## Original raw evidence q-161521

If the solid region $R$ is given by
$R = {(x, y, z): x^{2} + (y + 3)^{2} \le 9, 0 \le z \le 2 + x^{2} + y^{2}}$,
then $∭_(R)xydV =$

- $\displaystyle \int_{π}^{2π}\displaystyle \int_{0}^{6 cos ⁡ θ}\displaystyle \int_{0}^{2 + r 2}r 3 cos ⁡ θ sin ⁡ θdzdrdθ$

- $\displaystyle \int_{π}^{2π}\displaystyle \int_{0}^{3}\displaystyle \int_{0}^{2 + r}r 3 cos ⁡ θ sin ⁡ θdzdrdθ$

- $\displaystyle \int_{π}^{2π}\displaystyle \int_{0}^{-6 sin ⁡ θ}\displaystyle \int_{0}^{2 + r 2}r 3 cos ⁡ θ sin ⁡ θdzdrdθ$

- $\displaystyle \int_{π}^{2π}\displaystyle \int_{0}^{-6 sin ⁡ θ}\displaystyle \int_{0}^{2 + r 2}r 2 cos ⁡ θ sin ⁡ θdzdrdθ$

- $\displaystyle \int_{π}^{2π}\displaystyle \int_{0}^{3}\displaystyle \int_{0}^{2 + r}r 2 cos ⁡ θ sin ⁡ θdzdrdθ$

---

## Generated lower_xy variant 1

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,{x}^{2}+(y+3)^{2}\le 9,\,0\le z\le x^{2} + y^{2} + 5\},
$$

then express the triple integral

$$
{∭}_{R}x y\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{\pi}^{2 \pi}{\int }_{0}^{- 6 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 5}r^{2} \sin^{2}{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi}^{2 \pi}{\int }_{0}^{- 6 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 5}r^{3} \cos^{2}{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi}^{2 \pi}{\int }_{0}^{- 6 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 5}r^{3} \sin^{2}{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi}^{2 \pi}{\int }_{0}^{- 6 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 5}r^{3} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi}^{2 \pi}{\int }_{0}^{- 6 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 5}r^{2} \cos^{2}{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $


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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129268/images/projection-b73a1576d72d672ffdad03d6de7ebfa317456cb61fefc14ec615fd7251277fb1.png)

The region $R$ is a right vertical cylinder of radius $3$ whose axis passes through the point $(0,-3)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=x^{2} + y^{2} + 5=r^{2} + 5.$

With that in mind, let's write the equation ${x}^{2}+(y+3)^{2}=9$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+(y+3)^{2} & =9 \\ (r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta+3)^{2} & =9 \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta +6r\operatorname{sin}⁡\theta+9 & =9 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+6r\operatorname{sin}⁡\theta & =0 \\ {r}^{2}+6r\operatorname{sin}⁡\theta & =0 \\ r(r+6\operatorname{sin}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire circle, we must have $r=- 6 \sin{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le - 6 \sin{\left(\theta \right)},\,\pi\le \theta \le 2 \pi,\,0\le z\le r^{2} + 5\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}x y\,\text{d}V & ={∭}_{Δ}(r\operatorname{cos}⁡\theta)(r\operatorname{sin}⁡\theta)\cdot r\,dz\,dr\,d\theta \\  & ={\int }_{\pi}^{2 \pi}{\int }_{0}^{- 6 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 5}r^{3} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## Generated lower_xy variant 2

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,{x}^{2}+(y+3)^{2}\le 9,\,0\le z\le x^{2} + y^{2} + 1\},
$$

then express the triple integral

$$
{∭}_{R}x y\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{\pi}^{2 \pi}{\int }_{0}^{- 6 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 1}r^{2} \cos^{2}{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi}^{2 \pi}{\int }_{0}^{- 6 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 1}r^{3} \sin^{2}{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi}^{2 \pi}{\int }_{0}^{- 6 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 1}r^{2} \sin^{2}{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi}^{2 \pi}{\int }_{0}^{- 6 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 1}r^{3} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi}^{2 \pi}{\int }_{0}^{- 6 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 1}r^{3} \cos^{2}{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $


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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129268/images/projection-b73a1576d72d672ffdad03d6de7ebfa317456cb61fefc14ec615fd7251277fb1.png)

The region $R$ is a right vertical cylinder of radius $3$ whose axis passes through the point $(0,-3)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=x^{2} + y^{2} + 1=r^{2} + 1.$

With that in mind, let's write the equation ${x}^{2}+(y+3)^{2}=9$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+(y+3)^{2} & =9 \\ (r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta+3)^{2} & =9 \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta +6r\operatorname{sin}⁡\theta+9 & =9 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+6r\operatorname{sin}⁡\theta & =0 \\ {r}^{2}+6r\operatorname{sin}⁡\theta & =0 \\ r(r+6\operatorname{sin}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire circle, we must have $r=- 6 \sin{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le - 6 \sin{\left(\theta \right)},\,\pi\le \theta \le 2 \pi,\,0\le z\le r^{2} + 1\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}x y\,\text{d}V & ={∭}_{Δ}(r\operatorname{cos}⁡\theta)(r\operatorname{sin}⁡\theta)\cdot r\,dz\,dr\,d\theta \\  & ={\int }_{\pi}^{2 \pi}{\int }_{0}^{- 6 \sin{\left(\theta \right)}}{\int }_{0}^{r^{2} + 1}r^{3} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## Original raw evidence q-161523

If the solid region $R$ is given by
$R = {(x, y, z): (x - 1)^{2} + y^{2} \le 1, y \ge 0, 1 \le z \le 2}$,
then $∭_(R)x^{2} + y^{2}dV =$

