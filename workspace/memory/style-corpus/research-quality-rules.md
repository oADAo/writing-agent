# 玫玫物語研究品質硬規則

更新日期：2026-05-29

使用者明確要求：以後任何研究都要做真正的研究，不可以只做搜尋結果或表面功夫。

## 永久規則

- YouTube 搜尋結果只能當候選線索，不能當作已研究證據。
- 只有實際點進影片、抓到字幕 / 自動字幕 / 描述 / 留言，或完成音訊轉錄，才可以把該影片列為研究依據。
- 如果影片抓不到字幕、逐字稿或音訊內容，必須標記「YT 字幕不足」或「未能擷取內容」，並降低權重。
- 網站、新聞、論壇、攻略頁必須讀正文；搜尋摘要和標題不能支撐文案結論。
- 每個寫進文稿的「最厲害的地方 / 值得期待點」都要能回推到至少一個實際讀到的來源內容。
- 官方來源只確認基本事實；玩家是否在意、疑慮和期待，要用社群、留言、論壇、試玩心得或媒體 hands-on 補強。
- 交付前自檢：每款遊戲是否有實際讀到的正文或字幕內容；沒有就不可寫成高信心結論。

## 不合格做法

- 只跑 `opencli youtube search` 或一般搜尋後就開始寫。
- 只看影片標題、縮圖、觀看數，就推論影片內容。
- 沒有讀正文，卻把新聞摘要當作已查證。
- 把官方行銷詞直接改寫成推薦理由。

## 2026-05-28 研究方法沉澱

本節從近期有效研究 run 回收可重用流程，目標是讓不同遊戲的新對話不要重新摸索工具，而是直接沿用已驗證的方法。

### 有效起手流程

- 每次進入熱門題目、買前研究、新手攻略或月份推薦研究前，先跑 `python scripts/opencli_tooling.py ensure --update --run-dir <run-dir>`。如果一開始 `Browser Bridge` 斷線，不要降級；先讓工具重啟 daemon 並開 Edge extension，直到 `doctor ok: True`、`transcript ok: True`。
- run 目錄要固定保留 `tool-readiness.md`、`tool-readiness.json`、`query-log.md` 或 `query-log-reviewed.md`。後續寫稿時不能只引用最終研究包，要能回到這些證據檔。
- 批次研究優先用 `scripts/opencli_research.py topic ... --breadth broad` 或 `shorts-topic ... --breadth broad` 起手；使用者要求越廣越好時才升到 `--breadth max`。批次結果要再人工分簇，不可直接把搜尋 hit 當結論。
- 查詢要先做中文、日文、英文名稱表，再用各語圈原生關鍵字查。例如 FH6 的中文 `地平线6 调校 / 过弯`、日文 `フォルツァ ホライゾン 6 チューニング / 初心者`、英文 `Forza Horizon 6 tuning guide / handling settings` 各自找到不同證據。

### 影片與字幕流程

- YouTube 高訊號影片先用 `python scripts/opencli_tooling.py transcript "<url>" --out-dir "<run-dir>\\transcripts" --label "<source-label>"`。可接受證據包括 `.srt`、`.vtt`、`.txt`、`.json`、`.tsv`，但研究包要標示來源層級。
- 如果 `opencli youtube transcript` 失敗，但 `yt-dlp --write-subs --write-auto-subs` 成功，仍可納入研究；證據要寫成 `yt-dlp subtitles fallback 成功`，不要假裝是人工聽完。
- 如果 YouTube 影片完全抓不到字幕或音訊，就只能用 metadata、描述、留言與其他正文來源交叉佐證，並在研究包標示 `未能擷取逐字稿`、降低權重。
- B 站原生 subtitle / summary 常會回 `AUTH_REQUIRED`。有效替代流程是：保留 `bilibili video / comments` JSON，必要時下載音訊做本地 Whisper 轉錄；tiny 轉錄只用來確認影片主題結構，不採細節數字為硬事實。
- 留言本身是研究證據，但只能支撐「玩家在意什麼 / 擔心什麼 / 怎麼命名問題」，不能單獨證明玩法或數值。

