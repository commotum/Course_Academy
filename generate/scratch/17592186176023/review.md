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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/401ba9a619b2ce6f7fb6411ce762cc7d2a1698e42cd21e9b8dc024c13fc0c1ed.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/465106ed423d0ab62e1002dc418d6722f705ba6d8f6a491c77c940ddade38392.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/401ba9a619b2ce6f7fb6411ce762cc7d2a1698e42cd21e9b8dc024c13fc0c1ed.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/465106ed423d0ab62e1002dc418d6722f705ba6d8f6a491c77c940ddade38392.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/a8dcbbcdb26796e4dd826fd8b10658e2f37c1920d096ba3978e046fe2060ea03.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/f1fbf6afb03f43d2b4e15af6731f2dfeb3928dca41e40aabfadbacd75252b844.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/2231f0384fa357a184e34c3ee7613100725381814f36f74ca02a72e1e48ab366.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/825e72ad80ca1d0d5d037d40ea741e5157fc4e249f9f681ab69dafdaf79e866a.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/8be2361b5bdd978d2223a9dbf2f56bf8ebf62955c8928c0ac11c85cb2bebd80e.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/59b2374002adcef6430c4add960f31d5ae97b27afb039cadb79018651fe44d09.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/2231f0384fa357a184e34c3ee7613100725381814f36f74ca02a72e1e48ab366.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/825e72ad80ca1d0d5d037d40ea741e5157fc4e249f9f681ab69dafdaf79e866a.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/d22a474ff03ae7ec8a9f8bc41b00e85829d6c01adef6305bdc384b758cbdb1e9.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/465106ed423d0ab62e1002dc418d6722f705ba6d8f6a491c77c940ddade38392.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/401ba9a619b2ce6f7fb6411ce762cc7d2a1698e42cd21e9b8dc024c13fc0c1ed.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/465106ed423d0ab62e1002dc418d6722f705ba6d8f6a491c77c940ddade38392.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/cc2ffc8f7e430d156cb6160d152943f7bff4a2b20511c1359a4a808ec05ab868.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/a3f3bb483d00fe18955b2af11db3d7d84ef3be1b95e651fc5bf4162ee18c44db.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/a3f3bb483d00fe18955b2af11db3d7d84ef3be1b95e651fc5bf4162ee18c44db.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/a3f3bb483d00fe18955b2af11db3d7d84ef3be1b95e651fc5bf4162ee18c44db.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/2f073176a1c14ed9a61988196c19cbfd99de9aaad1adb55dc9fc96bb6f3037fd.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/539fd7c12e2771758acf9ed431a12eb7f8eccb8dff873623d2ed2c2d6ece8e9f.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/5a5f3bb57356cd161cc2a896d1a0c629193b92763780d08d218f33d6aeb3185b.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/3950aa69cf731adfd1a905f8e512481cf4b3836122da278b83963f33d366a534.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/b3c2049404ca26d270308d10339674d94c5db19a24c37bf3464b8c620cda3887.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/96fdfbc6b3d4eca2857d471cd273df88ce25149a3bc5ca6755ae9059cf71561e.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/5a5f3bb57356cd161cc2a896d1a0c629193b92763780d08d218f33d6aeb3185b.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/3950aa69cf731adfd1a905f8e512481cf4b3836122da278b83963f33d366a534.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/a3f3bb483d00fe18955b2af11db3d7d84ef3be1b95e651fc5bf4162ee18c44db.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/465106ed423d0ab62e1002dc418d6722f705ba6d8f6a491c77c940ddade38392.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/401ba9a619b2ce6f7fb6411ce762cc7d2a1698e42cd21e9b8dc024c13fc0c1ed.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/465106ed423d0ab62e1002dc418d6722f705ba6d8f6a491c77c940ddade38392.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/2fbb7820ab08e84742355997dab0dc6539e1f1bd85ff115eec465b700eb8c85e.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/454c47ea39d6c3157047fa7d1160bb147434f0ebf7f596bed08e519b65018718.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/be73c08d19a12cdf183a98f292d8019835fc04ca332ebe0ccc136ce47fe106d6.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/59d0f0c59efbcc153583d22fcb769eece2262d739aa914fe17acce7f8fd302c8.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/b5f38431366978d0e9b6ce0e88023ed7da7e41fe2a39bf51e03e3ede713746eb.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/797399ab8dcb6440403e34e0c4749f3a1ade76b0207a77b42608af6b3ec7d244.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/be73c08d19a12cdf183a98f292d8019835fc04ca332ebe0ccc136ce47fe106d6.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/59d0f0c59efbcc153583d22fcb769eece2262d739aa914fe17acce7f8fd302c8.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/f5493974356d6e071fc68c8f08cd83eca5c8a239e21e760d5300f5b624cfc2b4.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/4d5a8e005faa79dfc933355a57dc779a0debc33e9020c1856f4aa4e7d630eae1.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/893d3ebb5c16206ac65e35d0165b5d1efc0cf0ffb5c3baf810d8abc8dfca3ac0.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/fe56e2e17632f00bf2c230e58f7e9885c7f400eef86bd03f7b63eaf3d52a0da5.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/5df57d8bfcf1968d2b3877e48427fb3223c1928386dafa429d14bb42d4f25564.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/91ccbfa8486c46ba8d4bf6bee17b3a74e960b6d16bf91b9236428d4da429f77a.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/893d3ebb5c16206ac65e35d0165b5d1efc0cf0ffb5c3baf810d8abc8dfca3ac0.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/fe56e2e17632f00bf2c230e58f7e9885c7f400eef86bd03f7b63eaf3d52a0da5.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/401ba9a619b2ce6f7fb6411ce762cc7d2a1698e42cd21e9b8dc024c13fc0c1ed.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/465106ed423d0ab62e1002dc418d6722f705ba6d8f6a491c77c940ddade38392.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/401ba9a619b2ce6f7fb6411ce762cc7d2a1698e42cd21e9b8dc024c13fc0c1ed.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/465106ed423d0ab62e1002dc418d6722f705ba6d8f6a491c77c940ddade38392.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/465106ed423d0ab62e1002dc418d6722f705ba6d8f6a491c77c940ddade38392.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/465106ed423d0ab62e1002dc418d6722f705ba6d8f6a491c77c940ddade38392.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/401ba9a619b2ce6f7fb6411ce762cc7d2a1698e42cd21e9b8dc024c13fc0c1ed.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/465106ed423d0ab62e1002dc418d6722f705ba6d8f6a491c77c940ddade38392.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/401ba9a619b2ce6f7fb6411ce762cc7d2a1698e42cd21e9b8dc024c13fc0c1ed.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/465106ed423d0ab62e1002dc418d6722f705ba6d8f6a491c77c940ddade38392.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/d22a474ff03ae7ec8a9f8bc41b00e85829d6c01adef6305bdc384b758cbdb1e9.png)

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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186176023/plots/465106ed423d0ab62e1002dc418d6722f705ba6d8f6a491c77c940ddade38392.png)

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


