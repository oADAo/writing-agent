from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


TOKEN_RE = re.compile(r"[\w\u4e00-\u9fff]+", re.UNICODE)


def tokens(value: str) -> set[str]:
    raw_tokens = set(TOKEN_RE.findall(value.lower()))
    compact = "".join(raw_tokens)
    char_tokens = {compact[index : index + 2] for index in range(max(len(compact) - 1, 0))}
    return raw_tokens | {token for token in char_tokens if token}


def overlap_score(left: str, right: str) -> float:
    left_tokens = tokens(left)
    right_tokens = tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def score_sample(sample: dict[str, Any], *, topic: str, game: str, formula: str) -> float:
    title = str(sample.get("title") or sample.get("source_title") or "")
    score = float(sample.get("score") or 0.0) / 100.0
    if formula and str(sample.get("formula") or "") == formula:
        score += 2.0
    if game and game in title:
        score += 1.0
    score += overlap_score(topic, title)
    return round(score, 4)


def retrieve_samples(
    samples: list[dict[str, Any]],
    *,
    topic: str,
    game: str = "",
    formula: str = "",
    main_count: int = 3,
    auxiliary_count: int = 2,
) -> dict[str, list[dict[str, Any]]]:
    eligible = [sample for sample in samples if sample.get("selected_as_gold", True)]
    scored = [
        {**sample, "retrieval_score": score_sample(sample, topic=topic, game=game, formula=formula)}
        for sample in eligible
    ]
    formula_matches = [sample for sample in scored if formula and sample.get("formula") == formula]
    formula_matches.sort(key=lambda item: item["retrieval_score"], reverse=True)
    main_samples = formula_matches[:main_count]

    used = {str(item.get("video_id") or item.get("source_doc")) for item in main_samples}
    remaining = [
        sample
        for sample in sorted(scored, key=lambda item: item["retrieval_score"], reverse=True)
        if str(sample.get("video_id") or sample.get("source_doc")) not in used
    ]
    if len(main_samples) < main_count:
        needed = main_count - len(main_samples)
        main_samples.extend(remaining[:needed])
        used.update(str(item.get("video_id") or item.get("source_doc")) for item in main_samples)
        remaining = [
            sample for sample in remaining if str(sample.get("video_id") or sample.get("source_doc")) not in used
        ]

    return {
        "main_samples": main_samples[:main_count],
        "auxiliary_samples": remaining[:auxiliary_count],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Retrieve Maymei golden samples for a new script topic.")
    parser.add_argument("--samples", default=str(repo_root / "workspace" / "memory" / "style-corpus" / "maymei-golden-samples.json"))
    parser.add_argument("--topic", required=True)
    parser.add_argument("--game", default="")
    parser.add_argument("--formula", default="")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--output")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    payload = json.loads(Path(args.samples).read_text(encoding="utf-8"))
    samples = payload.get("records", []) if isinstance(payload, dict) else payload
    result = retrieve_samples(
        [item for item in samples if isinstance(item, dict)],
        topic=args.topic,
        game=args.game,
        formula=args.formula,
        main_count=min(args.limit, 3),
        auxiliary_count=max(args.limit - 3, 0),
    )
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
