# Product rules generator

Scope: KP 17592186115393, Using the Product Rules for Differentiation; basis 1356. All 13 observed templates are implemented: four easy scalar products, five moderate dot products, four hard cross products. Every complete source bank is replayed. Learner generation defaults to whole authored banks derived from missed terms, wrong signs/order, and derivative-factor errors; fitted observed profiles remain explicit replay evidence. Authored parameter extensions stay within those structures; no missing-level synthesis was necessary.

From the repository root:

```sh
.venv/bin/python generate/scratch/17592186115393/validate.py
.venv/bin/python generate/scratch/17592186115393.py --difficulty all --count 2 --seed 101 --format markdown
```

`validation.json` separates original-bank fidelity, independent displayed mathematics, source repairs, and actual engine grading. q-32353 uses the supported single-widget layout; its legacy field lacks a source correct ref and is separately replayed as evidence. q-33446 removes an intermediate typo. See `template-extraction.md` for exact evidence and every original choice recipe. `review.md` includes all originals and two variants of both the observed replay and authored default banks per template, plus two legacy-bank evidence variants.

No database writes, generator registrations, plots, or engine changes are performed.
