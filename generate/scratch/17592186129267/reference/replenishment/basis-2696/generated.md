The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=17$ between the surfaces $z=0$ and $z=12.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}{z}^{2}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V
$$

1. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{17}}{\int }_{0}^{12}r z^{2}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{17}}{\int }_{0}^{12}r^{2} z^{2}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2 \pi}{\int }_{\sqrt{17}}^{2 \sqrt{17}}{\int }_{0}^{12}r^{2} z^{2}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2 \pi}{\int }_{\sqrt{17}}^{2 \sqrt{17}}{\int }_{0}^{r}r z^{2}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{17}}{\int }_{0}^{r}r^{2} z^{2}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/99/994f3537bf54a849e6a725c4c692a2326266d8065a742b1988308c793708827f.png)

The region $R$ is a right vertical cylinder of radius $\sqrt{17}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=12.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le \sqrt{17},\,0\le \theta <2\pi ,\,0\le z\le 12\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}{z}^{2}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V & ={∭}_{Δ}{z}^{2}\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\cdot r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}r{z}^{2}\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{17}}{\int }_{0}^{12}{r}^{2}{z}^{2}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=5$ between the surfaces $z=\sqrt{{x}^{2}+{y}^{2}}$ and $z=4.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V
$$

1. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{5}}{\int }_{r^{2}}^{4}r^{2}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2 \pi}{\int }_{0}^{5}{\int }_{r^{2}}^{4}r^{3}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{5}}{\int }_{r}^{4}r^{2}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2 \pi}{\int }_{0}^{5}{\int }_{r}^{4}r\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{5}}{\int }_{r}^{4}r\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/f8/f869ef32fb741040d355c3280da541178bcac9b52477ebfa7d078d8b832a5903.png)

The region $R$ is a right vertical cylinder of radius $\sqrt{5}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=\sqrt{{x}^{2}+{y}^{2}}=r,$ and

- bounded above by $z=4.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le \sqrt{5},\,0\le \theta <2\pi ,\,r\le z\le 4\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V & ={∭}_{Δ}\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\cdot r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}r\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{5}}{\int }_{r}^{4}{r}^{2}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=17$ for $x\le 0,$ between the surfaces $z=x$ and $z={y}^{2}.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}{x}^{2}-{y}^{2}\,\text{d}V
$$

1. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{17}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)}}r^{3} \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{\sqrt{17}}{\int }_{r \sin{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)}}r^{3} \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{\sqrt{17}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)}}r^{2} \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{17}}{\int }_{r \sin{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)}}r^{2} \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{\sqrt{17}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)}}r^{3} \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/24/249116dd79140b8e49d64902c46a3f0bc7c6411c9f8e7129faf38c64e7cc859e.png)

The region $R$ is one-half of a right vertical cylinder of radius $\sqrt{17}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=x=r\operatorname{cos}⁡\theta ,$ and

- bounded above by $z={y}^{2}={r}^{2}{sin}^{2}⁡\theta .$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le \sqrt{17},\,\frac{\pi }{2}\le \theta <\frac{3\pi }{2},\,r\operatorname{cos}⁡\theta \le z\le {r}^{2}{sin}^{2}⁡\theta \}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}{x}^{2}-{y}^{2}\,\text{d}V & ={∭}_{Δ}((r\operatorname{cos}⁡\theta )^{2}-(r\operatorname{sin}⁡\theta )^{2})\cdot r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}r({r}^{2}{cos}^{2}⁡\theta -{r}^{2}{sin}^{2}⁡\theta )\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}{r}^{3}({cos}^{2}⁡\theta -{sin}^{2}⁡\theta )\,dz\,dr\,d\theta  \\  & ={\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{\sqrt{17}}{\int }_{r\operatorname{cos}⁡\theta }^{{r}^{2}{sin}^{2}⁡\theta }{r}^{3}\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=5$ for $x\le 0$ and $y\ge 0,$ between the surfaces $z=0$ and $z=\sqrt{81-({x}^{2}+{y}^{2})}.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}\text{d}V
$$

1. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{5}}{\int }_{0}^{\sqrt{81 - r^{2}}}r^{2}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{\pi}{\int }_{0}^{\sqrt{5}}{\int }_{0}^{\sqrt{81 - r^{2}}}r\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{\pi}{\int }_{0}^{\sqrt{5}}{\int }_{0}^{\sqrt{81 - r}}r^{2}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{5}}{\int }_{0}^{\sqrt{81 - r^{2}}}r\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{5}}{\int }_{0}^{\sqrt{81 - r}}r\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/3e/3e51a479b8fe2a00f7b51a8613fe2cb6a45d790d737637c31b7858766e0491ff.png)

