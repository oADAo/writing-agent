from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


PHRASE_PATTERNS = (
    "總體來說",
    "可以說是",
    "值得注意的是",
    "在這個過程中",
    "對玩家來說是一個不錯的選擇",
    "本作提供了豐富",
    "沉浸式體驗",
    "具有一定",
    "研究顯示",
    "這輪研究",
    "我這次查到",
)

REGEX_PATTERNS = (
    re.compile(r"不是[^。\n]{0,50}而是"),
    re.compile(r"不要[^。\n]{0,50}而是"),
    re.compile(r"不只是[^。\n]{0,50}更是"),
)
BLOCKING_PATTERNS = REGEX_PATTERNS


def evaluate_ai_patterns(text: str, *, threshold: int = 85) -> dict[str, Any]:
    phrase_hits = [phrase for phrase in PHRASE_PATTERNS if phrase in text]
    regex_hits = [pattern.pattern for pattern in REGEX_PATTERNS if pattern.search(text)]
    blocking_hits = [pattern.pattern for pattern in BLOCKING_PATTERNS if pattern.search(text)]
    hits = phrase_hits + regex_hits

    score = max(0, 100 - min(70, len(hits) * 10))
    return {
        "score": score,
        "threshold": threshold,
        "passed": score >= threshold and not blocking_hits,
        "hits": hits,
        "blocking_hits": blocking_hits,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Traditional Chinese copy for Maymei AI-tone patterns.")
    parser.add_argument("draft")
    parser.add_argument("--threshold", type=int, default=85)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    text = Path(args.draft).read_text(encoding="utf-8")
    result = evaluate_ai_patterns(text, threshold=args.threshold)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Maymei AI pattern score: {result['score']} / {result['threshold']}")
        if result["hits"]:
            print("Hits: " + ", ".join(result["hits"]))
        if result["blocking_hits"]:
            print("Blocking hits: " + ", ".join(result["blocking_hits"]))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
