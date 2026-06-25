# Project Evolution Memory

Updated: 2026-05-28

Purpose: 讓不同遊戲、不同對話串的研究經驗可以沉澱回 `X:\writing-agent`，避免每次重新摸索工具和研究深度。

## 2026-05-28 Research Capability Pass

Scope: 掃描近期 `workspace/memory/runs/`、`workspace/deliverables/`、`workspace/memory/games/`、`workspace/memory/style-corpus/`，沉澱可重用的資料抓取、影片字幕、站外正文與研究包方法。

### Files Updated

- `workspace/memory/style-corpus/research-quality-rules.md`
- `workspace/memory/project-evolution.md`

### Reusable Methods Added

- 研究前置工具檢查要有實際 run-dir 證據：`opencli_tooling.py ensure --update --run-dir <run-dir>`，通過後才進主研究；Browser Bridge 斷線要先修。
- YouTube 高訊號影片要優先抓 transcript；`opencli` 失敗時用 `yt-dlp` 字幕 fallback。仍失敗才降權使用 metadata / 留言 / 其他正文交叉佐證。
- B 站常見 `AUTH_REQUIRED`，要把字幕失敗寫清楚；可用 B 站影片資訊、留言、音訊下載、本地 Whisper 轉錄補強，但轉錄錯字和數字不能當硬事實。
- Google / site search 只是入口；主結論必須來自已讀正文、影片字幕、留言內容或攻略頁內容。
- 研究包要保留給後續寫稿使用的高密度資料：已確認事實、玩家痛點、逐項研究卡、可講判斷、禁講點、口播句、B-roll、來源對照表、Query Log。

### Evidence Used

- `workspace/memory/runs/20260524-110709-007-first-light-buy-before-research/query-log-reviewed.md`
- `workspace/deliverables/research/2026-05-24-007-first-light-buy-before-research.md`
- `workspace/memory/games/007-first-light/buy-before-research-2026-05-24.md`
- `workspace/memory/runs/20260522-195540-topic-forza-horizon-6-next-guide/`
- `workspace/deliverables/topic/2026-05-22-forza-horizon-6-next-guide-topic-brief.md`
- `workspace/memory/runs/20260527-161955-007-youtube-mEsA9jAWcpQ-review/`

### Failed Or Lower-Weight Methods To Avoid

- 不要把 `opencli youtube search` 結果本身當影片研究。沒有字幕、逐字稿、描述、留言或音訊轉錄，就只是候選線索。
- 不要把 B 站 search / video metadata 直接當影片內容。字幕或 AI summary 需要登入時，必須標示限制。
- 不要把 Reddit / Steam 搜尋結果中的無關高分貼當社群訊號。一定要讀具體討論串正文。
- 不要把搜尋摘要、新聞標題或官方行銷詞改寫成玩家真正在意的賣點。

### Next Checks For Future Runs

- 新研究完成後，檢查是否有 `query-log-reviewed.md` 或同等整理；沒有就補。
- 檢查高訊號影片是否有 `transcripts/`、字幕 fallback 或明確降權原因。
- 檢查研究包是否能支援寫稿：如果只有結論和少量 bullet，要補來源內容、玩家問題、口播句與來源對照。
- 若新增了成功的資料抓取方式，回寫到 `workspace/memory/style-corpus/research-quality-rules.md`，不要只留在單次 run 目錄。

## 2026-05-29 Research Capability Maintenance Pass

Scope: 依 `AGENTS.md -> docs/project-map.md -> docs/agents/skill-routing.md -> 研究 workflow` 重新掃描近期研究 run 與 deliverables，確認哪些方法真的被近期 007 / Elliot / FH6 任務驗證，哪些只是留在原始 run 裡沒有沉澱。

### Files Updated

- `workspace/memory/style-corpus/research-quality-rules.md`
- `workspace/memory/project-evolution.md`

### Reusable Methods Added

- 三語圈關鍵字要從玩家判斷詞起手，不是只翻譯遊戲名。近期穩定有效的詞簇包括：
  - 中文：`買前 / 值不值得 / 試玩 / 難度 / 前期 / 優化`
  - 日文：`買うべきか / 体験版 感想 / 難易度 / 序盤 / 金策`
  - 英文：`before you buy / demo impressions / difficulty / performance`
- run 內保留 `opencli` 原始 YAML / JSON 很有用，但一定要補 reviewed log；否則像 Elliot 這種 run 雖然原始證據厚，後續仍難快速辨認「哪些命中被採用、哪些只是候選」。
- 登入後補查與使用者 Demo 補證，必須在同輪同步回寫 game memory 或研究包，不然只留 `web read` 回條與原始檔，後續代理很難直接復用。
- `web read` 保存回條不是正文摘要。真正可回用的知識，必須再整理成玩家疑慮、可講判斷、禁講點、待實機確認，並寫回研究包 / game memory。

### Evidence Used

- `workspace/memory/runs/20260524-110709-007-first-light-buy-before-research/query-log-reviewed.md`
- `workspace/deliverables/research/2026-05-24-007-first-light-buy-before-research.md`
- `workspace/memory/games/007-first-light/buy-before-research-2026-05-24.md`
- `workspace/deliverables/research/20260528-elliot-buy-before-pre-research.md`
- `workspace/memory/games/elliot-millennium-tales/20260528-buy-before-baseline.md`
- `workspace/memory/runs/2026-05-28-172207-opencli-tooling/tool-readiness.md`

### Failed Or Lower-Weight Methods To Avoid

- 不要把只有 `opencli/*.yaml` 的 run 當成已沉澱完成。沒有 `query-log-reviewed.md` / `sources.md` 時，知識可復用性仍不足。
- 不要把 `opencli web read` 的保存回條當成已深讀正文。若沒把內容再整理進研究包或 game memory，下一輪等於還要重讀一次。
- 不要把登入後補查當成附錄。近期 Elliot run 已證明 Steam / 巴哈補查會直接改變章節優先順序與風險比重。

### Next Checks For Future Runs

- 如果 run 有 `login-supplement/` 或 `user-demo-supplement/`，檢查是否已同步整理進研究包與 game memory；沒有就補。
- 如果只看到 `web read` 回條而看不到正文摘要，補一份最少可用的結論卡，說清楚這頁實際支撐哪個章節或風險。
- 如果研究包會交給後續寫稿代理，先確認它能回推到具體 query、正文、字幕與留言，而不是只剩結論段落。

## 2026-05-30 Research Capability Maintenance Pass

Scope: Re-read the repo routing docs, then scan recent 007, Elliot, and opencli tooling runs to capture only evidence-backed reusable research methods.

### Files Updated

- `workspace/memory/style-corpus/research-quality-rules.md`
- `workspace/memory/project-evolution.md`
- `C:\codex-home\automations\maymei-research-method-evolution\memory.md`

