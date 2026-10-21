Run from this evidence directory; all outputs remain here. Context Python is /home/jake/Developer/Course_Academy/.venv/bin/python.

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python review_checks.py
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input easy-samples.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-sample --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-report.json
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-input.json --output render --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-counterfactual-input.json --output render-counterfactual --limit 7 --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python followup_checks.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-delivery-input.json grader-delivery-report.json
/home/jake/Developer/Course_Academy/.venv/bin/python acceptance_regressions.py
/home/jake/Developer/Course_Academy/.venv/bin/python finish_report.py
```

acceptance_regressions.py intentionally exits 1 on the current demonstrated defects. Other scripts save measurements; exit zero alone does not certify acceptance. See result.json for the independent verdict. Source analysis was saved before package inspection. No repair history, preflight or prior review file was present.
