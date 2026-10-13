# Reciprocal-function antiderivative generator

Local generator: `generate/scratch/17592186064169.py`. No database operations. Sources: math basis 1356. All three levels integrate one unit negative power with n≠-1; hard higher-root notation is an explicitly authored extension, not an observed source rating. Every template has plot rating none.

```sh
.venv/bin/python generate/scratch/17592186064169.py --difficulty all --seed 7 --count 2 --format json
.venv/bin/python generate/scratch/17592186064169/validate.py
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Parameters are primitive positive integers `p,q`, representing negative exponent `-p/q`. Explicit inputs outside documented level/template bounds raise `ValueError`. Only radio is supported; raw fieldless evidence omits fields.

Raw source example: `generate('easy', template='negative_named_radio', parameters={'p':2,'q':3}, profile='raw_q-29987')`. All six raw source profiles preserve absent keys. The two complete old source banks are parameterized evidence-only profiles with opaque distractor intent; completed observed profiles are `observed_q-29987` and `observed_q-29989`. Default `authored_power_errors` banks are eligible for learning.

`validate.py` replays all six sources, exact prompts, all four present solutions and both complete banks. It independently parses rendered TeX, differentiates every displayed choice and intermediate primitive, verifies complete recipe formulas, rewrites and stage counts, exhausts finite domains, checks scope/identity/formatting, tests deliberate corruptions, and invokes `generate/runs/current/check-engine` for every completed record's five choices. `validation.json` reports precise counts and limitations. `hashes.json` freezes final files; `review.md` shows captured originals, completed originals, raw profile variants and at least two authored variants per template/level.

Source keys are absent, so 0/0 original designations can be matched. All inferred keys are separately authored and verified. q-29662's missing initial differential is preserved raw and repaired normal. Radio selection is the native response type; no blank-equivalence claim is made. All rational identities and primitives use x>0 on a connected real interval.

Normal learner prompts explicitly add `Assume $x>0$.` so every root/reciprocal rewrite and primitive uses the declared positive connected real domain. Raw replay preserves the original prompt exactly. Markdown/review previews label difficulty and source/generated origin and mark generated correct choices with ✓; raw missing keys remain explicitly unmarked.

Durable replenishment uses `replenish.py`, the existing application contributor and EDB transport. It records finite capabilities in `capabilities.json`, excludes equivalent source/canonical integrands across all levels, and retains exact requests, speculative previews, receipts and readback under `reference/replenishment/`. Generator registration reuses an existing identity when present; otherwise its stable UUID is derived from the KP UUID and `question-generator`. The application `api.lock` is held through basis recheck, preparation, submission and verification. Source records remain unchanged.
