# Template extraction

## 1. Specific source instances

The fourteen original records are analyzed at fixed basis 2275. All use x as the independent variable and y or f(x) as the dependent quantity. The requested response is an explicit particular function, or precisely the supplied blank fragment. The initial pair determines a single additive constant. Every complete original choice and source field is mapped below; prose and full source stages remain in source.json and review.md.

### q-119078

Find the particular solution to the differential equation $(x - 1)^{2}y^{′} =-2$ that satisfies the condition $y(2) = 1$.

Field :answer-field.type/radio; key selection. Captured difficulty absent. Primitive \frac{2}{x - 1}; given pair (2, 1); supplied component 0.

| Choice identity | Captured complete value | Explicit replay expression | Captured designation |
|---|---|---|---|
| d2cdeff7-1bd1-52cc-b4d2-58765a1e715e | `y = - (1)/(2(x - 1)) + \frac{3}{2}` | `r * (3/2 - 1/(2*x - 2))` | absent |
| e264582e-6aa3-5da8-b05d-657aca25a556 | `y = \frac{1}{x - 1} + \frac{1}{2}` | `r * (1/2 + 1/(x - 1))` | absent |
| 43d2def0-e7d1-54fb-834f-84b6876ea10b | `y = \frac{2}{x - 1} - 1` | `r * (-1 + 2/(x - 1))` | absent |
| 518e0850-647a-5199-8686-13cfd746ca8f | `y = \frac{1}{x - 1}` | `r * (1/(x - 1))` | absent |
| 6fc7592f-e41a-5c1f-9369-d6bc76a6ea98 | `y = \frac{2}{x - 1} + 3` | `r * (3 + 2/(x - 1))` | absent |

### q-49942

Find the particular solution to the differential equation below that satisfies the condition $f(0) =-1$.

$2f^{′}(x) + e^{x} = 0$.

Field :answer-field.type/radio; key selection. Captured difficulty absent. Primitive - \frac{e^{x}}{2}; given pair (0, -1); supplied component 0.

| Choice identity | Captured complete value | Explicit replay expression | Captured designation |
|---|---|---|---|
| 9acd2481-0ec3-5994-9168-964cb3c474c8 | `f(x) = \frac{1}{2}e^{x} - 1` | `r * (exp(x)/2 - 1)` | absent |
| b3631b1e-e008-5fb9-a825-84c8ecba10b9 | `f(x) = e^{x} - 2` | `r * (exp(x) - 2)` | absent |
| c508b657-4c25-56c5-960c-217135f76315 | `f(x) =-\frac{1}{2}e^{x} + 1` | `r * (1 - exp(x)/2)` | absent |
| f83fba29-574c-5d24-b1a6-4adbe9283fcb | `f(x) = \frac{1}{2}(e^{x} - 3)` | `r * (exp(x)/2 - 3/2)` | absent |
| 38b83252-dae4-5abd-841f-1818a0da90fc | `f(x) =-\frac{1}{2}(e^{x} + 1)` | `r * (-exp(x)/2 - 1/2)` | absent |

### q-119045

Find the particular solution to the differential equation ${f}^{′}(x)+2\operatorname{cos}⁡x=0$ that satisfies the condition $f(0)=-1.$

Field :answer-field.type/radio; key selection. Captured difficulty :question.difficulty/easy. Primitive - 2 \sin{(x )}; given pair (0, -1); supplied component 0.

| Choice identity | Captured complete value | Explicit replay expression | Captured designation |
|---|---|---|---|
| 42ecc69b-755b-5462-8126-6d18390bc9cd | `f(x)=-2\operatorname{sin}⁡x-1` | `r * (-2*sin(x) - 1)` | True |
| 51d0ffb6-6f64-5896-abdf-17cb6f16197d | `f(x)=2\operatorname{cos}⁡x-3` | `r * (2*cos(x) - 3)` | False |
| b403e123-9b40-51a1-b551-d4ee97aeac63 | `f(x)=\frac{1}{2}\operatorname{sin}⁡x-1` | `r * (sin(x)/2 - 1)` | False |
| bcae2f92-0655-5e91-b689-f83acfb52de0 | `f(x)=2\operatorname{sin}⁡x-3` | `r * (2*sin(x) - 3)` | False |
| ec6281fe-2594-5ca0-8ac1-0635fb6762ac | `f(x)=-2\operatorname{cos}⁡x+1` | `r * (1 - 2*cos(x))` | False |

### q-119046

Find the particular solution to the differential equation ${f}^{′}(x)-4x=1$ that satisfies the condition $f(1)=-1.$

