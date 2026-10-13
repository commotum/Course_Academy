# Direct-integration review

Raw original profiles have dependent_scale=1; changed profiles have dependent_scale=2. Normal records have an authored method bank.


## Original source replay — Unrated — linear — q-14245 {'dependent_scale': '1'}

Find the general solution to the differential equation $f^{′}(x) + 11x = 0$.

- $f(x) =-\frac{11}{2}x^{2} + C$
- $f(x) = \frac{11}{2} - C$
- $f(x) =-\frac{11}{2}x + C$
- $f(x) = 11x^{2} + C$
- $f(x) = \frac{11}{2}x^{2}$

*Raw source has no correct designation.*

*Raw source has no worked solution.*


## Generated evidence variant — Unrated — linear — q-14245 {'dependent_scale': '2'}

Find the general solution to the differential equation $\left(2\cdot f^{′}(x)\right) + 11x = 0$.

- $\left(2\cdot f(x)\right) =-\frac{11}{2}x^{2} + C$
- $\left(2\cdot f(x)\right) = \frac{11}{2} - C$
- $\left(2\cdot f(x)\right) =-\frac{11}{2}x + C$
- $\left(2\cdot f(x)\right) = 11x^{2} + C$
- $\left(2\cdot f(x)\right) = \frac{11}{2}x^{2}$

*Raw source has no correct designation.*

*Raw source has no worked solution.*


## Original source replay — Moderate — exp_linear — q-50136 {'dependent_scale': '1'}

Solve the differential equation $\frac{\text{d}y}{\text{d}x}+4{e}^{2x}=-2x.$

- $y=-{e}^{2x}-{x}^{2}+C$
- $y=-2{e}^{2x}-{x}^{2}+C$
- $y=-2{e}^{2x}-2{x}^{2}+C$
- $y=-4{e}^{2x}-2{x}^{2}+C$
- $y=-{e}^{2x}-2{x}^{2}+C$

**Correct:** $y=-2{e}^{2x}-{x}^{2}+C$

First, we rearrange the equation to isolate the derivative term:

$$
\frac{\text{d}y}{\text{d}x}=-4{e}^{2x}-2x.
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int (-4{e}^{2x}-2x)\,\text{d}x \\ y & =\int (-4{e}^{2x}-2x)\,\text{d}x\end{aligned}
$$

Finally, we get

$$
\begin{aligned}\begin{aligned}y & =\int (-4{e}^{2x}-2x)\,\text{d}x \\  & =-4\int {e}^{2x}\,\text{d}x-2\int x\,\text{d}x \\  & =-2{e}^{2x}-{x}^{2}+C.\end{aligned}\end{aligned}
$$


## Generated evidence variant — Moderate — exp_linear — q-50136 {'dependent_scale': '2'}

Solve the differential equation $\left(2\cdot \frac{\text{d}y}{\text{d}x}\right)+4{e}^{2x}=-2x.$

- $\left(2\cdot y\right)=-{e}^{2x}-{x}^{2}+C$
- $\left(2\cdot y\right)=-2{e}^{2x}-{x}^{2}+C$
- $\left(2\cdot y\right)=-2{e}^{2x}-2{x}^{2}+C$
- $\left(2\cdot y\right)=-4{e}^{2x}-2{x}^{2}+C$
- $\left(2\cdot y\right)=-{e}^{2x}-2{x}^{2}+C$

**Correct:** $\left(2\cdot y\right)=-2{e}^{2x}-{x}^{2}+C$

First, we rearrange the equation to isolate the derivative term:

$$
\left(2\cdot \frac{\text{d}y}{\text{d}x}\right)=-4{e}^{2x}-2x.
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int \left(2\cdot \frac{\text{d}y}{\text{d}x}\right)\,\text{d}x & =\int (-4{e}^{2x}-2x)\,\text{d}x \\ \left(2\cdot y\right) & =\int (-4{e}^{2x}-2x)\,\text{d}x\end{aligned}
$$

Finally, we get

$$
\begin{aligned}\begin{aligned}\left(2\cdot y\right) & =\int (-4{e}^{2x}-2x)\,\text{d}x \\  & =-4\int {e}^{2x}\,\text{d}x-2\int x\,\text{d}x \\  & =-2{e}^{2x}-{x}^{2}+C.\end{aligned}\end{aligned}
$$


## Original source replay — Easy — sine — q-119032 {'dependent_scale': '1'}

Find the general solution to the differential equation  ${f}^{′}(x)=\frac{1}{2}\operatorname{sin}⁡4x.$

- $f(x)=-\frac{1}{4}\operatorname{cos}⁡4x+C$
- $f(x)=\frac{1}{2}\operatorname{cos}⁡4x+C$
- $f(x)=-8\operatorname{cos}⁡4x+C$
- $f(x)=2\operatorname{cos}⁡4x+C$
- $f(x)=-\frac{1}{8}\operatorname{cos}⁡4x+C$

**Correct:** $f(x)=-\frac{1}{8}\operatorname{cos}⁡4x+C$

First, notice that the derivative term is already isolated on the left:

$$
\begin{aligned}{f}^{′}(x) & =\frac{1}{2}\operatorname{sin}⁡4x.\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =\int \frac{1}{2}\operatorname{sin}⁡4x\,\text{d}x \\ f(x) & =\frac{1}{2}\int \operatorname{sin}⁡4x\,\text{d}x \\  & =\frac{1}{2}(-\frac{1}{4}\operatorname{cos}⁡4x) \\  & =-\frac{1}{8}\operatorname{cos}⁡4x+C.\end{aligned}
$$


## Generated evidence variant — Easy — sine — q-119032 {'dependent_scale': '2'}

Find the general solution to the differential equation  $\left(2\cdot {f}^{′}(x)\right)=\frac{1}{2}\operatorname{sin}⁡4x.$

- $\left(2\cdot f(x)\right)=-\frac{1}{4}\operatorname{cos}⁡4x+C$
- $\left(2\cdot f(x)\right)=\frac{1}{2}\operatorname{cos}⁡4x+C$
- $\left(2\cdot f(x)\right)=-8\operatorname{cos}⁡4x+C$
- $\left(2\cdot f(x)\right)=2\operatorname{cos}⁡4x+C$
- $\left(2\cdot f(x)\right)=-\frac{1}{8}\operatorname{cos}⁡4x+C$

**Correct:** $\left(2\cdot f(x)\right)=-\frac{1}{8}\operatorname{cos}⁡4x+C$

