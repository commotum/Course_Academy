# Replenishment review

Current source basis 2645. Existing historical evidence remains unchanged.

All candidates are generated; source and mathematical task identities are checked separately.

## Generated variant — easy

Let $C$ be the intersection of the cylinder $x^2+y^2=9$ and the plane $z=1$. The curve $C$ is oriented counter-clockwise when viewed from above. Given that $\text{curl}\,F=\langle - x z,\,- y z,\,x + z^{2}\rangle$, use Stokes' theorem to evaluate $\oint_C F\cdot\mathrm{d}r.$

- $- 9 \pi$
- $6 \pi$
- $9 \pi$ **(correct)**
- $0$
- $36 \pi$

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

There are many surfaces whose boundary is the curve $C.$ One such surface is our graph $S$ with the equation

$$z=g(x,y)=1.$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$\begin{aligned}\frac{\partial g}{\partial x}&=\frac{\partial}{\partial x}\left(1\right)=0\\
\frac{\partial g}{\partial y}&=\frac{\partial}{\partial y}\left(1\right)=0.\end{aligned}$$

Next, we substitute the equation $z=g(x,y)$ into the expression for $\text{curl}\,F:$

$$\begin{aligned}\text{curl}\,F|_{z=g(x,y)}&=\langle - x z,\,- y z,\,x + z^{2}\rangle|_{z=1}\\
&=\langle - x,\,- y,\,x + 1\rangle\\
&=\langle - x,\,- y,\,x + 1\rangle.\end{aligned}$$

So, we have

$$\begin{aligned}\iint_S\text{curl}\,F\cdot\mathrm{d}S&=\iint_D(-P g_x-Q g_y+R)\,\mathrm{d}A\\
&=\iint_D\left(-\left(- x\right)\left(0\right)-\left(- y\right)\left(0\right)+\left(x + 1\right)\right)\,\mathrm{d}A\\
&=\iint_D\left((0)+(0)+(x + 1)\right)\,\mathrm{d}A\\
&=\iint_D\left(x + 1\right)\,\mathrm{d}A.\end{aligned}$$

where $D$ is the region enclosed by the projection of $C$ onto the $xy$-plane.
Notice that the projection of $C$ onto the $xy$-plane is the circle $x^2+y^2=9.$ Therefore, using the change of variables to polar coordinates

$$x=r\cos\theta,\quad y=r\sin\theta,\quad \mathrm{d}A=r\,\mathrm{d}r\,\mathrm{d}\theta,$$

we obtain

$$\begin{aligned}\iint_D\left(x + 1\right)\,\mathrm{d}A
&=\int_0^{3}\int_0^{2\pi}\left(r \cos{\left(\theta \right)} + 1\right)r\,\mathrm{d}\theta\,\mathrm{d}r\\
&=\int_0^{3}\int_0^{2\pi}\left(r^{2} \cos{\left(\theta \right)} + r\right)\,\mathrm{d}\theta\,\mathrm{d}r\\
&=\int_0^{3}\left[r^{2} \sin{\left(\theta \right)} + r \theta\right]_0^{2\pi}\,\mathrm{d}r\\
&=\int_0^{3}\left[\left(2 \pi r\right)-\left(0\right)\right]\,\mathrm{d}r\\
&=\int_0^{3}\left(2 \pi r\right)\,\mathrm{d}r\\
&=\left[\pi r^{2}\right]_0^{3}\\
&=\left[\left(9 \pi\right)\right]-\left[\left(0\right)\right]\\
&=9 \pi.\end{aligned}$$


## Generated variant — easy

Let $C$ be the intersection of the cylinder $x^2+y^2=9$ and the plane $z=2$. The curve $C$ is oriented counter-clockwise when viewed from above. Given that $\text{curl}\,F=\langle - x z,\,- y z,\,x + z^{2}\rangle$, use Stokes' theorem to evaluate $\oint_C F\cdot\mathrm{d}r.$

- $81 \pi$
- $0$
- $36 \pi$ **(correct)**
- $24 \pi$
- $- 36 \pi$

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

There are many surfaces whose boundary is the curve $C.$ One such surface is our graph $S$ with the equation

$$z=g(x,y)=2.$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$\begin{aligned}\frac{\partial g}{\partial x}&=\frac{\partial}{\partial x}\left(2\right)=0\\
\frac{\partial g}{\partial y}&=\frac{\partial}{\partial y}\left(2\right)=0.\end{aligned}$$

Next, we substitute the equation $z=g(x,y)$ into the expression for $\text{curl}\,F:$

$$\begin{aligned}\text{curl}\,F|_{z=g(x,y)}&=\langle - x z,\,- y z,\,x + z^{2}\rangle|_{z=2}\\
&=\langle - 2 x,\,- 2 y,\,x + 4\rangle\\
&=\langle - 2 x,\,- 2 y,\,x + 4\rangle.\end{aligned}$$

So, we have

$$\begin{aligned}\iint_S\text{curl}\,F\cdot\mathrm{d}S&=\iint_D(-P g_x-Q g_y+R)\,\mathrm{d}A\\
&=\iint_D\left(-\left(- 2 x\right)\left(0\right)-\left(- 2 y\right)\left(0\right)+\left(x + 4\right)\right)\,\mathrm{d}A\\
&=\iint_D\left((0)+(0)+(x + 4)\right)\,\mathrm{d}A\\
&=\iint_D\left(x + 4\right)\,\mathrm{d}A.\end{aligned}$$

where $D$ is the region enclosed by the projection of $C$ onto the $xy$-plane.
Notice that the projection of $C$ onto the $xy$-plane is the circle $x^2+y^2=9.$ Therefore, using the change of variables to polar coordinates

$$x=r\cos\theta,\quad y=r\sin\theta,\quad \mathrm{d}A=r\,\mathrm{d}r\,\mathrm{d}\theta,$$

we obtain

$$\begin{aligned}\iint_D\left(x + 4\right)\,\mathrm{d}A
&=\int_0^{3}\int_0^{2\pi}\left(r \cos{\left(\theta \right)} + 4\right)r\,\mathrm{d}\theta\,\mathrm{d}r\\
&=\int_0^{3}\int_0^{2\pi}\left(r^{2} \cos{\left(\theta \right)} + 4 r\right)\,\mathrm{d}\theta\,\mathrm{d}r\\
&=\int_0^{3}\left[r^{2} \sin{\left(\theta \right)} + 4 r \theta\right]_0^{2\pi}\,\mathrm{d}r\\
&=\int_0^{3}\left[\left(8 \pi r\right)-\left(0\right)\right]\,\mathrm{d}r\\
&=\int_0^{3}\left(8 \pi r\right)\,\mathrm{d}r\\
&=\left[4 \pi r^{2}\right]_0^{3}\\
&=\left[\left(36 \pi\right)\right]-\left[\left(0\right)\right]\\
&=36 \pi.\end{aligned}$$


## Generated variant — easy

