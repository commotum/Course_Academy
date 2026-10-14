# Source evidence and generated review

All observed banks are opaque historical evidence; normal examples use authored method banks. Raw anomalous originals remain explicitly ineligible.

## Original q-109119

Use Green's theorem to evaluate ${∮}_{C}F\cdot dr,$ where $F(x,y)=⟨{x}^{2}y-\operatorname{cos}⁡x,4-x{y}^{2}⟩$ and $C$ is the circle ${x}^{2}+{y}^{2}=4,$ oriented counterclockwise.

Source bank: $16\pi $, $-20\pi $, $\frac{13\pi }{2}$, $-8\pi $, $-\frac{9\pi }{2}$

First, notice that we can rewrite our integral as 

$$
{∮}_{C}F\cdot dr={∮}_{C}({x}^{2}y-\operatorname{cos}⁡x)\,dx+(4-x{y}^{2})\,dy.
$$

Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](images/09/09a69771617d73af6e4a1a42720223951e2e6edeb71a8df4d12aeb1bc22031aa.png)

Now, since 

$$
P(x,y)={x}^{2}y-\operatorname{cos}⁡x,\,Q(x,y)=4-x{y}^{2},
$$

we have that

$$
\begin{aligned}\frac{∂P}{∂y}={x}^{2},\,\frac{∂Q}{∂x}=-{y}^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}{∮}_{C}({x}^{2}y-\operatorname{cos}⁡x)\,dx+(4-x{y}^{2})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & ={∬}_{D}(-{y}^{2}-{x}^{2})\,\text{d}A \\  & ={∬}_{D}-({x}^{2}+{y}^{2})\,\text{d}A.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
Δ={(r,\theta )\,:\,0\le r\le 2,\,0\le \theta \le 2\pi }.
$$

