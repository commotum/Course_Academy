# Four-stage template extraction


##1. Specific captured examples

All35 displayed values are mapped below, along with every formal derivative/term derivative/evaluation stage. Original prose is preserved by masking complete mathematical components of each captured string; it is never returned as an unparameterized literal branch. Source annotations/feedback are preserved where supplied.


### q-1919

- Observed label: :question.difficulty/moderate

- Parameters: `{"a": -5, "b": 1, "base": 11}`

- Prompt: Find ${f}^{′}(x)$ for $f(x)={11}^{x}-5ln⁡x.$

- Formal derivative operand: ${11}^{x}-5ln⁡x$.

- Ordered derivative RHS stages: ${11}^{x}\cdot ln⁡11-5(\frac{1}{x})$ → ${11}^{x}ln⁡11-\frac{5}{x}$

- Ordered point arithmetic RHS stages: none

- Source worked solution: Taking the derivative, we have

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}({11}^{x}-5ln⁡x) \\  & ={11}^{x}\cdot ln⁡11-5(\frac{1}{x}) \\  & ={11}^{x}ln⁡11-\frac{5}{x}.\end{aligned}
$$


### q-1920

- Observed label: absent (authored moderate routing only)

- Parameters: `{"a": 2, "b": -5}`

- Prompt: Calculate $\frac{dy}{dx}$ for $y =-5e^{x} + 2\ln x$.

- Formal derivative operand: $-5e^{x} + 2\ln x$.

- Ordered derivative RHS stages: $-5e^{x} + \frac{2}{x}$

- Ordered point arithmetic RHS stages: none

- Source worked solution: absent


### q-11914

- Observed label: :question.difficulty/easy

- Parameters: `{"a": 5, "b": -3, "c": 2}`

- Prompt: Given that $y=5\operatorname{ln}x-3{x}^{2}+2x$, find $\frac{\text{d}y}{\text{d}x}.$

- Formal derivative operand: $5\operatorname{ln}x-3{x}^{2}+2x$.

- Ordered derivative RHS stages: $5(\frac{1}{x})-3\cdot 2x+2$ → $\frac{5}{x}-6x+2$

- Ordered point arithmetic RHS stages: none

- Source worked solution: Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(5\operatorname{ln}x-3{x}^{2}+2x) \\  & =5(\frac{1}{x})-3\cdot 2x+2 \\  & =\frac{5}{x}-6x+2.\end{aligned}
$$


### q-339973

- Observed label: :question.difficulty/hard

- Parameters: `{"a": 2, "r": "pi", "c": 1}`

- Prompt: Given that $y=2\operatorname{ln}x+{x}^{\pi }+1$, find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}

- Formal derivative operand: $2\operatorname{ln}x+{x}^{\pi }+1$.

- Ordered derivative RHS stages: $2(\frac{1}{x})+\pi {x}^{\pi -1}$ → $\frac{2}{x}+\pi {x}^{\pi -1}$

- Ordered point arithmetic RHS stages: none

- Source worked solution: Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(2\operatorname{ln}x+{x}^{\pi }+1) \\  & =2(\frac{1}{x})+\pi {x}^{\pi -1} \\  & =\frac{2}{x}+\pi {x}^{\pi -1}.\end{aligned}
$$


### q-101716

- Observed label: :question.difficulty/easy

- Parameters: `{"a": 2, "b": 7, "c": -10, "d": -1}`

- Prompt: Calculate $\frac{\text{d}y}{\text{d}x}$ for $y=2\operatorname{ln}⁡x-10x+7{x}^{3}-1.$

- Formal derivative operand: $2\operatorname{ln}⁡x-10x+7{x}^{3}-1$.

- Ordered derivative RHS stages: $2(\frac{1}{x})-10+21{x}^{2}$ → $\frac{2}{x}-10+21{x}^{2}$

- Ordered point arithmetic RHS stages: none

- Source worked solution: Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(2\operatorname{ln}⁡x-10x+7{x}^{3}-1) \\  & =2(\frac{1}{x})-10+21{x}^{2} \\  & =\frac{2}{x}-10+21{x}^{2}.\end{aligned}
$$


### q-11911