First, notice that the derivative term is already isolated on the left:

$$
\begin{aligned}\left(2\cdot {f}^{′}(x)\right) & =\frac{1}{2}\operatorname{sin}⁡4x.\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int \left(2\cdot {f}^{′}(x)\right)\,\text{d}x & =\int \frac{1}{2}\operatorname{sin}⁡4x\,\text{d}x \\ \left(2\cdot f(x)\right) & =\frac{1}{2}\int \operatorname{sin}⁡4x\,\text{d}x \\  & =\frac{1}{2}(-\frac{1}{4}\operatorname{cos}⁡4x) \\  & =-\frac{1}{8}\operatorname{cos}⁡4x+C.\end{aligned}
$$


## Original source replay — Easy — reciprocal — q-119034 {'dependent_scale': '1'}

Find the general solution to the differential equation  ${f}^{′}(x)=\frac{3}{x-1}.$

- $f(x)=\frac{1}{3}\operatorname{ln}⁡|x-1|+C$
- $f(x)=-\frac{3}{(x-1)^{2}}+C$
- $f(x)=3\operatorname{ln}⁡|x-1|+C$
- $f(x)=\operatorname{ln}⁡|3x-1|+C$
- $f(x)=-\frac{1}{(3x-1)^{2}}+C$

**Correct:** $f(x)=3\operatorname{ln}⁡|x-1|+C$

First, notice that the derivative term is already isolated on the left:

$$
\begin{aligned}{f}^{′}(x) & =\frac{3}{x-1}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =\int \frac{3}{x-1}\,\text{d}x \\ f(x) & =3\int \frac{1}{x-1}\,\text{d}x \\  & =3\operatorname{ln}⁡|x-1|+C.\end{aligned}
$$


## Generated evidence variant — Easy — reciprocal — q-119034 {'dependent_scale': '2'}

Find the general solution to the differential equation  $\left(2\cdot {f}^{′}(x)\right)=\frac{3}{x-1}.$

- $\left(2\cdot f(x)\right)=\frac{1}{3}\operatorname{ln}⁡|x-1|+C$
- $\left(2\cdot f(x)\right)=-\frac{3}{(x-1)^{2}}+C$
- $\left(2\cdot f(x)\right)=3\operatorname{ln}⁡|x-1|+C$
- $\left(2\cdot f(x)\right)=\operatorname{ln}⁡|3x-1|+C$
- $\left(2\cdot f(x)\right)=-\frac{1}{(3x-1)^{2}}+C$

**Correct:** $\left(2\cdot f(x)\right)=3\operatorname{ln}⁡|x-1|+C$

First, notice that the derivative term is already isolated on the left:

$$
\begin{aligned}\left(2\cdot {f}^{′}(x)\right) & =\frac{3}{x-1}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int \left(2\cdot {f}^{′}(x)\right)\,\text{d}x & =\int \frac{3}{x-1}\,\text{d}x \\ \left(2\cdot f(x)\right) & =3\int \frac{1}{x-1}\,\text{d}x \\  & =3\operatorname{ln}⁡|x-1|+C.\end{aligned}
$$


## Original source replay — Moderate — polynomial_pair — q-119035 {'dependent_scale': '1'}

Find the general solution to the differential equation  ${f}^{′}(x)+6{x}^{2}=4x.$

- $f(x)={x}^{2}(2x-1)+C$
- $f(x)=2{x}^{2}({x}^{2}-1)+C$
- $f(x)=2{x}^{2}(1-x)+C$
- $f(x)=2{x}^{2}(3-x)+C$
- $f(x)={x}^{2}(2-x)+C$

**Correct:** $f(x)=2{x}^{2}(1-x)+C$

First, we rearrange the equation to isolate the derivative term:

$$
\begin{aligned}{f}^{′}(x) & =4x-6{x}^{2}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =\int (4x-6{x}^{2})\text{d}x \\  & =4\int x\,\text{d}x-6\int {x}^{2}\,\text{d}x \\  & =4\cdot \frac{1}{2}{x}^{2}-6\cdot \frac{1}{3}{x}^{3} \\  & =2{x}^{2}-2{x}^{3}+C \\  & =2{x}^{2}(1-x)+C.\end{aligned}
$$


## Generated evidence variant — Moderate — polynomial_pair — q-119035 {'dependent_scale': '2'}

Find the general solution to the differential equation  $\left(2\cdot {f}^{′}(x)\right)+6{x}^{2}=4x.$

- $\left(2\cdot f(x)\right)={x}^{2}(2x-1)+C$
- $\left(2\cdot f(x)\right)=2{x}^{2}({x}^{2}-1)+C$
- $\left(2\cdot f(x)\right)=2{x}^{2}(1-x)+C$
- $\left(2\cdot f(x)\right)=2{x}^{2}(3-x)+C$
- $\left(2\cdot f(x)\right)={x}^{2}(2-x)+C$

**Correct:** $\left(2\cdot f(x)\right)=2{x}^{2}(1-x)+C$

First, we rearrange the equation to isolate the derivative term:

$$
\begin{aligned}\left(2\cdot {f}^{′}(x)\right) & =4x-6{x}^{2}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int \left(2\cdot {f}^{′}(x)\right)\,\text{d}x & =\int (4x-6{x}^{2})\text{d}x \\  & =4\int x\,\text{d}x-6\int {x}^{2}\,\text{d}x \\  & =4\cdot \frac{1}{2}{x}^{2}-6\cdot \frac{1}{3}{x}^{3} \\  & =2{x}^{2}-2{x}^{3}+C \\  & =2{x}^{2}(1-x)+C.\end{aligned}
$$


## Original source replay — Moderate — scaled_cosine — q-99006 {'dependent_scale': '1'}

Solve the differential equation $-5{f}^{′}(x)+3\operatorname{cos}⁡(3x)=0.$

- $f(x)=\frac{3}{5}\operatorname{sin}⁡(3x)+C$
- $f(x)=\frac{9}{5}\operatorname{cos}⁡(3x)+C$
- $f(x)=\frac{9}{5}\operatorname{sin}⁡(3x)+C$
- $f(x)=\frac{1}{5}\operatorname{sin}⁡(3x)+C$
- $f(x)=\frac{1}{5}\operatorname{cos}⁡(3x)+C$

**Correct:** $f(x)=\frac{1}{5}\operatorname{sin}⁡(3x)+C$

First, we rearrange the equation to isolate the derivative term:

$$
{f}^{′}(x)=\frac{3}{5}\operatorname{cos}⁡(3x).
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =\int \frac{3}{5}\operatorname{cos}⁡(3x)\,\text{d}x \\ f(x) & =\int \frac{3}{5}\operatorname{cos}⁡(3x)\,\text{d}x.\end{aligned}
$$

Finally, we get

$$
\begin{aligned}\begin{aligned}f(x) & =\int \frac{3}{5}\operatorname{cos}⁡(3x)\,\text{d}x \\  & =\frac{3}{5}\int \operatorname{cos}⁡(3x)\,\text{d}x \\  & =\frac{3}{5}\cdot \frac{1}{3}\operatorname{sin}⁡(3x)+C \\  & =\frac{1}{5}\operatorname{sin}⁡(3x)+C.\end{aligned}\end{aligned}
$$


## Generated evidence variant — Moderate — scaled_cosine — q-99006 {'dependent_scale': '2'}

Solve the differential equation $-5\left(2\cdot {f}^{′}(x)\right)+3\operatorname{cos}⁡(3x)=0.$

- $\left(2\cdot f(x)\right)=\frac{3}{5}\operatorname{sin}⁡(3x)+C$
- $\left(2\cdot f(x)\right)=\frac{9}{5}\operatorname{cos}⁡(3x)+C$
- $\left(2\cdot f(x)\right)=\frac{9}{5}\operatorname{sin}⁡(3x)+C$
- $\left(2\cdot f(x)\right)=\frac{1}{5}\operatorname{sin}⁡(3x)+C$
- $\left(2\cdot f(x)\right)=\frac{1}{5}\operatorname{cos}⁡(3x)+C$

**Correct:** $\left(2\cdot f(x)\right)=\frac{1}{5}\operatorname{sin}⁡(3x)+C$

First, we rearrange the equation to isolate the derivative term:

$$
\left(2\cdot {f}^{′}(x)\right)=\frac{3}{5}\operatorname{cos}⁡(3x).
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int \left(2\cdot {f}^{′}(x)\right)\,\text{d}x & =\int \frac{3}{5}\operatorname{cos}⁡(3x)\,\text{d}x \\ \left(2\cdot f(x)\right) & =\int \frac{3}{5}\operatorname{cos}⁡(3x)\,\text{d}x.\end{aligned}
$$

Finally, we get

$$
\begin{aligned}\begin{aligned}\left(2\cdot f(x)\right) & =\int \frac{3}{5}\operatorname{cos}⁡(3x)\,\text{d}x \\  & =\frac{3}{5}\int \operatorname{cos}⁡(3x)\,\text{d}x \\  & =\frac{3}{5}\cdot \frac{1}{3}\operatorname{sin}⁡(3x)+C \\  & =\frac{1}{5}\operatorname{sin}⁡(3x)+C.\end{aligned}\end{aligned}
$$


## Original source replay — Easy — exponential — q-119033 {'dependent_scale': '1'}

Find the general solution to the differential equation  ${f}^{′}(x)+3{e}^{-x}=0.$

- $f(x)=3{e}^{-x}+C$
- $f(x)=\frac{1}{3}{e}^{-x}+C$
- $f(x)={e}^{x-3}+C$
- $f(x)=-{e}^{-x/3}+C$
- $f(x)={e}^{-3x}+C$

**Correct:** $f(x)=3{e}^{-x}+C$

First, we rearrange the equation to isolate the derivative term:

$$
\begin{aligned}{f}^{′}(x) & =-3{e}^{-x}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =\int (-3{e}^{-x})\text{d}x \\ f(x) & =-3\int {e}^{-x}\,\text{d}x \\  & =-3(-{e}^{-x})+C \\  & =3{e}^{-x}+C.\end{aligned}
$$


## Generated evidence variant — Easy — exponential — q-119033 {'dependent_scale': '2'}

Find the general solution to the differential equation  $\left(2\cdot {f}^{′}(x)\right)+3{e}^{-x}=0.$

- $\left(2\cdot f(x)\right)=3{e}^{-x}+C$
- $\left(2\cdot f(x)\right)=\frac{1}{3}{e}^{-x}+C$
- $\left(2\cdot f(x)\right)={e}^{x-3}+C$
- $\left(2\cdot f(x)\right)=-{e}^{-x/3}+C$
- $\left(2\cdot f(x)\right)={e}^{-3x}+C$

**Correct:** $\left(2\cdot f(x)\right)=3{e}^{-x}+C$

First, we rearrange the equation to isolate the derivative term:

$$
\begin{aligned}\left(2\cdot {f}^{′}(x)\right) & =-3{e}^{-x}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int \left(2\cdot {f}^{′}(x)\right)\,\text{d}x & =\int (-3{e}^{-x})\text{d}x \\ \left(2\cdot f(x)\right) & =-3\int {e}^{-x}\,\text{d}x \\  & =-3(-{e}^{-x})+C \\  & =3{e}^{-x}+C.\end{aligned}
$$


## Original source replay — Moderate — exp_constant — q-119037 {'dependent_scale': '1'}

Find the general solution to the differential equation  ${f}^{′}(x)-6{e}^{-3x}=1.$

- $f(x)=x+{e}^{-3x}+C$
- $f(x)=x-2{e}^{-3x}+C$
- $f(x)=2(x+9{e}^{-3x})+C$
- $f(x)=2(x-3{e}^{-3x})+C$
- $f(x)=x-18{e}^{-3x}+C$

**Correct:** $f(x)=x-2{e}^{-3x}+C$

First, we rearrange the equation to isolate the derivative term:

$$
\begin{aligned}{f}^{′}(x) & =1+6{e}^{-3x}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int {f}^{′}(x)\,\text{d}x & =\int (1+6{e}^{-3x})\text{d}x \\  & =\int \text{d}x+6\int {e}^{-3x}\,\text{d}x \\  & =x+6(-\frac{1}{3}{e}^{-3x}) \\  & =x-2{e}^{-3x}+C.\end{aligned}
$$


## Generated evidence variant — Moderate — exp_constant — q-119037 {'dependent_scale': '2'}

Find the general solution to the differential equation  $\left(2\cdot {f}^{′}(x)\right)-6{e}^{-3x}=1.$

- $\left(2\cdot f(x)\right)=x+{e}^{-3x}+C$
- $\left(2\cdot f(x)\right)=x-2{e}^{-3x}+C$
- $\left(2\cdot f(x)\right)=2(x+9{e}^{-3x})+C$
- $\left(2\cdot f(x)\right)=2(x-3{e}^{-3x})+C$
- $\left(2\cdot f(x)\right)=x-18{e}^{-3x}+C$

