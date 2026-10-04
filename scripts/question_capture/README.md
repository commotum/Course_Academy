# Question capture

Run sequential Math Academy lessons, reviews, multisteps, required quizzes/assessments, and quiz retakes;
add captured **content only** to EDB.
The entry point is `python scripts/question_capture`; the code is self-contained
apart from Playwright, the EDB CLI, and a solver command.

MA can include the identical `/js/math-editor.js` tag twice in a page, causing
its `const OPERATIONS` declaration to fail on the second execution. Navigation
keeps the first tag and removes only repeated tags for that exact script URL.
The editor code and answer interactions remain the site's original code.

The runner:

1. Reads existing lesson scores without filtering personal task status, and
   calculates directed scores for offered lesson and review topics from your study targets
   and assignment mappings, even if no personal task exists. The scoring follows
   `engine/rust/learning.rs`: target reach, remaining prerequisite work, distance
   to targets, and assignment deadlines. The capture account's latest knowledge
   snapshot determines which branches need further preparation; it never credits
   that work to your personal learner. Curriculum and target configuration are
   read once per invocation at one database basis. The runner takes the highest
   score among eligible lessons and reviews actually available in Math Academy's visible queue.
   When no scored activity is available, it takes the
   first new review in the visible queue. If no review is available, it takes the
   first remaining activity in visible queue order, including an unranked lesson.
   Already captured tasks and completed lesson topics are skipped.
   It refreshes and logs the queue after every completed activity, including the
   last activity allowed by `--limit`, and uses that observation for the next
   selection. Assessments, including quizzes, and in-progress tasks are also
   logged, with their observed URLs, IDs, progress, and assessment details.
   Assessments have their queue details expanded and saved, including test ID,
   time limit, question count, exact Notes text, and the remaining optional-XP
   allowance. An optional quiz stays queued while other activities continue.
   A required assessment takes precedence and runs automatically. A notice with
   zero XP remaining or explicit required wording establishes that requirement.
   Quiz retakes also run as soon as they appear, ahead of lessons and reviews.
   The runner recognizes the `(Retake)` title or the quiz-retake Notes text,
   checks the question count and time limit, and uses the same quiz player.
   Retake status and the exact Notes are saved in the queue, checkpoint, and content capture.
   Required quizzes can also omit Notes: a sole queued assessment with complete
   question-count and time-limit details and no Notes row is treated as required.
   This is checked again before Start; other unknown layouts stop before starting.
   Multisteps are supported in the remaining queue order, including their task
   and multistep IDs and original queue card HTML.
   In-progress captures require explicit recovery. Lessons and reviews compete
   by topic capture priority; the highest scored eligible activity is selected.
   Equal scores prefer the lower topic ID, then a lesson over a review of that
   same topic. Unscored reviews retain queue order as a fallback.
   `selection/capture-priorities.json` records score
   components and the snapshot/configuration basis used.
   It does not change EDB task priorities or statuses.
2. Captures each canonical example live. For each KP it randomly chooses
   `C-W-C-W-C` with probability **0.7**, or `W-C-W-C-C` with probability **0.3**.
   It captures each practice problem and locally observed answer widgets before
   submitting, then captures the result and revealed worked solution. It checks
   every grading result before continuing.
   If a live lesson introduces a new KP title, its example establishes a stable
   identity within that topic. The content import adds the KP and topic membership
   only with that captured example and a nonempty matching practice pool. Existing
   example identities and ambiguous titles remain guarded.
   Reviews use the same `C-W-C-W-C` / `W-C-W-C-C` patterns and 70/30 weights,
   with one saved pattern across the whole review because questions can switch
   KPs. If the site continues beyond five questions, that same pattern repeats;
   `--review-question-limit 20` bounds unexpected continuation. Site completion
   remains authoritative. An interrupted activity keeps its already chosen patterns.
   A negative-XP lesson or review overrides this policy on its next offered
   attempt: every answer is intended to be correct. The runner reads negative-XP
   cards from activity history as well as completion messages, and persists the
   obligation in `.local/question_capture/perfect-retakes.json`. Only a completed
   all-correct retake clears it; rereading the old failure does not re-arm it.
   Lessons can then finish after two correct answers per KP, and reviews after
   two correct answers overall. This favors progression over question quantity.
   The rule applies separately to each topic's lesson/review attempts and does
   not change personal learner state in EDB.
