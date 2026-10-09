# Question capture

Run sequential Math Academy lessons, reviews, multisteps, placement diagnostics, and eligible quizzes/assessments;
add captured **content only** to EDB.
The entry point is `python scripts/question_capture`; the code is self-contained
apart from Playwright, the EDB CLI, a solver command, and the native comparison helper.

## Multiple account workers

From the repository root, start every configured account and attach to tmux:

```sh
./scripts/ma-workers start --attach
```

The installed terminal shortcut `cap` runs this same command. It is linked from
`~/.local/bin/cap` to `scripts/cap` and accepts additional Start options.

`workers.json` provides four permanent windows in session `ma`, in this order:
**Mathematical Methods**, **Linear Algebra**, **Multivariable Calculus**, and
**Differential Equations**. Unconfigured accounts have idle windows and are skipped
by Start. Saving the two remaining profiles is all that is needed to enable them;
the same Start command then launches all four. Repeating Start leaves active
workers alone. An unrelated process in a course window is also left alone.

The Methods account retains the `foundations` worker ID and its existing
`.local/question_capture` profile,
checkpoints, logs and `reference/mathacademy/question-capture` output. The other
workers each use `.local/question_capture-workers/<worker>/` and
`reference/mathacademy/question-capture-workers/<worker>/`. Their browser profiles,
capture locks, solver and repair sessions, pacing, retry ledgers and knowledge
snapshots are separate. All workers import content into the same EDB using its
existing bounded stale-basis retry handling. Verified captures in all four output
roots can supply provenance evidence. Only installation of tested shared source
repairs takes a short shared lock; solving and ordinary imports remain concurrent.

Mathematical Methods for Physical Sciences I (`commotum`, course 154),
Linear Algebra (`linearharrison`, course 55),
Multivariable Calculus (`multiwilliam`, course 54) and Differential Equations
(`differentwalker`, course 61) have saved and verified profiles.
Workers run headless from those
profiles, independently of the account currently signed into everyday Chrome.
Cookies are copied only when explicitly saving a profile, rather than at every
worker startup. All workers discover progress scopes from their account's Learn
sidebar after activity completion, then visit each course once. Unit links are
deduplicated into `/courses/<id>/progress`; these pages include every unit's rows,
including collapsed units. No account-specific progress list is needed.
Verified scopes are Methods 154/105/106, Linear Algebra 55/105/106,
Multivariable Calculus 54/106/55, and Differential Equations 61/55/54.
Previously saved completion snapshots remain unchanged. Explicit
`--progress-course-id` or `--progress-url` arguments still select a fixed scope.
Every account uses its own diagnostic topic graph. Methods answers only topics in
the union of the Foundations I, II, and III `Topics.csv` files, frozen with their
source hashes in `.local/question_capture-fleet/methods-foundations-only/covered-topics.json`.
Its placement exam skips every other or uncertain skill; progress colors and credit
from a previous diagnostic do not add topics to that list.

To add an account, sign into its enrolled course in Chrome, then run the matching
command. These examples use Chrome's `Default` profile; replace it with the actual
Chrome profile directory if different:

```sh
./scripts/ma-workers save-profile linear --browser-spec chrome/mathacademy.com:Default
./scripts/ma-workers save-profile differential --browser-spec chrome/mathacademy.com:Default
```

Save one account at a time while Chrome is signed into that account. The helper
checks the enrolled course, discovers its course ID and saves only Math Academy
cookies into the worker profile. `save-profile multivariable` uses the same syntax
if that account later needs a fresh login. Profile data stays in ignored local
directories; no cookie values are printed.

The Methods window has a status pane refreshed every five seconds, showing
four course cards with running/readiness state, daily earned/base XP, counts of
completed lessons/reviews/quizzes/multisteps/diagnostics, daily unique database
questions added and existing questions captured in verified imports, course
percent and a progress bar, and the last 20
completed activities' earned-XP bars. Bars run oldest to newest and use an
XP scale per course, with the range shown; downward arrows identify XP penalties. Database counts use committed
receipts and are cached locally; dashboard refreshes make no database queries.
Finished captures show COMPLETE after import, HISTORY PENDING when explanations
still need recovery, or IMPORT PENDING when only the database import remains.
A recovered live worker shows RUNNING without retaining
its previous deferred label. Saved graded captures reconcile interrupted checkpoint updates
when the server has already advanced.
History preserves No Credit separately from Incorrect and recovers its correct
answer from the revealed solution. A staged proof's first terminal Incorrect
submission can bind to history's No Credit only when its saved stage, submitted
values and terminal observation identify that same question with no accepted
fields. Both original grade labels are retained; later failures and partial
credit remain distinct. Diagnostic pacing credits capture and solver
time toward the answer delay.
An exhausted queue shows **BLOCKED**, with its waiting task IDs and saved reasons
in `status --json`, even though the process remains available to poll for new work.
This is recorded only after repair and saved-resume selection find no eligible work;
ordinary solving and pacing remain RUNNING. Wait records belong to the capture
process and are cleared when it resumes work. Intentional shutdown shows **STOPPED**,
including any blocked queue, without claiming that recovery is ready.
The tmux status bar also shows running, ready, unconfigured, blocked and stopped counts.
Use **Ctrl+b then n/p** to switch course windows and **Ctrl+b then d** to detach;
detaching leaves workers running. Additional commands:

