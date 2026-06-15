from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

try:
    from scripts.opencli_tooling import ensure_tooling_ready
except ModuleNotFoundError:  # pragma: no cover - supports direct `python scripts/...` execution
    from opencli_tooling import ensure_tooling_ready


LANGUAGE_LABELS = {
    "zh": "中文",
    "jp": "日文",
    "en": "英文",
}

GOOGLE_LANGUAGE_FLAGS = {
    "zh": "zh",
    "jp": "ja",
    "en": "en",
}

BREADTH_CHOICES = ("standard", "broad", "max")
YOUTUBE_API_ENV_KEYS = ("YOUTUBE_API_KEY", "YTAPIKEY", "YT_API_KEY")
YOUTUBE_SHORTS_MAX_SECONDS = 180


@dataclass(frozen=True)
class SearchTask:
    provider: str
    language: str
    site_label: str
    query: str
    limit: int
    note: str
    evidence_family: str
    tier: str = "core"
    shorts_only: bool = False
    url_must_contain: tuple[str, ...] = ()


@dataclass
class SearchResult:
    task: SearchTask
    command: str
    ok: bool
    records: list[dict[str, Any]]
    error: str = ""
    backend: str = "opencli"
    fallback_reason: str = ""


def slugify(text: str) -> str:
    cleaned: list[str] = []
    previous_was_dash = False
    for char in text.strip().lower():
        if char.isascii() and char.isalnum():
            cleaned.append(char)
            previous_was_dash = False
            continue
        if not previous_was_dash:
            cleaned.append("-")
            previous_was_dash = True
    value = "".join(cleaned).strip("-")
    return value or "research"


def make_task(
    provider: str,
    site_label: str,
    query_template: str,
    note: str,
    evidence_family: str,
    tier: str = "core",
    *,
    shorts_only: bool = False,
    url_must_contain: Iterable[str] = (),
) -> tuple[str, str, str, str, str, str, bool, tuple[str, ...]]:
    return (
        provider,
        site_label,
        query_template,
        note,
        evidence_family,
        tier,
        shorts_only,
        tuple(url_must_contain),
    )


