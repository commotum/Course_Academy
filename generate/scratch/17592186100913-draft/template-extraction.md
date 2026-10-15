# Template extraction

## 1. Specific observations

The complete per-source component inventory below records original prompts, present solutions, field types and answer fragments; every source choice is paired with its exact mathematical recipe in the extraction appendix. Canonical e-5885 is contextual evidence, not a practice record. Two unrated source questions omit difficulty, solution and correct refs. These omissions are preserved individually by the public evidence profiles and are not counted as matched labels/designations.

The2×2 family contains four repeated factor pairs with one more row-major product filled at each row, a separate evaluated-cell equality at each row, and a concluding full matrix. The3×2 named family includes shape prose and a symbolic shape equation, a factor-substitution row, an unevaluated product matrix, then the evaluated result. The4×3 unnamed family starts the aligned calculation with the printed factor pair equals the product matrix, then collection; it has no redundant standalone substitution row. q-1031 has no source solution. The undefined sources stop after the shape incompatibility stage; they do not receive an invented outer-product calculation in raw replay.

The original2×2 scalar-blank layout q-275545/q-318484 staggers field-3/field-4 one column left of field-1/field-2. Exact raw replay retains the table. Normal output aligns the same four fields in two columns. No answer role, field count or type changes.3×2 blank layouts are already aligned.4×3 scalar blanks are an explicitly authored extension of the same complete-entry response contract, with twelve row-major fields.

## 2. Shared pattern

Supply a column vector a and row vector b, check their matching inner dimension1, compute every ordered scalar product a_i b_j, and return the entire matrix. Dimensions and factor orientation are part of the skill. Each question has one fixed solution, independent of selected error. Source undefined/reversed cases are retained as evidence but cannot define a new normal branch.

## 3. Components and banks

`templates.json` is an auditable recipe extraction, not a source-question payload bank. Prompts/solutions contain whole-component FIRST,SECOND,PRODUCTS,PARTIAL1…3,RESULT and CELL0…3 slots. There is no short-number global substitution. Every number in a concluding matrix, partially filled matrix, product cell and evaluated equality derives from the current printed factors. `source-cases.json` supplies original numerical anchors. `build_templates.py` is the one-time extractor; runtime generation renders recipes and masks and never returns captured question JSON.

Historical distractor intentions can be underdetermined. q-1031's a0+b0 scalar cell and q-130136's unusual augmented-looking wrong shapes are explicit opaque historical expression patterns, not claimed recovered cognitive errors. q-130230's b1−2 wrong factor is likewise an opaque preserved feature. q-129961's wrong row/column fragments use a source slot a0 where its historical meaning is unclear. Their whole banks are reproduced at the anchors, available publicly for evidence, and ineligible for learning. There are no arbitrary fitted coefficients in normal banks.

The normal radio bank is selected as one complete operation profile before sampling: true outer product, transposed product, componentwise addition instead of multiplication, negation of every product, Undefined. All choices remain complete matrices or the original Undefined shape answer. The wrong operations are tied to this method. The entire sampled instance is rejected for any mathematical collision or arithmetic ceiling; no first-valid option replacement occurs. Blank fields have their single exact scalar fragment and no invented wrong choices.

## 4. Reusable backbone, slots and constraints

Fixed roles: first factor is n×1, second1×k; every output cell is requested. Supported dimension roles are2×2,3×2,4×3, with the original family-specific calculation stages above. Entry slots a_i and b_j are integers. Matrix letters are inherited prose, not claimed task variety. There is no requested-target slot because the requested object is always the whole product; changing to one entry would enter sibling KP 00873.

Every explicit call and random sample uses the same guards. Whole zero factors are rejected in normal output. Global source-grounded ceilings: each factor magnitude≤10, each product magnitude≤50, sum of absolute product entries≤240. Normal easy allows at most four products with both factors nonunit and total≤150. Moderate is3×2, all six factor pairs nonunit, factor magnitude≤5, each product≤15, total≤60. Hard is4×3, at least eight nonunit products, each≤50, total≤240. No division, fractions, extra algebra or dot-product sums are added. Signed exact integer arithmetic is grounded in source factors up to10 and products up to50; MA's easy4×3 q-1038 already reaches50. Hard varies multiplication count rather than admitting unbounded coefficients.

