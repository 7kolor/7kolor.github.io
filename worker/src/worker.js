// Cloudflare Worker 入口：7kolor.github.io 的 AI 数据网关（issue #31）。
//
//   /ai/*      把同路径代理回源站，字节一致（每次请求记录：路径 + UA 分桶 + 脱敏 UA）
//   /ai/ping   自愿签到端点（llms.txt 引导，返回极简 JSON，同样计数）
//   /ai-stats  只读聚合 JSON：by_agent / by_path / by_day / recent（≤20 条脱敏记录）
//
// 隐私契约：不存 IP、不存 query、不存请求体；UA 先脱敏再入存储层；
// /ai-stats 不输出任何 UA 值（含脱敏后的）。

import { bucketUa, sanitizePath, sanitizeUa } from "./ua.js";
import { buildDataPoint, buildSqlQuery, composePayload, parseSqlResponse } from "./stats.js";
import { ORIGIN_HOST, WORKER_NAME, STATS_CACHE_MS, SQL_TIMEOUT_MS } from "./config.js";

const ORIGIN = "https://" + ORIGIN_HOST;

// 允许透传的源站响应头（location 让 301/302 原样穿透；content-length 仅在
// body 未被运行时重编码时透传，见 handleProxy）。
const PASS_THROUGH_HEADERS = [
  "content-type",
  "etag",
  "last-modified",
  "cache-control",
  "content-disposition",
  "location",
];

export default {
  async fetch(request, env, ctx) {
    try {
      const url = new URL(request.url);
      if (url.pathname === "/ai-stats") return handleStats(request, env, ctx);
      if (url.pathname === "/ai" || url.pathname.startsWith("/ai/")) {
        return handleProxy(request, url, env, ctx);
      }
      return jsonResponse(
        { error: "not_found", hint: "machine data lives under /ai/* and /ai-stats" },
        404,
      );
    } catch (err) {
      return jsonResponse({ error: "internal_error", reason: reasonOf(err) }, 500);
    }
  },
};

// ---- /ai/* 代理 ----

async function handleProxy(request, url, env, ctx) {
  if (request.method !== "GET" && request.method !== "HEAD") {
    return jsonResponse({ error: "method_not_allowed" }, 405, { allow: "GET, HEAD" });
  }

  const ua = request.headers.get("user-agent") || "";
  logRequest(ctx, env, {
    path: sanitizePath(url.pathname),
    bucket: bucketUa(ua),
    ua: ua,
  });

  // /ai/ping 是 llms.txt 引导的自愿签到端点：返回极简 JSON（同样计入统计），
  // 不代理源站（源站并没有 /ping 这个文件）。
  const targetPath = url.pathname.replace(/^\/ai/, "") || "/";
  if (targetPath === "/ping") {
    const pingHeaders = { "cache-control": "no-store" };
    if (request.method === "HEAD") return new Response(null, { status: 200, headers: pingHeaders });
    return jsonResponse({ ok: true, gateway: WORKER_NAME }, 200, pingHeaders);
  }

  const target = ORIGIN + targetPath + (url.search || "");
  let originRes;
  try {
    originRes = await fetch(target, {
      method: request.method,
      headers: {
        "user-agent": ua || WORKER_NAME + "/1",
        accept: request.headers.get("accept") || "*/*",
      },
      redirect: "manual", // 重定向原样穿透，像任何镜像一样
    });
  } catch (err) {
    return jsonResponse({ error: "origin_unreachable", reason: reasonOf(err) }, 502);
  }

  const headers = new Headers();
  for (const name of PASS_THROUGH_HEADERS) {
    const value = originRes.headers.get(name);
    if (value != null) headers.set(name, value);
  }
  // body 被运行时透明解压时 content-length 会失配，只在没有 content-encoding
  // 时透传（curl 不带压缩头访问两端，diff 仍为空）。
  if (!originRes.headers.get("content-encoding")) {
    const len = originRes.headers.get("content-length");
    if (len != null) headers.set("content-length", len);
  }
  headers.set("x-ai-gateway", WORKER_NAME + "/1 (+" + ORIGIN_HOST + ")");

  return new Response(originRes.body, { status: originRes.status, headers: headers });
}

