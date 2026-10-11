# 3. Activity Capture

Complete the selected activity, then review its history page to finish the capture. The shared process handles content; each activity type sets the answer policy, submission timing, and completion rules.

**Python controls the process:** page navigation, extraction, images, answer policies, timing, response entry, and completeness checks. It calls the math-solving sub-agent for answers and source interpretation. When checks find missing or conflicting evidence, Python requests a focused agent review, performs any additional page reads, and checks the returned result. The agent returns answers and evidence; Python records and acts on them.

## 3.1. Shared Process

Our schema separates the activity's structure from the content it presents:

| Record | What it contains |
|---|---|
| Activity | Title, type, scope, time limit, and steps. |
| Step | A content reference and its place in an activity or multistep. The owner's first-step and `step/next` define linear order. |
| Tutorial | A title and instructional content, including equations and images. |
| Knowledge Point | A canonical example and a pool of practice questions. A lesson step can present the knowledge point and expand into both. |
| Question | Problem, calculator requirement, answer fields, worked solution, and observed difficulty. Canonical examples are also questions. |
| Answer Field → Answer | The field's type and location, its answer choices, and a reference to its correct answer. |
| Multistep | Shared context and its own ordered steps. |

### Activity and steps

1. Open or resume the activity using its queue details. Save instructions, task ID, title, and topic/course references before starting when possible. Read instructions before starting a timed activity; use the queue's question count/time limit and monitor the live timer.
2. Follow Math Academy's steps. Record each step's title/type, content ID, verified placement ID when available, and position. Save its HTML, screenshot, and original images, including source URLs and where images appear.
3. Capture the content identified in the table above. Expand knowledge points into their example and practice, and multisteps into their shared context and parts. Use the question process below whenever a response is required.
4. Save responses and feedback before advancing. Continue until Math Academy ends the activity, recording success, failure, or timeout as the actual outcome.
5. Open its history page and expand every question. Match source IDs and positions to the live capture. Add difficulty, topic/knowledge-point/example references, final grades, revealed correct answers, and worked solutions, preserving the history HTML, screenshots, and images.
6. Before leaving Activity Capture, Python checks the live questions against history, including repeated presentations, and checks answer fields, correct-answer evidence, source identities, images, and activity structure. It fetches missing source material immediately. If the evidence needs interpretation, it gives the same sub-agent the specific gap or conflict and relevant captures, then checks the proposed resolution. Include the full lesson-page review described below when applicable.
7. Finish the source review and save a checked capture before handing it to Post-Activity Processing. Every question has an agent's final answer judgment and supporting evidence, including a reasoned finding of source error, genuine ambiguity, or unavailable evidence. Missing optional values are recorded as absent. No question waits for Jake or a later judgment queue. Learner responses, timing, and solver reasoning remain evidence for later.

Keep task, content, and placement IDs separate. Questions use `q-N`; canonical examples use `e-N`. Screen labels such as `step-qN` are not verified placement IDs. Keep observed attempt order distinct from reusable activity structure; preserve evidence of the route actually taken.

Never quit, defer, or abandon an unfinished activity because of an error or uncertain answer. Completing it lets Math Academy expose more work. Recover and continue; after an external interruption or manual stop, resume saved progress and check what Math Academy already accepted before repeating an action.

Finish the activity and its question judgments as one unit of work. Math Academy completing an activity and us finishing its capture are separate events. Resolve source ambiguities during the final history/lesson-page review. Decide disagreements now and preserve both Math Academy's stated answer and the agent's conclusion with their evidence. A final finding that evidence is unavailable closes the judgment without inventing an answer or repeating the activity.

### Questions

1. Before answering, save the problem, calculator instructions, question ID when visible, HTML, screenshot, and images. Record each answer field's type, location, choices, and displayed order.
2. Launch one competent math-solving sub-agent for the first question and save its session ID. Resume that same conversation throughout the activity, including across knowledge points. Send each new question's fields, current choices, screenshot, and images, plus new examples, shared context, solutions, and grades. Earlier questions and reasoning remain in the conversation. Python restarts or replaces an unavailable or repeatedly inconclusive agent using the saved evidence.
3. When answering, request the correct answer for each field, reasoning, and confidence; save these separately from Math Academy's content. Apply the activity's answer policy to choose the actual response and preserve that decision on resume.
4. Enter and verify the field values or selected choices. Submit when the activity calls for it. Record actual responses, skips, retries, and timing. Check current choices again after a reload or shuffle.
5. Save each revealed grade, correct answer, worked solution, HTML, and image. Capture and answer any additional fields revealed within the same question before advancing.
6. Give feedback to the same sub-agent to check its answer. Resolve disagreements within the activity and record its conclusion separately from Math Academy's answer. A submission alone does not establish the correct answer.
7. During history review, Python records difficulty and checks the complete question record. It sends ambiguous answer evidence to the sub-agent for a final judgment before ending capture. If another competent agent is needed, Python requests that review now.

