from __future__ import annotations

import argparse
import json
import sys
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


def split_blocks(text: str) -> list[str]:
    blocks = [block.strip() for block in text.replace("\r\n", "\n").split("\n\n")]
    return [block for block in blocks if block]


def align_revisions(ai_text: str, user_text: str, *, min_similarity: float = 0.05) -> list[dict[str, Any]]:
    ai_blocks = split_blocks(ai_text)
    user_blocks = split_blocks(user_text)
    pairs: list[dict[str, Any]] = []
    used_user_indexes: set[int] = set()

    for ai_block in ai_blocks:
        best_index = -1
        best_score = 0.0
        for index, user_block in enumerate(user_blocks):
            if index in used_user_indexes:
                continue
            score = SequenceMatcher(None, ai_block, user_block).ratio()
            if score > best_score:
                best_index = index
                best_score = score
        if best_index >= 0 and best_score >= min_similarity and ai_block != user_blocks[best_index]:
            used_user_indexes.add(best_index)
            pairs.append(
                {
                    "ai_line": ai_block,
                    "user_line": user_blocks[best_index],
                    "similarity": round(best_score, 4),
                    "transformation": "user_revision",
                }
            )

    return pairs


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract Maymei line transform pairs from user revisions.")
    parser.add_argument("--ai-draft", required=True)
    parser.add_argument("--user-revision", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--min-similarity", type=float, default=0.05)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    ai_text = Path(args.ai_draft).read_text(encoding="utf-8")
    user_text = Path(args.user_revision).read_text(encoding="utf-8")
    pairs = align_revisions(ai_text, user_text, min_similarity=args.min_similarity)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "".join(json.dumps(pair, ensure_ascii=False) + "\n" for pair in pairs),
        encoding="utf-8",
    )
    print(json.dumps({"pairs": len(pairs), "output": str(output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
