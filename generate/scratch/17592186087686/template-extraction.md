# Template extraction

## 1. Specific observed instances

q-215719 says `The lines $y =-7x + 5$ and $y = mx + 2$ are parallel. What is the value of $m$?$m =$` followed by `{{field-1}}`. The negative coefficient is an integer; the intercepts differ. One blank field is present, but no choices, correct ref, difficulty, or worked solution is present.

q-215726 has the identical prompt mask and single blank, with `y =-\frac{1}{8}x - 4` and `y = mx + 6`. The negative unit-fraction coefficient introduces fraction/sign reading; no additional algebra is needed. The same four assessment attributes are absent.

q-44314 says `The lines $y = 2x + 3$ and $y = mx + 9$ are parallel. The value of $m =$`. It owns a selection radio field and values 3, 3/2, 1, 2, 2/3 (EDB ordering differs from the widget order). Its difficulty, solution, and correct ref are absent. It has no placeholder because the choice widget follows the prompt. Parameter masks preserve the literal spacing and adjacent question/answer fragment in raw and completed profiles.

## 2. Shared mathematical purpose

For distinct lines already written y=ax+b and y=mx+k, compare x-coefficients. Parallelism gives m=a immediately. No isolation, equation solving, points, diagram reading, or perpendicular rule is required. The expected response is only the coefficient fragment. The canonical example provides the teaching stages: same-slope rule; read each x-coefficient; list both slopes; conclude equality.

## 3. Components and complete observed bank

| Slot | q-215719 | q-215726 | q-44314 |
|---|---|---|---|
| a (slope) | -7 | -1/8 | 2 |
| b (given intercept) | 5 | -4 | 3 |
| k (unknown-slope intercept) | 2 | 6 | 9 |
| answer shape | scalar blank | scalar blank | scalar radio |
| mathematically inferred coefficient | -7 | -1/8 | 2 |
| captured correct designation | absent | absent | absent |
| captured solution | absent | absent | absent |

Complete historical scalar bank profile:

| Original answer DB ID | Original value | Parameterized expression | Evidence status |
|---|---|---|---|
| 17592186085711 | 3 | b | possible intercept confusion, intent unproved |
| 17592186085712 | 3/2 | b/a | ratio of visible intercept/coefficient, intent opaque |
| 17592186085713 | 1 | 1 | fixed observed scalar, intent opaque |
| 17592186085714 | 2 | a | inferred correct coefficient |
| 17592186085715 | 2/3 | a/b | ratio of visible coefficient/intercept, intent opaque |

All five expressions replay together through `raw_scalar_radio`; the public completed version supplies the inferred key while retaining the entire bank. Both scalar historical profiles are explicitly **evidence-only, ineligible for learning** because a single bank cannot establish distractor authoring intent. They are not hidden source samplers: a,b,k are actual public parameters, the prompt changes and all five expressions recompute when those parameters change. The bank rejects b=0 or any equivalence/collision as a whole. It never fills missing members from a candidate pool. No exact original correct ref existed to match.

Normal authored radio bank is the fixed complete tuple a, -a, b, k, 1/a: reading the actual coefficient, reversing its sign, mistaking either intercept for slope, and reversing the slope ratio. The last operation is grounded in slope rise/run recognition from prerequisites, not a perpendicular rule. The same complete tuple is used for authored line-choice slopes, with each equation's intercept k; the correct line y=ax+k is distinct from the target y=ax+b. No learner-facing distractor diagnosis is added. Whole-instance rejection excludes equivalent slopes/options and coincident correct lines. This is a separately labeled authored bank, not a recovered source bank.

## 4. Reusable masks, domains and solutions

Observed coefficient_blank:

`The lines ${source_line(a,b)}$ and ${source_line(m,k)}$ are parallel. What is the value of $m$?$m =$\n{{field-1}}`

Observed coefficient_radio:

`The lines ${source_line(a,b)}$ and ${source_line(m,k)}$ are parallel. The value of $m =$`

Source spacing is controlled by complete equation components, never arbitrary global replacement. Fixed components include variable x/y/m, same-slope criterion, response shape and field key. Sign and exact rational formatting are conditional; integers omit fraction wrappers, negative numerators put minus before the fraction. Raw public profiles omit solution/rating/keys and omit blank choices exactly. Enum ident maps become local enum strings; generated UUIDs replace source UUIDs, and source DB identity attributes remain evidence. All original non-UUID attributes, including presence, are verified per source.

Completed original and normal coefficient solutions use the canonical sentences verbatim, then the canonical two slope bullets and final equality. They adapt only the complete line/coefficient slots and bullet ordering to the given equation order. No captured practice solution exists, so practice solution fidelity has denominator zero; canonical-stage reuse and generated-stage correctness are separate tests. Authored line-choice solutions adapt “Both lines” to “All the lines”, list the actual target and each complete answer line with its slope, and identify the unique equal-slope distinct line.

Explicit and sampled parameters have the same guards: integer intercepts -12..12, b≠k; easy a a nonzero integer -12..12, moderate a=±1/d for d2..12, hard a=±n/d with n,d2..12 coprime and n>1. Opaque historical profiles are restricted to the authored tier of the original. Complete radio banks additionally require all five slopes distinct; explicit invalid instances raise ValueError and never resample.

Task fingerprints retain only the actual coefficient and number-form workload for both coefficient-fragment layouts: changing the two intercepts cannot change the operation m=a. They exclude the scalar candidate bank, profiles, seed, notation aliases and option order. For line-choice identification, they retain the target slope and the complete unordered compared slope set, since those define the comparison; intercepts serve distinctness only and do not create new mathematical tasks. Geometric slope is read from normalized y=mx+b, equivalent to a*x-y+b=0 with the y coefficient fixed at -1; rational/scalar/sign notation aliases normalize before fingerprinting. Content identity separately retains actual complete line equations, both offsets, prompt, fixed solution, displayed bank, answer shape, and difficulty. Thus changed offsets change presentation identity while leaving coefficient-read task identity fixed.

The finite coefficient-read domains contain24 integer,22 unit-fraction and136 reduced nonunit rational tasks. Signed coefficient/magnitude/denominator changes alter the actual assessed value; intercept variation is incidental and is not counted as mathematical variety. Both coefficient_blank and coefficient_radio share this finite task domain rather than counting response-layout aliases twice. This narrow read-off skill honestly has finite variety.

Authored line-choice comparison has a larger finite domain from actual unequal compared slope sets:22 eligible easy target slopes (±1 cause reciprocal collision), each with253 eligible unordered integer distractor pairs =5,566 tasks;22 moderate targets each with276 pairs =6,072;136 hard targets each with300 pairs =40,800. The two additional integer candidate slopes arise from the displayed intercept-confusion recipes and are part of the actual compared bank. Duplicate/equivalent slope sets, ordering changes and all distinctness-only line offsets are deduplicated. These counts are independently enumerated by validation. Supported normal totals are5,590 /6,094 /40,936 across the coefficient-read and line-choice demand; no symbolic algebra or new mathematical method was added merely to increase variety.
