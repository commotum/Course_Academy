/home/jake/Developer/MA/.venv/bin/python scripts/question_capture run --headless --limit 60

Topics:
    - Topic Difficulty (Initial Estimate), (What determines a topic's difficulty)
    - Topic Encompasses (Initial Estimates), (What determines whether a topic is encompassed)
    - 





In reference/engine-dependencies.dots you modeled earned xp as dependent on graded learner results. Let's check our verified progress to see which is the better model, dependent on graded learner results, or dependent on learner accuracy. Same for the fractional repetition credit.




The overall schema is sound, but the engine is not yet compatible with the current content model. I would keep the generic activity/step design and migrate the engine to it. The remaining issues are mostly application behavior, plus a few unresolved schema decisions.

I reviewed all 25 EDN files, the Rust engine, EDB’s best practices, and the recorded evidence and proposals. No files changed.

The engine still expects the deleted activity-specific schemas.

It recognizes lesson/id, review/id, assessment/id, etc., rather than activity/id plus activity/type. It also reads the old step indexes, question collections, diagnostic probes, and per-type timing attributes. A correctly populated generic activity currently fails this dispatch. Engine dispatch (engine/rust/runtime.rs:768)

The migration needs generic step traversal, nested multistep expansion, assigned-problem expansion, and diagnostic branches. We do not need to restore separate step schemas.

Queue and task priority now represent required work twice.

learner-task/priority (schema/learner/2-1-learner-task.edn:33) says a task becomes required above a threshold. Meanwhile, queue/selection (schema/learner/1-4-learner-queue.edn:21) independently marks work required, recommended, or self-selected.

This is the clearest remaining redundancy. I recommend making the queue a query over eligible, unfinished learner tasks, ordered by priority, following your newer design. Required work should have one authoritative rule. That would let us remove the separate queue records rather than synchronize two representations.
 
External assignment questions are valid content but cannot currently pass through the engine.

The engine requires every answered question to belong to exactly one KP bank and resolve to exactly one topic. That contradicts our intentional ability to import school problems before mapping them. Bank requirement (engine/rust/schema.rs:247)

Recording a response and grading it must work independently of awarding topic credit. For verified bank questions, normal FIRe updates remain appropriate. For external problems, assigned-problem/topic-coverage should guide preparation—not automatically grant mastery across every mapped topic.

Proofs and written reflections still need a decision.

Our question model supports selections and structured blanks, with required answer fields and correct answers. That fits the captured MA content, but not all the worksheet problems that motivated assignments. A multistep wrapper does not solve this. Question requirements (schema/content/4-question.edn:62)

My recommendation: initially allow written assignment work to be displayed and tracked for completion without pretending it has a machine-verified correct answer. If we want to collect and evaluate written submissions, we should explicitly design that small extension. Proofs should not become exact-string answers.

Several engine behaviors differ from our intended behavior or recorded proposals.

    Area                     Current behavior                               Needed adjustment
   ━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Assessment navigation    Earlier items must finish before later         Separate presentation order from completion
                             ones; returning to an earlier question is      order, allowing pause, navigation, and
                             rejected.                                      return.
   ───────────────────────  ─────────────────────────────────────────────  ──────────────────────────────────────────────
    Lesson readiness         Prerequisite retention is checked during       Check eligibility when starting; a
                             answer completion.                             prerequisite becoming due mid-lesson should
                                                                            not invalidate an answer.
   ───────────────────────  ─────────────────────────────────────────────  ──────────────────────────────────────────────
    Reviews                  Requires three consecutive correct answers.    The proposal recommends at least three
                                                                            questions, ending when the last two are
                                                                            correct, capped at five.
   ───────────────────────  ─────────────────────────────────────────────  ──────────────────────────────────────────────
    Question freshness       Checks questions used within the current       Exclude questions already presented anywhere
                             task.                                          in the learner’s history and reserve
                                                                            presentation atomically.

These are application changes, not reasons for new schema entities. Navigation and readiness checks (engine/rust/runtime.rs:777), review controller (engine/rust/activities.rs:58), proposed review rule and observations (reference/scheduling-proposal.md:59)

The existing learner → task → item → content relationships are sufficient for freshness checks. We still do not need question/seen-by.

The assignment-driven scheduler is not implemented yet.

We now have the necessary starting inputs: deadlines, assigned-problem coverage, the topic graph, learner progress, and task priority. The current ranker evaluates supplied candidates for retention benefit; it does not construct preparation plans from assignments. Current ranker (engine/rust/core.rs:945)

Preparation should collect the missing prerequisite closure, merge shared prerequisites across assignment problems, and prioritize useful ready work according to deadlines and estimated effort. A single shortest graph path would miss prerequisites when a topic requires several branches.

This needs scheduling code, not another curriculum hierarchy.

XP proposals need reconciliation with the assignment consolidation.

The code still requires an explicit award for imperfect lessons/reviews, rather than implementing the proposed formulas. The proposals also treat multistep as a separate task type, while our schema now represents it as content inside an assignment. Current XP functions (engine/rust/activities.rs:166)

We should preserve the intended scoring for MA-style multipart practice while explicitly deciding what school assignments earn. Arbitrary homework should not inherit mastery credit or XP merely because it shares the assignment wrapper.

Question-generator storage remains unfinished.

knowledge-point/question-generator (schema/data/5-knowledge-point.edn:34) still references an undefined generator entity. The grading proposal instead recommends a repository-relative Python path.

I agree with that recommendation: store a string path on the KP and keep the script in Git. No separate entity is justified merely to hold that path.

The generic model needs application validation and lifecycle rules.

Required-attribute specs do not enforce the rules described in their documentation. The generic interpreter must check ownership, valid targets, connected sequences, diagnostic branches, and activity-specific restrictions—for example, reviews and assessments containing questions rather than tutorials or KP expansions.

We also need stable interpretation of content already used in attempts. Editing or deleting component-owned answers can change what current response refs resolve to. Preserve referenced content or read its historical state. This does not require duplicating answer text or automatically restoring a source-step attribute.

The parts I would preserve are:

One global topic graph and learner-topic profile, shared across courses.
Separate prerequisites, KP key prerequisites, and weighted encompassing relationships.
Shared activity definitions, authored steps, and actual learner presentations as distinct concepts.
Question → answer-field → answer, with direct selected-answer refs and separate entered responses.
Separate correctness, XP, accuracy, and retention.
Status-history timing, with elapsed values treated as derived summaries.
The existing FIRe policy and progress fields; these still align with the numerical engine.

There are two qualifications to the timing model. Expanded step/time-limit-seconds needs an explicit active-time versus wall-clock meaning. Historical imports also need a timestamp strategy: EDB forbids backdating transactions before its existing timeline, so older MA occurrence times cannot always be represented by import transaction times. EDB import rules (/home/jake/Developer/EDB/docs/02_core_concepts/05_best_practices.md:312)

The evidence still supports the main distinctions we have modeled. However, fixed diagnostic outcome branches, our retry policy, and the no-repeat guarantee are deliberate local choices. The diagnostic investigation distinguishes constructing a compressed representative graph from selecting the next question using accumulated evidence; those are not automatically the same as fixed correct/incorrect edges. Diagnostic analysis (reference/diagnostic-graph-analysis.md:84)

Some older reasoning is therefore superseded: the diagnostic timing gate, course-map ordering, queue modes, and standalone multistep scoring should not silently become implementation requirements.

Verification reflected that split:

45 Rust tests passed.

The native EDB check installed all 25 current schemas, then failed on an obsolete assessment fixture with schema/unknown-attribute.

The passing unit suites use older activity fixtures, so they do not establish compatibility with the current schema.

My recommended order is to settle the queue and written-assignment decisions, migrate the generic content interpreter, then implement the agreed scheduling, grading, freshness, and XP behavior. The FIRe mathematics does not need a wholesale redesign.
