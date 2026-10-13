# Particular-solution generator review

Observed raw originals preserve absent attributes and teaching errors. Repaired variants are labeled. No plots.

## q-119078 — unrated (authored easy in repaired completion) — original raw replay

Find the particular solution to the differential equation $(x - 1)^{2}y^{′} =-2$ that satisfies the condition $y(2) = 1$.

- $y=-1 + \frac{2}{x - 1}$
- $y=\frac{1}{2} + \frac{1}{x - 1}$
- $y=\frac{3}{2} - \frac{1}{2 x - 2}$
- $y=3 + \frac{2}{x - 1}$
- $y=\frac{1}{x - 1}$

[No captured worked solution.]

### easy — generated initial-ordinate variant (repaired source presentation)

Find the particular solution to the differential equation $(x - 1)^{2}y^{′} =-2$ that satisfies the condition $y(2) = 3$.

- $y=5 + \frac{2}{x - 1}$
- $y=2 + \frac{1}{x - 1}$
- $y=1 + \frac{2}{x - 1}$
- $y=\frac{7}{2} - \frac{1}{2 x - 2}$
- $y=\frac{5}{2} + \frac{1}{x - 1}$

First, we rearrange the equation to give

$$
y'=- \frac{2}{(x - 1)^{2}}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int y'\,\text{d}x & =\int (- \frac{2}{(x - 1)^{2}})\,\text{d}x \\ y & =(-2)\int (\frac{1}{(x - 1)^{2}})\,\text{d}x \\ & =(-2)(- \frac{1}{x - 1})+C \\ & =\frac{2}{x - 1}+C.\end{aligned}
$$

So our general solution is $y=\frac{2}{x - 1}+C.$ To find a particular solution, we substitute the condition $y(2)=3$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}3 & =(\frac{2}{(2) - 1})+C \\ 3 & =2+C \\ C & =1.\end{aligned}
$$

Therefore, our particular solution is

$$
y=1 + \frac{2}{x - 1}.
$$

## q-49942 — unrated (authored easy in repaired completion) — original raw replay

Find the particular solution to the differential equation below that satisfies the condition $f(0) =-1$.

$2f^{′}(x) + e^{x} = 0$.

- $f(x)=1 - \frac{e^{x}}{2}$
- $f(x)=e^{x} - 2$
- $f(x)=\frac{e^{x}}{2} - 1$
- $f(x)=- \frac{e^{x}}{2} - \frac{1}{2}$
- $f(x)=\frac{e^{x}}{2} - \frac{3}{2}$

[No captured worked solution.]

### easy — generated initial-ordinate variant (repaired source presentation)

Find the particular solution to the differential equation below that satisfies the condition $f(0) =1$.

$2f^{′}(x) + e^{x} = 0$.

- $f(x)=\frac{3}{2} - \frac{e^{x}}{2}$
- $f(x)=\frac{e^{x}}{2} + \frac{1}{2}$
- $f(x)=3 - \frac{e^{x}}{2}$
- $f(x)=\frac{e^{x}}{2} + 1$
- $f(x)=e^{x}$

First, we rearrange the equation to give

$$
f'(x)=- \frac{e^{x}}{2}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int f'(x)\,\text{d}x & =\int (- \frac{e^{x}}{2})\,\text{d}x \\ f(x) & =(- \frac{1}{2})\int (e^{x})\,\text{d}x \\ & =(- \frac{1}{2})(e^{x})+C \\ & =- \frac{e^{x}}{2}+C.\end{aligned}
$$

So our general solution is $f(x)=- \frac{e^{x}}{2}+C.$ To find a particular solution, we substitute the condition $f(0)=1$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}1 & =(- \frac{e^{(0)}}{2})+C \\ 1 & =- \frac{1}{2}+C \\ C & =\frac{3}{2}.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=\frac{3}{2} - \frac{e^{x}}{2}.
$$

## q-119045 — easy — original raw replay

Find the particular solution to the differential equation ${f}^{′}(x)+2\operatorname{cos}⁡x=0$ that satisfies the condition $f(0)=-1.$

- $f(x)=\frac{\sin{(x )}}{2} - 1$
- $f(x)=2 \cos{(x )} - 3$
- $f(x)=- 2 \sin{(x )} - 1$
- $f(x)=1 - 2 \cos{(x )}$
- $f(x)=2 \sin{(x )} - 3$

First, we rearrange the equation to give

$$
{f}^{′}(x)=-2\operatorname{cos}⁡x.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =\int (-2\operatorname{cos}⁡x)\,\text{d}x \\ f(x) & =-2\int \operatorname{cos}⁡x\,\text{d}x \\  & =-2\operatorname{sin}⁡x+C.\end{aligned}
$$

So our general solution is $y=-2\operatorname{sin}⁡x+C.$ To find a particular solution, we substitute the condition $f(0)=-1$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}-1 & =-2\operatorname{sin}⁡0+C \\ -1 & =-2(0)+C \\ C & =-1.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=-2\operatorname{sin}⁡x-1.
$$

### easy — generated initial-ordinate variant (repaired source presentation)

Find the particular solution to the differential equation ${f}^{′}(x)+2\operatorname{cos}⁡x=0$ that satisfies the condition $f(0)=1.$

- $f(x)=3 - 2 \cos{(x )}$
- $f(x)=2 \sin{(x )} - 1$
- $f(x)=\frac{\sin{(x )}}{2} + 1$
- $f(x)=1 - 2 \sin{(x )}$
- $f(x)=2 \cos{(x )} - 1$

First, we rearrange the equation to give

$$
{f}^{′}(x)=-2\operatorname{cos}⁡x.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =\int (-2\operatorname{cos}⁡x)\,\text{d}x \\ f(x) & =-2\int \operatorname{cos}⁡x\,\text{d}x \\  & =-2\operatorname{sin}⁡x+C.\end{aligned}
$$

So our general solution is $f(x)=-2\operatorname{sin}⁡x+C.$ To find a particular solution, we substitute the condition $f(0)=1$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}1 & =-2\operatorname{sin}⁡0+C \\ 1 & =-2(0)+C \\ C & =1.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=-2\operatorname{sin}⁡x-1+2.
$$

