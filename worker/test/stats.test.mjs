import test from "node:test";
import assert from "node:assert/strict";

import {
  buildDataPoint,
  buildSqlQuery,
  composePayload,
  parseSqlResponse,
  normalizeTs,
} from "../src/stats.js";
import { RECENT_LIMIT, DATASET, BY_PATH_LIMIT, BY_DAY_LIMIT } from "../src/config.js";

test("buildDataPoint maps path/bucket/ua onto the AWE columns", () => {
  assert.deepEqual(
    buildDataPoint({ path: "/ai/reports.json", bucket: "openai-crawler", ua: "GPTBot/1.2" }),
    {
      blobs: ["/ai/reports.json", "openai-crawler", "GPTBot/1.2"],
      doubles: [],
      indexes: ["openai-crawler"],
    },
  );
});

test("buildSqlQuery covers the four aggregation kinds on the configured dataset", () => {
  for (const kind of ["by_agent", "by_path", "by_day", "recent"]) {
    const sql = buildSqlQuery(kind);
    assert.ok(sql.includes(" FROM " + DATASET + " "), sql);
    assert.ok(sql.endsWith("FORMAT JSON"), sql);
  }
  assert.ok(buildSqlQuery("by_agent").includes("SUM(_sample_interval) AS n"));
  assert.ok(buildSqlQuery("by_path").includes("LIMIT " + BY_PATH_LIMIT));
  assert.ok(buildSqlQuery("by_day").includes("LIMIT " + BY_DAY_LIMIT));
  assert.ok(buildSqlQuery("recent").includes("LIMIT " + RECENT_LIMIT));
  assert.ok(buildSqlQuery("by_day").includes("formatDateTime(toDateTime(timestamp), '%Y-%m-%d')"));
  assert.throws(() => buildSqlQuery("nope"));
});

test("parseSqlResponse accepts both response shapes and junk", () => {
  assert.deepEqual(parseSqlResponse({ data: [{ a: 1 }], rows: 1 }), [{ a: 1 }]);
  assert.deepEqual(parseSqlResponse([{ a: 1 }]), [{ a: 1 }]);
  assert.deepEqual(parseSqlResponse(null), []);
  assert.deepEqual(parseSqlResponse({}), []);
});

test("composePayload returns exactly the four required keys in order", () => {
  const payload = composePayload({
    agentRows: [
      { bucket: "unknown", n: 5 },
      { bucket: "openai-chatgpt", n: 3 },
      { bucket: "openai-chatgpt", n: 2 },
    ],
    pathRows: [{ path: "/ai/reports.json", n: 7 }],
    dayRows: [{ day: "2026-10-22", n: 10 }],
    recentRows: [{ ts: "2026-10-22 08:15:00", path: "/ai/reports.json", bucket: "unknown" }],
  });
  assert.deepEqual(Object.keys(payload), ["by_agent", "by_path", "by_day", "recent"]);
  assert.deepEqual(payload.by_agent, { "openai-chatgpt": 5, unknown: 5 });
  assert.deepEqual(payload.by_path, { "/ai/reports.json": 7 });
  assert.deepEqual(payload.by_day, { "2026-10-22": 10 });
  assert.deepEqual(payload.recent, [
    { ts: "2026-10-22T08:15:00Z", path: "/ai/reports.json", bucket: "unknown" },
  ]);
  for (const r of payload.recent) {
    assert.deepEqual(Object.keys(r), ["ts", "path", "bucket"]);
  }
});

test("recent entries are capped at 20 and keep SQL order (newest first)", () => {
  const rows = Array.from({ length: 50 }, (_, i) => ({
    ts: "2026-10-22 00:" + String(i).padStart(2, "0") + ":00",
    path: "/p" + i,
    bucket: "unknown",
  }));
  const payload = composePayload({ agentRows: [], pathRows: [], dayRows: [], recentRows: rows });
  assert.equal(payload.recent.length, RECENT_LIMIT);
  assert.equal(payload.recent[0].path, "/p0");
  assert.equal(payload.recent[RECENT_LIMIT - 1].path, "/p" + (RECENT_LIMIT - 1));
});

test("normalizeTs converts AWE timestamps to ISO-8601 UTC", () => {
  assert.equal(normalizeTs("2026-10-22 08:15:00"), "2026-10-22T08:15:00Z");
  assert.equal(normalizeTs("2026-10-22T08:15:00"), "2026-10-22T08:15:00Z");
  assert.equal(normalizeTs("2026-10-22 08:15:00.123"), "2026-10-22T08:15:00Z");
  assert.equal(normalizeTs(""), "");
  assert.equal(normalizeTs(null), "");
});
