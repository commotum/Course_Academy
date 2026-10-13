# Ellipse axis-length generator

Run `.venv/bin/python generate/scratch/17592186087841/validate.py`, then `.venv/bin/python generate/scratch/17592186087841/build_evidence.py` to regenerate private review evidence. Preview: `.venv/bin/python generate/scratch/17592186087841.py --difficulty all --count 2 --seed 42 --format markdown`.

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and three difficulty entrypoints. Parameters are exact `dx`,`dy` squared radii. Explicit observed radio profiles use `observed_q-N`; source blank layouts use `source_q-N`. All replay cases are in source-cases.json. Default banks are separately authored; observed profiles are explicit evidence requests.

21/21 source banks,81/81 option values,21/21 prompts,20/20 present worked solutions and28/28 present correct refs match. One source lacks difficulty, solution and correct ref; raw presence parity is verified, completion is separate. 90 authored instances plus21 changed-source profiles are mathematically checked. Native checks104 accepted and150 rejected; raw missing-ref evidence is not grader-compatible and is excluded from native fixtures only, never source coverage. Six opaque numerical transforms have no recovered intent. Moderate/hard scope is authored bounded rational arithmetic of the same ellipse method. No plots or DB writes.

manifest.json freezes producer/input/output SHA256 hashes; evidence is local review data. Parent independent QA remains separate.
