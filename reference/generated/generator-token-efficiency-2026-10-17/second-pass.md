# Second efficiency pass

Inspected the nine latest local author/reviewer event logs and the worker retry,
source capture, publication and validation paths. No live database scan was run.

Implemented:

- Persisted a maximum of three launches per unfinished Codex session. Timeouts,
  nonzero exits and interrupted sessions cannot restart indefinitely. Completed
  structured results still bypass launches. Exhaustion retains the workspace,
  evidence and original stage for deliberate recovery.
- Extracted publication record preparation into one shared function. The offline
  `generate/pipeline/check_delivery.py` uses it for KP validation, localization,
  question validation, stable identities and deduplication against saved inventory.
  It enforces the requested difficulty and writes images only to evidence. Both
  agent prompts now point to this tool and concise grader/renderer interfaces.
- Reused publication's fresh, pinned KP read for its source check, eliminating
  the second KP pull and status call at the same basis. The full source comparison
  still runs, including lesson, prerequisite and image evidence.

Verification: 35 pipeline, 24 publication, 5 delivery-helper, 9 review-contract,
and 45 inventory-worker tests passed (118 total). A five-question saved real batch
for KP 17592186176090 at inventory basis 3597 produced records identical to its
verified publication through the new helper. No publication was performed in
that smoke check. Syntax and targeted whitespace checks passed.

All eight independent review checks remain required; review policy remains 2.
Generator rejection, learner selection and pedagogical analysis remain explicit
responsibilities outside the delivery helper. No service restart or interruption
was performed. Running Python processes retain already imported code; subsequent
pipeline processes load the changes, and prompts/helpers load on their next use.

No dedicated retry CLI exists for terminal jobs. Recovery after correcting an
infrastructure problem must deliberately reset/requeue the saved session under
the existing worker locks; ordinary ranking updates do not reset its budget.
