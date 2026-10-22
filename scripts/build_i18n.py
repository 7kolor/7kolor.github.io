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
from html.parser import HTMLParser
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

    Two cases for the default text after ">":
    - plain text (no child tags): replaced by the selected language text.
    - text followed by child tags (e.g. <a> links): only the plain-text
      prefix is replaced; the child elements (clickable links) are kept
      as-is. This avoids duplicating content when bilingual elements
      carry inline anchors in their default text.
    """
    pat = re.compile(
        r''' data-zh="([^"]*)" data-en="([^"]*)"([^>]*)>([^<]*)''', re.S
    )

    def repl(m):
        zh, en, tail, prefix = m.group(1), m.group(2), m.group(3), m.group(4)
        rest = html[m.end():]
        nxt = rest.lstrip()
        # Child-carrying element: the plain text after ">" (if any) is
        # only the first slice of the sentence; the remaining slices are
        # carried by children that each hold their own data-zh /
        # data-en. Keep the prefix as-is and strip the data-* attrs —
        # the children translate themselves.
        if nxt[:1] == "<" and nxt[1:2] != "/":
            return tail + ">" + prefix
        # Plain-text element: replace with the chosen language value.
        picked = zh if lang == "zh" else en
        picked = picked or (en if lang == "zh" else zh)
        return tail + ">" + picked

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


_SKIP_TAGS = {"script", "style", "svg", "nav", "header", "footer", "button"}
_HEADING_PREFIX = {"h1": "# ", "h2": "## ", "h3": "### ", "h4": "#### "}


class _MdConverter(HTMLParser):
    """Minimal HTML -> Markdown converter for report bodies.

    Supports: h1-h4, p, ul/ol/li (nested), strong/b, em/i, a[href],
    blockquote, code/pre, br. Unknown block tags are traversed (content
    kept); tables degrade to plain-text rows. Deliberately small: report
    bodies use a limited, consistent markup subset.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.stack = []          # open tag names, for nesting context
        self.list_stack = []     # 'ul' / 'ol' per nesting level
        self.href = None         # open <a> href
        self.pre = False         # inside <pre>
        self.in_heading = None   # h1-h4 tag name while inside it
        self.in_li = False
        self.cell_sep = False    # inside table row: separate cells

    def _emit(self, s):
        self.out.append(s)

    def _newline(self, n=1):
        text = "".join(self.out)
        need = n - (len(text) - len(text.rstrip("\n")))
        if need > 0:
            self.out.append("\n" * need)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.stack.append(tag)
        if tag in _SKIP_TAGS:
            return
        if tag in _HEADING_PREFIX:
            self._newline(2)
            self._emit(_HEADING_PREFIX[tag])
            self.in_heading = tag
        elif tag == "p":
            self._newline(2)
        elif tag == "br":
            self._newline(1)
        elif tag in ("ul", "ol"):
            self.list_stack.append(tag)
            self._newline(1)
        elif tag == "li":
            self._newline(1)
            indent = "  " * max(0, len(self.list_stack) - 1)
            bullet = "-" if (self.list_stack and self.list_stack[-1] == "ul") else "1."
            self._emit(f"{indent}{bullet} ")
            self.in_li = True
        elif tag in ("strong", "b"):
            self._emit("**")
        elif tag in ("em", "i"):
            self._emit("*")
        elif tag == "a":
            self.href = attrs.get("href")
            if self.href:
                self._emit("[")
        elif tag == "blockquote":
            self._newline(2)
            self._emit("> ")
        elif tag == "pre":
            self._newline(2)
            self._emit("```\n")
            self.pre = True
        elif tag == "code":
            if not self.pre:
                self._emit("`")
        elif tag in ("td", "th"):
            if self.cell_sep:
                self._emit(" | ")
            self.cell_sep = True
        elif tag == "tr":
            self._newline(1)
            self.cell_sep = False
        elif tag == "table":
            self._newline(2)
        # other tags: traverse children, keep text

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        if tag in _SKIP_TAGS:
            return
        if tag in _HEADING_PREFIX:
            self._newline(2)
            self.in_heading = None
        elif tag == "p":
            self._newline(2)
        elif tag in ("ul", "ol"):
            if self.list_stack:
                self.list_stack.pop()
            self._newline(1)
        elif tag == "li":
            self.in_li = False
        elif tag in ("strong", "b"):
            self._emit("**")
        elif tag in ("em", "i"):
            self._emit("*")
        elif tag == "a":
            if self.href:
                self._emit(f"]({self.href})")
            self.href = None
        elif tag == "blockquote":
            self._newline(2)
        elif tag == "pre":
            self._emit("\n```")
            self._newline(2)
            self.pre = False
        elif tag == "code":
            if not self.pre:
                self._emit("`")
        elif tag == "table":
            self._newline(2)

    def handle_startendtag(self, tag, attrs):
        if tag == "br":
            self._newline(1)

    def handle_data(self, data):
        if any(t in _SKIP_TAGS for t in self.stack):
            return
        if self.pre or self.in_heading:
            self._emit(data)
        else:
            self._emit(re.sub(r"\s+", " ", data))

    def result(self):
        text = "".join(self.out)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip() + "\n"


