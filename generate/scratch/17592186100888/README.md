# First-order ODE verification generator

Current version 1.2.0 matches the live source format: three checkbox fields, I, II, III, each with owned false/true answers. Historical version 1.1.0 and its freeze remain under reference/. Symbolic calculations, source-specific solution steps and parameter bounds are retained. Normal generated content uses the documented interval wording correction; raw source replay is ineligible for learning.

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186100888/validate-current.py
.venv/bin/python generate/scratch/17592186100888.py --difficulty moderate --count 5 --seed 71 --format json
.venv/bin/python generate/scratch/17592186100888/replenish.py
```

The replenisher is scoped to this KP and the requested moderate job. It acquires the application api.lock, rechecks live inventory and basis, retains exact previews/requests/receipts, commits additive content through the configured application contributor, and verifies at the receipt basis before writing the requested outcome. Re-running recovers the exact saved request and verifies it without new intent.

Moderate has a finite domain of fifteen mathematical tasks; the source task is excluded from new generation by mathematical comparison. A count of sixteen fails explicitly. The asserted derivative recipe a-n reproduces the single observed error; its historical diagnosis is underdetermined. Hard is an authored family with no source difficulty rating; this job does not fill or certify hard inventory. No plots are required.

See classification.md, template-extraction.md, validation-current.json and reference/replenishment/ for the current evidence. The prior validator and masks retain the full original radio evidence.
