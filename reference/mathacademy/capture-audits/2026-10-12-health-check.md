# Capture runner health check

Checked October 12, 2026, approximately 8:05 PM Pacific. This was a read-only inspection of runner and database state; no runners were stopped and no capture or database content was changed.

## Current operation

| Account | Current course | Answer profile | Observed state |
|---|---|---|---|
| foundations | Mathematical Methods for the Physical Sciences I | capture | Advancing through history review |
| linear | Mathematical Foundations I | fast-strong | Completed one activity and advanced to another |
| multivariable | Mathematical Methods for the Physical Sciences II | capture | Continuing answer capture |
| differential | Mathematics for Machine Learning | capture | Completed history processing and selected subsequent work |

All four supervisors and capture child processes matched their saved process start tokens. None had restarted since the current launch. No current capture blocker, browser failure, solver dependency failure, or import error was present in the checked state. The additional live legacy process is a dashboard, not another capture worker.

Log write age alone does not indicate a stall: PS1 and MF1 had logs over two minutes old while their history checkpoints were updating every few seconds.

The database was reachable at basis 1874, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. A query pinned to that basis found all 207 supported question identities from the newest verified batch, `1f80b696-e883-4013-8725-6edb38278aa6`. Its archived receipt reports a committed transaction. The six latest batches contained 204, 217, 212, 218, 204, and 207 distinct questions.

At the final queue check, three completed activities containing 32 distinct questions were accumulating toward the configured 200-question minimum. They had no errors or previous failed attempts requiring recovery. No active batch pointer or unresolved per-capture database request remained. This queue is expected under the user's batching policy.

Disk space was ample: approximately 680 GiB available on the workspace filesystem and 1.7 TiB on the database filesystem.

## Outstanding capture gaps

Three questions excluded from completed imports were absent from the database at the checked basis:

| Account | Activity | Question | Omission |
|---|---|---|---|
| foundations | `14131041`, Quiz 5 | `q-162827` | Missing verified question identity and complete answer fields |
| linear | `14151668`, Compound Inequalities | `q-186809` | Graphic rendering/image unavailable |
| differential | `14129781`, Truth Sets of Predicates | `q-175392` | Graphic rendering/image unavailable |

These are completed capture omissions, not current runner blockers. They remain unresolved by this health check.

There are 13 additional distinct question/example capture gaps whose identities already exist in the database: 11 PS2 questions omitted for unverified source identity and two Mathematics for Machine Learning examples omitted for unavailable images. Existing records do not establish that those particular captures were fully imported. Two ML lesson definitions were also omitted, and a tutorial has an image extraction error.

Separately, 37 distinct existing questions were protected from source reimport because they have separately attributed agent corrections: 19 PS1, 11 PS2, and seven Mathematics for Machine Learning. All 37 identities were found in the database. These protection omissions should not be treated as lost questions or repaired by overwriting their corrections. Some associated activity wrappers were omitted when the importer could not include the full activity.

## Recent recovered failures

Inspection of the latest 35 completed activities per account found:

- MF1 task `14155407` encountered four MathQuill readback failures while entering a mixed fraction. It subsequently recovered and completed. The activity phase lasted approximately 8.6 minutes.
- PS2 task `14150188` encountered four dropdown click-target failures and subsequently completed.
- PS1 task `14152076` retried one failed topic-page navigation and subsequently completed.
- Intermittent HTTP 502 errors appeared in saved browser events. No 401, 403, or 429 event appeared in that inspected recent sample.

These recovered failures are recurrence risks, not evidence of a present stall. This check did not modify their entry or recovery implementations.

MF1's previously investigated percentage/topic-color oscillation remains unresolved. The other accounts' saved percentage histories did not exhibit comparable jumps in the earlier fleet-wide scan. MF1's unreliable displayed progress does not currently determine the runner's task selection.

## Scope and evidence

The saved-record scan covered approximately 936 completed captures and their shared import outbox, with the newest entries changing during inspection. It checked required capture files, pending account observations, content extraction gaps, omission reasons, active checkpoints, recent error events, process identities, batch state, and live database question presence. A missing `import-status.json` briefly observed for a newly completed activity was consistent with the activity being queued before its first import attempt.

Canonical live records are under `.local/capture/<account>/`; capture and omission evidence is under `reference/mathacademy/capture/<account>/<task>/`; batch receipts and manifests are under `reference/mathacademy/capture-database/`. No tests were run because this inspection made no implementation changes.

## Remediation completed after the health check

The subsequent repair work corrected the local causes and verified replacement imports:

- Normalize harmless prose paragraph boundaries and empty table paragraphs when binding the same live/history question. Mathematical content and typed choices remain checked. This recovered the original 12 identity omissions and two additional occurrences captured while work continued.
- Convert recognized HTML named entities to XML character references in standalone SVG, preserving original SVG source bytes. This restored two ML canonical examples, one tutorial, and their full lesson definitions.
- Bind a failed history solution image to its verified original solution occurrence even when a choice reuses the same storage bytes. Full solution equality, question identity, and raster decoding remain required. This restored both missing solution images.
- Support MathJax's equivalent reordered solid-border CSS declaration, preserving padding and phantom geometry. This restored a newly omitted PS2 example and lesson definition; a clean verified reread retires the corresponding parser failure while retaining its extraction history.
- Remove unsupported TeX-only spacing before MathQuill entry. The original failure was reproduced with Math Academy's public MathQuill version; readback still checks the unchanged mathematical value.
- Select an exposed point on a partially clipped dropdown option without scrolling an open menu or clicking through an overlay. Existing hidden-menu recovery remains bounded.
- Reference existing corrected practice questions and owned canonical examples in complete activities without changing any corrected question facts or learner responses. Twelve previously omitted activity definitions were requeued and verified.
- Show capture gaps independently of preserved corrections, retaining warnings while repaired imports await verification. Mark the MF1 percentage unverified when abrupt percentage switches coincide with widespread topic-color changes. Legitimate prerequisite-color propagation alone is not flagged.
- Retain original progress HTTP bodies and allowlisted headers separately from rendered DOM. Share batch receipt parsing across activity archives to avoid repeatedly parsing identical snapshots.

All **22** queued historical repairs were verified through normal batches. The two relevant completed batches contained **201** and **215** distinct supported questions; no timer or undersized flush was used. The original three absent questions, `q-162827`, `q-175392`, and `q-186809`, were found in a live query pinned to database basis **1915**. All four accounts subsequently reported **zero capture-gap items and activities**, with no unknown import counts.

Original capture evidence was archived under each activity's `repairs/source-health-*/originals/` or `repairs/protected-activity-reference-v1/`. No Math Academy activities were replayed. Account XP, completion, exposure, and answer-profile ledgers were preserved. All four workers resumed; MF1 remains `fast-strong`, and the others remain `capture`.

The full regression suite passed **625 tests**, and the final dashboard/receipt-cache regression run passed **39 tests**. These runs overlap and should not be summed. Relevant native previews, committed receipts, and per-activity readbacks passed before the repair results were marked verified.

The remaining external issue is the unexplained MF1 progress oscillation on Math Academy. The viewer flags that uncertainty and does not attribute the large changes to individual lessons. A [support report](/home/jake/Developer/Course_Academy/reference/mathacademy/capture-audits/2026-10-12-mf1-progress-report.md) is prepared but has not been sent. Resolving Math Academy's internal progress-state discrepancy requires their investigation; this repair did not reset the account or its diagnostic.
