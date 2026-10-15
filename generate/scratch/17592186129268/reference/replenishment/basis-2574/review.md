If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,(x-2)^{2}+{y}^{2}\le 4,y\ge 0,\,4\le z\le 7\},
$$

then express the triple integral

$$
{∭}_{R}x^{2} + y^{2}\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{2 \cos{\left(\theta \right)}}{\int }_{4}^{7}r^{3}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{7}^{4}r^{3}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{4}^{7}r^{2}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{4}^{7}r^{4}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{4}^{7}r^{3}\,dz\,\text{d}r\,\text{d}\theta $


Worked solution

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/d2/d2b3344b7b910f5685d4fd81b75a600608af6b008778ff608cb084edb5a92da9.png)

The region $R$ is one-half of a right vertical cylinder of radius $2$ whose axis passes through the point $(2,0)$ in the $xy$-plane, and is

- bounded below by $z=4,$ and

- bounded above by $z=7.$

With that in mind, let's now write the $(x-2)^{2}+{y}^{2}=4$ in polar coordinates:

$$
\begin{aligned}(x-2)^{2}+{y}^{2} & =4 \\ (r\operatorname{cos}⁡\theta-2)^{2}+(r\operatorname{sin}⁡\theta)^{2} & =4 \\ {r}^{2}{cos}^{2}⁡\theta -4r\operatorname{cos}⁡\theta+4+{r}^{2}{sin}^{2}⁡\theta & =4 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-4r\operatorname{cos}⁡\theta & =0 \\ {r}^{2}-4r\operatorname{cos}⁡\theta & =0 \\ r(r-4\operatorname{cos}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=4 \cos{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 4 \cos{\left(\theta \right)},\,0\le \theta \le \frac{\pi}{2},\,4\le z\le 7\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}x^{2} + y^{2}\,\text{d}V & ={∭}_{Δ}((r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta)^{2})\cdot r\,dz\,dr\,d\theta \\  & ={∭}_{Δ}{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\cdot r\,dz\,dr\,d\theta \\  & ={\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{4}^{7}r^{3}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,(x-4)^{2}+{y}^{2}\le 16,y\ge 0,\,1\le z\le 2\},
$$

then express the triple integral

$$
{∭}_{R}x^{2} + y^{2}\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{8 \cos{\left(\theta \right)}}{\int }_{1}^{2}r^{3}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{8 \cos{\left(\theta \right)}}{\int }_{1}^{2}r^{4}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{8 \cos{\left(\theta \right)}}{\int }_{1}^{2}r^{2}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{8 \cos{\left(\theta \right)}}{\int }_{2}^{1}r^{3}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{1}^{2}r^{3}\,dz\,\text{d}r\,\text{d}\theta $


Worked solution

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/80/80a919b28ae7ed559b06b34bd8512859794a7d6550970b56347e2deb653bf76d.png)

The region $R$ is one-half of a right vertical cylinder of radius $4$ whose axis passes through the point $(4,0)$ in the $xy$-plane, and is

- bounded below by $z=1,$ and

- bounded above by $z=2.$

With that in mind, let's now write the $(x-4)^{2}+{y}^{2}=16$ in polar coordinates:

$$
\begin{aligned}(x-4)^{2}+{y}^{2} & =16 \\ (r\operatorname{cos}⁡\theta-4)^{2}+(r\operatorname{sin}⁡\theta)^{2} & =16 \\ {r}^{2}{cos}^{2}⁡\theta -8r\operatorname{cos}⁡\theta+16+{r}^{2}{sin}^{2}⁡\theta & =16 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-8r\operatorname{cos}⁡\theta & =0 \\ {r}^{2}-8r\operatorname{cos}⁡\theta & =0 \\ r(r-8\operatorname{cos}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=8 \cos{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 8 \cos{\left(\theta \right)},\,0\le \theta \le \frac{\pi}{2},\,1\le z\le 2\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}x^{2} + y^{2}\,\text{d}V & ={∭}_{Δ}((r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta)^{2})\cdot r\,dz\,dr\,d\theta \\  & ={∭}_{Δ}{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\cdot r\,dz\,dr\,d\theta \\  & ={\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{8 \cos{\left(\theta \right)}}{\int }_{1}^{2}r^{3}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,(x-4)^{2}+{y}^{2}\le 16,y\ge 0,\,4\le z\le 7\},
$$

then express the triple integral

$$
{∭}_{R}x^{2} + y^{2}\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{8 \cos{\left(\theta \right)}}{\int }_{4}^{7}r^{4}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{4}^{7}r^{3}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{8 \cos{\left(\theta \right)}}{\int }_{4}^{7}r^{3}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{8 \cos{\left(\theta \right)}}{\int }_{7}^{4}r^{3}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{8 \cos{\left(\theta \right)}}{\int }_{4}^{7}r^{2}\,dz\,\text{d}r\,\text{d}\theta $


Worked solution

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/80/80a919b28ae7ed559b06b34bd8512859794a7d6550970b56347e2deb653bf76d.png)

The region $R$ is one-half of a right vertical cylinder of radius $4$ whose axis passes through the point $(4,0)$ in the $xy$-plane, and is

- bounded below by $z=4,$ and

- bounded above by $z=7.$

With that in mind, let's now write the $(x-4)^{2}+{y}^{2}=16$ in polar coordinates:

$$
\begin{aligned}(x-4)^{2}+{y}^{2} & =16 \\ (r\operatorname{cos}⁡\theta-4)^{2}+(r\operatorname{sin}⁡\theta)^{2} & =16 \\ {r}^{2}{cos}^{2}⁡\theta -8r\operatorname{cos}⁡\theta+16+{r}^{2}{sin}^{2}⁡\theta & =16 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-8r\operatorname{cos}⁡\theta & =0 \\ {r}^{2}-8r\operatorname{cos}⁡\theta & =0 \\ r(r-8\operatorname{cos}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=8 \cos{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 8 \cos{\left(\theta \right)},\,0\le \theta \le \frac{\pi}{2},\,4\le z\le 7\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}x^{2} + y^{2}\,\text{d}V & ={∭}_{Δ}((r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta)^{2})\cdot r\,dz\,dr\,d\theta \\  & ={∭}_{Δ}{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\cdot r\,dz\,dr\,d\theta \\  & ={\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{8 \cos{\left(\theta \right)}}{\int }_{4}^{7}r^{3}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,(x-2)^{2}+{y}^{2}\le 4,y\ge 0,\,0\le z\le 1\},
$$

then express the triple integral

$$
{∭}_{R}x^{2} + y^{2}\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{0}^{1}r^{4}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{1}^{0}r^{3}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{2 \cos{\left(\theta \right)}}{\int }_{0}^{1}r^{3}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{0}^{1}r^{3}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{0}^{1}r^{2}\,dz\,\text{d}r\,\text{d}\theta $


Worked solution

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/d2/d2b3344b7b910f5685d4fd81b75a600608af6b008778ff608cb084edb5a92da9.png)

The region $R$ is one-half of a right vertical cylinder of radius $2$ whose axis passes through the point $(2,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=1.$

With that in mind, let's now write the $(x-2)^{2}+{y}^{2}=4$ in polar coordinates:

$$
\begin{aligned}(x-2)^{2}+{y}^{2} & =4 \\ (r\operatorname{cos}⁡\theta-2)^{2}+(r\operatorname{sin}⁡\theta)^{2} & =4 \\ {r}^{2}{cos}^{2}⁡\theta -4r\operatorname{cos}⁡\theta+4+{r}^{2}{sin}^{2}⁡\theta & =4 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-4r\operatorname{cos}⁡\theta & =0 \\ {r}^{2}-4r\operatorname{cos}⁡\theta & =0 \\ r(r-4\operatorname{cos}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=4 \cos{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 4 \cos{\left(\theta \right)},\,0\le \theta \le \frac{\pi}{2},\,0\le z\le 1\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}x^{2} + y^{2}\,\text{d}V & ={∭}_{Δ}((r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta)^{2})\cdot r\,dz\,dr\,d\theta \\  & ={∭}_{Δ}{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\cdot r\,dz\,dr\,d\theta \\  & ={\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{0}^{1}r^{3}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,(x-2)^{2}+{y}^{2}\le 4,y\ge 0,\,4\le z\le 6\},
$$

then express the triple integral

$$
{∭}_{R}x^{2} + y^{2}\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{4}^{6}r^{4}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{6}^{4}r^{3}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{2 \cos{\left(\theta \right)}}{\int }_{4}^{6}r^{3}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{4}^{6}r^{3}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{4}^{6}r^{2}\,dz\,\text{d}r\,\text{d}\theta $


Worked solution

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/d2/d2b3344b7b910f5685d4fd81b75a600608af6b008778ff608cb084edb5a92da9.png)

The region $R$ is one-half of a right vertical cylinder of radius $2$ whose axis passes through the point $(2,0)$ in the $xy$-plane, and is

- bounded below by $z=4,$ and

- bounded above by $z=6.$

With that in mind, let's now write the $(x-2)^{2}+{y}^{2}=4$ in polar coordinates:

$$
\begin{aligned}(x-2)^{2}+{y}^{2} & =4 \\ (r\operatorname{cos}⁡\theta-2)^{2}+(r\operatorname{sin}⁡\theta)^{2} & =4 \\ {r}^{2}{cos}^{2}⁡\theta -4r\operatorname{cos}⁡\theta+4+{r}^{2}{sin}^{2}⁡\theta & =4 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-4r\operatorname{cos}⁡\theta & =0 \\ {r}^{2}-4r\operatorname{cos}⁡\theta & =0 \\ r(r-4\operatorname{cos}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=4 \cos{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 4 \cos{\left(\theta \right)},\,0\le \theta \le \frac{\pi}{2},\,4\le z\le 6\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}x^{2} + y^{2}\,\text{d}V & ={∭}_{Δ}((r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta)^{2})\cdot r\,dz\,dr\,d\theta \\  & ={∭}_{Δ}{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\cdot r\,dz\,dr\,d\theta \\  & ={\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{4}^{6}r^{3}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,{x}^{2}+(y+2)^{2}\le 4,\,0\le z\le x^{2} + y^{2} + 5\},
$$

then express the triple integral

$$
{∭}_{R}x y\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{\pi}^{2 \pi}{\int }_{0}^{- 4 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 5}r^{3} \cos^{2}{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi}^{2 \pi}{\int }_{0}^{- 4 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 5}r^{3} \sin^{2}{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi}^{2 \pi}{\int }_{0}^{- 4 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 5}r^{2} \cos^{2}{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi}^{2 \pi}{\int }_{0}^{- 4 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 5}r^{3} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi}^{2 \pi}{\int }_{0}^{- 4 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 5}r^{2} \sin^{2}{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $


Worked solution

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/ce/cee08173667c9577f4c7aab8cac5386434f2e1ecab8836150ebe8066d1cbaa68.png)

The region $R$ is a right vertical cylinder of radius $2$ whose axis passes through the point $(0,-2)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=x^{2} + y^{2} + 5=r^{2} + 5.$

With that in mind, let's write the equation ${x}^{2}+(y+2)^{2}=4$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+(y+2)^{2} & =4 \\ (r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta+2)^{2} & =4 \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta +4r\operatorname{sin}⁡\theta+4 & =4 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+4r\operatorname{sin}⁡\theta & =0 \\ {r}^{2}+4r\operatorname{sin}⁡\theta & =0 \\ r(r+4\operatorname{sin}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire circle, we must have $r=- 4 \sin{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le - 4 \sin{\left(\theta \right)},\,\pi\le \theta \le 2 \pi,\,0\le z\le r^{2} + 5\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}x y\,\text{d}V & ={∭}_{Δ}(r\operatorname{cos}⁡\theta)(r\operatorname{sin}⁡\theta)\cdot r\,dz\,dr\,d\theta \\  & ={\int }_{\pi}^{2 \pi}{\int }_{0}^{- 4 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 5}r^{3} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,{x}^{2}+(y+4)^{2}\le 16,\,0\le z\le x^{2} + y^{2} + 2\},
$$

then express the triple integral

$$
{∭}_{R}x y\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{\pi}^{2 \pi}{\int }_{0}^{- 8 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 2}r^{2} \cos^{2}{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi}^{2 \pi}{\int }_{0}^{- 8 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 2}r^{2} \sin^{2}{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi}^{2 \pi}{\int }_{0}^{- 8 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 2}r^{3} \sin^{2}{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi}^{2 \pi}{\int }_{0}^{- 8 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 2}r^{3} \cos^{2}{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi}^{2 \pi}{\int }_{0}^{- 8 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 2}r^{3} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $


Worked solution

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/5e/5ed28b1e7b49276cdb59da432056597e5992b8c4015ac8e9384f6bfe3f1fb7ba.png)

The region $R$ is a right vertical cylinder of radius $4$ whose axis passes through the point $(0,-4)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=x^{2} + y^{2} + 2=r^{2} + 2.$

With that in mind, let's write the equation ${x}^{2}+(y+4)^{2}=16$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+(y+4)^{2} & =16 \\ (r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta+4)^{2} & =16 \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta +8r\operatorname{sin}⁡\theta+16 & =16 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+8r\operatorname{sin}⁡\theta & =0 \\ {r}^{2}+8r\operatorname{sin}⁡\theta & =0 \\ r(r+8\operatorname{sin}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire circle, we must have $r=- 8 \sin{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le - 8 \sin{\left(\theta \right)},\,\pi\le \theta \le 2 \pi,\,0\le z\le r^{2} + 2\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}x y\,\text{d}V & ={∭}_{Δ}(r\operatorname{cos}⁡\theta)(r\operatorname{sin}⁡\theta)\cdot r\,dz\,dr\,d\theta \\  & ={\int }_{\pi}^{2 \pi}{\int }_{0}^{- 8 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 2}r^{3} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,(x+4)^{2}+{y}^{2}\le 16,\,-6\le z\le x + 5\},
$$

then express the triple integral

$$
{∭}_{R}\frac{1}{\sqrt{x^{2} + y^{2} + 2}}\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 8 \cos{\left(\theta \right)}}{\int }_{-6}^{r \cos{\left(\theta \right)} + 5}\frac{r^{2}}{\sqrt{r^{2} + 2}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 8 \cos{\left(\theta \right)}}{\int }_{-6}^{r \cos{\left(\theta \right)} + 5}\frac{r}{\sqrt{r^{2} + 2}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 4 \cos{\left(\theta \right)}}{\int }_{-6}^{r \cos{\left(\theta \right)} + 5}\frac{r}{\sqrt{r^{2} + 2}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 8 \cos{\left(\theta \right)}}{\int }_{r \cos{\left(\theta \right)} + 5}^{-6}\frac{r}{\sqrt{r^{2} + 2}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 8 \cos{\left(\theta \right)}}{\int }_{-6}^{r \cos{\left(\theta \right)} + 5}\frac{1}{\sqrt{r^{2} + 2}}\,dz\,\text{d}r\,\text{d}\theta $


Worked solution

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/8b/8b16f7e69a4ce84b0b7c4597defd9e9f55593e50623f344f001d24518d59c483.png)

The region $R$ is a right vertical cylinder of radius $4$ whose axis passes through the point $(-4,0)$ in the $xy$-plane, and is

- bounded below by $z=-6,$ and

- bounded above by $z=x + 5=r \cos{\left(\theta \right)} + 5.$

With that in mind, let's write the equation $(x+4)^{2}+{y}^{2}=16$ in polar coordinates:

$$
\begin{aligned}(x+4)^{2}+{y}^{2} & =16 \\ (r\operatorname{cos}⁡\theta+4)^{2}+(r\operatorname{sin}⁡\theta)^{2} & =16 \\ {r}^{2}{cos}^{2}⁡\theta +8r\operatorname{cos}⁡\theta+16+{r}^{2}{sin}^{2}⁡\theta & =16 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+8r\operatorname{cos}⁡\theta & =0 \\ {r}^{2}+8r\operatorname{cos}⁡\theta & =0 \\ r(r+8\operatorname{cos}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire circle, we must have $r=- 8 \cos{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le - 8 \cos{\left(\theta \right)},\,\frac{\pi}{2}\le \theta \le \frac{3 \pi}{2},\,-6\le z\le r \cos{\left(\theta \right)} + 5\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\frac{1}{\sqrt{x^{2} + y^{2} + 2}}\,\text{d}V & ={∭}_{Δ}\frac{1}{\sqrt{(r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta)^{2}+2}}\cdot r\,dz\,dr\,d\theta \\  & ={∭}_{Δ}\frac{r}{\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+2}}\,dz\,dr\,d\theta \\  & ={\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 8 \cos{\left(\theta \right)}}{\int }_{-6}^{r \cos{\left(\theta \right)} + 5}\frac{r}{\sqrt{r^{2} + 2}}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,(x+2)^{2}+{y}^{2}\le 4,\,-4\le z\le x + 1\},
$$

then express the triple integral

$$
{∭}_{R}\frac{1}{\sqrt{x^{2} + y^{2} + 2}}\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 4 \cos{\left(\theta \right)}}{\int }_{-4}^{r \cos{\left(\theta \right)} + 1}\frac{r^{2}}{\sqrt{r^{2} + 2}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 4 \cos{\left(\theta \right)}}{\int }_{r \cos{\left(\theta \right)} + 1}^{-4}\frac{r}{\sqrt{r^{2} + 2}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 2 \cos{\left(\theta \right)}}{\int }_{-4}^{r \cos{\left(\theta \right)} + 1}\frac{r}{\sqrt{r^{2} + 2}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 4 \cos{\left(\theta \right)}}{\int }_{-4}^{r \cos{\left(\theta \right)} + 1}\frac{1}{\sqrt{r^{2} + 2}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 4 \cos{\left(\theta \right)}}{\int }_{-4}^{r \cos{\left(\theta \right)} + 1}\frac{r}{\sqrt{r^{2} + 2}}\,dz\,\text{d}r\,\text{d}\theta $


Worked solution

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/f8/f830c1469527c615d213ffcd11e472083c77d7e5fbc8c1577a85244fb5739fc4.png)

The region $R$ is a right vertical cylinder of radius $2$ whose axis passes through the point $(-2,0)$ in the $xy$-plane, and is

- bounded below by $z=-4,$ and

- bounded above by $z=x + 1=r \cos{\left(\theta \right)} + 1.$

With that in mind, let's write the equation $(x+2)^{2}+{y}^{2}=4$ in polar coordinates:

$$
\begin{aligned}(x+2)^{2}+{y}^{2} & =4 \\ (r\operatorname{cos}⁡\theta+2)^{2}+(r\operatorname{sin}⁡\theta)^{2} & =4 \\ {r}^{2}{cos}^{2}⁡\theta +4r\operatorname{cos}⁡\theta+4+{r}^{2}{sin}^{2}⁡\theta & =4 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+4r\operatorname{cos}⁡\theta & =0 \\ {r}^{2}+4r\operatorname{cos}⁡\theta & =0 \\ r(r+4\operatorname{cos}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire circle, we must have $r=- 4 \cos{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le - 4 \cos{\left(\theta \right)},\,\frac{\pi}{2}\le \theta \le \frac{3 \pi}{2},\,-4\le z\le r \cos{\left(\theta \right)} + 1\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\frac{1}{\sqrt{x^{2} + y^{2} + 2}}\,\text{d}V & ={∭}_{Δ}\frac{1}{\sqrt{(r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta)^{2}+2}}\cdot r\,dz\,dr\,d\theta \\  & ={∭}_{Δ}\frac{r}{\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+2}}\,dz\,dr\,d\theta \\  & ={\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 4 \cos{\left(\theta \right)}}{\int }_{-4}^{r \cos{\left(\theta \right)} + 1}\frac{r}{\sqrt{r^{2} + 2}}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,(x+2)^{2}+{y}^{2}\le 4,\,-1\le z\le x + 5\},
$$

then express the triple integral

$$
{∭}_{R}\frac{1}{\sqrt{x^{2} + y^{2} + 2}}\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 4 \cos{\left(\theta \right)}}{\int }_{-1}^{r \cos{\left(\theta \right)} + 5}\frac{r^{2}}{\sqrt{r^{2} + 2}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 4 \cos{\left(\theta \right)}}{\int }_{-1}^{r \cos{\left(\theta \right)} + 5}\frac{1}{\sqrt{r^{2} + 2}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 2 \cos{\left(\theta \right)}}{\int }_{-1}^{r \cos{\left(\theta \right)} + 5}\frac{r}{\sqrt{r^{2} + 2}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 4 \cos{\left(\theta \right)}}{\int }_{-1}^{r \cos{\left(\theta \right)} + 5}\frac{r}{\sqrt{r^{2} + 2}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 4 \cos{\left(\theta \right)}}{\int }_{r \cos{\left(\theta \right)} + 5}^{-1}\frac{r}{\sqrt{r^{2} + 2}}\,dz\,\text{d}r\,\text{d}\theta $


