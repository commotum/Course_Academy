# General-base logarithm derivative generator

Frozen math basis1356; all12 source questions are publicly replayable. Raw replay preserves omissions and is evidence-only. Normal output covers easy, authored moderate and observed hard. The prior basis1905 draft is archived under `previous-basis1905/`.

```sh
.venv/bin/python generate/scratch/17592186096615/validate.py
.venv/bin/python generate/scratch/17592186096615/validate-boundaries.py
.venv/bin/python generate/scratch/17592186096615.py --difficulty all --seed 40 --count 2 --format json
```

Python API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`, plus all three level wrappers. Profiles: `raw-source`, `observed-bank`, `authored-bank`, `normal`. Use source-case parameters and `raw-source` to preserve source absence/field contracts. Opaque observed banks are evidence-only; authored complete banks supply normal practice. Fixed parameters determine IDs independently of option order/seed. CLI batches deduplicate mathematical tasks.

All logarithm arguments stay x>0, integer bases2..12; no next-topic chain rule. No plots or database writes. `validation.json` separates exact fidelity, completed normal correctness and native grading. `review.md`/`review.json` show every source and two variants per template. The raw exact-answer wording has a documented equivalent-entry rejection; normal wording accepts independently derived common-denominator equivalents.

Legacy `reference/`, `replenish.py`, `check-current-engine`, `capabilities.json`, `freeze.json`, `previews.md`, `current-engine-build.json` and `side-by-side.json` remain historical basis1905/1906 artifacts and are not used by this frozen generator or validation. Shared native checks use `generate/runs/current/check-engine`.
