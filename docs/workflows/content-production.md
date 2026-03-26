# Content Production Workflow

這份文件定義這個 repo 目前的標準內容流程。

## 目標

把內容工作拆成五個獨立但可串接的能力：

1. 長影片熱門主題研究
2. 高流量標題發想
3. 文案撰寫
4. Shorts 文本撰寫
5. 熱門 Shorts 主題研究

這五步是分開執行的，不自動連續串步。
主入口是自然語言；如果需求已經很明顯，就直接判斷對應模式執行。
只有在需求混合或模糊時，才回頭補問。

## 工作區

每次任務都要留下兩層結果：

- 正式成品：`workspace/deliverables/<mode>/`
- 工作記憶：`workspace/memory/runs/<timestamp>-<mode>-<slug>/`

可長期回用的遊戲記憶則整理到：

- `workspace/memory/games/<slug>/`

## 標準流程

### 1. 主題研究

- 先讀 `docs/profiles/may-story/channel_scope.md`
- 先確認題材是否屬於 `玫玫物語` 會做的遊戲類型
- 先確認平台、受眾、內容類型
- 固定比對中文、日文、英文的高流量頻道與熱門影片
- 固定補查 `YouTube` 以外的高流量社群、論壇、攻略站或其他站外來源
- 找近期熱門題目、反覆出現的需求、正在升溫的關鍵詞
- 如果資訊有時效性，一律重新查證，不用記憶硬寫
- 研究過程要留下查詢平台、原生關鍵字、代表來源與是否納入主結論
- 輸出應該包含：
  - `Inputs`
  - `Query Log`
  - `Market Signals`
  - `Community / Forum Signals`
  - `Cross-Language Competitor Hits`
  - `Cross-Source Validation`
  - `Chinese Audience Fit`
  - `5 Topic Options`
  - `Top 1 Recommendation`
  - `Why Now`
  - `Risks / Unknowns`

### 5. Shorts 主題研究

- 先讀 `docs/profiles/may-story/shorts_topic_research_rules.md`
- 先確認找的是 `真正的 Shorts`，`YouTube` 只認 `/shorts/`
- 先整理遊戲名翻譯表：`中文 / 日文 / 英文` 與常見別名
- 各語圈要用自己的原生關鍵字分開搜，而且 `一題一搜`
- 主證據優先看 `小型自媒體 / 個人創作者 / 非官方搬運解析`
- 官方與大型媒體只拿來做事實校正
- 每個語圈先抓 `10 到 20 支` 候選，再分成 `主題簇`
- 先排除 `假熱門`，只留下 `可複製熱門`
- 正式成品寫到 `workspace/deliverables/shorts-topic/`
- 輸出應該包含：
  - `Inputs`
  - `Query Log`
  - `Platform Signals`
  - `Comment / Community Signals`
  - `Cross-Language Shorts Hits`
  - `Cross-Platform Validation`
  - `Chinese Audience Fit`
  - `5 Shorts Topic Options`
  - `Top 1 Recommendation`
  - `Why Now`
  - `Risks / Unknowns`

### 2. 標題發想

- 先讀 `docs/profiles/may-story/title_thumbnail_rules.md`
- 每次至少先出 10 個候選，不要第一個就定案
- 標題要明確交代價值、風險、差異、結果或強烈好奇點
- 同步產出封面文案與封面構圖方向
- 標題不只追求誇張，要和內容本體真的對得上
- 正式成品寫到 `workspace/deliverables/title/`
- 輸出應該包含：
  - `Top 3`
  - `10 Candidate Titles`
  - `Angle Notes`
  - `3 Thumbnail Copy Options`
  - `3 Thumbnail Composition Directions`
  - `Final Title + Thumbnail Pair`

### 3. 文案撰寫

- 先讀 `docs/profiles/may-story/content_rules.md`
- 先讀 `docs/profiles/may-story/voice_memory.md`
- 先整理研究事實和重點，不要直接對著來源拼字
- 先做結構，再寫完整稿
- 如果 profile 有聲線記憶檔，抽象規則要讓位給實際聲線
- 正式成品寫到 `workspace/deliverables/script/`
- 輸出應該包含：
  - `Outline`
  - `Full Draft`
  - `Fact Check Notes`

### 4. Shorts 文本撰寫

- 先讀 `docs/profiles/may-story/voice_memory.md`
- 先讀 `docs/profiles/may-story/shorts_rules.md`
- 題材維持遊戲相關，但不限定劇情、冷知識、反轉、提醒或攻略
- 每支 Shorts 只打一個最值得講的 punch
- 第一行要鉤人，最後一句要有重擊
- 正式成品寫到 `workspace/deliverables/shorts/`
- 輸出應該包含：
  - `Hook Title`
  - `Hook Burst Text`
  - `Template Marked Script`

## 建議交付格式

### 研究階段

```md
# Topic Brief

## Inputs
## Query Log
## Market Signals
## Community / Forum Signals
## Cross-Language Competitor Hits
## Cross-Source Validation
## Chinese Audience Fit
## 5 Topic Options
## Top 1 Recommendation
## Why Now
## Risks / Unknowns
```

### 標題階段

```md
# Title Pack

## Topic
## Top 3
## 10 Candidate Titles
## Angle Notes
## 3 Thumbnail Copy Options
## 3 Thumbnail Composition Directions
## Final Title + Thumbnail Pair
```

### 寫稿階段

```md
# Script Package

## Outline
## Full Draft
## Fact Check Notes
```

### Shorts 階段

```md
# Shorts Package

## Hook Title
## Hook Burst Text
## Template Marked Script
```

### Shorts 主題研究階段

```md
# Shorts Topic Pack

## Inputs
## Query Log
## Platform Signals
## Comment / Community Signals
## Cross-Language Shorts Hits
## Cross-Platform Validation
## Chinese Audience Fit
## 5 Shorts Topic Options
## Top 1 Recommendation
## Why Now
## Risks / Unknowns
```
