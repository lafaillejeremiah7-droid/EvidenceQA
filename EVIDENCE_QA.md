# Evidence QA

A local, dependency-free Python 3.10+ tool for finding relevant passages in text and Markdown documents. It returns source paths and line numbers, not generated claims. No API key is required.

## Usage

From the repository root:

```sh
python -m evidence_qa "When do applications close?" ./documents
python -m unittest discover -s tests -p test_evidence_qa.py
```

Results are JSON. BM25 scores measure lexical relevance, not truth or confidence. A match does not establish that a question has been answered. Review original documents before relying on results.

## Roadmap

- PDF extraction and page citations
- Better passage segmentation and retrieval evaluation
- Optional local model synthesis with citation checks
- Controlled retrieval of public sources

The prototype is isolated from legacy repository code. Licensing and release preparation are pending.
