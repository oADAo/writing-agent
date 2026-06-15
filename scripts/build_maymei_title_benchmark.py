from __future__ import annotations

import argparse
import csv
import io
import json
import statistics
import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable
from zipfile import ZipFile

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.build_article_corpus_index import classify_formula, classify_primary_category
from scripts.build_maymei_golden_samples import infer_game_name


REQUIRED_TABLE_COLUMNS = {
    "內容",
    "影片標題",
    "影片發布時間",
    "時間長度",
    "觀看次數",
    "觀看時間 (小時)",
    "平均觀看時間",
    "平均觀看比例 (%)",
    "曝光次數",
    "曝光點閱率 (%)",
}

NUMERIC_COLUMNS = {
    "互動觀看次數": "interactive_views",
    "平均觀看比例 (%)": "avg_view_percent",
    "續看觀眾比率 (%)": "returning_viewer_percent",
    "獲得的訂閱人數": "subscribers_gained",
    "流失的訂閱人數": "subscribers_lost",
    "喜歡次數": "like_count",
    "不喜歡次數": "dislike_count",
    "分享次數": "share_count",
    "已新增留言": "comment_count",
    "觀看次數": "view_count",
    "觀看時間 (小時)": "watch_hours",
    "訂閱人數": "subscriber_delta",
    "曝光次數": "impressions",
    "曝光點閱率 (%)": "ctr_percent",
}


