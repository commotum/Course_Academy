What is $\int (-1)\cdot {e}^{- \frac{x}{2}}\,\text{d}x$?

2 {e}^{- \frac{x}{2}}+C
- {e}^{- \frac{x}{2}}+C
\frac{{e}^{- \frac{x}{2}}}{2}+C
- 2 {e}^{- \frac{x}{2}}+C
2 {e}^{\frac{x}{2}}+C

If we let $u=- \frac{x}{2},$ then

$$
\frac{\text{d}u}{\text{d}x}=- \frac{1}{2}\quad\Longrightarrow\quad \text{d}x=(-2)\,\text{d}u.
$$

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int (-1)\cdot {e}^{- \frac{x}{2}}\,\text{d}x & =\int (-1)\cdot {e}^{u}\cdot (-2)\,\text{d}u \\  & =(2)\int {e}^{u}\,\text{d}u \\  & =(2){e}^{u}+C \\  & =2 {e}^{- \frac{x}{2}}+C\end{aligned}
$$

Calculate $\int {e}^{(x-3)/2\,-\,1}\,\text{d}x.$

2 {e}^{\frac{x}{2} - \frac{5}{2}}+C
{e}^{\frac{x}{2} - \frac{5}{2}}+C
- 2 {e}^{\frac{x}{2} - \frac{5}{2}}+C
\frac{{e}^{\frac{x}{2} - \frac{5}{2}}}{2}+C
2 {e}^{x - 4}+C

If we let $u=\frac{(x-3)}{2}-1,$ then

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{2}\,⟹\,2\,\text{d}u=\text{d}x.
$$

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int {e}^{(x-3)/2\,-\,1}\,\text{d}x & =\int {e}^{u}\cdot 2\,\text{d}u \\  & =2\int {e}^{u}\,\text{d}u \\  & =2\,{e}^{u}+C \\  & =2\,{e}^{(x-3)/2\,-\,1}+C\end{aligned}
$$

$\int {e}^{(z-3)}{e}^{(z-3)}\,\text{d}z=$

\frac{{e}^{2 z - 6}}{2}+C
- \frac{{e}^{(z - 3)^{2}}}{2}+C
2 {e}^{2 z - 6}+C
{e}^{2 z - 6}+C
\frac{{e}^{z - 3}}{2}+C

First, we notice that

$$
\int {e}^{(z-3)}{e}^{(z-3)}\,\text{d}z=\int {e}^{2(z-3)}\,\text{d}z.
$$

If we let $u=2(z-3)$, then

$$
\frac{\text{d}u}{\text{d}z}=2\,⟹\,\text{d}z=\frac{1}{2}\text{d}u.
$$

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int {e}^{2(z-3)}\,\text{d}z & =\int {e}^{2(u/2)}\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}\int {e}^{2(u/2)}\,\text{d}u \\  & =\frac{1}{2}\int {e}^{u}\,\text{d}u \\  & =\frac{1}{2}\cdot {e}^{u}+C \\  & =\frac{{e}^{2(z-3)}}{2}+C\end{aligned}\end{aligned}
$$

${\int }_{3}^{\ln{(3 )} + 3}5{e}^{-4(x-3)}\,\text{d}x=$

\frac{100}{81}
- \frac{205}{162}
- \frac{100}{81}
- \frac{5}{324}
- \frac{400}{81}

If we let $u=-4(x-3),$ then, 

$$
\frac{\text{d}u}{\text{d}x}=-4\,⟹\,-\frac{1}{4}\text{d}u=\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $3$ | $\ln{(3 )} + 3$ |
| --- | --- | --- |
| $u$ | $0$ | $-4\operatorname{ln}⁡3$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{3}^{\ln{(3 )} + 3}5{e}^{-4(x-3)}\,\text{d}x & =5{\int }_{3}^{\ln{(3 )} + 3}{e}^{-4(x-3)}\,\text{d}x \\  & =5{\int }_{0}^{-4\operatorname{ln}⁡3}{e}^{u}(-\frac{1}{4})\text{d}u \\  & =-\frac{5}{4}{\int }_{0}^{\operatorname{ln}⁡({3}^{-4})}{e}^{u}\text{d}u \\  & =-\frac{5}{4}({e}^{u}){|}_{0}^{\operatorname{ln}⁡({3}^{-4})} \\  & =-\frac{5}{4}({e}^{\operatorname{ln}⁡({3}^{-4})}-{e}^{0}) \\  & =-\frac{5}{4}({3}^{-4}-1) \\  & =-\frac{5}{4}(\frac{1}{{3}^{4}}-1) \\  & =-\frac{5}{4}(\frac{1}{81}-1) \\  & =-\frac{5}{4}(-\frac{80}{81}) \\  & =\frac{100}{81}\end{aligned}
$$

Evaluate the following integral. Give an exact answer.

$\int_{-2}^{1} (-4)\cdot {e}^{4 x + 2}\,\text{d}x=$  
{{field-1}}

- {e}^{6} + {e}^{-6}

If we let $u=4 x + 2,$ then

$$
\frac{\text{d}u}{\text{d}x}=4\quad\Longrightarrow\quad \text{d}x=(\frac{1}{4})\,\text{d}u.
$$

Computing our limits of integration, we get the following:

| $x$ | $-2$ | $1$ |
| --- | --- | --- |
| $u$ | $-6$ | $6$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{-2}^{1} (-4)\cdot {e}^{4 x + 2}\,\text{d}x & =(-4)\int_{-2}^{1} {e}^{4 x + 2}\,\text{d}x \\  & =(-4)\int_{-6}^{6} {e}^{u}\cdot (\frac{1}{4})\,\text{d}u \\  & =(-1)\int_{-6}^{6} {e}^{u}\,\text{d}u \\  & =(-1){e}^{u}|_{-6}^{6} \\  & =(-1)({e}^{6}-{e}^{-6}) \\  & =(- {e}^{6})-(- \frac{1}{{e}^{6}}) \\  & =- {e}^{6} + {e}^{-6}\end{aligned}
$$

Evaluate the following integral. Give an exact answer.

$\int_{1}^{2} (3)\cdot {e}^{2 x + 1}\,\text{d}x=$  
{{field-1}}

- \frac{3 {e}^{3}}{2} + \frac{3 {e}^{5}}{2}

If we let $u=2 x + 1,$ then

$$
\frac{\text{d}u}{\text{d}x}=2\quad\Longrightarrow\quad \text{d}x=(\frac{1}{2})\,\text{d}u.
$$

Computing our limits of integration, we get the following:

| $x$ | $1$ | $2$ |
| --- | --- | --- |
| $u$ | $3$ | $5$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{1}^{2} (3)\cdot {e}^{2 x + 1}\,\text{d}x & =(3)\int_{1}^{2} {e}^{2 x + 1}\,\text{d}x \\  & =(3)\int_{3}^{5} {e}^{u}\cdot (\frac{1}{2})\,\text{d}u \\  & =(\frac{3}{2})\int_{3}^{5} {e}^{u}\,\text{d}u \\  & =(\frac{3}{2}){e}^{u}|_{3}^{5} \\  & =(\frac{3}{2})({e}^{5}-{e}^{3}) \\  & =(\frac{3 {e}^{5}}{2})-(\frac{3 {e}^{3}}{2}) \\  & =- \frac{3 {e}^{3}}{2} + \frac{3 {e}^{5}}{2}\end{aligned}
$$
