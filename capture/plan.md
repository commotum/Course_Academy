# Capture rebuild

Design a fresh capture system with small, clearly separated modules. Use the existing script and saved captures to understand Math Academy and preserve useful evidence. Existing behavior is not automatically a requirement for the new build.

We will work through the stages in order. For each stage, propose a simple design, discuss it with Jake, record the decisions here, and draw its flow chart. Settle how the stages fit together before replacing the running system.

**Queue Processing and the Activity Selection priority order are agreed.** The priority-score calculation remains to be defined. The later sections below are starting proposals, not agreed specifications.

## What we have agreed

- Build fresh rather than continue adding exceptions to the old script.
- Give each stage a clear job and a defined record to pass to the next stage.
- Queue Processing handles the activity queue only. Course summaries, the completed-activity list, and XP tracking belong to Post-Activity Processing.
- Activity Capture includes doing the activity and reviewing its activity history page afterward. Each activity type has its own capture path.
- Post-Activity Processing contains the general actions shared by all activity types and has its own separate stage.
- Never defer or abandon an activity for any reason. Recover and continue until it is complete. After an external interruption or manual stop, resume that activity when operation resumes. Ambiguous questions, uncertain answers, and difficult imports must not cause the script or agent to move on from an unfinished activity.
- Define a completion behavior for each activity type, including what to do when an answer is uncertain. Decide those behaviors during the relevant stage interview.
- Save enough progress to continue after an external interruption or manual stop. After an interruption, check what Math Academy already accepted before repeating an action.
- Resolve source-content gaps during Activity Capture's final history and lesson-page review. Database Preparation receives checked source content and handles database mapping and transaction construction.
- Diagnostic behavior uses course membership and shortest prerequisite distance, with the answer probabilities and timing recorded in `v2/3-Activity-Capture.md`.
- Keep **Activity Capture** in one design file with the shared process followed by each activity type. Draw Post-Activity Processing separately.
- Keep the writing and charts understandable without reading the code.
- Use engineering judgment for routine reliability and implementation choices. Ask Jake only when something is genuinely ambiguous; do not turn ordinary error handling into an interview question.

The existing source rules still apply: preserve Math Academy's original content, including its errors. Keep our corrections separate and apply them later under the appropriate source. A guess submitted to finish an activity does not by itself establish a correct answer for the database.

## Shared foundations — proposed

**One way to work with Math Academy.** A shared browser module reads pages and performs actions such as opening an activity, filling an answer field, submitting, and continuing. It returns the same kinds of records to every activity module. Page selectors, HTML parsing, and browser details live here.

**One capture record.** Use a consistent record for original page evidence, questions, answer fields, submissions, grades, worked solutions, images, lesson structure, and completion. Keep source observations distinguishable from the agent's reasoning and conclusions.

**One way to save and resume progress.** Every activity uses the same mechanism to save its position and record actions before submitting them. Recoverable browser or process failures trigger recovery. An unavailable site or connection leaves the activity waiting to continue, with its progress intact.

**Shared tools, separate activity rules.** Reuse answer-field handling, image collection, page reading, and saved progress. Each activity type specifies its own sequence and answer policy. Avoid one large function containing every activity's exceptions.

The shared process and activity-specific behavior are described in `v2/3-Activity-Capture.md`, including navigation, answer/skip policy, submission timing, and history-page review.

**Python controls the workflow and detects exceptions.** It reads and validates captures, applies policies, performs browser actions, matches known database identities, and builds and submits transactions. It calls agents for mathematical answers, interpretation of source evidence, or ambiguous database identity matches. Each call includes the specific question or detected exception and relevant evidence; the agent returns a structured result that Python checks before acting. Database Commit is entirely scripted.

**One way to read and write the database.** Selection and preparation receive the database information they need through a shared interface. Transaction/Commit owns database writes. Keep account login, queue state, and activity progress separate for each account while sharing the content database and image library.

These are proposed boundaries. Choose implementation details as the stage discussions reveal what is needed.

## 1. Queue Processing

**Job:** produce a reliable record of what the account's queue page shows.

Agreed actions:

- Read the activities in their displayed order, keeping Math Academy's identifiers and wording.
- Default to expanding every activity in the queue, collecting its links, and recording any details.
- Record each activity's type, title, links, progress, and available details, including assessment question counts, time limits, requirements, and retake labels.
- Preserve unexpected cards or missing fields as observations so later stages can respond to them.
- Recover from read errors where possible and continue with the usable queue details.
- Save the extracted queue details in their displayed order alongside the queue's HTML. Activity Selection uses that record to decide what to do.

Agreed scope: the activity queue only. The course summary, completed-activity list, and XP calculations move to the shared Post-Activity Processing stage.

Agreed card handling: default to expanding every activity shown in the queue, collecting its links, and recording any details. Jake noted that the cards previously left closed do not contain additional details and does not expect locked activities to appear in the queue. No separate locked-activity handling is planned.

Agreed evidence: save the queue's HTML alongside the extracted details so a bad read can be reviewed from the saved page.

Queue reading must be fault tolerant and continue. Routine retry and recovery details are implementation decisions; an unreadable card must not prevent processing the rest of the queue.

## 2. Activity Selection / Priorities

**Job:** choose an activity and explain why it serves our capture goals.

Agreed form: prioritize the five base activity types—Lesson, Review, Assessment, Multistep, and Diagnostic—in either started (begun but not completed) or unstarted form. Rank Lessons and Reviews together by priority score within each status group. This gives eight priority levels covering the same ten type/status combinations. Choose the first available level, then the highest-scoring Lesson or Review within that level.

