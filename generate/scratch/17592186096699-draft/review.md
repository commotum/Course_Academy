# Basis-2275 particular-solution draft review

Original replay preserves missing attributes and documented source errors. Banks use standard-TeX notation from scaling recipes. All observed banks are evidence-only. Independent inventory is separately identified.

## q-119078 — unrated original raw replay

Find the particular solution to the differential equation $(x - 1)^{2}y^{′} =-2$ that satisfies the condition $y(2) = 1$.

- $y=-1 + \frac{2}{x - 1}$
- $y=\frac{1}{2} + \frac{1}{x - 1}$
- $y=\frac{3}{2} - \frac{1}{2 x - 2}$
- $y=3 + \frac{2}{x - 1}$
- $y=\frac{1}{x - 1}$

[No captured worked solution.]

### easy generated observed-pattern variant (scale 2; repaired and ineligible)

Find the particular solution to the differential equation ${y}^{′} x^{2} - 2 {y}^{′} x + {y}^{′}=-4$ that satisfies the condition $y(2) = 2$.

- $y=-2 + \frac{4}{x - 1}$
- $y=1 + \frac{2}{x - 1}$
- $y=3 - \frac{2}{2 x - 2}$
- $y=6 + \frac{4}{x - 1}$
- $y=\frac{2}{x - 1}$

First, we rearrange the equation to give

$$
y'=- \frac{4}{(x - 1)^{2}}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int y'\,\text{d}x & =\int (- \frac{4}{(x - 1)^{2}})\,\text{d}x \\ y & =(-4)\int (\frac{1}{(x - 1)^{2}})\,\text{d}x \\ & =(-4)(- \frac{1}{x - 1})+C \\ & =\frac{4}{x - 1}+C.\end{aligned}
$$

So our general solution is $y=\frac{4}{x - 1}+C.$ To find a particular solution, we substitute the condition $y(2)=2$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}2 & =(\frac{4}{(2) - 1})+C \\ 2 & =4+C \\ C & =-2.\end{aligned}
$$

Therefore, our particular solution is

$$
y=-2 + \frac{4}{x - 1}.
$$

### easy generated normal family variant (authored method bank)

Find the particular solution to the differential equation ${y}^{′} x^{2} - 2 {y}^{′} x + {y}^{′}=4$ that satisfies the condition $y(2) = 7$.

- $y=3 + \frac{4}{x - 1}$
- $y=4 - \frac{4}{x - 1}$
- $y=11 - \frac{4}{x - 1}$
- $y=3 - \frac{4}{x - 1}$
- $y=3 + \frac{4}{(x - 1)^{2}}$

First, we rearrange the equation to give

$$
y'=\frac{4}{(x - 1)^{2}}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int y'\,\text{d}x & =\int (\frac{4}{(x - 1)^{2}})\,\text{d}x \\ y & =(4)\int (\frac{1}{(x - 1)^{2}})\,\text{d}x \\ & =(4)(- \frac{1}{x - 1})+C \\ & =- \frac{4}{x - 1}+C.\end{aligned}
$$

So our general solution is $y=- \frac{4}{x - 1}+C.$ To find a particular solution, we substitute the condition $y(2)=7$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}7 & =(- \frac{4}{(2) - 1})+C \\ 7 & =-4+C \\ C & =11.\end{aligned}
$$

Therefore, our particular solution is

$$
y=11 - \frac{4}{x - 1}.
$$

## q-49942 — unrated original raw replay

Find the particular solution to the differential equation below that satisfies the condition $f(0) =-1$.

$2f^{′}(x) + e^{x} = 0$.

- $f(x)=1 - \frac{e^{x}}{2}$
- $f(x)=e^{x} - 2$
- $f(x)=\frac{e^{x}}{2} - 1$
- $f(x)=- \frac{e^{x}}{2} - \frac{1}{2}$
- $f(x)=\frac{e^{x}}{2} - \frac{3}{2}$

[No captured worked solution.]

### easy generated observed-pattern variant (scale 2; repaired and ineligible)

Find the particular solution to the differential equation below that satisfies the condition $f(0) =-2$.

$2 {f}^{′}(x) + 2 e^{x}=0$.

- $f(x)=2 - e^{x}$
- $f(x)=2 e^{x} - 4$
- $f(x)=e^{x} - 2$
- $f(x)=- e^{x} - 1$
- $f(x)=e^{x} - 3$

First, we rearrange the equation to give

$$
f'(x)=- e^{x}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int f'(x)\,\text{d}x & =\int (- e^{x})\,\text{d}x \\ f(x) & =(-1)\int (e^{x})\,\text{d}x \\ & =(-1)(e^{x})+C \\ & =- e^{x}+C.\end{aligned}
$$

So our general solution is $f(x)=- e^{x}+C.$ To find a particular solution, we substitute the condition $f(0)=-2$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}-2 & =(- e^{(0)})+C \\ -2 & =-1+C \\ C & =-1.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=- e^{x} - 1.
$$

### easy generated normal family variant (authored method bank)

Find the particular solution to the differential equation below that satisfies the condition $f(0) =7$.

$2 {f}^{′}(x) - 2 e^{x}=0$.

- $f(x)=8 - e^{x}$
- $f(x)=e^{x} - 1$
- $f(x)=e^{x} + 6$
- $f(x)=e^{x} + 8$
- $f(x)=2 e^{x} + 5$

First, we rearrange the equation to give

$$
f'(x)=e^{x}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int f'(x)\,\text{d}x & =\int (e^{x})\,\text{d}x \\ f(x) & =(1)\int (e^{x})\,\text{d}x \\ & =(1)(e^{x})+C \\ & =e^{x}+C.\end{aligned}
$$

So our general solution is $f(x)=e^{x}+C.$ To find a particular solution, we substitute the condition $f(0)=7$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}7 & =(e^{(0)})+C \\ 7 & =1+C \\ C & =6.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=e^{x} + 6.
$$

## q-119045 — easy original raw replay

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

### easy generated observed-pattern variant (scale 2; repaired and ineligible)

Find the particular solution to the differential equation ${f}^{′}(x) + 4 \cos{(x )}=0$ that satisfies the condition $f(0)=-2.$

- $f(x)=\sin{(x )} - 2$
- $f(x)=4 \cos{(x )} - 6$
- $f(x)=- 4 \sin{(x )} - 2$
- $f(x)=2 - 4 \cos{(x )}$
- $f(x)=4 \sin{(x )} - 6$

First, we rearrange the equation to give

