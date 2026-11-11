# Generator incident recovery — 2026-11-11

The original `summary.json` and `quota-affected-jobs.json` document the read-only
incident investigation. They remain unchanged historical evidence.

The user subsequently authorized cleanup so the detached generator can resume.
Generation remained stopped throughout this recovery. No model turn, database
transaction, approval, question publication, or lesson-content edit was run.

## Initial quota batch

`recovery/plan.json` binds 2,640 current blocked jobs to their exact failed
executions and event logs. The terminal quota events support **7,915 replacement
launch credits**: 2,635 executions receive three credits and five receive two.
Total recorded launches remain unchanged. The five earlier non-quota launches
remain charged; all author, source-account, review, correction, and content
failure counters remain unchanged.

The exact original bytes of all 7,920 changed files are retained in
`recovery/backups.tar.gz`. The plan contains original and resulting SHA-256
hashes, field-level patches, and event-log hashes. `applied.json` records
completion; `verification.json` records the check performed while the inventory
lock was held.

The first apply completed 737 jobs, then stopped safely when the UI inventory
refresh acquired its lock. The UI subsequently refreshed their ranking and
marked the saved unfinished cycles `running`, its label for resumable work.
That did not start workers. Recovery resumed idempotently, preserving those
ranking updates and every applied credit, then completed the other 1,903 jobs.
The tool now holds the inventory lock throughout apply and verification.

## Supplemental infrastructure batch

The independent inventory audit found another 14 recoverable infrastructure
holds. `supplemental-recovery/plan.json`, `backups.tar.gz`, `dry-run.json`,
`applied.json`, and `verification.json` document their separate recovery:

| Cause | Jobs | Restored agent launch capacity |
| --- | ---: | ---: |
| Additional quota failures | 8 | 16 |
| Invalid structured-output schema, now fixed | 3 | 6 |
| Provider model capacity rejection | 1 | 3 |
| Stale database preparation | 1 | 0 |
| Runtime asset handling, now fixed | 1 | 0 |

The same evidence supports 35 root process-failure credits: 16 quota, six
schema, nine UUID serialization failures, and four stale database preparations.
The UUID and schema implementation defects were repaired before applying this
batch. One genuine 3,600-second author timeout remains charged.

Provider failures sometimes occurred after useful work. All saved work remains;
these credits describe the terminal infrastructure failure, not zero-cost turns.
No saved review is automatically accepted by this recovery. Normal policy,
source, package, grading, and all-band checks still apply on resume.

The runtime-asset job resumes with its existing final author attempt: attempt 2
of limit 3 and its recorded no-progress counter of 1 are unchanged. It is not
approved or published.

## Recovery mechanism

`scripts/generator_quota_recovery.py` builds evidence-bound plans and backups,
then applies them with supervisor, inventory, KP, and pipeline locks. It checks
every file and event hash before a job's writes. Exact after-images allow safe
resumption after interruption. A narrowly recognized inventory ranking refresh
is preserved; changes to cycles, attempts, outcomes, job inputs, or recovery
markers still reject the apply. Seven regression tests exercise these rules.

`prepare_supplemental.py` is the one-time audited recipe for the 14 additional
jobs. It validates exact terminal provider errors, the final process-error
sequence, and the remaining asset-author allowance before preparing any patch.

The final resume-readiness audit lives alongside this folder at
`../2026-11-11-generator-resume-readiness/`. It separately checks operational
state and any pre-existing interrupted-attempt issues discovered during recovery.

The independent check found one interrupted third author attempt whose
`author_running` marker had been cleared by an earlier phase migration. The
migration now preserves that marker. The separate
`../2026-11-11-generator-resume-readiness/author-continuity-repair/receipt.json`
records restoration of the marker from the saved pre-migration evidence. Attempt
3 and its limit of 3 remain unchanged; no fourth attempt or approval was granted.
This audited follow-up is the only subsequent exception to the main batch's
exact pipeline after-images.
