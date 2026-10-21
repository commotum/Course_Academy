# Leading-entry sums: instructional account

The learner reads the named rows, scans each from left to right for its first
nonzero entry, adds those signed integers, and selects the matching numeric radio
answer. Tutorial 3148 (`24451a80-db9f-5a0f-a591-41500a69774c`) defines the leading
entry as the first nonzero entry from the left and explicitly says a zero row has
none. Prerequisite examples e-4371/e-4372 establish row/column indexing. Canonical
e-6166 (`7fd5c01f-c20e-5c47-b8d9-8cfbe634c14d`) demonstrates identifying three
entries, stating them in row order, and adding them. Row-echelon classification
from the surrounding lesson is not assessed here.

The captured practice evidence consists of 15 questions and complete five-choice
numeric banks. They form two prompt templates: sums of two or three rows. Each
source bank remains a separate profile, derived from every captured question
rather than a manually selected list. The source-case fixture records all IDs,
prompts, banks, keys and available solutions for independent replay comparison.
q-42362 and q-42363 lack original solutions, keys and difficulty labels; their
keys and solutions are reconstructed using the lesson definition, and replay
metadata identifies those missing fields. No mathematical source errors were
found. All available original difficulty labels are preserved during replay.

The latest finding concerns q-129207
(`0d70558d-9878-55b8-b37b-3292e69959ea`): rows 2, 3 and 4 contribute 7, 3 and -7,
giving 3. Its entire bank is {3, 12, 9, -3, 1}; its worked solution explicitly
states `7+3+(-7)=3`. The bundled snapshot was basis 4110 and omitted this question;
the supplied capture is basis 5355. The other 14 question records are unchanged.
The repair refreshes the complete bundled KP snapshot, basis and source hash;
the existing profile-construction loop then covers the new bank automatically.
No separate hard-coded exception or substitute bank is needed.

Answer-bearing roles are the selected row subset, the first nonzero column in
each selected row, its signed value, and the resulting sum. Before incidental
entries are sampled, normal generation selects a profile, an eligible bank anchor,
two or three target rows, and leading columns. Values are then sampled subject
to bank compatibility. Every two-row or three-row subset and every leading
column is eligible. Leading values can be positive or negative; sums can also
be zero. Changes to target rows, earlier nonzero evidence, or leading values
must change all dependent prompt/solution/key content. Changes to trailing
entries or unselected rows must preserve the answer.

Fixed features have workload or response reasons: a 4-by-4 matrix keeps scanning
short and matches all practice evidence; two or three selected rows retain the
observed amount of addition; bounded integers [-9,9] retain elementary signed
arithmetic; nonzero rows ensure the requested operation is defined; five distinct
numeric options preserve the source response contract. The letter A merely names
the single supplied matrix and carries no answer role. Any leading column is
allowed because the lesson definition depends on the first nonzero entry, not
the diagonal. Zero rows, fractions, larger matrices, and other operations are
outside this conservative implementation, without claiming they are invalid math.

Changing row subsets and leading columns is a conservative same-method extension
beyond individual source arrangements. Trailing entries and unselected rows may
vary without changing the calculation. Banks retain complete observed numeric
gap patterns by translation; the correct anchor can occupy any of the five ranks,
and display order is shuffled independently. Cognitive interpretations of source
distractors are unresolved, so no invented error explanation is shown. Bank values
stay within the possible sum range so range alone cannot discard choices.

Only easy is supported. Moderate and hard would require evidence for a different
workload and remain unsupported. No diagrams are generated. The surrounding
lesson's gray staircase image illustrates row-echelon form, not this question's
sum; matrices here are mathematical notation rather than plots.

Affected checks: replay all 15 complete banks with original parameters, prompts,
available solutions and labels; independently compute the sum from visible
records; exercise the new profile's anchors, row subsets, leading columns and
signed cases; test changed targets with other matrix data held fixed and irrelevant
changes with responses preserved; check all choices using the native grader;
compare shortcut probes before and after shared delivery filtering; render the
repaired profile and controlled examples in the real learning UI. Previously
passing behavior is retained and a small sample covers the existing profiles.
No stored generated instance is implicated merely by a missing source profile;
the captured inventory is separately audited with its provenance limits.
