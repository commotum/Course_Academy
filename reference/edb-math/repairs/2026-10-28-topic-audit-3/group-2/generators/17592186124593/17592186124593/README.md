# Supplied-gradient derivative at a point

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186124593/validate.py
.venv/bin/python generate/scratch/17592186124593.py --difficulty all --seed 4 --count 2 --format markdown
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and separate easy/moderate/hard entrypoints. Radio5 only. Explicit observed replay uses each source's `observed_q-*` profile and `{"c":1,"time_scale":1}` as recorded in `source-cases.json`. Source-layout profiles also support bounded coherent scaling/dilation. Default parameter/point variations use complete authored operation banks. Hard's two templates are authored same-KP extensions with curriculum rationale in `template-extraction.md`.

Snapshot: math basis 1356. All eight source banks, forty options and eight correct designations replay. Public raw full-solution fidelity is 8/8; normal source-layout solutions are 7/8 raw-exact plus the supported q-94878 i→j dot-basis repair. The public `raw_observed_q-94878` profile preserves the original erroneous solution. All opaque observed banks carry `evidence_only=true` and `eligible_for_learning=false`; authored defaults are eligible. Original decoded bytes and source remain intact. Wrong scalar recipes are underdetermined; do not claim their intent recovered. No plots, database writes or shared changes.

`validate.py` reads printed TeX independently, checks every mathematical stage and full bank, then invokes the real native radio grader. `validation.json` records honest counts, hashes, limits and native results; `review.md`/`review.json` show originals and labeled observed/default variants.
