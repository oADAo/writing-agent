from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


PROMISE_MARKERS = ("必看", "買之前", "省", "少踩", "值不值得", "適合", "首發", "先等")
JUDGMENT_MARKERS = ("我推薦", "我會", "先等", "可以買", "觀望", "適合", "不建議", "最推薦")
PLAYER_MARKERS = ("玩家", "新手", "喜歡", "介意", "首發", "PC", "Switch", "主機")
NEXT_HOOK_MARKERS = ("再來", "接下來", "那", "最後", "如果你", "這裡")


def split_sections(text: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_title = "Opening"
    current_lines: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            sections.append((current_title, "\n".join(current_lines).strip()))
            current_title = line[3:].strip()
            current_lines = []
        elif not line.startswith("# "):
            current_lines.append(line)
    sections.append((current_title, "\n".join(current_lines).strip()))
    return [(title, body) for title, body in sections if body]


def evaluate_retention_beats(text: str, *, threshold: int = 80) -> dict[str, Any]:
    sections = split_sections(text)
    opening = sections[0][1] if sections else text[:300]
    missing: list[str] = []
    score = 100

    if not any(marker in opening for marker in PROMISE_MARKERS):
        missing.append("opening_promise")
        score -= 20

    body_sections = sections[1:] if len(sections) > 1 else sections
    weak_sections: list[str] = []
    for title, body in body_sections:
        has_judgment = any(marker in body for marker in JUDGMENT_MARKERS)
        has_player = any(marker in body for marker in PLAYER_MARKERS)
        if not (has_judgment and has_player):
            weak_sections.append(title)

    if weak_sections:
        score -= min(35, len(weak_sections) * 7)
        missing.append("section_player_judgment")

    if len(body_sections) >= 3 and not any(marker in text for marker in NEXT_HOOK_MARKERS):
        score -= 10
        missing.append("transition_hooks")

    if not re.search(r"B-?roll|B roll|畫面", text, re.IGNORECASE):
        score -= 10
        missing.append("broll_debt")

    score = max(0, score)
    return {
        "score": score,
        "threshold": threshold,
        "passed": score >= threshold,
        "missing": missing,
        "weak_sections": weak_sections,
        "section_count": len(body_sections),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Maymei draft retention beats.")
    parser.add_argument("draft")
    parser.add_argument("--threshold", type=int, default=80)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    text = Path(args.draft).read_text(encoding="utf-8")
    result = evaluate_retention_beats(text, threshold=args.threshold)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Maymei retention beat score: {result['score']} / {result['threshold']}")
        if result["missing"]:
            print("Missing: " + ", ".join(result["missing"]))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
