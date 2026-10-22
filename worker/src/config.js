// Pure constants shared by the Worker entry and the node test-suite.
// 依仓库惯例零依赖：本文件（以及 ua.js / stats.js）不得 import 任何
// Workers 运行时 API（worker/test/config.test.mjs 会强制检查）。

export const ORIGIN_HOST = "7kolor.github.io";
export const WORKER_NAME = "7kolor-ai-gateway";

// 必须与 wrangler.toml 的 [[analytics_engine_datasets]] 一致。
export const STATS_BINDING = "AI_LOG";
export const DATASET = "ai_gateway_log";

// ---- 存储上限（脱敏后的值才会写进来）----
export const UA_MAX_STORED = 256; // 存储的 UA 字符数上限
export const PATH_MAX_STORED = 256; // 存储的路径字符数上限

// ---- /ai-stats 输出形状（issue #31 验收标准）----
export const RECENT_LIMIT = 20; // recent 最多 20 条
export const BY_DAY_LIMIT = 90; // by_day 最多保留 90 天
export const BY_PATH_LIMIT = 100; // by_path 最多保留 100 个路径

// ---- /ai-stats 查询节奏 ----
export const STATS_CACHE_MS = 60_000; // 进程内缓存，省 AWE 读查询（免费 1 万/天）
export const SQL_TIMEOUT_MS = 8_000;

// UA 分桶规则：有序、大小写不敏感的子串匹配，先命中先用。
// 顺序即优先级：更具体的 token 放在其可能被包含的更泛 token 之前。
// 验收标准（issue #31）：ChatGPT-User→openai-chatgpt、Claude-User→
// anthropic-claude、GPTBot→openai-crawler、curl/8.x→unknown。
export const UA_RULES = [
  ["chatgpt-user", "openai-chatgpt"], // ChatGPT 联网浏览（网页版带浏览）
  ["oai-searchbot", "openai-searchbot"], // OpenAI 搜索爬虫
  ["gptbot", "openai-crawler"], // OpenAI 训练爬虫
  ["claude-user", "anthropic-claude"], // Claude 联网浏览（网页版带浏览）
  ["claudebot", "anthropic-crawler"], // Anthropic 爬虫
  ["claude-cli", "agent-claude-code"], // 终端 agent：Claude Code
  ["codex", "agent-codex"], // 终端 agent：OpenAI Codex CLI
  ["opencode", "agent-opencode"], // 终端 agent：OpenCode
  ["perplexity-user", "perplexity-user"], // Perplexity 联网浏览
  ["perplexitybot", "perplexity-crawler"], // Perplexity 爬虫
  ["google-extended", "google-extended"], // Google-Extended（Gemini 训练抓取）
  ["bytespider", "bytedance-crawler"], // 字节跳动爬虫
];

// 兜底桶：浏览器、curl、未知脚本、空 UA 一律归 unknown（不阻断、照常代理）。
export const BUCKET_UNKNOWN = "unknown";
