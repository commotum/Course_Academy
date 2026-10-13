# Template extraction

## 1. Describe every observed question

The complete decoded prompts, enum objects, answer banks, correct values, field keys/order, solution prose and each aligned row are in `source.json`. `source-cases.json` maps every source to its public recipe/profile and original translation parameters k=h=0. The source family definitions in the script preserve exact t values, number forms, domains and operators:

- Quartic_axis: x=t⁴+t, y=t², t=−1; x-axis crossing in a tuple radio bank; image illustration. Missing source difficulty, solution and key. Independently x=0,y=1,x′=−3,y′=−2,m=2/3,mₙ=−3/2; crossing (2/3,0).
- Log_sine: x=ln(sin t), y=1/sin t on (0,π), t=π/2. ln1 evaluation, chain/reciprocal derivatives, canceled derivative quotient, tangent slope −1, normal slope 1, y=x+1. Both parameter derivatives vanish at this endpoint. The image curve y=e^(−x), x≤0 has unique one-sided tangent slope −1; normal output adds this justification before the original chain.
- Log_power: x=ln(t²), y=2t³−3t on t>0, t=1. ln1, chain derivative 2/t, cubic derivative, division by a fraction → multiply by t, slope3/2, negative reciprocal−2/3, line y=−2x/3−1.
- Cubic_axis: x=t²+t/2+1/2, y=t³+7t²+8t, t=−1. Signed coordinate substitution, 2t+1/2 and 3t²+14t+8, substituted quotient → −3/(−3/2) →2, normal−1/2. Point-slope normal at (1,−2), y=0 substitution, reversed-side equality, isolate x−1, x=−3; two blanks (−3,0).
- Sixth_axis: x=7t²−9t, y=t⁶+2t², t=1. Two polynomial sums, derivative ratio(6t⁵+4t)/(14t−9), substituted quotient10/5→2, normal−1/2. Five source normal rearrangement rows through y=−x/2+2; two intersection evaluation rows; (0,2), with field-2 first in capture.
- Cubic_linear: x=t³−3t, y=2−t, t=0. Zero substitution, derivatives3t²−3 and−1, quotient represented as (−1) times reciprocal then negative fraction, evaluate −1/(0−3)=1/3, negative reciprocal−3, line y=−3x+2.
- Exponential: x=eᵗ, y=2teᵗ−2eᵗ, t=1. Coordinate cancellation, derivative y′=2teᵗ, quotient cancellation 2teᵗ/eᵗ→2t, slope2, normal−1/2, line y=−x/2+e/2. Source prose incorrectly calls this the tangent line; raw retains it, normal replaces that noun with normal.
- Quartic_cubic: x=t⁴−3t², y=2t³−t, t=1. Point(−2,1), polynomial derivatives4t³−6t and6t²−1, quotient5/(−2), normal2/5, point-slope line y=2(x+2)/5+1.

No source asks to identify all horizontal or vertical normals. Those branches are excluded. All source difficulty values are compared to the actual captured enum ident, not just checked for presence.

## 2. Shared assessed pattern

Find the point by substituting the supplied t, differentiate each coordinate function, form y′/x′, evaluate the tangent slope, take the negative reciprocal, and find the normal via point-slope form. For hard sources, continue with the specified axis substitution and solve for the remaining coordinate. Each family retains its own arithmetic stage sequence. Raw anchors reproduce the entire shared prose and all stages exactly.

## 3. Component and complete bank mapping

`source.json` supplies every value verbatim, including whole equations and tuples. Every observed bank is retained as an inseparable evidence-only profile. The following is the full map in captured order:

| Family | Complete observed bank | Designated correct |
|---|---|---|
| quartic_axis | (3/5,0); (7/12,0); (5/8,0); (4/7,0); (2/3,0) | absent; independently inferred2/3 only for authored completion |
| log_sine | y=x+1; y=x+2; y=x; y=2x+1; y=2x+3 | y=x+1 |
| log_power | y=−2x/3+2; y=4x/3+2; y=−3x/2−1; y=2x/3+1; y=−2x/3−1 | last |
| cubic_axis | field-1:−3; field-2:0 | both |
| sixth_axis | field-2:2; field-1:0 | both |
| cubic_linear | y=−3x+2; y=−3x+12/5; y=−9x/4+2; y=−12x/5+2; y=−9x/4+8/3 | first |
| exponential | y=x/3+e/4; y=−x/2+e/2; y=−x/4+2e/3; y=x/2−e/4; y=x/2+2/e | second |
| quartic_cubic | y=2(x+2)/5−1; y=5(x+2)/2+1; y=2(x+2)/5+1; y=2(x−2)/5+1; y=5(x+2)/2−1 | third |

Historical numerical distractors do not establish author intent. Each whole line bank is parameterized geometrically by x→x−k and RHS→RHS+h, preserving its original complete mathematical objects at k=h=0. Legacy tuple x-intercepts similarly translate by k−h/mₙ. This is a pattern generalization, not a recovered error explanation. The quartic_axis raw raster profile is confined to the original geometry; its normally generated textual completion changes geometry without attaching the unchanged picture.

Supported normal radio banks are separately authored from the actual operation: correct normal; tangent through the point; positive reciprocal through the point; omit the point's x-coordinate; reverse the point's y-coordinate. They are selected as a whole before parameters, and any coincident lines reject the entire instance. The m=±1 log_sine family uses a separate complete operation bank: correct normal; tangent; normal through origin; reversed point y-coordinate; tangent through origin. This avoids equating tangent and positive-reciprocal errors. No first-valid pooling or unrelated random answer perturbation occurs. Bank errors have no invented learner-facing diagnosis. Hard completed questions preserve coordinate-fragment blanks, not unsupported equation blanks.

## 4. Reusable masks, bounds and consistency

All moderate/hard curves retain their source functions and t. Complete coordinate expressions accept integer translations k,h∈[−6,6]. Translations alter the point and normal line and, for hard questions, the axis intersection. Every coordinate evaluation equality receives its matching translation; every source normal rearrangement line is written in the corresponding translated coordinates. The source's cancellation, reciprocal, distribution and collection rows remain individually present, rather than becoming a generic CAS sequence. Hard intersection rows are derived for the actual translated normal with the same axis-isolation stages. Signed added quantities are grouped or signed explicitly. Complete coordinate tuples in prose and concluding intercepts have separate masks.

Easy parameters: x=at+k,y=bt²+h,t₀=±1, integera,b∈[1,4], k∈[−4,4], h∈[−4,−1]∪[1,4]. Nonzero a,b maintain the one-term derivative workload. The guard a≠2b prevents slope magnitude1, so easy always uses its preselected complete bank. The whole-bank eligibility check removes collisions, not individual choices. Explicit inputs obey the same bounds as sampled inputs.

Observed source replay is evidence-only, with eligibility flags, exact omissions and captured wording. Normal hard changes “Do not round the answers” to “Give exact answers”: the native grader otherwise treats “round” as a numeric form constraint and rejects meaningful equivalent exact expressions. Raw graded values and these rejected equivalents have separate counters. No engine changes.

Decoded byte scans of all34 answer strings show zero adjacent ordinal92 pairs; apparent double backslashes were JSON rendering. No backslash repair is applied. Exact raw source fidelity is8/8 prompts,7/7 present solutions,1/1 missing solution,7/7 difficulty enums,1/1 omitted difficulty,34/34 values,9/9 present correct refs,1/1 missing correct ref. There are no mathematical source-key errors; two explanatory-prose repairs are explicitly recorded above.

`finite-domain.json` enumerates the valid parameter families after whole-bank eligibility: 1544 easy tasks, 714 moderate tasks (134+140+141+156+143), and507 hard tasks. Both translations affect the printed curve and assessed line/intercept; bank and notation aliases are not counted. Parameterization is assessed via differentiation, rather than traversal direction.
