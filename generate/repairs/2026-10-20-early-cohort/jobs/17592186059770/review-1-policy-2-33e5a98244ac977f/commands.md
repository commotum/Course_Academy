All commands run from this evidence directory, with PYTHONDONTWRITEBYTECODE=1. The reviewed package is never an output destination.

Rebuild independent source replay, samples, math, grading and packaging evidence:

    /home/jake/Developer/Course_Academy/.venv/bin/python audit.py

Read-only delivery checks (INPUT is sample.json or batch.json, OUTPUT is delivery-sample or delivery-batch):

    /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input INPUT --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output OUTPUT --math-root /media/jake/SSD/EDB/math

Independent shortcut/selection and prior-inventory reproduction:

    /home/jake/Developer/Course_Academy/.venv/bin/python probes.py
    /home/jake/Developer/Course_Academy/.venv/bin/python inventory_audit.py
    /home/jake/Developer/Course_Academy/.venv/bin/python milestone_checks.py

Strict failing regression (exit1 on reviewed batch, expected to be adopted by repair):

    /home/jake/Developer/Course_Academy/.venv/bin/python reproduce_shortcut.py delivery-batch/accepted.json

Actual native learner grading of the equation-blind action:

    /home/jake/Developer/Course_Academy/generate/runs/current/check-engine shortcut-native-input.json shortcut-native-report.json

Actual UI render invocations:

    /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render-all --limit 10 --math-root /media/jake/SSD/EDB/math
    /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input extra-render-records.json --output render-extra --limit 5 --math-root /media/jake/SSD/EDB/math
    /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input irrelevant-render-records.json --output render-irrelevant --limit 2 --math-root /media/jake/SSD/EDB/math

The first render attempt used default limit6; render-all supersedes its coverage. Scripts and screenshots remain in this directory. Original history had no retained finding entries and no preflight file; author feedback_regression.py was inspected but not executed because it writes into the package. audit.py independently reproduces the actual legacy easy CLI failure and tests the current CLI. No supplied validation report was treated as acceptance evidence. Legacy reference records were treated as claims until inventory_audit.py exactly reproduced each entire record and matched captured bank entities.
