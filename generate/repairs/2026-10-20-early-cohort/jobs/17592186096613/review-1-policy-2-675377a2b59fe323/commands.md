All commands run from evidence_root; package is read only. PYTHONDONTWRITEBYTECODE=1 for package imports.

- Repo Python: /home/jake/Developer/Course_Academy/.venv/bin/python
- `python reproduce_source_gap.py --package ../review-0-policy-2-81a000b338586d94/relocated --output original-failure.json` (expected exit 1); same with default package and `--output repaired-gap.json` (exit 0).
- `python retained_regression_original.py > retained-regression-original.log 2>&1` (expected exit 1). This is the retained executable check redirected to prior immutable package and evidence outputs.
- `python retained_regression.py > retained-regression.log 2>&1` (exit 0). Copied author regression writes only author-regression/ under evidence_root.
- `python review_checks.py > review-checks.log 2>&1` (exit 0). Reused independent script updated with fresh seeds 57103..57114, quotient boundaries and controlled pairs. Early reviewer-script invalid negative fraction probe was corrected to valid positive numerator change; no generator repair occurred.
- `python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --asset-root . --math-root /media/jake/SSD/EDB/math` (exit 0). Repeat with samples.json and delivery-samples (exit 0).
- `python supplement.py > supplement.log 2>&1` (exit 0), after review_checks finishes. Adds denominator pair, every-row checks, grader inputs. Early reviewer parser missed derivative operators followed by TeX sizing commands; normalization fixed without changing any test expectations.
- `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-combined-input.json grader-report.json > grader.log 2>&1` (exit 0).
- `python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render-pairs --asset-root . --math-root /media/jake/SSD/EDB/math --limit 32 > render-pairs.log 2>&1` (exit 0). Initial default limit rendered only six, so repeated with explicit full limit.
- `python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input delivery-batch/accepted.json --output render-delivered --asset-root delivery-batch/assets --math-root /media/jake/SSD/EDB/math > render-delivered.log 2>&1` (exit 0).
- `python3 variation_checks.py --candidate-records batch.json > variation.log 2>&1` (exit 0), after rendering.
- `node ui-order-probe.js delivery-batch/accepted.json` (exit 0). Exact application choiceOrder function tests the observed synthetic preview-ID coincidence; accepts an explicit candidate file.
- `python3 finish_review.py` (exit 0).

Reused source/inventory/engine evidence is identified in provenance.json. Source hashes and policy matched by runner; all cited source questions and banks were checked directly before copying source-analysis.json. Current package and batch checks were rerun. No database writes, publication, or package edits.
