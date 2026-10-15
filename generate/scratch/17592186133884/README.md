# Green's theorem repeated-integral generator

Run from repository root with system Python (it selects `.venv` for SymPy):

```
python3 generate/scratch/17592186133884.py --difficulty hard --count 4 --seed 117 --format json
.venv/bin/python generate/scratch/17592186133884/validate.py
.venv/bin/python generate/scratch/17592186133884/replenish.py
```

Supported: moderate, triangle polynomial coefficient a=1..12; hard, parabola/vector
coefficient a=2..12. These are bounded local capabilities, not the full space of
possible questions. Easy remains unsupported with its shortage explicit. Hard a=1
is available only for fidelity replay and is rejected by instance validation for
normal output. No seed or choice shuffle creates a new mathematical identity.

Classification, extraction, complete source components, source-bank replay,
independent display parsing and native engine grading evidence are adjacent.
Source diagrams are unchanged and byte-verified. review.md compares source
parameters with coefficient boundaries; source-components.json retains originals.

The replenisher uses the existing Database and native inventory/pool/grader
integration, acquires the application api.lock, rechecks current captured inventory,
resolves the existing generator identity, and prepares only additive content for
this KP. It retains exact EDN, request key/basis/source, speculative preview, durable
receipt, scoped datom audit, exact-basis content/grading readback and final counts
under reference/generated/17592186133884. It uses application/ca-engine attribution
and native ensure specs; source questions and learner facts are not modified.
