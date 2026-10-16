# Factorial control recovery — 2026-10-11

The seven original question records are now committed to the rebuilt `math` lineage with their original problem statements, worked solutions, stable UUIDs, and owning knowledge-point links. Per the user’s explicit authorization, they have **zero answer fields** for now: complete original control sets have not been found in the sources checked. No distractors or response types were invented. The original manual transaction and receipt remain unchanged; that transaction targeted `course-academy-v2`.

## Why the completed history has no controls

The Math Academy history renderer explicitly creates `questionText` and the grade/details row. Its `loadAnswers` switch renders controls for `FR`, `SS`, `DS`, and `PR`; it has no `MC` case. Multiple-choice history therefore omits the original choices. For an incorrect MC response, it separately displays only the selected learner answer under the explanation. That single displayed value is not a complete choice set.

This is supported by the public `/js/task-answers.js` recovered from all four runner browser caches, each with identical decoded SHA-256 `ddc6a94fd74e3e3f24eb82483cf425e27f6dd1e3451d142f7905e4cdcafaae1c`. See `task-answers-ddc6a94fd74e3e3f.js`, lines 200–207 and 246–264, and `cache-inspection.json` for cache and body hashes. This explains why even q-73002 and q-5371, whose archived original multiple-choice widgets are available, now expose zero fields in completed history. The controls are absent from the source DOM; widening the extractor cannot restore them.

## Types and recovery results

| Question | Original controls verified? | Supported type conclusion | Recovery |
|---|---|---|---|
| q-122027 | No | MC/radio likely, unverified | Original choices unavailable |
| q-122033 | No | MC/radio likely, unverified | Original choices unavailable; displayed learner answer cannot supply the missing list |
| q-124400 | No | MC/radio likely, unverified | Original choices unavailable |
| q-124403 | No | MC/radio likely, unverified | Original choices unavailable |
| q-73003 | No | MC/radio likely, unverified | Original choices unavailable |
| q-73005 | No | MC/radio likely, unverified | Original choices unavailable |
| q-73014 | No | MC/radio likely, unverified | Original choices unavailable |
| q-73002 | Yes, archived lesson widget | Multiple-choice, mapped to radio | Five original choices available; already present in database |
| q-5371 | Yes, archived lesson widget | Multiple-choice, mapped to radio | Five original choices available; already present in database |

The likely classification of the seven follows from the renderer behavior, the lack of FR/structured body output, and archived same-KP multiple-choice widgets. It is an inference, not exact-ID control verification. Their old manually authored distractors must not be presented as Math Academy choices. Correct mathematical values and worked solutions cannot establish the original response type or full choice set.

## Sources inspected

- Original factorial package, manual review and transaction; current-lineage reconciliation and old UUID readback.
- October 4 saved completed-history records and October 11 expanded history, including all sibling question/explanation nodes.
- Local MA `DATA` and `WORKING-PROGRESS` HTML/JSON/Markdown exact-ID searches: none of the seven appears. The archived `/topics/774` lesson contains six other original multiple-choice widgets, including q-73002 and q-5371.
- Cached visible `/learn` and `/topics` HTML from four runner profiles: 108 entries, no target IDs. The cache search excluded internal API responses. None of these profiles contains a browser `History` database.
- A fresh, bounded read-only `/topics/774` inspection: the current visible lesson contains tutorials and canonical examples, with zero question widgets. See `topic-visible-*.html`, screenshot, and `visible-inspection.json`.
- The completed q-122027 visible help menu: only “Report a content error”; no question preview or choice recovery control. See `history-help-visible-*.html`, screenshot, and `visible-inspection.json`. No report was sent.

The foundations runner was checkpoint-stopped while outside a timed assessment, inspected through the normal `MathAcademyBrowser`, then restarted in `finally`. An initial selector timeout also restarted cleanly. No activity was answered or replayed, and no hidden answer keys or internal API payloads were queried. Credentials, profile files, learner attempts, and full checkpoints were not sent to a solver; no solver was needed.

`findings.json` preserves the earlier control-recovery findings and evidence hashes. Those findings concern the missing controls; they no longer block the explicitly authorized fieldless original-content import.

## Current committed result

The normal native Committer committed 35 Math Academy assertions and zero retractions at basis **1155 → 1156**. Pinned readback confirms all seven exact original texts and historical UUIDs, their seven own-KP memberships, unchanged prior KP metadata and memberships, zero answer fields, and a no-op second preparation. The immutable source input SHA is `53b5460082f7067d6eb202047b0fcaf404cdee52e631787fca8547692ea51815`; the writer refuses changed inputs before creating a database client. See [native verification](../fieldless-original-content-inputs/native-fieldless-content/verification.json) and [independent receipt/readback QC](../fieldless-original-content-inputs/independent-committed-readback-qc.json).

This repairs original question content only. Exact original answer widgets are still not found in the sources checked. Future control recovery must use exact-ID source evidence and the normal guarded database pipeline.

## Capture chronology and search boundary

The displayed lesson occurred October 3, 2026, around 12:51–12:56 PDT, before the earliest preserved capture-engine commit at 17:10 PDT. The timestamped completed-history capture was saved October 4 at `2026-10-04T22:57:57.915Z` (15:57 PDT). The earliest preserved factorial pilot text was derived from completed history, rather than a live original question-widget capture.

The later bounded `rg -uuu` search included ignored `scripts/question_capture` and `.local/question_capture` paths, repository `reference` and `.local` sources, and the local `/home/jake/Developer/MA` tree. No exact owning live `step-qN` root or complete target radio/select control IDs were found for these seven. The replacement-evidence fixture is a copied authoring package; `simulated-q-73003` explicitly labels itself simulated and “DO NOT COMMIT.” Neither supplies original choices. Browser-profile bodies, internal API payloads, deleted Git objects, and remote sources outside this search were not treated as inspected evidence. This is a bounded “not found” result, not a claim that no original source exists anywhere. See [chronology and search evidence](../fieldless-original-content-inputs/chronology-and-bounded-source-search.json).
