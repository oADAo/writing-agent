# Maymei Conversation Workbench Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 repo 整理成可用的對話驅動工作台，補齊自然語言使用說明、工作區結構、模板與驗證腳本。

**Architecture:** 保留既有 `AGENTS.md` 與 profile/prompt 文件作為規則來源，新增 `workspace/`、`templates/`、`scripts/` 與 `tests/`。驗證腳本使用 Python 標準函式庫與 `unittest`，不新增外部依賴；文件層統一固定輸出格式，工作層透過模板與檢查器降低漂移。

**Tech Stack:** Markdown, Python 3 standard library, unittest, git

---

### Task 1: Establish repository structure and tracked workspace skeleton

**Files:**
- Modify: `.gitignore`
- Create: `docs/how-to-use-this-agent.md`
- Create: `workspace/.gitkeep`
- Create: `workspace/deliverables/.gitkeep`
- Create: `workspace/deliverables/topic/.gitkeep`
- Create: `workspace/deliverables/title/.gitkeep`
- Create: `workspace/deliverables/script/.gitkeep`
- Create: `workspace/deliverables/shorts/.gitkeep`
- Create: `workspace/memory/.gitkeep`
- Create: `workspace/memory/runs/.gitkeep`
- Create: `workspace/memory/games/.gitkeep`
- Create: `templates/deliverables/topic-brief.md`
- Create: `templates/deliverables/title-pack.md`
- Create: `templates/deliverables/script-package.md`
- Create: `templates/deliverables/shorts-package.md`
- Create: `templates/memory/run-request.md`
- Create: `templates/memory/query-log.md`
- Create: `templates/memory/source-index.md`
- Create: `templates/memory/decision-log.md`
- Create: `templates/memory/game-memory.md`

- [ ] **Step 1: Create the workspace and template directories**

Run: `mkdir -p workspace/deliverables/{topic,title,script,shorts} workspace/memory/{runs,games} templates/deliverables templates/memory`
Expected: directories exist with no errors

- [ ] **Step 2: Add keep files and update ignore rules**

Use `apply_patch` to:
- add `.worktrees/` and `output/` to `.gitignore`
- add `.gitkeep` files so empty directories are tracked

- [ ] **Step 3: Write deliverable templates**

Use `apply_patch` to create:
- `templates/deliverables/topic-brief.md`
- `templates/deliverables/title-pack.md`
- `templates/deliverables/script-package.md`
- `templates/deliverables/shorts-package.md`

Each template must include the exact required section headings from the spec.

- [ ] **Step 4: Write memory templates**

Use `apply_patch` to create:
- `templates/memory/run-request.md`
- `templates/memory/query-log.md`
- `templates/memory/source-index.md`
- `templates/memory/decision-log.md`
- `templates/memory/game-memory.md`

Each template must reflect the fields the validators will later enforce.

- [ ] **Step 5: Add user-facing usage doc**

Use `apply_patch` to create `docs/how-to-use-this-agent.md` with:
- supported modes
- natural-language request examples
- where deliverables are written
- where memory is written

### Task 2: Add failing tests for validation scripts

**Files:**
- Create: `tests/test_check_docs_consistency.py`
- Create: `tests/test_check_deliverable_shape.py`
- Create: `tests/test_check_memory_completeness.py`

- [ ] **Step 1: Write failing tests for docs consistency checks**

Create `tests/test_check_docs_consistency.py` using `unittest` that expects a checker to:
- report missing `Query Log` / `Community / Forum Signals` / `Cross-Source Validation` in malformed topic docs
- pass for well-formed topic docs

- [ ] **Step 2: Run the docs consistency tests to verify they fail**

Run: `python3 -m unittest tests.test_check_docs_consistency -v`
Expected: FAIL with import error or missing function because checker is not implemented yet

- [ ] **Step 3: Write failing tests for deliverable shape checks**

Create `tests/test_check_deliverable_shape.py` using `unittest` that expects a checker to:
- pass for each valid deliverable mode fixture
- fail when a required heading is missing

- [ ] **Step 4: Run the deliverable shape tests to verify they fail**

Run: `python3 -m unittest tests.test_check_deliverable_shape -v`
Expected: FAIL with import error or missing function because checker is not implemented yet

- [ ] **Step 5: Write failing tests for topic memory completeness**

Create `tests/test_check_memory_completeness.py` using `unittest` that expects a checker to:
- require `query-log.md`, `sources.md`, `decision-log.md`
- require platform, keyword, representative source, and inclusion markers

- [ ] **Step 6: Run the memory completeness tests to verify they fail**

Run: `python3 -m unittest tests.test_check_memory_completeness -v`
Expected: FAIL with import error or missing function because checker is not implemented yet

### Task 3: Implement reusable validation scripts

**Files:**
- Create: `scripts/__init__.py`
- Create: `scripts/check_docs_consistency.py`
- Create: `scripts/check_deliverable_shape.py`
- Create: `scripts/check_memory_completeness.py`
- Test: `tests/test_check_docs_consistency.py`
- Test: `tests/test_check_deliverable_shape.py`
- Test: `tests/test_check_memory_completeness.py`

