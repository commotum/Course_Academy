# General logarithm chain-rule generator

Private, unregistered numeric pair. No EDB, registration, engine, shared QA or git mutations. The absent-pair baseline is in `registered-baseline.json`.

Run `.venv/bin/python generate/scratch/17592186092265.py --difficulty all --count 3 --seed 7` for JSON, or add `--format markdown`. Public API: `generate(level, seed=0, template=None, parameters=None, profile="source", field_type=None)`. `source_replay(source_id,"observed_raw")` returns immutable original records; `"observed_served"` returns corrected/completed originals. Supported levels are easy, moderate and hard.

`validate.py` independently reads printed prompts and every operative math stage, replays all original banks, rejects mutation regressions and exercises the frozen native engine in small batches. `review.md` and `review.json` contain every original plus two meaningful variants per source-specific family. Normal instances carry exact parameters, domain, excluded poles, version, source basis, whole-bank profile and task identity. The source cannot calibrate a finer difficulty progression; none is asserted.

`private_readback.py`, `private_scalar.py` and `private_math_format.py` are private frozen dependencies loaded by explicit path. All file SHA-256 hashes are sealed in `frozen-manifest.json` after validation. Any native equivalence gaps are reported in `engine-validation.json` without excluding valid mathematics.


Native-equivalence limitation: the frozen engine accepts canonical keys, but broader valid equivalents can return “answer comparison has unresolved domain differences.” This includes the original unreduced radical chain 7/(2 sqrt(7x) sqrt(7x) ln4) on x>0 and logarithm-power rewrites ln4=2ln2, ln8=3ln2, ln9=2ln3. `equivalent-probe-validation.json` records the mathematical expectation separately from the actual grader result. All valid parameters and outputs remain available.
