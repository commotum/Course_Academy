# Automated content capture

The replacement capture system implements the six stages in [the design](../plan.md). Python owns the workflow. An activity's agent solves questions, closes its final answer judgments, and handles specific ambiguities. Database work continues independently after the completed capture is saved.

## Run

From `/home/jake/Developer/Course_Academy`, use the existing Python environment:

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
| Post-Activity Processing | `post_activity.py` | Save dashboard/progress observations, count XP once, and retain retake instructions. |
| Database Preparation | `database/prepare.py`, `images.py`, `difficulty.py` | Resolve identities, prepare content and relationships, localize images, and calculate lesson difficulty. |
| Database Commit | `database/commit.py`, `client.py`, `pipeline.py` | Preview, submit, recover exact requests, and verify receipts and content. |
| Continuous operation | `runner.py`, `outbox.py`, `fleet.py`, `storage.py` | Pin the current activity, save checkpoints, recover failures, and serialize imports across accounts. |

The implementation has no runtime dependency on `scripts/question_capture`.

## State and evidence

| Location | Contents |
|---|---|
| `.local/capture/<account>/` | Active task, queue, cached course graph, XP ledger and daily totals, retake instructions, status. |
| `reference/mathacademy/capture/<account>/<task-id>/` | Original HTML, screenshots, downloaded images, submissions, agent sessions/judgments, content, and post-activity observations. |
| The capture's `database/` folder | Prepared EDN, source decisions, previews, exact requests, receipts, and verification. |
| `reference/mathacademy/capture-database/` | Ordered pending imports shared by all accounts. |
| `/media/jake/SSD/EDB/math/images/<first-two-hash-characters>/<sha256>.<extension>` | Original image bytes, deduplicated by SHA-256. Content uses relative `images/...` references. |

`capture-complete.json` means source review and question judgments are saved. `import-status.json` separately records whether the database import is pending or verified. A database outage does not cause the activity to be repeated or block the next capture. An unknown commit outcome blocks later database writes until its exact saved request is resolved.

An agent's final finding that source evidence is unavailable stays with the capture. Preparation excludes the unsupported entity and dependent references, preserves the reason, and continues with supported content. Submitted guesses never become confirmed source answers.

Original content uses `:org/Math-Academy`, including source errors. Agent corrections remain separate evidence for later separately sourced transactions. Learner attempts, XP, and progress are saved locally. Calculated topic difficulty is also saved locally unless `--derived-source` names an existing source for it.

## Configuration and saved captures

Use `--config path/to/config.json` for fields defined in [config.py](config.py); command-line options override them. Account-specific `run` commands accept separate state, output, profile, and course paths. `fleet` reserves those settings for its four account processes.

Selection reads the configured learner's targets and topic coverage from unfinished assignments. Set that learner with `--learner-id`; repeated `--target <math-academy-topic-id>` options supply an explicit target set instead. More supported targets rank first, then the shortest distance to a target; equal scores retain queue order. Missing target information also falls back to queue order and retries database reads in the background. The selection record includes the supporting targets and the reason for the score.

The default solver starts a read-only Codex session per activity and resumes it for subsequent questions and final review. A replacement session receives the saved conversation. `--solver-command 'command arguments'` can provide another solver: it receives one JSON request on stdin and returns a JSON result on stdout. The request contains `task`, `payload`, `instructions`, `session_id`, and saved conversation; response shapes are defined in [activity/solver.py](activity/solver.py).

```bash
# Show capture state and the shared pending-import count.
/home/jake/Developer/MA/.venv/bin/python capture/scripts status --account linear

# Prepare and preview one completed capture without committing it.
/home/jake/Developer/MA/.venv/bin/python capture/scripts prepare /absolute/path/to/capture

# Keep processing pending imports without running browser activities.
/home/jake/Developer/MA/.venv/bin/python capture/scripts drain
```

`prepare` expects the new capture format. It can save prepared files and canonical images, and call an agent for identity ambiguity. It does not replay old migration EDNs. `drain --once` makes one attempt on the oldest eligible pending capture.

## Tests

```bash
PYTHONPATH=capture /home/jake/Developer/MA/.venv/bin/python -m unittest discover -s capture/scripts/tests -v
```

The tests use saved source HTML, fake browser failures, a structured test solver, and a source-aware database fixture. Browser tests block network requests. They cover activity policies, staged answers, final judgments, image storage, lesson/multistep preparation, interrupted actions, exact commit retries, identity preservation, and repeated imports. Running the tests does not submit live Math Academy answers or commit to the math database.
