# Template extraction

Capture provenance is preserved in source.json: math, basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. No original authoring code was recovered. Explicit observed profiles reproduce complete banks; hypotheses about error intent are not promoted to default generation.

## Stage 1 — each specific source

### q-80679

Calculate the vertical asymptotes of $f(x)=\frac{1}{{x}^{2}-4x+5}.$

Level: easy. Family: quadratic. Original parameters: `{"a": 1, "b": -4, "c": 5, "n": 1}`. Numerator: `1`; denominator: `x**2 - 4*x + 5`; irreducible quadratic: `x**2 - 4*x + 5`; real-root set: `[]`.

Field layout: one :answer-field.type/radio field, key `selection`.

Full worked sequence (captured verbatim, including any anomaly):

To find the vertical asymptotes of a rational function, we factor the numerator and denominator and cancel any common factors. Then, we set the denominator equal to zero and solve for $x.$

There are no common factors in the numerator and denominator, so we set the denominator equal to zero. This gives

$$
{x}^{2}-4x+5=0.
$$

Note that the above equation has no real solutions because the discriminant $D$ is negative:

$$
\begin{aligned}D & ={b}^{2}-4ac \\  & =(-4{)}^{2}-4(1)(5) \\  & =16-20 \\  & =-4\end{aligned}
$$

Therefore, $y=f(x)$ has no vertical asymptotes.

### q-80680

Calculate the vertical asymptotes of $f(x)=\frac{x+1}{{x}^{2}+3x+4}.$

Level: easy. Family: quadratic. Original parameters: `{"a": 1, "b": 3, "c": 4, "n": 1}`. Numerator: `x + 1`; denominator: `x**2 + 3*x + 4`; irreducible quadratic: `x**2 + 3*x + 4`; real-root set: `[]`.

Field layout: **fieldless capture**; the original profile must omit the attribute.

Full worked sequence (captured verbatim, including any anomaly):

To find the vertical asymptotes of a rational function, we factor the numerator and denominator and cancel any common factors. Then, we set the denominator equal to zero and solve for $x:$

Note that the equation ${x}^{2}+3x+4=0$ has no real solutions because the discriminant $D$ is negative:

$$
\begin{aligned}D & ={b}^{2}-4ac \\  & ={3}^{2}-4(1)(4) \\  & =9-16 \\  & =-7\end{aligned}
$$

Therefore, $y=f(x)$ has no vertical asymptotes.

### q-6912

Determine the vertical asymptotes of $f(x)=\frac{2x}{3{x}^{2}+1}.$

Level: easy. Family: quadratic. Original parameters: `{"a": 3, "b": 0, "c": 1, "n": 2}`. Numerator: `2*x`; denominator: `3*x**2 + 1`; irreducible quadratic: `3*x**2 + 1`; real-root set: `[]`.

Field layout: one :answer-field.type/radio field, key `selection`.

Full worked sequence (captured verbatim, including any anomaly):

To find the vertical asymptotes of a rational function, we factor the numerator and denominator and cancel any common factors. Then, we set the denominator equal to zero and solve for $x.$

There are no common factors in the numerator and denominator, so we set the denominator equal to zero. This gives

$$
3{x}^{2}+1=0
$$

This equation does not have any real solutions. Therefore, $f(x)$ does not have any vertical asymptotes.

### q-39795

Calculate the vertical asymptotes of $f(x)=\frac{5}{{x}^{3}+{x}^{2}+x}.$

Level: moderate. Family: gcf. Original parameters: `{"a": 1, "b": 1, "c": 1, "n": 5}`. Numerator: `5`; denominator: `x**3 + x**2 + x`; irreducible quadratic: `x**2 + x + 1`; real-root set: `[0]`.

Field layout: one :answer-field.type/radio field, key `selection`.

Full worked sequence (captured verbatim, including any anomaly):

To find the vertical asymptotes of a rational function, we factor the numerator and denominator and cancel any common factors. Then, we set the denominator equal to zero and solve for $x.$

Factoring the numerator and denominator, we get