- $\displaystyle \int_{0}^{π}\displaystyle \int_{0}^{-cos ⁡ θ}\displaystyle \int_{1}^{2}r 3dzdrdθ$

- $\displaystyle \int_{0}^{π / 2}\displaystyle \int_{0}^{cos ⁡ θ}\displaystyle \int_{1}^{2}r 2dzdrdθ$

- $\displaystyle \int_{0}^{π}\displaystyle \int_{0}^{2 cos ⁡ θ}\displaystyle \int_{1}^{2}r 2dzdrdθ$

- $\displaystyle \int_{0}^{π / 2}\displaystyle \int_{0}^{-2 sin ⁡ θ}\displaystyle \int_{1}^{2}r 3dzdrdθ$

- $\displaystyle \int_{0}^{π / 2}\displaystyle \int_{0}^{2 cos ⁡ θ}\displaystyle \int_{1}^{2}r 3dzdrdθ$

---

## Generated upper_square variant 1

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,(x-3)^{2}+{y}^{2}\le 9,y\ge 0,\,4\le z\le 9\},
$$

then express the triple integral

$$
{∭}_{R}x^{2} + y^{2}\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{6 \cos{\left(\theta \right)}}{\int }_{4}^{9}r^{2}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{3 \cos{\left(\theta \right)}}{\int }_{4}^{9}r^{3}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{6 \cos{\left(\theta \right)}}{\int }_{9}^{4}r^{3}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{6 \cos{\left(\theta \right)}}{\int }_{4}^{9}r^{4}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{6 \cos{\left(\theta \right)}}{\int }_{4}^{9}r^{3}\,dz\,\text{d}r\,\text{d}\theta $


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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129268/images/projection-f9195c163a4ce95c96d12c9471a56a5a3ac7e6cc927614c282635127474d96c3.png)

The region $R$ is one-half of a right vertical cylinder of radius $3$ whose axis passes through the point $(3,0)$ in the $xy$-plane, and is

- bounded below by $z=4,$ and

- bounded above by $z=9.$

With that in mind, let's now write the $(x-3)^{2}+{y}^{2}=9$ in polar coordinates:

$$
\begin{aligned}(x-3)^{2}+{y}^{2} & =9 \\ (r\operatorname{cos}⁡\theta-3)^{2}+(r\operatorname{sin}⁡\theta)^{2} & =9 \\ {r}^{2}{cos}^{2}⁡\theta -6r\operatorname{cos}⁡\theta+9+{r}^{2}{sin}^{2}⁡\theta & =9 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-6r\operatorname{cos}⁡\theta & =0 \\ {r}^{2}-6r\operatorname{cos}⁡\theta & =0 \\ r(r-6\operatorname{cos}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=6 \cos{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 6 \cos{\left(\theta \right)},\,0\le \theta \le \frac{\pi}{2},\,4\le z\le 9\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}x^{2} + y^{2}\,\text{d}V & ={∭}_{Δ}((r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta)^{2})\cdot r\,dz\,dr\,d\theta \\  & ={∭}_{Δ}{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\cdot r\,dz\,dr\,d\theta \\  & ={\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{6 \cos{\left(\theta \right)}}{\int }_{4}^{9}r^{3}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## Generated upper_square variant 2

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,(x-3)^{2}+{y}^{2}\le 9,y\ge 0,\,0\le z\le 4\},
$$

then express the triple integral

$$
{∭}_{R}x^{2} + y^{2}\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{3 \cos{\left(\theta \right)}}{\int }_{0}^{4}r^{3}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{6 \cos{\left(\theta \right)}}{\int }_{0}^{4}r^{2}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{6 \cos{\left(\theta \right)}}{\int }_{4}^{0}r^{3}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{6 \cos{\left(\theta \right)}}{\int }_{0}^{4}r^{4}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{6 \cos{\left(\theta \right)}}{\int }_{0}^{4}r^{3}\,dz\,\text{d}r\,\text{d}\theta $


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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129268/images/projection-f9195c163a4ce95c96d12c9471a56a5a3ac7e6cc927614c282635127474d96c3.png)

The region $R$ is one-half of a right vertical cylinder of radius $3$ whose axis passes through the point $(3,0)$ in the $xy$-plane, and is

- bounded below by $z=0,$ and

- bounded above by $z=4.$

With that in mind, let's now write the $(x-3)^{2}+{y}^{2}=9$ in polar coordinates:

$$
\begin{aligned}(x-3)^{2}+{y}^{2} & =9 \\ (r\operatorname{cos}⁡\theta-3)^{2}+(r\operatorname{sin}⁡\theta)^{2} & =9 \\ {r}^{2}{cos}^{2}⁡\theta -6r\operatorname{cos}⁡\theta+9+{r}^{2}{sin}^{2}⁡\theta & =9 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-6r\operatorname{cos}⁡\theta & =0 \\ {r}^{2}-6r\operatorname{cos}⁡\theta & =0 \\ r(r-6\operatorname{cos}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=6 \cos{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 6 \cos{\left(\theta \right)},\,0\le \theta \le \frac{\pi}{2},\,0\le z\le 4\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}x^{2} + y^{2}\,\text{d}V & ={∭}_{Δ}((r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta)^{2})\cdot r\,dz\,dr\,d\theta \\  & ={∭}_{Δ}{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\cdot r\,dz\,dr\,d\theta \\  & ={\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{6 \cos{\left(\theta \right)}}{\int }_{0}^{4}r^{3}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## Original raw evidence q-161630

If the solid region $R$ is given by 

$$
R={(x,y,z)\,:\,(x+3)^{2}+{y}^{2}\le 9,\,-8\le z\le x+2},
$$

then ${∭}_{R}\frac{1}{\sqrt{{x}^{2}+{y}^{2}+1}}\,\text{d}V=$

- ${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{-6\operatorname{sin}⁡\theta }{\int }_{-8}^{r\operatorname{cos}⁡\theta +2}\frac{r}{\sqrt{{r}^{2}+1}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{-6\operatorname{sin}⁡\theta }{\int }_{-8}^{r\operatorname{sin}⁡\theta +2}\frac{1}{\sqrt{{r}^{2}+1}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{-6\operatorname{cos}⁡\theta }{\int }_{-8}^{r\operatorname{cos}⁡\theta +2}\frac{1}{\sqrt{{r}^{2}+1}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{-6\operatorname{cos}⁡\theta }{\int }_{-8}^{r\operatorname{cos}⁡\theta +2}\frac{r}{\sqrt{{r}^{2}+1}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{-6\operatorname{cos}⁡\theta }{\int }_{-8}^{r\operatorname{sin}⁡\theta +2}\frac{r}{\sqrt{{r}^{2}+1}}\,dz\,\text{d}r\,\text{d}\theta $


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

![](images/3c/3c03dde21942c60de527ace896bb51ad8070781126d72f5be5e2f6069700736d.png)

The region $R$ is a right vertical cylinder of radius $3$ whose axis passes through the point $(-3,0)$ in the $xy$-plane, and is

- bounded below by $z=-8,$ and

- bounded above by $z=x+2=r\operatorname{cos}⁡\theta +2.$

With that in mind, let's write the equation $(x+3)^{2}+{y}^{2}=9$ in polar coordinates:

$$
\begin{aligned}(x+3)^{2}+{y}^{2} & =9 \\ {(r\operatorname{cos}⁡\theta +3)}^{2}+{(r\operatorname{sin}⁡\theta )}^{2} & =9 \\ {r}^{2}{cos}^{2}⁡\theta +6r\operatorname{cos}⁡\theta +9+{r}^{2}{sin}^{2}⁡\theta  & =9 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+6r\operatorname{cos}⁡\theta  & =0 \\ {r}^{2}+6r\operatorname{cos}⁡\theta  & =0 \\ r(r+6\operatorname{cos}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire circle, we must have $r=-6\operatorname{cos}⁡\theta .$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ={(r,\theta ,z)\,:\,0\le r\le -6\operatorname{cos}⁡\theta ,\,\frac{\pi }{2}\le \theta \le \frac{3\pi }{2},\,-8\le z\le r\operatorname{cos}⁡\theta +2}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\frac{1}{\sqrt{{x}^{2}+{y}^{2}+1}}\,\text{d}V & ={∭}_{Δ}\frac{1}{\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}+1}}\cdot r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}\frac{r}{\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+1}}\,dz\,dr\,d\theta  \\  & ={\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{-6\operatorname{cos}⁡\theta }{\int }_{-8}^{r\operatorname{cos}⁡\theta +2}\frac{r}{\sqrt{{r}^{2}+1}}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## Generated left_inverse variant 1

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,(x+3)^{2}+{y}^{2}\le 9,\,-6\le z\le x + 5\},
$$

then express the triple integral

$$
{∭}_{R}\frac{1}{\sqrt{x^{2} + y^{2} + 1}}\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 6 \cos{\left(\theta \right)}}{\int }_{r \cos{\left(\theta \right)} + 5}^{-6}\frac{r}{\sqrt{r^{2} + 1}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 3 \cos{\left(\theta \right)}}{\int }_{-6}^{r \cos{\left(\theta \right)} + 5}\frac{r}{\sqrt{r^{2} + 1}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 6 \cos{\left(\theta \right)}}{\int }_{-6}^{r \cos{\left(\theta \right)} + 5}\frac{r}{\sqrt{r^{2} + 1}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 6 \cos{\left(\theta \right)}}{\int }_{-6}^{r \cos{\left(\theta \right)} + 5}\frac{1}{\sqrt{r^{2} + 1}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 6 \cos{\left(\theta \right)}}{\int }_{-6}^{r \cos{\left(\theta \right)} + 5}\frac{r^{2}}{\sqrt{r^{2} + 1}}\,dz\,\text{d}r\,\text{d}\theta $


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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129268/images/projection-62c2b9b4de84864ce9ec977a2fd201be0c89dafc5943bcf5389df000a987cf60.png)

The region $R$ is a right vertical cylinder of radius $3$ whose axis passes through the point $(-3,0)$ in the $xy$-plane, and is

- bounded below by $z=-6,$ and

- bounded above by $z=x + 5=r \cos{\left(\theta \right)} + 5.$

With that in mind, let's write the equation $(x+3)^{2}+{y}^{2}=9$ in polar coordinates:

$$
\begin{aligned}(x+3)^{2}+{y}^{2} & =9 \\ (r\operatorname{cos}⁡\theta+3)^{2}+(r\operatorname{sin}⁡\theta)^{2} & =9 \\ {r}^{2}{cos}^{2}⁡\theta +6r\operatorname{cos}⁡\theta+9+{r}^{2}{sin}^{2}⁡\theta & =9 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+6r\operatorname{cos}⁡\theta & =0 \\ {r}^{2}+6r\operatorname{cos}⁡\theta & =0 \\ r(r+6\operatorname{cos}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire circle, we must have $r=- 6 \cos{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le - 6 \cos{\left(\theta \right)},\,\frac{\pi}{2}\le \theta \le \frac{3 \pi}{2},\,-6\le z\le r \cos{\left(\theta \right)} + 5\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\frac{1}{\sqrt{x^{2} + y^{2} + 1}}\,\text{d}V & ={∭}_{Δ}\frac{1}{\sqrt{(r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta)^{2}+1}}\cdot r\,dz\,dr\,d\theta \\  & ={∭}_{Δ}\frac{r}{\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+1}}\,dz\,dr\,d\theta \\  & ={\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 6 \cos{\left(\theta \right)}}{\int }_{-6}^{r \cos{\left(\theta \right)} + 5}\frac{r}{\sqrt{r^{2} + 1}}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## Generated left_inverse variant 2

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,(x+3)^{2}+{y}^{2}\le 9,\,-9\le z\le x + 1\},
$$

then express the triple integral

$$
{∭}_{R}\frac{1}{\sqrt{x^{2} + y^{2} + 1}}\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 3 \cos{\left(\theta \right)}}{\int }_{-9}^{r \cos{\left(\theta \right)} + 1}\frac{r}{\sqrt{r^{2} + 1}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 6 \cos{\left(\theta \right)}}{\int }_{-9}^{r \cos{\left(\theta \right)} + 1}\frac{1}{\sqrt{r^{2} + 1}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 6 \cos{\left(\theta \right)}}{\int }_{-9}^{r \cos{\left(\theta \right)} + 1}\frac{r}{\sqrt{r^{2} + 1}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 6 \cos{\left(\theta \right)}}{\int }_{-9}^{r \cos{\left(\theta \right)} + 1}\frac{r^{2}}{\sqrt{r^{2} + 1}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 6 \cos{\left(\theta \right)}}{\int }_{r \cos{\left(\theta \right)} + 1}^{-9}\frac{r}{\sqrt{r^{2} + 1}}\,dz\,\text{d}r\,\text{d}\theta $


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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129268/images/projection-62c2b9b4de84864ce9ec977a2fd201be0c89dafc5943bcf5389df000a987cf60.png)

The region $R$ is a right vertical cylinder of radius $3$ whose axis passes through the point $(-3,0)$ in the $xy$-plane, and is

- bounded below by $z=-9,$ and

- bounded above by $z=x + 1=r \cos{\left(\theta \right)} + 1.$

With that in mind, let's write the equation $(x+3)^{2}+{y}^{2}=9$ in polar coordinates:

$$
\begin{aligned}(x+3)^{2}+{y}^{2} & =9 \\ (r\operatorname{cos}⁡\theta+3)^{2}+(r\operatorname{sin}⁡\theta)^{2} & =9 \\ {r}^{2}{cos}^{2}⁡\theta +6r\operatorname{cos}⁡\theta+9+{r}^{2}{sin}^{2}⁡\theta & =9 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+6r\operatorname{cos}⁡\theta & =0 \\ {r}^{2}+6r\operatorname{cos}⁡\theta & =0 \\ r(r+6\operatorname{cos}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire circle, we must have $r=- 6 \cos{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le - 6 \cos{\left(\theta \right)},\,\frac{\pi}{2}\le \theta \le \frac{3 \pi}{2},\,-9\le z\le r \cos{\left(\theta \right)} + 1\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\frac{1}{\sqrt{x^{2} + y^{2} + 1}}\,\text{d}V & ={∭}_{Δ}\frac{1}{\sqrt{(r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta)^{2}+1}}\cdot r\,dz\,dr\,d\theta \\  & ={∭}_{Δ}\frac{r}{\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+1}}\,dz\,dr\,d\theta \\  & ={\int }_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}{\int }_{0}^{- 6 \cos{\left(\theta \right)}}{\int }_{-9}^{r \cos{\left(\theta \right)} + 1}\frac{r}{\sqrt{r^{2} + 1}}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## Original raw evidence q-161636

If the solid region $R$ is given by 

$$
R={(x,y,z)\,:\,(x-3)^{2}+{y}^{2}\le 9,\,y\le 0,\,y\le z\le 6},
$$

then ${∭}_{R}\frac{1}{\sqrt{z+1}}\,\text{d}V=$

- ${\int }_{3\pi /2}^{2\pi }{\int }_{0}^{-6\operatorname{sin}⁡\theta }{\int }_{r\operatorname{sin}⁡\theta }^{6}\frac{1}{\sqrt{z+1}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{3\pi /2}^{2\pi }{\int }_{0}^{6\operatorname{cos}⁡\theta }{\int }_{r\operatorname{sin}⁡\theta }^{6}\frac{1}{\sqrt{z+1}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{3\pi /2}^{2\pi }{\int }_{0}^{6\operatorname{cos}⁡\theta }{\int }_{r\operatorname{sin}⁡\theta }^{6}\frac{r}{\sqrt{z+1}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{3\pi /2}^{2\pi }{\int }_{0}^{-6\operatorname{sin}⁡\theta }{\int }_{r\operatorname{cos}⁡\theta }^{6}\frac{r}{\sqrt{z+1}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{3\pi /2}^{2\pi }{\int }_{0}^{6\operatorname{cos}⁡\theta }{\int }_{r\operatorname{cos}⁡\theta }^{6}\frac{r}{\sqrt{z+1}}\,dz\,\text{d}r\,\text{d}\theta $


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

![](images/cc/ccc5cab37aed89c0d701ce0195414796211ddc73a498eaaa1ff145a45c42e9fd.png)

The region $R$ is one-half of a right vertical cylinder of radius $3$ whose axis passes through the point $(3,0)$ in the $xy$-plane, and is

- bounded below by $z=y=r\operatorname{sin}⁡\theta ,$ and

- bounded above by $z=6.$

With that in mind, let's now write the $(x-3)^{2}+{y}^{2}=9$ in polar coordinates:

$$
\begin{aligned}(x-3)^{2}+{y}^{2} & =9 \\ (r\operatorname{cos}⁡\theta -3)^{2}+(r\operatorname{sin}⁡\theta )^{2} & =3 \\ {r}^{2}{cos}^{2}⁡\theta -6r\operatorname{cos}⁡\theta +9+{r}^{2}{sin}^{2}⁡\theta  & =9 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-6r\operatorname{cos}⁡\theta  & =0 \\ {r}^{2}-6r\operatorname{cos}⁡\theta  & =0 \\ r(r-6\operatorname{cos}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=6\operatorname{cos}⁡\theta .$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ={(r,\theta ,z)\,:\,0\le r\le 6\operatorname{cos}⁡\theta ,\,\frac{3\pi }{2}\le \theta \le 2\pi ,\,r\operatorname{sin}⁡\theta \le z\le 6}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\frac{1}{\sqrt{z+1}}\,\text{d}V & ={∭}_{Δ}\frac{1}{\sqrt{z+1}}\cdot r\,dz\,dr\,d\theta  \\  & ={\int }_{3\pi /2}^{2\pi }{\int }_{0}^{6\operatorname{cos}⁡\theta }{\int }_{r\operatorname{sin}⁡\theta }^{6}\frac{r}{\sqrt{z+1}}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## Generated lower_zinverse variant 1

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,(x-3)^{2}+{y}^{2}\le 9,y\le 0,\,y\le z\le 9\},
$$

then express the triple integral

$$
{∭}_{R}\frac{1}{\sqrt{z + 8}}\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{6 \cos{\left(\theta \right)}}{\int }_{r \sin{\left(\theta \right)}}^{9}\frac{1}{\sqrt{z + 8}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{3 \cos{\left(\theta \right)}}{\int }_{r \sin{\left(\theta \right)}}^{9}\frac{r}{\sqrt{z + 8}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{6 \cos{\left(\theta \right)}}{\int }_{9}^{r \sin{\left(\theta \right)}}\frac{r}{\sqrt{z + 8}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{6 \cos{\left(\theta \right)}}{\int }_{r \sin{\left(\theta \right)}}^{9}\frac{r^{2}}{\sqrt{z + 8}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{6 \cos{\left(\theta \right)}}{\int }_{r \sin{\left(\theta \right)}}^{9}\frac{r}{\sqrt{z + 8}}\,dz\,\text{d}r\,\text{d}\theta $


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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129268/images/projection-849e9cc8ad5ed06488e3e327e733c700e1d266f8f53e5b152495ab51425447a9.png)

The region $R$ is one-half of a right vertical cylinder of radius $3$ whose axis passes through the point $(3,0)$ in the $xy$-plane, and is

- bounded below by $z=y=r \sin{\left(\theta \right)},$ and

- bounded above by $z=9.$

With that in mind, let's now write the $(x-3)^{2}+{y}^{2}=9$ in polar coordinates:

$$
\begin{aligned}(x-3)^{2}+{y}^{2} & =9 \\ (r\operatorname{cos}⁡\theta-3)^{2}+(r\operatorname{sin}⁡\theta)^{2} & =9 \\ {r}^{2}{cos}^{2}⁡\theta -6r\operatorname{cos}⁡\theta+9+{r}^{2}{sin}^{2}⁡\theta & =9 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-6r\operatorname{cos}⁡\theta & =0 \\ {r}^{2}-6r\operatorname{cos}⁡\theta & =0 \\ r(r-6\operatorname{cos}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=6 \cos{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 6 \cos{\left(\theta \right)},\,\frac{3 \pi}{2}\le \theta \le 2 \pi,\,r \sin{\left(\theta \right)}\le z\le 9\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\frac{1}{\sqrt{z + 8}}\,\text{d}V & ={∭}_{Δ}\frac{1}{\sqrt{z + 8}}\cdot r\,dz\,dr\,d\theta \\  & ={\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{6 \cos{\left(\theta \right)}}{\int }_{r \sin{\left(\theta \right)}}^{9}\frac{r}{\sqrt{z + 8}}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## Generated lower_zinverse variant 2

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,(x-3)^{2}+{y}^{2}\le 9,y\le 0,\,y\le z\le 1\},
$$

then express the triple integral

$$
{∭}_{R}\frac{1}{\sqrt{z + 7}}\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{3 \cos{\left(\theta \right)}}{\int }_{r \sin{\left(\theta \right)}}^{1}\frac{r}{\sqrt{z + 7}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{6 \cos{\left(\theta \right)}}{\int }_{r \sin{\left(\theta \right)}}^{1}\frac{1}{\sqrt{z + 7}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{6 \cos{\left(\theta \right)}}{\int }_{1}^{r \sin{\left(\theta \right)}}\frac{r}{\sqrt{z + 7}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{6 \cos{\left(\theta \right)}}{\int }_{r \sin{\left(\theta \right)}}^{1}\frac{r^{2}}{\sqrt{z + 7}}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{6 \cos{\left(\theta \right)}}{\int }_{r \sin{\left(\theta \right)}}^{1}\frac{r}{\sqrt{z + 7}}\,dz\,\text{d}r\,\text{d}\theta $


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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129268/images/projection-849e9cc8ad5ed06488e3e327e733c700e1d266f8f53e5b152495ab51425447a9.png)

The region $R$ is one-half of a right vertical cylinder of radius $3$ whose axis passes through the point $(3,0)$ in the $xy$-plane, and is

- bounded below by $z=y=r \sin{\left(\theta \right)},$ and

- bounded above by $z=1.$

With that in mind, let's now write the $(x-3)^{2}+{y}^{2}=9$ in polar coordinates:

$$
\begin{aligned}(x-3)^{2}+{y}^{2} & =9 \\ (r\operatorname{cos}⁡\theta-3)^{2}+(r\operatorname{sin}⁡\theta)^{2} & =9 \\ {r}^{2}{cos}^{2}⁡\theta -6r\operatorname{cos}⁡\theta+9+{r}^{2}{sin}^{2}⁡\theta & =9 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-6r\operatorname{cos}⁡\theta & =0 \\ {r}^{2}-6r\operatorname{cos}⁡\theta & =0 \\ r(r-6\operatorname{cos}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=6 \cos{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 6 \cos{\left(\theta \right)},\,\frac{3 \pi}{2}\le \theta \le 2 \pi,\,r \sin{\left(\theta \right)}\le z\le 1\}.
$$

Therefore, using the change of variables formula, we obtain  

$$
\begin{aligned}{∭}_{R}\frac{1}{\sqrt{z + 7}}\,\text{d}V & ={∭}_{Δ}\frac{1}{\sqrt{z + 7}}\cdot r\,dz\,dr\,d\theta \\  & ={\int }_{\frac{3 \pi}{2}}^{2 \pi}{\int }_{0}^{6 \cos{\left(\theta \right)}}{\int }_{r \sin{\left(\theta \right)}}^{1}\frac{r}{\sqrt{z + 7}}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## Original raw evidence q-161633

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,{x}^{2}+(y-2)^{2}\le 4,\,x\le 0,\,-2\le z\le \sqrt{16-({x}^{2}+{y}^{2})}\},
$$

then ${∭}_{R}2xy\,\text{d}V=$

- ${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{-4\operatorname{cos}⁡\theta }{\int }_{-2}^{\sqrt{16-{r}^{2}}}{r}^{2}\operatorname{sin}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi /2}^{\pi }{\int }_{0}^{4\operatorname{sin}⁡\theta }{\int }_{-2}^{\sqrt{16-{r}^{2}}}{r}^{3}\operatorname{sin}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi /2}^{\pi }{\int }_{0}^{4\operatorname{sin}⁡\theta }{\int }_{-2}^{\sqrt{16-{r}^{2}}}{r}^{2}\operatorname{sin}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi /2}^{\pi }{\int }_{0}^{-4\operatorname{cos}⁡\theta }{\int }_{-2}^{\sqrt{16-{r}^{2}}}{r}^{3}\operatorname{sin}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{4\operatorname{sin}⁡\theta }{\int }_{-2}^{\sqrt{16-{r}^{2}}}{r}^{3}\operatorname{sin}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta $


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

![](images/83/831de8cf1d9833f8674a7e4cb69d01098970eefb9cf576c0537fa7be471c8c2c.png)

The region $R$ is one-half of a right vertical cylinder of radius $2$ whose axis passes through the point $(0,2)$ in the $xy$-plane, and is

- bounded below by $z=-2,$ and

- bounded above by $z=\sqrt{16-({x}^{2}+{y}^{2})}=\sqrt{16-{r}^{2}}.$

With that in mind, let's now write the ${x}^{2}+(y-2)^{2}=4$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+(y-2)^{2} & =4 \\ (r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta -2)^{2} & =4 \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -4r\operatorname{sin}⁡\theta +4 & =4 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-4r\operatorname{sin}⁡\theta  & =0 \\ {r}^{2}-4r\operatorname{sin}⁡\theta  & =0 \\ r(r-4\operatorname{sin}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=4\operatorname{sin}⁡\theta .$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 4\operatorname{sin}⁡\theta ,\,\frac{\pi }{2}\le \theta \le \pi ,\,-2\le z\le \sqrt{16-{r}^{2}}\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}2xy\,\text{d}V & ={∭}_{Δ}2(r\operatorname{cos}⁡\theta )(r\operatorname{sin}⁡\theta )\cdot r\,dz\,dr\,d\theta  \\  & ={\int }_{\pi /2}^{\pi }{\int }_{0}^{4\operatorname{sin}⁡\theta }{\int }_{-2}^{\sqrt{16-{r}^{2}}}{r}^{3}\operatorname{sin}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## Generated left_xy_sphere variant 1

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,{x}^{2}+(y-3)^{2}\le 9,x\le 0,\,-5\le z\le \sqrt{- x^{2} - y^{2} + 64}\},
$$

then express the triple integral

$$
{∭}_{R}2 x y\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{-5}^{\sqrt{64 - r^{2}}}2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{3 \sin{\left(\theta \right)}}{\int }_{-5}^{\sqrt{64 - r^{2}}}2 r^{3} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{\sqrt{64 - r^{2}}}^{-5}2 r^{3} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{-5}^{\sqrt{64 - r^{2}}}2 r^{4} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{-5}^{\sqrt{64 - r^{2}}}2 r^{3} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $


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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129268/images/projection-2ea234dba2bc115feb915e814812519e5a46e86ecbe97c05ae9f133a0211dbfc.png)

The region $R$ is one-half of a right vertical cylinder of radius $3$ whose axis passes through the point $(0,3)$ in the $xy$-plane, and is

- bounded below by $z=-5,$ and

- bounded above by $z=\sqrt{- x^{2} - y^{2} + 64}=\sqrt{64 - r^{2}}.$

With that in mind, let's now write the ${x}^{2}+(y-3)^{2}=9$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+(y-3)^{2} & =9 \\ (r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta-3)^{2} & =9 \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -6r\operatorname{sin}⁡\theta+9 & =9 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-6r\operatorname{sin}⁡\theta & =0 \\ {r}^{2}-6r\operatorname{sin}⁡\theta & =0 \\ r(r-6\operatorname{sin}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=6 \sin{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 6 \sin{\left(\theta \right)},\,\frac{\pi}{2}\le \theta \le \pi,\,-5\le z\le \sqrt{64 - r^{2}}\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}2 x y\,\text{d}V & ={∭}_{Δ}2(r\operatorname{cos}⁡\theta)(r\operatorname{sin}⁡\theta)\cdot r\,dz\,dr\,d\theta \\  & ={\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{-5}^{\sqrt{64 - r^{2}}}{r}^{3}\operatorname{sin}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## Generated left_xy_sphere variant 2

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,{x}^{2}+(y-3)^{2}\le 9,x\le 0,\,-1\le z\le \sqrt{- x^{2} - y^{2} + 49}\},
$$

then express the triple integral

$$
{∭}_{R}2 x y\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{3 \sin{\left(\theta \right)}}{\int }_{-1}^{\sqrt{49 - r^{2}}}2 r^{3} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{-1}^{\sqrt{49 - r^{2}}}2 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{\sqrt{49 - r^{2}}}^{-1}2 r^{3} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{-1}^{\sqrt{49 - r^{2}}}2 r^{4} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{-1}^{\sqrt{49 - r^{2}}}2 r^{3} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,dz\,\text{d}r\,\text{d}\theta $


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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129268/images/projection-2ea234dba2bc115feb915e814812519e5a46e86ecbe97c05ae9f133a0211dbfc.png)

The region $R$ is one-half of a right vertical cylinder of radius $3$ whose axis passes through the point $(0,3)$ in the $xy$-plane, and is

- bounded below by $z=-1,$ and

- bounded above by $z=\sqrt{- x^{2} - y^{2} + 49}=\sqrt{49 - r^{2}}.$

With that in mind, let's now write the ${x}^{2}+(y-3)^{2}=9$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+(y-3)^{2} & =9 \\ (r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta-3)^{2} & =9 \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -6r\operatorname{sin}⁡\theta+9 & =9 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-6r\operatorname{sin}⁡\theta & =0 \\ {r}^{2}-6r\operatorname{sin}⁡\theta & =0 \\ r(r-6\operatorname{sin}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=6 \sin{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 6 \sin{\left(\theta \right)},\,\frac{\pi}{2}\le \theta \le \pi,\,-1\le z\le \sqrt{49 - r^{2}}\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}2 x y\,\text{d}V & ={∭}_{Δ}2(r\operatorname{cos}⁡\theta)(r\operatorname{sin}⁡\theta)\cdot r\,dz\,dr\,d\theta \\  & ={\int }_{\frac{\pi}{2}}^{\pi}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{-1}^{\sqrt{49 - r^{2}}}{r}^{3}\operatorname{sin}⁡2\theta \,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## Original raw evidence q-161637

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,{x}^{2}+(y-4)^{2}\le 16,\,x\ge 0,\,-5\le z\le x\},
$$

then ${∭}_{R}\sqrt{{x}^{2}+{y}^{2}+1}\,\text{d}V=$

- ${\int }_{0}^{\pi /2}{\int }_{0}^{8\operatorname{sin}⁡\theta }{\int }_{-5}^{r\operatorname{sin}⁡\theta }r\sqrt{{r}^{2}+1}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\pi /2}{\int }_{0}^{8\operatorname{sin}⁡\theta }{\int }_{-5}^{r\operatorname{cos}⁡\theta }r\sqrt{{r}^{2}+1}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\pi }{\int }_{0}^{8\operatorname{sin}⁡\theta }{\int }_{-5}^{r\operatorname{sin}⁡\theta }\sqrt{{r}^{2}+1}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\pi }{\int }_{0}^{8\operatorname{sin}⁡\theta }{\int }_{-5}^{r\operatorname{cos}⁡\theta }r\sqrt{{r}^{2}+1}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\pi /2}{\int }_{0}^{8\operatorname{sin}⁡\theta }{\int }_{-5}^{r\operatorname{cos}⁡\theta }\sqrt{{r}^{2}+1}\,dz\,\text{d}r\,\text{d}\theta $


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

![](images/b6/b66b8db18b2f5773addc2d00c02f2f15f4a7ead53323418e63bd50457f74466b.png)

The region $R$ is one-half of a right vertical cylinder of radius $4$ whose axis passes through the point $(0,4)$ in the $xy$-plane, and is

- bounded below by $z=-5,$ and

- bounded above by $z=x=r\operatorname{cos}⁡\theta .$

With that in mind, let's now write the ${x}^{2}+(y-4)^{2}=16$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+(y-4)^{2} & =16 \\ (r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta -4)^{2} & =16 \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -8r\operatorname{sin}⁡\theta +16 & =16 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-8r\operatorname{sin}⁡\theta  & =0 \\ {r}^{2}-8r\operatorname{sin}⁡\theta  & =0 \\ r(r-8\operatorname{sin}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=8\operatorname{sin}⁡\theta .$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 8\operatorname{sin}⁡\theta ,\,0\le \theta \le \frac{\pi }{2},\,-5\le z\le r\operatorname{cos}⁡\theta \}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}\sqrt{{x}^{2}+{y}^{2}+1}\,\text{d}V & ={∭}_{Δ}\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}+1}\cdot r\,dz\,dr\,d\theta  \\  & ={∭}_{Δ}\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+1}\cdot r\,dz\,dr\,d\theta  \\  & ={\int }_{0}^{\pi /2}{\int }_{0}^{8\operatorname{sin}⁡\theta }{\int }_{-5}^{r\operatorname{cos}⁡\theta }r\sqrt{{r}^{2}+1}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## Generated right_radical variant 1

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,{x}^{2}+(y-3)^{2}\le 9,x\ge 0,\,-5\le z\le x\},
$$

then express the triple integral

$$
{∭}_{R}\sqrt{x^{2} + y^{2} + 5}\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{-5}^{r \cos{\left(\theta \right)}}r \sqrt{r^{2} + 5}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{-5}^{r \cos{\left(\theta \right)}}\sqrt{r^{2} + 5}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\pi}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{-5}^{r \cos{\left(\theta \right)}}r \sqrt{r^{2} + 5}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{-5}^{r \sin{\left(\theta \right)}}r \sqrt{r^{2} + 5}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\pi}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{-5}^{r \sin{\left(\theta \right)}}\sqrt{r^{2} + 5}\,dz\,\text{d}r\,\text{d}\theta $


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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129268/images/projection-6ee757ec93b731478ba9a67b4ae38030924b0fdaec7b026a1e0faca5c60fe640.png)

