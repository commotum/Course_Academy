## Original q-160836 — raw evidence, ineligible

Evaluate the surface integral
$∬_(S)12xyzdS$
where $S$ is defined by $z = x + y$ for $0 \le x \le 1$ and $0 \le y \le 1$.

- $4$
- $4\sqrt{3}$
- $\sqrt{3}$
- $-6$
- $-12\sqrt{3}$

[Original worked solution absent.]

### Generated raw q-160836 scale 2 — evidence only, opaque bank

Evaluate the surface integral
$∬_(S)24xyzdS$
where $S$ is defined by $z = x + y$ for $0 \le x \le 1$ and $0 \le y \le 1$.

- $2\left(\sqrt{3}\right)$
- $2\left(-6\right)$
- $2\left(4\right)$
- $2\left(4\sqrt{3}\right)$
- $2\left(-12\sqrt{3}\right)$

[Original worked solution absent.]

### Normal plane_xyz at original parameters — authored bank, source-family chain

Evaluate the surface integral

$$
\iint_S 12 x y z\,\mathrm{d}S
$$

where $S$ is defined by $z=x + y$ for $0\le x\le 1$ and $0\le y\le 1$.

- $- 4 \sqrt{3}$
- $4 \sqrt{3}$
- $0$
- $12$
- $4$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(x + y)=1,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(x + y)=1.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}12 x y z\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\left(12 x y \left(x + y\right)\right)\sqrt{1+\left(1\right)^{2}+\left(1\right)^{2}}\,\text{d}A\\ & =\int_{0}^{1}\int_{0}^{1}\left(\sqrt{3} \left(12 x^{2} y + 12 x y^{2}\right)\right)\,\text{d}y\,\text{d}x\\ & =\sqrt{3}\int_{0}^{1}[(4 x y^{3})+(6 x^{2} y^{2})]_{y=0}^{y=1}\,\text{d}x\\ & =\sqrt{3}\int_{0}^{1}\left((4 x)+(6 x^{2})-\left((0)+(0)\right)\right)\,\text{d}x\\ & =\sqrt{3}\int_{0}^{1}\left(2 x \left(3 x + 2\right)\right)\,\text{d}x\\ & =\sqrt{3}[(2 x^{2})+(2 x^{3})]_{x=0}^{x=1}\\ & =\sqrt{3}\left((2)+(2)-\left((0)+(0)\right)\right)\\ & =4 \sqrt{3}.\end{aligned}
$$

### Generated plane_xyz variant 1 — authored bank

Evaluate the surface integral

$$
\iint_S 2 x y z\,\mathrm{d}S
$$

where $S$ is defined by $z=2 x + 2 y$ for $0\le x\le 2$ and $0\le y\le 2$.

- $\frac{128}{3}$
- $0$
- $384$
- $128$
- $-128$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x + 2 y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x + 2 y)=2.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}2 x y z\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\left(2 x y \left(2 x + 2 y\right)\right)\sqrt{1+\left(2\right)^{2}+\left(2\right)^{2}}\,\text{d}A\\ & =\int_{0}^{2}\int_{0}^{2}\left(12 x^{2} y + 12 x y^{2}\right)\,\text{d}y\,\text{d}x\\ & =3\int_{0}^{2}[(\frac{4 x y^{3}}{3})+(2 x^{2} y^{2})]_{y=0}^{y=2}\,\text{d}x\\ & =3\int_{0}^{2}\left((\frac{32 x}{3})+(8 x^{2})-\left((0)+(0)\right)\right)\,\text{d}x\\ & =3\int_{0}^{2}\left(\frac{8 x \left(3 x + 4\right)}{3}\right)\,\text{d}x\\ & =3[(\frac{8 x^{3}}{3})+(\frac{16 x^{2}}{3})]_{x=0}^{x=2}\\ & =3\left((\frac{64}{3})+(\frac{64}{3})-\left((0)+(0)\right)\right)\\ & =128.\end{aligned}
$$

### Generated plane_xyz variant 2 — authored bank

Evaluate the surface integral

$$
\iint_S 2 x y z\,\mathrm{d}S
$$

where $S$ is defined by $z=2 x + 2 y$ for $0\le x\le 1$ and $0\le y\le 1$.

- $\frac{4}{3}$
- $4$
- $0$
- $-4$
- $12$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x + 2 y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x + 2 y)=2.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}2 x y z\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\left(2 x y \left(2 x + 2 y\right)\right)\sqrt{1+\left(2\right)^{2}+\left(2\right)^{2}}\,\text{d}A\\ & =\int_{0}^{1}\int_{0}^{1}\left(12 x^{2} y + 12 x y^{2}\right)\,\text{d}y\,\text{d}x\\ & =3\int_{0}^{1}[(\frac{4 x y^{3}}{3})+(2 x^{2} y^{2})]_{y=0}^{y=1}\,\text{d}x\\ & =3\int_{0}^{1}\left((\frac{4 x}{3})+(2 x^{2})-\left((0)+(0)\right)\right)\,\text{d}x\\ & =3\int_{0}^{1}\left(\frac{2 x \left(3 x + 2\right)}{3}\right)\,\text{d}x\\ & =3[(\frac{2 x^{3}}{3})+(\frac{2 x^{2}}{3})]_{x=0}^{x=1}\\ & =3\left((\frac{2}{3})+(\frac{2}{3})-\left((0)+(0)\right)\right)\\ & =4.\end{aligned}
$$

## Original q-161355 — raw evidence, ineligible

Evaluate the surface integral 

$$
{∬}_{S}\frac{z}{\sqrt{1+2{cos}^{2}⁡(x+y)}}\,\text{d}S
$$

where $S$ is defined by $z=\operatorname{sin}⁡(x+y)$ for $0\le x\le \pi $ and $-x\le y\le x.$

- $\pi $
- $\frac{3\pi }{2}$
- $\frac{\pi }{3}$
- $\frac{3\sqrt{3}}{2}$
- $0$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}\operatorname{sin}⁡(x+y)=\operatorname{cos}⁡(x+y),
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}\operatorname{sin}⁡(x+y)=\operatorname{cos}⁡(x+y).
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{z}{\sqrt{1+2{cos}^{2}⁡(x+y)}}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}\,\frac{\operatorname{sin}⁡(x+y)}{\sqrt{1+2{cos}^{2}⁡(x+y)}}\sqrt{1+2(\operatorname{cos}⁡(x+y))^{2}}\,\text{d}A \\  & ={∬}_{D}\,\frac{\operatorname{sin}⁡(x+y)}{\cancel{\sqrt{1+2{cos}^{2}⁡(x+y)}}}\cancel{\sqrt{1+2(\operatorname{cos}⁡(x+y))^{2}}}\,\text{d}A \\  & ={∬}_{D}\,\operatorname{sin}⁡(x+y)\,\text{d}A \\  & ={\int }_{0}^{\pi }{\int }_{-x}^{x}\operatorname{sin}⁡(x+y)\,\text{d}y\,\text{d}x \\  & ={\int }_{0}^{\pi }[-\operatorname{cos}⁡(x+y)]_{y=-x}^{y=x}\,\text{d}x \\  & ={\int }_{0}^{\pi }(1-\operatorname{cos}⁡(2x))\,\text{d}x \\  & ={[x-\frac{\operatorname{sin}⁡(2x)}{2}]}_{0}^{\pi } \\  & =\pi \end{aligned}
$$

### Generated raw q-161355 scale 2 — evidence only, opaque bank

Evaluate the surface integral 

$$
{∬}_{S}2\left(\frac{z}{\sqrt{1+2{cos}^{2}⁡(x+y)}}\right)\,\text{d}S
$$

where $S$ is defined by $z=\operatorname{sin}⁡(x+y)$ for $0\le x\le \pi $ and $-x\le y\le x.$

- $2\left(\frac{\pi }{3}\right)$
- $2\left(\frac{3\sqrt{3}}{2}\right)$
- $2\left(\pi \right)$
- $2\left(\frac{3\pi }{2}\right)$
- $2\left(0\right)$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}\operatorname{sin}⁡(x+y)=\operatorname{cos}⁡(x+y),
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}\operatorname{sin}⁡(x+y)=\operatorname{cos}⁡(x+y).
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}2\left(\frac{z}{\sqrt{1+2{cos}^{2}⁡(x+y)}}\right)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & =2\left({∬}_{D}\,\frac{\operatorname{sin}⁡(x+y)}{\sqrt{1+2{cos}^{2}⁡(x+y)}}\sqrt{1+2(\operatorname{cos}⁡(x+y))^{2}}\,\text{d}A\right)\\  & =2\left({∬}_{D}\,\frac{\operatorname{sin}⁡(x+y)}{\cancel{\sqrt{1+2{cos}^{2}⁡(x+y)}}}\cancel{\sqrt{1+2(\operatorname{cos}⁡(x+y))^{2}}}\,\text{d}A\right)\\  & =2\left({∬}_{D}\,\operatorname{sin}⁡(x+y)\,\text{d}A\right)\\  & =2\left({\int }_{0}^{\pi }{\int }_{-x}^{x}\operatorname{sin}⁡(x+y)\,\text{d}y\,\text{d}x\right)\\  & =2\left({\int }_{0}^{\pi }[-\operatorname{cos}⁡(x+y)]_{y=-x}^{y=x}\,\text{d}x\right)\\  & =2\left({\int }_{0}^{\pi }(1-\operatorname{cos}⁡(2x))\,\text{d}x\right)\\  & =2\left({[x-\frac{\operatorname{sin}⁡(2x)}{2}]}_{0}^{\pi }\right)\\  & =2\left(\pi\right)\end{aligned}
$$

### Normal trig_triangle at original parameters — authored bank, source-family chain

Evaluate the surface integral

$$
\iint_S \frac{z}{\sqrt{2 \cos^{2}{\left(x + y \right)} + 1}}\,\mathrm{d}S
$$

where $S$ is defined by $z=\sin{\left(x + y \right)}$ for $0\le x\le \pi$ and $- x\le y\le x$.

