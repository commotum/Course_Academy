# Template extraction

The backbone is defined before coefficient bounds. There is no evaluation target: all requests ask for the entire derivative function in x. Names f,g,h,y are preserved from their supplied function; q-28551's incorrect h label is repaired to y. Names and random option ordering do not contribute mathematical variety.

## 1. Specific originals

| Template key | Original | Supplied operand | Requested order | Ordered source row counts |
|---|---|---|---|---|
|polynomial_reciprocal_radio|q-28546|3x²−5x+3/x|3|rewrite2; first2; second2; third3|
|cubic_reciprocal_radio|q-28550|x³/4−4/x²|3|solution absent; authored first2/second2/third2|
|quadratic_constant_reciprocal|q-28551|7x²−1+1/(2x)|3|rewrite2; first3; second3; third3|
|polynomial_reciprocal_blank|q-310170|4x²+6x−2/x|3|rewrite2; first2; second2; third3|
|log_radical|q-104294|2ln x−8√(x⁵)|3|first3; second3; third3|
|cos_log|q-310171|cos x+ln x|4|first2; second3; third2; fourth3|
|polynomial|q-343075|2x⁵−3x³|3|first2; second2; third2|
|quotient_sum|q-343086|(x⁵−x²+x)/(4x²)|3|rewrite2; first3; second2; third3|
|exponential_reciprocal|q-343089|3eˣ−1/(3x²)|3|first3; second2; third3|
|log_polynomial|q-343114|2ln x+x⁴|3|first3; second2; third3|
|sin_exponential|q-343120|sin x−eˣ|4|first2; second2; third2; fourth2|

`source.json` preserves every original prompt, field, choice, feedback attribute, correct designation, solution and omission. `source-cases.json` contains exactly these 11 MA originals; independent-inventory.json is empty with the same wrapper provenance. Raw replay uses generate(level, parameters={'source_id': original_id}, profile='raw-evidence') and returns the complete original Pull record with evidence_only=true/eligible_for_learning=false. That explicit profile is not normal generation.

## 2. Shared mathematical pattern

Rewrite reciprocals/radicals or a quotient into powers when the source does, then differentiate each term successively exactly three or four times. The formal d/dx input at stage n is the full previous derivative, not the original operand or a higher derivative. Preserve the named target and any final negative-power-to-fraction row. The normal solution keeps every source prose paragraph and row position, changing complete mathematical components from one coefficient vector. An authored solution fills only q-28550's absent worked solution. Field shape follows each family; q-28551's authored blank is separately labeled.

## 3. Components and complete observed banks

Let a,b,c multiply the original first, second and third displayed terms independently; at every source replay a=b=c=1. Denominators and exponents remain fixed. The following lists are the full observed banks in captured order, including all errors; these are algebraic patterns, not claims that a learner misconception is uniquely known.

- q-28546: [−6c/x³, **−18c/x⁴**, +6c/x³, −6c/x⁴+6a, +18c/x⁴]. Recipes: shortened order/factor; correct; its sign counterpart; retained quadratic second derivative plus incomplete reciprocal factor; final-sign error. One complete observed profile. All 4 distractors replay.
- q-28550: [3a/2+24b/x⁴, 3ax/2−24b/x⁴, 3ax/2+24b/x⁵, 3a/2−96b/x⁵, **3a/2+96b/x⁵**]. These are the exact observed incomplete-chain/mixed-order/retained-x/missed-factor/sign patterns. The final option is independently inferred correct; original correct designation is absent. All 4 inferred distractors replay, but this does not create an original designation.
- q-104294: [−6a/x³−60bx, 4a/x²−60bx, −6a/x³+15b/√x, a/x²−b/√x, **4a/x³−15b/√x**]. Compound altered-factor/power patterns remain interpretation-limited. One complete observed profile, all 4 distractors replay.

Scalar source masks alone cannot establish all historical error intentions. Normal radio defaults use a distinct complete authored-errors profile: correct nth derivative; the (n−1)st derivative; the (n−2)nd derivative; negated nth derivative; omission of the first surviving term contribution (or omission of the reciprocal's previous-stage contribution when only it survives). These are operations from the displayed method. Choose the whole profile before coefficients, derive all 5 choices and reject the whole instance on any equivalence. No random +1 perturbations, pooled first-valid recipes or hybrid banks are served. +1 is used only as a required grading negative control.

All7 observed blank values are reproduced; q-28551's authored blank is not counted as observed. Blank fields retain the exact RHS expression response contract and no invented learner feedback. No source answer feedback is present; raw replay preserves every attribute and its absence.

## 4. Reusable masks and slots

Fixed: original expression structure; x as independent variable; three derivatives at easy/moderate, four at hard; denominator constants/powers; exponent5/2 for the radical; all operator inputs, rewrite locations and ordered row profile; supplied function name; original field shape and bank size. Altering n changes stage count and would violate this backbone, so n is not a parameter. New composition, arbitrary n, point evaluation, variable inner trig frequency and product/quotient-rule branches are excluded.

Slots: one nonzero integer multiplier per complete original additive term, range−6..−1 or1..6, independently sampled. Each slot controls its full prompt term, each surviving derivative contribution, rewrite representation, all bank recipes and any final fraction. Quotient_sum's three scales control its three numerator terms while preserving denominator4x² and sum rewrite. Signs may change with the same term count, exponent and reasoning stages. These bounds multiply observed small coefficients with an arithmetic ceiling of six; no new differentiation method or additional operation stage is added. Function letters and source IDs are not slots.

Domains: log/radical functions require x>0; reciprocal/quotient functions require x≠0; polynomial and sine/exponential functions permit every real x. The positive x CAS assumption simplifies radical identities only on their stated domain; rational/polynomial derivatives are exact identities on their full source domain.

Capacity counts vary only coefficients surviving in the requested derivative, with all killed coefficients held at1. This deliberately excludes seed, label, option order, bank profile and coefficients erased by differentiation. Independent boundary sweeps still exercise every slot's full signed scale domain. See validation.json for the enumerated deduplicated task counts, complete-bank rejections and actual slot coverage. Different easy/moderate source labels are preserved rather than retroactively imposing a new workload ranking.

Every template is a source family with a conservative authored coefficient extension, not a newly recovered family. Every source solution is compared in full after listed presentation/name repairs, including formal-operator operands and all intermediate row values. Independent negative controls corrupt target order, target function name, operator input and a control character. Native grading covers canonical and unreduced equivalent blank entries, ordinary0/1/+1 wrong entries and every owned radio option for all successful bounded tasks. Malformed entries are separate diagnostics.
