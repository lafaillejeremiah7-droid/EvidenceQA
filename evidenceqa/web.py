"""Opt-in public research using the English Wikipedia search API."""
import json
from datetime import datetime, timezone
from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen
from .engine import Passage

def _get(params):
    url = "https://en.wikipedia.org/w/api.php?" + urlencode(dict(params,format="json",formatversion=2))
    req = Request(url,headers={"User-Agent":"EvidenceQA/0.2 (open-source research; https://github.com/lafaillejeremiah7-droid/EvidenceQA)"})
    with urlopen(req,timeout=20) as response:
        data = response.read(4_000_001)
    if len(data)>4_000_000:
        raise ValueError("Web response too large")
    return json.loads(data)

def wikipedia(question, limit=5, fetch=_get):
    if not 1<=limit<=10:
        raise ValueError("Web result limit must be 1-10")
    found = fetch({"action":"query","list":"search","srsearch":question,"srlimit":limit})
    ids = [str(int(item["pageid"])) for item in found.get("query",{}).get("search",[])]
    if not ids:
        return []
    data = fetch({"action":"query","prop":"extracts|revisions","explaintext":1,"exlimit":limit,"rvprop":"ids","pageids":"|".join(ids)})
    results = []
    for page in data.get("query",{}).get("pages",[]):
        revs = page.get("revisions",[])
        url = "https://en.wikipedia.org/wiki/" + quote(page["title"].replace(" ","_"))
        if revs:
            url = "https://en.wikipedia.org/w/index.php?oldid=" + str(int(revs[0]["revid"]))
        text = page.get("extract","")
        timestamp = datetime.now(timezone.utc).isoformat()
        for i in range(0,min(len(text),30000),1000):
            excerpt = text[i:i+1000]
            if excerpt.strip():
                results.append(Passage(url,f"{page['title']}; characters {i+1}-{i+len(excerpt)}; retrieved {timestamp}",excerpt))
    return results
