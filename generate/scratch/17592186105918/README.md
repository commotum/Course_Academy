# Perpendicular scalar projection generator

Local review only: database math basis 1356; steps 3–7; no database writes.

```sh
.venv/bin/python generate/scratch/17592186105918/validate.py
.venv/bin/python generate/scratch/17592186105918.py --difficulty all --seed 42 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186105918.py --difficulty moderate --template q-236734 --profile observed:q-236734 --seed 42 --count 2 --format json
```

The normal API is `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and the three difficulty entrypoints. Source cases replay explicit parameters/profile through that API. Raw observed radio profiles are opaque evidence-only banks, while normal defaults use method-derived complete banks. Easy and hard are authored within the same zero-projection KP. Easy has one finite meaningful task; its two information forms and repeated review examples do not count as extra tasks. Moderate varies the observed unknown component; hard collects two nonzero linear contributions before the same solve.

Read classification and extraction for source anomalies, exact/repaired denominators, arithmetic bounds, and workload claims. `review.md` puts originals, public original replays, changed observed-profile evidence variants, and normal variants together. `review.json` holds schema-shaped review records. `validation.json` separates complete source fidelity, prompt/stage math, native grading, family coverage, and true variety. It contains actual Python/SymPy versions and frozen script/source/engine hashes. `extract.py` is a deterministic source-to-mask extraction utility, not a runtime source sampler. No plot renderer is needed.
