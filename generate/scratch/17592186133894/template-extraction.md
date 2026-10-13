# Four-stage template extraction

## 1. Specific source descriptions

All exact prompts and complete worked solutions remain in source.json and are shown publicly in review.md. The following table identifies component forms, bounds and the five-option bank without choice-order assumptions.

| Source | Family | Curve / field pattern | Difficulty |
|---|---|---|---|
| q-124639 | product | F=(yz,xz,xy); r=(t,t²,t³), [0,1] | hard |
| q-124674 | helix_root | F=(x,y,z); r=(cos t,sin t,2√t), [0,π] | unrated |
| q-124669 | mixed_polynomial | F=(x+z,z−y,z²); r=(t²,3t²,2t), [0,1] | hard |
| q-124677 | trig_cancel | F=(x,z,y); r=(−sin t,sec t,cos t), [0,π/6] | hard |
| q-124690 | exp_cancel_xy | F=(y,x,z); r=(exp(−t),exp(t),exp(2t)), [0,1] | hard |
| q-124695 | exp_cancel_yz | F=(x,z,y); r=(2exp(t),3exp(2t),exp(−2t)), [0,1] | hard |
| q-165420 | quotient_exp | F=(z/x,z/y,1); r=(exp(t),exp(t),t), [0,1] | hard |
| q-165421 | radical_power | F=(√x,√y,z); r=(t,t,t²), [1,2] | hard |

## 2. General shared pattern

Evaluate the direct three-dimensional vector integral by substituting every coordinate into every field component, differentiating the three curve components, forming ordered component products, reducing their sum, finding a primitive and subtracting endpoint values. Preserve independent variables and directed parameter bounds. All answers are exact scalar expressions; every source has one radio widget with five alternatives.

## 3. Complete component and bank mapping

Historical scalar alternatives do not determine unique mistake operations. Every one is explicitly classified as opaque evidence and retained in a distinct replay profile; no numerical-fit distractors are used. A field multiplier λ legitimately scales every option and F-dependent solution expression by linearity. This is an evidence extension, not a claim about the historical wrong operation. The curve, derivative, coordinate rows and symbolic generic integral retain their original meanings. λ=1 reproduces source strings through the same field/RHS masks.

### q-124639 — observed:product

Prompt: Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y,z)=yz\,i+xz\,j+xy\,k$ and $C$ is the path $r(t)=t\,i+{t}^{2}\,j+{t}^{3}\,k$ for $t\in [0,1].$

Every original option maps to λ times its displayed expression (intent unresolved):
- `2557c5c7-30b3-5afb-b66c-cd97d609a91f`: $0$; historical wrong choice
- `39d24363-05be-531d-96a3-8a8345e36593`: $1$; historical correct designation
- `3df3fcde-f645-5bcb-9f52-c5f9612e7bde`: $\frac{1}{4}$; historical wrong choice
- `b9cf3b24-513f-538e-8e00-08e6da4ad492`: $\frac{1}{2}$; historical wrong choice
- `c6f52992-7d3e-58e1-9e49-6dd7d9bf1180`: $\frac{1}{3}$; historical wrong choice

Original solution math-block row counts: [2, 2, 3, 3, 3, 4]. The complete original sequence is retained, including omitted redundant substitution and endpoint rows.

### q-124674 — observed:helix_root

Prompt: Evaluate $\displaystyle \int_{C}F \cdot dr$ given that $F(x, y, z) = xi + yj + zk$ and $C$ is the path $r(t) = \cos ti + \sin tj + 2\sqrt{t}k$ for $t ∈ [0, π]$.

Every original option maps to λ times its displayed expression (intent unresolved):
- `a99d10b2-ab07-502d-8794-b8f6ee5b7f4d`: $\frac{π}{2}$; no historical designation
- `b9622713-417d-5fef-850f-81703cfa693c`: $π^{2}$; no historical designation
- `d7fe33ba-a2de-5d8c-8512-fb0862ceb070`: $π$; no historical designation
- `ee290483-c8ec-5e13-8ce7-343637205be2`: $2π$; no historical designation
- `029e5be3-14d0-5061-b997-ad2219db3e11`: $4π$; no historical designation

