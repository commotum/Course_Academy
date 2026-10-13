# Template extraction

Every original question, field, choice, exact bank value and solution is retained in reference/source.edn and reference/source.json. contract.json assigns every complete source to exactly one template/profile and records every original option as an exact coefficient, rational exponent and affine-base shift offset, along with its complete printed expression and correct designation. No pooled or mixed banks are used. The misconceptions behind unusual options remain unresolved; exact observed expressions are retained. Blanks and additional field shapes are absent.

Shared pattern: rewrite a root or reciprocal root as (a v+b)^p, let u=a v+b, use dv=du/a, integrate u^p, substitute back, and verify by differentiation. Correct antiderivative coefficient is 1/[a(p+1)]. Real odd roots use the real branch; even roots require nonnegative base. Reciprocal roots exclude zero. Work on open intervals away from zero for differentiation. Some source distractors have additional real-domain restrictions, recorded in generation metadata.

Parameter extraction preserves each source slope a, exponent p, variable and exact option coefficients. Only b varies. This intentionally narrower policy avoids inferring general coefficient recipes from one observed bank. Bounds are integer b in [-100,100] excluding zero, retaining observed shifts -100, -1, 1, 3 and 11. All eight profiles are available; there are 600 distinct moderate and 1000 distinct hard affine integrands in these bounds before existing-content exclusions. Changing seed, profile identity or bank order does not add a mathematical question.

Fixed: root index, powers, slope, option coefficients, radio field key and choice count, instructional sentences and solution sequence. Variable: every occurrence of the affine base in prompt, choices and solution. Conditional: negative-slope base is rendered b+a v; positive-slope base is rendered a v+b. q-49393 has one distractor whose base offset is b-2 (observed 1-5s compared to prompt 3-5s); that offset moves with b. The generator keeps exact original notation. No new assets are required.

## q-49391

Source entity 17592186064861; moderate; variable y; base 4y-1; slope 4; shift -1; integrand exponent -1/2.

Prompt template: $\int \frac{1}{\sqrt{@@BASE@@}}\,\text{d}y=$

| Original option template | Coefficient | Exponent | Base offset | Correct |
|---|---|---|---|---|
| `\frac{\sqrt{@@BASE@@}}{2}+C` | 1/2 | 1/2 | 0 | True |
| `\frac{\sqrt{@@BASE@@}}{3}+C` | 1/3 | 1/2 | 0 | False |
| `\frac{\sqrt{@@BASE@@}}{4}+C` | 1/4 | 1/2 | 0 | False |
| `\frac{3\sqrt{@@BASE@@}}{2}+C` | 3/2 | 1/2 | 0 | False |
| `\sqrt{@@BASE@@}+C` | 1 | 1/2 | 0 | False |

Worked-solution template:

First, we rewrite the integral as

$$
\int (@@BASE@@)^{-1/2}\,\text{d}y.
$$

Now, we let $u=@@BASE@@.$ Then differentiating with respect to $y$ gives

$$
\frac{\text{d}u}{\text{d}y}=4\,⟹\,\text{d}y=\frac{1}{4}\text{d}u.
$$

We now write our integral in terms of $u,$ calculate the integral as normal, and write the final answer in terms of $u$ at the very end:

$$
\begin{aligned}\int (@@BASE@@)^{-1/2}\,\text{d}y & =\int {u}^{-1/2}\cdot \frac{1}{4}\,\text{d}u \\  & =\frac{1}{4}\int {u}^{-1/2}\,\text{d}u \\  & =\frac{1}{4}\cdot \frac{1}{(1/2)}{u}^{1/2}+C \\  & =\frac{2}{4}\cdot {u}^{1/2}+C \\  & =\frac{1}{2}(@@BASE@@)^{1/2}+C \\  & =\frac{\sqrt{@@BASE@@}}{2}+C\end{aligned}
$$

Let's double-check that our result is correct. If we differentiate the result, then it should come out to the original integrand:

