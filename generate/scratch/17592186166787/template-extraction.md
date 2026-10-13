# Template extraction

## Individual sources

q-95548: “What is $\displaystyle \int\frac{csch^{2} x}{3\coth x + 1}dx$?” Real independent variable x. The numerator is a squared reciprocal hyperbolic function; the denominator is an affine coth expression with integer scale 3 and shift +1. One radio selection field and five complete indefinite-antiderivative choices include additive C. There is no plot, feedback, key or worked solution. The exact bare csch notation is preserved in replay and normalized to a defined TeX command in new variants.

q-95551: “Evaluate the integral $\displaystyle \int_{0}^{\ln 2}\frac{\cosh x}{3 + \sinh x}dx$.” Bounds are 0 and the logarithm of the positive integer 2; numerator is cosh, denominator has a positive constant shift 3. One radio selection field and five exact logarithmic constants, with no additive C. There is no plot, feedback, key or solution. The key follows from sinh(ln 2)=3/4, giving ln(5/4).

Canonical e-8408: u=cosh(x²), du=2x sinh(x²) dx, result (1/2)ln(cosh(x²))+C. The full observed solution remains in source.edn and source.json. It supports substitution scope but introduces no new practice template or inventory item.

## Generalized patterns and components

Indefinite family: substitute u=a coth x+1 in ∫csch² x/(a coth x+1) dx; since u'=-a csch² x, answer is -(1/a)ln|a coth x+1|+C. Domain is each connected real interval where x≠0 and a coth x+1≠0. With a≥2 the latter exclusion adds no real singularity. Preserve original question sentence, field layout, five options and additive constant shape. Fixed: +1, numerator, variable, type/key, bank profile. Variable: integer denominator scale a, coefficients and arguments of all five expressions. The source scale is 3; proposed bounded sampler is a=2..12. Bounds are authored and cover the original scale.

Definite family: ∫₀^(ln n)cosh x/(3+sinh x) dx; substitute u=3+sinh x and compute the bounds as 3 and R=3+(n-1/n)/2. The answer is ln(R/3). Domain is [0,ln n] for n=2..12; denominator and logarithm arguments are positive. Fixed: shift 3, numerator, lower bound, radio layout/key. Variable: upper log bound, exact transformed upper endpoint and five bank values. The observed n is 2. Proposed integer n=2..12 is an explicitly bounded extension.

No supplied solution sequence exists for either source. Authored fixed worked solutions show substitution, derivative relation, reciprocal integral or converted bounds, and substitution back or endpoint evaluation. No option-specific feedback is invented.

## Complete bank mapping

Every source option is listed in source order. These are observed expression-shape extensions, not established author mistake recipes. Profiles are never pooled. At original parameters the raw values replay byte-for-byte; generated variants normalize csch TeX notation and fraction layout, with mathematical equality checked separately.

| q-95548 option | Exact observed value | Parameterized complete value | Full replay |
|---|---|---|---|
| 1 | -\frac{1}{2}\ln \mid 3\coth x - 1 \mid + C | -(1/2)ln\|a coth x-1\|+C | yes |
| 2 | \frac{1}{3}\ln \mid 3csch x + 1 \mid + C | (1/a)ln\|a csch x+1\|+C | yes |
| 3 | -\frac{1}{3}\ln \mid 3\coth x + 1 \mid + C | -(1/a)ln\|a coth x+1\|+C | yes; derived key |
| 4 | \frac{1}{2}\ln \mid 3csch^{2} x + 1 \mid + C | (1/2)ln\|a csch² x+1\|+C | yes |
| 5 | -\frac{1}{3}\ln \mid csch^{2} x \mid + C | -(1/a)ln\|csch² x\|+C | yes |

| q-95551 option | Exact observed value | Parameterized complete value | Full replay |
|---|---|---|---|
| 1 | \ln (\frac{2}{3}) | ln(n/(n+1)) | yes |
| 2 | \ln 4 | ln(n²) | yes |
| 3 | 3\ln (\frac{4}{5}) | 3ln(n²/(n²+1)) | yes |
| 4 | \ln (\frac{5}{4}) | ln((3+(n-1/n)/2)/3) | yes; derived key |
| 5 | \ln (\frac{3}{3}) | ln(3/3) | yes |

The distractor source intent is unresolved: more than one mathematical recipe can explain a single observed expression. The stated extensions preserve the complete shapes, are narrower than arbitrary hyperbolic integration, and are exhaustively checked for uniqueness and exactly one correct answer throughout the finite domain. No unmapped, extra or excluded source options remain.

## Distinctness and limits

Indefinite tasks differ by the coefficient of coth in the actual integrand. Definite tasks differ by the integration endpoint. UUIDs are derived from these mathematical fingerprints; seed and option order do not change identity. Source tasks and the canonical example are excluded from new-content selection. Each level has 11 bounded tasks, of which 10 can be new relative to these sources. Extra variants outside this policy require new validation. Hard is unsupported, not filled.
