# First-order ODE verification: repaired decision variation

Source: sibling `source/source.json`, EDB math basis 3683, KP 17592186100888.
The learner differentiates a supplied function, compares that derivative with
statement I, substitutes the actual derivative and function into the ODE, and
decides whether the resulting identity holds on the stated interval. No solving
of an ODE, initial conditions, integration, or new response format is involved.

Tutorial 17592186102031 explicitly says to calculate the derivative and plug the
result into the equation, and demonstrates `y=e^(2x)` against `y'=2y`.
Canonical example 17592186100725 does the same for `1/x` and `y'=-y/x`.
The definition in each solution justifies II and III having the same truth value;
it does not justify fixing that value or the truth of I across a function family.
The source's "equation's domain" wording is narrowed to an interval where both
the function and equation are defined, as the preexisting draft already did.

The nine captured practice cases are retained for explicit source replay with
their entire Boolean banks and original prompts/solutions. Current source fields
are checkboxes I, II, III with both `false` and `true` values; field and option
ordering is not a mathematical constraint. Original labels and difficulties are
preserved in replay:

| Source db id / MA id | Family | Original key |
| --- | --- | --- |
| 17592186101155 / q-140631 | power_easy | FTT |
| 17592186101157 / q-141078 | exp_true | TTT |
| 17592186272196 / q-141080 | sin_none | FFF |
| 17592186272197 / q-141081 | cos_i | TFF |
| 17592186272198 / q-141082 | log_all | TTT |
| 17592186272199 / q-141084 | inverse_none | FFF |
| 17592186272200 / q-141086 | exp_none | FFF |
| 17592186272201 / q-141088 | log_scaled | FTT |
| 17592186272202 / q-141089 | power_moderate | FTT |

These original arrangements are observations, not constraints. Default learning
sampling uses the following conservative extensions. For each family choose the
truth of I and the common truth of II/III independently, then choose compatible
integer coefficients from the same bounded pool. A false coefficient differs in
magnitude, not sign or expression type. The key is subsequently recomputed from
the symbolic function, claim, and ODE rather than copied from the chosen case.
Every family must exercise FFF, FTT, TFF, and TTT; the impossible unequal II/III
combinations are intentionally absent.

* Positive and signed power functions: keep `f=a*x^n`, compare the claimed
  coefficient of `x^(n-1)`, and test `y'=q*y/x`. Easy uses `a=1`; moderate uses
  a negative nonunit integer and retains the explicit coefficient product step.
* Exponential functions: keep `f=a*e^(k*x)` or `a*e^(-k*x)` and compare chain
  coefficients in both the claim and `y'=q*y` (with matching sign). The same
  numerical values can be true or false when the exponent coefficient changes.
* Sine/cosine: the original `sin(kx)/k` versus `y'=k*y`, and `cos(kx)` versus
  `y'=y*cos(kx)`, can never be solutions on an interval for nonzero k. To remove
  that mathematical family-to-answer cue, normal questions use `sin(kx)/b`
  against `y'=(q/b)*cos(kx)` and `cos(kx)` against `y'=-q*sin(kx)`. These retain
  elementary chain differentiation and comparison of a proposed solution with
  an explicit first-order ODE; no extra trigonometric identity is needed. The
  fact that an ODE need not explicitly contain y is an allowed same-method
  extension, not an observed source layout. Original RHS forms remain replay
  evidence only; mixing those always-false forms into normal sampling would
  restore the shortcut.
* Inverse powers: retain `f=-1/x^n`, compare `c/x^(n+1)`, and test `y'=-q*y/x`,
  using the canonical example's RHS structure. The original `y'=y/x^n` is
  replay only because it can never match this family on an interval.
* Logarithms: normal elementary cases use `ln(k*x+h)`, claim `c/(k*x+h)`, and
  `y'=q*e^(-y)` on `k*x+h>0`. A nonunit inner coefficient lets the same visible
  coefficients occur in both true and false cases, while keeping one elementary
  chain derivative and exponential/logarithm cancellation. This extends the
  source `ln(x)`/preexisting shifted-log family; the source sine/exponential
  cases already require one constant inner-chain factor. Scaled-log cases keep
  `2m*ln(x)` and `y'=q*x/e^(y/m)`, with `c/x` as the claim, preserving the source
  cancellation to `q/x` and its successive substitution stages.
* Hard retains the preexisting authored affine-log extension: `a*ln(b*x+c)`,
  nonunit signed a, positive nonunit b, nonzero c, and `y'=q*e^(-y/a)`. Both
  candidate coefficients are signed products of a with independently selected
  members of the same positive pool as b. It needs the outer factor, affine
  chain derivative, and nonlinear substitution; the old hard recipe's opposite
  sign for every false solution was removed. No captured hard example exists,
  so hard remains explicitly an authored extension, not source-observed evidence.

The layouts, three statement roles, domain restrictions, and Boolean banks stay
fixed for instructional/UI reasons. Numeric ranges keep arithmetic comparable;
the exact original source parameters are separately replayable. Same-sign
coefficient changes are substantive evidence, not decorative number changes:
holding f fixed and changing only the claim toggles I; holding f/claim fixed and
changing only the ODE coefficient toggles II/III. Signs, template identity,
field positions, and cardinality are tested within each family. Mathematical
shortcuts such as recognizing the power-rule coefficient are the target skill;
they are not incidental leaks. Coverage after the shared publication filter is
checked separately; actual learner history selection is outside this offline
author check and is not claimed.

Supported bands: easy (eight observed families with stated extensions), moderate
(signed power family), hard (preexisting authored affine-log extension).
No plots are needed. Runtime is a seeded, relocatable Python/SymPy package with
the canonical math formatter vendored and normalization applied before IDs.
