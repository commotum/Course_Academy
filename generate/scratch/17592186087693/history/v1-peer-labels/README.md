# Determining the Dimensions of a Matrix

Generator: `../17592186087693.py`; source basis: math 1356. Read-only generation and memory-only native grading; no database writes.

From repository root:

```sh
.venv/bin/python generate/scratch/17592186087693/validate.py
.venv/bin/python generate/scratch/17592186087693.py --difficulty all --seed 20 --count 2 --format markdown
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` plus all three difficulty entrypoints. Parameters are exactly `entries` (rectangular nested list of bounded numeric TeX strings) and `name` (uppercase matrix letter). Explicit source cases/profiles are in `source-cases.json`; observed prompt masks and complete bank recipes are in `recipes.json`. Invalid explicit inputs and ineligible whole banks fail rather than change silently.

All eight sources replay their complete raw prompt, field layout and answer bank. Six existing worked solutions are exact; two missing solutions are authored. Eight existing field correct designations match; two missing legacy keys are inferred independently. Explicit evidence replay preserves the q-139406 wrong matrix label R and legacy EDB dot notation. Normal output repairs both. Moderate/hard are transparently authored peer variants of the same counting skill; each level has the same finite 25 ordered shapes. Entries, labels, layouts and levels do not inflate mathematical task counts.

`validation.json` separates source fidelity, supported repairs, displayed mathematics, identity, and actual grading. `review.md`/`review.json` include each original, each observed-bank variant, changed-dimension variants wherever eligible, and two normal authored variants per level. No unresolved mathematical/bank comparison is hidden. Native engine hashes are recorded; tests submit every choice, canonical and unevaluated equivalent blanks, and wrong counts. This is frozen for independent parent QA after validation passes.
