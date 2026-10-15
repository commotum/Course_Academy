![](images/42/424cfad485da7dd6cac42c9784df348a2a09d2bb4da651926cae32aa6e06cded.png)

Given $\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}=2 x^{2} + 2 y^{2}$, calculate $\oint_{\partial D}P\,\mathrm dx+Q\,\mathrm dy$ over the positively oriented annular region shown above.

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}P\,\mathrm dx+Q\,\mathrm dy & =\iint_D 2 x^{2} + 2 y^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$\Delta=\{(r,\theta):1\le r\le 5,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D 2 x^{2} + 2 y^{2}\,\mathrm dA & =\int_{0}^{2 \pi}\int_{1}^{5}2\left(((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{1}^{5}2\left(r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{1}^{5}2 r^{3}\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{1}^{5}2 r^{3}\,\mathrm d r\\ & =4 \pi\cdot \int_{1}^{5}r^{3}\,\mathrm d r\\ & =4 \pi\cdot \frac{r^{4}}{4}\big|_{1}^{5}\\ & =4 \pi\cdot (\left(\frac{625}{4}\right)-\left(\frac{1}{4}\right))\\ & =2\cdot\left(\frac{\pi}{2}\right)\cdot \left((5)^{4}-\left((1)^{4}\right)\right)\\ & =\pi\cdot \left(625-\left(1\right)\right)\\ & =624 \pi.\end{aligned}
$$

---

![](images/37/37c3ffbceecd99f2c618c1401e392b27620a0e34ce284683446eae4217c5e973.png)

Given $\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}=3 x^{2} + 3 y^{2}$, calculate $\oint_{\partial D}P\,\mathrm dx+Q\,\mathrm dy$ over the positively oriented annular region shown above.

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}P\,\mathrm dx+Q\,\mathrm dy & =\iint_D 3 x^{2} + 3 y^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$\Delta=\{(r,\theta):1\le r\le 4,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D 3 x^{2} + 3 y^{2}\,\mathrm dA & =\int_{0}^{2 \pi}\int_{1}^{4}3\left(((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{1}^{4}3\left(r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{1}^{4}3 r^{3}\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{1}^{4}3 r^{3}\,\mathrm d r\\ & =6 \pi\cdot \int_{1}^{4}r^{3}\,\mathrm d r\\ & =6 \pi\cdot \frac{r^{4}}{4}\big|_{1}^{4}\\ & =6 \pi\cdot (\left(64\right)-\left(\frac{1}{4}\right))\\ & =3\cdot\left(\frac{\pi}{2}\right)\cdot \left((4)^{4}-\left((1)^{4}\right)\right)\\ & =\frac{3 \pi}{2}\cdot \left(256-\left(1\right)\right)\\ & =\frac{765 \pi}{2}.\end{aligned}
$$

---

![](images/9e/9e863fbe1fbcc931a1acaf67fe92990d4bd0551f8c5a1a89a01c8eeba367d668.png)

Given $\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}=- 2 x^{2} - 2 y^{2}$, calculate $\oint_{\partial D}P\,\mathrm dx+Q\,\mathrm dy$ over the positively oriented annular region shown above.

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}P\,\mathrm dx+Q\,\mathrm dy & =\iint_D - 2 x^{2} - 2 y^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$\Delta=\{(r,\theta):2\le r\le 5,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 2 x^{2} - 2 y^{2}\,\mathrm dA & =\int_{0}^{2 \pi}\int_{2}^{5}-2\left(((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{2}^{5}-2\left(r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{2}^{5}- 2 r^{3}\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{2}^{5}- 2 r^{3}\,\mathrm d r\\ & =- 4 \pi\cdot \int_{2}^{5}r^{3}\,\mathrm d r\\ & =- 4 \pi\cdot \frac{r^{4}}{4}\big|_{2}^{5}\\ & =- 4 \pi\cdot (\left(\frac{625}{4}\right)-\left(4\right))\\ & =-2\cdot\left(\frac{\pi}{2}\right)\cdot \left((5)^{4}-\left((2)^{4}\right)\right)\\ & =- \pi\cdot \left(625-\left(16\right)\right)\\ & =- 609 \pi.\end{aligned}
$$

---

![](images/c4/c4b3ac630020f1c4bd2d19dfb311b00fc0af41876497ce4772838e90ced60bd7.png)

Given $\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}=- 2 x^{2} - 2 y^{2}$, calculate $\oint_{\partial D}P\,\mathrm dx+Q\,\mathrm dy$ over the positively oriented annular region shown above.

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}P\,\mathrm dx+Q\,\mathrm dy & =\iint_D - 2 x^{2} - 2 y^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$\Delta=\{(r,\theta):3\le r\le 4,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 2 x^{2} - 2 y^{2}\,\mathrm dA & =\int_{0}^{2 \pi}\int_{3}^{4}-2\left(((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}-2\left(r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}- 2 r^{3}\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{3}^{4}- 2 r^{3}\,\mathrm d r\\ & =- 4 \pi\cdot \int_{3}^{4}r^{3}\,\mathrm d r\\ & =- 4 \pi\cdot \frac{r^{4}}{4}\big|_{3}^{4}\\ & =- 4 \pi\cdot (\left(64\right)-\left(\frac{81}{4}\right))\\ & =-2\cdot\left(\frac{\pi}{2}\right)\cdot \left((4)^{4}-\left((3)^{4}\right)\right)\\ & =- \pi\cdot \left(256-\left(81\right)\right)\\ & =- 175 \pi.\end{aligned}
$$

---

![](images/b7/b73bdd66e1e9ac758c98d854bfe93b6fcf82ff8d85322f607e50b75a5797770f.png)

Given $\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}=x^{2} + y^{2}$, calculate $\oint_{\partial D}P\,\mathrm dx+Q\,\mathrm dy$ over the positively oriented annular region shown above.

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}P\,\mathrm dx+Q\,\mathrm dy & =\iint_D x^{2} + y^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$\Delta=\{(r,\theta):3\le r\le 5,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D x^{2} + y^{2}\,\mathrm dA & =\int_{0}^{2 \pi}\int_{3}^{5}((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{5}r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{5}r^{3}\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{3}^{5}r^{3}\,\mathrm d r\\ & =2 \pi\cdot \int_{3}^{5}r^{3}\,\mathrm d r\\ & =2 \pi\cdot \frac{r^{4}}{4}\big|_{3}^{5}\\ & =2 \pi\cdot (\left(\frac{625}{4}\right)-\left(\frac{81}{4}\right))\\ & =\frac{\pi}{2}\cdot \left((5)^{4}-\left((3)^{4}\right)\right)\\ & =\frac{\pi}{2}\cdot \left(625-\left(81\right)\right)\\ & =272 \pi.\end{aligned}
$$

---

![](images/c4/c4b3ac630020f1c4bd2d19dfb311b00fc0af41876497ce4772838e90ced60bd7.png)

Calculate $\oint_{\partial D}(x^{2} y + y^{3})\,\mathrm dx+(- x^{3} - x y^{2})\,\mathrm dy$, where $D$ is the annular region shown above.

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=x^{2} y + y^{3}$ and $Q(x,y)=- x^{3} - x y^{2}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(x^{2} y + y^{3}\right)=\left(3 y^{2}\right)+\left(x^{2}\right)=x^{2} + 3 y^{2}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- x^{3} - x y^{2}\right)=\left(- 3 x^{2}\right)+\left(- y^{2}\right)=- 3 x^{2} - y^{2}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=x^{2} + 3 y^{2},\qquad\frac{\partial Q}{\partial x}=- 3 x^{2} - y^{2}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(x^{2} y + y^{3})\,\mathrm dx+(- x^{3} - x y^{2})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(- 3 x^{2} - y^{2}-(x^{2} + 3 y^{2})\right)\,\mathrm dA\\ & =\iint_D(- 4 x^{2} - 4 y^{2})\,\mathrm dA\\ & =\iint_D - 4 \left(x^{2} + y^{2}\right)\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$\Delta=\{(r,\theta):3\le r\le 4,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 4 \left(x^{2} + y^{2}\right)\,\mathrm dA & =-4\cdot \int_{0}^{2 \pi}\int_{3}^{4}((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =-4\cdot \int_{0}^{2 \pi}\int_{3}^{4}r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =-4\cdot \int_{0}^{2 \pi}\int_{3}^{4}r^{3}\,\mathrm d r\,\mathrm d \theta\\ & =-4\cdot \int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{3}^{4}r^{3}\,\mathrm d r\\ & =- 8 \pi\cdot \int_{3}^{4}r^{3}\,\mathrm d r\\ & =- 8 \pi\cdot \frac{r^{4}}{4}\big|_{3}^{4}\\ & =- 8 \pi\cdot (\left(64\right)-\left(\frac{81}{4}\right))\\ & =-1\cdot\left(2 \pi\right)\cdot \left((4)^{4}-\left((3)^{4}\right)\right)\\ & =- 2 \pi\cdot \left(256-\left(81\right)\right)\\ & =- 350 \pi.\end{aligned}
$$