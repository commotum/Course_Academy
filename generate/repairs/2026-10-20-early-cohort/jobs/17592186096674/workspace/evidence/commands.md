All commands run from the supplied workspace. No publication, service calls or database writes were performed. Python bytecode writes were disabled. Reports and assets are under this workspace.

Reproduction before changes (exit 1, three KeyErrors):

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python -B ../review-0-policy-2-c7b8a9fa63291d09/reproduce_missing.py --workspace . > evidence/latest-failure-before.json
```

Reproduction after changes and retained executable regression (exit 0):

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/reproduce_missing.py --workspace . > evidence/latest-failure-after.json
/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/source_regression.py
```

Source replay: 15 cases, 14 complete practice banks, 70 matched choices. Captured source solution stages match; q-20589's missing key/solution are explicitly inferred. q-131590's earlier key correction remains in place. The canonical example has no invented bank and is excluded from sampling.

Affected validation, native grader and delivery (all exit 0):

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/validate_repair.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/grader-input.json evidence/grader-results.json
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/delivery-input.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/validate_repair.py --after
```

54 records independently parsed and solved using Fraction arithmetic; each displayed row-operation matrix checked. Native grading: 53 correct choices accepted, 212 distractors rejected. Delivery: 39 input / 39 accepted / 0 duplicates. Controlled subset: five candidate roles and four elimination masks within each of five profiles, preserved after filtering. Constant-position, extrema and coordinate-frequency strategies all have counterexamples within each controlled profile. Relevant/irrelevant counterfactuals cover restored matrix/text profiles and existing vector shape. Five fresh seeded records and package-only relocation match exactly.

Actual UI rendering and ordering (all exit 0):

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math --limit 6
/home/jake/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node checks/ui_order.cjs
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/render-delivered-records.json --output evidence/render-delivered --asset-root evidence/delivery/assets --math-root /media/jake/SSD/EDB/math --limit 2
/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/finalize_evidence.py
```

Eight screenshots inspected: restored source matrix/text, fieldless canonical, matrix/text counterfactuals, delivered text/vector. All renderer reports pass. Exact learning.js ordering matches five rendered DOM fixtures and does not assign a constant correct position within either restored profile. Production allocation IDs and live learner history are unavailable.

Inventory: 19 captured records inspected for source identities and generation attribution. The demonstrated replay-registry omission is not an existing-instance construction failure. affected-inventory.json is empty for this specific finding. Five non-source records lack generation metadata; their provenance and seeds cannot be reconstructed. This is not a broad assertion of correctness for untested stored items.

Prior review's selection-branch analysis retained after confirming the question_selection.rs hash is unchanged and inspecting the relevant branches; its current delivery count was updated. No live selection claim is made. Prior twelve runtime profile objects compare equal to the review's relocated original package. Python 3.13.5 and SymPy 1.14.0 match the unchanged manifest and pinned requirements. jsonschema is unavailable; evidence sections and referenced files were checked, without adding a runtime dependency.