### Reusable Methods Added

- Native query families by language are now explicitly preserved as the default start for buy-before and demo research.
- The durable research chain is now stricter: `tool-readiness` -> reviewed query log / sources -> game memory or research pack. Raw `opencli` artifacts alone do not count as reusable memory.
- Bilibili `AUTH_REQUIRED` is now treated as a weight downgrade, not a reason to pretend there is no source. Use metadata, comments, and outside transcript generation if available, then mark the remaining uncertainty.
- Demo supplements and login supplements are now first-class research inputs. When they change chapter framing, they must be promoted into game memory in the same pass.
- Dense research packages should preserve transcript status, source weight, player-facing phrasing, risk notes, and B-roll cues so later Maymei script writing is not forced to reconstruct them.

### Evidence Used

- `workspace/memory/runs/20260529-145942-007-topic-research/`
- `workspace/deliverables/topic-research/2026-05-29-007-high-traffic-topic-brief.md`
- `workspace/memory/games/007-first-light/topic-research-signal-2026-05-29.md`
- `workspace/deliverables/research/20260528-elliot-buy-before-pre-research.md`
- `workspace/memory/games/elliot-millennium-tales/20260528-buy-before-baseline.md`
- `workspace/memory/games/elliot-millennium-tales/20260529-content-series-plan.md`
- `workspace/memory/runs/2026-05-28-172207-opencli-tooling/tool-readiness.md`

### Failed Or Lower-Weight Methods To Avoid

- Treating `opencli/*.yaml` as a finished memory layer.
- Leaving `web read` saves unpromoted after they already shaped the judgement.
- Treating bilibili title / metadata / AI summary alone as enough for a main conclusion.
- Letting demo or login supplements sit outside game memory after they change framing.

### Gap Report / Next Checks

- `workspace/memory/runs/20260528-172755-elliot-buy-before-research/` still needs `query-log-reviewed.md` and `sources.md`.
- The next Elliot-focused pass should consolidate the existing raw evidence before expanding the source set.
- Keep using the 007 topic run as the better current template for reviewed logs plus transcript status tracking.

## 2026-06-15 Research Capability Maintenance Pass

Scope: Re-read the repo routing docs, then scan recent Dave longform runs, Ocarina Shorts runs, the Dave community-title follow-up run, and the newest opencli tooling run for reusable research-method updates only.

### Files Updated

- `workspace/memory/style-corpus/research-quality-rules.md`
- `workspace/memory/project-evolution.md`
- `C:\codex-home\automations\maymei-research-method-evolution\memory.md`

### Reusable Methods Added

- Community-only follow-up notes are now confirmed as a useful second-pass research shape when the question is title pressure, buyer-fit wording, or comment-side tension rather than new gameplay facts.
- Later writing packs may reuse prior transcripts, Reddit captures, and other already-readable evidence, but the reused files should be copied into a clearly labeled `previous-run-reuse` area and traced back to the original run.
- Mixed transcript capture is now a preserved method: if the newest official YouTube video yields English YAML on direct `opencli youtube transcript` but only a fallback-language markdown via the helper, keep both and record which one is the primary factual source.
- Tool-readiness summary flags are now treated as potentially unreliable when they conflict with the embedded command logs. Manual interpretation of the actual `opencli doctor` output is required before deciding the tool state.
- Historical or official sources that stay image-only or Cloudflare-blocked after a reasonable attempt should be logged as failed/low-weight and replaced by readable official pages, creator transcripts, and community comment bodies.
- Dense writer-facing packs should preserve concrete next-query targets with dates or trigger points so later script work can resume from a precise follow-up list.

### Evidence Used

- `workspace/memory/runs/20260611-191449-longform-research-dave-the-diver-in-the-jungle-buy-before/creator-video-evidence.md`
- `workspace/memory/runs/20260611-191449-longform-research-dave-the-diver-in-the-jungle-buy-before/sources.md`
- `workspace/memory/runs/20260611-111000-shorts-research-ocarina-final-three-details/query-log-reviewed.md`
- `workspace/memory/runs/20260611-111000-shorts-research-ocarina-final-three-details/sources.md`
- `workspace/memory/runs/20260612-111047-title-research-dave-jungle-community-hooks/community-title-signal.md`
- `workspace/memory/runs/2026-06-12-111246-opencli-tooling/tool-readiness.md`
- `workspace/deliverables/longform-research/20260612-dave-the-diver-in-the-jungle-final-buy-before-writing-pack.md`

### Failed Or Lower-Weight Methods To Avoid

- Treating forum正文 capture failure as total forum failure when readable comment bodies from the same market still exist.
- Reusing old transcripts/comments without labeling the reuse path and original provenance.
- Trusting only the top-level `doctor_ok` / `transcript_ok` summary flags when the raw doctor blocks show a different state.
- Spending too long retrying image-only PDFs or Cloudflare-blocked text dumps after readable alternatives already support the claim better.

### Next Checks For Future Runs

- Verify whether `scripts/opencli_tooling.py ensure` is misreporting `doctor_ok` / `transcript_ok` in some runs despite successful `opencli doctor` output.
- When a new writing pack reuses old evidence, keep the reuse pattern consistent so later memory passes can distinguish fresh capture from carried-forward proof.
- If another community-title follow-up run works well, consider formalizing that small-note pattern as a repeatable template instead of leaving it implicit.

## 2026-06-16 Research Capability Maintenance Pass

Scope: Re-read the repo routing docs, then scan the newest Gagabird topic-selection and daily-must-do runs, the Palworld 1.0 returner package, the latest opencli tooling run, and nearby durable game memory for reusable method updates only.

### Files Updated

- `workspace/memory/style-corpus/research-quality-rules.md`
- `workspace/memory/project-evolution.md`
- `C:\codex-home\automations\maymei-research-method-evolution\memory.md`

### Reusable Methods Added

- Search-intent pollution is now a preserved topic-selection check. When a candidate query cluster drifts into payment tutorials,代儲站, transaction pages, or other commercial intent while the alternative cluster yields dense攻略/新手/資源正文, treat that as evidence against the polluted topic for natural traffic framing.
- Cross-run evidence reuse inside the same game/topic is valid when the later run explicitly points to the earlier artifact path or copies the earlier source into the new package. Recent Gagabird daily research confirmed that reused transcripts and prior successful web reads remain durable only when the new run labels the dependency instead of silently inheriting it.
- A transcript file that exists but is unreadable, mojibake, or only exposes the wrong auto-caption language should be downgraded the same way as a missing transcript. Keep the file for auditability, but do not treat it as readable creator evidence.
- Weak/noisy adjacent queries can still be useful as exclusion evidence. If direct guild/arena/daily-dungeon searches surface mostly unrelated games or only site shells, use that to justify excluding those chapters from the main list instead of padding the pack with unsupported claims.
- Comment evidence that only appeared in chat and was not persisted to a raw file is reusable only as low-weight note-taking, not as durable package evidence. If a later pack may need those comments, save them to the run folder before relying on them.

