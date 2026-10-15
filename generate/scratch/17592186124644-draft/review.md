# Original and generated review

Original source records are immutable in source.json. The source-facing replay uses normalized TeX and preserves every original absent attribute. Generated examples below use the method-derived complete bank and are eligible for local review.

## Original q-132257

For the function $f(x, y) = y^{2}\tan x + \frac{y}{x}$, evaluate $\frac{∂f}{∂x}$ at the point $(π, 2)$.

Bank: $2 - \frac{4}{π^{2}}$, $1 - \frac{2}{π^{2}}$, $4 - π^{2}$, $\frac{2}{π^{2}}$, $4 - \frac{2}{π^{2}}$

No original solution or correct designation.

### Generated variant (hard)

Difficulty: hard · Template: `tan-reciprocal` · Profile: `method-sum-bank`

For the function $f(x, y) =4 x^{2} \tan{(y )}+\frac{4 x}{y}$, evaluate $\frac{∂f}{∂y}$ at the point $(3,- 2 \pi)$.

- $\frac{3}{\pi^{2}} + 36$
- $36 - \frac{3}{\pi^{2}}$ **(correct)**
- $- \frac{3}{\pi^{2}}$
- $-36 - \frac{3}{\pi^{2}}$
- $36$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(4 x^{2} \tan{(y )}+\frac{4 x}{y}) \\  & =\frac{∂}{∂y}(4 x^{2} \tan{(y )})+\frac{∂}{∂y}(\frac{4 x}{y}) \\  & =4 x^{2}\cdot \frac{∂}{∂y}(\tan{(y )})+4 x\cdot \frac{∂}{∂y}(\frac{1}{y}) \\  & =4 x^{2}\cdot (\sec^{2}{(y )})+4 x\cdot (- \frac{1}{y^{2}}) \\  & =4 x^{2} \sec^{2}{(y )}-\frac{4 x}{y^{2}}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(3,- 2 \pi):$

$$
\begin{aligned}\frac{∂f}{∂y}{|}_{(3,- 2 \pi)} & =4 (3)^{2} \sec^{2}{((- 2 \pi) )}-\frac{4 (3)}{(- 2 \pi)^{2}} \\  & =36-(\frac{3}{\pi^{2}}) \\  & =36 - \frac{3}{\pi^{2}}\end{aligned}
$$

### Generated variant (hard)

Difficulty: hard · Template: `tan-reciprocal` · Profile: `method-sum-bank`

For the function $f(x, y) =2 x^{2} \tan{(y )}+\frac{x}{y}$, evaluate $\frac{∂f}{∂y}$ at the point $(3,- 2 \pi)$.

- $-18 - \frac{3}{4 \pi^{2}}$
- $- \frac{3}{4 \pi^{2}}$
- $18 - \frac{3}{4 \pi^{2}}$ **(correct)**
- $\frac{3}{4 \pi^{2}} + 18$
- $18$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(2 x^{2} \tan{(y )}+\frac{x}{y}) \\  & =\frac{∂}{∂y}(2 x^{2} \tan{(y )})+\frac{∂}{∂y}(\frac{x}{y}) \\  & =2 x^{2}\cdot \frac{∂}{∂y}(\tan{(y )})+x\cdot \frac{∂}{∂y}(\frac{1}{y}) \\  & =2 x^{2}\cdot (\sec^{2}{(y )})+x\cdot (- \frac{1}{y^{2}}) \\  & =2 x^{2} \sec^{2}{(y )}-\frac{x}{y^{2}}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(3,- 2 \pi):$

$$
\begin{aligned}\frac{∂f}{∂y}{|}_{(3,- 2 \pi)} & =2 (3)^{2} \sec^{2}{((- 2 \pi) )}-\frac{(3)}{(- 2 \pi)^{2}} \\  & =18-(\frac{3}{4 \pi^{2}}) \\  & =18 - \frac{3}{4 \pi^{2}}\end{aligned}
$$

## Original q-159604

For the function $f(x, y) = 2^{x}\tan y + \frac{y}{πx^{2}}$, evaluate $f_{x}(1, \frac{π}{4})$.

Bank: $2\ln 2 - \frac{1}{2}$, $\frac{1}{\ln 2}$, $2\ln 2$, $\ln 2 - 1$, $4\ln 2 - \frac{π}{2}$

No original solution or correct designation.

### Generated variant (hard)

Difficulty: hard · Template: `base-exponential-tan` · Profile: `method-sum-bank`

For the function $f(x, y) =4 \cdot 2^{y} \tan{(x )}+\frac{4 x}{\pi y^{2}}$, evaluate $f_{y}(\frac{3 \pi}{4},3)$.

- $- \frac{2}{9}$
- $- 32 \ln{(2 )} - \frac{2}{9}$ **(correct)**
- $\frac{2}{9} - 32 \ln{(2 )}$
- $- 32 \ln{(2 )}$
- $- \frac{2}{9} + 32 \ln{(2 )}$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{y}(x,y) & =\frac{∂}{∂y}(4 \cdot 2^{y} \tan{(x )}+\frac{4 x}{\pi y^{2}}) \\  & =\frac{∂}{∂y}(4 \cdot 2^{y} \tan{(x )})+\frac{∂}{∂y}(\frac{4 x}{\pi y^{2}}) \\  & =4 \tan{(x )}\cdot \frac{∂}{∂y}(2^{y})+\frac{4 x}{\pi}\cdot \frac{∂}{∂y}(\frac{1}{y^{2}}) \\  & =4 \tan{(x )}\cdot (2^{y} \ln{(2 )})+\frac{4 x}{\pi}\cdot (- \frac{2}{y^{3}}) \\  & =4 \cdot 2^{y} \ln{(2 )} \tan{(x )}-\frac{8 x}{\pi y^{3}}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(\frac{3 \pi}{4},3):$

$$
\begin{aligned}{f}_{y}(\frac{3 \pi}{4},3) & =4 \cdot 2^{(3)} \ln{(2 )} \tan{((\frac{3 \pi}{4}) )}-\frac{8 (\frac{3 \pi}{4})}{\pi (3)^{3}} \\  & =- 32 \ln{(2 )}-(\frac{2}{9}) \\  & =- 32 \ln{(2 )} - \frac{2}{9}\end{aligned}
$$

### Generated variant (hard)

Difficulty: hard · Template: `base-exponential-tan` · Profile: `method-sum-bank`

