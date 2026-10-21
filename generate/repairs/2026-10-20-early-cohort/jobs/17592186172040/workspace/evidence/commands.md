Run from this workspace with the job interpreter. No commands publish images or write database content.

Before edits, both exact retained failures were reproduced by a relocated package with an empty plot directory and the undeclared Python 3.10 executable hidden, and by generate('easy', seed=991, profile='e-8507'). Exact sandbox command/error: before/cold-result.json. Canonical error: before/canonical-result.json.

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python checks/cold_dependency_probe.py
/home/jake/Developer/Course_Academy/.venv/bin/python checks/canonical_replay_probe.py
/home/jake/Developer/Course_Academy/.venv/bin/python checks/validate_repair.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/grader-input.json evidence/grader-report.json
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/moderate-probes.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output evidence/delivery --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python checks/check_variation.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/delivery-grader-input.json evidence/delivery-grader-report.json
```

Both retained regressions were rerun after the final runtime edit and passed. The cold test hides both the original Python 3.10 and the uv archive, disables networking, makes the relocated package read-only, and allows persistent writes only to the explicit output directory. It tests moderate seed 801239 plus a changed empirical source-bank rendering. Package hashes remain unchanged by generation. Canonical replay compares the exact supplied source prompt/solution and independently measures slope variation in each visible panel; only III varies in both directions.

Source replay: all 8 five-option banks match (40/40 options); seven have original designations/solutions and match exactly. The eighth remains explicitly distinguished as authored completion of incomplete evidence. Canonical replay retains all four source panels, with its missing captured answer field supplied by a documented radio adapter.

Independent sample: 12 authored records, controlled relevant/irrelevant pairs, five default moderate records (seed 801239 and next four), explicit invalid-input guards and deterministic replay. The powered-factor prompt parser required a validation-only implicit-multiplication correction; the generator's supported scope was not reduced.

Native grader: 39 accepted, 155 rejected, zero unresolved before delivery; 14 accepted, 56 rejected, zero unresolved after delivery. All 14 moderate probe records passed the shared delivery filter, including all five requested batch records. Cue results are in shortcut-results.json: each moderate template has more than one correct display position both before and after delivery. Controlled sign changes update equation/key/solution/guide; an unused single-field slot preserves the complete question. The hard x/y-direction pair holds four background fields fixed and changes the outlier/key/guide. Fifteen actual PNG fields pass independent angular checks; three unmodified-UI screenshots pass DOM checks and were visually inspected.

Inventory basis 5386 contains eight original sources, without generated metadata. No affected stored generated instance was demonstrated; affected-inventory.json is empty for that verified reason. Live inventory and learner history/policy weights are unavailable. The source canonical lacks captured answer fields/difficulty; the four-label adapter and easy assignment are authored and explicit. Unknown empirical distractor formulas remain unresolved as before; byte-exact source replay and the existing measured-geometry reconstruction are retained.
