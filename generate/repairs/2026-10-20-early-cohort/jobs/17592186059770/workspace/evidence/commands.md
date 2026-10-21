Run from the supplied workspace. All outputs are local; none contacts a service or database.

```bash
CA_PY=/home/jake/Developer/Course_Academy/.venv/bin/python
CA_REPO=/home/jake/Developer/Course_Academy
"$CA_PY" checks/feedback_regression.py
"$CA_PY" checks/validate.py
"$CA_PY" checks/decision_roles.py
"$CA_PY" checks/retrospective.py
"$CA_PY" "$CA_REPO/generate/pipeline/check_delivery.py" --input evidence/sample-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-easy --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
"$CA_PY" "$CA_REPO/generate/pipeline/check_delivery.py" --input evidence/moderate-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output evidence/delivery-moderate --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
"$CA_PY" "$CA_REPO/generate/pipeline/check_delivery.py" --input evidence/role-records-easy.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/role-delivery-easy --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
"$CA_PY" "$CA_REPO/generate/pipeline/check_delivery.py" --input evidence/role-records-moderate.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output evidence/role-delivery-moderate --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
"$CA_PY" checks/after_delivery.py
"$CA_PY" "$CA_REPO/generate/pipeline/check_delivery.py" --input evidence/learner-request.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/requested-delivery --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
"$CA_PY" "$CA_REPO/generate/pipeline/render_preview.py" --input evidence/render-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
```

`checks/validate.py` batches the native grader into evidence/native-input.json; `decision_roles.py` uses evidence/role-native-input.json; `after_delivery.py` uses evidence/requested-native-input.json. Each invokes `$CA_REPO/generate/runs/current/check-engine INPUT REPORT` once, not once per response. Final reports record 875, 410 and 25 checks respectively: 262 accepted choices, 1,048 rejected choices, zero unresolved, zero DB writes. The manifest regression invokes the feedback check and role counterfactuals; running the commands separately may repeat those same checks.

The original failure is retained as evidence/original-failure.stderr. History has an empty findings array, so the only identifier available for the retained runtime failure is its history event reason code `legacy_packaging_or_sampling`; that exact code is used in repair-regressions.json. No earlier finding IDs were dropped.

The initial source replay detected an incorrectly simplified q-71731 transposed distractor. The complete source bank includes reversal of off-diagonal signs before transposition; the corrected recipe now matches all five source choices. Author probes also exposed fixed-row and bank-minority cues; eligible correct-role selection, rather than another isolated numerical patch, repaired them. See instructional-account.md and evidence/decision-roles.json.

Historical inventory reproduction uses the retained unchanged legacy entrypoint copied into evidence/legacy/ plus the original provenance data, and exact historical seeds/templates. Full commands are in retrospective-commands.json; generated-records.json exactly matches the five archived generated records, including UUIDs, answer order and generation metadata. The supplied external legacy entrypoint is read only. No source question is marked generated. In affected-inventory.json the evidence path `../workspace/evidence/generated-records.json` is relative to the supplied `author-1` evidence_root, because all authored files must remain in the workspace.
