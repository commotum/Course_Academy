# Template extraction

## 1. Specific originals

All originals have independent variable x; dependent variable is y or f(x). Domains are connected real intervals containing the initial input. Rational denominator and radical restrictions are part of mathematical verification; q-50159 is restricted to x>−1/2 for its given input. Multiplication by x in q-50044 is handled away from x=0 when rearranging, and the derived smooth polynomial remains a solution of its displayed original equation at x=0 as well.

### q-119078

Find the particular solution to the differential equation $(x - 1)^{2}y^{′} =-2$ that satisfies the condition $y(2) = 1$.

Field: :answer-field.type/radio; key selection. Observed difficulty absent. Primitive \frac{2}{x - 1}; actual given input 2; target 1. Supplied fragment 0.

| Source choice | Exact captured value | Parameter recipe | Correct captured |
|---|---|---|---|
| d2cdeff7-1bd1-52cc-b4d2-58765a1e715e | `y = - (1)/(2(x - 1)) + \frac{3}{2}` | `3/2 - 1/(2*x - 2) + B − (1)` | absent |
| e264582e-6aa3-5da8-b05d-657aca25a556 | `y = \frac{1}{x - 1} + \frac{1}{2}` | `1/2 + 1/(x - 1) + B − (1)` | absent |
| 43d2def0-e7d1-54fb-834f-84b6876ea10b | `y = \frac{2}{x - 1} - 1` | `-1 + 2/(x - 1) + B − (1)` | absent |
| 518e0850-647a-5199-8686-13cfd746ca8f | `y = \frac{1}{x - 1}` | `1/(x - 1) + B − (1)` | absent |
| 6fc7592f-e41a-5c1f-9369-d6bc76a6ea98 | `y = \frac{2}{x - 1} + 3` | `3 + 2/(x - 1) + B − (1)` | absent |

Solution stages: 0 aligned row separators. Original complete solution stays in source.json and review.md; replay preserves all sentences and each primitive/initial-substitution row.

### q-49942

Find the particular solution to the differential equation below that satisfies the condition $f(0) =-1$.

$2f^{′}(x) + e^{x} = 0$.

Field: :answer-field.type/radio; key selection. Observed difficulty absent. Primitive - \frac{e^{x}}{2}; actual given input 0; target -1. Supplied fragment 0.

| Source choice | Exact captured value | Parameter recipe | Correct captured |
|---|---|---|---|
| 9acd2481-0ec3-5994-9168-964cb3c474c8 | `f(x) = \frac{1}{2}e^{x} - 1` | `exp(x)/2 - 1 + B − (-1)` | absent |
| b3631b1e-e008-5fb9-a825-84c8ecba10b9 | `f(x) = e^{x} - 2` | `exp(x) - 2 + B − (-1)` | absent |
| c508b657-4c25-56c5-960c-217135f76315 | `f(x) =-\frac{1}{2}e^{x} + 1` | `1 - exp(x)/2 + B − (-1)` | absent |
| f83fba29-574c-5d24-b1a6-4adbe9283fcb | `f(x) = \frac{1}{2}(e^{x} - 3)` | `exp(x)/2 - 3/2 + B − (-1)` | absent |
| 38b83252-dae4-5abd-841f-1818a0da90fc | `f(x) =-\frac{1}{2}(e^{x} + 1)` | `-exp(x)/2 - 1/2 + B − (-1)` | absent |

Solution stages: 0 aligned row separators. Original complete solution stays in source.json and review.md; replay preserves all sentences and each primitive/initial-substitution row.

### q-119045

Find the particular solution to the differential equation ${f}^{′}(x)+2\operatorname{cos}⁡x=0$ that satisfies the condition $f(0)=-1.$

Field: :answer-field.type/radio; key selection. Observed difficulty :question.difficulty/easy. Primitive - 2 \sin{(x )}; actual given input 0; target -1. Supplied fragment 0.

