"""Tests for agent-facing entry points: sitemap.xml / llms.txt / robots.txt.

Guarded contracts:
- sitemap is derived from TRACKED files only: redirect aliases excluded,
  untracked local junk can never leak in, single-language pages included
- committed sitemap.xml / llms.txt are always identical to a fresh build
  (if they drift, both these tests and the CI freshness gate go red)
- a new ISSUE of a registered kind appears in sitemap + llms with zero
  hand-maintained edits (registering a brand-new KIND is a deliberate
  code step — documented in agents.md, not implied here)
- meta fields are sanitized before entering llms.txt Markdown
"""
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import build_site

ROOT = Path(__file__).resolve().parent.parent
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


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


def sitemap_locs(items):
    tree = ET.fromstring(build_site.build_sitemap(items))
    return {loc.text: url for loc, url in
            ((u.find("sm:loc", NS), u) for u in tree.findall("sm:url", NS))}


class SitemapTest(unittest.TestCase):
    def test_valid_xml_covers_static_pages_and_reports(self):
        items = build_site.load_items()
        locs = sitemap_locs(items)
        for page in ("/", "/about.html", "/weekly/", "/steps/step-1/", "/steps/step-6/"):
            self.assertIn(build_site.SITE + page, locs)
        for m in items["weekly"]:
            self.assertIn(build_site.SITE + m["url"], locs)

    def test_redirect_alias_excluded(self):
        # weekly/w34/ is a <meta refresh> alias of /weekly/2026-W34/ —
        # sitemap <loc> must be the canonical URL only
        locs = sitemap_locs(build_site.load_items())
        self.assertNotIn(build_site.SITE + "/weekly/w34/", locs)
        self.assertIn(build_site.SITE + "/weekly/2026-W34/", locs)

    def test_single_language_pages_included_with_lastmod(self):
        items = build_site.load_items()
        locs = sitemap_locs(items)
        m = items["weekly"][0]
        for lang in ("report-zh.html", "report-en.html"):
            url = build_site.SITE + m["url"] + lang
            self.assertIn(url, locs)
            self.assertEqual(locs[url].find("sm:lastmod", NS).text, m["date"])

    def test_new_issue_of_registered_kind_appears(self):
        items = build_site.load_items()
        fresh = make_meta(id="2026-W50", url="/weekly/2026-W50/",
                          date="2026-12-19")
        items["weekly"].insert(0, fresh)
        locs = sitemap_locs(items)
        self.assertIn(build_site.SITE + "/weekly/2026-W50/", locs)
        self.assertEqual(locs[build_site.SITE + "/weekly/2026-W50/"]
                         .find("sm:lastmod", NS).text, "2026-12-19")
        body = build_site.build_llms_reports(items)
        self.assertIn("2026-W50 测试标题", body)
        self.assertIn("https://7kolor.github.io/weekly/2026-W50/", body)

    def test_committed_sitemap_matches_build(self):
        committed = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        self.assertEqual(committed, build_site.build_sitemap(build_site.load_items()))

    def test_untracked_junk_cannot_leak_in(self):
        # discover_static_pages reads the git index, not the working tree:
        # untracked dirs/files must never appear in the sitemap
        locs = sitemap_locs(build_site.load_items())
        for bad in ("/_site/", "/drafts/", "/node_modules/"):
            self.assertFalse(any(bad in u for u in locs), bad)


class LlmsTest(unittest.TestCase):
    def test_llms_reports_lists_items(self):
        items = {"weekly": [make_meta()], "cases": [make_meta(
            kind="cases", id="case-x", url="/cases/case-x/", title_zh="案例")]}
        body = build_site.build_llms_reports(items)
        self.assertIn("2026-W99 测试标题", body)
        self.assertIn("https://7kolor.github.io/weekly/2026-W99/", body)
        self.assertIn("测试摘要", body)
        self.assertIn("case-x 案例", body)
        self.assertIn("cases/case-x/", body)

    def test_md_safe_blocks_injection(self):
        evil = make_meta(
            title_zh="标题 ](https://evil.example/x)",
            desc_zh="第一行\n## 伪造标题 <!-- AUTO:llms-reports:end --> [link](https://evil.example)")
        body = build_site.build_llms_reports({"weekly": [evil]})
        self.assertNotIn("<!--", body)          # HTML comments stripped
        # newline-collapsed: injected heading cannot become a new block
        self.assertNotIn("\n## 伪造标题", body)
        self.assertNotIn("[link](https://evil.example)", body)
        # no raw ](... can break the list link
        self.assertIn("标题 \]\(https://evil.example/x\)", body)

    def test_committed_llms_block_matches_build(self):
        llms_path = ROOT / "llms.txt"
        self.assertTrue(llms_path.is_file(), "llms.txt missing")
        llms = llms_path.read_text(encoding="utf-8")
        items = build_site.load_items()
        out = build_site.replace_auto(llms, "llms-reports",
                                      build_site.build_llms_reports(items),
                                      indent="")
        self.assertEqual(out, llms)  # committed file is a fresh build
        self.assertIn("<!-- AUTO:llms-reports:begin -->", llms)

    def test_empty_title_falls_back_to_id(self):
        body = build_site.build_llms_reports(
            {"weekly": [make_meta(title_zh="", title_en="")]})
        self.assertIn("- [2026-W99]", body)
        self.assertNotIn("2026-W99 2026-W99", body)

    def test_robots_txt_points_to_sitemap(self):
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("Allow: /", robots)
        self.assertIn("Sitemap: " + build_site.SITE + "/sitemap.xml", robots)


if __name__ == "__main__":
    unittest.main()