TOPIC_TASKS = {
    "standard": {
        "zh": [
            make_task("youtube", "YouTube", "{name} 攻略", "中文長片主題簇", "video"),
            make_task("youtube", "YouTube", "{name} 必看", "中文高點擊 promise", "video"),
            make_task("bilibili", "bilibili", "{name} 攻略", "中文站內攻略樣本", "video"),
            make_task("google", "巴哈姆特論壇", "site:forum.gamer.com.tw {name} 攻略", "中文論壇問題簇", "community"),
            make_task("google", "巴哈創作", "site:home.gamer.com.tw {name}", "中文心得與攻略創作", "community"),
        ],
        "jp": [
            make_task("youtube", "YouTube", "{name} 攻略", "日文長片主題簇", "video"),
            make_task("youtube", "YouTube", "{name} 知らないと損", "日文反常識切角", "video"),
            make_task("google", "Game8", "site:game8.jp {name} 攻略", "日文攻略站熱門需求", "guide"),
            make_task("google", "GameWith", "site:gamewith.jp {name} 攻略", "日文攻略站熱門需求", "guide"),
        ],
        "en": [
            make_task("youtube", "YouTube", "{name} guide", "英文長片主題簇", "video"),
            make_task("youtube", "YouTube", "{name} mistakes", "英文避坑切角", "video"),
            make_task("reddit", "Reddit", "{name} tips", "英文玩家需求簇", "community"),
            make_task("google", "Steam Community", "site:steamcommunity.com {name} guide", "PC 玩家攻略與需求", "community"),
        ],
    },
    "broad": {
        "zh": [
            make_task("youtube", "YouTube", "{name} 隱藏", "中文隱藏內容需求", "video", "expansion"),
            make_task("youtube", "YouTube", "{name} 別做", "中文避坑切角", "video", "expansion"),
            make_task("bilibili", "bilibili", "{name} 开荒", "中文開荒與初期需求", "video", "expansion"),
            make_task("google", "bilibili", "site:bilibili.com {name} 攻略", "bilibili 公開頁補查", "video", "expansion"),
            make_task("google", "巴哈文章", "site:gamer.com.tw {name} 攻略", "中文攻略站補查", "guide", "expansion"),
            make_task("google", "Threads", "site:threads.net {name}", "中文社群補查", "community", "validation"),
        ],
        "jp": [
            make_task("youtube", "YouTube", "{name} 初心者", "日文新手需求", "video", "expansion"),
            make_task("youtube", "YouTube", "{name} 効率", "日文效率切角", "video", "expansion"),
            make_task("google", "Altema", "site:altema.jp {name}", "日文攻略站補查", "guide", "expansion"),
            make_task("google", "Kamigame", "site:kamigame.jp {name}", "日文攻略站補查", "guide", "expansion"),
            make_task("google", "Threads", "site:threads.net {name}", "日文社群補查", "community", "validation"),
        ],
        "en": [
            make_task("youtube", "YouTube", "{name} hidden", "英文隱藏內容切角", "video", "expansion"),
            make_task("reddit", "Reddit", "{name} best early", "英文早期痛點", "community", "expansion"),
            make_task("google", "Steam Discussions", "site:steamcommunity.com/app {name} discussion", "Steam 討論區痛點", "community", "expansion"),
            make_task("google", "GameFAQs", "site:gamefaqs.gamespot.com {name}", "老牌攻略與問答補查", "guide", "validation"),
            make_task("google", "Reddit", "site:reddit.com {name} guide", "Reddit 公開頁補查", "community", "validation"),
            make_task("google", "Threads", "site:threads.net {name}", "英文社群補查", "community", "validation"),
        ],
    },
    "max": {
        "zh": [
            make_task("twitter", "X / Twitter", "{name}", "中文即時熱點補查", "community", "validation"),
            make_task("google", "Discord Discovery", "site:discord.gg {name}", "社群入口補查", "community", "validation"),
        ],
        "jp": [
            make_task("twitter", "X / Twitter", "{name}", "日文即時熱點補查", "community", "validation"),
            make_task("google", "Discord Discovery", "site:discord.gg {name}", "社群入口補查", "community", "validation"),
        ],
        "en": [
            make_task("twitter", "X / Twitter", "{name}", "英文即時熱點補查", "community", "validation"),
            make_task("google", "Discord Discovery", "site:discord.gg {name}", "社群入口補查", "community", "validation"),
            make_task("google", "Official Support", "site:support.nintendo.com {name}", "官方說明與事實校正", "fact-check", "validation"),
        ],
    },
}

