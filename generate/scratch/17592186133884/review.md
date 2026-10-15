Consider the triangle $C$ in the plane with vertices $(0,0),(1,0)$ and $(1,2),$ traversed counterclockwise, and the region $D$ bounded by $C.$ Express $\oint_C\left(x y^{2}\right)\,dx+\left(2 x^{2} y\right)\,dy$ as a repeated integral.

- $\int_{0}^{1}\int_{0}^{2 x}2 x y\,\mathrm{d}y\,\mathrm{d}x$ (correct)
- $\int_{0}^{1}\int_{0}^{2 x}x^{2} y\,\mathrm{d}y\,\mathrm{d}x$
- $\int_{0}^{2}\int_{0}^{2 x}x^{2} y^{2}\,\mathrm{d}y\,\mathrm{d}x$
- $\int_{0}^{1}\int_{0}^{2 x}x y^{2}\,\mathrm{d}y\,\mathrm{d}x$
- $\int_{0}^{2}\int_{0}^{x}2 x\,\mathrm{d}y\,\mathrm{d}x$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D$, then Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

The region $D$ and the curve $C$ for this case are shown below.

![](images/2e/2e63a57e50b60d7f0c6a3ce12d164716e2cba71c6bd4c6df10460a35beba4209.png)

We have that $P(x,y)=x y^{2}$ and $Q(x,y)=2 x^{2} y.$ Therefore,

$$
\begin{aligned}\frac{\partial P}{\partial y}&=2 x y,\\\frac{\partial Q}{\partial x}&=4 x y.\end{aligned}
$$

We can express the region $D$ as a type I region as follows:

$$
D=\{(x,y):0\le x\le1,\,0\le y\le2x\}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_C\left(x y^{2}\right)\,dx+\left(2 x^{2} y\right)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA\\&=\iint_D\left((4 x y)-(2 x y)\right)\,dA\\&=\iint_D 2 x y\,dA\\&=\int_{0}^{1}\int_{0}^{2 x}2 x y\,\mathrm{d}y\,\mathrm{d}x.\end{aligned}
$$

---

Consider the triangle $C$ in the plane with vertices $(0,0),(1,0)$ and $(1,2),$ traversed counterclockwise, and the region $D$ bounded by $C.$ Express $\oint_C\left(2 x y^{2}\right)\,dx+\left(4 x^{2} y\right)\,dy$ as a repeated integral.

- $\int_{0}^{1}\int_{0}^{2 x}4 x y\,\mathrm{d}y\,\mathrm{d}x$ (correct)
- $\int_{0}^{1}\int_{0}^{2 x}2 x^{2} y\,\mathrm{d}y\,\mathrm{d}x$
- $\int_{0}^{2}\int_{0}^{2 x}2 x^{2} y^{2}\,\mathrm{d}y\,\mathrm{d}x$
- $\int_{0}^{1}\int_{0}^{2 x}2 x y^{2}\,\mathrm{d}y\,\mathrm{d}x$
- $\int_{0}^{2}\int_{0}^{x}4 x\,\mathrm{d}y\,\mathrm{d}x$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D$, then Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

The region $D$ and the curve $C$ for this case are shown below.

![](images/2e/2e63a57e50b60d7f0c6a3ce12d164716e2cba71c6bd4c6df10460a35beba4209.png)

We have that $P(x,y)=2 x y^{2}$ and $Q(x,y)=4 x^{2} y.$ Therefore,

$$
\begin{aligned}\frac{\partial P}{\partial y}&=4 x y,\\\frac{\partial Q}{\partial x}&=8 x y.\end{aligned}
$$

We can express the region $D$ as a type I region as follows:

$$
D=\{(x,y):0\le x\le1,\,0\le y\le2x\}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_C\left(2 x y^{2}\right)\,dx+\left(4 x^{2} y\right)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA\\&=\iint_D\left((8 x y)-(4 x y)\right)\,dA\\&=\iint_D 4 x y\,dA\\&=\int_{0}^{1}\int_{0}^{2 x}4 x y\,\mathrm{d}y\,\mathrm{d}x.\end{aligned}
$$

---

Consider the triangle $C$ in the plane with vertices $(0,0),(1,0)$ and $(1,2),$ traversed counterclockwise, and the region $D$ bounded by $C.$ Express $\oint_C\left(12 x y^{2}\right)\,dx+\left(24 x^{2} y\right)\,dy$ as a repeated integral.

