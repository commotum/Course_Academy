# Overflow-onset scratch generator

Frozen at step 7 for independent root QA. Owns only this evidence folder and ../17592186229183.py. No database operations or plots.

Verification: `.venv/bin/python generate/scratch/17592186229183/validate.py`

Preview: `.venv/bin/python generate/scratch/17592186229183.py --difficulty all --count 2 --seed 5 --format markdown`

Public API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), and generate_easy/moderate/hard. Parameters are exactly H (capacity), v (initial volume), q (initial amount), c (incoming concentration), rin and rout. Use strings for exact rationals. Profiles: method (normal default), observed:<source-id> (raw public evidence), repaired:<source-id> (completed opaque public evidence, still ineligible). Source replay must use source-cases.json parameters; changing numerical parameters renders all masks through the same ordinary API.

All normal records have one five-option radio and a complete fixed worked solution. Source raw replay preserves duplicate fields, missing difficulty/solution/correct keys and valid single-backslash LaTeX suffixes. These records are explicitly evidence-only. Native tests distinguish supplied source fields from completed inferred fields; omitted original keys cannot count as matched keys. Decimal rounding is half up to one decimal, including 93.75 → 93.8.

See classification.md, template-extraction.md, decoded-byte-evidence.json, validation.json and review.md. Sampling tests expose 100 distinct mathematical tasks at each level, excluding context and profile aliases. A mathematical fingerprint includes the actual physical quantities because each changes the ODE, initial condition, or endpoint; content identity additionally includes difficulty, complete displayed bank, prompt and solution. Seed and order do not alter identity.
