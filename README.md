# EvidenceQA

An open-source, local-first research engine that retrieves evidence and optionally generates answers with traceable citations. Python 3.10+; no mandatory paid API.

## Install

```sh
pip install .
evidenceqa "When do applications close?" ./examples
```

Optional PDF and semantic search: `pip install '.[pdf,semantic]'`. Semantic search downloads a pretrained model on first use. Scanned PDFs require OCR, not implemented.

## Online research

```sh
evidenceqa "What is photosynthesis?" --web
```

The web provider searches English Wikipedia and retrieves article extracts with revision links where available. It is not general web search or a real-time news service. Your question is sent to Wikipedia only when you enable --web.

## Local AI synthesis

Install and start Ollama separately, then download a compatible model, for example `ollama pull qwen2.5:3b`.

```sh
evidenceqa "When do applications close?" ./examples --model qwen2.5:3b
evidenceqa "What is photosynthesis?" --web --semantic --model qwen2.5:3b
```

The model receives retrieved text and the question on localhost. Each generated claim must cite valid evidence IDs and exact quotes; malformed answers are rejected. Exact quotation validation does **not** prove that a claim follows from the quote. Models can still misinterpret sources or follow malicious text. Inspect evidence, especially for high-stakes decisions. Semantic similarity and BM25 scores are not confidence estimates. Network requests and models may fail. No independent fact-checking or source trust scoring is provided.

## Tests

```sh
python -m unittest discover -s tests
```

Tests use mocked web and model responses; they do not establish live integration reliability.

MIT licensed. Contributions welcome.
