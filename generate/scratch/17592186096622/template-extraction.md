# Four-stage extraction

Evidence source.json is the exact basis2275 wrapper. Topic/lesson snapshots are frozen alongside it. Normal mathematical replay, complete-bank matching, operative stages and raw fidelity are reported separately. The following source-specific families are kept separate because their answer fragments or solution stages differ.

## q-340336

1. **Specific observation.** Given that $y=\frac{\operatorname{tan}x}{{x}^{2}}$, find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=\frac{1}{{x}^{3}}\cdot ($
{{field-1}}
$).$

Source rating {':db/ident': ':question.difficulty/easy'}. Numerator `tan(x)`, denominator `x**2`, ordered derivatives `tan(x)**2 + 1` and `2*x`. The response is blank. Captured prose and complete banks appear verbatim in source-components.json.

2. **General pattern.** Identify u and v in Leibniz notation, differentiate each, substitute the four ordered operands in (v du/dx−u dv/dx)/v², preserve this family’s factor/collection stages, and fill the printed derivative or derivative fragment.

3. **Components and banks.** Anchor slots `{"c": 1}`; complete bank `fragment`.

- `x{sec}^{2}x-2\operatorname{tan}x` → `x*sec(x)**2 - 2*tan(x)`.

4. **Backbone and slots.** Kind `tan-square`; exact slot keys `c`. Slots are substantive coefficients, log base, or a positive integer power as detailed below. Each slot changes the actual function, both derivative definitions, every substituted factor, every dependent intermediate, the requested fragment/factor and all options. Original anchors are retained. No target-name, choice-order or seed variation counts as a new task.


## q-340340

1. **Specific observation.** Given that $y=\frac{{e}^{x}}{x+1},$ find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}

Source rating {':db/ident': ':question.difficulty/easy'}. Numerator `exp(x)`, denominator `x + 1`, ordered derivatives `exp(x)` and `1`. The response is blank. Captured prose and complete banks appear verbatim in source-components.json.

2. **General pattern.** Identify u and v in Leibniz notation, differentiate each, substitute the four ordered operands in (v du/dx−u dv/dx)/v², preserve this family’s factor/collection stages, and fill the printed derivative or derivative fragment.

3. **Components and banks.** Anchor slots `{"c": 1, "b": 1}`; complete bank `fragment`.

- `\frac{x{e}^{x}}{(x+1)^{2}}` → `x*exp(x)/(x + 1)**2`.

4. **Backbone and slots.** Kind `exp-linear`; exact slot keys `c, b`. Slots are substantive coefficients, log base, or a positive integer power as detailed below. Each slot changes the actual function, both derivative definitions, every substituted factor, every dependent intermediate, the requested fragment/factor and all options. Original anchors are retained. No target-name, choice-order or seed variation counts as a new task.


## q-340337

1. **Specific observation.** Given that $y=\frac{x}{cos⁡x}$, find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=\frac{1}{{cos}^{2}⁡x}\cdot ($
{{field-1}}
$).$

Source rating {':db/ident': ':question.difficulty/easy'}. Numerator `x`, denominator `cos(x)`, ordered derivatives `1` and `-sin(x)`. The response is blank. Captured prose and complete banks appear verbatim in source-components.json.

2. **General pattern.** Identify u and v in Leibniz notation, differentiate each, substitute the four ordered operands in (v du/dx−u dv/dx)/v², preserve this family’s factor/collection stages, and fill the printed derivative or derivative fragment.

3. **Components and banks.** Anchor slots `{"c": 1}`; complete bank `fragment`.

- `\operatorname{cos}x+x\operatorname{sin}x` → `x*sin(x) + cos(x)`.

4. **Backbone and slots.** Kind `linear-cos`; exact slot keys `c`. Slots are substantive coefficients, log base, or a positive integer power as detailed below. Each slot changes the actual function, both derivative definitions, every substituted factor, every dependent intermediate, the requested fragment/factor and all options. Original anchors are retained. No target-name, choice-order or seed variation counts as a new task.


## q-47994

1. **Specific observation.** Given that $y=\frac{sin⁡x}{x},$ find $\frac{\text{d}y}{\text{d}x}.$

