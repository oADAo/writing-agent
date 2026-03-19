# 玫玫物語 Conversation Workbench Design

**Date:** 2026-03-19

## Goal

把這個 repo 從「規格文件集合」整理成「可持續使用的對話驅動工作台」。

使用者不需要記 CLI，也不需要手動維護格式；只要用自然語言說要做什麼，agent 就能：

- 判斷目前是在做 `熱門主題搜尋 / 標題與封面方向 / 長影片腳本 / Shorts 文本`
- 讀取對應規格與 prompt
- 需要最新資訊時自動查證
- 把正式成品與工作記憶分開落檔
- 在輸出前做基本驗證，避免格式與規則漂移

## Problem

目前 repo 的核心問題不是規格不夠，而是規格還沒有被整理成穩定的工作層：

- `AGENTS.md`、`README.md`、workflow、examples、prompts 已開始分工，但內容仍有漂移
- 同一種輸出格式在不同文件裡不一致，例如 `Topic Brief` 的欄位要求已經分裂
- repo 還沒有正式的工作區，成品、查詢證據、決策理由與長期記憶沒有固定落點
- repo 還沒有內部驗證器，無法自動攔住「規格改了但範例沒改」這種退化
- 使用方式仍偏向「人工閱讀文件後再臨場拼裝」，而不是可重複執行的工作台

## Goals

- 保持自然語言作為唯一主要入口
- 固定支援四種模式：`topic`、`title`、`script`、`shorts`
- 在可判斷模式時直接執行，只有混合任務或資訊不足時才反問
- 每次任務都留下正式成品與可回用記憶
- 優先透過本地工具、驗證器與既有 skills 降低跑偏
- 讓 repo 內所有文件對同一套輸出格式與流程說同一種話

## Non-Goals

- 不把 repo 做成完整自動化資料抓取平台
- 不要求使用者改成 CLI 工作流
- 不處理封面生圖、影音 pipeline、字幕、章節、Drive inbox 或社群貼文
- 不在第一版就做多頻道抽象化

## User Model

使用者的預期互動方式是自然語言，例如：

- `幫我找這款遊戲最近能做的熱門題目`
- `這個題目幫我想高點擊標題和封面文案`
- `這個題目直接幫我出長影片腳本`
- `把這個題目寫成一篇 Shorts 口播稿`

系統行為：

- 如果句子明顯落在單一步驟，直接執行
- 如果句子混了多步，例如「找題目順便寫腳本」，先拆解或反問
- 如果任務涉及最新資訊、趨勢、競品、版本、Shorts 樣本，優先查證，不靠記憶硬寫

## Recommended Approach

第一版採用「對話驅動、檔案留痕、內部驗證」的整理方式：

1. 保留 `AGENTS.md` 作為總控規格
2. 新增 `workspace/` 作為工作區，把成品與記憶分開
3. 新增 `templates/` 與 `scripts/`，把格式與檢查從口頭規則變成 repo 內資產
4. 更新 README 與使用文件，明寫使用者只需要自然語言下需求
5. 補一層 mode resolver / context loader / validator 的內部設計

## Product Behavior

### Single Entry

主入口是自然語言，不要求使用者背命令。

### Four Explicit Modes

內部固定四種模式：

- `topic`
- `title`
- `script`
- `shorts`

### Mode Resolution Policy

- 可以明確判斷時直接執行
- 缺關鍵前提時才補問
- 跨兩步以上的複合需求，不直接硬做成單步結果

### Write Policy

每次任務預設都要寫入 repo：

- `deliverables` 放正式成品
- `memory` 放查詢證據、來源、決策理由與可重用摘要

### Evidence Policy

只要任務有時效性或競品性，先查證再輸出。

`topic` 模式尤其要保存：

- 查詢平台 / 站點
- 各語圈原生關鍵字
- 代表來源與是否納入主結論
- 交叉驗證結論

## Architecture

### 1. Rule Layer

現有規格文件繼續作為唯一規則來源：

- `AGENTS.md`
- `docs/profiles/may-story/*.md`
- `prompts/*.md`
- `docs/workflows/content-production.md`

### 2. Workspace Layer

新增 `workspace/` 作為執行結果存放區。

#### Deliverables

正式成品存放於：

- `workspace/deliverables/topic/`
- `workspace/deliverables/title/`
- `workspace/deliverables/script/`
- `workspace/deliverables/shorts/`

命名規則：

- `YYYY-MM-DD-<slug>-topic.md`
- `YYYY-MM-DD-<slug>-title.md`
- `YYYY-MM-DD-<slug>-script.md`
- `YYYY-MM-DD-<slug>-shorts.md`

#### Run Memory

每次任務建立獨立 run 目錄：

- `workspace/memory/runs/<timestamp>-<mode>-<slug>/`

至少包含：

- `request.md`
- `query-log.md`
- `sources.md`
- `decision-log.md`
- `result-snapshot.md`

#### Game Memory

長期可重用記憶存於：

- `workspace/memory/games/<slug>/`

至少包含：

- `game-memory.md`
- `source-index.md`
- `open-questions.md`

### 3. Template Layer

新增 `templates/` 保存固定格式，避免每次手打：

- `templates/deliverables/topic-brief.md`
- `templates/deliverables/title-pack.md`
- `templates/deliverables/script-package.md`
- `templates/deliverables/shorts-package.md`
- `templates/memory/run-request.md`
- `templates/memory/query-log.md`
- `templates/memory/source-index.md`
- `templates/memory/decision-log.md`
- `templates/memory/game-memory.md`

### 4. Validation Layer

新增 `scripts/` 保存檢查工具。

第一版至少包含：

