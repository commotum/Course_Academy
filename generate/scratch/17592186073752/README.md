# Basic substitution scratch generator

Only local review artifacts; no registration, database transactions, engine changes or plots.

```sh
.venv/bin/python generate/scratch/17592186073752/validate.py
.venv/bin/python generate/scratch/17592186073752.py --difficulty all --seed 42 --count 2 --format markdown
```

API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus generate_easy/moderate/hard. Observed profiles and original parameters are in source-cases.json; replay uses the same parameterized recipes as variants. source.json preserves all raw evidence. All 16 captured values, all eight nonempty field banks and six existing correct refs are compared. Four absent correct refs and three absent solutions are independently authored. Three raw prompts match exactly; all six match after documented presentation normalization. Existing solutions match after the system-brace escape; raw-exact solutions do not. Contextual default prompts add the omitted relation.

Moderate and hard are authored labels; hard keeps integer coefficients and unit isolation, with bounded rational results. source_4133 and source_5179 preserve numerical banks while honestly limiting their inferred intent; normal radios use a separate whole method-derived bank. validation.json separates fidelity, repairs, correctness, scope, variety and native grading. review.md shows every original, its repaired replay, an observed-profile variant and at least two authored defaults at every level. No images require rendering.
