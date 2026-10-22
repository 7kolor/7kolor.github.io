// 纯函数：UA 分桶 + 脱敏 + 路径清洗。
// 不依赖 Workers 运行时 API、无 I/O —— worker/test/ua.test.mjs（node:test）
// 直接测试，guard 工作流经 tests/test_worker.py 桥接执行。

import {
  UA_RULES,
  BUCKET_UNKNOWN,
  UA_MAX_STORED,
  PATH_MAX_STORED,
} from "./config.js";

// 把原始 User-Agent 归入分桶。大小写不敏感，按 UA_RULES 顺序首个命中的桶；
// 浏览器 / curl / 未知脚本 / 空值一律 unknown。
export function bucketUa(ua) {
  const s = String(ua ?? "").toLowerCase();
  for (const [token, bucket] of UA_RULES) {
    if (s.includes(token)) return bucket;
  }
  return BUCKET_UNKNOWN;
}

// 邮箱打码：保留首字符与域名 —— "jane@7kolor.com" -> "j***@example.com"
//（issue #31 给出的格式）。任何邮箱必须先被本规则覆盖，才能进入存储层。
const EMAIL_RE = /([A-Za-z0-9._%+-])[A-Za-z0-9._%+-]*@([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)/g;

// 用户名式键值打码：user: bob / login=rocky / uid: alice -> "***"
//（Claude Code 等终端 agent 会在 UA 里自报用户名/邮箱）。
// 值终止字符集排除空白与 , ; ) ] } " '
const USER_FIELD_RE = /((?:user|username|login|account|uid)\s*[=:]\s*)("[^"]*"|[^\s,;)\]}"']+)/gi;

// 家目录用户名打码：/Users/rocky/... /home/rocky/... -> /***/
const HOME_DIR_RE = /(\/(?:Users|home)\/)[^/\s,;)\]}"']+/g;

// UA 脱敏：这是唯一允许把 UA 写进存储层的通道（worker.js 只能先调它）。
export function sanitizeUa(ua) {
  let s = String(ua ?? "").trim();
  if (s === "") return "(empty)";
  s = s.replace(EMAIL_RE, "$1***@$2");
  s = s.replace(USER_FIELD_RE, "$1***");
  s = s.replace(HOME_DIR_RE, "$1***");
  if (s.length > UA_MAX_STORED) s = s.slice(0, UA_MAX_STORED);
  return s;
}

// 路径清洗：只保留 pathname（query 里可能出现 token/邮箱等 PII，一律丢弃），
// 并截断到存储上限。
export function sanitizePath(pathname) {
  let p = String(pathname ?? "/");
  if (p === "") p = "/";
  if (p.length > PATH_MAX_STORED) p = p.slice(0, PATH_MAX_STORED);
  return p;
}
