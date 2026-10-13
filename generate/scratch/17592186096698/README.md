# Local curve-family generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186096698/validate.py
.venv/bin/python generate/scratch/17592186096698.py --difficulty all --seed 2 --count 2 --format json
.venv/bin/python generate/scratch/17592186096698.py --difficulty moderate --profile raw-q-119132 --format markdown
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and individually documented easy/moderate/hard entrypoints. Normal templates: linear/quadratic/cubic/logarithmic/reciprocal (easy); cubic/exponential (moderate/hard). Profile `authored-five-family` is normal. Eleven `raw-q-…` profiles expose observed banks with honest metric-inference limits; these preserve source fields and absent attributes. `source-cases.json` supplies exact reference parameters.

Directly integrate the displayed ODE and identify its whole solution family. No IVPs or other ODE methods. Source replay preserves 11 prompts/solutions, 12 field banks, 60 captured image-choice records and 11 present correct designations. Hard is authored. Normal shifts use {−2,−1,0,1,2}, omitting zero for moderate/hard cubic tasks; fractional shifts are rejected, including huge denominators. Four raw distractor metric coefficients are uncertain; normal generation excludes them and uses exact operation banks. Source PNG identity is counted separately from extracted geometric confidence.

Independent verification reads the actual ODE and displayed final primitive, differentiates every complete choice curve, compares general families modulo constants, checks source key presence/full banks/full solutions, exercises level guards and identity, tests concurrent fresh Matplotlib writes, and calls the real native grader on every designated image choice. The renderer uses the cached Python3.10/Matplotlib fallback read-only, installing nothing. Unique requests and atomic PNG+sidecar outputs stay private. `frozen-artifacts.json` is recorded after all producers end; no cache pruning. Steps 3–7 only; zero database writes.
