from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    from scripts.build_article_corpus_index import extract_paragraphs_from_docx
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.build_article_corpus_index import extract_paragraphs_from_docx


MAYMEI_MARKERS = (
    "我推薦",
    "我會",
    "我自己",
    "最推薦",
    "直接",
    "真的",
    "超",
    "新手",
    "省時間",
    "不用",
    "少走",
    "輕鬆",
    "無腦",
    "必看",
)
TRANSITION_PREFIXES = ("第一", "第二", "第三", "第四", "第五", "接著", "另外", "不過", "最後", "如果", "所以")
DATA_RE = re.compile(r"\d+|%|等級|傷害|素材|位置|機制|數值")


def split_text_units(text: str) -> list[str]:
    units: list[str] = []
    for paragraph in text.splitlines():
        clean = paragraph.strip()
        if not clean:
            continue
        parts = re.split(r"(?<=[。！？!?])\s*", clean)
        units.extend(part.strip() for part in parts if part.strip())
    return units


def cap_lines(lines: list[str], *, limit: int = 5, max_chars: int = 120) -> list[str]:
    return [line[:max_chars] for line in lines[:limit]]


def infer_opening_pattern(units: list[str], title: str) -> str:
    first_content = next((unit for unit in units if "大家好" not in unit and "玫玫物語" not in unit), title)
    if "如果" in first_content:
        return "以玩家情境開場，先點出觀眾正在猶豫或會遇到的問題。"
    if any(marker in first_content for marker in ("必看", "推薦", "最", "直接")):
        return "以明確 promise 開場，先告訴觀眾看完能省時間或變強。"
    return "以題目 promise 開場，接著快速進入攻略價值。"


def infer_information_order(units: list[str], formula: str) -> list[str]:
    order = ["開場 promise", "玩家痛點或使用情境"]
    if "新手" in formula:
        order.extend(["前期最容易卡住的原因", "逐點給可操作技巧", "提醒資源或時間成本"])
    elif "效率" in formula:
        order.extend(["先講收益", "講前置條件", "拆步驟", "補省時間細節"])
    elif "排行" in formula or "top" in formula.lower():
        order.extend(["先定排名標準", "每名給理由", "補適合玩家", "收斂推薦"])
    elif "build" in formula or "流派" in formula:
        order.extend(["先講成形效果", "拆核心零件", "講操作方式", "補缺點與替代"])
    else:
        order.extend(["先講重點", "拆機制或路線", "補風險與例外"])
    if any(unit.startswith("最後") for unit in units):
        order.append("最後收斂成具體建議")
    return order


def analyze_style_text(text: str, *, title: str = "", formula: str = "一般攻略") -> dict[str, Any]:
    units = split_text_units(text)
    maymei_like = [
        unit
        for unit in units
        if any(marker in unit for marker in MAYMEI_MARKERS) or ("我" in unit and ("建議" in unit or "推薦" in unit))
    ]
    data_only = [
        unit
        for unit in units
        if DATA_RE.search(unit) and not any(marker in unit for marker in MAYMEI_MARKERS) and "我" not in unit
    ]
    transitions = [unit for unit in units if unit.startswith(TRANSITION_PREFIXES)]
    first_person = [unit for unit in units if "我" in unit or "自己" in unit or "實測" in unit]
    player_alignment = [
        unit for unit in units if any(marker in unit for marker in ("新手", "省", "不用", "少走", "後悔", "卡", "變強"))
    ]
    lengths = [len(unit) for unit in units] or [0]
    average_length = sum(lengths) / len(lengths)

    return {
        "title": title,
        "formula": formula,
        "opening_promise_pattern": infer_opening_pattern(units, title),
        "first_person_experience": cap_lines(first_person),
        "emotional_player_alignment": cap_lines(player_alignment),
        "sentence_rhythm": {
            "unit_count": len(units),
            "average_chars": round(average_length, 1),
            "short_units": sum(1 for length in lengths if length <= 22),
            "long_units": sum(1 for length in lengths if length >= 55),
        },
        "transitions": cap_lines(transitions),
        "information_order": infer_information_order(units, formula),
        "maymei_like_lines": cap_lines(maymei_like),
        "data_only_lines": cap_lines(data_only),
        "learnable_structure": [
            "先把玩家會得到的好處講清楚，再補條件和步驟。",
            "每個段落都要有判斷語氣，不只列資料。",
            "把機制翻成省時間、少走路、變強、少踩雷這類玩家體感。",
        ],
        "do_not_copy": [
            "不要照抄樣本句子，只學 promise、轉場、段落節奏。",
            "不要把舊遊戲事實帶到新攻略。",
            "不要平均混合所有樣本；先套同類型公式卡。",
        ],
    }


def read_source_text(record: dict[str, Any]) -> str:
    if record.get("text"):
        return str(record["text"])
    source = Path(str(record.get("source_doc") or record.get("source_path") or ""))
    if source.exists() and source.suffix.lower() == ".docx":
        return "\n".join(extract_paragraphs_from_docx(source))
    parts = [
        str(record.get("title") or ""),
        str(record.get("opening_promise") or ""),
        str(record.get("intro_line") or ""),
    ]
    return "\n".join(part for part in parts if part)


def analyze_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    analyzed: list[dict[str, Any]] = []
    for record in records:
        text = read_source_text(record)
        analysis = analyze_style_text(
            text,
            title=str(record.get("title") or record.get("source_title") or ""),
            formula=str(record.get("formula") or "一般攻略"),
        )
        analyzed.append({**record, "style_forensics": analysis})
    return analyzed


def parse_args(argv: list[str]) -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Analyze Maymei golden samples into style forensics.")
    parser.add_argument(
        "--golden-samples",
        default=str(repo_root / "workspace" / "memory" / "style-corpus" / "maymei-golden-samples.json"),
    )
    parser.add_argument(
        "--output",
        default=str(repo_root / "workspace" / "memory" / "style-corpus" / "maymei-style-forensics.json"),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    payload = json.loads(Path(args.golden_samples).read_text(encoding="utf-8"))
    records = payload.get("records", []) if isinstance(payload, dict) else payload
    analyzed = analyze_records([item for item in records if isinstance(item, dict)])
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"total": len(analyzed), "records": analyzed}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(analyzed)} style forensics records to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
