# Project Map

這份文件是給接手 agent 用的專案地圖。新架構是 `玫玫物語研究引擎`，正式支援 `Longform Research` 與 `Shorts Research`。

## 規則優先級

1. `AGENTS.md`
   - 最高優先級。
   - 新任務先讀這份。
   - 只放研究硬規則、鎖定規則與交付底線。
2. `docs/workflows/source-capture-research-rules.md`
   - 全專案研究證據規則。
   - 定義哪些來源能當主證據、抓不到正文或字幕時怎麼處理。
3. `docs/workflows/research-source-acquisition.md`
   - 研究前厚資料蒐集流程。
   - 定義 YouTube 字幕、高讚留言、社群攻略正文與可導入爬蟲工具的優先順序。
4. `docs/workflows/opencli-tooling.md`
   - opencli、Browser Bridge、YouTube 字幕與工具 readiness。
5. `docs/profiles/may-story/channel_scope.md`
   - 頻道題材邊界。
6. `docs/workflows/longform-research.md`
   - 長片研究主工作流。
7. `docs/workflows/shorts-research.md`
   - Shorts 主題搜尋與 Shorts 研究包主工作流。
8. `prompts/topic-research.md`
   - 長片研究執行 prompt。
9. `prompts/shorts-topic-research.md`
   - Shorts 主題搜尋執行 prompt。
10. `templates/`
   - 正式研究報告、Shorts 研究包與 run memory 模板。
11. `scripts/`
   - opencli 批次工具與交付檢查。

正式寫稿、文風 finalizer、Google Docs 正式稿提交不是主流程入口。除非使用者明確要求臨時例外，不要引用它們來執行研究任務。

## 資料夾責任

| 路徑 | 負責內容 | 平常怎麼用 |
| --- | --- | --- |
| `AGENTS.md` | 研究最高規則 | 新任務必讀 |
| `docs/workflows/longform-research.md` | 長片研究主流程 | 長片研究任務必讀 |
| `docs/workflows/shorts-research.md` | Shorts 主題搜尋與研究包主流程 | Shorts 研究任務必讀 |
| `docs/workflows/source-capture-research-rules.md` | 原文、正文、字幕、逐字稿、留言保存規則 | 研究前與交付前必讀 |
| `docs/workflows/research-source-acquisition.md` | 厚資料蒐集、YouTube 高讚留言、GitHub 爬蟲工具建議 | 攻略 / 買前深度研究前讀 |
| `docs/workflows/opencli-tooling.md` | opencli readiness、字幕備援 | 正式搜尋前必讀 |
| `docs/profiles/may-story/channel_scope.md` | 頻道能不能做某題 | 判斷題材邊界先讀 |
| `docs/profiles/may-story/topic_research_rules.md` | 長片熱門題目研究細則 | 需要更細的長片題目判斷時讀 |
| `docs/profiles/may-story/shorts_topic_research_rules.md` | Shorts 熱門題型研究細則 | Shorts 主題搜尋時讀 |
| `docs/agents/skill-routing.md` | 工程任務與 repo 規則路由 | 改文件、腳本或測試前讀 |
| `prompts/topic-research.md` | 長片研究 prompt | 真正執行長片研究時讀 |
| `prompts/shorts-topic-research.md` | Shorts 題型搜尋 prompt | 真正執行 Shorts 主題搜尋時讀 |
| `templates/deliverables/longform-research-report.md` | 長片研究報告模板 | 建長片研究報告時用 |
| `templates/deliverables/shorts-topic-pack.md` | Shorts 主題包模板 | 建 Shorts 主題包時用 |
| `templates/deliverables/shorts-research-pack.md` | Shorts 研究包模板 | 建 Shorts 深度研究包時用 |
| `templates/memory/` | Query Log、Source Index、Decision Log 模板 | 建 run memory 時用 |
| `scripts/opencli_tooling.py` | 工具 readiness 與 transcript fallback | 正式研究前跑 |
| `scripts/opencli_research.py` | opencli 批次研究工具 | 需要批次蒐集時用 |
| `scripts/check_deliverable_shape.py` | 研究報告格式檢查 | 交付前跑 |
| `scripts/check_memory_completeness.py` | run folder 檢查 | 有 run folder 時跑 |
| `workspace/deliverables/longform-research/` | 長片研究報告與 package | 新長片研究成品放這裡 |
| `workspace/deliverables/shorts-topic/` | Shorts 主題包 | 新 Shorts 主題搜尋成品放這裡 |
| `workspace/deliverables/shorts-research/` | Shorts 研究包 | 新 Shorts 深度研究成品放這裡 |
| `workspace/memory/runs/` | 單次任務證據 | query log、來源、原文、字幕、留言 |
| `workspace/memory/games/` | 遊戲長期記憶 | 可回用判斷才更新 |