Field :answer-field.type/radio; key selection. Captured difficulty :question.difficulty/easy. Primitive 2 x^{2} + x; given pair (1, -1); supplied component 0.

| Choice identity | Captured complete value | Explicit replay expression | Captured designation |
|---|---|---|---|
| 0877a493-110b-5bc5-b8f0-b95a212d57cb | `f(x)=2{x}^{2}+x-4` | `r * (2*x**2 + x - 4)` | True |
| 404b89d5-fb90-54b3-9fd1-b0ed48ad3aca | `f(x)={x}^{2}-2x` | `r * (x**2 - 2*x)` | False |
| 7d24a901-b539-53de-9ab1-410020de269d | `f(x)={x}^{2}+2x-4` | `r * (x**2 + 2*x - 4)` | False |
| b2cb0cc0-4925-5d83-a3b2-07b01eb84c1d | `f(x)=2{x}^{2}+3x-6` | `r * (2*x**2 + 3*x - 6)` | False |
| c233f23d-d374-5888-ae7d-c2e80f985c8b | `f(x)=2{x}^{2}+x-1` | `r * (2*x**2 + x - 1)` | False |

### q-119075

Find the particular solution to the differential equation ${y}^{′}+{e}^{-2x}=8x$ that satisfies the condition $y(0)=1.$

Field :answer-field.type/radio; key selection. Captured difficulty :question.difficulty/moderate. Primitive 4 x^{2} + \frac{e^{- 2 x}}{2}; given pair (0, 1); supplied component 0.

| Choice identity | Captured complete value | Explicit replay expression | Captured designation |
|---|---|---|---|
| 063d885c-e465-53c3-8fc9-1185c7d2a24c | `y=2{x}^{2}-2{e}^{-2x}+3` | `r * (2*x**2 + 3 - 2*exp(-2*x))` | False |
| 2352b722-ccc2-5fb7-b992-99d02c98a38b | `y=8{x}^{2}+2{e}^{-2x}-1` | `r * (8*x**2 - 1 + 2*exp(-2*x))` | False |
| 4927258a-3e5d-57d8-ad17-4093de1cc583 | `y=2{x}^{2}+\frac{{e}^{-2x}}{2}+\frac{1}{2}` | `r * (2*x**2 + 1/2 + exp(-2*x)/2)` | False |
| 7cf4bda2-85a0-506d-86cb-55bb6ebcdb9d | `y=4{x}^{2}+\frac{{e}^{-2x}}{2}-\frac{3}{2}` | `r * (4*x**2 - 3/2 + exp(-2*x)/2)` | False |
| febdfee4-02c6-55f5-970a-792e4ad18364 | `y=4{x}^{2}+\frac{{e}^{-2x}}{2}+\frac{1}{2}` | `r * (4*x**2 + 1/2 + exp(-2*x)/2)` | True |

### q-119083

Find the particular solution to the differential equation ${y}^{′}-2x={e}^{x/2}$ that satisfies the condition $y(0)=2.$

Field :answer-field.type/radio; key selection. Captured difficulty :question.difficulty/moderate. Primitive x^{2} + 2 e^{\frac{x}{2}}; given pair (0, 2); supplied component 0.

| Choice identity | Captured complete value | Explicit replay expression | Captured designation |
|---|---|---|---|
| 4861751d-591d-55c3-986e-ef2a5b44047f | `y=x-\frac{{e}^{x/2}}{2}+\frac{5}{2}` | `r * (x - exp(x/2)/2 + 5/2)` | False |
| 66412d8c-05ca-5d19-b457-71e9ce3cbc83 | `y={x}^{2}+2{e}^{x/2}+2` | `r * (x**2 + 2*exp(x/2) + 2)` | False |
| 73dd9002-7420-57dd-aa1f-4e2c936b2b76 | `y=2x+{e}^{x/2}+1` | `r * (2*x + exp(x/2) + 1)` | False |
| 906cd958-b4d4-5e47-8a8a-6773bb3989db | `y={x}^{2}+2{e}^{x/2}` | `r * (x**2 + 2*exp(x/2))` | True |
| f2723fb9-3ffe-529a-aa32-10cf5b96b2dd | `y={x}^{2}+\frac{{e}^{x/2}}{2}+\frac{3}{2}` | `r * (x**2 + exp(x/2)/2 + 3/2)` | False |

### q-347842

Find the particular solution to the differential equation $8x-\frac{\text{d}y}{\text{d}x}={x}^{2}$ that satisfies the condition $y(2)=5.$

$y=-\frac{{x}^{3}}{3}\,+${{field-1}}

