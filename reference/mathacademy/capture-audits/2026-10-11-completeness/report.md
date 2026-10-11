# Capture completeness review — 2026-10-11

The highest-priority defect is incomplete question-body extraction. **35 normalized questions across seven new-engine captures omit authored proof, fill-in, or table content. 31 of those truncated prompts are stored in the current database; four proof questions are absent.** Increasing browser delays will not repair this: the missing sections are present in saved source HTML.

This is a review and recovery inventory. The fixes below are recommendations; this audit changed only audit artifacts. It did not change capture evidence, runner configuration, principles, or database content.

## Scope and checks

Audited 1,223 activity packages: 1,160 completed legacy engine activities, 57 completed new-engine activities, five earlier standalone captures, and one standalone diagnostic. Together they contain 12,581 question occurrences and 1,828 canonical-example occurrences; these are archive occurrences, not unique database entities. The new-engine snapshot is frozen at **2026-10-11 03:12:27 PDT / 10:12:27 UTC**. Four active captures and captures completed after that cutoff are excluded.

Checks covered required question/answer structure, source-backed answers, source identity reconciliation, lesson step coverage, final judgments, saved source paths, original asset hashes, historical progress records, recorded import omissions, and current database identity coverage. Four saved-DOM reproductions ran in a local browser with network requests blocked. Legacy records were assessed with the legacy engine's own `prepare_authoritative_content`; they were not rejected merely for lacking the new engine's evidence schema.

Database reads were pinned to **math, basis 269, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1**. Of 14,216 distinct source question/example IDs across the packages, 14,153 are present and 63 absent. Identity presence alone does not verify answer fields, provenance, lesson membership, or question correctness.

The audit is a structural and provenance review, not a fresh mathematical solution of every archived question. Source-code hashes and artifact hashes are in [audit.json](audit.json); per-capture findings are in the linked JSON files below.

## 1. Full question bodies are omitted — highest priority

[capture/scripts/browser/extract.js](/home/jake/Developer/Course_Academy/capture/scripts/browser/extract.js:226) reads `.questionText` / `.questionWidget-text` and the graphic, but ignores sibling `.questionBody` and `.questionWidget-body` sections. It nevertheless finds their answer controls elsewhere in the question node. The result can have complete choices and answer keys while omitting the sentences or table that define those controls.

For example, `linear/14114596` stores ten questions whose entire normalized problem is “Select the correct options in the reasoning below.” The missing reasoning remains in the source HTML. `q-182663` retains “Find the missing values in the following truth table:” but loses the truth table. Four proof questions in `linear/14114805` omit `.questionWidget-body` even in the live extraction; using the saved live problem alone cannot recover these four.

| Task | Title | Truncated prompts | Question IDs |
| --- | --- | ---: | --- |
| 14108275 | Parity | 4 | q-184106, q-183996, q-184115, q-184100 |
| 14108276 | The Maximum and Minimum of a Set | 4 | q-181731, q-182007, q-181726, q-182027 |
| 14109722 | Conditional Statements | 1 | q-182663 |
| 14114517 | Parity | 8 | q-184102, q-184120, q-184128, q-184131, q-184073, q-184080, q-184000, q-184062 |
| 14114596 | Integer Divisibility | 10 | q-221902, q-221906, q-221901, q-221908, q-221899, q-221914, q-221915, q-221921, q-221916, q-221913 |
| 14114643 | Singular Value Decomposition of Larger Matrices | 2 | q-363823, q-363828 |
| 14114805 | Disproving Universal Statements | 6 | q-221691, q-185001, q-221707, q-221701, q-221834, q-221775 |

All 31 matching database records contain the same truncated prompt at basis 269. The remaining four are `q-221701`, `q-221707`, `q-221775`, and `q-221834`.

This selector gap also exists in [the old DOM extractor](/home/jake/Developer/Course_Academy/scripts/question_capture/dom.js:209). However, [legacy authoritative preparation](/home/jake/Developer/Course_Academy/scripts/question_capture/authoritative.py:250) restores the original **before** problem rather than replacing it with history's shorter prompt. That reduced the history-overwrite problem in the old pipeline. The legacy source scan found no archived live questions with a nonempty sibling `.questionWidget-body`; that result does not establish universal support for every possible old HTML layout.

