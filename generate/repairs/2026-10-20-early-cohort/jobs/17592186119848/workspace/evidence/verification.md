# Final verification

All commands used `/home/jake/Developer/Course_Academy/.venv/bin/python` (3.13.5).
The runtime dependency is SymPy 1.14.0. Permanent changes are confined to this
workspace. No database writes, service calls or image publication occurred.

```sh
python checks/check_runtime.py
python checks/validate_content.py
python checks/check_delivery_variation.py
python checks/audit_inventory.py
python 17592186119848.py --difficulty easy --count 5 --seed 119848 --format json > evidence/sample.json
python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --math-root /media/jake/SSD/EDB/math
```

- Relocation: only manifest files copied into an isolated temporary directory;
  five records generated twice, byte-identically, with no unresolved imports.
- Fidelity: 10/10 complete source questions, 15/15 field banks, 54/54 choices;
  source checkbox layout/None retained. Two incomplete originals are excluded.
- Correctness: all 39 generated presentations independently parsed and ranked;
  15 controlled qualifying-subset changes reject stale keys and solutions.
  Four scale controls preserve responses and require fresh visible-content IDs.
- Grading: native learner engine accepted 76 correct choices and rejected 211
  wrong choices; no unresolved outcomes. The full input is grader-input.json.
- Variation: 24 semantic structural classes; scalar changes and label permutations
  do not add capacity. All 39 presentations survive actual delivery against the
  supplied inventory. Twelve conditional profile/layout/dimension/bank groups
  retain multiple responses and positions, with no always-selected label.
- Inventory: all 12 stored IDs are original source items; no stored generated
  instances. Ten complete items independently checked; two cannot be graded
  from supplied evidence. affected-inventory.json is empty with this scope.
- Rendering: four final previews in render/ use the unmodified application UI.
  All were visually inspected. Subset matrices now wrap without clipping;
  the other three final screenshots match the previously inspected image hashes.

Before-repair reproductions are packaging-before.json,
delivery-shortcut-before-repair.json, conditional-shortcut-before-repair.json,
and checkbox-identity-before-repair.json. Runtime, bank, filtering and rendering
repairs are described in instructional-account.md. The old validator is retained
as legacy-validate.py; the original validator entrypoint now runs the current check.

`repair-regressions.json` identifies the sole retained history event using its
code, legacy_packaging_or_sampling; the supplied history has no named finding IDs.
All other discovered defects have executable coverage in the content/delivery
checks. No grading criteria were weakened. Easy is supported; other bands,
unlimited replenishment and live learner-selection behavior are not claimed.
