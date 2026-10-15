# Local partial-derivative generator draft

Script: `../17592186124644-draft.py`. Source wrapper is frozen math basis2275. No EDB reads/writes, registration, engine changes or commits occur. Numeric script/tree/cache and sibling pyc absence is captured before imports and rechecked. The generator sets `sys.dont_write_bytecode=True` before third-party/shared imports.

```sh
.venv/bin/python -B generate/scratch/17592186124644-draft.py --difficulty all --seed 7 --count 2 --format json
.venv/bin/python -B generate/scratch/17592186124644-draft/validate.py
.venv/bin/python -B generate/scratch/17592186124644-draft/build-docs.py
.venv/bin/python -B generate/scratch/17592186124644-draft/render.py
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and the three difficulty wrappers. `parameters` uses a,b,n,m,U,V,target. `observed-q-…` replays complete original banks at documented anchors and preserves missing attributes; these are explicitly ineligible evidence. `method-sum-bank` is the normal default complete bank. See `domains.json` for every explicit-input guard. API JSON is review data, never transaction data.

Read `validation.json` for separate source-fidelity/math/native denominators and `scalar-native-report.json` for the Euler-e semantic probes and explicitly reproduced raw-source parser limitation, `render-report.json` and `renders/` for actual player controls and full solutions, and `freeze-manifest.json` for final owned hashes. Root approval remains pending.
