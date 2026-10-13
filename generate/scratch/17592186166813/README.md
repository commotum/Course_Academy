# ODE-order generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186166813/validate.py
.venv/bin/python generate/scratch/17592186166813.py --difficulty all --seed 42 --count 2 --format markdown
```

API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus generate_easy/moderate/hard. Source replay uses template=source_id, profile="observed", parameters from source-cases.json. Authored defaults use single/selection/mixed_selection and profile="authored". Invalid explicit parameters raise ValueError; they are never replaced by sampled values. JSON records are local review artifacts, never transactions.

Scope is recognition of the highest displayed ordinary derivative only. Easy/moderate observed; hard authored from existing higher-derivative notation plus sourced derivative power/product and full-equation scanning. Source opaque numeric catalogs remain evidence-only. q-167787 restated RHS anomaly has a separate source_repaired profile; source order answer itself is unchanged. All learner eligible defaults use authored complete banks and clean solutions. No solving, ODE linearity/autonomy, IVP/PDE branch or plots.

Frozen version ode-order-frozen-1. Evidence includes source wrapper, full extraction and73-choice mapping, original parameter replay cases, changed-source recipes, source-fidelity results, explicit finite-domain QA, native input/report, labeled review and dependency/hash freeze. Validation compares every original prompt, solution and field/bank with source evidence, checks displayed order via an independent reader and SymPy, tests every native choice plus equivalent/wrong blank entries, and fails on mismatch. Historical distractor intention is explicitly unresolved; exact source values are not a recovered authorship claim.
