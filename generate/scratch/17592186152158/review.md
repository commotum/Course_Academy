# Scalar graph line integral review

Original evidence is immutable basis 1356; replay choices may normalize notation. Every generated solution is fixed independently of selected option.

## Original q-76483

Evaluate the integral of the function $f(x,y)=2{y}^{2}$ along the curve $y={e}^{x},$ $\,0\le x\le \operatorname{ln}⁡3.$

- $\frac{2}{3}(5\sqrt{10}-\sqrt{2})$
- $2(5\sqrt{10}-\sqrt{2})$
- $-2\sqrt{2}$
- $5\sqrt{10}$
- $\frac{4}{3}(5\sqrt{10}-\sqrt{2})$ **Captured correct**

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)={e}^{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,{e}^{t}⟩,\,0\le t\le \operatorname{ln}⁡3
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(u) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({e}^{t})j \\  & =i+{e}^{t}j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{({e}^{t})}^{2}} \\  & =\sqrt{1+{e}^{2t}}\end{aligned}
$$

Now, since $f(x,y)=2{y}^{2}$, we obtain

$$
\begin{aligned}f(r(t)) & =2({e}^{t})^{2}=2{e}^{2t}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{\operatorname{ln}⁡3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\operatorname{ln}⁡3}2{e}^{2t}\cdot \sqrt{1+{e}^{2t}}\cdot \text{d}t \\  & ={\int }_{0}^{\operatorname{ln}⁡3}2{e}^{2t}\,\sqrt{1+{e}^{2t}}\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=1+{e}^{2t}$, $\text{d}u=2{e}^{2t}\,\text{d}t$ as follows:  

$$
\begin{aligned}{\int }_{0}^{\operatorname{ln}⁡3}2{e}^{2t}\,\sqrt{1+{e}^{2t}}\,\text{d}t & ={\int }_{2}^{10}{u}^{1/2}\,\text{d}u \\  & =\frac{2}{3}{u}^{3/2}{|}_{2}^{10} \\  & =\frac{2}{3}({10}^{3/2}-{2}^{3/2}) \\  & =\frac{2}{3}(10\sqrt{10}-2\sqrt{2}) \\  & =\frac{4}{3}(5\sqrt{10}-\sqrt{2})\end{aligned}
$$

## Generated observed-profile replay

Evaluate the integral of the function $f(x,y)=2{y}^{2}$ along the curve $y={e}^{x},$ $\,0\le x\le \ln{\left(3 \right)}.$

- $- 2 \sqrt{2}$

- $- 2 \sqrt{2} + 10 \sqrt{10}$

- $- \frac{2 \sqrt{2}}{3} + \frac{10 \sqrt{10}}{3}$

- $- \frac{4 \sqrt{2}}{3} + \frac{20 \sqrt{10}}{3}$ **Correct**

- $5 \sqrt{10}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)={e}^{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,{e}^{t}⟩,\,0\le t\le \ln{\left(3 \right)}
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({e}^{t})j \\  & =i+{e}^{t}j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{({e}^{t})}^{2}} \\  & =\sqrt{1+{e}^{2t}}\end{aligned}
$$

Now, since $f(x,y)=2{y}^{2}$, we obtain

$$
\begin{aligned}f(r(t)) & =2({e}^{t})^{2}=2{e}^{2t}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{\ln{\left(3 \right)}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\ln{\left(3 \right)}}2{e}^{2t}\cdot \sqrt{1+{e}^{2t}}\cdot \text{d}t \\  & ={\int }_{0}^{\ln{\left(3 \right)}}2{e}^{2t}\,\sqrt{1+{e}^{2t}}\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=1+{e}^{2t}$, $\text{d}u=2{e}^{2t}\,\text{d}t$ as follows:  

$$
\begin{aligned}{\int }_{0}^{\ln{\left(3 \right)}}2{e}^{2t}\,\sqrt{1+{e}^{2t}}\,\text{d}t & ={\int }_{2}^{10}{u}^{1/2}\,\text{d}u \\  & =\frac{2}{3}{u}^{3/2}{|}_{2}^{10} \\  & =\frac{2}{3}({10}^{3/2}-{2}^{3/2}) \\  & =\frac{2}{3}(10 \sqrt{10}-2\sqrt{2}) \\  & =- \frac{4 \sqrt{2}}{3} + \frac{20 \sqrt{10}}{3}\end{aligned}
$$

## Original q-76508

Evaluate the integral of the function $f(x, y) = x(y - 1)$ along the line $y = 2x + 1$, $0 \le x \le 1$.

- $\frac{2\sqrt{5}}{3}$
- $\frac{2}{3}$
- $2\sqrt{5}$
- $\frac{\sqrt{5}}{3}$
- $\frac{5\sqrt{2}}{3}$

No source solution, difficulty or correct ref.

## Generated observed-profile replay

Evaluate the integral of the function $f(x,y)=x \left(y - 1\right)$ along the line $y=2 x + 1,$ $\,0\le x\le 1.$

- $2 \sqrt{5}$

- $\frac{2}{3}$

- $\frac{2 \sqrt{5}}{3}$ **Correct**

- $\frac{5 \sqrt{2}}{3}$

- $\frac{\sqrt{5}}{3}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2 t + 1.$ This gives the following parametrization of the curve:

$$
\mathbf r(t)=\langle t,2 t + 1\rangle,\qquad 0\le t\le 1
$$

Computing $\mathbf r^{\prime}(t)$ and $\|\mathbf r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}\mathbf r^{\prime}(t)&=\frac{\mathrm dx}{\mathrm dt}\mathbf i+\frac{\mathrm dy}{\mathrm dt}\mathbf j \\ &=\frac{\mathrm d}{\mathrm dt}(t)\mathbf i+\frac{\mathrm d}{\mathrm dt}(2 t + 1)\mathbf j \\ &=\mathbf i+(2)\mathbf j \\ \|\mathbf r^{\prime}(t)\|&=\sqrt{(\frac{\mathrm dx}{\mathrm dt})^2+(\frac{\mathrm dy}{\mathrm dt})^2} \\ &=\sqrt{1^2+(2)^2} \\ &=\sqrt{5}\end{aligned}
$$

Now, since $f(x,y)=x \left(y - 1\right)$, we obtain

$$
\begin{aligned}f(r(t))&=2 t^{2}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm ds&=\int_{0}^{1}f(r(t))\|\mathbf r^{\prime}(t)\|\,\mathrm dt \\ &=\int_{0}^{1}(2 t^{2})(\sqrt{5})\,\mathrm dt \\ &=\left[\frac{2 \sqrt{5} t^{3}}{3}\right]_{0}^{1} \\ &=\frac{2 \sqrt{5}}{3}\left((1)^{3}-(0)^{3}\right) \\ &=\frac{2 \sqrt{5}}{3}\left(1-0\right) \\ &=\frac{2 \sqrt{5}}{3}.\end{aligned}
$$

## Original q-148215

Evaluate the integral of the function $f(x,y)=2xy$ along the curve $y=\sqrt{4-{x}^{2}},$ $\,0\le x\le 2.$

- $\frac{3}{8}$
- $4\sqrt{2}$
- $\sqrt{2}$
- $\frac{1}{4}$
- $8$ **Captured correct**

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\sqrt{4-{t}^{2}}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,\sqrt{4-{t}^{2}}⟩,\,0\le t\le 2
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(u) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\sqrt{4-{t}^{2}})j \\  & =i-\frac{t}{\sqrt{4-{t}^{2}}}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(-\frac{t}{\sqrt{4-{t}^{2}}})}^{2}} \\  & =\sqrt{1+\frac{{t}^{2}}{4-{t}^{2}}} \\  & =\frac{2}{\sqrt{4-{t}^{2}}}\end{aligned}
$$

Now, since $f(x,y)=2xy$, we obtain

$$
\begin{aligned}f(r(t)) & =2t\sqrt{4-{t}^{2}}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{2}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{2}2t\sqrt{4-{t}^{2}}\cdot \frac{2}{\sqrt{4-{t}^{2}}}\cdot \text{d}t \\  & =4{\int }_{0}^{2}t\,\text{d}t \\  & =2{t}^{2}\,{|}_{0}^{2} \\  & =2({2}^{2}-{0}^{2}) \\  & =8.\end{aligned}
$$

## Generated observed-profile replay

Evaluate the integral of the function $f(x,y)=2xy$ along the curve $y=\sqrt{4-{x}^{2}},$ $\,0\le x\le 2.$

- $\sqrt{2}$

- $4 \sqrt{2}$

- $\frac{3}{8}$

- $8$ **Correct**

- $\frac{1}{4}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\sqrt{4-{t}^{2}}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,\sqrt{4-{t}^{2}}⟩,\,0\le t\le 2
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\sqrt{4-{t}^{2}})j \\  & =i-\frac{t}{\sqrt{4-{t}^{2}}}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(-\frac{t}{\sqrt{4-{t}^{2}}})}^{2}} \\  & =\sqrt{1+\frac{{t}^{2}}{4-{t}^{2}}} \\  & =\frac{2}{\sqrt{4-{t}^{2}}}\end{aligned}
$$

