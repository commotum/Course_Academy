# Local scalar-matrix generator

`../17592186059740.py` builds exact, deterministic easy/moderate/hard entrywise scalar multiplication. It stops after guide step7. No EDB access, database writes, registration, shared edits or plots.

```sh
.venv/bin/python generate/scratch/17592186059740/validate.py
.venv/bin/python generate/scratch/17592186059740.py --difficulty all --seed 42 --count 2
.venv/bin/python generate/scratch/17592186059740.py --difficulty easy --profile raw_986 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy/moderate/hard`. Exact parameters are `{ "k": 3, "matrix": [[4,-5],[-2,"1/3"]], "name": "A" }`. Explicit invalid parameters raise, while random whole-bank collisions reject the entire instance. Never use float parameters. Public raw profiles replay every original using recipes rather than captured payload returns; they are evidence-only and preserve missing attributes. Normal outputs repair missing information and the q320075 introductory coefficient, and align lower-row blank padding. No feedback is invented.

`classification.md` documents scope and authored levels; `template-extraction.md` maps every bank and solution component. `source-cases.json` is the complete original replay list. `review.md/json` show raw originals, changed raw profiles, normal repairs and generated examples. `validate.py` independently reads printed matrices/products/prose, checks full-source fidelity, level bounds, whole-bank ambiguity, formatting, deterministic/content/math identity, mutation failures and real memory-only native grading. `validation.json` records the completed source, mathematical and grading checks; `validation-freeze.json` records final review. `native-input.json` and `native-grading.json` are engine evidence.

q979/q986 source keys, solutions and ratings are absent. Normal keys are independently derived. q986's compound last-row distractor has underidentified historical intent; it is available solely as a public raw bank, never a normal default. Moderate/hard labels are authored design claims. Calculator requirement remains unknown. Source wrappers stay unchanged at basis2275.

## Inventory registration and commit

`validation-freeze.json` records completed independent review and input hashes.
`replenish.py` extends the generation-only script through database preparation
and commit using the existing EDB integration and configured
`:application/ca-engine` contributor. It takes `api.lock`, captures current
inventory and source facts, excludes historical presentations/reservations,
validates distinct mathematical tasks and learner grading, and registers the
stable generator UUID and repository-relative script path. Requests, preview,
receipt and exact-basis readback stay under `reference/replenishment/basis-*`.
The seven original practice records and canonical example remain unchanged.
The malformed coefficient prose in q-320075 excludes it from verified usable
inventory; q-979/q-986 remain incomplete originals, preserved as evidence.
Zero-scalar 2×3 multiplication has one mathematical task, already present;
changing its operands cannot replenish that finite source profile. Other
supported profiles supply the easy reserve. Moderate and hard use the authored
arithmetic bounds documented in `classification.md`.