```sh
./scripts/ma-workers status
./scripts/ma-workers check foundations multivariable  # Reopen saved logins; no activities
./scripts/ma-workers start --dry-run                 # Inspect queues/resume checkpoints only
./scripts/ma-workers stop                            # Request checkpoint shutdown for all
./scripts/ma-workers stop multivariable              # Stop one account
./scripts/ma-workers start multivariable             # Start/resume one account
./scripts/ma-workers attach                          # Attach without starting workers
```

Linear Algebra's 42-question placement diagnostic has completed and its content
import is verified. Differential Equations' 63-question diagnostic and import are
also complete and verified.
Their runners use their own `Topics.csv` files (181 and 159 topics respectively)
as the in-course skip lists, with the same correct-prerequisite / Don't Know policy
and complete capture as Multivariable Calculus. Once a diagnostic reveals its
detailed sidebar, progress discovery includes all its prerequisite courses.
To run only a
diagnostic and stop before selecting a lesson:

```sh
./scripts/ma-workers start linear --limit 1 --attach
./scripts/ma-workers start differential --limit 1 --attach
```

Daily XP sums the earned/base values on completed task rows marked **Today**.
Penalties remain negative; fixed awards such as placement exams use their displayed
full award as both earned and base. The denominator is the sum of task base points,
rather than the daily goal. Task IDs are recorded in `daily-xp.json` by local date
(America/Los_Angeles), so repeated queue reads and restarts do not double count.
Rows observed earlier that day stay recorded if a later queue omits them. Course
completion comes from `#coursePercentComplete`. `dashboard.json` is refreshed during
normal queue reads and profile checks; the five-second display refresh only reads
local files. At date rollover, daily XP shows unknown until a new queue read.

The supervisor records each run's console log and process identity under that
worker's `supervision/` directory. Stop signals only the supervisor it owns; it
allows the capture child 60 seconds to save a checkpoint before terminating its
own process group. Start resumes through the runner's existing recovery path.
`--limit N` optionally bounds each newly started worker; the default is unlimited.

Build the native importer comparison helper before use:

```sh
cargo build --offline --bin compare-question-answers
```

The importer uses `target/debug/compare-question-answers`, or the executable named
by `COURSE_ACADEMY_MATH_COMPARE_BIN`. It does not build code during capture or a
sweep. The helper shares the engine's error-preserving exact comparison, prompt
form requirements, and KP context (including formal vector/Riemann `i` and integer
sequence indices). Beyond existing notation identity it returns **equivalent**,
**different**, or **unresolved**. Equivalent values reuse the stored answer entity;
choice grading still compares answer identities. Image/text comparison, field
identity, and exact provenance hashes retain their existing rules. Different and
unresolved pairs follow the replacement/review policy. Missing executables,
execution errors, unsupported domains, and resource limits remain explicit; they
do not make a new captured symbolic blank invalid or adapt it into a radio field.
The helper accepts bounded requests, has a three-second execution deadline, reuses
one process, and caches pairs with their prompt/KP context and executable hash.

Completed saved imports are revisited on `run` startup, after a successful
comparison/import repair and retry of the current activity, and before the batch
ends. Installed cooldown repairs are picked up by the next startup. These sweeps
call only `Database.import_content`: they never navigate MA or launch backlog
repair sessions. A started assessment or diagnostic without confirmed terminal completion
defers the sweep. `--dry-run` skips sweeps entirely.
An assessment explicitly recorded as expired with a matching terminal answered
count is finished for this guard. Its own import still needs complete source
capture; an expired quiz does not block unrelated completed imports.

Eligibility requires the task-specific completion checkpoint and terminal screen
text, complete history, a finalized `content.json` matching the saved question
records, history explanations and activity metadata, and matching examples.
Queue-after failures are eligible. Verified committed/no-op imports are skipped,
with stale checkpoint flags repaired. Committed but unverified receipts use the
existing receipt path; pending intents retain their original content, transaction,
request key, basis and frozen reconciliation hash. Preview never sends a commit,
including when an unresolved intent already exists.
The completed canonical-example payload migration archived original commit files.
Those verifications now record the exact archived receipt location and old/new
content hashes. Recognition checks the original transaction hash and basis and
reconstructs the original payload hash solely for audit; changed content still
requires reconciliation. New imports never add the retired example attribute.

