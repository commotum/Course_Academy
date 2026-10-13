# Template extraction

The per-source transcription in source-components.json specifies every exact prompt, field, choice, correct value, and worked solution. source.edn preserves all original facts at one immutable basis. All source functions use real x; quotients require nonzero denominators. Logarithms require positive arguments, with ln(x) additionally nonzero when in a denominator. Trigonometric denominators exclude their zeros. Points in the tangent-slope families must be in the quotient domain.

Source-specific forms (no grouping by operation alone): q-17921 differentiates cos(x)/ln(x), unrated radio with missing correct/solution; q-47999 differentiates x^2/sin(x), similarly incomplete. q-340318 evaluates d[x/e^(3x)]/dx at 1, whole scalar blank. q-9908 evaluates d[cos(x)/(1+sin(x))]/dx at pi/2, no field. q-167328 expects the entire derivative of a previously defined f/h; q-167782 expects only cos(x)-sin(x) in a displayed numerator fragment. q-2385 differentiates cos(x)/(10x^2), five-option radio. q-340308 differentiates tan(x)/x, whole derivative blank. q-340309 differentiates x/sin(x), whole derivative blank. q-340316 evaluates d[2^x/(x^2-1)]/dx at 0, scalar blank. q-47943 differentiates e^x/cos(x), radio. q-47998 differentiates sin(x)/x^2, radio. q-48504 evaluates d[x^2/ln(x)]/dx at e, radio with opaque scalar distractors. q-48507 evaluates d[sin(x)/(2x)]/dx at pi, radio with opaque scalar distractors. Their bank profiles and layouts remain separate. No multimodal or multiple-field sources occur.

## Supported easy profile q-2385

Observed c=10; proposed bounded integer scale 1<=c<=20. Fixed numerator cos(x), exponent 2 and variable x; variable denominator c*x^2. No change in quotient-rule workload. Prompt asks for f'(x), radio key selection, five math answers. Exact recipes in original option order:

1. (x^2*sin(x)-2*cos(x))/(c*x^3)
2. (x*sin(x)-2*cos(x))/(c*x^4)
3. (sin(x)-cos(x))/(c*x^3)
4. (-x*sin(x)-2*cos(x))/(c*x^3), correct
5. (sin(x)-2*cos(x))/(c*x^3)

These are observed algebraic patterns. No inferred feedback is presented. Every recipe reproduces the entire original mathematical value at c=10. Domain x!=0. The sampler does not silently drop any option or mix profiles. Symbolic equality checks enforce a unique correct derivative and five inequivalent options. The full bank has four matched distractors.

## Supported moderate profile q-48507

Observed c=2; proposed bounded integer scale 1<=c<=20. Fixed numerator sin(x), denominator c*x, evaluation point pi. The learner must differentiate with the quotient rule, then evaluate sin(pi)=0 and cos(pi)=-1. Exact recipes in original option order:

1. 1/(2*c*pi)
2. -pi
3. c*pi
4. -1/c
5. -1/(c*pi), correct

All five values replay at c=2. Distractors 2–4 have unresolved misconception interpretations; these are explicitly retained observed expression patterns, not asserted causal error recipes. The bounds extend scale only; variable trigonometric arguments, points and exponents are outside this version. Domain x!=0, pi is valid. No recipe profile mixing, option-count change, or blank-to-radio conversion. Five options remain distinct throughout all 20 c values.

## Rendering and solution fidelity

Keep the original instructional sentences introducing u,v, applying the quotient rule, and (moderate) substituting the point and concluding the slope. Render a fixed solution with the formula, the original functions substituted with derivative markers, the evaluated primitive derivatives, and an equivalent simplified result. Moderate adds substitution, trig values, and final slope. Equivalent intermediate algebra is normalized; fidelity does not claim identical source bytes or identical factor placement. The derivative sequence is unchanged, and no invented misconception text appears in questions. Original full solutions remain available side by side with source-parameter and changed-parameter previews.

Unsupported generator templates retain their complete bank transcriptions and unresolved mapping flags in source-components.json. They are not counted as replay successes; the claimed complete replay coverage is 2/2 supported banks, 8/8 supported distractors. Their original content and learner responses remain unchanged.

## Identity and finite capacity

A task consists of the exact quotient function and, if applicable, evaluation point. Changing c changes the mathematical function and correct answer. Question identity is derived from that task, field identity from question plus field key, and answer identity from its owning field and exact value. Seed and option order do not affect task identity. A bank fingerprint sorts values. The observed easy and moderate families each have exactly 20 bounded tasks, including their source-parameter task; exclude source/canonical and existing generated tasks before committing. An exhausted family leaves an explicit finite-limit shortage. The CLI rejects counts exceeding the band capacity rather than duplicating tasks.


## Authored hard extension

u=x^2+a*sin(x), v=e^x+b*cos(x); a,b are positive integers 1..3. Source e-3638 supplies quotient-rule layout, q-47998 supplies polynomial/trigonometric combinations, q-47943 supplies exponential/trigonometric functions, and q-9908 demonstrates use of sin^2(x)+cos^2(x)=1. This is a new prompt/value template and profile with **authored** hard difficulty, not a replay of a nonexistent hard source. Compared with easy single-primitive quotients and moderate evaluation at familiar points, learners compute two sum derivatives and combine several cross terms. The required calculus rules are already in the source KP.

Let du=2x+a*cos(x), dv=e^x-b*sin(x), N=du*v-u*dv. Select the complete authored operation profile as one bank:

1. N/v^2, correct
2. (du*v+u*dv)/v^2, add instead of subtract
3. N/v, omit squaring the denominator
4. du/dv, quotient of the derivatives
5. N/u^2, square the numerator function instead

No observed source option is claimed to map to this profile. Every pair of a,b has five inequivalent complete rational/trigonometric functions, one correct derivative. Domain of the function/correct answer is v!=0. Incorrect options can have additional poles and are not equivalent to the derivative on its domain. These mistake recipes do not appear as learner feedback. The prompt is one radio field with selection key. The solution identifies u,v, substitutes their derivatives, applies the same quotient formula, and consolidates the trig squares into 1. The final numerator is e^x*(2x-x^2+a*(cos(x)-sin(x)))+b*(2x*cos(x)+x^2*sin(x)+a), over v^2. All displayed evaluated steps are independently parsed and differentiated. The bounded hard capacity is nine distinct tasks, and an exhausted pool leaves the shortage explicit.
