# Modeling Inhibited Growth generator

Read-only capture: math basis 1356. Generator scope is construction of one inhibited-growth ODE; no integration, calibration or future-population calculation.

```sh
.venv/bin/python generate/scratch/17592186124674.py --difficulty all --count 2
.venv/bin/python generate/scratch/17592186124674/validate.py
```

API: `generate_easy`, `generate_moderate`, `generate_hard`, or `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`. Source cases use public `observed_<source-db-id>` profiles, complete parameterized masks and banks. Those raw profiles preserve absent difficulty/solution/correct attributes. `repaired_<source-db-id>` adds supported completions; factory units are minimally repaired. Normal defaults use bounded operation banks; scalar evidence ratios are excluded from default sampling.

Moderate/hard levels are authored coefficient-placement extensions. See classification/extraction for scope, limits and finite semantic model counts. `review.md` explicitly labels originals, changed observed profiles, supported completions and all authored levels. `validation.json` reports exact coverage and native-grade outcomes separately. `producer-manifest.json` freezes file SHA256s, excludes itself, and is private worker evidence; parent QA may amend findings separately.

Root QA: raw and opaque banks expose explicit evidence-only/ineligible metadata; defaults remain eligible. Review choices show present correct designations and actual difficulty labels. Repaired opaque scalar banks also remain evidence-only.
