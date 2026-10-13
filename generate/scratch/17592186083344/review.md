## q-118619 original / replay

Evaluate the integral ${\int }_{0}^{\infty }\frac{x}{{(1+{x}^{2})}^{2}}\,\text{d}x.$

First, we substitute $u=1+{x}^{2}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\frac{1}{2}\text{d}u=x\,\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u=1+{x}^{2}$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $1$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{x}{{(1+{x}^{2})}^{2}}\,\text{d}x & =\frac{1}{2}{\int }_{1}^{\infty }\frac{1}{{u}^{2}}\,\text{d}u.\end{aligned}
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{x}{{(1+{x}^{2})}^{2}}\,\text{d}x & =\frac{1}{2}{\int }_{1}^{\infty }\frac{1}{{u}^{2}}\,\text{d}u \\  & =\frac{1}{2}{\int }_{1}^{\infty }{u}^{-2}\,\text{d}u \\  & =\frac{1}{2}{lim}_{a\to \infty }{\int }_{1}^{a}{u}^{-2}\,\text{d}u \\  & =\frac{1}{2}{lim}_{a\to \infty }[-{u}^{-1}]_{1}^{a} \\  & =-\frac{1}{2}{lim}_{a\to \infty }{[\frac{1}{u}]}_{1}^{a} \\  & =-\frac{1}{2}{lim}_{a\to \infty }(\frac{1}{a}-1) \\  & =-\frac{1}{2}(0-1) \\  & =\frac{1}{2}.\end{aligned}
$$

### Coefficient variant (scale 7)

Evaluate the integral ${\int }_{0}^{\infty }\frac{7 x}{(x^{2} + 1)^{2}}\,\text{d}x.$

First, we substitute $u=x^{2} + 1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=2 x\quad\Longrightarrow\quad\text{d}u=2 x\,\text{d}x.
$$

Since $u\to \infty$ when $x\to \infty,$ the table for the limits of integration using the rule $u=x^{2} + 1$ is as follows:

| $x$ | $0$ | $\infty$ |
| --- | --- | --- |
| $u$ | $1$ | $\infty$ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{7 x}{(x^{2} + 1)^{2}}\,\text{d}x=\frac{7}{2}\int_{1}^{\infty}u^{-2}\,\text{d}u.
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to\infty.$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{7 x}{(x^{2} + 1)^{2}}\,\text{d}x & =\frac{7}{2}\lim_{a\to\infty}\int_{1}^{a}u^{-2}\,\text{d}u \\ & =\lim_{a\to\infty}\left[- \frac{7}{2}u^{-1}\right]_{1}^{a} \\ & =- \frac{7}{2}\lim_{a\to\infty}\left(a^{-1}-1\right) \\ & =- \frac{7}{2}\left(0-1\right) \\ & =\frac{7}{2}.\end{aligned}
$$

---

## q-118618 original / replay

Evaluate the integral ${\int }_{0}^{\infty }\frac{x}{\sqrt{({x}^{2}+1)^{3}}}\,\text{d}x.$

First, we substitute $u={x}^{2}+1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\frac{1}{2}\text{d}u=x\,\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u={x}^{2}+1$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $1$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{x}{\sqrt{({x}^{2}+1)^{3}}}\,\text{d}x & =\frac{1}{2}{\int }_{1}^{\infty }\frac{1}{\sqrt{{u}^{3}}}\,\text{d}u.\end{aligned}
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{x}{\sqrt{{x}^{2}+1}}\,\text{d}x & =\frac{1}{2}{\int }_{1}^{\infty }\frac{1}{\sqrt{{u}^{3}}}\,\text{d}u \\  & =\frac{1}{2}{\int }_{1}^{\infty }{u}^{-3/2}\,\text{d}u \\  & =\frac{1}{2}{lim}_{a\to \infty }{\int }_{1}^{a}{u}^{-3/2}\,\text{d}u \\  & =\frac{1}{2}{lim}_{a\to \infty }{[-2{u}^{-1/2}]}_{1}^{a} \\  & =-{lim}_{a\to \infty }{[\frac{1}{\sqrt{u}}]}_{1}^{a} \\  & =-{lim}_{a\to \infty }(\frac{1}{\sqrt{a}}-1) \\  & =-(0-1) \\  & =1.\end{aligned}
$$

### Coefficient variant (scale 7)

Evaluate the integral ${\int }_{0}^{\infty }\frac{7 x}{\sqrt{(x^{2} + 1)^{3}}}\,\text{d}x.$

First, we substitute $u=x^{2} + 1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=2 x\quad\Longrightarrow\quad\text{d}u=2 x\,\text{d}x.
$$

Since $u\to \infty$ when $x\to \infty,$ the table for the limits of integration using the rule $u=x^{2} + 1$ is as follows:

| $x$ | $0$ | $\infty$ |
| --- | --- | --- |
| $u$ | $1$ | $\infty$ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{7 x}{\sqrt{(x^{2} + 1)^{3}}}\,\text{d}x=\frac{7}{2}\int_{1}^{\infty}u^{-\frac{3}{2}}\,\text{d}u.
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to\infty.$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{7 x}{\sqrt{(x^{2} + 1)^{3}}}\,\text{d}x & =\frac{7}{2}\lim_{a\to\infty}\int_{1}^{a}u^{-\frac{3}{2}}\,\text{d}u \\ & =\lim_{a\to\infty}\left[-7u^{- \frac{1}{2}}\right]_{1}^{a} \\ & =-7\lim_{a\to\infty}\left(a^{- \frac{1}{2}}-1\right) \\ & =-7\left(0-1\right) \\ & =7.\end{aligned}
$$

---

## q-152045 original / replay

Evaluate ${\int }_{0}^{\infty }\frac{3}{\sqrt{(2x+4)^{3}}}\,\text{d}x.$