$$
{f}^{′}(x)=(2)\cdot(-2\operatorname{cos}⁡x).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =(2)\cdot(\int (-2\operatorname{cos}⁡x)\,\text{d}x )\\ f(x) & =(2)\cdot(-2\int \operatorname{cos}⁡x\,\text{d}x )\\  & =(2)\cdot(-2\operatorname{sin}⁡x)+C.\end{aligned}
$$

So our general solution is $f(x)=(2)\cdot(-2\operatorname{sin}⁡x)+C.$ To find a particular solution, we substitute the condition $f(0)=-2$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}-2 & =(2)\cdot(-2\operatorname{sin}⁡0)+C \\ -2 & =(2)\cdot(-2(0))+C \\ C & =-2.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=- 4 \sin{(x )} - 2.
$$

### easy generated normal family variant (authored method bank)

Find the particular solution to the differential equation ${f}^{′}(x) - 4 \cos{(x )}=0$ that satisfies the condition $f(0)=7.$

- $f(x)=7 - 4 \sin{(x )}$
- $f(x)=4 \sin{(x )}$
- $f(x)=4 \sin{(x )} + 7$
- $f(x)=\frac{\sin{(x )}}{4} + 7$
- $f(x)=4 \cos{(x )} + 3$

First, we rearrange the equation to give

$$
{f}^{′}(x)=(-2)\cdot(-2\operatorname{cos}⁡x).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =(-2)\cdot(\int (-2\operatorname{cos}⁡x)\,\text{d}x )\\ f(x) & =(-2)\cdot(-2\int \operatorname{cos}⁡x\,\text{d}x )\\  & =(-2)\cdot(-2\operatorname{sin}⁡x)+C.\end{aligned}
$$

So our general solution is $f(x)=(-2)\cdot(-2\operatorname{sin}⁡x)+C.$ To find a particular solution, we substitute the condition $f(0)=7$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}7 & =(-2)\cdot(-2\operatorname{sin}⁡0)+C \\ 7 & =(-2)\cdot(-2(0))+C \\ C & =7.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=4 \sin{(x )} + 7.
$$

## q-119046 — easy original raw replay

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

### easy generated observed-pattern variant (scale 2; repaired and ineligible)

Find the particular solution to the differential equation ${f}^{′}(x) - 8 x=2$ that satisfies the condition $f(1)=-2.$

- $f(x)=2 x^{2} + 4 x - 8$
- $f(x)=2 x^{2} - 4 x$
- $f(x)=4 x^{2} + 2 x - 8$
- $f(x)=4 x^{2} + 2 x - 2$
- $f(x)=4 x^{2} + 6 x - 12$

First, we rearrange the equation to give

$$
{f}^{′}(x)=(2)\cdot(4x+1).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =(2)\cdot(\int (4x+1)\,\text{d}x )\\ f(x) & =(2)\cdot(4\int x\,\text{d}x+\int \text{d}x )\\  & =(2)\cdot(4(\frac{1}{2}{x}^{2})+x)+C \\  & =(2)\cdot(2{x}^{2}+x)+C.\end{aligned}
$$

So our general solution is $f(x)=(2)\cdot(2{x}^{2}+x)+C.$ To find a particular solution, we substitute the condition $f(1)=-2$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}-2 & =(2)\cdot(2(1)^{2}+1)+C \\ -2 & =(2)\cdot(2+1)+C \\ C & =-8.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=4 x^{2} + 2 x - 8.
$$

### easy generated normal family variant (authored method bank)

Find the particular solution to the differential equation ${f}^{′}(x) + 8 x=-2$ that satisfies the condition $f(1)=7.$

- $f(x)=4 x^{2} + 2 x + 1$
- $f(x)=- 4 x^{2} - 2 x + 6$
- $f(x)=- 4 x^{2} - 2 x + 13$
- $f(x)=- 8 x^{2} - 2 x + 17$
- $f(x)=15 - 8 x$

First, we rearrange the equation to give

$$
{f}^{′}(x)=(-2)\cdot(4x+1).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =(-2)\cdot(\int (4x+1)\,\text{d}x )\\ f(x) & =(-2)\cdot(4\int x\,\text{d}x+\int \text{d}x )\\  & =(-2)\cdot(4(\frac{1}{2}{x}^{2})+x)+C \\  & =(-2)\cdot(2{x}^{2}+x)+C.\end{aligned}
$$

So our general solution is $f(x)=(-2)\cdot(2{x}^{2}+x)+C.$ To find a particular solution, we substitute the condition $f(1)=7$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}7 & =(-2)\cdot(2(1)^{2}+1)+C \\ 7 & =(-2)\cdot(2+1)+C \\ C & =13.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=- 4 x^{2} - 2 x + 13.
$$

## q-119075 — moderate original raw replay

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

### moderate generated observed-pattern variant (scale 2; repaired and ineligible)

Find the particular solution to the differential equation ${y}^{′} + 2 e^{- 2 x}=16 x$ that satisfies the condition $y(0)=2.$

- $y=4 x^{2} + 1 + e^{- 2 x}$
- $y=16 x^{2} - 2 + 4 e^{- 2 x}$
- $y=4 x^{2} + 6 - 4 e^{- 2 x}$
- $y=8 x^{2} + 1 + e^{- 2 x}$
- $y=8 x^{2} - 3 + e^{- 2 x}$

First, we rearrange the equation to give

$$
{y}^{′}=(2)\cdot(8x-{e}^{-2x}).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {y}^{′}\,\text{d}x & =(2)\cdot(\int (8x-{e}^{-2x})\,\text{d}x )\\ y & =(2)\cdot(8\int x\,\text{d}x-\int {e}^{-2x}\,\text{d}x )\\  & =(2)\cdot(8(\frac{{x}^{2}}{2})-(-\frac{{e}^{-2x}}{2}))+C \\  & =(2)\cdot(4{x}^{2}+\frac{{e}^{-2x}}{2})+C.\end{aligned}
$$

So our general solution is $y=(2)\cdot(4{x}^{2}+\frac{{e}^{-2x}}{2})+C.$ To find a particular solution, we substitute the condition $y(0)=2$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}2 & =(2)\cdot(4(0)^{2}+\frac{{e}^{-2(0)}}{2})+C \\ 2 & =(2)\cdot(0+\frac{1}{2})+C \\ C & =1.\end{aligned}
$$

Therefore, our particular solution is

$$
y=8 x^{2} + 1 + e^{- 2 x}.
$$

### moderate generated normal family variant (authored method bank)