### 站外正文與社群流程

- Google / site search 只能當入口。納入主結論前，要用 `opencli web read` 讀官方頁、商店頁、新聞、攻略站、論壇或 Steam / Reddit 討論正文。
- Steam / Reddit 搜尋容易混入無關高分貼；只看搜尋結果會誤判。必須打開具體討論串，確認正文和回覆真的在講該遊戲、該問題，再納入。
- 站外來源至少分成兩類，例如 `論壇 / 社群` 加 `攻略站 / wiki`。FH6 有效組合是 YouTube + bilibili + Steam discussion + Reddit guide + TheGamer / GamesRadar 正文；007 有效組合是 YouTube 字幕 + 巴哈 / GNN + Reddit / Steam Community + 多語媒體試玩正文。
- 對發售前或媒體試玩資料，要把 `官方確認`、`媒體試玩`、`玩家留言`、`研究推論` 分開寫。不要把媒體轉述或創作者說法升級成官方定案。

### 研究包厚度標準

- 合格研究包不是結論表。至少要包含：工具預檢、Query Log、來源重點對照表、已確認事實、玩家在意點、風險和不要講死、逐項研究卡、可直接改寫口播句、B-roll 建議、需要實機驗證。
- 每個推薦章節或主題都要有「觀眾問題 -> 可用證據 -> 可講判斷 -> 不要講死 -> 可用口播句」。這比只列 `章節名 + 重點` 更能支援後續寫稿。
- 如果使用者後續要交給 Claude Code 寫稿，研究包應另外附 `Claude Code 撰寫提示詞` 或 `寫稿卡`，但必須放在資料之後，不能取代資料。

### 近期證據樣板

- `workspace/memory/runs/20260524-110709-007-first-light-buy-before-research/query-log-reviewed.md` 是買前研究包樣板：先通過 opencli readiness，再把官方 / 商店 / YouTube 字幕 / bilibili 降權 / 媒體正文 / 社群留言分表記錄。
- `workspace/deliverables/research/2026-05-24-007-first-light-buy-before-research.md` 是高密度買前研究包樣板：保留事實、玩法、玩家疑慮、章節池、B-roll、來源對照與禁講點。
- `workspace/memory/runs/20260522-195540-topic-forza-horizon-6-next-guide/` 是攻略題目研究樣板：結合三語圈 YouTube、B 站、Steam / Reddit、攻略站正文、YouTube 字幕與 B 站本地轉錄，最後才推 Top 1。
- `workspace/memory/runs/20260527-161955-007-youtube-mEsA9jAWcpQ-review/` 證明單支 YouTube 影片也應保留 metadata、留言、音訊、轉錄文字與字幕檔，方便後續回看「觀眾怎麼反應」和「影片實際講了什麼」。

## 2026-05-29 補充規則：從 Elliot 與 007 run 回收的研究維護點

### 三語圈高訊號來源怎麼找

- 買前與攻略研究的起手，不要只搜遊戲名本身；要直接把玩家判斷詞帶進三語圈關鍵字。近期有效組合是：
  - 中文：`買前 / 值不值得 / 試玩 / 難度 / 前期 / 夥伴太吵 / 優化`
  - 日文：`買うべきか / 体験版 感想 / 期待と不安 / 難易度 / 序盤 / 金策`
  - 英文：`before you buy / demo impressions / review / difficulty / early route / performance`
- 日文圈常能更早補到系統拆解與玩家操作感，英文圈常補媒體 hands-on 與 PC 風險，中文圈常補巴哈 / B 站留言裡真正會影響台灣觀眾點擊與收看的說法。不要讓三語圈做重複工。
- 先用 YouTube / B 站找題型與玩家語言，再用攻略站、論壇、Steam / Reddit、官方頁把細節補滿。最近有效樣板：
  - Elliot：`youtube-ja-demo-impressions.yaml` + Steam 登入補查 + 巴哈 Demo 心得 + Gamerch 難度頁
  - 007：`query-log-reviewed.md` 裡的官方 / 商店 / YouTube 字幕 / Reddit / Steam Community 分層

