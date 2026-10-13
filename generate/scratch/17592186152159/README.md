# Scalar line-integral setup generator

Local review generator only; math basis1356. No engine/database edits or writes. Scope: reduce scalar line integrals on graphs y(x) to t-integrals using ds. Easy source patterns, authored moderate/hard peers. No plots or evaluating-integral questions.

```sh
.venv/bin/python generate/scratch/17592186152159.py --difficulty all --seed 12 --count 2 --format json
.venv/bin/python generate/scratch/17592186152159/validate.py
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and individual difficulty functions. Radio only. `observed_evidence` retains complete raw banks, including two equal-wrong-option banks; it is explicitly review-only. `observed` rejects ambiguous banks. Default `authored_operations` is a separate complete operation bank. Explicit input errors never silently resample.

`source-cases.json` gives all 9 public-API original-parameter replays. 45/45 exact choices, 8/8 present original designations, 8/8 present worked solutions. One source lacks a designation, solution and difficulty; these are authored/inferred with separate counts. One legacy integral subscript gets a presentation repair. See classification and extraction for bounds, source anomalies, missing-level rationale, complete bank mapping and interpretation limits. `review.md/json`, `validation.json` and native `engine-validation.json` record verified outputs; `freeze.json` contains artifact hashes after worker validation. Parent independent QA is still required.
