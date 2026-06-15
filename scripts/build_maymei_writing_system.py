from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    from scripts.build_article_corpus_index import (
        classify_formula,
        classify_primary_category,
        extract_paragraphs_from_docx,
    )
    from scripts.retrieve_maymei_samples import overlap_score
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.build_article_corpus_index import (
        classify_formula,
        classify_primary_category,
        extract_paragraphs_from_docx,
    )
    from scripts.retrieve_maymei_samples import overlap_score


AI_TONE_PATTERNS = (
    re.compile(r"不是[^。\n]{0,50}而是"),
    re.compile(r"不要[^。\n]{0,50}而是"),
    re.compile(r"不只是[^。\n]{0,50}更是"),
)
FACT_MARKERS = (
    "官方",
    "Steam",
    "版本",
    "平台",
    "發售",
    "上市",
    "支援",
    "確認",
    "公布",
    "新增",
    "包含",
)
JUDGMENT_MARKERS = (
    "我覺得",
    "我會",
    "我推薦",
    "我最推薦",
    "建議",
    "先等",
    "很香",
    "很尷尬",
    "值得",
    "不值得",
    "適合",
    "不適合",
    "先不要",
)
REPORT_TONE_MARKERS = (
    "值得一提的是",
    "另外值得一提的是",
    "目前看起來",
    "目前整理",
    "根據",
    "資料顯示",
)
PLAYER_MARKERS = (
    "新手",
    "玩家",
    "老玩家",
    "買之前",
    "入坑",
    "少走",
    "省時間",
    "卡",
    "後悔",
    "首日",
    "長玩",
)
OPENING_MARKERS = ("大家好", "這部影片", "我這次", "今天")
ENDING_MARKERS = ("以上就是", "那影片就到這邊", "大家掰掰", "歡迎訂閱")


@dataclass
class WritingSample:
    sample_id: str
    title: str
    source_path: str
    primary_category: str
    formula: str
    char_count: int
    paragraph_count: int
    trust_level: str
    priority: int
    opening: list[str]
    chapter_heads: list[str]
    judgment_lines: list[str]
    player_lines: list[str]
    ai_tone_hits: list[str]


@dataclass
class TransformPair:
    sample_id: str
    title: str
    formula: str
    source_path: str
    fact_line: str
    maymei_line: str
    transformation: str


