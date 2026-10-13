# Automated content capture

The replacement capture system implements the six stages in [the design](../plan.md). Python owns the workflow. An activity's agent solves questions, closes its final answer judgments, and handles specific ambiguities. Database work continues independently after the completed capture is saved.

## Run

Run `cap` to start or resume the new capture in tmux and open its dashboard. It uses the `ma-capture` session, with a four-account overview above the Mathematical Methods log and one log window per course. Repeating `cap` reconnects without duplicating running workers. The old `ma` session is left in place.

- `cap linear` starts or resumes just Linear Algebra.
- `Ctrl-b`, then `d` detaches; capture continues.
- `Ctrl-b`, then `n` or `p` switches course windows.
- `scripts/ma-workers attach` opens the dashboard without starting workers.
- `scripts/ma-workers status` shows current activity, today's XP/completions, and pending imports from the new capture records.
- `scripts/ma-workers stop` requests a checkpoint stop for all four accounts; add an account name to stop just that one.
- `scripts/ma-workers start` starts workers without attaching.

The dashboard reads local capture records. Old capture totals are not merged into it. Console logs are saved in `.local/capture/<account>/console.log`. Workers restart from their checkpoints after an unexpected exit; a requested stop leaves them stopped.

For direct commands, from `/home/jake/Developer/Course_Academy`, use the existing Python environment:

```bash
/home/jake/Developer/MA/.venv/bin/python capture/scripts check --account linear
/home/jake/Developer/MA/.venv/bin/python capture/scripts inspect --account linear
/home/jake/Developer/MA/.venv/bin/python capture/scripts run --account linear
```

`check` checks local dependencies and paths. `inspect` reads and expands the queue without starting an activity. `run` performs activities and automatically imports supported original content into `math`.

To run all four accounts:

```bash
/home/jake/Developer/MA/.venv/bin/python capture/scripts fleet
```

Accounts are `foundations` (Mathematical Methods), `linear`, `multivariable`, and `differential`. Each uses its existing authenticated browser profile and a separate capture process. The old and new workers share the profile's lock, so stop the old worker before launching its replacement. Installing this code does not switch running workers.

Stop with Ctrl-C or SIGTERM. Restart the same command to resume. `--visible` shows the browser. `--capture-only` performs activities and saves evidence without database commits.

New environments need Python 3.10+, [requirements.txt](requirements.txt), Playwright's Chromium, an authenticated account profile, the EDB writer, and an authenticated `codex` CLI. The repository's existing MA environment already has the Python dependencies.

## Modules

| Stage | Code | Responsibility |
|---|---|---|
| Queue Processing | `queue_processing.py`, `browser/parsing.py` | Expand every card; save displayed details, links, and HTML. |
| Activity Selection | `selection.py`, `context.py` | Apply the agreed activity/status order; rank Lessons and Reviews by downstream targets. |
| Activity Capture | `activity/capture.py`, `policy.py`, `solver.py`, `evidence.py` | Save steps, answer questions, reconcile accepted actions, review history and full lessons, and close question judgments. |
| Browser access | `browser/` | Read source pages, enter and verify responses, navigate, and collect original images. |
| Post-Activity Processing | `post_activity.py`, `progress.py` | Save dashboard/progress observations, compare topic colors and bands by course, count XP once, and retain retake instructions. |
| Database Preparation | `database/prepare.py`, `images.py`, `difficulty.py` | Resolve identities, prepare content and relationships, localize images, and calculate lesson difficulty. |
| Database Commit | `database/batch.py`, `commit.py`, `client.py`, `pipeline.py` | Batch complete activities, preview, recover exact requests, and verify receipts and content. |
| Continuous operation | `runner.py`, `outbox.py`, `fleet.py`, `terminal.py`, `monitor.py`, `storage.py` | Pin the current activity, save checkpoints, recover failures, and serialize imports across accounts. |

The implementation has no runtime dependency on `scripts/question_capture`.

## State and evidence

The `cap` / `scripts/ma-workers start --attach` view is one full-window dashboard.
Each account has fixed capture metrics above its own rolling log tail. Wide
terminals use a 2×2 layout; tall narrower terminals stack the accounts, and small
terminals shorten the tails. The dashboard shows earned/base XP, daily activity
counts (`L/R/Q/M/D`), daily unique new/existing database questions, course
completion, the last 20 earned-XP awards, answer profile, active task, pending
imports, omissions, and current errors. `↓` indicates an XP penalty, `·` a zero
award, `?` an unknown award, and `*` a partial total. XP charts use the displayed
scale for each account, ordered oldest to newest.

