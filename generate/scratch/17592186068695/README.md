# Graphical continuity generator

KP 17592186068695, version continuity-graph-7. Current source basis 2227;
historical source basis 1356. Database `math`, original lineage retained.

```bash
.venv/bin/python generate/scratch/17592186068695.py --difficulty hard --seed 0 --format json
.venv/bin/python generate/scratch/17592186068695/validate.py
.venv/bin/python generate/scratch/17592186068695/replenish.py
```

Easy has one five-image radio field. Normal moderate/hard output has three
checkbox fields I/II/III, each with owned true/false choices. `profile=observed`
replays historical source content; `profile=current` replays current source
content. Neither raw profile repairs q-48081 or q-48082. Normal samples retain
the original reasoning and repair presentation defects without editing sources.

The finite mathematical catalog is 4 easy, 5 moderate, 2 hard tasks. Coordinate
transforms and response-form changes cannot replenish exhausted tasks. The
replenisher enumerates that catalog, excludes every existing mathematical task,
counts validated unseen/unreserved inventory including retained learner history,
and records any remaining shortage as finite-limit. It acquires api.lock and
holds it across a fresh basis read, guarded preview/commit, receipt and exact-basis
verification. Writes use application/ca-engine and registered generator UUID/path.
Exact requests, receipts, assets and readbacks are kept under reference/replenishment.

Historical and current source replay are separate from graph correctness and
learner grading. PNG centers/rings are independently checked. The local native
harness uses the current application library, checks every owned-choice
combination (including all 8 checkbox subsets), and rejects incomplete responses.