$$
\begin{aligned}\frac{\text{d}}{\text{d}y}[\frac{\sqrt{@@BASE@@}}{2}+C] & =\frac{1}{2}\cdot \frac{\text{d}}{\text{d}y}[\sqrt{@@BASE@@}]+\frac{\text{d}}{\text{d}y}(C) \\  & =\frac{1}{2}\cdot \frac{\text{d}}{\text{d}y}[(@@BASE@@)^{1/2}]+\frac{\text{d}}{\text{d}y}(C) \\  & =\frac{1}{2}\cdot \frac{1}{2}(@@BASE@@)^{-1/2}\cdot \frac{\text{d}}{\text{d}y}(@@BASE@@)+0 \\  & =\frac{1}{4}(@@BASE@@)^{-1/2}\cdot 4 \\  & =\frac{1}{\sqrt{@@BASE@@}}\,✓\end{aligned}
$$

## q-17019

Source entity 17592186284623; hard; variable x; base 3-4x; slope -4; shift 3; integrand exponent 2/3.

Prompt template: Calculate the integral
$\int \sqrt[3]{(@@BASE@@)^{2}}\,\text{d}x.$

| Original option template | Coefficient | Exponent | Base offset | Correct |
|---|---|---|---|---|
| `-\frac{1}{5}\sqrt[3]{(@@BASE@@)^{5}}+C` | -1/5 | 5/3 | 0 | False |
| `-\frac{3}{20}\sqrt[3]{(@@BASE@@)^{5}}+C` | -3/20 | 5/3 | 0 | True |
| `-\frac{1}{5}\sqrt[3]{(@@BASE@@)^{2}}+C` | -1/5 | 2/3 | 0 | False |
| `-\frac{3}{5}\sqrt[3]{(@@BASE@@)^{5}}+C` | -3/5 | 5/3 | 0 | False |
| `-\frac{3}{20}\sqrt[3]{(@@BASE@@)^{2}}+C` | -3/20 | 2/3 | 0 | False |

Worked-solution template:

First, we rewrite the integral as

$$
\int (@@BASE@@)^{2/3}\,\text{d}x.
$$

Now, we let  $u=@@BASE@@.$ Then differentiating with respect to $x$ gives

$$
\frac{\text{d}u}{\text{d}x}=-4\,⟹\,\text{d}x=-\frac{1}{4}\text{d}u.
$$

We now write our integral in terms of $u,$ calculate the integral as normal, and write the final answer in terms of $u$ at the very end:

$$
\begin{aligned}\int (@@BASE@@)^{2/3}\,\text{d}x & =\int {u}^{2/3}\cdot (-\frac{1}{4})\,\text{d}u \\  & =-\frac{1}{4}\int {u}^{2/3}\,\text{d}u \\  & =-\frac{1}{4}\cdot \frac{1}{5/3}{u}^{5/3}+C \\  & =-\frac{1}{4}\cdot \frac{3}{5}{u}^{5/3}+C \\  & =-\frac{3}{20}{u}^{5/3}+C \\  & =-\frac{3}{20}(@@BASE@@)^{5/3}+C \\  & =-\frac{3}{20}\sqrt[3]{(@@BASE@@)^{5}}+C\end{aligned}
$$

Let's double-check that our result is correct. If we differentiate the result, then it should come out to the original integrand:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}[-\frac{3}{20}(@@BASE@@)^{5/3}+C] & =-\frac{3}{20}\cdot \frac{\text{d}}{\text{d}x}[(@@BASE@@)^{5/3}]+\frac{\text{d}}{\text{d}x}(C) \\  & =-\frac{3}{20}\cdot \frac{5}{3}(@@BASE@@)^{2/3}\cdot \frac{\text{d}}{\text{d}x}(@@BASE@@)+0 \\  & =-\frac{1}{4}(@@BASE@@)^{3/2}\cdot (-4) \\  & =(@@BASE@@)^{3/2} \\  & =\sqrt[3]{(@@BASE@@)^{2}}\,✓\end{aligned}
$$

## q-49393

Source entity 17592186332709; hard; variable s; base 3-5s; slope -5; shift 3; integrand exponent -2/3.

Prompt template: $\int \frac{1}{\sqrt[3]{(@@BASE@@)^{2}}}\,\text{d}s=$

| Original option template | Coefficient | Exponent | Base offset | Correct |
|---|---|---|---|---|
| `\sqrt{@@BASE@@}+C` | 1 | 1/2 | 0 | False |
| `\frac{5}{3\sqrt[4]{@@ALTERED@@}}+C` | 5/3 | -1/4 | -2 | False |
| `-\frac{5}{7}\sqrt[3]{@@BASE@@}+C` | -5/7 | 1/3 | 0 | False |
| `-\frac{3}{5}\sqrt[3]{@@BASE@@}+C` | -3/5 | 1/3 | 0 | True |
| `\frac{1}{\sqrt[3]{@@BASE@@}}+C` | 1 | -1/3 | 0 | False |

