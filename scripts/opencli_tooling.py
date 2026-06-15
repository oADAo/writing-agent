from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


DEFAULT_TRANSCRIPT_LANGS = ("en", "zh-Hant", "zh-Hans", "ja")
DEFAULT_TRANSCRIPT_URL = "https://www.youtube.com/watch?v=I9bUB3mcqso"
DEFAULT_YOUTUBE_VIDEO_URL = "https://www.youtube.com/watch?v=rscYUQZCfFM"
DEFAULT_BILIBILI_BVID = "BV1TnLn65EFe"
DEFAULT_WEB_READ_URL = "https://forza.net/news/forza-horizon-6-series-1"


@dataclass
class CommandResult:
    command: str
    ok: bool
    returncode: int
    stdout: str = ""
    stderr: str = ""


@dataclass
class TranscriptResult:
    ok: bool
    method: str
    output_files: list[str]
    attempts: list[CommandResult]
    error: str = ""


@dataclass
class ToolingReport:
    generated_at: str
    opencli_version: str
    opencli_latest: str
    yt_dlp_version: str
    doctor_ok: bool
    transcript_ok: bool
    commands: list[CommandResult]
    transcript: TranscriptResult | None = None
    notes: list[str] | None = None


def repo_root_from_here() -> Path:
    return Path(__file__).resolve().parents[1]


def command_to_text(args: list[str]) -> str:
    return subprocess.list2cmdline([str(arg) for arg in args])


