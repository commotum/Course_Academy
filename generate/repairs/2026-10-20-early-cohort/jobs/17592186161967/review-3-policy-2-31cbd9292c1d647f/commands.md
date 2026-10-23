All commands run from this evidence_root. Generator package and database remain read-only. Context Python: /home/jake/Developer/Course_Academy/.venv/bin/python. Use -B to avoid bytecode writes.

1. `context-python -B review.py` — source replay, fresh seeds 73691..73694 per profile, ten-profile sign quartets (98641), controlled counterfactuals (472), nine-coordinate boundaries (79213), source replay (94739), dependency and generator rejection checks; copies manifest files under relocated/.
2. `execution-results.json` retains exact executable commands and exit codes for both author and independent historical/current regression controls, shared delivery of batch.json/fresh-samples.json, and relocated CLI replay at seed 1278010737/count 5. Historical controls intentionally exit 1 for the demonstrated defects. Author scripts are isolated under control-*/; their delivery paths point at captured source/inventory.
3. `context-python -B followup.py` — independently chosen fresh CLI seed/count pairs 49217/12, 10983/5, 483/2, 904/3; selection model and post-delivery measurements; exact historical batch validation.
4. `context-python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input fresh-cli.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-cli --math-root /media/jake/SSD/EDB/math`
5. `context-python -B grade_and_probe.py`
6. `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-combined-input.json grader-report.json`
7. `context-python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --limit 8 --math-root /media/jake/SSD/EDB/math`
8. `context-python -B layout_probe.py` — actual UI scrollability check, no UI modifications.
9. `python3 -B finalize.py` — schema, evidence existence, results, and package SHA256-map verification. System Python's jsonschema is review-only; generator tests use context Python.

Retained reproduction with explicit candidate records: `context-python -B reproduce_batch_shortcut.py delivery-batch/accepted.json`. Historical failing records: negative-batch-records.json; minimal first historical failure: negative-bank-records.json. Full input/seed metadata are included in each generated record.

Source analysis reused with confirmed source passages before package reading; provenance.json records prior independent review. A bootstrap attempt to locate a historical script failed before copying it; corrected to review-0's relocated snapshot. No package writes occurred. The resampling trace was corrected to line 73 with distinct loop-index counting (inline comprehensions emit repeated line events), without changing tested records or generator behavior.