Field :answer-field.type/blank; key field-1. Captured difficulty :question.difficulty/easy. Primitive - \frac{x^{3}}{3} + 4 x^{2}; given pair (2, 5); supplied component - \frac{x^{3}}{3}.

| Choice identity | Captured complete value | Explicit replay expression | Captured designation |
|---|---|---|---|
| a99c790f-778d-5a5f-97a8-2b99e8f49b10 | `4{x}^{2}-\frac{25}{3}` | `r * (4*x**2 - 25/3)` | True |

### q-352066

Find the particular solution to the differential equation $(x-3)^{2}{y}^{′}=8$ that satisfies the condition $y(4)=1.$

$y=\,${{field-1}}

Field :answer-field.type/blank; key field-1. Captured difficulty :question.difficulty/easy. Primitive - \frac{8}{x - 3}; given pair (4, 1); supplied component 0.

| Choice identity | Captured complete value | Explicit replay expression | Captured designation |
|---|---|---|---|
| 203a3079-ee5c-560e-8635-760c7bf1066a | `-\frac{8}{x-3}+9` | `r * (9 - 8/(x - 3))` | True |

### q-352068

Find the particular solution to the differential equation $\sqrt{x+1}\,{y}^{′}=4$ that satisfies the condition $y(3)=10.$

$y=\,${{field-1}}

Field :answer-field.type/blank; key field-1. Captured difficulty :question.difficulty/easy. Primitive 8 \sqrt{x + 1}; given pair (3, 10); supplied component 0.

| Choice identity | Captured complete value | Explicit replay expression | Captured designation |
|---|---|---|---|
| c11b83c6-f179-56e1-8175-cb7b2c642c20 | `8\sqrt{x+1}-6` | `r * (8*sqrt(x + 1) - 6)` | True |

### q-352075

Find the particular solution to the differential equation ${f}^{′}(x)+3\operatorname{sin}⁡x=0$ that satisfies the condition $f(0)=2.$

$f(x)=\,${{field-1}}

Field :answer-field.type/blank; key field-1. Captured difficulty :question.difficulty/easy. Primitive 3 \cos{(x )}; given pair (0, 2); supplied component 0.

| Choice identity | Captured complete value | Explicit replay expression | Captured designation |
|---|---|---|---|
| 98c0bcef-46b2-545e-843c-328afdee9423 | `3\operatorname{cos}x-1` | `r * (3*cos(x) - 1)` | True |

### q-50044

Find the particular solution to the differential equation below that satisfies the condition $y(-1)=2$
 

$$
x\cdot \frac{\text{d}y}{\text{d}x}=6{x}^{3}.
$$

Field :answer-field.type/radio; key selection. Captured difficulty :question.difficulty/easy. Primitive 2 x^{3}; given pair (-1, 2); supplied component 0.

| Choice identity | Captured complete value | Explicit replay expression | Captured designation |
|---|---|---|---|
| 2c2556ab-42eb-5b03-9b82-ffafb8c7bdf9 | `y=6{x}^{3}+8` | `r * (6*x**3 + 8)` | False |
| 340e3d02-facf-523f-89ff-093dd1bcd18f | `y=-2{x}^{2}+4` | `r * (4 - 2*x**2)` | False |
| aae0e4e4-5033-5e88-827b-62d31ab7b6e4 | `y={x}^{3}+3` | `r * (x**3 + 3)` | False |
| f0f11883-6eaf-55d0-bcf4-0414977256ab | `y=3{x}^{2}-1` | `r * (3*x**2 - 1)` | False |
| fdcec268-59b1-5bae-be4e-f748d99e9108 | `y=2{x}^{3}+4` | `r * (2*x**3 + 4)` | True |

### q-50092

Find the particular solution to the differential equation below that satisfies the condition $y(1)=1.$

$$
2x+\frac{\text{d}y}{\text{d}x}={x}^{2}+4x.
$$

Field :answer-field.type/radio; key selection. Captured difficulty :question.difficulty/easy. Primitive \frac{x^{3}}{3} + x^{2}; given pair (1, 1); supplied component 0.

