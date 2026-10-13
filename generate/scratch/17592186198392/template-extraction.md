# Template extraction

## Stage 1: specific observed questions

Every original source prompt, complete bank, designation and worked solution is preserved in source.json. Source-cases.json maps all 12 questions. The following table identifies graph, response layout and values at original parameters.

| Source | Difficulty | Graph | Original parameters | Complete choice bank, original ordering |

|---|---|---|---|---|

| q-161166 | moderate | z graph symbolic | `{"function": "g"}` | $-P,\,$ $∂P,\,$ $∂x$<br>$P,\,$ $∂g,\,$ $∂x$<br>$-P,\,$ $∂g,\,$ $∂x$<br>$P,\,$ $∂g,\,$ $∂y$<br>$-P,\,$ $∂g,\,$ $∂y$ |

| q-161189 | easy | z graph symbolic | `{"function": "g"}` | $P$ and $Q$<br>$-P$ and $Q$<br>$Q$ and $P$<br>$P$ and $-Q$<br>$-P$ and $-Q$ |

| q-161446 | moderate | x graph symbolic | `{"function": "k"}` | $-Q$ and $∂z$<br>$-Q$ and $∂x$<br>$Q$ and $∂x$<br>$Q$ and $∂z$<br>$-R$ and $∂z$ |

| q-161453 | hard | y graph monomial | `{"c": -1, "m": 2, "n": 1}` | $2P$ and $R$<br>$P$ and $-2R$<br>$P$ and $R$<br>$-2P$ and $2R$<br>$2P$ and $-2R$ |

| q-161456 | moderate | x graph monomial | `{"c": 2, "m": 1, "n": 1}` | $-2Q$ and $R$<br>$-2Q$ and $-2R$<br>$Q$ and $R$<br>$Q$ and $-2R$<br>$-Q$ and $-R$ |

| q-161465 | moderate | x graph symbolic | `{"function": "k"}` | -Q,\text{ }\frac{∂k}{∂z},\text{ }\frac{∂k}{∂y}<br>-Q,\text{ }\frac{∂k}{∂x},\text{ }\frac{∂k}{∂z}<br>-Q,\text{ }\frac{∂k}{∂y},\text{ }\frac{∂k}{∂z}<br>Q,\text{ }\frac{∂k}{∂y},\text{ }\frac{∂k}{∂x}<br>Q,\text{ }\frac{∂k}{∂y},\text{ }\frac{∂k}{∂z} |

| q-161460 | hard | y graph symbolic | `{"function": "h"}` | P,\,\frac{∂h}{∂z},\,\frac{∂h}{∂x}<br>-P,\,\frac{∂h}{∂x},\,\frac{∂h}{∂y}<br>-P,\,\frac{∂h}{∂y},\,\frac{∂h}{∂z}<br>-P,\,\frac{∂h}{∂x},\,\frac{∂h}{∂z}<br>-P,\,\frac{∂h}{∂y},\,\frac{∂h}{∂x} |

| q-161455 | hard | y graph monomial | `{"c": 2, "m": 1, "n": 3}` | $-2R$ and $-2P$<br>$P$ and $R$<br>$P$ and $-6R$<br>$-2P$ and $-R$<br>$-2P$ and $6R$ |

| q-161457 | easy | z graph symbolic | `{"function": "g"}` | ∂g,\text{ }-Q,\text{ }∂Q<br>∂g,\text{ }Q,\text{ }∂z<br>∂g,\text{ }-Q,\text{ }∂z<br>∂g,\text{ }-Q,\text{ }∂y<br>∂g,\text{ }Q,\text{ }∂y |

| q-161463 | easy | z graph symbolic | `{"function": "g"}` | $∂z$ and $∂x$<br>$∂x$ and $∂z$<br>$∂y$ and $∂z$<br>$∂x$ and $∂y$<br>$∂y$ and $∂x$ |

| q-161449 | easy | z graph monomial | `{"c": 1, "m": 2, "n": 1}` | $-4P$ and $-2Q$<br>$-2P$ and $-Q$<br>$-4Q$ and $P$<br>$-2R$ and $Q$<br>$P$ and $-R$ |