Find the particular solution to the differential equation ${y}^{′} - 2 e^{- 2 x}=- 16 x$ that satisfies the condition $y(0)=7.$

- $y=8 x^{2} + 6 + e^{- 2 x}$
- $y=- 8 x^{2} + 1 - e^{- 2 x}$
- $y=- 8 x^{2} + 8 - e^{- 2 x}$
- $y=- 8 x^{2} + 11 - 4 e^{- 2 x}$
- $y=- 16 x + 5 + 2 e^{- 2 x}$

First, we rearrange the equation to give

$$
{y}^{′}=(-2)\cdot(8x-{e}^{-2x}).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {y}^{′}\,\text{d}x & =(-2)\cdot(\int (8x-{e}^{-2x})\,\text{d}x )\\ y & =(-2)\cdot(8\int x\,\text{d}x-\int {e}^{-2x}\,\text{d}x )\\  & =(-2)\cdot(8(\frac{{x}^{2}}{2})-(-\frac{{e}^{-2x}}{2}))+C \\  & =(-2)\cdot(4{x}^{2}+\frac{{e}^{-2x}}{2})+C.\end{aligned}
$$

So our general solution is $y=(-2)\cdot(4{x}^{2}+\frac{{e}^{-2x}}{2})+C.$ To find a particular solution, we substitute the condition $y(0)=7$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}7 & =(-2)\cdot(4(0)^{2}+\frac{{e}^{-2(0)}}{2})+C \\ 7 & =(-2)\cdot(0+\frac{1}{2})+C \\ C & =8.\end{aligned}
$$

Therefore, our particular solution is

$$
y=- 8 x^{2} + 8 - e^{- 2 x}.
$$

## q-119083 — moderate original raw replay

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

### moderate generated observed-pattern variant (scale 2; repaired and ineligible)

Find the particular solution to the differential equation ${y}^{′} - 4 x=2 e^{\frac{x}{2}}$ that satisfies the condition $y(0)=4.$

- $y=4 x + 2 e^{\frac{x}{2}} + 2$
- $y=2 x^{2} + 4 e^{\frac{x}{2}} + 4$
- $y=2 x - e^{\frac{x}{2}} + 5$
- $y=2 x^{2} + e^{\frac{x}{2}} + 3$
- $y=2 x^{2} + 4 e^{\frac{x}{2}}$

First, we rearrange the equation to give

$$
{y}^{′}=(2)\cdot(2x+{e}^{x/2}).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {y}^{′}\,\text{d}x & =(2)\cdot(\int (2x+{e}^{x/2})\text{d}x )\\ y & =(2)\cdot(2\int x\,\text{d}x+\int {e}^{x/2}\,\text{d}x )\\  & =(2)\cdot(2\cdot \frac{{x}^{2}}{2}+2{e}^{x/2})+C \\  & =(2)\cdot({x}^{2}+2{e}^{x/2})+C.\end{aligned}
$$

So our general solution is $y=(2)\cdot({x}^{2}+2{e}^{x/2})+C.$ To find a particular solution, we substitute the condition $y(0)=4$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}4 & =(2)\cdot({0}^{2}+2{e}^{0})+C \\ 4 & =(2)\cdot(0+2(1))+C \\ C & =0.\end{aligned}
$$

Therefore, our particular solution is

$$
y=2 x^{2} + 4 e^{\frac{x}{2}}.
$$

### moderate generated normal family variant (authored method bank)

Find the particular solution to the differential equation ${y}^{′} + 4 x=- 2 e^{\frac{x}{2}}$ that satisfies the condition $y(0)=7.$

- $y=2 x^{2} + 4 e^{\frac{x}{2}} + 3$
- $y=- 2 x^{2} - 4 e^{\frac{x}{2}} + 4$
- $y=- 2 x^{2} - 4 e^{\frac{x}{2}} + 11$
- $y=- 2 x^{2} - e^{\frac{x}{2}} + 8$
- $y=- 4 x - 2 e^{\frac{x}{2}} + 9$

First, we rearrange the equation to give

$$
{y}^{′}=(-2)\cdot(2x+{e}^{x/2}).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {y}^{′}\,\text{d}x & =(-2)\cdot(\int (2x+{e}^{x/2})\text{d}x )\\ y & =(-2)\cdot(2\int x\,\text{d}x+\int {e}^{x/2}\,\text{d}x )\\  & =(-2)\cdot(2\cdot \frac{{x}^{2}}{2}+2{e}^{x/2})+C \\  & =(-2)\cdot({x}^{2}+2{e}^{x/2})+C.\end{aligned}
$$

So our general solution is $y=(-2)\cdot({x}^{2}+2{e}^{x/2})+C.$ To find a particular solution, we substitute the condition $y(0)=7$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}7 & =(-2)\cdot({0}^{2}+2{e}^{0})+C \\ 7 & =(-2)\cdot(0+2(1))+C \\ C & =11.\end{aligned}
$$

Therefore, our particular solution is

$$
y=- 2 x^{2} - 4 e^{\frac{x}{2}} + 11.
$$

## q-347842 — easy original raw replay

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

### easy generated observed-pattern variant (scale 2; repaired and ineligible)

Find the particular solution to the differential equation $- \frac{\text{d}y}{\text{d}x} + 16 x=2 x^{2}$ that satisfies the condition $y(2)=10.$

$y=(2)\cdot(-\frac{{x}^{3}}{3}\,)+${{field-1}}

- $8 x^{2} - \frac{50}{3}$

First, we rearrange the equation to give

$$
\frac{\text{d}y}{\text{d}x}=(2)\cdot(-{x}^{2}+8x).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =(2)\cdot(\int (-{x}^{2}+8x)\,\text{d}x )\\ y & =(2)\cdot(-\frac{{x}^{3}}{3}+8\cdot \frac{{x}^{2}}{2})+C \\  & =(2)\cdot(-\frac{{x}^{3}}{3}+4{x}^{2})+C.\end{aligned}
$$

So our general solution is $y=(2)\cdot(-\frac{{x}^{3}}{3}+4{x}^{2})+C.$ To find a particular solution, we substitute the condition $y(2)=10$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}y & =(2)\cdot(-\frac{{x}^{3}}{3}+4{x}^{2})+C \\ 10 & =(2)\cdot(-\frac{{2}^{3}}{3}+4({2}^{2}))+C \\ 10 & =(2)\cdot(-\frac{8}{3}+16)+C \\ 10 & =(2)\cdot(\frac{40}{3})+C \\ C & =-\frac{50}{3}.\end{aligned}
$$