For the function $f(x, y) =2 \cdot 2^{y} \tan{(x )}+\frac{x}{\pi y^{3}}$, evaluate $f_{y}(\frac{3 \pi}{4},2)$.

- $- \frac{9}{64} + 8 \ln{(2 )}$
- $- \frac{9}{64}$
- $- 8 \ln{(2 )} - \frac{9}{64}$ **(correct)**
- $\frac{9}{64} - 8 \ln{(2 )}$
- $- 8 \ln{(2 )}$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{y}(x,y) & =\frac{∂}{∂y}(2 \cdot 2^{y} \tan{(x )}+\frac{x}{\pi y^{3}}) \\  & =\frac{∂}{∂y}(2 \cdot 2^{y} \tan{(x )})+\frac{∂}{∂y}(\frac{x}{\pi y^{3}}) \\  & =2 \tan{(x )}\cdot \frac{∂}{∂y}(2^{y})+\frac{x}{\pi}\cdot \frac{∂}{∂y}(\frac{1}{y^{3}}) \\  & =2 \tan{(x )}\cdot (2^{y} \ln{(2 )})+\frac{x}{\pi}\cdot (- \frac{3}{y^{4}}) \\  & =2 \cdot 2^{y} \ln{(2 )} \tan{(x )}-\frac{3 x}{\pi y^{4}}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(\frac{3 \pi}{4},2):$

$$
\begin{aligned}{f}_{y}(\frac{3 \pi}{4},2) & =2 \cdot 2^{(2)} \ln{(2 )} \tan{((\frac{3 \pi}{4}) )}-\frac{3 (\frac{3 \pi}{4})}{\pi (2)^{4}} \\  & =- 8 \ln{(2 )}-(\frac{9}{64}) \\  & =- 8 \ln{(2 )} - \frac{9}{64}\end{aligned}
$$

## Original q-159585

For the function $f(x,y)=\operatorname{sin}⁡x\operatorname{cos}⁡y-xy,$ evaluate ${f}_{x}(0,\pi ).$

Bank: $\pi +1$, $1-\pi $, $-\pi -1$, ${\pi }^{2}+1$, $1-{\pi }^{2}$

We differentiate the given function with respect to $x,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(\operatorname{sin}⁡x\operatorname{cos}⁡y-xy) \\  & =\frac{∂}{∂x}(\operatorname{sin}⁡x\operatorname{cos}⁡y)-\frac{∂}{∂x}(xy) \\  & =\operatorname{cos}⁡y\cdot \frac{∂}{∂x}(\operatorname{sin}⁡x)-y\cdot \frac{∂}{∂x}(x) \\  & =\operatorname{cos}⁡y\cdot (\operatorname{cos}⁡x)-y\cdot (1) \\  & =\operatorname{cos}⁡y\operatorname{cos}⁡x-y\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(0,\pi ):$

$$
\begin{aligned}{f}_{x}(0,\pi ) & =\operatorname{cos}⁡\pi \operatorname{cos}⁡0-\pi  \\  & =(-1)\cdot 1-\pi  \\  & =-\pi -1\end{aligned}
$$

### Generated variant (hard)

Difficulty: hard · Template: `sin-cos-linear` · Profile: `method-sum-bank`

For the function $f(x,y)=4 \sin{(y )} \cos{(x )}-4 y x,$ evaluate ${f}_{y}(- 2 \pi,2 \pi).$

- $4 - 8 \pi$
- $4 + 8 \pi$ **(correct)**
- $8 \pi$
- $-4 + 8 \pi$
- $4$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{y}(x,y) & =\frac{∂}{∂y}(4 \sin{(y )} \cos{(x )}-4 y x) \\  & =\frac{∂}{∂y}(4 \sin{(y )} \cos{(x )})-\frac{∂}{∂y}(4 y x) \\  & =4 \cos{(x )}\cdot \frac{∂}{∂y}(\sin{(y )})-4 x\cdot \frac{∂}{∂y}(y) \\  & =4 \cos{(x )}\cdot (\cos{(y )})-4 x\cdot (1) \\  & =4 \cos{(y )} \cos{(x )}-4 x\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(- 2 \pi,2 \pi):$

$$
\begin{aligned}{f}_{y}(- 2 \pi,2 \pi) & =4 \cos{((2 \pi) )} \cos{((- 2 \pi) )}-4 (- 2 \pi) \\  & =(4)\cdot (1)-(- 8 \pi) \\  & =4 + 8 \pi\end{aligned}
$$

### Generated variant (hard)

Difficulty: hard · Template: `sin-cos-linear` · Profile: `method-sum-bank`

For the function $f(x,y)=2 \sin{(y )} \cos{(x )}-y x,$ evaluate ${f}_{y}(- 2 \pi,2 \pi).$

- $-2 + 2 \pi$
- $2 \pi$
- $2 + 2 \pi$ **(correct)**
- $2 - 2 \pi$
- $2$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{y}(x,y) & =\frac{∂}{∂y}(2 \sin{(y )} \cos{(x )}-y x) \\  & =\frac{∂}{∂y}(2 \sin{(y )} \cos{(x )})-\frac{∂}{∂y}(y x) \\  & =2 \cos{(x )}\cdot \frac{∂}{∂y}(\sin{(y )})-x\cdot \frac{∂}{∂y}(y) \\  & =2 \cos{(x )}\cdot (\cos{(y )})-x\cdot (1) \\  & =2 \cos{(y )} \cos{(x )}-x\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(- 2 \pi,2 \pi):$

$$
\begin{aligned}{f}_{y}(- 2 \pi,2 \pi) & =2 \cos{((2 \pi) )} \cos{((- 2 \pi) )}-(- 2 \pi) \\  & =(2)\cdot (1)-(- 2 \pi) \\  & =2 + 2 \pi\end{aligned}
$$

## Original q-159597

For the function $f(x,y)={x}^{3}\operatorname{ln}⁡y-2y\sqrt{x},$ evaluate $\frac{∂f}{∂x}$ at the point $(1,e).$

Bank: $3$, $3-e$, $3e$, $2e$, $1+e$

We differentiate the given function with respect to $x,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂}{∂x}({x}^{3}\operatorname{ln}⁡y-2y\sqrt{x}) \\  & =\frac{∂}{∂x}({x}^{3}\operatorname{ln}⁡y)-\frac{∂}{∂x}(2y\sqrt{x}) \\  & =\operatorname{ln}⁡y\cdot \frac{∂}{∂x}({x}^{3})-2y\cdot \frac{∂}{∂x}(\sqrt{x}) \\  & =\operatorname{ln}⁡y\cdot (3{x}^{2})-2y\cdot (\frac{1}{2\sqrt{x}}) \\  & =3{x}^{2}\operatorname{ln}⁡y-\frac{y}{\sqrt{x}}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(1,e):$