Source rating {':db/ident': ':question.difficulty/easy'}. Numerator `sin(x)`, denominator `x`, ordered derivatives `cos(x)` and `1`. The response is radio. Captured prose and complete banks appear verbatim in source-components.json.

2. **General pattern.** Identify u and v in Leibniz notation, differentiate each, substitute the four ordered operands in (v du/dx−u dv/dx)/v², preserve this family’s factor/collection stages, and fill the printed derivative or derivative fragment.

3. **Components and banks.** Anchor slots `{"c": 1}`; complete bank `observed-47994`.

- `\frac{xcos⁡x+sin⁡x}{{x}^{2}}` → `c*(x*cos(x)+sin(x))/x^2`.
- `\frac{x(cos⁡x-sin⁡x)}{{x}^{2}}` → `c*x*(cos(x)-sin(x))/x^2`.
- `\frac{xcos⁡x-sin⁡x}{{x}^{2}}` → `c*(x*cos(x)-sin(x))/x^2`.
- `\frac{cos⁡x-xsin⁡x}{{x}^{2}}` → `c*(cos(x)-x*sin(x))/x^2`.
- `\frac{xcos⁡x-sin⁡x}{x}` → `c*(x*cos(x)-sin(x))/x`.

4. **Backbone and slots.** Kind `sin-linear`; exact slot keys `c`. Slots are substantive coefficients, log base, or a positive integer power as detailed below. Each slot changes the actual function, both derivative definitions, every substituted factor, every dependent intermediate, the requested fragment/factor and all options. Original anchors are retained. No target-name, choice-order or seed variation counts as a new task.


## q-11969

1. **Specific observation.** Given that $y=\frac{-x}{9-2x}$, find $\frac{\text{d}y}{\text{d}x}.$

Source rating {':db/ident': ':question.difficulty/moderate'}. Numerator `-x`, denominator `9 - 2*x`, ordered derivatives `-1` and `-2`. The response is radio. Captured prose and complete banks appear verbatim in source-components.json.

2. **General pattern.** Identify u and v in Leibniz notation, differentiate each, substitute the four ordered operands in (v du/dx−u dv/dx)/v², preserve this family’s factor/collection stages, and fill the printed derivative or derivative fragment.

3. **Components and banks.** Anchor slots `{"c": -1, "a": -2, "b": 9}`; complete bank `observed-11969`.

- `\frac{9}{{(9-2x)}^{2}}` → `-c*b/(a*x+b)^2`.
- `-\frac{9}{{(9-2x)}^{2}}` → `c*b/(a*x+b)^2`.
- `\frac{4x-9}{{(9-2x)}^{2}}` → `c*(b+2*a*x)/(a*x+b)^2`.
- `-\frac{2x-9}{{(9-2x)}^{2}}` → `-c*(b+a*x)/(a*x+b)^2`.
- `-\frac{4x-9}{{(9-2x)}^{2}}` → `-c*(b+2*a*x)/(a*x+b)^2`.

4. **Backbone and slots.** Kind `linear-linear`; exact slot keys `c, a, b`. Slots are substantive coefficients, log base, or a positive integer power as detailed below. Each slot changes the actual function, both derivative definitions, every substituted factor, every dependent intermediate, the requested fragment/factor and all options. Original anchors are retained. No target-name, choice-order or seed variation counts as a new task.


## q-340332

1. **Specific observation.** Given that $y=\frac{{x}^{2}}{{x}^{2}+1}$, find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}

Source rating {':db/ident': ':question.difficulty/moderate'}. Numerator `x**2`, denominator `x**2 + 1`, ordered derivatives `2*x` and `2*x`. The response is blank. Captured prose and complete banks appear verbatim in source-components.json.

2. **General pattern.** Identify u and v in Leibniz notation, differentiate each, substitute the four ordered operands in (v du/dx−u dv/dx)/v², preserve this family’s factor/collection stages, and fill the printed derivative or derivative fragment.

3. **Components and banks.** Anchor slots `{"c": 1, "b": 1}`; complete bank `fragment`.

- `\frac{2x}{{({x}^{2}+1)}^{2}}` → `2*x/(x**2 + 1)**2`.

