# Template extraction (step 4)

## 1. Specific originals

The exact prompts, all scalar choices, field types, correct designations, shared solution sentences, ordered derivative/norm/integration/evaluation stages and image references are retained without loss in `source.json` and reproduced in `review.md`. The inventory below describes each original before generalization. All intervals are increasing and every answer is exact; no rounding requirement exists.

- **q-77065**: Cubic/quadratic, directly completed square. Curve `(t**3 - 3*t, 3*t**2)`, interval `[1,2]`, simplified speed `3*t**2 + 3`. The response is an entire scalar length, not an integral setup or missing fragment. The source contains 12 aligned equality rows.
- **q-77066**: Fractional-power/linear, affine radical integral. Curve `(2*t**(3/2), 3*t)`, interval `[0,3]`, simplified speed `3*sqrt(t + 1)`. The response is an entire scalar length, not an integral setup or missing fragment. The source contains 11 aligned equality rows.
- **q-127573**: Exponential spiral, product rules and cross-term cancellation. Curve `(exp(t)*cos(t), exp(t)*sin(t))`, interval `[0,pi/2]`, simplified speed `sqrt(2)*exp(t)`. The response is an entire scalar length, not an integral setup or missing fragment. The source contains 13 aligned equality rows.
- **q-127585**: Reflected cubic/quadratic, factored square and signed endpoint arithmetic. Curve `(-t**3 + 3*t, 3*t**2)`, interval `[-1,1]`, simplified speed `3*t**2 + 3`. The response is an entire scalar length, not an integral setup or missing fragment. The source contains 16 aligned equality rows.
- **q-127602**: Linear/nested power, chain rule and completed square. Curve `(t, (t**2 + 2)**(3/2)/3)`, interval `[-1,2]`, simplified speed `t**2 + 1`. The response is an entire scalar length, not an integral setup or missing fragment. The source contains 13 aligned equality rows.
- **q-77068**: Logarithmic/quadratic, reciprocal completed square. Curve `(-t**2/2 + log(t), 2*t)`, interval `[1,E]`, simplified speed `t + 1/t`. The response is an entire scalar length, not an integral setup or missing fragment. The source contains 13 aligned equality rows.
- **q-77070**: Trigonometric involute, product-rule cancellation. Curve `(t*sin(t) + cos(t), t*cos(t) - sin(t))`, interval `[0,2]`, simplified speed `t`. The response is an entire scalar length, not an integral setup or missing fragment. The source contains 10 aligned equality rows.
- **q-77219**: Linear/reciprocal cubic, factored reciprocal square. Curve `(6*t, -t**3 - 3/t)`, interval `[1,3]`, simplified speed `3*t**2 + 3/t**2`. The response is an entire scalar length, not an integral setup or missing fragment. The source contains 14 aligned equality rows.
- **q-77220**: Double-angle involute, product/chain cancellation. Curve `(2*t*sin(2*t) + cos(2*t), -2*t*cos(2*t) + sin(2*t))`, interval `[1,2]`, simplified speed `4*t`. The response is an entire scalar length, not an integral setup or missing fragment. The source contains 11 aligned equality rows.
- **q-77072**: Cubic/quadratic, nonnegative-t radical substitution. Curve `(7 - 2*t**3, 3*t**2 + 10)`, interval `[0,sqrt(3)]`, simplified speed `6*t*sqrt(t**2 + 1)`. The response is an entire scalar length, not an integral setup or missing fragment. The source contains 14 aligned equality rows.

## 2. Shared instructional pattern

Differentiate both planar coordinates, form the Euclidean norm, retain the source's distributed cross terms and ordered simplifications, establish the sign needed to remove the norm square root, and integrate that positive speed over the displayed interval. A fixed worked solution applies to every chosen option. Involute families cancel product-rule terms; exponential spirals cancel opposite norm cross terms; polynomial/reciprocal pairs complete positive squares; radical curves use the source elementary substitution. These are observations, not inferred source authoring code.

## 3. Components and complete bank mapping

Each observed profile is the complete bank displayed together, with5members and4wrong values. A scalar value generally cannot identify its error operation. Consequently the only asserted extension for an observed bank is the justified homothety operation **H_c(v)=c·v**, with the same positive multiplier applied to the entire curve, every derivative vector, every norm and every explicit base-integrand/evaluation node (the symbolic displayed-curve norm integral already includesc). This operation exactly reproduces all original options atc=1 and preserves their inequalities for every admissible positivec. Distractor intent remains unresolved, explicitly; these banks are replay profiles, not claimed recovered error recipes or the default learner bank. Correctness is recomputed from the curve, never read from the correct option.

### q-77065: `observed:q-77065`, field `selection`

