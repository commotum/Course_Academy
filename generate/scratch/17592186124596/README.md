# Cylindrical chain-rule generator

Step-7 local draft; no database operations, registration or engine edits. Seven practice originals at math basis 1356: four easy and three moderate. Two authored hard polynomial families are anchored to the canonical example and cylindrical tutorial. Every question uses one five-option radio field; no blanks or plots.

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186124596/validate.py
.venv/bin/python generate/scratch/17592186124596.py --difficulty all --seed 18 --count 2 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Complete explicit parameters include `name`; source-cases.json gives all seven original tuples and bank profiles. Invalid tuples raise. Default profile is `authored_operations`; `observed` replays the entire parameterized original bank. Wrong-choice source intent is often underdetermined and remains explicitly unresolved, separate from default method-based banks.

Classification.md gives per-level bounds, ordered curriculum route and the q-95172 first-chain-row repair. Template-extraction.md accounts for every source choice. Review.md/review.json show originals, replays and two changed examples for every template/profile, including hard. Validation.json separates raw strings, notation normalization, complete bank/prose/ordered stage fidelity, mathematics and actual native grading.

The validator reads the actual displayed function and every solution equation, including zero contributions and uncollected sums; tests complete banks, all six supported function labels, identities, invalid parameters and meaningful fingerprints; and invokes real `learning::grade_field` with each owned correct/wrong UUID. Blank-equivalent-entry testing is inapplicable to radio fields. Native binary/source hashes and the fully checked generator SHA are recorded.
