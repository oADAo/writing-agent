from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def _flatten(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value]
    return []


def build_formula_cards(forensics: list[dict[str, Any]], *, min_samples: int = 5) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in forensics:
        analysis = item.get("style_forensics", item)
        formula = str(analysis.get("formula") or item.get("formula") or "一般攻略")
        grouped[formula].append(analysis)

    cards: dict[str, dict[str, Any]] = {}
    for formula, items in sorted(grouped.items()):
        opening_patterns = Counter(str(item.get("opening_promise_pattern") or "") for item in items)
        structures = Counter()
        transitions = Counter()
        for item in items:
            structures.update(_flatten(item.get("learnable_structure")))
            transitions.update(_flatten(item.get("transitions")))
        cards[formula] = {
            "formula": formula,
            "status": "ready" if len(items) >= min_samples else "insufficient_data",
            "sample_count": len(items),
            "opening_patterns": [value for value, _ in opening_patterns.most_common(3) if value],
            "common_structures": [value for value, _ in structures.most_common(6)],
            "common_transitions": [value for value, _ in transitions.most_common(6)],
            "anti_ai_notes": [
                "Keep the promise concrete: say what the player saves, gains, avoids, or unlocks.",
                "Use samples for rhythm and ordering only; do not reuse old facts or exact phrasing.",
                "Add judgment voice every few paragraphs so the draft does not become a neutral report.",
            ],
        }
    return cards


def render_formula_cards_markdown(cards: dict[str, dict[str, Any]]) -> str:
    lines = ["# Maymei Formula Cards", ""]
    for formula, card in cards.items():
        lines.extend(
            [
                f"## {formula}",
                f"- Status: `{card['status']}`",
                f"- Sample count: `{card['sample_count']}`",
                "- Opening patterns:",
            ]
        )
        lines.extend(f"  - {item}" for item in card.get("opening_patterns", []) or ["資料不足"])
        lines.append("- Common structures:")
        lines.extend(f"  - {item}" for item in card.get("common_structures", []) or ["資料不足"])
        lines.append("- Anti-AI notes:")
        lines.extend(f"  - {item}" for item in card.get("anti_ai_notes", []))
        lines.append("")
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    default_dir = repo_root / "workspace" / "memory" / "style-corpus"
    parser = argparse.ArgumentParser(description="Build reusable Maymei formula cards from style forensics.")
    parser.add_argument("--forensics", default=str(default_dir / "maymei-style-forensics.json"))
    parser.add_argument("--json-output", default=str(default_dir / "maymei-formula-cards.json"))
    parser.add_argument("--markdown-output", default=str(default_dir / "maymei-formula-cards.md"))
    parser.add_argument("--min-samples", type=int, default=5)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    payload = json.loads(Path(args.forensics).read_text(encoding="utf-8"))
    records = payload.get("records", []) if isinstance(payload, dict) else payload
    cards = build_formula_cards([item for item in records if isinstance(item, dict)], min_samples=args.min_samples)
    json_output = Path(args.json_output)
    markdown_output = Path(args.markdown_output)
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(cards, ensure_ascii=False, indent=2), encoding="utf-8")
    markdown_output.write_text(render_formula_cards_markdown(cards), encoding="utf-8")
    print(f"Wrote {len(cards)} formula cards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
