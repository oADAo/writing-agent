# Maymei Shorts Topic Research Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a fifth workflow mode, `熱門 Shorts 主題搜尋`, with dedicated docs, prompt, deliverable template, and validation support.

**Architecture:** Keep long-form topic research and short-form topic research as separate modes at the root controller level. Add one new profile rules file, one new prompt, one new deliverable template, then update repo-facing docs and validation scripts so the new mode is treated as first-class rather than an ad hoc variation of topic research.

**Tech Stack:** Markdown docs, Python validation scripts, unittest

---

### Task 1: Update root mode definitions and public docs

**Files:**
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `docs/how-to-use-this-agent.md`
- Modify: `docs/workflows/content-production.md`
- Modify: `examples/output-outline.md`

- [ ] **Step 1: Write the failing doc expectations down**

Add a local checklist of the required new statements before editing:

```text
- AGENTS.md says 5 modes, not 4
- mode 1 explicitly means long-form topic research
- mode 5 is named 熱門 Shorts 主題搜尋
- README and how-to-use list the new mode and example prompt
- workflow explains mode 5 feeds mode 4
- output-outline includes Shorts Topic Pack
```

- [ ] **Step 2: Edit `AGENTS.md` to add the new mode**

Implement:
- change the global mode count from 4 to 5
- update disambiguation bullets so users can ask for Shorts topic research explicitly
- rename mode 1 wording so it clearly targets long-form topics
- add full mode 5 section with:
  - required files to read
  - fixed platforms and languages
  - deliverable format
  - hotness criteria
  - forbidden behaviors
  - recommended natural-language entrypoints

- [ ] **Step 3: Update repo-facing docs**

Implement:
- `README.md`: reflect 5 modes, add mode 5 explanation and deliverable format
- `docs/how-to-use-this-agent.md`: add the new mode and example command
- `docs/workflows/content-production.md`: describe the 5-step model and how mode 5 hands off to mode 4
- `examples/output-outline.md`: add `Shorts Topic Pack` skeleton with topic-option subfields

- [ ] **Step 4: Run docs consistency check**

Run: `python3 scripts/check_docs_consistency.py`
Expected: PASS after all docs are updated

- [ ] **Step 5: Commit**

```bash
git add AGENTS.md README.md docs/how-to-use-this-agent.md docs/workflows/content-production.md examples/output-outline.md
git commit -m "docs: add shorts topic research mode"
```

### Task 2: Add dedicated rules, prompt, and deliverable template

**Files:**
- Create: `docs/profiles/may-story/shorts_topic_research_rules.md`
- Create: `prompts/shorts-topic-research.md`
- Create: `templates/deliverables/shorts-topic-pack.md`

- [ ] **Step 1: Write the failing shape for the new deliverable**

Prepare the exact target headings:

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

- [ ] **Step 2: Write `shorts_topic_research_rules.md`**

Include:
- fixed language coverage: `中文 / 日文 / 英文`
- fixed platforms: `YouTube Shorts / TikTok / IG Reels / 巴哈姆特 / bilibili`
- baseline hotness criteria and Top 1 gate
- required topic-option fields
- rules for handling weak platform samples
- explicit separation from long-form topic research

- [ ] **Step 3: Write `shorts-topic-research.md`**

Include:
- required reads
- research process order
- evidence requirements
- output format contract
- reminders not to confuse a single viral clip with a repeatable format

- [ ] **Step 4: Write `shorts-topic-pack.md`**

Implement a reusable template that mirrors the required headings and includes one sample topic-option block with:
- `Topic Cluster`
- `Why It’s Moving`
- `Platform Evidence`
- `Cross-Language Evidence`
- `One-Line Topic Pitch`
- `Possible Hook`
- `Rhythm / Format Reference`
- `Chinese Audience Fit`
- `Use / Skip`

- [ ] **Step 5: Commit**

```bash
git add docs/profiles/may-story/shorts_topic_research_rules.md prompts/shorts-topic-research.md templates/deliverables/shorts-topic-pack.md
git commit -m "feat: add shorts topic research docs"
```

### Task 3: Extend validation scripts for the new mode

**Files:**
- Modify: `scripts/check_docs_consistency.py`
- Modify: `scripts/check_deliverable_shape.py`
- Test: `tests/test_check_docs_consistency.py`
- Test: `tests/test_check_deliverable_shape.py`

- [ ] **Step 1: Write the failing tests**

Add tests that fail until the scripts know about `Shorts Topic Pack`:

```python
content = """# Shorts Topic Pack

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
"""
```

- [ ] **Step 2: Extend docs consistency expectations**

Update `scripts/check_docs_consistency.py`:
- add `Shorts Topic Pack` to `EXPECTED_PACKAGES`
- add `prompts/shorts-topic-research.md` to default checked paths

- [ ] **Step 3: Extend deliverable mode detection**

Update `scripts/check_deliverable_shape.py`:
- add mode key `shorts-topic`
- set title to `Shorts Topic Pack`
- require all new sections

- [ ] **Step 4: Run targeted tests**

Run: `python3 -m unittest tests.test_check_docs_consistency tests.test_check_deliverable_shape -v`
Expected: PASS

- [ ] **Step 5: Run deliverable shape checks on templates**

Run: `python3 scripts/check_deliverable_shape.py templates/deliverables/shorts-topic-pack.md --mode shorts-topic`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add scripts/check_docs_consistency.py scripts/check_deliverable_shape.py tests/test_check_docs_consistency.py tests/test_check_deliverable_shape.py
git commit -m "test: validate shorts topic research mode"
```

### Task 4: End-to-end verification sweep

**Files:**
- Verify only

- [ ] **Step 1: Run the full docs consistency check**

Run: `python3 scripts/check_docs_consistency.py`
Expected: `Docs consistency check passed.`

- [ ] **Step 2: Run the full unit test suite**

Run: `python3 -m unittest`
Expected: PASS

- [ ] **Step 3: Spot-check the new public contract**

Verify manually:
- `AGENTS.md` exposes 5 modes and lists mode 5 correctly
- `README.md` and `docs/how-to-use-this-agent.md` mention the new example command
- `templates/deliverables/shorts-topic-pack.md` matches the rules file

- [ ] **Step 4: Final commit if verification edits were needed**

```bash
git add .
git commit -m "chore: finalize shorts topic research mode"
```
