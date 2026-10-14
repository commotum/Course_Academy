# Template extraction

The whole raw source and every field/value are retained in `source.json`. `source-cases.json` contains six MA-original public raw-API replay cases, including the unrated original. `independent-cases.json` separately replays the one exact independently authored inventory record preserved in `independent-inventory.json`. `source-choice-mapping.json` maps every one of 38 raw answer values to its complete expression pattern and generated value, including both duplicate q-11440 banks. All 24 raw distractors are accounted for. Recipes below represent observed mathematical patterns; exact numeric reproduction does not establish cognitive intent.

## Stage 1 — describe each source before generalizing


### q-101

Source 17592186054939, unrated. Operand entries in row-major order: A=[-4, -5, 12, 3], B=[-9, 5, 6, -11]; result=[-13, 0, 18, -8]. Values are exact signed integers; zeros, opposite signs and cancellation are retained. Names ['A', 'B'] and first-operand wrapping positions [] are source notation. Template `inline-question`; five complete matrix choices.

What is $\begin{bmatrix}-4 & -5 \\ 12 & 3\end{bmatrix} + \begin{bmatrix}-9 & 5 \\ 6 & -11\end{bmatrix}$?

No source worked solution. Raw replay preserves its absence; the separately labeled eligible completion authors the corresponding-entry solution.


### q-11440

Source 17592186054967, :question.difficulty/easy. Operand entries in row-major order: A=[2, 5, 3, 1], B=[4, 1, -2, 2]; result=[6, 6, 1, 3]. Values are exact signed integers; zeros, opposite signs and cancellation are retained. Names ['A', 'B'] and first-operand wrapping positions [] are source notation. Template `named-radio`; five complete matrix choices.

Calculate $A+B$, where

$$
A=\begin{bmatrix}2 & 5 \\ 3 & 1\end{bmatrix},\,B=\begin{bmatrix}4 & 1 \\ -2 & 2\end{bmatrix}.
$$

We add the corresponding entries:

$$
\begin{aligned}A+B & =\begin{bmatrix}2 & 5 \\ 3 & 1\end{bmatrix}+\begin{bmatrix}4 & 1 \\ -2 & 2\end{bmatrix} \\  & =\begin{bmatrix}2+4 & 5+1 \\ 3+(-2) & 1+2\end{bmatrix} \\  & =\begin{bmatrix}6 & 6 \\ 1 & 3\end{bmatrix}\end{aligned}
$$


### q-100

Source 17592186237775, :question.difficulty/easy. Operand entries in row-major order: A=[6, -1, 7, 0], B=[-2, 9, 1, 8]; result=[4, 8, 8, 8]. Values are exact signed integers; zeros, opposite signs and cancellation are retained. Names ['A', 'B'] and first-operand wrapping positions [1] are source notation. Template `inline-equality`; five complete matrix choices.

$\begin{bmatrix}6 & -1 \\ 7 & 0\end{bmatrix}+\begin{bmatrix}-2 & 9 \\ 1 & 8\end{bmatrix}=$

We add the corresponding entries:

$$
\begin{aligned}\begin{bmatrix}6 & -1 \\ 7 & 0\end{bmatrix}+\begin{bmatrix}-2 & 9 \\ 1 & 8\end{bmatrix} & =\begin{bmatrix}6+(-2) & (-1)+9 \\ 7+1 & 0+8\end{bmatrix} \\  & =\begin{bmatrix}4 & 8 \\ 8 & 8\end{bmatrix}\end{aligned}
$$


### q-125630

Source 17592186259832, :question.difficulty/easy. Operand entries in row-major order: A=[1, -2, 0, -3], B=[1, 0, 0, 1]; result=[2, -2, 0, -2]. Values are exact signed integers; zeros, opposite signs and cancellation are retained. Names ['P', 'Q'] and first-operand wrapping positions [1, 3] are source notation. Template `named-radio`; five complete matrix choices.

Calculate $P+Q$, where

$$
P=\begin{bmatrix}1 & -2 \\ 0 & -3\end{bmatrix},\,Q=\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}.
$$

We add the corresponding entries:

$$
\begin{aligned}P+Q & =\begin{bmatrix}1 & -2 \\ 0 & -3\end{bmatrix}+\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}1+1 & (-2)+0 \\ 0+0 & (-3)+1\end{bmatrix} \\  & =\begin{bmatrix}2 & -2 \\ 0 & -2\end{bmatrix}\end{aligned}
$$


### q-125631

Source 17592186259833, :question.difficulty/easy. Operand entries in row-major order: A=[2, 0, 0, 1], B=[0, -1, -2, 0]; result=[2, -1, -2, 1]. Values are exact signed integers; zeros, opposite signs and cancellation are retained. Names ['X', 'Y'] and first-operand wrapping positions [] are source notation. Template `named-radio`; five complete matrix choices.