### Evidence Used

- `workspace/memory/runs/20260615-205435-longform-research-gagabird-topic-selection/query-log-reviewed.md`
- `workspace/memory/runs/20260615-205435-longform-research-gagabird-topic-selection/sources.md`
- `workspace/memory/runs/20260615-214500-longform-research-gagabird-daily-must-do/query-log-reviewed.md`
- `workspace/memory/runs/20260615-214500-longform-research-gagabird-daily-must-do/sources.md`
- `workspace/memory/runs/20260615-150919-longform-research-palworld-1-0-returner-content/query-log-reviewed.md`
- `workspace/memory/runs/20260615-150919-longform-research-palworld-1-0-returner-content/sources.md`
- `workspace/memory/runs/20260615-150919-longform-research-palworld-1-0-returner-content/creator-video-evidence.md`
- `workspace/memory/runs/2026-06-15-220304-opencli-tooling/tool-readiness.md`
- `workspace/deliverables/longform-research/20260615-gagabird-topic-selection-data-brief.md`
- `workspace/memory/games/palworld/20260609-longform-traffic-topic.md`

### Failed Or Lower-Weight Methods To Avoid

- Treating commercial-intent query pollution as if it still proves organic viewer demand for a longform topic.
- Assuming a transcript artifact is usable just because a file was created; unreadable mojibake and wrong-language auto-captions still require downgrade.
- Filling a locked chapter list with weakly related system names when direct evidence stayed noisy or shallow.
- Leaving comment capture only in transient chat output when the conclusion may need to be audited later.

### Next Checks For Future Runs

- If a run uses YouTube comments in the conclusion, persist the raw comment output into the run folder instead of leaving it only in chat history.
- If `yt-dlp -U` fails but the installed version still works, keep separating updater/network failure from actual transcript-capture failure.
- When a sponsor or exception-topic task compares two framing options, keep logging search-intent pollution explicitly so later maintenance can tell traffic mismatch from weak evidence.

## 2026-06-17 Research Capability Maintenance Pass

Scope: Re-read the repo routing docs, then scan the post-previous-pass Elliot prelaunch chapter-pool run, the Elliot six-chapter deep-dive run, their paired longform deliverables, and nearby Elliot durable memory for reusable method updates only.

### Files Updated

- `workspace/memory/style-corpus/research-quality-rules.md`
- `workspace/memory/project-evolution.md`
- `C:\codex-home\automations\maymei-research-method-evolution\memory.md`

### Reusable Methods Added

- A hybrid capture chain is now a durable method when `opencli` discovery works but later Browser Bridge-backed adapters become unstable.
  - Keep the successful `opencli` query log and raw result file.
  - Pivot正文 capture to browser/web tooling plus locally saved HTML.
  - Record the pivot in `sources.md` instead of pretending the whole source family failed.
- Prelaunch guide research now has a clearer three-layer weighting model:
  - JP guide sites define the system and chapter candidate map.
  - TW/zh-TW official pages, Bahamut, and Taiwan media translate that map into local audience wording and actual friction points.
  - Creator transcripts show what experienced players repeatedly teach or warn about.
  - The pass should preserve these as separate evidence jobs rather than collapsing them into one blended confidence score.
- Transcript failure handling is now more specific.
  - `No subtitles available` is a current low-weight source state.
  - `HTTP 429` is a retry-later capture failure, not a relevance judgment.
  - `BROWSER_CONNECT` after search means preserve the hit and switch capture path instead of erasing the source trail.
- Candidate-only prewriting packs should now include an explicit writer-freedom boundary when the user supplied material buckets but did not lock final chapter order.
  - This keeps later writing turns from mistaking the research grouping for a fixed sequence.
- Player-reported farming numbers and cost caps remain usable only when the package labels them as player-report evidence and pairs them with a matching in-game verification checklist.

### Evidence Used

- `workspace/memory/runs/20260616-162057-longform-research-elliot-prelaunch-chapter-pool/query-log-reviewed.md`
- `workspace/memory/runs/20260616-162057-longform-research-elliot-prelaunch-chapter-pool/sources.md`
- `workspace/memory/runs/20260616-162057-longform-research-elliot-prelaunch-chapter-pool/tool-readiness.md`
- `workspace/memory/runs/20260616-163434-longform-research-elliot-six-chapter-deep-dive/query-log-reviewed.md`
- `workspace/memory/runs/20260616-163434-longform-research-elliot-six-chapter-deep-dive/sources.md`
- `workspace/memory/runs/20260616-163434-longform-research-elliot-six-chapter-deep-dive/creator-video-evidence.md`
- `workspace/memory/runs/20260616-163434-longform-research-elliot-six-chapter-deep-dive/tool-readiness.md`
- `workspace/deliverables/longform-research/20260616-elliot-prelaunch-japanese-guide-chapter-pool-research-pack.md`
- `workspace/deliverables/longform-research/20260616-elliot-six-chapter-deep-prewriting-research-pack.md`

### Failed Or Lower-Weight Methods To Avoid

- Treating a post-search Browser Bridge drop as if discovery also failed.
- Letting dense JP guide-site coverage override TW audience-fit evidence and creator-explanation evidence as if they answer the same question.
- Flattening `no subtitles`, `HTTP 429`, and `BROWSER_CONNECT` into one generic transcript failure label.
- Presenting candidate/prewriting chapter buckets as if they were already the user's approved final order.

### Gap Report / Next Checks

- `workspace/memory/games/elliot-millennium-tales/` still has no 2026-06-16 durable game-memory promotion, even though the new prelaunch packs contain reusable chapter-framing and verification debt.
- After official launch evidence arrives, promote the stable parts of these two Elliot packs into game memory so later buy-before / beginner turns do not have to reopen the entire run.
- If the Browser Bridge keeps disconnecting after `opencli` discovery but before page/video capture, consider a future tooling fix that records the run as `search usable, capture degraded` instead of `doctor_ok=False` / `transcript_ok=False` only.

## 2026-06-18 Research Capability Maintenance Pass

Scope: Re-read the repo routing docs, then scan the newest Palworld beginner-guide run, the 嘎嘎奇兵 locked-daily run, the crawler-method tool evaluation run, the latest opencli-tooling recovery log, nearby longform deliverables, and current game/style memory for reusable method updates only.

### Files Updated

- `workspace/memory/style-corpus/research-quality-rules.md`
- `workspace/memory/project-evolution.md`
- `C:\codex-home\automations\maymei-research-method-evolution\memory.md`

### Reusable Methods Added