### opencli 與 query log 的保留方式

- `opencli` 查詢原始結果要保留，但原始 YAML / JSON 不能取代 reviewed log。像 Elliot run 只有 `opencli/*.yaml` 和補查頁面時，後續代理仍要重新猜哪些命中真的被採用。
- 最低合格形態應同時有：
  - `tool-readiness.md`
  - `query-log.md` 或 `query-log-reviewed.md`
  - `sources.md` 或等價來源對照
  - 最終交付物或 game memory 的採用結論
- 如果 run 內只有 `opencli web read` 的保存回條，例如 `Steam Deck performance.md`、`demo簡易心得.md` 這種只記錄 saved path 的檔案，不算完成的正文沉澱；同一輪必須再把真正讀到的重點抄回研究包或 game memory。

### YouTube / bilibili / forum / guide 的深讀規則

- YouTube 可分三層保存：搜尋命中、字幕 / 逐字稿、留言。缺任一層時要明寫降權原因。
- bilibili 若 `subtitle / summary` 卡在 `AUTH_REQUIRED`，不要只停在留言或標題；至少保留：
  - `video` metadata
  - `comments`
  - 需要時的音訊 / 本地轉錄
  - 在 reviewed log 裡標示「只能支撐玩家反應或影片主題，不支撐細節數字」
- 論壇、Steam Community、巴哈、Reddit 的 `web read` 若只留下保存回條，後面一定要把正文要點整理成：
  - 玩家在意什麼
  - 反覆吵什麼
  - 哪些點只能當社群情緒，哪些能變成章節或風險
- 攻略站 / wiki / 難度頁適合補系統表格，但要標示來源層級。像 Elliot 的 Gamerch 難度頁可以支撐「差異項目有哪些」，不能直接當繁中 UI 或正式版最終規則。

### 使用者 Demo / 手動補證如何沉澱

- 如果使用者後續自己玩了 Demo，這種資訊不是備註，而是新約束。應像 Elliot run 一樣單獨放 `user-demo-supplement-<date>/`，再同步把必講點回寫到 game memory。
- 使用者 Demo 補證最常影響三件事：
  - 章節優先順序
  - 哪些系統一定要講
  - 哪些官方 / 社群說法要改成待實機確認
- 補證後不能只更新 deliverable，還要更新 `workspace/memory/games/<slug>/...`，避免下一輪又把舊結論講回去。

### Dense research pack 的最低厚度再補強

- 高密度研究包不只要有 `來源重點對照表`，還要能看出「哪段證據是登入後補查才拿到的」。像 Elliot 的 Steam / 巴哈補查，直接改變了章節優先順序，這種變化要在研究包裡明寫，不要藏在 run 資料夾。
- 每輪如果有高價值補查，最好加一個小節說明：
  - 補查前原本怎麼判斷
  - 補查後哪個章節或風險升級 / 降級
  - 哪些點仍待實機確認
- 研究包若最後沒有獨立 `Query Log` 小節，至少要能讓讀者沿著表格回推到具體指令與命中，不然後續寫稿很難驗證。

### 目前確認的 gap

- `workspace/memory/runs/20260528-172755-elliot-buy-before-research/` 原始證據很多，但缺少 `query-log-reviewed.md` 與 `sources.md` 這類整合層。未來看到這種 run，要先補整合層，再把它當成熟樣板。
- 單純保存 `web read` 的回條檔，若沒再寫進 game memory 或研究包，後續可復用性太低。這種做法應視為未完成的沉澱，不是正式完成。

## 2026-05-30 Maintenance Pass

### Reusable methods confirmed from recent 007 + Elliot + tooling runs

- Start multi-language topic research with native keyword families instead of literal translation.
  - zh-TW / zh-CN: `買前 / 買前必看 / 試玩 / 評價 / 難度 / 實機 / 新手 / 前期`
  - ja: `体験版 / 先行プレイ / レビュー / 難易度 / 序盤 / ビルド / 評価`
  - en: `before you buy / demo impressions / review / difficulty / early route / performance / hands-on`