The viewer reads saved evidence and bounded console-log tails. It refreshes once
per second after collecting metrics; receipt-derived counts are cached in memory.
It makes no database or Math Academy requests and never treats pending imports as
verified question yield. Unknown course progress and unavailable import evidence
remain marked as unknown. "Last write" reports log freshness, not proof of work.

Supervisors run in the separate `<session>-workers` tmux session (normally
`ma-capture-workers`). Start and Stop still address accounts as before. The owned
older four-window layout migrates by moving panes/windows, retaining supervisor
PIDs, browsers, checkpoints, and log files. The main `ma-capture` session contains
the dashboard; worker windows remain available in the worker session for detailed
inspection. Detaching with `Ctrl+b d` leaves capture running.

| Location | Contents |
|---|---|
| `.local/capture/<account>/` | Active task, pacing and cooldown state, cached course graph, XP ledger and daily totals, retake instructions, status. |
| `reference/mathacademy/capture/<account>/<task-id>/` | Original HTML, screenshots, downloaded images, submissions, agent sessions/judgments, content, and post-activity observations. |
| `reference/mathacademy/capture/<account>/queue/` | Queue HTML, screenshots, expanded card details, and normalized selection inputs. |
| The capture's `progress-before.json`, `progress-comparison.json`, and `post-activity.json` | Immutable comparison baseline, before/after topic colors and bands, and timestamped observation/comparison history, including late reads. |
| The capture's `database/` folder | Prepared EDN, source decisions, previews, exact requests, receipts, and verification. |
| `reference/mathacademy/capture-database/` | Ordered pending imports shared by all accounts. |
| `/media/jake/SSD/EDB/math/images/<first-two-hash-characters>/<sha256>.<extension>` | Original image bytes, deduplicated by SHA-256. Content uses relative `images/...` references. |

`capture-complete.json` means source review and question judgments are saved. It does not erase source limitations. `import-status.json` separately records whether the database import is pending or verified. The dashboard reports missing source evidence as **Gaps**, independently of **Protected** existing agent corrections. Pending repaired captures retain their previous gap warnings until the replacement import is verified. A database outage does not cause the activity to be repeated or block the next capture. An unknown commit outcome blocks later database writes until its exact saved request is resolved.

`PYTHONPATH=capture python -m scripts.recovery sources --account ACCOUNT DIRECTORY` repairs a finished capture from its saved source and queues the complete revised activity for the ordinary 200-question batch. Use `--prepare-only` to validate without publishing the revision. Recovery preserves original evidence and account XP/completion/exposure ledgers. It refuses changes to an active capture or an unresolved database request. `reprocess` also queues its revision; it does not automatically perform a small individual commit.

Large short-term percentage jumps accompanied by widespread topic-color changes after an ordinary activity flag Math Academy's percentage as unverified. The original percentage and color observations remain available, while progress comparisons explicitly disable attribution to that activity. Original Learn/progress HTTP bodies and allowlisted cache headers are retained separately from rendered DOM evidence; authentication headers are excluded.

An agent's final finding that source evidence is unavailable stays with the capture. Preparation excludes the unsupported entity and dependent references, preserves the reason, and continues with supported content. Submitted guesses never become confirmed source answers.

Preparation rejects explicit incomplete-field sets and requires a final judgment for each newly discovered source gap, bound to the current evidence. Successful recaptures clear only the extraction failures they resolve, preserving their provenance and the original source artifacts. Topic display comparisons use course and topic IDs together; missing or unknown colors never become an inferred band or loss of progress. The 0–6 bands describe the display, not exact internal learner state.

Original content uses `:org/Math-Academy`, including source errors. Agent corrections remain separate evidence for later separately sourced transactions. Learner attempts, XP, and progress are saved locally. Calculated topic difficulty is also saved locally unless `--derived-source` names an existing source for it.

## Configuration and saved captures

Use `--config path/to/config.json` for fields defined in [config.py](config.py); command-line options override them. Account-specific `run` commands accept separate state, output, profile, and course paths. `fleet` reserves those settings for its four account processes.

### Answer profiles

All accounts default to `capture`, preserving the existing lesson/review patterns,
all-correct multisteps and failed-lesson/review retakes, and 87.17% assessment draws.
The nine learner profiles combine a learning speed with a starting accuracy:

