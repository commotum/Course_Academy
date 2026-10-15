# Private natural exponential integral review

Raw original and translated-coordinate replay is evidence only. Normal source families include documented repairs and method-derived complete banks.

## q-13733 original raw

What is $\displaystyle \int3e^{-6x}dx$?

e^{-6x} + C
-e^{-6x} + C
-6e^{-6x} + C
-\frac{1}{2}e^{-6x} + C
\frac{1}{2}e^{-6x} + C

[No worked solution in captured evidence]

## q-13733 changed raw

What is $\displaystyle \int3e^{-6(x-2)}dx$?

e^{-6(x-2)} + C
-e^{-6(x-2)} + C
-6e^{-6(x-2)} + C
-\frac{1}{2}e^{-6(x-2)} + C
\frac{1}{2}e^{-6(x-2)} + C

[No worked solution in captured evidence]

## q-13733 normal at anchor

What is $\int (3)\cdot {e}^{- 6 x}\,\text{d}x$?

- {e}^{- 6 x}+C
- 6 {e}^{- 6 x}+C
- \frac{{e}^{- 6 x}}{2}+C
\frac{{e}^{- 6 x}}{2}+C
{e}^{- 6 x}+C

If we let $u=- 6 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=-6\quad\Longrightarrow\quad \text{d}x=(- \frac{1}{6})\,\text{d}u.
$$

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int (3)\cdot {e}^{- 6 x}\,\text{d}x & =\int (3)\cdot {e}^{u}\cdot (- \frac{1}{6})\,\text{d}u \\  & =(- \frac{1}{2})\int {e}^{u}\,\text{d}u \\  & =(- \frac{1}{2}){e}^{u}+C \\  & =- \frac{{e}^{- 6 x}}{2}+C\end{aligned}
$$

## q-13733 changed normal

What is $\int (3)\cdot {e}^{12 - 6 x}\,\text{d}x$?

- {e}^{12 - 6 x}+C
- 6 {e}^{12 - 6 x}+C
- \frac{{e}^{12 - 6 x}}{2}+C
\frac{{e}^{12 - 6 x}}{2}+C
{e}^{12 - 6 x}+C

If we let $u=12 - 6 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=-6\quad\Longrightarrow\quad \text{d}x=(- \frac{1}{6})\,\text{d}u.
$$

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int (3)\cdot {e}^{12 - 6 x}\,\text{d}x & =\int (3)\cdot {e}^{u}\cdot (- \frac{1}{6})\,\text{d}u \\  & =(- \frac{1}{2})\int {e}^{u}\,\text{d}u \\  & =(- \frac{1}{2}){e}^{u}+C \\  & =- \frac{{e}^{12 - 6 x}}{2}+C\end{aligned}
$$

## q-30923 original raw

${\int }_{0}^{3}\frac{1}{3}{e}^{x/3}\,\text{d}x=$

e
e-1
\frac{1}{e}
\frac{1}{3}
3

If we let $u=\frac{x}{3},$ then

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{3}\,⟹\,\text{d}u=\frac{1}{3}\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $0$ | $3$ |
| --- | --- | --- |
| $u$ | $0$ | $1$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{3}\frac{1}{3}{e}^{x/3}\,\text{d}x & ={\int }_{0}^{3}{e}^{x/3}\cdot \frac{1}{3}\text{d}x \\  & ={\int }_{0}^{1}{e}^{u}\,\text{d}u \\  & =({e}^{u}){|}_{0}^{1} \\  & ={e}^{1}-{e}^{0} \\  & =e-1\end{aligned}
$$

## q-30923 changed raw

${\int }_{2}^{5}\frac{1}{3}{e}^{(x-2)/3}\,\text{d}x=$

e
e-1
\frac{1}{e}
\frac{1}{3}
3

If we let $u=\frac{(x-2)}{3},$ then

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{3}\,⟹\,\text{d}u=\frac{1}{3}\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $2$ | $5$ |
| --- | --- | --- |
| $u$ | $0$ | $1$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{2}^{5}\frac{1}{3}{e}^{(x-2)/3}\,\text{d}x & ={\int }_{2}^{5}{e}^{(x-2)/3}\cdot \frac{1}{3}\text{d}x \\  & ={\int }_{0}^{1}{e}^{u}\,\text{d}u \\  & =({e}^{u}){|}_{0}^{1} \\  & ={e}^{1}-{e}^{0} \\  & =e-1\end{aligned}
$$

## q-30923 normal at anchor

${\int }_{0}^{3}\frac{1}{3}{e}^{x/3}\,\text{d}x=$

e
{e}^{-1}
-1 + e
\frac{1}{3}
3

If we let $u=\frac{x}{3},$ then

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{3}\,⟹\,\text{d}u=\frac{1}{3}\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $0$ | $3$ |
| --- | --- | --- |
| $u$ | $0$ | $1$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{3}\frac{1}{3}{e}^{x/3}\,\text{d}x & ={\int }_{0}^{3}{e}^{x/3}\cdot \frac{1}{3}\text{d}x \\  & ={\int }_{0}^{1}{e}^{u}\,\text{d}u \\  & =({e}^{u}){|}_{0}^{1} \\  & ={e}^{1}-{e}^{0} \\  & =e-1\end{aligned}
$$

## q-30923 changed normal

${\int }_{2}^{5}\frac{1}{3}{e}^{(x-2)/3}\,\text{d}x=$

e
{e}^{-1}
-1 + e
\frac{1}{3}
3

If we let $u=\frac{(x-2)}{3},$ then

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{3}\,⟹\,\text{d}u=\frac{1}{3}\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $2$ | $5$ |
| --- | --- | --- |
| $u$ | $0$ | $1$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{2}^{5}\frac{1}{3}{e}^{(x-2)/3}\,\text{d}x & ={\int }_{2}^{5}{e}^{(x-2)/3}\cdot \frac{1}{3}\text{d}x \\  & ={\int }_{0}^{1}{e}^{u}\,\text{d}u \\  & =({e}^{u}){|}_{0}^{1} \\  & ={e}^{1}-{e}^{0} \\  & =e-1\end{aligned}
$$

## q-113833 original raw

Calculate $\int {e}^{x/2\,-\,1}\,\text{d}x.$

2\,{e}^{x/2\,-\,1}+C
-2\,{e}^{x/2\,-\,1}+C
2\,{e}^{x-1}+C
{e}^{x/2\,-\,1}+C
\frac{{e}^{x/2\,-\,1}}{2}+C

If we let $u=\frac{x}{2}-1,$ then

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{2}\,⟹\,2\,\text{d}u=\text{d}x.
$$

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int {e}^{x/2\,-\,1}\,\text{d}x & =\int {e}^{u}\cdot 2\,\text{d}u \\  & =2\int {e}^{u}\,\text{d}u \\  & =2\,{e}^{u}+C \\  & =2\,{e}^{x/2\,-\,1}+C\end{aligned}
$$

## q-113833 changed raw

Calculate $\int {e}^{(x-2)/2\,-\,1}\,\text{d}x.$

2\,{e}^{(x-2)/2\,-\,1}+C
-2\,{e}^{(x-2)/2\,-\,1}+C
2\,{e}^{(x-2)-1}+C
{e}^{(x-2)/2\,-\,1}+C
\frac{{e}^{(x-2)/2\,-\,1}}{2}+C

If we let $u=\frac{(x-2)}{2}-1,$ then

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{2}\,⟹\,2\,\text{d}u=\text{d}x.
$$

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int {e}^{(x-2)/2\,-\,1}\,\text{d}x & =\int {e}^{u}\cdot 2\,\text{d}u \\  & =2\int {e}^{u}\,\text{d}u \\  & =2\,{e}^{u}+C \\  & =2\,{e}^{(x-2)/2\,-\,1}+C\end{aligned}
$$

## q-113833 normal at anchor

Calculate $\int {e}^{x/2\,-\,1}\,\text{d}x.$

