# Template extraction (step 4)

All seven original records, omissions, UUIDs, prompts, full worked solutions, fields, complete banks and correct records are retained in `source.json` and `source-cases.json`. Every original choice is mapped individually in `choice-recipes.json`, including its original answer UUID and full expression. At original parameters the normal generator uses the original prompt/solution rather than a newly written approximation; `observed_raw(original_MA_ID, original_parameters)` returns the exact full Pull and is explicitly evidence-only and ineligible.

| Source | Variable, parameter | Original equation | Original bank in field order | Correct |
| --- | --- | --- | --- | --- |
| q-287665 | x, p | 2px=3 | 0, 3, 1/2, 1, 2 | 0 |
| q-288135 | y, p | 4py=-2 | 0, 4, -2, 1/2, -1/4 | 0 |
| q-288107 | t, q | 5qt=-4 | 5, 4, 0, 1, 1/5 | 0 |
| q-288593 | y, q | (q-1)y=4 | 1/4, -4, 2, 1, 0 | 1 |
| q-288596 | y, q | (q+9)y=-6 | 1/9, -6, -9, 6, 1/6 | -9 |
| q-288143 | x, q | -3(q+4)x=6 | 0, -3, 3, 4, -4 | -4 |
| q-288144 | z, p | -5(p-9)z=10 | 5/9, 10, 1/5, 9, -5 | 9 |

The response is the constant parameter making the variable coefficient zero while the supplied right side remains nonzero. The prompt identifies the equation's variable and parameter, supplies one equation, and asks for the parameter. Solutions state the general `ax=b` condition, identify a and b, set a to zero, then solve for the parameter. Easy has one final equation, moderate has two aligned equations, and hard has four equations including explicit division by the supplied nonzero multiplier. Changing the parameter's sign or magnitude has no progression: every instance at a level performs the same stages.

The frozen lesson introduces the contradiction `0=b` for nonzero b, then this parameter problem. The prerequisite topics include solving linear equations with variables on both sides and factoring linear expressions. The next KPs separately introduce constants on both sides and variables/constants on both sides; those structures are excluded here.

## Slots fixed before implementation

| Slot | Role and domain | Dependent content |
| --- | --- | --- |
| c | nonzero multiplier; integers of magnitude 2..7 for easy/hard; exactly 1 moderate | given coefficient, a assignment, zero-coefficient condition, hard numerator/divisor, complete bank |
| s | additive shift; exactly 0 easy, nonzero integer magnitude 1..9 moderate/hard | given coefficient, a assignment, every intermediate, final target -s, complete bank |
| b | nonzero RHS integer magnitude 2..10, either sign | given equation, b assignment, contradiction check, complete bank |
| bank profile | one full observed profile chosen before values; incompatible/ambiguous banks are excluded | all five values, correct owned ID, reproducibility metadata |

The target always has the role of the parameter in the variable coefficient. Its numerical value varies across both signs for moderate/hard. Zero is mathematically forced for easy, so changing that target would change the easy backbone. Equation-variable/parameter letters match the chosen source profile and do not count as substantive novelty. Operators and field contracts stay fixed; no free-input fields, alternative problem forms, or extra solution stages are introduced. Signed easy/hard multipliers extend sparse source coverage conservatively without adding a method.

Observed recipes are full expression patterns, not inferred procedures. For example, q-288593's value 2 is represented by b/2, but its psychological origin is unresolved; q-288144's 5/9 follows c/s with its observed signs. The evidence cannot identify a unique distractor mechanism. None is falsely presented as an authored procedural error, and no generic answer plus/minus-one distractors are added. Each profile is retained whole; values colliding with one another or with the target exclude that profile/parameter combination.

Substantive fingerprints ignore cosmetic labels, option order, seed, profile changes and nonzero uniform equation scaling. The bounds are finite. All API entry points enforce exact integers, nonzero conditions, the level's slot restrictions, and valid complete banks. Raw observation replay is excluded from batch and capacity APIs.