def run_command(args: list[str], *, cwd: Path, timeout: int = 120) -> CommandResult:
    try:
        completed = subprocess.run(
            [str(arg) for arg in args],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except FileNotFoundError as exc:
        return CommandResult(
            command=command_to_text(args),
            ok=False,
            returncode=127,
            stderr=str(exc),
        )
    return CommandResult(
        command=command_to_text(args),
        ok=completed.returncode == 0,
        returncode=completed.returncode,
        stdout=completed.stdout.strip(),
        stderr=completed.stderr.strip(),
    )


def resolve_binary(explicit: str, env_name: str, candidates: Iterable[str]) -> str:
    values = [explicit.strip(), os.environ.get(env_name, "").strip(), *candidates]
    for value in values:
        if value and shutil.which(value):
            return value
    return explicit.strip() or next(iter(candidates))


def resolve_opencli_binary(explicit: str = "") -> str:
    return resolve_binary(explicit, "OPENCLI_BIN", ("opencli.cmd", "opencli", "opencli.ps1"))


def resolve_yt_dlp_binary(explicit: str = "") -> str:
    return resolve_binary(explicit, "YT_DLP_BIN", ("yt-dlp", "yt-dlp.exe"))


def resolve_npm_binary() -> str:
    return resolve_binary("", "NPM_BIN", ("npm.cmd", "npm"))


def first_line(value: str) -> str:
    return value.splitlines()[0].strip() if value.strip() else ""


def sanitize_filename(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip())
    return cleaned.strip("-") or "transcript"


def find_extension_dir(repo_root: Path) -> Path | None:
    env_value = os.environ.get("OPENCLI_EXTENSION_DIR", "").strip()
    candidates = [
        Path(env_value) if env_value else None,
        Path("C:/opencli-runtime/extension-v1.0.15"),
        Path("C:/Users/玫玫/opencli/extension"),
        repo_root / "workspace" / "tools" / "opencli-extension-v1.0.15",
    ]
    for candidate in candidates:
        if candidate and (candidate / "manifest.json").exists():
            return candidate
    return None


def find_browser() -> Path | None:
    env_value = os.environ.get("OPENCLI_BROWSER", "").strip()
    candidates = [
        Path(env_value) if env_value else None,
        Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
        Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
        Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
        Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    ]
    for candidate in candidates:
        if candidate and candidate.exists():
            return candidate
    return None


def browser_profile_dir(repo_root: Path) -> Path:
    env_value = os.environ.get("OPENCLI_BROWSER_PROFILE", "").strip()
    if env_value:
        return Path(env_value)
    return Path("C:/opencli-runtime/edge-profile")


def launch_browser_bridge(repo_root: Path) -> tuple[bool, str]:
    browser = find_browser()
    extension = find_extension_dir(repo_root)
    profile = browser_profile_dir(repo_root)
    if not browser:
        return False, "No supported Chrome/Edge browser executable found."
    if not extension:
        return False, "No OpenCLI extension directory found."

    profile.mkdir(parents=True, exist_ok=True)
    args = [
        str(browser),
        f"--user-data-dir={profile}",
        f"--disable-extensions-except={extension}",
        f"--load-extension={extension}",
        "--no-first-run",
        "--no-default-browser-check",
        "data:text/html,<html></html>",
    ]
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0
    subprocess.Popen(
        args,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=creationflags,
    )
    return True, f"Launched {browser} with extension {extension} and profile {profile}."


def doctor_is_ok(result: CommandResult) -> bool:
    text = f"{result.stdout}\n{result.stderr}"
    return result.ok and "[OK] Connectivity" in text and "Everything looks good" in text


def ensure_browser_bridge(repo_root: Path, opencli_bin: str, commands: list[CommandResult]) -> bool:
    doctor = run_command([opencli_bin, "doctor"], cwd=repo_root, timeout=60)
    commands.append(doctor)
    if doctor_is_ok(doctor):
        return True

    restart = run_command([opencli_bin, "daemon", "restart"], cwd=repo_root, timeout=60)
    commands.append(restart)
    launched, launch_note = launch_browser_bridge(repo_root)
    commands.append(CommandResult("launch OpenCLI Browser Bridge", launched, 0 if launched else 1, launch_note, ""))
    if not launched:
        return False

    deadline = time.time() + 30
    while time.time() < deadline:
        time.sleep(3)
        doctor = run_command([opencli_bin, "doctor"], cwd=repo_root, timeout=60)
        commands.append(doctor)
        if doctor_is_ok(doctor):
            return True
    return False


def write_command_stdout(path: Path, result: CommandResult) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(result.stdout, encoding="utf-8")


def fetch_youtube_transcript(
    url: str,
    output_dir: Path,
    *,
    label: str = "",
    opencli_bin: str = "",
    yt_dlp_bin: str = "",
    repo_root: Path | None = None,
    languages: Iterable[str] = DEFAULT_TRANSCRIPT_LANGS,
) -> TranscriptResult:
    root = repo_root or repo_root_from_here()
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_label = sanitize_filename(label or url.rsplit("=", 1)[-1].rsplit("/", 1)[-1])
    opencli = resolve_opencli_binary(opencli_bin)
    attempts: list[CommandResult] = []

    for lang in languages:
        args = [opencli, "youtube", "transcript", url, "--lang", lang, "-f", "md"]
        result = run_command(args, cwd=root, timeout=180)
        attempts.append(result)
        if result.ok and len(result.stdout.strip()) > 80:
            output_file = output_dir / f"{safe_label}.{lang}.opencli.md"
            write_command_stdout(output_file, result)
            return TranscriptResult(True, "opencli-youtube-transcript", [str(output_file)], attempts)

    auto_result = run_command([opencli, "youtube", "transcript", url, "-f", "md"], cwd=root, timeout=180)
    attempts.append(auto_result)
    if auto_result.ok and len(auto_result.stdout.strip()) > 80:
        output_file = output_dir / f"{safe_label}.auto.opencli.md"
        write_command_stdout(output_file, auto_result)
        return TranscriptResult(True, "opencli-youtube-transcript-auto", [str(output_file)], attempts)

    yt_dlp = resolve_yt_dlp_binary(yt_dlp_bin)
    before = {path.resolve() for path in output_dir.glob(f"{safe_label}*")}
    lang_arg = ",".join([f"{lang}.*" for lang in languages])
    args = [
        yt_dlp,
        "--skip-download",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs",
        lang_arg,
        "--sub-format",
        "vtt",
        "--convert-subs",
        "srt",
        "--print",
        "after_move:filepath",
        "-o",
        str(output_dir / f"{safe_label}.%(ext)s"),
        url,
    ]
    yt_result = run_command(args, cwd=root, timeout=240)
    attempts.append(yt_result)
    after = {path.resolve() for path in output_dir.glob(f"{safe_label}*")}
    created = sorted(str(path) for path in after - before if path.exists() and path.stat().st_size > 0)
    if yt_result.ok and created:
        return TranscriptResult(True, "yt-dlp-subs", created, attempts)

    error = yt_result.stderr or yt_result.stdout or "No transcript or subtitle file was created."
    return TranscriptResult(False, "none", created, attempts, error)


def run_smoke_tests(repo_root: Path, opencli_bin: str, commands: list[CommandResult]) -> None:
    smoke_commands = [
        [opencli_bin, "youtube", "search", "Forza Horizon 6 fastest car", "--limit", "3", "-f", "json"],
        [opencli_bin, "youtube", "video", DEFAULT_YOUTUBE_VIDEO_URL, "-f", "json"],
        [opencli_bin, "youtube", "comments", DEFAULT_YOUTUBE_VIDEO_URL, "--limit", "3", "-f", "json"],
        [opencli_bin, "bilibili", "search", "地平线6 最强车", "--limit", "3", "-f", "json"],
        [opencli_bin, "bilibili", "video", DEFAULT_BILIBILI_BVID, "-f", "json"],
        [opencli_bin, "bilibili", "comments", DEFAULT_BILIBILI_BVID, "--limit", "3", "-f", "json"],
        [opencli_bin, "web", "read", "--url", DEFAULT_WEB_READ_URL, "-f", "md"],
    ]
    for args in smoke_commands:
        commands.append(run_command(args, cwd=repo_root, timeout=180))


def render_markdown_report(report: ToolingReport) -> str:
    lines = [
        "# Tool Readiness Log",
        "",
        f"- Generated at: `{report.generated_at}`",
        f"- opencli version: `{report.opencli_version or 'unknown'}`",
        f"- latest npm opencli: `{report.opencli_latest or 'unknown'}`",
        f"- yt-dlp version: `{report.yt_dlp_version or 'unknown'}`",
        f"- doctor ok: `{report.doctor_ok}`",
        f"- transcript ok: `{report.transcript_ok}`",
        "",
        "## Commands",
    ]
    for item in report.commands:
        lines.extend(
            [
                "",
                f"### `{item.command}`",
                f"- ok: `{item.ok}`",
                f"- return code: `{item.returncode}`",
            ]
        )
        if item.stdout:
            lines.append("- stdout:")
            lines.append("```text")
            lines.append(item.stdout[:4000])
            lines.append("```")
        if item.stderr:
            lines.append("- stderr:")
            lines.append("```text")
            lines.append(item.stderr[:4000])
            lines.append("```")

    if report.transcript:
        lines.extend(["", "## Transcript Capability", ""])
        lines.append(f"- ok: `{report.transcript.ok}`")
        lines.append(f"- method: `{report.transcript.method}`")
        if report.transcript.output_files:
            lines.append("- output files:")
            for path in report.transcript.output_files:
                lines.append(f"  - `{path}`")
        if report.transcript.error:
            lines.append(f"- error: `{report.transcript.error}`")

    if report.notes:
        lines.extend(["", "## Notes"])
        for note in report.notes:
            lines.append(f"- {note}")

    lines.append("")
    return "\n".join(lines)


def ensure_tooling_ready(
    *,
    repo_root: Path | None = None,
    run_dir: Path | None = None,
    update: bool = False,
    opencli_bin: str = "",
    yt_dlp_bin: str = "",
    run_network_tests: bool = True,
    transcript_url: str = DEFAULT_TRANSCRIPT_URL,
) -> ToolingReport:
    root = repo_root or repo_root_from_here()
    target_dir = run_dir or root / "workspace" / "memory" / "runs" / datetime.now().strftime("%Y-%m-%d-%H%M%S-opencli-tooling")
    target_dir.mkdir(parents=True, exist_ok=True)

    opencli = resolve_opencli_binary(opencli_bin)
    yt_dlp = resolve_yt_dlp_binary(yt_dlp_bin)
    npm = resolve_npm_binary()
    commands: list[CommandResult] = []
    notes: list[str] = []

    commands.append(run_command([opencli, "--version"], cwd=root, timeout=60))
    commands.append(run_command([npm, "view", "@jackwener/opencli", "version"], cwd=root, timeout=120))
    commands.append(run_command([yt_dlp, "--version"], cwd=root, timeout=60))

    if update:
        commands.append(run_command([npm, "install", "-g", "@jackwener/opencli@latest"], cwd=root, timeout=240))
        commands.append(run_command([yt_dlp, "-U"], cwd=root, timeout=240))
        opencli = resolve_opencli_binary(opencli_bin)
        yt_dlp = resolve_yt_dlp_binary(yt_dlp_bin)
        commands.append(run_command([opencli, "--version"], cwd=root, timeout=60))
        commands.append(run_command([yt_dlp, "--version"], cwd=root, timeout=60))

    opencli_version = ""
    yt_dlp_version = ""
    for item in commands:
        if item.command.endswith("--version") and "opencli" in item.command:
            opencli_version = first_line(item.stdout)
        if item.command.endswith("--version") and "yt-dlp" in item.command:
            yt_dlp_version = first_line(item.stdout)

    doctor_ok = ensure_browser_bridge(root, opencli, commands)
    transcript_result: TranscriptResult | None = None
    transcript_ok = False

    if run_network_tests and doctor_ok:
        run_smoke_tests(root, opencli, commands)
        transcript_result = fetch_youtube_transcript(
            transcript_url,
            target_dir / "transcripts",
            label="readiness-transcript",
            opencli_bin=opencli,
            yt_dlp_bin=yt_dlp,
            repo_root=root,
        )
        transcript_ok = transcript_result.ok
        if not transcript_ok:
            notes.append("YouTube transcript failed even after yt-dlp fallback. Research must mark video body unavailable.")
    elif not doctor_ok:
        notes.append("OpenCLI Browser Bridge is still unavailable; native opencli site adapters will fail.")

    report = ToolingReport(
        generated_at=datetime.now().isoformat(timespec="seconds"),
        opencli_version=opencli_version,
        opencli_latest=first_line(commands[1].stdout) if len(commands) > 1 else "",
        yt_dlp_version=yt_dlp_version,
        doctor_ok=doctor_ok,
        transcript_ok=transcript_ok,
        commands=commands,
        transcript=transcript_result,
        notes=notes,
    )
    (target_dir / "tool-readiness.json").write_text(
        json.dumps(asdict(report), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (target_dir / "tool-readiness.md").write_text(render_markdown_report(report), encoding="utf-8")
    return report


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Repair and verify OpenCLI research tooling.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ensure = subparsers.add_parser("ensure", help="Update, launch, and smoke-test OpenCLI tooling.")
    ensure.add_argument("--update", action="store_true", help="Update @jackwener/opencli and yt-dlp before testing.")
    ensure.add_argument("--run-dir", default="", help="Directory for tool-readiness logs.")
    ensure.add_argument("--opencli-bin", default="", help="Optional explicit opencli binary.")
    ensure.add_argument("--yt-dlp-bin", default="", help="Optional explicit yt-dlp binary.")
    ensure.add_argument("--skip-network-tests", action="store_true", help="Only verify version and Browser Bridge.")
    ensure.add_argument("--transcript-url", default=DEFAULT_TRANSCRIPT_URL, help="YouTube URL used for transcript test.")

    transcript = subparsers.add_parser("transcript", help="Fetch a YouTube transcript with opencli plus yt-dlp fallback.")
    transcript.add_argument("url", help="YouTube video URL or ID.")
    transcript.add_argument("--out-dir", default="", help="Output directory for transcript files.")
    transcript.add_argument("--label", default="", help="Output filename label.")
    transcript.add_argument("--opencli-bin", default="", help="Optional explicit opencli binary.")
    transcript.add_argument("--yt-dlp-bin", default="", help="Optional explicit yt-dlp binary.")
    transcript.add_argument("--langs", default=",".join(DEFAULT_TRANSCRIPT_LANGS), help="Comma-separated language order.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    root = repo_root_from_here()
    if args.command == "ensure":
        run_dir = Path(args.run_dir) if args.run_dir else None
        report = ensure_tooling_ready(
            repo_root=root,
            run_dir=run_dir,
            update=args.update,
            opencli_bin=args.opencli_bin,
            yt_dlp_bin=args.yt_dlp_bin,
            run_network_tests=not args.skip_network_tests,
            transcript_url=args.transcript_url,
        )
        print(f"Wrote tool readiness logs. doctor_ok={report.doctor_ok} transcript_ok={report.transcript_ok}")
        return 0 if report.doctor_ok and (args.skip_network_tests or report.transcript_ok) else 1

    out_dir = Path(args.out_dir) if args.out_dir else root / "workspace" / "memory" / "runs" / "manual-transcripts"
    languages = tuple(lang.strip() for lang in args.langs.split(",") if lang.strip())
    result = fetch_youtube_transcript(
        args.url,
        out_dir,
        label=args.label,
        opencli_bin=args.opencli_bin,
        yt_dlp_bin=args.yt_dlp_bin,
        repo_root=root,
        languages=languages,
    )
    print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
