# Template extraction

## 1. Specific source descriptions

Every original prompt, complete answer bank and complete worked solution remains in source.json. The following inventory describes each instance before generalizing.

### q-1088

What is $\begin{vmatrix}\sqrt{2} & 5 \\ 1 & 3\end{vmatrix}$?

Difficulty: easy (authored assignment; source unrated); response: :answer-field.type/radio; field key: selection; options: 5.

Parameters: `{"n": 2, "b": 5, "c": 1, "d": 3}`.

Source solution:

Absent. Authored standard formal ad−bc, matrix, substituted products, individually evaluated products and final subtraction are supplied.

### q-1089

Calculate $det(Z)$, if
 $Z=[\begin{aligned}\sqrt{x} & y \\ {y}^{2} & \sqrt{x}\end{aligned}].$

Difficulty: easy (observed); response: :answer-field.type/radio; field key: selection; options: 5.

Parameters: `{"k": 2}`.

Source solution:

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(Z) & =|\begin{aligned}\sqrt{x} & y \\ {y}^{2} & \sqrt{x}\end{aligned}| \\  & =\sqrt{x}\cdot \sqrt{x}-y\cdot {y}^{2} \\  & =x-{y}^{3}\end{aligned}
$$

### q-1083

$|\begin{aligned}2x & {y}^{2} \\ z & -3\end{aligned}|=$

Difficulty: easy (observed); response: :answer-field.type/radio; field key: selection; options: 5.

Parameters: `{"a": 2, "d": 3, "k": 2}`.

Source solution:

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}|\begin{aligned}2x & {y}^{2} \\ z & -3\end{aligned}| & =2x\cdot (-3)-{y}^{2}\cdot z \\  & =-6x-{y}^{2}z\end{aligned}
$$

### q-1087

Calculate $det(T)$, if
    $T=[\begin{aligned}\frac{1}{2} & 17 \\ 1 & 10\end{aligned}].$

Difficulty: easy (observed); response: :answer-field.type/radio; field key: selection; options: 5.

Parameters: `{"q": 2, "b": 17, "c": 1, "d": 10}`.

Source solution:

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(T) & =|\begin{aligned}\frac{1}{2} & 17 \\ 1 & 10\end{aligned}| \\  & =\frac{1}{2}\cdot 10-17\cdot 1 \\  & =5-17 \\  & =-12\end{aligned}
$$

### q-127601

Calculate $det(C)$, if
    $C=[\begin{aligned}-x & -2y \\ \frac{x}{2} & 5y\end{aligned}].$

Difficulty: moderate (observed); response: :answer-field.type/radio; field key: selection; options: 5.

Parameters: `{"a": 1, "b": 2, "q": 2, "d": 5}`.

Source solution:

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(C) & =|\begin{aligned}-x & -2y \\ \frac{x}{2} & 5y\end{aligned}| \\  & =-x\cdot 5y-(-2y)\cdot \frac{x}{2} \\  & =-5xy+xy \\  & =-4xy\end{aligned}
$$

### q-127603

Calculate $det(D)$, if
    $D=[\begin{aligned}2x & y \\ -5 & xy\end{aligned}].$

Difficulty: moderate (observed); response: :answer-field.type/radio; field key: selection; options: 5.

Parameters: `{"a": 2, "b": 5}`.

Source solution:

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}2x & y \\ -5 & xy\end{aligned}| \\  & =2x\cdot xy-y\cdot (-5) \\  & =2{x}^{2}y+5y \\  & =y(2{x}^{2}+5)\end{aligned}
$$

### q-275595

Evaluate the determinant:

$|\begin{aligned}\sqrt{3} & y \\ 2 & \sqrt{3}\end{aligned}|=$
 {{field-1}}

Difficulty: easy (observed); response: :answer-field.type/blank; field key: field-1; options: 1.

Parameters: `{"n": 3, "c": 2}`.

Source solution:

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}|\begin{aligned}\sqrt{3} & y \\ 2 & \sqrt{3}\end{aligned}| & =\sqrt{3}\cdot \sqrt{3}-y\cdot 2 \\  & =3-2y.\end{aligned}
$$

### q-317367

Calculate $det(D)$ given that
$D=[\begin{aligned}\frac{2}{5} & -3 \\ -\frac{1}{2} & 2\end{aligned}].$

