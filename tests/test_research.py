import json
import unittest
from evidenceqa.engine import Passage
from evidenceqa.research import research, retrieve
from evidenceqa.web import wikipedia

class ResearchTests(unittest.TestCase):
    def setUp(self):
        self.docs = [Passage("policy","line 1","Applications close Friday.")]

    def test_cited_answer(self):
        raw = {"claims":[{"statement":"The deadline is Friday.","citations":[{"id":1,"quote":"Applications close Friday."}]}]}
        result = research("applications close",self.docs,generate=lambda _:json.dumps(raw))
        self.assertEqual(result["status"],"generated")

    def test_invented_quote(self):
        raw = {"claims":[{"statement":"Monday","citations":[{"id":1,"quote":"Monday"}]}]}
        self.assertEqual(research("applications",self.docs,generate=lambda _:json.dumps(raw))["status"],"synthesis_failed")

    def test_invented_id(self):
        raw = {"claims":[{"statement":"Friday","citations":[{"id":9,"quote":"Friday"}]}]}
        self.assertEqual(research("applications",self.docs,generate=lambda _:json.dumps(raw))["status"],"synthesis_failed")

    def test_abstain(self):
        self.assertEqual(research("applications",self.docs,generate=lambda _:'{"claims":[]}')["status"],"insufficient_evidence")

    def test_no_evidence(self):
        self.assertEqual(research("astronomy",self.docs,generate=lambda _:self.fail("unexpected model call"))["status"],"no_evidence")

    def test_semantic(self):
        class Encoder:
            def encode(self,texts,normalize_embeddings):
                return [[1.,0.],[1.,0.]]
        self.assertEqual(retrieve("deadline",self.docs,encoder=Encoder())[0]["source"],"policy")

    def test_web(self):
        def fetch(params):
            if "list" in params:
                return {"query":{"search":[{"pageid":3}]}}
            return {"query":{"pages":[{"title":"Example","extract":"Public evidence.","revisions":[{"revid":123}]}]}}
        self.assertEqual(wikipedia("example",fetch=fetch)[0].source,"https://en.wikipedia.org/w/index.php?oldid=123")