$$
\begin{aligned}f(x) & =\frac{5}{{x}^{3}+{x}^{2}+x} \\  & =\frac{5}{x({x}^{2}+x+1)}.\end{aligned}
$$

There are no common factors in the numerator and denominator, so we set the denominator equal to zero. This gives

$$
x({x}^{2}+x+1)=0.
$$

We now solve the above equation using the zero product property:

- Solving $2x=0$ gives the solution $x=0.$

- The equation ${x}^{2}+x+1=0$ has no real solutions because the discriminant $D$ is negative:

$$
\begin{aligned}D & ={b}^{2}-4ac \\  & ={1}^{2}-4(1)(1) \\  & =1-4 \\  & =-3.\end{aligned}
$$

Therefore, the only vertical asymptote is $x=0.$

### q-113525

Calculate the vertical asymptotes of $f(x)=\frac{3}{{x}^{3}+{x}^{2}+7x}.$

Level: moderate. Family: gcf. Original parameters: `{"a": 1, "b": 1, "c": 7, "n": 3}`. Numerator: `3`; denominator: `x**3 + x**2 + 7*x`; irreducible quadratic: `x**2 + x + 7`; real-root set: `[0]`.

Field layout: one :answer-field.type/radio field, key `selection`.

Full worked sequence (captured verbatim, including any anomaly):

To find the vertical asymptotes of a rational function, we factor the numerator and denominator and cancel any common factors. Then, we set the denominator equal to zero and solve for $x.$

Factoring the numerator and denominator, we get

$$
\begin{aligned}f(x) & =\frac{3}{{x}^{3}+{x}^{2}+7x} \\  & =\frac{3}{x({x}^{2}+x+7)}.\end{aligned}
$$

There are no common factors in the numerator and denominator, so we set the denominator equal to zero. This gives

$$
x({x}^{2}+x+7)=0.
$$

We now solve the above equation using the zero product property:

- Solving $x=0$ gives the solution $x=0.$

- The equation ${x}^{2}+x+7=0$ has no real solutions because the discriminant $D$ is negative:

$$
\begin{aligned}D & ={b}^{2}-4ac \\  & ={1}^{2}-4(1)(7) \\  & =1-28 \\  & =-27.\end{aligned}
$$

Therefore, the only vertical asymptote is $x=0.$

### q-113523

Calculate the vertical asymptotes of $f(x)=\frac{2x+4}{{x}^{3}-{x}^{2}+3x-3}.$

Level: moderate. Family: group. Original parameters: `{"a": 1, "c": 3, "r": 1, "n": 2, "s": 2}`. Numerator: `2*x + 4`; denominator: `x**3 - x**2 + 3*x - 3`; irreducible quadratic: `x**2 + 3`; real-root set: `[1]`.

Field layout: **fieldless capture**; the original profile must omit the attribute.

Full worked sequence (captured verbatim, including any anomaly):

To find the vertical asymptotes of a rational function, we factor the numerator and denominator and cancel any common factors. Then, we set the denominator equal to zero and solve for $x.$

Factoring the numerator and denominator, we get

$$
\begin{aligned}f(x) & =\frac{2x+4}{{x}^{3}-{x}^{2}+3x-3} \\  & =\frac{2(x+2)}{{x}^{2}(x-1)+3(x-1)} \\  & =\frac{2(x+2)}{({x}^{2}+3)(x-1)}.\end{aligned}
$$

There are no common factors in the numerator and denominator, so we set the denominator equal to zero. This gives

$$
({x}^{2}+3)(x-1)=0.
$$

We now solve the above equation using the zero product property:

- Solving $x-1=0$ gives the solution $x=1.$

- The equation ${x}^{2}+3=0$ has no real solutions.

Therefore, the only vertical asymptote is $x=1.$

### q-278551

The vertical asymptote of $f(x)=\frac{4}{2{x}^{3}-2{x}^{2}+x-1}$ is $x=${{field-1}}.

