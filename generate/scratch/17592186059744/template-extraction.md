# Vector transpose templates

The assessed method is to interchange the row and column positions of a single supplied vector without changing its entries. The requested object is always the complete transpose, either selected as a matrix or entered as indexed scalar fragments. No matrix arithmetic, entry simplification, additional matrix, or transpose identities are introduced. The matrix letter is retained from each source; changing it cannot establish novelty.

The per-source inventory in `source-specs.json` describes concrete orientation, entry count and forms, prompt structure, difficulty, field keys, bank profile, and plot requirements. `source.json` retains the full source-specific descriptions; `source-choice-mapping.json` maps every original choice to an exact complete matrix or scalar and its generating recipe.

Shared slots are the ordered entries of the supplied vector. Easy samples use integers from -20 through 20, including zero and negative values. This is a documented narrower policy than sources such as q-70063 with entry 100. Moderate samples retain each original variable and additive/monomial structure, varying the nonzero absolute coefficients from 1 through 6 while preserving term signs. This conservative same-method extension goes beyond some observed unit coefficients; it adds no computation to transposition. Original coefficients and values are always available for exact replay. Repeated source values, zero entries and source parameters outside normal bounds remain replayable. All algebraic entries are formal real expressions. Reciprocal-bank samplers exclude zero entries so all generated options are defined as formal rational expressions. No assumptions about a learner-selected answer alter the fixed worked solution.

Keep the supplied orientation, original entry count for the selected source layout, response type, field count, table, matrix letter, prompt wording, and ordered solution stages fixed. These define the question contract, not novelty. Changing row to column uses its own source-backed template. Blank field `field-i` always denotes entry i of the transposed result; supplied entries, table targets, correct fragments and displayed solution are parameterized together. Radio retains five choices, without new learner-facing feedback.

The solution first says to interchange rows and columns, then (for radio sources) describes the single row becoming a column or conversely, then prints the transposed matrix. Blank sources preserve their shorter introduction and displayed result. Source q-1048 has no solution; its independently inferred replay solution is evidence-only.

Complete radio bank recipes are implemented by `recipes(profile, entries, orientation)`. Let v be the ordered input entries, rev the reversed list, neg the negated list, O the input orientation, and T the opposite orientation. The complete profiles, including correct option, are:

| Profile / source | Ordered recipes |
|---|---|
| row-sign-reverse / q-1045 | T(v), T(rev), O(rev), T(neg), O([-v4,-v3,v2,v1]) |
| column-swap / q-11468 | T(v), T([v1,v4,v3,v2]), O(rev), O(v), T(rev) |
| column-sign-reverse / q-126136 | T(v), O(-rev), T(rev), T(neg), O(rev) |
| column-negate / q-126137 | O(neg), T(neg), O(rev), T(rev), T(v) |
| column-reciprocal-reverse / q-70063 | O(rev), O(1/rev), T(v), T(rev), O(-rev) |
| column-reciprocal / q-70070 | O(rev), O(1/v), T(rev), O(neg), T(v) |
| unrated-reshape / q-1048 (evidence only) | 2x2 row-major(v), T(neg), O(rev), T(v), T(rev) |

The q-11468 permutation is an explicit observed-pattern mapping: repeated source 3s do not identify a unique misconception. Its mathematical list recipe is retained without claiming a psychological interpretation. Complete profiles are selected with their source-backed template; they are never mixed. Reject an instance if options coincide or any distractor equals the transpose. New question identity hashes the supplied vector, orientation and KP, ignoring seed, bank, matrix letter, and choice order. Pool deduplication also excludes canonical/source tasks and alternate response formats for the same task.

Validation parses the rendered givens and solution and checks every transpose entry by its original row/column indices, then checks the complete option matrices, blank target keys, replay, and live grader. Coefficient coverage is recorded for every entry, and a changed first algebraic entry with the second held constant checks for stale prompt/solution/keys. Side-by-side original, replay and sampled examples are in `review.md`. The fixed index roles are intentional: the complete transpose is requested, so every input entry is assessed rather than sampling a different target.
