# Per-source normal solution fidelity

These are calculation-renderer comparisons, not eligibility claims for original operation banks. Rectangle anchors with colliding normal banks remain rejected by the public API. Each source’s own operative stages are checked in order, beyond mathematical equality. Raw source mistakes remain in the source column; the normal column uses documented minimal repairs.

## q-126566 — original anchor

Parameters: `{"c": 1, "inner": 1, "outer": 2}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=-{x}^{2}y$ and $Q(x,y)=x{y}^{2}.$ So,

$$
\frac{∂P}{∂y}=-{x}^{2},\,\frac{∂Q}{∂x}={y}^{2}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}-{x}^{2}y\,dx+x{y}^{2}\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}{y}^{2}-(-{x}^{2})\,\text{d}A \\  & ={∬}_{D}{x}^{2}+{y}^{2}\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$
Δ=\{(r,\theta )\,:\,1\le r\le 2,\,0\le \theta \le 2\pi \}.
$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}{x}^{2}+{y}^{2}\,\text{d}A & ={\int }_{0}^{2\pi }{\int }_{1}^{2}(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}\cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{1}^{2}{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{1}^{2}{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }\,\text{d}\theta {\int }_{1}^{2}{r}^{3}\,\text{d}r \\  & =2\pi {\int }_{1}^{2}{r}^{3}\,\text{d}r \\  & =2\pi \cdot {\frac{1}{4}{r}^{4}|}_{1}^{2} \\  & =\frac{\pi }{2}\cdot ({2}^{4}-{1}^{4}) \\  & =\frac{15\pi }{2}.\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=- x^{2} y$ and $Q(x,y)=x y^{2}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- x^{2} y\right)=\left(- x^{2}\right)=- x^{2}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(x y^{2}\right)=\left(y^{2}\right)=y^{2}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- x^{2},\qquad\frac{\partial Q}{\partial x}=y^{2}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(- x^{2} y)\,\mathrm dx+(x y^{2})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(y^{2}-(- x^{2})\right)\,\mathrm dA\\ & =\iint_D x^{2} + y^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$\Delta=\{(r,\theta):1\le r\le 2,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D x^{2} + y^{2}\,\mathrm dA & =\int_{0}^{2 \pi}\int_{1}^{2}((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{1}^{2}r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{1}^{2}r^{3}\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{1}^{2}r^{3}\,\mathrm d r\\ & =2 \pi\cdot \int_{1}^{2}r^{3}\,\mathrm d r\\ & =2 \pi\cdot \frac{r^{4}}{4}\big|_{1}^{2}\\ & =2 \pi\cdot (\left(4\right)-\left(\frac{1}{4}\right))\\ & =\frac{\pi}{2}\cdot \left((2)^{4}-\left((1)^{4}\right)\right)\\ & =\frac{\pi}{2}\cdot \left(16-\left(1\right)\right)\\ & =\frac{15 \pi}{2}.\end{aligned}
$$

Checked original operation fragments in order:

- `\int_{0}^{2 \pi}\int_{1}^{2}((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\int_{1}^{2}r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\int_{1}^{2}r^{3}\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{1}^{2}r^{3}\,\mathrm d r`
- `2 \pi\cdot \int_{1}^{2}r^{3}\,\mathrm d r`
- `2 \pi\cdot \frac{r^{4}}{4}\big|_{1}^{2}`
- `\frac{\pi}{2}\cdot \left((2)^{4}-\left((1)^{4}\right)\right)`

## q-126566 — changed parameters

Parameters: `{"c": -3, "inner": 3, "outer": 4}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=-{x}^{2}y$ and $Q(x,y)=x{y}^{2}.$ So,

$$
\frac{∂P}{∂y}=-{x}^{2},\,\frac{∂Q}{∂x}={y}^{2}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}-{x}^{2}y\,dx+x{y}^{2}\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}{y}^{2}-(-{x}^{2})\,\text{d}A \\  & ={∬}_{D}{x}^{2}+{y}^{2}\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$
Δ=\{(r,\theta )\,:\,1\le r\le 2,\,0\le \theta \le 2\pi \}.
$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}{x}^{2}+{y}^{2}\,\text{d}A & ={\int }_{0}^{2\pi }{\int }_{1}^{2}(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}\cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{1}^{2}{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{1}^{2}{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }\,\text{d}\theta {\int }_{1}^{2}{r}^{3}\,\text{d}r \\  & =2\pi {\int }_{1}^{2}{r}^{3}\,\text{d}r \\  & =2\pi \cdot {\frac{1}{4}{r}^{4}|}_{1}^{2} \\  & =\frac{\pi }{2}\cdot ({2}^{4}-{1}^{4}) \\  & =\frac{15\pi }{2}.\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=3 x^{2} y$ and $Q(x,y)=- 3 x y^{2}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(3 x^{2} y\right)=\left(3 x^{2}\right)=3 x^{2}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- 3 x y^{2}\right)=\left(- 3 y^{2}\right)=- 3 y^{2}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=3 x^{2},\qquad\frac{\partial Q}{\partial x}=- 3 y^{2}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(3 x^{2} y)\,\mathrm dx+(- 3 x y^{2})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(- 3 y^{2}-(3 x^{2})\right)\,\mathrm dA\\ & =\iint_D - 3 \left(x^{2} + y^{2}\right)\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$\Delta=\{(r,\theta):3\le r\le 4,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 3 \left(x^{2} + y^{2}\right)\,\mathrm dA & =\int_{0}^{2 \pi}\int_{3}^{4}-3\left(((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}-3\left(r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}- 3 r^{3}\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{3}^{4}- 3 r^{3}\,\mathrm d r\\ & =- 6 \pi\cdot \int_{3}^{4}r^{3}\,\mathrm d r\\ & =- 6 \pi\cdot \frac{r^{4}}{4}\big|_{3}^{4}\\ & =- 6 \pi\cdot (\left(64\right)-\left(\frac{81}{4}\right))\\ & =-3\cdot\left(\frac{\pi}{2}\right)\cdot \left((4)^{4}-\left((3)^{4}\right)\right)\\ & =- \frac{3 \pi}{2}\cdot \left(256-\left(81\right)\right)\\ & =- \frac{525 \pi}{2}.\end{aligned}
$$

Checked original operation fragments in order:

- `\int_{0}^{2 \pi}\int_{3}^{4}-3\left(((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\right)\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\int_{3}^{4}-3\left(r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\right)\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\int_{3}^{4}- 3 r^{3}\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{3}^{4}- 3 r^{3}\,\mathrm d r`
- `- 6 \pi\cdot \int_{3}^{4}r^{3}\,\mathrm d r`
- `- 6 \pi\cdot \frac{r^{4}}{4}\big|_{3}^{4}`
- `-3\cdot\left(\frac{\pi}{2}\right)\cdot \left((4)^{4}-\left((3)^{4}\right)\right)`

## q-126645 — original anchor

Parameters: `{"c": 1, "hole": [0, 2, -1, 2], "outer": [-4, 4, -3, 3]}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=x{y}^{2}$ and $Q(x,y)={x}^{2}y+x{y}^{2}.$ Therefore,

$$
\frac{∂P}{∂y}=2xy,\,\frac{∂Q}{∂x}=2xy+{y}^{2}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}x{y}^{2}\,dx+({x}^{2}y+x{y}^{2})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}(2xy+{y}^{2})-2xy\,\text{d}A \\  & ={∬}_{D}{y}^{2}\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as ${Δ}_{1}∖{Δ}_{2},$ where

- ${Δ}_{1}={(x,y)\,:\,-4\le x\le 4,-3\le y\le 3}$ is the region enclosed by the outer curve, and

- ${Δ}_{2}={(x,y)\,:\,0\le x\le 2,-1\le y\le 2}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}{y}^{2}\,\text{d}A & ={∬}_{{Δ}_{1}}{y}^{2}\,\text{d}A-{∬}_{{Δ}_{2}}{y}^{2}\,\text{d}A \\  & ={\int }_{-3}^{3}{\int }_{-4}^{4}{y}^{2}\,\text{d}x\,\text{d}y-{\int }_{-1}^{2}{\int }_{0}^{2}{y}^{2}\,\text{d}x\,\text{d}y \\  & ={\int }_{-4}^{4}\,\text{d}x{\int }_{-3}^{3}{y}^{2}\,\text{d}y-{\int }_{0}^{2}\,\text{d}x{\int }_{-1}^{2}{y}^{2}\,\text{d}y \\  & =x\,{|}_{-4}^{4}\cdot \frac{{y}^{3}}{3}\,{|}_{-3}^{3}-x\,{|}_{0}^{2}\cdot \frac{{y}^{3}}{3}{|}_{-1}^{2} \\  & =(4-(-4))\cdot (9-(-9))-(2-0)\cdot (\frac{8}{3}-(-\frac{1}{3})) \\  & =8\cdot 18-2\cdot 3 \\  & =138.\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=x y^{2}$ and $Q(x,y)=x^{2} y + x y^{2}.$ Therefore,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(x y^{2}\right)=\left(2 x y\right)=2 x y\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(x^{2} y + x y^{2}\right)=\left(y^{2}\right)+\left(2 x y\right)=2 x y + y^{2}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=2 x y,\qquad\frac{\partial Q}{\partial x}=2 x y + y^{2}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(x y^{2})\,\mathrm dx+(x^{2} y + x y^{2})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(2 x y + y^{2}-(2 x y)\right)\,\mathrm dA\\ & =\iint_D y^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as $\Delta_1\setminus\Delta_2,$ where

- $\Delta_1=\{(x,y):-4\le x\le 4,-3\le y\le 3\}$ is the region enclosed by the outer curve, and

- $\Delta_2=\{(x,y):0\le x\le 2,-1\le y\le 2\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D y^{2}\,\mathrm dA & =\iint_{\Delta_1}y^{2}\,\mathrm dA-\iint_{\Delta_2}y^{2}\,\mathrm dA\\ & =\int_{-3}^{3}\int_{-4}^{4}y^{2}\,\mathrm d x\,\mathrm d y-\int_{-1}^{2}\int_{0}^{2}y^{2}\,\mathrm d x\,\mathrm d y\\ & =\int_{-4}^{4}\,\mathrm d x\cdot \int_{-3}^{3}y^{2}\,\mathrm d y-\int_{0}^{2}\,\mathrm d x\cdot \int_{-1}^{2}y^{2}\,\mathrm d y\\ & =x\big|_{-4}^{4}\cdot \frac{y^3}{3}\big|_{-3}^{3}-x\big|_{0}^{2}\cdot \frac{y^3}{3}\big|_{-1}^{2}\\ & =(\left(4\right)-\left(-4\right))\cdot (\left(9\right)-\left(-9\right))-(\left(2\right)-\left(0\right))\cdot (\left(\frac{8}{3}\right)-\left(- \frac{1}{3}\right))\\ & =\left(8\right)\cdot \left(18\right)-\left(2\right)\cdot \left(3\right)\\ & =138.\end{aligned}
$$

Checked original operation fragments in order:

- `\iint_{\Delta_1}y^{2}\,\mathrm dA-\iint_{\Delta_2}y^{2}\,\mathrm dA`
- `\int_{-3}^{3}\int_{-4}^{4}y^{2}\,\mathrm d x\,\mathrm d y-\int_{-1}^{2}\int_{0}^{2}y^{2}\,\mathrm d x\,\mathrm d y`
- `\int_{-4}^{4}\,\mathrm d x\cdot \int_{-3}^{3}y^{2}\,\mathrm d y-\int_{0}^{2}\,\mathrm d x\cdot \int_{-1}^{2}y^{2}\,\mathrm d y`
- `x\big|_{-4}^{4}\cdot \frac{y^3}{3}\big|_{-3}^{3}-x\big|_{0}^{2}\cdot \frac{y^3}{3}\big|_{-1}^{2}`
- `(\left(4\right)-\left(-4\right))\cdot (\left(9\right)-\left(-9\right))-(\left(2\right)-\left(0\right))\cdot (\left(\frac{8}{3}\right)-\left(- \frac{1}{3}\right))`
- `\left(8\right)\cdot \left(18\right)-\left(2\right)\cdot \left(3\right)`

## q-126645 — changed parameters

Parameters: `{"c": -3, "hole": [1, 3, -2, 1], "outer": [-3, 5, -4, 2]}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=x{y}^{2}$ and $Q(x,y)={x}^{2}y+x{y}^{2}.$ Therefore,

$$
\frac{∂P}{∂y}=2xy,\,\frac{∂Q}{∂x}=2xy+{y}^{2}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}x{y}^{2}\,dx+({x}^{2}y+x{y}^{2})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}(2xy+{y}^{2})-2xy\,\text{d}A \\  & ={∬}_{D}{y}^{2}\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as ${Δ}_{1}∖{Δ}_{2},$ where

- ${Δ}_{1}={(x,y)\,:\,-4\le x\le 4,-3\le y\le 3}$ is the region enclosed by the outer curve, and

- ${Δ}_{2}={(x,y)\,:\,0\le x\le 2,-1\le y\le 2}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}{y}^{2}\,\text{d}A & ={∬}_{{Δ}_{1}}{y}^{2}\,\text{d}A-{∬}_{{Δ}_{2}}{y}^{2}\,\text{d}A \\  & ={\int }_{-3}^{3}{\int }_{-4}^{4}{y}^{2}\,\text{d}x\,\text{d}y-{\int }_{-1}^{2}{\int }_{0}^{2}{y}^{2}\,\text{d}x\,\text{d}y \\  & ={\int }_{-4}^{4}\,\text{d}x{\int }_{-3}^{3}{y}^{2}\,\text{d}y-{\int }_{0}^{2}\,\text{d}x{\int }_{-1}^{2}{y}^{2}\,\text{d}y \\  & =x\,{|}_{-4}^{4}\cdot \frac{{y}^{3}}{3}\,{|}_{-3}^{3}-x\,{|}_{0}^{2}\cdot \frac{{y}^{3}}{3}{|}_{-1}^{2} \\  & =(4-(-4))\cdot (9-(-9))-(2-0)\cdot (\frac{8}{3}-(-\frac{1}{3})) \\  & =8\cdot 18-2\cdot 3 \\  & =138.\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=- 3 x y^{2}$ and $Q(x,y)=- 3 x^{2} y - 3 x y^{2}.$ Therefore,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- 3 x y^{2}\right)=\left(- 6 x y\right)=- 6 x y\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- 3 x^{2} y - 3 x y^{2}\right)=\left(- 3 y^{2}\right)+\left(- 6 x y\right)=- 6 x y - 3 y^{2}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- 6 x y,\qquad\frac{\partial Q}{\partial x}=- 6 x y - 3 y^{2}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(- 3 x y^{2})\,\mathrm dx+(- 3 x^{2} y - 3 x y^{2})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(- 6 x y - 3 y^{2}-(- 6 x y)\right)\,\mathrm dA\\ & =\iint_D - 3 y^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as $\Delta_1\setminus\Delta_2,$ where

