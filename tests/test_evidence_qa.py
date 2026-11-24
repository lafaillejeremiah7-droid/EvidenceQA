import unittest
import tempfile
from pathlib import Path
from evidence_qa import index, search

class RetrievalTests(unittest.TestCase):
    def test_rank_and_cite(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "policy.txt"
            path.write_text("Office hours\nApplications close Friday\n", encoding="utf-8")
            hit = search("applications close", index(directory))[0]
            self.assertEqual(hit["line"], 2)
            self.assertEqual(hit["source"], str(path))

    def test_no_match(self):
        self.assertEqual(search("astronomy", [{"text": "tax policy"}]), [])

    def test_empty(self):
        self.assertEqual(search("question", []), [])

if __name__ == "__main__":
    unittest.main()