Therefore, our particular solution is 

$$
y=- \frac{2 x^{3}}{3} + 8 x^{2} - \frac{50}{3}.
$$

### easy generated normal family variant (authored method bank)

Find the particular solution to the differential equation $- \frac{\text{d}y}{\text{d}x} - 16 x=- 2 x^{2}$ that satisfies the condition $y(2)=7.$

$y=(-2)\cdot(-\frac{{x}^{3}}{3}\,)+${{field-1}}

- $\frac{101}{3} - 8 x^{2}$

First, we rearrange the equation to give

$$
\frac{\text{d}y}{\text{d}x}=(-2)\cdot(-{x}^{2}+8x).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =(-2)\cdot(\int (-{x}^{2}+8x)\,\text{d}x )\\ y & =(-2)\cdot(-\frac{{x}^{3}}{3}+8\cdot \frac{{x}^{2}}{2})+C \\  & =(-2)\cdot(-\frac{{x}^{3}}{3}+4{x}^{2})+C.\end{aligned}
$$

So our general solution is $y=(-2)\cdot(-\frac{{x}^{3}}{3}+4{x}^{2})+C.$ To find a particular solution, we substitute the condition $y(2)=7$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}y & =(-2)\cdot(-\frac{{x}^{3}}{3}+4{x}^{2})+C \\ 7 & =(-2)\cdot(-\frac{{2}^{3}}{3}+4({2}^{2}))+C \\ 7 & =(-2)\cdot(-\frac{8}{3}+16)+C \\ 7 & =(-2)\cdot(\frac{40}{3})+C \\ C & =\frac{101}{3}.\end{aligned}
$$

Therefore, our particular solution is 

$$
y=\frac{2 x^{3}}{3} - 8 x^{2} + \frac{101}{3}.
$$

## q-352066 — easy original raw replay

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

### easy generated observed-pattern variant (scale 2; repaired and ineligible)

Find the particular solution to the differential equation ${y}^{′} x^{2} - 6 {y}^{′} x + 9 {y}^{′}=16$ that satisfies the condition $y(4)=2.$

$y=\,${{field-1}}

- $18 - \frac{16}{x - 3}$

First, we rearrange the equation to give

$$
{y}^{′}=(2)\cdot(\frac{8}{(x-3)^{2}}).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {y}^{′}\,\text{d}x & =(2)\cdot(\int \frac{8}{(x-3)^{2}}\,\text{d}x )\\ y & =(2)\cdot(8\int \frac{1}{(x-3)^{2}}\,\text{d}x )\\  & =(2)\cdot(8(-\frac{1}{x-3}))+C \\  & =(2)\cdot(-\frac{8}{x-3})+C.\end{aligned}
$$

So our general solution is $y=(2)\cdot(-\frac{8}{x-3})+C.$ To find a particular solution, we substitute the condition $y(4)=2$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}2 & =(2)\cdot(-\frac{8}{4-3})+C \\ 2 & =(2)\cdot(-8)+C \\ C & =18.\end{aligned}
$$

Therefore, our particular solution is

$$
y=18 - \frac{16}{x - 3}.
$$

### easy generated normal family variant (authored method bank)

Find the particular solution to the differential equation ${y}^{′} x^{2} - 6 {y}^{′} x + 9 {y}^{′}=-16$ that satisfies the condition $y(4)=7.$

$y=\,${{field-1}}

- $-9 + \frac{16}{x - 3}$

First, we rearrange the equation to give

$$
{y}^{′}=(-2)\cdot(\frac{8}{(x-3)^{2}}).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {y}^{′}\,\text{d}x & =(-2)\cdot(\int \frac{8}{(x-3)^{2}}\,\text{d}x )\\ y & =(-2)\cdot(8\int \frac{1}{(x-3)^{2}}\,\text{d}x )\\  & =(-2)\cdot(8(-\frac{1}{x-3}))+C \\  & =(-2)\cdot(-\frac{8}{x-3})+C.\end{aligned}
$$

So our general solution is $y=(-2)\cdot(-\frac{8}{x-3})+C.$ To find a particular solution, we substitute the condition $y(4)=7$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}7 & =(-2)\cdot(-\frac{8}{4-3})+C \\ 7 & =(-2)\cdot(-8)+C \\ C & =-9.\end{aligned}
$$

Therefore, our particular solution is

$$
y=-9 + \frac{16}{x - 3}.
$$

## q-352068 — easy original raw replay

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

### easy generated observed-pattern variant (scale 2; repaired and ineligible)

Find the particular solution to the differential equation ${y}^{′} \sqrt{x + 1}=8$ that satisfies the condition $y(3)=20.$

$y=\,${{field-1}}

- $16 \sqrt{x + 1} - 12$

First, we rearrange the equation to give

$$
{y}^{′}=(2)\cdot(\frac{4}{\sqrt{x+1}}).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {y}^{′}\,\text{d}x & =(2)\cdot(\int \frac{4}{\sqrt{x+1}}\,\text{d}x )\\ y & =(2)\cdot(4\int (x+1)^{-1/2}\,\text{d}x )\\  & =(2)\cdot(4(2(x+1)^{1/2}))+C \\  & =(2)\cdot(8\sqrt{x+1})+C.\end{aligned}
$$

So our general solution is $y=(2)\cdot(8\sqrt{x+1})+C.$ To find a particular solution, we substitute the condition $y(3)=20$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}20 & =(2)\cdot(8\sqrt{3+1})+C \\ 20 & =(2)\cdot(8(2))+C \\ C & =-12.\end{aligned}
$$

Therefore, our particular solution is

$$
y=16 \sqrt{x + 1} - 12.
$$

### easy generated normal family variant (authored method bank)

Find the particular solution to the differential equation ${y}^{′} \sqrt{x + 1}=-8$ that satisfies the condition $y(3)=7.$

$y=\,${{field-1}}

- $39 - 16 \sqrt{x + 1}$

First, we rearrange the equation to give

$$
{y}^{′}=(-2)\cdot(\frac{4}{\sqrt{x+1}}).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {y}^{′}\,\text{d}x & =(-2)\cdot(\int \frac{4}{\sqrt{x+1}}\,\text{d}x )\\ y & =(-2)\cdot(4\int (x+1)^{-1/2}\,\text{d}x )\\  & =(-2)\cdot(4(2(x+1)^{1/2}))+C \\  & =(-2)\cdot(8\sqrt{x+1})+C.\end{aligned}
$$

