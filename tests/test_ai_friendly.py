"""Tests for the #21/#22 AI-friendliness layer: reports.json, per-report
Markdown, and report-page head metadata (canonical / Open Graph / JSON-LD).
"""
import json
import re
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import build_i18n
import build_site

ROOT = Path(__file__).resolve().parent.parent


def make_meta(**over):
    m = {
        "kind": "weekly",
        "id": "2026-W99",
        "title_zh": "测试标题",
        "title_en": "Test title",
        "desc_zh": "测试摘要",
        "desc_en": "Test desc",
        "date": "2026-10-17",
        "url": "/weekly/2026-W99/",
    }
    m.update(over)
    return m


class ReportsJsonTest(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "reports.json").read_text(encoding="utf-8"))

    def test_valid_and_count_matches_items(self):
        items = build_site.load_items()
        total = sum(len(v) for v in items.values())
        self.assertEqual(self.data["count"], len(self.data["reports"]))
        self.assertEqual(self.data["count"], total)
        self.assertEqual(self.data["site"], build_site.SITE)

    def test_links_point_to_real_files(self):
        # every advertised link must exist on disk — no dead links (#20 lesson)
        for r in self.data["reports"]:
            for key, url in r["links"].items():
                self.assertTrue(url.startswith(build_site.SITE), url)
                rel = url[len(build_site.SITE):].lstrip("/")
                path = ROOT / rel
                if rel.endswith("/"):
                    path = path / "index.html"   # directory URL → its index
                self.assertTrue(path.is_file(), f"{key}: {url}")

    def test_committed_reports_json_matches_build(self):
        committed = (ROOT / "reports.json").read_text(encoding="utf-8")
        self.assertEqual(committed, build_site.build_reports_json(build_site.load_items()))


class MarkdownTest(unittest.TestCase):
    def test_headings_paragraph_strong_link(self):
        md = build_i18n.html_to_markdown(
            '<h2 data-zh="趋势" data-en="Trends">趋势</h2>'
            '<p>正文 <strong>重点</strong> 与 <a href="https://x.example">链接</a>。</p>')
        self.assertIn("## 趋势", md)
        self.assertIn("**重点**", md)
        self.assertIn("[链接](https://x.example)", md)

    def test_nested_lists_and_ordered(self):
        md = build_i18n.html_to_markdown(
            "<ul><li>甲</li><li>乙<ul><li>乙一</li></ul></li></ul><ol><li>第一步</li></ol>")
        self.assertIn("- 甲", md)
        self.assertIn("- 乙", md)
        self.assertIn("  - 乙一", md)          # nested item indented
        self.assertIn("1. 第一步", md)

    def test_blockquote_code_table_fallback(self):
        md = build_i18n.html_to_markdown(
            "<blockquote>引用</blockquote><pre><code>x = 1</code></pre>"
            "<table><tr><td>A</td><td>B</td></tr><tr><td>1</td><td>2</td></tr></table>")
        self.assertIn("> 引用", md)
        self.assertIn("```", md)
        self.assertIn("x = 1", md)

    def test_table_is_gfm_not_fake_heading(self):
        # a leading "# 标题" cell must NOT become an H1 (review finding):
        # GFM table rows are pipe-wrapped, with a header separator line
        md = build_i18n.html_to_markdown(
            "<table><tr><th># 标题</th><th>热度</th></tr>"
            "<tr><td>甲</td><td>100</td></tr></table>")
        self.assertIn("| # 标题 | 热度 |", md)
        self.assertIn("|---|", md)
        self.assertIn("| 甲 | 100 |", md)
        self.assertNotIn("\n# 标题\n", md)

    def test_h5_h6_img_and_ol_numbers(self):
        md = build_i18n.html_to_markdown(
            "<h5>五级</h5><h6>六级</h6><img src='a.png' alt='图A'>"
            "<ol><li>一</li><li>二</li></ol>")
        self.assertIn("##### 五级", md)
        self.assertIn("###### 六级", md)
        self.assertIn("![图A](a.png)", md)
        self.assertIn("1. 一", md)
        self.assertIn("2. 二", md)

    def test_report_en_md_has_english_content(self):
        items = build_site.load_items()
        for m in items["weekly"]:
            p = ROOT / m["url"].lstrip("/") / "report-en.md"
            md = p.read_text(encoding="utf-8")
            self.assertGreater(len(md), 500, p)
            self.assertIn(m["title_en"][:15].replace('"', ''),
                          md.replace('"', ''))

    def test_script_style_content_dropped(self):
        md = build_i18n.html_to_markdown(
            "<p>可见</p><script>var secret = 1;</script><style>.x{}</style>")
        self.assertIn("可见", md)
        self.assertNotIn("secret", md)
        self.assertNotIn(".x{}", md)

    def test_report_md_files_exist_and_match_html(self):
        def norm(s):  # 「」“” differ between meta and in-page headings
            for ch in ['「', '」', '“', '”', "'", '"', ' ']:
                s = s.replace(ch, '')
            return s
        items = build_site.load_items()
        self.assertTrue(items["weekly"], "no weekly items")
        for m in items["weekly"]:
            md_path = ROOT / m["url"].lstrip("/") / "report.md"
            en_path = ROOT / m["url"].lstrip("/") / "report-en.md"
            self.assertTrue(md_path.is_file(), md_path)
            self.assertTrue(en_path.is_file(), en_path)
            md = md_path.read_text(encoding="utf-8")
            # page heading carries the issue title (quotes may differ in style)
            self.assertIn(norm(m["title_zh"])[:12], norm(md))
            self.assertIn("report-", en_path.name)  # en variant distinct name
            self.assertNotIn("<div", md)          # no raw HTML tags leak
            self.assertNotIn("data-zh", md)