$$
\begin{aligned}\frac{∂f}{∂x}{|}_{(1,e)} & =3\cdot {1}^{2}\cdot \operatorname{ln}⁡e-\frac{e}{\sqrt{1}} \\  & =3-e\end{aligned}
$$

### Generated variant (moderate)

Difficulty: moderate · Template: `power-log-root` · Profile: `method-sum-bank`

For the function $f(x,y)=4 y^{2} \ln{(x )}-4 \sqrt{y} x,$ evaluate $\frac{∂f}{∂y}$ at the point $(e^{2},9).$

- $- \frac{2 \cdot e^{2}}{3}$
- $144 - \frac{2 \cdot e^{2}}{3}$ **(correct)**
- $\frac{2 \cdot e^{2}}{3} + 144$
- $144$
- $-144 - \frac{2 \cdot e^{2}}{3}$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(4 y^{2} \ln{(x )}-4 \sqrt{y} x) \\  & =\frac{∂}{∂y}(4 y^{2} \ln{(x )})-\frac{∂}{∂y}(4 \sqrt{y} x) \\  & =4 \ln{(x )}\cdot \frac{∂}{∂y}(y^{2})-4 x\cdot \frac{∂}{∂y}(\sqrt{y}) \\  & =4 \ln{(x )}\cdot (2 y)-4 x\cdot (\frac{1}{2 \sqrt{y}}) \\  & =8 y \ln{(x )}-\frac{2 x}{\sqrt{y}}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(e^{2},9):$

$$
\begin{aligned}\frac{∂f}{∂y}{|}_{(e^{2},9)} & =8 (9) \ln{((e^{2}) )}-\frac{2 (e^{2})}{\sqrt{(9)}} \\  & =144 - \frac{2 \cdot e^{2}}{3}\end{aligned}
$$

### Generated variant (moderate)

Difficulty: moderate · Template: `power-log-root` · Profile: `method-sum-bank`

For the function $f(x,y)=2 y^{3} \ln{(x )}-\sqrt{y} x,$ evaluate $\frac{∂f}{∂y}$ at the point $(e^{2},4).$

- $-192 - \frac{e^{2}}{4}$
- $- \frac{e^{2}}{4}$
- $192 - \frac{e^{2}}{4}$ **(correct)**
- $\frac{e^{2}}{4} + 192$
- $192$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(2 y^{3} \ln{(x )}-\sqrt{y} x) \\  & =\frac{∂}{∂y}(2 y^{3} \ln{(x )})-\frac{∂}{∂y}(\sqrt{y} x) \\  & =2 \ln{(x )}\cdot \frac{∂}{∂y}(y^{3})-x\cdot \frac{∂}{∂y}(\sqrt{y}) \\  & =2 \ln{(x )}\cdot (3 y^{2})-x\cdot (\frac{1}{2 \sqrt{y}}) \\  & =6 y^{2} \ln{(x )}-\frac{x}{2 \sqrt{y}}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(e^{2},4):$

$$
\begin{aligned}\frac{∂f}{∂y}{|}_{(e^{2},4)} & =6 (4)^{2} \ln{((e^{2}) )}-\frac{(e^{2})}{2 \sqrt{(4)}} \\  & =192 - \frac{e^{2}}{4}\end{aligned}
$$

## Original q-159599

For the function $f(x,y)={e}^{x}\operatorname{ln}⁡y+{x}^{7}y,$ evaluate $\frac{∂f}{∂y}$ at the point $(1,\frac{1}{2}).$

Bank: ${e}^{2}+1$, $2e+1$, $e+1$, $\frac{1}{2}e+1$, $2e$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}({e}^{x}\operatorname{ln}⁡y+{x}^{7}y) \\  & =\frac{∂}{∂y}({e}^{x}\operatorname{ln}⁡y)+\frac{∂}{∂y}({x}^{7}y) \\  & ={e}^{x}\cdot \frac{∂}{∂y}(\operatorname{ln}⁡y)+{x}^{7}\cdot \frac{∂}{∂y}(y) \\  & ={e}^{x}\cdot (\frac{1}{y})+{x}^{7}\cdot (1) \\  & =\frac{{e}^{x}}{y}+{x}^{7}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(1,\frac{1}{2}):$

$$
\begin{aligned}\frac{∂f}{∂y}{|}_{(1,1/2)} & =\frac{{e}^{1}}{(\frac{1}{2})}+{1}^{7} \\  & =2e+1\end{aligned}
$$

### Generated variant (moderate)

Difficulty: moderate · Template: `exp-log-power` · Profile: `method-sum-bank`

For the function $f(x,y)=4 \cdot e^{x} \ln{(y )}+4 y x^{3},$ evaluate $\frac{∂f}{∂y}$ at the point $(2,3).$

- $-32 + \frac{4 \cdot e^{2}}{3}$
- $\frac{4 \cdot e^{2}}{3} + 32$ **(correct)**
- $32$
- $32 - \frac{4 \cdot e^{2}}{3}$
- $\frac{4 \cdot e^{2}}{3}$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(4 \cdot e^{x} \ln{(y )}+4 y x^{3}) \\  & =\frac{∂}{∂y}(4 \cdot e^{x} \ln{(y )})+\frac{∂}{∂y}(4 y x^{3}) \\  & =4 \cdot e^{x}\cdot \frac{∂}{∂y}(\ln{(y )})+4 x^{3}\cdot \frac{∂}{∂y}(y) \\  & =4 \cdot e^{x}\cdot (\frac{1}{y})+4 x^{3}\cdot (1) \\  & =\frac{4 \cdot e^{x}}{y}+4 x^{3}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(2,3):$

$$
\begin{aligned}\frac{∂f}{∂y}{|}_{(2,3)} & =\frac{4 \cdot e^{(2)}}{(3)}+4 (2)^{3} \\  & =\frac{4 \cdot e^{2}}{3} + 32\end{aligned}
$$

### Generated variant (moderate)

Difficulty: moderate · Template: `exp-log-power` · Profile: `method-sum-bank`

For the function $f(x,y)=2 \cdot e^{x} \ln{(y )}+y x^{5},$ evaluate $\frac{∂f}{∂y}$ at the point $(2,3).$