The change of variables formula for plane polar coordinates states that

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}{∬}_{D}-({x}^{2}+{y}^{2})\,\text{d}A & ={∬}_{Δ}-({r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta )\,r\,\text{d}r\text{d}\theta  \\  & =-{\int }_{0}^{2\pi }{\int }_{0}^{2}{r}^{3}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & =-{\int }_{0}^{2\pi }{\int }_{0}^{2}{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & =-{\int }_{0}^{2\pi }[\frac{{r}^{4}}{4}]_{0}^{2}\,\text{d}\theta  \\  & =-{\int }_{0}^{2\pi }4\,\text{d}\theta  \\  & =-4[\theta ]_{0}^{2\pi } \\  & =-4(2\pi -0) \\  & =-8\pi \end{aligned}
$$

### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle x^2y-\cos x,4-xy^2\rangle$ and $C$ is the circle $x^2+y^2=4,$ oriented counterclockwise.

- $- \frac{16 \pi}{3}$

- $8 \pi$

- $- 8 \pi$

- $- 4 \pi$

- $- 32 \pi$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(x^2y-\cos x)\,dx+(4-xy^2)\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/95b347882765352377ac71e985c8c96cf10411cedd7ea3c3d3922afac3ceb594.png)

Now, since

$$
P(x,y)=x^2y-\cos x,\quad Q(x,y)=4-xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=x^{2},\quad \frac{\partial Q}{\partial x}=- y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(x^2y-\cos x)\,dx+(4-xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(- y^{2}-(x^{2})\right)\,dA \\ &=\iint_D -(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 2,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D -(x^2+y^2)\,dA&=\iint_\Delta -(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=-\int_{0}^{2 \pi}\int_{0}^{2}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=-\int_{0}^{2 \pi}\int_{0}^{2}r^3\,dr\,d\theta \\ &=-\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{2}\,d\theta \\ &=-\int_{0}^{2 \pi}\left(4-0\right)\,d\theta \\ &=-\int_{0}^{2 \pi}4\,d\theta \\ &=-4[\theta]_{0}^{2 \pi} \\ &=-4\left(2 \pi-0\right) \\ &=- 8 \pi.\end{aligned}
$$



### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle 5x^2y-\cos x,4-5xy^2\rangle$ and $C$ is the circle $x^2+y^2=9,$ oriented counterclockwise.

- $- \frac{405 \pi}{2}$

- $- 90 \pi$

- $\frac{405 \pi}{2}$

- $- 810 \pi$

- $- \frac{405 \pi}{4}$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(5x^2y-\cos x)\,dx+(4-5xy^2)\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/6dbf71fec3d4d1f489cebd6d8ab224425d3cd4479fb355236f579b1db5392662.png)

Now, since

$$
P(x,y)=5x^2y-\cos x,\quad Q(x,y)=4-5xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=5 x^{2},\quad \frac{\partial Q}{\partial x}=- 5 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(5x^2y-\cos x)\,dx+(4-5xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(- 5 y^{2}-(5 x^{2})\right)\,dA \\ &=\iint_D -5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 3,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D -5(x^2+y^2)\,dA&=\iint_\Delta -5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=-5\int_{0}^{2 \pi}\int_{0}^{3}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=-5\int_{0}^{2 \pi}\int_{0}^{3}r^3\,dr\,d\theta \\ &=-5\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{3}\,d\theta \\ &=-5\int_{0}^{2 \pi}\left(\frac{81}{4}-0\right)\,d\theta \\ &=-5\int_{0}^{2 \pi}\frac{81}{4}\,d\theta \\ &=- \frac{405}{4}[\theta]_{0}^{2 \pi} \\ &=- \frac{405}{4}\left(2 \pi-0\right) \\ &=- \frac{405 \pi}{2}.\end{aligned}
$$



### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle 5x^2y-\cos x,4-5xy^2\rangle$ and $C$ is the circle $x^2+y^2=4,$ oriented counterclockwise.

- $40 \pi$

- $- 40 \pi$

- $- 160 \pi$

- $- \frac{80 \pi}{3}$

- $- 20 \pi$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(5x^2y-\cos x)\,dx+(4-5xy^2)\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/95b347882765352377ac71e985c8c96cf10411cedd7ea3c3d3922afac3ceb594.png)

Now, since

$$
P(x,y)=5x^2y-\cos x,\quad Q(x,y)=4-5xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=5 x^{2},\quad \frac{\partial Q}{\partial x}=- 5 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(5x^2y-\cos x)\,dx+(4-5xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(- 5 y^{2}-(5 x^{2})\right)\,dA \\ &=\iint_D -5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 2,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D -5(x^2+y^2)\,dA&=\iint_\Delta -5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=-5\int_{0}^{2 \pi}\int_{0}^{2}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=-5\int_{0}^{2 \pi}\int_{0}^{2}r^3\,dr\,d\theta \\ &=-5\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{2}\,d\theta \\ &=-5\int_{0}^{2 \pi}\left(4-0\right)\,d\theta \\ &=-5\int_{0}^{2 \pi}4\,d\theta \\ &=-20[\theta]_{0}^{2 \pi} \\ &=-20\left(2 \pi-0\right) \\ &=- 40 \pi.\end{aligned}
$$



### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle 5x^2y-\cos x,4-5xy^2\rangle$ and $C$ is the circle $x^2+y^2=9,$ oriented counterclockwise.

- $- \frac{405 \pi}{2}$

- $- 90 \pi$

- $\frac{405 \pi}{2}$

- $- 810 \pi$

- $- \frac{405 \pi}{4}$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(5x^2y-\cos x)\,dx+(4-5xy^2)\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/6dbf71fec3d4d1f489cebd6d8ab224425d3cd4479fb355236f579b1db5392662.png)

Now, since

$$
P(x,y)=5x^2y-\cos x,\quad Q(x,y)=4-5xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=5 x^{2},\quad \frac{\partial Q}{\partial x}=- 5 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(5x^2y-\cos x)\,dx+(4-5xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(- 5 y^{2}-(5 x^{2})\right)\,dA \\ &=\iint_D -5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 3,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D -5(x^2+y^2)\,dA&=\iint_\Delta -5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=-5\int_{0}^{2 \pi}\int_{0}^{3}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=-5\int_{0}^{2 \pi}\int_{0}^{3}r^3\,dr\,d\theta \\ &=-5\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{3}\,d\theta \\ &=-5\int_{0}^{2 \pi}\left(\frac{81}{4}-0\right)\,d\theta \\ &=-5\int_{0}^{2 \pi}\frac{81}{4}\,d\theta \\ &=- \frac{405}{4}[\theta]_{0}^{2 \pi} \\ &=- \frac{405}{4}\left(2 \pi-0\right) \\ &=- \frac{405 \pi}{2}.\end{aligned}
$$



## Original q-125717

![](images/66/66ab1a3e2e7244a9b3e5fc9bda814736194c28dd9438fbb97086e99be4633261.png)

Evaluate $∮_(C)(\sqrt{x} - 4x^{2}y)dx + (e^{y} + 4xy^{2})dy$, where the path $C$ is shown above.

Source bank: $-4π$, $2π$, $-\frac{π}{2}$, $8π$, $4π$

Original worked solution absent; no original difficulty or correct designation.

### Generated :question.difficulty/hard; authored method bank

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/4fce3c4d86780eedc114f529dd302e94475d856745c4bbb479ee5cbb12b0d056.png)

Evaluate $\oint_C(\sqrt{x+1}-4x^2y)\,dx+(e^y+4xy^2)\,dy,$ where the path $C$ is shown above.

- $\frac{16 \pi}{3}$

- $- 8 \pi$

- $8 \pi$

- $4 \pi$

- $32 \pi$


Worked solution


Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/79190b83bb26b855845a9df56083872b9efe1a99c8be476c4b015d44be35e18c.png)

Now, since

$$
P(x,y)=\sqrt{x+1}-4x^2y,\quad Q(x,y)=e^y+4xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 4 x^{2},\quad \frac{\partial Q}{\partial x}=4 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(\sqrt{x+1}-4x^2y)\,dx+(e^y+4xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(4 y^{2}-(- 4 x^{2})\right)\,dA \\ &=\iint_D 4(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 2,0\le\theta\le \frac{\pi}{2}\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 4(x^2+y^2)\,dA&=\iint_\Delta 4(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=4\int_{0}^{\frac{\pi}{2}}\int_{0}^{2}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=4\int_{0}^{\frac{\pi}{2}}\int_{0}^{2}r^3\,dr\,d\theta \\ &=4\int_{0}^{\frac{\pi}{2}}\left[\frac{r^4}{4}\right]_{0}^{2}\,d\theta \\ &=4\int_{0}^{\frac{\pi}{2}}\left(4-0\right)\,d\theta \\ &=4\int_{0}^{\frac{\pi}{2}}4\,d\theta \\ &=16[\theta]_{0}^{\frac{\pi}{2}} \\ &=16\left(\frac{\pi}{2}-0\right) \\ &=8 \pi.\end{aligned}
$$



### Generated :question.difficulty/hard; authored method bank

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/d6eee734a12b8fd4ce75badd1ac235c818098b7257063679172bf23286499d97.png)

Evaluate $\oint_C(\sqrt{x+1}-5x^2y)\,dx+(e^y+5xy^2)\,dy,$ where the path $C$ is shown above.

- $\frac{3125 \pi}{8}$

- $\frac{625 \pi}{6}$

- $- \frac{3125 \pi}{8}$

- $\frac{3125 \pi}{2}$

- $\frac{3125 \pi}{16}$


Worked solution


Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/cb56b829d2c3e042e45acc5e86814e3062374171788e11496d6cc9970a26e47e.png)

Now, since

$$
P(x,y)=\sqrt{x+1}-5x^2y,\quad Q(x,y)=e^y+5xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 x^{2},\quad \frac{\partial Q}{\partial x}=5 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(\sqrt{x+1}-5x^2y)\,dx+(e^y+5xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 y^{2}-(- 5 x^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 5,0\le\theta\le \frac{\pi}{2}\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\int_{0}^{5}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\int_{0}^{5}r^3\,dr\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\left[\frac{r^4}{4}\right]_{0}^{5}\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\left(\frac{625}{4}-0\right)\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\frac{625}{4}\,d\theta \\ &=\frac{3125}{4}[\theta]_{0}^{\frac{\pi}{2}} \\ &=\frac{3125}{4}\left(\frac{\pi}{2}-0\right) \\ &=\frac{3125 \pi}{8}.\end{aligned}
$$



### Generated :question.difficulty/hard; authored method bank

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/b14c1a6b82ba3f1856e9c76ca11d279bde92fe090c2e51d76aacac30fd7de927.png)

Evaluate $\oint_C(\sqrt{x+1}-5x^2y)\,dx+(e^y+5xy^2)\,dy,$ where the path $C$ is shown above.

- $- 160 \pi$

- $160 \pi$

- $640 \pi$

- $\frac{160 \pi}{3}$

- $80 \pi$


Worked solution


Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/96d5a78383242eed8f3a4fec6af9c389063fcdf0b1c4fa4de5b92eb52a3c4d71.png)

Now, since

$$
P(x,y)=\sqrt{x+1}-5x^2y,\quad Q(x,y)=e^y+5xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 x^{2},\quad \frac{\partial Q}{\partial x}=5 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(\sqrt{x+1}-5x^2y)\,dx+(e^y+5xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 y^{2}-(- 5 x^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 4,0\le\theta\le \frac{\pi}{2}\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\int_{0}^{4}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\int_{0}^{4}r^3\,dr\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\left[\frac{r^4}{4}\right]_{0}^{4}\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\left(64-0\right)\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}64\,d\theta \\ &=320[\theta]_{0}^{\frac{\pi}{2}} \\ &=320\left(\frac{\pi}{2}-0\right) \\ &=160 \pi.\end{aligned}
$$



### Generated :question.difficulty/hard; authored method bank

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/d6eee734a12b8fd4ce75badd1ac235c818098b7257063679172bf23286499d97.png)

Evaluate $\oint_C(\sqrt{x+1}-5x^2y)\,dx+(e^y+5xy^2)\,dy,$ where the path $C$ is shown above.

- $\frac{3125 \pi}{8}$

- $\frac{625 \pi}{6}$

- $- \frac{3125 \pi}{8}$

- $\frac{3125 \pi}{2}$

- $\frac{3125 \pi}{16}$


Worked solution


Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/cb56b829d2c3e042e45acc5e86814e3062374171788e11496d6cc9970a26e47e.png)

Now, since

$$
P(x,y)=\sqrt{x+1}-5x^2y,\quad Q(x,y)=e^y+5xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 x^{2},\quad \frac{\partial Q}{\partial x}=5 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(\sqrt{x+1}-5x^2y)\,dx+(e^y+5xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 y^{2}-(- 5 x^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 5,0\le\theta\le \frac{\pi}{2}\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\int_{0}^{5}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\int_{0}^{5}r^3\,dr\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\left[\frac{r^4}{4}\right]_{0}^{5}\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\left(\frac{625}{4}-0\right)\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\frac{625}{4}\,d\theta \\ &=\frac{3125}{4}[\theta]_{0}^{\frac{\pi}{2}} \\ &=\frac{3125}{4}\left(\frac{\pi}{2}-0\right) \\ &=\frac{3125 \pi}{8}.\end{aligned}
$$



## Original q-126733

Use Green's theorem to evaluate ${∮}_{C}F\cdot dr,$ where $F(x,y)=⟨2-{x}^{2}y,1+x{y}^{2}⟩$ and $C$ is the circle ${x}^{2}+{y}^{2}=25,$ oriented counterclockwise.

Source bank: $\frac{5\pi }{4}$, $\frac{125\pi }{2}$, $\frac{25\pi }{4}$, $625\pi $, $\frac{625\pi }{2}$

First, notice that we can rewrite our integral as 

$$
{∮}_{C}F\cdot dr={∮}_{C}(2-{x}^{2}y)\,dx+(1+x{y}^{2})\,dy.
$$

Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](images/d0/d081f4dc19484f0c483c5518295c7c3b7195bb096404fb7ff6e27d8bda1cccc1.png)

Now, since 

$$
P(x,y)=2-{x}^{2}y,\,Q(x,y)=1+x{y}^{2},
$$

 we have that

$$
\begin{aligned}\frac{∂P}{∂y}=-{x}^{2},\,\frac{∂Q}{∂x}={y}^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}{∮}_{C}(2-{x}^{2}y)\,dx+(1+x{y}^{2})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & ={∬}_{D}({y}^{2}-(-{x}^{2}))\,\text{d}A \\  & ={∬}_{D}({y}^{2}+{x}^{2})\,\text{d}A.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
Δ={(r,\theta )\,:\,0\le r\le 5,\,0\le \theta \le 2\pi }.
$$

The change of variables formula for plane polar coordinates states that

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Finally, we can calculate our double integral, as follows: 

$$
\begin{aligned}{∬}_{D}({x}^{2}+{y}^{2})\,\text{d}A & ={∬}_{Δ}({r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta )\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{5}{r}^{3}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{5}{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }[\frac{{r}^{4}}{4}]_{0}^{5}\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }\frac{625}{4}\,\text{d}\theta  \\  & =\frac{625}{4}[\theta ]_{0}^{2\pi } \\  & =\frac{625}{4}(2\pi -0) \\  & =\frac{625\pi }{2}.\end{aligned}
$$

### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle 2-x^2y,1+xy^2\rangle$ and $C$ is the circle $x^2+y^2=25,$ oriented counterclockwise.

- $\frac{250 \pi}{3}$

- $- \frac{625 \pi}{2}$

- $\frac{625 \pi}{2}$

- $\frac{625 \pi}{4}$

- $1250 \pi$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(2-x^2y)\,dx+(1+xy^2)\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/0a738176367aa859654ca169ac13cf5cb713ffd400f98dbb7b59ea6a095d9af5.png)

Now, since

$$
P(x,y)=2-x^2y,\quad Q(x,y)=1+xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- x^{2},\quad \frac{\partial Q}{\partial x}=y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(2-x^2y)\,dx+(1+xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(y^{2}-(- x^{2})\right)\,dA \\ &=\iint_D (x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 5,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D (x^2+y^2)\,dA&=\iint_\Delta (r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=\int_{0}^{2 \pi}\int_{0}^{5}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=\int_{0}^{2 \pi}\int_{0}^{5}r^3\,dr\,d\theta \\ &=\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{5}\,d\theta \\ &=\int_{0}^{2 \pi}\left(\frac{625}{4}-0\right)\,d\theta \\ &=\int_{0}^{2 \pi}\frac{625}{4}\,d\theta \\ &=\frac{625}{4}[\theta]_{0}^{2 \pi} \\ &=\frac{625}{4}\left(2 \pi-0\right) \\ &=\frac{625 \pi}{2}.\end{aligned}
$$



### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle 2-5x^2y,1+5xy^2\rangle$ and $C$ is the circle $x^2+y^2=9,$ oriented counterclockwise.

- $\frac{405 \pi}{2}$

- $90 \pi$

- $- \frac{405 \pi}{2}$

- $810 \pi$

- $\frac{405 \pi}{4}$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(2-5x^2y)\,dx+(1+5xy^2)\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/6dbf71fec3d4d1f489cebd6d8ab224425d3cd4479fb355236f579b1db5392662.png)

Now, since

$$
P(x,y)=2-5x^2y,\quad Q(x,y)=1+5xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 x^{2},\quad \frac{\partial Q}{\partial x}=5 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(2-5x^2y)\,dx+(1+5xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 y^{2}-(- 5 x^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 3,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{3}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{3}r^3\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{3}\,d\theta \\ &=5\int_{0}^{2 \pi}\left(\frac{81}{4}-0\right)\,d\theta \\ &=5\int_{0}^{2 \pi}\frac{81}{4}\,d\theta \\ &=\frac{405}{4}[\theta]_{0}^{2 \pi} \\ &=\frac{405}{4}\left(2 \pi-0\right) \\ &=\frac{405 \pi}{2}.\end{aligned}
$$



### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle 2-5x^2y,1+5xy^2\rangle$ and $C$ is the circle $x^2+y^2=4,$ oriented counterclockwise.

- $- 40 \pi$

- $40 \pi$

- $160 \pi$

- $\frac{80 \pi}{3}$

- $20 \pi$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(2-5x^2y)\,dx+(1+5xy^2)\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/95b347882765352377ac71e985c8c96cf10411cedd7ea3c3d3922afac3ceb594.png)

Now, since

$$
P(x,y)=2-5x^2y,\quad Q(x,y)=1+5xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 x^{2},\quad \frac{\partial Q}{\partial x}=5 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(2-5x^2y)\,dx+(1+5xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 y^{2}-(- 5 x^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 2,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{2}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{2}r^3\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{2}\,d\theta \\ &=5\int_{0}^{2 \pi}\left(4-0\right)\,d\theta \\ &=5\int_{0}^{2 \pi}4\,d\theta \\ &=20[\theta]_{0}^{2 \pi} \\ &=20\left(2 \pi-0\right) \\ &=40 \pi.\end{aligned}
$$



### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle 2-5x^2y,1+5xy^2\rangle$ and $C$ is the circle $x^2+y^2=9,$ oriented counterclockwise.

- $\frac{405 \pi}{2}$

- $90 \pi$

- $- \frac{405 \pi}{2}$

- $810 \pi$

- $\frac{405 \pi}{4}$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(2-5x^2y)\,dx+(1+5xy^2)\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/6dbf71fec3d4d1f489cebd6d8ab224425d3cd4479fb355236f579b1db5392662.png)

Now, since

$$
P(x,y)=2-5x^2y,\quad Q(x,y)=1+5xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 x^{2},\quad \frac{\partial Q}{\partial x}=5 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(2-5x^2y)\,dx+(1+5xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 y^{2}-(- 5 x^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 3,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{3}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{3}r^3\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{3}\,d\theta \\ &=5\int_{0}^{2 \pi}\left(\frac{81}{4}-0\right)\,d\theta \\ &=5\int_{0}^{2 \pi}\frac{81}{4}\,d\theta \\ &=\frac{405}{4}[\theta]_{0}^{2 \pi} \\ &=\frac{405}{4}\left(2 \pi-0\right) \\ &=\frac{405 \pi}{2}.\end{aligned}
$$



## Original q-126736

Use Green's theorem to evaluate ${∮}_{C}F\cdot dr,$ where $F(x,y)=⟨\operatorname{sin}⁡x-2{x}^{2}y,\text{ }\,\sqrt{y+3}+2x{y}^{2}⟩$ and $C$ is the circle ${x}^{2}+{y}^{2}=1,$ oriented counterclockwise.

Source bank: $\frac{3\pi }{2}$, $2\pi $, $\frac{\pi }{4}$, $\frac{\pi }{2}$, $\pi $

First, notice that we can rewrite our integral as 

$$
{∮}_{C}F\cdot dr={∮}_{C}(\operatorname{sin}⁡x-2{x}^{2}y)\,dx+(\sqrt{y+3}-2x{y}^{2})\,dy.
$$

Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](images/90/902790a00a049bbfc759403125ad5f19a8c2528a46b59c721ac43fb137cd5d8e.png)

Now, since 

$$
P(x,y)=\operatorname{sin}⁡x-2{x}^{2}y,\,Q(x,y)=\sqrt{y+3}+2x{y}^{2},
$$

 we have that

$$
\begin{aligned}\frac{∂P}{∂y}=-2{x}^{2},\,\frac{∂Q}{∂x}=2{y}^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}{∮}_{C}(\operatorname{sin}⁡x-2{x}^{2}y)\,dx+(\sqrt{y+3}-2x{y}^{2})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & ={∬}_{D}(2{y}^{2}-(-2{x}^{2}))\,\text{d}A \\  & ={∬}_{D}2({x}^{2}+{y}^{2})\,\text{d}A.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
Δ={(r,\theta )\,:\,0\le r\le 1,\,0\le \theta \le 2\pi }.
$$

The change of variables formula for plane polar coordinates states that

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Finally, we can calculate our double integral, as follows: 

$$
\begin{aligned}{∬}_{D}2({x}^{2}+{y}^{2})\,\text{d}A & ={∬}_{Δ}2({r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta )\,r\,\text{d}r\text{d}\theta  \\  & =2{\int }_{0}^{2\pi }{\int }_{0}^{1}{r}^{3}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & =2{\int }_{0}^{2\pi }{\int }_{0}^{1}{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & =2{\int }_{0}^{2\pi }[\frac{{r}^{4}}{4}]_{0}^{1}\,\text{d}\theta  \\  & =2{\int }_{0}^{2\pi }\frac{1}{4}\,\text{d}\theta  \\  & =\frac{1}{2}[\theta ]_{0}^{2\pi } \\  & =\pi \end{aligned}
$$

### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle \sin x-2x^2y,\sqrt{y+3}+2xy^2\rangle$ and $C$ is the circle $x^2+y^2=1,$ oriented counterclockwise.

- $\frac{4 \pi}{3}$

- $- \pi$

- $\pi$

- $\frac{\pi}{2}$

- $4 \pi$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(\sin x-2x^2y)\,dx+(\sqrt{y+3}+2xy^2)\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/efdff6a65c44890a566ac4b9963e7e26a3e85eb38607bf746bfe305093d3a6c0.png)

Now, since

$$
P(x,y)=\sin x-2x^2y,\quad Q(x,y)=\sqrt{y+3}+2xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 2 x^{2},\quad \frac{\partial Q}{\partial x}=2 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(\sin x-2x^2y)\,dx+(\sqrt{y+3}+2xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(2 y^{2}-(- 2 x^{2})\right)\,dA \\ &=\iint_D 2(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 1,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 2(x^2+y^2)\,dA&=\iint_\Delta 2(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=2\int_{0}^{2 \pi}\int_{0}^{1}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=2\int_{0}^{2 \pi}\int_{0}^{1}r^3\,dr\,d\theta \\ &=2\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{1}\,d\theta \\ &=2\int_{0}^{2 \pi}\left(\frac{1}{4}-0\right)\,d\theta \\ &=2\int_{0}^{2 \pi}\frac{1}{4}\,d\theta \\ &=\frac{1}{2}[\theta]_{0}^{2 \pi} \\ &=\pi.\end{aligned}
$$



### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle \sin x-5x^2y,\sqrt{y+3}+5xy^2\rangle$ and $C$ is the circle $x^2+y^2=2,$ oriented counterclockwise.

- $10 \pi$

- $\frac{20 \sqrt{2} \pi}{3}$

- $- 10 \pi$

- $40 \pi$

- $5 \pi$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(\sin x-5x^2y)\,dx+(\sqrt{y+3}+5xy^2)\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/c803dd5de2de64486bb24816426a08b47face5ddc1c156a1dd6068471cc068ce.png)

Now, since

$$
P(x,y)=\sin x-5x^2y,\quad Q(x,y)=\sqrt{y+3}+5xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 x^{2},\quad \frac{\partial Q}{\partial x}=5 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(\sin x-5x^2y)\,dx+(\sqrt{y+3}+5xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 y^{2}-(- 5 x^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le \sqrt{2},0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{\sqrt{2}}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{\sqrt{2}}r^3\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{\sqrt{2}}\,d\theta \\ &=5\int_{0}^{2 \pi}\left(1-0\right)\,d\theta \\ &=5\int_{0}^{2 \pi}1\,d\theta \\ &=5[\theta]_{0}^{2 \pi} \\ &=10 \pi.\end{aligned}
$$



### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle \sin x-5x^2y,\sqrt{y+3}+5xy^2\rangle$ and $C$ is the circle $x^2+y^2=2,$ oriented counterclockwise.

- $- 10 \pi$

- $10 \pi$

- $40 \pi$

- $\frac{20 \sqrt{2} \pi}{3}$

- $5 \pi$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(\sin x-5x^2y)\,dx+(\sqrt{y+3}+5xy^2)\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/c803dd5de2de64486bb24816426a08b47face5ddc1c156a1dd6068471cc068ce.png)

Now, since

$$
P(x,y)=\sin x-5x^2y,\quad Q(x,y)=\sqrt{y+3}+5xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 x^{2},\quad \frac{\partial Q}{\partial x}=5 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(\sin x-5x^2y)\,dx+(\sqrt{y+3}+5xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 y^{2}-(- 5 x^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le \sqrt{2},0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{\sqrt{2}}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{\sqrt{2}}r^3\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{\sqrt{2}}\,d\theta \\ &=5\int_{0}^{2 \pi}\left(1-0\right)\,d\theta \\ &=5\int_{0}^{2 \pi}1\,d\theta \\ &=5[\theta]_{0}^{2 \pi} \\ &=10 \pi.\end{aligned}
$$



### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle \sin x-5x^2y,\sqrt{y+3}+5xy^2\rangle$ and $C$ is the circle $x^2+y^2=2,$ oriented counterclockwise.

- $10 \pi$

- $\frac{20 \sqrt{2} \pi}{3}$

- $- 10 \pi$

- $40 \pi$

- $5 \pi$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(\sin x-5x^2y)\,dx+(\sqrt{y+3}+5xy^2)\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/c803dd5de2de64486bb24816426a08b47face5ddc1c156a1dd6068471cc068ce.png)

Now, since

$$
P(x,y)=\sin x-5x^2y,\quad Q(x,y)=\sqrt{y+3}+5xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 x^{2},\quad \frac{\partial Q}{\partial x}=5 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(\sin x-5x^2y)\,dx+(\sqrt{y+3}+5xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 y^{2}-(- 5 x^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le \sqrt{2},0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{\sqrt{2}}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{\sqrt{2}}r^3\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{\sqrt{2}}\,d\theta \\ &=5\int_{0}^{2 \pi}\left(1-0\right)\,d\theta \\ &=5\int_{0}^{2 \pi}1\,d\theta \\ &=5[\theta]_{0}^{2 \pi} \\ &=10 \pi.\end{aligned}
$$



## Original q-126747

![](images/21/21e8aa9acdca87acf153b2e7ad3f5e51d5708f53b81562e682e16098721d752a.png)

Evaluate ${∮}_{C}({3}^{x}+{x}^{2}y)dx+({2}^{y}+x{y}^{2})\,dy,$ where the path $C$ is shown above.

Source bank: $-\frac{8\pi }{3}$, $-16\sqrt{3}$, $8\sqrt{3}$, $8\pi $, $\frac{\sqrt{3}}{2}$

Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](images/92/922ae907661e21ea5510dc0d02f151afc4f4423ad11a572ede6849c623397baa.png)

Now, since 

$$
P(x,y)={3}^{x}+{x}^{2}y,\,Q(x,y)={2}^{y}+x{y}^{2},
$$

 we have that

$$
\begin{aligned}\frac{∂P}{∂y}={x}^{2},\,\frac{∂Q}{∂x}={y}^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}{∮}_{C}({3}^{x}+{x}^{2}y)dx+({2}^{y}+x{y}^{2})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & ={∬}_{D}({y}^{2}-{x}^{2})\,\text{d}A.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
Δ={(r,\theta )\,:\,0\le r\le 4,\,0\le \theta \le \frac{\pi }{3}}.
$$

The change of variables formula for plane polar coordinates states that

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}{∬}_{D}({y}^{2}-{x}^{2})\,\text{d}A & ={∬}_{Δ}({r}^{2}{sin}^{2}⁡\theta -{r}^{2}{cos}^{2}⁡\theta )\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{0}^{\pi /3}{\int }_{0}^{4}-{r}^{3}({cos}^{2}⁡\theta -{sin}^{2}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & =-{\int }_{0}^{\pi /3}\operatorname{cos}⁡(2\theta ){\int }_{0}^{4}{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & =-{\int }_{0}^{\pi /3}\operatorname{cos}⁡(2\theta ){[\frac{{r}^{4}}{4}]}_{0}^{4}\,\text{d}\theta  \\  & =-64{\int }_{0}^{\pi /3}\operatorname{cos}⁡(2\theta )\,\text{d}\theta  \\  & =-64{[\frac{\operatorname{sin}⁡(2\theta )}{2}]}_{0}^{\pi /3} \\  & =-32[\operatorname{sin}⁡(\frac{2\pi }{3})-\operatorname{sin}⁡0] \\  & =-16\sqrt{3}.\end{aligned}
$$

### Generated :question.difficulty/hard; authored method bank

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/f42c2e7a1f3ffb39ba9873ce30fbc024f8d4b53cd8ff7f6db00a09c6af29667e.png)

Evaluate $\oint_C(3^x+x^2y)\,dx+(2^y+xy^2)\,dy,$ where the path $C$ is shown above.

- $- 32 \sqrt{3}$

- $16 \sqrt{3}$

- $- 16 \sqrt{3}$

- $\frac{64 \pi}{3}$

- $- \frac{16 \sqrt{3}}{3}$


Worked solution


Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/d98a5c96ddff63e16c7af8bba9457e1f29089fe235ad179d95800e3b878fb3a9.png)

Now, since

$$
P(x,y)=3^x+x^2y,\quad Q(x,y)=2^y+xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=x^{2},\quad \frac{\partial Q}{\partial x}=y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(3^x+x^2y)\,dx+(2^y+xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(y^{2}-(x^{2})\right)\,dA\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 4,0\le\theta\le \frac{\pi}{3}\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D - x^{2} + y^{2}\,dA&=\iint_\Delta (r^2\sin^2\theta-r^2\cos^2\theta)\,r\,dr\,d\theta \\ &=\int_{0}^{\frac{\pi}{3}}\int_{0}^{4}-r^3(\cos^2\theta-\sin^2\theta)\,dr\,d\theta \\ &=-\int_{0}^{\frac{\pi}{3}}\cos(2\theta)\int_{0}^{4}r^3\,dr\,d\theta \\ &=-\int_{0}^{\frac{\pi}{3}}\cos(2\theta)\left[\frac{r^4}{4}\right]_{0}^{4}\,d\theta \\ &=-64\int_{0}^{\frac{\pi}{3}}\cos(2\theta)\,d\theta \\ &=-64\left[\frac{\sin(2\theta)}{2}\right]_{0}^{\frac{\pi}{3}} \\ &=-32\left(\sin(\frac{2 \pi}{3})-\sin(0)\right) \\ &=- 16 \sqrt{3}.\end{aligned}
$$



### Generated :question.difficulty/hard; authored method bank

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/1747f470795d617561561e7f2b96ef40a4ace9edb2095377edaea055516de890.png)

Evaluate $\oint_C(3^x+5x^2y)\,dx+(2^y+5xy^2)\,dy,$ where the path $C$ is shown above.

- $- \frac{3125 \sqrt{3}}{16}$

- $- \frac{3125 \sqrt{3}}{8}$

- $\frac{3125 \sqrt{3}}{16}$

- $- \frac{625 \sqrt{3}}{12}$

- $\frac{3125 \pi}{12}$


Worked solution


Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/d34d9f25c5307cf8aa107a6ab334a1698d3f3664f004d8de3cb5597e1882585f.png)

Now, since

$$
P(x,y)=3^x+5x^2y,\quad Q(x,y)=2^y+5xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=5 x^{2},\quad \frac{\partial Q}{\partial x}=5 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(3^x+5x^2y)\,dx+(2^y+5xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 y^{2}-(5 x^{2})\right)\,dA\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 5,0\le\theta\le \frac{\pi}{3}\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D - 5 x^{2} + 5 y^{2}\,dA&=\iint_\Delta 5(r^2\sin^2\theta-r^2\cos^2\theta)\,r\,dr\,d\theta \\ &=\int_{0}^{\frac{\pi}{3}}\int_{0}^{5}-5r^3(\cos^2\theta-\sin^2\theta)\,dr\,d\theta \\ &=-5\int_{0}^{\frac{\pi}{3}}\cos(2\theta)\int_{0}^{5}r^3\,dr\,d\theta \\ &=-5\int_{0}^{\frac{\pi}{3}}\cos(2\theta)\left[\frac{r^4}{4}\right]_{0}^{5}\,d\theta \\ &=-\frac{3125}{4}\int_{0}^{\frac{\pi}{3}}\cos(2\theta)\,d\theta \\ &=-\frac{3125}{4}\left[\frac{\sin(2\theta)}{2}\right]_{0}^{\frac{\pi}{3}} \\ &=-\frac{3125}{8}\left(\sin(\frac{2 \pi}{3})-\sin(0)\right) \\ &=- \frac{3125 \sqrt{3}}{16}.\end{aligned}
$$



### Generated :question.difficulty/hard; authored method bank

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/2aeef50b717012e2c125fb831804408bbdfbf171bf0b5df219a2f210fa097f8e.png)

Evaluate $\oint_C(3^x+5x^2y)\,dx+(2^y+5xy^2)\,dy,$ where the path $C$ is shown above.

- $- 80 \sqrt{3}$

- $80 \sqrt{3}$

- $\frac{80 \sqrt{3}}{3}$

- $160 \sqrt{3}$

- $\frac{640 \pi}{3}$


Worked solution


Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/2e966d3490e14a0a329a644bd1efde6d29b09dcb2f7b1871cab14ffa3b90b96e.png)

Now, since

$$
P(x,y)=3^x+5x^2y,\quad Q(x,y)=2^y+5xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=5 x^{2},\quad \frac{\partial Q}{\partial x}=5 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(3^x+5x^2y)\,dx+(2^y+5xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 y^{2}-(5 x^{2})\right)\,dA\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 4,0\le\theta\le \frac{2 \pi}{3}\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D - 5 x^{2} + 5 y^{2}\,dA&=\iint_\Delta 5(r^2\sin^2\theta-r^2\cos^2\theta)\,r\,dr\,d\theta \\ &=\int_{0}^{\frac{2 \pi}{3}}\int_{0}^{4}-5r^3(\cos^2\theta-\sin^2\theta)\,dr\,d\theta \\ &=-5\int_{0}^{\frac{2 \pi}{3}}\cos(2\theta)\int_{0}^{4}r^3\,dr\,d\theta \\ &=-5\int_{0}^{\frac{2 \pi}{3}}\cos(2\theta)\left[\frac{r^4}{4}\right]_{0}^{4}\,d\theta \\ &=-320\int_{0}^{\frac{2 \pi}{3}}\cos(2\theta)\,d\theta \\ &=-320\left[\frac{\sin(2\theta)}{2}\right]_{0}^{\frac{2 \pi}{3}} \\ &=-160\left(\sin(\frac{4 \pi}{3})-\sin(0)\right) \\ &=80 \sqrt{3}.\end{aligned}
$$



### Generated :question.difficulty/hard; authored method bank

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/1747f470795d617561561e7f2b96ef40a4ace9edb2095377edaea055516de890.png)

Evaluate $\oint_C(3^x+5x^2y)\,dx+(2^y+5xy^2)\,dy,$ where the path $C$ is shown above.

- $- \frac{3125 \sqrt{3}}{16}$

- $- \frac{3125 \sqrt{3}}{8}$

- $\frac{3125 \sqrt{3}}{16}$

- $- \frac{625 \sqrt{3}}{12}$

- $\frac{3125 \pi}{12}$


Worked solution


Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/d34d9f25c5307cf8aa107a6ab334a1698d3f3664f004d8de3cb5597e1882585f.png)

Now, since

$$
P(x,y)=3^x+5x^2y,\quad Q(x,y)=2^y+5xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=5 x^{2},\quad \frac{\partial Q}{\partial x}=5 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(3^x+5x^2y)\,dx+(2^y+5xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 y^{2}-(5 x^{2})\right)\,dA\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 5,0\le\theta\le \frac{\pi}{3}\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D - 5 x^{2} + 5 y^{2}\,dA&=\iint_\Delta 5(r^2\sin^2\theta-r^2\cos^2\theta)\,r\,dr\,d\theta \\ &=\int_{0}^{\frac{\pi}{3}}\int_{0}^{5}-5r^3(\cos^2\theta-\sin^2\theta)\,dr\,d\theta \\ &=-5\int_{0}^{\frac{\pi}{3}}\cos(2\theta)\int_{0}^{5}r^3\,dr\,d\theta \\ &=-5\int_{0}^{\frac{\pi}{3}}\cos(2\theta)\left[\frac{r^4}{4}\right]_{0}^{5}\,d\theta \\ &=-\frac{3125}{4}\int_{0}^{\frac{\pi}{3}}\cos(2\theta)\,d\theta \\ &=-\frac{3125}{4}\left[\frac{\sin(2\theta)}{2}\right]_{0}^{\frac{\pi}{3}} \\ &=-\frac{3125}{8}\left(\sin(\frac{2 \pi}{3})-\sin(0)\right) \\ &=- \frac{3125 \sqrt{3}}{16}.\end{aligned}
$$



## Original q-126755

Use Green's theorem to evaluate ${∮}_{C}F\cdot dr,$ where $F(x,y)=⟨{4}^{x}-{y}^{3}+2,\,\frac{2}{{y}^{2}+1}+{x}^{3}⟩$ and $C$ is the circle ${x}^{2}+{y}^{2}=2,$ oriented counterclockwise.

Source bank: $\frac{\pi }{3}$, $3\pi $, $6\pi $, $\frac{3\pi }{2}$, $\frac{\pi }{6}$

First, notice that we can rewrite our integral as 

$$
{∮}_{C}F\cdot dr={∮}_{C}({4}^{x}-{y}^{3}+2)\,dx+(\frac{2}{{y}^{2}+1}+{x}^{3})\,dy.
$$

Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](images/c8/c8ebdae5c3fb2c2ca7b318f32a357589d73bbe0d6471877cbf8babd813edd395.png)

Now, since 

$$
P(x,y)={4}^{x}-{y}^{3}+2,\,Q(x,y)=\frac{2}{{y}^{2}+1}+{x}^{3},
$$

 we have that 

$$
\begin{aligned}\frac{∂P}{∂y}=-3{y}^{2},\,\frac{∂Q}{∂x}=3{x}^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}{∮}_{C}({4}^{x}-{y}^{3}+2)\,dx+(\frac{2}{{y}^{2}+1}+{x}^{3})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & ={∬}_{D}(3{x}^{2}-(-3{y}^{2}))\,\text{d}A \\  & ={∬}_{D}3({x}^{2}+{y}^{2})\,\text{d}A.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
Δ={(r,\theta )\,:\,0\le r\le \sqrt{2},\,0\le \theta \le 2\pi }.
$$

The change of variables formula for plane polar coordinates states that

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}{∬}_{D}3({x}^{2}+{y}^{2})\,\text{d}A & ={∬}_{Δ}3({r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta )\,r\,\text{d}r\text{d}\theta  \\  & =3{\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{2}}{r}^{3}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & =3{\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{2}}{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & =3{\int }_{0}^{2\pi }[\frac{{r}^{4}}{4}]_{0}^{\sqrt{2}}\,\text{d}\theta  \\  & =3{\int }_{0}^{2\pi }\,\text{d}\theta  \\  & =3[\theta ]_{0}^{2\pi } \\  & =3(2\pi -0) \\  & =6\pi .\end{aligned}
$$

### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle 4^x-y^3+2,\frac{2}{y^2+1}+x^3\rangle$ and $C$ is the circle $x^2+y^2=2,$ oriented counterclockwise.

- $4 \sqrt{2} \pi$

- $- 6 \pi$

- $6 \pi$

- $3 \pi$

- $24 \pi$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(4^x-y^3+2)\,dx+(\frac{2}{y^2+1}+x^3)\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/c803dd5de2de64486bb24816426a08b47face5ddc1c156a1dd6068471cc068ce.png)

Now, since

$$
P(x,y)=4^x-y^3+2,\quad Q(x,y)=\frac{2}{y^2+1}+x^3,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 3 y^{2},\quad \frac{\partial Q}{\partial x}=3 x^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(4^x-y^3+2)\,dx+(\frac{2}{y^2+1}+x^3)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(3 x^{2}-(- 3 y^{2})\right)\,dA \\ &=\iint_D 3(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le \sqrt{2},0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 3(x^2+y^2)\,dA&=\iint_\Delta 3(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=3\int_{0}^{2 \pi}\int_{0}^{\sqrt{2}}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=3\int_{0}^{2 \pi}\int_{0}^{\sqrt{2}}r^3\,dr\,d\theta \\ &=3\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{\sqrt{2}}\,d\theta \\ &=3\int_{0}^{2 \pi}\left(1-0\right)\,d\theta \\ &=3\int_{0}^{2 \pi}\,d\theta \\ &=3[\theta]_{0}^{2 \pi} \\ &=3\left(2 \pi-0\right) \\ &=6 \pi.\end{aligned}
$$



### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle 4^x-\frac{5}{3}y^3+2,\frac{2}{y^2+1}+\frac{5}{3}x^3\rangle$ and $C$ is the circle $x^2+y^2=9,$ oriented counterclockwise.

- $\frac{405 \pi}{2}$

- $90 \pi$

- $- \frac{405 \pi}{2}$

- $810 \pi$

- $\frac{405 \pi}{4}$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(4^x-\frac{5}{3}y^3+2)\,dx+(\frac{2}{y^2+1}+\frac{5}{3}x^3)\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/6dbf71fec3d4d1f489cebd6d8ab224425d3cd4479fb355236f579b1db5392662.png)

Now, since

$$
P(x,y)=4^x-\frac{5}{3}y^3+2,\quad Q(x,y)=\frac{2}{y^2+1}+\frac{5}{3}x^3,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 y^{2},\quad \frac{\partial Q}{\partial x}=5 x^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(4^x-\frac{5}{3}y^3+2)\,dx+(\frac{2}{y^2+1}+\frac{5}{3}x^3)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 x^{2}-(- 5 y^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 3,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{3}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{3}r^3\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{3}\,d\theta \\ &=5\int_{0}^{2 \pi}\left(\frac{81}{4}-0\right)\,d\theta \\ &=5\int_{0}^{2 \pi}\frac{81}{4}\,d\theta \\ &=\frac{405}{4}[\theta]_{0}^{2 \pi} \\ &=\frac{405}{4}\left(2 \pi-0\right) \\ &=\frac{405 \pi}{2}.\end{aligned}
$$



### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle 4^x-\frac{5}{3}y^3+2,\frac{2}{y^2+1}+\frac{5}{3}x^3\rangle$ and $C$ is the circle $x^2+y^2=4,$ oriented counterclockwise.

- $- 40 \pi$

- $40 \pi$

- $160 \pi$

- $\frac{80 \pi}{3}$

- $20 \pi$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(4^x-\frac{5}{3}y^3+2)\,dx+(\frac{2}{y^2+1}+\frac{5}{3}x^3)\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/95b347882765352377ac71e985c8c96cf10411cedd7ea3c3d3922afac3ceb594.png)

Now, since

$$
P(x,y)=4^x-\frac{5}{3}y^3+2,\quad Q(x,y)=\frac{2}{y^2+1}+\frac{5}{3}x^3,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 y^{2},\quad \frac{\partial Q}{\partial x}=5 x^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(4^x-\frac{5}{3}y^3+2)\,dx+(\frac{2}{y^2+1}+\frac{5}{3}x^3)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 x^{2}-(- 5 y^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 2,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{2}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{2}r^3\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{2}\,d\theta \\ &=5\int_{0}^{2 \pi}\left(4-0\right)\,d\theta \\ &=5\int_{0}^{2 \pi}4\,d\theta \\ &=20[\theta]_{0}^{2 \pi} \\ &=20\left(2 \pi-0\right) \\ &=40 \pi.\end{aligned}
$$



### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle 4^x-\frac{5}{3}y^3+2,\frac{2}{y^2+1}+\frac{5}{3}x^3\rangle$ and $C$ is the circle $x^2+y^2=9,$ oriented counterclockwise.

- $\frac{405 \pi}{2}$

- $90 \pi$

- $- \frac{405 \pi}{2}$

- $810 \pi$

- $\frac{405 \pi}{4}$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(4^x-\frac{5}{3}y^3+2)\,dx+(\frac{2}{y^2+1}+\frac{5}{3}x^3)\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/6dbf71fec3d4d1f489cebd6d8ab224425d3cd4479fb355236f579b1db5392662.png)

Now, since

$$
P(x,y)=4^x-\frac{5}{3}y^3+2,\quad Q(x,y)=\frac{2}{y^2+1}+\frac{5}{3}x^3,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 y^{2},\quad \frac{\partial Q}{\partial x}=5 x^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(4^x-\frac{5}{3}y^3+2)\,dx+(\frac{2}{y^2+1}+\frac{5}{3}x^3)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 x^{2}-(- 5 y^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 3,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{3}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{3}r^3\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{3}\,d\theta \\ &=5\int_{0}^{2 \pi}\left(\frac{81}{4}-0\right)\,d\theta \\ &=5\int_{0}^{2 \pi}\frac{81}{4}\,d\theta \\ &=\frac{405}{4}[\theta]_{0}^{2 \pi} \\ &=\frac{405}{4}\left(2 \pi-0\right) \\ &=\frac{405 \pi}{2}.\end{aligned}
$$



## Original q-126756

![](images/d6/d675e8d06f2037531a2eec3a7e48374bb0d2e5cb59adfee0cbee5ce3a23add67.png)

Evaluate ${∮}_{C}({e}^{x}-2{x}^{2}y)dx+({e}^{y}+2x{y}^{2})\,dy,$ where the path $C$ is shown above.

Source bank: $\frac{9\pi }{4}$, $\frac{81\pi }{4}$, $\frac{27\pi }{4}$, $\frac{3\pi }{2}$, $\frac{27\pi }{2}$

Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](images/96/96998e4a17d20459622486970518a677309b23fd936c993d8c97dcf0d65a9a29.png)

 

Now, since 

$$
P(x,y)={e}^{x}-2{x}^{2}y,\,Q(x,y)={e}^{y}+2x{y}^{2},
$$

 we have that 

$$
\begin{aligned}\frac{∂P}{∂y}=-2{x}^{2},\,\frac{∂Q}{∂x}=2{y}^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}{∮}_{C}({e}^{x}-2{x}^{2}y)dx+({e}^{y}+2x{y}^{2})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & ={∬}_{D}(2{y}^{2}-(-2{x}^{2}))\,\text{d}A \\  & ={∬}_{D}2({y}^{2}+{x}^{2})\,\text{d}A\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
Δ={(r,\theta )\,:\,0\le r\le 3,\,\frac{\pi }{2}\le \theta \le \pi }.
$$

The change of variables formula for plane polar coordinates states that

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}{∬}_{D}2({y}^{2}+{x}^{2})\,\text{d}A & ={∬}_{Δ}2({r}^{2}{sin}^{2}⁡\theta +{r}^{2}{cos}^{2}⁡\theta )\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{\pi /2}^{\pi }{\int }_{0}^{3}2{r}^{3}({sin}^{2}⁡\theta +{cos}^{2}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{\pi /2}^{\pi }{\int }_{0}^{3}2{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{\pi /2}^{\pi }{[\frac{{r}^{4}}{2}]}_{0}^{3}\,\text{d}\theta  \\  & ={\int }_{\pi /2}^{\pi }\frac{81}{2}\,\text{d}\theta  \\  & =\frac{81}{2}[\theta ]_{\pi /2}^{\pi } \\  & =\frac{81}{2}\cdot \frac{\pi }{2} \\  & =\frac{81\pi }{4}.\end{aligned}
$$

### Generated :question.difficulty/hard; authored method bank

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/3c109ac0ba8fd93a4208ac13b9fecfa1ee15ce4d1d20a1840b5ac69f962885bd.png)

Evaluate $\oint_C(e^x-2x^2y)\,dx+(e^y+2xy^2)\,dy,$ where the path $C$ is shown above.

- $9 \pi$

- $- \frac{81 \pi}{4}$

- $\frac{81 \pi}{4}$

- $\frac{81 \pi}{8}$

- $81 \pi$


Worked solution


Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/b40fe8900016a3cc674ef504614aa10986a23cddf0cee94d2183b059037971a4.png)

Now, since

$$
P(x,y)=e^x-2x^2y,\quad Q(x,y)=e^y+2xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 2 x^{2},\quad \frac{\partial Q}{\partial x}=2 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(e^x-2x^2y)\,dx+(e^y+2xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(2 y^{2}-(- 2 x^{2})\right)\,dA \\ &=\iint_D 2(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 3,\frac{\pi}{2}\le\theta\le \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 2(x^2+y^2)\,dA&=\iint_\Delta 2(r^2(\sin^2\theta+\cos^2\theta))\,r\,dr\,d\theta \\ &=\int_{\frac{\pi}{2}}^{\pi}\int_{0}^{3}2r^3(\sin^2\theta+\cos^2\theta)\,dr\,d\theta \\ &=\int_{\frac{\pi}{2}}^{\pi}\int_{0}^{3}2r^3\,dr\,d\theta \\ &=\int_{\frac{\pi}{2}}^{\pi}\left[2r^4/4\right]_{0}^{3}\,d\theta \\ &=\int_{\frac{\pi}{2}}^{\pi}\left(\frac{81}{2}-0\right)\,d\theta \\ &=\int_{\frac{\pi}{2}}^{\pi}\frac{81}{2}\,d\theta \\ &=\frac{81}{2}[\theta]_{\frac{\pi}{2}}^{\pi} \\ &=\frac{81}{2}\left(\pi-\frac{\pi}{2}\right) \\ &=\frac{81 \pi}{4}.\end{aligned}
$$



### Generated :question.difficulty/hard; authored method bank

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/b9bc3a78e0a9d464048f9606769b9fe52de1d0526e24467473bbcdc5b659e7bd.png)

Evaluate $\oint_C(e^x-5x^2y)\,dx+(e^y+5xy^2)\,dy,$ where the path $C$ is shown above.

- $\frac{3125 \pi}{8}$

- $\frac{625 \pi}{6}$

- $- \frac{3125 \pi}{8}$

- $\frac{3125 \pi}{2}$

- $\frac{3125 \pi}{16}$


Worked solution


Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/ee9b83b1e98ecce68485aa48e6984e89c61e00f1e0edc133871ca8df9d23d74b.png)

Now, since

$$
P(x,y)=e^x-5x^2y,\quad Q(x,y)=e^y+5xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 x^{2},\quad \frac{\partial Q}{\partial x}=5 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(e^x-5x^2y)\,dx+(e^y+5xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 y^{2}-(- 5 x^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 5,\frac{\pi}{2}\le\theta\le \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\sin^2\theta+\cos^2\theta))\,r\,dr\,d\theta \\ &=\int_{\frac{\pi}{2}}^{\pi}\int_{0}^{5}5r^3(\sin^2\theta+\cos^2\theta)\,dr\,d\theta \\ &=\int_{\frac{\pi}{2}}^{\pi}\int_{0}^{5}5r^3\,dr\,d\theta \\ &=\int_{\frac{\pi}{2}}^{\pi}\left[5r^4/4\right]_{0}^{5}\,d\theta \\ &=\int_{\frac{\pi}{2}}^{\pi}\left(\frac{3125}{4}-0\right)\,d\theta \\ &=\int_{\frac{\pi}{2}}^{\pi}\frac{3125}{4}\,d\theta \\ &=\frac{3125}{4}[\theta]_{\frac{\pi}{2}}^{\pi} \\ &=\frac{3125}{4}\left(\pi-\frac{\pi}{2}\right) \\ &=\frac{3125 \pi}{8}.\end{aligned}
$$



### Generated :question.difficulty/hard; authored method bank

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/fd97727ddcec1205d2fff0bf7cc1d6153dca43f639e30b98d50df7dd0af26131.png)

