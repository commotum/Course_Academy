# Third targeted repair: commands and results

Run from this workspace. `py=/home/jake/Developer/Course_Academy/.venv/bin/python`, `repo=/home/jake/Developer/Course_Academy`; set `PYTHONDONTWRITEBYTECODE=1` if desired. Every write is confined to this workspace; tools are offline. No engine, database, publication or image content changed.

```bash
/home/jake/Developer/Course_Academy/.venv/bin/python ../review-2-policy-2-0c1c91bdcd7c4ff5/test_batch_shortcut.py
```

Exact latest failure reproduced before editing: exit 1, 5/5 heuristic successes, captured in `../batch-shortcut-before.json` relative to this evidence directory. The reviewed seed was 4251183390. The old first-record sign control is regenerated from exact matrix parameters rather than editing a record's key.

```bash
/home/jake/Developer/Course_Academy/.venv/bin/python checks/validate.py
/home/jake/Developer/Course_Academy/.venv/bin/python checks/single_witness.py
/home/jake/Developer/Course_Academy/.venv/bin/python checks/batch_shortcut.py
/home/jake/Developer/Course_Academy/.venv/bin/python checks/package_check.py
```

All pass. Both history finding IDs and the initial packaging event have executable regressions in `repair-regressions.json`. `batch_shortcut.py` executes six real easy count=5 CLI batches, one shared delivery invocation and one native-grader invocation; its input/output reports and complete records are in this directory. Seeds: 4251183390, 0, 19, 71, 991, 20261022. Exact reviewed heuristic scores after filtering: 1/5, 1/5, 1/5, 3/5, 2/5, 2/5. Every permitted single-cue and joint size/sign/letter lookup has a conflicting classification. Every size with both orientations has a joint sign/letter collision, varying correct positions and both successes and failures for choosing the first orientation choice. All 30 survive delivery, with identical visible matrices, classifications and cue reports. Native grader: 45 accepted, 153 rejected, zero unresolved, 0 database writes across 33 records/198 responses. This includes all five choices plus the exact heuristic submission per record; the sign-only -9 to 9 change keeps Upper accepted while heuristic Lower is rejected. Transposing the off-diagonal evidence with the same diagonal yields Lower, independently verified in visible prompt and solution.

Retained checks: 11/11 complete source banks, 55/55 choices, original raw difficulty/key/solution presence, 11 normal parameter replays; the canonical sole-witness case and all nonempty supports remain accepted. Easy retains all 18 structural tasks (2x2=3, 3x3=15), moderate 15, authored hard 127. Full easy exhaustion and exclusion-of-13-leaves-five checks pass. Finite tasks and source-supported sparse cases have not been removed.

```bash
/home/jake/Developer/Course_Academy/.venv/bin/python checks/prepare_targeted.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/grader-all-input.json evidence/grader-report.json
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/delivery-input.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery --asset-root evidence --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/samples.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/sample-delivery --asset-root evidence --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/single-witness-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/sparse-delivery --asset-root evidence --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python checks/delivery_probe.py
/home/jake/Developer/Course_Academy/.venv/bin/python checks/targeted_delivery.py
```

Retained native regression: 60 accepted/240 rejected. Delivery retains 42/42 audit, 5/5 seed-0 sample, 10/10 sparse controls. Post-filter independent math and density/first-cell/label/position checks pass. The read-only within-band learner-selection probe sees all three classifications under both surrogate orderings. Real numeric entity order, policy, learner history and current prefix remain unavailable; offline delivery is not a guarantee about a future history-filtered learner subset.

```bash
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/batch-repair/render-input.json --output evidence/batch-repair/render --asset-root evidence/batch-repair/delivery/assets --math-root /media/jake/SSD/EDB/math
```

Actual UI: 3/3 passed and all screenshots visually inspected. Lower, sparse Upper, Diagonal each share negative top-left values and letter C. All matrices, radio labels and solutions are readable; witnesses c31=-10 and c23=2 agree with their matrices. See `render-inspection.json` and `render/rendering.json`.

Relocation from the exact three manifest runtime files passes and reproduces the deterministic five-record batch. Installed Python 3.13.5 and SymPy 1.14.0 match manifest/requirements. No new dependency.

Fidelity, mathematical correctness, native grading and the named decision-variation probes are separate passing claims; none establishes absence of every imaginable shortcut. The new batch rule changes joint sampling by conditioning on counterexamples, not the valid parameter domain. Explicit single-family requests and forced finite remainders may lack cross-family contrasts and retain all eligible structures; they are not claimed to provide classification diversity. Requested normal five-question easy batches are covered by the strict regression.

Inventory: all 16 supplied matrices inspected. No generated batch metadata is present, so historical batch associations cannot be reconstructed. `affected-inventory.json` stays empty because no affected stored generated cohort was demonstrated; this is an untestable cohort attribution, not a verified absence of the batch defect. One original source has no key, remains evidence-only on raw replay, and was not marked generated.