| q-162607 | easy | z graph symbolic | `{"function": "g"}` | $∂z,∂g,$ and $-1$<br>$∂x,∂g,$ and $-R$<br>$∂x,∂g,$ and $1$<br>$∂x,∂g,$ and $-1$<br>$∂x,∂g,$ and $R$ |

## Stage 2: generalized family

Given a Cartesian graph with its canonical orientation, fill two or three omitted formula fragments in F·dS = (F composed with graph)·(oriented unnormalized normal) dA. P,Q,R denote the generic field components on the surface. Sources retain formula-recognition slots in denominators, numerators and coefficient positions. Numeric monomial sources require differentiation; positive-j hard sources also reverse orientation.

## Stage 3: component mapping

For every layout, extraction.json stores the prompt/solution templates, original parameters, complete bank, correct index, answer type, exact display aliases and repairs. Every full displayed choice is preserved, including text dollar fragments and math fragments. The symbolic banks are explicit ordered token tuples whose derivative numerators, denominators, signs and field-component choices are independently reinserted into the formula by validate.py. Functions can be renamed via a protected single-letter token replacement; the derivative structure stays unchanged. The source includes no distractor-specific explanation, so none is added.

### Monomial operation banks

Write the graph as c u^m v^n. All tuples below are complete ordered banks and are computed operations; no source-payload return branch or literal answer lookup is used. The chosen tuple is multiplied by the displayed bases u^(m−1)v^n and u^m v^(n−1). For q161455 the second tuple coefficient has a preprinted minus sign. Each operation is explicit; learner intent is not uniquely inferred from a symbolic coefficient.

#### q-161453

Axis y; correct source tuple index 0 (zero based).

- Option 1: `(-cmP, -cnR)` -> `(2*P, R)`; exact original value reproduced. Correct.

- Option 2: `(-cnP, cmR)` -> `(P, -2*R)`; exact original value reproduced. Incorrect; no source learner-error diagnosis.

- Option 3: `(-cnP, -cnR)` -> `(P, R)`; exact original value reproduced. Incorrect; no source learner-error diagnosis.

- Option 4: `(cmP, -cmR)` -> `(-2*P, 2*R)`; exact original value reproduced. Incorrect; no source learner-error diagnosis.

- Option 5: `(-cmP, cmR)` -> `(2*P, -2*R)`; exact original value reproduced. Incorrect; no source learner-error diagnosis.

#### q-161456

Axis x; correct source tuple index 1 (zero based).

- Option 1: `(-cQ, R)` -> `(-2*Q, R)`; exact original value reproduced. Incorrect; no source learner-error diagnosis.

- Option 2: `(-cQ, -cR)` -> `(-2*Q, -2*R)`; exact original value reproduced. Correct.

- Option 3: `(Q, R)` -> `(Q, R)`; exact original value reproduced. Incorrect; no source learner-error diagnosis.

- Option 4: `(Q, -cR)` -> `(Q, -2*R)`; exact original value reproduced. Incorrect; no source learner-error diagnosis.

- Option 5: `(-Q, -R)` -> `(-Q, -R)`; exact original value reproduced. Incorrect; no source learner-error diagnosis.

#### q-161455

Axis y; correct source tuple index 4 (zero based).

- Option 1: `(-cmR, -cmP)` -> `(-2*R, -2*P)`; exact original value reproduced. Incorrect; no source learner-error diagnosis.

- Option 2: `(P, R)` -> `(P, R)`; exact original value reproduced. Incorrect; no source learner-error diagnosis.

- Option 3: `(P, -cnR)` -> `(P, -6*R)`; exact original value reproduced. Incorrect; no source learner-error diagnosis.

- Option 4: `(-cmP, -R)` -> `(-2*P, -R)`; exact original value reproduced. Incorrect; no source learner-error diagnosis.

- Option 5: `(-cmP, cnR)` -> `(-2*P, 6*R)`; exact original value reproduced. Correct.

#### q-161449

Axis z; correct source tuple index 1 (zero based).

- Option 1: `(-2cmP, -2cnQ)` -> `(-4*P, -2*Q)`; exact original value reproduced. Incorrect; no source learner-error diagnosis.

- Option 2: `(-cmP, -cnQ)` -> `(-2*P, -Q)`; exact original value reproduced. Correct.