- 2 {e}^{\frac{x}{2} - 1}+C
2 {e}^{x - 1}+C
2 {e}^{\frac{x}{2} - 1}+C
{e}^{\frac{x}{2} - 1}+C
\frac{{e}^{\frac{x}{2} - 1}}{2}+C

If we let $u=\frac{x}{2}-1,$ then

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{2}\,⟹\,2\,\text{d}u=\text{d}x.
$$

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int {e}^{x/2\,-\,1}\,\text{d}x & =\int {e}^{u}\cdot 2\,\text{d}u \\  & =2\int {e}^{u}\,\text{d}u \\  & =2\,{e}^{u}+C \\  & =2\,{e}^{x/2\,-\,1}+C\end{aligned}
$$

## q-113833 changed normal

Calculate $\int {e}^{(x-2)/2\,-\,1}\,\text{d}x.$

- 2 {e}^{\frac{x}{2} - 2}+C
2 {e}^{x - 3}+C
2 {e}^{\frac{x}{2} - 2}+C
{e}^{\frac{x}{2} - 2}+C
\frac{{e}^{\frac{x}{2} - 2}}{2}+C

If we let $u=\frac{(x-2)}{2}-1,$ then

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{2}\,⟹\,2\,\text{d}u=\text{d}x.
$$

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int {e}^{(x-2)/2\,-\,1}\,\text{d}x & =\int {e}^{u}\cdot 2\,\text{d}u \\  & =2\int {e}^{u}\,\text{d}u \\  & =2\,{e}^{u}+C \\  & =2\,{e}^{(x-2)/2\,-\,1}+C\end{aligned}
$$

## q-13732 original raw

$\int 5{e}^{3x}\,\text{d}x=$

\frac{5}{3}{e}^{3x}+C
5{e}^{3x}+C
\frac{3}{5}{e}^{3x}+C
\frac{5}{3}{e}^{5x}+C
3{e}^{3x}+C

If we let $u=3x,$ then

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\frac{1}{3}\text{d}u=\text{d}x.
$$

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 5{e}^{3x}\,\text{d}x & =\int 5{e}^{u}\cdot \frac{1}{3}\,\text{d}u \\  & =\frac{5}{3}\int {e}^{u}\,\text{d}u \\  & =\frac{5}{3}{e}^{u}+C \\  & =\frac{5}{3}{e}^{3x}+C\end{aligned}
$$

## q-13732 changed raw

$\int 5{e}^{3(x-2)}\,\text{d}x=$

\frac{5}{3}{e}^{3(x-2)}+C
5{e}^{3(x-2)}+C
\frac{3}{5}{e}^{3(x-2)}+C
\frac{5}{3}{e}^{5(x-2)}+C
3{e}^{3(x-2)}+C

If we let $u=3(x-2),$ then

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\frac{1}{3}\text{d}u=\text{d}x.
$$

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 5{e}^{3(x-2)}\,\text{d}x & =\int 5{e}^{u}\cdot \frac{1}{3}\,\text{d}u \\  & =\frac{5}{3}\int {e}^{u}\,\text{d}u \\  & =\frac{5}{3}{e}^{u}+C \\  & =\frac{5}{3}{e}^{3(x-2)}+C\end{aligned}
$$

## q-13732 normal at anchor

$\int 5{e}^{3x}\,\text{d}x=$

5 {e}^{3 x}+C
\frac{3 {e}^{3 x}}{5}+C
\frac{5 {e}^{3 x}}{3}+C
\frac{5 {e}^{5 x}}{3}+C
3 {e}^{3 x}+C

If we let $u=3x,$ then

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\frac{1}{3}\text{d}u=\text{d}x.
$$

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 5{e}^{3x}\,\text{d}x & =\int 5{e}^{u}\cdot \frac{1}{3}\,\text{d}u \\  & =\frac{5}{3}\int {e}^{u}\,\text{d}u \\  & =\frac{5}{3}{e}^{u}+C \\  & =\frac{5}{3}{e}^{3x}+C\end{aligned}
$$

## q-13732 changed normal

$\int 5{e}^{3(x-2)}\,\text{d}x=$

5 {e}^{3 x - 6}+C
\frac{3 {e}^{3 x - 6}}{5}+C
\frac{5 {e}^{3 x - 6}}{3}+C
\frac{5 {e}^{5 x - 10}}{3}+C
3 {e}^{3 x - 6}+C

If we let $u=3(x-2),$ then

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\frac{1}{3}\text{d}u=\text{d}x.
$$

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 5{e}^{3(x-2)}\,\text{d}x & =\int 5{e}^{u}\cdot \frac{1}{3}\,\text{d}u \\  & =\frac{5}{3}\int {e}^{u}\,\text{d}u \\  & =\frac{5}{3}{e}^{u}+C \\  & =\frac{5}{3}{e}^{3(x-2)}+C\end{aligned}
$$

## q-13775 original raw

Evaluate ${\int }_{0}^{\operatorname{ln}⁡2}4{e}^{6x}\,\text{d}x.$

42
\frac{130}{3}
\frac{2}{3}
63
\frac{128}{3}

If we let $u=6x$ then,

$$
\frac{\text{d}u}{\text{d}x}=6\,⟹\,\frac{1}{6}\text{d}u=\,\text{d}x.
$$

Computing our limits of integration,  we get the following:

| $x$ | $0$ | $\operatorname{ln}⁡2$ |
| --- | --- | --- |
| $u$ | $0$ | $6\operatorname{ln}⁡2$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\operatorname{ln}⁡2}4{e}^{6x}\,\text{d}x & =4{\int }_{0}^{\operatorname{ln}⁡2}{e}^{6x}\,\text{d}u \\  & =4{\int }_{0}^{6\operatorname{ln}⁡2}{e}^{u}\frac{1}{6}\text{d}u \\  & =\frac{2}{3}{\int }_{0}^{\operatorname{ln}⁡({2}^{6})}{e}^{u}\text{d}u \\  & =\frac{2}{3}({e}^{u}){|}_{0}^{\operatorname{ln}⁡({2}^{6})} \\  & =\frac{2}{3}({e}^{\operatorname{ln}⁡({2}^{6})}-{e}^{0}) \\  & =\frac{2}{3}({2}^{6}-1) \\  & =\frac{2}{3}(64-1) \\  & =\frac{2}{3}\cdot 63 \\  & =42\end{aligned}
$$

## q-13775 changed raw

Evaluate ${\int }_{2}^{\ln{(2 )} + 2}4{e}^{6(x-2)}\,\text{d}x.$

42
\frac{130}{3}
\frac{2}{3}
63
\frac{128}{3}

If we let $u=6(x-2)$ then,

$$
\frac{\text{d}u}{\text{d}x}=6\,⟹\,\frac{1}{6}\text{d}u=\,\text{d}x.
$$

Computing our limits of integration,  we get the following:

| $x$ | $2$ | $\ln{(2 )} + 2$ |
| --- | --- | --- |
| $u$ | $0$ | $6\operatorname{ln}⁡2$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{2}^{\ln{(2 )} + 2}4{e}^{6(x-2)}\,\text{d}x & =4{\int }_{2}^{\ln{(2 )} + 2}{e}^{6(x-2)}\,\text{d}u \\  & =4{\int }_{0}^{6\operatorname{ln}⁡2}{e}^{u}\frac{1}{6}\text{d}u \\  & =\frac{2}{3}{\int }_{0}^{\operatorname{ln}⁡({2}^{6})}{e}^{u}\text{d}u \\  & =\frac{2}{3}({e}^{u}){|}_{0}^{\operatorname{ln}⁡({2}^{6})} \\  & =\frac{2}{3}({e}^{\operatorname{ln}⁡({2}^{6})}-{e}^{0}) \\  & =\frac{2}{3}({2}^{6}-1) \\  & =\frac{2}{3}(64-1) \\  & =\frac{2}{3}\cdot 63 \\  & =42\end{aligned}
$$

## q-13775 normal at anchor

Evaluate ${\int }_{0}^{\operatorname{ln}⁡2}4{e}^{6x}\,\text{d}x.$

-42
252
42
\frac{130}{3}
\frac{128}{3}

