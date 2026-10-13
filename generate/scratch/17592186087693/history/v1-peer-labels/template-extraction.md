# Template extraction

## 1. Specific source descriptions

`source-components.json` gives every actual entry, row count, column count and complete original field bank. q-11454 has signed integers in a 2×4 bmatrix, inline after a line break; q-7806 has integers in a 2×3 bmatrix in the same layout. q-125527 is a 6×6 inline aligned array with integers (including zeros and repeated entries). q-125528 is a 2×2 array with two radical entries and −23. q-125529 is a 3×3 array containing signed integers, zero and radicals. q-69542 is a 4×2 integer array with a line break before its matrix. q-139406 is a 3×3 matrix P, introduced as Maria's representation of a table; no table is actually supplied or required. It requests rows and columns as separate blanks around ×, with capture whitespace. q-319310 is a 5×5 K with integer, radical and fractional entries and two blanks after “Let”.

All radio sources have five **ordered dimension pairs**; blanks have one integer fragment each, not a combined product. All six available solutions consist of one fixed sentence: count rows, count columns, then state the ordered dimensions. The two legacy cases have no source solution; the same canonical sentence is authored for them. The canonical sentence does not calculate entries.

## 2. Generalized shared pattern

Given one fully displayed rectangular array with at least two rows and columns, count horizontal rows and vertical columns, reporting row-count × column-count. Entry sign or number form has no effect. Preserve two-count field layouts separately from whole-pair radios, and preserve the three radio prompt/layout masks plus two blank masks separately.

## 3. Component and complete-bank mapping

`recipes.json` stores parameterized prompt masks with complete `@ARRAY@` and `@NAME@` components; it never stores a complete answer payload or chooses an answer by source ID. `source-components.json` maps every original radio choice one-to-one to its separator and the following symbolic pair recipe, evaluated with independent row/column counts r,c. Original blank mapping is field-1→r and field-2→c, while preserving original collection order.

| Profile/source | Entire bank in captured order |
|---|---|
| q-11454 | (c,r), (r,c), (r,r), (r+1,r+1), (r,c−1) |
| q-7806 | (r,c), (c,r), (c,c), (r,c+1), (r,r) |
| q-125527 | (r−1,c−1), (r,c), (r−1,c), (r−2,c−2), (r,c−2) |
| q-125528 | (r,c+1), (r−1,c−1), (r,c), (r+1,c), (r+1,c+1) |
| q-125529 | (r,c−1), (r−1,c−1), (r+2,c+2), (r+2,c), (r,c) |
| q-69542 | (r−1,c), (c,r), (r,c), (r,c+1), (r−1,c+2) |

The large offsets and midpoint-square member are exact observed **expression patterns**, with underdetermined pedagogical intent. They are available only as labeled explicit replay profiles; this document does not claim those scalar offsets recover a learner error. Five distinct positive dimension pairs are required together before any complete instance is eligible. Every observed bank is exhaustively checked on all 25 dimension pairs; exact eligible domains are recorded in `validation.json`. No pooled-bank first-valid fallback is used.

## 4. Reusable template and finite domains

Fixed: original prose and Markdown mask, environment, answer-field type/key/order, every bank recipe/separator, one row/column sentence and its stage order. Variable: a complete rectangular array and its matrix letter; derived: r, c, every bank value, each blank count and four count occurrences in solution. Source q-139406's R/P error is preserved only on explicit replay with original name P, and the raw source remains unchanged. The other available solutions replay byte-for-byte. The two missing solutions/keys and unrated labels are explicitly authored/inferred.

All normal levels use display math with bmatrix, a single letter, and either a five-choice radio or two blanks. The finite mathematical domain is exactly `{2,3,4,5,6} × {2,3,4,5,6}`: 25 ordered dimensions per level and 25 in their union. Both square and rectangular shapes occur in every level. Do not multiply the task count by matrix entries, letter, bank, layout or difficulty label. Entry sampling uses integers −9..9, familiar √2, −√3 and 1/3; explicit inputs allow source-compatible signed integers of absolute value ≤30, radicals with radicand 2..13, and bounded fractions (numerator 1..30, denominator 1..9). These bounds preserve legible 6×6 matrices; rectangularity and cell syntax are checked even for explicit parameters.

Default rectangular bank: correct (r,c), reversed (c,r), rows used twice (r,r), columns used twice (c,c), overcount both (r+1,c+1). Default square bank: correct; undercount both; overcount both; overcount columns; overcount rows. They are separately authored complete banks; rectangular and square eligibility are disjoint, so square swap duplicates never enter a bank. All pairs are positive and distinct. Field choices are deterministically shuffled after identifying the correct owned UUID. Exact fixed content has one identity independent of seed or choice order.

The moderate/hard extension is a curriculum design claim limited to equal-method peer repetition, not a claim of measured higher workload. It introduces no new mathematical task. Explicit bounds equal random-sampler bounds at all three levels. Parameter fingerprint retains only ordered row/column counts. Content fingerprint retains version, actual entries via displayed prompt, complete fixed solution, field layouts and complete displayed bank, ignoring option order. Source aliases, incidental metadata and level label cannot create new IDs for identical learner content.
