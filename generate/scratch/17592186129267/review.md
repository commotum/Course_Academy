## original raw q-161520

The region $R$ is enclosed inside the cylinder $x^{2} + y^{2} = 25$ for $x \ge 0$ between the surfaces $z = 0$ and $z = 6 + y$.
Express the following triple integral in cylindrical polar coordinates.
$∭_(R)xzdV$

1. $\displaystyle \int_{- π / 2}^{π/2}\displaystyle \int_{0}^{5}\displaystyle \int_{0}^{6 + r cos ⁡ θ}r 2 z cos ⁡ θdzdrdθ$
2. $\displaystyle \int_{- π / 2}^{π/2}\displaystyle \int_{0}^{5}\displaystyle \int_{0}^{6 + r sin ⁡ θ}r 2 z cos ⁡ θdzdrdθ$
3. $\displaystyle \int_{0}^{π/2}\displaystyle \int_{0}^{5}\displaystyle \int_{0}^{6 + r sin ⁡ θ}r 2 z sin ⁡ θdzdrdθ$
4. $\displaystyle \int_{0}^{π/2}\displaystyle \int_{0}^{5}\displaystyle \int_{0}^{6 + r cos ⁡ θ}r z sin ⁡ θdzdrdθ$
5. $\displaystyle \int_{- π / 2}^{π/2}\displaystyle \int_{0}^{5}\displaystyle \int_{0}^{6 + r sin ⁡ θ}r z cos ⁡ θdzdrdθ$

[Original solution absent.]

---

## generated half_xz

The region $R$ is enclosed inside the cylinder $x^2+y^2=10$ for $x\ge 0$, between the surfaces $z=0$ and $z=y + 8$. Express the following triple integral in cylindrical polar coordinates.

$$
\iiint_R x z\,\mathrm{d}V
$$

1. ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{r \sin{\left(\theta \right)} + 8}r^{2} z \sin{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{r \cos{\left(\theta \right)} + 8}r z \sin{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{- \frac{\pi}{2}}^{\frac{\pi}{2}}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{r \cos{\left(\theta \right)} + 8}r^{2} z \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{- \frac{\pi}{2}}^{\frac{\pi}{2}}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{r \sin{\left(\theta \right)} + 8}r^{2} z \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{- \frac{\pi}{2}}^{\frac{\pi}{2}}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{r \sin{\left(\theta \right)} + 8}r z \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-6a7adecbe9d05c474e08cc8adc644e478976ef3c03cea1c675b5cd0c35661a95.png)

The region $R$ is one-half of a right vertical cylinder of radius $\sqrt{10}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0=0,$ and

- bounded above by $z=y + 8=r \sin{\left(\theta \right)} + 8.$

As a result, in cylindrical polar coordinates, our region can be expressed as

$$
\Delta=\{(r,\theta,z):0\le r\le \sqrt{10},- \frac{\pi}{2}\le\theta\le \frac{\pi}{2},0\le z\le r \sin{\left(\theta \right)} + 8\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iiint_R x z\,\mathrm{d}V&=\iiint_\Delta (r\cos\theta)z\cdot r\,dz\,dr\,d\theta \\ &=\iiint_\Delta r^2z\cos\theta\,dz\,dr\,d\theta \\ &={\int }_{- \frac{\pi}{2}}^{\frac{\pi}{2}}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{r \sin{\left(\theta \right)} + 8}r^{2} z \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta \end{aligned}
$$

---

## generated half_xz

The region $R$ is enclosed inside the cylinder $x^2+y^2=11$ for $x\ge 0$, between the surfaces $z=0$ and $z=y + 4$. Express the following triple integral in cylindrical polar coordinates.

$$
\iiint_R x z\,\mathrm{d}V
$$

1. ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{\sqrt{11}}{\int }_{0}^{r \sin{\left(\theta \right)} + 4}r^{2} z \sin{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{\sqrt{11}}{\int }_{0}^{r \cos{\left(\theta \right)} + 4}r z \sin{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{- \frac{\pi}{2}}^{\frac{\pi}{2}}{\int }_{0}^{\sqrt{11}}{\int }_{0}^{r \cos{\left(\theta \right)} + 4}r^{2} z \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{- \frac{\pi}{2}}^{\frac{\pi}{2}}{\int }_{0}^{\sqrt{11}}{\int }_{0}^{r \sin{\left(\theta \right)} + 4}r^{2} z \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{- \frac{\pi}{2}}^{\frac{\pi}{2}}{\int }_{0}^{\sqrt{11}}{\int }_{0}^{r \sin{\left(\theta \right)} + 4}r z \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-31fca9ab20e300a443729a83c79eda833152531acbc8c8d3ab87e2eeaaf99e3e.png)

The region $R$ is one-half of a right vertical cylinder of radius $\sqrt{11}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0=0,$ and

- bounded above by $z=y + 4=r \sin{\left(\theta \right)} + 4.$

As a result, in cylindrical polar coordinates, our region can be expressed as

$$
\Delta=\{(r,\theta,z):0\le r\le \sqrt{11},- \frac{\pi}{2}\le\theta\le \frac{\pi}{2},0\le z\le r \sin{\left(\theta \right)} + 4\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iiint_R x z\,\mathrm{d}V&=\iiint_\Delta (r\cos\theta)z\cdot r\,dz\,dr\,d\theta \\ &=\iiint_\Delta r^2z\cos\theta\,dz\,dr\,d\theta \\ &={\int }_{- \frac{\pi}{2}}^{\frac{\pi}{2}}{\int }_{0}^{\sqrt{11}}{\int }_{0}^{r \sin{\left(\theta \right)} + 4}r^{2} z \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta \end{aligned}
$$

---

## original raw q-39481

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=9$ between the surfaces $z=1$ and $z=10-x.$
Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}z\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V
$$

1. $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{3}\displaystyle \int_{1}^{10 - r cos ⁡ θ}r 2 zdzdrdθ$
2. $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{3}\displaystyle \int_{1}^{10}r 2 zdzdrdθ$
3. $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{3}\displaystyle \int_{1}^{10 - r cos ⁡ θ}r zdzdrdθ$
4. $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{9}\displaystyle \int_{1}^{10}r 2 zdzdrdθ$
5. $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{9}\displaystyle \int_{1}^{10 - r sin ⁡ θ}r 2 zdzdrdθ$
1. ${\int }_{0}^{2\pi }{\int }_{0}^{3}{\int }_{1}^{10}{r}^{2}z\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2\pi }{\int }_{0}^{3}{\int }_{1}^{10-r\operatorname{cos}⁡\theta }{r}^{2}z\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2\pi }{\int }_{0}^{3}{\int }_{1}^{10-r\operatorname{cos}⁡\theta }rz\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2\pi }{\int }_{0}^{9}{\int }_{1}^{10-r\operatorname{sin}⁡\theta }{r}^{2}z\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2\pi }{\int }_{0}^{9}{\int }_{1}^{10}{r}^{2}z\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/9c/9c4ea0ba92e19a201e3944defa6deb0bc1ee76971adaa809521722b6ac31241f.png)

The region $R$ is a right vertical cylinder of radius $3$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=1,$ and

- bounded above by $z=10-x=10-r\operatorname{cos}⁡\theta .$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ={(r,\theta ,z)\,:\,0\le r\le 3,\,0\le \theta <2\pi ,\,1\le z\le 10-r\operatorname{cos}⁡\theta }.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}z\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V & ={∭}_{Δ}z\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\,r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}z\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,r\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{3}{\int }_{1}^{10-r\operatorname{cos}⁡\theta }{r}^{2}z\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated full_zradial

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=10$ between the surfaces $z=0$ and $z=8-x.$
Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}z\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V
$$

1. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{8}r^{2} z\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2 \pi}{\int }_{0}^{10}{\int }_{0}^{8}r^{2} z\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{- r \cos{\left(\theta \right)} + 8}r^{2} z\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2 \pi}{\int }_{0}^{10}{\int }_{0}^{- r \sin{\left(\theta \right)} + 8}r^{2} z\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{- r \cos{\left(\theta \right)} + 8}r z\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-39d14c21202e441ca00b770fe1607f17e67d75484c16a786f07cb7318e860dfc.png)

