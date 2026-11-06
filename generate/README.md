# Generator pipeline

[Question generation principles](principles.md) is the canonical pedagogical contract.
The three role prompts define phase responsibilities; guides and conditional task
examples implement that contract. Historical run notes do not redefine new jobs.

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
initial publication band. An explicit band is never silently replaced. Every
build implements and verifies easy, moderate, and hard together; the requested
band controls immediate inventory publication, not generator coverage. Existing
source questions are preserved.

When generation is enabled, the learner application defaults to three concurrent
generator builders and one independent refill worker. This installation sets
`COURSE_ACADEMY_GENERATOR_BUILD_WORKERS=6`, so it runs six builders plus the refill
worker. Builders use the
[finder's urgency ordering](scripts/README.md). With two or more builders, one
slot prefers queued reviews of existing packages, so a continuing lesson backlog
cannot consume all approval-review capacity. Immediate activity deficits and
unfinished publication recovery still come first. The review slot takes ordinary
work when no eligible, unlocked review is waiting; the other builders retain the
finder order. Shared KP locks prevent builders and refills from publishing
competing versions. Builder slot locks preserve the total concurrency limit
across service restarts.

Each review covers the entire package's three difficulty bands. Pending review
requests for different bands of the same KP/package are consolidated into one
catch-up review; they do not create a separate background approval backlog per
band. Observed imported ratings can still prioritize routine reserve work, but
they neither limit the review's coverage nor approve a package. Shortage and
assessment-variety requests retain their priority. Missing imported examples do
not make a difficulty unsupported; investigation supplies complete exemplars.

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

1. **Investigate:** A script captures the target at one database basis. Complete
   target evidence needs no donor. When examples are missing, the script ranks
   candidates using prerequisite metadata and title evidence, then supplies a
   bounded set of complete references. The investigator establishes the target
   operation first and selects a compatible reference or none, explaining what
   transfers. Agents consume supplied captures rather than search EDB ad hoc.
   If needed, the investigator creates and checks three local design exemplars,
   one per band. They remain local permanently; they are not published inventory,
   imported evidence, or authority over the target task. Later phases may correct
   them. Legacy uncertain exemplar requests are reconciled exactly before migration.
2. **Author:** The author builds or continues one relocatable Python generator
   covering all three bands from target material and the revisable account/examples.
   Source replay records original banks; fresh practice repairs their defects and
   preserves valid mathematical cases. The author may repair shared tools or the
   answer engine. The runner samples every band twice at its saved seed and compares
   records/assets for deterministic replay.
3. **Verify and repair:** The verifier writes an independent source account before
   inspecting author work, then tests and repairs in the same persistent session.
   It compares actual pre-feedback decisions, required recall, support and response
   endpoints across every material family and all bands. The initial account stays
   unchanged; conceptual corrections have explicit source-backed amendments linked
   to the final report. Shared-tool defects and report omissions remain this agent's
   responsibility. There is no fourth approval agent.

Engine hashes record the environment used for verification. An engine change during
an active review requires affected compatibility checks to be rerun. Later unrelated
engine builds do not expire a completed approval. Engine repairs retain their own
regressions; actual defects or material package/source changes trigger generator repair.

Incomplete imports remain unchanged. Missing fields, keys, solutions, or labels
are partial evidence, never inventory-repair obligations or publication blockers.
Historical inventory observations need no blocking handoff artifact. Defects in
new output must be repaired and checked before acceptance.

`:knowledge-point/level-coverage` is a cardinality-many ref recording observed
imported labels independently of completeness. Its values are easy, moderate,
hard, or `:question.difficulty/unobserved` alone when no imported label exists.
Authored exemplars and verified generator capabilities do not add observed
coverage, and unobserved is not a served question difficulty. The script
installs/backfills coverage through the existing
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

The verifier calls `finalize_review_command` before acceptance, including when
no repair was needed. This regenerates all three final batches and assets and
saves `final-binding.json` for the actual package, source, inventory, engine and
instructional inputs, including the supplied account/reference/local examples.
It checks those final outputs and validates its
report with `scripts/generator_review.py --result FILE --evidence-root DIRECTORY`
before returning. Report corrections resume the same persistent verifier session.
Acceptance requires explicit passing results for easy, moderate, and hard with
their final batch hashes, plus nine shared checks: source replay, mathematics,
variety, decision-relevant variation, scope, grading, rendering, packaging, and
progression. Shared analysis need not be repeated in three separate reports.
Each band cites recognized delivery, native-grader and rendering evidence for its
actual final raw or delivered records. Representative checks must cover materially
different families. A report-shaped file or an unresolved valid answer is not a pass.

[Shared validation tools](pipeline/validation-tools.md) use the actual publication
filter, native grader, and learning UI. Rendering defaults to unanswered and
completed states; choose representative record indices and relevant desktop/narrow
viewports. Omitted records are reported. Inspect actual controls, graphs and
mathematical layout, not just parse success. The renderer ignores hidden native
backing values while inspecting opened rich-dropdown menus. Visible raw TeX remains
a failure. It selects installed Node >=20 beside Playwright; `--node` or
`COURSE_ACADEMY_NODE_EXECUTABLE` can override that choice.

After acceptance, deterministic **prepare** and **push** steps publish the
immutable package/assets, preview the typed EDB forms, retain the exact guarded
request, submit it, and verify receipt and readback. Lost replies recover the
same request before new work. No human approval is required.

Policy 6 records all three verified capabilities together, tied to one final
package, instructional source, database lineage, KP, answer engine, and review
session. Its format-2 approval record stores the actual publication receipt and
published band separately from the three verification results. Testing a band
does not claim that its sampled questions were published. Only needed inventory
is published, and later refills use the recorded verified band set instead of
the original review request's difficulty.

Existing single-band approvals require one all-band catch-up review per
KP/package. That review reuses the completed investigation, exemplars, authored
package, and applicable evidence; it does not restart those phases merely to
obtain the other band approvals. A policy upgrade does not relabel old evidence
as new passes. Earlier published questions remain available, and uncertain
publication requests are recovered before any new work. Older jobs that never
completed the three-phase investigation still use its existing migration, which
retains drafts and error history.

If an existing package cannot initially sample one of the new verification
bands, the catch-up verifier receives the actual sampling errors and repairs
that capability in its session. Strict finalization must then produce all three
complete batches before acceptance. The policy migration grants a recorded,
bounded allowance for its newly required review work; ordinary restarts still
do not replenish retry budgets.

`--stop-after generate`, `validate`, or `prepare` stops after sampling, final
verification, or preparation respectively. Preparation publishes files to the
shared store but does not commit database content. Repeat without `--stop-after`
to resume through verified publication.

## Storage and recovery

Manual jobs live under `.local/generation/<database>/<kp>-<difficulty>/`.
Inventory jobs keep their pipeline directory beside the existing inventory job.
Each has `job.json`, the source snapshot, investigation/author/verifier JSONL logs and evidence,
the sampled batches, and a publication directory containing preparation, request,
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

## Refill checks and finite domains

Approved packages refill without another LLM review. Every new approval declares
`refill-review-plan.json` in the immutable package. It records `format:
"course-academy-refill-plan-v1"`, `status` (`checks` or `not_applicable`), a concrete
`reason`, `source_refs`, review-root-relative `evidence_paths`, `checks`, and
`finding_exemptions`. Each check has `id`, `purpose` and `finding_ids`. Every retained
generator finding must map to a check or an exemption with `id`, `reason`,
`source_refs` and `evidence_paths`. The verifier judges applicability; an empty
history does not itself justify omitting useful response/task checks. The runner
binds that decision to the approved package. A `not_applicable` plan has no checks
or checker descriptor; it must explain why the native controls suffice for this
package's applicable refill risks.

A `checks` plan declares `refill-validation.json` and its checker in runtime files:

```json
{
  "format": "course-academy-refill-check-v1",
  "script": "check_refill.py",
  "args": [],
  "files": []
}
```

The checker receives `--records`, `--inventory`, and `--output`, and returns a report
with `status: "passed"` and `checked_fingerprints` equal to the exact sorted
`content_fingerprint(question)` set of surviving records. It also returns
`check_results`, one `{id, status: "passed", checked_fingerprints}` for every
approved check; each check considers every survivor, applying its reviewed
condition where relevant. Optional `native_checks`
rows contain `fingerprint` and native-harness `checks`. Keep this checker and its
inputs declared/package-bound. `--inventory` supplies all deduplication fingerprints,
normalized nonretired complete `questions`, `usable_fingerprints`, and
`questions_sha256`, so population-level checks can inspect actual content. The
checker runs in a temporary copy containing only declared package files, outside
the repository/workspace, with a scrubbed environment and isolated Python import
path. No workspace sidecars, repository imports or ambient Python paths are
supplied. This tests dependency completeness; it is not a security sandbox against
hostile code. Applicable checks run on final delivery survivors before new
approval and on future refills. Use them for independently justified valid-equivalent,
near-miss, task-contract and demonstrated cue regressions, not copied metadata
assertions. Completed legacy approvals remain usable without a new plan and are
explicitly reported as legacy fallback. Without contextual checks, native grading tests every offered
selection choice and canonical acceptance for blank fields, recording the missing
blank-response controls as limitations. It does not invent wrong blank answers or
prove semantic equivalence or pedagogical variety. Population coverage is assessed against relevant delivered
inventory, not forced into every small refill fragment.

`generation-limits.json` can additionally declare
`finite_catalogs: {"easy": "easy-catalog.json"}`, with complete generated-record
lists in declared runtime files. The finite catalog must enumerate the supported
domain; only the complete catalog already present in inventory proves exhaustion
and produces `finite-limit`. A duplicate-heavy sample or `no_changes` alone does
not prove that no valid unseen questions remain. Per-batch caps still apply to all
verification/refill requests without dropping any of the three required bands.
The finder projects content-only source and pool hashes from captured teaching,
canonical examples, question/answer content and retirement state. Those changes
or a different package reopen a finite conclusion; learner availability counts
and unrelated database writes do not.

## Configuration

The runner uses the application's existing EDB environment and generated-content
contributor. Codex uses the existing login; every phase explicitly selects
`gpt-6.1-sol` and `model_reasoning_effort="high"`.

- `COURSE_ACADEMY_CODEX_EXECUTABLE`: explicit Codex CLI path.
- `COURSE_ACADEMY_GENERATOR_PYTHON`: Python interpreter; defaults to `.venv/bin/python`.
- `COURSE_ACADEMY_GENERATOR_BUILD_WORKERS`: simultaneous builder pipelines;
  defaults to 3; this installation configures 6. Each pipeline runs investigation,
  authorship, and verification/repair. The
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
session identities survive interruption. Cached phase results are reusable only
when their role inputs, material source/reference content and instruction versions
match; changed evidence is not written underneath a stale accepted interpretation.
Produced accounts/examples remain distinct from the inputs used to cache their
creator. Routine inventory/basis churn alone does not restart authorship. Genuine repeated failures retain bounded
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
