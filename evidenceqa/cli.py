import argparse
import json
from .engine import passages
from .research import research, ollama
from .web import wikipedia

def main():
    parser = argparse.ArgumentParser(description="Research questions with traceable sources.")
    parser.add_argument("question")
    parser.add_argument("path",nargs="?")
    parser.add_argument("--web",action="store_true",help="Send question to Wikipedia search")
    parser.add_argument("--semantic",action="store_true",help="Use optional sentence-transformers model")
    parser.add_argument("--model",help="Local Ollama model name")
    parser.add_argument("--limit",type=int,default=5)
    args = parser.parse_args()
    if not args.path and not args.web:
        parser.error("Provide a document path or --web")
    try:
        docs = list(passages(args.path)) if args.path else []
        if args.web:
            docs.extend(wikipedia(args.question))
        encoder = None
        if args.semantic:
            from sentence_transformers import SentenceTransformer
            encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        result = research(args.question,docs,args.limit,encoder,ollama(args.model) if args.model else None)
    except (OSError,ValueError,RuntimeError,ImportError) as exc:
        parser.error(str(exc))
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