- For demo-heavy or prelaunch games, JP and EN hands-on coverage usually explains systems better than CN metadata alone. Pair that with Taiwan community threads, Steam discussions, and Reddit so the pack stays useful for Maymei audience fit and risk framing.
- Run `python scripts/opencli_tooling.py ensure --update --run-dir <run-dir>` before deeper research and keep `tool-readiness.md` plus `tool-readiness.json` in the run folder. The readiness artifact is part of the evidence chain, not optional cleanup.
- Treat raw `opencli` YAML / JSON as collection artifacts only. They become durable only after the findings are rewritten into `query-log-reviewed.md`, `sources.md`, game memory, or the main research pack.
- Use `python scripts/opencli_tooling.py transcript "<url>" --out-dir "<run-dir>\\transcripts" --label "<source-label>"` as the default YouTube capture path.
  - If transcript capture still fails, keep the source at reduced weight and explicitly mark `metadata/comments only` or `未能擷取逐字稿`.
- For bilibili, `AUTH_REQUIRED` on subtitle / summary is a source-weight warning, not a stop condition.
  - Keep using `bilibili video` and `bilibili comments`.
  - If audio or outside capture is available, convert that into text.
  - Do not promote bilibili AI summary alone into a main conclusion.
- `opencli web read` receipts are not deep-read memory by themselves. The saved markdown path proves retrieval, but the durable layer is the human-readable extraction of what the page said, what player concern or system detail it supports, and where it should affect topic choice, chapter framing, or risk notes.
- Login supplements and demo supplements must be promoted in the same pass when they change chapter framing.
  - `login-supplement/` is for community friction, performance, price, and PC risk.
  - `user-demo-supplement-<date>/` is for demo-verified system wording, difficulty, or player expectation shifts.
  - Neither should stay stranded as side receipts once they materially change the research judgement.
- Dense research packages stay writer-useful when each main source carries four things: concrete finding, source weight, player-facing phrasing, and overclaim risk. Recent 007 and Elliot runs also showed that B-roll cues and transcript status per source save later script-writing time.

### Failed or lower-value patterns reinforced by this pass

- Do not leave a strong run with only `opencli/*.yaml`, transcript files, and saved page markdown. That shape is expensive to reuse and easy for later agents to misread.
- Do not treat `web read` success as proof the content was absorbed. If the page findings are not copied into `sources.md`, the pack, or game memory, the research is still shallow for future reuse.
- Do not rely on bilibili title / metadata / AI summary alone for a major conclusion when subtitle capture failed.
- Do not collapse demo findings into a generic topic note. Put them where later buy-before or beginner-guide writing will actually look first.

### Current gap report

- `workspace/memory/runs/20260528-172755-elliot-buy-before-research/` still lacks `query-log-reviewed.md` and `sources.md`.
- That run already has strong raw evidence across `opencli/*.yaml`, `transcripts/`, `login-supplement/`, and `user-demo-supplement-20260528/`.
- Next maintenance pass should consolidate those artifacts into durable reviewed logs before adding more Elliot research.

## 2026-06-15 Maintenance Pass

### Reusable methods confirmed from recent Dave + Ocarina + tooling runs

- Community-only follow-up runs are worth doing after the main pack when the open question is title/hook framing rather than new gameplay facts.
  - Good inputs: PTT, Bahamut, Reddit, YouTube comments, bilibili comments.
  - Output shape: one focused note that states what audience tension or title signal the comments actually reveal.
  - Weight rule: use these for buyer-fit, fear, hype, title pressure, or wording fit; do not upgrade them into gameplay/system fact.
- Reusing prior captured evidence is valid when a later writing pack needs the same transcript or comment body.
  - Copy the reused artifacts into a clearly named folder such as `source-originals/previous-run-reuse/`.
  - Preserve the original run path in the new pack so later agents can trace provenance instead of assuming it was freshly captured.