Imports validate every actual assertion/retraction in EDB's committed receipt
against the allowed content attributes and approved replacements, then read back
the affected content at that receipt's basis and check that reimport is a no-op.
They do not scan the entire database before and after each activity.
`verification_method` records `committed_transaction_and_content`; older full-scan
verification receipts remain valid. Schema predicate symbols remain EDN data.

Reviewed mathematical source errors are corrected in the study database while
their original captures remain unchanged. Corrections under
`reference/mathacademy/mathematical-corrections/<question-id>/` include the original
and corrected content, mathematical rationale, transaction and verified readback.
Their problem, worked solution and correct-answer values are attested at the
committed basis before reconciliation uses them. Later captures retain those exact
corrected values instead of restoring the source mistake or deferring the import.
Answer fields are replaced by new component identities; original fields, answers
and question versions remain available for historical use.

Exact question **330826** in topic **6372** has a verified convergence-domain
correction: the transform of $\int_0^t e^{-3\tau}\,d\tau$ exists for $s>0$.
Its unchanged displayed formula is $1/[s(s+3)]$. The solver applies this domain
only when the exact original prompt and choices match the committed correction's
hash-bound review. Original source wording, solutions and grades stay captured;
missing or changed evidence falls back to ordinary solving.

Topic **2616**, KP `624215ff-efdc-5b12-8d61-9d66371672d9`, has a reviewed containing-region interpretation for rectangular zero-extension questions. A matching committed canonical correction attests the explicit requirement $D\subseteq R$ for solver inputs, including verification. Original prompts, widgets, grades and worked solutions stay unchanged; decisions and content record the interpretation separately. The incremental health check flags newly verified interpreted questions lacking a matching per-question study correction, so capture can continue while the study clarification is completed. Other topics and unrecognized forms use ordinary solving.

Question **335252** in topic **6682** has a reviewed sufficient-theorem request.
Its authentic worked solution tests continuity and existence of the parameter
partial derivative on local rectangles and accepts I and III. A verified study
correction makes that criterion explicit and explains that II still admits
differentiation by dominated convergence. Only that exact source prompt, KP and
complete choice set receive the hash-bound interpretation. Raw prompts, grades
and choices remain separate; missing or changed attestation uses ordinary
solving and its existing confidence checks.

When the EDB CLI hides a remote conflict behind `transport/remote-error`, the
importer replays the exact saved request through a temporary local relay to read
only the original rejection code. Confirmed `postgres/stale-basis` rejections
archive the rejected plan and use the existing bounded replan path. Other errors
and unknown outcomes retain the original intent. The EDB development binary is
not rebuilt or replaced.

Identical displayed choices retain their positions in saved captures and share
one answer entity in EDB. An existing field without a correct answer can be
completed from the captured answer rather than failing reconciliation.
For broken history explanation-image aliases, the reader can reuse the original
bytes from that same question's graded live capture when the explanation text,
image order and saved asset hash match. Recovery records its bindings and
archives earlier history artifacts. Review history also accepts the same
topic-specific title aliases as lesson history.
If a solver stop leaves a completed event stream but no answer file, recovery
uses the streamed structured final answer after validation in the same activity
session. A completed turn without a usable answer repeats only its read-only
solver prompt. Empty pre-start checkpoints can be closed as superseded when a
later capture of that topic has a verified import; their original diagnostics
remain archived and are excluded from future capture repairs.

Each sweep attempts at most **20 captures**, at most once per capture. The durable
`.local/question_capture/saved-import-attempts.json` ledger prevents unchanged
failures from retrying on every activity or restart. A retry requires a changed
importer/comparison source or native executable hash, relevant authoring/capture
evidence or receipt, or a different preview/apply/database destination. New
verified source evidence for the same question IDs counts; unrelated captures,
database basis advances, checkpoint flags and diagnostic messages do not. The
final attempt key includes any newly created frozen intent artifacts. Failed
items stay deferred while other captures and live selection continue. Sweep
attempts do not consume activity limits, cooldown counts, RNG draws or queue
priorities. Review cases retain their existing authorization and history checks.

For a content-only invocation, without opening a browser:

```sh
/home/jake/Developer/MA/.venv/bin/python scripts/question_capture sweep-saved --preview
# Apply only when ready to import the bounded eligible backlog:
/home/jake/Developer/MA/.venv/bin/python scripts/question_capture sweep-saved
```

Both commands take the normal capture lock. Explicit `import-saved --content ...`
or `--resume DIRECTORY` remains available for a deliberate individual retry;
finalized completed captures resume through content-only recovery. Original capture
content and frozen intents are retained. A preview of an unresolved intent leaves
it deferred for apply-mode receipt recovery.

