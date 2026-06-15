# 玫玫物語 Research Agent

這個 repo 只服務一個頻道：`玫玫物語`。

目前專案定位是研究引擎，不是通用內容助手，也不是文稿 finalizer。這裡正式支援兩種研究工作：

1. `Longform Research`：長片主題、攻略章節、買前必看與深度研究報告。
2. `Shorts Research`：Shorts 主題搜尋、Shorts 題型研究、參考短片與製作素材研究包。

## 服務範圍

- 只處理 `PC / Switch / PS5` 這類主機與單機買斷制遊戲。
- 支援長片研究與 Shorts 研究。
- 主要產物是高密度研究報告，不是可直接朗讀稿。
- 所有回覆與正式交付一律使用繁體中文；原文、字幕與引用資料保留來源語言，並附中文整理。

## 不做什麼

除非使用者明確要求臨時例外，否則本 repo 不做：

- Shorts 完整文稿。
- 長影片正式朗讀稿。
- maymei-script-finalizer 文風打分。
- Voice Check / 85 分文風門檻。
- Google Docs 正式稿提交。
- 純標題封面發想。

如果使用者要求上述工作，先說明本 repo 目前主範圍是研究，預設只提供研究報告、研究包、章節包、Shorts 題型包或 writer handoff。不要偷偷切回舊的正式寫稿流程。

## 新任務啟動順序

每次新任務固定先讀：

1. `AGENTS.md`
2. `docs/project-map.md`
3. `docs/workflows/source-capture-research-rules.md`
4. `docs/workflows/opencli-tooling.md`
5. `docs/profiles/may-story/channel_scope.md`

再依任務讀對應文件：

- 長片研究：`docs/workflows/longform-research.md`、`prompts/topic-research.md`
- Shorts 主題搜尋或 Shorts 研究包：`docs/workflows/shorts-research.md`、`docs/profiles/may-story/shorts_topic_research_rules.md`、`prompts/shorts-topic-research.md`

如果需要理解 skills、issue、triage 或工程規則，再讀 `docs/agents/skill-routing.md`。

## 固定工作流

### Longform Research

```text
長片需求判斷
-> 長片主題研究
-> 候選章節與必查問題
-> 使用者確認或保留候選狀態
-> 深度來源擷取
-> Longform Research Report
-> 來源包與 manifest
```

如果使用者只給 `遊戲名 + 買前必看 / 買之前 / 入坑前 / 值不值得買`，直接進入 `買前長片研究`。

如果使用者只給 `遊戲名 + 新手攻略 / 新手開局 / 前期必做 / 攻略`，直接進入 `攻略長片研究`。

如果使用者只說要找長片題目，先做長片主題研究，不跳到標題封面或完整稿。

### Shorts Research

```text
Shorts 需求判斷
-> Shorts 主題搜尋或指定主題研究
-> 跨平台短影音搜尋
-> 參考 Shorts / 留言 / 說明 / 字幕擷取
-> 主題簇與 hook / punch 分析
-> Shorts Topic Pack 或 Shorts Research Pack
-> 來源包與 manifest
```

如果使用者說 `Shorts 主題 / Shorts 題型 / 短影音題目 / 找能做的 Shorts`，直接進入 `Shorts 主題搜尋`。

如果使用者說 `Shorts 研究包 / 這個 Shorts 題目幫我查 / 參考短片整理 / 短影音素材包`，直接進入 `Shorts 研究包`。

Shorts Research 只做研究與素材整理，不自動寫完整 Shorts 腳本。

## 不能動的鎖定規則

- 使用者已經挑好的章節、順序、必講點、排除點、Shorts 題型、參考短片或製作限制，是鎖定條件。
- 不可擅自刪除、合併、替換或重排使用者鎖定內容。
- 如果研究發現鎖定內容有風險，只能標註風險並提出修改理由，等使用者同意後再改。
- 只有使用者明確說 `就照這個 / 鎖這幾章 / 這些保留 / 這個順序 / 不要改 / 就做這支 Shorts / 這個題型要保留`，才算確認或鎖定。
- agent 自己整理出的候選章節、候選題目、推薦排序、Shorts 題型，不等於已鎖定。
- 候選階段只能用 `候選章節 / 候選題型 / 可考慮 / 建議優先查 / 供你挑 / 取捨方向` 這類語氣。
- 避免使用 `必講章節 / 最後保留 / 核心章節 / 建議最後鎖定 / 必做 Shorts` 這類會讓人誤以為定案的字眼，除非是使用者原話或已確認內容。

## 頻道邊界