Original solution math-block row counts: []. The complete original sequence is retained, including omitted redundant substitution and endpoint rows.

### q-124669 — observed:mixed_polynomial

Prompt: Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y,z)=(x+z)\,i+(z-y)\,j+{z}^{2}\,k$ and $C$ is the path $r(t)={t}^{2}\,i+3{t}^{2}\,j+2t\,k$ for $t\in [0,1].$

Every original option maps to λ times its displayed expression (intent unresolved):
- `83e0770e-c267-5e3b-955d-1a6ae19f426e`: $16$; historical wrong choice
- `8424e559-0373-54af-9037-937c2d95caaf`: $6$; historical wrong choice
- `88ee1a02-2607-536b-9a0e-c10769c3649b`: $4$; historical correct designation
- `9681efc7-d9d1-594e-a8c4-90f17c60112e`: $8$; historical wrong choice
- `c5190a1a-c270-5ec1-826a-6a00690e62bd`: $5$; historical wrong choice

Original solution math-block row counts: [2, 2, 2, 3, 3, 5]. The complete original sequence is retained, including omitted redundant substitution and endpoint rows.

### q-124677 — observed:trig_cancel

Prompt: Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y,z)=x\,i+z\,j+y\,k$ and $C$ is the path $r(t)=-\operatorname{sin}⁡t\,i+\operatorname{sec}⁡t\,j+\operatorname{cos}⁡t\,k$ for $t\in [0,\frac{\pi }{6}].$

Every original option maps to λ times its displayed expression (intent unresolved):
- `30c1308d-48c3-5f0f-922b-8509570a2038`: $\frac{1}{3}$; historical wrong choice
- `51686c62-e3e7-5654-a41a-83d8e877d098`: $\frac{1}{8}$; historical correct designation
- `5d9fed1a-f7e4-5722-89dc-8b57c09f4643`: $\frac{1}{9}$; historical wrong choice
- `963cbc68-6c9d-5269-b521-b240e487709a`: $\frac{1}{4}$; historical wrong choice
- `e8030e68-9504-5bd8-98de-16c58eaffbdf`: $\frac{1}{2}$; historical wrong choice

Original solution math-block row counts: [2, 2, 2, 3, 3, 7]. The complete original sequence is retained, including omitted redundant substitution and endpoint rows.

### q-124690 — observed:exp_cancel_xy

Prompt: Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y,z)=y\,i+x\,j+z\,k$ and $C$ is the path $r(t)={e}^{-t}\,i+{e}^{t}\,j+{e}^{2t}\,k$ for $t\in [0,1].$

Every original option maps to λ times its displayed expression (intent unresolved):
- `3a5bc4af-772e-516e-a11f-68562d901d17`: $\frac{e-1}{4}$; historical wrong choice
- `997d0ead-44af-5031-96e5-ef15347630fd`: $\frac{{e}^{4}-1}{2}$; historical correct designation
- `d0f77ec9-76c5-5ab3-9612-44ceb7a7b709`: $\frac{{e}^{2}-1}{4}$; historical wrong choice
- `d5a47826-dabe-597f-a081-dfcabcd95468`: $\frac{{e}^{4}-1}{4}$; historical wrong choice
- `dae0bc6d-5495-509b-afd6-5e35a74959c2`: $\frac{{e}^{2}-1}{2}$; historical wrong choice

Original solution math-block row counts: [2, 2, 2, 3, 3, 4]. The complete original sequence is retained, including omitted redundant substitution and endpoint rows.

### q-124695 — observed:exp_cancel_yz

Prompt: Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y,z)=x\,i+z\,j+y\,k$ and $C$ is the path $r(t)=2{e}^{t}\,i+3{e}^{2t}\,j+{e}^{-2t}\,k$ for $t\in [0,1].$

