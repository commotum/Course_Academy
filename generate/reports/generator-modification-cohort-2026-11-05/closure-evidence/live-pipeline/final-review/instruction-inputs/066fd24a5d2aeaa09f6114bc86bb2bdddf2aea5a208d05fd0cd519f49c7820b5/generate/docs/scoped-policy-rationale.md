# Why the retained integration controls exist

These controls apply to the named, versioned constructors. They are not universal
laws for a knowledge point or difficulty label. A new construction that preserves
the target learner work may justify a different parameter or response design;
the investigator and verifier must assess that design against target evidence.
They must repair a conflicting shared guard rather than narrow valid mathematics
just to satisfy an old implementation. No imported difficulty label is changed.

The November 5 follow-up audited `trig_substitution_batch_policy.py`,
`inverse_substitution_batch_policy.py`, `substitution_pedagogy_batch_policy.py`,
`integration_batch_policy.py` and its delegated `kp2_integration_policy.py`.
The grouping below covers their correctness, response, domain, workload,
calibration and variation restrictions. The executable controls are in
`tests/test_scoped_generator_constraints.py` and the existing model/policy tests.

| Control | Instructional reason and scope | Case that must survive |
|---|---|---|
| Independent substitution and full evaluation; no supplied primitive or endpoint values | These KPs assess selecting the substitution, accounting for its differential, recalling prerequisites and reaching an antiderivative/value. A transformed-integral endpoint is a different task. | A simpler integrand or complete-answer bank retaining those decisions; task-specific givens that do not supply them. |
| Final worked expression reaches the exact keyed fragment; external `+C` for the existing blank contract | Avoid asking the learner for an unshown conversion or making the grader infer an unrequested constant. This is a response contract, not a ban on equivalent mathematics. | Valid equivalent entries through the native grader; a justified, shown conversion; definite values including zero. |
| Supported primitive/function families and real domains | Keep an inverse-sine, inverse-tangent, inverse-secant or elementary-power task within its target. A logarithmic primitive for power `-1` is not part of the elementary-power constructor. | Function families supported by the target across labels; reciprocal/square-root and ordinary-power trig substitutions in hard where sources show them. |
| Bounded coefficients, familiar powers/angles and real nonsingular definite intervals | Keep incidental arithmetic manageable in these finite constructors. The numeric ceilings describe this sample domain, not the entire mathematical curriculum. Compounding fractional amplitudes, awkward slopes and radical bounds is not needed to manufacture hard. | Canonical trig `2 sin(x/3)`; inverse-sine `9/(4 sqrt(1-9x²))`; inverse-tangent `3/(2+50x²)`; a single familiar radical bound in the product-trig family. |
| Inverse normalization bands | Compare work after simplification. A common factor making a printed large expression direct-standard-form must not be promoted merely because coefficients look large. Easy uses direct familiar scaling, moderate permits bounded denominator/fractional-prefactor normalization, and the current hard constructor uses a genuine remaining normalization or familiar bound demand. This is authored calibration, not an empirical rating. | The old `4/(4+16x²)` case as easy; canonical fractional/ratio normalizations on the ordinary moderate path; no rank, endpoint or small-batch mix quota. |
| Diagnostic inverse banks | Detect omitted differential factors, wrong normalization, primitive/endpoint errors. Copied substitutions and arbitrary numeric offsets must not replace meaningful alternatives. Option-count equality with metadata is integrity, while exactly five alternatives is not required. | A three-choice diagnostic bank; a colliding recipe replaced with another valid bank without excluding the mathematical case. |
| Two/three nonzero power terms, family-specific power patterns and bounded coefficients in the linearity constructors | The targets differ in whether the learner integrates a constant plus a term, combines two scaled terms, or applies linearity to three terms. The named families encode those source-derived tasks; zero terms can remove a required term-level operation. | A small filtered refill containing one supported family; another supported response layout; sign changes that affect calculation, without counting sign-only clones as new structural coverage. |
| Matching power/sign profiles and copied constant contributions in the repaired linearity banks | Earlier complete banks exposed the key through degree, sign or a copied constant before the requested coefficient calculations. These are retained controls for that demonstrated construction defect, not a rule that all mathematical distractors everywhere share signs. | Different plausible wrong coefficients with the same necessary superficial pattern; any valid bank size of at least two with consistent metadata. |
| No duplicate mathematical task/amplitude-only or sign-only clone within the bounded recent fragment | UUID, order or cosmetic changes must not masquerade as fresh learner calculations. | Distinct calculations from a single family, including legitimate cancellation and invariant outcomes when they express the task. |
| Correct contract/version and metadata-to-record agreement | Route the known construction through its corresponding regressions and preserve reproducibility. A version tag alone is not pedagogical evidence. | Legacy published versions remain supported; revised constructors and guards change together with old-failure and valid-neighbor controls. |

Removed requirements have explicit source counterexamples:

- Exponential hard need not have a negative inner derivative: KP
  `17592186184350`, source `q-211992`, has a positive quartic derivative. Its
  canonical `e-14403` also requires fourth-power inner functions. The constructor
  now supports quartics and both signs without adding another operation.
- Product-trig hard need not use reciprocal/square-root inner recognition:
  `q-13467` and `q-13470` use ordinary powers. Familiar transformed bounds occur
  in `q-13533` and `q-13537`; the constructor includes those families without
  stacking them with reciprocal/radical inner recognition.
- Quotient-trig hard need not add nesting or rearrangement: `q-113998` is a
  direct logarithmic-derivative case. Those source families remain available.
- Exponential “More Complex Cases” hard need not introduce a composite numerator:
  `q-31478` is `5^x/(5^x+1)`. Definite exponential practice also retains the power
  family of canonical `e-14407`, alongside the supported logarithmic family.
- Inverse canonical examples `e-470` and `e-471` require the modest fractional
  prefactor and common-ratio normalizations above. The ordinary generator now
  supports them before the separate exclusion of already imported/served tasks.
- Exactly five options, every-family refill fragments, per-batch answer-rank
  balance and a negative-sign definition of hard are not required. The delegated
  KP2 guard's two-record rank/position observations are diagnostics, not automatic
  publication failures. A real construction invariant or usable finite-pool cue
  still requires investigation and an applicable retained regression.

The source passages are retained under
`reference/edb-math/repairs/2026-10-25-restore-substitution-recognition/<kp>/source.json`
and `2026-10-25-inverse-bank-balance/<kp>/fresh-source/source.json`. Linearity
source cases are under
`reference/mathacademy/repairs/2026-10-20-integration-lesson-quality/<kp>/package/source-cases.json`.
Captured labels support the specific counterexamples above; they do not establish
calibration of every newly authored numerical instance.