Now, since $f(x,y)=2xy$, we obtain

$$
\begin{aligned}f(r(t)) & =2t\sqrt{4-{t}^{2}}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{2}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{2}2t\sqrt{4-{t}^{2}}\cdot \frac{2}{\sqrt{4-{t}^{2}}}\cdot \text{d}t \\  & =4{\int }_{0}^{2}t\,\text{d}t \\  & =2{t}^{2}\,{|}_{0}^{2} \\  & =2(2^{2}-0^{2}) \\  & = 8.\end{aligned}
$$

## Original q-148216

Evaluate the integral of the function $f(x,y)=x+y$ along the line $y=x,$ $\,0\le x\le 3.$

- $9\sqrt{2}$ **Captured correct**
- $\frac{\sqrt{2}}{3}$
- $3\sqrt{2}$
- $9$
- $\frac{\sqrt{2}}{9}$

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=t.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,t⟩,\,0\le t\le 3
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(u) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(t)j \\  & =i+\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{1}^{2}} \\  & =\sqrt{2}\end{aligned}
$$

Now, since $f(x,y)=x+y$, we obtain

$$
\begin{aligned}f(r(t)) & =t+t=2t.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{3}2t\cdot \sqrt{2}\cdot \text{d}t \\  & =2\sqrt{2}{\int }_{0}^{3}t\,\text{d}t \\  & =\sqrt{2}\,{t}^{2}{|}_{0}^{3} \\  & =\sqrt{2}({3}^{2}-{0}^{2}) \\  & =9\sqrt{2}.\end{aligned}
$$

## Generated observed-profile replay

Evaluate the integral of the function $f(x,y)=x+y$ along the line $y=x,$ $\,0\le x\le 3.$

- $3 \sqrt{2}$

- $\frac{\sqrt{2}}{3}$

- $9 \sqrt{2}$ **Correct**

- $\frac{\sqrt{2}}{9}$

- $9$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=t.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,t⟩,\,0\le t\le 3
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(t)j \\  & =i+\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{1}^{2}} \\  & =\sqrt{2}\end{aligned}
$$

Now, since $f(x,y)=x+y$, we obtain

$$
\begin{aligned}f(r(t)) & =t+t=2t.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{3}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{3}2t\cdot \sqrt{2}\cdot \text{d}t \\  & =2\sqrt{2}{\int }_{0}^{3}t\,\text{d}t \\  & =\sqrt{2}\,{t}^{2}{|}_{0}^{3} \\  & =\sqrt{2}(3^{2}-0^{2}) \\  & =9 \sqrt{2}.\end{aligned}
$$

## Original q-148218

Evaluate the integral of the function $f(x,y)=({x}^{2}+y)$ along the line $y=3x+2,$ $\,0\le x\le 1.$

- $\frac{\sqrt{5}}{6}$
- $3\sqrt{5}$
- $13\sqrt{10}$
- $\frac{\sqrt{10}}{3}$
- $\frac{23\sqrt{10}}{6}$ **Captured correct**

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=3t+2.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,3t+2⟩,\,0\le t\le 1
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(u) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(3t+2)j \\  & =i+3\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{3}^{2}} \\  & =\sqrt{10}\end{aligned}
$$

Now, since $f(x,y)={x}^{2}+y$, we obtain

$$
\begin{aligned}f(r(t)) & ={t}^{2}+(3t+2)={t}^{2}+3t+2.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}({t}^{2}+3t+2)\cdot \sqrt{10}\cdot \text{d}t \\  & =\sqrt{10}{\int }_{0}^{1}({t}^{2}+3t+2)\,\text{d}t \\  & =\sqrt{10}\,(\frac{{t}^{3}}{3}+\frac{3{t}^{2}}{2}+2t){|}_{0}^{1} \\  & =\sqrt{10}(\frac{1}{3}+\frac{3}{2}+2) \\  & =\frac{23\sqrt{10}}{6}.\end{aligned}
$$

## Generated observed-profile replay

Evaluate the integral of the function $f(x,y)=({x}^{2}+y)$ along the line $y=3x+2,$ $\,0\le x\le 1.$

- $13 \sqrt{10}$

- $3 \sqrt{5}$

- $\frac{\sqrt{5}}{6}$

- $\frac{23 \sqrt{10}}{6}$ **Correct**

- $\frac{\sqrt{10}}{3}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=3t+2.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,3t+2⟩,\,0\le t\le 1
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(3t+2)j \\  & =i+3\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{3}^{2}} \\  & =\sqrt{10}\end{aligned}
$$

Now, since $f(x,y)={x}^{2}+y$, we obtain

$$
\begin{aligned}f(r(t)) & ={t}^{2}+(3t+2)={t}^{2}+3t+2.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{1}({t}^{2}+3t+2)\cdot \sqrt{10}\cdot \text{d}t \\  & =\sqrt{10}{\int }_{0}^{1}({t}^{2}+3t+2)\,\text{d}t \\  & =\sqrt{10}\,(\frac{{t}^{3}}{3}+\frac{3{t}^{2}}{2}+2t){|}_{0}^{1} \\  & =\sqrt{10}(\frac{1}{3}+\frac{3}{2}+2) \\  & =\frac{23 \sqrt{10}}{6}.\end{aligned}
$$

## Original q-148219

Evaluate the integral of the function $f(x,y)=\frac{1}{x-y}$ along the line $y=x-4,$ $\,0\le x\le 2.$

- $\frac{1}{2}$
- $\frac{\sqrt{2}}{2}$ **Captured correct**
- $2$
- $\frac{3}{2}$
- $\sqrt{2}$

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=t-4.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,t-4⟩,\,0\le t\le 2
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(u) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(t-4)j \\  & =i+\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{1}^{2}} \\  & =\sqrt{2}\end{aligned}
$$

Now, since $f(x,y)=\frac{1}{x-y}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{1}{t-(t-4))}=\frac{1}{4}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{2}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{2}\frac{1}{4}\cdot \sqrt{2}\cdot \text{d}t \\  & =\frac{\sqrt{2}}{4}{\int }_{0}^{2}\,\text{d}t \\  & =\frac{\sqrt{2}}{4}\,t\,{|}_{0}^{2} \\  & =\frac{\sqrt{2}}{4}(2-0) \\  & =\frac{\sqrt{2}}{2}.\end{aligned}
$$

## Generated observed-profile replay

Evaluate the integral of the function $f(x,y)=\frac{1}{x-y}$ along the line $y=x-4,$ $\,0\le x\le 2.$

- $2$

- $\frac{\sqrt{2}}{2}$ **Correct**

- $\frac{1}{2}$

- $\sqrt{2}$

- $\frac{3}{2}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=t-4.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,t-4⟩,\,0\le t\le 2
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(t-4)j \\  & =i+\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{1}^{2}} \\  & =\sqrt{2}\end{aligned}
$$

Now, since $f(x,y)=\frac{1}{x-y}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{1}{t-(t-4)}=\frac{1}{4}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{2}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{2}\frac{1}{4}\cdot \sqrt{2}\cdot \text{d}t \\  & =\frac{\sqrt{2}}{4}{\int }_{0}^{2}\,\text{d}t \\  & =\frac{\sqrt{2}}{4}\,t\,{|}_{0}^{2} \\  & =\frac{\sqrt{2}}{4}(2-0) \\  & =\frac{\sqrt{2}}{2}.\end{aligned}
$$

## Original q-76431

Evaluate the integral ${\int }_{C}\frac{y}{x}\,\text{d}s,$ where the curve $C$ is given by $y=\frac{{x}^{2}}{4},$ $\,0\le x\le 4\sqrt{6}.$

- $\frac{124}{3}$ **Captured correct**
- $\frac{\sqrt{5}}{3}$
- $\frac{25}{3}$
- $\frac{5\sqrt{5}}{3}$
- $\frac{125}{3}$

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\frac{{t}^{2}}{4}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,\frac{{t}^{2}}{4}⟩,\,0\le t\le 4\sqrt{6}
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(u) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\frac{{t}^{2}}{4})j \\  & =i+\frac{t}{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(\frac{t}{2})}^{2}} \\  & =\sqrt{1+\frac{{t}^{2}}{4}}\end{aligned}
$$

