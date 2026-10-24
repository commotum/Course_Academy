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

When generation is enabled, the learner application defaults to three concurrent
generator builders and one independent refill worker. Builders use the
[finder's urgency ordering](scripts/README.md). With two or more builders, one
slot prefers queued reviews of existing packages, so a continuing lesson backlog
cannot consume all approval-review capacity. Immediate activity deficits and
unfinished publication recovery still come first. The review slot takes ordinary
work when no eligible, unlocked review is waiting; the other builders retain the
finder order. Shared KP locks prevent builders and refills from publishing
competing versions. Builder slot locks preserve the total concurrency limit
across service restarts.

Within routine reserve reviews, bands observed in the KP's question inventory
come before unobserved bands, both when selecting a KP's next review and when the
review slot claims work. A failed refill's saved eligible-source capture takes
precedence over the broader inventory ratings when its KP, lineage and registered
package still match. Shortage and assessment-variety requests retain their
priority. Observed ratings are a scheduling hint, not proof that a package can
generate that band or permission to publish it. Unobserved bands remain queued as
background work. Missing imported examples do not make a difficulty unsupported; investigation supplies complete exemplars.

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

## Investigation, authorship, and verification

Each build uses three headless `gpt-6.1-sol` agents with `high` reasoning:

1. **Investigate:** A script captures the KP and selects one reference KP with at
   least two complete Math Academy imports at each difficulty. Selection uses
   fixed Datalog, one database basis, and batched explicit Pulls; agents do not
   search the database themselves. The investigator studies the target and the
   reference progression. When evidence is incomplete, it constructs and checks
   three complete exemplars, one easy, one moderate, and one hard. The runner
   publishes them as ordinary questions under the target KP using `:agent/codex`
   provenance. No reconstruction labels or imported Math Academy IDs are added.
2. **Author:** The author builds or continues a relocatable Python generator from
   the target material and completed exemplars. It may revise earlier assumptions
   and repair relevant shared tools or the answer engine. The runner samples twice
   at the saved seed and compares records and asset bytes for deterministic replay.
3. **Verify and repair:** The verifier first examines the instructional evidence
   independently, then tests and repairs the generator in the same persistent
   session. It owns mathematics, pedagogy, grading, rendering, packaging, and
   delivered variation. Earlier requirements may be overridden with evidence.
   Shared-tool defects and report omissions are corrected by this verifier rather
   than handed to another agent. There is no fourth approval agent.

Incomplete imports remain unchanged. Missing fields, keys, solutions, or labels
are partial evidence, never inventory-repair obligations or publication blockers.
Historical inventory observations need no blocking handoff artifact. Defects in
new output must be repaired and checked before acceptance.

`:knowledge-point/level-coverage` is a cardinality-many ref recording observed
imported labels independently of completeness. Its values are easy, moderate,
hard, or `:question.difficulty/unobserved` alone when no imported label exists.
Authored exemplars do not add observed coverage, and unobserved is not a served
question difficulty. The script installs/backfills coverage through the existing
EDB transport, with durable requests and exact-basis readback:

```bash
.venv/bin/python scripts/generator_investigation.py --directory .local/generation/coverage --apply
```

The same command without `--apply` prepares the next required migration step.
Schema declarations live in `schema/data/6-knowledge-point.edn` and
`schema/content/4-question.edn`, mirrored in the math database schema directory.

All phases may repair relevant shared renderer, delivery policy, runner, or
answer-engine code. They stage a unified diff in their own workspace and use
`shared_repair_command` with `--patch` and repeated `--check-json` argv arrays.
The helper serializes shared changes and their tests. A failed check reverses
that patch and restores the native grader's previous bytes and mode; additional
build outputs are declared with repeated `--artifact` options. The same agent
resolves conflicts and retries its repair. Ordinary per-KP package changes need
no shared lock, and workers never edit another KP's job or imported questions.

The verifier calls `finalize_review_command` after its repairs. This regenerates
the final batch and assets and saves `final-binding.json` for the actual package,
source, inventory, and engine. It checks those final outputs and validates its
report with `scripts/generator_review.py --result FILE --evidence-root DIRECTORY`
before returning. Report corrections resume the same persistent verifier session.
Acceptance requires evidence for all eight checks: source replay, mathematics,
variety, decision-relevant variation, scope, grading, rendering, and packaging.

[Shared validation tools](pipeline/validation-tools.md) use the actual publication
filter, native grader, and learning UI. The renderer ignores hidden native
backing values while inspecting every opened rich-dropdown menu. Visible raw
TeX remains a failure. It selects the installed Node >=20 runtime beside
Playwright; `--node` or `COURSE_ACADEMY_NODE_EXECUTABLE` can override that choice.

After acceptance, deterministic **prepare** and **push** steps publish the
immutable package/assets, preview the typed EDB forms, retain the exact guarded
request, submit it, and verify receipt and readback. Lost replies recover the
same request before new work. No human approval is required.

Approval remains specific to package, instructional source, database lineage,
KP, difficulty, and review policy. Policy 5 supports the three phases and verifier
repairs. Existing certificates that lack the current policy enter the normal
review queue; earlier published questions remain available. One approved band
does not certify other bands. Saved pre-policy blocked jobs are migrated into
investigation while retaining their work and original error history; uncertain
publication requests are recovered first.

`--stop-after generate`, `validate`, or `prepare` stops after sampling, final
verification, or preparation respectively. Preparation publishes files to the
shared store but does not commit database content. Repeat without `--stop-after`
to resume through verified publication.

## Storage and recovery

Manual jobs live under `.local/generation/<database>/<kp>-<difficulty>/`.
Inventory jobs keep their pipeline directory beside the existing inventory job.
Each has `job.json`, the source snapshot, investigation/author/verifier JSONL logs and evidence,
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
contributor. Codex uses the existing login; every phase explicitly selects
`gpt-6.1-sol` and `model_reasoning_effort="high"`.

- `COURSE_ACADEMY_CODEX_EXECUTABLE`: explicit Codex CLI path.
- `COURSE_ACADEMY_GENERATOR_PYTHON`: Python interpreter; defaults to `.venv/bin/python`.
- `COURSE_ACADEMY_GENERATOR_BUILD_WORKERS`: simultaneous builder pipelines;
  defaults to 3. Each pipeline runs investigation, authorship, and verification/repair. The
  refill worker runs separately. Set to 1 for sequential builds; restart the
  service after changing the setting.
- `COURSE_ACADEMY_GENERATOR_REVIEW_WORKERS`: builder slots that prefer pending
  approval/repair reviews for existing packages; defaults to 1 with multiple
  builders and 0 with a single builder. Valid values are 0 through the builder
  count minus 1, preserving at least one builder for ordinary shortage ordering.
  These slots are part of the configured builder total, not additional workers.
  For example, six builders normally provide five priority slots and one review
  slot. This preference neither retries blocked/rejected jobs nor waives review.
- `EDB_MATH_ROOT`, `EDB_POSTGRES_URL`, `EDB_ENDPOINT`, `EDB_BIN`,
  `LEARNING_REQUEST_DIR`: existing database and asset configuration.
- `--max-attempts`: durable investigation/author budget, default 3; verification has three correction rounds per configured attempt by default.
- `--resume-reason`: after fixing a saved blocker, explicitly grant one additional bounded recovery and record why. Increasing `--max-attempts` or restarting alone does not reset a saved budget.

Agents use persistent noninteractive sandboxed sessions with access to the
repository and their job/evidence directories. They own relevant shared repairs;
database publication stays in the runner's durable transport. `repair-history.json`
retains findings, `repair-regressions.json` maps generator findings to executable
checks, and `repair-preflight.json` records their results. Completed work and
session identities survive interruption. Genuine repeated failures retain bounded
retry budgets and explicit errors; restarting alone does not renew those budgets
or replace uncertain publication requests.

A controlled UI service stop records the exact unfinished agent launches owned
by that service before terminating its children. On restart, each matching launch
receives one replacement launch; the original execution and shutdown evidence
remain recorded. Completed results are reused. Failed agents, unmarked crashes,
and ordinary process failures retain their existing retry limits, and logical
author-attempt limits do not reset. Shutdown also closes new pipeline and agent
admission, so it cannot start fresh work while stopping. Older interrupted jobs
without ownership markers require explicit, evidence-backed recovery; a restart
alone never grants them more attempts. Publication intents and approval state are
not changed by this mechanism.

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
They complement native EDB pilot runs and actual verifier trials;
mocked agent acceptance is not evidence of pedagogical quality.