- $\Delta_1=\{(x,y):-3\le x\le 5,-4\le y\le 2\}$ is the region enclosed by the outer curve, and

- $\Delta_2=\{(x,y):1\le x\le 3,-2\le y\le 1\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 3 y^{2}\,\mathrm dA & =\iint_{\Delta_1}- 3 y^{2}\,\mathrm dA-\iint_{\Delta_2}- 3 y^{2}\,\mathrm dA\\ & =\int_{-4}^{2}\int_{-3}^{5}- 3 y^{2}\,\mathrm d x\,\mathrm d y-\int_{-2}^{1}\int_{1}^{3}- 3 y^{2}\,\mathrm d x\,\mathrm d y\\ & =\int_{-3}^{5}-3\,\mathrm d x\cdot \int_{-4}^{2}y^{2}\,\mathrm d y-\int_{1}^{3}-3\,\mathrm d x\cdot \int_{-2}^{1}y^{2}\,\mathrm d y\\ & =- 3 x\big|_{-3}^{5}\cdot \frac{y^3}{3}\big|_{-4}^{2}-- 3 x\big|_{1}^{3}\cdot \frac{y^3}{3}\big|_{-2}^{1}\\ & =(\left(-15\right)-\left(9\right))\cdot (\left(\frac{8}{3}\right)-\left(- \frac{64}{3}\right))-(\left(-9\right)-\left(-3\right))\cdot (\left(\frac{1}{3}\right)-\left(- \frac{8}{3}\right))\\ & =\left(-24\right)\cdot \left(24\right)-\left(-6\right)\cdot \left(3\right)\\ & =-558.\end{aligned}
$$

Checked original operation fragments in order:

- `\iint_{\Delta_1}- 3 y^{2}\,\mathrm dA-\iint_{\Delta_2}- 3 y^{2}\,\mathrm dA`
- `\int_{-4}^{2}\int_{-3}^{5}- 3 y^{2}\,\mathrm d x\,\mathrm d y-\int_{-2}^{1}\int_{1}^{3}- 3 y^{2}\,\mathrm d x\,\mathrm d y`
- `\int_{-3}^{5}-3\,\mathrm d x\cdot \int_{-4}^{2}y^{2}\,\mathrm d y-\int_{1}^{3}-3\,\mathrm d x\cdot \int_{-2}^{1}y^{2}\,\mathrm d y`
- `- 3 x\big|_{-3}^{5}\cdot \frac{y^3}{3}\big|_{-4}^{2}-- 3 x\big|_{1}^{3}\cdot \frac{y^3}{3}\big|_{-2}^{1}`
- `(\left(-15\right)-\left(9\right))\cdot (\left(\frac{8}{3}\right)-\left(- \frac{64}{3}\right))-(\left(-9\right)-\left(-3\right))\cdot (\left(\frac{1}{3}\right)-\left(- \frac{8}{3}\right))`
- `\left(-24\right)\cdot \left(24\right)-\left(-6\right)\cdot \left(3\right)`

## q-169207 — original anchor

Parameters: `{"c": 1, "inner": 1, "outer": 2}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

As we saw earlier, we can use Green's theorem to write our line integral in polar coordinates as 

$$
{∮}_{∂R}3x{y}^{2}\,dx-{y}^{3}\,dy={∬}_{Δ}-3{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\text{d}\theta .
$$

But this time, our region $R$ (in polar coordinates) is given by 

$$
Δ={(r,\theta )\,:\,1\le r\le 2,\,0\le \theta <2\pi }.
$$

Therefore, we get

$$
\begin{aligned}{∬}_{Δ}-3{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\text{d}\theta  & =-3{\int }_{0}^{2\pi }{\int }_{1}^{2}{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta  \\  & =-3{\int }_{0}^{2\pi }\operatorname{sin}⁡(2\theta )\,\text{d}\theta \cdot {\int }_{1}^{2}{r}^{3}\,\text{d}r \\  & =-3{[\frac{\operatorname{cos}⁡(2\theta )}{-2}]}_{\theta =0}^{\theta =2\pi }\cdot {[\frac{1}{4}{r}^{4}]}_{r=1}^{r=2}\,\text{d}r \\  & =\frac{3}{2}(1-1)\cdot \frac{1}{4}({2}^{4}-{1}^{4}) \\  & =0.\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=3 x y^{2}$ and $Q(x,y)=- y^{3}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(3 x y^{2}\right)=\left(6 x y\right)=6 x y\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- y^{3}\right)=\left(0\right)=0.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=6 x y,\qquad\frac{\partial Q}{\partial x}=0.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial R}(3 x y^{2})\,\mathrm dx+(- y^{3})\,\mathrm dy & =\iint_R\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_R\left(0-(6 x y)\right)\,\mathrm dA\\ & =\iint_R - 6 x y\,\mathrm dA.\end{aligned}
$$

As we saw earlier, we can use Green's theorem to write our line integral in polar coordinates as 

$$\oint_{\partial R}(3 x y^{2})\,\mathrm dx+(- y^{3})\,\mathrm dy=\iint_\Delta -3r^3\sin(2\theta)\,\mathrm dr\,\mathrm d\theta.$$

But this time, our region $R$ (in polar coordinates) is given by 

$$\Delta=\{(r,\theta):1\le r\le 2,0\le\theta<2\pi\}.$$

Therefore, we get

$$
\begin{aligned}\iint_\Delta -3r^3\sin(2\theta)\,\mathrm dr\,\mathrm d\theta & =-3\cdot \int_{0}^{2 \pi}\int_{1}^{2}r^3\sin(2\theta)\,\mathrm d r\,\mathrm d \theta\\ & =-3\cdot \int_{0}^{2 \pi}\sin(2\theta)\,\mathrm d \theta\cdot \int_{1}^{2}r^3\,\mathrm d r\\ & =-3\cdot \frac{\cos(2\theta)}{-2}\big|_{0}^{2 \pi}\cdot \frac{r^4}{4}\big|_{1}^{2}\\ & =-3\cdot (\left(- \frac{1}{2}\right)-\left(- \frac{1}{2}\right))\cdot (\left(4\right)-\left(\frac{1}{4}\right))\\ & =\frac{3}{2}\cdot (1-1)\cdot\frac{1}{4}\cdot \left((2)^{4}-\left((1)^{4}\right)\right)\\ & =\frac{3}{2}\cdot (1-1)\cdot\frac{1}{4}\cdot \left(16-\left(1\right)\right)\\ & =0.\end{aligned}
$$

Checked original operation fragments in order:

- `-3\cdot \int_{0}^{2 \pi}\int_{1}^{2}r^3\sin(2\theta)\,\mathrm d r\,\mathrm d \theta`
- `-3\cdot \int_{0}^{2 \pi}\sin(2\theta)\,\mathrm d \theta\cdot \int_{1}^{2}r^3\,\mathrm d r`
- `-3\cdot \frac{\cos(2\theta)}{-2}\big|_{0}^{2 \pi}\cdot \frac{r^4}{4}\big|_{1}^{2}`
- `\frac{3}{2}\cdot (1-1)\cdot\frac{1}{4}\cdot \left((2)^{4}-\left((1)^{4}\right)\right)`

## q-169207 — changed parameters

Parameters: `{"c": -3, "inner": 3, "outer": 4}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

As we saw earlier, we can use Green's theorem to write our line integral in polar coordinates as 

$$
{∮}_{∂R}3x{y}^{2}\,dx-{y}^{3}\,dy={∬}_{Δ}-3{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\text{d}\theta .
$$

But this time, our region $R$ (in polar coordinates) is given by 

$$
Δ={(r,\theta )\,:\,1\le r\le 2,\,0\le \theta <2\pi }.
$$

Therefore, we get

$$
\begin{aligned}{∬}_{Δ}-3{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\text{d}\theta  & =-3{\int }_{0}^{2\pi }{\int }_{1}^{2}{r}^{3}\operatorname{sin}⁡(2\theta )\,\text{d}r\,\text{d}\theta  \\  & =-3{\int }_{0}^{2\pi }\operatorname{sin}⁡(2\theta )\,\text{d}\theta \cdot {\int }_{1}^{2}{r}^{3}\,\text{d}r \\  & =-3{[\frac{\operatorname{cos}⁡(2\theta )}{-2}]}_{\theta =0}^{\theta =2\pi }\cdot {[\frac{1}{4}{r}^{4}]}_{r=1}^{r=2}\,\text{d}r \\  & =\frac{3}{2}(1-1)\cdot \frac{1}{4}({2}^{4}-{1}^{4}) \\  & =0.\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=- 9 x y^{2}$ and $Q(x,y)=3 y^{3}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- 9 x y^{2}\right)=\left(- 18 x y\right)=- 18 x y\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(3 y^{3}\right)=\left(0\right)=0.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- 18 x y,\qquad\frac{\partial Q}{\partial x}=0.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial R}(- 9 x y^{2})\,\mathrm dx+(3 y^{3})\,\mathrm dy & =\iint_R\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_R\left(0-(- 18 x y)\right)\,\mathrm dA\\ & =\iint_R 18 x y\,\mathrm dA.\end{aligned}
$$

As we saw earlier, we can use Green's theorem to write our line integral in polar coordinates as 

$$\oint_{\partial R}(- 9 x y^{2})\,\mathrm dx+(3 y^{3})\,\mathrm dy=\iint_\Delta 9r^3\sin(2\theta)\,\mathrm dr\,\mathrm d\theta.$$

But this time, our region $R$ (in polar coordinates) is given by 

$$\Delta=\{(r,\theta):3\le r\le 4,0\le\theta<2\pi\}.$$

Therefore, we get

$$
\begin{aligned}\iint_\Delta 9r^3\sin(2\theta)\,\mathrm dr\,\mathrm d\theta & =9\cdot \int_{0}^{2 \pi}\int_{3}^{4}r^3\sin(2\theta)\,\mathrm d r\,\mathrm d \theta\\ & =9\cdot \int_{0}^{2 \pi}\sin(2\theta)\,\mathrm d \theta\cdot \int_{3}^{4}r^3\,\mathrm d r\\ & =9\cdot \frac{\cos(2\theta)}{-2}\big|_{0}^{2 \pi}\cdot \frac{r^4}{4}\big|_{3}^{4}\\ & =9\cdot (\left(- \frac{1}{2}\right)-\left(- \frac{1}{2}\right))\cdot (\left(64\right)-\left(\frac{81}{4}\right))\\ & =-3\cdot\left(\frac{3}{2}\right)\cdot (1-1)\cdot\frac{1}{4}\cdot \left((4)^{4}-\left((3)^{4}\right)\right)\\ & =- \frac{9}{2}\cdot (1-1)\cdot\frac{1}{4}\cdot \left(256-\left(81\right)\right)\\ & =0.\end{aligned}
$$

Checked original operation fragments in order:

- `9\cdot \int_{0}^{2 \pi}\int_{3}^{4}r^3\sin(2\theta)\,\mathrm d r\,\mathrm d \theta`
- `9\cdot \int_{0}^{2 \pi}\sin(2\theta)\,\mathrm d \theta\cdot \int_{3}^{4}r^3\,\mathrm d r`
- `9\cdot \frac{\cos(2\theta)}{-2}\big|_{0}^{2 \pi}\cdot \frac{r^4}{4}\big|_{3}^{4}`
- `-3\cdot\left(\frac{3}{2}\right)\cdot (1-1)\cdot\frac{1}{4}\cdot \left((4)^{4}-\left((3)^{4}\right)\right)`

## q-126935 — original anchor

Parameters: `{"c": 1, "inner": 1, "outer": 3}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=-{x}^{4}y-\frac{1}{3}{x}^{2}{y}^{3}$ and $Q(x,y)=x{y}^{4}+\frac{1}{3}{x}^{3}{y}^{2}.$ So,

$$
\frac{∂P}{∂y}=-{x}^{4}-{x}^{2}{y}^{2},\,\frac{∂Q}{∂x}={y}^{4}+{x}^{2}{y}^{2}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}-({x}^{4}y+\frac{1}{3}{x}^{2}{y}^{3})\,dx+(x{y}^{4}+\frac{1}{3}{x}^{3}{y}^{2})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}{y}^{4}+{x}^{2}{y}^{2}-(-{x}^{4}-{x}^{2}{y}^{2})\,\text{d}A \\  & ={∬}_{D}{x}^{4}+2{x}^{2}{y}^{2}+{y}^{4}\,\text{d}A \\  & ={∬}_{D}({x}^{2}+{y}^{2})^{2}\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$
Δ={(r,\theta )\,:\,1\le r\le 3,\,0\le \theta \le 2\pi }.
$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}({x}^{2}+{y}^{2})^{2}\,\text{d}A & ={\int }_{0}^{2\pi }{\int }_{1}^{3}((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2})^{2}\cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{1}^{3}{r}^{4}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )^{2}\cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{1}^{3}{r}^{5}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }\,\text{d}\theta {\int }_{1}^{3}{r}^{5}\,\text{d}r \\  & =2\pi {\int }_{1}^{3}{r}^{5}\,\text{d}r \\  & =2\pi \cdot {\frac{1}{6}{r}^{6}|}_{1}^{3} \\  & =\frac{\pi }{3}\cdot ({3}^{6}-{1}^{6}) \\  & =\frac{728\pi }{3}.\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=- x^{4} y - \frac{x^{2} y^{3}}{3}$ and $Q(x,y)=\frac{x^{3} y^{2}}{3} + x y^{4}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- x^{4} y - \frac{x^{2} y^{3}}{3}\right)=\left(- x^{4}\right)+\left(- x^{2} y^{2}\right)=- x^{4} - x^{2} y^{2}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(\frac{x^{3} y^{2}}{3} + x y^{4}\right)=\left(y^{4}\right)+\left(x^{2} y^{2}\right)=x^{2} y^{2} + y^{4}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- x^{4} - x^{2} y^{2},\qquad\frac{\partial Q}{\partial x}=x^{2} y^{2} + y^{4}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(- x^{4} y - \frac{x^{2} y^{3}}{3})\,\mathrm dx+(\frac{x^{3} y^{2}}{3} + x y^{4})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(x^{2} y^{2} + y^{4}-(- x^{4} - x^{2} y^{2})\right)\,\mathrm dA\\ & =\iint_D(x^{4} + 2 x^{2} y^{2} + y^{4})\,\mathrm dA\\ & =\iint_D \left(x^{2} + y^{2}\right)^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$\Delta=\{(r,\theta):1\le r\le 3,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D \left(x^{2} + y^{2}\right)^{2}\,\mathrm dA & =\int_{0}^{2 \pi}\int_{1}^{3}((r\cos\theta)^2+(r\sin\theta)^2)^2\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{1}^{3}r^{4}(\cos^2\theta+\sin^2\theta)^2\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{1}^{3}r^{5}\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{1}^{3}r^{5}\,\mathrm d r\\ & =2 \pi\cdot \int_{1}^{3}r^{5}\,\mathrm d r\\ & =2 \pi\cdot \frac{r^{6}}{6}\big|_{1}^{3}\\ & =2 \pi\cdot (\left(\frac{243}{2}\right)-\left(\frac{1}{6}\right))\\ & =\frac{\pi}{3}\cdot \left((3)^{6}-\left((1)^{6}\right)\right)\\ & =\frac{\pi}{3}\cdot \left(729-\left(1\right)\right)\\ & =\frac{728 \pi}{3}.\end{aligned}
$$

Checked original operation fragments in order:

- `\int_{0}^{2 \pi}\int_{1}^{3}((r\cos\theta)^2+(r\sin\theta)^2)^2\cdot r\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\int_{1}^{3}r^{4}(\cos^2\theta+\sin^2\theta)^2\cdot r\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\int_{1}^{3}r^{5}\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{1}^{3}r^{5}\,\mathrm d r`
- `2 \pi\cdot \int_{1}^{3}r^{5}\,\mathrm d r`
- `2 \pi\cdot \frac{r^{6}}{6}\big|_{1}^{3}`
- `\frac{\pi}{3}\cdot \left((3)^{6}-\left((1)^{6}\right)\right)`

## q-126935 — changed parameters

Parameters: `{"c": -3, "inner": 3, "outer": 4}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=-{x}^{4}y-\frac{1}{3}{x}^{2}{y}^{3}$ and $Q(x,y)=x{y}^{4}+\frac{1}{3}{x}^{3}{y}^{2}.$ So,

$$
\frac{∂P}{∂y}=-{x}^{4}-{x}^{2}{y}^{2},\,\frac{∂Q}{∂x}={y}^{4}+{x}^{2}{y}^{2}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}-({x}^{4}y+\frac{1}{3}{x}^{2}{y}^{3})\,dx+(x{y}^{4}+\frac{1}{3}{x}^{3}{y}^{2})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}{y}^{4}+{x}^{2}{y}^{2}-(-{x}^{4}-{x}^{2}{y}^{2})\,\text{d}A \\  & ={∬}_{D}{x}^{4}+2{x}^{2}{y}^{2}+{y}^{4}\,\text{d}A \\  & ={∬}_{D}({x}^{2}+{y}^{2})^{2}\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$
Δ={(r,\theta )\,:\,1\le r\le 3,\,0\le \theta \le 2\pi }.
$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}({x}^{2}+{y}^{2})^{2}\,\text{d}A & ={\int }_{0}^{2\pi }{\int }_{1}^{3}((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2})^{2}\cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{1}^{3}{r}^{4}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )^{2}\cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{1}^{3}{r}^{5}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }\,\text{d}\theta {\int }_{1}^{3}{r}^{5}\,\text{d}r \\  & =2\pi {\int }_{1}^{3}{r}^{5}\,\text{d}r \\  & =2\pi \cdot {\frac{1}{6}{r}^{6}|}_{1}^{3} \\  & =\frac{\pi }{3}\cdot ({3}^{6}-{1}^{6}) \\  & =\frac{728\pi }{3}.\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=3 x^{4} y + x^{2} y^{3}$ and $Q(x,y)=- x^{3} y^{2} - 3 x y^{4}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(3 x^{4} y + x^{2} y^{3}\right)=\left(3 x^{4}\right)+\left(3 x^{2} y^{2}\right)=3 x^{4} + 3 x^{2} y^{2}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- x^{3} y^{2} - 3 x y^{4}\right)=\left(- 3 y^{4}\right)+\left(- 3 x^{2} y^{2}\right)=- 3 x^{2} y^{2} - 3 y^{4}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=3 x^{4} + 3 x^{2} y^{2},\qquad\frac{\partial Q}{\partial x}=- 3 x^{2} y^{2} - 3 y^{4}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(3 x^{4} y + x^{2} y^{3})\,\mathrm dx+(- x^{3} y^{2} - 3 x y^{4})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(- 3 x^{2} y^{2} - 3 y^{4}-(3 x^{4} + 3 x^{2} y^{2})\right)\,\mathrm dA\\ & =\iint_D(- 3 x^{4} - 6 x^{2} y^{2} - 3 y^{4})\,\mathrm dA\\ & =\iint_D - 3 \left(x^{2} + y^{2}\right)^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$\Delta=\{(r,\theta):3\le r\le 4,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 3 \left(x^{2} + y^{2}\right)^{2}\,\mathrm dA & =\int_{0}^{2 \pi}\int_{3}^{4}-3\left(((r\cos\theta)^2+(r\sin\theta)^2)^2\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}-3\left(r^{4}(\cos^2\theta+\sin^2\theta)^2\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}- 3 r^{5}\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{3}^{4}- 3 r^{5}\,\mathrm d r\\ & =- 6 \pi\cdot \int_{3}^{4}r^{5}\,\mathrm d r\\ & =- 6 \pi\cdot \frac{r^{6}}{6}\big|_{3}^{4}\\ & =- 6 \pi\cdot (\left(\frac{2048}{3}\right)-\left(\frac{243}{2}\right))\\ & =-3\cdot\left(\frac{\pi}{3}\right)\cdot \left((4)^{6}-\left((3)^{6}\right)\right)\\ & =- \pi\cdot \left(4096-\left(729\right)\right)\\ & =- 3367 \pi.\end{aligned}
$$

Checked original operation fragments in order:

- `\int_{0}^{2 \pi}\int_{3}^{4}-3\left(((r\cos\theta)^2+(r\sin\theta)^2)^2\cdot r\right)\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\int_{3}^{4}-3\left(r^{4}(\cos^2\theta+\sin^2\theta)^2\cdot r\right)\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\int_{3}^{4}- 3 r^{5}\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{3}^{4}- 3 r^{5}\,\mathrm d r`
- `- 6 \pi\cdot \int_{3}^{4}r^{5}\,\mathrm d r`
- `- 6 \pi\cdot \frac{r^{6}}{6}\big|_{3}^{4}`
- `-3\cdot\left(\frac{\pi}{3}\right)\cdot \left((4)^{6}-\left((3)^{6}\right)\right)`

## q-126937 — original anchor

Parameters: `{"c": 1, "inner": 2, "outer": 4}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=\frac{1}{3}{y}^{3}+\operatorname{cos}⁡x$ and $Q(x,y)=\operatorname{ln}⁡({sin}^{2}⁡y)-\frac{1}{3}{x}^{3}.$ So,

$$
\frac{∂P}{∂y}={y}^{2},\,\frac{∂Q}{∂x}=-{x}^{2}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}(\frac{1}{3}{y}^{3}+\operatorname{cos}⁡x)\,dx+(\operatorname{ln}⁡({sin}^{2}⁡y)-\frac{1}{3}{x}^{3})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}-{x}^{2}-{y}^{2}\,\text{d}A \\  & ={∬}_{D}-({x}^{2}+{y}^{2})\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$
Δ={(r,\theta )\,:\,2\le r\le 4,\,0\le \theta \le 2\pi }.
$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}-({x}^{2}+{y}^{2})\,\text{d}A & ={\int }_{0}^{2\pi }{\int }_{2}^{4}-((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2})\cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{2}^{4}-{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{2}^{4}-{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }\,\text{d}\theta {\int }_{2}^{4}-{r}^{3}\,\text{d}r \\  & =-2\pi {\int }_{2}^{4}{r}^{3}\,\text{d}r \\  & =-2\pi \cdot {\frac{1}{4}{r}^{4}|}_{2}^{4} \\  & =-\frac{\pi }{2}\cdot ({4}^{4}-{2}^{4}) \\  & =-120\pi .\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=\frac{y^{3}}{3} + \cos{\left(x \right)}$ and $Q(x,y)=- \frac{x^{3}}{3} + \ln{\left(\sin^{2}{\left(y \right)} + 1 \right)}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(\frac{y^{3}}{3} + \cos{\left(x \right)}\right)=\left(y^{2}\right)+\left(0\right)=y^{2}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- \frac{x^{3}}{3} + \ln{\left(\sin^{2}{\left(y \right)} + 1 \right)}\right)=\left(- x^{2}\right)+\left(0\right)=- x^{2}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=y^{2},\qquad\frac{\partial Q}{\partial x}=- x^{2}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(\frac{y^{3}}{3} + \cos{\left(x \right)})\,\mathrm dx+(- \frac{x^{3}}{3} + \ln{\left(\sin^{2}{\left(y \right)} + 1 \right)})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(- x^{2}-(y^{2})\right)\,\mathrm dA\\ & =\iint_D(- x^{2} - y^{2})\,\mathrm dA\\ & =\iint_D - x^{2} - y^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$\Delta=\{(r,\theta):2\le r\le 4,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - x^{2} - y^{2}\,\mathrm dA & =\int_{0}^{2 \pi}\int_{2}^{4}-1\left(((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{2}^{4}-1\left(r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{2}^{4}- r^{3}\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{2}^{4}- r^{3}\,\mathrm d r\\ & =- 2 \pi\cdot \int_{2}^{4}r^{3}\,\mathrm d r\\ & =- 2 \pi\cdot \frac{r^{4}}{4}\big|_{2}^{4}\\ & =- 2 \pi\cdot (\left(64\right)-\left(4\right))\\ & =- \frac{\pi}{2}\cdot \left((4)^{4}-\left((2)^{4}\right)\right)\\ & =- \frac{\pi}{2}\cdot \left(256-\left(16\right)\right)\\ & =- 120 \pi.\end{aligned}
$$

Checked original operation fragments in order:

- `\int_{0}^{2 \pi}\int_{2}^{4}-1\left(((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\right)\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\int_{2}^{4}-1\left(r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\right)\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\int_{2}^{4}- r^{3}\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{2}^{4}- r^{3}\,\mathrm d r`
- `- 2 \pi\cdot \int_{2}^{4}r^{3}\,\mathrm d r`
- `- 2 \pi\cdot \frac{r^{4}}{4}\big|_{2}^{4}`
- `- \frac{\pi}{2}\cdot \left((4)^{4}-\left((2)^{4}\right)\right)`

## q-126937 — changed parameters

Parameters: `{"c": -3, "inner": 3, "outer": 4}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=\frac{1}{3}{y}^{3}+\operatorname{cos}⁡x$ and $Q(x,y)=\operatorname{ln}⁡({sin}^{2}⁡y)-\frac{1}{3}{x}^{3}.$ So,

$$
\frac{∂P}{∂y}={y}^{2},\,\frac{∂Q}{∂x}=-{x}^{2}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}(\frac{1}{3}{y}^{3}+\operatorname{cos}⁡x)\,dx+(\operatorname{ln}⁡({sin}^{2}⁡y)-\frac{1}{3}{x}^{3})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}-{x}^{2}-{y}^{2}\,\text{d}A \\  & ={∬}_{D}-({x}^{2}+{y}^{2})\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$
Δ={(r,\theta )\,:\,2\le r\le 4,\,0\le \theta \le 2\pi }.
$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}-({x}^{2}+{y}^{2})\,\text{d}A & ={\int }_{0}^{2\pi }{\int }_{2}^{4}-((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2})\cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{2}^{4}-{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{2}^{4}-{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }\,\text{d}\theta {\int }_{2}^{4}-{r}^{3}\,\text{d}r \\  & =-2\pi {\int }_{2}^{4}{r}^{3}\,\text{d}r \\  & =-2\pi \cdot {\frac{1}{4}{r}^{4}|}_{2}^{4} \\  & =-\frac{\pi }{2}\cdot ({4}^{4}-{2}^{4}) \\  & =-120\pi .\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=- y^{3} - 3 \cos{\left(x \right)}$ and $Q(x,y)=x^{3} - 3 \ln{\left(\sin^{2}{\left(y \right)} + 1 \right)}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- y^{3} - 3 \cos{\left(x \right)}\right)=\left(- 3 y^{2}\right)+\left(0\right)=- 3 y^{2}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(x^{3} - 3 \ln{\left(\sin^{2}{\left(y \right)} + 1 \right)}\right)=\left(3 x^{2}\right)+\left(0\right)=3 x^{2}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- 3 y^{2},\qquad\frac{\partial Q}{\partial x}=3 x^{2}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(- y^{3} - 3 \cos{\left(x \right)})\,\mathrm dx+(x^{3} - 3 \ln{\left(\sin^{2}{\left(y \right)} + 1 \right)})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(3 x^{2}-(- 3 y^{2})\right)\,\mathrm dA\\ & =\iint_D(3 x^{2} + 3 y^{2})\,\mathrm dA\\ & =\iint_D 3 \left(x^{2} + y^{2}\right)\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$\Delta=\{(r,\theta):3\le r\le 4,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D 3 \left(x^{2} + y^{2}\right)\,\mathrm dA & =\int_{0}^{2 \pi}\int_{3}^{4}3\left(((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}3\left(r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\right)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}3 r^{3}\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{3}^{4}3 r^{3}\,\mathrm d r\\ & =6 \pi\cdot \int_{3}^{4}r^{3}\,\mathrm d r\\ & =6 \pi\cdot \frac{r^{4}}{4}\big|_{3}^{4}\\ & =6 \pi\cdot (\left(64\right)-\left(\frac{81}{4}\right))\\ & =-3\cdot\left(- \frac{\pi}{2}\right)\cdot \left((4)^{4}-\left((3)^{4}\right)\right)\\ & =\frac{3 \pi}{2}\cdot \left(256-\left(81\right)\right)\\ & =\frac{525 \pi}{2}.\end{aligned}
$$

Checked original operation fragments in order:

- `\int_{0}^{2 \pi}\int_{3}^{4}3\left(((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\right)\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\int_{3}^{4}3\left(r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\right)\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\int_{3}^{4}3 r^{3}\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{3}^{4}3 r^{3}\,\mathrm d r`
- `6 \pi\cdot \int_{3}^{4}r^{3}\,\mathrm d r`
- `6 \pi\cdot \frac{r^{4}}{4}\big|_{3}^{4}`
- `-3\cdot\left(- \frac{\pi}{2}\right)\cdot \left((4)^{4}-\left((3)^{4}\right)\right)`

## q-126941 — original anchor

Parameters: `{"c": 1, "hole": [0, 1, 0, 1], "outer": [-2, 2, -1, 2]}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)={x}^{3}{y}^{3}+x$ and $Q(x,y)={x}^{4}{y}^{2}-y.$ Therefore,

$$
\frac{∂P}{∂y}=3{x}^{3}{y}^{2},\,\frac{∂Q}{∂x}=4{x}^{3}{y}^{2}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}({x}^{3}{y}^{3}+x)\,dx+({x}^{4}{y}^{2}-y)\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}4{x}^{3}{y}^{2}-3{x}^{3}{y}^{2}\,\text{d}A \\  & ={∬}_{D}{x}^{3}{y}^{2}\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as ${Δ}_{1}∖{Δ}_{2},$ where

- ${Δ}_{1}={(x,y)\,:\,-2\le x\le 2,-1\le y\le 2}$ is the region enclosed by the outer curve, and

- ${Δ}_{2}={(x,y)\,:\,0\le x\le 1,0\le y\le 1}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}{x}^{3}{y}^{2}\,\text{d}A & ={∬}_{{Δ}_{1}}{x}^{3}{y}^{2}\,\text{d}A-{∬}_{{Δ}_{2}}{x}^{3}{y}^{2}\,\text{d}A \\  & ={\int }_{-1}^{2}{\int }_{-2}^{2}{x}^{3}{y}^{2}\,\text{d}x\,\text{d}y-{\int }_{0}^{1}{\int }_{0}^{1}{x}^{3}{y}^{2}\,\text{d}x\,\text{d}y \\  & ={\int }_{-2}^{2}{x}^{3}\,\text{d}x{\int }_{-1}^{2}{y}^{2}\,\text{d}y-{\int }_{0}^{1}{x}^{3}\,\text{d}x{\int }_{0}^{1}{y}^{2}\,\text{d}y \\  & =\frac{{x}^{4}}{4}\,{|}_{-2}^{2}\cdot \frac{{y}^{3}}{3}\,{|}_{-1}^{2}-\frac{{x}^{4}}{4}\,{|}_{0}^{1}\cdot \frac{{y}^{3}}{3}\,{|}_{0}^{1} \\  & =(4-4)\cdot (\frac{8}{3}-(-\frac{1}{3}))-(\frac{1}{4}-0)\cdot (\frac{1}{3}-0) \\  & =0\cdot 3-\frac{1}{4}\cdot \frac{1}{3} \\  & =-\frac{1}{12}.\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=x^{3} y^{3} + x$ and $Q(x,y)=x^{4} y^{2} - y.$ Therefore,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(x^{3} y^{3} + x\right)=\left(0\right)+\left(3 x^{3} y^{2}\right)=3 x^{3} y^{2}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(x^{4} y^{2} - y\right)=\left(0\right)+\left(4 x^{3} y^{2}\right)=4 x^{3} y^{2}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=3 x^{3} y^{2},\qquad\frac{\partial Q}{\partial x}=4 x^{3} y^{2}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(x^{3} y^{3} + x)\,\mathrm dx+(x^{4} y^{2} - y)\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(4 x^{3} y^{2}-(3 x^{3} y^{2})\right)\,\mathrm dA\\ & =\iint_D x^{3} y^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as $\Delta_1\setminus\Delta_2,$ where

- $\Delta_1=\{(x,y):-2\le x\le 2,-1\le y\le 2\}$ is the region enclosed by the outer curve, and

- $\Delta_2=\{(x,y):0\le x\le 1,0\le y\le 1\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D x^{3} y^{2}\,\mathrm dA & =\iint_{\Delta_1}x^{3} y^{2}\,\mathrm dA-\iint_{\Delta_2}x^{3} y^{2}\,\mathrm dA\\ & =\int_{-1}^{2}\int_{-2}^{2}x^{3} y^{2}\,\mathrm d x\,\mathrm d y-\int_{0}^{1}\int_{0}^{1}x^{3} y^{2}\,\mathrm d x\,\mathrm d y\\ & =\int_{-2}^{2}x^{3}\,\mathrm d x\cdot \int_{-1}^{2}y^{2}\,\mathrm d y-\int_{0}^{1}x^{3}\,\mathrm d x\cdot \int_{0}^{1}y^{2}\,\mathrm d y\\ & =\frac{x^4}{4}\big|_{-2}^{2}\cdot \frac{y^3}{3}\big|_{-1}^{2}-\frac{x^4}{4}\big|_{0}^{1}\cdot \frac{y^3}{3}\big|_{0}^{1}\\ & =(\left(4\right)-\left(4\right))\cdot (\left(\frac{8}{3}\right)-\left(- \frac{1}{3}\right))-(\left(\frac{1}{4}\right)-\left(0\right))\cdot (\left(\frac{1}{3}\right)-\left(0\right))\\ & =\left(0\right)\cdot \left(3\right)-\left(\frac{1}{4}\right)\cdot \left(\frac{1}{3}\right)\\ & =- \frac{1}{12}.\end{aligned}
$$

Checked original operation fragments in order:

- `\iint_{\Delta_1}x^{3} y^{2}\,\mathrm dA-\iint_{\Delta_2}x^{3} y^{2}\,\mathrm dA`
- `\int_{-1}^{2}\int_{-2}^{2}x^{3} y^{2}\,\mathrm d x\,\mathrm d y-\int_{0}^{1}\int_{0}^{1}x^{3} y^{2}\,\mathrm d x\,\mathrm d y`
- `\int_{-2}^{2}x^{3}\,\mathrm d x\cdot \int_{-1}^{2}y^{2}\,\mathrm d y-\int_{0}^{1}x^{3}\,\mathrm d x\cdot \int_{0}^{1}y^{2}\,\mathrm d y`
- `\frac{x^4}{4}\big|_{-2}^{2}\cdot \frac{y^3}{3}\big|_{-1}^{2}-\frac{x^4}{4}\big|_{0}^{1}\cdot \frac{y^3}{3}\big|_{0}^{1}`
- `(\left(4\right)-\left(4\right))\cdot (\left(\frac{8}{3}\right)-\left(- \frac{1}{3}\right))-(\left(\frac{1}{4}\right)-\left(0\right))\cdot (\left(\frac{1}{3}\right)-\left(0\right))`
- `\left(0\right)\cdot \left(3\right)-\left(\frac{1}{4}\right)\cdot \left(\frac{1}{3}\right)`

## q-126941 — changed parameters

Parameters: `{"c": -3, "hole": [1, 2, -1, 0], "outer": [-1, 3, -2, 1]}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)={x}^{3}{y}^{3}+x$ and $Q(x,y)={x}^{4}{y}^{2}-y.$ Therefore,

$$
\frac{∂P}{∂y}=3{x}^{3}{y}^{2},\,\frac{∂Q}{∂x}=4{x}^{3}{y}^{2}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}({x}^{3}{y}^{3}+x)\,dx+({x}^{4}{y}^{2}-y)\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}4{x}^{3}{y}^{2}-3{x}^{3}{y}^{2}\,\text{d}A \\  & ={∬}_{D}{x}^{3}{y}^{2}\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as ${Δ}_{1}∖{Δ}_{2},$ where

