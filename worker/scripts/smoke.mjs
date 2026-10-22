// 本地冒烟：用真实源站（7kolor.github.io）验证 /ai/* 代理字节一致 + UA 分桶/脱敏。
// 用法：node worker/scripts/smoke.mjs   （退出码非 0 即失败）
// 说明：workerd 在部分 macOS 上无法运行（libc++ 符号缺失），本脚本用 node 的
// fetch/Request/Response 直接驱动 worker.js 的 fetch 处理器，行为与线上等价。

import assert from "node:assert/strict";

import worker from "../src/worker.js";

const captured = [];
const env = {
  AI_LOG: {
    writeDataPoint(dp) {
      captured.push(dp);
    },
  },
  // 故意不设 CF_ACCOUNT_ID / CF_API_TOKEN：本地验证 /ai-stats 的 503 形状
};
const ctx = { waitUntil: () => {} };

const ORIGIN = "https://7kolor.github.io";

async function proxyOf(path, ua) {
  const headers = ua ? { "user-agent": ua } : {};
  const res = await worker.fetch(new Request("https://gw.test" + path, { headers }), env, ctx);
  return { status: res.status, body: Buffer.from(await res.arrayBuffer()) };
}

async function originOf(path) {
  const res = await fetch(ORIGIN + path, { redirect: "manual" });
  return { status: res.status, body: Buffer.from(await res.arrayBuffer()) };
}

let failures = 0;

// 1) 字节一致：Worker /ai/<path> vs 源站 <path>
const paths = [
  "/reports.json",
  "/weekly/2026-W41/report.md",
  "/weekly/2026-W41/report-en.md",
  "/llms.txt",
  "/feed.xml",
  "/sitemap.xml",
  "/",
];
for (const p of paths) {
  const gw = await proxyOf("/ai" + p, "curl/8.7.1");
  const origin = await originOf(p);
  const same = gw.status === origin.status && gw.body.equals(origin.body);
  console.log(
    (same ? "BYTE-IDENTICAL" : "MISMATCH") + "  " + p +
    "  gw=" + gw.status + "/" + gw.body.length + "B" +
    "  origin=" + origin.status + "/" + origin.body.length + "B",
  );
  if (!same) failures += 1;
}

// 2) 分桶实测（issue #31 验收的四类模拟 UA）
const uaCases = [
  ["ChatGPT-User/1.0; +https://openai.com/bot", "openai-chatgpt"],
  ["Mozilla/5.0 (compatible) Claude-User/1.0", "anthropic-claude"],
  ["GPTBot/1.2", "openai-crawler"],
  ["curl/8.7.1", "unknown"],
  ["Claude-User/1.0 (user: bob@7kolor.com)", "anthropic-claude"],
  ["claude-cli/1.0.83 (external, cli)", "agent-claude-code"],
];
const before = captured.length;
for (const [ua, bucket] of uaCases) {
  await proxyOf("/ai/reports.json", ua);
}
for (let i = 0; i < uaCases.length; i += 1) {
  const [ua, bucket] = uaCases[i];
  const dp = captured[before + i];
  const ok = dp.blobs[1] === bucket;
  console.log((ok ? "BUCKET-OK  " : "BUCKET-FAIL") + "  " + bucket.padEnd(18) + " <= " + ua);
  console.log("           stored-ua: " + JSON.stringify(dp.blobs[2]));
  if (!ok) failures += 1;
}

// 3) 邮箱必须打码后才进存储层
const withEmail = captured[before + uaCases.length - 2].blobs[2];
try {
  assert.ok(!withEmail.includes("bob@7kolor.com"), "raw email reached storage");
  assert.ok(withEmail.includes("***"), "email not masked");
  console.log("MASK-OK        " + JSON.stringify(withEmail));
} catch (err) {
  console.log("MASK-FAIL      " + String(err));
  failures += 1;
}

// 4) /ai-stats 无 secret → 503 + 明确 reason（本地无 CF 运行时凭据）
const stats = await proxyOf("/ai-stats", "curl/8.7.1");
try {
  const body = JSON.parse(stats.body.toString("utf8"));
  assert.equal(stats.status, 503);
  assert.equal(body.error, "stats_unavailable");
  console.log("STATS-503-OK   " + JSON.stringify(body));
} catch (err) {
  console.log("STATS-FAIL     status=" + stats.status + " body=" + stats.body.toString("utf8").slice(0, 200));
  failures += 1;
}

// 5) 自愿签到端点
const ping = await proxyOf("/ai/ping", "OpenCode/1.0");
try {
  const body = JSON.parse(ping.body.toString("utf8"));
  assert.equal(ping.status, 200);
  assert.deepEqual(body, { ok: true, gateway: "7kolor-ai-gateway" });
  console.log("PING-OK        " + JSON.stringify(body));
} catch (err) {
  console.log("PING-FAIL      status=" + ping.status);
  failures += 1;
}

console.log("");
console.log("captured datapoints: " + captured.length);
if (failures > 0) {
  console.log("SMOKE FAILED: " + failures + " failure(s)");
  process.exit(1);
}
console.log("SMOKE OK");
