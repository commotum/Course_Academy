# Template extraction

## 1. Specific source descriptions

`source-components.json` records **every entry at its ordered row/column position**, all target dimensions, labels, source choice values, positional subset recipes, and recorded correctness. `source.json` retains complete original prompt/field/answer/solution records. No choice is omitted or guessed.

The table in `classification.md` maps every source to template, dimensions, and correct subset. q-69514/q-125552 contrast a 2×2 square with a column and row vector; q-69515/q-69523 contrast a requested 3×4/4×3 rectangle with its transposed shape and a third rectangle/square; q-125550 contrasts 3×2 against 2×3 and 3×3; q-69518 contrasts 3×2 against 2×2 and 2×3; q-69517 contrasts 3×1 against 3×3 and 1×3; q-125549 contains two distinct 2×2 arrays and one 4×2 foil. Matrices with identical dimensions can have different entries and must both be included in the correct subset.

Entries include 0, signed integers (including 12), signed decimal −0.1, and square roots of 2 or 3. Their values must be reproduced faithfully, but their signs/types do not affect row/column counting. All prompts show three arrays in a fixed label order; array row separators and column separators determine the target relation. All eight banks have exactly five text choices, three singletons and two pairs. Canonical matrices are not answer-bank choices; the bank names subsets of the displayed arrays.

For six solutions, the stage order is three bullets in displayed array order, each stating row count, column count, resulting ordered dimensions, then a correct/incorrect mark. A final sentence names exactly the matching subset and target dimensions. Singular/plural varies with counts; the one-match conclusion says “is a … matrix,” and the two-match conclusion says “are … matrices.” Complete prose is replayed byte-for-byte at the original parameters for those six solutions.

## 2. Generalized shared pattern

Given an ordered requested shape `(rows, columns)` and three labeled rectangular arrays, count each array's rows and columns, compute the matching label subset, and choose that exact subset from a text-radio bank. No arithmetic on entries is required. The same fixed solution counts all three arrays independently of the learner's chosen option.

## 3. Components and complete banks

Parameters are `target:[r,c]`, three distinct uppercase `labels`, and three complete `matrices` of exact entry strings. The entire array is a mathematical component; rendering derives separators from nested rows, never replaces a short expression across prose. All original values are explicitly parameterized, including entry positions; replay does not return the literal source payload or consult a correct-answer lookup.

The bank recipes are positional subsets, not alleged mathematical mistakes. Example `q-125550`: `(0,2),(2),(1,2),(1),(0)` renders E and G only; G only; F and G only; F only; E only. Every profile in the generator maps all five original answers this way, and the independently parsed arrays determine which subset is actually correct. There is no defensible need to infer a cognitive error behind “E and G”; the recipe is its exact response-set meaning. `source-components.json` contains all 40 option mappings, including 32 incorrect ones.

The three whole structures are all singletons plus pairs 01/02 (omit12), 01/12 (omit02), or 02/12 (omit01). Default profiles are named by their omitted pair and selected as complete eligible banks. A bank must contain the calculated correct subset. No pooled distractor selection, numerical perturbation, or option replacement occurs. Five unique valid subsets must remain distinct and exactly one must equal the full matching set. Bank/profile/order is not a mathematical task dimension; displayed bank changes are content changes.

## 4. Reusable templates and calculations

Fixed structure: dimension question, three arrays, one radio field keyed `selection`, five text options, three counting bullets, final conclusion. Variable components: target shape, full array entries/shape, labels, singleton/pair subsets, exact singular/plural counts, correct marks. Conditional components: inline bmatrix/legacy target notation versus aligned display; one-match versus two-match conclusion. Source legacy prompts preserve `\cdot` exactly; authored peer prompts use curriculum-standard `\times`.

Calculation: for each rectangular array, dimensions are `(len(rows),len(first_row))`; compare ordered tuples to target; derive exact match indices; validate the whole bank; render one fixed solution. Exact number tokens are parsed with SymPy for mathematical entry fidelity. Arbitrary expressions are rejected because they add no assessed skill. Entry domain: finite signed integers, familiar radicals and simple decimals for random generation; explicit numeric replay permits all source integer values. Dimension, match-count and level constraints apply to explicit inputs too. Invalid explicit parameters raise errors without resampling.

Easy/moderate/hard bounds and their curriculum rationale are in `classification.md` and separately documented in the script's level sections. Source observed profiles are validated at changed parameters using the same normal API and original profile; source replay retains exact notation, bank, and full observed solution. Normal peer templates preserve the shared aligned structure and counting prose. Each named source bank has two displayed changed-parameter examples in `review.md`/`review.json`, and each level has at least two authored examples.

## Source anomalies and supported repairs

- **q-69514:** original field has no correct ref, difficulty or solution. The actual displayed B/C/D arrays have dimensions 2×2/2×1/1×2. The requested 1×2 therefore selects **D only**, already an existing bank option. Derive its ref and provide a common counting explanation; label moderate assignment and explanation as authored. The authoritative lesson widget independently confirms all three complete arrays and five text-radio choices, but supplies no correct designation or solution. No absent designation is counted as matched.
- **q-69515:** same missing fields; P/Q/R have dimensions 2×2/4×3/3×4, so the requested 3×4 selects **R only**, already present. Same separately reported derivation/authorship. Authoritative layout confirms full content, not an unseen key.
- **e-5017 canonical example:** captured prompt contains one unnamed 2×3 matrix although the explanation discusses A/B/C. The authoritative local lesson snapshot has the same missing B/C arrays. Preserve the raw canonical evidence; do not reconstruct unobserved entries. Its ordered-dimension explanation anchors scope, but it is not included in practice-bank fidelity denominators.

No observed mathematical errors, malformed array TeX or ambiguous banks were found. Legacy `\cdot` is unconventional dimension notation but is confirmed as multiplication-style dimension notation by the source's actual `×` widget, so it stays exact in explicit replay. Peer defaults use `\times`. Raw evidence and derived repairs are separated in `source-cases.json` and `validation.json`. All 8 original prompts and banks, all 6 extant solutions, and all 6 recorded correct designations have exact fidelity; 2 absent solutions/refs are reported as additions, not matches.