**Correct:** $\left(2\cdot f(x)\right)=x-2{e}^{-3x}+C$

First, we rearrange the equation to isolate the derivative term:

$$
\begin{aligned}\left(2\cdot {f}^{′}(x)\right) & =1+6{e}^{-3x}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int \left(2\cdot {f}^{′}(x)\right)\,\text{d}x & =\int (1+6{e}^{-3x})\text{d}x \\  & =\int \text{d}x+6\int {e}^{-3x}\,\text{d}x \\  & =x+6(-\frac{1}{3}{e}^{-3x}) \\  & =x-2{e}^{-3x}+C.\end{aligned}
$$


## Generated learning question — Easy — linear — authored-direct-operations {'d': 1, 'terms': [['poly', 3, 1]]}

Find the general solution to the differential equation $f'(x)=3 x.$

- $f(x)=3 x+C$
- $f(x)=- \frac{3 x^{2}}{2}+C$
- $f(x)=\frac{3 x^{2}}{2}+C$
- $f(x)=\frac{x^{2}}{2}+C$
- $f(x)=6 x^{2}+C$

**Correct:** $f(x)=\frac{3 x^{2}}{2}+C$

First, notice that the derivative term is already isolated on the left:

$$
\begin{aligned}f'(x) &=3 x\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (3 x)\,\text{d}x \\ f(x) &=\int (3 x)\,\text{d}x \\ &=1\cdot \left(\frac{3 x^{2}}{2}\right)+C \\ &=\frac{3 x^{2}}{2}+C.\end{aligned}
$$


## Generated learning question — Easy — linear — authored-direct-operations {'d': 1, 'terms': [['poly', -4, 1]]}

Find the general solution to the differential equation $f'(x)=- 4 x.$

- $f(x)=- 4 x+C$
- $f(x)=- 8 x^{2}+C$
- $f(x)=\frac{x^{2}}{2}+C$
- $f(x)=- 2 x^{2}+C$
- $f(x)=2 x^{2}+C$

**Correct:** $f(x)=- 2 x^{2}+C$

First, notice that the derivative term is already isolated on the left:

$$
\begin{aligned}f'(x) &=- 4 x\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (- 4 x)\,\text{d}x \\ f(x) &=\int (- 4 x)\,\text{d}x \\ &=1\cdot \left(- 2 x^{2}\right)+C \\ &=- 2 x^{2}+C.\end{aligned}
$$


## Generated learning question — Easy — sine — authored-direct-operations {'d': 1, 'terms': [['sin', 3, -4]]}

Find the general solution to the differential equation $f'(x)=- 3 \sin{\left(4 x \right)}.$

- $f(x)=- 3 \sin{\left(4 x \right)}+C$
- $f(x)=- \frac{3 \cos{\left(4 x \right)}}{4}+C$
- $f(x)=\frac{3 \cos{\left(4 x \right)}}{4}+C$
- $f(x)=\frac{\cos{\left(4 x \right)}}{4}+C$
- $f(x)=12 \cos{\left(4 x \right)}+C$

**Correct:** $f(x)=\frac{3 \cos{\left(4 x \right)}}{4}+C$

First, notice that the derivative term is already isolated on the left:

$$
\begin{aligned}f'(x) &=- 3 \sin{\left(4 x \right)}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (- 3 \sin{\left(4 x \right)})\,\text{d}x \\ f(x) &=\int (- 3 \sin{\left(4 x \right)})\,\text{d}x \\ &=1\cdot \left(\frac{3 \cos{\left(4 x \right)}}{4}\right)+C \\ &=\frac{3 \cos{\left(4 x \right)}}{4}+C.\end{aligned}
$$


## Generated learning question — Easy — sine — authored-direct-operations {'d': 1, 'terms': [['sin', 8, -4]]}

Find the general solution to the differential equation $f'(x)=- 8 \sin{\left(4 x \right)}.$

- $f(x)=- 8 \sin{\left(4 x \right)}+C$
- $f(x)=32 \cos{\left(4 x \right)}+C$
- $f(x)=\frac{\cos{\left(4 x \right)}}{4}+C$
- $f(x)=2 \cos{\left(4 x \right)}+C$
- $f(x)=- 2 \cos{\left(4 x \right)}+C$

**Correct:** $f(x)=2 \cos{\left(4 x \right)}+C$

First, notice that the derivative term is already isolated on the left:

$$
\begin{aligned}f'(x) &=- 8 \sin{\left(4 x \right)}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (- 8 \sin{\left(4 x \right)})\,\text{d}x \\ f(x) &=\int (- 8 \sin{\left(4 x \right)})\,\text{d}x \\ &=1\cdot \left(2 \cos{\left(4 x \right)}\right)+C \\ &=2 \cos{\left(4 x \right)}+C.\end{aligned}
$$


## Generated learning question — Easy — reciprocal — authored-direct-operations {'d': 1, 'terms': [['reciprocal', -2, 1]]}

Find the general solution to the differential equation $f'(x)=- \frac{2}{x - 1}.$

- $f(x)=- \frac{2}{x - 1}+C$
- $f(x)=2 \ln{\left(\left|{x - 1}\right| \right)}+C$
- $f(x)=- 2 \ln{\left(\left|{x - 1}\right| \right)}+C$
- $f(x)=\ln{\left(\left|{x - 1}\right| \right)}+C$
- $f(x)=- \frac{\ln{\left(\left|{x - 1}\right| \right)}}{2}+C$

**Correct:** $f(x)=- 2 \ln{\left(\left|{x - 1}\right| \right)}+C$

First, notice that the derivative term is already isolated on the left:

$$
\begin{aligned}f'(x) &=- \frac{2}{x - 1}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (- \frac{2}{x - 1})\,\text{d}x \\ f(x) &=\int (- \frac{2}{x - 1})\,\text{d}x \\ &=1\cdot \left(- 2 \ln{\left(\left|{x - 1}\right| \right)}\right)+C \\ &=- 2 \ln{\left(\left|{x - 1}\right| \right)}+C.\end{aligned}
$$


## Generated learning question — Easy — reciprocal — authored-direct-operations {'d': 1, 'terms': [['reciprocal', -2, -3]]}

Find the general solution to the differential equation $f'(x)=- \frac{2}{x + 3}.$

