# 6. Template generator

Implement [the extracted task](4-template-extraction.md) under [the current principles](../principles.md). For pipeline jobs use the supplied workspace, source capture and manifest contract; a manual draft may start at `generate/scratch/<knowledge-point-db-id>.py`. Read only applicable [task-specific checks](topic-checks.md) and [presentation checks](presentation-checks.md). These references do not redefine the target operation.

## Construct the instance and bank

1. State the target operation, required prerequisite recall, supplied information and response endpoint. Define supported variable slots and justify task-relevant fixed features.
2. Design eligible answer-bearing roles or rule cases before incidental values where the mathematics permits it. Use seeded sampling and one source of instance data for targets, labels, parameters and relationships.
3. Build the ordered learner derivation, then derive prompt, key, intermediate values, choices, solution and plot data from that instance. Use exact arithmetic/SymPy as a separate verifier; render the intended mathematical form rather than an unrelated CAS normal form.
4. For fresh choice practice, construct a valid, plausible bank that requires the target work. Reuse a source profile only while its recipes remain useful and valid. If recipes collide or expose the key, try a repaired or authored bank before excluding a valid mathematical case. Record its source relationship and construction for reproducibility. Blanks retain only the canonical answer for the exact requested fragment.
5. Render the prompt, supplied notation and one concrete worked solution, independent of the learner’s chosen answer. Only `blank` and `select` fields use `{{key}}` placeholders; radio, checkbox and free controls render separately. A radio question’s missing formula component can be shown as `?`. Derive all changed references and conditional grammar from the instance.
6. Use [plot generation](7-plot-generator.md) when assets vary, or reuse unchanged assets. Parameter-dependent images use the same instance, not a second random draw.
7. Expose seeded generation and replay by difficulty/template. Build easy, moderate and hard together, preserving observed labels separately from authored calibration. Missing source bands do not authorize rejection; genuine finite limits use the contract below.