Worked solution

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/f8/f830c1469527c615d213ffcd11e472083c77d7e5fbc8c1577a85244fb5739fc4.png)

The region $R$ is a right vertical cylinder of radius $2$ whose axis passes through the point $(-2,0)$ in the $xy$-plane, and is

- bounded below by $z=-1,$ and

- bounded above by $z=x + 5=r \cos{\left(\theta \right)} + 5.$

With that in mind, let's write the equation $(x+2)^{2}+{y}^{2}=4$ in polar coordinates:

$$
\begin{aligned}(x+2)^{2}+{y}^{2} & =4 \\ (r\operatorname{cos}⁡\theta+2)^{2}+(r\operatorname{sin}⁡\theta)^{2} & =4 \\ {r}^{2}{cos}^{2}⁡\theta +4r\operatorname{cos}⁡\theta+4+{r}^{2}{sin}^{2}⁡\theta & =4 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+4r\operatorname{cos}⁡\theta & =0 \\ {r}^{2}+4r\operatorname{cos}⁡\theta & =0 \\ r(r+4\operatorname{cos}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire circle, we must have $r=- 4 \cos{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le - 4 \cos{\left(\theta \right)},\,\frac{\pi}{2}\le \theta \le \frac{3 \pi}{2},\,-1\le z\le r \cos{\left(\theta \right)} + 5\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\frac{1}{\sqrt{x^{2} + y^{2} + 2}}\,\text{d}V & ={∭}_{Δ}\frac{1}{\sqrt{(r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta)^{2}+2}}\cdot r\,dz\,dr\,d\theta \\  & ={∭}_{Δ}\frac{r}{\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+2}}\,dz\,dr\,d\theta \\  & ={\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 4 \cos{\left(\theta \right)}}{\int }_{-1}^{r \cos{\left(\theta \right)} + 5}\frac{r}{\sqrt{r^{2} + 2}}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,(x-2)^{2}+{y}^{2}\le 4,y\le 0,\,y\le z\le 10\},
$$

