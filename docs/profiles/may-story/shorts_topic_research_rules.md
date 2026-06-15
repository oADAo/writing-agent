# 玫玫物語熱門 Shorts 主題搜尋規則

## 目的

這份規則只處理 `玫玫物語` 的 Shorts 熱門主題搜尋。

重點不是找單支爆片，而是找：
- 可複製的 Shorts 題型
- 已經在多平台或多語圈出現的 punch
- 能直接接到 Shorts 寫稿步驟的題目包

## 必讀

開始前先讀：
- `docs/profiles/may-story/channel_scope.md`
- `docs/workflows/shorts-research.md`
- `prompts/shorts-topic-research.md`

## opencli 優先原則

熱門 Shorts 主題搜尋一律先用 `opencli`。

正式搜尋前必須先跑：

```powershell
python scripts/opencli_tooling.py ensure --update
```

如果這一步失敗，先修復 Browser Bridge / opencli / yt-dlp，或在研究包明確標註限制；不能默默只看搜尋結果標題。

### 固定平台

- `YouTube Shorts`
- `TikTok`
- `IG Reels`
- `巴哈姆特`
- `bilibili`

### 預設工具棧

- `YouTube Shorts`：`opencli youtube search`
- `TikTok`：`opencli tiktok search`
- `bilibili`：`opencli bilibili search`
- `IG Reels`：`opencli google search "site:instagram.com/reel/ ..."`
- `巴哈姆特`：`opencli google search "site:forum.gamer.com.tw ..."`

### 平台分層

- `核心平台`
  - `YouTube Shorts`
  - `TikTok`
  - `IG Reels`
  - `bilibili`
- `擴張平台`
  - `巴哈姆特`
  - `TikTok Web`
  - `Threads`
- `驗證 / 即時補查`
  - `X / Twitter`
  - `Reddit`

如果這次任務要求「越廣越好」或「寧可慢一點」，預設直接用 `--breadth broad`；需要再往外擴時，再切 `--breadth max`。

## 查詢流程

### 1. 先確認找的是 Shorts，不是一般短片

- `YouTube` 只認 `/shorts/` 連結
- 不是秒數短就算 Shorts
- 不要把一般影片切片混進來

### 2. 先做翻譯表

每款遊戲先列：
- 中文名
- 日文名
- 英文名
- 常見別名 / 玩家暱稱 / 舊譯名

### 3. 一題一搜，不要用超寬泛大雜燴

每個語圈都要分開查，例如：
- `遊戲名 + hidden + shorts`
- `遊戲名 + tips + shorts`
- `遊戲名 + funny + shorts`
- `遊戲名 + build + shorts`

### 4. 每個語圈先抓 10 到 20 支候選，再分主題簇

固定記下：
- 原文標題
- 中文翻譯
- 連結
- 觀看數快照
- 發片時間
- 所屬主題簇
- 為什麼值得抄
- 這題是不是可複製熱門

### 5. 不只看 YouTube Shorts

Shorts 題型研究不是只看 YouTube。

要一起比對：
- TikTok 有沒有相同 punch
- IG Reels 有沒有相同畫面記憶點
- bilibili / 巴哈姆特有沒有同樣的社群共鳴

## Query Log 硬規則

每個查詢都要留下：
- `Query platform / site`
- `Language`
- `opencli command`
- `Keywords`
- `High-signal hits`
- `Included in final conclusion?`

不能只寫平台名，不附實際 `opencli command`。

## 什麼才算可複製熱門

不是看單支片，而是看題型可複製性。

通常要同時滿足大部分條件：
- 不同創作者都做過
- 不同語言圈也有人做
- 標題一看就懂
- 畫面一眼就懂
- 不靠創作者本人魅力也成立

再用這 `5` 個標準判斷值不值得做：
- 這題 `3 秒內` 看得懂嗎
- 有明確結果嗎
- 有反差嗎
- 畫面有記憶點嗎
- 其他人做也有機會跑嗎

## 交付格式

如果任務只是找最近可做的 Shorts 題型，交付：

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

如果使用者要求 `Shorts 研究包 / 參考短片整理 / hook、punch、畫面節奏 / 可製作素材`，改交 `Shorts Research Pack`，格式以 `templates/deliverables/shorts-research-pack.md` 為準。

## 禁止事項

- 不要把官方片、新聞通稿題、大媒體整理片直接當主證據。
- 不要把 VTuber、實況主、靠人格魅力撐起來的片直接當題型。
- 不要只看單語圈。
- 不要只看標題，不看畫面和留言共鳴。
- 不要把一般短片硬當 Shorts。
- 不要不記 `opencli command`。