The region $R$ is a right vertical cylinder of radius $\sqrt{10}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=8-x=8-r\operatorname{cos}⁡\theta .$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le \sqrt{10},\,0\le \theta <2\pi ,\,0\le z\le 8-r\operatorname{cos}⁡\theta \}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}z\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V & ={∭}_{Δ}z\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\,r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}z\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,r\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{8-r\operatorname{cos}⁡\theta }{r}^{2}z\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated full_zradial

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=16$ between the surfaces $z=-2$ and $z=3-x.$
Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}z\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V
$$

1. ${\int }_{0}^{2 \pi}{\int }_{0}^{4}{\int }_{-2}^{- r \cos{\left(\theta \right)} + 3}r^{2} z\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2 \pi}{\int }_{0}^{16}{\int }_{-2}^{3}r^{2} z\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2 \pi}{\int }_{0}^{4}{\int }_{-2}^{3}r^{2} z\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2 \pi}{\int }_{0}^{16}{\int }_{-2}^{- r \sin{\left(\theta \right)} + 3}r^{2} z\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2 \pi}{\int }_{0}^{4}{\int }_{-2}^{- r \cos{\left(\theta \right)} + 3}r z\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-253627f77276b714b2be50721ac3b274e943c22a1c3925f92ac428b1b7b052a7.png)

The region $R$ is a right vertical cylinder of radius $4$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=-2,$ and

- bounded above by $z=3-x=3-r\operatorname{cos}⁡\theta .$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 4,\,0\le \theta <2\pi ,\,-2\le z\le 3-r\operatorname{cos}⁡\theta \}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}z\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V & ={∭}_{Δ}z\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\,r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}z\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,r\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{4}{\int }_{-2}^{3-r\operatorname{cos}⁡\theta }{r}^{2}z\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## original raw q-161605

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=1$ between the surfaces $z=0$ and $z=1.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}{z}^{2}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V
$$

1. ${\int }_{0}^{2\pi }{\int }_{0}^{1}{\int }_{0}^{1}r{z}^{2}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2\pi }{\int }_{1}^{2}{\int }_{0}^{1}{r}^{2}{z}^{2}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2\pi }{\int }_{1}^{2}{\int }_{0}^{r}r{z}^{2}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2\pi }{\int }_{0}^{1}{\int }_{0}^{1}{r}^{2}{z}^{2}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2\pi }{\int }_{0}^{1}{\int }_{0}^{r}{r}^{2}{z}^{2}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/f4/f4c6f3acefa5d89fd5064de469952da3d68d379559bb4a6a4990a2ea24e4f861.png)

The region $R$ is a right vertical cylinder of radius $1$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=1.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ={(r,\theta ,z)\,:\,0\le r\le 1,\,0\le \theta <2\pi ,\,0\le z\le 1}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}{z}^{2}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V & ={∭}_{Δ}{z}^{2}\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\cdot r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}r{z}^{2}\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{1}{\int }_{0}^{1}{r}^{2}{z}^{2}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated full_z2radial

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=10$ between the surfaces $z=0$ and $z=8.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}{z}^{2}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V
$$

1. ${\int }_{0}^{2 \pi}{\int }_{\sqrt{10}}^{2 \sqrt{10}}{\int }_{0}^{r}r z^{2}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{8}r^{2} z^{2}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{8}r z^{2}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2 \pi}{\int }_{\sqrt{10}}^{2 \sqrt{10}}{\int }_{0}^{8}r^{2} z^{2}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{r}r^{2} z^{2}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-39d14c21202e441ca00b770fe1607f17e67d75484c16a786f07cb7318e860dfc.png)

The region $R$ is a right vertical cylinder of radius $\sqrt{10}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=8.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le \sqrt{10},\,0\le \theta <2\pi ,\,0\le z\le 8\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}{z}^{2}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V & ={∭}_{Δ}{z}^{2}\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\cdot r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}r{z}^{2}\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{8}{r}^{2}{z}^{2}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated full_z2radial

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=16$ between the surfaces $z=0$ and $z=3.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}{z}^{2}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V
$$

1. ${\int }_{0}^{2 \pi}{\int }_{0}^{4}{\int }_{0}^{3}r z^{2}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2 \pi}{\int }_{4}^{8}{\int }_{0}^{r}r z^{2}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2 \pi}{\int }_{0}^{4}{\int }_{0}^{r}r^{2} z^{2}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2 \pi}{\int }_{0}^{4}{\int }_{0}^{3}r^{2} z^{2}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2 \pi}{\int }_{4}^{8}{\int }_{0}^{3}r^{2} z^{2}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-253627f77276b714b2be50721ac3b274e943c22a1c3925f92ac428b1b7b052a7.png)

The region $R$ is a right vertical cylinder of radius $4$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=3.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 4,\,0\le \theta <2\pi ,\,0\le z\le 3\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}{z}^{2}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V & ={∭}_{Δ}{z}^{2}\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\cdot r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}r{z}^{2}\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{4}{\int }_{0}^{3}{r}^{2}{z}^{2}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## original raw q-161607

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=2$ between the surfaces $z=0$ and $z=\sqrt{16-({x}^{2}+{y}^{2})}.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}\frac{1}{\sqrt{1+z}}\,\text{d}V
$$

1. ${\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{2}}{\int }_{0}^{\sqrt{16-{r}^{2}}}\frac{r}{\sqrt{1+z}}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2\pi }{\int }_{0}^{2}{\int }_{0}^{\sqrt{4-r}}\frac{1}{\sqrt{1+z}}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{2}}{\int }_{0}^{\sqrt{4-r}}\frac{r}{\sqrt{1+z}}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2\pi }{\int }_{0}^{2}{\int }_{0}^{\sqrt{16-{r}^{2}}}\frac{r}{\sqrt{1+z}}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{2}}{\int }_{0}^{\sqrt{16-{r}^{2}}}\frac{1}{\sqrt{1+z}}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/36/36839d1fbde65e86df7335d40374fe72a5ff43ed92b89405327406a62dc8763c.png)

The region $R$ is a right vertical cylinder of radius $\sqrt{2}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=\sqrt{16-({x}^{2}+{y}^{2})}=\sqrt{16-{r}^{2}}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ={(r,\theta ,z)\,:\,0\le r\le \sqrt{2},\,0\le \theta <2\pi ,\,0\le z\le \sqrt{16-{r}^{2}}}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\frac{1}{\sqrt{z}}\,\text{d}V & ={∭}_{Δ}\frac{1}{\sqrt{1+z}}\cdot r\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{2}}{\int }_{0}^{\sqrt{16-{r}^{2}}}\frac{r}{\sqrt{1+z}}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated full_sphere_inverse

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=6$ between the surfaces $z=0$ and $z=\sqrt{64-({x}^{2}+{y}^{2})}.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}\frac{1}{\sqrt{1+z}}\,\text{d}V
$$

1. ${\int }_{0}^{2 \pi}{\int }_{0}^{6}{\int }_{0}^{\sqrt{8 - r}}\frac{1}{\sqrt{z + 1}}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2 \pi}{\int }_{0}^{6}{\int }_{0}^{\sqrt{64 - r^{2}}}\frac{r}{\sqrt{z + 1}}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{6}}{\int }_{0}^{\sqrt{8 - r}}\frac{r}{\sqrt{z + 1}}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{6}}{\int }_{0}^{\sqrt{64 - r^{2}}}\frac{r}{\sqrt{z + 1}}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{6}}{\int }_{0}^{\sqrt{64 - r^{2}}}\frac{1}{\sqrt{z + 1}}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-c34ac99073b685ae8384281b4e269f5b348d1d8163c54e02b7030494e3f69131.png)

The region $R$ is a right vertical cylinder of radius $\sqrt{6}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=\sqrt{64-({x}^{2}+{y}^{2})}=\sqrt{64-{r}^{2}}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le \sqrt{6},\,0\le \theta <2\pi ,\,0\le z\le \sqrt{64-{r}^{2}}\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\frac{1}{\sqrt{1+z}}\,\text{d}V & ={∭}_{Δ}\frac{1}{\sqrt{1+z}}\cdot r\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{6}}{\int }_{0}^{\sqrt{64-{r}^{2}}}\frac{r}{\sqrt{1+z}}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated full_sphere_inverse

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=8$ between the surfaces $z=0$ and $z=\sqrt{64-({x}^{2}+{y}^{2})}.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}\frac{1}{\sqrt{1+z}}\,\text{d}V
$$