If we let $u=6x$ then,

$$
\frac{\text{d}u}{\text{d}x}=6\,⟹\,\frac{1}{6}\text{d}u=\,\text{d}x.
$$

Computing our limits of integration,  we get the following:

| $x$ | $0$ | $\operatorname{ln}⁡2$ |
| --- | --- | --- |
| $u$ | $0$ | $6\operatorname{ln}⁡2$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\operatorname{ln}⁡2}4{e}^{6x}\,\text{d}x & =4{\int }_{0}^{\operatorname{ln}⁡2}{e}^{6x}\,\text{d}x \\  & =4{\int }_{0}^{6\operatorname{ln}⁡2}{e}^{u}\frac{1}{6}\text{d}u \\  & =\frac{2}{3}{\int }_{0}^{\operatorname{ln}⁡({2}^{6})}{e}^{u}\text{d}u \\  & =\frac{2}{3}({e}^{u}){|}_{0}^{\operatorname{ln}⁡({2}^{6})} \\  & =\frac{2}{3}({e}^{\operatorname{ln}⁡({2}^{6})}-{e}^{0}) \\  & =\frac{2}{3}({2}^{6}-1) \\  & =\frac{2}{3}(64-1) \\  & =\frac{2}{3}\cdot 63 \\  & =42\end{aligned}
$$

## q-13775 changed normal

Evaluate ${\int }_{2}^{\ln{(2 )} + 2}4{e}^{6(x-2)}\,\text{d}x.$

-42
252
42
\frac{130}{3}
\frac{128}{3}

If we let $u=6(x-2)$ then,

$$
\frac{\text{d}u}{\text{d}x}=6\,⟹\,\frac{1}{6}\text{d}u=\,\text{d}x.
$$

Computing our limits of integration,  we get the following:

| $x$ | $2$ | $\ln{(2 )} + 2$ |
| --- | --- | --- |
| $u$ | $0$ | $6\operatorname{ln}⁡2$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{2}^{\ln{(2 )} + 2}4{e}^{6(x-2)}\,\text{d}x & =4{\int }_{2}^{\ln{(2 )} + 2}{e}^{6(x-2)}\,\text{d}x \\  & =4{\int }_{0}^{6\operatorname{ln}⁡2}{e}^{u}\frac{1}{6}\text{d}u \\  & =\frac{2}{3}{\int }_{0}^{\operatorname{ln}⁡({2}^{6})}{e}^{u}\text{d}u \\  & =\frac{2}{3}({e}^{u}){|}_{0}^{\operatorname{ln}⁡({2}^{6})} \\  & =\frac{2}{3}({e}^{\operatorname{ln}⁡({2}^{6})}-{e}^{0}) \\  & =\frac{2}{3}({2}^{6}-1) \\  & =\frac{2}{3}(64-1) \\  & =\frac{2}{3}\cdot 63 \\  & =42\end{aligned}
$$

## q-13786 original raw

${\int }_{0}^{\operatorname{ln}⁡3}5{e}^{-4x}\,\text{d}x=$

\frac{10}{27}
\frac{100}{81}
\frac{100}{9}
\frac{40}{81}
\frac{80}{9}

If we let $u=-4x,$ then, 

$$
\frac{\text{d}u}{\text{d}x}=-4\,⟹\,-\frac{1}{4}\text{d}u=\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $0$ | $\operatorname{ln}⁡3$ |
| --- | --- | --- |
| $u$ | $0$ | $-4\operatorname{ln}⁡3$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\operatorname{ln}⁡3}5{e}^{-4x}\,\text{d}x & =5{\int }_{0}^{\operatorname{ln}⁡3}{e}^{-4x}\,\text{d}x \\  & =5{\int }_{0}^{-4\operatorname{ln}⁡3}{e}^{u}(-\frac{1}{4})\text{d}u \\  & =-\frac{5}{4}{\int }_{0}^{\operatorname{ln}⁡({3}^{-4})}{e}^{u}\text{d}u \\  & =-\frac{5}{4}({e}^{u}){|}_{0}^{\operatorname{ln}⁡({3}^{-4})} \\  & =-\frac{5}{4}({e}^{\operatorname{ln}⁡({3}^{-4})}-{e}^{0}) \\  & =-\frac{5}{4}({3}^{-4}-1) \\  & =-\frac{5}{4}(\frac{1}{{3}^{4}}-1) \\  & =-\frac{5}{4}(\frac{1}{81}-1) \\  & =-\frac{5}{4}(-\frac{80}{81}) \\  & =\frac{100}{81}\end{aligned}
$$

## q-13786 changed raw

${\int }_{2}^{\ln{(3 )} + 2}5{e}^{-4(x-2)}\,\text{d}x=$

\frac{10}{27}
\frac{100}{81}
\frac{100}{9}
\frac{40}{81}
\frac{80}{9}

If we let $u=-4(x-2),$ then, 

$$
\frac{\text{d}u}{\text{d}x}=-4\,⟹\,-\frac{1}{4}\text{d}u=\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $2$ | $\ln{(3 )} + 2$ |
| --- | --- | --- |
| $u$ | $0$ | $-4\operatorname{ln}⁡3$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{2}^{\ln{(3 )} + 2}5{e}^{-4(x-2)}\,\text{d}x & =5{\int }_{2}^{\ln{(3 )} + 2}{e}^{-4(x-2)}\,\text{d}x \\  & =5{\int }_{0}^{-4\operatorname{ln}⁡3}{e}^{u}(-\frac{1}{4})\text{d}u \\  & =-\frac{5}{4}{\int }_{0}^{\operatorname{ln}⁡({3}^{-4})}{e}^{u}\text{d}u \\  & =-\frac{5}{4}({e}^{u}){|}_{0}^{\operatorname{ln}⁡({3}^{-4})} \\  & =-\frac{5}{4}({e}^{\operatorname{ln}⁡({3}^{-4})}-{e}^{0}) \\  & =-\frac{5}{4}({3}^{-4}-1) \\  & =-\frac{5}{4}(\frac{1}{{3}^{4}}-1) \\  & =-\frac{5}{4}(\frac{1}{81}-1) \\  & =-\frac{5}{4}(-\frac{80}{81}) \\  & =\frac{100}{81}\end{aligned}
$$

## q-13786 normal at anchor

${\int }_{0}^{\operatorname{ln}⁡3}5{e}^{-4x}\,\text{d}x=$

- \frac{100}{81}
- \frac{400}{81}
\frac{100}{81}
- \frac{205}{162}
- \frac{5}{324}

If we let $u=-4x,$ then, 

$$
\frac{\text{d}u}{\text{d}x}=-4\,⟹\,-\frac{1}{4}\text{d}u=\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $0$ | $\operatorname{ln}⁡3$ |
| --- | --- | --- |
| $u$ | $0$ | $-4\operatorname{ln}⁡3$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\operatorname{ln}⁡3}5{e}^{-4x}\,\text{d}x & =5{\int }_{0}^{\operatorname{ln}⁡3}{e}^{-4x}\,\text{d}x \\  & =5{\int }_{0}^{-4\operatorname{ln}⁡3}{e}^{u}(-\frac{1}{4})\text{d}u \\  & =-\frac{5}{4}{\int }_{0}^{\operatorname{ln}⁡({3}^{-4})}{e}^{u}\text{d}u \\  & =-\frac{5}{4}({e}^{u}){|}_{0}^{\operatorname{ln}⁡({3}^{-4})} \\  & =-\frac{5}{4}({e}^{\operatorname{ln}⁡({3}^{-4})}-{e}^{0}) \\  & =-\frac{5}{4}({3}^{-4}-1) \\  & =-\frac{5}{4}(\frac{1}{{3}^{4}}-1) \\  & =-\frac{5}{4}(\frac{1}{81}-1) \\  & =-\frac{5}{4}(-\frac{80}{81}) \\  & =\frac{100}{81}\end{aligned}
$$

## q-13786 changed normal

${\int }_{2}^{\ln{(3 )} + 2}5{e}^{-4(x-2)}\,\text{d}x=$

