# Accuracy correction for the removed multipart attempt

The read-only helper replays the application's native `learning::credit` function from the immutable database state immediately before transaction 3377. Its control branch includes all six later accuracy events; the corrected branch skips only item `17592186576138` and preserves the five later Product Rule answers in their original order, with their original correctness and timestamps.

The control branch exactly matches every historical state-changing transaction and all 1,203 learner progress/performance records at basis 3429. There are no unexplained state updates or retention events in that interval. Instants are normalized before comparing the API's ISO representation with EDB's millisecond representation.

The correction changes three progress records and global performance. The trig profile returns exactly to its pre-event state. Product Rule and one downstream profile retain their actual answers but receive the counterfactual initial practice forecasts; simply subtracting one global/topic observation would miss these dependencies. Memory, learned status, repetition counts, intervals, assessment evidence, and all other records are unchanged.

- `accuracy-forms.edn`: guarded value changes and native entity ensures; these must be combined with the task-chain repair in a transaction guarded by basis 3429.
- `audit.json`: exact replay events and field changes.
- `initial.json`, `before.json`, `after.json`: immutable pre-event, current, and corrected dynamic records.
- `independent-checks.json`: separate five-answer global EWMA calculation, exact trig restoration, and protected-field checks.
- `build.json`, `build.py`, `replay_tail.rs`: native build provenance and reproducible read-only helper. It never commits transactions.

If learner state changes after basis 3429, rerun the helper before preparing a new transaction. The initial instant-representation diagnostic is retained separately and is superseded by the successful normalized control replay.
