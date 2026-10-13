# Template extraction

## Stage 1: specific source descriptions

All original strings and fields appear below and in raw source.json. No source was omitted. Numbers, notation, fragment location, full option ownership and exact mathematical values are preserved. Parameters listed here are observed values, not recovered sampling code.

### q-1933

Parameters: `{"c": 5, "b": 3}`; template `log_log_radio`; profile `log_log_observed`.

Given that $f(x) = 5\log_{3} x\ln x$, find $f^{′}(x)$.

Field: `:answer-field.type/radio`; key `selection`.

Original worked solution:

Absent. The four-row solution in generated replay is authored from the displayed product; it is not counted as source solution fidelity.

| Original option (exact bytes after JSON decoding) | Parameterized recipe | Designation |
|---|---|---|
| `$\frac{5\log_{3} x}{x} + \frac{5\ln x}{x}$` | omit_base_scale; exact expression `5*log(x)/(x*log(3)) + 5*log(x)/x` at these parameters | distractor |
| `$\frac{5}{x} + \frac{5\ln x}{x\ln 3}$` | drop_log_first; exact expression `5*log(x)/(x*log(3)) + 5/x` at these parameters | distractor |
| `$\frac{5\log_{3} x}{x} + \frac{\ln x}{x\ln 3}$` | drop_coefficient_second; exact expression `6*log(x)/(x*log(3))` at these parameters | distractor |
| `$\frac{5\log_{3} x}{x} + \frac{5\ln x}{x\ln 3}$` | correct; exact expression `10*log(x)/(x*log(3))` at these parameters | correct, derived because original ref absent |
| `$\frac{5\log_{3} x}{x} + \frac{5}{x\ln 3}$` | drop_log_second; exact expression `5*log(x)/(x*log(3)) + 5/(x*log(3))` at these parameters | distractor |

### q-47966

Parameters: `{"n": -3, "b": 2}`; template `power_log_radio`; profile `power_log_observed`.

Given that $f(x) = x^{-3}\log_{2} x$, find $f^{′}(x)$.

Field: `:answer-field.type/radio`; key `selection`.

Original worked solution:

Absent. The four-row solution in generated replay is authored from the displayed product; it is not counted as source solution fidelity.

| Original option (exact bytes after JSON decoding) | Parameterized recipe | Designation |
|---|---|---|
| `$-3x^{-4}\log_{2} x + x^{-3} \cdot \frac{1}{x}$` | omit_base_scale; exact expression `-3*log(x)/(x**4*log(2)) + x**(-4)` at these parameters | distractor |
| `$-3x^{-4} \cdot \frac{1}{x\ln 2}$` | multiply_derivatives; exact expression `-3/(x**5*log(2))` at these parameters | distractor |
| `$x^{-3}(3\log_{2} x - \frac{1}{\ln 2})$` | negate_and_wrong_power; exact expression `(3*log(x)/log(2) - 1/log(2))/x**3` at these parameters | distractor |
| `$-3x^{-4} + \frac{1}{x\ln 2}$` | sum_derivatives; exact expression `1/(x*log(2)) - 3/x**4` at these parameters | distractor |
| `$x^{-4}(-3\log_{2} x + \frac{1}{\ln 2})$` | correct; exact expression `(-3*log(x)/log(2) + 1/log(2))/x**4` at these parameters | correct, derived because original ref absent |

### q-319421

Parameters: `{"b": 5}`; template `base_sin_left_blank`; profile `None`.