Calculate $X+Y$, where

$$
X=\begin{bmatrix}2 & 0 \\ 0 & 1\end{bmatrix},\,Y=\begin{bmatrix}0 & -1 \\ -2 & 0\end{bmatrix}.
$$

We add the corresponding entries:

$$
\begin{aligned}X+Y & =\begin{bmatrix}2 & 0 \\ 0 & 1\end{bmatrix}+\begin{bmatrix}0 & -1 \\ -2 & 0\end{bmatrix} \\  & =\begin{bmatrix}2+0 & 0+(-1) \\ 0+(-2) & 1+0\end{bmatrix} \\  & =\begin{bmatrix}2 & -1 \\ -2 & 1\end{bmatrix}\end{aligned}
$$


### q-319591

Source 17592186299781, :question.difficulty/easy. Operand entries in row-major order: A=[3, -4, -2, 7], B=[-9, 10, 5, -1]; result=[-6, 6, 3, 6]. Values are exact signed integers; zeros, opposite signs and cancellation are retained. Names ['F', 'G'] and first-operand wrapping positions [] are source notation. Template `cell-blanks`; four scalar blanks, field-1/2 on the first response row and field-3/4 on the second.

Calculate $F+G,$ where $F=\begin{bmatrix}3 & -4 \\ -2 & 7\end{bmatrix}$ and 
$G=\begin{bmatrix}-9 & 10 \\ 5 & -1\end{bmatrix}.$

| $F+G=\,\,$ |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
|  | {{field-3}} | {{field-4}} |  |  |

We add the corresponding entries:

$$
\begin{aligned}\begin{aligned}F+G & =\begin{bmatrix}3 & -4 \\ -2 & 7\end{bmatrix}+\begin{bmatrix}-9 & 10 \\ 5 & -1\end{bmatrix} \\  & =\begin{bmatrix}3+(-9) & -4+10 \\ -2+5 & 7+(-1)\end{bmatrix} \\  & =\begin{bmatrix}-6 & 6 \\ 3 & 6\end{bmatrix}\end{aligned}\end{aligned}
$$


### Independently authored inventory ef70fb38-cef6-5843-b533-7177233ed52d

Source 17592186510633, :question.difficulty/easy. Operand entries in row-major order: A=[-6, 6, 4, 8], B=[-11, -12, -10, -6]; result=[-17, -6, -6, 2]. Values are exact signed integers; zeros, opposite signs and cancellation are retained. Names ['F', 'G'] and first-operand wrapping positions [] are source notation. Template `cell-blanks`; four scalar blanks, field-1/2 on the first response row and field-3/4 on the second.

Calculate $F+G,$ where $F=\begin{bmatrix}-6 & 6 \\ 4 & 8\end{bmatrix}$ and 
$G=\begin{bmatrix}-11 & -12 \\ -10 & -6\end{bmatrix}.$

| $F+G=\,\,$ |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
|  | {{field-3}} | {{field-4}} |  |  |

We add the corresponding entries:

$$
\begin{aligned}\begin{aligned}F+G & =\begin{bmatrix}-6 & 6 \\ 4 & 8\end{bmatrix}+\begin{bmatrix}-11 & -12 \\ -10 & -6\end{bmatrix} \\  & =\begin{bmatrix}-6+(-11) & 6+(-12) \\ 4+(-10) & 8+(-6)\end{bmatrix} \\  & =\begin{bmatrix}-17 & -6 \\ -6 & 2\end{bmatrix}\end{aligned}\end{aligned}
$$


## Stage 2 — shared mathematical pattern

Given two 2×2 integer matrices, add each pair of corresponding entries and return the whole sum, either by selecting its matrix or entering all four scalar cells. No scalar-solving, matrix multiplication, determinant, dimension inference, symbolic coefficients or rectangular matrices are added. Every displayed cell affects the assessed task; no unrelated unqueried entry is sampled.

## Stage 3 — components and complete banks

Prompt components are the two supplied matrices, addition sign, optional distinct names, and one observed response contract. Solutions share “We add the corresponding entries:” followed by displayed operand sum, corresponding-entry arithmetic matrix and collected matrix. The inline-equality solution combines the operand and arithmetic matrices in its first equality row; named/inline-question/cell templates keep the operand sum as its own equality row. The source contains no distractor feedback; none is added.

For complete source banks let a/b/c be row-major first operand, second operand and correct sum, with indices 00,01,10,11. Each list below is a complete five-choice bank in recipe order; choice order is not fidelity. Every untouched entry is c. Source answer UUIDs and each exact source matrix are mapped one-to-one in `source-choice-mapping.json`.


### observed-q-101

1. `[c00, -(a01-b01), c10, -|a11|-|b11|]`.
2. `[c00, a01-b01, a10, c11]`.
3. `[-(a00-b00), -(a01-b01), c10, c11]`.
4. `c`.
5. `c with c11=-|a11|-|b11|`.


