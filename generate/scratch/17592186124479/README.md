# Pivot-column generator

KP 17592186124479: Finding the Number of Pivot Columns of a Matrix.

Registered generator UUID: `1a826b59-74a9-5e36-9c52-67364fe51a6d`.
Repository script: `generate/scratch/17592186124479.py`.
Supported difficulty: moderate; 16 source-specific radio templates and four complete numeric banks. Easy and hard remain unsupported by this evidence-bounded package, with five unfilled places each. The incomplete unrated q-35459 remains unchanged and excluded.

From the repository root:

```sh
.venv/bin/python generate/scratch/17592186124479.py --difficulty moderate --count 5 --seed 42 --format json
.venv/bin/python generate/scratch/17592186124479.py --difficulty moderate --count 1 --seed 42 --format markdown
.venv/bin/python generate/scratch/17592186124479/validate.py
```

The application invokes the same JSON command. JSON output is an array of question records; reproducibility data, parameters, exact states, coefficients, source references and dependency versions accompany each record. The optional --template selects a source template. The batch sampler excludes equivalent row rescalings, ignores seed and choice order for identity, and reports bounded shortfalls on stderr. Python and SymPy are the only generator dependencies. The validator additionally uses the existing native application grader.

Validation passed on 224 instances: all 16 source banks replayed completely (80 options, 64 distractors), exact Fraction elimination agreed with rendered solutions, all declared variable slots varied, and native grading accepted 224 correct selections and rejected 896 wrong ones. Side-by-side originals and variants are in reference/side-by-side.md. Current validated file hashes are in validation-freeze.json.

This job needed generator registration only: the inventory check under api.lock found 16 distinct, never-shown, unreserved, gradable moderate questions. The application contributor committed the generator UUID/path and KP reference from basis 2730 to 2731. All 17 source questions and learner history were preserved, and post-commit inventory had no remaining KP job. No new practice questions were inserted.

reference/replenishment/basis-2730 retains the exact preview, request, receipt, typed before/readback snapshots, native inventory grading, preparation, verification and outcome. reference/registration-generator.py retains the exact script hash captured in the request; reference/cli-compatibility-update.json records the final CLI-only update and its validation. The mathematical generator is byte-for-byte unchanged by that update. reference/final-audit.json verifies the complete evidence chain. replenish.py is the recovery/submission runner for this particular job, not a general job scheduler.