SHORTS_TASKS = {
    "standard": {
        "zh": [
            make_task("youtube", "YouTube Shorts", "{name} shorts", "中文 Shorts 主查詢", "video", shorts_only=True, url_must_contain=("/shorts/",)),
            make_task("youtube", "YouTube Shorts", "{name} 隱藏 shorts", "中文 Shorts punch", "video", shorts_only=True, url_must_contain=("/shorts/",)),
            make_task("tiktok", "TikTok", "{name}", "TikTok 主查詢", "video"),
            make_task("bilibili", "bilibili", "{name} 攻略", "bilibili 短內容與切片補查", "video"),
            make_task("google", "Instagram Reels", "site:instagram.com/reel/ {name}", "IG Reels 主查詢", "video"),
            make_task("google", "巴哈姆特論壇", "site:forum.gamer.com.tw {name}", "中文社群共鳴補查", "community"),
        ],
        "jp": [
            make_task("youtube", "YouTube Shorts", "{name} shorts", "日文 Shorts 主查詢", "video", shorts_only=True, url_must_contain=("/shorts/",)),
            make_task("youtube", "YouTube Shorts", "{name} 小ネタ shorts", "日文 Shorts 小知識角度", "video", shorts_only=True, url_must_contain=("/shorts/",)),
            make_task("tiktok", "TikTok", "{name}", "日文 TikTok 主查詢", "video"),
            make_task("google", "Instagram Reels", "site:instagram.com/reel/ {name}", "日文 IG Reels 補查", "video"),
        ],
        "en": [
            make_task("youtube", "YouTube Shorts", "{name} shorts", "英文 Shorts 主查詢", "video", shorts_only=True, url_must_contain=("/shorts/",)),
            make_task("youtube", "YouTube Shorts", "{name} hidden shorts", "英文 Shorts 隱藏角度", "video", shorts_only=True, url_must_contain=("/shorts/",)),
            make_task("tiktok", "TikTok", "{name}", "英文 TikTok 主查詢", "video"),
            make_task("google", "Instagram Reels", "site:instagram.com/reel/ {name}", "英文 IG Reels 補查", "video"),
        ],
    },
    "broad": {
        "zh": [
            make_task("youtube", "YouTube Shorts", "{name} 技巧 shorts", "中文 Shorts 教學 punch", "video", "expansion", shorts_only=True, url_must_contain=("/shorts/",)),
            make_task("youtube", "YouTube Shorts", "{name} 搞笑 shorts", "中文 Shorts 趣味 punch", "video", "expansion", shorts_only=True, url_must_contain=("/shorts/",)),
            make_task("google", "TikTok Web", "site:tiktok.com {name}", "TikTok 公開頁補查", "video", "expansion"),
            make_task("google", "bilibili", "site:bilibili.com {name}", "bilibili 公開頁補查", "video", "expansion"),
            make_task("google", "Threads", "site:threads.net {name}", "短內容社群補查", "community", "validation"),
        ],
        "jp": [
            make_task("youtube", "YouTube Shorts", "{name} 裏技 shorts", "日文 Shorts 裏技切角", "video", "expansion", shorts_only=True, url_must_contain=("/shorts/",)),
            make_task("youtube", "YouTube Shorts", "{name} 比較 shorts", "日文 Shorts 比較切角", "video", "expansion", shorts_only=True, url_must_contain=("/shorts/",)),
            make_task("google", "TikTok Web", "site:tiktok.com {name}", "TikTok 公開頁補查", "video", "expansion"),
            make_task("google", "Threads", "site:threads.net {name}", "短內容社群補查", "community", "validation"),
        ],
        "en": [
            make_task("youtube", "YouTube Shorts", "{name} tips shorts", "英文 Shorts 技巧切角", "video", "expansion", shorts_only=True, url_must_contain=("/shorts/",)),
            make_task("youtube", "YouTube Shorts", "{name} funny shorts", "英文 Shorts 反差 / 趣味切角", "video", "expansion", shorts_only=True, url_must_contain=("/shorts/",)),
            make_task("google", "TikTok Web", "site:tiktok.com {name}", "TikTok 公開頁補查", "video", "expansion"),
            make_task("google", "Threads", "site:threads.net {name}", "短內容社群補查", "community", "validation"),
        ],
    },
    "max": {
        "zh": [
            make_task("twitter", "X / Twitter", "{name}", "中文短內容即時熱點補查", "community", "validation"),
        ],
        "jp": [
            make_task("twitter", "X / Twitter", "{name}", "日文短內容即時熱點補查", "community", "validation"),
        ],
        "en": [
            make_task("twitter", "X / Twitter", "{name}", "英文短內容即時熱點補查", "community", "validation"),
            make_task("reddit", "Reddit", "{name} funny", "英文短內容共鳴補查", "community", "validation"),
        ],
    },
}


def build_tasks_from_specs(
    names: dict[str, str],
    limit: int,
    spec_sets: dict[str, dict[str, list[tuple[str, str, str, str, str, str, bool, tuple[str, ...]]]]],
    breadth: str,
) -> list[SearchTask]:
    ordered_breadths = BREADTH_CHOICES[: BREADTH_CHOICES.index(breadth) + 1]
    tasks: list[SearchTask] = []
    for language, name in names.items():
        if not name:
            continue
        for breadth_key in ordered_breadths:
            for spec in spec_sets.get(breadth_key, {}).get(language, []):
                provider, site_label, query_template, note, family, tier, shorts_only, url_must_contain = spec
                tasks.append(
                    SearchTask(
                        provider=provider,
                        language=language,
                        site_label=site_label,
                        query=query_template.format(name=name),
                        limit=limit,
                        note=note,
                        evidence_family=family,
                        tier=tier,
                        shorts_only=shorts_only,
                        url_must_contain=url_must_contain,
                    )
                )
    return dedupe_tasks(tasks)


def dedupe_tasks(tasks: list[SearchTask]) -> list[SearchTask]:
    seen: set[tuple[str, str, str, str]] = set()
    unique: list[SearchTask] = []
    for task in tasks:
        key = (task.provider, task.language, task.site_label, task.query)
        if key in seen:
            continue
        seen.add(key)
        unique.append(task)
    return unique


def build_topic_tasks(names: dict[str, str], limit: int, breadth: str = "broad") -> list[SearchTask]:
    return build_tasks_from_specs(names, limit, TOPIC_TASKS, breadth)


