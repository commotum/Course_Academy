### original evidence q-161146

![](/media/jake/SSD/EDB/math/images/36/365c6e6ebc861b9d8276773d5afe39b971096f0de6f07fced2c5a2ea9e035554.png)

Evaluate the surface integral 

$$
{∬}_{S}3x\,\text{d}S,
$$

where $S$ is defined by $z=x-y$ and whose domain is the quarter-circle of radius $2$ centered at $O$ in the first quadrant, as shown above.

- $8\sqrt{3}$
- $12\sqrt{2}$
- $2$
- $2\sqrt{3}$
- $12$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(x-y)=1,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(x-y)=-1.
$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}{∬}_{S}3x\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}3x\cdot \sqrt{1+{1}^{2}+(-1)^{2}}\,\text{d}A \\  & ={∬}_{D}3x\cdot \sqrt{3}\,\text{d}A \\  & =\sqrt{3}{∬}_{D}\,3x\,\text{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta ),$ our domain can be expressed as 

$$
Δ={(r,\theta )\,:\,0\le r\le 2,\,0\le \theta \le \frac{\pi }{2}}.
$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\operatorname{cos}⁡\theta $ and $y=r\operatorname{sin}⁡\theta ,$ we obtain 

$$
\begin{aligned}\sqrt{3}{∬}_{D}\,3x\,\text{d}A & =\sqrt{3}{∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta  \\  & =\sqrt{3}{∬}_{Δ}3r\operatorname{cos}⁡\theta \cdot r\cdot \text{d}r\text{d}\theta  \\  & =\sqrt{3}{∬}_{Δ}3{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\text{d}\theta  \\  & =\sqrt{3}{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta {\int }_{0}^{2}3{r}^{2}\,\text{d}r\,\text{d}\theta  \\  & =\sqrt{3}{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta [{r}^{3}]_{0}^{2}\,\text{d}\theta  \\  & =\sqrt{3}{\int }_{0}^{\pi /2}8\operatorname{cos}⁡\theta \,\text{d}\theta  \\  & =8\sqrt{3}[\operatorname{sin}⁡\theta ]_{0}^{\pi /2} \\  & =8\sqrt{3}(1-0) \\  & =8\sqrt{3}.\end{aligned}
$$

---

### generated authored bank / source family q-161146

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/fe30baf13bc7979a774d42a42fa75cde3fd8284cc2c63f95d06e27c66ddbd933.png)

Evaluate the surface integral

$$\iint_S 4 x\,\mathrm{d}S,$$

where $S$ is defined by $z=- 4 x - 4 y$ and whose domain is the right half-circle of radius $2$ centered at $O$, as shown above. Give an exact answer.

- $\frac{64 \sqrt{33}}{3}$
- $\frac{8 \sqrt{33}}{3}$
- $704$
- $\frac{32 \sqrt{33}}{3}$
- $\frac{64}{3}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(- 4 x - 4 y)=-4,$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(- 4 x - 4 y)=-4.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{4 x}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(4 x)\cdot\sqrt{1+(-4)^2+(-4)^2}}\,\mathrm{d}A \\ & =\iint_D{(4 x)\cdot\sqrt{33}}\,\mathrm{d}A \\ & =(\sqrt{33})\iint_D{4 x}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 2,\ - \frac{\pi}{2}\le\theta\le \frac{\pi}{2}\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(\sqrt{33})\iint_D{4 x}\,\mathrm{d}A & =(\sqrt{33})\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{33})\iint_\Delta{(4(r\cos\theta))\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{33})\iint_\Delta{4 r^{2} \cos{\left(\theta \right)}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{33})\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}{(\cos{\left(\theta \right)})\int_{0}^{2}{4 r^{2}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(\sqrt{33})\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}{(\cos{\left(\theta \right)})\left[\frac{4 r^{3}}{3}\right]_{0}^{2}}\,\mathrm{d}\theta \\ & =(\sqrt{33})\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}{(\cos{\left(\theta \right)})\left[((\frac{32}{3}))-((0))\right]}\,\mathrm{d}\theta \\ & =(\sqrt{33})\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}{\frac{32 \cos{\left(\theta \right)}}{3}}\,\mathrm{d}\theta \\ & =(\frac{32 \sqrt{33}}{3})\left[\sin{\left(\theta \right)}\right]_{- \frac{\pi}{2}}^{\frac{\pi}{2}} \\ & =(\frac{32 \sqrt{33}}{3})\left[((1))-((-1))\right] \\ & =(\frac{32 \sqrt{33}}{3})\cdot((1)-(-1)) \\ & =\frac{64 \sqrt{33}}{3}.\end{aligned}
$$

Therefore, the surface integral is $\frac{64 \sqrt{33}}{3}$.

---

### generated authored bank / source family q-161146

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/ce2f2c97892c2377764df14ac7e0b420b32a680c4f3ccfdac5af264932ab0c56.png)

Evaluate the surface integral

$$\iint_S 8 x\,\mathrm{d}S,$$

where $S$ is defined by $z=2 x + 2 y$ and whose domain is the quarter-circle in the first quadrant of radius $1$ centered at $O$, as shown above. Give an exact answer.

- $1$
- $8$
- $\frac{8}{3}$
- $24$
- $4 \sqrt{2}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(2 x + 2 y)=2,$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(2 x + 2 y)=2.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{8 x}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(8 x)\cdot\sqrt{1+(2)^2+(2)^2}}\,\mathrm{d}A \\ & =\iint_D{(8 x)\cdot\sqrt{9}}\,\mathrm{d}A \\ & =(3)\iint_D{8 x}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 1,\ 0\le\theta\le \frac{\pi}{2}\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(3)\iint_D{8 x}\,\mathrm{d}A & =(3)\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{(8(r\cos\theta))\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{8 r^{2} \cos{\left(\theta \right)}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{(\cos{\left(\theta \right)})\int_{0}^{1}{8 r^{2}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{(\cos{\left(\theta \right)})\left[\frac{8 r^{3}}{3}\right]_{0}^{1}}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{(\cos{\left(\theta \right)})\left[((\frac{8}{3}))-((0))\right]}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{\frac{8 \cos{\left(\theta \right)}}{3}}\,\mathrm{d}\theta \\ & =(8)\left[\sin{\left(\theta \right)}\right]_{0}^{\frac{\pi}{2}} \\ & =(8)\left[((1))-((0))\right] \\ & =(8)\cdot((1)-(0)) \\ & =8.\end{aligned}
$$

Therefore, the surface integral is $8$.

---

### original evidence q-161302

![](/media/jake/SSD/EDB/math/images/78/7836860694ae6246dee36a70b86bc7fcd8cf7358d47a10586ea6880759fb1588.png)

Evaluate the surface integral 

$$
{∬}_{S}({x}^{2}+{y}^{2})\,\text{d}S,
$$

where $S$ is defined by $z=2x-y$ and whose domain is the circle of radius $2$ centered at $O,$ as shown above.

- $8\sqrt{6}\pi $
- $3\sqrt{2}\pi $
- $\sqrt{6}$
- $\pi $
- $\sqrt{3}\pi $

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2x-y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2x-y)=-1.
$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}{∬}_{S}({x}^{2}+{y}^{2})\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}({x}^{2}+{y}^{2})\cdot \sqrt{1+{2}^{2}+(-1)^{2}}\,\text{d}A \\  & ={∬}_{D}({x}^{2}+{y}^{2})\cdot \sqrt{6}\,\text{d}A \\  & =\sqrt{6}{∬}_{D}\,({x}^{2}+{y}^{2})\,\text{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta ),$ our domain can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 2,\,0\le \theta \le 2\pi \}.
$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\operatorname{cos}⁡\theta $ and $y=r\operatorname{sin}⁡\theta ,$ we obtain 