$det(D)=$
{{field-1}}

Difficulty: moderate (observed); response: :answer-field.type/blank; field key: field-1; options: 1.

Parameters: `{"p": 2, "q": 5, "b": -3, "h": -1, "j": 2, "d": 2}`.

Source solution:

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}\frac{2}{5} & -3 \\ -\frac{1}{2} & 2\end{aligned}| \\  & =\frac{2}{5}\cdot 2-(-3)\cdot (-\frac{1}{2}) \\  & =\frac{4}{5}-\frac{3}{2} \\  & =-\frac{7}{10}.\end{aligned}
$$

### q-317368

Calculate $det(E)$ given that
$E=[\begin{aligned}-\frac{3}{4} & 5 \\ 2 & -1\end{aligned}].$

$det(E)=$
{{field-1}}

Difficulty: moderate (observed); response: :answer-field.type/blank; field key: field-1; options: 1.

Parameters: `{"p": -3, "q": 4, "b": 5, "c": 2, "d": -1}`.

Source solution:

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(E) & =|\begin{aligned}-\frac{3}{4} & 5 \\ 2 & -1\end{aligned}| \\  & =-\frac{3}{4}\cdot (-1)-5\cdot 2 \\  & =\frac{3}{4}-10 \\  & =-\frac{37}{4}.\end{aligned}
$$

### q-317372

Calculate $det(D)$ given that
$D=[\begin{aligned}3x & 2y \\ -5 & x\end{aligned}].$

$det(D)=$
{{field-1}}

Difficulty: moderate (observed); response: :answer-field.type/blank; field key: field-1; options: 1.

Parameters: `{"a": 3, "b": 2, "c": 5}`.

Source solution:

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}3x & 2y \\ -5 & x\end{aligned}| \\  & =3x\cdot x-2y\cdot (-5) \\  & =3{x}^{2}+10y.\end{aligned}
$$

### q-317374

Evaluate the determinant:

$|\begin{aligned}\sqrt{6} & y \\ 4 & \sqrt{6}\end{aligned}|=$
{{field-1}}

Difficulty: easy (observed); response: :answer-field.type/blank; field key: field-1; options: 1.

Parameters: `{"n": 6, "c": 4}`.

Source solution:

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}|\begin{aligned}\sqrt{6} & y \\ 4 & \sqrt{6}\end{aligned}| & =\sqrt{6}\cdot \sqrt{6}-y\cdot 4 \\  & =6-4y.\end{aligned}
$$

### q-69649

$|\begin{aligned}3\sqrt{x} & {z}^{2} \\ 2y & -\sqrt{x}\end{aligned}|=$

Difficulty: easy (observed); response: :answer-field.type/radio; field key: selection; options: 5.

Parameters: `{"a": 3, "b": 2, "k": 2}`.

Source solution:

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}|\begin{aligned}3\sqrt{x} & {z}^{2} \\ 2y & -\sqrt{x}\end{aligned}| & =3\sqrt{x}\cdot (-\sqrt{x})-{z}^{2}\cdot 2y \\  & =-3x-2y{z}^{2}\end{aligned}
$$

### q-69650

Calculate $det(H)$, if
    $H=[\begin{aligned}-2r & 3s \\ -2t & 3u\end{aligned}].$

Difficulty: moderate (observed); response: :answer-field.type/radio; field key: selection; options: 5.

Parameters: `{"a": -2, "b": 3}`.

Source solution:

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(H) & =|\begin{aligned}-2r & 3s \\ -2t & 3u\end{aligned}| \\  & =-2r\cdot 3u-3s\cdot (-2t) \\  & =-6ru-(-6st) \\  & =-6ru+6st \\  & =6(st-ru)\end{aligned}
$$

## 2. Shared mathematical pattern

Read four entries in row order, multiply the top-left and bottom-right, subtract the top-right times bottom-left, then simplify the resulting scalar or elementary polynomial. The matrix is given; there is never an unknown equation to solve. Each layout expects the complete scalar expression, without an equals sign or determinant wrapper. Radios have exactly five choices and blanks one owned reference answer.

## 3. Components and complete observed banks

Every original option maps one-to-one to an explicit parameterized recipe below. Recipes marked opaque retain an algebraic replay pattern only; matching a scalar does not identify learner intent. Complete profiles are selected together, never assembled by picking convenient options.

