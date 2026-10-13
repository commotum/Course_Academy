# Parametric coordinate ranges

Scratch generator: `../17592186087722.py`. No database writes or registration. Requires the project `.venv` and existing shared native grader.

```sh
.venv/bin/python generate/scratch/17592186087722/validate.py
.venv/bin/python generate/scratch/17592186087722.py --difficulty all --seed 21 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186087722.py --difficulty moderate --template q-16199 --profile observed:q-16199 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and the three level wrappers. Observed recipes accept `sx,sy` positive integers 1..6. Source cases use unit scales; source profiles transport complete source banks. Authored endpoint banks are the normal radio default. Explicit invalid inputs fail without replacement.

See classification.md for authored level scope, template-extraction.md for complete prompt/field/bank/solution extraction, and review.md/review.json for all original replays, variants of every observed bank, and all three levels. validation.json separates observed matches from missing-field/designation repairs; engine-validation.json reports real application grading.

Remaining evidence limits: q-16203/q-16205 lack observed correct refs/rating/solution, and q-73604's original assessment widget is absent locally. Their supported authored fields/designations are clearly marked. Opaque source distractor bounds are preserved as complete coordinate-transport profiles and carry no claim of recovered error intentions.
