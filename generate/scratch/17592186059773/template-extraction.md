# Template extraction

Basis 2368, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Complete observed practice: eight moderate, three instructional templates, eight complete bank profiles. Two incomplete unrated questions remain untouched.

The shared prompt supplies two 3 by 3 integer matrices and asks which of five row expressions transforms the first into the second. Each response is one radio field named `selection`. The solution first identifies unchanged and changed rows, considers operations on those rows, shows the supplied and target matrices linked by the correct operation, and concludes with that operation. Scaling, swapping and row addition remain separate templates because they change different numbers of rows and perform different arithmetic.

Fixed structure: 3 by 3 matrices, five choices from a single source bank, one elementary correct operation, matrix names, radio response, observed ordered solution sentences. Coefficients in each source bank are deliberately fixed to their observed values; a source fraction is not extrapolated into an invented distractor misconception. Source q-72850 includes two non-elementary distractor expressions; they are preserved exactly as row replacement expressions and validated as incorrect. No profiles are mixed.

Variable slots: one originally nonzero supplied matrix entry may change by any of -3, -2, -1, 1, 2, 3 subject to retaining its original sign and nonzero status. Originally zero entries remain zero. The target matrix is recomputed from the supplied matrix and correct operation. This is a conservative same-method numeric generalization; other coefficients, zeros and dimensions remain observed. All three row identities may be permuted together, with target rows, bank expressions, ordinal prose and final solution operation following the same permutation. Row permutations alone do not count as novelty.

All eight sources show only the supplied matrix and its numeric target in the worked solution, so substitution changes both matrices without adding/removing solution stages. Symbolic row-operation expressions and mathematical signs stay delimiter-free in answer values. Every source is replayed at delta zero and identity row mapping for exact prompt, solution and full-bank fidelity. A matrix name change, seed, UUID, source profile, choice order, row permutation, or uniform scalar multiple is excluded from the mathematical task fingerprint.

The finite sampling policy changes actual numerical data within the same operation-recognition workload. Each candidate has all five expressions executed independently; equivalent outcomes or more than one correct choice invalidate the candidate. Source constants and psychological distractor interpretations remain separate: exact row-expression recipes are recorded in choice-recipes.json; unresolved intent is not learner feedback.

## q-130087

Source UUID b8c55c12-17df-581d-b93b-78d07db8cec0; operation ('replace', 2, (0, 0, 1/5)).

Supplied matrix: `[[5, 2, -3], [-8, 0, 2], [10, 5, -5]]`. Target matrix: `[[5, 2, -3], [-8, 0, 2], [2, 1, -1]]`. Nonzero entries are signed integers; exact rational coefficients occur in some banks. The exact prompt and worked solution are retained in source.json and review.md.

Complete source bank (all five expressions retained together):

- `{R}_{3}:={R}_{3}+(-2)\cdot {R}_{1}` → `('replace', 2, (-2, 0, 1))`
- `{R}_{3}:=\frac{1}{5}\cdot {R}_{3}` → `('replace', 2, (0, 0, 1/5))` (correct)
- `{R}_{3}:={R}_{3}+{R}_{2}` → `('replace', 2, (0, 1, 1))`
- `{R}_{2}:={R}_{2}+{R}_{3}` → `('replace', 1, (0, 1, 1))`
- `{R}_{2}:={R}_{2}+(-\frac{3}{10})\cdot {R}_{3}` → `('replace', 1, (0, 1, -3/10))`

## q-130095

Source UUID 84b806b0-6ebe-59b8-9bb2-7c89ea346a6f; operation ('replace', 0, (3, 0, 0)).

Supplied matrix: `[[-2, 1, -1], [7, 7, 2], [-6, 1, 6]]`. Target matrix: `[[-6, 3, -3], [7, 7, 2], [-6, 1, 6]]`. Nonzero entries are signed integers; exact rational coefficients occur in some banks. The exact prompt and worked solution are retained in source.json and review.md.

Complete source bank (all five expressions retained together):

- `{R}_{1}:={R}_{1}+{R}_{2}` → `('replace', 0, (1, 1, 0))`
- `{R}_{1}:=\frac{1}{3}\cdot {R}_{1}` → `('replace', 0, (1/3, 0, 0))`
- `{R}_{1}↔{R}_{3}` → `('swap', 0, 2)`
- `{R}_{1}:=3\cdot {R}_{1}` → `('replace', 0, (3, 0, 0))` (correct)
- `{R}_{1}:={R}_{1}+(-\frac{4}{7})\cdot {R}_{2}` → `('replace', 0, (1, -4/7, 0))`

## q-130100

Source UUID 85e6dfb7-2447-51c4-a184-4a363a6b54d0; operation ('swap', 1, 2).

Supplied matrix: `[[5, -2, 3], [8, -3, 7], [-3, 1, -3]]`. Target matrix: `[[5, -2, 3], [-3, 1, -3], [8, -3, 7]]`. Nonzero entries are signed integers; exact rational coefficients occur in some banks. The exact prompt and worked solution are retained in source.json and review.md.

Complete source bank (all five expressions retained together):

- `{R}_{3}:={R}_{3}-{R}_{1}` → `('replace', 2, (-1, 0, 1))`
- `{R}_{3}:=(-\frac{8}{3})\cdot {R}_{3}` → `('replace', 2, (0, 0, -8/3))`
- `{R}_{2}↔{R}_{3}` → `('swap', 1, 2)` (correct)
- `{R}_{2}:={R}_{2}+(-5)\cdot {R}_{1}` → `('replace', 1, (-5, 1, 0))`
- `{R}_{2}:=(-\frac{3}{8})\cdot {R}_{2}` → `('replace', 1, (0, -3/8, 0))`

