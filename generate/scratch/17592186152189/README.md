# General-center ellipse scratch generator

Verification:

```bash
.venv/bin/python generate/scratch/17592186152189/validate.py
.venv/bin/python generate/scratch/17592186152189.py --difficulty all --seed 21 --count 2 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy/moderate/hard`. Normal templates are supplied, graph, oriented_radio and oriented_blank. All defaults are method-derived complete banks; raw `observed:q-ID` profiles and matching source templates preserve every source mask, full historical bank, attribute omission and field order. Raw profiles are evidence-only; normal questions have complete refs/solutions and authored metadata. Invalid explicit inputs and ambiguous whole banks raise, without silently changing parameters.

Source-cases.json exercises every public replay. Validation separates exact source fidelity, independently parsed printed mathematics, original raster geometry and native learner grading. Canonical/factored blank entries grade; trig phase-shift identities receive 14 explicitly documented unresolved checks. They are independently mathematically valid and do not count as native acceptance. The two captured missing correct refs cannot be graded as raw fields; fixtures explicitly include only designated fields, preserving raw evidence separately. See classification.md for source anomalies and authored level rationale.

The original package stopped at step 7. Inventory replenishment now continues through preparation and durable commit with `replenish.py`; it only adds this KP's generated questions and generator registration. Current source additions, replay evidence, and the actual commit are described below.

[native-limitations.md](native-limitations.md) lists every actual unresolved submission, source/normal eligibility, parameters and native error.


## Inventory replenishment

Run `.venv/bin/python generate/scratch/17592186152189/replenish.py` from the repository root. It reuses the application database integration, compiles the grader fixture against the current application library, checks all 18 captured source questions and complete banks, rechecks current inventory, and holds `.local/learning/requests/math/api.lock` through fresh basis reads, guarded submission and exact-basis verification. A retained exact request is recovered before preparing another submission. Committed questions have content-derived identities and field-owned answer identities. The stable generator identity is retained in `generator-id.json`.

Current source capture is at basis 2658; `current-source-extraction.md` and `specs-current-additions.json` cover the three additional source questions. Original source captures remain unchanged. `reference/replenishment/validation.json` supersedes the old freeze for the expanded source loader; normal templates retain version `ellipse-general-1` and unchanged payload semantics. All new generated questions are validated by the actual grader. Historical phase-shift blank equivalence limitations remain documented and are not counted as accepted checks.

The verified transaction advanced basis 2658 to 2659, added five genuinely different easy ellipses, and registered the generator. The final checked inventory is easy 5, moderate 7, hard 9, with no remaining shortage. All 18 source questions, the canonical example and learner history were preserved. Exact original request, logical EDN, preview, receipt, readback and verification are retained under `reference/replenishment/basis-2658/`. Later invocations recover this job's retained submission; they do not manufacture duplicate content.