- ${Δ}_{1}={(x,y)\,:\,-2\le x\le 2,-1\le y\le 2}$ is the region enclosed by the outer curve, and

- ${Δ}_{2}={(x,y)\,:\,0\le x\le 1,0\le y\le 1}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}{x}^{3}{y}^{2}\,\text{d}A & ={∬}_{{Δ}_{1}}{x}^{3}{y}^{2}\,\text{d}A-{∬}_{{Δ}_{2}}{x}^{3}{y}^{2}\,\text{d}A \\  & ={\int }_{-1}^{2}{\int }_{-2}^{2}{x}^{3}{y}^{2}\,\text{d}x\,\text{d}y-{\int }_{0}^{1}{\int }_{0}^{1}{x}^{3}{y}^{2}\,\text{d}x\,\text{d}y \\  & ={\int }_{-2}^{2}{x}^{3}\,\text{d}x{\int }_{-1}^{2}{y}^{2}\,\text{d}y-{\int }_{0}^{1}{x}^{3}\,\text{d}x{\int }_{0}^{1}{y}^{2}\,\text{d}y \\  & =\frac{{x}^{4}}{4}\,{|}_{-2}^{2}\cdot \frac{{y}^{3}}{3}\,{|}_{-1}^{2}-\frac{{x}^{4}}{4}\,{|}_{0}^{1}\cdot \frac{{y}^{3}}{3}\,{|}_{0}^{1} \\  & =(4-4)\cdot (\frac{8}{3}-(-\frac{1}{3}))-(\frac{1}{4}-0)\cdot (\frac{1}{3}-0) \\  & =0\cdot 3-\frac{1}{4}\cdot \frac{1}{3} \\  & =-\frac{1}{12}.\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=- 3 x^{3} y^{3} - 3 x$ and $Q(x,y)=- 3 x^{4} y^{2} + 3 y.$ Therefore,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- 3 x^{3} y^{3} - 3 x\right)=\left(0\right)+\left(- 9 x^{3} y^{2}\right)=- 9 x^{3} y^{2}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- 3 x^{4} y^{2} + 3 y\right)=\left(0\right)+\left(- 12 x^{3} y^{2}\right)=- 12 x^{3} y^{2}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- 9 x^{3} y^{2},\qquad\frac{\partial Q}{\partial x}=- 12 x^{3} y^{2}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(- 3 x^{3} y^{3} - 3 x)\,\mathrm dx+(- 3 x^{4} y^{2} + 3 y)\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(- 12 x^{3} y^{2}-(- 9 x^{3} y^{2})\right)\,\mathrm dA\\ & =\iint_D - 3 x^{3} y^{2}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as $\Delta_1\setminus\Delta_2,$ where

