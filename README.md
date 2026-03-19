# Script Writing Agent

這個 repo 現在是 `玫玫物語` 專用的對話驅動工作台。

你不需要記 CLI。主入口就是自然語言：直接告訴我你要找題目、想標題、寫長影片腳本，或寫 Shorts，我會按 repo 規則執行、查證、落檔，並盡量把可回用記憶保留下來。

目前這個 repo 只處理四種內容工作：

- 搜尋熱門主題
- 想高流量標題與封面方向
- 撰寫長影片腳本
- 撰寫 Shorts 文本

不處理影音 pipeline、字幕切軸、章節、overlay、Google Drive、ffmpeg、Shorts 剪輯、社群貼文或封面生圖流程。那些能力仍留在原本的 [studio-tools](/Users/may/Documents/studio-tools) 或其他工具。

## 怎麼用

直接用自然語言下需求：

- `幫我找這款遊戲最近能做的熱門題目`
- `這個題目幫我想高點擊標題和封面文案`
- `這個題目直接幫我出長影片腳本`
- `把這個題目寫成一篇 Shorts 口播稿`

如果你的句子已經很明確，我會直接判斷模式執行。
如果你一句話混了兩步以上，或缺少關鍵前提，我才會補問。

更完整的使用說明在 [how-to-use-this-agent.md](/Users/may/Documents/script-writing-agent/docs/how-to-use-this-agent.md)。

## 目前功能

- `熱門主題搜尋`
  會依 `AGENTS.md` 與 `topic_research_rules.md` 查中文、日文、英文三語圈，並要求 `YouTube + 站外來源` 交叉驗證。
- `高流量標題與封面方向`
  會輸出 `Title Pack`，包含標題候選、封面文案與構圖方向。
- `長影片腳本撰寫`
  會依 `content_rules.md`、`voice_memory.md` 與 `script_template.md` 產出 `Script Package`。
- `Shorts 文本撰寫`
  會依 `shorts_rules.md` 產出 `Shorts Package`。
- `內部驗證工具`
  可以檢查文件格式一致性、deliverable 結構與 topic memory 完整性。

## 成品與記憶會寫去哪裡

正式成品寫到：

- `workspace/deliverables/topic/`
- `workspace/deliverables/title/`
- `workspace/deliverables/script/`
- `workspace/deliverables/shorts/`

單次任務的工作記憶寫到：

- `workspace/memory/runs/`

可長期回用的遊戲記憶寫到：

- `workspace/memory/games/`

## 目前結構

```text
script-writing-agent/
├─ AGENTS.md
├─ README.md
├─ docs/
│  ├─ how-to-use-this-agent.md
│  ├─ profiles/
│  │  └─ may-story/
│  ├─ superpowers/
│  │  ├─ plans/
│  │  └─ specs/
│  └─ workflows/
├─ prompts/
├─ scripts/
├─ templates/
│  ├─ deliverables/
│  └─ memory/
├─ tests/
├─ workspace/
│  ├─ deliverables/
│  └─ memory/
└─ examples/
```

## 頻道定位

這個 agent 只服務 `玫玫物語`，並且只處理：

- `PC / Switch / PS5`
- 主機與單機買斷制遊戲
- 適合做成買前必知、新手攻略、每天必做、前期速衝、機制拆解的內容

熱門主題研究時，固定比對：

- 中文圈高流量頻道
- 日文圈高流量頻道
- 英文圈高流量頻道
- 各語圈自己的原生搜尋關鍵字

研究熱門時先整理 `主題簇`，再判斷哪個題型是真的熱。單支低觀看 Shorts、小圈子切片或偶發梗片，只能當補充案例，不能直接當主結論。

## 固定輸出格式

### 主題研究

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

### 標題與封面方向

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

### 長影片腳本

```md
# Script Package

## Outline
## Full Draft
## Fact Check Notes
```

### Shorts 文本

```md
# Shorts Package

## Hook Title
## Final Short Script
```

## 可手動跑的檢查工具

- `python3 scripts/check_docs_consistency.py`
- `python3 scripts/check_deliverable_shape.py <deliverable.md> --mode topic`
- `python3 scripts/check_memory_completeness.py <topic-run-dir>`
