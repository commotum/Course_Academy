## Current time

Determines how much memory has decayed and which reviews are due.

## Your progress in each topic

Shows what you’ve learned, what you’re ready to learn, and what needs review. Includes retention state and accuracy.

## Your overall accuracy and topic difficulty

Calibrates how quickly your retention advances through successful practice.

## Topic prerequisites

Determines which new lessons are eligible.

## Encompassing relationships and their weights

Determines whether practicing one topic can satisfy review needs in several others.

## Your previous question attempts

Helps select questions, avoid excessive repetition, identify weak knowledge points, and target remediation.

## Available activities and their estimated durations

Lets the engine compare the benefit of different lessons or reviews relative to the time they take.

## Your selected courses/topics

Defines the material the scheduler should consider—for example, all three courses you’re taking.

## An explicitly selected lesson

Directs the engine to prepare that lesson, while still checking prerequisites and handling its completion normally. `learner/queue` records the selected content, its position, selection mode, and why it is next. `self-selected` means the learner chose it, `recommended` means the engine suggested it, and `required` means engine policy makes it mandatory. All three use the same grading rules. An optional queue course ref records the motivating course. Failure counts and earned-XP thresholds for required work are application policy decisions.

For our flexible scheduler, available study time, priorities, and assignment deadlines can also influence selection. Those are planned extensions; the current FIRe core does not use them.

Then, after you do the work, the engine needs new evidence:

Which learner, task, activity definition, question, knowledge point, and topic were involved.
What you submitted and whether it was correct.
When it happened and how much active solving time you used.
Whether you used hints or revealed the answer.
Whether the work was lesson practice, review, assessment, or diagnostic.
Whether you successfully completed the lesson or review.

The grading and completion rules turn that evidence into topic-level success or failure. FIRe uses it to update retention and accuracy; the scheduler uses the updated state for its next decision. Several answers may support one review result—we wouldn’t award a full repetition for every question.

The current FIRe core already uses time, learner progress, accuracy, topic difficulty, encompassing weights, and graded results. Its ranker also requires estimated duration. Prerequisite eligibility, question selection, study scope, and the full lesson/review/test scheduling rules still need application code.

The schema now has task attempt records in `learner/2-1-learner-task.edn`, individual presentation records in `learner/2-2-learner-task-item.edn`, and response details in `proposed/submission.edn` and `proposed/submitted-answer.edn`, which remain draft models. `learner/2-3-learner-task-performance.edn` holds the topic-specific graded input to FIRe; one task may yield several results. Its existing `fire-event/*` contract is unchanged. `learner/1-4-learner-queue.edn` records current up-next choices through `queue/activity`. Activity category and intended topic scope come from the shared definition referenced by `learner-task/activity`; task-item records hold the topics actually observed. Their optional `source-step` links preserve the connection to authored lesson or multistep placements. `learner/knowledge-profile` owns the existing retention and accuracy records.

Study scope, priorities, available time, and deadlines still need models where they are required. The scheduler and activity controller must turn these inputs into decisions, record measurements, and update progress. Optional queue entries can be dismissed; required work cannot be dismissed to clear its obligation. Launching a task can remove its queue entry but does not satisfy a requirement: the controller must carry or recompute the obligation until the policy completion condition is met, requeuing failed or abandoned work when necessary. The selection enum does not enforce this behavior. Queue entries do not provide a permanent explanation of past scheduling decisions; a durable decision history is not modeled yet.