- Observed label: :question.difficulty/easy

- Parameters: `{"a": 1, "b": 2}`

- Prompt: Given that $y=2x+ln⁡x$, find $\frac{\text{d}y}{\text{d}x}.$

- Formal derivative operand: $2x+ln⁡x$.

- Ordered derivative RHS stages: $2+\frac{1}{x}$

- Ordered point arithmetic RHS stages: none

- Source worked solution: Taking the derivative, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(2x+ln⁡x) \\  & =2+\frac{1}{x}.\end{aligned}
$$


### q-308854

- Observed label: :question.difficulty/hard

- Parameters: `{"a": 1, "b": 3, "r": "e", "t": 1}`

- Prompt: Given the function  $y=3{x}^{e}+ln⁡x,$ find the instantaneous rate of change at $x=1.$ Do not round the answer.

The instantaneous rate of change at $x=1$ is
{{field-1}}.

- Formal derivative operand: $3{x}^{e}+ln⁡x$.

- Ordered derivative RHS stages: $3e{x}^{e-1}+\frac{1}{x}$

- Ordered point arithmetic RHS stages: $3e\cdot {1}^{e-1}+\frac{1}{1}$ → $3e+1$

- Source worked solution: To find the instantaneous rate of change at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(3{x}^{e}+ln⁡x) \\  & =3e{x}^{e-1}+\frac{1}{x}.\end{aligned}
$$

Therefore, the instantaneous rate of change at $x=1$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1} & ={(3e{x}^{e-1}+\frac{1}{x})|}_{x=1} \\  & =3e\cdot {1}^{e-1}+\frac{1}{1} \\  & =3e+1\,.\end{aligned}
$$


### q-340099

- Observed label: :question.difficulty/easy

- Parameters: `{"a": 2, "b": 1, "t": 1}`

- Prompt: Given the function  $y=2\operatorname{ln}⁡x+{e}^{x}$, find the instantaneous rate of change at $x=1.$ Do not round the answer.

The instantaneous rate of change at $x=1$ is
{{field-1}}.

- Formal derivative operand: $2\operatorname{ln}⁡x+{e}^{x}$.

- Ordered derivative RHS stages: $\frac{2}{x}+{e}^{x}$

- Ordered point arithmetic RHS stages: $\frac{2}{1}+{e}^{1}$ → $2+e$

- Source worked solution: To find the instantaneous rate of change at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(2\operatorname{ln}⁡x+{e}^{x}) \\  & =\frac{2}{x}+{e}^{x}.\end{aligned}
$$

Therefore, the instantaneous rate of change at $x=1$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1} & ={(\frac{2}{x}+{e}^{x})|}_{x=1} \\  & =\frac{2}{1}+{e}^{1} \\  & =2+e\,.\end{aligned}
$$


### q-340100

- Observed label: :question.difficulty/easy

- Parameters: `{"a": -3, "b": 2, "c": 4, "t": 2}`

- Prompt: Given the function  $y=-3\operatorname{ln}⁡x+2{e}^{x}+4$, find the instantaneous rate of change at $x=2.$ Do not round the answer.

The instantaneous rate of change at $x=2$ is
{{field-1}}.

- Formal derivative operand: $-3\operatorname{ln}⁡x+2{e}^{x}+4$.

- Ordered derivative RHS stages: $-\frac{3}{x}+2{e}^{x}$

- Ordered point arithmetic RHS stages: $-\frac{3}{2}+2{e}^{2}$

- Source worked solution: To find the instantaneous rate of change at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(-3\operatorname{ln}⁡x+2{e}^{x}+4) \\  & =-\frac{3}{x}+2{e}^{x}.\end{aligned}
$$

Therefore, the instantaneous rate of change at $x=2$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=2} & ={(-\frac{3}{x}+2{e}^{x})|}_{x=2} \\  & =-\frac{3}{2}+2{e}^{2}\,.\end{aligned}
$$


### q-340104

- Observed label: :question.difficulty/easy

- Parameters: `{"a": 4, "b": "-1/3", "base": 2, "c": 5, "t": 2}`

- Prompt: Given the function  $y=4ln⁡x-\frac{1}{3}\cdot {2}^{x}+5$, find the instantaneous rate of change at $x=2.$ Do not round the answer.