Evaluate $\oint_C(e^x-5x^2y)\,dx+(e^y+5xy^2)\,dy,$ where the path $C$ is shown above.

- $- 320 \pi$

- $320 \pi$

- $1280 \pi$

- $\frac{320 \pi}{3}$

- $160 \pi$


Worked solution


Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/2cc6fd5f2de5bfa3e49c4307e381c84af8112028590e1dcd48f3a9ff0d20b4af.png)

Now, since

$$
P(x,y)=e^x-5x^2y,\quad Q(x,y)=e^y+5xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 x^{2},\quad \frac{\partial Q}{\partial x}=5 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(e^x-5x^2y)\,dx+(e^y+5xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 y^{2}-(- 5 x^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 4,0\le\theta\le \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\sin^2\theta+\cos^2\theta))\,r\,dr\,d\theta \\ &=\int_{0}^{\pi}\int_{0}^{4}5r^3(\sin^2\theta+\cos^2\theta)\,dr\,d\theta \\ &=\int_{0}^{\pi}\int_{0}^{4}5r^3\,dr\,d\theta \\ &=\int_{0}^{\pi}\left[5r^4/4\right]_{0}^{4}\,d\theta \\ &=\int_{0}^{\pi}\left(320-0\right)\,d\theta \\ &=\int_{0}^{\pi}320\,d\theta \\ &=320[\theta]_{0}^{\pi} \\ &=320\left(\pi-0\right) \\ &=320 \pi.\end{aligned}
$$



