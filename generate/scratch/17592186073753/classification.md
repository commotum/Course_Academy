# Classification

Captured database `math`, basis **1356**, lineage
`01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` preserves the full capture
wrapper and raw colon-keyed record. Every practice question is **unrated**, has
one `selection` radio field with five mathematical choices, and lacks both its
correct reference and worked solution. No observed easy/moderate/hard claims are
made. Three distinct prompt/response templates and three empirical complete
choice profiles are observed; plots are **none**.

| Source | Template/profile | Printed structure and response | Author design level |
|---|---|---|---|
| q-12444 | pair_first / source_q12444 | -3p+q=-9; 5p+4q=32; full named pair | easy |
| q-12457 | pair_second / source_q12457_raw | -7a+2b=18; -6a+6b=0; full named pair | hard replay tag, not valid source assessment |
| q-18483 | difference / source_q18483 | 5q+55=0; 2p+3q+3=0; scalar p-q | easy |

The canonical e-13010 provides a fourth prose/stage template,
`canonical_second`: isolate u in the second integer-coefficient equation,
substitute into the first, distribute two nonunit products, collect, solve v,
and back-substitute into the first. It has no practice bank. A complete authored
five-choice method bank supports this template at all three author-designed
levels. Pair templates preserve full named pairs; the difference template
preserves scalar shape.

The route is recovered through activity/first-step 17592186074657 -> step/next
17592186074658 -> step/next 17592186074659, rather than collection order:
Introduction -> basic substitution KP 17592186073752 -> challenging substitution
KP 17592186073753. Prerequisite topics are Introduction to Systems of Linear
Equations and Solving Two-Variable Equations. Later separate branches explicitly
include decimal coefficients, fractional coefficients and nonlinear equations;
none is introduced here. Source coefficients remain integers even where an
answer is fractional.

The basic sibling canonical isolates a variable with coefficient 1 then inserts
it into another unit-leading equation. Authored normal questions here require
nonunit division and/or multiplication across the affine substituted expression.
Easy pair_first retains the observed q-12444 unit y isolation only because the
other equation has nonunit multipliers. The triangular difference source is an
observed special form; its authored easy variants preserve two nonunit divisions
and a final difference rather than introducing an unrelated skill.

All level assignments and bounds are author decisions: easy has small integer
coefficients (absolute value <=6), integer solutions and nonunit division or
distribution; moderate has all four nonzero variable coefficients nonunit and
<=9, an integer affine isolation, integer solutions; hard has all coefficients
nonunit and <=10, the same canonical operation, and at least one fractional
solution with denominator <=12. They are parallel arithmetic workloads, with no
new branch or within-level progression. Constants are bounded separately at
70/110/120. Nontrivial affine isolation has nonzero constant and slope in normal
pair/canonical tasks. Explicit calls receive the same guards as sampled calls.
Raw and empirical replay profiles retain original parameter structures and are
clearly separated from the normal level bounds.