First, we substitute $u=2x+4.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=2\,⟹\,\frac{1}{2}\,\text{d}u=\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u=2x+4$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $4$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{3}{\sqrt{(2x+4)^{3}}}\,\text{d}x & ={\int }_{4}^{\infty }\frac{3}{\sqrt{{u}^{3}}}(\frac{1}{2}\,\text{d}u) \\  & =\frac{3}{2}{\int }_{4}^{\infty }\frac{1}{\sqrt{{u}^{3}}}\,\text{d}u\end{aligned}
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{3}{\sqrt{(2x+4)^{3}}}\,\text{d}x & =\frac{3}{2}{\int }_{4}^{\infty }\frac{1}{\sqrt{{u}^{3}}}\,\text{d}u \\  & =\frac{3}{2}{\int }_{4}^{\infty }{u}^{-3/2}\,\text{d}u \\  & =\frac{3}{2}{lim}_{a\to \infty }{\int }_{4}^{a}{u}^{-3/2}\,\text{d}u \\  & =\frac{3}{2}{lim}_{a\to \infty }{[-2{u}^{-1/2}]}_{4}^{a} \\  & =-3\cdot {lim}_{a\to \infty }{[\frac{1}{\sqrt{u}}]}_{4}^{a} \\  & =-3\cdot {lim}_{a\to \infty }[\frac{1}{\sqrt{a}}-\frac{1}{\sqrt{4}}] \\  & =-3\cdot (0-\frac{1}{2}) \\  & =\frac{3}{2}.\end{aligned}
$$

### Coefficient variant (scale 7)

Evaluate the integral ${\int }_{0}^{\infty }\frac{21}{\sqrt{(2 x + 4)^{3}}}\,\text{d}x.$

First, we substitute $u=2 x + 4.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=2\quad\Longrightarrow\quad\text{d}u=2\,\text{d}x.
$$

Since $u\to \infty$ when $x\to \infty,$ the table for the limits of integration using the rule $u=2 x + 4$ is as follows:

| $x$ | $0$ | $\infty$ |
| --- | --- | --- |
| $u$ | $4$ | $\infty$ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{21}{\sqrt{(2 x + 4)^{3}}}\,\text{d}x=\frac{21}{2}\int_{4}^{\infty}u^{-\frac{3}{2}}\,\text{d}u.
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to\infty.$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{21}{\sqrt{(2 x + 4)^{3}}}\,\text{d}x & =\frac{21}{2}\lim_{a\to\infty}\int_{4}^{a}u^{-\frac{3}{2}}\,\text{d}u \\ & =\lim_{a\to\infty}\left[-21u^{- \frac{1}{2}}\right]_{4}^{a} \\ & =-21\lim_{a\to\infty}\left(a^{- \frac{1}{2}}-\frac{1}{2}\right) \\ & =-21\left(0-\frac{1}{2}\right) \\ & =\frac{21}{2}.\end{aligned}
$$

---

## q-152056 original / replay

Evaluate the integral ${\int }_{0}^{\infty }\frac{{x}^{2}}{\sqrt{({x}^{3}+1)^{5}}}\,\text{d}x.$

First, we substitute $u={x}^{3}+1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=3{x}^{2}\,⟹\,\frac{1}{3}\text{d}u={x}^{2}\,\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u={x}^{3}+1$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $1$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{{x}^{2}}{\sqrt{({x}^{3}+1)^{5}}}\,\text{d}x & =\frac{1}{3}{\int }_{1}^{\infty }\frac{1}{\sqrt{{u}^{5}}}\,\text{d}u.\end{aligned}
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{x}{\sqrt{{x}^{3}+1}}\,\text{d}x & =\frac{1}{3}{\int }_{1}^{\infty }\frac{1}{\sqrt{{u}^{5}}}\,\text{d}u \\  & =\frac{1}{3}{\int }_{1}^{\infty }{u}^{-5/2}\,\text{d}u \\  & =\frac{1}{3}{lim}_{a\to \infty }{\int }_{1}^{a}{u}^{-5/2}\,\text{d}u \\  & =\frac{1}{3}{lim}_{a\to \infty }{[-\frac{2}{3}{u}^{-3/2}]}_{1}^{a} \\  & =-\frac{2}{9}{lim}_{a\to \infty }{[\frac{1}{\sqrt{{u}^{3}}}]}_{1}^{a} \\  & =-\frac{2}{9}{lim}_{a\to \infty }(\frac{1}{\sqrt{{a}^{3}}}-1) \\  & =-\frac{2}{9}(0-1) \\  & =\frac{2}{9}.\end{aligned}
$$

### Coefficient variant (scale 7)

Evaluate the integral ${\int }_{0}^{\infty }\frac{7 x^{2}}{\sqrt{(x^{3} + 1)^{5}}}\,\text{d}x.$

First, we substitute $u=x^{3} + 1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=3 x^{2}\quad\Longrightarrow\quad\text{d}u=3 x^{2}\,\text{d}x.
$$

Since $u\to \infty$ when $x\to \infty,$ the table for the limits of integration using the rule $u=x^{3} + 1$ is as follows:

| $x$ | $0$ | $\infty$ |
| --- | --- | --- |
| $u$ | $1$ | $\infty$ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{7 x^{2}}{\sqrt{(x^{3} + 1)^{5}}}\,\text{d}x=\frac{7}{3}\int_{1}^{\infty}u^{-\frac{5}{2}}\,\text{d}u.
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to\infty.$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{7 x^{2}}{\sqrt{(x^{3} + 1)^{5}}}\,\text{d}x & =\frac{7}{3}\lim_{a\to\infty}\int_{1}^{a}u^{-\frac{5}{2}}\,\text{d}u \\ & =\lim_{a\to\infty}\left[- \frac{14}{9}u^{- \frac{3}{2}}\right]_{1}^{a} \\ & =- \frac{14}{9}\lim_{a\to\infty}\left(a^{- \frac{3}{2}}-1\right) \\ & =- \frac{14}{9}\left(0-1\right) \\ & =\frac{14}{9}.\end{aligned}
$$