| Source choice | Exact captured value | Parameter recipe | Correct captured |
|---|---|---|---|
| 42ecc69b-755b-5462-8126-6d18390bc9cd | `f(x)=-2\operatorname{sin}⁡x-1` | `-2*sin(x) - 1 + B − (-1)` | True |
| 51d0ffb6-6f64-5896-abdf-17cb6f16197d | `f(x)=2\operatorname{cos}⁡x-3` | `2*cos(x) - 3 + B − (-1)` | False |
| b403e123-9b40-51a1-b551-d4ee97aeac63 | `f(x)=\frac{1}{2}\operatorname{sin}⁡x-1` | `sin(x)/2 - 1 + B − (-1)` | False |
| bcae2f92-0655-5e91-b689-f83acfb52de0 | `f(x)=2\operatorname{sin}⁡x-3` | `2*sin(x) - 3 + B − (-1)` | False |
| ec6281fe-2594-5ca0-8ac1-0635fb6762ac | `f(x)=-2\operatorname{cos}⁡x+1` | `1 - 2*cos(x) + B − (-1)` | False |

Solution stages: 4 aligned row separators. Original complete solution stays in source.json and review.md; replay preserves all sentences and each primitive/initial-substitution row.

### q-119046

Find the particular solution to the differential equation ${f}^{′}(x)-4x=1$ that satisfies the condition $f(1)=-1.$

Field: :answer-field.type/radio; key selection. Observed difficulty :question.difficulty/easy. Primitive 2 x^{2} + x; actual given input 1; target -1. Supplied fragment 0.

| Source choice | Exact captured value | Parameter recipe | Correct captured |
|---|---|---|---|
| 0877a493-110b-5bc5-b8f0-b95a212d57cb | `f(x)=2{x}^{2}+x-4` | `2*x**2 + x - 4 + B − (-1)` | True |
| 404b89d5-fb90-54b3-9fd1-b0ed48ad3aca | `f(x)={x}^{2}-2x` | `x**2 - 2*x + B − (-1)` | False |
| 7d24a901-b539-53de-9ab1-410020de269d | `f(x)={x}^{2}+2x-4` | `x**2 + 2*x - 4 + B − (-1)` | False |
| b2cb0cc0-4925-5d83-a3b2-07b01eb84c1d | `f(x)=2{x}^{2}+3x-6` | `2*x**2 + 3*x - 6 + B − (-1)` | False |
| c233f23d-d374-5888-ae7d-c2e80f985c8b | `f(x)=2{x}^{2}+x-1` | `2*x**2 + x - 1 + B − (-1)` | False |

Solution stages: 5 aligned row separators. Original complete solution stays in source.json and review.md; replay preserves all sentences and each primitive/initial-substitution row.

### q-119075

Find the particular solution to the differential equation ${y}^{′}+{e}^{-2x}=8x$ that satisfies the condition $y(0)=1.$

Field: :answer-field.type/radio; key selection. Observed difficulty :question.difficulty/moderate. Primitive 4 x^{2} + \frac{e^{- 2 x}}{2}; actual given input 0; target 1. Supplied fragment 0.

| Source choice | Exact captured value | Parameter recipe | Correct captured |
|---|---|---|---|
| 063d885c-e465-53c3-8fc9-1185c7d2a24c | `y=2{x}^{2}-2{e}^{-2x}+3` | `2*x**2 + 3 - 2*exp(-2*x) + B − (1)` | False |
| 2352b722-ccc2-5fb7-b992-99d02c98a38b | `y=8{x}^{2}+2{e}^{-2x}-1` | `8*x**2 - 1 + 2*exp(-2*x) + B − (1)` | False |
| 4927258a-3e5d-57d8-ad17-4093de1cc583 | `y=2{x}^{2}+\frac{{e}^{-2x}}{2}+\frac{1}{2}` | `2*x**2 + 1/2 + exp(-2*x)/2 + B − (1)` | False |
| 7cf4bda2-85a0-506d-86cb-55bb6ebcdb9d | `y=4{x}^{2}+\frac{{e}^{-2x}}{2}-\frac{3}{2}` | `4*x**2 - 3/2 + exp(-2*x)/2 + B − (1)` | False |
| febdfee4-02c6-55f5-970a-792e4ad18364 | `y=4{x}^{2}+\frac{{e}^{-2x}}{2}+\frac{1}{2}` | `4*x**2 + 1/2 + exp(-2*x)/2 + B − (1)` | True |

