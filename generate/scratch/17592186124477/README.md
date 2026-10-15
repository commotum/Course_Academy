# Pivot columns of a REF matrix

Validated easy generator: `generate/scratch/17592186124477.py`. Moderate/hard exceptions and the 40-task structural bound are recorded in capabilities.json. See classification.md, template-extraction.md, source-components.json, source-fidelity.json and review.md for source evidence and fidelity.

```sh
.venv/bin/python generate/scratch/17592186124477.py --difficulty easy --count 5 --seed 19 --format json
.venv/bin/python generate/scratch/17592186124477.py --profile q-73607 --seed 19 --format markdown
.venv/bin/python generate/scratch/17592186124477/validate.py
.venv/bin/python generate/scratch/17592186124477/replenish.py
```

Python and SymPy versions are retained with each instance. Validation uses the existing check-engine executable to test the actual application grader. The generator itself performs no database operations. Replenishment reuses the configured EDB integration and contributor, rechecks inventory under api.lock, preserves complete requests and verifies the exact committed basis. A stock already meeting the reserve requires only generator registration. Original source records and learner history are immutable inputs to this package.