1. ${\int }_{0}^{2 \pi}{\int }_{0}^{2 \sqrt{2}}{\int }_{0}^{\sqrt{8 - r}}\frac{r}{\sqrt{z + 1}}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2 \pi}{\int }_{0}^{2 \sqrt{2}}{\int }_{0}^{\sqrt{64 - r^{2}}}\frac{1}{\sqrt{z + 1}}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2 \pi}{\int }_{0}^{8}{\int }_{0}^{\sqrt{8 - r}}\frac{1}{\sqrt{z + 1}}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2 \pi}{\int }_{0}^{2 \sqrt{2}}{\int }_{0}^{\sqrt{64 - r^{2}}}\frac{r}{\sqrt{z + 1}}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2 \pi}{\int }_{0}^{8}{\int }_{0}^{\sqrt{64 - r^{2}}}\frac{r}{\sqrt{z + 1}}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-54c50082895500eb46206f90413a187bda548b2b54a4f437a72ccc7b967ba9d6.png)

The region $R$ is a right vertical cylinder of radius $2 \sqrt{2}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=\sqrt{64-({x}^{2}+{y}^{2})}=\sqrt{64-{r}^{2}}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 2 \sqrt{2},\,0\le \theta <2\pi ,\,0\le z\le \sqrt{64-{r}^{2}}\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\frac{1}{\sqrt{1+z}}\,\text{d}V & ={∭}_{Δ}\frac{1}{\sqrt{1+z}}\cdot r\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{2 \sqrt{2}}{\int }_{0}^{\sqrt{64-{r}^{2}}}\frac{r}{\sqrt{1+z}}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## original raw q-161611

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=9$ for $x\le 0,$ between the surfaces $z=x$ and $z={y}^{2}.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}{x}^{2}-{y}^{2}\,\text{d}V
$$

1. ${\int }_{\pi /2}^{\pi }{\int }_{0}^{3}{\int }_{r\operatorname{cos}⁡\theta }^{{r}^{2}{sin}^{2}⁡\theta }{r}^{3}\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{3}{\int }_{r\operatorname{cos}⁡\theta }^{{r}^{2}{sin}^{2}⁡\theta }{r}^{2}\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\pi /2}^{\pi }{\int }_{0}^{3}{\int }_{r\operatorname{sin}⁡\theta }^{{r}^{2}{sin}^{2}⁡\theta }{r}^{2}\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{3}{\int }_{r\operatorname{sin}⁡\theta }^{{r}^{2}{sin}^{2}⁡\theta }{r}^{3}\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{3}{\int }_{r\operatorname{cos}⁡\theta }^{{r}^{2}{sin}^{2}⁡\theta }{r}^{3}\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/16/16b7c2f69bb20df2faafabf10368776cb69b608bb61eb8432495ae5f146e7100.png)

The region $R$ is one-half of a right vertical cylinder of radius $3$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=x=r\operatorname{cos}⁡\theta ,$ and

- bounded above by $z={y}^{2}={r}^{2}{sin}^{2}⁡\theta .$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ={(r,\theta ,z)\,:\,0\le r\le 3,\,\frac{\pi }{2}\le \theta <\frac{3\pi }{2},\,r\operatorname{cos}⁡\theta \le z\le {r}^{2}{sin}^{2}⁡\theta }.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}{x}^{2}-{y}^{2}\,\text{d}V & ={∭}_{Δ}((r\operatorname{cos}⁡\theta )^{2}-(r\operatorname{sin}⁡\theta )^{2})\cdot r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}r({r}^{2}{cos}^{2}⁡\theta -{r}^{2}{sin}^{2}⁡\theta )\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}{r}^{3}({cos}^{2}⁡\theta -{sin}^{2}⁡\theta )\,dz\,dr\,d\theta  \\  & ={\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{3}{\int }_{r\operatorname{cos}⁡\theta }^{{r}^{2}{sin}^{2}⁡\theta }{r}^{3}\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated half_difference

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=10$ for $x\le 0,$ between the surfaces $z=x$ and $z={y}^{2}.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}{x}^{2}-{y}^{2}\,\text{d}V
$$

1. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{10}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)}}r^{3} \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{\sqrt{10}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)}}r^{2} \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{10}}{\int }_{r \sin{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)}}r^{2} \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{\sqrt{10}}{\int }_{r \sin{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)}}r^{3} \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{\sqrt{10}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)}}r^{3} \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-18580e050efef846d690decbfe19087a909ad41e5d3873cfc3cb711dc9d14f94.png)

The region $R$ is one-half of a right vertical cylinder of radius $\sqrt{10}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=x=r\operatorname{cos}⁡\theta ,$ and

- bounded above by $z={y}^{2}={r}^{2}{sin}^{2}⁡\theta .$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le \sqrt{10},\,\frac{\pi }{2}\le \theta <\frac{3\pi }{2},\,r\operatorname{cos}⁡\theta \le z\le {r}^{2}{sin}^{2}⁡\theta \}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}{x}^{2}-{y}^{2}\,\text{d}V & ={∭}_{Δ}((r\operatorname{cos}⁡\theta )^{2}-(r\operatorname{sin}⁡\theta )^{2})\cdot r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}r({r}^{2}{cos}^{2}⁡\theta -{r}^{2}{sin}^{2}⁡\theta )\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}{r}^{3}({cos}^{2}⁡\theta -{sin}^{2}⁡\theta )\,dz\,dr\,d\theta  \\  & ={\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{\sqrt{10}}{\int }_{r\operatorname{cos}⁡\theta }^{{r}^{2}{sin}^{2}⁡\theta }{r}^{3}\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated half_difference

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=16$ for $x\le 0,$ between the surfaces $z=x$ and $z={y}^{2}.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}{x}^{2}-{y}^{2}\,\text{d}V
$$

1. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{4}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)}}r^{3} \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{4}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)}}r^{3} \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{4}{\int }_{r \sin{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)}}r^{2} \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{4}{\int }_{r \sin{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)}}r^{3} \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{4}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)}}r^{2} \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-4a2305169e13f40b1a1a5734ae53f14153f1699babd2a39d50ce3d6aca2aefed.png)

The region $R$ is one-half of a right vertical cylinder of radius $4$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=x=r\operatorname{cos}⁡\theta ,$ and

- bounded above by $z={y}^{2}={r}^{2}{sin}^{2}⁡\theta .$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 4,\,\frac{\pi }{2}\le \theta <\frac{3\pi }{2},\,r\operatorname{cos}⁡\theta \le z\le {r}^{2}{sin}^{2}⁡\theta \}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}{x}^{2}-{y}^{2}\,\text{d}V & ={∭}_{Δ}((r\operatorname{cos}⁡\theta )^{2}-(r\operatorname{sin}⁡\theta )^{2})\cdot r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}r({r}^{2}{cos}^{2}⁡\theta -{r}^{2}{sin}^{2}⁡\theta )\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}{r}^{3}({cos}^{2}⁡\theta -{sin}^{2}⁡\theta )\,dz\,dr\,d\theta  \\  & ={\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{4}{\int }_{r\operatorname{cos}⁡\theta }^{{r}^{2}{sin}^{2}⁡\theta }{r}^{3}\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## original raw q-161612

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=5$ for $y\ge 0,$ between the surfaces $z=-1$ and $z=y+2.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}z({x}^{2}-{y}^{2})\,\text{d}V
$$

1. ${\int }_{0}^{\pi /2}{\int }_{0}^{\sqrt{5}}{\int }_{-1}^{r\operatorname{cos}⁡\theta +2}{r}^{2}z\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{\pi /2}{\int }_{0}^{\sqrt{5}}{\int }_{-1}^{r\operatorname{sin}⁡\theta +2}{r}^{3}z\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{\pi }{\int }_{0}^{\sqrt{5}}{\int }_{-1}^{r\operatorname{cos}⁡\theta +2}{r}^{3}z\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{\pi }{\int }_{0}^{\sqrt{5}}{\int }_{-1}^{r\operatorname{sin}⁡\theta +2}{r}^{2}z\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{\pi }{\int }_{0}^{\sqrt{5}}{\int }_{-1}^{r\operatorname{sin}⁡\theta +2}{r}^{3}z\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/7d/7d3ef0b0a9a2f1c9ab60b4ed09f8a0318c57f74236e404baf181e0197ef66002.png)

