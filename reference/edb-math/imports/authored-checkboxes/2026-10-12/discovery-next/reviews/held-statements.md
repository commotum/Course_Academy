# Held statement review

Reviewed all 33 historical held cases at discovery basis 1534. No database writes or existing artifact edits.

All 33 support checkbox conversion under their stored source keys: 102 atomic statements and 165 complete old-choice mappings across 8 KPs. No missing keys, key changes, or unavailable capture evidence.

The 28 cases without source-verdict conflicts were held because the scanner did not recognize wording such as 'only statements', 'also true', or bare Roman labels. Independent proofs and raw source comparisons resolve these holds.

Seven worked solutions need corrections while preserving their existing keys:

- q-2459, q-2469, q-2471: VI is a typo for source statement IV.
- q-334851: remove stray +1, mark II false, and correct the signed/two-sided infinity arguments using absolute ratios.
- q-335020: mark III false; its own computation already establishes not O(1).
- q-71892: the type-II horizontal bounds constrain x, not y.
- q-71402: dividing 3y=-9x+c+4 gives intercept (c+4)/3, not /9.

q-71391 additionally needs a domain qualification: y!=0 removes two points from the implicit ellipse and circle. Its existing II/III key uses conic-shape classification. The review preserves that convention and records the exact omissions; a strict full-locus interpretation would require a separate content decision.

The JSON separates conversion-only proposed prompts from proposed worked-solution repairs. Root must reconcile current state and decide which explicit solution repairs to include before creating or previewing transactions.

| Class | Questions |
|---|---|
| big_o | 2 |
| discontinuity | 3 |
| ellipse | 1 |
| level_curve | 8 |
| level_curve_domain_qualification | 1 |
| linear_transformation | 2 |
| path_limit | 2 |
| region_both | 5 |
| region_neither | 5 |
| region_type_i | 1 |
| second_derivative | 3 |

Reproduce this isolated file analysis with `python3 reviews/review_held_statements.py`. It reads historical JSON snapshots only and asserts every source prompt/field, key, option mapping and independently derived verdict.