def html_to_markdown(html: str) -> str:
    """Convert a report-body HTML fragment to Markdown (zero-dependency)."""
    conv = _MdConverter()
    conv.feed(html)
    conv.close()
    return conv.result()


def content_div(html: str) -> str:
    """The <div class="content"> body of a report page (same traversal rule
    as build_site._content_html, kept local to avoid a cross-module import)."""
    start = html.find('<div class="content">')
    if start < 0:
        return ""
    i = start + len('<div class="content">')
    depth, j, n = 1, i, len(html)
    while j < n and depth:
        od = html.find("<div", j)
        cd = html.find("</div>", j)
        if od < 0 and cd < 0:
            break
        if cd < 0 or (0 <= od < cd):
            depth += 1
            j = od + 5
        else:
            depth -= 1
            j = cd + 6
    return html[i : j - 6]


def build(item_dir: Path) -> None:
    src = (item_dir / "index.html").read_text(encoding="utf-8")
    label_zh = label_en = item_dir.name
    meta_path = item_dir / "meta.json"
    desc = {}
    titles_meta = {}
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            label_zh = meta.get("week_label_zh") or label_zh
            label_en = meta.get("week_label_en") or label_en
            desc = {c: meta.get("desc_" + c) for c in ("zh", "en")}
            titles_meta = {c: meta.get("title_" + c) for c in ("zh", "en")}
        except (json.JSONDecodeError, OSError):
            pass  # label falls back to the folder name
    try:
        base = item_dir.relative_to(ROOT)
    except ValueError:
        base = Path(item_dir.name)  # outside the repo (e.g. tests): use bare name
    tt = titles(label_zh, label_en)
    md_targets = {"zh": "report.md", "en": "report-en.md"}
    for lang in ("zh", "en"):
        out = src
        out = pick_lang(out, lang)
        out = retarget_toggle(out, lang, base)
        out = re.sub(r'<html lang="zh-CN"', f'<html lang="{"zh-CN" if lang == "zh" else lang}"', out, count=1)
        out = re.sub(r"<title>.*?</title>", f"<title>{tt[lang]}</title>", out, count=1)
        if desc.get(lang):
            out = re.sub(r'<meta name="description" content="[^"]*">',
                         f'<meta name="description" content="{desc[lang]}">', out, count=1)
        out = out.replace("<body>", f'<body data-lang-page="{lang}">', 1)
        target = item_dir / f"report-{lang}.html"
        target.write_text(out, encoding="utf-8")
        print(f"built {target}")

        # LLM-friendly Markdown variant of this language's body (#21)
        body = html_to_markdown(content_div(out))
        header = f"# {tt[lang]}\n\n"
        if titles_meta.get(lang):
            header += f"## {titles_meta[lang]}\n\n"
        if desc.get(lang):
            header += f"> {desc[lang]}\n\n"
        header += f"原文 / Source: /{base.as_posix()}/\n\n---\n\n"
        md_target = item_dir / md_targets[lang]
        md_target.write_text(header + body, encoding="utf-8")
        print(f"built {md_target}")


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
