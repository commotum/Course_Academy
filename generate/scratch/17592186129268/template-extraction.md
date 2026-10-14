# Template extraction

## 1. Specific observations before generalization

q-161521: full disk centered(0,-3), radius3, lower0, upper2+x²+y², integrandxy. Five flattened integral options use π≤θ≤2π. No worked solution, difficulty or correct reference. Its source screenshot establishes superscripts in the flattened expressions. Every displayed interpreted integral has value0, so a structural setup distinction cannot establish a unique answer to the requested equivalent integral.

q-161523: disk centered(1,0), radius1 clipped by y≥0, heights1 and2, integrandx²+y². No worked solution/difficulty/correct designation. The correct structure is θ∈[0,π/2], r∈[0,2cosθ], integrandr³; the negative-sine radial option also has complete value3π/4. The raw bank is ambiguous even though its negative radial interval does not describe the intended region.

q-161630: moderate full left disk centered(-3,0), radius3, lower-8, upperx+2, integrand1/sqrt(x²+y²+1). It has full six-row circle algebra; full integral substitution → grouped radial reciprocal → final definite integral. Correct designated option is the last EDB bank entry. Wrong options3 and4 have equal complete values by sine/cosine symmetry. Their equality is not correct-answer equivalence, but still violates bank uniqueness.

q-161636: hard lower half of right disk centered(3,0), radius3, lowerz=y, upper6, integrand1/sqrt(z+1). Six-row circle chain contains an erroneous substituted-square RHS3 in its second row while all other rows use9. Also y reaches-3, so z+1 is negative on an open part of the region: the requested real integral is undefined there. The normal solution uses RHSa², and normal parameters require C>a in1/sqrt(z+C). Raw evidence preserves both errors. The integrand retains z; it is not translated to a shifted coordinate system.

q-161633: hard left half of upper disk centered(0,2), radius2, lower-2, uppersqrt(16-x²-y²), integrand2xy. Six-row y-shift circle chain. Final double-angle collection r³sin2θ follows actual complete product2(r cosθ)(r sinθ)r. Correct bank option2 equals option5 under θ↦3π/2−θ; options3 and4 both have complete value0. The source bank is ambiguous.

q-161637: hard right half of upper disk centered(0,4), radius4, lower-5, upperx, integrandsqrt(x²+y²+1). Three integrand stages: full substitution, grouped trigonometric squares and finalr sqrt(r²+1). Its complete bank is distinct, supported by independent quadrature and normal output tests, and is the default bank for this family.

Decoded-byte inspection found zero adjacent backslash pairs in every first source answer, actual U+2061 function application characters and no literal backslash-u2061 sequences. The apparent doubled escapes in serialized tool output were not a source defect. Real legacy presentation issues are flattened powers/function typography and unescaped set braces. Normal TeX uses grouped superscripts, standard functions and visible escaped braces; raw evidence remains exact.

## 2. Shared pattern

The projected disk is tangent to the origin, centered on one signed coordinate axis. From(x−cx)²+(y−cy)²=a² with cx²+cy²=a², substitutionx=r cosθ,y=r sinθ gives r²−2r(cx cosθ+cy sinθ)=0. The disk has0≤r≤2(cx cosθ+cy sinθ), restricted to the appropriate half-turn or quarter-turn. Substitute all Cartesian components of both surfaces and the integrand, multiply by the Jacobianr, and express the complete dz dr dθ integral. No integral evaluation is requested from the learner.

## 3. Components and complete banks

Let c=(α,β,R,l,h,f) denote the correct cylindrical bounds and integrand including J. `source.json` preserves every exact option value/UUID. `source-cases.json` supplies every family's original parameter/profile recipe. The order below is captured EDB bank order, not screenshot label order. Every expression is rendered parametrically; no option is copied by final scalar lookup.

| Source | Complete bank operations, in EDB order | Original designation |
|---|---|---|
| q-161521 | c; R=a,h=H+r; R=2a cosθ; R=a,h=H+r,f=f/r; f=f/r | absent |
| q-161523 | β=π,f=r²; R=a cosθ,f=r²; β=π,R=−a cosθ; c; R=−2a sinθ | absent |
| q-161630 | f=f/r; R=−2a sinθ,h=r sinθ+H,f=f/r; R=−2a sinθ; h=r sinθ+H; c | index5 |
| q-161636 | c; f=f/r; R=−2a sinθ,f=f/r; l=r cosθ; R=−2a sinθ,l=r cosθ | index1 |
| q-161633 | f=f/r; c; β=3π/2,R=−2a cosθ,f=f/r; β=3π/2; R=−2a cosθ | index2 |
| q-161637 | β=π,h=r sinθ,f=f/r; c; h=r sinθ; f=f/r; β=π | index2 |