def normalize_line(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def split_units(paragraphs: list[str]) -> list[str]:
    units: list[str] = []
    for paragraph in paragraphs:
        clean = normalize_line(paragraph)
        if not clean:
            continue
        parts = re.split(r"(?<=[。！？!?])\s*", clean)
        units.extend(part.strip() for part in parts if part.strip())
    return units


def looks_like_heading(line: str) -> bool:
    clean = normalize_line(line)
    if len(clean) > 38:
        return False
    return bool(
        re.match(r"^(第[一二三四五六七八九十]+|0?\d+|[一二三四五六七八九十]+[、.])", clean)
        or any(marker in clean for marker in ("系統", "地圖", "版本", "結語", "總結", "開場", "前言", "攻略"))
    )


def has_ai_tone(line: str) -> bool:
    return any(pattern.search(line) for pattern in AI_TONE_PATTERNS)


def has_report_tone(line: str) -> bool:
    return any(marker in line for marker in REPORT_TONE_MARKERS)


def is_fact_line(line: str) -> bool:
    return bool(
        re.search(r"\d|%|X\|S|PC|PS5|Switch|Steam|Game Pass", line)
        or any(marker in line for marker in FACT_MARKERS)
    )


def is_judgment_line(line: str) -> bool:
    return any(marker in line for marker in JUDGMENT_MARKERS) and not has_report_tone(line)


def is_player_line(line: str) -> bool:
    return any(marker in line for marker in PLAYER_MARKERS)


def cap(items: list[str], limit: int = 8, max_chars: int = 120) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        clean = normalize_line(item)
        if not clean or clean in seen:
            continue
        seen.add(clean)
        output.append(clean[:max_chars])
        if len(output) >= limit:
            break
    return output


def sample_id_for(path: Path) -> str:
    return re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", path.stem).strip("-")[:80]


def title_from_path(path: Path) -> str:
    stem = re.sub(r"^\d+\s*-\s*", "", path.stem)
    return normalize_line(stem.replace("_", ":"))


def classify_writing_formula(title: str) -> str:
    if re.search(r"(買之前|買前|玩之前|入坑|值得買)", title, re.IGNORECASE):
        return "買前必看"
    return classify_formula(title)


def trust_for_path(path: Path) -> tuple[str, int]:
    text = str(path).replace("\\", "/")
    if "high-precision-clean" in text:
        return "curated-google-export", 90
    if "google-docs-export" in text:
        return "google-docs-export", 70
    return "local-docx", 80


def build_sample_from_docx(path: Path) -> tuple[WritingSample | None, list[TransformPair]]:
    try:
        paragraphs = extract_paragraphs_from_docx(path)
    except Exception:
        return None, []
    paragraphs = [normalize_line(paragraph) for paragraph in paragraphs if normalize_line(paragraph)]
    if len(paragraphs) < 5:
        return None, []
    body = "\n".join(paragraphs)
    if "大家好" not in body and len(body) < 800:
        return None, []

    first = paragraphs[0] if paragraphs else ""
    title = title_from_path(path) if first.startswith(("大家好", "前言")) else first
    formula = classify_writing_formula(title)
    primary_category = classify_primary_category(title)
    units = split_units(paragraphs)
    trust_level, priority = trust_for_path(path)
    sample_id = sample_id_for(path)

    sample = WritingSample(
        sample_id=sample_id,
        title=title[:160],
        source_path=str(path),
        primary_category=primary_category,
        formula=formula,
        char_count=len(body),
        paragraph_count=len(paragraphs),
        trust_level=trust_level,
        priority=priority,
        opening=cap([unit for unit in units[:10] if any(marker in unit for marker in OPENING_MARKERS)], limit=4),
        chapter_heads=cap([paragraph for paragraph in paragraphs if looks_like_heading(paragraph)], limit=10),
        judgment_lines=cap([unit for unit in units if is_judgment_line(unit) and not has_ai_tone(unit)], limit=10),
        player_lines=cap([unit for unit in units if is_player_line(unit)], limit=10),
        ai_tone_hits=cap([unit for unit in units if has_ai_tone(unit)], limit=10),
    )
    return sample, extract_transform_pairs(sample, units)


def infer_transformation(fact_line: str, maymei_line: str) -> str:
    if any(marker in maymei_line for marker in ("我推薦", "我會", "建議", "先等")):
        return "把資料條件轉成購買或行動建議。"
    if any(marker in maymei_line for marker in ("適合", "不適合", "玩家")):
        return "把功能資訊轉成適合族群。"
    if any(marker in maymei_line for marker in ("省時間", "少走", "不用", "後悔")):
        return "把機制翻成玩家收益或避坑。"
    return "把事實資訊轉成中文口播判斷。"


def extract_transform_pairs(sample: WritingSample, units: list[str]) -> list[TransformPair]:
    pairs: list[TransformPair] = []
    for index, line in enumerate(units[:-1]):
        next_line = units[index + 1]
        if not is_fact_line(line):
            continue
        if not (is_judgment_line(next_line) or is_player_line(next_line)):
            continue
        if has_ai_tone(next_line):
            continue
        pairs.append(
            TransformPair(
                sample_id=sample.sample_id,
                title=sample.title,
                formula=sample.formula,
                source_path=sample.source_path,
                fact_line=line[:180],
                maymei_line=next_line[:180],
                transformation=infer_transformation(line, next_line),
            )
        )
        if len(pairs) >= 6:
            break
    return pairs


def iter_docx_files(source_dirs: list[Path]) -> list[Path]:
    files: list[Path] = []
    for source_dir in source_dirs:
        if source_dir.is_file() and source_dir.suffix.lower() == ".docx":
            files.append(source_dir)
        elif source_dir.exists():
            files.extend(sorted(source_dir.rglob("*.docx")))
    return files


def build_writing_system(
    source_dirs: list[Path],
    *,
    max_samples: int = 240,
    topic: str = "",
    formula: str = "",
) -> dict[str, Any]:
    samples: list[WritingSample] = []
    pairs: list[TransformPair] = []
    for path in iter_docx_files(source_dirs):
        built_sample, built_pairs = build_sample_from_docx(path)
        if not built_sample:
            continue
        samples.append(built_sample)
        pairs.extend(built_pairs)

    samples.sort(
        key=lambda item: (
            item.priority,
            1.0 if formula and item.formula == formula else 0.0,
            overlap_score(topic, item.title) if topic else 0.0,
            item.char_count,
        ),
        reverse=True,
    )
    samples = samples[:max_samples]
    selected_ids = {sample.sample_id for sample in samples}
    pairs = [pair for pair in pairs if pair.sample_id in selected_ids]

    cards = build_decision_cards(samples)
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "source_dirs": [str(path) for path in source_dirs],
        "total_samples": len(samples),
        "total_transform_pairs": len(pairs),
        "samples": [asdict(sample) for sample in samples],
        "transform_pairs": [asdict(pair) for pair in pairs],
        "decision_cards": cards,
        "runtime_workflow": [
            "先從攻略研究包鎖定已確認事實、不可講死、玩家問題。",
            "依片型檢索 3 到 5 篇同類中文樣本。",
            "先寫每章 chapter card：玩家問題、玫玫判斷、可用事實、玩家翻譯、禁用句型。",
            "逐章生成可念稿，不一次爆整篇。",
            "AI 人工審稿逐句判斷：資料腔、英文翻譯腔、沒有立場、缺玩家情境都要二修。",
            "最後才跑機械檢查作保底。",
        ],
    }