The region $R$ is one-half of a right vertical cylinder of radius $\sqrt{5}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=-1,$ and

- bounded above by $z=y+2=r\operatorname{sin}⁡\theta +2.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ={(r,\theta ,z)\,:\,0\le r\le \sqrt{5},\,0\le \theta \le \pi ,\,-1\le z\le r\operatorname{sin}⁡\theta +2}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}z({x}^{2}-{y}^{2})\,\text{d}V & ={∭}_{Δ}z((r\operatorname{cos}⁡\theta )^{2}-(r\operatorname{sin}⁡\theta )^{2})r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}rz({r}^{2}{cos}^{2}⁡\theta -{r}^{2}{sin}^{2}⁡\theta )r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}{r}^{3}z({cos}^{2}⁡\theta -{sin}^{2}⁡\theta )dz\,dr\,d\theta  \\  & ={\int }_{0}^{\pi }{\int }_{0}^{\sqrt{5}}{\int }_{-1}^{r\operatorname{sin}⁡\theta +2}{r}^{3}z\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated half_zdifference

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=10$ for $y\ge 0,$ between the surfaces $z=0$ and $z=y+8.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}z({x}^{2}-{y}^{2})\,\text{d}V
$$

1. ${\int }_{0}^{\pi}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{r \cos{\left(\theta \right)} + 8}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{\pi}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{r \sin{\left(\theta \right)} + 8}r^{2} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{r \cos{\left(\theta \right)} + 8}r^{2} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{\pi}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{r \sin{\left(\theta \right)} + 8}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{r \sin{\left(\theta \right)} + 8}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-8c0135acb69f554799f78daa2032ac3e052b2076f7bb006481d8ca7511677a0b.png)

The region $R$ is one-half of a right vertical cylinder of radius $\sqrt{10}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=y+8=r\operatorname{sin}⁡\theta +8.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le \sqrt{10},\,0\le \theta \le \pi ,\,0\le z\le r\operatorname{sin}⁡\theta +8\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}z({x}^{2}-{y}^{2})\,\text{d}V & ={∭}_{Δ}z((r\operatorname{cos}⁡\theta )^{2}-(r\operatorname{sin}⁡\theta )^{2})r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}rz({r}^{2}{cos}^{2}⁡\theta -{r}^{2}{sin}^{2}⁡\theta )\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}{r}^{3}z({cos}^{2}⁡\theta -{sin}^{2}⁡\theta )dz\,dr\,d\theta  \\  & ={\int }_{0}^{\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{r\operatorname{sin}⁡\theta +8}{r}^{3}z\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated half_zdifference

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=16$ for $y\ge 0,$ between the surfaces $z=-2$ and $z=y+3.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}z({x}^{2}-{y}^{2})\,\text{d}V
$$

1. ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{4}{\int }_{-2}^{r \cos{\left(\theta \right)} + 3}r^{2} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{\pi}{\int }_{0}^{4}{\int }_{-2}^{r \sin{\left(\theta \right)} + 3}r^{2} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{\pi}{\int }_{0}^{4}{\int }_{-2}^{r \cos{\left(\theta \right)} + 3}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{\pi}{\int }_{0}^{4}{\int }_{-2}^{r \sin{\left(\theta \right)} + 3}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{4}{\int }_{-2}^{r \sin{\left(\theta \right)} + 3}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-d76d3f4ecdc5ea6b51aebc0c3028364d48069b8943fd6981bb2f589b01806b8b.png)

The region $R$ is one-half of a right vertical cylinder of radius $4$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=-2,$ and

- bounded above by $z=y+3=r\operatorname{sin}⁡\theta +3.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 4,\,0\le \theta \le \pi ,\,-2\le z\le r\operatorname{sin}⁡\theta +3\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}z({x}^{2}-{y}^{2})\,\text{d}V & ={∭}_{Δ}z((r\operatorname{cos}⁡\theta )^{2}-(r\operatorname{sin}⁡\theta )^{2})r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}rz({r}^{2}{cos}^{2}⁡\theta -{r}^{2}{sin}^{2}⁡\theta )\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}{r}^{3}z({cos}^{2}⁡\theta -{sin}^{2}⁡\theta )dz\,dr\,d\theta  \\  & ={\int }_{0}^{\pi }{\int }_{0}^{4}{\int }_{-2}^{r\operatorname{sin}⁡\theta +3}{r}^{3}z\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## original raw q-161613

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=1$ for $x\le 0$ and $y\ge 0,$ between the surfaces $z=0$ and $z=\sqrt{4-({x}^{2}+{y}^{2})}.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}\text{d}V
$$

1. ${\int }_{\pi /2}^{\pi }{\int }_{0}^{1}{\int }_{0}^{\sqrt{4-{r}^{2}}}{r}^{2}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\pi /2}^{\pi }{\int }_{0}^{1}{\int }_{0}^{\sqrt{4-r}}r\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\pi /2}^{\pi }{\int }_{0}^{1}{\int }_{0}^{\sqrt{4-{r}^{2}}}r\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{\pi }{\int }_{0}^{1}{\int }_{0}^{\sqrt{4-{r}^{2}}}r\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{\pi }{\int }_{0}^{1}{\int }_{0}^{\sqrt{4-r}}{r}^{2}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/8d/8dc4ea0ad2bb776fb31132e1ff8d97efdd2c166dc23ffbc8641f8d7034b8d487.png)

The region $R$ is one-quarter of a right vertical cylinder of radius $1$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=\sqrt{4-({x}^{2}+{y}^{2})}=\sqrt{4-{r}^{2}}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 1,\,\frac{\pi }{2}\le \theta \le \pi ,\,0\le z\le \sqrt{4-{r}^{2}}\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\text{d}V & ={\int }_{\pi /2}^{\pi }{\int }_{0}^{1}{\int }_{0}^{\sqrt{4-{r}^{2}}}r\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated quarter_sphere_volume

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=10$ for $x\le 0$ and $y\ge 0,$ between the surfaces $z=0$ and $z=\sqrt{49-({x}^{2}+{y}^{2})}.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}\text{d}V
$$

1. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{\sqrt{49 - r^{2}}}r\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{\pi}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{\sqrt{49 - r^{2}}}r\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{\sqrt{49 - r^{2}}}r^{2}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{\sqrt{49 - r}}r\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{\pi}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{\sqrt{49 - r}}r^{2}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-0361d5ae05f22bf51bffc5c913bb51a1390aeb8b17ec6d5ebb49d5f2a9375121.png)

The region $R$ is one-quarter of a right vertical cylinder of radius $\sqrt{10}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=\sqrt{49-({x}^{2}+{y}^{2})}=\sqrt{49-{r}^{2}}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le \sqrt{10},\,\frac{\pi }{2}\le \theta \le \pi ,\,0\le z\le \sqrt{49-{r}^{2}}\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\text{d}V & ={\int }_{\pi /2}^{\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{\sqrt{49-{r}^{2}}}r\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated quarter_sphere_volume

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=16$ for $x\le 0$ and $y\ge 0,$ between the surfaces $z=0$ and $z=\sqrt{36-({x}^{2}+{y}^{2})}.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}\text{d}V
$$

1. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{4}{\int }_{0}^{\sqrt{36 - r^{2}}}r^{2}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{4}{\int }_{0}^{\sqrt{36 - r^{2}}}r\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{\pi}{\int }_{0}^{4}{\int }_{0}^{\sqrt{36 - r}}r^{2}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{\pi}{\int }_{0}^{4}{\int }_{0}^{\sqrt{36 - r^{2}}}r\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{4}{\int }_{0}^{\sqrt{36 - r}}r\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-c7675ced8ad4883ec7672885f5f69c9795e80505ccac54a9300a6efccf0bad02.png)

