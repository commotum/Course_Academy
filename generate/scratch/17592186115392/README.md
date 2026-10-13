# Vector-chain generator draft

KP 17592186115392, Using the Chain Rule for Differentiation; immutable math basis 1356. Local review artifacts only; no database writes or registration.

```sh
.venv/bin/python generate/scratch/17592186115392/validate.py
.venv/bin/python generate/scratch/17592186115392.py --difficulty all --seed 42 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186115392.py --difficulty easy --template sin_log_tan_power --profile observed --seed 29 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`, plus `generate_easy`, `generate_moderate`, `generate_hard`. Explicit source cases live in `source-cases.json`; parameter keys/defaults are in `SPECS`. All fields are radio, key selection, five whole-vector math values. `observed` preserves a complete source bank, `authored` is the method-error default. Missing-level observed profiles are rejected. Explicit invalid parameters or a colliding whole bank raise an error; random sampling deterministically rejects the whole instance and retries.

The validator reads printed functions, options and every displayed derivative/substitution/distributed row with an independent local TeX parser, derives the actual derivative, and matches all 60 original vector options. Native grading exercises every owned answer ID via the real `learning::grade_field`. It separately checks prose, original row counts, formatting, signed level bounds, and stable content identities. Seeds/order do not change identity for fixed mathematics, template/profile/domain. Mathematical fingerprints use complete derivatives/domains and are distinct from presentation identities.

Moderate/hard are authored scope claims, specified in `classification.md`; neither rating was observed in source data. Four source teaching typos are minimally corrected; source bank mathematics remains 60/60. Prose and row sequences match 12/12; unaltered mathematical teaching sequences 8/12 and repaired sequences 4/12. TeX notation is normalized in every replay, so exact solution-byte matches are 0/12. Complete source banks are mapped in `bank-extraction.json` and residual interpretation limits are explicit in `template-extraction.md`; no inferred distractor diagnosis appears in learner content.

No plots are required. The linked lesson's SVGs are standalone formula/notation assets, not graphs. Work stops after stages 3–7.
