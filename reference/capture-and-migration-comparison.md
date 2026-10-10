This describes the capture script inspected on October 10, 2026 and the evidence used for the migration through `math` basis 132. Older captures can differ by script version or page layout.

Each activity section follows the script's stages. **MA HTML source** names literal Math Academy elements, classes, attributes, or URLs. **Saved evidence** names files and JSON properties produced by our script; these JSON files are DOM extractions and checkpoints, not an assumed Math Academy JSON API. **Schema / migration use** describes how that evidence was represented in the new database, which can include work the original capture importer did not perform.

Capture filenames below are relative to a `<task-id>/` folder under `reference/mathacademy/question-capture/` or `question-capture-workers/{linear,multivariable,differential}/`. `N` denotes an MA content/question ID; `S` denotes a page step identifier. A content ID, placement ID, numbered diagnostic position, and task ID are different identifiers. Generated answer-field keys and UUIDs are our identifiers, not MA labels.

Source code: [lesson/review player and shared extraction](../scripts/question_capture/browser.py), [HTML-to-content extraction](../scripts/question_capture/dom.js), [multistep player](../scripts/question_capture/multistep.py), [assessment player and completed-activity joins](../scripts/question_capture/assessment.py), [diagnostic player](../scripts/question_capture/diagnostic.py), and [capture orchestration](../scripts/question_capture/capture.py).

All confirmed original content described here was transacted with `:org/Math-Academy` as source. Learner submissions, results, elapsed times, XP, and progress observations remained evidence rather than migrated learner state. Assistant corrections remain separate and unapplied.

# 1. Lesson

Process: select the lesson → walk its tutorial, example, and question screens → capture each question before and after submission → capture completion and course progress → open completed-activity history → join difficulty, knowledge points, and explanations → prepare question/example content for import.

## Activity

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Selection, before starting | `/learn`, `#incompleteTasks .taskUnlocked`; card `#task-N`; `.taskTypeUnlocked`; `a.taskStartButton` with `/tasks/<task-id>/topics/<topic-id>/lesson`; `[id^="taskName-"]` / `.taskNameUnlocked` | `selection/queue.json`; `state.json`: `task_id`, `task_type`, `topic_id`, `activity_url` | Identifies the lesson attempt and source topic. The task ID is not substituted for `:activity/math-academy-id`. The existing lesson activity targets the topic through `:activity/scope`. |

## Step

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| During the lesson, before each screen | `.stepButton.current`, visible `.step.questionWidget`, and `continueButton-<token>` identify the current screen; tokens follow `stepButton-tN`, `stepButton-eN`, or `stepButton-qN`, with content under `#step-tN`, `#step-eN`, or `#step-qN` | The screen's HTML in its content capture; `state.json.pending_continue.source_step` while advancing | These runtime tokens guide the player. They do not establish a complete durable placement sequence or prove that the suffix is the schema's `:step/math-academy-id`. |
| During migration, for six affected lessons | Separate `/topics/<topic-id>` pages: `.step` elements with `stepId`, `stepType`, and `contentId`; `.sectionLink` / `.stepName` identify sections; page order establishes placement order | `reference/edb-math/imports/math-academy/newer-captures/source-evidence/topic-<id>.html`; `original-batches.json` | Additional retrieval, not automatic lesson capture. Updated `:activity/steps`, `:activity/first-step`, `:step/content`, `:step/next`, and verified `:step/math-academy-id`. Preserved existing UUIDs; added 14 steps and reused 28 across those six lessons. |

## Tutorial

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| When a tutorial screen is reached, before Continue | `#step-tN`; instructional HTML and `.stepName` within the screen | `tutorial-N.html`, containing the element's `outerHTML` | Migration extracted `:tutorial/title`, `:tutorial/content`, and source identity. The script saved HTML and advanced; it did not run the normal question/example extraction and asset-saving routine here. |
| During migration | Saved tutorial HTML; graphics referenced by `<img>` and embedded `<svg>`; source formulas in rendered math markup | Reviewed tutorial records and source-to-image mappings in `reference/edb-math/imports/math-academy/newer-captures` | Converted text, equations, tables, and links; extracted saved SVGs; separately recovered missing graphic files. Eleven tutorials were additional sections. Tutorial 15932 replaced 14488 on the same existing entity, preserving its history. |

