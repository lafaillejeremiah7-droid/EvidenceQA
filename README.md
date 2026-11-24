# EvidenceQA

EvidenceQA is a privacy-first Python tool for finding relevant, traceable evidence in documents. Its goal is to help students, researchers and the public navigate policies, instructions, reports and other documents without paying for an AI service.

## Quick start

Requires Python 3.10 or newer.

```sh
pip install .
evidenceqa "When do applications close?" ./examples
```

For PDF text extraction, install with `pip install '.[pdf]'`. Scanned PDFs require OCR, which is not yet supported.

## What it does

- Searches local text, Markdown and text-based PDF files.
- Ranks excerpts using BM25 lexical relevance.
- Returns exact source paths and line ranges or PDF page references.
- Returns no evidence when no query terms match.
- Runs locally without an API key or network access after installation.

The current release is an **extractive retrieval prototype**, not a general-purpose AI chatbot or fact checker. Scores are not probabilities. Read original sources before making decisions. No web search, generated answers, semantic retrieval or OCR is implemented yet.

## Development

```sh
python -m unittest discover -s tests
```

See CONTRIBUTING.md for contribution guidance.

## Roadmap

1. Evaluate retrieval on public question-answer benchmarks.
2. Improve passage boundaries, synonyms and multilingual retrieval.
3. Add optional local model synthesis with citation checking and explicit abstention.
4. Add opt-in public-source retrieval and a local user interface.

MIT licensed.
