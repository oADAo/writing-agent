# OpenCLI Tooling Workflow

這份流程用來避免研究任務在 `opencli`、Browser Bridge 或 YouTube 字幕失效時，偷偷降級成只看標題。

## Before Topic Research

先跑：

```powershell
python scripts/opencli_tooling.py ensure --update
```

這個指令會：

- 檢查並更新 `@jackwener/opencli`。
- 檢查並更新 `yt-dlp`。
- 重啟 opencli daemon。
- 用本機保存的 OpenCLI extension 啟動 Edge / Chrome Browser Bridge。
- 測試 `youtube search / video / comments`。
- 測試 `bilibili search / video / comments`。
- 測試 `web read`。
- 測試 YouTube 字幕擷取。

記錄會寫到：

```text
workspace/memory/runs/<timestamp>-opencli-tooling/
```

## Transcript Fallback

抓 YouTube 逐字稿時優先用：

```powershell
python scripts/opencli_tooling.py transcript "<YouTube URL>" --out-dir "<run-dir>\transcripts" --label "<source-label>"
```

流程順序：

1. `opencli youtube transcript --lang en`
2. `opencli youtube transcript --lang zh-Hant`
3. `opencli youtube transcript --lang zh-Hans`
4. `opencli youtube transcript --lang ja`
5. `opencli youtube transcript` auto mode
6. `yt-dlp --write-subs --write-auto-subs`

只要 `yt-dlp` 抓到字幕檔，就可以把影片內容納入研究證據。若這整串都失敗，研究包必須標註 `未能擷取逐字稿`，並降低該影片權重。

## Batch Research

`scripts/opencli_research.py` 預設會先跑工具 readiness check，並把記錄放進該次 run directory 的 `tool-readiness/`。

常用指令：

```powershell
python scripts/opencli_research.py topic <slug> --name-zh "<中文名>" --name-jp "<日文名>" --name-en "<英文名>" --breadth broad --repair-tools
```

如果只是跑單元測試或離線檢查，可以加：

```powershell
--skip-tool-readiness
```

研究任務不要使用這個 skip，除非使用者明確允許降級。
