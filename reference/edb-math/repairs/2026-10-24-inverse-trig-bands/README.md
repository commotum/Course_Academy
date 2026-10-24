# Inverse-trigonometric substitution: generator repair and pool refresh

Published to `math` at **T6401–T6404**, attributed to `:agent/codex`, following the
request to repair the generators, retire old generated questions, and replenish
the pool for topic **17592186048189**.

## Delivered pool

| KP | Easy added | Moderate added | Hard added | Total |
|---|---:|---:|---:|---:|
| Inverse sine — 17592186064218 | 8 | 8 | 8 | 24 |
| Inverse tangent — 17592186064219 | 8 | 8 | 8 | 24 |
| Inverse secant — 17592186064250 | 8 | 8 | 8 | 24 |
| Definite integrals — 17592186064220 | 10 | 10 | 10 | 30 |
| **Total** | **34** | **34** | **34** | **102** |

The live pool check at **T6404** confirmed all 102 additions are active, correctly
associated with their KPs, and have no saved task references. All four current
registrations point to verified immutable packages. The three old generator
entities remain in history; their registration pointers were replaced. The
definite-integral KP previously had no registered generator.

**There were no old generated questions to retire.** The fresh live capture
found 75 imported practice questions: 15 sine, 16 tangent, 17 secant, and 27
definite. Publication checked that fact again. All 75 imports, their complete
answer banks and solutions, and all four canonical examples remain unchanged.
Exact receipt validation confirms no learner or engine-policy facts changed.

The imported improper-endpoint question `q-351834` remains an unchanged import;
it is explicitly excluded as a generation anchor. No generated descendant of
that endpoint family is emitted by the replacement. This refresh does not
retire or relabel imported questions.

## Generator changes

The shared implementation is [generate/inverse_trig.py](../../../../generate/inverse_trig.py).
All four repository entrypoints and their capability records now identify the
replacement; immutable packages include their own exact helper and source
evidence, without a runtime dependency on repository files.

- Coefficients have independent mathematical roles. Numerators, denominator
  constants and inner factors no longer share slots because their source text
  happened to contain the same numeral.
- Batches balance structural cases rather than weighting a family by the number
  of near-identical imported examples. Unit-numerator tangent cases now vary
  their denominator/substitution instead of replaying a single import.
- Bands enforce explicit operation contracts. Sine hard combines nonunit
  constant extraction and a radical inner factor. Tangent hard normalizes both
  nonunit quadratic coefficients. Easy secant follows canonical matching-du
  examples; moderate retains a nonunit prefactor; hard explicitly normalizes
  the absolute-value argument. Trivial normalization cancellations are rejected
  in the authored sine/tangent hard families.
- Definite bands depend on normalization and endpoint work. Hard has both
  nonunit coefficients, an irrational inner factor and two unlike nonzero
  transformed endpoints. Arcsine endpoints must stay strictly inside `(-1,1)`;
  improper endpoint questions are rejected, including explicit parameter calls.
- Solutions show normalization, the differential and reciprocal factor, both
  changed bounds, individual inverse values, and the final simplification.
  Secant explicitly shows `|u|=s|x|` for positive `s` and explains its two domain
  components. Negative inverse-sine endpoint values appear before simplification.
- Complete authored error-recipe banks are checked for equivalent choices.
  Inapplicable reciprocal-endpoint profiles are rejected before sampling. Each
  task deterministically selects its bank; new seeds only reorder options and
  do not create new question identities. Per-family key positions vary.
- Mathematical fingerprints exclude imported/canonical/captured generated tasks
  and duplicates across one batch's bands. Exhausted catalogs fail explicitly.
  Indefinite questions retain radio responses; definite practice includes full
  exact-entry fields and the observed arctangent coefficient/argument shape.
- Long calculations were reflowed after visual inspection exposed clipping.

Sine/tangent hard, secant easy and the consistent definite-hard contract are
**authored compositions of established skills**. No imported hard anchor or
external calibration is claimed where it does not exist. All normal choice
banks are labelled authored; exact source-bank generalization is not claimed.
All 79 practice/canonical source records are retained verbatim as evidence.

## Verification

- Independent printed-math checks passed for **201 records and 2,581 equalities**.
  The checker reconstructs the actual integrands, coefficients, derivatives,
  absolute-value identities, transformed endpoints, derivation rows and answer
  keys without treating generation metadata as mathematical proof. Secant
  comparisons also exercise both real domain components.
- Controlled numerator changes update answers while retaining the substitution.
  Seed-only option changes preserve identities and mathematical content.
  Corrupted printed reciprocal factors, easy work relabelled hard and singular
  endpoints fail the relevant checks.
- All **102** candidates survived the shared delivery filters, with zero
  duplicates. Their printed mathematics was checked again after delivery.
- The actual native `learning::grade_field` passed **117 accepted** and **370
  rejected** submissions, including equivalent exact blank entries, with no
  unresolved outcomes. The harness was linked against the current release engine.
- **14** actual learner-UI cases rendered without raw-TeX, MathJax or asset errors.
  Five screenshots were visually inspected, including normalization, secant,
  negative endpoints, and arctangent fragment entry.
- **Six repository regression tests** passed. `git diff --check` passed.
- Each published relocated package reproduced the approved records and instance
  metadata. Native speculative previews and committed receipts matched the
  exact guarded transaction intent. Readback preserved all existing content.
- The running app's read-only preview passed **16** checks: correct answers in
  every KP/band, plus one incorrect answer per KP. No attempts were saved.

Primary records: [completion.json](completion.json),
[generator-verification.json](generator-verification.json),
[grader-verification.json](grader-verification.json),
[delivery-verification.json](delivery-verification.json),
[live-pool-verification.json](live-pool-verification.json), and
[live-grading-verification.json](live-grading-verification.json).

`publication/<kp>/` archives the exact preparation, native preview, durable
request, receipt, immutable package verification and readback. `deploy.py`
recovers an outstanding request before preparing new work and recognizes
completed publications. `build.py`, `check.py`, `grade.py` and `verify_live.py`
retain the preparation and verification commands. `originals/` preserves the
superseded scripts and local capability/readme documents.
