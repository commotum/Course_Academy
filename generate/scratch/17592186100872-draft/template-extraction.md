# Template extraction

## 1. Specific originals

`replay-specifications.json` records every original's exact parameters, prompt/solution masks, field keys/types, original correct-reference presence, all 46 raw values, complete per-cell recipes, matrix progression masks, observed labels, source errors and arithmetic ceilings. `source-cases.json` covers all 11 originals through the public `generate(..., profile="observed-raw")` API. The two unrated sources use an authored dispatch level `easy` in that metadata; their raw question records still omit difficulty, worked solution and correct refs. No absent attribute is called a matched designation.

The observed inputs are small signed integer coefficient matrices, inner dimensions 2–4, rectangular output matrices and ordinary A/B-style factor names. Field values are complete matrices for radios and single numeric entries for blanks. The blank layouts supply the other result entries. A fragment is never promoted to a complete equation.

## 2. Generalized backbone, defined before implementation

Verify dimensions and matching inner dimensions. State conformability and output dimensions. Compute each requested entry in row-major order using the ordered row of the left factor and column of the right factor. For each entry show the same full factor matrices, a progressively filled result, and that entry's complete dot-product factors. Conclude with the complete product. Blanks compute at least two unknown entries; radio asks for the entire product. The solution is fixed for an instance and independent of learner response.

Fixed components: matrix multiplication, integer entries, left/right roles, original family dimensions, original answer type/count, dot-factor order, conformability/progressive-result/conclusion stages. Variable slots: every numeric operand entry within coupled caps, selected queried result cells for partial-matrix families (same count and scalar role), all dependent supplied product cells, factors, sums, result entries and answer values. Source factor names remain fixed and do not increase task counts. No operations or stages are introduced for variety.

## 3. Complete component/choice mapping

For every source, `bank[*].choices[*]` in the extracted specifications retains raw values and original answer UUID, and supplies a full rectangular array of parameterized expressions. An expression is a finite signed sum of actual operand entries (`A,i,j` / `B,i,j`), individual multiplicative terms (`product,i,k,j`) or complete row-column dots (`dot,i,j`). There are no fixed answer lookup tables or literal payload-return branches. Each expression exactly reproduces its observed cell and re-evaluates when the operands change. Those historical distractor expressions are explicitly opaque: multiple operations can explain an isolated integer and no intent was recovered by fitting one expression. They are exposed only as ineligible evidence profiles. Default generation never samples them.

The single complete normal radio bank is selected before any operand sampling:

1. Correct row-column product C.
2. Transpose of C (placing result entries by the wrong orientation).
3. Negation of C (global sign error).
4. Dot products omitting their final term.
5. Dot products alternating the signs of their actual successive products.

All five complete objects must be pairwise different, including shape. Any collision rejects the whole instance. No member is repaired or replaced from a pool. Blanks have one owned scalar answer per original field and no distractors. Wrong-option diagnosis is metadata/documentation only, never learner-facing prose.

## 4. Reusable template and permitted domains

Every observed source family is served by normal easy sampling, including all partial result layouts, rather than being available only in replay. Original zero positions remain zero in easy; other entries range over nonzero signed integers. Random easy values use magnitude at most min(5, source coefficient ceiling). Explicit easy inputs may use the full recorded source ceiling, but must satisfy the same product, dot-L1, result and displayed-bank guards. All observed profiles use that original family's ceilings and preserve original values. Normal method-profile query targets can vary over all result cells with the original count; observed profiles explicitly reject any target map different from their source map; they stay in row-major order. Supplied cells, keys and worked stages follow the chosen roles together.

Authored moderate is 2×3 times 3×2, nonzero entries, coefficient≤6, individual |product|≤12, dot sum of absolute products≤24, |result|≤18. Authored hard is 2×4 times 4×2, nonzero entries, coefficient≤5, individual |product|≤10, dot sum of absolute products≤20, |result|≤18. Normal samplers conservatively use coefficient magnitude≤5 for both. Every displayed distractor coefficient is also bounded by the dot-L1 ceiling. These restrictions are joint, not independent large boxes: an individually permitted factor can be rejected when coupled to another factor. Explicit inputs and random sampling run the identical guard. No new operator, number form, symbolic method or algebra progression is present.

The task fingerprint contains actual A/B entries, queried roles and assessed information/workload, excluding seed, factor-name aliases, complete banks and profiles. The content identity includes normalized learner prompt, fixed solution, complete bank, expected selection and actual difficulty; changing seed or choice order preserves it. Stable field-owned answer UUIDs are derived only after shared `math_format.py` normalization. Every matrix is explicitly an ordinary coefficient matrix, not an augmented system.

### Raw anomalies and normal repairs

q-1029 and q-1034 omit difficulty, correct reference and worked solution in the capture. Raw public replay preserves all three omissions. A separately authored/repaired presentation infers the unique true matrix product and supplies the same shared source solution stages. Their native bank checks use that completed fixture and never claim an original designation match.

q-129495 prints the wrong A in its last intermediate row: first row [-2,1,1] instead of [2,-1,1]. The last dot and final product are nevertheless correct for the actual prompt. Raw replay retains this error byte-for-byte after shared normalization. Normal/repaired output prints the actual operand consistently. Thus 9/9 captured solutions replay exactly, but 8/9 are mathematically sound in all operand displays; the repaired normal solutions are checked independently.

The legacy blank Markdown tables have five padded/shifted columns. Normal output uses a consistent product label plus one column per result entry. Raw replay retains the original layout. The odd early reveal of an unknown in q-317846's first result matrix remains in raw; normal progress matrices show only supplied entries and already-computed unknowns. Logical teaching stages and requested-entry order are unchanged.

All captured aligned calculations put the factor equation and scalar dot in separate horizontal columns, overflowing the actual 662px inner player width. Normal/repaired presentation places the dot immediately below its matching factor equation within the same ordered aligned chain. This is a documented line-wrap repair: all operands, individual factors, progressive matrices, prose and logical stages remain; the original physical row count is retained only in raw replay. No arithmetic operation is replaced by an equal but structurally different one. Raw screenshots include horizontal-scroll views; normal output must fit without scrolling.
