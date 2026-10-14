# Scalar line integrals with substitution

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186133827/validate.py
.venv/bin/python generate/scratch/17592186133827.py --difficulty all --count 2 --seed 10 --format json
.venv/bin/python generate/scratch/17592186133827.py --difficulty moderate --profile raw:q-76187 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`, plus separate easy/moderate/hard entrypoints. `field_type` accepts radio only. Normal bank profile is `method`; all six historical banks are public as `raw:q-ID`, with scale integers 1–6. Exact source cases use scale 1. Raw profiles are explicitly evidence-only, with observed attribute omissions and teaching defects retained. Correct designation for q-76187 is inferred only in normal output. Difficulty routing on that raw case is API metadata, not a recovered question rating.

Normal finite domains are defined by `domain(template)` and apply identically to explicit inputs and sampling. Family/profile are selected first; any collision rejects the entire bank. The finite task counts in `domain-counts.json` exclude seed/order/profile/notation aliases and retain the actual assessed curve, integrand and parameter interval. Different mathematical representations with the same task are normalized by SymPy; bank and cosmetic identities remain outside the mathematical fingerprint. Task diversity is finite, not unlimited.

`validate.py` parses the actual displayed prompt, coordinate derivatives, speed rows, substituted f, setup integrands, u substitution/differential, primitive, and both individual endpoint values. It compares all raw option values and present designations separately from correctness and native ID grading. No blanks occur: equivalent blank-entry tests are inapplicable. Native grading uses the existing `check-engine` binary and creates only local fixtures; no EDB operations.

Review files contain originals, a generated evidence-only scale variant for every historical bank, and two eligible authored-bank examples for each normal family at all three levels. Source anomaly details and opaque-bank interpretation limits are in `template-extraction.md`.

Root QA corrected the sine-line endpoint fraction mask in version2: every TeX command is now a raw string component. Formatting validation rejects unintended control characters, with a form-feed regression; generated previews and validation were rebuilt.
