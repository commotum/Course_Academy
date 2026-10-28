# Evaluating Surface Integrals

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186105887/validate_inventory.py
.venv/bin/python generate/scratch/17592186105887.py --difficulty all --seed 7 --count 2
.venv/bin/python generate/scratch/17592186105887.py --difficulty moderate --template plane_log --profile raw:q-161347 --format json
```

The script exposes `generate`, `generate_easy`, `generate_moderate`, `generate_hard`. Explicit normal parameters are `a,b,c,lo,hi,k`; only meaningful components for each family enter mathematical identity. Raw source profiles accept the genuine integrand `scale` parameter 1..4, preserve omitted source attributes, and reproduce complete original strings/banks at unit scale. They are evidence only and ineligible for learning, because historical scalar banks do not establish historical error operations. The malformed legacy inline integral in q-160836 is preserved in raw evidence; normal output uses standard LaTeX.

Defaults cover ten observed moderate families and two authored easy constant-density families with full method-derived operation banks. `--difficulty all` emits easy and moderate. Hard generation raises an explicit unsupported-band error: the historical hard draft added an xy term outside the source backbone. Its reserve remains short. Invalid explicit parameters and whole-bank equivalences raise errors. Random sampling resamples the complete instance after selecting family and bank. The generator itself has no plots or database operations. Native radio grading is separate from displayed mathematical verification.

Version 2 retains source-family aligned worked solutions in all normal supported families. `normal-structure-regression.json` records original-parameter and varied-parameter structural checks; `family_chains.py` contains complete mathematical masks. Supplemental endpoint rows are documented in template extraction. Shared source prose, cancellation/expansion stages, metric placement, primitive stages and the natural-log convention remain in learner presentation.

Current classification, including the repaired source and two additional source-only families, is in `reference/current-classification.md`. `reference/validation-current/validation.json` records current-source and supported-generator validation. The basis-1356 source fixture and original step-7 validation remain historical evidence; the original script/freeze are retained in `reference/prior-v2/`. Current capability and freeze evidence are separate from that historical freeze.

`replenish.py --prepare-only` prepares and previews additive content using the existing database integration. Running without that option submits the exact retained request under `api.lock`, with a basis guard, and verifies the receipt and all content at its exact committed basis. It reuses registered generator identity, adds only missing supported inventory, preserves every existing question and learner fact, and reports the hard exception explicitly. Commit requests, receipts and readbacks remain in `reference/replenishment/basis-*/`.