- $\Delta_1=\{(x,y):-1\le x\le 3,-2\le y\le 1\}$ is the region enclosed by the outer curve, and

- $\Delta_2=\{(x,y):1\le x\le 2,-1\le y\le 0\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 3 x^{3} y^{2}\,\mathrm dA & =\iint_{\Delta_1}- 3 x^{3} y^{2}\,\mathrm dA-\iint_{\Delta_2}- 3 x^{3} y^{2}\,\mathrm dA\\ & =\int_{-2}^{1}\int_{-1}^{3}- 3 x^{3} y^{2}\,\mathrm d x\,\mathrm d y-\int_{-1}^{0}\int_{1}^{2}- 3 x^{3} y^{2}\,\mathrm d x\,\mathrm d y\\ & =\int_{-1}^{3}- 3 x^{3}\,\mathrm d x\cdot \int_{-2}^{1}y^{2}\,\mathrm d y-\int_{1}^{2}- 3 x^{3}\,\mathrm d x\cdot \int_{-1}^{0}y^{2}\,\mathrm d y\\ & =\frac{-3x^4}{4}\big|_{-1}^{3}\cdot \frac{y^3}{3}\big|_{-2}^{1}-\frac{-3x^4}{4}\big|_{1}^{2}\cdot \frac{y^3}{3}\big|_{-1}^{0}\\ & =(\left(- \frac{243}{4}\right)-\left(- \frac{3}{4}\right))\cdot (\left(\frac{1}{3}\right)-\left(- \frac{8}{3}\right))-(\left(-12\right)-\left(- \frac{3}{4}\right))\cdot (\left(0\right)-\left(- \frac{1}{3}\right))\\ & =\left(-60\right)\cdot \left(3\right)-\left(- \frac{45}{4}\right)\cdot \left(\frac{1}{3}\right)\\ & =- \frac{705}{4}.\end{aligned}
$$

Checked original operation fragments in order:

- `\iint_{\Delta_1}- 3 x^{3} y^{2}\,\mathrm dA-\iint_{\Delta_2}- 3 x^{3} y^{2}\,\mathrm dA`
- `\int_{-2}^{1}\int_{-1}^{3}- 3 x^{3} y^{2}\,\mathrm d x\,\mathrm d y-\int_{-1}^{0}\int_{1}^{2}- 3 x^{3} y^{2}\,\mathrm d x\,\mathrm d y`
- `\int_{-1}^{3}- 3 x^{3}\,\mathrm d x\cdot \int_{-2}^{1}y^{2}\,\mathrm d y-\int_{1}^{2}- 3 x^{3}\,\mathrm d x\cdot \int_{-1}^{0}y^{2}\,\mathrm d y`
- `\frac{-3x^4}{4}\big|_{-1}^{3}\cdot \frac{y^3}{3}\big|_{-2}^{1}-\frac{-3x^4}{4}\big|_{1}^{2}\cdot \frac{y^3}{3}\big|_{-1}^{0}`
- `(\left(- \frac{243}{4}\right)-\left(- \frac{3}{4}\right))\cdot (\left(\frac{1}{3}\right)-\left(- \frac{8}{3}\right))-(\left(-12\right)-\left(- \frac{3}{4}\right))\cdot (\left(0\right)-\left(- \frac{1}{3}\right))`
- `\left(-60\right)\cdot \left(3\right)-\left(- \frac{45}{4}\right)\cdot \left(\frac{1}{3}\right)`

## q-126945 — original anchor

Parameters: `{"c": 1, "hole": [-1, 1, 0, 1], "outer": [-2, 2, -1, 2]}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=x{y}^{2}+{x}^{3}$ and $Q(x,y)=2{x}^{2}y-{y}^{3}.$ Therefore,

$$
\frac{∂P}{∂y}=2xy,\,\frac{∂Q}{∂x}=4xy.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}(x{y}^{2}+{x}^{3})\,dx+(2{x}^{2}y-{y}^{3})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & ={∬}_{D}4xy-2xy\,\text{d}A \\  & ={∬}_{D}2xy\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as ${Δ}_{1}∖{Δ}_{2},$ where

- ${Δ}_{1}={(x,y)\,:\,-2\le x\le 2,-1\le y\le 2}$ is the region enclosed by the outer curve, and

- ${Δ}_{2}={(x,y)\,:\,-1\le x\le 1,0\le y\le 1}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}2xy\,\text{d}A & ={∬}_{{Δ}_{1}}2xy\,\text{d}A-{∬}_{{Δ}_{2}}2xy\,\text{d}A \\  & ={\int }_{-1}^{2}{\int }_{-2}^{2}2xy\,\text{d}x\,\text{d}y-{\int }_{0}^{1}{\int }_{-1}^{1}2xy\,\text{d}x\,\text{d}y \\  & ={\int }_{-2}^{2}2x\,\text{d}x{\int }_{-1}^{2}y\,\text{d}y-{\int }_{-1}^{1}2x\,\text{d}x{\int }_{0}^{1}y\,\text{d}y \\  & ={x}^{2}\,{|}_{-2}^{2}\cdot \frac{{y}^{2}}{2}\,{|}_{-1}^{2}-{x}^{2}\,{|}_{-1}^{1}\cdot \frac{{y}^{2}}{2}\,{|}_{0}^{1} \\  & =(4-4)\cdot (2-\frac{1}{2})-(1-1)\cdot (\frac{1}{2}-0) \\  & =0\cdot \frac{3}{2}-0\cdot \frac{1}{2} \\  & =0.\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=x^{3} + x y^{2}$ and $Q(x,y)=2 x^{2} y - y^{3}.$ Therefore,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(x^{3} + x y^{2}\right)=\left(0\right)+\left(2 x y\right)=2 x y\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(2 x^{2} y - y^{3}\right)=\left(0\right)+\left(4 x y\right)=4 x y.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=2 x y,\qquad\frac{\partial Q}{\partial x}=4 x y.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(x^{3} + x y^{2})\,\mathrm dx+(2 x^{2} y - y^{3})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(4 x y-(2 x y)\right)\,\mathrm dA\\ & =\iint_D 2 x y\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as $\Delta_1\setminus\Delta_2,$ where

- $\Delta_1=\{(x,y):-2\le x\le 2,-1\le y\le 2\}$ is the region enclosed by the outer curve, and

- $\Delta_2=\{(x,y):-1\le x\le 1,0\le y\le 1\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D 2 x y\,\mathrm dA & =\iint_{\Delta_1}2 x y\,\mathrm dA-\iint_{\Delta_2}2 x y\,\mathrm dA\\ & =\int_{-1}^{2}\int_{-2}^{2}2 x y\,\mathrm d x\,\mathrm d y-\int_{0}^{1}\int_{-1}^{1}2 x y\,\mathrm d x\,\mathrm d y\\ & =\int_{-2}^{2}2 x\,\mathrm d x\cdot \int_{-1}^{2}y\,\mathrm d y-\int_{-1}^{1}2 x\,\mathrm d x\cdot \int_{0}^{1}y\,\mathrm d y\\ & =x^{2}\big|_{-2}^{2}\cdot \frac{y^2}{2}\big|_{-1}^{2}-x^{2}\big|_{-1}^{1}\cdot \frac{y^2}{2}\big|_{0}^{1}\\ & =(\left(4\right)-\left(4\right))\cdot (\left(2\right)-\left(\frac{1}{2}\right))-(\left(1\right)-\left(1\right))\cdot (\left(\frac{1}{2}\right)-\left(0\right))\\ & =\left(0\right)\cdot \left(\frac{3}{2}\right)-\left(0\right)\cdot \left(\frac{1}{2}\right)\\ & =0.\end{aligned}
$$

Checked original operation fragments in order:

- `\iint_{\Delta_1}2 x y\,\mathrm dA-\iint_{\Delta_2}2 x y\,\mathrm dA`
- `\int_{-1}^{2}\int_{-2}^{2}2 x y\,\mathrm d x\,\mathrm d y-\int_{0}^{1}\int_{-1}^{1}2 x y\,\mathrm d x\,\mathrm d y`
- `\int_{-2}^{2}2 x\,\mathrm d x\cdot \int_{-1}^{2}y\,\mathrm d y-\int_{-1}^{1}2 x\,\mathrm d x\cdot \int_{0}^{1}y\,\mathrm d y`
- `x^{2}\big|_{-2}^{2}\cdot \frac{y^2}{2}\big|_{-1}^{2}-x^{2}\big|_{-1}^{1}\cdot \frac{y^2}{2}\big|_{0}^{1}`
- `(\left(4\right)-\left(4\right))\cdot (\left(2\right)-\left(\frac{1}{2}\right))-(\left(1\right)-\left(1\right))\cdot (\left(\frac{1}{2}\right)-\left(0\right))`
- `\left(0\right)\cdot \left(\frac{3}{2}\right)-\left(0\right)\cdot \left(\frac{1}{2}\right)`

## q-126945 — changed parameters

Parameters: `{"c": -3, "hole": [0, 2, -1, 0], "outer": [-1, 3, -2, 1]}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=x{y}^{2}+{x}^{3}$ and $Q(x,y)=2{x}^{2}y-{y}^{3}.$ Therefore,

$$
\frac{∂P}{∂y}=2xy,\,\frac{∂Q}{∂x}=4xy.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}(x{y}^{2}+{x}^{3})\,dx+(2{x}^{2}y-{y}^{3})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\text{d}A \\  & ={∬}_{D}4xy-2xy\,\text{d}A \\  & ={∬}_{D}2xy\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as ${Δ}_{1}∖{Δ}_{2},$ where