Worked-solution template:

First, we rewrite the integral as

$$
\int (@@BASE@@)^{-2/3}\,\text{d}s.
$$

Now, we let  $u=@@BASE@@.$ Then differentiating with respect to $s$ gives

$$
\frac{\text{d}u}{\text{d}s}=-5\,⟹\,\text{d}s=-\frac{1}{5}\text{d}u.
$$

We now write our integral in terms of $u,$ calculate the integral as normal, and write the final answer in terms of $u$ at the very end:

$$
\begin{aligned}\int (@@BASE@@)^{-2/3}\,\text{d}s & =\int {u}^{-2/3}\cdot (-\frac{1}{5}\text{d}u) \\  & =-\frac{1}{5}\int {u}^{-2/3}\,\text{d}u \\  & =-\frac{1}{5}\cdot \frac{1}{1/3}{u}^{1/3}+C \\  & =-\frac{3}{5}{u}^{1/3}+C \\  & =-\frac{3}{5}(@@BASE@@)^{1/3}+C \\  & =-\frac{3}{5}\sqrt[3]{@@BASE@@}+C\end{aligned}
$$

Let's double-check that our result is correct. If we differentiate the result, then it should come out to the original integrand:

$$
\begin{aligned}\frac{\text{d}}{\text{d}s}[-\frac{3}{5}\sqrt[3]{@@BASE@@}+C] & =-\frac{3}{5}\cdot \frac{\text{d}}{\text{d}s}[\sqrt[3]{@@BASE@@}]+\frac{\text{d}}{\text{d}s}(C) \\  & =-\frac{3}{5}\cdot \frac{\text{d}}{\text{d}s}[(@@BASE@@)^{1/3}]+\frac{\text{d}}{\text{d}s}(C) \\  & =-\frac{3}{5}\cdot \frac{1}{3}(@@BASE@@)^{-2/3}\cdot \frac{\text{d}}{\text{d}s}(@@BASE@@)+0 \\  & =-\frac{1}{5}(@@BASE@@)^{-2/3}\cdot (-5) \\  & =(@@BASE@@)^{-2/3} \\  & =\frac{1}{\sqrt[3]{(@@BASE@@)^{2}}}\,✓\end{aligned}
$$

## q-49437

Source entity 17592186332715; hard; variable y; base y+11; slope 1; shift 11; integrand exponent 5/3.

Prompt template: Calculate the integral $\int \sqrt[3]{(@@BASE@@)^{5}}\,\text{d}y.$

| Original option template | Coefficient | Exponent | Base offset | Correct |
|---|---|---|---|---|
| `8\sqrt[3]{(@@BASE@@)^{5}}+C` | 8 | 5/3 | 0 | False |
| `\frac{8}{3}\sqrt[3]{(@@BASE@@)^{2}}+C` | 8/3 | 2/3 | 0 | False |
| `\sqrt[3]{(@@BASE@@)^{8}}+C` | 1 | 8/3 | 0 | False |
| `\frac{3}{8}\sqrt[3]{(@@BASE@@)^{8}}+C` | 3/8 | 8/3 | 0 | True |
| `3\sqrt[3]{(@@BASE@@)^{8}}+C` | 3 | 8/3 | 0 | False |

Worked-solution template:

First, we rewrite the integral as

$$
\int (@@BASE@@)^{5/3}\,\text{d}y.
$$

Now, we let $u=@@BASE@@.$ Then differentiating with respect to $y$ gives

$$
\frac{\text{d}u}{\text{d}y}=1\,⟹\,\text{d}y=\text{d}u.
$$

We now write our integral in terms of $u,$ calculate the integral as normal, and write the final answer in terms of $u$ at the very end:

$$
\begin{aligned}\int (@@BASE@@)^{5/3}\,\text{d}y & =\int {u}^{5/3}\,\text{d}u \\  & =\frac{{u}^{8/3}}{8/3}+C \\  & =\frac{3}{8}(@@BASE@@)^{8/3}+C \\  & =\frac{3}{8}\sqrt[3]{(@@BASE@@)^{8}}+C\end{aligned}
$$

