# Shorts Research Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Shorts topic search and Shorts research packs as supported research workflows without restoring Shorts script writing as a default.

**Architecture:** Keep the repo as a research agent with two formal tracks: longform research and Shorts research. Shorts writing, final script writing, Maymei voice scoring, and Google Docs final copy remain non-default routes.

**Tech Stack:** Markdown workflow docs, deliverable templates, Python validation scripts, pytest.

---

### Task 1: Add Shorts Research Contract

**Files:**
- Create: `docs/workflows/shorts-research.md`
- Create: `templates/deliverables/shorts-research-pack.md`

- [ ] **Step 1: Define the workflow**

Add a Shorts workflow that requires `opencli_tooling.py ensure --update`, cross-platform Shorts search, source capture, reference Shorts records, and a package manifest.

- [ ] **Step 2: Define the deliverable template**

Add `# Shorts Research Pack` with sections for scope, Query Log, source capture, platform signals, topic clusters, reference Shorts evidence, hook/punch analysis, production notes, evidence table, and risks.

### Task 2: Promote Shorts Research Into Routing

**Files:**
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `docs/project-map.md`
- Modify: `docs/agents/skill-routing.md`
- Modify: `docs/how-to-use-this-agent.md`
- Modify: `docs/workflows/content-production.md`

- [ ] **Step 1: Update product scope**

Replace "longform only" wording with "research agent" wording that supports `Longform Research` and `Shorts Research`.

- [ ] **Step 2: Preserve non-default writing routes**

Keep Shorts writing, longform final drafts, Maymei voice scoring, and Google Docs final copy as explicit non-default workflows.

### Task 3: Update Validation

**Files:**
- Modify: `scripts/check_deliverable_shape.py`
- Modify: `scripts/check_docs_consistency.py`
- Modify: `tests/test_check_deliverable_shape.py`
- Modify: `tests/test_check_docs_consistency.py`
- Modify: `tests/test_opencli_research_workflow.py`
- Modify: `tests/test_shorts_template_scope.py`

- [ ] **Step 1: Add `shorts-research` mode**

Validate the new `Shorts Research Pack` title, required sections, and source-capture markers.

- [ ] **Step 2: Keep `shorts-topic` support**

Keep existing `Shorts Topic Pack` validation for focused topic searches.

- [ ] **Step 3: Update tests**

Tests should assert that Shorts topic search and Shorts research packs are formal research entrypoints, while `prompts/shorts-writing.md` remains non-default.

### Task 4: Verify

**Files:**
- No source changes.

- [ ] **Step 1: Run deliverable checks**

Run:

```powershell
python scripts/check_deliverable_shape.py templates/deliverables/shorts-topic-pack.md --mode shorts-topic
python scripts/check_deliverable_shape.py templates/deliverables/shorts-research-pack.md --mode shorts-research
python scripts/check_deliverable_shape.py templates/deliverables/longform-research-report.md --mode longform-research
python scripts/check_docs_consistency.py
```

- [ ] **Step 2: Run tests**

Run:

```powershell
python -m pytest -q
```