- $32 - \frac{2 \cdot e^{2}}{3}$
- $32$
- $\frac{2 \cdot e^{2}}{3} + 32$ **(correct)**
- $-32 + \frac{2 \cdot e^{2}}{3}$
- $\frac{2 \cdot e^{2}}{3}$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(2 \cdot e^{x} \ln{(y )}+y x^{5}) \\  & =\frac{∂}{∂y}(2 \cdot e^{x} \ln{(y )})+\frac{∂}{∂y}(y x^{5}) \\  & =2 \cdot e^{x}\cdot \frac{∂}{∂y}(\ln{(y )})+x^{5}\cdot \frac{∂}{∂y}(y) \\  & =2 \cdot e^{x}\cdot (\frac{1}{y})+x^{5}\cdot (1) \\  & =\frac{2 \cdot e^{x}}{y}+x^{5}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(2,3):$

$$
\begin{aligned}\frac{∂f}{∂y}{|}_{(2,3)} & =\frac{2 \cdot e^{(2)}}{(3)}+(2)^{5} \\  & =\frac{2 \cdot e^{2}}{3} + 32\end{aligned}
$$

## Original q-159602

For the function $f(x,y)=4y{x}^{2}-x{y}^{4},$ evaluate $\frac{∂f}{∂y}$ at the point $(2,1).$

Bank: $16$, $2$, $4$, $1$, $8$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(4y{x}^{2}-x{y}^{4}) \\  & =\frac{∂}{∂y}(4y{x}^{2})-\frac{∂}{∂y}(x{y}^{4}) \\  & =4{x}^{2}\cdot \frac{∂}{∂y}(y)-x\cdot \frac{∂}{∂y}({y}^{4}) \\  & =4{x}^{2}\cdot (1)-x\cdot (4{y}^{3}) \\  & =4{x}^{2}-4x{y}^{3}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(2,1):$

$$
\begin{aligned}\frac{∂f}{∂y}{|}_{(2,1)} & =4\cdot {2}^{2}-4\cdot 2\cdot {1}^{3} \\  & =16-8 \\  & =8\end{aligned}
$$

### Generated variant (moderate)

Difficulty: moderate · Template: `polynomial` · Profile: `method-sum-bank`

For the function $f(x,y)=4 y x^{2}-4 y^{3} x,$ evaluate $\frac{∂f}{∂y}$ at the point $(1,3).$

- $-108$
- $-104$ **(correct)**
- $112$
- $4$
- $-112$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(4 y x^{2}-4 y^{3} x) \\  & =\frac{∂}{∂y}(4 y x^{2})-\frac{∂}{∂y}(4 y^{3} x) \\  & =4 x^{2}\cdot \frac{∂}{∂y}(y)-4 x\cdot \frac{∂}{∂y}(y^{3}) \\  & =4 x^{2}\cdot (1)-4 x\cdot (3 y^{2}) \\  & =4 x^{2}-12 y^{2} x\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(1,3):$

$$
\begin{aligned}\frac{∂f}{∂y}{|}_{(1,3)} & =4 (1)^{2}-12 (3)^{2} (1) \\  & =4-(108) \\  & =-104\end{aligned}
$$

### Generated variant (moderate)

Difficulty: moderate · Template: `polynomial` · Profile: `method-sum-bank`

For the function $f(x,y)=2 y x^{2}-y^{4} x,$ evaluate $\frac{∂f}{∂y}$ at the point $(1,2).$

- $-34$
- $-32$
- $-30$ **(correct)**
- $34$
- $2$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(2 y x^{2}-y^{4} x) \\  & =\frac{∂}{∂y}(2 y x^{2})-\frac{∂}{∂y}(y^{4} x) \\  & =2 x^{2}\cdot \frac{∂}{∂y}(y)-x\cdot \frac{∂}{∂y}(y^{4}) \\  & =2 x^{2}\cdot (1)-x\cdot (4 y^{3}) \\  & =2 x^{2}-4 y^{3} x\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(1,2):$

$$
\begin{aligned}\frac{∂f}{∂y}{|}_{(1,2)} & =2 (1)^{2}-4 (2)^{3} (1) \\  & =2-(32) \\  & =-30\end{aligned}
$$

## Original q-159607

For the function $f(x,y)=x\operatorname{sec}⁡y+{x}^{4}y,$ evaluate ${f}_{y}(\sqrt{2},\frac{\pi }{4}).$

Bank: $6$, $8$, $4$, $3$, $2$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{y}(x,y) & =\frac{∂}{∂y}(x\operatorname{sec}⁡y+{x}^{4}y) \\  & =\frac{∂}{∂y}(x\operatorname{sec}⁡y)+\frac{∂}{∂y}({x}^{4}y) \\  & =x\cdot \frac{∂}{∂y}(\operatorname{sec}⁡y)+{x}^{4}\cdot \frac{∂}{∂y}(y) \\  & =x\cdot (\operatorname{sec}⁡y\operatorname{tan}⁡y)+{x}^{4}\cdot (1) \\  & =x\operatorname{sec}⁡y\operatorname{tan}⁡y+{x}^{4}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(\sqrt{2},\frac{\pi }{4}):$

$$
\begin{aligned}{f}_{y}(\sqrt{2},\frac{\pi }{4}) & =\sqrt{2}\cdot \operatorname{sec}⁡(\frac{\pi }{4})\cdot \operatorname{tan}⁡(\frac{\pi }{4})+{(\sqrt{2})}^{4} \\  & =\sqrt{2}\cdot \sqrt{2}\cdot 1+4 \\  & =6\end{aligned}
$$

### Generated variant (hard)

Difficulty: hard · Template: `sec-power` · Profile: `method-sum-bank`

For the function $f(x,y)=3 x \sec{(y )}+4 y x^{4},$ evaluate ${f}_{y}(\sqrt{2},\frac{3 \pi}{4}).$

- $6$
- $16$
- $10$
- $22$ **(correct)**
- $-10$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{y}(x,y) & =\frac{∂}{∂y}(3 x \sec{(y )}+4 y x^{4}) \\  & =\frac{∂}{∂y}(3 x \sec{(y )})+\frac{∂}{∂y}(4 y x^{4}) \\  & =3 x\cdot \frac{∂}{∂y}(\sec{(y )})+4 x^{4}\cdot \frac{∂}{∂y}(y) \\  & =3 x\cdot (\sec{(y )} \tan{(y )})+4 x^{4}\cdot (1) \\  & =3 x \sec{(y )} \tan{(y )}+4 x^{4}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(\sqrt{2},\frac{3 \pi}{4}):$