Use the queue record, desired content, existing captured content, and the account's Math Academy progress. Pass the selected activity and its reason to Activity Capture, which applies the activity's answer and completion policy.

The agreed order is listed in `v2/2-activity-selection.md`: started Assessment, Diagnostic, Lesson/Review by score, Multistep; then unstarted Diagnostic, Lesson/Review by score, Multistep, Assessment. Started activities come before unstarted ones. Comparing scores happens when choosing or resuming an activity; changing scores must not interrupt the activity currently being captured. Use queue order for equal scores or when none are available. An assessment offered alone will still be selected even though unstarted assessments rank last.

This replaces the earlier draft's mixture of activity types, requirements, repeats, and capture goals. The priority-score calculation remains to be defined.

Jake expects a required assessment to be the only displayed queue option. Treat that as an observation to verify when needed, rather than a separate priority category.

Discuss capture goals, what counts as captured, missing lessons versus additional practice questions, required assessments, repeats, and coordination between accounts. Work out how selection and diagnostic behavior cooperate to make wanted lessons available. Do not carry forward the old priority formula or fixed diagnostic topic lists without deciding that they fit.

## 3. Activity Capture

**Job:** do the activity and then review its activity history page to capture its content and results.

Activity Capture covers both parts:

1. **Do the activity.** Carry it through to Math Academy's completion state, saving the original content and evidence from each interaction.
2. **Review the activity history page.** Collect the recorded questions, results, grades, and worked solutions, and connect them to the evidence saved while doing the activity.

Together, these form Activity Capture. Before handing off to Post-Activity Processing, Python checks source completeness and fetches missing evidence. It calls the activity's agent when the evidence needs interpretation, including ambiguous answer evidence, and checks the returned result. Lessons also receive the full topic-page review. Recovery does not change the fact that Math Academy already completed the activity.

Use [3-Activity-Capture.md](v2/3-Activity-Capture.md) as the single design document: shared activity/step and question processes, followed by Lesson, Review, Assessment, Diagnostic, and Multistep.

Assessment question counts and time limits belong to Queue Processing. Activity Capture uses those values and observes the current time remaining during a timed activity.

New and failed lessons are paths within Lesson capture. Resuming an interrupted activity continues that activity; it is not another activity type.

Python applies the answer and completion policies recorded for each type. During an activity it preserves uncertainty and continues; during the final source review it resolves missing or conflicting evidence before the capture is handed off. An unavailable source value stays an explicit limitation rather than an invented fact.

## 4. Post-Activity Processing

**Job:** perform the account-level work that follows any completed activity, once, through shared Python code. See [4-post-activity-processing.md](v2/4-post-activity-processing.md).

This stage owns the course summary, completed-activity list, and XP tracking. The starting proposal also includes saving updated topic progress, comparing it with the previous observation, and recording that the activity has completed. Keep these observations available for later use without automatically treating them as learner facts in EDB.

Discuss exactly which pages to read, when to collect these observations, and how to recover missing observations. Also decide what account information must be collected at startup, before the first activity has finished. A delay here must not cause the system to repeat an already completed activity.

The shared stage has its own chart, `4-post-activity-processing.dots`. Activity Capture hands off to it after collecting the activity's content and history.

## 5. Database Preparation

**Job:** use Python to turn checked captures into prepared transactions. See [5-database-prep.md](v2/5-database-prep.md).

Reconcile questions, answer fields, solutions, tutorials, knowledge points, lesson steps, and multistep structure with the existing database. Python matches known identities and detects conflicting or ambiguous mappings. Only those cases go to an agent with the candidate entities and source evidence; Python checks the proposed resolution before building EDN. Preserve existing identities for confirmed source revisions. A newly discovered source-content gap returns to Activity Capture's source review.

Python converts content, stores images using the existing SHA-256 layout under `/media/jake/SSD/EDB/math/images`, builds references and schema relationships, and calculates the topic workload multiplier from the checked lesson inputs. It produces reviewable EDN with separate source attribution for original and derived facts, and validates complete batches. Incomplete or unresolved cases remain explicit; independent complete changes can proceed.

## 6. Database Transaction / Commit

**Job:** use Python to preview, commit, and verify prepared transactions against `/media/jake/SSD/EDB/math`. See [6-database-commit.md](v2/6-database-commit.md).

Content interpretation stays in Activity Capture; database identity decisions stay in Preparation. Python checks the prepared changes, submits them with the agreed source, records the receipt, and verifies the database result. It handles exact retries and classifies rejected or unknown outcomes. If a write times out, establish whether it committed before sending a different transaction.

Discuss batch size, automatic versus reviewed commits, concurrent accounts, retry behavior, and what verification is enough to call an import complete.

## Design files and build sequence

- `v1/` holds the charts describing the old system.
- `v2/` holds the six stage documents, from `1-queue-processing.md` through `6-database-commit.md`.
- Keep one Activity Capture document with the shared process and activity-specific sections. Add charts as the design is settled, with separate Post-Activity Processing, preparation, and commit charts.
- Update this plan as decisions are made. Keep unanswered questions visible rather than filling them with assumptions.
- After the designs fit together, agree on the implementation sequence and checks using saved captures. Test completion and recovery before switching live accounts to the replacement.

No implementation changes are authorized by this planning step. Keep the existing capture system running while we design its replacement.
