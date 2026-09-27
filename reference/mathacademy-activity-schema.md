# Math Academy completed-activity schema

Inspection date: 2026-09-24. Source: authenticated Chrome result pages linked from the learner's activity history.

This document describes data observable on completed activity pages. It is a proposed export schema grounded in the inspected HTML and expanded UI. It is not Math Academy's internal database or API schema, and it does not establish behavior for active, abandoned, or future activities.

The six activity types remain distinct: **Lesson**, **Review**, **Assessment**, **Multistep**, **Diagnostic**, and **Supplemental Diagnostic**. Shared presentation does not erase those distinctions.

## Evidence and coverage

Seventeen completed activities were inspected: three of each type except Supplemental Diagnostic, for which both available entries were inspected. Counts below come from loaded question-result elements, not XP. Explanation expansion was verified for every activity family. This is sampled coverage of the completed-history UI, not a proof of every possible platform variant.

| Activity | Task | Name or scope | Questions | KP groups | Displayed XP | Notes |
| --- | --- | --- | ---: | ---: | --- | --- |
| Lesson | [13510941](https://mathacademy.com/learn?taskId=13510941) | The Rational Roots Theorem | 9 | 4 | 19/19 | Grouped result layout |
| Lesson | [13512234](https://mathacademy.com/learn?taskId=13512234) | The Argument of a Complex Number | 8 | 4 | 20/16 | Earned XP exceeds denominator |
| Lesson | [12601433](https://mathacademy.com/learn?taskId=12601433) | Left and Right Riemann Sums in Sigma Notation | 4 | 2 | -1/14 | Negative earned XP; explicit CALCULUS I label |
| Review | [13675888](https://mathacademy.com/learn?taskId=13675888) | Multiplicities of the Roots of Polynomials | 3 | — | 4/4 | 1 incorrect result |
| Review | [13537500](https://mathacademy.com/learn?taskId=13537500) | The Argument of a Complex Number | 5 | — | 4/4 | 1 incorrect result |
| Review | [13409092](https://mathacademy.com/learn?taskId=13409092) | Calculating Limits of Radical Functions Using Conjugate Multiplication | 5 | — | 0/6 | 2 incorrect results |
| Assessment | [13553418](https://mathacademy.com/learn?taskId=13553418) | Quiz 4 | 10 | — | 10/15 | 3 incorrect results |
| Assessment | [12228526](https://mathacademy.com/learn?taskId=12228526) | Quiz 1 (Retake) | 8 | — | 13/13 | 1 incorrect result |
| Assessment | [4833336](https://mathacademy.com/learn?taskId=4833336) | Quiz 1 | 9 | — | 2/12 | 5 incorrect results, all with No answer |
| Diagnostic | [13469233](https://mathacademy.com/learn?taskId=13469233) | Mathematical Foundations II: Placement Exam | 65 | — | 60 XP | No displayed denominator; 65 explanations |
| Diagnostic | [11604423](https://mathacademy.com/learn?taskId=11604423) | Calculus II: Placement Exam | 45 | — | 31 XP | 20 Correct, 25 Incorrect; 45 explanations |
| Diagnostic | [4748206](https://mathacademy.com/learn?taskId=4748206) | Multivariable Calculus: Placement Exam | 9 | — | 0 XP | 3 Correct, 6 Incorrect; date discrepancy described below |
| Multistep | [13498401](https://mathacademy.com/learn?taskId=13498401) | Quadratic Profit Functions | 7 | — | 13/10 | All Correct |
| Multistep | [11976594](https://mathacademy.com/learn?taskId=11976594) | Limits of Trigonometric Functions, Instantaneous Rates of Change, and Infinite Geometric Series | 10 | — | 12/15 | 2 incorrect results |
| Multistep | [4821880](https://mathacademy.com/learn?taskId=4821880) | Exploring Function Arithmetic Using Graphs | 9 | — | 2/7 | 4 incorrect results |
| Supplemental Diagnostic | [9319474](https://mathacademy.com/learn?taskId=9319474) | Mathematical Foundations II: Supplemental Diagnostic Exam | 3 | — | 4 XP | 2 Correct, 1 Incorrect; 3 explanations |
| Supplemental Diagnostic | [5454029](https://mathacademy.com/learn?taskId=5454029) | Mathematical Foundations II: Supplemental Diagnostic Exam | 5 | — | 3 XP | 3 Correct, 2 Incorrect; 5 explanations |

A dash in KP groups means that no lesson-style grouping was displayed, not that the activity covers zero knowledge points. Task 12563189 was opened but its results could not be inspected reliably because of browser timeouts; it is excluded from the evidence table.

| Type | Result structure | Main topic / prerequisites | XP denominator |
| --- | --- | --- | --- |
| Lesson | Ordered KP groups, each containing question/explanation pairs | Both shown in samples | Shown |
| Review | Flat question/explanation pairs with per-question topic/KP links | Both shown in samples | Shown |
| Assessment | Flat question/explanation pairs with per-question topic/KP links | Neither shown in samples | Shown |
| Multistep | Ordered dependent questions with per-question topic/KP links | Neither shown in samples | Shown |
| Diagnostic | Flat question/explanation pairs with per-question topic/KP links | Exam scope in title; no main topic/prerequisite links | Absent |
| Supplemental Diagnostic | Same observed result structure as Diagnostic | Exam scope in title; no main topic/prerequisite links | Absent |

## Recommended representation

Use one activity record with nested groups/questions/content, or equivalent related tables. The existing one-row-per-activity CSV remains useful as an index, but it cannot cleanly contain ordered questions, multiple answer parts, worked explanations, images, and knowledge-point relationships.

Recommended logical records:

1. `activity`: one completed task and its summary.
2. `knowledge_point_group`: lesson result grouping, when present.
3. `question_result`: one displayed question occurrence within an activity.
4. `rich_content`: prompt, solution, answer, and asset-bearing content.
5. `source_observation`: URL, capture time, selectors, and provenance.

The companion `mathacademy-activity.schema.json` is a proposed JSON Schema (Draft 2020-12) for one activity record. It preserves optional/unknown fields, allows newly observed properties, and leaves result labels extensible. It is not a declaration of Math Academy internals. The activity owns ordered `question_results`; lesson groups refer to question occurrence indices to avoid duplicating results.

These record names and field names are proposed. CSS selectors, labels, counts, IDs, and inspected content behavior below are observations.

## Shared activity fields

| Proposed field | Type | Meaning and source |
| --- | --- | --- |
| `task_id` | string | ID in `learn?taskId=…`, also present in result container IDs. Keep as an identifier, not a quantity. |
| `url` | URL string | Observed completed-task URL. |
| `activity_type` | enum string | Literal displayed type; preserve all six values. |
| `task_name` | string | Displayed title from `.taskNameUnlocked`; may be a topic, quiz name, scenario, or exam title. |
| `status_raw` | string | Displayed completion text, such as `Completed @ 5:05 PM`. |
| `status` | string | Normalized `completed` for inspected examples; broader status vocabulary is unverified. |
| `completed_time_raw` | string/null | Header completion time without inventing a date or zone. |
| `completed_date_raw` | string/null | Feed date heading or another explicit date source, with provenance. |
| `completed_at_local` | string/null | Normalized local date/time when supported, without claiming a verified timezone. |
| `completed_at` | datetime/null | Populate only when date, year, and timezone have adequate evidence. |
| `completed_at_provenance` | object/null | Where normalization obtained date/year/zone: feed, explicit page, user setting, or inference. |
| `xp_raw` | string | Preserve the displayed XP label and both values when shown. |
| `xp_earned` | number/null | Signed earned XP; observed negative, zero, positive, and greater-than-denominator values. |
| `xp_possible` | number/null | Displayed denominator when present; absence is null. |
| `xp_unit` | string | `XP` when explicitly displayed. |
| `course_label_raw` | string/null | Task's own optional course label, separate from global sidebar course. |
| `course_id` | string/null | Only from an observed task-specific course link or other explicit source; not from the sidebar by default. |
| `course_code` | string/null | Existing local catalog value if joined, with provenance; not established by the task header alone. |
| `topic_id` | string/null | Main topic ID when an observed task-topic link identifies it. |
| `topic_url` | URL string/null | Main task-topic link for the lesson/review samples. |
| `prerequisites` | array/null | Ordered task-specific prerequisite topic links; empty for verified absence, null if not inspected. |
| `context` | rich_content/null | Shared scenario/problem context only when actually available on the result page. |
| `result_layout` | string/null | Observed result container/layout label, separate from activity type. |
| `question_count` | integer | Count of displayed question result occurrences. Derived from loaded content. |
| `knowledge_point_group_count` | integer/null | Count of lesson KP groups; null for ungrouped layout. |
| `question_results` | array | Ordered question-result records. |
| `knowledge_point_groups` | array/null | Lesson groups preserving both group and question ordering. |
| `source_observation` | object | Capture information and source evidence. |

### Header selectors

All inspected result pages use:

```text
#taskAnswersFrame
  .taskAnswers#taskAnswers-TASK_ID
    .taskExpanded#task-TASK_ID-expanded
    <activity-specific result content>
```

Observed header descendants include:

| Selector | Meaning |
| --- | --- |
| `.taskHeader` | Container for type, completion icon, and XP |
| `img.completedCheckmark` | Completion icon |
| `.taskTypeLocked` | Displayed activity type |
| `.taskPointsLocked` | XP wrapper |
| `.taskPoints` | XP display |
| `.pointsGained`, `.pointsLost` | Observed XP styling classes, not a standalone score model |
| `.completedTaskPointsSlash` | Separator when a denominator is displayed |
| `.completedTaskPoints` | Denominator plus XP unit for scored activities; XP unit only for diagnostics |
| `.taskCourseNameUnlocked` | Optional task-specific course label; may exist but be empty |
| `.taskNameUnlocked` | Task title |
| `.taskTimeCompleted` | Completion status/time label |
| `.taskDetails#taskDetails-TASK_ID-expanded` | Optional task details; empty in inspected diagnostic |
| `.taskTopicLinkExpanded` | Lesson/review main topic link |
| `.taskPrerequisiteLink` | Lesson/review prerequisite topic links |

A hidden `.taskCompletedDate#completedTasksDate-13469233` input was present without a `value` attribute. On task 11604423, both the absent value attribute and empty `value` property were verified. Its existence is not evidence of a usable completion date. Prefer explicit displayed values and verify any attribute before relying on it.

### XP must remain separate from correctness

The examples rule out treating `xp_earned / xp_possible` as a count of correct answers or a bounded percentage:

- Review 13675888 shows 4/4 XP with one incorrect question among three.
- Assessment 13553418 shows 10/15 XP for ten questions, three incorrect.
- Lesson 13512234 shows 20/16 XP.
- Lesson 12601433 shows -1/14 XP.
- Diagnostic 13469233 shows 60 XP for 65 question results and no denominator.

Store earned XP, displayed denominator, number of questions, and derived result counts separately. Do not clamp XP or invent a denominator for diagnostic activities. The export name `xp_possible` follows the existing CSV, but means the displayed denominator, not a verified maximum achievable award. A Completed label does not establish that a lesson was mastered or every answer was correct.

## Shared question-result fields

A question result is a displayed occurrence within a task. Use `(task_id, occurrence_index)` as the safe export key, while preserving the question ID as a separate reference. Global uniqueness of question IDs across tasks or repeated attempts is not established.

| Proposed field | Type | Meaning and source |
| --- | --- | --- |
| `occurrence_index` | integer | One-based document order within this activity. |
| `question_id` | string | ID from `.question#question-ID`; `.helpButton[questionid]` also identifies it. |
| `question_number_raw` | string | Displayed number from `.questionNumber`, preserving punctuation. |
| `question_number` | integer/null | Parsed displayed number if unambiguous. |
| `group_index` | integer/null | Parent lesson KP-group order when grouped. |
| `knowledge_point_name` | string/null | Linked subskill title on flat results or parent lesson-group title. |
| `knowledge_point_id` | string/null | Fragment from an observed topic/KP link; unavailable from lesson-group title alone. |
| `knowledge_point_url` | URL string/null | Observed `.questionKP` href. |
| `topic_id` | string/null | Topic ID parsed from that link, separate from knowledge-point ID. |
| `prompt` | rich_content | Question text plus inline answer-position markup where present. |
| `prompt_graphics` | array | Graphics associated with the question, including separate graphic frame. |
| `difficulty_raw` | string/null | Displayed difficulty letter. E/M/H observed in diagnostic. |
| `difficulty` | string/null | Easy/moderate/hard when corresponding class provides evidence. |
| `answered_at_raw` | string/null | `.answerCreated` text, including displayed date/time. |
| `answered_at_local` | string/null | Normalized local answer date/time only when the year is supported. |
| `answered_at` | datetime/null | Normalized value only with adequate date/year/zone evidence. |
| `elapsed_raw` | string/null | Displayed elapsed duration, such as `Elapsed: 0:50`. |
| `elapsed_seconds` | integer/null | Parsed duration; preserve raw alongside normalized value. |
| `result_raw` | string | Literal outcome text, such as `Correct` or `Incorrect`. |
| `result` | string | Proposed normalized outcome; keep unknown labels rather than forcing a boolean. |
| `explanation` | rich_content/null | Worked solution from paired explanation element. |
| `student_answer_present` | boolean | Whether a student-answer region exists. |
| `student_answer_state` | enum | Proposed: `not_shown`, `no_answer_label`, or `shown`; never infer one from another. |
| `student_answer` | rich_content/null | Exact displayed response from optional `.studentAnswer`. |
| `displayed_answer_parts` | array | Answer-position values visible in prompt, distinct from submitted response. |
| `choices` | array/null | Only if choices are actually displayed; missing choice list is not an empty original option set. |
| `source_observation` | object | Container IDs/selectors and capture evidence. |

### Question and explanation selectors

```text
.question#question-QUESTION_ID
  .questionHeader
    .questionNumber
    a.questionKP              # flat results where observed
    .helpButton[questionid]
  .questionGraphicFrame       # optional
  .questionText
  .answerDetails
    .questionDifficulty
    .answerCreated
    .answerDetailsSeparator
    .timeElpased
    .answerResult
.questionExplanation#questionExplanation-QUESTION_ID
  <rich worked solution>
  .studentAnswerHeader         # optional
  .studentAnswer               # optional
```

The selector `.timeElpased` contains that exact misspelling in the observed DOM.

Explanations are siblings of questions rather than children. They are already present in loaded DOM while visually collapsed. Clicking a question's `.answerDetails` reveals the matching explanation. This was verified by expansion in the inspected activity families.

The `?` control is for reporting content errors. It does not expose extra result schema; do not submit a report during extraction.

### Correct answer versus student's answer

Inline `.freeResponseTextbox` fields may show the correct/displayed answer on the completed result page. They are not reliable evidence of the student's submitted answer.

Observed lesson question 323830 shows `+2/3` in an inline blank while the result is Incorrect and the separate `.studentAnswer` contains `-2/3`.

Assessment blanks differ: inspected questions 350593 (Correct) and 349085 (Incorrect) have empty `.freeResponseTextbox` fields. An empty displayed textbox does not establish that the student submitted no response. Preserve an empty string as the observed field value and keep student-answer state separate.

Preserve these independently:

- The blank's order, local DOM ID, displayed value, and surrounding prompt position.
- The result label.
- The optional separate student-answer content.
- The worked explanation.

IDs such as `freeResponseTextbox-1`, `freeResponseTextbox-2`, and `freeResponseTextbox-3` repeat in different questions. Scope lookup to the question and use local order; do not use `document.getElementById('freeResponseTextbox-1')` as a unique answer identifier.

Correct results inspected did not show a student-answer block, and original option lists were absent from the inspected assessment results. Do not reconstruct selected letters or original choices from an explanation.

Assessment `.questionStatements` regions containing `ol > li` are Roman-numbered statements within the question, not selectable answer choices. Preserve them as prompt content.

Multiple blanks can belong to one question. Multistep questions 167210 and 133099 each have two `.freeResponseTextbox` elements; question 133099 has student-answer text `-4, 2`. A single outcome, difficulty, and elapsed time describe the whole question. No per-blank grading is exposed in these examples.

In Diagnostic 13469233, 26 of 65 explanations have student-answer regions. Sampled incorrect records show literal italic `No answer`. Missing region and explicit `No answer` are different observations. Neither alone proves that the platform classified a question as skipped.

## Rich content and assets

Use one reusable rich-content structure for prompts, explanations, student answers, displayed answer parts, and choices when present.

| Proposed field | Type | Meaning |
| --- | --- | --- |
| `html` | string/null | Sanitized captured markup preserving order and semantic content. |
| `text` | string | Searchable text, with a documented math-normalization policy. |
| `math` | array | Ordered formula records with MathML and, only when available, original TeX. |
| `assets` | array | Referenced graphics with observed URL, alt text, and content position. |
| `tables` | array/null | Structured rows/cells if separately extracted; retain relation to surrounding content. |
| `answer_parts` | array/null | Inline blanks/selects and displayed values, scoped to this content/question. |
| `source_selector` | string | Source element selector or scoped locator. |

Observed content includes paragraphs, lists, tables, images, separate graphics, and MathJax output. Question images may occur in `.questionGraphicFrame`; explanation graphics may occur in `.graphic`. Image URLs include `/graphics/…` paths.

For example, Diagnostic 11604423 question 70661 asks the student to identify a graph. Its result prompt contains no original graph choices or selection controls. Expanding its explanation exposes the correct graph at `/graphics/q-70661-a-1`, with no alt attribute. Preserve that as a solution asset; it does not recover the original option set or the student's selected choice.

MathJax assistive MathML is present and retains mathematical structure. Plain `innerText` can scramble fractions, matrices, powers, and alignment; it should not be the only representation. Preserve original visible HTML/MathML, and avoid duplicating visual and assistive copies of the same formula in text output.

Resolve relative asset/topic links against `https://mathacademy.com`, while retaining the raw href/src for traceability. Do not invent image meanings from opaque filenames.

## Type-specific layouts

### Lesson

Observed result container: `.kpList`, with ordered `.kp` children. Each group begins with `.kpTitle` and contains alternating question and explanation siblings.

The group title has text like `KP 1. …`. The inspected lesson results do not expose a numeric knowledge-point ID or link in that title. Export group order and title; keep numeric KP ID null unless independently verified from a cited source.

Lesson question numbers preserve the activity-wide order. Retain both activity-wide question order and group membership.

Main topic link and prerequisite topic links are present in the expanded header. A task's own course label is optional. Lesson answer timestamps vary across questions.

### Review

Observed result container: `.reviewAnswerList`, with flat question/explanation pairs. Question headers have `a.questionKP` links, allowing topic ID and knowledge-point ID to be recovered independently.

Main topic and prerequisite links can occur in the header. Review answer timestamps vary across questions. XP denominator is not the count of questions or correct responses.

### Assessment

Observed result container: `.testAnswers#testAnswers-TASK_ID`, with flat question/explanation pairs and per-question knowledge-point links. No prerequisite links were observed on Quiz 4.

Titles include quiz names and a retake label; do not store those as catalog topic names or assign a main topic ID without a real link. All `.answerCreated` values within each of the three inspected assessments equal that task’s completion timestamp; they must not be interpreted as individually measured question completion times without further evidence.

Retake 12228526 is an independent task with its own ID and title. No explicit `retake_of` relation was exposed. Do not infer such a relation solely from quiz naming.

The older assessment uses the same observed structure. Its five incorrect questions each show `No answer`; correct questions do not have student-answer blocks. The additional examples expose no new assessment-specific fields. Assessment prompt blanks remain empty even when the result is Correct, as described above.

### Diagnostic

All three inspected diagnostics use the same observed `.testAnswers#testAnswers-TASK_ID` pairing pattern as assessments. They have 65, 45, and 9 question records respectively; those counts are observations, not fixed limits.

Its task header shows exam scope in the name, `Diagnostic`, 60 XP, and completion time. The task course-label element and task-details region are empty. No XP denominator or result-container link to a placement/knowledge profile was observed.

Difficulty classes observed are `difficultyEasy`, `difficultyModerate`, and `difficultyHard`, displayed as E, M, and H. Results observed are Correct and Incorrect. Its answer timestamps vary across questions.

Questions 53708 and 53707 both link to `/topics/491#2993`. This confirms that repeated knowledge points may have distinct ordered questions within one diagnostic.

Calculus II task 11604423 has 45 questions, 45 explanations, 31 XP, 20 Correct and 25 Incorrect results. Its question timestamps run from July 14 at 5:32 PM to 8:10 PM. Multivariable Calculus task 4748206 has nine questions and nine explanations, 0 XP, three Correct and six Incorrect results. It has the timestamp discrepancy documented below. No additional diagnostic-only result fields were found in these comparisons.

### Multistep

Observed result container: `.multistepAnswerList`, containing flat alternating question/explanation pairs with per-question `.questionKP` links. This structure was confirmed across tasks 13498401, 11976594, and 4821880. Explanation expansion was verified on question 167208.

No main task-topic link or prerequisite links appear in these samples; task-details and task-course-label regions are empty. The task name describes the multistep activity rather than a single catalog topic.

Individual questions may contain multiple answer blanks, but expose a single result/difficulty/time record. Keep ordered answer parts without inventing per-part correctness.

A shared scenario can be unavailable on the completed result page: an inspected first question refers to `p(20)` without defining `p` in a separate shared scenario region. Preserve any context actually shown in question/explanation content, mark separate context unavailable, and do not reconstruct missing setup from another source without provenance.

### Supplemental Diagnostic

Both available examples were inspected. They use `.testAnswers#testAnswers-TASK_ID`, the same question/explanation structure, per-question topic/KP links, difficulty, result, timestamp, elapsed duration, graphics, worked solutions, and optional student-answer fields as ordinary diagnostics. Explanation expansion was verified for question 119781 in task 9319474.

Task 9319474 has three questions and three explanations, 4 XP, two Correct and one Incorrect result. Task 5454029 has five questions and five explanations, 3 XP, three Correct and two Incorrect results. All incorrect questions in these two examples show the separate `No answer` label. Both task headers omit an XP denominator, main topic link, and prerequisite links; exam scope is stated in the title. Per-question answer times vary.

The user's hypothesis is supported for the observed export schema: Diagnostic and Supplemental Diagnostic share the same result fields and nesting. Preserve distinct type values. Their question counts differ in these examples, but these samples do not establish fixed limits, selection rules, scoring equivalence, or any internal algorithmic difference.

## Dates, missingness, and provenance

Preserve raw display strings before normalization. The diagnostic header supplies only a time; question strings such as `Thu, Sep 17th @ 3:35 PM` omit year and timezone. A feed date or existing CSV may support a join, but record that source explicitly.

Do not silently apply the current system timezone to historical activity. If using `America/Los_Angeles` as a user-context assumption, label it as an assumption and distinguish normalized local time from a verified UTC instant.

**Observed discrepancy:** task 4748206 is dated `2026-01-09 00:35` in the previously reconciled feed/CSV and shows `Completed @ 12:35 AM` in its header. All nine answer records instead show `Thu, Jun 5th`, between 6:48 PM and 7:03 PM, with no year. Do not simply assign the task-completion year to those answer records. Whether this reflects resumed work, reused history, or another display behavior is unresolved; preserve both sources and the discrepancy rather than inventing an explanation.

Displayed elapsed durations are question-level values, not proof of uninterrupted active work. Their sum may differ from wall-clock task duration; the result page does not expose a reliable total task start time in these samples.

Use null for unknown/unavailable values, an empty array for a verified empty collection, and an explicit absence flag when missing-versus-empty matters. Keep an explicit `No answer` label as content/state rather than converting it to the same null as an absent answer region.

The global sidebar displays the account's current course, progress, XP totals, and leaderboard. Those are not historical task fields and must not be attached to an old activity as though they were its completion-time values.

The existing `vault/252/progress-notes.md` says many course assignments in `progress.csv` were inferred from the enrollment timeline. Assessment/multistep course attributions are contextual; catalog IDs on lessons/reviews were reconciled locally. Preserve those joins as derived fields with provenance rather than presenting them as result-page facts.

## Extraction and validation guidance

1. Load the observed completed-task URL once.
2. Scope reads to `#taskAnswers-TASK_ID` so sidebar/account state is excluded.
3. Capture header fields and actual task links.
4. Identify the activity-specific container and enumerate ordered questions/groups.
5. Pair each question with its explanation using both position and matching question ID.
6. Capture already-loaded collapsed content; a verified expansion establishes UI semantics without opening every question.
7. Keep prompt/displayed blanks, student's answer, result, explanation, and XP separate.
8. Record capture time, source URL, selectors, and any inferred normalization.
9. Verify question counts, explanation pairing, group membership, IDs, and null handling.
10. Preserve unrecognized fields or labels for review instead of dropping them.

Recommended checks include: header task ID agrees with URL; each question has a paired explanation when expected; duplicate question IDs remain representable; question numbers preserve source order; a missing XP denominator stays null; earned XP is not range-clamped; math and assets survive normalization; inferred courses/timestamps are labeled.

## Limits of the observed schema

- Coverage is the 17 completed activities above; active-task, abandoned-task, and future variants are unverified.
- The results expose worked explanations and some recorded answers, but not every original answer choice, selected option, question-format identifier, answer-attempt identifier, or shared multistep scenario.
- No independent machine field for a correct answer was found across all formats. Inline result blanks and worked explanations must remain separate representations; extracting a final answer from prose would be a derived operation.
- No per-blank grade, reliable task start time, task-level active duration, diagnostic placement score/profile, or adaptive selection parameters were exposed on the inspected result pages.
- Missing lesson KP IDs can potentially be joined from the linked topic/catalog, but such a join is outside the task-result observations and needs provenance.
- Historical timestamp normalization remains uncertain where the page omits year/zone or conflicts with the feed.
- JSON validity checks structure; it cannot prove complete extraction or source accuracy. Future exporters must validate counts, group references, source order, and content separately.
