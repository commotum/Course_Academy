Run from this evidence directory. All audit inputs and outputs are retained here. The package is read-only; `-B` prevents bytecode writes. No command publishes or connects to EDB.

```bash
/home/jake/Developer/Course_Academy/.venv/bin/python -B audit.py
```

This saves exact source replays, independent role and fresh-seed samples, counterfactuals, native grading inputs, relocation records, runtime versions and package hashes. Seeds 683021..683276 per difficulty, profile seed 92317, boundary seed 91377, counterfactual seed 91379, source replay seed 78419. Full parameters and complete records are retained. Split the independent samples by the recorded question difficulty into samples-easy.json and samples-moderate.json (the existing files retain the exact split).

```bash
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input samples-easy.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-easy --asset-root .
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input samples-moderate.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output delivery-moderate --asset-root .
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input runner-batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --asset-root .
/home/jake/Developer/Course_Academy/.venv/bin/python -B postprocess.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-all-input.json grader-all-report.json
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render-all --asset-root . --limit 9
/home/jake/Developer/Course_Academy/.venv/bin/python -B resampling.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B finalize.py
python3 validate_contract.py
```

Inspect render-all/question-001.png through question-009.png. They show all six controlled pair records, cancellation, the source all-selected bank, and a runner record. Initial rendering used the renderer's default six-case limit; render-all explicitly renders all nine. All nine records were visually inspected.

Author instructional-account.md, evidence/validation.json, source-fidelity.json and pedagogical-variation.json were consulted only after source-analysis.json was written and verified. Their claims were treated as claims; independent scripts above provide the acceptance evidence.

Retrospective inventory: all 12 captured entries match original source question IDs, with no generation metadata. Their complete source banks and solutions are replayed and checked. affected-inventory.json has no demonstrated generated defects; this is an inspected captured pool, not a claim about later inventory. No original source was marked generated.

One audit command initially used system python3 for a candidate import and failed because SymPy is absent there. It was rerun successfully as resampling.py using the supplied virtualenv. This is not a package runtime failure: the manifest's exact dependency versions were verified with the required interpreter.

Selection limits and tested scenarios are in selection-results.json. Production weights/history/entity IDs are absent from the captured inputs; explicit scenario reproduction is used, not a claim that live selections were observed. Unconfigured lowest-ID fallback and exhausted easy pools are retained as explicit cases.