The region $R$ is one-quarter of a right vertical cylinder of radius $4$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=\sqrt{36-({x}^{2}+{y}^{2})}=\sqrt{36-{r}^{2}}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 4,\,\frac{\pi }{2}\le \theta \le \pi ,\,0\le z\le \sqrt{36-{r}^{2}}\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\text{d}V & ={\int }_{\pi /2}^{\pi }{\int }_{0}^{4}{\int }_{0}^{\sqrt{36-{r}^{2}}}r\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## original raw q-161604

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=9$ between the surfaces $z=\sqrt{{x}^{2}+{y}^{2}}$ and $z=3.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V
$$

1. ${\int }_{0}^{2\pi }{\int }_{0}^{9}{\int }_{{r}^{2}}^{3}{r}^{3}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2\pi }{\int }_{0}^{3}{\int }_{r}^{3}{r}^{2}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2\pi }{\int }_{0}^{3}{\int }_{r}^{3}r\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2\pi }{\int }_{0}^{9}{\int }_{r}^{3}r\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2\pi }{\int }_{0}^{3}{\int }_{{r}^{2}}^{3}{r}^{2}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/9c/9c4ea0ba92e19a201e3944defa6deb0bc1ee76971adaa809521722b6ac31241f.png)

The region $R$ is a right vertical cylinder of radius $3$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=\sqrt{{x}^{2}+{y}^{2}}=r,$ and

- bounded above by $z=3.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 3,\,0\le \theta <2\pi ,\,r\le z\le 3\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V & ={∭}_{Δ}\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\cdot r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}r\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{3}{\int }_{r}^{3}{r}^{2}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated full_cone_radial

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=10$ between the surfaces $z=\sqrt{{x}^{2}+{y}^{2}}$ and $z=8.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V
$$

1. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{10}}{\int }_{r}^{8}r\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2 \pi}{\int }_{0}^{10}{\int }_{r}^{8}r\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2 \pi}{\int }_{0}^{10}{\int }_{r^{2}}^{8}r^{3}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{10}}{\int }_{r}^{8}r^{2}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{10}}{\int }_{r^{2}}^{8}r^{2}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-39d14c21202e441ca00b770fe1607f17e67d75484c16a786f07cb7318e860dfc.png)

The region $R$ is a right vertical cylinder of radius $\sqrt{10}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=\sqrt{{x}^{2}+{y}^{2}}=r,$ and

- bounded above by $z=8.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le \sqrt{10},\,0\le \theta <2\pi ,\,r\le z\le 8\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V & ={∭}_{Δ}\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\cdot r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}r\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{10}}{\int }_{r}^{8}{r}^{2}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated full_cone_radial

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=11$ between the surfaces $z=\sqrt{{x}^{2}+{y}^{2}}$ and $z=4.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V
$$

1. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{11}}{\int }_{r}^{4}r\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2 \pi}{\int }_{0}^{11}{\int }_{r}^{4}r\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2 \pi}{\int }_{0}^{11}{\int }_{r^{2}}^{4}r^{3}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{11}}{\int }_{r}^{4}r^{2}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{11}}{\int }_{r^{2}}^{4}r^{2}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-53695a87e5f1b5e20fdf58ad9200a5e46040b8286d95995368651206ad602b21.png)

The region $R$ is a right vertical cylinder of radius $\sqrt{11}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=\sqrt{{x}^{2}+{y}^{2}}=r,$ and

- bounded above by $z=4.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le \sqrt{11},\,0\le \theta <2\pi ,\,r\le z\le 4\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V & ={∭}_{Δ}\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\cdot r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}r\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{11}}{\int }_{r}^{4}{r}^{2}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated quarter_zdifference

The region $R$ is enclosed inside the cylinder $x^2+y^2=10$ for $x\le 0$ and $y\ge 0$, between the surfaces $z=x$ and $z=y^{2} + 8$. Express the following triple integral in cylindrical polar coordinates.

$$
\iiint_R z \left(x^{2} - y^{2}\right)\,\mathrm{d}V
$$

1. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{10}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 8}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{10}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 8}r^{2} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{10}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 8}r^{4} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{10}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 8}r^{2} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{10}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 8}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-0361d5ae05f22bf51bffc5c913bb51a1390aeb8b17ec6d5ebb49d5f2a9375121.png)

The region $R$ is one-quarter of a right vertical cylinder of radius $\sqrt{10}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=x=r \cos{\left(\theta \right)},$ and

- bounded above by $z=y^{2} + 8=r^{2} \sin^{2}{\left(\theta \right)} + 8.$

As a result, in cylindrical polar coordinates, our region can be expressed as

$$
\Delta=\{(r,\theta,z):0\le r\le \sqrt{10},\frac{\pi}{2}\le\theta\le \pi,r \cos{\left(\theta \right)}\le z\le r^{2} \sin^{2}{\left(\theta \right)} + 8\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iiint_R z \left(x^{2} - y^{2}\right)\,\mathrm{d}V&=\iiint_\Delta z((r\cos\theta)^2-(r\sin\theta)^2)\cdot r\,dz\,dr\,d\theta \\ &=\iiint_\Delta rz(r^2\cos^2\theta-r^2\sin^2\theta)\,dz\,dr\,d\theta \\ &=\iiint_\Delta r^3z(\cos^2\theta-\sin^2\theta)\,dz\,dr\,d\theta \\ &=\iiint_\Delta r^3z\cos(2\theta)\,dz\,dr\,d\theta \\ &={\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{10}}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 8}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta \end{aligned}
$$

---

## generated quarter_zdifference

The region $R$ is enclosed inside the cylinder $x^2+y^2=16$ for $x\le 0$ and $y\ge 0$, between the surfaces $z=x$ and $z=y^{2} + 3$. Express the following triple integral in cylindrical polar coordinates.

$$
\iiint_R z \left(x^{2} - y^{2}\right)\,\mathrm{d}V
$$

1. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{4}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 3}r^{4} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{4}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 3}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{16}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 3}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{16}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 3}r^{2} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{4}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 3}r^{2} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-c7675ced8ad4883ec7672885f5f69c9795e80505ccac54a9300a6efccf0bad02.png)

The region $R$ is one-quarter of a right vertical cylinder of radius $4$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=x=r \cos{\left(\theta \right)},$ and

- bounded above by $z=y^{2} + 3=r^{2} \sin^{2}{\left(\theta \right)} + 3.$

As a result, in cylindrical polar coordinates, our region can be expressed as

$$
\Delta=\{(r,\theta,z):0\le r\le 4,\frac{\pi}{2}\le\theta\le \pi,r \cos{\left(\theta \right)}\le z\le r^{2} \sin^{2}{\left(\theta \right)} + 3\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iiint_R z \left(x^{2} - y^{2}\right)\,\mathrm{d}V&=\iiint_\Delta z((r\cos\theta)^2-(r\sin\theta)^2)\cdot r\,dz\,dr\,d\theta \\ &=\iiint_\Delta rz(r^2\cos^2\theta-r^2\sin^2\theta)\,dz\,dr\,d\theta \\ &=\iiint_\Delta r^3z(\cos^2\theta-\sin^2\theta)\,dz\,dr\,d\theta \\ &=\iiint_\Delta r^3z\cos(2\theta)\,dz\,dr\,d\theta \\ &={\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{4}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)} + 3}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta \end{aligned}
$$

---

## generated raw evidence bank q-161520

The region $R$ is enclosed inside the cylinder $x^{2} + y^{2} = 10$ for $x \ge 0$ between the surfaces $z = 0$ and $z = 8 + y$.
Express the following triple integral in cylindrical polar coordinates.
$∭_(R)xzdV$

1. $\displaystyle \int_{- π / 2}^{π/2}\displaystyle \int_{0}^{\sqrt{10}}\displaystyle \int_{0}^{8 + r sin ⁡ θ}r z cos ⁡ θdzdrdθ$
2. $\displaystyle \int_{- π / 2}^{π/2}\displaystyle \int_{0}^{\sqrt{10}}\displaystyle \int_{0}^{8 + r sin ⁡ θ}r 2 z cos ⁡ θdzdrdθ$
3. $\displaystyle \int_{0}^{π/2}\displaystyle \int_{0}^{\sqrt{10}}\displaystyle \int_{0}^{8 + r cos ⁡ θ}r z sin ⁡ θdzdrdθ$
4. $\displaystyle \int_{- π / 2}^{π/2}\displaystyle \int_{0}^{\sqrt{10}}\displaystyle \int_{0}^{8 + r cos ⁡ θ}r 2 z cos ⁡ θdzdrdθ$
5. $\displaystyle \int_{0}^{π/2}\displaystyle \int_{0}^{\sqrt{10}}\displaystyle \int_{0}^{8 + r sin ⁡ θ}r 2 z sin ⁡ θdzdrdθ$

