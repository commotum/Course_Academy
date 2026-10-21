All paths below are run from evidence_root. Scripts disable bytecode writes. No database operations.

- `/home/jake/Developer/Course_Academy/.venv/bin/python -B audit.py`
- `/home/jake/Developer/Course_Academy/.venv/bin/python -B reproduce_missing.py > missing-reproduction.json` (exit 1 demonstrates defect)
- `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-results.json`
- `/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input random-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-sample --math-root /media/jake/SSD/EDB/math`
- Same delivery command with `--input runner-batch.json --output delivery-batch`.
- `python3 -B variation.py`
- `/home/jake/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node ui-order.cjs`
- `/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --math-root /media/jake/SSD/EDB/math` (default 6)
- Same renderer with `--input counterfactual-records.json --output render-pairs --limit 9`.
- Same renderer with `--input delivery-batch/accepted.json --output render-delivered --limit 5`.
