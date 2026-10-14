# Template extraction

The full source-specific prompts, choices, answer UUIDs, and solution strings are
in `source.json`; `choice-mapping.json` maps every moderate option explicitly.

The moderate backbone supplies a signed integer 3×3 matrix, requests the matrix
following one elementary row addition, and presents exactly five full-matrix
radio choices under `selection`. The solution explains the operation, displays
the initial matrix, displays each target-cell calculation, and displays the
result. Only the target row changes. All three target entries must be computed.
Both observed instances cancel the target's first entry to zero; this property
is retained. No additional operation, field type, or solution stage is introduced.

q-10248: M=[[-1,2,4],[8,3,1],[3,-1,9]], source row 1, target row 3, k=3.
q-20239: X=[[1,2,1],[3,-1,1],[2,3,2]], source row 1, target row 2, k=-3.

Variable slots: integer entries in [-9,9], ordered distinct source and target rows
(all six pairs), multiplier magnitude 2..5, unchanged remaining row. For q-10248,
k is positive and the source first entry is -1; for q-20239, k is negative and
the source first entry is 1. Set target first entry to -k times source first entry.
Observed parameters above remain exactly replayable. Expanded entry bounds and
other eligible row roles are conservative same-method generalizations, not extra
source evidence. Matrix symbols M/X follow their respective source profiles.

Keep the dimension, first-column cancellation, three-entry workload, one operation,
five choices, field key, and solution stages fixed for mathematical/contract reasons.
No geometric assets are needed. The canonical example's raster asset contains
only a typeset matrix; its pixels were inspected and are not a new-plot requirement.

Complete q-10248 profile: correct addition; unchanged matrix; exchange source and
target rows; put the negated original target into the source and original source
into the target; update only the target's first cell, retaining its other cells.

Complete q-20239 profile: correct addition; exchange source and target rows after
correct addition; replace unused row by [-source[0],k,-source[2]]; put that altered
row into source, original source into target, and original target into unused;
perform C2:=C2+k C1 across all rows. The altered-row expression is an observed
pattern with underdetermined cognitive intent; do not label it a learner misconception.
The middle value is parameterized as k, not copied as the literal -3. Full original
values must replay, and collisions or extra correct options reject the whole bank.

For all other source families the original components remain in source.json.
Easy swaps supply a matrix, interchange two rows, and display initial/final matrices.
Scaling supplies a reciprocal factor and displays component multiplication then
result. Hard two-target variants display two row additions with an unchanged
common source; same-target variants apply two additions in order to that target.
Their complete source banks and solution stages are retained but not generalized
into normal samplers in this moderate replenishment job.