## q-119046 — easy — original raw replay

Find the particular solution to the differential equation ${f}^{′}(x)-4x=1$ that satisfies the condition $f(1)=-1.$

- $f(x)=x^{2} + 2 x - 4$
- $f(x)=x^{2} - 2 x$
- $f(x)=2 x^{2} + x - 4$
- $f(x)=2 x^{2} + x - 1$
- $f(x)=2 x^{2} + 3 x - 6$

First, we rearrange the equation to give

$$
{f}^{′}(x)=4x+1.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =\int (4x+1)\,\text{d}x \\ f(x) & =4\int x\,\text{d}x+\int \text{d}x \\  & =4(\frac{1}{2}{x}^{2})+x+C \\  & =2{x}^{2}+x+C.\end{aligned}
$$

So our general solution is $f(x)=2{x}^{2}+x+C.$ To find a particular solution, we substitute the condition $f(1)=-1$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}-1 & =2(1)^{2}+1+C \\ -1 & =2+1+C \\ C & =-4.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=2{x}^{2}+x-4.
$$

### easy — generated initial-ordinate variant (repaired source presentation)

Find the particular solution to the differential equation ${f}^{′}(x)-4x=1$ that satisfies the condition $f(1)=1.$

- $f(x)=2 x^{2} + x + 1$
- $f(x)=2 x^{2} + 3 x - 4$
- $f(x)=x^{2} + 2 x - 2$
- $f(x)=2 x^{2} + x - 2$
- $f(x)=x^{2} - 2 x + 2$

First, we rearrange the equation to give

$$
{f}^{′}(x)=4x+1.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =\int (4x+1)\,\text{d}x \\ f(x) & =4\int x\,\text{d}x+\int \text{d}x \\  & =4(\frac{1}{2}{x}^{2})+x+C \\  & =2{x}^{2}+x+C.\end{aligned}
$$

So our general solution is $f(x)=2{x}^{2}+x+C.$ To find a particular solution, we substitute the condition $f(1)=1$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}1 & =2(1)^{2}+1+C \\ 1 & =2+1+C \\ C & =-2.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=2{x}^{2}+x-4+2.
$$

## q-119075 — moderate — original raw replay

Find the particular solution to the differential equation ${y}^{′}+{e}^{-2x}=8x$ that satisfies the condition $y(0)=1.$

- $y=2 x^{2} + \frac{1}{2} + \frac{e^{- 2 x}}{2}$
- $y=8 x^{2} - 1 + 2 e^{- 2 x}$
- $y=2 x^{2} + 3 - 2 e^{- 2 x}$
- $y=4 x^{2} + \frac{1}{2} + \frac{e^{- 2 x}}{2}$
- $y=4 x^{2} - \frac{3}{2} + \frac{e^{- 2 x}}{2}$

First, we rearrange the equation to give

$$
{y}^{′}=8x-{e}^{-2x}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {y}^{′}\,\text{d}x & =\int (8x-{e}^{-2x})\,\text{d}x \\ y & =8\int x\,\text{d}x-\int {e}^{-2x}\,\text{d}x \\  & =8(\frac{{x}^{2}}{2})-(-\frac{{e}^{-2x}}{2})+C \\  & =4{x}^{2}+\frac{{e}^{-2x}}{2}+C.\end{aligned}
$$

So our general solution is $y=4{x}^{2}+\frac{{e}^{-2x}}{2}+C.$ To find a particular solution, we substitute the condition $y(0)=1$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}1 & =4(0)^{2}+\frac{{e}^{-2(0)}}{2}+C \\ 1 & =0+\frac{1}{2}+C \\ C & =\frac{1}{2}.\end{aligned}
$$

Therefore, our particular solution is

$$
y=4{x}^{2}+\frac{{e}^{-2x}}{2}+\frac{1}{2}.
$$

### moderate — generated initial-ordinate variant (repaired source presentation)

Find the particular solution to the differential equation ${y}^{′}+{e}^{-2x}=8x$ that satisfies the condition $y(0)=3.$

- $y=4 x^{2} + \frac{5}{2} + \frac{e^{- 2 x}}{2}$
- $y=4 x^{2} + \frac{1}{2} + \frac{e^{- 2 x}}{2}$
- $y=2 x^{2} + \frac{5}{2} + \frac{e^{- 2 x}}{2}$
- $y=2 x^{2} + 5 - 2 e^{- 2 x}$
- $y=8 x^{2} + 1 + 2 e^{- 2 x}$

First, we rearrange the equation to give

$$
{y}^{′}=8x-{e}^{-2x}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {y}^{′}\,\text{d}x & =\int (8x-{e}^{-2x})\,\text{d}x \\ y & =8\int x\,\text{d}x-\int {e}^{-2x}\,\text{d}x \\  & =8(\frac{{x}^{2}}{2})-(-\frac{{e}^{-2x}}{2})+C \\  & =4{x}^{2}+\frac{{e}^{-2x}}{2}+C.\end{aligned}
$$

So our general solution is $y=4{x}^{2}+\frac{{e}^{-2x}}{2}+C.$ To find a particular solution, we substitute the condition $y(0)=3$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}3 & =4(0)^{2}+\frac{{e}^{-2(0)}}{2}+C \\ 3 & =0+\frac{1}{2}+C \\ C & =\frac{5}{2}.\end{aligned}
$$

Therefore, our particular solution is

$$
y=4{x}^{2}+\frac{{e}^{-2x}}{2}+\frac{1}{2}+2.
$$

## q-119083 — moderate — original raw replay

Find the particular solution to the differential equation ${y}^{′}-2x={e}^{x/2}$ that satisfies the condition $y(0)=2.$

- $y=2 x + e^{\frac{x}{2}} + 1$
- $y=x^{2} + 2 e^{\frac{x}{2}} + 2$
- $y=x - \frac{e^{\frac{x}{2}}}{2} + \frac{5}{2}$
- $y=x^{2} + \frac{e^{\frac{x}{2}}}{2} + \frac{3}{2}$
- $y=x^{2} + 2 e^{\frac{x}{2}}$

First, we rearrange the equation to give