Every original option maps to λ times its displayed expression (intent unresolved):
- `1e557883-27cf-5b9b-86a9-bebb6f242a60`: $4{e}^{2}-1$; historical wrong choice
- `20ed3abb-812c-5053-b9f8-6f958cc90a39`: $4{e}^{4}-4$; historical wrong choice
- `83f044b9-598d-57ca-a361-e38ec3156e7a`: $2{e}^{2}-1$; historical wrong choice
- `af8267a1-ce48-5b02-af6a-53815dda0d77`: $4{e}^{2}-2$; historical wrong choice
- `ffa15884-2ebf-590b-95f2-642ef9548fdf`: $2{e}^{2}-2$; historical correct designation

Original solution math-block row counts: [2, 2, 2, 3, 3, 4]. The complete original sequence is retained, including omitted redundant substitution and endpoint rows.

### q-165420 — observed:quotient_exp

Prompt: Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y,z)=\frac{z}{x}\,i+\frac{z}{y}\,j+k$ and $C$ is the path $r(t)={e}^{t}\,i+{e}^{t}\,j+t\,k$ for $t\in [0,1].$

Every original option maps to λ times its displayed expression (intent unresolved):
- `0cd2b6b6-0325-5b52-9c15-4b3958efbfe6`: $1$; historical wrong choice
- `0f3891c3-c0e9-51aa-ae2a-1115424938e7`: $2+e$; historical wrong choice
- `7c744f46-1dde-51e0-9bbd-73c472928650`: $2$; historical correct designation
- `9efef550-a80c-54b2-a611-ccdeb6fa03e3`: $1+e$; historical wrong choice
- `fb233049-a49f-5dc7-86ce-9813de943cb3`: $2+{e}^{2}$; historical wrong choice

Original solution math-block row counts: [2, 2, 2, 3, 3, 4]. The complete original sequence is retained, including omitted redundant substitution and endpoint rows.

### q-165421 — observed:radical_power

Prompt: Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y,z)=\sqrt{x}\,i+\sqrt{y}\,j+z\,k$ and $C$ is the path $r(t)=t\,i+t\,j+{t}^{2}\,k$ for $t\in [1,2].$

Every original option maps to λ times its displayed expression (intent unresolved):
- `3dc6092a-1d9c-5d00-b848-0eb08cf8711f`: $\frac{7\sqrt{2}+32}{6}$; historical wrong choice
- `9fb55c89-b4ca-5c95-bc06-7698dd988f07`: $\frac{5\sqrt{2}+31}{6}$; historical wrong choice
- `b3b16f14-4103-53c3-a3c1-24e547b169b4`: $\frac{8\sqrt{2}+47}{6}$; historical wrong choice
- `c7f112b6-723a-540f-bc01-82ba0c2d3788`: $\frac{16\sqrt{2}+37}{6}$; historical correct designation
- `e32ee68a-9e5c-5e34-8f6b-ddb64d91ac1a`: $\frac{10\sqrt{2}+45}{6}$; historical wrong choice

Original solution math-block row counts: [2, 2, 2, 3, 3, 5]. The complete original sequence is retained, including omitted redundant substitution and endpoint rows.

## 4. Reusable masks, domains and calculations

Historical masks own the complete field expression and complete F-dependent RHS components. No short-variable replacement is applied to source prose. Normal masks own complete mathematical vector components. Coordinate substitution operates on symbol atoms, including xy and arguments of roots; endpoint substitution protects TeX command names. Source prose is shared: “We will use the formula”, “Along the curve C, we have”, “Therefore”, “Computing r′(t), we get”, and “Finally, we evaluate the integral as follows”. Source masks preserve exact sentences and row counts. Authored normal masks add explicit component products and individually evaluated signed primitive components at both endpoints, so every operation is reviewable. The final worked solution is fixed independently of answer order/error choice.