The instantaneous rate of change at $x=2$ is
{{field-1}}.

- Formal derivative operand: $4ln⁡x-\frac{1}{3}\cdot {2}^{x}+5$.

- Ordered derivative RHS stages: $\frac{4}{x}-\frac{1}{3}\cdot {2}^{x}ln⁡(2)$

- Ordered point arithmetic RHS stages: $\frac{4}{2}-\frac{1}{3}\cdot {2}^{2}ln⁡(2)$ → $2-\frac{4}{3}ln⁡(2)$

- Source worked solution: To find the instantaneous rate of change at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(4ln⁡x-\frac{1}{3}\cdot {2}^{x}+5) \\  & =\frac{4}{x}-\frac{1}{3}\cdot {2}^{x}ln⁡(2).\end{aligned}
$$

Therefore, the instantaneous rate of change at $x=2$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=2} & ={(\frac{4}{x}-\frac{1}{3}\cdot {2}^{x}ln⁡(2))|}_{x=2} \\  & =\frac{4}{2}-\frac{1}{3}\cdot {2}^{2}ln⁡(2) \\  & =2-\frac{4}{3}ln⁡(2)\,.\end{aligned}
$$


### q-17392

- Observed label: :question.difficulty/hard

- Parameters: `{"a": -1, "b": 2, "r": "e", "t": 1}`

- Prompt: Given that $y=2{x}^{e}-ln⁡x$, find the instantaneous rate of change at $x=1.$

- Formal derivative operand: $2{x}^{e}-ln⁡x$.

- Ordered derivative RHS stages: $2e{x}^{e-1}-\frac{1}{x}$

- Ordered point arithmetic RHS stages: $2e\cdot {1}^{e-1}-\frac{1}{1}$ → $2e-1$

- Source worked solution: To find the instantaneous rate of change at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

Taking the derivative, we have 

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(2{x}^{e}-ln⁡x) \\  & =2e{x}^{e-1}-\frac{1}{x}.\end{aligned}
$$

Therefore, the instantaneous rate of change at $x=1$ is 

$$
\begin{aligned}{\frac{\text{d}y}{\text{d}x}|}_{x=1} & ={(2e{x}^{e-1}-\frac{1}{x})|}_{x=1} \\  & =2e\cdot {1}^{e-1}-\frac{1}{1} \\  & =2e-1\,.\end{aligned}
$$


##2. Shared pattern

Differentiate a finite sum containing a constant multiple of ln x term by term. Use the reciprocal derivative for ln x and the previously learned power/exponential rule for the other terms. Some observed tasks evaluate the derivative at a familiar positive point. Response is a derivative expression or exact scalar RHS; the captured radio/blank contract remains fixed per layout. Distinct source operative chains are retained, including the cubic/irrational-power substituted reciprocal row and the omission of redundant evaluation rows in q-340100.


##3. Full component and bank mapping

Every row below is an entire source option, preserving option count and correct designation. “Historical expression pattern” is an explicit parameterized replay formula, not a claim to have recovered the learner error. Those whole banks are ineligible for default learning. q-1920 raw ln(-5) is not a real-domain expression; it is preserved as malformed evidence, not reported as mathematically valid.


### observed:q-1919

| Source answer ID | Complete source expression | Key designation | Recipe/pattern |

|---|---|---|---|

| 1045aaaf-0a76-5469-afdc-876ec049ae29 | ${11}^{x}-ln⁡11-\frac{5}{x}$ | incorrect | historical expression pattern (opaque) |

| aa30aba2-91df-575b-9e42-a1c8a2d47cbf | ${11}^{x}ln⁡x-\frac{1}{x}$ | incorrect | historical expression pattern (opaque) |

| c13aff45-c853-5d8b-ae11-7b4d6befdcb6 | $ln⁡11+\frac{5}{x}$ | incorrect | historical expression pattern (opaque) |

| eff2509a-f3c8-5644-a073-b8761ffb95e6 | ${11}^{x}ln⁡11-\frac{5}{x}$ | correct | historical expression pattern (opaque) |

