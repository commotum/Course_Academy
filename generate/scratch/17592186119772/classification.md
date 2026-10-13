# Classification

Capture: `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is a byte-for-byte copy of the captured wrapper. All eight practice questions are rated. Canonical example e-4395 is context, not a ninth practice question.

| Level | Observed questions | Template / response | Complete profiles | Plot rating |
|---|---:|---|---:|---|
| Easy | 6 | One upper/lower triangular matrix among five whole labeled matrices; math radio options; correct matrix plus four foils repeated in solution | 6 | none |
| Moderate | 2 | Identify the complete qualifying subset among three labeled matrices; five text radio choices; real offdiagonal witnesses in solution | 2 | none |
| Hard | 0 | Authored five 4×4 matrices, identify complete subset of two or three; five text radio choices | 2 authored | none |

The easy source family has conditional upper/lower wording. Moderate has separate observed singular and plural correct-set prose branches, both retained exactly in source-profile masks. They are not merged into a generic solution. Every full source bank is separately parameterized; source-choice-mapping.json records all 45 options across nine captured fields.

Easy profiles: q-68740, q-126352, q-126354, q-13760, q-126353, q-74316. Moderate: q-42090 (one correct A, mixed 4×4/3×3 dimensions) and q-126351 (A and B correct, all 2×2, A is identity). The canonical raster shows three 3×3 matrices and lower triangular B; each other matrix has a real above-diagonal witness.

q-42090 has two duplicate `selection` radio fields in EDB. The first lacks a correct designation, the second specifies A only. Both fields have the same complete five-value bank. The original MA normalized JSON (`question_id:42090`, `question_format:multiple-choice`, `choice_count:5`) and inspected screenshot show **one** widget. Normal generation removes the first duplicate; `raw:q-42090` preserves both and the missing correct-ref key. Neither field lacks its key. The historical artifact is unkeyed only with respect to correctness, not `:answer-field/key`. No checkbox migration is performed.

Hard scope is an explicit authorship claim. The linked lesson route, traversed from `:activity/first-step` through `:step/next`, is Introduction → Describing a Triangular Matrix → **Identifying a Triangular Matrix** → Identifying Correct Statements About a Matrix. Introduction explicitly permits any entries, including zero, on the diagonal and allowed side. Prerequisite topics are Zero/Square/Diagonal/Identity Matrices and Transpose; successor topics include Block Matrices, LU, Determinants, and Inverses. This generator uses only square size and opposite-side zero support. It introduces none of those operations and no multi-statement question.

Within hard, every task inspects five 4×4 matrices (six relevant positions per matrix), includes a diagonal qualifying matrix, and recognizes the entire subset. Each strict qualifying matrix has three allowed-side nonzeros; every foil has three allowed-side nonzeros and exactly one forbidden-side witness. Two versus three qualifying objects are unordered variants of this fixed thirty-position recognition workload. This increases bookkeeping over the observed moderate three-matrix selection, while keeping the same definition and prerequisites. Hard is never reported as a recovered source difficulty.
