# 2D vector-field identification generator

Local draft; no database writes. Eight source easy families plus authored missing-level moderate/hard catalogs. Plot requirement none.

```sh
.venv/bin/python generate/scratch/17592186172085/validate.py
.venv/bin/python generate/scratch/17592186172085.py --difficulty all --count 2 --seed 7 --format markdown
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`, plus each level entrypoint. Only radio fields. Source template/profile IDs are listed in source-cases.json. Normal easy profile names append `-normal`; source IDs select exact public raw evidence. Moderate template `mixed_dimensions`, hard `restricted_mixed_dimensions`, profile `authored`. Parameters: integer h in -4..4, permutation order of [0,1,2]; q-122641 requires h in 1..4. Authored parameters may include kind as listed in extraction. All explicit inputs use the same bounds as samplers.

Validation checks every complete source bank/value/designation, exact source prompt/solution, attribute presence, actual displayed signatures/components/domain conclusions, all permitted finite boundary combinations, five content mutations, seed-independent owned identity and native grading of every displayed option. The source name errors and authorship limitation are documented in classification.md. validation.json has counts and actual dependency/binary metadata. review.md and review.json show originals/generated variants. Intermediate stages here are classification/examination/domain/conclusion prose, not arithmetic chains.
