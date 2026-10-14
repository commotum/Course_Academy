# Interval invertibility from descriptions

Validated current generator: `generate/scratch/17592186124474.py`, version `1.1.0-checkbox`. Reuses the existing mathematical templates and generator identity; the current public API emits one field-owned Boolean checkbox for each interval I, II, III. All 12 current source prompts, complete solutions and 36 Boolean banks replay at basis 2222. Source content and learner history remain immutable.

```sh
.venv/bin/python generate/scratch/17592186124474.py --difficulty hard --seed 8 --count 2 --format json
.venv/bin/python generate/scratch/17592186124474/validate_checkbox.py
.venv/bin/python generate/scratch/17592186124474/replenish.py
```

`generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` supports easy, moderate and hard, with `field_type="checkbox"`. Historical radio fidelity is retained through `generate_legacy` and `validate.py`. Current source replay with `profile="current:q-66482"` retains the original identity and is evidence only. Historical `raw` q-66785 also remains evidence only; the current captured question already has all three fields.

Easy has exactly two distinct tasks: a nonconstant line passes the one-to-one test on all three nondegenerate intervals, whereas a constant fails all three. Four existing nonconstant-line source identities do not provide four distinct tasks. Only the constant task is fresh. Do not generate another line by changing coefficients, seed, identity or interval order.

Authored moderate has 12 unordered branch-domain structures. Authored hard has 15 unordered pairs of finite branch-domain types plus a crossing interval; its noninteger vertex has reduced denominator 2–4. Hard is an explicitly authored same-method extension supported by the interval/vertex comparison backbone, not an observed source difficulty. Different translations, folded formula families and Roman permutations do not increase these counts. Earlier ordered counts of 72/90 in historical validation measure render coverage only and are superseded as capacity claims.

Classification and template extraction retain source-specific masks and historical radio banks separately from the current checkbox contract. Both validators check printed mathematics and worked solutions. `checkbox-validation.json` records source fidelity, catalog coverage, a changed-target check with the function fixed, semantic alias rejection, and actual application grading. Plot extraction and visual review remain in the package; the replenishment's constant and rational examples require no new plots.

The scoped worker rechecks native inventory and source evidence at a current basis under `.local/learning/requests/math/api.lock`, retains the exact prepared EDN and durable request, submits with a basis guard through the existing EDB integration, verifies the receipt and additive attribution at its exact after basis, then rechecks inventory. Evidence and receipts are in `reference/replenishment/`; the job outcome retains the easy finite-limit shortage explicitly.
