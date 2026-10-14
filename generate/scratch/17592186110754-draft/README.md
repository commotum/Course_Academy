# Unit-circle coordinate draft

Draft only: `../17592186110754-draft.py`; registered numeric generator and complete evidence baseline remain untouched. No EDB operations or registration.

Verify: `.venv/bin/python generate/scratch/17592186110754-draft/validate.py`

Preview: `.venv/bin/python generate/scratch/17592186110754-draft.py --difficulty all --count 2 --format markdown`

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` plus all three level entrypoints. Templates coordinate-equation/coordinate-value; defaults method-equation/method-value. Explicit raw:q-N profiles preserve complete original bank patterns and absent attributes through the public API; they are evidence-only. Parameters are n,d,known, representing supplied sqrt(n)/d and known=x|y. Explicit inputs violating level guards reject instead of resampling.

Moderate/Hard are authored workload policies; the source contains five Easy labels and two omissions. See template-extraction.md, review.md, source-cases.json, validation.json and native-source-inspection.json. Native checks are memory-only `learning::grade_field`. There are no plots and no free-entry fields.