- $\int_{0}^{1}\int_{0}^{2 x}24 x y\,\mathrm{d}y\,\mathrm{d}x$ (correct)
- $\int_{0}^{1}\int_{0}^{2 x}12 x^{2} y\,\mathrm{d}y\,\mathrm{d}x$
- $\int_{0}^{2}\int_{0}^{2 x}12 x^{2} y^{2}\,\mathrm{d}y\,\mathrm{d}x$
- $\int_{0}^{1}\int_{0}^{2 x}12 x y^{2}\,\mathrm{d}y\,\mathrm{d}x$
- $\int_{0}^{2}\int_{0}^{x}24 x\,\mathrm{d}y\,\mathrm{d}x$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D$, then Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

The region $D$ and the curve $C$ for this case are shown below.

![](images/2e/2e63a57e50b60d7f0c6a3ce12d164716e2cba71c6bd4c6df10460a35beba4209.png)

We have that $P(x,y)=12 x y^{2}$ and $Q(x,y)=24 x^{2} y.$ Therefore,

$$
\begin{aligned}\frac{\partial P}{\partial y}&=24 x y,\\\frac{\partial Q}{\partial x}&=48 x y.\end{aligned}
$$

We can express the region $D$ as a type I region as follows:

$$
D=\{(x,y):0\le x\le1,\,0\le y\le2x\}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_C\left(12 x y^{2}\right)\,dx+\left(24 x^{2} y\right)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA\\&=\iint_D\left((48 x y)-(24 x y)\right)\,dA\\&=\iint_D 24 x y\,dA\\&=\int_{0}^{1}\int_{0}^{2 x}24 x y\,\mathrm{d}y\,\mathrm{d}x.\end{aligned}
$$

---

Consider the closed curve $C,$ which is the boundary of the region enclosed by the curves $y=x^2$ and $y=x+2,$ traversed counterclockwise. Express $\oint_C F\cdot dr,$ where $F(x,y)=\langle - 2 y^{2} + \ln{\left(x + 2 \right)},x^{2} + y^{2}\rangle,$ as a repeated integral.

- $\int_{-1}^{2}\int_{x^{2}}^{x + 2}2 x + 4 y\,\mathrm{d}y\,\mathrm{d}x$ (correct)
- $\int_{-1}^{2}\int_{x + 2}^{x^{2} + x + 2}2 x + 4 y\,\mathrm{d}y\,\mathrm{d}x$
- $\int_{0}^{2}\int_{- x^{2}}^{x + 2}2 x + 4 y\,\mathrm{d}y\,\mathrm{d}x$
- $\int_{0}^{2}\int_{x^{2}}^{x + 2}2 x - 4 y\,\mathrm{d}y\,\mathrm{d}x$
- $\int_{-1}^{2}\int_{x^{2}}^{x + 2}- x + 4 y\,\mathrm{d}y\,\mathrm{d}x$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D$, then Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

The region $D$ and the curve $C$ for this case are shown below.

![](images/e3/e32b8e7d6ce80d7cedad928f9a2f7acc3c3d7f06add7909e856db27d154068d6.png)

First, notice that we can rewrite our integral as follows:

$$
\oint_C F\cdot dr=\oint_C\left(- 2 y^{2} + \ln{\left(x + 2 \right)}\right)\,dx+\left(x^{2} + y^{2}\right)\,dy
$$

We have that $P(x,y)=- 2 y^{2} + \ln{\left(x + 2 \right)}$ and $Q(x,y)=x^{2} + y^{2}.$ Therefore,

$$
\begin{aligned}\frac{\partial P}{\partial y}&=- 4 y,\\\frac{\partial Q}{\partial x}&=2 x.\end{aligned}
$$

We can express the region $D$ as a type I region as follows:

$$
D=\{(x,y):-1\le x\le2,\,x^2\le y\le x+2\}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_C\left(- 2 y^{2} + \ln{\left(x + 2 \right)}\right)\,dx+\left(x^{2} + y^{2}\right)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA\\&=\iint_D\left((2 x)-(- 4 y)\right)\,dA\\&=\iint_D 2 x + 4 y\,dA\\&=\int_{-1}^{2}\int_{x^{2}}^{x + 2}2 x + 4 y\,\mathrm{d}y\,\mathrm{d}x.\end{aligned}
$$

---

Consider the closed curve $C,$ which is the boundary of the region enclosed by the curves $y=x^2$ and $y=x+2,$ traversed counterclockwise. Express $\oint_C F\cdot dr,$ where $F(x,y)=\langle - 3 y^{2} + \ln{\left(x + 2 \right)},x^{2} + y^{2}\rangle,$ as a repeated integral.