Solution stages: 5 aligned row separators. Original complete solution stays in source.json and review.md; replay preserves all sentences and each primitive/initial-substitution row.

### q-119083

Find the particular solution to the differential equation ${y}^{′}-2x={e}^{x/2}$ that satisfies the condition $y(0)=2.$

Field: :answer-field.type/radio; key selection. Observed difficulty :question.difficulty/moderate. Primitive x^{2} + 2 e^{\frac{x}{2}}; actual given input 0; target 2. Supplied fragment 0.

| Source choice | Exact captured value | Parameter recipe | Correct captured |
|---|---|---|---|
| 4861751d-591d-55c3-986e-ef2a5b44047f | `y=x-\frac{{e}^{x/2}}{2}+\frac{5}{2}` | `x - exp(x/2)/2 + 5/2 + B − (2)` | False |
| 66412d8c-05ca-5d19-b457-71e9ce3cbc83 | `y={x}^{2}+2{e}^{x/2}+2` | `x**2 + 2*exp(x/2) + 2 + B − (2)` | False |
| 73dd9002-7420-57dd-aa1f-4e2c936b2b76 | `y=2x+{e}^{x/2}+1` | `2*x + exp(x/2) + 1 + B − (2)` | False |
| 906cd958-b4d4-5e47-8a8a-6773bb3989db | `y={x}^{2}+2{e}^{x/2}` | `x**2 + 2*exp(x/2) + B − (2)` | True |
| f2723fb9-3ffe-529a-aa32-10cf5b96b2dd | `y={x}^{2}+\frac{{e}^{x/2}}{2}+\frac{3}{2}` | `x**2 + exp(x/2)/2 + 3/2 + B − (2)` | False |

Solution stages: 5 aligned row separators. Original complete solution stays in source.json and review.md; replay preserves all sentences and each primitive/initial-substitution row.

### q-347842

Find the particular solution to the differential equation $8x-\frac{\text{d}y}{\text{d}x}={x}^{2}$ that satisfies the condition $y(2)=5.$

$y=-\frac{{x}^{3}}{3}\,+${{field-1}}

Field: :answer-field.type/blank; key field-1. Observed difficulty :question.difficulty/easy. Primitive - \frac{x^{3}}{3} + 4 x^{2}; actual given input 2; target 5. Supplied fragment - \frac{x^{3}}{3}.

| Source choice | Exact captured value | Parameter recipe | Correct captured |
|---|---|---|---|
| a99c790f-778d-5a5f-97a8-2b99e8f49b10 | `4{x}^{2}-\frac{25}{3}` | `4*x**2 - 25/3 + B − (5)` | True |

Solution stages: 6 aligned row separators. Original complete solution stays in source.json and review.md; replay preserves all sentences and each primitive/initial-substitution row.

### q-352066

Find the particular solution to the differential equation $(x-3)^{2}{y}^{′}=8$ that satisfies the condition $y(4)=1.$

$y=\,${{field-1}}

Field: :answer-field.type/blank; key field-1. Observed difficulty :question.difficulty/easy. Primitive - \frac{8}{x - 3}; actual given input 4; target 1. Supplied fragment 0.

| Source choice | Exact captured value | Parameter recipe | Correct captured |
|---|---|---|---|
| 203a3079-ee5c-560e-8635-760c7bf1066a | `-\frac{8}{x-3}+9` | `9 - 8/(x - 3) + B − (1)` | True |

