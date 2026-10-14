# Adding Square Matrices — draft generator

This draft preserves the registered `../17592186054648.py` and all numeric evidence. It implements same-method easy, moderate and hard 2×2 signed-integer addition with four observed prompt/solution backbones, five explicit source-evidence banks and two complete authored default banks. All existing radio or four-cell blank contracts remain supported. Moderate/hard labels are authored, not observed MA placements. No within-level progression, matrix subtraction assessment, multiplication, determinant or new field layout is introduced.

Verify from repository root:

```sh
.venv/bin/python generate/scratch/17592186054648-draft/validate.py
.venv/bin/python generate/scratch/17592186054648-draft/build-docs.py
.venv/bin/python generate/scratch/17592186054648-draft.py --difficulty all --seed 42 --count 2 --format json
```

Public interface: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`, plus `generate_easy`, `generate_moderate`, `generate_hard`. CLI supports all/easy/moderate/hard, template, field type, profile and JSON parameters. Observed evidence-only profiles require explicit parameters and cannot be selected by normal sampling; source-cases.json provides six MA-original raw replay calls; independent-cases.json separately provides the exact inventory replay. Raw profiles preserve all attribute-presence contracts; normal eligible completions are distinct and explicitly labeled. Invalid explicit parameters or equivalent complete banks raise ValueError/SampleRejected instead of silently changing parameters or options.

independent-inventory.json retains the independent generated practice record with its exact captured payload and role; inventory.json instead records learner availability. Source coverage and limitations are in report.md and validation.json; every bank operation in source-choice-mapping.json and template-extraction.md; source/variant previews in review.md and review.json; slots, finite domain bounds and task deduplication in finite-capacity.json. Source, topic and lesson wrappers all retain math2275 provenance. inventory.json separately preserves availability, which is not the source count. baseline-hashes.json verifies every registered-baseline file remains unchanged.

Native grading runs the existing check-engine binary in memory, with no database access. No registration, transaction data, engine edits or shared edits are authorized. Worker checks passed; independent root QA is required before treating the draft as approved.
