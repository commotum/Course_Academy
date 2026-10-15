# 3. Classification

Frozen math basis 2275, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. All 20 captured questions have Math Academy IDs; captured independently authored inventory is empty. The canonical example e-475 is context, not one of these 20 practice questions. Counts: easy 2, moderate 7, hard 11. There are 13 single radio fields (five options each) and seven single blank fields. One blank collects two equivalent spellings, for 73 total answer records and 52 radio distractors.

Twenty conservative prompt/solution templates are retained rather than merging different normalization sequences, definite versus indefinite tasks, or field shapes. Each template has its own complete observed bank profile; blank profiles have no distractors. Different endpoints with different field contracts remain separate. No question, answer or worked solution references an image or plot, so all plot ratings are none.

| Source | Level | Field / key | Collected values | Substitution | Plot |
| --- | --- | --- | ---: | --- | --- |
| q-2622 | hard | radio / selection | 5 | `cos(x)` | none |
| q-49259 | moderate | radio / selection | 5 | `sin(x)` | none |
| q-114294 | easy | radio / selection | 5 | `cos(x)` | none |
| q-347941 | hard | blank / field-1 | 1 | `sin(3*x)` | none |
| q-352786 | hard | blank / field-1 | 1 | `sec(x)` | none |
| q-352797 | hard | blank / field-1 | 2 | `1+sin(2*x)` | none |
| q-352798 | hard | blank / field-1 | 1 | `sin(2*x)` | none |
| q-362157 | hard | blank / field-1 | 1 | `cos(x)` | none |
| q-49256 | moderate | radio / selection | 5 | `3*x` | none |
| q-49257 | moderate | radio / selection | 5 | `sin(2*x)` | none |
| q-49277 | moderate | radio / selection | 5 | `cos(x)` | none |
| q-49278 | moderate | radio / selection | 5 | `cos(3*x)` | none |
| q-49280 | moderate | radio / selection | 5 | `4*x` | none |
| q-49281 | moderate | radio / selection | 5 | `2*x` | none |
| q-10040 | easy | radio / selection | 5 | `cos(x)` | none |
| q-49279 | hard | radio / selection | 5 | `tan(x)` | none |
| q-362158 | hard | blank / field-1 | 1 | `sin(4*x)` | none |
| q-114295 | hard | radio / selection | 5 | `cos(x/2)` | none |
| q-73371 | hard | radio / selection | 5 | `sin(2*x)` | none |
| q-347942 | hard | blank / field-1 | 1 | `sin(3*x)` | none |

Each original prompt, field, bank, correct designation and complete worked solution remains in source.json. source-cases.json replays only these MA originals. Independently authored parameter variants are in review-cases.json. The independent-inventory.json questions array is empty because the database capture contains zero non-MA questions; generated cases are never misrepresented as captured inventory.

Eleven original profiles contain bare brace-group trig operator names. Exact raw replays are ineligible for serving; separately supported normal operator-name repairs are included in the review cases. This presentation defect is separate from mathematical source correctness.
