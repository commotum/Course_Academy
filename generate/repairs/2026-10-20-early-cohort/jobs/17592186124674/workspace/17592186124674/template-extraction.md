# Template extraction

## 1. Specific source descriptions

Every question specifies a growing stock or speed below a maximum and asks for one differential equation. Capacity and initial stocks are positive integers; proportionality is represented by a positive symbolic k. The derivative always uses time t. Direct questions use current symbols N, F, S, P or V and four wrong operations: reversed gap sign, extra population factor, extra squared population factor, and negative sum. Capacity questions use R, T, M, B or C with a named initial stock, five numerical candidate equilibria and the same derivative form. Solution-bearing sources use exactly two display blocks: the general equation, followed by the capacity substitution, with complete context-specific prose between them.

## 2. General pattern

Convert “rate proportional to maximum minus current” into `dX/dt=k(a-X)`. Current stock is incidental when the question asks only for the ODE. A supplied numerical positive coefficient replaces k across the complete gap. The required answer is the whole equation, not an RHS blank, not a solved model.

## 3. Complete source-component and bank map

All source prompt and worked-solution strings become complete numerical-capacity/initial-stock slots in `extracted-recipes.json`. Each complete option is represented by its own full equation mask and a derived constant. Masks preserve text/spacing/LaTeX at original parameters. There is no literal-source payload return or keyed correct-answer lookup. Correctness follows the `correct` operation and is independently checked from the printed prompt.

Scalar wrong values alone do not identify historical authoring algorithms. These profiles use explicit normalized capacity ratios: if observed equilibrium B accompanies actual capacity A0, the replay recipe is `(B/A0)*A`. This is a transparent, genuinely parameterized evidence relation. It is not claimed to recover the original error intent. Full banks stay intact; they are never default learner sampling. Changed-parameter replay uses integer scaling and verifies every equation/prose stage. The ratios have finite bounds and every generated value must be a positive integer <=20000; explicit capacity is 10..5000 and initial stock lies strictly below it. No polynomial fits, random numerical perturbations or pooled first-valid distractors are used.

| Source | Complete bank recipes (in captured order) |
|---|---|
| q-106691 | reverse_gap; population_factor; quadratic_factor; correct; negative_sum |
| q-37376 | opaque (105/85)A; opaque (1700/85)A; opaque (65/85)A; opaque (55/85)A; correct |
| q-335135 | reverse_gap; quadratic_factor; negative_sum; correct; population_factor |
| q-335142 | correct; opaque (30/95)A; opaque (60/95)A; opaque (100/95)A; opaque (950/95)A |
| q-335145 | opaque (35/60)A; correct; opaque (150/60)A; opaque (250/60)A; opaque (50/60)A |
| q-344214 | reverse_gap; quadratic_factor; population_factor; correct; negative_sum |
| q-344218 | correct; population_factor; quadratic_factor; reverse_gap; negative_sum |
| q-344219 | correct; population_factor; reverse_gap; quadratic_factor; negative_sum |
| q-344228 | opaque (80/50)A; opaque (35/50)A; opaque (25/50)A; correct; opaque (18/50)A |
| q-344233 | opaque (320/1000)A; opaque (800/1000)A; correct; opaque (500/1000)A; opaque (1500/1000)A |
| q-335137 | reverse_gap; quadratic_factor; population_factor; negative_sum; correct |

The exact equation mask, field ownership, original option text, and raw correct designation or its absence are available in `source.json`, `extracted-recipes.json` and `source-cases.json`. All 55 displayed source option texts must match one-to-one. Of these, nine banks have captured correct designations; two have independently inferable mathematical answers but no captured designation.

## 4. Reusable template and constraints

Observed masks have fixed context, variable capacity and optional initial-stock slots. Whole banks are selected before sampling. Only complete mathematical integer components are substituted. Default normal easy questions parameterize five measured count contexts and capacity 20..500 with the entire direct sign/function-placement bank. Moderate/hard use the whole level-specific authored coefficient-placement bank. All options are independently parsed as full derivative equations and required to be pairwise unequal. Explicit parameter keys must exactly match the selected template, and invalid inputs fail rather than being silently changed.

Normal numerical catalogs: capacity A=20..500; initial I=1..A-1; moderate coefficient r∈{2,3,4,5,6}; hard r∈{1/2,1/3,2/3,1/4,3/4,1/5,2/5,3/5} with reduced numerator/denominator spelling. These are draft policies, not source constraints. Easy assesses 481 distinct numerical model capacities; moderate 2405 capacity/coefficient models; hard 3848 capacity/coefficient models. Named count contexts and symbols do not inflate these counts; initial stocks change presentation, not assessed ODE identity. Positive initial stock remains below capacity. No implausible negative count capacities appear.

Solution masks preserve full source wording/stage sequence, not selected shared phrases. Authored solutions retain the common general-model explanation → formal model → parameter assignments → substituted model. Correct-reference repair and missing-solution authorship are counted separately from raw reproduction. Source raw identity intentionally includes presence/absence of supported attributes. Captured database UUIDs and db IDs are evidence/provenance; generator instances receive stable new local UUIDs and do not reuse database question identities.

Content identity hashes generator version, actual displayed prompt, complete bank independently of ordering, fixed solution, correct designation and difficulty presence. Mathematical fingerprints use canonical model capacity and proportionality coefficient, excluding symbol/context aliases, initial stock, profiles and full banks. Identity invariance under changed seed/order, and differing identities for actual displayed prompts, are validated.

## Plot extraction / step 7

All source and authored question/bank/solution templates have plot rating **none**. The lesson introduction has a graph but no practice question uses it and no graph is required to translate the model. No assets or renderer are needed. Work stops after local generator and validation; no EDB transactions.
