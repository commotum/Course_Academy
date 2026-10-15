# Replenishment source review

The current source snapshot is retained in `initial/kp.edn` at basis 2612,
lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Final preparation captures its
own basis under the application lock. `source.json`, the generator, extraction,
source replay, full finite-domain validation and freeze manifest remain intact.
The freeze's file hashes all match. It covers nine source families and 45/45
source choices, with 119 independently checked displayed mathematical instances.

The current bank contains ten source practice records: three complete moderate,
five complete hard, and two unrated records without keys or solutions. Each has
one `selection` radio field with five mathematical integral options. The latter
two do not count as current available questions, and are not repaired by this
job. Every original record, including its current formatting repairs, remains
unchanged. Seven existing solutions have already received coordinate-system
TeX repairs since the frozen snapshot. The xy2 source additionally has visible
set braces and replacement radial/angular diagrams. Snapshot comparison permits
only these documented presentation differences; mathematical expressions,
answer values, keys, ratings and identities must agree.

The existing validated generator remains bounded to its documented templates:
four authored constant-integrand easy orientations (20 tasks), three moderate
source families (30 tasks), and six hard source families (60 tasks). Its setup
criterion requires the actual nonnegative-r region and transformed density
with Jacobian. Scalar-zero coincidences in observed banks are separately
reported; new questions state the setup criterion explicitly. No source-bank
fidelity claim is made for the additional family below, which is not added to
the frozen generator. This preserves the validated package while allowing it
to replenish every supported difficulty.

## Additional source family

Source 17592186436974 (`q-161064`), question UUID
`0f9560d7-409d-5ebf-b57a-a19bcb1f8e6e`, is rated moderate. The source asks to
rewrite the integral of `2xy` over `x²+(y+3)²≤9`, a full disk centered at `(0,-3)`.
The generalized backbone is a bilinear Cartesian density on an origin-tangent
full disk centered below the origin, polar circle substitution and factoring,
nonnegative radial bounds, angular bounds, Jacobian and double-angle identity.
The observed radius is 3. It differs from the existing difference template's
Cartesian density and from the linear/x2y families' substitution sequence.

There is one complete observed bank, no extra feedback, five choices. In source
bank order, its exact operations are:

| Choice answer UUID prefix | Angular bounds | Radial bounds | Density | Interpretation |
|---|---|---|---|---|
| 93b12cef | π,2π | 0,−3sinθ | r²cos2θ | half radial scale, missing radial power, cosine identity |
| 98177725 | 0,2π | 0,−6sinθ | r³sin2θ | wrong angular interval, including negative radial upper bound |
| 9d796d42 | π,2π | 0,−6sinθ | r³sin2θ | correct region and Jacobian |
| c0e3648e | 0,2π | 0,3 | r²cos2θ | origin-centered disk, missing radial power, cosine identity |
| d9abcc56 | π,2π | 0,3 | r³sin2θ | constant radial upper bound |

These are observed expressions; compound distractor intent is inferred, not
recovered authoring code. The correct reference points to the third choice.
Substituting `x=r cosθ,y=r sinθ` gives `r(r+6sinθ)=0`, hence `0≤r≤−6sinθ`
for `π≤θ≤2π`. The density becomes `2r³sinθ cosθ=r³sin2θ`.
The solution follows exactly these stages; the validator parses its actual final
integral and every choice and checks the correct designation. The current
native learner grader checks correct and all incorrect radio submissions.

The source has two solution-only plots: a blue filled full disk with Cartesian
axes, radius/center ticks at −3 and −6 and equation label, then a pink radial
arrow and bound `0≤r≤−6sinθ`. Both were visually inspected; the region and ray
agree with the mathematics. New radii in this family would require redrawing
both, giving a moderate plot rating. There are no prompt or choice plots. This
family is classified and contributes to validated inventory, while production
continues through the existing validated generator.

## Validation and publication

Generated tasks are deduplicated against every original setup, including the
two unrated families, by exact decoded radial bounds, transformed density,
angular start modulo 2π, and angular width. New UUIDs, bank changes, option order
and seed changes cannot bypass that comparison. Selected instances replay the
frozen generator exactly and pass its independent displayed-mathematics audit.
Their complete banks are graded using the current engine, compiled locally in
this KP's `reference/native/` directory. Figures are published with the existing
`ImageLibrary` content-addressed store. Stored SHA-256 bytes and the application's
asset path resolver are checked before submission.

The easy contact sheet was inspected across all four orientations. The current
xy2 radial/angular replacements were also inspected: they correctly show the
lower half disk centered left of the origin, `0≤r≤−cosθ` and `π≤θ≤3π/2`.
No production question is changed to match the frozen presentation.

Only additive facts for this KP, new question/field/answer entities and its
registered generator are permitted in the receipt. The exact native preview,
request EDN, request key, lineage, contributor, guarded basis, receipt and
readback are retained under the final `basis-*` directory. The application lock
is held from the fresh inventory read through submission and readback.
