# Complete source practice questions

EDB math basis 1522; KP 17592186059749. Original prompts, every choice, and one original worked solution are retained. Missing source attributes remain explicitly missing.

## q-1088 — unrated

**Specific components:** {"entries": ["\\sqrt{2}", "5", "1", "3"], "ad": "3*sqrt(2)", "bc": "5", "symbol_aliases": {}, "domains": "Real variables; x >= 0 in templates containing sqrt(x).", "expected_answer": "-5 + 3 \\sqrt{2}"}

**Template:** `unrated-radical-radio`

What is $\begin{vmatrix}\sqrt{2} & 5 \\ 1 & 3\end{vmatrix}$?

| Field | Type | Bank profile | Source answer entity | Original value | Source correct | Value recipe |
|---|---|---|---:|---|---|---|
| selection | radio | bank-q-1088 | 17592186056245 | $1$ | unrecorded | `p / q`; {"p": "1", "q": "1"} |
| selection | radio | bank-q-1088 | 17592186056246 | $\sqrt{6} + 5$ | unrecorded | `sqrt(6) + 5`; {} |
| selection | radio | bank-q-1088 | 17592186056247 | $3\sqrt{2} - 5$ | unrecorded | `-5 + 3*sqrt(2)`; {} |
| selection | radio | bank-q-1088 | 17592186056248 | $-2$ | unrecorded | `p / q`; {"p": "-2", "q": "1"} |
| selection | radio | bank-q-1088 | 17592186056249 | $\sqrt{6} - 5$ | unrecorded | `-5 + sqrt(6)`; {} |

**Original worked solution:**

**Missing in database. No source solution was invented.**

## q-1089 — easy

**Specific components:** {"entries": ["\\sqrt{x}", "y", "{y}^{2}", "\\sqrt{x}"], "ad": "x", "bc": "y**3", "symbol_aliases": {}, "domains": "Real variables; x >= 0 in templates containing sqrt(x).", "expected_answer": "x - y^{3}"}

**Template:** `E1-named-symbolic-root-radio`

Calculate $det(Z)$, if
 $Z=[\begin{aligned}\sqrt{x} & y \\ {y}^{2} & \sqrt{x}\end{aligned}].$

| Field | Type | Bank profile | Source answer entity | Original value | Source correct | Value recipe |
|---|---|---|---:|---|---|---|
| selection | radio | bank-q-1089 | 17592186241696 | $x-2{y}^{2}$ | False | `x - 2*y**2`; {"x": "source symbol x", "y": "source symbol y"} |
| selection | radio | bank-q-1089 | 17592186241737 | $2\sqrt{x}-{y}^{3}$ | False | `2*sqrt(x) - y**3`; {"x": "source symbol x", "y": "source symbol y"} |
| selection | radio | bank-q-1089 | 17592186241756 | $x-{y}^{3}$ | True | `ad - bc`; {"a": "sqrt(x)", "b": "y", "c": "y**2", "d": "sqrt(x)"} |
| selection | radio | bank-q-1089 | 17592186242493 | $\sqrt{x}-2{y}^{3}$ | False | `sqrt(x) - 2*y**3`; {"x": "source symbol x", "y": "source symbol y"} |
| selection | radio | bank-q-1089 | 17592186243110 | $x-{y}^{2}$ | False | `x - y**2`; {"x": "source symbol x", "y": "source symbol y"} |

**Original worked solution:**

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(Z) & =|\begin{aligned}\sqrt{x} & y \\ {y}^{2} & \sqrt{x}\end{aligned}| \\  & =\sqrt{x}\cdot \sqrt{x}-y\cdot {y}^{2} \\  & =x-{y}^{3}\end{aligned}
$$

## q-1083 — easy

**Specific components:** {"entries": ["2x", "{y}^{2}", "z", "-3"], "ad": "-6*x", "bc": "y**2*z", "symbol_aliases": {}, "domains": "Real variables; x >= 0 in templates containing sqrt(x).", "expected_answer": "- 6 x - y^{2} z"}

**Template:** `E2-bare-symbolic-radio`

$|\begin{aligned}2x & {y}^{2} \\ z & -3\end{aligned}|=$

