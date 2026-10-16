Given that
$∮_(C)F \cdot dr = \displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{3}\boxed{}drdθ$,
where $F(x, y) = ⟨5xy^{2}, 5x + e^{\cos y}⟩$ and $C$ is the circle $x^{2} + y^{2} = 9$ oriented counterclockwise, what is the missing part of the equation? Use $x=r\cos\theta$, $y=r\sin\theta$, and simplify the integrand pointwise before integration.

- $r (- 5 r^{2} \sin{(2 \theta )} + 5)$
- $5 r$
- $- 5 r^{3} \sin{(2 \theta )}$
- $- 5 r^{2} \sin{(2 \theta )} + 5$
- $r (5 r^{2} \sin{(2 \theta )} + 5)$

First, notice that we can rewrite our integral as $\oint_C F\cdot dr=\oint_C(5 x y^{2})\,dx+(5 x + e^{\cos{(y )}})\,dy$.

Green's theorem states that $\oint_C P\,dx+Q\,dy=\iint_D(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y})\,dA$.

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![](images/3b/3b1a8cf50ccf8ab3a73f31753def3c2fee2143a7372309cccf2ff7a5e68aedd9.png)

Since $P(x,y)=5 x y^{2}$ and $Q(x,y)=5 x + e^{\cos{(y )}}$, we obtain $\frac{\partial P}{\partial y}=10 x y$, $\frac{\partial Q}{\partial x}=5$.

Applying Green's theorem, we get $\oint_C F\cdot dr=\iint_D(5-(10 x y))\,dA=\iint_D(- 10 x y + 5)\,dA$.

Now, notice that the region $D$ can be represented in polar coordinates as $\Delta=\{(r,\theta):0\le r\le 3,0\le\theta\le2\pi\}$.

The change of variables formula for plane polar coordinates states that $\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,dr\,d\theta$.

Therefore, we can write our double integral as $\iint_D(- 10 x y + 5)\,dA=\iint_\Delta(- 10 r^{2} \sin{(\theta )} \cos{(\theta )} + 5)r\,dr\,d\theta=\int_0^{2\pi}\int_0^{3}r (- 5 r^{2} \sin{(2 \theta )} + 5)\,dr\,d\theta$.