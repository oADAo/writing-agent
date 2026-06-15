# 玫玫物語長片主題研究規則

這份規則只處理 `玫玫物語` 的長片主題研究。主流程以 `docs/workflows/longform-research.md` 為準。

## 目的

重點不是找所有熱門，而是找：

- 這個頻道現在做有機會吃到流量的長片攻略題。
- 有明確玩家需求的題型。
- 能延伸出可研究章節的題型。
- 有可保存正文、字幕、逐字稿或留言證據的題型。

## 必讀

開始前先讀：

- `docs/workflows/longform-research.md`
- `docs/workflows/source-capture-research-rules.md`
- `docs/workflows/opencli-tooling.md`
- `docs/profiles/may-story/channel_scope.md`
- `prompts/topic-research.md`

## opencli 優先原則

長片研究一律先用 `opencli` 或專案既有批次工具。

正式搜尋前必須先跑：

```powershell
python scripts/opencli_tooling.py ensure --update
```

如果這一步失敗，先修復 Browser Bridge / opencli / yt-dlp，或在研究報告明確標註限制；不能默默只看搜尋結果標題。

### 預設工具棧

- `YouTube`：`opencli youtube search`
- `bilibili`：`opencli bilibili search`
- `Google / site:` 補查：`opencli google search`
- `Reddit`：`opencli reddit search`
- 單頁讀取：`opencli web read`
- YouTube 字幕：`python scripts/opencli_tooling.py transcript "<YouTube URL>" --out-dir "<run-dir>\transcripts" --label "<source-label>"`

## 查詢流程

### 1. 先整理翻譯表

每次先列出：

- 中文名。
- 日文名。
- 英文名。
- 常見簡稱 / 別名 / 舊譯名 / 玩家暱稱。
- 官方繁中名是否已確認。

### 2. 分語圈查詢

至少查中文、日文、英文三語圈。不要只拿英文硬翻。

每個語圈要用原生關鍵字，例如：

- 中文：`新手攻略`、`買前必看`、`前期必做`、`速刷`、`心得`
- 日文：`初心者`、`序盤`、`攻略`、`レビュー`、`おすすめ`
- 英文：`beginner guide`、`before you buy`、`early game tips`、`review`、`best route`

### 3. 先找主題簇，不要被單片綁架

固定先看：

- 哪些玩家問題反覆出現。
- 哪些攻略需求反覆出現。
- 哪些高流量創作者都在做同一簇。
- 哪些站外討論也在問同一件事。

不要先因為某支影片爆了，就把它當市場結論。

### 4. 判斷競品爆款要看頻道內相對表現

競品影片不能只看絕對觀看數。至少記：

- `Channel baseline`：該頻道最近 8 到 12 支同類影片的常見觀看區間或中位數。
- `Format baseline`：同一片型，例如買前、新手、速刷、機制拆解。
- `Age-adjusted views`：發布天數與觀看數。
- `Relative lift`：大約高出頻道平常水位幾倍。
- `Likely signal`：高出的原因比較像遊戲本身、片型、標題 promise、發售時機，還是頻道粉絲盤。

相對爆款只能代表候選資格，仍然要用站外來源和實際內容交叉驗證。

### 5. 站外來源至少補兩種不同類型

依遊戲生態補：

- 論壇 / 社群。
- 攻略站 / wiki。
- Steam Community。
- 官方頁、商店頁或新聞正文。
- 玩家留言。

如果站外生態很薄，要在 `Risks / Unknowns` 明寫。

### 6. 主結論要通過 source capture

主結論至少要能指出：

- 實際讀到哪段正文、字幕、逐字稿或留言。
- 原文或擷取檔存在哪裡。
- 該來源支撐哪個主題或章節。
- 來源層級是官方確認、玩家回報、創作者實測、攻略站整理，還是研究推論。

## Query Log 硬規則

每個查詢都要留下：

- `Query platform / site`
- `Language`
- `opencli command`
- `Keywords`
- `High-signal hits`
- `Included in final conclusion?`

不能只寫「有查 YouTube / 有查 Reddit」。

## 可以當主結論的題型

- 反覆出現在多個語圈。
- 多位創作者都做。
- 站外也有相同問題簇或需求簇。
- 有正文、字幕、逐字稿、留言或 OCR 證據。
- 可以轉成中文圈可點、可講、可研究的長片章節。

## 只能當輔證的題型

- 小頻道單支爆片。
- 單篇爆文，沒有其他來源跟上。
- 只有搜尋摘要或影片標題。
- 只是一時事件，不能延伸成可研究長片。

## 交付格式

長片主題研究也使用正式研究報告格式：

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

- 不要只列題目，不解釋流量理由。
- 不要只看中文圈。
- 不要只看絕對觀看數。
- 不要把單支特例爆片直接當市場主題。
- 不要把單篇高互動貼文直接當整個市場都在追。
- 不要跳過查詢證據。
- 不要不記 `opencli command`。
- 不要沒有原文、正文、字幕、逐字稿或留言就寫重結論。
