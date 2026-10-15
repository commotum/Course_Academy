# Horizontal or vertical tangents generator

Run `.venv/bin/python generate/scratch/17592186083278/validate.py` from the repository root. Preview `.venv/bin/python generate/scratch/17592186083278.py --difficulty all --seed 31 --count 2 --format json`.

API: generate_easy/moderate/hard(seed=0, template=None, field_type=None, parameters=None, profile=None), plus generate(level,...). Templates and original parameters are in source-cases.json. Profiles: method (supported normal default), observed (historical complete banks, opaque ones ineligible), raw (faithful public evidence including original omissions, always ineligible). Hard paired_cubics is explicitly authored. Raw q-21206 omits difficulty, solution and correct ref; raw q-21081 retains duplicate legacy field and missing correct ref. No source geometry exists.

Scope: complete requested regular-tangent parameter sets, derivative-zero solve and nonzero companion check, within the actual interval. Stationary values are excluded; no tangent classification is asserted from 0/0. Source wrapper math basis1356 is preserved. No DB, register, engine, environment or shared-file edits.

Evidence: classification.md and template-extraction.md give complete banks, four extraction stages, authored bounds and route rationale. review.md/review.json show every raw source and two changed-parameter variants per template, including all three levels. validation.json, engine-report.json, raw-equivalent-report.json and unsupported-report.json separate fidelity, mathematics, normal native acceptance and native restrictions. Original exact-answer Do not round wording rejects six equivalent entries; normal Give exact answers accepts unreduced equivalents. Inverse-cosine notation is a documented parser restriction (one unresolved probe), not a passed equivalence or engine repair.

## Inventory replenishment (2026-10-15)

The historical generator above remains unchanged. `replenish.py` now handles scoped database preparation and commit through the existing integration. See `reference/current-classification.md` for the current 12-source bank, including the migrated checkbox contract, added families, and conservative source exclusions. Run `.venv/bin/python generate/scratch/17592186083278/replenish.py` to recover retained requests or recheck inventory. It holds the application's api.lock through a guarded commit and readback. Requests, previews, receipts, native grader reports and verification are retained under `reference/replenishment/`.

Historical fidelity counts describe source basis 1356. Current source grading and mathematics have separate reports; this replenishment samples the validated polynomial, power-line and authored paired-cubic families, without claiming generator coverage for new or migrated contracts. No source questions or learner facts are changed.
