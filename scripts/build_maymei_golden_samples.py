from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable


KEEP_RE = re.compile(r"[\w\u4e00-\u9fff]+", re.UNICODE)
KNOWN_GAME_PATTERNS = (
    (re.compile(r"薩爾達傳說\s*[:：]?\s*王國之淚|王國之淚", re.I), "薩爾達傳說：王國之淚"),
    (re.compile(r"薩爾達傳說\s*[:：]\s*王國", re.I), "薩爾達傳說：王國之淚"),
    (re.compile(r"黑神話\s*[:：]?\s*悟空|黑神話悟空|Black Myth", re.I), "黑神話悟空"),
    (re.compile(r"魔物獵人\s*荒野|Monster Hunter Wilds", re.I), "魔物獵人荒野"),
    (re.compile(r"魔物獵人物語\s*3", re.I), "魔物獵人物語3"),
    (re.compile(r"寶可夢\s*(?:傳說)?\s*Z[- ]?A|Pokemon Legends Z[- ]?A|Pok[eé]mon Legends Z[- ]?A", re.I), "寶可夢傳說 Z-A"),
    (re.compile(r"寶可夢\s*朱紫|Pokemon Scarlet|Pokemon Violet|Pok[eé]mon Scarlet|Pok[eé]mon Violet", re.I), "寶可夢朱紫"),
    (re.compile(r"寶可夢卡牌|Pok[eé]mon Trading Card Game Pocket", re.I), "寶可夢卡牌"),
    (re.compile(r"Pokopia|寶可夢\s*Pokopia", re.I), "Pokopia"),
    (re.compile(r"Pokemon Champions|Pok[eé]mon Champions|寶可夢\s*Champions", re.I), "Pokemon Champions"),
    (re.compile(r"光與影\s*33\s*號遠征隊|Clair Obscur", re.I), "光與影33號遠征隊"),
    (re.compile(r"Tomodachi Life|朋友收藏集", re.I), "Tomodachi Life"),
    (re.compile(r"博德之門\s*3|Baldur'?s Gate\s*3", re.I), "博德之門3"),
    (re.compile(r"艾爾登法環\s*(?:DLC)?\s*黃金樹幽影|黃金樹幽影", re.I), "艾爾登法環 DLC 黃金樹幽影"),
    (re.compile(r"艾爾登法環\s*黑夜君臨|艾爾登法環《黑夜君臨》|黑夜君臨", re.I), "艾爾登法環 黑夜君臨"),
    (re.compile(r"艾爾登法環|Elden Ring", re.I), "艾爾登法環"),
    (re.compile(r"暗喻幻想|ReFantazio", re.I), "暗喻幻想"),
    (re.compile(r"三國無雙起源", re.I), "三國無雙起源"),
    (re.compile(r"智慧的再現", re.I), "薩爾達傳說：智慧的再現"),
    (re.compile(r"Hades\s*II|黑帝斯\s*2", re.I), "Hades II 黑帝斯 2"),
    (re.compile(r"死亡擱淺\s*2|死亡擱淺2", re.I), "死亡擱淺2"),
    (re.compile(r"明末\s*[:：]\s*淵虛之羽", re.I), "明末：淵虛之羽"),
    (re.compile(r"歧路旅人\s*0", re.I), "歧路旅人0"),
    (re.compile(r"國津神", re.I), "國津神：女神之道"),
    (re.compile(r"鼠托邦|Ratopia", re.I), "鼠托邦 Ratopia"),
    (re.compile(r"皮克敏\s*4|Pikmin\s*4", re.I), "皮克敏4"),
    (re.compile(r"瑪利歐|Mario", re.I), "瑪利歐系列"),
    (re.compile(r"動物森友會|Animal Crossing", re.I), "動物森友會"),
    (re.compile(r"\d+\s*月最新精選強作|2025\s*必玩|2026年遊戲大作推薦|遊戲大作推薦|GFN年度必玩", re.I), "遊戲推薦清單"),
)
GENERIC_TITLE_TERMS = (
    "超詳細",
    "超實用",
    "實用",
    "完全攻略",
    "開荒",
    "新手",
    "必看",
    "必做",
    "攻略",
    "技巧",
    "推薦",
    "排行",
    "top",
    "買前",
    "最強",
    "最快",
    "刷錢",
    "刷經驗",
    "小知識",
    "月份",
    "pc",
    "switch",
    "ps5",
    "xbox",
)


def normalize_title(value: str) -> str:
    parts = KEEP_RE.findall(value.lower())
    return "".join(parts)


