"""Local passage retrieval with BM25 and inspectable citations."""
import math
import re
from collections import Counter
from pathlib import Path

def tokens(text):
    return re.findall(r"\b\w+\b", text.casefold())

def index(root):
    root = Path(root)
    paths = [root] if root.is_file() else sorted(root.rglob("*"))
    passages = []
    for path in paths:
        if path.is_symlink() or not path.is_file() or path.suffix.lower() not in {".txt", ".md"}:
            continue
        if path.stat().st_size > 5_000_000:
            continue
        for start, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if line.strip():
                passages.append({"source": str(path), "line": start, "text": line})
    return passages

def search(question, passages, limit=5):
    if limit < 1:
        raise ValueError("limit must be positive")
    query = set(tokens(question))
    docs = [Counter(tokens(p["text"])) for p in passages]
    n = len(docs)
    if not n or not query:
        return []
    avg = sum(sum(d.values()) for d in docs) / n or 1
    df = {t: sum(t in d for d in docs) for t in query}
    results = []
    for p, d in zip(passages, docs):
        length = sum(d.values())
        score = sum(math.log(1 + (n-df[t]+0.5)/(df[t]+0.5)) * d[t]*2.2 /
                    (d[t]+1.2*(0.25+0.75*length/avg)) for t in query if d[t])
        if score > 0:
            results.append(dict(p, score=score))
    return sorted(results, key=lambda p: -p["score"])[:limit]
