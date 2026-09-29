# Scheduling proposal

Proposed initial policy, September 29, 2026. This combines Math Academy's published mechanisms, Jake's captured activity, and explicit local choices. It specifies behavior for our application; it is not a claim to have recovered Math Academy's private selector. No schema or runtime changes are made by this document.

The central recommendation is a dynamic menu: finish any current task, resolve required work, then choose among useful lessons, reviews, and multisteps. Self-selected lessons enter the same delivery and learning-update path. Every completed question updates the available evidence; task completion can award XP, establish lesson mastery, create remediation, and refresh the menu. Opening the application also refreshes due reviews, because retention can change without a new answer.

## What the evidence supports

| Finding | Evidence and its limit |
| --- | --- |
| The menu changes with the learner's state; it is not a fixed course list. | The [practice FAQ](<The Math Academy Way/VI-FREQUENTLY-ASKED-QUESTIONS/FAQ-The-Practice-Experience/FAQ-The-Practice-Experience.md>) describes lessons replacing redundant reviews and importance based on implicit review coverage and useful future content. It does not publish numerical ranking weights. |
| Review compression should favor work that rehearses several needed skills. | [Learning efficiency, chapter 31](<The Math Academy Way/V-TECHNICAL-DEEP-DIVES/31-Technical-Deep-Dive-on-Learning-Efficiency/31-Technical-Deep-Dive-on-Learning-Efficiency.md>) describes covering due repetitions while gaining future repetitions and maintaining several learning branches. Prerequisite edges alone do not establish rehearsal coverage. |
| Remediation has specific triggers. | [Targeted remediation, chapter 21](<The Math Academy Way/III-COGNITIVE-LEARNING-STRATEGIES/21-Targeted-Remediation/21-Targeted-Remediation.md>) describes a break after a failed lesson, key-prerequisite reviews after failure twice at the same point without progress, and a review of every topic missed on a quiz. |
| Jake's quiz errors were followed by the corresponding reviews. | The [September 24 capture](fire-live-account-analysis.md#the-quiz-errors-identify-the-intervening-review-topics) matches three incorrect quiz topics to three subsequent reviews. It does not expose their assignment times or mandatory flags. |
| Assessments mix previously learned topics and test automaticity. | The [practice FAQ](<The Math Academy Way/VI-FREQUENTLY-ASKED-QUESTIONS/FAQ-The-Practice-Experience/FAQ-The-Practice-Experience.md>) includes older learning, describes the 80–85% accuracy target, and distinguishes assessment conditions from first learning. [Chapter 20](<The Math Academy Way/III-COGNITIVE-LEARNING-STRATEGIES/20-The-Testing-Effect-Retrieval-Practice/20-The-Testing-Effect-Retrieval-Practice.md>) says timed testing follows successful untimed performance. |
| One question per topic is a strong starting assessment rule. | All [13 captured assessments](assessment-topic-observations-2026-09-28.json) contain distinct topics: 118 questions total, with 7–12 questions per assessment and no repeated topic within one assessment. This includes three retakes. The difficulty totals are 58 E, 50 M, and 10 H, a sample-specific mix rather than an identified quota. |
| Assessment size follows workload rather than a fixed count. | The [XP investigation](mathacademy-xp-analysis.md#how-base-xp-is-assigned) records the published 15-minute quiz explanation and differing elementary/calculus question counts. Fifteen minutes is a useful initial default, not a universal historical fact. |
| A 150-XP cadence is supported; its precise counter is not. | The [engine analysis](mathacademy_engine_analysis.md) records the public 150-XP availability statement. The [completed-task CSV](progress.csv) contains both 120 and 181 routine XP between particular consecutive quizzes. Completion gaps do not identify the offer time or counter reset. |

## 1. Eligibility and the three queue modes

**Recommended** means the scheduler thinks the task is useful now. **Self-selected** means the learner requested it. **Required** means a specific assessment or remediation obligation must be resolved. The selection label changes priority, never answer grading, mastery requirements, XP, or FIRe credit. These meanings already fit [learner-queue](../schema/learner/1-4-learner-queue.edn).

For a new lesson, require complete instructional content, sufficient fresh questions, and learned direct prerequisites whose current memory is above the FIRe due threshold. If a selected lesson is not ready, show the small missing prerequisite set and offer its available lessons/reviews. Preserve the selected destination while those prerequisites are completed. Do not mark the destination mastered because the learner selected it.

A self-selected new lesson earns the same XP as a recommended one. Revisiting an already learned topic should normally route to its needed review or remediation. Optional extra practice on a satisfied, not-due topic remains available, but show zero XP before it starts; otherwise repeatedly choosing easy mastered work would manufacture assessment cadence. This is the reward-eligibility rule proposed in [XP](xp-proposal.md), separate from the learner's ability to inspect or practice material.

Check this readiness at task start. Once an attempt starts, a clock crossing a prerequisite's due threshold must not reject an otherwise valid answer halfway through the lesson. Finish that attempt, update evidence, and reconsider readiness for the next task. The current runtime checks readiness during completion, so this is one concrete implementation adjustment.

**Recommended initial meaning of required:** required work comes before starting another ordinary graded task, including a self-selected lesson. The selected lesson stays queued; viewing instructional content remains possible. This preserves the existing meaning of mandatory assessments/remediation, but it is a product tradeoff: if we later want a learner override, it should be an explicit change to this rule, not an accidentally dismissible queue row. Never interrupt an in-progress task to enforce a newly created obligation.

Launching a required task does not satisfy it. An abandoned assessment stays required; a failed required review creates appropriate further support. Recompute the obligation from activity history and current progress instead of parsing `queue/reason`. Only one unresolved obligation per purpose/topic should produce a visible entry.

## 2. Reviews and recommendation order

Retain the engine's FIRe due criterion: a learned topic is due when its decayed memory reaches the configured threshold. Do not add a parallel fixed schedule such as “every topic every seven days.” Review timing follows the learner-topic state and encompassing credit already modeled in [core.py](../engine/fire/core.py).

Build candidates from ready lessons, due topic reviews, useful early reviews that cover due component topics, and eligible authored multisteps. Simulate successful retention updates with the real encompassing graph and slow-learning restrictions. This is a ranking estimate, not actual credit. The existing `FireEngine.rank` already computes due topics removed per expected minute and future due-date gains; these are suitable initial ranking signals.

Use this order:

1. Required remediation and required assessments. When both exist, repair the known weakness first rather than testing it again immediately.
2. Otherwise rank work by **due topics resolved / estimated learner minutes**, then **future retention days gained / minute**. Among equally valuable candidates, favor coverage of the most overdue topics, measured in their own stored decay intervals rather than a universal number of days.
3. When those retention scores tie, favor ready lessons that unlock more currently blocked topics in the selected scope, then favor a different module from the most recent lesson, then use course-map order as a stable tie-breaker.

Ordinary due reviews remain recommendations, even when overdue. Neither the sources nor the goal of self-direction justify a new hard lock based only on inactivity. Failures and assessment cadence create the required obligations. An explicit quiz-error or failed-review remediation requirement needs direct evidence; ordinary implicit credit does not erase it.

Show up to **five** recommendations alongside required work and the selected destination. Avoid showing an ordinary review made redundant by a lesson already offered, but remove it from the due set only after the lesson actually succeeds and the retention calculation clears it. Reserve at least one ready new lesson in the menu when there is no required work. Initially, put a new lesson first after three consecutive routine reviews if one is ready. Five options and this three-review balancing rule are local starting defaults, not recovered MA rules; the learner can still choose a different recommendation or eligible lesson.

Module membership is only a weak tie-breaker for variety, not a newly invented concept-similarity graph. Favoring topics that unlock later work is supported by [chapter 32](<The Math Academy Way/V-TECHNICAL-DEEP-DIVES/32-Technical-Deep-Dive-on-Prioritizing-Core-Topics/32-Technical-Deep-Dive-on-Prioritizing-Core-Topics.md>); it does not justify assigning an unverified permanent “core” label to every topic.

## 3. Lesson and review delivery

Keep **two consecutive correct answers, at most five presented questions per KP** as the initial lesson rule. A skip consumes a presentation and breaks the streak. Pass the lesson only after all required KPs pass. Completion by itself, a positive XP award, or passing one KP does not establish whole-topic mastery. This follows the published adaptive practice structure recorded in the [engine analysis](mathacademy_engine_analysis.md), while remaining a local rule for our implementation.

For reviews, prepare five unseen questions from the topic's KP banks, interleave KPs/cases, and select the first three to cover different cases where possible. Then use **at least three questions, passing when the final two are correct, with a maximum of five**. The fifth question may complete the passing streak. This improves the current three-consecutive rule:

| Observed response sequence | Observed award | Proposed interpretation |
| --- | --- | --- |
| `CCC` | Base + 2 | Pass after three, perfect bonus |
| `ICC` | Base, observed twice | Pass after three following recovery |
| `CCICC` | Base | Pass after five following recovery |
| `CCICI` | Zero | Stop after five, failed retrieval |
| `CCIIC` | Half base | Stop after five, partial work without a passing streak |

These sequences come from [question-level XP observations](mathacademy-xp-observations.json). The result pages do not expose every internal pass flag, so the stopping rule is an inference chosen to fit the evidence, not a universal claim about MA. The [XP proposal](xp-proposal.md) specifies awards separately. Unserved fourth/fifth questions remain available for future work; preparation is not presentation.

If a topic has more cases than five questions can cover, rotate less recently tested KPs across later reviews and assessments. Do not expand every review indefinitely to cover every case. The [practice FAQ](<The Math Academy Way/VI-FREQUENTLY-ASKED-QUESTIONS/FAQ-The-Practice-Experience/FAQ-The-Practice-Experience.md>) explains that reviews mix KPs and assess consistent retrieval.

## 4. Remediation without repeated punishment loops

After one failed lesson, recommend an unrelated ready task before retrying. Use one completed unrelated task or 30 minutes away as the initial retry cooldown; these numbers are our choices. The student's requested destination remains visible.

After two failed attempts that reach the same KP without reaching a later KP, require direct reviews of that KP's `knowledge-point/key-prerequisites`. If a prerequisite has never been learned, offer its lesson instead. If those links are missing, use known direct prerequisites ordered by weakest current retention and explain that the targeting is less precise. Do not manufacture missing graph edges or assign the entire ancestor graph as homework.

After a failed required review, offer the corresponding lesson for relearning. After an ordinary review fails, the same direct support is appropriate; do not send the student through endless fresh five-question reviews without instruction. Retain the observed history and reduced retention rather than treating a single failure as proof the topic was never learned.

After an assessment, require one direct review per incorrectly answered or explicitly skipped topic, deduplicated by topic. A passed review satisfies this requirement. A failed review leads to the topic's lesson; successful relearning satisfies the immediate remediation requirement and restores ordinary spaced scheduling. Questions never presented before a timer expired create neither an incorrect answer nor a topic-specific remediation requirement.

There is no additional assessment-retake state machine. Once remediation is complete, the learner may take a newly assembled assessment through the ordinary assessment path. It uses unseen questions and normal scoring. No passing assessment grade is required to escape an endless retake loop. The source supports reviews after quiz errors; this completion/reset policy is our simpler implementation choice.

If required work lacks usable content, prepare its questions or instruction before making it a blocking queue entry. Keep the unresolved need visible and permit unrelated eligible work while content is unavailable. Repeatedly failing the same relearning lesson invokes its key-prerequisite support, rather than another identical immediate loop. At a foundational topic with no deeper prerequisites, the next action is improved instruction or a narrower worked example and fresh practice; do not pretend that reissuing the same task is remediation. Missing content never silently discharges the learning need.

## 5. Assessment cadence

Initially require an assessment after **150 positive finalized XP from lessons, reviews, and multisteps** since the last completed assessment. Include remedial work and self-selected work because both are practice. Exclude assessment and diagnostic XP; exclude negative awards rather than subtracting them from the counter. Use `max(0, xp-earned)` per finalized practice task. XP is a cadence measure here, not a knowledge score.

When the threshold is crossed, finish the current task and create one assessment obligation. Complete the assessment by finishing every selected question, with explicit skips allowed, or by genuine timer expiry. Initially there is no separate early-submit action. Either completion condition satisfies the obligation **regardless of score** and resets the counter to zero; pausing or abandonment does not. Resetting instead of repeatedly subtracting 150 prevents a series of immediately consecutive tests if assessment delivery was delayed. A voluntarily started fresh assessment uses the same completion/reset rule.

The full selected question set remains the XP denominator, including questions left unfinished at expiry. That does not make unfinished questions incorrect learning evidence: only actual submitted answers update answer accuracy, explicit skips trigger their stated remediation, and unpresented questions establish nothing about knowledge. A broad selected assessment is an opportunity for broad retrieval, not proof that all its topics were actually retrieved before time expired.

The counter is initially derived from existing task types, completion times, and finalized XP; it does not need a second mutable copy of the XP ledger. If early migration lacks enough history, start the counter at zero when local study begins rather than inventing historical eligibility. Imported MA XP stays the observed value.

This exact category/reset policy is a judgment call. The 150-XP public statement does not resolve it, and the completion CSV cannot. It deliberately avoids quiz XP generating more quizzes, penalties postponing needed feedback, and low assessment scores forcing repeated timed tests before remediation.

If the learner does not yet have enough practiced, testable topics or fresh questions for a meaningful quiz, retain the pending threshold and continue eligible learning/content preparation. Do not hard-lock the application on an assessment it cannot assemble. This is a delivery constraint, not permission to reuse seen questions or pretend that unready topics are assessable.

## 6. Assessment assembly

Start with a **900-second time limit** and aim for **12–15 minutes of expected question work**. Choose questions to fit the budget rather than fixing the count at ten. Shorter definitions remain valid; advanced problems may naturally produce fewer questions. Distinct observed counts, including ten versus eight questions on the September 24 pair, make a fixed-count rule poorly supported.

Use the following selection procedure:

1. Start from learned topics across the learner's profile, favoring the currently selected course and its foundations without excluding older knowledge. For initial eligibility, require successful untimed learning or placement, plus later successful retrieval evidence. An explicit review is sufficient; a completed encompassing task is also sufficient when its actual credited coverage is at least 0.5. Require at least 24 hours since first local mastery unless diagnostic placement establishes prior knowledge. The coverage and delay thresholds are conservative local defaults, not MA measurements. Do not treat a speed-adjusted repetition number as a count of distinct learning occasions.
2. Exclude topics still awaiting direct remediation and questions the learner has already seen. A newly completed lesson does not become a timed test question merely because the XP counter crossed 150.
3. Rank topics first by longest time since direct assessment, treating never-assessed eligible topics as first. Within that group favor the selected course, weaker assessment performance, and useful prerequisite coverage. After selecting a topic, lower the remaining priority of topics substantially encompassed by it; do not eliminate all old foundational topics permanently.
4. Choose one question per selected topic, rotating its KP/case rather than always taking the first or easiest example. Mix representations and difficulty while respecting the taught skill. Initially use **50% E, 40% M, 10% H**, approximately the captured mixture, when the available bank supports it; do not require an exact quota on a small quiz. Treat these labels as authored relative difficulty, not a universal time or XP multiplier.
5. Fill the expected-time budget without repeating a topic. Shuffle the completed set for presentation. Save the selected question refs in an ordinary assessment definition; record only the actually presented questions as task items.

As a starting adaptation rule, examine the last 30 submitted assessment answers, once at least 20 exist. If accuracy exceeds 85%, shift ten percentage points from E to M on the next assembly; once E reaches 20%, shift M to H instead, capping H at 30%. Below 80%, reverse one shift, reducing H first. Limit the change to one adjustment per completed assessment and do not remove necessary skill coverage merely to raise the score. The 80–85% target is published; the window, mixture, and step size are our choices. This adapts the assembly policy without overwriting authored question difficulty or confusing it with `topic/difficulty`.

With fewer than five eligible topics, continue normal study instead of repeating topics to manufacture a broad quiz. If a later advanced course has fewer, longer questions that already fill the workload budget, allow that smaller set. This is a breadth preference rather than an inflexible question-count requirement.

## 7. Expected duration

Keep **expected workload**, **learner duration prediction**, and **actual elapsed time** distinct. The [XP analysis](mathacademy-xp-analysis.md#how-base-xp-is-assigned) supports authored timing estimates calibrated by data; the [live inspection](fire-live-account-analysis.md#timing-and-outcome-fields-need-careful-interpretation) shows long elapsed values that may include interruptions. Neither E/M/H nor one person's stopwatch is a population workload calibration.

Use an authored or generator-supplied expected duration when available. For imported activities without one, use `60 × observed base XP` as an explicitly approximate task-level starting estimate. Never use awarded XP, since bonuses and penalties describe performance. For entirely new uncalibrated content, start with a reviewed estimate; shared provisional reference defaults are 12 minutes for a lesson, 6 minutes for a review, or 90 seconds per question. These seed both scheduling estimates and base XP under the [XP proposal](xp-proposal.md), rather than creating conflicting workload estimates. They are explicitly uncalibrated and must not drive answer grading or FIRe speed penalties. Imported base XP remains observed; do not feed its timing fallback back into a recalculated historical award.

For recommendation ranking, adjust the reference task estimate using the learner's last 20 comparable tasks with usable timing. Use the median ratio of actual focused duration to reference duration, shrink it toward 1 with weight `n/(n+10)`, and clamp the result to 0.5–2.0 initially. Do not apply this adjustment to base XP. Do not use old wall-clock spans or obvious idle outliers as focused duration; absent reliable timing, keep the reference estimate.

For lessons, the expected workload includes instruction and adaptive practice, not just two questions per KP. For reviews, it includes the expected early stopping behavior, not always all five prepared questions. For assessments and multisteps, sum the selected questions' reference times plus any substantive scenario reading. The saved assessment expected-seconds and time-limit-seconds remain separate. Broader timing metadata can be added when the generator/grading interface is reviewed; this proposal does not add speculative schema fields.

## 8. Fresh questions and content supply

Enforce our chosen **no previously presented question** policy across lessons, reviews, assessments, diagnostics, and multisteps. MA demonstrably repeats some diagnostic IDs; our guarantee is an intentional product choice rather than a claim about their implementation.

Determine seen questions through `learner/activity → learner-task/items → task-item/content`. Count presentations even if skipped, unfinished, or abandoned. Query candidate questions and atomically reserve the selected presentation against the same database basis before displaying it; a concurrent conflict triggers a fresh selection. This follows EDB's [one-direction relationship and consistent-database guidance](../../EDB/docs/02_core_concepts/05_best_practices.md). It needs no `question/seen-by` mirror.

Allow only one active graded attempt per learner, including a paused attempt that can be resumed. Revalidate prepared content before launch, refilling any stale question selections then. If a definition has already been used by an earlier task, create a fresh definition instead of rewriting its question refs. Once an assessment begins, freeze its selected set, expected workload, and XP baseline; do not change its denominator or swap questions midway. Reserve each actual presentation atomically before display. The one-active-attempt rule prevents a second task from consuming a prepared question during the first attempt.

Prepare enough supply before beginning: up to five unseen questions per lesson KP, five per review, and the whole assessment set. Preparing refs does not mark them seen. When supply is exhausted, invoke the KP's configured generator or explain that new content is being prepared; do not silently recycle a question or grant mastery. Generated questions receive ordinary persistent question identities and bank membership after validation. Identical content with a newly minted UUID is not meaningful novelty; generation should reject exact equivalent instances, allowing superficial formatting differences.

## 9. How this fits the current application

The schemas already separate reusable content, learner attempts, question presentations, current progress, and the current queue. They can express the proposed selected activities and resulting evidence without duplicating topic/course links on every record. Scheduling reasons remain display text; eligibility and obligations are derived by application rules.

The existing runtime already contains adaptive lesson/review delivery, per-answer updates, task completion, and FIRe transitions. The existing ranker is a useful compression primitive, not the complete scheduler described here. Work still needed includes candidate construction, the required-work rules, assessment assembly, robust timing estimates, and atomic cross-task question reservation. The review stopping change and start-time prerequisite check are explicit differences from current code.

Keep scheduling constants in a small application policy initially. They are different from the mathematical FIRe parameters in `engine/1-fire-policy.edn`; if editable scheduling settings need persistent history, add that focused configuration later rather than treating every decision as a new content attribute. The proposals do not require a new engine-update event table.

Seed a normal **Custom** or **Self-Directed** course alongside the MA catalog when the database is populated. It can supply initial recommendation context without a new activity type or separate learner profile. Broader concurrent study scope remains a later application decision. Retention already belongs to the global learner-topic profile, so studying the same topic in another course does not restart it.

For diagnostics, use the accepted retry's result in place of the original answer for frontier estimation, while retaining both presentations in history. That is the user's settled rule, not an open scheduling choice. It does not justify replacing assessment results or awarding the same task twice.
