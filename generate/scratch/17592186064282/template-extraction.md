# Extraction

## 1. Specific source evidence

source-profiles.json preserves every original prompt, complete field-owned bank, feedback omission, correct designation or omission, and full worked solution at basis2275. source-cases.json contains all 13 parameterized public raw replay cases. Each source ID remains a distinct wording/stage/profile family; sharing mathematics does not merge their layouts.

## 2. Backbone

Write a reciprocal trig function as an outer sec, csc, or cot with inner polynomial/affine expression; differentiate outer and inner separately, multiply the chain factor, and substitute the actual inner expression. Moderate includes the observed sum-rule or point evaluation. Hard continues point evaluation into point-slope and slope-intercept form. No inverse trig, nested trig compositions, trig powers, quotient-rule tasks, or new method branches are introduced. Inner signs, poles, degree and the requested object are part of the instance.

## 3. Complete components and recipes

| Source | Variable slots, with a integer1..9 | Full profile / answer components |
|---|---|---|
| q-31330 | A=3a, U=x+1 | A csc U; -csc U; csc²U; -A csc²U; A csc²U |
| q-48640 | B=8a, U=Bx³+1, D=3Bx² | (D+1)sec²U; (D+1)sec U tan U; D sec U tan U; D sec²U tan U; D tan U |
| q-31333 | A=8a, U=10x | derivative -10A csc U cot U; original fields absent |
| q-310222 | U=2ax³ | fragment -6ax²csc²U |
| q-31320 | B=2a, U=Bx-1 | -B sec U tan U; -B csc U tan U; sec U tan U; B sec U tan U; -B sec x tan x |
| q-31341 | d=a+4, U=1-x/d, x0=1 | slope csc²((d-1)/d)/d; original fields absent |
| q-342405 | F=a sec(πx²), x0=1/2 | slope aπ√2 |
| q-342412 | F=a csc(πx³/6), x0=1, y0=2a | slope -aπ√3; intercept aπ√3+2a |
| q-48510 | F=sec(3x)-(a+1)x, x0=0, y0=1 | tangent RHS 1-(a+1)x; original fields absent |
| q-31338 | n=a+2, U=(n-1)π-nx, x0=(2n-3)π/(2n) | -n; n; x0; -1; 1 |
| q-31340 | n=2a+3 odd, U=nx, x0=-π/2 | 0; -1; n; 1; -n |
| q-342402 | F=sec(2x)/2-ax⁴/4 | sec(2x)tan(2x)-ax³ |
| q-48512 | F=a cot(2π-3x), x0=π/2, y0=0, m=3a | y=x0; y=0; y=x-x0; y=mx-x0; y=mx-mx0 |

Numeric profiles q31338/q31340 have underdetermined misconception labels: retain their full observed numerical operation patterns, including ±unit, rate, and requested point, rather than inventing explanations. Complete profiles are selected before construction; collisions cause whole-instance rejection. Bank order is not a task identity. Bounds are enforced on explicit calls and samplers.

## 4. Reusable prompt and solution template

transform() defines complete textual mathematical components and applies a simultaneous longest-component substitution, avoiding cascades and exponent/operator corruption. Every parameter affects the printed function or requested point. function() independently defines one exact instance. The same instance derives normal keys and field completions; the full captured stage sequence/prose is rendered from the component masks at originals and changed inputs. No source-anchor literal return exists. Normal fieldless completions append one explicit blank: derivative RHS, slope scalar, or tangent RHS. Their source solutions are retained.

Original degree, shift, function kind, and response shape are fixed because changing them would change the observed workload/profile; amplitude, inner scale, or denominator vary conservatively within each family. The three normal field completions are authored variants of their original source templates; six previews are saved in authored-field-completions.json. The frozen capture has no non-MA inventory, so independent-inventory.json contains an empty basis/lineage wrapper.

Raw profiles retain all absent keys/solutions/fields and remain evidence-only. Mathematical repairs: q31341's evaluation row says f′(x) despite substituting x=1; normal says f′(1). q342412 has cot inside csc's argument braces in two intermediate rows; normal moves the csc boundary before cot. Raw preserves both errors. Normal presentation converts unwrapped align/eqnarray into canonical display aligned blocks, removes the source font-style wrapper around “and”, and removes answer dollar delimiters/uses math type. Complete source prose, stage counts and mathematical response shapes otherwise remain intact.

Real domains exclude cos(U)=0 for sec and sin(U)=0 for cot/csc. All requested points avoid these poles. Equality checks use exact reciprocal identities, parity, and integer-π periodicity, respecting the source domain. Finite task counts use the actual printed function, requested point and response operation; seed, aliases, profile bank/order and metadata are excluded. Native grading constrains learner-eligible q310222 to a1..8 (inner scale2..16); a9 remains raw evidence/unsupported diagnostics. Both explicit calls and normal sampling enforce the reduced bound. Bounds produce 26 easy,45 moderate,27 hard normal tasks. q31340 has a zero final slope throughout but its actual differentiated/evaluated inner rate and phase vary; this is not nine different answer scalars.

Native diagnostic: q310222 a9 (inner coefficient18) has no supported wrong-answer witness for wrong0 or correct+1; the engine reports unresolved domain differences / unsupported equivalence. This instance is excluded from normal serving. Every declared served blank tests canonical input, an independently expressed reciprocal identity/rationalized radical/point-slope equivalent, wrong0, wrong+1, and the native empty-submission gate.

TeX fraction components in q31341: source single-digit shorthand at the original d5 anchor remains byte-exact. At d10..13, every complete x/d,1/d,(d-1)/d component uses explicit numerator/denominator braces in both normal and changed raw presentation. The private parser and public output guard reject unbraced multi-digit fraction arguments rather than interpreting a lexical number as one TeX token. Eighteen original/changed raw and normal cases, malformed shorthand controls, and a rendered prompt mutation test cover this boundary.