[Original solution absent.]

---

## generated raw evidence bank q-39481

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=10$ between the surfaces $z=0$ and $z=8-x.$
Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}z\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V
$$

1. $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{10}\displaystyle \int_{0}^{8 - r sin ⁡ θ}r 2 zdzdrdθ$
2. $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{\sqrt{10}}\displaystyle \int_{0}^{8}r 2 zdzdrdθ$
3. $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{10}\displaystyle \int_{0}^{8}r 2 zdzdrdθ$
4. $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{\sqrt{10}}\displaystyle \int_{0}^{8 - r cos ⁡ θ}r 2 zdzdrdθ$
5. $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{\sqrt{10}}\displaystyle \int_{0}^{8 - r cos ⁡ θ}r zdzdrdθ$
1. ${\int }_{0}^{2\pi }{\int }_{0}^{10}{\int }_{0}^{8}{r}^{2}z\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{8-r\operatorname{cos}⁡\theta }{r}^{2}z\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2\pi }{\int }_{0}^{10}{\int }_{0}^{8-r\operatorname{sin}⁡\theta }{r}^{2}z\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{8-r\operatorname{cos}⁡\theta }rz\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{8}{r}^{2}z\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/9c/9c4ea0ba92e19a201e3944defa6deb0bc0ee76971adaa809521722b6ac31241f.png)

The region $R$ is a right vertical cylinder of radius $\sqrt{10}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=8-x=8-r\operatorname{cos}⁡\theta .$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ={(r,\theta ,z)\,:\,0\le r\le \sqrt{10},\,0\le \theta <2\pi ,\,0\le z\le 8-r\operatorname{cos}⁡\theta }.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}z\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V & ={∭}_{Δ}z\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\,r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}z\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,r\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{8-r\operatorname{cos}⁡\theta }{r}^{2}z\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated raw evidence bank q-161605

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=10$ between the surfaces $z=0$ and $z=8.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}{z}^{2}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V
$$

1. ${\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{r}{r}^{2}{z}^{2}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2\pi }{\int }_{\sqrt{10}}^{2 \sqrt{10}}{\int }_{0}^{8}{r}^{2}{z}^{2}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{8}{r}^{2}{z}^{2}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{8}r{z}^{2}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2\pi }{\int }_{\sqrt{10}}^{2 \sqrt{10}}{\int }_{0}^{r}r{z}^{2}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/f4/f4c6f3acefa5d89fd5064de469952da3d68d379559bb4a6a4990a2ea24e4f861.png)

The region $R$ is a right vertical cylinder of radius $\sqrt{10}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=8.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ={(r,\theta ,z)\,:\,0\le r\le \sqrt{10},\,0\le \theta <2\pi ,\,0\le z\le 8}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}{z}^{2}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V & ={∭}_{Δ}{z}^{2}\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\cdot r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}r{z}^{2}\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{8}{r}^{2}{z}^{2}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated raw evidence bank q-161607

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=6$ between the surfaces $z=0$ and $z=\sqrt{64-({x}^{2}+{y}^{2})}.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}\frac{1}{\sqrt{1+z}}\,\text{d}V
$$

1. ${\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{6}}{\int }_{0}^{\sqrt{64-{r}^{2}}}\frac{1}{\sqrt{1+z}}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2\pi }{\int }_{0}^{6}{\int }_{0}^{\sqrt{8-r}}\frac{1}{\sqrt{1+z}}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2\pi }{\int }_{0}^{6}{\int }_{0}^{\sqrt{64-{r}^{2}}}\frac{r}{\sqrt{1+z}}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{6}}{\int }_{0}^{\sqrt{64-{r}^{2}}}\frac{r}{\sqrt{1+z}}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{6}}{\int }_{0}^{\sqrt{8-r}}\frac{r}{\sqrt{1+z}}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/36/36839d1fbde65e86df7335d40374fe72a5ff43ed92b89405327406a62dc8763c.png)

The region $R$ is a right vertical cylinder of radius $\sqrt{6}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=\sqrt{64-({x}^{2}+{y}^{2})}=\sqrt{64-{r}^{2}}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ={(r,\theta ,z)\,:\,0\le r\le \sqrt{6},\,0\le \theta <2\pi ,\,0\le z\le \sqrt{64-{r}^{2}}}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\frac{1}{\sqrt{z}}\,\text{d}V & ={∭}_{Δ}\frac{1}{\sqrt{1+z}}\cdot r\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{6}}{\int }_{0}^{\sqrt{64-{r}^{2}}}\frac{r}{\sqrt{1+z}}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated raw evidence bank q-161611

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=10$ for $x\le 0,$ between the surfaces $z=x$ and $z={y}^{2}.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}{x}^{2}-{y}^{2}\,\text{d}V
$$

1. ${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{\sqrt{10}}{\int }_{r\operatorname{cos}⁡\theta }^{{r}^{2}{sin}^{2}⁡\theta }{r}^{3}\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{\sqrt{10}}{\int }_{r\operatorname{cos}⁡\theta }^{{r}^{2}{sin}^{2}⁡\theta }{r}^{2}\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{\sqrt{10}}{\int }_{r\operatorname{sin}⁡\theta }^{{r}^{2}{sin}^{2}⁡\theta }{r}^{3}\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\pi /2}^{\pi }{\int }_{0}^{\sqrt{10}}{\int }_{r\operatorname{cos}⁡\theta }^{{r}^{2}{sin}^{2}⁡\theta }{r}^{3}\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\pi /2}^{\pi }{\int }_{0}^{\sqrt{10}}{\int }_{r\operatorname{sin}⁡\theta }^{{r}^{2}{sin}^{2}⁡\theta }{r}^{2}\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/16/16b7c2f69bb20df2faafabf10368776cb69b608bb61eb8432495ae5f146e7100.png)

The region $R$ is one-half of a right vertical cylinder of radius $\sqrt{10}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=x=r\operatorname{cos}⁡\theta ,$ and

- bounded above by $z={y}^{2}={r}^{2}{sin}^{2}⁡\theta .$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ={(r,\theta ,z)\,:\,0\le r\le \sqrt{10},\,\frac{\pi }{2}\le \theta <\frac{3\pi }{2},\,r\operatorname{cos}⁡\theta \le z\le {r}^{2}{sin}^{2}⁡\theta }.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}{x}^{2}-{y}^{2}\,\text{d}V & ={∭}_{Δ}((r\operatorname{cos}⁡\theta )^{2}-(r\operatorname{sin}⁡\theta )^{2})\cdot r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}r({r}^{2}{cos}^{2}⁡\theta -{r}^{2}{sin}^{2}⁡\theta )\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}{r}^{3}({cos}^{2}⁡\theta -{sin}^{2}⁡\theta )\,dz\,dr\,d\theta  \\  & ={\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{\sqrt{10}}{\int }_{r\operatorname{cos}⁡\theta }^{{r}^{2}{sin}^{2}⁡\theta }{r}^{3}\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated raw evidence bank q-161612

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=10$ for $y\ge 0,$ between the surfaces $z=0$ and $z=y+8.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}z({x}^{2}-{y}^{2})\,\text{d}V
$$

1. ${\int }_{0}^{\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{r\operatorname{sin}⁡\theta +8}{r}^{3}z\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{\pi /2}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{r\operatorname{sin}⁡\theta +8}{r}^{3}z\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{r\operatorname{sin}⁡\theta +8}{r}^{2}z\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{\pi /2}{\int }_{0}^{\sqrt{10}}{\int }_{0}^{r\operatorname{cos}⁡\theta +8}{r}^{2}z\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{r\operatorname{cos}⁡\theta +8}{r}^{3}z\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/7d/7d3ef0b0a9a2f1c9ab60b4ed09f8a0318c57f74236e404baf181e0197ef66002.png)