- ${Δ}_{1}={(x,y)\,:\,-2\le x\le 2,-1\le y\le 2}$ is the region enclosed by the outer curve, and

- ${Δ}_{2}={(x,y)\,:\,-1\le x\le 1,0\le y\le 1}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}2xy\,\text{d}A & ={∬}_{{Δ}_{1}}2xy\,\text{d}A-{∬}_{{Δ}_{2}}2xy\,\text{d}A \\  & ={\int }_{-1}^{2}{\int }_{-2}^{2}2xy\,\text{d}x\,\text{d}y-{\int }_{0}^{1}{\int }_{-1}^{1}2xy\,\text{d}x\,\text{d}y \\  & ={\int }_{-2}^{2}2x\,\text{d}x{\int }_{-1}^{2}y\,\text{d}y-{\int }_{-1}^{1}2x\,\text{d}x{\int }_{0}^{1}y\,\text{d}y \\  & ={x}^{2}\,{|}_{-2}^{2}\cdot \frac{{y}^{2}}{2}\,{|}_{-1}^{2}-{x}^{2}\,{|}_{-1}^{1}\cdot \frac{{y}^{2}}{2}\,{|}_{0}^{1} \\  & =(4-4)\cdot (2-\frac{1}{2})-(1-1)\cdot (\frac{1}{2}-0) \\  & =0\cdot \frac{3}{2}-0\cdot \frac{1}{2} \\  & =0.\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=- 3 x^{3} - 3 x y^{2}$ and $Q(x,y)=- 6 x^{2} y + 3 y^{3}.$ Therefore,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- 3 x^{3} - 3 x y^{2}\right)=\left(0\right)+\left(- 6 x y\right)=- 6 x y\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- 6 x^{2} y + 3 y^{3}\right)=\left(0\right)+\left(- 12 x y\right)=- 12 x y.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- 6 x y,\qquad\frac{\partial Q}{\partial x}=- 12 x y.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(- 3 x^{3} - 3 x y^{2})\,\mathrm dx+(- 6 x^{2} y + 3 y^{3})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(- 12 x y-(- 6 x y)\right)\,\mathrm dA\\ & =\iint_D - 6 x y\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as $\Delta_1\setminus\Delta_2,$ where

- $\Delta_1=\{(x,y):-1\le x\le 3,-2\le y\le 1\}$ is the region enclosed by the outer curve, and

