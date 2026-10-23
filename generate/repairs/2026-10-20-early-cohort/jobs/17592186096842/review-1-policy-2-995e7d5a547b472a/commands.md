Review commands (run from evidence_root; all generated output stays here):

- `/home/jake/Developer/Course_Academy/.venv/bin/python -B audit.py > audit.log 2>&1` — current source replay, fresh samples, controlled pairs, relocation and boundaries.
- `/home/jake/Developer/Course_Academy/.venv/bin/python -B verify_saved.py > verify-saved.log 2>&1` — independent displayed-function differentiation; domain-aware radical equivalence; creates batched grading inputs. Reran after focused samples were added.
- `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-results.json > grader.log 2>&1` — actual native grader, final 414 checks.
- `/home/jake/Developer/Course_Academy/.venv/bin/python -B regression_recheck.py > regression-recheck.log 2>&1` — unchanged author spacing-check function against old negative control and current samples; only author output directory redirected.
- `/home/jake/Developer/Course_Academy/.venv/bin/python -B inspect_cues.py independent-samples.json > cues.log 2>&1`
- `/home/jake/Developer/Course_Academy/.venv/bin/python -B focused_followup.py > focused.log 2>&1`
- `/home/jake/Developer/Course_Academy/.venv/bin/python -B nearest_zero_regression.py > nearest-zero.log 2>&1` — expected exit 1 on current generator.
- `/home/jake/Developer/Course_Academy/.venv/bin/python -B nearest_zero_regression.py delivery-focused/accepted.json > nearest-zero-delivered.log 2>&1` — expected exit 1 after shared filtering.
- `/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input batch-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --asset-root . --math-root /media/jake/SSD/EDB/math`
- Repeated delivery for `independent-easy.json`, `independent-moderate.json`, `independent-hard.json` with matching difficulty/output directory, and `focused-samples.json` with easy/output `delivery-focused`. Reports retain exact input hashes and counts.
- `/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --asset-root . --math-root /media/jake/SSD/EDB/math` — default first six.
- `/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-extra-records.json --output render-extra --limit 8 --asset-root . --math-root /media/jake/SSD/EDB/math`
- `/home/jake/Developer/Course_Academy/.venv/bin/python -B finish_review.py > finish-review.log 2>&1`
- `python3 write_result.py` and `python3 validate_contract.py` — assemble and validate report/evidence references.

Source-analysis.json was written and read back before author inspection. Reused scripts/data provenance and unchanged-file hashes are in provenance.json. No database writes or publication. All package files were hashed before tests and verified unchanged after tests.
