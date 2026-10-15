# Template extraction

## 1. Specific source descriptions

The immutable source.json holds every field, answer, original key omission and raw string. templates.json extracts complete matrices, per-recipe prompt masks, source solution matrix nodes and exact surrounding prose; source-cases.json maps all originals to explicit parameter/profile calls.

### q-127270

Level: {':db/ident': ':question.difficulty/hard'}; assigned hard. Matrix [['a', '-a', 'a'], ['a', '-2b', 'b'], ['2a', '-b', 'a']]; column [['1'], ['-1'], ['-1']].

Field contract: [('selection', 'radio', 5, 4)].

Solution matrix nodes: 5 (two operands in first row; then dot products, optional evaluated additions, collected result).

### q-13554

Level: None; assigned easy. Matrix [['a', 'c'], ['b', 'd']]; column [['1'], ['2']].

Field contract: [('selection', 'radio', 5, None)].

Solution matrix nodes: 0 (two operands in first row; then dot products, optional evaluated additions, collected result).

### q-127276

Level: {':db/ident': ':question.difficulty/moderate'}; assigned moderate. Matrix [['s', 't'], ['-t', 's']]; column [['s'], ['t']].

Field contract: [('selection', 'radio', 5, 1)].

Solution matrix nodes: 5 (two operands in first row; then dot products, optional evaluated additions, collected result).

### q-127277

Level: {':db/ident': ':question.difficulty/moderate'}; assigned moderate. Matrix [['m', '2m'], ['-m', 'n']]; column [['-2'], ['3']].

Field contract: [('selection', 'radio', 5, 0)].

Solution matrix nodes: 5 (two operands in first row; then dot products, optional evaluated additions, collected result).

### q-275597

Level: {':db/ident': ':question.difficulty/hard'}; assigned hard. Matrix [['a', 'b', 'a'], ['a', '-b', 'a'], ['0', '0', 'a']]; column [['a'], ['0'], ['-a']].

Field contract: [('field-3', 'blank', 1, 0), ('field-2', 'blank', 1, 0), ('field-1', 'blank', 1, 0)].

Solution matrix nodes: 5 (two operands in first row; then dot products, optional evaluated additions, collected result).

### q-318589

Level: {':db/ident': ':question.difficulty/hard'}; assigned hard. Matrix [['b', 'a', '-b'], ['-b', 'a', 'b'], ['-b', '0', '-b']]; column [['-b'], ['0'], ['b']].

Field contract: [('field-3', 'blank', 1, 0), ('field-1', 'blank', 1, 0), ('field-2', 'blank', 1, 0)].

Solution matrix nodes: 5 (two operands in first row; then dot products, optional evaluated additions, collected result).

### q-318591

Level: {':db/ident': ':question.difficulty/hard'}; assigned hard. Matrix [['m', 'n', '-m'], ['m', '-n', '-m'], ['0', '2', '0']]; column [['1'], ['p'], ['1']].

Field contract: [('field-3', 'blank', 1, 0), ('field-1', 'blank', 1, 0), ('field-2', 'blank', 1, 0)].

Solution matrix nodes: 5 (two operands in first row; then dot products, optional evaluated additions, collected result).

### q-318595

Level: {':db/ident': ':question.difficulty/moderate'}; assigned moderate. Matrix [['6p', '-4q'], ['-5p', '2q']]; column [['p'], ['q']].

Field contract: [('field-2', 'blank', 1, 0), ('field-1', 'blank', 1, 0)].

Solution matrix nodes: 4 (two operands in first row; then dot products, optional evaluated additions, collected result).

### q-70226

Level: {':db/ident': ':question.difficulty/hard'}; assigned hard. Matrix [['x', 'y', 'x'], ['x', '-y', 'x'], ['-x', '-y', 'x']]; column [['x'], ['0'], ['-x']].

Field contract: [('selection', 'radio', 5, 0)].

Solution matrix nodes: 5 (two operands in first row; then dot products, optional evaluated additions, collected result).

### q-13556

Level: {':db/ident': ':question.difficulty/moderate'}; assigned moderate. Matrix [['b', 'b'], ['c', 'c']]; column [['3'], ['4']].

Field contract: [('selection', 'radio', 5, 2)].

Solution matrix nodes: 5 (two operands in first row; then dot products, optional evaluated additions, collected result).

## 2. Generalized pattern