class HeadMetaTest(unittest.TestCase):
    def _pages(self):
        """Every report page in every language: bilingual index, report-zh,
        report-en (review B1 — the single-language pages used to inherit
        Chinese metadata, and tests that only checked index.html were
        blind to it)."""
        items = build_site.load_items()
        for m in items["weekly"]:
            base = ROOT / m["url"].lstrip("/")
            yield m, "zh", "index.html", (base / "index.html").read_text(encoding="utf-8")
            yield m, "zh", "report-zh.html", (base / "report-zh.html").read_text(encoding="utf-8")
            yield m, "en", "report-en.html", (base / "report-en.html").read_text(encoding="utf-8")

    def test_auto_block_present_on_all_report_pages(self):
        for m, lang, fname, html in self._pages():
            self.assertIn("<!-- AUTO:head-meta:begin -->", html, f"{m['id']} {fname}")
            self.assertIn("<!-- AUTO:head-meta:end -->", html, f"{m['id']} {fname}")

    def test_jsonld_parses_and_has_required_types(self):
        pat = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
        for m, lang, fname, html in self._pages():
            scripts = pat.findall(html)
            self.assertTrue(scripts, f"no JSON-LD on {m['id']} {fname}")
            data = json.loads(scripts[0])
            types = {node.get("@type") for node in data["@graph"]}
            self.assertIn("NewsArticle", types, f"{m['id']} {fname}")
            self.assertIn("BreadcrumbList", types, f"{m['id']} {fname}")
            article = next(n for n in data["@graph"] if n["@type"] == "NewsArticle")
            self.assertEqual(article["headline"], m["title_" + lang],
                             f"{m['id']} {fname} headline not in {lang}")
            self.assertEqual(article["inLanguage"], "zh-CN" if lang == "zh" else "en",
                             f"{m['id']} {fname} inLanguage mismatch")
            self.assertEqual(article["datePublished"], m["date"])
            crumb = next(n for n in data["@graph"] if n["@type"] == "BreadcrumbList")
            self.assertEqual(len(crumb["itemListElement"]), 3)

    def test_jsonld_safe_against_script_truncation(self):
        # a stray "</" in title/desc must not break out of the script element
        evil = dict(make_meta(), url="/weekly/2026-W99/",
                    title_zh='标题 </script><script>alert(1)</script>',
                    desc_zh='摘要 </script>')
        out = build_site.build_head_meta(evil)
        body = out.split('ld+json">', 1)[1].rsplit("</script>", 1)[0]
        self.assertNotIn("</", body)          # every "</" JSON-escaped as "<\/"
        self.assertIn("<\\/script>", body)

    def test_canonical_and_og_present(self):
        for m, lang, fname, html in self._pages():
            tag = f"{m['id']} {fname}"
            self.assertIn(f'<link rel="canonical" href="{build_site.SITE}{m["url"]}">', html, tag)
            self.assertIn('property="og:title"', html, tag)
            self.assertIn('property="og:description"', html, tag)
            expected_locale = "zh_CN" if lang == "zh" else "en_US"
            self.assertIn(f'property="og:locale" content="{expected_locale}"', html, tag)
            # html lang attribute agrees with the metadata language
            html_lang = re.search(r'<html lang="([^"]+)"', html).group(1)
            self.assertTrue(html_lang.startswith("zh") if lang == "zh" else html_lang == "en",
                            f"{tag}: html lang={html_lang} meta lang={lang}")
            # no un-filled block
            block = re.search(
                r"<!-- AUTO:head-meta:begin -->(.*?)<!-- AUTO:head-meta:end -->",
                html, re.S).group(1)
            self.assertIn("canonical", block, tag)

    def test_committed_report_md_is_fresh(self):
        # same freshness contract as reports.json: rebuilding i18n output
        # must reproduce the committed report.md byte-for-byte. Runs in a
        # temp copy so the test never writes the working tree.
        import shutil
        import tempfile
        items = build_site.load_items()
        m = items["weekly"][0]
        src = ROOT / m["url"].lstrip("/")
        with tempfile.TemporaryDirectory() as tmp:
            # mirror the repo-relative layout (weekly/<id>) and point
            # build_i18n.ROOT at the temp root so relative paths match
            d = Path(tmp) / src.parent.name / src.name
            d.parent.mkdir(parents=True)
            shutil.copytree(src, d)
            committed = (src / "report.md").read_text(encoding="utf-8")
            saved_root = build_i18n.ROOT
            try:
                build_i18n.ROOT = Path(tmp)
                build_i18n.build(d)
            finally:
                build_i18n.ROOT = saved_root
            self.assertEqual(committed, (d / "report.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