The region $R$ is one-half of a right vertical cylinder of radius $3$ whose axis passes through the point $(0,3)$ in the $xy$-plane, and is

- bounded below by $z=-5,$ and

- bounded above by $z=x=r \cos{\left(\theta \right)}.$

With that in mind, let's now write the ${x}^{2}+(y-3)^{2}=9$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+(y-3)^{2} & =9 \\ (r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta-3)^{2} & =9 \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -6r\operatorname{sin}⁡\theta+9 & =9 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-6r\operatorname{sin}⁡\theta & =0 \\ {r}^{2}-6r\operatorname{sin}⁡\theta & =0 \\ r(r-6\operatorname{sin}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=6 \sin{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 6 \sin{\left(\theta \right)},\,0\le \theta \le \frac{\pi}{2},\,-5\le z\le r \cos{\left(\theta \right)}\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}\sqrt{x^{2} + y^{2} + 5}\,\text{d}V & ={∭}_{Δ}\sqrt{(r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta)^{2}+5}\cdot r\,dz\,dr\,d\theta \\  & ={∭}_{Δ}\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+5}\cdot r\,dz\,dr\,d\theta \\  & ={\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{-5}^{r \cos{\left(\theta \right)}}r \sqrt{r^{2} + 5}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

---

## Generated right_radical variant 2