- Tool readiness is now preserved as a chronological state judgment, not a single pass/fail bit.
  - The wrapper header may stay `doctor_ok=False` / `transcript_ok=False` even after later doctor blocks show the Browser Bridge reconnected.
  - Later runs should explicitly note `wrapper false negative after recovery` when the command logs prove searches or page reads were usable.
- The current stable Browser Bridge recovery path remains `opencli.cmd daemon restart` plus relaunching the saved OpenCLI Browser Bridge Edge profile, then re-checking `opencli.cmd doctor` until extension/connectivity are both connected.
- The local crawler/tool-eval run now confirms two helpers as durable first choices for future research maintenance:
  - `youtube-transcript-api` for a fast transcript first pass
  - `yt-comment-dl` for popular-comment capture with votes/replies/author/time fields
  - These do not replace the repo helper or `yt-dlp`; they strengthen the fallback ladder.
- Reddit discovery and Reddit evidence are now more clearly separated.
  - Native `opencli reddit search` can be polluted even when `reddit read` works well.
  - When that happens, use Google `site:reddit.com` discovery and only promote saved thread正文 / replies into evidence coverage.
- Bilibili subtitle failures now have a more precise downgrade rule.
  - `AUTH_REQUIRED` and `EMPTY_RESULT` both allow metadata/comment use.
  - Neither one allows the spoken guide content to be cited as if it were captured.
  - This keeps bilibili valuable for demand and version-warning signals without pretending transcript depth exists.
- Three-language coverage now has a stronger documentation requirement.
  - Recent Palworld research achieved real zh/en/ja evidence depth, but the run still lacked `language-source-matrix.md`.
  - Future runs claiming A/B/C language coverage should keep the matrix file so candidate counts, usable-source counts, primary-evidence counts, and failed captures are audit-ready.
- Exception-topic research has a clarified boundary.
  - A locked practical guide can still be valid when official/store and guide-site evidence are strong but community or cross-market depth is thin.
  - The package must state that thinness explicitly instead of implying full multilingual player validation.
- URL escaping remains part of evidence quality on Windows.
  - Bahamut, Google Play, Steam, and similar URLs with `&` or other query params can silently drift to the wrong page through the wrapper.
  - Verifying returned title/original URL after `web read` is now part of the durable method, not optional caution.

### Evidence Used

- `workspace/memory/runs/20260617-longform-research-palworld-beginner-guide/query-log-reviewed.md`
- `workspace/memory/runs/20260617-longform-research-palworld-beginner-guide/sources.md`
- `workspace/memory/runs/20260617-longform-research-palworld-beginner-guide/source-capture-status.md`
- `workspace/memory/runs/20260617-191351-longform-research-gaga-qibing-daily-five/query-log-reviewed.md`
- `workspace/memory/runs/20260617-191351-longform-research-gaga-qibing-daily-five/sources.md`
- `workspace/memory/runs/20260617-crawler-method-tool-eval/TOOL-EVALUATION.md`
- `workspace/memory/runs/2026-06-18-010833-opencli-tooling/tool-readiness.md`
- `workspace/deliverables/longform-research/20260617-palworld-beginner-guide-research.md`
- `workspace/deliverables/longform-research/20260617-gaga-qibing-daily-five-longform-research.md`
- `workspace/memory/games/palworld/20260609-longform-traffic-topic.md`

### Failed Or Lower-Weight Methods To Avoid

- Trusting the top-level `tool-readiness.md` header or final note while ignoring later doctor/smoke-test blocks that show the actual recovered state.
- Claiming creator-spoken bilibili evidence when only metadata/comments survived subtitle failure.
- Claiming full three-language validation without a durable matrix or equivalent count breakdown.
- Leaving proven side-tool evaluations buried in one-off run folders without promoting the method into shared memory.

### Gap Report / Next Checks

- `workspace/memory/runs/20260617-longform-research-palworld-beginner-guide/` still lacks `language-source-matrix.md` even though the run documents multilingual evidence depth. A future cleanup pass should add that file or relax any implied A/B/C coverage wording.
- The newest opencli-tooling log still ends with a stale `Browser Bridge is still unavailable` note despite later command blocks showing the extension connected. The readiness script/log formatting should eventually be fixed so recovered runs are not mislabeled.
- `skills/maymei-research-pack-builder/SKILL.md` points to `references/evidence-quality-contract.md`, `references/platform-capture-playbook.md`, and `references/deliverable-contract.md`, but those files are not present in the current workspace. Treat that as routing-doc drift to fix in a later repo-maintenance pass rather than assuming the references exist.

## 2026-06-19 Research Capability Maintenance Pass

Scope: Re-read the repo routing docs, then scan the Elliot postlaunch beginner-guide run, its paired longform deliverable, nearby Elliot durable game memory, and the latest opencli-tooling / crawler-eval evidence for reusable method updates only.

### Files Updated

- `workspace/memory/style-corpus/research-quality-rules.md`
- `workspace/memory/project-evolution.md`
- `C:\codex-home\automations\maymei-research-method-evolution\memory.md`

### Reusable Methods Added

- Today-only follow-up research is now a durable method for release-day and update-day topics.
  - Lock an explicit local cutoff first, for example `2026-06-18 00:00 +08:00`.
  - Keep a dedicated sweep note that records included sources, downgraded sources, and excluded-but-strong sources whose local publish time missed the cutoff.
  - This prevents relative `today` / `latest` labels from quietly drifting across time zones.
- `opencli web read` failure with `BROWSER_CONNECT 69` is now a structured fallback path, not an automatic source-family loss.
  - Preserve the discovered source in the reviewed log.
  - Save raw HTML with a browser-like fetch path.
  - Promote it into evidence only after readable body text is extracted or summarized back into the run.
- Release-day multilingual coverage now has a sharper split between usable evidence and audience-signal-only hits.
  - The newest Elliot run preserved strong Japanese same-day guide text, one Chinese same-day forum body, and mixed Chinese no-subtitle video hits that stayed candidate-only.
  - Future runs should copy that separation instead of flattening all same-day hits into equal evidence.
- Game memory promotion is now confirmed as part of the maintenance target, not just deliverable cleanup.
  - The Elliot `20260603-beginner-guide-material-pool.md` file was updated with the locked 7-chapter order, new official-release corrections, and today-only source-layer notes.
  - When a run changes durable beginner-guide wording, the shared game-memory layer should reflect it the same day.
- Windows command-shape failures should be logged as evidence-method issues rather than hidden under generic source shortage.
  - This run showed quoted English Reddit / Steam queries splitting inside PowerShell + `.cmd`.
  - The correct response is to preserve the failure reason, switch discovery path, and avoid pretending the English community had no readable sources.
- Encoding is now part of transcript reliability on this machine.
  - When transcript or helper output hits `UnicodeEncodeError` under `CP950`, rerun with UTF-8 environment settings before downgrading the source itself.