def build_decision_cards(samples: list[WritingSample]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[WritingSample]] = defaultdict(list)
    for sample in samples:
        grouped[sample.formula].append(sample)

    cards: dict[str, dict[str, Any]] = {}
    for formula, items in sorted(grouped.items()):
        category_counts = Counter(item.primary_category for item in items)
        chapter_heads = Counter(head for item in items for head in item.chapter_heads)
        judgment_openers = Counter(first_clause(line) for item in items for line in item.judgment_lines)
        player_patterns = Counter(first_clause(line) for item in items for line in item.player_lines)
        ai_hits = sum(len(item.ai_tone_hits) for item in items)
        cards[formula] = {
            "formula": formula,
            "sample_count": len(items),
            "primary_categories": dict(category_counts.most_common()),
            "chapter_entry_patterns": [value for value, _ in chapter_heads.most_common(8)],
            "judgment_patterns": [value for value, _ in judgment_openers.most_common(8)],
            "player_alignment_patterns": [value for value, _ in player_patterns.most_common(8)],
            "drafting_directives": directives_for_formula(formula),
            "ai_tone_risk_count": ai_hits,
            "must_not": [
                "不要用英文 buyer guide 順序硬套中文稿。",
                "不要用 `不是...而是...`、`不要...而是...` 當主要轉折。",
                "不要只列官方功能；每章都要收成玩家該怎麼判斷。",
                "不要一次生成整篇；逐章寫，逐章審。",
            ],
        }
    return cards


def first_clause(line: str) -> str:
    clean = normalize_line(line)
    for sep in ("，", "。", "：", "；"):
        if sep in clean:
            return clean.split(sep, 1)[0][:60]
    return clean[:60]


