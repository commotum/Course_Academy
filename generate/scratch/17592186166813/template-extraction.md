# Template extraction — all four stages

Provenance matches source.json: math basis1356, captured lineage. Original prompt, exact field shapes, complete bank and whole solution follow for every practice case. No source is omitted. Exact whitespace in the blank is preserved by source.json and public observed replay; code fences below show decoded strings.

## Stage1 — describe originals before generalizing

### q-95982 / easy

Derivative occurrence orders, in printed order: [2, 1]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
What is the order of the ordinary differential equation $\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}+{x}^{3}y=5{y}^{4}\frac{\text{d}y}{\text{d}x}?$
```

Full worked solution:

```text
The order of an ordinary differential equation (ODE) is the order of the highest derivative in the equation.

The highest derivative in the given ODE is $\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}},$ which has order $2.$

Therefore, the order of the ODE is $2.$
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| selection | :answer-field.type/radio | :answer.type/math | 4, 1, 2, 3, 5 | 2 |


Source solution stages: 3 double-newline paragraphs; exact sentence sequence above. Definition → identify highest derivative and order → conclusion; q-167787 additionally restates an equation and includes whitespace paragraphs. No solution-stage omissions introduced.

### q-95983 / moderate

Derivative occurrence orders, in printed order: [3, 1, 2, 1, 1, 1, 2]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
Which of the following are third-order ordinary differential equations?

Select all that apply.

- **I.** ${y}^{‴}+3x{y}^{′}=xy$
- **II.** $3{y}^{″}{y}^{′}-2xy=2{y}^{′}$
- **III.** ${x}^{3}{y}^{′}-2x={y}^{″}$
```

Full worked solution:

```text
A differential equation is of third-order if the largest derivative term in the equation is ${y}^{‴}.$

Keeping this in mind, let's check each given equation.

- Equation I is a third-order differential equation. The highest derivative in this equation is ${y}^{‴}.$

- Equation II is not a third-order differential equation. The highest derivative in this equation is ${y}^{″},$ so this is a second-order differential equation.

- Equation III is not a third-order differential equation. The highest derivative in this equation is ${y}^{″},$ so this is a second-order differential equation.

Therefore, the correct answer is "I only."
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| I | :answer-field.type/checkbox | :answer.type/text | false, true | true |

| II | :answer-field.type/checkbox | :answer.type/text | false, true | false |

| III | :answer-field.type/checkbox | :answer.type/text | false, true | false |


Source solution stages: 6 double-newline paragraphs; exact sentence sequence above. Target-order definition → invitation to check → I classification → II classification → III classification → selected-set conclusion. No solution-stage omissions introduced.

### q-118780 / easy

Derivative occurrence orders, in printed order: [7, 1, 8]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
What is the order of the ordinary differential equation ${x}^{2}\frac{{\text{d}}^{7}y}{\text{d}{x}^{7}}-9{x}^{7}\frac{\text{d}y}{\text{d}x}=2\frac{{\text{d}}^{8}y}{\text{d}{x}^{8}}?$
```

Full worked solution:

```text
The order of an ordinary differential equation (ODE) is the order of the highest derivative in the equation.

The highest derivative in the given ODE is $\frac{{\text{d}}^{8}y}{\text{d}{x}^{8}},$ which has order $8.$

Therefore, the order of the ODE is $8.$
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| selection | :answer-field.type/radio | :answer.type/math | 9, 6, 8, 2, 7 | 8 |


Source solution stages: 3 double-newline paragraphs; exact sentence sequence above. Definition → identify highest derivative and order → conclusion; q-167787 additionally restates an equation and includes whitespace paragraphs. No solution-stage omissions introduced.

### q-118782 / moderate

Derivative occurrence orders, in printed order: [2, 1, 2, 3, 2]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
Which of the following are second-order ordinary differential equations?

Select all that apply.

