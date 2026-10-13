# Template extraction at basis 1356


## Stage 1 — specific source descriptions

The per-question capture, exact field type, full bank and supplied worked solution remain in `source-cases.json`. The original scalar/asymptote equations below are complete mathematical sets of vertical lines. Blank values are scalar equation RHS fragments. Source solutions begin with the same rational-function rule, optionally factor the function, set the noncancelled denominator to zero, list the distinct real solutions, and conclude with the asymptote equations. q-39793 omits the unnecessary factoring-function row because its denominator is already supplied in factored form. q-278534 has four addition stages before its zero-product equation. q-269955 factors numerator as 3x(2x+3), with denominator (x-2)(x+2) in the function row and (x+2)(x-2) in the equation row; this ordering is preserved. q-278249 retains its repeated factor x² but reports zero only once. q-39790 preserves its nonunit rational root.

## Stage 2 — shared pattern

Determine the distinct real roots of the denominator after checking numerator/denominator factorization. In this KP all captured functions have no common factor and only real rational denominator roots. Existing numerator zeroes are distractor candidates, not poles; independent validation computes poles after cancellation anyway. The hard sum must first be combined using a common denominator. The elementary operation is unchanged across every within-level variant.

## Stage 3 — component and complete-bank map

Every captured field/choice follows. The evidence transform is a positive dilation r ↦ s·r of the complete set, preserving types, singleton text, empty-set statements, counts and source co-occurrence. These source radio banks are evidence-only, not recovered mistake recipes. Numeric scalar options underdetermine error intent; in particular q-6908's four unrelated pairs cannot justify a default learner operation bank. No arbitrary scalar fit is promoted. The whole observed bank is selected by source profile before dilation. All resulting sets must be pairwise distinct, with exactly one correct full set; otherwise reject the whole instance.


### q-39796

Calculate the vertical asymptotes of $f(x) = \frac{2}{2 - x} + \frac{3}{2 + x}$.

Numerator: `10 - x`; denominator: `(2 - x)*(x + 2)`; actual reduced pole set: `(-2, 2)`. Public mask/profile: `observed_39796`.

Field `selection`, `:answer-field.type/radio`.

- `:answer.type/math` / `x =-2, x = 0, x = 2`; complete evidence recipe `(-2*s, 0, 2*s)`; no original designation.

- `:answer.type/math` / `x =-2, x = 2`; complete evidence recipe `(-2*s, 2*s)`; no original designation.

- `:answer.type/math` / `x =-2, x = 1`; complete evidence recipe `(-2*s, s)`; no original designation.

- `:answer.type/text` / `$x = 2$ only`; complete evidence recipe `(2*s,)`; no original designation.

- `:answer.type/math` / `x = 0, x = 2`; complete evidence recipe `(0, 2*s)`; no original designation.

Supplied worked solution: missing; authored completion with shared sentences and full applicable stages.

### q-4629

Calculate the vertical asymptotes of $f(x) = \frac{3x^{2} - 12x}{x^{2} - 2x - 3}$.

Numerator: `3*x*(x - 4)`; denominator: `x**2 - 2*x - 3`; actual reduced pole set: `(-1, 3)`. Public mask/profile: `observed_4629`.

Field `selection`, `:answer-field.type/radio`.

- `:answer.type/text` / `$x = 3$ only`; complete evidence recipe `(3*s,)`; no original designation.

- `:answer.type/math` / `x = 1, x = 4`; complete evidence recipe `(s, 4*s)`; no original designation.

- `:answer.type/math` / `x =-1, x = 3`; complete evidence recipe `(-s, 3*s)`; no original designation.

- `:answer.type/text` / `No vertical asymptotes`; complete evidence recipe `()`; no original designation.

- `:answer.type/text` / `$x =-1$ only`; complete evidence recipe `(-s,)`; no original designation.

Supplied worked solution: missing; authored completion with shared sentences and full applicable stages.

### q-6908

Determine the vertical asymptotes of $f(x) = \frac{1}{x^{2} + 6x - 16}$.

