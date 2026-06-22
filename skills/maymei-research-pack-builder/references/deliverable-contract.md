# Deliverable Contract

## Run Folder

Create:

```text
workspace/memory/runs/<timestamp>-<mode>-<slug>/
  query-log-reviewed.md
  sources.md
  claim-map.md
  sources-candidates-opencli.md
  source-capture-status.md
  source-originals/
  transcripts/
  tool-readiness/
  PACKAGE-MANIFEST.md
```

`sources.md` must list only validated sources or clearly mark downgraded sources. `claim-map.md` maps neutral claim IDs to source artifacts. Keep raw candidate lists separate.

## Formal Evidence Pack

Longform evidence packs go in `workspace/deliverables/longform-research/` and must follow `templates/deliverables/longform-research-report.md` when that template is required. Interpret subjective template sections as evidence inventory sections, not writing recommendations.

Shorts topic packs go in `workspace/deliverables/shorts-topic/`.

Shorts research packs go in `workspace/deliverables/shorts-research/`.

The default deliverable is objective. It may include evidence groups, candidate structures, and gap reports. It must not include final titles, final script outlines, writing prompts, or recommended conclusions unless the user explicitly asks for a separate writing brief.

## Package Manifest

Manifest must state:

- Evidence pack path.
- Query log path.
- Source index path.
- Claim map path.
- Tool-readiness path.
- Included originals/transcripts/comments/OCR.
- Link-only or downgraded sources.
- Uncaptured sources and why.
- Known limits and needed in-game verification.

## Zip Package

Zip the formal evidence pack plus run folder evidence. Do not deliver only a narrative markdown conclusion.

## Checks

Run the matching shape check:

```powershell
python scripts/check_deliverable_shape.py <report.md> --mode longform-research
python scripts/check_deliverable_shape.py <pack.md> --mode shorts-topic
python scripts/check_deliverable_shape.py <pack.md> --mode shorts-research
```

Always run:

```powershell
python scripts/check_docs_consistency.py
```

If there is a run folder:

```powershell
python scripts/check_memory_completeness.py <run-dir>
```

Finally confirm the zip exists and has entries.
