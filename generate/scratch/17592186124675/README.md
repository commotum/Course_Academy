# Inhibited growth scratch generator

Generator: `generate/scratch/17592186124675.py`. Run from the repository root:

```bash
.venv/bin/python generate/scratch/17592186124675.py --difficulty all --seed 42 --count 2
.venv/bin/python generate/scratch/17592186124675.py --difficulty hard --template q-335619 --profile q-335619_empirical --format json
.venv/bin/python generate/scratch/17592186124675/validate.py
```

The API offers `generate`, `generate_easy`, `generate_moderate`, and `generate_hard`. All levels use the observed five-option text radio format. Defaults use a complete five-option profile with four documented operation-derived errors and reject nonphysical values before rounding; explicit empirical source replay profiles retain every original bank while labeling distractor intent unknown. The eight supplied solutions replay verbatim. q-37389 has an explicitly authored hard assignment, reconstructed solution and mathematically verified 468-egg designation; its missing source designation is not counted as matched.

`source.json` is unchanged basis-1356 evidence. `extract.py` reproduces numeric-role skeletons. `classification.md` and `template-extraction.md` describe source grouping, all four extraction stages and scope. `source-bank-math.json` maps every option. `display_math.py` independently solves the displayed prompt and evaluates every displayed worked relation. `validate.py` fails on fidelity, math, scope, layout, identity and real grading failures, with deliberate mutation probes. `review.md` and `review.json` contain originals and authored/empirical generated variants for each template and all levels. No database writes or shared engine changes.