| Field | Type | Bank profile | Source answer entity | Original value | Source correct | Value recipe |
|---|---|---|---:|---|---|---|
| selection | radio | bank-q-1083 | 17592186241263 | $5$ | False | `p / q`; {"p": "5", "q": "1"} |
| selection | radio | bank-q-1083 | 17592186241757 | $1$ | False | `p / q`; {"p": "1", "q": "1"} |
| selection | radio | bank-q-1083 | 17592186241929 | $6x-{y}^{2}$ | False | `6*x - y**2`; {"x": "source symbol x", "y": "source symbol y"} |
| selection | radio | bank-q-1083 | 17592186242069 | $6x-{y}^{2}z$ | False | `6*x - y**2*z`; {"x": "source symbol x", "y": "source symbol y", "z": "source symbol z"} |
| selection | radio | bank-q-1083 | 17592186242077 | $-6x-{y}^{2}z$ | True | `ad - bc`; {"a": "2*x", "b": "y**2", "c": "z", "d": "-3"} |

**Original worked solution:**

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}|\begin{aligned}2x & {y}^{2} \\ z & -3\end{aligned}| & =2x\cdot (-3)-{y}^{2}\cdot z \\  & =-6x-{y}^{2}z\end{aligned}
$$

## q-1087 — easy

**Specific components:** {"entries": ["\\frac{1}{2}", "17", "1", "10"], "ad": "5", "bc": "17", "symbol_aliases": {}, "domains": "Real variables; x >= 0 in templates containing sqrt(x).", "expected_answer": "-12"}

**Template:** `E3-numeric-rational-radio`

Calculate $det(T)$, if
    $T=[\begin{aligned}\frac{1}{2} & 17 \\ 1 & 10\end{aligned}].$

| Field | Type | Bank profile | Source answer entity | Original value | Source correct | Value recipe |
|---|---|---|---:|---|---|---|
| selection | radio | bank-q-1087 | 17592186241212 | $3$ | False | `p / q`; {"p": "3", "q": "1"} |
| selection | radio | bank-q-1087 | 17592186241604 | $7$ | False | `p / q`; {"p": "7", "q": "1"} |
| selection | radio | bank-q-1087 | 17592186242243 | $-17$ | False | `p / q`; {"p": "-17", "q": "1"} |
| selection | radio | bank-q-1087 | 17592186242600 | $-12$ | True | `ad - bc`; {"a": "1/2", "b": "17", "c": "1", "d": "10"} |
| selection | radio | bank-q-1087 | 17592186242897 | $22$ | False | `p / q`; {"p": "22", "q": "1"} |

**Original worked solution:**

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(T) & =|\begin{aligned}\frac{1}{2} & 17 \\ 1 & 10\end{aligned}| \\  & =\frac{1}{2}\cdot 10-17\cdot 1 \\  & =5-17 \\  & =-12\end{aligned}
$$

## q-127601 — moderate

**Specific components:** {"entries": ["-x", "-2y", "\\frac{x}{2}", "5y"], "ad": "-5*x*y", "bc": "-x*y", "symbol_aliases": {}, "domains": "Real variables; x >= 0 in templates containing sqrt(x).", "expected_answer": "- 4 x y"}

**Template:** `M1-fraction-cancellation-radio`

Calculate $det(C)$, if
    $C=[\begin{aligned}-x & -2y \\ \frac{x}{2} & 5y\end{aligned}].$

| Field | Type | Bank profile | Source answer entity | Original value | Source correct | Value recipe |
|---|---|---|---:|---|---|---|
| selection | radio | bank-q-127601 | 17592186260077 | $5xy$ | False | `5*x*y`; {"x": "source symbol x", "y": "source symbol y"} |
| selection | radio | bank-q-127601 | 17592186261052 | $-\frac{3xy}{2}$ | False | `-3*x*y/2`; {"x": "source symbol x", "y": "source symbol y"} |
| selection | radio | bank-q-127601 | 17592186261081 | $-4xy$ | True | `ad - bc`; {"a": "-x", "b": "-2*y", "c": "x/2", "d": "5*y"} |
| selection | radio | bank-q-127601 | 17592186261316 | $\frac{5xy}{2}$ | False | `5*x*y/2`; {"x": "source symbol x", "y": "source symbol y"} |
| selection | radio | bank-q-127601 | 17592186261379 | $-5xy$ | False | `-5*x*y`; {"x": "source symbol x", "y": "source symbol y"} |

