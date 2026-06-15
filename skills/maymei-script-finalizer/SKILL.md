---
name: maymei-script-finalizer
description: Finalize a Maymei Story long-form script from a completed research pack by retrieving golden samples, applying formula cards, and running voice/fact checks.
---

# maymei-script-finalizer

## 使用時機

當使用者已經完成攻略研究，並要求「最終定稿」、「直接朗讀版」、「最終校正」、「跑 maymei-script-finalizer+」時，使用這個 skill。這個 skill 本體只負責把既有研究包收斂成 `玫玫物語` 長影片可朗讀正式稿；Shorts、標題封面和其他文稿仍要套用下方同一套中文撰寫系統，但入口在各自的 prompt。

## 全域撰寫規則

這個 skill 的完整 finalizer 流程只在長影片正式稿階段使用；但它底下的 `中文撰寫系統` 是全域規則。之後任何文稿型任務，只要會產出可被使用者採用的文字，都要先套用同一套核心流程：鎖事實、判片型、抓同片型樣本或歷史錨點、建立寫作卡、再做 AI 文風驗收與機械保底檢查。

適用範圍包含長影片腳本、Shorts 文本、標題與封面方向、推薦清單、排行稿、攻略稿、買前必看、文案素材包與使用者要求的最終定稿。即使使用者沒有明講 `跑 maymei finalizer`，只要任務是文稿撰寫，也要自動套用這套流程。

## Maymei Writing System v2

正式稿下筆前，必須先讀並套用：

- `docs/profiles/may-story/writing-retention-system.md`
- `docs/profiles/may-story/maymei-micro-voice-fingerprint.md`
- `docs/profiles/may-story/anti-ai-chinese-patterns.md`

v2 的關鍵不是最後去 AI 味，而是改變下筆順序：

1. 先建立 `包裝承諾卡`：標題 / 封面 / 前 30 秒承諾觀眾什麼。
2. 再建立 `玩家雙層問題卡`：表層問題和深層擔心要分開。
3. 每章建立 `章節留存卡`：觀眾問題、玫玫判斷、可用事實、玩家翻譯、B-roll 債務、下一章鉤子。
4. AI 第一輪先審大綱，不直接寫稿；找出資料腔、缺判斷、缺畫面和 AI 句型風險。
5. 審完後逐章寫，不一次生成整篇。
6. 完稿後先人工 Voice Check，再跑機械檢查。

如果使用者提供 AI 版和親改版，必須優先用 `scripts/learn_from_user_revision.py` 抽出 `AI 原句 -> 使用者改句`，再把轉換對放進 `workspace/memory/style-corpus/user-corrected-drafts/` 或對應任務記憶。

## 固定前提

- 先讀 `docs/profiles/may-story/content_rules.md`、`voice_memory.md`、`article_taxonomy.md`、`script_template.md`，再開始改稿。
- 樣本只提供語氣、節奏、結構與玩家對位，不提供正文事實。
- 正文只能使用攻略研究包中已確認的事實；不確定的版本、數值、掉落率、刷新條件都放進 `Fact Check Notes`。
- 高觀看只代表候選資格，不等於高品質；必須經過 `style forensics` 與 `formula card` 才能進 finalizer。
- 不模仿單篇爆款，不搬原句；用同類型多篇樣本歸納出可學結構。

## 樣本記憶建置

樣本庫不足或過期時，從 repo root 依序執行：

```powershell
python scripts/build_maymei_video_metrics.py
python scripts/build_maymei_golden_samples.py --target-count 100 --per-formula-cap 18
python scripts/analyze_maymei_style_samples.py
python scripts/build_maymei_formula_cards.py --min-samples 5
python scripts/build_maymei_writing_system.py
```

預設產物放在 `workspace/memory/style-corpus/`：

- `maymei-video-metrics.json`
- `maymei-golden-samples.json`
- `maymei-style-forensics.json`
- `maymei-formula-cards.json`
- `maymei-formula-cards.md`
- `maymei-writing-system.json`
- `maymei-writing-system.md`
- `maymei-writing-samples.jsonl`
- `maymei-line-transform-pairs.jsonl`

