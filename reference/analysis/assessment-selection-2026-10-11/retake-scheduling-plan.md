# Required assessment reviews and optional retakes

Proposal dated 2026-10-11. This document does not implement scheduling or change the database. Assessment weights are already implemented: initial 50/40/10 and remedial 45/40/15, read from the active database policy. The application has one learner.

Later choices are recorded in the root [scheduler report](../../../scheduler-report.md). Its confirmed rules supersede earlier alternatives here, including the below-75% retake cutoff without an expiry exception, whole-assessment submission with editable drafts and no skipped outcomes, and signed earned-XP accounting.

## Intended behavior and evidence

The lifecycle is: finish an assessment → require practice on missed topics → complete that practice → offer an optional retake alongside normal study.

Math Academy's [FAQ](https://mathacademy.com/faq) explicitly describes immediate missed-topic reviews followed by an optional retake on the same topics with different questions. It also describes reviews after exceeding the quiz time limit. Our [eight captured retake pairs](retake-behavior.md) support this sequence: in four fully observed non-expired sequences, the retake first appears immediately after the final required-topic review, alongside other work. There is no observed additional XP requirement or cooldown.

Retake eligibility is a separate issue. Four fully traced originals scoring 63.64–71.43% produced offers; 22 originals scoring 76.92–90.91% did not show offers after their reviews. **Proposed default: offer one retake when the original score is below 75%, or the original expires with unresolved questions.** The precise Math Academy cutoff is unknown. The 75% rule is our provisional implementation choice; requiring missed-topic reviews applies at every score. It is independent of an eventual controller targeting 80% expected accuracy.

## Scheduling rules

1. Keep answers as editable drafts until the learner selects Submit or the time limit expires, then freeze and grade the entire assessment together. Derive affected topics from the frozen route and final answers. Wrong and unanswered questions require review at either form of finalization, without recording invented wrong answers or incorrect-answer FIRe events for unanswered slots. Navigation and draft edits do not submit individual answers or create skipped outcomes. Deduplicate topics within the attempt and finalize score, XP, and obligations once. Apply the same submission behavior to retakes.
2. Immediately establish outstanding practice obligations and prepare the corresponding reviews. Reuse a suitable unstarted review where possible, linking it to the triggering assessment; do not count practice completed before that assessment. Required assessment practice survives course changes and self-directed mode.
3. While required remediation is ready, show only that work and prevent starting or resuming unrelated study through every API entry point. A failed required lesson keeps its obligation but waits for five other successful practice activities. Other ready required remediation takes precedence; if all remaining remediation is waiting for retries, temporarily allow ordinary study. At five successes, the eligible fresh-question lesson retry becomes required again. Keep the associated assessment retake unavailable until all obligations resolve. Reading content and history remains available. An already running timed assessment may finish or expire; its clock is not suspended to enforce this gate. Raising a numerical priority alone is insufficient.
4. Passing a linked review clears its obligation under the existing review completion rule. If a remediation review fails, immediately require the full lesson on the same topic, linking it to the original assessment. Add no cooldown or new 48-hour wait before this replacement lesson. Passing that linked lesson clears the topic obligation without an extra automatic review; failure or unfinished work does not clear it. If the lesson fails, apply rule 3's five-successful-activities break; another failure at the same KP without further progress triggers key-prerequisite remediation. Preserve the failed attempts and their outcomes. The same review-to-lesson escalation applies to key-prerequisite remediation after repeated lesson failure, with that origin's learning-path gate. Ordinary review failures only update learner state and end; they do not force a lesson.
5. Once every obligation for an eligible original is resolved, offer the retake on the next queue refresh, with no cooldown and no new 150-XP requirement. Normal study becomes available at the same time. The retake remains optional indefinitely: no XP countdown, required-priority promotion, or prerequisite blocking normal progress.
6. Retake misses immediately create required practice again. After that practice, return to normal study. Offer at most one retake per original automatically, matching the observed sample; do not generate an endless retake chain.

The first implementation applies to new locally completed assessments after rollout. Do not manufacture outstanding obligations or retake relationships for partially imported historical records.

## Retake contents and weights

- Derive the retake's topics from the original assessment's reserved questions: one question per original topic, preserving the KP of its original question. Topic sampling does not mean one question for every KP in a topic. Recheck previously correct topics as well as missed topics. All 67 captured retake questions were fresh questions on the original knowledge points; 34 rechecked previously correct topics.
- Select fresh alternatives within each original knowledge point using the existing assessment **remedial 45/40/15** database weights. Ordinary assessments continue using initial 50/40/10. Remediation reviews keep the existing review weight policy.
- Initially aim to cover every original knowledge point. This is a simple explicit rule, rather than a claim to reproduce Math Academy's unknown omission rule: five of eight captured retakes omitted one or two original topics. Existing locally generated originals have at most ten questions.
- If a knowledge point lacks a valid fresh alternative, show the supply shortage and retain the pending offer; never substitute the original question or silently declare the topic reviewed. Required-review shortages remain visible and trigger replenishment rather than disappearing from the queue or changing the activity to a full lesson solely because supply is short.
- Reserve a retake's route atomically when preparing it and preserve the route once prepared. Database weight edits affect subsequent preparations, consistent with existing activities. Keep both attempts and their XP in history. Retake XP is additive; completing a retake must not restart the ordinary assessment cadence, and merely having an optional retake must not prevent scheduling the next ordinary quiz.

## Minimal schema and code changes

Propose two optional noncomponent task-to-task references in `schema/learner/2-1-learner-task.edn`, mirrored to the SSD schema:

| Attribute | Cardinality | Purpose |
| --- | --- | --- |
| `:learner-task/retake-of` | One | Link a retake attempt to the exact original assessment attempt. |
| `:learner-task/remediation-for` | Many | Link a review or replacement relearning task to the assessment attempt(s) that made it required. |

These capture relationships currently absent from the schema. Use reverse navigation for originals' retakes and practice tasks. Derive reasons, missed knowledge points, readiness, timestamps, and counts from original content, outcomes, linked practice, and status history. No new weight attributes, activity type, score field, readiness flag, or stored countdown is needed. Keep the existing required-attribute validation spec; add application checks for reference targets, allowed task kinds, no self/cyclic retake links, and at most one generated retake per original.

Implementation touches:

- `engine/rust/retrieval.rs`: derive assessment-specific obligations; prepare required practice and same-knowledge-point retakes; distinguish ordinary versus retake history/cadence; keep optional offers separate from ordinary-assessment pending detection. Remove the self-directed/course restriction for assessment obligations without changing ordinary review scope.
- Assessment cadence in `history`: remove the per-award `.max(0.0)` from `:learner-task/xp-earned` reads and sum signed finalized qualifying practice awards. Do not alter earned-XP formulas or introduce another stored balance. Verify that 140 XP followed by a -1 award becomes 139, and that only ordinary assessment completion/expiry resets cadence, with retake rewards excluded.
- `engine/rust/learning.rs`: apply a shared obligation gate to automatic and self-directed candidates, instead of only sorting higher priorities first.
- `scripts/learning_api.rs`: persist origin links with task creation; refresh after terminal outcomes; enforce the same gate for start, resume, and direct topic study. Reuse exact-basis transactions and stable requests to prevent duplicate tasks on retries or concurrent refreshes.
- Home and task/history presentation: display “Required review after Quiz …”, remaining required topics, supply shortages, and “Optional retake”. Show which original caused each task and which knowledge points the retake contains.

Install the two attributes in a schema-only transaction before writing facts that use them, then deploy the implementation. Preserve all existing attempts and prepared routes; do not replay the default policy seed. Attribute authored schema/configuration transactions to the established assistant source and retain preview/receipt evidence.

## Question counts and time budgets

Math Academy's Justin Skycak [explains](https://www.justinmath.com/chalk-and-talk-podcast-42/) that quiz counts are calibrated to expected question-solving time: lower grades may have about 20 questions in 15 minutes, while calculus may have six or seven. The quiz is assembled before starting; its advertised count and time limit are already on our captured cards. The live timer enforces the deadline on that assembled quiz.

Our [assessment inventory](assessment-tasks.csv) has 41 known 15-minute quizzes ranging from **4 to 13 questions**. The five automated retakes advertise **12–14 minutes**. Difficulty labels alone do not determine counts: quiz 14095468 has five questions and no Hard questions; quiz 14094319 has twelve questions and no Hard questions. Topic complexity and expected workload matter. The captures do not expose Math Academy's duration formula or explain each omitted retake topic.

Our current engine uses a flat **90 seconds per question**, with a **900-second limit**, yielding at most ten questions and requiring at least five eligible topics for an ordinary assessment. This is an approximation, not Math Academy's sizing algorithm. The later [chosen assembly rule](../../../scheduler-report.md#7-assessment-sizing-and-workload-estimates) replaces this estimate in the planned implementation.

The chosen ordinary-assessment plan reserves one easy, one moderate, and one hard question from distinct eligible topics, using provisional **1/2/3-minute** estimates. Fill the remaining nine minutes through weighted topic draws without replacement and database difficulty weights, restricted to available bands that fit. Shuffle and freeze the completed route before start. Use existing `step/expected-seconds` and `activity/expected-seconds` for estimates; no new duration attributes are needed. The minimums and budget restrictions change realized difficulty proportions. Keep the actual 15-minute timer independent and defer the accuracy controller.

Retakes keep one fresh question per original topic, preserving its original KP, and use remedial 45/40/15 weights. Before each draw, restrict available difficulties to choices that leave a feasible completion for every remaining original topic within 15 estimated minutes and with at least one easy, one moderate, and one hard overall. Redistribute the database weights over those choices. This adds lookahead to the ordinary budget-aware sampler because a retake must cover its fixed topic list. Prevent overruns during assembly; this rule supersedes the earlier resampling and minimum-change repair proposals. Shuffle and reserve the completed route before start.

The original's difficulty assignment provides a feasible combination for originals assembled under the new rules. Check fresh supply before assembly; replenish missing questions and retain the pending offer rather than dropping original topics or KPs, adding unrelated topics, reusing seen questions, or relaxing minimums. Later solving-time evidence can refine the estimates without changing the basic assembly process; the 1/2/3 estimates are our starting policy, not a recovered Math Academy formula.

## Verification before rollout

Exercise the whole sequence in isolated engine/native-EDB fixtures: immediate obligations at high and low scores; timed-out unanswered questions and navigation without skip outcomes; all-review completion; failed remediation reviews replaced by linked required lessons; successful replacement-lesson clearance without another automatic review; ordinary failures without forced follow-up; optional retake availability; fresh same-knowledge-point selection and remedial weight updates; retake misses with no third attempt; original/retake XP and ordinary cadence; course/manual/start/resume gate bypasses; shortages; retry/concurrent-refresh deduplication; and preservation of prior routes and imported history. Run the existing Rust and native API suites, preview schema transactions, and verify the deployed queue through the API after rollout.
