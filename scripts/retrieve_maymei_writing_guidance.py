from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from scripts.retrieve_maymei_samples import overlap_score
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.retrieve_maymei_samples import overlap_score


def score_sample(sample: dict[str, Any], *, topic: str, game: str, formula: str) -> float:
    title = str(sample.get("title") or "")
    score = float(sample.get("priority") or 0.0) / 100.0
    if formula and sample.get("formula") == formula:
        score += 3.0
    if game and game in title:
        score += 1.0
    score += overlap_score(topic, title)
    return round(score, 4)


def score_pair(pair: dict[str, Any], *, topic: str, formula: str) -> float:
    text = f"{pair.get('title', '')} {pair.get('fact_line', '')} {pair.get('maymei_line', '')}"
    score = 0.0
    if formula and pair.get("formula") == formula:
        score += 2.0
    score += overlap_score(topic, text)
    return round(score, 4)


def retrieve_guidance(
    system: dict[str, Any],
    *,
    topic: str,
    game: str = "",
    formula: str = "",
    sample_count: int = 5,
    pair_count: int = 8,
) -> dict[str, Any]:
    samples = [
        {**sample, "retrieval_score": score_sample(sample, topic=topic, game=game, formula=formula)}
        for sample in system.get("samples", [])
        if isinstance(sample, dict)
    ]
    samples.sort(key=lambda item: item["retrieval_score"], reverse=True)

    pairs = [
        {**pair, "retrieval_score": score_pair(pair, topic=topic, formula=formula)}
        for pair in system.get("transform_pairs", [])
        if isinstance(pair, dict)
    ]
    pairs.sort(key=lambda item: item["retrieval_score"], reverse=True)

    decision_cards = system.get("decision_cards", {})
    decision_card = decision_cards.get(formula) if formula else None
    if not decision_card and samples:
        decision_card = decision_cards.get(str(samples[0].get("formula") or ""))

    return {
        "topic": topic,
        "game": game,
        "formula": formula,
        "decision_card": decision_card or {},
        "reference_samples": samples[:sample_count],
        "line_transform_pairs": pairs[:pair_count],
        "chapter_card_template": {
            "觀眾問題": "",
            "玫玫判斷": "",
            "可用事實": [],
            "玩家翻譯": "",
            "禁用句型": [
                "不是...而是...",
                "不要...而是...",
                "總體來說",
                "值得注意的是",
                "英文 buyer guide 排序",
            ],
        },
        "drafting_order": [
            "先寫 chapter card，不直接寫正文。",
            "每章先給玫玫判斷，再放事實。",
            "把 fact line 轉成玩家能用的選擇句。",
            "逐章生成，逐章 AI 審稿。",
        ],
    }


def render_markdown(guidance: dict[str, Any]) -> str:
    lines = [
        "# Maymei Writing Guidance",
        "",
        "## Topic",
        f"- Topic: {guidance['topic']}",
        f"- Game: {guidance['game'] or '未指定'}",
        f"- Formula: {guidance['formula'] or '未指定'}",
        "",
        "## Decision Card",
    ]
    card = guidance.get("decision_card") or {}
    if card:
        lines.append(f"- Formula: {card.get('formula')}")
        lines.append("- Drafting directives:")
        lines.extend(f"  - {item}" for item in card.get("drafting_directives", []))
        lines.append("- Must not:")
        lines.extend(f"  - {item}" for item in card.get("must_not", []))
    else:
        lines.append("- 無對應 decision card。")

    lines.extend(["", "## Reference Samples"])
    for sample in guidance.get("reference_samples", []):
        lines.extend(
            [
                f"- `{sample.get('formula')}` {sample.get('title')}",
                f"  - Source: `{sample.get('source_path')}`",
                f"  - Score: `{sample.get('retrieval_score')}`",
            ]
        )

    lines.extend(["", "## Line Transform Pairs"])
    for pair in guidance.get("line_transform_pairs", []):
        lines.extend(
            [
                f"- Transformation: {pair.get('transformation')}",
                f"  - Fact: {pair.get('fact_line')}",
                f"  - Maymei: {pair.get('maymei_line')}",
            ]
        )

    lines.extend(["", "## Chapter Card Template"])
    template = guidance["chapter_card_template"]
    for key, value in template.items():
        lines.append(f"- {key}: {value if value else ''}")
    lines.append("")
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Retrieve Maymei writing guidance for a researched script topic.")
    parser.add_argument("--system", default=str(repo_root / "workspace" / "memory" / "style-corpus" / "maymei-writing-system.json"))
    parser.add_argument("--topic", required=True)
    parser.add_argument("--game", default="")
    parser.add_argument("--formula", default="")
    parser.add_argument("--sample-count", type=int, default=5)
    parser.add_argument("--pair-count", type=int, default=8)
    parser.add_argument("--output")
    parser.add_argument("--markdown", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    system = json.loads(Path(args.system).read_text(encoding="utf-8"))
    guidance = retrieve_guidance(
        system,
        topic=args.topic,
        game=args.game,
        formula=args.formula,
        sample_count=args.sample_count,
        pair_count=args.pair_count,
    )
    rendered = render_markdown(guidance) if args.markdown else json.dumps(guidance, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
