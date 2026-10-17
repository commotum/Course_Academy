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

The learner application runs two independent background workers. The build worker
uses the [finder's relevance-first ordering](scripts/README.md), taking one KP at a time through
authoring and independent review. The refill worker runs approved hashed packages
without Codex sessions, aiming for five easy, five moderate and five hard questions
per KP. It maintains existing packages even after their topics leave the urgency
groups. Legacy scripts and approved drafts enter the build worker for packaging and
review. A shared KP lock prevents the two workers from publishing competing versions.

The application refreshes the ranking at startup, after learner actions and completed
generation jobs, and through the scheduler's 30-second refresh. Both workers wait for
the first ranked inventory. The read-only scan runs separately from learner requests
and does not hold their API lock. The existing `COURSE_ACADEMY_DISABLE_GENERATION=1`
and developer-mode switches control both generation workers.

Approval is specific to the package, original instructional source, database lineage,
KP, reviewed difficulty, and review-policy version. Missing or stale approval queues an independent review
in the build worker. An unsupported band is recorded and other work continues.
An unchanged rejected request is not repeatedly retried. Inventory is rechecked
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
   Rejections return to the author, up to three authoring attempts by default.
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
- `EDB_MATH_ROOT`, `EDB_POSTGRES_URL`, `EDB_ENDPOINT`, `EDB_BIN`,
  `LEARNING_REQUEST_DIR`: existing database and asset configuration.
- `--max-attempts`: bounded author/repair attempts, default 3.

Author and reviewer sessions cannot publish through this workflow. They work in
their own directories with noninteractive sandboxed Codex execution. The runner
performs deterministic publication after acceptance. Unsupported or exhausted
content jobs are recorded and other queued jobs continue; infrastructure failures
remain resumable with background backoff.

## Verification

```bash
.venv/bin/python -m unittest discover -s tests -p 'test_generator*.py'
.venv/bin/python -m unittest discover -s tests -p 'test_inventory_jobs.py'
```

Tests exercise real package/image stores and generator subprocesses. Database
failure-injection tests simulate lost replies, stale guards, and failed readback.
They complement native EDB pilot runs and actual independent reviewer trials;
mocked agent acceptance is not evidence of pedagogical quality.