3. Opens the completed activity, expands the explanations, and joins all question
   IDs to KP titles and source E/M/H difficulty labels. It checks that the live
   and activity question sets and KP mappings agree.
   Review history uses `.reviewAnswerList .question` and a per-question
   `.questionKP` source link. Each link must belong to the selected topic, and
   its title must match exactly one of that topic's database KPs. It captures
   whatever questions were served; reviews do not require five per KP or a live
   canonical example. An unknown review tutorial/example layout defers the activity for inspection.
   Assessments use their fixed question count and one whole-test submission.
   Each new question independently selects an intended correct response with
   probability **0.8717** and an incorrect response with probability **0.1283**.
   This also applies to quiz retakes. A wrong radio/select response chooses a
   distinct displayed distractor; a blank uses the solver's validated incorrect
   value. Questions with several fields make one field wrong. The correct/wrong
   intent and chosen distractor are saved before entry and retained on resume,
   even if options move. `--assessment-correct-weight` changes the probability;
   `1` restores all-correct quizzes. The weight is saved per activity, and it
   determines probabilities rather than guaranteeing a particular final score.
   The solver continues to identify the correct answer. Incorrect graded answers
   are checked against the revealed worked solution before importing content.
   All live fields, displayed choice ordering,
   images, calculator instructions, and entered answers are captured before
   submission. Their history supplies explanations, difficulty, and per-question
   topic/KP links. Each KP title is matched within that question's source topic;
   assessments can span several topics and import in one guarded transaction.
   No canonical examples were presented by the observed Quiz 5 layout.
   Multisteps answer every ordered part correctly. They save shared setup and
   diagrams before answering, support multiple unnamed MathQuill blanks, and
   capture each grade and explanation before Continue. Their activity records
   supply topic/KP links and difficulty just like assessments. All parts use one
   solver session. Each imported question includes the setup and earlier parts
   with confirmed answers, so references such as “part 5” remain understandable;
   the capture also keeps each original stem and its order separately. The
   existing question/KP import is reused; no activity or learner entities are
   created. Unrecognized intervening context layouts stop for inspection.
4. Matches `q-N` and `e-N` globally in EDB. Adds missing attributes and choices,
   reuses existing owned answer entities, and links new practice to the correct
   `knowledge-point/questions`. Existing populated attributes are preserved.
   Conflicting correct answers, field types, KP ownership, or canonical example
   IDs stop the import for review.
   Worked-example roles come from `knowledge-point/canonical-example` references,
   and canonical targets are excluded from every KP practice pool. `q-N` / `e-N`
   distinguish MA source ID namespaces, not database roles. Captures omit
   `is_example`; saved payloads and checkpoints have been migrated, and imports
   reject that retired field. Captured `canonical_examples` supply the observed canonical references,
   while `questions` supply practice membership. The retired `question/is-example`
   attribute is never written. Having a worked solution alone does not make a
   practice question canonical.
5. Previews a content-only transaction, commits with a basis guard and stable
   request key, and verifies that all learner and engine facts are unchanged
   across that exact transaction. It also verifies that a repeated import would
   produce no further changes.

It saves one snapshot of all three course progress pages **after each completed
activity**. There are no new baseline or mid-activity checks. The snapshot is
compared with the preceding completed activity's snapshot when available.
Existing snapshots from older runs remain preserved. Reads are sequential and
use randomized navigation pauses: three page reads per completed activity.

Each `knowledge-state/<event>.json` contains every topic row from courses
113/111/136, its source ID, title, color, mapped display band, module and topic
number, the source `#units` HTML, per-course timestamps, and changes since the
previous snapshot. Shared topics remain qualified by course, so conflicting
colors are retained. Unknown colors or an incomplete topic count defer the activity.
Use repeated `--progress-course-id ID` options to override the three-course scope.

These files capture the **full displayed profile for those courses**, not MA's
complete internal learner state. The rows do not expose exact continuous FIRe
repetitions, memory, intervals, or ability. White-to-0 and blue-to-1–6 follows our
existing initialization convention; darkest-to-6 is an assumption. Unchanged
bands do not prove the underlying values stayed unchanged. Progress snapshots
are saved separately and never transacted into EDB learner state.