---

## q-152779 original / replay

Evaluate ${\int }_{-1}^{\infty }\frac{6}{(z+2)^{4}}\,\text{d}z.$

First, we substitute $u=z+2.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}z}=1\,⟹\,\text{d}u=\text{d}z.
$$

Since $u\to \infty $ when $z\to \infty ,$ the table for the limits of integration using the rule $u=z+2$ is as follows:

| $z$ | $-1$ | $\infty $ |
| --- | --- | --- |
| $u$ | $1$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{-1}^{\infty }\frac{6}{(z+2)^{4}}\,\text{d}z={\int }_{1}^{\infty }\frac{6}{{u}^{4}}\,\text{d}u
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{-1}^{\infty }\frac{6}{(z+2)^{4}}\,\text{d}z & ={\int }_{1}^{\infty }\frac{6}{{u}^{4}}\,\text{d}u \\  & =6{\int }_{1}^{\infty }{u}^{-4}\,\text{d}u \\  & =6{lim}_{a\to \infty }{\int }_{1}^{a}{u}^{-4}\,\text{d}u \\  & =6{lim}_{a\to \infty }{[-\frac{1}{3}{u}^{-3}]}_{1}^{a} \\  & =-2\cdot {lim}_{a\to \infty }{[\frac{1}{{u}^{3}}]}_{1}^{a} \\  & =-2\cdot {lim}_{a\to \infty }[\frac{1}{{a}^{3}}-\frac{1}{{1}^{3}}] \\  & =-2\cdot (0-1) \\  & =2.\end{aligned}
$$

### Coefficient variant (scale 7)

Evaluate the integral ${\int }_{-1}^{\infty }\frac{42}{(z + 2)^{4}}\,\text{d}z.$

First, we substitute $u=z + 2.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}z}=1\quad\Longrightarrow\quad\text{d}u=1\,\text{d}z.
$$

Since $u\to \infty$ when $z\to \infty,$ the table for the limits of integration using the rule $u=z + 2$ is as follows:

| $z$ | $-1$ | $\infty$ |
| --- | --- | --- |
| $u$ | $1$ | $\infty$ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{-1}^{\infty }\frac{42}{(z + 2)^{4}}\,\text{d}z=42\int_{1}^{\infty}u^{-4}\,\text{d}u.
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to\infty.$

$$
\begin{aligned}{\int }_{-1}^{\infty }\frac{42}{(z + 2)^{4}}\,\text{d}z & =42\lim_{a\to\infty}\int_{1}^{a}u^{-4}\,\text{d}u \\ & =\lim_{a\to\infty}\left[-14u^{-3}\right]_{1}^{a} \\ & =-14\lim_{a\to\infty}\left(a^{-3}-1\right) \\ & =-14\left(0-1\right) \\ & =14.\end{aligned}
$$

---

## q-152785 original / replay

Evaluate the integral ${\int }_{1}^{\infty }\frac{8{z}^{3}}{{({z}^{4}+1)}^{4}}\,\text{d}z.$

First, we substitute $u={z}^{4}+1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}z}=4{z}^{3}\,⟹\,\frac{1}{4}\text{d}u={z}^{3}\,\text{d}z.
$$

Since $u\to \infty $ when $z\to \infty ,$ the table for the limits of integration using the rule $u={z}^{4}+1$ is as follows:

| $z$ | $1$ | $\infty $ |
| --- | --- | --- |
| $u$ | $2$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
\begin{aligned}{\int }_{1}^{\infty }\frac{8{z}^{3}}{{({z}^{4}+1)}^{4}}\,\text{d}z & ={\int }_{2}^{\infty }\frac{8}{{u}^{4}}(\frac{1}{4}\,\text{d}u) \\  & =2{\int }_{2}^{\infty }\frac{1}{{u}^{4}}\,\text{d}u.\end{aligned}
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{1}^{\infty }\frac{8{z}^{3}}{{({z}^{4}+1)}^{4}}\,\text{d}z & =2{\int }_{2}^{\infty }\frac{1}{{u}^{4}}\,\text{d}u \\  & =2{\int }_{2}^{\infty }{u}^{-4}\,\text{d}u \\  & =2{lim}_{a\to \infty }{\int }_{2}^{a}{u}^{-4}\,\text{d}u \\  & =2{lim}_{a\to \infty }{[-\frac{1}{3}{u}^{-3}]}_{2}^{a} \\  & =-\frac{2}{3}{lim}_{a\to \infty }{[\frac{1}{{u}^{3}}]}_{2}^{a} \\  & =-\frac{2}{3}{lim}_{a\to \infty }(\frac{1}{{a}^{3}}-\frac{1}{8}) \\  & =-\frac{2}{3}(0-\frac{1}{8}) \\  & =\frac{1}{12}.\end{aligned}
$$

### Coefficient variant (scale 7)

Evaluate the integral ${\int }_{1}^{\infty }\frac{56 z^{3}}{(z^{4} + 1)^{4}}\,\text{d}z.$

First, we substitute $u=z^{4} + 1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}z}=4 z^{3}\quad\Longrightarrow\quad\text{d}u=4 z^{3}\,\text{d}z.
$$

Since $u\to \infty$ when $z\to \infty,$ the table for the limits of integration using the rule $u=z^{4} + 1$ is as follows:

| $z$ | $1$ | $\infty$ |
| --- | --- | --- |
| $u$ | $2$ | $\infty$ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{1}^{\infty }\frac{56 z^{3}}{(z^{4} + 1)^{4}}\,\text{d}z=14\int_{2}^{\infty}u^{-4}\,\text{d}u.
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to\infty.$

$$
\begin{aligned}{\int }_{1}^{\infty }\frac{56 z^{3}}{(z^{4} + 1)^{4}}\,\text{d}z & =14\lim_{a\to\infty}\int_{2}^{a}u^{-4}\,\text{d}u \\ & =\lim_{a\to\infty}\left[- \frac{14}{3}u^{-3}\right]_{2}^{a} \\ & =- \frac{14}{3}\lim_{a\to\infty}\left(a^{-3}-\frac{1}{8}\right) \\ & =- \frac{14}{3}\left(0-\frac{1}{8}\right) \\ & =\frac{7}{12}.\end{aligned}
$$

---

## q-350527 original / replay

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{3}{(x+1)^{5}}\,\text{d}x=$
{{field-1}}

First, we substitute $u=x+1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=1\,⟹\,\text{d}u=\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u=x+1$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $1$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{3}{(x+1)^{5}}\,\text{d}x={\int }_{1}^{\infty }\frac{3}{{u}^{5}}\,\text{d}u
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{3}{(x+1)^{5}}\,\text{d}x & ={\int }_{1}^{\infty }\frac{3}{{u}^{5}}\,\text{d}u \\  & ={\int }_{1}^{\infty }3{u}^{-5}\,\text{d}u \\  & ={lim}_{a\to \infty }{\int }_{1}^{a}3{u}^{-5}\,\text{d}u \\  & ={lim}_{a\to \infty }{[-\frac{3}{4}{u}^{-4}]}_{1}^{a} \\  & =-\frac{3}{4}\cdot {lim}_{a\to \infty }{[{u}^{-4}]}_{1}^{a} \\  & =-\frac{3}{4}\cdot {lim}_{a\to \infty }[\frac{1}{{a}^{4}}-\frac{1}{{1}^{4}}] \\  & =-\frac{3}{4}\cdot (0-1) \\  & =\frac{3}{4}.\end{aligned}
$$

### Coefficient variant (scale 7)

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{21}{(x + 1)^{5}}\,\text{d}x=$
{{field-1}}

First, we substitute $u=x + 1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=1\quad\Longrightarrow\quad\text{d}u=1\,\text{d}x.
$$

Since $u\to \infty$ when $x\to \infty,$ the table for the limits of integration using the rule $u=x + 1$ is as follows:

| $x$ | $0$ | $\infty$ |
| --- | --- | --- |
| $u$ | $1$ | $\infty$ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{21}{(x + 1)^{5}}\,\text{d}x=21\int_{1}^{\infty}u^{-5}\,\text{d}u.
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to\infty.$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{21}{(x + 1)^{5}}\,\text{d}x & =21\lim_{a\to\infty}\int_{1}^{a}u^{-5}\,\text{d}u \\ & =\lim_{a\to\infty}\left[- \frac{21}{4}u^{-4}\right]_{1}^{a} \\ & =- \frac{21}{4}\lim_{a\to\infty}\left(a^{-4}-1\right) \\ & =- \frac{21}{4}\left(0-1\right) \\ & =\frac{21}{4}.\end{aligned}
$$

---

## q-350528 original / replay

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{2}{\sqrt{(x+3)^{8}}}\,\text{d}x=$
{{field-1}}

First, we substitute $u=x+3.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=1\,⟹\,\text{d}u=\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u=x+3$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $3$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{2}{\sqrt{(x+3)^{8}}}\,\text{d}x={\int }_{3}^{\infty }\frac{2}{\sqrt{{u}^{8}}}\,\text{d}u
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{2}{\sqrt{(x+3)^{8}}}\,\text{d}x & ={\int }_{3}^{\infty }\frac{2}{\sqrt{{u}^{8}}}\,\text{d}u \\  & ={\int }_{3}^{\infty }2{u}^{-4}\,\text{d}u \\  & ={lim}_{a\to \infty }{\int }_{3}^{a}2{u}^{-4}\,\text{d}u \\  & ={lim}_{a\to \infty }{[-\frac{2}{3}{u}^{-3}]}_{3}^{a} \\  & =-\frac{2}{3}\cdot {lim}_{a\to \infty }{[{u}^{-3}]}_{3}^{a} \\  & =-\frac{2}{3}\cdot {lim}_{a\to \infty }[\frac{1}{{a}^{3}}-\frac{1}{{3}^{3}}] \\  & =-\frac{2}{3}\cdot (0-\frac{1}{27}) \\  & =\frac{2}{81}.\end{aligned}
$$

### Coefficient variant (scale 7)

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{14}{\sqrt{(x + 3)^{8}}}\,\text{d}x=$
{{field-1}}

First, we substitute $u=x + 3.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=1\quad\Longrightarrow\quad\text{d}u=1\,\text{d}x.
$$

Since $u\to \infty$ when $x\to \infty,$ the table for the limits of integration using the rule $u=x + 3$ is as follows:

| $x$ | $0$ | $\infty$ |
| --- | --- | --- |
| $u$ | $3$ | $\infty$ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{14}{\sqrt{(x + 3)^{8}}}\,\text{d}x=14\int_{3}^{\infty}u^{-4}\,\text{d}u.
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to\infty.$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{14}{\sqrt{(x + 3)^{8}}}\,\text{d}x & =14\lim_{a\to\infty}\int_{3}^{a}u^{-4}\,\text{d}u \\ & =\lim_{a\to\infty}\left[- \frac{14}{3}u^{-3}\right]_{3}^{a} \\ & =- \frac{14}{3}\lim_{a\to\infty}\left(a^{-3}-\frac{1}{27}\right) \\ & =- \frac{14}{3}\left(0-\frac{1}{27}\right) \\ & =\frac{14}{81}.\end{aligned}
$$

