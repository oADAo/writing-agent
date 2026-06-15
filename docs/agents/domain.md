# Domain Docs

This is a single-context repo for the `玫玫物語` research agent.

There is no root `CONTEXT.md` yet. Until one exists, skills should treat these files as the practical domain map.

## Required Starting Points

Read in this order:

1. `AGENTS.md`
2. `docs/project-map.md`
3. `docs/workflows/source-capture-research-rules.md`
4. `docs/workflows/opencli-tooling.md`
5. `docs/profiles/may-story/channel_scope.md`

Then route to:

- Longform: `docs/workflows/longform-research.md`, `prompts/topic-research.md`
- Shorts: `docs/workflows/shorts-research.md`, `docs/profiles/may-story/shorts_topic_research_rules.md`, `prompts/shorts-topic-research.md`

## Domain Vocabulary

Use the repo's own terms:

- `玫玫物語`
- `Longform Research`
- `長片研究`
- `長片主題研究`
- `買前長片研究`
- `攻略長片研究`
- `候選章節池`
- `使用者鎖定章節`
- `Longform Research Report`
- `Shorts Research`
- `Shorts 主題搜尋`
- `Shorts Topic Pack`
- `Shorts Research Pack`
- `候選題型`
- `使用者鎖定 Shorts 題型`
- `hook / punch`
- `Reference Shorts Evidence`
- `Production Research Notes`
- `Source Capture Status`
- `Original Text / Transcript Index`
- `query-log-reviewed.md`
- `source-originals/`
- `transcripts/`
- `PACKAGE-MANIFEST.md`

Do not rename these concepts casually. If a new term is needed, add it to `docs/project-map.md` or a future `CONTEXT.md`.

## Out Of Current Scope

The following concepts are not current default routes:

- Shorts complete script writing.
- Final longform script writing.
- Maymei voice finalizer.
- Monthly game recommendation submission.

Only use these if the user explicitly asks to leave the research scope.

## ADRs

No `docs/adr/` directory exists yet.

If a future task makes a durable process decision, create an ADR under `docs/adr/` instead of burying it in a one-off chat memory.