- $2 \pi$
- $\pi$
- $0$
- $\frac{\pi}{2}$
- $- \pi$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(\sin{\left(x + y \right)})=\cos{\left(x + y \right)},
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(\sin{\left(x + y \right)})=\cos{\left(x + y \right)}.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{z}{\sqrt{2 \cos^{2}{\left(x + y \right)} + 1}}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{\sin{\left(x + y \right)}}{\sqrt{2 \cos^{2}{\left(x + y \right)} + 1}}\sqrt{1+\left(\cos{\left(x + y \right)}\right)^{2}+\left(\cos{\left(x + y \right)}\right)^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{\sin{\left(x + y \right)}}{\cancel{\sqrt{2 \cos^{2}{\left(x + y \right)} + 1}}}\cancel{\sqrt{2 \cos^{2}{\left(x + y \right)} + 1}}\,\text{d}A\\ & ={∬}_{D}\sin{\left(x + y \right)}\,\text{d}A\\ & =\int_{0}^{\pi}\int_{- x}^{x}\left(\sin{\left(x + y \right)}\right)\,\text{d}y\,\text{d}x\\ & =\int_{0}^{\pi}[- \cos{\left(x + y \right)}]_{y=- x}^{y=x}\,\text{d}x\\ & =\int_{0}^{\pi}\left(2 \sin^{2}{\left(x \right)}\right)\,\text{d}x\\ & =[(x)+(- \frac{\sin{\left(2 x \right)}}{2})]_{x=0}^{x=\pi}\\ & =\left((\pi)+(0)-\left((0)+(0)\right)\right)\\ & =\pi.\end{aligned}
$$

### Generated trig_triangle variant 1 — authored bank

Evaluate the surface integral

$$
\iint_S \frac{2 z}{\sqrt{2 \cos^{2}{\left(x + y \right)} + 1}}\,\mathrm{d}S
$$

where $S$ is defined by $z=\sin{\left(x + y \right)}$ for $0\le x\le \pi$ and $- x\le y\le x$.

- $- 2 \pi$
- $4 \pi$
- $\pi$
- $2 \pi$
- $0$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(\sin{\left(x + y \right)})=\cos{\left(x + y \right)},
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(\sin{\left(x + y \right)})=\cos{\left(x + y \right)}.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{2 z}{\sqrt{2 \cos^{2}{\left(x + y \right)} + 1}}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{2 \sin{\left(x + y \right)}}{\sqrt{2 \cos^{2}{\left(x + y \right)} + 1}}\sqrt{1+\left(\cos{\left(x + y \right)}\right)^{2}+\left(\cos{\left(x + y \right)}\right)^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{2 \sin{\left(x + y \right)}}{\cancel{\sqrt{2 \cos^{2}{\left(x + y \right)} + 1}}}\cancel{\sqrt{2 \cos^{2}{\left(x + y \right)} + 1}}\,\text{d}A\\ & ={∬}_{D}2 \sin{\left(x + y \right)}\,\text{d}A\\ & =\int_{0}^{\pi}\int_{- x}^{x}\left(2 \sin{\left(x + y \right)}\right)\,\text{d}y\,\text{d}x\\ & =\int_{0}^{\pi}[- 2 \cos{\left(x + y \right)}]_{y=- x}^{y=x}\,\text{d}x\\ & =\int_{0}^{\pi}\left(4 \sin^{2}{\left(x \right)}\right)\,\text{d}x\\ & =[(2 x)+(- \sin{\left(2 x \right)})]_{x=0}^{x=\pi}\\ & =\left((2 \pi)+(0)-\left((0)+(0)\right)\right)\\ & =2 \pi.\end{aligned}
$$

### Generated trig_triangle variant 2 — authored bank

Evaluate the surface integral

$$
\iint_S \frac{2 z}{\sqrt{2 \cos^{2}{\left(x + y \right)} + 1}}\,\mathrm{d}S
$$

where $S$ is defined by $z=\sin{\left(x + y \right)}$ for $0\le x\le \pi$ and $- x\le y\le x$.

- $2 \pi$
- $\pi$
- $0$
- $- 2 \pi$
- $4 \pi$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(\sin{\left(x + y \right)})=\cos{\left(x + y \right)},
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(\sin{\left(x + y \right)})=\cos{\left(x + y \right)}.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{2 z}{\sqrt{2 \cos^{2}{\left(x + y \right)} + 1}}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{2 \sin{\left(x + y \right)}}{\sqrt{2 \cos^{2}{\left(x + y \right)} + 1}}\sqrt{1+\left(\cos{\left(x + y \right)}\right)^{2}+\left(\cos{\left(x + y \right)}\right)^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{2 \sin{\left(x + y \right)}}{\cancel{\sqrt{2 \cos^{2}{\left(x + y \right)} + 1}}}\cancel{\sqrt{2 \cos^{2}{\left(x + y \right)} + 1}}\,\text{d}A\\ & ={∬}_{D}2 \sin{\left(x + y \right)}\,\text{d}A\\ & =\int_{0}^{\pi}\int_{- x}^{x}\left(2 \sin{\left(x + y \right)}\right)\,\text{d}y\,\text{d}x\\ & =\int_{0}^{\pi}[- 2 \cos{\left(x + y \right)}]_{y=- x}^{y=x}\,\text{d}x\\ & =\int_{0}^{\pi}\left(4 \sin^{2}{\left(x \right)}\right)\,\text{d}x\\ & =[(2 x)+(- \sin{\left(2 x \right)})]_{x=0}^{x=\pi}\\ & =\left((2 \pi)+(0)-\left((0)+(0)\right)\right)\\ & =2 \pi.\end{aligned}
$$

## Original q-161340 — raw evidence, ineligible

Evaluate the surface integral 

$$
{∬}_{S}\frac{xy}{\sqrt{z}}\,\text{d}S
$$

where $S$ is defined by $z=\frac{1}{4}+{x}^{2}+{y}^{2}$ for $0\le x\le 1$ and $-2\le y\le 1.$

- $-\frac{3}{2}$
- $-\frac{3}{4}$
- $\frac{3}{2}$
- $0$
- $3$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(\frac{1}{4}+{x}^{2}+{y}^{2})=2x,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(\frac{1}{4}+{x}^{2}+{y}^{2})=2y.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{xy}{\sqrt{z}}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}\,\frac{xy}{\sqrt{\frac{1}{4}+{x}^{2}+{y}^{2}}}\sqrt{1+(2x)^{2}+(2y)^{2}}\,\text{d}A \\  & ={∬}_{D}\,\frac{xy}{\sqrt{\frac{1}{4}+{x}^{2}+{y}^{2}}}\sqrt{1+4{x}^{2}+4{y}^{2}}\,\text{d}A \\  & ={∬}_{D}\,\frac{2xy}{\sqrt{1+4{x}^{2}+4{y}^{2}}}\sqrt{1+4{x}^{2}+4{y}^{2}}\,\text{d}A \\  & ={∬}_{D}\,\frac{2xy}{\cancel{\sqrt{1+4{x}^{2}+4{y}^{2}}}}\cancel{\sqrt{1+4{x}^{2}+4{y}^{2}}}\,\text{d}A \\  & ={∬}_{D}\,2xy\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{-2}^{1}(2xy)\,\text{d}y\,\text{d}x \\  & ={\int }_{0}^{1}[x{y}^{2}]_{y=-2}^{y=1}\,\text{d}x \\  & ={\int }_{0}^{1}(-3x)\,\text{d}x \\  & ={[-\frac{3}{2}{x}^{2}]}_{0}^{1} \\  & =-\frac{3}{2}(1-0) \\  & =-\frac{3}{2}\end{aligned}
$$

### Generated raw q-161340 scale 2 — evidence only, opaque bank

Evaluate the surface integral 

$$
{∬}_{S}2\left(\frac{xy}{\sqrt{z}}\right)\,\text{d}S
$$

where $S$ is defined by $z=\frac{1}{4}+{x}^{2}+{y}^{2}$ for $0\le x\le 1$ and $-2\le y\le 1.$

- $2\left(\frac{3}{2}\right)$
- $2\left(0\right)$
- $2\left(-\frac{3}{2}\right)$
- $2\left(-\frac{3}{4}\right)$
- $2\left(3\right)$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(\frac{1}{4}+{x}^{2}+{y}^{2})=2x,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(\frac{1}{4}+{x}^{2}+{y}^{2})=2y.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}2\left(\frac{xy}{\sqrt{z}}\right)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & =2\left({∬}_{D}\,\frac{xy}{\sqrt{\frac{1}{4}+{x}^{2}+{y}^{2}}}\sqrt{1+(2x)^{2}+(2y)^{2}}\,\text{d}A\right)\\  & =2\left({∬}_{D}\,\frac{xy}{\sqrt{\frac{1}{4}+{x}^{2}+{y}^{2}}}\sqrt{1+4{x}^{2}+4{y}^{2}}\,\text{d}A\right)\\  & =2\left({∬}_{D}\,\frac{2xy}{\sqrt{1+4{x}^{2}+4{y}^{2}}}\sqrt{1+4{x}^{2}+4{y}^{2}}\,\text{d}A\right)\\  & =2\left({∬}_{D}\,\frac{2xy}{\cancel{\sqrt{1+4{x}^{2}+4{y}^{2}}}}\cancel{\sqrt{1+4{x}^{2}+4{y}^{2}}}\,\text{d}A\right)\\  & =2\left({∬}_{D}\,2xy\,\text{d}A\right)\\  & =2\left({\int }_{0}^{1}{\int }_{-2}^{1}(2xy)\,\text{d}y\,\text{d}x\right)\\  & =2\left({\int }_{0}^{1}[x{y}^{2}]_{y=-2}^{y=1}\,\text{d}x\right)\\  & =2\left({\int }_{0}^{1}(-3x)\,\text{d}x\right)\\  & =2\left({[-\frac{3}{2}{x}^{2}]}_{0}^{1}\right)\\  & =2\left(-\frac{3}{2}(1-0)\right)\\  & =2\left(-\frac{3}{2}\right)\end{aligned}
$$

### Normal paraboloid_xy at original parameters — authored bank, source-family chain

Evaluate the surface integral

$$
\iint_S \frac{x y}{\sqrt{z}}\,\mathrm{d}S
$$

where $S$ is defined by $z=x^{2} + y^{2} + \frac{1}{4}$ for $0\le x\le 1$ and $-2\le y\le 1$.

- $- \frac{3}{8}$
- $- \frac{3}{2}$
- $-3$
- $3$
- $\frac{3}{2}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(x^{2} + y^{2} + \frac{1}{4})=2 x,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(x^{2} + y^{2} + \frac{1}{4})=2 y.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{x y}{\sqrt{z}}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{x y}{\sqrt{x^{2} + y^{2} + \frac{1}{4}}}\sqrt{1+\left(2 x\right)^{2}+\left(2 y\right)^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{x y}{\sqrt{x^{2} + y^{2} + \frac{1}{4}}}\sqrt{4 x^{2} + 4 y^{2} + 1}\,\text{d}A\\ & ={∬}_{D}\frac{2 x y}{\sqrt{4 x^{2} + 4 y^{2} + 1}}\sqrt{4 x^{2} + 4 y^{2} + 1}\,\text{d}A\\ & ={∬}_{D}\frac{2 x y}{\cancel{\sqrt{4 x^{2} + 4 y^{2} + 1}}}\cancel{\sqrt{4 x^{2} + 4 y^{2} + 1}}\,\text{d}A\\ & ={∬}_{D}2 x y\,\text{d}A\\ & =\int_{0}^{1}\int_{-2}^{1}\left(2 x y\right)\,\text{d}y\,\text{d}x\\ & =\int_{0}^{1}[(x y^{2})]_{y=-2}^{y=1}\,\text{d}x\\ & =\int_{0}^{1}\left((x)-\left((4 x)\right)\right)\,\text{d}x\\ & =\int_{0}^{1}\left(- 3 x\right)\,\text{d}x\\ & =[(- \frac{3 x^{2}}{2})]_{x=0}^{x=1}\\ & =\left((- \frac{3}{2})-\left((0)\right)\right)\\ & =- \frac{3}{2}.\end{aligned}
$$

### Generated paraboloid_xy variant 1 — authored bank

Evaluate the surface integral

$$
\iint_S \frac{2 x y}{\sqrt{z}}\,\mathrm{d}S
$$

where $S$ is defined by $z=x^{2} + y^{2} + \frac{1}{4}$ for $0\le x\le 2$ and $-2\le y\le 1$.

- $12$
- $-24$
- $24$
- $-12$
- $-3$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(x^{2} + y^{2} + \frac{1}{4})=2 x,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(x^{2} + y^{2} + \frac{1}{4})=2 y.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{2 x y}{\sqrt{z}}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{2 x y}{\sqrt{x^{2} + y^{2} + \frac{1}{4}}}\sqrt{1+\left(2 x\right)^{2}+\left(2 y\right)^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{2 x y}{\sqrt{x^{2} + y^{2} + \frac{1}{4}}}\sqrt{4 x^{2} + 4 y^{2} + 1}\,\text{d}A\\ & ={∬}_{D}\frac{4 x y}{\sqrt{4 x^{2} + 4 y^{2} + 1}}\sqrt{4 x^{2} + 4 y^{2} + 1}\,\text{d}A\\ & ={∬}_{D}\frac{4 x y}{\cancel{\sqrt{4 x^{2} + 4 y^{2} + 1}}}\cancel{\sqrt{4 x^{2} + 4 y^{2} + 1}}\,\text{d}A\\ & ={∬}_{D}4 x y\,\text{d}A\\ & =\int_{0}^{2}\int_{-2}^{1}\left(4 x y\right)\,\text{d}y\,\text{d}x\\ & =\int_{0}^{2}[(2 x y^{2})]_{y=-2}^{y=1}\,\text{d}x\\ & =\int_{0}^{2}\left((2 x)-\left((8 x)\right)\right)\,\text{d}x\\ & =\int_{0}^{2}\left(- 6 x\right)\,\text{d}x\\ & =[(- 3 x^{2})]_{x=0}^{x=2}\\ & =\left((-12)-\left((0)\right)\right)\\ & =-12.\end{aligned}
$$

### Generated paraboloid_xy variant 2 — authored bank

Evaluate the surface integral

$$
\iint_S \frac{2 x y}{\sqrt{z}}\,\mathrm{d}S
$$

where $S$ is defined by $z=x^{2} + y^{2} + \frac{1}{4}$ for $0\le x\le 1$ and $-2\le y\le 1$.

- $3$
- $-3$
- $-6$
- $- \frac{3}{4}$
- $6$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(x^{2} + y^{2} + \frac{1}{4})=2 x,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(x^{2} + y^{2} + \frac{1}{4})=2 y.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{2 x y}{\sqrt{z}}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{2 x y}{\sqrt{x^{2} + y^{2} + \frac{1}{4}}}\sqrt{1+\left(2 x\right)^{2}+\left(2 y\right)^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{2 x y}{\sqrt{x^{2} + y^{2} + \frac{1}{4}}}\sqrt{4 x^{2} + 4 y^{2} + 1}\,\text{d}A\\ & ={∬}_{D}\frac{4 x y}{\sqrt{4 x^{2} + 4 y^{2} + 1}}\sqrt{4 x^{2} + 4 y^{2} + 1}\,\text{d}A\\ & ={∬}_{D}\frac{4 x y}{\cancel{\sqrt{4 x^{2} + 4 y^{2} + 1}}}\cancel{\sqrt{4 x^{2} + 4 y^{2} + 1}}\,\text{d}A\\ & ={∬}_{D}4 x y\,\text{d}A\\ & =\int_{0}^{1}\int_{-2}^{1}\left(4 x y\right)\,\text{d}y\,\text{d}x\\ & =\int_{0}^{1}[(2 x y^{2})]_{y=-2}^{y=1}\,\text{d}x\\ & =\int_{0}^{1}\left((2 x)-\left((8 x)\right)\right)\,\text{d}x\\ & =\int_{0}^{1}\left(- 6 x\right)\,\text{d}x\\ & =[(- 3 x^{2})]_{x=0}^{x=1}\\ & =\left((-3)-\left((0)\right)\right)\\ & =-3.\end{aligned}
$$

## Original q-161341 — raw evidence, ineligible

Evaluate the surface integral 

$$
{∬}_{S}4z\,\text{d}S
$$

where $S$ is defined by $z=x+y$ for $0\le x\le 1$ and $0\le y\le 1.$

- $2\sqrt{3}-1$
- $\frac{\sqrt{3}}{4}$
- $2\sqrt{3}$
- $\sqrt{3}-1$
- $4\sqrt{3}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(x+y)=1,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(x+y)=1.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}4z\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}\,4(x+y)\,\sqrt{1+{1}^{2}+{1}^{2}}\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{0}^{1}4(x+y)\sqrt{3}\,\text{d}y\,\text{d}x \\  & =\sqrt{3}{\int }_{0}^{1}{[4xy+2{y}^{2}]}_{y=0}^{y=1}\,\text{d}x \\  & =\sqrt{3}{\int }_{0}^{1}(4x+2)\,\text{d}x \\  & =\sqrt{3}{[2{x}^{2}+2x]}_{0}^{1} \\  & =4\sqrt{3}\end{aligned}
$$

### Generated raw q-161341 scale 2 — evidence only, opaque bank

Evaluate the surface integral 

$$
{∬}_{S}2\left(4z\right)\,\text{d}S
$$

where $S$ is defined by $z=x+y$ for $0\le x\le 1$ and $0\le y\le 1.$

- $2\left(2\sqrt{3}\right)$
- $2\left(\sqrt{3}-1\right)$
- $2\left(2\sqrt{3}-1\right)$
- $2\left(\frac{\sqrt{3}}{4}\right)$
- $2\left(4\sqrt{3}\right)$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(x+y)=1,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(x+y)=1.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}2\left(4z\right)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & =2\left({∬}_{D}\,4(x+y)\,\sqrt{1+{1}^{2}+{1}^{2}}\,\text{d}A\right)\\  & =2\left({\int }_{0}^{1}{\int }_{0}^{1}4(x+y)\sqrt{3}\,\text{d}y\,\text{d}x\right)\\  & =2\left(\sqrt{3}{\int }_{0}^{1}{[4xy+2{y}^{2}]}_{y=0}^{y=1}\,\text{d}x\right)\\  & =2\left(\sqrt{3}{\int }_{0}^{1}(4x+2)\,\text{d}x\right)\\  & =2\left(\sqrt{3}{[2{x}^{2}+2x]}_{0}^{1}\right)\\  & =2\left(4\sqrt{3}\right)\end{aligned}
$$

### Normal plane_linear at original parameters — authored bank, source-family chain

Evaluate the surface integral

$$
\iint_S 4 z\,\mathrm{d}S
$$

where $S$ is defined by $z=x + y$ for $0\le x\le 1$ and $0\le y\le 1$.

- $- 4 \sqrt{3}$
- $4 \sqrt{3}$
- $0$
- $12$
- $4$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(x + y)=1,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(x + y)=1.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}4 z\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\left(4 x + 4 y\right)\sqrt{1+\left(1\right)^{2}+\left(1\right)^{2}}\,\text{d}A\\ & =\int_{0}^{1}\int_{0}^{1}\left(\sqrt{3} \left(4 x + 4 y\right)\right)\,\text{d}y\,\text{d}x\\ & =\sqrt{3}\int_{0}^{1}[(4 x y)+(2 y^{2})]_{y=0}^{y=1}\,\text{d}x\\ & =\sqrt{3}\int_{0}^{1}\left((4 x)+(2)-\left((0)+(0)\right)\right)\,\text{d}x\\ & =\sqrt{3}\int_{0}^{1}\left(4 x + 2\right)\,\text{d}x\\ & =\sqrt{3}[(2 x)+(2 x^{2})]_{x=0}^{x=1}\\ & =\sqrt{3}\left((2)+(2)-\left((0)+(0)\right)\right)\\ & =4 \sqrt{3}.\end{aligned}
$$