Normal complete banks (chosen before parameters; every member must be unequal, real and finite; any collision rejects the entire instance):
- **constant_affine**: correct, reverse_orientation, omit_x, omit_y, omit_z.
- **diagonal_power**: correct, reverse_orientation, omit_x, omit_y, omit_z.
- **product**: correct, omit_x, omit_y, omit_z, do_not_differentiate_curve.
- **mixed_polynomial**: correct, omit_x, omit_y, omit_z, do_not_differentiate_curve.
- **exp_cancel_xy**: correct, omit_x, omit_y, omit_z, do_not_differentiate_curve.
- **exp_cancel_yz**: correct, omit_x, omit_y, omit_z, do_not_differentiate_curve.
- **trig_cancel**: correct, reverse_orientation, omit_half_in_sin_squared_primitive, drop_sine_square_in_primitive, omit_lower_endpoint_of_cosine_primitive.
- **radical_power**: correct, omit_both_radicals, omit_z, omit_factor_two_in_z_derivative, reverse_orientation.
- **quotient_exp**: correct, omit_both_quotient_components, omit_z, fail_cancel_first_exponential, fail_cancel_both_exponentials.
- **helix_root**: correct, omit_z, omit_half_in_sqrt_derivative, replace_sqrt_denominator_by_t, move_sqrt_denominator_to_numerator.

The omitted-component errors actually integrate the remaining products. The “do not differentiate” error integrates the actual three field pullbacks. Root errors change the actual derivative factor, not the final number by arbitrary perturbation. Trig errors alter the sine-square/cosine primitive and endpoint operations. Quotient errors retain specific uncancelled exponentials in the actual substituted products. No learner-facing diagnosis is added.

Sampling/explicit-input bounds: easy field scales are nonzero integers of absolute magnitude ≤5, affine slopes ±1,±2,±3, offsets −3…3; moderate field scales are nonzero integers of magnitude ≤4 on t,t²,t³; hard coordinate scales are nonzero integers of magnitude ≤3 (positive for root families). Exponential rates are 1,2,3. Nontrig polynomial/exponential bounds are increasing integer endpoints in 0…2; radical endpoints are increasing integers 1…4. Trig intervals are [0,π/6], [0,π/4], [0,π/3], away from secant poles. Normal root helices use a∈{1,2}, b∈{π,2π}. All bounds are enforced on explicit inputs. Historical profiles accept only lift λ∈{−3,−2,−1,1,2,3}.

Mathematical fingerprints use actual symbolic field, curve and directed limits, independent of seed, bank, option order and notation aliases. Constant-field affine offsets are incidental and excluded. The unused helix B metadata cannot inflate task identity. Full presentation identity includes version, displayed prompt, complete solution, difficulty and complete bank; bank/profile aliases alone cannot create identities. Native radio checks grade each actual owned answer. Separate temporary blank fixtures probe numeric equivalents without changing normal/source field layout.

Normal mathematical repairs: all third formal derivative terms use k; trig derivatives and dot vectors use t; the missing root-helix correct value is independently 2π at historical parameters and appears only as an authored/inferred result, never as a matched historical designation. No source error is silently declared passed. The source widget capture at /home/jake/Developer/MA/DATA/Lessons/2108/Source/2108.json confirms the unrated question’s five-choice radio layout and no correct designation in the captured widget.

Two authored complete banks have documented source-parameter collisions: trig_cancel at b=π/6 has an upper-only cosine-primitive value equal to the reversed-orientation value; quotient_exp at k=l=1 on [0,1] makes omission of both quotient components equal omission of z. Public raw profiles retain their complete historical banks. Normal method profiles reject the whole colliding instance and sample another eligible parameter tuple; they never replace individual options.

Exact comparison of exponential scalars converts integer-rate/endpoint exponentials to a rational Laurent polynomial in e. A nonzero polynomial with rational coefficients cannot vanish because e is transcendental. Other symbolic/trigonometric/radical comparisons still use exact independent SymPy reduction; no floating tolerances establish answer eligibility. This also prevents slow heuristic hyperbolic rewrites during bank collision checks.
