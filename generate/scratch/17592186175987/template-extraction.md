# Template extraction

## Stage 1 — Specific source descriptions

Original fields, choices, keyed answers, prompts and complete worked solutions are retained in source.json, sourced from math basis1356. Each radio family has one historical five-choice bank. The continuation has three supplied-fragment blanks; Pull order is integrand, radius, angle but keys are field-1, field-3, field-2 and uniquely determine each role. Original-bank source shape is preserved in public `generate(..., profile="observed")` replay.

- **q-108544 / constant**: P=3*y - exp(cos(x)), Q=7*x + sqrt(y + 5); radial0..2, angular-pi/2..pi/2. Field cross partials, formal Green operator, substituted difference, source reduction/factorization, polar-domain declaration, change-of-variables formula, polar substitution and source final repeated-integral stages.
- **q-125719 / cubic_y**: P=x**2*cos(x) + y**3, Q=x + y*exp(y + 1); radial0..1, angularpi..3*pi/2. Field cross partials, formal Green operator, substituted difference, source reduction/factorization, polar-domain declaration, change-of-variables formula, polar substitution and source final repeated-integral stages.
- **q-126687 / linear_pair**: P=-x*y + 2*y**2 + 2, Q=x**2 + x*y; radial0..8, angular-pi..pi/2. Field cross partials, formal Green operator, substituted difference, source reduction/factorization, polar-domain declaration, change-of-variables formula, polar substitution and source final repeated-integral stages.
- **q-126710 / factored**: P=y*(x + 1), Q=x*(y + 1); radial0..3, angularpi/2..3*pi/2. Field cross partials, formal Green operator, substituted difference, source reduction/factorization, polar-domain declaration, change-of-variables formula, polar substitution and source final repeated-integral stages.
- **q-126711 / linear_y**: P=x**2 + y**2, Q=x*y + y*exp(y); radial0..1, angular-pi..0. Field cross partials, formal Green operator, substituted difference, source reduction/factorization, polar-domain declaration, change-of-variables formula, polar substitution and source final repeated-integral stages.
- **q-126514 / radial_square**: P=-x**2*y + sin(cos(x)), Q=x*y**2 - 1/(y + 1); radial0..3, angular0..pi. Field cross partials, formal Green operator, substituted difference, source reduction/factorization, polar-domain declaration, change-of-variables formula, polar substitution and source final repeated-integral stages.
- **q-126686 / mixed_cancel**: P=x*y**2 - y*cos(x), Q=2*x**2*y - sin(x); radial0..5, angular0..pi/2. Field cross partials, formal Green operator, substituted difference, source reduction/factorization, polar-domain declaration, change-of-variables formula, polar substitution and source final repeated-integral stages.
- **q-126709 / constant_mixed**: P=x*y**2 + exp(x/4), Q=2*x + exp(sin(y)); radial0..4, angular-pi/2..0. Field cross partials, formal Green operator, substituted difference, source reduction/factorization, polar-domain declaration, change-of-variables formula, polar substitution and source final repeated-integral stages.
- **q-126708 / affine_y**: P=x + y, Q=-x*y; radial0..6, angularpi/2..2*pi. Field cross partials, formal Green operator, substituted difference, source reduction/factorization, polar-domain declaration, change-of-variables formula, polar substitution and source final repeated-integral stages.
- **q-126516 / square_difference**: P=-x + y**3, Q=x**3 + exp(1/y); radial0..1, angular-pi/2..pi. Field cross partials, formal Green operator, substituted difference, source reduction/factorization, polar-domain declaration, change-of-variables formula, polar substitution and source final repeated-integral stages.
- **q-169204 / polar_blanks**: P=None, Q=None; radial0..2, angularpi/2..2*pi. Supplied Cartesian integrand −6xy; double-angle reduction; 3 blanks.

## Stage 2 — Shared mathematical pattern

Identify P,Q (rewriting a vector field when supplied); compute ∂Q/∂x−∂P/∂y; read the positive sector; replace x,y by r cosθ,r sinθ; multiply the integrand by r; supply the complete repeated integral or original fragments. The response criterion for complete-integral choices is equality of the actual definite scalar value: visually different setup formulas can be equivalent answers. Full scalar-value ambiguity checks are independent of native radio ID grading.