Let $C$ be the intersection of the cylinder $x^2+y^2=9$ and the plane $z=3$. The curve $C$ is oriented counter-clockwise when viewed from above. Given that $\text{curl}\,F=\langle - x z,\,- y z,\,x + z^{2}\rangle$, use Stokes' theorem to evaluate $\oint_C F\cdot\mathrm{d}r.$

- $- 81 \pi$
- $144 \pi$
- $54 \pi$
- $0$
- $81 \pi$ **(correct)**

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

There are many surfaces whose boundary is the curve $C.$ One such surface is our graph $S$ with the equation

$$z=g(x,y)=3.$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$\begin{aligned}\frac{\partial g}{\partial x}&=\frac{\partial}{\partial x}\left(3\right)=0\\
\frac{\partial g}{\partial y}&=\frac{\partial}{\partial y}\left(3\right)=0.\end{aligned}$$

Next, we substitute the equation $z=g(x,y)$ into the expression for $\text{curl}\,F:$

$$\begin{aligned}\text{curl}\,F|_{z=g(x,y)}&=\langle - x z,\,- y z,\,x + z^{2}\rangle|_{z=3}\\
&=\langle - 3 x,\,- 3 y,\,x + 9\rangle\\
&=\langle - 3 x,\,- 3 y,\,x + 9\rangle.\end{aligned}$$

So, we have

$$\begin{aligned}\iint_S\text{curl}\,F\cdot\mathrm{d}S&=\iint_D(-P g_x-Q g_y+R)\,\mathrm{d}A\\
&=\iint_D\left(-\left(- 3 x\right)\left(0\right)-\left(- 3 y\right)\left(0\right)+\left(x + 9\right)\right)\,\mathrm{d}A\\
&=\iint_D\left((0)+(0)+(x + 9)\right)\,\mathrm{d}A\\
&=\iint_D\left(x + 9\right)\,\mathrm{d}A.\end{aligned}$$

where $D$ is the region enclosed by the projection of $C$ onto the $xy$-plane.
Notice that the projection of $C$ onto the $xy$-plane is the circle $x^2+y^2=9.$ Therefore, using the change of variables to polar coordinates

$$x=r\cos\theta,\quad y=r\sin\theta,\quad \mathrm{d}A=r\,\mathrm{d}r\,\mathrm{d}\theta,$$

we obtain

$$\begin{aligned}\iint_D\left(x + 9\right)\,\mathrm{d}A
&=\int_0^{3}\int_0^{2\pi}\left(r \cos{\left(\theta \right)} + 9\right)r\,\mathrm{d}\theta\,\mathrm{d}r\\
&=\int_0^{3}\int_0^{2\pi}\left(r^{2} \cos{\left(\theta \right)} + 9 r\right)\,\mathrm{d}\theta\,\mathrm{d}r\\
&=\int_0^{3}\left[r^{2} \sin{\left(\theta \right)} + 9 r \theta\right]_0^{2\pi}\,\mathrm{d}r\\
&=\int_0^{3}\left[\left(18 \pi r\right)-\left(0\right)\right]\,\mathrm{d}r\\
&=\int_0^{3}\left(18 \pi r\right)\,\mathrm{d}r\\
&=\left[9 \pi r^{2}\right]_0^{3}\\
&=\left[\left(81 \pi\right)\right]-\left[\left(0\right)\right]\\
&=81 \pi.\end{aligned}$$


## Generated variant — easy

Let $C$ be the intersection of the cylinder $x^2+y^2=9$ and the plane $z=4$. The curve $C$ is oriented counter-clockwise when viewed from above. Given that $\text{curl}\,F=\langle - x z,\,- y z,\,x + z^{2}\rangle$, use Stokes' theorem to evaluate $\oint_C F\cdot\mathrm{d}r.$

- $96 \pi$
- $144 \pi$ **(correct)**
- $0$
- $- 144 \pi$
- $225 \pi$

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

There are many surfaces whose boundary is the curve $C.$ One such surface is our graph $S$ with the equation

$$z=g(x,y)=4.$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$\begin{aligned}\frac{\partial g}{\partial x}&=\frac{\partial}{\partial x}\left(4\right)=0\\
\frac{\partial g}{\partial y}&=\frac{\partial}{\partial y}\left(4\right)=0.\end{aligned}$$

Next, we substitute the equation $z=g(x,y)$ into the expression for $\text{curl}\,F:$

$$\begin{aligned}\text{curl}\,F|_{z=g(x,y)}&=\langle - x z,\,- y z,\,x + z^{2}\rangle|_{z=4}\\
&=\langle - 4 x,\,- 4 y,\,x + 16\rangle\\
&=\langle - 4 x,\,- 4 y,\,x + 16\rangle.\end{aligned}$$

So, we have

$$\begin{aligned}\iint_S\text{curl}\,F\cdot\mathrm{d}S&=\iint_D(-P g_x-Q g_y+R)\,\mathrm{d}A\\
&=\iint_D\left(-\left(- 4 x\right)\left(0\right)-\left(- 4 y\right)\left(0\right)+\left(x + 16\right)\right)\,\mathrm{d}A\\
&=\iint_D\left((0)+(0)+(x + 16)\right)\,\mathrm{d}A\\
&=\iint_D\left(x + 16\right)\,\mathrm{d}A.\end{aligned}$$

where $D$ is the region enclosed by the projection of $C$ onto the $xy$-plane.
Notice that the projection of $C$ onto the $xy$-plane is the circle $x^2+y^2=9.$ Therefore, using the change of variables to polar coordinates

$$x=r\cos\theta,\quad y=r\sin\theta,\quad \mathrm{d}A=r\,\mathrm{d}r\,\mathrm{d}\theta,$$

we obtain

$$\begin{aligned}\iint_D\left(x + 16\right)\,\mathrm{d}A
&=\int_0^{3}\int_0^{2\pi}\left(r \cos{\left(\theta \right)} + 16\right)r\,\mathrm{d}\theta\,\mathrm{d}r\\
&=\int_0^{3}\int_0^{2\pi}\left(r^{2} \cos{\left(\theta \right)} + 16 r\right)\,\mathrm{d}\theta\,\mathrm{d}r\\
&=\int_0^{3}\left[r^{2} \sin{\left(\theta \right)} + 16 r \theta\right]_0^{2\pi}\,\mathrm{d}r\\
&=\int_0^{3}\left[\left(32 \pi r\right)-\left(0\right)\right]\,\mathrm{d}r\\
&=\int_0^{3}\left(32 \pi r\right)\,\mathrm{d}r\\
&=\left[16 \pi r^{2}\right]_0^{3}\\
&=\left[\left(144 \pi\right)\right]-\left[\left(0\right)\right]\\
&=144 \pi.\end{aligned}$$


## Generated variant — easy

