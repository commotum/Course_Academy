# General-center ellipse scratch generator

Verification:

```bash
.venv/bin/python generate/scratch/17592186152189/validate.py
.venv/bin/python generate/scratch/17592186152189.py --difficulty all --seed 21 --count 2 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy/moderate/hard`. Normal templates are supplied, graph, oriented_radio and oriented_blank. All defaults are method-derived complete banks; raw `observed:q-ID` profiles and matching source templates preserve every source mask, full historical bank, attribute omission and field order. Raw profiles are evidence-only; normal questions have complete refs/solutions and authored metadata. Invalid explicit inputs and ambiguous whole banks raise, without silently changing parameters.

Source-cases.json exercises every public replay. Validation separates exact source fidelity, independently parsed printed mathematics, original raster geometry and native learner grading. Canonical/factored blank entries grade; trig phase-shift identities receive 14 explicitly documented unresolved checks. They are independently mathematically valid and do not count as native acceptance. The two captured missing correct refs cannot be graded as raw fields; fixtures explicitly include only designated fields, preserving raw evidence separately. See classification.md for source anomalies and authored level rationale.

Evidence remains local and stops at step 7. No database, registration, engine edits, or shared files are changed.

[native-limitations.md](native-limitations.md) lists every actual unresolved submission, source/normal eligibility, parameters and native error.
