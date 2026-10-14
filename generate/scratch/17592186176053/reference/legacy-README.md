# Cosecant general properties — local draft

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186176053.py --difficulty all --seed 17 --count 2 --format json
.venv/bin/python generate/scratch/17592186176053/validate.py
.venv/bin/python generate/scratch/17592186176053/build-evidence.py
```

Scope: untransformed y=csc x, three property statements, five-choice radio. Normal moderate sampling serves all seven source masks. Easy and hard are authored workloads with finite catalogs (80 and 12,544 objects); moderate supports 3,326 parameterized tested-object instances across its seven masks. See classification and extraction for finite conceptual limits and source-specific guards. Frozen math capture is basis 1356; this work stops after step 7.

`generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and individual difficulty entrypoints are supported. Moderate templates are q-42912, q-65310, q-103811, q-103814, q-65307, q-65308, q-103812. Profiles `observed:<template>` are public evidence-only replay retaining omissions and raw malformed TeX; `method:<template>` are normal supported records. Easy template basic_properties and hard indexed_properties use subset-errors. Exact source parameters are in source-cases.json. Explicit bad inputs raise ValueError rather than silently changing them.

Original unchanged graphs resolve under `/media/jake/SSD/EDB/math/`; their references/hashes are in plot-provenance.json. No parameter-dependent plot and no new renderer assets are necessary. Validation independently reads printed numerical objects, full subset choices and solution conclusions, then separately runs real native grading. Native radio ID acceptance is not semantic proof. Two correct references/solutions and missing-level labels are authored/inferred; none are counted as recovered original evidence. One raw prompt's trailing $$ is minimally repaired in normal output.
