from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable


DEFAULT_CHANNEL_URL = "https://www.youtube.com/@maymei_gaming/videos"


def safe_int(value: Any) -> int:
    if value is None:
        return 0
    if isinstance(value, int):
        return value
    raw = str(value).strip().replace(",", "")
    if not raw:
        return 0
    try:
        return int(float(raw))
    except ValueError:
        return 0


def parse_yt_dlp_video(payload: dict[str, Any]) -> dict[str, Any]:
    video_id = str(payload.get("id") or payload.get("display_id") or "").strip()
    view_count = safe_int(payload.get("view_count"))
    like_count = safe_int(payload.get("like_count"))
    comment_count = safe_int(payload.get("comment_count"))
    like_rate = (like_count / view_count) if view_count and like_count else 0.0
    url = str(payload.get("webpage_url") or payload.get("url") or "").strip()
    if video_id and not url:
        url = f"https://www.youtube.com/watch?v={video_id}"

    return {
        "video_id": video_id,
        "title": str(payload.get("title") or "").strip(),
        "url": url,
        "view_count": view_count,
        "like_count": like_count,
        "like_rate": round(like_rate, 6),
        "comment_count": comment_count,
        "upload_date": str(payload.get("upload_date") or "").strip(),
        "duration": safe_int(payload.get("duration")),
    }


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


def run_yt_dlp(args: list[str]) -> str:
    completed = subprocess.run(
        args,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if completed.returncode != 0:
        raise RuntimeError((completed.stderr or completed.stdout).strip())
    return completed.stdout


def fetch_flat_playlist(
    channel_url: str,
    *,
    limit: int,
    yt_dlp_bin: str = "yt-dlp",
) -> list[dict[str, Any]]:
    args = [
        yt_dlp_bin,
        "--flat-playlist",
        "--dump-json",
        "--playlist-end",
        str(limit),
        channel_url,
    ]
    return [parse_yt_dlp_video(item) for item in parse_json_lines(run_yt_dlp(args))]


def fetch_video_detail(url: str, *, yt_dlp_bin: str = "yt-dlp") -> dict[str, Any]:
    args = [yt_dlp_bin, "--dump-json", "--skip-download", url]
    records = parse_json_lines(run_yt_dlp(args))
    if not records:
        return {}
    return parse_yt_dlp_video(records[0])


def collect_video_metrics(
    channel_url: str = DEFAULT_CHANNEL_URL,
    *,
    limit: int = 300,
    with_details: bool = True,
    yt_dlp_bin: str = "yt-dlp",
) -> list[dict[str, Any]]:
    flat_records = fetch_flat_playlist(channel_url, limit=limit, yt_dlp_bin=yt_dlp_bin)
    if not with_details:
        return flat_records

    detailed: list[dict[str, Any]] = []
    for record in flat_records:
        url = record.get("url") or (
            f"https://www.youtube.com/watch?v={record['video_id']}" if record.get("video_id") else ""
        )
        if not url:
            detailed.append(record)
            continue
        try:
            detail = fetch_video_detail(str(url), yt_dlp_bin=yt_dlp_bin)
        except RuntimeError:
            detail = {}
        detailed.append({**record, **detail} if detail else record)
    return detailed


def write_metrics(records: Iterable[dict[str, Any]], output_path: Path, *, channel_url: str) -> None:
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "channel_url": channel_url,
        "records": list(records),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    default_output = repo_root / "workspace" / "memory" / "style-corpus" / "maymei-video-metrics.json"
    parser = argparse.ArgumentParser(description="Build Maymei YouTube video metrics from public metadata.")
    parser.add_argument("--channel", default=DEFAULT_CHANNEL_URL)
    parser.add_argument("--limit", type=int, default=300)
    parser.add_argument("--output", default=str(default_output))
    parser.add_argument("--yt-dlp-bin", default="yt-dlp")
    parser.add_argument("--flat-only", action="store_true", help="Skip per-video detail calls.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    records = collect_video_metrics(
        args.channel,
        limit=args.limit,
        with_details=not args.flat_only,
        yt_dlp_bin=args.yt_dlp_bin,
    )
    write_metrics(records, Path(args.output), channel_url=args.channel)
    print(f"Wrote {len(records)} video metric records to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
