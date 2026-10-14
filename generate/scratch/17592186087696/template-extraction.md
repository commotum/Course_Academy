# Template and component extraction

The specific original prompts, exact numerical/radical/decimal entries, every choice, and ordered solution sentences are retained in `source.json`; `source-cases.json` maps all five supported questions to their original variable slots and complete bank profile. Entries include signed integers, zeros, decimals (0.2, 0.5, 1.5) and signed square roots (√2, √3). They do not affect whether a matrix is square.

The mathematical backbone is three supplied rectangular matrices, three independent checkbox responses, and three row/column explanations followed by a selected-subset conclusion. The assessed method is dimension comparison, not testing diagonal structure, identity matrices, rank, or entry values. Preserve three targets because this is the observed response contract and workload. Matrix positions have equal instructional roles.

Slots are matrix label, rectangular rows of entries, dimensions, and source layout flags. All prompt references, field keys, solution targets and key values derive from the same parameters. Dimensions may independently range from 1 through 5 in each slot: all these row/column counts occur in the originals. This independent combination policy is a conservative same-method generalization, separate from observed tuples. Entries normally sample integers −5 through 5 for readability; original decimal and radical entries remain available for exact source replay. No arithmetic is performed on the entries. Label and entry changes are cosmetic for diversity purposes.

Prompt backbone:

`Which of the following are square matrices?` followed by three `label=\begin{bmatrix}…\end{bmatrix}` expressions in one display, then `Select all that apply.` The optional no-selection instruction is present in two sources and used for normal variants. Original trailing separators and pluralization are replayed exactly. Normal output uses correct singular grammar. Empty-selection conclusions generalize the existing checkbox contract without adding a reasoning stage.

Worked solution for each matrix follows the source wording: it is a square matrix since the numbers of rows and columns are the same, or it is *not* a square matrix since they are not the same; state both counts and the dimension. Then name only the selected labels, or explain that none is square. The solution is concrete and independent of the learner's submitted choices.

Every supported source field uses profile `boolean-membership`: the text value `true` means select the corresponding matrix and `false` means leave it unselected. Compute the canonical value by `rows == columns`. The other value is the complementary error. For each of 15 fields the original complete two-choice bank is reproduced; all 30 source choices and all 15 canonical designations are accounted for. Choice order does not establish novelty. There is no inferred distractor recipe or extra feedback.

Excluded q-7826 radio bank is retained exactly in `source.json`: A and C only, None, A and B only, B only, A only. Each is a direct subset-selector recipe against the labels A/B/C. Its absent key, difficulty and solution prevent a supported source replay; no authored replacement is served. The malformed canonical example is also excluded. These exclusions do not weaken the exact fidelity requirement for the five supported banks.

Mathematical fingerprints use an unordered multiset of the three dimension pairs. They ignore seed, labels, matrix order, coefficients, rendering flags, identities and choices. The bounded dimension domain has C(25+3−1,3)=2925 shape multisets. Replenishment excludes every existing practice task, including the incomplete source, and never pads a shortage with cosmetic variants. No moderate or hard generator is exposed as supported.