- $f(x)=- \frac{2}{x + 3}+C$
- $f(x)=- \frac{\ln{\left(\left|{x + 3}\right| \right)}}{2}+C$
- $f(x)=\ln{\left(\left|{x + 3}\right| \right)}+C$
- $f(x)=- 2 \ln{\left(\left|{x + 3}\right| \right)}+C$
- $f(x)=2 \ln{\left(\left|{x + 3}\right| \right)}+C$

**Correct:** $f(x)=- 2 \ln{\left(\left|{x + 3}\right| \right)}+C$

First, notice that the derivative term is already isolated on the left:

$$
\begin{aligned}f'(x) &=- \frac{2}{x + 3}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (- \frac{2}{x + 3})\,\text{d}x \\ f(x) &=\int (- \frac{2}{x + 3})\,\text{d}x \\ &=1\cdot \left(- 2 \ln{\left(\left|{x + 3}\right| \right)}\right)+C \\ &=- 2 \ln{\left(\left|{x + 3}\right| \right)}+C.\end{aligned}
$$


## Generated learning question — Easy — exponential — authored-direct-operations {'d': 1, 'terms': [['exp', 4, 2]]}

Find the general solution to the differential equation $f'(x)=4 e^{2 x}.$

- $f(x)=4 e^{2 x}+C$
- $f(x)=- 2 e^{2 x}+C$
- $f(x)=2 e^{2 x}+C$
- $f(x)=\frac{e^{2 x}}{2}+C$
- $f(x)=8 e^{2 x}+C$

**Correct:** $f(x)=2 e^{2 x}+C$

First, notice that the derivative term is already isolated on the left:

$$
\begin{aligned}f'(x) &=4 e^{2 x}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (4 e^{2 x})\,\text{d}x \\ f(x) &=\int (4 e^{2 x})\,\text{d}x \\ &=1\cdot \left(2 e^{2 x}\right)+C \\ &=2 e^{2 x}+C.\end{aligned}
$$


## Generated learning question — Easy — exponential — authored-direct-operations {'d': 1, 'terms': [['exp', 4, 2]]}

Find the general solution to the differential equation $f'(x)=4 e^{2 x}.$

- $f(x)=4 e^{2 x}+C$
- $f(x)=8 e^{2 x}+C$
- $f(x)=\frac{e^{2 x}}{2}+C$
- $f(x)=2 e^{2 x}+C$
- $f(x)=- 2 e^{2 x}+C$

**Correct:** $f(x)=2 e^{2 x}+C$

First, notice that the derivative term is already isolated on the left:

$$
\begin{aligned}f'(x) &=4 e^{2 x}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (4 e^{2 x})\,\text{d}x \\ f(x) &=\int (4 e^{2 x})\,\text{d}x \\ &=1\cdot \left(2 e^{2 x}\right)+C \\ &=2 e^{2 x}+C.\end{aligned}
$$


## Generated learning question — Moderate — exp_linear — authored-direct-operations {'d': 1, 'terms': [['exp', -2, 2], ['poly', 2, 1]]}

Find the general solution to the differential equation $f'(x)=- 2 e^{2 x}+2 x.$

- $f(x)=2 x - 2 e^{2 x}+C$
- $f(x)=- x^{2} + e^{2 x}+C$
- $f(x)=x^{2} - e^{2 x}+C$
- $f(x)=- e^{2 x}+C$
- $f(x)=4 x^{2} - 4 e^{2 x}+C$

**Correct:** $f(x)=x^{2} - e^{2 x}+C$

First, notice that the derivative term is already isolated on the left:

$$
\begin{aligned}f'(x) &=- 2 e^{2 x}+2 x\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (- 2 e^{2 x}+2 x)\,\text{d}x \\ f(x) &=\int (- 2 e^{2 x})\,\text{d}x+\int (2 x)\,\text{d}x \\ &=1\cdot \left(- e^{2 x}\right)+1\cdot \left(x^{2}\right)+C \\ &=- e^{2 x}+x^{2}+C.\end{aligned}
$$


## Generated learning question — Moderate — exp_linear — authored-direct-operations {'d': 1, 'terms': [['exp', 4, 4], ['poly', 3, 1]]}

Find the general solution to the differential equation $f'(x)=4 e^{4 x}+3 x.$

- $f(x)=3 x + 4 e^{4 x}+C$
- $f(x)=6 x^{2} + 16 e^{4 x}+C$
- $f(x)=e^{4 x}+C$
- $f(x)=\frac{3 x^{2}}{2} + e^{4 x}+C$
- $f(x)=- \frac{3 x^{2}}{2} - e^{4 x}+C$

**Correct:** $f(x)=\frac{3 x^{2}}{2} + e^{4 x}+C$

First, notice that the derivative term is already isolated on the left:

$$
\begin{aligned}f'(x) &=4 e^{4 x}+3 x\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (4 e^{4 x}+3 x)\,\text{d}x \\ f(x) &=\int (4 e^{4 x})\,\text{d}x+\int (3 x)\,\text{d}x \\ &=1\cdot \left(e^{4 x}\right)+1\cdot \left(\frac{3 x^{2}}{2}\right)+C \\ &=e^{4 x}+\frac{3 x^{2}}{2}+C.\end{aligned}
$$


## Generated learning question — Moderate — polynomial_pair — authored-direct-operations {'d': 1, 'terms': [['poly', 8, 1], ['poly', -3, 2]]}

Find the general solution to the differential equation $f'(x)=8 x- 3 x^{2}.$

- $f(x)=- 3 x^{2} + 8 x+C$
- $f(x)=x^{3} - 4 x^{2}+C$
- $f(x)=- x^{3} + 4 x^{2}+C$
- $f(x)=4 x^{2}+C$
- $f(x)=- 9 x^{3} + 16 x^{2}+C$

**Correct:** $f(x)=- x^{3} + 4 x^{2}+C$

First, notice that the derivative term is already isolated on the left:

$$
\begin{aligned}f'(x) &=8 x- 3 x^{2}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (8 x- 3 x^{2})\,\text{d}x \\ f(x) &=\int (8 x)\,\text{d}x+\int (- 3 x^{2})\,\text{d}x \\ &=1\cdot \left(4 x^{2}\right)+1\cdot \left(- x^{3}\right)+C \\ &=4 x^{2}- x^{3}+C.\end{aligned}
$$


## Generated learning question — Moderate — polynomial_pair — authored-direct-operations {'d': 1, 'terms': [['poly', -3, 1], ['poly', -6, 2]]}