**C** means intended correct; **W** means intentionally incorrect. The sub-agent solves for the correct answer in both cases. Record intended responses separately from actual grades. The sequences and probabilities below are defaults: completion takes precedence when a disagreement, ambiguous question, timer, or unexpected behavior requires a different response. Save the planned response, actual response, and reason for deviation. Continue the sequence at its next position rather than restarting it.

### Default actions when something goes wrong

| Situation | Default action |
|---|---|
| The solver is uncertain, fails, or stops responding | Python requests focused reconsideration or replaces it using saved evidence. During a timed activity, submit the best available valid response before the deadline; finish the agent's judgment during history review. |
| A question is genuinely ambiguous or unanswerable | The agent chooses the best supported valid response, or an offered Don't Know/skip when no answer is defensible. If skipping is unavailable, submit its best attempt. Record the uncertainty and continue. |
| The agent disagrees with Math Academy | Check the mathematics and source evidence now. Use the response needed to advance, including Math Academy's expected response when required. Preserve both conclusions and override the planned C/W response when necessary. |
| A field, page, or submission behaves unexpectedly | Save the current evidence, reread the page, and check what was accepted. Python requests a focused agent interpretation when needed, then retries the appropriate action on the same activity. |
| Source content or images cannot be recovered | Try the saved evidence and available source pages. The agent makes a final finding of what is supported and what is unavailable; preserve that finding and continue without inventing content. |
| The site or connection is unavailable | Save progress and retry automatically with backoff. Resume the same activity when access returns; do not abandon it or ask Jake to resolve its questions. |

Each recovery attempt must obtain new evidence, change the attempted action, or wait for an unavailable dependency. Repeating the same unsuccessful reasoning indefinitely is not progress. A final finding of ambiguity or missing evidence is recorded for this capture; new evidence in a future capture can revise it.

## 3.2. Lesson

A lesson teaches one topic through tutorials and knowledge points. Each knowledge point has a canonical example followed by adaptive practice questions.

**Answer policy:** Independently choose `CWCWC` with 70% probability or `WCWCC` with 30% probability for each knowledge point. Keep that choice on resume. After those five questions, answer any additional questions correctly until Math Academy advances. A retake following a negative-XP completion uses all-correct answers throughout.

1. Capture each tutorial's title, body, images, and source ID. Capture each canonical example's title, problem, worked solution, images, and `e-N` ID, and pass it to the sub-agent before the associated practice.
2. Capture and answer the practice questions, retaining their knowledge-point association and every revealed result. Follow Math Academy's completion state even when it serves fewer questions or ends the lesson unsuccessfully.
3. At completion, save Math Academy's displayed base-XP denominator and its source evidence: for “8 of 13 XP,” save 13 as the base. Preserve the first two distinct practice questions per knowledge point in presentation order, with their problems, answer fields, and worked solutions completed from history.
4. After history review, capture `/topics/<topic-id>` for the complete lesson: tutorial and example content, verified placement/content IDs, titles, and order, including sections this attempt did not visit. Database Preparation compares that definition with the existing lesson and preserves existing identities when updating it.

Lesson steps point to tutorials and knowledge points. Served practice questions join the knowledge point's pool, rather than becoming permanent lesson steps. Failed lessons and retakes share the definition but retain separate attempt evidence.

**Topic difficulty:** Python checks these inputs during the final lesson review and recovers missing source content here. Database Preparation then applies the [existing workload formula](../../reference/xp-docs/expected-distribution-base-xp.md): expected 1.6 difficulty weighting on per-KP solution measurements, followed by `topic/difficulty = observed base XP / unrounded workload score`, including the seven-XP minimum handling. Save the inputs and formula version with this derived value. An incomplete lesson does not produce a calibrated multiplier.

## 3.3. Review

A review serves practice questions from a topic's knowledge points, usually without presenting their canonical examples first.

**Answer policy:** Choose `CWCWC` with 70% probability or `WCWCC` with 30% probability once for the whole review. Continue the sequence across knowledge points and repeat it if Math Academy serves more than five questions. A retake following a negative-XP completion uses all-correct answers.

