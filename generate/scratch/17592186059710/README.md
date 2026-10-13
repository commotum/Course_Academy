# Component-form vectors — local steps 3–7

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186059710/validate.py
.venv/bin/python generate/scratch/17592186059710.py --difficulty all --seed 7 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186059710.py --difficulty easy --template left_scale --profile raw-q-70402 --format json
```

Import the script and call `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` or the easy/moderate/hard wrappers. Only authored supported radio fields are offered. Exact source-case parameter dictionaries are in source-cases.json. `raw-q-*` profiles preserve original absent fields/difficulty/solutions/correct refs; they are evidence-only and cannot be graded directly when fields/refs are absent. `completed-q-*` profiles independently supply the missing components. Completed historical q70402 is still evidence-only because its distractor intentions are opaque. Normal defaults sample all eligible observed easy families and complete banks before parameters, plus explicitly authored moderate/hard same-method extensions.

Explicit invalid dictionaries, unused scalar aliases, out-of-level parameters and colliding complete banks raise `ValueError`. Parameters are never silently changed. Random sampling rejects whole instances. Identity is stable under seed/order changes for fixed displayed content. Separate task fingerprints exclude complete banks, notation/spacing, seed and unused inputs (unused inputs are rejected).

Evidence: classification.md; template-extraction.md; source-distractor-ledger.json; source-cases.json; fidelity.json; plot-extraction.md; review.md/review.json; validation.json; engine-input.json/engine-report.json. The validator independently parses actual displayed operands, operator, bank and every worked row, including ordered distributed terms; it runs the real memory-only `learning::grade_field` harness for all completed/normal options. Radio grading verifies selected identities; mathematical value checks are independent.

There are four source prompts, two available source worked solutions and two complete original banks (10 values). All correct refs are missing; correct-designation fidelity has denominator zero. Missing source fields have no observed layout claim. Moderate/hard are authored level definitions. Sampled task counts are lower bounds, not exhaustive finite-domain claims. No database writes, registration, engine changes, commits, or plots.
