All commands run from this evidence directory, with PYTHONDONTWRITEBYTECODE / -B protections. No package mutation, publication or database write.

Independent source-analysis.json was written and read back before inspecting package files. Original source and generate/principles.md were the only instructional authorities at that point. Reused earlier independent parser/harness/selection code is attributed by hashes in script-provenance.json; seeds and bank controls were updated for this package.

Use P=/home/jake/Developer/Course_Academy/.venv/bin/python and REPO=/home/jake/Developer/Course_Academy as shell abbreviations if rerunning; the paths are explicit below.

/home/jake/Developer/Course_Academy/.venv/bin/python -B review.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input samples.json --output delivery --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input runner-batch.json --output batch-delivery --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B variation_audit.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B selection_check.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input bank-assignment-control.json --output control-delivery --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B delivery_audit.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input-complete.json grading-complete.json
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --limit 24 --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input additional-render-records.json --output additional-render --limit 14 --math-root /media/jake/SSD/EDB/math
python3 -B finalize_review.py

The renderer's default six-case limit was discovered from its actual report; full-limit reruns cover all 38 intended records. Contact sheets and underlying screenshots were visually inspected. Intermediate native runs are retained; grading-complete.json is the final combined grader result.

Final contract validation uses system python3 because jsonschema is installed there; generator/runtime/grader tests above used the job Python.
