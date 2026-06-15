# 玫玫物語 Research Agent

這個 repo 是 `玫玫物語` 專用的研究工作台。它現在負責兩條研究線：長片研究與 Shorts 研究；正式文稿、Shorts 完整口播稿、文風 finalizer 仍不是預設主流程。

## 先看哪裡

- `AGENTS.md`：最高優先級規則，新任務必讀。
- `docs/project-map.md`：專案地圖，說明每個資料夾負責什麼。
- `docs/workflows/longform-research.md`：長片研究主流程。
- `docs/workflows/shorts-research.md`：Shorts 主題搜尋與 Shorts 研究包流程。
- `docs/workflows/source-capture-research-rules.md`：來源擷取與原文保存硬規則。
- `docs/workflows/opencli-tooling.md`：opencli、Browser Bridge、YouTube 字幕擷取流程。
- `docs/profiles/may-story/channel_scope.md`：頻道題材邊界。
- `prompts/topic-research.md`：長片研究執行 prompt。
- `prompts/shorts-topic-research.md`：Shorts 主題搜尋 prompt。

## 固定服務範圍

- 只處理 `PC / Switch / PS5` 這類主機與單機買斷制遊戲。
- 長片研究：找主題、定章節、查來源、產研究報告。
- Shorts 研究：找短影音題型、整理參考 Shorts、分析 hook / punch / 畫面節奏、產 Shorts 研究包。
- 不預設做可直接朗讀稿。
- 不預設跑 maymei-script-finalizer 文風流程。

如果需要正式寫稿，這個 repo 只提供 writer handoff 或研究包，不在預設流程中收斂成最終文稿。

## 常用下法

- `幫我找這款遊戲最近能做的長片攻略主題`
- `這款遊戲買前必看可以講哪些章節，先給我研究方向`
- `這款遊戲新手攻略幫我做深度研究包`
- `這幾章已經鎖定，幫我查每章資料跟來源`
- `幫我找這款遊戲能做的 Shorts 題型`
- `這個 Shorts 題目幫我做研究包，參考短片和 hook 都整理出來`
- `資料越多越好，我自己整理，請保留原文和字幕`

## 主要產物

長片研究交付：

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

Shorts 主題搜尋交付：

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

Shorts 深度研究交付：

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

成品位置：

- 長片研究報告：`workspace/deliverables/longform-research/`
- Shorts 主題包：`workspace/deliverables/shorts-topic/`
- Shorts 研究包：`workspace/deliverables/shorts-research/`
- 單次 run memory：`workspace/memory/runs/<timestamp>-<mode>-<slug>/`
- 原文與正文擷取：`<run-dir>/source-originals/`
- 字幕與逐字稿：`<run-dir>/transcripts/`
- 可長期回用的遊戲記憶：`workspace/memory/games/<slug>/`

每次研究成功完成後，正式報告旁要有 zip package 與 `PACKAGE-MANIFEST.md`，保留 query log、來源對照、工具檢查紀錄、正文、字幕、逐字稿、OCR 或附件。

## 專案結構

```text
writing-agent/
├─ AGENTS.md                         # 最高優先級操作規則
├─ README.md                         # 專案入口
├─ docs/
│  ├─ project-map.md                 # 專案地圖與維護規則
│  ├─ agents/                        # engineering skills 的 repo 設定
│  ├─ profiles/may-story/            # 頻道邊界與研究規則
│  └─ workflows/                     # longform / shorts / source capture / opencli 流程
├─ prompts/                          # 長片與 Shorts 研究 prompt
├─ scripts/                          # 研究、opencli、驗證工具
├─ templates/                        # research report / topic pack / memory 模板
├─ tests/                            # 驗證腳本測試
└─ workspace/
   ├─ deliverables/                  # 正式研究報告與研究包
   ├─ memory/                        # 工作記憶與長期記憶
   ├─ source-docs/                   # 匯出的原始語料
   └─ references/                    # 外部參考資料
```

## 常用檢查

```powershell
python scripts/opencli_tooling.py ensure --update
python scripts/check_deliverable_shape.py <research-report.md> --mode longform-research
python scripts/check_deliverable_shape.py <shorts-topic-pack.md> --mode shorts-topic
python scripts/check_deliverable_shape.py <shorts-research-pack.md> --mode shorts-research
python scripts/check_docs_consistency.py
python scripts/check_memory_completeness.py <run-dir>
pytest
```

## 維護原則

- 規則入口要少而明確：`AGENTS.md` 指向 longform、Shorts、source capture、opencli。
- Shorts Research 是正式研究入口；Shorts Writing 不是預設入口。
- 不要只交 markdown 結論；研究任務必須有來源擷取、字幕、留言、原文或可保存文字索引。
- 使用者已鎖定的章節、順序、必講點、Shorts 題型或參考短片不可擅自改動。
