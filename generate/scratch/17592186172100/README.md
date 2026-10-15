# Flux-form Green theorem generator

Validated source package for KP 17592186172100. Registration points to
`generate/scratch/17592186172100.py`; stable UUID is in generator-id.json.

```
python3 generate/scratch/17592186172100.py --difficulty easy --count 5 --seed 1930 --format json
.venv/bin/python generate/scratch/17592186172100/validate.py
.venv/bin/python generate/scratch/17592186172100/replenish.py
```

The public script re-execs the repository Python environment when SymPy is absent.
SymPy 1.14.0 and existing math_format helpers are required. Only easy/moderate
are supported; unsupported hard raises an explicit error. Per-template replay:
`--template q-127070 --scale 1 --count 1`. Sampling uses seeded selection without
replacement within one invocation. Across calls, consumers must compare semantic
fingerprints and existing question identities; the seed is provenance only.
Catalog capacity and hard exception remain explicit in capabilities.json.

Validation covers all original banks and the complete 120-task bounded domain,
reads displayed component fields independently, differentiates them exactly,
checks displayed solution derivatives and final objects, checks all option keys,
compares unevaluated repeated-integral structures, tests actual native grading,
checks unchanged content-addressed diagram bytes, and demonstrates that changing
only the seed preserves identities. The source bank already provides five unseen,
unreserved validated questions per supported band at basis 2651. No extra question
should be committed while those counts remain sufficient.

Durable registration/replenishment is scoped to this KP. It uses the application's
Database integration, contributor and native specs; serializes with api.lock;
checks current lineage/basis; saves exact EDN/request before submission; recovers
receipts; reads at db_after; and audits all datoms and unchanged source questions.
Evidence and receipts live under reference/. Source questions and learner data
are never retracted or changed.