- $\Delta_2=\{(x,y):0\le x\le 2,-1\le y\le 0\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 6 x y\,\mathrm dA & =\iint_{\Delta_1}- 6 x y\,\mathrm dA-\iint_{\Delta_2}- 6 x y\,\mathrm dA\\ & =\int_{-2}^{1}\int_{-1}^{3}- 6 x y\,\mathrm d x\,\mathrm d y-\int_{-1}^{0}\int_{0}^{2}- 6 x y\,\mathrm d x\,\mathrm d y\\ & =\int_{-1}^{3}- 6 x\,\mathrm d x\cdot \int_{-2}^{1}y\,\mathrm d y-\int_{0}^{2}- 6 x\,\mathrm d x\cdot \int_{-1}^{0}y\,\mathrm d y\\ & =- 3 x^{2}\big|_{-1}^{3}\cdot \frac{y^2}{2}\big|_{-2}^{1}-- 3 x^{2}\big|_{0}^{2}\cdot \frac{y^2}{2}\big|_{-1}^{0}\\ & =(\left(-27\right)-\left(-3\right))\cdot (\left(\frac{1}{2}\right)-\left(2\right))-(\left(-12\right)-\left(0\right))\cdot (\left(0\right)-\left(\frac{1}{2}\right))\\ & =\left(-24\right)\cdot \left(- \frac{3}{2}\right)-\left(-12\right)\cdot \left(- \frac{1}{2}\right)\\ & =30.\end{aligned}
$$

Checked original operation fragments in order:

- `\iint_{\Delta_1}- 6 x y\,\mathrm dA-\iint_{\Delta_2}- 6 x y\,\mathrm dA`
- `\int_{-2}^{1}\int_{-1}^{3}- 6 x y\,\mathrm d x\,\mathrm d y-\int_{-1}^{0}\int_{0}^{2}- 6 x y\,\mathrm d x\,\mathrm d y`
- `\int_{-1}^{3}- 6 x\,\mathrm d x\cdot \int_{-2}^{1}y\,\mathrm d y-\int_{0}^{2}- 6 x\,\mathrm d x\cdot \int_{-1}^{0}y\,\mathrm d y`
- `- 3 x^{2}\big|_{-1}^{3}\cdot \frac{y^2}{2}\big|_{-2}^{1}-- 3 x^{2}\big|_{0}^{2}\cdot \frac{y^2}{2}\big|_{-1}^{0}`
- `(\left(-27\right)-\left(-3\right))\cdot (\left(\frac{1}{2}\right)-\left(2\right))-(\left(-12\right)-\left(0\right))\cdot (\left(0\right)-\left(\frac{1}{2}\right))`
- `\left(-24\right)\cdot \left(- \frac{3}{2}\right)-\left(-12\right)\cdot \left(- \frac{1}{2}\right)`

## q-126939 — original anchor

Parameters: `{"c": 1, "inner": 1, "outer": 4}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)={x}^{2}-{y}^{4}$ and $Q(x,y)=({x}^{3}y-x{y}^{3}).$ So,

$$
\frac{∂P}{∂y}=-4{y}^{3},\,\frac{∂Q}{∂x}=3{x}^{2}y-{y}^{3}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}({x}^{2}-{y}^{4})\,dx+({x}^{3}y-x{y}^{3})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}3{x}^{2}y-{y}^{3}-(-4{y}^{3})\,\text{d}A \\  & ={∬}_{D}3{x}^{2}y+3{y}^{3}\,\text{d}A \\  & ={∬}_{D}3y({x}^{2}+{y}^{2})\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$
Δ=\{(r,\theta )\,:\,1\le r\le 4,\,0\le \theta \le 2\pi \}.
$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}3y({x}^{2}+{y}^{2})\,\text{d}A & ={\int }_{0}^{2\pi }{\int }_{1}^{4}3\cdot r\operatorname{sin}⁡\theta \cdot ((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2})\cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{1}^{4}3{r}^{2}\operatorname{sin}⁡\theta \cdot {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{1}^{4}3{r}^{4}\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }\operatorname{sin}⁡\theta \,\text{d}\theta {\int }_{1}^{4}3{r}^{4}\,\text{d}r \\  & =\operatorname{cos}⁡\theta \,{|}_{0}^{2\pi }\cdot \frac{3{r}^{5}}{5}\,{|}_{1}^{4} \\  & =(\operatorname{cos}⁡(2\pi )-\operatorname{cos}⁡(0))\cdot (\frac{3(4)^{5}}{5}-\frac{3(1)^{5}}{5}) \\  & =(1-1)\cdot (\frac{3(4)^{5}}{5}-\frac{3(1)^{5}}{5}) \\  & =0.\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=x^{2} - y^{4}$ and $Q(x,y)=x^{3} y - x y^{3}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(x^{2} - y^{4}\right)=\left(0\right)+\left(- 4 y^{3}\right)=- 4 y^{3}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(x^{3} y - x y^{3}\right)=\left(3 x^{2} y\right)+\left(- y^{3}\right)=3 x^{2} y - y^{3}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- 4 y^{3},\qquad\frac{\partial Q}{\partial x}=3 x^{2} y - y^{3}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(x^{2} - y^{4})\,\mathrm dx+(x^{3} y - x y^{3})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(3 x^{2} y - y^{3}-(- 4 y^{3})\right)\,\mathrm dA\\ & =\iint_D(3 x^{2} y + 3 y^{3})\,\mathrm dA\\ & =\iint_D 3 y \left(x^{2} + y^{2}\right)\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$\Delta=\{(r,\theta):1\le r\le 4,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D 3 y \left(x^{2} + y^{2}\right)\,\mathrm dA & =\int_{0}^{2 \pi}\int_{1}^{4}3\cdot r\sin\theta\cdot ((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{1}^{4}3r^2\sin\theta\cdot r^2(\cos^2\theta+\sin^2\theta)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{1}^{4}3r^4\sin\theta\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\sin\theta\,\mathrm d \theta\cdot \int_{1}^{4}3r^4\,\mathrm d r\\ & =-\cos\theta\big|_{0}^{2 \pi}\cdot \frac{3r^5}{5}\big|_{1}^{4}\\ & =\left(-\cos(2\pi)-\left(-\cos(0)\right)\right)\cdot \left(\frac{3\cdot (4)^{5}}{5}-\left(\frac{3\cdot (1)^{5}}{5}\right)\right)\\ & =\left(-1-\left(-1\right)\right)\cdot \left(\frac{3\cdot (4)^{5}}{5}-\left(\frac{3\cdot (1)^{5}}{5}\right)\right)\\ & =(\left(-1\right)-\left(-1\right))\cdot (\left(\frac{3072}{5}\right)-\left(\frac{3}{5}\right))\\ & =0.\end{aligned}
$$

Checked original operation fragments in order:

- `\int_{0}^{2 \pi}\int_{1}^{4}3\cdot r\sin\theta\cdot ((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\int_{1}^{4}3r^2\sin\theta\cdot r^2(\cos^2\theta+\sin^2\theta)\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\int_{1}^{4}3r^4\sin\theta\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\sin\theta\,\mathrm d \theta\cdot \int_{1}^{4}3r^4\,\mathrm d r`
- `-\cos\theta\big|_{0}^{2 \pi}\cdot \frac{3r^5}{5}\big|_{1}^{4}`
- `\left(-\cos(2\pi)-\left(-\cos(0)\right)\right)\cdot \left(\frac{3\cdot (4)^{5}}{5}-\left(\frac{3\cdot (1)^{5}}{5}\right)\right)`
- `\left(-1-\left(-1\right)\right)\cdot \left(\frac{3\cdot (4)^{5}}{5}-\left(\frac{3\cdot (1)^{5}}{5}\right)\right)`

## q-126939 — changed parameters

Parameters: `{"c": -3, "inner": 3, "outer": 4}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)={x}^{2}-{y}^{4}$ and $Q(x,y)=({x}^{3}y-x{y}^{3}).$ So,

$$
\frac{∂P}{∂y}=-4{y}^{3},\,\frac{∂Q}{∂x}=3{x}^{2}y-{y}^{3}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}({x}^{2}-{y}^{4})\,dx+({x}^{3}y-x{y}^{3})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}3{x}^{2}y-{y}^{3}-(-4{y}^{3})\,\text{d}A \\  & ={∬}_{D}3{x}^{2}y+3{y}^{3}\,\text{d}A \\  & ={∬}_{D}3y({x}^{2}+{y}^{2})\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$
Δ=\{(r,\theta )\,:\,1\le r\le 4,\,0\le \theta \le 2\pi \}.
$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}3y({x}^{2}+{y}^{2})\,\text{d}A & ={\int }_{0}^{2\pi }{\int }_{1}^{4}3\cdot r\operatorname{sin}⁡\theta \cdot ((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2})\cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{1}^{4}3{r}^{2}\operatorname{sin}⁡\theta \cdot {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{1}^{4}3{r}^{4}\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }\operatorname{sin}⁡\theta \,\text{d}\theta {\int }_{1}^{4}3{r}^{4}\,\text{d}r \\  & =\operatorname{cos}⁡\theta \,{|}_{0}^{2\pi }\cdot \frac{3{r}^{5}}{5}\,{|}_{1}^{4} \\  & =(\operatorname{cos}⁡(2\pi )-\operatorname{cos}⁡(0))\cdot (\frac{3(4)^{5}}{5}-\frac{3(1)^{5}}{5}) \\  & =(1-1)\cdot (\frac{3(4)^{5}}{5}-\frac{3(1)^{5}}{5}) \\  & =0.\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=- 3 x^{2} + 3 y^{4}$ and $Q(x,y)=- 3 x^{3} y + 3 x y^{3}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- 3 x^{2} + 3 y^{4}\right)=\left(0\right)+\left(12 y^{3}\right)=12 y^{3}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- 3 x^{3} y + 3 x y^{3}\right)=\left(- 9 x^{2} y\right)+\left(3 y^{3}\right)=- 9 x^{2} y + 3 y^{3}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=12 y^{3},\qquad\frac{\partial Q}{\partial x}=- 9 x^{2} y + 3 y^{3}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(- 3 x^{2} + 3 y^{4})\,\mathrm dx+(- 3 x^{3} y + 3 x y^{3})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(- 9 x^{2} y + 3 y^{3}-(12 y^{3})\right)\,\mathrm dA\\ & =\iint_D(- 9 x^{2} y - 9 y^{3})\,\mathrm dA\\ & =\iint_D - 9 y \left(x^{2} + y^{2}\right)\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$\Delta=\{(r,\theta):3\le r\le 4,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 9 y \left(x^{2} + y^{2}\right)\,\mathrm dA & =\int_{0}^{2 \pi}\int_{3}^{4}-9\cdot r\sin\theta\cdot ((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}-9r^2\sin\theta\cdot r^2(\cos^2\theta+\sin^2\theta)\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\int_{3}^{4}-9r^4\sin\theta\,\mathrm d r\,\mathrm d \theta\\ & =\int_{0}^{2 \pi}\sin\theta\,\mathrm d \theta\cdot \int_{3}^{4}-9r^4\,\mathrm d r\\ & =-\cos\theta\big|_{0}^{2 \pi}\cdot \frac{-9r^5}{5}\big|_{3}^{4}\\ & =\left(-\cos(2\pi)-\left(-\cos(0)\right)\right)\cdot \left(\frac{-9\cdot (4)^{5}}{5}-\left(\frac{-9\cdot (3)^{5}}{5}\right)\right)\\ & =\left(-1-\left(-1\right)\right)\cdot \left(\frac{-9\cdot (4)^{5}}{5}-\left(\frac{-9\cdot (3)^{5}}{5}\right)\right)\\ & =(\left(-1\right)-\left(-1\right))\cdot (\left(- \frac{9216}{5}\right)-\left(- \frac{2187}{5}\right))\\ & =0.\end{aligned}
$$

Checked original operation fragments in order:

- `\int_{0}^{2 \pi}\int_{3}^{4}-9\cdot r\sin\theta\cdot ((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\int_{3}^{4}-9r^2\sin\theta\cdot r^2(\cos^2\theta+\sin^2\theta)\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\int_{3}^{4}-9r^4\sin\theta\,\mathrm d r\,\mathrm d \theta`
- `\int_{0}^{2 \pi}\sin\theta\,\mathrm d \theta\cdot \int_{3}^{4}-9r^4\,\mathrm d r`
- `-\cos\theta\big|_{0}^{2 \pi}\cdot \frac{-9r^5}{5}\big|_{3}^{4}`
- `\left(-\cos(2\pi)-\left(-\cos(0)\right)\right)\cdot \left(\frac{-9\cdot (4)^{5}}{5}-\left(\frac{-9\cdot (3)^{5}}{5}\right)\right)`
- `\left(-1-\left(-1\right)\right)\cdot \left(\frac{-9\cdot (4)^{5}}{5}-\left(\frac{-9\cdot (3)^{5}}{5}\right)\right)`

## q-126938 — original anchor

Parameters: `{"c": 1, "inner": 1, "outer": 3}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=-{x}^{2}y-{y}^{3}$ and $Q(x,y)={x}^{3}+x{y}^{2}.$ So,

$$
\frac{∂P}{∂y}=-{x}^{2}-3{y}^{2},\,\frac{∂Q}{∂x}=3{x}^{2}+{y}^{2}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}-({x}^{2}y+{y}^{3})\,dx+({x}^{3}+x{y}^{2})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}3{x}^{2}+{y}^{2}-(-{x}^{2}-3{y}^{2})\,\text{d}A \\  & ={∬}_{D}4{x}^{2}+4{y}^{2}\,\text{d}A \\  & ={∬}_{D}4({x}^{2}+{y}^{2})\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$
Δ=\{(r,\theta )\,:\,1\le r\le 3,\,0\le \theta \le 2\pi \}.
$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}4({x}^{2}+{y}^{2})\,\text{d}A & =4{\int }_{0}^{2\pi }{\int }_{1}^{3}(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}\cdot r\,\text{d}r\,\text{d}\theta  \\  & =4{\int }_{0}^{2\pi }{\int }_{1}^{3}{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\cdot r\,\text{d}r\,\text{d}\theta  \\  & =4{\int }_{0}^{2\pi }{\int }_{1}^{3}{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & =4{\int }_{0}^{2\pi }\,\text{d}\theta {\int }_{1}^{3}{r}^{3}\,\text{d}r \\  & =8\pi {\int }_{1}^{2}{r}^{3}\,\text{d}r \\  & =8\pi \cdot {\frac{1}{4}{r}^{4}|}_{1}^{3} \\  & =2\pi \cdot ({3}^{4}-{1}^{4}) \\  & =160\pi .\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=- x^{2} y - y^{3}$ and $Q(x,y)=x^{3} + x y^{2}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- x^{2} y - y^{3}\right)=\left(- 3 y^{2}\right)+\left(- x^{2}\right)=- x^{2} - 3 y^{2}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(x^{3} + x y^{2}\right)=\left(3 x^{2}\right)+\left(y^{2}\right)=3 x^{2} + y^{2}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- x^{2} - 3 y^{2},\qquad\frac{\partial Q}{\partial x}=3 x^{2} + y^{2}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(- x^{2} y - y^{3})\,\mathrm dx+(x^{3} + x y^{2})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(3 x^{2} + y^{2}-(- x^{2} - 3 y^{2})\right)\,\mathrm dA\\ & =\iint_D(4 x^{2} + 4 y^{2})\,\mathrm dA\\ & =\iint_D 4 \left(x^{2} + y^{2}\right)\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$\Delta=\{(r,\theta):1\le r\le 3,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D 4 \left(x^{2} + y^{2}\right)\,\mathrm dA & =4\cdot \int_{0}^{2 \pi}\int_{1}^{3}((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =4\cdot \int_{0}^{2 \pi}\int_{1}^{3}r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =4\cdot \int_{0}^{2 \pi}\int_{1}^{3}r^{3}\,\mathrm d r\,\mathrm d \theta\\ & =4\cdot \int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{1}^{3}r^{3}\,\mathrm d r\\ & =8 \pi\cdot \int_{1}^{3}r^{3}\,\mathrm d r\\ & =8 \pi\cdot \frac{r^{4}}{4}\big|_{1}^{3}\\ & =8 \pi\cdot (\left(\frac{81}{4}\right)-\left(\frac{1}{4}\right))\\ & =2 \pi\cdot \left((3)^{4}-\left((1)^{4}\right)\right)\\ & =2 \pi\cdot \left(81-\left(1\right)\right)\\ & =160 \pi.\end{aligned}
$$

Checked original operation fragments in order:

- `4\cdot \int_{0}^{2 \pi}\int_{1}^{3}((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\,\mathrm d r\,\mathrm d \theta`
- `4\cdot \int_{0}^{2 \pi}\int_{1}^{3}r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\,\mathrm d r\,\mathrm d \theta`
- `4\cdot \int_{0}^{2 \pi}\int_{1}^{3}r^{3}\,\mathrm d r\,\mathrm d \theta`
- `4\cdot \int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{1}^{3}r^{3}\,\mathrm d r`
- `8 \pi\cdot \int_{1}^{3}r^{3}\,\mathrm d r`
- `8 \pi\cdot \frac{r^{4}}{4}\big|_{1}^{3}`
- `2 \pi\cdot \left((3)^{4}-\left((1)^{4}\right)\right)`

## q-126938 — changed parameters

Parameters: `{"c": -3, "inner": 3, "outer": 4}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=-{x}^{2}y-{y}^{3}$ and $Q(x,y)={x}^{3}+x{y}^{2}.$ So,

$$
\frac{∂P}{∂y}=-{x}^{2}-3{y}^{2},\,\frac{∂Q}{∂x}=3{x}^{2}+{y}^{2}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}-({x}^{2}y+{y}^{3})\,dx+({x}^{3}+x{y}^{2})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}3{x}^{2}+{y}^{2}-(-{x}^{2}-3{y}^{2})\,\text{d}A \\  & ={∬}_{D}4{x}^{2}+4{y}^{2}\,\text{d}A \\  & ={∬}_{D}4({x}^{2}+{y}^{2})\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$
Δ=\{(r,\theta )\,:\,1\le r\le 3,\,0\le \theta \le 2\pi \}.
$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}4({x}^{2}+{y}^{2})\,\text{d}A & =4{\int }_{0}^{2\pi }{\int }_{1}^{3}(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}\cdot r\,\text{d}r\,\text{d}\theta  \\  & =4{\int }_{0}^{2\pi }{\int }_{1}^{3}{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\cdot r\,\text{d}r\,\text{d}\theta  \\  & =4{\int }_{0}^{2\pi }{\int }_{1}^{3}{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & =4{\int }_{0}^{2\pi }\,\text{d}\theta {\int }_{1}^{3}{r}^{3}\,\text{d}r \\  & =8\pi {\int }_{1}^{2}{r}^{3}\,\text{d}r \\  & =8\pi \cdot {\frac{1}{4}{r}^{4}|}_{1}^{3} \\  & =2\pi \cdot ({3}^{4}-{1}^{4}) \\  & =160\pi .\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=3 x^{2} y + 3 y^{3}$ and $Q(x,y)=- 3 x^{3} - 3 x y^{2}.$ So,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(3 x^{2} y + 3 y^{3}\right)=\left(9 y^{2}\right)+\left(3 x^{2}\right)=3 x^{2} + 9 y^{2}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- 3 x^{3} - 3 x y^{2}\right)=\left(- 9 x^{2}\right)+\left(- 3 y^{2}\right)=- 9 x^{2} - 3 y^{2}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=3 x^{2} + 9 y^{2},\qquad\frac{\partial Q}{\partial x}=- 9 x^{2} - 3 y^{2}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(3 x^{2} y + 3 y^{3})\,\mathrm dx+(- 3 x^{3} - 3 x y^{2})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(- 9 x^{2} - 3 y^{2}-(3 x^{2} + 9 y^{2})\right)\,\mathrm dA\\ & =\iint_D(- 12 x^{2} - 12 y^{2})\,\mathrm dA\\ & =\iint_D - 12 \left(x^{2} + y^{2}\right)\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in polar coordinates as 

$$\Delta=\{(r,\theta):3\le r\le 4,0\le\theta\le2\pi\}.$$

Recall that the change of variables formula for polar coordinates gives

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 12 \left(x^{2} + y^{2}\right)\,\mathrm dA & =-12\cdot \int_{0}^{2 \pi}\int_{3}^{4}((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =-12\cdot \int_{0}^{2 \pi}\int_{3}^{4}r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\,\mathrm d r\,\mathrm d \theta\\ & =-12\cdot \int_{0}^{2 \pi}\int_{3}^{4}r^{3}\,\mathrm d r\,\mathrm d \theta\\ & =-12\cdot \int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{3}^{4}r^{3}\,\mathrm d r\\ & =- 24 \pi\cdot \int_{3}^{4}r^{3}\,\mathrm d r\\ & =- 24 \pi\cdot \frac{r^{4}}{4}\big|_{3}^{4}\\ & =- 24 \pi\cdot (\left(64\right)-\left(\frac{81}{4}\right))\\ & =-3\cdot\left(2 \pi\right)\cdot \left((4)^{4}-\left((3)^{4}\right)\right)\\ & =- 6 \pi\cdot \left(256-\left(81\right)\right)\\ & =- 1050 \pi.\end{aligned}
$$

Checked original operation fragments in order:

- `-12\cdot \int_{0}^{2 \pi}\int_{3}^{4}((r\cos\theta)^2+(r\sin\theta)^2)\cdot r\,\mathrm d r\,\mathrm d \theta`
- `-12\cdot \int_{0}^{2 \pi}\int_{3}^{4}r^{2}(\cos^2\theta+\sin^2\theta)\cdot r\,\mathrm d r\,\mathrm d \theta`
- `-12\cdot \int_{0}^{2 \pi}\int_{3}^{4}r^{3}\,\mathrm d r\,\mathrm d \theta`
- `-12\cdot \int_{0}^{2 \pi}\,\mathrm d \theta\cdot \int_{3}^{4}r^{3}\,\mathrm d r`
- `- 24 \pi\cdot \int_{3}^{4}r^{3}\,\mathrm d r`
- `- 24 \pi\cdot \frac{r^{4}}{4}\big|_{3}^{4}`
- `-3\cdot\left(2 \pi\right)\cdot \left((4)^{4}-\left((3)^{4}\right)\right)`

## q-126942 — original anchor

Parameters: `{"c": 1, "hole": [1, 2, 0, 1], "outer": [0, 3, -1, 2]}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)={y}^{2}(x+1)$ and $Q(x,y)=3{x}^{2}y+2xy.$ Therefore,

$$
\frac{∂P}{∂y}=2y(x+1),\,\frac{∂Q}{∂x}=6xy+2y.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}{y}^{2}(x+1)\,dx+(3{x}^{2}y+2xy)\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}(6xy+2y)-2y(x+1)\,\text{d}A \\  & ={∬}_{D}4xy\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as ${Δ}_{1}∖{Δ}_{2},$ where

- ${Δ}_{1}=\{(x,y)\,:\,0\le x\le 3,-1\le y\le 2\}$ is the region enclosed by the outer curve, and

- ${Δ}_{2}=\{(x,y)\,:\,1\le x\le 2,0\le y\le 1\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}4xy\,\text{d}A & ={∬}_{{Δ}_{1}}4xy\,\text{d}A-{∬}_{{Δ}_{2}}4xy\,\text{d}A \\  & ={\int }_{-1}^{2}{\int }_{0}^{3}4xy\,\text{d}x\,\text{d}y-{\int }_{0}^{1}{\int }_{1}^{2}4xy\,\text{d}x\,\text{d}y \\  & ={\int }_{0}^{3}2x\,\text{d}x{\int }_{-1}^{2}2y\,\text{d}y-{\int }_{1}^{2}2x\,\text{d}x{\int }_{0}^{1}2y\,\text{d}y \\  & ={x}^{2}\,{|}_{0}^{3}\cdot {y}^{2}\,{|}_{-1}^{2}-{x}^{2}\,{|}_{1}^{2}\cdot {y}^{2}\,{|}_{0}^{1} \\  & =(9-0)\cdot (4-1)-(4-1)\cdot (1-0) \\  & =9\cdot 3-3\cdot 1 \\  & =24.\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=y^{2} \left(x + 1\right)$ and $Q(x,y)=3 x^{2} y + 2 x y.$ Therefore,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(y^{2} \left(x + 1\right)\right)=\left(2 y \left(x + 1\right)\right)=2 y \left(x + 1\right)\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(3 x^{2} y + 2 x y\right)=\left(2 y\right)+\left(6 x y\right)=6 x y + 2 y.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=2 y \left(x + 1\right),\qquad\frac{\partial Q}{\partial x}=6 x y + 2 y.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(y^{2} \left(x + 1\right))\,\mathrm dx+(3 x^{2} y + 2 x y)\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(6 x y + 2 y-(2 y \left(x + 1\right))\right)\,\mathrm dA\\ & =\iint_D 4 x y\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as $\Delta_1\setminus\Delta_2,$ where

- $\Delta_1=\{(x,y):0\le x\le 3,-1\le y\le 2\}$ is the region enclosed by the outer curve, and

- $\Delta_2=\{(x,y):1\le x\le 2,0\le y\le 1\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D 4 x y\,\mathrm dA & =\iint_{\Delta_1}4 x y\,\mathrm dA-\iint_{\Delta_2}4 x y\,\mathrm dA\\ & =\int_{-1}^{2}\int_{0}^{3}4 x y\,\mathrm d x\,\mathrm d y-\int_{0}^{1}\int_{1}^{2}4 x y\,\mathrm d x\,\mathrm d y\\ & =\int_{0}^{3}2 x\,\mathrm d x\cdot \int_{-1}^{2}2 y\,\mathrm d y-\int_{1}^{2}2 x\,\mathrm d x\cdot \int_{0}^{1}2 y\,\mathrm d y\\ & =x^{2}\big|_{0}^{3}\cdot y^2\big|_{-1}^{2}-x^{2}\big|_{1}^{2}\cdot y^2\big|_{0}^{1}\\ & =(\left(9\right)-\left(0\right))\cdot (\left(4\right)-\left(1\right))-(\left(4\right)-\left(1\right))\cdot (\left(1\right)-\left(0\right))\\ & =\left(9\right)\cdot \left(3\right)-\left(3\right)\cdot \left(1\right)\\ & =24.\end{aligned}
$$

Checked original operation fragments in order:

- `\iint_{\Delta_1}4 x y\,\mathrm dA-\iint_{\Delta_2}4 x y\,\mathrm dA`
- `\int_{-1}^{2}\int_{0}^{3}4 x y\,\mathrm d x\,\mathrm d y-\int_{0}^{1}\int_{1}^{2}4 x y\,\mathrm d x\,\mathrm d y`
- `\int_{0}^{3}2 x\,\mathrm d x\cdot \int_{-1}^{2}2 y\,\mathrm d y-\int_{1}^{2}2 x\,\mathrm d x\cdot \int_{0}^{1}2 y\,\mathrm d y`
- `x^{2}\big|_{0}^{3}\cdot y^2\big|_{-1}^{2}-x^{2}\big|_{1}^{2}\cdot y^2\big|_{0}^{1}`
- `(\left(9\right)-\left(0\right))\cdot (\left(4\right)-\left(1\right))-(\left(4\right)-\left(1\right))\cdot (\left(1\right)-\left(0\right))`
- `\left(9\right)\cdot \left(3\right)-\left(3\right)\cdot \left(1\right)`

## q-126942 — changed parameters

Parameters: `{"c": -3, "hole": [2, 3, -1, 0], "outer": [1, 4, -2, 1]}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)={y}^{2}(x+1)$ and $Q(x,y)=3{x}^{2}y+2xy.$ Therefore,

$$
\frac{∂P}{∂y}=2y(x+1),\,\frac{∂Q}{∂x}=6xy+2y.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}{y}^{2}(x+1)\,dx+(3{x}^{2}y+2xy)\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}(6xy+2y)-2y(x+1)\,\text{d}A \\  & ={∬}_{D}4xy\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as ${Δ}_{1}∖{Δ}_{2},$ where

- ${Δ}_{1}=\{(x,y)\,:\,0\le x\le 3,-1\le y\le 2\}$ is the region enclosed by the outer curve, and

- ${Δ}_{2}=\{(x,y)\,:\,1\le x\le 2,0\le y\le 1\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}4xy\,\text{d}A & ={∬}_{{Δ}_{1}}4xy\,\text{d}A-{∬}_{{Δ}_{2}}4xy\,\text{d}A \\  & ={\int }_{-1}^{2}{\int }_{0}^{3}4xy\,\text{d}x\,\text{d}y-{\int }_{0}^{1}{\int }_{1}^{2}4xy\,\text{d}x\,\text{d}y \\  & ={\int }_{0}^{3}2x\,\text{d}x{\int }_{-1}^{2}2y\,\text{d}y-{\int }_{1}^{2}2x\,\text{d}x{\int }_{0}^{1}2y\,\text{d}y \\  & ={x}^{2}\,{|}_{0}^{3}\cdot {y}^{2}\,{|}_{-1}^{2}-{x}^{2}\,{|}_{1}^{2}\cdot {y}^{2}\,{|}_{0}^{1} \\  & =(9-0)\cdot (4-1)-(4-1)\cdot (1-0) \\  & =9\cdot 3-3\cdot 1 \\  & =24.\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=- 3 y^{2} \left(x + 1\right)$ and $Q(x,y)=- 9 x^{2} y - 6 x y.$ Therefore,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- 3 y^{2} \left(x + 1\right)\right)=\left(- 6 y \left(x + 1\right)\right)=- 6 y \left(x + 1\right)\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- 9 x^{2} y - 6 x y\right)=\left(- 6 y\right)+\left(- 18 x y\right)=- 18 x y - 6 y.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- 6 y \left(x + 1\right),\qquad\frac{\partial Q}{\partial x}=- 18 x y - 6 y.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(- 3 y^{2} \left(x + 1\right))\,\mathrm dx+(- 9 x^{2} y - 6 x y)\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(- 18 x y - 6 y-(- 6 y \left(x + 1\right))\right)\,\mathrm dA\\ & =\iint_D - 12 x y\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as $\Delta_1\setminus\Delta_2,$ where