$$
{y}^{′}=2x+{e}^{x/2}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {y}^{′}\,\text{d}x & =\int (2x+{e}^{x/2})\text{d}x \\ y & =2\int x\,\text{d}x+\int {e}^{x/2}\,\text{d}x \\  & =2\cdot \frac{{x}^{2}}{2}+2{e}^{x/2}+C \\  & ={x}^{2}+2{e}^{x/2}+C.\end{aligned}
$$

So our general solution is $y={x}^{2}+2{e}^{x/2}+C.$ To find a particular solution, we substitute the condition $y(0)=2$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}2 & ={0}^{2}+2{e}^{0}+C \\ 2 & =0+2(1)+C \\ C & =0.\end{aligned}
$$

Therefore, our particular solution is

$$
y={x}^{2}+2{e}^{x/2}.
$$

### moderate — generated initial-ordinate variant (repaired source presentation)

Find the particular solution to the differential equation ${y}^{′}-2x={e}^{x/2}$ that satisfies the condition $y(0)=4.$

- $y=x^{2} + \frac{e^{\frac{x}{2}}}{2} + \frac{7}{2}$
- $y=x^{2} + 2 e^{\frac{x}{2}} + 2$
- $y=2 x + e^{\frac{x}{2}} + 3$
- $y=x - \frac{e^{\frac{x}{2}}}{2} + \frac{9}{2}$
- $y=x^{2} + 2 e^{\frac{x}{2}} + 4$

First, we rearrange the equation to give

$$
{y}^{′}=2x+{e}^{x/2}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {y}^{′}\,\text{d}x & =\int (2x+{e}^{x/2})\text{d}x \\ y & =2\int x\,\text{d}x+\int {e}^{x/2}\,\text{d}x \\  & =2\cdot \frac{{x}^{2}}{2}+2{e}^{x/2}+C \\  & ={x}^{2}+2{e}^{x/2}+C.\end{aligned}
$$

So our general solution is $y={x}^{2}+2{e}^{x/2}+C.$ To find a particular solution, we substitute the condition $y(0)=4$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}4 & ={0}^{2}+2{e}^{0}+C \\ 4 & =0+2(1)+C \\ C & =2.\end{aligned}
$$

Therefore, our particular solution is

$$
y={x}^{2}+2{e}^{x/2}+2.
$$

## q-347842 — easy — original raw replay

Find the particular solution to the differential equation $8x-\frac{\text{d}y}{\text{d}x}={x}^{2}$ that satisfies the condition $y(2)=5.$

$y=-\frac{{x}^{3}}{3}\,+${{field-1}}

- $4 x^{2} - \frac{25}{3}$

First, we rearrange the equation to give

$$
\frac{\text{d}y}{\text{d}x}=-{x}^{2}+8x.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (-{x}^{2}+8x)\,\text{d}x \\ y & =-\frac{{x}^{3}}{3}+8\cdot \frac{{x}^{2}}{2}+C \\  & =-\frac{{x}^{3}}{3}+4{x}^{2}+C.\end{aligned}
$$

So our general solution is $y=-\frac{{x}^{3}}{3}+4{x}^{2}+C.$ To find a particular solution, we substitute the condition $y(2)=5$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}y & =-\frac{{x}^{3}}{3}+4{x}^{2}+C \\ 5 & =-\frac{{2}^{3}}{3}+4({2}^{2})+C \\ 5 & =-\frac{8}{3}+16+C \\ 5 & =\frac{40}{3}+C \\ C & =-\frac{25}{3}.\end{aligned}
$$

Therefore, our particular solution is 

$$
y=-\frac{{x}^{3}}{3}+4{x}^{2}-\frac{25}{3}.
$$

### easy — generated initial-ordinate variant (repaired source presentation)

Find the particular solution to the differential equation $8x-\frac{\text{d}y}{\text{d}x}={x}^{2}$ that satisfies the condition $y(2)=7.$

$y=-\frac{{x}^{3}}{3}\,+${{field-1}}

- $4 x^{2} - \frac{19}{3}$

First, we rearrange the equation to give

$$
\frac{\text{d}y}{\text{d}x}=-{x}^{2}+8x.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (-{x}^{2}+8x)\,\text{d}x \\ y & =-\frac{{x}^{3}}{3}+8\cdot \frac{{x}^{2}}{2}+C \\  & =-\frac{{x}^{3}}{3}+4{x}^{2}+C.\end{aligned}
$$

So our general solution is $y=-\frac{{x}^{3}}{3}+4{x}^{2}+C.$ To find a particular solution, we substitute the condition $y(2)=7$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}y & =-\frac{{x}^{3}}{3}+4{x}^{2}+C \\ 7 & =-\frac{{2}^{3}}{3}+4({2}^{2})+C \\ 7 & =-\frac{8}{3}+16+C \\ 7 & =\frac{40}{3}+C \\ C & =- \frac{19}{3}.\end{aligned}
$$

Therefore, our particular solution is 

$$
y=-\frac{{x}^{3}}{3}+4{x}^{2}-\frac{25}{3}+2.
$$

## q-352066 — easy — original raw replay

Find the particular solution to the differential equation $(x-3)^{2}{y}^{′}=8$ that satisfies the condition $y(4)=1.$

$y=\,${{field-1}}

- $9 - \frac{8}{x - 3}$

First, we rearrange the equation to give

$$
{y}^{′}=\frac{8}{(x-3)^{2}}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {y}^{′}\,\text{d}x & =\int \frac{8}{(x-3)^{2}}\,\text{d}x \\ y & =8\int \frac{1}{(x-3)^{2}}\,\text{d}x \\  & =8(-\frac{1}{x-3})+C \\  & =-\frac{8}{x-3}+C.\end{aligned}
$$

So our general solution is $y=-\frac{8}{x-3}+C.$ To find a particular solution, we substitute the condition $y(4)=1$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}1 & =-\frac{8}{4-3}+C \\ 1 & =-8+C \\ C & =9.\end{aligned}
$$

Therefore, our particular solution is

$$
y=-\frac{8}{x-3}+9.
$$

### easy — generated initial-ordinate variant (repaired source presentation)

Find the particular solution to the differential equation $(x-3)^{2}{y}^{′}=8$ that satisfies the condition $y(4)=3.$