Find the general solution to the differential equation $f'(x)=- 3 x- 6 x^{2}.$

- $f(x)=- 6 x^{2} - 3 x+C$
- $f(x)=- 18 x^{3} - 6 x^{2}+C$
- $f(x)=- \frac{3 x^{2}}{2}+C$
- $f(x)=- 2 x^{3} - \frac{3 x^{2}}{2}+C$
- $f(x)=2 x^{3} + \frac{3 x^{2}}{2}+C$

**Correct:** $f(x)=- 2 x^{3} - \frac{3 x^{2}}{2}+C$

First, notice that the derivative term is already isolated on the left:

$$
\begin{aligned}f'(x) &=- 3 x- 6 x^{2}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (- 3 x- 6 x^{2})\,\text{d}x \\ f(x) &=\int (- 3 x)\,\text{d}x+\int (- 6 x^{2})\,\text{d}x \\ &=1\cdot \left(- \frac{3 x^{2}}{2}\right)+1\cdot \left(- 2 x^{3}\right)+C \\ &=- \frac{3 x^{2}}{2}- 2 x^{3}+C.\end{aligned}
$$


## Generated learning question — Moderate — scaled_cosine — authored-direct-operations {'d': 4, 'terms': [['cos', 6, -3]]}

Find the general solution to the differential equation $4f'(x)=6 \cos{\left(3 x \right)}.$

- $f(x)=\frac{3 \cos{\left(3 x \right)}}{2}+C$
- $f(x)=- \frac{\sin{\left(3 x \right)}}{2}+C$
- $f(x)=\frac{\sin{\left(3 x \right)}}{2}+C$
- $f(x)=\frac{\sin{\left(3 x \right)}}{12}+C$
- $f(x)=\frac{9 \sin{\left(3 x \right)}}{2}+C$

**Correct:** $f(x)=\frac{\sin{\left(3 x \right)}}{2}+C$

First, we rearrange the equation to isolate the derivative term:

$$
\begin{aligned}f'(x) &=\frac{3 \cos{\left(3 x \right)}}{2}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (\frac{3 \cos{\left(3 x \right)}}{2})\,\text{d}x \\ f(x) &=\frac{1}{4}\cdot \int (6 \cos{\left(3 x \right)})\,\text{d}x \\ &=\frac{1}{4}\cdot \left(2 \sin{\left(3 x \right)}\right)+C \\ &=\frac{\sin{\left(3 x \right)}}{2}+C.\end{aligned}
$$


## Generated learning question — Moderate — scaled_cosine — authored-direct-operations {'d': -2, 'terms': [['cos', 4, -4]]}

Find the general solution to the differential equation $-2f'(x)=4 \cos{\left(4 x \right)}.$

- $f(x)=- 2 \cos{\left(4 x \right)}+C$
- $f(x)=- 8 \sin{\left(4 x \right)}+C$
- $f(x)=- \frac{\sin{\left(4 x \right)}}{8}+C$
- $f(x)=- \frac{\sin{\left(4 x \right)}}{2}+C$
- $f(x)=\frac{\sin{\left(4 x \right)}}{2}+C$

**Correct:** $f(x)=- \frac{\sin{\left(4 x \right)}}{2}+C$

First, we rearrange the equation to isolate the derivative term:

$$
\begin{aligned}f'(x) &=- 2 \cos{\left(4 x \right)}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (- 2 \cos{\left(4 x \right)})\,\text{d}x \\ f(x) &=- \frac{1}{2}\cdot \int (4 \cos{\left(4 x \right)})\,\text{d}x \\ &=- \frac{1}{2}\cdot \left(\sin{\left(4 x \right)}\right)+C \\ &=- \frac{\sin{\left(4 x \right)}}{2}+C.\end{aligned}
$$


## Generated learning question — Moderate — exp_constant — authored-direct-operations {'d': 1, 'terms': [['poly', -2, 0], ['exp', -4, -4]]}

Find the general solution to the differential equation $f'(x)=-2- 4 e^{- 4 x}.$

- $f(x)=-2 - 4 e^{- 4 x}+C$
- $f(x)=2 x - e^{- 4 x}+C$
- $f(x)=- 2 x + e^{- 4 x}+C$
- $f(x)=- 2 x+C$
- $f(x)=- 2 x + 16 e^{- 4 x}+C$

**Correct:** $f(x)=- 2 x + e^{- 4 x}+C$

First, notice that the derivative term is already isolated on the left:

$$
\begin{aligned}f'(x) &=-2- 4 e^{- 4 x}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (-2- 4 e^{- 4 x})\,\text{d}x \\ f(x) &=\int (-2)\,\text{d}x+\int (- 4 e^{- 4 x})\,\text{d}x \\ &=1\cdot \left(- 2 x\right)+1\cdot \left(e^{- 4 x}\right)+C \\ &=- 2 x+e^{- 4 x}+C.\end{aligned}
$$


## Generated learning question — Moderate — exp_constant — authored-direct-operations {'d': 1, 'terms': [['poly', 3, 0], ['exp', 3, 3]]}

Find the general solution to the differential equation $f'(x)=3+3 e^{3 x}.$

- $f(x)=3 e^{3 x} + 3+C$
- $f(x)=3 x + 9 e^{3 x}+C$
- $f(x)=3 x+C$
- $f(x)=3 x + e^{3 x}+C$
- $f(x)=- 3 x - e^{3 x}+C$

**Correct:** $f(x)=3 x + e^{3 x}+C$

First, notice that the derivative term is already isolated on the left:

$$
\begin{aligned}f'(x) &=3+3 e^{3 x}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (3+3 e^{3 x})\,\text{d}x \\ f(x) &=\int (3)\,\text{d}x+\int (3 e^{3 x})\,\text{d}x \\ &=1\cdot \left(3 x\right)+1\cdot \left(e^{3 x}\right)+C \\ &=3 x+e^{3 x}+C.\end{aligned}
$$


## Generated learning question — Hard — three_poly_exp — authored-direct-operations {'d': 4, 'terms': [['poly', 8, 1], ['poly', -2, 2], ['exp', 6, 4]]}

Find the general solution to the differential equation $4f'(x)=8 x- 2 x^{2}+6 e^{4 x}.$

- $f(x)=- \frac{x^{2}}{2} + 2 x + \frac{3 e^{4 x}}{2}+C$
- $f(x)=\frac{x^{3}}{6} - x^{2} - \frac{3 e^{4 x}}{8}+C$
- $f(x)=- \frac{x^{3}}{6} + x^{2} + \frac{3 e^{4 x}}{8}+C$
- $f(x)=- \frac{x^{3}}{6} + x^{2}+C$
- $f(x)=- \frac{3 x^{3}}{2} + 4 x^{2} + 6 e^{4 x}+C$

