# Parametric graph generator

Run `.venv/bin/python generate/scratch/17592186087721/validate.py` for source prose/table/asset fidelity, independent displayed mathematics, complete graph-bank uniqueness, native radio grading and concurrent render checks. Run `.venv/bin/python generate/scratch/17592186087721.py --difficulty all --seed 42 --count 2 --format json` for local previews. No database operations.

Observed coverage:16 easy questions,80 exact unchanged answer assets,16 exact correct parametrizations,16 full two-table worked sequences. The64 wrong graph formulas are residual source assets, not claimed recovered operations. Default banks are authored, parameter-dependent and rendered via cached Matplotlib3.10 dependencies; source replay is restricted to the original complete profiles. Moderate/hard levels are authored bounded table/graph-recognition extensions, described in classification.md.

`capabilities.json` records the supported levels and finite restrictions. Moderate and hard share the same 96 parameter combinations; changing the bank does not create another mathematical task. Replenishment deduplicates complete loci and domains across source and generated questions and across difficulty levels.

Run `.venv/bin/python generate/scratch/17592186087721/replenish.py` to recheck current inventory and prepare validated, previewed transactions. Add `--commit` to submit. The helper acquires the application's `api.lock`, reads current inventory and source evidence at one basis, retains that lock through basis-guarded submission and exact-basis verification, and recovers an existing saved request before preparing another. It preserves the generator UUID once registered. Existing request recovery can confirm a previously submitted transaction even without `--commit`.

The scoped `reference/replenishment/` folder retains current source reads, exact selected instances, native grader reports, published asset hashes, preparation, preview, complete request, durable receipt and readback. `freeze.json` records the generator identity and hashes. No captured question or learner history is rewritten.
