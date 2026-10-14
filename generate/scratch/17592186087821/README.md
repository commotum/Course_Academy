# Vertical shift recognition generator

Run `.venv/bin/python generate/scratch/17592186087821/validate.py` from the
repository root. CLI: `.venv/bin/python generate/scratch/17592186087821.py
--difficulty all --seed 42 --count 2 --format json` (put this command on one line).
API has generate_easy, generate_moderate, generate_hard and generate with optional
parameters/profile. Parameters are exactly b,c. The sole template is
identify_shifted_growth; radio is the only field type.

Seven original full-bank evidence profiles `observed:q-...` preserve all
35 images and raw omissions through the same public API. Five present correct
refs and five present complete solutions replay; the two missing correct refs
remain missing. Defaults use two explicitly authored method-derived complete
banks. Hard is a missing-level authored fractional-grid recognition extension.
No shifted/stretched target, unknown-shift task or other KP is introduced.

See classification.md, template-extraction.md and plot-extraction.md for scope,
finite task domains and original unticked-horizontal-scale uncertainty. All
observed profiles are evidence-only and ineligible for learning. Native grader
checks are separate from complete original fidelity and actual raster geometry.
Generator and renderer hashes/runtimes are frozen in validation.json. review.md
labels originals and generated examples; review.json is local preview data,
never a database transaction. No EDB writes or shared files are changed.

Renderer v8 measures text boxes and places coordinate/asymptote labels clear of axes, curves, markers, arrows and other labels without feature-label backgrounds. validate.py checks 16 near-zero/origin/base-boundary image regressions and all 35 independently read source features, retaining the corrected q-170588 fifth option. Actual CLI JSON/Markdown previews include original/generated labels, actual levels, correct-choice markers and hash/runtime manifests; CLI output is included in native grading.

Inventory replenishment: `.venv/bin/python generate/scratch/17592186087821/replenish.py`. This scoped worker validates retained output, rechecks inventory and sources under the application API lock, registers the stable generator UUID, publishes content-addressed PNGs, and previews/commits/reads back through the existing EDB integration. Exact intent, EDN, receipt and verification are retained under `reference/replenishment/`. Only generated records are added; incomplete unrated originals remain excluded. Version 8 adds continuous-curve text clearance to prevent steep-curve sampling gaps.
