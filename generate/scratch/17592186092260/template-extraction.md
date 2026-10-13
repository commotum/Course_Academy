# Template extraction

## Stage 1: individual source evidence

Every source below retains its own prompt, field layout, complete bank and worked-solution mask in masks.json; source.json preserves the unmodified captured wrapper. Profiles are raw:<source-id>. Parameter anchors are source-cases.json. Each bank is listed completely, with correct designation presence recorded independently.

### q-11816

Given that $f(x) = e^{3x}$, find $\frac{df}{dx}$.

Anchor: `{"a": 3, "b": 0, "c": 1, "d": 0}`.

Field `selection`, :answer-field.type/radio.

- `\frac{e^{3x}}{3}`
- `xe^{3x}`
- `3e^{3x}`
- `3xe^{3x}`
- `e^{3x}`

Correct designation absent; independently inferred a e^(ax+b), never counted as a matched designation.

### q-11817

Given that $f(x) = e^{2x + 5}$, find $\frac{df}{dx}$.

Anchor: `{"a": 2, "b": 5, "c": 1, "d": 0}`.

Field `selection`, :answer-field.type/radio.

- `\frac{e^{2x + 5}}{2}`
- `2xe^{2x + 5}`
- `2e^{2x + 5}`
- `e^{2x + 5}`
- `(2x + 5)e^{2x + 5}`

Correct designation absent; independently inferred a e^(ax+b), never counted as a matched designation.

### q-107420

