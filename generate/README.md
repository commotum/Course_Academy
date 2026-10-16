# Generator pipeline

Run or resume one knowledge point:

```bash
.venv/bin/python scripts/generator_pipeline.py --kp 17592186096841 --difficulty easy --count 5
```

Repeat `--kp` to process a small queue. The same command resumes its saved job;
completed jobs stay complete. Use `--directory .local/generation/another-run`
when intentionally requesting another batch. An existing approved draft is
adopted from `generate/runs/current/manifest.json`; the command does not start
the whole campaign.

Omit `--difficulty` (or use `auto`) to classify the source and choose a justified
band. An explicit band is never silently replaced. Inventory classification
requests likewise produce a reviewed initial batch; existing source questions
are preserved.

The learner application's inventory worker invokes this pipeline automatically.
It retains its existing trigger and inventory verification rules. A registered
hashed package is reused directly; legacy scripts and approved drafts are
packaged by the author. The existing `COURSE_ACADEMY_DISABLE_GENERATION=1` and
developer-mode switches still control background generation.

## The four stages

1. **Generate:** Capture original lesson, source questions, complete answer
   banks, prerequisite context and source-image hashes at one EDB basis. A
   headless Codex author adopts or repairs a relocatable generator package in
   the job workspace. The runner checks its dependencies, runs it twice at a
   saved seed, and compares the records and image bytes.
2. **Validate:** A fresh Codex session independently reconstructs the assessed
   skill from the sources before inspecting the author's work. It tests source
   replay, mathematics, variation, scope, actual grading, rendering and package
   relocation. Acceptance requires evidence files for the named checks.
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

Packages are stored at:

```text
$EDB_MATH_ROOT/
  generators/<first-two-hash-characters>/<sha256>/
    generator-package.json
    <entrypoint and declared runtime files>
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