## Example

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| When an example screen is reached | `#step-eN`; `.exampleQuestion`; `.exampleExplanation`; `.stepName` | `example-N.json` (`problem`, `worked_solution`, `name`, `html`, `assets`), `example-N.png`; `state.json.examples["e-N"]` | `:question/problem`, `:question/worked-solution`, and `:question/math-academy-id = "e-N"`; relationship through `:knowledge-point/canonical-example`. |
| Before practice for that knowledge point | Example title and ID, matched against the script's database topic snapshot; a new example/title can establish a new knowledge point within that topic | `state.json.current_kp`, `state.json.kps`; `content.json.canonical_examples`; `new_knowledge_points` when applicable | Associates following practice with the knowledge point. Difficulty and answer fields are generally absent from the example screen; the script records those absences rather than inventing them. |

## Question

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Before answering | `#step-qN`; `.questionWidget-text`; `.questionWidget-graphic`; `.questionWidget-calculatorInstructions` | `q-N-before.json`: `problem`, `calculator_instructions`, `html`, `fields`, `assets`; `q-N-before.png`; `state.json.questions["q-N"].before` | `:question/problem`, `:question/math-academy-id = "q-N"`, and `:question/requires-calculator` where positively established. Missing instructions do not establish `false`. |
| After submission, before Continue | `.questionWidget-result`; `.questionWidget-explanation`; `.questionWidget-feedback` where present | `q-N-after.json`, `q-N-after.png`; question record `after`, `actual_result`, and any verification/reconciliation records | Revealed content supplies `:question/worked-solution`. The grade is evidence, not migrated learner state. Solver review may change normalized answers, so migration checked original HTML/feedback separately. |
| Completed-activity history | `/learn?taskId=<task-id>`; `.kp .question`; `.questionDifficulty`; `.questionKP` or enclosing `.kpTitle`; `.answerResult`; `.answerDetails`; `#questionExplanation-N` | `activity-metadata.json`: `id`, `difficulty`, `kp_title`, `kp_href`, `result`, `raw_html`; `history-q-N.json/png`; question record `history` | Adds `:question/difficulty`; checks the live knowledge-point mapping and grades. The script replaces normalized `worked_solution` with the expanded history explanation. Confirms the same question-ID set was captured live and in history. |

## Answer field and Answer

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Before answering: radio field | `.questionWidget-choicesTable tr`; `.questionWidget-choiceLetterCircle`; `.questionWidget-choiceText` | `before.fields`: `type = radio`, generated key `selection`, choices with source option labels, DOM IDs, HTML, types, and values | `:answer-field/type`, `:answer-field/key`, `:answer-field/choices`; individual `:answer/type` and `:answer/value`. Source option letters are presentation evidence, not stable answer identities. |
| Before answering: select field | `.selectList`, `.selectListOptions > .selectListOption`, or native `<select><option>` | `before.fields`: `type = select`, generated `field-N` key, DOM binding, and original choices | Same answer-field/answer attributes; preserve authored choices and their binding to the problem. |
| Before answering: blank field | `.matheditor-wrapper-answer` with MathQuill, or supported `<input>`, `<textarea>`, or editable element | `before.fields`: `type = blank`, generated `field-N` key, DOM binding; problem placeholders `{{field-N}}` | `:answer-field/type` and `:answer-field/key`. The blank itself does not reveal the correct `:answer/value`. |
| At entry and submission | Selected source choice or entered value in the observed field | Submitted values/options in the checkpoint; `q-N-entered.png`; solver decisions stored separately | Used to verify what was actually submitted. These submissions were not imported as learner responses. |
| After grading or in history | Explicit source answers, correct graded selections, or explicit values in MA's worked solution; custom-select classes `.correctSelection`, `.correctSelectionMultipleAttempts`, `.incorrectSelection` can establish per-field feedback | Saved field properties such as `source_selected`, `source_result`, and `source_correct`; original HTML and solution; migration key-evidence records | Establishes `:answer-field/correct`, referencing a member of `:answer-field/choices`. The original script could use solver-derived `correct_value`; migration reconstructed MA-original values and held unconfirmed keys. |

