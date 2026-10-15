Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle 6 x^{2} - x y + 11,y^{2} + 1\rangle$ and $C$ is the boundary of the triangle with vertices at $(0,0),$ $(2,-1)$ and $(2,1),$ traversed counterclockwise.

- $- \frac{2}{3}$
- $\frac{8}{3}$ (correct)
- $- \frac{8}{3}$
- $- \frac{4}{3}$
- $\frac{4}{3}$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D$, then Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

The region $D$ and the curve $C$ for this case are shown below.

![](images/00/007634ca34871f05cde9d44a58fcf24b1e5fd3b8c337c68f2025fb8724eef819.png)

First, notice that we can rewrite our integral as follows:

$$
\oint_C F\cdot dr=\oint_C \left(6 x^{2} - x y + 11\right)\,dx+\left(y^{2} + 1\right)\,dy
$$

We have that $P(x,y)=6 x^{2} - x y + 11$ and $Q(x,y)=y^{2} + 1.$ Therefore,

$$
\begin{aligned}\frac{\partial P}{\partial y}&=- x,\\\frac{\partial Q}{\partial x}&=0.\end{aligned}
$$

We can express the region $D$ as a type I region as follows:

$$
D=\{(x,y):0\le x\le2,\,-x/2\le y\le x/2\}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_C \left(6 x^{2} - x y + 11\right)\,dx+\left(y^{2} + 1\right)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA\\&=\iint_D\left((0)-(- x)\right)\,dA\\&=\iint_D x\,dA\\&=\int_0^2\int_{-x/2}^{x/2} x\,dy\,dx\\&=\int_0^2 x[y]_{-x/2}^{x/2}\,dx\\&=\int_0^2 x(x)\,dx\\&=\int_0^2 x^{2}\,dx\\&=\left[\frac{x^{3}}{3}\right]_0^2\\&=\frac{8}{3}.\end{aligned}
$$

---

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle 6 x^{2} - 2 x y + 11,y^{2} + 1\rangle$ and $C$ is the boundary of the triangle with vertices at $(0,0),$ $(2,-1)$ and $(2,1),$ traversed counterclockwise.

- $- \frac{4}{3}$
- $\frac{16}{3}$ (correct)
- $- \frac{16}{3}$
- $- \frac{8}{3}$
- $\frac{8}{3}$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D$, then Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

The region $D$ and the curve $C$ for this case are shown below.

![](images/00/007634ca34871f05cde9d44a58fcf24b1e5fd3b8c337c68f2025fb8724eef819.png)

First, notice that we can rewrite our integral as follows:

$$
\oint_C F\cdot dr=\oint_C \left(6 x^{2} - 2 x y + 11\right)\,dx+\left(y^{2} + 1\right)\,dy
$$

We have that $P(x,y)=6 x^{2} - 2 x y + 11$ and $Q(x,y)=y^{2} + 1.$ Therefore,

$$
\begin{aligned}\frac{\partial P}{\partial y}&=- 2 x,\\\frac{\partial Q}{\partial x}&=0.\end{aligned}
$$

We can express the region $D$ as a type I region as follows:

$$
D=\{(x,y):0\le x\le2,\,-x/2\le y\le x/2\}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_C \left(6 x^{2} - 2 x y + 11\right)\,dx+\left(y^{2} + 1\right)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA\\&=\iint_D\left((0)-(- 2 x)\right)\,dA\\&=\iint_D 2 x\,dA\\&=\int_0^2\int_{-x/2}^{x/2} 2 x\,dy\,dx\\&=\int_0^2 2 x[y]_{-x/2}^{x/2}\,dx\\&=\int_0^2 2 x(x)\,dx\\&=\int_0^2 2 x^{2}\,dx\\&=\left[\frac{2 x^{3}}{3}\right]_0^2\\&=\frac{16}{3}.\end{aligned}
$$

---

Use Green's theorem to evaluate $\oint_C F\cdot dr,$ where $F(x,y)=\langle 6 x^{2} - 12 x y + 11,y^{2} + 1\rangle$ and $C$ is the boundary of the triangle with vertices at $(0,0),$ $(2,-1)$ and $(2,1),$ traversed counterclockwise.

- $-8$
- $32$ (correct)
- $-32$
- $-16$
- $16$

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D$, then Green's theorem states that

$$
\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.
$$

The region $D$ and the curve $C$ for this case are shown below.

![](images/00/007634ca34871f05cde9d44a58fcf24b1e5fd3b8c337c68f2025fb8724eef819.png)

First, notice that we can rewrite our integral as follows:

$$
\oint_C F\cdot dr=\oint_C \left(6 x^{2} - 12 x y + 11\right)\,dx+\left(y^{2} + 1\right)\,dy
$$

We have that $P(x,y)=6 x^{2} - 12 x y + 11$ and $Q(x,y)=y^{2} + 1.$ Therefore,

$$
\begin{aligned}\frac{\partial P}{\partial y}&=- 12 x,\\\frac{\partial Q}{\partial x}&=0.\end{aligned}
$$

We can express the region $D$ as a type I region as follows:

$$
D=\{(x,y):0\le x\le2,\,-x/2\le y\le x/2\}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_C \left(6 x^{2} - 12 x y + 11\right)\,dx+\left(y^{2} + 1\right)\,dy&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA\\&=\iint_D\left((0)-(- 12 x)\right)\,dA\\&=\iint_D 12 x\,dA\\&=\int_0^2\int_{-x/2}^{x/2} 12 x\,dy\,dx\\&=\int_0^2 12 x[y]_{-x/2}^{x/2}\,dx\\&=\int_0^2 12 x(x)\,dx\\&=\int_0^2 12 x^{2}\,dx\\&=\left[4 x^{3}\right]_0^2\\&=32.\end{aligned}
$$