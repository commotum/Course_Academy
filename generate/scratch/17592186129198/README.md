# Supplied polar repeated-integral generator

Scratch generator: `../17592186129198.py`. Read-only source: math basis 1356. No database writes, registration, image generation or extra dependencies.

```bash
.venv/bin/python generate/scratch/17592186129198.py --difficulty all --seed 42 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186129198.py --difficulty moderate --template q-83966 --profile q-83966_observed --seed 4 --format json
.venv/bin/python generate/scratch/17592186129198/validate.py
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` plus separate easy/moderate/hard entrypoints. `TEMPLATES` and `BANK_PROFILES` enumerate the supported complete profiles. Explicit observed replay takes `parameters={"scale": 1}`. Invalid explicit inputs fail without resampling. Defaults use authored operation banks and family-specific bounded parameters; observed banks are explicit homogeneous evidence profiles.

Scope: evaluate the supplied repeated integral only. Hard is authored from canonical e-7346, with the same half-angle method and nonzero familiar-angle endpoint term. q-38127's missing key, difficulty and solution are independently authored. All source bounds, banks and provided solution stages are retained. Scalar source distractor intent remains unresolved and is not promoted to default generation.

`validate.py` independently parses the actual displayed TeX and checks all solution equality stages, identity substitutions, primitive derivatives, complete answer banks, source values/prose/layout, domains, parameter guards, UUID shape/stability and deterministic shuffling. It then invokes the captured native engine for correct and incorrect selection in every reviewed bank. `review.md` labels exact source originals, two authored variants of every template and four scaled variants of every observed bank. `validation.json` reports honest fidelity and native grading counts. `freeze.json` hashes the verified artifacts.
