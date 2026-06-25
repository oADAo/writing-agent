# 玫玫物語研究品質硬規則

更新日期：2026-06-22

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

## 2026-06-17 Maintenance Pass

### Reusable methods confirmed from recent Elliot prelaunch chapter-pool + six-chapter deep-dive runs

- When `opencli` search succeeds but later `web read`, YouTube, bilibili, or Reddit adapters break because Browser Bridge drops, keep the run alive with a hybrid capture chain instead of treating the whole pass as failed.
  - Discovery layer: preserve the successful `opencli google search` / `youtube search` command and raw result file in `query-log-reviewed.md`.
  - Body-capture layer: pivot to browser/web tooling for readable正文 and save the raw page locally as HTML.
  - Audit layer: record the pivot explicitly in `sources.md` so later agents know which sources came from native opencli capture and which came from fallback body capture.
- Prelaunch guide research is strongest when three evidence layers stay separate instead of being flattened together.
  - Japanese guide sites define the candidate system/chapter buckets.
  - Traditional Chinese official pages, Bahamut, and Taiwan media translate those systems into Maymei audience wording and pain points.
  - Creator transcripts explain what other people actually spend time teaching, repeating, or warning about.
  - Do not let any single layer pretend to cover all three jobs.
- Subtitle failure needs a three-way classification, not a single `transcript failed` bucket.
  - `No subtitles available`: lower the source weight now and only restore it if later local transcription or comments add usable text.
  - `HTTP 429 / temporary fetch block`: keep it as a scheduled retry target; this is a capture problem, not proof the video is low-value.
  - `BROWSER_CONNECT / bridge drop after search`: preserve the search hit, then move capture to another channel instead of erasing the source from the run history.
- Candidate-only / prewriting packs should explicitly protect writer freedom when the user has buckets but has not locked final chapter order.
  - Add a short boundary note that the pack is a material warehouse, not a final structure.
  - Keep phrases like `素材桶`, `候選`, `可合併`, `可重排`, and avoid accidental finality language.
  - This prevents later writing turns from mistaking research grouping for a user-approved sequence.
- Player-reported farming numbers can be useful, but only when the package keeps the source layer and verification debt visible at the same time.
  - Acceptable use: cite Bahamut / Reddit / creator claims as `玩家回報` or `創作者實測線索`.
  - Required companion: add a matching `Needs in-game verification` item for the same number or route.
  - Do not upgrade prelaunch player numbers into tutorial certainty just because multiple players repeat them.

### Failed or lower-value patterns reinforced by this pass

- Do not discard a whole run as unusable merely because Browser Bridge died after the discovery phase; the fallback body-capture path is still durable if it is logged clearly.
- Do not let Japanese guide-site density silently overwrite Taiwan audience-fit evidence; chapter usefulness and local wording are not the same question.
- Do not collapse `no subtitles`, `HTTP 429`, and `BROWSER_CONNECT` into one generic transcript failure label.
- Do not present research grouping buckets as if they were already the user's locked final chapter order.

## 2026-06-18 Maintenance Pass

### Reusable methods confirmed from recent Palworld + 嘎嘎奇兵 + crawler/tooling runs

- Treat tool readiness as a chronological evidence chain, not a single boolean verdict.
  - First record the wrapper header result from `tool-readiness.md`.
  - Then read the later `opencli doctor`, smoke-test, and transcript blocks in order.
  - If the header says `doctor_ok=False` / `transcript_ok=False` but later command blocks show the extension connected and searches succeeding, mark the run as `wrapper false negative after recovery` instead of treating the whole toolchain as dead.
- The currently verified Browser Bridge recovery path is still:
  - `opencli.cmd daemon restart`
  - relaunch the saved OpenCLI Browser Bridge Edge profile
  - re-run `opencli.cmd doctor` until `Extension: connected` and `Connectivity: connected`
  - keep those doctor blocks in the run folder as the real readiness proof
- Recent local tool evaluation confirms a more explicit YouTube capture stack.
  - First-choice transcript probe: `youtube-transcript-api`
  - Default repo helper: `python scripts/opencli_tooling.py transcript "<url>" --out-dir "<run-dir>\\transcripts" --label "<label>"`
  - Subtitle fallback: direct `yt-dlp --write-subs --write-auto-subs`
  - Popular comments first choice: `yt-comment-dl`
  - `opencli youtube comments` remains useful as smoke test or secondary fallback, but high-value comment evidence should be persisted to file.