The complete displayed radio bank additionally caps any coefficient at50 and total absolute coefficient workload at600; this includes wrong choices. The observed banks fit that aggregate ceiling. Historical evidence profiles use their source-label dimensions, the same global factor/product ceiling, and the complete bank cap. Evidence-only profiles are not normal easy/moderate samplers.

Easy random sampling uses either a_i∈[-10,10],b_j∈{-1,0,1} or a_i∈{-1,0,1},b_j∈[-5,5]. Explicit easy supports the documented wider ≤4 nonunit workload guard. Moderate's sampled factor alphabet is±2…±5; hard's is±2,±3,±4,±5,±6,±8,±10. Explicit integer inputs can use intervening integer magnitudes within the same coupled caps; this is a documented broader eligible domain, not weaker workload checking. No infinite variety claim is made: QA measures500 bounded samples per level and all observed family/layout slots, excluding seed, option order and bank aliases from task counts.

A task fingerprint contains ordered mathematical factors and meaningful orientation. Factor rescaling generally changes the scalar multiplications being assessed even if it preserves the final matrix. Banks, profiles, letters and option order are excluded from the task fingerprint. Content identity includes the actual prompt, all fixed solution stages, level, complete field bank and version. Deterministic source family profiles and field contracts allow exact regeneration with changed seed; option shuffling is excluded from identity.

Raw source TeX was inspected as decoded bytes. It has one slash before begin/end and two at row separators; JSON display escaping is not a malformed-TeX finding. Source-exact prompt/solution replay remains11/11 and9/9. Normal negative factors are visibly grouped; full matrix components are normalized through shared math-format helpers before IDs. No malformed source content is served.


# Extraction appendix: every observed component and choice

## q-1031
Source label: missing; parameters: `{"a": [3, 0, 1], "b": [2, 4]}`; family: outer-3x2.
Prompt:

What is $\begin{bmatrix}3 \\ 0 \\ 1\end{bmatrix}\begin{bmatrix}2 & 4\end{bmatrix}$?
Solution:

RAW MISSING ATTRIBUTE
Field `selection` :answer-field.type/radio; correct RAW MISSING ATTRIBUTE (zero-based source bank index).
- 0. original `Undefined`; recipe `undefined`; type :answer.type/text.
- 1. original `[6]`; recipe `"["+str(a[0]*b[0])+"]"`; type :answer.type/math.
- 2. original `\begin{bmatrix}6 & 12 \\ 2 & 4 \\ 2 & 4\end{bmatrix}`; recipe `matrix([[p[0][0],p[0][1]],[p[2][0],p[2][1]],[p[2][0],p[2][1]]])`; type :answer.type/math.
- 3. original `\begin{bmatrix}6 & 12 \\ 5 & 4\end{bmatrix}`; recipe `matrix([[p[0][0],p[0][1]],[a[0]+b[0],p[2][1]]])`; type :answer.type/math.
- 4. original `\begin{bmatrix}6 & 12 \\ 0 & 0 \\ 2 & 4\end{bmatrix}`; recipe `matrix(p)`; type :answer.type/math.

## q-13636
Source label: missing; parameters: `{"a": [0, -2, -3], "b": [1, 2]}`; family: undefined-evidence.
Prompt:

Find $CD$, if
$C = \begin{bmatrix}1 & 2\end{bmatrix}$
and
$D = \begin{bmatrix}0 \\ -2 \\ -3\end{bmatrix}$.
Solution:

RAW MISSING ATTRIBUTE
Field `selection` :answer-field.type/radio; correct RAW MISSING ATTRIBUTE (zero-based source bank index).
- 0. original `Undefined`; recipe `undefined`; type :answer.type/text.
- 1. original `\begin{bmatrix}1 & 0 \\ -2 & -4 \\ -3 & -6\end{bmatrix}`; recipe `matrix([[b[0],a[0]],[p[1][0],p[1][1]],[p[2][0],p[2][1]]])`; type :answer.type/math.
- 2. original `[4]`; recipe `"["+str(abs(b[1]*a[1]))+"]"`; type :answer.type/math.
- 3. original `\begin{bmatrix}0 & 0 \\ -2 & -4 \\ 3 & -6\end{bmatrix}`; recipe `matrix([[p[0][0],p[0][1]],[p[1][0],p[1][1]],[-p[2][0],p[2][1]]])`; type :answer.type/math.
- 4. original `\begin{bmatrix}0 & 0 \\ -2 & -4 \\ -3 & -6\end{bmatrix}`; recipe `matrix(p)`; type :answer.type/math.

## q-1038
Source label: {':db/ident': ':question.difficulty/easy'}; parameters: `{"a": [-10, 6, 0, 8], "b": [1, -5, -1]}`; family: outer-4x3.
Prompt:

$\begin{bmatrix}-10 \\ 6 \\ 0 \\ 8\end{bmatrix}\begin{bmatrix}1 & -5 & -1\end{bmatrix}=$
Solution:

Here, the first factor is $4\times 1$ matrix and the second factor is a $1\times 3$ matrix. 

There is $1$ column in the first matrix and $1$ row in the second matrix, so the product is well defined:

$$
4\times \boxed{\text{1}}✓\boxed{\text{1}}\times 3=4\times 3
$$

Computing the product, we have:

$$
\begin{aligned}\begin{bmatrix}-10 \\ 6 \\ 0 \\ 8\end{bmatrix}\begin{bmatrix}1 & -5 & -1\end{bmatrix} & =\begin{bmatrix}-10\cdot 1 & -10\cdot (-5) & -10\cdot (-1) \\ 6\cdot 1 & 6\cdot (-5) & 6\cdot (-1) \\ 0\cdot 1 & 0\cdot (-5) & 0\cdot (-1) \\ 8\cdot 1 & 8\cdot (-5) & 8\cdot (-1)\end{bmatrix} \\  & =\begin{bmatrix}-10 & 50 & 10 \\ 6 & -30 & -6 \\ 0 & 0 & 0 \\ 8 & -40 & -8\end{bmatrix}\end{aligned}
$$
Field `selection` :answer-field.type/radio; correct 3 (zero-based source bank index).
- 0. original `\begin{bmatrix}-10 & -30 & 0 & -8\end{bmatrix}`; recipe `matrix([[a[i]*b[min(i,len(b)-1)] for i in range(len(a))]])`; type :answer.type/math.
- 1. original `\begin{bmatrix}-10 & 50 & 10 \\ 6 & -30 & -6 \\ 0 & 0 & 0\end{bmatrix}`; recipe `matrix(p[:-1])`; type :answer.type/math.
- 2. original `Undefined`; recipe `undefined`; type :answer.type/text.
- 3. original `\begin{bmatrix}-10 & 50 & 10 \\ 6 & -30 & -6 \\ 0 & 0 & 0 \\ 8 & -40 & -8\end{bmatrix}`; recipe `matrix(p)`; type :answer.type/math.
- 4. original `\begin{bmatrix}-10 & -50 & -10 \\ 6 & -30 & -6 \\ 0 & 0 & 0 \\ 8 & -40 & -8\end{bmatrix}`; recipe `matrix([[p[0][0],-p[0][1],-p[0][2]]]+p[1:])`; type :answer.type/math.

## q-129961
Source label: {':db/ident': ':question.difficulty/easy'}; parameters: `{"a": [-1, -3], "b": [3, -1]}`; family: outer-2x2.
Prompt:

If
$A=\begin{bmatrix}-1 \\ -3\end{bmatrix}$
and
$B=\begin{bmatrix}3 & -1\end{bmatrix}$
then $AB=$
Solution:

Here, $A$ is a $2\times 1$ matrix and $B$ is a $1\times 2$ matrix. 

There is $1$ column in $A$ and $1$ row in $B,$ so $A$ and $B$ are conformable for multiplication: 

$$
{A}_{2\times \boxed{\text{1}}}{\cdot }_{✓}{B}_{\boxed{\text{1}}\times 2}={AB}_{2\times 2}
$$