### Generated plane_linear variant 1 — authored bank

Evaluate the surface integral

$$
\iint_S 2 z\,\mathrm{d}S
$$

where $S$ is defined by $z=2 x + 2 y$ for $0\le x\le 2$ and $0\le y\le 2$.

- $32$
- $0$
- $288$
- $96$
- $-96$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x + 2 y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x + 2 y)=2.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}2 z\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\left(4 x + 4 y\right)\sqrt{1+\left(2\right)^{2}+\left(2\right)^{2}}\,\text{d}A\\ & =\int_{0}^{2}\int_{0}^{2}\left(12 x + 12 y\right)\,\text{d}y\,\text{d}x\\ & =3\int_{0}^{2}[(4 x y)+(2 y^{2})]_{y=0}^{y=2}\,\text{d}x\\ & =3\int_{0}^{2}\left((8 x)+(8)-\left((0)+(0)\right)\right)\,\text{d}x\\ & =3\int_{0}^{2}\left(8 x + 8\right)\,\text{d}x\\ & =3[(8 x)+(4 x^{2})]_{x=0}^{x=2}\\ & =3\left((16)+(16)-\left((0)+(0)\right)\right)\\ & =96.\end{aligned}
$$

### Generated plane_linear variant 2 — authored bank

Evaluate the surface integral

$$
\iint_S 2 z\,\mathrm{d}S
$$

where $S$ is defined by $z=2 x + 2 y$ for $0\le x\le 1$ and $0\le y\le 1$.

- $4$
- $12$
- $0$
- $-12$
- $36$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x + 2 y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x + 2 y)=2.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}2 z\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\left(4 x + 4 y\right)\sqrt{1+\left(2\right)^{2}+\left(2\right)^{2}}\,\text{d}A\\ & =\int_{0}^{1}\int_{0}^{1}\left(12 x + 12 y\right)\,\text{d}y\,\text{d}x\\ & =3\int_{0}^{1}[(4 x y)+(2 y^{2})]_{y=0}^{y=1}\,\text{d}x\\ & =3\int_{0}^{1}\left((4 x)+(2)-\left((0)+(0)\right)\right)\,\text{d}x\\ & =3\int_{0}^{1}\left(4 x + 2\right)\,\text{d}x\\ & =3[(2 x)+(2 x^{2})]_{x=0}^{x=1}\\ & =3\left((2)+(2)-\left((0)+(0)\right)\right)\\ & =12.\end{aligned}
$$

## Original q-161347 — raw evidence, ineligible

Evaluate the surface integral 

$$
{∬}_{S}\frac{z-y}{\sqrt{6}y}\,\text{d}S
$$

where $S$ is defined by $z=2x+y$ for $1\le x\le 2$ and $1\le y\le e.$

- $\frac{\sqrt{6}}{2}$
- $4\sqrt{6}$
- $e-1$
- $3$
- $e+3$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2x+y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2x+y)=1.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{z-y}{\sqrt{6}y}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}\,\frac{(2x+y)-y}{\sqrt{6}y}\sqrt{1+{2}^{2}+{1}^{2}}\,\text{d}A \\  & ={∬}_{D}\,\frac{2x}{y}\,\text{d}A \\  & ={\int }_{1}^{2}{\int }_{1}^{e}\frac{2x}{y}\,\text{d}y\,\text{d}x \\  & ={\int }_{1}^{2}2x[\operatorname{ln}⁡y]_{y=1}^{y=e}\,\text{d}x \\  & ={\int }_{1}^{2}2x\,\text{d}x \\  & =[{x}^{2}]_{1}^{2} \\  & =4-1 \\  & =3\end{aligned}
$$

### Generated raw q-161347 scale 2 — evidence only, opaque bank

Evaluate the surface integral 

$$
{∬}_{S}2\left(\frac{z-y}{\sqrt{6}y}\right)\,\text{d}S
$$

where $S$ is defined by $z=2x+y$ for $1\le x\le 2$ and $1\le y\le e.$

- $2\left(e-1\right)$
- $2\left(3\right)$
- $2\left(\frac{\sqrt{6}}{2}\right)$
- $2\left(4\sqrt{6}\right)$
- $2\left(e+3\right)$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2x+y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2x+y)=1.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}2\left(\frac{z-y}{\sqrt{6}y}\right)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & =2\left({∬}_{D}\,\frac{(2x+y)-y}{\sqrt{6}y}\sqrt{1+{2}^{2}+{1}^{2}}\,\text{d}A\right)\\  & =2\left({∬}_{D}\,\frac{2x}{y}\,\text{d}A\right)\\  & =2\left({\int }_{1}^{2}{\int }_{1}^{e}\frac{2x}{y}\,\text{d}y\,\text{d}x\right)\\  & =2\left({\int }_{1}^{2}2x[\operatorname{ln}⁡y]_{y=1}^{y=e}\,\text{d}x\right)\\  & =2\left({\int }_{1}^{2}2x\,\text{d}x\right)\\  & =2\left([{x}^{2}]_{1}^{2}\right)\\  & =2\left(4-1\right)\\  & =2\left(3\right)\end{aligned}
$$

### Normal plane_log at original parameters — authored bank, source-family chain

Evaluate the surface integral

$$
\iint_S \frac{z-\left(y\right)}{\left(\sqrt{6}\right)y}\,\mathrm{d}S
$$

where $S$ is defined by $z=2 x + y$ for $1\le x\le 2$ and $1\le y\le e$.