## 主流程

### Longform Research

```text
1. 讀 AGENTS.md
2. 讀 source-capture-research-rules.md
3. 讀 research-source-acquisition.md
4. 讀 opencli-tooling.md
5. 讀 channel_scope.md
6. 讀 longform-research.md
7. 判斷長片研究類型
8. 跑 opencli readiness
9. 建 run folder
10. 做跨語圈搜尋與站外來源搜尋
11. 擷取正文、字幕、逐字稿、留言或 OCR
12. 產生候選章節或使用者鎖定章節的研究卡
13. 產生 Longform Research Report
14. 打包 report、來源、字幕、query log、manifest
15. 跑檢查並回報限制
```

### Shorts Research

```text
1. 讀 AGENTS.md
2. 讀 source-capture-research-rules.md
3. 讀 research-source-acquisition.md
4. 讀 opencli-tooling.md
5. 讀 channel_scope.md
6. 讀 shorts-research.md
7. 讀 shorts_topic_research_rules.md
8. 判斷是 Shorts Topic Pack 或 Shorts Research Pack
9. 跑 opencli readiness
10. 建 run folder
11. 查 YouTube Shorts / TikTok / IG Reels / bilibili / 巴哈姆特
12. 保存標題、說明、留言、字幕、逐字稿或 OCR
13. 分主題簇，分析 hook / punch / 畫面節奏
14. 產生 Shorts Topic Pack 或 Shorts Research Pack
15. 打包 report、來源、字幕、query log、manifest
16. 跑檢查並回報限制
```

## 要改規則時去哪裡

- 頻道收不收某種遊戲：改 `docs/profiles/may-story/channel_scope.md`，必要時同步 `AGENTS.md`。
- 長片研究流程：改 `docs/workflows/longform-research.md`。
- Shorts 研究流程：改 `docs/workflows/shorts-research.md`。
- 原文與字幕保存規則：改 `docs/workflows/source-capture-research-rules.md`。
- 研究前厚資料蒐集與爬蟲工具建議：改 `docs/workflows/research-source-acquisition.md`。
- opencli 或字幕備援：改 `docs/workflows/opencli-tooling.md` 與相關腳本。
- 研究報告格式：改 `templates/deliverables/`、`scripts/check_deliverable_shape.py` 與測試。
- 任務路由：改 `docs/agents/skill-routing.md`。

## 什麼不要亂動

- 不要為了瘦身刪掉 `workspace/deliverables/` 舊稿，這些是頻道工作紀錄。
- 不要刪 `workspace/memory/runs/` 的查詢證據，除非使用者明確說要清。
- 不要把 Shorts 寫稿或 finalizer 重新設成研究任務主入口。
- 不要把 `.auth/`、`.env`、`cookies.txt` 這類憑證檔加入版本控制。
- 不要把 `__pycache__/`、`.pytest_cache/`、暫存音訊或下載片段當正式專案內容。

## 舊文件狀態

以下文件仍可使用，但不是研究任務主入口：

- `docs/profiles/may-story/shorts_rules.md`
- `prompts/shorts-writing.md`
- `prompts/script-writing.md`
- `skills/maymei-script-finalizer/`
- `docs/workflows/monthly-game-recommendations.md`

以下 Shorts 研究文件已恢復為正式入口：

- `docs/profiles/may-story/shorts_topic_research_rules.md`
- `prompts/shorts-topic-research.md`
- `docs/workflows/shorts-research.md`
- `templates/deliverables/shorts-topic-pack.md`
- `templates/deliverables/shorts-research-pack.md`
