import argparse
import json
from .engine import answer, passages

def main():
    parser = argparse.ArgumentParser(description="Find cited evidence in local documents.")
    parser.add_argument("question")
    parser.add_argument("path")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    try:
        result = answer(args.question, passages(args.path), args.limit)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
