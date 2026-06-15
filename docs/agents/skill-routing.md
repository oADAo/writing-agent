# Skill Routing

Use this file to decide which skill, workflow, or local rule set applies before changing this repo.

## Always Start Here

1. Read `AGENTS.md`.
2. Read `docs/project-map.md`.
3. If the task touches sources, read `docs/workflows/source-capture-research-rules.md`.
4. If the task uses search, captions, transcripts, or web reading, read `docs/workflows/opencli-tooling.md`.
5. Route to the matching research workflow:
   - Longform: `docs/workflows/longform-research.md`
   - Shorts: `docs/workflows/shorts-research.md`

## Current Product Scope

This repo is now a Maymei research agent with two formal research routes.

Default longform route:

```text
longform topic / guide research
-> chapter plan
-> source capture
-> Longform Research Report
```

Default Shorts route:

```text
Shorts topic search / Shorts research pack
-> cross-platform short-video evidence
-> hook / punch / production research
-> Shorts Topic Pack or Shorts Research Pack
```

Do not route new tasks to Shorts writing, final script writing, Maymei voice scoring, or Google Docs final copy unless the user explicitly asks to temporarily leave the research scope.

## Task To Skill / Workflow Map

| User intent | Use this first | Then read |
| --- | --- | --- |
| Longform game topic research | local workflow | `docs/workflows/longform-research.md`, `prompts/topic-research.md` |
| Buy-before longform research | local workflow | `docs/workflows/longform-research.md`, `docs/profiles/may-story/channel_scope.md` |
| Beginner guide / strategy research | local workflow | `docs/workflows/longform-research.md`, `docs/workflows/source-capture-research-rules.md` |
| Longform deep research pack / detailed report | local workflow | `docs/workflows/longform-research.md`, `templates/deliverables/longform-research-report.md` |
| Shorts topic search | local workflow | `docs/workflows/shorts-research.md`, `docs/profiles/may-story/shorts_topic_research_rules.md`, `prompts/shorts-topic-research.md` |
| Shorts research pack / reference short analysis | local workflow | `docs/workflows/shorts-research.md`, `templates/deliverables/shorts-research-pack.md` |
| Source capture / transcripts / web body extraction | local workflow | `docs/workflows/source-capture-research-rules.md`, `docs/workflows/opencli-tooling.md` |
| Organize repo, clarify file responsibility | architecture review | `docs/project-map.md`, `docs/agents/*.md` |
| Implement script or validation changes | `tdd` if behavior changes | relevant tests under `tests/` |
| Debug failing tools or tests | `diagnose` or `systematic-debugging` | failing command output and related tests |
| Final verification | `verification-before-completion` | exact commands and outputs |

## Explicit Non-Default Routes

These are not current default behavior:

- `skills/maymei-script-finalizer/`
- `prompts/script-writing.md`
- `prompts/shorts-writing.md`
- `docs/workflows/monthly-game-recommendations.md`

Only use them when the user explicitly says to leave the research scope. If the user asks for Shorts research, use `docs/workflows/shorts-research.md`, not Shorts writing.

## Required Checks

Longform:

```powershell
python scripts/check_deliverable_shape.py <research-report.md> --mode longform-research
```

Shorts topic:

```powershell
python scripts/check_deliverable_shape.py <shorts-topic-pack.md> --mode shorts-topic
```

Shorts research:

```powershell
python scripts/check_deliverable_shape.py <shorts-research-pack.md> --mode shorts-research
```

All docs:

```powershell
python scripts/check_docs_consistency.py
```

If there is a run folder, also check that it contains query log, sources, source originals, transcripts where available, tool readiness, and package manifest.

## Do Not Use Skills To Do These

- Do not use finalizer skills to turn research into a finished script.
- Do not use Shorts writing workflows for Shorts research.
- Do not create Google Docs for research packs unless the user asks.
- Do not move old deliverables or run memory just to make the tree look cleaner.