### Evidence Used

- `workspace/memory/runs/20260618-142710-longform-research-elliot-postlaunch-beginner-guide/query-log-reviewed.md`
- `workspace/memory/runs/20260618-142710-longform-research-elliot-postlaunch-beginner-guide/sources.md`
- `workspace/memory/runs/20260618-142710-longform-research-elliot-postlaunch-beginner-guide/source-capture-status.md`
- `workspace/memory/runs/20260618-142710-longform-research-elliot-postlaunch-beginner-guide/language-source-matrix.md`
- `workspace/memory/runs/20260618-142710-longform-research-elliot-postlaunch-beginner-guide/today-0618-after-midnight-source-sweep.md`
- `workspace/deliverables/longform-research/20260618-elliot-postlaunch-beginner-guide-research.md`
- `workspace/memory/games/elliot-millennium-tales/20260603-beginner-guide-material-pool.md`
- `workspace/memory/runs/2026-06-18-010833-opencli-tooling/tool-readiness.md`
- `workspace/memory/runs/20260617-crawler-method-tool-eval/TOOL-EVALUATION.md`

### Failed Or Lower-Weight Methods To Avoid

- Treating platform-relative `today` signals as sufficient proof of a Taiwan-time cutoff.
- Treating saved raw HTML as fully reusable evidence before readable body extraction exists.
- Promoting no-subtitle same-day creator videos into main攻略 conclusions just because they are fresh.
- Leaving user-corrected system wording stranded in the deliverable without updating the durable game-memory layer.
- Hiding PowerShell / `.cmd` query-splitting problems under vague `source not found` wording.
- Downgrading a transcript source too early when the actual failure was local encoding, not missing subtitles.

### Next Checks For Future Runs

- If another release-day or patch-day task asks for `今天` / `凌晨後` evidence, reuse the dedicated today-sweep pattern with explicit timezone math and exclusion notes.
- If raw HTML fallback is used again, verify that each promoted page also has extracted readable text or a research-card summary before calling it dense evidence.
- If quoted English community queries keep splitting through `opencli.cmd`, consider a later tooling/command-wrapper fix so the failure stops recurring at the method layer.
## 2026-06-20 Research Capability Maintenance Pass

Scope: Re-read the repo routing docs, then scan the newest Elliot 10-chapter prewriting pack, the Elliot Day 2 refresh run, the Dave the Diver Jungle DLC guide-seed run, nearby Elliot game memory, and the latest deliverable layer for reusable method updates only.

### Files Updated

- `workspace/memory/style-corpus/research-quality-rules.md`
- `workspace/memory/project-evolution.md`
- `C:\codex-home\automations\maymei-research-method-evolution\memory.md`

### Reusable Methods Added

- Retained-source layering is now a confirmed dense-pack pattern.
  - When a user says earlier research must stay intact, the new pack should name the older pack as a `retained source layer` in `sources.md` instead of silently absorbing it.
  - The new run then adds only the delta layer: fresh web bodies, comments, transcripts, or locked-chapter deepening.
  - `PACKAGE-MANIFEST.md` should say whether prior run folders were bundled whole or selectively copied.
- Readiness wrapper failure is now confirmed to have an extension-update false-negative variant.
  - Recent Elliot refresh evidence showed `opencli_tooling.py ensure` returning non-zero because the browser extension wanted an update, while direct `opencli.cmd` search / web-read smoke tests still worked.
  - Future runs should record that as tool-wrapper failure but usable direct commands, not as whole-toolchain death.
- Once a baseline beginner pack exists, refresh search should become chapter-specific rather than fully broad again.
  - Recent Elliot 10-chapter work got more value by targeting `glass vial`, `cats`, `missables`, `magicite rank 5`, `Trial Sanctuary`, `spear build`, and similar nouns than by rebuilding the whole beginner-search surface from zero.
- Candidate-only discovery now has a clearer storage boundary.
  - The Elliot 10-chapter pack separated validated evidence in `sources.md` from search-only leads in `sources-candidates-opencli.md`.
  - This is the better default for thick packs because it preserves discovery breadth without weakening the accepted evidence table.
- Bilibili metadata/comment capture has two distinct reusable roles when subtitle capture fails.
  - User-provided or older competitor videos can still be saved as `format signal only`.
  - Current guide-video metadata/comments can still be promoted as `player problem pool` evidence when they expose mission-order confusion, boss friction, missing item questions, or patch-risk chatter.
  - Neither role substitutes for creator-spoken evidence unless readable subtitle/audio text exists.
- Day-after refreshes do not need to rebuild every language layer from zero.
  - The Elliot Day 2 run added fresh English / Chinese bodies while explicitly keeping the 6/18 Japanese layer primary.
  - That is now a durable refresh pattern for postlaunch or patch-day follow-up.
- Dense writer-facing packs are more understandable when they preserve source-layer hierarchy explicitly.
  - `retained source layer`
  - `refresh layer`
  - `new direct captures`
  - This makes later script-writing and future maintenance passes understand what is inherited versus newly captured.

### Evidence Used

- `workspace/memory/runs/20260619-longform-research-elliot-10chapter-prewriting-pack/query-log-reviewed.md`
- `workspace/memory/runs/20260619-longform-research-elliot-10chapter-prewriting-pack/sources.md`
- `workspace/memory/runs/20260619-longform-research-elliot-10chapter-prewriting-pack/source-capture-status.md`
- `workspace/memory/runs/20260619-elliot-postlaunch-day2-beginner-guide-refresh/query-log-reviewed.md`
- `workspace/memory/runs/20260619-elliot-postlaunch-day2-beginner-guide-refresh/sources.md`
- `workspace/memory/runs/20260619-elliot-postlaunch-day2-beginner-guide-refresh/day2-refresh-findings.md`
- `workspace/memory/runs/20260619-102753-longform-research-dave-diver-jungle-dlc-guide-seed/query-log-reviewed.md`
- `workspace/memory/runs/20260619-102753-longform-research-dave-diver-jungle-dlc-guide-seed/sources.md`
- `workspace/deliverables/longform-research/20260619-elliot-10chapter-prewriting-research-pack.md`
- `workspace/memory/games/elliot-millennium-tales/20260603-beginner-guide-material-pool.md`

### Failed Or Lower-Weight Methods To Avoid

- Treating a non-zero readiness wrapper result as proof that `opencli` was unusable when the actual issue was only an extension-update warning.
- Mixing competitor-format reference videos into the same evidence tier as readable guide bodies, transcripts, or saved comments.
- Re-running a full multilingual baseline during every refresh when the true task is chapter-gap deepening.
- Letting search-result-only leads crowd the accepted evidence table instead of separating them into a candidate-only file.
- Presenting bilibili metadata/comment captures as if the spoken guide itself was captured.

