# Parallel-vector factor generator

Verify with `.venv/bin/python generate/scratch/17592186096648/validate.py`.
Preview with `.venv/bin/python generate/scratch/17592186096648.py --difficulty all --seed 10 --count 2 --format markdown` (or json).

Public faithful raw replay:

```sh
.venv/bin/python generate/scratch/17592186096648.py --difficulty easy --template target_first --profile raw_12135 --parameters '{"u":"1","v":"-3","k":"4"}' --format json
.venv/bin/python generate/scratch/17592186096648.py --difficulty moderate --template lambda_first --profile raw_12139 --parameters '{"u":"-1/2","v":"6","k":"-2"}' --format json
```

Both originals are unrated and lack worked solutions/correct refs. Raw outputs preserve those omissions, are evidence-only and cannot be native-graded without invented refs. Normal five-choice radio questions use an authored method bank and complete fixed worked solutions. All E/M/H scopes are authored and source/lesson-grounded. Zero vectors are parallel to any vector in this curriculum; declared nonzero source equality excludes them. No plots, DB calls or registration. Freeze and runtime hashes are in freeze.json and validation.json. Stop at guide step 7.
