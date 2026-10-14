# Template extraction

## Original components

All original prompts, values, layouts, fields, choices, correct references and available solutions are retained exactly in source.json. source-choice-mapping.json maps every original option to its field, original parameters and complete bank recipe index. The numbered recipes below correspond to source order, not shuffled presentation.

- q-103: A=[2,-12;7,-4;-8,7], B=[3,0;-1,5;9,13]. Inline question, 3×2 matrix radio, absent key/solution/rating. Unique sum [5,-12;6,1;1,20].
- q-105: X=[2,-1,8;-14,0,-6], Y=[-12,3,5;13,1,0]. Named inline operands, 2×3 radio, absent key/solution/rating. Unique sum [-10,2,13;-1,1,-6].
- q-125722: P=[1,-1;-4,0;-1,2], Q=[2,-3;1,1;2,-4]. Named display operands, 3×2 radio. Sum [3,-4;-3,1;1,-2]. Three stages: copy operand addition; expand six additions (parenthesize negative first operands); simplify.
- q-319601: P=[-4,9,3;7,-2,11], Q=[10,-5,-8;-1,4,-6]. Six row-major result cells, scalar integer blank fields 1–6. Sum [6,4,-5;6,2,5]. Same three stages; negative first operands unparenthesized.
- q-69622: A=[1,-1,4;3,-2,2], B=[-2,0,-1;1,2,10]. Inline 2×3 sum equality, radio. Sum [-1,-1,3;4,0,12]. Two solution stages: expand additions then simplify.
- q-69635: A=[-1,-3;-6,-3;-2,10], B=[1,-11;0,-14;11,-16]. Inline 3×2 equality, radio. Sum [0,-14;-6,-17;9,-6]. Same two stages, source introductory trailing space preserved.
- q-106: M=[3,-6,14;2,9,-13], N=[-15,-6,-13;-1,-8,14]. Named display 2×3 operands, radio. Sum [-12,-12,1;1,1,1]. Three solution stages.

## Backbone and variable slots

One entrywise sum of two equal-sized non-square signed integer matrices, with six elementary additions, no branches. Preserve each source's dimensions, named versus inline presentation, punctuation, response contract, choice count and solution stages. Matrix dimensions stay fixed per template to retain six operations and source layout. Every operand entry is a variable slot in [-16,16], a conservative small-integer range spanning all observed entries. Source parameters remain separately available via original(template). Zero, positive and negative values are allowed. Correct result c=a+b is computed first, followed by expansion and distractors. All dependent prompt, solution and answer values use the same parameter object.

No eligible target subset exists in the blank template: all six result entries are requested in their ordinary row-major locations. Changing which entry is filled is not an added slot because that would change this full-result contract. Fixed letters are cosmetic; neither letter nor option order creates a new question. No assets or conditional plots.

## Complete choice banks

Let a,b,c be row-major six-vectors, c=a+b. R{i:v} means replace the stated entries of c and leave all others unchanged. Every recipe below produces a complete matrix, including compound mistakes. The cognitive cause of irregular mixed-cell patterns is unresolved; preserve the explicit transformation without inventing learner feedback. Literal residual offsets below are narrow observed error patterns, not claims of a unique inferred error mechanism. Their values are applied to the new computed sum, never copied as entire answer matrices.

- q-103: R{2:a2-b2,5:-c5}; c; R{3:-a3+b3,5:-c5}; R{0:-c0,4:-a4+b4}; R{1:-c1,2:-c2}.
- q-105: R{0:-c0,4:c4+12}; c; R{4:c4+12,5:-c5}; R{1:-c1,4:c4+12}; R{3:-c3,4:c4+12}. The repeated +12 residual is an unresolved observed mixed-cell error, retained explicitly instead of inventing a multiplication or new arithmetic operation.
- q-125722: c; R{0:b0,1:a1}; R{2:a4,5:c2}; R{4:b4-a4,5:b5-a5}; R{2:a3}. Omitted operand, wrong-cell copying, reversed subtraction in final row, and single wrong-cell copying; cognitive interpretation remains uncertain for wrong-cell choices.
- q-69622: c+d for d respectively [-2,-1,-3,-4,-1,-10], [0,8,-6,1,0,-15], [0,0,-3,-11,0,-10], [4,0,-4,8,0,-11], [0,0,0,0,0,0]. These are complete observed residual-vector profiles; no additional cognitive generalization is claimed.
- q-69635: R{3:c3+6,4:-c4,5:-c5}; R{0:a0-b0,2:-c2,5:a5-b5}; c; R{2:c2-10,3:c3+5,4:-c4,5:-c5}; R{2:-c2,3:c3+28,5:-c5}. Offsets 6,-10,5,28 retain unresolved compound source patterns.
- q-106: R{3:-c3}; c; R{1:-c1}; R{5:-a4+b4}; R{1:-c1,4:-c4}.

Choose a template and its entire observed bank, never pooled distractors. Reject if a required distractor equals the answer or another choice; retry at most 1000 times. Preserve all five choices. Blanks have exactly one field-owned canonical scalar answer each, with no distractors or added feedback. All mathematical values are delimiter-free LaTeX.

## Source repair boundaries, identity and validation

New instances of q-103/q-105 receive independently computed keys and corresponding-entry solutions; originals remain incomplete and unrated. Canonical prompt defect is documented, never propagated. All source bank values must replay exactly and correct references must match where present. Fidelity and mathematical validation are separate.

New question UUIDs derive from KP identity, frozen version, template, parameters and complete bank. Fields derive from question UUID and original key; answers derive from field UUID and value. Seed is metadata only. Conservative mathematical deduplication compares the unordered pair of complete operand matrices across templates, ignoring letter names, seed, choice order, and UUIDs. Reversed operand order cannot create inventory. Retain canonical and every original question in this comparison.

Validation independently parses rendered operand matrices, arithmetic expansions and results with SymPy, checks each correct bank value and all six blank keys, tests every profile at 40 seeds, perturbs every scalar operand slot through its full bounded domain with other data fixed, and excludes colliding banks. Native learner grading tests every radio option and accepted equivalent/rejected incorrect integer blanks. review.md pairs each original with a changed-parameter variant. No position-changing check is applicable: there are no variable target slots.