Level: moderate. Family: group. Original parameters: `{"a": 2, "c": 1, "r": 1, "n": 4}`. Numerator: `4`; denominator: `2*x**3 - 2*x**2 + x - 1`; irreducible quadratic: `2*x**2 + 1`; real-root set: `[1]`.

Field layout: one :answer-field.type/blank field, key `field-1`.

Full worked sequence (captured verbatim, including any anomaly):

To find the vertical asymptotes of a rational function, we factor the numerator and denominator and cancel any common factors. Then, we set the denominator equal to zero and solve for $x.$

Factoring the numerator and denominator, we get

$$
\begin{aligned}f(x) & =\frac{4}{2{x}^{3}-2{x}^{2}+x-1} \\  & =\frac{4}{2{x}^{2}(x-1)+(x-1)} \\  & =\frac{4}{(2{x}^{2}+1)(x-1)}.\end{aligned}
$$

There are no common factors in the numerator and denominator, so we set the denominator equal to zero. This gives

$$
(2{x}^{2}+1)(x-1)=0.
$$

We now solve the above equation using the zero product property:

- Solving $x-1=0$ gives the solution $x=1.$

- The equation $2{x}^{2}+1=0$ has no real solutions.

Therefore, the vertical asymptote is $x=1.$

### q-270003

The vertical asymptote of $f(x)=\frac{2x-3}{{x}^{3}-4{x}^{2}+5x-20}$ is $x=${{field-1}}.

Level: moderate. Family: group. Original parameters: `{"a": 1, "c": 5, "r": 4, "n": 2, "s": 3}`. Numerator: `2*x - 3`; denominator: `x**3 - 4*x**2 + 5*x - 20`; irreducible quadratic: `x**2 + 5`; real-root set: `[4]`.

Field layout: one :answer-field.type/blank field, key `field-1`.

Full worked sequence (captured verbatim, including any anomaly):

To find the vertical asymptotes of a rational function, we factor the numerator and denominator and cancel any common factors. Then, we set the denominator equal to zero and solve for $x.$

Factoring the numerator and denominator, we get

$$
\begin{aligned}f(x) & =\frac{2x-3}{{x}^{3}-4{x}^{2}+5x-20} \\  & =\frac{2x-3}{{x}^{2}(x-4)+5(x-4)} \\  & =\frac{2x-3}{({x}^{2}+5)(x-4)}.\end{aligned}
$$

There are no common factors in the numerator and denominator, so we set the denominator equal to zero. This gives

$$
({x}^{2}+5)(x-4)=0.
$$

We now solve the above equation using the zero product property:

- Solving $x-4=0$ gives the solution $x=4.$

- The equation ${x}^{2}+5=0$ has no real solutions.

Therefore, the vertical asymptote is $x=4.$

### q-80676

Calculate the vertical asymptotes of $f(x)=\frac{2x-1}{{x}^{3}-2{x}^{2}+4x-8}.$

Level: moderate. Family: group. Original parameters: `{"a": 1, "c": 4, "r": 2, "n": 2, "s": 1}`. Numerator: `2*x - 1`; denominator: `x**3 - 2*x**2 + 4*x - 8`; irreducible quadratic: `x**2 + 4`; real-root set: `[2]`.

Field layout: one :answer-field.type/radio field, key `selection`.

Full worked sequence (captured verbatim, including any anomaly):

To find the vertical asymptotes of a rational function, we factor the numerator and denominator and cancel any common factors. Then, we set the denominator equal to zero and solve for $x.$

Factoring the numerator and denominator, we get

$$
\begin{aligned}f(x) & =\frac{2x-1}{{x}^{3}-2{x}^{2}+4x-8} \\  & =\frac{2x-1}{{x}^{2}(x-2)+4(x-2)} \\  & =\frac{2x-1}{({x}^{2}+4)(x-2)}.\end{aligned}
$$

There are no common factors in the numerator and denominator, so we set the denominator equal to zero. This gives

$$
({x}^{2}+4)(x-2)=0.
$$

We now solve the above equation using the zero product property:

- Solving $x-2=0$ gives the solution $x=2.$

- The equation ${x}^{2}+4=0$ has no real solutions.

