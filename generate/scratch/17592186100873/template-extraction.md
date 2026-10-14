# Source extraction and executable boundaries

`source-components.json` retains every original record, exact parameter matrices,
queried target, source field, answer ID, complete option value, and profile.
`source-fidelity.json` reports ten complete banks, 34/34 values and 24/24
incorrect values matched one-to-one, with correct designations preserved.

The shared backbone is C=AB with signed integer matrices of compatible dimensions;
the supplied objects are two complete matrices, and the requested object is one
entry of their product. A single integer is selected or entered. The solution
states which row and column to multiply, displays the two full matrices, extracts
that row and column, expands their dot product, evaluates each product and sums.
Two- and three-term workloads and radio/blank layouts remain separate families.
Each source keeps its source notation (explicit multiplication dots or implicit
parentheses). Labels, matrices, number forms, operand order, field key/type/count,
choice count, instructional wording and solution stage order stay source-fixed.

The variable slots row and column independently range over all product cells in
each source matrix pair, subject only to a radio-bank collision rejection. This
is a conservative same-method generalization of the observed target, including
rows/columns other than the original position. It preserves signed integer dot
products of the original length, without adding operations or reasoning stages.
Source matrices are a deliberate narrow sampling policy: entry randomization is
unnecessary to provide distinct target tasks and unsupported error interpretations
would not justify inventing more complex numerical policies. Original parameters
are always retained for exact source replay.

For a target (i,j), compute A*B exactly with SymPy, independently cross-check the
sum of selected scalar products, and derive every target subscript, ordinal,
row/column vector, expansion, signed intermediate sum and answer from that target.
Radio banks retain each observed incorrect integer as a fixed literal recipe;
the interpretation of those mistakes is unresolved. The source does not establish
parameter-dependent error formulas, so none are inferred. The selected profile
is chosen before constructing its complete bank. Its correct value becomes the
computed target entry, and targets equal to a fixed incorrect value are rejected.
Every normal bank is therefore one observed source profile with no pooled recipes,
no invented distractors and five unique values. Blanks retain their one canonical
integer and source equation fragment. Original question/field/answer identities
are never used for authored variants.

The exact bank and source solution are replayed only at the observed target and
marked evidence-only. Mathematical and grading checks independently read the
rendered source replay as well as every normal variant. The replay API cannot be
used to admit a source duplicate into inventory. Normal generation can produce
a source target, but preparation excludes every existing source/canonical
fingerprint and every already generated task before adding content.

Only the ordered selected row and column vectors establish mathematical content
identity. Seed, labels, unused matrix entries, IDs, answer-field type and choice
order do not. Full eligible cell enumeration yields 94 source/profile variants,
90 distinct tasks before excluding the current database. Other difficulty levels
and arbitrary matrices are outside this bounded generator. Unsupported shortages
are explicit in capabilities.json and the job result.
