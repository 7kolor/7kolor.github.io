"""Unit tests for scripts/publish.py (meta validation)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import publish


def write_meta(d: Path, data):
    (d / "meta.json").write_text(json.dumps(data), encoding="utf-8")
    return d / "meta.json"


class ValidateMetaTest(unittest.TestCase):
    def test_valid_weekly(self):
        with tempfile.TemporaryDirectory() as td:
            p = write_meta(Path(td), {
                "kind": "weekly", "id": "W1",
                "title_zh": "t", "title_en": "t", "date": "2026-09-01",
                "week_label_zh": "l", "week_label_en": "l",
                "date_range": "x", "sources": "s",
            })
            self.assertEqual(publish.validate_meta(p), [])

    def test_missing_required(self):
        with tempfile.TemporaryDirectory() as td:
            p = write_meta(Path(td), {"kind": "weekly", "id": "W1"})
            problems = publish.validate_meta(p)
            texts = " ".join(problems)
            for f in ("title_zh", "title_en", "date", "week_label_zh"):
                self.assertIn(f, texts)

    def test_unknown_kind(self):
        with tempfile.TemporaryDirectory() as td:
            p = write_meta(Path(td), {"kind": "mystery", "id": "x",
                                      "title_zh": "t", "title_en": "t"})
            problems = publish.validate_meta(p)
            self.assertTrue(any("mystery" in x for x in problems))

    def test_bad_json(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "meta.json"
            p.write_text("{not json", encoding="utf-8")
            problems = publish.validate_meta(p)
            self.assertTrue(any("JSON" in x for x in problems))

    def test_bad_date(self):
        with tempfile.TemporaryDirectory() as td:
            p = write_meta(Path(td), {
                "kind": "weekly", "id": "W1",
                "title_zh": "t", "title_en": "t", "date": "not-a-date",
                "week_label_zh": "l", "week_label_en": "l",
                "date_range": "x", "sources": "s",
            })
            problems = publish.validate_meta(p)
            self.assertTrue(any("ISO" in x for x in problems))


if __name__ == "__main__":
    unittest.main()
