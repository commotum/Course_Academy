# Four extraction stages

## 1. Describe the five observed instances

Every source uses the exact sentence “Which of the following equations has
infinitely many solutions?”, an unlabeled three-item math list, one selection
radio field, five text choices, and the shared opening “Let's attempt to solve
each equation in turn:”. The worked solution treats first, second and third in
order and closes with the correct subset sentence. Variable x is real. There
are no plots, per-option feedback, or distractor diagnoses.

| Source | Affine quadruples (a,b,c,d) | Classes | Profile |
| --- | --- | --- | --- |
| q-287966 | (2,0,1,1); (2,1,2,1); (2,1,2,3) | unique, identity, empty | observed_a |
| q-288419 | (3,0,2,5); (4,-2,4,-2); (5,3,5,1) | unique, identity, empty | observed_a |
| q-288425 | (-3,2,-3,7); (6,1,6,5); (7,-4,6,-6) | empty, empty, unique | observed_b |
| q-288427 | (2,-5,1,-2); (6,1,6,9); (-4,3,-4,3) | unique, empty, identity | observed_d |
| q-288591 | (3,2,4,1); (2,-5,3,-3); (5,-4,5,-4) | unique, unique, identity | observed_c |

The first two unique cases have zero left constants and three algebra rows.
Other unique cases have five rows, removing the constant after the variable.
When the right slope is larger the solution moves variables right and prints
x=value at the end. Negative shared slopes use addition of their magnitude.

## 2. Generalize the shared pattern

For each numeric equation ax+b=cx+d, compare reduced coefficients and constants:
a=c and b=d gives infinitely many solutions; a=c and b≠d gives none;
a≠c gives one. Select the complete subset of identities from the retained bank.
The source triple positions and truth patterns are instances of one template,
not independent arithmetic skills. No source difficulty other than easy exists.

## 3. Map every component and complete bank

The prompt slots are three complete equations. Their four numeric components
feed every subsequent algebra row and sentence, without substring replacements.
Source stages are: original equation; subtract the shared or smaller coefficient
from both sides; simplify; if needed subtract a constant on both sides; final x.
All equations, constant equalities, and printed unique-solution values are
independently checked from the actual rendered prompt/solution.

Each answer recipe is the exact literal description of a finite subset of the
three displayed equations. These recipes do not depend numerically on the
coefficients; the correct designation does. Every source choice is mapped here:

| Complete profile | Five values (the complete bank) | Sources |
| --- | --- | --- |
| observed_a | II only; III only; I and II only; II and III only; I, II, and III | q-287966, q-288419 |
| observed_b | None; I and II only; II only; III only; I and III only | q-288425 |
| observed_c | I and II only; II only; I only; II and III only; III only | q-288591 |
| observed_d | II and III only; III only; None; I and III only; II only | q-288427 |

No intent is inferred for an incorrect subset. Five choices per source, including
all twenty incorrect choices and five correct designations, are preserved.
Neither a candidate distractor pool nor a new mixed bank is used. The chosen
complete bank determines eligible identity subsets before equation sampling.
None and all-three patterns are real eligible tasks where their complete bank
contains the required answer. Each nonidentity peer can independently be empty
or unique; no fixed source position or truth mask limits normal practice.

## 4. Extract reusable masks, constraints and extensions

The observed template `direct` builds whole affine expressions, signed removal
rows and conditional constant-removal rows. It reproduces every captured prompt
and full solution string exactly at original parameters. IDs and choice order
are review identities rather than copied source identities. Zero constants and
unit coefficients are handled structurally. Source replay is the ordinary API
with explicit parameters/profile; no source payload-returning branch exists.

Authored `one_distribution` uses k(x+b)=cx+d. Every equation has a nonunit k and
nonzero b, with distinct formal multiplication and evaluated affine rows before
the common solving sequence. `two_distributions` uses
k(ax+b)+tx+s=m(cx+d)+ux+v, with all ten components nonzero, two distinct
formal products per side, evaluated products, collection, then the shared
solving sequence. Additional division for a nonunit reduced slope gap is kept
inside the unique peer's already prerequisite-supported solution, while the
learner still selects identities. The classification file gives the actual
prerequisite and route rationale and all sampled/explicit reduced bounds.

Content identities include the actual prompt, full fixed solution, difficulty,
generator version and complete sorted bank. Option order and seed are absent.
The mathematical fingerprint excludes banks and seed, canonically normalizes
common scaling/side reversal for direct affine comparisons, and retains the
substantive arithmetic structure for authored distribution tasks. Numerical
components, not variable-letter aliases, vary. This is a bounded discrete
catalog; validation reports distinct sampled fingerprints rather than claiming
unlimited variety. Parameter fingerprints separately retain the exact inputs.