$$
\begin{aligned}\sqrt{6}{∬}_{D}\,({x}^{2}+{y}^{2})\,\text{d}A & =\sqrt{6}{∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta  \\  & =\sqrt{6}{∬}_{Δ}({r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta )\cdot r\text{d}r\text{d}\theta  \\  & =\sqrt{6}{\int }_{0}^{2\pi }{\int }_{0}^{2}{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & =\sqrt{6}{\int }_{0}^{2\pi }{[\frac{{r}^{4}}{4}]}_{0}^{2}\,\text{d}\theta  \\  & =\sqrt{6}{\int }_{0}^{2\pi }4\,\text{d}\theta  \\  & =4\sqrt{6}{\int }_{0}^{2\pi }\,\text{d}\theta  \\  & =4\sqrt{6}[\theta ]_{0}^{2\pi } \\  & =8\sqrt{6}\pi .\end{aligned}
$$

---

### generated authored bank / source family q-161302

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/52d23bb30ea29a9679a80533cd3fef5e0c10ae6bf26ac43ad7f1f79ed0d6f209.png)

Evaluate the surface integral

$$\iint_S 3(x^2+y^2)\,\mathrm{d}S,$$

where $S$ is defined by $z=\sqrt{2} x + \sqrt{2} y$ and whose domain is the disk of radius $3$ centered at $O$, as shown above. Give an exact answer.

- $\frac{243 \sqrt{5} \pi}{2}$
- $\frac{243 \sqrt{5} \pi}{32}$
- $\frac{1215 \pi}{2}$
- $\frac{243 \sqrt{5} \pi}{4}$
- $\frac{243 \pi}{2}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2},$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2}.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{3(x^2+y^2)}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(3(x^2+y^2))\cdot\sqrt{1+(\sqrt{2})^2+(\sqrt{2})^2}}\,\mathrm{d}A \\ & =\iint_D{(3(x^2+y^2))\cdot\sqrt{5}}\,\mathrm{d}A \\ & =(\sqrt{5})\iint_D{3(x^2+y^2)}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 3,\ 0\le\theta\le 2 \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(\sqrt{5})\iint_D{3(x^2+y^2)}\,\mathrm{d}A & =(\sqrt{5})\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{(3(r^2\cos^2\theta+r^2\sin^2\theta))\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{3 r^{3}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{0}^{2 \pi}{\int_{0}^{3}{3 r^{3}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{0}^{2 \pi}{\left[\frac{3 r^{4}}{4}\right]_{0}^{3}}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{0}^{2 \pi}{\left[((\frac{243}{4}))-((0))\right]}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{0}^{2 \pi}{\frac{243}{4}}\,\mathrm{d}\theta \\ & =(\frac{243 \sqrt{5}}{4})\left[\theta\right]_{0}^{2 \pi} \\ & =(\frac{243 \sqrt{5}}{4})\left[((2 \pi))-((0))\right] \\ & =(\frac{243 \sqrt{5}}{4})\cdot((2 \pi)-(0)) \\ & =\frac{243 \sqrt{5} \pi}{2}.\end{aligned}
$$

Therefore, the surface integral is $\frac{243 \sqrt{5} \pi}{2}$.

---

### generated authored bank / source family q-161302

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/c65e6ecdea7e108d29ef494a88a55112e0e4cfa54bec96b124c7109f42112915.png)

Evaluate the surface integral

$$\iint_S 8(x^2+y^2)\,\mathrm{d}S,$$

where $S$ is defined by $z=2 x + 2 y$ and whose domain is the disk of radius $1$ centered at $O$, as shown above. Give an exact answer.

- $\frac{3 \pi}{4}$
- $12 \pi$
- $4 \pi$
- $36 \pi$
- $6 \pi$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(2 x + 2 y)=2,$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(2 x + 2 y)=2.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{8(x^2+y^2)}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(8(x^2+y^2))\cdot\sqrt{1+(2)^2+(2)^2}}\,\mathrm{d}A \\ & =\iint_D{(8(x^2+y^2))\cdot\sqrt{9}}\,\mathrm{d}A \\ & =(3)\iint_D{8(x^2+y^2)}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 1,\ 0\le\theta\le 2 \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(3)\iint_D{8(x^2+y^2)}\,\mathrm{d}A & =(3)\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{(8(r^2\cos^2\theta+r^2\sin^2\theta))\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{8 r^{3}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\int_{0}^{2 \pi}{\int_{0}^{1}{8 r^{3}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{2 \pi}{\left[2 r^{4}\right]_{0}^{1}}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{2 \pi}{\left[((2))-((0))\right]}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{2 \pi}{2}\,\mathrm{d}\theta \\ & =(6)\left[\theta\right]_{0}^{2 \pi} \\ & =(6)\left[((2 \pi))-((0))\right] \\ & =(6)\cdot((2 \pi)-(0)) \\ & =12 \pi.\end{aligned}
$$

Therefore, the surface integral is $12 \pi$.

---

### original evidence q-161291

![](/media/jake/SSD/EDB/math/images/97/9795c04bf6d4bfa407a7b9176cd5c4b97b3d89bfcc6fff17d1d78190047b3a54.png)

Evaluate the surface integral 

$$
{∬}_{S}6y\,\text{d}S,
$$

where $S$ is defined by $z=x+y$ and whose domain is the upper half-circle of radius $1$ centered at $O,$ as shown above.

- $\sqrt{3}$
- $4\sqrt{3}$
- $3\sqrt{3}$
- $5\sqrt{3}$
- $2\sqrt{3}$

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

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}{∬}_{S}6y\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}6y\cdot \sqrt{1+{1}^{2}+(1)^{2}}\,\text{d}A \\  & ={∬}_{D}6y\cdot \sqrt{3}\,\text{d}A \\  & =\sqrt{3}{∬}_{D}\,6y\,\text{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta ),$ our domain can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 1,\,0\le \theta \le \pi \}.
$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\operatorname{cos}⁡\theta $ and $y=r\operatorname{sin}⁡\theta ,$ we obtain 

$$
\begin{aligned}\sqrt{3}{∬}_{D}\,6y\,\text{d}A & =\sqrt{3}{∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta  \\  & =\sqrt{3}{∬}_{Δ}6r\operatorname{sin}⁡\theta \cdot r\cdot \text{d}r\text{d}\theta  \\  & =6\sqrt{3}{\int }_{0}^{\pi }\operatorname{sin}⁡\theta {\int }_{0}^{1}{r}^{2}\,\text{d}r\,\text{d}\theta  \\  & =6\sqrt{3}{\int }_{0}^{\pi }\operatorname{sin}⁡\theta {[\frac{{r}^{3}}{3}]}_{0}^{1}\,\text{d}\theta  \\  & =6\sqrt{3}{\int }_{0}^{\pi }\frac{1}{3}\operatorname{sin}⁡\theta \,\text{d}\theta  \\  & =2\sqrt{3}{\int }_{0}^{\pi }\operatorname{sin}⁡\theta \,\text{d}\theta  \\  & =2\sqrt{3}[-\operatorname{cos}⁡\theta ]_{0}^{\pi } \\  & =2\sqrt{3}(1+1) \\  & =4\sqrt{3}.\end{aligned}
$$

---

### generated authored bank / source family q-161291

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/04bd17254d9833ff34f9eb980a85c9e6835a101a9da606a17713e234b3f9f230.png)

Evaluate the surface integral

$$\iint_S 4 y\,\mathrm{d}S,$$

where $S$ is defined by $z=- 4 x - 4 y$ and whose domain is the upper half-circle of radius $2$ centered at $O$, as shown above. Give an exact answer.

- $\frac{64 \sqrt{33}}{3}$
- $\frac{8 \sqrt{33}}{3}$
- $704$
- $\frac{32 \sqrt{33}}{3}$
- $\frac{64}{3}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(- 4 x - 4 y)=-4,$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(- 4 x - 4 y)=-4.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{4 y}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(4 y)\cdot\sqrt{1+(-4)^2+(-4)^2}}\,\mathrm{d}A \\ & =\iint_D{(4 y)\cdot\sqrt{33}}\,\mathrm{d}A \\ & =(\sqrt{33})\iint_D{4 y}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 2,\ 0\le\theta\le \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(\sqrt{33})\iint_D{4 y}\,\mathrm{d}A & =(\sqrt{33})\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{33})\iint_\Delta{(4(r\sin\theta))\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{33})\iint_\Delta{4 r^{2} \sin{\left(\theta \right)}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{33})\int_{0}^{\pi}{(\sin{\left(\theta \right)})\int_{0}^{2}{4 r^{2}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(\sqrt{33})\int_{0}^{\pi}{(\sin{\left(\theta \right)})\left[\frac{4 r^{3}}{3}\right]_{0}^{2}}\,\mathrm{d}\theta \\ & =(\sqrt{33})\int_{0}^{\pi}{(\sin{\left(\theta \right)})\left[((\frac{32}{3}))-((0))\right]}\,\mathrm{d}\theta \\ & =(\sqrt{33})\int_{0}^{\pi}{\frac{32 \sin{\left(\theta \right)}}{3}}\,\mathrm{d}\theta \\ & =(\frac{32 \sqrt{33}}{3})\left[- \cos{\left(\theta \right)}\right]_{0}^{\pi} \\ & =(\frac{32 \sqrt{33}}{3})\left[((1))-((-1))\right] \\ & =(\frac{32 \sqrt{33}}{3})\cdot((1)-(-1)) \\ & =\frac{64 \sqrt{33}}{3}.\end{aligned}
$$

Therefore, the surface integral is $\frac{64 \sqrt{33}}{3}$.

---

### generated authored bank / source family q-161291

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/ce2f2c97892c2377764df14ac7e0b420b32a680c4f3ccfdac5af264932ab0c56.png)

Evaluate the surface integral

$$\iint_S 8 y\,\mathrm{d}S,$$

where $S$ is defined by $z=2 x + 2 y$ and whose domain is the quarter-circle in the first quadrant of radius $1$ centered at $O$, as shown above. Give an exact answer.

- $1$
- $8$
- $\frac{8}{3}$
- $24$
- $8 - 4 \sqrt{2}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(2 x + 2 y)=2,$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(2 x + 2 y)=2.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{8 y}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(8 y)\cdot\sqrt{1+(2)^2+(2)^2}}\,\mathrm{d}A \\ & =\iint_D{(8 y)\cdot\sqrt{9}}\,\mathrm{d}A \\ & =(3)\iint_D{8 y}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 1,\ 0\le\theta\le \frac{\pi}{2}\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(3)\iint_D{8 y}\,\mathrm{d}A & =(3)\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{(8(r\sin\theta))\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{8 r^{2} \sin{\left(\theta \right)}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{(\sin{\left(\theta \right)})\int_{0}^{1}{8 r^{2}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{(\sin{\left(\theta \right)})\left[\frac{8 r^{3}}{3}\right]_{0}^{1}}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{(\sin{\left(\theta \right)})\left[((\frac{8}{3}))-((0))\right]}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{\frac{8 \sin{\left(\theta \right)}}{3}}\,\mathrm{d}\theta \\ & =(8)\left[- \cos{\left(\theta \right)}\right]_{0}^{\frac{\pi}{2}} \\ & =(8)\left[((0))-((-1))\right] \\ & =(8)\cdot((0)-(-1)) \\ & =8.\end{aligned}
$$

Therefore, the surface integral is $8$.

---

### original evidence q-161300

![](/media/jake/SSD/EDB/math/images/01/0148ca16ee12a0f651c91091715b4ec07d95639530defb8ed366bacb33e4e87d.png)

Evaluate the surface integral 

$$
{∬}_{S}8xy\,\text{d}S,
$$

where $S$ is defined by $z=y-2x$ and whose domain is the quarter-circle of radius $2$ centered at $O$ in the first quadrant, as shown above.

- $16\sqrt{6}$
- $8$
- $\sqrt{8}$
- $2\sqrt{3}$
- $\sqrt{6}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(y-2x)=-2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(y-2x)=1.
$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}{∬}_{S}8xy\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}8xy\cdot \sqrt{1+(-2)^{2}+{1}^{2}}\,\text{d}A \\  & ={∬}_{D}8xy\cdot \sqrt{6}\,\text{d}A \\  & =\sqrt{6}{∬}_{D}\,8xy\,\text{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta ),$ our domain can be expressed as 

$$
Δ={(r,\theta )\,:\,0\le r\le 2,\,0\le \theta \le \frac{\pi }{2}}.
$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\operatorname{cos}⁡\theta $ and $y=r\operatorname{sin}⁡\theta ,$ we obtain 

$$
\begin{aligned}\sqrt{6}{∬}_{D}\,8xy\,\text{d}A & =\sqrt{6}{∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta  \\  & =\sqrt{6}{∬}_{Δ}8r\operatorname{cos}⁡\theta \cdot r\operatorname{sin}⁡\theta \cdot r\,\text{d}r\text{d}\theta  \\  & =\sqrt{6}{∬}_{Δ}4{r}^{3}\operatorname{sin}⁡2\theta \,\text{d}r\text{d}\theta  \\  & =\sqrt{6}{\int }_{0}^{\pi /2}\operatorname{sin}⁡2\theta {\int }_{0}^{2}4{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & =\sqrt{6}{\int }_{0}^{\pi /2}\operatorname{sin}⁡2\theta [{r}^{4}]_{0}^{2}\,\text{d}\theta  \\  & =\sqrt{6}{\int }_{0}^{\pi /2}16\operatorname{sin}⁡2\theta \,\text{d}\theta  \\  & =8\sqrt{6}[-\operatorname{cos}⁡2\theta ]_{0}^{\pi /2} \\  & =8\sqrt{6}(1+1) \\  & =16\sqrt{6}.\end{aligned}
$$

---

### generated authored bank / source family q-161300

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/6385f17950d6e41f410131df0889429bb9ae37cbb1dc832c3a1b04883d3081a1.png)

Evaluate the surface integral

$$\iint_S 3 x y\,\mathrm{d}S,$$

where $S$ is defined by $z=\sqrt{2} x + \sqrt{2} y$ and whose domain is the quarter-circle in the second quadrant of radius $3$ centered at $O$, as shown above. Give an exact answer.

- $- \frac{243 \sqrt{5}}{8}$
- $- \frac{243 \sqrt{5}}{128}$
- $- \frac{1215}{8}$
- $- \frac{243 \sqrt{5}}{16}$
- $- \frac{243}{8}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2},$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2}.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{3 x y}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(3 x y)\cdot\sqrt{1+(\sqrt{2})^2+(\sqrt{2})^2}}\,\mathrm{d}A \\ & =\iint_D{(3 x y)\cdot\sqrt{5}}\,\mathrm{d}A \\ & =(\sqrt{5})\iint_D{3 x y}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 3,\ \frac{\pi}{2}\le\theta\le \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(\sqrt{5})\iint_D{3 x y}\,\mathrm{d}A & =(\sqrt{5})\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{(3(r\cos\theta)(r\sin\theta))\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{\frac{3 r^{3} \sin{\left(2 \theta \right)}}{2}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{\pi}{2}}^{\pi}{(\sin{\left(2 \theta \right)})\int_{0}^{3}{\frac{3 r^{3}}{2}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{\pi}{2}}^{\pi}{(\sin{\left(2 \theta \right)})\left[\frac{3 r^{4}}{8}\right]_{0}^{3}}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{\pi}{2}}^{\pi}{(\sin{\left(2 \theta \right)})\left[((\frac{243}{8}))-((0))\right]}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{\pi}{2}}^{\pi}{\frac{243 \sin{\left(2 \theta \right)}}{8}}\,\mathrm{d}\theta \\ & =(\frac{243 \sqrt{5}}{16})\left[- \cos{\left(2 \theta \right)}\right]_{\frac{\pi}{2}}^{\pi} \\ & =(\frac{243 \sqrt{5}}{16})\left[((-1))-((1))\right] \\ & =(\frac{243 \sqrt{5}}{16})\cdot((-1)-(1)) \\ & =- \frac{243 \sqrt{5}}{8}.\end{aligned}
$$

Therefore, the surface integral is $- \frac{243 \sqrt{5}}{8}$.

---

### generated authored bank / source family q-161300

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/ce2f2c97892c2377764df14ac7e0b420b32a680c4f3ccfdac5af264932ab0c56.png)

Evaluate the surface integral