Let's double-check that our result is correct. If we differentiate the result, then it should come out to the original integrand:

$$
\begin{aligned}\frac{\text{d}}{\text{d}y}[\frac{3}{8}\sqrt[3]{(@@BASE@@)^{8}}] & =\frac{3}{8}\cdot \frac{\text{d}}{\text{d}y}[\sqrt[3]{(@@BASE@@)^{8}}]+\frac{\text{d}}{\text{d}y}(C) \\  & =\frac{3}{8}\cdot \frac{\text{d}}{\text{d}y}[(@@BASE@@)^{8/3}]+\frac{\text{d}}{\text{d}y}(C) \\  & =\frac{3}{8}\cdot \frac{8}{3}(@@BASE@@)^{5/3}\cdot \frac{\text{d}}{\text{d}y}(@@BASE@@)+0 \\  & =(@@BASE@@)^{5/3}\cdot 1 \\  & =\sqrt[3]{(@@BASE@@)^{5}}\,✓\end{aligned}
$$

## q-12498

Source entity 17592186395728; moderate; variable x; base 5x+1; slope 5; shift 1; integrand exponent 1/2.

Prompt template: $\int \sqrt{@@BASE@@}\,\text{d}x=$

| Original option template | Coefficient | Exponent | Base offset | Correct |
|---|---|---|---|---|
| `\frac{1}{5}\sqrt{(@@BASE@@)^{3}}+C` | 1/5 | 3/2 | 0 | False |
| `\frac{2}{3}\sqrt{@@BASE@@}+C` | 2/3 | 1/2 | 0 | False |
| `\frac{1}{5}\sqrt{@@BASE@@}+C` | 1/5 | 1/2 | 0 | False |
| `\frac{2}{15}\sqrt{(@@BASE@@)^{3}}+C` | 2/15 | 3/2 | 0 | True |
| `\frac{2}{3}\sqrt{(@@BASE@@)^{3}}+C` | 2/3 | 3/2 | 0 | False |

Worked-solution template:

First, we rewrite the integral as

$$
\int (@@BASE@@)^{1/2}\,\text{d}x.
$$

Now, we let $u=@@BASE@@.$ Then differentiating with respect to $x$ gives

$$
\frac{\text{d}u}{\text{d}x}=5\,⟹\,\text{d}x=\frac{1}{5}\text{d}u.
$$

We now write our integral in terms of $u,$ calculate the integral as normal, and write the final answer in terms of $u$ at the very end:

$$
\begin{aligned}\int (@@BASE@@)^{1/2}\,\text{d}x & =\int {u}^{1/2}\cdot (\frac{1}{5})\,\text{d}u \\  & =\frac{1}{5}\int {u}^{1/2}\,\text{d}u \\  & =\frac{1}{5}\cdot \frac{2}{3}{u}^{3/2}+C \\  & =\frac{2}{15}{u}^{3/2}+C \\  & =\frac{2}{15}(@@BASE@@)^{3/2}+C \\  & =\frac{2}{15}\sqrt{(@@BASE@@)^{3}}+C\end{aligned}
$$

Let's double-check that our result is correct. If we differentiate the result, then it should come out to the original integrand:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}[\frac{2}{15}\sqrt{(@@BASE@@)^{3}}+C] & =\frac{2}{15}\cdot \frac{\text{d}}{\text{d}x}[\sqrt{(@@BASE@@)^{3}}]+\frac{\text{d}}{\text{d}x}(C) \\  & =\frac{2}{15}\cdot \frac{\text{d}}{\text{d}x}[(@@BASE@@)^{3/2}]+\frac{\text{d}}{\text{d}x}(C) \\  & =\frac{2}{15}\cdot \frac{3}{2}(@@BASE@@)^{1/2}\cdot \frac{\text{d}}{\text{d}x}(@@BASE@@)+0 \\  & =\frac{1}{5}(@@BASE@@)^{1/2}\cdot 5 \\  & =(@@BASE@@)^{1/2} \\  & =\sqrt{@@BASE@@}\,✓\end{aligned}
$$

## q-49431

Source entity 17592186398869; moderate; variable z; base 1-9z; slope -9; shift 1; integrand exponent -1/2.

Prompt template: Calculate $\int \frac{1}{\sqrt{@@BASE@@}}\,\text{d}z.$