### Next Checks For Future Runs

- If another retained-layer pack is built, keep the `retained source layer` / `refresh layer` / `new direct captures` wording consistent so later maintenance can audit inheritance cleanly.
- If `opencli_tooling.py ensure` keeps failing on extension-update state while direct commands work, consider a later tooling fix so the wrapper reports a warning instead of a hard failure.
- If future dense packs keep accumulating search-only leads, consider formalizing `sources-candidates-opencli.md` as a reusable template instead of leaving it as an ad hoc filename.

## 2026-06-21 Research Capability Maintenance Pass

Scope: Re-read the repo routing docs, then scan the newest Dave the Diver Jungle seven-chapter deep dive, its nearby practical-chapter material, the Elliot retained-layer pack examples, the crawler-method evaluation, and the latest deliverable layer for reusable method updates only.

### Files Updated

- `workspace/memory/style-corpus/research-quality-rules.md`
- `workspace/memory/project-evolution.md`
- `C:\codex-home\automations\maymei-research-method-evolution\memory.md`

### Reusable Methods Added

- Late creator/community expansion is now a named evidence layer, not ad hoc spillover.
  - If the first pack is already stable and the user asks for more creator videos, comments, or community pain points, add a dedicated `source-originals/social-supplement/` and `transcripts/social-supplement/` layer instead of mixing those files into the first-pass capture set.
  - If there is a second late sweep after publication or after another hour of discussion growth, an `extra-hour-pass/` subfolder is acceptable as long as the package manifest explains why it exists.
- User-provided screenshots are now confirmed as first-class evidence for exact UI wording, quest text, and trigger-state clues.
  - Save the original image into `source-originals/`.
  - Add one source entry that says exactly what the screenshot proves and exactly what it does not prove.
  - Use it to correct or constrain weaker guide-site guesses, not to invent broader trigger rules.
- Steam / Reddit discussion bodies are strongest as pain-point and blocker evidence, not as mechanic truth tables.
  - Current-discussion sweeps are useful for buyer hesitation, patch-risk chatter, upgrade blockers, time-pressure complaints, and misunderstood systems.
  - Keep official pages and readable guide bodies as the authority for entry rules, feature scope, and system facts.
- Lower-authority guide bodies can still help dense packs when their role stays narrow and explicit.
  - Sources like smaller walkthrough hubs or lighter guide sites can support route sketches, terminology, or system-shape cross-checks.
  - They should not be the final word on day counts, customer counts, profit rankings, or universal trigger conditions when stronger sources are missing.
- Source-quality downgrade can be evidence-backed, not just silence.
  - If a transcript/comment pair shows internal quality red flags or conflicts with stronger official / guide evidence, keep the artifact and record why it was downgraded.
  - This is better than quietly deleting it, because later runs can see that the source was checked and rejected for a reason.

### Evidence Used

- `workspace/memory/runs/20260620-longform-research-dave-jungle-seven-chapter-deep-dive/source-capture-status.md`
- `workspace/memory/runs/20260620-longform-research-dave-jungle-seven-chapter-deep-dive/language-source-matrix.md`
- `workspace/memory/runs/20260620-longform-research-dave-jungle-seven-chapter-deep-dive/sources.md`
- `workspace/memory/runs/20260620-longform-research-dave-jungle-seven-chapter-deep-dive/creator-video-evidence.md`
- `workspace/memory/runs/20260620-longform-research-dave-jungle-seven-chapter-deep-dive/PACKAGE-MANIFEST.md`
- `workspace/memory/runs/20260619-longform-research-elliot-10chapter-prewriting-pack/sources.md`
- `workspace/memory/runs/20260619-elliot-postlaunch-day2-beginner-guide-refresh/day2-refresh-findings.md`
- `workspace/memory/runs/20260617-crawler-method-tool-eval/TOOL-EVALUATION.md`
- `workspace/deliverables/longform-research/20260620-dave-diver-in-the-jungle-seven-chapter-deep-dive.md`

### Failed Or Lower-Weight Methods To Avoid

- Mixing late social/community supplements into the same undifferentiated evidence tier as the first-pass captured bodies.
- Using player complaint threads as if they were official mechanic confirmation.
- Letting weaker guide hubs decide exact numbers or universal trigger rules when they only provide route hints.
- Quietly discarding low-quality creator sources without recording why they were checked and downgraded.
- Referring to a screenshot as general proof of all-playthrough behavior when it only proves one observed quest/UI state.

### Next Checks For Future Runs

- If the repo keeps using `social-supplement/` and `extra-hour-pass/`, consider templating those names in the run-memory scaffold so later packs stay consistent.
- If Bahamut direct body capture keeps failing while Google leads remain useful, add a more explicit repo rule for when Bahamut should stay lead-only versus when OCR/manual capture is worth the time.
- If more user screenshots become part of guide research, consider standardizing a short `user-evidence.md` note so image-backed facts and their limits are always explicit.

## 2026-06-22 Research Capability Maintenance Pass

Scope: Re-read the repo routing docs, then compare the 2026-06-21 automation memory against the late-completed files in the Dave the Diver Jungle seven-chapter deep-dive run, its paired deliverable, and the current shared memory layer. The goal was to promote only methods that became clear after the pack was fully completed, and to avoid duplicating methods already captured on 2026-06-21.

### Files Updated

- `workspace/memory/style-corpus/research-quality-rules.md`
- `workspace/memory/project-evolution.md`
- `C:\codex-home\automations\maymei-research-method-evolution\memory.md`

### Reusable Methods Added

- Late user-playtest corrections now have a durable evidence shape.
  - When a locked guide pack is already dense and later user playtest changes the recommended wording, add a dedicated `mechanic-correction-table.md` instead of only editing the report prose.
  - The table should reconcile `user result / question`, `external evidence`, `current ruling`, and `evidence level`.
  - This is the cleanest way to stabilize guide points such as favorite gifts vs favorite food, Auto Supply behavior, quest-marker routing, and portion-prep heuristics.
- `claim-map.md` is now confirmed as the right layer for separating source status in dense Maymei research packs.
  - Recent Dave completion work used distinct statuses for `supported`, `limited`, `conflicted`, `needs-verification`, `user-playtest`, and `downgraded`.
  - That made it possible to reuse user screenshots and low-quality creator captures without collapsing them into the same confidence tier as readable official / guide bodies.
- User screenshots are now better treated as evidence-layer inputs, not only attachments.
  - Save the image in `source-originals/`.
  - Add a source entry describing what the screenshot proves and what it does not prove.
  - Then connect that point into `claim-map.md` or `mechanic-correction-table.md` so quest text, gift-heart markers, and similar UI facts become reusable method memory.
