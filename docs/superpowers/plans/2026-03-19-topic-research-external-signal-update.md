# Topic Research External Signal Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 `熱門主題搜尋` 的規則更新成每次都必查 YouTube 以外的高流量社群 / 論壇 / 攻略站，並在輸出中留下可驗證的查詢證據。

**Architecture:** 這次修改只動文件，不改程式邏輯。核心做法是同步更新 `AGENTS.md`、研究規則文件、研究 prompt，讓工作模式定義、執行規格與 prompt 指令完全一致，並加入查詢證據與跨來源驗證欄位。

**Tech Stack:** Markdown, repo documentation

---

### Task 1: Update Agent-Level Requirements

**Files:**
- Modify: `AGENTS.md`

- [ ] **Step 1: Update common rules**

加入「每次熱門主題搜尋都必查高流量社群 / 論壇 / 攻略站」與「必須附查詢證據」的共通規則。

- [ ] **Step 2: Update mode 1 requirements**

補上主題研究時的站外高訊號來源要求、交叉比對要求與輸出欄位要求。

- [ ] **Step 3: Review wording for consistency**

確認用語和 `topic_research_rules.md`、`prompts/topic-research.md` 相容，避免一處寫「社群」，另一處只剩「論壇」。

### Task 2: Expand Topic Research Rules

**Files:**
- Modify: `docs/profiles/may-story/topic_research_rules.md`

- [ ] **Step 1: Add mandatory source layers**

把研究範圍改成固定涵蓋 `官方 / YouTube / 社群平台 / 論壇與攻略站 / 搜尋需求`。

- [ ] **Step 2: Add high-signal source criteria**

定義什麼叫高流量、高訊號來源，並明確說明平台名單只作示例，不可侷限。

- [ ] **Step 3: Add query evidence and validation rules**

加入查詢證據要求、資料不足時的處理方式，以及 YouTube 與站外來源交叉驗證規則。

- [ ] **Step 4: Update fixed output format**

新增 `Query Log`、`Community / Forum Signals`、`Cross-Source Validation` 等欄位。

### Task 3: Update Prompt and Verify Alignment

**Files:**
- Modify: `prompts/topic-research.md`

- [ ] **Step 1: Mirror the new hard rules in the prompt**

把每次必查、查詢證據、跨來源驗證等要求補進 prompt。

- [ ] **Step 2: Mirror the new output structure**

讓 prompt 輸出格式和規則文件完全一致。

- [ ] **Step 3: Verify file alignment**

Run: `rg -n "Query Log|Community / Forum Signals|Cross-Source Validation|每次都必查|查詢證據" AGENTS.md docs/profiles/may-story/topic_research_rules.md prompts/topic-research.md`

Expected: 三份文件都能找到對應規則，且沒有互相矛盾的舊欄位定義。