### Generated :question.difficulty/hard; authored method bank

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/b9bc3a78e0a9d464048f9606769b9fe52de1d0526e24467473bbcdc5b659e7bd.png)

Evaluate $\oint_C(e^x-5x^2y)\,dx+(e^y+5xy^2)\,dy,$ where the path $C$ is shown above.

- $\frac{3125 \pi}{8}$

- $\frac{625 \pi}{6}$

- $- \frac{3125 \pi}{8}$

- $\frac{3125 \pi}{2}$

- $\frac{3125 \pi}{16}$


Worked solution


Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/ee9b83b1e98ecce68485aa48e6984e89c61e00f1e0edc133871ca8df9d23d74b.png)

Now, since

$$
P(x,y)=e^x-5x^2y,\quad Q(x,y)=e^y+5xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 x^{2},\quad \frac{\partial Q}{\partial x}=5 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(e^x-5x^2y)\,dx+(e^y+5xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 y^{2}-(- 5 x^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 5,\frac{\pi}{2}\le\theta\le \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\sin^2\theta+\cos^2\theta))\,r\,dr\,d\theta \\ &=\int_{\frac{\pi}{2}}^{\pi}\int_{0}^{5}5r^3(\sin^2\theta+\cos^2\theta)\,dr\,d\theta \\ &=\int_{\frac{\pi}{2}}^{\pi}\int_{0}^{5}5r^3\,dr\,d\theta \\ &=\int_{\frac{\pi}{2}}^{\pi}\left[5r^4/4\right]_{0}^{5}\,d\theta \\ &=\int_{\frac{\pi}{2}}^{\pi}\left(\frac{3125}{4}-0\right)\,d\theta \\ &=\int_{\frac{\pi}{2}}^{\pi}\frac{3125}{4}\,d\theta \\ &=\frac{3125}{4}[\theta]_{\frac{\pi}{2}}^{\pi} \\ &=\frac{3125}{4}\left(\pi-\frac{\pi}{2}\right) \\ &=\frac{3125 \pi}{8}.\end{aligned}
$$



