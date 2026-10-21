# Corpus-wide fraction-parenthesis repair

The earlier pass checked tutorials linked to the exponent lesson. The newly
reported entries, tutorial **17592186111878** and worked solution
**17592186110491**, belong to the logarithm quotient-rule lesson. Both are fixed.

This pass scanned all five stored content attributes across the database,
including **all 6,180 tutorials**, rather than selecting individual lessons.
It found and repaired **12,539 fields on 11,492 entities**:

| Content | Fields repaired |
| --- | ---: |
| Tutorial content | 199 |
| Worked solutions | 8,350 |
| Question prompts | 1,378 |
| Answer values | 2,612 |

The main repair adds only `\left` and `\right` around the exact fraction forms
recognized by the shared formatter. Removing sizing commands from each before
and after value produces identical bytes. It does not change exponents,
coefficients, signs, expression order, answer identities, correct-answer links,
or learner data.

All **15,242 unique changed math spans** were compared before and after through
the learner UI's actual MathJax typesetting path, with **zero introduced errors**.
The two reported entries were also rendered as full learner pages and inspected.

The comparison exposed four preexisting errors. Archived MathML establishes
that two tutorial formulas lost zero-stroke binomial notation and text handling,
and two worked solutions lost overbars. These four fields were reconstructed
separately, rendered without errors, committed, and read back exactly. Their
evidence and receipts are under `additional-errors/`.

The main repair committed in eight bounded transactions, with exact field CAS
and application entity validation, through the configured application writer.
Every committed batch was read at its exact before and after bases and compared
against the intended replacements. All other pulled question, answer and
tutorial data are unchanged. Requests, previews, receipts, and readbacks are
retained under `batches/`.

- Main repair: committed through basis **4919**; `verification.json`.
- Four source-specific reconstructions: committed at basis **4921**;
  `additional-errors/verification.json`.
- Fresh full-corpus check at basis **4921**: **zero remaining matches of this
  exact fraction-parenthesis pattern**; `final-census.json`.

All four registered generators in the reported logarithm lesson were checked.
Two bundled formatter copies lacked the fraction-sizing rule and reproduced the
defect. Their packages now include that rule; only the normalizer and patch
version metadata changed. Before/after comparisons of **80 seeded records**
verify unchanged mathematical content and correct answers. Full learner-page
renders passed for all four generators. The two package references were committed
and read back at basis **4922**; `generator-commit-verification.json`.

The scan covers the shared formatter's fraction-parenthesis rule. It is not a
claim that every possible LaTeX or layout defect has been eliminated.