MA can include the identical `/js/math-editor.js` tag twice in a page, causing
its `const OPERATIONS` declaration to fail on the second execution. Navigation
keeps the first tag and removes only repeated tags for that exact script URL.
The editor code and answer interactions remain the site's original code.

DNS/connection failures complete the intercepted request rather than leaving
navigation pending. Page navigation retries network failures, timeouts and HTTP
5xx responses with interruptible backoff, capped at 180–185 seconds per wait.
Document fetches time out after 30 seconds. These retries do not repeat answer
submissions; saved activity checkpoints remain intact.

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
   Already captured tasks and completed lesson topics are skipped. A newly
   assigned unlocked lesson with zero progress and matching task/topic Start
   link can override a historical completed topic, for example after placement
   changes the account's course progression. Its task ID must be absent from
   saved captures and the observed completed task rows. Queue observations
   record these exceptions as `reassigned_lessons`.
   It refreshes and logs the queue after every completed activity, including the
   last activity allowed by `--limit`, and uses that observation for the next
   selection. Assessments, including quizzes, and in-progress tasks are also
   logged, with their observed URLs, IDs, progress, and assessment details.
   Assessments have their queue details expanded and saved, including test ID,
   time limit, question count, exact Notes text, and the remaining optional-XP
   allowance. An optional quiz stays queued while other eligible activities continue.
   If no eligible lesson, review, or multistep remains, it takes an optional quiz
   with complete question-count and time-limit details. Deferred or in-progress
   activities do not block this fallback. The player rechecks for alternatives
   before starting, and saves the optional notice and fallback decision.
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
   Saved in-progress captures recover automatically after fresh eligible work;
   `--resume` remains an optional way to choose one first. Lessons and reviews compete
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
   A recognized failed completion is captured and imported as a terminal attempt,
   with its actual grades and penalty retained. Its partial question pool does
   not need five questions per KP. A failed attempt does not mark the topic's
   lesson as successfully captured, so a subsequently offered retake remains eligible.
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
   `knowledge-point/questions`. Documented local values can be superseded by
   recovered MA content, attribute by attribute. Unknown provenance and
   contradictory source evidence stop the import with a review report.
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

## Authoritative replacement

`provenance.py` reads the saved Factorials authoring records and historical
question reconstruction/format repairs. Each usable declaration needs its
original transaction, verification basis, and a database readback at that basis.
The current question identity and value must still match; field evidence also
requires the same current field entity. Old content is never presumed authored
because of its age. Original lesson CSVs provide identity and format metadata,
not proof that a particular solution or distractor was locally written.

Saved completed automator captures establish the incoming authority from the
DOM/checkpoint and activity metadata, rather than from the solver's provenance
labels. The importer also checks prior committed automator evidence so a local
value subsequently confirmed by MA is treated as source content.

- Directly captured MA problems, worked solutions, and observed E/M/H labels
  replace stored values for the same question without requiring proof of the old
  values' authorship. Source DOM/checkpoint matching remains required. Old values
  remain in database history; exact retraction and basis guards still apply.
- Observed widgets can replace a documented local field type. Correct-key
  changes require an explicit source answer or a matching submitted value with
  a successful grade, or a confident source-based review by the persistent repair
  agent. Reviewed derivations remain distinct from directly observed answer keys.
  The explicit historical correction for q-23188 remains source
  evidence; its alternatives remain locally authored.
- Complete observed radio/select choice sets supersede old alternatives.
  Completeness comes from the full extractor output, or the saved legacy radio
  DOM's option count. Incomplete choices only enrich the existing field. A
  correct key is checked independently; unknown old distractor authorship does
  not block replacement by a complete live option set.
- Replaced fields and answers receive fresh versioned identities. The importer
  retracts the question's old ownership link and retains all old component
  entities and values. Matching answer feedback survives when no replacement is
  supplied. Blank-field values are retained, including prior entered strings.
- Any retained historical presentation or response defers field replacement.
  The usage check includes retracted presentations/responses and detached fields.
  A `db/noHistory` setting on those relationships also prevents automatic field
  replacement. Referenced fields/answers need additional handling outside this
  importer; no learner response is changed or component cascade performed.
- Missing source attributes preserve existing content, including canonical
  example fields and estimated difficulty. Existing practice can likewise be
  enriched by a partial source record; new practice still needs complete content.

Answer identity uses typed semantic values, math normalization and image bytes,
not displayed letters, option order, or image filename order. Question identity,
KP ownership, canonical references, and practice membership retain their existing
checks. A single legacy radio field named `answer` matches the observed single
radio field `selection` and is replaced through fresh field/answer entities.
Other changed field keys or a changed KP mapping require review.