- Reddit discovery should stay split from Reddit evidence capture.
  - If native `opencli reddit search` is noisy or polluted, switch to `opencli google search "site:reddit.com <game> <topic>"`, then deep-read the exact thread.
  - Only the saved Reddit正文 / replies count as evidence; the noisy native search result should be logged as a discovery failure, not promoted into source coverage.
- Bilibili subtitle failures now need two separate downgrade labels.
  - `AUTH_REQUIRED`: keep `video` metadata and comments, then look for logged-in subtitle tools or outside audio transcription.
  - `EMPTY_RESULT`: keep metadata and comments only; do not pretend the spoken guide content was captured.
  - In both cases, bilibili comments can support player demand or version warnings, but not the creator's exact spoken steps unless text/audio capture exists.
- Windows URL handling remains a real evidence-risk point.
  - URLs containing `&` or query parameters can be split by the `.cmd` wrapper, especially for Bahamut, Google Play, and some Steam / Mobile01 pages.
  - After every escaped `web read`, verify the output title and original URL are the intended page, not a shell page or site homepage.
- Dense research packs are more reusable when they preserve the gap between candidate volume and validated evidence volume.
  - Keep candidate counts in the reviewed log.
  - Keep validated-source counts in `sources.md`.
  - Add `language-source-matrix.md` whenever the run claims three-language coverage or A/B/C coverage judgment.
  - If the matrix is missing, treat language coverage as incomplete documentation rather than silently assuming it was done.
- Guide/exception-topic research should keep source-family limits visible.
  - Recent 嘎嘎奇兵 research had strong official/store and guide-site coverage, but weak Japanese / bilibili / creator-transcript depth.
  - That shape is still usable for a locked practical guide, but the report must say the community layer is thin instead of implying full three-market validation.

### Failed or lower-value patterns reinforced by this pass

- Do not trust the top header or final note in `tool-readiness.md` more than the command-by-command blocks beneath it.
- Do not count bilibili metadata + comments as if they were creator transcript evidence when subtitle capture returned `AUTH_REQUIRED` or `EMPTY_RESULT`.
- Do not claim three-language coverage only because three-language searches were attempted; coverage is proven by saved usable sources and, ideally, `language-source-matrix.md`.
- Do not let successful local tool evaluation stay stranded in a side run; promote proven tools like `yt-comment-dl` and `youtube-transcript-api` into the main method memory layer.

## 2026-06-19 Maintenance Pass

### Reusable methods confirmed from the Elliot postlaunch beginner-guide run

- `今天 / 凌晨後 / 最新` 類研究要先鎖定明確時區 cutoff，再做專門的 `today-only` 補查層。
  - 這次有效做法是先定 `2026-06-18 00:00 +08:00`，再把納入與排除來源都寫進獨立檔。
  - 不要只看 YouTube `upload_date`、平台上的 `today` 標籤，或英文站點的當地時區時間。
  - 即使來源本身很強，只要台灣時間落在 cutoff 之前，也要明寫排除原因，避免把「昨天深夜」誤算成「今天凌晨後」。
- `opencli web read` 出現 `BROWSER_CONNECT 69` 時，不要把整頁直接判成失敗。
  - 先用 `curl.exe -L` 或同級 raw 抓取把 HTML 存下來。
  - 只有當 saved HTML 裡真的讀得到正文，並且再整理成 extracted markdown 或研究卡時，才能把它升成 `raw-body fallback` 證據。
  - 只保存 raw HTML 但沒整理出正文重點，仍然只能算半完成保存，不算可直接寫稿的深讀證據。
- 發售日 / 更新日當天的 guide cluster 值得單獨保留一層，因為它和一般累積研究不是同一件事。
  - 這次 AppMedia、Dengeki、Gamerch、Bahamut、YouTube release-day clips 被集中寫進 `today-0618-after-midnight-source-sweep.md`，讓後續代理能快速知道哪些是「當日新增」而不是前幾天沿用。
  - 這種 today-only 檔要同時記錄：cutoff、查詢詞、採用來源、降權來源、排除原因。