- \frac{100}{81}
- \frac{400}{81}
\frac{100}{81}
- \frac{205}{162}
- \frac{5}{324}

If we let $u=-4(x-2),$ then, 

$$
\frac{\text{d}u}{\text{d}x}=-4\,⟹\,-\frac{1}{4}\text{d}u=\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $2$ | $\ln{(3 )} + 2$ |
| --- | --- | --- |
| $u$ | $0$ | $-4\operatorname{ln}⁡3$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{2}^{\ln{(3 )} + 2}5{e}^{-4(x-2)}\,\text{d}x & =5{\int }_{2}^{\ln{(3 )} + 2}{e}^{-4(x-2)}\,\text{d}x \\  & =5{\int }_{0}^{-4\operatorname{ln}⁡3}{e}^{u}(-\frac{1}{4})\text{d}u \\  & =-\frac{5}{4}{\int }_{0}^{\operatorname{ln}⁡({3}^{-4})}{e}^{u}\text{d}u \\  & =-\frac{5}{4}({e}^{u}){|}_{0}^{\operatorname{ln}⁡({3}^{-4})} \\  & =-\frac{5}{4}({e}^{\operatorname{ln}⁡({3}^{-4})}-{e}^{0}) \\  & =-\frac{5}{4}({3}^{-4}-1) \\  & =-\frac{5}{4}(\frac{1}{{3}^{4}}-1) \\  & =-\frac{5}{4}(\frac{1}{81}-1) \\  & =-\frac{5}{4}(-\frac{80}{81}) \\  & =\frac{100}{81}\end{aligned}
$$

## q-30922 original raw

Evaluate the integral ${\int }_{0}^{\operatorname{ln}⁡4}-5{e}^{-2x}\,\text{d}x.$

-\frac{15}{16}
-\frac{75}{32}
-\frac{25}{16}
-\frac{25}{8}
-\frac{75}{16}

If we let $u=-2x,$ then,

$$
\frac{\text{d}u}{\text{d}x}=-2\,⟹\,-\frac{1}{2}\text{d}u=\,\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $0$ | $\operatorname{ln}⁡4$ |
| --- | --- | --- |
| $u$ | $0$ | $-2\operatorname{ln}⁡4$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\operatorname{ln}⁡4}-5{e}^{-2x}\,\text{d}x & =-5{\int }_{0}^{\operatorname{ln}⁡4}{e}^{-2x}\,\text{d}u \\  & =-5{\int }_{0}^{-2\operatorname{ln}⁡4}{e}^{u}(-\frac{1}{2}\,\text{d}u) \\  & =\frac{5}{2}{\int }_{0}^{\operatorname{ln}⁡({4}^{-2})}{e}^{u}\,\text{d}u \\  & =\frac{5}{2}({e}^{u}){|}_{0}^{\operatorname{ln}⁡({4}^{-2})} \\  & =\frac{5}{2}({e}^{\operatorname{ln}⁡({4}^{-2})}-{e}^{0}) \\  & =\frac{5}{2}({4}^{-2}-1) \\  & =\frac{5}{2}(\frac{1}{16}-1) \\  & =\frac{5}{2}\cdot (-\frac{15}{16}) \\  & =-\frac{75}{32}\end{aligned}
$$

## q-30922 changed raw

Evaluate the integral ${\int }_{2}^{\ln{(4 )} + 2}-5{e}^{-2(x-2)}\,\text{d}x.$

-\frac{15}{16}
-\frac{75}{32}
-\frac{25}{16}
-\frac{25}{8}
-\frac{75}{16}

If we let $u=-2(x-2),$ then,

$$
\frac{\text{d}u}{\text{d}x}=-2\,⟹\,-\frac{1}{2}\text{d}u=\,\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $2$ | $\ln{(4 )} + 2$ |
| --- | --- | --- |
| $u$ | $0$ | $-2\operatorname{ln}⁡4$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{2}^{\ln{(4 )} + 2}-5{e}^{-2(x-2)}\,\text{d}x & =-5{\int }_{2}^{\ln{(4 )} + 2}{e}^{-2(x-2)}\,\text{d}u \\  & =-5{\int }_{0}^{-2\operatorname{ln}⁡4}{e}^{u}(-\frac{1}{2}\,\text{d}u) \\  & =\frac{5}{2}{\int }_{0}^{\operatorname{ln}⁡({4}^{-2})}{e}^{u}\,\text{d}u \\  & =\frac{5}{2}({e}^{u}){|}_{0}^{\operatorname{ln}⁡({4}^{-2})} \\  & =\frac{5}{2}({e}^{\operatorname{ln}⁡({4}^{-2})}-{e}^{0}) \\  & =\frac{5}{2}({4}^{-2}-1) \\  & =\frac{5}{2}(\frac{1}{16}-1) \\  & =\frac{5}{2}\cdot (-\frac{15}{16}) \\  & =-\frac{75}{32}\end{aligned}
$$

## q-30922 normal at anchor

Evaluate the integral ${\int }_{0}^{\operatorname{ln}⁡4}-5{e}^{-2x}\,\text{d}x.$

\frac{75}{32}
\frac{75}{16}
- \frac{75}{32}
\frac{85}{32}
\frac{5}{32}

If we let $u=-2x,$ then,

$$
\frac{\text{d}u}{\text{d}x}=-2\,⟹\,-\frac{1}{2}\text{d}u=\,\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $0$ | $\operatorname{ln}⁡4$ |
| --- | --- | --- |
| $u$ | $0$ | $-2\operatorname{ln}⁡4$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\operatorname{ln}⁡4}-5{e}^{-2x}\,\text{d}x & =-5{\int }_{0}^{\operatorname{ln}⁡4}{e}^{-2x}\,\text{d}x \\  & =-5{\int }_{0}^{-2\operatorname{ln}⁡4}{e}^{u}(-\frac{1}{2}\,\text{d}u) \\  & =\frac{5}{2}{\int }_{0}^{\operatorname{ln}⁡({4}^{-2})}{e}^{u}\,\text{d}u \\  & =\frac{5}{2}({e}^{u}){|}_{0}^{\operatorname{ln}⁡({4}^{-2})} \\  & =\frac{5}{2}({e}^{\operatorname{ln}⁡({4}^{-2})}-{e}^{0}) \\  & =\frac{5}{2}({4}^{-2}-1) \\  & =\frac{5}{2}(\frac{1}{16}-1) \\  & =\frac{5}{2}\cdot (-\frac{15}{16}) \\  & =-\frac{75}{32}\end{aligned}
$$

## q-30922 changed normal

Evaluate the integral ${\int }_{2}^{\ln{(4 )} + 2}-5{e}^{-2(x-2)}\,\text{d}x.$

\frac{75}{32}
\frac{75}{16}
- \frac{75}{32}
\frac{85}{32}
\frac{5}{32}

If we let $u=-2(x-2),$ then,

$$
\frac{\text{d}u}{\text{d}x}=-2\,⟹\,-\frac{1}{2}\text{d}u=\,\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $2$ | $\ln{(4 )} + 2$ |
| --- | --- | --- |
| $u$ | $0$ | $-2\operatorname{ln}⁡4$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{2}^{\ln{(4 )} + 2}-5{e}^{-2(x-2)}\,\text{d}x & =-5{\int }_{2}^{\ln{(4 )} + 2}{e}^{-2(x-2)}\,\text{d}x \\  & =-5{\int }_{0}^{-2\operatorname{ln}⁡4}{e}^{u}(-\frac{1}{2}\,\text{d}u) \\  & =\frac{5}{2}{\int }_{0}^{\operatorname{ln}⁡({4}^{-2})}{e}^{u}\,\text{d}u \\  & =\frac{5}{2}({e}^{u}){|}_{0}^{\operatorname{ln}⁡({4}^{-2})} \\  & =\frac{5}{2}({e}^{\operatorname{ln}⁡({4}^{-2})}-{e}^{0}) \\  & =\frac{5}{2}({4}^{-2}-1) \\  & =\frac{5}{2}(\frac{1}{16}-1) \\  & =\frac{5}{2}\cdot (-\frac{15}{16}) \\  & =-\frac{75}{32}\end{aligned}
$$