// ---- /ai-stats ----

// 进程内缓存：/ai-stats 读多写少，且 AWE 按查询计费（免费 1 万次/天），
// 60s 进程内缓存 + 30s 边缘缓存对这种统计页绰绰有余。
let statsCache = { at: 0, payload: null };

async function handleStats(request, env, ctx) {
  const ua = request.headers.get("user-agent") || "";
  logRequest(ctx, env, {
    path: sanitizePath(new URL(request.url).pathname),
    bucket: bucketUa(ua),
    ua: ua,
  });

  if (statsCache.payload && Date.now() - statsCache.at < STATS_CACHE_MS) {
    return jsonResponse(statsCache.payload, 200, { "cache-control": "public, max-age=30" });
  }

  const accountId = (env && env.CF_ACCOUNT_ID) || "";
  const apiToken = (env && env.CF_API_TOKEN) || "";
  if (!accountId || !apiToken) {
    return jsonResponse(
      {
        error: "stats_unavailable",
        reason:
          "runtime secrets CF_ACCOUNT_ID / CF_API_TOKEN are not configured yet " +
          "(deployed by .github/workflows/deploy-worker.yml, see worker/README.md)",
      },
      503,
      { "cache-control": "no-store" },
    );
  }

  try {
    const kinds = ["by_agent", "by_path", "by_day", "recent"];
    const rows = await Promise.all(kinds.map((k) => queryRows(accountId, apiToken, buildSqlQuery(k))));
    const payload = composePayload({
      agentRows: rows[0],
      pathRows: rows[1],
      dayRows: rows[2],
      recentRows: rows[3],
    });
    statsCache = { at: Date.now(), payload: payload };
    return jsonResponse(payload, 200, { "cache-control": "public, max-age=30" });
  } catch (err) {
    return jsonResponse({ error: "stats_query_failed", reason: reasonOf(err) }, 502, {
      "cache-control": "no-store",
    });
  }
}

async function queryRows(accountId, apiToken, sql) {
  const endpoint =
    "https://api.cloudflare.com/client/v4/accounts/" +
    encodeURIComponent(accountId) +
    "/analytics_engine/sql";
  const res = await fetch(endpoint, {
    method: "POST",
    headers: {
      authorization: "Bearer " + apiToken,
      "content-type": "text/plain; charset=utf-8",
    },
    body: sql,
    signal: AbortSignal.timeout(SQL_TIMEOUT_MS),
  });
  if (!res.ok) throw new Error("analytics sql api returned " + res.status);
  return parseSqlResponse(await res.json());
}

// ---- 记录与工具 ----

// 请求日志：UA 在这里、在数据点构造之前脱敏 —— 未脱敏的 UA 不存在任何
// 能进入存储层的路径（issue #31 验收标准）。写失败绝不影响代理本身。
function logRequest(ctx, env, { path, bucket, ua }) {
  try {
    const binding = env && env.AI_LOG;
    if (!binding || typeof binding.writeDataPoint !== "function") return;
    const dataPoint = buildDataPoint({ path: path, bucket: bucket, ua: sanitizeUa(ua) });
    if (ctx && typeof ctx.waitUntil === "function") {
      ctx.waitUntil(Promise.resolve(binding.writeDataPoint(dataPoint)));
    } else {
      binding.writeDataPoint(dataPoint);
    }
  } catch (err) {
    console.error("ai-gateway: writeDataPoint failed:", reasonOf(err));
  }
}

function reasonOf(err) {
  return String((err && err.message) || err);
}

function jsonResponse(obj, status, extraHeaders) {
  return new Response(JSON.stringify(obj) + "\n", {
    status: status,
    headers: Object.assign({ "content-type": "application/json; charset=utf-8" }, extraHeaders || {}),
  });
}