Now, since $f(x,y)=\frac{y}{x}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{(\frac{{t}^{2}}{4})}{t}=\frac{t}{4}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}\frac{y}{x}\,\text{d}s & ={\int }_{0}^{4\sqrt{6}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{4\sqrt{6}}\frac{t}{4}\cdot \sqrt{1+\frac{{t}^{2}}{4}}\cdot \text{d}t \\  & =\frac{1}{4}{\int }_{0}^{4\sqrt{6}}t\sqrt{1+\frac{{t}^{2}}{4}}\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=1+\frac{{t}^{2}}{4}$, $\text{d}u=\frac{t}{2}\,\text{d}t$ as follows: 

$$
\begin{aligned}\frac{1}{4}{\int }_{0}^{4\sqrt{6}}t\sqrt{1+\frac{{t}^{2}}{4}}\text{d}t & =\frac{1}{2}{\int }_{1}^{25}{u}^{1/2}\,\text{d}u \\  & =\frac{{u}^{3/2}}{3}{|}_{1}^{25} \\  & =\frac{1}{3}({25}^{3/2}-{1}^{3/2}) \\  & =\frac{1}{3}(125-1) \\  & =\frac{124}{3}\end{aligned}
$$

## Generated observed-profile replay

Evaluate the integral ${\int }_{C}\frac{y}{x}\,\text{d}s,$ where the curve $C$ is given by $y=\frac{{x}^{2}}{4},$ $\,0\le x\le 4 \sqrt{6}.$

- $\frac{25}{3}$

- $\frac{\sqrt{5}}{3}$

- $\frac{124}{3}$ **Correct**

- $\frac{125}{3}$

- $\frac{5 \sqrt{5}}{3}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\frac{{t}^{2}}{4}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,\frac{{t}^{2}}{4}⟩,\,0\le t\le 4 \sqrt{6}
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\frac{{t}^{2}}{4})j \\  & =i+\frac{t}{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(\frac{t}{2})}^{2}} \\  & =\sqrt{1+\frac{{t}^{2}}{4}}\end{aligned}
$$

Now, since $f(x,y)=\frac{y}{x}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{(\frac{{t}^{2}}{4})}{t}=\frac{t}{4}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}\frac{y}{x}\,\text{d}s & ={\int }_{0}^{4 \sqrt{6}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{4 \sqrt{6}}\frac{t}{4}\cdot \sqrt{1+\frac{{t}^{2}}{4}}\cdot \text{d}t \\  & =\frac{1}{4}{\int }_{0}^{4 \sqrt{6}}t\sqrt{1+\frac{{t}^{2}}{4}}\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=1+\frac{{t}^{2}}{4}$, $\text{d}u=\frac{t}{2}\,\text{d}t$ as follows: 

$$
\begin{aligned}\frac{1}{4}{\int }_{0}^{4 \sqrt{6}}t\sqrt{1+\frac{{t}^{2}}{4}}\text{d}t & =\frac{1}{2}{\int }_{1}^{25}{u}^{1/2}\,\text{d}u \\  & =\frac{{u}^{3/2}}{3}{|}_{1}^{25} \\  & =\frac{1}{3}({25}^{3/2}-{1}^{3/2}) \\  & =\frac{1}{3}(125-1) \\  & =\frac{124}{3}\end{aligned}
$$

## Original q-76480

Evaluate the integral ${\int }_{C}\frac{4{y}^{2}}{{x}^{3}}\,\text{d}s,$ where the curve $C$ is given by $y=\frac{1}{x},$ $\,1\le x\le \sqrt[4]{2}.$

- $16\sqrt{2}-6\sqrt{6}$
- $32\sqrt{2}$
- $\frac{1}{6}(8\sqrt{2}-3\sqrt{6})$ **Captured correct**
- $2(16\sqrt{2}-6\sqrt{6})$
- $12\sqrt{6}$

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\frac{1}{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,\frac{1}{t}⟩,\,1\le t\le \sqrt[4]{2}
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(u) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\frac{1}{t})j \\  & =i-\frac{1}{{t}^{2}}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(-\frac{1}{{t}^{2}})}^{2}} \\  & =\sqrt{1+\frac{1}{{t}^{4}}}\end{aligned}
$$

Now, since $f(x,y)=\frac{4{y}^{2}}{{x}^{3}}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{4{(\frac{1}{t})}^{2}}{{t}^{3}}=\frac{4}{{t}^{5}}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}3{x}^{5}{y}^{2}\,\text{d}s & ={\int }_{1}^{\sqrt[4]{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{\sqrt[4]{2}}\frac{4}{{t}^{5}}\cdot \sqrt{1+\frac{1}{{t}^{4}}}\cdot \text{d}t \\  & =4{\int }_{1}^{\sqrt[4]{2}}\frac{1}{{t}^{5}}\,\sqrt{1+\frac{1}{{t}^{4}}}\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=1+\frac{1}{{t}^{4}}$, $\text{d}u=-\frac{4}{{t}^{5}}\,\text{d}t$ as follows: 

$$
\begin{aligned}4{\int }_{1}^{\sqrt[4]{2}}\frac{1}{{t}^{5}}\,\sqrt{1+\frac{1}{{t}^{4}}}\,\text{d}t & =-{\int }_{2}^{3/2}{u}^{1/2}\,\text{d}u \\  & =-\frac{2}{3}{u}^{3/2}{|}_{2}^{3/2} \\  & =-\frac{2}{3}(\sqrt{{(\frac{3}{2})}^{3}}-\sqrt{{2}^{3}}) \\  & =-\frac{2}{3}(\frac{3\sqrt{6}}{4}-2\sqrt{2}) \\  & =\frac{1}{6}(8\sqrt{2}-3\sqrt{6})\end{aligned}
$$

## Generated observed-profile replay

Evaluate the integral ${\int }_{C}\frac{4{y}^{2}}{{x}^{3}}\,\text{d}s,$ where the curve $C$ is given by $y=\frac{1}{x},$ $\,1\le x\le \sqrt[4]{2}.$

- $- \frac{\sqrt{6}}{2} + \frac{4 \sqrt{2}}{3}$ **Correct**

- $32 \sqrt{2}$

- $- 6 \sqrt{6} + 16 \sqrt{2}$

- $12 \sqrt{6}$

- $- 12 \sqrt{6} + 32 \sqrt{2}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\frac{1}{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,\frac{1}{t}⟩,\,1\le t\le \sqrt[4]{2}
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\frac{1}{t})j \\  & =i-\frac{1}{{t}^{2}}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(-\frac{1}{{t}^{2}})}^{2}} \\  & =\sqrt{1+\frac{1}{{t}^{4}}}\end{aligned}
$$

Now, since $f(x,y)=\frac{4{y}^{2}}{{x}^{3}}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{4{(\frac{1}{t})}^{2}}{{t}^{3}}=\frac{4}{{t}^{5}}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}\frac{4{y}^{2}}{{x}^{3}}\,\text{d}s & ={\int }_{1}^{\sqrt[4]{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{\sqrt[4]{2}}\frac{4}{{t}^{5}}\cdot \sqrt{1+\frac{1}{{t}^{4}}}\cdot \text{d}t \\  & =4{\int }_{1}^{\sqrt[4]{2}}\frac{1}{{t}^{5}}\,\sqrt{1+\frac{1}{{t}^{4}}}\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=1+\frac{1}{{t}^{4}}$, $\text{d}u=-\frac{4}{{t}^{5}}\,\text{d}t$ as follows: 

$$
\begin{aligned}4{\int }_{1}^{\sqrt[4]{2}}\frac{1}{{t}^{5}}\,\sqrt{1+\frac{1}{{t}^{4}}}\,\text{d}t & =-{\int }_{2}^{\frac{3}{2}}{u}^{1/2}\,\text{d}u \\  & =-\frac{2}{3}{u}^{3/2}{|}_{2}^{\frac{3}{2}} \\  & =-\frac{2}{3}(\sqrt{(\frac{3}{2})^{3}}-\sqrt{{2}^{3}}) \\  & =-\frac{2}{3}(\frac{3 \sqrt{6}}{4}-2\sqrt{2}) \\  & =- \frac{\sqrt{6}}{2} + \frac{4 \sqrt{2}}{3}\end{aligned}
$$

## Generated variant — easy_linear / authored_operations

Evaluate the integral of the function $f(x,y)=5 x$ along the line $y=3 x,$ $\,0\le x\le 5.$

- $\frac{125 \sqrt{10}}{2}$ **Correct**

- $- \frac{125 \sqrt{10}}{2}$

- $\frac{125}{2}$

- $625$

- $25 \sqrt{10}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=3 t.$ This gives the following parametrization of the curve:

$$
\mathbf r(t)=\langle t,3 t\rangle,\qquad 0\le t\le 5
$$

Computing $\mathbf r^{\prime}(t)$ and $\|\mathbf r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}\mathbf r^{\prime}(t)&=\frac{\mathrm dx}{\mathrm dt}\mathbf i+\frac{\mathrm dy}{\mathrm dt}\mathbf j \\ &=\frac{\mathrm d}{\mathrm dt}(t)\mathbf i+\frac{\mathrm d}{\mathrm dt}(3 t)\mathbf j \\ &=\mathbf i+(3)\mathbf j \\ \|\mathbf r^{\prime}(t)\|&=\sqrt{(\frac{\mathrm dx}{\mathrm dt})^2+(\frac{\mathrm dy}{\mathrm dt})^2} \\ &=\sqrt{1^2+(3)^2} \\ &=\sqrt{10}\end{aligned}
$$

Now, since $f(x,y)=5 x$, we obtain

$$
\begin{aligned}f(r(t))&=5 t\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm ds&=\int_{0}^{5}f(r(t))\|\mathbf r^{\prime}(t)\|\,\mathrm dt \\ &=\int_{0}^{5}(5 t)(\sqrt{10})\,\mathrm dt \\ &=\left[\frac{5 \sqrt{10} t^{2}}{2}\right]_{0}^{5} \\ &=\frac{5 \sqrt{10}}{2}\left((5)^{2}-(0)^{2}\right) \\ &=\frac{5 \sqrt{10}}{2}\left(25-0\right) \\ &=\frac{125 \sqrt{10}}{2}.\end{aligned}
$$

## Generated variant — easy_linear / authored_operations

Evaluate the integral of the function $f(x,y)=5 x$ along the line $y=2 x,$ $\,0\le x\le 8.$

- $40 \sqrt{5}$

- $160$

- $- 160 \sqrt{5}$

- $800$

- $160 \sqrt{5}$ **Correct**

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2 t.$ This gives the following parametrization of the curve:

$$
\mathbf r(t)=\langle t,2 t\rangle,\qquad 0\le t\le 8
$$

Computing $\mathbf r^{\prime}(t)$ and $\|\mathbf r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}\mathbf r^{\prime}(t)&=\frac{\mathrm dx}{\mathrm dt}\mathbf i+\frac{\mathrm dy}{\mathrm dt}\mathbf j \\ &=\frac{\mathrm d}{\mathrm dt}(t)\mathbf i+\frac{\mathrm d}{\mathrm dt}(2 t)\mathbf j \\ &=\mathbf i+(2)\mathbf j \\ \|\mathbf r^{\prime}(t)\|&=\sqrt{(\frac{\mathrm dx}{\mathrm dt})^2+(\frac{\mathrm dy}{\mathrm dt})^2} \\ &=\sqrt{1^2+(2)^2} \\ &=\sqrt{5}\end{aligned}
$$