1. Capture each question before answering, then save its grade and worked solution before continuing. Preserve any instructional content Math Academy does show.
2. Continue until Math Academy completes the review. Save the actual question order and outcome.
3. Use history to confirm each question's topic, knowledge point, difficulty, and answer evidence. Keep the served order as attempt evidence; it does not define a fixed question sequence for every review.

## 3.4. Assessment

An assessment presents a fixed set of questions under a time limit. It may span several topics. The whole assessment is submitted together, so question grades and worked solutions arrive afterward.

**Answer policy:** Independently choose C with **87.17%** probability or W with **12.83%** probability per question, including retakes. Save the draw and response before entry. For W, use a different choice or an incorrect entered value; make only one field wrong. The probabilities do not guarantee a final score.

1. Save the instructions before starting. Use the question count and time limit already recorded by Queue Processing, and track the remaining time during the activity.
2. Capture and fill every question using the shared process. Save the entered answers before submitting the whole assessment. As time runs short, use the best available responses and submit before the timer expires.
3. Confirm completion, then expand every history question to collect grades, worked solutions, correct-answer evidence, difficulty, and topic/knowledge-point references. Preserve timeout or unanswered questions if they occur.

## 3.5. Diagnostic

A diagnostic adapts to answers and skips to determine placement. It has an observed path rather than a fixed question list known in advance.

### Before starting

1. Read and save the course's complete topic list, with IDs and titles, through `course/units → unit/modules → module/topics`.
2. Read the prerequisite graph. For each prerequisite topic, find the shortest directed path to any topic in the course. `topic/next` points from a prerequisite to the topic that requires it: one edge means a direct prerequisite.
3. Save the course topic list, prerequisite distances, instructions, and policy with the activity. Reuse them when resuming.

If the database is unavailable, use the latest saved course-topic and prerequisite snapshot and record which snapshot was used. Missing topic or graph information uses the unknown-topic response below; it must not stop the diagnostic.

### Answer policy and timing

| Question's topic | Intended response | Time from question appearing to submission |
|---|---|---|
| In the course | Independently choose 50% correct or 50% Don't Know | Correct: random 4½–6 minutes. Don't Know: immediate. |
| Direct prerequisite of a course topic: 1 edge | Correct | Random 1½–2 minutes |
| Prerequisite 2 edges from the closest course topic | Correct | Random 1–1½ minutes |
| Prerequisite 3 or more edges from the closest course topic | Correct | Random 30–60 seconds |

Check course membership first: a topic in the course keeps the 50/50 policy even if it is also a prerequisite of another course topic. An unknown topic or one with no path to the course is not a distant prerequisite; capture it, record the uncertainty, and choose Don't Know.

Draw each correct-answer delay uniformly within its range. Capture and solving time count toward that delay; wait only for the remaining time. If solving takes longer, submit when ready. **Don't Know has no deliberate wait** after capturing and classifying the question. Save the response decision, sampled delay, and question start time so resuming does not redraw or restart the wait.

### Capture sequence

1. Capture every question, including all answer fields, choices, and images, before answering or choosing Don't Know. Save its numbered position when a source question ID is unavailable.
2. Identify its topic from an existing source-question association when available. Otherwise, have the same sub-agent match it against the saved course and prerequisite topics. Use the graph's recorded distance for timing.
3. Apply the policy above. Record the matched topic, distance, chosen action, timing, any offered retry, feedback, and next question presented. Continue until Math Academy ends the diagnostic.
4. Capture the results and history. Match numbered positions to the revealed `q-N` IDs and collect topic/knowledge-point references, difficulty, and worked solutions, including for skipped questions where provided.

Record the branches observed without inventing unvisited routes. A diagnostic worked solution remains part of its question; it does not become a canonical example.

## 3.6. Multistep

A multistep is one problem with shared setup and ordered parts. In the current schema mapping, an assignment activity contains a step referencing an assigned problem, which references the reusable multistep. The multistep owns its part steps, which reference reusable questions.

**Answer policy:** Aim for every part correct. Use the same sub-agent conversation for the whole problem, including shared context, earlier parts, and their confirmed answers.

1. Capture the source problem ID, title, instructions, shared setup, diagrams, and part order. Keep shared context available as each part is presented, including any additions revealed later.
2. Capture and answer each part in order, including all answer fields. Save its grade and explanation before continuing. Keep the original part statement separate from the shared context and earlier answers supplied to the sub-agent.
3. After the final part and history review, confirm the complete part sequence and collect each question's difficulty, topic/knowledge-point references, and answer evidence. Database Preparation stores shared setup in `multistep/context` and part order through `multistep/first-step` and `step/next`.
