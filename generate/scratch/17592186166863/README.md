# Identifying Conservative Vector Fields

Run `.venv/bin/python generate/scratch/17592186166863.py --difficulty moderate --count 5 --seed 20261014` for JSON; add `--format markdown` for review.
The stable generator UUID is derived from the existing KP UUID and registered
through question-generator/id and question-generator/script by replenish.py.
No source question, canonical example or learner history is revised.

Validation: `.venv/bin/python generate/scratch/17592186166863/validate.py`.
Uses project SymPy and the actual application grader at generate/runs/current/check-engine.
Independent LaTeX parsing requires antlr4-python3-runtime 4.11.1; this run installed
it only in /tmp/ca-17592186166863-deps, with a separate temporary uv cache. To
recreate: `UV_CACHE_DIR=/tmp/ca-17592186166863-uv uv pip install --python .venv/bin/python --target /tmp/ca-17592186166863-deps antlr4-python3-runtime==4.11.1`.
Normal generator execution uses only the existing SymPy dependency and its frozen
source-components.json; it does not need the parser dependency.

reference/replenishment retains inventory snapshots, exact transactions, requests,
previews, receipts and exact-basis verification. replenish.py acquires the
application api.lock before inventory planning and holds it through readback.