- [ ] **Step 1: Implement docs consistency checker**

Create `scripts/check_docs_consistency.py` with:
- expected section maps per package
- helpers to extract headings from markdown or fenced markdown samples
- a `check_files(paths)` function returning structured failures
- a CLI entrypoint that exits non-zero on failure

- [ ] **Step 2: Run docs consistency tests to verify they pass**

Run: `python3 -m unittest tests.test_check_docs_consistency -v`
Expected: PASS

- [ ] **Step 3: Implement deliverable shape checker**

Create `scripts/check_deliverable_shape.py` with:
- per-mode required heading lists
- mode auto-detection from top-level title
- a `check_deliverable(path, mode=None)` function
- a CLI entrypoint accepting file paths

- [ ] **Step 4: Run deliverable shape tests to verify they pass**

Run: `python3 -m unittest tests.test_check_deliverable_shape -v`
Expected: PASS

- [ ] **Step 5: Implement memory completeness checker**

Create `scripts/check_memory_completeness.py` with:
- required files per mode, starting with `topic`
- content checks for required markers in `query-log.md`, `sources.md`, and `decision-log.md`
- a `check_topic_run(path)` function
- a CLI entrypoint accepting a run directory

- [ ] **Step 6: Run memory completeness tests to verify they pass**

Run: `python3 -m unittest tests.test_check_memory_completeness -v`
Expected: PASS

### Task 4: Align docs, prompts, and examples with the workbench model

**Files:**
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `docs/workflows/content-production.md`
- Modify: `examples/output-outline.md`
- Modify: `prompts/topic-research.md`
- Modify: `prompts/title-ideation.md`
- Modify: `prompts/script-writing.md`
- Modify: `prompts/shorts-writing.md`
- Reference: `docs/how-to-use-this-agent.md`

- [ ] **Step 1: Update agent-level docs**

Use `apply_patch` to update `AGENTS.md` and `README.md` so they:
- describe the repo as a conversation workbench
- explain `workspace/deliverables` vs `workspace/memory`
- include natural-language request examples

- [ ] **Step 2: Fix the workflow and example output formats**

Use `apply_patch` to update:
- `docs/workflows/content-production.md`
- `examples/output-outline.md`

Ensure `Topic Brief` now includes:
- `Query Log`
- `Community / Forum Signals`
- `Cross-Source Validation`

- [ ] **Step 3: Update prompts to reflect workbench behavior**

Use `apply_patch` to update all four prompt files so they:
- mention the exact fixed output structure
- reinforce writing evidence to memory for research-oriented tasks
- align wording with the README and AGENTS terminology

- [ ] **Step 4: Run docs consistency checker against the repo**

Run: `python3 scripts/check_docs_consistency.py`
Expected: PASS with no reported mismatches

### Task 5: End-to-end verification and sample artifact generation

**Files:**
- Create: `workspace/deliverables/topic/2026-03-19-sample-topic.md`
- Create: `workspace/memory/runs/2026-03-19-120000-topic-sample/request.md`
- Create: `workspace/memory/runs/2026-03-19-120000-topic-sample/query-log.md`
- Create: `workspace/memory/runs/2026-03-19-120000-topic-sample/sources.md`
- Create: `workspace/memory/runs/2026-03-19-120000-topic-sample/decision-log.md`
- Create: `workspace/memory/runs/2026-03-19-120000-topic-sample/result-snapshot.md`
- Create: `workspace/memory/games/sample-game/game-memory.md`
- Create: `workspace/memory/games/sample-game/source-index.md`
- Create: `workspace/memory/games/sample-game/open-questions.md`

- [ ] **Step 1: Create a sample topic deliverable from the template**

Use `apply_patch` to add a minimal but valid sample file at `workspace/deliverables/topic/2026-03-19-sample-topic.md`.

- [ ] **Step 2: Create a minimal valid topic run memory set**

Use `apply_patch` to add:
- `request.md`
- `query-log.md`
- `sources.md`
- `decision-log.md`
- `result-snapshot.md`

These files must satisfy the memory completeness checker.

- [ ] **Step 3: Create a minimal game memory set**

Use `apply_patch` to add:
- `game-memory.md`
- `source-index.md`
- `open-questions.md`

- [ ] **Step 4: Run deliverable and memory validators on the sample files**

Run: `python3 scripts/check_deliverable_shape.py workspace/deliverables/topic/2026-03-19-sample-topic.md`
Expected: PASS

Run: `python3 scripts/check_memory_completeness.py workspace/memory/runs/2026-03-19-120000-topic-sample`
Expected: PASS

- [ ] **Step 5: Run the full test suite**

Run: `python3 -m unittest discover -s tests -v`
Expected: PASS

- [ ] **Step 6: Review git status before final summary**

Run: `git status --short`
Expected: only files related to the conversation workbench implementation are changed or added
