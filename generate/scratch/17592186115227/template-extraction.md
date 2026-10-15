# Extraction

The immutable specific descriptions, original matrix entries, field contracts,
all correct values, complete original choices, and source solution wording are
in source.json and source-components.json. Every original choice is retained
with its owning field and source profile. Radio distractor interpretations remain
unresolved; those profiles are excluded from generative support rather than
replaced with arbitrary offsets or invented misconceptions.

The blank backbone is “Calculate ABC”: choose the grouping with fewer intermediate
entries, compute that two-matrix product, then multiply it by the remaining
matrix. All entries of the resulting matrix are requested in source row-major
order, with source field keys and Markdown/HTML table layouts. Dimensions are
fixed because they determine grouping, output shape, workload and field count.
There is no independently selected cell: the target is the whole matrix.

Source dimensions and grouping:

| Source | A; B; C | First product | Requested entries |
|---|---|---|---|
| q-320021 | 1×2; 2×1; 1×3 | AB, scalar | 3, row |
| q-320026 | 1×2; 2×2; 2×2 | AB, 1×2 | 2, row |
| q-275521 | 2×3; 3×1; 1×2 | AB, 2×1 | 4, 2×2 |
| q-319938 | 3×1; 1×2; 2×1 | BC, scalar | 3, column |
| q-319943 | 3×1; 1×2; 2×1 | BC, scalar, expanded sum | 3, column |
| q-320017 | 3×2; 2×3; 3×1 | BC, 2×1 | 3, column |

Each entry of A, B and C is a numerical variable slot. The conservative
same-method generalization allows integers -7..7, normally sampled -6..6.
Observed values remain available for replay. Signs and zero are included.
q-320017 keeps B's third column and C's third entry zero, a narrower sampling
policy retaining its observed workload; all other entries vary independently.
No dimensions, operators, output layouts, or grouping decisions vary. There is
no restriction on invertibility: these are compatible products, not inverses.
All arithmetic is exact over the integers; there are no branches or denominators.

Correct answers come from ABC, independently checked as both (AB)C and A(BC).
Solutions retain the exact source sentence and formatting skeleton and replace
every matrix occurrence by its sampled role (A, B, C, intermediate, final).
q-320021 keeps its dot-product expansion and signed-sum stages; q-319943 keeps
its signed-sum stage. Source replay must reproduce each complete prompt,
solution and blank bank exactly. Blanks have one canonical field-owned integer
answer, no distractors or invented feedback.

Mathematical identity is the ordered triple of exact input matrices. Seed,
field-layout choice, solution expansion, difficulty and UUID do not distinguish
an otherwise identical triple. Source/canonical input triples are excluded
before selecting fresh questions. Every selected triple must also have a
previously unused final result, a conservative additional deduplication check.