$y=\,${{field-1}}

- $11 - \frac{8}{x - 3}$

First, we rearrange the equation to give

$$
{y}^{′}=\frac{8}{(x-3)^{2}}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {y}^{′}\,\text{d}x & =\int \frac{8}{(x-3)^{2}}\,\text{d}x \\ y & =8\int \frac{1}{(x-3)^{2}}\,\text{d}x \\  & =8(-\frac{1}{x-3})+C \\  & =-\frac{8}{x-3}+C.\end{aligned}
$$

So our general solution is $y=-\frac{8}{x-3}+C.$ To find a particular solution, we substitute the condition $y(4)=3$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}3 & =-\frac{8}{4-3}+C \\ 3 & =-8+C \\ C & =11.\end{aligned}
$$

Therefore, our particular solution is

$$
y=-\frac{8}{x-3}+9+2.
$$

## q-352068 — easy — original raw replay

Find the particular solution to the differential equation $\sqrt{x+1}\,{y}^{′}=4$ that satisfies the condition $y(3)=10.$

$y=\,${{field-1}}

- $8 \sqrt{x + 1} - 6$

First, we rearrange the equation to give

$$
{y}^{′}=\frac{4}{\sqrt{x+1}}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {y}^{′}\,\text{d}x & =\int \frac{4}{\sqrt{x+1}}\,\text{d}x \\ y & =4\int (x+1)^{-1/2}\,\text{d}x \\  & =4(2(x+1)^{1/2})+C \\  & =8\sqrt{x+1}+C.\end{aligned}
$$

So our general solution is $y=8\sqrt{x+1}+C.$ To find a particular solution, we substitute the condition $y(3)=10$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}10 & =8\sqrt{3+1}+C \\ 10 & =8(2)+C \\ C & =-6.\end{aligned}
$$

Therefore, our particular solution is

$$
y=8\sqrt{x+1}-6.
$$

### easy — generated initial-ordinate variant (repaired source presentation)

Find the particular solution to the differential equation $\sqrt{x+1}\,{y}^{′}=4$ that satisfies the condition $y(3)=12.$

$y=\,${{field-1}}

- $8 \sqrt{x + 1} - 4$

First, we rearrange the equation to give

$$
{y}^{′}=\frac{4}{\sqrt{x+1}}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {y}^{′}\,\text{d}x & =\int \frac{4}{\sqrt{x+1}}\,\text{d}x \\ y & =4\int (x+1)^{-1/2}\,\text{d}x \\  & =4(2(x+1)^{1/2})+C \\  & =8\sqrt{x+1}+C.\end{aligned}
$$

So our general solution is $y=8\sqrt{x+1}+C.$ To find a particular solution, we substitute the condition $y(3)=12$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}12 & =8\sqrt{3+1}+C \\ 12 & =8(2)+C \\ C & =-4.\end{aligned}
$$

Therefore, our particular solution is

$$
y=8\sqrt{x+1}-6+2.
$$

## q-352075 — easy — original raw replay

Find the particular solution to the differential equation ${f}^{′}(x)+3\operatorname{sin}⁡x=0$ that satisfies the condition $f(0)=2.$

$f(x)=\,${{field-1}}

- $3 \cos{(x )} - 1$

First, we rearrange the equation to give

$$
{f}^{′}(x)=-3\operatorname{sin}⁡x.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =\int (-3\operatorname{sin}⁡x)\,\text{d}x \\ f(x) & =-3\int \operatorname{sin}⁡x\,\text{d}x \\  & =-3(-\operatorname{cos}⁡x)+C \\  & =3\operatorname{cos}⁡x+C.\end{aligned}
$$

So our general solution is $f(x)=3\operatorname{cos}⁡x+C.$ To find a particular solution, we substitute the condition $f(0)=2$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}2 & =3\operatorname{cos}⁡0+C \\ 2 & =3(1)+C \\ C & =-1.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=3\operatorname{cos}⁡x-1.
$$

### easy — generated initial-ordinate variant (repaired source presentation)

Find the particular solution to the differential equation ${f}^{′}(x)+3\operatorname{sin}⁡x=0$ that satisfies the condition $f(0)=4.$

$f(x)=\,${{field-1}}

- $3 \cos{(x )} + 1$

First, we rearrange the equation to give

$$
{f}^{′}(x)=-3\operatorname{sin}⁡x.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =\int (-3\operatorname{sin}⁡x)\,\text{d}x \\ f(x) & =-3\int \operatorname{sin}⁡x\,\text{d}x \\  & =-3(-\operatorname{cos}⁡x)+C \\  & =3\operatorname{cos}⁡x+C.\end{aligned}
$$

So our general solution is $f(x)=3\operatorname{cos}⁡x+C.$ To find a particular solution, we substitute the condition $f(0)=4$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}4 & =3\operatorname{cos}⁡0+C \\ 4 & =3(1)+C \\ C & =1.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=3\operatorname{cos}⁡x-1+2.
$$

## q-50044 — easy — original raw replay

Find the particular solution to the differential equation below that satisfies the condition $y(-1)=2$
 

$$
x\cdot \frac{\text{d}y}{\text{d}x}=6{x}^{3}.
$$

- $y=x^{3} + 3$
- $y=4 - 2 x^{2}$
- $y=6 x^{3} + 8$
- $y=2 x^{3} + 4$
- $y=3 x^{2} - 1$

First, we rearrange the equation to give

$$
\frac{\text{d}y}{\text{d}x}=6{x}^{2}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 6{x}^{2}\,\text{d}x \\ y & =6(\frac{{x}^{3}}{3})\,\text{d}x \\  & =2{x}^{3}+C.\end{aligned}
$$

So our general solution is $y=2{x}^{3}+C.$ To find a particular solution, we substitute the condition $y(-1)=2$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}y & =2{x}^{3}+C \\ 2 & =2(-1)^{3}+C \\ 2 & =-2+C \\ C & =4.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=2{x}^{3}+4.
$$

### easy — generated initial-ordinate variant (repaired source presentation)

Find the particular solution to the differential equation below that satisfies the condition $y(-1)=4$
 

