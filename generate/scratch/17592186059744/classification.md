# Finding the Transpose of a Row Vector or Column Vector

Captured all 16 practice sources and canonical example at EDB basis 2680, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json`, `source-specs.json`, and `source-choice-mapping.json` retain every original field, bank, key, value, prompt, and solution. There was no registered generator and no job `.generated` file on initial inspection.

Easy: numeric entries, radio or one blank per entry. Moderate: formal algebraic entries, radio or one blank per entry. No hard source is observed; the package does not invent a higher-workload task. An unsupported hard band is a bounded capability exception, not evidence that hard transposition tasks are mathematically impossible.

Prompt/solution backbones are `Find ... given that ...` radio, `If ... then ...` radio, and `If ... find the transpose` blanks. Row/column orientation is a distinct mathematical role. Single-entry, two-entry, and three/four-entry blank layouts remain separate because their target field counts and table structures differ. In the three/four-entry column-answer blank family, length selects the corresponding source-backed layout and count. The two-entry row-answer table is a separate layout. Templates and per-source assignments (including shape, length, difficulty, field keys and bank profile) are in `source-specs.json`. Numeric and algebraic entries at the same shape have separate difficulty contracts. Radio bank profiles are separate from prompt templates.

Every template's plot rating is **none**. Matrices and tables are standalone mathematical notation, not graphical plots; no assets are needed.

`q-1045` contains two `selection` radio fields with equivalent complete banks; one historical field lacks a correct key. Normal generation preserves the valid captured single-field contract, explicitly omitting the redundant malformed field only in new content. All ten original bank choices are replayed for fidelity; the source question is preserved and excluded from available inventory. `q-1048` is unrated, lacks both a correct key and solution, and remains evidence-only. Its full five-choice bank is mapped and mathematically replayed but is never emitted as supported practice. Existing learner records and source identities are unchanged.

| Difficulty | Prompt/field template | Supplied orientation | Sources (profiles in source-specs.json) | Plot rating |
|---|---|---|---|---|
| easy | find-radio | row | q-1045 | none |
| unclassified | if-radio | column | q-1048 | none |
| easy | find-radio | column | q-11468 | none |
| moderate | find-radio | column | q-126136, q-70070 | none |
| moderate | if-radio | column | q-126137 | none |
| easy | if-blank-column-answer-4 | row | q-275365 | none |
| moderate | if-blank-column-answer-4 | row | q-275366 | none |
| easy | if-blank-column-answer-3 | row | q-282761 | none |
| easy | if-blank-column-answer-2 | row | q-282766 | none |
| easy | if-blank-column-answer-1 | row | q-282769 | none |
| moderate | if-blank-column-answer-2 | row | q-282775 | none |
| moderate | if-blank-row-answer-2 | column | q-282779 | none |
| easy | if-blank-row-answer-2 | column | q-282780 | none |
| easy | if-blank-row-answer-3 | column | q-282781 | none |
| easy | if-radio | column | q-70063 | none |

Template counts by difficulty: easy = 9, moderate = 5, unclassified = 1. Hard has no supported template in this package. Radio profiles are not added to the Markdown-template count. Exact entry counts select the source-backed blank layouts; field counts are preserved.
