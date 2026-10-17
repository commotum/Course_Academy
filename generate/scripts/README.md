# Rank generator-build candidates

Run from the repository root:

```sh
python3 generate/scripts/find_candidates.py
```

The fixed Datalog queries are in `queries/`. Rust executes them against one captured EDB database value; the Python launcher reuses the project's native build and database configuration. The default database and learner match the local application. Output retains complete nested `topics` and their inventories, and adds a flat `knowledge_points` list containing one ranked build candidate per KP. Topics with no KPs and KPs with empty question banks remain visible.

Eligibility includes studied topics, targets, queued topics, their unmet necessary prerequisites, direct descendants of studied or queued topics, and current activity needs. Necessary prerequisites follow `topic/next` and KP key-prerequisite relationships transitively, stopping at mastered prerequisite branches. Direct descendant expansion remains one hop. Required remediation and active work can enter even outside the learner's selections. There is no course or stock filter. A completed lesson or initialized learned progress establishes study; legacy positive repetitions count when `progress/learned` is absent. A completed review establishes review history.

The finder and durable worker use one comparator, `scripts/generator_priority.py`, under policy `relevance-v2`. Relevance is the first key:

| Tier | Relevance |
| ---: | --- |
| 0 | Required remediation or supply needed by an active/requested activity |
| 1 | Selected study: queue, targets, and unmet necessary prerequisites |
| 2 | Other current review or assessment needs |
| 3 | Speculative preparation and maintenance outside current study |

Tier 0 applies to the matching activity demand, not every possible shortage in its topic. A selected review shortage precedes a speculative lesson shortage regardless of either bank's size. Within each relevance tier, purpose orders work as follows:

| Purpose | Points | Shortage |
| --- | ---: | --- |
| Upcoming lesson | 60,000 | Missing toward 5 total questions in this KP |
| Upcoming review | 50,000 | Missing toward 5 total questions across the topic |
| Upcoming assessment | 40,000 | Missing toward 1 rated question across the topic |
| Hard-topic assessment coverage | 30,000 | Missing toward 1 distinct topic |
| Moderate-topic assessment coverage | 20,000 | Missing toward 2 distinct topics |
| Easy-topic assessment coverage | 10,000 | Missing toward 3 distinct topics |
| Advance build | 0 | 0 |

Only a positive shortage receives shortage priority. The strongest applicable reason wins; reasons are not added. The old additive `score` and point components remain diagnostic fields and do not determine ordering.

Within lesson work, topics sort by global prerequisite layer ascending, distinct selected goals supported descending, engine priority descending, waiting age, and stable topic ID. Layers reuse the engine's longest path through `topic/next`; the stored layer is zero-based. Support counts distinct IDs in the union of queue and targets, including the topic itself if selected. Duplicate selections and multiple paths to one goal count once. Topic ordering precedes KP shortage size, so an earlier lesson's deficient KPs stay together. Reviews use their due dates rather than graph layers; assessments retain first-study age as a tiebreaker. Stable KP IDs finish the ordering.

Activity demands are simultaneous. A target without a completed local lesson needs lesson supply even if imported mastery implies a review next. A queued topic establishes explicit lesson demand, including re-study after an earlier local completion. A completed review or assessment does not substitute for a completed local lesson. Existing review or assessment demand is evaluated alongside lesson demand, using its own pool. `next_activity` remains a diagnostic summary, not an exclusive filter on shortages. First-study dates come from completed lesson timestamps; unknown imported dates stay unknown and sort last.

Counts exclude seen, reserved, canonical, invalid and ungraded free-response questions. Valid unrated questions count toward lesson/review totals; assessments require rated questions. Variety is measured over all eligible studied-and-reviewed topics, including topics whose generators already exist or whose next activity is another review. Each demand determines its depletion scope, not membership in this coverage pool. One topic occupies at most one of the six difficulty slots. A candidate earns variety priority only when adding a source-observed band improves this coverage; unknown band capability is not assumed. Output shows the proposed band and resulting coverage.

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

Repeat `--topic` to annotate several scheduler requests. These establish demand for the requested activity and can admit a topic outside the usual eligibility groups. They do not restrict the global inventory read. Use bounded entity reads for a small readiness investigation instead of treating this option as a query filter. The coverage calculation guides build ranking and does not construct an assessment or change assessment admission. `--at RFC3339_TIME` makes review checks reproducible.

This command is read-only. The learner server calls the same discovery and ranking
code in its background inventory refresh, then admits durable jobs through
`scripts/inventory_jobs.py`. Its build worker uses this ranking; valid legacy
registrations additionally enter the queue for packaging and independent review.
Its separate refill worker maintains approved packages toward five questions per
difficulty. `--include-registered` adds registered hashed-package topics outside
the urgency groups to the nested inventory for maintenance; those topics cannot
create new generators and use routine replenishment priority.

The accepted live cursor and job files are under
`.local/learning/inventory/<database>/<learner>/`; the cursor marks this policy as
`relevance-v2`. `/api/inventory` remains the native activity-readiness diagnostic from
`engine/rust/inventory.rs`, not the ranked generator job queue. Generator ranking
does not change the engine's lesson/review/assessment admission rules.

Pending or uncertain publications retain a recovery override so the worker can
reconcile the exact saved request. Other unfinished drafts retain their workspaces
and resume at their current priority. A draft whose demand disappears is retained
without running until demand returns. Existing approved packages remain in the
separate refill lane; routine replenishment does not acquire an unrelated activity's
immediate priority.

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
