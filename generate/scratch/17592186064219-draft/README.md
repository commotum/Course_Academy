# Inverse tangent substitution draft

Run from repository root:

```
.venv/bin/python generate/scratch/17592186064219-draft.py --difficulty all --count 3 --seed 2275 --format json
.venv/bin/python generate/scratch/17592186064219-draft/validate.py
```

`all` returns count questions per level. Seed/count accept builtin integers only, count positive. source-cases.json contains only 16 MA originals; review-cases.json holds changed and authored examples; independent-inventory.json uses the standard basis/lineage/questions wrapper. Source evidence is raw source.json; normalized output has field-owned UUIDs and bare TeX values. No source errors or missing practice records were excluded. Canonical e-471 has a differential omitted in its first intermediate equality; the authored H presentation restores dx while retaining the supported calculation. This is a labeled presentation repair, not a new practice source.

Registered numeric script and entire numeric tree are immutable and never imported. registered-baseline.json records their complete original path set and SHA values including caches; final-preservation.json compares them after validation. check-engine is a private frozen copy of the actual current native runner; no engine/registration/DB writes occur. H is an authored canonical extension, not observed H practice. Native blank probes preserve any valid-equivalent grading gaps separately from wrong-math probes.

Normal generator output is radio only. Independent authored blank fixtures in diagnostic-blank-cases.json exist exclusively for diagnostic parser probes; independent-inventory.json is empty because the captured snapshot has no nonMA records; all 15 unresolved outcomes are outside the supported response shape and do not qualify the verified radio grading result.
