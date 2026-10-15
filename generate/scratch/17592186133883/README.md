# KP 17592186133883

`../17592186133883.py` generates hard radio questions from the q-41475
triangle-linear-curl family. It supports 12 distinct coefficient values, including
one source replay. Easy and moderate are outside this bounded version; they must
not be reported filled. All original questions and learner records are preserved.

Run from the repository root:

```sh
python3 generate/scratch/17592186133883.py --difficulty hard --count 5 --seed 123 --format json
.venv/bin/python generate/scratch/17592186133883/validate.py
.venv/bin/python generate/scratch/17592186133883/replenish.py
```

The worker CLI uses the repository venv automatically when system Python lacks
SymPy. The generator only produces local JSON/Markdown. Its UUIDs encode the
mathematical coefficient and complete field-owned bank, never the seed.
Classification, exact source components, extraction, full-bank replay, independent
math checks, native grading and side-by-side examples are retained here.

Replenishment reuses the existing configured Database, EDN, native pool and writer
preview integrations. It captures inventory before work, acquires the application's
api.lock, rechecks inventory/basis/lineage under that lock and holds it through
guarded submission and exact-basis readback. It adds questions only for an actual
supported-band shortage and registers the generator through the installed schema,
reusing an existing identity when present. An unknown submission is recovered
using the identical durable intent. Exact requests, receipts, verification and
post-commit inventory are retained in reference/generated/17592186133883.

At the initial current basis 2602, eleven mathematically validated source questions
were fresh and gradable. The hard reserve already exceeded five. The outstanding
classify job therefore requires a validated generator registration, with no extra
practice questions unless the final locked inventory recheck finds a shortage.
