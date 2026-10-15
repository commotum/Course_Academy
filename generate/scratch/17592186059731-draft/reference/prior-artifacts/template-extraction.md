# Template extraction

## Stage 1: describe each source specifically

### q-1348

Let $p=[\begin{aligned}7 \\ n\end{aligned}]$ and $q=[\begin{aligned}4 \\ -4\end{aligned}].$ Given that $p⊥q$, find the value of $n.$

Template `linear2`; original difficulty `:question.difficulty/easy`; field `selection`, `:answer-field.type/radio`; complete math bank: `11`, `7`, `\frac{3}{4}`, `14`, `-7`.

Original parameters: `{"a": 7, "b": 4, "c": -4}`. Correct designation: `7`.

### q-317932

If $c=[\begin{aligned}k \\ 2k \\ 4\end{aligned}],$ $d=[\begin{aligned}-3 \\ 2 \\ 2\end{aligned}],$ and $c⊥d,$ then $k=${{field-1}}.

Template `linear3`; original difficulty `:question.difficulty/easy`; field `field-1`, `:answer-field.type/blank`; complete math bank: `-8`.

Original parameters: `{"a": 2, "b": 4, "c": -3, "d": 2, "e": 2}`. Correct designation: `-8`.

### q-317945

Let $a=⟨2{x}^{2},-4⟩$ and $b=⟨8,4⟩.$ If $a⊥b$ and $x>0,$ then $x=${{field-1}}.

Template `square2_blank`; original difficulty `:question.difficulty/easy`; field `field-1`, `:answer-field.type/blank`; complete math bank: `1`.

Original parameters: `{"a": 2, "b": -4, "c": 8, "d": 4, "sign": 1}`. Correct designation: `1`.

### q-19021

Let $u = \begin{bmatrix}x \\ -2\end{bmatrix}$ and $v = \begin{bmatrix}x \\ 2\end{bmatrix}$. Given that $u⊥v$ and $x > 0$, find the value of $x$.

Template `square2_shared`; original difficulty `UNRATED`; field `selection`, `:answer-field.type/radio`; complete math bank: `3`, `8`, `1`, `4`, `2`.

Original parameters: `{"a": 2, "sign": 1}`. Correct designation: MISSING; independent derivation supplies it, without claiming source designation fidelity.

### q-101417

Let $u=[\begin{aligned}9 \\ 2x\end{aligned}]$ and $v=[\begin{aligned}-2 \\ x\end{aligned}].$ Given that $u⊥v$ and $x<0$, find the value of $x.$

Template `square2_scaled`; original difficulty `:question.difficulty/moderate`; field `selection`, `:answer-field.type/radio`; complete math bank: `-1`, `-5`, `-3`, `-4`, `-2`.

Original parameters: `{"a": 9, "b": 2, "c": -2, "sign": -1}`. Correct designation: `-3`.

### q-19023

Let $g=[\begin{aligned}{r}^{2} \\ -1 \\ -6\end{aligned}]$ and $h=[\begin{aligned}3 \\ {r}^{2} \\ 2\end{aligned}].$ Given that $g⊥h$ and $r<0$, find the value of $r.$

Template `square3_collect`; original difficulty `:question.difficulty/moderate`; field `selection`, `:answer-field.type/radio`; complete math bank: `-\sqrt{12}`, `-6`, `-12`, `-\sqrt{6}`, `-3`.

Original parameters: `{"a": 1, "b": 3, "c": -1, "d": 1, "e": -6, "f": 2, "sign": -1}`. Correct designation: `-\sqrt{6}`.

### q-77152

Let $u=[\begin{aligned}a \\ 2 \\ 4\end{aligned}]$ and $v=[\begin{aligned}a \\ -4 \\ -2\end{aligned}].$ Given that $u⊥v$ and $a<0$, find the value of $a.$

Template `square3_shared`; original difficulty `:question.difficulty/moderate`; field `selection`, `:answer-field.type/radio`; complete math bank: `-9`, `-1`, `-2`, `-8`, `-4`.

Original parameters: `{"a": 2, "b": 4, "c": -4, "d": -2, "sign": -1}`. Correct designation: `-4`.

### q-19022

What is the value of $x$ given that $a = ⟨x,-6x, 3⟩, b = ⟨x, 1, 3⟩$ and $a⊥b$?

Template `repeated3`; original difficulty `UNRATED`; field `selection`, `:answer-field.type/radio`; complete math bank: `-6`, `6`, `3`, `9`, `-3`.

Original parameters: `{"t": 3}`. Correct designation: MISSING; independent derivation supplies it, without claiming source designation fidelity.

## Stage 2: generalized assessed pattern

