from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, UTC
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET
from zipfile import ZipFile


DOCX_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

PRIMARY_CATEGORY_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("推薦清單", (r"推薦", r"必玩大作", r"最新遊戲", r"大作")),
    ("配裝流派", (r"流派", r"配點", r"裝備推薦")),
    ("資源效率", (r"刷錢", r"刷等", r"掛機", r"效率", r"農")),
    (
        "完整攻略",
        (
            r"完全攻略",
            r"詳細攻略",
            r"神廟攻略",
            r"解法攻略",
            r"支線.*攻略",
            r"隱藏.*攻略",
            r"機制詳細解說",
            r"神殿",
        ),
    ),
    ("排行精選", (r"top\s*\d+", r"排名", r"最難", r"最強boss", r"武器", r"稀有")),
    ("新手開局", (r"新手", r"開局", r"第一天")),
    (
        "完整攻略",
        (r"攻略", r"技巧", r"解說", r"機制", r"神殿", r"支線", r"boss", r"血月"),
    ),
]

FORMULA_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("第一天必做", (r"第一天",)),
    ("推薦清單", (r"推薦", r"必玩", r"大作")),
    ("效率刷法", (r"刷錢", r"刷等", r"掛機")),
    ("流派 build", (r"流派", r"配點", r"裝備推薦")),
    ("排行 top list", (r"top\s*\d+", r"排名", r"最難")),
    (
        "完整攻略",
        (
            r"完全攻略",
            r"詳細攻略",
            r"神廟攻略",
            r"解法攻略",
            r"支線.*攻略",
            r"隱藏.*攻略",
            r"鑰匙位置",
        ),
    ),
    ("新手技巧清單", (r"新手", r"開局")),
    ("技巧教學", (r"技巧",)),
    ("機制拆解", (r"機制", r"詳細解說", r"血月")),
]

VOICE_MARKERS = (
    "大家好",
    "這部影片要來",
    "我推薦",
    "最推薦",
    "前期",
    "少走彎路",
    "輕鬆",
    "效率",
    "直接",
)

SKIP_PARAGRAPHS = {
    "前言",
    "影片介紹:",
    "影片介紹",
    "遊戲攻略",
}

SKIP_PREFIXES = (
    "以下為將原字幕內容完整改寫",
)


@dataclass
class ArticleRecord:
    source_path: str
    source_file: str
    title: str
    primary_category: str
    formula: str
    char_count: int
    paragraph_count: int
    opening_promise: str
    voice_markers: list[str]


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_paragraphs_from_docx(path: Path) -> list[str]:
    with ZipFile(path) as archive:
        xml = archive.read("word/document.xml")

    root = ET.fromstring(xml)
    paragraphs: list[str] = []
    for paragraph in root.findall(".//w:p", DOCX_NS):
        chunks = [node.text or "" for node in paragraph.findall(".//w:t", DOCX_NS)]
        text = normalize_text("".join(chunks))
        if text:
            paragraphs.append(text)
    return paragraphs


def matches_any(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def classify_primary_category(title: str) -> str:
    normalized = normalize_text(title)
    for category, patterns in PRIMARY_CATEGORY_RULES:
        if matches_any(normalized, patterns):
            return category
    return "完整攻略"


def classify_formula(title: str) -> str:
    normalized = normalize_text(title)
    for formula, patterns in FORMULA_RULES:
        if matches_any(normalized, patterns):
            return formula
    return "一般攻略"


def pick_opening_promise(paragraphs: list[str]) -> str:
    for paragraph in paragraphs[1:]:
        if paragraph in SKIP_PARAGRAPHS:
            continue
        if paragraph.startswith(SKIP_PREFIXES):
            continue
        if paragraph.startswith("大家好"):
            continue
        return paragraph[:180]
    return ""


def detect_voice_markers(paragraphs: list[str]) -> list[str]:
    combined = " ".join(paragraphs)
    return [marker for marker in VOICE_MARKERS if marker in combined]


def build_record(path: Path) -> ArticleRecord:
    paragraphs = extract_paragraphs_from_docx(path)
    title = paragraphs[0] if paragraphs else path.stem
    body = " ".join(paragraphs)
    return ArticleRecord(
        source_path=str(path),
        source_file=path.name,
        title=title,
        primary_category=classify_primary_category(title),
        formula=classify_formula(title),
        char_count=len(body),
        paragraph_count=len(paragraphs),
        opening_promise=pick_opening_promise(paragraphs),
        voice_markers=detect_voice_markers(paragraphs),
    )


def build_records(source_dir: Path) -> list[ArticleRecord]:
    files = sorted(source_dir.glob("*.docx"))
    return [build_record(path) for path in files]


def render_markdown(source_dir: Path, records: list[ArticleRecord]) -> str:
    counts = Counter(record.primary_category for record in records)
    grouped: dict[str, list[ArticleRecord]] = defaultdict(list)
    for record in records:
        grouped[record.primary_category].append(record)

    lines = [
        "# Local DOCX Corpus Index",
        "",
        "## Source",
        f"- Source directory: `{source_dir}`",
        f"- Total files: `{len(records)}`",
        f"- Generated at: `{datetime.now(UTC).isoformat()}`",
        "",
        "## Category Counts",
    ]

    for category, count in sorted(counts.items()):
        lines.append(f"- `{category}`: {count}")

    lines.extend(["", "## Entries"])
    for category in sorted(grouped):
        lines.extend(["", f"### {category}"])
        for record in grouped[category]:
            marker_summary = " / ".join(record.voice_markers) if record.voice_markers else "無"
            lines.extend(
                [
                    "",
                    f"#### {record.title}",
                    f"- Source file: `{record.source_file}`",
                    f"- Formula: `{record.formula}`",
                    f"- Approx chars: `{record.char_count}`",
                    f"- Paragraphs: `{record.paragraph_count}`",
                    f"- Voice markers: `{marker_summary}`",
                    f"- Opening promise: {record.opening_promise or '無'}",
                ]
            )

    lines.append("")
    return "\n".join(lines)


def write_outputs(
    source_dir: Path,
    records: list[ArticleRecord],
    markdown_output: Path,
    json_output: Path,
) -> None:
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.parent.mkdir(parents=True, exist_ok=True)

    markdown_output.write_text(render_markdown(source_dir, records), encoding="utf-8")
    payload = {
        "source_dir": str(source_dir),
        "generated_at": datetime.now(UTC).isoformat(),
        "total_files": len(records),
        "records": [asdict(record) for record in records],
    }
    json_output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    default_markdown = repo_root / "workspace" / "memory" / "style-corpus" / "local-docx-corpus.md"
    default_json = repo_root / "workspace" / "memory" / "style-corpus" / "local-docx-corpus.json"

    parser = argparse.ArgumentParser(
        description="Build a markdown and JSON index from a folder of DOCX article samples."
    )
    parser.add_argument("source_dir", help="Directory containing DOCX article samples.")
    parser.add_argument("--markdown-output", default=str(default_markdown))
    parser.add_argument("--json-output", default=str(default_json))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    source_dir = Path(args.source_dir)
    if not source_dir.exists():
        print(f"Source directory not found: {source_dir}")
        return 1

    records = build_records(source_dir)
    if not records:
        print(f"No DOCX files found in: {source_dir}")
        return 1

    write_outputs(
        source_dir=source_dir,
        records=records,
        markdown_output=Path(args.markdown_output),
        json_output=Path(args.json_output),
    )
    print(f"Indexed {len(records)} DOCX files from {source_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
