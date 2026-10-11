# Capture rebuild

Design a fresh capture system with small, clearly separated modules. Use the existing script and saved captures to understand Math Academy and preserve useful evidence. Existing behavior is not automatically a requirement for the new build.

We will work through the stages in order. For each stage, propose a simple design, discuss it with Jake, record the decisions here, and draw its flow chart. Settle how the stages fit together before replacing the running system.

**1. Queue Processing is agreed at the stage level.** Next: Activity Selection / Priorities. The later sections below are starting proposals, not agreed specifications.

## What we have agreed

- Build fresh rather than continue adding exceptions to the old script.
- Give each stage a clear job and a defined record to pass to the next stage.
- Queue Processing handles the activity queue only. Course summaries, the completed-activity list, and XP tracking belong to Post-Activity Processing.
- Activity Capture includes doing the activity and reviewing its activity history page afterward. Each activity type has its own capture path.
- Post-Activity Processing contains the general actions shared by all activity types and has its own separate stage.
- Once an activity starts, keep working toward its completion. Ambiguous questions, uncertain answers, or content that is difficult to import must not cause the script or agent to abandon it.
- Define a completion behavior for each activity type, including what to do when an answer is uncertain. Decide those behaviors during the relevant stage interview.
- Save enough progress to continue after an external interruption or manual stop. After an interruption, check what Math Academy already accepted before repeating an action.
- Put content recovery in Database Preparation. Finishing an activity and having its content ready for the database are separate milestones.
- Diagnostic behavior must take account of lessons already captured and lessons we want to capture. Define what “captured” means before using it in that policy.
- Give each activity type one **Activity Capture** design file covering the activity itself and its history-page review. Draw Post-Activity Processing separately.
- Keep the writing and charts understandable without reading the code.
- Use engineering judgment for routine reliability and implementation choices. Ask Jake about choices that affect capture goals, content, source attribution, or intended behavior; do not turn ordinary error handling into an interview question.

The existing source rules still apply: preserve Math Academy's original content, including its errors. Keep our corrections separate and apply them later under the appropriate source. A guess submitted to finish an activity does not by itself establish a correct answer for the database.

## Shared foundations — proposed

**One way to work with Math Academy.** A shared browser module reads pages and performs actions such as opening an activity, filling an answer field, submitting, and continuing. It returns the same kinds of records to every activity module. Page selectors, HTML parsing, and browser details live here.

**One capture record.** Use a consistent record for original page evidence, questions, answer fields, submissions, grades, worked solutions, images, lesson structure, and completion. Keep source observations distinguishable from the agent's reasoning and conclusions.

**One way to save and resume progress.** Every activity uses the same mechanism to save its position and record actions before submitting them. Recoverable browser or process failures trigger recovery. An unavailable site or connection leaves the activity waiting to continue, with its progress intact.

**Shared tools, separate activity rules.** Reuse answer-field handling, image collection, page reading, and saved progress. Each activity type specifies its own sequence and answer policy. Avoid one large function containing every activity's exceptions.

**One way to read and write the database.** Selection and preparation receive the database information they need through a shared interface. Transaction/Commit owns database writes. Keep account login, queue state, and activity progress separate for each account while sharing the content database and image library.

These are proposed boundaries. Choose implementation details as the stage discussions reveal what is needed.

## 1. Queue Processing

**Job:** produce a reliable record of what the account's queue page shows.

Agreed actions:

- Read the activities in their displayed order, keeping Math Academy's identifiers and wording.
- Default to expanding every activity in the queue, collecting its links, and recording any details.
- Record each activity's type, title, links, progress, and available details, including assessment requirements and retake labels.
- Preserve unexpected cards or missing fields as observations so later stages can respond to them.
- Recover from read errors where possible and continue with the usable queue details.
- Save the extracted queue details in their displayed order alongside the queue's HTML. Activity Selection uses that record to decide what to do.

Agreed scope: the activity queue only. The course summary, completed-activity list, and XP calculations move to the shared Post-Activity Processing stage.

Agreed card handling: default to expanding every activity shown in the queue, collecting its links, and recording any details. Jake noted that the cards previously left closed do not contain additional details and does not expect locked activities to appear in the queue. No separate locked-activity handling is planned.

Agreed evidence: save the queue's HTML alongside the extracted details so a bad read can be reviewed from the saved page.

Queue reading must be fault tolerant and continue. Routine retry and recovery details are implementation decisions; an unreadable card must not prevent processing the rest of the queue.

## 2. Activity Selection / Priorities

**Job:** choose an activity and explain why it serves our capture goals.

Use the queue record, desired content, existing captured content, and the account's Math Academy progress. Produce an activity plan containing the choice, its reason, and the answer/completion policy Activity Capture should follow.

