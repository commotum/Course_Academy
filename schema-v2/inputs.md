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

Directs the engine to prepare that lesson, while still checking prerequisites and handling its completion normally.

For our flexible scheduler, available study time, priorities, and assignment deadlines can also influence selection. Those are planned extensions; the current FIRe core does not use them.

Then, after you do the work, the engine needs new evidence:

Which learner, activity, question, knowledge point, and topic were involved.
What you submitted and whether it was correct.
When it happened and how much active solving time you used.
Whether you used hints or revealed the answer.
Whether the work was lesson practice, review, assessment, or diagnostic.
Whether you successfully completed the lesson or review.

The grading and completion rules turn that evidence into topic-level success or failure. FIRe uses it to update retention and accuracy; the scheduler uses the updated state for its next decision. Several answers may support one review result—we wouldn’t award a full repetition for every question.

The current FIRe core already uses time, learner progress, accuracy, topic difficulty, encompassing weights, and graded results. Its ranker also requires estimated duration. Prerequisite eligibility, question selection, study scope, and the full lesson/review/test scheduling rules still need application code.

Schema-wise, the clearest missing inputs are therefore structured question attempts, activity records, and your study scope. The retention and encompassing attributes already exist in the prototype, but need a simpler home.