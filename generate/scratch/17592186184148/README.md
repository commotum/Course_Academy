# Cotangent stretch/vertical-shift draft

Verification: `.venv/bin/python generate/scratch/17592186184148/validate.py`.

Preview: `.venv/bin/python generate/scratch/17592186184148.py --difficulty all --count 2 --seed 4 --format markdown` (or `--format json`). Source replay: `--difficulty moderate --profile observed_q-65549`.

Only KP 17592186184148, frozen math basis 1356. Steps 3–7, no registration, DB writes, engine changes or commits. Parameter-dependent plots are Matplotlib PNGs under this private folder. `render.py` uses the read-only cached Python 3.10 Matplotlib environment; actual runtime/dependency versions, label boxes and geometry are recorded per PNG sidecar. Primary generator and validation use the project .venv.

All observed banks and masks replay publicly; they are evidence-only because scalar error intent is underdetermined. Normal defaults use complete method-derived five-choice banks. Source omission and q-79188 legacy duplicate are retained separately from the authoritative supported native single-field fixture. Missing easy/hard levels are explicitly authored. See classification.md, template-extraction.md, plot-extraction.md, source-geometry.json, bank-mapping.json, review.md, review.json, validation.json and engine-report.json.