| ff507140-fe41-5deb-989d-ac21680f83b3 | ${11}^{x}-\frac{1}{x}$ | incorrect | historical expression pattern (opaque) |


### observed:q-1920

| Source answer ID | Complete source expression | Key designation | Recipe/pattern |

|---|---|---|---|

| 8847ec53-1ef1-5244-9261-3db213a50ea2 | $-5e^{x}\ln x + \frac{1}{x}$ | absent key | historical expression pattern (opaque) |

| af4a5664-c507-5fd9-af8c-e68ce9129a6b | $-5e^{x}\ln - 5 + \frac{2}{x}$ | absent key | historical expression pattern (opaque) |

| d160ad97-ce05-5c09-a415-37e669bc37d0 | $-e^{x} + \frac{1}{x}$ | absent key | historical expression pattern (opaque) |

| f0f5dc19-0891-5c65-ba47-3963e6e0a451 | $-5e^{x} - \ln 3 + \frac{2}{x}$ | absent key | historical expression pattern (opaque) |

| fdb7af8c-26aa-56d2-9b2c-2028d177a3e0 | $-5e^{x} + \frac{2}{x}$ | absent key | historical expression pattern (opaque) |


### observed:q-11914

| Source answer ID | Complete source expression | Key designation | Recipe/pattern |

|---|---|---|---|

| 3b2b9b31-ff69-5fd5-b05e-2f7659ff135f | $\frac{5}{x}+6x+2$ | incorrect | flip_quadratic_sign |

| 0d5c95ed-e8ad-537b-a8d6-7a28ab66e027 | $\frac{5}{x}-6x+2$ | correct | correct |

| 91dae272-a571-532b-b8c9-5f1a0d446765 | $\frac{1}{x}-6x+2$ | incorrect | drop_log_coefficient |

| 3b96cf13-3041-512c-817b-bce2b6cd16ae | $\frac{5}{x}-3x^{2}+2$ | incorrect | retain_quadratic |

| 441d1cc7-ac98-5400-9e91-3512f2bc8afd | $\frac{5}{x}-3x+2$ | incorrect | omit_power_multiplier_and_log |


### observed:q-339973

| Source answer ID | Complete source expression | Key designation | Recipe/pattern |

|---|---|---|---|

| 74933759-75c5-532d-af31-afd3380ef04d | $\frac{2}{x}+\pi {x}^{\pi -1}$ | correct | term derivatives, then point substitution when requested |


### observed:q-101716

| Source answer ID | Complete source expression | Key designation | Recipe/pattern |

|---|---|---|---|

| 0384a71b-bf28-515f-8b2b-476abb5fca12 | $\frac{1}{x}-10+7{x}^{2}$ | incorrect | drop_log_coefficient_and_power_multiplier |

| 4e8c24ce-0ee5-5eba-b662-bb6dcb3d78e8 | $\frac{1}{x}-10+21{x}^{2}$ | incorrect | drop_log_coefficient |

| 5659c514-e496-58f4-9efc-5892bb18fbec | $\frac{2}{x}-10+21{x}^{2}$ | correct | correct |

| 682d240f-295a-54b0-8f99-5ef92b911aaf | $\frac{2}{x}+10+21{x}^{3}$ | incorrect | flip_linear_and_retain_cubic_power |

| fee011ed-5418-5bfa-a0ce-9610f711b134 | $\frac{4}{x}+10+21{x}^{2}$ | incorrect | double_log_and_flip_linear |


### observed:q-11911

| Source answer ID | Complete source expression | Key designation | Recipe/pattern |

|---|---|---|---|

| 26bf5cf8-eaf1-5b10-8d2a-662c31b3b508 | $\frac{2}{x}$ | incorrect | historical expression pattern (opaque) |

| 783b0f4c-199c-5928-b08e-dcb4df838be4 | $2+\frac{2}{x}$ | incorrect | historical expression pattern (opaque) |

| 89f1e417-01f6-5b82-ba77-84fd142edcc2 | $\frac{1}{2x}$ | incorrect | historical expression pattern (opaque) |

| e0afa8a6-a60b-5d30-b8a6-b2c64b3b9e85 | $2x+\frac{1}{x}$ | incorrect | historical expression pattern (opaque) |