## q-130103

Source UUID 8d79bcd3-c9f6-51cc-bac3-1326fcc4218c; operation ('replace', 0, (1, 0, 5)).

Supplied matrix: `[[0, 0, 5], [5, 6, 10], [1, -1, -3]]`. Target matrix: `[[5, -5, -10], [5, 6, 10], [1, -1, -3]]`. Nonzero entries are signed integers; exact rational coefficients occur in some banks. The exact prompt and worked solution are retained in source.json and review.md.

Complete source bank (all five expressions retained together):

- `{R}_{1}:={R}_{1}+5{R}_{3}` → `('replace', 0, (1, 0, 5))` (correct)
- `{R}_{1}:={R}_{1}+{R}_{2}` → `('replace', 0, (1, 1, 0))`
- `{R}_{1}:={R}_{1}+\frac{1}{5}{R}_{3}` → `('replace', 0, (1, 0, 1/5))`
- `{R}_{1}↔{R}_{2}` → `('swap', 0, 1)`
- `{R}_{3}:={R}_{3}+5{R}_{1}` → `('replace', 2, (5, 0, 1))`

## q-20387

Source UUID bf5f9366-1ce3-5395-93b6-14a04149ebc4; operation ('replace', 0, (1/4, 0, 0)).

Supplied matrix: `[[60, 0, 120], [20, 0, 40], [15, 0, 30]]`. Target matrix: `[[15, 0, 30], [20, 0, 40], [15, 0, 30]]`. Nonzero entries are signed integers; exact rational coefficients occur in some banks. The exact prompt and worked solution are retained in source.json and review.md.

Complete source bank (all five expressions retained together):

- `{R}_{1}:={R}_{1}-\frac{1}{2}{R}_{3}` → `('replace', 0, (1, 0, -1/2))`
- `{R}_{1}:=-\frac{1}{4}{R}_{1}` → `('replace', 0, (-1/4, 0, 0))`
- `{R}_{1}:=\frac{1}{4}{R}_{1}` → `('replace', 0, (1/4, 0, 0))` (correct)
- `{R}_{1}:=(-2){R}_{1}` → `('replace', 0, (-2, 0, 0))`
- `{R}_{1}:={R}_{1}+\frac{1}{4}{R}_{2}` → `('replace', 0, (1, 1/4, 0))`

## q-72850

Source UUID c70a88ac-8f1d-5e97-afff-9c3f83ff71f2; operation ('swap', 0, 2).

Supplied matrix: `[[1, 3, 2], [6, 4, 5], [1, 2, -1]]`. Target matrix: `[[1, 2, -1], [6, 4, 5], [1, 3, 2]]`. Nonzero entries are signed integers; exact rational coefficients occur in some banks. The exact prompt and worked solution are retained in source.json and review.md.

Complete source bank (all five expressions retained together):

- `{R}_{1}↔{R}_{3}` → `('swap', 0, 2)` (correct)
- `{R}_{2}↔{R}_{1}` → `('swap', 1, 0)`
- `{R}_{3}:={R}_{2}+(-5){R}_{1}` → `('replace', 2, (-5, 1, 0))`
- `{R}_{2}↔{R}_{3}` → `('swap', 1, 2)`
- `{R}_{2}:=2{R}_{3}+4{R}_{1}` → `('replace', 1, (4, 0, 2))`

## q-72854

Source UUID 4a88dee0-a622-519b-8c88-19f1fcfff46b; operation ('replace', 1, (4, 1, 0)).

Supplied matrix: `[[1, 1, 2], [-4, -1, 1], [2, 1, 6]]`. Target matrix: `[[1, 1, 2], [0, 3, 9], [2, 1, 6]]`. Nonzero entries are signed integers; exact rational coefficients occur in some banks. The exact prompt and worked solution are retained in source.json and review.md.

Complete source bank (all five expressions retained together):

- `{R}_{2}:={R}_{2}+{R}_{3}` → `('replace', 1, (0, 1, 1))`
- `{R}_{2}:={R}_{2}+2{R}_{3}` → `('replace', 1, (0, 1, 2))`
- `{R}_{1}↔{R}_{2}` → `('swap', 0, 1)`
- `{R}_{2}:={R}_{2}+4{R}_{1}` → `('replace', 1, (4, 1, 0))` (correct)
- `{R}_{2}↔{R}_{3}` → `('swap', 1, 2)`

## q-72856

Source UUID dd718a57-6301-5304-b58e-f8632645f2ed; operation ('replace', 1, (2, 1, 0)).

Supplied matrix: `[[1, 3, 2], [-2, 4, -2], [0, -1, -1]]`. Target matrix: `[[1, 3, 2], [0, 10, 2], [0, -1, -1]]`. Nonzero entries are signed integers; exact rational coefficients occur in some banks. The exact prompt and worked solution are retained in source.json and review.md.

Complete source bank (all five expressions retained together):

- `{R}_{2}:={R}_{2}+2{R}_{1}` → `('replace', 1, (2, 1, 0))` (correct)
- `{R}_{2}↔{R}_{3}` → `('swap', 1, 2)`
- `{R}_{2}:=\frac{1}{2}{R}_{2}` → `('replace', 1, (0, 1/2, 0))`
- `{R}_{2}:={R}_{2}+(-2){R}_{3}` → `('replace', 1, (0, 1, -2))`
- `{R}_{2}↔{R}_{1}` → `('swap', 1, 0)`