If the solid region $R$ is given by 

$$
R=\{(x,y,z)\,:\,{x}^{2}+(y-3)^{2}\le 9,x\ge 0,\,-1\le z\le x\},
$$

then express the triple integral

$$
{∭}_{R}\sqrt{x^{2} + y^{2} + 4}\,\text{d}V
$$

as an equivalent integral in cylindrical polar coordinates.

{{selection}}

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{-1}^{r \cos{\left(\theta \right)}}\sqrt{r^{2} + 4}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{-1}^{r \cos{\left(\theta \right)}}r \sqrt{r^{2} + 4}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\pi}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{-1}^{r \cos{\left(\theta \right)}}r \sqrt{r^{2} + 4}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{-1}^{r \sin{\left(\theta \right)}}r \sqrt{r^{2} + 4}\,dz\,\text{d}r\,\text{d}\theta $

- ${\int }_{0}^{\pi}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{-1}^{r \sin{\left(\theta \right)}}\sqrt{r^{2} + 4}\,dz\,\text{d}r\,\text{d}\theta $


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

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129268/images/projection-6ee757ec93b731478ba9a67b4ae38030924b0fdaec7b026a1e0faca5c60fe640.png)

The region $R$ is one-half of a right vertical cylinder of radius $3$ whose axis passes through the point $(0,3)$ in the $xy$-plane, and is

