# Instructional account and repair scope

The learner reads a stated elementary row operation, identifies the affected row
and any donor row or scalar, updates every entry including the constants column,
and selects the resulting whole matrix. For two operations the learner must use
the intermediate rows, not the original rows. The response is one radio selection
from five distinct matrices, with exactly one mathematically correct choice.

Tutorial `7aa753a7-1450-53dd-8e61-71e07952cecb` in source.json defines switching
“any two rows,” multiplication of “each element” by a nonzero scalar, and addition
of a multiple of a different row. It describes assignment as assigning new values
to “every element of a given row.” Prerequisite example
`b5967dd6-bdf9-5cd0-9639-ec2816d04256` explains the augmented constants column;
it must undergo the same operation as the coefficient columns. No diagrams occur.

Observed easy sources are swap `926d4b45-89b4-5d26-9733-b0d97c69c160` and
reciprocal scaling `0f08a2c2-eb16-5d85-a714-beb36e4a0c94`. The canonical example
`2ff0a6f5-f3b2-5b39-8b69-1a0c969548cf` is another swap and has no captured
answer bank. Moderate sources use one row addition, including
`337ae2e1-4641-5c8b-9b2a-9435340f0134` (q-72747). Hard sources
`25230851-35bf-5052-9d49-2045d4671518`,
`56624c75-a028-5dc9-962f-9700b721674f`, and
`4f7e0cb8-b82b-5c57-8695-0b8e08268369` use swap/add or scale/add sequences.
All captured practice fields are five-choice radio fields.

The current package supports easy, moderate, and hard; this job requests easy.
Operation counts stay fixed within each band to preserve workload. Matrix shapes
remain those of these sources: three-row easy matrices, two- or three-row moderate
matrices, and three-row hard matrices. These are conservative sampling bounds,
not claims that other dimensions are mathematically invalid. Five choices and one
key preserve the observed response contract. Nonzero factors and distinct donor
and target rows are required by the elementary-operation definitions. Unaffected
rows stay unchanged because assignment replaces only its named row. The augmented
separator is explicit in all generated matrices, including q-72747 whose source
uses unpartitioned bmatrix notation despite calling the matrix augmented.

Answer-bearing roles are the swapped pair, scaling target and factor, addition
donor/target/coefficient, and the intermediate rows used by a sequence. The
mathematical rule fixes these roles' meanings, not their indices. The existing
random families choose these assignments before entries, then compatible small
signed integer entries. Reciprocal factors use compatible denominators to limit
arithmetic workload. All three pairs, all three easy scaling targets, both scalar
signs, and varied correct-choice positions must survive delivery. Moderate donor
and target may exchange roles; hard donor and recipient may intersect the swap.
Matrix names and display order are incidental. Controlled changes of the target
with entries held fixed must change prompt, key and solution together; renaming
must preserve the mathematical result. No extra row-reduction or system-solving
task is introduced.

The random comparison banks are existing conservative extensions: scale choices
use distinct eligible factors; addition choices use distinct eligible coefficients;
hard choices use competing two-operation sequences. Swap uses its captured
permutation bank relative to the requested pair. Original source banks remain
separate replay profiles. Their unusual distractors must not be replaced by a
different source's bank or generalized without evidence. Exact source-only banks
reject altered mathematical parameters; they may change matrix names or choice
order. Normal sampling retains the previously reviewed families and bounds.

## Concrete omissions to repair

Before runtime edits, `checks/latest_failure.py` reproduced both review failures:
q-10252 matched none of the twelve existing partial-column assignments; q-72747
raised StopIteration. Results are retained in evidence/before-repair.json.
The construction error is treating incomplete source-profile coverage as adequate
replay coverage. The repair adds both complete banks, with an executable coverage
check over every supplied practice question and the canonical example.

Source `afe0707b-0259-50d7-a719-7a8d24334500` (q-10252) supplies a complete bank
for R1 := 2R1 but has no captured difficulty, key or solution. Its independently
inferred key is the fifth choice, [[2,4,6],[3,4,5],[4,6,7]]. The generated solution
interprets scaling, shows the three products, then their values. Easy is inferred
from the single scaling operation; the immutable source capture stays unlabeled.
Its first distractor scales column 1; the second scales only cell (1,1). The third
scales every cell except (1,1). The fourth is preserved as an observed entire
matrix [[1,4,6],[1,12,15],[1,24,28]]: no general error rule is established. This
uncertainty justifies a guarded replay-only bank, not an invented variable recipe.

Source q-72747 adds -3 times row 1 to row 2. Its middle stage is
[[1,-1,2],[3+(-3)(1),-4+(-3)(-1),4+(-3)(2)]], yielding
[[1,-1,2],[0,-1,-2]], the captured third key. Its four distractors are retained
exactly, including compound entry errors whose underlying learner model is
uncertain. The existing parameterized row-addition renderer already supplies the
source's interpretation, expansion, and final-value stages.

Validation will compare complete mathematical banks and correct designation,
independently parse the visible prompts/solutions, grade all five responses for
the changed profiles and representative counterfactuals, and render the two
repaired examples. A small unchanged-family sample checks decision roles and
shortcuts before and after the shared delivery filter. Inventory examination is
read-only; original source records are not reclassified as generated records.
