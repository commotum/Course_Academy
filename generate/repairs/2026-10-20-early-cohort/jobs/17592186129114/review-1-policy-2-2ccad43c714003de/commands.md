All commands run from this evidence directory, with PYTHONDONTWRITEBYTECODE=1 for generator imports. No package/database/publication writes.

1. `PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python audit.py`
   Current complete source replay, seeds 114031..114038 in each supported profile, raw/pool seed 782311, relocation seed 802139, mathematical and packaging assertions.
2. `PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python author-check/regression_pool.py`
   Exact retained preflight executable copied unchanged; common.py redirects only root/evidence. Historical witness must exit 1. Current seeds 924724049,0,802139,920113, actual delivery and native grader.
3. `python3 batch_role_probe.py historical-runner-batch.json historical-role-results.json` (expected exit 1)
   `python3 batch_role_probe.py delivery-batch/accepted.json batch-role-results.json` (expected exit 0)
4. `/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input runner-batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --asset-root ../workspace --math-root /media/jake/SSD/EDB/math`
   Repeat with `--input independent-samples.json --output delivery-independent` for the control.
5. `PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python c_counterfactual.py`
6. `PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python inventory_probe.py`
   `/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input inventory-reproduction-input.json --source ../source/source.json --inventory inventory-empty-for-identity-check.json --difficulty easy --output inventory-identity --asset-root ../workspace --math-root /media/jake/SSD/EDB/math`
7. `PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python stage_audit.py`
   Independently chosen fresh pool seeds 20261021,37193, read-only delivery, conditional shortcut probes, identity-matched inventory reconstructions, 32 deterministic selection examples. Actual subprocess commands/results saved in commands.log.
8. `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine final-grader-input.json final-grader-results.json`
9. `/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --asset-root ../workspace --math-root /media/jake/SSD/EDB/math`
   Repeat with `--input render-counterfactual-records.json --output render-counterfactual --limit 6`. Each invocation renders six actual-UI previews; screenshot inspections listed in render-inspection.json.
10. `PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python finalize_review.py`
   Asserts completed results, retained preflight hash, strict empty-parameter rejection/deterministic seeded resampling, relative evidence contract, runtime versions and all-file package immutability. Writes review.json/result.json. Source analysis was confirmed/written before package inspection; provenance.json documents reused unaffected evidence.

The replay text checker normalizes repeated whitespace in its classification sentence check: source q-72498 has two spaces before "is". Full replay bank/content comparisons remain exact except independently documented source corrections. This avoids a string-matching false positive without changing source or generated content.