Let $C$ be the intersection of the cylinder $x^2+y^2=1$ and the plane $z=3$. The curve $C$ is oriented counter-clockwise when viewed from above. Given that $\text{curl}\,F=\langle - 2 x z,\,- 2 y z,\,2 x + 2 z^{2}\rangle$, use Stokes' theorem to evaluate $\oint_C F\cdot\mathrm{d}r.$

- $36 \pi$
- $18 \pi$ **(correct)**
- $32 \pi$
- $0$
- $- 18 \pi$

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

There are many surfaces whose boundary is the curve $C.$ One such surface is our graph $S$ with the equation

$$z=g(x,y)=3.$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$\begin{aligned}\frac{\partial g}{\partial x}&=\frac{\partial}{\partial x}\left(3\right)=0\\
\frac{\partial g}{\partial y}&=\frac{\partial}{\partial y}\left(3\right)=0.\end{aligned}$$

Next, we substitute the equation $z=g(x,y)$ into the expression for $\text{curl}\,F:$

$$\begin{aligned}\text{curl}\,F|_{z=g(x,y)}&=\langle - 2 x z,\,- 2 y z,\,2 x + 2 z^{2}\rangle|_{z=3}\\
&=\langle - 6 x,\,- 6 y,\,2 x + 18\rangle\\
&=\langle - 6 x,\,- 6 y,\,2 x + 18\rangle.\end{aligned}$$

So, we have

$$\begin{aligned}\iint_S\text{curl}\,F\cdot\mathrm{d}S&=\iint_D(-P g_x-Q g_y+R)\,\mathrm{d}A\\
&=\iint_D\left(-\left(- 6 x\right)\left(0\right)-\left(- 6 y\right)\left(0\right)+\left(2 x + 18\right)\right)\,\mathrm{d}A\\
&=\iint_D\left((0)+(0)+(2 x + 18)\right)\,\mathrm{d}A\\
&=\iint_D\left(2 x + 18\right)\,\mathrm{d}A.\end{aligned}$$

where $D$ is the region enclosed by the projection of $C$ onto the $xy$-plane.
Notice that the projection of $C$ onto the $xy$-plane is the circle $x^2+y^2=1.$ Therefore, using the change of variables to polar coordinates

$$x=r\cos\theta,\quad y=r\sin\theta,\quad \mathrm{d}A=r\,\mathrm{d}r\,\mathrm{d}\theta,$$

we obtain

$$\begin{aligned}\iint_D\left(2 x + 18\right)\,\mathrm{d}A
&=\int_0^{1}\int_0^{2\pi}\left(2 r \cos{\left(\theta \right)} + 18\right)r\,\mathrm{d}\theta\,\mathrm{d}r\\
&=\int_0^{1}\int_0^{2\pi}\left(2 r^{2} \cos{\left(\theta \right)} + 18 r\right)\,\mathrm{d}\theta\,\mathrm{d}r\\
&=\int_0^{1}\left[2 r^{2} \sin{\left(\theta \right)} + 18 r \theta\right]_0^{2\pi}\,\mathrm{d}r\\
&=\int_0^{1}\left[\left(36 \pi r\right)-\left(0\right)\right]\,\mathrm{d}r\\
&=\int_0^{1}\left(36 \pi r\right)\,\mathrm{d}r\\
&=\left[18 \pi r^{2}\right]_0^{1}\\
&=\left[\left(18 \pi\right)\right]-\left[\left(0\right)\right]\\
&=18 \pi.\end{aligned}$$


## Generated variant — moderate

Let $C$ be the intersection of the surface $z=- x^{2} - y^{2} + 4$ and the vertical column over $D$, where $0\leq x\leq 2$ and $0\leq y\leq 2 - x$. The curve $C$ is oriented counter-clockwise when viewed from above. Given that $\text{curl}\,F=\langle - 4 z,\,0,\,0\rangle$, use Stokes' theorem to write down the integral that gives the circulation along $C.$

- $\int_{0}^{2}\int_{0}^{2}\left(- 8 x^{2} + 8 y^{2} + 16\right)\,\mathrm{d}y\,\mathrm{d}x$
- $\int_{0}^{2}\int_{0}^{2 - x}\left(- 8 x^{2} + 8 y^{2} + 16\right)\,\mathrm{d}y\,\mathrm{d}x$
- $\int_{0}^{2}\int_{0}^{2 - x}\left(8 x \left(x^{2} + y^{2} - 4\right)\right)\,\mathrm{d}y\,\mathrm{d}x$ **(correct)**
- $\int_{0}^{2}\int_{0}^{2}\left(8 x \left(x^{2} + y^{2} - 4\right)\right)\,\mathrm{d}y\,\mathrm{d}x$
- $\int_{0}^{2}\int_{0}^{x}\left(- 8 x^{2} + 8 y^{2} + 16\right)\,\mathrm{d}y\,\mathrm{d}x$

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

There are many surfaces whose boundary is the curve $C.$ One such surface is our graph $S$ with the equation

$$z=g(x,y)=- x^{2} - y^{2} + 4.$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$\begin{aligned}\frac{\partial g}{\partial x}&=\frac{\partial}{\partial x}\left(- x^{2} - y^{2} + 4\right)=- 2 x\\
\frac{\partial g}{\partial y}&=\frac{\partial}{\partial y}\left(- x^{2} - y^{2} + 4\right)=- 2 y.\end{aligned}$$

Next, we substitute the equation $z=g(x,y)$ into the expression for $\text{curl}\,F:$

$$\begin{aligned}\text{curl}\,F|_{z=g(x,y)}&=\langle - 4 z,\,0,\,0\rangle|_{z=- x^{2} - y^{2} + 4}\\
&=\langle 4 x^{2} + 4 y^{2} - 16,\,0,\,0\rangle\\
&=\langle 4 x^{2} + 4 y^{2} - 16,\,0,\,0\rangle.\end{aligned}$$

So, we have

$$\begin{aligned}\iint_S\text{curl}\,F\cdot\mathrm{d}S&=\iint_D(-P g_x-Q g_y+R)\,\mathrm{d}A\\
&=\iint_D\left(-\left(4 x^{2} + 4 y^{2} - 16\right)\left(- 2 x\right)-\left(0\right)\left(- 2 y\right)+\left(0\right)\right)\,\mathrm{d}A\\
&=\iint_D\left((- 2 x \left(- 4 x^{2} - 4 y^{2} + 16\right))+(0)+(0)\right)\,\mathrm{d}A\\
&=\iint_D\left(8 x \left(x^{2} + y^{2} - 4\right)\right)\,\mathrm{d}A.\end{aligned}$$

where $D$ is the region enclosed by the projection of $C$ onto the $xy$-plane.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133927/assets/region-1abc4b412853ff2ef7.png)

Therefore, we obtain

$$\int_{0}^{2}\int_{0}^{2 - x}\left(8 x \left(x^{2} + y^{2} - 4\right)\right)\,\mathrm{d}y\,\mathrm{d}x.$$


## Generated variant — moderate