Multiply each matrix row by the complete column vector in displayed order and collect polynomial terms. Return the entire result column, through the original vector radio or component blank fields. The result is always a column with the input row count. Variable names denote scalars; the matrix and vector object labels remain fixed complete labels.

## 3. Component and complete-bank mapping

Each source matrix entry and bank component is an exact polynomial expression recipe. Apply the simultaneous invertible substitution v ↦ c_v n_v to every scalar component, including source bank polynomials. This preserves all complete bank values and inequivalence without asserting a learner mistake explanation. For source-pattern profiles the algebraic expression is known but its original distractor intent is unverified. No arbitrary offsets or fitted numerical polynomials are used.

### q-127270 / observed

- selection option 1: `$\begin{bmatrix}a \\ a-b \\ a+b\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation False.

- selection option 2: `$\begin{bmatrix}3a \\ a+b \\ 2a+b\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation False.

- selection option 3: `$\begin{bmatrix}3a \\ a-b \\ a+b\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation False.

- selection option 4: `$\begin{bmatrix}3a \\ a+b \\ a+b\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation False.

- selection option 5: `$\begin{bmatrix}a \\ a+b \\ a+b\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation True.

### q-13554 / observed

- selection option 1: `$\begin{bmatrix}a + c \\ b + 2d\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation absent.

- selection option 2: `$\begin{bmatrix}a + 2c \\ 2b + 2d\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation absent.

- selection option 3: `$\begin{bmatrix}2a + 2c \\ b + 2d\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation absent.

- selection option 4: `$\begin{bmatrix}a + 2c \\ b + 2d\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation absent.

- selection option 5: `$\begin{bmatrix}a + 2c \\ b + d\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation absent.

### q-127276 / observed

- selection option 1: `$\begin{bmatrix}(s+t)^{2} \\ 0\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation False.

- selection option 2: `$\begin{bmatrix}{s}^{2}+{t}^{2} \\ 0\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation True.

- selection option 3: `$\begin{bmatrix}(s-t)^{2} \\ 0\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation False.

- selection option 4: `$\begin{bmatrix}{s}^{2}+{t}^{2} \\ -2st\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation False.

- selection option 5: `$\begin{bmatrix}(s+t)^{2} \\ -2st\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation False.

### q-127277 / observed

- selection option 1: `$\begin{bmatrix}4m \\ 2m+3n\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation True.

- selection option 2: `$\begin{bmatrix}2m \\ 2m+3n\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation False.

- selection option 3: `$\begin{bmatrix}4m \\ m+n\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation False.

- selection option 4: `$\begin{bmatrix}2m \\ 2m+n\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation False.

- selection option 5: `$\begin{bmatrix}4m \\ 2m+n\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation False.

### q-275597 / observed

- field-3 option 1: `$-{a}^{2}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation True.

- field-2 option 1: `$0$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation True.

- field-1 option 1: `$0$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation True.

### q-318589 / observed

- field-3 option 1: `$0$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation True.

- field-1 option 1: `$-2{b}^{2}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation True.

- field-2 option 1: `$2{b}^{2}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation True.

### q-318591 / observed

- field-3 option 1: `$2p$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation True.

- field-1 option 1: `$np$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation True.

- field-2 option 1: `$-np$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation True.

### q-318595 / observed

- field-2 option 1: `$-5{p}^{2}+2{q}^{2}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation True.

- field-1 option 1: `$6{p}^{2}-4{q}^{2}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation True.

### q-70226 / observed

- selection option 1: `$\begin{bmatrix}0 \\ 0 \\ -2{x}^{2}\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation True.

- selection option 2: `$\begin{bmatrix}{x}^{3}y \\ 0 \\ -{x}^{3}y\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation False.

- selection option 3: `$\begin{bmatrix}{x}^{2}y \\ 0 \\ -{x}^{2}y\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation False.

- selection option 4: `$\begin{bmatrix}{x}^{2} \\ -{x}^{2} \\ 0\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation False.

- selection option 5: `$\begin{bmatrix}{x}^{2} \\ 0 \\ -{x}^{2}\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation False.

### q-13556 / observed

- selection option 1: `$\begin{bmatrix}-7b \\ -7c\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation False.

- selection option 2: `$\begin{bmatrix}7c \\ 7c\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation False.

- selection option 3: `$\begin{bmatrix}7b \\ 7c\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation True.

- selection option 4: `$\begin{bmatrix}7b \\ 7b\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation False.

