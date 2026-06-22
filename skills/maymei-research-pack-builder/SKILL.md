---
name: maymei-research-pack-builder
description: Use when preparing objective Maymei evidence catalogs, source-backed research packs, transcript/comment capture, multilingual game research, or neutral material for a separate writing project.
---

# Maymei Research Pack Builder

## Core Rule

Build a writing-neutral evidence catalog. The research task is to capture, preserve, classify, and map evidence; the writing project decides angle, voice, thesis, pacing, and final judgment.

Search hits, titles, snippets, thumbnails, AI summaries, and store blurbs are leads only. Evidence requires readable body text, transcripts, subtitles, high-signal comments, OCR, or user-provided material.

Do not turn evidence into recommendations unless the user explicitly asks for a separate writing brief.

## Required Repo Start

1. Read `AGENTS.md`, `docs/project-map.md`, `docs/agents/skill-routing.md`, `docs/workflows/source-capture-research-rules.md`, `docs/workflows/research-source-acquisition.md`, `docs/workflows/opencli-tooling.md`, and `docs/profiles/may-story/channel_scope.md`.
2. Route the task:
   - Longform: read `docs/workflows/longform-research.md`, `prompts/topic-research.md`, and `templates/deliverables/longform-research-report.md`.
   - Shorts: read `docs/workflows/shorts-research.md`, `docs/profiles/may-story/shorts_topic_research_rules.md`, and the matching template.
3. Read references as needed:
   - Always: `references/evidence-quality-contract.md`
   - Source capture: `references/platform-capture-playbook.md`
   - Delivery and checks: `references/deliverable-contract.md`

## Evidence Workflow

1. Create a run folder before research: `workspace/memory/runs/<timestamp>-<mode>-<slug>/`.
2. Run tool readiness and save it in the run folder:
   ```powershell
   python scripts/opencli_tooling.py ensure --update --run-dir "<run-dir>\tool-readiness"
   ```
3. If readiness wrapper fails, run platform smoke tests before giving up. Do not silently downgrade to title-only research.
4. Search by language market: Traditional/Simplified Chinese, English, Japanese. Aim for 20 candidates per language for major topics, but report the real validated count separately.
5. Capture enough source families for the task:
   - Longform: official facts, YouTube transcripts, YouTube comments, bilibili, Reddit/Steam/Bahamut, guide sites, and at least two non-official community types.
   - Shorts: YouTube Shorts `/shorts/`, TikTok, Reels, bilibili, and community reactions when available.
6. For every source, record: query, platform, language, command, URL, capture method, evidence file, actual text read, neutral claim IDs, source status, and inclusion decision.
7. Extract facts, not angles:
   - Observed text: what the source literally says, shows, measures, or reports.
   - Extracted facts: verifiable statements with source paths.
   - Claim map: which evidence supports, conflicts with, or limits each neutral claim.
   - Limits: what the source does not prove.
8. For攻略 tasks, extract exact process, prerequisites, systems/items/characters/settings, efficiency numbers, stability, failure causes, version risk, and in-game verification needs. Mark every efficiency claim by source tier.

## Writing Boundary

Default research output must stay objective. Do not include:

- Recommended angle, thesis, or final judgment.
- "Worth doing", "best hook", "must mention", or "core selling point" language.
- Final title, script outline, Claude Code prompt, writer handoff, or suggested conclusion.
- Unlabeled audience-fit claims such as "Taiwan viewers will care" unless directly backed by captured comments or platform data.

Allowed output by default:

- Evidence Pack: saved originals, transcripts, comments, OCR, metadata, and data snapshots.
- Claim Map: neutral, verifiable claim IDs mapped to source artifacts.
- Source Index: source status, evidence level, language, platform, capture method, and paths.
- Gap Report: missing evidence, blocked platforms, thin language coverage, and in-game verification needs.
- Candidate Structure: only when useful for navigation; mark it as `candidate`, `user-locked`, or `evidence-group`, not as a recommendation.

If the user explicitly asks for writing support, create a separate file labeled `writing-brief` or `interpretation`. Keep it outside the evidence layer and state that it is a writing aid, not objective evidence.

## Source Weighting

Use this hierarchy:

| Weight | Evidence |
| --- | --- |
| Primary | Full webpage body, transcript/subtitle, saved comment body, OCR/user evidence |
| Supporting | Official pages for facts, metadata with comments, creator description with comments |
| Lead only | Search results, snippets, titles, thumbnails, store short descriptions, AI summaries |

High views are not enough. A video without transcript, subtitle, readable description, or useful comments is a candidate, not a research source.

## Comment Rules

Prioritize comments with likes, replies, timestamps, correction of outdated advice, concrete steps, failure reports, or version warnings. Save raw comment text and do not paraphrase away the signal. Mark whether the comment supports, challenges, or updates the creator's claim.

## Required Output

Deliver an objective evidence package, not a narrative outline:

- Formal evidence pack or research pack in the correct deliverable folder.
- `query-log-reviewed.md`
- `sources.md` with validated sources, not only candidates.
- `claim-map.md` mapping neutral claims to evidence artifacts.
- `sources-candidates-opencli.md` or equivalent raw candidate list.
- `source-originals/` and `transcripts/`
- `tool-readiness/`
- `source-capture-status.md`
- `PACKAGE-MANIFEST.md`
- Zip package next to the formal evidence pack.

Do not include writing prompts or suggested conclusions in the default package.

## Failure Handling

If a platform fails, try the fallback path in `references/platform-capture-playbook.md`. If it still fails, write the failed command, error, attempted fallback, and effect on source weighting. Never invent coverage to satisfy a count target.

## Verification

Before final response, run the relevant shape check, `python scripts/check_docs_consistency.py`, `python scripts/check_memory_completeness.py <run-dir>` if a run folder exists, and confirm the zip exists. Report exact pass/fail status.
