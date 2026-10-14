# Special square matrix draft

Only `generate/scratch/17592186087697-draft.py` and this private evidence directory are owned by this draft. The registered numeric script and all numeric evidence are hashed in `baseline-hashes.json`; validation fails on any change, addition or deletion there. No database write, registration, engine edit, commit or asset generation is performed.

Run from the repository root:

```bash
.venv/bin/python generate/scratch/17592186087697-draft/validate.py
.venv/bin/python generate/scratch/17592186087697-draft.py --difficulty all --count 2 --seed 0 --format markdown
.venv/bin/python generate/scratch/17592186087697-draft.py --difficulty easy --profile raw-q-7829 --format json
```

The public API is `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` plus `generate_easy`, `generate_moderate`, `generate_hard`. Explicit replay uses each row of `source-cases.json`: pass its level, template, parameters and bank_profile. Raw q-7829 deliberately omits its absent source difficulty, correct ref and solution and remains ineligible for learning; method-q-7829 has an independently inferred D-only key and an authored solution. Raw profiles reproduce source wording and complete banks; normal method profiles parameterize the same masks and method.

`source.json`, `topic.json`, and `lesson.json` are exact immutable basis-2275 wrappers. `classification.md` describes source and curriculum scope; `template-extraction.md` and `extraction.json` document all components/banks; `review.md`/`review.json` show each original and two authored variants of every family at every level. `validate.py` checks actual displayed math, full source prose and missing-attribute parity, complete bank membership/equivalence, native grading, identities, boundaries, slot coverage, mutations and baseline hashes. `validation.json` records exact denominators and finite predicate-based task capacities.

Only easy source difficulty is observed. Moderate/hard labels use disjoint larger inspection workloads with the same three matrices and same predicates; their calibration is uncertain. No human UI raster inspection is claimed. Parent independent QA is required before acceptance. Raw q-7829's missing original attributes remain an explicit source limitation; inferred values do not count as recovered fidelity.
