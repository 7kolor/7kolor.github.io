"""Unit tests for scripts/build_i18n.py."""
import json
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import build_i18n


SAMPLE_HTML = """<!DOCTYPE html>
<html lang="zh-CN" class="no-js">
<head><meta charset="UTF-8"><title>7Kolor — 测试</title></head>
<body>
    <header><span class="logo-text">7Kolor <span>Insights</span></span>
        <div class="lang-toggle">
            <button class="lang-btn active" data-lang="zh">中文</button>
            <button class="lang-btn" data-lang="en">EN</button>
        </div>
    </header>
    <h1 data-zh="趋势分析" data-en="Trend Analysis">趋势分析</h1>
    <p data-zh="为独立开发者提供洞察" data-en="Insight for indie developers">为独立开发者提供洞察</p>
    <p data-zh="无翻译的元素" data-en="">无翻译的元素</p>
</body>
</html>"""


class PickLangTest(unittest.TestCase):
    def test_zh_selected(self):
        out = build_i18n.pick_lang(SAMPLE_HTML, "zh")
        self.assertIn(">趋势分析<", out)
        self.assertIn(">为独立开发者提供洞察<", out)
        self.assertNotIn("data-zh", out)
        self.assertNotIn("data-en", out)

    def test_en_selected(self):
        out = build_i18n.pick_lang(SAMPLE_HTML, "en")
        self.assertIn(">Trend Analysis<", out)
        self.assertIn(">Insight for indie developers<", out)

    def test_empty_en_falls_back_to_empty(self):
        out = build_i18n.pick_lang(SAMPLE_HTML, "en")
        self.assertIn(">无翻译的元素<", out)


class RetargetToggleTest(unittest.TestCase):
    def test_links_generated(self):
        base = Path("weekly/2026-W99")
        out = build_i18n.retarget_toggle(SAMPLE_HTML, "zh", base)
        self.assertIn("/weekly/2026-W99/report-zh.html", out)
        self.assertIn("/weekly/2026-W99/report-en.html", out)
        self.assertIn("lang-btn active", out.split("report-zh")[0])
        # the zh one is active; en link must not carry active
        zh_btn = out[out.find("report-zh.html") - 120 : out.find("report-zh.html")]
        self.assertIn("active", zh_btn)

    def test_no_toggle_no_change(self):
        html = "<p>no toggle</p>"
        self.assertEqual(build_i18n.retarget_toggle(html, "zh", Path("x")), html)


class TitlesTest(unittest.TestCase):
    def test_no_double_suffix(self):
        t = build_i18n.titles("2026 W34 周报", "2026 W34 Weekly Report")
        self.assertEqual(t["zh"], "7Kolor Insights — 2026 W34 周报")
        self.assertEqual(t["en"], "7Kolor Insights — 2026 W34 Weekly Report")


class BuildEndToEndTest(unittest.TestCase):
    def _make_item(self):
        d = Path(tempfile.mkdtemp())
        (d / "index.html").write_text(SAMPLE_HTML, encoding="utf-8")
        (d / "meta.json").write_text(
            json.dumps({
                "kind": "weekly",
                "id": "2026-W99",
                "week_label_zh": "2026 W99 周报",
                "week_label_en": "2026 W99 Weekly Report",
                "title_zh": "标题", "title_en": "Title",
                "date": "2026-09-01",
            }),
            encoding="utf-8",
        )
        return d

    def test_build_writes_both_pages(self):
        d = self._make_item()
        build_i18n.build(d)
        zh = (d / "report-zh.html").read_text(encoding="utf-8")
        en = (d / "report-en.html").read_text(encoding="utf-8")
        self.assertIn("<title>7Kolor Insights — 2026 W99 周报</title>", zh)
        self.assertIn("<title>7Kolor Insights — 2026 W99 Weekly Report</title>", en)
        self.assertIn(">趋势分析<", zh)
        self.assertIn(">Trend Analysis<", en)
        self.assertIn('lang="zh"', zh)
        self.assertIn('lang="en"', en)


if __name__ == "__main__":
    unittest.main()