The region $R$ is one-half of a right vertical cylinder of radius $\sqrt{10}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=y+8=r\operatorname{sin}⁡\theta +8.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ={(r,\theta ,z)\,:\,0\le r\le \sqrt{10},\,0\le \theta \le \pi ,\,0\le z\le r\operatorname{sin}⁡\theta +8}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}z({x}^{2}-{y}^{2})\,\text{d}V & ={∭}_{Δ}z((r\operatorname{cos}⁡\theta )^{2}-(r\operatorname{sin}⁡\theta )^{2})r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}rz({r}^{2}{cos}^{2}⁡\theta -{r}^{2}{sin}^{2}⁡\theta )r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}{r}^{3}z({cos}^{2}⁡\theta -{sin}^{2}⁡\theta )dz\,dr\,d\theta  \\  & ={\int }_{0}^{\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{r\operatorname{sin}⁡\theta +8}{r}^{3}z\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated raw evidence bank q-161613

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=10$ for $x\le 0$ and $y\ge 0,$ between the surfaces $z=0$ and $z=\sqrt{49-({x}^{2}+{y}^{2})}.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}\text{d}V
$$

1. ${\int }_{0}^{\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{\sqrt{49-r}}{r}^{2}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\pi /2}^{\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{\sqrt{49-r}}r\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{\sqrt{49-{r}^{2}}}r\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\pi /2}^{\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{\sqrt{49-{r}^{2}}}{r}^{2}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\pi /2}^{\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{\sqrt{49-{r}^{2}}}r\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/8d/8dc49ea0ad2bb776fb31132e1ff8d97efdd2c166dc23ffbc8641f8d7034b8d487.png)

The region $R$ is one-quarter of a right vertical cylinder of radius $\sqrt{10}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=\sqrt{49-({x}^{2}+{y}^{2})}=\sqrt{49-{r}^{2}}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le \sqrt{10},\,\frac{\pi }{2}\le \theta \le \pi ,\,0\le z\le \sqrt{49-{r}^{2}}\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\text{d}V & ={\int }_{\pi /2}^{\pi }{\int }_{0}^{\sqrt{10}}{\int }_{0}^{\sqrt{49-{r}^{2}}}r\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated raw evidence bank q-161604

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=10$ between the surfaces $z=\sqrt{{x}^{2}+{y}^{2}}$ and $z=8.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V
$$

1. ${\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{10}}{\int }_{{r}^{2}}^{8}{r}^{2}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{10}}{\int }_{r}^{8}{r}^{2}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2\pi }{\int }_{0}^{10}{\int }_{r}^{8}r\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2\pi }{\int }_{0}^{10}{\int }_{{r}^{2}}^{8}{r}^{8}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{10}}{\int }_{r}^{8}r\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/9c/9c4ea0ba92e19a201e3944defa6deb0bc1ee76971adaa809521722b6ac31241f.png)

The region $R$ is a right vertical cylinder of radius $\sqrt{10}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=\sqrt{{x}^{2}+{y}^{2}}=r,$ and

- bounded above by $z=8.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le \sqrt{10},\,0\le \theta <2\pi ,\,r\le z\le 8\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V & ={∭}_{Δ}\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\cdot r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}r\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{10}}{\int }_{r}^{8}{r}^{2}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated authored bank half_xz

The region $R$ is enclosed inside the cylinder $x^2+y^2=2$ for $x\ge 0$, between the surfaces $z=0$ and $z=y + 11$. Express the following triple integral in cylindrical polar coordinates.

$$
\iiint_R x z\,\mathrm{d}V
$$

1. ${\int }_{- \frac{\pi}{2}}^{\frac{\pi}{2}}{\int }_{0}^{2}{\int }_{0}^{r \sin{\left(\theta \right)} + 11}r^{2} z \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{- \frac{\pi}{2}}^{\frac{\pi}{2}}{\int }_{0}^{2}{\int }_{0}^{r \sin{\left(\theta \right)} + 11}r z \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{- \frac{\pi}{2}}^{\frac{\pi}{2}}{\int }_{0}^{\sqrt{2}}{\int }_{0}^{r \sin{\left(\theta \right)} + 11}r^{2} z \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{- \frac{\pi}{2}}^{\frac{\pi}{2}}{\int }_{0}^{\sqrt{2}}{\int }_{0}^{r \sin{\left(\theta \right)} + 11}r z \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{- \frac{\pi}{2}}^{\frac{\pi}{2}}{\int }_{0}^{\sqrt{2}}{\int }_{0}^{r \sin{\left(\theta \right)} + 11}r^{3} z \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-804f44d94708ff42da0a7b3e36cd8a53e0c9786e791bae4e6e398a57f82935eb.png)

The region $R$ is one-half of a right vertical cylinder of radius $\sqrt{2}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0=0,$ and

- bounded above by $z=y + 11=r \sin{\left(\theta \right)} + 11.$

As a result, in cylindrical polar coordinates, our region can be expressed as

$$
\Delta=\{(r,\theta,z):0\le r\le \sqrt{2},- \frac{\pi}{2}\le\theta\le \frac{\pi}{2},0\le z\le r \sin{\left(\theta \right)} + 11\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iiint_R x z\,\mathrm{d}V&=\iiint_\Delta (r\cos\theta)z\cdot r\,dz\,dr\,d\theta \\ &=\iiint_\Delta r^2z\cos\theta\,dz\,dr\,d\theta \\ &={\int }_{- \frac{\pi}{2}}^{\frac{\pi}{2}}{\int }_{0}^{\sqrt{2}}{\int }_{0}^{r \sin{\left(\theta \right)} + 11}r^{2} z \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta \end{aligned}
$$

---

## generated authored bank full_zradial

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=25$ between the surfaces $z=-3$ and $z=11-x.$
Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}z\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V
$$

1. ${\int }_{0}^{2 \pi}{\int }_{0}^{25}{\int }_{-3}^{- r \cos{\left(\theta \right)} + 11}r z\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2 \pi}{\int }_{0}^{5}{\int }_{-3}^{- r \cos{\left(\theta \right)} + 11}r^{2} z\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2 \pi}{\int }_{0}^{5}{\int }_{-3}^{- r \cos{\left(\theta \right)} + 11}r^{3} z\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2 \pi}{\int }_{0}^{5}{\int }_{-3}^{- r \cos{\left(\theta \right)} + 11}r z\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2 \pi}{\int }_{0}^{25}{\int }_{-3}^{- r \cos{\left(\theta \right)} + 11}r^{2} z\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-f5f8e432b0fd9f4e1f4c2f1986e2f4f48612228ddaa59420aa956b74fbb3cd28.png)

The region $R$ is a right vertical cylinder of radius $5$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=-3,$ and

- bounded above by $z=11-x=11-r\operatorname{cos}⁡\theta .$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 5,\,0\le \theta <2\pi ,\,-3\le z\le 11-r\operatorname{cos}⁡\theta \}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}z\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V & ={∭}_{Δ}z\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\,r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}z\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,r\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{5}{\int }_{-3}^{11-r\operatorname{cos}⁡\theta }{r}^{2}z\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated authored bank full_z2radial

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=25$ between the surfaces $z=0$ and $z=1.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}{z}^{2}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V
$$

1. ${\int }_{0}^{2 \pi}{\int }_{0}^{25}{\int }_{0}^{1}r z^{2}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2 \pi}{\int }_{0}^{5}{\int }_{0}^{1}r^{2} z^{2}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2 \pi}{\int }_{0}^{5}{\int }_{0}^{1}r^{3} z^{2}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2 \pi}{\int }_{0}^{5}{\int }_{0}^{1}r z^{2}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2 \pi}{\int }_{0}^{25}{\int }_{0}^{1}r^{2} z^{2}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-f5f8e432b0fd9f4e1f4c2f1986e2f4f48612228ddaa59420aa956b74fbb3cd28.png)

The region $R$ is a right vertical cylinder of radius $5$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=1.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 5,\,0\le \theta <2\pi ,\,0\le z\le 1\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}{z}^{2}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V & ={∭}_{Δ}{z}^{2}\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\cdot r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}r{z}^{2}\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{5}{\int }_{0}^{1}{r}^{2}{z}^{2}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated authored bank full_sphere_inverse

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=2$ between the surfaces $z=0$ and $z=\sqrt{36-({x}^{2}+{y}^{2})}.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}\frac{1}{\sqrt{1+z}}\,\text{d}V
$$

