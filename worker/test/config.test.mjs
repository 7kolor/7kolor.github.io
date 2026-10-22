import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

import { WORKER_NAME, DATASET, STATS_BINDING } from "../src/config.js";

test("wrangler.toml and config.js stay in sync", () => {
  const toml = readFileSync(new URL("../wrangler.toml", import.meta.url), "utf8");
  const value = (key) => {
    const m = new RegExp("(?:^|\\n)" + key + ' = "([^"]+)"').exec(toml);
    return m ? m[1] : null;
  };
  assert.equal(value("name"), WORKER_NAME);
  assert.equal(value("binding"), STATS_BINDING);
  assert.equal(value("dataset"), DATASET);
  assert.equal(value("main"), "src/worker.js");
});

test("pure modules never import Workers-runtime APIs", () => {
  for (const f of ["src/config.js", "src/ua.js", "src/stats.js"]) {
    const src = readFileSync(new URL("../" + f, import.meta.url), "utf8");
    assert.ok(!src.includes('from "cloudflare:'), f + " imports a cloudflare: module");
    assert.ok(!src.includes("await fetch("), f + " does I/O (must stay pure)");
  }
});
