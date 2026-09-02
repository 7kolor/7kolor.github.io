"""One-command publish: validate → roll out single-language pages → rebuild site.

Usage:
    python3 scripts/publish.py            # full build (used by CI and locally)
    python3 scripts/publish.py --check    # validate only, no writes

Steps:
  1. Discover every content dir (weekly/, analysis/, insights/, cases/ ...)
  2. Validate each meta.json (required fields per kind); fail fast on error
  3. Generate report-zh.html / report-en.html for every bilingual content dir
  4. Rebuild homepage cards, archive list and feed.xml (build_site)
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_i18n
import build_site

# Fields every item must provide, regardless of kind.
REQUIRED_COMMON = ("kind", "id", "title_zh", "title_en", "date")
# Extra fields required per content kind.
REQUIRED_BY_KIND = {
    "weekly": ("week_label_zh", "week_label_en", "date_range", "sources"),
    "analysis": (),
    "insights": (),
    "cases": (),
}
KNOWN_KINDS = tuple(REQUIRED_BY_KIND)


def validate_meta(path: Path):
    """Return a list of human-readable problems (empty means valid)."""
    problems = []
    try:
        meta = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"{path}: 不是合法 JSON ({e})"]
    except OSError as e:
        return [f"{path}: 无法读取 ({e})"]
    if not isinstance(meta, dict):
        return [f"{path}: meta.json 必须是 JSON 对象"]

    kind = meta.get("kind")
    if kind not in KNOWN_KINDS:
        problems.append(
            f"{path}: kind={kind!r} 未知，应为 {list(KNOWN_KINDS)} 之一"
        )
    required = REQUIRED_COMMON + REQUIRED_BY_KIND.get(kind, ())
    for field in required:
        if not meta.get(field):
            problems.append(f"{path}: 缺少必填字段 {field!r}")
    if meta.get("date"):
        from datetime import datetime
        try:
            datetime.fromisoformat(meta["date"])
        except ValueError:
            problems.append(f"{path}: date={meta['date']!r} 不是 ISO 日期")
    return problems


def all_content_dirs():
    return build_i18n.discover_content_dirs()


def run_checks():
    dirs = all_content_dirs()
    problems = []
    for d in dirs:
        problems.extend(validate_meta(d / "meta.json"))
    return dirs, problems


def main():
    ap = argparse.ArgumentParser(description="7Kolor site publisher")
    ap.add_argument("--check", action="store_true", help="只校验，不写任何文件")
    args = ap.parse_args()

    dirs, problems = run_checks()
    for p in problems:
        print("ERROR:", p, file=sys.stderr)
    if problems:
        sys.exit(f"校验失败：{len(problems)} 个问题，已中止（不写入任何文件）")
    if not dirs:
        print("未发现任何内容目录（需要 meta.json + index.html）")
        return 0
    print(f"校验通过：{len(dirs)} 个内容目录")

    if args.check:
        return 0

    # 1) single-language pages
    for d in dirs:
        build_i18n.build(d)
    # 2) site-wide rebuild (cards + archive + feed)
    build_site.main()
    return 0


if __name__ == "__main__":
    sys.exit(main())
