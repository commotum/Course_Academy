# Half-open number-line generator

```sh
.venv/bin/python generate/scratch/17592186059828/validate.py
.venv/bin/python generate/scratch/17592186059828.py --difficulty all --seed 29 --count 2 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and three difficulty entrypoints. One five-choice radio template. Exact finite catalogs contain 52 easy, 42 moderate and 80 hard mathematical tasks. Defaults are authored; the two unrated original complete banks remain parameterized explicit raw profiles. Raw profiles retain missing fields and are evidence_only. q-31762 has both-open source geometry; its normal repair closes the left endpoint. Normal output is strictly one bounded half-open interval.

source-cases.json supplies complete raw replay and normal repair calls. validation.json separates raw fidelity from authored repairs, correctness and native grading. review.md/review.json contain raw originals, normal repairs and at least two variants per level for every normal complete bank. Source PNGs are independently read back using each original's axis fit. Plots use Matplotlib with already cached read-only dependencies; assets and sidecars publish atomically. No EDB operations or shared edits. Frozen code remains subject to parent QA.
