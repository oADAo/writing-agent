# Shorts Research Workflow

這份文件只處理 `玫玫物語` 的 Shorts 研究工作。

Shorts 研究不是 Shorts 正式寫稿。這條工作流負責找題型、抓參考短片、整理 hook / punch / 畫面節奏與可製作素材，最後交付研究包給後續剪輯或寫稿使用。

## 目標

1. 找出最近值得做的 Shorts 題型。
2. 將候選短片整理成可複製的主題簇。
3. 保存可回查的 Shorts 證據、留言、字幕、說明或原文。
4. 產出 `Shorts Topic Pack` 或 `Shorts Research Pack`。
5. 不直接產出 Shorts 完整文稿，除非使用者另外明確要求。

## 任務類型

### 1. Shorts 主題搜尋

使用者想知道最近有哪些 Shorts 題型可做時，交付 `Shorts Topic Pack`。

重點是：

- 哪些題型正在跑。
- 哪些 punch 可以複製。
- 哪些題型有跨平台或跨語圈驗證。
- 哪些題型適合台灣觀眾。
- 哪些題型不適合做或證據不足。

### 2. Shorts 研究包

使用者已經有遊戲、方向、主題或候選短片，需要整理成可製作資料時，交付 `Shorts Research Pack`。

重點是：

- 參考短片實際做了什麼。
- 3 秒內 hook 是什麼。
- 畫面 punch 是什麼。
- 轉折、反差、結果或資訊密度在哪裡。
- 可拍哪些畫面。
- 可保留哪些原文、字幕、留言或說明作為證據。

## 啟動流程

### Step 1. 建立 run folder

每次正式研究都建立：

```text
workspace/memory/runs/<timestamp>-shorts-research-<slug>/
```

最少要包含：

- `query-log-reviewed.md`
- `sources.md`
- `decision-log.md`
- `source-originals/`
- `transcripts/`
- `tool-readiness.md`
- `PACKAGE-MANIFEST.md`

### Step 2. 跑工具 readiness

正式搜尋前先跑：

```powershell
python scripts/opencli_tooling.py ensure --update
```

如果失敗，先修復或在研究包明確標註限制。不能默默退回只看標題、縮圖或搜尋摘要。

### Step 3. 建立遊戲名翻譯表

每款遊戲先列：

- 中文名。
- 日文名。
- 英文名。
- 常見別名、簡稱、舊譯名、玩家暱稱。

每個語圈用該語圈自己的關鍵字查，不要拿英文直接硬翻全部語圈。

### Step 4. 平台搜尋

固定優先查：

- YouTube Shorts。
- TikTok。
- IG Reels。
- bilibili。
- 巴哈姆特。

預設工具：

```powershell
opencli youtube search "<keyword>" --limit 20 -f json
opencli tiktok search "<keyword>" --limit 10 -f json
opencli bilibili search "<keyword>" --limit 10 -f json
opencli google search "site:instagram.com/reel/ <keyword>" --limit 10 -f json
opencli google search "site:forum.gamer.com.tw <keyword>" --limit 10 -f json
```

YouTube 只把 `/shorts/` 連結當 Shorts 證據。不是秒數短就算 Shorts。

如果要批次先抓一輪，優先用：

```powershell
python scripts/opencli_research.py shorts-topic <slug> --name-zh "<中文名>" --name-jp "<日文名>" --name-en "<英文名>"
python scripts/opencli_research.py shorts-topic <slug> --name-zh "<中文名>" --name-jp "<日文名>" --name-en "<英文名>" --breadth max
```

需要同步修工具時加 `--repair-tools`。

### Step 5. 擷取可保存文字證據

Shorts 研究也要遵守 `docs/workflows/source-capture-research-rules.md`。

可用主證據包含：

- Shorts 標題、說明、置頂留言、高讚留言。
- 可擷取字幕、逐字稿或本地轉錄。
- TikTok / IG / B 站可保存的貼文正文、留言或說明。
- 巴哈姆特、Reddit、Threads、X 等社群正文。
- 使用者提供截圖或附件的 OCR。

不能只看：

- 搜尋結果摘要。
- 縮圖文字。
- 平台卡片預覽。
- AI 摘要。

### Step 6. 分主題簇

每個候選短片都要歸到主題簇，例如：

- 隱藏道具 / 隱藏地點。
- 反差結果。
- 速刷方法。
- 角色或武器強度比較。
- 玩家常犯錯。
- 官方沒講清楚的小知識。
- 趣味互動或意外畫面。

不要把很多同質題目拆成假裝不同方向。

### Step 7. 判斷可複製性

每個題型至少檢查：

- 3 秒內看不看得懂。
- 是否有明確結果。
- 是否有反差或驚喜。
- 畫面是否有記憶點。
- 不靠創作者個人魅力是否仍然成立。
- 台灣觀眾是否能理解名詞和情境。
- 是否需要實機拍攝或額外素材。

官方片、大媒體片、純宣傳片、VTuber 人格魅力片只能當線索或事實校正，不能直接當可複製熱門主證據。

## 正式交付格式

### Topic Search Template

主題搜尋使用：

```text
templates/deliverables/shorts-topic-pack.md
```

### Deep Research Template

深度研究包使用：

```text
templates/deliverables/shorts-research-pack.md
```

格式固定為：

```md
# Shorts Research Pack

## Research Scope
## Query Log
## Source Capture Status
## Platform Signals
## Topic Clusters
## Reference Shorts Evidence
## Hook / Punch Analysis
## Comment / Community Signals
## Chinese Audience Fit
## Production Research Notes
## Source Evidence Table
## Original Text / Transcript Index
## Risks / Unknowns
## Suggested Next Research
```

## 產物位置

- Shorts 主題包：`workspace/deliverables/shorts-topic/`
- Shorts 研究包：`workspace/deliverables/shorts-research/`
- 單次 run memory：`workspace/memory/runs/<timestamp>-shorts-research-<slug>/`
- 原文與正文擷取：`<run-dir>/source-originals/`
- 字幕與逐字稿：`<run-dir>/transcripts/`
- 可長期回用的遊戲記憶：`workspace/memory/games/<slug>/`

每次研究成功完成後，都要整理 zip package，放在正式研究包旁。壓縮包至少包含正式研究包、Query Log、來源對照、工具檢查紀錄、已取得的原文 / 字幕 / 逐字稿 / OCR / 截圖 / 使用者附件，以及 `PACKAGE-MANIFEST.md`。

## 交付前檢查

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

如果有 run folder，也要確認：

- `query-log-reviewed.md` 存在。
- `sources.md` 存在。
- `source-originals/` 存在。
- `tool-readiness.md` 存在。
- `PACKAGE-MANIFEST.md` 存在。

## 禁止事項

- 不要把 Shorts 研究自動變成 Shorts 完整文稿。
- 不要把一般影片、剪輯片或單純秒數短的影片當 YouTube Shorts。
- 不要只看單語圈或單平台。
- 不要把官方片、大媒體整理片直接當主證據。
- 不要只列連結，不寫實際讀到什麼。
- 不要在抓不到字幕、留言或正文時硬下重結論。
