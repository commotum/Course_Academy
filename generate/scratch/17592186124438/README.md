# Tangent-line generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186124438/validate.py
.venv/bin/python generate/scratch/17592186124438.py --difficulty all --count 2 --seed 7 --format json
.venv/bin/python generate/scratch/17592186124438.py --difficulty moderate --template q-132589 --profile raw_q-132589 --count 1
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`, plus each named difficulty entrypoint. Field type is radio. All 14 source moderate families are eligible normal defaults. Raw observed banks use `raw_q-…` profiles and remain evidence-only; source-cases.json supplies exact original parameters. `authored_operations` supplies the method-derived five-choice bank. Raw source q-36369 preserves the legacy missing correct ref and cannot be passed as a two-field fixture to the native harness. Its banks are independently verified; separately labeled native fixture copies infer the absent legacy designation mathematically and grade both fields. Faithful raw output retains the omission.

Easy parameters: signed nonzero integers a,b,k of magnitude 1–4; nonzero integer altitude z of magnitude ≤12. Hard parameters: signed nonzero integer a of magnitude 1–4, k of magnitude 1–3 (y=k pi), nonzero integer altitude z of magnitude ≤12. Moderate parameters: scale is signed nonzero integer of magnitude 1–3; normal altitude is integer/half-integer of magnitude ≤12 or integer multiple of pi with multiplier magnitude ≤3. Source xy coordinates retain familiar source evaluations; altitude and scale affect assessed arithmetic. Explicit invalid inputs fail; random whole-bank collisions reject the entire instance. No mixed-bank replacement or hidden resampling of explicit parameters.

Validation reads the actual printed prompt, every derivative stage and substituted/rearranged point-slope stage, conclusion, and each whole affine line using exact arithmetic. Complete line equality uses augmented affine row spaces, covering nonzero equation scaling and dependent-variable substitutions. Native radio grading checks IDs only after independent displayed-mathematics verification. No typed blanks are supplied by this KP, so typed-equivalence grading is inapplicable. Metadata survives full JSON roundtrip; identities ignore option order and seeds, while mathematical fingerprints exclude banks/profile aliases. There is no renderer/cache; fresh and repeated records are deterministic modulo option order.

All outputs are scratch review artifacts. No database transactions, registration, engine changes, installs, or commits.