- Option 3: `(-2cmQ, cnP)` -> `(-4*Q, P)`; exact original value reproduced. Incorrect; no source learner-error diagnosis.

- Option 4: `(-cmR, cnQ)` -> `(-2*R, Q)`; exact original value reproduced. Incorrect; no source learner-error diagnosis.

- Option 5: `(cnP, -cnR)` -> `(P, -R)`; exact original value reproduced. Incorrect; no source learner-error diagnosis.

## Stage 4: reusable rendering and constraints

Fixed components: generic flux identity, question wording, formula-mask layout, one field with five complete options, tangent/cross-product sequence and final dot-product integral. Variable components: nonzero signed coefficient, within-family exponent-role pair, derivative values, oriented normal, displayed bases and coefficient tuple bank. Symbolic function names are optional notation aliases. Conditional component: the source hard positive-j reversal paragraph. All numeric graph/derivative/normal/base/coefficient values are computed with SymPy; exact source lexemes are used only when algebraically equal to the derived value. They never supply the mathematical answer.

Numerical slots are restricted to mathematical components. Bilinear base slots occur only in the two displayed coefficient-times-base positions. Their original y,z notation is fixed in prose, determinant basis labels and coordinate names. Displayed mathematics is checked independently against the actual prompt, including every scalar formula option and the final expanded integrand. Source shared prose remains fixed across parameter variation.

## Source teaching errors and supported repairs

No answer-designation or bank-value error was found. Four source solutions have a wrong notation line; raw evidence remains unchanged and repairs are applied in the normal recipe, including explicit observed replays.

- q-161446: F(r(x,y)) -> F(r(y,z)). Independent tangent determinant and chosen orientation prove the replacement. Bank/prompt still replay exactly; solution is counted repaired rather than verbatim.

- q-161453: Final integral uses r_z cross r_x, matching selected positive-j normal. Independent tangent determinant and chosen orientation prove the replacement. Bank/prompt still replay exactly; solution is counted repaired rather than verbatim.

- q-161465: F(r(x,y)) -> F(r(y,z)). Independent tangent determinant and chosen orientation prove the replacement. Bank/prompt still replay exactly; solution is counted repaired rather than verbatim.

- q-161460: Final integral uses r_z cross r_x, matching selected positive-j normal. Independent tangent determinant and chosen orientation prove the replacement. Bank/prompt still replay exactly; solution is counted repaired rather than verbatim.

Some captured formula masks contain invisible omitted coefficients or empty fraction cells (q161166/189/446/453/456/460). Explicit observed replay retains their exact prompt. Normal authored presentation inserts a visible box in those same slots, preserving the mathematical assessment and choice bank. This is a presentation repair, separate from the four teaching corrections.

## Variation limits

The observed operation banks remain intact under coefficient/exponent variation. Exponent-role transpositions are authored equal-workload extensions, not recovered extra source templates. All finite coefficient/exponent cases are enumerated by validate.py. Normal generation does not count cosmetic symbolic-function renaming as additional assessed mathematics.

## Authored translated-bilinear extraction

Specific recovered base: q161456, x=2yz, normal (1,−2z,−2y), missing coefficient tuple (−2Q,−2R). Generalized peer family: translate the two factors, x=c(y−a)(z−b)+h, keeping one first derivative in each factor. Components: graph c(y−a)(z−b)+h; r_y=(c(z−b),1,0); r_z=(c(y−a),0,1); normal=(1,−c(z−b),−c(y−a)); displayed bases (z−b),(y−a); complete original coefficient-operation bank remains unchanged. Reusable template: only graph, mathematical derivative/normal slots and the two coefficient-times-base slots vary; coordinate names and teaching prose are protected. Bases with additions are parenthesized. Zero offsets reproduce the original. Small integer shifts have magnitude at most 2; no extra differentiation or integration enters the task. The authored profile is separately named and nonzero offsets cannot silently enter an observed profile. Constant h shifts affect the displayed surface, but meaningful variation is established using h=0 and 100 distinct normals.

Enumeration also rejects q161455 at c=−1 with transposed (m,n)=(3,1): its fourth operation equals the correct fifth operation. This is a whole-bank rejection; the script does not replace a distractor.
