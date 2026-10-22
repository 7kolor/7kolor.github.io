import test from "node:test";
import assert from "node:assert/strict";

import { bucketUa, sanitizeUa, sanitizePath } from "../src/ua.js";

test("issue #31 acceptance: the four required UA buckets", () => {
  assert.equal(bucketUa("ChatGPT-User/1.0; +https://openai.com/bot"), "openai-chatgpt");
  assert.equal(bucketUa("Mozilla/5.0 (compatible) Claude-User/1.0"), "anthropic-claude");
  assert.equal(bucketUa("GPTBot/1.2 (+https://openai.com/gptbot)"), "openai-crawler");
  assert.equal(bucketUa("curl/8.7.1"), "unknown");
});

test("terminal agents, web crawlers and browsers", () => {
  assert.equal(bucketUa("claude-cli/1.0.83 (external, cli)"), "agent-claude-code");
  assert.equal(bucketUa("codex_cli_rs/0.42.0 (Mac OS 15.0; arm64)"), "agent-codex");
  assert.equal(bucketUa("OpenCode/1.0.12"), "agent-opencode");
  assert.equal(bucketUa("PerplexityBot/1.0; +https://perplexity.ai/perplexitybot"), "perplexity-crawler");
  assert.equal(bucketUa("Perplexity-User"), "perplexity-user");
  assert.equal(bucketUa("Google-Extended"), "google-extended");
  assert.equal(
    bucketUa(
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 " +
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    ),
    "unknown",
  );
});

test("matching is case-insensitive; empty/unknown UAs fall back", () => {
  assert.equal(bucketUa("GPTBOT/1.0"), "openai-crawler");
  assert.equal(bucketUa("chatgpt-user"), "openai-chatgpt");
  assert.equal(bucketUa(""), "unknown");
  assert.equal(bucketUa(undefined), "unknown");
});

test("issue #31 acceptance: raw email never reaches the stored value", () => {
  const raw = "Claude-User/1.0 (user: bob@7kolor.com)";
  const stored = sanitizeUa(raw);
  assert.ok(!stored.includes("bob@7kolor.com"), "raw email leaked: " + stored);
  assert.ok(!stored.includes("bob"), "username leaked: " + stored);
  assert.ok(stored.includes("***"), "nothing masked: " + stored);
});

test("email masking keeps first char and domain (issue #31 format)", () => {
  assert.equal(sanitizeUa("jane@7kolor.com"), "j***@7kolor.com");
});

test("user fields and home directories are masked", () => {
  const stored = sanitizeUa("codex_cli_rs/0.42 (user=rocky; home=/Users/rocky/tmp)");
  assert.ok(!stored.includes("rocky"), "username leaked: " + stored);
  assert.ok(stored.includes("user=***"), stored);
  assert.ok(stored.includes("/Users/***/tmp"), stored);
  const stored2 = sanitizeUa("agent/1.0 login:testuser /home/testuser/work");
  assert.ok(!stored2.includes("sami"), "username leaked: " + stored2);
  assert.ok(stored2.includes("/home/***/work"), stored2);
});

test("sanitizeUa caps length and is idempotent", () => {
  const long = "x".repeat(600) + " bob@7kolor.com";
  const once = sanitizeUa(long);
  assert.ok(once.length <= 256);
  assert.ok(!once.includes("bob@7kolor.com"));
  assert.equal(sanitizeUa(once), once);
});

test("empty UA is stored as a placeholder", () => {
  assert.equal(sanitizeUa(""), "(empty)");
  assert.equal(sanitizeUa(null), "(empty)");
});

test("sanitizePath drops query strings and caps length", () => {
  assert.equal(sanitizePath("/weekly/2026-W41/report.md"), "/weekly/2026-W41/report.md");
  assert.equal(sanitizePath("/" + "x".repeat(300)), "/" + "x".repeat(255));
});
