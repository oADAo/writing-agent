# Platform Capture Playbook

## OpenCLI Preflight

Run:

```powershell
python scripts/opencli_tooling.py ensure --update --run-dir "<run-dir>\tool-readiness"
```

If this exits non-zero, inspect the readiness log and run smoke tests for the platforms needed. A wrapper false negative does not automatically mean every capture path is broken.

## Batch Search

Use the repo batch helper when the topic has a game name:

```powershell
python scripts/opencli_research.py topic <slug> --name-zh "<zh>" --name-jp "<jp>" --name-en "<en>" --breadth broad --limit 20 --run-dir "<run-dir>"
```

Use `--skip-tool-readiness` only after direct smoke tests prove the needed platform commands work, and record why.

## YouTube

Search first:

```powershell
opencli.cmd youtube search "<query>" --limit 20 -f json
```

Capture transcript with the helper:

```powershell
python scripts/opencli_tooling.py transcript "<YouTube URL>" --out-dir "<run-dir>\transcripts" --label "<source-label>"
```

Fallback order:

1. opencli transcript with target languages.
2. opencli auto transcript.
3. `yt-dlp --write-subs --write-auto-subs --convert-subs srt`.
4. Local audio transcription when necessary and allowed.
5. Description, pinned/top comments, or another high-signal video.

Capture comments separately. High-liked comments can upgrade or correct the transcript.

## Bilibili

Use:

```powershell
opencli.cmd bilibili search "<query>" --limit 20 -f json
opencli.cmd bilibili video "<BV_ID>" -f json
opencli.cmd bilibili comments "<BV_ID>" --limit 50 -f json
opencli.cmd bilibili subtitle "<BV_ID>" -f json
```

If subtitle returns empty, keep metadata and comments only. Do not treat the video speech as read.

## Reddit / Steam / Forums

Native Reddit search can be noisy. Prefer site search plus direct read:

```powershell
opencli.cmd google search "site:reddit.com/r/<subreddit> <game> <topic>" --limit 20 --lang en -f json
opencli.cmd reddit read "<reddit-url>" -f json
```

For Steam, Bahamut, and guide sites, use `opencli.cmd web read --url "<url>" -f markdown`. If URL query parameters confuse the command, save raw HTML with `curl.exe -L` and also try web read/browser read.

## Shorts Platforms

Only count YouTube Shorts when the URL contains `/shorts/`. For TikTok/Reels/Bilibili, save title, description, visible comments, subtitles/OCR when possible, view snapshot, post date, observed hook, observed punch, visual format, and evidence file.

Record observed hook/punch as what appears in the captured short, not as a recommendation for the writing project.
