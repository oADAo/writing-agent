# Research Source Acquisition Workflow

這份文件定義研究包撰寫前的「厚資料」蒐集方法。目的不是多抓網址，而是穩定抓到能保存、能回查、能支撐章節判斷的正文、字幕、逐字稿、留言與攻略內容。

適用於：

- 買前必看、攻略、新手開局、每日必做、資源效率、機制拆解。
- Shorts 題型研究中需要驗證熱門短影音是否真的有可複製觀眾反應。
- 任何需要先證明「大家真的覺得有用 / 有疑慮 / 有需求」的研究包。

## Evidence Standard

搜尋結果、影片標題、縮圖、觀看數、Google snippet、AI 摘要只能當線索。納入研究結論前，至少要取得其中一種可保存證據：

- YouTube / bilibili 字幕、逐字稿、本地轉錄。
- YouTube / bilibili 高讚留言、置頂留言、回覆數明顯的討論。
- Reddit、Steam Community、巴哈姆特、官方論壇、攻略站的正文。
- TikTok / Instagram / Reels 的標題、說明、字幕、留言正文或可 OCR 截圖。
- 官方頁、商店頁、新聞稿正文，僅用於事實校正。

每個來源都要保存原始輸出，並在 `sources.md` 或來源重點對照表中寫清楚：

- 讀到哪段正文、字幕或留言。
- 支撐哪個玩法、疑慮、需求、風險或章節判斷。
- 來源層級是官方確認、創作者實測、玩家回報、攻略站整理或研究推論。
- 原始檔路徑。

## Quality Gate

研究包開始寫章節前，先做資料厚度檢查。

長片攻略 / 買前必看最低門檻：

- `3` 支以上非官方創作者影片或同等玩家實測來源。
- 至少 `2` 支影片有字幕、逐字稿、本地轉錄或可用高訊號留言。
- 至少 `2` 種站外社群 / 攻略來源，例如 Reddit、Steam Community、巴哈姆特、bilibili、攻略站。
- 至少 `1` 份官方或商店正文，用來確認平台、版本、售價、更新、系統名稱。
- 每個核心章節至少 `2` 個來源支撐，其中至少 `1` 個不是官方來源。

攻略型內容加嚴：

- 效率數字必須標來源層級：`影片實測 / 留言回報 / 攻略站整理 / 本機尚未驗證`。
- 刷錢、刷經驗、掛機、宏、漏洞、可能被修正的方法，要另外標 `風險與避坑`。
- 如果只有影片標題或留言傳聞，不能寫成肯定攻略，只能列 `待實機驗證`。

高品質留言判定：

- 優先採用按熱門排序的留言，並保存 likes / votes、replies、author、time。
- 留言內容要有資訊量，例如補充步驟、指出錯誤、驗證可行性、提出常見失敗原因、說明誰適合或不適合。
- 純梗圖、純情緒、單句稱讚、無內容爭吵，只能當氣氛線索，不算研究證據。
- 高讚但內容與玩法無關時，不能用來支撐攻略結論。

## Language Coverage Targets

長片攻略、買前必看、系統拆解、資源效率研究，預設要同時查中文、英文、日文三個語圈。`中文 20 / 英文 20 / 日文 20` 不設為硬性可交付門檻，而是每個語圈的「候選搜尋與擷取嘗試目標」：能抓到就抓，抓不到要留下明確缺口，不可以為了湊數納入低品質來源。

數量定義：

- `候選來源`：搜尋命中的影片、討論串、攻略頁、評論頁或社群貼文。只有標題、snippet、觀看數或搜尋結果時，仍然只是候選。
- `可用來源`：已成功保存正文、字幕、逐字稿、高訊號留言、OCR 或本地轉錄，且內容能支撐玩法、疑慮、需求、流程或章節判斷。
- `主證據來源`：可用來源中，包含創作者實測、玩家實測、攻略流程、高讚補充留言、社群驗證或反例回報者。

厚資料目標：

