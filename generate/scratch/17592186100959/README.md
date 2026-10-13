# KP 17592186100959

Verify all three supplied functions against a first-order ODE and choose the complete subset. There are 11 observed moderate originals; easy and hard are explicitly authored within the same method. No ODE solving, initial conditions, plots, database transactions or registration.

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186100959.py --difficulty all --count 2 --seed 9 --format markdown
.venv/bin/python generate/scratch/17592186100959/validate.py
.venv/bin/python generate/scratch/17592186100959/boundary-qa.py
.venv/bin/python generate/scratch/17592186100959/presentation-qa.py
```

Public source replay: `generate("moderate", profile="q-141096", parameters={"scale":1})`. All 11 original profiles are listed in `source-cases.json`; generated source-mask variants use scale 2 and -3. Raw profiles retain source failed-equality notation and are marked evidence-only. Authored defaults use corrected query/nonidentity stages and complete five-choice subset banks.

`classification.md` documents observed labels and authored workload bounds. `template-extraction.md` maps every original option and ordered stage. `review.md`/`review.json` show all originals and labeled variants. `validation.json` separates exact source fidelity, independent displayed mathematics, actual native grading and sampled meaningful diversity. `freeze.json` records final hashes; a validator rerun reproduces artifacts deterministically.

`boundary-validation.json` independently checks 25 explicit edge records (including easy all-three solutions, hard coefficient extremes and every source scale ±6), 125 additional native checks, five invalid scope guards and deterministic six-record CLI output. These checks are separate from the sampled/source denominators in `validation.json`.

Markdown previews and review headings show Easy (E), Moderate (M) or Hard (H), observed/evidence-only versus authored origin, and the correct option. `presentation-validation.json` confirms all 47 stored mathematical records remain unchanged, all 11 raw prompt/solution pairs remain exact, and the six-record JSON CLI hash is unchanged.