**Fix:** extract every authored problem section once, preserve table structure and answer positions, and exclude explanation, learner-response, and grading metadata. Use the same canonical rendering for live and history layouts before binding them. Preserve originals and existing identity/field matching guards; do not relax identity checks or remove meaningful mathematical whitespace to force a match. Add regressions using these actual source layouts, including completed proof bodies and a truth table.

Evidence: [new-captures.json](new-captures.json), [database-suspect-prompts.json](database-suspect-prompts.json), [legacy-prompt-bodies.json](legacy-prompt-bodies.json).

## 2. Completed proof history is falsely marked incomplete

[extract.js](/home/jake/Developer/Course_Academy/capture/scripts/browser/extract.js:231) requires an internal final-result element for staged questions. Completed history places the overall grade outside that node. [adapter.history](/home/jake/Developer/Course_Academy/capture/scripts/browser/adapter.py:832) overlays the parsed grade after extraction, without recomputing field completeness.

Six questions are affected: four in `linear/14114805` and two in `linear/14114643`. Their saved history shows `Correct` and correctly graded select fields, but extraction returns `answer_fields_complete=false`. The four proof-lesson records were omitted. The two matrix-review records were imported with zero recorded omissions, but both still fail the **current** validator; their archived preparation also retains the false flag. Zero historical omissions therefore does not prove that this flag was repaired.

**Fix:** include trusted, visibly parsed history grading context in the completeness decision and verify the whole observed field layout and completed proof stages. A correct field alone must not imply that an unfinished proof is complete. Keep the full source body, rather than treating grading as a substitute for it.

Evidence: [history-dom-reproductions.json](history-dom-reproductions.json).

## 3. Final-answer evidence checks happen too late

Four raw questions in `foundations/14116310` lack confirmed answer evidence: `q-103560`, `q-20359`, `q-105187`, and `q-72785`. Their final judgments use a correct-grade attribution without the verified presentation binding needed by `finalize_answers`. A mathematically correct judgment does not make that attribution source-backed.

[ActivityCapture._review](/home/jake/Developer/Course_Academy/capture/scripts/activity/capture.py:693) checks structural capture gaps before judgments and saves finalized answers without feeding failed authoritative evidence checks back to the agent. Preparation subsequently recovered three answers using checked worked-solution quotations; `q-103560` remains omitted from that import. Its source ID already exists in the database from other content, which does not make this capture's import complete.

**Fix:** run authoritative answer checks after finalization. For a recoverable evidence gap, request a bounded, focused follow-up judgment that identifies a checked source quotation or direct visible answer. Persist that repair and judgment with the capture. If evidence remains unavailable, preserve an explicit final limitation and continue the activity; never promote a guess or fieldless history grade into a confirmed answer.

## 4. Historical captures are not reconciled after extraction or preparation fixes

The same quiz still contains an unreconciled live `q-181457` and fieldless history record. Re-extracting its saved HTML with the **current** static-blank fix produces one blank field and an exact source match. This is historical reprocessing work, not another remaining inline-blank selector defect.

Preparation works on a copy and can repair answers without updating `content.json`. The quiz's three preparation-only answer repairs therefore remain missing from the saved capture. Completed outbox entries are terminal, so a fixed extractor does not automatically cause them to be reread or reimported.

**Fix:** provide an explicit archive-and-reprocess path for affected completed captures. Preserve old checkpoints/content/results, regenerate from saved HTML, obtain fresh judgments for changed evidence, retain UUIDs, and reset only the corresponding outbox work. Commit through Database Commit with preview, commit, and readback verification. Record which validation/extraction version and evidence hash produced the final completeness finding.

## 5. Progress cards hide partial imports

Two new captures have **10 omission records** despite `import_status=verified`: four in the quiz and six in the proof lesson. These include unreconciled originals and an omitted assessment structure; they are not ten distinct missing database questions.

[monitor.snapshot](/home/jake/Developer/Course_Academy/capture/scripts/monitor.py:74) counts only nonterminal outbox items. “Imports 0” means no pending imports. `verified` verifies the submitted database work, not completeness of every captured source record.

**Fix:** label the count “Pending imports” and separately display captures with omissions/unresolved content. Keep database verification and capture completeness as separate recorded outcomes. Detect source controls that have lost their authored problem positions; the present placeholder check catches missing controls referenced by text but misses controls whose entire containing body disappeared.

