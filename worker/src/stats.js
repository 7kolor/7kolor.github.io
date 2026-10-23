// 纯函数：Analytics Engine 数据点形状、SQL 文本、/ai-stats 载荷组装。
// 不依赖 Workers 运行时 API、无 I/O —— worker/test/stats.test.mjs 直接测试。

import {
  DATASET,
  RECENT_LIMIT,
  BY_DAY_LIMIT,
  BY_PATH_LIMIT,
  BUCKET_UNKNOWN,
} from "./config.js";

// 一个数据点 = 一次请求。列映射（AWE SQL 里 blob 从 1 开始编号）：
//   blob1=path  blob2=bucket  blob3=已脱敏 UA   index1=bucket（采样键）
// 注意：调用方必须先用 sanitizeUa() 处理 UA 再构造数据点 ——
// 本函数不做脱敏，测试会钉住「脱敏先于存储」的契约。
export function buildDataPoint({ path, bucket, ua }) {
  return {
    blobs: [path, bucket, ua],
    doubles: [],
    indexes: [bucket],
  };
}

// 四类聚合查询文本。计数一律用 SUM(_sample_interval) 加权：
// AWE 在高流量下会采样，加权后总数仍然正确。
// recent 依赖 SQL 的 ORDER BY ts DESC —— composePayload 只负责截断。
export function buildSqlQuery(kind) {
  switch (kind) {
    case "by_agent":
      return "SELECT blob2 AS bucket, SUM(_sample_interval) AS n FROM " + DATASET + " GROUP BY bucket ORDER BY n DESC FORMAT JSON";
    case "by_path":
      return "SELECT blob1 AS path, SUM(_sample_interval) AS n FROM " + DATASET + " GROUP BY path ORDER BY n DESC LIMIT " + BY_PATH_LIMIT + " FORMAT JSON";
    case "by_day":
      return "SELECT formatDateTime(toDateTime(timestamp), '%Y-%m-%d') AS day, SUM(_sample_interval) AS n FROM " + DATASET + " GROUP BY day ORDER BY day DESC LIMIT " + BY_DAY_LIMIT + " FORMAT JSON";
    case "recent":
      return "SELECT toDateTime(timestamp) AS ts, blob1 AS path, blob2 AS bucket FROM " + DATASET + " ORDER BY ts DESC LIMIT " + RECENT_LIMIT + " FORMAT JSON";
    default:
      throw new Error("unknown query kind: " + kind);
  }
}

// SQL API 响应兼容两种形态：{meta,data,rows,...}（FORMAT JSON）或裸数组。
export function parseSqlResponse(body) {
  if (Array.isArray(body)) return body;
  if (body && Array.isArray(body.data)) return body.data;
  return [];
}

// 组装 /ai-stats 载荷：恰好四个键（issue #31 验收标准），顺序固定。
export function composePayload({ agentRows, pathRows, dayRows, recentRows }) {
  return {
    by_agent: toCounts(agentRows, "bucket"),
    by_path: toCounts(pathRows, "path"),
    by_day: toCounts(dayRows, "day"),
    recent: toRecent(recentRows),
  };
}

// recent 每条只含 时间/路径/桶 三键 —— 不输出 UA（脱敏后的也不输出）。
function toRecent(rows) {
  return (rows ?? []).slice(0, RECENT_LIMIT).map((r) => ({
    ts: normalizeTs(r && r.ts),
    path: String((r && r.path) ?? "/"),
    bucket: String((r && r.bucket) ?? BUCKET_UNKNOWN),
  }));
}

function toCounts(rows, key) {
  const acc = new Map();
  for (const row of rows ?? []) {
    const k = String((row && row[key]) ?? BUCKET_UNKNOWN);
    const n = Number((row && row.n) ?? 0);
    if (!Number.isFinite(n)) continue;
    acc.set(k, (acc.get(k) ?? 0) + n);
  }
  // 计数降序、同数按键名升序 —— 输出顺序确定，测试可钉住。
  return Object.fromEntries(
    [...acc.entries()].sort((a, b) => b[1] - a[1] || (a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0)),
  );
}

// AWE 返回 ClickHouse 风格 "YYYY-MM-DD hh:mm:ss"（UTC）；统一成 ISO-8601。
export function normalizeTs(ts) {
  const s = String(ts ?? "").trim();
  const m = /^(\d{4}-\d{2}-\d{2})[ T](\d{2}:\d{2}:\d{2})/.exec(s);
  return m ? m[1] + "T" + m[2] + "Z" : s;
}
