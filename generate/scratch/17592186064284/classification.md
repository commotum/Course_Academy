# Classification and extraction

Captured all 11 practice questions and canonical e-735 at math basis 1931,
lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Exact questions, fields, every
choice and correct value are in source.json and classification.json. All plots
are none: no source contains a mathematical graph or diagram.

| Band | Source templates | Response shapes | Generator capability |
|---|---:|---|---|
| Easy | 0 | unobserved | uncertified; no easy inventory claimed |
| Moderate | 9 | three complete radio banks, four blank layouts (1/2/3 fields), two fieldless captures | classified; existing stock suffices; not implemented by this bounded hard generator |
| Hard | 1 | source field missing; tangent equation inferred from solution | authored RHS blank; 54 validated parameter pairs |
| Unrated | 1 | radio with no correct reference or solution | retained incomplete source; excluded from available inventory |

Moderate templates remain separate: sin(cos x) radio q-48643;
cot(sin x) radio q-72161; 3 sec(cos x) radio q-72173; sin(sec x)
fieldless q-72163; csc(cos x) fieldless q-72170; 4 cos(sin x)
two blanks q-341223; tan(tan x) one blank q-342436; 4 sec(sin x)
three blanks q-342443; sec(csc x) two blanks q-342445. Each radio
bank has its own profile in classification.json; choices are not pooled.
The unrated cot(cos x) q-31356 has five choices but lacks its key, solution,
and difficulty. No source is repaired, relabeled, retired, or overwritten.

The hard source q-48644 is cos(sin x), tangent at (0,1), with no captured
field. Its ordered method is: evaluate slope at the abscissa; decompose the
composition; differentiate both functions; multiply by the chain rule;
evaluate at zero; use point-slope form. It gives slope zero and y=1.
The canonical e-735 uses tan(sin x), with the same decomposition/chain rule.
Canonical examples do not count as practice inventory.

## Bounded hard template

Fixed: composition of trig functions, differentiation via chain rule,
tangent at abscissa zero, one authored blank for the RHS of y=..., and the
source's six-stage worked solution sequence. No distractor bank is authored.

Variable: y=a cos(sin x+b), point (0,a cos b). Coefficient a is an integer
1..9; b/pi is one of 0, 1/6, 1/4, 1/3, 2/3, 3/4. These are explicit
extensions of the source's observed a=1, b=0. Phase changes alter both the
curve and tangent; coefficients alter actual numerical values. Neither seed
nor field/answer identities nor presentation order creates a new variant.

For all real x, f'(x)=-a sin(sin x+b) cos x. The slope is -a sin b and the
height is a cos b, so the exact tangent is y=(-a sin b)x+a cos b. All
sampled angles have exact rational/radical trigonometric values. All curves
are smooth on R. Positive coefficients and distinct phases in [0,pi) yield
54 distinct curves and tangent lines. The sampling bound is deliberately
finite; exhaustion must remain explicit rather than mint duplicate variants.

The authored RHS blank records the equation fragment, without y= or math
delimiters. A field-owned canonical answer is its only bank value. Source
bank fidelity is inapplicable to this hard template: the captured source has
zero fields and zero options. Moderate bank replay is not claimed. At source
parameters the computed slope and tangent match q-48644, while the authored
field and solution formatting are labeled as extensions. review.md presents
that original beside five instances. The original's prose remains exact in
evidence; the generated solution retains its method and stage order.

## Capability exception

This package certifies hard tangent-line generation only. It does not certify
an easy template or new moderate variants. Easy is unobserved, not proved
mathematically impossible; its five-question potential reserve remains
unfilled and unclassified. New source evidence reopens that classification.
Moderate source inventory meets the native rolling minimum at the preparation
basis. If it later needs replenishment, implement and fully replay the
captured complete banks and blank layouts before certifying moderate output.
The incomplete unrated source remains explicitly unresolved.