**Original worked solution:**

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(C) & =|\begin{aligned}-x & -2y \\ \frac{x}{2} & 5y\end{aligned}| \\  & =-x\cdot 5y-(-2y)\cdot \frac{x}{2} \\  & =-5xy+xy \\  & =-4xy\end{aligned}
$$

## q-127603 — moderate

**Specific components:** {"entries": ["2x", "y", "-5", "xy"], "ad": "2*x**2*y", "bc": "-5*y", "symbol_aliases": {}, "domains": "Real variables; x >= 0 in templates containing sqrt(x).", "expected_answer": "2 x^{2} y + 5 y"}

**Template:** `M2-polynomial-factor-radio`

Calculate $det(D)$, if
    $D=[\begin{aligned}2x & y \\ -5 & xy\end{aligned}].$

| Field | Type | Bank profile | Source answer entity | Original value | Source correct | Value recipe |
|---|---|---|---:|---|---|---|
| selection | radio | bank-q-127603 | 17592186260592 | $3{y}^{2}x-5$ | False | `3*x*y**2 - 5`; {"x": "source symbol x", "y": "source symbol y"} |
| selection | radio | bank-q-127603 | 17592186260716 | $y(2{x}^{2}+5)$ | True | `ad - bc`; {"a": "2*x", "b": "y", "c": "-5", "d": "x*y"} |
| selection | radio | bank-q-127603 | 17592186261219 | $3{x}^{2}y+3$ | False | `3*x**2*y + 3`; {"x": "source symbol x", "y": "source symbol y"} |
| selection | radio | bank-q-127603 | 17592186261256 | $4{x}^{2}{y}^{2}$ | False | `4*x**2*y**2`; {"x": "source symbol x", "y": "source symbol y"} |
| selection | radio | bank-q-127603 | 17592186261294 | $y(2{x}^{2}-3)$ | False | `y*(2*x**2 - 3)`; {"x": "source symbol x", "y": "source symbol y"} |

**Original worked solution:**

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}2x & y \\ -5 & xy\end{aligned}| \\  & =2x\cdot xy-y\cdot (-5) \\  & =2{x}^{2}y+5y \\  & =y(2{x}^{2}+5)\end{aligned}
$$

## q-275595 — easy

**Specific components:** {"entries": ["\\sqrt{3}", "y", "2", "\\sqrt{3}"], "ad": "3", "bc": "2*y", "symbol_aliases": {}, "domains": "Real variables; x >= 0 in templates containing sqrt(x).", "expected_answer": "3 - 2 y"}

**Template:** `E4-root-blank`

Evaluate the determinant:

$|\begin{aligned}\sqrt{3} & y \\ 2 & \sqrt{3}\end{aligned}|=$
 {{field-1}}

| Field | Type | Bank profile | Source answer entity | Original value | Source correct | Value recipe |
|---|---|---|---:|---|---|---|
| field-1 | blank | none | 17592186291231 | $3-2y$ | True | `ad - bc`; {"a": "sqrt(3)", "b": "y", "c": "2", "d": "sqrt(3)"} |

**Original worked solution:**

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}|\begin{aligned}\sqrt{3} & y \\ 2 & \sqrt{3}\end{aligned}| & =\sqrt{3}\cdot \sqrt{3}-y\cdot 2 \\  & =3-2y.\end{aligned}
$$

## q-317367 — moderate

**Specific components:** {"entries": ["\\frac{2}{5}", "-3", "-\\frac{1}{2}", "2"], "ad": "4/5", "bc": "3/2", "symbol_aliases": {}, "domains": "Real variables; x >= 0 in templates containing sqrt(x).", "expected_answer": "- \\frac{7}{10}"}

**Template:** `M4-numeric-rational-blank`

Calculate $det(D)$ given that
$D=[\begin{aligned}\frac{2}{5} & -3 \\ -\frac{1}{2} & 2\end{aligned}].$

$det(D)=$
{{field-1}}