4. **Backbone and slots.** Kind `square-square`; exact slot keys `c, b`. Slots are substantive coefficients, log base, or a positive integer power as detailed below. Each slot changes the actual function, both derivative definitions, every substituted factor, every dependent intermediate, the requested fragment/factor and all options. Original anchors are retained. No target-name, choice-order or seed variation counts as a new task.


## q-340341

1. **Specific observation.** Given that $y=\frac{x}{ln⁡x},$ find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}

Source rating {':db/ident': ':question.difficulty/moderate'}. Numerator `x`, denominator `log(x)`, ordered derivatives `1` and `1/x`. The response is blank. Captured prose and complete banks appear verbatim in source-components.json.

2. **General pattern.** Identify u and v in Leibniz notation, differentiate each, substitute the four ordered operands in (v du/dx−u dv/dx)/v², preserve this family’s factor/collection stages, and fill the printed derivative or derivative fragment.

3. **Components and banks.** Anchor slots `{"c": 1}`; complete bank `fragment`.

- `\frac{\operatorname{ln}x-1}{(\operatorname{ln}x)^{2}}` → `(log(x) - 1)/log(x)**2`.

4. **Backbone and slots.** Kind `linear-ln`; exact slot keys `c`. Slots are substantive coefficients, log base, or a positive integer power as detailed below. Each slot changes the actual function, both derivative definitions, every substituted factor, every dependent intermediate, the requested fragment/factor and all options. Original anchors are retained. No target-name, choice-order or seed variation counts as a new task.


## q-340343

1. **Specific observation.** Given that $y=\frac{{log}_{3}⁡x}{{x}^{2}},$ find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}}
$)\cdot \frac{1}{{x}^{3}ln⁡3}$

Source rating {':db/ident': ':question.difficulty/moderate'}. Numerator `log(x)/log(3)`, denominator `x**2`, ordered derivatives `1/(x*log(3))` and `2*x`. The response is blank. Captured prose and complete banks appear verbatim in source-components.json.

2. **General pattern.** Identify u and v in Leibniz notation, differentiate each, substitute the four ordered operands in (v du/dx−u dv/dx)/v², preserve this family’s factor/collection stages, and fill the printed derivative or derivative fragment.

3. **Components and banks.** Anchor slots `{"b": 3, "n": 2}`; complete bank `fragment`.

- `1-2\operatorname{ln}x` → `1 - 2*log(x)`.

4. **Backbone and slots.** Kind `log-power`; exact slot keys `b, n`. Slots are substantive coefficients, log base, or a positive integer power as detailed below. Each slot changes the actual function, both derivative definitions, every substituted factor, every dependent intermediate, the requested fragment/factor and all options. Original anchors are retained. No target-name, choice-order or seed variation counts as a new task.


## q-340335

1. **Specific observation.** Given that $f(x)=\frac{1-sin⁡x}{sin⁡x},$ find ${f}^{′}(x).$

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}

Source rating {':db/ident': ':question.difficulty/hard'}. Numerator `1 - sin(x)`, denominator `sin(x)`, ordered derivatives `-cos(x)` and `cos(x)`. The response is blank. Captured prose and complete banks appear verbatim in source-components.json.

2. **General pattern.** Identify u and v in Leibniz notation, differentiate each, substitute the four ordered operands in (v du/dx−u dv/dx)/v², preserve this family’s factor/collection stages, and fill the printed derivative or derivative fragment.

3. **Components and banks.** Anchor slots `{"a": 1, "b": 1}`; complete bank `fragment`.

- `-\operatorname{csc}x\operatorname{cot}x` → `-cot(x)*csc(x)`.

4. **Backbone and slots.** Kind `sin-sin`; exact slot keys `a, b`. Slots are substantive coefficients, log base, or a positive integer power as detailed below. Each slot changes the actual function, both derivative definitions, every substituted factor, every dependent intermediate, the requested fragment/factor and all options. Original anchors are retained. No target-name, choice-order or seed variation counts as a new task.


## q-11944

1. **Specific observation.** Given that $y = \frac{3x + 5}{\ln x}$, find $\frac{dy}{dx}$.

Source rating absent. Numerator `3*x + 5`, denominator `log(x)`, ordered derivatives `3` and `1/x`. The response is radio. Captured prose and complete banks appear verbatim in source-components.json.

