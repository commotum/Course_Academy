All commands run from evidence_root. No package, database or published asset mutation. Python -B suppresses bytecode writes.

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python -B audit.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B variation.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B reproduce.py shortcut
/home/jake/Developer/Course_Academy/.venv/bin/python -B reproduce.py source
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-report.json
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine shortcut-grader-input.json shortcut-grader-report.json
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --asset-root . --math-root /media/jake/SSD/EDB/math --limit 14
/home/jake/Developer/Course_Academy/.venv/bin/python -B inspect_render.py
```

Delivery commands use `/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py`, with `--input sample-easy.json --output delivery-sample` and separately `--input batch-records.json --output delivery-batch`; both use `--source ../source/source.json --inventory ../source/inventory.json --difficulty easy --asset-root . --math-root /media/jake/SSD/EDB/math`.

The two reproduce.py invocations are strict acceptance tests and intentionally exit 1 on this package; reproduction-results.json retains commands, stdout and tracebacks. They are not failed audit execution. audit.py generated seed-stratified samples before probes; variation.py analyzes saved records and the read-only selection rules. Three n=5 source failures are retained in source-replay.json. Runtime relocation uses copies under relocated/.
