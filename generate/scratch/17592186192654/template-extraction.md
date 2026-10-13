# Four-stage template extraction

## 1. Specific observed questions

q-210858 has variables x,y; coefficients (1,−1),(−7,5), constants 1,9, semicolon-separated inline system after an unmatched visible brace. The first field selects equation first/second; the second selects a delimiter-free scalar. Capture array order is field-2 then field-1. Scalar option order 5,7,−7,−5; text order first,second. No original rating, solution, feedback or correct ref exists. MA4026 captured widget independently confirms the same two select widgets and values, with widget option order different from EDB's many-ref order.

q-210859 has variables s,t; coefficients (3,4),(1,5), constants 8,10 and the identical prompt mask. Capture order field-1 then field-2; text options second,first; scalar options 4,−3,3,−4. Same omissions and no feedback. Its required cancellation uses the second equation, while q-210858 uses first.

Canonical e-13995 (a+4b=1;2a+b=−5) supplies the source teaching sequence: notice coefficients, identify multiplication/cancellation, display original equations with ONE scale marker, display transformed first row, second row, grouped addition of remaining-variable terms/constants, collected equation, operation conclusion. Practice sources do not supply their own solution stages.

## 2. Generalized family

Given a1*x+b1*y=c1 and a2*x+b2*y=c2, select a single equation and scalar m such that m*a_selected+a_unchanged=0, then add. Response is the **paired operation**, not a solution tuple or transformed equation blank. Exactly one scaling marker is permitted. The first variable is always the elimination target; variables are presentation aliases.

## 3. Complete source component/choice mapping

Let A be the first-variable coefficient in the original nonunit row and B its second-variable coefficient. Historical interpretation beyond these expressions is underdetermined; raw banks are evidence-only even though the complete source banks are mathematically unambiguous at anchors. The recipes below reproduce all values and genuinely respond to changed coefficient parameters. They do not claim recovered distractor intent.

| Source/profile | Field | Answer UUID | Exact value | Parameter recipe |
|---|---|---|---|---|
| raw-q-210858 | field-2 | 8e0b7d00-1654-52b7-9052-7a91aba67a61 | 5 | B=b2 |
| raw-q-210858 | field-2 | 8f6b863b-f16e-552b-a6e4-05539ba27cdf | 7 | −A=−a2 |
| raw-q-210858 | field-2 | 11e4d5ce-3fc3-53e8-8584-1042acdeff24 | −7 | A=a2 |
| raw-q-210858 | field-2 | 41f6c130-1233-542f-a28b-1ce8647c5922 | −5 | −B=−b2 |
| raw-q-210858 | field-1 | 15818fb1-87d0-562d-b98a-b5e28f06c22d | first | fixed ordinal |
| raw-q-210858 | field-1 | 191da071-188e-5707-938f-7f3a2b084c8d | second | fixed ordinal |
| raw-q-210859 | field-1 | 8a45b4e3-546f-58ce-bc86-f21f14be794d | second | fixed ordinal |
| raw-q-210859 | field-1 | 6ce11990-8f77-5ca3-bb7c-924e6d9f7e71 | first | fixed ordinal |
| raw-q-210859 | field-2 | d2d6ae65-382f-5725-8d12-368b3161c220 | 4 | B=b1 |
| raw-q-210859 | field-2 | e5dd37b2-c127-522c-8a0a-7efbd395282d | −3 | −A=−a1 |
| raw-q-210859 | field-2 | 2d811e29-d735-5f20-b57d-488fa19f4d20 | 3 | A=a1 |
| raw-q-210859 | field-2 | 43aa771d-f31e-507f-a36a-818c77be68a0 | −4 | −B=−b1 |

All answer attributes, IDs, source field order and original values are preserved in public raw anchor replay. No source designation exists. Inferred first/7 and second/−3 are independently calculated from displayed equations and original banks, then appear only in authored completions. Original practice solution absence is preserved; canonical solution is contextual, not silently inserted into raw records.

## 4. Reusable mask, domain, calculations and extension

Fixed prompt prose and `{{field-1}}` / `{{field-2}}` layout are shared. Whole coefficient-variable terms and constants are slots; variables are selected only from xy,st,ab,uv. Conditional coefficient ±1 rendering omits the numeral; negative terms have a proper subtraction sign. Raw masks preserve source `- 7x` spacing; normal masks produce balanced `\{` notation. Public profiles are `raw-q-210858`, `raw-q-210859` and default `authored-coefficient-confusion`.

Raw replay is parameterized via the same prompt/choice recipes, with absence parity. It preserves exact source UUIDs at anchors and assigns content-dependent IDs under changed parameters. Raw evidence is not eligible for learning; its missing correct refs cannot be natively graded. Normal default uses the smaller absolute target coefficient's row and m=−a_other/a_selected. The complete authored scalar bank [m,−m,b_other,−b_other] is selected before sampling. Wrong signs come from forgetting cancellation sign; b_other and −b_other come from reading the remaining-variable coefficient in place of the required first-variable quotient. This is a plausible **authored** method-related bank, not recovered historical error diagnosis; no diagnosis enters learner prose.

Compute the correct pair and all four scalars. Reject the whole instance on duplicate values, nonunique full `(first/second,scalar)` combinations, zero defining coefficients, singular systems or level-bound violations. Never substitute first-valid wrong options. In particular [m,−m,1/m,−1/m] is invalid with this paired response because the reciprocal scales the other row correctly. A changed full system's equivalence is checked independently but cannot override required first-variable cancellation.

The four aligned rows keep the canonical operation structure at original and changed values. Solution ends at (b1'+b2')y=c1'+c2'; it never divides to solve y, nor substitutes to solve x. The normal explanation adds only the explicit name of the unchanged equation in the cancellation sentence, making reversed row selection clear. Canonical shared prose/conclusion and ordered stages are retained; practice-source worked-solution fidelity has denominator zero.

The finite meaningful strategy domains have 24 easy, 36 moderate and 36 hard tasks: actual division operands count after normalizing global target-coefficient sign aliases; variable aliases, bank profiles, b/c variation and option order do not. Common magnitude scaling remains in the fingerprint because deciding 12/3 versus 4/1 changes the actual printed quotient calculation and authored workload; b/c values only affect the unassessed demonstration. Full content identity includes printed prompt, solution, full bank, version and authored difficulty, independent of shuffle/seed.

No plots exist or are needed. Generator scope stops at documentation, source replay, parameterized local records and native grading; no EDB writes, engine changes, registration or transaction preparation.
