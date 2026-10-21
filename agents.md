# 7Kolor 开发规范

> 本文档供开发者和 AI 助手参考，包含内部技术规范、发布流程和目录结构。

---

## 技术栈

- **前端**: 纯 HTML/CSS/JS，无框架依赖
- **构建**: Python 3 标准库（零外部依赖）
- **部署**: GitHub Pages + GitHub Actions
- **测试**: unittest（36 个测试用例）
- **CI**: guard（安全门禁 + 测试/产物新鲜度门禁）+ publish（自动发布）
- **本地钩子**: pre-commit（身份校验 + staged 敏感信息扫描）+ pre-push（全量测试 + meta 校验 + 全量敏感信息扫描）

---

## 目录结构

```
.
├── index.html               # 首页（英雄区 + 数据资产 + 情报卡片）
├── about.html               # 关于页
├── llms.txt                 # 给阅读型 agent 的站点导览（报告列表为 AUTO 块，构建生成）
├── robots.txt               # 全放行 + 指向 sitemap
├── sitemap.xml              # 全站 URL 地图（构建生成，基于 git 跟踪文件，重定向别名除外）
├── weekly/                  # 每周情报内容
│   ├── index.html           # 周报归档页
│   └── 2026-W34/            # 一期周报
│       ├── index.html       # 双语正文（带 data-zh / data-en 属性）
│       ├── meta.json        # 元数据（标题/日期/来源）
│       ├── report-zh.html   # 单语版（构建生成）
│       └── report-en.html   # 单语版（构建生成）
├── assets/                  # CSS / JS / 图片
├── scripts/                 # 构建脚本
├── tests/                   # 单元测试
├── templates/               # 发布工作流说明
│   └── partials/            # 页眉 header.html / 页脚 footer.html（全站唯一来源）
└── .github/workflows/       # CI/CD
```

---

## 核心脚本

| 脚本 | 职责 | 使用场景 |
|------|------|---------|
| `scripts/publish.py` | 一键发布：校验 meta.json → 生成单语页 → 更新首页/归档/feed | CI 或本地发布 |
| `scripts/build_i18n.py` | 生成单语页 report-zh/en | 双语内容分离 |
| `scripts/build_site.py` | 更新首页卡片、归档列表、feed.xml、sitemap.xml、llms.txt 报告列表，并同步全站页眉/页脚/最新周报 CTA | 只动 AUTO 块，不碰手写内容；sitemap/llms 基于 git 跟踪文件与已注册 MODULES 自动生成：新增一期内容零登记，新增内容类型需按下方步骤注册 |
| `scripts/check_sanitize.py` | 安全门禁 | 检查历史/工作区敏感信息 |

---

## 发布流程

### 自动发布（推荐）

```bash
# 1. 复制上一期作为模板
cp -r weekly/2026-W34 weekly/2026-W35
rm weekly/2026-W35/meta.json

# 2. 编辑正文（双语，data-zh / data-en 属性）与 meta.json
#    详见 templates/weekly-report.md

# 3. 本地构建（生成归档/feed/sitemap/llms 更新），测试后 push
python3 scripts/publish.py
python3 -m unittest discover -s tests
git add -A
git commit -m "feat: 2026 W35 周报"
git push   # pre-push 钩子跑全量门禁；CI guard 再挡一次，不过关无法合并
```

> 忘了跑 `publish.py` 就 push：CI guard 的 "Generated files must be up to date" 会重新构建并
> 检查工作区（含 untracked）是否干净，产物过期或漏 add 新页都会红。注意 guard 与 publish 是
> 两个独立触发的 workflow，guard 红不会阻止 publish —— 但 stale 产物上线后下次任一内容 push
> 会被门禁拦住，所以应在 guard 变绿后再合并/推送。
>
> **新增内容类型（kind）注册步骤**：① `build_site.py` 的 MODULES + KIND_LABEL ② `publish.py`
> 的 REQUIRED_BY_KIND ③ `build_i18n.py` 的 CONTENT_ROOTS ④ 首页预留 `<!-- AUTO:cards-<kind> -->` 块。
> 注册后该类型的每期内容对 sitemap / llms.txt / feed / 归档全部自动生效，无需再改代码。
> 新增一期内容（已有类型）则什么都不用登记。

### 手动构建（本地预览）

```bash
python3 scripts/publish.py            # 校验 + 全量构建
python3 scripts/publish.py --check    # 只校验，不写文件
python3 -m http.server 4000           # 本地预览
```

---

## meta.json 格式

```json
{
  "kind": "weekly",
  "id": "2026-W35",
  "week_label_zh": "2026 W35 周报",
  "week_label_en": "2026 W35 Weekly Report",
  "title_zh": "本期中文标题",
  "title_en": "English title",
  "desc_zh": "中文摘要（首页卡片 + RSS 用）",
  "desc_en": "English summary",
  "date_range": "2026-08-30 ~ 09-05",
  "date": "2026-09-05",
  "sources": "Reddit · HN · IH · PH"
}
```

### kind 类型

| kind | 说明 |
|------|------|
| `weekly` | 每周情报 |
| `analysis` | 专项分析 |
| `insights` | 行业洞察 |
| `cases` | 成功案例 |

新内容类型需完成 4 步注册（见「发布流程」上方的注册步骤清单）；已有类型新增一期只需建目录 + meta.json + 正文。

---

## 开发命令

```bash
# 运行全部测试（36 个）
python3 -m unittest discover -s tests -v

# 本地预览
python3 -m http.server 4000
```

---

## 内容编辑规范

1. **双语内容**：使用 `data-zh` / `data-en` 属性标记
2. **模板参考**：`templates/weekly-report.md`
3. **AUTO 块**：首页/归档/feed 有 `<!-- AUTO:xxx -->` 标记，构建脚本只修改这些区域
4. **安全门禁**：CI 会自动扫描敏感信息，避免泄露
