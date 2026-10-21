"""Tests for agent-facing entry points: sitemap.xml / llms.txt / robots.txt.

These guard the "future updates stay automatic" contract:
new content kinds, new report issues and new top-level pages must appear
in sitemap.xml and llms.txt without any manual editing.
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
    return [loc.text for loc in tree.findall("sm:url/sm:loc", NS)]


class SitemapTest(unittest.TestCase):
    def test_valid_xml_covers_static_pages_and_reports(self):
        items = build_site.load_items()
        locs = sitemap_locs(items)
        for page in ("/", "/about.html", "/weekly/", "/steps/step-1/", "/steps/step-6/"):
            self.assertIn(build_site.SITE + page, locs)
        for m in items["weekly"]:
            self.assertIn(build_site.SITE + m["url"], locs)

    def test_new_content_kind_appears_automatically(self):
        items = {"weekly": [make_meta()], "cases": [make_meta(
            kind="cases", id="case-x", url="/cases/case-x/")]}
        locs = sitemap_locs(items)
        self.assertIn(build_site.SITE + "/cases/case-x/", locs)

    def test_content_items_carry_lastmod(self):
        items = {"weekly": [make_meta()]}
        tree = ET.fromstring(build_site.build_sitemap(items))
        url = tree.find("sm:url[sm:loc='%s/weekly/2026-W99/']" % build_site.SITE, NS)
        self.assertIsNotNone(url)
        self.assertEqual(url.find("sm:lastmod", NS).text, "2026-10-17")


class LlmsTest(unittest.TestCase):
    def test_llms_reports_lists_every_kind(self):
        items = {"weekly": [make_meta()], "cases": [make_meta(
            kind="cases", id="case-x", url="/cases/case-x/", title_zh="案例")]}
        body = build_site.build_llms_reports(items)
        self.assertIn("2026-W99 测试标题", body)
        self.assertIn("https://7kolor.github.io/weekly/2026-W99/", body)
        self.assertIn("测试摘要", body)
        # a brand-new kind shows up without touching any hand-maintained list
        self.assertIn("case-x 案例", body)
        self.assertIn("cases/case-x/", body)

    def test_llms_txt_block_updates_from_repo(self):
        llms_path = ROOT / "llms.txt"
        self.assertTrue(llms_path.is_file(), "llms.txt missing")
        llms = llms_path.read_text(encoding="utf-8")
        self.assertIn("<!-- AUTO:llms-reports:begin -->", llms)
        items = build_site.load_items()
        out = build_site.replace_auto(llms, "llms-reports",
                                      build_site.build_llms_reports(items))
        latest = items["weekly"][0]
        self.assertIn(latest["id"], out)
        self.assertIn("<!-- AUTO:llms-reports:begin -->", out)
        self.assertIn("<!-- AUTO:llms-reports:end -->", out)

    def test_robots_txt_points_to_sitemap(self):
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("Allow: /", robots)
        self.assertIn("Sitemap: https://7kolor.github.io/sitemap.xml", robots)


if __name__ == "__main__":
    unittest.main()
