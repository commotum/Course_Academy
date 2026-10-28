# Lesson-wide radio-to-checkbox migration — 2026-10-28

Committed and verified at EDB **T9990 → T9991**, source `:agent/codex`. Live grading verified at T9998.

Lesson/topic `17592186048123` — Global vs. Local Extrema and Critical Points. Audited all **29 questions** across both KPs: `17592186064162` (Identifying Extrema of a Function Given Its Graph) and `17592186064273` (Identifying Critical and Stationary Points of a Function Given Its Graph). This includes 27 practice questions and two canonical worked examples.

## Outcome

- Converted **nine radio questions** to **34 owned Boolean checkbox fields**, each displaying a complete x-value, complete statement, or a documented point label beside its shared graph.
- Removed the redundant “None of the above” field from one existing checkbox question, preserving its other three field/answer identities. None is represented by an empty selected subset.
- Resolved two missing keys independently from the graphs during conversion. Did not invent difficulty labels or missing worked solutions.
- Mapped **four saved response items** without changing status, elapsed time, timestamps, scores, progress or XP. All 45 old radio choices, including wrong and empty-subset choices, have explicit semantic mappings.
- Retained seven radios, six other existing checkbox questions, four numerical-entry questions and both canonical examples.
- Retained all **57 detached old field/answer entities** unchanged. Only reviewed question text/field links, two solutions’ references to removed Roman labels, and equivalent task-item response links changed.

## Converted questions

| Entity | Imported source | Correct subset |
|---|---|---|
| `17592186064800` | `q-47692` | x=1, x=3 |
| `17592186064802` | `q-47913` | x=3 |
| `17592186238008` | `q-103442` | I |
| `17592186329838` | `q-47911` | x=2, x=4 |
| `17592186341964` | `q-73399` | x=3, x=7 |
| `17592186341965` | `q-73401` | x=0 |
| `17592186600826` | `q-73400` | x=2, x=8 |
| `17592186600837` | `q-48736` | I, II |
| `17592186620891` | `q-47693` | A |

The question originally reported, `17592186341965` (`q-73401`), now has independent `$x=0$`, `$x=2$`, `$x=6$` checkboxes, with only `$x=0$` true.

The missing original keys were on `17592186064800` (`q-47692`: critical points x=1 and x=3) and `17592186064802` (`q-47913`: stationary point x=3). Both conclusions were directly verified on their graph rasters and match an offered original radio alternative. Existing keys on the other seven conversions take priority and were independently confirmed. Detached unkeyed old fields remain unchanged.

Cleanup: `17592186238006` (`q-103438`) now has only its three substantive statements. Its saved correct response loses only the redundant false response to “None”; all substantive selections stay unchanged.

## Retained radios

Five questions describe whole intervals or interval unions: `17592186238003`, `17592186238004`, `17592186329839`, `17592186403633`, `17592186403640`. Turning them into disjoint selectable atoms would redesign the response, rather than convert an existing finite list.

Two questions choose one whole graph: `17592186064801` and `17592186620883`. They retain the single-graph response contract. The former already lacked its original answer key; this separate content issue was recorded and was not hidden by a response-format conversion. No graph-image key was guessed from entity or display order.

Existing source derivative-index typos in the solutions of `q-47911` and `q-103442` are separate content issues. Mathematical graphs and stored keys agree; the typos were preserved rather than silently changed as part of this migration.

## Verification

- Read one captured immutable basis for the audit, then refreshed current question/ownership/response state before the one guarded batch.
- Native preview used the deployed writer EDB library and the application’s actual validation callbacks, including answer, field, question and affected task-item ensures. Speculative `db_after` was pulled and checked.
- Presentation lint passed for all ten proposed changes, their speculative readbacks and committed readbacks.
- Actual learning UI: ten desktop and ten phone-width previews passed with no math/image/field errors. All ten sets of rendered checkbox captions were visually reviewed; representative full solutions and phone layouts were also inspected.
- Native grader: 37 correct Boolean choices accepted, 37 incorrect choices rejected, ten complete canonical subsets accepted, 37 single-checkbox flips rejected, ten incomplete responses rejected. All 45 old radio choices and eight consistent prior checkbox subsets preserved their whole-question grades.
- Production read-only preview-answer API: **110 checks passed**, covering canonical subsets, every single flip, all original choices, consistent prior subsets and empty selections. These checks wrote no learner state.
- Eight presentation-lint tests passed.
- Exact committed readback compared all 29 questions, retained original entities and saved item states. Historical pre-migration reads were independently checked at T9990. Receipt datoms were checked against the exact prepared assertions/retractions and their explicit contributor.

## Handoff

Neither KP has a registered question generator, so no generator update is claimed. Future generator source snapshots must be captured from the converted database.

`case-ledger.json` contains every resolution, source/object mapping, independent key evidence, prior response mapping, committed request identity and follow-up notes. `status.json` separates converted, retained and cleanup IDs. `commit-receipt.json` confirms the transaction; `publication/requests/capture-8e7e1353-8606-4027-91e8-dd5a9a349d73/` retains its exact request, transaction, preview and receipt. No pending request remains.

Other evidence: `capture/`, `questions.json`, `topic.json`, `graphs-*.png`, `review/`, `native-build.json`, `engine-input.json`, `engine-report.json`, `render/`, `render-narrow/`, `publication/committed-verification.json`, `verification.json`, `live-grading-verification.json`, `completion.json`.

The earlier single-question assessment at `reference/edb-math/audits/2026-10-28-radio2checkbox-17592186341965/` remains historical evidence of the pre-migration state.