Therefore, the only vertical asymptote is $x=2.$

### q-113527

Determine the vertical asymptotes of $f(x)=\frac{{x}^{2}-9}{{x}^{3}-2{x}^{2}+6x-12}.$

Level: moderate. Family: group. Original parameters: `{"a": 1, "c": 6, "r": 2, "s": 3}`. Numerator: `x**2 - 9`; denominator: `x**3 - 2*x**2 + 6*x - 12`; irreducible quadratic: `x**2 + 6`; real-root set: `[2]`.

Field layout: one :answer-field.type/radio field, key `selection`.

Full worked sequence (captured verbatim, including any anomaly):

To find the vertical asymptotes of a rational function, we factor the numerator and denominator and cancel any common factors. Then, we set the denominator equal to zero and solve for $x:$

Factoring the numerator and denominator, we get

$$
\begin{aligned}f(x) & =\frac{{x}^{2}-9}{{x}^{3}-2{x}^{2}+6x-12} \\  & =\frac{(x+3)(x-3)}{{x}^{2}(x-2)+6(x-2)} \\  & =\frac{(x+3)(x-3)}{({x}^{2}+6)(x-2)}\end{aligned}
$$

There are no common factors in the numerator and denominator, so we set the denominator equal to zero. This gives

$$
({x}^{2}+6)(x-2)=0.
$$

We now solve the above equation using the zero product property:

- Solving $x-2=0$ gives the solution $x=2.$

- The equation ${x}^{2}+6=0$ has no real solutions.

Therefore, the only vertical asymptote is $x=2.$

### q-4694

Calculate the vertical asymptotes of $f(x)=\frac{2x}{{x}^{3}-27}.$

Level: hard. Family: cube. Original parameters: `{"r": 3, "n": 2}`. Numerator: `2*x`; denominator: `x**3 - 27`; irreducible quadratic: `x**2 + 3*x + 9`; real-root set: `[3]`.

Field layout: one :answer-field.type/radio field, key `selection`.

Full worked sequence (captured verbatim, including any anomaly):

To find the vertical asymptotes of a rational function, we factor the numerator and denominator and cancel any common factors. Then, we set the denominator equal to zero and solve for $x.$

Factoring the numerator and denominator, we get

$$
\begin{aligned}f(x) & =\frac{2x}{{x}^{3}-27} \\  & =\frac{2x}{{x}^{3}-{3}^{3}} \\  & =\frac{2x}{(x-3)({x}^{2}+3x+9)}.\end{aligned}
$$

Notice that we used the difference of cubes formula to factor the denominator.

There are no common factors in the numerator and denominator, so we set the denominator equal to zero. This gives

$$
(x-3)({x}^{2}+3x+9)=0.
$$

We now solve the above equation using the zero product property:

- Solving $(x-3)=0$ gives the solution $x=3.$

- The equation ${x}^{2}+3x+9=0$ has no real solutions because the discriminant $D$ is negative:

$$
\begin{aligned}D & ={b}^{2}-4ac \\  & ={3}^{2}-4(1)(9) \\  & =9-36 \\  & =-27.\end{aligned}
$$

Therefore, the only vertical asymptote is $x=3.$

### q-270004

The vertical asymptote of $f(x)=\frac{{x}^{2}-9}{2{x}^{3}-2}$ is $x=${{field-1}}.

Level: hard. Family: cube. Original parameters: `{"r": 1, "n": 2, "s": 3}`. Numerator: `x**2 - 9`; denominator: `2*x**3 - 2`; irreducible quadratic: `x**2 + x + 1`; real-root set: `[1]`.

Field layout: one :answer-field.type/blank field, key `field-1`.

Full worked sequence (captured verbatim, including any anomaly):

To find the vertical asymptotes of a rational function, we factor the numerator and denominator and cancel any common factors. Then, we set the denominator equal to zero and solve for $x.$

Factoring the numerator and denominator, we get