Recipe definitions (a,b,c,d denote the parameters named in source-cases.json; AD/BC denote actual matrix products):

- numeric_radical: c; √(n d)+BC; AD−BC; −n; √(n d)−BC. The radical-index multiplication options are interpretable; the c and −n scalar choices are opaque.
- symbolic_radical: x−2y^k; 2√x−y^(k+1); x−y^(k+1); √x−2y^(k+1); x−y^k.
- linear_power: d+a; d−a; −AD−BC/z; −AD−BC; AD−BC. First two scalar constants are opaque replay patterns.
- easy_fraction: (3/5)AD; (7/5)AD; −BC; AD−BC; AD+BC. First two multipliers are opaque observed coefficients; no fitted error intent is claimed.
- shared_monomial: −AD; (3/2)BC; AD−BC; −AD/2; AD. Fractional coefficient errors remain observed patterns.
- factored_polynomial: (a+1)y²x−b; y(ax²+b); (a+1)x²y+(a+1); a²x²y²; y(ax²−(a+1)). Altered a+1 patterns and reversed powers are observed algebraic transformations, not recovered psychology.
- radical_power: −ax−byz^k; ax−bz^k y; −bx−ayz^k; −ax−by^k z; bx+ayz^k.
- factored_bilinear: n(ru−st); n ru−(n/2)st; n(st−ru); −n ru+(n/2)st; b((−a)st−ru), n=−ab. These whole expressions replay independently.

### Bank mapping q-1088

| Original complete value | Generated parameterized value at original inputs | Designation |

|---|---|---|

| $1$ | $1$ | wrong |

| $\sqrt{6} + 5$ | $\sqrt{6}+5$ | wrong |

| $3\sqrt{2} - 5$ | $3\sqrt{2}-5$ | inferred correct (source key absent) |

| $-2$ | $-2$ | wrong |

| $\sqrt{6} - 5$ | $-5+\sqrt{6}$ | wrong |

### Bank mapping q-1089

| Original complete value | Generated parameterized value at original inputs | Designation |

|---|---|---|

| $x-2{y}^{2}$ | $x-2{y}^{2}$ | wrong |

| $2\sqrt{x}-{y}^{3}$ | $2\sqrt{x}-{y}^{3}$ | wrong |

| $x-{y}^{3}$ | $x-{y}^{3}$ | observed correct |

| $\sqrt{x}-2{y}^{3}$ | $\sqrt{x}-2{y}^{3}$ | wrong |

| $x-{y}^{2}$ | $x-{y}^{2}$ | wrong |

### Bank mapping q-1083

| Original complete value | Generated parameterized value at original inputs | Designation |

|---|---|---|

| $5$ | $5$ | wrong |

| $1$ | $1$ | wrong |

| $6x-{y}^{2}$ | $6x-{y}^{2}$ | wrong |

| $6x-{y}^{2}z$ | $6x-{y}^{2}z$ | wrong |

| $-6x-{y}^{2}z$ | $-6x-{y}^{2}z$ | observed correct |

### Bank mapping q-1087

| Original complete value | Generated parameterized value at original inputs | Designation |

|---|---|---|

| $3$ | $3$ | wrong |

| $7$ | $7$ | wrong |

| $-17$ | $-17$ | wrong |

| $-12$ | $-12$ | observed correct |

| $22$ | $22$ | wrong |

### Bank mapping q-127601

| Original complete value | Generated parameterized value at original inputs | Designation |

|---|---|---|

| $5xy$ | $5xy$ | wrong |

| $-\frac{3xy}{2}$ | $-\frac{3xy}{2}$ | wrong |

| $-4xy$ | $-4xy$ | observed correct |

| $\frac{5xy}{2}$ | $\frac{5xy}{2}$ | wrong |

| $-5xy$ | $-5xy$ | wrong |

### Bank mapping q-127603

| Original complete value | Generated parameterized value at original inputs | Designation |

|---|---|---|

| $3{y}^{2}x-5$ | $3{y}^{2}x-5$ | wrong |

| $y(2{x}^{2}+5)$ | $y(2{x}^{2}+5)$ | observed correct |

| $3{x}^{2}y+3$ | $3{x}^{2}y+3$ | wrong |

| $4{x}^{2}{y}^{2}$ | $4{x}^{2}{y}^{2}$ | wrong |