Calculate ${f}^{'}(x)$ if $f(x)={x}^{3}-{e}^{1-3x}.$

Anchor: `{"a": -3, "b": 1, "c": -1, "d": 0, "n": 3}`.

Answer fields absent; no bank exists to recover.

### q-48003

Given that $y=-3{e}^{5-x},$ find $\frac{\text{d}y}{\text{d}x}$

Anchor: `{"a": -1, "b": 5, "c": -3, "d": 0}`.

Answer fields absent; no bank exists to recover.

### q-340496

Calculate ${f}^{′}(x)$ if $f(x)=8x+{e}^{-3x+5}.$

${f}^{′}(x)=$
{{field-1}}

Anchor: `{"a": -3, "b": 5, "c": 1, "d": 0, "r": 8}`.

Field `field-1`, :answer-field.type/blank.

- `-3{e}^{-3x+5}+8` — recorded correct

### q-340497

Find the slope $m$ of the tangent to the curve $y=-4{e}^{2-x}$ at the point where $x=2-ln⁡(3).$

$m=$
{{field-1}}

Anchor: `{"a": -1, "b": 2, "c": -4, "d": 0, "k": 3}`.

Field `field-1`, :answer-field.type/blank.

- `12` — recorded correct

### q-48007

Calculate ${f}^{′}(x)$ if $f(x)=-2{e}^{4x-1}+3.$

Anchor: `{"a": 4, "b": -1, "c": -2, "d": 3}`.

Field `selection`, :answer-field.type/radio.

- `-8{e}^{4x-1}+3`
- `\frac{1}{2}{e}^{4x-1}`
- `8{e}^{4x-1}+3`
- `-8{e}^{4x-2}`
- `-8{e}^{4x-1}` — recorded correct

### q-48657

Find the equation of the tangent to the curve $y=5{e}^{4x}$ at the point where $x=\frac{1}{4}.$

Anchor: `{"a": 4, "b": 0, "c": 5, "d": 0}`.

Field `selection`, :answer-field.type/radio.

- `y=20ex\cdot ln⁡(5)`
- `y=5ex`
- `y=ex`
- `y=4ex`
- `y=20ex` — recorded correct

### q-48658

Find the slope of the tangent to the curve $y=-3{e}^{5-x}$ at the point where $x=5-ln⁡(2).$

Anchor: `{"a": -1, "b": 5, "c": -3, "d": 0, "k": 2}`.

Field `selection`, :answer-field.type/radio.

- `3{e}^{5}`
- `3e`
- `6` — recorded correct
- `3{e}^{2}`
- `5`

## Stage 2: generalized families

Direct derivatives use c e^(ax+b)+d; the outer derivative is c e^u and inner derivative a. Sources retain their distinct wording, formatting and absence states. q-107420 differentiates x^n-e^(b-nx), with the same shared n factored in its last row. q-340496 differentiates r x+e^(ax+b), preserving derivative order r+a e^u before reordering the final answer. The slope sources evaluate c e^(b-x) at b-ln(k), producing -c k. The tangent source evaluates c e^(ax) at 1/a, finding ca e, c e, then expanding point-slope form to y=ca e x.

## Stage 3: components and complete banks

Let E=e^(ax+b), h=ax+b, D=caE. q-11816 has [E/a, xE, aE, axE, E]; q-11817 has [E/a, axE, aE, E, hE]. Their missed chain factor, reciprocal factor and extra x/inner-argument patterns are defensible observed expressions, without claiming recovered author intent.

q-48007 has [D+d, (-c/a)E, -D+d, ca e^(ax+2b), D]. The doubled shift and positive reciprocal coefficient are opaque historical expression patterns. The raw bank is public evidence-only; no arbitrary fitted scalar recipe becomes the default. Its whole bank requires b nonzero. Normal uses the separately labeled method bank [D,cE,cE/a,-D,D+d].

q-48658 has [-c e^b, -c e, -c k, -c e^k, b]. These are parameterized literal observed component patterns; their intended mistakes are underdetermined. A full raw bank requires b not in {1,k,-ck}. Normal slope radios use [-ck,ck,-k,-c e^b,-c e^k], with whole-bank collision rejection; normal q-340497 retains a blank.

q-48657 has [ca e x ln(c), c e x, e x, a e x, ca e x]. These expressions reproduce the complete equations, including the opaque ln(c) factor. Normal moderate tangent uses this complete bank, labeled authored method based on the displayed outer/inner factors; the extra ln(c) models treating the outer scale as a general base, with no source-intent assertion. Requires a,c nonunit, positive and unequal.

The two observed blanks contain the whole derivative expression (-3e^(-3x+5)+8), and the scalar slope 12. Raw fieldless families have no invented fields. Completed versions add expression fragments. Normal polynomial sum radio operations (available explicitly) use correct derivative, omitted inner factor, sign error, undifferentiated power and omitted power term. Linear sum radios use correct, omitted/reciprocal/sign chain factor, and omitted linear term. Every bank is chosen complete; collisions reject the entire parameter instance rather than replacing individual options.

## Stage 4: reusable masks and constraints

Masks use complete mathematical component slots and simultaneous longest matching extraction, avoiding recursive numeric substitutions. Slots include full exponents, outer/product coefficient terms, derivative terms, individual point substitutions, logarithms, final sums, evaluated products and complete tangent-equation coefficients. Raw replay uses the public generate API at arbitrary eligible parameters and retains question/field attribute absence. Identity conversion removes internal db IDs and uses the established local UUID/enum/ref shape. It does not count that schema conversion as content alteration.

Existing source solutions retain the complete composite-definition block, separate outer/inner derivative block, formal chain-rule operator row, substituted factors, multiplied result and restored exponent. Each family then retains its own sum/evaluation/tangent rows and original shared prose, including introductory evaluation points. Normal ln⁡ uses \ln, preserving U+2061 in raw evidence. No decoded adjacent slash anomaly exists: JSON display escaping is not a source TeX error. No mathematical source correction was needed.

Easy coefficients have |a|≤6, |c|≤8, |b|≤8; direct source radios require nonunit a, reflected-scale family keeps a=-1. Scaled-translation normal a,c are nonunit, d nonzero. Moderate has n=3..5 with a=-n, c=-1 for factored power sums; linear sums require |a|=2..6 and |r|=2..8; slope c=-2..-8, a=-1, k=2..6, |b|≤8; reciprocal-point tangent a=2..6,c=2..8,a≠c. Hard |a|,|c|=2..6; b∈{-6..-1,2..6}; |d|=1..6. Every explicit call obeys its family bounds. There is no progression inside any family.

Meaningful parameter counts are computed from these finite domains (see validation.json). Derivative task fingerprints exclude d, which is incidental to that operation; tangent fingerprints include the curve and point because vertical translation affects the required line. Profiles, choice order and letter aliases never inflate mathematical task counts. Content identity includes actual prompt, fixed solution, difficulty/absence, complete bank, and correct-key presence/designated mathematical value; profile aliases and incidental unused metadata do not change it.

Plot extraction/specification (steps 5 and 7): none required; no image creation or renderer is used.