$$\iint_S 8 x y\,\mathrm{d}S,$$

where $S$ is defined by $z=2 x + 2 y$ and whose domain is the quarter-circle in the first quadrant of radius $1$ centered at $O$, as shown above. Give an exact answer.

- $\frac{3}{16}$
- $3$
- $1$
- $9$
- $\frac{3}{2}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(2 x + 2 y)=2,$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(2 x + 2 y)=2.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{8 x y}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(8 x y)\cdot\sqrt{1+(2)^2+(2)^2}}\,\mathrm{d}A \\ & =\iint_D{(8 x y)\cdot\sqrt{9}}\,\mathrm{d}A \\ & =(3)\iint_D{8 x y}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 1,\ 0\le\theta\le \frac{\pi}{2}\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(3)\iint_D{8 x y}\,\mathrm{d}A & =(3)\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{(8(r\cos\theta)(r\sin\theta))\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{4 r^{3} \sin{\left(2 \theta \right)}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{(\sin{\left(2 \theta \right)})\int_{0}^{1}{4 r^{3}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{(\sin{\left(2 \theta \right)})\left[r^{4}\right]_{0}^{1}}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{(\sin{\left(2 \theta \right)})\left[((1))-((0))\right]}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{\sin{\left(2 \theta \right)}}\,\mathrm{d}\theta \\ & =(\frac{3}{2})\left[- \cos{\left(2 \theta \right)}\right]_{0}^{\frac{\pi}{2}} \\ & =(\frac{3}{2})\left[((1))-((-1))\right] \\ & =(\frac{3}{2})\cdot((1)-(-1)) \\ & =3.\end{aligned}
$$

Therefore, the surface integral is $3$.

---

### original evidence q-161301

![](/media/jake/SSD/EDB/math/images/52/5276afad13c3e52854d33a3ff3404ab401781e08d1888214121cf2d56c0bb304.png)

Evaluate the surface integral 

$$
{∬}_{S}5x{y}^{2}\,\text{d}S,
$$

where $S$ is defined by $z=2x+2y$ and whose domain is the right half-circle of radius $2$ centered at $O$, as shown above.

- $72$
- $56$
- $48$
- $64$
- $60$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(2x+2y)=2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(2x+2y)=2.
$$

 

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}{∬}_{S}5x{y}^{2}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}5x{y}^{2}\cdot \sqrt{1+{2}^{2}+{2}^{2}}\,\text{d}A \\  & ={∬}_{D}5x{y}^{2}\cdot \sqrt{9}\,\text{d}A \\  & =3{∬}_{D}\,5x{y}^{2}\,\text{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta ),$ our domain can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 2,\,-\frac{\pi }{2}\le \theta \le \frac{\pi }{2}\}.
$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\operatorname{cos}⁡\theta $ and $y=r\operatorname{sin}⁡\theta ,$ we obtain 

$$
\begin{aligned}3{∬}_{D}\,5x{y}^{2}\,\text{d}A & =3{∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta  \\  & =3{∬}_{Δ}5r\operatorname{cos}⁡\theta \cdot {r}^{2}{sin}^{2}⁡\theta \cdot r\,\text{d}r\text{d}\theta  \\  & =3{∬}_{Δ}5{r}^{4}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}r\text{d}\theta  \\  & =3{\int }_{-\pi /2}^{\pi /2}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta {\int }_{0}^{2}5{r}^{4}\,\text{d}r\,\text{d}\theta  \\  & =3{\int }_{-\pi /2}^{\pi /2}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta [{r}^{5}]_{0}^{2}\,\text{d}\theta  \\  & =96{\int }_{-\pi /2}^{\pi /2}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}\theta  \\  & =96{[\frac{{sin}^{3}⁡\theta }{3}]}_{-\pi /2}^{\pi /2} \\  & =32(1+1) \\  & =64.\end{aligned}
$$

---

### generated authored bank / source family q-161301

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/6385f17950d6e41f410131df0889429bb9ae37cbb1dc832c3a1b04883d3081a1.png)

Evaluate the surface integral

$$\iint_S 3 x y^{2}\,\mathrm{d}S,$$

where $S$ is defined by $z=\sqrt{2} x + \sqrt{2} y$ and whose domain is the quarter-circle in the second quadrant of radius $3$ centered at $O$, as shown above. Give an exact answer.

- $- \frac{243 \sqrt{5}}{5}$
- $- \frac{243 \sqrt{5}}{160}$
- $-243$
- $\frac{243 \sqrt{5} \left(-4 + \sqrt{2}\right)}{20}$
- $- \frac{243}{5}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2},$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2}.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{3 x y^{2}}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(3 x y^{2})\cdot\sqrt{1+(\sqrt{2})^2+(\sqrt{2})^2}}\,\mathrm{d}A \\ & =\iint_D{(3 x y^{2})\cdot\sqrt{5}}\,\mathrm{d}A \\ & =(\sqrt{5})\iint_D{3 x y^{2}}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 3,\ \frac{\pi}{2}\le\theta\le \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(\sqrt{5})\iint_D{3 x y^{2}}\,\mathrm{d}A & =(\sqrt{5})\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{(3(r\cos\theta)(r\sin\theta)^2)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{3 r^{4}\cos\theta\sin^2\theta}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{\pi}{2}}^{\pi}{(\cos\theta\sin^2\theta)\int_{0}^{3}{3 r^{4}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{\pi}{2}}^{\pi}{(\cos\theta\sin^2\theta)\left[\frac{3 r^{5}}{5}\right]_{0}^{3}}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{\pi}{2}}^{\pi}{(\cos\theta\sin^2\theta)\left[((\frac{729}{5}))-((0))\right]}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{\pi}{2}}^{\pi}{\frac{729 \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)}}{5}}\,\mathrm{d}\theta \\ & =(\frac{729 \sqrt{5}}{5})\left[\frac{\sin^{3}{\left(\theta \right)}}{3}\right]_{\frac{\pi}{2}}^{\pi} \\ & =(\frac{729 \sqrt{5}}{5})\left[((0))-((\frac{1}{3}))\right] \\ & =(\frac{243 \sqrt{5}}{5})\cdot((0)-(1)) \\ & =- \frac{243 \sqrt{5}}{5}.\end{aligned}
$$

Therefore, the surface integral is $- \frac{243 \sqrt{5}}{5}$.

---

### generated authored bank / source family q-161301

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/ce2f2c97892c2377764df14ac7e0b420b32a680c4f3ccfdac5af264932ab0c56.png)

Evaluate the surface integral

$$\iint_S 8 x y^{2}\,\mathrm{d}S,$$

where $S$ is defined by $z=2 x + 2 y$ and whose domain is the quarter-circle in the first quadrant of radius $1$ centered at $O$, as shown above. Give an exact answer.

- $\frac{1}{20}$
- $\frac{8}{5}$
- $\frac{8}{15}$
- $\frac{24}{5}$
- $\frac{2 \sqrt{2}}{5}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(2 x + 2 y)=2,$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(2 x + 2 y)=2.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{8 x y^{2}}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(8 x y^{2})\cdot\sqrt{1+(2)^2+(2)^2}}\,\mathrm{d}A \\ & =\iint_D{(8 x y^{2})\cdot\sqrt{9}}\,\mathrm{d}A \\ & =(3)\iint_D{8 x y^{2}}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 1,\ 0\le\theta\le \frac{\pi}{2}\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(3)\iint_D{8 x y^{2}}\,\mathrm{d}A & =(3)\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{(8(r\cos\theta)(r\sin\theta)^2)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{8 r^{4}\cos\theta\sin^2\theta}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{(\cos\theta\sin^2\theta)\int_{0}^{1}{8 r^{4}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{(\cos\theta\sin^2\theta)\left[\frac{8 r^{5}}{5}\right]_{0}^{1}}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{(\cos\theta\sin^2\theta)\left[((\frac{8}{5}))-((0))\right]}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{\frac{8 \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)}}{5}}\,\mathrm{d}\theta \\ & =(\frac{24}{5})\left[\frac{\sin^{3}{\left(\theta \right)}}{3}\right]_{0}^{\frac{\pi}{2}} \\ & =(\frac{24}{5})\left[((\frac{1}{3}))-((0))\right] \\ & =(\frac{8}{5})\cdot((1)-(0)) \\ & =\frac{8}{5}.\end{aligned}
$$

Therefore, the surface integral is $\frac{8}{5}$.

---

### original evidence q-161311

![](/media/jake/SSD/EDB/math/images/5b/5ba2dbc746b9fe8b36202d31bbeb8193ffb9e747d6ed4c2e2f0f994499f88e8e.png)

Evaluate the surface integral 

$$
{∬}_{S}\frac{x}{{x}^{2}+{y}^{2}}\,\text{d}S,
$$

where $S$ is defined by $z=-x+\sqrt{2}y$ and whose domain is the quarter-circle of radius $3$ centered at $O$ in the second quadrant, as shown above.

- $3$
- $\frac{1}{3}$
- $-6$
- $\frac{1}{6}$
- $2$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(-x+\sqrt{2}y)=-1,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(-x+\sqrt{2}y)=\sqrt{2}.
$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}{∬}_{S}\frac{x}{{x}^{2}+{y}^{2}}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}\frac{x}{{x}^{2}+{y}^{2}}\cdot \sqrt{1+(-1)^{2}+(\sqrt{2})^{2}}\,\text{d}A \\  & ={∬}_{D}\frac{x}{{x}^{2}+{y}^{2}}\cdot \sqrt{4}\,\text{d}A \\  & =2{∬}_{D}\,\frac{x}{{x}^{2}+{y}^{2}}\,\text{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta ),$ our domain can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 3,\,\frac{\pi }{2}\le \theta \le \pi \}.
$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\operatorname{cos}⁡\theta $ and $y=r\operatorname{sin}⁡\theta ,$ we obtain 