- A 級厚資料：每個語圈至少搜尋或嘗試擷取 `20` 個候選來源，且每個語圈有 `10-20` 個可用來源。適合熱門遊戲、剛發售大作、攻略需求很強的題目。
- B 級可開寫：每個語圈至少完成 `20` 個候選搜尋或合理窮盡搜尋，且每個語圈至少有 `5-8` 個可用來源；三語合計至少 `18-24` 個可用來源，其中至少 `8` 個是主證據來源。
- C 級資料不足：任一語圈少於 `3` 個可用來源，或三語合計少於 `12` 個可用來源。這時可以交研究缺口報告或較薄研究包，但不能包裝成完整深度攻略研究。

降級規則：

- 冷門獨立遊戲、未上市 demo、只有單一語圈社群活躍、日文或中文官方名稱不明時，可以低於 20 個候選，但必須在 `language-source-matrix.md` 寫明搜尋詞、命中數、抓取失敗原因與替代來源。
- 如果英文資料很多、中文或日文資料少，不能直接用英文結論覆蓋中文 / 日文玩家需求；只能標成 `英文語圈回報`，並把缺口列入風險。
- 如果日文資料抓不到正文，但有高品質日文影片字幕或留言，仍可算日文可用來源。
- 如果只抓到官方日文新聞、商店頁或媒體通稿，不能當成日文玩家社群證據。

每個 run folder 要建立 `language-source-matrix.md`，至少記錄：

```text
Language: zh / en / ja
Native keywords:
Candidate hits reviewed:
Capture attempts:
Usable sources:
Primary evidence sources:
Failed captures:
Best source types:
Coverage judgment: A / B / C / gap
Notes:
```

## Capture Stack

### 1. Tool Readiness

正式研究前先跑：

```powershell
python scripts/opencli_tooling.py ensure --update --run-dir "<run-dir>\tool-readiness"
```

如果 readiness summary 顯示失敗，但 `opencli doctor` 內容實際顯示 daemon、extension、connectivity 都 OK，不能直接降級。要做直接 smoke test：

```powershell
opencli.cmd youtube search "<game> guide" --limit 3 -f json
opencli.cmd youtube comments "<youtube-url>" --limit 5 -f json
opencli.cmd web read --url "<article-or-forum-url>" --stdout true -f md
```

若 smoke test 成功，記錄為 `readiness wrapper false, direct commands usable`。若 Browser Bridge 斷線，先重啟 daemon 並重新打開 OpenCLI Browser Bridge profile。

### 2. YouTube Metadata

先用 opencli 找高訊號影片：

```powershell
opencli.cmd youtube search "<game> before you buy" --limit 20 -f json
opencli.cmd youtube search "<game> guide beginner tips" --limit 20 -f json
opencli.cmd youtube video "<youtube-url>" -f json
```

候選影片要記錄：

- 標題、頻道、URL、觀看數、發布時間、時長。
- 是否非官方創作者。
- 影片類型：before you buy / guide / review / hands-on / update / farming / build。
- 是否有字幕、逐字稿、說明欄、置頂留言或高讚留言。

### 3. YouTube Transcripts

逐字稿抓取優先順序：

1. `youtube-transcript-api`，適合快速抓公開字幕與自動字幕。
2. `scripts/opencli_tooling.py transcript`，保留現有 opencli + yt-dlp fallback 紀錄。
3. 直接 `yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs ... --convert-subs srt`。
4. 抓音訊後本地轉錄。
5. 改用影片說明、置頂留言、高讚留言、同主題其他影片。

保存位置：

```text
<run-dir>/transcripts/<source-label>.<method>.<lang>.md
<run-dir>/transcripts/<source-label>.<method>.<lang>.srt
```

如果 `opencli youtube transcript --lang <lang>` 回傳 `Caption URL returned empty response`，不要直接判定無字幕。先試 auto mode，再試 `yt-dlp`，再試 `youtube-transcript-api`。

### 4. YouTube Popular Comments

首選工具：

