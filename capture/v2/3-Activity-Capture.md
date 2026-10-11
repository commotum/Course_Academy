# 3. Activity Capture

Complete the selected activity, then review its history page to finish the capture. The shared process handles content; each activity type sets the answer policy, submission timing, and completion rules.

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
6. Check live questions against history, retaining repeated presentations and discrepancies. Continue to Post-Activity Processing. Database Preparation handles content recovery, image-library references, and matching existing entities; learner responses, timing, and solver reasoning remain evidence for later.

Keep task, content, and placement IDs separate. Questions use `q-N`; canonical examples use `e-N`. Screen labels such as `step-qN` are not verified placement IDs. Keep observed attempt order distinct from reusable activity structure; preserve evidence of the route actually taken.

Never defer or abandon an unfinished activity. Recover and continue. After an external interruption or manual stop, resume saved progress and check what Math Academy already accepted before repeating an action.

### Questions

1. Before answering, save the problem, calculator instructions, question ID when visible, HTML, screenshot, and images. Record each answer field's type, location, choices, and displayed order.
2. Launch one math-solving sub-agent for the first question and save its session ID. Resume that same conversation throughout the activity, including across knowledge points. Send each new question's fields, current choices, screenshot, and images, plus new examples, shared context, solutions, and grades. Earlier questions and reasoning remain in the conversation.
3. When answering, request the correct answer for each field, reasoning, and confidence; save these separately from Math Academy's content. Apply the activity's answer policy to choose the actual response and preserve that decision on resume.
4. Enter and verify the field values or selected choices. Submit when the activity calls for it. Record actual responses, skips, retries, and timing. Check current choices again after a reload or shuffle.
5. Save each revealed grade, correct answer, worked solution, HTML, and image. Capture and answer any additional fields revealed within the same question before advancing.
6. Give feedback to the same sub-agent to check its answer. Preserve Math Academy's answer and flag disagreements. A submission alone does not establish the correct answer.
7. Finish the record during history review. Record difficulty after the activity ends.

**C** means intended correct; **W** means intentionally incorrect. The sub-agent solves for the correct answer in both cases. Record intended responses separately from actual grades. When uncertain, use the best available response, or Don't Know when the activity's policy calls for it, and record the uncertainty.

## 3.2. Lesson

A lesson teaches one topic through tutorials and knowledge points. Each knowledge point has a canonical example followed by adaptive practice questions.

**Answer policy:** Independently choose `CWCWC` with 70% probability or `WCWCC` with 30% probability for each knowledge point. Keep that choice on resume. After those five questions, answer any additional questions correctly until Math Academy advances. A retake following a negative-XP completion uses all-correct answers throughout.

1. Capture each tutorial's title, body, images, and source ID. Capture each canonical example's title, problem, worked solution, images, and `e-N` ID, and pass it to the sub-agent before the associated practice.
2. Capture and answer the practice questions, retaining their knowledge-point association and every revealed result. Follow Math Academy's completion state even when it serves fewer questions or ends the lesson unsuccessfully.
3. After history review, capture `/topics/<topic-id>` for the complete lesson: tutorial and example content, verified placement/content IDs, titles, and order, including sections this attempt did not visit. Database Preparation compares that definition with the existing lesson and preserves existing identities when updating it.

Lesson steps point to tutorials and knowledge points. Served practice questions join the knowledge point's pool, rather than becoming permanent lesson steps. Failed lessons and retakes share the definition but retain separate attempt evidence.

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

**Answer policy — needs review:** Decide whether to answer correctly or choose **Don't Know** using the lessons already captured in `math` and the lessons we still want to capture. The existing script's prerequisite and covered-topic rules are reference material; the replacement needs its own policy.

Review what counts as a captured lesson, which lessons should remain available, how prerequisite/knowledge-point matches affect decisions, and when to accept retries. Save the policy and decisions for resuming. For an uncertain match, capture the question and use Don't Know to continue.

1. Save the instructions and the capture information used to make placement decisions.
2. Capture every question before answering or skipping, including complete answer fields and choices. Save its numbered position when a source question ID is unavailable. Record the chosen action, its reason, any offered retry, feedback, and the next question presented.
3. Continue until Math Academy ends the diagnostic, then capture its results and history. Match numbered positions to the revealed `q-N` IDs and collect topic/knowledge-point references, difficulty, and worked solutions, including for skipped questions where provided.

Record the branches observed without inventing unvisited routes. A diagnostic worked solution remains part of its question; it does not become a canonical example.

## 3.6. Multistep

A multistep is one problem with shared setup and ordered parts. In the current schema mapping, an assignment activity contains a step referencing an assigned problem, which references the reusable multistep. The multistep owns its part steps, which reference reusable questions.

**Answer policy:** Aim for every part correct. Use the same sub-agent conversation for the whole problem, including shared context, earlier parts, and their confirmed answers.

1. Capture the source problem ID, title, instructions, shared setup, diagrams, and part order. Keep shared context available as each part is presented, including any additions revealed later.
2. Capture and answer each part in order, including all answer fields. Save its grade and explanation before continuing. Keep the original part statement separate from the shared context and earlier answers supplied to the sub-agent.
3. After the final part and history review, confirm the complete part sequence and collect each question's difficulty, topic/knowledge-point references, and answer evidence. Database Preparation stores shared setup in `multistep/context` and part order through `multistep/first-step` and `step/next`.
