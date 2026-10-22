import test from "node:test";
import assert from "node:assert/strict";

import worker from "../src/worker.js";

// 离线 handler 测试：mock 全局 fetch（不真连源站），mock AI_LOG 绑定捕获数据点，
// 验证路由、字节透传、脱敏先于存储、/ai-stats 无 secret 时的形状。

function makeEnv() {
  const captured = [];
  const env = {
    AI_LOG: {
      writeDataPoint(dp) {
        captured.push(dp);
      },
    },
    captured,
  };
  return env;
}

const realFetch = globalThis.fetch;

test("GET /ai/reports.json proxies the origin response untouched and logs the request", async () => {
  globalThis.fetch = async () =>
    new Response("origin-bytes", {
      status: 200,
      headers: { "content-type": "application/json; charset=utf-8", etag: "abc123" },
    });
  const env = makeEnv();
  const waiters = [];
  const req = new Request("https://gw.test/ai/reports.json", {
    headers: { "user-agent": "GPTBot/1.2" },
  });
  const res = await worker.fetch(req, env, { waitUntil: (p) => waiters.push(p) });
  assert.equal(res.status, 200);
  assert.equal(await res.text(), "origin-bytes");
  assert.equal(res.headers.get("etag"), "abc123");
  assert.match(res.headers.get("x-ai-gateway") ?? "", /7kolor-ai-gateway/);
  await Promise.all(waiters);
  assert.equal(env.captured.length, 1);
  const dp = env.captured[0];
  assert.deepEqual(dp.blobs[0], "/ai/reports.json");
  assert.deepEqual(dp.blobs[1], "openai-crawler");
  assert.deepEqual(dp.indexes[0], "openai-crawler");
});

test("UA is sanitized BEFORE it reaches the storage layer (issue #31)", async () => {
  globalThis.fetch = async () => new Response("x", { status: 200 });
  const env = makeEnv();
  const waiters = [];
  const req = new Request("https://gw.test/ai/llms.txt", {
    headers: { "user-agent": "Claude-User/1.0 (user: bob@7kolor.com)" },
  });
  await worker.fetch(req, env, { waitUntil: (p) => waiters.push(p) });
  await Promise.all(waiters);
  const storedUa = env.captured[0].blobs[2];
  assert.ok(!storedUa.includes("bob@7kolor.com"), "raw email reached storage: " + storedUa);
  assert.ok(storedUa.includes("***"), storedUa);
  assert.deepEqual(env.captured[0].blobs[1], "anthropic-claude");
});

test("query strings are never stored", async () => {
  globalThis.fetch = async () => new Response("x", { status: 200 });
  const env = makeEnv();
  const waiters = [];
  const req = new Request("https://gw.test/ai/reports.json?token=SECRET");
  await worker.fetch(req, env, { waitUntil: (p) => waiters.push(p) });
  await Promise.all(waiters);
  assert.deepEqual(env.captured[0].blobs[0], "/ai/reports.json");
});

test("GET /ai/ping returns the check-in JSON and still counts", async () => {
  globalThis.fetch = async () => {
    throw new Error("ping must not hit the origin");
  };
  const env = makeEnv();
  const waiters = [];
  const req = new Request("https://gw.test/ai/ping", {
    headers: { "user-agent": "OpenCode/1.0" },
  });
  const res = await worker.fetch(req, env, { waitUntil: (p) => waiters.push(p) });
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.deepEqual(body, { ok: true, gateway: "7kolor-ai-gateway" });
  await Promise.all(waiters);
  assert.equal(env.captured.length, 1);
  assert.deepEqual(env.captured[0].blobs[1], "agent-opencode");
});

test("HEAD /ai/ping returns 200 without a body", async () => {
  globalThis.fetch = async () => new Response("x");
  const res = await worker.fetch(new Request("https://gw.test/ai/ping", { method: "HEAD" }), makeEnv(), null);
  assert.equal(res.status, 200);
  assert.equal(await res.text(), "");
});

test("/ai-stats without runtime secrets returns a clear 503 JSON", async () => {
  globalThis.fetch = async () => {
    throw new Error("stats must not need the origin");
  };
  const env = makeEnv();
  const waiters = [];
  const res = await worker.fetch(new Request("https://gw.test/ai-stats"), env, {
    waitUntil: (p) => waiters.push(p),
  });
  assert.equal(res.status, 503);
  const body = await res.json();
  assert.deepEqual(body.error, "stats_unavailable");
  await Promise.all(waiters);
  assert.equal(env.captured.length, 1); // stats requests are logged too
});

test("unknown paths get a JSON 404; non-GET/HEAD get 405", async () => {
  globalThis.fetch = async () => new Response("x");
  const res404 = await worker.fetch(new Request("https://gw.test/other"), makeEnv(), null);
  assert.equal(res404.status, 404);
  const res405 = await worker.fetch(
    new Request("https://gw.test/ai/reports.json", { method: "POST" }),
    makeEnv(),
    null,
  );
  assert.equal(res405.status, 405);
});

test("missing AI_LOG binding never breaks the proxy", async () => {
  globalThis.fetch = async () => new Response("ok", { status: 200 });
  const res = await worker.fetch(
    new Request("https://gw.test/ai/reports.json"),
    {}, // no AI_LOG binding
    { waitUntil: () => {} },
  );
  assert.equal(res.status, 200);
  assert.equal(await res.text(), "ok");
});

test("globalThis.fetch restored after the suite", () => {
  globalThis.fetch = realFetch;
  assert.equal(globalThis.fetch, realFetch);
});
