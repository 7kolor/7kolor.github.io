#!/usr/bin/env python3
"""Build single-language report pages from bilingual index.html files.

Usage:
    python3 scripts/build_i18n.py                    # scan & build all content dirs
    python3 scripts/build_i18n.py weekly/2026-W35    # build one or more dirs

For each <dir> containing meta.json + a bilingual index.html (elements carry
data-zh / data-en attributes, written in that order), writes report-zh.html
and report-en.html.

The bilingual page stays canonical; single-language pages are share-friendly
variants whose lang toggle links between them.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_ROOTS = ("weekly", "analysis", "insights", "cases")  # future content types
LANG_NAMES = {"zh": "中文", "en": "EN"}


def discover_content_dirs(roots=CONTENT_ROOTS, base: Path = ROOT):
    """Return every dir under content roots that has a content item
    (meta.json + bilingual index.html). New root folders (analysis/,
    insights/, cases/, ...) are picked up automatically."""
    dirs = []
    for root in roots:
        root_dir = base / root
        if not root_dir.is_dir():
            continue
        for meta_path in sorted(root_dir.glob("*/meta.json")):
            item_dir = meta_path.parent
            if (item_dir / "index.html").is_file():
                dirs.append(item_dir)
    return dirs


def titles(label_zh: str, label_en: str):
    """<title> for the single-language variants. Labels already carry their
    own wording ('2026 W34 周报' / '2026 W34 Weekly Report'), nothing extra
    is appended."""
    return {
        "zh": f"7Kolor Insights — {label_zh}",
        "en": f"7Kolor Insights — {label_en}",
    }


def pick_lang(html: str, lang: str) -> str:
    """Replace bilingual elements with the chosen language text.

    Matches elements written as  data-zh="A" data-en="B">TEXT  (attributes in
    that order, text without child tags) — the convention used across all
    site templates. Returns the tag without the data-* attributes, keeping
    the selected language's text.
    """
    pat = re.compile(
        r''' data-zh="([^"]*)" data-en="([^"]*)"([^>]*)>[^<]*''', re.S
    )

    def repl(m):
        zh, en, tail = m.group(1), m.group(2), m.group(3)
        picked = zh if lang == "zh" else en
        # fall back to the other language when the chosen one is empty,
        # so elements with an empty translation never lose their content
        return tail + ">" + (picked or (en if lang == "zh" else zh))

    return pat.sub(repl, html)


def retarget_toggle(html: str, lang: str, base: Path) -> str:
    """Turn the JS lang toggle into plain links between single-language pages."""
    toggle = re.search(r'<div class="lang-toggle">.*?</div>', html, re.S)
    if not toggle:
        return html
    links = (
        '<div class="lang-toggle">\n'
        + "".join(
            '                    <a class="lang-btn{active}" href="/{base}/report-{code}.html">{name}</a>\n'.format(
                active=" active" if code == lang else "",
                base=base.as_posix(),
                code=code,
                name=LANG_NAMES[code],
            )
            for code in ("zh", "en")
        )
        + "                </div>"
    )
    return html[: toggle.start()] + links + html[toggle.end():]


def build(item_dir: Path) -> None:
    src = (item_dir / "index.html").read_text(encoding="utf-8")
    label_zh = label_en = item_dir.name
    meta_path = item_dir / "meta.json"
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            label_zh = meta.get("week_label_zh") or label_zh
            label_en = meta.get("week_label_en") or label_en
        except (json.JSONDecodeError, OSError):
            pass  # label falls back to the folder name
    try:
        base = item_dir.relative_to(ROOT)
    except ValueError:
        base = Path(item_dir.name)  # outside the repo (e.g. tests): use bare name
    tt = titles(label_zh, label_en)
    for lang in ("zh", "en"):
        out = src
        out = pick_lang(out, lang)
        out = retarget_toggle(out, lang, base)
        out = re.sub(r'<html lang="zh-CN"', f'<html lang="{lang}"', out, count=1)
        out = re.sub(r"<title>.*?</title>", f"<title>{tt[lang]}</title>", out, count=1)
        out = out.replace("<body>", f'<body data-lang-page="{lang}">', 1)
        target = item_dir / f"report-{lang}.html"
        target.write_text(out, encoding="utf-8")
        print(f"built {target}")


def main():
    args = sys.argv[1:]
    if args:
        targets = [Path(a) for a in args]
        missing = [t for t in targets if not (t / "index.html").is_file()]
        if missing:
            sys.exit("missing index.html in: " + ", ".join(map(str, missing)))
    else:
        targets = discover_content_dirs()
        if not targets:
            sys.exit("no content dirs found (need meta.json + index.html)")
    for target in targets:
        build(target)


if __name__ == "__main__":
    main()
