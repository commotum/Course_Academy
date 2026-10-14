# Template extraction — scalar multiplication

## Stage1: describe each source before generalizing

The complete captured original prompts, answer banks, field records and worked solutions remain in `source.json`; `review.json` also places every original record beside its public parameterized replay. The descriptions below distinguish specific observed number forms from proposed bounds.

| Original | Specific supplied data | Response and notation | Source solution |
| --- | --- | --- | --- |
| q-979 | scalar5, matrix[[1,0],[2,6]] | What-is direct2×2;5 complete matrix radios; no key/rating | absent |
| q-986 | scalar6, D=[[-1,2],[1,0],[1/3,4]] | named3×2;5 complete matrix radios; no key/rating | absent |
| q-125885 | scalar0, W=[[1,-1,-3],[-5,0,2]] | named2×3;5 complete matrix radios | named scalar/input, six unevaluated cell products, result |
| q-320045 | scalar3, A=[[2,1],[4,3]] | named2×2, four entry blanks | named scalar/input, four cell products, result |
| q-320075 | scalar-7, A=[[5,4],[-6,2]] | named2×2, four entry blanks; parenthesized negative product factor | introductory prose says3 in error; rows correctly use-7 |
| q-320082 | scalar2, C=[[1,2],[-2,4]] | named2×2, four entry blanks | named scalar/input, four cell products, result |
| q-980 | scalar3, matrix[[4,-5],[-2,1/3]] | direct2×2 equals;5 complete matrix radios | input on LHS of first aligned row, four cell products, result on second row |

Source field Pull order is not matrix row order. q320045 is4,1,2,3; q320075 is1,4,2,3; q320082 is3,4,1,2. Placeholders define field1=top-left, field2=top-right, field3=bottom-left, field4=bottom-right. Raw replay preserves original collection order. Normal records use row-major fields and minimal table padding repair: both placeholder rows align in columns3/4. The raw source lower row is staggered one column left.

Decoded source answer values begin with one actual backslash (character92) before `begin`; JSON visual escaping does not establish a doubled-command anomaly. No TeX normalization is required for the observed practice matrices.

## Stage2: generalized shared pattern

A supplied exact scalar k multiplies every entry of supplied matrix A independently, preserving matrix dimensions and entry positions. The response is either one whole-matrix radio choice or four scalar entry fragments in the supplied2×2 layout. Stable stages are scalar×input → matrix of unevaluated scalar·entry products → evaluated matrix. Named families have three aligned calculation rows; the direct family has two aligned rows, with scalar×input on the first row's left. Each instance gets one solution independent of the selected response.

No inverse operation, additional matrix, scalar unknown, summation, matrix product or branching method belongs to this backbone. Matrix letters are cosmetic slots; actual input factors are arithmetic workload slots. Shape is fixed within named/what/entry families; authored direct six-entry variants use shapes already taught by named sources.

## Stage3: components and complete bank mapping

Notation below uses aij for the printed entry, cij=k·aij, and M[i,j←x] for replacing that cell while preserving all other entries. The public recipe derives each entire displayed matrix; numeric reproduction does not prove historical error intention. Recipes are metadata, never learner feedback.

| Profile | Complete operations in source order-independent bank |
| --- | --- |
| bank979 | C with c21 negated; C with bottom-right unscaled; C; C with zero upper-right replaced by k; C with lower-left unscaled |
| bank986 | C with first two first-column entries negated; C; C with upper two second-column entries swapped; C with bottom-left negated and bottom-right k+a32; C with top-left negated |
| bankzero | only first column scaled; C; only top-left scaled; only top row scaled; no entries scaled |
| bank980 | upper-right unscaled; lower-right k·numerator(a22), ignoring denominator; previous plus lower-left sign flip; lower-left unscaled; C |

bank986's final-row(-2,10) admits many explanations. `(-k·a31, k+a32)` is an explicit algebraic replay operation, not a recovered intention. The whole bank remains evidence-only. Normal named3×2 output uses the separately authored method bank C, A, -kA, first row unscaled, last row unscaled. Each wrong matrix arises from the printed entrywise operation. Whole-bank eligibility is chosen before parameters; correct/correct, correct/wrong and wrong/wrong equivalence reject the entire instance. No post-hoc replacement or first-valid recipe pool is used.

