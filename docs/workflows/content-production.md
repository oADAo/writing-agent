# Content Production Workflow

本檔保留作舊入口轉向。新架構已收斂為研究專用，不再維護舊的五種內容生產模式。

新任務請依研究類型使用：

- 長片研究：`docs/workflows/longform-research.md`
- Shorts 研究：`docs/workflows/shorts-research.md`
- 來源擷取：`docs/workflows/source-capture-research-rules.md`
- 工具 readiness：`docs/workflows/opencli-tooling.md`
- 長片 prompt：`prompts/topic-research.md`
- Shorts prompt：`prompts/shorts-topic-research.md`

## Current Scope

本 repo 現在只預設做：

1. 長片主題研究。
2. 長片章節與內容規劃。
3. 長片深度研究報告。
4. Shorts 主題搜尋。
5. Shorts 題型、hook、punch、畫面節奏與參考短片研究包。
6. 原文、正文、字幕、逐字稿、留言與來源包保存。

不再預設做：

- Shorts 完整文稿。
- 長影片正式朗讀稿。
- 標題封面素材包。
- maymei-script-finalizer 文風檢查。
- Google Docs 正式稿提交。

## Required Deliverables

長片研究交付使用：

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

Shorts 主題搜尋交付使用：

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

Shorts 深度研究交付使用：

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

模板在：

```text
templates/deliverables/longform-research-report.md
templates/deliverables/shorts-topic-pack.md
templates/deliverables/shorts-research-pack.md
```

交付前檢查：

```powershell
python scripts/check_deliverable_shape.py <research-report.md> --mode longform-research
python scripts/check_deliverable_shape.py <shorts-topic-pack.md> --mode shorts-topic
python scripts/check_deliverable_shape.py <shorts-research-pack.md> --mode shorts-research
python scripts/check_docs_consistency.py
```
