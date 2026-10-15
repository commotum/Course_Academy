# Equal-flow dilution generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186229181/validate.py
.venv/bin/python generate/scratch/17592186229181.py --difficulty all --seed 42 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186229181.py --difficulty moderate --profile raw_17592186377242 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and documented easy/moderate/hard entrypoints. Normal templates are `expression`, `amount`, `amount_unit_conversion`; normal complete bank is `method_bank`. Seven `source_<db-id>` templates and `raw_<db-id>` profiles preserve all source evidence and are ineligible for learning. Normal parameters are V, r, c (normalized kg/L), q0, context, plus time for moderate/hard; raw parameters are positive integer mass_scale in 1–4 and flow_scale in 1–3. Explicit invalid/ambiguous instances fail without resampling.

`source.json` and `source-cases.json` preserve provenance and replay routes. `masks.json` is the extraction product. `extract.py` rebuilds only those masks/cases from the private frozen source. `classification.md` and `template-extraction.md` document scope, bank limitations and omissions. `review.md`/`review.json` label originals and variants. `validate.py` checks original bytes/presence/banks/designations, printed numerical stages, exact model/distractor mathematics, identities, parameter guards, public JSON serialization, CLI labeling and the real native grader. Native reports are `engine-input.json`/`engine.json`; `validation.json` keeps denominators separate.

The missing hard level is authored feed-unit conversion followed by the same constant-volume IVP and rounded amount. Numerical source banks and two easy banks have opaque wrong-answer coefficients; defaults use a separately authored complete operation bank. This script has no plots, database client, writes, registrations, or engine changes. Frozen at step 7 for parent QA.

## Published replenishment, 2026-10-15

The generator script remains unchanged from its validated step-7 version.
`replenish.py` completes stages 8–9 using the existing native database integration:
application `api.lock`, fresh inventory and basis reads, configured application
source, typed ensures, native preview, durable exact request, guarded commit,
readback at the receipt basis, scoped additive datom checks, and final inventory.
It recovers saved submission intent before preparing another transaction.

Publication basis 2704 → 2705 registered generator
`90943b8b-a658-5a9b-a2fd-363b88498657` (the authoritative UUID is retained in
`reference/replenishment/basis-2704/commit-intent.json`) and added two moderate
and five hard questions. Easy inventory already met its reserve. All three reserves
have at least five available questions after publication; no KP jobs remain.
All ten existing source questions, canonical example, and learner history were
preserved. One incomplete unrated original remains excluded.

`validate_inventory.py` checks each committed instance from its rendered prompt,
all options, exact differential model, printed worked stages, final rounding,
formatting and deterministic regeneration. Current captured source checks and
complete excluded banks are in `reference/current-source-validation.json`;
classification and extraction document the evidence refresh. The seven original
source bank replays and the separately authored normal method bank remain intact.
`reference/publication-validation.json` freezes implementation/evidence hashes.
The publication folder retains generated JSON/Markdown, validation, inventory,
preview, exact durable intent, transaction, committed receipt and verification.