## Stage 3 — Every source component and choice mapping

The following source expressions are preserved as complete historical bank patterns. A single scalar observation does not recover author intent. Their explicit replay transformation is common positive field amplitude s multiplying the complete integral and changed radius R in every original radius slot; the source radial-square wrong upper bound2 versus correct3 becomes R−1 (minimum1). These opaque transformations are **evidence-only** and are not normal distractor recipes. They reproduce all choices and keys, not merely the correct answer. BANKS is an independently checked exact mathematical transcription for QA; generator rendering uses source component masks, not a numerical answer lookup table.

### q-108544 / constant

Field `selection`, :answer-field.type/radio

- source distractor: `${\int }_{-\pi /2}^{\pi /2}\operatorname{cos}⁡\theta {\int }_{0}^{2}2r\,dr\,d\theta $`; exact complete object ∫[-pi/2,pi/2]∫[0,2](2*r*cos(theta)) dr dθ; multiplied by s with original radius replaced by R.
- keyed correct: `${\int }_{-\pi /2}^{\pi /2}\,{\int }_{0}^{2}4r\,dr\,d\theta $`; exact complete object ∫[-pi/2,pi/2]∫[0,2](4*r) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{0}^{\pi }\,{\int }_{0}^{2}4r\,dr\,d\theta $`; exact complete object ∫[0,pi]∫[0,2](4*r) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{0}^{\pi }\,{\int }_{0}^{2}({r}^{3}-{e}^{\operatorname{cos}⁡\theta })r\,dr\,d\theta $`; exact complete object ∫[0,pi]∫[0,2](r*(r**3 - exp(cos(theta)))) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{-\pi /2}^{\pi /2}\,{\int }_{0}^{2}({r}^{3}-{e}^{\operatorname{cos}⁡\theta })\,dr\,d\theta $`; exact complete object ∫[-pi/2,pi/2]∫[0,2](r**3 - exp(cos(theta))) dr dθ; multiplied by s with original radius replaced by R.
### q-125719 / cubic_y

Field `selection`, :answer-field.type/radio

- keyed correct: `${\int }_{\pi }^{3\pi /2}\,{\int }_{0}^{1}(1-3{r}^{2}{sin}^{2}⁡\theta )r\,dr\,d\theta $`; exact complete object ∫[pi,3*pi/2]∫[0,1](r*(-3*r**2*sin(theta)**2 + 1)) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{\pi }^{2\pi }\,{\int }_{0}^{1}(1-3{r}^{2}{sin}^{2}⁡\theta )\,dr\,d\theta $`; exact complete object ∫[pi,2*pi]∫[0,1](-3*r**2*sin(theta)**2 + 1) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{\pi }^{2\pi }\,{\int }_{0}^{1}(r-{sin}^{2}⁡\theta )r\,dr\,d\theta $`; exact complete object ∫[pi,2*pi]∫[0,1](r*(r - sin(theta)**2)) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{\pi }^{3\pi /2}\,{\int }_{0}^{1}({r}^{2}-3\operatorname{sin}⁡\theta )\,dr\,d\theta $`; exact complete object ∫[pi,3*pi/2]∫[0,1](r**2 - 3*sin(theta)) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{\pi }^{3\pi /2}\,{\int }_{0}^{1}({r}^{2}-3\operatorname{sin}⁡\theta )r\,dr\,d\theta $`; exact complete object ∫[pi,3*pi/2]∫[0,1](r*(r**2 - 3*sin(theta))) dr dθ; multiplied by s with original radius replaced by R.
### q-126687 / linear_pair

Field `selection`, :answer-field.type/radio

- source distractor: `${\int }_{-\pi }^{\pi /2}\,{\int }_{0}^{8}r(\operatorname{cos}⁡\theta -2\operatorname{sin}⁡\theta )\,dr\,d\theta $`; exact complete object ∫[-pi,pi/2]∫[0,8](r*(-2*sin(theta) + cos(theta))) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{-\pi /2}^{\pi }\,{\int }_{0}^{8}3{r}^{2}\operatorname{cos}⁡\theta \,dr\,d\theta $`; exact complete object ∫[-pi/2,pi]∫[0,8](3*r**2*cos(theta)) dr dθ; multiplied by s with original radius replaced by R.
- keyed correct: `${\int }_{-\pi }^{\pi /2}\,{\int }_{0}^{8}3{r}^{2}(\operatorname{cos}⁡\theta -\operatorname{sin}⁡\theta )\,dr\,d\theta $`; exact complete object ∫[-pi,pi/2]∫[0,8](3*r**2*(-sin(theta) + cos(theta))) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{-\pi }^{\pi /2}\,{\int }_{0}^{8}2{r}^{2}\operatorname{sin}⁡\theta \,dr\,d\theta $`; exact complete object ∫[-pi,pi/2]∫[0,8](2*r**2*sin(theta)) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{-\pi /2}^{\pi }\,{\int }_{0}^{8}r(3\operatorname{cos}⁡\theta -\operatorname{sin}⁡\theta )\,dr\,d\theta $`; exact complete object ∫[-pi/2,pi]∫[0,8](r*(-sin(theta) + 3*cos(theta))) dr dθ; multiplied by s with original radius replaced by R.
### q-126710 / factored

