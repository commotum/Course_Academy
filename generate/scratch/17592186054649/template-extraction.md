# Extracted templates

All IDs and complete original components are retained in `source.json` and `reference/initial/kp.edn`; every source answer has a field-owned mapping in `source-choice-mapping.json`. Source inputs are replayable with `original(template)`.

## Original instances

- q-108: inline question asking the difference of signed 2×3 integer matrices A=[7,-4,9;1,10,-7], B=[-8,6,-2;-4,3,-6]. Five matrix choices, no source key/solution/rating. Difference [15,-10,11;5,7,-1] is the unique correct choice.
- q-11478: named P-Q on a second line, two positive 2×2 matrices P=[4,3;1,2], Q=[1,2;3,4]. Five choices, absent key/solution/rating. Difference [3,1;-2,-2] is uniquely correct.
- q-11441: display A-B, positive/zero 2×2 matrices A=[5,5;5,4], B=[3,2;1,0]. Source key [2,3;4,4], five choices. Explanation: corresponding-entry rule, copy subtraction, expand four differences, simplify.
- q-319618: named C-D, signed 2×3 matrices [-4,12,-1;6,-7,3] and [-9,5,2;-8,-1,10]. Six entry blanks, row-major keys; source answer [5,7,-3;14,-6,-7]. Same three-stage explanation.
- q-319622: named G-H, signed 3×2 matrices [7,7;-6,2;5,-8] and [10,-5;-6,-9;3,-1]. Six entry blanks, including zero answer: [-3,12;0,11;2,-7]. Same explanation.
- q-319625: named P-Q, signed 3×3 matrices [-6,4,9;7,-2,5;10,0,-3] and [1,-8,6;-4,3,-7;12,-5,9]. Six blanks at zero-based row-major cells [0,1,4,5,6,8]; supplied cells 2,3,7 are [3,11,5]. Source answer [-7,12,3;11,-5,12;-2,5,-12]. Three-stage explanation, with literal spacing retained on source replay.
- q-69603: inline 2×3 subtraction equality, A=[4,-8,1;-2,6,-9], B=[-2,1,-10;-1,8,-4]. Five matrix choices, source key [6,-9,11;-1,-2,-5]. Its explanation begins directly with expanded differences (two stages).

## Backbone and slots

Each template asks for one entrywise difference of equal-sized integer matrices. Fixed components: subtraction operation, source dimensions, source prompt structure/names, source response type/count, and corresponding-entry explanation and ordered stages. Keeping dimensions and number of response fields fixes workload; arbitrary dimensions or new operators are outside scope. Matrix names are fixed cosmetic labels, not counted as variation.

Variable components: every A/B entry and every dependent prompt, arithmetic expansion, result, and choice value. Exact integers, no domain branches. Policy: signed source families sample [-12,12]; positive q-11441 uses [0,9]. Source values are retained separately for replay. q-11478 positive source is conservatively generalized to small signed integers because rated easy signed subtraction supplies that same method; no new operation or stage is added. Blanks preserve scalar integer answer shapes and field keys, without distractors or feedback.

For the partial 3×3 blank template, any six distinct result cells can play the requested-entry role, with three complementary entries supplied; keys are assigned in row-major order. This preserves six ordinary entrywise subtractions and the original field layout/workload. The chosen cells, prefilled values, answer keys, and worked result derive from one instance. Source positions are retained for replay. A fixed-matrices/different-targets check independently reads rendered table cells and keys. All nine eligible positions occur in validation samples.

## Complete radio profiles

Let a,b be flattened operands, c=a-b. `replace(c,i,v)` changes only cell i. These lists preserve source order for replay; order is not identity variation. Every option is mapped and reproduced exactly at original inputs; some cognitive interpretations remain unresolved, so no error explanation is added to learner presentation.

- q-108: replace(c,0,a0+b0); c; replace(c,2,a2+b2); replace(c,1,-(a1+b1)); replace(c,3,a3+b3). The fourth is a sign-plus-addition compound pattern, not simple addition.
- q-11478: [a0-a3,a0-a3,c2,c3]; [c2,c3,c1,c0]; c; [c2,c3,c0,c1]; [c0,c1,-c2,-c3]. First observed repeated-value pattern has an unresolved cognitive explanation; the other banks preserve row/column permutations and sign patterns.
- q-11441: replace(c,3,-c3); [a0,a0,a0,a0]; replace(c,1,c0); [c3,c3,c3,c3]; c. Repeated-cell patterns are observed expressions, not a claim about learner mistakes.
- q-69603: [a0+b0,a1+b1,a2+b2,c3,a4+b4,a5+b5]; [c3,c4,c5,c0,c1,c2]; c; [c0,-(a1+b1),c2,c3,a4+b4,b5]; [c0,c2,c1,c3,c5,c4]. The first and fourth are compound mixed-cell patterns with unresolved cognitive interpretation.

Choose the complete source profile with the template; never pool recipes. Reject and resample if options coincide or if a wrong option equals the correct matrix. Preserve five choices and one correct field-owned answer. Values are delimiter-free LaTeX matrices. Source-bank fidelity is reported separately from independent correctness and native grading.

## Identity and validation

New UUIDs derive from the KP UUID, frozen generator version, template, parameters, and complete bank. Seeds are metadata only; the same parameters produce the same identities and content. Deduplication uses operand matrices across all templates, disregarding seed, identity, choices, names, and partial-entry target variations. This is deliberately conservative: changing which entries are requested on identical operands does not add inventory.

Independent checks parse all rendered matrix entries and arithmetic expansions with SymPy, parse partial-entry tables, test source replay, boundaries/zero/equal operands, all profiles and declared cell slots, and the actual application's `learning::grade_field`. Source solution padding is cosmetic; numeric fidelity is exact for all generated variants. `review.md` pairs originals and variants for each template.
