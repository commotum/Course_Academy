# Tangent periodicity scratch generator

Source snapshot: math basis 1356. The generator itself makes no database writes. Generator: `../17592186176050.py`.

```sh
.venv/bin/python generate/scratch/17592186176050/validate.py
.venv/bin/python generate/scratch/17592186176050.py --difficulty all --seed 19 --count 2 --format json
.venv/bin/python generate/scratch/17592186176050.py --difficulty moderate --profile source_q-103307 --count 1
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Parameters require exactly `v,a,b,n`; scalars may be exact SymPy-compatible strings. Only radio fields are supported. Explicit source profiles are parameterized evidence-only replays and preserve omitted source attributes. Normal output is completed, with separately labeled authored banks and levels.

`validate.py` reads actual prompt/answer/solution strings through an independent scalar and tangent-period parser, compares every source bank and source attribute presence, checks every displayed equality and required arithmetic stage, exercises rejected mutations, and runs the real native grader. `validation.json` separates fidelity, authored sampling and native grading. Raw originals missing correct refs remain ungraded evidence; no missing designation is reported as matched. `review.md`/`review.json` include every source bank and at least two normal variants per family and difficulty. `classification.md`, `template-extraction.md` and `variety.json` document scope and finite task counts.

The inventory job was completed at verified commit basis **2244**, from preparation basis **2243**. Current source replay confirmed all seven questions unchanged and all 35 choices matched. Five unused moderate questions already filled that band; replenishment added five easy and five hard questions, each with a distinct `(v,a,b)` task. All ten generated questions and every correct and incorrect choice passed mathematical validation and the native learner grader. Available distinct inventory after commit is easy **5**, moderate **5**, hard **5**, with no remaining job for this KP.

The registered generator UUID is `1ea1585c-ea92-559a-ab38-46752f78a2dc`, with script `generate/scratch/17592186176050.py`. Generated content is attributed to `:application/ca-engine`. `capabilities.json` records the supported bands and finite domains. Easy and hard remain explicitly authored workload levels; the two incomplete unrated originals remain preserved and excluded from inventory.

`replenish.py` is the scoped helper for this job. It acquires the application `api.lock`, rechecks current inventory and basis, retains the exact basis-guarded request, submits through the existing database integration, and verifies the receipt and content before releasing the lock. `reference/replenishment/basis-2243/` contains preparation, selected question review, native grading, speculative preview, exact transaction and request, committed receipt, exact-basis readback, and inventory recheck. Repeating this helper reconciles the retained request without adding content.