Let's compute $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}-1 \\ -3\end{bmatrix}\begin{bmatrix}3 & -1\end{bmatrix}=\begin{bmatrix}-3 & ∗ \\ ∗ & ∗\end{bmatrix}, &  & \,-3=-1\cdot 3 \\  & \begin{bmatrix}-1 \\ -3\end{bmatrix}\begin{bmatrix}3 & -1\end{bmatrix}=\begin{bmatrix}-3 & 1 \\ ∗ & ∗\end{bmatrix}, &  & \,1=(-1)\cdot (-1) \\  & \begin{bmatrix}-1 \\ -3\end{bmatrix}\begin{bmatrix}3 & -1\end{bmatrix}=\begin{bmatrix}-3 & 1 \\ -9 & ∗\end{bmatrix}, &  & \,-9=(-3)\cdot 3 \\  & \begin{bmatrix}-1 \\ -3\end{bmatrix}\begin{bmatrix}3 & -1\end{bmatrix}=\begin{bmatrix}-3 & 1 \\ -9 & 3\end{bmatrix}, &  & \,3=(-3)\cdot (-1)\end{aligned}
$$

Therefore, 
$AB=\begin{bmatrix}-3 & 1 \\ -9 & 3\end{bmatrix}.$
Field `selection` :answer-field.type/radio; correct 1 (zero-based source bank index).
- 0. original `\begin{bmatrix}-3 \\ -1\end{bmatrix}`; recipe `matrix([[p[0][0]],[a[0]]])`; type :answer.type/math.
- 1. original `\begin{bmatrix}-3 & 1 \\ -9 & 3\end{bmatrix}`; recipe `matrix(p)`; type :answer.type/math.
- 2. original `\begin{bmatrix}3 & -1 \\ -9 & 3\end{bmatrix}`; recipe `matrix([[-p[0][0],-p[0][1]]]+p[1:])`; type :answer.type/math.
- 3. original `\begin{bmatrix}-3 & 9\end{bmatrix}`; recipe `matrix([[p[0][0],-p[1][0]]])`; type :answer.type/math.
- 4. original `\begin{bmatrix}-1 \\ -9\end{bmatrix}`; recipe `matrix([[a[0]],[p[1][0]]])`; type :answer.type/math.

## q-130136
Source label: {':db/ident': ':question.difficulty/easy'}; parameters: `{"a": [4, 2, 1, 1], "b": [1, 0, 4]}`; family: outer-4x3.
Prompt:

$\begin{bmatrix}4 \\ 2 \\ 1 \\ 1\end{bmatrix}\begin{bmatrix}1 & 0 & 4\end{bmatrix}=$
Solution:

Here, the first factor is $4\times 1$ matrix and the second factor is a $1\times 3$ matrix. 

There is $1$ column in the first matrix and $1$ row in the second matrix, so the product is well defined:

$$
4\times \boxed{\text{1}}✓\boxed{\text{1}}\times 3=4\times 3
$$

Computing the product, we have