Solution stages: 5 aligned row separators. Original complete solution stays in source.json and review.md; replay preserves all sentences and each primitive/initial-substitution row.

### q-352068

Find the particular solution to the differential equation $\sqrt{x+1}\,{y}^{′}=4$ that satisfies the condition $y(3)=10.$

$y=\,${{field-1}}

Field: :answer-field.type/blank; key field-1. Observed difficulty :question.difficulty/easy. Primitive 8 \sqrt{x + 1}; actual given input 3; target 10. Supplied fragment 0.

| Source choice | Exact captured value | Parameter recipe | Correct captured |
|---|---|---|---|
| c11b83c6-f179-56e1-8175-cb7b2c642c20 | `8\sqrt{x+1}-6` | `8*sqrt(x + 1) - 6 + B − (10)` | True |

Solution stages: 5 aligned row separators. Original complete solution stays in source.json and review.md; replay preserves all sentences and each primitive/initial-substitution row.

### q-352075

Find the particular solution to the differential equation ${f}^{′}(x)+3\operatorname{sin}⁡x=0$ that satisfies the condition $f(0)=2.$

$f(x)=\,${{field-1}}

Field: :answer-field.type/blank; key field-1. Observed difficulty :question.difficulty/easy. Primitive 3 \cos{(x )}; actual given input 0; target 2. Supplied fragment 0.

| Source choice | Exact captured value | Parameter recipe | Correct captured |
|---|---|---|---|
| 98c0bcef-46b2-545e-843c-328afdee9423 | `3\operatorname{cos}x-1` | `3*cos(x) - 1 + B − (2)` | True |

Solution stages: 5 aligned row separators. Original complete solution stays in source.json and review.md; replay preserves all sentences and each primitive/initial-substitution row.

### q-50044

Find the particular solution to the differential equation below that satisfies the condition $y(-1)=2$
 

$$
x\cdot \frac{\text{d}y}{\text{d}x}=6{x}^{3}.
$$

Field: :answer-field.type/radio; key selection. Observed difficulty :question.difficulty/easy. Primitive 2 x^{3}; actual given input -1; target 2. Supplied fragment 0.

| Source choice | Exact captured value | Parameter recipe | Correct captured |
|---|---|---|---|
| 2c2556ab-42eb-5b03-9b82-ffafb8c7bdf9 | `y=6{x}^{3}+8` | `6*x**3 + 8 + B − (2)` | False |
| 340e3d02-facf-523f-89ff-093dd1bcd18f | `y=-2{x}^{2}+4` | `4 - 2*x**2 + B − (2)` | False |
| aae0e4e4-5033-5e88-827b-62d31ab7b6e4 | `y={x}^{3}+3` | `x**3 + 3 + B − (2)` | False |
| f0f11883-6eaf-55d0-bcf4-0414977256ab | `y=3{x}^{2}-1` | `3*x**2 - 1 + B − (2)` | False |
| fdcec268-59b1-5bae-be4e-f748d99e9108 | `y=2{x}^{3}+4` | `2*x**3 + 4 + B − (2)` | True |

Solution stages: 5 aligned row separators. Original complete solution stays in source.json and review.md; replay preserves all sentences and each primitive/initial-substitution row.

### q-50092

Find the particular solution to the differential equation below that satisfies the condition $y(1)=1.$

$$
2x+\frac{\text{d}y}{\text{d}x}={x}^{2}+4x.
$$

Field: :answer-field.type/radio; key selection. Observed difficulty :question.difficulty/easy. Primitive \frac{x^{3}}{3} + x^{2}; actual given input 1; target 1. Supplied fragment 0.