So our general solution is $y=(-2)\cdot(8\sqrt{x+1})+C.$ To find a particular solution, we substitute the condition $y(3)=7$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}7 & =(-2)\cdot(8\sqrt{3+1})+C \\ 7 & =(-2)\cdot(8(2))+C \\ C & =39.\end{aligned}
$$

Therefore, our particular solution is

$$
y=39 - 16 \sqrt{x + 1}.
$$

## q-352075 — easy original raw replay

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

### easy generated observed-pattern variant (scale 2; repaired and ineligible)

Find the particular solution to the differential equation ${f}^{′}(x) + 6 \sin{(x )}=0$ that satisfies the condition $f(0)=4.$

$f(x)=\,${{field-1}}

- $6 \cos{(x )} - 2$

First, we rearrange the equation to give

$$
{f}^{′}(x)=(2)\cdot(-3\operatorname{sin}⁡x).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =(2)\cdot(\int (-3\operatorname{sin}⁡x)\,\text{d}x )\\ f(x) & =(2)\cdot(-3\int \operatorname{sin}⁡x\,\text{d}x )\\  & =(2)\cdot(-3(-\operatorname{cos}⁡x))+C \\  & =(2)\cdot(3\operatorname{cos}⁡x)+C.\end{aligned}
$$

So our general solution is $f(x)=(2)\cdot(3\operatorname{cos}⁡x)+C.$ To find a particular solution, we substitute the condition $f(0)=4$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}4 & =(2)\cdot(3\operatorname{cos}⁡0)+C \\ 4 & =(2)\cdot(3(1))+C \\ C & =-2.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=6 \cos{(x )} - 2.
$$

### easy generated normal family variant (authored method bank)

Find the particular solution to the differential equation ${f}^{′}(x) - 6 \sin{(x )}=0$ that satisfies the condition $f(0)=7.$

$f(x)=\,${{field-1}}

- $13 - 6 \cos{(x )}$

First, we rearrange the equation to give

$$
{f}^{′}(x)=(-2)\cdot(-3\operatorname{sin}⁡x).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =(-2)\cdot(\int (-3\operatorname{sin}⁡x)\,\text{d}x )\\ f(x) & =(-2)\cdot(-3\int \operatorname{sin}⁡x\,\text{d}x )\\  & =(-2)\cdot(-3(-\operatorname{cos}⁡x))+C \\  & =(-2)\cdot(3\operatorname{cos}⁡x)+C.\end{aligned}
$$

So our general solution is $f(x)=(-2)\cdot(3\operatorname{cos}⁡x)+C.$ To find a particular solution, we substitute the condition $f(0)=7$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}7 & =(-2)\cdot(3\operatorname{cos}⁡0)+C \\ 7 & =(-2)\cdot(3(1))+C \\ C & =13.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=13 - 6 \cos{(x )}.
$$

## q-50044 — easy original raw replay

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

### easy generated observed-pattern variant (scale 2; repaired and ineligible)

Find the particular solution to the differential equation below that satisfies the condition $y(-1)=4$
 

$$
\frac{\text{d}y}{\text{d}x} x=12 x^{3}.
$$

- $y=2 x^{3} + 6$
- $y=8 - 4 x^{2}$
- $y=12 x^{3} + 16$
- $y=4 x^{3} + 8$
- $y=6 x^{2} - 2$

First, we rearrange the equation to give

$$
\frac{\text{d}y}{\text{d}x}=(2)\cdot(6{x}^{2}).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =(2)\cdot(\int 6{x}^{2}\,\text{d}x )\\ y & =(2)\cdot(6(\frac{{x}^{3}}{3}))+C \\  & =(2)\cdot(2{x}^{3})+C.\end{aligned}
$$

So our general solution is $y=(2)\cdot(2{x}^{3})+C.$ To find a particular solution, we substitute the condition $y(-1)=4$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}y & =(2)\cdot(2{x}^{3})+C \\ 4 & =(2)\cdot(2(-1)^{3})+C \\ 4 & =(2)\cdot(-2)+C \\ C & =8.\end{aligned}
$$

Therefore, our particular solution is

$$
y=4 x^{3} + 8.
$$

### easy generated normal family variant (authored method bank)

Find the particular solution to the differential equation below that satisfies the condition $y(-1)=7$
 

$$
\frac{\text{d}y}{\text{d}x} x=- 12 x^{3}.
$$

- $y=4 x^{3} + 11$
- $y=- 4 x^{3} - 4$
- $y=3 - 4 x^{3}$
- $y=- 12 x^{3} - 5$
- $y=19 - 12 x^{2}$

First, we rearrange the equation to give

$$
\frac{\text{d}y}{\text{d}x}=(-2)\cdot(6{x}^{2}).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =(-2)\cdot(\int 6{x}^{2}\,\text{d}x )\\ y & =(-2)\cdot(6(\frac{{x}^{3}}{3}))+C \\  & =(-2)\cdot(2{x}^{3})+C.\end{aligned}
$$

So our general solution is $y=(-2)\cdot(2{x}^{3})+C.$ To find a particular solution, we substitute the condition $y(-1)=7$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}y & =(-2)\cdot(2{x}^{3})+C \\ 7 & =(-2)\cdot(2(-1)^{3})+C \\ 7 & =(-2)\cdot(-2)+C \\ C & =3.\end{aligned}
$$

Therefore, our particular solution is

$$
y=3 - 4 x^{3}.
$$

## q-50092 — easy original raw replay

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

### easy generated observed-pattern variant (scale 2; repaired and ineligible)

Find the particular solution to the differential equation below that satisfies the condition $y(1)=2.$

$$
\frac{\text{d}y}{\text{d}x} + 4 x=2 x^{2} + 8 x.
$$

- $y=2 x^{3} + 4 x^{2} - 4$
- $y=\frac{2 x^{3}}{3} + 2 x^{2} - \frac{2}{3}$
- $y=2 x^{3} + 2 x^{2} - 2$
- $y=\frac{2 x^{3}}{3} + 4 x^{2} - \frac{8}{3}$
- $y=\frac{2 x^{3}}{3} - 2 x^{2} + \frac{10}{3}$

First, we rearrange the equation to give

$$
\frac{\text{d}y}{\text{d}x}=(2)\cdot({x}^{2}+2x).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =(2)\cdot(\int ({x}^{2}+2x)\,\text{d}x )\\ y & =(2)\cdot(\frac{{x}^{3}}{3}+2\cdot \frac{{x}^{2}}{2})+C \\  & =(2)\cdot(\frac{{x}^{3}}{3}+{x}^{2})+C.\end{aligned}
$$