The manual review captured on October 3, 2026 ended after two consecutive
correct answers across different KPs. The runner waits for the site's completion
screen and verifies it says the review completed; it does not declare completion
from a predicted question count. Two-consecutive-wrong termination was not tested.

## Run

The existing MA Python environment already has Playwright 1.58 and Chromium:

```bash
CAPTURE_PY=/home/jake/Developer/MA/.venv/bin/python
"$CAPTURE_PY" scripts/question_capture login
"$CAPTURE_PY" scripts/question_capture run --dry-run
"$CAPTURE_PY" scripts/question_capture run --limit 1
```

`login` opens a dedicated visible Chromium profile. Sign in there and press Enter
in the terminal. Its credentials stay under `.local/question_capture`, with
owner-only permissions. No login credentials or cookie values are logged or
included in solver requests. Alternatively, `--browser-spec chrome` imports only
Math Academy cookies through the original MA pipeline's `cookiekit`. This is
optional and depends on that helper's browser/decryption dependencies.

`run` **answers questions on Math Academy and commits EDB content by default**.
`--dry-run` only inspects the queue and priorities. `--preview` still takes the
activity but previews its database transaction without committing. Default limit
is one activity; use `--limit N` for a bounded sequential batch. A required review or assessment
counts toward that limit. For example, `--limit 2` permits a review followed by a
lesson if completing the review makes a ranked lesson available. The queue and
EDB priorities are read afresh between activities. Each observation prints the
activity titles, types, task/topic IDs, and any lesson priorities. Post-activity
observations are saved as `queue-after.json` in that activity's capture directory;
all observations are appended as `queue_observed` events in the local journal.

To use a different Python environment, install `requirements.txt` there and
install its Playwright Chromium browser if needed. No dependencies were added to
the main application environment.

The default learner is `59d5cf13-351c-4114-be19-4c3bb64ee051`. Override it with
`--learner-id`. Database defaults match this project's local EDB service; override
`EDB_POSTGRES_URL`, `--database`, `--edb-bin`, and `--endpoint` as appropriate.
All paths work when invoked from this repository root.

## Solver

The default adapter keeps **one Codex session per activity**, for both lessons
reviews, multisteps, and assessments, including verification turns. The first question starts `codex exec`;
subsequent calls use `codex exec resume <SESSION_ID>` with that explicit saved ID.
The CLI process exits between calls, but its persisted conversation carries forward.
It never uses `--last` or silently starts over if a resumed session has a different ID.

Each turn receives the current problem, locally observed fields and choices,
and its screenshot, along with newly captured canonical examples (including their
saved screenshots) and newly
revealed worked solutions from that activity. Grading feedback distinguishes
intentional wrong submissions from solver errors. Examples and feedback are
sent once, then retained in the session; changing KPs does not reset it. Current
choice letters and ordering must always be checked anew.

