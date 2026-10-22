Run from this evidence directory with `PYTHONDONTWRITEBYTECODE=1`. All output paths are inside this directory. No publication/database command was run.

```bash
PY=/home/jake/Developer/Course_Academy/.venv/bin/python
REPO=/home/jake/Developer/Course_Academy
JOB=/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186087886
E="$PWD"
"$PY" review_setup.py
"$PY" author-replay/workspace/checks/check_repair.py > author-regression.log 2>&1
"$PY" regression_controls.py
"$PY" independent_review.py > independent.log 2>&1
```

`review_setup.py` copies the supplied package/source into evidence and runs retained checks there. `regression_controls.py` reproduces the historical shortest-answer failure with the retained v1.1.0 implementation and the packaging failure by omitting the required local module in a disposable manifest. `independent_review.py` checks the current package with independent displayed-math parsing, fresh seeds, all eight source banks, boundaries, stale/grouping negative controls and native grading.

```bash
for NAME in batch-records independent-records fresh-batch; do
  "$PY" "$REPO/generate/pipeline/check_delivery.py" --input "$E/$NAME.json" --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty easy --output "$E/delivery-$NAME" --asset-root "$E" --math-root /media/jake/SSD/EDB/math
done
"$PY" "$REPO/generate/pipeline/render_preview.py" --input render-records.json --output render --asset-root . --math-root /media/jake/SSD/EDB/math > renderer.log 2>&1
"$PY" "$REPO/generate/pipeline/render_preview.py" --input counterfactual-render-records.json --output counterfactual-render --asset-root . --math-root /media/jake/SSD/EDB/math > counterfactual-renderer.log 2>&1
"$PY" finish_review.py > finish.log 2>&1
"$PY" write_report.py
```

The first renderer uses its default limit of six, covering all five normalized runner records and the negative-shift rational counterfactual. The second renders the remaining five review records. Input JSON arrays, HTML, screenshots and reports are retained. `fresh-math-results.json` was produced by applying `independent_review.validate` to each record in `fresh-batch.json`. `finish_review.py` additionally exercises fresh cancellation targets, runs their actual delivery filter, measures shortcuts and selection rules, repeats native grading including normalized records, and checks exact dependencies/package hashes. `write_report.py` compiles the review; schema and relative evidence paths were validated separately with jsonschema.

Native harness commands and complete inputs/results are in `grader-command.json`, `grader-input.json`, `grader-report.json`, `grader-final-command.json`, `grader-final-input.json` and `grader-final-report.json`. Source-first analysis was written and verified before package inspection. The package hashes were captured before any executable package test; final comparison is in `package-final.json`.
