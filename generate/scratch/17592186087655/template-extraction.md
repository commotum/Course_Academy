# Four-stage template extraction

## 1. Specific observations

Every practice source is listed with original parameters, field key/type, attribute presence and all choices in `source-components.json`. q-54187 and q-54210 use spaces in complete equation answers; later sources use compact TeX, including `{x}^{2}`, `{y}^{2}` for zero shifts. All radio sources have five math choices and no distractor feedback. Choices are whole equations, never center/radius tuple responses. q-167932 has one blank full-equation answer and `{{field-1}}`. Its prompt image is stripped; the raw source's whitespace is retained.

The six present solutions open with the general equation, state the center and radius from the diagram (or “In our case” for blank), and display three aligned rows: general relation, unsimplified signed coordinate/radius substitution, simplified standard equation. q-117081 encloses the first shifted x term in an extra brace group. q-167932 repeats the final equation in a concluding display after its aligned block. Exact replay preserves those sentences, complete rows and conclusion; there are no inferred worked solutions in raw unrated replay.

Original parameters: q-54187 (1,3,3), q-54210 (-2,5,7), q-167932 (3,0,3), q-116929 (-4,-3,6), q-117077 (2,-3,4), q-117081 (-5,0,7), q-70896 (1,2,5), q-70898 (-2,-3,8). Radii are positive integers; coordinates can be signed/zero. Plots explicitly label all input numbers rather than requiring estimation.

## 2. Shared mathematical pattern

Substitute the given center (h,k) and positive radius r into `(x-h)^2+(y-k)^2=r^2`, retaining minus signs around signed coordinates; then simplify shifted signs/zero terms and square r. A radio selects the complete equation; a blank writes that complete equation. Real-plane variables and r>0 determine the circle, and complete-equation equality is compared up to a nonzero scalar, not by sidewise equality.

## 3. Component map / complete profiles

Operation tuple `(u,v,q)` renders the proposed equation `(x-u)^2+(y-v)^2=q`. Thus changing u/v represents the operation of reversing a center sign, swapping input coordinates or omitting a shift. q=r is failing to square the input radius; q=sqrt(r) is taking a square root of the given radius instead of squaring it (this is an inferred interpretation, not recovered author intent); q=r² is the intended square. Every source choice including compound mistakes has an explicit parameter-dependent tuple below and a one-to-one answer ID/value map in `source-components.json`.

| Profile | Complete ordered operation bank |
|---|---|
| q-54187 | (h,k,r), **(h,k,r²)**, (-h,-k,r), (-h,-k,r²), (h,-k,r²) |
| q-54210 | (-h,-k,r²), (-h,-k,r), (h,-k,r²), **(h,k,r²)**, (h,k,r) |
| q-116929 | (-h,-k,sqrt(r)), (h,-k,r), **(h,k,r²)**, (-h,k,r), (-h,-k,r²) |
| q-117077 | (-h,k,r), (h,-k,r²), **(h,k,r²)**, (-h,-k,r²), (-h,-k,r) |
| q-117081 | (-h,k,r), **(h,k,r²)**, (0,0,r²), (h,k,r), (-h,k,r²); k=0 |
| q-70896 | (-h,k,r²), (k,h,r²), **(h,k,r²)**, (-h,-k,r²), (-k,-h,r²) |
| q-70898 | (-k,-h,r²), (-h,k,r²), (-h,-k,r²), (k,h,r²), **(h,k,r²)** |
| blank | **(h,k,r²)**; no distractors |

Bold tuples are mathematically correct. q-54187/q-54210 have no observed correct reference, so bold is inferred analysis only and raw field correct refs remain absent. Source banks are not pooled. Swap profiles reject equal or opposite coordinates whenever a required choice collides. All profile collisions (including zero signs and radius/square equality) reject the whole sampled instance, not an individual option.

The authored default bank `(h,k,r²),(-h,k,r²),(h,-k,r²),(-h,-k,r²),(h,k,r)` reflects the actual two sign substitutions and radius squaring. It is explicitly an authored complete bank, not a falsely recovered source profile. Its four errors are method-derived for all three number forms. No learner-facing distractor diagnosis is added.

## 4. Reusable masks, calculations and constraints

Prompt `![]({diagram})` then fixed “What is the equation of the circle given above?”; blank prompt retains the standard-form instruction and field placeholder, with restored diagram. Raw stripped blank's prompt stays fixed incomplete evidence. Changed diagrams use the exact sampled parameters, labels and selected radius orientation. Unchanged source geometry reuses the original hashed raster. See `plot-extraction.md`.

Source solution masks replace **complete** final equations, complete unsimplified substituted LHS, center tuple, radius equality and squared-radius expression. They preserve source paragraphs and the complete aligned sequence; replacements of bare numbers never occur. Signed terms conditionally group negative coordinates, rational radii use parenthesized squares, and zero shifts simplify only in the final row. The raw q-117081 brace style and blank conclusion are separate structural slots. All slots evaluate through normal parameterized generation, never a branch returning the source answer payload. Normal solutions use the same common prose and three structural rows plus the blank conclusion.

Raw source APIs: `generate('easy', parameters=..., profile='raw:q-ID')` reproduces omissions, exact prompt/solution and complete bank. `completed:q-ID` makes absent information explicit and labels inference/repair in metadata. `q-ID` is also an explicit completed source-bank profile. An authored call without a source profile uses normal level guards; these are detailed in `classification.md` and individual entrypoint comments. Every input value must be finite exact real; normal authored values are rational. Integer observed profiles do not silently accept number-form escalation.

Correct values are calculated first, then the complete bank. SymPy `Poly(..., extension=True)` constructs the field from the entire displayed expression, including any unsquared sqrt(r) distractor, and checks whole equations under nonzero scalar equivalence. Unknown/incomplete parameters, wrong level bounds and invalid profiles fail, with no explicit-input resampling.

Content identity includes version, actual displayed prompt, fixed solution, sorted complete bank, field type, difficulty presence/value and correct designation presence/value. Mathematical fingerprint contains the center, positive squared radius and assessed information/response, excluding orientation, bank and notation aliases. Seed changes only shuffle owned radio choices and cannot change fixed-instance identity. Generation metadata retains full provenance, dependencies, actual exact domain, recipes, inference/repair flags and plot metadata outside learner content.
