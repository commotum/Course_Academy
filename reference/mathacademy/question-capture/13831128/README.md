# Determining Continuity from Graphs — live capture test

Math Academy task **13831128**, topic **462**, completed October 3, 2026. Selected from the live lesson queue using the highest available EDB priority, **1244.0365296803652**. The selection files preserve the queue and database scores. Completing the Square (450) and End Behavior of Polynomials (2050) had no unlocked lesson score in EDB and were excluded from ranking.

- Captured **15 practice questions**, five from each of the three knowledge points, plus **3 canonical examples**.
- All three independently drawn sequences were **CWCWC**, using the configured 0.7 weight. The probability of this three-KP outcome is 0.7³ = 34.3%.
- All 15 practice records contain a problem, observed radio field, choices, verified correct answer, activity difficulty, and expanded worked solution. Actual grading matched every intentional submission: nine correct, six incorrect. Math Academy awarded 4 of 7 XP.
- Saved **45 original image files**, with source URLs and SHA-256 hashes in `assets/manifest.json`. Every file was verified against its saved hash. Image filenames do not determine displayed choice order; the highlighted DOM option was checked before each submission.
- Saved **22 complete progress snapshots**, each containing 1,040 course-qualified topic rows from courses 113, 111, and 136: baseline, every tutorial/example/question step, and completion. The sole observed display-color change was topic 462 in course 111, white (local band 0) to the second blue band (local band 2). These bands are display observations, not exact internal FIRe repetitions or ability.
- Reused **one Codex session** for all **21 solver turns**: 15 solves and six checks against revealed explanations. Canonical examples and feedback were added incrementally.

The content transaction committed at **EDB basis 305 → 306**. It created **12 practice questions** and linked them to the correct knowledge points; **3 existing practice questions** gained difficulty and worked-solution attributes. Their answer entities were reused, including identical image files originally imported under other paths. The three canonical examples matched existing `e-` IDs and remained associated with their existing KPs.

All **4,614 protected learner and engine facts** were identical before and after the transaction. Replanning the same captured content produced no writes. See `edb-import/verification.json`, `matching-report.json`, and `commit.edn` for the database evidence; `verification.json` contains the capture audit.

Canonical examples expose no interactive answer widgets or difficulty labels. Those attributes are still pending authoring; their complete displayed problems, images, and worked solutions were captured without inventing source data.

The live test exposed and fixed two startup issues: learner IDs must be queried as strings, and initial numbered step placeholders must finish loading before processing real tutorial/example/question IDs. The checkpoint was resumed before any answer had been submitted.

This completed run used the earlier additional 5–12 second pre-submit wait. Subsequent runs credit measured Codex solving time against the randomized 5–12 second answer budget and wait only the remainder. Event waits remain 0.8–2.5 seconds. The new budget behavior and loading/priority fixes have focused regression checks.

Files:

- `content.json`: content-only import source.
- `state.json`: live checkpoints, decisions, source fields, and submission audit.
- `activity-metadata.json`: activity-page question metadata.
- `q-*-before/after.json` and `history-q-*.json`: displayed live and activity content, including original HTML.
- `example-*.json`: canonical example source content.
- `knowledge-state/`: full progress observations.
- `solver-session/` and question directories: persistent session identity, inputs, structured answers, and CLI events.
- `lesson-completed.png`: site completion evidence.
