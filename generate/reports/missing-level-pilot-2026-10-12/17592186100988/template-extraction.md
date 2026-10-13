# Template extraction: matrix-entry lookup

Protocol: [4-template-extraction](../../../docs/4-template-extraction.md). All source questions are from basis **1522**. [Source cases](source-cases.json) describe every original before generalization; [source questions](source-questions.md) retain every original prompt, choice, field, and available fixed worked solution.

## Specific originals

| Source | Matrix shape | Target | Answer | Response | Distinguishing feature |
|---|---|---|---|---|---|
| q-279260 | 2×3 | y₂₂ | −1 | Easy radio | Repeated −2 entries; bank includes a fixed +2 not present in the matrix |
| q-279539 | 5×4 | e₅₃ | 2 | Easy blank | Already a large, repeated-value matrix |
| q-279540 | 3×4 | f₃₂ | 4 | Easy blank | Mixed signs and zero entries |
| q-13497 | 3×4 | c₂₄ | 5 | Easy radio | Includes “No such entry”; solution says “should lie” |
| q-125561 | 3×2 | e₃₁ | −3 | Easy radio | All five displayed answers correspond to matrix entries |
| q-13488 | 2×3 | a₁₃ | 2 | Unrated radio | Inline layout; source correct reference and solution missing |
| q-13496 | 3×4 | d₄₃ | No such entry | Unrated radio | Requested row does not exist; correct reference and solution missing |

## Shared pattern and components

Identify the intersection of a supplied one-based row and column and return its scalar value. Neither calculation of matrix entries nor reverse identification of their indices is part of the rated template.

Fixed components are the “Find the entry …” request, a literal matrix, one response field, and the worked solution's row/column identification followed by the repeated matrix. Variable components are the matrix letter, dimensions, literal entries, and requested indices. The blank family's supplied `letter_ij=` and field placeholder are fixed layout components. Radio and blank are separate templates.

Observed dimensions are 2×3, 3×2, 3×4, and 5×4; rated entries are integers from −8 to 9, including zero and repeated values. Proposed bounds are not inferred from that range: retain all source shapes and values for replay, and keep any larger arrays or fractional entries explicitly authored extensions. Rectangular matrices preserve separation from the square-matrix sibling. Valid-entry variants require 1 ≤ i ≤ m and 1 ≤ j ≤ n. The incomplete absent-entry family deliberately violates one bound.

## Reusable Markdown/value templates

Radio prompt:

```text
Find the entry ${letter}_{i j}$ of the matrix $LETTER$, where

$$
LETTER=[\begin{aligned}{rows joined by \\; cells by &}\end{aligned}].
$$
```

Blank prompt appends:

```text
${letter}_{i j}=$
{{field-1}}
```

Preserve each source's mathematical typesetting and “lies”/“should lie” render style. The calculation is `answer = A[i-1][j-1]`. The fixed worked solution states the same i-th row and j-th column, gives that answer, and repeats the same matrix. A blank's expected fragment is only the scalar, with its sign.

## Choice profiles and complete-value accounting

Every original option has its source answer entity, field key, exact value, profile, and a complete observed recipe in [source-cases.json](source-cases.json). Matrix-cell recipes retain **all matching locations** when values repeat; the extraction does not pretend to know which location supplied a distractor. A value not present in the matrix remains a fixed source scalar with an unresolved sampling rule. “No such entry” retains `:answer.type/text`; numerical choices retain `:answer.type/math`.

The three rated radio profiles cannot be pooled indiscriminately: one contains a nonexistent-entry distractor, one includes a scalar absent from the matrix, and one draws all its choices from matrix cells. Parameter changes must preserve five distinct answer values and exactly one correct option. Repeated matrix entries can cause choice collisions, so a future generator must reject an entire unsuitable bank or specify an authored extension. No distractors are added to blanks.

## Missing-level experiment

[Authored probe](../probes.md#matrix-entry-lookup): request a negative fractional entry from a 5×4 literal matrix using the observed blank contract. It is mathematically valid and stays in scope, but still requires only row/column lookup. Recognizing a fraction instead of an integer and scanning more entries give limited extra workload, not a convincing moderate mathematical task. The source's easy 5×4 example makes that limitation concrete.

A reverse-index question would use the sibling KP; adding a transpose or computing a matrix expression would add another skill. **Best judgment: retain easy variants for this KP rather than manufacturing a moderate label from visual clutter.** A moderate-labelled source could change that judgment, but none was found here.