def directives_for_formula(formula: str) -> list[str]:
    if "新手" in formula:
        return [
            "第一段先讓新手知道不先懂會卡哪裡。",
            "每章給現成做法，再補原因和例外。",
            "多用前期、少走彎路、先做、先不要這類玩家決策語。",
        ]
    if "買" in formula or "推薦" in formula:
        return [
            "先講玩家猶豫點，再講值得期待和要觀望的地方。",
            "平台、版本、價格放後段，前段先講遊戲本體吸引力。",
            "每章最後給適合誰、誰要等、誰可以先買的判斷。",
        ]
    if "效率" in formula or "刷" in formula:
        return [
            "先丟收益或效率差，再講前置條件。",
            "把路線、時間、收益寫成玩家能照做的口播。",
            "補失敗條件和替代方案，避免只像數據表。",
        ]
    if "排行" in formula or "top" in formula.lower():
        return [
            "先交代排名標準，不要只喊最強。",
            "每一名都要有一句記憶點和一句玩家對位。",
            "主觀排序要敢講理由，不要假裝完全客觀。",
        ]
    return [
        "先講觀眾現在最需要知道的判斷。",
        "事實只當材料，正文要轉成玩家情境。",
        "每 2 到 4 段補一次自己的推薦或提醒。",
    ]


def render_markdown(system: dict[str, Any]) -> str:
    lines = [
        "# Maymei Chinese Writing System",
        "",
        "## Purpose",
        "把既有中文文稿轉成可執行的寫作決策系統，而不是只把樣本當 few-shot。",
        "",
        "## Runtime Workflow",
    ]
    lines.extend(f"{index}. {step}" for index, step in enumerate(system["runtime_workflow"], 1))
    lines.extend(
        [
            "",
            "## Corpus Summary",
            f"- Samples: `{system['total_samples']}`",
            f"- Transform pairs: `{system['total_transform_pairs']}`",
            "",
            "## Decision Cards",
        ]
    )
    for formula, card in system["decision_cards"].items():
        lines.extend(["", f"### {formula}", f"- Sample count: `{card['sample_count']}`"])
        lines.append("- Drafting directives:")
        lines.extend(f"  - {item}" for item in card["drafting_directives"])
        if card["judgment_patterns"]:
            lines.append("- Judgment patterns:")
            lines.extend(f"  - {item}" for item in card["judgment_patterns"][:5])
        if card["must_not"]:
            lines.append("- Must not:")
            lines.extend(f"  - {item}" for item in card["must_not"])
    lines.append("")
    return "\n".join(lines)


def write_outputs(system: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "maymei-writing-system.json").write_text(
        json.dumps(system, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "maymei-writing-system.md").write_text(render_markdown(system), encoding="utf-8")
    with (output_dir / "maymei-writing-samples.jsonl").open("w", encoding="utf-8") as handle:
        for sample in system["samples"]:
            handle.write(json.dumps(sample, ensure_ascii=False) + "\n")
    with (output_dir / "maymei-line-transform-pairs.jsonl").open("w", encoding="utf-8") as handle:
        for pair in system["transform_pairs"]:
            handle.write(json.dumps(pair, ensure_ascii=False) + "\n")


def parse_args(argv: list[str]) -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    default_sources = [
        repo_root
        / "workspace"
        / "source-docs"
        / "google-maymei-yt-scripts-high-precision-clean-2026-03-31",
        repo_root / "workspace" / "source-docs" / "google-docs-export-2026-03-30" / "docs",
    ]
    parser = argparse.ArgumentParser(description="Build Maymei Chinese writing decision system from DOCX samples.")
    parser.add_argument("--source-dir", action="append", default=[str(path) for path in default_sources])
    parser.add_argument(
        "--output-dir",
        default=str(repo_root / "workspace" / "memory" / "style-corpus"),
    )
    parser.add_argument("--max-samples", type=int, default=240)
    parser.add_argument("--topic", default="")
    parser.add_argument("--formula", default="")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    system = build_writing_system(
        [Path(value) for value in args.source_dir],
        max_samples=args.max_samples,
        topic=args.topic,
        formula=args.formula,
    )
    write_outputs(system, Path(args.output_dir))
    print(
        "Built Maymei writing system: "
        f"{system['total_samples']} samples, {system['total_transform_pairs']} transform pairs"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