2. **General pattern.** Identify u and v in Leibniz notation, differentiate each, substitute the four ordered operands in (v du/dx−u dv/dx)/v², preserve this family’s factor/collection stages, and fill the printed derivative or derivative fragment.

3. **Components and banks.** Anchor slots `{"a": 3, "b": 5}`; complete bank `observed-11944`.

- `(3\ln x - (3x + 5))/(x\ln^{2} x)` → `(a*ln(x)-(a*x+b))/(x*ln(x)^2)`.
- `(3x\ln x - (3x + 5))/(\ln^{2} x)` → `(a*x*ln(x)-(a*x+b))/ln(x)^2`.
- `(3x\ln x - (3x + 5))/(x\ln^{2} x)` → `(a*x*ln(x)-(a*x+b))/(x*ln(x)^2)`.
- `(x\ln x - (3x + 5))/(x\ln^{2} x)` → `(x*ln(x)-(a*x+b))/(x*ln(x)^2)`.
- `(3\ln x - (3x + 5))/(\ln^{2} x)` → `(a*ln(x)-(a*x+b))/ln(x)^2`.

4. **Backbone and slots.** Kind `affine-ln`; exact slot keys `a, b`. Slots are substantive coefficients, log base, or a positive integer power as detailed below. Each slot changes the actual function, both derivative definitions, every substituted factor, every dependent intermediate, the requested fragment/factor and all options. Original anchors are retained. No target-name, choice-order or seed variation counts as a new task.


## q-9909

1. **Specific observation.** Given that $y = \frac{1 + \cos x}{\sin x}$, find $\frac{dy}{dx}$.

Source rating absent. Numerator `cos(x) + 1`, denominator `sin(x)`, ordered derivatives `-sin(x)` and `cos(x)`. The response is radio. Captured prose and complete banks appear verbatim in source-components.json.

2. **General pattern.** Identify u and v in Leibniz notation, differentiate each, substitute the four ordered operands in (v du/dx−u dv/dx)/v², preserve this family’s factor/collection stages, and fill the printed derivative or derivative fragment.

3. **Components and banks.** Anchor slots `{"c": 1}`; complete bank `observed-9909`.

- `\frac{1}{\sin^{2} x}` → `c/sin(x)^2`.
- `\frac{1}{1 - \cos x}` → `c/(1-cos(x))`.
- `-\frac{1}{\sin^{2} x}` → `-c/sin(x)^2`.
- `-\frac{1}{1 + \cos x}` → `-c/(1+cos(x))`.
- `-\frac{1}{1 - \cos x}` → `-c/(1-cos(x))`.

4. **Backbone and slots.** Kind `cos-sin`; exact slot keys `c`. Slots are substantive coefficients, log base, or a positive integer power as detailed below. Each slot changes the actual function, both derivative definitions, every substituted factor, every dependent intermediate, the requested fragment/factor and all options. Original anchors are retained. No target-name, choice-order or seed variation counts as a new task.


## Fixed method, slots and constraints

x remains the independent variable and y the dependent variable because this KP assesses Leibniz notation. u always means the actual displayed numerator and v the actual displayed denominator. Quotient order is v du/dx−u dv/dx with denominator v². Power, trig, exponential and logarithmic derivatives are already present in the lesson/practice. No tangent evaluation, new derivative rule, nested quotient, inverse trig, new answer contract or plot is introduced.

Every integer slot is nonzero with absolute value at most12. q-340336 scales tan x/x² by c while retaining the x⁻³ printed factor and its four-row chain. q-340340 uses c eˣ/(x+b), retaining substitution, unsimplified x+b−1 and final collection. q-340337 scales x/cos x by c and retains the cos⁻² printed factor. q-47994 scales sin x/x by c and preserves its full five-member source profile.

q-11969 varies c x/(a x+b), a,b,c nonzero: its original −x/(9−2x) is an anchor. q-340332 uses c x²/(x²+b), preserving the separate cubic terms before cancellation. q-340341 scales x/ln x by c. q-340343 varies log base b=2..12 and denominator power n=2..4. The source change-of-base equality, quotient substitution, separate logarithmic fractions, common denominator, power factorization, cancellation and final printed factor remain in order. n changes the power-rule coefficient and exponents without adding a rule or operation count. Negative log bases and n=1 are excluded to preserve real domains and the positive-power factorization stage.

