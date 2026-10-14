# Basis-2275 alternative-vector draft

Script: `generate/scratch/17592186059713-draft.py`. Evidence is private to this directory. The registered numeric generator and its evidence remain unchanged, checked against `baseline-hashes.json`. No registration, database operations, engine edits or commits.

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python generate/scratch/17592186059713-draft/validate.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python generate/scratch/17592186059713-draft.py --difficulty all --seed 27 --count 2 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and documented `generate_easy`, `generate_moderate`, `generate_hard`. Explicit invalid inputs fail without resampling. Only supported radio fields are used in normal output. Raw fieldless evidence intentionally omits fields.

Easy samples both sum masks, subtraction and scalar multiplication. Moderate pu±qv and hard pu-(qv±rw) are authored missing-level backbones using the already taught 2D componentwise operations and alternative arrow notation. Within each template, grouping, supplied-vector count and ordered stages stay fixed. Allowed signs/coefficient/coordinate slots vary at equal workload; no direction, norm, dot product, geometry, 3D, unknown solving or representation change is added.

Source replay: `raw-q-1323`, `raw-q-1386`, `raw-q-1300`, `raw-q-1324` preserve original bank values, whole available prose/solutions and raw omissions. Opaque q-1323 bank remains evidence-only; normal subtraction uses a separately authored complete operation bank. Legacy caret-arrow text is raw evidence; normal teaching uses supported observed overset-arrow TeX. Five exact independent inventory records are in `independent-inventory.json` and have public `raw-inventory-<db-id>` replay profiles. They are current authored inventory, not recovered MA difficulty evidence.

Results in `validation.json`: original MA fidelity 4/4 prompts, 2/2 available solutions, 2/2 complete banks, 10/10 values and 8/8 distractors; captured correct refs 0/0, with 2 missing. Inventory coverage 5 exact records, 5 prompts/solutions/banks/correct designations and 25 values. Independent mathematical QA checks 1,200 generated records and 4,400 solution stages, 450 changed raw replays, 3 valid boundary cases, 9 invalid inputs and 8 mutation failures. Native grading accepts 1,209 correct selections and rejects 4,836 wrong selections, with no unresolved results. Four raw MA originals remain ungradeable because of their captured omissions; their completed learning versions are independently checked and graded separately.

Exact easy mathematical task capacities: sum 63,342, subtraction 115,668, scalar 1,406 after conservative aliases. Witnessed moderate/hard lower bounds: 1,599/1,600. Full details/slot coverage are in `capacity.json` and explicit witness parameters in `capacity-witnesses.json`. Letter case, order, seed and bank aliases do not count as task variety; cosmetic case does not change content IDs.

`source.json`, `topic.json`, `lesson.json` preserve frozen basis-2275 wrappers. Read `classification.md`, four-stage `template-extraction.md`, `choice-map.json`, `plot-extraction.md`, `source-cases.json`, `raw-replay.json`, `independent-replay.json`, `review.md`/`review.json`, `native-input.json`/`native-report.json`. Runtime is Python 3.13.5, SymPy 1.14.0; installed Matplotlib 3.11.2, with no generated assessed plots. Script/source/native hashes are in `validation.json`.
