# Question capture

Run sequential Math Academy lessons and add captured **content only** to EDB.
The entry point is `python scripts/question_capture`; the code is self-contained
apart from Playwright, the EDB CLI, and a solver command.

The runner:

1. Reads unlocked lesson priorities for the selected learner from EDB. Intersects
   them with new lessons actually available in Math Academy's visible queue, then
   takes the highest priority. It does not change EDB task priorities or statuses.
2. Captures each canonical example live. For each KP it randomly chooses
   `C-W-C-W-C` with probability **0.7**, or `W-C-W-C-C` with probability **0.3**.
   It captures each practice problem and locally observed answer widgets before
   submitting, then captures the result and revealed worked solution. It checks
   every grading result before continuing.
3. Opens the completed activity, expands the explanations, and joins all question
   IDs to KP titles and source E/M/H difficulty labels. It checks that the live
   and activity question sets and KP mappings agree.
4. Matches `q-N` and `e-N` globally in EDB. Adds missing attributes and choices,
   reuses existing owned answer entities, and links new practice to the correct
   `knowledge-point/questions`. Existing populated attributes are preserved.
   Conflicting correct answers, field types, KP ownership, or canonical example
   IDs stop the import for review.
5. Previews a content-only transaction, commits with a basis guard and stable
   request key, and verifies that all learner and engine facts are unchanged
   across that exact transaction. It also verifies that a repeated import would
   produce no further changes.

It also saves a baseline and a snapshot of all three course progress pages
after **every step** (tutorial, canonical example, or answered question), after
Continue advances the lesson, and once more after lesson completion. An
unexpected grade is captured before stopping. The progress pages use a separate
tab, leaving the live lesson loaded. Reads are sequential and use the existing
randomized navigation pauses: three additional page reads per snapshot.

Each `knowledge-state/<event>.json` contains every topic row from courses
113/111/136, its source ID, title, color, mapped display band, module and topic
number, the source `#units` HTML, per-course timestamps, and changes since the
previous snapshot. Shared topics remain qualified by course, so conflicting
colors are retained. Unknown colors or an incomplete topic count stop the run.
Use repeated `--progress-course-id ID` options to override the three-course scope.

These files capture the **full displayed profile for those courses**, not MA's
complete internal learner state. The rows do not expose exact continuous FIRe
repetitions, memory, intervals, or ability. White-to-0 and blue-to-1–6 follows our
existing initialization convention; darkest-to-6 is an assumption. Unchanged
bands do not prove the underlying values stayed unchanged. Progress snapshots
are saved separately and never transacted into EDB learner state.

**Reviews are not automated yet.** If required reviews occupy the queue, the
runner reports that no ranked lesson is available and stops. Capture a review
manually before designing its automation; do not assume lesson stopping rules
apply to it. This is the current live queue situation as of October 3, 2026.

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
lesson but previews its database transaction without committing. Default limit
is one lesson; use `--limit N` for a bounded sequential batch.

To use a different Python environment, install `requirements.txt` there and
install its Playwright Chromium browser if needed. No dependencies were added to
the main application environment.

The default learner is `59d5cf13-351c-4114-be19-4c3bb64ee051`. Override it with
`--learner-id`. Database defaults match this project's local EDB service; override
`EDB_POSTGRES_URL`, `--database`, `--edb-bin`, and `--endpoint` as appropriate.
All paths work when invoked from this repository root.

## Solver

The default adapter calls `codex exec` with structured output and a read-only
temporary working directory, using only the displayed question, available
choices, and a screenshot of the question. It uses `--ignore-user-config` so
project instructions, configured connectors, and custom tools do not influence
the solver. It does not set a model unless `--solver-model` is supplied. It needs
an authenticated Codex CLI and consumes model usage. The structured-output
interface follows the [official noninteractive documentation](https://learn.chatgpt.com/docs/non-interactive-mode).

The solver must identify the correct answer even when the runner intends to
submit a wrong answer. The runner picks a different radio/select choice or types
the solver's explicitly incorrect blank value. After an incorrect submission,
the solver independently checks the correct answer against the revealed worked
solution. Correct submissions are confirmed by the site's grader.

Use `--solver-command 'python3 /absolute/path/solver.py'` to substitute a solver.
It receives JSON on stdin (`mode`, `problem`, `worked_solution`, `fields`,
`screenshot`) and must emit JSON matching `solver.py:SCHEMA` on stdout. Commands
are parsed as argument lists, never executed through a shell. Uncertain results
or invalid choices stop before submission.

The extractor supports observed radio circles, native blanks/selects, MathQuill
answer wrappers, and the original `.selectList` widget. MathQuill entry uses
explicit typed characters and arrow-key events, with no hidden widget API.
Unknown widgets, unreadable formulas, and unrendered graphical assets stop for
review. Radio extraction is validated against all fifteen actual Sum Rule
widgets; native mixed fields have fixture tests. MathQuill/custom-select typing
still needs validation on a live activity. A solver error can break the intended
five-question sequence; the runner stops immediately on an unexpected grade.

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
| Before submitting an answer, in addition to solver time | 5–12 seconds |
| Between lessons | 10–25 seconds |
| After every 20 lessons when more remain | 120–360 seconds |
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
- Rendered graphical assets saved locally without additional download requests.
- Canonical examples, activity metadata, and `content.json` for import.
- `state.json` with chosen sequences and a checkpoint before every submission.
- `knowledge-state/` with a full course profile and band changes after each step.
- EDB reads, `transaction.edn`, preview, exact commit intent, receipt, matching
  report, and verification under `edb-import/`.

Attempt results are retained only to audit the intentional capture sequence.
They are never transacted into learner tasks, timing, responses, or ability.
Canonical examples normally expose no answer widgets or difficulty; those facts
remain unknown and are listed as missing source fields. This runner does not
invent canonical answer fields, difficulty ratings, or practice distractors.

Resume an interrupted live capture with:

```bash
"$CAPTURE_PY" scripts/question_capture run --resume reference/mathacademy/question-capture/TASK_ID
```

If submission may have occurred, resume only waits for/reads its grading result;
it does not send the answer again. If the site cannot establish the result, the
checkpoint remains available for manual recovery.

Pending progress snapshots are checkpointed before Continue. If interrupted after
advancing, resume captures the missing observation without resubmitting the
answer; it marks the snapshot `recovered_after_interruption` because its original
capture time cannot be reconstructed. Completed snapshot files are reused.

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
so an EDB failure does not cause the lesson to be retaken.

## Validation

```bash
"$CAPTURE_PY" -m unittest discover -s scripts/question_capture -p 'test_*.py' -v
python3 scripts/question_capture import-saved --content reference/mathacademy/sum-rule-13925458/content.json --preview
```

Tests use the saved real lesson DOM and EDB snapshots. Browser fixture tests run
offline, including full five-question progression, activity joining, and a
grading mismatch that must stop before the second submission. The progression
test checks all 1,040 course-qualified rows in each of its 20 snapshots and a
known color transition. Recovery tests ensure a failed snapshot does not resend
an answer. The EDB preview
for the saved Sum Rule capture passes at basis 305: three existing practice
records enriched, twelve new practice records planned, with no learner writes.
No live lesson, live review, or database commit was performed while developing
this script.