So our general solution is $y=(2)\cdot(\frac{{x}^{3}}{3}+{x}^{2})+C.$ To find a particular solution, we substitute the condition $y(1)=2$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}y & =(2)\cdot(\frac{{x}^{3}}{3}+{x}^{2})+C \\ 2 & =(2)\cdot(\frac{{1}^{3}}{3}+{1}^{2})+C \\ 2 & =(2)\cdot(\frac{4}{3})+C \\ C & =-\frac{2}{3}.\end{aligned}
$$

Therefore, our particular solution is

$$
y=\frac{2 x^{3}}{3} + 2 x^{2} - \frac{2}{3}.
$$

### easy generated normal family variant (authored method bank)

Find the particular solution to the differential equation below that satisfies the condition $y(1)=7.$

$$
\frac{\text{d}y}{\text{d}x} - 4 x=- 2 x^{2} - 8 x.
$$

- $y=\frac{2 x^{3}}{3} + 2 x^{2} + \frac{13}{3}$
- $y=- \frac{2 x^{3}}{3} - 2 x^{2} + \frac{8}{3}$
- $y=- \frac{2 x^{3}}{3} - 2 x^{2} + \frac{29}{3}$
- $y=- 2 x^{3} - 4 x^{2} + 13$
- $y=- 2 x^{2} - 4 x + 13$

First, we rearrange the equation to give

$$
\frac{\text{d}y}{\text{d}x}=(-2)\cdot({x}^{2}+2x).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =(-2)\cdot(\int ({x}^{2}+2x)\,\text{d}x )\\ y & =(-2)\cdot(\frac{{x}^{3}}{3}+2\cdot \frac{{x}^{2}}{2})+C \\  & =(-2)\cdot(\frac{{x}^{3}}{3}+{x}^{2})+C.\end{aligned}
$$

So our general solution is $y=(-2)\cdot(\frac{{x}^{3}}{3}+{x}^{2})+C.$ To find a particular solution, we substitute the condition $y(1)=7$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}y & =(-2)\cdot(\frac{{x}^{3}}{3}+{x}^{2})+C \\ 7 & =(-2)\cdot(\frac{{1}^{3}}{3}+{1}^{2})+C \\ 7 & =(-2)\cdot(\frac{4}{3})+C \\ C & =\frac{29}{3}.\end{aligned}
$$

Therefore, our particular solution is

$$
y=- \frac{2 x^{3}}{3} - 2 x^{2} + \frac{29}{3}.
$$

## q-50159 — easy original raw replay

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

### easy generated observed-pattern variant (scale 2; repaired and ineligible)

Find the particular solution to the differential equation below that satisfies the condition $f(0)=-4.$

$$
2 {f}^{′}(x) x + {f}^{′}(x) - 4=0.
$$

- $f(x)=2 \ln{(|{2 x + 1}| )} - 2$
- $f(x)=2 \ln{(|{2 x + 1}| )} - 4$
- $f(x)=4 \ln{(|{2 x + 1}| )} - 4$
- $f(x)=4 x^{2} + 2 x - 4$
- $f(x)=4 x - 4$

First, we rearrange the equation to give

$$
{f}^{′}(x)=(2)\cdot(\frac{2}{1+2x}).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =(2)\cdot(\int \frac{2}{1+2x}\,\text{d}x )\\ f(x) & =(2)\cdot(\int \frac{2}{1+2x}\,\text{d}x).\end{aligned}
$$

Let $u=(1+2x).$ Then $\text{d}u=2\,\text{d}x.$ Therefore,

$$
\begin{aligned}f(x) & =(2)\cdot(\int \frac{2}{1+2x}\,\text{d}x )\\  & =(2)\cdot(\int \frac{1}{u}\,\text{d}u )\\  & =(2)\cdot(\operatorname{ln}⁡|u|)+C \\  & =(2)\cdot(\operatorname{ln}⁡|1+2x|)+C.\end{aligned}
$$

So our general solution is $f(x)=(2)\cdot(\operatorname{ln}⁡|1+2x|)+C.$ To find a particular solution, we substitute the condition $f(0)=-4$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}f(x) & =(2)\cdot(\operatorname{ln}⁡|1+2x|)+C \\ -4 & =(2)\cdot(\operatorname{ln}⁡|1+2\cdot 0|)+C \\ -4 & =(2)\cdot(\operatorname{ln}⁡|1|)+C \\ C & =-4.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=2 \ln{(|{2 x + 1}| )} - 4.
$$

### easy generated normal family variant (authored method bank)

Find the particular solution to the differential equation below that satisfies the condition $f(0)=7.$

$$
2 {f}^{′}(x) x + {f}^{′}(x) + 4=0.
$$

- $f(x)=2 \ln{(|{2 x + 1}| )} + 7$
- $f(x)=- 2 \ln{(|{2 x + 1}| )}$
- $f(x)=7 - 2 \ln{(|{2 x + 1}| )}$
- $f(x)=7 - 4 \ln{(|{2 x + 1}| )}$
- $f(x)=11 - \frac{4}{2 x + 1}$

First, we rearrange the equation to give

$$
{f}^{′}(x)=(-2)\cdot(\frac{2}{1+2x}).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =(-2)\cdot(\int \frac{2}{1+2x}\,\text{d}x )\\ f(x) & =(-2)\cdot(\int \frac{2}{1+2x}\,\text{d}x).\end{aligned}
$$

Let $u=(1+2x).$ Then $\text{d}u=2\,\text{d}x.$ Therefore,

$$
\begin{aligned}f(x) & =(-2)\cdot(\int \frac{2}{1+2x}\,\text{d}x )\\  & =(-2)\cdot(\int \frac{1}{u}\,\text{d}u )\\  & =(-2)\cdot(\operatorname{ln}⁡|u|)+C \\  & =(-2)\cdot(\operatorname{ln}⁡|1+2x|)+C.\end{aligned}
$$

So our general solution is $f(x)=(-2)\cdot(\operatorname{ln}⁡|1+2x|)+C.$ To find a particular solution, we substitute the condition $f(0)=7$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}f(x) & =(-2)\cdot(\operatorname{ln}⁡|1+2x|)+C \\ 7 & =(-2)\cdot(\operatorname{ln}⁡|1+2\cdot 0|)+C \\ 7 & =(-2)\cdot(\operatorname{ln}⁡|1|)+C \\ C & =7.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=7 - 2 \ln{(|{2 x + 1}| )}.
$$