Normal bank979 requires zero top-right and noncolliding cells; bank980 requires a noninteger lower-right entry; bankzero requires scalar0 and enough nonzero entries to distinguish omission patterns. Their observed error operations are defensible hypotheses, not assertions about the original authoring implementation. Normal default sampling serves all five easy families. Public method banks also support what/named2×3/direct profiles when requested explicitly.



### q-979 — raw_979

Prompt components: scalar `$5$`, name `A`, matrix `$\begin{bmatrix}1 & 0 \\ 2 & 6\end{bmatrix}$`; template `what_2x2`.

| Source field | Exact source choice | Derived recipe | Source designation |
| --- | --- | --- | --- |

| selection | `$\begin{bmatrix}5 & 0 \\ -10 & 30\end{bmatrix}$` | C[2,1←-c21] | missing key; independently derived wrong |

| selection | `$\begin{bmatrix}5 & 0 \\ 10 & 6\end{bmatrix}$` | C[2,2←a22] | missing key; independently derived wrong |

| selection | `$\begin{bmatrix}5 & 0 \\ 10 & 30\end{bmatrix}$` | C=kA | missing key; independently derived correct |

| selection | `$\begin{bmatrix}5 & 5 \\ 10 & 30\end{bmatrix}$` | C[1,2←k] | missing key; independently derived wrong |

| selection | `$\begin{bmatrix}5 & 0 \\ 2 & 30\end{bmatrix}$` | C[2,1←a21] | missing key; independently derived wrong |

Raw parameterized solution component: source absent, raw attribute omitted; normal solution authored from shared named-family backbone.


### q-986 — raw_986

Prompt components: scalar `$6$`, name `D`, matrix `$\begin{bmatrix}-1 & 2 \\ 1 & 0 \\ \frac{1}{3} & 4\end{bmatrix}$`; template `named_3x2`.

| Source field | Exact source choice | Derived recipe | Source designation |
| --- | --- | --- | --- |

| selection | `$\begin{bmatrix}6 & 12 \\ -6 & 0 \\ 2 & 24\end{bmatrix}$` | C[1,1←-c11;2,1←-c21] | missing key; independently derived wrong |

| selection | `$\begin{bmatrix}-6 & 12 \\ 6 & 0 \\ 2 & 24\end{bmatrix}$` | C=kA | missing key; independently derived correct |

| selection | `$\begin{bmatrix}-6 & 0 \\ 6 & 12 \\ 2 & 24\end{bmatrix}$` | C[1,2←c22;2,2←c12] | missing key; independently derived wrong |

| selection | `$\begin{bmatrix}-6 & 12 \\ 6 & 0 \\ -2 & 10\end{bmatrix}$` | C[3,1←-c31;3,2←k+a32] (historical intent underidentified) | missing key; independently derived wrong |

| selection | `$\begin{bmatrix}6 & 12 \\ 6 & 0 \\ 2 & 24\end{bmatrix}$` | C[1,1←-c11] | missing key; independently derived wrong |

Raw parameterized solution component: source absent, raw attribute omitted; normal solution authored from shared named-family backbone.


### q-125885 — raw_125885

Prompt components: scalar `$0$`, name `W`, matrix `$\begin{bmatrix}1 & -1 & -3 \\ -5 & 0 & 2\end{bmatrix}$`; template `named_2x3`.

| Source field | Exact source choice | Derived recipe | Source designation |
| --- | --- | --- | --- |

| selection | `$\begin{bmatrix}0 & -1 & -3 \\ 0 & 0 & 2\end{bmatrix}$` | scale only column1 | incorrect |

| selection | `$\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix}$` | C=kA | correct |

| selection | `$\begin{bmatrix}0 & -1 & -3 \\ -5 & 0 & 2\end{bmatrix}$` | scale only cell(1,1) | incorrect |

| selection | `$\begin{bmatrix}0 & 0 & 0 \\ -5 & 0 & 2\end{bmatrix}$` | scale only row1 | incorrect |

| selection | `$\begin{bmatrix}1 & -1 & -3 \\ -5 & 0 & 2\end{bmatrix}$` | A (omit all scaling) | incorrect |

Raw parameterized solution component: 

We multiply each entry of $W$ by $0,$ as follows:

$$
\begin{aligned}0W & =0\begin{bmatrix}1 & -1 & -3 \\ -5 & 0 & 2\end{bmatrix} \\  & =\begin{bmatrix}0\cdot 1 & 0\cdot (-1) & 0\cdot (-3) \\ 0\cdot (-5) & 0\cdot 0 & 0\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix}\end{aligned}
$$