Now, since $f(x,y)=5 x$, we obtain

$$
\begin{aligned}f(r(t))&=5 t\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm ds&=\int_{0}^{8}f(r(t))\|\mathbf r^{\prime}(t)\|\,\mathrm dt \\ &=\int_{0}^{8}(5 t)(\sqrt{5})\,\mathrm dt \\ &=\left[\frac{5 \sqrt{5} t^{2}}{2}\right]_{0}^{8} \\ &=\frac{5 \sqrt{5}}{2}\left((8)^{2}-(0)^{2}\right) \\ &=\frac{5 \sqrt{5}}{2}\left(64-0\right) \\ &=160 \sqrt{5}.\end{aligned}
$$

## Generated variant — exponential / authored_operations

Evaluate the integral of the function $f(x,y)=2{y}^{2}$ along the curve $y={e}^{x},$ $\,0\le x\le \ln{\left(8 \right)}.$

- $\ln{\left(39402006196394479212279040100143613805079739270465446667948293404245721771497210611414266254884915640806627990306816 \right)}$

- $\frac{4221}{2}$

- $63$

- $- \frac{4 \sqrt{2}}{3} + \frac{130 \sqrt{65}}{3}$ **Correct**

- $- \frac{130 \sqrt{65}}{3} + \frac{4 \sqrt{2}}{3}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)={e}^{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,{e}^{t}⟩,\,0\le t\le \ln{\left(8 \right)}
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({e}^{t})j \\  & =i+{e}^{t}j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{({e}^{t})}^{2}} \\  & =\sqrt{1+{e}^{2t}}\end{aligned}
$$

Now, since $f(x,y)=2{y}^{2}$, we obtain

$$
\begin{aligned}f(r(t)) & =2({e}^{t})^{2}=2{e}^{2t}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{\ln{\left(8 \right)}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\ln{\left(8 \right)}}2{e}^{2t}\cdot \sqrt{1+{e}^{2t}}\cdot \text{d}t \\  & ={\int }_{0}^{\ln{\left(8 \right)}}2{e}^{2t}\,\sqrt{1+{e}^{2t}}\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=1+{e}^{2t}$, $\text{d}u=2{e}^{2t}\,\text{d}t$ as follows:  

$$
\begin{aligned}{\int }_{0}^{\ln{\left(8 \right)}}2{e}^{2t}\,\sqrt{1+{e}^{2t}}\,\text{d}t & ={\int }_{2}^{65}{u}^{1/2}\,\text{d}u \\  & =\frac{2}{3}{u}^{3/2}{|}_{2}^{65} \\  & =\frac{2}{3}({65}^{3/2}-{2}^{3/2}) \\  & =\frac{2}{3}(65 \sqrt{65}-2\sqrt{2}) \\  & =- \frac{4 \sqrt{2}}{3} + \frac{130 \sqrt{65}}{3}\end{aligned}
$$

## Generated variant — exponential / authored_operations

Evaluate the integral of the function $f(x,y)=2{y}^{2}$ along the curve $y={e}^{x},$ $\,0\le x\le \ln{\left(4 \right)}.$

- $\frac{285}{2}$

- $- \frac{34 \sqrt{17}}{3} + \frac{4 \sqrt{2}}{3}$

- $15$

- $- \frac{4 \sqrt{2}}{3} + \frac{34 \sqrt{17}}{3}$ **Correct**

- $\ln{\left(18446744073709551616 \right)}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)={e}^{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,{e}^{t}⟩,\,0\le t\le \ln{\left(4 \right)}
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({e}^{t})j \\  & =i+{e}^{t}j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{({e}^{t})}^{2}} \\  & =\sqrt{1+{e}^{2t}}\end{aligned}
$$

Now, since $f(x,y)=2{y}^{2}$, we obtain

$$
\begin{aligned}f(r(t)) & =2({e}^{t})^{2}=2{e}^{2t}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{\ln{\left(4 \right)}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\ln{\left(4 \right)}}2{e}^{2t}\cdot \sqrt{1+{e}^{2t}}\cdot \text{d}t \\  & ={\int }_{0}^{\ln{\left(4 \right)}}2{e}^{2t}\,\sqrt{1+{e}^{2t}}\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=1+{e}^{2t}$, $\text{d}u=2{e}^{2t}\,\text{d}t$ as follows:  

$$
\begin{aligned}{\int }_{0}^{\ln{\left(4 \right)}}2{e}^{2t}\,\sqrt{1+{e}^{2t}}\,\text{d}t & ={\int }_{2}^{17}{u}^{1/2}\,\text{d}u \\  & =\frac{2}{3}{u}^{3/2}{|}_{2}^{17} \\  & =\frac{2}{3}({17}^{3/2}-{2}^{3/2}) \\  & =\frac{2}{3}(17 \sqrt{17}-2\sqrt{2}) \\  & =- \frac{4 \sqrt{2}}{3} + \frac{34 \sqrt{17}}{3}\end{aligned}
$$

## Generated variant — exponential / observed_expression_pattern_unresolved_intent

Evaluate the integral of the function $f(x,y)=2{y}^{2}$ along the curve $y={e}^{x},$ $\,0\le x\le \ln{\left(10 \right)}.$

- $- \frac{2 \sqrt{2}}{3} + \frac{101 \sqrt{101}}{3}$

- $- \frac{4 \sqrt{2}}{3} + \frac{202 \sqrt{101}}{3}$ **Correct**

- $- 2 \sqrt{2} + 101 \sqrt{101}$

- $- 2 \sqrt{2}$

- $\frac{101 \sqrt{101}}{2}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)={e}^{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,{e}^{t}⟩,\,0\le t\le \ln{\left(10 \right)}
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({e}^{t})j \\  & =i+{e}^{t}j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{({e}^{t})}^{2}} \\  & =\sqrt{1+{e}^{2t}}\end{aligned}
$$

Now, since $f(x,y)=2{y}^{2}$, we obtain

$$
\begin{aligned}f(r(t)) & =2({e}^{t})^{2}=2{e}^{2t}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{\ln{\left(10 \right)}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\ln{\left(10 \right)}}2{e}^{2t}\cdot \sqrt{1+{e}^{2t}}\cdot \text{d}t \\  & ={\int }_{0}^{\ln{\left(10 \right)}}2{e}^{2t}\,\sqrt{1+{e}^{2t}}\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=1+{e}^{2t}$, $\text{d}u=2{e}^{2t}\,\text{d}t$ as follows:  

$$
\begin{aligned}{\int }_{0}^{\ln{\left(10 \right)}}2{e}^{2t}\,\sqrt{1+{e}^{2t}}\,\text{d}t & ={\int }_{2}^{101}{u}^{1/2}\,\text{d}u \\  & =\frac{2}{3}{u}^{3/2}{|}_{2}^{101} \\  & =\frac{2}{3}({101}^{3/2}-{2}^{3/2}) \\  & =\frac{2}{3}(101 \sqrt{101}-2\sqrt{2}) \\  & =- \frac{4 \sqrt{2}}{3} + \frac{202 \sqrt{101}}{3}\end{aligned}
$$

## Generated variant — line_product / authored_operations

Evaluate the integral of the function $f(x,y)=x \left(y - 1\right)$ along the line $y=2 x + 1,$ $\,0\le x\le \frac{13}{2}.$

- $- \frac{2197 \sqrt{5}}{12}$

- $\frac{10985}{12}$

- $\frac{2197}{12}$

- $\frac{2197 \sqrt{5}}{12}$ **Correct**

