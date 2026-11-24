import argparse
import json
from .engine import index, search

def main():
    parser = argparse.ArgumentParser(description="Retrieve cited passages from local documents.")
    parser.add_argument("question")
    parser.add_argument("path")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    hits = search(args.question, index(args.path), args.limit)
    print(json.dumps({"status": "matches" if hits else "no_matches", "evidence": hits}, indent=2))

if __name__ == "__main__":
    main()
