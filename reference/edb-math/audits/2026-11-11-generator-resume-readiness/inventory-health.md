# Generator resume readiness audit

Read-only snapshot taken on 2026-11-11 before recovery. Generation remained stopped.

The detached generator service was inactive with a successful exit. The study app remained active. No generator pipelines were running; all nine worker/runtime locks were free. The older priority service was linked, not enabled.

Across 9,027 inventory records, there were no running jobs, malformed inspected files, missing attempted current pipelines, unresolved current publication requests, legacy publication requests, or pending parent-completion reports. The cursor was at basis 14220. One old review execution still says running, but its process is gone and its controlled-stop witness exists; it does not hold a lock.

The 2,640 known quota jobs were still blocked at this snapshot. The audit found eight additional overnight quota cases hidden behind the process-failure label and sent their exact evidence to the recovery agent.

Additional infrastructure findings sent to the parent:

- Three reviewer sessions were rejected for an invalid JSON schema: `checks.progression` combined `$ref` and `description`.
- Fresh donor preparation returned raw EDB UUIDs in `reference_candidates`, although its saved JSON was normalized. That caused prompt serialization failures on the first attempt.
- One older session exhausted three launches on model-capacity errors.
- One preparation job consumed two process retries on stale database bases after one genuine author timeout. Recovery should preserve the timeout.

Per-job holds that must not be blindly reset:

- Seven protected imported-question repair blocks concern missing grading keys/solutions or demonstrated choice-bank shortcuts.
- Three review-binding blocks have changed instructional and engine evidence. Their old final receipts do not match the current inputs.
- One author block reports an answer-bank shortcut. Another reports an older runtime-image lookup error; its exact PNG survives, but the package still lacks hard-band support and needs author completion.

See [inventory-health.json](inventory-health.json) for exact job keys, current cycle paths, structured error counts, and binding differences. The parent and recovery agent own subsequent fixes and post-repair verification; this snapshot is not the post-repair count.