---

## q-350530 original / replay

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{5}{(3y+2)^{4}}\,\text{d}y=$
{{field-1}}

First, we substitute $u=3y+2.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}y}=3\,⟹\,\text{d}u=3\text{d}y.
$$

Since $u\to \infty $ when $y\to \infty ,$ the table for the limits of integration using the rule $u=3y+2$ is as follows:

| $y$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $2$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{5}{(3y+2)^{4}}\,\text{d}y={\int }_{2}^{\infty }\frac{5}{3{u}^{4}}\,\text{d}u
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{5}{(3y+2)^{4}}\,\text{d}y & ={\int }_{2}^{\infty }\frac{5}{3{u}^{4}}\,\text{d}u \\  & ={\int }_{2}^{\infty }\frac{5}{3}{u}^{-4}\,\text{d}u \\  & ={lim}_{a\to \infty }{\int }_{2}^{a}\frac{5}{3}{u}^{-4}\,\text{d}u \\  & ={lim}_{a\to \infty }{[-\frac{5}{9}{u}^{-3}]}_{2}^{a} \\  & =-\frac{5}{9}\cdot {lim}_{a\to \infty }{[{u}^{-3}]}_{2}^{a} \\  & =-\frac{5}{9}\cdot {lim}_{a\to \infty }[\frac{1}{{a}^{3}}-\frac{1}{{2}^{3}}] \\  & =-\frac{5}{9}\cdot (0-\frac{1}{8}) \\  & =\frac{5}{72}.\end{aligned}
$$

### Coefficient variant (scale 7)

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{35}{(3 y + 2)^{4}}\,\text{d}y=$
{{field-1}}

First, we substitute $u=3 y + 2.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}y}=3\quad\Longrightarrow\quad\text{d}u=3\,\text{d}y.
$$

Since $u\to \infty$ when $y\to \infty,$ the table for the limits of integration using the rule $u=3 y + 2$ is as follows:

| $y$ | $0$ | $\infty$ |
| --- | --- | --- |
| $u$ | $2$ | $\infty$ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{35}{(3 y + 2)^{4}}\,\text{d}y=\frac{35}{3}\int_{2}^{\infty}u^{-4}\,\text{d}u.
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to\infty.$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{35}{(3 y + 2)^{4}}\,\text{d}y & =\frac{35}{3}\lim_{a\to\infty}\int_{2}^{a}u^{-4}\,\text{d}u \\ & =\lim_{a\to\infty}\left[- \frac{35}{9}u^{-3}\right]_{2}^{a} \\ & =- \frac{35}{9}\lim_{a\to\infty}\left(a^{-3}-\frac{1}{8}\right) \\ & =- \frac{35}{9}\left(0-\frac{1}{8}\right) \\ & =\frac{35}{72}.\end{aligned}
$$

---

## q-350531 original / replay

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{6}{\sqrt{(4t+3)^{3}}}\,\text{d}t=$
{{field-1}}

First, we substitute $u=4t+3.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}t}=4\,⟹\,\text{d}u=4\text{d}t.
$$

Since $u\to \infty $ when $t\to \infty ,$ the table for the limits of integration using the rule $u=4t+3$ is as follows:

| $t$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $3$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{6}{\sqrt{(4t+3)^{3}}}\,\text{d}t={\int }_{3}^{\infty }\frac{3}{2\sqrt{{u}^{3}}}\,\text{d}u
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{6}{\sqrt{(4t+3)^{3}}}\,\text{d}t & ={\int }_{3}^{\infty }\frac{3}{2\sqrt{{u}^{3}}}\,\text{d}u \\  & ={\int }_{3}^{\infty }\frac{3}{2}{u}^{-3/2}\,\text{d}u \\  & ={lim}_{a\to \infty }{\int }_{3}^{a}\frac{3}{2}{u}^{-3/2}\,\text{d}u \\  & ={lim}_{a\to \infty }{[-3{u}^{-1/2}]}_{3}^{a} \\  & =-3\cdot {lim}_{a\to \infty }{[{u}^{-1/2}]}_{3}^{a} \\  & =-3\cdot {lim}_{a\to \infty }[\frac{1}{\sqrt{a}}-\frac{1}{\sqrt{3}}] \\  & =-3\cdot (0-\frac{1}{\sqrt{3}}) \\  & =\sqrt{3}.\end{aligned}
$$

### Coefficient variant (scale 7)

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{42}{\sqrt{(4 t + 3)^{3}}}\,\text{d}t=$
{{field-1}}

First, we substitute $u=4 t + 3.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}t}=4\quad\Longrightarrow\quad\text{d}u=4\,\text{d}t.
$$

Since $u\to \infty$ when $t\to \infty,$ the table for the limits of integration using the rule $u=4 t + 3$ is as follows:

| $t$ | $0$ | $\infty$ |
| --- | --- | --- |
| $u$ | $3$ | $\infty$ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{42}{\sqrt{(4 t + 3)^{3}}}\,\text{d}t=\frac{21}{2}\int_{3}^{\infty}u^{-\frac{3}{2}}\,\text{d}u.
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to\infty.$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{42}{\sqrt{(4 t + 3)^{3}}}\,\text{d}t & =\frac{21}{2}\lim_{a\to\infty}\int_{3}^{a}u^{-\frac{3}{2}}\,\text{d}u \\ & =\lim_{a\to\infty}\left[-21u^{- \frac{1}{2}}\right]_{3}^{a} \\ & =-21\lim_{a\to\infty}\left(a^{- \frac{1}{2}}-\frac{\sqrt{3}}{3}\right) \\ & =-21\left(0-\frac{\sqrt{3}}{3}\right) \\ & =7 \sqrt{3}.\end{aligned}
$$

