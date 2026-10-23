# Targeted second repair

All commands run in the workspace. Python: `/home/jake/Developer/Course_Academy/.venv/bin/python`.

Before implementation, copied the unchanged reviewer reproducer into this evidence directory to keep all writes in scope:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python evidence/repair-2/before/reproduce-batch-shortcut.py ../review-1-policy-2-33f27ec8b7c41b11/delivery-batch/accepted.json
```

Exit 1, second-largest cue correct on 2/2. Complete records/results in `before/`. Retained first-repair regression passed before changes (`before/retained-check.log`).

After repair:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python check_batch_selection.py
/home/jake/Developer/Course_Academy/.venv/bin/python validate_batch_repair.py
/home/jake/Developer/Course_Academy/.venv/bin/python check_repair.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/repair-2/native-input.json evidence/repair-2/native-results.json
/home/jake/Developer/Course_Academy/.venv/bin/python evidence/repair-2/after/reproduce-batch-shortcut.py evidence/repair-2/delivery-exact/accepted.json
python3 /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/repair-2/render-input.json --output evidence/repair-2/render --asset-root evidence/repair-2 --math-root /media/jake/SSD/EDB/math
```

All exit 0. `check_batch_selection.py` invokes the shared delivery filter; exact commands and stdout/stderr are in `exact-delivery-command.json`, `easy-delivery-command.json`, and `moderate-delivery-command.json`. Its current output preserves all five original template/parameter selections while changing the second q-73544 bank's rank from 4 to 5. Effective generation seeds preserve exact per-record replay. `after/batch-shortcut-results.json` reports 1/2 successes rather than 2/2. No source-supported task was removed to pass this check.

Checks and scope:

- Fidelity: all ten source prompts, solutions, full banks and keys replay (`source-replay.json`).
- Correctness: exact arithmetic and visible row-operation witnesses pass for 47 records, including source replays and controlled relevant-constant changes (`validation-summary.json`).
- Grading: 48 expected acceptances and 192 expected rejections through the native grader; includes an irrelevant choice-order reversal.
- Decision variation: exact batch 5/5, small easy sample 15/15 and moderate sample 15/15 survive actual delivery. Every repeated visible coefficient/endpoint group varies rank and authored position, before and after filtering (`batch-results.json`). These samples cover nine profiles in aggregate; the unchanged direct bank regression still tests rank/position variation in all ten profiles (`retained-check.log`). This is a focused repair, not a new exhaustive sampler audit.
- Packaging: exact installed dependencies, relocation and deterministic batch replay pass (`packaging.json`).
- Rendering: both exact q-73544 records rendered and screenshots visually inspected (`render/rendering.json`, `visual-inspection.json`).

Historical evidence remains in `evidence/`. Its old delivered batch is superseded by this repair's `delivery-exact/accepted.json`. The previous validation script now obtains the current batch through `batch()` and retains its mathematical task comparison; it no longer assumes each effective bank seed equals the batch seed. The focused replacement validation above was run; the old broad validation was not repeated.

Captured inventory basis 5576 still consists solely of the ten original source questions; prior verified evidence is `../validation/inventory-review.json`. `affected-inventory.json` remains empty. No images published, database mutations, live services, or outside-workspace writes. Offline delivery cannot guarantee which subset a future live learner-history/reservation filter selects. The new batch rule does not claim that every arbitrary subset has contrasting roles.
