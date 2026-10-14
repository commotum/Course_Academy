# Current source classification

The read at math basis 2141, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`,
contains five practice questions. The complete read is retained in
`replenishment/kp-initial.edn`. Replenishment captures and validates the current
pool again under the application lock. The original classification and generator
remain frozen, with their source-bank replay and validation evidence intact.

| Difficulty | Field layouts | Separate source templates | Plot rating | Sources |
|---|---|---|---|---|
| Unrated | One five-choice radio | Named-pair first isolation; named-pair second isolation; triangular first-minus-second difference | none for each | q-12444, q-12457, q-18483 |
| Moderate | Two math blanks, field-1 and field-2 | First-equation isolation, ordered pair in separate fields | none | q-181207 |
| Hard | One five-choice radio | Homogeneous first equation, second-equation isolation, second-minus-first difference | none | q-112214 |

The new moderate and hard sources are separate templates. Their prompt layouts,
response shapes and worked-solution sequences differ from the frozen generator's
templates. The canonical example continues to supply the frozen generator's
fourth template. Easy, moderate and hard generation workloads are authored and
documented in the original classification; these source additions do not change
those bounds. The frozen generator supports five-choice radio output at all
three levels. It does not expose the two newly observed layouts. Difficulty
inventory is pooled across valid layouts; there is no requested layout quota.

## q-112214

The printed equations are `21x-9y=0` and `5y-15x+10=0`. The first is homogeneous;
both have nonunit integer coefficients. The second yields `y=3x-2`.
Substitution yields `21x-9(3x-2)=0`, then `-6x+18=0`, so `x=3`, `y=7` and
`y-x=4`. The response is a scalar in a five-choice `selection` math radio field.
The recorded hard rating is retained as source evidence.

The complete source bank is `{4,10,-4,0,-10}`; its correct owned answer is `4`.
At `(X,Y)=(3,7)`, the entire bank is reproduced by
`{Y-X,X+Y,X-Y,0,-X-Y}`. These are observed expressions, not a claim to recover
the author's error intent. In particular, the literal zero option has only one
observed value and no evidenced general error recipe. No mixed bank is inferred.

The solution numbers both equations, uses three isolation rows, six substitution
rows including the reversed `18=6x` equation, and three back-substitution rows
into the isolated expression. It then states the pair and computes `y-x`.
The independent verifier reads the two actual printed equations and every row,
checks every complete option and the designated answer, and tests all choices
through the current application's grader. The source is kept unchanged.

## q-181207

The equations are `3p-6q=-18` and `4p+3q+2=0`, with signed integer coefficients.
The first gives `p=2q-6`; substitution into the second gives
`4(2q-6)+3q+2=0`, then `11q=22`, so `q=2`, `p=-2`.
The problem asks for `(p,q)` with separate placeholders `{{field-1}}` and
`{{field-2}}`. Each blank owns one canonical math answer, respectively `-2`
and `2`, with no distractor bank. The recorded moderate rating is source evidence.

The source solution numbers the system, uses three isolation rows, four
substitution/distribution/collection/division rows and four back-substitution
rows into the first equation. Its final ordered pair is `(-2,2)`. The verifier
checks these equations and field meanings independently. Native grading tests
both canonical answers, equivalent fractions `-4/2` and `4/2`, and incorrect
values for each field. No source values, fields or solutions are rewritten.

All five source templates need no plots. Steps 5 and 7 therefore require no new
assets. The three unrated, incomplete original sources remain excluded from
available inventory, and the source q-12457 mathematical failure stays explicit.
Registration refers to the existing frozen generator script and reuses its
registered UUID if one appears before the locked read. Generated instances use
the validated default method banks, with the unchanged authored level bounds.

## Current canonical presentation

The current canonical e-13010 has presentation changes since basis 1356. The
prompt now uses an aligned system. The numbered equations are a MathJax SVG at
`images/77/77459b19bb1fd1f28e05e6f613e4e49af34595eae33eeeca584d65a289f7ea2c.svg`.
Its rendered glyph sequence is `{2u+9v−6=0(1)2u+6v−8=0(2)`, independently
decoded from the SVG's actual glyph references; its bytes match the SHA-256 in
its filename. This is standalone rendered mathematics, not a plot.

The worked solution now uses `eqalign`, inline rather than display math in
some sentences, a TeX colon, and a terminal period. The current verifier checks
the printed equations and all 17 rows against the frozen canonical generator,
then checks the entire prose and notation after only these documented markup
normalizations. Everything matches, so the current presentation does not require
a mathematical or generator change. Both captures and the exact validation
receipt are retained. No canonical content or source asset is modified.
