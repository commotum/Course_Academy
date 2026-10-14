# Tangent oddness generator

Local generator: `../17592186176058.py`. Source capture: math basis 1356. The generator itself performs no database writes.

Replenishment reused this package and committed ten distinct questions at math basis **2240**, from preparation basis **2239**: two easy, five moderate, and three hard. The verified fresh inventory is five per level. Generator UUID `ee2be17c-7ff2-5ace-8a40-875aced950b8` is registered at `generate/scratch/17592186176058.py`. Moderate is an authored workload label; easy and hard have observed labels. All six source questions and the canonical example remain unchanged, and the receipt contains only additive scoped content datoms attributed to `:application/ca-engine`.

`replenish.py` retains the exact request, native-spec preview, receipt, grading checks, and exact-basis verification in `reference/replenishment/basis-2239/`. It holds the application's `api.lock` through the current inventory check, preparation, submission, and readback. No application code or other KPs were changed.

```sh
.venv/bin/python generate/scratch/17592186176058/validate.py
.venv/bin/python generate/scratch/17592186176058.py --difficulty all --seed 17 --count 2 --format json
.venv/bin/python generate/scratch/17592186176058.py --difficulty moderate --profile raw_unrated --format markdown
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` plus the three difficulty entrypoints. `source-cases.json` supplies exact replay calls. Source JSON fields use colon-prefixed schema keys and enum strings; outer KP keys are plain. All answer IDs are field-owned UUIDs. Explicit parameter bounds and whole-bank rejection match sampling guards.

Every source family is served by defaults. Moderate is an authored level assignment and completion of an unrated observed reflected-shift family. Two opaque historical banks and the missing-key raw record are evidence-only and labeled in metadata. Hard defaults use an authored five-operation bank, preserving the two source solution structures. `validation.json` separates full-bank/source-layout fidelity, missing attribute denominators, independent printed mathematics, native grading, finite variety and unresolved source interpretation. `review.md` juxtaposes all originals and labeled changed-parameter examples.

Canonical task counts: **easy 92, moderate 92, hard 245**. Period-shift aliases yield 2,208 moderate and 5,880 hard presentation variants; they do not increase mathematical-task counts. `validation.json` records the separate totals and tests identical mathematical fingerprints but distinct content IDs for shifts 3 and 7.
