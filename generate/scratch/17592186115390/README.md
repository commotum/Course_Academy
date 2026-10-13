# Vector sum/constant derivative generator

Scratch-only KP 17592186115390, database math basis 1356. No transactions or engine changes.

```sh
.venv/bin/python generate/scratch/17592186115390/validate.py
.venv/bin/python generate/scratch/17592186115390.py --difficulty all --seed 31 --count 2 --format markdown
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy/moderate/hard`. Templates use source IDs plus `canonical-mixed`. Field type is radio. Profiles use a source ID for explicit complete source-bank replay, or `authored-operations` (normal default). Source replay parameters are `{"scales":[1,1,1]}`; signed component scales are bounded to ±1..3 (authored triple-sum default: x,z ±1..6, y=1). Fixed parameters/profile/content keep identity when seed only shuffles options. Equivalent mathematical parameters retain their mathematical fingerprint separately from presentation identity.

All source records, complete source bank maps, exact/repair fidelity denominators and authored hard scope are documented. `review.md` shows all originals, all replays, two variants per source bank and authored examples at each level. `review.json` contains generated variants. `validation.json` reports source fidelity separately from mathematics and native grading. q-33143 has an inferred missing designation and authored moderate level/solution; q-128452 needs a real-domain log repair. Residual distractor interpretation limits remain explicit. Stop at steps 3–7.
