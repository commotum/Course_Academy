# Ellipse derivative generator

Local review only; database math basis 1356. No database writes or registration.

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186166866/validate.py
.venv/bin/python generate/scratch/17592186166866.py --difficulty all --count 2 --seed 0 --format markdown
```

Public API: `generate_easy`, `generate_moderate`, `generate_hard`, and `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`. Template origin/shifted is determined by geometry. Only radio is supported. Profiles: normal `authored-method`; source `observed-q-...` preserves omitted raw attributes; `completed-q-...` adds separately inferred correct ref/solution/label. Source profiles remain explicitly evidence only. JSON is local review data, never EDN.

All variants reconstruct the displayed ellipse equation and use the same implicit differentiation. Moderate uses one shift with two nonunit reduced ratio terms, or two shifts with one unit reduced term. Hard requires both shifted coordinates and both nonunit reduced terms, with coprime semiaxes 3..8; no other conic or calculus method enters scope. Historical bank cognitive interpretations remain hypotheses. Two absent captured refs cannot count as observed matched designations. The real grader checks owned radio selections; independent mathematics verifies all displayed values and solution stages separately.

`generation.domain` records the real ellipse equation, positive unequal horizontal/vertical semiaxes, and the sole finite-slope exclusion y=k. Coordinate axes themselves are allowed on the locus. `generation.source` records immutable database/basis/lineage and applicable source support; `generation.dependencies` records runtime Python/SymPy versions. `domain-proof.py` checks these metadata against displayed denominators and proves fixed-call learner questions/identities are unchanged; no plot rerender or native regrade is required for metadata-only changes.

`difficulty-boundary.json` records zero overlap between the finite meaningful-task domains and explicit rejection regressions. Unrated q-127364 remains unrated in raw replay and receives inferred hard in its separate completion. Content identity includes actual level. Version 2.0 deliberately changes generated question/answer IDs while preserving source prompts, every source value/bank and all present source solutions. Metadata-only preservation evidence from version 1.1 is retained as historical evidence; the current domain proof snapshots apply to version 2.0.