Field `selection`, :answer-field.type/radio

- source distractor: `${\int }_{\pi /2}^{3\pi /2}\,{\int }_{0}^{3}r(\operatorname{cos}⁡\theta -\operatorname{sin}⁡\theta )\,dr\,d\theta $`; exact complete object ∫[pi/2,3*pi/2]∫[0,3](r*(-sin(theta) + cos(theta))) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{\pi /2}^{3\pi /2}\,{\int }_{0}^{3}{r}^{2}(\operatorname{cos}⁡\theta -\operatorname{sin}⁡\theta )\,dr\,d\theta $`; exact complete object ∫[pi/2,3*pi/2]∫[0,3](r**2*(-sin(theta) + cos(theta))) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{-\pi /2}^{\pi /2}\,{\int }_{0}^{3}r(\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta )\,dr\,d\theta $`; exact complete object ∫[-pi/2,pi/2]∫[0,3](r*(sin(theta) - cos(theta))) dr dθ; multiplied by s with original radius replaced by R.
- keyed correct: `${\int }_{\pi /2}^{3\pi /2}\,{\int }_{0}^{3}{r}^{2}(\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta )\,dr\,d\theta $`; exact complete object ∫[pi/2,3*pi/2]∫[0,3](r**2*(sin(theta) - cos(theta))) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{0}^{\pi /2}\,{\int }_{0}^{3}{r}^{2}(\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta )\,dr\,d\theta $`; exact complete object ∫[0,pi/2]∫[0,3](r**2*(sin(theta) - cos(theta))) dr dθ; multiplied by s with original radius replaced by R.
### q-126711 / linear_y

Field `selection`, :answer-field.type/radio

- source distractor: `${\int }_{0}^{\pi /2}\,{\int }_{0}^{1}-r\operatorname{cos}⁡\theta \,dr\,d\theta $`; exact complete object ∫[0,pi/2]∫[0,1](-r*cos(theta)) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{-\pi }^{0}\,{\int }_{0}^{1}r\operatorname{sin}⁡\theta \,dr\,d\theta $`; exact complete object ∫[-pi,0]∫[0,1](r*sin(theta)) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{0}^{\pi /2}\,{\int }_{0}^{1}{r}^{2}\operatorname{sin}⁡\theta \,dr\,d\theta $`; exact complete object ∫[0,pi/2]∫[0,1](r**2*sin(theta)) dr dθ; multiplied by s with original radius replaced by R.
- keyed correct: `${\int }_{-\pi }^{0}\,{\int }_{0}^{1}-{r}^{2}\operatorname{sin}⁡\theta \,dr\,d\theta $`; exact complete object ∫[-pi,0]∫[0,1](-r**2*sin(theta)) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{-\pi }^{0}\,{\int }_{0}^{1}-{r}^{2}\operatorname{cos}⁡\theta \,dr\,d\theta $`; exact complete object ∫[-pi,0]∫[0,1](-r**2*cos(theta)) dr dθ; multiplied by s with original radius replaced by R.
### q-126514 / radial_square

Field `selection`, :answer-field.type/radio

