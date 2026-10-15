# Supplied polar repeated-integral generator

Generator: `../17592186129198.py`. Source evidence: math basis 1356. The generator itself performs no database writes or image generation. `replenish.py` validates and publishes scoped additive content through the existing application integration.

```bash
.venv/bin/python generate/scratch/17592186129198.py --difficulty all --seed 42 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186129198.py --difficulty moderate --template q-83966 --profile q-83966_observed --seed 4 --format json
.venv/bin/python generate/scratch/17592186129198/validate.py
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` plus separate easy/moderate/hard entrypoints. `TEMPLATES` and `BANK_PROFILES` enumerate the supported complete profiles. Explicit observed replay takes `parameters={"scale": 1}`. Invalid explicit inputs fail without resampling. Defaults use authored operation banks and family-specific bounded parameters; observed banks are explicit homogeneous evidence profiles.

Scope: evaluate the supplied repeated integral only. Hard is authored from canonical e-7346, with the same half-angle method and nonzero familiar-angle endpoint term. q-38127's missing key, difficulty and solution are independently authored. All source bounds, banks and provided solution stages are retained. Scalar source distractor intent remains unresolved and is not promoted to default generation.

`validate.py` independently parses the actual displayed TeX and checks all solution equality stages, identity substitutions, primitive derivatives, complete answer banks, source values/prose/layout, domains, parameter guards, UUID shape/stability and deterministic shuffling. It then invokes the captured native engine for correct and incorrect selection in every reviewed bank. `review.md` labels exact source originals, two authored variants of every template and four scaled variants of every observed bank. `validation.json` reports honest fidelity and native grading counts. `freeze.json` hashes the verified artifacts.


Replenishment uses `replenish.py` with the application contributor `:application/ca-engine`, a stable UUID derived from the existing KP identity, and the registered repository-relative script path. It checks all original source evidence against a current captured basis, excludes shown/reserved/unrated/incomplete questions, and deduplicates the mathematical supplied integral independently of choice banks and identities. The current application library supplies grading checks for every choice of every available and generated question. Native writer validation specs are required during preview and durable submission.

Requests, exact EDN, previews, receipts, source comparison and readback evidence are retained in `reference/replenishment/`. The application `api.lock` is held from the inventory recheck through commit and exact-basis readback. Existing source questions and learner history are preserved. `capabilities.json` records the authored hard-level rationale and bounded sampling policy; finite bounds are not presented as unlimited capacity.
