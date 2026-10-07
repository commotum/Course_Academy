# Multivariable Calculus diagnostic capture

Completed manually through Chrome on 2026-10-07. Task **14033238**, diagnostic **428723**, course **54**, account `multiwilliam` (WP). The diagnostic served 54 questions: 39 prerequisite answers were correct; 15 questions belonging to the requested course were skipped. Official activity-history topic IDs agree with every classification. The account remains enrolled in Multivariable Calculus at 0%, with all 187 displayed topic bands white.

Question 1 was source topic 2036, **Velocity and Acceleration for Plane Motion**, knowledge point 9819, **Finding the Time when a Particle Reaches a Particular Velocity**. It was a prerequisite, so answering it correctly followed the policy. Basic vector motion is distinct from the course's Newton's second law, vector-function calculus, and displacement-dependent acceleration topics.

The adaptive exam tests a sample and infers other knowledge. These observations establish the outcome of this run, not a guarantee that every prerequisite was directly tested or that every possible question was captured.

## Saved evidence

- [capture.json](capture.json): all 54 questions, complete live choices/fields, correct answers, submitted decisions, authentic worked solutions, original asset bindings, source topics, knowledge points, difficulties, and history provenance. It is a capture artifact, **not yet an EDB import payload**.
- [activity-metadata.json](activity-metadata.json): authentic source question IDs, numbered order, source topic/KP links, difficulty, grades, response timestamps and elapsed times in the original history DOM.
- [history-extracted.json](history-extracted.json) and [history-solutions-extracted.json](history-solutions-extracted.json): all 54 history problems and solutions.
- `question-NNN-before.{json,html,jpg}` and `question-NNN-graded.{json,html,jpg}`: live before/after evidence. JSON includes full DOM and rendered text. The first two graded extraction records were supplemented from authentic history; question 1's field normalization was reconstructed from its saved live DOM. The source evidence is retained.
- [assets-manifest.json](assets-manifest.json), `assets/`, and `inline-svg/`: original page image bytes, SHA-256 bindings and captured inline SVG markup. Asset bundles reported no failures. Every question/solution image URL resolves to a saved original asset.
- [analysis.json](analysis.json), `diagnostic-results.{json,html,jpg}`: official topic analysis. The same topic can appear under multiple courses; this duplication does not represent additional questions.
- [knowledge-state.json](knowledge-state.json): all 187 course-qualified topic rows and original progress HTML, using the existing white-to-zero display convention. This is displayed knowledge state, not exact internal FIRe values.
- `queue-before.json`, `queue-after.{json,html,jpg}`, and [proof-queue.jpg](proof-queue.jpg): enrollment, completion, and available course lessons. Initial lessons include vector-function domains, cylindrical coordinates, double summations, moments/center of mass, and Newton's second law.
- [state.json](state.json), [policy.json](policy.json), and `course-graph/`: decisions, checkpoints, course topic allowlist and the supplied graph files.
- [capture-verification.json](capture-verification.json): focused completeness, identity, policy, image-hash and topic-band checks.

Diagnostics exposed worked solutions, but no canonical-example role bindings. The capture preserves those solutions without relabeling them as canonical examples. No EDB import was performed, and no diagnostic runner code was changed during this manual run.

## Observed controls and transitions