| Original option template | Coefficient | Exponent | Base offset | Correct |
|---|---|---|---|---|
| `-\frac{2}{9}\sqrt{(@@BASE@@)^{3}}+C` | -2/9 | 3/2 | 0 | False |
| `-2\sqrt{@@BASE@@}+C` | -2 | 1/2 | 0 | False |
| `-\frac{2}{9}\sqrt{@@BASE@@}+C` | -2/9 | 1/2 | 0 | True |
| `9\sqrt{@@BASE@@}+C` | 9 | 1/2 | 0 | False |
| `2\sqrt{(@@BASE@@)^{3}}+C` | 2 | 3/2 | 0 | False |

Worked-solution template:

First, we rewrite the integral as

$$
\int (@@BASE@@)^{-1/2}\,\text{d}z.
$$

Now, we let $u=@@BASE@@.$ Then differentiating with respect to $z$ gives

$$
\frac{\text{d}u}{\text{d}z}=-9\,⟹\,\text{d}z=-\frac{1}{9}\text{d}u.
$$

We now write our integral in terms of $u,$ calculate the integral as normal, and write the final answer in terms of $u$ at the very end:

$$
\begin{aligned}\int (@@BASE@@)^{-1/2}\,\text{d}z & =\int {u}^{-1/2}\cdot (-\frac{1}{9}\text{d}u) \\  & =-\frac{1}{9}\int {u}^{-1/2}\,\text{d}u \\  & =-\frac{1}{9}\frac{1}{(1/2)}{u}^{1/2}+C \\  & =-\frac{2}{9}{u}^{1/2}+C \\  & =-\frac{2}{9}(@@BASE@@)^{1/2}+C \\  & =-\frac{2}{9}\sqrt{@@BASE@@}+C\end{aligned}
$$

Let's double-check that our result is correct. If we differentiate the result, then it should come out to the original integrand:

$$
\begin{aligned}\frac{\text{d}}{\text{d}z}[-\frac{2}{9}\sqrt{@@BASE@@}+C] & =-\frac{2}{9}\cdot \frac{\text{d}}{\text{d}z}[\sqrt{@@BASE@@}]+\frac{\text{d}}{\text{d}z}(C) \\  & =-\frac{2}{9}\cdot \frac{\text{d}}{\text{d}z}[(@@BASE@@)^{1/2}]+\frac{\text{d}}{\text{d}z}(C) \\  & =-\frac{2}{9}\cdot \frac{1}{2}(@@BASE@@)^{-1/2}\cdot \frac{\text{d}}{\text{d}z}(@@BASE@@)+0 \\  & =-\frac{1}{9}\cdot (@@BASE@@)^{-1/2}\cdot (-9) \\  & =(@@BASE@@)^{-1/2} \\  & =\frac{1}{\sqrt{@@BASE@@}}\,✓\end{aligned}
$$

## q-49439

Source entity 17592186398876; hard; variable x; base x-100; slope 1; shift -100; integrand exponent 7/4.

Prompt template: Calculate the integral $\int \sqrt[4]{(@@BASE@@)^{7}}\,\text{d}x.$

| Original option template | Coefficient | Exponent | Base offset | Correct |
|---|---|---|---|---|
| `\frac{4}{11}\sqrt[4]{(@@BASE@@)^{11}}+C` | 4/11 | 11/4 | 0 | True |
| `\sqrt[4]{(@@BASE@@)^{11}}+C` | 1 | 11/4 | 0 | False |
| `11\sqrt[4]{(@@BASE@@)^{11}}+C` | 11 | 11/4 | 0 | False |
| `\sqrt[4]{(@@BASE@@)^{9}}+C` | 1 | 9/4 | 0 | False |
| `\frac{4}{9}\sqrt[4]{(@@BASE@@)^{9}}+C` | 4/9 | 9/4 | 0 | False |

Worked-solution template:

First, we rewrite the integral as

$$
\int (@@BASE@@)^{7/4}\,\text{d}x.
$$

Now, we let  $u=@@BASE@@.$ Then differentiating with respect to $x$ gives

$$
\frac{\text{d}u}{\text{d}x}=1\,⟹\,\text{d}x=\text{d}u.
$$

We now write our integral in terms of $u,$ calculate the integral as normal, and write the final answer in terms of $u$ at the very end:

$$
\begin{aligned}\int (@@BASE@@)^{7/4}\,\text{d}x & =\int {u}^{7/4}\,\text{d}u \\  & =\frac{{u}^{11/4}}{11/4}+C \\  & =\frac{4}{11}(@@BASE@@)^{11/4}+C \\  & =\frac{4}{11}\sqrt[4]{(@@BASE@@)^{11}}+C\end{aligned}
$$

Let's double-check that our result is correct. If we differentiate the result, then it should come out to the original integrand:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}[\frac{4}{11}\sqrt[4]{(@@BASE@@)^{11}}+C] & =\frac{4}{11}\cdot \frac{\text{d}}{\text{d}x}[\sqrt[4]{(@@BASE@@)^{11}}]+\frac{\text{d}}{\text{d}x}(C) \\  & =\frac{4}{11}\cdot \frac{\text{d}}{\text{d}x}[(@@BASE@@)^{11/4}]+\frac{\text{d}}{\text{d}x}(C) \\  & =\frac{4}{11}\cdot \frac{11}{4}(@@BASE@@)^{7/4}\cdot \frac{\text{d}}{\text{d}x}(@@BASE@@)+0 \\  & =(@@BASE@@)^{7/4}\cdot 1 \\  & =\sqrt[4]{(@@BASE@@)^{7}}\,✓\end{aligned}
$$

## q-49468

Source entity 17592186398883; hard; variable s; base s+1; slope 1; shift 1; integrand exponent -3/5.

Prompt template: $\int \frac{1}{\sqrt[5]{{(@@BASE@@)}^{3}}}\,\text{d}s=$

| Original option template | Coefficient | Exponent | Base offset | Correct |
|---|---|---|---|---|
| `5\sqrt[5]{{(@@BASE@@)}^{3}}+C` | 5 | 3/5 | 0 | False |
| `2\sqrt[5]{{(@@BASE@@)}^{2}}+C` | 2 | 2/5 | 0 | False |
| `\sqrt[5]{{(@@BASE@@)}^{2}}+C` | 1 | 2/5 | 0 | False |
| `\frac{1}{2}\sqrt[5]{{(@@BASE@@)}^{3}}+C` | 1/2 | 3/5 | 0 | False |
| `\frac{5}{2}\sqrt[5]{{(@@BASE@@)}^{2}}+C` | 5/2 | 2/5 | 0 | True |

Worked-solution template:

First, we rewrite the integral as

$$
\int {(@@BASE@@)}^{-3/5}\,\text{d}s.
$$

Now, we let  $u=@@BASE@@.$ Then differentiating with respect to $s$ gives

$$
\frac{\text{d}u}{\text{d}s}=1\,⟹\,\text{d}s=\text{d}u.
$$

We now write our integral in terms of $u,$ calculate the integral as normal, and write the final answer in terms of $u$ at the very end:

$$
\begin{aligned}\int {(@@BASE@@)}^{-3/5}\,\text{d}s & =\int {u}^{-3/5}\,\text{d}u \\  & =\frac{1}{2/5}{u}^{2/5}+C \\  & =\frac{5}{2}{u}^{2/5}+C \\  & =\frac{5}{2}{(@@BASE@@)}^{2/5}+C \\  & =\frac{5}{2}\sqrt[5]{{(@@BASE@@)}^{2}}+C\end{aligned}
$$

Let's double-check that our result is correct. If we differentiate the result, then it should come out to the original integrand:

$$
\begin{aligned}\frac{\text{d}}{\text{d}s}[\frac{5}{2}\sqrt[5]{{(@@BASE@@)}^{2}}+C] & =\frac{5}{2}\cdot \frac{\text{d}}{\text{d}s}[\sqrt[5]{{(@@BASE@@)}^{2}}]+\frac{\text{d}}{\text{d}s}(C) \\  & =\frac{5}{2}\cdot \frac{\text{d}}{\text{d}s}[{(@@BASE@@)}^{2/5}]+\frac{\text{d}}{\text{d}s}(C) \\  & =\frac{5}{2}\cdot \frac{2}{5}{(@@BASE@@)}^{-3/5}\cdot \frac{\text{d}}{\text{d}s}(@@BASE@@)+0 \\  & ={(@@BASE@@)}^{-3/5}\cdot 1 \\  & =\frac{1}{\sqrt[5]{{(@@BASE@@)}^{3}}}\,✓\end{aligned}
$$