Discuss capture goals, what counts as captured, missing lessons versus additional practice questions, required assessments, repeats, and coordination between accounts. Work out how selection and diagnostic behavior cooperate to make wanted lessons available. Do not carry forward the old priority formula or fixed diagnostic topic lists without deciding that they fit.

## 3. Activity Capture

**Job:** do the activity and then review its activity history page to capture its content and results.

Each activity's chart covers both parts:

1. **Do the activity.** Carry it through to Math Academy's completion state, saving the original content and evidence from each interaction.
2. **Review the activity history page.** Collect the recorded questions, results, grades, and worked solutions, and connect them to the evidence saved while doing the activity.

Together, these form Activity Capture. Each activity type then hands off to the shared Post-Activity Processing stage. Missing evidence becomes recovery work without changing the fact that the activity finished. Discuss any additional source pages, such as the full lesson page, when designing that activity's capture path.

Prepare a separate chart and interview for each path:

| Path | Main questions to settle |
|---|---|
| New Lesson | Which tutorials and examples must be visited? How should practice be answered? How do we obtain the complete lesson and its step order? |
| Failed Lesson | What changes when repeating a failed lesson? How do we link the repeat to earlier evidence and capture anything previously missed? |
| Review | How do we answer, collect more reusable questions, and retain their knowledge-point associations? |
| Assessment | How do we fill and submit the whole test, handle its time limit, and collect feedback afterward? Include quiz retakes here. |
| Multistep | How do we preserve shared context, each question, dependencies between parts, and their order? |
| Diagnostic | Which skills should we demonstrate or skip to reach the lessons we want? How do existing captures and missing lessons determine that behavior? |

Proposal: New Lesson and Failed Lesson get separate charts and policies but share lesson-handling code. Resuming an interrupted activity continues that activity; it is not another activity type.

For every path, explicitly agree on what happens when the agent is uncertain, a field behaves unexpectedly, submission feedback is unclear, or the browser loses its place. The goal remains completion. Do not silently reuse the old intentional-correct/incorrect sequences.

## 4. Post-Activity Processing

**Job:** perform the account-level work that follows any completed activity, once, through one shared module.

This stage owns the course summary, completed-activity list, and XP tracking. The starting proposal also includes saving updated topic progress, comparing it with the previous observation, and recording that the activity has completed. Keep these observations available for later use without automatically treating them as learner facts in EDB.

Discuss exactly which pages to read, when to collect these observations, and how to recover missing observations. Also decide what account information must be collected at startup, before the first activity has finished. A delay here must not cause the system to repeat an already completed activity.

The shared stage has its own chart, `4-post-activity-processing.dots`. Individual activity charts reference it rather than repeat its steps.

## 5. Database Preparation

**Job:** turn saved captures into complete, source-supported content and prepared transactions.

Resolve missing or ambiguous content here using saved evidence and, when needed, additional source reads. Reconcile questions, answer fields, solutions, tutorials, knowledge points, lesson steps, and multistep structure with the existing database. Preserve existing entity identities when the source content has changed.

Store images using the existing SHA-256 layout under `/media/jake/SSD/EDB/math/images`, and produce references that use that library. Produce reviewable EDN, with source attribution and a clear account of any recovery still needed.

Discuss what recovery can run automatically, how to confirm answers from worked solutions, how to handle conflicting captures, and whether a small unresolved part should hold an entire batch. Keep unresolved evidence available for another recovery attempt.

## 6. Database Transaction / Commit

**Job:** preview, commit, and verify prepared transactions against `/media/jake/SSD/EDB/math`.

Keep content interpretation and mathematical reasoning in preparation. This stage checks the prepared changes, submits them with the agreed source, records the receipt, and verifies the database result. If a write times out, establish whether it committed before sending a different transaction.

Discuss batch size, automatic versus reviewed commits, concurrent accounts, retry behavior, and what verification is enough to call an import complete.

## Design files and build sequence

- `v1/` holds the charts describing the old system.
- `v2/` will hold the agreed designs for the replacement. Start with `1-queue-processing.dots`, then `2-activity-selection.dots`.
- Add six Activity Capture charts, each covering doing the activity and reviewing its history page. Add a separate Post-Activity Processing chart for the general actions shared by all activities, followed by preparation and commit charts.
- Update this plan as decisions are made. Keep unanswered questions visible rather than filling them with assumptions.
- After the designs fit together, agree on the implementation sequence and checks using saved captures. Test completion and recovery before switching live accounts to the replacement.

No implementation changes are authorized by this planning step. Keep the existing capture system running while we design its replacement.
