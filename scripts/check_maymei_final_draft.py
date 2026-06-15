from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


AI_CLICHES = (
    "總體來說",
    "可以說是",
    "對玩家來說是一個不錯的選擇",
    "值得注意的是",
    "在這個過程中",
    "不只是",
    "更是",
)
AI_CLICHE_PATTERNS = (
    re.compile(r"不是[^。\n]{0,40}而是"),
    re.compile(r"不要[^。\n]{0,40}而是"),
)
BLOCKING_PATTERNS = AI_CLICHE_PATTERNS
JUDGMENT_MARKERS = ("我推薦", "我不建議", "我會", "最推薦", "最省事", "真的差很多", "直接", "先不要")
PLAYER_MARKERS = ("新手", "玩家", "省時間", "少走", "不用", "變強", "資源", "卡住", "後悔")
PROMISE_MARKERS = ("必看", "攻略", "省", "變強", "少走", "解鎖", "最強", "效率", "如果")


def split_paragraphs(text: str) -> list[str]:
    return [paragraph.strip() for paragraph in text.splitlines() if paragraph.strip()]


def repeated_starts(paragraphs: list[str]) -> bool:
    starts = [paragraph[:3] for paragraph in paragraphs if len(paragraph) >= 3]
    counts = Counter(starts)
    return any(count >= 3 for count in counts.values())


def evaluate_final_draft(
    draft: str,
    *,
    allowed_facts: list[str] | None = None,
    threshold: int = 85,
) -> dict[str, Any]:
    score = 100
    failed: list[str] = []
    paragraphs = split_paragraphs(draft)
    first_block = "\n".join(paragraphs[:2])

    cliches = [phrase for phrase in AI_CLICHES if phrase in draft]
    cliches.extend(pattern.pattern for pattern in AI_CLICHE_PATTERNS if pattern.search(draft))
    blocking_hits = [pattern.pattern for pattern in BLOCKING_PATTERNS if pattern.search(draft)]
    if cliches:
        score -= min(25, 8 * len(cliches))
        failed.append("ai_cliche")
    if blocking_hits:
        failed.append("blocking_phrase_pattern")

    if not any(marker in draft for marker in JUDGMENT_MARKERS):
        score -= 20
        failed.append("judgment_voice")

    if not any(marker in draft for marker in PLAYER_MARKERS):
        score -= 12
        failed.append("player_alignment")

    if not any(marker in first_block for marker in PROMISE_MARKERS):
        score -= 12
        failed.append("opening_promise")

    if repeated_starts(paragraphs):
        score -= 8
        failed.append("repeated_paragraph_start")

    if len(paragraphs) < 3:
        score -= 8
        failed.append("thin_structure")

    if allowed_facts:
        numeric_claims = re.findall(r"\d+(?:\.\d+)?%?|\d+\s*(?:個|隻|把|等|級|分鐘|小時)", draft)
        unsupported = [
            claim for claim in numeric_claims if not any(claim in fact for fact in allowed_facts)
        ]
        if unsupported:
            score -= min(15, 5 * len(unsupported))
            failed.append("unsupported_numeric_claim")

    score = max(score, 0)
    return {
        "score": score,
        "threshold": threshold,
        "passed": score >= threshold and not blocking_hits,
        "failed_checks": failed,
        "ai_cliches": cliches,
        "blocking_hits": blocking_hits,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check a final Maymei read-aloud draft for voice quality.")
    parser.add_argument("draft")
    parser.add_argument("--allowed-facts", action="append", default=[])
    parser.add_argument("--threshold", type=int, default=85)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    draft = Path(args.draft).read_text(encoding="utf-8")
    result = evaluate_final_draft(draft, allowed_facts=args.allowed_facts, threshold=args.threshold)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Maymei voice score: {result['score']} / {result['threshold']}")
        if result["failed_checks"]:
            print("Failed checks: " + ", ".join(result["failed_checks"]))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