- A named `mechanic-correction-pass/` layer is now a valid late-stage source family.
  - Use it when the job is no longer broad multilingual discovery, but reconciling conflicting guide wording, base-game carryover assumptions, and user-playtest corrections.
  - This keeps the correction sweep distinct from `social-supplement/` and avoids hiding terminology repairs inside the base evidence pile.
- `source-capture-status.md` is more useful when it explicitly separates tool state from evidence state.
  - The newest Dave run preserved wrapper failure, direct-command success, externally unconfirmed gaps, and user-playtest-only confirmations in one file.
  - That makes later reuse safer for topics like Auto Supply, one-dive time cost, New Game max gear, and underwater quest markers.

### Failed Or Lower-Weight Methods To Avoid

- Editing only the final report when late user-playtest corrections materially change system wording.
- Leaving screenshot-backed facts or user-playtest findings outside the claim/correction layer.
- Treating `sources.md` alone as enough for a pack that now includes conflicts, user evidence, and downgraded creator captures.
- Upgrading base-game mechanic text into DLC certainty without a clearly labeled DLC-specific validation source.

### Gap Report / Next Checks

- There were no newer Shorts research examples after the 2026-06-21 pass, so this maintenance update is longform-heavy.
- The most useful new evidence came from the late-completed Dave Jungle pack rather than from a brand-new run family; future passes should keep checking whether late package completion is surfacing new reusable layers.
- Bahamut direct body capture still remains mostly lead-only, and Chinese no-subtitle creator videos remain a weak evidence family rather than a solved method.

## 2026-06-23 Research Capability Maintenance Pass

Scope: Re-read the repo routing docs, then compare the current shared memory against the fully packaged Dave Jungle run and the later script deliverable to capture only the reusable packaging rules that actually improved downstream writing reuse. No new Shorts evidence family appeared in this pass.

### Files Updated

- `workspace/memory/style-corpus/research-quality-rules.md`
- `workspace/memory/project-evolution.md`
- `C:\codex-home\automations\maymei-research-method-evolution\memory.md`

### Reusable Methods Added

- `PACKAGE-MANIFEST.md` is now confirmed as a first-class research-navigation layer for dense writer-facing packs.
  - The strongest current shape is: formal report, run-file inventory, source-family summary, uncaptured/downgraded families, and a clear `Known Limits` block.
  - The run-file inventory should call out `user-playtest-notes.md`, `claim-map.md`, `mechanic-correction-table.md`, `sources-candidates-opencli.md`, and `source-capture-status.md` so later writing can route quickly to the right evidence layer.
  - This avoids forcing later script work to rediscover uncertainty and source status by reading the whole report end to end.
- Late refreshes now have a better naming rule when they serve a narrow writing need instead of broad discovery.
  - Dated plus intent-named folders such as `20260622-update`, `20260622-money-method-update`, and `20260622-weapon-recommendation-update` are easier to audit than a single catch-all supplement folder.
  - The manifest should explain why each delta layer exists and what chapter or claim family it was meant to repair.
  - This makes later writing or maintenance able to pull only the relevant delta instead of rescanning the full run.
- Writer-facing uncertainty should stay mirrored in the package layer, not only the prose layer.
  - The Dave pack-to-script path shows that `user-playtest`, `needs-verification`, `candidate-only`, and weaker-language warnings remain useful even after the research becomes a script.
  - Keeping those labels in `Known Limits` reduces the chance that later writing upgrades Auto Supply, customer counts, Hook Gun prompts, or Chinese money-route candidates into harder claims than the evidence allows.

### Failed Or Lower-Weight Methods To Avoid

- Treating `PACKAGE-MANIFEST.md` as a thin archive receipt once the run has multiple evidence-control files and late correction layers.
- Hiding narrow late refresh work inside unnamed supplement folders that do not explain whether the pass was for hotfixes, money methods, weapon advice, or another specific chapter repair.
- Leaving uncertainty labels only in chapter prose when the package is expected to support later script writing.

### Gap Report / Next Checks

- No newer Shorts research package or Shorts topic pack appeared after the 2026-06-22 pass, so this update still cannot promote a new Shorts-specific method.
- The new evidence here is mostly packaging-layer evidence from the Dave pack plus its later script reuse, not a new capture-tool breakthrough.
- If a future pass sees another research-to-script handoff, check whether the writer actually used `PACKAGE-MANIFEST.md` plus the claim/correction files directly, or still had to fall back to the full report.

## 2026-06-24 Research Capability Maintenance Pass

Scope: Re-read the repo routing docs, then compare the current shared memory against the newest `20260623-user-demo-transcript-zhuanshi-zhishou` run plus nearby durable game memory. The goal was to promote only reusable local-transcription workflow lessons instead of repeating the 2026-06-23 packaging rules.

### Files Updated

- `workspace/memory/style-corpus/research-quality-rules.md`
- `workspace/memory/project-evolution.md`
- `C:\codex-home\automations\maymei-research-method-evolution\memory.md`

### Reusable Methods Added

- User-provided long local audio can now be treated as a first-class evidence layer when Maymei research needs demo/playtest wording but no web transcript path exists.
  - The current verified shape is a dedicated run folder with `query-log-reviewed.md`, `sources.md`, `tool-readiness.md`, `PACKAGE-MANIFEST.md`, and a `transcripts/` bundle.
  - This keeps user-demo or local-recording evidence inside the same reusable memory structure as normal longform research instead of leaving it as an unattached helper file.
- Local ASR packaging now has a stronger default artifact set.
  - Keep `timestamped.md` for citation and chapter routing.
  - Keep `plain.txt` for fast reading/search.
  - Keep `raw-asr.txt` so later passes can inspect pre-normalization output instead of trusting only cleaned text.
  - Keep `segments.json` so later tooling or manual QA can re-slice exact time ranges without rerunning ASR.
- The local-ASR readiness note should preserve inference settings, not only the output text.
  - The newest run proved it is useful to record engine, model, device, compute type, thread count, language, VAD state, hotword use, and OpenCC normalization choice in `tool-readiness.md`.
  - This makes later agents able to compare quality differences instead of guessing why one local transcript was cleaner than another.
- Progress logging is now part of reusable auditability for large local transcription jobs.
  - The current run kept `transcription-progress.log` with elapsed minutes, segment counts, and audio progress across a `01:17:02` file.
  - That is a better default than a silent one-shot transcript because later maintenance can estimate runtime and spot stalled or low-yield jobs.
- Spot-QA audio slices are a useful middle layer between full raw media and final transcript text.
  - The run kept `source-originals/sample-*.wav` slices for later VAD/quality checks while leaving the original `185 MB` MP3 outside the run folder.
  - This is a good packaging pattern when the source is large: keep the original path in `sources.md` / `PACKAGE-MANIFEST.md`, keep small QA slices locally, and avoid bloating the reusable package unless the full media is truly needed.