- **I.** $9x{y}^{''}+8{y}^{'}=4$
- **II.** $\sqrt{{y}^{''}+x}=3y$
- **III.** ${y}^{‴}+{x}^{2}{y}^{''}=3$
```

Full worked solution:

```text
A differential equation is of second-order if the largest derivative term in the equation is ${y}^{''}.$

Keeping this in mind, let's check each given equation.

- Equation I is a second-order differential equation. The highest derivative in this equation is ${y}^{''}.$

- Equation II is also a second-order differential equation. The highest derivative in this equation is ${y}^{''}.$

- Equation III is not a second-order differential equation. The highest derivative in this equation is ${y}^{‴},$ so this is a third-order differential equation.

Therefore, the correct answer is "I and II only."
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| I | :answer-field.type/checkbox | :answer.type/text | false, true | true |

| II | :answer-field.type/checkbox | :answer.type/text | false, true | true |

| III | :answer-field.type/checkbox | :answer.type/text | false, true | false |


Source solution stages: 6 double-newline paragraphs; exact sentence sequence above. Target-order definition → invitation to check → I classification → II classification → III classification → selected-set conclusion. No solution-stage omissions introduced.

### q-96669 / moderate

Derivative occurrence orders, in printed order: [3, 1, 2, 1, 1, 1]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
Which of the following are first-order ordinary differential equations?

Select all that apply.

- **I.** ${y}^{‴}+(\operatorname{sin}⁡x){y}^{′}={x}^{2}y$
- **II.** $5{y}^{″}{y}^{′}+3xy=4{y}^{′}$
- **III.** ${({y}^{′})}^{2}-2{x}^{2}=y$
```

Full worked solution:

```text
A differential equation is of first-order if the largest derivative term in the equation is ${y}^{′}.$

Keeping this in mind, let's check each given equation.

- Equation I is not a first-order differential equation. The highest derivative in this equation is ${y}^{‴},$ so this is a third-order differential equation.

- Equation II is not a first-order differential equation. The highest derivative in this equation is ${y}^{″},$ so this is a second-order differential equation.

- Equation III is a first-order differential equation. The highest derivative in this equation is ${y}^{′}.$

Therefore, the correct answer is "III only."
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| I | :answer-field.type/checkbox | :answer.type/text | false, true | false |

| II | :answer-field.type/checkbox | :answer.type/text | false, true | false |

| III | :answer-field.type/checkbox | :answer.type/text | false, true | true |


Source solution stages: 6 double-newline paragraphs; exact sentence sequence above. Target-order definition → invitation to check → I classification → II classification → III classification → selected-set conclusion. No solution-stage omissions introduced.

### q-96676 / moderate

Derivative occurrence orders, in printed order: [2, 1, 1, 1]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
Which of the following are first-order ordinary differential equations?

Select all that apply.

- **I.** $3{y}^{''}+2x{y}^{'}={x}^{2}y$
- **II.** $5{x}^{2}y+3{y}^{5}{y}^{'}=4x$
- **III.** $\sqrt{{y}^{2}+{y}^{'}}+7{x}^{3}={e}^{y}$
```

Full worked solution:

```text
A differential equation is of first-order if the largest derivative term in the equation is ${y}^{'}.$

Keeping this in mind, let's check each given equation.

- Equation I is not a first-order differential equation. The highest derivative in this equation is ${y}^{''},$ so this is a second-order differential equation.

- Equation II is a first-order differential equation. The highest derivative in this equation is ${y}^{'}.$

- Equation III is also a first-order differential equation. The highest derivative in this equation is ${y}^{'}.$

Therefore, the correct answer is "II and III only."
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| I | :answer-field.type/checkbox | :answer.type/text | false, true | false |

| II | :answer-field.type/checkbox | :answer.type/text | false, true | true |

| III | :answer-field.type/checkbox | :answer.type/text | false, true | true |


Source solution stages: 6 double-newline paragraphs; exact sentence sequence above. Target-order definition → invitation to check → I classification → II classification → III classification → selected-set conclusion. No solution-stage omissions introduced.

### q-96680 / moderate

Derivative occurrence orders, in printed order: [1, 2, 3, 1, 1, 1]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
Which of the following are first-order ordinary differential equations?

Select all that apply.

- **I.** $3{y}^{'}+2x{y}^{''}={x}^{2}y$
- **II.** $5{x}^{2}{y}^{‴}+3x{y}^{'}={e}^{x}$
- **III.** $4{({y}^{'})}^{3}+7{x}^{3}=x({y}^{2}+{({y}^{'})}^{2})$
```

Full worked solution:

```text
A differential equation is of first-order if the largest derivative term in the equation is ${y}^{'}.$

Keeping this in mind, let's check each given equation.

- Equation I is not a first-order differential equation. The highest derivative in this equation is ${y}^{''},$ so this is a second-order differential equation.

- Equation II is not a first-order differential equation. The highest derivative in this equation is ${y}^{‴},$ so this is a third-order differential equation.

- Equation III is a first-order differential equation. The highest derivative in this equation is ${y}^{'}.$

Therefore, the correct answer is "III only."
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| I | :answer-field.type/checkbox | :answer.type/text | false, true | false |

| II | :answer-field.type/checkbox | :answer.type/text | false, true | false |

| III | :answer-field.type/checkbox | :answer.type/text | false, true | true |


Source solution stages: 6 double-newline paragraphs; exact sentence sequence above. Target-order definition → invitation to check → I classification → II classification → III classification → selected-set conclusion. No solution-stage omissions introduced.

### q-167787 / easy

Derivative occurrence orders, in printed order: [4, 2, 1]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
Consider the following differential equation.

$$
{x}^{3}\frac{{\text{d}}^{4}y}{\text{d}{x}^{4}}-x\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}+\frac{\text{d}y}{\text{d}x}=f(x)
$$

The order of this differential equation is

                            
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        .
```

Full worked solution:

```text
We have the differential equation

$$
{x}^{3}\frac{{\text{d}}^{4}y}{\text{d}{x}^{4}}-x\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}+\frac{\text{d}y}{\text{d}x}=\frac{1}{2}{e}^{x}.
$$

 

The order of an ordinary differential equation (ODE) is the order of the highest derivative in the equation.

The highest derivative in the given ODE is $\frac{{\text{d}}^{4}y}{\text{d}{x}^{4}},$ which has order $4.$

Therefore, the order of the ODE is $4.$
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| field-1 | :answer-field.type/blank | :answer.type/math | 4 | 4 |


Source solution stages: 6 double-newline paragraphs; exact sentence sequence above. Definition → identify highest derivative and order → conclusion; q-167787 additionally restates an equation and includes whitespace paragraphs. No solution-stage omissions introduced.

### q-118779 / easy

Derivative occurrence orders, in printed order: [6, 3]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
What is the order of the ordinary differential equation $y\frac{{\text{d}}^{6}y}{\text{d}{x}^{6}}+3x\frac{{\text{d}}^{3}y}{\text{d}{x}^{3}}={x}^{8}?$
```

Full worked solution:

```text
The order of an ordinary differential equation (ODE) is the order of the highest derivative in the equation.

The highest derivative in the given ODE is $\frac{{\text{d}}^{6}y}{\text{d}{x}^{6}},$ which has order $6.$

Therefore, the order of the ODE is $6.$
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| selection | :answer-field.type/radio | :answer.type/math | 6, 8, 7, 3, 4 | 6 |


Source solution stages: 3 double-newline paragraphs; exact sentence sequence above. Definition → identify highest derivative and order → conclusion; q-167787 additionally restates an equation and includes whitespace paragraphs. No solution-stage omissions introduced.

### q-118781 / easy

Derivative occurrence orders, in printed order: [3, 4]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
What is the order of the ordinary differential equation $x\frac{{\text{d}}^{3}y}{\text{d}{x}^{3}}-{y}^{2}\frac{{\text{d}}^{4}y}{\text{d}{x}^{4}}={y}^{5}?$
```

Full worked solution:

```text
The order of an ordinary differential equation (ODE) is the order of the highest derivative in the equation.

The highest derivative in the given ODE is $\frac{{\text{d}}^{4}y}{\text{d}{x}^{4}},$ which has order $4.$

Therefore, the order of the ODE is $4.$
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| selection | :answer-field.type/radio | :answer.type/math | 4, 3, 2, 6, 5 | 4 |


Source solution stages: 3 double-newline paragraphs; exact sentence sequence above. Definition → identify highest derivative and order → conclusion; q-167787 additionally restates an equation and includes whitespace paragraphs. No solution-stage omissions introduced.

### q-118783 / moderate

Derivative occurrence orders, in printed order: [2, 1, 3, 2, 1]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
Which of the following are second-order ordinary differential equations?

Select all that apply.

- **I.** ${y}^{″}+{y}^{′}={x}^{2}-x$
- **II.** ${y}^{‴}-y=x-{y}^{″}$
- **III.** ${x}^{3}{y}^{′}+x=y$
```

Full worked solution:

```text
A differential equation is of second-order if the largest derivative term in the equation is ${y}^{″}.$

Keeping this in mind, let's check each given equation.

- Equation I is a second-order differential equation. The highest derivative in this equation is ${y}^{″}.$

- Equation II is not a second-order differential equation. The highest derivative in this equation is ${y}^{‴},$ so this is a third-order differential equation.

- Equation III is not a second-order differential equation. The highest derivative in this equation is ${y}^{′},$ so this is a first-order differential equation.

Therefore, the correct answer is "I only."
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| I | :answer-field.type/checkbox | :answer.type/text | false, true | true |

| II | :answer-field.type/checkbox | :answer.type/text | false, true | false |

| III | :answer-field.type/checkbox | :answer.type/text | false, true | false |


Source solution stages: 6 double-newline paragraphs; exact sentence sequence above. Target-order definition → invitation to check → I classification → II classification → III classification → selected-set conclusion. No solution-stage omissions introduced.

### q-96662 / easy

Derivative occurrence orders, in printed order: [3, 2]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
What is the order of the ordinary differential equation $\frac{{\text{d}}^{3}y}{\text{d}{x}^{3}}+5{y}^{2}\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}+3{y}^{5}=0?$
```

Full worked solution:

```text
The order of an ordinary differential equation (ODE) is the order of the highest derivative in the equation.

The highest derivative in the given ODE is $\frac{{\text{d}}^{3}y}{\text{d}{x}^{3}},$ which has order $3.$

Therefore, the order of the ODE is $3.$
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| selection | :answer-field.type/radio | :answer.type/math | 5, 1, 2, 3, 4 | 3 |


Source solution stages: 3 double-newline paragraphs; exact sentence sequence above. Definition → identify highest derivative and order → conclusion; q-167787 additionally restates an equation and includes whitespace paragraphs. No solution-stage omissions introduced.

### q-96663 / easy

Derivative occurrence orders, in printed order: [4, 2, 1]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
What is the order of the ordinary differential equation $y\frac{{\text{d}}^{4}y}{\text{d}{x}^{4}}-4{x}^{2}\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}+\operatorname{sin}⁡x\frac{\text{d}y}{\text{d}x}=2x?$
```

Full worked solution:

```text
The order of an ordinary differential equation (ODE) is the order of the highest derivative in the equation.

The highest derivative in the given ODE is $\frac{{\text{d}}^{4}y}{\text{d}{x}^{4}},$ which has order $4.$

Therefore, the order of the ODE is $4.$
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| selection | :answer-field.type/radio | :answer.type/math | 1, 5, 2, 4, 3 | 4 |


Source solution stages: 3 double-newline paragraphs; exact sentence sequence above. Definition → identify highest derivative and order → conclusion; q-167787 additionally restates an equation and includes whitespace paragraphs. No solution-stage omissions introduced.

### q-96672 / moderate

Derivative occurrence orders, in printed order: [2, 1, 2, 1, 1, 3, 1]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
Which of the following are second-order ordinary differential equations?

Select all that apply.

- **I.** ${y}^{″}{x}^{3}-2y{y}^{′}=\operatorname{sin}⁡x$
- **II.** $3{y}^{″}{y}^{′}-2y=2{y}^{′}$
- **III.** $4{y}^{‴}x-7{x}^{2}{y}^{′}=y{e}^{x}$
```

Full worked solution:

```text
A differential equation is of second-order if the largest derivative term in the equation is ${y}^{″}.$

Keeping this in mind, let's check each given equation.

- Equation I is a second-order differential equation. The highest derivative in this equation is ${y}^{″}.$

- Equation II is also a second-order differential equation. The highest derivative in this equation is ${y}^{″}.$

- Equation III is not a second-order differential equation. The highest derivative in this equation is ${y}^{‴},$ so this is a third-order differential equation.

Therefore, the correct answer is "I and II only."
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| I | :answer-field.type/checkbox | :answer.type/text | false, true | true |

| II | :answer-field.type/checkbox | :answer.type/text | false, true | true |

| III | :answer-field.type/checkbox | :answer.type/text | false, true | false |


Source solution stages: 6 double-newline paragraphs; exact sentence sequence above. Target-order definition → invitation to check → I classification → II classification → III classification → selected-set conclusion. No solution-stage omissions introduced.


## Stage2 — shared pattern and response

Scalar: recognize each formal Leibniz derivative, read its differentiation order, take the maximum across the full equation, and return that integer through the original radio or blank. Ordinary x/y exponents and coefficient functions do not determine order. Three-way selection: read requested order and independently compare it with the largest prime/Leibniz derivative in each equation; preserve one checkbox field for each I/II/III. Products, powers or a square root containing a derivative do not change the derivative's order. Nothing is differentiated or solved.

## Stage3 — components and complete original choice mapping

`choice-recipes.json` maps all73 original choices to owning field, original UUID, exact value, correct designation, recipe, original parameters and bank profile. It is generated from immutable source evidence and cross-checked by validate.py, not an answer lookup used by generation. Source numerical offset recipes are interpretation-limited explicit replay catalogs; no arbitrary numerical regression is promoted as a historical error operation. Source checkbox banks always contain false and true. Their keys remain I/II/III and their correct choice derives from printed highest order equal to target. The blank contains a single math answer and retains {{field-1}}.

The source renderer masks **whole derivative components**, including their full numerator and denominator. It also slots complete ordinal words in prose and the whole $n.$ order fragment in scalar conclusions. No blind coefficient substitution touches prose, function names, labels or derivative arguments. Variable/component notation style remains exact whenever order is unchanged; changed prime orders above3 switch to unambiguous Leibniz notation. No derivative-free equation can be generated.

## Stage4 — reusable masks, domains and computations

Public observed replay: template is the source ID, profile observed; parameters are a complete `orders` dictionary from old source order to new order. Values are integer1–8, strictly increasing in old-order order; every source-relative radio option must stay positive, distinct, and include the new highest exactly once. Thus preserved source sentence truth and selected-set layout remain valid. The entire complete bank is chosen before rendering and rejected together on collision/domain failure. Original maps are identity maps; every source is also tested with a nonidentity map through the same public API. Raw q-167787 RHS prose anomaly remains visible; source_repaired changes only the wrong restated RHS.

Authored easy: n3–7; m1–n−2; ordinary exponent e in n+2..9. Left layout yD_n+3xD_m=x^e; right layout x^eD_m−3x=yD_n. Both have exactly two derivative occurrences. Correct n; complete bank [n,m,e,n−1,n+1]. Wrong operations read lower derivative, read an ordinary exponent, or count one too few/many differentiations. All five values are distinct under the bounds; the profile is selected as a whole. The source numerical banks motivate recognition of ordinary exponents and nearby order labels, without asserting recovered intention. Seventy meaningful bounded tasks are exhaustively checked; coefficient and variable aliases do not inflate counts.

Authored moderate: target and each of three highest orders1–3, forms0–2. Per-equation forms are D_n+3xD_1=x^5 y; sqrt(D_n+x)=3y^4; (D_n)^2+xD_1=y^5. Same first–third-order membership judgment in all forms, with one or two derivative occurrences; prime glyphs match observed source conventions. All2187 semantic parameter combinations are exhaustively checked. The second form reduces derivative occurrence count as in observed q-118782 but still requires reading derivative under a radical rather than confusing its power/placement with order.

Authored hard: target and each highest order4–8; lower m1..n−2; highest-derivative power2–5; ordinary exponent e in n+1..10; layout0–2. Define A=D_m(D_n)^p, B=x^eD_1, C=yD_(m+1). Layouts are A+B=C, A=B+C, B+C=A. Each has exactly four derivative occurrences; orders m and m+1 are lower than n, and highest power and ordinary exponent are irrelevant to true order. Boolean bank and full definition/check-each/conclusion solution remain fixed independently of a selected learner error. The factorized finite catalog has840 genuinely distinct per-equation structures, independently enumerated and parsed. Ordered three-equation tasks with five target orders total5×840³=2963520000; this is a factorized bound, not a claim to render billions of questions. Powers/exponents and equation-side placement are retained because they create distinct order-versus-exponent/read-all-terms recognition tasks; symbol names, coefficients, profile and seed are excluded.

Mathematics reads back actual displayed derivatives independently in validate.py; exact derivative counts are confirmed with SymPy. Public generation stores domain, complete recipe set, source lineage, actual Python/SymPy versions, seed and original parameters outside learner content. Mathematical task identity excludes bank/profile/seed and coefficient magnitudes; content identity includes version, level, actual prompt, entire fixed solution, full displayed bank and correct values. Shuffling radio options cannot change identity. Distinct non-order coefficients are not exposed as purported task diversity.

All original profiles and variants appear in review.md/review.json, followed by at least two clearly labeled authored examples per level. No plots, native engine edits, database writes or post-step7 registration occur.