then express the triple integral

$$
{∭}_{R}\frac{1}{\sqrt{z + 5}}\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{2 \cos{\left(\theta \right)}}{\int }_{r \sin{\left(\theta \right)}}^{10}\frac{r}{\sqrt{z + 5}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{10}^{r \sin{\left(\theta \right)}}\frac{r}{\sqrt{z + 5}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{r \sin{\left(\theta \right)}}^{10}\frac{1}{\sqrt{z + 5}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{r \sin{\left(\theta \right)}}^{10}\frac{r^{2}}{\sqrt{z + 5}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{r \sin{\left(\theta \right)}}^{10}\frac{r}{\sqrt{z + 5}}\,dz\,\text{d}r\,\text{d}\theta $


Worked solution

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/d8/d8d5ba5f13ed464fa4e2b53fb2cd4fbdab92b3de371d3f7b535aeac8d0adb6d5.png)

The region $R$ is one-half of a right vertical cylinder of radius $2$ whose axis passes through the point $(2,0)$ in the $xy$-plane, and is

- bounded below by $z=y=r \sin{\left(\theta \right)},$ and

- bounded above by $z=10.$

With that in mind, let's now write the $(x-2)^{2}+{y}^{2}=4$ in polar coordinates:

$$
\begin{aligned}(x-2)^{2}+{y}^{2} & =4 \\ (r\operatorname{cos}⁡\theta-2)^{2}+(r\operatorname{sin}⁡\theta)^{2} & =4 \\ {r}^{2}{cos}^{2}⁡\theta -4r\operatorname{cos}⁡\theta+4+{r}^{2}{sin}^{2}⁡\theta & =4 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-4r\operatorname{cos}⁡\theta & =0 \\ {r}^{2}-4r\operatorname{cos}⁡\theta & =0 \\ r(r-4\operatorname{cos}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=4 \cos{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 4 \cos{\left(\theta \right)},\,\frac{3 \pi}{2}\le \theta \le 2 \pi,\,r \sin{\left(\theta \right)}\le z\le 10\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\frac{1}{\sqrt{z + 5}}\,\text{d}V & ={∭}_{Δ}\frac{1}{\sqrt{z + 5}}\cdot r\,dz\,dr\,d\theta \\  & ={\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{r \sin{\left(\theta \right)}}^{10}\frac{r}{\sqrt{z + 5}}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,(x-4)^{2}+{y}^{2}\le 16,y\le 0,\,y\le z\le 4\},
$$

then express the triple integral

$$
{∭}_{R}\frac{1}{\sqrt{z + 5}}\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{8 \cos{\left(\theta \right)}}{\int }_{r \sin{\left(\theta \right)}}^{4}\frac{r}{\sqrt{z + 5}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{8 \cos{\left(\theta \right)}}{\int }_{r \sin{\left(\theta \right)}}^{4}\frac{r^{2}}{\sqrt{z + 5}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{8 \cos{\left(\theta \right)}}{\int }_{r \sin{\left(\theta \right)}}^{4}\frac{1}{\sqrt{z + 5}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{8 \cos{\left(\theta \right)}}{\int }_{4}^{r \sin{\left(\theta \right)}}\frac{r}{\sqrt{z + 5}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{4 \cos{\left(\theta \right)}}{\int }_{r \sin{\left(\theta \right)}}^{4}\frac{r}{\sqrt{z + 5}}\,dz\,\text{d}r\,\text{d}\theta $


Worked solution

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/51/510a5ecd48459be9372c1a797d00cc78a167b7ebc0563063e4f1a1e187e32bd0.png)

The region $R$ is one-half of a right vertical cylinder of radius $4$ whose axis passes through the point $(4,0)$ in the $xy$-plane, and is

- bounded below by $z=y=r \sin{\left(\theta \right)},$ and

- bounded above by $z=4.$

With that in mind, let's now write the $(x-4)^{2}+{y}^{2}=16$ in polar coordinates:

$$
\begin{aligned}(x-4)^{2}+{y}^{2} & =16 \\ (r\operatorname{cos}⁡\theta-4)^{2}+(r\operatorname{sin}⁡\theta)^{2} & =16 \\ {r}^{2}{cos}^{2}⁡\theta -8r\operatorname{cos}⁡\theta+16+{r}^{2}{sin}^{2}⁡\theta & =16 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-8r\operatorname{cos}⁡\theta & =0 \\ {r}^{2}-8r\operatorname{cos}⁡\theta & =0 \\ r(r-8\operatorname{cos}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=8 \cos{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 8 \cos{\left(\theta \right)},\,\frac{3 \pi}{2}\le \theta \le 2 \pi,\,r \sin{\left(\theta \right)}\le z\le 4\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\frac{1}{\sqrt{z + 5}}\,\text{d}V & ={∭}_{Δ}\frac{1}{\sqrt{z + 5}}\cdot r\,dz\,dr\,d\theta \\  & ={\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{8 \cos{\left(\theta \right)}}{\int }_{r \sin{\left(\theta \right)}}^{4}\frac{r}{\sqrt{z + 5}}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,{x}^{2}+(y-4)^{2}\le 16,x\le 0,\,-5\le z\le \sqrt{- x^{2} - y^{2} + 81}\},
$$

then express the triple integral

$$
{∭}_{R}2 x y\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{8 \sin{\left(\theta \right)}}{\int }_{-5}^{\sqrt{81 - r^{2}}}2 r^{4} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{4 \sin{\left(\theta \right)}}{\int }_{-5}^{\sqrt{81 - r^{2}}}2 r^{3} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{8 \sin{\left(\theta \right)}}{\int }_{-5}^{\sqrt{81 - r^{2}}}2 r^{3} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{8 \sin{\left(\theta \right)}}{\int }_{\sqrt{81 - r^{2}}}^{-5}2 r^{3} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{8 \sin{\left(\theta \right)}}{\int }_{-5}^{\sqrt{81 - r^{2}}}2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $


Worked solution

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/57/5764f328a614ddaa96abd28a4568c4cd7dfcf0988033d3122bdce0e1e52b7bc5.png)

The region $R$ is one-half of a right vertical cylinder of radius $4$ whose axis passes through the point $(0,4)$ in the $xy$-plane, and is

- bounded below by $z=-5,$ and

- bounded above by $z=\sqrt{- x^{2} - y^{2} + 81}=\sqrt{81 - r^{2}}.$

With that in mind, let's now write the ${x}^{2}+(y-4)^{2}=16$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+(y-4)^{2} & =16 \\ (r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta-4)^{2} & =16 \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -8r\operatorname{sin}⁡\theta+16 & =16 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-8r\operatorname{sin}⁡\theta & =0 \\ {r}^{2}-8r\operatorname{sin}⁡\theta & =0 \\ r(r-8\operatorname{sin}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=8 \sin{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 8 \sin{\left(\theta \right)},\,\frac{\pi}{2}\le \theta \le \pi,\,-5\le z\le \sqrt{81 - r^{2}}\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}2 x y\,\text{d}V & ={∭}_{Δ}2(r\operatorname{cos}⁡\theta)(r\operatorname{sin}⁡\theta)\cdot r\,dz\,dr\,d\theta \\  & ={\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{8 \sin{\left(\theta \right)}}{\int }_{-5}^{\sqrt{81 - r^{2}}}{r}^{3}\operatorname{sin}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,{x}^{2}+(y-4)^{2}\le 16,x\ge 0,\,-2\le z\le x\},
$$

then express the triple integral

$$
{∭}_{R}\sqrt{x^{2} + y^{2} + 1}\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{8 \sin{\left(\theta \right)}}{\int }_{-2}^{r \cos{\left(\theta \right)}}\sqrt{r^{2} + 1}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{8 \sin{\left(\theta \right)}}{\int }_{-2}^{r \sin{\left(\theta \right)}}r \sqrt{r^{2} + 1}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\pi}{\int }_{0}^{8 \sin{\left(\theta \right)}}{\int }_{-2}^{r \cos{\left(\theta \right)}}r \sqrt{r^{2} + 1}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{8 \sin{\left(\theta \right)}}{\int }_{-2}^{r \cos{\left(\theta \right)}}r \sqrt{r^{2} + 1}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\pi}{\int }_{0}^{8 \sin{\left(\theta \right)}}{\int }_{-2}^{r \sin{\left(\theta \right)}}\sqrt{r^{2} + 1}\,dz\,\text{d}r\,\text{d}\theta $


Worked solution

We will use the change of variables formula in the form

$$
{∭}_{R}f(x,y,z)\,dV={∭}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta ,z)\,r\,dz\,dr\,d\theta .
$$

If $(r,\theta ,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta ,\,z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](images/26/262fdb09ab8f6ee5de1a31cec2d238cb633ae2d5dfa2e99d80ed58d4cb849ec5.png)

The region $R$ is one-half of a right vertical cylinder of radius $4$ whose axis passes through the point $(0,4)$ in the $xy$-plane, and is

- bounded below by $z=-2,$ and

- bounded above by $z=x=r \cos{\left(\theta \right)}.$

With that in mind, let's now write the ${x}^{2}+(y-4)^{2}=16$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+(y-4)^{2} & =16 \\ (r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta-4)^{2} & =16 \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -8r\operatorname{sin}⁡\theta+16 & =16 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-8r\operatorname{sin}⁡\theta & =0 \\ {r}^{2}-8r\operatorname{sin}⁡\theta & =0 \\ r(r-8\operatorname{sin}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=8 \sin{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 8 \sin{\left(\theta \right)},\,0\le \theta \le \frac{\pi}{2},\,-2\le z\le r \cos{\left(\theta \right)}\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}\sqrt{x^{2} + y^{2} + 1}\,\text{d}V & ={∭}_{Δ}\sqrt{(r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta)^{2}+1}\cdot r\,dz\,dr\,d\theta \\  & ={∭}_{Δ}\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+1}\cdot r\,dz\,dr\,d\theta \\  & ={\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{8 \sin{\left(\theta \right)}}{\int }_{-2}^{r \cos{\left(\theta \right)}}r \sqrt{r^{2} + 1}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$