- $\frac{169 \sqrt{5}}{2}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2 t + 1.$ This gives the following parametrization of the curve:

$$
\mathbf r(t)=\langle t,2 t + 1\rangle,\qquad 0\le t\le \frac{13}{2}
$$

Computing $\mathbf r^{\prime}(t)$ and $\|\mathbf r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}\mathbf r^{\prime}(t)&=\frac{\mathrm dx}{\mathrm dt}\mathbf i+\frac{\mathrm dy}{\mathrm dt}\mathbf j \\ &=\frac{\mathrm d}{\mathrm dt}(t)\mathbf i+\frac{\mathrm d}{\mathrm dt}(2 t + 1)\mathbf j \\ &=\mathbf i+(2)\mathbf j \\ \|\mathbf r^{\prime}(t)\|&=\sqrt{(\frac{\mathrm dx}{\mathrm dt})^2+(\frac{\mathrm dy}{\mathrm dt})^2} \\ &=\sqrt{1^2+(2)^2} \\ &=\sqrt{5}\end{aligned}
$$

Now, since $f(x,y)=x \left(y - 1\right)$, we obtain

$$
\begin{aligned}f(r(t))&=2 t^{2}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm ds&=\int_{0}^{\frac{13}{2}}f(r(t))\|\mathbf r^{\prime}(t)\|\,\mathrm dt \\ &=\int_{0}^{\frac{13}{2}}(2 t^{2})(\sqrt{5})\,\mathrm dt \\ &=\left[\frac{2 \sqrt{5} t^{3}}{3}\right]_{0}^{\frac{13}{2}} \\ &=\frac{2 \sqrt{5}}{3}\left((\frac{13}{2})^{3}-(0)^{3}\right) \\ &=\frac{2 \sqrt{5}}{3}\left(\frac{2197}{8}-0\right) \\ &=\frac{2197 \sqrt{5}}{12}.\end{aligned}
$$

## Generated variant — line_product / authored_operations

Evaluate the integral of the function $f(x,y)=x \left(y - 1\right)$ along the line $y=2 x + 1,$ $\,0\le x\le \frac{5}{2}.$

- $\frac{625}{12}$

- $\frac{25 \sqrt{5}}{2}$

- $\frac{125}{12}$

- $\frac{125 \sqrt{5}}{12}$ **Correct**

- $- \frac{125 \sqrt{5}}{12}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2 t + 1.$ This gives the following parametrization of the curve:

$$
\mathbf r(t)=\langle t,2 t + 1\rangle,\qquad 0\le t\le \frac{5}{2}
$$

Computing $\mathbf r^{\prime}(t)$ and $\|\mathbf r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}\mathbf r^{\prime}(t)&=\frac{\mathrm dx}{\mathrm dt}\mathbf i+\frac{\mathrm dy}{\mathrm dt}\mathbf j \\ &=\frac{\mathrm d}{\mathrm dt}(t)\mathbf i+\frac{\mathrm d}{\mathrm dt}(2 t + 1)\mathbf j \\ &=\mathbf i+(2)\mathbf j \\ \|\mathbf r^{\prime}(t)\|&=\sqrt{(\frac{\mathrm dx}{\mathrm dt})^2+(\frac{\mathrm dy}{\mathrm dt})^2} \\ &=\sqrt{1^2+(2)^2} \\ &=\sqrt{5}\end{aligned}
$$

Now, since $f(x,y)=x \left(y - 1\right)$, we obtain

$$
\begin{aligned}f(r(t))&=2 t^{2}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm ds&=\int_{0}^{\frac{5}{2}}f(r(t))\|\mathbf r^{\prime}(t)\|\,\mathrm dt \\ &=\int_{0}^{\frac{5}{2}}(2 t^{2})(\sqrt{5})\,\mathrm dt \\ &=\left[\frac{2 \sqrt{5} t^{3}}{3}\right]_{0}^{\frac{5}{2}} \\ &=\frac{2 \sqrt{5}}{3}\left((\frac{5}{2})^{3}-(0)^{3}\right) \\ &=\frac{2 \sqrt{5}}{3}\left(\frac{125}{8}-0\right) \\ &=\frac{125 \sqrt{5}}{12}.\end{aligned}
$$

## Generated variant — line_product / observed_expression_pattern_unresolved_intent

Evaluate the integral of the function $f(x,y)=x \left(y - 1\right)$ along the line $y=2 x + 1,$ $\,0\le x\le 7.$

- $\frac{343 \sqrt{5}}{3}$

- $\frac{686 \sqrt{5}}{3}$ **Correct**

- $\frac{686}{3}$

- $\frac{1715 \sqrt{2}}{3}$

- $686 \sqrt{5}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=2 t + 1.$ This gives the following parametrization of the curve:

$$
\mathbf r(t)=\langle t,2 t + 1\rangle,\qquad 0\le t\le 7
$$

Computing $\mathbf r^{\prime}(t)$ and $\|\mathbf r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}\mathbf r^{\prime}(t)&=\frac{\mathrm dx}{\mathrm dt}\mathbf i+\frac{\mathrm dy}{\mathrm dt}\mathbf j \\ &=\frac{\mathrm d}{\mathrm dt}(t)\mathbf i+\frac{\mathrm d}{\mathrm dt}(2 t + 1)\mathbf j \\ &=\mathbf i+(2)\mathbf j \\ \|\mathbf r^{\prime}(t)\|&=\sqrt{(\frac{\mathrm dx}{\mathrm dt})^2+(\frac{\mathrm dy}{\mathrm dt})^2} \\ &=\sqrt{1^2+(2)^2} \\ &=\sqrt{5}\end{aligned}
$$

Now, since $f(x,y)=x \left(y - 1\right)$, we obtain

$$
\begin{aligned}f(r(t))&=2 t^{2}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm ds&=\int_{0}^{7}f(r(t))\|\mathbf r^{\prime}(t)\|\,\mathrm dt \\ &=\int_{0}^{7}(2 t^{2})(\sqrt{5})\,\mathrm dt \\ &=\left[\frac{2 \sqrt{5} t^{3}}{3}\right]_{0}^{7} \\ &=\frac{2 \sqrt{5}}{3}\left((7)^{3}-(0)^{3}\right) \\ &=\frac{2 \sqrt{5}}{3}\left(343-0\right) \\ &=\frac{686 \sqrt{5}}{3}.\end{aligned}
$$

## Generated variant — circle / authored_operations

Evaluate the integral of the function $f(x,y)=2xy$ along the curve $y=\sqrt{4-{x}^{2}},$ $\,0\le x\le \frac{3}{2}.$

- $16 - 4 \sqrt{7}$

- $\frac{16}{3} - \frac{7 \sqrt{7}}{12}$

- $\frac{9}{2}$ **Correct**

- $\frac{9 \sqrt{7}}{4}$

- $- \frac{9}{2}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\sqrt{4-{t}^{2}}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,\sqrt{4-{t}^{2}}⟩,\,0\le t\le \frac{3}{2}
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\sqrt{4-{t}^{2}})j \\  & =i-\frac{t}{\sqrt{4-{t}^{2}}}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(-\frac{t}{\sqrt{4-{t}^{2}}})}^{2}} \\  & =\sqrt{1+\frac{{t}^{2}}{4-{t}^{2}}} \\  & =\frac{2}{\sqrt{4-{t}^{2}}}\end{aligned}
$$

Now, since $f(x,y)=2xy$, we obtain

$$
\begin{aligned}f(r(t)) & =2t\sqrt{4-{t}^{2}}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{\frac{3}{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\frac{3}{2}}2t\sqrt{4-{t}^{2}}\cdot \frac{2}{\sqrt{4-{t}^{2}}}\cdot \text{d}t \\  & =4{\int }_{0}^{\frac{3}{2}}t\,\text{d}t \\  & =2{t}^{2}\,{|}_{0}^{\frac{3}{2}} \\  & =2(\frac{3}{2}^{2}-0^{2}) \\  & = \frac{9}{2}.\end{aligned}
$$

## Generated variant — circle / authored_operations

Evaluate the integral of the function $f(x,y)=2xy$ along the curve $y=\sqrt{4-{x}^{2}},$ $\,0\le x\le \frac{3}{2}.$

- $16 - 4 \sqrt{7}$

- $- \frac{9}{2}$

- $\frac{16}{3} - \frac{7 \sqrt{7}}{12}$

- $\frac{9}{2}$ **Correct**

- $\frac{9 \sqrt{7}}{4}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\sqrt{4-{t}^{2}}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,\sqrt{4-{t}^{2}}⟩,\,0\le t\le \frac{3}{2}
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\sqrt{4-{t}^{2}})j \\  & =i-\frac{t}{\sqrt{4-{t}^{2}}}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(-\frac{t}{\sqrt{4-{t}^{2}}})}^{2}} \\  & =\sqrt{1+\frac{{t}^{2}}{4-{t}^{2}}} \\  & =\frac{2}{\sqrt{4-{t}^{2}}}\end{aligned}
$$

Now, since $f(x,y)=2xy$, we obtain

