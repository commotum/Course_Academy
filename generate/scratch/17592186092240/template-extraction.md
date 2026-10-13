# Template extraction

source-components.json contains every original prompt, solution, field, choice, value and canonical designation; source-questions.md gives readable originals. Each supported source has a complete blank bank, so no distractor recipes are required. Radio banks are separately recorded with their observed formulas and unresolved interpretations in classification.md; they are never pooled into the supported blanks.

For f(x)=scale*f_source(x), point x0, y0=f(x0), m=fprime(x0), m!=0, the normal has slope -1/m and equation L*x+L*m*y=L*(x0+m*y0). The fixed source prompt gives plus for positive m or minus for negative m; field-1 expects abs(L*m), field-2 expects the signed RHS. L=8 only for q-342190 and L=1 otherwise. Polynomials allow all real x; this bounded sampler uses only specified nonnegative points. Reciprocal and cube-root variants use positive x to avoid poles and branch ambiguity. Signed coefficients, negative y0 and negative RHS are retained. m=0 and non-finite slopes are rejected.

Scale=1 and original x0 replay every original bank and exact prompt. Proposed scale 1..30 and additional points are narrower bounded policies, not an inferred full source domain. Polynomial-plus has distinct cubic, quadratic-plus-constant, and degree-6/degree-3 solution profiles. Reciprocal-minus has negative powers; polynomial-minus uses the observed x0=0; radical-scaled-plus preserves rational coordinates and fixed multiplier 8.

Variants retain the shared original instructional sentences and derivative/tangent/normal/point-slope/rearrangement sequence. Algebra lines are compacted into one final rearrangement, so solution fidelity is structural, not byte-identical. All differences are shown in review.md. No feedback or choice fields are added to blanks.
