# Evidence Quality Contract

## Objective Evidence Boundary

Evidence work is separate from writing work. Research files should preserve what was captured, what can be verified, and what remains unknown. They should not decide the final angle, voice, recommendation, title, or conclusion for the writing project.

If interpretation is unavoidable, label it `interpretation` and put it in a separate writing brief. Do not mix it into `sources.md`, `claim-map.md`, evidence cards, or source indexes.

## Validated Evidence Definition

A source counts as validated only when at least one saved artifact contains claim-bearing text:

- `opencli web read` or equivalent readable body.
- YouTube / bilibili subtitle, transcript, or local transcription.
- Saved YouTube / Bilibili / Reddit / Steam / forum / Shorts comments.
- Official body text for dates, platforms, versions, price, features, and names.
- OCR or manual extraction from user-provided files.

## Candidate vs Validated Counts

- Candidate count: search results, channel/video hits, site hits, social posts, or metadata.
- Validated count: sources with saved claim-bearing text.
- For major topics, aim for at least 20 candidates in Chinese, English, and Japanese. Do not claim 20 validated sources unless they were actually captured.
- If validated counts are thin, deliver a gap report with next queries and blocked platforms.

## Minimum Practical Coverage

For a normal longform research pack, try to reach:

- 3+ creator/video sources with transcript, subtitle, or useful comments.
- 2+ community/forum sources with readable body.
- 2+ guide/news/official body sources.
- Chinese, English, and Japanese represented when the game has those markets.

For an攻略 pack, every claim about efficiency, route, farming, settings, builds, or exploits needs a source tier:

- `video-tested`
- `comment-reported`
- `guide-site`
- `official`
- `unverified-local`

Do not guarantee an efficiency number without local verification.

## Source Inclusion Rules

Include a source in the claim map only if:

1. It supports, conflicts with, or limits a concrete neutral claim.
2. The evidence artifact can be reopened locally.
3. Its language, version, and source type are recorded.
4. Risks or conflicts are marked.

Downgrade sources when:

- Transcript/subtitle failed and comments are absent or generic.
- The source is only metadata.
- The advice is version-sensitive and not cross-validated.
- The page is official but the claim is about player sentiment or strategy.

## Neutral Claim Rules

Write claims as verifiable statements:

- Good: `C-014: The official Steam page lists PC as a supported platform.`
- Good: `C-027: Three captured YouTube comments report confusion about the crafting menu.`
- Good: `C-041: The transcript shows the creator tested the early farming route for 20 minutes.`
- Bad: `This is the strongest hook.`
- Bad: `Players will definitely care about this.`
- Bad: `This should be the first chapter.`

Every claim should have:

- `claim_id`
- `claim_text`
- `source_paths`
- `source_tier`
- `status`: `supported`, `conflicted`, `limited`, `needs-verification`
- `limits`

## Prohibited Evidence-Layer Language

Avoid these in evidence files unless quoting a source verbatim:

- `worth doing`
- `best angle`
- `must mention`
- `core selling point`
- `final conclusion`
- `recommended chapter`
- `Claude Code prompt`
- `writer handoff`