---

## q-350532 original / replay

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{2}{(5\theta +1)^{3}}\,\text{d}\theta =$
{{field-1}}

First, we substitute $u=5\theta +1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}\theta }=5\,⟹\,\text{d}u=5\text{d}\theta .
$$

Since $u\to \infty $ when $\theta \to \infty ,$ the table for the limits of integration using the rule $u=5\theta +1$ is as follows:

| $\theta $ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $1$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{2}{(5\theta +1)^{3}}\,\text{d}\theta ={\int }_{1}^{\infty }\frac{2}{5{u}^{3}}\,\text{d}u
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{2}{(5\theta +1)^{3}}\,\text{d}\theta  & ={\int }_{1}^{\infty }\frac{2}{5{u}^{3}}\,\text{d}u \\  & ={\int }_{1}^{\infty }\frac{2}{5}{u}^{-3}\,\text{d}u \\  & ={lim}_{a\to \infty }{\int }_{1}^{a}\frac{2}{5}{u}^{-3}\,\text{d}u \\  & ={lim}_{a\to \infty }{[-\frac{1}{5}{u}^{-2}]}_{1}^{a} \\  & =-\frac{1}{5}\cdot {lim}_{a\to \infty }{[{u}^{-2}]}_{1}^{a} \\  & =-\frac{1}{5}\cdot {lim}_{a\to \infty }[\frac{1}{{a}^{2}}-\frac{1}{{1}^{2}}] \\  & =-\frac{1}{5}\cdot (0-1) \\  & =\frac{1}{5}.\end{aligned}
$$

### Coefficient variant (scale 7)

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{14}{(5 \theta + 1)^{3}}\,\text{d}\theta=$
{{field-1}}

First, we substitute $u=5 \theta + 1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}\theta}=5\quad\Longrightarrow\quad\text{d}u=5\,\text{d}\theta.
$$

Since $u\to \infty$ when $\theta\to \infty,$ the table for the limits of integration using the rule $u=5 \theta + 1$ is as follows:

| $\theta$ | $0$ | $\infty$ |
| --- | --- | --- |
| $u$ | $1$ | $\infty$ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{14}{(5 \theta + 1)^{3}}\,\text{d}\theta=\frac{14}{5}\int_{1}^{\infty}u^{-3}\,\text{d}u.
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to\infty.$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{14}{(5 \theta + 1)^{3}}\,\text{d}\theta & =\frac{14}{5}\lim_{a\to\infty}\int_{1}^{a}u^{-3}\,\text{d}u \\ & =\lim_{a\to\infty}\left[- \frac{7}{5}u^{-2}\right]_{1}^{a} \\ & =- \frac{7}{5}\lim_{a\to\infty}\left(a^{-2}-1\right) \\ & =- \frac{7}{5}\left(0-1\right) \\ & =\frac{7}{5}.\end{aligned}
$$

---

## q-350534 original / replay

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{4{x}^{3}}{\sqrt{({x}^{4}+2)^{3}}}\,\text{d}x=$
{{field-1}}

First, we substitute $u={x}^{4}+2.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=4{x}^{3}\,⟹\,\text{d}u=4{x}^{3}\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u={x}^{4}+2$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $2$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{4{x}^{3}}{\sqrt{({x}^{4}+2)^{3}}}\,\text{d}x={\int }_{2}^{\infty }\frac{1}{\sqrt{{u}^{3}}}\,\text{d}u
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{4{x}^{3}}{\sqrt{({x}^{4}+2)^{3}}}\,\text{d}x & ={\int }_{2}^{\infty }\frac{1}{\sqrt{{u}^{3}}}\,\text{d}u \\  & ={\int }_{2}^{\infty }{u}^{-3/2}\,\text{d}u \\  & ={lim}_{a\to \infty }{\int }_{2}^{a}{u}^{-3/2}\,\text{d}u \\  & ={lim}_{a\to \infty }{[-2{u}^{-1/2}]}_{2}^{a} \\  & =-2\cdot {lim}_{a\to \infty }{[{u}^{-1/2}]}_{2}^{a} \\  & =-2\cdot {lim}_{a\to \infty }[\frac{1}{{a}^{1/2}}-\frac{1}{{2}^{1/2}}] \\  & =-2\cdot (0-\frac{1}{\sqrt{2}}) \\  & =\sqrt{2}.\end{aligned}
$$

### Coefficient variant (scale 7)

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{28 x^{3}}{\sqrt{(x^{4} + 2)^{3}}}\,\text{d}x=$
{{field-1}}

First, we substitute $u=x^{4} + 2.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=4 x^{3}\quad\Longrightarrow\quad\text{d}u=4 x^{3}\,\text{d}x.
$$

Since $u\to \infty$ when $x\to \infty,$ the table for the limits of integration using the rule $u=x^{4} + 2$ is as follows:

| $x$ | $0$ | $\infty$ |
| --- | --- | --- |
| $u$ | $2$ | $\infty$ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{28 x^{3}}{\sqrt{(x^{4} + 2)^{3}}}\,\text{d}x=7\int_{2}^{\infty}u^{-\frac{3}{2}}\,\text{d}u.
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to\infty.$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{28 x^{3}}{\sqrt{(x^{4} + 2)^{3}}}\,\text{d}x & =7\lim_{a\to\infty}\int_{2}^{a}u^{-\frac{3}{2}}\,\text{d}u \\ & =\lim_{a\to\infty}\left[-14u^{- \frac{1}{2}}\right]_{2}^{a} \\ & =-14\lim_{a\to\infty}\left(a^{- \frac{1}{2}}-\frac{\sqrt{2}}{2}\right) \\ & =-14\left(0-\frac{\sqrt{2}}{2}\right) \\ & =7 \sqrt{2}.\end{aligned}
$$