Numerator: `1`; denominator: `x**2 + 6*x - 16`; actual reduced pole set: `(-8, 2)`. Public mask/profile: `observed_6908`.

Field `selection`, `:answer-field.type/radio`.

- `:answer.type/math` / `x = 3, x = \frac{1}{2}`; complete evidence recipe `(s/2, 3*s)`; no original designation.

- `:answer.type/math` / `x =-12, x = 3`; complete evidence recipe `(-12*s, 3*s)`; no original designation.

- `:answer.type/math` / `x =-5, x = 1`; complete evidence recipe `(-5*s, s)`; no original designation.

- `:answer.type/math` / `x =-2, x = \frac{1}{4}`; complete evidence recipe `(-2*s, s/4)`; no original designation.

- `:answer.type/math` / `x =-8, x = 2`; complete evidence recipe `(-8*s, 2*s)`; no original designation.

Supplied worked solution: missing; authored completion with shared sentences and full applicable stages.

### q-278249

In **ascending order**, the vertical asymptotes of $f(x)=\frac{x+2}{{x}^{3}-3{x}^{2}}$ are

$x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

Numerator: `x + 2`; denominator: `x**2*(x - 3)`; actual reduced pole set: `(0, 3)`. Public mask/profile: `observed_278249`.

Field `field-1`, `:answer-field.type/blank`.

- `:answer.type/math` / `0`; complete evidence recipe `(0,)`; original correct designation.

Field `field-2`, `:answer-field.type/blank`.

- `:answer.type/math` / `3`; complete evidence recipe `(3*s,)`; original correct designation.

Supplied worked solution: full raw prose and all displayed stages preserved, including root ordering and optional factoring-row omission.

### q-39790

Calculate the vertical asymptotes of $f(x)=\frac{x+1}{2{x}^{2}+x-3}.$

Numerator: `x + 1`; denominator: `2*x**2 + x - 3`; actual reduced pole set: `(-3/2, 1)`. Public mask/profile: `observed_39790`.

No original fields; authored ascending scalar blanks are a presentation repair.

Supplied worked solution: full raw prose and all displayed stages preserved, including root ordering and optional factoring-row omission.

### q-269955

In **ascending order**, the vertical asymptotes of $f(x)=\frac{6{x}^{2}+9x}{{x}^{2}-4}$ are

$x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

Numerator: `3*x*(2*x + 3)`; denominator: `x**2 - 4`; actual reduced pole set: `(-2, 2)`. Public mask/profile: `observed_269955`.

Field `field-2`, `:answer-field.type/blank`.

- `:answer.type/math` / `2`; complete evidence recipe `(2*s,)`; original correct designation.

Field `field-1`, `:answer-field.type/blank`.

- `:answer.type/math` / `-2`; complete evidence recipe `(-2*s,)`; original correct designation.

Supplied worked solution: full raw prose and all displayed stages preserved, including root ordering and optional factoring-row omission.

### q-278534

In **ascending order**, the vertical asymptotes of $f(x)=\frac{2}{x-1}+\frac{1}{x+5}$ are

$x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

Numerator: `3*x + 9`; denominator: `(x - 1)*(x + 5)`; actual reduced pole set: `(-5, 1)`. Public mask/profile: `observed_278534`.

Field `field-2`, `:answer-field.type/blank`.

- `:answer.type/math` / `1`; complete evidence recipe `(s,)`; original correct designation.

Field `field-1`, `:answer-field.type/blank`.

- `:answer.type/math` / `-5`; complete evidence recipe `(-5*s,)`; original correct designation.

Supplied worked solution: full raw prose and all displayed stages preserved, including root ordering and optional factoring-row omission.

### q-39791

Determine the vertical asymptotes of $f(x)=\frac{3}{2{x}^{2}-8}.$

Numerator: `3`; denominator: `2*x**2 - 8`; actual reduced pole set: `(-2, 2)`. Public mask/profile: `observed_39791`.

Field `selection`, `:answer-field.type/radio`.