- `scripts/check_docs_consistency.py`
- `scripts/check_deliverable_shape.py`
- `scripts/check_memory_completeness.py`

## Internal Workflow

### Mode Resolver

根據自然語言意圖判斷模式：

- `找題目 / 最近能做什麼 / 熱門` -> `topic`
- `標題 / 封面文案 / 點擊` -> `title`
- `長影片 / 腳本 / 完整稿` -> `script`
- `Shorts / 短影音 / 口播稿` -> `shorts`

如果同句同時要求多模式結果，改為追問或拆任務。

### Context Loader

每個模式自動載入對應規格。

`topic`
- `docs/profiles/may-story/channel_scope.md`
- `docs/profiles/may-story/topic_research_rules.md`
- `prompts/topic-research.md`

`title`
- `docs/profiles/may-story/channel_scope.md`
- `docs/profiles/may-story/title_thumbnail_rules.md`
- `prompts/title-ideation.md`

`script`
- `docs/profiles/may-story/content_rules.md`
- `docs/profiles/may-story/voice_memory.md`
- `docs/profiles/may-story/script_template.md`
- `prompts/script-writing.md`

`shorts`
- `docs/profiles/may-story/channel_scope.md`
- `docs/profiles/may-story/voice_memory.md`
- `docs/profiles/may-story/shorts_rules.md`
- `prompts/shorts-writing.md`

### Tool and Skill Routing

第一版不做抽象 plugin 系統，但明寫優先順序：

1. 先用 repo 內規格與模板
2. 任務涉及最新資訊時用 web 查證
3. 任務需要工作流紀律時優先調用適合的 skills

預設路由原則：

- 新功能與結構調整：`brainstorming`
- 寫正式實作計畫：`writing-plans`
- 除錯與驗證失敗：`systematic-debugging`
- 宣稱完成前：`verification-before-completion`

### Write Flow

每次工作固定遵循：

1. 判斷模式
2. 讀規格與 prompt
3. 視需要查證
4. 先寫 `workspace/memory/runs/...`
5. 再整理正式成品到 `workspace/deliverables/...`
6. 更新 `workspace/memory/games/...` 的長期記憶
7. 跑驗證器

## Validation Design

### Docs Consistency Check

檢查下列檔案的固定輸出區塊是否一致：

- `AGENTS.md`
- `README.md`
- `docs/workflows/content-production.md`
- `examples/output-outline.md`
- `prompts/*.md`

至少要能抓出：

- `Topic Brief` 是否缺 `Query Log`
- `Topic Brief` 是否缺 `Community / Forum Signals`
- `Topic Brief` 是否缺 `Cross-Source Validation`
- 四模式名稱是否一致

### Deliverable Shape Check

檢查正式成品是否符合模式要求：

`topic`
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

`title`
- `Topic`
- `Top 3`
- `10 Candidate Titles`
- `Angle Notes`
- `3 Thumbnail Copy Options`
- `3 Thumbnail Composition Directions`
- `Final Title + Thumbnail Pair`

`script`
- `Outline`
- `Full Draft`
- `Fact Check Notes`

`shorts`
- `Hook Title`
- `Final Short Script`

### Memory Completeness Check

第一版優先檢查 `topic` memory：

- 是否有查詢平台
- 是否有關鍵字
- 是否有代表來源
- 是否標記是否納入主結論

之後可再擴到 `title / script / shorts` 的來源與決策記錄。

## File Plan

### Create

- `docs/superpowers/specs/2026-03-19-maymei-conversation-workbench-design.md`
- `docs/how-to-use-this-agent.md`
- `workspace/.gitkeep`
- `workspace/deliverables/.gitkeep`
- `workspace/memory/.gitkeep`
- `templates/deliverables/topic-brief.md`
- `templates/deliverables/title-pack.md`
- `templates/deliverables/script-package.md`
- `templates/deliverables/shorts-package.md`
- `templates/memory/run-request.md`
- `templates/memory/query-log.md`
- `templates/memory/source-index.md`
- `templates/memory/decision-log.md`
- `templates/memory/game-memory.md`
- `scripts/check_docs_consistency.py`
- `scripts/check_deliverable_shape.py`
- `scripts/check_memory_completeness.py`

### Modify

- `README.md`
- `AGENTS.md`
- `docs/workflows/content-production.md`
- `examples/output-outline.md`
- `prompts/topic-research.md`
- `prompts/title-ideation.md`
- `prompts/script-writing.md`
- `prompts/shorts-writing.md`

## Risks and Guardrails

- 如果只補 README，不補 `templates/` 與 `scripts/`，repo 還是會持續漂移
- 如果工作記憶和正式成品混放，之後很難回收與重用
- 如果 mode resolver 太貪心，會誤把複合需求當單步任務；第一版寧可保守
- 如果驗證器只檢查檔名，不檢查段落名稱，文件還是會默默失真

## Acceptance Criteria

- 使用者可以只靠自然語言描述任務，不需要知道 CLI
- repo 有清楚的 `workspace/` 結構，正式成品與工作記憶分離
- repo 有四種模式對應的 deliverable 模板
- repo 有至少三個可執行檢查器：文件一致性、成品結構、記憶完整性
- README 與使用文件明確教使用者怎麼以自然語言下需求
- workflow、example、prompts、README、AGENTS 的固定輸出格式一致

## Verification Plan

- 人工檢查 spec 是否和已確認的設計一致
- 後續進 implementation plan 前，先讓使用者 review 這份 spec
- implementation 完成後，用驗證器與抽樣任務確認：
  - `topic` 任務能同時產出 deliverable 與 memory
  - `title`、`script`、`shorts` 至少能產出正確結構的 deliverable
  - docs consistency check 能抓到目前 repo 既有的格式漂移問題
