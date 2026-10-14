# Constant×ln generator draft

Current authoritative evidence is frozen `math` basis 1356 in source.json. Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186096613/validate.py
.venv/bin/python generate/scratch/17592186096613.py --difficulty all --seed 7 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186096613.py --difficulty easy --profile raw-q-70881 --format json
```

The API is `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and dedicated easy/moderate/hard entrypoints. Exact parameters are `{n,d,k}` with c=(n/d)e^k. Raw profiles are source-specific `raw-q-ID`; they preserve absent source attributes and original notation. Incomplete raw records are evidence only. Normal profiles are complete integer/fraction/euler/canonical/equivalent-entry banks. Moderate and hard are explicitly authored constant recognition variants, not observed difficulty labels. All questions stay y=c ln x, x>0, with no chain rule, nonconstant product, sum, general-base log or point evaluation.

Validation independently reads displayed expressions, every operative worked stage, all bank pairs, formatting and identities, then exercises the actual shared `learning::grade_field` harness. No DB writes, engine changes, registration, plots or commits. Older reference material under reference/, replenish.py, and check-current-engine are historical and unused in this draft. The current grader is generate/runs/current/check-engine; current-engine-build.json records its hash. No replenishment or registration workflow was run. Current evidence is the source, classification, extraction, source cases, generated reviews, validation, native reports, CLI preview and capabilities files described here.