### q-320045 — raw_320045

Prompt components: scalar `$3$`, name `A`, matrix `$\begin{bmatrix}2 & 1 \\ 4 & 3\end{bmatrix}$`; template `entries_2x2`.

| Source field | Exact source choice | Derived recipe | Source designation |
| --- | --- | --- | --- |

| field-4 | `$9$` | k·a22 | correct |

| field-1 | `$6$` | k·a11 | correct |

| field-2 | `$3$` | k·a12 | correct |

| field-3 | `$12$` | k·a21 | correct |

Raw parameterized solution component: 

We multiply each entry of $A$ by $3,$ as follows:

$$
\begin{aligned}3A & =3\begin{bmatrix}2 & 1 \\ 4 & 3\end{bmatrix} \\  & =\begin{bmatrix}3\cdot 2 & 3\cdot 1 \\ 3\cdot 4 & 3\cdot 3\end{bmatrix} \\  & =\begin{bmatrix}6 & 3 \\ 12 & 9\end{bmatrix}\end{aligned}
$$


### q-320075 — raw_320075

Prompt components: scalar `$-7$`, name `A`, matrix `$\begin{bmatrix}5 & 4 \\ -6 & 2\end{bmatrix}$`; template `entries_2x2`.

| Source field | Exact source choice | Derived recipe | Source designation |
| --- | --- | --- | --- |

| field-1 | `$-35$` | k·a11 | correct |

| field-4 | `$-14$` | k·a22 | correct |

| field-2 | `$-28$` | k·a12 | correct |

| field-3 | `$42$` | k·a21 | correct |

Raw parameterized solution component: 

We multiply each entry of $A$ by $3,$ as follows:

$$
\begin{aligned}-7A & =-7\begin{bmatrix}5 & 4 \\ -6 & 2\end{bmatrix} \\  & =\begin{bmatrix}(-7)\cdot 5 & (-7)\cdot 4 \\ (-7)\cdot (-6) & (-7)\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}-35 & -28 \\ 42 & -14\end{bmatrix}\end{aligned}
$$


### q-320082 — raw_320082

Prompt components: scalar `$2$`, name `C`, matrix `$\begin{bmatrix}1 & 2 \\ -2 & 4\end{bmatrix}$`; template `entries_2x2`.

| Source field | Exact source choice | Derived recipe | Source designation |
| --- | --- | --- | --- |

| field-3 | `$-4$` | k·a21 | correct |

| field-4 | `$8$` | k·a22 | correct |

| field-1 | `$2$` | k·a11 | correct |

| field-2 | `$4$` | k·a12 | correct |

Raw parameterized solution component: 

We multiply each entry of $C$ by $2,$ as follows:

$$
\begin{aligned}2C & =2\begin{bmatrix}1 & 2 \\ -2 & 4\end{bmatrix} \\  & =\begin{bmatrix}2\cdot 1 & 2\cdot 2 \\ 2\cdot (-2) & 2\cdot 4\end{bmatrix} \\  & =\begin{bmatrix}2 & 4 \\ -4 & 8\end{bmatrix}\end{aligned}
$$


### q-980 — raw_980

Prompt components: scalar `$3$`, name `A`, matrix `$\begin{bmatrix}4 & -5 \\ -2 & \frac{1}{3}\end{bmatrix}$`; template `direct`.

| Source field | Exact source choice | Derived recipe | Source designation |
| --- | --- | --- | --- |

| selection | `$\begin{bmatrix}12 & -5 \\ -6 & 1\end{bmatrix}$` | C[1,2←a12] | incorrect |

| selection | `$\begin{bmatrix}12 & -15 \\ -6 & 3\end{bmatrix}$` | C[2,2←k·numerator(a22)] | incorrect |

| selection | `$\begin{bmatrix}12 & -15 \\ 6 & 3\end{bmatrix}$` | C[2,1←-c21;2,2←k·numerator(a22)] | incorrect |

| selection | `$\begin{bmatrix}12 & -15 \\ -2 & 1\end{bmatrix}$` | C[2,1←a21] | incorrect |

| selection | `$\begin{bmatrix}12 & -15 \\ -6 & 1\end{bmatrix}$` | C=kA | correct |

Raw parameterized solution component: 

We multiply each entry of the matrix by $3$, as follows:

$$
\begin{aligned}3\begin{bmatrix}4 & -5 \\ -2 & \frac{1}{3}\end{bmatrix} & =\begin{bmatrix}3\cdot 4 & 3\cdot (-5) \\ 3\cdot (-2) & 3\cdot \frac{1}{3}\end{bmatrix} \\  & =\begin{bmatrix}12 & -15 \\ -6 & 1\end{bmatrix}\end{aligned}
$$


## Stage4: reusable backbone and variable slots

| Component | Status and constraints | Dependent components |
| --- | --- | --- |
| Assessed method | fixed single entrywise scalar multiplication | prompt, key, every option, all product cells and final matrix |
| Scalar k | exact rational; normal level bounds in classification and code enforced for explicit and sampled calls | request label, intro prose, scalar×input row, every product, bank operations |
| Matrix entries | exact rational; arithmetic workloads are fixed per level | supplied matrix, every entry product, blank semantic keys and complete option banks |
| Matrix dimensions | named/what/blank source shape fixed; direct2×2 at easy and2×3/3×2 at authored M/H | unchanged dimension throughout solution and choices |
| Matrix name | one of A,C,D,M,R,W, cosmetic | named request, definition, prose, symbolic first row; excluded from math fingerprint |
| Blank roles | fixed four row-major slots, no reordered meaning | supplied placeholders and matching field-key answers; raw collection order retained |
| Scalar grouping | conditional negative factor grouping for named normal/blank negative source; direct source grouping unchanged | unevaluated product tokens |
| Prompt punctuation | family-specific source mask | raw complete prompt strings |
| Solution row sequence | named3, direct2; input/product/result matrices kept separate | source prose and complete mathematical stages |
| Field type/options | source contract: radio5 matrices or blank4 scalar fields with1 answer each | field-owned identities, native grader |
| Feedback | absent in all sources, remains absent | answer records |

Rendering is component-based, not global replacement. Negative entries in the product row are parenthesized and every numeric multiplication uses visible `\cdot`, preventing concatenated numbers. SymPy evaluates final answers only; the intermediate product strings retain the actual unevaluated factors. Bank recipes derive all wrong matrices from the same instance. Source q320075's raw introduction preserves erroneous3, while normal introduction derives actual k. Exact raw solution fidelity is5/5; mathematically sound original solutions are4/5 and normal minimal repair restores5/5. q979/q986 lack source solutions and keys, so their normal completions are authored, not reported as recovered fidelity.

Public raw recipes admit changed exact-rational parameters within evidence bounds, but never enter default sampling. They preserve missing source rating, worked solution and correct-ref attribute presence, and record `evidence_only=true`, `eligible_for_learning=false`. Every raw anchor matches all values, layouts and full existing solution prose exactly; source correct designation counts exclude the two absent keys.

Moderate/hard are anchored authored workloads, not new recovered templates. Six products at each authored level retain all source entrywise stages; the distinction is exactly three half-integer results at moderate versus exactly three rational cancellation products and at least four rational results at hard. Both require signed nonzero inputs. No within-level progression is defined.

Meaningful capacity is counted through mathematical operands and workload, not labels, option order or profiles. A nonzero scalar and its matrix entries remain substantive arithmetic factors even if another factorization yields the same final matrix. For scalar0, input entries are irrelevant to the operation's answer and are excluded. Conservative guaranteed lower bounds: easy what-family1728, moderate2×3 family160000, hard2×3 families5523520. The hard count restricts all outputs to fractions and fixes a mixed-sign assignment, so it is below the full valid domain. Enumeration formulas and per-scalar slot counts are in `validation.json`; zero2×3 contributes one task.

Content identity hashes generator version, displayed prompt, complete bank, fixed solution, difficulty, parameters and selected profile, excluding seed and answer order. Mathematical fingerprint excludes presentation, profiles and cosmetic names, and additionally zero-scalar irrelevant input entries. Different banks have different content identities even for the same operation.

`validate.py` parses actual rendered scalars/matrices/products and final prose with an independent Fraction grammar; it does not establish correctness by trusting generation metadata. It checks all pairwise matrix choices, complete source strings/presence, native equivalent and wrong blank entries, deterministic reruns, level domains and mutation regressions. Native radio ID checks remain separate from mathematical bank fidelity. All seven original banks receive native memory-only fixtures. For the two missing source keys, the fixture alone receives an independently derived correct ref; the public raw generator still omits it, and no source designation match is claimed. Normal full solutions at original parameters are compared separately with the complete captured strings, allowing only the documented q320075 coefficient repair. Plot rating is none and no plot specification is needed. This work stops before database preparation.

