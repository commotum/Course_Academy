# General exponential chain-rule generator

Run from the repository root:

```bash
.venv/bin/python generate/scratch/17592186092261/validate.py
.venv/bin/python generate/scratch/17592186092261.py --difficulty all --seed 119 --count 2 --format json
```

The API exposes `generate_easy`, `generate_moderate`, `generate_hard`, and `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`. Template names are source IDs plus `authored-three-term-slope`. Default `method:<qid>` profiles are supported learner records. `observed:<qid>` profiles replay complete captured records through parameterized masks, preserving absent attributes, duplicate legacy fields, exact original notation and missing refs; `historical:<qid>` profiles use a repaired single-field layout with the original bank. Both evidence profiles are marked ineligible for normal learning.

Ten original questions and nine field banks are retained, including q-48631's unrated/missing-solution record and two fieldless records. Normal completions are explicitly recorded. The hard family is authored: a bounded scaled three-term exponential derivative evaluated for a slope at a familiar point. No other skill is added, and no plots are required.

`validate.py` independently reads the actual displayed prompt, every bank value, composite definitions, both derivatives, all chain/evaluation rows and final prose. It tests complete source bank/value/designation fidelity separately from mathematical correctness, scope, formatting, task/content identities, stage-loss regressions, default family coverage and native grading through `generate/runs/current/check-engine`. The existing native grader fixture never accesses EDB. Raw incomplete records remain ungradable as captured; supported normal completions are tested separately.

Detailed counts and actual Python/SymPy versions are in `validation.json`; native acceptance/rejection counts are in `engine-validation.json`. Review originals and labeled variants in `review.md`/`review.json`. This work stops at guide step 7: no database, registration, shared engine changes, installs or commits.