### Evidence Used

- `workspace/memory/runs/20260623-user-demo-transcript-zhuanshi-zhishou/query-log-reviewed.md`
- `workspace/memory/runs/20260623-user-demo-transcript-zhuanshi-zhishou/sources.md`
- `workspace/memory/runs/20260623-user-demo-transcript-zhuanshi-zhishou/tool-readiness.md`
- `workspace/memory/runs/20260623-user-demo-transcript-zhuanshi-zhishou/transcription-progress.log`
- `workspace/memory/runs/20260623-user-demo-transcript-zhuanshi-zhishou/PACKAGE-MANIFEST.md`
- `workspace/memory/games/elliot-millennium-tales/20260603-beginner-guide-material-pool.md`

### Failed Or Lower-Weight Methods To Avoid

- Saving only one cleaned transcript file from a long local demo recording and discarding the raw ASR / segment structure.
- Treating local ASR as reusable evidence without recording the inference settings that shaped quality.
- Stuffing the entire large source media into every reusable run package when a source path plus QA slices is enough.
- Leaving user-demo transcription work outside the normal run-memory structure, where later longform research cannot find or reuse it.

### Gap Report / Next Checks

- This pass did not surface a new multilingual source-discovery or opencli capture breakthrough; the useful new evidence was the local-ASR packaging pattern only.
- No newer Shorts topic pack or Shorts research pack appeared after the 2026-06-23 pass, so Shorts-specific method memory still did not advance.
- If a future run promotes a local user-demo transcript into a full longform pack, check whether the transcript also lands in the game-memory layer with explicit chapter/risk links instead of remaining a standalone transcript run.

## 2026-06-25 Research Capability Maintenance Pass

Scope: Re-read the repo routing docs, then scan the new `20260625-002148-longform-research-dave-diver-jungle-traffic-evidence` run, its paired longform deliverable, and the nearby `20260625-001332-topic-decision-elliot-vs-dave` comparison run. The goal was to capture only reusable methods for compact traffic-evidence research and to log the new raw-only comparison run as a gap instead of promoting it as a good template.

### Files Updated

- `workspace/memory/style-corpus/research-quality-rules.md`
- `workspace/memory/project-evolution.md`
- `C:\codex-home\automations\maymei-research-method-evolution\memory.md`

### Reusable Methods Added

- A compact `traffic-evidence` longform pack is now a valid formal research shape when the user asks for topic-choice proof rather than a full chapter-complete guide pack.
  - The current minimum reusable layer is still formal: `query-log-reviewed.md`, `sources.md`, `claim-map.md`, `source-capture-status.md`, `decision-log.md`, `PACKAGE-MANIFEST.md`, a report, and a zip package.
  - This is the right correction when a prior verbal recommendation failed the repo's evidence rules: keep the pack smaller, but do not drop the artifact chain.
- Traffic ranking should keep `candidate-only metadata` and `validated claim-bearing evidence` explicitly separated.
  - Use raw YouTube/Bilibili search files plus a normalized helper like `candidate-metrics.csv` only for candidate ranking and query comparison.
  - Promote only selected videos/pages into `sources.md` after exact Bilibili `video` metadata, comments, transcripts, or readable web bodies are captured.
  - `claim-map.md` can then state which ranking claims depend partly on candidate metadata and which are supported by read evidence.
- Bilibili exact video metadata is a stronger traffic layer than Bilibili search score when comparing topic buckets.
  - The 2026-06-25 Dave run used `bilibili search` for discovery, then upgraded chosen hits through `opencli.cmd bilibili video` and comment capture.
  - That is the better default when the task is traffic-evidence topic ranking rather than broad source harvesting.
- `web read` exit code alone is not enough to classify the capture state.
  - The newest Dave traffic-evidence run had several `web read` calls that emitted readable bodies while still returning exit code `1`.
  - When that happens, verify the saved markdown body and log the source as usable-with-wrapper-caveat instead of auto-failing it.
- Tool-readiness summaries can now conflict at three different layers: header booleans, raw doctor blocks, and the final free-text note.
  - The `20260625-001332-topic-decision-elliot-vs-dave` readiness file ended with `OpenCLI Browser Bridge is still unavailable` even though repeated later `opencli doctor` blocks showed `[OK] Extension: connected` and `[OK] Connectivity`.
  - Future maintenance should trust the latest command blocks and direct smoke behavior over the stale header booleans or note paragraph.

### Evidence Used

- `workspace/memory/runs/20260625-002148-longform-research-dave-diver-jungle-traffic-evidence/query-log-reviewed.md`
- `workspace/memory/runs/20260625-002148-longform-research-dave-diver-jungle-traffic-evidence/sources.md`
- `workspace/memory/runs/20260625-002148-longform-research-dave-diver-jungle-traffic-evidence/claim-map.md`
- `workspace/memory/runs/20260625-002148-longform-research-dave-diver-jungle-traffic-evidence/source-capture-status.md`
- `workspace/memory/runs/20260625-002148-longform-research-dave-diver-jungle-traffic-evidence/PACKAGE-MANIFEST.md`
- `workspace/memory/runs/20260625-002148-longform-research-dave-diver-jungle-traffic-evidence/decision-log.md`
- `workspace/memory/runs/20260625-002148-longform-research-dave-diver-jungle-traffic-evidence/source-originals/candidate-metrics.csv`
- `workspace/deliverables/longform-research/20260625-dave-diver-jungle-traffic-evidence-report.md`
- `workspace/memory/runs/20260625-001332-topic-decision-elliot-vs-dave/tool-readiness/tool-readiness.md`

### Failed Or Lower-Weight Methods To Avoid

- Treating a raw comparison run with only platform JSON and `tool-readiness/` as reusable project memory.
- Collapsing `candidate traffic metadata` and `validated evidence` into one undifferentiated source table during topic ranking.
- Trusting Bilibili search `score` as if it were the same thing as exact video views.
- Auto-failing `web read` captures purely from the process exit code when the saved body is readable and was actually inspected.
- Trusting the final prose note in `tool-readiness.md` when the repeated doctor blocks show a newer connected state.

### Gap Report / Next Checks

- `workspace/memory/runs/20260625-001332-topic-decision-elliot-vs-dave/` is not a reusable template yet. It lacks `query-log-reviewed.md`, `sources.md`, `decision-log.md`, and any saved interpretation layer beyond raw JSON.
- If future topic-comparison runs stay intentionally small, add at least a one-page reviewed log plus a decision note so they can feed later maintenance without reopening the raw search files.
- The 2026-06-25 Dave run did not complete a new Reddit/Steam discussion pass, so this maintenance update does not add a new forum-deep-read method.
- No newer Shorts topic pack or Shorts research pack appeared in this pass, so Shorts-specific method memory still remains unchanged.