$$
x\cdot \frac{\text{d}y}{\text{d}x}=6{x}^{3}.
$$

- $y=2 x^{3} + 6$
- $y=3 x^{2} + 1$
- $y=x^{3} + 5$
- $y=6 x^{3} + 10$
- $y=6 - 2 x^{2}$

First, we rearrange the equation to give

$$
\frac{\text{d}y}{\text{d}x}=6{x}^{2}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int 6{x}^{2}\,\text{d}x \\ y & =6(\frac{{x}^{3}}{3})+C \\  & =2{x}^{3}+C.\end{aligned}
$$

So our general solution is $y=2{x}^{3}+C.$ To find a particular solution, we substitute the condition $y(-1)=4$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}y & =2{x}^{3}+C \\ 4 & =2(-1)^{3}+C \\ 4 & =-2+C \\ C & =6.\end{aligned}
$$

Therefore, our particular solution is

$$
y=2{x}^{3}+4+2.
$$

## q-50092 — easy — original raw replay

Find the particular solution to the differential equation below that satisfies the condition $y(1)=1.$

$$
2x+\frac{\text{d}y}{\text{d}x}={x}^{2}+4x.
$$

- $y=x^{3} + 2 x^{2} - 2$
- $y=\frac{x^{3}}{3} + x^{2} - \frac{1}{3}$
- $y=x^{3} + x^{2} - 1$
- $y=\frac{x^{3}}{3} + 2 x^{2} - \frac{4}{3}$
- $y=\frac{x^{3}}{3} - x^{2} + \frac{5}{3}$

First, we rearrange the equation to give

$$
\frac{\text{d}y}{\text{d}x}={x}^{2}+2x.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int ({x}^{2}+2x)\,\text{d}x \\ y & =\frac{{x}^{3}}{3}+2\cdot \frac{{x}^{2}}{2}+C \\  & =\frac{{x}^{3}}{3}+{x}^{2}+C.\end{aligned}
$$

So our general solution is $y=\frac{{x}^{3}}{3}+{x}^{2}+C.$ To find a particular solution, we substitute the condition $y(1)=1$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}y & =\frac{{x}^{3}}{3}+{x}^{2}+C \\ 1 & =\frac{{1}^{3}}{3}+{1}^{2}+C \\ 1 & =\frac{4}{3}+C \\ C & =-\frac{1}{3}.\end{aligned}
$$

Therefore, our particular solution is

$$
y=\frac{{x}^{3}}{3}+{x}^{2}-\frac{1}{3}.
$$

### easy — generated initial-ordinate variant (repaired source presentation)

Find the particular solution to the differential equation below that satisfies the condition $y(1)=3.$

$$
2x+\frac{\text{d}y}{\text{d}x}={x}^{2}+4x.
$$

- $y=\frac{x^{3}}{3} + 2 x^{2} + \frac{2}{3}$
- $y=\frac{x^{3}}{3} - x^{2} + \frac{11}{3}$
- $y=x^{3} + 2 x^{2}$
- $y=x^{3} + x^{2} + 1$
- $y=\frac{x^{3}}{3} + x^{2} + \frac{5}{3}$

First, we rearrange the equation to give

$$
\frac{\text{d}y}{\text{d}x}={x}^{2}+2x.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int ({x}^{2}+2x)\,\text{d}x \\ y & =\frac{{x}^{3}}{3}+2\cdot \frac{{x}^{2}}{2}+C \\  & =\frac{{x}^{3}}{3}+{x}^{2}+C.\end{aligned}
$$

So our general solution is $y=\frac{{x}^{3}}{3}+{x}^{2}+C.$ To find a particular solution, we substitute the condition $y(1)=3$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}y & =\frac{{x}^{3}}{3}+{x}^{2}+C \\ 3 & =\frac{{1}^{3}}{3}+{1}^{2}+C \\ 3 & =\frac{4}{3}+C \\ C & =\frac{5}{3}.\end{aligned}
$$

Therefore, our particular solution is

$$
y=\frac{{x}^{3}}{3}+{x}^{2}-\frac{1}{3}+2.
$$

## q-50159 — easy — original raw replay

Find the particular solution to the differential equation below that satisfies the condition $f(0)=-2.$

$$
(1+2x){f}^{′}(x)-2=0.
$$

- $f(x)=\ln{(|{2 x + 1}| )} - 1$
- $f(x)=\ln{(|{2 x + 1}| )} - 2$
- $f(x)=2 \ln{(|{2 x + 1}| )} - 2$
- $f(x)=2 x^{2} + x - 2$
- $f(x)=2 x - 2$

First, we rearrange the equation to give

$$
{f}^{′}(x)=\frac{2}{1+2x}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =\int \frac{2}{1+2x}\,\text{d}x \\ f(x) & =\int \frac{2}{1+2x}\,\text{d}x.\end{aligned}
$$

Let $u=(1+2x).$ Then $\text{d}u=2\,\text{d}x.$ Therefore,

$$
\begin{aligned}f(x) & =\int \frac{2}{1+2x}\,\text{d}x \\  & =\int \frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|+C \\  & =\operatorname{ln}⁡|1+2x|+C.\end{aligned}
$$

So our general solution is $f(x)=\operatorname{ln}⁡|1+2x|+C.$ To find a particular solution, we substitute the condition $f(0)=-2$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}f(x) & =\operatorname{ln}⁡|1+2x|+C \\ -2 & =\operatorname{ln}⁡|1+2\cdot 0|+C \\ -2 & =\operatorname{ln}⁡|1|+C \\ C & =-2.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=\operatorname{ln}⁡|1+2x|-2.
$$

### easy — generated initial-ordinate variant (repaired source presentation)

Find the particular solution to the differential equation below that satisfies the condition $f(0)=0.$

$$
(1+2x){f}^{′}(x)-2=0.
$$

- $f(x)=2 x^{2} + x$
- $f(x)=2 x$
- $f(x)=\ln{(|{2 x + 1}| )} + 1$
- $f(x)=2 \ln{(|{2 x + 1}| )}$
- $f(x)=\ln{(|{2 x + 1}| )}$

First, we rearrange the equation to give

