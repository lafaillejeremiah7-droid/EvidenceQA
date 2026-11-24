"""Extract and rank evidence without sending documents to external services."""
from collections import Counter
from dataclasses import dataclass, asdict
import math
from pathlib import Path
import re

STOP = frozenset("a an the is are was were be been of to for in on at and or what which when where how why who does do did can could would should i you my your it that this with from".split())

def terms(text):
    return [w for w in re.findall(r"[^\W_]+", text.casefold()) if w not in STOP]

@dataclass(frozen=True)
class Passage:
    source: str
    locator: str
    text: str

def passages(root):
    root = Path(root)
    if not root.exists():
        raise FileNotFoundError(root)
    paths = [root] if root.is_file() else sorted(root.rglob("*"))
    for path in paths:
        if path.is_symlink() or not path.is_file() or path.stat().st_size > 20_000_000:
            continue
        if any(part in {".git", ".venv", "node_modules"} for part in path.parts):
            continue
        if path.suffix.lower() in {".txt", ".md", ".rst"}:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            for i in range(0, len(lines), 4):
                text = "\n".join(lines[i:i+4]).strip()
                if text:
                    yield Passage(str(path), f"lines {i+1}-{min(i+4,len(lines))}", text)
        elif path.suffix.lower() == ".pdf":
            try:
                from pypdf import PdfReader
            except ImportError as exc:
                raise RuntimeError("PDF support requires pip install '.[pdf]'") from exc
            reader = PdfReader(path)
            for page, obj in enumerate(reader.pages, 1):
                text = obj.extract_text() or ""
                for i in range(0, len(text), 1200):
                    if text[i:i+1200].strip():
                        yield Passage(str(path), f"page {page}, characters {i+1}-{min(i+1200,len(text))}", text[i:i+1200])

def answer(question, documents, limit=5):
    if limit < 1:
        raise ValueError("limit must be positive")
    q = set(terms(question))
    docs = list(documents)
    counts = [Counter(terms(p.text)) for p in docs]
    n = len(docs)
    if not q or not n:
        return {"status": "no_evidence", "evidence": []}
    avg = sum(map(lambda c: sum(c.values()), counts)) / n or 1
    df = {t: sum(t in c for c in counts) for t in q}
    hits = []
    for p,c in zip(docs,counts):
        overlap = q.intersection(c)
        if not overlap:
            continue
        score = sum(math.log(1+(n-df[t]+.5)/(df[t]+.5))*c[t]*2.2/(c[t]+1.2*(.25+.75*sum(c.values())/avg)) for t in overlap)
        hits.append(dict(asdict(p), relevance=round(score,6), matched_terms=sorted(overlap)))
    hits.sort(key=lambda h: -h["relevance"])
    return {"status": "evidence_found" if hits else "no_evidence", "evidence": hits[:limit],
            "note": "Retrieved excerpts are not verified conclusions. Relevance is not confidence."}
