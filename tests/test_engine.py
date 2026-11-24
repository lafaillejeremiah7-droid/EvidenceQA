import tempfile
import unittest
from pathlib import Path
from evidenceqa.engine import Passage, answer, passages

class EngineTests(unittest.TestCase):
    def test_ranking(self):
        docs = [Passage("a", "line 1", "Office hours"), Passage("b", "line 2", "Applications close Friday")]
        self.assertEqual(answer("When do applications close?", docs)["evidence"][0]["source"], "b")

    def test_no_match(self):
        self.assertEqual(answer("astronomy", [Passage("a", "1", "tax policy")])["status"], "no_evidence")

    def test_empty(self):
        self.assertEqual(answer("deadline", [])["evidence"], [])

    def test_citation(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "policy.txt"
            p.write_text("Applications close Friday\n", encoding="utf-8")
            hit = answer("applications close", passages(d))["evidence"][0]
            self.assertEqual(hit["locator"], "lines 1-1")
            self.assertEqual(hit["source"], str(p))

    def test_limit(self):
        with self.assertRaises(ValueError):
            answer("test", [], 0)
