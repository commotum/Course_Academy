# Find inventory candidates

Run from the repository root:

```sh
python3 generate/scripts/find_candidates.py
```

The fixed Datalog queries are in `queries/`. Rust executes them against one captured EDB database value; the Python launcher reuses the project's native build and database configuration. The default database and learner match the local application. Output is JSON containing qualifying topics, trigger reasons, activity types, their knowledge points, and each KP's generator reference or absence. Topics with no KPs and KPs with empty question banks remain visible.

Full discovery finds queue selections, targets, unlocked lessons, due reviews, and assigned unstarted reviews/assessments. It follows assessment steps containing KPs or questions and recovers retake topics from the original task's question presentations. It applies no course restriction or question-supply filter. Due reviews use current stored memory, its anchor and interval, and the referenced database policy's threshold; there is no assessment-age floor for reviews. Incomplete imported progress without operational memory state cannot establish a due review.

For later runs, pass the last successfully processed cursor:

```sh
python3 generate/scripts/find_candidates.py --after-basis BASIS --lineage LINEAGE
```

This reads additions and unlock/assignment changes from the captured transaction log, then checks current qualifying state. Withdrawn selections and completed tasks do not produce new work. Due reviews are checked on every run because time can advance without a transaction. The output contains the next cursor; persist it **after** the resulting inventory jobs are durably accepted. Reuse overlapping jobs as described in Trigger. A lineage mismatch or log gap fails instead of silently advancing; run full discovery to recover.

The scheduler can supply selected topic entity IDs before creating an activity or choosing questions:

```sh
python3 generate/scripts/find_candidates.py --topic TOPIC_EID --activity-type assessment
```

Repeat `--topic` to batch several selections. Selection and activity eligibility belong to the scheduler: this script discovers inventory targets and does not choose the assessment pool or enforce retake gating. `--at RFC3339_TIME` makes review checks reproducible. A generator reference establishes association; generator execution and validation belong to Inventory.

This remains a read-only discovery command. The learner server now integrates automatic preparation, captured-basis inventory counts, durable generation jobs, and generator execution or creation through `scripts/inventory_jobs.py`; `/api/inventory` exposes the scheduler inventory.

To calculate evidence-of-absence scores for every surfaced KP, save discovery output and join it to a frozen KP difficulty inventory:

```sh
python3 generate/scripts/find_candidates.py > /tmp/kp-candidates.json
python3 generate/scripts/score_absence.py --candidates /tmp/kp-candidates.json --output generate/reports/kp-absence
```

The scorer writes a table, full-precision JSON scores, and a copy of discovery output. It uses the report's `100 × (1 − (1 − p)ⁿ)` measure separately for each missing level, excludes unrated questions from n, and treats a level observed in either database or capture evidence as available. KPs with no rated evidence remain listed without scores. Discovery and inventory must have the same database, lineage and basis; use `--analysis` to select another frozen inventory. The scorer reads saved evidence and does not transact.

The table groups KPs by their missing levels. Every scored KP also receives a hybrid score for its entire missing-level pattern, `100 × [1 − (1 − Σ p_missing)ⁿ]`. Group summaries show medians of individual KP scores. A high hybrid measures the combined gap's surprise under the reference distribution; separate level scores show how strong the evidence is for each level.

Run isolated native fixtures without database access:

```sh
python3 generate/scripts/find_candidates.py --test
```