- `:answer.type/math` / `x=-\frac{1}{2},\,x=0`; complete evidence recipe `(-s/2, 0)`; original incorrect choice.

- `:answer.type/math` / `x=0,\,x=2`; complete evidence recipe `(0, 2*s)`; original incorrect choice.

- `:answer.type/math` / `x=-4,\,x=4`; complete evidence recipe `(-4*s, 4*s)`; original incorrect choice.

- `:answer.type/math` / `x=-2,\,x=0,\,x=2`; complete evidence recipe `(-2*s, 0, 2*s)`; original incorrect choice.

- `:answer.type/math` / `x=-2,\,x=2`; complete evidence recipe `(-2*s, 2*s)`; original correct designation.

Supplied worked solution: full raw prose and all displayed stages preserved, including root ordering and optional factoring-row omission.

### q-80669

Determine the vertical asymptotes of $f(x)=\frac{{x}^{2}+3x}{{x}^{2}-3x-4}.$

Numerator: `x*(x + 3)`; denominator: `x**2 - 3*x - 4`; actual reduced pole set: `(-1, 4)`. Public mask/profile: `observed_80669`.

Field `selection`, `:answer-field.type/radio`.

- `:answer.type/text` / `$x=4$ only`; complete evidence recipe `(4*s,)`; original incorrect choice.

- `:answer.type/text` / `The function has no vertical asymptotes`; complete evidence recipe `()`; original incorrect choice.

- `:answer.type/text` / `$x=-1$ only`; complete evidence recipe `(-s,)`; original incorrect choice.

- `:answer.type/math` / `x=-1,\,x=4`; complete evidence recipe `(-s, 4*s)`; original correct designation.

- `:answer.type/math` / `x=-3,\,x=0`; complete evidence recipe `(-3*s, 0)`; original incorrect choice.

Supplied worked solution: full raw prose and all displayed stages preserved, including root ordering and optional factoring-row omission.

### q-39793

Determine the vertical asymptotes of $f(x)=\frac{x}{(x+3)(x+1)(x-1)}.$

Numerator: `x`; denominator: `(x - 1)*(x + 1)*(x + 3)`; actual reduced pole set: `(-3, -1, 1)`. Public mask/profile: `observed_39793`.

Field `selection`, `:answer-field.type/radio`.

- `:answer.type/math` / `x=-1,\,x=1,\,x=3`; complete evidence recipe `(-s, s, 3*s)`; original incorrect choice.

- `:answer.type/math` / `x=-3,\,x=1,\,x=3`; complete evidence recipe `(-3*s, s, 3*s)`; original incorrect choice.

- `:answer.type/math` / `x=-3,\,x=-1,\,x=1`; complete evidence recipe `(-3*s, -s, s)`; original correct designation.

- `:answer.type/math` / `x=-1,\,x=1`; complete evidence recipe `(-s, s)`; original incorrect choice.

- `:answer.type/math` / `x=-1,\,x=-\frac{1}{3},\,x=1`; complete evidence recipe `(-s, -s/3, s)`; original incorrect choice.

Supplied worked solution: full raw prose and all displayed stages preserved, including root ordering and optional factoring-row omission.

## Stage 4 — reusable masks, domains, calculations

`observed_<source-number>` renders each complete source Markdown/value mask through expression slots: a polynomial P of degree d becomes s^d·P(x/s), each already factored linear component receives its dilated constant, and each printed root becomes s·r. Positive scale s is an integer 1–3, with every pole bounded by 24. The q-39790 profile requires odd s so its reduced nonunit factor stays primitive with a noninteger root. Every mathematical segment is transformed before supported f/g/h function names are inserted; function arguments, TeX command names and polynomial exponent digits are protected. This transformation can change an overall rational-function scalar but preserves pole sets and equality among stages within the question. Source unknown error operations are explicitly unresolved. All source radio profiles carry `evidence_only=true` and `eligible_for_learning=false`. Existing blanks preserve required scalar fragments and captured field order. Parameter dictionaries are public, enforced and never silently repaired.