- source distractor: `${\int }_{0}^{\pi }\,{\int }_{0}^{3}r\,dr\,d\theta $`; exact complete object ∫[0,pi]∫[0,3](r) dr dθ; multiplied by s with original radius replaced by R.
- keyed correct: `${\int }_{0}^{\pi }\,{\int }_{0}^{3}{r}^{3}\,dr\,d\theta $`; exact complete object ∫[0,pi]∫[0,3](r**3) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{-\pi /2}^{\pi /2}\,{\int }_{0}^{3}{r}^{3}\,dr\,d\theta $`; exact complete object ∫[-pi/2,pi/2]∫[0,3](r**3) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{-\pi /2}^{\pi /2}\,{\int }_{0}^{3}r\,dr\,d\theta $`; exact complete object ∫[-pi/2,pi/2]∫[0,3](r) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{0}^{\pi }\,{\int }_{0}^{2}(r+\operatorname{sin}⁡(\operatorname{cos}⁡\theta ))\,dr\,d\theta $`; exact complete object ∫[0,pi]∫[0,2](r + sin(cos(theta))) dr dθ; multiplied by s with original radius replaced by R.
### q-126686 / mixed_cancel

Field `selection`, :answer-field.type/radio

- source distractor: `${\int }_{0}^{\pi /2}\,{\int }_{0}^{5}{r}^{3}\operatorname{cos}⁡\theta \,dr\,d\theta $`; exact complete object ∫[0,pi/2]∫[0,5](r**3*cos(theta)) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{0}^{\pi /2}\,{\int }_{0}^{5}{r}^{2}\operatorname{sin}⁡\theta \,dr\,d\theta $`; exact complete object ∫[0,pi/2]∫[0,5](r**2*sin(theta)) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{0}^{\pi }\,{\int }_{0}^{5}{r}^{3}\operatorname{sin}⁡(2\theta )\,dr\,d\theta $`; exact complete object ∫[0,pi]∫[0,5](r**3*sin(2*theta)) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{\pi /2}^{\pi }\,{\int }_{0}^{5}{r}^{2}\operatorname{sin}⁡\theta \,dr\,d\theta $`; exact complete object ∫[pi/2,pi]∫[0,5](r**2*sin(theta)) dr dθ; multiplied by s with original radius replaced by R.
- keyed correct: `${\int }_{0}^{\pi /2}\,{\int }_{0}^{5}{r}^{3}\operatorname{sin}⁡(2\theta )\,dr\,d\theta $`; exact complete object ∫[0,pi/2]∫[0,5](r**3*sin(2*theta)) dr dθ; multiplied by s with original radius replaced by R.
### q-126709 / constant_mixed

Field `selection`, :answer-field.type/radio

- source distractor: `${\int }_{0}^{3\pi /2}\,{\int }_{0}^{4}(2r-{r}^{2}\operatorname{sin}⁡\theta )\,dr\,d\theta $`; exact complete object ∫[0,3*pi/2]∫[0,4](-r**2*sin(theta) + 2*r) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{-\pi /2}^{0}\,{\int }_{0}^{4}(2r{e}^{\operatorname{sin}⁡\theta }-{r}^{2}\operatorname{sin}⁡\theta )\,dr\,d\theta $`; exact complete object ∫[-pi/2,0]∫[0,4](-r**2*sin(theta) + 2*r*exp(sin(theta))) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{0}^{3\pi /2}\,{\int }_{0}^{4}(r{e}^{\operatorname{sin}⁡\theta }-{r}^{3}\operatorname{sin}⁡(2\theta ))\,dr\,d\theta $`; exact complete object ∫[0,3*pi/2]∫[0,4](-r**3*sin(2*theta) + r*exp(sin(theta))) dr dθ; multiplied by s with original radius replaced by R.
- keyed correct: `${\int }_{-\pi /2}^{0}\,{\int }_{0}^{4}(2r-{r}^{3}\operatorname{sin}⁡(2\theta ))\,dr\,d\theta $`; exact complete object ∫[-pi/2,0]∫[0,4](-r**3*sin(2*theta) + 2*r) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{-\pi /2}^{0}\,{\int }_{0}^{4}(2r-{r}^{2}\operatorname{sin}⁡(2\theta ))\,dr\,d\theta $`; exact complete object ∫[-pi/2,0]∫[0,4](-r**2*sin(2*theta) + 2*r) dr dθ; multiplied by s with original radius replaced by R.
### q-126708 / affine_y

Field `selection`, :answer-field.type/radio

- source distractor: `${\int }_{\pi /2}^{2\pi }\,{\int }_{0}^{6}(-2{r}^{2}\operatorname{sin}⁡\theta -1)\,dr\,d\theta $`; exact complete object ∫[pi/2,2*pi]∫[0,6](-2*r**2*sin(theta) - 1) dr dθ; multiplied by s with original radius replaced by R.
- keyed correct: `${\int }_{\pi /2}^{2\pi }\,{\int }_{0}^{6}(-{r}^{2}\operatorname{sin}⁡\theta -r)\,dr\,d\theta $`; exact complete object ∫[pi/2,2*pi]∫[0,6](-r**2*sin(theta) - r) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{0}^{\pi /2}\,{\int }_{0}^{6}({r}^{3}\operatorname{sin}⁡\theta -r)\,dr\,d\theta $`; exact complete object ∫[0,pi/2]∫[0,6](r**3*sin(theta) - r) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{\pi /2}^{2\pi }\,{\int }_{0}^{6}(-{r}^{2}\operatorname{sin}⁡\theta -1)\,dr\,d\theta $`; exact complete object ∫[pi/2,2*pi]∫[0,6](-r**2*sin(theta) - 1) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{0}^{\pi /2}\,{\int }_{0}^{6}(-2{r}^{2}\operatorname{sin}⁡\theta -r)\,dr\,d\theta $`; exact complete object ∫[0,pi/2]∫[0,6](-2*r**2*sin(theta) - r) dr dθ; multiplied by s with original radius replaced by R.
### q-126516 / square_difference