Let $C$ be the intersection of the surface $z=- x - y + 3$ and the vertical column over $D$, where $0\leq x\leq 2$ and $0\leq y\leq 2$. The curve $C$ is oriented counter-clockwise when viewed from above. Given that $\text{curl}\,F=\langle 4 x y,\,- 2 y^{2} + 4 z,\,4 y\rangle$, use Stokes' theorem to write down the integral that gives the circulation along $C.$ The circulation is $\int_0^{2}\int_0^{2}$ {{field-1}} $\mathrm{d}y\,\mathrm{d}x$.

- $4 x y - 4 x - 2 y^{2} + 12$ **(correct)**

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

There are many surfaces whose boundary is the curve $C.$ One such surface is our graph $S$ with the equation

$$z=g(x,y)=- x - y + 3.$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$\begin{aligned}\frac{\partial g}{\partial x}&=\frac{\partial}{\partial x}\left(- x - y + 3\right)=-1\\
\frac{\partial g}{\partial y}&=\frac{\partial}{\partial y}\left(- x - y + 3\right)=-1.\end{aligned}$$

Next, we substitute the equation $z=g(x,y)$ into the expression for $\text{curl}\,F:$

$$\begin{aligned}\text{curl}\,F|_{z=g(x,y)}&=\langle 4 x y,\,- 2 y^{2} + 4 z,\,4 y\rangle|_{z=- x - y + 3}\\
&=\langle 4 x y,\,- 4 x - 2 y^{2} - 4 y + 12,\,4 y\rangle\\
&=\langle 4 x y,\,- 4 x - 2 y^{2} - 4 y + 12,\,4 y\rangle.\end{aligned}$$

So, we have

$$\begin{aligned}\iint_S\text{curl}\,F\cdot\mathrm{d}S&=\iint_D(-P g_x-Q g_y+R)\,\mathrm{d}A\\
&=\iint_D\left(-\left(4 x y\right)\left(-1\right)-\left(- 4 x - 2 y^{2} - 4 y + 12\right)\left(-1\right)+\left(4 y\right)\right)\,\mathrm{d}A\\
&=\iint_D\left((4 x y)+(- 4 x - 2 y^{2} - 4 y + 12)+(4 y)\right)\,\mathrm{d}A\\
&=\iint_D\left(4 x y - 4 x - 2 y^{2} + 12\right)\,\mathrm{d}A.\end{aligned}$$

where $D$ is the region enclosed by the projection of $C$ onto the $xy$-plane.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133927/assets/region-581d84c86078820a64.png)

Therefore, we obtain

$$\int_{0}^{2}\int_{0}^{2}\left(4 x y - 4 x - 2 y^{2} + 12\right)\,\mathrm{d}y\,\mathrm{d}x.$$


## Generated variant — moderate

Let $C$ be the intersection of the surface $z=x^{2} + 2 y^{2} + 2$ and the vertical column over $D$, where $0\leq x\leq 2$ and $x - 2\leq y\leq 0$. The curve $C$ is oriented counter-clockwise when viewed from above. Given that $\text{curl}\,F=\langle 3 y,\,- 3 x,\,3\rangle$, use Stokes' theorem to write down the integral that gives the circulation along $C.$

- $$
\begin{aligned}\int_{0}^{2}\int_{0}^{x - 2}\left(- 6 x y + 3\right)\,\mathrm{d}y\,\mathrm{d}x\end{aligned}
$$
- $$
\begin{aligned}\int_{0}^{2}\int_{0}^{x - 2}\left(6 x y + 3\right)\,\mathrm{d}y\,\mathrm{d}x\end{aligned}
$$
- $$
\begin{aligned}\int_{0}^{2}\int_{x - 2}^{0}\left(6 x y + 3\right)\,\mathrm{d}y\,\mathrm{d}x\end{aligned}
$$ **(correct)**
- $$
\begin{aligned}\int_{0}^{2}\int_{0}^{2 - x}\left(3 x^{2} + 6 y^{2}\right)\,\mathrm{d}y\,\mathrm{d}x\end{aligned}
$$
- $$
\begin{aligned}\int_{0}^{2}\int_{x - 2}^{0}\left(- 6 x y + 3\right)\,\mathrm{d}y\,\mathrm{d}x\end{aligned}
$$

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

There are many surfaces whose boundary is the curve $C.$ One such surface is our graph $S$ with the equation

$$z=g(x,y)=x^{2} + 2 y^{2} + 2.$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$\begin{aligned}\frac{\partial g}{\partial x}&=\frac{\partial}{\partial x}\left(x^{2} + 2 y^{2} + 2\right)=2 x\\
\frac{\partial g}{\partial y}&=\frac{\partial}{\partial y}\left(x^{2} + 2 y^{2} + 2\right)=4 y.\end{aligned}$$

Next, we substitute the equation $z=g(x,y)$ into the expression for $\text{curl}\,F:$

$$\begin{aligned}\text{curl}\,F|_{z=g(x,y)}&=\langle 3 y,\,- 3 x,\,3\rangle|_{z=x^{2} + 2 y^{2} + 2}\\
&=\langle 3 y,\,- 3 x,\,3\rangle\\
&=\langle 3 y,\,- 3 x,\,3\rangle.\end{aligned}$$

So, we have

$$\begin{aligned}\iint_S\text{curl}\,F\cdot\mathrm{d}S&=\iint_D(-P g_x-Q g_y+R)\,\mathrm{d}A\\
&=\iint_D\left(-\left(3 y\right)\left(2 x\right)-\left(- 3 x\right)\left(4 y\right)+\left(3\right)\right)\,\mathrm{d}A\\
&=\iint_D\left((- 6 x y)+(12 x y)+(3)\right)\,\mathrm{d}A\\
&=\iint_D\left(6 x y + 3\right)\,\mathrm{d}A.\end{aligned}$$

where $D$ is the region enclosed by the projection of $C$ onto the $xy$-plane.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133927/assets/region-191db9dfb54abe4590.png)

Therefore, we obtain

$$\int_{0}^{2}\int_{x - 2}^{0}\left(6 x y + 3\right)\,\mathrm{d}y\,\mathrm{d}x.$$


## Generated variant — moderate

Let $C$ be the intersection of the surface $z=\frac{3}{x^{2} + y^{2} + 1}$ and the vertical column over $D$, where $-2\leq x\leq 2$ and $-2\leq y\leq 2$. The curve $C$ is oriented counter-clockwise when viewed from above. Given that $\text{curl}\,F=\langle 2 x,\,2 y,\,- 4 z\rangle$, use Stokes' theorem to write down the integral that gives the circulation along $C.$