Default method bank for lower_xy: c; x→y with J; x→y without J; y→x with J; y→x without J. Correct value0 arises from odd-in-x symmetry; the four incorrect objects are positive substitution errors and are verified mutually unequal. Its finite domain is a=1..5,H=1..5.

Default method bank for upper_square, left_inverse, lower_zinverse and left_xy_sphere: c; omit J; duplicate J; forget the doubled radial upper bound; reverse dz orientation. These are complete operations on the printed setup, not arbitrary final-value perturbations. The whole bank is selected before parameters; every member is required and the whole instance is rejected on collision/non-real evaluation. right_radical defaults to its valid complete observed operation bank; authored:method remains explicit.

Every source family has shared prose and an operative solution recipe. Normal output retains the initial change-of-variables formula, coordinates, projection, cylinder and surface description, full six-stage circle derivation, radial bound sentence, polar-domain set, and each family's original integrand substitution/grouping/final integral sequence. Upper_square and lower_xy normal worked solutions are authored because sources have none. Minimal normal changes include explicit setup-request wording/field placeholder, set-brace typography, source circle RHS repair, real-kernel guard, standard TeX and removal of redundant z=L=L descriptions when applicable. These are reported as presentation/mathematical repairs, not raw-exact solution claims.

## 4. Reusable masks and domains

Public observed:<q-id> uses captured complete strings as masks with independent radius/squared-radius/doubled-radius and surface/kernel slots. Powers and fixed angle fractions are protected before numerical slots. The same API supports changed parameters and retains missing raw attributes. Changing seed/option order preserves content identity; altered displayed bank/prompt/solution changes it. Field-owned answer UUIDs are derived from full content, with correct refs remapped to those UUIDs.

| Normal family | Domains | Equal-workload reasoning |
|---|---|---|
| upper_square easy | a1..5; L0..4; H−L1..5 | quarter angular restriction, constant surfaces, radial quadratic reduction |
| lower_xy moderate | a1..5; H1..5 | full shifted disk, quadratic roof, complete product xy substitution |
| left_inverse moderate | a1..5; H1..5; C1..5; H−2a−L1..5 | full left disk, affine roof, reciprocal radial grouping |
| lower_zinverse hard | a1..5; H1..10; C−a1..5 | half shifted disk, variable lower surface, z-dependent reciprocal retained |
| left_xy_sphere hard | a1..5; −L1..5; K=(2a+j)²,j0..2 | half shifted disk, spherical roof, product and double-angle collection |
| right_radical hard | a1..5; −L1..5; C1..5 | half shifted disk, affine roof, radial square-root grouping |

These small integer/perfect-square forms match the source/canonical workload. Bounds apply identically to explicit calls and sampling; invalid explicit inputs never silently change. Normal real-domain z-kernel and sphere restrictions are mathematical source repairs, not difficulty inventions.

Meaningful candidate tasks before complete-bank rejection: easy25, moderate150, hard450. Easy lower/upper common vertical offset does not inflate its25 tasks; left_inverse common canceled vertical offset is likewise excluded, leaving125 rather than625 tasks. Bank/profile aliases, layouts and seed shuffles are excluded. Mathematical fingerprints retain actual family/assessed components, separate from presentation identity. These are finite candidate-domain counts; runtime bank eligibility can reduce them and no claim of unlimited variety is made.

Symbolic source ambiguity proofs: all lower_xy original options integrate an odd trigonometric product over a symmetric half-turn, hence0. For upper_square, the r³ primitive makes ±sine/cosine radial bounds contribute fourth powers with equal quarter-turn integrals. For left_inverse options3/4, variable-height terms cancel by reflection and the remaining(H−L) weighted integrals ofsqrt(4a²sin²θ+C) andsqrt(4a²cos²θ+C) over a half-turn agree. For left_xy_sphere, θ↦3π/2−θ exchanges sinθ and−cosθ while preserving sin2θ; the full roof depends only onr, giving equality of correct/option5. Full-turn extensions also create two zero choices. These claims concern complete integrals, not merely bound syntax.