---

## q-152053 original / replay

Evaluate the integral ${\int }_{0}^{\infty }\frac{{x}^{2}}{{(1+{x}^{3})}^{4}}\,\text{d}x.$

First, we substitute $u=1+{x}^{3}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=3{x}^{2}\,⟹\,\frac{1}{3}\text{d}u={x}^{2}\,\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u=1+{x}^{3}$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $1$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{{x}^{2}}{{(1+{x}^{3})}^{4}}\,\text{d}x & =\frac{1}{3}{\int }_{1}^{\infty }\frac{1}{{u}^{4}}\,\text{d}u.\end{aligned}
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{{x}^{2}}{{(1+{x}^{3})}^{4}}\,\text{d}x & =\frac{1}{3}{\int }_{1}^{\infty }\frac{1}{{u}^{4}}\,\text{d}u \\  & =\frac{1}{3}{\int }_{1}^{\infty }{u}^{-4}\,\text{d}u \\  & =\frac{1}{3}{lim}_{a\to \infty }{\int }_{1}^{a}{u}^{-4}\,\text{d}u \\  & =\frac{1}{3}{lim}_{a\to \infty }{[-\frac{1}{3}{u}^{-3}]}_{1}^{a} \\  & =-\frac{1}{9}{lim}_{a\to \infty }{[\frac{1}{{u}^{3}}]}_{1}^{a} \\  & =-\frac{1}{9}{lim}_{a\to \infty }(\frac{1}{{a}^{3}}-1) \\  & =-\frac{1}{9}(0-1) \\  & =\frac{1}{9}.\end{aligned}
$$

### Coefficient variant (scale 7)

Evaluate the integral ${\int }_{0}^{\infty }\frac{7 x^{2}}{(x^{3} + 1)^{4}}\,\text{d}x.$

First, we substitute $u=x^{3} + 1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=3 x^{2}\quad\Longrightarrow\quad\text{d}u=3 x^{2}\,\text{d}x.
$$

Since $u\to \infty$ when $x\to \infty,$ the table for the limits of integration using the rule $u=x^{3} + 1$ is as follows:

| $x$ | $0$ | $\infty$ |
| --- | --- | --- |
| $u$ | $1$ | $\infty$ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{7 x^{2}}{(x^{3} + 1)^{4}}\,\text{d}x=\frac{7}{3}\int_{1}^{\infty}u^{-4}\,\text{d}u.
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to\infty.$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{7 x^{2}}{(x^{3} + 1)^{4}}\,\text{d}x & =\frac{7}{3}\lim_{a\to\infty}\int_{1}^{a}u^{-4}\,\text{d}u \\ & =\lim_{a\to\infty}\left[- \frac{7}{9}u^{-3}\right]_{1}^{a} \\ & =- \frac{7}{9}\lim_{a\to\infty}\left(a^{-3}-1\right) \\ & =- \frac{7}{9}\left(0-1\right) \\ & =\frac{7}{9}.\end{aligned}
$$

---

## q-346591 original / replay

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{1}{\sqrt{(x+1)^{9}}}\,\text{d}x=$
{{field-1}}

First, we substitute $u=x+1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=1\,⟹\,\text{d}u=\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u=x+1$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $1$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{1}{\sqrt{(x+1)^{9}}}\,\text{d}x={\int }_{1}^{\infty }\frac{1}{\sqrt{{u}^{9}}}\,\text{d}u
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{1}{\sqrt{(x+1)^{9}}}\,\text{d}x & ={\int }_{1}^{\infty }\frac{1}{\sqrt{{u}^{9}}}\,\text{d}u \\  & ={\int }_{1}^{\infty }{u}^{-9/2}\,\text{d}u \\  & ={lim}_{a\to \infty }{\int }_{1}^{a}{u}^{-9/2}\,\text{d}u \\  & ={lim}_{a\to \infty }{[-\frac{2}{7}{u}^{-7/2}]}_{1}^{a} \\  & =-\frac{2}{7}\cdot {lim}_{a\to \infty }{[{u}^{-7/2}]}_{1}^{a} \\  & =-\frac{2}{7}\cdot {lim}_{a\to \infty }[\frac{1}{{a}^{7/2}}-\frac{1}{{1}^{7/2}}] \\  & =-\frac{2}{7}\cdot (0-1) \\  & =\frac{2}{7}.\end{aligned}
$$

### Coefficient variant (scale 7)

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{7}{\sqrt{(x + 1)^{9}}}\,\text{d}x=$
{{field-1}}

First, we substitute $u=x + 1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=1\quad\Longrightarrow\quad\text{d}u=1\,\text{d}x.
$$

Since $u\to \infty$ when $x\to \infty,$ the table for the limits of integration using the rule $u=x + 1$ is as follows:

| $x$ | $0$ | $\infty$ |
| --- | --- | --- |
| $u$ | $1$ | $\infty$ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{7}{\sqrt{(x + 1)^{9}}}\,\text{d}x=7\int_{1}^{\infty}u^{-\frac{9}{2}}\,\text{d}u.
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to\infty.$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{7}{\sqrt{(x + 1)^{9}}}\,\text{d}x & =7\lim_{a\to\infty}\int_{1}^{a}u^{-\frac{9}{2}}\,\text{d}u \\ & =\lim_{a\to\infty}\left[-2u^{- \frac{7}{2}}\right]_{1}^{a} \\ & =-2\lim_{a\to\infty}\left(a^{- \frac{7}{2}}-1\right) \\ & =-2\left(0-1\right) \\ & =2.\end{aligned}
$$

---

## q-350533 original / replay

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{3{x}^{2}}{\sqrt{({x}^{3}+1)^{3}}}\,\text{d}x=$
{{field-1}}

