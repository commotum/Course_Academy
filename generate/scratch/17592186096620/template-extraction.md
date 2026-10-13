# Differentiating a Quotient of Two Polynomials

Source basis 1981. Each source retains its exact question, bank, identities and solution in source.json and reference/source.edn. Source structures remain separate even where their algebra overlaps.

## q-11955

Source 17592186097024: :question.difficulty/easy; constant-linear; radio; profile `observed-11955`; 3 quotient rows.

Observed parameters: `{"c": -2, "a": 4, "b": -9}`. Numerator `-2`; denominator `4*x - 9`; exact derivative `8/(16*x**2 - 72*x + 81)`.

Captured prompt and complete response shape support this family.

Shared mathematical pattern: differentiate the displayed polynomial quotient using the numerator and denominator derivatives, in the original subtraction order, then simplify on the original nonzero-denominator domain.

- `\frac{8}{9{(4x-9)}^{2}}` → `(-c*a/(-b))/(a*x+b)^2`; complete value reproduced; incorrect.
- `\frac{2}{{(4x-9)}^{2}}` → `(-c)/(a*x+b)^2`; complete value reproduced; incorrect.
- `\frac{8}{{(4x-9)}^{2}}` → `(-c*a)/(a*x+b)^2`; complete value reproduced; correct.
- `\frac{1}{{(4x-9)}^{2}}` → `(-c/2)/(a*x+b)^2`; complete value reproduced; incorrect.
- `-\frac{4}{{(4x-9)}^{2}}` → `(-a)/(a*x+b)^2`; complete value reproduced; incorrect.

## q-11966

Source 17592186097025: unrated; linear-linear; radio; profile `observed-11966`; 4 quotient rows.

Observed parameters: `{"c": -5, "a": 2, "b": -1}`. Numerator `-5*x`; denominator `2*x - 1`; exact derivative `5/(4*x**2 - 4*x + 1)`.

Unrated source without solution/correct ref; easy analog q-340297; correct designation computed.

Shared mathematical pattern: differentiate the displayed polynomial quotient using the numerator and denominator derivatives, in the original subtraction order, then simplify on the original nonzero-denominator domain.

- `(10x + 5)/((2x - 1)^{2})` → `(-c*a*x+c*b)/(a*x+b)^2`; complete value reproduced; incorrect.
- `(20x + 5)/((2x - 1)^{2})` → `(-2*c*a*x+c*b)/(a*x+b)^2`; complete value reproduced; incorrect.
- `(5)/((2x - 1)^{2})` → `(c*b)/(a*x+b)^2`; complete value reproduced; correct.
- `(5 - 10x)/((2x - 1)^{2})` → `(c*b+c*a*x)/(a*x+b)^2`; complete value reproduced; incorrect.
- `- (5)/((2x - 1)^{2})` → `(-c*b)/(a*x+b)^2`; complete value reproduced; incorrect.

## q-104305

Source 17592186233084: :question.difficulty/easy; constant-quadratic; blank; profile `fragment`; 3 quotient rows.

Observed parameters: `{"c": 10, "a": -1, "b": 0, "d": 3}`. Numerator `10`; denominator `3 - x**2`; exact derivative `20*x/(x**4 - 6*x**2 + 9)`.

Missing source field; explicit blank extension from observed blank response shape.

Shared mathematical pattern: differentiate the displayed polynomial quotient using the numerator and denominator derivatives, in the original subtraction order, then simplify on the original nonzero-denominator domain.



## q-104309

Source 17592186233085: :question.difficulty/easy; affine-quadratic; blank; profile `fragment`; 5 quotient rows.

Observed parameters: `{"c": -2, "e": 3, "a": 2, "b": 0, "d": -2}`. Numerator `3 - 2*x`; denominator `2*x**2 - 2`; exact derivative `(x**2 - 3*x + 1)/(x**4 - 2*x**2 + 1)`.

Missing source field; explicit blank extension from observed blank response shape.

Shared mathematical pattern: differentiate the displayed polynomial quotient using the numerator and denominator derivatives, in the original subtraction order, then simplify on the original nonzero-denominator domain.



## q-340290

Source 17592186233906: :question.difficulty/easy; constant-monomial; blank; profile `fragment`; 4 quotient rows.

Observed parameters: `{"c": 2}`. Numerator `2`; denominator `x**2`; exact derivative `-4/x**3`.

Captured prompt and complete response shape support this family.

Shared mathematical pattern: differentiate the displayed polynomial quotient using the numerator and denominator derivatives, in the original subtraction order, then simplify on the original nonzero-denominator domain.

- `-\frac{4}{{x}^{3}}` → `diff(u/v,x)`; complete value reproduced; correct.

## q-128235