### observed-q-11440

1. `c`.
2. `[a01,a00,c10,c11]`.
3. `all entries=a01`.
4. `[-c00,c01,c10,-c11]`.
5. `all entries=c00`.


### observed-q-100

1. `[a00-b00,b01-a01,c10,c11]`.
2. `c with c01=b01-a01`.
3. `c`.
4. `all entries=c01`.
5. `c with c00=-c00`.


### observed-q-125630

1. `c with c10=c01`.
2. `c with c01=b11`.
3. `c`.
4. `c with c10=c00`.
5. `c with c00=c00+1 (observed offset; intent unresolved)`.


### observed-q-125631

1. `c with c00=a11`.
2. `c with c01=-c01`.
3. `[-c00,c01,-c10,c11]`.
4. `c`.
5. `c with c01=a01`.


Copy-entry, repeated-entry, arbitrary +1, and compound sign patterns have underdetermined cognitive intent. These full observed banks are public **evidence-only** profiles requiring explicit parameters; they never enter default learner sampling. They are parameterized expressions, not literal question/value return branches. Raw `raw-q-*` profiles and separate eligible completed `observed-q-*` profiles use the same parameterized prompt/solution/bank calculations and shared assembly. Raw profiles preserve source difficulty/solution/key presence and duplicate contracts; completed profiles add only the documented eligible presentation. No captured learner payload is copied into an API result. Changed-parameter review cases verify each pattern through the public API; their status remains evidence-only, not a recovered method bank. A full-bank collision rejects the entire explicit instance.

Default authored profiles derive complete wrong operations from the assessed corresponding-entry/sign method. They are distinct from observed-bank fidelity:


### authored-correspondence

1. entrywise A+B.
2. entrywise A-B.
3. entrywise B-A.
4. retain A without adding B.
5. transpose the complete sum.


### authored-signs

1. entrywise A+B.
2. add absolute B entries.
3. add absolute A entries to B.
4. negate the complete sum.
5. add transposed B instead of corresponding B.


## Stage 4 — backbone, slots and constraints

| Component | Role / allowed slot | Dependent content / constraint |
| --- | --- | --- |
| Dimension/operator | fixed 2×2, two supplied matrices, addition | four corresponding additions; no change of skill |
| a00..a11 and b00..b11 | eight exact integer operand slots | prompt, all solution operand/addend/sum cells, every whole-bank operation, four keys |
| All result cells | fixed target set {00,01,10,11} | radio selects whole matrix; blanks request all four, no unqueried cell |
| Matrix names | distinct uppercase names | named prompt and solution change together; notation only, excluded from task counts |
| First-negative grouping | eligible row-major indices 0..3 | explicit parentheses only; unused positive grouping does not change content identity |
| Redundant outer alignment | boolean notation slot | source blanks retain nested aligned; no extra arithmetic stage or task count |
| Complete bank | one eligible complete profile chosen first | compute all five options, reject any correct/incorrect or incorrect/incorrect equality; no first-valid pooling |
| Level | authored guards described in classification | applied equally to explicit parameters and sampler; observed banks only easy |

The four fixed parameterized prompt/solution builders preserve full original wording and stage sequence. Source parameters and source profile replay through `generate(level, seed=0, template=..., parameters=..., profile=...)`. Normal blanks have no bank profile; raw blank profiles preserve their source field layouts and order. Every scalar blank owns its value. `raw-q-101` leaves solution, grade and correct ref absent; `raw-q-11440` retains the duplicate selection fields and absent legacy ref. Only separately labeled eligible completions author missing stages/key/rating or collapse the legacy field. Raw source records are ineligible for native fixture grading when a correct ref is absent; no engine change is made.

Normal samples retain one concrete worked solution independent of the chosen error. Both summands are shown at every cell, negative second operands are parenthesized, and no malformed `+-`/`--` sequences are introduced. Shared `math_format.py` supplies matrix rendering, normalizes prose/bare answers before identities, and validates every public return. Raw evidence is never normalized in place.

Semantic task identity hashes the unordered pair of complete supplied matrices (addition is commutative), excludes names, grouping, profile, bank, layout, level, seed and option order. Presentation identity hashes version, displayed difficulty (or its absence), actual normalized prompt, complete fixed solution (or its absence), canonically ordered keyed field contracts, complete unordered banks and present correct values. Absent attributes and duplicate raw contracts enter the identity explicitly; field collection order alone does not. Different banks get distinct identities; changing seed/order alone does not. Unused notation parameters cannot add identities.

Scope limits and fidelity denominators are recorded in `validation.json`. All supplied designations and available solutions are tested separately from bank matching, inferred missing keys, native grading, or authored-level design claims.
