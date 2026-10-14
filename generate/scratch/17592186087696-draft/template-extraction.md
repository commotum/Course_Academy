# Four-stage extraction

## 1. Specific source descriptions

| Source | Labels/shapes in prompt order | Entries and structure | Presentation/solution |
|---|---|---|---|
| q-11557 | C3×3, D4×4, E2×2 | sparse signed/decimal C, unit-diagonal D, signed radicals E | trailing thin space; three square explanations; all-three conclusion |
| q-11556 | P3×2, S2×2, T5×5 | signed/decimal P, signed S, sparse signed/decimal/radical T | trailing thin space; nonsquare/square/square explanations; S/T only |
| q-126275 | K2×2, L1×2, M4×3 | radical K, single-row L, zero-rich signed M | none instruction; source says “1 rows”; K only |
| q-7835 | K2×3, L2×2, M4×4 | zero-rich signed K/L/M | no none instruction; nonsquare/square/square; L/M only |
| q-126278 | A1×1, B3×3, C1×2 | signed singleton, signed dense B, single-row C | none instruction; singular grammar; A/B only |
| q-7826 | A5×5, B3×2, C1×3 | A all zero, repeated B rows, C all zero | inline comma-separated spaced equals; one radio; no key/difficulty/solution |

Source-cases.json contains every exact original entry, label and presentation flag as parameter values. Those values drive ordinary rendering, never a source-payload return branch.

## 2. Shared generalized pattern

Count each labeled matrix's rows and columns. A square matrix has equal counts, independently of entries. Classify all three supplied matrices, then select their precise set of labels. Checkbox source fields encode each membership independently; the historical radio field encodes a complete subset. The answer criterion is subset equality, not entrywise matrix equality or one valid square option. Multiple square matrices are expected.

## 3. Component/choice mapping

The boolean bank for every checkbox field is exactly `false` and `true`. The correct value is parameterized by `rows == columns`; the wrong choice is its logical complement. It is not a numerical distractor. Every original field maps as follows:

| Source | Field→correct | Both complete bank choices |
|---|---|---|
| q-11557 | C→true, D→true, E→true | false,true for each |
| q-11556 | P→false, S→true, T→true | false,true for each |
| q-126275 | K→true, L→false, M→false | false,true for each |
| q-7835 | K→false, L→true, M→true | false,true for each |
| q-126278 | A→true, B→true, C→false | false,true for each |

The q-7826 historical radio bank is a complete ordered recipe catalog before shuffling: indices(0,2)→`$A$ and $C$ only`; empty→`None`; indices(0,1)→`$A$ and $B$ only`; index1→`$B$ only`; index0→`$A$ only`. Replace labels from the chosen roles. All five are mutually distinct subsets, including every pair of incorrect choices. At the anchor only index0 is correct mathematically; original correct ref is absent. Wrong subsets represent extra/missing membership. The underlying psychological cause is not recoverable, and no invented diagnosis is exposed. Sampling selects this complete five-choice bank before choosing parameters and rejects the whole instance if its correct subset is missing. None of the original bank choices is omitted.

Prompt backbone: “Which of the following are square matrices?”, three labeled matrices, source-specific inline/display layout and selection instruction. Solution backbone: three ordered bullets with verdict, equality/inequality reason, counted rows/columns, dimension statement; then “Therefore” exact selected-label set. Every dependent label/count/grammar/conclusion is regenerated. Source shared prose and full operative sequence reproduce exactly for all five present solutions. The legacy singular/plural anomaly is retained only by an explicit source flag; normal output uses singular grammar.

## 4. Reusable slots and constraints

Fixed: assessed square predicate, three labeled targets, existing field types, Boolean bank or five-subset bank, ordered count-and-compare bullets and one final set conclusion. Variable: three distinct A–Z labels; each rectangular shape within the observed1..5 or authored level ceiling; real signed integer/decimal/radical entries; source layout flags; field-owned deterministic option shuffle. Matrix role is ordinary matrix throughout, never augmented coefficients. All rendering calls shared matrix_tex and normalizes prose before IDs.

Observed checkbox replay allows the full observed1..5 shape domain and retains observed easy labeling. Normal authored easy limits shapes to1..3 and requires at least one single-row target. Authored moderate requires all dimensions2..6, one square, and the two nonsquare matrices are transposes in shape. Authored hard requires common row count n∈2..7, column counts l<n, n, u>n with1≤l,u≤8. Role assignment can occupy any of the three positions. Explicit calls enforce the identical policy as sampling. These policies preserve three targets and no new mathematical stage; difficulty calibration remains uncertain.

Entries/letters/order/seed/profile are excluded from semantic fingerprint; sorted shape multiset retains shape multiplicity and row-versus-column orientation. Displayed prompt, fixed solution, full unordered owned banks and present keys determine content identity (including displayed difficulty). Correct entries or option order alone cannot establish identity. Entry changes can yield new presentation IDs but never claimed task capacity. The finite meaningful checkbox capacities are easy109, moderate50, hard56 unordered shape multisets. These are categorical limits, not unbounded repeated-practice claims. Radio shapes independently range1..5 but require one of the five bank subsets.

No plot extraction/generation is needed: standalone matrices are mathematical notation. Missing q-7826 fields are presentation/schema completion, separate from raw original fidelity. Raw evidence remains public through observed-radio-raw and has no key/solution/difficulty; completed-observed-radio is explicitly authored and eligible. Every normal instance is independent of the learner's selected error.

Authored visual-counting bounds extend the observed5×5 ceiling to6 at moderate and8 at hard (hard rows2..7). These are bounded presentation/counting extensions, not added algebra or new matrix classes. They allow independently varied smaller/larger hard column counts rather than restricting to±1. Bounds and difficulty remain authored calibration claims; the public source replay and historical radio stay within1..5. Semantic capacities exclude label/order/entry aliases.