## Original q-126758

![](images/bc/bcdc0f59fa284c2b1f1621e7de057ef6f0e084d2eca6732fbc5eae3f74ede113.png)

Evaluate ${∮}_{C}(\sqrt{5+x}-3{x}^{2}y)dx+({e}^{-{y}^{2}}+3x{y}^{2})\,dy,$ where the path $C$ is shown above.

Source bank: $90\pi $, $15\pi $, $\frac{90\pi }{4}$, $\frac{45\pi }{2}$, $45\pi $

Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](images/62/6273034b38059d3d49b2a29c91052c290151b4a29073f1c925172dd1c4c2bf72.png)

Now, since 

$$
P(x,y)=\sqrt{5+x}-3{x}^{2}y,\,Q(x,y)={e}^{-{y}^{2}}+3x{y}^{2},
$$

we have that

$$
\begin{aligned}\frac{∂P}{∂y}=-3{x}^{2},\,\frac{∂Q}{∂x}=3{y}^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}{∮}_{C}(\sqrt{5+x}-3{x}^{2}y)dx+({e}^{-{y}^{2}}+x{y}^{2})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & ={∬}_{D}(3{y}^{2}-(-3{x}^{2}))\,\text{d}A \\  & ={∬}_{D}3({x}^{2}+{y}^{2})\,\text{d}A\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
Δ={(r,\theta )\,:\,2\le r\le 4,\,0\le \theta \le \frac{\pi }{2}}.
$$