- $$
\begin{aligned}\int_{-2}^{2}\int_{-2}^{2}\left(- \frac{6 y^{2}}{\left(x^{2} + y^{2} + 1\right)^{2}}\right)\,\mathrm{d}y\,\mathrm{d}x\end{aligned}
$$
- $$
\begin{aligned}\int_{-2}^{2}\int_{-2}^{2}\left(- \frac{24}{\left(x^{2} + y^{2} + 1\right)^{2}}\right)\,\mathrm{d}y\,\mathrm{d}x\end{aligned}
$$
- $$
\begin{aligned}\int_{-2}^{2}\int_{-2}^{2}\left(\frac{6 x^{2}}{\left(x^{2} + y^{2} + 1\right)^{2}}\right)\,\mathrm{d}y\,\mathrm{d}x\end{aligned}
$$
- $$
\begin{aligned}\int_{-2}^{2}\int_{-2}^{2}\left(- \frac{6 x y}{\left(x^{2} + y^{2} + 1\right)^{2}}\right)\,\mathrm{d}y\,\mathrm{d}x\end{aligned}
$$
- $$
\begin{aligned}\int_{-2}^{2}\int_{-2}^{2}\left(- \frac{12}{\left(x^{2} + y^{2} + 1\right)^{2}}\right)\,\mathrm{d}y\,\mathrm{d}x\end{aligned}
$$ **(correct)**

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

There are many surfaces whose boundary is the curve $C.$ One such surface is our graph $S$ with the equation

$$z=g(x,y)=\frac{3}{x^{2} + y^{2} + 1}.$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$\begin{aligned}\frac{\partial g}{\partial x}&=\frac{\partial}{\partial x}\left(\frac{3}{x^{2} + y^{2} + 1}\right)=- \frac{6 x}{\left(x^{2} + y^{2} + 1\right)^{2}}\\
\frac{\partial g}{\partial y}&=\frac{\partial}{\partial y}\left(\frac{3}{x^{2} + y^{2} + 1}\right)=- \frac{6 y}{\left(x^{2} + y^{2} + 1\right)^{2}}.\end{aligned}$$

Next, we substitute the equation $z=g(x,y)$ into the expression for $\text{curl}\,F:$

$$\begin{aligned}\text{curl}\,F|_{z=g(x,y)}&=\langle 2 x,\,2 y,\,- 4 z\rangle|_{z=\frac{3}{x^{2} + y^{2} + 1}}\\
&=\langle 2 x,\,2 y,\,- \frac{12}{x^{2} + y^{2} + 1}\rangle\\
&=\langle 2 x,\,2 y,\,- \frac{12}{x^{2} + y^{2} + 1}\rangle.\end{aligned}$$

So, we have

$$\begin{aligned}\iint_S\text{curl}\,F\cdot\mathrm{d}S&=\iint_D(-P g_x-Q g_y+R)\,\mathrm{d}A\\
&=\iint_D\left(-\left(2 x\right)\left(- \frac{6 x}{\left(x^{2} + y^{2} + 1\right)^{2}}\right)-\left(2 y\right)\left(- \frac{6 y}{\left(x^{2} + y^{2} + 1\right)^{2}}\right)+\left(- \frac{12}{x^{2} + y^{2} + 1}\right)\right)\,\mathrm{d}A\\
&=\iint_D\left((\frac{12 x^{2}}{\left(x^{2} + y^{2} + 1\right)^{2}})+(\frac{12 y^{2}}{\left(x^{2} + y^{2} + 1\right)^{2}})+(- \frac{12}{x^{2} + y^{2} + 1})\right)\,\mathrm{d}A\\
&=\iint_D\left(- \frac{12}{\left(x^{2} + y^{2} + 1\right)^{2}}\right)\,\mathrm{d}A.\end{aligned}$$

where $D$ is the region enclosed by the projection of $C$ onto the $xy$-plane.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133927/assets/region-7d843b2c826e7ffa99.png)

Therefore, we obtain

$$\int_{-2}^{2}\int_{-2}^{2}\left(- \frac{12}{\left(x^{2} + y^{2} + 1\right)^{2}}\right)\,\mathrm{d}y\,\mathrm{d}x.$$


## Generated variant — moderate

Let $C$ be the intersection of the surface $z=\sqrt{x^{2} + y^{2}}$ and the vertical column over $D$, where $-2\leq x\leq 0$ and $0\leq y\leq x + 2$. The curve $C$ is oriented counter-clockwise when viewed from above. Given that $\text{curl}\,F=\langle 0,\,- 2 z^{3},\,0\rangle$, use Stokes' theorem to write down the integral that gives the circulation along $C.$

- $$
\begin{aligned}\int_{-2}^{0}\int_{0}^{2}\left(2 y \left(x^{2} + y^{2}\right)^{3}\right)\,\mathrm{d}y\,\mathrm{d}x\end{aligned}
$$
- $$
\begin{aligned}\int_{-2}^{0}\int_{0}^{2}\left(2 \sqrt{x^{2} + y^{2}}\right)\,\mathrm{d}y\,\mathrm{d}x\end{aligned}
$$
- $$
\begin{aligned}\int_{-2}^{0}\int_{0}^{x + 2}\left(2 \left(x^{2} + y^{2}\right)^{2}\right)\,\mathrm{d}y\,\mathrm{d}x\end{aligned}
$$
- $$
\begin{aligned}\int_{-2}^{0}\int_{0}^{x + 2}\left(2 y \left(x^{2} + y^{2}\right)\right)\,\mathrm{d}y\,\mathrm{d}x\end{aligned}
$$ **(correct)**
- $$
\begin{aligned}\int_{-2}^{0}\int_{0}^{x + 2}\left(2 x^{2} + 2 y^{2}\right)\,\mathrm{d}y\,\mathrm{d}x\end{aligned}
$$

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

There are many surfaces whose boundary is the curve $C.$ One such surface is our graph $S$ with the equation

$$z=g(x,y)=\sqrt{x^{2} + y^{2}}.$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$\begin{aligned}\frac{\partial g}{\partial x}&=\frac{\partial}{\partial x}\left(\sqrt{x^{2} + y^{2}}\right)=\frac{x}{\sqrt{x^{2} + y^{2}}}\\
\frac{\partial g}{\partial y}&=\frac{\partial}{\partial y}\left(\sqrt{x^{2} + y^{2}}\right)=\frac{y}{\sqrt{x^{2} + y^{2}}}.\end{aligned}$$

Next, we substitute the equation $z=g(x,y)$ into the expression for $\text{curl}\,F:$

$$\begin{aligned}\text{curl}\,F|_{z=g(x,y)}&=\langle 0,\,- 2 z^{3},\,0\rangle|_{z=\sqrt{x^{2} + y^{2}}}\\
&=\langle 0,\,- 2 \left(x^{2} + y^{2}\right)^{\frac{3}{2}},\,0\rangle\\
&=\langle 0,\,- 2 x^{2} \sqrt{x^{2} + y^{2}} - 2 y^{2} \sqrt{x^{2} + y^{2}},\,0\rangle.\end{aligned}$$

So, we have

