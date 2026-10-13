# Autonomous ODE recognition

Validated generator, registered in `math` at verified basis **2019** as UUID `6c93b455-deee-5719-9f14-e7863ffa3268`. The registration request and receipt are in `reference/replenishment/basis-2018/`. This review job's topic pool already had 22 easy, 10 moderate, and 5 hard available questions, so no new questions were committed. All 15 source questions, the canonical example, and learner history were preserved. Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186166814.py --difficulty all --seed 11 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186166814/validate.py
```

The public API has `generate_easy`, `generate_moderate`, `generate_hard`, and `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`. Normal defaults use authored checkbox triplets. For source evidence, use a `q-...` template with its captured level and `profile="observed_raw"`; this preserves the erroneous q-96702 worked solution and marks the whole record evidence-only. `observed_repaired` is eligible and fixes that denominator. Source cases list exact parameters and profiles. The source snapshot's database, basis 1356, and lineage remain attached.

The CLI filters repeated mathematical fingerprints within each requested batch and rejects counts above its finite catalog limits. Existing source-mask templates offer one categorical task each. Before any future content commit, compare the output with the entire current KP pool and canonical example; local seed changes and shuffled choices do not establish fresh inventory. `capabilities.json` documents finite bounds and the authored hard-level extension. Five distinct local previews per level are in `reference/execution.json`; independent mathematics and current-engine grading results are retained alongside them.

Easy authored questions classify three isolated RHS expressions. Moderate authored questions subtract one constant and divide by a derivative coefficient for each equation. Hard authored questions divide a factored RHS by an affine independent-variable coefficient, recognizing matching versus unmatched factors. All remain first-order autonomous recognition; no differential equation is solved. These authored level claims are not observed labels. Numerical aliases do not inflate the finite semantic catalogs.

`validation.json` separates raw fidelity, original mathematics, supported repairs, and actual engine grading. `review.md` displays every original and changed-source variant, plus authored examples at every level. `native-report.json` records real `learning::grade_field` checks. `validate.py` reads all mathematical stages back from displayed strings and rejects undocumented anomalies, schema errors, invalid bounds, identity instability, and native grading failures. No assets or plotting dependencies are required.

Frozen artifact hashes are in `freeze.json`. Re-running validation deterministically refreshes review and QA evidence; do not change the source capture.
