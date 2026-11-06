# Rank generator-build candidates

Run from the repository root:

```sh
python3 generate/scripts/find_candidates.py
```

The fixed Datalog queries are in `queries/`. Rust executes them against one captured EDB database value; the Python launcher reuses the project's native build and database configuration. The default database and learner match the local application. Output retains complete nested `topics` and their inventories, and adds a flat `knowledge_points` list containing one ranked build candidate per KP. Topics with no KPs and KPs with empty question banks remain visible.

In self-directed mode, ordinary new-lesson demand uses the same scope as Study:
`learner/targets` union `learner/queue`, plus prerequisites through two reverse
`topic/next` edges, limited to global layer 30 or above. Topics with no progress
record or fewer than one repetition are new, unless explicit learned status or a
completed lesson/review already establishes learning. Repetitions of one or more
exclude a topic even when its local learned flag is false. Deeper prerequisites
and KP-only prerequisite links do not expand this scope, and prerequisite mastery
does not gate its lessons.

Required remediation, active work, scheduler requests, and current review or
assessment needs retain demand outside the new-lesson scope. Registered packages
remain available for maintenance. Broader studied and descendant metadata can
appear for diagnostics, but an outside ordinary lesson without activity demand
does not create an authoring job.

Standard self-directed discovery captures this population at one database basis.
It does not wait for directly selected topics to have usable generators or a full
five-per-band reserve before considering prerequisite lessons. `selection_gate`
reports mode `study-scope`, the scoped KP set, missing generators, and shortages
against five total questions per KP; its `open` field stays true. These shortages
affect ranking rather than admission of other jobs.

Course mode retains the earlier discovery phases and completion gate. Its first
pass reads directly selected topics and registered refill packages. Broader
authoring opens only after every directly selected KP has a usable hashed
generator and five available questions in each difficulty band. The full capture
checks this gate again. Course-mode prerequisite discovery retains operational
readiness and transitive topic/KP prerequisite links. Explicit native
`selected_only` inspection also keeps its direct-selection contract; the standard
launcher sends `respect_study_scope` to use the self-directed behavior.

The finder and durable worker share `scripts/generator_priority.py`, under policy
`study-scope-v6`. Urgency is the first comparison:

| Order | Work |
| ---: | --- |
| 0 | Actual shortages for active, requested, or required remedial work |
| 1 | Other actual lesson, review, or assessment shortages |
| 2 | Distinct-topic assessment variety |
| 3 | Advance builds and routine replenishment |

Within an urgency class, relevance precedes activity purpose:

| Tier | Relevance |
| ---: | --- |
| 0 | The matching active, requested, or remedial activity demand |
| 1 | All new scoped lessons, plus directly selected study needs |
| 2 | Other selected prerequisite preparation, including course-mode preparation |
| 3 | Other current review or assessment needs |
| 4 | Speculative preparation and maintenance outside current study |

A depth-two new lesson has the same relevance as a selected root. An active
review shortage keeps its immediate priority, while a stocked selected topic's
advance build cannot displace an actual lesson shortage. Immediate priority does
not carry over to unrelated future bands on the same topic.

| Purpose | Diagnostic points | Shortage |
| --- | ---: | --- |
| Upcoming lesson | 60,000 | Missing toward 5 total questions in this KP |
| Upcoming review | 50,000 | Missing toward 5 total questions across the topic |
| Upcoming assessment | 40,000 | Missing toward 1 rated question across the topic |
| Hard-topic assessment coverage | 30,000 | Missing toward 1 distinct topic |
| Moderate-topic assessment coverage | 20,000 | Missing toward 2 distinct topics |
| Easy-topic assessment coverage | 10,000 | Missing toward 3 distinct topics |
| Advance build | 0 | 0 |

Only a positive shortage receives shortage priority. At the same urgency and
relevance, lesson shortages precede reviews and assessments; variety follows
hard/moderate/easy order. The strongest applicable reason wins; reasons are not
added. The additive `score` and point components remain diagnostic fields and do
not determine ordering.

