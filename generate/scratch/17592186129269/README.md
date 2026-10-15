# Inverse Jacobian generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186129269/validate.py
.venv/bin/python generate/scratch/17592186129269.py --difficulty all --seed 73 --count 2 --format json
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and individually documented `generate_easy`, `generate_moderate`, `generate_hard` entrypoints. Source templates use `parameters={"u":a,"v":b,"w":c}`: these positive integer coefficients scale the supplied inverse components, rather than resampling the question. Source cases are replayed with all coefficients 1 and `profile="observed"`. `source-repaired` preserves their banks while correcting component labels or cofactor structure and clarifying the cubic family's positive branch. Both historical profiles are evidence-only. Normal `method` banks are authored from incorrect operations on the actual derivative matrix. Default moderate generation chooses all six observed source-shaped method families before sampling, with a normal authored method bank. The authored moderate diagonal family requires an explicit template. Easy `easy_diagonal` uses `{"a":integer}`; moderate `moderate_diagonal` uses `{"a":integer,"b":integer}`.

The original source extraction covers steps 3–7. The KP-local inventory integration below completes steps 8–9. No shared-engine edits, new skills, integration questions, or critical-point questions. `review.md`/`review.json` distinguish originals, transported opaque-bank variants, repairs and normal method variants. `validation.json` separates exact raw fidelity, mathematical repairs, finite task counts and native grading. Its frozen hashes bind the tested generator and readback artifacts.

Raw q-39300 has mislabeled component functions. Raw q-161807 has an incorrect but zero-contributing cofactor-minor entry; its nonzero-domain fractional powers require real cube-root interpretation, while normal questions use the positive branch. Raw q-161808 has distractors with extra poles not excluded by the prompt; these remain explicit evidence, never the learning default. No unresolved native grading checks remain.


## Inventory integration

The validated `inverse-jacobian-v3` method output uses the shared canonical TeX formatter; observed and source-repaired evidence profiles retain their historical notation and are never admitted to learning. `replenish.py` implements stages 8–9 through the existing application EDB integration. It excludes the three documented defective source banks from validated reserve counts, preserves them in storage, rechecks current inventory under `api.lock`, and retains complete requests, native grading, previews, receipts and exact-basis readback in `reference/replenishment/`. Run `.venv/bin/python generate/scratch/17592186129269/replenish.py` from the repository root. Registration reuses any existing KP/script identity; otherwise it derives a stable UUID from the existing KP UUID.

The live source changes since basis 1356 are presentation-only standard matrix environments; the shared formatter establishes equality of all source prompt, solution and answer data before generation. The current captured read is retained in `reference/replenishment/initial-kp.edn`. No source question or history is rewritten.
