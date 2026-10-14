# Local scalar-matrix generator

`../17592186059740.py` builds exact, deterministic easy/moderate/hard entrywise scalar multiplication. It stops after guide step7. No EDB access, database writes, registration, shared edits or plots.

```sh
.venv/bin/python generate/scratch/17592186059740/validate.py
.venv/bin/python generate/scratch/17592186059740.py --difficulty all --seed 42 --count 2
.venv/bin/python generate/scratch/17592186059740.py --difficulty easy --profile raw_986 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy/moderate/hard`. Exact parameters are `{ "k": 3, "matrix": [[4,-5],[-2,"1/3"]], "name": "A" }`. Explicit invalid parameters raise, while random whole-bank collisions reject the entire instance. Never use float parameters. Public raw profiles replay every original using recipes rather than captured payload returns; they are evidence-only and preserve missing attributes. Normal outputs repair missing information and the q320075 introductory coefficient, and align lower-row blank padding. No feedback is invented.

`classification.md` documents scope and authored levels; `template-extraction.md` maps every bank and solution component. `source-cases.json` is the complete original replay list. `review.md/json` show raw originals, changed raw profiles, normal repairs and generated examples. `validate.py` independently reads printed matrices/products/prose, checks full-source fidelity, level bounds, whole-bank ambiguity, formatting, deterministic/content/math identity, mutation failures and real memory-only native grading. `validation.json` records worker findings with parent QA pending. `native-input.json` and `native-grading.json` are engine evidence.

q979/q986 source keys, solutions and ratings are absent. Normal keys are independently derived. q986's compound last-row distractor has underidentified historical intent; it is available solely as a public raw bank, never a normal default. Moderate/hard labels are authored design claims. Calculator requirement remains unknown. Source wrappers stay unchanged at basis2275.
