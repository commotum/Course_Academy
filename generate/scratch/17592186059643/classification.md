# Classification

Immutable capture: math basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json`, `topic.json`, and `lesson.json` are unchanged capture copies. `ordered-lesson.json` follows activity/first-step and step/next.

Practice: **11 questions**, each with one selection radio field and five mathematical choices. **8 moderate, 1 hard, 2 unrated**. No practice easy sources exist. No plots occur; plot rating **none** for every template. Canonical examples are context, not practice coverage.

All questions combine two terms over a common denominator and apply sin²+cos²=1. The two unrated originals have no difficulty, correct reference or worked solution. Raw public replay preserves those missing attributes. Supported correct choices are inferred independently from the printed expressions; an inferred moderate assignment for the quotient-rewrite source and inferred easy assignment for the one-denominator source are design claims, not source labels. The API routes q1579 as inferred Moderate and q23522 as inferred Easy; repaired evidence exposes those inferred labels, while raw replay still omits the original absent difficulty attribute. Both originals remain counted as unrated source practice, and no observed Easy practice label is invented.

| Source | Observed level | Template | Shape / sequence |
|---|---|---|---|
17592186060072 | unrated | observed_q_1579 | cos/(1−sin)−tan; no source solution |
17592186060226 | unrated | observed_q_23522 | cos+sin²/cos; no source solution |
17592186253594 | moderate | observed_q_119764 | tan−(1−cos)/sin; rewrite, cross products, subtraction, identity |
17592186253596 | moderate | ratio sum | sin/cos+cos/sin; cross products, identity, reciprocals |
17592186253599 | moderate | squared numerator plus term | cos²/(1+sin)+sin; common denominator, expand, identity, cancel |
17592186253600 | moderate | squared shift | 1+cos²/(1+sin²); common denominator, identity |
17592186253602 | moderate | term minus squared fraction | sin−cos²/(1−sin); common denominator, expand, identity, signed cancellation |
17592186329714 | moderate | conjugate fraction sum | cos/(1−sin)+(1−sin)/cos; cross products, square, identity, cancellation |
17592186329718 | moderate | prefactored ratio sum | sin(cos/sin+sin/cos); distribute, cancel, common denominator, identity |
17592186335821 | moderate | sine/cosine-sum denominator | cos²/(sin+cos)+sin; common denominator, expand, identity |
17592186341847 | hard | linear numerator plus quotient | (1+cos)/sin+tan; rewrite, cross products, expansion, identity |

Each original has its own complete five-choice observed profile, with no pooling or invented diagnosis. Differences in prompts, answer shapes and complete ordered solution stages remain separate templates. `source-cases.json` supplies exact template identifiers and parameters for every row; those identifiers are authoritative.

The ordered lesson route is introduction → expanding-parentheses sibling → factoring sibling → rational-expression sibling → this common-denominator KP. Factoring-only and already-combined rational-expression problems belong to the sibling KPs and are excluded. Relevant prerequisites are adding rational expressions with no common denominator factors and reciprocal trigonometric ratios. No double-angle identities, numerical angle evaluation, equation solving, factoring exercises or new algebraic branches are added.
