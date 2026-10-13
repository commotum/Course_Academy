# Scalar line-integral setup generator

Draft for parent QA, math basis1356. No database writes/registration or learner integral evaluation.

```
.venv/bin/python generate/scratch/17592186133829/validate.py
.venv/bin/python generate/scratch/17592186133829/validate-boundaries.py
.venv/bin/python generate/scratch/17592186133829.py --difficulty all --seed 5 --count 2 --format markdown
```

Public API: generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None), plus easy/moderate/hard entrypoints. Profiles method(default), observed:q-ID(raw evidence), completed-source(only linear_cubic). Raw source-cases.json demonstrates omission-preserving source replay. Normal defaults cover all supported families. Hard is authored three-coordinate scalar substitution with one product and one square, full speed setup, fixed workload, no integration method.

Independent TeX readback validates prompt coordinates, scalar, bounds, each derivative operator/component/norm stage, all scalar substitution rows, formal/concrete/simplified setup rows, and all complete answer integral values. The real application grader validates owned radio selections; this does not substitute for mathematical QA. Captured incorrect radicals/nonexistent source key remain reported in classification/extraction/validation rather than hidden. No blank fields are authored because none were observed.

validation.json records exact denominators, public raw changes, level guards, identity, candidate domain sizes, native grading and actual runtime versions. Candidate counts are honest pre-rejection counts; no exhaustive accepted count is claimed. Review includes every original and at least two generated examples per observed family and each level. JSON is review data, not transaction EDN.