- `yt-comment-dl`：維護中的 `youtube-comment-downloader` fork，已實測可抓熱門留言、votes、replies、author、time。
- `youtube-comment-downloader`：上游專案，可抓 popular / recent，無需 YouTube API key。
- YouTube Data API `commentThreads.list`：有 API key 時最穩，支援 `order=relevance`，comment resource 有 `likeCount`。
- `opencli youtube comments`：作為快速 smoke test 或 fallback。
- `yt-dlp --write-comments`：適合和 infojson 同步保存，但留言量大時可能慢。

建議命令：

```powershell
yt-comment-dl "<youtube-url>" --sort 0 --limit 50 --pretty --output "<run-dir>\source-originals\youtube-comments\<label>.popular.json"
opencli.cmd youtube comments "<youtube-url>" --limit 20 -f json
```

整理時建立 `creator-video-evidence.md`：

```text
Video: <title>
Transcript: <path or failed>
Popular comments: <path>
Useful comment signals:
- <votes> likes / <replies> replies: <comment summary>
- <votes> likes / <replies> replies: <comment summary>
Research use:
- Supports: <chapter / risk / player demand>
- Not enough for: <unsupported claim>
```

### 5. Community Guides And Reviews

優先抓可保存正文的社群頁。

Reddit：

```powershell
opencli.cmd reddit search "<game> tips" --limit 10 -f json
opencli.cmd reddit read "<post-id-or-url>" --sort top --limit 25 --depth 2 --replies 5 -f json
```

Steam Community：

```powershell
opencli.cmd google search "site:steamcommunity.com/app <game> guide discussion" --limit 10 -f json
opencli.cmd web read --url "<steam-discussion-or-guide-url>" --stdout true --wait 5 --wait-until networkidle -f md
```

巴哈姆特：

```powershell
opencli.cmd google search "site:forum.gamer.com.tw <game> 攻略 巴哈" --limit 10 --lang zh-TW -f json
```

巴哈 URL 常有 `&`，在 Windows `.cmd` wrapper 下要轉義或改用 `cmd /c` 雙引號。抓完要確認輸出標題與原文連結是目標串，不是板首頁。

bilibili：

```powershell
opencli.cmd bilibili search "<game> 攻略" --limit 10 -f json
opencli.cmd bilibili video "<bvid>" -f json
opencli.cmd bilibili comments "<bvid>" --limit 30 -f json
opencli.cmd bilibili subtitle "<bvid>" -f json
```

若 subtitle 回 `AUTH_REQUIRED`，改用留言、說明、彈幕、同主題其他影片或登入後工具；不得把無字幕影片當主證據。

### 6. Three-Language Query Batches

每個攻略研究至少建立三語查詢批次。先確認官方英文名、中文名、日文名；如果日文名或中文名未確認，要把查詢使用的別名標成 `unconfirmed alias`。

中文查詢：

```powershell
opencli.cmd youtube search "<中文名或英文名> 攻略 新手 前期" --limit 20 -f json
opencli.cmd bilibili search "<中文名或英文名> 攻略 新手 前期" --limit 20 -f json
opencli.cmd google search "site:forum.gamer.com.tw <中文名或英文名> 攻略" --limit 20 --lang zh-TW -f json
opencli.cmd google search "<中文名或英文名> 攻略 巴哈 Steam 評價 新手" --limit 20 --lang zh-TW -f json
```

英文查詢：

```powershell
opencli.cmd youtube search "<English title> beginner guide tips before you buy" --limit 20 -f json
opencli.cmd youtube search "<English title> farming build best settings review" --limit 20 -f json
opencli.cmd reddit search "<English title> beginner guide tips" --limit 20 -f json
opencli.cmd google search "site:steamcommunity.com/app <English title> guide tips discussion" --limit 20 -f json
opencli.cmd google search "<English title> guide tips review walkthrough" --limit 20 -f json
```

日文查詢：