Structured output and a read-only working directory are retained. The persistent
working directory and session checkpoint are under the activity's
`solver-session/`; the Codex transcript uses normal CLI session storage. It uses `--ignore-user-config` so
project instructions, configured connectors, and custom tools do not influence
the solver. It does not set a model unless `--solver-model` is supplied. It needs
an authenticated Codex CLI and consumes model usage. The structured-output
interface follows the [official noninteractive documentation](https://learn.chatgpt.com/docs/non-interactive-mode).

The solver must identify the correct answer even when the runner intends to
submit a wrong answer. The runner picks a different radio/select choice or types
the solver's explicitly incorrect blank value. After an incorrect submission,
the solver rechecks the correct answer against the revealed worked
solution. Correct submissions are confirmed by the site's grader.
Radio choices are clicked by their observed choice-circle IDs, using the displayed
option token from the solver. The actual highlighted letter is checked before
Submit. Graph filenames do not determine displayed order. Native select and
blank values are also checked before submitting; the entered screenshot and
checkpoint retain the selection for recovery.

Use `--solver-command 'python3 /absolute/path/solver.py'` to substitute a solver.
It receives JSON on stdin (`mode`, `problem`, `worked_solution`, `fields`, `activity_context`,
`screenshot`) and must emit JSON matching `solver.py:SCHEMA` on stdout. Commands
are parsed as argument lists, never executed through a shell. A custom command
manages its own session persistence; its activity context contains all available
examples and grading feedback. Uncertain results
or invalid choices stop before submission.

The extractor supports observed radio circles, native blanks/selects, MathQuill
answer wrappers, and the original `.selectList` widget. MathQuill entry uses
explicit typed characters, arrow-key events, and visible symbol-menu buttons.
The runner focuses each editor's keyboard input when switching fields, so a
floating toolbox over the next answer box cannot intercept a mouse click.
Named symbols such as π use the displayed toolbox when available, with explicit
backslash commands as a fallback. The runner checks the existing editor's value
through MathQuill's public read-only `.latex()` getter before Submit; it never
sets answers through the widget API. The checkpoint retains observed LaTeX,
typing actions, and any symbol buttons used.
Verification accepts editor formatting such as `\left`/`\right`, fraction-style
commands, and numeric rational exponents written as `^{1/3}` or
`^{\frac{1}{3}}`, while preserving fraction and exponent grouping and symbol identity.
Numeric measurement answers also reconcile legacy suffixes such as `32ft^{2}`
with `32\,{\text{ft}}^{2}` for recognized units, preserving the quantity, unit,
and exponent. Plain text answers remain exact. When changing fields briefly leaves
two symbol toolboxes visible, the runner waits for the previous toolbox to hide,
then clicks the single visible button. Persistent ambiguity stops before Submit;
keyboard commands are a fallback only when no matching button is visible.
The existing editor's value must still verify before Submit.
Unknown widgets, unreadable formulas, and unrendered graphical assets defer the
activity for review. Formulas supplied only as SVG paths are preserved as rendered
formula images in the problem and worked solution. Invisible MathML `mphantom`
content is omitted. Graphics are allowed to
become visible and images must finish loading within `--timeout-ms` before capture;
an asset that never renders saves diagnostics and defers that activity.
Radio extraction is validated against all fifteen actual Sum Rule
widgets; native mixed fields have fixture tests. Offline keyboard tests use the
exact public MathQuill distribution loaded by Math Academy and cover π menu
clicks, command fallback, incorrect-answer entry, and fraction grouping. The
custom-select path still needs validation on a live activity. A solver error can break the intended
five-question sequence; an unexpected grade defers that activity before another
answer, then the runner selects another available activity.

## Pacing inherited from the original pipeline

Sources:

- `/home/jake/Developer/MA/PIPELINE/Math-Academy/0-Ingest/1-Course-Source/course-source.py`
- `/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/2-Topics/topics.py`

Both use uniform random waits, sequential captures, saved progress, bounded
retries, and periodic rests. Their topic/course interval is 10–25 seconds and
their longer rest is 120–360 seconds every 20 captures. The original per-section
read pacing is 0.2–0.8 seconds; this interactive runner uses longer pauses:

| Event | Default uniform wait |
| --- | --- |
| Navigation, field selection, Continue, history expansion | 0.8–2.5 seconds |
| Total answer budget, crediting Codex solving time; only the remainder is waited before Submit | 5–12 seconds |
| Between activities | 10–25 seconds |
| After every 20 activities when more remain | 120–360 seconds |
| Retry a failed read-only navigation | 30/60 seconds plus 0–5 seconds jitter |

Each range has `--event-min/max`, `--answer-min/max`, `--lesson-min/max`, or
`--rest-min/max` overrides. `--rest-every` controls periodic rests. `--seed` makes
draws reproducible for investigation; it does not change the 70/30 default.
Random delays reduce request frequency; they do not guarantee a site considers
automation acceptable. There are no parallel browser captures or direct calls
to private endpoints. HTTP 401/403/429 and challenge pages stop the run. Submission
and Continue actions are never blindly retried.

## Saved data and recovery

Artifacts go to `reference/mathacademy/question-capture/<taskId>/` by default:

- Source DOM JSON, formula data inside its HTML, and before/after screenshots.
- Original images from browser-observed responses, with source URLs, hashes, and
  local paths in `assets/manifest.json`. Identical bytes under different URLs reuse
  one file. Canvas, inline SVG, or an unavailable original response uses a rendered
  capture, explicitly marked in the manifest. No extra image requests are issued.
- Canonical examples, activity metadata, and `content.json` for import.
- Assessment queue notice/eligibility, start instructions, fixed question IDs,
  filled test HTML, and completion result. These source facts are saved in the
  queue observation, `assessment-queue.json`, and assessment `content.json`.
- `state.json` with chosen sequences and a checkpoint before every submission.
- `solver-session/state.json` with the activity's Codex session ID, delivered
  context, and pending turn checkpoint; question directories retain solver events
  and inputs/outputs. Completed answers are reused on restart. An interrupted
  solver prompt resumes in the same confirmed activity session; uncertain website
  submissions are never replayed unless an explicit resume reloads the activity
  and confirms the same radio question is unanswered, with no selected choice,
  no pending request, and a disabled Submit button. That evidence is journaled.
- `knowledge-state/` with a full displayed course profile after activity completion.
- EDB reads, `transaction.edn`, preview, exact commit intent, receipt, matching
  report, and verification under `edb-import/`.
- `diagnostics/<timestamp>/` on activity failures: exception and full traceback,
  source hashes, configuration, checkpoint, last observed queue, page URL, DOM,
  screenshot, current question extraction, recent browser console/JavaScript/network
  errors, and subprocess stdout/stderr when
  supplied by the exception. Each browser artifact is collected independently;
  failed diagnostic reads are listed in `error.json`.

Each invocation also writes a persistent run log to
`.local/question_capture/logs/run-<timestamp>.log`. Activity errors, including
solver, entry, extraction, history, snapshot, and database import failures, save
diagnostics, mark the task with `deferred_error` in `state.json`, and continue
other available activities. Deferred tasks are excluded from automatic selection
across invocations until selected with `--resume`. `--limit` bounds attempted
activities, including failures. A deferred import retains completed content and
its original transaction/commit checkpoint.

Authentication, access blocks, challenges, and user interruptions stop the batch.
If the queue cannot be read or another task cannot be selected, the runner saves
diagnostics and ends the batch. Submission and Continue actions are never retried
as part of failure handling.

Attempt results are retained only to audit the intentional capture sequence.
They are never transacted into learner tasks, timing, responses, or ability.
Canonical examples normally expose no answer widgets or difficulty; those facts
remain unknown and are listed as missing source fields. This runner does not
invent canonical answer fields, difficulty ratings, or practice distractors.

The normal command automatically resumes a single unfinished saved capture or
import that has not been deferred, before selecting a new activity:

```bash
"$CAPTURE_PY" scripts/question_capture run --headless --limit 1
```

Use `--resume reference/mathacademy/question-capture/TASK_ID` to select a run
explicitly. If several unfinished runs exist, they are left for explicit recovery
while the runner selects new activities.
`run --dry-run` reports a pending capture without starting a browser or answering.

Assessment recovery retains one solver session and reuses solved answers,
matching them to current displayed options before refilling the unsubmitted test.
New quizzes, assessments, and quiz retakes target a random **70–85% of their
time limit** by default: about **10.5–12.75 minutes for a 15-minute quiz**.
One saved schedule allocates uneven time to each question. The runner waits
before entering each new answer, counting actual solving, navigation, and entry
time toward the total. These are real waits; recorded durations are not edited.
It shortens or skips extra waits when the visible countdown or remaining question
count leaves too little time. It keeps a final submission margin and checks for
shutdown every 30 seconds during longer waits. Slow solving can exceed the
target, so this is pacing rather than a guaranteed completion time.
Use `--assessment-time-min` and `--assessment-time-max` to change those fractions;
set both to `0` to disable added quiz pacing. A saved plan survives interruption,
and already filled questions do not wait again. Older in-progress captures
without a pacing plan continue under their original timing policy.
The site's timer continues during an interruption. An uncertain whole-test
submission is inspected for a completion screen and is never blindly confirmed
again. Unknown question counts, navigation layouts, and requirement wording stop
before starting or submitting. A completed assessment's snapshot/import can resume
without retaking it. The usual 70/30 lesson/review patterns do not apply to quizzes.

Checkpoints preserve chosen patterns, captured questions, grades, and pending
Continue actions. A restored graded question is advanced without being answered
again. Completed solver results are reused and rematched by value if the site
reshuffles choice letters. Solver events stream to disk. Ctrl+C and SIGTERM request
a stop at a safe capture checkpoint instead of raising inside a Playwright wait;
a read-only solver turn may finish before the stop. The saved activity session ID
is retained. The supervision launcher allows 60 seconds for shutdown, then stops
only its isolated capture process group if needed. A confirmed completed turn can
be recovered without another model call. An incomplete read-only solver prompt
can be repeated in that same session.

If submission may have occurred, resume reads its grading result rather than
sending the answer again. If the site cannot establish the result, the checkpoint
remains available for inspection and the task is deferred. An unconfirmed solver
session ID also defers the task instead of resetting its context. Explicitly resumed
completion snapshots and content imports recover without retaking the activity. Previous per-step snapshot
checkpoints are migrated to Continue checkpoints without another mid-activity fetch.
When a restored page has moved past a pending submission, the runner reconciles
its complete saved after-capture before answering the next question. Incomplete
saved results defer the activity for recovery. Unexpected grades also defer the activity;
reviewed checkpoint repairs preserve the intended answer, actual entry, and grade.

Import or retry already captured content without visiting Math Academy:

```bash
python3 scripts/question_capture import-saved --content /absolute/path/content.json --preview
python3 scripts/question_capture import-saved --content /absolute/path/content.json
```

After a commit timeout, preserve `commit-intent.json` and `transaction.edn` and
retry the same command. The original payload, database, endpoint, basis guard,
and request key are reused. A definitive stale-basis rejection requires a fresh
plan after checking that no commit occurred; unresolved intents are never
silently replaced. Completed captures are journaled separately from imports,
so an EDB failure does not cause the activity to be retaken. Reviews are tracked by
task ID and do not mark their topic's lesson as already captured. Legacy lesson
checkpoints and journal entries remain supported.

## Validation

```bash
"$CAPTURE_PY" -m unittest discover -s scripts/question_capture -p 'test_*.py' -v
python3 scripts/question_capture import-saved --content reference/mathacademy/sum-rule-13925458/content.json --preview
```

Tests use saved real lesson/review DOM and EDB snapshots. Offline progression
checks cover five-question lessons, both shared review patterns, activity joining,
original image capture, and correct KP mapping. Recovery checks cover interrupted
post-submission extraction of the real complex-argument explanation (including
`mphantom`), delayed graphics, and recovery of its correct grade without resubmission;
they also cover interrupted
Continue, completion snapshot failure, automatic unfinished-run discovery, completed
solver-answer reuse, reshuffled choice letters, and interrupted CLI turns retaining
the same session. A local toy subprocess verifies streamed events survive a timeout
and its process stops. Grading and selected-option mismatches prevent another
submission in that activity. Runner tests inject start, capture, history, and
import failures, verify diagnostic preservation and selection of the next task,
and check that access blocks and interruptions stop the batch. Fixture tests never make model calls.
The real six-part pool multistep fixture covers shared diagrams and context,
seven unnamed MathQuill fields, square-root entry, source explanations and
synthetic-division tables, six topic/KP mappings, and one content transaction.
Prepared-answer and post-submission interruptions resume without replaying grades;
completion recovery does not take the activity again.
The saved Quiz 5 fixture also covers eight-question assessment capture, radio
images whose filename order differs from displayed letters, two real MathQuill
blanks, all source explanations, original images, multi-topic content planning,
optional-XP notes loaded on queue expansion, and uncertain-submission recovery.
Perfect-retake tests cover two correct answers per lesson KP and per review,
negative-XP discovery, persistence, and clearing only after a successful retake.

No live activity or database commit is performed by these fixture tests. The
standalone automator completed live lesson **13831128**, Determining Continuity
from Graphs, on October 3, 2026: fifteen practice questions, three canonical
examples, 45 original images, and 22 full progress observations. One solver
session handled all 21 solving/verification turns. The import created twelve
questions and enriched three, committing basis 305 → 306 with all 4,614 protected
learner/engine facts unchanged and a no-op reimport. See
`reference/mathacademy/question-capture/13831128/README.md` and its verification
files. That historical test included per-step snapshots. Current runs capture one
completion snapshot per activity. String learner-ID lookup and initial loading
placeholders are handled; solver duration is credited toward the answer budget. The review path still relies on
the earlier manual review and offline fixtures; it has not yet been run live by
the standalone automator.