| fe2d11d8-637f-5d1f-abb2-68fd4be88574 | $2+\frac{1}{x}$ | correct | historical expression pattern (opaque) |


### observed:q-308854

| Source answer ID | Complete source expression | Key designation | Recipe/pattern |

|---|---|---|---|

| 9cae6982-03b7-597e-93e4-369fa68c8f5f | $3e+1$ | correct | term derivatives, then point substitution when requested |


### observed:q-340099

| Source answer ID | Complete source expression | Key designation | Recipe/pattern |

|---|---|---|---|

| 596bfc33-1d46-58a1-9057-d28b147c68d1 | $2+e$ | correct | term derivatives, then point substitution when requested |


### observed:q-340100

| Source answer ID | Complete source expression | Key designation | Recipe/pattern |

|---|---|---|---|

| 566f2bfd-9b10-5889-ad0c-475cdee4aa4a | $-\frac{3}{2}+2{e}^{2}$ | correct | term derivatives, then point substitution when requested |


### observed:q-340104

| Source answer ID | Complete source expression | Key designation | Recipe/pattern |

|---|---|---|---|

| 39500646-122f-5de4-a3f8-1b1dfa91aa61 | $2-\frac{4}{3}\operatorname{ln}(2)$ | correct | term derivatives, then point substitution when requested |


### observed:q-17392

| Source answer ID | Complete source expression | Key designation | Recipe/pattern |

|---|---|---|---|

| 0beb1ecb-7649-51d5-8923-8085f1d146bc | $2e$ | incorrect | omit_log |

| aa5ec049-b8d0-5c17-a28c-05813122674f | $2e-1$ | correct | correct |

| c2d87b1b-17a5-523c-a973-f5e0ad287cd3 | $2$ | incorrect | omit_power_multiplier_and_log |

| ea4f4094-0cfd-5ae4-8308-88f0b83b2c27 | $2e+1$ | incorrect | flip_log_sign |

| 946c0adc-baba-5359-a975-69b7a89f4838 | $-1$ | incorrect | omit_power |


### Separately authored banks

For q-1919 select the entire profile: correct; omit exponential ln(base) factor; use ln(x) in that factor; flip ln-term sign; omit exponential derivative. For q-1920: correct; flip exponential sign; drop ln coefficient; retain ln term; omit exponential derivative. For q-11911: correct; retain ln term; drop ln coefficient; retain linear term; omit linear derivative. These are operations on the displayed function; no unrelated additive/scale perturbation is used. Authored banks do not retain source feedback absent from their source. Other radios use the full observed, defensible method bank as parameterized above. Banks are selected before parameter sampling and rejected as a whole on expression equivalence; no first-valid distractor pooling.


##4. Reusable backbone and slots

Each template preserves the exact source prompt/solution prose, term order, field layout, formal derivative operator operand, ordered derivative RHS stages and ordered point-evaluation stages. The renderer performs one noncascading replacement pass over whole complete expressions; evaluation-point prose is a separately masked full x=point component. Feedback in q-11914 has its own dependent coefficient slots. Complete original banks are separately retained for replay.

Slots: nonzero integer coefficients have absolute values1..10, with original signs/roles enforced for quadratic/cubic/scaled point templates. Normal linear/base/exponential authored banks require nonunit ln coefficient so a coefficient-drop error stays distinct. Base is integer2..12 for moderate; evaluated easy base is2..5 with negative small rational coefficient -i/j, i∈{1,2}, j∈{2,3,4}. Familiar evaluation point remains1 for q-340099/hard power tasks and2 for scaled/base exponential tasks. Irrational exponent is pi or e, an observed constant-exponent number form; it is not an inner variable/function. Constants vary only as presentation parameters and do not inflate mathematical-task counts. Every explicit API input passes the same family-specific guards as random sampling.

Workload: source integer powers2/3 are fixed; varying their coefficient preserves the two or three substantive term derivatives and optional constant disappearance. Moderate keeps an uncomposed exponential derivative and reciprocal derivative. Hard keeps a constant irrational power derivative, coefficient/exponent factor and successor exponent, optionally evaluated at1. Sampling has no progression within any difficulty. q-339973 has18 distinct meaningful coefficient/exponent tasks under positive default sign; the hard point families provide162 each (9 positive or negative log coefficients×9 power coefficients×2 exponent forms), with no need to invent another branch. Default sampling serves every family, verified independently.

