# Classification

Snapshot: database `math`, basis1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Frozen source wrapper is source.json. Owning topic17592186050574 is MA462, **Determining Continuity from Graphs**; KP17592186068695 is the first assessed step. Lesson route, followed by first-step/next (not Pull order): Introduction → Continuity at a Point → this KP → Identifying Points of Discontinuity → Determining the Behavior of a Function in the Neighborhood of a Point. Prerequisite: Piecewise Functions (MA165).

|Level|Source practice IDs|Field contract|Templates/banks|Plot rating|
|---|---|---|---|---|
|easy|q-48039, q-48081, q-69782, q-48082|radio selecting a whole graph, five image options|4 distinct graph-bank/solution families|heavy|
|moderate|q-102106, q-78133, q-102115, q-78131, q-78132|radio selecting subset of three specified points; source2 fieldless|5 graph/solution families,3 observed text banks and2 authored complete banks|heavy|
|hard|none|authored five-option radio subset,3 specified points|2 authored scale-reading realizations of jump+hole families|heavy|

q-48081 has two legacy radio fields sharing a five-image bank, with no correct designation on the first. The authoritative MA462 Source/462.json shows one radio widget, five options, one continuous function. Public observed replay preserves both fields and missing-ref presence; normal output uses the second, complete field. q-102106 and q-78133 omit the answer-fields attribute entirely. Observed replay omits it; normal output adds explicitly authored complete5-option banks derived from possible three-point subsets. Their source prose independently establishes I+II and II. No absent designation is counted as an observed matched designation.

The canonical e-3567 reciprocal graph supports detecting an asymptote at the **specified** point. The local-neighborhood lesson explicitly shows a function can have a discontinuity elsewhere and remain continuous at the asked point. None of these tasks asks to find every discontinuity. No formal derivative, L'Hôpital calculation, or algebraic continuity theorem is added.

Hard is an authored design claim: exactly3 local checks on graphs with both a jump and a displaced singleton. At least two targets are half-integers, read against unit-spaced ticks/grid with no target-specific half-integer tick labels. This adds coordinate-scale reading to the same continuity decision; it does not add a fourth local check or introduce a progression. q-78133 has2 midpoint readings and1 labeled integer reading; q-102115 has3 midpoint readings. Both require exactly3 local continuity checks and at least2 unlabelled midpoint coordinate readings, a comparable coordinate-reading workload within this level. Its2 families are unordered variants, not a progression. Easy/moderate use integer queried coordinate ticks. Explicit inputs enforce these separate coordinate bounds and at least2 half-integer targets.


## Current source and commit contract (2026-10-14)

Rechecked `math` at basis 2227 and the same immutable lineage. The nine source
questions remain, but all five moderate questions now have three checkbox fields
with keys I, II, III, each owning text `true` and `false` answers. The migrated
prompts say “Select all that apply” and label all three coordinates. The current
correct sets match the independently transcribed graph predicates. Easy still
uses five-image radio banks. q-48081 still has duplicate selection fields and an
absent correct designation. q-48082 still has the contradictory solution plot.
Both are preserved and excluded from validated inventory. All current source
questions are stored in `current-source.json`; historical source evidence is
retained in `source.json`. `current-replay.json` reports exact complete current
bank, field, prompt and solution replay. Historical observed replay remains exact.

Version continuity-graph-7 uses the current checkbox contract for normal moderate
and hard output. `profile=current` is exact current-source replay at identity
coordinates, while `profile=observed` retains historical bank/omission evidence.
Checkbox answers encode each point's independently computed continuity predicate;
no subset radio distractor bank is mixed into the checkbox layout. All complete
owned-choice combinations are checked through the current application grader.
Hard still has exactly three local checks, both jump and displaced-singleton
features, and at least two half-unit coordinate readings against unit tick grids.

The declared finite catalog remains four easy, five moderate and two hard tasks.
Changes to widget format, answer order, affine coordinates, seed or UUID are not
additional tasks. Every source task consumes its mathematical fingerprint even
if defective or shown. Only unused hard tasks can be committed from this catalog.
Per-band reserves remain short where no unused task exists; these are bounded
capability exceptions for this generator, not claims that the broader skill has
no other possible questions. New validated templates can reopen that boundary.