- $\frac{5}{4}$
- $3$
- $6$
- $3 - \frac{3}{e}$
- $-3$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x + y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x + y)=1.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{z-\left(y\right)}{\left(\sqrt{6}\right)y}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{\left(\left(2 x + y\right)-\left(y\right)\right)}{\left(\sqrt{6}\right)y}\sqrt{1+\left(2\right)^{2}+\left(1\right)^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{2 x}{y}\,\text{d}A\\ & =\int_{1}^{2}\int_{1}^{e}\left(\frac{2 x}{y}\right)\,\text{d}y\,\text{d}x\\ & =\int_{1}^{2}\left(2 x\right)[\ln y]_{y=1}^{y=e}\,\text{d}x\\ & =\int_{1}^{2}\left(2 x\right)\left(1-\left(0\right)\right)\,\text{d}x\\ & =\int_{1}^{2}2 x\,\text{d}x\\ & =[(x^{2})]_{x=1}^{x=2}\\ & =\left((4)-\left((1)\right)\right)\\ & =3.\end{aligned}
$$

### Generated plane_log variant 1 — authored bank

Evaluate the surface integral

$$
\iint_S \frac{2\left(z-\left(2 y\right)\right)}{\left(3\right)y}\,\mathrm{d}S
$$

where $S$ is defined by $z=2 x + 2 y$ for $1\le x\le 2$ and $1\le y\le e^{2}$.

- $-12$
- $24$
- $6 - \frac{6}{e^{2}}$
- $12$
- $5$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x + 2 y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x + 2 y)=2.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{2\left(z-\left(2 y\right)\right)}{\left(3\right)y}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{\left(2\right)\left(\left(2 x + 2 y\right)-\left(2 y\right)\right)}{\left(3\right)y}\sqrt{1+\left(2\right)^{2}+\left(2\right)^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{4 x}{y}\,\text{d}A\\ & =\int_{1}^{2}\int_{1}^{e^{2}}\left(\frac{4 x}{y}\right)\,\text{d}y\,\text{d}x\\ & =\int_{1}^{2}\left(4 x\right)[\ln y]_{y=1}^{y=e^{2}}\,\text{d}x\\ & =\int_{1}^{2}\left(4 x\right)\left(2-\left(0\right)\right)\,\text{d}x\\ & =\int_{1}^{2}8 x\,\text{d}x\\ & =[(4 x^{2})]_{x=1}^{x=2}\\ & =\left((16)-\left((4)\right)\right)\\ & =12.\end{aligned}
$$

### Generated plane_log variant 2 — authored bank

Evaluate the surface integral

$$
\iint_S \frac{2\left(z-\left(2 y\right)\right)}{\left(3\right)y}\,\mathrm{d}S
$$

where $S$ is defined by $z=2 x + 2 y$ for $1\le x\le 2$ and $1\le y\le e$.

- $-6$
- $6$
- $12$
- $\frac{5}{2}$
- $6 - \frac{6}{e}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x + 2 y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x + 2 y)=2.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{2\left(z-\left(2 y\right)\right)}{\left(3\right)y}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{\left(2\right)\left(\left(2 x + 2 y\right)-\left(2 y\right)\right)}{\left(3\right)y}\sqrt{1+\left(2\right)^{2}+\left(2\right)^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{4 x}{y}\,\text{d}A\\ & =\int_{1}^{2}\int_{1}^{e}\left(\frac{4 x}{y}\right)\,\text{d}y\,\text{d}x\\ & =\int_{1}^{2}\left(4 x\right)[\ln y]_{y=1}^{y=e}\,\text{d}x\\ & =\int_{1}^{2}\left(4 x\right)\left(1-\left(0\right)\right)\,\text{d}x\\ & =\int_{1}^{2}4 x\,\text{d}x\\ & =[(2 x^{2})]_{x=1}^{x=2}\\ & =\left((8)-\left((2)\right)\right)\\ & =6.\end{aligned}
$$

## Original q-161348 — raw evidence, ineligible

Evaluate the surface integral 

$$
{∬}_{S}({x}^{2}+{z}^{2})\,\text{d}S
$$

where $S$ is defined by $z=5x-y$ for $0\le x\le 1$ and $0\le y\le 2x.$

- $25\sqrt{3}$
- $26\sqrt{3}$
- $5+\sqrt{3}$
- $25+\sqrt{3}$
- $\frac{10}{3}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(5x-y)=5,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(5x-y)=-1.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}({x}^{2}+{z}^{2})\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}\,({x}^{2}+(5x-y)^{2})\sqrt{1+{5}^{2}+(-1)^{2}}\,\text{d}A \\  & ={∬}_{D}\,({x}^{2}+25{x}^{2}+{y}^{2}-10xy)\sqrt{27}\,\text{d}A \\  & =3\sqrt{3}{∬}_{D}\,(26{x}^{2}+{y}^{2}-10xy)\,\text{d}A \\  & =3\sqrt{3}{\int }_{0}^{1}{\int }_{0}^{2x}(26{x}^{2}+{y}^{2}-10xy)\,\text{d}y\,\text{d}x \\  & =3\sqrt{3}{\int }_{0}^{1}{[26{x}^{2}y+\frac{{y}^{3}}{3}-5x{y}^{2}]}_{y=0}^{y=2x}\,\text{d}x \\  & =3\sqrt{3}{\int }_{0}^{1}(52{x}^{3}+\frac{8{x}^{3}}{3}-20{x}^{3})\,\text{d}x \\  & =3\sqrt{3}{\int }_{0}^{1}\frac{104{x}^{3}}{3}\,\text{d}x \\  & =\sqrt{3}{\int }_{0}^{1}104{x}^{3}\,\text{d}x \\  & =\sqrt{3}[26{x}^{4}]_{0}^{1} \\  & =26\sqrt{3}\end{aligned}
$$

### Generated raw q-161348 scale 2 — evidence only, opaque bank

Evaluate the surface integral 

$$
{∬}_{S}2\left(({x}^{2}+{z}^{2})\right)\,\text{d}S
$$

where $S$ is defined by $z=5x-y$ for $0\le x\le 1$ and $0\le y\le 2x.$

- $2\left(5+\sqrt{3}\right)$
- $2\left(25+\sqrt{3}\right)$
- $2\left(25\sqrt{3}\right)$
- $2\left(26\sqrt{3}\right)$
- $2\left(\frac{10}{3}\right)$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(5x-y)=5,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(5x-y)=-1.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}2\left(({x}^{2}+{z}^{2})\right)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & =2\left({∬}_{D}\,({x}^{2}+(5x-y)^{2})\sqrt{1+{5}^{2}+(-1)^{2}}\,\text{d}A\right)\\  & =2\left({∬}_{D}\,({x}^{2}+25{x}^{2}+{y}^{2}-10xy)\sqrt{27}\,\text{d}A\right)\\  & =2\left(3\sqrt{3}{∬}_{D}\,(26{x}^{2}+{y}^{2}-10xy)\,\text{d}A\right)\\  & =2\left(3\sqrt{3}{\int }_{0}^{1}{\int }_{0}^{2x}(26{x}^{2}+{y}^{2}-10xy)\,\text{d}y\,\text{d}x\right)\\  & =2\left(3\sqrt{3}{\int }_{0}^{1}{[26{x}^{2}y+\frac{{y}^{3}}{3}-5x{y}^{2}]}_{y=0}^{y=2x}\,\text{d}x\right)\\  & =2\left(3\sqrt{3}{\int }_{0}^{1}(52{x}^{3}+\frac{8{x}^{3}}{3}-20{x}^{3})\,\text{d}x\right)\\  & =2\left(3\sqrt{3}{\int }_{0}^{1}\frac{104{x}^{3}}{3}\,\text{d}x\right)\\  & =2\left(\sqrt{3}{\int }_{0}^{1}104{x}^{3}\,\text{d}x\right)\\  & =2\left(\sqrt{3}[26{x}^{4}]_{0}^{1}\right)\\  & =2\left(26\sqrt{3}\right)\end{aligned}
$$

### Normal quadratic_triangle at original parameters — authored bank, source-family chain

Evaluate the surface integral

$$
\iint_S \left(x^{2} + z^{2}\right)\,\mathrm{d}S
$$

where $S$ is defined by $z=5 x - y$ for $0\le x\le 1$ and $0\le y\le 2 x$.

- $- 26 \sqrt{3}$
- $26 \sqrt{3}$
- $\frac{3 \sqrt{3}}{2}$
- $234$
- $\frac{26}{3}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(5 x - y)=5,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(5 x - y)=-1.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\left(x^{2} + z^{2}\right)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\left(x^{2} + \left(5 x - y\right)^{2}\right)\sqrt{1+\left(5\right)^{2}+\left(-1\right)^{2}}\,\text{d}A\\ & ={∬}_{D}\left((x^{2})+(25 x^{2})+(y^{2})+(- 10 x y)\right)\sqrt{27}\,\text{d}A\\ & =3 \sqrt{3}{∬}_{D}\left(26 x^{2} - 10 x y + y^{2}\right)\,\text{d}A\\ & =3 \sqrt{3}\int_{0}^{1}\int_{0}^{2 x}\left(26 x^{2} - 10 x y + y^{2}\right)\,\text{d}y\,\text{d}x\\ & =3 \sqrt{3}\int_{0}^{1}[(\frac{y^{3}}{3})+(26 x^{2} y)+(- 5 x y^{2})]_{y=0}^{y=2 x}\,\text{d}x\\ & =3 \sqrt{3}\int_{0}^{1}\left((\frac{8 x^{3}}{3})+(52 x^{3})+(- 20 x^{3})-\left((0)+(0)+(0)\right)\right)\,\text{d}x\\ & =3 \sqrt{3}\int_{0}^{1}\left(\frac{104 x^{3}}{3}\right)\,\text{d}x\\ & =\sqrt{3}\int_{0}^{1}104 x^{3}\,\text{d}x\\ & =\sqrt{3}[(26 x^{4})]_{x=0}^{x=1}\\ & =\sqrt{3}\left((26)-\left((0)\right)\right)\\ & =26 \sqrt{3}.\end{aligned}
$$

### Generated quadratic_triangle variant 1 — authored bank

Evaluate the surface integral

$$
\iint_S \left(2 x^{2} + 2 z^{2}\right)\,\mathrm{d}S
$$

where $S$ is defined by $z=2 x - 2 y$ for $0\le x\le 2$ and $0\le y\le 2 x$.

- $\frac{112}{3}$
- $48$
- $336$
- $112$
- $-112$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x - 2 y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x - 2 y)=-2.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\left(2 x^{2} + 2 z^{2}\right)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\left(2 x^{2} + 2 \left(2 x - 2 y\right)^{2}\right)\sqrt{1+\left(2\right)^{2}+\left(-2\right)^{2}}\,\text{d}A\\ & ={∬}_{D}\left(2\right)\left((x^{2})+(4 x^{2})+(4 y^{2})+(- 8 x y)\right)\sqrt{9}\,\text{d}A\\ & =3{∬}_{D}\left(10 x^{2} - 16 x y + 8 y^{2}\right)\,\text{d}A\\ & =3\int_{0}^{2}\int_{0}^{2 x}\left(10 x^{2} - 16 x y + 8 y^{2}\right)\,\text{d}y\,\text{d}x\\ & =3\int_{0}^{2}[(\frac{8 y^{3}}{3})+(10 x^{2} y)+(- 8 x y^{2})]_{y=0}^{y=2 x}\,\text{d}x\\ & =3\int_{0}^{2}\left((\frac{64 x^{3}}{3})+(20 x^{3})+(- 32 x^{3})-\left((0)+(0)+(0)\right)\right)\,\text{d}x\\ & =3\int_{0}^{2}\left(\frac{28 x^{3}}{3}\right)\,\text{d}x\\ & =1\int_{0}^{2}28 x^{3}\,\text{d}x\\ & =1[(7 x^{4})]_{x=0}^{x=2}\\ & =1\left((112)-\left((0)\right)\right)\\ & =112.\end{aligned}
$$

### Generated quadratic_triangle variant 2 — authored bank

Evaluate the surface integral

$$
\iint_S \left(2 x^{2} + 2 z^{2}\right)\,\mathrm{d}S
$$

where $S$ is defined by $z=2 x - 2 y$ for $0\le x\le 1$ and $0\le y\le x$.

- $\frac{7}{6}$
- $\frac{7}{2}$
- $\frac{3}{2}$
- $- \frac{7}{2}$
- $\frac{21}{2}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x - 2 y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x - 2 y)=-2.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\left(2 x^{2} + 2 z^{2}\right)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\left(2 x^{2} + 2 \left(2 x - 2 y\right)^{2}\right)\sqrt{1+\left(2\right)^{2}+\left(-2\right)^{2}}\,\text{d}A\\ & ={∬}_{D}\left(2\right)\left((x^{2})+(4 x^{2})+(4 y^{2})+(- 8 x y)\right)\sqrt{9}\,\text{d}A\\ & =3{∬}_{D}\left(10 x^{2} - 16 x y + 8 y^{2}\right)\,\text{d}A\\ & =3\int_{0}^{1}\int_{0}^{x}\left(10 x^{2} - 16 x y + 8 y^{2}\right)\,\text{d}y\,\text{d}x\\ & =3\int_{0}^{1}[(\frac{8 y^{3}}{3})+(10 x^{2} y)+(- 8 x y^{2})]_{y=0}^{y=x}\,\text{d}x\\ & =3\int_{0}^{1}\left((\frac{8 x^{3}}{3})+(10 x^{3})+(- 8 x^{3})-\left((0)+(0)+(0)\right)\right)\,\text{d}x\\ & =3\int_{0}^{1}\left(\frac{14 x^{3}}{3}\right)\,\text{d}x\\ & =1\int_{0}^{1}14 x^{3}\,\text{d}x\\ & =1[(\frac{7 x^{4}}{2})]_{x=0}^{x=1}\\ & =1\left((\frac{7}{2})-\left((0)\right)\right)\\ & =\frac{7}{2}.\end{aligned}
$$

