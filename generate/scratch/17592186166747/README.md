# One independent variable chain rule

Run from the repository root:

```
.venv/bin/python generate/scratch/17592186166747/validate.py
.venv/bin/python generate/scratch/17592186166747/variety.py
.venv/bin/python generate/scratch/17592186166747.py --difficulty all --count 2 --seed 42 --format json
```

The script implements easy/moderate/hard and `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`. Normal output uses `method_branches`; the public `observed_raw` and `observed_repaired` profiles preserve each complete original bank and are explicitly evidence-only/ineligible. Replay profile parameters are `{h: integer between -3 and 3}`; normal parameters are integer n,a,b,h,k with the per-level guards in the script. See source-cases.json for all twelve original replay calls.

Validation reads the actual prompt, every partial and component derivative, each substitution equality and each final arithmetic/product row, and all choices with an independent TeX reader and SymPy. Native owned radio selection is tested separately with the current real application check-engine. There are no blank fields, so typed-equivalent submission testing is inapplicable. Source missing correct/solution/difficulty, domain omissions and opaque distractor intent are explicitly recorded. Scope stops at steps 3–7; no database or registration writes.
