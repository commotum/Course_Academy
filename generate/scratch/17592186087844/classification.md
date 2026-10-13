# Classification

Capture: database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The unmodified capture wrapper is [source.json](source.json); owning topic 807 context and linked lesson activity are preserved beside it. There are **13** practice questions (not 14), all rated. Canonical e-5301 is contextual evidence, excluded from practice counts.

| Level | Source IDs | Field/layout | Structural templates | Plots |
|---|---|---|---:|---|
| easy | q-80679, q-80680, q-6912 | 2 radio; 1 fieldless | 3 | none |
| moderate | q-39795, q-113525, q-113523, q-278551, q-270003, q-80676, q-113527 | 4 radio, 2 blank, 1 fieldless | 6 | none |
| hard | q-4694, q-270004, q-4698 | 1 radio, 1 blank, 1 fieldless | 3 | none |

The 12 structural templates use 13 separately retained source masks: q-39795 and q-113525 share the GCF/discriminant structure, with distinct complete banks and a source-specific stray factor. Easy distinguishes a displayed denominator equation/discriminant, an inline equation/discriminant without a separate denominator-setting paragraph, and a positive quadratic without discriminant arithmetic. Moderate distinguishes GCF, grouping with a factorable linear numerator, grouping with a nonunit leading quadratic and constant numerator (blank), grouping with linear numerator (radio or blank), and grouping with difference-of-squares numerator. Hard distinguishes difference of cubes with linear numerator, scaled difference of cubes plus difference-of-squares numerator (blank), and quartic GCF plus sum of cubes (fieldless).

Seven complete observed radio profiles have five choices each. Three observed blanks have one math answer fragment each. The raw public `original` profile preserves the absence of `:question/answer-fields` for q-80680, q-113523 and q-4698. `supported-observed` supplies independently derived five-choice radio completions only for those fieldless records, and repairs the q-39795 teaching typo. In normal `authored` generation all radio banks are complete authored operation banks with explicit zero-polynomial recipes; original raw profiles and opaque supported-observed radio banks are marked evidence-only and ineligible for learning; blanks retain their supplied `x=` fragment and matching placeholder. Correct refs are never inferred and counted as observed for missing fields.

## Curriculum boundary

Following `:activity/first-step` and then `:step/next` gives Introduction → basic rational vertical asymptotes (87842) → common-factor asymptotes (87843) → **this KP** (87844) → common factors with complex roots (87845). Pull array order is not used. Prerequisites explicitly include discriminants, sums/differences of cubes and further GCF factoring. The topic also precedes locating holes. Thus this generator always has a negative-discriminant quadratic denominator factor and coprime numerator/denominator. Canceled holes and entirely real denominator roots belong to siblings and are rejected.

All three difficulty levels are observed; no missing-level assignment is invented. Authorship extends parameter domains and banks within each observed workload, plus supported fields for fieldless captured examples. Easy evaluates one familiar quadratic discriminant (or recognizes positive squares). Moderate performs one GCF/grouping and isolates exactly one real linear factor. Hard uses a cube identity, possibly with outer GCF and difference-of-squares numerator, then excludes the quadratic via its discriminant. Variations within levels are unordered alternatives, not a progression.

## Anomalies

q-39795 factors the denominator as `x(x²+x+1)` but says “Solving 2x=0.” Its root is still correct, but the stated factor does not match the factored polynomial. Raw evidence and `original` replay preserve it. All supported normal output changes only this equation to `x=0`. Raw exact solution count and supported exact solution count are reported separately. No formatting repair is inferred from JSON escaping: decoded source backslashes are standard single TeX commands. No source plots occur in these questions.
