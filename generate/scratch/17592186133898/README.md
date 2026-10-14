# Calculating the Scalar Curl of a Vector Field

Validated bounded easy/moderate radio generator for KP 17592186133898. Registration uses the existing generator reference and stable UUID; `registration.json` records identity reuse. Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186133898.py --difficulty easy --count 5 --seed 13 --format json
.venv/bin/python generate/scratch/17592186133898/validate.py
.venv/bin/python generate/scratch/17592186133898/replenish.py
```

The JSON CLI enumerates unique variants without replacement. Hard requests fail explicitly; counts beyond 48 easy or 56 moderate fail with the finite limit. `capabilities.json` records remaining unsupported scope. `source-components.json`, `source-fidelity.json`, `validation.json` and `review.md` document extraction, fidelity, mathematics and actual engine grading. No plots are required.

Replenishment uses the existing native inventory, question pool, EDB CLI and deployed validation preview. The application `api.lock` serializes basis recheck, final selection, preview, exact durable request, basis-guarded submission and receipt readback. Prior intents are recovered before new work. Only additive generated content and this KP's generator registration are allowed; source questions, canonical example and learner history are verified unchanged. Every exact request, preview, committed receipt and verification remains in `reference/replenishment/basis-*`.
