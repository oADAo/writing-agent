# 玫玫物語 YouTube Agent Design

**Goal:** 把這個 repo 設定成只服務 `玫玫物語` 頻道的內容 agent，固定分三個獨立步驟工作：
1. 熱門主題搜尋
2. 高流量標題與封面方向
3. 長影片腳本撰寫

## Product Scope

### In Scope
- 只服務 `玫玫物語` 這個 YouTube 頻道。
- 只處理 `PC / Switch / PS5` 這類主機與單機買斷制遊戲。
- 研究中文、日文、英文三個語圈的熱門影片、熱門切角與高流量頻道。
- 根據外國爆款題型，轉成適合中文圈觀看的題目、標題與封面文案方向。
- 產出長影片腳本，沿用現有 `may-story` profile 的口吻與腳本結構。

### Out of Scope
- 不自動串成一條龍流程；使用者每次明確指定目前只做哪一步。
- 不直接產出封面圖片。
- 不處理 Shorts、社群貼文、影片描述、字幕、章節、剪輯、素材管線。
- 不處理手機遊戲、抽卡手遊、長期 live service 遊戲，除非使用者另行指定。

## Design Principles

- 單一頻道優先，不保留通用化抽象層。
- 每一步都用固定輸出格式，方便重複使用。
- 只要資訊牽涉趨勢、更新、競品或最新熱度，一律重新查證，不依賴記憶。
- 研究不是只看中文圈，而是固定比對中文、日文、英文高流量內容。
- 標題與封面方向要能借鏡爆款，但不能脫離內容本體。
- 腳本一定要先有結構，再進全文。

## Architecture

### 1. Root Controller
根目錄 `AGENTS.md` 作為總控：
- 明確規定 repo 只服務 `玫玫物語`
- 明確規定三個獨立工作模式
- 明確規定先讀哪些 profile / rules
- 明確規定哪些情況必須上網查證

### 2. Channel Profile Layer
`docs/profiles/may-story/` 保留頻道專用知識：
- `channel_scope.md`: 頻道定位、題材邊界、受眾與內容支柱
- `content_rules.md`: 長影片腳本總規則
- `voice_memory.md`: 實際口氣與句法
- `script_template.md`: 研究轉腳本模板
- `topic_research_rules.md`: 熱門主題搜尋規則
- `title_thumbnail_rules.md`: 標題與封面方向規則

### 3. Task Prompts
`prompts/` 下的三份 prompt 保持分工：
- `topic-research.md`
- `title-ideation.md`
- `script-writing.md`

這些 prompt 不再只寫抽象目標，而是要寫清楚：
- 何時使用
- 必讀資料
- 固定輸出格式
- 禁止行為

## Step Design

### Step 1: 熱門主題搜尋

**Input**
- 遊戲名稱，或使用者指定「先找最近可做的題目」
- 可選：平台、發售時間、目前影片方向

**Required Sources**
- 中文高流量頻道 / 熱門影片
- 日文高流量頻道 / 熱門影片
- 英文高流量頻道 / 熱門影片
- 官方頁面、商店頁面、發售與更新資訊

**Core Questions**
- 這款遊戲最近在三個語圈裡，什麼題型最容易爆？
- 哪些題型屬於 `玫玫物語` 會做、而且有機會在中文圈吃流量？
- 外國紅的角度裡，哪些還沒被中文圈做爛？
- 哪些題目符合頻道常見強項：
  - 新手必看
  - 第一天一定要做
  - 每天必做
  - 前期速衝
  - 機制拆解
  - 買前必知

**Output**
- `Inputs`
- `Market Signals`
- `Cross-Language Competitor Hits`
- `Chinese Audience Fit`
- `5 Topic Options`
- `Top 1 Recommendation`
- `Why Now`
- `Risks / Unknowns`

### Step 2: 高流量標題與封面方向

**Input**
- 已確定的題目或角度
- 可選：競品影片、你偏好的風格

**Rules**
- 只做 `標題 + 封面文案 + 封面構圖方向`
- 不直接生圖
- 標題必須先拆切角：
  - 收益
  - 損失
  - 效率
  - 反差
  - 好奇
  - 權威
- 要能從外國爆款題型翻成自然的中文點擊語感
- 封面文案要短、狠、讀一眼就懂，不可和標題重複到失去資訊增量

**Output**
- `Top 3`
- `10 Candidate Titles`
- `Angle Notes`
- `3 Thumbnail Copy Options`
- `3 Thumbnail Composition Directions`
- `Final Title + Thumbnail Pair`

### Step 3: 長影片腳本

**Input**
- 已確定題目
- 已整理事實與研究資料

**Rules**
- 先讀 `content_rules.md`、`voice_memory.md`、`script_template.md`
- 只寫長影片腳本
- 先出結構，再出全文
- 涉及版本、數字、刷新、條件時先重新查證
- 腳本要能直接朗讀，不帶筆記腔

**Output**
- `Outline`
- `Full Draft`
- `Fact Check Notes`

## File Plan

### Create
- `AGENTS.md`
- `docs/profiles/may-story/channel_scope.md`
- `docs/profiles/may-story/topic_research_rules.md`
- `docs/profiles/may-story/title_thumbnail_rules.md`
- `docs/superpowers/specs/2026-03-19-maymei-youtube-agent-design.md`
- `docs/superpowers/plans/2026-03-19-maymei-youtube-agent.md`

### Modify
- `README.md`
- `prompts/topic-research.md`
- `prompts/title-ideation.md`
- `prompts/script-writing.md`
- `docs/workflows/content-production.md`
- `examples/output-outline.md`

## Risks and Guardrails

- 熱門主題搜尋最容易失真，所以必須明寫「熱門」與「最新」都要重新查證。
- 競品模仿不能等於照抄，要保留「翻譯成中文圈可吃角度」這個步驟。
- 標題與封面規則若寫得太寬，容易回到通用行銷腔；必須綁定 `玫玫物語` 的遊戲題型。
- 腳本規則要維持現有 `may-story` 口氣優先，不能被新文件覆蓋掉。

## Verification Plan

- 檢查 `AGENTS.md` 是否正確串接到頻道 scope、主題研究規則、標題封面規則、腳本規則。
- 檢查三份 prompt 是否都明確寫出：用途、必讀文件、固定輸出、禁止行為。
- 檢查 `README.md` 是否反映新結構。
- 檢查所有新增檔案是否用一致的中文術語描述三個工作模式。