The change of variables formula for plane polar coordinates states that

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Finally, we can calculate our double integral, as follows:  

$$
\begin{aligned}{∬}_{D}3({x}^{2}+{y}^{2})\,\text{d}A & ={∬}_{Δ}3({r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta )\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}{\int }_{2}^{4}3{r}^{3}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & =3{\int }_{0}^{\pi /2}{\int }_{2}^{4}{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & =3{\int }_{0}^{\pi /2}{[\frac{{r}^{4}}{4}]}_{2}^{4}\,\text{d}\theta  \\  & =3{\int }_{0}^{\pi /2}60\,\text{d}\theta  \\  & =180[\theta ]_{0}^{\pi /2} \\  & =180\cdot \frac{\pi }{2} \\  & =90\pi \end{aligned}
$$

### Generated :question.difficulty/hard; authored method bank

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/8a8fc41e2f16267981b9bafcb93cab4942d96bebd56d9b1534fb1a7430f602ae.png)

Evaluate $\oint_C(\sqrt{5+x}-3x^2y)\,dx+(e^{-y^2}+3xy^2)\,dy,$ where the path $C$ is shown above.

- $28 \pi$

- $- 90 \pi$

- $90 \pi$

- $45 \pi$

- $360 \pi$


Worked solution


Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/e77b677fd2c8f255473266982ba79ca9cfe27e72af2f17e7bb2304c5bf87ac57.png)

Now, since

$$
P(x,y)=\sqrt{5+x}-3x^2y,\quad Q(x,y)=e^{-y^2}+3xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 3 x^{2},\quad \frac{\partial Q}{\partial x}=3 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(\sqrt{5+x}-3x^2y)\,dx+(e^{-y^2}+3xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(3 y^{2}-(- 3 x^{2})\right)\,dA \\ &=\iint_D 3(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):2\le r\le 4,0\le\theta\le \frac{\pi}{2}\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 3(x^2+y^2)\,dA&=\iint_\Delta 3(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=3\int_{0}^{\frac{\pi}{2}}\int_{2}^{4}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=3\int_{0}^{\frac{\pi}{2}}\int_{2}^{4}r^3\,dr\,d\theta \\ &=3\int_{0}^{\frac{\pi}{2}}\left[\frac{r^4}{4}\right]_{2}^{4}\,d\theta \\ &=3\int_{0}^{\frac{\pi}{2}}\left(64-4\right)\,d\theta \\ &=3\int_{0}^{\frac{\pi}{2}}60\,d\theta \\ &=180[\theta]_{0}^{\frac{\pi}{2}} \\ &=180\left(\frac{\pi}{2}-0\right) \\ &=90 \pi.\end{aligned}
$$



### Generated :question.difficulty/hard; authored method bank

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/79c519766e01280e911a12705947808ccad86fbc8ea3fa6fd373a7fcf772f5ae.png)

Evaluate $\oint_C(\sqrt{5+x}-5x^2y)\,dx+(e^{-y^2}+5xy^2)\,dy,$ where the path $C$ is shown above.

- $340 \pi$

- $\frac{245 \pi}{3}$

- $- 340 \pi$

- $1360 \pi$

- $170 \pi$


Worked solution


Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/b165ab302b80b647a394bbbda221d17a5c80900c1dcadb3a932fae290917bd93.png)

Now, since

$$
P(x,y)=\sqrt{5+x}-5x^2y,\quad Q(x,y)=e^{-y^2}+5xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 x^{2},\quad \frac{\partial Q}{\partial x}=5 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(\sqrt{5+x}-5x^2y)\,dx+(e^{-y^2}+5xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 y^{2}-(- 5 x^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):3\le r\le 5,0\le\theta\le \frac{\pi}{2}\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\int_{3}^{5}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\int_{3}^{5}r^3\,dr\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\left[\frac{r^4}{4}\right]_{3}^{5}\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\left(\frac{625}{4}-\frac{81}{4}\right)\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}136\,d\theta \\ &=680[\theta]_{0}^{\frac{\pi}{2}} \\ &=680\left(\frac{\pi}{2}-0\right) \\ &=340 \pi.\end{aligned}
$$



### Generated :question.difficulty/hard; authored method bank

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/24d5a57dd4699737d76153687ce0fa01247423cd073b6219306cff827b5b49aa.png)

Evaluate $\oint_C(\sqrt{5+x}-5x^2y)\,dx+(e^{-y^2}+5xy^2)\,dy,$ where the path $C$ is shown above.

- $- \frac{875 \pi}{8}$

- $\frac{875 \pi}{8}$

- $\frac{875 \pi}{2}$

- $\frac{185 \pi}{6}$

- $\frac{875 \pi}{16}$


Worked solution


Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/31c31c52b5255802c8ba1b53b57c81b49b01c7695aa09e83c3491c6d75d03ef1.png)

Now, since

$$
P(x,y)=\sqrt{5+x}-5x^2y,\quad Q(x,y)=e^{-y^2}+5xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 x^{2},\quad \frac{\partial Q}{\partial x}=5 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(\sqrt{5+x}-5x^2y)\,dx+(e^{-y^2}+5xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 y^{2}-(- 5 x^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):3\le r\le 4,0\le\theta\le \frac{\pi}{2}\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\int_{3}^{4}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\int_{3}^{4}r^3\,dr\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\left[\frac{r^4}{4}\right]_{3}^{4}\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\left(64-\frac{81}{4}\right)\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\frac{175}{4}\,d\theta \\ &=\frac{875}{4}[\theta]_{0}^{\frac{\pi}{2}} \\ &=\frac{875}{4}\left(\frac{\pi}{2}-0\right) \\ &=\frac{875 \pi}{8}.\end{aligned}
$$



### Generated :question.difficulty/hard; authored method bank

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/79c519766e01280e911a12705947808ccad86fbc8ea3fa6fd373a7fcf772f5ae.png)

Evaluate $\oint_C(\sqrt{5+x}-5x^2y)\,dx+(e^{-y^2}+5xy^2)\,dy,$ where the path $C$ is shown above.

- $340 \pi$

- $\frac{245 \pi}{3}$

- $- 340 \pi$

- $1360 \pi$

- $170 \pi$


Worked solution


Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/b165ab302b80b647a394bbbda221d17a5c80900c1dcadb3a932fae290917bd93.png)

Now, since

$$
P(x,y)=\sqrt{5+x}-5x^2y,\quad Q(x,y)=e^{-y^2}+5xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 x^{2},\quad \frac{\partial Q}{\partial x}=5 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(\sqrt{5+x}-5x^2y)\,dx+(e^{-y^2}+5xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 y^{2}-(- 5 x^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):3\le r\le 5,0\le\theta\le \frac{\pi}{2}\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\int_{3}^{5}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\int_{3}^{5}r^3\,dr\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\left[\frac{r^4}{4}\right]_{3}^{5}\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}\left(\frac{625}{4}-\frac{81}{4}\right)\,d\theta \\ &=5\int_{0}^{\frac{\pi}{2}}136\,d\theta \\ &=680[\theta]_{0}^{\frac{\pi}{2}} \\ &=680\left(\frac{\pi}{2}-0\right) \\ &=340 \pi.\end{aligned}
$$



## Original q-126759

Use Green's theorem to evaluate ${∮}_{C}F\cdot dr,$ where $F(x,y)=⟨\frac{\sqrt{x+5}-{y}^{3}}{3},\frac{\sqrt{y+5}+{x}^{3}}{3}⟩$ and $C$ is the circle ${x}^{2}+{y}^{2}=4,$ oriented counterclockwise.

Source bank: $16\pi $, $8\pi $, $2\pi $, $4\pi $, $0$

First, notice that we can rewrite our integral as 

$$
{∮}_{C}F\cdot dr={∮}_{C}\frac{\sqrt{x+5}-{y}^{3}}{3}\,dx+\frac{\sqrt{y+5}+{x}^{3}}{3}\,dy.
$$

Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](images/09/09a69771617d73af6e4a1a42720223951e2e6edeb71a8df4d12aeb1bc22031aa.png)

Now, since 

