# Maymei YouTube Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 將 repo 設定成只服務玫玫物語頻道的 YouTube 內容 agent，支援分步執行的主題研究、標題封面方向、長影片腳本三個流程。

**Architecture:** 以根目錄 `AGENTS.md` 作為總控，將頻道邊界、主題研究規則、標題封面規則拆到 `docs/profiles/may-story/`，並同步更新三份 prompt、workflow 與 README，讓 repo 結構與使用方式一致。

**Tech Stack:** Markdown documentation, repo conventions, existing profile docs

---

### Task 1: 建立頻道邊界與規則文件

**Files:**
- Create: `docs/profiles/may-story/channel_scope.md`
- Create: `docs/profiles/may-story/topic_research_rules.md`
- Create: `docs/profiles/may-story/title_thumbnail_rules.md`
- Reference: `docs/profiles/may-story/content_rules.md`
- Reference: `docs/profiles/may-story/voice_memory.md`

- [ ] **Step 1: 定義頻道 scope**

寫出頻道定位、遊戲類型邊界、受眾、常見題型、明確排除項目。

- [ ] **Step 2: 寫主題研究規則**

明確規定跨中文、日文、英文三語圈查找競品與熱門題型，並固定輸出格式。

- [ ] **Step 3: 寫標題與封面方向規則**

明確規定只交付標題、封面文案、構圖方向，不直接生圖。

- [ ] **Step 4: 檢查新文件與既有腳本規則不衝突**

Run: `sed -n '1,220p' docs/profiles/may-story/channel_scope.md docs/profiles/may-story/topic_research_rules.md docs/profiles/may-story/title_thumbnail_rules.md`
Expected: 新文件用語一致，且沒有覆蓋 `content_rules.md` / `voice_memory.md` 的聲線優先順序

### Task 2: 建立根目錄 AGENTS 控制文件

**Files:**
- Create: `AGENTS.md`
- Reference: `docs/profiles/may-story/channel_scope.md`
- Reference: `docs/profiles/may-story/topic_research_rules.md`
- Reference: `docs/profiles/may-story/title_thumbnail_rules.md`
- Reference: `docs/profiles/may-story/content_rules.md`
- Reference: `docs/profiles/may-story/voice_memory.md`
- Reference: `docs/profiles/may-story/script_template.md`

- [ ] **Step 1: 寫 AGENTS.md 的角色與邊界**

明寫此 agent 只服務玫玫物語、只支援三個分步模式、不得擅自跳步。

- [ ] **Step 2: 串接必讀文件**

對三個模式分別指定先讀哪些檔案、哪些情況必須上網查證。

- [ ] **Step 3: 定義固定輸出要求**

在 AGENTS.md 中總結三個模式的交付格式與核心禁止行為。

- [ ] **Step 4: 重新檢查 AGENTS.md**

Run: `sed -n '1,260p' AGENTS.md`
Expected: 可以單獨閱讀並理解 agent 如何工作，且與 profile docs 對齊

### Task 3: 更新 prompts、workflow、README 與範例

**Files:**
- Modify: `prompts/topic-research.md`
- Modify: `prompts/title-ideation.md`
- Modify: `prompts/script-writing.md`
- Modify: `docs/workflows/content-production.md`
- Modify: `examples/output-outline.md`
- Modify: `README.md`

- [ ] **Step 1: 升級三份 prompt**

每份 prompt 都要補齊：使用時機、必讀文件、輸出格式、禁止行為。

- [ ] **Step 2: 更新 workflow**

明寫三步分開執行，不自動串步驟。

- [ ] **Step 3: 更新範例輸出**

讓範例對齊新的 Topic Brief / Title Pack / Script Package 結構。

- [ ] **Step 4: 更新 README**

反映新增檔案與新的使用方式。

- [ ] **Step 5: 驗證文件互相引用一致**

Run: `rg -n "topic_research_rules|title_thumbnail_rules|channel_scope|Topic Brief|Title Pack|Script Package" README.md AGENTS.md docs prompts examples`
Expected: 引用名稱一致，沒有舊格式殘留

### Task 4: 最終驗證

**Files:**
- Verify: `AGENTS.md`
- Verify: `README.md`
- Verify: `docs/profiles/may-story/channel_scope.md`
- Verify: `docs/profiles/may-story/topic_research_rules.md`
- Verify: `docs/profiles/may-story/title_thumbnail_rules.md`
- Verify: `prompts/topic-research.md`
- Verify: `prompts/title-ideation.md`
- Verify: `prompts/script-writing.md`
- Verify: `docs/workflows/content-production.md`
- Verify: `examples/output-outline.md`

- [ ] **Step 1: 查看 git status**

Run: `git status --short`
Expected: 目前 repo 尚未有初始 commit，所以會看到整批文件是未追蹤狀態；確認沒有超出本次範圍的意外路徑

- [ ] **Step 2: 人工檢查流程完整性**

確認使用者可透過三種指令完成分步工作：
- 只做主題研究
- 只做標題與封面方向
- 只做長影片腳本

- [ ] **Step 3: 準備交付摘要**

列出新增文件、更新重點、驗證命令結果與尚未做的項目（若有）
