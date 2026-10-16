# Rank generator-build candidates

Run from the repository root:

```sh
python3 generate/scripts/find_candidates.py
```

The fixed Datalog queries are in `queries/`. Rust executes them against one captured EDB database value; the Python launcher reuses the project's native build and database configuration. The default database and learner match the local application. Output retains complete nested `topics` and their inventories, and adds a flat `knowledge_points` list containing one ranked build candidate per KP. Topics with no KPs and KPs with empty question banks remain visible.

Eligibility is the union of studied topics, targets, queued topics, direct prerequisites of targets, and direct descendants of studied or queued topics. Graph expansion is exactly one hop across `topic/next` and KP key-prerequisite relationships. There is no course or stock filter. A completed lesson or initialized learned progress establishes study; legacy positive repetitions count when `progress/learned` is absent. A completed review establishes review history. Pending activities and due reviews identify the next activity within the eligible population; they do not bypass eligibility.

The score is `purpose_points + 1000 × shortage + 100 × urgency_value`:

| Purpose | Points | Shortage |
| --- | ---: | --- |
| Upcoming lesson | 60,000 | Missing toward 5 total questions in this KP |
| Upcoming review | 50,000 | Missing toward 5 total questions across the topic |
| Upcoming assessment | 40,000 | Missing toward 1 rated question across the topic |
| Hard-topic assessment coverage | 30,000 | Missing toward 1 distinct topic |
| Moderate-topic assessment coverage | 20,000 | Missing toward 2 distinct topics |
| Easy-topic assessment coverage | 10,000 | Missing toward 3 distinct topics |
| Advance build | 0 | 0 |

Only a positive shortage receives its purpose points. The strongest applicable reason wins; reasons are not added. Urgency values are studied 5, target 4, queued 3, direct prerequisite 2, direct descendant 1; overlapping groups use their maximum. Thus purpose precedes shortage size, then urgency. Equal assessment-shortage scores use the oldest known first-study date. Other ties use the oldest selection/offer date and stable entity IDs. Assignment deadlines and engine priority remain diagnostics and do not affect this score.

The next activity is exclusive: active work first, then unlocked/scheduler-selected work, due reviews, and assigned work. Without a concrete upcoming activity, unstudied means lesson, studied means review, and studied plus reviewed means assessment. First-study dates come from completed lesson timestamps; unknown imported dates stay unknown and sort last.

Counts exclude seen, reserved, canonical, invalid and ungraded free-response questions. Valid unrated questions count toward lesson/review totals; assessments require rated questions. Variety is measured over all eligible studied-and-reviewed topics, including topics whose generators already exist or whose next activity is another review. Next activity determines depletion scope, not membership in this coverage pool. One topic occupies at most one of the six difficulty slots. A candidate earns variety points only when adding a source-observed band improves this coverage; unknown band capability is not assumed. Output shows the proposed band and resulting coverage.

Registered script paths are checked without execution; hashed packages are verified against their manifests. Usable registrations are excluded from the flat build list. Missing/corrupt registered scripts remain as `repair-generator` candidates with `generator_error`. This checks artifacts, not runtime dependencies or pedagogical approval. Existing unregistered drafts remain candidates for the pipeline to adopt and review. Each candidate exposes its score components, inventory scope, alternative reasons and per-band `refill_deficits` toward 5 easy, 5 moderate and 5 hard. Refill deficits do not become extra build-priority points.

For later runs, pass the last successfully processed cursor:

```sh
python3 generate/scripts/find_candidates.py --after-basis BASIS --lineage LINEAGE
```

The cursor validates the captured transaction log and lineage. Every invocation still ranks the complete current eligible population: omitting unchanged topics would corrupt global variety counts and hide proactive builds. Due reviews are also checked on every run because time can advance without a transaction. The output contains the next cursor. A lineage mismatch or log gap fails instead of silently advancing; run full discovery to recover.

The scheduler can supply selected topic entity IDs before creating an activity or choosing questions:

```sh
python3 generate/scripts/find_candidates.py --topic TOPIC_EID --activity-type assessment
```

Repeat `--topic` to annotate several selections. These override the inferred next activity only within the five eligibility groups; they do not restrict the global inventory read or admit unrelated topics. The coverage calculation guides build ranking and does not construct an assessment or change assessment admission. `--at RFC3339_TIME` makes review checks reproducible.

This remains a read-only discovery command. It does not launch builds or refill questions. The learner server has a separate scheduling policy in `engine/rust/inventory.rs` and `scripts/inventory_jobs.py`; updating this finder does not change that live worker's ranking. `/api/inventory` exposes the live scheduler inventory.

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