$$\begin{aligned}\iint_S\text{curl}\,F\cdot\mathrm{d}S&=\iint_D(-P g_x-Q g_y+R)\,\mathrm{d}A\\
&=\iint_D\left(-\left(0\right)\left(\frac{x}{\sqrt{x^{2} + y^{2}}}\right)-\left(- 2 x^{2} \sqrt{x^{2} + y^{2}} - 2 y^{2} \sqrt{x^{2} + y^{2}}\right)\left(\frac{y}{\sqrt{x^{2} + y^{2}}}\right)+\left(0\right)\right)\,\mathrm{d}A\\
&=\iint_D\left((0)+(\frac{y \left(2 x^{2} \sqrt{x^{2} + y^{2}} + 2 y^{2} \sqrt{x^{2} + y^{2}}\right)}{\sqrt{x^{2} + y^{2}}})+(0)\right)\,\mathrm{d}A\\
&=\iint_D\left(2 y \left(x^{2} + y^{2}\right)\right)\,\mathrm{d}A.\end{aligned}$$

where $D$ is the region enclosed by the projection of $C$ onto the $xy$-plane.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186133927/assets/region-16ef80662c23add039.png)

Therefore, we obtain

$$\int_{-2}^{0}\int_{0}^{x + 2}\left(2 y \left(x^{2} + y^{2}\right)\right)\,\mathrm{d}y\,\mathrm{d}x.$$


## Generated variant — hard

Let $C$ be the intersection of the cylinder $x^2+y^2=9$ and the surface $z=\left(x - 2\right)^{2} + \left(y + 2\right)^{2}$. The curve $C$ is oriented counter-clockwise when viewed from above. Given that $\text{curl}\,F=\langle 2 x + 2 y,\,- 2 x + 2 y,\,- 4 z\rangle$, use Stokes' theorem to evaluate $\oint_C F\cdot\mathrm{d}r.$

- $- 450 \pi$
- $- 336 \pi$
- $612 \pi$
- $- 612 \pi$ **(correct)**
- $- 162 \pi$

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

There are many surfaces whose boundary is the curve $C.$ One such surface is our graph $S$ with the equation

$$z=g(x,y)=\left(x - 2\right)^{2} + \left(y + 2\right)^{2}.$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$\begin{aligned}\frac{\partial g}{\partial x}&=\frac{\partial}{\partial x}\left(\left(x - 2\right)^{2} + \left(y + 2\right)^{2}\right)=2 x - 4\\
\frac{\partial g}{\partial y}&=\frac{\partial}{\partial y}\left(\left(x - 2\right)^{2} + \left(y + 2\right)^{2}\right)=2 y + 4.\end{aligned}$$

Next, we substitute the equation $z=g(x,y)$ into the expression for $\text{curl}\,F:$

$$\begin{aligned}\text{curl}\,F|_{z=g(x,y)}&=\langle 2 x + 2 y,\,- 2 x + 2 y,\,- 4 z\rangle|_{z=\left(x - 2\right)^{2} + \left(y + 2\right)^{2}}\\
&=\langle 2 x + 2 y,\,- 2 x + 2 y,\,- 4 \left(x - 2\right)^{2} - 4 \left(y + 2\right)^{2}\rangle\\
&=\langle 2 x + 2 y,\,- 2 x + 2 y,\,- 4 x^{2} + 16 x - 4 y^{2} - 16 y - 32\rangle.\end{aligned}$$

So, we have

$$\begin{aligned}\iint_S\text{curl}\,F\cdot\mathrm{d}S&=\iint_D(-P g_x-Q g_y+R)\,\mathrm{d}A\\
&=\iint_D\left(-\left(2 x + 2 y\right)\left(2 x - 4\right)-\left(- 2 x + 2 y\right)\left(2 y + 4\right)+\left(- 4 x^{2} + 16 x - 4 y^{2} - 16 y - 32\right)\right)\,\mathrm{d}A\\
&=\iint_D\left((\left(- 2 x - 2 y\right) \left(2 x - 4\right))+(\left(2 x - 2 y\right) \left(2 y + 4\right))+(- 4 x^{2} + 16 x - 4 y^{2} - 16 y - 32)\right)\,\mathrm{d}A\\
&=\iint_D\left(- 8 x^{2} + 32 x - 8 y^{2} - 16 y - 32\right)\,\mathrm{d}A.\end{aligned}$$

where $D$ is the region enclosed by the projection of $C$ onto the $xy$-plane.
Notice that the projection of $C$ onto the $xy$-plane is the circle $x^2+y^2=9.$ Therefore, using the change of variables to polar coordinates

$$x=r\cos\theta,\quad y=r\sin\theta,\quad \mathrm{d}A=r\,\mathrm{d}r\,\mathrm{d}\theta,$$

we obtain

$$\begin{aligned}\iint_D\left(- 8 x^{2} + 32 x - 8 y^{2} - 16 y - 32\right)\,\mathrm{d}A
&=\int_0^{3}\int_0^{2\pi}\left(- 8 r^{2} \sin^{2}{\left(\theta \right)} - 8 r^{2} \cos^{2}{\left(\theta \right)} - 16 r \sin{\left(\theta \right)} + 32 r \cos{\left(\theta \right)} - 32\right)r\,\mathrm{d}\theta\,\mathrm{d}r\\
&=\int_0^{3}\int_0^{2\pi}\left(- 8 r^{3} \sin^{2}{\left(\theta \right)} - 8 r^{3} \cos^{2}{\left(\theta \right)} - 16 r^{2} \sin{\left(\theta \right)} + 32 r^{2} \cos{\left(\theta \right)} - 32 r\right)\,\mathrm{d}\theta\,\mathrm{d}r\\
&=\int_0^{3}\left[- 8 r^{3} \left(\frac{\theta}{2} - \frac{\sin{\left(\theta \right)} \cos{\left(\theta \right)}}{2}\right) - 8 r^{3} \left(\frac{\theta}{2} + \frac{\sin{\left(\theta \right)} \cos{\left(\theta \right)}}{2}\right) + 32 r^{2} \sin{\left(\theta \right)} + 16 r^{2} \cos{\left(\theta \right)} - 32 r \theta\right]_0^{2\pi}\,\mathrm{d}r\\
&=\int_0^{3}\left[\left(- 16 \pi r^{3} + 16 r^{2} - 64 \pi r\right)-\left(16 r^{2}\right)\right]\,\mathrm{d}r\\
&=\int_0^{3}\left(16 \pi r \left(- r^{2} - 4\right)\right)\,\mathrm{d}r\\
&=\left[- 4 \pi r^{4} - 32 \pi r^{2}\right]_0^{3}\\
&=\left[\left(- 288 \pi\right)+\left(- 324 \pi\right)\right]-\left[\left(0\right)+\left(0\right)\right]\\
&=- 612 \pi.\end{aligned}$$


## Generated variant — hard

Let $C$ be the intersection of the cylinder $x^2+y^2=9$ and the surface $z=2 x$. The curve $C$ is oriented counter-clockwise when viewed from above. Given that $\text{curl}\,F=\langle 0,\,2 z,\,2 x\rangle$, use Stokes' theorem to evaluate $\oint_C F\cdot\mathrm{d}r.$

