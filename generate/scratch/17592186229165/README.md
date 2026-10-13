# Exponential first-order initial value problems

Frozen generator `../17592186229165.py` covers observed easy nonresonant and moderate resonant IVPs, plus explicitly authored hard two-component IVPs using the preceding lesson methods. It stops at generation/validation; no database writes.

```sh
.venv/bin/python generate/scratch/17592186229165/validate.py
.venv/bin/python generate/scratch/17592186229165.py --difficulty all --seed 9 --count 2 --format json
.venv/bin/python generate/scratch/17592186229165.py --difficulty moderate --profile q-332936 --seed 9
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and three named level entrypoints. Only blank fields are supported. Source-named profiles replay normal complete banks; `raw:q-…` preserves original missing answer/solution data for the two unrated originals. Their normal profiles add independently verified authored answers, solutions and labels. Explicit invalid inputs fail without resampling.

`source.json` preserves the basis-1356 capture; `source-cases.json` includes all 15 practice sources. `classification.md` and `template-extraction.md` separate source observation from authorship. `validate.py` checks byte-exact prompts/full solutions and complete source banks, parses actual displayed ODE/trial/derivative/substitution/coefficient/general/initial stages, checks deterministic identity and workload guards, and invokes the actual memory-only application grader. `review.md`/`review.json` show all original profiles, two variants per profile, and at least two examples for each level and authored hard family. `validation.json` reports separate available/raw/completed denominators; `native-report.json` records actual grading.

There are no source mathematical corrections or slash-normalization repairs. Two equivalent answer alternatives in each of q-332936/q-332938 are preserved. The two absent original correct designations are excluded from the 13/13 designation-match denominator, retained as raw evidence and completed only in the separately labeled authored normal presentation.