- $\Delta_1=\{(x,y):1\le x\le 4,-2\le y\le 1\}$ is the region enclosed by the outer curve, and

- $\Delta_2=\{(x,y):2\le x\le 3,-1\le y\le 0\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 12 x y\,\mathrm dA & =\iint_{\Delta_1}- 12 x y\,\mathrm dA-\iint_{\Delta_2}- 12 x y\,\mathrm dA\\ & =\int_{-2}^{1}\int_{1}^{4}- 12 x y\,\mathrm d x\,\mathrm d y-\int_{-1}^{0}\int_{2}^{3}- 12 x y\,\mathrm d x\,\mathrm d y\\ & =\int_{1}^{4}- 6 x\,\mathrm d x\cdot \int_{-2}^{1}2 y\,\mathrm d y-\int_{2}^{3}- 6 x\,\mathrm d x\cdot \int_{-1}^{0}2 y\,\mathrm d y\\ & =- 3 x^{2}\big|_{1}^{4}\cdot y^2\big|_{-2}^{1}-- 3 x^{2}\big|_{2}^{3}\cdot y^2\big|_{-1}^{0}\\ & =(\left(-48\right)-\left(-3\right))\cdot (\left(1\right)-\left(4\right))-(\left(-27\right)-\left(-12\right))\cdot (\left(0\right)-\left(1\right))\\ & =\left(-45\right)\cdot \left(-3\right)-\left(-15\right)\cdot \left(-1\right)\\ & =120.\end{aligned}
$$

Checked original operation fragments in order:

- `\iint_{\Delta_1}- 12 x y\,\mathrm dA-\iint_{\Delta_2}- 12 x y\,\mathrm dA`
- `\int_{-2}^{1}\int_{1}^{4}- 12 x y\,\mathrm d x\,\mathrm d y-\int_{-1}^{0}\int_{2}^{3}- 12 x y\,\mathrm d x\,\mathrm d y`
- `\int_{1}^{4}- 6 x\,\mathrm d x\cdot \int_{-2}^{1}2 y\,\mathrm d y-\int_{2}^{3}- 6 x\,\mathrm d x\cdot \int_{-1}^{0}2 y\,\mathrm d y`
- `- 3 x^{2}\big|_{1}^{4}\cdot y^2\big|_{-2}^{1}-- 3 x^{2}\big|_{2}^{3}\cdot y^2\big|_{-1}^{0}`
- `(\left(-48\right)-\left(-3\right))\cdot (\left(1\right)-\left(4\right))-(\left(-27\right)-\left(-12\right))\cdot (\left(0\right)-\left(1\right))`
- `\left(-45\right)\cdot \left(-3\right)-\left(-15\right)\cdot \left(-1\right)`

## q-126946 — original anchor

Parameters: `{"c": 1, "hole": [0, 1, 0, 1], "outer": [-1, 2, -2, 2]}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=2{x}^{2}{y}^{4}-x$ and $Q(x,y)=4{x}^{3}{y}^{3}-{y}^{2}.$ Therefore,

$$
\frac{∂P}{∂y}=8{x}^{2}{y}^{3},\,\frac{∂Q}{∂x}=12{x}^{2}{y}^{3}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}(2{x}^{2}{y}^{4}-x)\,dx+(4{x}^{3}{y}^{3}-{y}^{2})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}12{x}^{2}{y}^{3}-8{x}^{2}{y}^{3}\,\text{d}A \\  & ={∬}_{D}4{x}^{2}{y}^{3}\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as ${Δ}_{1}∖{Δ}_{2},$ where

- ${Δ}_{1}=\{(x,y)\,:\,-1\le x\le 2,-2\le y\le 2\}$ is the region enclosed by the outer curve, and

- ${Δ}_{2}=\{(x,y)\,:\,0\le x\le 1,0\le y\le 1\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}4{x}^{2}{y}^{3}\,\text{d}A & ={∬}_{{Δ}_{1}}4{x}^{2}{y}^{3}\,\text{d}A-{∬}_{{Δ}_{2}}4{x}^{2}{y}^{3}\,\text{d}A \\  & ={\int }_{-2}^{2}{\int }_{-1}^{2}4{x}^{2}{y}^{3}\,\text{d}x\,\text{d}y-{\int }_{0}^{1}{\int }_{0}^{1}4{x}^{2}{y}^{3}\,\text{d}x\,\text{d}y \\  & ={\int }_{-1}^{2}{x}^{2}\,\text{d}x{\int }_{-2}^{2}4{y}^{3}\,\text{d}y-{\int }_{0}^{1}{x}^{2}\,\text{d}x{\int }_{0}^{1}4{y}^{3}\,\text{d}y \\  & =\frac{{x}^{3}}{3}\,{|}_{-1}^{2}\cdot {y}^{4}\,{|}_{-2}^{2}-\frac{{x}^{3}}{3}\,{|}_{0}^{1}\cdot {y}^{4}\,{|}_{0}^{1} \\  & =(\frac{8}{3}-(-\frac{1}{3}))\cdot (16-16)-(\frac{1}{3}-0)\cdot (1-0) \\  & =3\cdot 0-\frac{1}{3}\cdot 1 \\  & =-\frac{1}{3}.\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=2 x^{2} y^{4} - x$ and $Q(x,y)=4 x^{3} y^{3} - y^{2}.$ Therefore,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(2 x^{2} y^{4} - x\right)=\left(0\right)+\left(8 x^{2} y^{3}\right)=8 x^{2} y^{3}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(4 x^{3} y^{3} - y^{2}\right)=\left(0\right)+\left(12 x^{2} y^{3}\right)=12 x^{2} y^{3}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=8 x^{2} y^{3},\qquad\frac{\partial Q}{\partial x}=12 x^{2} y^{3}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(2 x^{2} y^{4} - x)\,\mathrm dx+(4 x^{3} y^{3} - y^{2})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(12 x^{2} y^{3}-(8 x^{2} y^{3})\right)\,\mathrm dA\\ & =\iint_D 4 x^{2} y^{3}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as $\Delta_1\setminus\Delta_2,$ where

- $\Delta_1=\{(x,y):-1\le x\le 2,-2\le y\le 2\}$ is the region enclosed by the outer curve, and

- $\Delta_2=\{(x,y):0\le x\le 1,0\le y\le 1\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D 4 x^{2} y^{3}\,\mathrm dA & =\iint_{\Delta_1}4 x^{2} y^{3}\,\mathrm dA-\iint_{\Delta_2}4 x^{2} y^{3}\,\mathrm dA\\ & =\int_{-2}^{2}\int_{-1}^{2}4 x^{2} y^{3}\,\mathrm d x\,\mathrm d y-\int_{0}^{1}\int_{0}^{1}4 x^{2} y^{3}\,\mathrm d x\,\mathrm d y\\ & =\int_{-1}^{2}x^{2}\,\mathrm d x\cdot \int_{-2}^{2}4 y^{3}\,\mathrm d y-\int_{0}^{1}x^{2}\,\mathrm d x\cdot \int_{0}^{1}4 y^{3}\,\mathrm d y\\ & =\frac{x^3}{3}\big|_{-1}^{2}\cdot y^4\big|_{-2}^{2}-\frac{x^3}{3}\big|_{0}^{1}\cdot y^4\big|_{0}^{1}\\ & =(\left(\frac{8}{3}\right)-\left(- \frac{1}{3}\right))\cdot (\left(16\right)-\left(16\right))-(\left(\frac{1}{3}\right)-\left(0\right))\cdot (\left(1\right)-\left(0\right))\\ & =\left(3\right)\cdot \left(0\right)-\left(\frac{1}{3}\right)\cdot \left(1\right)\\ & =- \frac{1}{3}.\end{aligned}
$$

Checked original operation fragments in order:

- `\iint_{\Delta_1}4 x^{2} y^{3}\,\mathrm dA-\iint_{\Delta_2}4 x^{2} y^{3}\,\mathrm dA`
- `\int_{-2}^{2}\int_{-1}^{2}4 x^{2} y^{3}\,\mathrm d x\,\mathrm d y-\int_{0}^{1}\int_{0}^{1}4 x^{2} y^{3}\,\mathrm d x\,\mathrm d y`
- `\int_{-1}^{2}x^{2}\,\mathrm d x\cdot \int_{-2}^{2}4 y^{3}\,\mathrm d y-\int_{0}^{1}x^{2}\,\mathrm d x\cdot \int_{0}^{1}4 y^{3}\,\mathrm d y`
- `\frac{x^3}{3}\big|_{-1}^{2}\cdot y^4\big|_{-2}^{2}-\frac{x^3}{3}\big|_{0}^{1}\cdot y^4\big|_{0}^{1}`
- `(\left(\frac{8}{3}\right)-\left(- \frac{1}{3}\right))\cdot (\left(16\right)-\left(16\right))-(\left(\frac{1}{3}\right)-\left(0\right))\cdot (\left(1\right)-\left(0\right))`
- `\left(3\right)\cdot \left(0\right)-\left(\frac{1}{3}\right)\cdot \left(1\right)`

## q-126946 — changed parameters

Parameters: `{"c": -3, "hole": [1, 2, -1, 0], "outer": [0, 3, -3, 1]}`.

### Original source chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=2{x}^{2}{y}^{4}-x$ and $Q(x,y)=4{x}^{3}{y}^{3}-{y}^{2}.$ Therefore,

$$
\frac{∂P}{∂y}=8{x}^{2}{y}^{3},\,\frac{∂Q}{∂x}=12{x}^{2}{y}^{3}.
$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}{∮}_{∂D}(2{x}^{2}{y}^{4}-x)\,dx+(4{x}^{3}{y}^{3}-{y}^{2})\,dy & ={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A \\  & ={∬}_{D}12{x}^{2}{y}^{3}-8{x}^{2}{y}^{3}\,\text{d}A \\  & ={∬}_{D}4{x}^{2}{y}^{3}\,\text{d}A.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as ${Δ}_{1}∖{Δ}_{2},$ where

- ${Δ}_{1}=\{(x,y)\,:\,-1\le x\le 2,-2\le y\le 2\}$ is the region enclosed by the outer curve, and

- ${Δ}_{2}=\{(x,y)\,:\,0\le x\le 1,0\le y\le 1\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}{∬}_{D}4{x}^{2}{y}^{3}\,\text{d}A & ={∬}_{{Δ}_{1}}4{x}^{2}{y}^{3}\,\text{d}A-{∬}_{{Δ}_{2}}4{x}^{2}{y}^{3}\,\text{d}A \\  & ={\int }_{-2}^{2}{\int }_{-1}^{2}4{x}^{2}{y}^{3}\,\text{d}x\,\text{d}y-{\int }_{0}^{1}{\int }_{0}^{1}4{x}^{2}{y}^{3}\,\text{d}x\,\text{d}y \\  & ={\int }_{-1}^{2}{x}^{2}\,\text{d}x{\int }_{-2}^{2}4{y}^{3}\,\text{d}y-{\int }_{0}^{1}{x}^{2}\,\text{d}x{\int }_{0}^{1}4{y}^{3}\,\text{d}y \\  & =\frac{{x}^{3}}{3}\,{|}_{-1}^{2}\cdot {y}^{4}\,{|}_{-2}^{2}-\frac{{x}^{3}}{3}\,{|}_{0}^{1}\cdot {y}^{4}\,{|}_{0}^{1} \\  & =(\frac{8}{3}-(-\frac{1}{3}))\cdot (16-16)-(\frac{1}{3}-0)\cdot (1-0) \\  & =3\cdot 0-\frac{1}{3}\cdot 1 \\  & =-\frac{1}{3}.\end{aligned}
$$

### Normal chain and prose

Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial derivatives on an open region containing $D,$ then Green's theorem states that

$$
{∮}_{C}P\,dx+Q\,dy={∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A.
$$

Green's theorem can be extended to include regions containing holes. In such cases, we can apply Green's theorem in the same way as before.

We have that $P(x,y)=- 6 x^{2} y^{4} + 3 x$ and $Q(x,y)=- 12 x^{3} y^{3} + 3 y^{2}.$ Therefore,

For $\partial P/\partial y$ we hold $x$ fixed, and for $\partial Q/\partial x$ we hold $y$ fixed. The component derivatives, including zero contributions, are

$$
\begin{aligned}\frac{\partial P}{\partial y} & =\frac{\partial}{\partial y}\left(- 6 x^{2} y^{4} + 3 x\right)=\left(0\right)+\left(- 24 x^{2} y^{3}\right)=- 24 x^{2} y^{3}\\ \frac{\partial Q}{\partial x} & =\frac{\partial}{\partial x}\left(- 12 x^{3} y^{3} + 3 y^{2}\right)=\left(0\right)+\left(- 36 x^{2} y^{3}\right)=- 36 x^{2} y^{3}.\end{aligned}
$$

$$\frac{\partial P}{\partial y}=- 24 x^{2} y^{3},\qquad\frac{\partial Q}{\partial x}=- 36 x^{2} y^{3}.$$

Therefore, applying Green's theorem, we get

$$
\begin{aligned}\oint_{\partial D}(- 6 x^{2} y^{4} + 3 x)\,\mathrm dx+(- 12 x^{3} y^{3} + 3 y^{2})\,\mathrm dy & =\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,\mathrm dA\\ & =\iint_D\left(- 36 x^{2} y^{3}-(- 24 x^{2} y^{3})\right)\,\mathrm dA\\ & =\iint_D - 12 x^{2} y^{3}\,\mathrm dA.\end{aligned}
$$

The region $D$ can be represented in Cartesian coordinates as $\Delta_1\setminus\Delta_2,$ where

- $\Delta_1=\{(x,y):0\le x\le 3,-3\le y\le 1\}$ is the region enclosed by the outer curve, and

- $\Delta_2=\{(x,y):1\le x\le 2,-1\le y\le 0\}$ is the region enclosed by the inner curve.

Therefore, our double integral becomes

$$
\begin{aligned}\iint_D - 12 x^{2} y^{3}\,\mathrm dA & =\iint_{\Delta_1}- 12 x^{2} y^{3}\,\mathrm dA-\iint_{\Delta_2}- 12 x^{2} y^{3}\,\mathrm dA\\ & =\int_{-3}^{1}\int_{0}^{3}- 12 x^{2} y^{3}\,\mathrm d x\,\mathrm d y-\int_{-1}^{0}\int_{1}^{2}- 12 x^{2} y^{3}\,\mathrm d x\,\mathrm d y\\ & =\int_{0}^{3}- 3 x^{2}\,\mathrm d x\cdot \int_{-3}^{1}4 y^{3}\,\mathrm d y-\int_{1}^{2}- 3 x^{2}\,\mathrm d x\cdot \int_{-1}^{0}4 y^{3}\,\mathrm d y\\ & =\frac{-3x^3}{3}\big|_{0}^{3}\cdot y^4\big|_{-3}^{1}-\frac{-3x^3}{3}\big|_{1}^{2}\cdot y^4\big|_{-1}^{0}\\ & =(\left(-27\right)-\left(0\right))\cdot (\left(1\right)-\left(81\right))-(\left(-8\right)-\left(-1\right))\cdot (\left(0\right)-\left(1\right))\\ & =\left(-27\right)\cdot \left(-80\right)-\left(-7\right)\cdot \left(-1\right)\\ & =2153.\end{aligned}
$$

Checked original operation fragments in order:

- `\iint_{\Delta_1}- 12 x^{2} y^{3}\,\mathrm dA-\iint_{\Delta_2}- 12 x^{2} y^{3}\,\mathrm dA`
- `\int_{-3}^{1}\int_{0}^{3}- 12 x^{2} y^{3}\,\mathrm d x\,\mathrm d y-\int_{-1}^{0}\int_{1}^{2}- 12 x^{2} y^{3}\,\mathrm d x\,\mathrm d y`
- `\int_{0}^{3}- 3 x^{2}\,\mathrm d x\cdot \int_{-3}^{1}4 y^{3}\,\mathrm d y-\int_{1}^{2}- 3 x^{2}\,\mathrm d x\cdot \int_{-1}^{0}4 y^{3}\,\mathrm d y`
- `\frac{-3x^3}{3}\big|_{0}^{3}\cdot y^4\big|_{-3}^{1}-\frac{-3x^3}{3}\big|_{1}^{2}\cdot y^4\big|_{-1}^{0}`
- `(\left(-27\right)-\left(0\right))\cdot (\left(1\right)-\left(81\right))-(\left(-8\right)-\left(-1\right))\cdot (\left(0\right)-\left(1\right))`
- `\left(-27\right)\cdot \left(-80\right)-\left(-7\right)\cdot \left(-1\right)`