A complete blank layout can be replaced through an explicit
`field-layout-source-reviews.json` review. The review binds the original database
question UUID, prompt, all field entities and values to a saved readback, and the
incoming prompt, worked solution, complete raw DOM widget set and source-backed
correct answers to hashes. Cited evidence files must remain exact. The same key
can name a different mathematical component; this path detaches every old field
and creates fresh layout-versioned identities without copying old-role values.
It requires checked, unused presentation/response history and retained component
relationships, and cannot override a reviewed mathematical correction. Missing
or changed review evidence leaves ordinary omitted-field validation in place.
Original components and the original question prompt remain in database history.


Each import saves `replacement-report.json` with per-attribute/component hashes,
categories, authoring/capture paths and hashes, basis, reason, and (after commit)
receipt. `reconciliation.edn` freezes the attested records, usage check, exact
approved retractions and immutable answer IDs. Its hash is part of the saved
commit intent. Native preview/receipt validation permits only those exact
retractions, rejects writes to preexisting answer identities/representations/
strings, and protects every non-content domain attribute. Post-commit verification
uses the frozen evidence and checks that reimport is a no-op. Unresolved intents
always retry their original transaction and evidence; altered content is rejected.
Reconciliation failures also reach the comparison repair session: formatting
errors can be repaired, while unsupported key changes still remain conflicts.
Saved-import sweeps use that same session rather than only repeating failed reads.
Pre-commit database-basis races replan locally, up to three attempts.

Confirmed `postgres/stale-basis` commit rejections use the same bounded retry:
the importer archives the rejected intent, transaction and reconciliation under
`edb-import/rejected-commits/`, then reads the current basis and replans. New
request keys include the basis as well as the transaction hash. EDB checks for an
existing receipt before rejecting a stale basis, so unknown commit outcomes still
replay their original request unchanged. Contention never launches a model repair;
after three attempts it leaves the capture pending, continues other work, and
permits another bounded attempt at the next saved-import sweep.

The changes apply on the next importer invocation; no database migration or
worker restart is required. To inspect a real saved capture without visiting MA:

```sh
/home/jake/Developer/MA/.venv/bin/python scripts/question_capture import-saved \
  --content reference/mathacademy/question-capture/ACTIVITY/content.json --preview
```

Read `edb-import/replacement-report.json`, matching report, and native preview
before importing that same capture without `--preview`. Use a new capture/import
directory for new evidence; keep an existing commit intent and its artifacts
unchanged. Do not commit simulated test captures. This implementation does not
perform a bulk replacement or start any MA activity.

Focused offline checks:

```sh
cd scripts/question_capture
/home/jake/Developer/MA/.venv/bin/python -m unittest \
  test_replacement test_capture.PolicyTests test_capture.ReconciliationTests \
  test_assessment test_multistep test_import_repair
```

