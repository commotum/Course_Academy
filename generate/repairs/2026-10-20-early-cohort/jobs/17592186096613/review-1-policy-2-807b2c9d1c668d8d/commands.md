Commands run from this evidence directory. All writes stay here; imports disable bytecode.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python review_checks.py > review-checks.log 2>&1
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python reproduce_source_gap.py --package ../review-0-policy-2-81a000b338586d94/relocated --output original-failure.json
# Previous package exits 1; current package exits 0:
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python reproduce_source_gap.py
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python author_regression.py > author-regression.log 2>&1
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python author_negative_control.py > author-negative-control.log 2>&1
# Negative control exits 1 at the retained minimal counterexample.
```

For each pair `(batch.json, delivery-batch)` and `(samples.json, delivery-samples)`:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input INPUT --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output OUTPUT --asset-root assets --math-root /media/jake/SSD/EDB/math
```

```sh
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python supplement_checks.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-combined-input.json grader-report.json > grader.log 2>&1
python3 /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render-pairs --limit 25 --math-root /media/jake/SSD/EDB/math > render.log 2>&1
python3 /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input delivery-batch/accepted.json --output render-delivered --asset-root delivery-batch/assets --math-root /media/jake/SSD/EDB/math > render-delivered.log 2>&1
python3 variation_checks.py --candidate-records batch.json > variation.log 2>&1
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python finalize_review.py
```

Fresh sample seeds: 73001..73024; explicit boundaries seed 808; counterfactual seeds 53/54; denominator-5 case seed 761. CLI batch: seed 3129290382, count 5, easy. Complete inputs and records are retained, including historical-records.json and grader-combined-input.json. `supplement_checks.py` appends checks to that retained combined input; regenerate or copy the saved input for an exact native grading replay. Renderer default six-record limit was corrected to 25 before the completed inspection. Source analysis and script provenance are in source-analysis.json and provenance.json.