## q-349595 original raw

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\operatorname{ln}⁡2}4{e}^{5x}\,\text{d}x=$  
{{field-1}}

\frac{124}{5}

If we let $u=5x,$ then

$$
\frac{\text{d}u}{\text{d}x}=5\,⟹\,\frac{1}{5}\text{d}u=\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $0$ | $\operatorname{ln}⁡2$ |
| --- | --- | --- |
| $u$ | $0$ | $5\operatorname{ln}⁡2$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\operatorname{ln}⁡2}4{e}^{5x}\,\text{d}x & =4{\int }_{0}^{\operatorname{ln}⁡2}{e}^{5x}\,\text{d}x \\  & =4{\int }_{0}^{5\operatorname{ln}⁡2}{e}^{u}\cdot \frac{1}{5}\,\text{d}u \\  & =\frac{4}{5}{\int }_{0}^{\operatorname{ln}⁡({2}^{5})}{e}^{u}\,\text{d}u \\  & =\frac{4}{5}\cdot {e}^{u}\,{|}_{0}^{\operatorname{ln}⁡({2}^{5})} \\  & =\frac{4}{5}({e}^{\operatorname{ln}⁡({2}^{5})}-{e}^{0}) \\  & =\frac{4}{5}({2}^{5}-1) \\  & =\frac{4}{5}(32-1) \\  & =\frac{4}{5}\cdot 31 \\  & =\frac{124}{5}\end{aligned}
$$

## q-349595 changed raw

Evaluate the following integral. Do not round the answer.

${\int }_{2}^{\ln{(2 )} + 2}4{e}^{5(x-2)}\,\text{d}x=$  
{{field-1}}

\frac{124}{5}

If we let $u=5(x-2),$ then

$$
\frac{\text{d}u}{\text{d}x}=5\,⟹\,\frac{1}{5}\text{d}u=\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $2$ | $\ln{(2 )} + 2$ |
| --- | --- | --- |
| $u$ | $0$ | $5\operatorname{ln}⁡2$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{2}^{\ln{(2 )} + 2}4{e}^{5(x-2)}\,\text{d}x & =4{\int }_{2}^{\ln{(2 )} + 2}{e}^{5(x-2)}\,\text{d}x \\  & =4{\int }_{0}^{5\operatorname{ln}⁡2}{e}^{u}\cdot \frac{1}{5}\,\text{d}u \\  & =\frac{4}{5}{\int }_{0}^{\operatorname{ln}⁡({2}^{5})}{e}^{u}\,\text{d}u \\  & =\frac{4}{5}\cdot {e}^{u}\,{|}_{0}^{\operatorname{ln}⁡({2}^{5})} \\  & =\frac{4}{5}({e}^{\operatorname{ln}⁡({2}^{5})}-{e}^{0}) \\  & =\frac{4}{5}({2}^{5}-1) \\  & =\frac{4}{5}(32-1) \\  & =\frac{4}{5}\cdot 31 \\  & =\frac{124}{5}\end{aligned}
$$

## q-349595 normal at anchor

Evaluate the following integral. Give an exact answer.

${\int }_{0}^{\operatorname{ln}⁡2}4{e}^{5x}\,\text{d}x=$  
{{field-1}}

\frac{124}{5}

If we let $u=5x,$ then

$$
\frac{\text{d}u}{\text{d}x}=5\,⟹\,\frac{1}{5}\text{d}u=\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $0$ | $\operatorname{ln}⁡2$ |
| --- | --- | --- |
| $u$ | $0$ | $5\operatorname{ln}⁡2$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\operatorname{ln}⁡2}4{e}^{5x}\,\text{d}x & =4{\int }_{0}^{\operatorname{ln}⁡2}{e}^{5x}\,\text{d}x \\  & =4{\int }_{0}^{5\operatorname{ln}⁡2}{e}^{u}\cdot \frac{1}{5}\,\text{d}u \\  & =\frac{4}{5}{\int }_{0}^{\operatorname{ln}⁡({2}^{5})}{e}^{u}\,\text{d}u \\  & =\frac{4}{5}\cdot {e}^{u}\,{|}_{0}^{\operatorname{ln}⁡({2}^{5})} \\  & =\frac{4}{5}({e}^{\operatorname{ln}⁡({2}^{5})}-{e}^{0}) \\  & =\frac{4}{5}({2}^{5}-1) \\  & =\frac{4}{5}(32-1) \\  & =\frac{4}{5}\cdot 31 \\  & =\frac{124}{5}\end{aligned}
$$

## q-349595 changed normal

Evaluate the following integral. Give an exact answer.

${\int }_{2}^{\ln{(2 )} + 2}4{e}^{5(x-2)}\,\text{d}x=$  
{{field-1}}

\frac{124}{5}

If we let $u=5(x-2),$ then

$$
\frac{\text{d}u}{\text{d}x}=5\,⟹\,\frac{1}{5}\text{d}u=\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $2$ | $\ln{(2 )} + 2$ |
| --- | --- | --- |
| $u$ | $0$ | $5\operatorname{ln}⁡2$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{2}^{\ln{(2 )} + 2}4{e}^{5(x-2)}\,\text{d}x & =4{\int }_{2}^{\ln{(2 )} + 2}{e}^{5(x-2)}\,\text{d}x \\  & =4{\int }_{0}^{5\operatorname{ln}⁡2}{e}^{u}\cdot \frac{1}{5}\,\text{d}u \\  & =\frac{4}{5}{\int }_{0}^{\operatorname{ln}⁡({2}^{5})}{e}^{u}\,\text{d}u \\  & =\frac{4}{5}\cdot {e}^{u}\,{|}_{0}^{\operatorname{ln}⁡({2}^{5})} \\  & =\frac{4}{5}({e}^{\operatorname{ln}⁡({2}^{5})}-{e}^{0}) \\  & =\frac{4}{5}({2}^{5}-1) \\  & =\frac{4}{5}(32-1) \\  & =\frac{4}{5}\cdot 31 \\  & =\frac{124}{5}\end{aligned}
$$

## q-349596 original raw

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\operatorname{ln}⁡4}5{e}^{3x}\,\text{d}x=$  
{{field-1}}

105

If we let $u=3x,$ then

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\frac{1}{3}\text{d}u=\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $0$ | $\operatorname{ln}⁡4$ |
| --- | --- | --- |
| $u$ | $0$ | $3\operatorname{ln}⁡4$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\operatorname{ln}⁡4}5{e}^{3x}\,\text{d}x & =5{\int }_{0}^{\operatorname{ln}⁡4}{e}^{3x}\,\text{d}x \\  & =5{\int }_{0}^{3\operatorname{ln}⁡4}{e}^{u}\cdot \frac{1}{3}\,\text{d}u \\  & =\frac{5}{3}{\int }_{0}^{\operatorname{ln}⁡({4}^{3})}{e}^{u}\,\text{d}u \\  & =\frac{5}{3}\cdot {e}^{u}\,{|}_{0}^{\operatorname{ln}⁡({4}^{3})} \\  & =\frac{5}{3}({e}^{\operatorname{ln}⁡({4}^{3})}-{e}^{0}) \\  & =\frac{5}{3}({4}^{3}-1) \\  & =\frac{5}{3}(64-1) \\  & =\frac{5}{3}(63) \\  & =105\end{aligned}
$$

## q-349596 changed raw

Evaluate the following integral. Do not round the answer.

${\int }_{2}^{\ln{(4 )} + 2}5{e}^{3(x-2)}\,\text{d}x=$  
{{field-1}}

105