Given that $f(x)={5}^{x}\operatorname{sin}(x),$ find ${f}^{'}(x).$

${f}^{'}(x)=$
{{field-1}} $+\,{5}^{x}\operatorname{cos}(x)$

Field: `:answer-field.type/blank`; key `field-1`.

Original worked solution:

Here, we have the product of two functions $u(x)={5}^{x}$ and $v(x)=\operatorname{sin}(x).$ So, we apply the product rule:

$$
\begin{aligned}{f}^{'}(x) & ={({5}^{x})}^{'}\operatorname{sin}(x)+{5}^{x}{(\operatorname{sin}(x))}^{'} \\  & =({5}^{x}\operatorname{ln}(5))\operatorname{sin}(x)+{5}^{x}(\operatorname{cos}(x)) \\  & ={5}^{x}\operatorname{ln}(5)\operatorname{sin}(x)+{5}^{x}\operatorname{cos}(x)\end{aligned}
$$

| Original option (exact bytes after JSON decoding) | Parameterized recipe | Designation |
|---|---|---|
| `${5}^{x}\operatorname{ln}(5)\operatorname{sin}(x)$` | fragment; exact expression `5**x*log(5)*sin(x)` at these parameters | correct |

### q-319909

Parameters: `{"c": 1, "n": 2, "k": 2}`; template `power_exp_right_blank`; profile `None`.

Given that $f(x)={x}^{2}{e}^{2x},$ find ${f}^{'}(x).$

${f}^{'}(x)=2x{e}^{2x}\,+$
{{field-1}}

Field: `:answer-field.type/blank`; key `field-1`.

Original worked solution:

Here, we have the product of two functions $u(x)={x}^{2}$ and $v(x)={e}^{2x}.$ So, we apply the product rule:

$$
\begin{aligned}{f}^{'}(x) & =({x}^{2})^{'}{e}^{2x}+{x}^{2}({e}^{2x})^{'} \\  & =(2x)({e}^{2x})+({x}^{2})(2{e}^{2x}) \\  & =2x{e}^{2x}+2{x}^{2}{e}^{2x}\end{aligned}
$$

| Original option (exact bytes after JSON decoding) | Parameterized recipe | Designation |
|---|---|---|
| `$2{x}^{2}{e}^{2x}$` | fragment; exact expression `2*x**2*exp(2*x)` at these parameters | correct |

### q-11841

Parameters: `{"b": 3}`; template `linear_base_radio`; profile `linear_base_observed`.

Given that $f(x)=x\cdot {3}^{x},$ find ${f}^{′}(x).$

Field: `:answer-field.type/radio`; key `selection`.

Original worked solution:

Here, we have the product of two functions $u(x)=x$ and $v(x)={3}^{x}.$ So, we apply the product rule:

$$
\begin{aligned}{f}^{′}(x) & =(x)^{′}\cdot {3}^{x}+x\cdot ({3}^{x})^{′} \\  & ={3}^{x}+(x)(\operatorname{ln}⁡3\cdot {3}^{x}) \\  & ={3}^{x}+x\operatorname{ln}⁡3\cdot {3}^{x} \\  & =(1+x\operatorname{ln}⁡3){3}^{x}\end{aligned}
$$

| Original option (exact bytes after JSON decoding) | Parameterized recipe | Designation |
|---|---|---|
| `$\operatorname{ln}⁡3\cdot {3}^{x}$` | omit_x_and_first; exact expression `3**x*log(3)` at these parameters | distractor |
| `$(1+\operatorname{ln}⁡3){3}^{x}$` | omit_x; exact expression `3**x*(1 + log(3))` at these parameters | distractor |
| `$(1+x\operatorname{ln}⁡3){3}^{x}$` | correct; exact expression `3**x*(x*log(3) + 1)` at these parameters | correct |
| `${3}^{x}$` | omit_second; exact expression `3**x` at these parameters | distractor |
| `$(x\operatorname{ln}⁡3){3}^{x}$` | omit_first; exact expression `3**x*x*log(3)` at these parameters | distractor |

### q-1916

Parameters: `{"n": 2, "k": 1, "c": 1}`; template `power_exp_radio`; profile `power_exp_observed`.

Given that $f(x)={x}^{2}{e}^{x},$ find ${f}^{′}(x).$

Field: `:answer-field.type/radio`; key `selection`.

Original worked solution:

Here, we have the product of two functions $u(x)={x}^{2}$ and $v(x)={e}^{x}.$ So, we apply the product rule:

$$
\begin{aligned}{f}^{′}(x) & =({x}^{2})^{′}{e}^{x}+{x}^{2}({e}^{x})^{′} \\  & =(2x)({e}^{x})+({x}^{2})({e}^{x}) \\  & =2x{e}^{x}+{x}^{2}{e}^{x} \\  & =(x+2)x{e}^{x}\end{aligned}
$$

| Original option (exact bytes after JSON decoding) | Parameterized recipe | Designation |
|---|---|---|
| `$(x+2)x{e}^{x}$` | correct; exact expression `x*(x + 2)*exp(x)` at these parameters | correct |
| `$2{x}^{2}{e}^{x}$` | power_not_decreased; exact expression `2*x**2*exp(x)` at these parameters | distractor |
| `$x(2{e}^{x}+x)$` | omit_exp_second; exact expression `x*(x + 2*exp(x))` at these parameters | distractor |
| `$(x+1)x{e}^{x}$` | wrong_power_coefficient; exact expression `x*(x + 1)*exp(x)` at these parameters | distractor |
| `$x(x{e}^{x}+2)$` | omit_exp_first; exact expression `x*(x*exp(x) + 2)` at these parameters | distractor |

### q-1934

Parameters: `{"b": 10}`; template `cos_log_radio`; profile `cos_log_observed`.

Given that $f(x)=cos⁡xlog⁡x,$ find ${f}^{′}(x).$

Field: `:answer-field.type/radio`; key `selection`.

Original worked solution:

Here, we have the product of two functions $u(x)=cos⁡x$ and $v(x)=log⁡x.$ So, we apply the product rule:

$$
\begin{aligned}{f}^{′}(x) & ={(cos⁡x)}^{′}log⁡x+cos⁡x{(log⁡x)}^{′} \\  & =(-sin⁡x)(log⁡x)+(cos⁡x)(\frac{1}{xln⁡10}) \\  & =\frac{cos⁡x}{xln⁡10}-sin⁡xlog⁡x\end{aligned}
$$

| Original option (exact bytes after JSON decoding) | Parameterized recipe | Designation |
|---|---|---|
| `$\frac{cos⁡x}{ln⁡10}-sin⁡xlog⁡x$` | omit_x; exact expression `-log(x)*sin(x)/log(10) + cos(x)/log(10)` at these parameters | distractor |
| `$\frac{cos⁡x}{x}-sin⁡xlog⁡x$` | omit_base_scale; exact expression `-log(x)*sin(x)/log(10) + cos(x)/x` at these parameters | distractor |
| `$\frac{cos⁡x}{xln⁡10}+sin⁡xlog⁡x$` | wrong_trig_sign; exact expression `log(x)*sin(x)/log(10) + cos(x)/(x*log(10))` at these parameters | distractor |
| `$\frac{cos⁡x}{xln⁡10}-sin⁡xlog⁡x$` | correct; exact expression `-log(x)*sin(x)/log(10) + cos(x)/(x*log(10))` at these parameters | correct |
| `$\frac{cos⁡x}{x}-sin⁡x$` | drop_log_and_base_scale; exact expression `-sin(x) + cos(x)/x` at these parameters | distractor |

### q-319425

Parameters: `{"b": 4}`; template `base_tan_right_blank`; profile `None`.

Given that $f(x)={4}^{x}tan⁡(x),$ find ${f}^{′}(x).$

${f}^{′}(x)={4}^{x}ln⁡(4)tan⁡(x)\,+$
{{field-1}}

Field: `:answer-field.type/blank`; key `field-1`.

Original worked solution:

Here, we have the product of two functions $u(x)={4}^{x}$ and $v(x)=tan⁡(x).$ So, we apply the product rule:

$$
\begin{aligned}{f}^{′}(x) & ={({4}^{x})}^{′}tan⁡(x)+{4}^{x}{(tan⁡(x))}^{′} \\  & =({4}^{x}ln⁡(4))tan⁡(x)+{4}^{x}({sec}^{2}⁡(x)) \\  & ={4}^{x}ln⁡(4)tan⁡(x)+{4}^{x}{sec}^{2}⁡(x)\end{aligned}
$$

| Original option (exact bytes after JSON decoding) | Parameterized recipe | Designation |
|---|---|---|
| `${4}^{x}{sec}^{2}(x)$` | fragment; exact expression `4**x*(tan(x)**2 + 1)` at these parameters | correct |

### q-319902

Parameters: `{"c": 1, "n": 3, "k": 1}`; template `power_exp_left_blank`; profile `None`.

Given that $f(x)={x}^{3}{e}^{x},$ find ${f}^{′}(x).$

${f}^{′}(x)=$
{{field-1}} $+\,{x}^{3}{e}^{x}$

Field: `:answer-field.type/blank`; key `field-1`.

Original worked solution:

Here, we have the product of two functions $u(x)={x}^{3}$ and $v(x)={e}^{x}.$ So, we apply the product rule:

$$
\begin{aligned}{f}^{′}(x) & =({x}^{3})^{′}{e}^{x}+{x}^{3}({e}^{x})^{′} \\  & =(3{x}^{2})({e}^{x})+({x}^{3})({e}^{x}) \\  & =3{x}^{2}{e}^{x}+{x}^{3}{e}^{x}\end{aligned}
$$

| Original option (exact bytes after JSON decoding) | Parameterized recipe | Designation |
|---|---|---|
| `$3{x}^{2}{e}^{x}$` | fragment; exact expression `3*x**2*exp(x)` at these parameters | correct |

### q-319903

Parameters: `{"c": 5, "n": 2, "k": 1}`; template `power_exp_right_blank`; profile `None`.

Given that $f(x)=5{x}^{2}{e}^{x},$ find ${f}^{′}(x).$

${f}^{′}(x)=10x{e}^{x}\,+$
{{field-1}}

Field: `:answer-field.type/blank`; key `field-1`.

Original worked solution:

Here, we have the product of two functions $u(x)=5{x}^{2}$ and $v(x)={e}^{x}.$ So, we apply the product rule:

$$
\begin{aligned}{f}^{′}(x) & =(5{x}^{2})^{′}{e}^{x}+5{x}^{2}({e}^{x})^{′} \\  & =(10x)({e}^{x})+(5{x}^{2})({e}^{x}) \\  & =10x{e}^{x}+5{x}^{2}{e}^{x}\end{aligned}
$$

| Original option (exact bytes after JSON decoding) | Parameterized recipe | Designation |
|---|---|---|
| `$5{x}^{2}{e}^{x}$` | fragment; exact expression `5*x**2*exp(x)` at these parameters | correct |

### q-320814

Parameters: `{"b": 3, "d": 3, "k": 1}`; template `base_log_left_blank`; profile `None`.

Given that $f(x)={3}^{x}{log}_{3}⁡(x),$ find ${f}^{′}(x).$

${f}^{′}(x)=$
{{field-1}} $+\,\frac{{3}^{x}}{x\operatorname{ln}⁡(3)}$

Field: `:answer-field.type/blank`; key `field-1`.

Original worked solution:

Here, we have the product of the two functions $u(x)={3}^{x}$ and $v(x)={log}_{3}⁡(x).$ So, we apply the product rule:

$$
\begin{aligned}{f}^{′}(x) & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & ={({3}^{x})}^{′}{log}_{3}⁡(x)+{3}^{x}{({log}_{3}⁡(x))}^{′} \\  & =({3}^{x}\operatorname{ln}⁡(3))({log}_{3}⁡(x))+({3}^{x})(\frac{1}{x\operatorname{ln}⁡(3)}) \\  & ={3}^{x}\operatorname{ln}⁡(3){log}_{3}⁡(x)+\frac{{3}^{x}}{x\operatorname{ln}⁡(3)}\end{aligned}
$$

| Original option (exact bytes after JSON decoding) | Parameterized recipe | Designation |
|---|---|---|
| `${3}^{x}\operatorname{ln}(3){log}_{3}(x)$` | fragment; exact expression `3**x*log(x)` at these parameters | correct |

### q-320815

Parameters: `{"b": 4, "d": 4, "k": 1}`; template `base_log_right_blank`; profile `None`.

Given that $f(x)={4}^{x}{log}_{4}⁡(x),$ find ${f}^{′}(x).$

${f}^{′}(x)={4}^{x}\operatorname{ln}⁡(4){log}_{4}⁡(x)\,+$
{{field-1}}

Field: `:answer-field.type/blank`; key `field-1`.

Original worked solution:

Here, we have the product of the two functions $u(x)={4}^{x}$ and $v(x)={log}_{4}⁡(x).$ So, we apply the product rule:

$$
\begin{aligned}{f}^{′}(x) & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & ={({4}^{x})}^{′}{log}_{4}⁡(x)+{4}^{x}{({log}_{4}⁡(x))}^{′} \\  & =({4}^{x}\operatorname{ln}⁡(4))({log}_{4}⁡(x))+({4}^{x})(\frac{1}{x\operatorname{ln}⁡(4)}) \\  & ={4}^{x}\operatorname{ln}⁡(4){log}_{4}⁡(x)+\frac{{4}^{x}}{x\operatorname{ln}⁡(4)}\end{aligned}
$$

| Original option (exact bytes after JSON decoding) | Parameterized recipe | Designation |
|---|---|---|
| `$\frac{{4}^{x}}{x\operatorname{ln}(4)}$` | fragment; exact expression `4**x/(x*log(4))` at these parameters | correct |

### q-320816

Parameters: `{"b": 5, "d": 7, "k": -1}`; template `base_log_negative_left_blank`; profile `None`.

Given that $f(x)={5}^{-x}{log}_{7}⁡(x),$ find ${f}^{′}(x).$

${f}^{′}(x)=$
{{field-1}} $+\,\frac{{5}^{-x}}{xln⁡(7)}$

Field: `:answer-field.type/blank`; key `field-1`.

Original worked solution:

Here, we have the product of the two functions $u(x)={5}^{-x}$ and $v(x)={log}_{7}⁡(x).$ So, we apply the product rule:

$$
\begin{aligned}{f}^{′}(x) & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & ={({5}^{-x})}^{′}{log}_{7}⁡(x)+{5}^{-x}{({log}_{7}⁡(x))}^{′} \\  & =(-{5}^{-x}ln⁡(5))({log}_{7}⁡(x))+({5}^{-x})(\frac{1}{xln⁡(7)}) \\  & =-{5}^{-x}ln⁡(5){log}_{7}⁡(x)+\frac{{5}^{-x}}{xln⁡(7)}\end{aligned}
$$

| Original option (exact bytes after JSON decoding) | Parameterized recipe | Designation |
|---|---|---|
| `$-{5}^{-x}\operatorname{ln}(5){log}_{7}(x)$` | fragment; exact expression `-log(5)*log(x)/(5**x*log(7))` at these parameters | correct |

## Stage 2: shared mathematical pattern

Identify u and v from a displayed product containing an exponential or logarithmic function, differentiate each, substitute into u′v+uv′, distribute and collect/factor only where the source does. Blanks expect a single prescribed summand, not an interchangeable complete derivative. The two base-log layouts retain the supplied complement term and generic formal-rule row. Polynomial–exponential blanks omit the redundant final factored row; their radios keep it. The exponential-sine and exponential-tangent blanks have three rows, while base-log blanks have four. The cosine/common-log radio has three rows.

## Stage 3: components and complete bank operations

The per-source tables account for every displayed option. In generator code bank tuples contain complete parameterized rendered expressions, exact SymPy expressions and recipe labels. Wrong-operation labels are hypotheses about the displayed expression transformations, not recovered author intent and never learner feedback. The full five-member banks remain separate:

- log_log_observed: omit the logarithm-base derivative divisor, omit one logarithmic factor, omit the coefficient in only the second term, correct two-term product derivative, omit the other logarithmic factor. For c=1, the missing-coefficient option collides with correct; reject the whole explicit instance or resample the whole random instance.
- power_log_observed: omit ln b from log derivative, multiply derivatives, negate derivative structure with the wrong power, add derivatives, correct factored derivative.
- linear_base_observed: remove both x and first term, remove x from second term, correct, retain only first term, retain only second term.
- power_exp_observed: correct factorization; fail to reduce power and multiply by n; omit exponential in second term; use n−1 instead of n; omit exponential in first term.
- cos_log_observed: omit x denominator; omit ln b divisor; reverse sine sign; correct; omit log and base divisor together.

q-1933 and q-47966 have no source correct reference, solution, or difficulty. Differentiating 5 log_3 x ln x independently gives 10 ln x/(x ln 3), uniquely matching the fourth displayed option. Differentiating x^−3 log_2 x gives x^−4(−3 log_2 x+1/ln 2), uniquely matching the fifth displayed option. These two inferred references do not count as matched source designations. Raw capture is retained unchanged. Authored easy placement is based on atomic factors and a single product rule, comparable to the full easy exponential/cosine-log radios. Original MA widget excerpts were read from /home/jake/Developer/MA/DATA/Lessons/1109/Source/1109.json and preserved in widget-excerpts.json with hash. They confirm the two five-option radio layouts, lack any correct designation/explanation, and order their choices differently (derived correct letters a for1933 and d for47966). No mathematical or presentation repair is required for the existing 11 worked solutions; all 11 replay byte-exact. JSON serialization doubles backslashes visually, but decoded source command bytes use ordinary single backslashes. Unicode application characters and original math notation remain intact in observed replay, and formatting checks still apply.

## Stage 4: reusable masks and sampling bounds

The build function constructs complete component masks U,V,D,DV and complete row masks, with shared prose and source-specific punctuation/prime notation. It contains no source-record import, answer lookup or literal-source payload return branch. At original parameters every full bank is byte-exact; at changed parameters the same mathematical operations compute all answers and each intermediate row. Source-bank selection occurs as one complete profile before sampling; collisions reject the entire instance. Seeds shuffle owned radio options after correct identity is recorded.

Easy bases are integers 2..10. Polynomial–exponential blank coefficients are 1..6, powers 2..4, exponential scales 1..3. The observed polynomial–exponential radio retains scale 1 and powers 2..4 and common scalar coefficient 1..6, preserving its entire five-operation bank. Negative-power/log radio powers are −4..−1. Exponential-log negative layout uses −x, and other base-log layouts use kx for k=1..3. These are authored bounded sampling policies supported by observed structures, not claims about original randomization. Explicit calls obey identical guards. Invalid base, zero coefficient, collapsed degree and complete-bank ambiguity are failures, never silently substituted.

The authored moderate/hard solution has the common formal rule, actual factor operator row, component-derivative row and distribution/collection row. Coefficient signs use grouped sums. No eager CAS rewrite to hyperbolic functions occurs; natural-log notation uses ln. Mathematical-task fingerprints depend only on the canonical displayed product, excluding answer banks, profile names, and layout; content identity includes actual prompt, fixed worked solution, field type and complete displayed bank. Shuffling cannot change identity. Source profiles are not disguised as authored default banks.

Native alternate submissions normalize invisible Unicode application marks in source component-row notation; this affects test-entry spelling only, not replay learner content. The native parser reports unsupported notation for sec² followed by the invisible application mark, while the canonical source blank has no such mark and grades correctly. A mathematically equivalent ln4=2ln2 denominator rewrite yields native unresolved domain differences; a dedicated fixture records that real restriction, with source canonicals and supported unreduced component forms tested independently. Authored logarithmic distribution masks retain the displayed logarithm base and each original x·ln(base) denominator, while independently parsing every distributed term proves equality. Canceling x in those quotients is mathematically valid on the prompt’s logarithmic domain x>0, but the native grader retains a composite nonzero denominator guard and reports unresolved domain differences after the cancellation. A separate independently verified fixture records this native limitation. The distribution row still explicitly distributes every polynomial component and avoids introducing a new quotient differentiation task. All 75 supported accepted entries and 90 incorrect rejections pass; three dedicated unsupported/equivalent entries are reported explicitly unresolved. No engine changes were made.

No plots are present; plot extraction and generator stages 5/7 are not applicable beyond this checked none rating. This work stops before database preparation or registration.