$$
\begin{aligned}{f}_{y}(\sqrt{2},\frac{3 \pi}{4}) & =3 (\sqrt{2}) \sec{((\frac{3 \pi}{4}) )} \tan{((\frac{3 \pi}{4}) )}+4 (\sqrt{2})^{4} \\  & =(3 \sqrt{2})\cdot (- \sqrt{2})\cdot (-1)+(16) \\  & =22\end{aligned}
$$

### Generated variant (hard)

Difficulty: hard · Template: `sec-power` · Profile: `method-sum-bank`

For the function $f(x,y)=2 x \sec{(y )}+y x^{4},$ evaluate ${f}_{y}(2 \sqrt{2},- \frac{\pi}{4}).$

- $72$
- $64$
- $56$ **(correct)**
- $-72$
- $-8$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{y}(x,y) & =\frac{∂}{∂y}(2 x \sec{(y )}+y x^{4}) \\  & =\frac{∂}{∂y}(2 x \sec{(y )})+\frac{∂}{∂y}(y x^{4}) \\  & =2 x\cdot \frac{∂}{∂y}(\sec{(y )})+x^{4}\cdot \frac{∂}{∂y}(y) \\  & =2 x\cdot (\sec{(y )} \tan{(y )})+x^{4}\cdot (1) \\  & =2 x \sec{(y )} \tan{(y )}+x^{4}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(2 \sqrt{2},- \frac{\pi}{4}):$

$$
\begin{aligned}{f}_{y}(2 \sqrt{2},- \frac{\pi}{4}) & =2 (2 \sqrt{2}) \sec{((- \frac{\pi}{4}) )} \tan{((- \frac{\pi}{4}) )}+(2 \sqrt{2})^{4} \\  & =(4 \sqrt{2})\cdot (\sqrt{2})\cdot (-1)+(64) \\  & =56\end{aligned}
$$

## Original q-159587

For the function $f(x,y)={y}^{2}\sqrt{x}+\frac{x}{y},$ evaluate $\frac{∂f}{∂y}$ at the point $(4,2).$

Bank: $\frac{7}{2}$, $\frac{9}{2}$, $9$, $7$, $6$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}({y}^{2}\sqrt{x}+\frac{x}{y}) \\  & =\frac{∂}{∂y}({y}^{2}\sqrt{x}+x{y}^{-1}) \\  & =\frac{∂}{∂y}({y}^{2}\sqrt{x})+\frac{∂}{∂y}(x{y}^{-1}) \\  & =\sqrt{x}\cdot \frac{∂}{∂y}({y}^{2})+x\cdot \frac{∂}{∂y}({y}^{-1}) \\  & =\sqrt{x}\cdot (2y)+x\cdot (-{y}^{-2}) \\  & =2y\sqrt{x}-x{y}^{-2}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(4,2):$

$$
\begin{aligned}\frac{∂f}{∂y}{|}_{(4,2)} & =2\cdot 2\cdot \sqrt{4}-4\cdot {2}^{-2} \\  & =8-1 \\  & =7\end{aligned}
$$

### Generated variant (moderate)

Difficulty: moderate · Template: `root-reciprocal` · Profile: `method-sum-bank`

For the function $f(x,y)=4 y^{2} \sqrt{x}+\frac{4 x}{y},$ evaluate $\frac{∂f}{∂y}$ at the point $(16,4).$

- $132$
- $124$ **(correct)**
- $-4$
- $-132$
- $128$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(4 y^{2} \sqrt{x}+\frac{4 x}{y}) \\  & =\frac{∂}{∂y}(4 y^{2} \sqrt{x}+4 x{y}^{-1}) \\  & =\frac{∂}{∂y}(4 y^{2} \sqrt{x})+\frac{∂}{∂y}(4 x{y}^{-1}) \\  & =4 \sqrt{x}\cdot \frac{∂}{∂y}(y^{2})+4 x\cdot \frac{∂}{∂y}({y}^{-1}) \\  & =4 \sqrt{x}\cdot (2 y)+4 x\cdot (-{y}^{-2}) \\  & =8 y \sqrt{x}-4 x{y}^{-2}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(16,4):$

$$
\begin{aligned}\frac{∂f}{∂y}{|}_{(16,4)} & =8 (4) \sqrt{(16)}-4 (16){(4)}^{-2} \\  & =128-(4) \\  & =124\end{aligned}
$$

### Generated variant (moderate)

Difficulty: moderate · Template: `root-reciprocal` · Profile: `method-sum-bank`

For the function $f(x,y)=2 y^{3} \sqrt{x}+\frac{x}{y},$ evaluate $\frac{∂f}{∂y}$ at the point $(16,4).$

- $-385$
- $-1$
- $383$ **(correct)**
- $385$
- $384$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(2 y^{3} \sqrt{x}+\frac{x}{y}) \\  & =\frac{∂}{∂y}(2 y^{3} \sqrt{x}+x{y}^{-1}) \\  & =\frac{∂}{∂y}(2 y^{3} \sqrt{x})+\frac{∂}{∂y}(x{y}^{-1}) \\  & =2 \sqrt{x}\cdot \frac{∂}{∂y}(y^{3})+x\cdot \frac{∂}{∂y}({y}^{-1}) \\  & =2 \sqrt{x}\cdot (3 y^{2})+x\cdot (-{y}^{-2}) \\  & =6 y^{2} \sqrt{x}-x{y}^{-2}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(16,4):$

$$
\begin{aligned}\frac{∂f}{∂y}{|}_{(16,4)} & =6 (4)^{2} \sqrt{(16)}-(16){(4)}^{-2} \\  & =384-(1) \\  & =383\end{aligned}
$$

## Original q-159600

For the function $f(x,y)=2x\sqrt{y}-4y\sqrt{x},$ evaluate $\frac{∂f}{∂x}$ at the point $(1,4).$

Bank: $-8$, $2$, $-4$, $4$, $0$

We differentiate the given function with respect to $x,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂}{∂x}(2x\sqrt{y}-4y\sqrt{x}) \\  & =\frac{∂}{∂x}(2x\sqrt{y})-\frac{∂}{∂x}(4y\sqrt{x}) \\  & =2\sqrt{y}\cdot \frac{∂}{∂x}(x)-4y\cdot \frac{∂}{∂x}(\sqrt{x}) \\  & =2\sqrt{y}\cdot (1)-4y\cdot (\frac{1}{2\sqrt{x}}) \\  & =2\sqrt{y}-\frac{2y}{\sqrt{x}}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(1,4):$

