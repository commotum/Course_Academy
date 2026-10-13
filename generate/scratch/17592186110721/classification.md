# Classification

Snapshot: database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`; current source capture is retained unchanged as `source.json`. There are seven practice sources: three observed easy radio questions, two observed moderate blank questions, and two unrated originals. Canonical e-18852 is context, not an eighth practice source.

| Source/template | Observed level | Field | Structure | Solution stages | Plot |
|---|---|---|---|---|---|
| q-288622 | easy | radio, 5 choices | shifted coefficient; scaled constant | formal equation/rule, displayed equation, match/solve each, sum | none |
| q-288623 | easy | radio, 5 choices | scaled coefficient with fractional answer; direct constant | same, omits redundant constant solve | none |
| q-288627 | easy | radio, 5 choices | divided coefficient; direct constant | same, omits redundant constant solve | none |
| q-288583 | moderate | blank, 1 answer | scaled coefficient; reversed-sign shifted constant | match/solve both, signed sum | none |
| q-288584 | moderate | blank, 1 answer | reversed-sign shifted coefficient; scaled constant | match/solve both, sum | none |
| q-287978 | unrated | radio, 5 choices, no correct ref | shifted coefficient; direct constant; inline prompt | absent | none |
| q-287985 | unrated | blank, no answers or correct ref | shifted coefficient; scaled constant; inline prompt | absent | none |

Seven prompt/value masks preserve different inline/display spacing, answer fields and solution omissions. Each source has an explicit complete raw bank profile. No plotted assets occur; plot extraction and generation are not needed.

The authoritative local lesson capture `/home/jake/Developer/MA/DATA/Lessons/1414/Source/1414.json` confirms q-287978 is a five-choice math multiple-choice widget and q-287985 is one math-editor free-response textbox. It has no worked solutions or difficulty labels for these questions. Their normal authored completion is easy: the coefficient shift and constant scaling reproduce canonical e-18852 and observed easy q-288622. The verified answers are 8 and 10, respectively. Missing source designations cannot count as matched designations.

No mathematical source errors were found. Decoded integer byte-run audit finds **zero adjacent-backslash runs in all 22 source choice strings**, including the fractional q-288623 bank. Apparent doubled slashes in tool serialization were not source bytes and require no normalization.

Lesson order follows activity/first-step and step/next: introduction → identifying identities (10719) → coefficient-only rule and one parameter (10720) → general coefficient/constant rule → tutorial with independently matched parameters → this KP (10721). Its prerequisite topic is linear equations with variables on both sides. Later polynomial-coefficient and coupled-system topics are outside this implementation.

Hard is authored, not observed: two independently matched affine parameter expressions, each with a nonunit multiplier and nonzero offset, with at least one rational answer, followed by the same parameter sum. Primitive coefficient triples prevent common-factor reduction from removing its arithmetic workload. These are two separate single-parameter equalities, never coupled systems, quadratics, or solution-count classification.