| Source answer ID | Exact original scalar | Designation | Parameterized recipe |
|---|---|---|---|
| 75e5fa3c-091c-520e-8479-d218155399c2 | $14$ | wrong; intent unresolved | H_c(14) / observed_homothety:0 |
| 8b51d751-2961-50bb-98bc-c99dea65a8e5 | $18$ | wrong; intent unresolved | H_c(18) / observed_homothety:1 |
| 8baa903e-69cf-5fab-bf1d-52f2ba066f34 | $10$ | correct | H_c(10) / observed_homothety:2 |
| c0402a4e-bae1-581e-b109-bffe3d5de024 | $21$ | wrong; intent unresolved | H_c(21) / observed_homothety:3 |
| deebeadd-1734-5b4a-bc84-8d64bed65493 | $15$ | wrong; intent unresolved | H_c(15) / observed_homothety:4 |

### q-77066: `observed:q-77066`, field `selection`

| Source answer ID | Exact original scalar | Designation | Parameterized recipe |
|---|---|---|---|
| 42dd07b3-4065-530a-88aa-6e7a0aca511d | $16$ | wrong; intent unresolved | H_c(16) / observed_homothety:0 |
| 78d7838b-fe95-5cad-a4c4-269d7bdb904b | $18$ | wrong; intent unresolved | H_c(18) / observed_homothety:1 |
| 881ebcca-4863-55f5-9890-dcd0a9df648a | $12$ | wrong; intent unresolved | H_c(12) / observed_homothety:2 |
| 8eab15db-b045-510e-8571-aaaaa67b97ca | $14$ | correct | H_c(14) / observed_homothety:3 |
| fee32fe0-e17a-5ba1-bc6c-a8f5d62a18d5 | $10$ | wrong; intent unresolved | H_c(10) / observed_homothety:4 |

### q-127573: `observed:q-127573`, field `selection`

| Source answer ID | Exact original scalar | Designation | Parameterized recipe |
|---|---|---|---|
| 094b9b5d-90a5-52e6-ad22-1226b75da63c | $\sqrt{2}{e}^{\pi }-1$ | wrong; intent unresolved | H_c(\sqrt{2}{e}^{\pi }-1) / observed_homothety:0 |
| 4077f389-0099-57f1-8340-852121cc2cb5 | $2({e}^{\pi }-1)$ | wrong; intent unresolved | H_c(2({e}^{\pi }-1)) / observed_homothety:1 |
| 6c320932-603e-58a3-a9fc-86f6548e4a8b | $\sqrt{2}({e}^{\pi /2}-1)$ | correct | H_c(\sqrt{2}({e}^{\pi /2}-1)) / observed_homothety:2 |
| 87a3a0e9-f0fa-50c2-9617-655e6d9e094e | $2{e}^{\pi /2}$ | wrong; intent unresolved | H_c(2{e}^{\pi /2}) / observed_homothety:3 |
| f7a2e11f-134c-5105-9358-e819e1684bb1 | $\sqrt{2}{e}^{\pi /2}$ | wrong; intent unresolved | H_c(\sqrt{2}{e}^{\pi /2}) / observed_homothety:4 |

### q-127585: `observed:q-127585`, field `selection`

| Source answer ID | Exact original scalar | Designation | Parameterized recipe |
|---|---|---|---|
| 645b7b78-a1b2-5fca-b90e-39d47899cd92 | $4$ | wrong; intent unresolved | H_c(4) / observed_homothety:0 |
| 88e591c2-1771-5bd4-9969-13cd8f27d0ba | $4\sqrt{2}$ | wrong; intent unresolved | H_c(4\sqrt{2}) / observed_homothety:1 |
| b7f29c98-2b8a-5e10-afa8-61e4c808e5dd | $6$ | wrong; intent unresolved | H_c(6) / observed_homothety:2 |
| c6d54c34-a83c-514e-812b-09d754b2eef3 | $8$ | correct | H_c(8) / observed_homothety:3 |
| ccd06f32-fb58-584a-a752-9e7577253c10 | $3\sqrt{2}$ | wrong; intent unresolved | H_c(3\sqrt{2}) / observed_homothety:4 |

### q-127602: `observed:q-127602`, field `selection`

| Source answer ID | Exact original scalar | Designation | Parameterized recipe |
|---|---|---|---|
| 33362404-a630-58e0-ab60-b015a97a07bb | $\frac{16}{3}$ | wrong; intent unresolved | H_c(\frac{16}{3}) / observed_homothety:0 |
| 8b9f6888-780f-56da-9b96-be6ea61dfe14 | $4$ | wrong; intent unresolved | H_c(4) / observed_homothety:1 |
| b0b610b3-0649-5a84-aede-f6eaefb07746 | $8$ | wrong; intent unresolved | H_c(8) / observed_homothety:2 |
| d2902a59-e5b1-5475-92d3-40644cd440c0 | $6$ | correct | H_c(6) / observed_homothety:3 |
| d811aa28-4287-58e1-aa7e-780dedbda6bd | $\frac{11}{3}$ | wrong; intent unresolved | H_c(\frac{11}{3}) / observed_homothety:4 |

