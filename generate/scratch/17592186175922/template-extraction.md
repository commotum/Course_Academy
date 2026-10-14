# Four-stage extraction

## 1. Particular source instances

Write the given line as y=ax+c and the required point as (u,v). Let m=-1/a and b=v-mu. Source prose uses named lines l1/l2, the negative reciprocal rule, and point-slope form. The source line's intercept c matters to the plotted presentation but not the assessed calculation.

| Source | a,c | (u,v) | m,b | Captured solution sequence |
|---|---|---|---|---|
| q-213914 | 3,2 | (0,2), labelled in raster | -1/3,2 | absent; completion uses easy prose |
| q-44604 | 1/2,0 | (-4,10), dashed labelled guides | -2,2 | absent; completion uses point-slope prose |
| q-237031 | 4,-6 | (8,-3), text | -1/4,-1 | Let l1/l2; reciprocal; formal point-slope; substitute; distribute with y+3; collect |
| q-237193 | -4,-3 | (4,2), dashed labelled guides | 1/4,1 | reciprocal; formal point-slope; substitute; distribute; collect |
| q-237197 | 2/5,-2 | (6,-1), text | -5/2,14 | Let; reciprocal; formal; substitute; distribute with y+1; collect; Therefore b=14 |
| q-44337 | 2,-1 | (0,6), raster intercept label | -1/2,6 | reciprocal; marked y-intercept; slope-intercept equation |
| q-44606 | 1/2,-3 | (-1,5), text | -2,3 | Let; reciprocal; formal; substitute; simplify x-(-1); distribute; collect; Therefore b=3 |

Blank values are RHS expressions `-x/4-1`, `x/4+1`, and scalar `14`. q-213914 requests a RHS expression but captures no answer value. No source blank asks for the whole equation including `y=`. The equation radios do require the complete `y=...` object.

## 2. Generalized backbone

Known slope in an explicit slope-intercept equation; take its negative reciprocal. Combine with an annotated graph intercept (easy), annotated non-axis graph point (moderate), or supplied text point (hard). For a non-axis point, use the formal point-slope equation, concrete substitution, optional negative-x simplification, distribution while retaining the left side, and final collection. Intercept tasks then retain the final Therefore b=... sentence. Every instance has one fixed worked solution independent of learner response.

## 3. Complete bank components and mappings

Every captured choice is mapped below in source order. These are parameterized structural recipes, not a claim to recover the original authoring algorithm. Original answer IDs, exact bytes and field ownership remain in source.json.

| Source | Source value | Parameterized recipe | Status |
|---|---|---|---|
| q-44337 | y=2x+6 | y=ax+b | observed, plausible unchanged slope |
| q-44337 | y=-1/2x+6 | y=mx+b | observed correct ref |
| q-44337 | y=1/2x | y=(1/a)x | observed; sign and intercept omission |
| q-44337 | y=-6x-2 | y=-bx-a | observed; opaque swapped-role structure |
| q-44337 | y=-2x+6 | y=-ax+b | observed negative given slope |
| q-44604 | y=-2x+2 | y=mx+b | mathematically inferred correct; no captured ref |
| q-44604 | y=-1/2x+8 | y=-ax+(v+au) | observed, slope negation with point substitution |
| q-44604 | y=-2x-4 | y=mx+u | observed x-coordinate in intercept position |
| q-44604 | y=1/2x+12 | y=ax+(v-au) | observed given-slope substitution |
| q-44604 | y=2x+12 | y=(1/a)x+(v-au) | observed mixed reciprocal/given-slope computation |
| q-44606 | -2 | m | observed slope supplied as scalar intercept |
| q-44606 | 1 | -u | observed; opaque coordinate-only structure |
| q-44606 | 3 | b=v+u/a | observed correct ref |
| q-44606 | -1 | u | observed; opaque coordinate-only structure |
| q-44606 | 5.5 | v-au | observed given-slope substitution |
| q-237031 | -1/4x-1 | mx+b, RHS only | observed correct |
| q-237193 | 1/4x+1 | mx+b, RHS only | observed correct |
| q-237197 | 14 | b | observed correct |
| q-213914 | absent | mx+b=-1/3x+2, RHS only | inferred completion, not a matched captured value |

Default complete banks are chosen before parameters. Graph-intercept radio: `(m,b), (a,b), (1/a,b), (-a,b), (m,c)`. Graph-point radio: `(m,b), (a,v-au), (1/a,v-u/a), (-a,v+au), (m,v+mu)`. Scalar-intercept radio: `b, v-au, v-u/a, v+au, -mu`. The final scalar recipe omits the point's y-coordinate; these operations all arise from the displayed method. Reject the whole instance if any two options are equivalent, including two wrong options; never replace individual options from a pool. Historical profiles remain public but evidence-only, including completed historical banks.

## 4. Reusable slots, constraints and stages

`a,c,u,v` are complete component slots. `extracted-masks.json` records full mathematical-atom masks, not numeral replacement. All dependent values m,b, prompt references, prose point/slope claims, aligned rows and Therefore b sentences are derived. A negative u adds the source-supported x-(-u) simplification stage; a negative v remains grouped at substitution then becomes y+abs(v) at distribution. No CAS collapse removes these teaching operations.

All explicit inputs and samplers require nonzero rational a, reduced numerator magnitude <=5, denominator <=5; integer c,u,v with absolute value <=12; absolute final b<=24. Easy point has u=0. Moderate point requires u,v both nonzero; moderate blank's known a is integer. Hard text RHS likewise has integer a; hard intercept normal fields have a proper fractional value (noninteger). Nonzero v and b and abs(a)!=1 preserve meaningful normal workload. Hard supplied points have u!=0. Source evidence permits the original number forms and missing attributes.

Default sampler bounds are narrower: c from -8..8; easy a from signed integers 2..5 and nonzero v from -8..8; moderate blank/hard RHS the same integer a, u from nonzero -12..12 with u/a integral, v from nonzero -10..10. Moderate radio a from signed unit fractions with denominator2..5 and the same point bounds. Hard intercept a from signed reduced noninteger fractions with numerator magnitude1..5/denominator2..5, same point bounds and integral u/a. These are comparable-workload variations grounded in the source negative reciprocal and point-slope steps, not new curriculum branches. Explicit normal inputs retain each family’s slope number form and integral distributed offset u/a; c,u,v may vary within the stated guard bounds. Invalid inputs are rejected without silently changing them.

`domain-counts.json` enumerates the default samplers: 128 easy tasks, 3344 moderate tasks, and 5940 hard tasks. These exclude bank/profile/response aliases and incidental c. Mathematical fingerprints use the known slope, required point, and graph-intercept/graph-point/text-point information role. Content identity independently uses actual displayed prompt, complete bank, fixed solution, version and actual difficulty/presence. Seeds and option order do not alter it; displayed changes do.

Source omissions: q-213914 lacks choices, correct ref, solution and rating; q-44604 lacks correct ref, solution and rating. Raw public profiles omit each attribute individually. Completed profiles provide independently derived answers/solutions and authored ratings. Missing captured designations never count as matched source correct refs. There are no decoded malformed TeX bytes in these source strings; ordinary punctuation inside source math is retained. Normal q-213914 adds paragraph separation before the supplied y= expression, a layout clarification only. No mathematical source error was found.