$$
{f}^{′}(x)=\frac{2}{1+2x}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =\int \frac{2}{1+2x}\,\text{d}x \\ f(x) & =\int \frac{2}{1+2x}\,\text{d}x.\end{aligned}
$$

Let $u=(1+2x).$ Then $\text{d}u=2\,\text{d}x.$ Therefore,

$$
\begin{aligned}f(x) & =\int \frac{2}{1+2x}\,\text{d}x \\  & =\int \frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|+C \\  & =\operatorname{ln}⁡|1+2x|+C.\end{aligned}
$$

So our general solution is $f(x)=\operatorname{ln}⁡|1+2x|+C.$ To find a particular solution, we substitute the condition $f(0)=0$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}f(x) & =\operatorname{ln}⁡|1+2x|+C \\ 0 & =\operatorname{ln}⁡|1+2\cdot 0|+C \\ 0 & =\operatorname{ln}⁡|1|+C \\ C & =0.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=\operatorname{ln}⁡|1+2x|-2+2.
$$

## q-8311 — easy — original raw replay

Find the specific solution to the differential equation $\frac{\text{d}y}{\text{d}x}+4=0$ given that $y(-1)=4.$

- $y=- 4 x$
- $y=4$
- $y=4 x^{2}$
- $y=- 2 x - 2$
- $y=-4$

First, we rearrange the equation to give

$$
\frac{\text{d}y}{\text{d}x}=-4.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (-4)\,\text{d}x \\ \int \,\text{d}y & =\int (-4)\,\text{d}x \\ y & =-4x+C\,.\end{aligned}
$$

So our general solution is $y=-4x+C.$ To find a particular solution, we substitute the condition $y(-1)=4$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}4 & =-4\cdot (-1)+C \\ 4 & =4+C \\ 0 & =C\,.\end{aligned}
$$

Therefore, our particular solution is

$$
y=-4x\,.
$$

### easy — generated initial-ordinate variant (repaired source presentation)

Find the specific solution to the differential equation $\frac{\text{d}y}{\text{d}x}+4=0$ given that $y(-1)=6.$

- $y=- 2 x$
- $y=-2$
- $y=2 - 4 x$
- $y=4 x^{2} + 2$
- $y=6$

First, we rearrange the equation to give

$$
\frac{\text{d}y}{\text{d}x}=-4.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (-4)\,\text{d}x \\ \int \,\text{d}y & =\int (-4)\,\text{d}x \\ y & =-4x+C\,.\end{aligned}
$$

So our general solution is $y=-4x+C.$ To find a particular solution, we substitute the condition $y(-1)=6$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}6 & =-4\cdot (-1)+C \\ 6 & =4+C \\ 2 & =C\,.\end{aligned}
$$

Therefore, our particular solution is

$$
y=-4x+2.
$$

## easy authored peer 1

Find the particular solution to the differential equation $f'(x)=2 \cos{(x )}$ that satisfies the condition $f(0)=8.$

$f(x)=\,${{field-1}}

- $2 \sin{(x )} + 8$

The derivative is already isolated, so we have

$$
f'(x)=2 \cos{(x )}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int f'(x)\,\text{d}x & =\int (2 \cos{(x )})\,\text{d}x \\ f(x) & =\int (2 \cos{(x )})\,\text{d}x \\ & =(2)(\sin{(x )})+C \\ & =2 \sin{(x )}+C.\end{aligned}
$$

So our general solution is $f(x)=2 \sin{(x )}+C.$ To find a particular solution, we substitute the condition $f(0)=8$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}8 & =(2 \sin{((0) )})+C \\ 8 & =(0)+C \\ C & =8.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=2 \sin{(x )} + 8.
$$

## easy authored peer 2

Find the particular solution to the differential equation $f'(x)=2 \cos{(x )}$ that satisfies the condition $f(0)=8.$

- $f(x)=8 - 2 \sin{(x )}$
- $f(x)=2 \sin{(x )}$
- $f(x)=2 \sin{(x )} + 8$
- $f(x)=\sin{(x )} + 8$
- $f(x)=2 \cos{(x )} + 6$

The derivative is already isolated, so we have

$$
f'(x)=2 \cos{(x )}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int f'(x)\,\text{d}x & =\int (2 \cos{(x )})\,\text{d}x \\ f(x) & =\int (2 \cos{(x )})\,\text{d}x \\ & =(2)(\sin{(x )})+C \\ & =2 \sin{(x )}+C.\end{aligned}
$$

So our general solution is $f(x)=2 \sin{(x )}+C.$ To find a particular solution, we substitute the condition $f(0)=8$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}8 & =(2 \sin{((0) )})+C \\ 8 & =(0)+C \\ C & =8.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=2 \sin{(x )} + 8.
$$

## easy authored peer 3

Find the particular solution to the differential equation $f'(x)=- 4 \cos{(x )}$ that satisfies the condition $f(0)=-5.$

$f(x)=\,${{field-1}}

- $- 4 \sin{(x )} - 5$

The derivative is already isolated, so we have

$$
f'(x)=- 4 \cos{(x )}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int f'(x)\,\text{d}x & =\int (- 4 \cos{(x )})\,\text{d}x \\ f(x) & =\int (- 4 \cos{(x )})\,\text{d}x \\ & =(-4)(\sin{(x )})+C \\ & =- 4 \sin{(x )}+C.\end{aligned}
$$

So our general solution is $f(x)=- 4 \sin{(x )}+C.$ To find a particular solution, we substitute the condition $f(0)=-5$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}-5 & =(- 4 \sin{((0) )})+C \\ -5 & =(0)+C \\ C & =-5.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=- 4 \sin{(x )} - 5.
$$

## easy authored peer 4

Find the particular solution to the differential equation $f'(x)=- 4 \cos{(x )}$ that satisfies the condition $f(0)=-5.$

- $f(x)=4 \sin{(x )} - 5$
- $f(x)=- 4 \cos{(x )} - 1$
- $f(x)=- 2 \sin{(x )} - 5$
- $f(x)=- 4 \sin{(x )} - 5$
- $f(x)=- 4 \sin{(x )}$

The derivative is already isolated, so we have

