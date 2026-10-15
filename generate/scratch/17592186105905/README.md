# Quadrilateral area generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186105905/validate.py
.venv/bin/python generate/scratch/17592186105905.py --difficulty all --seed 401 --count 2 --format json
.venv/bin/python generate/scratch/17592186105905.py --difficulty moderate --template q-67787 --profile observed-q-67787 --count 1
```

API: generate_easy, generate_moderate, generate_hard; generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None). Public templates are the ten source IDs in recipes.json. Defaults use method-derived complete banks; observed-<ID> profiles are raw, evidence-only/ineligible, preserving original omissions/errors. Blank/radio layouts follow each template; fieldless raw remains fieldless, and normal completion is an authored blank. See classification.md for source-grounded level design and constraints, template-extraction.md for all banks/anomalies, and plot-extraction.md for diagrams. review.json/review.md include every original and two generated variants per source mask plus at least two per level. validation.json separates full-source fidelity, mathematical checks and native grading.

The original generator evidence is frozen at math basis 1356. Historical wrong-choice intent remains unresolved and is not promoted to learner generation. The two missing source correct designations and one absent field stay absent in that raw public replay. Normal source repairs are explicit.

Inventory replenishment was verified at math basis **2692** (preparation basis 2691): five easy and five hard questions added, with ten existing moderate questions retained. All source questions and learner history were preserved. The generator UUID is `6893e50d-e3f7-5b49-8a0d-a1072f81fe87`, registered to `generate/scratch/17592186105905.py`. `classification-current.md` covers the current source additions; `capabilities.json` states the bounded source-profile coverage. Exact requests, preview, receipt, published image hashes, native grading, visual review and readback are in `reference/replenishment/basis-2691/`.

`replenish.py` uses the configured application contributor and holds the application `api.lock` through the fresh inventory read, basis-guarded submission and exact-basis verification. A saved commit intent is recovered before new planning. No engine or scheduler code was changed.