If we let $u=3(x-2),$ then

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\frac{1}{3}\text{d}u=\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $2$ | $\ln{(4 )} + 2$ |
| --- | --- | --- |
| $u$ | $0$ | $3\operatorname{ln}⁡4$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{2}^{\ln{(4 )} + 2}5{e}^{3(x-2)}\,\text{d}x & =5{\int }_{2}^{\ln{(4 )} + 2}{e}^{3(x-2)}\,\text{d}x \\  & =5{\int }_{0}^{3\operatorname{ln}⁡4}{e}^{u}\cdot \frac{1}{3}\,\text{d}u \\  & =\frac{5}{3}{\int }_{0}^{\operatorname{ln}⁡({4}^{3})}{e}^{u}\,\text{d}u \\  & =\frac{5}{3}\cdot {e}^{u}\,{|}_{0}^{\operatorname{ln}⁡({4}^{3})} \\  & =\frac{5}{3}({e}^{\operatorname{ln}⁡({4}^{3})}-{e}^{0}) \\  & =\frac{5}{3}({4}^{3}-1) \\  & =\frac{5}{3}(64-1) \\  & =\frac{5}{3}(63) \\  & =105\end{aligned}
$$

## q-349596 normal at anchor

Evaluate the following integral. Give an exact answer.

${\int }_{0}^{\operatorname{ln}⁡4}5{e}^{3x}\,\text{d}x=$  
{{field-1}}

105

If we let $u=3x,$ then

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\frac{1}{3}\text{d}u=\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $0$ | $\operatorname{ln}⁡4$ |
| --- | --- | --- |
| $u$ | $0$ | $3\operatorname{ln}⁡4$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\operatorname{ln}⁡4}5{e}^{3x}\,\text{d}x & =5{\int }_{0}^{\operatorname{ln}⁡4}{e}^{3x}\,\text{d}x \\  & =5{\int }_{0}^{3\operatorname{ln}⁡4}{e}^{u}\cdot \frac{1}{3}\,\text{d}u \\  & =\frac{5}{3}{\int }_{0}^{\operatorname{ln}⁡({4}^{3})}{e}^{u}\,\text{d}u \\  & =\frac{5}{3}\cdot {e}^{u}\,{|}_{0}^{\operatorname{ln}⁡({4}^{3})} \\  & =\frac{5}{3}({e}^{\operatorname{ln}⁡({4}^{3})}-{e}^{0}) \\  & =\frac{5}{3}({4}^{3}-1) \\  & =\frac{5}{3}(64-1) \\  & =\frac{5}{3}(63) \\  & =105\end{aligned}
$$

## q-349596 changed normal

Evaluate the following integral. Give an exact answer.

${\int }_{2}^{\ln{(4 )} + 2}5{e}^{3(x-2)}\,\text{d}x=$  
{{field-1}}

105

If we let $u=3(x-2),$ then

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\frac{1}{3}\text{d}u=\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $2$ | $\ln{(4 )} + 2$ |
| --- | --- | --- |
| $u$ | $0$ | $3\operatorname{ln}⁡4$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{2}^{\ln{(4 )} + 2}5{e}^{3(x-2)}\,\text{d}x & =5{\int }_{2}^{\ln{(4 )} + 2}{e}^{3(x-2)}\,\text{d}x \\  & =5{\int }_{0}^{3\operatorname{ln}⁡4}{e}^{u}\cdot \frac{1}{3}\,\text{d}u \\  & =\frac{5}{3}{\int }_{0}^{\operatorname{ln}⁡({4}^{3})}{e}^{u}\,\text{d}u \\  & =\frac{5}{3}\cdot {e}^{u}\,{|}_{0}^{\operatorname{ln}⁡({4}^{3})} \\  & =\frac{5}{3}({e}^{\operatorname{ln}⁡({4}^{3})}-{e}^{0}) \\  & =\frac{5}{3}({4}^{3}-1) \\  & =\frac{5}{3}(64-1) \\  & =\frac{5}{3}(63) \\  & =105\end{aligned}
$$

## q-349601 original raw

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{2}4{e}^{4x+1}\,\text{d}x=$  
{{field-1}}

{e}^{9}-e

If we let $u=4x+1,$ then

$$
\frac{\text{d}u}{\text{d}x}=4\,⟹\,\frac{1}{4}\text{d}u=\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $0$ | $2$ |
| --- | --- | --- |
| $u$ | $1$ | $9$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{2}4{e}^{4x+1}\,\text{d}x & =4{\int }_{0}^{2}{e}^{4x+1}\,\text{d}x \\  & =4{\int }_{1}^{9}{e}^{u}\cdot \frac{1}{4}\,\text{d}u \\  & ={\int }_{1}^{9}{e}^{u}\,\text{d}u \\  & ={e}^{u}\,{|}_{1}^{9} \\  & ={e}^{9}-{e}^{1} \\  & ={e}^{9}-e\end{aligned}
$$

## q-349601 changed raw

Evaluate the following integral. Do not round the answer.

${\int }_{2}^{4}4{e}^{4(x-2)+1}\,\text{d}x=$  
{{field-1}}

{e}^{9}-e

If we let $u=4(x-2)+1,$ then

$$
\frac{\text{d}u}{\text{d}x}=4\,⟹\,\frac{1}{4}\text{d}u=\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $2$ | $4$ |
| --- | --- | --- |
| $u$ | $1$ | $9$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{2}^{4}4{e}^{4(x-2)+1}\,\text{d}x & =4{\int }_{2}^{4}{e}^{4(x-2)+1}\,\text{d}x \\  & =4{\int }_{1}^{9}{e}^{u}\cdot \frac{1}{4}\,\text{d}u \\  & ={\int }_{1}^{9}{e}^{u}\,\text{d}u \\  & ={e}^{u}\,{|}_{1}^{9} \\  & ={e}^{9}-{e}^{1} \\  & ={e}^{9}-e\end{aligned}
$$

## q-349601 normal at anchor

Evaluate the following integral. Give an exact answer.

${\int }_{0}^{2}4{e}^{4x+1}\,\text{d}x=$  
{{field-1}}

- e + {e}^{9}

If we let $u=4x+1,$ then

$$
\frac{\text{d}u}{\text{d}x}=4\,⟹\,\frac{1}{4}\text{d}u=\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $0$ | $2$ |
| --- | --- | --- |
| $u$ | $1$ | $9$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{2}4{e}^{4x+1}\,\text{d}x & =4{\int }_{0}^{2}{e}^{4x+1}\,\text{d}x \\  & =4{\int }_{1}^{9}{e}^{u}\cdot \frac{1}{4}\,\text{d}u \\  & ={\int }_{1}^{9}{e}^{u}\,\text{d}u \\  & ={e}^{u}\,{|}_{1}^{9} \\  & ={e}^{9}-{e}^{1} \\  & ={e}^{9}-e\end{aligned}
$$

## q-349601 changed normal

Evaluate the following integral. Give an exact answer.

${\int }_{2}^{4}4{e}^{4(x-2)+1}\,\text{d}x=$  
{{field-1}}

- e + {e}^{9}

If we let $u=4(x-2)+1,$ then

$$
\frac{\text{d}u}{\text{d}x}=4\,⟹\,\frac{1}{4}\text{d}u=\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $2$ | $4$ |
| --- | --- | --- |
| $u$ | $1$ | $9$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{2}^{4}4{e}^{4(x-2)+1}\,\text{d}x & =4{\int }_{2}^{4}{e}^{4(x-2)+1}\,\text{d}x \\  & =4{\int }_{1}^{9}{e}^{u}\cdot \frac{1}{4}\,\text{d}u \\  & ={\int }_{1}^{9}{e}^{u}\,\text{d}u \\  & ={e}^{u}\,{|}_{1}^{9} \\  & ={e}^{9}-{e}^{1} \\  & ={e}^{9}-e\end{aligned}
$$

## q-362689 original raw

Evaluate the following integral. Do not round the answer.

${\int }_{-1}^{0}12{e}^{-4x}\,\text{d}x=$  
{{field-1}}

3{e}^{4}-3

If we let $u=-4x,$ then

