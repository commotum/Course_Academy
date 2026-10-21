# Reproduce from the workspace

```sh
CA_REPO=/home/jake/Developer/Course_Academy
CA_PY="$CA_REPO/.venv/bin/python"
"$CA_PY" validate.py
"$CA_REPO/generate/runs/current/check-engine" evidence/grader-input.json evidence/grader-report.json
"$CA_PY" "$CA_REPO/generate/pipeline/check_delivery.py" --input evidence/records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
"$CA_PY" validate.py --final
python3 "$CA_REPO/generate/pipeline/render_preview.py" --input evidence/render-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math --limit 18
python3 "$CA_REPO/generate/pipeline/render_preview.py" --input evidence/render-extra-records.json --output evidence/render-extra --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math --limit 3
"$CA_PY" relocation_check.py
"$CA_PY" "$CA_REPO/generate/pipeline/check_delivery.py" --input evidence/final-five.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/final-five-delivery --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
```

`validate.py` reconstructs source banks, independent manual derivative oracles, exact symbolic checks, known-term prompt checks, counterfactuals, parameter endpoints, native-grader cases, and render inputs. `--final` compares coverage, shortcut probes and mathematical content before/after the actual shared delivery filter. No publication or database writes occur.

Native limits: the native checker cannot certify negative-power and fraction forms equivalent on the explicitly positive domain; 30 such oracle comparisons are deliberately recorded as unresolved. Radio selection of these source questions still grades correctly. During development, expanding a log constant (ln(4) to 2ln(2)) also produced an unresolved native equivalence result. This is a platform comparison limitation, not a mathematical inequivalence. Tests use supported canonical and canceling-scalar equivalent forms, and retain the source aliases.

The renderer saved all 21 full-page screenshots. The author inspected the first 18 through the five contact sheets and inspected the three extra screenshots individually. See visual-inspection.json. The screenshot report by itself was not treated as visual approval.