$$
\begin{aligned}\begin{bmatrix}4 \\ 2 \\ 1 \\ 1\end{bmatrix}\begin{bmatrix}1 & 0 & 4\end{bmatrix} & =\begin{bmatrix}4\cdot 1 & 4\cdot 0 & 4\cdot 4 \\ 2\cdot 1 & 2\cdot 0 & 2\cdot 4 \\ 1\cdot 1 & 1\cdot 0 & 1\cdot 4 \\ 1\cdot 1 & 1\cdot 0 & 1\cdot 4\end{bmatrix} \\  & =\begin{bmatrix}4 & 0 & 16 \\ 2 & 0 & 8 \\ 1 & 0 & 4 \\ 1 & 0 & 4\end{bmatrix}\end{aligned}
$$
Field `selection` :answer-field.type/radio; correct 0 (zero-based source bank index).
- 0. original `\begin{bmatrix}4 & 0 & 16 \\ 2 & 0 & 8 \\ 1 & 0 & 4 \\ 1 & 0 & 4\end{bmatrix}`; recipe `matrix(p)`; type :answer.type/math.
- 1. original `\begin{bmatrix}4 & 1 & 16 & 1 \\ 0 & 0 & 0 & 0 \\ 2 & -1 & 8 & 2 \\ 1 & 0 & 4 & 3\end{bmatrix}`; recipe `matrix([[p[0][0],a[2],p[0][2],a[3]],[p[0][1],p[1][1],p[2][1],p[3][1]],[p[1][0],-a[2],p[1][2],a[1]],[p[2][0],p[2][1],p[2][2],a[0]-a[2]]])`; type :answer.type/math.
- 2. original `\begin{bmatrix}4 & 1 & 16 & 1 \\ 2 & -1 & 8 & 2 \\ 0 & 0 & 0 & 0 \\ 1 & 0 & 4 & 3\end{bmatrix}`; recipe `matrix([[p[0][0],a[2],p[0][2],a[3]],[p[1][0],-a[2],p[1][2],a[1]],[p[0][1],p[1][1],p[2][1],p[3][1]],[p[2][0],p[2][1],p[2][2],a[0]-a[2]]])`; type :answer.type/math.
- 3. original `\begin{bmatrix}4 & 1 & 16 \\ 2 & -1 & 8 \\ 1 & 0 & 4 \\ 0 & 4 & 0\end{bmatrix}`; recipe `matrix([[p[0][0],a[2],p[0][2]],[p[1][0],-a[2],p[1][2]],[p[2][0],p[2][1],p[2][2]],[p[3][1],p[3][2],p[3][1]]])`; type :answer.type/math.
- 4. original `Undefined`; recipe `undefined`; type :answer.type/text.

## q-130230
Source label: {':db/ident': ':question.difficulty/moderate'}; parameters: `{"a": [3, -4, 2], "b": [4, -3]}`; family: undefined-evidence.
Prompt:

Find $ST$, if 
$S=\begin{bmatrix}3 \\ -4 \\ 2\end{bmatrix}$
and 
$T=\begin{bmatrix}4 \\ -3\end{bmatrix}.$
Solution:

Here, $S$ is $3\times 1$ matrix and $T$ is a $2\times 1$ matrix. 

There is $1$ column in $S$ and $2$ rows in $T$, so the product is undefined:

$$
{S}_{3\times 1}{\times }_{\ne }{T}_{2\times 1}=\text{undefined}
$$
Field `selection` :answer-field.type/radio; correct 2 (zero-based source bank index).
- 0. original `\begin{bmatrix}24\end{bmatrix}`; recipe `matrix([[sum(a[i]*b[i] for i in range(2))]])`; type :answer.type/math.
- 1. original `\begin{bmatrix}12 & -15 \\ -16 & 20 \\ 8 & -10\end{bmatrix}`; recipe `matrix([[x*b[0],x*(b[1]-2)] for x in a])`; type :answer.type/math.
- 2. original `Undefined`; recipe `undefined`; type :answer.type/text.
- 3. original `\begin{bmatrix}-1\end{bmatrix}`; recipe `matrix([[sum(a[:2])]])`; type :answer.type/math.
- 4. original `\begin{bmatrix}12 & -15 \\ 8 & -10\end{bmatrix}`; recipe `matrix([[a[i]*b[0],a[i]*(b[1]-2)] for i in [0,2]])`; type :answer.type/math.

## q-275545
Source label: {':db/ident': ':question.difficulty/easy'}; parameters: `{"a": [2, -1], "b": [-2, 3]}`; family: outer-2x2.
Prompt:

If
$A=\begin{bmatrix}2 \\ -1\end{bmatrix}$
and
$B=\begin{bmatrix}-2 & 3\end{bmatrix},$
find $AB.$

| $AB=\,\,$ |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
|  | {{field-3}} | {{field-4}} |  |  |
Solution:

Here, $A$ is a $2\times 1$ matrix and $B$ is a $1\times 2$ matrix. 

There is $1$ column in $A$ and $1$ row in $B,$ so $A$ and $B$ are conformable for multiplication: 

