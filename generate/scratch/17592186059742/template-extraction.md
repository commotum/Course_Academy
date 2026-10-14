# Template extraction

## 1. Specific source descriptions

Full originals below are preserved evidence, including absent attributes. Parameter anchors are in source-cases.json and used by the public API; the generator never reads a source payload at runtime.

### q-11534

Calculate $4A + 6B$, where
$A = \begin{bmatrix}-1 & 1 \\ 1 & -1\end{bmatrix}$
and
$B = \begin{bmatrix}2 & -2 \\ -2 & 2\end{bmatrix}$.

Anchor: `{"a": "4", "b": "6", "op": "+", "A": [[-1, 1], [1, -1]], "B": [[2, -2], [-2, 2]], "names": ["A", "B"]}`

Captured solution:


Absent; raw replay retains absence. Normal completion is authored using the shared five-stage method.

### q-11536

Calculate $2P - 3Q$, where
$P = \begin{bmatrix}2 & 1 \\ -2 & -1\end{bmatrix}$
and
$Q = \begin{bmatrix}2 & 1 \\ 1 & -1\end{bmatrix}$.

Anchor: `{"a": "2", "b": "3", "op": "-", "A": [[2, 1], [-2, -1]], "B": [[2, 1], [1, -1]], "names": ["P", "Q"]}`

Captured solution:


Absent; raw replay retains absence. Normal completion is authored using the shared five-stage method.

### q-11532

Calculate $2H-3L$, where
$H=\begin{bmatrix}3 & -2 \\ 2 & -1\end{bmatrix}$
and
$L=\begin{bmatrix}0 & 1 \\ 2 & 1\end{bmatrix}.$

Anchor: `{"a": "2", "b": "3", "op": "-", "A": [[3, -2], [2, -1]], "B": [[0, 1], [2, 1]], "names": ["H", "L"]}`

Captured solution:


We multiply each entry of $H$ by $2$ and each entry of $L$ by $3,$ and then subtract the resulting matrices, as follows:

$$
\begin{aligned}2H-3L & =2\begin{bmatrix}3 & -2 \\ 2 & -1\end{bmatrix}-3\begin{bmatrix}0 & 1 \\ 2 & 1\end{bmatrix} \\  & =\begin{bmatrix}2\cdot 3 & 2\cdot (-2) \\ 2\cdot 2 & 2\cdot (-1)\end{bmatrix}-\begin{bmatrix}3\cdot 0 & 3\cdot 1 \\ 3\cdot 2 & 3\cdot 1\end{bmatrix} \\  & =\begin{bmatrix}6 & -4 \\ 4 & -2\end{bmatrix}-\begin{bmatrix}0 & 3 \\ 6 & 3\end{bmatrix} \\  & =\begin{bmatrix}6-0 & -4-3 \\ 4-6 & -2-3\end{bmatrix} \\  & =\begin{bmatrix}6 & -7 \\ -2 & -5\end{bmatrix}\end{aligned}
$$

### q-11531

Calculate $3F+\frac{1}{2}G$, where
$F=\begin{bmatrix}1 & 3 \\ -2 & 2\end{bmatrix}$
and
$G=\begin{bmatrix}2 & 0 \\ 4 & 6\end{bmatrix}.$

Anchor: `{"a": "3", "b": "1/2", "op": "+", "A": [[1, 3], [-2, 2]], "B": [[2, 0], [4, 6]], "names": ["F", "G"]}`

Captured solution:


We multiply each entry of $F$ by $3$ and each entry of $G$ by $\frac{1}{2},$ and then add the resulting matrices, as follows:

$$
\begin{aligned}3F+\frac{1}{2}G & =3\begin{bmatrix}1 & 3 \\ -2 & 2\end{bmatrix}+\frac{1}{2}\begin{bmatrix}2 & 0 \\ 4 & 6\end{bmatrix} \\  & =\begin{bmatrix}3\cdot 1 & 3\cdot 3 \\ 3\cdot (-2) & 3\cdot 2\end{bmatrix}+\begin{bmatrix}\frac{1}{2}\cdot 2 & \frac{1}{2}\cdot 0 \\ \frac{1}{2}\cdot 4 & \frac{1}{2}\cdot 6\end{bmatrix} \\  & =\begin{bmatrix}3 & 9 \\ -6 & 6\end{bmatrix}+\begin{bmatrix}1 & 0 \\ 2 & 3\end{bmatrix} \\  & =\begin{bmatrix}3+1 & 9+0 \\ -6+2 & 6+3\end{bmatrix} \\  & =\begin{bmatrix}4 & 9 \\ -4 & 9\end{bmatrix}\end{aligned}
$$

### q-126009

Calculate $-A+2B$, where
$A=\begin{bmatrix}3 & 1 \\ 1 & 0\end{bmatrix}$
and
$B=\begin{bmatrix}0 & -2 \\ -2 & 2\end{bmatrix}.$

Anchor: `{"a": "-1", "b": "2", "op": "+", "A": [[3, 1], [1, 0]], "B": [[0, -2], [-2, 2]], "names": ["A", "B"]}`

Captured solution:


We multiply each entry of $A$ by $-1$ and each entry of $B$ by $2,$ and then add the resulting matrices, as follows:

$$
\begin{aligned}-A+2B & =(-1)\begin{bmatrix}3 & 1 \\ 1 & 0\end{bmatrix}+2\begin{bmatrix}0 & -2 \\ -2 & 2\end{bmatrix} \\  & =\begin{bmatrix}(-1)\cdot 3 & (-1)\cdot 1 \\ (-1)\cdot 1 & (-1)\cdot 0\end{bmatrix}+\begin{bmatrix}2\cdot 0 & 2\cdot (-2) \\ 2\cdot (-2) & 2\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}-3 & -1 \\ -1 & 0\end{bmatrix}+\begin{bmatrix}0 & -4 \\ -4 & 4\end{bmatrix} \\  & =\begin{bmatrix}-3+0 & -1+(-4) \\ -1+(-4) & 0+4\end{bmatrix} \\  & =\begin{bmatrix}-3 & -5 \\ -5 & 4\end{bmatrix}\end{aligned}
$$

### q-320656

Calculate $4F-\frac{1}{2}G$, where
$F=\begin{bmatrix}4 & -1 & 0 & 2\end{bmatrix}$
and
$G=\begin{bmatrix}2 & 0 & 4 & -6\end{bmatrix}.$

| $4F-\frac{1}{2}G=\,\,$ |  | {{field-1}} | {{field-2}} | {{field-3}} | {{field-4}} |  |
| --- | --- | --- | --- | --- | --- | --- |

Anchor: `{"a": "4", "b": "1/2", "op": "-", "A": [[4, -1, 0, 2]], "B": [[2, 0, 4, -6]], "names": ["F", "G"]}`

Captured solution:


We multiply each entry of $F$ by $4$ and each entry of $G$ by $\frac{1}{2},$ and then subtract the resulting matrices, as follows:

$$
\begin{aligned}4F-\frac{1}{2}G & =4\begin{bmatrix}4 & -1 & 0 & 2\end{bmatrix}-\frac{1}{2}\begin{bmatrix}2 & 0 & 4 & -6\end{bmatrix} \\  & =\begin{bmatrix}4\cdot 4 & 4\cdot (-1) & 4\cdot 0 & 4\cdot 2\end{bmatrix}-\begin{bmatrix}\frac{1}{2}\cdot 2 & \frac{1}{2}\cdot 0 & \frac{1}{2}\cdot 4 & \frac{1}{2}\cdot (-6)\end{bmatrix} \\  & =\begin{bmatrix}16 & -4 & 0 & 8\end{bmatrix}-\begin{bmatrix}1 & 0 & 2 & -3\end{bmatrix} \\  & =\begin{bmatrix}16-1 & -4-0 & 0-2 & 8-(-3)\end{bmatrix} \\  & =\begin{bmatrix}15 & -4 & -2 & 11\end{bmatrix}\end{aligned}
$$

