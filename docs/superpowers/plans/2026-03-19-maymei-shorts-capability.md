# Maymei Shorts Capability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 為 `玫玫物語` agent 新增 Shorts 文本撰寫模式，支援遊戲相關的短影音口播稿輸出。

**Architecture:** 新增一份 Shorts 專用 profile 規則與 prompt，並把 `AGENTS.md`、README、workflow、example 更新成 4 模式結構。Shorts 與長影片共用品牌聲線，但不共用結構規則。

**Tech Stack:** Markdown documentation, repo conventions, existing voice/profile docs

---

### Task 1: 新增 Shorts 規則與 Prompt

**Files:**
- Create: `docs/profiles/may-story/shorts_rules.md`
- Create: `prompts/shorts-writing.md`
- Reference: `docs/profiles/may-story/voice_memory.md`
- Reference: `docs/profiles/may-story/channel_scope.md`

- [ ] **Step 1: 寫 Shorts 規則**

定義 Shorts 的用途、適用題型、結構、長度、聲線與禁止行為。

- [ ] **Step 2: 寫 Shorts prompt**

定義必讀文件、任務目標、工作原則與固定輸出格式。

- [ ] **Step 3: 驗證規則與 prompt 對齊**

Run: `sed -n '1,220p' docs/profiles/may-story/shorts_rules.md prompts/shorts-writing.md`
Expected: 兩份文件對齊同一套輸出與聲線規則

### Task 2: 更新總控與使用文件

**Files:**
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `docs/workflows/content-production.md`
- Modify: `examples/output-outline.md`

- [ ] **Step 1: 更新 AGENTS.md**

新增第 4 模式，補齊必讀文件、輸出格式與禁止行為。

- [ ] **Step 2: 更新 README**

把 repo 介紹從 3 個模式改成 4 個模式，並補 Shorts 相關檔案與輸出格式。

- [ ] **Step 3: 更新 workflow 與 example**

讓使用方式與範例輸出反映 Shorts 能力。

- [ ] **Step 4: 驗證命名一致**

Run: `rg -n "Shorts Package|shorts-writing|shorts_rules|Shorts 文本" AGENTS.md README.md docs prompts examples`
Expected: 新模式名稱、檔名與輸出格式一致

### Task 3: 最終驗證

**Files:**
- Verify: `AGENTS.md`
- Verify: `README.md`
- Verify: `docs/profiles/may-story/shorts_rules.md`
- Verify: `prompts/shorts-writing.md`
- Verify: `docs/workflows/content-production.md`
- Verify: `examples/output-outline.md`

- [ ] **Step 1: 查看 git status**

Run: `git status --short`
Expected: 變更集中在本次新增 Shorts 能力相關檔案

- [ ] **Step 2: 檢查舊結構沒有被破壞**

確認主題研究、標題封面、長影片腳本三個既有模式仍可照原規則運作。

- [ ] **Step 3: 準備交付摘要**

列出新增模式、檔案與驗證結果