$$
P(x,y)=\frac{\sqrt{x+5}-{y}^{3}}{3},\,Q(x,y)=\frac{\sqrt{y+5}+{x}^{3}}{3},
$$

 we have that

$$
\begin{aligned}\frac{∂P}{∂y}=-{y}^{2},\,\frac{∂Q}{∂x}={x}^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}{∮}_{C}\frac{\sqrt{x+5}-{y}^{3}}{3}\,dx+\frac{\sqrt{y+5}+{x}^{3}}{3}\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & ={∬}_{D}({x}^{2}-(-{y}^{2}))\,\text{d}A \\  & ={∬}_{D}({x}^{2}+{y}^{2})\,\text{d}A.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
Δ={(r,\theta )\,:\,0\le r\le 2,\,0\le \theta \le 2\pi }.
$$

The change of variables formula for plane polar coordinates states that

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}{∬}_{D}({x}^{2}+{y}^{2})\,\text{d}A & ={∬}_{Δ}({r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta )\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{2}{r}^{3}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{2}{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }[\frac{{r}^{4}}{4}]_{0}^{2}\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }4\,\text{d}\theta  \\  & =4[\theta ]_{0}^{2\pi } \\  & =4(2\pi -0) \\  & =8\pi .\end{aligned}
$$

### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle \frac{\sqrt{x+5}-y^3}{3},\frac{\sqrt{y+5}+x^3}{3}\rangle$ and $C$ is the circle $x^2+y^2=4,$ oriented counterclockwise.

- $\frac{16 \pi}{3}$

- $- 8 \pi$

- $8 \pi$

- $4 \pi$

- $32 \pi$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(\frac{\sqrt{x+5}-y^3}{3})\,dx+(\frac{\sqrt{y+5}+x^3}{3})\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/95b347882765352377ac71e985c8c96cf10411cedd7ea3c3d3922afac3ceb594.png)

Now, since

$$
P(x,y)=\frac{\sqrt{x+5}-y^3}{3},\quad Q(x,y)=\frac{\sqrt{y+5}+x^3}{3},
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- y^{2},\quad \frac{\partial Q}{\partial x}=x^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(\frac{\sqrt{x+5}-y^3}{3})\,dx+(\frac{\sqrt{y+5}+x^3}{3})\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(x^{2}-(- y^{2})\right)\,dA \\ &=\iint_D (x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 2,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D (x^2+y^2)\,dA&=\iint_\Delta (r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=\int_{0}^{2 \pi}\int_{0}^{2}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=\int_{0}^{2 \pi}\int_{0}^{2}r^3\,dr\,d\theta \\ &=\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{2}\,d\theta \\ &=\int_{0}^{2 \pi}\left(4-0\right)\,d\theta \\ &=\int_{0}^{2 \pi}4\,d\theta \\ &=4[\theta]_{0}^{2 \pi} \\ &=4\left(2 \pi-0\right) \\ &=8 \pi.\end{aligned}
$$



### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle \frac{\sqrt{x+5}-5y^3}{3},\frac{\sqrt{y+5}+5x^3}{3}\rangle$ and $C$ is the circle $x^2+y^2=9,$ oriented counterclockwise.

- $\frac{405 \pi}{2}$

- $90 \pi$

- $- \frac{405 \pi}{2}$

- $810 \pi$

- $\frac{405 \pi}{4}$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(\frac{\sqrt{x+5}-5y^3}{3})\,dx+(\frac{\sqrt{y+5}+5x^3}{3})\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/6dbf71fec3d4d1f489cebd6d8ab224425d3cd4479fb355236f579b1db5392662.png)

Now, since

$$
P(x,y)=\frac{\sqrt{x+5}-5y^3}{3},\quad Q(x,y)=\frac{\sqrt{y+5}+5x^3}{3},
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 y^{2},\quad \frac{\partial Q}{\partial x}=5 x^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(\frac{\sqrt{x+5}-5y^3}{3})\,dx+(\frac{\sqrt{y+5}+5x^3}{3})\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 x^{2}-(- 5 y^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 3,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{3}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{3}r^3\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{3}\,d\theta \\ &=5\int_{0}^{2 \pi}\left(\frac{81}{4}-0\right)\,d\theta \\ &=5\int_{0}^{2 \pi}\frac{81}{4}\,d\theta \\ &=\frac{405}{4}[\theta]_{0}^{2 \pi} \\ &=\frac{405}{4}\left(2 \pi-0\right) \\ &=\frac{405 \pi}{2}.\end{aligned}
$$



### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle \frac{\sqrt{x+5}-5y^3}{3},\frac{\sqrt{y+5}+5x^3}{3}\rangle$ and $C$ is the circle $x^2+y^2=4,$ oriented counterclockwise.

- $- 40 \pi$

- $40 \pi$

- $160 \pi$

- $\frac{80 \pi}{3}$

- $20 \pi$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(\frac{\sqrt{x+5}-5y^3}{3})\,dx+(\frac{\sqrt{y+5}+5x^3}{3})\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/95b347882765352377ac71e985c8c96cf10411cedd7ea3c3d3922afac3ceb594.png)

Now, since

$$
P(x,y)=\frac{\sqrt{x+5}-5y^3}{3},\quad Q(x,y)=\frac{\sqrt{y+5}+5x^3}{3},
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 y^{2},\quad \frac{\partial Q}{\partial x}=5 x^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(\frac{\sqrt{x+5}-5y^3}{3})\,dx+(\frac{\sqrt{y+5}+5x^3}{3})\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 x^{2}-(- 5 y^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 2,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{2}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{2}r^3\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{2}\,d\theta \\ &=5\int_{0}^{2 \pi}\left(4-0\right)\,d\theta \\ &=5\int_{0}^{2 \pi}4\,d\theta \\ &=20[\theta]_{0}^{2 \pi} \\ &=20\left(2 \pi-0\right) \\ &=40 \pi.\end{aligned}
$$



### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle \frac{\sqrt{x+5}-5y^3}{3},\frac{\sqrt{y+5}+5x^3}{3}\rangle$ and $C$ is the circle $x^2+y^2=9,$ oriented counterclockwise.

- $\frac{405 \pi}{2}$

- $90 \pi$

- $- \frac{405 \pi}{2}$

- $810 \pi$

- $\frac{405 \pi}{4}$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(\frac{\sqrt{x+5}-5y^3}{3})\,dx+(\frac{\sqrt{y+5}+5x^3}{3})\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/6dbf71fec3d4d1f489cebd6d8ab224425d3cd4479fb355236f579b1db5392662.png)

Now, since

$$
P(x,y)=\frac{\sqrt{x+5}-5y^3}{3},\quad Q(x,y)=\frac{\sqrt{y+5}+5x^3}{3},
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 y^{2},\quad \frac{\partial Q}{\partial x}=5 x^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(\frac{\sqrt{x+5}-5y^3}{3})\,dx+(\frac{\sqrt{y+5}+5x^3}{3})\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 x^{2}-(- 5 y^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 3,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{3}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{3}r^3\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{3}\,d\theta \\ &=5\int_{0}^{2 \pi}\left(\frac{81}{4}-0\right)\,d\theta \\ &=5\int_{0}^{2 \pi}\frac{81}{4}\,d\theta \\ &=\frac{405}{4}[\theta]_{0}^{2 \pi} \\ &=\frac{405}{4}\left(2 \pi-0\right) \\ &=\frac{405 \pi}{2}.\end{aligned}
$$



## Original q-126753

Use Green's theorem to evaluate ${∮}_{C}F\cdot dr,$ where $F(x,y)=⟨{sin}^{3}⁡x-{y}^{3},{y}^{4}+{x}^{3}⟩$ and $C$ is the circle ${x}^{2}+{y}^{2}=9,$ oriented counterclockwise.

Source bank: $\frac{3\text{ }\,\pi }{2}$, $\frac{729\text{ }\,\pi }{2}$, $\frac{81\text{ }\,\pi }{2}$, $\frac{243\text{ }\,\pi }{2}$, $\frac{27\text{ }\,\pi }{2}$

First, notice that we can rewrite our integral as 

$$
{∮}_{C}F\cdot dr={∮}_{C}({sin}^{3}⁡x-{y}^{3})\,dx+({y}^{4}+{x}^{3})\,dy.
$$

Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](images/e2/e218f4b6938b166aa6eacab02ce0276a4a863a0cfade8528816a54c2621b51e7.png)

Now, since 

$$
P(x,y)={sin}^{3}⁡x-{y}^{3},\,Q(x,y)={y}^{4}+{x}^{3},
$$

 we have that 

$$
\begin{aligned}\frac{∂P}{∂y}=-3{y}^{2},\,\frac{∂Q}{∂x}=3{x}^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}{∮}_{C}({sin}^{3}⁡x-{y}^{3})\,dx+({y}^{4}+{x}^{3})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & ={∬}_{D}(3{x}^{2}-(-3{y}^{2}))\,\text{d}A \\  & ={∬}_{D}3({x}^{2}+{y}^{2})\,\text{d}A.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
Δ={(r,\theta )\,:\,0\le r\le 3,\,0\le \theta \le 2\pi }.
$$

