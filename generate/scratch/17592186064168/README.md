# Radical antiderivative generator

Script: `../17592186064168.py`; read-only capture basis 1356. Easy, authored moderate and hard entrypoints all use one rational-power integration method. No database writes or registration.

```sh
.venv/bin/python generate/scratch/17592186064168/validate.py
.venv/bin/python generate/scratch/17592186064168.py --difficulty all --seed 42 --count 2
.venv/bin/python generate/scratch/17592186064168.py --difficulty moderate --profile raw:q-2023 --format json
```

The public API is `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`, with `generate_easy`, `generate_moderate`, `generate_hard`. Explicit parameters are integer `p,d` within the finite reduced bounds in `classification.md`. `raw:<source_id>` preserves source omissions exactly; `completed:<source_id>` adds inferred/authored completion. All raw and opaque-bank outputs are evidence only and ineligible. Normal defaults use complete eligible operation banks, positive-domain wording and constant-free fragment answers. Source omissions and opaque interpretation are documented separately from fidelity.

`review.md` shows all eight original records, completed original parameters, changed-parameter variants, and two examples of each template/level with visible correct designation. `validation.json` separates full original fidelity (8 prompts, 6 present solutions, 4 present banks, 12 values, 2 present correct refs) from completion and native grading. `source-choice-mapping.json` covers every source option. `frozen-hashes.json` records final artifact SHA256 hashes.

Validation exhaustively checks 162 eligible normal layout/parameter instances (81 meaningful mathematical tasks: 18 easy, 22 moderate, 41 hard), plus 120 seeded samples. Native checks use the real memory-only `learning::grade_field`, and independent QA reads actual printed operators, prose conversions, radical powers, unsimplified fractions and all solution stages. Moderate/hard numerators include proper and improper peers within p≤20, p+d≤24 and p/d≤5, with explicit-input and sampler guards. Degree-9 authored powers were excluded after native grading rejected them; hard indices are 5–8. q-29635's original distractor intent remains opaque, with an exact separate evidence profile rather than an unsupported default error recipe.