```powershell
opencli.cmd youtube search "<Japanese title or English title> 攻略 初心者 序盤" --limit 20 -f json
opencli.cmd youtube search "<Japanese title or English title> おすすめ 稼ぎ 金策 レビュー 評価" --limit 20 -f json
opencli.cmd google search "<Japanese title or English title> 攻略 初心者 序盤 おすすめ" --limit 20 --lang ja -f json
opencli.cmd google search "<Japanese title or English title> wiki 攻略 掲示板 評価" --limit 20 --lang ja -f json
```

三語批次完成後，不能只回報命中數。要回報每個語圈實際抓到多少可用來源、多少主證據來源、多少失敗擷取，以及是否達到 A / B / C 覆蓋等級。

## Tool Recommendations

Snapshot date: 2026-06-17.

| Priority | Tool / project | Use | Why | Caveat |
| --- | --- | --- | --- | --- |
| A | `yt-dlp/yt-dlp` | subtitles, metadata, comments fallback | Large active project, supports thousands of sites, direct subtitle flags and `--write-comments` | Comment capture can be slow; infojson needs post-processing |
| A | `youssefadly237/yt-comment-dl` | YouTube popular comments | Maintained fork, simple JSON output, tested locally | Small project; keep `youtube-comment-downloader` upstream as fallback |
| A | `egbertbouman/youtube-comment-downloader` | YouTube popular / recent comments | Mature no-API comment scraper with popular sort | Platform changes can break it; verify per run |
| A | `jdepoix/youtube-transcript-api` | YouTube transcripts | Fast API, no browser, no API key, tested locally | YouTube bot protection can break some environments; keep yt-dlp fallback |
| A | YouTube Data API | official comments | Stable official route, relevance order, `likeCount`, pagination | Needs API key and quota; captions for non-owned videos are not generally solved by Data API |
| B | `Nemo2011/bilibili-api` | B 站 API, comments, video info, subtitles | Active Python library, broad B 站 coverage | GPL-3.0; B 站 anti-bot and login state still matter |
| B | `HamsteRider-m/bilibili-subtitle` | B 站 subtitles via BBDown | Purpose-built subtitle extractor with login preflight | Small project; use as reference unless repeated tests pass |
| B | `instaloader/instaloader` | Instagram captions/comments/metadata | Mature project, supports comments and captions | Comments often require login; IG rate limits are common |
| C | `davidteather/TikTok-Api` | TikTok metadata/search/user data | Popular unofficial TikTok wrapper | TikTok changes frequently; comments are historically brittle |
| C | `HasData/tiktok-scraping` | TikTok Playwright/network examples | Useful reference for capturing internal API responses | Example repo, not a durable dependency by itself |

## Source Status Labels

Use these labels in `query-log-reviewed.md` and `sources.md`:

- `accepted-primary`: transcript,正文, or high-signal comments directly support a conclusion.
- `accepted-supporting`: useful context, but not enough alone.
- `candidate-only`: title, metadata, search result, short description, or unread page.
- `failed-capture`: source found but正文 / 字幕 / 留言抓不到.
- `rejected-low-signal`: captured but only memes, empty text, duplicated snippets, or irrelevant discussion.
- `needs-in-game-verification`: plausible guide step or efficiency claim that has not been tested locally.

## Pre-Writing Checklist

Before drafting a research report or writer handoff:

- `tool-readiness/` exists, or direct smoke-test logs explain why readiness wrapper is unreliable.
- `language-source-matrix.md` records zh / en / ja candidate counts, usable-source counts, primary-evidence counts, failed captures, and A / B / C coverage judgment.
- `query-log-reviewed.md` records every platform, keyword, command, hit, and inclusion decision.
- `sources.md` maps each accepted source to supported conclusions.
- `creator-video-evidence.md` has transcripts or useful popular comments for each included creator video.
- `source-originals/` contains raw JSON / Markdown / OCR / transcript files.
- Every chapter research card has source paths, not just links.
- Every source with only title/snippet is marked `candidate-only`.
- Every failed transcript/comment/page read has a fallback attempt or a stated limitation.
- If any language has fewer than `5` usable sources, the report explicitly labels that language as thin coverage and avoids treating that market as proven.

If the checklist fails, the research is not ready for final writing. Write a gap report or continue source capture.
