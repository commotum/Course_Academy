# Polar-coordinate circular-cap generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186157298.py --difficulty moderate --count 5 --seed 12 --format json
.venv/bin/python generate/scratch/17592186157298/validate.py
.venv/bin/python generate/scratch/17592186157298/replenish.py
```

The registered CLI can re-execute the repository's existing `.venv/bin/python` when the calling interpreter lacks SymPy. Dependencies: Python, SymPy 1.14, Matplotlib 3.11, NumPy; native learner grading is linked against the existing release engine. Source evidence is frozen at basis 2758, with current inventory rechecked before generation and under `api.lock` before every write.

Supported difficulty: moderate only, with 11 source-faithful templates and complete five-option banks. Unsupported: easy/hard (no source evidence; deficits remain explicit). Normal bounded output has 121 candidates, with a further 11 source-equivalent scale-1 replays excluded from replenishment. Seeds select mathematical tasks; they do not enter identities.

`classification.md`, `template-extraction.md`, `plot-extraction.md`, `components.json`, `review.md`, `validation.json`, and the real `engine-report.json` separate source fidelity, mathematical correctness, actual grading, and visual review. `reference/replenishment/` retains exact requests, previews, receipts and exact-basis verification. The generator UUID is stable and is reused from an existing registration when present. The registration is additive; it changes neither source questions nor learner history.