- bounded below by $z=-1,$ and

- bounded above by $z=x=r \cos{\left(\theta \right)}.$

With that in mind, let's now write the ${x}^{2}+(y-3)^{2}=9$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+(y-3)^{2} & =9 \\ (r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta-3)^{2} & =9 \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -6r\operatorname{sin}⁡\theta+9 & =9 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-6r\operatorname{sin}⁡\theta & =0 \\ {r}^{2}-6r\operatorname{sin}⁡\theta & =0 \\ r(r-6\operatorname{sin}⁡\theta) & =0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=6 \sin{\left(\theta \right)}.$

As a result, in cylindrical polar coordinates, our region can be expressed as 

$$
Δ=\{(r,\theta ,z)\,:\,0\le r\le 6 \sin{\left(\theta \right)},\,0\le \theta \le \frac{\pi}{2},\,-1\le z\le r \cos{\left(\theta \right)}\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}{∭}_{R}\sqrt{x^{2} + y^{2} + 4}\,\text{d}V & ={∭}_{Δ}\sqrt{(r\operatorname{cos}⁡\theta)^{2}+(r\operatorname{sin}⁡\theta)^{2}+4}\cdot r\,dz\,dr\,d\theta \\  & ={∭}_{Δ}\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+4}\cdot r\,dz\,dr\,d\theta \\  & ={\int }_{0}^{\frac{\pi}{2}}{\int }_{0}^{6 \sin{\left(\theta \right)}}{\int }_{-1}^{r \cos{\left(\theta \right)}}r \sqrt{r^{2} + 4}\,dz\,\text{d}r\,\text{d}\theta .\end{aligned}
$$