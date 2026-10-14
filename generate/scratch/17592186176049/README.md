# Tangent-property generator

Local generator for KP17592186176049, `math` basis 1356. Stops at steps 3–7; no database writes.

```sh
.venv/bin/python generate/scratch/17592186176049/validate.py
.venv/bin/python generate/scratch/17592186176049/build_evidence.py
.venv/bin/python generate/scratch/17592186176049/check_concurrency.py
.venv/bin/python generate/scratch/17592186176049.py --difficulty all --seed 20 --count 2 --format json
.venv/bin/python generate/scratch/17592186176049.py --difficulty hard --template two_identity_properties --seed 21
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and each level entrypoint. Source cases in `source-cases.json` supply exact template/parameters and `observed:<template>` profiles; the incomplete source raw replay omits its original missing keys and is ineligible for learning. Normal replay/completion uses profile `completed`. Authored catalogs use `authored-subsets`.

Review: `review.md` originals and two labeled variants of every observed bank, plus two examples at each authored level and the hard extension; complete generated records in `review.json`. Extraction/classification record difficulty authorship and finite scope. `native-grading.json` reports real engine checks; source fidelity is separate in `source-replay.json`. The validator enumerates the finite parameter catalogs, independently parses all printed propositions and periodicity chains, checks teaching locations, key presence, subset eligibility, source fidelity, option-order identity invariance, explicit invalid inputs and mutation regressions. It tests each displayed choice through the application grader. `tangent.png` is a fixed Matplotlib graph, not an answer-dependent diagram.

Limits: no observed easy/moderate labels; their bounds are authored from the lesson and graph prerequisite. q-27660 lacks a source key/solution/level; its completion is explicitly authored. Graph geometry and readability were visually reviewed, without claiming pixel-exact source styling.