The change of variables formula for plane polar coordinates states that

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}{∬}_{D}3({x}^{2}+{y}^{2})\,\text{d}A & ={∬}_{Δ}3({r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta )\,r\,\text{d}r\text{d}\theta  \\  & =3{\int }_{0}^{2\pi }{\int }_{0}^{3}{r}^{3}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & =3{\int }_{0}^{2\pi }{\int }_{0}^{3}{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & =3{\int }_{0}^{2\pi }{[\frac{{r}^{4}}{4}]}_{0}^{3}\,\text{d}\theta  \\  & =3{\int }_{0}^{2\pi }\frac{81}{4}\,\text{d}\theta  \\  & =\frac{243}{4}[\theta ]_{0}^{2\pi } \\  & =\frac{243}{4}(2\pi -0) \\  & =\frac{243\text{ }\,\pi }{2}.\end{aligned}
$$

### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle \sin^3 x-y^3,y^4+x^3\rangle$ and $C$ is the circle $x^2+y^2=9,$ oriented counterclockwise.

- $54 \pi$

- $- \frac{243 \pi}{2}$

- $\frac{243 \pi}{2}$

- $\frac{243 \pi}{4}$

- $486 \pi$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(\sin^3 x-y^3)\,dx+(y^4+x^3)\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/6dbf71fec3d4d1f489cebd6d8ab224425d3cd4479fb355236f579b1db5392662.png)

Now, since

$$
P(x,y)=\sin^3 x-y^3,\quad Q(x,y)=y^4+x^3,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 3 y^{2},\quad \frac{\partial Q}{\partial x}=3 x^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(\sin^3 x-y^3)\,dx+(y^4+x^3)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(3 x^{2}-(- 3 y^{2})\right)\,dA \\ &=\iint_D 3(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 3,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 3(x^2+y^2)\,dA&=\iint_\Delta 3(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=3\int_{0}^{2 \pi}\int_{0}^{3}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=3\int_{0}^{2 \pi}\int_{0}^{3}r^3\,dr\,d\theta \\ &=3\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{3}\,d\theta \\ &=3\int_{0}^{2 \pi}\left(\frac{81}{4}-0\right)\,d\theta \\ &=3\int_{0}^{2 \pi}\frac{81}{4}\,d\theta \\ &=\frac{243}{4}[\theta]_{0}^{2 \pi} \\ &=\frac{243}{4}\left(2 \pi-0\right) \\ &=\frac{243 \pi}{2}.\end{aligned}
$$



### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle \sin^3 x-\frac{5}{3}y^3,y^4+\frac{5}{3}x^3\rangle$ and $C$ is the circle $x^2+y^2=9,$ oriented counterclockwise.

- $\frac{405 \pi}{2}$

- $90 \pi$

- $- \frac{405 \pi}{2}$

- $810 \pi$

- $\frac{405 \pi}{4}$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(\sin^3 x-\frac{5}{3}y^3)\,dx+(y^4+\frac{5}{3}x^3)\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/6dbf71fec3d4d1f489cebd6d8ab224425d3cd4479fb355236f579b1db5392662.png)

Now, since

$$
P(x,y)=\sin^3 x-\frac{5}{3}y^3,\quad Q(x,y)=y^4+\frac{5}{3}x^3,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 y^{2},\quad \frac{\partial Q}{\partial x}=5 x^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(\sin^3 x-\frac{5}{3}y^3)\,dx+(y^4+\frac{5}{3}x^3)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 x^{2}-(- 5 y^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 3,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{3}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{3}r^3\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{3}\,d\theta \\ &=5\int_{0}^{2 \pi}\left(\frac{81}{4}-0\right)\,d\theta \\ &=5\int_{0}^{2 \pi}\frac{81}{4}\,d\theta \\ &=\frac{405}{4}[\theta]_{0}^{2 \pi} \\ &=\frac{405}{4}\left(2 \pi-0\right) \\ &=\frac{405 \pi}{2}.\end{aligned}
$$



### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle \sin^3 x-\frac{5}{3}y^3,y^4+\frac{5}{3}x^3\rangle$ and $C$ is the circle $x^2+y^2=4,$ oriented counterclockwise.

- $- 40 \pi$

- $40 \pi$

- $160 \pi$

- $\frac{80 \pi}{3}$

- $20 \pi$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(\sin^3 x-\frac{5}{3}y^3)\,dx+(y^4+\frac{5}{3}x^3)\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/95b347882765352377ac71e985c8c96cf10411cedd7ea3c3d3922afac3ceb594.png)

Now, since

$$
P(x,y)=\sin^3 x-\frac{5}{3}y^3,\quad Q(x,y)=y^4+\frac{5}{3}x^3,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 y^{2},\quad \frac{\partial Q}{\partial x}=5 x^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(\sin^3 x-\frac{5}{3}y^3)\,dx+(y^4+\frac{5}{3}x^3)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 x^{2}-(- 5 y^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 2,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{2}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{2}r^3\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{2}\,d\theta \\ &=5\int_{0}^{2 \pi}\left(4-0\right)\,d\theta \\ &=5\int_{0}^{2 \pi}4\,d\theta \\ &=20[\theta]_{0}^{2 \pi} \\ &=20\left(2 \pi-0\right) \\ &=40 \pi.\end{aligned}
$$



### Generated :question.difficulty/moderate; authored method bank

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle \sin^3 x-\frac{5}{3}y^3,y^4+\frac{5}{3}x^3\rangle$ and $C$ is the circle $x^2+y^2=9,$ oriented counterclockwise.

- $\frac{405 \pi}{2}$

- $90 \pi$

- $- \frac{405 \pi}{2}$

- $810 \pi$

- $\frac{405 \pi}{4}$


Worked solution


First, notice that we can rewrite our integral as

$$
\oint_C F\cdot dr=\oint_C(\sin^3 x-\frac{5}{3}y^3)\,dx+(y^4+\frac{5}{3}x^3)\,dy.
$$

Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/6dbf71fec3d4d1f489cebd6d8ab224425d3cd4479fb355236f579b1db5392662.png)

Now, since

$$
P(x,y)=\sin^3 x-\frac{5}{3}y^3,\quad Q(x,y)=y^4+\frac{5}{3}x^3,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 5 y^{2},\quad \frac{\partial Q}{\partial x}=5 x^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(\sin^3 x-\frac{5}{3}y^3)\,dx+(y^4+\frac{5}{3}x^3)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(5 x^{2}-(- 5 y^{2})\right)\,dA \\ &=\iint_D 5(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 3,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 5(x^2+y^2)\,dA&=\iint_\Delta 5(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{3}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\int_{0}^{3}r^3\,dr\,d\theta \\ &=5\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{3}\,d\theta \\ &=5\int_{0}^{2 \pi}\left(\frac{81}{4}-0\right)\,d\theta \\ &=5\int_{0}^{2 \pi}\frac{81}{4}\,d\theta \\ &=\frac{405}{4}[\theta]_{0}^{2 \pi} \\ &=\frac{405}{4}\left(2 \pi-0\right) \\ &=\frac{405 \pi}{2}.\end{aligned}
$$



## Authored missing easy level

Use Green's theorem to evaluate $\oint_C(e^{-x^2}-x^2y)\,dx+(y+xy^2)\,dy,$ where $C$ is the counterclockwise boundary of the disk with polar description $0\le r\le 2,\ 0\le\theta\le2\pi$.

- $\frac{16 \pi}{3}$

- $- 8 \pi$

- $8 \pi$

- $4 \pi$

- $32 \pi$


Worked solution


Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/95b347882765352377ac71e985c8c96cf10411cedd7ea3c3d3922afac3ceb594.png)

Now, since

$$
P(x,y)=e^{-x^2}-x^2y,\quad Q(x,y)=y+xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- x^{2},\quad \frac{\partial Q}{\partial x}=y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(e^{-x^2}-x^2y)\,dx+(y+xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(y^{2}-(- x^{2})\right)\,dA \\ &=\iint_D (x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 2,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D (x^2+y^2)\,dA&=\iint_\Delta (r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=\int_{0}^{2 \pi}\int_{0}^{2}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=\int_{0}^{2 \pi}\int_{0}^{2}r^3\,dr\,d\theta \\ &=\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{2}\,d\theta \\ &=\int_{0}^{2 \pi}\left(4-0\right)\,d\theta \\ &=\int_{0}^{2 \pi}4\,d\theta \\ &=4[\theta]_{0}^{2 \pi} \\ &=4\left(2 \pi-0\right) \\ &=8 \pi.\end{aligned}
$$



Use Green's theorem to evaluate $\oint_C(e^{-x^2}-4x^2y)\,dx+(y+4xy^2)\,dy,$ where $C$ is the counterclockwise boundary of the disk with polar description $0\le r\le 3,\ 0\le\theta\le2\pi$.

- $162 \pi$

- $72 \pi$

- $- 162 \pi$

- $648 \pi$

- $81 \pi$


Worked solution


Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/6dbf71fec3d4d1f489cebd6d8ab224425d3cd4479fb355236f579b1db5392662.png)

Now, since

$$
P(x,y)=e^{-x^2}-4x^2y,\quad Q(x,y)=y+4xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 4 x^{2},\quad \frac{\partial Q}{\partial x}=4 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(e^{-x^2}-4x^2y)\,dx+(y+4xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(4 y^{2}-(- 4 x^{2})\right)\,dA \\ &=\iint_D 4(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 3,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 4(x^2+y^2)\,dA&=\iint_\Delta 4(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=4\int_{0}^{2 \pi}\int_{0}^{3}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=4\int_{0}^{2 \pi}\int_{0}^{3}r^3\,dr\,d\theta \\ &=4\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{3}\,d\theta \\ &=4\int_{0}^{2 \pi}\left(\frac{81}{4}-0\right)\,d\theta \\ &=4\int_{0}^{2 \pi}\frac{81}{4}\,d\theta \\ &=81[\theta]_{0}^{2 \pi} \\ &=81\left(2 \pi-0\right) \\ &=162 \pi.\end{aligned}
$$



Use Green's theorem to evaluate $\oint_C(e^{-x^2}-3x^2y)\,dx+(y+3xy^2)\,dy,$ where $C$ is the counterclockwise boundary of the disk with polar description $0\le r\le 5,\ 0\le\theta\le2\pi$.

- $- \frac{1875 \pi}{2}$

- $\frac{1875 \pi}{2}$

- $3750 \pi$

- $250 \pi$

- $\frac{1875 \pi}{4}$


Worked solution


Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/0a738176367aa859654ca169ac13cf5cb713ffd400f98dbb7b59ea6a095d9af5.png)

Now, since

$$
P(x,y)=e^{-x^2}-3x^2y,\quad Q(x,y)=y+3xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 3 x^{2},\quad \frac{\partial Q}{\partial x}=3 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(e^{-x^2}-3x^2y)\,dx+(y+3xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(3 y^{2}-(- 3 x^{2})\right)\,dA \\ &=\iint_D 3(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 5,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 3(x^2+y^2)\,dA&=\iint_\Delta 3(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=3\int_{0}^{2 \pi}\int_{0}^{5}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=3\int_{0}^{2 \pi}\int_{0}^{5}r^3\,dr\,d\theta \\ &=3\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{5}\,d\theta \\ &=3\int_{0}^{2 \pi}\left(\frac{625}{4}-0\right)\,d\theta \\ &=3\int_{0}^{2 \pi}\frac{625}{4}\,d\theta \\ &=\frac{1875}{4}[\theta]_{0}^{2 \pi} \\ &=\frac{1875}{4}\left(2 \pi-0\right) \\ &=\frac{1875 \pi}{2}.\end{aligned}
$$



Use Green's theorem to evaluate $\oint_C(e^{-x^2}-4x^2y)\,dx+(y+4xy^2)\,dy,$ where $C$ is the counterclockwise boundary of the disk with polar description $0\le r\le 3,\ 0\le\theta\le2\pi$.

- $162 \pi$

- $72 \pi$

- $- 162 \pi$

- $648 \pi$

- $81 \pi$


Worked solution


Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/6dbf71fec3d4d1f489cebd6d8ab224425d3cd4479fb355236f579b1db5392662.png)

Now, since

$$
P(x,y)=e^{-x^2}-4x^2y,\quad Q(x,y)=y+4xy^2,
$$

we have that

$$
\begin{aligned}\frac{\partial P}{\partial y}=- 4 x^{2},\quad \frac{\partial Q}{\partial x}=4 y^{2}.\end{aligned}
$$

Applying Green's theorem, we get

$$
\begin{aligned}\oint_C(e^{-x^2}-4x^2y)\,dx+(y+4xy^2)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA \\ &=\iint_D\left(4 y^{2}-(- 4 x^{2})\right)\,dA \\ &=\iint_D 4(x^2+y^2)\,dA.\end{aligned}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
\Delta=\{(r,\theta):0\le r\le 3,0\le\theta\le 2 \pi\}.
$$

The change of variables formula for plane polar coordinates states that

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

Finally, we can calculate our double integral, as follows:

$$
\begin{aligned}\iint_D 4(x^2+y^2)\,dA&=\iint_\Delta 4(r^2(\cos^2\theta+\sin^2\theta))\,r\,dr\,d\theta \\ &=4\int_{0}^{2 \pi}\int_{0}^{3}r^3(\cos^2\theta+\sin^2\theta)\,dr\,d\theta \\ &=4\int_{0}^{2 \pi}\int_{0}^{3}r^3\,dr\,d\theta \\ &=4\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_{0}^{3}\,d\theta \\ &=4\int_{0}^{2 \pi}\left(\frac{81}{4}-0\right)\,d\theta \\ &=4\int_{0}^{2 \pi}\frac{81}{4}\,d\theta \\ &=81[\theta]_{0}^{2 \pi} \\ &=81\left(2 \pi-0\right) \\ &=162 \pi.\end{aligned}
$$