$$
\begin{aligned}f(r(t)) & =2t\sqrt{4-{t}^{2}}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{\frac{3}{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\frac{3}{2}}2t\sqrt{4-{t}^{2}}\cdot \frac{2}{\sqrt{4-{t}^{2}}}\cdot \text{d}t \\  & =4{\int }_{0}^{\frac{3}{2}}t\,\text{d}t \\  & =2{t}^{2}\,{|}_{0}^{\frac{3}{2}} \\  & =2(\frac{3}{2}^{2}-0^{2}) \\  & = \frac{9}{2}.\end{aligned}
$$

## Generated variant — circle / observed_expression_pattern_unresolved_intent

Evaluate the integral of the function $f(x,y)=2xy$ along the curve $y=\sqrt{4-{x}^{2}},$ $\,0\le x\le \frac{1}{4}.$

- $\frac{3}{512}$

- $\frac{1}{8}$ **Correct**

- $\frac{\sqrt{2}}{16}$

- $\frac{\sqrt{2}}{64}$

- $\frac{1}{256}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\sqrt{4-{t}^{2}}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,\sqrt{4-{t}^{2}}⟩,\,0\le t\le \frac{1}{4}
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\sqrt{4-{t}^{2}})j \\  & =i-\frac{t}{\sqrt{4-{t}^{2}}}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(-\frac{t}{\sqrt{4-{t}^{2}}})}^{2}} \\  & =\sqrt{1+\frac{{t}^{2}}{4-{t}^{2}}} \\  & =\frac{2}{\sqrt{4-{t}^{2}}}\end{aligned}
$$

Now, since $f(x,y)=2xy$, we obtain

$$
\begin{aligned}f(r(t)) & =2t\sqrt{4-{t}^{2}}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{\frac{1}{4}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\frac{1}{4}}2t\sqrt{4-{t}^{2}}\cdot \frac{2}{\sqrt{4-{t}^{2}}}\cdot \text{d}t \\  & =4{\int }_{0}^{\frac{1}{4}}t\,\text{d}t \\  & =2{t}^{2}\,{|}_{0}^{\frac{1}{4}} \\  & =2(\frac{1}{4}^{2}-0^{2}) \\  & = \frac{1}{8}.\end{aligned}
$$

## Generated variant — line_sum / authored_operations

Evaluate the integral of the function $f(x,y)=x+y$ along the line $y=x,$ $\,0\le x\le 6.$

- $- 36 \sqrt{2}$

- $72$

- $36$

- $36 \sqrt{2}$ **Correct**

- $12 \sqrt{2}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=t.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,t⟩,\,0\le t\le 6
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(t)j \\  & =i+\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{1}^{2}} \\  & =\sqrt{2}\end{aligned}
$$

Now, since $f(x,y)=x+y$, we obtain

$$
\begin{aligned}f(r(t)) & =t+t=2t.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{6}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{6}2t\cdot \sqrt{2}\cdot \text{d}t \\  & =2\sqrt{2}{\int }_{0}^{6}t\,\text{d}t \\  & =\sqrt{2}\,{t}^{2}{|}_{0}^{6} \\  & =\sqrt{2}(6^{2}-0^{2}) \\  & =36 \sqrt{2}.\end{aligned}
$$

## Generated variant — line_sum / authored_operations

Evaluate the integral of the function $f(x,y)=x+y$ along the line $y=x,$ $\,0\le x\le 4.$

- $32$

- $8 \sqrt{2}$

- $16$

- $16 \sqrt{2}$ **Correct**

- $- 16 \sqrt{2}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=t.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,t⟩,\,0\le t\le 4
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(t)j \\  & =i+\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{1}^{2}} \\  & =\sqrt{2}\end{aligned}
$$

Now, since $f(x,y)=x+y$, we obtain

$$
\begin{aligned}f(r(t)) & =t+t=2t.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{4}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{4}2t\cdot \sqrt{2}\cdot \text{d}t \\  & =2\sqrt{2}{\int }_{0}^{4}t\,\text{d}t \\  & =\sqrt{2}\,{t}^{2}{|}_{0}^{4} \\  & =\sqrt{2}(4^{2}-0^{2}) \\  & =16 \sqrt{2}.\end{aligned}
$$

## Generated variant — line_sum / observed_expression_pattern_unresolved_intent

Evaluate the integral of the function $f(x,y)=x+y$ along the line $y=x,$ $\,0\le x\le 7.$

- $49 \sqrt{2}$ **Correct**

- $\frac{\sqrt{2}}{49}$

- $\frac{\sqrt{2}}{7}$

- $7 \sqrt{2}$

- $49$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=t.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,t⟩,\,0\le t\le 7
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(t)j \\  & =i+\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{1}^{2}} \\  & =\sqrt{2}\end{aligned}
$$

Now, since $f(x,y)=x+y$, we obtain

$$
\begin{aligned}f(r(t)) & =t+t=2t.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{7}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{7}2t\cdot \sqrt{2}\cdot \text{d}t \\  & =2\sqrt{2}{\int }_{0}^{7}t\,\text{d}t \\  & =\sqrt{2}\,{t}^{2}{|}_{0}^{7} \\  & =\sqrt{2}(7^{2}-0^{2}) \\  & =49 \sqrt{2}.\end{aligned}
$$

## Generated variant — line_polynomial / authored_operations

Evaluate the integral of the function $f(x,y)=({x}^{2}+y)$ along the line $y=3x+2,$ $\,0\le x\le \frac{13}{2}.$

- $- \frac{2015 \sqrt{10}}{12}$

- $\frac{10075}{6}$

- $\frac{2015}{12}$

- $\frac{2015 \sqrt{10}}{12}$ **Correct**

- $\frac{247 \sqrt{10}}{4}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=3t+2.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,3t+2⟩,\,0\le t\le \frac{13}{2}
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(3t+2)j \\  & =i+3\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{3}^{2}} \\  & =\sqrt{10}\end{aligned}
$$

Now, since $f(x,y)={x}^{2}+y$, we obtain

$$
\begin{aligned}f(r(t)) & ={t}^{2}+(3t+2)={t}^{2}+3t+2.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{\frac{13}{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\frac{13}{2}}({t}^{2}+3t+2)\cdot \sqrt{10}\cdot \text{d}t \\  & =\sqrt{10}{\int }_{0}^{\frac{13}{2}}({t}^{2}+3t+2)\,\text{d}t \\  & =\sqrt{10}\,(\frac{{t}^{3}}{3}+\frac{3{t}^{2}}{2}+2t){|}_{0}^{\frac{13}{2}} \\  & =\sqrt{10}(\frac{2197}{24}+\frac{507}{8}+13) \\  & =\frac{2015 \sqrt{10}}{12}.\end{aligned}
$$

## Generated variant — line_polynomial / authored_operations

Evaluate the integral of the function $f(x,y)=({x}^{2}+y)$ along the line $y=3x+2,$ $\,0\le x\le \frac{5}{2}.$

- $\frac{1175}{6}$

- $\frac{55 \sqrt{10}}{4}$

- $\frac{235}{12}$

- $\frac{235 \sqrt{10}}{12}$ **Correct**

- $- \frac{235 \sqrt{10}}{12}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=3t+2.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,3t+2⟩,\,0\le t\le \frac{5}{2}
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(3t+2)j \\  & =i+3\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{3}^{2}} \\  & =\sqrt{10}\end{aligned}
$$

Now, since $f(x,y)={x}^{2}+y$, we obtain

$$
\begin{aligned}f(r(t)) & ={t}^{2}+(3t+2)={t}^{2}+3t+2.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{\frac{5}{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\frac{5}{2}}({t}^{2}+3t+2)\cdot \sqrt{10}\cdot \text{d}t \\  & =\sqrt{10}{\int }_{0}^{\frac{5}{2}}({t}^{2}+3t+2)\,\text{d}t \\  & =\sqrt{10}\,(\frac{{t}^{3}}{3}+\frac{3{t}^{2}}{2}+2t){|}_{0}^{\frac{5}{2}} \\  & =\sqrt{10}(\frac{125}{24}+\frac{75}{8}+5) \\  & =\frac{235 \sqrt{10}}{12}.\end{aligned}
$$

## Generated variant — line_polynomial / observed_expression_pattern_unresolved_intent

Evaluate the integral of the function $f(x,y)=({x}^{2}+y)$ along the line $y=3x+2,$ $\,0\le x\le 7.$

- $\frac{7 \sqrt{10}}{3}$

- $\frac{7 \sqrt{5}}{6}$

- $21 \sqrt{5}$

- $\frac{1211 \sqrt{10}}{6}$ **Correct**

- $91 \sqrt{10}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=3t+2.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,3t+2⟩,\,0\le t\le 7
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(3t+2)j \\  & =i+3\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{3}^{2}} \\  & =\sqrt{10}\end{aligned}
$$

Now, since $f(x,y)={x}^{2}+y$, we obtain