- 三語圈覆蓋現在不只要有矩陣，還要把「可當結論的 today-only 證據」與「只有市場訊號的 today-only 命中」分開。
  - 這次 Elliot run 的 `language-source-matrix.md` 把 `Japanese strong / Chinese medium-high but today-only mixed / English medium-high` 分層，這種寫法比只寫有沒有查過更有用。
- 使用者實機補充若直接修正系統用語，必須在研究層立刻改寫敘述，不可讓舊說法繼續混用。
  - 這次已把 `魔石碎片` 修正成「先視為隨機生成魔石資源」，並要求正式稿前再用 UI 驗證。
  - 類似補充如果會改變章節口徑，應同輪回寫 game memory，而不是只留在 deliverable。

### Failed or lower-value patterns reinforced by this pass

- 不要把 `today` 或 `最新` 當成搜尋平台自己的相對時間語意；一定要換算成任務要求的本地時區 cutoff。
- 不要因為 raw HTML 成功存下來，就假設正文已經被吸收；沒有 extracted text 或研究卡，還是不能直接拿來寫結論。
- 不要把沒有字幕的當日中文影片升成攻略證據；它們最多只能當市場 / 觀眾問題訊號。
- 不要讓使用者已修正的系統說法和舊的網路說法並列存在；一旦使用者補充更接近實機，就要把舊口徑降成待驗證。
- 不要忽略 Windows 預設編碼對字幕工具的影響；遇到 `UnicodeEncodeError` / `CP950`，重跑前先設 `$env:PYTHONIOENCODING='utf-8'`。
- 不要直接把帶引號的英文查詢丟進 `opencli.cmd` 後就信任結果；如果 PowerShell / `.cmd` 拆參數導致 Reddit 或 Steam 搜尋失敗，要把它記成命令層失敗，再改走 web discovery + body capture。
## 2026-06-20 Maintenance Pass

### Reusable methods confirmed from recent Elliot 10-chapter / Day 2 refresh / Dave Jungle seed runs

- Incremental deepening packs should treat the previous accepted pack as a named retained source layer, not as invisible background memory.
  - If the user says not to delete earlier beginner-guide research, keep the old pack in `sources.md` as `retained source layer`.
  - New refresh work should focus on the gaps: new web bodies, new comments, new day-after corrections, or newly locked chapters.
  - `PACKAGE-MANIFEST.md` should say whether earlier run folders were retained wholesale or specific files were copied forward.
- Wrapper failure can now come from extension-update state, not only lost connectivity.
  - If `python scripts/opencli_tooling.py ensure --update --run-dir <run-dir>` exits non-zero because the browser extension reports an update warning, do not immediately downgrade the whole toolchain.
  - Read the embedded `opencli doctor` block and run direct smoke tests for `youtube search`, `google search`, `web read`, and `youtube comments`.
  - Record the final state as `wrapper false negative from extension update warning` when direct commands work.
- Locked-chapter refreshes should pivot from broad beginner queries to chapter-noun query families once the baseline pack already exists.
  - Example pattern: after the base beginner pack is stable, query specific nouns such as `glass vial`, `cats`, `missable quests`, `magicite rank 5`, `Trial Sanctuary`, `spear build`, or `friendship rewards`.
  - This keeps the refresh dense instead of re-collecting the same broad hits.
- Candidate-only search volume deserves its own file when the pack is already dense.
  - Keep validated evidence in `sources.md`.
  - Move search-result-only leads into a separate file such as `sources-candidates-opencli.md`.
  - This preserves discovery receipts without diluting the accepted evidence table.
- Bilibili can still contribute two different supporting roles when subtitles fail.
  - Older competitor videos with only metadata/comments are `format signal only`.
  - Current guide-video metadata/comments can still be `player problem pool` evidence when comments expose mission-order confusion, boss friction, missing item questions, or patch concerns.
  - Neither role upgrades into creator-spoken guide evidence unless subtitle/audio text exists.
- Day-after refreshes do not need to rebuild every language layer from zero.
  - If no stronger new Japanese bodies appear, explicitly keep the previous-day JP layer as primary.
  - Add only the fresh English / Chinese / community delta, and say that in `sources.md` and the report.
- Dense writer-facing packs stay reusable when they preserve source-layer hierarchy.
  - `retained source layer` for prior base pack
  - `refresh layer` for day-after or patch-day additions
  - `new direct captures` for the current run
  - This makes later script-writing and maintenance passes understand what is inherited versus new.

### Failed or lower-value patterns reinforced by this pass

