# AI 数据网关（Cloudflare Worker）

issue #31 的 T1：在 7kolor.github.io 前面加一层**可选**的数据网关，像 GA4 记录人类访客一样记录 AI agent 的访问。

- 站点托管不变（GitHub Pages）。Worker 是引导而非强制：静态文件全保留，未识别 agent 照常放行
- 部署后网关地址形如 `https://7kolor-ai-gateway.<你的子域>.workers.dev`
- 边界（issue #31「明确不做」）：不做令牌门、不撤公开数据、不阻断未识别 agent

## 端点

| 路径 | 行为 |
|------|------|
| `/ai/<path>` | 代理回源 `7kolor.github.io/<path>`，**字节一致**；每次请求记录「时间 / 路径 / UA 分桶 / 脱敏 UA」 |
| `/ai/ping` | 自愿签到端点（llms.txt 引导配合的 agent 访问），返回极简 JSON，同样计数 |
| `/ai-stats` | 只读聚合 JSON：`by_agent` / `by_path` / `by_day` / `recent`（≤20 条，每条仅 ts/path/bucket） |

## 存储：Analytics Engine（免费版）

- 每请求一次 `writeDataPoint`：blob1=path、blob2=bucket、blob3=脱敏 UA、index1=bucket
- 免费额度 **10 万数据点/天写入 + 1 万读查询/天**（2026-10 时点未计费）
- 无需预建任何资源：dataset（`ai_gateway_log`）在首次写入时自动创建
- 为什么不用 KV：KV 免费档每天仅约 1000 次写，且计数器要读改写、有并发竞态；AWE 专为高频事件写入设计，天然匹配 issue 的「10 万请求/天」量级

## 开通步骤（约 10 分钟，一次性）

1. 注册 Cloudflare 免费账号；记下 workers.dev 子域（注册时设置，在 Workers & Pages 面板右侧可见）
2. 创建 API Token（Custom Token），两个权限：
   - `Account | Workers Scripts | Edit`（wrangler 部署）
   - `Account | Account Analytics | Read`（`/ai-stats` 运行时查 AWE SQL API，官方要求）
3. 本仓库 Settings → Secrets and variables → Actions → New repository secret，添加两个：
   - `CF_API_TOKEN`（上面的 token；**绝不写进代码或提交**）
   - `CF_ACCOUNT_ID`（32 位账号 ID，面板首页可见）
4. push `worker/**` 到 main → `.github/workflows/deploy-worker.yml` 自动部署，并把两个 secret 自动 `wrangler secret put` 进运行时（`/ai-stats` 查询用）
5. 部署成功后（后续小 commit）：
   - 从 Actions run 摘要复制真实网关 URL，写入 llms.txt 引导句与蜜罐链接
   - 设置 repo **variable**（不是 secret）`AI_GATEWAY_BASE` = 网关 URL，site-health 会开始非阻塞探测

## 本地开发与验收

```bash
cd worker
node --test test/*.test.mjs    # 单测（分桶 / 脱敏 / 统计形状 / handler 行为）
node scripts/smoke.mjs         # 本地冒烟：直连源站验证字节一致 + 分桶实测
npx wrangler dev               # http://localhost:8787（workerd 与部分 macOS libc++ 不兼容时，用上面的 smoke.mjs 等价验证）

# 字节一致验收（diff 为空即过）
curl -s http://localhost:8787/ai/reports.json -o /tmp/gw.json
curl -s https://7kolor.github.io/reports.json -o /tmp/origin.json
diff /tmp/gw.json /tmp/origin.json && echo BYTE-IDENTICAL

# 分桶/脱敏实测（模拟 UA）
curl -s -A "ChatGPT-User/1.0"  http://localhost:8787/ai/reports.json -o /dev/null -w '%{http_code}\n'
curl -s -A "Claude-User/1.0 (user: bob@7kolor.com)" http://localhost:8787/ai/llms.txt -o /dev/null -w '%{http_code}\n'
```

## 隐私边界

- 不记录完整 IP、不记录请求体；路径只存 pathname（**query 一律丢弃**）
- UA 必须先过 `sanitizeUa()` 才进存储层：邮箱打码（`jane@7kolor.com` → `j***@example.com`）、`user:/login=` 值打码、家目录用户名打码、截断 256 字符
- `/ai-stats` 只输出计数与 ≤20 条「时间/路径/桶」记录，**不输出任何 UA 值**（脱敏后的也不输出）
- 统计写失败绝不影响代理本身（fire-and-forget + catch）

## 代码结构

```
worker/
├── wrangler.toml        # name / dataset 与 src/config.js 有同步测试
├── src/config.js        # 纯常量：分桶规则表、存储上限、缓存节奏
├── src/ua.js            # 纯函数：bucketUa / sanitizeUa / sanitizePath
├── src/stats.js         # 纯函数：数据点形状 / SQL 文本 / /ai-stats 载荷组装
├── src/worker.js        # 入口：/ai/* 代理 + /ai/ping + /ai-stats
└── test/*.test.mjs      # node:test；经 tests/test_worker.py 桥入 guard 工作流
```