### q-320671

Calculate $\frac{2}{3}M+2N$, where
$M=\begin{bmatrix}6 & 0 & 15 \\ -12 & 6 & 0\end{bmatrix}$
and
$N=\begin{bmatrix}3 & -1 & 0 \\ -2 & \frac{1}{2} & -1\end{bmatrix}.$

| $\frac{2}{3}M+2N=\,\,$ |  | {{field-1}} | $-2$ | {{field-2}} |  |
| --- | --- | --- | --- | --- | --- |
|  | $-12$ | {{field-3}} | {{field-4}} |  |  |

Anchor: `{"a": "2/3", "b": "2", "op": "+", "A": [[6, 0, 15], [-12, 6, 0]], "B": [[3, -1, 0], [-2, "1/2", -1]], "names": ["M", "N"], "targets": [0, 2, 4, 5]}`

Captured solution:


We multiply each entry of $M$ by $\frac{2}{3}$ and each entry of $N$ by $2,$ and then add the resulting matrices, as follows:

$$
\begin{aligned}\frac{2}{3}M+2N & =\frac{2}{3}\begin{bmatrix}6 & 0 & 15 \\ -12 & 6 & 0\end{bmatrix}+2\begin{bmatrix}3 & -1 & 0 \\ -2 & \frac{1}{2} & -1\end{bmatrix} \\  & =\begin{bmatrix}\frac{2}{3}\cdot 6 & \frac{2}{3}\cdot 0 & \frac{2}{3}\cdot 15 \\ \frac{2}{3}\cdot (-12) & \frac{2}{3}\cdot 6 & \frac{2}{3}\cdot 0\end{bmatrix}+\begin{bmatrix}2\cdot 3 & 2\cdot (-1) & 2\cdot 0 \\ 2\cdot (-2) & 2\cdot \frac{1}{2} & 2\cdot (-1)\end{bmatrix} \\  & =\begin{bmatrix}4 & 0 & 10 \\ -8 & 4 & 0\end{bmatrix}+\begin{bmatrix}6 & -2 & 0 \\ -4 & 1 & -2\end{bmatrix} \\  & =\begin{bmatrix}4+6 & 0-2 & 10+0 \\ -8-4 & 4+1 & 0-2\end{bmatrix} \\  & =\begin{bmatrix}10 & -2 & 10 \\ -12 & 5 & -2\end{bmatrix}\end{aligned}
$$

### q-69642

Calculate $\frac{1}{3}G+2H$, where
$G=\begin{bmatrix}3 & 6 & 15 \\ -12 & 9 & 6\end{bmatrix}$
and
$H=\begin{bmatrix}1 & 2 & 5 \\ 3 & 4 & 6\end{bmatrix}.$

Anchor: `{"a": "1/3", "b": "2", "op": "+", "A": [[3, 6, 15], [-12, 9, 6]], "B": [[1, 2, 5], [3, 4, 6]], "names": ["G", "H"]}`

Captured solution:


We multiply each entry of $G$ by $\frac{1}{3}$ and each entry of $H$ by $2,$ and then add the resulting matrices, as follows:

$$
\begin{aligned}\frac{1}{3}G+2H & =\frac{1}{3}\begin{bmatrix}3 & 6 & 15 \\ -12 & 9 & 6\end{bmatrix}+2\begin{bmatrix}1 & 2 & 5 \\ 3 & 4 & 6\end{bmatrix} \\  & =\begin{bmatrix}\frac{1}{3}\cdot 3 & \frac{1}{3}\cdot 6 & \frac{1}{3}\cdot 15 \\ \frac{1}{3}\cdot (-12) & \frac{1}{3}\cdot 9 & \frac{1}{3}\cdot 6\end{bmatrix}+\begin{bmatrix}2\cdot 1 & 2\cdot 2 & 2\cdot 5 \\ 2\cdot 3 & 2\cdot 4 & 2\cdot 6\end{bmatrix} \\  & =\begin{bmatrix}1 & 2 & 5 \\ -4 & 3 & 2\end{bmatrix}+\begin{bmatrix}2 & 4 & 10 \\ 6 & 8 & 12\end{bmatrix} \\  & =\begin{bmatrix}1+2 & 2+4 & 5+10 \\ -4+6 & 3+8 & 2+12\end{bmatrix} \\  & =\begin{bmatrix}3 & 6 & 15 \\ 2 & 11 & 14\end{bmatrix}\end{aligned}
$$