- Do not treat a non-zero readiness wrapper exit as tool death when the real blocker is only an extension-update warning.
- Do not mix competitor-format reference videos into factual evidence tables just because they are user-provided.
- Do not rerun a full multilingual baseline on every refresh if the real need is a few chapter-specific gaps.
- Do not let candidate-only search hits crowd the same evidence table as readable bodies, transcripts, or saved comments.
- Do not present bilibili metadata/comment captures as if the spoken guide itself was captured.

## 2026-06-21 Maintenance Pass

### Reusable methods confirmed from recent Dave Jungle deep-dive / practical-chapter runs

- If a stable baseline pack already exists and the user asks for more creator/community depth, create a named late-capture layer instead of flattening everything into one pile.
  - Put the extra bodies, comments, and transcripts under `source-originals/social-supplement/` and `transcripts/social-supplement/`.
  - If there is a later post-release or extra-hour follow-up, an `extra-hour-pass/` child folder is acceptable.
  - `PACKAGE-MANIFEST.md` should explain why the supplement exists and what it added beyond the base pack.
- User-provided screenshots are first-class research evidence when they show exact quest text, UI markers, or one observed trigger state.
  - Save the original image in `source-originals/`.
  - Add one source entry that separates `what the screenshot proves` from `what still needs outside confirmation`.
  - Use screenshot evidence to tighten wording, especially when guide sites disagree on NPC, quest, or unlock phrasing.
- Steam / Reddit discussion bodies should be promoted as player-pain or blocker evidence, not as official mechanics.
  - Good uses: buyer hesitation, bug complaints, restaurant blockers, return-path confusion, time-pressure stress, feature expectations, and patch-risk chatter.
  - Bad use: turning one complaint thread into a hard rule for exact time costs, exact progression logic, or official feature behavior.
- Lower-authority guide hubs can stay in a dense pack, but only with a narrow role label.
  - Valid roles: route sketch, terminology cross-check, system-shape support, or fallback explanation when stronger sources cover the same point.
  - Invalid roles: final customer counts, universal trigger timing, exact profit rankings, or hard optimization tables without stronger corroboration.
- When a creator source is captured but low quality, keep the downgrade evidence explicit.
  - If the transcript/comment pair shows AI-script accusations, self-contradiction, or conflicts with stronger official/guide sources, preserve the file and state why it was downgraded.
  - This creates a reusable `checked and rejected` record for later runs.

### Failed or lower-value patterns reinforced by this pass

- Do not mix late `social-supplement` captures into the same unlabeled evidence tier as the base-source layer.
- Do not use current Steam / Reddit complaint threads as the final authority for mechanics.
- Do not let weaker guide hubs carry exact numbers that stronger sources did not confirm.
- Do not write `user screenshot confirms` when the screenshot only confirms one observed instance.
- Do not silently drop a captured low-quality creator source; record the downgrade reason.

## 2026-06-22 Maintenance Pass

### Reusable methods confirmed from the late-completed Dave Jungle evidence layer

- When a locked guide pack gets user playtest corrections after the main pack is already dense, add a dedicated `mechanic-correction-table.md` instead of burying the fix only in the deliverable.
  - Record `Topic`, `New user result` or `User understanding / question`, `External evidence`, `Current ruling`, and `Evidence level`.
  - This is the cleanest way to stop gift / favorite food / Auto Supply / portion-prep / quest-marker wording from drifting again in later writing turns.
- Thick research packs are easier to audit when they preserve an explicit `claim-map.md`, not only `sources.md`.
  - Keep status buckets such as `supported`, `limited`, `conflicted`, `needs-verification`, `user-playtest`, and `downgraded`.
  - `user-playtest` keeps reusable user evidence without pretending it is outside confirmation.
  - `downgraded` preserves checked-but-rejected creator sources so later agents do not accidentally resurrect them.
- User screenshots should be promoted through the evidence layer, not left as raw attachments.
  - Save the original image in `source-originals/`.
  - Add a source entry that states exactly what the screenshot proves and what it does not prove.
  - Then attach the point to `claim-map.md` or `mechanic-correction-table.md` so quest text, gift-heart markers, and similar UI clues become reusable memory.
