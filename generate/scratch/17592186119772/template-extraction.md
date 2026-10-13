# Four-stage extraction

## 1. Specific observed questions

`source.json` holds exact original strings; `source-choice-mapping.json` maps each original option one-to-one, including the duplicate legacy bank. All matrix entries are integers from −7 through 11 (the actual broad signed display domain used here is −11 through 11), square sizes 2, 3 and one 4. Zeros on the diagonal are common and do not exclude triangular membership.

| Source | Level | Requested side | True subset | Ordered dimensions A/B/C/D/E | Worked solution |
|---|---|---|---|---|---|
| q-68740 | easy | upper | C | 2/3/3/2/3 | correct C repeated, then complete A/B/D/E repeated |
| q-126352 | easy | upper | D | 2/3/2/3/3 | correct D repeated, then complete A/B/C/E repeated |
| q-126354 | easy | upper | E | 2/2/2/2/2 | correct E repeated, then complete A/B/C/D repeated |
| q-13760 | easy | upper | A | 3/3/3/2/2 | correct A repeated, then complete B/C/D/E repeated |
| q-126353 | easy | upper | A | 2/2/3/2/3 | correct A repeated, then complete B/C/D/E repeated |
| q-74316 | easy | lower | B | 3/3/2/2/3 | correct B repeated, then complete A/C/D/E repeated |
| q-42090 | moderate | upper | A | 4/3/3 | A has zero entries below diagonal; B witness b31=5, C witness c32=3 |
| q-126351 | moderate | lower | A,B | 2/2/2 | both have zeros above diagonal, C witness c12=−2 |

q-42090 has two source fields. Every other question has one. All fields are radio, each has five choices; easy choices are math values containing the entire labeled array, moderate choices are text containing complete subsets. Moderate q-42090's complete bank is A only, B only, C only, A and B only, B and C only (repeated in legacy field). q-126351's complete bank is retained verbatim in mapping/source evidence; it is not replaced by q-42090's bank.

## 2. Shared mathematical pattern

An upper triangular square matrix has zeros at every position i>j; a lower triangular matrix has zeros at every position i<j. Recognize objects satisfying the requested definition, either as a single full-matrix answer or as a complete labeled subset. A diagonal, identity, or zero matrix satisfies both definitions. A foil is defined by at least one actual forbidden-side nonzero, independent of diagonal values and signs.

## 3. Components and complete bank recipes

`recipe(source_id)` extracts full matrices, a prompt mask, a worked-solution mask, the exact original subset bank, and preferred observed witness coordinates. Only complete matrix blocks and complete witness equalities are replaced. No short expression substitution or fitted scalar distractor rule is used.

Each easy option is a parameterized whole square matrix M_label; the source profile fixes its dimension and its counts of nonzeros in each triangle. These are method-relevant wrong objects: each source foil has a forbidden-side nonzero, while the correct object has none. Nonzero support relocation within each side is an authored extension; the exact observed supports and values are supplied for source replay. This does not claim to recover MA's original generation code. The correct matrix and all four *actual* foil matrices are independently filled into their repeated solution locations.

Each moderate option is the exact observed subset of the three parameterized matrix labels. Entire subset profiles are selected before matrix parameters. The original qualifying labels stay fixed for that profile. Matrix support counts preserve this eligibility. A source witness is used if still forbidden and nonzero; otherwise the first real forbidden-side nonzero supplies its actual row, column, and value. Original replay therefore recovers both source witnesses verbatim, while changed parameters cannot retain a stale value/index.

Hard has two separately labeled authored complete profiles. `hard_two` answers AB and supplies A, B, ABC, AC as foils. `hard_three` answers ABC and supplies AB, BC, ABCD, ACE as foils. These whole subset errors omit qualifying matrices and/or include a matrix whose forbidden nonzero was overlooked. They are tied to the printed recognition method, not arbitrary extra objects or number perturbations. Hard source-style shared prose and witness rows match the moderate reasoning structure.

## 4. Reusable masks, constraints and identity

Fixed: radio layout, five choices per field, complete arrays or complete text subsets, original sentence/stage sequences. Variable: requested criterion, full matrix entries, allowed/forbidden support coordinates, and all printed witnesses. Conditional: above/below and upper/lower wording; singular/plural correct-set source masks; raw duplicate field retention. Parameters contain exactly `criterion` and `matrices`.

Normal easy has five matrices, each 2×2 or 3×3, with exactly one qualifying choice. Source profiles enforce the original per-label dimension and two support counts. Normal moderate has three matrices, source-profile dimensions 2/3/4, one or two qualifying objects and the original complete subset profile. Hard has exactly five 4×4 matrices; A is diagonal; other qualifying matrices have exactly three allowed-side nonzeros; every foil has exactly three allowed-side and one forbidden-side nonzero. Profiles enforce AB or ABC membership before building options. All explicit and sampled entries are Python integers in [−11,11]. Reject the whole instance for duplicate matrices, incorrect shapes, disallowed counts, missing qualifying options or duplicate/equivalent subset choices. Defaults resample whole numerical instances after choosing their profile; explicit invalid inputs raise.

The finite sampler catalog uses 256 deterministic candidate supports for each observed profile and 384 for each hard profile, deduplicating complete mathematical tasks. Diagonal representative values distinguish displayed arrays during construction but never enter the task fingerprint. The catalog is the enumerated default sampling domain; the broader bounded explicit domain is not claimed as a counted task catalog. Runtime values vary diagonal entries and nonzero magnitudes/signs for presentation only.

Task identity is canonical over every matrix-label permutation and choice-order permutation. It includes difficulty, requested criterion, dimensions, offdiagonal zero support, the complete compared subset incidence and actual witness-coordinate demands where the source method supplies them. It ignores diagonal entries, nonzero magnitudes/signs and labels. Content identity separately includes version, difficulty, exact prompt, exact fixed solution, full choice banks and field layout/key/correct presence. Seed or a profile alias cannot create new content identity. Different printed banks do create different content identity.

Raw replay uses public `generate(level, profile='raw:q-N', parameters=...)` and the same parameterized masks, matrix rendering, solution witness generation and owned-answer construction as normal output. It preserves attribute presence, field layout, five options in both legacy fields, and absence of the first q-42090 correct ref. No literal-source-return branch or answer lookup table is used. Raw records are marked evidence-only/ineligible. Normal q-42090 has the single authoritative keyed radio field. Source correction and key-presence fidelity have separate denominators in validation.json.