$$
f'(x)=- 4 \cos{(x )}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int f'(x)\,\text{d}x & =\int (- 4 \cos{(x )})\,\text{d}x \\ f(x) & =\int (- 4 \cos{(x )})\,\text{d}x \\ & =(-4)(\sin{(x )})+C \\ & =- 4 \sin{(x )}+C.\end{aligned}
$$

So our general solution is $f(x)=- 4 \sin{(x )}+C.$ To find a particular solution, we substitute the condition $f(0)=-5$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}-5 & =(- 4 \sin{((0) )})+C \\ -5 & =(0)+C \\ C & =-5.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=- 4 \sin{(x )} - 5.
$$

## moderate authored peer 1

Find the particular solution to the differential equation $f'(x)=2 x+e^{x}$ that satisfies the condition $f(0)=8.$

$f(x)=\,${{field-1}}

- $x^{2} + e^{x} + 7$

The derivative is already isolated, so we have

$$
f'(x)=2 x+e^{x}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int f'(x)\,\text{d}x & =\int (2 x+e^{x})\,\text{d}x \\ f(x) & =\int (2 x)\,\text{d}x + \int (e^{x})\,\text{d}x \\ & =(2)(\frac{x^{2}}{2}) + (1)(e^{x})+C \\ & =x^{2}+e^{x}+C.\end{aligned}
$$

So our general solution is $f(x)=x^{2}+e^{x}+C.$ To find a particular solution, we substitute the condition $f(0)=8$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}8 & =((0)^{2}) + (e^{(0)})+C \\ 8 & =(0) + (1)+C \\ C & =7.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=x^{2} + e^{x} + 7.
$$

## moderate authored peer 2

Find the particular solution to the differential equation $f'(x)=2 x+e^{x}$ that satisfies the condition $f(0)=8.$

- $f(x)=- x^{2} - e^{x} + 9$
- $f(x)=x^{2} + e^{x}$
- $f(x)=x^{2} + e^{x} + 7$
- $f(x)=\frac{x^{2}}{2} + \frac{e^{x}}{2} + \frac{15}{2}$
- $f(x)=2 x + e^{x} + 7$

The derivative is already isolated, so we have

$$
f'(x)=2 x+e^{x}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int f'(x)\,\text{d}x & =\int (2 x+e^{x})\,\text{d}x \\ f(x) & =\int (2 x)\,\text{d}x + \int (e^{x})\,\text{d}x \\ & =(2)(\frac{x^{2}}{2}) + (1)(e^{x})+C \\ & =x^{2}+e^{x}+C.\end{aligned}
$$

So our general solution is $f(x)=x^{2}+e^{x}+C.$ To find a particular solution, we substitute the condition $f(0)=8$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}8 & =((0)^{2}) + (e^{(0)})+C \\ 8 & =(0) + (1)+C \\ C & =7.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=x^{2} + e^{x} + 7.
$$

## moderate authored peer 3

Find the particular solution to the differential equation $f'(x)=- 4 x+2 e^{x}$ that satisfies the condition $f(0)=-5.$

$f(x)=\,${{field-1}}

- $- 2 x^{2} + 2 e^{x} - 7$

The derivative is already isolated, so we have

$$
f'(x)=- 4 x+2 e^{x}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int f'(x)\,\text{d}x & =\int (- 4 x+2 e^{x})\,\text{d}x \\ f(x) & =\int (- 4 x)\,\text{d}x + \int (2 e^{x})\,\text{d}x \\ & =(-4)(\frac{x^{2}}{2}) + (2)(e^{x})+C \\ & =- 2 x^{2}+2 e^{x}+C.\end{aligned}
$$

So our general solution is $f(x)=- 2 x^{2}+2 e^{x}+C.$ To find a particular solution, we substitute the condition $f(0)=-5$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}-5 & =(- 2 (0)^{2}) + (2 e^{(0)})+C \\ -5 & =(0) + (2)+C \\ C & =-7.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=- 2 x^{2} + 2 e^{x} - 7.
$$

## moderate authored peer 4

Find the particular solution to the differential equation $f'(x)=- 4 x+2 e^{x}$ that satisfies the condition $f(0)=-5.$

- $f(x)=2 x^{2} - 2 e^{x} - 3$
- $f(x)=- 4 x + 2 e^{x} - 7$
- $f(x)=- x^{2} + e^{x} - 6$
- $f(x)=- 2 x^{2} + 2 e^{x} - 7$
- $f(x)=- 2 x^{2} + 2 e^{x}$

The derivative is already isolated, so we have

$$
f'(x)=- 4 x+2 e^{x}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int f'(x)\,\text{d}x & =\int (- 4 x+2 e^{x})\,\text{d}x \\ f(x) & =\int (- 4 x)\,\text{d}x + \int (2 e^{x})\,\text{d}x \\ & =(-4)(\frac{x^{2}}{2}) + (2)(e^{x})+C \\ & =- 2 x^{2}+2 e^{x}+C.\end{aligned}
$$

So our general solution is $f(x)=- 2 x^{2}+2 e^{x}+C.$ To find a particular solution, we substitute the condition $f(0)=-5$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}-5 & =(- 2 (0)^{2}) + (2 e^{(0)})+C \\ -5 & =(0) + (2)+C \\ C & =-7.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=- 2 x^{2} + 2 e^{x} - 7.
$$

## hard authored peer 1

Find the particular solution to the differential equation $f'(x)=2 x^{2}+e^{x}- 4 \cos{(x )}$ that satisfies the condition $f(0)=8.$

$f(x)=\,${{field-1}}

- $\frac{2 x^{3}}{3} + e^{x} - 4 \sin{(x )} + 7$

The derivative is already isolated, so we have

$$
f'(x)=2 x^{2}+e^{x}- 4 \cos{(x )}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int f'(x)\,\text{d}x & =\int (2 x^{2}+e^{x}- 4 \cos{(x )})\,\text{d}x \\ f(x) & =\int (2 x^{2})\,\text{d}x + \int (e^{x})\,\text{d}x + \int (- 4 \cos{(x )})\,\text{d}x \\ & =(2)(\frac{x^{3}}{3}) + (1)(e^{x}) + (-4)(\sin{(x )})+C \\ & =\frac{2 x^{3}}{3}+e^{x}- 4 \sin{(x )}+C.\end{aligned}
$$