def build_shorts_tasks(names: dict[str, str], limit: int, breadth: str = "broad") -> list[SearchTask]:
    return build_tasks_from_specs(names, limit, SHORTS_TASKS, breadth)


def resolve_opencli_binary(explicit_path: str = "") -> str:
    candidates = [explicit_path.strip(), os.environ.get("OPENCLI_BIN", "").strip()]
    candidates.extend(["opencli.cmd", "opencli", "opencli.ps1"])
    for candidate in candidates:
        if candidate and shutil.which(candidate):
            return candidate
    return "opencli"


def build_opencli_args(task: SearchTask, opencli_bin: str = "") -> list[str]:
    binary = resolve_opencli_binary(opencli_bin)
    if task.provider == "youtube":
        return [binary, "youtube", "search", task.query, "--limit", str(task.limit), "-f", "json"]
    if task.provider == "google":
        return [
            binary,
            "google",
            "search",
            task.query,
            "--limit",
            str(task.limit),
            "--lang",
            GOOGLE_LANGUAGE_FLAGS[task.language],
            "-f",
            "json",
        ]
    if task.provider == "reddit":
        return [
            binary,
            "reddit",
            "search",
            task.query,
            "--sort",
            "top",
            "--time",
            "month",
            "--limit",
            str(task.limit),
            "-f",
            "json",
        ]
    if task.provider == "bilibili":
        return [binary, "bilibili", "search", task.query, "--limit", str(task.limit), "-f", "json"]
    if task.provider == "tiktok":
        return [binary, "tiktok", "search", task.query, "--limit", str(task.limit), "-f", "json"]
    if task.provider == "twitter":
        return [binary, "twitter", "search", task.query, "--filter", "top", "--limit", str(task.limit), "-f", "json"]
    raise ValueError(f"Unsupported provider: {task.provider}")


def filter_records_for_task(task: SearchTask, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    filtered = records
    if task.shorts_only:
        filtered = [record for record in filtered if "/shorts/" in str(record.get("url", ""))]
    for marker in task.url_must_contain:
        filtered = [record for record in filtered if marker in str(record.get("url", ""))]
    return filtered


def parse_dotenv_file(dotenv_path: Path) -> dict[str, str]:
    if not dotenv_path.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value
    return values


def read_windows_user_env(name: str) -> str:
    if os.name != "nt":
        return ""

    try:
        import winreg
    except ImportError:
        return ""

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
            value, _ = winreg.QueryValueEx(key, name)
    except OSError:
        return ""
    return str(value).strip()


def resolve_youtube_api_key(repo_root: Path | None = None) -> str:
    for env_name in YOUTUBE_API_ENV_KEYS:
        value = os.environ.get(env_name, "").strip()
        if value:
            return value

    effective_root = repo_root or Path(__file__).resolve().parents[1]
    dotenv_values = parse_dotenv_file(effective_root / ".env")
    for env_name in YOUTUBE_API_ENV_KEYS:
        value = dotenv_values.get(env_name, "").strip()
        if value:
            return value

    for env_name in YOUTUBE_API_ENV_KEYS:
        value = read_windows_user_env(env_name)
        if value:
            return value

    return ""


def fetch_json(url: str, timeout: float = 15.0) -> Any:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "writing-agent/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def parse_iso8601_duration_to_seconds(value: str) -> int:
    if not value:
        return 0
    match = re.fullmatch(
        r"PT(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?",
        value,
    )
    if not match:
        return 0
    hours = int(match.group("hours") or 0)
    minutes = int(match.group("minutes") or 0)
    seconds = int(match.group("seconds") or 0)
    return hours * 3600 + minutes * 60 + seconds


def format_duration(total_seconds: int) -> str:
    if total_seconds <= 0:
        return ""
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes}:{seconds:02d}"


def format_view_count(value: str | int) -> str:
    raw = str(value).strip()
    if not raw:
        return ""
    try:
        return f"觀看次數：{int(raw):,}次"
    except ValueError:
        return raw


