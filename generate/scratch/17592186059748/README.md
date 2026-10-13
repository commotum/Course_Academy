# Integer 2x2 determinant generator

Verify using `.venv/bin/python generate/scratch/17592186059748/validate.py` from the repo root. Preview with `.venv/bin/python generate/scratch/17592186059748.py --difficulty all --count 2 --seed 42 --format markdown`.

API: generate_easy, generate_moderate, generate_hard, or generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None). Parameters require integer a,b,c,d and one supported name. Observed profiles are q IDs; authored_operations is the default. No DB access or registration.

All nine original prompts/banks are covered. Eight captured solutions/designations have full observed fidelity; q-11648 has a captured prompt/bank but an authored moderate rating, independently inferred correct designation and authored solution. Hard is explicitly authored direct integer determinant arithmetic. Six original radio banks are opaque scalar covariance replay profiles; default banks use complete defensible determinant operations. See validation.json for denominators and native grading checks; review.md displays all originals/replays and labeled variants at every level.