## 2. Shared pattern

Supply two equally shaped matrices and two numerical scalars; calculate their scalar-weighted sum/difference entry by entry. A whole-matrix radio answer or four scalar blank fragments is required. No matrix multiplication, unknown scalar solving, third matrix, determinants, symbolic variables or new topics.

The ordered five stages are: supplied matrices with their scalars → two explicit entrywise-product matrices → two evaluated scaled matrices → one matrix of ordered entrywise sum/difference expressions → one collected result matrix. Distinct masks preserve every product and both operands before collection. The full introductory prose derives names, scalar values, and add/subtract verb from the instance. q-126009 writes +(-v) for adding a negative; q-320671 writes −v shorthand.

## 3. Complete component and bank mapping

Indices below are row-major zero-based. A/B are supplied values, X=aA and Y=bB, C=X±Y. Each complete bank is chosen before parameters and used as a whole; every pair of matrices, including two wrong options, must differ entrywise. No first-valid recipe replacement. All original choice values below match exactly. Labels describe parameterized replay masks, not recovered author intent.

### q-11534 / observed-q-11534

Field `selection`, :answer-field.type/radio. Correct designation absent.

- `\begin{bmatrix}-8 & 8 \\ 8 & -8\end{bmatrix}` ← `−C`; original designation missing.

- `\begin{bmatrix}-8 & -8 \\ -8 & 8\end{bmatrix}` ← `[−C0,C1,C2,C3]`; original designation missing.

- `\begin{bmatrix}8 & 8 \\ 8 & 8\end{bmatrix}` ← `[C0,−C1,−C2,C3]`; original designation missing.

- `\begin{bmatrix}8 & -8 \\ -8 & 8\end{bmatrix}` ← `C`; original designation missing.

- `\begin{bmatrix}8 & -8 \\ -8 & -8\end{bmatrix}` ← `[C0,C1,C2,−C3]`; original designation missing.

### q-11536 / observed-q-11536

Field `selection`, :answer-field.type/radio. Correct designation absent.

- `\begin{bmatrix}-2 & -1 \\ 1 & 1\end{bmatrix}` ← `[C0,C1,B2,−B3]`; original designation missing.

- `\begin{bmatrix}-2 & -1 \\ -7 & -1\end{bmatrix}` ← `[C0,C1,C2,B3]`; original designation missing.

- `\begin{bmatrix}-2 & -1 \\ -1 & 1\end{bmatrix}` ← `[C0,C1,−B2,−B3]`; original designation missing.

- `\begin{bmatrix}-2 & -1 \\ -7 & 1\end{bmatrix}` ← `C`; original designation missing.

- `\begin{bmatrix}-2 & -1 \\ -1 & -1\end{bmatrix}` ← `[C0,C1,−B2,B3]`; original designation missing.

### q-11532 / observed-q-11532

### q-11531 / observed-q-11531

Field `selection`, :answer-field.type/radio. Correct designation present.

- `\begin{bmatrix}-4 & 9 \\ -4 & 9\end{bmatrix}` ← `[−C0,C1,C2,C3]`; incorrect.

- `\begin{bmatrix}4 & -9 \\ -4 & 9\end{bmatrix}` ← `[C0,−C1,C2,C3]`; incorrect.

- `\begin{bmatrix}4 & 9 \\ 9 & -4\end{bmatrix}` ← `[C0,C1,C3,C2]`; incorrect.

