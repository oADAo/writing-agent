# Longform Research Prompt

你現在的任務是替 `玫玫物語` 做長片研究。你不是在寫正式稿，也不是在做 Shorts。

## 先讀文件

- `AGENTS.md`
- `docs/workflows/longform-research.md`
- `docs/workflows/source-capture-research-rules.md`
- `docs/workflows/opencli-tooling.md`
- `docs/profiles/may-story/channel_scope.md`

## 任務目標

- 找出值得做的長片主題。
- 判斷這個主題為什麼有需求。
- 整理這支長片可以講哪些章節。
- 抓到網站正文、論壇正文、攻略頁正文、影片字幕、逐字稿、留言或 OCR。
- 產出高密度 `Longform Research Report`。
- 保留 query log、source originals、transcripts、source evidence table 與 package manifest。

## opencli 工作流

正式搜尋前先跑：

```powershell
python scripts/opencli_tooling.py ensure --update
```

主查詢優先使用：

```powershell
opencli youtube search
opencli bilibili search
opencli reddit search
opencli google search
opencli web read
```

高訊號 YouTube 影片逐字稿優先用：

```powershell
python scripts/opencli_tooling.py transcript "<YouTube URL>" --out-dir "<run-dir>\transcripts" --label "<source-label>"
```

如果要批次先抓基礎樣本，優先跑：

```powershell
python scripts/opencli_research.py topic <slug> --name-zh "<中文名>" --name-jp "<日文名>" --name-en "<英文名>" --breadth broad --repair-tools
```

工具失敗時，先修復、換方法或明確回報限制。不能默默降級成只看標題、摘要或搜尋結果。

## 工作原則

- 題材必須符合 `玫玫物語` 的頻道邊界。
- 只做長片研究，不做 Shorts，不寫正式朗讀稿。
- 涉及最新資訊、趨勢、更新、版本、攻略、競品或平台變化時，要重新查證。
- 每次先做遊戲名翻譯表：中文名、日文名、英文名、常見簡稱、舊譯名、玩家暱稱。
- 搜尋時要用各語圈自己的原生關鍵字，不要只拿單一語言硬搜。
- 長片研究預設看中文 / 日文 / 英文三個語圈。
- YouTube 高訊號影片要盡量抓字幕或逐字稿。
- 網站、論壇、攻略頁、新聞、商店頁必須讀正文。
- 搜尋結果頁、影片標題、縮圖文字、新聞摘要只能當線索，不能當主證據。
- 站外來源不可以只限於固定平台名單，要依遊戲生態找玩家真的會查的地方。
- 原則上至少查兩種站外來源類型；如果站外生態太薄，要直接寫明資料不足。
- 判斷競品影片是否值得參考時，要看頻道內相對表現，不只看絕對觀看數。
- 主題判斷要先看題型反覆出現，再看單支影片。
- 低觀看、小頻道、單支特例片只能當輔證，不能直接當主結論。
- 如果使用者已鎖定章節、順序或必講點，不可擅自刪除、合併、替換或重排。
- 如果章節尚未鎖定，只能給候選章節池與取捨理由，不要宣稱已定案。

## Query Log 最少要寫

- `Query platform / site`
- `Language`
- `opencli command`
- `Keywords`
- `High-signal hits`
- `Included in final conclusion?`

## Source Capture 最少要寫

每個來源都要記：

- `Source name`
- `URL`
- `Source type`
- `Evidence level`
- `Capture status`
- `Evidence file`
- `Actual text read`
- `Supports`
- `Included in conclusion?`

## 輸出格式

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

## 禁止事項

- 不要寫正式朗讀稿。
- 不要做 Shorts。
- 不要只交章節大綱。
- 不要只列網址。
- 不要把抓不到字幕或正文的影片當主證據。
- 不要把搜尋結果摘要補成玩法細節。
- 不要把資料不足的點寫成肯定句。
- 不要忽略使用者鎖定章節。
