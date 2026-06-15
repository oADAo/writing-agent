# Longform Research Workflow

這份文件是本 repo 的主工作流。它只服務 `玫玫物語` 長片研究，不處理 Shorts，也不產正式朗讀稿。

## 目標

每次任務要把遊戲題目整理成可支撐長片的研究資料：

1. 找到值得做的長片主題。
2. 說清楚這個主題為什麼有需求。
3. 整理候選章節或使用者鎖定章節。
4. 擷取網站正文、論壇正文、影片字幕、逐字稿、留言或 OCR。
5. 產出高密度 `Longform Research Report`。
6. 打包原文、字幕、query log、sources 與 manifest。

## 任務類型

### 1. 長片主題研究

使用者可能會說：

- `幫我找這款遊戲最近能做的長片題目`
- `這款遊戲有什麼攻略主題可以做`
- `找一個適合玫玫物語的主題`

交付重點：

- 主題簇。
- YouTube 與站外需求證據。
- 中文 / 日文 / 英文語圈訊號。
- 為什麼適合 `玫玫物語`。
- 可延伸的章節方向。

### 2. 買前長片研究

使用者可能會說：

- `遊戲名 + 買前必看`
- `遊戲名 + 買之前`
- `遊戲名 + 入坑前`
- `遊戲名 + 值不值得買`

預設先交候選章節池，不直接做正式稿。

候選章節應圍繞：

- 玩法核心。
- 內容量與耐玩度。
- 單人 / 多人 / 連線需求。
- 平台與版本差異。
- 適合誰、不適合誰。
- 價格、發售日、版本、DLC 或預購資訊。
- 玩家真正擔心或看不懂的地方。

### 3. 攻略長片研究

使用者可能會說：

- `遊戲名 + 新手攻略`
- `遊戲名 + 新手開局`
- `遊戲名 + 前期必做`
- `遊戲名 + 速刷 / 刷錢 / 刷經驗 / 資源效率`

預設先建立玩家問題池與候選章節池，再做每章深度研究。

每章研究卡必須盡量包含：

- 具體流程。
- 前置條件。
- 位置、入口、選單、設定或路線。
- 需要的角色、車、裝備、道具或系統。
- 效率數字與來源層級。
- 穩定性。
- 常見失敗原因。
- 版本更新風險。
- 是否需要實機驗證。

## 啟動流程

### Step 1. 建立 run folder

路徑：

```text
workspace/memory/runs/<timestamp>-longform-research-<slug>/
```

至少準備：

```text
query-log-reviewed.md
sources.md
decision-log.md
source-originals/
transcripts/
tool-readiness.md
PACKAGE-MANIFEST.md
```

### Step 2. 跑工具 readiness

正式研究前先跑：

```powershell
python scripts/opencli_tooling.py ensure --update
```

如果失敗，先修復或換方法。不能在工具失效時默默降級成只看標題、摘要或搜尋結果。

### Step 3. 建立遊戲名翻譯表

每次先列：

- 中文名。
- 日文名。
- 英文名。
- 常見簡稱。
- 舊譯名。
- 玩家暱稱。
- 官方繁中名稱是否已確認。

找不到官方繁中譯名時，標示 `待實機或官方資料確認`。

### Step 4. 跨語圈搜尋

至少查：

- 中文語圈。
- 日文語圈。
- 英文語圈。

不要只拿英文硬翻三語圈。每個語圈要用原生關鍵字，例如：

- 中文：`遊戲名 新手攻略`、`遊戲名 買前必看`、`遊戲名 前期必做`
- 日文：`ゲーム名 初心者 攻略`、`ゲーム名 序盤 おすすめ`、`ゲーム名 レビュー`
- 英文：`game name beginner guide`、`game name before you buy`、`game name early game tips`

### Step 5. 搜尋平台

依遊戲生態調整，但長片研究預設優先查：

- YouTube。
- bilibili。
- 巴哈姆特。
- Reddit。
- Steam Community。
- 官方頁或商店頁。
- 攻略站，例如 Game8、GameWith、Altema、Kamigame 或英文攻略站。
- 新聞或媒體正文，只用來補事實或背景。

原則上至少要有兩種站外來源類型。如果站外生態不足，要在研究報告明寫 `站外社群訊號不足`。

### Step 6. 擷取正文與字幕

主證據必須有可保存文字。優先方式：

- 網站、新聞、攻略頁、論壇：用 `opencli web read` 或等價方式讀正文。
- YouTube：用 transcript 工具抓字幕或逐字稿。
- bilibili：抓字幕、影片說明、評論或可保存正文。
- Reddit / Steam / 巴哈：讀討論串正文與留言。
- 使用者附件：OCR 或人工摘錄。

YouTube 字幕固定優先跑：

```powershell
python scripts/opencli_tooling.py transcript "<YouTube URL>" --out-dir "<run-dir>\transcripts" --label "<source-label>"
```

每個來源在 `sources.md` 與研究報告中都要標明：

- URL。
- Source type。
- Evidence level。
- Capture status。
- Evidence file。
- 實際讀到什麼。
- 支撐哪個結論。

### Step 7. 章節規劃

如果使用者尚未鎖定章節：

- 只交候選章節池。
- 不要宣稱已定案。
- 每章要附玩家問題、可查證方向、可能來源與風險。

如果使用者已鎖定章節：

- 保留使用者章節、順序與必講點。
- 研究只能補強、查證、標註風險。
- 不可擅自刪除、合併、替換或重排。

### Step 8. 寫研究報告

正式研究報告固定使用：

```text
templates/deliverables/longform-research-report.md
```

輸出位置：

```text
workspace/deliverables/longform-research/
```

研究報告不是腳本，也不是薄摘要。每一章都要有可回查來源與可直接拿去寫稿的資料。

### Step 9. 打包

研究完成後，報告旁必須有 zip package，至少包含：

- 正式研究報告。
- `query-log-reviewed.md`。
- `sources.md`。
- `decision-log.md`。
- `tool-readiness.md` 或 readiness 資料夾。
- `source-originals/`。
- `transcripts/`。
- `PACKAGE-MANIFEST.md`。
- 使用者附件或 OCR 結果。

如果某些來源只保留連結或未能擷取全文，必須寫進 manifest。

## Longform Research Report 格式

```md
# Longform Research Report

## Research Scope
## Topic Decision
## Query Log
## Source Capture Status
## Market / Player Demand Signals
## Chapter Plan
## Chapter Research Cards
## Source Evidence Table
## Original Text / Transcript Index
## Risks / Unknowns
## Need In-Game Verification
## Suggested Next Research
```

## 交付前檢查

至少跑：

```powershell
python scripts/check_deliverable_shape.py <research-report.md> --mode longform-research
python scripts/check_docs_consistency.py
```

如果有 run folder，再確認：

- `query-log-reviewed.md` 存在。
- `sources.md` 存在。
- `decision-log.md` 存在。
- `source-originals/` 存在。
- `tool-readiness.md` 或 readiness 資料夾存在。
- `PACKAGE-MANIFEST.md` 存在。

## 禁止事項

- 不要做 Shorts。
- 不要寫正式朗讀稿。
- 不要跑 maymei-script-finalizer 當主流程。
- 不要只看搜尋結果、標題、縮圖或摘要。
- 不要把沒有字幕或正文的影片當主證據。
- 不要只列網址而不說明實際讀到什麼。
- 不要因為資料不足而硬湊結論。
- 不要改動使用者已鎖定章節。