def parse_number(value: str | None) -> float | None:
    text = str(value or "").strip().replace(",", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def parse_int(value: str | None) -> int | None:
    parsed = parse_number(value)
    if parsed is None:
        return None
    return int(round(parsed))


def parse_publish_date(value: str | None) -> str | None:
    text = str(value or "").strip()
    if not text:
        return None
    for pattern in ("%b %d, %Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, pattern).date().isoformat()
        except ValueError:
            continue
    return None


def parse_duration_seconds(value: str | None) -> int | None:
    text = str(value or "").strip()
    if not text:
        return None
    if ":" not in text:
        return parse_int(text)
    parts = text.split(":")
    if not all(part.strip().isdigit() for part in parts):
        return None
    numbers = [int(part) for part in parts]
    if len(numbers) == 2:
        minutes, seconds = numbers
        return minutes * 60 + seconds
    if len(numbers) == 3:
        hours, minutes, seconds = numbers
        return hours * 3600 + minutes * 60 + seconds
    return None


def safe_divide(numerator: float | int | None, denominator: float | int | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return float(numerator) / float(denominator)


def iter_csv_texts(source: Path) -> Iterable[tuple[str, str]]:
    if source.is_dir():
        for path in sorted(source.glob("*.csv")):
            yield path.name, path.read_text(encoding="utf-8-sig")
        return

    if source.suffix.lower() == ".zip":
        with ZipFile(source) as archive:
            for name in sorted(archive.namelist()):
                if name.lower().endswith(".csv"):
                    yield Path(name).name, archive.read(name).decode("utf-8-sig")
        return

    yield source.name, source.read_text(encoding="utf-8-sig")


def read_csv_records(csv_text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(csv_text)))


def find_studio_table(source: Path) -> tuple[str, list[dict[str, str]]]:
    for name, text in iter_csv_texts(source):
        records = read_csv_records(text)
        if not records:
            continue
        columns = set(records[0].keys())
        if REQUIRED_TABLE_COLUMNS.issubset(columns):
            return name, records
    required = ", ".join(sorted(REQUIRED_TABLE_COLUMNS))
    raise ValueError(f"Could not find YouTube Studio content table with columns: {required}")


def build_record(
    row: dict[str, str],
    *,
    row_number: int,
    shorts_max_duration_seconds: int,
) -> dict[str, Any]:
    raw_video_id = str(row.get("內容") or "")
    video_id = raw_video_id.strip()
    title = str(row.get("影片標題") or "").strip()
    duration_seconds = parse_duration_seconds(row.get("時間長度"))
    published_at = parse_publish_date(row.get("影片發布時間"))
    avg_view_duration_seconds = parse_duration_seconds(row.get("平均觀看時間"))
    flags: list[str] = []

    if raw_video_id != video_id:
        flags.append("trimmed_video_id")
    if not published_at:
        flags.append("missing_published_at")

    metrics: dict[str, float | int | None] = {}
    for source_column, target_key in NUMERIC_COLUMNS.items():
        value = parse_number(row.get(source_column))
        if target_key.endswith("_count") or target_key in {
            "interactive_views",
            "subscribers_gained",
            "subscribers_lost",
            "view_count",
            "subscriber_delta",
            "impressions",
        }:
            metrics[target_key] = int(round(value)) if value is not None else None
        else:
            metrics[target_key] = value

    view_count = metrics.get("view_count")
    impressions = metrics.get("impressions")
    ctr_percent = metrics.get("ctr_percent")

    if impressions in (None, 0):
        flags.append("missing_or_zero_impressions")
    if ctr_percent is None:
        flags.append("missing_ctr")

    like_count = metrics.get("like_count")
    comment_count = metrics.get("comment_count")
    share_count = metrics.get("share_count")
    engagement_count = sum(
        value for value in (like_count, comment_count, share_count) if isinstance(value, int)
    )

    record = {
        "source_row_number": row_number,
        "video_id": video_id,
        "title": title,
        "published_at": published_at,
        "duration_seconds": duration_seconds,
        "format": "short" if duration_seconds is not None and duration_seconds <= shorts_max_duration_seconds else "long",
        "game": infer_game_name(title),
        "primary_category": classify_primary_category(title),
        "formula": classify_formula(title),
        **metrics,
        "avg_view_duration_seconds": avg_view_duration_seconds,
        "views_per_impression": safe_divide(view_count, impressions),
        "engagement_rate": safe_divide(engagement_count, view_count),
        "subscriber_conversion_rate": safe_divide(metrics.get("subscribers_gained"), view_count),
        "data_quality_flags": flags,
    }
    return record


def median(values: list[float | int]) -> float | int | None:
    clean_values = [value for value in values if value is not None]
    if not clean_values:
        return None
    result = statistics.median(clean_values)
    return round(result, 4) if isinstance(result, float) else result


def build_formula_benchmarks(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        if record.get("format") == "long":
            grouped[str(record.get("formula") or "一般攻略")].append(record)

    benchmarks: list[dict[str, Any]] = []
    for formula, formula_records in grouped.items():
        top_by_ctr = max(
            formula_records,
            key=lambda record: (
                record.get("ctr_percent") or 0,
                record.get("impressions") or 0,
            ),
        )
        benchmarks.append(
            {
                "formula": formula,
                "count": len(formula_records),
                "median_ctr_percent": median(
                    [record.get("ctr_percent") for record in formula_records if record.get("ctr_percent") is not None]
                ),
                "median_views": median(
                    [record.get("view_count") for record in formula_records if record.get("view_count") is not None]
                ),
                "total_impressions": int(
                    sum(record.get("impressions") or 0 for record in formula_records)
                ),
                "top_ctr_title": top_by_ctr.get("title"),
                "top_ctr_percent": top_by_ctr.get("ctr_percent"),
            }
        )
    return sorted(benchmarks, key=lambda item: (item["count"], item["total_impressions"]), reverse=True)


def build_summary(records: list[dict[str, Any]], *, table_file: str) -> dict[str, Any]:
    long_records = [record for record in records if record.get("format") == "long"]
    short_records = [record for record in records if record.get("format") == "short"]
    published_dates = [record["published_at"] for record in records if record.get("published_at")]
    quality_counter = Counter(
        flag for record in records for flag in record.get("data_quality_flags", [])
    )
    return {
        "table_file": table_file,
        "total_videos": len(records),
        "long_videos": len(long_records),
        "short_videos": len(short_records),
        "trimmed_video_ids": quality_counter.get("trimmed_video_id", 0),
        "missing_ctr_rows": quality_counter.get("missing_ctr", 0),
        "missing_or_zero_impressions_rows": quality_counter.get("missing_or_zero_impressions", 0),
        "release_date_min": min(published_dates) if published_dates else None,
        "release_date_max": max(published_dates) if published_dates else None,
        "long_total_views": int(sum(record.get("view_count") or 0 for record in long_records)),
        "long_total_impressions": int(sum(record.get("impressions") or 0 for record in long_records)),
        "short_total_views": int(sum(record.get("view_count") or 0 for record in short_records)),
        "short_total_impressions": int(sum(record.get("impressions") or 0 for record in short_records)),
        "quality_flags": dict(sorted(quality_counter.items())),
    }


def build_dataset(
    source: Path | str,
    *,
    generated_at: str | None = None,
    shorts_max_duration_seconds: int = 60,
) -> dict[str, Any]:
    source_path = Path(source)
    table_file, rows = find_studio_table(source_path)
    records: list[dict[str, Any]] = []
    for row_number, row in enumerate(rows, start=2):
        video_id = str(row.get("內容") or "").strip()
        if video_id == "總計":
            continue
        if not video_id:
            continue
        records.append(
            build_record(
                row,
                row_number=row_number,
                shorts_max_duration_seconds=shorts_max_duration_seconds,
            )
        )

    timestamp = generated_at or datetime.now(UTC).isoformat()
    return {
        "source": str(source_path),
        "generated_at": timestamp,
        "shorts_max_duration_seconds": shorts_max_duration_seconds,
        "summary": build_summary(records, table_file=table_file),
        "formula_benchmarks": build_formula_benchmarks(records),
        "records": records,
    }


def format_number(value: Any) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, float):
        return f"{value:,.2f}"
    if isinstance(value, int):
        return f"{value:,}"
    return str(value)


def render_markdown(dataset: dict[str, Any], *, min_impressions: int = 100_000) -> str:
    summary = dataset["summary"]
    records = dataset["records"]
    long_records = [record for record in records if record.get("format") == "long"]
    top_ctr = sorted(
        [
            record
            for record in long_records
            if (record.get("impressions") or 0) >= min_impressions and record.get("ctr_percent") is not None
        ],
        key=lambda record: (record.get("ctr_percent") or 0, record.get("impressions") or 0),
        reverse=True,
    )[:15]

    lines = [
        "# Maymei Title Benchmark",
        "",
        "## Source",
        f"- Source: `{dataset['source']}`",
        f"- Table file: `{summary['table_file']}`",
        f"- Generated at: `{dataset['generated_at']}`",
        "- Privacy note: revenue fields are intentionally excluded from this title dataset.",
        "",
        "## Coverage",
        f"- Total videos: `{summary['total_videos']}`",
        f"- Long videos: `{summary['long_videos']}`",
        f"- Shorts / short-form rows: `{summary['short_videos']}`",
        f"- Release date range: `{summary['release_date_min']}` to `{summary['release_date_max']}`",
        f"- Long video impressions: `{format_number(summary['long_total_impressions'])}`",
        f"- Long video views: `{format_number(summary['long_total_views'])}`",
        "",
        "## Data Quality",
        f"- Trimmed video IDs: `{summary['trimmed_video_ids']}`",
        f"- Missing CTR rows: `{summary['missing_ctr_rows']}`",
        f"- Missing / zero impression rows: `{summary['missing_or_zero_impressions_rows']}`",
        "",
        "## Formula Benchmarks",
    ]

    for item in dataset.get("formula_benchmarks", []):
        lines.append(
            "- "
            f"公式：`{item['formula']}` | "
            f"樣本：`{item['count']}` | "
            f"CTR 中位數：`{format_number(item['median_ctr_percent'])}%` | "
            f"觀看中位數：`{format_number(item['median_views'])}` | "
            f"最高 CTR 標題：{item['top_ctr_title']}"
        )

    lines.extend(["", f"## Top CTR Long Videos (>= {format_number(min_impressions)} impressions)"])
    for record in top_ctr:
        lines.extend(
            [
                "",
                f"### {record['title']}",
                f"- Video ID: `{record['video_id']}`",
                f"- 公式：`{record['formula']}`",
                f"- 遊戲：`{record['game'] or '未判定'}`",
                f"- CTR: `{format_number(record['ctr_percent'])}%`",
                f"- Impressions: `{format_number(record['impressions'])}`",
                f"- Views: `{format_number(record['view_count'])}`",
                f"- Avg view duration: `{format_number(record['avg_view_duration_seconds'])}s`",
            ]
        )

    lines.append("")
    return "\n".join(lines)


def write_outputs(dataset: dict[str, Any], json_output: Path, markdown_output: Path) -> None:
    json_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(dataset, ensure_ascii=False, indent=2), encoding="utf-8")
    markdown_output.write_text(render_markdown(dataset), encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    default_json = repo_root / "workspace" / "memory" / "style-corpus" / "maymei-title-benchmark.json"
    default_markdown = repo_root / "workspace" / "memory" / "style-corpus" / "maymei-title-benchmark.md"
    parser = argparse.ArgumentParser(
        description="Build a sanitized title benchmark dataset from a YouTube Studio content export."
    )
    parser.add_argument("source", help="YouTube Studio CSV, directory of CSVs, or ZIP export.")
    parser.add_argument("--json-output", default=str(default_json))
    parser.add_argument("--markdown-output", default=str(default_markdown))
    parser.add_argument("--shorts-max-duration-seconds", type=int, default=60)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    dataset = build_dataset(
        Path(args.source),
        shorts_max_duration_seconds=args.shorts_max_duration_seconds,
    )
    write_outputs(dataset, Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