## Original q-161352 — raw evidence, ineligible

Evaluate the surface integral 

$$
{∬}_{S}\frac{z}{36x}\,\text{d}S
$$

where $S$ is defined by $z=4x+8y$ for $1\le x\le 2$ and $0\le y\le x.$

- $\frac{5}{2}$
- $18$
- $1$
- $3$
- $9$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(4x+8y)=4,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(4x+8y)=8.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{z}{36x}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}\,\frac{4x+8y}{36x}\sqrt{1+{4}^{2}+{8}^{2}}\,\text{d}A \\  & ={∬}_{D}\,9\frac{4(x+2y)}{36x}\,\text{d}A \\  & ={∬}_{D}\,\frac{x+2y}{x}\,\text{d}A \\  & ={\int }_{1}^{2}{\int }_{0}^{x}(1+\frac{2y}{x})\,\text{d}y\,\text{d}x \\  & ={\int }_{1}^{2}{[y+\frac{{y}^{2}}{x}]}_{0}^{x}\,\text{d}x \\  & ={\int }_{1}^{2}(x+\frac{{x}^{2}}{x}-0)\,\text{d}x \\  & ={\int }_{1}^{2}2x\,\text{d}x \\  & =[{x}^{2}]_{1}^{2} \\  & =4-1 \\  & =3\end{aligned}
$$

### Generated raw q-161352 scale 2 — evidence only, opaque bank

Evaluate the surface integral 

$$
{∬}_{S}2\left(\frac{z}{36x}\right)\,\text{d}S
$$

where $S$ is defined by $z=4x+8y$ for $1\le x\le 2$ and $0\le y\le x.$

- $2\left(1\right)$
- $2\left(3\right)$
- $2\left(\frac{5}{2}\right)$
- $2\left(18\right)$
- $2\left(9\right)$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(4x+8y)=4,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(4x+8y)=8.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}2\left(\frac{z}{36x}\right)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & =2\left({∬}_{D}\,\frac{4x+8y}{36x}\sqrt{1+{4}^{2}+{8}^{2}}\,\text{d}A\right)\\  & =2\left({∬}_{D}\,9\frac{4(x+2y)}{36x}\,\text{d}A\right)\\  & =2\left({∬}_{D}\,\frac{x+2y}{x}\,\text{d}A\right)\\  & =2\left({\int }_{1}^{2}{\int }_{0}^{x}(1+\frac{2y}{x})\,\text{d}y\,\text{d}x\right)\\  & =2\left({\int }_{1}^{2}{[y+\frac{{y}^{2}}{x}]}_{0}^{x}\,\text{d}x\right)\\  & =2\left({\int }_{1}^{2}(x+\frac{{x}^{2}}{x}-0)\,\text{d}x\right)\\  & =2\left({\int }_{1}^{2}2x\,\text{d}x\right)\\  & =2\left([{x}^{2}]_{1}^{2}\right)\\  & =2\left(4-1\right)\\  & =2\left(3\right)\end{aligned}
$$

### Normal plane_ratio at original parameters — authored bank, source-family chain

Evaluate the surface integral

$$
\iint_S \frac{z}{\left(36\right)x}\,\mathrm{d}S
$$

where $S$ is defined by $z=4 x + 8 y$ for $1\le x\le 2$ and $0\le y\le x$.

- $\frac{5}{4}$
- $3$
- $6$
- $\frac{9}{2}$
- $-3$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(4 x + 8 y)=4,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(4 x + 8 y)=8.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{z}{\left(36\right)x}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{1\left(4 x + 8 y\right)}{\left(36\right)x}\sqrt{1+\left(4\right)^{2}+\left(8\right)^{2}}\,\text{d}A\\ & ={∬}_{D}\left(9\right)\frac{\left(4\right)\left(x+\left(2\right)y\right)}{\left(36\right)x}\,\text{d}A\\ & ={∬}_{D}\frac{\left(1\right)\left(x+\left(2\right)y\right)}{x}\,\text{d}A\\ & =\int_{1}^{2}\int_{0}^{x}\left(1 + \frac{2 y}{x}\right)\,\text{d}y\,\text{d}x\\ & =\int_{1}^{2}[(y)+(\frac{y^{2}}{x})]_{y=0}^{y=x}\,\text{d}x\\ & =\int_{1}^{2}\left((x)+(x)-\left((0)+(0)\right)\right)\,\text{d}x\\ & =\int_{1}^{2}\left(2 x\right)\,\text{d}x\\ & =[(x^{2})]_{x=1}^{x=2}\\ & =\left((4)-\left((1)\right)\right)\\ & =3.\end{aligned}
$$

### Generated plane_ratio variant 1 — authored bank

Evaluate the surface integral

$$
\iint_S \frac{2 z}{\left(6\right)x}\,\mathrm{d}S
$$

where $S$ is defined by $z=2 x + 2 y$ for $1\le x\le 2$ and $0\le y\le 2 x$.

- $-12$
- $24$
- $18$
- $12$
- $5$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x + 2 y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x + 2 y)=2.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{2 z}{\left(6\right)x}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{2\left(2 x + 2 y\right)}{\left(6\right)x}\sqrt{1+\left(2\right)^{2}+\left(2\right)^{2}}\,\text{d}A\\ & ={∬}_{D}\left(3\right)\frac{\left(4\right)\left(x+\left(1\right)y\right)}{\left(6\right)x}\,\text{d}A\\ & ={∬}_{D}\frac{\left(2\right)\left(x+\left(1\right)y\right)}{x}\,\text{d}A\\ & =\int_{1}^{2}\int_{0}^{2 x}\left(2 + \frac{2 y}{x}\right)\,\text{d}y\,\text{d}x\\ & =\int_{1}^{2}[(2 y)+(\frac{y^{2}}{x})]_{y=0}^{y=2 x}\,\text{d}x\\ & =\int_{1}^{2}\left((4 x)+(4 x)-\left((0)+(0)\right)\right)\,\text{d}x\\ & =\int_{1}^{2}\left(8 x\right)\,\text{d}x\\ & =[(4 x^{2})]_{x=1}^{x=2}\\ & =\left((16)-\left((4)\right)\right)\\ & =12.\end{aligned}
$$

### Generated plane_ratio variant 2 — authored bank

Evaluate the surface integral

$$
\iint_S \frac{2 z}{\left(6\right)x}\,\mathrm{d}S
$$

where $S$ is defined by $z=2 x + 2 y$ for $1\le x\le 2$ and $0\le y\le x$.

- $- \frac{9}{2}$
- $\frac{9}{2}$
- $9$
- $\frac{15}{8}$
- $6$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x + 2 y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x + 2 y)=2.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{2 z}{\left(6\right)x}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{2\left(2 x + 2 y\right)}{\left(6\right)x}\sqrt{1+\left(2\right)^{2}+\left(2\right)^{2}}\,\text{d}A\\ & ={∬}_{D}\left(3\right)\frac{\left(4\right)\left(x+\left(1\right)y\right)}{\left(6\right)x}\,\text{d}A\\ & ={∬}_{D}\frac{\left(2\right)\left(x+\left(1\right)y\right)}{x}\,\text{d}A\\ & =\int_{1}^{2}\int_{0}^{x}\left(2 + \frac{2 y}{x}\right)\,\text{d}y\,\text{d}x\\ & =\int_{1}^{2}[(2 y)+(\frac{y^{2}}{x})]_{y=0}^{y=x}\,\text{d}x\\ & =\int_{1}^{2}\left((2 x)+(x)-\left((0)+(0)\right)\right)\,\text{d}x\\ & =\int_{1}^{2}\left(3 x\right)\,\text{d}x\\ & =[(\frac{3 x^{2}}{2})]_{x=1}^{x=2}\\ & =\left((6)-\left((\frac{3}{2})\right)\right)\\ & =\frac{9}{2}.\end{aligned}
$$

## Original q-161353 — raw evidence, ineligible

Evaluate the surface integral 

$$
{∬}_{S}\frac{1}{\sqrt{3}{z}^{2}}\,\text{d}S
$$

where $S$ is defined by $z=1+x+y$ for $0\le x\le \frac{1}{2}$ and $-x\le y\le 0.$

- $\operatorname{ln}⁡2-\operatorname{ln}⁡3-\frac{1}{2}$
- $\operatorname{ln}⁡2-\operatorname{ln}⁡3+\frac{1}{2}$
- $\operatorname{ln}⁡2+\operatorname{ln}⁡3+1$
- $\operatorname{ln}⁡2+\operatorname{ln}⁡3+\frac{1}{2}$
- $\operatorname{ln}⁡2+\operatorname{ln}⁡3-\frac{1}{2}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(1+x+y)=1,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(1+x+y)=1.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{1}{\sqrt{3}{z}^{2}}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}\,\frac{1}{\sqrt{3}(1+x+y)^{2}}\sqrt{1+{1}^{2}+{1}^{2}}\,\text{d}A \\  & ={\int }_{0}^{1/2}{\int }_{-x}^{0}\,\frac{1}{(1+x+y)^{2}}\,\text{d}y\,\text{d}x \\  & ={\int }_{0}^{1/2}{[-\frac{1}{1+x+y}]}_{y=-x}^{y=0}\,\text{d}x \\  & ={\int }_{0}^{1/2}(-\frac{1}{1+x}+1)\text{d}x \\  & =[-\operatorname{ln}⁡(x+1)+x]_{0}^{1/2} \\  & =-\operatorname{ln}⁡(\frac{3}{2})+\frac{1}{2}-0 \\  & =\operatorname{ln}⁡2-\operatorname{ln}⁡3+\frac{1}{2}\end{aligned}
$$

### Generated raw q-161353 scale 2 — evidence only, opaque bank

Evaluate the surface integral 

$$
{∬}_{S}2\left(\frac{1}{\sqrt{3}{z}^{2}}\right)\,\text{d}S
$$

where $S$ is defined by $z=1+x+y$ for $0\le x\le \frac{1}{2}$ and $-x\le y\le 0.$

- $2\left(\operatorname{ln}⁡2+\operatorname{ln}⁡3+1\right)$
- $2\left(\operatorname{ln}⁡2+\operatorname{ln}⁡3+\frac{1}{2}\right)$
- $2\left(\operatorname{ln}⁡2-\operatorname{ln}⁡3-\frac{1}{2}\right)$
- $2\left(\operatorname{ln}⁡2-\operatorname{ln}⁡3+\frac{1}{2}\right)$
- $2\left(\operatorname{ln}⁡2+\operatorname{ln}⁡3-\frac{1}{2}\right)$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(1+x+y)=1,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(1+x+y)=1.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}2\left(\frac{1}{\sqrt{3}{z}^{2}}\right)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & =2\left({∬}_{D}\,\frac{1}{\sqrt{3}(1+x+y)^{2}}\sqrt{1+{1}^{2}+{1}^{2}}\,\text{d}A\right)\\  & =2\left({\int }_{0}^{1/2}{\int }_{-x}^{0}\,\frac{1}{(1+x+y)^{2}}\,\text{d}y\,\text{d}x\right)\\  & =2\left({\int }_{0}^{1/2}{[-\frac{1}{1+x+y}]}_{y=-x}^{y=0}\,\text{d}x\right)\\  & =2\left({\int }_{0}^{1/2}(-\frac{1}{1+x}+1)\text{d}x\right)\\  & =2\left([-\operatorname{ln}⁡(x+1)+x]_{0}^{1/2}\right)\\  & =2\left(-\operatorname{ln}⁡(\frac{3}{2})+\frac{1}{2}-0\right)\\  & =2\left(\operatorname{ln}⁡2-\operatorname{ln}⁡3+\frac{1}{2}\right)\end{aligned}
$$

### Normal reciprocal_triangle at original parameters — authored bank, source-family chain

Evaluate the surface integral

$$
\iint_S \frac{1}{\sqrt{3}z^{2}}\,\mathrm{d}S
$$

