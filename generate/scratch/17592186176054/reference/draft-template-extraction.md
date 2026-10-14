# Four-stage template extraction

All banks below remain intact in the public `raw:<source-id>` API. The raw profiles preserve original attribute presence, source field/choice order and original references at original parameters. These are parameterized expressions, not payload-return branches. At changed parameters they have newly owned content identities and remain evidence-only. `source-cases.json` covers every practice source, including both unrated sources.

## 1. Specific source descriptions

Let c denote the given value, n the signed full-period index, a the outside coefficient, and b the outside constant. All inputs have coefficient +1 on x and offset 2nπ. The requested response is one scalar math-valued radio choice with key selection; each field owns five answers.

| Source | Original parameters | Requested expression | Solution shape |
|---|---|---|---|
| q-66472 | c=4, n=2, a=1, b=0 | csc(x+4π) | absent |
| q-66473 | c=4/3, n=-1, a=1, b=0 | csc(x-2π) | absent |
| q-103818 | c=3, n=6, a=5, b=0 | 5 csc(x+12π) | shared reduction, then one multiplication chain |
| q-103820 | c=√5, n=7, a=1, b=0 | csc(x+14π) | shared reduction only |
| q-103822 | c=6, n=8, a=1/3, b=5 | (1/3)csc(x+16π)+5 | substitution, unreduced 6/3+5, reduced 2+5, final 7 |
| q-66605 | c=2, n=-2, a=1/4, b=2 | (1/4)csc(x-4π)+2 | substitution, reduced 1/2+2, final 5/2; no extra 2/4 row |
| q-66667 | c=√2, n=5, a=5, b=-1 | 5 csc(x+10π)-1 | shared reduction, then one radical-expression equality |

Source strings were decoded and adjacent backslash counts examined: every answer command has exactly one leading backslash. JSON serialization's doubled visual escapes are not TeX defects. No TeX repair is asserted. All five complete source solutions are mathematically sound. The two legacy omissions are schema incompleteness, not incorrect correct values; the mathematically inferred unchanged values are not counted as matched original designations.

## 2. Shared pattern and purpose

Use the fixed period 2π to identify csc(x+2nπ)=csc(x), then substitute the given value. Preserve each family's displayed arithmetic sequence. All generated given values are valid cosecant values (>1), and the prompt assumes a defined x. The learning target is periodic reduction, not finding x or using oddness.

## 3. Component and complete-bank mapping

Below the lists map every displayed source option in its original field order to a parameterized expression. An expression's exact reproduction does not recover an author's intended error; several historical lists are expressly opaque. Their exact string masks (spacing, fraction form, Unicode pi, grouping) are implemented separately from the algebraic expressions here.

| Public profile | Complete ordered mathematical bank | Matched original correct designation |
|---|---|---|
| raw:q-66472 | c, π, c(1+π), c+2π, (2nc)π | absent; inferred c only in normal output |
| raw:q-66473 | c=u/d, c+2π, π/d, uπ/d, u+π | absent; inferred c only in normal output |
| raw:q-103818 | ac, a+c, c(π+n), cπ, π/c | ac |
| raw:q-103820 | 2nc, π+c, nc, cπ, c | c |
| raw:q-103822 | n, 2b, ac+b, c, b | ac+b |
| raw:q-66605 | -b, ac+b, b-ac, π-a, c | ac+b |
| raw:q-66667 | -c, π-b, √(c²+3)+2π, (a-2)c, ac+b | ac+b |

The n-only historical option, the constant +3 inside a changed radical, and other forms have no confidently recovered wrong-operation meaning. They are parameterized evidence shapes only, cannot become defaults, and never advertise instructional intent. Even raw banks reject an entire changed instance when a choice is nonreal, infinite, duplicate or ambiguous; they do not replace offending members.

Normal operation banks (all are labeled authored, selected by family before parameters):

| Family | Complete five-operation bank |
|---|---|
| direct integer/fraction/radical | c; 1/c (confuse reciprocal); -c (change sign); c+2nπ (shift output); 2nc (multiply by the input's offset coefficient) |
| scaled_integer | ac; c (omit scale); a+c (add scale); a/c (invert given value); a(c+2nπ) (shift output before scaling) |
| reciprocal families | ac+b; c+b (omit scale); ac (omit offset); b-ac (reverse product sign); ac-b (reverse offset sign) |
| affine_radical | ac+b; c+b; ac; a(c+b) (scale offset); ac-b |
| authored two_terms | (a+d)c+b; ac+b (omit second term); dc+b (omit first term); (a-d)c+b (reverse second sign); (a+d)c-b (reverse offset sign) |

Each row is one indivisible bank; no first-valid choice pooling or random perturbation. Correctness, all wrong-operation values and whole-bank inequality are independently checked from the actual printed prompt. No error feedback is invented in learner content. Source fields remain radio; private blank fixtures exist only to test meaningful typed equivalents through the real grader.

## 4. Reusable masks, constraints and calculations

Fixed prose is the exact shared opening “The period of … Therefore, for integer n we have”, the identity display, “Substituting … into the right-hand-side of the above gives”, the source's single-row aligned reduction, and “Therefore, if … then …”. Scaled and affine families retain “Finally, then” and their original mathematical family stages. Complete components (given value, signed angle, coefficient, offset, unreduced quotient and conclusion) are built separately; no unprotected short-string replacement crosses prose or function arguments. Negative indices retain grouped factors in the substitution row.

Normal original-parameter solutions are byte-exact for all five observed complete solutions, independently of replacement operation banks. Changed parameters retain family row structures. No extra quotient row is added to reciprocal_fraction, and no redundant intermediate arithmetic replaces affine_radical's final row. Legacy normals add the existing shared reduction prose because no original solution exists. Hard repeats the same period substitution/conclusion for each term, then adds substitution, individually evaluated signed terms and a collected result. This added hard chain is explicitly authored.

Exact domains: n and m are nonzero integers of magnitude ≤12. Given c uses distinct reduced integers 2–12, noninteger rational numerator ≤12 and denominator 2–5 with c>1, or √2,√3,√5,√6,√7,√10. Legacy fractions require noninteger c; source easy scale uses integer a=2–8 and integer c. Reciprocal families use a=1/d for d=2–6, integer c and b=1–8, with ac integral only for reciprocal_integer and nonintegral for reciprocal_fraction. Affine radical uses a=2–8 and b=-6…-1. Hard coefficients are opposite signed, noninteger reduced rationals with denominator 2–6, numerator magnitude ≤5 and coefficient magnitude ≤3, nonzero sum; b is an integer of nonzero magnitude ≤6; n≠m. These guards also apply to explicit calls. Whole-bank collisions cause full rejection.

Fidelity, mathematical correctness, completed normal presentation, native grading and finite variety are separate validation denominators. There are no plots in this KP's assessment; step 7 is vacuous and no renderer dependencies/assets are introduced.