## q-8311 — easy original raw replay

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

### easy generated observed-pattern variant (scale 2; repaired and ineligible)

Find the specific solution to the differential equation $\frac{\text{d}y}{\text{d}x} + 8=0$ given that $y(-1)=8.$

- $y=- 8 x$
- $y=8$
- $y=8 x^{2}$
- $y=- 4 x - 4$
- $y=-8$

First, we rearrange the equation to give

$$
\frac{\text{d}y}{\text{d}x}=(2)\cdot(-4).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =(2)\cdot(\int (-4)\,\text{d}x )\\ \int \,\text{d}y & =(2)\cdot(\int (-4)\,\text{d}x )\\ y & =(2)\cdot(-4x)+C\,.\end{aligned}
$$

So our general solution is $y=(2)\cdot(-4x)+C.$ To find a particular solution, we substitute the condition $y(-1)=8$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}8 & =(2)\cdot(-4\cdot (-1))+C \\ 8 & =(2)\cdot(4)+C \\ 0 & =C\,.\end{aligned}
$$

Therefore, our particular solution is

$$
y=- 8 x.
$$

### easy generated normal family variant (authored method bank)

Find the specific solution to the differential equation $\frac{\text{d}y}{\text{d}x} - 8=0$ given that $y(-1)=7.$

- $y=- 8 x - 1$
- $y=8 x + 8$
- $y=8 x + 15$
- $y=4 x^{2} + 3$
- $y=7$

First, we rearrange the equation to give

$$
\frac{\text{d}y}{\text{d}x}=(-2)\cdot(-4).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =(-2)\cdot(\int (-4)\,\text{d}x )\\ \int \,\text{d}y & =(-2)\cdot(\int (-4)\,\text{d}x )\\ y & =(-2)\cdot(-4x)+C\,.\end{aligned}
$$

So our general solution is $y=(-2)\cdot(-4x)+C.$ To find a particular solution, we substitute the condition $y(-1)=7$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}7 & =(-2)\cdot(-4\cdot (-1))+C \\ 7 & =(-2)\cdot(4)+C \\ 15 & =C\,.\end{aligned}
$$

Therefore, our particular solution is

$$
y=8 x + 15.
$$

## easy generated default variant 1

Find the particular solution to the differential equation below that satisfies the condition $y(1)=-6.$

$$
\frac{\text{d}y}{\text{d}x} - 2 x=- x^{2} - 4 x.
$$

- $y=- x^{2} - 2 x - 3$
- $y=\frac{x^{3}}{3} + x^{2} - \frac{22}{3}$
- $y=- \frac{x^{3}}{3} - x^{2} - \frac{14}{3}$
- $y=- \frac{x^{3}}{3} - x^{2} + \frac{4}{3}$
- $y=- x^{3} - 2 x^{2} - 3$

First, we rearrange the equation to give

$$
\frac{\text{d}y}{\text{d}x}=(-1)\cdot({x}^{2}+2x).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =(-1)\cdot(\int ({x}^{2}+2x)\,\text{d}x )\\ y & =(-1)\cdot(\frac{{x}^{3}}{3}+2\cdot \frac{{x}^{2}}{2})+C \\  & =(-1)\cdot(\frac{{x}^{3}}{3}+{x}^{2})+C.\end{aligned}
$$

So our general solution is $y=(-1)\cdot(\frac{{x}^{3}}{3}+{x}^{2})+C.$ To find a particular solution, we substitute the condition $y(1)=-6$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}y & =(-1)\cdot(\frac{{x}^{3}}{3}+{x}^{2})+C \\ -6 & =(-1)\cdot(\frac{{1}^{3}}{3}+{1}^{2})+C \\ -6 & =(-1)\cdot(\frac{4}{3})+C \\ C & =-\frac{14}{3}.\end{aligned}
$$

Therefore, our particular solution is

$$
y=- \frac{x^{3}}{3} - x^{2} - \frac{14}{3}.
$$

## easy generated default variant 2

Find the particular solution to the differential equation ${f}^{′}(x) + 8 x=-2$ that satisfies the condition $f(1)=9.$

- $f(x)=17 - 8 x$
- $f(x)=- 8 x^{2} - 2 x + 19$
- $f(x)=4 x^{2} + 2 x + 3$
- $f(x)=- 4 x^{2} - 2 x + 15$
- $f(x)=- 4 x^{2} - 2 x + 6$

First, we rearrange the equation to give

$$
{f}^{′}(x)=(-2)\cdot(4x+1).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =(-2)\cdot(\int (4x+1)\,\text{d}x )\\ f(x) & =(-2)\cdot(4\int x\,\text{d}x+\int \text{d}x )\\  & =(-2)\cdot(4(\frac{1}{2}{x}^{2})+x)+C \\  & =(-2)\cdot(2{x}^{2}+x)+C.\end{aligned}
$$

So our general solution is $f(x)=(-2)\cdot(2{x}^{2}+x)+C.$ To find a particular solution, we substitute the condition $f(1)=9$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}9 & =(-2)\cdot(2(1)^{2}+1)+C \\ 9 & =(-2)\cdot(2+1)+C \\ C & =15.\end{aligned}
$$

Therefore, our particular solution is

$$
f(x)=- 4 x^{2} - 2 x + 15.
$$

## moderate generated default variant 1

Find the particular solution to the differential equation ${y}^{′} - e^{- 2 x}=- 8 x$ that satisfies the condition $y(0)=12.$

- $y=- 8 x + 11 + e^{- 2 x}$
- $y=4 x^{2} + \frac{23}{2} + \frac{e^{- 2 x}}{2}$
- $y=- 4 x^{2} + \frac{25}{2} - \frac{e^{- 2 x}}{2}$
- $y=- 4 x^{2} + \frac{1}{2} - \frac{e^{- 2 x}}{2}$
- $y=- 4 x^{2} + 14 - 2 e^{- 2 x}$

First, we rearrange the equation to give

$$
{y}^{′}=(-1)\cdot(8x-{e}^{-2x}).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {y}^{′}\,\text{d}x & =(-1)\cdot(\int (8x-{e}^{-2x})\,\text{d}x )\\ y & =(-1)\cdot(8\int x\,\text{d}x-\int {e}^{-2x}\,\text{d}x )\\  & =(-1)\cdot(8(\frac{{x}^{2}}{2})-(-\frac{{e}^{-2x}}{2}))+C \\  & =(-1)\cdot(4{x}^{2}+\frac{{e}^{-2x}}{2})+C.\end{aligned}
$$