- If the latest official YouTube video partially breaks one transcript path, keep both capture attempts when they add value.
  - Example pattern: direct `opencli youtube transcript --lang en -f yaml` succeeds for the newest official video, while `scripts/opencli_tooling.py transcript` only saves a fallback language markdown.
  - In that case, keep the English YAML as primary text, keep the fallback transcript as backup context, and document the mismatch explicitly.
- Tool-readiness headers are not always the final truth.
  - Recent runs showed `doctor_ok=False` / `transcript_ok=False` in the summary even when the embedded `opencli doctor` blocks showed the extension connected and some research actions succeeded.
  - When the summary booleans and the command logs disagree, trust the command-by-command evidence and write a manual note about what was actually usable.
- Some official or historical text sources will remain low-weight even after extra effort.
  - Image-only PDFs with empty text extraction and Cloudflare-blocked text dumps should be logged as failed attempts, then replaced with official pages, creator transcripts, and comment bodies that are actually readable.
  - Keep the failed artifact path so later agents do not waste time retrying the same dead end.
- Dense writer-facing packs stay useful when they carry explicit next-query targets, not only current evidence.
  - Good examples: exact launch-day checks, first-hour playthrough transcript capture, store-price follow-up, and forum/review re-checks with dates.
  - This turns the pack into a live continuation point instead of a frozen summary.

### Failed or lower-value patterns reinforced by this pass

- Do not treat a broken forum正文 capture as total forum failure if readable comment bodies were still captured elsewhere in the same language market.
- Do not hide reused evidence provenance. If a transcript/comment set came from a prior run, label it as reuse in the new package.
- Do not trust only the top-level readiness booleans when the raw `opencli doctor` output says something else.
- Do not keep chasing image-only PDF or Cloudflare-blocked text sources once official readable substitutes already cover the same claim at higher quality.

## 2026-06-16 Maintenance Pass

### Reusable methods confirmed from recent Gagabird + Palworld + tooling runs

- When comparing two possible topics, inspect search-intent quality, not only whether results exist.
  - If one query family yields dense攻略/新手/資源正文 and the other drifts into 代儲、儲值教學、交易站、App Store IAP lists, treat the polluted cluster as weak natural-topic demand even if it still returns many hits.
  - Preserve that pollution evidence in `query-log-reviewed.md` so later agents can see why the topic was rejected.
- Reuse within the same topic family is valid when the new run makes the dependency explicit.
  - Acceptable patterns: copy the earlier successful source into the new run, or reference the earlier run path directly from `sources.md`.
  - Silent reuse is not acceptable; later agents need to know which evidence was fresh and which was inherited.
- Transcript success means readable text, not merely a created file.
  - If the transcript is mojibake, empty, or only available through a wrong-language auto-caption path that does not yield readable content, downgrade it to secondary/market-signal use.
  - Keep the broken artifact path for auditability, but do not quote it as creator evidence.
- Noisy adjacent queries are useful for exclusion.
  - If `guild / arena / daily` follow-up queries mostly surface other games, site shells, or dead pages, use that as evidence to exclude those subtopics from the final daily list.
  - This is better than padding the research pack with unsupported chapter claims.
- Comment capture should become a file when it affects the conclusion.
  - Chat-visible `opencli youtube comments` output is enough for same-turn note-taking, but not durable enough for later reuse.
  - If the comment materially supports buyer-fit, daily-task priority, or creator framing, persist it into the run folder before calling it package evidence.
- Keep updater/network failures separate from actual research-tool failure.
  - Recent tooling logs showed `yt-dlp -U` timing out while the installed `yt-dlp` version still existed and other capture steps remained usable.
  - Log the updater failure, but judge transcript readiness from the real capture commands and saved artifacts.

### Failed or lower-value patterns reinforced by this pass

- Do not treat commercial-intent search pollution as proof that a topic has healthy organic demand.
- Do not count a transcript file as usable evidence before checking that the text is readable in the needed language.
- Do not force weak guild/arena/social-system claims into a daily guide when the deeper capture stayed noisy.
- Do not leave comment evidence only in transient tool/chat output if the package may be reused later.
