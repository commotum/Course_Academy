# Four-stage extraction

## 1. Specific source descriptions

q-54285: native red increasing line crosses (0,2), visibly passes (4,4), unit grid with every second coordinate labeled. Three claims y=x+1/2, y=x/2+2, y=x/2+1/2; only II matches the whole line. Current prompt adds Select all that apply and bold Roman bullet labels. Three checkbox fields I/II/III each own false and true answers; correct values false/true/false. Unrated. Captured one-sentence solution reads intercept/point/slope and concludes II; no solution image or feedback.

q-59732: native descending red line crosses (0,4),(4,0). Claims x+2y=4, y=2-x, y=4-x; only III. Three current checkbox fields I/II/III, false/true options; key false/false/true. Unrated. Compact solution reads both intercepts and concludes y=4-x, III; no solution image or feedback.

q-71837: steep red native line crosses (0,6),(2,0). Three claims y+3x=6, y/3+x=2, y=-3x+6 are all equations of exactly the same line. One radio field selection; complete values II and III only, I only, I, II and III, I and III only, III only; key I, II and III. Hard. Solution chooses two intercepts, shows marked A/B plot, explains point substitution criterion, checks each equation. Operative numeric row counts4/6/5: substitute/evaluate both points, retaining the intermediate zero-term sums for equationII and the -6+6 row for equationIII. Conclusion states all three. One fixed solution; feedback absent.

q-54293: red native line crosses (0,2),(4,0). Claims y=-2x+1/2, y=-x/2+2, y=x/2+2. Only II. Radio selection bank II only, II and III only, I only, I and II only, III only; key II only. Hard. Same intercept-reading and point-testing explanation. Row counts2/5/5: first wrong claim rejected at A, true claim checks both points including -2+2 row, opposite-slope claim fails at B including2+2 row. Source first row substitutes -1(0) instead of -2(0); it still has the same numeric residual because x=0, but is an operand error. Public raw profile preserves this single masked typo stage with an explicit source-error/ineligible flag. Normal profile repairs to -2(0). Remaining prose including source spacing and grammatical omissions is unchanged.

## 2. Generalized backbone

Given a plotted straight line and three complete supplied linear equations, recognize every equation representing the entire line. Read two distinct graph points, substitute actual coordinates and compare equalities. A single failed point excludes a claim; two distinct true points suffice for a supplied linear equation. The response is a complete subset, represented by three claim checkboxes or a radio choice naming the complete subset. Equivalent equations can be distinct true claims. Radio choices name distinct subsets even when the underlying equations are equivalent.

## 3. Every component and bank mapping

The full original field/answer records and exact source wording are retained in source.json; source-cases maps all four to explicit parameters and original profiles. No choice is omitted.

|Profile|Parameters|Claim I recipe|Claim II recipe|Claim III recipe|Truth|
|---|---|---|---|---|---|
|q-54285|b=2,t=4,c=b/t|y=x+c|y=cx+b|y=cx+c|F,T,F|
|q-59732|b=t=4|x+2y=b|y=b/2-x|y=b-x|F,F,T|
|q-71837|b=6,t=2,k=b/t integer|y+kx=b|y/k+x=t|y=-kx+b|T,T,T|
|q-54293|b=2,t=4,c=b/t|y=-bx+c|y=-cx+b|y=cx+b|F,T,F|

Original q-54285 and q-59732 each have three separate fields with both false/true values; every field-owned yes/no option is preserved. The statements are the claims; false/true options are not equation distractors. The full q-71837 radio bank represents subsets {II,III},{I},{I,II,III},{I,III},{III}. Full q-54293 bank represents {II},{II,III},{I},{I,II},{III}. All subsets are distinct and the correct subset equals the entire true-claim set. No source bank is opaque or mathematically ambiguous; the sole malformed operative stage is explicitly tracked. No arbitrary polynomial fit, unrelated numeric perturbation or pooled choice selection is used.

## 4. Reusable masks and allowed slots

Observed profiles retain exact prompt structure, bank cardinality, field layout, point roles, operation order and fixed solution sentences. q-71837 varies integer k=2..5,t=1..4,b=kt. Source formula construction preserves three scaled-equivalent claims and its4/6/5 rows at changed parameters. q-54293 varies b=1..6,t in2,3,4,6,8; c=b/t. The whole wrong swap and sign-reversal profiles are derived before sampling. EquationI still stops after A; equationII checks both points, retaining b-b; equationIII checks both points, retaining b+b. q-54285 varies b=2..5,t=2b; q-59732 varies b=t in2,4,6,8. These conservative observed-profile extensions do not establish missing original ratings. Raw profiles use the same recipes and optional single typo mask, never a copied literal question.

Authored default profiles are separately named authored-easy/moderate/hard, with domains/policies in classification.md and code. Easy claims are y=mx+b, y=-mx+b, y=mx-b. Moderate claims y=bx+m, y=mx+b, y=-mx+b. Hard claims y=mx+b, y=x/m+b, mx-y=-b. Complete profiles are method-derived; parameters cannot collapse slopes or intercepts to zero or make the swapped candidate true. Fixed solutions use actual coordinate substitution, evaluated rows and equation-by-equation conclusions. There is no feedback-specific diagnosis. Every solution is independent of the learner's response.

Mathematical task fingerprints use normalized graph slope/intercept, not equation spelling, profile, option order, plot bounds or UUID. Presentation identity includes actual prompt/solution, whole banks and contract. Numerical aliases are normalized before identity construction. Changed seeds shuffle only the radio bank, retaining field-owned answer UUIDs and question UUID.