Keep scope and workload comparable within a band. Do not introduce operators, response demands or extra solution stages merely to increase variety or separate difficulty labels. A response change needed to repair a defective bank must be justified and reflected in progression evidence. Follow [the principles’ difficulty and support rules](../principles.md#independent-practice-and-difficulty); an extra hard-stage requirement is not part of this guide.

## Source replay and ordinary coverage

Retain every usable eligible source case, original parameters, complete field/bank and source ID for replay evidence. Map original incorrect choices to observed expressions or operation recipes, marking unknown interpretations honestly. Exact replay ignores option order but preserves choice count and designations; compare whole equations under valid nonzero rescaling, with domains and branches. Keep mathematical equivalence, rendered notation and solution-layout claims separate.

Report matched/total usable banks and every missing or extra option. Preserve raw evidence for defective or incomplete sources with its documented correction or limitation; do not invent unavailable original fields, serve source errors, or block sound new practice merely to repair imports. An authored replacement bank or response format is not exact replay.

Compare representative source anchors with the ordinary sampler and delivery path. A replay-only branch does not establish normal learner-work coverage, but every imported number or bank need not be randomly reachable. Test eligible target changes with other data fixed, relevant role/branch boundaries and cases lost by rejection or deduplication. A validator enforces a slot’s mathematical role rather than its original example value.

## Response integrity

Use existing question/field/answer representations and field-owned answer identities. Math answer values are bare TeX; prompt notation defines the requested blank fragment. For an existing record’s typography repair preserve its identities; distinct generated content gets content-derived identities. Record version, dependencies, seed, mathematical parameters, domains and source references separately. Option shuffling, aliases and unused parameters do not create new assessed tasks.

Each checkbox must display its complete selectable statement or object. An empty correct subset is valid: include “If none apply, leave all boxes unchecked.” and submit the owned false answer for every unchecked field. Missing responses remain incomplete. Do not add a separate None checkbox solely to represent the empty subset. Preserve every original answer bank in raw source replay; fresh practice may express its None answer as the equivalent empty subset. The optional `nonempty_checkbox` sampler in `scripts/generator_policy.py` can restrict a particular family when intended, but nonempty selection is not an application-wide requirement.

Exclude empty-correct variants from normal sampling, explicit parameter calls and finite catalogs under the current contract. Do not silently invent None to rescue them or change historical responses. Coverage obligations respect these admissible cases. If this excludes an important target decision, document the concrete case for a product decision rather than weakening the guard or claiming complete coverage. Any separately authorized response migration must preserve the learner’s selected subset, grades and history.

## Runtime package

Use one seeded Python entrypoint accepting `--difficulty`, `--count`, `--seed` and `--format json`. Keep assets under `COURSE_ACADEMY_GENERATOR_OUTPUT_DIR`, not the immutable package. The runtime cannot write database content or depend on repository ancestors, hard-coded scratch paths or undeclared files. Bundle local helpers, data, fonts and renderers that affect output. Standard-library and declared installed third-party dependencies are allowed.

Write `package.json` with relative `entrypoint`, runtime `files` and `dependencies`. Example dependency shape: `{"python":"3.13.5","packages":{"sympy":"1.14.0","matplotlib":"3.11.2"}}`; inspect and declare actual exact versions, without ranges or `==`. For standard-library-only code `packages` is `{}`. Include a pinned requirements file when needed. Do not list logs, evidence, generated outputs or package.json itself as runtime files. The runner does not install dependencies.

A genuinely finite family may declare runtime `generation-limits.json` in `package.json.files`: `{"format":"course-academy-generator-limits-v1","maximum_distinct_batch":{"easy":4}}`. Use positive integer bounds and easy/moderate/hard keys; omit unrestricted bands. Justify the bound by distinct learner decisions/calculations. The runner caps requested batch counts; the CLI returns exactly the capped count and rejects direct over-capacity calls. All three bands still require verification. A per-batch bound alone is not proof that the unseen catalog is exhausted.

Test relocation outside the repository, such as a disposable `/tmp` copy, with the ordinary environment and a different output directory. Compare question/field/answer identities and asset bytes. Test installed entrypoints through the runner’s publication verification; do not publish independently to perform a check.

A complete finite domain may additionally use `finite_catalogs` mapping each bounded
band to a declared runtime JSON list of generated records. The runner can report
`finite-limit` only when that complete supported catalog is in inventory, not from
an empty random sample. New approvals require package-bound `refill-review-plan.json`:
applicable inexpensive survivor checks or explicit source/evidence-backed
nonapplicability. Map every retained generator finding to an immutable check or
justified exemption. Applicable `refill-validation.json` checks run in a declared-file-only
temporary copy on actual delivery survivors before approval and during later
refills, with normalized usable inventory content available for population checks.
Use [the exact plan/checker interface](../README.md#refill-checks-and-finite-domains).
Retain semantic/equivalence/cue regressions so fresh seeds exercise approved
behavior without another LLM review. Do not impose population coverage quotas on
each small refill fragment or invent generic wrong responses. Existing approved
packages remain compatible with explicitly reported native fallback.

## Verification and delivery

Run independent math, source replay, native grading, actual-UI presentation, meaningful coverage and deterministic/relocation checks. Use [shared validation tools](../pipeline/validation-tools.md), not homemade grader/render stacks. Test valid equivalents and plausible wrong responses, respecting legitimate response-form and precision requirements. An unresolved valid response is an unresolved limitation, not a positive grading pass.

Inspect the path from printed givens through displayed solution to keyed answer/blank fragment. Record necessary conversions and their taught or documented in-scope justification. When representation-changing construction or normalization is present, retain a relevant negative control that is algebraically equivalent but violates the shown/taught path. If none is applicable, explain that fact and test the actual response dependency instead; do not manufacture an unrelated trig/log example. Keep every relevant historical conversion regression.

Use controlled counterfactuals and conditional shortcut probes under [the evidence standard](../principles.md#meaningful-variation-and-shortcut-evidence). Fixed-bank counterfactuals test correctness dependencies; they do not themselves establish practice variety. Test the ordinary short batch for repeated main work and incidental cues. Preserve valid cancellation and finite instructional outcomes; avoid arbitrary balance quotas and post-hoc overclaims.

Inspect records surviving generator rejection, publication normalization/deduplication, difficulty filtering and applicable learner selection. `check_delivery.py` provides the actual publication filtering; state what it does not cover and the captured-basis limitations. Do not transact to test delivery. Save reproducible commands, records and results, and report fidelity, correctness, grading, scope, progression and decision variation separately. Keep useful prior evidence and rerun affected checks rather than repeating unrelated exhaustive audits. Pass the validated package and records to the runner’s [database preparation](8-database-prep.md).
