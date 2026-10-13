# Classification

Immutable evidence: `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json`, `topic.json`, and `lesson.json` preserve their complete capture wrappers. Eight practice questions, six observed moderate and two unrated; no observed easy/hard practice records.

| Source | Recorded difficulty | Template | Target | Array dimensions in displayed order | Correct selection |
|---|---|---|---|---|---|
| q-69514 | unrated | legacy_bmatrix | 1×2 | B:2×2, C:2×1, D:1×2 | D only (derived) |
| q-69515 | unrated | legacy_bmatrix | 3×4 | P:2×2, Q:4×3, R:3×4 | R only (derived) |
| q-125550 | moderate | aligned_single | 3×2 | E:2×3, F:3×2, G:3×3 | F only |
| q-125552 | moderate | aligned_single | 2×1 | B:2×2, C:2×1, D:1×2 | C only |
| q-69518 | moderate | aligned_single | 3×2 | L:2×2, M:2×3, N:3×2 | N only |
| q-69523 | moderate | aligned_single | 4×3 | L:4×3, M:3×4, N:2×3 | L only |
| q-125549 | moderate | aligned_multiple | 2×2 | P:2×2, Q:4×2, R:2×2 | P and R only |
| q-69517 | moderate | aligned_single | 3×1 | F:3×3, G:3×1, H:1×3 | G only |

All fields are `selection` radio, five text choices. Each bank has all three singleton subsets and two pair subsets; eight named replay profiles correspond to **three meaningful unordered subset-bank patterns**. Choice-order or label aliases do not count as additional templates/banks/tasks. Source values and full mapping are in `source-components.json`.

Observed templates: `legacy_bmatrix` has an inline bmatrix list, spaced equals and commas, and target `\cdot`; `aligned_single` has display aligned arrays and a one-match conclusion; `aligned_multiple` has the same array layout but a two-match conclusion. The legacy sources have no solution; the normal API supplies an explicitly authored explanation following the six source solutions' common counting sequence. Unrated records are assigned moderate only as an authored design decision based on identical three-array/five-choice reasoning.

Plots: **none**, across every level/template. Arrays are mathematical typesetting, not parameter-dependent diagrams; no renderer or source image is involved. No plot-extraction or plot-generator implementation is necessary.

## Curriculum and authored scope

The linked lesson route, reconstructed from first-step/next rather than collection order, is Introduction → Square Matrices → Determining the Dimensions of a Matrix → Matrices With One Row or Column → Determining the Dimensions of a Matrix with One Row or Column → **Identifying a Matrix by Its Description** → Using Matrices for Modeling → Matrices for Route Planning. This KP reverses the preceding row/column counting question: interpret ordered dimensions, count each candidate, choose matching labels. Matrix arithmetic, entry indexing, determinant calculation, and route modeling belong elsewhere. Radicals, signed numbers and decimals are merely entries, not computation tasks.

- **Easy, authored:** one matching array among three; nonsquare target sides 1–3; other arrays are its transpose and a square with one of its side lengths. This isolates the already-taught ordered row/column distinction and includes row/column vectors. It has a finite **12** meaningful shape tasks; changing numbers or labels is presentation variety only.
- **Moderate, observed plus authored peers:** one or two matching arrays; all sides 1–4, matching the source's vectors, square matrices and rectangles. Other dimensions may be any nonmatching shapes within the observed size bound. The two-match source proves that selecting an exact subset is in scope. The finite anonymous shape catalog contains **1920** tasks. These are peer instances, not a sequence of stages.
- **Hard, authored:** same three-array count and five-choice response; target sides 3–4; every nonmatching candidate differs by exactly one row or column, with sides 2–4. The demand is keeping two close counts in order across visually similar arrays, including one or two matches; there is no harder algebra. **25** meaningful shape tasks. This difficulty is a contextual authoring claim; no source hard label establishes it as MA's own scale.

All normal random generation uses authored peer templates and whole eligible banks. Source templates stay available with explicit complete parameters. Larger dimensions do not imply unlimited diversity; finite catalog counts exclude entries, names, candidate order and bank aliases.
