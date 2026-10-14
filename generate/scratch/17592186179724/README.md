# Segment integral construction draft

Script: `../17592186179724.py`. Immutable source wrappers: `source.json`, `topic.json`, `lesson.json`, math basis2275. No registration, database writes, engine edits or commits. Parent independent QA remains required.

Run from the repository:

```sh
.venv/bin/python generate/scratch/17592186179724.py --difficulty all --seed 17 --count 2 --format json
.venv/bin/python generate/scratch/17592186179724/validate.py
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and three difficulty wrappers. Templates: quadratic/log/cos/linear/exp. Parameters are the complete ax,ay,bx,by coordinate dictionary, using integer or rational strings. Explicit invalid parameters fail; random invalid complete instances are rejected and resampled. Profile names are `<family>_observed` (empirical evidence, ineligible for learner defaults) or `<family>_method` (authored complete method bank).

All five observed easy sources replay exact prompts, full worked solutions, complete five-option banks and correct designations. Moderate and hard are explicitly authored rational-bookkeeping bands within the same construction method, with bounded work per band. Normal default sampling serves all five source families with five method-derived complete banks. The full mathematical objects are definite integrals; all ten option pairs are checked for equality of actual definite value, including two incorrect options. Native radio grading checks UUID ownership and selection separately.

Validation reads actual displayed function, coordinates, parametrization, vector stages, derivative inputs/vector, speed, full function pullback, both weighted integral rows and every displayed answer. It verifies log branches over the entire interval, formatting, public explicit guards, deterministic identity, complete source replay and engine outcomes. `validation.json` reports exact counts, hashes and a conservative enumerated meaningful-capacity lower bound that excludes reversed traversal, translations, option order and bank aliases. Review originals and variants are in `review.md` and `review.json`.

Historical distractor intent remains underidentified, especially √27 and √20 speed choices; the empirical operations are explicit evidence recipes rather than claims to reconstruct MA's code. Exact replay is separated from method-bank defaults. Source math has no identified error or presentation repair. All learner solutions end at the constructed integral; exact/numerical integration occurs only in generator rejection and author validation.
