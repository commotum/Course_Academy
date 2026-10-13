# Scalar projection generator

Run `.venv/bin/python generate/scratch/17592186105916/validate.py` from the repository root. Preview `.venv/bin/python generate/scratch/17592186105916.py --difficulty all --count 2 --format json`.

Public API: generate_easy, generate_moderate, generate_hard and generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None). Source-cases.json specifies every explicit source replay. `parameters` must contain coefficient (exact rational string), radicand (1/2/3), angle (observed familiar integer degrees), unit (degrees/radians), and distinct vector letters a,b. Original source profiles are public evidence-only, with all missing attributes preserved. Default output has supported complete fields and authored method-derived banks; absent moderate/hard labels are authored design claims.

All 17 sources, complete banks, solution prose/stages and optional-key presence are independently checked. Native grading uses the real memory-only grade_field harness; it is reported separately from bank math/fidelity. The source lacking a correct reference is excluded from native grading only, with its evidence and mathematical validation retained. No DB writes, engine edits, plots, image models or commits. Frozen version scalar-angle-1; see validation.json for counts and limits.