First, we substitute $u={x}^{3}+1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=3{x}^{2}\,⟹\,\text{d}u=3{x}^{2}\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u={x}^{3}+1$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $1$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{3{x}^{2}}{\sqrt{({x}^{3}+1)^{3}}}\,\text{d}x={\int }_{1}^{\infty }\frac{1}{\sqrt{{u}^{3}}}\,\text{d}u
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{3{x}^{2}}{\sqrt{({x}^{3}+1)^{3}}}\,\text{d}x & ={\int }_{1}^{\infty }\frac{1}{\sqrt{{u}^{3}}}\,\text{d}u \\  & ={\int }_{1}^{\infty }{u}^{-3/2}\,\text{d}u \\  & ={lim}_{a\to \infty }{\int }_{1}^{a}{u}^{-3/2}\,\text{d}u \\  & ={lim}_{a\to \infty }{[-2{u}^{-1/2}]}_{1}^{a} \\  & =-2\cdot {lim}_{a\to \infty }{[{u}^{-1/2}]}_{1}^{a} \\  & =-2\cdot {lim}_{a\to \infty }[\frac{1}{{a}^{1/2}}-\frac{1}{{1}^{1/2}}] \\  & =-2\cdot (0-1) \\  & =2.\end{aligned}
$$

### Coefficient variant (scale 7)

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{21 x^{2}}{\sqrt{(x^{3} + 1)^{3}}}\,\text{d}x=$
{{field-1}}

First, we substitute $u=x^{3} + 1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=3 x^{2}\quad\Longrightarrow\quad\text{d}u=3 x^{2}\,\text{d}x.
$$

Since $u\to \infty$ when $x\to \infty,$ the table for the limits of integration using the rule $u=x^{3} + 1$ is as follows:

| $x$ | $0$ | $\infty$ |
| --- | --- | --- |
| $u$ | $1$ | $\infty$ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{21 x^{2}}{\sqrt{(x^{3} + 1)^{3}}}\,\text{d}x=7\int_{1}^{\infty}u^{-\frac{3}{2}}\,\text{d}u.
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to\infty.$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{21 x^{2}}{\sqrt{(x^{3} + 1)^{3}}}\,\text{d}x & =7\lim_{a\to\infty}\int_{1}^{a}u^{-\frac{3}{2}}\,\text{d}u \\ & =\lim_{a\to\infty}\left[-14u^{- \frac{1}{2}}\right]_{1}^{a} \\ & =-14\lim_{a\to\infty}\left(a^{- \frac{1}{2}}-1\right) \\ & =-14\left(0-1\right) \\ & =14.\end{aligned}
$$

---

## q-350536 original / replay

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{10{x}^{4}}{\sqrt{({x}^{5}+1)^{9}}}\,\text{d}x=$
{{field-1}}

First, we substitute $u={x}^{5}+1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=5{x}^{4}\,⟹\,\text{d}u=5{x}^{4}\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u={x}^{5}+1$ is as follows:

| $x$ | $0$ | $\infty $ |
| --- | --- | --- |
| $u$ | $1$ | $\infty $ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{10{x}^{4}}{\sqrt{({x}^{5}+1)^{9}}}\,\text{d}x={\int }_{1}^{\infty }\frac{2}{\sqrt{{u}^{9}}}\,\text{d}u
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{10{x}^{4}}{\sqrt{({x}^{5}+1)^{9}}}\,\text{d}x & ={\int }_{1}^{\infty }\frac{2}{\sqrt{{u}^{9}}}\,\text{d}u \\  & ={\int }_{1}^{\infty }2{u}^{-9/2}\,\text{d}u \\  & ={lim}_{a\to \infty }{\int }_{1}^{a}2{u}^{-9/2}\,\text{d}u \\  & ={lim}_{a\to \infty }{[-\frac{4}{7}{u}^{-7/2}]}_{1}^{a} \\  & =-\frac{4}{7}\cdot {lim}_{a\to \infty }{[{u}^{-7/2}]}_{1}^{a} \\  & =-\frac{4}{7}\cdot {lim}_{a\to \infty }[\frac{1}{{a}^{7/2}}-\frac{1}{{1}^{7/2}}] \\  & =-\frac{4}{7}\cdot (0-1) \\  & =\frac{4}{7}.\end{aligned}
$$

### Coefficient variant (scale 7)

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\infty }\frac{70 x^{4}}{\sqrt{(x^{5} + 1)^{9}}}\,\text{d}x=$
{{field-1}}

First, we substitute $u=x^{5} + 1.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=5 x^{4}\quad\Longrightarrow\quad\text{d}u=5 x^{4}\,\text{d}x.
$$

Since $u\to \infty$ when $x\to \infty,$ the table for the limits of integration using the rule $u=x^{5} + 1$ is as follows:

| $x$ | $0$ | $\infty$ |
| --- | --- | --- |
| $u$ | $1$ | $\infty$ |

So, the integral in terms of the new variable $u$ is

$$
{\int }_{0}^{\infty }\frac{70 x^{4}}{\sqrt{(x^{5} + 1)^{9}}}\,\text{d}x=14\int_{1}^{\infty}u^{-\frac{9}{2}}\,\text{d}u.
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to\infty.$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{70 x^{4}}{\sqrt{(x^{5} + 1)^{9}}}\,\text{d}x & =14\lim_{a\to\infty}\int_{1}^{a}u^{-\frac{9}{2}}\,\text{d}u \\ & =\lim_{a\to\infty}\left[-4u^{- \frac{7}{2}}\right]_{1}^{a} \\ & =-4\lim_{a\to\infty}\left(a^{- \frac{7}{2}}-1\right) \\ & =-4\left(0-1\right) \\ & =4.\end{aligned}
$$