The region $R$ is one-quarter of a right vertical cylinder of radius $\sqrt{5}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=\sqrt{81-({x}^{2}+{y}^{2})}=\sqrt{81-{r}^{2}}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le \sqrt{5},\,\frac{\pi }{2}\le \theta \le \pi ,\,0\le z\le \sqrt{81-{r}^{2}}\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\text{d}V & ={\int }_{\pi /2}^{\pi }{\int }_{0}^{\sqrt{5}}{\int }_{0}^{\sqrt{81-{r}^{2}}}r\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

The region $R$ is enclosed inside the cylinder $x^2+y^2=17$ for $x\le 0$ and $y\ge 0$, between the surfaces $z=x$ and $z=y^{2} + 12$. Express the following triple integral in cylindrical polar coordinates.

$$
\iiint_R z \left(x^{2} - y^{2}\right)\,\mathrm{d}V
$$

1. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{17}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 12}r^{4} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{17}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 12}r^{2} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{17}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 12}r^{2} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{17}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 12}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{17}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 12}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/0e/0e609e4abfb4512377285af757fa4002f8e976352c72e54a808d156a781298b1.png)

The region $R$ is one-quarter of a right vertical cylinder of radius $\sqrt{17}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=x=r \cos{\left(\theta \right)},$ and

- bounded above by $z=y^{2} + 12=r^{2} \sin^{2}{\left(\theta \right)} + 12.$

As a result, in cylindrical polar coordinates, our region can be expressed as

$$
\Delta=\{(r,\theta,z):0\le r\le \sqrt{17},\frac{\pi}{2}\le\theta\le \pi,r \cos{\left(\theta \right)}\le z\le r^{2} \sin^{2}{\left(\theta \right)} + 12\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iiint_R z \left(x^{2} - y^{2}\right)\,\mathrm{d}V&=\iiint_\Delta z((r\cos\theta)^2-(r\sin\theta)^2)\cdot r\,dz\,dr\,d\theta \\ &=\iiint_\Delta rz(r^2\cos^2\theta-r^2\sin^2\theta)\,dz\,dr\,d\theta \\ &=\iiint_\Delta r^3z(\cos^2\theta-\sin^2\theta)\,dz\,dr\,d\theta \\ &=\iiint_\Delta r^3z\cos(2\theta)\,dz\,dr\,d\theta \\ &={\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{17}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 12}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta \end{aligned}
$$

---

The region $R$ is enclosed inside the cylinder $x^2+y^2=5$ for $x\le 0$ and $y\ge 0$, between the surfaces $z=x$ and $z=y^{2} + 4$. Express the following triple integral in cylindrical polar coordinates.

$$
\iiint_R z \left(x^{2} - y^{2}\right)\,\mathrm{d}V
$$

1. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{5}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 4}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{5}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 4}r^{4} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{5}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 4}r^{2} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{5}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 4}r^{2} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{5}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 4}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/3e/3e51a479b8fe2a00f7b51a8613fe2cb6a45d790d737637c31b7858766e0491ff.png)

The region $R$ is one-quarter of a right vertical cylinder of radius $\sqrt{5}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=x=r \cos{\left(\theta \right)},$ and

- bounded above by $z=y^{2} + 4=r^{2} \sin^{2}{\left(\theta \right)} + 4.$

As a result, in cylindrical polar coordinates, our region can be expressed as

$$
\Delta=\{(r,\theta,z):0\le r\le \sqrt{5},\frac{\pi}{2}\le\theta\le \pi,r \cos{\left(\theta \right)}\le z\le r^{2} \sin^{2}{\left(\theta \right)} + 4\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iiint_R z \left(x^{2} - y^{2}\right)\,\mathrm{d}V&=\iiint_\Delta z((r\cos\theta)^2-(r\sin\theta)^2)\cdot r\,dz\,dr\,d\theta \\ &=\iiint_\Delta rz(r^2\cos^2\theta-r^2\sin^2\theta)\,dz\,dr\,d\theta \\ &=\iiint_\Delta r^3z(\cos^2\theta-\sin^2\theta)\,dz\,dr\,d\theta \\ &=\iiint_\Delta r^3z\cos(2\theta)\,dz\,dr\,d\theta \\ &={\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{5}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 4}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta \end{aligned}
$$

---

The region $R$ is enclosed inside the cylinder $x^2+y^2=30$ for $x\le 0$ and $y\ge 0$, between the surfaces $z=x$ and $z=y^{2} + 1$. Express the following triple integral in cylindrical polar coordinates.

$$
\iiint_R z \left(x^{2} - y^{2}\right)\,\mathrm{d}V
$$

1. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{30}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 1}r^{4} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{30}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 1}r^{2} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{30}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 1}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{30}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 1}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{30}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 1}r^{2} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/07/07f1c4ca9e71cac2149bee4c4ae2e4f506f280b580ff0a391229f7e1624f2119.png)

The region $R$ is one-quarter of a right vertical cylinder of radius $\sqrt{30}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=x=r \cos{\left(\theta \right)},$ and

