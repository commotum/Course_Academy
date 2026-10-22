# Targeted validation result

The latest failure was reproduced before retained validation, using
`/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/batch_regressions.py --finding inventory`.
It exits 1 for all five historical records and the retained 64/64 possible-history
shortcut witness. The same counterexample is captured first in commands.json.

The current generator's four retained findings pass. Source replay, delivery,
native grading and relocation were rerun by checks/recheck_status.py; results.json
and commands.json contain the exact commands and outcomes. Existing replacement
records and their mappings match the current package and captured inputs. The
retained UI screenshot was visually reinspected; rendering was not repeated.

No implementation change is warranted by this feedback: it requests a separate
inventory-remediation workflow for stored v2 records. The selector reads stored
question content without invoking this generator. Changing the current generator
or its sampling cannot repair those records. Applying the staged proposal would
require the prohibited database/publication action. The strict test is retained
and still fails; the proposed replacement pool is not substituted for inventory.

Status: unsupported until separate remediation and fresh inventory capture.
Completed repairs remain intact. No runtime, source, inventory, engine, database,
published asset, or other-job content was edited.