### q-77068: `observed:q-77068`, field `selection`

| Source answer ID | Exact original scalar | Designation | Parameterized recipe |
|---|---|---|---|
| 025cfcf4-6c89-537a-b8b1-2e525bd5c2da | $\frac{1}{{e}^{2}}+{e}^{2}-2$ | wrong; intent unresolved | H_c(\frac{1}{{e}^{2}}+{e}^{2}-2) / observed_homothety:0 |
| 18941e5d-726d-59b5-9e31-2ef48340a842 | $\frac{{e}^{2}}{2}$ | wrong; intent unresolved | H_c(\frac{{e}^{2}}{2}) / observed_homothety:1 |
| 47398ece-73e5-5c09-a241-0a1c111f3b99 | $\frac{{e}^{2}+1}{2}$ | correct | H_c(\frac{{e}^{2}+1}{2}) / observed_homothety:2 |
| b22dcc61-309a-5bea-8c94-67c83b72f6a5 | $\frac{{e}^{2}-1}{2}$ | wrong; intent unresolved | H_c(\frac{{e}^{2}-1}{2}) / observed_homothety:3 |
| b5dd1c31-05b4-597a-8db3-8c5b0a9b8a55 | ${e}^{2}+1$ | wrong; intent unresolved | H_c({e}^{2}+1) / observed_homothety:4 |

### q-77070: `observed:q-77070`, field `selection`

| Source answer ID | Exact original scalar | Designation | Parameterized recipe |
|---|---|---|---|
| 417d6dbd-2ce0-543a-b867-66f46ac5a28b | $1$ | wrong; intent unresolved | H_c(1) / observed_homothety:0 |
| 4af00b12-c488-528b-8d8e-a83c42ba6f9c | $2$ | correct | H_c(2) / observed_homothety:1 |
| 6b6338b2-dd43-5df9-9664-ecfbf4ec9d9b | $6$ | wrong; intent unresolved | H_c(6) / observed_homothety:2 |
| e29b77b4-101f-5781-976e-2efc7b315a07 | $8$ | wrong; intent unresolved | H_c(8) / observed_homothety:3 |
| f9e5b481-08c2-5c6e-93f4-60c15385b21b | $4$ | wrong; intent unresolved | H_c(4) / observed_homothety:4 |

### q-77219: `observed:q-77219`, field `selection`

| Source answer ID | Exact original scalar | Designation | Parameterized recipe |
|---|---|---|---|
| 1a04d171-7f37-5d9d-a2f8-61194e6e93c4 | $28$ | correct | H_c(28) / observed_homothety:0 |
| 2dbc28ff-5d76-56ae-8ecf-64a2fdcb3e2b | $18$ | wrong; intent unresolved | H_c(18) / observed_homothety:1 |
| a4e002a4-bd25-5f07-8e74-c15da484745e | $56$ | wrong; intent unresolved | H_c(56) / observed_homothety:2 |
| b2aa47f5-56ab-5309-a1ff-ddb6c0030709 | $32$ | wrong; intent unresolved | H_c(32) / observed_homothety:3 |
| c97a2a57-f756-5bf4-8ca0-819491201663 | $24$ | wrong; intent unresolved | H_c(24) / observed_homothety:4 |

### q-77220: `observed:q-77220`, field `selection`

| Source answer ID | Exact original scalar | Designation | Parameterized recipe |
|---|---|---|---|
| 0ffe2816-aae7-59ca-9562-412dd652a6c7 | $6$ | correct | H_c(6) / observed_homothety:0 |
| 2bb81157-2ab8-5ec8-a9fa-335547e6606a | $9$ | wrong; intent unresolved | H_c(9) / observed_homothety:1 |
| 519f8d58-aa96-5048-9d82-8885955e1cd1 | $10$ | wrong; intent unresolved | H_c(10) / observed_homothety:2 |
| 5ee0276d-41f4-5591-b923-85e85120cdc9 | $8$ | wrong; intent unresolved | H_c(8) / observed_homothety:3 |
| 988c1583-846c-502f-b92b-7cb927f59f72 | $7$ | wrong; intent unresolved | H_c(7) / observed_homothety:4 |

### q-77072: `observed:q-77072`, field `selection`