- $0$ **(correct)**
- $54 \pi$
- $-144$
- $36$
- $18$

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

There are many surfaces whose boundary is the curve $C.$ One such surface is our graph $S$ with the equation

$$z=g(x,y)=2 x.$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$\begin{aligned}\frac{\partial g}{\partial x}&=\frac{\partial}{\partial x}\left(2 x\right)=2\\
\frac{\partial g}{\partial y}&=\frac{\partial}{\partial y}\left(2 x\right)=0.\end{aligned}$$

Next, we substitute the equation $z=g(x,y)$ into the expression for $\text{curl}\,F:$

$$\begin{aligned}\text{curl}\,F|_{z=g(x,y)}&=\langle 0,\,2 z,\,2 x\rangle|_{z=2 x}\\
&=\langle 0,\,4 x,\,2 x\rangle\\
&=\langle 0,\,4 x,\,2 x\rangle.\end{aligned}$$

So, we have

$$\begin{aligned}\iint_S\text{curl}\,F\cdot\mathrm{d}S&=\iint_D(-P g_x-Q g_y+R)\,\mathrm{d}A\\
&=\iint_D\left(-\left(0\right)\left(2\right)-\left(4 x\right)\left(0\right)+\left(2 x\right)\right)\,\mathrm{d}A\\
&=\iint_D\left((0)+(0)+(2 x)\right)\,\mathrm{d}A\\
&=\iint_D\left(2 x\right)\,\mathrm{d}A.\end{aligned}$$

where $D$ is the region enclosed by the projection of $C$ onto the $xy$-plane.
Notice that the projection of $C$ onto the $xy$-plane is the circle $x^2+y^2=9.$ Therefore, using the change of variables to polar coordinates

$$x=r\cos\theta,\quad y=r\sin\theta,\quad \mathrm{d}A=r\,\mathrm{d}r\,\mathrm{d}\theta,$$

we obtain

$$\begin{aligned}\iint_D\left(2 x\right)\,\mathrm{d}A
&=\int_0^{3}\int_0^{2\pi}\left(2 r \cos{\left(\theta \right)}\right)r\,\mathrm{d}\theta\,\mathrm{d}r\\
&=\int_0^{3}\int_0^{2\pi}\left(2 r^{2} \cos{\left(\theta \right)}\right)\,\mathrm{d}\theta\,\mathrm{d}r\\
&=\int_0^{3}\left[2 r^{2} \sin{\left(\theta \right)}\right]_0^{2\pi}\,\mathrm{d}r\\
&=\int_0^{3}\left[\left(0\right)-\left(0\right)\right]\,\mathrm{d}r\\
&=\int_0^{3}\left(0\right)\,\mathrm{d}r\\
&=\left[0\right]_0^{3}\\
&=\left[\left(0\right)\right]-\left[\left(0\right)\right]\\
&=0.\end{aligned}$$


## Generated variant — hard

Let $C$ be the intersection of the half-cone $z=-\sqrt{x^2+y^2}$ and the plane $z=-2$. The curve $C$ is oriented counter-clockwise when viewed from above. Given that $\text{curl}\,F=\langle 2 y,\,4 y z,\,2 - 2 z^{2}\rangle$, use Stokes' theorem to evaluate $\oint_C F\cdot\mathrm{d}r.$

- $24 \pi$
- $- 96 \pi$
- $- 8 \pi$
- $- 24 \pi$ **(correct)**
- $- 32 \pi$

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

There are many surfaces whose boundary is the curve $C.$ One such surface is our graph $S$ with the equation

$$z=g(x,y)=-2.$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$\begin{aligned}\frac{\partial g}{\partial x}&=\frac{\partial}{\partial x}\left(-2\right)=0\\
\frac{\partial g}{\partial y}&=\frac{\partial}{\partial y}\left(-2\right)=0.\end{aligned}$$

Next, we substitute the equation $z=g(x,y)$ into the expression for $\text{curl}\,F:$

$$\begin{aligned}\text{curl}\,F|_{z=g(x,y)}&=\langle 2 y,\,4 y z,\,2 - 2 z^{2}\rangle|_{z=-2}\\
&=\langle 2 y,\,- 8 y,\,-6\rangle\\
&=\langle 2 y,\,- 8 y,\,-6\rangle.\end{aligned}$$

So, we have

$$\begin{aligned}\iint_S\text{curl}\,F\cdot\mathrm{d}S&=\iint_D(-P g_x-Q g_y+R)\,\mathrm{d}A\\
&=\iint_D\left(-\left(2 y\right)\left(0\right)-\left(- 8 y\right)\left(0\right)+\left(-6\right)\right)\,\mathrm{d}A\\
&=\iint_D\left((0)+(0)+(-6)\right)\,\mathrm{d}A\\
&=\iint_D\left(-6\right)\,\mathrm{d}A.\end{aligned}$$

where $D$ is the region enclosed by the projection of $C$ onto the $xy$-plane.
Notice that the projection of $C$ onto the $xy$-plane is the circle $x^2+y^2=4.$ Therefore, using the change of variables to polar coordinates

$$x=r\cos\theta,\quad y=r\sin\theta,\quad \mathrm{d}A=r\,\mathrm{d}r\,\mathrm{d}\theta,$$

we obtain

$$\begin{aligned}\iint_D\left(-6\right)\,\mathrm{d}A
&=\int_0^{2}\int_0^{2\pi}\left(-6\right)r\,\mathrm{d}\theta\,\mathrm{d}r\\
&=\int_0^{2}\int_0^{2\pi}\left(- 6 r\right)\,\mathrm{d}\theta\,\mathrm{d}r\\
&=\int_0^{2}\left[- 6 r \theta\right]_0^{2\pi}\,\mathrm{d}r\\
&=\int_0^{2}\left[\left(- 12 \pi r\right)-\left(0\right)\right]\,\mathrm{d}r\\
&=\int_0^{2}\left(- 12 \pi r\right)\,\mathrm{d}r\\
&=\left[- 6 \pi r^{2}\right]_0^{2}\\
&=\left[\left(- 24 \pi\right)\right]-\left[\left(0\right)\right]\\
&=- 24 \pi.\end{aligned}$$


## Generated variant — hard

Let $C$ be the intersection of the cylinder $x^2+y^2=9$ and the surface $z=2 x - y + 3$. The curve $C$ is oriented counter-clockwise when viewed from above. Given that $\text{curl}\,F=\langle - 2 y,\,2 z,\,- 4 x\rangle$, use Stokes' theorem to evaluate $\oint_C F\cdot\mathrm{d}r.$

- $36 \pi$
- $72 \pi$
- $0$
- $- 54 \pi$
- $54 \pi$ **(correct)**

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

There are many surfaces whose boundary is the curve $C.$ One such surface is our graph $S$ with the equation