q-340335 uses (a−b sin x)/sin x with positive a,b=1..12. Its six quotient rows preserve factoring cos x, cancelling the opposite sine terms, multiplying the remaining constant, splitting reciprocal factors, then csc/cot notation. q-9909 scales (1+cos x)/sin x by a nonzero c; its completed normal chain uses the existing quotient rule followed by the familiar sin²+cos² identity and reciprocal simplification. The source missing rating is assigned hard because this matches the captured hard trig simplification workload; that label is authored. q-11944 uses (a x+b)/ln x, nonzero a,b: its authored moderate completion follows the captured moderate x/ln x chain and clears the inner 1/x denominator.

Within each band these are peer practice families; seed selection has no pedagogical progression. Defaults can select any eligible family. Every family is explicitly selectable for review and replay. Source parameter domains include all positive and negative original values. In q-11944’s observed profile, a=1 makes the fourth source option identical to the correct option; the entire bank is ineligible and is rejected. The authored method profile remains eligible at a=1. Boundary tests preserve and report this collision rather than deleting a bank member. Any invalid or duplicate whole bank rejects the entire sampled instance; no first-valid recipe pool is used.

## Source bank mapping and authored profiles

All four original five-member banks are mapped member by member above and in source-components.json, including all altered coefficients/constants and missing x factors. The mapping formulas reproduce complete mathematical values at original anchors. Historical misconception intent is unresolved where the expression alone does not establish it; learner feedback does not claim an intent. q-11944/q-9909 correct designations are independently derived, not recovered source facts.

An explicitly selectable method profile for radio families is authored as one complete bank: correct quotient rule, addition instead of subtraction, reversed subtraction, unsquared denominator, and quotient of derivatives. Profile selection precedes construction; every wrong value must be wrong as a function on the real source domain, and every pair must be inequivalent. Equivalent isolated point values do not make two derivative functions equivalent. All whole-bank profiles are tested after selection. Normal defaults use the complete observed profile to establish fidelity; authored profiles are distinguishable in metadata and question content IDs.

Blank responses preserve the exact original requested fragment. tan-square and linear-cos expect only a bracket numerator after a supplied factor, log-power expects 1−n ln x before its printed factor, and other blanks expect the entire derivative. 0/1 learner entries are tested as mathematical values without rejection by policy.

## Ordered prose and source replay

Shared sentences are retained: “Let u=… and v=…. Then” followed by both Leibniz derivatives, and “Using the quotient rule, we get” before the ordered equations. Source-specific operative chains are represented by independent literal expected row counts and structural checks in validate.py. The original nine complete solutions are compared mathematically row by row in original order. Full prose, original symbols and erroneous/missing parts remain exact in raw records. The two missing solutions are authored and separately marked. q-340335’s inconsistent dependent-variable label is an explicit repaired source defect.

## Lesson scope

Following :activity/first-step and :step/next in lesson.json gives introduction → polynomial quotients → quotients with other functions → introduction to Leibniz notation → this KP → justification/tangent application. The immediately preceding Leibniz introduction establishes dy/dx notation; the owning topic’s canonical e-3639 sets u,v, computes du/dx,dv/dx, applies quotient rule and collects. This generator stays on that method. The source practice itself contains trig, exponential, log, polynomial and factored fragment contracts at the observed levels. No missing difficulty level needs an invented curriculum branch; both assigned ratings for the two incomplete records are explicitly authored completions.

## Identity and domains

Mathematical identity uses the supplied function, monic square-free polynomial denominator zero-set (fixed trig/log zero-set otherwise) and requested derivative task, excluding seed, choice order and profile. Content IDs include normalized prose, solution, complete bank, level and profile; answer IDs belong to their field. Banks cannot alias one identity. Real domains require denominator nonzero; logarithmic families also require x>0 and log bases positive and unequal1. Source replay retains original parameters, source membership, exact values and correct designation presence separately from normal completion. No source claims depend on a live capture parser or formatter; imports use explicit paths to frozen private copies.