Field `selection`, :answer-field.type/radio

- source distractor: `${\int }_{-\pi /2}^{\pi }\,{\int }_{0}^{1}2{r}^{2}\operatorname{cos}⁡\theta \,dr\,d\theta $`; exact complete object ∫[-pi/2,pi]∫[0,1](2*r**2*cos(theta)) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{\pi /2}^{2\pi }\,{\int }_{0}^{1}2{r}^{2}\operatorname{cos}⁡(\theta )\,dr\,d\theta $`; exact complete object ∫[pi/2,2*pi]∫[0,1](2*r**2*cos(theta)) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{\pi /2}^{2\pi }\,{\int }_{0}^{1}2{r}^{2}\operatorname{sin}⁡\theta \,dr\,d\theta $`; exact complete object ∫[pi/2,2*pi]∫[0,1](2*r**2*sin(theta)) dr dθ; multiplied by s with original radius replaced by R.
- source distractor: `${\int }_{-\pi /2}^{\pi }\,{\int }_{0}^{1}3{r}^{3}\operatorname{sin}⁡(2\theta )\,dr\,d\theta $`; exact complete object ∫[-pi/2,pi]∫[0,1](3*r**3*sin(2*theta)) dr dθ; multiplied by s with original radius replaced by R.
- keyed correct: `${\int }_{-\pi /2}^{\pi }\,{\int }_{0}^{1}3{r}^{3}\operatorname{cos}⁡(2\theta )\,dr\,d\theta $`; exact complete object ∫[-pi/2,pi]∫[0,1](3*r**3*cos(2*theta)) dr dθ; multiplied by s with original radius replaced by R.
### q-169204 / polar_blanks

Field `field-1`, :answer-field.type/blank

- keyed correct: `$-3{r}^{3}\operatorname{sin}(2\theta )$`; fragment transformed according to role: integrand×s, radial boundR, angular bound2π.
Field `field-3`, :answer-field.type/blank

- keyed correct: `$2$`; fragment transformed according to role: integrand×s, radial boundR, angular bound2π.
Field `field-2`, :answer-field.type/blank

- keyed correct: `$2\pi $`; fragment transformed according to role: integrand×s, radial boundR, angular bound2π.

## Stage 4 — Reusable recipes, constraints and normalization

Fixed: complete source prose, theorem formula, variable roles, order/count of every operative stage, grouped subtraction/cancellation/factorization/double-angle operations and angular-sector family. Variable: common positive amplitude s and meaningful radius R. Every math block has a complete component recipe; no replacement of isolated x/y/digits occurs. At s=1, original R, source raw replay restores exactly every prompt/solution/choice string, field type/key/count and correct designation. At changed s, numerical expressions are grouped behind the common amplitude; formal ∂Q/∂x−∂P/∂y is not scaled a second time because it already refers to the scaled P,Q. Every displayed stage is independently parsed and verified against the actual printed field.

