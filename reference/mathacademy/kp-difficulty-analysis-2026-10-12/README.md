# KP difficulty availability and lesson position

Read-only analysis of EDB `math` at basis **1522**. See the [full report](../../../kp-difficulty-report.md).

[Verification](verification.json) records inventory totals, source attribution, candidate classifications, capture positions, and evidence hashes. [KP inventory](kp-inventory.json) includes every KP, including zero-rated and small-sample cases. [Missing-level candidates](missing-level-candidates.json) gives all tentative and best-guess candidates with at least ten rated questions.

The database export precedes capture analysis. All saved EDB queries and inputs under `database/` were read with `--as-of 1522`. Capture projections preserve question identifiers, difficulty labels, lesson-order evidence and hashes of the original content/state/metadata files. Question availability is shared catalog evidence; activity-selection distributions remain separate by account.

To recalculate from these frozen inputs:

```bash
python3 capture/scripts/analyze_kp_difficulty.py analyze
/home/jake/Developer/MA/.venv/bin/python capture/scripts/analyze_kp_position.py
MPLCONFIGDIR=/tmp/course-academy-matplotlib /home/jake/Developer/MA/.venv/bin/python capture/scripts/write_kp_difficulty_report.py
```

No transaction is prepared or submitted by these scripts.