| Field | Type | Bank profile | Source answer entity | Original value | Source correct | Value recipe |
|---|---|---|---:|---|---|---|
| field-1 | blank | none | 17592186297616 | $-\frac{7}{10}$ | True | `ad - bc`; {"a": "2/5", "b": "-3", "c": "-1/2", "d": "2"} |

**Original worked solution:**

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}\frac{2}{5} & -3 \\ -\frac{1}{2} & 2\end{aligned}| \\  & =\frac{2}{5}\cdot 2-(-3)\cdot (-\frac{1}{2}) \\  & =\frac{4}{5}-\frac{3}{2} \\  & =-\frac{7}{10}.\end{aligned}
$$

## q-317368 — moderate

**Specific components:** {"entries": ["-\\frac{3}{4}", "5", "2", "-1"], "ad": "3/4", "bc": "10", "symbol_aliases": {}, "domains": "Real variables; x >= 0 in templates containing sqrt(x).", "expected_answer": "- \\frac{37}{4}"}

**Template:** `M4-numeric-rational-blank`

Calculate $det(E)$ given that
$E=[\begin{aligned}-\frac{3}{4} & 5 \\ 2 & -1\end{aligned}].$

$det(E)=$
{{field-1}}

| Field | Type | Bank profile | Source answer entity | Original value | Source correct | Value recipe |
|---|---|---|---:|---|---|---|
| field-1 | blank | none | 17592186297774 | $-\frac{37}{4}$ | True | `ad - bc`; {"a": "-3/4", "b": "5", "c": "2", "d": "-1"} |

**Original worked solution:**

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(E) & =|\begin{aligned}-\frac{3}{4} & 5 \\ 2 & -1\end{aligned}| \\  & =-\frac{3}{4}\cdot (-1)-5\cdot 2 \\  & =\frac{3}{4}-10 \\  & =-\frac{37}{4}.\end{aligned}
$$

## q-317372 — moderate

**Specific components:** {"entries": ["3x", "2y", "-5", "x"], "ad": "3*x**2", "bc": "-10*y", "symbol_aliases": {}, "domains": "Real variables; x >= 0 in templates containing sqrt(x).", "expected_answer": "3 x^{2} + 10 y"}

**Template:** `M5-symbolic-polynomial-blank`

Calculate $det(D)$ given that
$D=[\begin{aligned}3x & 2y \\ -5 & x\end{aligned}].$

$det(D)=$
{{field-1}}

| Field | Type | Bank profile | Source answer entity | Original value | Source correct | Value recipe |
|---|---|---|---:|---|---|---|
| field-1 | blank | none | 17592186297811 | $3{x}^{2}+10y$ | True | `ad - bc`; {"a": "3*x", "b": "2*y", "c": "-5", "d": "x"} |

**Original worked solution:**

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}3x & 2y \\ -5 & x\end{aligned}| \\  & =3x\cdot x-2y\cdot (-5) \\  & =3{x}^{2}+10y.\end{aligned}
$$

## q-317374 — easy

**Specific components:** {"entries": ["\\sqrt{6}", "y", "4", "\\sqrt{6}"], "ad": "6", "bc": "4*y", "symbol_aliases": {}, "domains": "Real variables; x >= 0 in templates containing sqrt(x).", "expected_answer": "6 - 4 y"}

**Template:** `E4-root-blank`

Evaluate the determinant:

$|\begin{aligned}\sqrt{6} & y \\ 4 & \sqrt{6}\end{aligned}|=$
{{field-1}}

| Field | Type | Bank profile | Source answer entity | Original value | Source correct | Value recipe |
|---|---|---|---:|---|---|---|
| field-1 | blank | none | 17592186297787 | $6-4y$ | True | `ad - bc`; {"a": "sqrt(6)", "b": "y", "c": "4", "d": "sqrt(6)"} |

**Original worked solution:**

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}|\begin{aligned}\sqrt{6} & y \\ 4 & \sqrt{6}\end{aligned}| & =\sqrt{6}\cdot \sqrt{6}-y\cdot 4 \\  & =6-4y.\end{aligned}
$$

## q-69649 — easy

