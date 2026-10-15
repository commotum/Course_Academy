# Four extraction stages

## 1. Specific source descriptions

| MA ID | observed level | displayed shapes | ordered products | I, II, III keys |
|---|---|---|---|---|
| q-22063 | easy | A: 3×3, B: 3×2, C: 3×1 | AB, BA, AC | true, false, true |
| q-42374 | easy | A: 4×2, B: 2×4, C: 2×2 | AB, BA, AC | true, true, true |
| q-129437 | moderate | P: 5×3, R: 1×3, S: 1×5 | RS, RP, SP | false, false, true |
| q-22055 | easy | X: 2×2, Y: 2×3, Z: 3×3 | XY, YX, YZ | true, false, true |
| q-22056 | easy | R: 4×2, S: 2×4, T: 3×2 | SR, RS, ST | true, true, false |
| q-22062 | moderate | P: 1×5, R: 1×2, S: 5×2 | RS, RP, PS | false, false, true |
| q-42375 | easy | J: 3×4, K: 3×2, L: 2×4 | JK, KL, JL | false, true, false |
| q-42376 | easy | D: 2×2, E: 3×2, F: 2×3 | ED, FD, EF | true, false, true |
| q-42377 | easy | L: 2×3, M: 2×3, N: 3×2 | ML, MN, LN | false, true, true |
| q-42381 | moderate | O: 3×2, P: 2×3, R: 1×3 | OP, OR, PR | true, false, false |

All actual source arrays, every Boolean bank member and designation, complete prompt strings, and individual solution paragraphs/annotation stages are transcribed in `source-components.json`. Entries include signed integers, zeros, q-42374's literal -0, rectangular arrays, square arrays, row vectors and one easy column vector. Entry values never affect conformability and are excluded from task counts.

q-22063 has a final column vector and an opening without a period. q-129437 has two row vectors, trailing opening whitespace, and singular “row” in its first comparison. q-22062 has two row vectors and singular “row” in its second comparison. q-42381 has a final row vector and the source grammar “1 rows”. q-42375 has its original comma outside the final math delimiters in stages II and III. q-42374 has a trailing matrix-list comma, singular “statement”, and three plain lines which Markdown collapses in the real player. These details are preserved in raw replay and separately normalized only where documented for normal learning.

## 2. Shared pattern and purpose

Read the row and column counts of each supplied array. For three requested **ordered** products, compare the number of columns of the first factor with the number of rows of the second. Select precisely the true statements using three Boolean checkbox fields. The solution identifies all three dimensions, gives the left-column/right-row counts in prose for each ordered pair, states equality or inequality, prints both factors in order with dimensions and check/inequality annotations, boxes both equal inner dimensions, and concludes the complete true/false subset.

## 3. Components and complete banks

The prompt has a display containing three named bmatrices, a shared question sentence, the three product statements and the selection instruction. Each field owns distinct false/true answer UUIDs and a single correct lookup ref. Both Boolean options are real bank members; false is not omitted just because its checkbox is unchecked. A true member means left columns = right rows; false means inequality. There is no opaque numeric distractor inference and no choice pooling.

`source-components.json` maps each captured answer entity one-to-one to its field, exact value, correctness and rule. `source-cases.json` records original arrays and ordered pairs for every MA source, through normal public generate API with raw profile. At anchors both prompt and full solution match original strings byte-for-byte. Identity UUIDs are generated local identities, not copied database entities.

## 4. Reusable backbone, slots and fixed roles

Fixed: three supplied arrays, three distinct ordered pairs of different supplied arrays, three independent checkbox fields, two text answers per field, three full ordered-comparison stages and one complete conclusion. Three comparisons are fixed to preserve source workload; self-products are excluded because the observed role is comparison of two different supplied factors. The source names are retained as aliases, not counted as variety. There is no additional learner-facing distractor diagnosis.

Variable slots: each full array is rectangular and its dimensions are jointly bounded; entries are integers -9..9 and incidental; each full requested ordered factor pair varies among the six pairs without repetition, changing every dependent prose and factor annotation together. Source role/layout profiles retain their specific row/column-vector positions. Easy normal ordinary shapes use dimensions 2..4; q-22063 retains the third column-vector slot with length 2..4. Moderate normal ordinary dimensions use 2..5, at most20 cells, and row-vector lengths 2..5 in the source positions. Hard has exactly one row vector and one column vector of unequal lengths 2..5 and a nonsquare ordinary array with dimensions 2..5, at most20 cells; their label positions vary. Both vector orders and one other ordered pair are requested, in any statement order. These are equal-workload instances within each level, with no progression inside a level.

All normal and explicit inputs use the same role, dimension, entry and product guards. Raw evidence profiles retain original grammar and source number forms but remain bounded to dimension maximum5 and20 cells. Complete Boolean profiles are chosen before shapes/entries; every required option is always computed together. Any invalid array, role, repeated pair, unsupported profile or dimension is rejected as a whole. No subset fallback exists.

Meaningful task fingerprint includes the supplied shape multiset and the multiset of requested ordered factor-dimension pairs; it excludes names, array order, statement order, entries, seed, layout aliases and Boolean bank. Ordered factor roles are retained inside each comparison. Content identity includes normalized actual prompt, fixed solution, all Boolean banks/designations, version and level. Replaying fixed parameters with another seed returns the same question identities. Easy and moderate domains are disjoint by orientation roles (easy column-vector exception retained); hard requires both vector orientations and their ordered contrast. Canonical meaningful task counts are easy4542, moderate11040, hard576, exhaustively enumerated in semantic-catalog files. The larger ordered-presentation counts are explicitly separate in domains.json.

The authored hard rationale comes from e-4403's ordered AB/BA contrast, observed row/column-vector recognition, and prerequisites Introduction to Matrices and Multiplying Square Matrices. The linked activity route is first-step 17592186101674 →17592186101747 →17592186101675 (this KP) →17592186101676 (00870) →17592186101677 (00871), read from next links. The following siblings ask product dimensions from given dimensions or actual arrays; that assessed result is deliberately excluded here. The tutorial capture has omissions in generic dimension notation and repeated array images, so canonical and verified practice establish the recognition rule instead of inventing missing content.