where $S$ is defined by $z=x + y + 1$ for $0\le x\le \frac{1}{2}$ and $- x\le y\le 0$.

- $\frac{1}{4} - \ln{\left(\frac{5}{4} \right)}$
- $\frac{1}{2} - \ln{\left(\frac{3}{2} \right)}$
- $1 - \ln{\left(\frac{9}{4} \right)}$
- $- \frac{1}{3} + \ln{\left(\frac{3}{2} \right)}$
- $- \frac{1}{2} + \ln{\left(\frac{3}{2} \right)}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(x + y + 1)=1,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(x + y + 1)=1.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{1}{\sqrt{3}z^{2}}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{1}{\sqrt{3}\left(x + y + 1\right)^{2}}\sqrt{1+\left(1\right)^{2}+\left(1\right)^{2}}\,\text{d}A\\ & =\int_{0}^{\frac{1}{2}}\int_{- x}^{0}\left(\frac{1}{\left(x + y + 1\right)^{2}}\right)\,\text{d}y\,\text{d}x\\ & =\int_{0}^{\frac{1}{2}}[- \frac{1}{x + y + 1}]_{y=- x}^{y=0}\,\text{d}x\\ & =\int_{0}^{\frac{1}{2}}\left((- \frac{1}{x + 1})-\left((-1)\right)\right)\,\text{d}x\\ & =[(- \ln{\left(x + 1 \right)})+(x)]_{x=0}^{x=\frac{1}{2}}\\ & =\left((- \ln{\left(\frac{3}{2} \right)})+(\frac{1}{2})-\left((0)+(0)\right)\right)\\ & =\ln{\left(2 \right)}-\ln{\left(3 \right)}+\frac{1}{2}.\end{aligned}
$$

### Generated reciprocal_triangle variant 1 — authored bank

Evaluate the surface integral

$$
\iint_S \frac{2}{\sqrt{3}z^{2}}\,\mathrm{d}S
$$

where $S$ is defined by $z=x + y + 3$ for $0\le x\le 1$ and $- x\le y\le 0$.

- $- \frac{1}{2} + \ln{\left(\frac{16}{9} \right)}$
- $- \frac{2}{3} - \ln{\left(\frac{9}{16} \right)}$
- $\ln{\left(\frac{36}{49} \right)} + \frac{1}{3}$
- $\ln{\left(\frac{81}{256} \right)} + \frac{4}{3}$
- $\ln{\left(\frac{9}{16} \right)} + \frac{2}{3}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(x + y + 3)=1,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(x + y + 3)=1.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{2}{\sqrt{3}z^{2}}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{2}{\sqrt{3}\left(x + y + 3\right)^{2}}\sqrt{1+\left(1\right)^{2}+\left(1\right)^{2}}\,\text{d}A\\ & =\int_{0}^{1}\int_{- x}^{0}\left(\frac{2}{\left(x + y + 3\right)^{2}}\right)\,\text{d}y\,\text{d}x\\ & =\int_{0}^{1}[- \frac{2}{x + y + 3}]_{y=- x}^{y=0}\,\text{d}x\\ & =\int_{0}^{1}\left((- \frac{2}{x + 3})-\left((- \frac{2}{3})\right)\right)\,\text{d}x\\ & =[(- 2 \ln{\left(x + 3 \right)})+(\frac{2 x}{3})]_{x=0}^{x=1}\\ & =\left((- 2 \ln{\left(4 \right)})+(\frac{2}{3})-\left((- 2 \ln{\left(3 \right)})+(0)\right)\right)\\ & =2 \ln{\left(3 \right)}-4 \ln{\left(2 \right)}+\frac{2}{3}.\end{aligned}
$$

### Generated reciprocal_triangle variant 2 — authored bank

Evaluate the surface integral

$$
\iint_S \frac{2}{\sqrt{3}z^{2}}\,\mathrm{d}S
$$

where $S$ is defined by $z=x + y + 2$ for $0\le x\le 1$ and $- x\le y\le 0$.

- $\ln{\left(\frac{16}{25} \right)} + \frac{1}{2}$
- $\ln{\left(\frac{4}{9} \right)} + 1$
- $2 \ln{\left(\frac{4}{9} \right)} + 2$
- $- \frac{2}{3} + \ln{\left(\frac{9}{4} \right)}$
- $-1 - \ln{\left(\frac{4}{9} \right)}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(x + y + 2)=1,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(x + y + 2)=1.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{2}{\sqrt{3}z^{2}}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{2}{\sqrt{3}\left(x + y + 2\right)^{2}}\sqrt{1+\left(1\right)^{2}+\left(1\right)^{2}}\,\text{d}A\\ & =\int_{0}^{1}\int_{- x}^{0}\left(\frac{2}{\left(x + y + 2\right)^{2}}\right)\,\text{d}y\,\text{d}x\\ & =\int_{0}^{1}[- \frac{2}{x + y + 2}]_{y=- x}^{y=0}\,\text{d}x\\ & =\int_{0}^{1}\left((- \frac{2}{x + 2})-\left((-1)\right)\right)\,\text{d}x\\ & =[(- 2 \ln{\left(x + 2 \right)})+(x)]_{x=0}^{x=1}\\ & =\left((- 2 \ln{\left(3 \right)})+(1)-\left((- 2 \ln{\left(2 \right)})+(0)\right)\right)\\ & =2 \ln{\left(2 \right)}-2 \ln{\left(3 \right)}+1.\end{aligned}
$$

## Original q-161342 — raw evidence, ineligible

Evaluate the surface integral 

$$
{∬}_{S}2z\operatorname{sin}⁡y\,\text{d}S
$$

where $S$ is defined by $z=x$ for $0\le x\le 1$ and $0\le y\le \frac{\pi }{2}.$

- $\sqrt{2}$
- $1$
- $-1$
- $2$
- $2\sqrt{2}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(x)=1,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(x)=0.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}2z\operatorname{sin}⁡y\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}\,2x\operatorname{sin}⁡y\sqrt{1+{1}^{2}+(0)^{2}}\,\text{d}A \\  & =\sqrt{2}{∬}_{D}\,2x\operatorname{sin}⁡y\,\text{d}A \\  & =\sqrt{2}{\int }_{0}^{1}{\int }_{0}^{\pi /2}2x\operatorname{sin}⁡y\,\text{d}y\,\text{d}x \\  & =\sqrt{2}{\int }_{0}^{1}[-2x\operatorname{cos}⁡y]_{y=0}^{y=\pi /2}\,\text{d}x \\  & =\sqrt{2}{\int }_{0}^{1}-2x(0-1)\,\text{d}x \\  & =\sqrt{2}{\int }_{0}^{1}2x\,\text{d}x \\  & =\sqrt{2}{[{x}^{2}]}_{0}^{1} \\  & =\sqrt{2}\end{aligned}
$$

### Generated raw q-161342 scale 2 — evidence only, opaque bank

Evaluate the surface integral 

$$
{∬}_{S}2\left(2z\operatorname{sin}⁡y\right)\,\text{d}S
$$

where $S$ is defined by $z=x$ for $0\le x\le 1$ and $0\le y\le \frac{\pi }{2}.$

- $2\left(-1\right)$
- $2\left(2\right)$
- $2\left(\sqrt{2}\right)$
- $2\left(1\right)$
- $2\left(2\sqrt{2}\right)$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(x)=1,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(x)=0.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}2\left(2z\operatorname{sin}⁡y\right)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & =2\left({∬}_{D}\,2x\operatorname{sin}⁡y\sqrt{1+{1}^{2}+(0)^{2}}\,\text{d}A\right)\\  & =2\left(\sqrt{2}{∬}_{D}\,2x\operatorname{sin}⁡y\,\text{d}A\right)\\  & =2\left(\sqrt{2}{\int }_{0}^{1}{\int }_{0}^{\pi /2}2x\operatorname{sin}⁡y\,\text{d}y\,\text{d}x\right)\\  & =2\left(\sqrt{2}{\int }_{0}^{1}[-2x\operatorname{cos}⁡y]_{y=0}^{y=\pi /2}\,\text{d}x\right)\\  & =2\left(\sqrt{2}{\int }_{0}^{1}-2x(0-1)\,\text{d}x\right)\\  & =2\left(\sqrt{2}{\int }_{0}^{1}2x\,\text{d}x\right)\\  & =2\left(\sqrt{2}{[{x}^{2}]}_{0}^{1}\right)\\  & =2\left(\sqrt{2}\right)\end{aligned}
$$

### Normal plane_sine at original parameters — authored bank, source-family chain

Evaluate the surface integral

$$
\iint_S 2 z \sin{\left(y \right)}\,\mathrm{d}S
$$

where $S$ is defined by $z=x$ for $0\le x\le 1$ and $0\le y\le \frac{\pi}{2}$.

- $- \sqrt{2}$
- $\sqrt{2}$
- $0$
- $2$
- $1$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(x)=1,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(x)=0.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}2 z \sin{\left(y \right)}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}2 x \sin{\left(y \right)}\sqrt{1+\left(1\right)^{2}+\left(0\right)^{2}}\,\text{d}A\\ & =\sqrt{2}{∬}_{D}2 x \sin{\left(y \right)}\,\text{d}A\\ & =\sqrt{2}\int_{0}^{1}\int_{0}^{\frac{\pi}{2}}\left(2 x \sin{\left(y \right)}\right)\,\text{d}y\,\text{d}x\\ & =\sqrt{2}\int_{0}^{1}[- 2 x \cos{\left(y \right)}]_{y=0}^{y=\frac{\pi}{2}}\,\text{d}x\\ & =\sqrt{2}\int_{0}^{1}\left(- 2 x\right)\left(0-\left(1\right)\right)\,\text{d}x\\ & =\sqrt{2}\int_{0}^{1}2 x\,\text{d}x\\ & =\sqrt{2}[(x^{2})]_{x=0}^{x=1}\\ & =\sqrt{2}\left((1)-\left((0)\right)\right)\\ & =\sqrt{2}.\end{aligned}
$$

### Generated plane_sine variant 1 — authored bank

Evaluate the surface integral

$$
\iint_S 2 z \sin{\left(y \right)}\,\mathrm{d}S
$$

where $S$ is defined by $z=2 x$ for $0\le x\le 2$ and $0\le y\le \frac{3 \pi}{2}$.

- $8$
- $- 8 \sqrt{5}$
- $40$
- $8 \sqrt{5}$
- $0$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x)=0.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}2 z \sin{\left(y \right)}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}4 x \sin{\left(y \right)}\sqrt{1+\left(2\right)^{2}+\left(0\right)^{2}}\,\text{d}A\\ & =\sqrt{5}{∬}_{D}4 x \sin{\left(y \right)}\,\text{d}A\\ & =\sqrt{5}\int_{0}^{2}\int_{0}^{\frac{3 \pi}{2}}\left(4 x \sin{\left(y \right)}\right)\,\text{d}y\,\text{d}x\\ & =\sqrt{5}\int_{0}^{2}[- 4 x \cos{\left(y \right)}]_{y=0}^{y=\frac{3 \pi}{2}}\,\text{d}x\\ & =\sqrt{5}\int_{0}^{2}\left(- 4 x\right)\left(0-\left(1\right)\right)\,\text{d}x\\ & =\sqrt{5}\int_{0}^{2}4 x\,\text{d}x\\ & =\sqrt{5}[(2 x^{2})]_{x=0}^{x=2}\\ & =\sqrt{5}\left((8)-\left((0)\right)\right)\\ & =8 \sqrt{5}.\end{aligned}
$$

### Generated plane_sine variant 2 — authored bank

Evaluate the surface integral

$$
\iint_S 2 z \sin{\left(y \right)}\,\mathrm{d}S
$$

where $S$ is defined by $z=2 x$ for $0\le x\le 1$ and $0\le y\le \frac{3 \pi}{2}$.

