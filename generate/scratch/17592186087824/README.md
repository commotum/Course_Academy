# Shift and stretch from exponential growth curves

Private draft for KP17592186087824, math basis 1356. No database writes. Identifies c from the horizontal asymptote, then k from the y-intercept by subtraction. Base is provided; no graph-selection or base-recovery tasks.

Verify:

```sh
.venv/bin/python generate/scratch/17592186087824/validate.py
.venv/bin/python generate/scratch/17592186087824.py --difficulty all --seed 12 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186087824.py --difficulty moderate --profile source:q-7241 --format json
```

API: generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None), plus generate_easy/generate_moderate/generate_hard. Parameters b,k,c, optional step; strict difficulty guards apply to explicit calls. Templates read_parameters (easy), read_equation (moderate), read_grid_equation (hard). Normal profiles intercept_shift and grid_reading. Source:q-N profiles are exact historical evidence with underdetermined error intent and keep raw missing attributes. All defaults use eligible, complete method-derived five-option banks.

Easy and moderate have observed ratings. Hard is an authored fractional-grid extension of the same reconstruction skill. Original and changed-parameter source-bank reviews plus four normal examples per level are in review.md/review.json. Source-cases.json replays all seven practice originals through the public API. Validation separates exact source bank/prose/presence fidelity, displayed mathematics, native grader checks and raster geometry. Two legacy sources lack correct refs/solutions/rating; inferred native fixtures are separate, not matched original designations. Original uncalibrated horizontal axes prevent numerical base recovery; supplied bases are retained.

Read classification.md, template-extraction.md and plot-spec.md for scope and evidence. Runtime uses the primary .venv where dependencies are available, with an existing read-only Python3.10/Matplotlib wheel cache fallback if needed; actual versions appear in sidecars. No environment installations. Retired v1–v4 caches are retained for active-reader safety; v5 is the accepted measured-placement and raster readback. Feature labels use nearest measured clear boxes without backgrounds. Hard tick labels stay at exact grid y coordinates, use measured regular naming spacing, and suppress collisions around the assessed features. Placement regressions include origin and signed near-zero intercepts, numerical bounds and largest quarter-grid viewports. Raw-source CLI previews state actual difficulty/unrated, authored-level and inferred-correct flags. freeze.json binds the private draft and evidence hashes.