So our general solution is $y=(-1)\cdot(4{x}^{2}+\frac{{e}^{-2x}}{2})+C.$ To find a particular solution, we substitute the condition $y(0)=12$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}12 & =(-1)\cdot(4(0)^{2}+\frac{{e}^{-2(0)}}{2})+C \\ 12 & =(-1)\cdot(0+\frac{1}{2})+C \\ C & =\frac{25}{2}.\end{aligned}
$$

Therefore, our particular solution is

$$
y=- 4 x^{2} + \frac{25}{2} - \frac{e^{- 2 x}}{2}.
$$

## moderate generated default variant 2

Find the particular solution to the differential equation ${y}^{′} - 2 e^{- 2 x}=- 16 x$ that satisfies the condition $y(0)=9.$

- $y=- 16 x + 7 + 2 e^{- 2 x}$
- $y=- 8 x^{2} + 13 - 4 e^{- 2 x}$
- $y=8 x^{2} + 8 + e^{- 2 x}$
- $y=- 8 x^{2} + 10 - e^{- 2 x}$
- $y=- 8 x^{2} + 1 - e^{- 2 x}$

First, we rearrange the equation to give

$$
{y}^{′}=(-2)\cdot(8x-{e}^{-2x}).
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int {y}^{′}\,\text{d}x & =(-2)\cdot(\int (8x-{e}^{-2x})\,\text{d}x )\\ y & =(-2)\cdot(8\int x\,\text{d}x-\int {e}^{-2x}\,\text{d}x )\\  & =(-2)\cdot(8(\frac{{x}^{2}}{2})-(-\frac{{e}^{-2x}}{2}))+C \\  & =(-2)\cdot(4{x}^{2}+\frac{{e}^{-2x}}{2})+C.\end{aligned}
$$

So our general solution is $y=(-2)\cdot(4{x}^{2}+\frac{{e}^{-2x}}{2})+C.$ To find a particular solution, we substitute the condition $y(0)=9$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}9 & =(-2)\cdot(4(0)^{2}+\frac{{e}^{-2(0)}}{2})+C \\ 9 & =(-2)\cdot(0+\frac{1}{2})+C \\ C & =10.\end{aligned}
$$

Therefore, our particular solution is

$$
y=- 8 x^{2} + 10 - e^{- 2 x}.
$$

## hard generated default variant 1

Find the particular solution to the differential equation $g'(x)=- 2 x^{2}- 2 e^{- 2 x}+2 \cos{(x )}$ that satisfies the condition $g(0)=-6.$

$g(x)=\,${{field-1}}

- $- \frac{2 x^{3}}{3} + 2 \sin{(x )} - 7 + e^{- 2 x}$

The derivative is already isolated, so we have

$$
g'(x)=- 2 x^{2}- 2 e^{- 2 x}+2 \cos{(x )}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int g'(x)\,\text{d}x & =\int (- 2 x^{2}- 2 e^{- 2 x}+2 \cos{(x )})\,\text{d}x \\ g(x) & =\int (- 2 x^{2})\,\text{d}x + \int (- 2 e^{- 2 x})\,\text{d}x + \int (2 \cos{(x )})\,\text{d}x \\ & =(-2)(\frac{x^{3}}{3}) + (-2)(- \frac{e^{- 2 x}}{2}) + (2)(\sin{(x )})+C \\ & =- \frac{2 x^{3}}{3}+e^{- 2 x}+2 \sin{(x )}+C.\end{aligned}
$$

So our general solution is $g(x)=- \frac{2 x^{3}}{3}+e^{- 2 x}+2 \sin{(x )}+C.$ To find a particular solution, we substitute the condition $g(0)=-6$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}-6 & =(- \frac{2 (0)^{3}}{3}) + (e^{- 2 (0)}) + (2 \sin{((0) )})+C \\ -6 & =(0) + (1) + (0)+C \\ C & =-7.\end{aligned}
$$

Therefore, our particular solution is

$$
g(x)=- \frac{2 x^{3}}{3} + 2 \sin{(x )} - 7 + e^{- 2 x}.
$$

## hard generated default variant 2

Find the particular solution to the differential equation $g'(x)=- 2 x^{2}- 2 e^{- 2 x}+2 \cos{(x )}$ that satisfies the condition $g(0)=-6.$

- $g(x)=- 2 x^{3} + 2 \sin{(x )} - 7 + e^{- 2 x}$
- $g(x)=- \frac{2 x^{3}}{3} + 2 \sin{(x )} - 7 + e^{- 2 x}$
- $g(x)=- 2 x^{2} + 2 \cos{(x )} - 6 - 2 e^{- 2 x}$
- $g(x)=- \frac{2 x^{3}}{3} + 2 \sin{(x )} - 1 + e^{- 2 x}$
- $g(x)=\frac{2 x^{3}}{3} - 2 \sin{(x )} - 5 - e^{- 2 x}$

The derivative is already isolated, so we have

$$
g'(x)=- 2 x^{2}- 2 e^{- 2 x}+2 \cos{(x )}.
$$

Then, we integrate both sides with respect to $x,$ and get

$$
\begin{aligned}\int g'(x)\,\text{d}x & =\int (- 2 x^{2}- 2 e^{- 2 x}+2 \cos{(x )})\,\text{d}x \\ g(x) & =\int (- 2 x^{2})\,\text{d}x + \int (- 2 e^{- 2 x})\,\text{d}x + \int (2 \cos{(x )})\,\text{d}x \\ & =(-2)(\frac{x^{3}}{3}) + (-2)(- \frac{e^{- 2 x}}{2}) + (2)(\sin{(x )})+C \\ & =- \frac{2 x^{3}}{3}+e^{- 2 x}+2 \sin{(x )}+C.\end{aligned}
$$

So our general solution is $g(x)=- \frac{2 x^{3}}{3}+e^{- 2 x}+2 \sin{(x )}+C.$ To find a particular solution, we substitute the condition $g(0)=-6$ into our solution and obtain a value for $C,$ as follows:

$$
\begin{aligned}-6 & =(- \frac{2 (0)^{3}}{3}) + (e^{- 2 (0)}) + (2 \sin{((0) )})+C \\ -6 & =(0) + (1) + (0)+C \\ C & =-7.\end{aligned}
$$

Therefore, our particular solution is

$$
g(x)=- \frac{2 x^{3}}{3} + 2 \sin{(x )} - 7 + e^{- 2 x}.
$$

