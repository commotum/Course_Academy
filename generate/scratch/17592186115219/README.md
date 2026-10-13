# Two-base exponential generator

Script: `../17592186115219.py`. Implements steps 3–7 only, with exact SymPy mathematics, deterministic shuffling, stable owned UUIDs, and no database writes or plots.

```sh
.venv/bin/python generate/scratch/17592186115219/validate.py
.venv/bin/python generate/scratch/17592186115219.py --difficulty all --seed 42 --count 2 --format markdown
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`, plus `generate_easy`, `generate_moderate`, `generate_hard`. Templates are source IDs from `source-cases.json`. Normal profile `authored-method` produces complete five-choice radio items. `observed:<source-id>` replays the original parameterized prompt, whole bank and solution while preserving omitted attributes; these opaque historical continuations are **evidence-only, ineligible for learning**. Source cases supply exact replay arguments. Explicit invalid parameters reject rather than silently changing input.

Scope: rewrite both displayed bases as powers of a familiar common base, apply power rules, then solve a linear equation. Easy uses adjacent powers, unit variable coefficients and one shift. Moderate uses two shifts or one scaled exponent. Hard retains the source reciprocal and product-rule families. Normal authored banks use the actual displayed operations. Every available source prompt/solution is reproduced exactly; original missing layout/correct refs cannot count as recovered designations.

`validation.json` separates exact source fidelity, absent source attributes, actual printed mathematics, native grading, variety and explicit guard tests. `engine-input.json` and `engine-validation.json` expose actual application `learning::grade_field` tests; engine hashes document read-only provenance. `freeze.json` hashes script and evidence. Historical distractor intent remains underdetermined; no learner-facing error explanations are invented.