$$
\begin{aligned}\frac{∂f}{∂x}{|}_{(1,4)} & =2\sqrt{4}-\frac{2\cdot 4}{\sqrt{1}} \\  & =4-8 \\  & =-4\end{aligned}
$$

### Generated variant (moderate)

Difficulty: moderate · Template: `cross-roots` · Profile: `method-sum-bank`

For the function $f(x,y)=4 y \sqrt{x}-4 \sqrt{y} x,$ evaluate $\frac{∂f}{∂y}$ at the point $(4,9).$

- $- \frac{8}{3}$
- $\frac{16}{3}$ **(correct)**
- $\frac{32}{3}$
- $8$
- $- \frac{32}{3}$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(4 y \sqrt{x}-4 \sqrt{y} x) \\  & =\frac{∂}{∂y}(4 y \sqrt{x})-\frac{∂}{∂y}(4 \sqrt{y} x) \\  & =4 \sqrt{x}\cdot \frac{∂}{∂y}(y)-4 x\cdot \frac{∂}{∂y}(\sqrt{y}) \\  & =4 \sqrt{x}\cdot (1)-4 x\cdot (\frac{1}{2 \sqrt{y}}) \\  & =4 \sqrt{x}-\frac{2 x}{\sqrt{y}}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(4,9):$

$$
\begin{aligned}\frac{∂f}{∂y}{|}_{(4,9)} & =4 \sqrt{(4)}-\frac{2 (4)}{\sqrt{(9)}} \\  & =8-(\frac{8}{3}) \\  & =\frac{16}{3}\end{aligned}
$$

### Generated variant (moderate)

Difficulty: moderate · Template: `cross-roots` · Profile: `method-sum-bank`

For the function $f(x,y)=2 y \sqrt{x}-\sqrt{y} x,$ evaluate $\frac{∂f}{∂y}$ at the point $(4,4).$

- $-5$
- $-1$
- $3$ **(correct)**
- $5$
- $4$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(2 y \sqrt{x}-\sqrt{y} x) \\  & =\frac{∂}{∂y}(2 y \sqrt{x})-\frac{∂}{∂y}(\sqrt{y} x) \\  & =2 \sqrt{x}\cdot \frac{∂}{∂y}(y)-x\cdot \frac{∂}{∂y}(\sqrt{y}) \\  & =2 \sqrt{x}\cdot (1)-x\cdot (\frac{1}{2 \sqrt{y}}) \\  & =2 \sqrt{x}-\frac{x}{2 \sqrt{y}}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(4,4):$

$$
\begin{aligned}\frac{∂f}{∂y}{|}_{(4,4)} & =2 \sqrt{(4)}-\frac{(4)}{2 \sqrt{(4)}} \\  & =4-(1) \\  & =3\end{aligned}
$$

## Original q-159601

For the function $f(x,y)=\operatorname{cos}⁡x\operatorname{ln}⁡y-x\operatorname{sin}⁡y,$ evaluate $\frac{∂f}{∂y}$ at the point $(\pi ,\frac{\pi }{2}).$

Bank: $-4\pi $, $\frac{\pi }{2}$, $-\frac{2}{\pi }$, $2\pi $, $\frac{2}{\pi }-\pi $

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(\operatorname{cos}⁡x\operatorname{ln}⁡y-x\operatorname{sin}⁡y) \\  & =\frac{∂}{∂y}(\operatorname{cos}⁡x\operatorname{ln}⁡y)-\frac{∂}{∂y}(x\operatorname{sin}⁡y) \\  & =\operatorname{cos}⁡x\cdot \frac{∂}{∂y}(\operatorname{ln}⁡y)-x\cdot \frac{∂}{∂y}(\operatorname{sin}⁡y) \\  & =\operatorname{cos}⁡x\cdot (\frac{1}{y})-x\cdot (\operatorname{cos}⁡y) \\  & =\frac{\operatorname{cos}⁡x}{y}-x\operatorname{cos}⁡y\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(\pi ,\frac{\pi }{2}):$

$$
\begin{aligned}\frac{∂f}{∂y}{|}_{(\pi ,\pi /2)} & =\frac{\operatorname{cos}⁡\pi }{(\frac{\pi }{2})}-\pi \cdot \operatorname{cos}⁡(\frac{\pi }{2}) \\  & =-\frac{2}{\pi }-0 \\  & =-\frac{2}{\pi }\end{aligned}
$$

### Generated variant (moderate)

Difficulty: moderate · Template: `cos-log-sin` · Profile: `method-sum-bank`

For the function $f(x,y)=4 \ln{(x )} \cos{(y )}-3 y \sin{(x )},$ evaluate $\frac{∂f}{∂x}$ at the point $(\frac{\pi}{3},2 \pi).$

- $\frac{12}{\pi} + 3 \pi$
- $- 3 \pi + \frac{12}{\pi}$ **(correct)**
- $\frac{12}{\pi}$
- $- 3 \pi - \frac{12}{\pi}$
- $- 3 \pi$

We differentiate the given function with respect to $x,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂}{∂x}(4 \ln{(x )} \cos{(y )}-3 y \sin{(x )}) \\  & =\frac{∂}{∂x}(4 \ln{(x )} \cos{(y )})-\frac{∂}{∂x}(3 y \sin{(x )}) \\  & =4 \cos{(y )}\cdot \frac{∂}{∂x}(\ln{(x )})-3 y\cdot \frac{∂}{∂x}(\sin{(x )}) \\  & =4 \cos{(y )}\cdot (\frac{1}{x})-3 y\cdot (\cos{(x )}) \\  & =\frac{4 \cos{(y )}}{x}-3 y \cos{(x )}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(\frac{\pi}{3},2 \pi):$

$$
\begin{aligned}\frac{∂f}{∂x}{|}_{(\frac{\pi}{3},2 \pi)} & =\frac{4 \cos{((2 \pi) )}}{(\frac{\pi}{3})}-3 (2 \pi) \cos{((\frac{\pi}{3}) )} \\  & =\frac{12}{\pi}-(3 \pi) \\  & =- 3 \pi + \frac{12}{\pi}\end{aligned}
$$

### Generated variant (moderate)