Within lesson work, topics sort by global prerequisite layer ascending, distinct
selected goals supported descending, engine priority descending, waiting age,
and stable topic ID. Layers use the engine's longest path through `topic/next`;
the stored layer is zero-based. Support counts distinct IDs in the union of queue
and targets. Topic ordering precedes KP shortage size, so an earlier lesson's
deficient KPs stay together. Reviews use their due dates; assessments retain
first-study age as a tiebreaker. Stable KP IDs finish the ordering. Study can keep
serving available lessons while generation prepares an earlier missing bank.

Activity demands are simultaneous. Self-directed ordinary lesson demand follows
the new-topic filter above; merely selecting an already known topic does not make
it a new lesson. Existing active, explicit scheduler, and remedial lesson requests
retain their independent demand. Review and assessment demand use their own
pools. Course mode retains its direct queue/target lesson rules. `next_activity`
is a diagnostic summary rather than an exclusive shortage filter. First-study
dates come from completed lesson timestamps; unknown imported dates stay unknown
and sort last.

Counts exclude seen, reserved, canonical, invalid and ungraded free-response questions. Valid unrated questions count toward lesson/review totals; assessments require rated questions. Variety is measured over all eligible studied-and-reviewed topics, including topics whose generators already exist or whose next activity is another review. Each demand determines its depletion scope, not membership in this coverage pool. One topic occupies at most one of the six difficulty slots. A candidate earns variety priority only when adding a source-observed band improves this coverage; unknown band capability is not assumed. Output shows the proposed band and resulting coverage.

Registered script paths are checked without execution; hashed packages are verified against their manifests. Usable registrations are excluded from the flat build list. Missing/corrupt registered scripts remain as `repair-generator` candidates with `generator_error`. This checks artifacts, not runtime dependencies or pedagogical approval. Existing unregistered drafts remain candidates for the pipeline to adopt and review. Each candidate exposes its score components, inventory scope, alternative reasons and per-band `refill_deficits` toward 5 easy, 5 moderate and 5 hard. Refill deficits do not become extra build-priority points.

For later runs, pass the last successfully processed cursor:

```sh
python3 generate/scripts/find_candidates.py --after-basis BASIS --lineage LINEAGE
```

The cursor validates the captured transaction log and lineage. Every invocation
ranks the current eligible population at its captured basis, including due reviews
whose eligibility can change without a transaction. Self-directed discovery reads
the full current population once; course-mode broader discovery remains subject
to its completion gate. Assessment coverage is diagnostic for the captured
population. The output contains the next cursor. A lineage mismatch or log gap
fails instead of silently advancing.

The scheduler can supply selected topic entity IDs before creating an activity or choosing questions:

```sh
python3 generate/scripts/find_candidates.py --topic TOPIC_EID --activity-type assessment
```

Repeat `--topic` to annotate several scheduler requests. In self-directed mode
these can establish immediate activity demand outside ordinary new-lesson scope.
Course-mode requests remain subject to its direct-selection completion gate. This
option is not a query filter: use bounded entity reads for a small readiness
investigation. Coverage guides build ranking and does not construct an assessment
or change assessment admission. `--at RFC3339_TIME` makes review checks reproducible.

This command is read-only. The learner server calls the same discovery and ranking
code in its background inventory refresh, then admits durable jobs through
`scripts/inventory_jobs.py`. Its build worker uses this ranking; valid legacy
registrations additionally enter the queue for packaging and independent review.
Its separate refill worker maintains approved packages toward five questions per
difficulty. Regardless of the selection gate, `--include-registered` adds registered
hashed-package topics outside the urgency groups to the nested inventory for
maintenance; those topics cannot create new generators and use routine
replenishment priority.

The accepted live cursor and job files are under
`.local/learning/inventory/<database>/<learner>/`; the cursor marks this policy as
`study-scope-v6`. `/api/inventory` remains the native activity-readiness diagnostic from
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
