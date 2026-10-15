# Flux-integral generator

Run `.venv/bin/python generate/scratch/17592186198378/validate.py`.
Preview `.venv/bin/python generate/scratch/17592186198378.py --difficulty all --seed 12 --count 2 --format markdown`.

Nine observed families (five easy, four moderate), with complete observed banks available via `--profile observed`. Defaults are labeled authored method-error banks; hard has two authored unhinted full-integrand families. No flux evaluation, plotting, database transactions, or engine edits. Domain and legacy-format repairs are documented in template-extraction.md. review.md shows every original, source replay, scaled observed bank and two authored default variants per template plus four authored hard examples.

validation.json separates exact full-bank mathematics, shared-sentence/stage fidelity, instance correctness, identities, and native radio grading. Source LaTeX is normalized rather than byte-identical. Native selection checks do not establish symbolic correctness; the failing independent validator does that separately.


## Inventory commit, 2026-10-15

The existing generator was revalidated and registered as `4f666256-5aea-5cdd-b77f-892b7d566373` with script `generate/scratch/17592186198378.py`. Current classification covers 12 source banks at basis 2693; the frozen sampler retains nine source families and its two authored hard families. See `classification-current.md` and `capabilities.json` for the distinction.

Five distinct hard questions were committed and read back at basis **2694**. Validated fresh inventory is **6 easy, 6 moderate, 5 hard**, leaving no reserve shortage. All 12 existing practice questions, the canonical example, prerequisites and learner history were preserved. All 154 committed datoms are additive and attributed to `:application/ca-engine`.

`reference/replenishment/basis-2693/` retains the exact EDN, durable request, speculative preview, confirmed receipt, generated content, source/native-grading checks and verified readback. `replenish.py` holds the application's `api.lock` from fresh inventory reads through commit/readback and recovers a saved submission before considering new work.