def build_youtube_record(
    video_id: str,
    snippet: dict[str, Any],
    detail: dict[str, Any],
    *,
    shorts_only: bool,
) -> dict[str, Any]:
    duration_seconds = parse_iso8601_duration_to_seconds(
        str(detail.get("contentDetails", {}).get("duration", ""))
    )
    if shorts_only and duration_seconds <= YOUTUBE_SHORTS_MAX_SECONDS:
        url = f"https://www.youtube.com/shorts/{video_id}"
    else:
        url = f"https://www.youtube.com/watch?v={video_id}"

    return {
        "title": str(snippet.get("title", "")).strip(),
        "channel": str(snippet.get("channelTitle", "")).strip(),
        "published": str(snippet.get("publishedAt", "")).strip(),
        "views": format_view_count(detail.get("statistics", {}).get("viewCount", "")),
        "duration": format_duration(duration_seconds),
        "url": url,
    }


def search_youtube_data_api(task: SearchTask, api_key: str = "") -> list[dict[str, Any]]:
    effective_api_key = api_key.strip() or resolve_youtube_api_key()
    if not effective_api_key:
        return []

    search_params = {
        "part": "snippet",
        "q": task.query,
        "type": "video",
        "maxResults": str(min(max(task.limit, 1), 50)),
        "key": effective_api_key,
    }
    if task.shorts_only:
        search_params["videoDuration"] = "short"

    search_url = "https://www.googleapis.com/youtube/v3/search?" + urllib.parse.urlencode(search_params)
    search_payload = fetch_json(search_url)

    items = search_payload.get("items", []) if isinstance(search_payload, dict) else []
    video_ids = [
        str(item.get("id", {}).get("videoId", "")).strip()
        for item in items
        if isinstance(item, dict)
    ]
    video_ids = [video_id for video_id in video_ids if video_id]
    if not video_ids:
        return []

    videos_params = {
        "part": "snippet,statistics,contentDetails",
        "id": ",".join(video_ids),
        "key": effective_api_key,
    }
    videos_url = "https://www.googleapis.com/youtube/v3/videos?" + urllib.parse.urlencode(videos_params)
    videos_payload = fetch_json(videos_url)
    details = videos_payload.get("items", []) if isinstance(videos_payload, dict) else []
    details_by_id = {
        str(detail.get("id", "")).strip(): detail
        for detail in details
        if isinstance(detail, dict)
    }

    records: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        video_id = str(item.get("id", {}).get("videoId", "")).strip()
        if not video_id:
            continue
        detail = details_by_id.get(video_id, {})
        snippet = item.get("snippet", {}) if isinstance(item.get("snippet", {}), dict) else {}
        records.append(build_youtube_record(video_id, snippet, detail, shorts_only=task.shorts_only))

    return records


def attempt_youtube_api_fallback(task: SearchTask, command: str, reason: str) -> SearchResult | None:
    api_key = resolve_youtube_api_key()
    if not api_key:
        return None

    try:
        records = search_youtube_data_api(task, api_key=api_key)
    except (OSError, urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, ValueError):
        return None

    return SearchResult(
        task=task,
        command=command,
        ok=True,
        records=filter_records_for_task(task, records),
        backend="youtube-data-api",
        fallback_reason=reason,
    )