- `\begin{bmatrix}4 & 9 \\ -4 & -9\end{bmatrix}` ← `[C0,C1,C2,−C3]`; incorrect.

- `\begin{bmatrix}4 & 9 \\ -4 & 9\end{bmatrix}` ← `C`; correct.

### q-126009 / observed-q-126009

Field `selection`, :answer-field.type/radio. Correct designation present.

- `\begin{bmatrix}-3 & -1 \\ -5 & 2\end{bmatrix}` ← `[C0,X1,C2,B3]`; incorrect.

- `\begin{bmatrix}-3 & 3 \\ 3 & -4\end{bmatrix}` ← `X−Y`; incorrect.

- `\begin{bmatrix}2 & -5 \\ -4 & 4\end{bmatrix}` ← `[b,C1,Y2,C3]`; incorrect.

- `\begin{bmatrix}-3 & -5 \\ -5 & 4\end{bmatrix}` ← `C`; correct.

- `\begin{bmatrix}1 & 3 \\ 3 & -4\end{bmatrix}` ← `[A2,X1−Y1,X2−Y2,−Y3]`; incorrect.

### q-320656 / observed-q-320656

Field `field-1`, :answer-field.type/blank. Correct designation present.

- `15` ← `C at the cell assigned to field-1`; correct.

Field `field-2`, :answer-field.type/blank. Correct designation present.

- `-4` ← `C at the cell assigned to field-2`; correct.

Field `field-3`, :answer-field.type/blank. Correct designation present.

- `-2` ← `C at the cell assigned to field-3`; correct.

Field `field-4`, :answer-field.type/blank. Correct designation present.

- `11` ← `C at the cell assigned to field-4`; correct.

### q-320671 / observed-q-320671

Field `field-3`, :answer-field.type/blank. Correct designation present.

- `5` ← `C at the cell assigned to field-3`; correct.

Field `field-1`, :answer-field.type/blank. Correct designation present.

- `10` ← `C at the cell assigned to field-1`; correct.

Field `field-2`, :answer-field.type/blank. Correct designation present.

- `10` ← `C at the cell assigned to field-2`; correct.

Field `field-4`, :answer-field.type/blank. Correct designation present.

- `-2` ← `C at the cell assigned to field-4`; correct.

### q-69642 / observed-q-69642

Field `selection`, :answer-field.type/radio. Correct designation present.

- `\begin{bmatrix}3 & 15 & 6 \\ 2 & 14 & 11\end{bmatrix}` ← `C indexed [0,2,1,3,5,4]`; incorrect.

- `\begin{bmatrix}3 & 6 & 15 \\ 2 & 11 & 14\end{bmatrix}` ← `C`; correct.

- `\begin{bmatrix}3 & 6 & 14 \\ 2 & 11 & 15\end{bmatrix}` ← `C indexed [0,1,5,3,4,2]`; incorrect.

- `\begin{bmatrix}3 & 2 & 5 \\ 2 & 11 & 10\end{bmatrix}` ← `[C0,X1,X2,C3,C4,X5+Y4]`; incorrect.

- `\begin{bmatrix}1 & 6 & 15 \\ -2 & 11 & 14\end{bmatrix}` ← `[X0,C1,C2,X3+Y0,C4,C5]`; incorrect.

q-11536 and q-126009 have opaque compound banks. Their component projections above faithfully reproduce all original options and change with actual operands, but cannot establish the historical misconception. They are explicit evidence-only profiles at original and changed parameters. The q-126009 option containing the scalar b as a matrix entry is particularly underidentified. No opaque bank is a normal learning default. Other observed banks are also evidence-only for consistent fidelity/eligibility separation.

The default authored radio method bank is complete: C; reverse the matrix combine sign X∓Y; omit A scaling (A±Y); omit B scaling (X±B); omit the first scaled matrix (±Y). These are actual operations on the displayed method, with no unrelated offsets, random wrong values or inferred feedback. Bank count is five. A colliding whole bank rejects the entire instance. Blanks have no distractors.

