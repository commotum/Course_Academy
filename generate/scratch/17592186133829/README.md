# Scalar line-integral setup generator

Validated and registered as generator `dd3dfc48-9a48-5a88-b422-3e3f29557457` at math basis 2587. The source capture remains basis 1356; all six source practices were checked unchanged at preparation basis 2586. The additive commit supplied 12 distinct practices: 4 easy, 3 moderate, and 5 hard. Verified reserves are 5 at each level. No learner integral evaluation is assessed.

The exact request, preview, receipt, generated batch, and readback are in [reference/replenishment/basis-2586](reference/replenishment/basis-2586). See [verification.json](reference/replenishment/basis-2586/verification.json), [generated-review.md](reference/replenishment/basis-2586/generated-review.md), and [outcome.json](reference/replenishment/basis-2586/outcome.json). The worker held the application's `api.lock` through fresh inventory, guarded submission, and verification. Attribution is `:application/ca-engine`; source practices and learner history were preserved.

Two historical banks contain nonreal distractors; another source lacks its difficulty, key, and solution. All remain unchanged and excluded from validated reserve counts. Hard is an explicitly authored workload classification, as documented in [classification.md](classification.md) and [reference/current-classification.md](reference/current-classification.md). No unsupported band is reported filled.

```
.venv/bin/python generate/scratch/17592186133829/validate.py
.venv/bin/python generate/scratch/17592186133829/validate-boundaries.py
.venv/bin/python generate/scratch/17592186133829.py --difficulty all --seed 5 --count 2 --format markdown
```

`replenish.py` retains exact-request recovery and exact-basis readback for this job. It reuses the registered identity and existing content rather than issuing a second content commit on recovery. `validation-freeze.json` records the validated package hashes and rerun evidence.

Public API: generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None), plus easy/moderate/hard entrypoints. Profiles method(default), observed:q-ID(raw evidence), completed-source(only linear_cubic). Raw source-cases.json demonstrates omission-preserving source replay. Normal defaults cover all supported families. Hard is authored three-coordinate scalar substitution with one product and one square, full speed setup, fixed workload, no integration method.

Independent TeX readback validates prompt coordinates, scalar, bounds, each derivative operator/component/norm stage, all scalar substitution rows, formal/concrete/simplified setup rows, and all complete answer integral values. The real application grader validates owned radio selections; this does not substitute for mathematical QA. Captured incorrect radicals/nonexistent source key remain reported in classification/extraction/validation rather than hidden. No blank fields are authored because none were observed.

validation.json records exact denominators, public raw changes, level guards, identity, candidate domain sizes, native grading and actual runtime versions. Candidate counts are honest pre-rejection counts; no exhaustive accepted count is claimed. Review includes every original and at least two generated examples per observed family and each level. JSON is review data, not transaction EDN.
