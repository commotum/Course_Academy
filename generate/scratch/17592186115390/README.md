# Vector sum/constant derivative generator

KP 17592186115390, database `math`. Source extraction is retained at basis 1356; current inventory was checked at basis 2534. The generator and seven distinct questions were committed and verified at basis 2535 using the application's contributor and `api.lock`.

```sh
.venv/bin/python generate/scratch/17592186115390/validate.py
.venv/bin/python generate/scratch/17592186115390.py --difficulty all --seed 31 --count 2 --format markdown
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy/moderate/hard`. Templates use source IDs plus `canonical-mixed`. Field type is radio. Profiles use a source ID for explicit complete source-bank replay, or `authored-operations` (normal default). Source replay parameters are `{"scales":[1,1,1]}`; signed component scales are bounded to ±1..3 (authored triple-sum default: x,z ±1..6, y=1). Fixed parameters/profile/content keep identity when seed only shuffles options. Equivalent mathematical parameters retain their mathematical fingerprint separately from presentation identity.

All source records, complete source bank maps, exact/repair fidelity denominators and authored hard scope are documented. `review.md` shows all originals, all replays, two variants per source bank and authored examples at each level. `review.json` contains generated variants. `validation.json` reports source fidelity separately from mathematics and native grading. q-33143 has an inferred missing designation and authored moderate level/solution; q-128452 needs a real-domain log repair. Residual distractor interpretation limits remain explicit.

The live source's `bmatrix` formatting repair for q-128458 is mathematically equivalent to the captured bracketed column layout. The exact recursive source comparison passes after this bounded notation normalization; both snapshots are retained in `reference/replenishment/`. Original questions, the canonical example, and learner history were preserved. The unrated original q-33143 and the real-domain-invalid original q-128452 remain excluded from validated inventory.

The registered identity is `34f2c402-acc1-5020-9544-72c94be0f985`, with script `generate/scratch/17592186115390.py`. The commit added two moderate and five authored hard questions. Verified inventory is six easy, five moderate, and five hard questions. Exact transaction, application-attributed receipt, current native grading evidence, and readback are in `reference/replenishment/basis-2534/`. `replenish.py` retains the exact request for recovery and uses mathematical fingerprints that ignore identity, seed, answer-bank profile, and choice order.