- A late correction sweep can use its own named source layer.
  - `source-originals/social-supplement/mechanic-correction-pass/` is a useful pattern when the work is no longer broad discovery and is instead reconciling conflicting guide wording, base-game carryover assumptions, and user playtest corrections.
  - This naming makes it obvious that the layer exists to repair terminology and mechanic framing, not to reopen the whole topic.
- `source-capture-status.md` should explicitly separate wrapper/tool state from evidence state.
  - Recent Dave evidence shows `opencli` wrapper failure, direct-command usability, user-playtest-only confirmations, and externally unconfirmed gaps can all coexist in one run.
  - Keeping that separation prevents later agents from overstating Auto Supply, dive-time fractions, New Game starting gear, or underwater quest markers as fully externally validated.

### Failed or lower-value patterns reinforced by this pass

- Do not fix late mechanic drift only inside the report body; add an explicit correction layer or later agents will lose the reason for the change.
- Do not leave screenshot or user-playtest evidence only in attachments or chat notes without connecting it to the claim map or correction table.
- Do not assume `sources.md` alone is enough once a pack accumulates conflicts, user corrections, and downgraded creator sources.
- Do not upgrade base-game Auto Supply text into a DLC hard fact unless the DLC behavior is separately labeled as user-playtest or otherwise revalidated.

### Gap note

- No newer Shorts research pattern appeared after the 2026-06-21 pass; the new reusable method evidence in this run comes almost entirely from the late-completed Dave Jungle pack.
- Bahamut still mostly remains a search-lead layer, and Chinese creator videos without subtitles are still a weak-evidence family rather than a solved capture path.

## 2026-06-23 Maintenance Pass

### Reusable methods confirmed from the Dave Jungle pack-to-script handoff

- Dense research packages stay more reusable for later writing when `PACKAGE-MANIFEST.md` acts as a navigation layer, not just a zip checklist.
  - List the run's decision files up front, especially `user-playtest-notes.md`, `claim-map.md`, `mechanic-correction-table.md`, `sources-candidates-opencli.md`, and `source-capture-status.md`.
  - Summarize source families, uncaptured families, downgraded families, and known limits in the same file.
  - This lets a later writing pass find what is safe, disputed, or still candidate-only without re-mining the full report first.
- Late refresh work is easier to reuse when each delta pass gets a dated and intent-named layer instead of one generic supplement bucket.
  - The current Dave pack proved `source-originals/20260622-update/`, `source-originals/20260622-money-method-update/`, and `source-originals/20260622-weapon-recommendation-update/` are easier to audit than dropping every late file into one folder.
  - Use the folder name to say what changed: hotfix refresh, money-method routing, weapon recommendation repair, and similar narrow jobs.
  - Mirror those layers in the manifest so later writing can pull only the relevant delta instead of rescanning the entire run.
- Writer-facing packs should keep uncertainty visible in the package layer, not only in chapter prose.
  - Preserve a `Known Limits` section in `PACKAGE-MANIFEST.md` for `user-playtest`, `needs in-game verification`, `candidate-only`, and weaker-language coverage notes.
  - If a later script or handoff uses those points, the source status is still recoverable without reverse-engineering the report.
  - This is especially important for Bancho Grill counts, Auto Supply behavior, Hook Gun prompts, and Chinese no-subtitle money-route candidates.

### Failed or lower-value patterns reinforced by this pass

- Do not treat `PACKAGE-MANIFEST.md` as a thin packing receipt once the run has claim maps, correction tables, user-playtest notes, and multiple late refresh layers.
- Do not hide late delta passes inside unnamed supplement folders; later writing passes lose the reason those files exist.
- Do not leave uncertainty labels only inside chapter prose when the package is expected to support later script writing or maintenance.

## 2026-06-24 Maintenance Pass

### Reusable methods confirmed from the local user-demo transcript run

- A user-provided local recording can be stored as a normal Maymei research run instead of a one-off helper artifact.
  - Keep `query-log-reviewed.md`, `sources.md`, `tool-readiness.md`, and `PACKAGE-MANIFEST.md` even if the source is only one local MP3 or WAV.
  - This keeps user-demo wording and later longform reuse inside the same memory structure as web-backed research.
- Long local transcription jobs should preserve four output layers by default.
  - `timestamped.md` for chapter routing and quotation.
  - `plain.txt` for fast reading and search.
  - `raw-asr.txt` for pre-normalization inspection.
  - `segments.json` for later re-slicing or targeted QA without rerunning the full job.
