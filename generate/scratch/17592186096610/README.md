# KP17592186096610 local generator

Scope: differentiate ae^x+c and optionally evaluate the derivative at a supplied point. Easy faithfully covers all seven captured practice originals. Moderate and hard are authored bounded exact-arithmetic peers; see classification for rationale and guards. All work stops after guide step 7. No database writes.

Verify from the repository root:

```sh
.venv/bin/python generate/scratch/17592186096610/validate.py
.venv/bin/python generate/scratch/17592186096610.py --difficulty all --seed 8 --count 2 --format json
```

Source replay uses `source-cases.json` with the normal `generate` API and explicit original profiles. Raw snapshot wrapper is in `source.json`; its provenance is unchanged. `review.md`/`review.json` show all originals and two changed variants per source profile, plus two peers for each authored missing level. `native-input.json` and `native-report.json` exercise the actual application's grader in memory-only fixtures, with canonical, meaningful equivalent, wrong-variable/sign and wrong-value responses.

Fidelity: 28/28 source answer values, 20/20 radio distractors, 7/7 whole banks, 7/7 raw prompts, 5/5 available correct designations; two missing refs independently inferred. Worked solutions: 4/5 raw exact, 5/5 whitespace-normalized exact; two absent legacy solutions explicitly authored. No mathematical repairs. Source scalar distractor intent remains unresolved where evidence is insufficient; those complete source banks are replay profiles, while authored scalar defaults use defensible operations. No native-grader unresolved results.

`freeze.json` records final private-file hashes for parent QA. After freezing, the worker will make no changes without a parent request.