def title_similarity(left: str, right: str) -> float:
    left_norm = normalize_title(left)
    right_norm = normalize_title(right)
    if not left_norm or not right_norm:
        return 0.0
    ratio = SequenceMatcher(None, left_norm, right_norm).ratio()
    left_tokens = set(KEEP_RE.findall(left.lower()))
    right_tokens = set(KEEP_RE.findall(right.lower()))
    token_ratio = 0.0
    if left_tokens and right_tokens:
        token_ratio = len(left_tokens & right_tokens) / len(left_tokens | right_tokens)
    return max(ratio, token_ratio)


def clean_game_candidate(value: str) -> str:
    cleaned = re.sub(r"\s+", " ", value).strip(" \t\r\n|-_")
    return cleaned.replace(" :", "：").replace(": ", "：").replace(":", "：")


def is_generic_title_fragment(value: str) -> bool:
    normalized = value.strip().lower()
    if not normalized or len(normalized) > 28:
        return True
    return any(term in normalized for term in GENERIC_TITLE_TERMS)


def infer_game_name(*values: str) -> str:
    text = " | ".join(str(value or "") for value in values)
    for pattern, canonical in KNOWN_GAME_PATTERNS:
        if pattern.search(text):
            return canonical

    for candidate in re.findall(r"【([^】]+)】", text):
        cleaned = clean_game_candidate(candidate)
        if cleaned and not is_generic_title_fragment(cleaned):
            return cleaned

    for candidate in re.split(r"[|｜]", text):
        cleaned = clean_game_candidate(candidate)
        if cleaned and not is_generic_title_fragment(cleaned):
            return cleaned
    return ""


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        return [item for item in payload["records"] if isinstance(item, dict)]
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    return []


def normalize_source_record(record: dict[str, Any]) -> dict[str, Any]:
    title = str(record.get("title") or record.get("name") or "").strip()
    source_path = (
        record.get("source_path")
        or record.get("source_file")
        or record.get("filename")
        or record.get("web_view_link")
        or record.get("webViewLink")
        or ""
    )
    return {
        "title": title,
        "game": str(record.get("game") or infer_game_name(title, str(record.get("opening_promise") or ""), str(source_path))).strip(),
        "formula": str(record.get("formula") or "一般攻略").strip(),
        "primary_category": str(record.get("primary_category") or record.get("formula") or "完整攻略").strip(),
        "source_path": str(source_path).strip(),
        "opening_promise": str(record.get("opening_promise") or title).strip(),
        "intro_line": str(record.get("intro_line") or "").strip(),
        "char_count": int(record.get("char_count") or 0),
        "paragraph_count": int(record.get("paragraph_count") or 0),
    }


def load_source_records(paths: Iterable[Path]) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    for path in paths:
        if not path.exists():
            continue
        for record in extract_records(load_json(path)):
            normalized = normalize_source_record(record)
            if normalized["title"]:
                sources.append(normalized)
    return sources


def match_video_to_sources(
    metric: dict[str, Any],
    sources: list[dict[str, Any]],
    *,
    min_similarity: float = 0.45,
) -> dict[str, Any] | None:
    title = str(metric.get("title") or "")
    best_source: dict[str, Any] | None = None
    best_score = 0.0
    for source in sources:
        score = max(
            title_similarity(title, str(source.get("title") or "")),
            title_similarity(title, str(source.get("opening_promise") or "")),
        )
        if score > best_score:
            best_source = source
            best_score = score
    if best_source is None or best_score < min_similarity:
        return None
    return {**best_source, "match_similarity": round(best_score, 4)}


def percentile_map(records: list[dict[str, Any]], key: str) -> dict[str, float]:
    values = sorted({float(item.get(key) or 0) for item in records})
    if not values:
        return {}
    if len(values) == 1:
        return {str(values[0]): 1.0}
    return {str(value): index / (len(values) - 1) for index, value in enumerate(values)}


def score_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    view_percentiles = percentile_map(candidates, "view_count")
    like_percentiles = percentile_map(candidates, "like_count")
    rate_percentiles = percentile_map(candidates, "like_rate")
    scored: list[dict[str, Any]] = []
    for item in candidates:
        view_score = view_percentiles.get(str(float(item.get("view_count") or 0)), 0.0)
        like_score = like_percentiles.get(str(float(item.get("like_count") or 0)), 0.0)
        rate_score = rate_percentiles.get(str(float(item.get("like_rate") or 0)), 0.0)
        score = (view_score * 50.0) + (like_score * 30.0) + (rate_score * 20.0)
        scored.append({**item, "score": round(score, 2), "selected_as_gold": True})
    return scored


