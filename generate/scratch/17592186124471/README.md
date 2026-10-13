# Pointwise chain-rule generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186124471.py --difficulty all --count 2 --seed 7
.venv/bin/python generate/scratch/17592186124471.py --difficulty hard --profile q-94888_raw --format json
.venv/bin/python generate/scratch/17592186124471/validate.py
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and the three level entrypoints. Only `radio` field type is supported because all originals use it. Original replay parameters/profiles are in source-cases.json. The two unrated originals use public `q-36247_raw_omission` / `q-36253_raw_omission` profiles that retain missing difficulty, solution, and correct-ref fields. Their `_raw` profiles supply separately labeled authored completions for full mathematical/native verification. All raw profiles are marked `evidence_only=true`, `eligible_for_learning=false`; authored operation profiles are eligible for learning. Explicit source profiles fix the source mathematical inputs and allow whole-function scale1..4; use scale1 for exact originals. Default `_operations` profiles vary coefficients/curves/time with complete chain-rule operation banks.

Scope: compute the gradient from a supplied scalar function, compose it with a two/three-coordinate curve, dot with curve velocity, evaluate at specified t. Easy is authored; two unrated sources have authored moderate/hard assignments. No plots are needed and no database/engine/shared-file edits occur.

Validation covers all eight banks and 40 exact source option strings, six present correct refs, six exact present solutions, 216 authored instances, 24 changed-scale raw instances total including originals, and 1,200 real native radio grading checks. Independent mathematics is read from printed prompts, choices, formal gradient/composition/curve-derivative rows, dot rows, evaluation rows and prose substitutions.

Known limits: source wrong scalar values underdetermine error intent, so raw banks use explicitly limited equivariant replay rather than inferred default recipes. Two raw solutions have a missing third derivative operator and five have dimension-label defects. Validation asserts/reports the two false rows; default normal output fixes the formal operators and labels. The two unrated sources have no observed correct designations or solutions to match; their authored derivations are reported separately. Radio grading tests owned IDs; printed-value correctness is established by the independent parser, not by those ID checks. Artifacts are author-review data, not database transaction records.
