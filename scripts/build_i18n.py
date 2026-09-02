#!/usr/bin/env python3
"""Build single-language report pages from a bilingual index.html.

Usage:
    python3 scripts/build_i18n.py weekly/w34

Reads  <dir>/index.html  (elements carry data-zh / data-en attributes)
Writes <dir>/report-zh.html and <dir>/report-en.html

The bilingual page stays the canonical URL; single-language pages are
share-friendly variants whose lang toggle links to the other page.
"""
import json
import re
import sys
from pathlib import Path

def titles(week_label):
    return {
        "zh": f"7Kolor Insights — {week_label} 周报",
        "en": f"7Kolor Insights — {week_label} Weekly Report",
    }
LANG_NAMES = {"zh": "中文", "en": "EN"}


def pick_lang(html: str, lang: str) -> str:
    """Replace bilingual data-* elements with the chosen language text."""
    other = "en" if lang == "zh" else "zh"
    # <tag ... data-zh="A" data-en="B">TEXT</tag>  ->  <tag ...>A or B</tag>
    pat = re.compile(
        r' data-zh="([^"]*)" data-en="([^"]*)"([^>]*)>[^<]*', re.S
    )

    def repl(m):
        zh, en, rest = m.group(1), m.group(2), m.group(3)
        return rest + ">" + (zh if lang == "zh" else en)

    return pat.sub(repl, html)


def retarget_toggle(html: str, lang: str, base: str) -> str:
    """Turn the JS lang toggle into plain links between single-language pages."""
    toggle = re.search(r'<div class="lang-toggle">.*?</div>', html, re.S)
    if not toggle:
        return html
    other = "en" if lang == "zh" else "zh"
    links = (
        '<div class="lang-toggle">\n'
        + "".join(
            '                    <a class="lang-btn{active}" href="/{base}/report-{code}.html">{name}</a>\n'.format(
                active=" active" if code == lang else "",
                base=base,
                code=code,
                name=LANG_NAMES[code],
            )
            for code in ("zh", "en")
        )
        + "                </div>"
    )
    return html[: toggle.start()] + links + html[toggle.end() :]


def build(week_dir: Path) -> None:
    src = (week_dir / "index.html").read_text(encoding="utf-8")
    base = str(week_dir).replace("\\", "/")
    # 从 meta.json 推导周次标签，退化为文件夹名
    label = week_dir.name
    meta_path = week_dir / "meta.json"
    if meta_path.exists():
        try:
            label = json.loads(meta_path.read_text(encoding="utf-8")).get(
                "week_label_zh" if label.startswith("zh") else "week_label_zh", label)
        except Exception:
            pass
    tt = titles(label)
    for lang in ("zh", "en"):
        out = src
        out = pick_lang(out, lang)
        out = retarget_toggle(out, lang, base)
        out = out.replace('<html lang="zh-CN">', f'<html lang="{lang}">')
        out = re.sub(r"<title>.*?</title>", f"<title>{tt[lang]}</title>", out, count=1)
        # mark as single-language page (main.js skips toggle restore)
        out = out.replace("<body>", f'<body data-lang-page="{lang}">', 1)
        target = week_dir / f"report-{lang}.html"
        target.write_text(out, encoding="utf-8")
        print(f"built {target}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: build_i18n.py <week-dir>   e.g. weekly/w34")
    build(Path(sys.argv[1]))
