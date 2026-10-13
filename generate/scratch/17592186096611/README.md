# Constant times e^x plus a polynomial

Validated generator registered for this KP as `337ca211-135e-5973-81fe-043f1cf73b4b` at math basis 1899. Implements easy, moderate, and hard with bounded exact integer coefficients. Missing hard examples are an authored canonical-example extension using two power-rule reductions. Nine original profiles preserve all 34 captured answer-bank values, including unrated originals and the extra legacy blank value. Missing source correct refs are independently inferred; malformed mathematics and missing contextual definitions are documented separately.

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186096611.py --difficulty all --seed 4 --count 2 --format json
.venv/bin/python generate/scratch/17592186096611/validate.py
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`, and separate `generate_easy`, `generate_moderate`, `generate_hard`. Source recipes use explicit `observed_<template>` profiles; cases and original parameters are in `source-cases.json`. Blank defaults use `fragment`, radio defaults use `authored_method`. Unknown profiles, extra/missing parameter keys, invalid level/field combinations, and invalid parameters fail. A complete collided bank rejects the whole instance. No literal-source answer return branches exist: the same mathematical recipes render original and changed parameters.

`validate.py` independently parses the actual displayed prompt, all solution rows, and every answer value. It checks complete source-bank matching, source prose/ordered stages, signed formatting, unreduced mathematical stages, identities, parameter bounds, and the real `learning::grade_field` via the captured shared harness. Review contains all originals, observed replays, and two generated examples of each family (at least two per level).

Question identity includes version, displayed prompt, fixed solution, response shape, complete bank, and correct value; option shuffle and seed do not change it. The mathematical fingerprint uses the symbolic derivative and response/evaluation demand, excluding incidental function names, branch thresholds, constant terms that differentiate to zero, profiles, banks, and layout. Polynomial derivative coefficients still count even when an evaluation at zero later removes their contribution, since termwise differentiation is part of the assessed method.


Replenishment verified at basis 1899: 13 genuinely distinct generated questions
(3 easy, 5 moderate, 5 hard). Conservative current inventory has 5 validated,
unseen, unreserved distinct tasks per supported level; native inventory has no
remaining job for this KP. All nine source questions and the canonical example
are unchanged. Only additive content and generator-reference facts were
committed under `:application/ca-engine`; learner history was unchanged.

`replenish.py` reuses the application EDB integration, locks `api.lock`, captures
current inventory, validates immutable source evidence, deduplicates by
independently parsed mathematics, exercises the current native grader, previews
installed validation specs, retains the exact basis-guarded request, and verifies
its receipt and exact-basis readback. Retained evidence is in
`reference/replenishment/basis-1898/`. The current native source/replay check has
64 accepted and 138 rejected cases; the committed batch has 21 accepted and 28
rejected grading checks, with no unresolved results.