**Correct:** $f(x)=- \frac{x^{3}}{6} + x^{2} + \frac{3 e^{4 x}}{8}+C$

First, we rearrange the equation to isolate the derivative term:

$$
\begin{aligned}f'(x) &=2 x- \frac{x^{2}}{2}+\frac{3 e^{4 x}}{2}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (2 x- \frac{x^{2}}{2}+\frac{3 e^{4 x}}{2})\,\text{d}x \\ f(x) &=\frac{1}{4}\cdot \int (8 x)\,\text{d}x+\frac{1}{4}\cdot \int (- 2 x^{2})\,\text{d}x+\frac{1}{4}\cdot \int (6 e^{4 x})\,\text{d}x \\ &=\frac{1}{4}\cdot \left(4 x^{2}\right)+\frac{1}{4}\cdot \left(- \frac{2 x^{3}}{3}\right)+\frac{1}{4}\cdot \left(\frac{3 e^{4 x}}{2}\right)+C \\ &=x^{2}- \frac{x^{3}}{6}+\frac{3 e^{4 x}}{8}+C.\end{aligned}
$$


## Generated learning question — Hard — three_poly_exp — authored-direct-operations {'d': -2, 'terms': [['poly', -8, 1], ['poly', 4, 2], ['exp', -2, 4]]}

Find the general solution to the differential equation $-2f'(x)=- 8 x+4 x^{2}- 2 e^{4 x}.$

- $f(x)=- 2 x^{2} + 4 x + e^{4 x}+C$
- $f(x)=- 6 x^{3} + 8 x^{2} + 4 e^{4 x}+C$
- $f(x)=- \frac{2 x^{3}}{3} + 2 x^{2}+C$
- $f(x)=- \frac{2 x^{3}}{3} + 2 x^{2} + \frac{e^{4 x}}{4}+C$
- $f(x)=\frac{2 x^{3}}{3} - 2 x^{2} - \frac{e^{4 x}}{4}+C$

**Correct:** $f(x)=- \frac{2 x^{3}}{3} + 2 x^{2} + \frac{e^{4 x}}{4}+C$

First, we rearrange the equation to isolate the derivative term:

$$
\begin{aligned}f'(x) &=4 x- 2 x^{2}+e^{4 x}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (4 x- 2 x^{2}+e^{4 x})\,\text{d}x \\ f(x) &=- \frac{1}{2}\cdot \int (- 8 x)\,\text{d}x- \frac{1}{2}\cdot \int (4 x^{2})\,\text{d}x- \frac{1}{2}\cdot \int (- 2 e^{4 x})\,\text{d}x \\ &=- \frac{1}{2}\cdot \left(- 4 x^{2}\right)- \frac{1}{2}\cdot \left(\frac{4 x^{3}}{3}\right)- \frac{1}{2}\cdot \left(- \frac{e^{4 x}}{2}\right)+C \\ &=2 x^{2}- \frac{2 x^{3}}{3}+\frac{e^{4 x}}{4}+C.\end{aligned}
$$


## Generated learning question — Hard — three_trig_exp — authored-direct-operations {'d': 4, 'terms': [['sin', 8, -3], ['exp', -2, -4], ['poly', -6, 1]]}

Find the general solution to the differential equation $4f'(x)=- 8 \sin{\left(3 x \right)}- 2 e^{- 4 x}- 6 x.$

- $f(x)=- \frac{3 x}{2} - 2 \sin{\left(3 x \right)} - \frac{e^{- 4 x}}{2}+C$
- $f(x)=\frac{3 x^{2}}{4} - \frac{2 \cos{\left(3 x \right)}}{3} - \frac{e^{- 4 x}}{8}+C$
- $f(x)=- \frac{3 x^{2}}{4} + \frac{2 \cos{\left(3 x \right)}}{3} + \frac{e^{- 4 x}}{8}+C$
- $f(x)=\frac{2 \cos{\left(3 x \right)}}{3} + \frac{e^{- 4 x}}{8}+C$
- $f(x)=- 3 x^{2} + 6 \cos{\left(3 x \right)} + 2 e^{- 4 x}+C$

**Correct:** $f(x)=- \frac{3 x^{2}}{4} + \frac{2 \cos{\left(3 x \right)}}{3} + \frac{e^{- 4 x}}{8}+C$

First, we rearrange the equation to isolate the derivative term:

$$
\begin{aligned}f'(x) &=- 2 \sin{\left(3 x \right)}- \frac{e^{- 4 x}}{2}- \frac{3 x}{2}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (- 2 \sin{\left(3 x \right)}- \frac{e^{- 4 x}}{2}- \frac{3 x}{2})\,\text{d}x \\ f(x) &=\frac{1}{4}\cdot \int (- 8 \sin{\left(3 x \right)})\,\text{d}x+\frac{1}{4}\cdot \int (- 2 e^{- 4 x})\,\text{d}x+\frac{1}{4}\cdot \int (- 6 x)\,\text{d}x \\ &=\frac{1}{4}\cdot \left(\frac{8 \cos{\left(3 x \right)}}{3}\right)+\frac{1}{4}\cdot \left(\frac{e^{- 4 x}}{2}\right)+\frac{1}{4}\cdot \left(- 3 x^{2}\right)+C \\ &=\frac{2 \cos{\left(3 x \right)}}{3}+\frac{e^{- 4 x}}{8}- \frac{3 x^{2}}{4}+C.\end{aligned}
$$


## Generated learning question — Hard — three_trig_exp — authored-direct-operations {'d': -2, 'terms': [['sin', -3, 3], ['exp', -6, -2], ['poly', -8, 1]]}

Find the general solution to the differential equation $-2f'(x)=- 3 \sin{\left(3 x \right)}- 6 e^{- 2 x}- 8 x.$

- $f(x)=4 x + \frac{3 \sin{\left(3 x \right)}}{2} + 3 e^{- 2 x}+C$
- $f(x)=8 x^{2} - \frac{9 \cos{\left(3 x \right)}}{2} - 6 e^{- 2 x}+C$
- $f(x)=- \frac{\cos{\left(3 x \right)}}{2} - \frac{3 e^{- 2 x}}{2}+C$
- $f(x)=2 x^{2} - \frac{\cos{\left(3 x \right)}}{2} - \frac{3 e^{- 2 x}}{2}+C$
- $f(x)=- 2 x^{2} + \frac{\cos{\left(3 x \right)}}{2} + \frac{3 e^{- 2 x}}{2}+C$