$$
\begin{aligned}2{∬}_{D}\,\frac{x}{{x}^{2}+{y}^{2}}\,\text{d}A & =2{∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta  \\  & =2{∬}_{Δ}\frac{r\operatorname{cos}⁡\theta }{{r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta }\cdot r\text{ }\text{d}r\text{d}\theta  \\  & =2{∬}_{Δ}\frac{{r}^{2}\operatorname{cos}⁡\theta }{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,\text{d}r\text{d}\theta  \\  & =2{∬}_{Δ}\operatorname{cos}⁡\theta \,\text{d}r\text{d}\theta  \\  & =2{\int }_{0}^{3}{\int }_{\pi /2}^{\pi }\operatorname{cos}⁡\theta \,\text{d}\theta \,\text{d}r \\  & =2{\int }_{0}^{3}{[\,\operatorname{sin}⁡\theta \,\,]}_{\pi /2}^{\pi }\,\text{d}r \\  & =2{\int }_{0}^{3}(-1)\,\text{d}r \\  & =2\cdot (-1)\cdot 3 \\  & =-6.\end{aligned}
$$

---

### generated authored bank / source family q-161311

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/6385f17950d6e41f410131df0889429bb9ae37cbb1dc832c3a1b04883d3081a1.png)

Evaluate the surface integral

$$\iint_S \frac{3 x}{x^{2} + y^{2}}\,\mathrm{d}S,$$

where $S$ is defined by $z=\sqrt{2} x + \sqrt{2} y$ and whose domain is the quarter-circle in the second quadrant of radius $3$ centered at $O$, as shown above. Give an exact answer. The value at $O$ may be assigned arbitrarily; it does not affect the integral.

- $- 9 \sqrt{5}$
- $- \frac{9 \sqrt{5}}{2}$
- $-45$
- $\frac{9 \sqrt{5} \left(-2 + \sqrt{2}\right)}{2}$
- $-9$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2},$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2}.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{\frac{3 x}{x^{2} + y^{2}}}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(\frac{3 x}{x^{2} + y^{2}})\cdot\sqrt{1+(\sqrt{2})^2+(\sqrt{2})^2}}\,\mathrm{d}A \\ & =\iint_D{(\frac{3 x}{x^{2} + y^{2}})\cdot\sqrt{5}}\,\mathrm{d}A \\ & =(\sqrt{5})\iint_D{\frac{3 x}{x^{2} + y^{2}}}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 3,\ \frac{\pi}{2}\le\theta\le \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(\sqrt{5})\iint_D{\frac{3 x}{x^{2} + y^{2}}}\,\mathrm{d}A & =(\sqrt{5})\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{(\frac{3(r\cos\theta)}{r^2\cos^2\theta+r^2\sin^2\theta})\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{\frac{3r^2\cos\theta}{r^2(\cos^2\theta+\sin^2\theta)}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{3 \cos{\left(\theta \right)}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3 \sqrt{5})\int_{0}^{3}{\int_{\frac{\pi}{2}}^{\pi}{\cos{\left(\theta \right)}}\,\mathrm{d}\theta}\,\mathrm{d}r \\ & =(3 \sqrt{5})\int_{0}^{3}{\left[\sin{\left(\theta \right)}\right]_{\frac{\pi}{2}}^{\pi}}\,\mathrm{d}r \\ & =(3 \sqrt{5})\int_{0}^{3}{\left[((0))-((1))\right]}\,\mathrm{d}r \\ & =(3 \sqrt{5})\int_{0}^{3}{-1}\,\mathrm{d}r \\ & =(- \sqrt{5})\left[3 r\right]_{0}^{3} \\ & =(- \sqrt{5})\left[((9))-((0))\right] \\ & =(\sqrt{5})\cdot(-1)\cdot(9) \\ & =- 9 \sqrt{5}.\end{aligned}
$$

Therefore, the surface integral is $- 9 \sqrt{5}$.

---

### generated authored bank / source family q-161311

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/ce2f2c97892c2377764df14ac7e0b420b32a680c4f3ccfdac5af264932ab0c56.png)

Evaluate the surface integral

$$\iint_S \frac{8 x}{x^{2} + y^{2}}\,\mathrm{d}S,$$

where $S$ is defined by $z=2 x + 2 y$ and whose domain is the quarter-circle in the first quadrant of radius $1$ centered at $O$, as shown above. Give an exact answer. The value at $O$ may be assigned arbitrarily; it does not affect the integral.

- $12$
- $24$
- $8$
- $72$
- $12 \sqrt{2}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(2 x + 2 y)=2,$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(2 x + 2 y)=2.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{\frac{8 x}{x^{2} + y^{2}}}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(\frac{8 x}{x^{2} + y^{2}})\cdot\sqrt{1+(2)^2+(2)^2}}\,\mathrm{d}A \\ & =\iint_D{(\frac{8 x}{x^{2} + y^{2}})\cdot\sqrt{9}}\,\mathrm{d}A \\ & =(3)\iint_D{\frac{8 x}{x^{2} + y^{2}}}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 1,\ 0\le\theta\le \frac{\pi}{2}\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(3)\iint_D{\frac{8 x}{x^{2} + y^{2}}}\,\mathrm{d}A & =(3)\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{(\frac{8(r\cos\theta)}{r^2\cos^2\theta+r^2\sin^2\theta})\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{\frac{8r^2\cos\theta}{r^2(\cos^2\theta+\sin^2\theta)}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{8 \cos{\left(\theta \right)}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(24)\int_{0}^{1}{\int_{0}^{\frac{\pi}{2}}{\cos{\left(\theta \right)}}\,\mathrm{d}\theta}\,\mathrm{d}r \\ & =(24)\int_{0}^{1}{\left[\sin{\left(\theta \right)}\right]_{0}^{\frac{\pi}{2}}}\,\mathrm{d}r \\ & =(24)\int_{0}^{1}{\left[((1))-((0))\right]}\,\mathrm{d}r \\ & =(24)\int_{0}^{1}{1}\,\mathrm{d}r \\ & =(3)\left[8 r\right]_{0}^{1} \\ & =(3)\left[((8))-((0))\right] \\ & =(3)\cdot(1)\cdot(8) \\ & =24.\end{aligned}
$$

Therefore, the surface integral is $24$.

---

### original evidence q-161318

![](/media/jake/SSD/EDB/math/images/5d/5d6cedcc2d8c5a232d8d7ed89f050fa7a545ed0da6075ddb44eec67e065b9e87.png)

Evaluate the surface integral 

$$
{∬}_{S}3{x}^{2}y\,\text{d}S,
$$

where $S$ is defined by $z=-4x+\sqrt{8}y$ and whose domain is the upper half-circle of radius $1$ centered at $O$, as shown above.

- $4$
- $2$
- $2\sqrt{2}$
- $1$
- $6$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(-4x+\sqrt{8}y)=-4,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(-4x+\sqrt{8}y)=\sqrt{8}.
$$

 

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}{∬}_{S}3{x}^{2}y\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}3{x}^{2}y\cdot \sqrt{1+(-4)^{2}+(\sqrt{8})^{2}}\,\text{d}A \\  & ={∬}_{D}3{x}^{2}y\cdot \sqrt{25}\,\text{d}A \\  & =5{∬}_{D}\,3{x}^{2}y\,\text{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta ),$ our domain can be expressed as 

$$
Δ={(r,\theta )\,:\,0\le r\le 1,\,0\le \theta \le \pi }.
$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\operatorname{cos}⁡\theta $ and $y=r\operatorname{sin}⁡\theta ,$ we obtain 

$$
\begin{aligned}5{∬}_{D}\,3{x}^{2}y\,\text{d}A & =5{∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta  \\  & =5{∬}_{Δ}3{r}^{2}{cos}^{2}⁡\theta \cdot r\operatorname{sin}⁡\theta \cdot r\,\text{d}r\text{d}\theta  \\  & =15{∬}_{Δ}{r}^{4}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\text{d}\theta  \\  & =15{\int }_{0}^{\pi }{cos}^{2}⁡\theta \operatorname{sin}⁡\theta {\int }_{0}^{1}{r}^{4}\,\text{d}r\,\text{d}\theta  \\  & =15{\int }_{0}^{\pi }{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,{[\frac{{r}^{5}}{5}]}_{0}^{1}\,\text{d}\theta  \\  & =3{\int }_{0}^{\pi }{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}\theta  \\  & ={[-{cos}^{3}⁡\theta ]}_{0}^{\pi } \\  & =2.\end{aligned}
$$

---

### generated authored bank / source family q-161318

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/f56c20db7c0f46c759b74ad8ddc847f9408228eb311ac5bb9ad54efd9c4fb8f2.png)

Evaluate the surface integral

$$\iint_S 3 x^{2} y\,\mathrm{d}S,$$

where $S$ is defined by $z=\sqrt{2} x + \sqrt{2} y$ and whose domain is the quarter-circle in the fourth quadrant of radius $3$ centered at $O$, as shown above. Give an exact answer.

- $- \frac{243 \sqrt{5}}{5}$
- $- \frac{243 \sqrt{5}}{160}$
- $-243$
- $- \frac{243 \sqrt{10}}{20}$
- $- \frac{243}{5}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2},$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2}.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{3 x^{2} y}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(3 x^{2} y)\cdot\sqrt{1+(\sqrt{2})^2+(\sqrt{2})^2}}\,\mathrm{d}A \\ & =\iint_D{(3 x^{2} y)\cdot\sqrt{5}}\,\mathrm{d}A \\ & =(\sqrt{5})\iint_D{3 x^{2} y}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 3,\ \frac{3 \pi}{2}\le\theta\le 2 \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(\sqrt{5})\iint_D{3 x^{2} y}\,\mathrm{d}A & =(\sqrt{5})\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{(3(r\cos\theta)^2(r\sin\theta))\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{3 r^{4}\cos^2\theta\sin\theta}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{3 \pi}{2}}^{2 \pi}{(\cos^2\theta\sin\theta)\int_{0}^{3}{3 r^{4}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{3 \pi}{2}}^{2 \pi}{(\cos^2\theta\sin\theta)\left[\frac{3 r^{5}}{5}\right]_{0}^{3}}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{3 \pi}{2}}^{2 \pi}{(\cos^2\theta\sin\theta)\left[((\frac{729}{5}))-((0))\right]}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{3 \pi}{2}}^{2 \pi}{\frac{729 \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)}}{5}}\,\mathrm{d}\theta \\ & =(\frac{243 \sqrt{5}}{5})\left[- \cos^{3}{\left(\theta \right)}\right]_{\frac{3 \pi}{2}}^{2 \pi} \\ & =(\frac{243 \sqrt{5}}{5})\left[((-1))-((0))\right] \\ & =(\frac{243 \sqrt{5}}{5})\cdot((-1)-(0)) \\ & =- \frac{243 \sqrt{5}}{5}.\end{aligned}
$$

Therefore, the surface integral is $- \frac{243 \sqrt{5}}{5}$.

---

### generated authored bank / source family q-161318

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/ce2f2c97892c2377764df14ac7e0b420b32a680c4f3ccfdac5af264932ab0c56.png)

Evaluate the surface integral

$$\iint_S 8 x^{2} y\,\mathrm{d}S,$$

where $S$ is defined by $z=2 x + 2 y$ and whose domain is the quarter-circle in the first quadrant of radius $1$ centered at $O$, as shown above. Give an exact answer.

- $\frac{1}{20}$
- $\frac{8}{5}$
- $\frac{8}{15}$
- $\frac{24}{5}$
- $\frac{8}{5} - \frac{2 \sqrt{2}}{5}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(2 x + 2 y)=2,$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(2 x + 2 y)=2.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{8 x^{2} y}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(8 x^{2} y)\cdot\sqrt{1+(2)^2+(2)^2}}\,\mathrm{d}A \\ & =\iint_D{(8 x^{2} y)\cdot\sqrt{9}}\,\mathrm{d}A \\ & =(3)\iint_D{8 x^{2} y}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 1,\ 0\le\theta\le \frac{\pi}{2}\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(3)\iint_D{8 x^{2} y}\,\mathrm{d}A & =(3)\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{(8(r\cos\theta)^2(r\sin\theta))\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{8 r^{4}\cos^2\theta\sin\theta}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{(\cos^2\theta\sin\theta)\int_{0}^{1}{8 r^{4}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{(\cos^2\theta\sin\theta)\left[\frac{8 r^{5}}{5}\right]_{0}^{1}}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{(\cos^2\theta\sin\theta)\left[((\frac{8}{5}))-((0))\right]}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{\frac{8 \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)}}{5}}\,\mathrm{d}\theta \\ & =(\frac{8}{5})\left[- \cos^{3}{\left(\theta \right)}\right]_{0}^{\frac{\pi}{2}} \\ & =(\frac{8}{5})\left[((0))-((-1))\right] \\ & =(\frac{8}{5})\cdot((0)-(-1)) \\ & =\frac{8}{5}.\end{aligned}
$$

Therefore, the surface integral is $\frac{8}{5}$.

---

### original evidence q-161322

![](/media/jake/SSD/EDB/math/images/92/9215246969b621002a96dec3aed8a012045b8061371e4c6a1234f54d53de29cc.png)

Evaluate the surface integral 

$$
{∬}_{S}{e}^{{x}^{2}+{y}^{2}}\,\text{d}S,
$$

where $S$ is defined by $z=x+\sqrt{3}y$ whose domain is the circle of radius $2$ centered at $O,$ as shown above.

- $\sqrt{3}\pi $
- $(e-1)\sqrt{2}\pi $
- $\sqrt{5}({e}^{4}-1)\pi $
- $({e}^{4}-1)\pi $
- ${e}^{4}\sqrt{5}\pi $

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(x+\sqrt{3}y)=1,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(x+\sqrt{3}y)=\sqrt{3}.
$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}{∬}_{S}{e}^{{x}^{2}+{y}^{2}}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}{e}^{{x}^{2}+{y}^{2}}\cdot \sqrt{1+{1}^{2}+(\sqrt{3})^{2}}\,\text{d}A \\  & ={∬}_{D}{e}^{{x}^{2}+{y}^{2}}\cdot \sqrt{5}\,\text{d}A \\  & =\sqrt{5}{∬}_{D}\,{e}^{{x}^{2}+{y}^{2}}\,\text{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta ),$ our domain can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 2,\,0\le \theta \le 2\pi \}.
$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\operatorname{cos}⁡\theta $ and $y=r\operatorname{sin}⁡\theta ,$ we obtain 

