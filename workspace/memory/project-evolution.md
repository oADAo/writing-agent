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
