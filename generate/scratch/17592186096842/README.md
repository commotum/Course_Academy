# Radical chain rule generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186096842/validate.py
.venv/bin/python generate/scratch/17592186096842.py --difficulty all --seed 42 --count 2 --format json
```

All nine source questions and all three observed levels are supported. Original complete banks are explicit profiles; radios default to authored whole operation banks. Scope: square-root/reciprocal-square-root outer functions, linear/two-term quadratic radicands, Leibniz differentiation or slope evaluation. No plots, registrations or database writes. q-48846's missing level, correct ref and solution are documented repairs. Unresolved empirical distractor intent is preserved as evidence; defaults do not use it.

See classification.md, template-extraction.md, choice-map.json, source-cases.json, review.md/json, and validation.json. templates.json contains reusable prose scaffolds, never source answer payloads. Re-extraction uses extract.py; regenerate documentation with document.py. The native grader binary path and digest are recorded in validation.json. Canonical and expanded-cubic-radical equivalent blanks are tested. A mathematically correct fractional-power alternate receives an unresolved-domain error from the current native grader; this failed acceptance capability is reported separately in engine-domain-probe-report.json and never counted as wrong-answer rejection.
