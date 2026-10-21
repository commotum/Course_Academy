Run from the workspace. All outputs stay in the workspace; no database writes or publication.

```sh
CA_REPO=/home/jake/Developer/Course_Academy
CA_PY="$CA_REPO/.venv/bin/python"
"$CA_PY" repair_validate.py
"$CA_REPO/generate/runs/current/check-engine" evidence/repair/grader-input.json evidence/repair/grader-report.json
"$CA_REPO/generate/runs/current/check-engine" evidence/repair/grader-diagnostic-input.json evidence/repair/grader-diagnostic-report.json
"$CA_PY" "$CA_REPO/generate/pipeline/check_delivery.py" --input evidence/repair/records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/repair/delivery --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
"$CA_PY" repair_validate.py --final
python3 "$CA_REPO/generate/pipeline/render_preview.py" --input evidence/repair/render-records.json --output evidence/repair/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math --limit 5
"$CA_PY" relocation_check.py
"$CA_PY" "$CA_REPO/generate/pipeline/check_delivery.py" --input evidence/final-five.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/repair/final-five-delivery --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
```

The required expected-accept check is intentionally preserved as a **failure**:

```sh
"$CA_REPO/generate/runs/current/check-engine" evidence/repair/required-grader-input.json evidence/repair/required-grader-report.json
```

Exit code 1: expected accepted, got unresolved (answer comparison has unresolved domain differences). `repair_validate.py` also runs this command and saves its exit code and console without changing its expected outcome. Diagnostic unresolved outcomes are a separate investigation, not a waiver of the acceptance check.

Results: all 17 source replays and 43 valid bank values remain unchanged. The complete affected domain has 36 mathematical tasks, including both targets for each n=2..4 and h=0..5. Native repair/regression batch: 215 accepted, 145 rejected, no unresolved. The separate required log-equivalent acceptance fails. Delivery: 44/44 records retained, all 36 affected tasks and both zero-shift targets preserved. Prior radio-bank shortcut assertions rerun on retained delivered evidence; bank code did not change. Five actual UI screenshots passed and were visually inspected. Relocated CLI output is deterministic; its five records all pass delivery.

Overall status: unsupported because the required native-grader behavior needs an engine fix outside this workspace. Completed generator repairs are retained.
