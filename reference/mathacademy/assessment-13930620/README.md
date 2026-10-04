# Quiz 5 assessment capture — 13930620

Completed October 3, 2026 at 8:51 PM America/Los_Angeles. Test ID 589340, course Mathematical Foundations II (111). Eight questions, 15-minute limit. All eight answers were correct: 100%, 15 XP plus 3 bonus XP. No canonical examples were presented.

`content.json` contains all eight problems, source worked solutions converted to Markdown/TeX, source difficulty labels, exact topic-scoped knowledge-point UUIDs, all observed answer fields and choices, correct values, calculator instructions where present, and provenance. Six questions are radio fields with five choices each; two are MathQuill blanks. Answers are independently solved and verified against Math Academy's Correct grades and explanations. These are agent-submitted answers, not evidence of the learner's unaided performance.

| Question | Topic / source KP | Difficulty | Field | Submitted answer |
| --- | --- | --- | --- | --- |
| q-98107 | 512 / 8660 | Easy | Radio | a: 6 |
| q-82938 | 167 / 3158 | Easy | Radio, images | c: clockwise 53° from positive x-axis |
| q-148499 | 3944 / 10460 | Moderate | Radio | e: (4x+1)/(x−3) |
| q-288831 | 729 / 18864 | Easy | Blank | 7x²−63x+105, with =0 supplied by the question |
| q-323219 | 757 / 5767 | Hard | Blank | 6 |
| q-74721 | 893 / 6224 | Easy | Radio | b: 4.02 |
| q-41570 | 437 / 5128 | Moderate | Radio | a: (8a+3)/(a−7) |
| q-66438 | 895 / 7517 | Moderate | Radio | c: x=1±(√3/3)i |

## Original evidence

Each `question-…-live.json` preserves the question HTML, assistive MathML, field markup, displayed choice identifiers/order, and image URLs; each has a screenshot. Blank answers also have answered HTML. `assessment-initial.html` and `assessment-answered.html` retain the complete live document before and after answering. `answers.json` records selected answers and reasoning. `activity-questions.json`, `activity-collapsed.html`, and `activity-expanded.html` retain source metadata and every source explanation. `completion.html` and `completion.png` show the 100% result; `activity-expanded.png` shows the expanded history.

`assets/manifest.json` maps seven question/explanation image URLs to permanent local files with SHA-256 hashes. The angle question's explanation reuses the same URL and bytes as its correct displayed choice c (`q-82938-a-1`). The complex-argument explanation adds `q-74721-e-0`. Image filenames were not used to infer correct choices; the displayed angle diagrams were inspected. The original browser asset bundles and inventories are retained in `live-assets/` and `history-assets/`; their original temporary paths are provenance, while `assets/` contains permanent copies.

## Assessment UI observations

The assessment has a fixed eight-question set and one whole-test submission, rather than per-question Submit/Continue grading. Live questions use `#questions > .question` and `#question-<ID>`; only the current question is displayed. Radio selectors are `#question-<ID>-choiceA` through `choiceE`, and the selected circle gains `.selectedChoice`. Choices use `.choiceText`; their letter and graphic URL must be captured together because image numbering and displayed letters differ. Math blanks use `.matheditor-wrapper-answer`, wrapping `.mq-editable-field`, `.mq-root-block`, and a textarea. The wrapper DOM ID is local to its question and should always be scoped by question ID.

Navigation controls are `#prevButton`, `#nextButton`, and `#submitTestButton`. Answer counts appear in `#questionsAnswered`, and the remaining timer appears in `#timeRemaining`. Submit Test opens a confirmation dialog. The result screen gives the total score and XP. Activity history at `/learn?taskId=13930620` supplies per-question difficulty, grade, timestamp/elapsed source metadata, and `.questionKP` links of the form `/topics/<topic>#<source-KP>`. Clicking `.answerDetails` reveals `#questionExplanation-<ID>`. All eight explanations were expanded and saved.

## Knowledge snapshot and database matching

One post-completion snapshot covers courses 113, 111, and 136: 357, 360, and 323 topic rows respectively, totaling 1,040 course-qualified rows. `knowledge-state-completed.json` maps white/blue display colors to local bands 0–6. Raw course JSON and HTML are retained. No baseline or mid-assessment snapshots were taken. The courses were read sequentially; these display bands are not exact continuous repetitions or the full internal knowledge state.

Read-only EDB matching at basis 322 found q-66438 already present; the other seven IDs were absent. All eight knowledge points matched by exact title within their source topics. `database/` retains the queries, results, and matching report. No database transaction, learner-state write, or automator-file change was made. Captured metadata remains in evidence files; `content.json` contains question content only. The assessment shape has multiple topics and is not assumed to work with the current single-topic `import-saved` path without checking it first.

`prepare_capture.py` reproduces normalization and completeness checks entirely from these saved files. `read_database.py` performs read-only matching; it never transacts. `verification.json` records capture counts and validation results.