- $\int_{-1}^{2}\int_{x^{2}}^{x + 2}2 x + 6 y\,\mathrm{d}y\,\mathrm{d}x$ (correct)
- $\int_{-1}^{2}\int_{x + 2}^{x^{2} + x + 2}2 x + 6 y\,\mathrm{d}y\,\mathrm{d}x$
- $\int_{0}^{2}\int_{- x^{2}}^{x + 2}2 x + 6 y\,\mathrm{d}y\,\mathrm{d}x$
- $\int_{0}^{2}\int_{x^{2}}^{x + 2}2 x - 6 y\,\mathrm{d}y\,\mathrm{d}x$
- $\int_{-1}^{2}\int_{x^{2}}^{x + 2}- x + 6 y\,\mathrm{d}y\,\mathrm{d}x$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D$, then Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

The region $D$ and the curve $C$ for this case are shown below.

![](images/e3/e32b8e7d6ce80d7cedad928f9a2f7acc3c3d7f06add7909e856db27d154068d6.png)

First, notice that we can rewrite our integral as follows:

$$
\oint_C F\cdot dr=\oint_C\left(- 3 y^{2} + \ln{\left(x + 2 \right)}\right)\,dx+\left(x^{2} + y^{2}\right)\,dy
$$

We have that $P(x,y)=- 3 y^{2} + \ln{\left(x + 2 \right)}$ and $Q(x,y)=x^{2} + y^{2}.$ Therefore,

$$
\begin{aligned}\frac{\partial P}{\partial y}&=- 6 y,\\\frac{\partial Q}{\partial x}&=2 x.\end{aligned}
$$

We can express the region $D$ as a type I region as follows:

$$
D=\{(x,y):-1\le x\le2,\,x^2\le y\le x+2\}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_C\left(- 3 y^{2} + \ln{\left(x + 2 \right)}\right)\,dx+\left(x^{2} + y^{2}\right)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA\\&=\iint_D\left((2 x)-(- 6 y)\right)\,dA\\&=\iint_D 2 x + 6 y\,dA\\&=\int_{-1}^{2}\int_{x^{2}}^{x + 2}2 x + 6 y\,\mathrm{d}y\,\mathrm{d}x.\end{aligned}
$$

---

Consider the closed curve $C,$ which is the boundary of the region enclosed by the curves $y=x^2$ and $y=x+2,$ traversed counterclockwise. Express $\oint_C F\cdot dr,$ where $F(x,y)=\langle - 12 y^{2} + \ln{\left(x + 2 \right)},x^{2} + y^{2}\rangle,$ as a repeated integral.

- $\int_{-1}^{2}\int_{x^{2}}^{x + 2}2 x + 24 y\,\mathrm{d}y\,\mathrm{d}x$ (correct)
- $\int_{-1}^{2}\int_{x + 2}^{x^{2} + x + 2}2 x + 24 y\,\mathrm{d}y\,\mathrm{d}x$
- $\int_{0}^{2}\int_{- x^{2}}^{x + 2}2 x + 24 y\,\mathrm{d}y\,\mathrm{d}x$
- $\int_{0}^{2}\int_{x^{2}}^{x + 2}2 x - 24 y\,\mathrm{d}y\,\mathrm{d}x$
- $\int_{-1}^{2}\int_{x^{2}}^{x + 2}- x + 24 y\,\mathrm{d}y\,\mathrm{d}x$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D$, then Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

The region $D$ and the curve $C$ for this case are shown below.

![](images/e3/e32b8e7d6ce80d7cedad928f9a2f7acc3c3d7f06add7909e856db27d154068d6.png)

First, notice that we can rewrite our integral as follows:

$$
\oint_C F\cdot dr=\oint_C\left(- 12 y^{2} + \ln{\left(x + 2 \right)}\right)\,dx+\left(x^{2} + y^{2}\right)\,dy
$$

We have that $P(x,y)=- 12 y^{2} + \ln{\left(x + 2 \right)}$ and $Q(x,y)=x^{2} + y^{2}.$ Therefore,

$$
\begin{aligned}\frac{\partial P}{\partial y}&=- 24 y,\\\frac{\partial Q}{\partial x}&=2 x.\end{aligned}
$$

We can express the region $D$ as a type I region as follows:

$$
D=\{(x,y):-1\le x\le2,\,x^2\le y\le x+2\}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_C\left(- 12 y^{2} + \ln{\left(x + 2 \right)}\right)\,dx+\left(x^{2} + y^{2}\right)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA\\&=\iint_D\left((2 x)-(- 24 y)\right)\,dA\\&=\iint_D 2 x + 24 y\,dA\\&=\int_{-1}^{2}\int_{x^{2}}^{x + 2}2 x + 24 y\,\mathrm{d}y\,\mathrm{d}x.\end{aligned}
$$