def run_search_task(task: SearchTask, opencli_bin: str = "") -> SearchResult:
    args = build_opencli_args(task, opencli_bin=opencli_bin)
    completed = subprocess.run(
        args,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    command = subprocess.list2cmdline(args)

    if completed.returncode != 0:
        fallback = None
        if task.provider == "youtube":
            fallback = attempt_youtube_api_fallback(task, command, "opencli command failed")
        if fallback is not None:
            return fallback
        return SearchResult(
            task=task,
            command=command,
            ok=False,
            records=[],
            error=(completed.stderr or completed.stdout).strip(),
        )

    try:
        parsed = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        fallback = None
        if task.provider == "youtube":
            fallback = attempt_youtube_api_fallback(task, command, "opencli returned invalid json")
        if fallback is not None:
            return fallback
        return SearchResult(
            task=task,
            command=command,
            ok=False,
            records=[],
            error=f"Unable to parse JSON output: {exc}",
        )

    if isinstance(parsed, list):
        records = parsed
    elif isinstance(parsed, dict):
        records = parsed.get("items") or parsed.get("results") or parsed.get("data") or []
        if not isinstance(records, list):
            records = []
    else:
        records = []

    filtered_records = filter_records_for_task(task, records)
    if task.provider == "youtube" and not filtered_records:
        fallback = attempt_youtube_api_fallback(task, command, "opencli returned no retained hits")
        if fallback is not None:
            return fallback

    return SearchResult(
        task=task,
        command=command,
        ok=True,
        records=filtered_records,
    )


def pick_title(record: dict[str, Any]) -> str:
    for key in ("title", "desc", "text", "snippet", "name"):
        value = str(record.get(key, "")).strip()
        if value:
            return value
    return "(untitled)"


def pick_url(record: dict[str, Any]) -> str:
    return str(record.get("url", "")).strip()


def pick_meta(record: dict[str, Any]) -> str:
    meta_parts = []
    for key in (
        "channel",
        "author",
        "subreddit",
        "views",
        "plays",
        "likes",
        "duration",
        "published",
        "created_at",
        "score",
        "comments",
    ):
        value = str(record.get(key, "")).strip()
        if value:
            meta_parts.append(value)
    return " | ".join(meta_parts)


def render_query_log(mode: str, names: dict[str, str], results: list[SearchResult], breadth: str) -> str:
    generated_at = datetime.now().isoformat(timespec="seconds")
    lines = [
        "# Query Log",
        "",
        f"- Mode: `{mode}`",
        f"- Search breadth: `{breadth}`",
        f"- Generated at: `{generated_at}`",
        f"- Inputs: `{json.dumps(names, ensure_ascii=False)}`",
    ]

    for index, result in enumerate(results, start=1):
        task = result.task
        query_lines = [
            "",
            f"## Query {index}",
            f"- Query platform / site: `{task.provider}` / `{task.site_label}`",
            f"- Language: `{LANGUAGE_LABELS.get(task.language, task.language)}`",
            f"- Evidence family: `{task.evidence_family}`",
            f"- Search tier: `{task.tier}`",
            f"- opencli command: `{result.command}`",
            f"- Execution backend: `{result.backend}`",
            f"- Keywords: `{task.query}`",
        ]
        if result.fallback_reason:
            query_lines.append(f"- Fallback reason: `{result.fallback_reason}`")
        query_lines.extend(
            [
                f"- Why this query exists: {task.note}",
                "- High-signal hits:",
            ]
        )
        lines.extend(query_lines)

        if result.records:
            for record in result.records[:5]:
                title = pick_title(record)
                url = pick_url(record)
                meta = pick_meta(record)
                summary = f"`{title}`"
                if meta:
                    summary = f"{summary} | `{meta}`"
                if url:
                    summary = f"{summary} | {url}"
                lines.append(f"  - {summary}")
        elif result.ok:
            lines.append("  - No retained hits after filtering.")
        else:
            lines.append(f"  - Command failed: {result.error or 'Unknown error'}")

        conclusion_flag = "pending" if result.ok else "skip: command failed"
        lines.append(f"- Included in final conclusion?: `{conclusion_flag}`")

    lines.append("")
    return "\n".join(lines)


def render_source_index(results: list[SearchResult], breadth: str) -> str:
    lines = [
        "# Source Index",
        "",
        f"- Generated at: `{datetime.now().isoformat(timespec='seconds')}`",
        f"- Search breadth: `{breadth}`",
    ]
    seen_urls: set[str] = set()
    source_number = 1

    for result in results:
        for record in result.records:
            url = pick_url(record)
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            lines.extend(
                [
                    "",
                    f"## Source {source_number}",
                    f"- Source name: `{pick_title(record)}`",
                    f"- URL: `{url}`",
                    f"- Source type: `{result.task.site_label}`",
                    f"- Evidence family: `{result.task.evidence_family}`",
                    f"- Search tier: `{result.task.tier}`",
                    f"- Why keep it?: {result.task.note}",
                ]
            )
            source_number += 1

    if source_number == 1:
        lines.extend(["", "- No sources captured yet."])

    lines.append("")
    return "\n".join(lines)


def render_decision_log_stub(mode: str, breadth: str) -> str:
    return "\n".join(
        [
            "# Decision Log",
            "",
            "## Confirmed Facts",
            f"- `opencli` queries for `{mode}` have been captured.",
            f"- Search breadth used: `{breadth}`.",
            "",
            "## Working Inferences",
            "- Pending manual clustering and cross-source validation.",
            "",
            "## Included In Final Output",
            "- Pending synthesis.",
            "",
            "## Excluded / Rejected Angles",
            "- Pending synthesis.",
            "",
            "## Unknowns / Follow-up",
            "- Note failed commands, weak evidence, and platforms that still need manual follow-up here.",
            "",
        ]
    )


def write_outputs(
    run_dir: Path,
    mode: str,
    names: dict[str, str],
    results: list[SearchResult],
    breadth: str,
) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "mode": mode,
        "breadth": breadth,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "inputs": names,
        "results": [
            {
                **asdict(result.task),
                "command": result.command,
                "ok": result.ok,
                "error": result.error,
                "backend": result.backend,
                "fallback_reason": result.fallback_reason,
                "records": result.records,
            }
            for result in results
        ],
    }

    (run_dir / "opencli-results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (run_dir / "query-log.md").write_text(render_query_log(mode, names, results, breadth), encoding="utf-8")
    (run_dir / "sources.md").write_text(render_source_index(results, breadth), encoding="utf-8")
    decision_log = run_dir / "decision-log.md"
    if not decision_log.exists():
        decision_log.write_text(render_decision_log_stub(mode, breadth), encoding="utf-8")


def default_run_dir(repo_root: Path, mode: str, slug: str) -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    return repo_root / "workspace" / "memory" / "runs" / f"{timestamp}-{mode}-{slug}"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect long-form or Shorts topic research signals with opencli.")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    def add_shared_arguments(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("slug", help="Game slug used in the run directory name.")
        subparser.add_argument("--name-zh", default="", help="Chinese game name or keyword.")
        subparser.add_argument("--name-jp", default="", help="Japanese game name or keyword.")
        subparser.add_argument("--name-en", default="", help="English game name or keyword.")
        subparser.add_argument("--limit", type=int, default=10, help="Per-query result limit.")
        subparser.add_argument("--breadth", choices=BREADTH_CHOICES, default="broad", help="Search depth profile.")
        subparser.add_argument("--run-dir", default="", help="Override the output run directory.")
        subparser.add_argument("--opencli-bin", default="", help="Optional explicit path or command name for opencli.")
        subparser.add_argument(
            "--skip-tool-readiness",
            action="store_true",
            help="Skip OpenCLI doctor / Browser Bridge readiness check before collecting searches.",
        )
        subparser.add_argument(
            "--repair-tools",
            action="store_true",
            help="Update @jackwener/opencli and yt-dlp before the readiness check.",
        )

    add_shared_arguments(subparsers.add_parser("topic", help="Collect long-form topic signals with opencli."))
    add_shared_arguments(subparsers.add_parser("shorts-topic", help="Collect Shorts topic signals with opencli."))
    return parser.parse_args(argv)


def collect_inputs(args: argparse.Namespace) -> dict[str, str]:
    return {
        "zh": args.name_zh.strip(),
        "jp": args.name_jp.strip(),
        "en": args.name_en.strip(),
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    names = collect_inputs(args)
    if not any(names.values()):
        print("Provide at least one of --name-zh / --name-jp / --name-en.")
        return 1

    limit = max(1, min(args.limit, 50))
    if args.mode == "topic":
        tasks = build_topic_tasks(names, limit, breadth=args.breadth)
    else:
        tasks = build_shorts_tasks(names, limit, breadth=args.breadth)

    if not tasks:
        print("No search tasks were generated from the provided inputs.")
        return 1

    repo_root = Path(__file__).resolve().parents[1]
    slug = slugify(args.slug)
    run_dir = Path(args.run_dir) if args.run_dir else default_run_dir(repo_root, args.mode, slug)

    if not args.skip_tool_readiness:
        readiness = ensure_tooling_ready(
            repo_root=repo_root,
            run_dir=run_dir / "tool-readiness",
            update=args.repair_tools,
            opencli_bin=args.opencli_bin,
            run_network_tests=True,
        )
        if not readiness.doctor_ok:
            print("OpenCLI Browser Bridge is not ready. Review tool-readiness/tool-readiness.md.")
            return 2
        if not readiness.transcript_ok:
            print("YouTube transcript fallback is not ready. Review tool-readiness/tool-readiness.md.")
            return 3

    results = [run_search_task(task, opencli_bin=args.opencli_bin) for task in tasks]
    write_outputs(run_dir=run_dir, mode=args.mode, names=names, results=results, breadth=args.breadth)

    failed = sum(1 for result in results if not result.ok)
    print(f"Wrote {len(results)} opencli query results to {run_dir}")
    if failed:
        print(f"{failed} query commands failed. Review query-log.md and decision-log.md for follow-up.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
