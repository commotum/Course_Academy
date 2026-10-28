# Classification, math basis 1356

Snapshot lineage: 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. `source.json` is the untouched capture wrapper. Seven practice questions: six observed easy, one unrated; no observed moderate/hard. Eight captured radio fields, all key `selection`, five complete choices each. q-37192 repeats the same widget as a legacy field and a current field. Normal questions have one five-option radio field. No practice prompt, bank, or solution has an image; plot rating **none** for all templates. The lesson introduction's explanatory tree is not part of any practice layout.

| Template | Source | Original name and target | Original structural demand | Level evidence |
|---|---|---|---|---|
| cross_theta | q-37192 | f, theta | 2xy+y²; three product contributions, double-angle collection | easy |
| log_linear_r | q-37196 | g, r | ln(x+y); common denominator and cancellation | unrated; authored easy assignment |
| cubic_r | q-94999 | h, r | x²y; two radial product contributions, cubic coefficient collection | easy |
| log_radial_r | q-95109 | w, r | ln(x²+y²); quotient partials and Pythagorean cancellation | easy |
| x_square_r | q-95112 | f, r | x²; one nonzero Cartesian partial, squared cosine | easy |
| y_square_theta | q-95113 | g, theta | y²; one nonzero Cartesian partial, double-angle identity | easy |
| radial_theta | q-95116 | w, theta | (x²+y²)/2; equal opposite angular terms cancel | easy |

Every original bank has its own `observed` profile; `cross_theta` also has `legacy`. The legacy/current banks are mathematically identical, with different captured notation/order. Source-cases retain both; normal output never asks for two duplicate selections.

## Missing-level scope

Prerequisites are Polar→Cartesian coordinate conversion (topic 936) and the Multivariable Chain Rule (3173). Canonical e-8294 differentiates ½x²+y² with respect to theta. Follow `activity/first-step` and `step/next`, not collection order: introduction (17592186125531) → this KP (17592186125532) → inverse-coordinate derivation (17592186125562) → polar-given function/Cartesian derivative sibling (17592186125533) → cylindrical tutorial/example (17592186125534/535) → spherical tutorial (17592186125563). Only the first two steps support this generator's assessed direction. The inverse sibling establishes a boundary and is excluded.

Moderate peer templates use nonzero unequal quadratic square coefficients plus a nonzero cross term, with target r or theta. Both Cartesian partials have two nonzero terms: four substitutions/products, one final collection; source cross_theta has three products. Coefficients are signed integers of absolute magnitude 1..4, square coefficients unequal. These are authored difficulty claims, not recovered labels, and the two derivative targets are peer tasks.

Hard peers are (a) a two-term cubic a x²y+b xy² with theta target, whose two two-term partials require four cubic angular products, and (b) ln(a x²+b xy+c y²) with theta target, whose four numerator products retain a common nonconstant angular denominator. Both extend observed cubic/log families rather than add another method. Coefficients are signed nonzero integers with absolute magnitude 1..4; logarithmic square coefficients are positive/unequal and 4ac>b². No angle evaluation, second derivative, inverse-coordinate derivative, cylindrical/spherical branch, or new function class is introduced. Each family samples equal-level peers, with no within-level progression.

Easy source-pattern sampling uses positive scale a∈{½,1,2,3,4,5,6}; each original is a=1. The scale multiplies the complete Cartesian function and every observed expression pattern. Function names f/g/h/w affect presentation only. There are 49 bounded easy function/target tasks. Moderate has at most 896 coefficient/target tasks, cubic hard at most 64; log-quadratic positive-definite triples are deduplicated by their Cartesian partials, so common positive argument scales do not inflate task counts. All authored defining coefficients stay nonzero on explicit inputs and sampling.

## Current inventory reclassification, basis 2370 (2026-10-14)

The original basis-1356 capture and frozen generator remain intact. A complete
current KP Pull is retained in `reference/replenishment/initial-snapshot.edn`,
with all 12 source questions, 13 fields, 65 choices, correct references,
solutions, difficulty and the canonical example at the same immutable basis and
lineage. All twelve are now rated easy; q-37196 has since received its missing
solution and reference. There are still no observed moderate/hard questions.
All fields are five-option radio fields with key `selection`; q-37192 retains
two duplicate fields, one without a reference. Every current question is assigned
to one complete bank per field in `current-source-audit.json`.

Five newly captured questions add five prompt/solution families. They retain
the same Cartesian-to-polar direction and have no plots:

| Source | Cartesian function | Target | Final solution rows | Generator treatment |
|---|---|---|---:|---|
| q-95108 | 2x+y² | theta | 3 | Newly classified, generation excluded; prose incorrectly calls p “n”. |
| q-165280 | 2y−xy | theta | 5 | Newly classified, generation excluded; current source independently validated. |
| q-95115 | x²−y² | r | 3 | Newly classified, generation excluded; current source independently validated. |
| q-165281 | x²+y | theta | 3 | Newly classified, generation excluded; one distractor has an unclosed parenthesis. |
| q-95111 | xy | theta | 4 | Newly classified, generation excluded; current source independently validated. |

There are twelve observed Markdown/value families with distinct supplied
function structures or ordered solution sequences, and thirteen raw bank
profiles including the duplicate legacy field. The frozen generator supports
seven observed families/eight raw banks and the four documented authored peer
families. The five added families are bounded exclusions from generation, not
unsupported difficulty bands. No bank from an excluded family is synthesized
or merged into another profile. Their complete literal banks remain in the
current snapshot, and their exact parsed values, correct-reference matches,
parse failures and solution checks are audited separately.

Inventory validation excludes q-37192 (duplicate/incomplete field), q-94999,
q-95113 and q-95116 (documented wrong derivative labels), q-95108 (wrong prose
function label), and q-165281 (malformed choice). These originals remain
unchanged. All current source tasks, including excluded or previously shown
ones, and the canonical example participate in mathematical duplicate checks.
Current counts additionally exclude all historical presentations and active
reservations and use the application's native pool and actual radio grader.