- $2 \sqrt{5}$
- $10$
- $0$
- $2$
- $- 2 \sqrt{5}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x)=0.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}2 z \sin{\left(y \right)}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}4 x \sin{\left(y \right)}\sqrt{1+\left(2\right)^{2}+\left(0\right)^{2}}\,\text{d}A\\ & =\sqrt{5}{∬}_{D}4 x \sin{\left(y \right)}\,\text{d}A\\ & =\sqrt{5}\int_{0}^{1}\int_{0}^{\frac{3 \pi}{2}}\left(4 x \sin{\left(y \right)}\right)\,\text{d}y\,\text{d}x\\ & =\sqrt{5}\int_{0}^{1}[- 4 x \cos{\left(y \right)}]_{y=0}^{y=\frac{3 \pi}{2}}\,\text{d}x\\ & =\sqrt{5}\int_{0}^{1}\left(- 4 x\right)\left(0-\left(1\right)\right)\,\text{d}x\\ & =\sqrt{5}\int_{0}^{1}4 x\,\text{d}x\\ & =\sqrt{5}[(2 x^{2})]_{x=0}^{x=1}\\ & =\sqrt{5}\left((2)-\left((0)\right)\right)\\ & =2 \sqrt{5}.\end{aligned}
$$

## Original q-161351 — raw evidence, ineligible

Evaluate the surface integral 

$$
{∬}_{S}(24xy+{z}^{2})\,\text{d}S
$$

where $S$ is defined by $z=3x-4y$ for $1\le x\le 2$ and $0\le y\le 1.$

- $\frac{121}{3}\sqrt{26}$
- $\frac{5}{3}$
- $\frac{25}{3}\sqrt{26}$
- $\frac{79}{3}\sqrt{26}$
- $\frac{395}{3}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(3x-4y)=3,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(3x-4y)=-4.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}(24xy+{z}^{2})\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}\,(24xy+(3x-4y)^{2})\sqrt{1+{3}^{2}+(-4)^{2}}\,\text{d}A \\  & =\sqrt{26}{∬}_{D}\,(24xy+9{x}^{2}+16{y}^{2}-24xy)\,\text{d}A \\  & =\sqrt{26}{∬}_{D}\,(9{x}^{2}+16{y}^{2})\,\text{d}A \\  & =\sqrt{26}{\int }_{1}^{2}{\int }_{0}^{1}(9{x}^{2}+16{y}^{2})\,\text{d}y\,\text{d}x \\  & =\sqrt{26}{\int }_{1}^{2}{[9{x}^{2}y+\frac{16}{3}{y}^{3}]}_{y=0}^{y=1}\,\text{d}x \\  & =\sqrt{26}{\int }_{1}^{2}(9{x}^{2}+\frac{16}{3})\,\text{d}x \\  & =\sqrt{26}{[3{x}^{3}+\frac{16}{3}x]}_{1}^{2} \\  & =\sqrt{26}(24+\frac{32}{3}-3-\frac{16}{3}) \\  & =\frac{79}{3}\sqrt{26}\end{aligned}
$$

### Generated raw q-161351 scale 2 — evidence only, opaque bank

Evaluate the surface integral 

$$
{∬}_{S}2\left((24xy+{z}^{2})\right)\,\text{d}S
$$

where $S$ is defined by $z=3x-4y$ for $1\le x\le 2$ and $0\le y\le 1.$

- $2\left(\frac{25}{3}\sqrt{26}\right)$
- $2\left(\frac{79}{3}\sqrt{26}\right)$
- $2\left(\frac{121}{3}\sqrt{26}\right)$
- $2\left(\frac{5}{3}\right)$
- $2\left(\frac{395}{3}\right)$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(3x-4y)=3,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(3x-4y)=-4.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}2\left((24xy+{z}^{2})\right)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & =2\left({∬}_{D}\,(24xy+(3x-4y)^{2})\sqrt{1+{3}^{2}+(-4)^{2}}\,\text{d}A\right)\\  & =2\left(\sqrt{26}{∬}_{D}\,(24xy+9{x}^{2}+16{y}^{2}-24xy)\,\text{d}A\right)\\  & =2\left(\sqrt{26}{∬}_{D}\,(9{x}^{2}+16{y}^{2})\,\text{d}A\right)\\  & =2\left(\sqrt{26}{\int }_{1}^{2}{\int }_{0}^{1}(9{x}^{2}+16{y}^{2})\,\text{d}y\,\text{d}x\right)\\  & =2\left(\sqrt{26}{\int }_{1}^{2}{[9{x}^{2}y+\frac{16}{3}{y}^{3}]}_{y=0}^{y=1}\,\text{d}x\right)\\  & =2\left(\sqrt{26}{\int }_{1}^{2}(9{x}^{2}+\frac{16}{3})\,\text{d}x\right)\\  & =2\left(\sqrt{26}{[3{x}^{3}+\frac{16}{3}x]}_{1}^{2}\right)\\  & =2\left(\sqrt{26}(24+\frac{32}{3}-3-\frac{16}{3})\right)\\  & =2\left(\frac{79}{3}\sqrt{26}\right)\end{aligned}
$$

### Normal cross_cancel at original parameters — authored bank, source-family chain

Evaluate the surface integral

$$
\iint_S \left(24 x y + z^{2}\right)\,\mathrm{d}S
$$

where $S$ is defined by $z=3 x - 4 y$ for $1\le x\le 2$ and $0\le y\le 1$.

- $- \frac{79 \sqrt{26}}{3}$
- $\frac{79 \sqrt{26}}{3}$
- $18 \sqrt{26}$
- $\frac{2054}{3}$
- $\frac{79}{3}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(3 x - 4 y)=3,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(3 x - 4 y)=-4.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\left(24 x y + z^{2}\right)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\left(24 x y + \left(3 x - 4 y\right)^{2}\right)\sqrt{1+\left(3\right)^{2}+\left(-4\right)^{2}}\,\text{d}A\\ & =\sqrt{26}{∬}_{D}\left((24 x y)+(9 x^{2})+(16 y^{2})+(- 24 x y)\right)\,\text{d}A\\ & =\sqrt{26}{∬}_{D}\left(9 x^{2} + 16 y^{2}\right)\,\text{d}A\\ & =\sqrt{26}\int_{1}^{2}\int_{0}^{1}\left(9 x^{2} + 16 y^{2}\right)\,\text{d}y\,\text{d}x\\ & =\sqrt{26}\int_{1}^{2}[(9 x^{2} y)+(\frac{16 y^{3}}{3})]_{y=0}^{y=1}\,\text{d}x\\ & =\sqrt{26}\int_{1}^{2}\left((9 x^{2})+(\frac{16}{3})-\left((0)+(0)\right)\right)\,\text{d}x\\ & =\sqrt{26}\int_{1}^{2}\left(9 x^{2} + \frac{16}{3}\right)\,\text{d}x\\ & =\sqrt{26}[(\frac{16 x}{3})+(3 x^{3})]_{x=1}^{x=2}\\ & =\sqrt{26}\left((\frac{32}{3})+(24)-\left((\frac{16}{3})+(3)\right)\right)\\ & =\frac{79 \sqrt{26}}{3}.\end{aligned}
$$

### Generated cross_cancel variant 1 — authored bank

Evaluate the surface integral

$$
\iint_S \left(16 x y + 2 z^{2}\right)\,\mathrm{d}S
$$

where $S$ is defined by $z=2 x - 2 y$ for $0\le x\le 2$ and $0\le y\le 2$.

- $\frac{256}{3}$
- $192$
- $768$
- $256$
- $-256$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x - 2 y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x - 2 y)=-2.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\left(16 x y + 2 z^{2}\right)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\left(16 x y + 2 \left(2 x - 2 y\right)^{2}\right)\sqrt{1+\left(2\right)^{2}+\left(-2\right)^{2}}\,\text{d}A\\ & =3{∬}_{D}\left(2\right)\left((8 x y)+(4 x^{2})+(4 y^{2})+(- 8 x y)\right)\,\text{d}A\\ & =3{∬}_{D}\left(8 x^{2} + 8 y^{2}\right)\,\text{d}A\\ & =3\int_{0}^{2}\int_{0}^{2}\left(8 x^{2} + 8 y^{2}\right)\,\text{d}y\,\text{d}x\\ & =3\int_{0}^{2}[(8 x^{2} y)+(\frac{8 y^{3}}{3})]_{y=0}^{y=2}\,\text{d}x\\ & =3\int_{0}^{2}\left((16 x^{2})+(\frac{64}{3})-\left((0)+(0)\right)\right)\,\text{d}x\\ & =3\int_{0}^{2}\left(16 x^{2} + \frac{64}{3}\right)\,\text{d}x\\ & =3[(\frac{64 x}{3})+(\frac{16 x^{3}}{3})]_{x=0}^{x=2}\\ & =3\left((\frac{128}{3})+(\frac{128}{3})-\left((0)+(0)\right)\right)\\ & =256.\end{aligned}
$$

### Generated cross_cancel variant 2 — authored bank

Evaluate the surface integral

$$
\iint_S \left(16 x y + 2 z^{2}\right)\,\mathrm{d}S
$$

where $S$ is defined by $z=2 x - 2 y$ for $0\le x\le 1$ and $0\le y\le 1$.

- $\frac{16}{3}$
- $16$
- $12$
- $-16$
- $48$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x - 2 y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x - 2 y)=-2.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\left(16 x y + 2 z^{2}\right)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\left(16 x y + 2 \left(2 x - 2 y\right)^{2}\right)\sqrt{1+\left(2\right)^{2}+\left(-2\right)^{2}}\,\text{d}A\\ & =3{∬}_{D}\left(2\right)\left((8 x y)+(4 x^{2})+(4 y^{2})+(- 8 x y)\right)\,\text{d}A\\ & =3{∬}_{D}\left(8 x^{2} + 8 y^{2}\right)\,\text{d}A\\ & =3\int_{0}^{1}\int_{0}^{1}\left(8 x^{2} + 8 y^{2}\right)\,\text{d}y\,\text{d}x\\ & =3\int_{0}^{1}[(8 x^{2} y)+(\frac{8 y^{3}}{3})]_{y=0}^{y=1}\,\text{d}x\\ & =3\int_{0}^{1}\left((8 x^{2})+(\frac{8}{3})-\left((0)+(0)\right)\right)\,\text{d}x\\ & =3\int_{0}^{1}\left(8 x^{2} + \frac{8}{3}\right)\,\text{d}x\\ & =3[(\frac{8 x}{3})+(\frac{8 x^{3}}{3})]_{x=0}^{x=1}\\ & =3\left((\frac{8}{3})+(\frac{8}{3})-\left((0)+(0)\right)\right)\\ & =16.\end{aligned}
$$

## Authored easy constant_plane variant 1

Evaluate the surface integral

$$
\iint_S 3\,\mathrm{d}S
$$

where $S$ is defined by $z=2 x + 2 y$ for $0\le x\le 2$ and $0\le y\le 2$.

- $12$
- $12 \sqrt{5}$
- $18$
- $108$
- $36$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x + 2 y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x + 2 y)=2.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}3\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}3\sqrt{1+\left(2\right)^{2}+\left(2\right)^{2}}\,\text{d}A\\ & ={∬}_{D}9\,\text{d}A\\ & =9{∬}_{D}\,\text{d}A\\ & =9\cdot\text{Area}(D)\\ & =9\cdot\left(2-\left(0\right)\right)\cdot\left(2-\left(0\right)\right)\\ & =9\cdot\left(2\right)\cdot\left(2\right)\\ & =36.\end{aligned}
$$

## Authored easy constant_plane variant 2

Evaluate the surface integral

$$
\iint_S 2\,\mathrm{d}S
$$

where $S$ is defined by $z=x + y$ for $0\le x\le 2$ and $0\le y\le 2$.

- $8 \sqrt{3}$
- $8$
- $24$
- $8 \sqrt{2}$
- $4 \sqrt{3}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(x + y)=1,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(x + y)=1.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}2\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}2\sqrt{1+\left(1\right)^{2}+\left(1\right)^{2}}\,\text{d}A\\ & ={∬}_{D}2 \sqrt{3}\,\text{d}A\\ & =2 \sqrt{3}{∬}_{D}\,\text{d}A\\ & =2 \sqrt{3}\cdot\text{Area}(D)\\ & =2 \sqrt{3}\cdot\left(2-\left(0\right)\right)\cdot\left(2-\left(0\right)\right)\\ & =2 \sqrt{3}\cdot\left(2\right)\cdot\left(2\right)\\ & =8 \sqrt{3}.\end{aligned}
$$

## Authored easy canonical_cancel variant 1

Evaluate the surface integral