$$
\begin{aligned}f(r(t)) & ={t}^{2}+(3t+2)={t}^{2}+3t+2.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{7}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{7}({t}^{2}+3t+2)\cdot \sqrt{10}\cdot \text{d}t \\  & =\sqrt{10}{\int }_{0}^{7}({t}^{2}+3t+2)\,\text{d}t \\  & =\sqrt{10}\,(\frac{{t}^{3}}{3}+\frac{3{t}^{2}}{2}+2t){|}_{0}^{7} \\  & =\sqrt{10}(\frac{343}{3}+\frac{147}{2}+14) \\  & =\frac{1211 \sqrt{10}}{6}.\end{aligned}
$$

## Generated variant — line_constant / authored_operations

Evaluate the integral of the function $f(x,y)=\frac{1}{x-y}$ along the line $y=x-4,$ $\,0\le x\le \frac{13}{2}.$

- $\frac{13 \sqrt{17}}{8}$

- $\frac{13}{4}$

- $\frac{13}{8}$

- $\frac{13 \sqrt{2}}{8}$ **Correct**

- $\frac{13 \sqrt{2}}{16}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=t-4.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,t-4⟩,\,0\le t\le \frac{13}{2}
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(t-4)j \\  & =i+\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{1}^{2}} \\  & =\sqrt{2}\end{aligned}
$$

Now, since $f(x,y)=\frac{1}{x-y}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{1}{t-(t-4)}=\frac{1}{4}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{\frac{13}{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\frac{13}{2}}\frac{1}{4}\cdot \sqrt{2}\cdot \text{d}t \\  & =\frac{\sqrt{2}}{4}{\int }_{0}^{\frac{13}{2}}\,\text{d}t \\  & =\frac{\sqrt{2}}{4}\,t\,{|}_{0}^{\frac{13}{2}} \\  & =\frac{\sqrt{2}}{4}(\frac{13}{2}-0) \\  & =\frac{13 \sqrt{2}}{8}.\end{aligned}
$$

## Generated variant — line_constant / authored_operations

Evaluate the integral of the function $f(x,y)=\frac{1}{x-y}$ along the line $y=x-4,$ $\,0\le x\le \frac{5}{2}.$

- $\frac{5}{4}$

- $\frac{5 \sqrt{2}}{16}$

- $\frac{5}{8}$

- $\frac{5 \sqrt{2}}{8}$ **Correct**

- $\frac{5 \sqrt{17}}{8}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=t-4.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,t-4⟩,\,0\le t\le \frac{5}{2}
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(t-4)j \\  & =i+\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{1}^{2}} \\  & =\sqrt{2}\end{aligned}
$$

Now, since $f(x,y)=\frac{1}{x-y}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{1}{t-(t-4)}=\frac{1}{4}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{\frac{5}{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\frac{5}{2}}\frac{1}{4}\cdot \sqrt{2}\cdot \text{d}t \\  & =\frac{\sqrt{2}}{4}{\int }_{0}^{\frac{5}{2}}\,\text{d}t \\  & =\frac{\sqrt{2}}{4}\,t\,{|}_{0}^{\frac{5}{2}} \\  & =\frac{\sqrt{2}}{4}(\frac{5}{2}-0) \\  & =\frac{5 \sqrt{2}}{8}.\end{aligned}
$$

## Generated variant — line_constant / observed_expression_pattern_unresolved_intent

Evaluate the integral of the function $f(x,y)=\frac{1}{x-y}$ along the line $y=x-4,$ $\,0\le x\le 7.$

- $\frac{21}{4}$

- $\frac{7}{4}$

- $\frac{7 \sqrt{2}}{4}$ **Correct**

- $\frac{7 \sqrt{2}}{2}$

- $7$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=t-4.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,t-4⟩,\,0\le t\le 7
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(t-4)j \\  & =i+\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{1}^{2}} \\  & =\sqrt{2}\end{aligned}
$$

Now, since $f(x,y)=\frac{1}{x-y}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{1}{t-(t-4)}=\frac{1}{4}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{7}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{7}\frac{1}{4}\cdot \sqrt{2}\cdot \text{d}t \\  & =\frac{\sqrt{2}}{4}{\int }_{0}^{7}\,\text{d}t \\  & =\frac{\sqrt{2}}{4}\,t\,{|}_{0}^{7} \\  & =\frac{\sqrt{2}}{4}(7-0) \\  & =\frac{7 \sqrt{2}}{4}.\end{aligned}
$$

## Generated variant — parabola / authored_operations

Evaluate the integral ${\int }_{C}\frac{y}{x}\,\text{d}s,$ where the curve $C$ is given by $y=\frac{{x}^{2}}{4},$ $\,0\le x\le 6 \sqrt{7}.$

- $63$

- $\frac{4095}{4}$

- $\frac{63}{2}$

- $\frac{511}{3}$ **Correct**

- $- \frac{511}{3}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\frac{{t}^{2}}{4}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,\frac{{t}^{2}}{4}⟩,\,0\le t\le 6 \sqrt{7}
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\frac{{t}^{2}}{4})j \\  & =i+\frac{t}{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(\frac{t}{2})}^{2}} \\  & =\sqrt{1+\frac{{t}^{2}}{4}}\end{aligned}
$$

Now, since $f(x,y)=\frac{y}{x}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{(\frac{{t}^{2}}{4})}{t}=\frac{t}{4}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}\frac{y}{x}\,\text{d}s & ={\int }_{0}^{6 \sqrt{7}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{6 \sqrt{7}}\frac{t}{4}\cdot \sqrt{1+\frac{{t}^{2}}{4}}\cdot \text{d}t \\  & =\frac{1}{4}{\int }_{0}^{6 \sqrt{7}}t\sqrt{1+\frac{{t}^{2}}{4}}\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=1+\frac{{t}^{2}}{4}$, $\text{d}u=\frac{t}{2}\,\text{d}t$ as follows: 

$$
\begin{aligned}\frac{1}{4}{\int }_{0}^{6 \sqrt{7}}t\sqrt{1+\frac{{t}^{2}}{4}}\text{d}t & =\frac{1}{2}{\int }_{1}^{64}{u}^{1/2}\,\text{d}u \\  & =\frac{{u}^{3/2}}{3}{|}_{1}^{64} \\  & =\frac{1}{3}({64}^{3/2}-{1}^{3/2}) \\  & =\frac{1}{3}(512-1) \\  & =\frac{511}{3}\end{aligned}
$$

## Generated variant — parabola / authored_operations

Evaluate the integral ${\int }_{C}\frac{y}{x}\,\text{d}s,$ where the curve $C$ is given by $y=\frac{{x}^{2}}{4},$ $\,0\le x\le 2 \sqrt{15}.$

- $\frac{255}{4}$

- $-21$

- $\frac{15}{2}$

- $21$ **Correct**

- $15$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\frac{{t}^{2}}{4}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,\frac{{t}^{2}}{4}⟩,\,0\le t\le 2 \sqrt{15}
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\frac{{t}^{2}}{4})j \\  & =i+\frac{t}{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(\frac{t}{2})}^{2}} \\  & =\sqrt{1+\frac{{t}^{2}}{4}}\end{aligned}
$$

Now, since $f(x,y)=\frac{y}{x}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{(\frac{{t}^{2}}{4})}{t}=\frac{t}{4}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}\frac{y}{x}\,\text{d}s & ={\int }_{0}^{2 \sqrt{15}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{2 \sqrt{15}}\frac{t}{4}\cdot \sqrt{1+\frac{{t}^{2}}{4}}\cdot \text{d}t \\  & =\frac{1}{4}{\int }_{0}^{2 \sqrt{15}}t\sqrt{1+\frac{{t}^{2}}{4}}\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=1+\frac{{t}^{2}}{4}$, $\text{d}u=\frac{t}{2}\,\text{d}t$ as follows: 

$$
\begin{aligned}\frac{1}{4}{\int }_{0}^{2 \sqrt{15}}t\sqrt{1+\frac{{t}^{2}}{4}}\text{d}t & =\frac{1}{2}{\int }_{1}^{16}{u}^{1/2}\,\text{d}u \\  & =\frac{{u}^{3/2}}{3}{|}_{1}^{16} \\  & =\frac{1}{3}({16}^{3/2}-{1}^{3/2}) \\  & =\frac{1}{3}(64-1) \\  & =21\end{aligned}
$$

## Generated variant — parabola / observed_expression_pattern_unresolved_intent

Evaluate the integral ${\int }_{C}\frac{y}{x}\,\text{d}s,$ where the curve $C$ is given by $y=\frac{{x}^{2}}{4},$ $\,0\le x\le 6 \sqrt{11}.$

- $333$ **Correct**

- $\frac{1000}{3}$

- $\frac{\sqrt{10}}{3}$

- $\frac{100}{3}$

- $\frac{10 \sqrt{10}}{3}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\frac{{t}^{2}}{4}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,\frac{{t}^{2}}{4}⟩,\,0\le t\le 6 \sqrt{11}
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\frac{{t}^{2}}{4})j \\  & =i+\frac{t}{2}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(\frac{t}{2})}^{2}} \\  & =\sqrt{1+\frac{{t}^{2}}{4}}\end{aligned}
$$