So our general solution is $f(x)=\frac{2 x^{3}}{3}+e^{x}- 4 \sin{(x )}+C.$ To find a particular solution, we substitute the condition $f(0)=8$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}8 & =(\frac{2 (0)^{3}}{3}) + (e^{(0)}) + (- 4 \sin{((0) )})+C \\ 8 & =(0) + (1) + (0)+C \\ C & =7.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=\frac{2 x^{3}}{3} + e^{x} - 4 \sin{(x )} + 7.
$$

## hard authored peer 2

Find the particular solution to the differential equation $f'(x)=2 x^{2}+e^{x}- 4 \cos{(x )}$ that satisfies the condition $f(0)=8.$

- $f(x)=- \frac{2 x^{3}}{3} - e^{x} + 4 \sin{(x )} + 9$
- $f(x)=\frac{2 x^{3}}{3} + e^{x} - 4 \sin{(x )}$
- $f(x)=\frac{2 x^{3}}{3} + e^{x} - 4 \sin{(x )} + 7$
- $f(x)=\frac{x^{3}}{3} + \frac{e^{x}}{2} - 2 \sin{(x )} + \frac{15}{2}$
- $f(x)=2 x^{2} + e^{x} - 4 \cos{(x )} + 11$

The derivative is already isolated, so we have

$$
f'(x)=2 x^{2}+e^{x}- 4 \cos{(x )}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int f'(x)\,\text{d}x & =\int (2 x^{2}+e^{x}- 4 \cos{(x )})\,\text{d}x \\ f(x) & =\int (2 x^{2})\,\text{d}x + \int (e^{x})\,\text{d}x + \int (- 4 \cos{(x )})\,\text{d}x \\ & =(2)(\frac{x^{3}}{3}) + (1)(e^{x}) + (-4)(\sin{(x )})+C \\ & =\frac{2 x^{3}}{3}+e^{x}- 4 \sin{(x )}+C.\end{aligned}
$$

So our general solution is $f(x)=\frac{2 x^{3}}{3}+e^{x}- 4 \sin{(x )}+C.$ To find a particular solution, we substitute the condition $f(0)=8$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}8 & =(\frac{2 (0)^{3}}{3}) + (e^{(0)}) + (- 4 \sin{((0) )})+C \\ 8 & =(0) + (1) + (0)+C \\ C & =7.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=\frac{2 x^{3}}{3} + e^{x} - 4 \sin{(x )} + 7.
$$

## hard authored peer 3

Find the particular solution to the differential equation $f'(x)=- 4 x^{2}+2 e^{x}- 4 \cos{(x )}$ that satisfies the condition $f(0)=-5.$

$f(x)=\,${{field-1}}

- $- \frac{4 x^{3}}{3} + 2 e^{x} - 4 \sin{(x )} - 7$

The derivative is already isolated, so we have

$$
f'(x)=- 4 x^{2}+2 e^{x}- 4 \cos{(x )}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int f'(x)\,\text{d}x & =\int (- 4 x^{2}+2 e^{x}- 4 \cos{(x )})\,\text{d}x \\ f(x) & =\int (- 4 x^{2})\,\text{d}x + \int (2 e^{x})\,\text{d}x + \int (- 4 \cos{(x )})\,\text{d}x \\ & =(-4)(\frac{x^{3}}{3}) + (2)(e^{x}) + (-4)(\sin{(x )})+C \\ & =- \frac{4 x^{3}}{3}+2 e^{x}- 4 \sin{(x )}+C.\end{aligned}
$$

So our general solution is $f(x)=- \frac{4 x^{3}}{3}+2 e^{x}- 4 \sin{(x )}+C.$ To find a particular solution, we substitute the condition $f(0)=-5$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}-5 & =(- \frac{4 (0)^{3}}{3}) + (2 e^{(0)}) + (- 4 \sin{((0) )})+C \\ -5 & =(0) + (2) + (0)+C \\ C & =-7.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=- \frac{4 x^{3}}{3} + 2 e^{x} - 4 \sin{(x )} - 7.
$$

## hard authored peer 4

Find the particular solution to the differential equation $f'(x)=- 4 x^{2}+2 e^{x}- 4 \cos{(x )}$ that satisfies the condition $f(0)=-5.$

- $f(x)=\frac{4 x^{3}}{3} - 2 e^{x} + 4 \sin{(x )} - 3$
- $f(x)=- 4 x^{2} + 2 e^{x} - 4 \cos{(x )} - 3$
- $f(x)=- \frac{2 x^{3}}{3} + e^{x} - 2 \sin{(x )} - 6$
- $f(x)=- \frac{4 x^{3}}{3} + 2 e^{x} - 4 \sin{(x )} - 7$
- $f(x)=- \frac{4 x^{3}}{3} + 2 e^{x} - 4 \sin{(x )}$

The derivative is already isolated, so we have

$$
f'(x)=- 4 x^{2}+2 e^{x}- 4 \cos{(x )}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int f'(x)\,\text{d}x & =\int (- 4 x^{2}+2 e^{x}- 4 \cos{(x )})\,\text{d}x \\ f(x) & =\int (- 4 x^{2})\,\text{d}x + \int (2 e^{x})\,\text{d}x + \int (- 4 \cos{(x )})\,\text{d}x \\ & =(-4)(\frac{x^{3}}{3}) + (2)(e^{x}) + (-4)(\sin{(x )})+C \\ & =- \frac{4 x^{3}}{3}+2 e^{x}- 4 \sin{(x )}+C.\end{aligned}
$$

So our general solution is $f(x)=- \frac{4 x^{3}}{3}+2 e^{x}- 4 \sin{(x )}+C.$ To find a particular solution, we substitute the condition $f(0)=-5$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}-5 & =(- \frac{4 (0)^{3}}{3}) + (2 e^{(0)}) + (- 4 \sin{((0) )})+C \\ -5 & =(0) + (2) + (0)+C \\ C & =-7.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=- \frac{4 x^{3}}{3} + 2 e^{x} - 4 \sin{(x )} - 7.
$$

