# Parallel-vector factor generator

Verify with `.venv/bin/python generate/scratch/17592186096648/validate.py`.
Preview with `.venv/bin/python generate/scratch/17592186096648.py --difficulty all --seed 10 --count 2 --format markdown` (or json).

Public faithful raw replay:

```sh
.venv/bin/python generate/scratch/17592186096648.py --difficulty easy --template target_first --profile raw_12135 --parameters '{"u":"1","v":"-3","k":"4"}' --format json
.venv/bin/python generate/scratch/17592186096648.py --difficulty moderate --template lambda_first --profile raw_12139 --parameters '{"u":"-1/2","v":"6","k":"-2"}' --format json
```

Both originals are unrated and lack worked solutions/correct refs. Raw outputs preserve those omissions, are evidence-only and cannot be native-graded without invented refs. Normal five-choice radio questions use an authored method bank and complete fixed worked solutions. All E/M/H scopes are authored and source/lesson-grounded. Zero vectors are parallel to any vector in this curriculum; declared nonzero source equality excludes them. The generator has no plots or database calls. Freeze and runtime hashes are in freeze.json and validation.json.

Inventory job `7d775e945c441ce31e7e714591367818667583367a6cf3aefea8dea373ee7982` completed stages 8–9 on 2026-10-13. The scoped transaction at basis 2133 committed at **2134**, adding 15 distinct practice questions, five per supported band, and registering generator UUID `7d18fadd-926e-5ea0-82ac-e7e894e439e5` with script `generate/scratch/17592186096648.py`. All original content and learner history were preserved. Exact requests, native grading evidence, previews, receipts and readback are in [reference/replenishment/basis-2133](reference/replenishment/basis-2133). A confirmed stale-basis rejection from the prior attempt is archived under basis-2132; it did not commit.

`replenish.py` is the retained preparation/submission/recovery runner for this specific job. It uses the application contributor, holds `api.lock` from fresh inventory through submission and readback, guards commits by basis, validates every choice through the current native grader, and deduplicates mathematical tasks across levels and existing content. [capabilities.json](capabilities.json) records the authored bands, finite sampling domains and source limitations. The final inventory at basis 2134 has no remaining job for this KP.