先讀 `docs/profiles/may-story/channel_scope.md`。

工作時要一直遵守：

- 題材必須落在 `玫玫物語` 會做的遊戲類型內。
- 研究熱門不是追所有熱門，而是找 `玫玫物語` 做了也有機會吃流量的題目。
- 長片研究優先回到買前必看、新手開局、前期效率、每天必做、資源效率、機制拆解、配置或路線攻略。
- Shorts 研究優先回到 3 秒內看得懂、有明確 punch、有畫面記憶點、可被本頻道重製的題型。
- 模仿高流量頻道只學題型、需求、切角、節奏和畫面結構，不照抄內容。

## 研究品質底線

本 repo 所有研究任務都適用 `docs/workflows/source-capture-research-rules.md`，包含長片研究與 Shorts 研究。

研究結論只能建立在已讀到、可保存或可回查的文字證據上。以下只能當線索，不能當主結論證據：

- 搜尋結果頁。
- 新聞摘要。
- 影片標題。
- 縮圖文字。
- 商店短介。
- AI 摘要。
- Google snippet。
- 社群貼文列表。

主證據至少要符合其中一種：

- `opencli web read` 或等價工具讀到的網頁正文。
- YouTube / bilibili 影片字幕、逐字稿或本地音訊轉錄。
- YouTube / B 站高讚留言、論壇留言、社群討論的可保存正文。
- Shorts / TikTok / Reels 的標題、說明、留言、字幕或可保存正文。
- 官方頁、新聞頁、攻略頁、商店頁的正文擷取結果。
- 使用者提供的截圖、文件、附件，搭配 OCR 或人工摘錄。

沒有抓到正文、字幕、逐字稿、留言文字、OCR 或本地轉錄，就不得把該來源當成深度研究證據。

## 長片研究必查範圍

每次長片研究盡量覆蓋：

- 中文 / 日文 / 英文三個語圈。
- YouTube 高訊號影片與可擷取字幕。
- 非官方創作者 / 社群影片，尤其是 `月份遊戲推薦 / upcoming games / new games / best games this month / gameplay preview / demo impression / hands-on / before you buy / trailer breakdown` 這類介紹影片；必須抓到字幕、逐字稿、本地轉錄或可保存留言正文，整理「別人介紹這款遊戲時實際講了什麼」。
- bilibili 高訊號影片或留言。
- 巴哈姆特、Reddit、Steam Community、攻略站、新聞或官方頁，依遊戲生態調整。
- 至少兩種站外來源類型；如果站外生態不足，要明寫 `資料不足`。

官方來源只負責確認基本事實，例如發售日、平台、版本、價格、系統名稱、已公開玩法與更新內容。玩家需求、疑慮、攻略價值與章節取捨，必須看玩家社群、留言、攻略站或創作者實測內容。

## Shorts 研究必查範圍

每次 Shorts 研究盡量覆蓋：

- 中文 / 日文 / 英文三個語圈。
- YouTube Shorts，且只認 `/shorts/` 連結。
- TikTok。
- IG Reels。
- bilibili。
- 巴哈姆特或其他玩家社群。

Shorts 證據要記錄：

- 原文標題與中文翻譯。
- 連結。
- 觀看數快照。
- 發片時間。
- 所屬主題簇。
- 3 秒內 hook。
- punch / payoff。
- 畫面形式。
- 可複製點。
- 不建議照抄的點。
- 證據保存路徑。

官方片、大媒體片、純宣傳片、VTuber 或實況主人格魅力片只能當線索或事實校正，不能直接當可複製熱門主證據。

## opencli 與字幕硬規則

正式研究前先跑：

```powershell
python scripts/opencli_tooling.py ensure --update
```

工具檢查紀錄要留在 run folder。若失敗，必須先修復、換方法或明確回報限制，不可默默降級成只看標題。

搜尋與擷取優先順序：

- YouTube：`opencli youtube search`
- TikTok：`opencli tiktok search`
- bilibili：`opencli bilibili search`
- Reddit：`opencli reddit search`
- site 搜尋：`opencli google search`
- 單頁正文：`opencli web read`
- YouTube 字幕：

```powershell
python scripts/opencli_tooling.py transcript "<YouTube URL>" --out-dir "<run-dir>\transcripts" --label "<source-label>"
```

如果字幕擷取失敗，依序嘗試自動字幕、其他語言字幕、音訊本地轉錄、影片說明、置頂留言、高讚留言或同主題其他影片。仍然失敗時，研究報告必須標註 `未能擷取逐字稿`，並降低或移除該影片權重。

## 研究報告深度規則