Now, since $f(x,y)=\frac{y}{x}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{(\frac{{t}^{2}}{4})}{t}=\frac{t}{4}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}\frac{y}{x}\,\text{d}s & ={\int }_{0}^{6 \sqrt{11}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{6 \sqrt{11}}\frac{t}{4}\cdot \sqrt{1+\frac{{t}^{2}}{4}}\cdot \text{d}t \\  & =\frac{1}{4}{\int }_{0}^{6 \sqrt{11}}t\sqrt{1+\frac{{t}^{2}}{4}}\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=1+\frac{{t}^{2}}{4}$, $\text{d}u=\frac{t}{2}\,\text{d}t$ as follows: 

$$
\begin{aligned}\frac{1}{4}{\int }_{0}^{6 \sqrt{11}}t\sqrt{1+\frac{{t}^{2}}{4}}\text{d}t & =\frac{1}{2}{\int }_{1}^{100}{u}^{1/2}\,\text{d}u \\  & =\frac{{u}^{3/2}}{3}{|}_{1}^{100} \\  & =\frac{1}{3}({100}^{3/2}-{1}^{3/2}) \\  & =\frac{1}{3}(1000-1) \\  & =333\end{aligned}
$$

## Generated variant — reciprocal / authored_operations

Evaluate the integral ${\int }_{C}\frac{4{y}^{2}}{{x}^{3}}\,\text{d}s,$ where the curve $C$ is given by $y=\frac{1}{x},$ $\,1\le x\le 2^{\frac{3}{4}}.$

- $\frac{1}{2} - \frac{\sqrt[4]{2}}{4}$

- $\frac{175}{128}$

- $\frac{7}{8}$

- $\frac{37 \sqrt{2}}{48}$ **Correct**

- $- \frac{37 \sqrt{2}}{48}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\frac{1}{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,\frac{1}{t}⟩,\,1\le t\le 2^{\frac{3}{4}}
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\frac{1}{t})j \\  & =i-\frac{1}{{t}^{2}}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(-\frac{1}{{t}^{2}})}^{2}} \\  & =\sqrt{1+\frac{1}{{t}^{4}}}\end{aligned}
$$

Now, since $f(x,y)=\frac{4{y}^{2}}{{x}^{3}}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{4{(\frac{1}{t})}^{2}}{{t}^{3}}=\frac{4}{{t}^{5}}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}\frac{4{y}^{2}}{{x}^{3}}\,\text{d}s & ={\int }_{1}^{2^{\frac{3}{4}}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{2^{\frac{3}{4}}}\frac{4}{{t}^{5}}\cdot \sqrt{1+\frac{1}{{t}^{4}}}\cdot \text{d}t \\  & =4{\int }_{1}^{2^{\frac{3}{4}}}\frac{1}{{t}^{5}}\,\sqrt{1+\frac{1}{{t}^{4}}}\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=1+\frac{1}{{t}^{4}}$, $\text{d}u=-\frac{4}{{t}^{5}}\,\text{d}t$ as follows: 

$$
\begin{aligned}4{\int }_{1}^{2^{\frac{3}{4}}}\frac{1}{{t}^{5}}\,\sqrt{1+\frac{1}{{t}^{4}}}\,\text{d}t & =-{\int }_{2}^{\frac{9}{8}}{u}^{1/2}\,\text{d}u \\  & =-\frac{2}{3}{u}^{3/2}{|}_{2}^{\frac{9}{8}} \\  & =-\frac{2}{3}(\sqrt{(\frac{9}{8})^{3}}-\sqrt{{2}^{3}}) \\  & =-\frac{2}{3}(\frac{27 \sqrt{2}}{32}-2\sqrt{2}) \\  & =\frac{37 \sqrt{2}}{48}\end{aligned}
$$

## Generated variant — reciprocal / authored_operations

Evaluate the integral ${\int }_{C}\frac{4{y}^{2}}{{x}^{3}}\,\text{d}s,$ where the curve $C$ is given by $y=\frac{1}{x},$ $\,1\le x\le \sqrt{2}.$

- $\frac{39}{32}$

- $- \frac{4 \sqrt{2}}{3} + \frac{5 \sqrt{5}}{12}$

- $\frac{3}{4}$

- $- \frac{5 \sqrt{5}}{12} + \frac{4 \sqrt{2}}{3}$ **Correct**

- $1 - \frac{\sqrt{2}}{2}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\frac{1}{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,\frac{1}{t}⟩,\,1\le t\le \sqrt{2}
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\frac{1}{t})j \\  & =i-\frac{1}{{t}^{2}}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(-\frac{1}{{t}^{2}})}^{2}} \\  & =\sqrt{1+\frac{1}{{t}^{4}}}\end{aligned}
$$

Now, since $f(x,y)=\frac{4{y}^{2}}{{x}^{3}}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{4{(\frac{1}{t})}^{2}}{{t}^{3}}=\frac{4}{{t}^{5}}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}\frac{4{y}^{2}}{{x}^{3}}\,\text{d}s & ={\int }_{1}^{\sqrt{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{\sqrt{2}}\frac{4}{{t}^{5}}\cdot \sqrt{1+\frac{1}{{t}^{4}}}\cdot \text{d}t \\  & =4{\int }_{1}^{\sqrt{2}}\frac{1}{{t}^{5}}\,\sqrt{1+\frac{1}{{t}^{4}}}\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=1+\frac{1}{{t}^{4}}$, $\text{d}u=-\frac{4}{{t}^{5}}\,\text{d}t$ as follows: 

$$
\begin{aligned}4{\int }_{1}^{\sqrt{2}}\frac{1}{{t}^{5}}\,\sqrt{1+\frac{1}{{t}^{4}}}\,\text{d}t & =-{\int }_{2}^{\frac{5}{4}}{u}^{1/2}\,\text{d}u \\  & =-\frac{2}{3}{u}^{3/2}{|}_{2}^{\frac{5}{4}} \\  & =-\frac{2}{3}(\sqrt{(\frac{5}{4})^{3}}-\sqrt{{2}^{3}}) \\  & =-\frac{2}{3}(\frac{5 \sqrt{5}}{8}-2\sqrt{2}) \\  & =- \frac{5 \sqrt{5}}{12} + \frac{4 \sqrt{2}}{3}\end{aligned}
$$

## Generated variant — reciprocal / observed_expression_pattern_unresolved_intent

Evaluate the integral ${\int }_{C}\frac{4{y}^{2}}{{x}^{3}}\,\text{d}s,$ where the curve $C$ is given by $y=\frac{1}{x},$ $\,1\le x\le \sqrt[4]{10}.$

- $- \frac{22 \sqrt{110}}{25} + 16 \sqrt{2}$

- $\frac{44 \sqrt{110}}{25}$

- $32 \sqrt{2}$

- $- \frac{11 \sqrt{110}}{150} + \frac{4 \sqrt{2}}{3}$ **Correct**

- $- \frac{44 \sqrt{110}}{25} + 32 \sqrt{2}$

Worked solution:

Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)=\frac{1}{t}.$ This gives the following parametrization of the curve:

$$
r(t)=⟨t,\,\frac{1}{t}⟩,\,1\le t\le \sqrt[4]{10}
$$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(\frac{1}{t})j \\  & =i-\frac{1}{{t}^{2}}\,j \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+{(-\frac{1}{{t}^{2}})}^{2}} \\  & =\sqrt{1+\frac{1}{{t}^{4}}}\end{aligned}
$$

Now, since $f(x,y)=\frac{4{y}^{2}}{{x}^{3}}$, we obtain

$$
\begin{aligned}f(r(t)) & =\frac{4{(\frac{1}{t})}^{2}}{{t}^{3}}=\frac{4}{{t}^{5}}.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}{\int }_{C}\frac{4{y}^{2}}{{x}^{3}}\,\text{d}s & ={\int }_{1}^{\sqrt[4]{10}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{\sqrt[4]{10}}\frac{4}{{t}^{5}}\cdot \sqrt{1+\frac{1}{{t}^{4}}}\cdot \text{d}t \\  & =4{\int }_{1}^{\sqrt[4]{10}}\frac{1}{{t}^{5}}\,\sqrt{1+\frac{1}{{t}^{4}}}\,\text{d}t.\end{aligned}
$$

We can solve this using the substitution $u=1+\frac{1}{{t}^{4}}$, $\text{d}u=-\frac{4}{{t}^{5}}\,\text{d}t$ as follows: 

$$
\begin{aligned}4{\int }_{1}^{\sqrt[4]{10}}\frac{1}{{t}^{5}}\,\sqrt{1+\frac{1}{{t}^{4}}}\,\text{d}t & =-{\int }_{2}^{\frac{11}{10}}{u}^{1/2}\,\text{d}u \\  & =-\frac{2}{3}{u}^{3/2}{|}_{2}^{\frac{11}{10}} \\  & =-\frac{2}{3}(\sqrt{(\frac{11}{10})^{3}}-\sqrt{{2}^{3}}) \\  & =-\frac{2}{3}(\frac{11 \sqrt{110}}{100}-2\sqrt{2}) \\  & =- \frac{11 \sqrt{110}}{150} + \frac{4 \sqrt{2}}{3}\end{aligned}
$$