# Shorts Topic Research Prompt

你現在只做一件事：替 `玫玫物語` 找出最近值得做的 `Shorts` 題型與題目。

不要直接寫稿，也不要自動跳到長影片主題、標題或完整 Shorts 文稿。

## 先讀文件

- `docs/profiles/may-story/channel_scope.md`
- `docs/workflows/shorts-research.md`
- `docs/profiles/may-story/shorts_topic_research_rules.md`

## 任務目標

- 找出最近值得切入的 `Shorts` 題型。
- 如果使用者要的是 `Shorts 研究包`，不要只交主題清單；要改用 `templates/deliverables/shorts-research-pack.md`，補參考短片證據、hook / punch 分析與製作研究筆記。
- 固定比對 `中文 / 日文 / 英文` 三個語圈。
- 固定查 `YouTube Shorts / TikTok / IG Reels / 巴哈姆特 / bilibili`。
- 主證據優先看 `小型自媒體 / 個人創作者 / 非官方搬運解析`。
- 先把候選片整理成 `主題簇`，再判斷哪個題型真的在跑。
- 每個候選方向都要附一句題目提案、可能 hook、節奏來源與 Shorts 證據表。

## opencli 工作流

- 正式搜尋前先跑 `python scripts/opencli_tooling.py ensure --update`，確認 opencli、Browser Bridge、YouTube / bilibili / web read 與 YouTube 字幕備援可用。
- `YouTube Shorts` 固定先用 `opencli youtube search`，再手動只保留 `/shorts/`。
- `TikTok` 固定先用 `opencli tiktok search`。
- `bilibili` 固定先用 `opencli bilibili search`。
- `IG Reels` 固定先用 `opencli google search "site:instagram.com/reel/ ..."`。
- `巴哈姆特` 固定先用 `opencli google search "site:forum.gamer.com.tw ..."`。
- Shorts 題型如果要擴到 `Threads / X / TikTok Web 補查`，直接把腳本切到 `--breadth max`。
- 如果要批次先抓一輪樣本，優先跑：
  - `X:\writing-agent\.venv\python314\python.exe scripts\opencli_research.py shorts-topic <slug> --name-zh "<中文名>" --name-jp "<日文名>" --name-en "<英文名>"`
  - `X:\writing-agent\.venv\python314\python.exe scripts\opencli_research.py shorts-topic <slug> --name-zh "<中文名>" --name-jp "<日文名>" --name-en "<英文名>" --breadth max`
  - 需要同步修工具時加 `--repair-tools`

### 指令範例

```powershell
opencli youtube search "Pokopia shorts" --limit 20 -f json
opencli youtube search "ぽこポケ 小ネタ shorts" --limit 20 -f json
opencli youtube search "Pokopia hidden shorts" --limit 20 -f json
opencli tiktok search "Pokopia" --limit 10 -f json
opencli bilibili search "Pokopia 攻略" --limit 10 -f json
opencli google search "site:tiktok.com Pokopia" --lang en --limit 10 -f json
opencli google search "site:instagram.com/reel/ Pokopia" --lang en --limit 10 -f json
opencli google search "site:threads.net Pokopia" --lang en --limit 10 -f json
opencli google search "site:forum.gamer.com.tw Pokopia" --lang zh --limit 10 -f json
```

## 工作原則

- `YouTube` 只認 `/shorts/` 連結。
- 每款遊戲先整理 `中文 / 日文 / 英文` 名稱與常見別名。
- 每個語圈用自己的關鍵字分開搜。
- 每個語圈、每個題型都要 `一題一搜`。
- 每個語圈先抓 `10 到 20 支` 有量候選，再分成主題簇。
- 不要把官方片、大媒體片或靠創作者本人撐起來的片當成可抄主題。
- 結論要回到 `可複製熱門`，不是單支爆片。
- `Query Log` 一定要留下實際的 `opencli command`。
- 如果樣本不足，要直接寫進 `Risks / Unknowns`。
- 完成後除了正式 `Shorts Topic Pack`，也要把查詢證據整理進 `workspace/memory/runs/...`。
- 如果這次研究形成可重用判斷，還要更新 `workspace/memory/games/...`。

## Query Log 最少要寫

- `Query platform / site`
- `Language`
- `opencli command`
- `Keywords`
- `High-signal hits`
- `Included in final conclusion?`

## 輸出格式

主題搜尋用：

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
### Option 1
- Topic Cluster
- Why It’s Moving
- Platform Evidence
- Cross-Language Evidence
- Reference Shorts
  - 原文標題
  - 中文翻譯
  - 連結
  - 觀看數快照
  - 發片時間
  - 所屬主題簇
  - 為什麼值得抄
  - 這題是不是可複製熱門
- One-Line Topic Pitch
- Possible Hook
- Rhythm / Format Reference
- Chinese Audience Fit
- Use / Skip
## Top 1 Recommendation
## Why Now
## Risks / Unknowns
```

深度研究包用：

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