Some lesson questions reveal successive answer fields inside `.proofSection` or a `.questionWidget-healthFrame`/`.selectList` layout. The player records `q-N-proof-observed-<stage>.json/png`, `proof_stages`, source selections, feedback, and later fields before capturing the terminal result. These are stages within one question, not independently inferred lesson steps.

## Image

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Example/question reads, including solutions and choices | `<img>`, `<canvas>`, and relevant `<svg>` in the captured element; browser-observed image responses; rendered math can use assistive MathML or SVG titles | `assets/<sha256>.<extension>`; `assets/manifest.json`; each extraction's `assets` list. An original response is saved when available; otherwise a rendered capture is marked as such. Original inline SVG is also saved by the inspected routine. | Migration copies/reuses image files at `math/images/<prefix>/<sha256>.<extension>` and inserts relative references in problem, solution, and answer values. No image bytes enter EDB. |
| Tutorial reads | Images and SVG within `tutorial-N.html` | Raw HTML references and inline SVG; no equivalent automatic per-tutorial asset check | Migration extracted SVG and recovered 35 missing graphics across 27 tutorials from the four capture streams. |

## Completion and knowledge state

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Lesson completion, before leaving | `#finalScreen`; `#finalScreen-doneButton` | `lesson-completed.png`; `state.json.completion`, completion/outcome flags and earned XP | Confirms a terminal activity capture. Learner outcome and XP were excluded from the content migration. |
| After completion, before the history join | Course progress pages, `.moduleTopics .topicLink`, course/unit HTML; account sidebar where configured | `knowledge-state/lesson-completed.json`, with observed progress colors and captured HTML | Source observation only. Display-color mappings are local approximations, not exact internal MA mastery or repetition state; not migrated as learner facts. |
| After the history join | Live content combined with history metadata | `content.json`: `questions`, `canonical_examples`, and any `new_knowledge_points`; original import evidence under `edb-import/` | The original lesson importer focused on question/example content and knowledge-point relationships. Full tutorial and lesson-placement transactions were added during migration. |

# 2. Review

Process: select the review → capture each served question before and after answering → record completion and course progress → open completed-review history → resolve each question's knowledge point and difficulty → prepare reusable question content.

## Activity and Step

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Selection | `/learn` queue card; `.taskTypeUnlocked = review`; `a.taskStartButton` pointing to `/tasks/<task-id>/topics/<topic-id>/review` | `selection/queue.json`; `state.json`: task, topic, URL, and review sequence | Identifies the review attempt and topic. The attempt does not establish a new reusable review activity definition. |
| During playback | Same live player as lessons, but recognized screens must be `stepButton-qN` / `#step-qN` | Per-question captures and pending Continue checkpoints | Captures the questions actually served. A tutorial/example screen in a review is treated as an unexpected layout and deferred, not automatically imported. The served order does not establish a universal review question sequence. |

## Question

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Before answering | `.questionWidget-text`, `.questionWidget-graphic`, and calculator instructions within `#step-qN` | `q-N-before.json/png`; checkpoint `before` | `:question/problem`, `:question/math-academy-id`, and a confirmed calculator requirement. |
| After answering | `.questionWidget-result`, `.questionWidget-explanation`, and field-level feedback | `q-N-after.json/png`; checkpoint `after` and grading/verification records | Worked solution and evidence for correct answers. Unlike lessons, no preceding captured canonical example establishes the live knowledge point. |
| Completed-review history | `/learn?taskId=<task-id>`; `.reviewAnswerList .question`; `.questionKP` with `/topics/<topic-id>#<source-reference>`; `.questionDifficulty`; `.answerResult`; `.answerDetails`; `#questionExplanation-N` | `activity-metadata.json`; `history-q-N.json/png`; normalized question provenance and source reference | Matches the knowledge-point title within the linked topic, establishes `:knowledge-point/questions`, adds `:question/difficulty`, and supplies the final normalized worked solution. The question-ID set and observed grades must agree with live captures. |