$$
\frac{\text{d}u}{\text{d}x}=-4\,⟹\,-\frac{1}{4}\text{d}u=\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $-1$ | $0$ |
| --- | --- | --- |
| $u$ | $4$ | $0$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{-1}^{0}12{e}^{-4x}\,\text{d}x & =12{\int }_{-1}^{0}{e}^{-4x}\,\text{d}x \\  & =12{\int }_{4}^{0}{e}^{u}\cdot (-\frac{1}{4})\,\text{d}u \\  & =-3{\int }_{4}^{0}{e}^{u}\,\text{d}u \\  & =-3\cdot {e}^{u}\,{|}_{4}^{0} \\  & =-3({e}^{0}-{e}^{4}) \\  & =-3(1-{e}^{4}) \\  & =3{e}^{4}-3\end{aligned}
$$

## q-362689 changed raw

Evaluate the following integral. Do not round the answer.

${\int }_{1}^{2}12{e}^{-4(x-2)}\,\text{d}x=$  
{{field-1}}

3{e}^{4}-3

If we let $u=-4(x-2),$ then

$$
\frac{\text{d}u}{\text{d}x}=-4\,⟹\,-\frac{1}{4}\text{d}u=\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $1$ | $2$ |
| --- | --- | --- |
| $u$ | $4$ | $0$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{1}^{2}12{e}^{-4(x-2)}\,\text{d}x & =12{\int }_{1}^{2}{e}^{-4(x-2)}\,\text{d}x \\  & =12{\int }_{4}^{0}{e}^{u}\cdot (-\frac{1}{4})\,\text{d}u \\  & =-3{\int }_{4}^{0}{e}^{u}\,\text{d}u \\  & =-3\cdot {e}^{u}\,{|}_{4}^{0} \\  & =-3({e}^{0}-{e}^{4}) \\  & =-3(1-{e}^{4}) \\  & =3{e}^{4}-3\end{aligned}
$$

## q-362689 normal at anchor

Evaluate the following integral. Give an exact answer.

${\int }_{-1}^{0}12{e}^{-4x}\,\text{d}x=$  
{{field-1}}

-3 + 3 {e}^{4}

If we let $u=-4x,$ then

$$
\frac{\text{d}u}{\text{d}x}=-4\,⟹\,-\frac{1}{4}\text{d}u=\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $-1$ | $0$ |
| --- | --- | --- |
| $u$ | $4$ | $0$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{-1}^{0}12{e}^{-4x}\,\text{d}x & =12{\int }_{-1}^{0}{e}^{-4x}\,\text{d}x \\  & =12{\int }_{4}^{0}{e}^{u}\cdot (-\frac{1}{4})\,\text{d}u \\  & =-3{\int }_{4}^{0}{e}^{u}\,\text{d}u \\  & =-3\cdot {e}^{u}\,{|}_{4}^{0} \\  & =-3({e}^{0}-{e}^{4}) \\  & =-3(1-{e}^{4}) \\  & =3{e}^{4}-3\end{aligned}
$$

## q-362689 changed normal

Evaluate the following integral. Give an exact answer.

${\int }_{1}^{2}12{e}^{-4(x-2)}\,\text{d}x=$  
{{field-1}}

-3 + 3 {e}^{4}

If we let $u=-4(x-2),$ then

$$
\frac{\text{d}u}{\text{d}x}=-4\,⟹\,-\frac{1}{4}\text{d}u=\text{d}x.
$$

Computing our limits of integration, we get the following:

| $x$ | $1$ | $2$ |
| --- | --- | --- |
| $u$ | $4$ | $0$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{1}^{2}12{e}^{-4(x-2)}\,\text{d}x & =12{\int }_{1}^{2}{e}^{-4(x-2)}\,\text{d}x \\  & =12{\int }_{4}^{0}{e}^{u}\cdot (-\frac{1}{4})\,\text{d}u \\  & =-3{\int }_{4}^{0}{e}^{u}\,\text{d}u \\  & =-3\cdot {e}^{u}\,{|}_{4}^{0} \\  & =-3({e}^{0}-{e}^{4}) \\  & =-3(1-{e}^{4}) \\  & =3{e}^{4}-3\end{aligned}
$$

## q-51160 original raw

$\int {e}^{z}{e}^{z}\,\text{d}z=$

-\frac{{e}^{{z}^{2}}}{2}+C
\frac{{e}^{2z}}{2}+C
2{e}^{2z}+C
\frac{{e}^{z}}{2}+C
{e}^{2z}+C

First, we notice that

$$
\int {e}^{z}{e}^{z}\,\text{d}z=\int {e}^{2z}\,\text{d}z.
$$

If we let $u=2z$, then

$$
\frac{\text{d}u}{\text{d}z}=2\,⟹\,\text{d}z=\frac{1}{2}\text{d}u.
$$

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int {e}^{2z}\,\text{d}z & =\int {e}^{2z}\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}\int {e}^{2z}\,\text{d}u \\  & =\frac{1}{2}\int {e}^{u}\,\text{d}u \\  & =\frac{1}{2}\cdot {e}^{u}+C \\  & =\frac{{e}^{2z}}{2}+C\end{aligned}\end{aligned}
$$

## q-51160 changed raw

$\int {e}^{(z-2)}{e}^{(z-2)}\,\text{d}z=$

-\frac{{e}^{{(z-2)}^{2}}}{2}+C
\frac{{e}^{2(z-2)}}{2}+C
2{e}^{2(z-2)}+C
\frac{{e}^{(z-2)}}{2}+C
{e}^{2(z-2)}+C

First, we notice that

$$
\int {e}^{(z-2)}{e}^{(z-2)}\,\text{d}z=\int {e}^{2(z-2)}\,\text{d}z.
$$

If we let $u=2(z-2)$, then

$$
\frac{\text{d}u}{\text{d}z}=2\,⟹\,\text{d}z=\frac{1}{2}\text{d}u.
$$

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int {e}^{2(z-2)}\,\text{d}z & =\int {e}^{2(z-2)}\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}\int {e}^{2(z-2)}\,\text{d}u \\  & =\frac{1}{2}\int {e}^{u}\,\text{d}u \\  & =\frac{1}{2}\cdot {e}^{u}+C \\  & =\frac{{e}^{2(z-2)}}{2}+C\end{aligned}\end{aligned}
$$

## q-51160 normal at anchor

$\int {e}^{z}{e}^{z}\,\text{d}z=$

- \frac{{e}^{z^{2}}}{2}+C
2 {e}^{2 z}+C
\frac{{e}^{2 z}}{2}+C
\frac{{e}^{z}}{2}+C
{e}^{2 z}+C

First, we notice that

$$
\int {e}^{z}{e}^{z}\,\text{d}z=\int {e}^{2z}\,\text{d}z.
$$

If we let $u=2z$, then

$$
\frac{\text{d}u}{\text{d}z}=2\,⟹\,\text{d}z=\frac{1}{2}\text{d}u.
$$

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int {e}^{2z}\,\text{d}z & =\int {e}^{2(u/2)}\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}\int {e}^{2(u/2)}\,\text{d}u \\  & =\frac{1}{2}\int {e}^{u}\,\text{d}u \\  & =\frac{1}{2}\cdot {e}^{u}+C \\  & =\frac{{e}^{2z}}{2}+C\end{aligned}\end{aligned}
$$

## q-51160 changed normal

$\int {e}^{(z-2)}{e}^{(z-2)}\,\text{d}z=$

- \frac{{e}^{(z - 2)^{2}}}{2}+C
2 {e}^{2 z - 4}+C
\frac{{e}^{2 z - 4}}{2}+C
\frac{{e}^{z - 2}}{2}+C
{e}^{2 z - 4}+C

First, we notice that

$$
\int {e}^{(z-2)}{e}^{(z-2)}\,\text{d}z=\int {e}^{2(z-2)}\,\text{d}z.
$$

If we let $u=2(z-2)$, then

$$
\frac{\text{d}u}{\text{d}z}=2\,⟹\,\text{d}z=\frac{1}{2}\text{d}u.
$$

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int {e}^{2(z-2)}\,\text{d}z & =\int {e}^{2(u/2)}\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}\int {e}^{2(u/2)}\,\text{d}u \\  & =\frac{1}{2}\int {e}^{u}\,\text{d}u \\  & =\frac{1}{2}\cdot {e}^{u}+C \\  & =\frac{{e}^{2(z-2)}}{2}+C\end{aligned}\end{aligned}
$$

