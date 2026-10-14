# Known-solid flux generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186133930/validate.py
.venv/bin/python generate/scratch/17592186133930.py --difficulty all --seed 11 --count 2 --format markdown
```

The public API has `generate_easy`, `generate_moderate`, `generate_hard`, and `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`. Normal profiles are `method`; `raw-q-162410` and each other captured source identifier select evidence-only original banks. Raw parameters are `{"k":1}` through `{"k":3}`: a uniform field multiplier with unchanged geometry. Scalar historical distractors are retained by homogeneous scaling, with no claim that their original error operations were recovered.

Normal easy/moderate parameters are `k=1..3` and `geometry`: `['cylinder',r,h,axis]`, `['box',a,b,c]`, or `['sphere',r,[cx,cy,cz]]`. Cylinders require `r,h=2..4` and their source axis; boxes use lengths1..4; spheres use radius2..5 and source nonzero-center support, with nonzero shifts in ±1..4. The complete bank must be distinct: any collision rejects the whole explicit instance; sampling resamples only parameters after choosing the family/bank. Hard parameters are `a,b=1..3`, `c=2..6`, and the same shifted sphere geometry; field is `(y²-a x²+2bxy, cy-by²,2axz)`. Difficulty claims are authored only for hard.

Ten originals have exact prompts, complete source solution chains and complete banks. One original has an extra legacy radio field without a correct reference. Public raw replay preserves this missing attribute and the duplicate layout; native grading of that entire malformed record fails. The authoritative second field is graded in an explicitly repaired fixture; normal generation owns one valid radio field. Raw records are ineligible for learning, including otherwise valid opaque historical banks. No EDB writes or engine edits.

See `classification.md`, `template-extraction.md`, `plot-extraction.md`, `source-cases.json`, `review.md`, `review.json`, `validation.json` and `engine-report.json`. Plots are Matplotlib PNGs with geometry/renderer sidecars. Mathematical task fingerprints exclude incidental sphere center translation; complete content identities retain the actual prompt, solution, complete bank, field layout and difficulty, and do not depend on seed or option order.