| Source choice | Exact captured value | Parameter recipe | Correct captured |
|---|---|---|---|
| 1a8cac35-ec47-5085-bcb0-da00cb39efe3 | `y={x}^{3}+{x}^{2}-1` | `x**3 + x**2 - 1 + B − (1)` | False |
| 2ecb6c15-4ffb-53a5-a6a3-acd959f971df | `y=\frac{{x}^{3}}{3}+{x}^{2}-\frac{1}{3}` | `x**3/3 + x**2 - 1/3 + B − (1)` | True |
| 82e52b8f-937b-5b6c-bf07-b2a4477afeb9 | `y={x}^{3}+2{x}^{2}-2` | `x**3 + 2*x**2 - 2 + B − (1)` | False |
| d1cbd642-0604-55df-9d4b-e311b2299017 | `y=\frac{{x}^{3}}{3}-{x}^{2}+\frac{5}{3}` | `x**3/3 - x**2 + 5/3 + B − (1)` | False |
| f83e9e7e-87a9-5751-b17a-60d01d2b92ac | `y=\frac{{x}^{3}}{3}+2{x}^{2}-\frac{4}{3}` | `x**3/3 + 2*x**2 - 4/3 + B − (1)` | False |

Solution stages: 5 aligned row separators. Original complete solution stays in source.json and review.md; replay preserves all sentences and each primitive/initial-substitution row.

### q-50159

Find the particular solution to the differential equation below that satisfies the condition $f(0)=-2.$

$$
(1+2x){f}^{′}(x)-2=0.
$$

Field: :answer-field.type/radio; key selection. Observed difficulty :question.difficulty/easy. Primitive \ln{(|{2 x + 1}| )}; actual given input 0; target -2. Supplied fragment 0.

| Source choice | Exact captured value | Parameter recipe | Correct captured |
|---|---|---|---|
| 88dad183-ed2b-5a15-83b8-2f429e39030d | `f(x)=2\operatorname{ln}⁡\vert1+2x\vert-2` | `2*log(Abs(2*x + 1)) - 2 + B − (-2)` | False |
| 963a6dbf-bdcb-54b7-b515-ded61ba89b6a | `f(x)=\operatorname{ln}⁡\vert1+2x\vert-2` | `log(Abs(2*x + 1)) - 2 + B − (-2)` | True |
| bafaabc4-4fca-516b-a9d6-7ed9697af49a | `f(x)=\operatorname{ln}⁡\vert1+2x\vert-1` | `log(Abs(2*x + 1)) - 1 + B − (-2)` | False |
| fd70074b-45df-5d86-ae50-06ecb0063c91 | `f(x)=2x-2` | `2*x - 2 + B − (-2)` | False |
| ffdab17a-cdb5-59fe-8492-3c8a1b66fd32 | `f(x)=2{x}^{2}+x-2` | `2*x**2 + x - 2 + B − (-2)` | False |

Solution stages: 7 aligned row separators. Original complete solution stays in source.json and review.md; replay preserves all sentences and each primitive/initial-substitution row.

### q-8311

Find the specific solution to the differential equation $\frac{\text{d}y}{\text{d}x}+4=0$ given that $y(-1)=4.$

Field: :answer-field.type/radio; key selection. Observed difficulty :question.difficulty/easy. Primitive - 4 x; actual given input -1; target 4. Supplied fragment 0.

| Source choice | Exact captured value | Parameter recipe | Correct captured |
|---|---|---|---|
| 7dc989a8-2c75-5f1c-9659-077b9b5ceeed | `y=4{x}^{2}` | `4*x**2 + B − (4)` | False |
| 90451e36-0f3c-542c-9624-ec09beef5517 | `y=4` | `4 + B − (4)` | False |
| 96633e09-e5d2-5a83-a534-6acb8fbe9b36 | `y=-4x` | `-4*x + B − (4)` | True |
| b2d311c7-63bd-56a8-90ae-daf55b933be8 | `y=-4` | `-4 + B − (4)` | False |
| eec3251e-786c-5a1a-9eba-fcc26b7bd286 | `y=-2x-2` | `-2*x - 2 + B − (4)` | False |

Solution stages: 4 aligned row separators. Original complete solution stays in source.json and review.md; replay preserves all sentences and each primitive/initial-substitution row.

