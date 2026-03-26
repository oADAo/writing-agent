# 玫玫物語 Shorts Topic Research Design

**Goal:** 在現有長片主題研究之外，新增第 5 個工作模式 `熱門 Shorts 主題搜尋`，專門研究短影音題型，輸出可直接接到 Shorts 寫稿流程的題目包。

## Product Scope

### In Scope
- 新增第 5 個工作模式：`熱門 Shorts 主題搜尋`
- 將現有 `熱門主題搜尋` 明確收斂為長片題材研究
- 為短影音研究建立獨立規則、prompt、deliverable template
- 固定研究 `中文 / 日文 / 英文` 三個語圈
- 固定研究 `YouTube Shorts / TikTok / IG Reels / 巴哈姆特 / bilibili` 五個主平台
- 輸出 `Shorts Topic Pack`，每個候選方向都附一句題目提案、可能 hook、適合模仿的節奏來源與查詢證據

### Out of Scope
- 不直接撰寫 Shorts 完整口播稿
- 不生成標題包、封面圖、剪輯腳本、字幕切軸
- 不把 `巴哈姆特` 或 `bilibili` 視為長片研究的固定主平台
- 不把模式 5 併回模式 1

## Why A Separate Mode

- 長片主題研究看的是搜尋需求、攻略需求、機制需求與跨來源驗證。
- Shorts 主題研究看的是短影音題型簇、hook 簇、留言共鳴、節奏模板與跨平台複製情況。
- 同一個遊戲在長片與 Shorts 的熱門角度經常不同，混用規則會讓 agent 把長片爆點誤判成短影音機會。

## Design Principles

- 模式 5 只研究短影音題型，不研究長影片題材。
- 不以單支爆片直接推主結論，而是先找重複出現的題型簇。
- 中文圈不能缺席，不能只用英文或日文爆款倒推中文。
- 交付物必須能直接接到下一步 `Shorts 文本撰寫`，不能只停在抽象市場觀察。
- 每次都要留下實際查詢證據，平台樣本不足也要明寫。

## Research Model

### Fixed Coverage
- 語圈固定查：`中文 / 日文 / 英文`
- 主平台固定查：`YouTube Shorts / TikTok / IG Reels / 巴哈姆特 / bilibili`

### Research Focus
- 先整理 `題型簇 / punch 簇 / hook 簇 / 留言共鳴簇`
- 再判斷哪些題型可以自然轉成 `玫玫物語` 會做的中文 Shorts
- 每個候選方向都要產出可執行的題目包，而不是只有市場描述

## Deliverable Contract

### Output Format
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

### Required Fields Per Topic Option
- `Topic Cluster`
- `Why It’s Moving`
- `Platform Evidence`
- `Cross-Language Evidence`
- `One-Line Topic Pitch`
- `Possible Hook`
- `Rhythm / Format Reference`
- `Chinese Audience Fit`
- `Use / Skip`

## Hotness Criteria

### Baseline Valid Topic
只有符合下列其中一條，才算成立的熱門 Shorts 題型：

- 同主題在至少 `2 個語圈` 都反覆出現
- 同語圈至少 `2 個主平台` 都出現相近題型、hook 或 punch
- 同語圈有 `2 位以上` 表現不差的創作者都在做，而且不是只紅單一支

### Top 1 Recommendation Gate
如果要推成 `Top 1 Recommendation`，還要再通過下列條件：

- 至少有 `1 個短影音平台` 的直接證據
- 至少有 `1 個中文圈平台` 的直接證據
- 至少有 `1 個跨語圈` 的對照證據
- 題型能在前 `1-3 秒` 成立 hook
- 可以自然轉成中文，不會過度依賴外語文化脈絡
- 題材符合 `玫玫物語` 的遊戲邊界與觀眾需求
- 題目能直接延伸成一篇可寫的 Shorts 文稿
- 題目的時效窗口仍在，不是已經過掉的單次事件熱度

### Analyst Questions
研究時需要明確回答：

- 這是 `題型` 還是只是 `單支影片事件`
- 這是 `可複製的熱門` 還是只是 `一次性爆點`
- 高讚留言反映的是哪種共鳴：`驚訝 / 荒謬 / 實用 / 吐槽 / 反差 / 發現`
- 中文圈最可能買單的是哪個情緒點或資訊點
- 題目更適合哪種短影音包裝與節奏

## Root Controller Changes

### AGENTS.md
- 將支援模式從 4 個改為 5 個
- 將模式 1 明確標記為長片主題研究
- 新增模式 5 的必讀文件、工作目標、輸出格式、熱門判準與禁止事項
- 補上新的推薦使用方式

### Supporting Docs
- `README.md` 需更新功能數量、模式說明、固定輸出格式與使用示例
- `docs/how-to-use-this-agent.md` 需加入新模式與新入口句
- `docs/workflows/content-production.md` 需反映模式 5 如何接到模式 4
- `examples/output-outline.md` 需補上 `Shorts Topic Pack` 骨架

## New Files

### Profile Rule Layer
- `docs/profiles/may-story/shorts_topic_research_rules.md`
  - 定義模式 5 的平台範圍、語圈範圍、熱門判準、證據要求、題目包格式

### Prompt Layer
- `prompts/shorts-topic-research.md`
  - 指定必讀文件、研究順序、輸出格式與禁止事項

### Deliverable Template
- `templates/deliverables/shorts-topic-pack.md`
  - 提供固定 `Shorts Topic Pack` 結構

## Validation Impact

- `scripts/check_docs_consistency.py` 需要把第 5 模式相關文件納入一致性檢查
- `scripts/check_deliverable_shape.py` 需要新增 `shorts-topic` 模式，檢查新 deliverable 的必填區塊
- 相關測試需要更新以反映新模式與新模板

## Risks and Guardrails

- 如果沿用長片主題規則，agent 會過度偏向搜尋需求，而漏掉短影音節奏與共鳴。
- 如果只看單支爆片，會把一次性事件誤判成可穩定複製的題型。
- 如果不固定查中文圈平台，會高估外語熱門在中文圈的可轉譯性。
- 如果不要求每題附 `One-Line Topic Pitch / Possible Hook / Rhythm Reference`，模式 5 很難順利銜接模式 4。

## Verification Plan

- 確認 `AGENTS.md` 已明確區分模式 1 與模式 5
- 確認新增規則檔、prompt 檔與 deliverable template
- 確認 README、how-to-use、workflow、examples 都反映第 5 模式
- 確認 deliverable shape 檢查可驗證 `Shorts Topic Pack`