| State | Observed selector / signal | Behavior |
| --- | --- | --- |
| Queue | `#task-14033238 .taskNameUnlocked` | Expands the placement-exam card. |
| Start link | `#taskStartButton-14033238` | Link `/tasks/14033238/diagnostics/428723`. |
| Instructions | `#initialScreen`, `#initialScreen-instructions` | Response time contributes to scoring; questions are timed independently; breaks belong between questions; leaving an unanswered question counts incorrect. |
| Start exam | `#initialScreen-startButton` | A DIV with START text. Starts the first question. |
| Live question | `#questionContainer.questionWidget` | Reused for every adaptive question; heading is `Question N`. Existing `dom.js` extracts the problem, complete choices, fields and displayed solution. |
| Progress | `#progressBarFrame`, `#progressBar` | Width changes with progress; no fixed total question count was shown. |
| Multiple choice | `.questionWidget-choiceLetterCircle`, `#questionWidget-choiceLetterCircle-{sourceQuestionId}-{letter}` | Click the actual visible option. IDs reveal source question identity. Display order must come from the DOM. Selected circle has a dark background. |
| Free response | `#freeResponseTextbox-1`, descendant MathQuill wrapper/textarea | Click the wrapper, then send text to the already focused field. With this Chrome control backend, `tab.typeText(null, value)` succeeded; direct locator typing and input preparation timed out. Two such fields were served. |
| Submit | `.questionWidget-submitButton` | Initially has `disabledButton`; enabled after selecting/filling. Submission returns immediately but grading DOM can arrive later. |
| Skip | `.questionWidget-skipButton` | Don't Know. Reveals **Skipped Question**, explanation, and Next. History records it as **Incorrect**. Keep deliberate skip separate from an accidental wrong answer. |
| Grade | `.questionWidget-result`, `.questionWidget-explanation` | Correct or Skipped Question plus worked solution. Save before navigating. |
| Continue | `#nextButton` | Requests another adaptive question. The first observation can still show the preceding question; wait for a changed question heading or completion URL. |
| Completion | `/tasks/14033238/diagnostics/428723/analysis#` | After question 54's Next, the server navigated straight to analysis. No separate Done action was needed. |
| Analysis | `.courseFrame`, `.courseHeader`, `.topic`, `.correctAnswer`, `.incorrectAnswer`, topic links | Topic-level results grouped under every course containing those topics. |
| History | Click `#task-14033238 .taskNameUnlocked` after completion | Navigates to `/learn?taskId=14033238`; exposes all 54 numbered questions. |
| History identity | `.question[id^="question-"]`, `.questionNumber`, `.questionKP` | Authentic source question ID and topic/KP binding `/topics/{topicId}#{knowledgePointId}`. |
| History grade/time | `.questionDifficulty`, `.answerDetails`, `.answerResult`, `.answerCreated`, `.timeElpased` | E/M/H, result, timestamp and response duration. `timeElpased` is the site's actual spelling. |
| History solution | `.questionExplanation[id^="questionExplanation-"]` | All 54 explanations were present; existing DOM extractor handles this container. |
| Topic bands | `.moduleTopics tr`, `.topicLink`, `.topicCircle`, `.unitNumTopics`, `#units` | Existing progress extraction works with course ID 54. |

The DOM also contained `#doneButton` and `#retryScreen-yesButton` / `#retryScreen-noButton`. They were not exercised in this run. Retry options offer another question from the same topic after a silly mistake, or moving to another topic after not understanding. Their interaction and recovery semantics still need a real observation; their presence alone does not prove support.

## Changes needed for unattended diagnostics

Implementation follow-up: [the diagnostic player](../../../../scripts/question_capture/diagnostic.py)
now implements this flow, with offline replay coverage. See the
[runner documentation](../../../../scripts/question_capture/README.md#placement-diagnostics)
for configuration and recovery. The observations and requirements below describe
the source state at the time of the manual capture.

1. **Queue recognition and dispatch.** `browser.py` currently recognizes lesson/review URLs, tests, and multisteps. Add the `diagnostic` kind and `/tasks/{taskId}/diagnostics/{diagnosticId}` route; route to a diagnostic loop rather than the whole-quiz submission loop.
2. **Adaptive question loop.** Capture the question before answering, choose correct/skip by membership in the configured course topic set, capture the grade/solution and assets, then Next. Do not require a fixed count, all question IDs upfront, a quiz deadline, or quiz correctness weighting. Diagnostics grade one question at a time.
3. **Topic classification while live.** The rendered question did not expose a topic/KP link before answering. Radio IDs expose question IDs; free-response fields did not. Use existing database question bindings when available, and mathematical skill matching to the course list otherwise. Retain sequence position and a problem fingerprint until history supplies authentic IDs. A missing early ID should not strand the question.
4. **Checkpoints and routine recovery.** Save question, decision, filled/submission intent, observed grade and Next intent. On resumption inspect the restored server view: continue an already graded question, restore a still unanswered question, or finalize the completed analysis/history. Check both completion and changed heading after Next so stale initial DOM does not cause duplicate answers. Do not refresh/navigate away from an unanswered diagnostic merely to inspect state.
5. **Skip-aware history and answers.** Reuse history extraction and source topic/KP binding, preserving the live skip decision alongside history's Incorrect grade. Recover the correct answer from the authentic worked solution for content capture. Do not trigger repair merely because the deliberate skip is Incorrect.
6. **Content import routing.** `database.py:content_topics` currently treats only assessment/multistep captures as containing multiple source topics. Diagnostics need that same topic-qualified content path. Keep the usual content-only transaction and learner-state preservation; deduplicate questions shared across course-analysis groups by source question ID.
7. **Completion snapshot and focused replay.** Snapshot course 54 after completion. Replay these fixtures for radio correct, deliberate skip, MathQuill free response, original image choices, delayed grade/Next, history supplementation and final analysis navigation. Retry overlays remain an unobserved case. There is no need for whole-database verification or repeated mid-question progress reads.

The main Foundations III worker was not restarted or reconfigured for this diagnostic. This folder is outside its normal saved-import sweep so incomplete diagnostic import support cannot disturb that worker.