## 2. Shared pattern

Rearrange the actual ODE; integrate the independent-variable function; write P(x)+C; substitute the actual initial pair; individually evaluate primitive components; solve C=B−P(a); render the explicit particular solution. A supplied-fragment blank expects precisely the missing additive fragment. A radio candidate is eligible only if its complete function both differentiates to the actual displayed ODE and satisfies the actual initial condition. An arbitrary-constant family is not a valid particular response.

## 3. Component mapping and bank interpretation

The tables map every captured option to its original field and complete bank. Observed error intent is opaque: the recipes explicitly retain each observed derivative candidate and translate its constant by the target displacement B−B₀. This is a genuine vertical-translation parameter family, not recovery of the author's error-generation code. These profiles are replay-only and ineligible for default generation. The explicit symbolic definitions are independently compared to every captured option. No polynomial fit or random wrong-value perturbation is used.

Correctness is derived independently from the actual prompt and condition; missing correct references are inferred only in observed_repaired completion. Missing raw difficulty, worked solution and correct references remain absent in observed_raw output. Raw evidence preserves source answer notation; generated bank values use standard TeX normalization of the explicit symbolic recipes. Full mathematical values and equation/fragment shapes match one-to-one. Authored operation banks have five complete candidates: correct; omit C; negate primitive and impose condition; use derivative as primitive and impose condition; halve primitive and impose condition. Every record exposes evidence_only and eligible_for_learning booleans in generation metadata. Both observed profiles are ineligible for learner generation; authored operation profiles are eligible. No option-specific feedback is added. Each bank is fixed before parameters; a collision rejects the whole instance.

## 4. Reusable masks and constraints

Observed parameter B changes the complete initial-condition component, numeric left components of substitution rows, complete solved constant component, and complete final solution component. Source primitive factors and all original evaluation rows remain fixed. Conditional algebra suppresses an empty zero translation in the complete expression; it does not return a copied source question. This conservative parameter axis honestly preserves observed stage structure. Authored defaults additionally vary integrand coefficients and initial pairs. Mathematical task hashes omit answer banks and function-letter aliases; content hashes include actual displayed prompt, fixed worked solution, full bank and key presence. Seeds only change samples or option order, never identity for fixed displayed content.

Easy authored power/trig peers use signed |a|≤8, nonzero coefficients, familiar integer power inputs or trig input zero. Moderate uses two nonzero components with |a|≤8, |b|≤4, exponent k∈{−2,−1,1/2,1,2} and initial input zero. Hard uses three nonzero components with |a|≤6, |b|≤3, |d|≤4, k∈{−2,−1,1,2} and input zero. All used coefficients and targets are integers; all targets satisfy |v|≤12. Initial inputs come from the stated finite integer catalog; fractional inputs, fractional targets and unbounded-denominator coefficients are rejected. Only the moderate exponent scale has the explicit familiar 1/2 option. Bounds apply to explicit inputs as well as samplers. Authored levels are parallel same-method workloads, not a progression within a difficulty. Coefficient-times-primitive stages and component substitution/evaluation rows use grouped signs, so negative numeric products cannot concatenate into another scalar.

## Source anomalies and repairs

q-119078 and q-49942 are unrated and lack worked solutions/correct references in this fixed-basis record. Their mathematical particular solutions uniquely identify the third and fifth source options, respectively; repaired records infer these designations and supply complete same-method stages. The owning authoritative 1061.json capture contains no matching question identifiers for these legacy items; no source difficulty or missing solution is claimed recovered.

q-119045's general-solution prose uses y although its ODE and final solution use f(x); repaired output uses f(x). q-50044 incorrectly prints dx after an evaluated primitive and names the final y solution f(x); repaired output removes that dx, retains the additive C stage, and uses y. Raw replay retains the captured errors as evidence, and the validator distinguishes them from normal correctness. There are no assumed TeX byte anomalies or image repairs.