Source 17592186235353: :question.difficulty/easy; symbolic-quadratic; blank; profile `fragment`; 4 quotient rows.

Observed parameters: `{"e": -2, "b": 4}`. Numerator `x - 2`; denominator `k + x**2 + 4*x`; exact derivative `(k - x**2 + 4*x + 8)/(k**2 + 2*k*x**2 + 8*k*x + x**4 + 8*x**3 + 16*x**2)`.

Source prompt omits function; supply u/v definitions from captured solution. k is constant.

Shared mathematical pattern: differentiate the displayed polynomial quotient using the numerator and denominator derivatives, in the original subtraction order, then simplify on the original nonzero-denominator domain.

- `\frac{-{x}^{2}+4x+k+8}{{({x}^{2}+4x+k)}^{2}}` → `diff(u/v,x)`; complete value reproduced; correct.

## q-128335

Source 17592186235369: :question.difficulty/easy; constant-quadratic; blank; profile `fragment`; 4 quotient rows.

Observed parameters: `{"c": 7, "a": 2, "b": -5, "d": -3}`. Numerator `7`; denominator `2*x**2 - 5*x - 3`; exact derivative `(35 - 28*x)/(4*x**4 - 20*x**3 + 13*x**2 + 30*x + 9)`.

Source prompt omits function; supply u/v definitions from captured solution.

Shared mathematical pattern: differentiate the displayed polynomial quotient using the numerator and denominator derivatives, in the original subtraction order, then simplify on the original nonzero-denominator domain.

- `\frac{7(5-4x)}{{(2{x}^{2}-5x-3)}^{2}}` → `diff(u/v,x)`; complete value reproduced; correct.

## q-340287

Source 17592186314921: :question.difficulty/easy; constant-unit-linear; blank; profile `fragment`; 4 quotient rows.

Observed parameters: `{"c": 1, "b": 1}`. Numerator `1`; denominator `x + 1`; exact derivative `-1/(x**2 + 2*x + 1)`.

Captured prompt and complete response shape support this family.

Shared mathematical pattern: differentiate the displayed polynomial quotient using the numerator and denominator derivatives, in the original subtraction order, then simplify on the original nonzero-denominator domain.

- `-\frac{1}{{(x+1)}^{2}}` → `diff(u/v,x)`; complete value reproduced; correct.

## q-340297

Source 17592186314923: :question.difficulty/easy; linear-linear; blank; profile `fragment`; 4 quotient rows.

Observed parameters: `{"c": 6, "a": -3, "b": 1}`. Numerator `6*x`; denominator `1 - 3*x`; exact derivative `6/(9*x**2 - 6*x + 1)`.

Captured prompt and complete response shape support this family.

Shared mathematical pattern: differentiate the displayed polynomial quotient using the numerator and denominator derivatives, in the original subtraction order, then simplify on the original nonzero-denominator domain.

- `\frac{6}{{(1-3x)}^{2}}` → `diff(u/v,x)`; complete value reproduced; correct.

## q-340298

Source 17592186314924: :question.difficulty/easy; square-linear; blank; profile `fragment`; 4 quotient rows.

Observed parameters: `{"b": 1}`. Numerator `x**2`; denominator `x + 1`; exact derivative `(x**2 + 2*x)/(x**2 + 2*x + 1)`.

Captured prompt and complete response shape support this family.

Shared mathematical pattern: differentiate the displayed polynomial quotient using the numerator and denominator derivatives, in the original subtraction order, then simplify on the original nonzero-denominator domain.

- `\frac{{x}^{2}+2x}{(x+1)^{2}}` → `diff(u/v,x)`; complete value reproduced; correct.

## q-340303

Source 17592186314926: :question.difficulty/easy; linear-unit-quadratic; blank; profile `fragment`; 4 quotient rows.

Observed parameters: `{"b": 1}`. Numerator `x`; denominator `x**2 + 1`; exact derivative `(1 - x**2)/(x**4 + 2*x**2 + 1)`.

Captured prompt and complete response shape support this family.

Shared mathematical pattern: differentiate the displayed polynomial quotient using the numerator and denominator derivatives, in the original subtraction order, then simplify on the original nonzero-denominator domain.

- `\frac{1-{x}^{2}}{({x}^{2}+1)^{2}}` → `diff(u/v,x)`; complete value reproduced; correct.

No mixed profiles. Blank fragments contain no inferred feedback or distractors. Rendered notation/whitespace is normalized; this version does not claim exact source text fidelity. The original shared prose and ordered quotient-rule stages are retained; repairs and missing-field extensions are explicit. q-11966 has no original solution to preserve. Canonical example e-3637 supports a cancellation domain restriction but is not a practice template or available inventory.