## Answer field and Answer

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Before answering | Radio choices in `.questionWidget-choicesTable`; select choices in `.selectList`/`<select>`; blanks in `.matheditor-wrapper-answer` or supported inputs | `before.fields`: generated key, type, original choices, DOM bindings, and choice HTML | `:question/answer-fields`; `:answer-field/key`, `/type`, `/choices`; `:answer/type` and `/value`. Same extraction as lesson questions. |
| Entry, immediate feedback, and history | Actual selected/entered values; explicit MA field feedback; revealed source solution | Submitted values/options, source field properties, saved after/history HTML, and separate solver records | Migration confirms `:answer-field/correct` from source evidence. Neither the submitted value nor normalized solver prediction is sufficient by itself. Unconfirmed complete keys remain held. |

The shared player also handles successive proof fields when that layout occurs, using the same question-stage captures described for lessons.

## Image

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Before-answer, after-answer, and history reads | Question/choice/solution `<img>`, `<canvas>`, and relevant `<svg>` | Hashed `assets/` files, manifest, and references in extraction JSON | Copied/reused in the SSD image library; content uses relative image paths. The history reader can restore broken image aliases from the saved live result. |

## Completion and knowledge state

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Review completion | `#finalScreen`, then Done; recovery can also inspect `#completedTasks #task-N`, `.taskTypeLocked`, topic link, and `.taskPoints` | `review-completed.png` on the normal path; completion/XP/grade-recovery evidence in `state.json` | Establishes completed-capture status; does not migrate the review attempt or its XP. |
| After completion | Course progress HTML and topic display colors | `knowledge-state/review-completed.json` | Retained observation; no learner-state import. |
| After history | Joined live fields, source metadata, and expanded explanation | `content.json.questions`; `canonical_examples` is normally empty | Imports reusable practice content and knowledge-point membership, not an inferred review definition or canonical example. |

# 3. Multistep

Process: select the multistep → inspect its ordered page steps → capture initial shared context → capture, answer, and grade each part in order → record completion and progress → join completed-activity history to source questions, knowledge points, and difficulty.

## Activity and Step

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Selection | Queue card `.taskTypeUnlocked = multistep`; title; `a.taskStartButton` pointing to `/tasks/<task-id>/multisteps/<multistep-id>` | `multistep-queue.json`, including original card HTML; `state.json.multistep_id`, `title`, and URL | Source identity/title evidence for the reusable multistep representation. The task ID remains separate from the multistep ID. |
| Before answering parts | Ordered `#steps > .step`, each with `step-S`; question parts contain `#question-N` | `state.json.multistep_question_order`; each record's `source_step` and `sequence_position` | Unlike the lesson player, this explicitly records the part sequence. Migration creates `:multistep/steps`, `:multistep/first-step`, and `:step/next`; source DOM identifiers are retained as evidence rather than assumed durable placement IDs. |

## Multistep context

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Before the first question | Initial `#steps > .step` elements without a `.question`, before the first question-bearing step | `context-step-S.json/png`; `state.json.shared_contexts`, with source HTML, extracted text, images, and IDs | `:multistep/context`, preserving shared setup, diagrams, and instructions. The player defers unknown non-question steps inserted between parts rather than guessing their meaning. |

## Question

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Before each part | `#question-N`; `.questionText`; `.questionGraphicFrame` / `#questionGraphic` where present | `q-N-before.json/png`; checkpoint `local_problem`, `sequence_position`, and `source_step` | `:question/problem` for the part; `:question/math-academy-id = "q-N"`. The source-local problem is retained separately from the script's expanded solver context. |
| While preparing solver input | Shared context plus earlier captured parts and their confirmed answers | Checkpoint `before.problem` can contain this expanded representation; `local_problem` retains the actual part statement | This concatenation is script-derived, not another MA-authored statement. Migration used explicit shared context and ordered parts rather than treating solver-added context as independent source content. |
| After each Submit, before Continue | `.correctAnswerText` / `.incorrectAnswerText`; `.questionExplanation`; `continueButton-S` | `q-N-after.json/png`; `after`, `actual_result`, and verification records in `state.json` | Worked solution and answer evidence. Submission and progression are checkpointed so a confirmed part is not blindly answered again. |
| Completed-activity history | `.question[id^="question-"]`; `.questionKP`, `.questionDifficulty`, `.answerResult`, `.answerDetails`, `#questionExplanation-N` | `activity-metadata.json`; `history-q-N.json/png`; `content.json.questions` in part order | Confirms IDs, resolves source topic/knowledge-point membership, adds difficulty, and captures expanded solutions. |

