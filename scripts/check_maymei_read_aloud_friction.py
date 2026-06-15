from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SENTENCE_SPLIT_RE = re.compile(r"[。！？\n]")


def sentence_units(text: str) -> list[str]:
    return [item.strip() for item in SENTENCE_SPLIT_RE.split(text) if item.strip()]


def evaluate_read_aloud_friction(text: str, *, threshold: int = 85) -> dict[str, Any]:
    sentences = sentence_units(text)
    long_sentences = [sentence for sentence in sentences if len(sentence) > 90]
    comma_heavy = [sentence for sentence in sentences if sentence.count("、") >= 5]
    colon_heavy = [sentence for sentence in sentences if sentence.count("：") + sentence.count(":") >= 2]

    average_length = round(sum(len(sentence) for sentence in sentences) / max(1, len(sentences)), 2)
    score = 100
    score -= min(30, len(long_sentences) * 8)
    score -= min(45, len(comma_heavy) * 18)
    score -= min(15, len(colon_heavy) * 5)
    if average_length > 55:
        score -= 10
    score = max(0, score)

    return {
        "score": score,
        "threshold": threshold,
        "passed": score >= threshold,
        "average_sentence_length": average_length,
        "long_sentence_count": len(long_sentences),
        "comma_heavy_count": len(comma_heavy),
        "colon_heavy_count": len(colon_heavy),
        "long_sentence_samples": long_sentences[:3],
        "comma_heavy_samples": comma_heavy[:3],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Maymei draft read-aloud friction.")
    parser.add_argument("draft")
    parser.add_argument("--threshold", type=int, default=85)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    text = Path(args.draft).read_text(encoding="utf-8")
    result = evaluate_read_aloud_friction(text, threshold=args.threshold)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Maymei read-aloud score: {result['score']} / {result['threshold']}")
        print(f"Average sentence length: {result['average_sentence_length']}")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
