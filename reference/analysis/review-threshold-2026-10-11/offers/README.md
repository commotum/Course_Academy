# First observed review offers

This audit re-reads saved queue and progress evidence, limited to the four frozen activity manifests in `reference/mathacademy/encompassing-analysis-2026-10-11`. It does not change the database, engine, capture state, or existing encompassing analysis.

Run from the repository root:

```bash
PYTHONPATH=capture python3 reference/analysis/review-threshold-2026-10-11/offers/analyze.py
```

`analyze.py` reconstructs the evidence; `finalize.py` adds conservative timing comparisons. The account JSON files contain source paths and original journal line numbers, offer brackets, course-qualified color evidence, prior direct-practice records, and intervening visible changes. `first-review-offers.csv` is the compact export; `summary.json` contains separate account summaries.

## What was counted

| Account | Frozen activities | Saved queue observations | Distinct review offers |
|---|---:|---:|---:|
| Foundations | 1,247 | 1,499 | 677 |
| Linear | 666 | 782 | 364 |
| Multivariable | 593 | 782 | 264 |
| Differential | 527 | 748 | 254 |

Each account/task is counted once, at its first saved offer. Every observed review offer has a preceding captured queue that lacks that task ID. These bracket **observed appearance in the queue**, not an unobserved backend due-time crossing. Repeated sightings do not add observations; repeated tasks on the same topic remain dependent observations.

Legacy queues come from saved `queue_observed` / `queue_observation_corrected` journal entries. Current queues come from the original Learn HTML in post-activity observations, using the dashboard's actual capture timestamp. Only unlocked task cards are parsed; completed-task history is excluded. Missing topic IDs are resolved from the same account/task in the frozen manifest when available.

## Timing and color controls

Elapsed time starts at the last captured passed lesson or review on the same account/topic. Legacy completion anchors are post-activity read start times, so they can lag actual completion slightly. Recovered late anchors are flagged and excluded from the clean timing summaries. A lesson is not automatically treated as first learning: the export includes the ordinal of the previous passed direct activity within captured history.

Pre-offer colors use only observations at or before the offer. Course IDs remain attached; disagreeing known colors across course views are excluded from band-conditioned comparisons. The main timing contrasts require a known band read within one hour. Unknown colors/history remain unknown.

Negative-XP or failed repeats, captured assessment misses since the last passed direct practice, and reviews first seen immediately after assessments with unresolved provenance are separated. The remaining group is labeled **no captured remediation trigger**, not asserted to be proven ordinary spaced review.

Additional comparisons separate the preceding activity into lesson versus review, then exclude every intervening captured assessment, and finally exclude observed upward color crossings between direct practice and the offer. The previous direct activity's own post snapshots are excluded from intervening changes. Multiple course reads can describe one shared change, so source paths are retained and rises are counted by source observation rather than as repetition credits.

## What this can establish

Review offers commonly appear while the target is in band 1, roughly 12–13 hours after its last passed direct practice in each account. Band-2 offers in foundations and linear typically follow longer gaps. These describe the captured offering behavior and support state-dependent scheduling; they are not a recovered numerical memory threshold.

The more conservative band-1 subset excludes every captured intervening assessment and every observed upward color crossing. It separates first captured passed lessons from repeated direct reviews:

| Account | After lesson: median hours (n) | After review: median hours (n) |
|---|---:|---:|
| Foundations | 10.17 (25) | 18.49 (2) |
| Linear | 7.04 (83) | 12.77 (18) |
| Multivariable | 8.77 (101) | 11.45 (22) |
| Differential | 8.66 (73) | 11.56 (15) |

No band-2 records survive every conservative exclusion. The assessment-free filter favors shorter windows, so this table is a sensitivity comparison, not an unbiased interval estimator. Typical appearance brackets in these groups are 3–6 minutes wide.

Colors are ordinal display categories. Flat colors can conceal fractional implicit credit, and visible rises can reflect ability/display updates as well as practice. Excluding visible rises therefore does not establish zero implicit credit. Missing activity before the capture window remains unknown. Higher-band observations are sparse and follow-up is short, so absent high-band offers do not imply permanent exemption from review. Exact threshold selection must combine these offer timings with the separate direct/implicit state reconstruction.

Verification checks all 1,559 offers for unique account/task identities and temporal ordering. Sixteen sampled source records were checked independently against original journal cards or the capture system's HTML queue parser; see `verification.json`.
