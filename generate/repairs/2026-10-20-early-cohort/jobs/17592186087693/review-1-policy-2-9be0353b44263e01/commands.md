All commands run in evidence_root. Package inputs read-only; Python uses -B.

Set task_python=/home/jake/Developer/Course_Academy/.venv/bin/python and task_repo=/home/jake/Developer/Course_Academy.

1. "$task_python" -B audit.py (48 fresh records, 37 explicit shapes, source replays, controls, deterministic CLI and relocation; seeds/parameters retained in records).
2. "$task_python" -B verify_repair.py (both regressions against old/current packages, plus Chelsea column control).
3. "$task_repo/generate/runs/current/check-engine" grader-input.json grader-results.json
4. For samples.json and runner-batch.json separately: "$task_python" -B "$task_repo/generate/pipeline/check_delivery.py" --input INPUT --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-sample_OR_delivery-batch --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
5. python3 variation.py
6. Actual renderer: "$task_python" -B "$task_repo/generate/pipeline/render_preview.py" --input INPUT --output OUTPUT --limit 6 --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
   INPUT/OUTPUT: render-input.json/render (first six), render-remaining.json/render-remaining (next six), render-middle.json/render-middle (five batch records and source replay), render-last.json/render-last (column control). The original 13-record remaining render was terminated after eight images without a report; bounded chunks supersede it.
7. Inspect screenshots; record visual-inspection.json; python3 finalize.py validates schema/evidence paths/integrity and writes result.json.

Provenance: audit.py, variation.py and replay_regression.py adapted/copied from previous independent review; revision-scope.json records bindings and changed files. Source account was verified and written before reading package files. No author result is treated as independent approval. The old relocated package remains only a negative control, never a publication candidate.