| $y(2{x}^{2}-3)$ | $y(2{x}^{2}-3)$ | wrong |

### Bank mapping q-275595

| Original complete value | Generated parameterized value at original inputs | Designation |

|---|---|---|

| $3-2y$ | $3-2y$ | observed correct |

### Bank mapping q-317367

| Original complete value | Generated parameterized value at original inputs | Designation |

|---|---|---|

| $-\frac{7}{10}$ | $-\frac{7}{10}$ | observed correct |

### Bank mapping q-317368

| Original complete value | Generated parameterized value at original inputs | Designation |

|---|---|---|

| $-\frac{37}{4}$ | $-\frac{37}{4}$ | observed correct |

### Bank mapping q-317372

| Original complete value | Generated parameterized value at original inputs | Designation |

|---|---|---|

| $3{x}^{2}+10y$ | $3{x}^{2}+10y$ | observed correct |

### Bank mapping q-317374

| Original complete value | Generated parameterized value at original inputs | Designation |

|---|---|---|

| $6-4y$ | $6-4y$ | observed correct |

### Bank mapping q-69649

| Original complete value | Generated parameterized value at original inputs | Designation |

|---|---|---|

| $-3x-2y{z}^{2}$ | $-3x-2y{z}^{2}$ | observed correct |

| $3x-2{z}^{2}y$ | $3x-2{z}^{2}y$ | wrong |

| $-2x-3y{z}^{2}$ | $-2x-3y{z}^{2}$ | wrong |

| $-3x-2{y}^{2}z$ | $-3x-2{y}^{2}z$ | wrong |

| $2x+3y{z}^{2}$ | $2x+3y{z}^{2}$ | wrong |

### Bank mapping q-69650

| Original complete value | Generated parameterized value at original inputs | Designation |

|---|---|---|

| $6(ru-st)$ | $6(ru-st)$ | wrong |

| $6ru-3st$ | $6ru-3st$ | wrong |

| $6(st-ru)$ | $6(st-ru)$ | observed correct |

| $-6ru+3st$ | $-6ru+3st$ | wrong |

| $3(2st-ru)$ | $3(2st-ru)$ | wrong |

## 4. Reusable Markdown/value templates

Fixed prose and generic determinant formula are shared. Complete entry components, matrix name/layout, substituted ordered products, evaluated products, collected expression and any source GCF-factor row are independent slots. No global textual replacement is used. Generalized families are visible in TEMPLATES/DEFAULTS/build/render; all exact explicit-input bounds are enforced in guard. Source-cases.json names every original parameter/profile combination. Changing parameters runs normal generation; no source literal-payload branch or answer lookup table exists.

Numerical easy_fraction requires 1/q times an integer multiple of q, preserving the original integer evaluated product and integer subtraction. one_fraction requires one signed reduced noninteger rational input whose diagonal product stays fractional. two_fractions requires two signed reduced proper fractions whose two products stay fractional with different denominators. shared_monomial preserves a fractional x/q times an integer multiple of q and combines like xy terms. Radical n is positive squarefree nonsquare; symbolic √x assumes x≥0. Nonunit monomial coefficients and source factoring steps persist at moderate. Each hard input is a reduced noninteger fraction with numerator magnitude and denominator 2..9; both reduced product denominators exceed one and neither divides the other. Explicit inputs cannot bypass these workload bounds.

Normal radio default is separately authored AD−BC, AD+BC, −(AD−BC), AD, −BC: determinant subtraction reversed or changed to addition, and omitted product terms. These are operation-based rather than opaque scalar fits. They are not described as recovered original banks. All five expressions are built together, and any correct/wrong or wrong/wrong mathematical equality rejects the whole question. Independent actual printed matrices/stages are checked, including every substituted sign and every individually evaluated product/collection/factor row.

Source mathematical errors: none found. q-1088 inferred answer is 3√2−5; neither √6−5 nor √6+5 is correct, because 3 is an external factor, not a square-root radicand. Missing source designation is not a match. No solution repair was necessary: all twelve available original worked solutions replay byte-exact. Source choice notation may normalize spacing/order while full mathematical value is compared one-to-one.

No mathematical plots or diagrams occur in these practice sources. The lesson introductory diagonal-arrow image explains the method but is not a question asset. Plot extraction/spec and rendering are therefore not applicable.
