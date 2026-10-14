# Tangent-property generator

Current generator: `../17592186176049.py`, version `tangent-properties-2-checkbox`. KP 17592186176049, Describing Properties of the Tangent Function. Uses three checkbox fields keyed I, II, III with field-owned `false`/`true` answers, matching the migrated sources captured at math basis 2242. Historical radio source evidence remains local; original database questions and learner history are preserved.

```sh
.venv/bin/python generate/scratch/17592186176049/validate.py
.venv/bin/python generate/scratch/17592186176049.py --difficulty all --count 5 --seed 20261014 --format json
.venv/bin/python generate/scratch/17592186176049/replenish.py --prepare-only
.venv/bin/python generate/scratch/17592186176049/replenish.py
```

`validate.py` replays current source prompts, solutions, complete Boolean banks and keys, enumerates all finite parameter domains, independently parses displayed mathematics and explanations, checks deterministic content identities and rejects incorrect key/solution mutations. Native grading uses the installed application engine. `legacy_validation.py` retains the historical mathematical parser and old radio fidelity checks. Fixed Matplotlib tangent graph assets are published by the existing content-addressed image library and verified by hash.

Easy (zeros, asymptotes, range) and moderate (domain, signs, least period) are authored workload assignments supported by the lesson and prerequisites. Hard retains observed source families plus the documented two-identity extension. q-27660 has migrated keys and solution but remains unrated and excluded from available inventory. All levels have finite catalogs; no seed, identity, bank or option permutation counts as a distinct task. Replenishment independently fingerprints the rendered claim sets, excludes all source/canonical/already generated content, and leaves any exhausted band explicit.

`replenish.py` rechecks inventory under the application's `api.lock`, prepares additive scoped transactions attributed to `:application/ca-engine`, previews installed entity validation, saves exact durable requests, submits with the current basis guard, and verifies the receipt's exact database value. It reuses existing generator identity and preserves receipts for recovery. Evidence lives in `reference/replenishment/`; the requested job result contains the verified commit basis and remaining shortages.
