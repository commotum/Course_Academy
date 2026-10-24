# Scaffolded trig-substitution generators and refreshed pools

Completed for topic **17592186050489**, Integrating Trigonometric Functions Using Substitution.

The four replacements were committed at **T6526–T6529**, attributed to `:agent/codex`. Live readback at **T6535** verified their registrations, all new records, retirement flags, and fresh inventory. See [completion.json](completion.json).

| KP | Scope | New easy | New moderate | New hard | Superseded generated questions retired |
| --- | --- | ---: | ---: | ---: | ---: |
| 17592186068915 | Sine/cosine with linear arguments | 8 | 8 | 8 | 19 |
| 17592186068916 | Reciprocal trig with linear arguments | 8 | 8 | 8 | 24 |
| 17592186068917 | Products using substitution | 8 | 8 | 8 | 24 |
| 17592186068918 | Quotients using substitution | 8 | 8 | 8 | 24 |
| **Total** | | **32** | **32** | **32** | **91** |

All **96 new questions were unserved** at final readback. All **68 imported practice questions**, four canonical examples, old question/answer content, and saved learner history were preserved. Retirement excludes old generated questions from fresh practice without detaching them from their KPs or rewriting saved work.

The overly demanding generated question **17592186676292** is retired. Previously retired **17592186482724**, with 24 and 48 in its easy integral, remains retired.

## Revised pedagogy

The design follows the [source comparison](../../audits/2026-10-24-difficulty-pedagogy/README.md), including the six complete easy/moderate/hard examples from KP 17592186064172 and the supplied-substitution tasks from KP 17592186064209.

- **Easy:** the question supplies u and asks which transformed integral follows. Five radio choices test the differential factor and, where applicable, the bounds. The learner does not have to finish evaluating the integral.
- **Moderate:** the learner chooses the substitution and completes the calculation. The prompt supplies the familiar primitive formula, plus endpoint values for definite integrals. Numerical work stays small.
- **Hard:** the prompt retains the primitive and evaluation support. One target-specific condition changes: a negative affine derivative/decreasing bounds; recognition of a reciprocal or square-root input; or a supported quotient rearrangement, nested input, or definite evaluation. These are separate cases, not independently stacked complications.

Linear amplitudes are small integers and slope magnitudes are 2–4. Reciprocal definite examples use magnitude 2 to keep the original bounds simple; their function families, intervals and amplitudes vary. Definite primitive endpoint values are supplied and remain integers. Product recognition questions have no radical integration bounds. Quotient numerators, offsets and coefficients are small, and no extra input frequency is layered onto their harder cases.

The field response is part of the declared progression: guided transformation uses radio choices, while full calculation uses an exact answer fragment. Antiderivative questions display +C outside the field so valid constant shifts are accepted. This is an explicitly authored response/scaffolding extension, not a claim to replay the imported answer banks.

The hard bands are a reviewed pedagogical design, not an external psychometric calibration. Imported labels and authored band decisions remain separate in every package's `source-evidence.json` and `band-contract.json`.

## Generator and pipeline changes

[generate/trig_scaffold.py](../../../../generate/trig_scaffold.py) implements the shared v4 model. Each registered package bundles its own immutable copy, formatter, KP evidence and band contract. The four repository entrypoints and local capability files match their registrations.

The sampler chooses a supported case before compatible parameters. Existing and retired mathematical task fingerprints are excluded; the capture normalization now reads all original and generated prompts in these four inventories. It rejects ambiguous choice banks, equivalent options, zero-result padding, and amplitude-only repetition within a delivered batch. Reusing a seed or changing distractor order cannot manufacture a new instance: banks and identities are deterministic for the instance.

The final canonical expression comes from the displayed derivation. Trig operator inputs stay visible. Log differences are retained rather than silently converted into another keyed form. A negative factor explicitly groups the expression it multiplies. Every generated answer belongs to its own field.

The author/reviewer prompts and template-generator instructions now require an account of the support available before feedback, matched-instance band comparisons, controlled prerequisite work, and explicit accounting for changes in response format. Correctness alone cannot establish difficulty calibration.

[The delivery guard](../../../../scripts/trig_substitution_batch_policy.py) checks the actual surviving batch for the v4 contract, supplied support, visible-number budget, exact final-to-key transition, supported target cases and family coverage. It rejects the previous compound hard profiles and legacy v3 records for fresh publication.

## Verification

- **192 sampled records** across two seeds were checked from their actual printed prompts, derivatives, bounds, transformations, integration steps and keys. All 96 surviving delivery records were checked again. The 64 sampled easy banks, each with five choices, were checked for a unique correct answer and mathematical nonduplication.
- A [matched pair](matched-scaffolding-pair.json) holds the integrand and bounds fixed while changing the requested operation from supplied-u transformation to full evaluation.
- Negative controls reject incorrect printed derivatives, oversized visible parameters, missing primitive support, unshown answer conversions and repeated tasks. All original and retired prompts are covered by the normalized exclusion inventory; expanding that normalization did not change the approved candidate/grader/render batches. See [exclusion-normalization-verification.json](exclusion-normalization-verification.json).
- **47 Python regression tests passed**, covering the scaffolding, small-parameter scope, delivery controls, publication and unrelated integration-policy regressions.
- **409 native grader checks passed:** 212 expected accepts and 197 expected rejects, with no unresolved comparisons. These include every radio choice, alternate fraction forms, numeric constants absorbed into external C, and expanded quotient antiderivatives. See the per-KP `grader-verification.json` files and [matched-grader-verification.json](matched-grader-verification.json).
- **18 actual UI previews passed.** Representative guided choices, decreasing bounds, reciprocal/root inputs and quotient rearrangements were visually inspected. See [render/rendering.json](render/rendering.json).
- Every published package was relocated and reproduced its approved 24 records exactly.
- Guarded native previews, exact requests, receipts and readbacks verified all four commits. Old records changed only by the planned retirement flags; unrelated learner and engine facts were unchanged.
- **31 live, read-only grading checks passed** against the running app, including valid expanded answers with integration constants absorbed. See [live-grading-verification.json](live-grading-verification.json).

[live-pool-verification.json](live-pool-verification.json) confirms that each KP has exactly the new 24 active generated questions, that all 91 superseded records are retired, and that local and published code match. Imported questions and their existing classifications were not revised in this repair.

## Retained evidence and recovery

Each KP directory retains its source and inventory snapshots, original entrypoint, approved package, candidate/accepted records, regression samples, exact retirement identities, and publication journal. The previous immutable packages remain in the math store for historical replay.

`deploy.py` reconciles a pending exact request before preparing new intent and recognizes completed deployments. It does not excise content or alter saved learner responses. The earlier unshipped v3.1 root-bound draft is marked superseded; it is not a current registration.