Domain: x>0 before simplification, with positive evaluation points. ln x remains ln x; no general-base logarithm, ln(composite), product/quotient rule or chain rule is introduced. Source non-e exponential functions are in this KP and do not constitute a general-base logarithm branch.

Identity: deterministic UUID/content fingerprint from version,difficulty,actual prompt,fixed solution,complete displayed bank and field type, independent of seed/order. Mathematical fingerprint from the reduced derivative and assessed evaluation/response role excludes incidental constant shifts and bank aliases.

Raw anomalies: q-1920 retains absent difficulty/key/solution and invalid ln(-5); default supplies an independently derived key, fixed source-style derivative solution and supported complete bank, labeled authored. Source solutions10/10 and designations10/10 use their own denominators; the missing entries cannot count as matches. Native raw q-1920 is not fixture-gradable without inventing a key. The four captured Do not round blanks preserve wording in replay; normal wording is minimally repaired to Give an exact answer because the native grader treats round as form-sensitive. No engine edits.

Plots: none. Plot extraction and rendering are therefore unnecessary.


## Minimal scalar notation repair and native limitations

Decoded q-308854 stored answer bytes are exactly3e+1 (Unicode code points51,101,43,49), with no TeX command or multiplication symbol. This is correct intended displayed algebra but ambiguous mathematical input: the captured native parser can read3e+1 as scientific notation30. native-semantic-probe.json retains a diagnostic copy of the original question with only its form restriction removed; the native grader accepts30 and rejects3\cdot e+1 against that storage. This copy is not a source fidelity record or eligible question. Normal authored q-308854 retains the response shape and ordered stages but stores and concludes3\cdot e+1 at the anchor, varying its coefficient consistently. Against corrected storage the native engine rejects30 and accepts1+3*e and(6\cdot e+2)/2. Raw original replay remains ineligible.

The ordinary native fixture includes canonical, reordered-term, unreduced-scalar and incorrect entries. Correct irrational-power derivative common-denominator entries are independently equivalent by SymPy but return unresolved from the native symbolic rules. This is reported as a grading limitation, not passed correctness. All faithful source blanks remain available through the public observed profiles, and normal canonical shapes are retained. validation.json separates successful valid-normal grading from excluded raw source/engine equivalent-answer limits; validate.py passes valid normal contracts and reports faithful raw evidence limitations separately. No native engine changes are made.


## Authored hard radio adaptation (source blank retained)

Normal profile authored:q-339973 preserves the source function and derivative request, all three source derivative RHS stages and shared prose; it removes only the original blank scaffolding and supplies an authored radio field named selection. Five-choice radio assessment is already observed in this KP at easy/moderate/hard. Its complete profile, chosen before coefficients, is: correct a/x+r*x^(r-1); omit ln coefficient, 1/x+r*x^(r-1); omit power exponent factor, a/x+x^(r-1); fail exponent decrement, a/x+r*x^r; flip reciprocal derivative sign, -a/x+r*x^(r-1). The log coefficient remains nonunit, r is pi/e, and the entire instance is rejected on any collision. Readback independently extracts a and r from the printed function and checks this exact full bank. This is an explicit answer-field adaptation at the same differentiation workload, not an observed field label or new mathematical branch. The public observed:q-339973 profile still has its original one-choice blank, placeholder, source prose, stages and correct designation. It remains evidence-only, and its common-denominator equivalent unresolved result is retained in the native report.

All observed profiles are evidence-only. Normal native fixtures verify every radio option and every supported scalar canonical, swapped-addition, unreduced-denominator and wrong-value entry. Known raw form/semantic failures are labeled excluded evidence; they do not count as passing mathematical grading. No field type is silently altered in raw replay. Mathematical fingerprints exclude field-layout aliases, profiles/banks and incidental constants; raw and authored q-339973 at the same parameters share the mathematical fingerprint and have different content identities.
