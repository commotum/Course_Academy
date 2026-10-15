# Classification at frozen basis 2275

The immutable math snapshot has eight MA practice questions, six easy and two unrated. There are no independent non-MA practice questions; `independent-inventory.json` records this separately. The canonical example e-17087 supports context and exclusions but is not practice inventory. All questions and their full source fields are readable. The topic, lesson, and exact prerequisite-reference captures remain beside `source.json`. Full prerequisite lesson content was not supplied by the refresh snapshot; no new operation is inferred from that absence.

The prerequisite is Solving Linear Equations With Variables on Both Sides (topic 343). The lesson introduces cancellation leading to an always-false equality. It then moves to parameter-solving KPs, which this generator excludes: this KP asks only which supplied equations are inconsistent.

| Source | Variable | Ordered (a,b,c,d) for a*x+b=c*x+d | Template | Observed band | Bank |
|---|---|---|---|---|---|
| q-287964 | x | [[2, 0, 1, 1], [2, 1, 2, 1], [2, 1, 2, 3]] | summary-spaced | unrated | boolean-per-equation |
| q-288058 | x | [[4, -2, 4, 3], [3, 4, 3, 4], [5, 0, 2, 6]] | summary-spaced | unrated | boolean-per-equation |
| q-288066 | u | [[-3, 4, -3, -1], [2, 5, 2, 8], [6, -2, 3, 1]] | detailed-scaled | easy | boolean-per-equation |
| q-288070 | y | [[-4, 2, -4, -5], [6, 3, 6, -1], [5, -7, 2, 1]] | detailed-scaled | easy | boolean-per-equation |
| q-288072 | z | [[2, -4, 2, 1], [5, 6, 5, 6], [3, 2, 1, 4]] | detailed-scaled | easy | boolean-per-equation |
| q-288073 | w | [[3, 2, 2, 2], [4, -7, 4, -7], [6, 5, 6, 9]] | detailed-unit | easy | boolean-per-equation |
| q-288074 | v | [[9, -5, 4, 2], [2, 3, 2, 7], [5, -1, 5, -1]] | detailed-scaled | easy | boolean-per-equation |
| q-288069 | x | [[2, -3, 2, 4], [-5, 7, -2, -2], [4, 1, 4, 1]] | radio-detailed-scaled | easy | subset-five |

There are four prompt/solution/field templates: summary-spaced, detailed-unit, detailed-scaled, and radio-detailed-scaled. The first three use three independent I/II/III checkbox fields with the complete true/false bank. The radio template has one selection field and exactly five observed subset choices. Its authored target-position slot relabels the entire observed bank with the three supplied equations, through all six N/U/I role permutations. The identity permutation retains the source anchor; I, II, and III can each be the lone inconsistent equation without changing the classification workload. Detailed-unit omits a division row because the surviving variable coefficient is one; detailed-scaled includes it. Summary-spaced uses a three-result prose sentence. Radio-detailed-scaled preserves the unbulleted Roman labels and the full cancellation/division solution.

The frozen source has 22 field banks and 47 choices: seven questions × three binary banks, plus one five-choice radio bank. Their exact recipes, values, and correct designations appear in `choice-mapping.json`. Feedback is absent in all source answers and remains absent.

Plot rating is none for every template. No prompt, answer, or solution has an image or diagram. Steps 5 and 7 therefore do not apply; there are no plot assets to reconstruct.

All three output bands are mandatory. Moderate and hard have no observed examples here, so they use disjoint finite parameter catalogs with the same coefficient bounds, forms, response contract, and ordered solution stages as easy. The labels do not claim a source-backed increase in demand. No distribution, fractions in supplied equations, nonlinear operators, unknown parameters, or extra reasoning stages are added.