## easy authored affine

What is $\int (2)\cdot {e}^{4 x - 1}\,\text{d}x$?

\frac{{e}^{4 x - 1}}{2}+C
2 {e}^{4 x - 1}+C
8 {e}^{4 x - 1}+C
\frac{{e}^{1 - 4 x}}{2}+C
- \frac{{e}^{4 x - 1}}{2}+C

If we let $u=4 x - 1,$ then

$$
\frac{\text{d}u}{\text{d}x}=4\quad\Longrightarrow\quad \text{d}x=(\frac{1}{4})\,\text{d}u.
$$

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int (2)\cdot {e}^{4 x - 1}\,\text{d}x & =\int (2)\cdot {e}^{u}\cdot (\frac{1}{4})\,\text{d}u \\  & =(\frac{1}{2})\int {e}^{u}\,\text{d}u \\  & =(\frac{1}{2}){e}^{u}+C \\  & =\frac{{e}^{4 x - 1}}{2}+C\end{aligned}
$$

## easy authored affine

What is $\int (-3)\cdot {e}^{2 x - 1}\,\text{d}x$?

\frac{3 {e}^{2 x - 1}}{2}+C
- 6 {e}^{2 x - 1}+C
- \frac{3 {e}^{2 x - 1}}{2}+C
- \frac{3 {e}^{1 - 2 x}}{2}+C
- 3 {e}^{2 x - 1}+C

If we let $u=2 x - 1,$ then

$$
\frac{\text{d}u}{\text{d}x}=2\quad\Longrightarrow\quad \text{d}x=(\frac{1}{2})\,\text{d}u.
$$

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int (-3)\cdot {e}^{2 x - 1}\,\text{d}x & =\int (-3)\cdot {e}^{u}\cdot (\frac{1}{2})\,\text{d}u \\  & =(- \frac{3}{2})\int {e}^{u}\,\text{d}u \\  & =(- \frac{3}{2}){e}^{u}+C \\  & =- \frac{3 {e}^{2 x - 1}}{2}+C\end{aligned}
$$

## moderate authored affine

Evaluate the following integral. Give an exact answer.

$\int_{-2}^{0} (-1)\cdot {e}^{- 2 x}\,\text{d}x=$  
{{field-1}}

\frac{1}{2} - \frac{{e}^{4}}{2}

If we let $u=- 2 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=-2\quad\Longrightarrow\quad \text{d}x=(- \frac{1}{2})\,\text{d}u.
$$

Computing our limits of integration, we get the following:

| $x$ | $-2$ | $0$ |
| --- | --- | --- |
| $u$ | $4$ | $0$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{-2}^{0} (-1)\cdot {e}^{- 2 x}\,\text{d}x & =(-1)\int_{-2}^{0} {e}^{- 2 x}\,\text{d}x \\  & =(-1)\int_{4}^{0} {e}^{u}\cdot (- \frac{1}{2})\,\text{d}u \\  & =(\frac{1}{2})\int_{4}^{0} {e}^{u}\,\text{d}u \\  & =(\frac{1}{2}){e}^{u}|_{4}^{0} \\  & =(\frac{1}{2})({e}^{0}-{e}^{4}) \\  & =(\frac{1}{2})-(\frac{{e}^{4}}{2}) \\  & =\frac{1}{2} - \frac{{e}^{4}}{2}\end{aligned}
$$

## moderate authored affine

Evaluate the following integral. Give an exact answer.

$\int_{0}^{1} (-4)\cdot {e}^{- x}\,\text{d}x=$  
{{field-1}}

-4 + \frac{4}{e}

If we let $u=- x,$ then

$$
\frac{\text{d}u}{\text{d}x}=-1\quad\Longrightarrow\quad \text{d}x=(-1)\,\text{d}u.
$$

Computing our limits of integration, we get the following:

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $0$ | $-1$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{1} (-4)\cdot {e}^{- x}\,\text{d}x & =(-4)\int_{0}^{1} {e}^{- x}\,\text{d}x \\  & =(-4)\int_{0}^{-1} {e}^{u}\cdot (-1)\,\text{d}u \\  & =(4)\int_{0}^{-1} {e}^{u}\,\text{d}u \\  & =(4){e}^{u}|_{0}^{-1} \\  & =(4)({e}^{-1}-{e}^{0}) \\  & =(\frac{4}{e})-(4) \\  & =-4 + \frac{4}{e}\end{aligned}
$$

## hard authored affine

Evaluate the following integral. Give an exact answer.

$\int_{-2}^{-1} (2)\cdot {e}^{1 - 2 x}\,\text{d}x=$  
{{field-1}}

- {e}^{3} + {e}^{5}

If we let $u=1 - 2 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=-2\quad\Longrightarrow\quad \text{d}x=(- \frac{1}{2})\,\text{d}u.
$$

Computing our limits of integration, we get the following:

| $x$ | $-2$ | $-1$ |
| --- | --- | --- |
| $u$ | $5$ | $3$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{-2}^{-1} (2)\cdot {e}^{1 - 2 x}\,\text{d}x & =(2)\int_{-2}^{-1} {e}^{1 - 2 x}\,\text{d}x \\  & =(2)\int_{5}^{3} {e}^{u}\cdot (- \frac{1}{2})\,\text{d}u \\  & =(-1)\int_{5}^{3} {e}^{u}\,\text{d}u \\  & =(-1){e}^{u}|_{5}^{3} \\  & =(-1)({e}^{3}-{e}^{5}) \\  & =(- {e}^{3})-(- {e}^{5}) \\  & =- {e}^{3} + {e}^{5}\end{aligned}
$$

## hard authored affine

Evaluate the following integral. Give an exact answer.

$\int_{-2}^{1} (-4)\cdot {e}^{- 4 x - 2}\,\text{d}x=$  
{{field-1}}

- {e}^{6} + {e}^{-6}

If we let $u=- 4 x - 2,$ then

$$
\frac{\text{d}u}{\text{d}x}=-4\quad\Longrightarrow\quad \text{d}x=(- \frac{1}{4})\,\text{d}u.
$$

Computing our limits of integration, we get the following:

| $x$ | $-2$ | $1$ |
| --- | --- | --- |
| $u$ | $6$ | $-6$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{-2}^{1} (-4)\cdot {e}^{- 4 x - 2}\,\text{d}x & =(-4)\int_{-2}^{1} {e}^{- 4 x - 2}\,\text{d}x \\  & =(-4)\int_{6}^{-6} {e}^{u}\cdot (- \frac{1}{4})\,\text{d}u \\  & =(1)\int_{6}^{-6} {e}^{u}\,\text{d}u \\  & =(1){e}^{u}|_{6}^{-6} \\  & =(1)({e}^{-6}-{e}^{6}) \\  & =({e}^{-6})-({e}^{6}) \\  & =- {e}^{6} + {e}^{-6}\end{aligned}
$$

## Explicit Euler coefficient semantics

Evaluate the following integral. Give an exact answer.

$\int_{0}^{1} (3)\cdot {e}^{x}\,\text{d}x=$  
{{field-1}}

-3 + 3\cdot e

If we let $u=x,$ then

$$
\frac{\text{d}u}{\text{d}x}=1\quad\Longrightarrow\quad \text{d}x=(1)\,\text{d}u.
$$

Computing our limits of integration, we get the following:

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $0$ | $1$ |

Then, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{1} (3)\cdot {e}^{x}\,\text{d}x & =(3)\int_{0}^{1} {e}^{x}\,\text{d}x \\  & =(3)\int_{0}^{1} {e}^{u}\cdot (1)\,\text{d}u \\  & =(3)\int_{0}^{1} {e}^{u}\,\text{d}u \\  & =(3){e}^{u}|_{0}^{1} \\  & =(3)({e}^{1}-{e}^{0}) \\  & =(3\cdot e)-(3) \\  & =-3 + 3\cdot e\end{aligned}
$$