**Correct:** $f(x)=2 x^{2} - \frac{\cos{\left(3 x \right)}}{2} - \frac{3 e^{- 2 x}}{2}+C$

First, we rearrange the equation to isolate the derivative term:

$$
\begin{aligned}f'(x) &=\frac{3 \sin{\left(3 x \right)}}{2}+3 e^{- 2 x}+4 x\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (\frac{3 \sin{\left(3 x \right)}}{2}+3 e^{- 2 x}+4 x)\,\text{d}x \\ f(x) &=- \frac{1}{2}\cdot \int (- 3 \sin{\left(3 x \right)})\,\text{d}x- \frac{1}{2}\cdot \int (- 6 e^{- 2 x})\,\text{d}x- \frac{1}{2}\cdot \int (- 8 x)\,\text{d}x \\ &=- \frac{1}{2}\cdot \left(\cos{\left(3 x \right)}\right)- \frac{1}{2}\cdot \left(3 e^{- 2 x}\right)- \frac{1}{2}\cdot \left(- 4 x^{2}\right)+C \\ &=- \frac{\cos{\left(3 x \right)}}{2}- \frac{3 e^{- 2 x}}{2}+2 x^{2}+C.\end{aligned}
$$


## Generated learning question — Hard — three_reciprocal_exp — authored-direct-operations {'d': 4, 'terms': [['reciprocal', 2, 0], ['exp', 6, -4], ['poly', 2, 1]]}

Find the general solution to the differential equation $4f'(x)=\frac{2}{x}+6 e^{- 4 x}+2 x.$

- $f(x)=\frac{x}{2} + \frac{3 e^{- 4 x}}{2} + \frac{1}{2 x}+C$
- $f(x)=- \frac{x^{2}}{4} - \frac{\ln{\left(\left|{x}\right| \right)}}{2} + \frac{3 e^{- 4 x}}{8}+C$
- $f(x)=\frac{x^{2}}{4} + \frac{\ln{\left(\left|{x}\right| \right)}}{2} - \frac{3 e^{- 4 x}}{8}+C$
- $f(x)=\frac{\ln{\left(\left|{x}\right| \right)}}{2} - \frac{3 e^{- 4 x}}{8}+C$
- $f(x)=x^{2} + \frac{\ln{\left(\left|{x}\right| \right)}}{8} - 6 e^{- 4 x}+C$

**Correct:** $f(x)=\frac{x^{2}}{4} + \frac{\ln{\left(\left|{x}\right| \right)}}{2} - \frac{3 e^{- 4 x}}{8}+C$

First, we rearrange the equation to isolate the derivative term:

$$
\begin{aligned}f'(x) &=\frac{1}{2 x}+\frac{3 e^{- 4 x}}{2}+\frac{x}{2}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (\frac{1}{2 x}+\frac{3 e^{- 4 x}}{2}+\frac{x}{2})\,\text{d}x \\ f(x) &=\frac{1}{4}\cdot \int (\frac{2}{x})\,\text{d}x+\frac{1}{4}\cdot \int (6 e^{- 4 x})\,\text{d}x+\frac{1}{4}\cdot \int (2 x)\,\text{d}x \\ &=\frac{1}{4}\cdot \left(2 \ln{\left(\left|{x}\right| \right)}\right)+\frac{1}{4}\cdot \left(- \frac{3 e^{- 4 x}}{2}\right)+\frac{1}{4}\cdot \left(x^{2}\right)+C \\ &=\frac{\ln{\left(\left|{x}\right| \right)}}{2}- \frac{3 e^{- 4 x}}{8}+\frac{x^{2}}{4}+C.\end{aligned}
$$


## Generated learning question — Hard — three_reciprocal_exp — authored-direct-operations {'d': -2, 'terms': [['reciprocal', -8, -3], ['exp', 6, -4], ['poly', 3, 1]]}

Find the general solution to the differential equation $-2f'(x)=- \frac{8}{x + 3}+6 e^{- 4 x}+3 x.$

- $f(x)=- \frac{3 x}{2} - 3 e^{- 4 x} + \frac{4}{x + 3}+C$
- $f(x)=- 3 x^{2} + \frac{\ln{\left(\left|{x + 3}\right| \right)}}{16} + 12 e^{- 4 x}+C$
- $f(x)=4 \ln{\left(\left|{x + 3}\right| \right)} + \frac{3 e^{- 4 x}}{4}+C$
- $f(x)=- \frac{3 x^{2}}{4} + 4 \ln{\left(\left|{x + 3}\right| \right)} + \frac{3 e^{- 4 x}}{4}+C$
- $f(x)=\frac{3 x^{2}}{4} - 4 \ln{\left(\left|{x + 3}\right| \right)} - \frac{3 e^{- 4 x}}{4}+C$

**Correct:** $f(x)=- \frac{3 x^{2}}{4} + 4 \ln{\left(\left|{x + 3}\right| \right)} + \frac{3 e^{- 4 x}}{4}+C$

First, we rearrange the equation to isolate the derivative term:

$$
\begin{aligned}f'(x) &=\frac{4}{x + 3}- 3 e^{- 4 x}- \frac{3 x}{2}\end{aligned}
$$

Then, we integrate both sides of the equation with respect to $x,$ and we get

$$
\begin{aligned}\int f\prime(x)\,\text{d}x &=\int (\frac{4}{x + 3}- 3 e^{- 4 x}- \frac{3 x}{2})\,\text{d}x \\ f(x) &=- \frac{1}{2}\cdot \int (- \frac{8}{x + 3})\,\text{d}x- \frac{1}{2}\cdot \int (6 e^{- 4 x})\,\text{d}x- \frac{1}{2}\cdot \int (3 x)\,\text{d}x \\ &=- \frac{1}{2}\cdot \left(- 8 \ln{\left(\left|{x + 3}\right| \right)}\right)- \frac{1}{2}\cdot \left(- \frac{3 e^{- 4 x}}{2}\right)- \frac{1}{2}\cdot \left(\frac{3 x^{2}}{2}\right)+C \\ &=4 \ln{\left(\left|{x + 3}\right| \right)}+\frac{3 e^{- 4 x}}{4}- \frac{3 x^{2}}{4}+C.\end{aligned}
$$