## 6. Older progress observations need a source-based backfill

48 of the 57 new captures predate normalized course-percentage and topic-comparison records. All 48 retain the Learn-page HTML with `#coursePercentComplete`; the exact displayed percentage can be recovered. Saved observations support 46 historical before/after topic comparisons. The first observations in `foundations/14109531` and `linear/14108275` have no comparable baseline; mark those unavailable rather than inventing one.

The nine newer captures have the normalized records. This is an older-archive gap, not evidence that the restored current reader is failing.

**Fix:** backfill only from saved source HTML, original observation times, and saved color/band snapshots. Preserve XP, retake instructions, completion dates, and current account progress. Do not rerun `post_activity.record` on old activities, because it mutates account ledgers. Course completion remains the **authored Learn-page label**, with no calculated completion percentage or percentage delta. Display bands remain observations, not exact FIRe state.

Evidence: `historical_progress_recovery` in [new-captures.json](new-captures.json).

## 7. Legacy answer provenance still needs review

All 1,160 legacy archives have their basic normalized question structure. All legacy question and example IDs are present in the migrated database. No legacy canonical example was held by the source checker.

The strict legacy checker cannot independently confirm **3,454 practice-question occurrences / 3,440 unique question IDs** across 1,069 captures. Its only held category is `unconfirmed_correct_answer`; it found no missing original captures, unresolved source markup, or identity mismatch. 2,921 held occurrences belong to archives with a local legacy commit-verification record.

These are provenance findings, not a claim that 3,454 answers are wrong or absent. Many legacy answers were recorded as `model_interpretation`, and other later imports or corrections may supply evidence outside that activity's checkpoint. The checker does not perform general mathematical interpretation of worked solutions.

**Fix:** review unsupported attributions using saved visible source answers, grading receipts, and checked worked-solution quotations. Keep our reasoning separate from Math Academy's originals. Reconcile any later confirmed source records before proposing changes to existing answers; do not blindly overwrite or recreate the content.

Evidence: [legacy-captures.json](legacy-captures.json).

## 8. Standalone packages are outside the automatic import path

Five earlier standalone packages and one standalone diagnostic have their basic saved question structure. Their formats differ from both engines' checkpoints and were checked separately.

Of the 63 source IDs absent from the current database:

- Four are the new proof questions identified above.
- 23 belong to the standalone diagnostic `14033238`, explicitly saved in capture-only mode.
- 29 belong to standalone lesson/review/multistep/assessment captures explicitly recorded without database commits.
- Seven belong to `factorials-13831129`, whose old local receipt reports a commit: `q-122027`, `q-122033`, `q-124400`, `q-124403`, `q-73003`, `q-73005`, and `q-73014`.

The seven factorial source-ID absences need reconciliation. The old receipt does not bind the current database lineage, and absent source IDs do not establish whether the UUIDs were retained under other facts. The other 52 standalone absences are consistent with their explicit no-import records and should not be presented as migration failures.

**Fix:** inventory standalone packages explicitly when undertaking historical recovery; normal runners discover their configured output directories, not every earlier manual package. Verify existing UUIDs and original source bindings before importing any missing content. Preserve intentional capture-only behavior.

Evidence: [standalone-captures.json](standalone-captures.json), [database-coverage.json](database-coverage.json).

## Checks that passed and repair order

All 6,427 manifested legacy asset files checked passed SHA-256 validation; the new-engine audit checked 140 original asset files with no missing/hash findings, and all 25 standalone diagnostic manifest assets passed. The new snapshot has final judgments for all 318 question records and 52 examples; its 44 tutorials and canonical lesson step coverage have no detected structural gaps. These checks do not excuse the separate missing-body findings.

Repair full-body extraction and proof completeness first, then reprocess the seven affected captures and quiz. Add post-finalization source validation and visible omission reporting, reconcile prepared repairs back into capture evidence, and backfill historical progress. Treat legacy provenance and standalone database reconciliation as explicit recovery inventories rather than changing guesses into confirmed facts.

Every repair should preserve originals, reuse supported identities, obtain final agent judgments, continue activity progress, and use the normal database preview/commit/verify path, following [capture/principles.md](/home/jake/Developer/Course_Academy/capture/principles.md). The principles were reviewed and left unchanged.