$$
\begin{aligned}f(x) & =\frac{{x}^{2}-9}{2{x}^{3}-2} \\  & =\frac{{x}^{2}-9}{2({x}^{3}-1)} \\  & =\frac{{x}^{2}-{3}^{2}}{2({x}^{3}-{1}^{3})} \\  & =\frac{(x-3)(x+3)}{2(x-1)({x}^{2}+x+1)}.\end{aligned}
$$

Notice that we used the difference of cubes formula to factor the denominator.

There are no common factors in the numerator and denominator, so we set the denominator equal to zero. This gives

$$
(x-1)({x}^{2}+x+1)=0.
$$

We now solve the above equation using the zero product property:

- Solving $(x-1)=0$ gives the solution $x=1.$

- The equation ${x}^{2}+x+1=0$ has no real solutions because the discriminant $D$ is negative:

$$
\begin{aligned}D & ={b}^{2}-4ac \\  & ={1}^{2}-4(1)(1) \\  & =1-4 \\  & =-3\end{aligned}
$$

Therefore, the vertical asymptote is $x=1.$

### q-4698

Determine the vertical asymptotes of $f(x)=\frac{{x}^{2}-1}{8{x}^{4}+x}.$

Level: hard. Family: quartic_cube. Original parameters: `{"p": 2, "q": 1, "s": 1}`. Numerator: `x**2 - 1`; denominator: `8*x**4 + x`; irreducible quadratic: `4*x**2 - 2*x + 1`; real-root set: `[0, -1/2]`.

Field layout: **fieldless capture**; the original profile must omit the attribute.

Full worked sequence (captured verbatim, including any anomaly):

To find the vertical asymptotes of a rational function, we factor the numerator and denominator and cancel any common factors. Then, we set the denominator equal to zero and solve for $x:$

Factoring the numerator and denominator, we get

$$
\begin{aligned}f(x) & =\frac{{x}^{2}-1}{8{x}^{4}+x} \\  & =\frac{(x+1)(x-1)}{x(8{x}^{3}+1)} \\  & =\frac{(x+1)(x-1)}{x[(2x)^{3}+{1}^{3}]} \\  & =\frac{(x+1)(x-1)}{x(2x+1)(4{x}^{2}-2x+1)}.\end{aligned}
$$

Notice that we used the sum of cubes formula to factor the denominator.

There are no common factors in the numerator and denominator, so we set the denominator equal to zero. This gives

$$
x(2x+1)(4{x}^{2}-2x+1)=0.
$$

We now solve the above equation using the zero product property:

- Solving $x=0$ gives the solution $x=0.$

- Solving $2x+1=0$ gives the solution $x=-\frac{1}{2}.$

- The equation $4{x}^{2}-2x+1=0$ has no real solutions because the discriminant $D$ is negative:

$$
\begin{aligned}D & ={b}^{2}-4ac \\  & =(-2)^{2}-4(4)(1) \\  & =4-16 \\  & =-12\end{aligned}
$$

Therefore, the equations of the vertical asymptotes are $x=0$ and $x=-\frac{1}{2}.$

## Stage 2 — generalized pattern and response

The learner finds real zeros of a rational denominator after factoring and confirms that its remaining quadratic factor has no real roots. A negative discriminant removes the entire complex conjugate pair from the vertical-asymptote set; computing complex roots is never required. Coprime numerators guarantee every remaining real denominator root is a vertical asymptote.

Easy is an irreducible quadratic with a constant or linear numerator and no real asymptotes. Moderate extracts x by GCF or a common linear factor by grouping, leaving a negative-discriminant or strictly positive quadratic and exactly one real asymptote. Hard applies a cube identity, with the observed quartic source extracting an additional x. Numerator factoring remains at the observed linear-GCF/difference-of-squares workload. No same-level family is ordered as a progression.

Blank responses supply only the root value after the provided `x=`; radio responses contain the complete asymptote set, including the no-asymptote statement. Three fieldless sources get authored supported radio fields only outside the original profile.

## Stage 3 — full component/bank accounting