| Learning speed | Shaky: 50% | Solid: 75% | Strong: 90% |
|---|---|---|---|
| Slow: 36 exposures per error halving | `slow-shaky` | `slow-solid` | `slow-strong` |
| Steady: 12 exposures per error halving | `steady-shaky` | `steady-solid` | `steady-strong` |
| Fast: 4 exposures per error halving | `fast-shaky` | `fast-solid` | `fast-strong` |

For each question, independently draw correct/wrong with probability
`p = 1 - (1 - base_accuracy) * 2 ** (-exposures / error_half_life)`.
These are simulation settings, not measured human learning rates. All profiles
approach the same 100% limit. Learner profiles apply to lessons, reviews,
multisteps, and assessments, including retakes; they do not switch to all-correct
to force progression. The existing diagnostic policy and timing apply to all ten
profiles, and diagnostics do not contribute practice exposures.

```bash
# Persist a profile for one account. Other accounts retain their settings.
scripts/ma-workers set-profile linear --answer-profile fast-strong
scripts/ma-workers set-profile linear --answer-profile capture

# Override the saved profile for a particular run.
/home/jake/Developer/MA/.venv/bin/python capture/scripts run --account linear --answer-profile steady-shaky
```

`--profile` still means the browser directory; `--answer-profile` means answer
behavior. The account setting is `.local/capture/<account>/answer-profile.json`.
New decisions read that setting while running; already saved decisions retain
their draw and policy on resume. A process running code from before profiles were
introduced needs one restart to load the implementation. Status JSON and the
dashboard expose the selected profile.

The account's `learning-exposures.json` retains counts and deduplicated events by
source KP and activity/question presentation. At first use, it includes earlier
confirmed practice from that account's saved captures. Correct and incorrect
graded questions each count once; browser retries, failed entries, examples, and
unanswered questions do not count. Assessment exposures arrive only after
completion and bound history grades. Existing ledgers continue tracking practice
when the account returns to `capture`. Profiles and courses share that account's
KP history; other accounts' practice does not transfer. Questions without a known
KP association use the base rate, with that limitation recorded, rather than
pooling unrelated unknown skills. Each decision records its profile, rate
parameters, exposure count, probability, and random draw in the capture evidence.

All accounts default to the logical EDB database `math` in the SSD PostgreSQL cluster at `/tmp/edb-math:55432`, with writes through `/tmp/edb-math/writer.sock` and images under `/media/jake/SSD/EDB/math/images`. A database rebuild may retain those paths while changing its immutable lineage. New capture requests record that lineage and refuse to replay against a different database; already verified imports remain verified.

Transaction previews use [the native preview helper](database/preview.rs), built and cached under `.local/edb/capture-runtime/` using the shared `engine/edb` predicates. The build requires Rust and the EDB release library recorded in the deployed writer's `bin/source/*/build.json`. Set `EDB_CORE_RLIB` to select an explicit library if that manifest is missing or ambiguous. Source or library changes invalidate the cached build. `--preview-bin` can select an explicitly deployed native preview executable. Preview never commits; `--edb-bin` remains the normal EDB CLI for reads and submissions to the existing writer.

Browser interactions have a minimum 500 ms delay (`--ui-delay-ms`), with 1 second for queue/progress settling. Defaults also restore the original 0.8–2.5 second event waits, 5–12 second answer pacing (crediting time spent solving), 10–25 seconds between activities, and a 2–6 minute rest every 20 completed activities. The `--event-min/max`, `--answer-min/max`, `--lesson-min/max`, `--rest-min/max`, and `--rest-every` options control these ranges. Between-activity and empty-queue waits keep their due times in `pacing.json`, resume after shutdown, and yield to an already active task. Assessment deadlines take precedence over optional pacing.

Browser operations default to a 45 second timeout and solver requests to a 300 second total budget. Temporary model capacity errors wait 30–60 seconds within that budget before resuming the same session; a manual stop preserves the cooldown. Browser recovery starts at 30 seconds and increases to 180 seconds, plus up to 5 seconds of jitter. Empty queues use exponential backoff with that same cap. All waits remain interruptible.

Assessments started by capture save a question schedule targeting 70–85% of the time limit. Live timer readings can shorten the saved deadline; restarting cannot extend it. Solving and optional waits leave a submission reserve of 15–60 seconds and account for unanswered questions. Minute-only timer labels use their conservative lower bound. Diagnostic answer timing retains its course/prerequisite policy; an offered prerequisite retry is saved once, so rereading the prompt cannot change the choice.

