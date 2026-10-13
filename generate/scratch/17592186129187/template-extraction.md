# Template extraction

Database provenance is fixed to math basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `choice-extraction.json` is the per-choice component map; `source-cases.json` maps every original to its normal parameterized template/profile.

## 1. Specific source descriptions

| Source | Transformation x,y | Observed forms and response |
|---|---|---|
| q-38078 | 2u cos v, 3u sin v | positive integer scales, product/trig derivatives; determinant 6u; five scalar multiples of u including ratios |
| q-160381 | 3u+2v, u+3v | linear coefficient matrix, constant determinant 7; bank mixes constants and linear expressions |
| q-160404 | 3u-5v, ln(u+v) | negative v coefficient and positive log argument domain; rational determinant 8/(u+v) |
| q-38241 | cos v tan(u/2), sin v | inner fraction, product and chain derivative; zero y_u; cosine-squared reciprocal answer |
| q-81264 | u²-v², u²+v² | quadratic sum/difference, four linear partials; determinant 8uv |
| q-160403 | exp(u+v), ln(uv) | exp of sum, log of product; reciprocal partials and common denominator; exp(u+v)(u-v)/(vu) |
| q-160405 | cos(u+v), 4u+6v | equal trig partials and unequal linear partials; -2sin(u+v) |
| q-81252 | sin(u+v), cos(u-v) | chain signs from sum/difference; 2cos(u+v)sin(u-v) |
| q-160406 | exp(u+v), u²+v² | common exponential with two linear partials; 2exp(u+v)(v-u) |
| q-38244 | ln(2u+v), uv | logarithmic reciprocal partials and product partials; unrated and no original solution/designation |

All prompts ask for the whole symbolic determinant. Easy sources use a display vector transformation; rated moderate sources use an inline transformation. q-38244 already uses inline bmatrix notation. Each field is a single `selection` radio with exactly five math answers, no answer-specific feedback, no blank fragment and no additional demanded quantity. UUID/correct lookup refs are generated field-owned local review identities.

Nine supplied worked solutions share: “Given a transformation”, the generic vector, determinant definition, “Here, we have”, “First, we find the partial derivatives:”, a two-row partial-derivative layout, “Therefore, the corresponding Jacobian determinant is”, then generic determinant, substituted determinant, product expansion and simplification. q-38241 goes directly from the substituted matrix to the simplified answer because y_u=0. Linear, quadratic, polar and exp/log sources have an extra scalar simplification row. All these sentence/stage patterns remain. Invisible function-application characters, `operatorname` trig and aligned bracket vectors normalize to standard native LaTeX; redundant spacing/text spaces normalize too. Source q-38078's incorrect intermediate row is corrected explicitly below.

## 2. Generalized pattern and purpose

Compute the four partial derivatives of two explicitly given functions x(u,v), y(u,v); assemble them as rows of the Jacobian matrix and evaluate x_u*y_v-x_v*y_u. The assessed skill is that determinant expression, not any geometric consequence. Difficulty varies only with the derivatives and algebra already present in the owning lesson.

Families remain separate because their function structures, symbolic answer forms and solution simplifications differ. Integer parameters vary outer scales, linear coefficients and the inner tangent divisor; the hard template varies low powers of the canonical sum/difference functions. No template alters the required response or introduces another branch of instruction.

## 3. Components and full observed bank map

`choice-extraction.json` lists every original choice's original LaTeX, parsed exact expression, parameterized generator recipe label, computed recipe expression, and complete profile. Fifty choices across ten banks are accounted for. The code's `observed_bank` contains the explicit operations for each complete bank; for example polar uses -b*u, a*u, (a/b)*u, -(b/a)*u, a*b*u, and linear uses c*u+b*v, a*d+b*c, a*d-b*c, a*d*u, a*u-c*v. These formulas preserve source shapes; the scalar source evidence does not uniquely identify their intended error mechanisms. The quadratic bank likewise retains 2x, a*u²-a*b*u*v+b*v², the determinant, 4(a*u-b*v), and 0 as a labeled expression replay, not a claim that the original author made a particular mistake.