Each of the following rows is one entire source option, rather than one equation from a multi-root choice. All roots in a set must be compared together. The schema type, exact source value, correct designation and parameterized recipe are retained. Fixed constants are explicit, not unrelated random perturbations. The original author intent of the wrong recipes is underdetermined; these are observed expression-pattern generalizations with limited interpretation, not recovered misconceptions.

### q-39795 — original profile

| Field | Type | Exact source answer | Correct | Complete parameterized recipe |
|---|---|---|---|---|
| selection | :answer.type/math | `x=1,\,x=0` | False | {b,0} |
| selection | :answer.type/text | `$x=0$ only` | True | {0} |
| selection | :answer.type/text | `$x=\frac{1}{2}$ only` | False | {b/2} |
| selection | :answer.type/math | `x=-1,\,x=-\frac{1}{2}` | False | {-b,-b/2} |
| selection | :answer.type/math | `x=1,\,x=-1` | False | {b,-b} |

### q-4694 — original profile

| Field | Type | Exact source answer | Correct | Complete parameterized recipe |
|---|---|---|---|---|
| selection | :answer.type/text | `No vertical asymptotes` | False | ∅ |
| selection | :answer.type/text | `$x=3$ only` | True | {r} |
| selection | :answer.type/text | `$x=9$ only` | False | {r²} |
| selection | :answer.type/math | `x=-3,x=0,x=3` | False | {-r,0,r} |
| selection | :answer.type/text | `$x=-3$ only` | False | {-r} |

### q-80679 — original profile

| Field | Type | Exact source answer | Correct | Complete parameterized recipe |
|---|---|---|---|---|
| selection | :answer.type/math | `x=-1,\,x=5` | False | {-1,c} |
| selection | :answer.type/text | `The function has no vertical asymptotes` | True | ∅ |
| selection | :answer.type/math | `x=1,\,x=5` | False | {1,c} |
| selection | :answer.type/text | `$x=1$ only` | False | {1} |
| selection | :answer.type/text | `$x=5$ only` | False | {c} |

### q-113523

No captured bank/correct designation; supported completions have separately authored banks and do not count as observed.

### q-278551 — original profile

| Field | Type | Exact source answer | Correct | Complete parameterized recipe |
|---|---|---|---|---|
| field-1 | :answer.type/math | `1` | True | r (required fragment) |

### q-4698

No captured bank/correct designation; supported completions have separately authored banks and do not count as observed.

### q-80680

No captured bank/correct designation; supported completions have separately authored banks and do not count as observed.

### q-113525 — original profile

| Field | Type | Exact source answer | Correct | Complete parameterized recipe |
|---|---|---|---|---|
| selection | :answer.type/text | `$x=-1$ and $x=0$` | False | {-b,0} |
| selection | :answer.type/text | `$x=0$ only` | True | {0} |
| selection | :answer.type/text | `$x=-1$ only` | False | {-b} |
| selection | :answer.type/text | `$x=-7$ and $x=0$` | False | {-c,0} |
| selection | :answer.type/text | `$x=1$ only` | False | {b} |

### q-270003 — original profile

| Field | Type | Exact source answer | Correct | Complete parameterized recipe |
|---|---|---|---|---|
| field-1 | :answer.type/math | `4` | True | r (required fragment) |

### q-270004 — original profile

| Field | Type | Exact source answer | Correct | Complete parameterized recipe |
|---|---|---|---|---|
| field-1 | :answer.type/math | `1` | True | r (required fragment) |

### q-6912 — original profile

| Field | Type | Exact source answer | Correct | Complete parameterized recipe |
|---|---|---|---|---|
| selection | :answer.type/math | `x=-3,\,x=\frac{1}{3}` | False | {-a,1/a} |
| selection | :answer.type/math | `x=-3,\,x=3` | False | {-a,a} |
| selection | :answer.type/math | `x=-\frac{1}{3},\,x=3` | False | {-1/a,a} |
| selection | :answer.type/math | `x=-\frac{1}{3},\,x=\frac{1}{3}` | False | {-1/a,1/a} |
| selection | :answer.type/text | `The function has no vertical asymptotes` | True | ∅ |

