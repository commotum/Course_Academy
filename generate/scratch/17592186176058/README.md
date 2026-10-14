# Tangent oddness generator

Local script: `../17592186176058.py`. Database capture: math basis1356. No DB writes, registrations, or shared engine edits.

```sh
.venv/bin/python generate/scratch/17592186176058/validate.py
.venv/bin/python generate/scratch/17592186176058.py --difficulty all --seed 17 --count 2 --format json
.venv/bin/python generate/scratch/17592186176058.py --difficulty moderate --profile raw_unrated --format markdown
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` plus the three difficulty entrypoints. `source-cases.json` supplies exact replay calls. Source JSON fields use colon-prefixed schema keys and enum strings; outer KP keys are plain. All answer IDs are field-owned UUIDs. Explicit parameter bounds and whole-bank rejection match sampling guards.

Every source family is served by defaults. Moderate is an authored level assignment and completion of an unrated observed reflected-shift family. Two opaque historical banks and the missing-key raw record are evidence-only and labeled in metadata. Hard defaults use an authored five-operation bank, preserving the two source solution structures. `validation.json` separates full-bank/source-layout fidelity, missing attribute denominators, independent printed mathematics, native grading, finite variety and unresolved source interpretation. `review.md` juxtaposes all originals and labeled changed-parameter examples.