## Answer field and Answer

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Before each part | Supported radio/select markup or `.matheditor-wrapper-answer` / other blank inputs within `#question-N` | `before.fields`, including multiple separately generated field keys and original choices | Owned `:question/answer-fields`, field types/keys/choices, and answer values. Multiple unnamed MathQuill blanks become distinct fields. |
| After each grade and during history | MA grading feedback and worked solution, compared with the actual submitted values | Source HTML and grade; separate solver verification/reconciliation records | Migration confirms each `:answer-field/correct` from source evidence and keeps our mathematical corrections separate. |

## Image

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Shared-context and part/solution reads | `<img>`, `<canvas>`, and relevant `<svg>` in the corresponding source element | `assets/manifest.json`, hashed files, and context/question extraction references | Relative SSD image paths in `:multistep/context`, question content, or answer values. |

## Completion and assigned problem

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| After the last part | `#finalScreen`, then `#finalScreen-doneButton` | `multistep-completed.html` (whole page), `multistep-completed.png`; completion flags | Confirms all saved parts have grades and solutions. Learner completion facts stay outside the content import. |
| After completion and history | Course progress, source topic/KP links, and captured part ordering | `knowledge-state/multistep-completed.json`; `content.json.shared_contexts`, `question_order`, `multistep_id`, and `title` | Original importer focused on question/KP content. Migration prepared 28 reusable multisteps, referenced through `:assigned-problem/content` with `:assigned-problem/topic-coverage`, and enclosing assignment activities. Those wrappers are schema translations, not additional MA-captured screens. |

# 4. Assessment

Process: select and inspect the assessment → save instructions before Start → record the fixed question set → capture and fill each question without individual grading → save the filled test → submit the whole test → record completion/progress → collect per-question feedback from completed history.

## Activity and instructions

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Selection, before Start | Queue `.taskTypeUnlocked = assessment`; link `/tasks/<task-id>/tests/<test-id>/start`; `.testDetails tr` with `.testFieldName` / `.testFieldValue`, including `Questions` and `Time Limit` | `assessment-queue.json`, with original card HTML and eligibility details; checkpoint `test_id`, `assessment_details`, and URL | Preserves observed title, test identifier, question count, and timing/eligibility evidence. Does not prove a complete reusable assessment definition. |
| Before starting the timer | `#screen` containing `#startButton` | `assessment-instructions.html`; saved start intent | Migration extracted instructional text into standalone `:tutorial/content` with a title. Instruction text is not a complete assessment activity or routing definition. |

## Question

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| After Start, before answering | `#questions > .question`, with `#question-N`; `#questionNavigator .questionButton` | `state.json.assessment_question_order`; `assessment-live.html` after navigator readiness | Saves the served fixed question set and page HTML for that attempt. The count must match the queue's `Questions` value. |
| Before filling each question | `.questionText`; `.questionGraphicFrame` / `#questionGraphic`; calculator instructions where present | `q-N-before.json/png`; checkpoint `before` | `:question/problem`, source `q-N` identity, and confirmed calculator requirement. |
| After filling, before whole-test submission | Actual choices/entered values in the question; complete test page | `q-N-entered.png`; checkpoint submitted values/options; `assessment-answered.html` | Submission evidence only. **There is no per-question after-answer grade at this point.** |
| After whole-test completion, in history | `/learn?taskId=<task-id>`; `.question[id^="question-"]`; `.questionKP` link `/topics/<topic-id>#<source-reference>`; `.questionDifficulty`; `.answerResult`; `.answerDetails`; `#questionExplanation-N` | `activity-metadata.json`, including `raw_html` and `details_html`; `history-q-N.json/png`; checkpoint `history` and `after` | Resolves each question's topic/KP, adds difficulty, and supplies the worked solution and answer evidence. Questions can span several topics. The history ID set must match the saved live set. |