1. ${\int }_{0}^{2 \pi}{\int }_{0}^{2}{\int }_{0}^{\sqrt{36 - r^{2}}}\frac{1}{\sqrt{z + 1}}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2 \pi}{\int }_{0}^{2}{\int }_{0}^{\sqrt{36 - r^{2}}}\frac{r}{\sqrt{z + 1}}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{2}}{\int }_{0}^{\sqrt{36 - r^{2}}}\frac{r^{2}}{\sqrt{z + 1}}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{2}}{\int }_{0}^{\sqrt{36 - r^{2}}}\frac{r}{\sqrt{z + 1}}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{2}}{\int }_{0}^{\sqrt{36 - r^{2}}}\frac{1}{\sqrt{z + 1}}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-c6dcd4f675a4674a4fd15f0d488c569b4fdac8a01cb263d61dbb53499528ef77.png)

The region $R$ is a right vertical cylinder of radius $\sqrt{2}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=\sqrt{36-({x}^{2}+{y}^{2})}=\sqrt{36-{r}^{2}}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le \sqrt{2},\,0\le \theta <2\pi ,\,0\le z\le \sqrt{36-{r}^{2}}\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\frac{1}{\sqrt{1+z}}\,\text{d}V & ={∭}_{Δ}\frac{1}{\sqrt{1+z}}\cdot r\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{2}}{\int }_{0}^{\sqrt{36-{r}^{2}}}\frac{r}{\sqrt{1+z}}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated authored bank half_difference

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=25$ for $x\le 0,$ between the surfaces $z=x$ and $z={y}^{2}.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}{x}^{2}-{y}^{2}\,\text{d}V
$$

1. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{5}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)}}r^{2} \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{5}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)}}r^{4} \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{25}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)}}r^{2} \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{25}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)}}r^{3} \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{5}{\int }_{r \cos{\left(\theta \right)}}^{r^{2} \sin^{2}{\left(\theta \right)}}r^{3} \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-dd5342d4e768430089e75431b2a211eb3de632e8de11a4167736e574eea65bf7.png)

The region $R$ is one-half of a right vertical cylinder of radius $5$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=x=r\operatorname{cos}⁡\theta ,$ and

- bounded above by $z={y}^{2}={r}^{2}{sin}^{2}⁡\theta .$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 5,\,\frac{\pi }{2}\le \theta <\frac{3\pi }{2},\,r\operatorname{cos}⁡\theta \le z\le {r}^{2}{sin}^{2}⁡\theta \}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}{x}^{2}-{y}^{2}\,\text{d}V & ={∭}_{Δ}((r\operatorname{cos}⁡\theta )^{2}-(r\operatorname{sin}⁡\theta )^{2})\cdot r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}r({r}^{2}{cos}^{2}⁡\theta -{r}^{2}{sin}^{2}⁡\theta )\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}{r}^{3}({cos}^{2}⁡\theta -{sin}^{2}⁡\theta )\,dz\,dr\,d\theta  \\  & ={\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{5}{\int }_{r\operatorname{cos}⁡\theta }^{{r}^{2}{sin}^{2}⁡\theta }{r}^{3}\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated authored bank half_zdifference

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=25$ for $y\ge 0,$ between the surfaces $z=-3$ and $z=y+11.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}z({x}^{2}-{y}^{2})\,\text{d}V
$$

1. ${\int }_{0}^{\pi}{\int }_{0}^{25}{\int }_{-3}^{r \sin{\left(\theta \right)} + 11}r^{2} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{\pi}{\int }_{0}^{5}{\int }_{-3}^{r \sin{\left(\theta \right)} + 11}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{\pi}{\int }_{0}^{5}{\int }_{-3}^{r \sin{\left(\theta \right)} + 11}r^{4} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{\pi}{\int }_{0}^{5}{\int }_{-3}^{r \sin{\left(\theta \right)} + 11}r^{2} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{\pi}{\int }_{0}^{25}{\int }_{-3}^{r \sin{\left(\theta \right)} + 11}r^{3} z \cos{\left(2 \theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-112441fda53fcf28d7e1f8eb4a2eac44b24eadb2c8db40d8848dc1b54202ee5a.png)

The region $R$ is one-half of a right vertical cylinder of radius $5$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=-3,$ and

- bounded above by $z=y+11=r\operatorname{sin}⁡\theta +11.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 5,\,0\le \theta \le \pi ,\,-3\le z\le r\operatorname{sin}⁡\theta +11\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}z({x}^{2}-{y}^{2})\,\text{d}V & ={∭}_{Δ}z((r\operatorname{cos}⁡\theta )^{2}-(r\operatorname{sin}⁡\theta )^{2})r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}rz({r}^{2}{cos}^{2}⁡\theta -{r}^{2}{sin}^{2}⁡\theta )\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}{r}^{3}z({cos}^{2}⁡\theta -{sin}^{2}⁡\theta )dz\,dr\,d\theta  \\  & ={\int }_{0}^{\pi }{\int }_{0}^{5}{\int }_{-3}^{r\operatorname{sin}⁡\theta +11}{r}^{3}z\operatorname{cos}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated authored bank quarter_sphere_volume

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=2$ for $x\le 0$ and $y\ge 0,$ between the surfaces $z=0$ and $z=\sqrt{36-({x}^{2}+{y}^{2})}.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}\text{d}V
$$

1. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{2}{\int }_{0}^{\sqrt{36 - r^{2}}}1\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{2}{\int }_{0}^{\sqrt{36 - r^{2}}}r\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{2}}{\int }_{0}^{\sqrt{36 - r^{2}}}r^{2}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{2}}{\int }_{0}^{\sqrt{36 - r^{2}}}r\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{\sqrt{2}}{\int }_{0}^{\sqrt{36 - r^{2}}}1\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-49d045399826a4949674ab7e849b4e3669159500d3e0d40472de030051329ae2.png)

The region $R$ is one-quarter of a right vertical cylinder of radius $\sqrt{2}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=\sqrt{36-({x}^{2}+{y}^{2})}=\sqrt{36-{r}^{2}}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le \sqrt{2},\,\frac{\pi }{2}\le \theta \le \pi ,\,0\le z\le \sqrt{36-{r}^{2}}\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\text{d}V & ={\int }_{\pi /2}^{\pi }{\int }_{0}^{\sqrt{2}}{\int }_{0}^{\sqrt{36-{r}^{2}}}r\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## generated authored bank full_cone_radial

The region $R$ is enclosed inside the cylinder ${x}^{2}+{y}^{2}=2$ between the surfaces $z=\sqrt{{x}^{2}+{y}^{2}}$ and $z=11.$ Express the following triple integral in cylindrical polar coordinates. 

$$
{∭}_{R}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V
$$

1. ${\int }_{0}^{2 \pi}{\int }_{0}^{2}{\int }_{r}^{11}r^{2}\,dz\,\text{d}r\,\text{d}\theta $
2. ${\int }_{0}^{2 \pi}{\int }_{0}^{2}{\int }_{r}^{11}r\,dz\,\text{d}r\,\text{d}\theta $
3. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{2}}{\int }_{r}^{11}r^{2}\,dz\,\text{d}r\,\text{d}\theta $
4. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{2}}{\int }_{r}^{11}r\,dz\,\text{d}r\,\text{d}\theta $
5. ${\int }_{0}^{2 \pi}{\int }_{0}^{\sqrt{2}}{\int }_{r}^{11}r^{3}\,dz\,\text{d}r\,\text{d}\theta $

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129267/images/projection-c6dcd4f675a4674a4fd15f0d488c569b4fdac8a01cb263d61dbb53499528ef77.png)

The region $R$ is a right vertical cylinder of radius $\sqrt{2}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=\sqrt{{x}^{2}+{y}^{2}}=r,$ and

- bounded above by $z=11.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le \sqrt{2},\,0\le \theta <2\pi ,\,r\le z\le 11\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}V & ={∭}_{Δ}\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\cdot r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}r\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{\sqrt{2}}{\int }_{r}^{11}{r}^{2}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$