Two named vectors in column or angle notation contain one unknown. Multiply matching components, add, use perpendicularity iff dot product zero, solve the resulting linear/square equation, then apply any supplied root sign. The fragment is the unknown value; the fixed solution does not depend on selected error. Source q-19022 specifically reduces to a repeated square; its generalization keeps that sole-root shape. General quadratic solving is excluded.

## Stage 3: complete component and bank mapping

Every prompt component is a complete vector-coordinate slot, vector name, unknown or inequality. Source cases preserve original fields, full exact bank, UUIDs and captured correct refs. All six available solution prose strings and stage sequences replay byte-for-byte; missing solutions are authored. Source constants and opaque bank ratios below describe explicit evidence-only parameterizations and do not imply author intent.

| Source/profile | Computed root / dot equation | Ordered full bank recipe | Status |

|---|---|---|---|

| q-1348 / observed_q1348 | R=−ab/c; ab+cn=0 | R·(11/7,1,3/28,2,−1) | all 5 values reproduced; wrong-scalar intent opaque |

| q-19021 / observed_q19021 | R=sqrt(a²); x²−a²=0, x>0 | R·(3/2,4,1/2,2,1) | all 5 values reproduced; wrong-scalar intent opaque |

| q-19022 / observed_q19022 | R=t; x²−2tx+t²=0 | R·(−2,2,1,3,−1) | all 5 values reproduced; wrong-scalar intent opaque |

| q-101417 / observed_q101417 | R=s·sqrt(−ac/b); ac+bx²=0 | R·(1/3,5/3,1,4/3,2/3) | all 5 values reproduced; wrong-scalar intent opaque |

| q-19023 / observed_q19023 | Q=−ef/(ab+cd), R=s·sqrt(Q) | (s·sqrt(2Q), sQ, 2sQ, R, sQ/2) | all 5 values reproduced; wrong-scalar intent opaque |

| q-77152 / observed_q77152 | Q=−(ac+bd), R=s·sqrt(Q) | R·(9/4,1/4,1/2,2,1) | all 5 values reproduced; wrong-scalar intent opaque |

Blanks: q-317932 computes `R=−be/(c+ad)` from `<k,ak,b>·<c,d,e>`; field-1 value −8. q-317945 computes `R=s·sqrt(−bd/(ac))` from `<ax²,b>·<c,d>`; field-1 value 1. These have no distractor profile.

Original radio values are shown in Stage 1 and fully retained in source cases. At original parameters each ordered recipe produces its original value, including the unsimplified `−sqrt(12)` answer fragment in q-19023; full mathematical equivalence is also checked. No choices are pooled, omitted or silently replaced.

## Stage 4: reusable Markdown/value templates

Fixed prose: “We know that … are perpendicular … if and only if … dot … =0”, “Computing the dot product, we have”, “Setting the dot product equal to $0,$ we obtain” and conditional “We disregard the … solution … Therefore …”. The code retains the original punctuation/colon differences. Complete column/angle slots are constructed before insertion; unknown names are not replaced across prose or TeX commands.

Ordered worked stages: (1) formal component sum; (2) substituted pairwise products; (3) individually evaluated product terms when the source has that row; (4) collected polynomial; (5) dot=0 and polynomial=0; (6) source-specific transpose and coefficient division; (7) ±root and sign selection when relevant. q-77152 intentionally collects its two constant products directly, as the source does. q-317932 has the original final direct linear-solving row. q-19023 has both evaluated and collected square-product rows. The validator compares every available source solution string, not merely openings or row count, then reads and checks every generated numerical stage independently.

Authored complete default linear bank: `(R, −R, −C, −A/C, 0)` for `Ax+C=0`, representing correct, transposition sign, omitted coefficient division, inverted solved ratio, and omitted constant product(s). Authored square bank: `(R, −R, sQ, s/sqrt(Q), 0)` for `Ax²+C=0`, `Q=−C/A`; correct, opposite root violating the sign, omitted square root, inverted radicand, omitted constant products. Authored repeated-square bank: `(t, −t, 2t, t², 0)`, using the original linear coefficient magnitude and constant product as wrong scalar fragments. All banks are selected whole; collisions reject the whole sampled instance. There is no inferred distractor diagnosis in learner output.

For blank fields, no bank profile is used. The expected answer remains the exact unknown fragment. Native checks include unreduced fractions and an unsimplified rational-radicand square root, plus wrong scalar rejection. Hard is an authored 3D collect-square radio/blank extension under the bounded scope described in classification; the same stage functions and shared prose apply.

Replay constraints: explicit observed profiles are opaque evidence banks; changed-parameter examples test their mathematical uniqueness but are not recommended default practice. Normal samplers enforce the authored bounds at the reduced equation/radicand, with a unique real eligible root and no equivalent answers. Explicit invalid parameters raise instead of resampling. Source-backed exact prompts, source-exact available solutions, missing-field authored repairs, native outcomes and scope claims have separate denominators.
