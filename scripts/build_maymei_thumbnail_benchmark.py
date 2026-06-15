from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.request
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable


DEFAULT_CHANNEL_URL = "https://www.youtube.com/@maymei_gaming/videos"


if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_json_lines(output: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in output.splitlines():
        raw = line.strip()
        if not raw:
            continue
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            records.append(parsed)
    return records


def fetch_channel_records(
    channel_url: str,
    *,
    limit: int,
    yt_dlp_args: list[str] | None = None,
) -> list[dict[str, Any]]:
    command = yt_dlp_args or [sys.executable, "-m", "yt_dlp"]
    completed = subprocess.run(
        [
            *command,
            "--flat-playlist",
            "--dump-json",
            "--playlist-end",
            str(limit),
            channel_url,
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if completed.returncode != 0:
        raise RuntimeError((completed.stderr or completed.stdout).strip())
    return parse_json_lines(completed.stdout)


def pick_best_thumbnail(thumbnails: Iterable[dict[str, Any]]) -> str:
    best_url = ""
    best_area = -1
    for item in thumbnails:
        url = str(item.get("url") or "").strip()
        if not url:
            continue
        width = int(float(item.get("width") or 0))
        height = int(float(item.get("height") or 0))
        area = width * height
        if area > best_area:
            best_url = url
            best_area = area
    return best_url


def canonical_thumbnail_url(video_id: str) -> str:
    return f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"


def fallback_thumbnail_url(video_id: str) -> str:
    return f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"


def download_thumbnail(video_id: str, url: str, thumbnail_dir: Path) -> tuple[str, bool]:
    thumbnail_dir.mkdir(parents=True, exist_ok=True)
    output_path = thumbnail_dir / f"{video_id}.jpg"
    urls = []
    if video_id:
        urls.append(canonical_thumbnail_url(video_id))
    urls.append(url)
    if video_id:
        urls.append(fallback_thumbnail_url(video_id))

    seen: set[str] = set()
    for candidate in urls:
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        try:
            request = urllib.request.Request(
                candidate,
                headers={"User-Agent": "Mozilla/5.0"},
            )
            with urllib.request.urlopen(request, timeout=20) as response:
                payload = response.read()
                if response.status >= 400 or len(payload) < 1024:
                    continue
                output_path.write_bytes(payload)
                return str(output_path), True
        except (OSError, urllib.error.URLError, urllib.error.HTTPError):
            continue
    return str(output_path), False


def extract_video_id(record: dict[str, Any]) -> str:
    return str(record.get("id") or record.get("display_id") or "").strip()


def title_benchmark_by_id(title_benchmark: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(record.get("video_id") or "").strip(): record
        for record in title_benchmark.get("records", [])
        if str(record.get("video_id") or "").strip()
    }


def normalize_thumbnail_annotations(raw_annotations: Any) -> dict[str, dict[str, Any]]:
    if isinstance(raw_annotations, dict) and isinstance(raw_annotations.get("records"), list):
        raw_records = raw_annotations["records"]
    elif isinstance(raw_annotations, dict):
        raw_records = [
            {"video_id": video_id, **annotation}
            for video_id, annotation in raw_annotations.items()
            if isinstance(annotation, dict)
        ]
    elif isinstance(raw_annotations, list):
        raw_records = raw_annotations
    else:
        raw_records = []

    annotations: dict[str, dict[str, Any]] = {}
    for record in raw_records:
        if not isinstance(record, dict):
            continue
        video_id = str(record.get("video_id") or "").strip()
        if not video_id:
            continue
        annotations[video_id] = record
    return annotations


def load_thumbnail_annotations(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    return normalize_thumbnail_annotations(load_json(path))


def build_record(
    channel_record: dict[str, Any],
    metric_record: dict[str, Any] | None,
    *,
    thumbnail_dir: Path,
    download: bool,
    annotations: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    video_id = extract_video_id(channel_record)
    title = str(channel_record.get("title") or "").strip()
    thumbnail_url = pick_best_thumbnail(channel_record.get("thumbnails") or [])
    if video_id:
        thumbnail_url = thumbnail_url or canonical_thumbnail_url(video_id)

    thumbnail_path = str(thumbnail_dir / f"{video_id}.jpg") if video_id else ""
    downloaded = False
    if download and video_id:
        thumbnail_path, downloaded = download_thumbnail(video_id, thumbnail_url, thumbnail_dir)

    metric_record = metric_record or {}
    duration = int(float(channel_record.get("duration") or metric_record.get("duration_seconds") or 0))
    inferred_format = "short" if duration and duration <= 60 else "long"
    resolved_format = metric_record.get("format") or inferred_format
    annotation = (annotations or {}).get(video_id, {})
    thumbnail_text = str(annotation.get("thumbnail_text") or "").strip()
    thumbnail_text_source = str(
        annotation.get("thumbnail_text_source")
        or ("manual_youtube_review" if thumbnail_text else "pending_manual_review")
    ).strip()
    thumbnail_notes = str(annotation.get("thumbnail_notes") or "").strip()

    return {
        "video_id": video_id,
        "title": metric_record.get("title") or title,
        "url": channel_record.get("webpage_url") or channel_record.get("url") or f"https://www.youtube.com/watch?v={video_id}",
        "format": resolved_format,
        "duration_seconds": metric_record.get("duration_seconds") or duration,
        "game": metric_record.get("game") or "",
        "formula": metric_record.get("formula") or "",
        "primary_category": metric_record.get("primary_category") or "",
        "ctr_percent": metric_record.get("ctr_percent"),
        "impressions": metric_record.get("impressions"),
        "view_count": metric_record.get("view_count"),
        "avg_view_percent": metric_record.get("avg_view_percent"),
        "thumbnail_url": thumbnail_url,
        "thumbnail_path": thumbnail_path,
        "thumbnail_downloaded": downloaded,
        "thumbnail_text": thumbnail_text,
        "thumbnail_text_source": thumbnail_text_source,
        "thumbnail_notes": thumbnail_notes,
        "matched_to_title_benchmark": bool(metric_record),
    }


def build_dataset(
    channel_records: list[dict[str, Any]],
    title_benchmark: dict[str, Any],
    *,
    channel_url: str,
    generated_at: str | None = None,
    thumbnail_dir: Path,
    download: bool = True,
    annotations: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    metrics = title_benchmark_by_id(title_benchmark)
    records = [
        build_record(
            record,
            metrics.get(extract_video_id(record)),
            thumbnail_dir=thumbnail_dir,
            download=download,
            annotations=annotations,
        )
        for record in channel_records
        if extract_video_id(record)
    ]
    format_counts = Counter(record.get("format") for record in records)
    summary = {
        "total_channel_records": len(records),
        "matched_to_title_benchmark": sum(1 for record in records if record["matched_to_title_benchmark"]),
        "long_videos": format_counts.get("long", 0),
        "short_videos": format_counts.get("short", 0),
        "downloaded_thumbnails": sum(1 for record in records if record["thumbnail_downloaded"]),
        "annotated_thumbnail_texts": sum(1 for record in records if record["thumbnail_text"]),
    }
    return {
        "source_channel_url": channel_url,
        "generated_at": generated_at or datetime.now(UTC).isoformat(),
        "thumbnail_dir": str(thumbnail_dir),
        "summary": summary,
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


def render_markdown(dataset: dict[str, Any], *, limit: int = 80) -> str:
    summary = dataset["summary"]
    lines = [
        "# Maymei Thumbnail Benchmark",
        "",
        "## Source",
        f"- Channel: `{dataset['source_channel_url']}`",
        f"- Generated at: `{dataset['generated_at']}`",
        f"- Thumbnail directory: `{dataset.get('thumbnail_dir', '')}`",
        "",
        "## Coverage",
        f"- Channel records: `{summary['total_channel_records']}`",
        f"- Matched to title benchmark: `{summary['matched_to_title_benchmark']}`",
        f"- Long videos: `{summary['long_videos']}`",
        f"- Shorts / short-form rows: `{summary['short_videos']}`",
        f"- Downloaded thumbnails: `{summary['downloaded_thumbnails']}`",
        f"- Annotated thumbnail text rows: `{summary.get('annotated_thumbnail_texts', 0)}`",
        "",
        "## Review Queue",
        "",
        "| Video | CTR | Impressions | Views | Formula | Thumbnail text | Status |",
        "|---|---:|---:|---:|---|---|---|",
    ]
    records = sorted(
        dataset["records"],
        key=lambda record: (
            record.get("ctr_percent") or 0,
            record.get("impressions") or 0,
        ),
        reverse=True,
    )
    for record in records[:limit]:
        title = str(record.get("title") or "").replace("|", "｜")
        thumbnail_text = record.get("thumbnail_text") or ""
        lines.append(
            "| "
            f"`{record.get('video_id')}` {title[:48]} | "
            f"`{format_number(record.get('ctr_percent'))}%` | "
            f"`{format_number(record.get('impressions'))}` | "
            f"`{format_number(record.get('view_count'))}` | "
            f"`{record.get('formula') or ''}` | "
            f"{thumbnail_text or '`(pending)`'} | "
            f"`{record.get('thumbnail_text_source')}` |"
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
    parser = argparse.ArgumentParser(
        description="Build a thumbnail benchmark by matching Maymei channel thumbnails to the title benchmark."
    )
    parser.add_argument("--channel", default=DEFAULT_CHANNEL_URL)
    parser.add_argument("--limit", type=int, default=500)
    parser.add_argument(
        "--title-benchmark",
        default=str(repo_root / "workspace" / "memory" / "style-corpus" / "maymei-title-benchmark.json"),
    )
    parser.add_argument(
        "--thumbnail-dir",
        default=str(repo_root / "workspace" / "memory" / "style-corpus" / "thumbnails"),
    )
    parser.add_argument(
        "--json-output",
        default=str(repo_root / "workspace" / "memory" / "style-corpus" / "maymei-thumbnail-benchmark.json"),
    )
    parser.add_argument(
        "--markdown-output",
        default=str(repo_root / "workspace" / "memory" / "style-corpus" / "maymei-thumbnail-benchmark.md"),
    )
    parser.add_argument(
        "--thumbnail-annotations",
        default=str(repo_root / "workspace" / "memory" / "style-corpus" / "maymei-thumbnail-text-annotations.json"),
    )
    parser.add_argument("--no-download", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    channel_records = fetch_channel_records(args.channel, limit=args.limit)
    title_benchmark = load_json(Path(args.title_benchmark))
    annotations = load_thumbnail_annotations(Path(args.thumbnail_annotations))
    dataset = build_dataset(
        channel_records,
        title_benchmark,
        channel_url=args.channel,
        thumbnail_dir=Path(args.thumbnail_dir),
        download=not args.no_download,
        annotations=annotations,
    )
    write_outputs(dataset, Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