- bounded above by $z=y^{2} + 1=r^{2} \sin^{2}{\left(\theta \right)} + 1.$

As a result, in cylindrical polar coordinates, our region can be expressed as

$$
\Delta=\{(r,\theta,z):0\le r\le \sqrt{30},\frac{\pi}{2}\le\theta\le \pi,r \cos{\left(\theta \right)}\le z\le r^{2} \sin^{2}{\left(\theta \right)} + 1\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iiint_R z \left(x^{2} - y^{2}\right)\,\mathrm{d}V&=\iiint_\Delta z((r\cos\theta)^2-(r\sin\theta)^2)\cdot r\,dz\,dr\,d\theta \\ &=\iiint_\Delta rz(r^2\cos^2\theta-r^2\sin^2\theta)\,dz\,dr\,d\theta \\ &=\iiint_\Delta r^3z(\cos^2\theta-\sin^2\theta)\,dz\,dr\,d\theta \\ &=\iiint_\Delta r^3z\cos(2\theta)\,dz\,dr\,d\theta \\ &={\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{30}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 1}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta \end{aligned}
$$

---

The region $R$ is enclosed inside the cylinder $x^2+y^2=4$ for $x\le 0$ and $y\ge 0$, between the surfaces $z=x$ and $z=y^{2} + 12$. Express the following triple integral in cylindrical polar coordinates.

$$
\iiint_R z \left(x^{2} - y^{2}\right)\,\mathrm{d}V
$$

1. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{2}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 12}r^{2} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{4}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 12}r^{2} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{2}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 12}r^{4} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{2}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 12}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{4}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 12}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/d8/d8c1c025e6e8992826d8629a129d83906a4af3c566d44dbb25fcdf7dca9df64d.png)

The region $R$ is one-quarter of a right vertical cylinder of radius $2$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=x=r \cos{\left(\theta \right)},$ and

- bounded above by $z=y^{2} + 12=r^{2} \sin^{2}{\left(\theta \right)} + 12.$

As a result, in cylindrical polar coordinates, our region can be expressed as

$$
\Delta=\{(r,\theta,z):0\le r\le 2,\frac{\pi}{2}\le\theta\le \pi,r \cos{\left(\theta \right)}\le z\le r^{2} \sin^{2}{\left(\theta \right)} + 12\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iiint_R z \left(x^{2} - y^{2}\right)\,\mathrm{d}V&=\iiint_\Delta z((r\cos\theta)^2-(r\sin\theta)^2)\cdot r\,dz\,dr\,d\theta \\ &=\iiint_\Delta rz(r^2\cos^2\theta-r^2\sin^2\theta)\,dz\,dr\,d\theta \\ &=\iiint_\Delta r^3z(\cos^2\theta-\sin^2\theta)\,dz\,dr\,d\theta \\ &=\iiint_\Delta r^3z\cos(2\theta)\,dz\,dr\,d\theta \\ &={\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{2}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 12}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta \end{aligned}
$$

---

The region $R$ is enclosed inside the cylinder $x^2+y^2=24$ for $x\le 0$ and $y\ge 0$, between the surfaces $z=x$ and $z=y^{2} + 8$. Express the following triple integral in cylindrical polar coordinates.

$$
\iiint_R z \left(x^{2} - y^{2}\right)\,\mathrm{d}V
$$

1. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{24}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 8}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{2 \sqrt{6}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 8}r^{2} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{2 \sqrt{6}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 8}r^{4} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{2 \sqrt{6}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 8}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{24}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 8}r^{2} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/83/83886f6b8e5d21c89818cecb7266a3b01aafb4e215616c56383c9f9d52aa77bd.png)

The region $R$ is one-quarter of a right vertical cylinder of radius $2 \sqrt{6}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=x=r \cos{\left(\theta \right)},$ and

- bounded above by $z=y^{2} + 8=r^{2} \sin^{2}{\left(\theta \right)} + 8.$

As a result, in cylindrical polar coordinates, our region can be expressed as

$$
\Delta=\{(r,\theta,z):0\le r\le 2 \sqrt{6},\frac{\pi}{2}\le\theta\le \pi,r \cos{\left(\theta \right)}\le z\le r^{2} \sin^{2}{\left(\theta \right)} + 8\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iiint_R z \left(x^{2} - y^{2}\right)\,\mathrm{d}V&=\iiint_\Delta z((r\cos\theta)^2-(r\sin\theta)^2)\cdot r\,dz\,dr\,d\theta \\ &=\iiint_\Delta rz(r^2\cos^2\theta-r^2\sin^2\theta)\,dz\,dr\,d\theta \\ &=\iiint_\Delta r^3z(\cos^2\theta-\sin^2\theta)\,dz\,dr\,d\theta \\ &=\iiint_\Delta r^3z\cos(2\theta)\,dz\,dr\,d\theta \\ &={\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{2 \sqrt{6}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 8}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta \end{aligned}
$$