- Local ASR provenance belongs in the readiness layer, not only in the command history.
  - Record engine, model, device, compute type, thread count, language, VAD state, hotword use, and text-normalization choice in `tool-readiness.md`.
  - This is the only reliable way to compare transcript quality across future local-demo runs.
- Large local transcription jobs should keep an explicit progress log.
  - A saved `transcription-progress.log` with elapsed minutes, segment counts, and audio progress is useful for runtime estimation and failure diagnosis.
  - Silent one-shot transcripts are weaker because later agents cannot tell whether the job stalled, restarted, or only partially completed.
- Large original media does not always need to be copied into the reusable run package.
  - Keep the original source path in `sources.md` and `PACKAGE-MANIFEST.md`.
  - Keep small `source-originals/sample-*.wav` spot-check slices for VAD/quality review.
  - Only bundle the full raw media when later research or audit actually requires it.

### Failed or lower-value patterns reinforced by this pass

- Do not save only a cleaned final transcript from a long local recording and throw away the raw ASR / segment structure.
- Do not treat local-demo transcription as reusable evidence if the ASR settings are undocumented.
- Do not bloat every run package with the full original recording when lighter QA slices plus the original path are enough.
- Do not leave local user-demo transcripts outside the run-memory tree where later guide research cannot discover them.

### Gap note

- This pass did not add a new opencli, multilingual discovery, or forum-capture method; the durable new method was local-ASR packaging and auditability only.
- Shorts-specific method memory still has no newer evidence family after the 2026-06-23 pass.

## 2026-06-25 Maintenance Pass

### Reusable methods confirmed from the Dave Jungle traffic-evidence run

- A compact `traffic-evidence` pack is acceptable when the user asks for topic-choice proof instead of a full deep-dive guide package.
  - Keep the evidence chain formal even in the smaller shape: `query-log-reviewed.md`, `sources.md`, `claim-map.md`, `source-capture-status.md`, `decision-log.md`, `PACKAGE-MANIFEST.md`, and a report.
  - This is the correct fix when a spoken recommendation or thin comparison note would violate the repo's research-pack rules.
- Topic-ranking work should split `candidate metadata` from `validated read evidence` more aggressively than normal deep research.
  - Keep raw search artifacts in `sources-candidates-opencli.md`.
  - If useful, derive a helper like `candidate-metrics.csv` for cross-bucket comparison.
  - Do not move a source into `sources.md` until exact video metadata, comments, transcript text, or readable body text has been checked.
- For Bilibili traffic evidence, `bilibili search` is discovery and `bilibili video` is validation.
  - Search `score` can surface good candidates quickly.
  - Exact views, replies, likes, and favorites from `opencli.cmd bilibili video` are the stronger comparison layer for final ranking.
  - Comment capture then decides whether the topic also has practical player-problem evidence.
- `web read` can be usable even when the wrapper returns exit code `1`.
  - If the saved markdown body is readable and matches the intended page, keep the source as usable-with-wrapper-caveat.
  - Record the caveat in `source-capture-status.md` and `PACKAGE-MANIFEST.md` so later agents do not misclassify it as a full failure.
- Treat `tool-readiness.md` as a three-layer artifact: top summary, raw command blocks, and trailing notes.
  - If those layers conflict, trust the newest raw `opencli doctor` blocks and direct smoke results.
  - A stale final note such as `Browser Bridge is still unavailable` is lower weight than repeated later `[OK] Connectivity` evidence.

### Failed or lower-value patterns reinforced by this pass

- Do not keep a quick topic-decision run as raw platform JSON only if the result may need later reuse.
- Do not collapse candidate traffic signals and validated claim-bearing text into one evidence tier.
- Do not treat Bilibili search `score` as exact traffic proof when exact video metadata was not captured.
- Do not auto-fail readable `web read` outputs purely because the process exit code was non-zero.
- Do not quote the final prose note in `tool-readiness.md` without checking whether later doctor blocks contradict it.

### Gap note

- `workspace/memory/runs/20260625-001332-topic-decision-elliot-vs-dave/` is still a gap example, not a reusable model, because it lacks reviewed logs and a decision layer.
- This pass did not add a new Reddit / Steam / Bahamut deep-read breakthrough; the strongest new evidence is packaging discipline for compact traffic-evidence work.
- Shorts-specific method memory still did not advance in this pass.
