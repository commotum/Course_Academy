Run from evidence_root. All outputs stay here; no package or database mutation.

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python -B review.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B author-regression-adapted.py ../workspace/17592186161967.py current
/home/jake/Developer/Course_Academy/.venv/bin/python -B author-regression-adapted.py ../review-0-policy-2-b2ba6e2b0f4d64c5/relocated/17592186161967.py old
/home/jake/Developer/Course_Academy/.venv/bin/python -B reproduce_shortcut.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B reproduce_shortcut.py ../review-0-policy-2-b2ba6e2b0f4d64c5/relocated/17592186161967.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-report.json
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input fresh-samples.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-fresh --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B relocated/17592186161967.py --seed 91643 --count 3 --format json > relocated-output.json
/home/jake/Developer/Course_Academy/.venv/bin/python -B post.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B reproduce_batch_shortcut.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine delivered-grader-input.json delivered-grader-report.json
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input target-render-records.json --output target-render
/home/jake/Developer/Course_Academy/.venv/bin/python -B layout_probe.py
python3 -B finalize.py
```

The old-code regression commands and current delivered-batch reproduction intentionally exit 1. Current generator regressions exit 0. `finalize.py` uses system Python's installed jsonschema; the context virtualenv lacks that review-only dependency. The generator itself was tested exclusively with the supplied context Python.

Fresh seeds: 91643..91650 per profile; source replay seed 94739; controlled pairs seed 472; same-bank sign quartets seed 98641; coordinate boundaries seed 79213. Current batch seeds: 1278010737..1278010741, as supplied. The renderer's default limit is six; the remaining two target cases were rendered separately. `provenance.json` records reused parser/regression origins; `layout_probe.py` is reused from the previous independent review and rerun here.