Other observed banks track nested inputs: tangent choices retain the u/k input, a missing u/k input, factor inversion and cos v additions/subtractions; trig choices retain both original and swapped u+v/u-v arguments. Log/product choices retain numerator alternatives over the same log argument. No arbitrary polynomial fitting is used. **Every observed profile is explicit replay only**, and uncertainty about author intent remains. Parameterized replay profiles also generate review variants, but the default learner banks are separately authored operations on the derivative matrix.

Authored defaults use reverse determinant subtraction, omitted diagonal products, added products, and multiplied products; tangent defaults use omitted/inverted chain factor and omitted y derivative. Recipes are selected as whole banks before construction, with all ambiguity/equivalence checked. Invalid explicit inputs fail; sampled inputs reject the whole instance. No learner-facing diagnosis is added.

## 4. Reusable templates, constraints and scope

Fixed text: the prompt request, derivative/determinant definitions, shared instructional sentences, one worked solution independent of answer choice. Variable: x,y; four partials; determinant entries; scalar expansion and simplification; all five choices. Conditional: inline vs display transformation, and extra simplification row by family. There are no plots and no optional learner fields.

Default sampling policies are authored bounds: positive scales 1..5; linear coefficients 1..6 with nonzero determinant; linear/log a=2..6, b=-2..-7; cos/linear positive unequal coefficients up to 8; tangent divisor 2..5; hard scales 1..3 and powers (3,2), (2,3), (3,3). Explicit parameters allow wider small integer ranges documented by `validate_parameters`, including every observed value. No random perturbation is used to make wrong answers. Parameters, profile, domain and complete bank content determine identity; shuffle/seed do not. A separate parameter fingerprint supports deduplication across distinct banks.

Domains: polynomial/trig/exponential families are real-plane functions, tangent excludes cos(u/k)=0, log(u+v) requires u+v>0, log(uv) requires uv>0, log(a*u+b*v) requires a*u+b*v>0. Domain metadata stays outside learner content, matching the source tasks.

Missing hard scope: canonical e-6810 already differentiates powers of two linear forms and factors the resulting determinant. Its four chain derivatives and determinant are more involved than the rated moderate first-order trig/exp/log forms without needing a new skill. Powers (3,2), (2,3), (3,3) have comparable workload, not an internal progression. Prerequisites are Introduction to Partial Derivatives and The Determinant of a 2x2 Matrix; the topic follows Computing Partial Derivatives Using the Rules of Differentiation. The actual activity first-step/next route is captured in `lesson-route.json`; finding the determinant precedes Evaluating a Jacobian Determinant, local area scale, and orientation KPs. These later tasks are excluded.

## Source anomalies and correction evidence

q-38078 displays `6u(cos² v+cos² v)` after correct diagonal products. Differentiating the displayed transformation gives 6u*cos² v+6u*sin² v. The new solution uses the verified latter expression and retains the final 6u. All five original answer values and the original correct designation remain matched.

q-38244's authoritative file `/home/jake/Developer/MA/DATA/Lessons/1999/Source/1999.json` (question 38244, five choices) confirms the captured widget bank. It supplies no correct designation. Direct differentiation gives x_u=2/(2u+v), x_v=1/(2u+v), y_u=v, y_v=u, so J=(2u-v)/(2u+v). This is a mathematically authored repair, **not a matched original designation**. Its authored worked solution follows the same shared solution scaffold; its moderate assignment is also authored. Raw evidence remains unchanged.

All 50 source values and all 10 complete banks must match, but only 9 original correct designations exist. Validation reports these denominators separately, with no hidden source exclusions. Source rendering normalization is separate from value equivalence and the acknowledged typo correction.


## Parent variety review

Hard retains the canonical powers-of-linear-forms method and adds inner coefficients 1 or 2: x=a(pu+qv)^m, y=b(ru-sv)^n. Outer scales remain 1..3 and powers (3,2),(2,3),(3,3). All-one inner coefficients reproduce the canonical form. These 432 bounded parameter combinations vary the four chain-rule factors without adding a mathematical branch, evaluation, orientation, or area scaling. This extension addresses the initial 27-combination limit; it is authored variation rather than an observed template.