| Choice identity | Captured complete value | Explicit replay expression | Captured designation |
|---|---|---|---|
| 1a8cac35-ec47-5085-bcb0-da00cb39efe3 | `y={x}^{3}+{x}^{2}-1` | `r * (x**3 + x**2 - 1)` | False |
| 2ecb6c15-4ffb-53a5-a6a3-acd959f971df | `y=\frac{{x}^{3}}{3}+{x}^{2}-\frac{1}{3}` | `r * (x**3/3 + x**2 - 1/3)` | True |
| 82e52b8f-937b-5b6c-bf07-b2a4477afeb9 | `y={x}^{3}+2{x}^{2}-2` | `r * (x**3 + 2*x**2 - 2)` | False |
| d1cbd642-0604-55df-9d4b-e311b2299017 | `y=\frac{{x}^{3}}{3}-{x}^{2}+\frac{5}{3}` | `r * (x**3/3 - x**2 + 5/3)` | False |
| f83e9e7e-87a9-5751-b17a-60d01d2b92ac | `y=\frac{{x}^{3}}{3}+2{x}^{2}-\frac{4}{3}` | `r * (x**3/3 + 2*x**2 - 4/3)` | False |

### q-50159

Find the particular solution to the differential equation below that satisfies the condition $f(0)=-2.$

$$
(1+2x){f}^{′}(x)-2=0.
$$

Field :answer-field.type/radio; key selection. Captured difficulty :question.difficulty/easy. Primitive \ln{(|{2 x + 1}| )}; given pair (0, -2); supplied component 0.

| Choice identity | Captured complete value | Explicit replay expression | Captured designation |
|---|---|---|---|
| 88dad183-ed2b-5a15-83b8-2f429e39030d | `f(x)=2\operatorname{ln}⁡\vert1+2x\vert-2` | `r * (2*log(Abs(2*x + 1)) - 2)` | False |
| 963a6dbf-bdcb-54b7-b515-ded61ba89b6a | `f(x)=\operatorname{ln}⁡\vert1+2x\vert-2` | `r * (log(Abs(2*x + 1)) - 2)` | True |
| bafaabc4-4fca-516b-a9d6-7ed9697af49a | `f(x)=\operatorname{ln}⁡\vert1+2x\vert-1` | `r * (log(Abs(2*x + 1)) - 1)` | False |
| fd70074b-45df-5d86-ae50-06ecb0063c91 | `f(x)=2x-2` | `r * (2*x - 2)` | False |
| ffdab17a-cdb5-59fe-8492-3c8a1b66fd32 | `f(x)=2{x}^{2}+x-2` | `r * (2*x**2 + x - 2)` | False |

### q-8311

Find the specific solution to the differential equation $\frac{\text{d}y}{\text{d}x}+4=0$ given that $y(-1)=4.$

Field :answer-field.type/radio; key selection. Captured difficulty :question.difficulty/easy. Primitive - 4 x; given pair (-1, 4); supplied component 0.

| Choice identity | Captured complete value | Explicit replay expression | Captured designation |
|---|---|---|---|
| 7dc989a8-2c75-5f1c-9659-077b9b5ceeed | `y=4{x}^{2}` | `r * (4*x**2)` | False |
| 90451e36-0f3c-542c-9624-ec09beef5517 | `y=4` | `r * (4)` | False |
| 96633e09-e5d2-5a83-a534-6acb8fbe9b36 | `y=-4x` | `r * (-4*x)` | True |
| b2d311c7-63bd-56a8-90ae-daf55b933be8 | `y=-4` | `r * (-4)` | False |
| eec3251e-786c-5a1a-9eba-fcc26b7bd286 | `y=-2x-2` | `r * (-2*x - 2)` | False |

## 2. Generalized backbone

Rearrange the supplied first-order equation to a derivative depending only on x; integrate once; retain source factorization and primitive stages; write P(x)+C; substitute the actual given function value; evaluate each displayed primitive component in the source order; collect the arithmetic when the source does; solve C=v−P(a); give the explicit particular function. The supplied cubic term in q-347842 is not part of its blank answer. An arbitrary-C family alone does not meet the particular-response criterion.

## 3. Components, banks and interpretation limits

Observed replay uses a genuine mathematical symmetry: rescale the dependent function by a nonzero integer r. Its derivative, primitive, initial target and every complete candidate function all rescale together. The actual displayed ODE preserves its derivative coefficient and rescales its derivative-free terms; this produces derivative r*g₀(x). The initial target is r*b₀. Each bank recipe is r*Fᵢ(x), as explicitly mapped above, rather than a source-value offset, unrelated perturbation or original-parameter answer table. The intent of historical wrong operations remains opaque, so both observed_raw and observed_repaired are ineligible evidence. Unit scalar multipliers suppress themselves as a generic component-formatting rule; there is no original-parameter branch returning a source question payload.

