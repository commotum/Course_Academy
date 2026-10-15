# Calculating Flux Across a Closed Surface

One local generator for math basis 1356; no database writes or plot assets.

```sh
.venv/bin/python generate/scratch/17592186133931.py --difficulty all --seed 42 --count 2
.venv/bin/python generate/scratch/17592186133931.py --difficulty moderate --profile observed:17592186134140 --format json
.venv/bin/python generate/scratch/17592186133931/validate.py
.venv/bin/python generate/scratch/17592186133931/catalog.py
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and individual `generate_easy`, `generate_moderate`, `generate_hard` wrappers. Parameters are `{"bounds": [x0,x1,y0,y1,z0,z1]}`; authored easy additionally requires integer `a` from 2 through 9. Profiles are `method` (normal default) and `observed:<source_db_id>` (evidence-only, moderate scope). Explicit invalid parameters raise; sampling rejects complete colliding banks and retries within the already selected family.

Easy is authored from the rectangular-solid tutorial: one constant nonzero partial and three distinct positive widths 2–5. Moderate serves every ten supported observed flux field/solution families, with fixed original fields and varied rectangular integration limits. The unrated `xz` original receives an explicitly authored moderate assignment only in normal output. Hard is authored from this KP's canonical example: two nonzero partials combine to `6x²y`, with both cubic and quadratic endpoint differences at positive translated bounds. Easy/hard are design claims, not observed labels. Finite sampler counts and easy permutation deduplication are in `catalog.json`.

Every raw prompt, all 51 option values across 11 banks, ten existing worked solutions and ten existing correct designations replay through the public API. The unrated source's missing difficulty, solution and correct designation remain absent. Its mathematical flux is 2; normal output has an authored correct designation. Historical numeric distractor intentions are underdetermined; replay profiles parameterize their scalar expression patterns and remain ineligible. Default banks instead derive complete sets of actual divergence, orientation, integration or endpoint mistakes.

Source 17592186235537 is a context-dependent integrand blank that supplies neither the original vector field nor its preceding part. The API preserves its original full whitespace/layout and fragment; it is evidence-only and excluded from normal sampling. Its full mathematical premise cannot be independently recovered from this frozen capture or the owning lesson snapshot. The blank fragment and displayed solution agree and pass canonical/equivalent/wrong native grading separately. This limitation is recorded in `validation.json`.

`validate.py` reads the actual printed field and all six bounds, independently checks held partials (including zero contributions), factorizations, order, primitives, each individual upper/lower endpoint and final arithmetic. It also reconstructs every normal displayed bank independently from the printed field, checks faithful full source strings/key presence, tests stable identity and scope, rejects mutations, and invokes the actual in-memory application grader. `review.md` includes all originals plus two clearly labeled variants per supported family and per authored level; `review.json` holds the generated records. No learner-facing diagnosis is added.

Verified: 237 independently parsed display records, 24 rejected mutation regressions, complete source fidelity 11/11 prompts and banks, 51/51 values, 10/10 existing worked solutions and designations. Native checks: 57 accepted, 207 rejected, zero unresolved. The preserved missing designation is not counted as a matched designation; the blank's absent prior context is explicitly unresolved and ineligible. Actual Python/SymPy versions and the native binary hash are in `validation.json`.

## Inventory integration

`reference/current-source-classification.md` supplements the frozen capture with the 13 live source records at basis 2723. Twelve self-contained moderate radios are mathematically validated; the context-dependent blank remains excluded. The radical and negative-sine source profiles are classified but not parameterized by this generator. These bounded family exceptions do not make the moderate level unsupported.

Run `.venv/bin/python generate/scratch/17592186133931/replenish.py` for this retained inventory request. It reuses the application's EDB environment, locks `.local/learning/requests/math/api.lock`, recovers exact saved requests first, checks the current basis and native pool, validates actual grader responses, adds only fresh distinct questions, registers the generator UUID/script, and reads back at the committed basis before unlocking. Exact transactions, requests, speculative previews, durable receipts and readback evidence are under `reference/replenishment/`. It preserves source questions, the canonical example and learner history. Retained commit recovery is idempotent; a new future inventory job requires its own request path.
