All commands run from this evidence directory. They read the package and captured database snapshots without publishing or opening the database. `targeted-regressions.py` intentionally exits 1 on this package. Its JSON report names the two failing tests. The other commands should exit 0.

```bash
export PYTHONDONTWRITEBYTECODE=1
REVIEW_PY=/home/jake/Developer/Course_Academy/.venv/bin/python
REVIEW_REPO=/home/jake/Developer/Course_Academy
REVIEW_JOB=/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186105746
"$REVIEW_PY" review.py
"$REVIEW_PY" "$REVIEW_REPO/generate/pipeline/check_delivery.py" --input easy-records.json --source "$REVIEW_JOB/source/source.json" --inventory "$REVIEW_JOB/source/inventory.json" --difficulty easy --output delivery-domain --math-root /media/jake/SSD/EDB/math
"$REVIEW_PY" "$REVIEW_REPO/generate/pipeline/check_delivery.py" --input batch-records.json --source "$REVIEW_JOB/source/source.json" --inventory "$REVIEW_JOB/source/inventory.json" --difficulty easy --output delivery-batch --math-root /media/jake/SSD/EDB/math
"$REVIEW_PY" expected_counterfactual.py
"$REVIEW_REPO/generate/runs/current/check-engine" grader-complete-input.json grader-complete-results.json
"$REVIEW_PY" "$REVIEW_REPO/generate/pipeline/render_preview.py" --input render-records.json --output render-all --limit 11 --math-root /media/jake/SSD/EDB/math
"$REVIEW_PY" "$REVIEW_REPO/generate/pipeline/render_preview.py" --input expected-counterfactual-records.json --output render-expected --limit 2 --math-root /media/jake/SSD/EDB/math
"$REVIEW_PY" finish_review.py
"$REVIEW_PY" targeted-regressions.py
"$REVIEW_PY" write_report.py
```

`render-records.json` is retained complete input: exact runner batch (5), supported relevant/irrelevant counterfactual pairs (4), and two independently selected moderate cases q-130924 at scale -3 and q-20960 at scale 2. It can be reused unchanged. All deterministic construction calls in review.py use fresh review seed 7331 with explicit templates/scales. `batch-records.json` retains the runner's original seed 4029664877 and all original generation metadata.

The actual native grader report contains 200 complete cases, with all five radio choices submitted per case: 200 accepted and 800 rejected. `expected-counterfactual-records.json` clearly labels the independently authored expected consistent instance. This is a repair oracle, not an assertion that the current generator supports it.

Relocation uses the manifest package copied to `relocated-package/` under this evidence directory; it writes CLI output to `relocated-records.json`. Package hashes refer to the original read-only workspace.

Interpretation: q-42157 has all eight variants inconsistent. Selecting No solution from the visible coefficient -6 succeeds on 8/8 raw variants and 7/7 after actual inventory deduplication. Changing only second RHS from -10 to -8 must instead make the system consistent. The renderer shuffles answer positions; the semantic shortcut is unaffected. This is a family-wide construction failure, also present in the runner's delivered five-question batch.