$$
\begin{aligned}\sqrt{5}{∬}_{D}\,{e}^{{x}^{2}+{y}^{2}}\,\text{d}A & =\sqrt{5}{∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta  \\  & =\sqrt{5}{∬}_{Δ}{e}^{({r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta )}\cdot r\,\text{d}r\text{d}\theta  \\  & =\sqrt{5}{∬}_{Δ}{e}^{{r}^{2}}r\,\text{d}r\text{d}\theta  \\  & =\sqrt{5}{\int }_{0}^{2\pi }{\int }_{0}^{2}r{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta  \\  & =\sqrt{5}{\int }_{0}^{2\pi }{[\frac{{e}^{{r}^{2}}}{2}]}_{0}^{2}\,\text{d}\theta  \\  & =\sqrt{5}{\int }_{0}^{2\pi }\frac{{e}^{4}-1}{2}\,\text{d}\theta  \\  & =\frac{\sqrt{5}({e}^{4}-1)}{2}{\int }_{0}^{2\pi }\,\text{d}\theta  \\  & =\frac{\sqrt{5}({e}^{4}-1)}{2}\cdot 2\pi  \\  & =\sqrt{5}({e}^{4}-1)\pi .\end{aligned}
$$

---

### generated authored bank / source family q-161322

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/52d23bb30ea29a9679a80533cd3fef5e0c10ae6bf26ac43ad7f1f79ed0d6f209.png)

Evaluate the surface integral

$$\iint_S 3 e^{x^{2} + y^{2}}\,\mathrm{d}S,$$

where $S$ is defined by $z=\sqrt{2} x + \sqrt{2} y$ and whose domain is the disk of radius $3$ centered at $O$, as shown above. Give an exact answer.

- $- 3 \sqrt{5} \pi \left(1 - e^{9}\right)$
- $- 3 \sqrt{5} \pi \left(1 - e^{\frac{9}{4}}\right)$
- $- 15 \pi \left(1 - e^{9}\right)$
- $- \frac{3 \sqrt{5} \pi \left(1 - e^{9}\right)}{2}$
- $- 3 \pi \left(1 - e^{9}\right)$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2},$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2}.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{3 e^{x^{2} + y^{2}}}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(3 e^{x^{2} + y^{2}})\cdot\sqrt{1+(\sqrt{2})^2+(\sqrt{2})^2}}\,\mathrm{d}A \\ & =\iint_D{(3 e^{x^{2} + y^{2}})\cdot\sqrt{5}}\,\mathrm{d}A \\ & =(\sqrt{5})\iint_D{3 e^{x^{2} + y^{2}}}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 3,\ 0\le\theta\le 2 \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(\sqrt{5})\iint_D{3 e^{x^{2} + y^{2}}}\,\mathrm{d}A & =(\sqrt{5})\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{(3e^{r^2\cos^2\theta+r^2\sin^2\theta})\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{3 r e^{r^{2}}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{0}^{2 \pi}{\int_{0}^{3}{3 r e^{r^{2}}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{0}^{2 \pi}{\left[\frac{3 e^{r^{2}}}{2}\right]_{0}^{3}}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{0}^{2 \pi}{\left[((\frac{3 e^{9}}{2}))-((\frac{3}{2}))\right]}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{0}^{2 \pi}{- \frac{3}{2} + \frac{3 e^{9}}{2}}\,\mathrm{d}\theta \\ & =(\sqrt{5} \left(- \frac{3}{2} + \frac{3 e^{9}}{2}\right))\left[\theta\right]_{0}^{2 \pi} \\ & =(\sqrt{5} \left(- \frac{3}{2} + \frac{3 e^{9}}{2}\right))\left[((2 \pi))-((0))\right] \\ & =(\sqrt{5} \left(- \frac{3}{2} + \frac{3 e^{9}}{2}\right))\cdot((2 \pi)-(0)) \\ & =- 3 \sqrt{5} \pi \left(1 - e^{9}\right).\end{aligned}
$$

Therefore, the surface integral is $- 3 \sqrt{5} \pi \left(1 - e^{9}\right)$.

---

### generated authored bank / source family q-161322

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/c65e6ecdea7e108d29ef494a88a55112e0e4cfa54bec96b124c7109f42112915.png)

Evaluate the surface integral

$$\iint_S 8 e^{x^{2} + y^{2}}\,\mathrm{d}S,$$

where $S$ is defined by $z=2 x + 2 y$ and whose domain is the disk of radius $1$ centered at $O$, as shown above. Give an exact answer.

- $- 24 \pi \left(1 - e^{\frac{1}{4}}\right)$
- $24 \pi \left(-1 + e\right)$
- $8 \pi \left(-1 + e\right)$
- $72 \pi \left(-1 + e\right)$
- $12 \pi \left(-1 + e\right)$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(2 x + 2 y)=2,$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(2 x + 2 y)=2.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{8 e^{x^{2} + y^{2}}}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(8 e^{x^{2} + y^{2}})\cdot\sqrt{1+(2)^2+(2)^2}}\,\mathrm{d}A \\ & =\iint_D{(8 e^{x^{2} + y^{2}})\cdot\sqrt{9}}\,\mathrm{d}A \\ & =(3)\iint_D{8 e^{x^{2} + y^{2}}}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 1,\ 0\le\theta\le 2 \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(3)\iint_D{8 e^{x^{2} + y^{2}}}\,\mathrm{d}A & =(3)\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{(8e^{r^2\cos^2\theta+r^2\sin^2\theta})\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{8 r e^{r^{2}}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\int_{0}^{2 \pi}{\int_{0}^{1}{8 r e^{r^{2}}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{2 \pi}{\left[4 e^{r^{2}}\right]_{0}^{1}}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{2 \pi}{\left[((4 e))-((4))\right]}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{2 \pi}{-4 + 4 e}\,\mathrm{d}\theta \\ & =(-12 + 12 e)\left[\theta\right]_{0}^{2 \pi} \\ & =(-12 + 12 e)\left[((2 \pi))-((0))\right] \\ & =(-12 + 12 e)\cdot((2 \pi)-(0)) \\ & =24 \pi \left(-1 + e\right).\end{aligned}
$$

Therefore, the surface integral is $24 \pi \left(-1 + e\right)$.

---

### original evidence q-161339

![](/media/jake/SSD/EDB/math/images/d1/d19d54d0e76ced24d1bd9f865578b72f2b8d67414c8506499c6ae7b1300a6275.png)

Evaluate the surface integral 

$$
{∬}_{S}(x+y)\,\text{d}S,
$$

where $S$ is defined by $z=-2x+2y$ and whose domain is the left half-circle of radius $1$ centered at $O$, as shown above.

- $8$
- $4$
- $-2$
- $5$
- $-1$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(-2x+2y)=-2,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(-2x+2y)=2.
$$

 

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}{∬}_{S}(x+y)\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}(x+y)\cdot \sqrt{1+(-2)^{2}+{2}^{2}}\,\text{d}A \\  & ={∬}_{D}(x+y)\cdot \sqrt{9}\,\text{d}A \\  & =3{∬}_{D}\,(x+y)\,\text{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta ),$ our domain can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 1,\,\frac{\pi }{2}\le \theta \le \frac{3\pi }{2}\}.
$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\operatorname{cos}⁡\theta $ and $y=r\operatorname{sin}⁡\theta ,$ we obtain 

$$
\begin{aligned}3{∬}_{D}\,(x+y)\,\text{d}A & =3{∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta  \\  & =3{∬}_{Δ}(r\operatorname{cos}⁡\theta +r\operatorname{sin}⁡\theta )\cdot r\,\text{d}r\text{d}\theta  \\  & =3{∬}_{Δ}{r}^{2}(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )\,\text{d}r\text{d}\theta  \\  & =3{\int }_{\pi /2}^{3\pi /2}(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta ){\int }_{0}^{1}{r}^{2}\,\text{d}r\,\text{d}\theta  \\  & =3{\int }_{\pi /2}^{3\pi /2}(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta ){[\frac{{r}^{3}}{3}]}_{0}^{1}\,\text{d}\theta  \\  & ={\int }_{\pi /2}^{3\pi /2}(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )\,\text{d}\theta  \\  & =[\,\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta ]_{\pi /2}^{3\pi /2} \\  & =-2.\end{aligned}
$$

---

### generated authored bank / source family q-161339

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/9c2de137d3ef021fadb8363e566200f11c5e012e5a4fed42892ea444dca8e215.png)

Evaluate the surface integral

$$\iint_S 3(x+y)\,\mathrm{d}S,$$

where $S$ is defined by $z=\sqrt{2} x + \sqrt{2} y$ and whose domain is the left half-circle of radius $3$ centered at $O$, as shown above. Give an exact answer.

- $- 54 \sqrt{5}$
- $- \frac{27 \sqrt{5}}{4}$
- $-270$
- $0$
- $-54$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2},$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2}.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{3(x+y)}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(3(x+y))\cdot\sqrt{1+(\sqrt{2})^2+(\sqrt{2})^2}}\,\mathrm{d}A \\ & =\iint_D{(3(x+y))\cdot\sqrt{5}}\,\mathrm{d}A \\ & =(\sqrt{5})\iint_D{3(x+y)}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 3,\ \frac{\pi}{2}\le\theta\le \frac{3 \pi}{2}\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(\sqrt{5})\iint_D{3(x+y)}\,\mathrm{d}A & =(\sqrt{5})\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{(3(r\cos\theta+r\sin\theta))\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{3 r^{2}(\cos\theta+\sin\theta)}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{(\cos\theta+\sin\theta)\int_{0}^{3}{3 r^{2}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{(\cos\theta+\sin\theta)\left[r^{3}\right]_{0}^{3}}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{(\cos\theta+\sin\theta)\left[((27))-((0))\right]}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{27 \sin{\left(\theta \right)} + 27 \cos{\left(\theta \right)}}\,\mathrm{d}\theta \\ & =(27 \sqrt{5})\left[\sin{\left(\theta \right)} - \cos{\left(\theta \right)}\right]_{\frac{\pi}{2}}^{\frac{3 \pi}{2}} \\ & =(27 \sqrt{5})\left[((-1)+(0))-((1)+(0))\right] \\ & =(27 \sqrt{5})\cdot((-1)-(1)) \\ & =- 54 \sqrt{5}.\end{aligned}
$$

Therefore, the surface integral is $- 54 \sqrt{5}$.

---

### generated authored bank / source family q-161339

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/ce2f2c97892c2377764df14ac7e0b420b32a680c4f3ccfdac5af264932ab0c56.png)

Evaluate the surface integral

$$\iint_S 8(x+y)\,\mathrm{d}S,$$

where $S$ is defined by $z=2 x + 2 y$ and whose domain is the quarter-circle in the first quadrant of radius $1$ centered at $O$, as shown above. Give an exact answer.

- $2$
- $16$
- $\frac{16}{3}$
- $48$
- $8$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(2 x + 2 y)=2,$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(2 x + 2 y)=2.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{8(x+y)}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(8(x+y))\cdot\sqrt{1+(2)^2+(2)^2}}\,\mathrm{d}A \\ & =\iint_D{(8(x+y))\cdot\sqrt{9}}\,\mathrm{d}A \\ & =(3)\iint_D{8(x+y)}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 1,\ 0\le\theta\le \frac{\pi}{2}\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(3)\iint_D{8(x+y)}\,\mathrm{d}A & =(3)\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{(8(r\cos\theta+r\sin\theta))\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{8 r^{2}(\cos\theta+\sin\theta)}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{(\cos\theta+\sin\theta)\int_{0}^{1}{8 r^{2}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{(\cos\theta+\sin\theta)\left[\frac{8 r^{3}}{3}\right]_{0}^{1}}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{(\cos\theta+\sin\theta)\left[((\frac{8}{3}))-((0))\right]}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{\frac{8 \sin{\left(\theta \right)}}{3} + \frac{8 \cos{\left(\theta \right)}}{3}}\,\mathrm{d}\theta \\ & =(8)\left[\sin{\left(\theta \right)} - \cos{\left(\theta \right)}\right]_{0}^{\frac{\pi}{2}} \\ & =(8)\left[((1)+(0))-((0)+(-1))\right] \\ & =(8)\cdot((1)-(-1)) \\ & =16.\end{aligned}
$$

Therefore, the surface integral is $16$.

---

### original evidence q-161316

![](/media/jake/SSD/EDB/math/images/0b/0b1b263baf01b692a0344388207c12d3c4dac0f49d11cd4bfa744f2841df2c6b.png)

Evaluate the surface integral 

$$
{∬}_{S}\frac{4xy}{{x}^{2}+{y}^{2}}\,\text{d}S,
$$

where $S$ is defined by $z=x-\sqrt{2}y$ and whose domain is the quarter-circle of radius $3$ centered at $O$ in the fourth quadrant, as shown above.

- $10\sqrt{6}$
- $-18$
- $-21$
- $-7\sqrt{3}$
- $16$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(x-\sqrt{2}y)=1,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(x-\sqrt{2}y)=-\sqrt{2}.
$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}{∬}_{S}\frac{4xy}{{x}^{2}+{y}^{2}}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}\frac{4xy}{{x}^{2}+{y}^{2}}\cdot \sqrt{1+{1}^{2}+(-\sqrt{2})^{2}}\,\text{d}A \\  & ={∬}_{D}\frac{4xy}{{x}^{2}+{y}^{2}}\cdot \sqrt{4}\,\text{d}A \\  & =2{∬}_{D}\,\frac{4xy}{{x}^{2}+{y}^{2}}\,\text{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta ),$ our domain can be expressed as 

$$
Δ={(r,\theta )\,:\,0\le r\le 3,\,\frac{3\pi }{2}\le \theta \le 2\pi }.
$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\operatorname{cos}⁡\theta $ and $y=r\operatorname{sin}⁡\theta ,$ we obtain 

$$
\begin{aligned}2{∬}_{D}\,\frac{4xy}{{x}^{2}+{y}^{2}}\,\text{d}A & =2{∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta  \\  & =2{∬}_{Δ}\frac{4r\operatorname{cos}⁡\theta \cdot r\operatorname{sin}⁡\theta }{{r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta }\cdot r\text{ }\text{d}r\text{d}\theta  \\  & =2{∬}_{Δ}\frac{4{r}^{3}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta }{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,\text{d}r\text{d}\theta  \\  & =2{∬}_{Δ}2r\operatorname{sin}⁡2\theta \,\text{d}r\text{d}\theta  \\  & =2{\int }_{3\pi /2}^{2\pi }\operatorname{sin}⁡2\theta {\int }_{0}^{3}2r\,\text{d}r\,\text{d}\theta  \\  & =2{\int }_{3\pi /2}^{2\pi }\operatorname{sin}⁡2\theta [{r}^{2}]_{0}^{3}\,\text{d}\theta  \\  & =9{\int }_{3\pi /2}^{2\pi }\,2\operatorname{sin}⁡2\theta \,\,\text{d}r \\  & =9[-\operatorname{cos}⁡2\theta ]_{3\pi /2}^{2\pi } \\  & =9\cdot (-1-1) \\  & =-18.\end{aligned}
$$

---

### generated authored bank / source family q-161316

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/6385f17950d6e41f410131df0889429bb9ae37cbb1dc832c3a1b04883d3081a1.png)

Evaluate the surface integral

$$\iint_S \frac{3 x y}{x^{2} + y^{2}}\,\mathrm{d}S,$$

where $S$ is defined by $z=\sqrt{2} x + \sqrt{2} y$ and whose domain is the quarter-circle in the second quadrant of radius $3$ centered at $O$, as shown above. Give an exact answer. The value at $O$ may be assigned arbitrarily; it does not affect the integral.

- $- \frac{27 \sqrt{5}}{4}$
- $- \frac{27 \sqrt{5}}{16}$
- $- \frac{135}{4}$
- $- \frac{27 \sqrt{5}}{8}$
- $- \frac{27}{4}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2},$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2}.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{\frac{3 x y}{x^{2} + y^{2}}}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(\frac{3 x y}{x^{2} + y^{2}})\cdot\sqrt{1+(\sqrt{2})^2+(\sqrt{2})^2}}\,\mathrm{d}A \\ & =\iint_D{(\frac{3 x y}{x^{2} + y^{2}})\cdot\sqrt{5}}\,\mathrm{d}A \\ & =(\sqrt{5})\iint_D{\frac{3 x y}{x^{2} + y^{2}}}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 3,\ \frac{\pi}{2}\le\theta\le \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(\sqrt{5})\iint_D{\frac{3 x y}{x^{2} + y^{2}}}\,\mathrm{d}A & =(\sqrt{5})\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{(\frac{3(r\cos\theta)(r\sin\theta)}{r^2\cos^2\theta+r^2\sin^2\theta})\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{\frac{3r^3\cos\theta\sin\theta}{r^2(\cos^2\theta+\sin^2\theta)}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{\frac{3 r \sin{\left(2 \theta \right)}}{2}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{\pi}{2}}^{\pi}{(\sin{\left(2 \theta \right)})\int_{0}^{3}{\frac{3 r}{2}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{\pi}{2}}^{\pi}{(\sin{\left(2 \theta \right)})\left[\frac{3 r^{2}}{4}\right]_{0}^{3}}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{\pi}{2}}^{\pi}{(\sin{\left(2 \theta \right)})\left[((\frac{27}{4}))-((0))\right]}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{\pi}{2}}^{\pi}{\frac{27 \sin{\left(2 \theta \right)}}{4}}\,\mathrm{d}\theta \\ & =(\frac{27 \sqrt{5}}{8})\left[- \cos{\left(2 \theta \right)}\right]_{\frac{\pi}{2}}^{\pi} \\ & =(\frac{27 \sqrt{5}}{8})\left[((-1))-((1))\right] \\ & =(\frac{27 \sqrt{5}}{8})\cdot((-1)-(1)) \\ & =- \frac{27 \sqrt{5}}{4}.\end{aligned}
$$

Therefore, the surface integral is $- \frac{27 \sqrt{5}}{4}$.

---

### generated authored bank / source family q-161316

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/ce2f2c97892c2377764df14ac7e0b420b32a680c4f3ccfdac5af264932ab0c56.png)

Evaluate the surface integral

$$\iint_S \frac{8 x y}{x^{2} + y^{2}}\,\mathrm{d}S,$$

where $S$ is defined by $z=2 x + 2 y$ and whose domain is the quarter-circle in the first quadrant of radius $1$ centered at $O$, as shown above. Give an exact answer. The value at $O$ may be assigned arbitrarily; it does not affect the integral.

- $\frac{3}{2}$
- $6$
- $2$
- $18$
- $3$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(2 x + 2 y)=2,$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(2 x + 2 y)=2.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{\frac{8 x y}{x^{2} + y^{2}}}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(\frac{8 x y}{x^{2} + y^{2}})\cdot\sqrt{1+(2)^2+(2)^2}}\,\mathrm{d}A \\ & =\iint_D{(\frac{8 x y}{x^{2} + y^{2}})\cdot\sqrt{9}}\,\mathrm{d}A \\ & =(3)\iint_D{\frac{8 x y}{x^{2} + y^{2}}}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 1,\ 0\le\theta\le \frac{\pi}{2}\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(3)\iint_D{\frac{8 x y}{x^{2} + y^{2}}}\,\mathrm{d}A & =(3)\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{(\frac{8(r\cos\theta)(r\sin\theta)}{r^2\cos^2\theta+r^2\sin^2\theta})\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{\frac{8r^3\cos\theta\sin\theta}{r^2(\cos^2\theta+\sin^2\theta)}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{4 r \sin{\left(2 \theta \right)}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{(\sin{\left(2 \theta \right)})\int_{0}^{1}{4 r}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{(\sin{\left(2 \theta \right)})\left[2 r^{2}\right]_{0}^{1}}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{(\sin{\left(2 \theta \right)})\left[((2))-((0))\right]}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{\frac{\pi}{2}}{2 \sin{\left(2 \theta \right)}}\,\mathrm{d}\theta \\ & =(3)\left[- \cos{\left(2 \theta \right)}\right]_{0}^{\frac{\pi}{2}} \\ & =(3)\left[((1))-((-1))\right] \\ & =(3)\cdot((1)-(-1)) \\ & =6.\end{aligned}
$$

Therefore, the surface integral is $6$.

---

### original evidence q-161338

![](/media/jake/SSD/EDB/math/images/fe/fe04241f55bae9dae231be6486a3c53985c8dc4af9e9656787267d9d852f829e.png)

Evaluate the surface integral 

$$
{∬}_{S}(1-{x}^{2}-{y}^{2})\,\text{d}S,
$$

where $S$ is defined by $z=4x+\sqrt{3}y$ and whose domain is the circle of radius $1$ centered at $O,$ as shown above.

- $\sqrt{5}\pi $
- $\frac{3\pi }{4}$
- $\frac{\pi }{4}$
- $\frac{\pi }{2}$
- $\pi $

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(4x+\sqrt{3}y)=4,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(4x+\sqrt{3}y)=\sqrt{3}.
$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}{∬}_{S}(1-{x}^{2}-{y}^{2})\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}(1-{x}^{2}-{y}^{2})\cdot \sqrt{1+{4}^{2}+(\sqrt{3})^{2}}\,\text{d}A \\  & ={∬}_{D}(1-{x}^{2}-{y}^{2})\cdot \sqrt{20}\,\text{d}A \\  & =2\sqrt{5}{∬}_{D}\,(1-{x}^{2}-{y}^{2})\,\text{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta ),$ our domain can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 1,\,0\le \theta \le 2\pi \}.
$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\operatorname{cos}⁡\theta $ and $y=r\operatorname{sin}⁡\theta ,$ we obtain 

$$
\begin{aligned}2\sqrt{5}{∬}_{D}\,(1-{x}^{2}-{y}^{2})\,\text{d}A & =2\sqrt{5}{∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta  \\  & =2\sqrt{5}{∬}_{Δ}(1-{r}^{2}{cos}^{2}⁡\theta -{r}^{2}{sin}^{2}⁡\theta )\cdot r\text{d}r\text{d}\theta  \\  & =2\sqrt{5}{\int }_{0}^{2\pi }{\int }_{0}^{1}(r-{r}^{3})\,\text{d}r\,\text{d}\theta  \\  & =2\sqrt{5}{\int }_{0}^{2\pi }{[\frac{{r}^{2}}{2}-\frac{{r}^{4}}{4}]}_{0}^{1}\,\text{d}\theta  \\  & =2\sqrt{5}{\int }_{0}^{2\pi }\frac{1}{4}\,\text{d}\theta  \\  & =\frac{\sqrt{5}}{2}[\theta ]_{0}^{2\pi } \\  & =\sqrt{5}\pi .\end{aligned}
$$

---

### generated authored bank / source family q-161338

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/52d23bb30ea29a9679a80533cd3fef5e0c10ae6bf26ac43ad7f1f79ed0d6f209.png)

Evaluate the surface integral

$$\iint_S 3(9-x^2-y^2)\,\mathrm{d}S,$$

where $S$ is defined by $z=\sqrt{2} x + \sqrt{2} y$ and whose domain is the disk of radius $3$ centered at $O$, as shown above. Give an exact answer.

- $\frac{243 \sqrt{5} \pi}{2}$
- $\frac{1701 \sqrt{5} \pi}{32}$
- $\frac{1215 \pi}{2}$
- $\frac{243 \sqrt{5} \pi}{4}$
- $\frac{243 \pi}{2}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2},$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2}.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{3(9-x^2-y^2)}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(3(9-x^2-y^2))\cdot\sqrt{1+(\sqrt{2})^2+(\sqrt{2})^2}}\,\mathrm{d}A \\ & =\iint_D{(3(9-x^2-y^2))\cdot\sqrt{5}}\,\mathrm{d}A \\ & =(\sqrt{5})\iint_D{3(9-x^2-y^2)}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 3,\ 0\le\theta\le 2 \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(\sqrt{5})\iint_D{3(9-x^2-y^2)}\,\mathrm{d}A & =(\sqrt{5})\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{(3(9-r^2\cos^2\theta-r^2\sin^2\theta))\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{27 r-3 r^{3}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{0}^{2 \pi}{\int_{0}^{3}{27 r-3 r^{3}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{0}^{2 \pi}{\left[\frac{27 r^{2}}{2}-\frac{3 r^{4}}{4}\right]_{0}^{3}}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{0}^{2 \pi}{\left[((\frac{243}{2})+(- \frac{243}{4}))-((0)+(0))\right]}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{0}^{2 \pi}{\frac{243}{4}}\,\mathrm{d}\theta \\ & =(\frac{243 \sqrt{5}}{4})\left[\theta\right]_{0}^{2 \pi} \\ & =(\frac{243 \sqrt{5}}{4})\left[((2 \pi))-((0))\right] \\ & =(\frac{243 \sqrt{5}}{4})\cdot((2 \pi)-(0)) \\ & =\frac{243 \sqrt{5} \pi}{2}.\end{aligned}
$$

Therefore, the surface integral is $\frac{243 \sqrt{5} \pi}{2}$.

---

### generated authored bank / source family q-161338

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/c65e6ecdea7e108d29ef494a88a55112e0e4cfa54bec96b124c7109f42112915.png)

Evaluate the surface integral

$$\iint_S 8(1-x^2-y^2)\,\mathrm{d}S,$$

where $S$ is defined by $z=2 x + 2 y$ and whose domain is the disk of radius $1$ centered at $O$, as shown above. Give an exact answer.

- $\frac{21 \pi}{4}$
- $12 \pi$
- $4 \pi$
- $36 \pi$
- $6 \pi$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(2 x + 2 y)=2,$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(2 x + 2 y)=2.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{8(1-x^2-y^2)}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(8(1-x^2-y^2))\cdot\sqrt{1+(2)^2+(2)^2}}\,\mathrm{d}A \\ & =\iint_D{(8(1-x^2-y^2))\cdot\sqrt{9}}\,\mathrm{d}A \\ & =(3)\iint_D{8(1-x^2-y^2)}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 1,\ 0\le\theta\le 2 \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(3)\iint_D{8(1-x^2-y^2)}\,\mathrm{d}A & =(3)\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{(8(1-r^2\cos^2\theta-r^2\sin^2\theta))\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{8 r-8 r^{3}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\int_{0}^{2 \pi}{\int_{0}^{1}{8 r-8 r^{3}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{2 \pi}{\left[\frac{8 r^{2}}{2}-\frac{8 r^{4}}{4}\right]_{0}^{1}}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{2 \pi}{\left[((4)+(-2))-((0)+(0))\right]}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{2 \pi}{2}\,\mathrm{d}\theta \\ & =(6)\left[\theta\right]_{0}^{2 \pi} \\ & =(6)\left[((2 \pi))-((0))\right] \\ & =(6)\cdot((2 \pi)-(0)) \\ & =12 \pi.\end{aligned}
$$

Therefore, the surface integral is $12 \pi$.

---

### original evidence q-161328

![](/media/jake/SSD/EDB/math/images/78/7836860694ae6246dee36a70b86bc7fcd8cf7358d47a10586ea6880759fb1588.png)

Evaluate the surface integral 

$$
{∬}_{S}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}S,
$$

where $S$ is defined by $z=4x+\sqrt{8}y$ and whose domain is the circle of radius $2$ centered at $O,$ as shown above.

- $40\pi $
- $\frac{2\pi }{3}$
- $\frac{\pi }{3}$
- $\frac{\pi }{2}$
- $\frac{80\pi }{3}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$
{∬}_{S}f(x,y,z)\,\text{d}S={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A.
$$

For the partial derivatives, we have

$$
\frac{∂z}{∂x}=\frac{∂}{∂x}(4x+\sqrt{8}y)=4,
$$

and

$$
\frac{∂z}{∂y}=\frac{∂}{∂y}(4x+\sqrt{8}y)=\sqrt{8}.
$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}{∬}_{S}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}S & ={∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A \\  & ={∬}_{D}\sqrt{{x}^{2}+{y}^{2}}\cdot \sqrt{1+{4}^{2}+(\sqrt{8})^{2}}\,\text{d}A \\  & ={∬}_{D}\sqrt{{x}^{2}+{y}^{2}}\cdot 5\,\text{d}A \\  & =5{∬}_{D}\,\sqrt{{x}^{2}+{y}^{2}}\,\text{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta ),$ our domain can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 2,\,0\le \theta \le 2\pi \}.
$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\operatorname{cos}⁡\theta $ and $y=r\operatorname{sin}⁡\theta ,$ we obtain 

$$
\begin{aligned}5{∬}_{D}\,\sqrt{{x}^{2}+{y}^{2}}\,\text{d}A & =5{∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta  \\  & =5{∬}_{Δ}\sqrt{{r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta }\cdot r\text{d}r\text{d}\theta  \\  & =5{\int }_{0}^{2\pi }{\int }_{0}^{2}{r}^{2}\,\text{d}r\,\text{d}\theta  \\  & =5{\int }_{0}^{2\pi }{[\frac{{r}^{3}}{3}]}_{0}^{2}\,\text{d}\theta  \\  & =5{\int }_{0}^{2\pi }\frac{8}{3}\,\text{d}\theta  \\  & =\frac{40}{3}{\int }_{0}^{2\pi }\,\text{d}\theta  \\  & =\frac{40}{3}[\theta ]_{0}^{2\pi } \\  & =\frac{80\pi }{3}.\end{aligned}
$$

---

### generated authored bank / source family q-161328

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/52d23bb30ea29a9679a80533cd3fef5e0c10ae6bf26ac43ad7f1f79ed0d6f209.png)

Evaluate the surface integral

$$\iint_S 3 \sqrt{x^{2} + y^{2}}\,\mathrm{d}S,$$

where $S$ is defined by $z=\sqrt{2} x + \sqrt{2} y$ and whose domain is the disk of radius $3$ centered at $O$, as shown above. Give an exact answer.

- $54 \sqrt{5} \pi$
- $\frac{27 \sqrt{5} \pi}{4}$
- $270 \pi$
- $27 \sqrt{5} \pi$
- $54 \pi$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2},$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2}.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{3 \sqrt{x^{2} + y^{2}}}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(3 \sqrt{x^{2} + y^{2}})\cdot\sqrt{1+(\sqrt{2})^2+(\sqrt{2})^2}}\,\mathrm{d}A \\ & =\iint_D{(3 \sqrt{x^{2} + y^{2}})\cdot\sqrt{5}}\,\mathrm{d}A \\ & =(\sqrt{5})\iint_D{3 \sqrt{x^{2} + y^{2}}}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 3,\ 0\le\theta\le 2 \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(\sqrt{5})\iint_D{3 \sqrt{x^{2} + y^{2}}}\,\mathrm{d}A & =(\sqrt{5})\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{(3\sqrt{r^2\cos^2\theta+r^2\sin^2\theta})\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{3 r^{2}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{0}^{2 \pi}{\int_{0}^{3}{3 r^{2}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{0}^{2 \pi}{\left[r^{3}\right]_{0}^{3}}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{0}^{2 \pi}{\left[((27))-((0))\right]}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{0}^{2 \pi}{27}\,\mathrm{d}\theta \\ & =(27 \sqrt{5})\left[\theta\right]_{0}^{2 \pi} \\ & =(27 \sqrt{5})\left[((2 \pi))-((0))\right] \\ & =(27 \sqrt{5})\cdot((2 \pi)-(0)) \\ & =54 \sqrt{5} \pi.\end{aligned}
$$

Therefore, the surface integral is $54 \sqrt{5} \pi$.

---

### generated authored bank / source family q-161328

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/c65e6ecdea7e108d29ef494a88a55112e0e4cfa54bec96b124c7109f42112915.png)

Evaluate the surface integral

$$\iint_S 8 \sqrt{x^{2} + y^{2}}\,\mathrm{d}S,$$

where $S$ is defined by $z=2 x + 2 y$ and whose domain is the disk of radius $1$ centered at $O$, as shown above. Give an exact answer.

- $2 \pi$
- $16 \pi$
- $\frac{16 \pi}{3}$
- $48 \pi$
- $8 \pi$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(2 x + 2 y)=2,$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(2 x + 2 y)=2.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{8 \sqrt{x^{2} + y^{2}}}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(8 \sqrt{x^{2} + y^{2}})\cdot\sqrt{1+(2)^2+(2)^2}}\,\mathrm{d}A \\ & =\iint_D{(8 \sqrt{x^{2} + y^{2}})\cdot\sqrt{9}}\,\mathrm{d}A \\ & =(3)\iint_D{8 \sqrt{x^{2} + y^{2}}}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 1,\ 0\le\theta\le 2 \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(3)\iint_D{8 \sqrt{x^{2} + y^{2}}}\,\mathrm{d}A & =(3)\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{(8\sqrt{r^2\cos^2\theta+r^2\sin^2\theta})\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{8 r^{2}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\int_{0}^{2 \pi}{\int_{0}^{1}{8 r^{2}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{2 \pi}{\left[\frac{8 r^{3}}{3}\right]_{0}^{1}}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{2 \pi}{\left[((\frac{8}{3}))-((0))\right]}\,\mathrm{d}\theta \\ & =(3)\int_{0}^{2 \pi}{\frac{8}{3}}\,\mathrm{d}\theta \\ & =(8)\left[\theta\right]_{0}^{2 \pi} \\ & =(8)\left[((2 \pi))-((0))\right] \\ & =(8)\cdot((2 \pi)-(0)) \\ & =16 \pi.\end{aligned}
$$

Therefore, the surface integral is $16 \pi$.

---

### generated easy 

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/52d23bb30ea29a9679a80533cd3fef5e0c10ae6bf26ac43ad7f1f79ed0d6f209.png)

Evaluate the surface integral

$$\iint_S 4\,\mathrm{d}S,$$

where $S$ is defined by $z=- x + y$ and whose domain is the disk of radius $3$ centered at $O$, as shown above. Give an exact answer.

- $108 \pi$
- $36 \pi$
- $36 \sqrt{3} \pi$
- $9 \sqrt{3} \pi$
- $18 \sqrt{3} \pi$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(- x + y)=-1,$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(- x + y)=1.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{4}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(4)\cdot\sqrt{1+(-1)^2+(1)^2}}\,\mathrm{d}A \\ & =\iint_D{(4)\cdot\sqrt{3}}\,\mathrm{d}A \\ & =(\sqrt{3})\iint_D{4}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 3,\ 0\le\theta\le 2 \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(\sqrt{3})\iint_D{4}\,\mathrm{d}A & =(\sqrt{3})\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{3})\iint_\Delta{(4)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{3})\iint_\Delta{4 r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{3})\int_{0}^{2 \pi}{\int_{0}^{3}{4 r}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(\sqrt{3})\int_{0}^{2 \pi}{\left[2 r^{2}\right]_{0}^{3}}\,\mathrm{d}\theta \\ & =(\sqrt{3})\int_{0}^{2 \pi}{\left[((18))-((0))\right]}\,\mathrm{d}\theta \\ & =(\sqrt{3})\int_{0}^{2 \pi}{18}\,\mathrm{d}\theta \\ & =(18 \sqrt{3})\left[\theta\right]_{0}^{2 \pi} \\ & =(18 \sqrt{3})\left[((2 \pi))-((0))\right] \\ & =(18 \sqrt{3})\cdot((2 \pi)-(0)) \\ & =36 \sqrt{3} \pi.\end{aligned}
$$

Therefore, the surface integral is $36 \sqrt{3} \pi$.

---

### generated easy 

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/c65e6ecdea7e108d29ef494a88a55112e0e4cfa54bec96b124c7109f42112915.png)

Evaluate the surface integral

$$\iint_S 5\,\mathrm{d}S,$$

where $S$ is defined by $z=- x + y$ and whose domain is the disk of radius $1$ centered at $O$, as shown above. Give an exact answer.

- $15 \pi$
- $\frac{5 \sqrt{3} \pi}{2}$
- $\frac{5 \sqrt{3} \pi}{4}$
- $5 \sqrt{3} \pi$
- $5 \pi$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(- x + y)=-1,$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(- x + y)=1.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{5}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(5)\cdot\sqrt{1+(-1)^2+(1)^2}}\,\mathrm{d}A \\ & =\iint_D{(5)\cdot\sqrt{3}}\,\mathrm{d}A \\ & =(\sqrt{3})\iint_D{5}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 1,\ 0\le\theta\le 2 \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(\sqrt{3})\iint_D{5}\,\mathrm{d}A & =(\sqrt{3})\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{3})\iint_\Delta{(5)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{3})\iint_\Delta{5 r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{3})\int_{0}^{2 \pi}{\int_{0}^{1}{5 r}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(\sqrt{3})\int_{0}^{2 \pi}{\left[\frac{5 r^{2}}{2}\right]_{0}^{1}}\,\mathrm{d}\theta \\ & =(\sqrt{3})\int_{0}^{2 \pi}{\left[((\frac{5}{2}))-((0))\right]}\,\mathrm{d}\theta \\ & =(\sqrt{3})\int_{0}^{2 \pi}{\frac{5}{2}}\,\mathrm{d}\theta \\ & =(\frac{5 \sqrt{3}}{2})\left[\theta\right]_{0}^{2 \pi} \\ & =(\frac{5 \sqrt{3}}{2})\left[((2 \pi))-((0))\right] \\ & =(\frac{5 \sqrt{3}}{2})\cdot((2 \pi)-(0)) \\ & =5 \sqrt{3} \pi.\end{aligned}
$$

Therefore, the surface integral is $5 \sqrt{3} \pi$.

---

### generated moderate 

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/f56c20db7c0f46c759b74ad8ddc847f9408228eb311ac5bb9ad54efd9c4fb8f2.png)

Evaluate the surface integral

$$\iint_S 4 y\,\mathrm{d}S,$$

where $S$ is defined by $z=- x + y$ and whose domain is the quarter-circle in the fourth quadrant of radius $3$ centered at $O$, as shown above. Give an exact answer.

- $-108$
- $-36$
- $- 36 \sqrt{3}$
- $- \frac{9 \sqrt{3}}{2}$
- $- 18 \sqrt{6}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(- x + y)=-1,$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(- x + y)=1.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{4 y}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(4 y)\cdot\sqrt{1+(-1)^2+(1)^2}}\,\mathrm{d}A \\ & =\iint_D{(4 y)\cdot\sqrt{3}}\,\mathrm{d}A \\ & =(\sqrt{3})\iint_D{4 y}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 3,\ \frac{3 \pi}{2}\le\theta\le 2 \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(\sqrt{3})\iint_D{4 y}\,\mathrm{d}A & =(\sqrt{3})\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{3})\iint_\Delta{(4(r\sin\theta))\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{3})\iint_\Delta{4 r^{2} \sin{\left(\theta \right)}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{3})\int_{\frac{3 \pi}{2}}^{2 \pi}{(\sin{\left(\theta \right)})\int_{0}^{3}{4 r^{2}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(\sqrt{3})\int_{\frac{3 \pi}{2}}^{2 \pi}{(\sin{\left(\theta \right)})\left[\frac{4 r^{3}}{3}\right]_{0}^{3}}\,\mathrm{d}\theta \\ & =(\sqrt{3})\int_{\frac{3 \pi}{2}}^{2 \pi}{(\sin{\left(\theta \right)})\left[((36))-((0))\right]}\,\mathrm{d}\theta \\ & =(\sqrt{3})\int_{\frac{3 \pi}{2}}^{2 \pi}{36 \sin{\left(\theta \right)}}\,\mathrm{d}\theta \\ & =(36 \sqrt{3})\left[- \cos{\left(\theta \right)}\right]_{\frac{3 \pi}{2}}^{2 \pi} \\ & =(36 \sqrt{3})\left[((-1))-((0))\right] \\ & =(36 \sqrt{3})\cdot((-1)-(0)) \\ & =- 36 \sqrt{3}.\end{aligned}
$$

Therefore, the surface integral is $- 36 \sqrt{3}$.

---

### generated moderate 

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/e48108aa44db7ba7c95b3d9f243bc7dfd1326c7deda3351c55dfd4ff9099158d.png)

Evaluate the surface integral

$$\iint_S 5 x\,\mathrm{d}S,$$

where $S$ is defined by $z=- x + y$ and whose domain is the quarter-circle in the second quadrant of radius $1$ centered at $O$, as shown above. Give an exact answer.

- $-5$
- $\frac{5 \sqrt{3} \left(-2 + \sqrt{2}\right)}{6}$
- $- \frac{5 \sqrt{3}}{24}$
- $- \frac{5 \sqrt{3}}{3}$
- $- \frac{5}{3}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(- x + y)=-1,$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(- x + y)=1.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{5 x}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(5 x)\cdot\sqrt{1+(-1)^2+(1)^2}}\,\mathrm{d}A \\ & =\iint_D{(5 x)\cdot\sqrt{3}}\,\mathrm{d}A \\ & =(\sqrt{3})\iint_D{5 x}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 1,\ \frac{\pi}{2}\le\theta\le \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(\sqrt{3})\iint_D{5 x}\,\mathrm{d}A & =(\sqrt{3})\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{3})\iint_\Delta{(5(r\cos\theta))\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{3})\iint_\Delta{5 r^{2} \cos{\left(\theta \right)}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{3})\int_{\frac{\pi}{2}}^{\pi}{(\cos{\left(\theta \right)})\int_{0}^{1}{5 r^{2}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(\sqrt{3})\int_{\frac{\pi}{2}}^{\pi}{(\cos{\left(\theta \right)})\left[\frac{5 r^{3}}{3}\right]_{0}^{1}}\,\mathrm{d}\theta \\ & =(\sqrt{3})\int_{\frac{\pi}{2}}^{\pi}{(\cos{\left(\theta \right)})\left[((\frac{5}{3}))-((0))\right]}\,\mathrm{d}\theta \\ & =(\sqrt{3})\int_{\frac{\pi}{2}}^{\pi}{\frac{5 \cos{\left(\theta \right)}}{3}}\,\mathrm{d}\theta \\ & =(\frac{5 \sqrt{3}}{3})\left[\sin{\left(\theta \right)}\right]_{\frac{\pi}{2}}^{\pi} \\ & =(\frac{5 \sqrt{3}}{3})\left[((0))-((1))\right] \\ & =(\frac{5 \sqrt{3}}{3})\cdot((0)-(1)) \\ & =- \frac{5 \sqrt{3}}{3}.\end{aligned}
$$

Therefore, the surface integral is $- \frac{5 \sqrt{3}}{3}$.

---

### generated hard 

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/52d23bb30ea29a9679a80533cd3fef5e0c10ae6bf26ac43ad7f1f79ed0d6f209.png)

Evaluate the surface integral

$$\iint_S 7 e^{x^{2} + y^{2}}\,\mathrm{d}S,$$

where $S$ is defined by $z=- 4 x + 2 y$ and whose domain is the disk of radius $3$ centered at $O$, as shown above. Give an exact answer.

- $- 147 \pi \left(1 - e^{9}\right)$
- $- 7 \pi \left(1 - e^{9}\right)$
- $- 7 \sqrt{21} \pi \left(1 - e^{9}\right)$
- $- 7 \sqrt{21} \pi \left(1 - e^{\frac{9}{4}}\right)$
- $- \frac{7 \sqrt{21} \pi \left(1 - e^{9}\right)}{2}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(- 4 x + 2 y)=-4,$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(- 4 x + 2 y)=2.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{7 e^{x^{2} + y^{2}}}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(7 e^{x^{2} + y^{2}})\cdot\sqrt{1+(-4)^2+(2)^2}}\,\mathrm{d}A \\ & =\iint_D{(7 e^{x^{2} + y^{2}})\cdot\sqrt{21}}\,\mathrm{d}A \\ & =(\sqrt{21})\iint_D{7 e^{x^{2} + y^{2}}}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 3,\ 0\le\theta\le 2 \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(\sqrt{21})\iint_D{7 e^{x^{2} + y^{2}}}\,\mathrm{d}A & =(\sqrt{21})\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{21})\iint_\Delta{(7e^{r^2\cos^2\theta+r^2\sin^2\theta})\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{21})\iint_\Delta{7 r e^{r^{2}}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{21})\int_{0}^{2 \pi}{\int_{0}^{3}{7 r e^{r^{2}}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(\sqrt{21})\int_{0}^{2 \pi}{\left[\frac{7 e^{r^{2}}}{2}\right]_{0}^{3}}\,\mathrm{d}\theta \\ & =(\sqrt{21})\int_{0}^{2 \pi}{\left[((\frac{7 e^{9}}{2}))-((\frac{7}{2}))\right]}\,\mathrm{d}\theta \\ & =(\sqrt{21})\int_{0}^{2 \pi}{- \frac{7}{2} + \frac{7 e^{9}}{2}}\,\mathrm{d}\theta \\ & =(\sqrt{21} \left(- \frac{7}{2} + \frac{7 e^{9}}{2}\right))\left[\theta\right]_{0}^{2 \pi} \\ & =(\sqrt{21} \left(- \frac{7}{2} + \frac{7 e^{9}}{2}\right))\left[((2 \pi))-((0))\right] \\ & =(\sqrt{21} \left(- \frac{7}{2} + \frac{7 e^{9}}{2}\right))\cdot((2 \pi)-(0)) \\ & =- 7 \sqrt{21} \pi \left(1 - e^{9}\right).\end{aligned}
$$

Therefore, the surface integral is $- 7 \sqrt{21} \pi \left(1 - e^{9}\right)$.

---

### generated hard 

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/cc7810e8a7f4cfcca58da19540469e2dbad3bd79814d690377279956f3b5a97f.png)

Evaluate the surface integral

$$\iint_S 2 x y\,\mathrm{d}S,$$

where $S$ is defined by $z=2 x - 2 y$ and whose domain is the quarter-circle in the second quadrant of radius $2$ centered at $O$, as shown above. Give an exact answer.

- $-36$
- $-6$
- $- \frac{3}{4}$
- $-12$
- $-4$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(2 x - 2 y)=2,$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(2 x - 2 y)=-2.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{2 x y}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(2 x y)\cdot\sqrt{1+(2)^2+(-2)^2}}\,\mathrm{d}A \\ & =\iint_D{(2 x y)\cdot\sqrt{9}}\,\mathrm{d}A \\ & =(3)\iint_D{2 x y}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 2,\ \frac{\pi}{2}\le\theta\le \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(3)\iint_D{2 x y}\,\mathrm{d}A & =(3)\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{(2(r\cos\theta)(r\sin\theta))\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\iint_\Delta{r^{3} \sin{\left(2 \theta \right)}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3)\int_{\frac{\pi}{2}}^{\pi}{(\sin{\left(2 \theta \right)})\int_{0}^{2}{r^{3}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(3)\int_{\frac{\pi}{2}}^{\pi}{(\sin{\left(2 \theta \right)})\left[\frac{r^{4}}{4}\right]_{0}^{2}}\,\mathrm{d}\theta \\ & =(3)\int_{\frac{\pi}{2}}^{\pi}{(\sin{\left(2 \theta \right)})\left[((4))-((0))\right]}\,\mathrm{d}\theta \\ & =(3)\int_{\frac{\pi}{2}}^{\pi}{4 \sin{\left(2 \theta \right)}}\,\mathrm{d}\theta \\ & =(6)\left[- \cos{\left(2 \theta \right)}\right]_{\frac{\pi}{2}}^{\pi} \\ & =(6)\left[((-1))-((1))\right] \\ & =(6)\cdot((-1)-(1)) \\ & =-12.\end{aligned}
$$

Therefore, the surface integral is $-12$.