$$
{A}_{2\times \boxed{\text{1}}}{\cdot }_{✓}{B}_{\boxed{\text{1}}\times 2}={AB}_{2\times 2}
$$

Let's compute $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}2 \\ -1\end{bmatrix}\begin{bmatrix}-2 & 3\end{bmatrix}=\begin{bmatrix}-4 & ∗ \\ ∗ & ∗\end{bmatrix}, &  & \,-4=2\cdot -2 \\  & \begin{bmatrix}2 \\ -1\end{bmatrix}\begin{bmatrix}-2 & 3\end{bmatrix}=\begin{bmatrix}-4 & 6 \\ ∗ & ∗\end{bmatrix}, &  & \,6=2\cdot 3 \\  & \begin{bmatrix}2 \\ -1\end{bmatrix}\begin{bmatrix}-2 & 3\end{bmatrix}=\begin{bmatrix}-4 & 6 \\ 2 & ∗\end{bmatrix}, &  & \,2=-1\cdot -2 \\  & \begin{bmatrix}2 \\ -1\end{bmatrix}\begin{bmatrix}-2 & 3\end{bmatrix}=\begin{bmatrix}-4 & 6 \\ 2 & -3\end{bmatrix}, &  & \,-3=-1\cdot 3\end{aligned}
$$

Therefore, 
$AB=\begin{bmatrix}-4 & 6 \\ 2 & -3\end{bmatrix}.$
Field `field-4` :answer-field.type/blank; correct 0 (zero-based source bank index).
- 0. original `-3`; recipe `str(p[1][1])`; type :answer.type/math.
Field `field-2` :answer-field.type/blank; correct 0 (zero-based source bank index).
- 0. original `6`; recipe `str(p[0][1])`; type :answer.type/math.
Field `field-1` :answer-field.type/blank; correct 0 (zero-based source bank index).
- 0. original `-4`; recipe `str(p[0][0])`; type :answer.type/math.
Field `field-3` :answer-field.type/blank; correct 0 (zero-based source bank index).
- 0. original `2`; recipe `str(p[1][0])`; type :answer.type/math.

## q-275548
Source label: {':db/ident': ':question.difficulty/easy'}; parameters: `{"a": [1, 2, -2], "b": [1, -2]}`; family: outer-3x2.
Prompt:

Find $AB,$ if $A=\begin{bmatrix}1 \\ 2 \\ -2\end{bmatrix}$
and 
$B=\begin{bmatrix}1 & -2\end{bmatrix}.$

|  |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
| $AB=\,\,$ |  | {{field-3}} | {{field-4}} |  |
|  |  | {{field-5}} | {{field-6}} |  |
Solution:

Here, $A$ is $3\times 1$ matrix and $B$ is a $1\times 2$ matrix.  

There is $1$ column in matrix $A$ and $1$ row in matrix $B$, so the product is well defined:

$$
{A}_{3\times \boxed{\text{1}}}{\cdot }_{✓}{B}_{\boxed{\text{1}}\times 2}={AB}_{3\times 2}
$$

Computing the product, we have

$$
\begin{aligned}AB & =\begin{bmatrix}1 \\ 2 \\ -2\end{bmatrix}\begin{bmatrix}1 & -2\end{bmatrix} \\  & =\begin{bmatrix}1\cdot 1 & 1\cdot (-2) \\ 2\cdot 1 & 2\cdot (-2) \\ (-2)\cdot 1 & (-2)\cdot (-2)\end{bmatrix} \\  & =\begin{bmatrix}1 & -2 \\ 2 & -4 \\ -2 & 4\end{bmatrix}.\end{aligned}
$$
Field `field-6` :answer-field.type/blank; correct 0 (zero-based source bank index).
- 0. original `4`; recipe `str(p[2][1])`; type :answer.type/math.
Field `field-3` :answer-field.type/blank; correct 0 (zero-based source bank index).
- 0. original `2`; recipe `str(p[1][0])`; type :answer.type/math.
Field `field-2` :answer-field.type/blank; correct 0 (zero-based source bank index).
- 0. original `-2`; recipe `str(p[0][1])`; type :answer.type/math.
Field `field-5` :answer-field.type/blank; correct 0 (zero-based source bank index).
- 0. original `-2`; recipe `str(p[2][0])`; type :answer.type/math.
Field `field-4` :answer-field.type/blank; correct 0 (zero-based source bank index).
- 0. original `-4`; recipe `str(p[1][1])`; type :answer.type/math.
Field `field-1` :answer-field.type/blank; correct 0 (zero-based source bank index).
- 0. original `1`; recipe `str(p[0][0])`; type :answer.type/math.

