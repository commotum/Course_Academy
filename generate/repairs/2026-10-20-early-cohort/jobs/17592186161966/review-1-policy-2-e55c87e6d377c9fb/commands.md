All commands run from evidence_root. Package imports use PYTHONDONTWRITEBYTECODE=1. All authored outputs are below evidence_root.

```bash
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python review.py
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python revision_checks.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-report.json
```

For both `samples.json` and the job's exact `samples.json`, ran `/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py` with `--source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --asset-root ../workspace --math-root /media/jake/SSD/EDB/math`; outputs `delivery-samples` and `delivery-batch`. Complete resolved input paths/hashes are in those delivery.json files.

```bash
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python delivery_review.py
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-input.json --output render --limit 8 --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python render_scroll.py --input scroll-input.json --output render-scroll --asset-root ../workspace
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python finalize_review.py
```

Fresh seeds: 943000 + 100*profile_index + i, i=0..4. Fixed-bank role seeds: 955300 + profile_index, answer_role=0..4. Explicit counterfactual parameters are in review.py and complete generated records in counterfactuals.json. Prior minimal counterexample seed 1118318699 and twelve old regression seeds are retained in reproduce.py and regression-current/regressions.py. Retained-check ROOT/OUT redirects are in revision_checks.py; assertion logic is unchanged.
