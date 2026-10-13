# Template extraction

## 1. Specific evidence

extraction-data.json gives all 19 individual prompts, parameters, field layouts, full source solution masks and every original choice. The integer vertices are not treated as literal payload branches. Each whole coordinate tuple is a prompt slot. q-20016 preserves its original comma-space spelling. q-18581 omits parentheses around the positive single-term origin vector k; changed multi-term or negative origins are parenthesized so subtraction remains well formed. q-316530 writes zero terms in SU and in the cross-product basis row. q-71106 uses positive 12 inside its norm square although the cross component is -12; this exact equivalent sign convention is preserved. Norm masks retain all rows, including individual squared components where present, sum radicands, optional reduction and final norm. Final masks retain whether the numerical half is followed by a separate reduced area equality.

## 2. General mathematical pattern

Given ordered vertices A, B, C, form u=B−A and v=C−A. Expand the 3×3 determinant using the i, −j, +k 2×2 minors. Evaluate the six ordered scalar products, reduce to the cross-product basis vector and tuple, compute √(w₁²+w₂²+w₃²), then divide by 2. The required response is the entire exact scalar area. Blanks supply A△= and expect only the scalar fragment. Source prose is fixed independently of the chosen error.

## 3. Component and bank mapping

Each record in extraction-data.json maps its prompt/solution mask, vertices, ordered edge vectors, cross product, N=||u×v||², exact area and complete bank. The 12 scalar banks underdetermine their original distractor intent. For explicit observed replay the recipe is a homogeneous expression scaling: replace each observed radical radicand b by bN/N₀, preserving original numerator coefficient and denominator. For a rational observed a, use a√(N/N₀). These formulas reproduce every value at N=N₀ and remain genuine parameterized expressions; they do not recover the original author's error operations. The correct expression scales to √N/2. They are explicit `observed/<source-id>` or `raw/<source-id>` profiles, never normal defaults. No scalar fitting or presumed diagnosis is presented as recovered.

The authored default radio profile is one whole five-operation bank: √N/2; √N (omitted half); N/2 (omitted square root); |u·v|/2 (dot product in place of cross norm); √((u·u)(v·v))/2 (edge magnitude product, omitting the angle factor). Every member is computed before accepting the instance. Nonpositive or equal values reject the entire instance; no option is filled from a fallback pool. Raw q-127908 is the sole explicit evidence exception to unequal distractors. The normal repair changes one duplicate as described in classification.md.

## 4. Reusable masks, domains and identity

`extract` constructs source masks by replacing complete mathematical RHS components and determinant numeric slots, preserving fixed prose, row order and source number style. Each arithmetic product independently records whether the original multiplicands were commuted. `solution` fills only complete slots. Negative multiplicative operands are grouped. The generator never returns a literal source question or a lookup answer. Every original source case calls the public API with original parameters and the original bank profile.

The authored easy/moderate/hard sections all call the same exact method. Bounds and scope are in classification.md and guard(). Translation and vertex permutation are incidental task aliases: the mathematical fingerprint canonically selects two coordinate differences among all six vertex orders. Axis rotations, altered Cartesian component patterns or distinct edge lengths are not deduplicated. Complete banks and layout belong in content identity, not task counts. Content UUIDs hash the actual displayed prompt, solution, bank, correct scalar and version; changing option order or a profile alias does not change identity. q-20016's missing observed labels remain separately counted.

The sampler is finite: pre-rejection ordered-edge upper bounds are 60² for authored easy, 1330² for moderate, and 2744² for hard; translation and labels do not increase those mathematical bounds. Explicit whole-bank validity and canonical deduplication further reduce them. Validation reports observed distinct tasks, not a claim of infinite numerical variety. All normal fields are single radio or blank assessment demands from the original response shapes.

The exhaustive easy radio domain in semantic-domain.json contains 1,824 eligible ordered edge pairs and 736 canonical meaningful tasks. Enumeration compares all five squared scalar values using exact integers, so it checks positivity and complete-bank collisions without numerical tolerance. Moderate and hard bounds remain upper bounds.