$$z=g(x,y)=2 x - y + 3.$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$\begin{aligned}\frac{\partial g}{\partial x}&=\frac{\partial}{\partial x}\left(2 x - y + 3\right)=2\\
\frac{\partial g}{\partial y}&=\frac{\partial}{\partial y}\left(2 x - y + 3\right)=-1.\end{aligned}$$

Next, we substitute the equation $z=g(x,y)$ into the expression for $\text{curl}\,F:$

$$\begin{aligned}\text{curl}\,F|_{z=g(x,y)}&=\langle - 2 y,\,2 z,\,- 4 x\rangle|_{z=2 x - y + 3}\\
&=\langle - 2 y,\,4 x - 2 y + 6,\,- 4 x\rangle\\
&=\langle - 2 y,\,4 x - 2 y + 6,\,- 4 x\rangle.\end{aligned}$$

So, we have

$$\begin{aligned}\iint_S\text{curl}\,F\cdot\mathrm{d}S&=\iint_D(-P g_x-Q g_y+R)\,\mathrm{d}A\\
&=\iint_D\left(-\left(- 2 y\right)\left(2\right)-\left(4 x - 2 y + 6\right)\left(-1\right)+\left(- 4 x\right)\right)\,\mathrm{d}A\\
&=\iint_D\left((4 y)+(4 x - 2 y + 6)+(- 4 x)\right)\,\mathrm{d}A\\
&=\iint_D\left(2 y + 6\right)\,\mathrm{d}A.\end{aligned}$$

where $D$ is the region enclosed by the projection of $C$ onto the $xy$-plane.
Notice that the projection of $C$ onto the $xy$-plane is the circle $x^2+y^2=9.$ Therefore, using the change of variables to polar coordinates

$$x=r\cos\theta,\quad y=r\sin\theta,\quad \mathrm{d}A=r\,\mathrm{d}r\,\mathrm{d}\theta,$$

we obtain

$$\begin{aligned}\iint_D\left(2 y + 6\right)\,\mathrm{d}A
&=\int_0^{3}\int_0^{2\pi}\left(2 r \sin{\left(\theta \right)} + 6\right)r\,\mathrm{d}\theta\,\mathrm{d}r\\
&=\int_0^{3}\int_0^{2\pi}\left(2 r^{2} \sin{\left(\theta \right)} + 6 r\right)\,\mathrm{d}\theta\,\mathrm{d}r\\
&=\int_0^{3}\left[- 2 r^{2} \cos{\left(\theta \right)} + 6 r \theta\right]_0^{2\pi}\,\mathrm{d}r\\
&=\int_0^{3}\left[\left(- 2 r^{2} + 12 \pi r\right)-\left(- 2 r^{2}\right)\right]\,\mathrm{d}r\\
&=\int_0^{3}\left(12 \pi r\right)\,\mathrm{d}r\\
&=\left[6 \pi r^{2}\right]_0^{3}\\
&=\left[\left(54 \pi\right)\right]-\left[\left(0\right)\right]\\
&=54 \pi.\end{aligned}$$


## Generated variant — hard

Let $C$ be the intersection of the paraboloid $z=x^2+y^2$ and the plane $z=3$. The curve $C$ is oriented counter-clockwise when viewed from above. Given that $\text{curl}\,F=\langle - 2 x e^{z},\,0,\,2 e^{z}\rangle$, use Stokes' theorem to evaluate $\oint_C F\cdot\mathrm{d}r.$

- $- 6 \pi e^{3}$
- $6 \pi e^{3}$ **(correct)**
- $6 \pi e^{4}$
- $6 \pi$
- $0$

**Worked solution**

Let $S$ be an oriented piecewise-smooth surface bounded by a simple, closed, piecewise-smooth boundary $C$ with positive orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $S,$ then Stokes' theorem states that

$$
{∮}_{C}F\cdot dr={∬}_{S}\text{curl}\,F\cdot \text{d}S.
$$

There are many surfaces whose boundary is the curve $C.$ One such surface is our graph $S$ with the equation

$$z=g(x,y)=3.$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$\begin{aligned}\frac{\partial g}{\partial x}&=\frac{\partial}{\partial x}\left(3\right)=0\\
\frac{\partial g}{\partial y}&=\frac{\partial}{\partial y}\left(3\right)=0.\end{aligned}$$

Next, we substitute the equation $z=g(x,y)$ into the expression for $\text{curl}\,F:$

$$\begin{aligned}\text{curl}\,F|_{z=g(x,y)}&=\langle - 2 x e^{z},\,0,\,2 e^{z}\rangle|_{z=3}\\
&=\langle - 2 x e^{3},\,0,\,2 e^{3}\rangle\\
&=\langle - 2 x e^{3},\,0,\,2 e^{3}\rangle.\end{aligned}$$

So, we have

$$\begin{aligned}\iint_S\text{curl}\,F\cdot\mathrm{d}S&=\iint_D(-P g_x-Q g_y+R)\,\mathrm{d}A\\
&=\iint_D\left(-\left(- 2 x e^{3}\right)\left(0\right)-\left(0\right)\left(0\right)+\left(2 e^{3}\right)\right)\,\mathrm{d}A\\
&=\iint_D\left((0)+(0)+(2 e^{3})\right)\,\mathrm{d}A\\
&=\iint_D\left(2 e^{3}\right)\,\mathrm{d}A.\end{aligned}$$

where $D$ is the region enclosed by the projection of $C$ onto the $xy$-plane.
Notice that the projection of $C$ onto the $xy$-plane is the circle $x^2+y^2=3.$ Therefore, using the change of variables to polar coordinates

$$x=r\cos\theta,\quad y=r\sin\theta,\quad \mathrm{d}A=r\,\mathrm{d}r\,\mathrm{d}\theta,$$

we obtain

$$\begin{aligned}\iint_D\left(2 e^{3}\right)\,\mathrm{d}A
&=\int_0^{\sqrt{3}}\int_0^{2\pi}\left(2 e^{3}\right)r\,\mathrm{d}\theta\,\mathrm{d}r\\
&=\int_0^{\sqrt{3}}\int_0^{2\pi}\left(2 r e^{3}\right)\,\mathrm{d}\theta\,\mathrm{d}r\\
&=\int_0^{\sqrt{3}}\left[2 r \theta e^{3}\right]_0^{2\pi}\,\mathrm{d}r\\
&=\int_0^{\sqrt{3}}\left[\left(4 \pi r e^{3}\right)-\left(0\right)\right]\,\mathrm{d}r\\
&=\int_0^{\sqrt{3}}\left(4 \pi r e^{3}\right)\,\mathrm{d}r\\
&=\left[2 \pi r^{2} e^{3}\right]_0^{\sqrt{3}}\\
&=\left[\left(6 \pi e^{3}\right)\right]-\left[\left(0\right)\right]\\
&=6 \pi e^{3}.\end{aligned}$$