After a complete activity and history capture, a failed import automatically
calls a dedicated headless Codex repair session. Its ID is saved in
`.local/question_capture/import-repair/session.json` and reused across lessons,
reviews, quizzes, and multisteps. This is separate from each activity's math
solver session. The capture worker keeps its lock and pauses at the import
boundary while the repair session inspects saved evidence in read-only mode.
It can propose a minimal `math_notation.py` comparison fix. The runner checks
the actual failing pair, nearby incorrect expressions, and the existing offline
comparison/import tests before applying it and retrying the original content
through all normal database guards. It can also request an unchanged retry when
the comparison is already fixed or the database basis changed. From authentic
worked solutions and original images it can propose confident answer corrections,
including lost function boundaries and unit exponent scope. Choice corrections
retain their original option indices. The runner archives previous derived
content and preserves raw captures and predictions. Pending commit intents use
exact receipt recovery. Each activity gets at most two repair turns per unchanged
code and evidence; model output,
diagnosis, candidates, and test logs are retained under the repair directory.
Failed validation output is supplied to the next diagnosis. Startup permits one
model diagnosis before reading the live queue; postponed repairs remain eligible
at subsequent activity boundaries.
Use `--no-import-repair` to disable this behavior, or `--import-repair-timeout`
to change its default 600-second limit. Session reuse follows the
[Codex non-interactive workflow](https://developers.openai.com/codex/noninteractive).

Browser interactions also use a 500 ms delay, including button clicks and answer
entry, in addition to the existing randomized waits. Change it with
`--ui-delay-ms` (for example, `1000` for one second). Multistep submissions wait
for the site's editor polling to enable Submit, then re-check the entered value;
a persistently disabled button or changed answer still stops before submission.

Every 20 attempted activities is the normal maintenance cadence while progress is
healthy. Two consecutive failures, queue-reading failures, interrupted assessments,
or a queue containing only saved work trigger repair earlier, without adding the
long rest. A persistent capture repair session examines saved diagnostics and uses
its judgment to resolve ordinary uncertainty from the source evidence.
After a completed capture is imported, queued unfinished failures that have not
been inspected under the current code and evidence also get one repair turn,
even while fresh activities remain available.
It handles targeted fixes, with at most two attempts per unchanged failure/evidence.
Budgets are scoped to the activity and retained for each evidence/source version. Only
the newest diagnostic for a failure is considered; old pages cannot alternate and reset
its budget. Solver uncertainty uses saved question, context, input and grade evidence;
diagnostic paths, observation timestamps and full-page render changes do not reopen it.
Resolved or blocked diagnoses are recorded. Capture source changes can reopen interaction
failures, while a proved mathematical source contradiction requires relevant source/input
or authentic grading evidence. Existing generic ledgers retain their original entries
and repair jobs while migrating completed attempts into scoped budgets. Import
failures and authentication/rate-limit blocks are excluded from this session.
If a nonempty queue contains only excluded activities, the runner attempts repair
early and keeps retrying with backoff. Each idle boundary inspects one failure,
then refreshes the queue so new work can proceed. Other repairable failures remain
eligible at later boundaries.
An empty queue or an exhausted activity limit does not trigger the early break.

The session proposes minimal related source patches and an offline regression
test. The runner stages them in an isolated copy and runs focused relevant checks.
Broad repairs can request the complete suite.
Existing tests, capture policies, import checks, saved activity data and learner state
are preserved. Only passing fixes are applied. The browser closes and the worker
restarts in the same process, reacquiring the capture lock and loading a checkpoint
that retains its attempted count, total limit, topic/task exclusions and RNG state.
The affected capture resumes using its existing checkpoint and solver session,
including an unfinished quiz. The browser inspects the restored state to determine
the next action, including previously uncertain submissions. A `resolved` diagnosis resumes it without
requiring a new code patch. Assessment and queue failures trigger maintenance
immediately instead of exiting before the regular break.

Repair time counts toward the randomized 2–6 minute cooldown; diagnosis and testing
can extend a break when needed. With no outstanding capture failures the usual
pause runs without a model call. Artifacts and the dedicated session ID are saved
under `.local/question_capture/capture-repair`. Use `--no-capture-repair` to keep
ordinary pauses, or `--capture-repair-timeout` to change the 180-second model limit.
The complete offline validation suite has a separate 30-minute timeout, configurable
with `--capture-repair-test-timeout SECONDS`. The initial focused regression retains
its five-minute limit. A timeout never permits a patch to be applied, and validation
remains interruptible. Testing can extend the cooldown beyond its usual duration.
Import repair continues immediately after complete captures as described above.

Recoverable assessment request errors and timeouts reload the same quiz at most
twice, preserving saved answers, decisions, solver session, and original timer.
A saved assessment interrupted by a recoverable timeout resumes before queue
selection. Once it finishes, the batch continues. Unknown dialogs, uncertain
final submissions, authentication blocks, and persistent failures require inspection.
The full question DOM is saved before answering, including unvisited questions.

It saves one snapshot of the account's configured course progress pages **after each completed
activity**. There are no new baseline or mid-activity checks. The snapshot is
compared with the preceding completed activity's snapshot when available.
Existing snapshots from older runs remain preserved. Reads are sequential and
use randomized navigation pauses: one read per configured page per completed activity.

Each `knowledge-state/<event>.json` contains every topic row from courses
in the configured scope (113/111/136 for Foundations), its source ID, title, color, mapped display band, module and topic
number, the source `#units` HTML, per-course timestamps, and changes since the
previous snapshot. Shared topics remain qualified by course, so conflicting
colors are retained. Unknown colors or an incomplete topic count defer the activity.
Use repeated `--progress-course-id ID` options to override the three-course scope.
Use repeated `--progress-url URL` instead when an exact URL with `unitId` is needed.
New activity checkpoints retain their configured progress scope for recovery.

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
activity but previews its database transaction without committing. By default,
the runner keeps going until no eligible activities remain or you interrupt it;
use `--limit N` for a bounded sequential batch. A required review or assessment
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

## Placement diagnostics

`diagnostic.py` handles `/tasks/T/diagnostics/D` separately from fixed-count quizzes.
A new placement diagnostic takes precedence over lesson selection. Before START,
the runner saves the enrolled course ID and a copy/hash of its `Topics.csv` in
`diagnostic-policy.json` and `diagnostic-Topics.csv`. It resolves the graph from
the visible course name under `--ma-root/COURSES/Math-Academy`; use
`--diagnostic-topics` to supply a CSV or graph directory explicitly, and
`--diagnostic-course-id` if the queue omits the enrolled course ID.

For a dedicated Multivariable Calculus account, after signing into its worker
profile, the diagnostic options are:

```bash
"$CAPTURE_PY" scripts/question_capture run --headless --limit 1 \
  --state-dir .local/question_capture-workers/multivariable \
  --output reference/mathacademy/question-capture-workers/multivariable \
  --diagnostic-topics /home/jake/Developer/MA/COURSES/Math-Academy/University/Multivariable-Calculus/GRAPH-Multivariable-Calculus/Topics.csv \
  --progress-url 'https://mathacademy.com/courses/106/progress?unitId=679' \
  --progress-url 'https://mathacademy.com/courses/55/progress' \
  --progress-url 'https://mathacademy.com/courses/54/progress'
```

This invocation answers the placement exam and imports its content. Diagnostics
answer prerequisites correctly and use **Don't Know** for skills in the requested
course. An existing source-question binding in EDB determines membership when
available; otherwise the same activity solver classifies the tested skill against
the saved topic list. Incidental vector notation does not itself make a problem
course content. A topic on the list remains course content even when another
course teaches it too. The 70/30 practice patterns and weighted quiz grades do
not apply to diagnostics.

For an account that should answer only previously covered skills, use
`--diagnostic-covered-topics /absolute/path/covered-topics.json`. This opt-in policy
replaces the prerequisite assumption: only explicitly covered topic IDs may be
answered. An uncovered prerequisite is skipped, and a covered skill is answered
even when it also belongs to the new course. The JSON must contain
`covered_topics` (possibly empty), optional `blocked_topics`, and a nonempty
`provenance` object identifying the account, observation time, and source progress
snapshots. Each topic has an integer `topic_id` and a nonempty `title`:

```json
{
  "covered_topics": [{"topic_id": 2036, "title": "Previously covered skill"}],
  "blocked_topics": [{"topic_id": 3340, "title": "Uncovered skill"}],
  "provenance": {"account_id": "account-name", "observed_at": "2026-10-09", "sources": ["saved-progress.json"]}
}
```

Refresh the account's sidebar progress before creating this snapshot. Include only
verified prior coverage; placement answers and other accounts' shared EDB completion
must not add known skills. The runner freezes the JSON bytes, source hash, topic
lists and provenance in `diagnostic-covered-topics.json` and
`diagnostic-policy.json`. Worker configuration can set `diagnostic_covered_topics`
to the snapshot path. Existing source-question/topic identity takes precedence;
unlisted and ambiguous source bindings skip. For blanks without a source ID, the
same solver session may classify only supplied topic IDs; uncertain, compound or
unmatched skills skip. The old policy remains the default for other workers.

For an exact Foundations CSV allowlist, set `require_source_binding: true` in
this JSON.
This stricter mode answers only when a source question has a unique, verified
topic binding whose ID appears in `covered_topics`. Missing, ambiguous and
unlisted bindings skip immediately; a solver's similar-skill suggestion cannot
make them covered. This option applies when a new diagnostic policy is frozen;
previously frozen policies and completed diagnostic evidence retain their rules.
Native history identities and grades are saved to `activity-metadata.json` after
the history join is validated, before per-question answer verification.

Resumes keep the frozen policy. An intentional policy migration must replace the
saved `diagnostic_policy` and `answer_policy` after preserving the old evidence.
The runner retains grades, invalidates unanswered decisions whose policy fingerprint
changed, and archives cached solver answers before reclassifying in the existing
activity session. It never resubmits a server grade to apply a new policy.

The player captures every served problem, answer widget, complete choices, assets,
decision, grade and revealed solution. It follows changed question headings and
the exam's analysis URL; there is no assumed question count. Live radio controls
expose source question IDs, while unnamed blanks retain durable numbered slots.
The diagnostic page's `student-diagnostic.js` requests one question through
`APISync.getNextDiagnosticQuestion(diagnosticId, taskId, retry)` when advancing;
the saved HTML contains the current widget, with no observed upcoming question bank.
History joins those slots to authentic question, topic and KP IDs, source difficulty
and worked solutions. Correct answers for skipped/incorrect questions are recovered
using verification turns in the same persistent solver session. Diagnostic solutions
are preserved as solutions; no canonical examples are inferred.

Submit and Next intents survive interruption. In-place observation retries are
bounded and do not reload a timed question. A restored grade continues without
resubmission; a fresh server view of an unanswered question permits saved answers
to be rematched and entered. Started diagnostics recover automatically. The retry
screen permits one immediate prerequisite retry in a retry chain; deliberate skips
choose No. Completion saves the analysis page and one knowledge snapshot, scoped
to the enrolled course unless `--progress-course-id` or `--progress-url` is explicit. Import failures
use the existing content-only receipt/recovery path.

The implementation is exercised offline using authentic radio, diagram and
MathQuill markup from the 54-question manual Multivariable Calculus diagnostic.
The fixture replays four representative questions, including skipped history
answers, adaptive completion, interrupted Submit/Next, and an asynchronous retry
overlay. The unattended player has not yet taken a new live diagnostic.

The EDB reader must support the existing database's storage format. Rebuilding
the adjacent EDB repository on a format-changing branch can break reads even
though capture code is unchanged. Repeated queue-read errors do not restart
the repair agent just because a diagnostic timestamp or queue page changed;
a changed error, reader binary, or capture source permits another diagnosis.

## Solver

The default adapter keeps **one Codex session per activity**, for lessons,
reviews, multisteps, diagnostics, and assessments, including verification turns. The first question starts `codex exec`;
subsequent calls use `codex exec resume <SESSION_ID>` with that explicit saved ID.
The CLI process exits between calls, but its persisted conversation carries forward.
It never uses `--last` or silently starts over if a resumed session has a different ID.

Each turn receives the current problem, locally observed fields and choices,
its screenshot and the original captured images displayed in that question,
along with newly captured canonical examples (including their
saved screenshots) and newly
revealed worked solutions from that activity. Grading feedback distinguishes
intentional wrong submissions from solver errors. Examples and feedback are
sent once, then retained in the session; changing KPs does not reset it. Current
choice letters and ordering must always be checked anew.

A cropped screenshot therefore does not hide a diagram that was captured intact.
An older uncertain answer can be rechecked in the same session when complete
displayed images are newly attached; its original input and answer are retained.
An exact model-capacity error gets at most two retries, each after a randomized
30–60 second wait, using the same confirmed activity session. Other errors are
deferred normally. Stop requests interrupt both the solver and retry waits.

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
Inequality commands use the visible ≤/≥ buttons when available. A typed fallback
finishes the command before leaving it; an unfinished command blocks Submit even
when MathQuill's LaTeX getter already returns the intended spelling. Outer fences
on powered logarithms are retained and checked separately from argument fences.

Use `--solver-command 'python3 /absolute/path/solver.py'` to substitute a solver.
It receives JSON on stdin (`mode`, `problem`, `worked_solution`, `fields`, `activity_context`,
`screenshot`) and must emit JSON matching `solver.py:SCHEMA` on stdout. Commands
are parsed as argument lists, never executed through a shell. A custom command
manages its own session persistence; its activity context contains all available
examples and grading feedback. Uncertain results
or invalid choices stop before submission.

Proof questions can reveal new fields after an intermediate Submit. Each stage
keeps its visible prompt, choices, entered values, and source field grades. The
player fills only unanswered fields, retains one C/W decision for the question,
and uses the same activity solver session for later stages. A restored submission
needs matching accepted or rejected source selections before it can continue.
Saved rejection feedback can confirm a restored stage when its problem, complete
choices, entered values, and displayed health match the pending submission.
One intended wrong choice is followed by correct retries; later stages introduce
no additional intentional wrong choices. The terminal source grade, including
Partial Credit, remains distinct, with canonical before/after captures and the
complete revealed proof. Repeated unchanged rejections defer the question.

The extractor supports observed radio circles, native blanks/selects, MathQuill
answer wrappers, and the original `.selectList` widget.
Custom selects retain their owned option node when the menu moves to `body` and
verify the selected content in `.selectListFrame`; selecting an option removes
the initial `.selectListSelectedText` placeholder.
MathQuill entry uses explicit typed characters, arrow-key events, and visible
symbol-menu buttons.
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
formula images in the problem and worked solution. SVG titles mixing outer TeX
with nested MathML also retain the whole rendering, including visible blank
boxes around phantom spacing. Rendered SVG assets save their exact original SVG
DOM beside the raster capture. Invisible MathML `mphantom` content is omitted.
Graphics are allowed to
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
automation acceptable. Each account captures activities sequentially; separate
account workers can run in parallel. There are no direct calls to private endpoints.
HTTP 401/403/429 and challenge pages stop the run. Submission
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
  submissions are recovered automatically by reloading the saved activity and
  inspecting actual grades or empty unanswered fields. Existing grades are
  captured without submitting again. Solver-reviewed worked solutions correct
  mistaken predictions, retaining the earlier prediction in the capture record.
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

The normal command continues available activities and automatically recovers
saved interruptions; completed imports are handled separately:

```bash
"$CAPTURE_PY" scripts/question_capture run --headless
```

Use `--resume reference/mathacademy/question-capture/TASK_ID` to select a run
first. Several unfinished captures are otherwise recovered automatically
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
and request key are reused. A definitive stale-basis rejection automatically
archives the rejected plan and replans within the three-attempt limit; unresolved intents are never
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
The diagnostic fixture additionally covers prerequisite/course classification,
unnamed-question history binding, source image choices, adaptive Next and completion,
retry overlays, resumable classification turns, and multi-topic content import.
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