Difficulty: moderate · Template: `cos-log-sin` · Profile: `method-sum-bank`

For the function $f(x,y)=4 \ln{(y )} \cos{(x )}-2 x \sin{(y )},$ evaluate $\frac{∂f}{∂y}$ at the point $(- 2 \pi,\frac{\pi}{6}).$

- $\frac{24}{\pi}$
- $- 2 \sqrt{3} \pi + \frac{24}{\pi}$
- $- \frac{24}{\pi} + 2 \sqrt{3} \pi$
- $\frac{24}{\pi} + 2 \sqrt{3} \pi$ **(correct)**
- $2 \sqrt{3} \pi$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(4 \ln{(y )} \cos{(x )}-2 x \sin{(y )}) \\  & =\frac{∂}{∂y}(4 \ln{(y )} \cos{(x )})-\frac{∂}{∂y}(2 x \sin{(y )}) \\  & =4 \cos{(x )}\cdot \frac{∂}{∂y}(\ln{(y )})-2 x\cdot \frac{∂}{∂y}(\sin{(y )}) \\  & =4 \cos{(x )}\cdot (\frac{1}{y})-2 x\cdot (\cos{(y )}) \\  & =\frac{4 \cos{(x )}}{y}-2 x \cos{(y )}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(- 2 \pi,\frac{\pi}{6}):$

$$
\begin{aligned}\frac{∂f}{∂y}{|}_{(- 2 \pi,\frac{\pi}{6})} & =\frac{4 \cos{((- 2 \pi) )}}{(\frac{\pi}{6})}-2 (- 2 \pi) \cos{((\frac{\pi}{6}) )} \\  & =\frac{24}{\pi}+(2 \sqrt{3} \pi) \\  & =\frac{24}{\pi} + 2 \sqrt{3} \pi\end{aligned}
$$

## Original q-159606

For the function $f(x,y)={y}^{3}\operatorname{cot}⁡x-{x}^{2}{y}^{2},$ evaluate ${f}_{x}(\frac{\pi }{2},1).$

Bank: $-\pi $, $2+\pi $, $3\pi $, $-1-\pi $, $1-2\pi $

We differentiate the given function with respect to $x,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}({y}^{3}\operatorname{cot}⁡x-{x}^{2}{y}^{2}) \\  & =\frac{∂}{∂x}({y}^{3}\operatorname{cot}⁡x)-\frac{∂}{∂x}({x}^{2}{y}^{2}) \\  & ={y}^{3}\cdot \frac{∂}{∂x}(\operatorname{cot}⁡x)-{y}^{2}\cdot \frac{∂}{∂x}({x}^{2}) \\  & ={y}^{3}\cdot (-{csc}^{2}⁡x)-{y}^{2}\cdot (2x) \\  & =-{y}^{3}{csc}^{2}⁡x-2x{y}^{2}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(\frac{\pi }{2},1):$

$$
\begin{aligned}{f}_{x}(\frac{\pi }{2},1) & =-(1)^{3}\cdot {csc}^{2}⁡(\frac{\pi }{2})-2\cdot \frac{\pi }{2}\cdot {1}^{2} \\  & =-1\cdot 1-\pi  \\  & =-1-\pi \end{aligned}
$$

### Generated variant (hard)

Difficulty: hard · Template: `cot-polynomial` · Profile: `method-sum-bank`

For the function $f(x,y)=4 x^{2} \cot{(y )}-4 y^{2} x^{3},$ evaluate ${f}_{y}(-1,- \frac{\pi}{2}).$

- $- 4 \pi$
- $- 4 \pi - 4$ **(correct)**
- $-4 + 4 \pi$
- $-4$
- $4 - 4 \pi$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{y}(x,y) & =\frac{∂}{∂y}(4 x^{2} \cot{(y )}-4 y^{2} x^{3}) \\  & =\frac{∂}{∂y}(4 x^{2} \cot{(y )})-\frac{∂}{∂y}(4 y^{2} x^{3}) \\  & =4 x^{2}\cdot \frac{∂}{∂y}(\cot{(y )})-4 x^{3}\cdot \frac{∂}{∂y}(y^{2}) \\  & =4 x^{2}\cdot (- \csc^{2}{(y )})-4 x^{3}\cdot (2 y) \\  & =- 4 x^{2} \csc^{2}{(y )}-8 y x^{3}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(-1,- \frac{\pi}{2}):$

$$
\begin{aligned}{f}_{y}(-1,- \frac{\pi}{2}) & =- 4 (-1)^{2} \csc^{2}{((- \frac{\pi}{2}) )}-8 (- \frac{\pi}{2}) (-1)^{3} \\  & =(-4)\cdot (1)-(4 \pi) \\  & =- 4 \pi - 4\end{aligned}
$$

### Generated variant (hard)

Difficulty: hard · Template: `cot-polynomial` · Profile: `method-sum-bank`

For the function $f(x,y)=2 x^{3} \cot{(y )}-y^{2} x^{2},$ evaluate ${f}_{y}(-1,\frac{3 \pi}{2}).$

- $- 3 \pi - 2$
- $- 3 \pi$
- $2 - 3 \pi$ **(correct)**
- $2 + 3 \pi$
- $2$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{y}(x,y) & =\frac{∂}{∂y}(2 x^{3} \cot{(y )}-y^{2} x^{2}) \\  & =\frac{∂}{∂y}(2 x^{3} \cot{(y )})-\frac{∂}{∂y}(y^{2} x^{2}) \\  & =2 x^{3}\cdot \frac{∂}{∂y}(\cot{(y )})-x^{2}\cdot \frac{∂}{∂y}(y^{2}) \\  & =2 x^{3}\cdot (- \csc^{2}{(y )})-x^{2}\cdot (2 y) \\  & =- 2 x^{3} \csc^{2}{(y )}-2 y x^{2}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(-1,\frac{3 \pi}{2}):$

$$
\begin{aligned}{f}_{y}(-1,\frac{3 \pi}{2}) & =- 2 (-1)^{3} \csc^{2}{((\frac{3 \pi}{2}) )}-2 (\frac{3 \pi}{2}) (-1)^{2} \\  & =(2)\cdot (1)-(3 \pi) \\  & =2 - 3 \pi\end{aligned}
$$

## Original q-159609

For the function $f(x,y)=y\operatorname{ln}⁡x-2{x}^{5}{e}^{y},$ evaluate ${f}_{x}(1,\operatorname{ln}⁡3).$