## Answer field and Answer

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Before filling | Radio rows `.choiceLetterCircle` / `.choiceText`, select options, MathQuill blanks, or other supported inputs | `q-N-before.json.fields`: keys, types, choices, source HTML, and DOM bindings | `:question/answer-fields`; field key/type/choices and individual answer type/value. |
| At filling | Selected choice or entered value, checked against the actual field | Checkpoint submitted values/options; separate solver predictions and intended response | Preserved for audit, not migrated as learner responses or automatically accepted as correct answers. |
| Completed history | Source correct-response evidence, `.answerResult`, and expanded worked explanation | Saved history HTML, `activity-metadata.json.raw_html`, and separate verification/reconciliation records | Migration establishes `:answer-field/correct` from MA evidence. The script's normalized key can come from solver decisions; migration did not blindly replay those keys. `Full Credit` is normalized to `Correct`, while the source result is also retained. |

## Image

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Before filling and during history explanation reads | Question/choice/solution image and rendered math elements | Hashed asset files and manifest through the shared reader | SSD image references in question, solution, and answer content; no image bytes in EDB. |
| Instruction capture | `#screen` HTML | `assessment-instructions.html` | Raw source retained; this write does not itself run the shared asset-saving routine. Migration checks and resolves any instructional image references. |

## Completion and knowledge state

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Whole-test submission | `#submitTestButton`; `#confirmationDialog` | Submission-intent checkpoint and event record; the filled test was saved before confirmation | Checkpoints distinguish an unsubmitted test from an uncertain submission. They do not create content attributes. |
| Completion | `#finalScreen`, including the completed question count; Done button | `assessment-completed.html` (final-screen element), `assessment-completed.png`; completion flags and timing observations | Verifies the completed attempt matches the captured count. Results and elapsed times stay outside the content migration. |
| After completion and history | Course progress plus joined question records | `knowledge-state/assessment-completed.json`; `content.json.questions`, `test_id`, `assessment_details`, and other selection metadata | Reusable question content and introductory text were imported. A universal assessment question collection and complete assessment definition were not inferred from this attempt. No canonical examples were captured in the observed assessment layout. |

# 5. Diagnostic

Process: select the diagnostic and freeze the local answer/skip policy → save instructions → capture each adaptive question before answering or skipping → save available grading feedback → continue or handle retry → record the analysis page → join history to bind numbered positions to MA question IDs, topics, and knowledge points.

## Activity and instructions

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Selection | Queue `.taskTypeUnlocked = diagnostic`; link `/tasks/<task-id>/diagnostics/<diagnostic-id>`; course from `a#courseNameLink` / `a.courseNameLink` | `diagnostic-queue.json`, including card HTML; checkpoint `diagnostic_id`, title, course, and URL | Preserves source identifiers and course association. The task ID and diagnostic ID remain distinct. |
| Before Start: local configuration | Existing MA course `Topics.csv` or an explicitly supplied covered-topic snapshot; optional old-database question/topic binding | `diagnostic-policy.json`; `diagnostic-Topics.csv` or `diagnostic-covered-topics.json`; checkpoint policy | Controls whether the automation answers or skips. These classifications and policies are local decisions, not source-authored diagnostic routing, and were not imported as such. |
| Before Start: source instructions | `#initialScreen` with `#initialScreen-startButton` | `diagnostic-instructions.html`; start-intent checkpoint | Migration preserved introductory text as tutorial content. The instruction write itself does not download its images through the shared reader. |

