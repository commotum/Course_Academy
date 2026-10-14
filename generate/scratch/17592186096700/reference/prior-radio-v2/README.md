# KP17592186096700 generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186096700/validate.py
.venv/bin/python generate/scratch/17592186096700.py --difficulty all --seed 30 --count 2 --format json
.venv/bin/python generate/scratch/17592186096700.py --difficulty hard --template reciprocal_multiple --profile authored-selection-flips --seed 44 --format markdown
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Only observed `radio` fields are supported. CLI accepts optional `--parameters` as exact JSON. Invalid explicit inputs raise; no silent resampling. Easy supports `opposite_multiple`; moderate/hard support both observed masks. Normal defaults select eligible observed completed catalogs; the selection-flip catalog is an explicit authored extension.

`source-cases.json` replays both practice originals through public `raw-a`/`raw-b` profiles. These preserve missing difficulty, worked solution and correct ref and are **evidence-only**. Keys inferred from actual calibrated arrows are in author metadata; they do not count as original designation fidelity. `observed-a-completed`/`observed-b-completed` preserve the observed bank but add supported inferred keys and authored solutions. All three level assignments are authored because no source practice difficulty exists.

Both complete banks and all10 choices match; native425 checks pass separately. Independent PNG/printed-statement/prose checks cover87 records. Finite meaningful task counts: easy192, moderate2240, hard2240. No zero arrows; actual lesson convention (antiparallel and zero vector parallel to any vector) is documented in classification. No off-topic arithmetic branch is added.

`review.md`/`review.json` show both originals, completed originals, two variants per level and three authored-bank examples. `visual-review.json` records full-resolution visual review of every source raster and all nine generated variants. Original images are read-only EDB assets; raw prompt references are exact, while review Markdown resolves them to absolute paths.

`render_plot.py` uses the fixed cached Python3.10/Matplotlib runtime read-only; the main API uses `.venv/bin/python` (Python3.13/SymPy). `dependency-lock.json` freezes paths. Plot sidecars include actual versions, dependency RECORD hashes, runtime/renderer hashes, PNG hashes, measured label bboxes and raster geometry. No package install or shared environment change occurs. Unique temporary inputs and atomic PNG/sidecar writes survive simultaneous identical/different instances; cache assets remain available during root QA. `freeze.json` records the tested source/script/renderer/validator hashes.

Work stops at step7 for independent root QA. No database writes, registration, engine/shared edits, commits or generated SVG assets.

The label regression suite covers default seeds0–17 at every level (54 cases), explicit replay of those same parameters, and20 family/coordinate-boundary cases. Hard seed0 is included. The correction changes only label collision geometry/search and version2 provenance; no sampler/family/domain is excluded to avoid the failure. Old plot caches remain intact.