| Source answer ID | Exact original scalar | Designation | Parameterized recipe |
|---|---|---|---|
| 4ed9d04a-f96a-5183-9fc4-8dcfd77061e7 | $16$ | wrong; intent unresolved | H_c(16) / observed_homothety:0 |
| 56a2e6b5-5884-5570-aa94-176a32aa11de | $10$ | wrong; intent unresolved | H_c(10) / observed_homothety:1 |
| 6e1ffe30-2504-50cd-8a45-20ca6353d983 | $18$ | wrong; intent unresolved | H_c(18) / observed_homothety:2 |
| 9778e0bb-2590-5c24-908d-c9bf4daf3a54 | $8$ | wrong; intent unresolved | H_c(8) / observed_homothety:3 |
| da2916dc-97c4-51c9-852e-307c5a102816 | $14$ | correct | H_c(14) / observed_homothety:4 |


The separate authored default is chosen as a whole eligible operation bank before computing/rejecting members: `[L,2L,L/2,∫||r'||²dt,||r(b)−r(a)||]`, corresponding to correct arc length, double traversal, halved antiderivative, omitted norm square root, and endpoint chord. All are derived mathematical operations and positive lengths; no unrelated numerical perturbation appears. For the symmetric cubic source family the chord equalsL/2 identically, so that family selects the separately declared complete bank `[L,2L,L/2,∫||r'||²dt,c∫3t²dt]` (omitted constant speed term) before checking collisions. There is no first-valid recipe pool or repair of sampled bad members. A nonpositive, non-real or coincident member rejects the whole instance; explicit bad parameters fail rather than silently resample.

## 4. Reusable masks and constraints

Observed families use a positive integer homothetyc in1..12; original intervals are retained, including signed endpoints, e,π/2 and√3. This deliberately bounded parameter space yields60 parameterized tasks per observed difficulty across5families. The multiplier changes the derivative magnitude and final length, so it is a substantive assessed parameter; translations/reflections with unchanged length are not added to inflate variety. One c=1 case per source is available through the ordinary parameter/profile API. Every source-specific mathematical block is compiled into ordered, complete-component masks; the factorc applies to explicit base-function mathematical nodes rather than substituting short tokens. Generic `L=∫||g′(t)||dt` nodes remain unscaled because the displayed g already includesc; the validator independently integrates their actual printed-curve norm. Coefficientone is uniformly omitted. The original rows remain structurally present, especially q-127585's8integration/evaluation rows and q-77072's separate6-rowu-substitution block. No source-payload return branch exists.

Hard exponential: `r(t)=<c exp(kt) cos(qt),c exp(kt) sin(qt)>`, c1..12,k2..3,q1..3 withq≠k, and integer0≤a<b≤2. Nonzero unequal rates force both product and chain coefficients while preserving positive speed `c√(k²+q²)exp(kt)` and elementary exponential integration. Hard affine reciprocal: `u=kt+d`, `r=<2cu,−c/u−cu³/3>`, c1..12,k2..3,d1..2,a=0,b=1, guaranteeingu>0. Speed is `ck(u⁻²+u²)`; changing tou uses the source power-rule integration branch. Explicit input guards enforce these bounds as strictly as samplers. These are alternatives at the same intended hard level, not successive tasks.

Presentation identity hashes generator version, prompt mask, fixed worked solution, complete displayed bank, designated value, full parameters/domain and curve data. UUIDs are field-owned and stable across option shuffling/seed. Task fingerprints hash the simplified positive speed, interval and reasoning family, excluding banks/profiles, incidental translations and option order. Cubic/nested-power tasks with the same positive quadratic speed use the same reasoning tag. Parameterization is assessed through speed and interval; the plot is contextual, not a plotted-locus response.

### Source defects and supported repairs

- **q-77220 worked norm stage:** raw `16t²cos²(t)+16t²sin²` loses the double-angle argument and the second argument entirely. Independently differentiating the printed curve gives`<4tcos(2t),4tsin(2t)>`; the minimal repair is`16t²cos²(2t)+16t²sin²(2t)`. Raw evidence remains unchanged. Raw complete solution fidelity is9/10; repaired complete solution fidelity is10/10, preserving all rows and prose.
- **q-77220 source plot:** raw labels putt=1 left of the y-axis andt=2 right. Actual printed coordinates aret=1≈(1.402448,1.741591),t=2≈(−3.680854,1.857772). The source graphic depicts reflected/reversed involute geometry inconsistent with the formula. Generated diagrams use the actual printed curve and those exact endpoints. This is a plot-content repair, not a bank/value exclusion. Raw plot montage and path remain evidence.
- Source notation uses Unicode function application and some shorthand`{cos}`/`{sin}` powers. Source replay retains these except the explicit defective argument repair; the independent parser normalizes them internally. Row whitespace is normalized for comparisons. Source prompt syntax/spacing is preserved with only the recreated asset path changing. No mathematical source is excluded.