## 4. Backbone and slots

Fixed: two supplied equally shaped matrices, two scalar products, ordered five-stage method, family add/subtract operator, field types/count, four requested scalar entries for blank families. The row family stays 1x4 and the rectangular family stays 2x3. Variable: matrix labels (distinct uppercase letters), all supplied entries, allowed nonzero scalar values, and four target-cell positions in the partial family. Labels/order are excluded from mathematical-task counts.

Easy: a,b∈{2,3}, A/B entries integers 0…4; nonzero matrices. Moderate: integer entries −6…6; half-plus a∈{2,…,6}, b=1/2 with even B; negative-plus a∈{−1,−2,−3}, b∈{2,…,6}; other square families a,b∈{2,…,6}; signed inputs required for their workload. Easy positive-only integer tasks cannot pass the moderate guard. Hard row: a∈{2,3,4}, b=1/2, even B, entries −6…6, subtraction. Hard rectangles: a∈{1/3,2/3}, b=2, A entries multiples of 3 bounded by 18, B integers/halves bounded by 6, giving integral scaled entries. Explicit inputs and samplers use these same bounds. These are conservative authored sampling policies, not recovered software ranges.

For q-320671 the source anchor targets are field-1→(1,1), field-2→(1,3), field-3→(2,2), field-4→(2,3); the other cells (1,2)/(2,1) are given. Pull order never determines cell position. The slot domain is all 15 four-cell subsets of six cells in row-major order: four requested cells and two supplied correct cells. Changing targets preserves the requested/given roles and four-entry assessment workload. Given values are computed from the actual supplied matrices. The changed-target regression holds scalars/matrices fixed and checks all fifteen masks, actual placeholder columns and answer keys.

Raw q-320671 source table staggers the bottom row by one Markdown column. Public observed replay preserves it exactly as ineligible evidence. Normal output inserts the missing bottom padding cell and removes the redundant trailing cell, placing both rows’ matrix entries in columns 3–5. This is a documented presentation repair, not a changed assessment. All original values/keys remain intact.

Raw q-11534/q-11536 retain missing difficulty, solution and correct refs; completed normal records infer only the uniquely correct mathematical matrix and author moderate assignment/solution. Raw q-11532 retains absent answer-fields; normal records author one five-choice radio field. Those inferred values are never counted as original designations. Canonical e-4382 lacks an A= assignment in its captured prompt; this is context evidence only, not a practice replay. Normal questions always name both supplied matrices.

Scope basis: lesson linked route follows first-step→next: Introduction; Multiplying a Matrix by a Scalar; Calculating the Value of a Scalar; Properties of Scalar Multiplication; this KP. The canonical example performs the same two scalar products then entrywise addition with a half scalar. Key prerequisite Evaluating Linear Expressions and topic predecessor Adding and Subtracting Matrices support the arithmetic. The scalar-solving sibling is a boundary, not a branch to add. Neither later matrix-column multiplication nor transpose/inverse topics is introduced.

Variety: level-capacity.json counts conservative valid subdomains separately from sampled uniqueness and target-slot coverage. Mathematical fingerprints contain the actual input matrices/scalars, response shape, and requested cells, excluding names, option order and bank profile. Content identity includes version, difficulty (or raw absence), actual prompt/solution, full displayed bank and field/reference presence; seeds/shuffling cannot change it.

Calculator flag remains unknown: the supplemental 86-record capture has no applicable flags. No calculator requirement is invented. All source anomalies and underidentified intent remain disclosed; no database operation or registration is prepared.

Partial-blank mathematical task identity uses only the four requested cell operands, their positions, scalar factors and matrix shape; the two provided result cells are incidental and cannot inflate capacity. Reordering field labels over the same requested positions is an alias. Both scalar products must contribute to the requested cells. The constructive hard capacity is211200 (19200 row +192000 partial), excluding provided-cell variation.