HTTP 429 responses pause the account using `Retry-After`, including asynchronous requests. Cooldowns survive restarts, and uncertain submissions are reconciled with the server before retrying. Rendering waits cover questions, solutions, tutorials, history, images, and diagrams. Math editor input gets its initial 500 ms poll plus a subsequent 200 ms poll before readback, then another verification after evidence capture. Identical duplicate MathEditor script tags are removed only after the original response bytes and the repair record are saved under `browser-originals/`. Missing evidence stays recorded for recovery and final judgment.

Pre-submit checks bind image choices to their original source URL and graphic HTML, so saved local image paths match the live page's extraction markers. Changed source graphics still require a fresh observation before any answer is entered.

Selection reads only the configured learner's persisted `:learner/targets`. Set that learner with `--learner-id`. When preparing an assignment transaction, explicitly include both its `:learner/assignments` link and its mapped topics in `:learner/targets`. Completing an assignment changes neither targets nor priority scores. You can also transact targets directly. Capture rereads the target set before each selection, while refreshing the course graph in the background. `--target` and nonempty `targets` configuration overrides are rejected. More supported targets rank first, then the shortest distance to a target; equal scores retain queue order. A database outage uses the latest saved learner targets; without saved targets, selection falls back to queue order and retries on the next selection. The selection record includes the supporting targets and the reason for the score.

The default solver starts a read-only Codex session per activity and resumes it for subsequent questions and final review. A replacement session receives the saved conversation. `--solver-command 'command arguments'` can provide another solver: it receives one JSON request on stdin and returns a JSON result on stdout. The request contains `task`, `payload`, `instructions`, `session_id`, and saved conversation; response shapes are defined in [activity/solver.py](activity/solver.py).

```bash
# Show capture state and the shared pending-import count.
/home/jake/Developer/MA/.venv/bin/python capture/scripts status --account linear

# Prepare and preview one completed capture without committing it.
/home/jake/Developer/MA/.venv/bin/python capture/scripts prepare /absolute/path/to/capture

# Keep processing pending imports without running browser activities.
/home/jake/Developer/MA/.venv/bin/python capture/scripts drain
```

`prepare` expects the new capture format. It can save prepared files and canonical images, and call an agent for identity ambiguity. It does not replay old migration EDNs. `drain --once` makes one attempt on an eligible batch and respects the question minimum; retries still honor backoff. Explicit `drain --flush` (optionally with `--once`) permits a smaller batch when deliberately clearing remaining work.

Runners accumulate completed activities across accounts until a compatible group has at least 200 distinct supported questions (practice plus canonical examples, including existing questions). An old queue never triggers a smaller automatic commit. The last whole activity may take the group above 200. Preparation enforces 8 MiB / 50,000-operation safety limits using actual EDN and expanded operations; it retains work instead of committing below the floor or splitting activities to fit. Conflicting revisions and dependent later activities stay in order while unrelated captures can fill the group. EDB defines capacity defaults, not recommended batch sizes.

Use `--database-batch-questions` to tune the minimum. JSON configuration also accepts `database_batch_max_bytes` and `database_batch_max_ops`. Retired settings `database_batch_max_age`, `database_batch_max_activities`, `database_batch_target_bytes`, and `database_batch_target_ops` are ignored when reading older JSON configurations; they cannot reinstate automatic small flushes. The group manifest, exact request, and receipt live in `capture-database/batches/`; each member also retains its receipt in its usual `database/requests/` archive. An unresolved submitted group blocks later imports while live capture continues, and previously saved requests still recover even if they were below the new floor. No answer policy changes with batching.

Completed batch archives can be compacted with `python3 scripts/compact_completed_batches.py BATCH_DIRECTORY` from the repository root. The tool requires final status, no pending or active request, matching original capture files and imported hashes, and verified no-op reimport evidence. It replaces duplicate content snapshots with references and hashes, stores shared receipts once, and divides activity records between `manifest.part-1.json` and `manifest.part-2.json`. A small `manifest.json` indexes the parts with checksums. The batch reader reconstructs the original completed results without replaying an import. An identical `.previous` checkpoint is removed; distinct prior content is retained by refusing compaction. Pending batch manifests retain their existing format.

## Tests

```bash
PYTHONPATH=capture /home/jake/Developer/MA/.venv/bin/python -m unittest discover -s capture/scripts/tests -v
```

The tests use saved source HTML, fake browser failures, a structured test solver, and a source-aware database fixture. Browser tests block network requests. They cover activity policies, staged answers, final judgments, image storage, lesson/multistep preparation, interrupted actions, exact commit retries, identity preservation, and repeated imports. Running the tests does not submit live Math Academy answers or commit to the math database.