### q-80676 — original profile

| Field | Type | Exact source answer | Correct | Complete parameterized recipe |
|---|---|---|---|---|
| selection | :answer.type/text | `$x=2$ only` | True | {r} |
| selection | :answer.type/math | `x=-2,\,x=0` | False | {-r,0} |
| selection | :answer.type/math | `x=-2,\,x=2` | False | {-r,r} |
| selection | :answer.type/text | `$x=-2$ only` | False | {-r} |
| selection | :answer.type/math | `x=0,\,x=2` | False | {0,r} |

### q-113527 — original profile

| Field | Type | Exact source answer | Correct | Complete parameterized recipe |
|---|---|---|---|---|
| selection | :answer.type/text | `$x=0$ and $x=2$` | False | {0,r} |
| selection | :answer.type/text | `$x=6$ only` | False | {c} |
| selection | :answer.type/text | `$x=2$ only` | True | {r} |
| selection | :answer.type/text | `$x=-6$ only` | False | {-c} |
| selection | :answer.type/text | `$x=2$ and $x=6$ only` | False | {r,c} |

The fixed prose is compiled from each source; all changed math components are identified by `components`. Fraction numerator and denominator groups are masked independently. This prevents scalar numerators from changing polynomial exponents and prevents a linear numerator from replacing a suffix inside a quadratic. Source stages are retained in exact order and row count; the formal discriminant → coefficient substitution → individually evaluated squares/product → final subtraction sequence is never collapsed by SymPy. Correct and wrong banks are computed together and the entire instance fails when any complete root sets coincide.

## Stage 4 — reusable masks, constraints and calculations

Public template names are the source IDs in SPECS; thirteen masks retain twelve structural families and seven distinct complete observed radio banks. Parameters affect entire polynomials/factors/equations, never arbitrary prose digits. At baseline, the same parameterized renderer reproduces the source strings; there is no literal-source return branch and no answer lookup.

| Family | Numerator/denominator model | Sampling and explicit-input bounds |
|---|---|---|
| easy monic quadratic | source constant/linear numerator over x²+bx+c | a=1, b∈{-7,…,-1,1,…,7}, c=1…12, b²<4c, n=1…6 |
| easy positive quadratic | nx/(ax²+1) | a=2…5, b=0,c=1,n=1…6; nonunit a preserves source form |
| moderate GCF | n/[x(x²+bx+c)] | a=1,b=1…4,c=1…9,b²<4c,n=1…6 |
| moderate grouping | source numerator/[(ax²+c)(x-r)] | r=1…5,c=1…9; a=1 except nonunit-blank a=2…3,c=1; n=1…6 (n≥2 for factored linear numerator),s=1…5 when present |
| hard difference of cubes | nx/(x³-r³) or (x²-s²)/[n(x³-r³)] | r=2…5 for radio; r=1…5 for scaled blank; n=1…5 or 2…5 for scaled blank, s=1…5, r≠s |
| hard quartic sum of cubes | (x²-s²)/[x((px)³+q³)] | p=2…3,q=1…2,gcd(p,q)=1,s=1…4; nonunit p and primitive pair preserve rational-root workload |

All bounds are design policies rather than observed source generator rules. Every explicit call passes the same guard as sampled calls. The denominator has exactly one complex quadratic; negative discriminant and coprime numerator/denominator are mandatory. Moderate nonunit-leading source cannot reduce to a monic source, and hard quartic primitive factors cannot conceal a GCF that converts the rational root to an integer. Grouping needs nonzero r,c. All-real denominators, holes and cancellation fail. Hard coefficients stay at familiar small cube/discriminant arithmetic; p=4,q=3 is deliberately excluded.

Authored radio defaults are entire operation banks, with each option's explicit `zeros_of` polynomial retained as `generation.bank_operations`. Every option set is independently checked against that printed polynomial by the validator:

| Family | Correct operation | Four complete wrong operations |
|---|---|---|
| monic easy quadratic | real zeros of ax²+bx+c (none) | four false factorizations (ax±b)(x±c), taking the displayed coefficients directly as factor constants; all four sign pairs are used |
| positive easy quadratic | real zeros of ax²+1 (none) | four false factorizations (x±a)(ax±1), all four sign pairs; this wrongly moves a between the two factors and treats the sum as a difference |
| moderate GCF | real zeros of x(x²+bx+c) | omit x → Q; replace Q by (x+b)(x+c) and omit x; make the same false replacement and retain x; replace Q by (x−b)(x−c) and retain x |
| moderate grouping | real zeros of (x−r)(ax²+c) | omit x−r → Q; reverse real factor sign → (x+r)Q; replace squared power by linear power → (x−r)(ax+c); also reverse the constant sign → (x−r)(ax−c) |
| hard difference of cubes | real zeros of D | omit the cube's real linear factor → Q; reverse its sign → (x+r)Q; incorrectly include all numerator zeros → ND; incorrectly use numerator zeros alone → N |
| hard quartic sum of cubes | real zeros of x(px+q)Q | omit outer x → (px+q)Q; omit px+q → xQ; omit both real factors → Q; reverse the real cube factor's sign → x(px−q)Q |

These are explicit incorrect factor/zero-selection operations, rather than perturbations of a scalar answer. Negative discriminants remove all real roots from Q; no complex-root arithmetic is introduced by the authored choices. Whole-bank collisions (for example c=r in a monic grouping instance) reject the entire instance; no replacement options are selected. All displayed wrong answers differ from the complete true asymptote set. Error labels stay in author metadata; the learner sees only the original fixed solution prose. Observed banks remain separate opt-in profiles with underdetermined error intent; blanks have no distractors.

`original` is always `evidence_only=true`, `eligible_for_learning=false`. `supported-observed` captured radio banks remain opaque evidence-only banks; its supported fieldless operation-bank completions and observed blanks are eligible. Default `authored` output is eligible. These flags make raw-source fidelity distinct from supported learner material.

Content UUIDs derive from generator version, actual rendered prompt, fixed solution, complete bank and shape. Seeds/order/profile aliases do not create new identity. The mathematical fingerprint includes the monic denominator polynomial. It also includes the monic numerator when its nontrivial factorization contributes to the observed workload: moderate q-113523 (numeric GCF and linear factor), moderate q-113527 (difference of squares), hard q-270004 and q-4698 (difference of squares). Easy linear shifts, unfactored moderate linear numerators, and all scalar prefactors are incidental and excluded. Source aliases, bank profiles and option order never add mathematical tasks. q-113523 requires n≥2 so its numeric GCF stage cannot disappear.

## Source anomalies and repairs

q-39795 contains the extraneous “Solving 2x=0” while its actual factor is x. Original replay preserves it exactly; normal output repairs it to x=0. Raw exact solution fidelity is 13/13; supported normal exact solutions are 12/13 plus one supported teaching correction. The three fieldless sources preserve missing attributes under original, receive independently derived supported fields under normal profiles, and have no matched original correct refs. No observed answer value or root set is incorrect. No TeX escape repair was needed.

## Verification and finite variety

The independent validator parses the actual printed function, every complete displayed root set and all printed rational-function/discriminant/equation stages. It compares raw prompts, entire source worked solutions, attribute presence, every exact option/type and complete correct designation separately. Native grader checks owned radio UUID selections plus canonical, unreduced equivalent, and wrong blank expressions. Validation reports every count; grade success alone is not mathematical validation.

`task-catalog.json` enumerates every distinct meaningful task reachable under the guards and complete authored-bank constraints. Numerator factorization variation is retained exactly where it contributes to the observed workload, without using scalar prefactors or bank aliases to inflate counts. `validation.json` reports both exhaustive eligible counts and sampled counts: **98 easy, 444 moderate, 36 hard** eligible tasks. Blank layouts can admit a mathematical task whose authored radio bank has a collision, so the global moderate count includes those independently valid blank tasks. Domains are finite, not an unlimited-variety claim. Each enumerated task is independently checked from the actual printed question and all worked stages.