Bank: $30\operatorname{ln}⁡3$, $\operatorname{ln}⁡3-5$, $3\operatorname{ln}⁡3$, $\operatorname{ln}⁡3-30$, $\operatorname{ln}⁡3-10$

We differentiate the given function with respect to $x,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(y\operatorname{ln}⁡x-2{x}^{5}{e}^{y}) \\  & =\frac{∂}{∂x}(y\operatorname{ln}⁡x)-\frac{∂}{∂x}(2{x}^{5}{e}^{y}) \\  & =y\cdot \frac{∂}{∂x}(\operatorname{ln}⁡x)-2{e}^{y}\cdot \frac{∂}{∂x}({x}^{5}) \\  & =y\cdot (\frac{1}{x})-2{e}^{y}\cdot (5{x}^{4}) \\  & =\frac{y}{x}-10{x}^{4}{e}^{y}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(1,\operatorname{ln}⁡3):$

$$
\begin{aligned}{f}_{x}(1,\operatorname{ln}⁡3) & =\frac{\operatorname{ln}⁡3}{1}-10\cdot {1}^{4}\cdot {e}^{\operatorname{ln}⁡3} \\  & =\operatorname{ln}⁡3-10\cdot 3 \\  & =\operatorname{ln}⁡3-30\end{aligned}
$$

### Generated variant (hard)

Difficulty: hard · Template: `log-power-exp` · Profile: `method-sum-bank`

For the function $f(x,y)=4 x \ln{(y )}-4 y^{3} \cdot e^{x},$ evaluate ${f}_{y}(\ln{(5 )},2).$

- $2 \ln{(5 )} + 240$
- $-240 + 2 \ln{(5 )}$ **(correct)**
- $-240$
- $-240 - 2 \ln{(5 )}$
- $2 \ln{(5 )}$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{y}(x,y) & =\frac{∂}{∂y}(4 x \ln{(y )}-4 y^{3} \cdot e^{x}) \\  & =\frac{∂}{∂y}(4 x \ln{(y )})-\frac{∂}{∂y}(4 y^{3} \cdot e^{x}) \\  & =4 x\cdot \frac{∂}{∂y}(\ln{(y )})-4 \cdot e^{x}\cdot \frac{∂}{∂y}(y^{3}) \\  & =4 x\cdot (\frac{1}{y})-4 \cdot e^{x}\cdot (3 y^{2}) \\  & =\frac{4 x}{y}-12 y^{2} \cdot e^{x}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(\ln{(5 )},2):$

$$
\begin{aligned}{f}_{y}(\ln{(5 )},2) & =\frac{4 (\ln{(5 )})}{(2)}-12 (2)^{2} \cdot e^{(\ln{(5 )})} \\  & =2 \ln{(5 )}-48\cdot 5 \\  & =-240 + 2 \ln{(5 )}\end{aligned}
$$

### Generated variant (hard)

Difficulty: hard · Template: `log-power-exp` · Profile: `method-sum-bank`

For the function $f(x,y)=2 x \ln{(y )}-y^{4} \cdot e^{x},$ evaluate ${f}_{y}(\ln{(5 )},2).$

- $-160 - \ln{(5 )}$
- $-160$
- $-160 + \ln{(5 )}$ **(correct)**
- $\ln{(5 )} + 160$
- $\ln{(5 )}$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{y}(x,y) & =\frac{∂}{∂y}(2 x \ln{(y )}-y^{4} \cdot e^{x}) \\  & =\frac{∂}{∂y}(2 x \ln{(y )})-\frac{∂}{∂y}(y^{4} \cdot e^{x}) \\  & =2 x\cdot \frac{∂}{∂y}(\ln{(y )})-e^{x}\cdot \frac{∂}{∂y}(y^{4}) \\  & =2 x\cdot (\frac{1}{y})-e^{x}\cdot (4 y^{3}) \\  & =\frac{2 x}{y}-4 y^{3} \cdot e^{x}\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(\ln{(5 )},2):$

$$
\begin{aligned}{f}_{y}(\ln{(5 )},2) & =\frac{2 (\ln{(5 )})}{(2)}-4 (2)^{3} \cdot e^{(\ln{(5 )})} \\  & =\ln{(5 )}-32\cdot 5 \\  & =-160 + \ln{(5 )}\end{aligned}
$$

## Authored easy generated variant

Difficulty: easy · Template: `easy-polynomial` · Profile: `method-sum-bank`

For the function $f(x,y)=4 y^{2} x^{2}+4 y x,$ evaluate $\frac{∂f}{∂y}$ at the point $(4,4).$

- $496$
- $528$ **(correct)**
- $16$
- $-496$
- $512$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(4 y^{2} x^{2}+4 y x) \\  & =\frac{∂}{∂y}(4 y^{2} x^{2})+\frac{∂}{∂y}(4 y x) \\  & =4 x^{2}\cdot \frac{∂}{∂y}(y^{2})+4 x\cdot \frac{∂}{∂y}(y) \\  & =4 x^{2}\cdot (2 y)+4 x\cdot (1) \\  & =8 y x^{2}+4 x\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(4,4):$

$$
\begin{aligned}\frac{∂f}{∂y}{|}_{(4,4)} & =8 (4) (4)^{2}+4 (4) \\  & =512+(16) \\  & =528\end{aligned}
$$

## Authored easy generated variant

Difficulty: easy · Template: `easy-polynomial` · Profile: `method-sum-bank`

For the function $f(x,y)=2 y^{2} x^{2}+y x,$ evaluate $\frac{∂f}{∂y}$ at the point $(4,4).$

- $-252$
- $4$
- $260$ **(correct)**
- $252$
- $256$

We differentiate the given function with respect to $y,$ treating all other variables as constants:

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(2 y^{2} x^{2}+y x) \\  & =\frac{∂}{∂y}(2 y^{2} x^{2})+\frac{∂}{∂y}(y x) \\  & =2 x^{2}\cdot \frac{∂}{∂y}(y^{2})+x\cdot \frac{∂}{∂y}(y) \\  & =2 x^{2}\cdot (2 y)+x\cdot (1) \\  & =4 y x^{2}+x\end{aligned}
$$

Finally, we evaluate the partial derivative at the point $(4,4):$

$$
\begin{aligned}\frac{∂f}{∂y}{|}_{(4,4)} & =4 (4) (4)^{2}+(4) \\  & =256+(4) \\  & =260\end{aligned}
$$