使用者要求 `研究包 / 深度研究 / 詳細研究 / 多平台研究 / 資料整理 / 給我完整資料` 時，預設交付 `高密度資料倉庫`，不能交薄大綱。

Longform Research Report 至少要包含：

- 研究範圍與任務目標。
- 主題判斷與為什麼值得做。
- Query Log，含平台、語言、原生關鍵字、opencli command、高訊號命中、是否納入結論。
- Source Capture Status，含工具檢查、原文資料夾、字幕資料夾、哪些來源抓不到。
- 社群 / 創作者影片摘要，列出每支非官方影片實際講到的賣點、疑慮、玩家對位、不可講死之處，以及字幕 / 逐字稿 / 轉錄保存路徑。
- 長片章節規劃，標明候選或已鎖定。
- 每章研究卡，含玩家問題、已確認事實、社群回報、研究推論、具體流程、風險、不建議講死。
- 來源重點對照表，列出每個來源實際支撐哪個結論。
- 原文 / 正文 / 字幕 / 逐字稿索引，必須有本地路徑或保存位置。
- 需要實機驗證的點。
- 風險、未知與後續補查方向。

Shorts Research Pack 至少要包含：

- 研究範圍與任務目標。
- Query Log。
- Source Capture Status。
- 平台訊號。
- 主題簇。
- 參考 Shorts 證據。
- hook / punch 分析。
- 留言與社群訊號。
- 台灣觀眾適配。
- 製作研究筆記。
- 來源重點對照表。
- 原文 / 字幕 / 留言索引。
- 風險、未知與後續補查方向。

研究報告可以最後附 `建議結論 / Claude Code 寫稿提示詞 / writer handoff`，但這些只能放在資料之後，不能取代研究內容。

## 攻略研究升級規則

任何 `新手攻略 / 速刷攻略 / 資源效率 / 掛機刷法 / 設定推薦 / 前期必做 / 系統教學` 任務，都當成可實機驗證的攻略研究處理。

必須整理：

- 具體流程。
- 前置條件。
- 需要的角色、車、裝備、道具、設定或系統。
- 效率數字與來源層級。
- 穩定性。
- 常見失敗原因。
- 是否可能被更新修掉。
- 是否需要實機驗證。

任何效率數字都要標明來源層級，例如 `影片實測 / 留言回報 / 攻略站整理 / 本機尚未驗證`。沒有親自驗證前，不要保證一定能達成。

遇到刷錢、刷經驗、刷技術點、掛機、自動駕駛、宏、外部工具、疑似漏洞或可能被修正的方法，必須另外整理 `風險與避坑`。

## 產物位置

- 長片研究報告：`workspace/deliverables/longform-research/`
- Shorts 主題包：`workspace/deliverables/shorts-topic/`
- Shorts 研究包：`workspace/deliverables/shorts-research/`
- 長片 run memory：`workspace/memory/runs/<timestamp>-longform-research-<slug>/`
- Shorts run memory：`workspace/memory/runs/<timestamp>-shorts-research-<slug>/`
- 原文與正文擷取：`<run-dir>/source-originals/`
- 字幕與逐字稿：`<run-dir>/transcripts/`
- 可長期回用的遊戲記憶：`workspace/memory/games/<slug>/`

每次研究成功完成後，都要同步整理 zip package，放在正式研究報告旁。壓縮包至少包含：

- 正式研究報告或研究包。
- Query Log。
- Sources / 來源重點對照。
- tool-readiness 記錄。
- 已取得的原文、正文、字幕、逐字稿、OCR、截圖或使用者附件。
- `PACKAGE-MANIFEST.md`，說明保留了哪些素材、哪些來源只保留連結、哪些來源未能擷取全文。

不能只交單一 markdown 結論檔。

## 交付前檢查

長片研究報告：

```powershell
python scripts/check_deliverable_shape.py <research-report.md> --mode longform-research
```

Shorts 主題包：

```powershell
python scripts/check_deliverable_shape.py <shorts-topic-pack.md> --mode shorts-topic
```

Shorts 研究包：

```powershell
python scripts/check_deliverable_shape.py <shorts-research-pack.md> --mode shorts-research
```

所有正式交付前都要跑：

```powershell
python scripts/check_docs_consistency.py
```

如果有 run folder，還要確認：

- `query-log-reviewed.md` 存在。
- `sources.md` 存在。
- `source-originals/` 或等價資料夾存在。
- `tool-readiness.md` 或等價工具紀錄存在。
- `PACKAGE-MANIFEST.md` 存在。

如果檢查無法執行，要在回覆中明講原因。