細節規則見 `references/golden-sample-selection.md`。
中文寫稿流程見 `references/chinese-writing-system.md`。

## 最終稿工作流

1. 從研究包先抽出可用事實，分成 `已確認`、`不要講死`、`不可使用`。
2. 判斷文案類型，例如新手開局、買前必看、效率刷法、Top 排行、配裝流派、機制拆解、完整路線攻略。
3. 讀 `references/chinese-writing-system.md`，並讀 `maymei-writing-system.json` 中對應片型的 decision card。
4. 建立 `包裝承諾卡` 與 `玩家雙層問題卡`。買前稿尤其要先確認這支片是在幫觀眾判斷首發、平台、版本、適合玩家，還是期待管理。
5. 用 `retrieve_maymei_writing_guidance.py` 取同片型寫作決策、樣本和轉換對：

```powershell
python scripts/retrieve_maymei_writing_guidance.py --topic "題目" --game "遊戲名" --formula "文案類型" --markdown --output workspace/memory/style-corpus/retrieved-writing-guidance.md
```

6. 必要時再用 `retrieve_maymei_samples.py` 取 3 篇主樣本與 2 篇輔助樣本：

```powershell
python scripts/retrieve_maymei_samples.py --topic "題目" --game "遊戲名" --formula "文案類型" --output workspace/memory/style-corpus/retrieved-samples.json
```

7. 先做每章 chapter card，不可直接寫全文。每章包含 `觀眾問題 / 玫玫判斷 / 可用事實 / 玩家翻譯 / B-roll 債務 / 下一章鉤子 / 禁用句型`。
8. AI 先審章節卡與大綱，標出 `keep / rewrite / cut / fact-risk / broll-missing`，通過後再寫正文。
9. 對照 `retrieved-writing-guidance.md`、`maymei-formula-cards.md`、`maymei-line-transform-pairs.jsonl`，逐章寫可朗讀稿。
10. 先做 AI 人工文風審稿，再跑機械文風驗收。AI 審稿不可只看禁用詞，必須逐章判斷：
   - 聽起來像不像中文口播，而不是英文文章翻譯。
   - 有沒有研究報告腔、資料交代腔、過度保守腔。
   - 每章是否有明確判斷，不只是整理資訊。
   - 章節標題和段落開頭是否太像模板。
   - 有沒有 `不是...而是...`、過度對稱、反覆修正型句法。

11. 跑機械文風驗收：

```powershell
python scripts/check_maymei_final_draft.py workspace/deliverables/script-writing/final-draft.md --json
python scripts/check_maymei_ai_patterns.py workspace/deliverables/script-writing/final-draft.md --json
python scripts/check_maymei_read_aloud_friction.py workspace/deliverables/script-writing/final-draft.md --json
```

12. 如果成品包含 B-roll 或留存卡，額外跑：

```powershell
python scripts/check_maymei_retention_beats.py workspace/deliverables/script-writing/final-draft.md --json
```

13. 分數低於 85，必須依 `Voice Check` 失敗項二修；即使分數通過，AI 人工審稿覺得不像人講話，也要二修。不要只修標點或換同義字。

## 交付格式

正式交付只包含：

```md
# Final Draft

# Voice Check

# Fact Check Notes
```

`Voice Check` 要列出 AI 人工審稿結論、機械檢查分數、是否通過 85 分、二修時修掉哪些問題。`Fact Check Notes` 要清楚標出哪些句子來自研究包，哪些資訊因為版本、條件或來源不足而保守處理。

## anti-AI 層

套用 `references/finalizer-rubric.md`。尤其注意：

- 禁止「總體來說」、「可以說是」、「對玩家來說是一個不錯的選擇」這類空泛總結。
- 禁止使用 `不是...而是...`、`不要...而是...` 當主要轉折句型；需要對比時改成直接講結論或拆成兩句。
- 避免連續使用「不只是 A，更是 B」等過度對稱句。
- 每 2 到 4 段至少要有一次體感型轉譯，把機制翻成玩家會怎麼省時間、少走路、變強或少踩坑。
- 每段都要有資訊推進；不能只是把研究包換句話重說。