**Specific components:** {"entries": ["3\\sqrt{x}", "{z}^{2}", "2y", "-\\sqrt{x}"], "ad": "-3*x", "bc": "2*y*z**2", "symbol_aliases": {}, "domains": "Real variables; x >= 0 in templates containing sqrt(x).", "expected_answer": "- 3 x - 2 y z^{2}"}

**Template:** `E5-bare-root-monomial-radio`

$|\begin{aligned}3\sqrt{x} & {z}^{2} \\ 2y & -\sqrt{x}\end{aligned}|=$

| Field | Type | Bank profile | Source answer entity | Original value | Source correct | Value recipe |
|---|---|---|---:|---|---|---|
| selection | radio | bank-q-69649 | 17592186333131 | $-3x-2y{z}^{2}$ | True | `ad - bc`; {"a": "3*sqrt(x)", "b": "z**2", "c": "2*y", "d": "-sqrt(x)"} |
| selection | radio | bank-q-69649 | 17592186333241 | $3x-2{z}^{2}y$ | False | `3*x - 2*y*z**2`; {"x": "source symbol x", "y": "source symbol y", "z": "source symbol z"} |
| selection | radio | bank-q-69649 | 17592186333886 | $-2x-3y{z}^{2}$ | False | `-2*x - 3*y*z**2`; {"x": "source symbol x", "y": "source symbol y", "z": "source symbol z"} |
| selection | radio | bank-q-69649 | 17592186334865 | $-3x-2{y}^{2}z$ | False | `-3*x - 2*y**2*z`; {"x": "source symbol x", "y": "source symbol y", "z": "source symbol z"} |
| selection | radio | bank-q-69649 | 17592186334901 | $2x+3y{z}^{2}$ | False | `2*x + 3*y*z**2`; {"x": "source symbol x", "y": "source symbol y", "z": "source symbol z"} |

**Original worked solution:**

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}|\begin{aligned}3\sqrt{x} & {z}^{2} \\ 2y & -\sqrt{x}\end{aligned}| & =3\sqrt{x}\cdot (-\sqrt{x})-{z}^{2}\cdot 2y \\  & =-3x-2y{z}^{2}\end{aligned}
$$

## q-69650 — moderate

**Specific components:** {"entries": ["-2r", "3s", "-2t", "3u"], "ad": "-6*i*k", "bc": "-6*j*t", "symbol_aliases": {"r": "i", "s": "j", "u": "k"}, "domains": "Real variables; x >= 0 in templates containing sqrt(x).", "expected_answer": "- 6 i k + 6 j t"}

**Template:** `M3-four-symbols-factor-radio`

Calculate $det(H)$, if
    $H=[\begin{aligned}-2r & 3s \\ -2t & 3u\end{aligned}].$

| Field | Type | Bank profile | Source answer entity | Original value | Source correct | Value recipe |
|---|---|---|---:|---|---|---|
| selection | radio | bank-q-69650 | 17592186333328 | $6(ru-st)$ | False | `6*i*k - 6*j*t`; {"i": "source symbol r", "j": "source symbol s", "k": "source symbol u", "t": "source symbol t"} |
| selection | radio | bank-q-69650 | 17592186333736 | $6ru-3st$ | False | `6*i*k - 3*j*t`; {"i": "source symbol r", "j": "source symbol s", "k": "source symbol u", "t": "source symbol t"} |
| selection | radio | bank-q-69650 | 17592186334293 | $6(st-ru)$ | True | `ad - bc`; {"a": "-2*i", "b": "3*j", "c": "-2*t", "d": "3*k"} |
| selection | radio | bank-q-69650 | 17592186334635 | $-6ru+3st$ | False | `-6*i*k + 3*j*t`; {"i": "source symbol r", "j": "source symbol s", "k": "source symbol u", "t": "source symbol t"} |
| selection | radio | bank-q-69650 | 17592186335181 | $3(2st-ru)$ | False | `-3*i*k + 6*j*t`; {"i": "source symbol r", "j": "source symbol s", "k": "source symbol u", "t": "source symbol t"} |

**Original worked solution:**

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(H) & =|\begin{aligned}-2r & 3s \\ -2t & 3u\end{aligned}| \\  & =-2r\cdot 3u-3s\cdot (-2t) \\  & =-6ru-(-6st) \\  & =-6ru+6st \\  & =6(st-ru)\end{aligned}
$$