def build_candidate_records(
    metrics: list[dict[str, Any]],
    sources: list[dict[str, Any]],
    *,
    min_similarity: float = 0.45,
) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    seen_sources: set[str] = set()
    for metric in metrics:
        match = match_video_to_sources(metric, sources, min_similarity=min_similarity)
        if not match:
            continue
        source_doc = str(match.get("source_path") or match.get("title") or "")
        dedupe_key = normalize_title(source_doc)
        if dedupe_key in seen_sources:
            continue
        seen_sources.add(dedupe_key)
        candidates.append(
            {
                "video_id": metric.get("video_id", ""),
                "url": metric.get("url", ""),
                "title": metric.get("title", ""),
                "view_count": int(metric.get("view_count") or 0),
                "like_count": int(metric.get("like_count") or 0),
                "like_rate": float(metric.get("like_rate") or 0.0),
                "comment_count": int(metric.get("comment_count") or 0),
                "upload_date": metric.get("upload_date", ""),
                "duration": int(metric.get("duration") or 0),
                "formula": match.get("formula", ""),
                "game": infer_game_name(
                    str(metric.get("title") or ""),
                    str(match.get("title") or ""),
                    str(match.get("opening_promise") or ""),
                )
                or match.get("game", ""),
                "primary_category": match.get("primary_category", ""),
                "source_doc": source_doc,
                "source_title": match.get("title", ""),
                "opening_promise": match.get("opening_promise", ""),
                "match_similarity": match.get("match_similarity", 0.0),
            }
        )
    return score_candidates(candidates)


def select_balanced(
    candidates: list[dict[str, Any]],
    *,
    target_count: int,
    per_formula_cap: int | None,
) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in sorted(candidates, key=lambda value: (value["score"], value.get("comment_count", 0)), reverse=True):
        groups[str(item.get("formula") or "一般攻略")].append(item)

    formulas = sorted(groups, key=lambda formula: groups[formula][0]["score"], reverse=True)
    if per_formula_cap is None and formulas:
        per_formula_cap = max(1, math.ceil(target_count / len(formulas)) + 1)

    selected: list[dict[str, Any]] = []
    selected_ids: set[str] = set()
    while len(selected) < target_count:
        before = len(selected)
        for formula in formulas:
            already_for_formula = sum(1 for item in selected if item.get("formula") == formula)
            if per_formula_cap is not None and already_for_formula >= per_formula_cap:
                continue
            while groups[formula]:
                item = groups[formula].pop(0)
                key = str(item.get("video_id") or item.get("source_doc"))
                if key in selected_ids:
                    continue
                selected.append(item)
                selected_ids.add(key)
                break
            if len(selected) >= target_count:
                break
        if len(selected) == before:
            break
    return selected


def select_golden_samples(
    metrics: list[dict[str, Any]],
    sources: list[dict[str, Any]],
    *,
    target_count: int = 100,
    per_formula_cap: int | None = None,
    min_similarity: float = 0.45,
) -> list[dict[str, Any]]:
    candidates = build_candidate_records(metrics, sources, min_similarity=min_similarity)
    return select_balanced(candidates, target_count=target_count, per_formula_cap=per_formula_cap)


def default_source_paths(repo_root: Path) -> list[Path]:
    return [
        repo_root / "workspace" / "memory" / "style-corpus" / "google-maymei-game-scripts.json",
        repo_root / "workspace" / "memory" / "style-corpus" / "google-docs-corpus.json",
        repo_root / "workspace" / "memory" / "style-corpus" / "local-docx-corpus.json",
        repo_root
        / "workspace"
        / "source-docs"
        / "google-maymei-yt-scripts-high-precision-clean-2026-03-31"
        / "manifest.json",
    ]


def parse_args(argv: list[str]) -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Build balanced Maymei golden script samples.")
    parser.add_argument(
        "--metrics",
        default=str(repo_root / "workspace" / "memory" / "style-corpus" / "maymei-video-metrics.json"),
    )
    parser.add_argument(
        "--output",
        default=str(repo_root / "workspace" / "memory" / "style-corpus" / "maymei-golden-samples.json"),
    )
    parser.add_argument("--target-count", type=int, default=100)
    parser.add_argument("--per-formula-cap", type=int)
    parser.add_argument("--min-similarity", type=float, default=0.45)
    parser.add_argument("--source-json", action="append", default=[])
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    repo_root = Path(__file__).resolve().parents[1]
    metrics_payload = load_json(Path(args.metrics))
    metrics = extract_records(metrics_payload)
    source_paths = [Path(path) for path in args.source_json] or default_source_paths(repo_root)
    sources = load_source_records(source_paths)
    selected = select_golden_samples(
        metrics,
        sources,
        target_count=args.target_count,
        per_formula_cap=args.per_formula_cap,
        min_similarity=args.min_similarity,
    )
    payload = {"source_metrics": args.metrics, "total": len(selected), "records": selected}
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(selected)} golden samples to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
