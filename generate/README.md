# Generator pipeline

Run or resume one knowledge point:

```bash
.venv/bin/python scripts/generator_pipeline.py --kp 17592186096841 --difficulty easy --count 5
```

Repeat `--kp` to process a small queue. The same command resumes its saved job;
completed jobs retain their published batch. A review-policy upgrade may require
a new independent review before a resumed job receives current approval. Use `--directory .local/generation/another-run`
when intentionally requesting another batch. An existing approved draft is
adopted from `generate/runs/current/manifest.json`; the command does not start
the whole campaign.

Omit `--difficulty` (or use `auto`) to classify the source and choose a justified
band. An explicit band is never silently replaced. Inventory classification
requests likewise produce a reviewed initial batch; existing source questions
are preserved.

When generation is enabled, the learner application runs three concurrent generator
builders and one independent refill worker. Each builder uses the
[finder's urgency ordering](scripts/README.md), claiming the highest-priority
unlocked KP through authoring and independent review. Shared KP locks prevent
builders and refills from publishing competing versions. Builder slot locks also
preserve the concurrency limit across service restarts.

In self-directed mode, ordinary lesson preparation follows the same L30+ targets,
queue, and depth-two prerequisite scope as Study, with the same below-band-one
new-topic filter. All new lessons in that scope share one relevance tier. Actual
shortages for active, requested, or remedial work come first; other activity
shortages follow, then assessment variety, then advance builds and routine
replenishment. Within ordinary lesson shortages, earlier global layers come first
and a topic's deficient KPs stay together. Required work and current review or
assessment needs can enter from outside the lesson scope.

The self-directed build lane does not wait for every direct selection to have a
complete bank. Five fresh questions per KP satisfy a lesson's total-stock need;
filling five of each difficulty remains background reserve work. Course mode
retains its direct-selection completion gate before broader authoring.
Approved hashed packages refill independently without Codex sessions, aiming for
five easy, five moderate, and five hard questions per KP, including existing
packages outside the current scope. Legacy scripts and approved drafts enter the
build worker for packaging and review at their current priority. Saved drafts are
retained; uncertain publications are reconciled using their exact requests.

The application refreshes the ranking at startup, after learner actions and completed
generation jobs, and through the scheduler's 30-second refresh. Both workers wait for
the first ranked inventory. The read-only scan runs separately from learner requests
and does not hold their API lock. The existing `COURSE_ACADEMY_DISABLE_GENERATION=1`
and developer-mode switches control both generation workers.

Approval is specific to the package, original instructional source, database lineage,
KP, reviewed difficulty, and review-policy version. Missing or stale approval queues an independent review
in the build worker. An unsupported band is recorded and other work continues.
An unsupported difficulty with no source evidence is retained as unsupported.
Generator defects return to the author with executable counterexamples. Report corrections stay with the independent reviewer, and historical inventory defects go to the runner. Repeated failures or exhausted budgets become visible `blocked` jobs; their workspaces and publication recovery state are retained. Inventory is rechecked
after publication; existing jobs and pending commit requests survive restarts.

Approval is the independent Codex reviewer's recorded acceptance, followed by
verified publication; it does not require human permission. The initial build
normally samples one requested or source-justified difficulty and certifies that
band only. Approval for easy questions does not certify moderate or hard output
from the same script. A missing band certificate waits for automatic review under
the existing build priorities; no question from that band is published merely
because another band passed. Existing usable questions remain available to the
learner while this work waits.

Review policy 2 separately requires **decision-relevant variation**. Reviewers must
challenge unjustified fixed roles, test relevant and irrelevant counterfactuals,
and probe shortcuts within recognizable templates, not merely count unique outputs.
Their `pedagogical-variation.json` records decision coverage, shortcut results and
filtering effects with reproducible sample evidence. Source replay, mathematics,
grading and this distribution-level judgment remain separate acceptance checks.
Legitimate mathematical simplifications and justified finite families are allowed.

Revisions preserve the generator workspace. A prior independent review's source
account and scripts are offered for reuse only when its source hash and review
policy match; tests still run against the current candidate and all eight checks
remain required. A malformed review report gets one correction by the reviewer
using its saved evidence, without another author pass or resampling. Each evidence root permits at most three review/report sessions before an explicit blocked stop. Correction sessions can write their full evidence root. Report-only corrections do not require runtime code changes. Completed structured
agent results are reused on restart. Prompts direct interrupted sessions to saved
progress, limit bulk output, and stop testing once the required evidence passes.

Each unfinished author/reviewer session has a persistent limit of three Codex
launches, including failed launches and timeouts. Exhaustion stops automatic
retrying and records the session and original stage; it preserves the workspace,
samples and evidence. Completed cached results remain reusable even at the limit.
After fixing the cause, recovery must deliberately requeue that saved session;
a service restart or ranking refresh does not reset the budget.

[Shared offline validation tools](pipeline/validation-tools.md) centralize delivery
filtering, grader invocation, and rendering. `check_delivery.py` calls the same
record-preparation function as publication against saved inventory, with all image
writes confined to local evidence. Agents still independently check mathematics,
source fidelity, grading, rendering and variation before and after filtering.
Publication also reuses its fresh KP read for the same-basis source check.

The shared UI renderer automatically selects an installed Node >=20 runtime,
preferring the runtime bundled alongside Playwright. It does not rely on the
service's older system Node. Override with `--node` or
`COURSE_ACADEMY_NODE_EXECUTABLE` when necessary.

Old certificates do not satisfy policy 2. Fast refill sends them through the existing
review queue; published questions are retained. Saved reviews are tied to the policy
and exact package/source/batch/inventory inputs. A pending durable publication is
recovered exactly before any new review, and its receipt is retained; re-review does
not republish that batch. This change does not increase review scheduling priority.

## The four stages

1. **Generate:** Capture original lesson, source questions, complete answer
   banks, prerequisite context and source-image hashes at one EDB basis. A
   headless Codex author adopts or repairs a relocatable generator package in
   the job workspace. The runner checks its dependencies, runs it twice at a
   saved seed, and compares the records and image bytes.
2. **Validate:** A fresh Codex session independently reconstructs the assessed
   skill from the sources before inspecting the author's work. It tests source
   replay, mathematics, variety, decision-relevant variation, scope, actual grading,
   rendering and package relocation. All eight checks require evidence. A read-only
   `source/inventory.json` provides the captured question bank and the publisher’s
   deduplication fingerprints for delivered-distribution checks.
   Generator rejections return to the author with a cumulative finding history and executable regressions. Evidence findings return to the reviewer; inventory findings are repaired by the runner before fresh independent review. An unchanged generator rejected for an actual code defect stops with a no-progress error.
   Three author attempts bound the saved job by default; restarting a worker does not renew them. A rejected unchanged package or repeated identical failure blocks. A job also has a durable budget of nine distinct review sessions by default, including input refreshes.
3. **Prepare:** Verify the approved code, records, source and images. Publish
   the immutable generator package and hash image bytes through the shared image
   library. Deduplicate content and construct typed EDB forms using the existing
   schema and contributor.
4. **Push:** Preview with native predicates, save the exact guarded request,
   submit it, and verify the receipt and readback. A lost reply resumes the same
   request. A confirmed stale-basis rejection triggers fresh preparation.

`--stop-after generate`, `validate`, or `prepare` stops at the corresponding
boundary. Preparation publishes files to the shared store but does not commit
database content. The default runs all four stages. To resume a stopped job,
repeat the command without `--stop-after`.

## Storage and recovery

Manual jobs live under `.local/generation/<database>/<kp>-<difficulty>/`.
Inventory jobs keep their pipeline directory beside the existing inventory job.
Each has `job.json`, the source snapshot, author/reviewer JSONL logs and evidence,
the sampled batch, and a publication directory containing preparation, request,
receipt and verification records. Read `job.json` for the current stage and last
content failure. A process or transport failure leaves its current stage resumable.
Unfinished authoring and review drafts resume according to the current generator
priority, preserving their saved inputs and cycle. Only pending or uncertain
publication recovery overrides that ordering. If a draft's demand disappears,
the workspace remains available for a later return of that demand.

Packages are stored at:

```text
$EDB_MATH_ROOT/
  generators/<first-two-hash-characters>/<sha256>/
    generator-package.json
    <entrypoint and declared runtime files>
  generators/approvals/<sha256>/<kp>.json
  images/<first-two-hash-characters>/<sha256>.<extension>
```

The package hash covers sorted file paths, bytes, executable bits, entrypoint,
and dependency specification. Registration stores the package-relative entrypoint
in `question-generator/script`; existing repository-relative registrations remain
readable. Each package version has its own generator identity. The KP points to
the current approved version, while previous entities and learner history remain.

Generators run from disposable writable copies. They should write new assets
under `COURSE_ACADEMY_GENERATOR_OUTPUT_DIR`; those assets are hashed by bytes
during preparation. The archived package never receives plots or Python caches.

The author manifest `package.json` declares `entrypoint`, `files`, and
`dependencies`, for example:

```json
{
  "entrypoint": "generator.py",
  "files": ["generator.py", "source.json", "requirements.txt"],
  "dependencies": {"python": "3.13", "packages": {"sympy": "1.14.0"}}
}
```

Declare the versions actually used; the runner checks installed versions and
does not install dependencies. Local helpers, renderers, data and fonts affecting
output must be included in the package. Standard-library dependencies need no
separate files. Logs, reviews and generated output stay outside the manifest.

## Configuration

The runner uses the application's existing EDB environment and generated-content
contributor. Codex uses the user's existing login and model configuration.

- `COURSE_ACADEMY_CODEX_EXECUTABLE`: explicit Codex CLI path.
- `COURSE_ACADEMY_GENERATOR_PYTHON`: Python interpreter; defaults to `.venv/bin/python`.
- `COURSE_ACADEMY_GENERATOR_BUILD_WORKERS`: simultaneous builder pipelines;
  defaults to 3. Each pipeline alternates authoring and independent review. The
  refill worker runs separately. Set to 1 for sequential builds; restart the
  service after changing the setting.
- `EDB_MATH_ROOT`, `EDB_POSTGRES_URL`, `EDB_ENDPOINT`, `EDB_BIN`,
  `LEARNING_REQUEST_DIR`: existing database and asset configuration.
- `--max-attempts`: durable author/repair budget, default 3, plus three review sessions per author attempt.
- `--resume-reason`: after fixing a saved blocker, explicitly grant one additional bounded recovery and record why. Increasing `--max-attempts` or restarting alone does not reset a saved budget.

Author and reviewer sessions cannot publish through this workflow. They work in
their own directories with noninteractive sandboxed Codex execution. The runner
performs deterministic publication after acceptance. `repair-history.json` preserves
every finding, `repair-regressions.json` maps generator findings to workspace Python checks,
and `repair-preflight.json` records actual executions. Failed preflight checks go
back to repair before another full review. A `sample` checkpoint resumes completed
author work without launching another author. Source-supported engine limitations
remain repair tasks; a grading finding permits a scoped engine fix with acceptance
and rejection regressions. Infrastructure interruptions retain exact state with bounded retry; three process failures without a structured result block the inventory job. Provider/session launch limits remain distinct from content
repair and never cause uncertain publication requests to be replaced.

Scoped campaigns use persistent user-service definitions installed by
`scripts/generator_services.py`, with restart on unexpected process failure. The
definition remains available after a clean boundary stop; resuming does not depend
on a transient unit that systemd may have unloaded. The priority worker uses exit
78 for capacity pauses and does not automatically restart against an exhausted
provider quota. The cohort records its capacity error and stops before attempting
the rest of the cohort.

## Verification

```bash
.venv/bin/python -m unittest discover -s tests -p 'test_generator*.py'
.venv/bin/python -m unittest discover -s tests -p 'test_inventory_jobs.py'
```

Tests exercise real package/image stores and generator subprocesses. Database
failure-injection tests simulate lost replies, stale guards, and failed readback.
They complement native EDB pilot runs and actual independent reviewer trials;
mocked agent acceptance is not evidence of pedagogical quality.
