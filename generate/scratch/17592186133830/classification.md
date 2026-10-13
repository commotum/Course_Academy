# Classification at math basis 1356

Capture provenance: database `math`, basis `1356`, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`; preserved verbatim in `source.json`.

| Original | Actual source rating | Template | Field / bank | Plot rating |
|---|---|---|---|---|
| q-167609 | easy | sum | radio, 5 scalar choices | none |
| q-76434 | easy | reciprocal | radio, 5 scalar choices | none |
| q-167621 | moderate | circle_cos | radio, 5 scalar choices | none |
| q-76433 | moderate | circle_sin | radio, 5 scalar choices | none |
| q-76447 | moderate | cubic | radio, 5 scalar choices | none |
| q-40258 | absent | fractional | radio, 5 scalar choices, no correct ref | none |
| q-41160 | absent | involute | radio, 5 scalar choices, no correct ref | none |

Seven distinct prompt/value/solution templates, each with one complete observed bank. Five source worked solutions exist; two are absent. Canonical e-6308 is analyzed but excluded from these practice counts. No source question is omitted. No assessment prompt, answer, or solution references an image; tutorial and sibling plots do not belong to this KP's assessment templates. No raster transcription or renderer is needed.

Observed source labels and missing attributes are preserved in public `raw_<family>` replay. `completed_fractional` and `completed_involute` separately infer the unique correct answer, author a full worked solution, and assign a supported draft difficulty. They remain evidence-only because their historical scalar banks have opaque intent. They do not turn missing original designations into fidelity matches.

## Curriculum scope and hard extension

The linked lesson route is first-step 17592186134750 (Introduction), then 17592186134751 (General Formula), 17592186134744 (setup KP 133829), 17592186134745 (this evaluation KP), 17592186134740 (substitution KP 133827), and 17592186134741 (derivation). The route follows step/next, not collection order. Captured prerequisites are arc length of vector-valued functions, introduction to integration by parts, and domain of a multivariable function. Canonical e-6308 has f=xy, r=(3t,4t), [0,1], speed5, substituted field12t², and direct power primitive yielding20. It establishes the complete evaluation demand after the setup formula, without a substitution method. The present generator uses elementary differentiation, trig identities, and direct definite-integral primitives already used by the canonical/source questions. It does not invoke integration by parts, substitution, vector work, path-as-function conversion, or qualitative properties as new response demands.

Easy retains constant-speed affine curves and a linear or reciprocal field whose denominator becomes a nonzero constant. Moderate retains the two observed circle identities and observed cubic power evaluation, plus an explicitly assigned unrated fractional curve whose speed becomes s(t+1). Every moderate family directly integrates the resulting elementary integrand. The cubic coefficients remain the familiar 3-4-5 pair with signed orientations and bounds [0,1]; this prevents endpoint powers from creating a large unrelated arithmetic burden.

Hard is authored, not a recovered source label. The involute source anchors cancellation of derivative product-rule terms and cancellation of squared-coordinate cross terms. Normal hard involute questions use c(x²+y²)+d, with both resulting primitive coefficients nonzero, to require separate t² and t⁴ endpoint components. The other hard family uses the observed fractional curve with cx+dy (both coefficients nonzero), requiring the same perfect-square speed and five direct primitive components. These are unordered alternatives at comparable bookkeeping demand; neither introduces a different integration method. The unrated involute completion itself is weaker than the normal hard policy and is explicitly ineligible evidence.