Normal families use the same observed prompt/solution masks and response contracts, but an independently sampled target v. Correct values come from r*P₀+v−r*P₀(a). A complete authored radio bank contains correct; discard the supplied initial value (impose zero instead); negate the primitive and then impose the real condition; use the derivative as a primitive and impose the condition (for q-49942 instead ignore the displayed derivative coefficient 2 while isolating, since its unscaled exponential derivative equals its primitive); and one family-specific operation. The fifth operation is: add instead of subtracting the primitive value when solving C for reciprocal/exponential single-term families; reciprocate the displayed coefficient in trig integration; swap exponential differentiation/integration scale for moderate sums; omit the new-power 1/2 divisor for the radical; omit inner-linear divisor 2 for the logarithm; treat a constant derivative as linear before integrating; or omit each new-degree divisor in polynomial integration. Hard uses the polynomial new-power-divisor-3 omission in one component. These are authored method operations, not recovered historical error intent. No distractor feedback is invented.

Banks are fixed as complete profiles before any parameters. Equivalent complete functions, duplicate options or correct distractors reject the entire sampled instance. Explicit invalid inputs raise, rather than being changed. Source blank shapes remain fixed in normal sampling; hard blank/radio peers are separately authored layouts. Captured absent answer feedback remains absent.

## 4. Slots, masks, bounds and dependencies

Observed replay parameters contain only scale r∈{−2,−1,1,2,3,4}. This bounded rescaling changes actual integration coefficients and conditions while keeping the operation, singularities, familiar evaluation input and all source stage roles. Normal easy/moderate parameters are exactly r in that catalog and integer v with 0<|v|≤12. Normal default selection exercises all twelve supported easy masks (including two explicitly authored easy assignments for unrated originals) and both moderate masks. Initial input a stays at its family-specific source point so the existing rational, perfect-square, trigonometric or exponential evaluation workload and its operative masks remain intact. This is a documented conservative arithmetic policy; it does not claim that source targets are intrinsically immutable. The v slot varies the requested initial function value and its solved constant independently with every other mathematical input held fixed in QA.

Signed scale factors wrap complete mathematical components with a visible multiplication operator. They do not concatenate numeric factors or modify variable/function labels, prose, TeX commands or differentials. Primitive factors, factored integrals, evaluated components and collected arithmetic remain separate ordered masks. Normal repair removes q-50044's erroneous dx before scaling, placing C outside the coefficient mask. This avoids treating r*C as the same subsequently solved C.

Hard parameters are integer nonzero |a|≤6, |b|≤3, |d|≤4, k∈{−2,−1,1,2}, initial input zero and integer |v|≤12. Three nonzero components are mandatory. Explicit fractional/huge-denominator coefficients or targets and noncatalog inputs fail. All samplers use these same bounds. Zero initial targets may produce a hard blank but an ambiguous radio bank is rejected as a whole. The coefficient/target arithmetic stays bounded and uses prerequisite power, exponential and trig rules. All family variants within one level are peers; no integrating-factor, separation, second-order or extra-condition branch is added.

Mathematical fingerprints normalize the actual derivative with exact factor/cancel and include the actual initial input and target. Function-letter aliases, banks, seed, shuffle and unused parameters do not inflate mathematical-task counts. Content identities use normalized displayed prompt, fixed solution, complete sorted bank, actual difficulty/key presence and actual correct designation. Shared scripts/question_capture/math_format.py normalizes before IDs and validates all public output; absent raw solutions are validated through a temporary empty fixture without adding that absent key to returned records. Runtime Python and SymPy versions are recorded.

## Domain and source errors

Initial connected intervals are x>1 for q-119078; x>3 for q-352066; x>−1 for q-352068; x>−1/2 for q-50159; and x<0 for rearranging q-50044. The last polynomial also satisfies its original unisolated equation at x=0, but the displayed division method uses the interval containing the negative given input. Others use all real x. No unconditional absolute-value/sign stripping is allowed: the validator verifies logarithmic expressions on the actual positive connected branch by a positive-symbol substitution.

q-119078 and q-49942 are unrated and lack worked solutions/correct references. Raw replay preserves all omissions. Repaired profiles explicitly author the easy assignment, infer the unique mathematically valid third/fifth choice and supply complete same-method stages. No missing source solution/difficulty is claimed recovered. q-119045's general-solution prose misnames f as y; q-50044 attaches dx to an evaluated primitive and misnames the final y solution f. Raw profiles preserve these errors and remain ineligible; repaired/normal profiles make the smallest supported corrections. Twelve exact original worked-solution matches are separate from ten unmodified complete solutions, two supported teaching corrections and two absent solutions completed by authorship. Bank notation normalization is separately counted from complete mathematical-value matches. No TeX escape anomaly is inferred from serialized display alone.
