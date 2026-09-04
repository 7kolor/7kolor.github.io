"""Unit tests for scripts/build_site.py."""
import unittest
from datetime import datetime

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import build_site


def make_meta(**over):
    m = {
        "kind": "weekly",
        "id": "2026-W34",
        "week_label_zh": "2026 W34 周报",
        "week_label_en": "2026 W34 Weekly Report",
        "title_zh": "AI 编程", "title_en": "AI Coding",
        "desc_zh": "中文描述", "desc_en": "English desc",
        "date_range": "2026-08-23 ~ 08-29",
        "date": "2026-08-29",
        "sources": "Reddit · HN",
    }
    m["url"] = "/weekly/2026-W34/"
    m.update(over)
    return m


class ReportCardTest(unittest.TestCase):
    def test_fields_present(self):
        card = build_site.report_card(make_meta())
        self.assertIn("2026 W34 周报：AI 编程", card)
        self.assertIn("href=\"/weekly/2026-W34/\"", card)
        self.assertIn("中文描述", card)

    def test_escaping(self):
        meta = make_meta(desc_zh='引号 " 与 <尖括号>')
        card = build_site.report_card(meta)
        self.assertIn("&quot;", card)
        self.assertIn("&lt;", card)


class ReplaceAutoTest(unittest.TestCase):
    def test_block_replaced(self):
        html = "A<!-- AUTO:cards-weekly:begin -->old<!-- AUTO:cards-weekly:end -->B"
        out = build_site.replace_auto(html, "cards-weekly", "<card/>")
        self.assertIn("<card/>", out)
        self.assertNotIn("old", out)

    def test_missing_block_raises(self):
        with self.assertRaises(SystemExit):
            build_site.replace_auto("no block here", "cards-weekly", "x")


class FeedTest(unittest.TestCase):
    def test_items_sorted_newest_first(self):
        # feed entries carry the zh title (not the id), so use distinct titles
        items = {
            "weekly": [
                make_meta(id="old", title_zh="旧一期",
                          title_en="Old issue", date="2026-01-01"),
                make_meta(id="new", title_zh="新一期",
                          title_en="New issue", date="2026-09-01"),
            ]
        }
        feed = build_site.build_feed(items)
        i_old = feed.find("旧一期")
        i_new = feed.find("新一期")
        self.assertNotEqual(i_old, -1)
        self.assertNotEqual(i_new, -1)
        # sort is date-desc; the newer item must appear first
        self.assertLess(i_new, i_old)

    def test_feed_has_rss_envelope(self):
        feed = build_site.build_feed({"weekly": [make_meta()]})
        self.assertTrue(feed.startswith("<?xml"))
        self.assertIn("<rss", feed)

    def test_feed_rss_enhancements(self):
        feed = build_site.build_feed({"weekly": [make_meta()]})
        # content-encoded namespace declared
        self.assertIn("xmlns:content=", feed)
        # channel-level image + ttl
        self.assertIn("<ttl>", feed)
        self.assertIn("<image>", feed)
        # every item carries a category
        self.assertIn("<category>", feed)
        # content:encoded is wrapped in CDATA
        self.assertIn("<content:encoded><![CDATA[", feed)


if __name__ == "__main__":
    unittest.main()
