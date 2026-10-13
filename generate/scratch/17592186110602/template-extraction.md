# Template extraction (step 4)

## 1. Specific source descriptions

Every original and source replay is printed in review.md. Source-cases.json records the actual parameters and complete bank profiles. Source.json is the immutable basis-1356 wrapper, including UUIDs and absent fields.

### q-215418

Parameters `{"c": 2, "a": -3, "b": 4}`; template `standard_horizontal_blank`. Unrated standard-form two-blank widget. Field 1 is the LHS variable; field 2 is the RHS integer. Both correct designations and the solution are absent. Authored level assignment: easy because the coordinates and required answer are integers and the method is canonical.

Find the equation of the line that is perpendicular to $y = 2$ and passes through the point $(-3, 4)$. Write your answer in **standard form.** {{field-1}} $=$
{{field-2}}

### q-215951

Parameters `{"c": "1/3", "a": 7, "b": 6}`; template `standard_vertical_blank`. Unrated standard-form two-blank widget. Field 1 is the LHS variable; field 2 is the RHS integer. Both correct designations and the solution are absent. Authored level assignment: easy because the coordinates and required answer are integers and the method is canonical.

Find the equation of the line that is perpendicular to $x = \frac{1}{3}$ and passes through the point $(7, 6)$. Write your answer in **standard form.** {{field-1}} $=$
{{field-2}}

### q-110139

Parameters `{"c": -1, "a": -2, "b": -3}`; template `line_first_vertical_radio`. Observed easy five-equation radio with delimiter-free whole equations and the full two-paragraph solution.

Find the equation of the line that is perpendicular to $x=-1$ and passes through the point $(-2,-3).$

### q-110140

Parameters `{"c": 2, "a": 1, "b": 4}`; template `line_first_vertical_radio`. Observed easy five-equation radio with delimiter-free whole equations and the full two-paragraph solution.

Find the equation of the line that is perpendicular to $x=2$ and passes through the point $(1,4).$

### q-110142

Parameters `{"c": 3, "a": -4, "b": -3}`; template `line_first_horizontal_radio`. Observed easy five-equation radio with delimiter-free whole equations and the full two-paragraph solution.

Find the equation of the line that is perpendicular to $y=3$ and passes through the point $(-4,-3).$

### q-110143

Parameters `{"c": "5/2", "a": 3, "b": 7}`; template `line_first_vertical_radio`. Observed easy five-equation radio with delimiter-free whole equations and the full two-paragraph solution.

Find the equation of the line that is perpendicular to $x=\frac{5}{2}$ and passes through the point $(3,7).$

### q-23628

Parameters `{"c": 3, "a": 1, "b": -2}`; template `point_first_vertical_radio`. Observed easy five-equation radio with delimiter-free whole equations and the full two-paragraph solution.

Find the equation of the line that passes through the point $(1,-2)$ and is perpendicular to $x=3.$

### q-44691

Parameters `{"c": 5, "a": -7, "b": -9}`; template `determine_horizontal_radio`. Observed easy five-equation radio with delimiter-free whole equations and the full two-paragraph solution.

Determine the equation of the line that passes through the point $(-7,-9)$ and is perpendicular to $y=5.$

## 2. Shared mathematical pattern

A reference line x=c is vertical. Its perpendicular through (a,b) is horizontal y=b. A reference line y=c is horizontal. Its perpendicular through (a,b) is vertical x=a. The reference constant c and the unused point coordinate do not affect the correct locus. The response is a whole equation in radios and two standard-form fragments in blanks. There is no negative-reciprocal-slope calculation; undefined vertical slope cannot participate in that product rule.

Canonical example e-14365 establishes the two steps: identify perpendicular orientation and copy the required coordinate. The prerequisite is Horizontal and Vertical Lines (MA 97). The recorded route was traversed by activity/first-step 17592186111499 and step/next: Introduction → slope-intercept perpendicular recognition → standard-form perpendicular recognition → unknown parameters → this axis-specific KP. The lesson introduction explicitly calls horizontal/vertical lines the exception. Sibling KPs own general-slope/unknown-parameter work; outgoing topics include Finding Equations of Perpendicular Lines (MA3562). Those methods are excluded here.

## 3. Component and complete-bank mapping

Prompt components: given axis, c, point a and b, original word order, exact spacing/punctuation, optional standard-form instruction and two matching placeholders. Worked-solution components: reference equation/orientation, perpendicular orientation, required axis=k, point, correct coordinate/article, concluding whole equation. No student-facing distractor diagnoses are added. Radio solutions have exactly the original two paragraphs. Blank solutions are authored from canonical prose; noninteger authored blanks append the standard-form integer-coefficient equation.

Each bank table lists every original choice in source order. Expressions use the ordinary prompt coordinates c,a,b and reproduce exact original values. These operations parameterize the observed whole bank; they do not identify the original authoring algorithm or prove a learner's misconception. Reciprocal-of-c intent and use of an unrelated reference constant are explicitly unresolved. Observed profiles remain available for replay; default learner sampling uses separately authored same-method profiles.

### `observed_q110139` — q-110139

| Field | Original value | Parameterized operation | Correct? |
|---|---|---|---|
| selection | `$y=-2` | `y:a` | no |
| selection | `$y=-3` | `y:b` | yes |
| selection | `$x=-3` | `x:b` | no |
| selection | `$x=-2` | `x:a` | no |
| selection | `$y=1` | `y:-c` | no |

### `observed_q110140` — q-110140

