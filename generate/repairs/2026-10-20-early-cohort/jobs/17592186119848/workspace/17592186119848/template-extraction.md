# Rank inspection extraction

The complete per-question description and every source option are in
`source-components.json`; original wording, matrices, keys, answers and solution
stages are retained in `source.json`. `source-replay.json` records full bank fidelity.

Backbone: ask which supplied matrices have a specified rank; first require at least
that many rows and columns; disregard dimension-ineligible matrices; count independent
pivots among the remaining matrices; state their ranks and select the qualifying labels.
No matrix arithmetic or row-reduction work is added to learner prompts. The matrices
are triangular/echelon or visibly triangular after ignoring zero rows. Shapes, target
rank, dimension-excluded matrices, field keys and response types are fixed per profile.
They define the source's workload and dimension-exclusion stage, not cosmetic labels.

Observed components: exact signed integer entries and zero rows/columns, given rank,
ordered dimension reasons, concrete pivot-count comparisons, five whole-matrix math
choices or five literal subset choices, or three field-owned Boolean banks. Mathematical
objects are matrices in this task, so complete source-bank replay compares all entries
and dimensions exactly; every source distractor is reproduced, including dimension-
ineligible matrices. No profiles are pooled. Distractor intent beyond these observed
rank/dimension conditions is not inferred.

Authored conservative slot: which dimension-eligible matrices have the requested rank.
`slot-coverage.json` enumerates every allowed subset per complete bank. Five-option
matrix radio profiles require exactly one; subset radio profiles allow only subsets
present in their observed complete bank; checkbox profiles allow their observed match
and the empty subset. Checkboxes retain three explicit true/false fields. Empty-set
variants exercise the same inspection skill, and no new response representation.

For each eligible matrix, preserve its shape and unchanged entries whenever its rank
already has the needed status. To lower rank, retain the first independent rows up to
the desired rank and zero the other rows. To increase rank, fill existing zero rows
with a standard basis row at the diagonal position when independent. All allowed
instances have been exhaustively checked: these changes retain a visible triangular
pivot pattern. The resulting rank is recomputed exactly. A former match loses one
pivot; a newly selected matrix gains only the necessary independent diagonal pivots.
Dimension-excluded objects never change. Each profile's actual operation sequence is
recorded by its original matrices, resulting ranks and explicit requested subset.

Variant solution template retains the source opening dimension explanations verbatim,
then renders each eligible matrix's concrete pivot count and rank, and the selected
subset. Original-parameter solution replay is exact after math normalization and the
spelling correction `coumns` -> `columns` in q-34824. That original is unchanged in EDB.

Choice recipes: whole-matrix options use the corresponding labeled source matrix with
the declared pivot edits; source subset literals remain fixed; Boolean values remain
exactly true and false. Correct designations are derived from displayed ranks, never
copied from source answer identities. Each new answer UUID belongs to its field.
Original parameters are each source's observed matching subset. Complete source replay
covers all 14 field banks and all source choices, with no missing/extra values.

Sampling is a finite catalog, not arbitrary random coefficients. Rank/pivot structure,
dimensions and target define mathematical novelty; scalar changes, relabeling, seeds
and order do not. `batch` refuses oversized requests. This bounded generator currently
has 23 distinct tasks, 13 beyond the sources. New variants are
served only when a fresh live count establishes an easy shortage.