$$
\iint_S \frac{3}{\sqrt{z-x+y^{2}}}\,\mathrm{d}S
$$

where $S$ is defined by $z=x + y^{2} + 1$ for $0\le x\le 2$ and $-2\le y\le 2$.

- $24$
- $- 24 \sqrt{2}$
- $6 \sqrt{2}$
- $48$
- $24 \sqrt{2}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(x + y^{2} + 1)=1,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(x + y^{2} + 1)=2 y.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{3}{\sqrt{z-x+y^{2}}}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{3}{\sqrt{\left(x + y^{2} + 1\right)-x+y^{2}}}\sqrt{1+\left(1\right)^{2}+\left(2 y\right)^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{3}{\sqrt{2 y^{2} + 1}}\sqrt{4 y^{2} + 2}\,\text{d}A\\ & ={∬}_{D}\frac{3}{\sqrt{2 y^{2} + 1}}\sqrt{2\left(2 y^{2} + 1\right)}\,\text{d}A\\ & ={∬}_{D}\frac{3}{\sqrt{2 y^{2} + 1}}\sqrt{2}\sqrt{2 y^{2} + 1}\,\text{d}A\\ & ={∬}_{D}\frac{3}{\cancel{\sqrt{2 y^{2} + 1}}}\sqrt{2}\cancel{\sqrt{2 y^{2} + 1}}\,\text{d}A\\ & ={∬}_{D}3 \sqrt{2}\,\text{d}A\\ & =3 \sqrt{2}{∬}_{D}\,\text{d}A\\ & =3 \sqrt{2}\cdot\text{Area}(D)\\ & =3 \sqrt{2}\cdot\left(2-\left(0\right)\right)\cdot\left(2-\left(-2\right)\right)\\ & =3 \sqrt{2}\cdot\left(2\right)\cdot\left(4\right)\\ & =24 \sqrt{2}.\end{aligned}
$$

## Authored easy canonical_cancel variant 2

Evaluate the surface integral

$$
\iint_S \frac{2}{\sqrt{z-x+y^{2}}}\,\mathrm{d}S
$$

where $S$ is defined by $z=x + y^{2} + 1$ for $0\le x\le 2$ and $-2\le y\le 2$.

- $16 \sqrt{2}$
- $16$
- $32$
- $- 16 \sqrt{2}$
- $4 \sqrt{2}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(x + y^{2} + 1)=1,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(x + y^{2} + 1)=2 y.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\frac{2}{\sqrt{z-x+y^{2}}}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{2}{\sqrt{\left(x + y^{2} + 1\right)-x+y^{2}}}\sqrt{1+\left(1\right)^{2}+\left(2 y\right)^{2}}\,\text{d}A\\ & ={∬}_{D}\frac{2}{\sqrt{2 y^{2} + 1}}\sqrt{4 y^{2} + 2}\,\text{d}A\\ & ={∬}_{D}\frac{2}{\sqrt{2 y^{2} + 1}}\sqrt{2\left(2 y^{2} + 1\right)}\,\text{d}A\\ & ={∬}_{D}\frac{2}{\sqrt{2 y^{2} + 1}}\sqrt{2}\sqrt{2 y^{2} + 1}\,\text{d}A\\ & ={∬}_{D}\frac{2}{\cancel{\sqrt{2 y^{2} + 1}}}\sqrt{2}\cancel{\sqrt{2 y^{2} + 1}}\,\text{d}A\\ & ={∬}_{D}2 \sqrt{2}\,\text{d}A\\ & =2 \sqrt{2}{∬}_{D}\,\text{d}A\\ & =2 \sqrt{2}\cdot\text{Area}(D)\\ & =2 \sqrt{2}\cdot\left(2-\left(0\right)\right)\cdot\left(2-\left(-2\right)\right)\\ & =2 \sqrt{2}\cdot\left(2\right)\cdot\left(4\right)\\ & =16 \sqrt{2}.\end{aligned}
$$

## Authored hard quadratic_rectangle_full variant 1

Evaluate the surface integral

$$
\iint_S \left(2 x^{2} + 2 x y + 2 z^{2}\right)\,\mathrm{d}S
$$

where $S$ is defined by $z=2 x - 2 y$ for $0\le x\le 2$ and $0\le y\le 2$.

- $40$
- $-120$
- $120$
- $360$
- $56$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x - 2 y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x - 2 y)=-2.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\left(2 x^{2} + 2 x y + 2 z^{2}\right)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\left(2 x^{2} + 2 x y + 2 \left(2 x - 2 y\right)^{2}\right)\sqrt{1+\left(2\right)^{2}+\left(-2\right)^{2}}\,\text{d}A\\ & =3{∬}_{D}\left(2\right)\left((x^{2})+(x y)+(4 x^{2})+(4 y^{2})+(- 8 x y)\right)\,\text{d}A\\ & =3{∬}_{D}\left(10 x^{2} - 14 x y + 8 y^{2}\right)\,\text{d}A\\ & =3\int_{0}^{2}\int_{0}^{2}\left(10 x^{2} - 14 x y + 8 y^{2}\right)\,\text{d}y\,\text{d}x\\ & =3\int_{0}^{2}[(\frac{8 y^{3}}{3})+(10 x^{2} y)+(- 7 x y^{2})]_{y=0}^{y=2}\,\text{d}x\\ & =3\int_{0}^{2}\left((\frac{64}{3})+(20 x^{2})+(- 28 x)-\left((0)+(0)+(0)\right)\right)\,\text{d}x\\ & =3\int_{0}^{2}\left(20 x^{2} - 28 x + \frac{64}{3}\right)\,\text{d}x\\ & =3[(\frac{64 x}{3})+(- 14 x^{2})+(\frac{20 x^{3}}{3})]_{x=0}^{x=2}\\ & =3\left((\frac{128}{3})+(-56)+(\frac{160}{3})-\left((0)+(0)+(0)\right)\right)\\ & =120.\end{aligned}
$$

## Authored hard quadratic_rectangle_full variant 2

Evaluate the surface integral

$$
\iint_S \left(x^{2} + x y + z^{2}\right)\,\mathrm{d}S
$$

where $S$ is defined by $z=4 x - y$ for $0\le x\le 2$ and $0\le y\le 2$.

- $204 \sqrt{2}$
- $68$
- $28 \sqrt{2}$
- $1224$
- $- 204 \sqrt{2}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(4 x - y)=4,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(4 x - y)=-1.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\left(x^{2} + x y + z^{2}\right)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\left(x^{2} + x y + \left(4 x - y\right)^{2}\right)\sqrt{1+\left(4\right)^{2}+\left(-1\right)^{2}}\,\text{d}A\\ & =3 \sqrt{2}{∬}_{D}\left((x^{2})+(x y)+(16 x^{2})+(y^{2})+(- 8 x y)\right)\,\text{d}A\\ & =3 \sqrt{2}{∬}_{D}\left(17 x^{2} - 7 x y + y^{2}\right)\,\text{d}A\\ & =3 \sqrt{2}\int_{0}^{2}\int_{0}^{2}\left(17 x^{2} - 7 x y + y^{2}\right)\,\text{d}y\,\text{d}x\\ & =3 \sqrt{2}\int_{0}^{2}[(\frac{y^{3}}{3})+(17 x^{2} y)+(- \frac{7 x y^{2}}{2})]_{y=0}^{y=2}\,\text{d}x\\ & =3 \sqrt{2}\int_{0}^{2}\left((\frac{8}{3})+(34 x^{2})+(- 14 x)-\left((0)+(0)+(0)\right)\right)\,\text{d}x\\ & =3 \sqrt{2}\int_{0}^{2}\left(34 x^{2} - 14 x + \frac{8}{3}\right)\,\text{d}x\\ & =3 \sqrt{2}[(\frac{8 x}{3})+(- 7 x^{2})+(\frac{34 x^{3}}{3})]_{x=0}^{x=2}\\ & =3 \sqrt{2}\left((\frac{16}{3})+(-28)+(\frac{272}{3})-\left((0)+(0)+(0)\right)\right)\\ & =204 \sqrt{2}.\end{aligned}
$$

## Authored hard quadratic_triangle_full variant 1

Evaluate the surface integral

$$
\iint_S \left(2 x^{2} + 2 x y + 2 z^{2}\right)\,\mathrm{d}S
$$

where $S$ is defined by $z=2 x - 2 y$ for $0\le x\le 2$ and $0\le y\le 2 x$.

- $\frac{160}{3}$
- $-160$
- $160$
- $480$
- $96$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2 x - 2 y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2 x - 2 y)=-2.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\left(2 x^{2} + 2 x y + 2 z^{2}\right)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\left(2 x^{2} + 2 x y + 2 \left(2 x - 2 y\right)^{2}\right)\sqrt{1+\left(2\right)^{2}+\left(-2\right)^{2}}\,\text{d}A\\ & ={∬}_{D}\left(2\right)\left((x^{2})+(x y)+(4 x^{2})+(4 y^{2})+(- 8 x y)\right)\sqrt{9}\,\text{d}A\\ & =3{∬}_{D}\left(10 x^{2} - 14 x y + 8 y^{2}\right)\,\text{d}A\\ & =3\int_{0}^{2}\int_{0}^{2 x}\left(10 x^{2} - 14 x y + 8 y^{2}\right)\,\text{d}y\,\text{d}x\\ & =3\int_{0}^{2}[(\frac{8 y^{3}}{3})+(10 x^{2} y)+(- 7 x y^{2})]_{y=0}^{y=2 x}\,\text{d}x\\ & =3\int_{0}^{2}\left((\frac{64 x^{3}}{3})+(20 x^{3})+(- 28 x^{3})-\left((0)+(0)+(0)\right)\right)\,\text{d}x\\ & =3\int_{0}^{2}\left(\frac{40 x^{3}}{3}\right)\,\text{d}x\\ & =1\int_{0}^{2}40 x^{3}\,\text{d}x\\ & =1[(10 x^{4})]_{x=0}^{x=2}\\ & =1\left((160)-\left((0)\right)\right)\\ & =160.\end{aligned}
$$

## Authored hard quadratic_triangle_full variant 2

Evaluate the surface integral

$$
\iint_S \left(x^{2} + x y + z^{2}\right)\,\mathrm{d}S
$$

where $S$ is defined by $z=4 x - y$ for $0\le x\le 2$ and $0\le y\le 2 x$.

- $272 \sqrt{2}$
- $\frac{272}{3}$
- $48 \sqrt{2}$
- $1632$
- $- 272 \sqrt{2}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(4 x - y)=4,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(4 x - y)=-1.
$$

Therefore, the surface integral can be evaluated as follows:

$$
\begin{aligned}{∬}_{S}\left(x^{2} + x y + z^{2}\right)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A\\ & ={∬}_{D}\left(x^{2} + x y + \left(4 x - y\right)^{2}\right)\sqrt{1+\left(4\right)^{2}+\left(-1\right)^{2}}\,\text{d}A\\ & ={∬}_{D}\left((x^{2})+(x y)+(16 x^{2})+(y^{2})+(- 8 x y)\right)\sqrt{18}\,\text{d}A\\ & =3 \sqrt{2}{∬}_{D}\left(17 x^{2} - 7 x y + y^{2}\right)\,\text{d}A\\ & =3 \sqrt{2}\int_{0}^{2}\int_{0}^{2 x}\left(17 x^{2} - 7 x y + y^{2}\right)\,\text{d}y\,\text{d}x\\ & =3 \sqrt{2}\int_{0}^{2}[(\frac{y^{3}}{3})+(17 x^{2} y)+(- \frac{7 x y^{2}}{2})]_{y=0}^{y=2 x}\,\text{d}x\\ & =3 \sqrt{2}\int_{0}^{2}\left((\frac{8 x^{3}}{3})+(34 x^{3})+(- 14 x^{3})-\left((0)+(0)+(0)\right)\right)\,\text{d}x\\ & =3 \sqrt{2}\int_{0}^{2}\left(\frac{68 x^{3}}{3}\right)\,\text{d}x\\ & =\sqrt{2}\int_{0}^{2}68 x^{3}\,\text{d}x\\ & =\sqrt{2}[(17 x^{4})]_{x=0}^{x=2}\\ & =\sqrt{2}\left((272)-\left((0)\right)\right)\\ & =272 \sqrt{2}.\end{aligned}
$$