| Field | Original value | Parameterized operation | Correct? |
|---|---|---|---|
| selection | `$x=-1` | `x:-a` | no |
| selection | `$y=-2` | `y:-c` | no |
| selection | `$y=1` | `y:a` | no |
| selection | `$x=4` | `x:b` | no |
| selection | `$y=4` | `y:b` | yes |

### `observed_q110142` — q-110142

| Field | Original value | Parameterized operation | Correct? |
|---|---|---|---|
| selection | `$x=3` | `x:c` | no |
| selection | `$x=-4` | `x:a` | yes |
| selection | `$y=-4` | `y:a` | no |
| selection | `$y=\frac{1}{3}` | `y:1/c` | no |
| selection | `$x=-3` | `x:b` | no |

### `observed_q110143` — q-110143

| Field | Original value | Parameterized operation | Correct? |
|---|---|---|---|
| selection | `$y=7` | `y:b` | yes |
| selection | `$y=-3` | `y:-a` | no |
| selection | `$y=-\frac{5}{2}` | `y:-c` | no |
| selection | `$x=7` | `x:b` | no |
| selection | `$x=3` | `x:a` | no |

### `observed_q23628` — q-23628

| Field | Original value | Parameterized operation | Correct? |
|---|---|---|---|
| selection | `$y=2` | `y:-b` | no |
| selection | `$x=-2` | `x:b` | no |
| selection | `$y=-2` | `y:b` | yes |
| selection | `$y=1` | `y:a` | no |
| selection | `$x=1` | `x:a` | no |

### `observed_q44691` — q-44691

| Field | Original value | Parameterized operation | Correct? |
|---|---|---|---|
| selection | `$x=-7` | `x:a` | yes |
| selection | `$x=-9` | `x:b` | no |
| selection | `$y=-7` | `y:a` | no |
| selection | `$x=5` | `x:c` | no |
| selection | `$y=-9` | `y:b` | no |

Blank repairs: q-215418 has given horizontal y=2 and a=-3, so the perpendicular is x=-3. Derived fragments are x and -3. q-215951 has given vertical x=1/3 and b=6, so the perpendicular is y=6. Derived fragments are y and 6. The original widgets show exactly two blanks surrounding an equals sign, confirming the field layout but providing no original correct values. Both placeholders already exist in the capture. No presentation repair is necessary. Newly owned answer objects and correct refs are generator output, never fabricated raw observations. Missing solutions are authored, not counted as exact source solutions.

## 4. Reusable templates, constraints and authored levels

The six templates are implemented structurally in render_prompt, never by replacing arbitrary numerals across prose. All exact parameters are rational. The coordinate bound is absolute magnitude 12. Source number forms include signed integers, c=5/2 and c=1/3. Easy coordinates remain integer. Source replay computes each option from c,a,b; no literal question payload branch or correct-answer lookup is used.

A complete profile is selected before sampling. All five equations are checked for mathematical distinctness and exactly one correct locus; any collision, invalid reciprocal or unsuitable exact decimal rejects the whole instance. No partial bank, truncation, perturbation or first-valid pool is used.

Authored default coordinate/sign bank: required-axis=required-coordinate; required-axis=unused-coordinate; given-axis=required-coordinate; given-axis=unused-coordinate; required-axis=negative-required-coordinate. Conditions: required coordinate nonzero, coordinate values unequal and unused coordinate not the negative of required coordinate. Authored zero bank replaces the sign option with required-axis=c; required coordinate is zero, unused coordinate and c are nonzero/unequal. These complete banks each have five choices. Blanks have no distractors and preserve field-1 LHS / field-2 RHS; fractions clear the denominator to primitive integer standard form with positive coefficient.

Moderate (authored, no source label): a noninteger required coordinate with reduced denominator 2..5, numerator absolute value <=24, all displayed parameter denominators <=5 and absolute value <=12. Hard (authored, no source label): a noninteger required coordinate either with reduced denominator 6..10 and numerator absolute value <=60, or an exact finite decimal with at most two places; absolute values <=12. Random decimal numerators come from -60..60 before reduction and denominators 10,20,25,50,100. Explicit decimals allow the complete <=12 two-place domain. The unused coordinate and c are sampled as integers, though bounded same-policy rationals are accepted explicitly. Hard fractional explicit inputs have all denominators <=10. Moderate/hard blanks perform only denominator clearing after selecting the coordinate.

These are bounded representation policies anchored to the rational constants already present, prerequisite coordinate equations and standard-form widget. They do not claim that copying a more cumbersome coordinate turns the intrinsic axis decision into a substantially harder skill. Numerical reading/retaining exact signs is the only additional radio workload; blank denominator clearing adds one elementary representation step. Both orientations and all layouts are unordered variations at each level. There is no within-level progression and no general slopes, geometry branches, unknown parameters or point-slope algebra.

Meaningful variety is finite for these bounds. Canonical task fingerprints contain only the required axis and reduced required coordinate, excluding c, unused coordinate, equation scaling, notation, layout, profile, answer-bank order and cosmetics. Thus changes to incidental numbers cannot inflate task counts. Content identity includes version, level, template, canonical display parameters, profile, prompt, fixed solution and sorted full banks; different presented content has different UUIDs. For fixed parameters/template/profile, seed changes only option order and never content identity.

Exact enumeration of target-axis/coordinate objects: easy has 50 meaningful tasks; moderate has 240; the hard random sampler has 1288; its broader explicit exact-decimal policy has 5320. Both reference orientations are counted once per reduced target coordinate. This is a finite object set, not a claim of new operations; profiles, layouts and incidental coordinates add no mathematical tasks.