## Question

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Before each adaptive response | `#questionContainer`; `.questionWidget-title` such as `Question 7`; `.questionWidget-text` and graphic elements | `question-007-before.json/png`; checkpoint `sequence_position`, `before`, and any observed `source_question_id` | Captures the actual question served. `007` is an attempt position, not an MA question ID or durable schema identity. |
| Before identity is fully known | IDs such as `questionWidget-choiceLetterCircle-N-...` or `selectList-N-...` can expose the MA question ID | Checkpoint `source_question_id` where available | Useful provisional source binding. A blank question may not expose a usable ID live; history establishes it later. |
| After answering/skipping, before Next/Done | `.questionWidget-result`; `.questionWidget-explanation`; `#nextButton` / `#doneButton` | `question-007-after.json/png` where a graded screen is available; checkpoint `after`, `actual_result`, and `live_result` | Captures feedback/solution evidence when present. The last response can navigate directly to analysis without a graded widget; history is then used to recover missing evidence. |
| Completed history | `.question[id^="question-"]`; `.questionNumber`; `.questionKP` source link; `.questionDifficulty`; `.answerResult`; `.answerDetails`; `#questionExplanation-N` | `activity-metadata.json`; `history-q-N.json/png`; rebinding in `state.json` and `diagnostic_question_order` | Matches each numbered live position to a real `q-N` identity, including blanks whose IDs were unavailable live. Resolves topic/KP membership and difficulty; expands solutions. Rejects mismatched IDs, counts, or duplicate bindings. |

## Answer field and Answer

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Before answering or skipping | Radio choices, `.selectList` / native selects, MathQuill blanks, and supported inputs within `#questionContainer` | `before.fields`, original choice HTML/values, generated keys, and field DOM bindings | The same owned answer-field and answer representation used for other questions. Fields are captured even when the local policy chooses to skip. |
| At response | `.questionWidget-submitButton` or `.questionWidget-skipButton`; entered/selected values when answering | Local decision/classification, submitted values, and intent checkpoint | Evidence of the automation's action. Neither a skip nor a solver answer establishes `:answer-field/correct`. |
| Feedback/history | MA field feedback and revealed solutions; history results can include `No Credit`, while live feedback can say `Skipped Question` | Saved original results, expanded history HTML, and verification records | Migration imports only questions whose complete original correct answers could be confirmed. Unconfirmed questions remain held; classifications and learner grades are excluded. |

## Step and adaptive sequence

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| During the diagnostic | Changing `.questionWidget-title` number; Next/Done; `#retryScreen-yesButton` / `#retryScreen-noButton` when a retry is offered | Numbered checkpoints, observed sequence, retry decisions, and final `question_order` | Preserves this attempt's adaptive path. It does **not** reveal all possible branches, a complete diagnostic definition, or verified reusable `:step/math-academy-id` values. We did not turn the observed path into an invented `:step/next` routing tree. |

## Image

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Live question/feedback and history explanation reads | `<img>`, `<canvas>`, and relevant `<svg>` in the captured question or explanation | Hashed `assets/` files, manifest, and extraction references | Copied/reused as relative SSD image references. Saved graded HTML can be re-extracted during recovery while reusing saved assets without fetching the original question again. |
| Instruction capture | `#initialScreen` HTML | `diagnostic-instructions.html` | Raw instructional evidence, later reviewed separately from the richer per-question asset capture. |

## Completion and knowledge state

| Stage | MA HTML source | Saved evidence | Schema / migration use |
|---|---|---|---|
| Diagnostic completion | `/tasks/<task-id>/diagnostics/<diagnostic-id>/analysis`; `.courseFrame` | `diagnostic-completed.html` (whole page), `diagnostic-completed.png`; completion URL/count and flags | Confirms completion through this diagnostic's analysis page. Learner placement results were not migrated. |
| After completion | Course progress page HTML and displayed topic colors | `knowledge-state/diagnostic-completed.json` | Observation only; no import of inferred mastery or internal diagnostic state. |
| After history binding | Source-confirmed questions, identities, topic/KP links, and explanations | `content.json.questions`, `diagnostic_id`, `course_id`, `question_order`, and local `diagnostic_policy` | Reusable question content and introductory instructions were imported. No canonical examples or complete adaptive activity definition were inferred. |

Across all five types, the original workflow saved its database preview, transaction, receipt, and verification under each task's `edb-import/`. Migration rebuilt transactions for the new schema/identities instead of replaying old numeric entity references. The 61 MA-original batches are committed through basis 132; supporting manifests, source evidence, held questions, and receipts are under [the newer-capture reference folder](edb-math/imports/math-academy/newer-captures/). Correction drafts remain separate for later attribution to the assistant.
