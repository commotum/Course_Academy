# Parametric tangent-line generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186083244/validate.py
.venv/bin/python generate/scratch/17592186083244.py --difficulty all --seed 42 --count 2 --format json
.venv/bin/python generate/scratch/17592186083244.py --difficulty hard --profile observed_17592186319230
```

Public Python API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus generate_easy/generate_moderate/generate_hard. Normal default profiles use authored complete banks. Public observed profiles reproduce raw captured field layouts and omission/presence; they are explicitly evidence_only and ineligible. source-cases.json contains all six calls at original parameters. No DB clients, registration, shared environment changes or plots are generated.

Scope: substitute parameter, derive finite tangent slope, compute line; hard asks its source-shaped axis intersection. Easy is the missing-level authored canonical extension. Moderate quintic rating/key/solution are authored from independent mathematics because captured q6862 lacks them. Source opaque banks are parameterized evidence, with unresolved intent documented. Full line equations are checked modulo nonzero scalar using actual point and derivative ratio; native UUID grading is separate. Native blank equivalents are exercised for every coordinate field. Raw log “Do not round” intentionally retains the engine's rejection limitation; normal “Give exact answers” preserves the exact-answer mathematical demand.

Evidence: source.json frozen wrapper; source-widget-q6862.json original widget confirming absent key; lesson-route.json next-link traversal; classification.md; template-extraction.md; plot-extraction.md; canonical-inspection.png; review.md/json; engine-input/report.json; validation.json. display-parser.py is a private read-only copy of the parent elementary parser, used independently of generator helpers and mathematics metadata. validate.py checks every original value, captured difficulty enum/presence, source prose/row fidelity, displayed curve and all solution stages, choice ambiguity, level limits, JSON equality, identity, and native grading. The parser is fail-closed for supported displayed forms.
