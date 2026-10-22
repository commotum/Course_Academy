# Rank by inspection

The learner compares the requested rank with row and column counts, excludes
impossible matrices, inspects independent pivots in the remaining matrices, and
selects a matrix or subset. Lesson tutorial 4151 defines rank as the number of
pivot columns, equivalently nonzero rows **in row echelon form**. Canonical
e-5417 excludes B by its three rows before comparing A's three pivots with C's
four. Neighboring e-5418 assesses row reduction, a different operation excluded
from this package. The sparse dependent rows in q-139965 are retained; arbitrary
dense matrices requiring elimination are not introduced.

The supplied snapshot at basis 5415 supports ten complete easy questions. Five
matrix-radio profiles are q-139958, q-34824, q-79559, q-79560 and q-79561. Three
subset-radio profiles are q-139965, q-34823 and q-79562. Two checkbox profiles
are q-35283 and q-79568. Every original choice, correct designation, matrix and
solution was read. q-34807 and q-35270 are also labeled easy but lack keys and
solutions; they remain incomplete evidence rather than invented replays. No
images occur in the supplied material. Default difficulty is easy, justified by
immediate dimension and pivot inspection; moderate and hard lack supporting
source workloads and are unsupported.

The backbone fixes the multiset of shapes, requested rank, number of dimension
exclusions and pivot inspections within each source profile. These preserve
method and workload. Dimension-ineligible matrices cannot qualify because rank
cannot exceed either dimension. Magnitudes and incidental labels have no such
mathematical restriction. Source values and arrangements are observations, not
universal requirements. Five-matrix radio requires exactly one qualifying matrix;
subset-radio requires a subset represented by its complete five-choice bank;
checkboxes use field-owned Boolean banks, with a visible None when none qualify.

Decision-relevant assignments are chosen before rendering. Eligible matrices may
gain or lose independent rows using the existing sparse rank-adjustment rule.
All corresponding matrix entries, answers and solution references derive from
that instance. Whole-matrix radio exercises each eligible singleton; q-34823
exercises the empty subset, either singleton and their pair; q-79562 exercises
either eligible singleton and the pair. Checkbox exercises its sole eligible
candidate qualifying and none qualifying. Rank-deficient cases must remain
visibly sparse, with no additional learner calculation method.

q-139965's original five-choice bank lacks A-only. Freezing its original
dimension arrangement therefore forced B to qualify. Normal practice permits
all six assignments of the same physical matrix roles to A/B/C. A stronger probe
conditions on the dimension-excluded label: reassignment alone still left a
forced member in some arrangements. Normal practice consequently selects a
**complete compatible observed bank**: the original q-139965 bank when B/C are
eligible, otherwise q-79562's same-family bank relabeled to the two eligible
candidates and the excluded candidate. Both eligible singletons and their pair
are then representable in every arrangement. No individual options are pooled.
Both bank profiles are sampled and identified by `choice_profile`. Original
q-139965 parameters and its complete original bank remain exactly replayable.

Source q-35283 supplies an explicit None checkbox. q-79568 has only three
matrix fields: exact source replay preserves those three, while normal practice
adds the same family's source-supported visible None, permitting a deficient
case with a correct selectable response. The supplied matrix-bearing checkbox
keys, rather than the legacy snapshot's A/B/C keys, are rendered with their
current entries. Source replay preserves all 15 complete banks and 54 choices.
The spelling error 'coumns' in q-34824 becomes 'columns'. Subset prompt matrices
use shared wrapping `matrix_operands` containers because the original single
wide display visibly clipped the third matrix. Prose and mathematical objects
are compared separately from this necessary presentation normalization.

Actual inventory filtering initially removed source-identical answer cases,
leaving fixed answers in several newly delivered profiles. Normal practice now
uniformly scales entries by 2 **after** constructing pivots; source replay uses
scale 1, also supported explicitly. Nonzero scaling preserves ranks, dependence,
zero patterns and workload, and requires no learner arithmetic. It does not add
semantic capacity. Both scales are checked for response preservation, with
changed visible matrices requiring distinct question identities. Content hashes
include rendered checkbox keys to prevent identity collisions.

Validation reads visible records using independent exact Fraction elimination,
checks full banks and solution assertions, and sends correct and incorrect
choices to the real native grader. Controlled changes alter qualifying pivots
while dimension-excluded matrices stay fixed; stale solutions and keys must
fail. Coverage and shortcut probes condition on source profile, field count,
excluded labels and bank profile, before and after the actual delivery filter.
The catalog contains 39 presentations but only 24 structural semantic classes;
`batch` chooses one seeded representative per class. Seeds, scalar changes and
pure relabelings never inflate capacity. This finite package can be exhausted
by future inventory or learner history; live history and reservations are not
available for offline verification. No database, image publication or engine
changes are part of this repair.