- selection option 5: `$\begin{bmatrix}7c \\ 7b\end{bmatrix}$`; recipe: simultaneous symbol substitution in this complete expression; original correct designation False.

For q-13554, independent numeric column slots (u,v) use the explicit five whole-vector recipes [(ua+c,ub+vd), (ua+vc,vb+vd), (va+vc,ub+vd), (ua+vc,ub+vd), (ua+vc,ub+d)]. At u=1,v=2 these reproduce all five original choices, with the fourth mathematically correct; the source has no designation. Each a,b,c,d here denotes its scaled displayed matrix entry.

Normal default radios outside q-13554 use a separately authored complete five-option bank: correct row sums, negated result, omit first column contributions, omit last column contributions, and a family-fixed fifth operation. The fifth operation swaps the input vector entries for q-127276, reverses result rows for q-13556, uses an all-one column for q-127277, and removes leading negative signs of the vector entries for q-127270/q-70226. These are operation recipes, not learner-facing diagnoses. Each whole profile is selected before constructing options; collisions reject the entire instance. All observed profiles remain explicitly selectable.

## 4. Reusable masks and slots

Fixed: matrix dimensions, expression pattern, zero positions, matrix/vector object labels, source-specific Markdown layout, field count/types/keys, and ordered operative teaching stages. The full result column is the assessed target; row/column positions are not independently permuted because their order defines multiplication and field-component roles.

Variable: each scalar symbol has a positive integer coefficient c_v in 1..5 and a distinct single-letter name n_v, excluding the column object label. Every source monomial, factor, evaluated term, answer and bank option derives from these same symbol slots. Coefficients add no operations and retain source polynomial degree/cancellation structure. Moderate/hard keep exactly four/nine substantive product positions, including original zero factors. Symbol renames are presentation variation and excluded from mathematical-task fingerprints.

Easy numeric vector slots: u=1..4, v=2..5, u≠v. These stay positive; all four row products remain. The v≠1 and u≠v conditions keep every observed bank member distinct. Source replay uses [1,2]. Every scalar coefficient candidate1..5 is probed with remaining data held fixed; values beyond the actual workload caps are explicitly rejected. Every accepted variable name is tested; all easy vector pairs are checked with over-cap pairs rejected. Representative all-low/all-high/mixed corners test interactions. The moderate q-318595 blank family additionally supports independently chosen coefficient magnitudes1..6 with its original +,-,-,+ signs; its unit-symbol vector remains. Hard q-275597/q-318589/q-70226 support uniform matrix gain1..2; both operand roles and all original zero/cancellation patterns remain.

Source banks, profile aliases, seed and option order do not inflate mathematical identity. Mathematical fingerprints use canonical scalar-role symbols and actual printed matrix/vector expressions. Content UUIDs include normalized prompt, fixed solution, complete field-owned bank and correct answer. The same displayed content has the same UUID despite seed or option-order changes. Normalization and C0 checks run before IDs.

The canonical images are mathematical typesetting, not geometric plots. No generated images are required. The lesson explains row dot products; variable coefficient changes remain in this KP and prerequisite polynomial simplification. Actual numeric workload is independently checked from printed operands, ordered row products and collected answers. Frozen source maxima are: easy canonical product3 (unrated source2), moderate product6 and collected7, hard product2 and collected2. Enforced caps (factor/product/collected numeric polynomial coefficients) are easy3/6/6, moderate6/6/7, hard2/4/4. Easy allows small products up to6 while factors stay within canonical3; hard permits at most2×2=4 and collection4. Both remain one-digit arithmetic. Moderate retains the actual observed maxima. Larger q-318595 products such as24p×4p=96p² are rejected. Positive scale slots1..5 remain only when the whole actual instance satisfies these tighter per-level caps. q-318595 independent coefficient slots1..6 preserve four products, signs and degree, yielding meaningful variety without making its arithmetic larger. Hard matrix gains preserve cancellation while allowing actual changed coefficients; finite domains are not presented as unlimited diversity. Mathematical fingerprints zero out matrix entries multiplied by a fixed zero vector entry, so irrelevant symbol/scale changes do not inflate task counts.

Native parsing reserves ln as a function token. A scalar l·n product therefore renders with explicit \cdot instead of concatenated ln. The held-name tests discovered this real parser limitation; formatting disambiguates the polynomial product. No engine edits.