Normal radio banks are complete authored profiles chosen before sampling. For the constant family, the dedicated complete bank is correct; reversed curl; omittedQx (−Py); omitted−Py (Qx); Qx+Py. This avoids the missing-Jacobian collision at its observed radius2, preserves original geometry in eligible normal output, and follows the assessed cross-partial operations. Standard five-option profile for the other nonzero families: correct curl×r; reversed curl×r; omitted Jacobian; using Qx+Py instead of Qx−Py; correct integrand over radiusR+1. The square-difference family has a zero integral for its sector, so sign reversal/missing-Jacobian/radius change remain zero and cannot serve as distractors. Its separately eligible complete profile uses correct; omitted−Py; omittedQx; Qx+Py; Qx+Py without Jacobian. Every complete integral is evaluated exactly for polynomial/trig forms and by independently converged 80/120-node Gauss quadratures for non-polynomial wrong sums. A collision rejects the entire instance; explicit inputs raise rather than being changed.

No feedback/distractor diagnosis is added to learner prose. Each question has one fixed solution, independent of chosen error. At normal s=1, original radius, standard source prose and all valid mathematical chains remain unchanged; the two supported repairs below alter only their invalid source components.

## Source errors and repairs

- q-108544: correct constant-curl integrals over right and upper half-disks both equal8π. Two source answers satisfy the requested equivalence criterion.
- q-126514: both r³ integrals over the upper and right half-disks equal81π/4; r distractors over those same intervals also equal9π/2.
- q-126710: reversed-curl/no-Jacobian integrals over different left/right half-disks both equal−9, duplicating two distractors.
- q-126686: the two r²sinθ distractors over quadrants I and II both equal125/3. Additionally its r³cosθ distractor and keyed r³sin(2θ) integral over quadrantI both equal625/4, so the keyed answer is not unique.
- q-126516: the two 2r²cosθ and 2r²sinθ options over [π/2,2π] both equal−2/3. Additionally e^(1/y) is undefined on y=0 in the region/boundary, so the original line integral and asserted Green conditions are invalid. Normal replaces the entire held-y term with e^y in prompt and all solution occurrences; this preserves Qx and intended task.
- q-125719: the applying-Green row writes minusQ dy, while prompt, initial rewrite and derivatives use plusQ dy. Normal minimally repairs that row; exact raw evidence retains it.
- q-169204: 'previous part' refers to an unseen region. Normal adds the exact sector diagram and explicit bounded-region context, preserving supplied curl and each original fragment/key. Raw retains the continuation text.

Historical bank ambiguity and mathematical validity are separate from source-string fidelity. All historical profiles carry evidence_only=true and eligible_for_learning=false, including the source banks whose choices are valid; normal profiles are independently supported method-derived banks. No ambiguous historical bank is promoted to default practice.

## Identity and scope

Content identity hashes actual level, prompt, fixed solution, complete bank, field layout and keyed correct value; seed/order and unused parameter aliases cannot change it. Mathematical identity hashes assessed field/partial information, meaningful sector/radius, and response demand, excluding profile and notation-only aliases. Source fixed null-coordinate terms participate in assessed recognition, and there are no unused public coefficient slots. Random family selection covers every source family. All public explicit parameters obey the same arithmetic bounds as samplers.

Native grader evidence: 52 accepted checks,145 rejected checks and3 explicitly documented unresolved product/double-angle equivalents were measured in the initial full run. The final totals are in validation.json and engine-report.json. Each integrand blank accepts its canonical double-angle form and an independently distributed equivalent (−s r³sin(2θ)−2s r³sin(2θ)); the mathematically equal product form −6s r³sinθcosθ returns a supported-rules equivalence error. No engine changes or silent passes were made.

Presentation v2: normal q-169204 removes capture indentation and unused blank lines, displaying one supplied partial-integral equation with field-1 outside math delimiters, followed by a=field-2 (angular bound) and b=field-3 (radial bound). Native field-array order remains field-1,field-3,field-2. Raw observed replay retains the exact captured whitespace. Regressions reject code-block indentation, swapped a/b keys and widgets inside math delimiters.