## q-318484
Source label: {':db/ident': ':question.difficulty/easy'}; parameters: `{"a": [5, -2], "b": [1, -3]}`; family: outer-2x2.
Prompt:

If
$A=\begin{bmatrix}5 \\ -2\end{bmatrix}$
and
$B=\begin{bmatrix}1 & -3\end{bmatrix},$
find $AB.$

| $AB=\,\,$ |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
|  | {{field-3}} | {{field-4}} |  |  |
Solution:

Here, $A$ is a $2\times 1$ matrix and $B$ is a $1\times 2$ matrix. 

There is $1$ column in $A$ and $1$ row in $B,$ so $A$ and $B$ are conformable for multiplication: 

$$
{A}_{2\times \boxed{\text{1}}}{\cdot }_{✓}{B}_{\boxed{\text{1}}\times 2}={AB}_{2\times 2}
$$

Let's compute $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}5 \\ -2\end{bmatrix}\begin{bmatrix}1 & -3\end{bmatrix}=\begin{bmatrix}5 & ∗ \\ ∗ & ∗\end{bmatrix}, &  & \,5=5\cdot 1 \\  & \begin{bmatrix}5 \\ -2\end{bmatrix}\begin{bmatrix}1 & -3\end{bmatrix}=\begin{bmatrix}5 & -15 \\ ∗ & ∗\end{bmatrix}, &  & \,-15=5\cdot (-3) \\  & \begin{bmatrix}5 \\ -2\end{bmatrix}\begin{bmatrix}1 & -3\end{bmatrix}=\begin{bmatrix}5 & -15 \\ -2 & ∗\end{bmatrix}, &  & \,-2=-2\cdot 1 \\  & \begin{bmatrix}5 \\ -2\end{bmatrix}\begin{bmatrix}1 & -3\end{bmatrix}=\begin{bmatrix}5 & -15 \\ -2 & 6\end{bmatrix}, &  & \,6=-2\cdot (-3)\end{aligned}
$$

Therefore, 
$AB=\begin{bmatrix}5 & -15 \\ -2 & 6\end{bmatrix}.$
Field `field-2` :answer-field.type/blank; correct 0 (zero-based source bank index).
- 0. original `-15`; recipe `str(p[0][1])`; type :answer.type/math.
Field `field-1` :answer-field.type/blank; correct 0 (zero-based source bank index).
- 0. original `5`; recipe `str(p[0][0])`; type :answer.type/math.
Field `field-4` :answer-field.type/blank; correct 0 (zero-based source bank index).
- 0. original `6`; recipe `str(p[1][1])`; type :answer.type/math.
Field `field-3` :answer-field.type/blank; correct 0 (zero-based source bank index).
- 0. original `-2`; recipe `str(p[1][0])`; type :answer.type/math.

## q-318588
Source label: {':db/ident': ':question.difficulty/easy'}; parameters: `{"a": [0, 3, -1], "b": [-4, 2]}`; family: outer-3x2.
Prompt:

Find $PQ,$ if
$P=\begin{bmatrix}0 \\ 3 \\ -1\end{bmatrix}$
and
$Q=\begin{bmatrix}-4 & 2\end{bmatrix}.$

|  |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
| $PQ=\,\,$ |  | {{field-3}} | {{field-4}} |  |
|  |  | {{field-5}} | {{field-6}} |  |
Solution:

Here, $P$ is a $3\times 1$ matrix and $Q$ is a $1\times 2$ matrix.  

There is $1$ column in matrix $P$ and $1$ row in matrix $Q$, so the product is well defined:

$$
{P}_{3\times \boxed{\text{1}}}{\cdot }_{✓}{Q}_{\boxed{\text{1}}\times 2}={PQ}_{3\times 2}
$$

Computing the product, we have:

$$
\begin{aligned}PQ & =\begin{bmatrix}0 \\ 3 \\ -1\end{bmatrix}\begin{bmatrix}-4 & 2\end{bmatrix} \\  & =\begin{bmatrix}0\cdot (-4) & 0\cdot 2 \\ 3\cdot (-4) & 3\cdot 2 \\ (-1)\cdot (-4) & (-1)\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}0 & 0 \\ -12 & 6 \\ 4 & -2\end{bmatrix}.\end{aligned}
$$
Field `field-4` :answer-field.type/blank; correct 0 (zero-based source bank index).
- 0. original `6`; recipe `str(p[1][1])`; type :answer.type/math.
Field `field-6` :answer-field.type/blank; correct 0 (zero-based source bank index).
- 0. original `-2`; recipe `str(p[2][1])`; type :answer.type/math.
Field `field-2` :answer-field.type/blank; correct 0 (zero-based source bank index).
- 0. original `0`; recipe `str(p[0][1])`; type :answer.type/math.
Field `field-5` :answer-field.type/blank; correct 0 (zero-based source bank index).
- 0. original `4`; recipe `str(p[2][0])`; type :answer.type/math.
Field `field-3` :answer-field.type/blank; correct 0 (zero-based source bank index).
- 0. original `-12`; recipe `str(p[1][0])`; type :answer.type/math.
Field `field-1` :answer-field.type/blank; correct 0 (zero-based source bank index).
- 0. original `0`; recipe `str(p[0][0])`; type :answer.type/math.

## q-13635
Source label: {':db/ident': ':question.difficulty/easy'}; parameters: `{"a": [0, -2, -3], "b": [1, 2]}`; family: outer-3x2.
Prompt:

Find $AB$, if 
$A=\begin{bmatrix}0 \\ -2 \\ -3\end{bmatrix}$
and 
$B=\begin{bmatrix}1 & 2\end{bmatrix}.$
Solution:

Here, $A$ is $3\times 1$ matrix and $B$ is a $1\times 2$ matrix. 

There is $1$ column in matrix $A$ and $1$ row in matrix $B$, so the product is well defined:

$$
{A}_{3\times \boxed{\text{1}}}{\cdot }_{✓}{B}_{\boxed{\text{1}}\times 2}={AB}_{3\times 2}
$$

Computing the product, we have:

$$
\begin{aligned}AB & =\begin{bmatrix}0 \\ -2 \\ -3\end{bmatrix}\begin{bmatrix}1 & 2\end{bmatrix} \\  & =\begin{bmatrix}0\cdot 1 & 0\cdot 2 \\ (-2)\cdot 1 & (-2)\cdot 2 \\ (-3)\cdot 1 & (-3)\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}0 & 0 \\ -2 & -4 \\ -3 & -6\end{bmatrix}\end{aligned}
$$
Field `selection` :answer-field.type/radio; correct 0 (zero-based source bank index).
- 0. original `$$ \begin{bmatrix}0 & 0 \\ -2 & -4 \\ -3 & -6\end{bmatrix} $$`; recipe `matrix(p)`; type :answer.type/text.
- 1. original `$$ \begin{bmatrix}1 & 2 \\ -2 & -4 \\ -3 & -6\end{bmatrix} $$`; recipe `matrix([[b[0],b[1]]]+p[1:])`; type :answer.type/text.
- 2. original `$$ \begin{bmatrix}1 & 0 \\ -2 & -4 \\ -3 & -6\end{bmatrix} $$`; recipe `matrix([[b[0],p[0][1]]]+p[1:])`; type :answer.type/text.
- 3. original `Undefined`; recipe `undefined`; type :answer.type/text.
- 4. original `$$ \begin{bmatrix}0 & 0 \\ -2 & -4 \\ 3 & -6\end{bmatrix} $$`; recipe `matrix(p[:2]+[[-p[2][0],p[2][1]]])`; type :answer.type/text.