The only source-format repair is q-39790's missing field layout: append an ascending-order answer row with two matching placeholders. Missing source keys are inferred from independently solved actual printed denominators. Missing source solutions are authored completions: q-39796 explicitly displays original sum, common-denominator numerator, distributed numerator, and collected numerator, then zero-product equation and distinct poles; q-4629 and q-6908 display the factorized function, zero-product equation and conclusion. These missing values/solutions do not count as source fidelity matches. Raw source remains untouched. No source byte-level TeX escape anomaly was found, and generated source text passes the same brace/delimiter tests as defaults.

### Authored eligible defaults and level rationale

All three source-rated levels exist, so no missing-level branch is invented. The defaults broaden bounded objects within those actual level demands:

| Level | Family | Components and explicit bounds | Preserved workload |
|---|---|---|---|
| easy | quadratic | distinct integer r<t in [-8,8], nonzero scalar c in [1,4] | factor expanded denominator quadratic |
| easy | repeated | denominator (x-r)²(x-t), numerator x-u; r<t and u within [-8,8] | factor real cubic with repeated root; count distinct poles |
| easy | factored_three | distinct r,t,v within [-8,8], numerator x-u disjoint | supplied three linear factors; solve without redundant factorization |
| easy | leading | (ax+b)(x-t), 2≤a≤4, 0<abs(b)≤8, gcd(a,abs(b))=1 | primitive nonunit factor and noninteger root, as q-39790 |
| moderate | numerator_quadratic | cx(ax+b), 1≤a≤3, 1≤c≤4, b nonzero, distinct r<t | numerator GCF factoring plus denominator quadratic and no common factor |
| hard | sum | a/(x-r)+b/(x-t), 1≤a,b≤4, distinct nonzero r<t | combine, distribute two nonzero constant products, collect, solve poles |

All bounds are also applied to explicit inputs. Primitive reduced numerator and denominator coefficients have magnitude at most 40/80/60 for easy/moderate/hard, real poles at most 12 in magnitude, and two or three distinct poles. Common factors, nonreal/irrational roots, a zero moderate extra term, inflated nonprimitive leading factors and a collapsed hard constant stage are rejected. These are equal-level variations, not steps in an internal difficulty progression. Functions f/g/h and nonzero overall scalars affect content presentation, not mathematical task counting.

Default authored banks are complete five-member operations, selected before sampling parameters:

- `method_omission_sign`: all denominator roots; omit final root; omit first root; negate all roots; add the numerator-independent false root zero. Select only objects where all five complete sets differ.
- `method_numerator`: all denominator roots; first only; last only; no poles; real numerator roots. Select only objects where all five complete sets differ.

The second bank is the normal moderate bank. These operations are defensible variations of the assessed denominator-versus-numerator and zero-product method. They are labeled authored and never presented as recovered source error intent. No choice-specific feedback is added. The displayed solution is fixed across all choices. Every normal bank rejects the whole sampled instance on collision; explicit invalid instances raise instead of resampling.

Identity uses version, actual prompt, actual fixed solution, full displayed bank and root fragments. It excludes seed and option order. Mathematical fingerprints exclude bank/profile/layout/name and nonzero scalar coefficients after monic polynomial normalization; equivalent assessed rational-function objects deduplicate across presentation spellings.

## Plot stages 5 and 7

No assessed template needs plots. See `plot-spec.md`. No renderer or image asset is produced; the generator stops before database preparation.



## Public raw evidence replay

Every `observed_<id>_raw` profile is available through the same `generate` API, selected using `source-cases.json`’s `raw_bank_profile`. It performs the same positive dilation of mathematical components and all choices while preserving attribute absence: missing original difficulty, worked solution, field layout and correct references remain absent. Raw q-39790 remains fieldless. All raw profiles are evidence-only and ineligible for learning; completed `observed_<id>` profiles separately carry supported authored repairs. `raw-source-replays.json` contains all ten original raw public replays and ten changed variants. Validation checks the absent attributes, exact available strings/full banks, changed actual function names/poles and deterministic identities. Raw records with absent assessment attributes are not passed to the native grader as if complete learner records.
