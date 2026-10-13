# Source and generated review

All nine originals, all observed banks and two labeled authored variants per template (18 variants, each level represented). Original source mathematical errors remain visible below and in public observed_raw evidence replay. Normal teaching uses supported corrections.

## Original q-38140

Integrate the function $f(x,y)=2x+y$ over the portion of the disk of radius $2$ centered at the origin, where $y\ge 0.$

- $8$
- $\frac{8}{3}$
- $\frac{3}{4}$
- $2$
- $\frac{16}{3}$ **correct**

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](/media/jake/SSD/EDB/math/images/b5/b5ba69ab02aa13e201b7b9113f6a36e705ad19e6412499504afc4f239459a8f3.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 2,\,0\le \theta \le \pi \}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}(2x+y)\,\text{d}A & ={∬}_{Δ}(2r\operatorname{cos}⁡\theta +r\operatorname{sin}⁡\theta )\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{0}^{\pi }{\int }_{0}^{2}{r}^{2}(2\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{\pi }(2\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta ){\int }_{0}^{2}{r}^{2}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{\pi }(2\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )\,{[\frac{{r}^{3}}{3}]}_{0}^{2}\,\text{d}\theta  \\  & ={\int }_{0}^{\pi }(2\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )(\frac{{2}^{3}}{3}-0)\text{d}\theta  \\  & =\frac{8}{3}{\int }_{0}^{\pi }(2\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )\,\text{d}\theta  \\  & =\frac{8}{3}[2\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta ]_{0}^{\pi } \\  & =\frac{8}{3}((2\operatorname{sin}⁡(\pi )-\operatorname{cos}⁡(\pi ))-(2\operatorname{sin}⁡(0)-\operatorname{cos}⁡(0))) \\  & =\frac{8}{3}(1+1) \\  & =\frac{16}{3}.\end{aligned}
$$

### Public observed_raw replay upper_linear

Parameters: `{'R': 2, 'a': 2, 'b': 1}`. Historical mathematical errors are deliberately retained, with balanced normalized TeX.

Integrate the function $f(x,y)=2 x + y$ over the portion of the disk of radius $2$ centered at the origin, where $y\ge0.$

- $2$
- $\frac{8}{3}$
- $\frac{3}{4}$
- $\frac{16}{3}$ **correct**
- $8$

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, let's sketch our region $D:$

![]( /home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/e8d6b416bb108196ad1c.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 2,\ 0\le\theta\le \pi\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}\iint_D 2 x + y\,\mathrm{d}A &=\iint_\Delta (2r\cos\theta+1r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\int_{0}^{\pi}\int_0^{2}r^{2}(2\cos\theta+1\sin\theta)\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{\pi}(2\cos\theta+1\sin\theta)\int_0^{2}r^2\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{\pi}(2\cos\theta+1\sin\theta)\left[\frac{r^3}{3}\right]_0^{2}\,\mathrm{d}\theta\\&=\int_{0}^{\pi}(2\cos\theta+1\sin\theta)(\frac{2^3}{3}-0)\,\mathrm{d}\theta\\&=\frac{8}{3}\int_{0}^{\pi}(2\cos\theta+1\sin\theta)\,\mathrm{d}\theta\\&=\frac{8}{3}\left[2\sin\theta-1\cos\theta\right]_{0}^{\pi}\\&=\frac{8}{3}((2\sin(\pi)-1\cos(\pi))-(2\sin(0)-1\cos(0)))\\&=\frac{8}{3}((1)-(-1))\\&=\frac{16}{3}\end{aligned}
$$

### Authored variant upper_linear / moderate

Parameters: `{'R': 4, 'a': 7, 'b': 1}`; complete authored profile; metadata is not learner content.

Integrate the function $f(x,y)=7 x + y$ over the portion of the disk of radius $4$ centered at the origin, where $y\ge0.$

- $\frac{128}{3}$ **correct**
- $0$
- $- \frac{128}{3}$
- $16$
- $\frac{896}{3}$

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, let's sketch our region $D:$

![]( /home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/e0582376cd252ab40f7a.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 4,\ 0\le\theta\le \pi\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}\iint_D 7 x + y\,\mathrm{d}A &=\iint_\Delta (7r\cos\theta+1r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\int_{0}^{\pi}\int_0^{4}r^{2}(7\cos\theta+1\sin\theta)\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{\pi}(7\cos\theta+1\sin\theta)\int_0^{4}r^2\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{\pi}(7\cos\theta+1\sin\theta)\left[\frac{r^3}{3}\right]_0^{4}\,\mathrm{d}\theta\\&=\int_{0}^{\pi}(7\cos\theta+1\sin\theta)(\frac{4^3}{3}-0)\,\mathrm{d}\theta\\&=\frac{64}{3}\int_{0}^{\pi}(7\cos\theta+1\sin\theta)\,\mathrm{d}\theta\\&=\frac{64}{3}\left[7\sin\theta-1\cos\theta\right]_{0}^{\pi}\\&=\frac{64}{3}((7\sin(\pi)-1\cos(\pi))-(7\sin(0)-1\cos(0)))\\&=\frac{64}{3}((0-(-1))-(0-(1)))\\&=\frac{128}{3}\end{aligned}
$$

### Authored variant upper_linear / moderate

Parameters: `{'R': 2, 'a': 2, 'b': 5}`; complete authored profile; metadata is not learner content.

Integrate the function $f(x,y)=2 x + 5 y$ over the portion of the disk of radius $2$ centered at the origin, where $y\ge0.$

- $0$
- $\frac{32}{3}$
- $- \frac{80}{3}$
- $20$
- $\frac{80}{3}$ **correct**

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, let's sketch our region $D:$

![]( /home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/e8d6b416bb108196ad1c.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 2,\ 0\le\theta\le \pi\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}\iint_D 2 x + 5 y\,\mathrm{d}A &=\iint_\Delta (2r\cos\theta+5r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\int_{0}^{\pi}\int_0^{2}r^{2}(2\cos\theta+5\sin\theta)\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{\pi}(2\cos\theta+5\sin\theta)\int_0^{2}r^2\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{\pi}(2\cos\theta+5\sin\theta)\left[\frac{r^3}{3}\right]_0^{2}\,\mathrm{d}\theta\\&=\int_{0}^{\pi}(2\cos\theta+5\sin\theta)(\frac{2^3}{3}-0)\,\mathrm{d}\theta\\&=\frac{8}{3}\int_{0}^{\pi}(2\cos\theta+5\sin\theta)\,\mathrm{d}\theta\\&=\frac{8}{3}\left[2\sin\theta-5\cos\theta\right]_{0}^{\pi}\\&=\frac{8}{3}((2\sin(\pi)-5\cos(\pi))-(2\sin(0)-5\cos(0)))\\&=\frac{8}{3}((0-(-5))-(0-(5)))\\&=\frac{80}{3}\end{aligned}
$$

## Original q-83968

![](/media/jake/SSD/EDB/math/images/fd/fd1a5a140c3a2d430312d6f6ceeb21d6b7282119c8ec53365553ff845d8c64d5.png)

Evaluate the double integral ${∬}_{D}x\sqrt{{x}^{2}+{y}^{2}}\,\text{d}A,$ where the region $D$ is the semicircle shown above.

- $\frac{1}{20}$ **correct**
- $\frac{1}{15}$
- $\frac{1}{10}$
- $\frac{1}{5}$
- $\frac{1}{4}$

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, notice that the region $D$ represents a portion of the disk of radius $\frac{1}{2}$ centered at 
$(0,-\frac{1}{2}).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the $x=\sqrt{-{y}^{2}-y}$ in polar coordinates:

$$
\begin{aligned}x & =\sqrt{-{y}^{2}-y} \\ {x}^{2} & =-{y}^{2}-y \\ {x}^{2}+{y}^{2} & =-y \\ (r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2} & =-r\operatorname{sin}⁡\theta  \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta ) & =-r\operatorname{sin}⁡\theta  \\ {r}^{2} & =-r\operatorname{sin}⁡\theta  \\ {r}^{2}+r\operatorname{sin}⁡\theta  & =0 \\ r(r+\operatorname{sin}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=-\operatorname{sin}⁡\theta .$

Therefore, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le -\operatorname{sin}⁡\theta ,\,-\frac{\pi }{2}\le \theta \le 0\}.
$$

Therefore, we obtain

$$
\begin{aligned}{∬}_{D}x\sqrt{{x}^{2}+{y}^{2}}\,\text{d}A & ={∬}_{Δ}(r\operatorname{cos}⁡\theta )\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{-\pi /2}^{0}\operatorname{cos}⁡\theta {\int }_{0}^{-\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{-\pi /2}^{0}\operatorname{cos}⁡\theta [\frac{{r}^{4}}{4}]_{0}^{-\operatorname{sin}⁡\theta }\,\text{d}\theta  \\  & =\frac{1}{4}{\int }_{-\pi /2}^{0}\operatorname{cos}⁡\theta ((-\operatorname{sin}⁡\theta )^{4}-{0}^{4})\,\text{d}\theta  \\  & =\frac{1}{4}{\int }_{-\pi /2}^{0}\operatorname{cos}⁡\theta {sin}^{4}⁡\theta \,\text{d}\theta  \\  & =\frac{1}{4}{[\frac{{sin}^{5}⁡\theta }{5}]}_{-\pi /2}^{0} \\  & =\frac{1}{20}({sin}^{5}⁡0-{sin}^{5}⁡(-\frac{\pi }{2})) \\  & =\frac{1}{20}.\end{aligned}
$$

### Public observed_raw replay lower_sqrt

Parameters: `{'R': 1, 'c': 1}`. Historical mathematical errors are deliberately retained, with balanced normalized TeX.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/cc776b31847dcecdb23a.png)

Evaluate the double integral $\iint_D x \sqrt{x^{2} + y^{2}}\,\mathrm{d}A,$ where the region $D$ is the semicircle shown above.

- $\frac{1}{5}$
- $\frac{1}{15}$
- $\frac{1}{10}$
- $\frac{1}{4}$
- $\frac{1}{20}$ **correct**

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, notice that the region $D$ represents a portion of the disk of radius $\frac{1}{2}$ centered at
$(0,- \frac{1}{2}).$

Cartesian and polar coordinates are connected by the following equations:

$$
\left\{\begin{aligned}x=r\cos\theta\\y=r\sin\theta\end{aligned}\right.
$$

With that in mind, let's now write the $x=\sqrt{-1y-y^2}$ in polar coordinates:

$$
\begin{aligned}x&=\sqrt{-1y-y^2}\\x^2&=-1y-y^2\\x^2+y^2&=-1y\\(r\cos\theta)^2+(r\sin\theta)^2&=-1r\sin\theta\\r^2(\cos^2\theta+\sin^2\theta)&=-1r\sin\theta\\r^2&=-1r\sin\theta\\r^2-(-1)r\sin\theta&=0\\r(r-(-1)\sin\theta)&=0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=- \sin{\left(\theta \right)}$.

Therefore, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le - \sin{\left(\theta \right)},\ - \frac{\pi}{2}\le\theta\le 0\}.
$$

Therefore, we obtain

$$
\begin{aligned}\iint_D x \sqrt{x^{2} + y^{2}}\,\mathrm{d}A &=\iint_\Delta 1(r\cos\theta)\sqrt{(r\cos\theta)^2+(r\sin\theta)^2}r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\int_{- \frac{\pi}{2}}^{0}1\cos\theta\int_0^{- \sin{\left(\theta \right)}}r^3\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{- \frac{\pi}{2}}^{0}1\cos\theta\left[\frac{r^4}{4}\right]_0^{- \sin{\left(\theta \right)}}\,\mathrm{d}\theta\\&=\frac{1}{4}\int_{- \frac{\pi}{2}}^{0}\cos\theta((- \sin{\left(\theta \right)})^4-0^4)\,\mathrm{d}\theta\\&=\frac{1}{4}\int_{- \frac{\pi}{2}}^{0}\cos\theta\sin^4\theta\,\mathrm{d}\theta\\&=\frac{1}{4}\left[\frac{\sin^5\theta}{5}\right]_{- \frac{\pi}{2}}^{0}\\&=\frac{1}{20}(\sin^5(0)-\sin^5(-\frac\pi2))\\&=\frac{1}{20}\end{aligned}
$$

### Authored variant lower_sqrt / hard

Parameters: `{'R': 4, 'c': 7}`; complete authored profile; metadata is not learner content.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/85b3dcb63d350b640875.png)

Evaluate the double integral $\iint_D 7 x \sqrt{x^{2} + y^{2}}\,\mathrm{d}A,$ where the region $D$ is the semicircle shown above.

- $- \frac{448}{5}$
- $\frac{112}{3}$
- $\frac{28}{5}$
- $448$
- $\frac{448}{5}$ **correct**

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, notice that the region $D$ represents a portion of the disk of radius $2$ centered at
$(0,-2).$

Cartesian and polar coordinates are connected by the following equations:

$$
\left\{\begin{aligned}x=r\cos\theta\\y=r\sin\theta\end{aligned}\right.
$$

With that in mind, let's now write the $x=\sqrt{-4y-y^2}$ in polar coordinates:

$$
\begin{aligned}x&=\sqrt{-4y-y^2}\\x^2&=-4y-y^2\\x^2+y^2&=-4y\\(r\cos\theta)^2+(r\sin\theta)^2&=-4r\sin\theta\\r^2(\cos^2\theta+\sin^2\theta)&=-4r\sin\theta\\r^2&=-4r\sin\theta\\r^2-(-4)r\sin\theta&=0\\r(r-(-4)\sin\theta)&=0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=- 4 \sin{\left(\theta \right)}$.

Therefore, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le - 4 \sin{\left(\theta \right)},\ - \frac{\pi}{2}\le\theta\le 0\}.
$$

Therefore, we obtain

$$
\begin{aligned}\iint_D 7 x \sqrt{x^{2} + y^{2}}\,\mathrm{d}A &=\iint_\Delta 7(r\cos\theta)\sqrt{(r\cos\theta)^2+(r\sin\theta)^2}r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\int_{- \frac{\pi}{2}}^{0}7\cos\theta\int_0^{- 4 \sin{\left(\theta \right)}}r^3\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{- \frac{\pi}{2}}^{0}7\cos\theta\left[\frac{r^4}{4}\right]_0^{- 4 \sin{\left(\theta \right)}}\,\mathrm{d}\theta\\&=\frac{7}{4}\int_{- \frac{\pi}{2}}^{0}\cos\theta((- 4 \sin{\left(\theta \right)})^4-0^4)\,\mathrm{d}\theta\\&=448\int_{- \frac{\pi}{2}}^{0}\cos\theta\sin^4\theta\,\mathrm{d}\theta\\&=448\left[\frac{\sin^5\theta}{5}\right]_{- \frac{\pi}{2}}^{0}\\&=\frac{448}{5}(\sin^5(0)-\sin^5(-\frac\pi2))\\&=\frac{448}{5}\end{aligned}
$$

### Authored variant lower_sqrt / hard

Parameters: `{'R': 2, 'c': 2}`; complete authored profile; metadata is not learner content.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/382f8b680c399083987a.png)

Evaluate the double integral $\iint_D 2 x \sqrt{x^{2} + y^{2}}\,\mathrm{d}A,$ where the region $D$ is the semicircle shown above.

- $\frac{1}{10}$
- $- \frac{8}{5}$
- $\frac{4}{3}$
- $\frac{8}{5}$ **correct**
- $8$

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, notice that the region $D$ represents a portion of the disk of radius $1$ centered at
$(0,-1).$

Cartesian and polar coordinates are connected by the following equations:

$$
\left\{\begin{aligned}x=r\cos\theta\\y=r\sin\theta\end{aligned}\right.
$$

With that in mind, let's now write the $x=\sqrt{-2y-y^2}$ in polar coordinates:

$$
\begin{aligned}x&=\sqrt{-2y-y^2}\\x^2&=-2y-y^2\\x^2+y^2&=-2y\\(r\cos\theta)^2+(r\sin\theta)^2&=-2r\sin\theta\\r^2(\cos^2\theta+\sin^2\theta)&=-2r\sin\theta\\r^2&=-2r\sin\theta\\r^2-(-2)r\sin\theta&=0\\r(r-(-2)\sin\theta)&=0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=- 2 \sin{\left(\theta \right)}$.

Therefore, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le - 2 \sin{\left(\theta \right)},\ - \frac{\pi}{2}\le\theta\le 0\}.
$$

Therefore, we obtain

$$
\begin{aligned}\iint_D 2 x \sqrt{x^{2} + y^{2}}\,\mathrm{d}A &=\iint_\Delta 2(r\cos\theta)\sqrt{(r\cos\theta)^2+(r\sin\theta)^2}r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\int_{- \frac{\pi}{2}}^{0}2\cos\theta\int_0^{- 2 \sin{\left(\theta \right)}}r^3\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{- \frac{\pi}{2}}^{0}2\cos\theta\left[\frac{r^4}{4}\right]_0^{- 2 \sin{\left(\theta \right)}}\,\mathrm{d}\theta\\&=\frac{1}{2}\int_{- \frac{\pi}{2}}^{0}\cos\theta((- 2 \sin{\left(\theta \right)})^4-0^4)\,\mathrm{d}\theta\\&=8\int_{- \frac{\pi}{2}}^{0}\cos\theta\sin^4\theta\,\mathrm{d}\theta\\&=8\left[\frac{\sin^5\theta}{5}\right]_{- \frac{\pi}{2}}^{0}\\&=\frac{8}{5}(\sin^5(0)-\sin^5(-\frac\pi2))\\&=\frac{8}{5}\end{aligned}
$$

## Original q-161050

Integrate the function $f(x,y)=15{x}^{2}y$ over the disk of radius $1$ centered at the origin.

- $3$
- $1$
- $\frac{1}{3}$
- $5$
- $0$ **correct**

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](/media/jake/SSD/EDB/math/images/9b/9b54b7a488a1983ba1816fdf5c55e039951eb417102c61963977b2f48b9c8d9e.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ={(r,\theta )\,:\,0\le r\le 1,\,0\le \theta \le 2\pi }.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}12{x}^{2}y\,\text{d}A & ={∬}_{Δ}15({r}^{2}{cos}^{2}⁡\theta \cdot r\operatorname{sin}⁡\theta )\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{1}15{r}^{4}({cos}^{2}⁡\theta \operatorname{sin}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }(3{cos}^{2}⁡\theta \operatorname{sin}⁡\theta ){\int }_{0}^{1}5{r}^{4}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }(3{cos}^{2}⁡\theta \operatorname{sin}⁡\theta )\,{[{r}^{5}]}_{0}^{1}\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }(3{cos}^{2}⁡\theta \operatorname{sin}⁡\theta )(1-0)\text{d}\theta  \\  & ={\int }_{0}^{2\pi }3{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}\theta  \\  & =[-{cos}^{3}⁡\theta ]_{0}^{2\pi } \\  & =-({cos}^{3}⁡(2\pi )-{cos}^{3}⁡(0)) \\  & =-(1-1) \\  & =0.\end{aligned}
$$

### Public observed_raw replay odd_disk

Parameters: `{'R': 1, 'c': 15}`. Historical mathematical errors are deliberately retained, with balanced normalized TeX.

Integrate the function $f(x,y)=15 x^{2} y$ over the disk of radius $1$ centered at the origin.

- $5$
- $1$
- $\frac{1}{3}$
- $0$ **correct**
- $3$

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, let's sketch our region $D:$

![]( /home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/6476e425f63b92968732.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 1,\ 0\le\theta\le 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}\iint_D 12 x^{2} y\,\mathrm{d}A &=\iint_\Delta 15(r^2\cos^2\theta\cdot r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\int_{0}^{2 \pi}\int_0^{1}15r^4\cos^2\theta\sin\theta\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}(3\cos^2\theta\sin\theta)\int_0^{1}5r^4\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}3\cos^2\theta\sin\theta\left[r^5\right]_0^{1}\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}3\cos^2\theta\sin\theta(1-0)\,\mathrm{d}\theta\\&=1\int_{0}^{2 \pi}3\cos^2\theta\sin\theta\,\mathrm{d}\theta\\&=1\left[-1\cos^3\theta\right]_{0}^{2 \pi}\\&=-1\cdot 1(\cos^3(2 \pi)-\cos^3(0))\\&=-1\cdot 1(1-1)\\&=0\end{aligned}
$$

### Authored variant odd_disk / easy

Parameters: `{'R': 4, 'c': 25}`; complete authored profile; metadata is not learner content.

Integrate the function $f(x,y)=25 x^{2} y$ over the disk of radius $4$ centered at the origin.

- $- \frac{5120}{3}$
- $\frac{10240}{3}$
- $\frac{5120}{3}$
- $0$ **correct**
- $\frac{20480}{3}$

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, let's sketch our region $D:$

![]( /home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/23c9891711b5a2bd4c16.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 4,\ 0\le\theta\le 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}\iint_D 25 x^{2} y\,\mathrm{d}A &=\iint_\Delta 25(r^2\cos^2\theta\cdot r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\int_{0}^{2 \pi}\int_0^{4}25r^4\cos^2\theta\sin\theta\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}(5\cos^2\theta\sin\theta)\int_0^{4}5r^4\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}5\cos^2\theta\sin\theta\left[r^5\right]_0^{4}\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}5\cos^2\theta\sin\theta(1024-0)\,\mathrm{d}\theta\\&=1024\int_{0}^{2 \pi}5\cos^2\theta\sin\theta\,\mathrm{d}\theta\\&=1024\left[-\frac{5}{3}\cos^3\theta\right]_{0}^{2 \pi}\\&=-1024\cdot \frac{5}{3}(\cos^3(2 \pi)-\cos^3(0))\\&=-1024\cdot \frac{5}{3}(1-1)\\&=0\end{aligned}
$$

### Authored variant odd_disk / easy

Parameters: `{'R': 2, 'c': 19}`; complete authored profile; metadata is not learner content.

Integrate the function $f(x,y)=19 x^{2} y$ over the disk of radius $2$ centered at the origin.

- $\frac{2432}{15}$
- $\frac{608}{15}$
- $- \frac{608}{15}$
- $\frac{1216}{15}$
- $0$ **correct**

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, let's sketch our region $D:$

![]( /home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/f0a161b130a86212547e.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 2,\ 0\le\theta\le 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}\iint_D 19 x^{2} y\,\mathrm{d}A &=\iint_\Delta 19(r^2\cos^2\theta\cdot r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\int_{0}^{2 \pi}\int_0^{2}19r^4\cos^2\theta\sin\theta\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}(\frac{19}{5}\cos^2\theta\sin\theta)\int_0^{2}5r^4\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}\frac{19}{5}\cos^2\theta\sin\theta\left[r^5\right]_0^{2}\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}\frac{19}{5}\cos^2\theta\sin\theta(32-0)\,\mathrm{d}\theta\\&=32\int_{0}^{2 \pi}\frac{19}{5}\cos^2\theta\sin\theta\,\mathrm{d}\theta\\&=32\left[-\frac{19}{15}\cos^3\theta\right]_{0}^{2 \pi}\\&=-32\cdot \frac{19}{15}(\cos^3(2 \pi)-\cos^3(0))\\&=-32\cdot \frac{19}{15}(1-1)\\&=0\end{aligned}
$$

## Original q-161052

Integrate the function $f(x,y)=4{y}^{2}$ over the disk of radius $3$ centered at the origin.

- $9+4\pi $
- $9\pi $
- $81\pi $ **correct**
- $18+2\pi $
- $27\pi $

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](/media/jake/SSD/EDB/math/images/0a/0a1de805051eff4ea82b4eefb7bb113c724b3d4e7304704831b6294ee4e4d674.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 3,\,0\le \theta \le 2\pi \}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}4{y}^{2}\,\text{d}A & ={∬}_{Δ}4(r\operatorname{sin}⁡\theta )^{2}\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{3}4{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{sin}^{2}⁡\theta {\int }_{0}^{3}4{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{sin}^{2}⁡\theta \,{[{r}^{4}]}_{0}^{3}\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{sin}^{2}⁡\theta (81-0)\text{d}\theta  \\  & =81{\int }_{0}^{2\pi }{sin}^{2}⁡\theta \,\text{d}\theta  \\  & =81{\int }_{0}^{2\pi }\frac{1}{2}(1-\operatorname{cos}⁡2\theta )\,\text{d}\theta  \\  & =\frac{81}{2}{[\theta -\frac{1}{2}\operatorname{sin}⁡2\theta ]}_{0}^{2\pi } \\  & =\frac{81}{2}[(2\pi -0)-\frac{1}{2}(\operatorname{sin}⁡4\pi -\operatorname{sin}⁡0)] \\  & =\frac{81}{2}\cdot 2\pi  \\  & =81\pi .\end{aligned}
$$

### Public observed_raw replay square_y

Parameters: `{'R': 3, 'c': 4}`. Historical mathematical errors are deliberately retained, with balanced normalized TeX.

Integrate the function $f(x,y)=4 y^{2}$ over the disk of radius $3$ centered at the origin.

- $2 \pi + 18$
- $9 \pi$
- $81 \pi$ **correct**
- $27 \pi$
- $9 + 4 \pi$

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, let's sketch our region $D:$

![]( /home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/1b979c6ab4bf17eb05c3.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 3,\ 0\le\theta\le 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}\iint_D 4 y^{2}\,\mathrm{d}A &=\iint_\Delta 4(r\sin\theta)^2r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\int_{0}^{2 \pi}\int_0^{3}4r^3\sin^2\theta\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}\sin^2\theta\int_0^{3}4r^3\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}\sin^2\theta\left[1r^4\right]_0^{3}\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}\sin^2\theta(81-0)\,\mathrm{d}\theta\\&=81\int_{0}^{2 \pi}\sin^2\theta\,\mathrm{d}\theta\\&=81\int_{0}^{2 \pi}\frac12(1-\cos2\theta)\,\mathrm{d}\theta\\&=\frac{81}{2}\left[\theta-\frac12\sin2\theta\right]_{0}^{2 \pi}\\&=\frac{81}{2}[(2 \pi-0)-\frac12(\sin(4\pi)-\sin0)]\\&=\frac{81}{2}\cdot2\pi\\&=81 \pi\end{aligned}
$$

### Authored variant square_y / easy

Parameters: `{'R': 4, 'c': 7}`; complete authored profile; metadata is not learner content.

Integrate the function $f(x,y)=7 y^{2}$ over the disk of radius $4$ centered at the origin.

- $- 448 \pi$
- $\frac{448 \pi}{3}$
- $224 \pi$
- $28 \pi$
- $448 \pi$ **correct**

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, let's sketch our region $D:$

![]( /home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/23c9891711b5a2bd4c16.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 4,\ 0\le\theta\le 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}\iint_D 7 y^{2}\,\mathrm{d}A &=\iint_\Delta 7(r\sin\theta)^2r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\int_{0}^{2 \pi}\int_0^{4}7r^3\sin^2\theta\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}\sin^2\theta\int_0^{4}7r^3\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}\sin^2\theta\left[\frac{7}{4}r^4\right]_0^{4}\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}\sin^2\theta(448-0)\,\mathrm{d}\theta\\&=448\int_{0}^{2 \pi}\sin^2\theta\,\mathrm{d}\theta\\&=448\int_{0}^{2 \pi}\frac12(1-\cos2\theta)\,\mathrm{d}\theta\\&=224\left[\theta-\frac12\sin2\theta\right]_{0}^{2 \pi}\\&=224[(2 \pi-0)-\frac12(\sin(4\pi)-\sin0)]\\&=224\cdot2\pi\\&=448 \pi\end{aligned}
$$

### Authored variant square_y / easy

Parameters: `{'R': 2, 'c': 2}`; complete authored profile; metadata is not learner content.

Integrate the function $f(x,y)=2 y^{2}$ over the disk of radius $2$ centered at the origin.

- $4 \pi$
- $- 8 \pi$
- $\frac{16 \pi}{3}$
- $8 \pi$ **correct**
- $\frac{\pi}{2}$

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, let's sketch our region $D:$

![]( /home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/f0a161b130a86212547e.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 2,\ 0\le\theta\le 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}\iint_D 2 y^{2}\,\mathrm{d}A &=\iint_\Delta 2(r\sin\theta)^2r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\int_{0}^{2 \pi}\int_0^{2}2r^3\sin^2\theta\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}\sin^2\theta\int_0^{2}2r^3\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}\sin^2\theta\left[\frac{1}{2}r^4\right]_0^{2}\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}\sin^2\theta(8-0)\,\mathrm{d}\theta\\&=8\int_{0}^{2 \pi}\sin^2\theta\,\mathrm{d}\theta\\&=8\int_{0}^{2 \pi}\frac12(1-\cos2\theta)\,\mathrm{d}\theta\\&=4\left[\theta-\frac12\sin2\theta\right]_{0}^{2 \pi}\\&=4[(2 \pi-0)-\frac12(\sin(4\pi)-\sin0)]\\&=4\cdot2\pi\\&=8 \pi\end{aligned}
$$

## Original q-161053

Integrate the function $f(x,y)={e}^{{x}^{2}+{y}^{2}}$ over the disk of radius $2$ centered at the origin.

- $2\pi ({e}^{2}-1)$
- ${e}^{2}(2\pi -1)$
- ${\pi }^{2}$
- $2\pi {e}^{4}$
- $\pi ({e}^{4}-1)$ **correct**

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](/media/jake/SSD/EDB/math/images/81/811cfa127ad232e8d5a990998604718a57344d1bd7f43173dc0987631c13db33.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ={(r,\theta )\,:\,0\le r\le 2,\,0\le \theta \le 2\pi }.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}{e}^{{x}^{2}+{y}^{2}}\,\text{d}A & ={∬}_{Δ}{e}^{(r{cos}^{2}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\,r\,\text{d}r\text{d}\theta  \\  & ={∬}_{Δ}{e}^{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,r\,\text{d}r\text{d}\theta  \\  & ={∬}_{Δ}{e}^{{r}^{2}}\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{0}^{2\pi }{\int }_{0}^{2}r{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }\,{[\frac{1}{2}{e}^{{r}^{2}}]}_{0}^{2}\,\text{d}\theta  \\  & ={\int }_{0}^{2\pi }\frac{1}{2}({e}^{4}-1)\text{d}\theta  \\  & =\frac{1}{2}({e}^{4}-1)[\theta ]_{0}^{2\pi } \\  & =\frac{1}{2}({e}^{4}-1)(2\pi -0) \\  & =\pi ({e}^{4}-1).\end{aligned}
$$

### Public observed_raw replay exponential

Parameters: `{'R': 2, 'c': 1}`. Historical mathematical errors are deliberately retained, with balanced normalized TeX.

Integrate the function $f(x,y)=e^{x^{2} + y^{2}}$ over the disk of radius $2$ centered at the origin.

- $2 \pi e^{4}$
- $\left(-1 + 2 \pi\right) e^{2}$
- $\pi^{2}$
- $- \pi \left(1 - e^{4}\right)$ **correct**
- $- 2 \pi \left(1 - e^{2}\right)$

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, let's sketch our region $D:$

![]( /home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/f0a161b130a86212547e.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 2,\ 0\le\theta\le 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}\iint_D e^{x^{2} + y^{2}}\,\mathrm{d}A &=\iint_\Delta 1e^{(r\cos^2\theta)^2+(r\sin\theta)^2}r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\iint_\Delta 1e^{r^2(\cos^2\theta+\sin^2\theta)}r\,\mathrm{d}r\,\mathrm{d}\theta\\&=\iint_\Delta 1e^{r^2}r\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}\int_0^{2}1r e^{r^2}\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}\left[\frac{1}{2}e^{r^2}\right]_0^{2}\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}\frac{1}{2}(e^{4}-1)\,\mathrm{d}\theta\\&=\frac{1}{2}(e^{4}-1)\left[\theta\right]_{0}^{2 \pi}\\&=\frac{1}{2}(e^{4}-1)(2\pi-0)\\&=- \pi \left(1 - e^{4}\right)\end{aligned}
$$

### Authored variant exponential / easy

Parameters: `{'R': 2, 'c': 7}`; complete authored profile; metadata is not learner content.

Integrate the function $f(x,y)=7 e^{x^{2} + y^{2}}$ over the disk of radius $2$ centered at the origin.

- $- 7 \pi \left(1 - e^{4}\right)$ **correct**
- $7 \pi \left(1 - e^{4}\right)$
- $7 \pi e^{4}$
- $- 7 \pi \left(1 - e^{2}\right)$
- $- 14 \pi \left(1 - e^{4}\right)$

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, let's sketch our region $D:$

![]( /home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/f0a161b130a86212547e.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 2,\ 0\le\theta\le 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}\iint_D 7 e^{x^{2} + y^{2}}\,\mathrm{d}A &=\iint_\Delta 7e^{(r\cos\theta)^2+(r\sin\theta)^2}r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\iint_\Delta 7e^{r^2(\cos^2\theta+\sin^2\theta)}r\,\mathrm{d}r\,\mathrm{d}\theta\\&=\iint_\Delta 7e^{r^2}r\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}\int_0^{2}7r e^{r^2}\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}\left[\frac{7}{2}e^{r^2}\right]_0^{2}\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}\frac{7}{2}(e^{4}-1)\,\mathrm{d}\theta\\&=\frac{7}{2}(e^{4}-1)\left[\theta\right]_{0}^{2 \pi}\\&=\frac{7}{2}(e^{4}-1)(2\pi-0)\\&=- 7 \pi \left(1 - e^{4}\right)\end{aligned}
$$

### Authored variant exponential / easy

Parameters: `{'R': 4, 'c': 2}`; complete authored profile; metadata is not learner content.

Integrate the function $f(x,y)=2 e^{x^{2} + y^{2}}$ over the disk of radius $4$ centered at the origin.

- $2 \pi \left(1 - e^{16}\right)$
- $- 4 \pi \left(1 - e^{16}\right)$
- $2 \pi e^{16}$
- $- 2 \pi \left(1 - e^{4}\right)$
- $- 2 \pi \left(1 - e^{16}\right)$ **correct**

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, let's sketch our region $D:$

![]( /home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/23c9891711b5a2bd4c16.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 4,\ 0\le\theta\le 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}\iint_D 2 e^{x^{2} + y^{2}}\,\mathrm{d}A &=\iint_\Delta 2e^{(r\cos\theta)^2+(r\sin\theta)^2}r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\iint_\Delta 2e^{r^2(\cos^2\theta+\sin^2\theta)}r\,\mathrm{d}r\,\mathrm{d}\theta\\&=\iint_\Delta 2e^{r^2}r\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}\int_0^{4}2r e^{r^2}\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}\left[1e^{r^2}\right]_0^{4}\,\mathrm{d}\theta\\&=\int_{0}^{2 \pi}1(e^{16}-1)\,\mathrm{d}\theta\\&=1(e^{16}-1)\left[\theta\right]_{0}^{2 \pi}\\&=1(e^{16}-1)(2\pi-0)\\&=- 2 \pi \left(1 - e^{16}\right)\end{aligned}
$$

## Original q-161054

Integrate the function $f(x,y)=2({x}^{2}+{y}^{2})$ over the disk of radius $3$ centered at the origin

- $27\pi $
- $9\pi -3$
- $81\pi $ **correct**
- $18\pi +2$
- $9\pi $

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](/media/jake/SSD/EDB/math/images/0a/0a1de805051eff4ea82b4eefb7bb113c724b3d4e7304704831b6294ee4e4d674.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ={(r,\theta )\,:\,0\le r\le 3,\,0\le \theta \le 2\pi }.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}2({x}^{2}+{y}^{2})\,\text{d}A & ={∬}_{Δ}2({(r\operatorname{cos}⁡\theta )}^{2}+{(r\operatorname{sin}⁡\theta )}^{2})\,r\,\text{d}r\text{d}\theta  \\  & ={∬}_{Δ}2{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\,r\,\text{d}r\text{d}\theta  \\  & =2{∬}_{Δ}{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & =2{\int }_{0}^{2\pi }{\int }_{0}^{3}{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & =2{\int }_{0}^{2\pi }\,{[\frac{{r}^{4}}{4}]}_{0}^{3}\,\text{d}\theta  \\  & =2{\int }_{0}^{2\pi }(\frac{81}{4}-0)\text{d}\theta  \\  & =\frac{81}{2}{\int }_{0}^{2\pi }\,\text{d}\theta  \\  & =\frac{81}{2}[\theta ]_{0}^{2\pi } \\  & =\frac{81}{2}(2\pi -0) \\  & =81\pi .\end{aligned}
$$

### Public observed_raw replay radial_square

Parameters: `{'R': 3, 'c': 2}`. Historical mathematical errors are deliberately retained, with balanced normalized TeX.

Integrate the function $f(x,y)=2 x^{2} + 2 y^{2}$ over the disk of radius $3$ centered at the origin.

- $2 + 18 \pi$
- $-3 + 9 \pi$
- $81 \pi$ **correct**
- $9 \pi$
- $27 \pi$

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, let's sketch our region $D:$

![]( /home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/1b979c6ab4bf17eb05c3.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 3,\ 0\le\theta\le 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}\iint_D 2 x^{2} + 2 y^{2}\,\mathrm{d}A &=\iint_\Delta 2((r\cos\theta)^2+(r\sin\theta)^2)r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\iint_\Delta 2r^2(\cos^2\theta+\sin^2\theta)r\,\mathrm{d}r\,\mathrm{d}\theta\\&=2\iint_\Delta r^3\,\mathrm{d}r\,\mathrm{d}\theta\\&=2\int_{0}^{2 \pi}\int_0^{3}r^3\,\mathrm{d}r\,\mathrm{d}\theta\\&=2\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_0^{3}\,\mathrm{d}\theta\\&=2\int_{0}^{2 \pi}(\frac{81}{4}-0)\,\mathrm{d}\theta\\&=\frac{81}{2}\int_{0}^{2 \pi}1\,\mathrm{d}\theta\\&=\frac{81}{2}\left[\theta\right]_{0}^{2 \pi}\\&=\frac{81}{2}(2 \pi-0)\\&=81 \pi\end{aligned}
$$

### Authored variant radial_square / easy

Parameters: `{'R': 4, 'c': 7}`; complete authored profile; metadata is not learner content.

Integrate the function $f(x,y)=7 x^{2} + 7 y^{2}$ over the disk of radius $4$ centered at the origin.

- $- 896 \pi$
- $\frac{896 \pi}{3}$
- $448 \pi$
- $56 \pi$
- $896 \pi$ **correct**

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, let's sketch our region $D:$

![]( /home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/23c9891711b5a2bd4c16.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 4,\ 0\le\theta\le 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}\iint_D 7 x^{2} + 7 y^{2}\,\mathrm{d}A &=\iint_\Delta 7((r\cos\theta)^2+(r\sin\theta)^2)r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\iint_\Delta 7r^2(\cos^2\theta+\sin^2\theta)r\,\mathrm{d}r\,\mathrm{d}\theta\\&=7\iint_\Delta r^3\,\mathrm{d}r\,\mathrm{d}\theta\\&=7\int_{0}^{2 \pi}\int_0^{4}r^3\,\mathrm{d}r\,\mathrm{d}\theta\\&=7\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_0^{4}\,\mathrm{d}\theta\\&=7\int_{0}^{2 \pi}(64-0)\,\mathrm{d}\theta\\&=448\int_{0}^{2 \pi}1\,\mathrm{d}\theta\\&=448\left[\theta\right]_{0}^{2 \pi}\\&=448(2 \pi-0)\\&=896 \pi\end{aligned}
$$

### Authored variant radial_square / easy

Parameters: `{'R': 2, 'c': 2}`; complete authored profile; metadata is not learner content.

Integrate the function $f(x,y)=2 x^{2} + 2 y^{2}$ over the disk of radius $2$ centered at the origin.

- $8 \pi$
- $- 16 \pi$
- $\frac{32 \pi}{3}$
- $16 \pi$ **correct**
- $\pi$

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, let's sketch our region $D:$

![]( /home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/f0a161b130a86212547e.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 2,\ 0\le\theta\le 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}\iint_D 2 x^{2} + 2 y^{2}\,\mathrm{d}A &=\iint_\Delta 2((r\cos\theta)^2+(r\sin\theta)^2)r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\iint_\Delta 2r^2(\cos^2\theta+\sin^2\theta)r\,\mathrm{d}r\,\mathrm{d}\theta\\&=2\iint_\Delta r^3\,\mathrm{d}r\,\mathrm{d}\theta\\&=2\int_{0}^{2 \pi}\int_0^{2}r^3\,\mathrm{d}r\,\mathrm{d}\theta\\&=2\int_{0}^{2 \pi}\left[\frac{r^4}{4}\right]_0^{2}\,\mathrm{d}\theta\\&=2\int_{0}^{2 \pi}(4-0)\,\mathrm{d}\theta\\&=8\int_{0}^{2 \pi}1\,\mathrm{d}\theta\\&=8\left[\theta\right]_{0}^{2 \pi}\\&=8(2 \pi-0)\\&=16 \pi\end{aligned}
$$

## Original q-161055

![](/media/jake/SSD/EDB/math/images/71/719f86db69489f62bcbe2753e88cdc6713f04dc6f53415cc2484e2eaab8ffac3.png)

Evaluate the double integral ${∬}_{D}\frac{x}{y}\,\text{d}A,$ where the region $D$ is the semicircle shown above.

- $\pi $
- $0$
- $1$ **correct**
- $2$
- $2\pi $

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, notice that the region $D$ represents a portion of the disk of radius $1$ centered at 
$(0,1).$

Cartesian and polar coordinates are connected by the following equations:

$$
{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the $x=\sqrt{2y-{y}^{2}}$ in polar coordinates:

$$
\begin{aligned}x & =\sqrt{2y-{y}^{2}} \\ {x}^{2} & =2y-{y}^{2} \\ {x}^{2}+{y}^{2} & =2y \\ (r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2} & =2r\operatorname{sin}⁡\theta  \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta ) & =2r\operatorname{sin}⁡\theta  \\ {r}^{2} & =2r\operatorname{sin}⁡\theta  \\ {r}^{2}-2r\operatorname{sin}⁡\theta  & =0 \\ r(r-2\operatorname{sin}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=2\operatorname{sin}⁡\theta .$

Therefore, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ={(r,\theta )\,:\,0\le r\le 2\operatorname{sin}⁡\theta ,\,0\le \theta \le \frac{\pi }{2}}.
$$

Therefore, we obtain

$$
\begin{aligned}{∬}_{D}\frac{x}{y}\,\text{d}A & ={∬}_{Δ}\frac{r\operatorname{cos}⁡\theta }{r\operatorname{sin}⁡\theta }\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}\frac{\operatorname{cos}⁡\theta }{\operatorname{sin}⁡\theta }{\int }_{0}^{2\operatorname{sin}⁡\theta }r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}\frac{\operatorname{cos}⁡\theta }{\operatorname{sin}⁡\theta }{[\frac{{r}^{2}}{2}]}_{0}^{2\operatorname{sin}⁡\theta }\,\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}\frac{\operatorname{cos}⁡\theta }{\operatorname{sin}⁡\theta }(2{sin}^{2}⁡\theta -0)\,\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}2\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}\operatorname{sin}⁡2\theta \,\text{d}\theta  \\  & ={[-\frac{1}{2}\operatorname{cos}⁡2\theta ]}_{0}^{\pi /2} \\  & =-\frac{1}{2}(\operatorname{cos}⁡\pi -\operatorname{cos}⁡0) \\  & =-\frac{1}{2}(-1-1) \\  & =1.\end{aligned}
$$

### Public observed_raw replay upper_ratio

Parameters: `{'R': 2, 'c': 1}`. Historical mathematical errors are deliberately retained, with balanced normalized TeX.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/80e1b905b79b16d1df9c.png)

Evaluate the double integral $\iint_D \frac{x}{y}\,\mathrm{d}A,$ where the region $D$ is the semicircle shown above.

- $2$
- $0$
- $1$ **correct**
- $2 \pi$
- $\pi$

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, notice that the region $D$ represents a portion of the disk of radius $1$ centered at
$(0,1).$

Cartesian and polar coordinates are connected by the following equations:

$$
\left\{\begin{aligned}x=r\cos\theta\\y=r\sin\theta\end{aligned}\right.
$$

With that in mind, let's now write the $x=\sqrt{2y-y^2}$ in polar coordinates:

$$
\begin{aligned}x&=\sqrt{2y-y^2}\\x^2&=2y-y^2\\x^2+y^2&=2y\\(r\cos\theta)^2+(r\sin\theta)^2&=2r\sin\theta\\r^2(\cos^2\theta+\sin^2\theta)&=2r\sin\theta\\r^2&=2r\sin\theta\\r^2-(2)r\sin\theta&=0\\r(r-(2)\sin\theta)&=0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=2 \sin{\left(\theta \right)}$.

Therefore, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 2 \sin{\left(\theta \right)},\ 0\le\theta\le \frac{\pi}{2}\}.
$$

Therefore, we obtain

$$
\begin{aligned}\iint_D \frac{x}{y}\,\mathrm{d}A &=\iint_\Delta 1\frac{r\cos\theta}{r\sin\theta}r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\int_{0}^{\frac{\pi}{2}}1\frac{\cos\theta}{\sin\theta}\int_0^{2 \sin{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}1\frac{\cos\theta}{\sin\theta}\left[\frac{r^2}{2}\right]_0^{2 \sin{\left(\theta \right)}}\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}1\frac{\cos\theta}{\sin\theta}(\frac{2^2}{2}\sin^2\theta-0)\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}2\cos\theta\sin\theta\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}1\sin2\theta\,\mathrm{d}\theta\\&=\left[-\frac{1}{2}\cos2\theta\right]_{0}^{\frac{\pi}{2}}\\&=-\frac{1}{2}(\cos\pi-\cos0)\\&=-\frac{1}{2}(-1-1)\\&=1\end{aligned}
$$

The integrand is defined for $y>0$ on the interior of $D$. The point $(0,0)$ is a boundary point. The integral is the limit with angular lower bound $\varepsilon>0$ as $\varepsilon\to0^+$; after radial integration the integrand is $\sin{\left(2 \theta \right)}$, whose integral converges. No principal value is required.

### Authored variant upper_ratio / hard

Parameters: `{'R': 1, 'c': 5}`; complete authored profile; metadata is not learner content.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/7278e55cff737d36ebc0.png)

Evaluate the double integral $\iint_D \frac{5 x}{y}\,\mathrm{d}A,$ where the region $D$ is the semicircle shown above.

- $\frac{5}{4}$ **correct**
- $\frac{5}{16}$
- $5$
- $\frac{5 \pi}{8}$
- $- \frac{5}{4}$

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, notice that the region $D$ represents a portion of the disk of radius $\frac{1}{2}$ centered at
$(0,\frac{1}{2}).$

Cartesian and polar coordinates are connected by the following equations:

$$
\left\{\begin{aligned}x=r\cos\theta\\y=r\sin\theta\end{aligned}\right.
$$

With that in mind, let's now write the $x=\sqrt{1y-y^2}$ in polar coordinates:

$$
\begin{aligned}x&=\sqrt{1y-y^2}\\x^2&=1y-y^2\\x^2+y^2&=1y\\(r\cos\theta)^2+(r\sin\theta)^2&=1r\sin\theta\\r^2(\cos^2\theta+\sin^2\theta)&=1r\sin\theta\\r^2&=1r\sin\theta\\r^2-(1)r\sin\theta&=0\\r(r-(1)\sin\theta)&=0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=\sin{\left(\theta \right)}$.

Therefore, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le \sin{\left(\theta \right)},\ 0\le\theta\le \frac{\pi}{2}\}.
$$

Therefore, we obtain

$$
\begin{aligned}\iint_D \frac{5 x}{y}\,\mathrm{d}A &=\iint_\Delta 5\frac{r\cos\theta}{r\sin\theta}r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\int_{0}^{\frac{\pi}{2}}5\frac{\cos\theta}{\sin\theta}\int_0^{\sin{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}5\frac{\cos\theta}{\sin\theta}\left[\frac{r^2}{2}\right]_0^{\sin{\left(\theta \right)}}\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}5\frac{\cos\theta}{\sin\theta}(\frac{1^2}{2}\sin^2\theta-0)\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}\frac{5}{2}\cos\theta\sin\theta\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}\frac{5}{4}\sin2\theta\,\mathrm{d}\theta\\&=\left[-\frac{5}{8}\cos2\theta\right]_{0}^{\frac{\pi}{2}}\\&=-\frac{5}{8}(\cos\pi-\cos0)\\&=-\frac{5}{8}(-1-1)\\&=\frac{5}{4}\end{aligned}
$$

The integrand is defined for $y>0$ on the interior of $D$. The point $(0,0)$ is a boundary point. The integral is the limit with angular lower bound $\varepsilon>0$ as $\varepsilon\to0^+$; after radial integration the integrand is $\frac{5 \sin{\left(2 \theta \right)}}{4}$, whose integral converges. No principal value is required.

### Authored variant upper_ratio / hard

Parameters: `{'R': 2, 'c': 2}`; complete authored profile; metadata is not learner content.

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/80e1b905b79b16d1df9c.png)

Evaluate the double integral $\iint_D \frac{2 x}{y}\,\mathrm{d}A,$ where the region $D$ is the semicircle shown above.

- $\pi$
- $-2$
- $4$
- $2$ **correct**
- $\frac{1}{2}$

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, notice that the region $D$ represents a portion of the disk of radius $1$ centered at
$(0,1).$

Cartesian and polar coordinates are connected by the following equations:

$$
\left\{\begin{aligned}x=r\cos\theta\\y=r\sin\theta\end{aligned}\right.
$$

With that in mind, let's now write the $x=\sqrt{2y-y^2}$ in polar coordinates:

$$
\begin{aligned}x&=\sqrt{2y-y^2}\\x^2&=2y-y^2\\x^2+y^2&=2y\\(r\cos\theta)^2+(r\sin\theta)^2&=2r\sin\theta\\r^2(\cos^2\theta+\sin^2\theta)&=2r\sin\theta\\r^2&=2r\sin\theta\\r^2-(2)r\sin\theta&=0\\r(r-(2)\sin\theta)&=0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=2 \sin{\left(\theta \right)}$.

Therefore, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 2 \sin{\left(\theta \right)},\ 0\le\theta\le \frac{\pi}{2}\}.
$$

Therefore, we obtain

$$
\begin{aligned}\iint_D \frac{2 x}{y}\,\mathrm{d}A &=\iint_\Delta 2\frac{r\cos\theta}{r\sin\theta}r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\int_{0}^{\frac{\pi}{2}}2\frac{\cos\theta}{\sin\theta}\int_0^{2 \sin{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}2\frac{\cos\theta}{\sin\theta}\left[\frac{r^2}{2}\right]_0^{2 \sin{\left(\theta \right)}}\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}2\frac{\cos\theta}{\sin\theta}(\frac{2^2}{2}\sin^2\theta-0)\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}4\cos\theta\sin\theta\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}2\sin2\theta\,\mathrm{d}\theta\\&=\left[-1\cos2\theta\right]_{0}^{\frac{\pi}{2}}\\&=-1(\cos\pi-\cos0)\\&=-1(-1-1)\\&=2\end{aligned}
$$

The integrand is defined for $y>0$ on the interior of $D$. The point $(0,0)$ is a boundary point. The integral is the limit with angular lower bound $\varepsilon>0$ as $\varepsilon\to0^+$; after radial integration the integrand is $2 \sin{\left(2 \theta \right)}$, whose integral converges. No principal value is required.

## Original q-83970

Integrate the function $f(x,y)=\frac{2}{{x}^{2}+{y}^{2}+1}$ over the portion of the disk of radius $1$ centered at the origin, where $x\le 0$ and $y\le 0.$

- $\frac{\pi }{2}$
- $2\operatorname{ln}⁡2$
- $\pi \operatorname{ln}⁡2$
- $\frac{\operatorname{ln}⁡2}{2}$
- $\frac{\pi \operatorname{ln}⁡2}{2}$ **correct**

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](/media/jake/SSD/EDB/math/images/e4/e4275e74a45deb22c0ed22546772e33fbd5caeb89a4036b1a2f4870e8ecf67a1.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 1,\,\pi \le \theta \le \frac{3\pi }{2}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}\frac{2}{{x}^{2}+{y}^{2}+1}\,\text{d}A & ={∬}_{Δ}\frac{2}{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}+1}\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{\pi }^{3\pi /2}{\int }_{0}^{1}\frac{2r}{{r}^{2}+1}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{\pi }^{3\pi /2}[\operatorname{ln}⁡({r}^{2}+1)]_{0}^{1}\,\text{d}\theta  \\  & ={\int }_{\pi }^{3\pi /2}(\operatorname{ln}⁡2-\operatorname{ln}⁡1)\,\text{d}\theta  \\  & =\operatorname{ln}⁡2{\int }_{\pi }^{3\pi /2}\text{d}\theta  \\  & =\operatorname{ln}⁡2[\theta ]_{\pi }^{3\pi /2} \\  & =\operatorname{ln}⁡2(\frac{3\pi }{2}-\pi ) \\  & =\frac{\pi \operatorname{ln}⁡2}{2}.\end{aligned}
$$

### Public observed_raw replay rational_quarter

Parameters: `{'R': 1, 'c': 2}`. Historical mathematical errors are deliberately retained, with balanced normalized TeX.

Integrate the function $f(x,y)=\frac{2}{x^{2} + y^{2} + 1}$ over the portion of the disk of radius $1$ centered at the origin, where $x\le0$ and $y\le0.$

- $\frac{\ln{\left(2 \right)}}{2}$
- $\ln{\left(4 \right)}$
- $\pi \ln{\left(2 \right)}$
- $\frac{\pi \ln{\left(2 \right)}}{2}$ **correct**
- $\frac{\pi}{2}$

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, let's sketch our region $D:$

![]( /home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/b26de10b6982335d3833.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 1,\ \pi\le\theta\le \frac{3 \pi}{2}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}\iint_D \frac{2}{x^{2} + y^{2} + 1}\,\mathrm{d}A &=\iint_\Delta \frac{2}{(r\cos\theta)^2+(r\sin\theta)^2+1}r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\int_{\pi}^{\frac{3 \pi}{2}}\int_0^{1}\frac{2r}{r^2+1}\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{\pi}^{\frac{3 \pi}{2}}\left[1\ln(r^2+1)\right]_0^{1}\,\mathrm{d}\theta\\&=\int_{\pi}^{\frac{3 \pi}{2}}1(\ln(2)-\ln1)\,\mathrm{d}\theta\\&=\ln{\left(2 \right)}\int_{\pi}^{\frac{3 \pi}{2}}1\,\mathrm{d}\theta\\&=\ln{\left(2 \right)}\left[\theta\right]_{\pi}^{\frac{3 \pi}{2}}\\&=\ln{\left(2 \right)}(\frac{3 \pi}{2}-\pi)\\&=\frac{\pi \ln{\left(2 \right)}}{2}\end{aligned}
$$

### Authored variant rational_quarter / moderate

Parameters: `{'R': 4, 'c': 7}`; complete authored profile; metadata is not learner content.

Integrate the function $f(x,y)=\frac{7}{x^{2} + y^{2} + 1}$ over the portion of the disk of radius $4$ centered at the origin, where $x\le0$ and $y\le0.$

- $- \frac{7 \pi \ln{\left(17 \right)}}{4}$
- $\frac{7 \pi \ln{\left(17 \right)}}{2}$
- $\frac{7 \ln{\left(17 \right)}}{2}$
- $7 \pi \ln{\left(17 \right)}$
- $\frac{7 \pi \ln{\left(17 \right)}}{4}$ **correct**

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, let's sketch our region $D:$

![]( /home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/5e3b5a07edc3e497a410.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 4,\ \pi\le\theta\le \frac{3 \pi}{2}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}\iint_D \frac{7}{x^{2} + y^{2} + 1}\,\mathrm{d}A &=\iint_\Delta \frac{7}{(r\cos\theta)^2+(r\sin\theta)^2+1}r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\int_{\pi}^{\frac{3 \pi}{2}}\int_0^{4}\frac{7r}{r^2+1}\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{\pi}^{\frac{3 \pi}{2}}\left[\frac{7}{2}\ln(r^2+1)\right]_0^{4}\,\mathrm{d}\theta\\&=\int_{\pi}^{\frac{3 \pi}{2}}\frac{7}{2}(\ln(17)-\ln1)\,\mathrm{d}\theta\\&=\frac{7 \ln{\left(17 \right)}}{2}\int_{\pi}^{\frac{3 \pi}{2}}1\,\mathrm{d}\theta\\&=\frac{7 \ln{\left(17 \right)}}{2}\left[\theta\right]_{\pi}^{\frac{3 \pi}{2}}\\&=\frac{7 \ln{\left(17 \right)}}{2}(\frac{3 \pi}{2}-\pi)\\&=\frac{7 \pi \ln{\left(17 \right)}}{4}\end{aligned}
$$

### Authored variant rational_quarter / moderate

Parameters: `{'R': 2, 'c': 2}`; complete authored profile; metadata is not learner content.

Integrate the function $f(x,y)=\frac{2}{x^{2} + y^{2} + 1}$ over the portion of the disk of radius $2$ centered at the origin, where $x\le0$ and $y\le0.$

- $\ln{\left(5 \right)}$
- $- \frac{\pi \ln{\left(5 \right)}}{2}$
- $\pi \ln{\left(5 \right)}$
- $\frac{\pi \ln{\left(5 \right)}}{2}$ **correct**
- $2 \pi \ln{\left(5 \right)}$

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, let's sketch our region $D:$

![]( /home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/306fe3fc5023d46773cb.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 2,\ \pi\le\theta\le \frac{3 \pi}{2}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}\iint_D \frac{2}{x^{2} + y^{2} + 1}\,\mathrm{d}A &=\iint_\Delta \frac{2}{(r\cos\theta)^2+(r\sin\theta)^2+1}r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\int_{\pi}^{\frac{3 \pi}{2}}\int_0^{2}\frac{2r}{r^2+1}\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{\pi}^{\frac{3 \pi}{2}}\left[1\ln(r^2+1)\right]_0^{2}\,\mathrm{d}\theta\\&=\int_{\pi}^{\frac{3 \pi}{2}}1(\ln(5)-\ln1)\,\mathrm{d}\theta\\&=\ln{\left(5 \right)}\int_{\pi}^{\frac{3 \pi}{2}}1\,\mathrm{d}\theta\\&=\ln{\left(5 \right)}\left[\theta\right]_{\pi}^{\frac{3 \pi}{2}}\\&=\ln{\left(5 \right)}(\frac{3 \pi}{2}-\pi)\\&=\frac{\pi \ln{\left(5 \right)}}{2}\end{aligned}
$$

## Original q-83520

Integrate the function $f(x,y)=x-y$ over the portion of the disk of radius $2$ centered at the origin, where $x\ge 0$ and $y\ge 0.$

- $\frac{16}{3}$
- $2$
- $\frac{4}{3}$
- $\frac{8}{3}$
- $0$ **correct**

We will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](/media/jake/SSD/EDB/math/images/7b/7b181b47af7d29b68d86d26b5c2b948c17ce39c01a62cbb36e874bb733865718.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 2,\,0\le \theta \le \frac{\pi }{2}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}x-y\,dA & ={∬}_{Δ}(r\operatorname{cos}⁡\theta -r\operatorname{sin}⁡\theta )\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}{\int }_{0}^{2}{r}^{2}(\operatorname{cos}⁡\theta -\operatorname{sin}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}(\operatorname{cos}⁡\theta -\operatorname{sin}⁡\theta ){\int }_{0}^{2}{r}^{2}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}(\operatorname{cos}⁡\theta -\operatorname{sin}⁡\theta )\,\frac{1}{3}{[{r}^{3}]}_{0}^{2}\,\text{d}\theta  \\  & =\frac{1}{3}{\int }_{0}^{\pi /2}(\operatorname{cos}⁡\theta -\operatorname{sin}⁡\theta )({2}^{3}-{0}^{3})\text{d}\theta  \\  & =\frac{8}{3}{\int }_{0}^{\pi /2}(\operatorname{cos}⁡\theta -\operatorname{sin}⁡\theta )\,\text{d}\theta  \\  & =\frac{8}{3}[\operatorname{sin}⁡\theta +\operatorname{cos}⁡\theta ]_{0}^{\pi /2} \\  & =\frac{8}{3}[(\operatorname{sin}⁡\frac{\pi }{2}+\operatorname{cos}⁡\frac{\pi }{2})-(\operatorname{sin}⁡0+\operatorname{cos}⁡0)] \\  & =\frac{8}{3}(1-1) \\  & =0.\end{aligned}
$$

### Public observed_raw replay quarter_difference

Parameters: `{'R': 2, 'c': 1}`. Historical mathematical errors are deliberately retained, with balanced normalized TeX.

Integrate the function $f(x,y)=x - y$ over the portion of the disk of radius $2$ centered at the origin, where $x\ge0$ and $y\ge0.$

- $\frac{8}{3}$
- $2$
- $\frac{4}{3}$
- $0$ **correct**
- $\frac{16}{3}$

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, let's sketch our region $D:$

![]( /home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/4d224e57769f9e38be0e.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 2,\ 0\le\theta\le \frac{\pi}{2}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}\iint_D x - y\,\mathrm{d}A &=\iint_\Delta 1(r\cos\theta-r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\int_{0}^{\frac{\pi}{2}}\int_0^{2}r^{2}1(\cos\theta-\sin\theta)\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}1(\cos\theta-\sin\theta)\int_0^{2}r^2\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}1(\cos\theta-\sin\theta)\left[\frac{r^3}{3}\right]_0^{2}\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}1(\cos\theta-\sin\theta)(\frac{2^3}{3}-0)\,\mathrm{d}\theta\\&=\frac{8}{3}\int_{0}^{\frac{\pi}{2}}1(\cos\theta-\sin\theta)\,\mathrm{d}\theta\\&=\frac{8}{3}\left[1(\sin\theta+\cos\theta)\right]_{0}^{\frac{\pi}{2}}\\&=\frac{8}{3}((1(\sin(\frac{\pi}{2})+\cos(\frac{\pi}{2})))-(1(\sin(0)+\cos(0))))\\&=\frac{8}{3}((1)-(1))\\&=0\end{aligned}
$$

### Authored variant quarter_difference / moderate

Parameters: `{'R': 4, 'c': 7}`; complete authored profile; metadata is not learner content.

Integrate the function $f(x,y)=7 x - 7 y$ over the portion of the disk of radius $4$ centered at the origin, where $x\ge0$ and $y\ge0.$

- $- \frac{896}{3}$
- $\frac{448}{3}$
- $- \frac{448}{3}$
- $\frac{896}{3}$
- $0$ **correct**

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, let's sketch our region $D:$

![]( /home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/995d0b57f7c53eeca928.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 4,\ 0\le\theta\le \frac{\pi}{2}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}\iint_D 7 x - 7 y\,\mathrm{d}A &=\iint_\Delta 7(r\cos\theta-r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\int_{0}^{\frac{\pi}{2}}\int_0^{4}r^{2}7(\cos\theta-\sin\theta)\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}7(\cos\theta-\sin\theta)\int_0^{4}r^2\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}7(\cos\theta-\sin\theta)\left[\frac{r^3}{3}\right]_0^{4}\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}7(\cos\theta-\sin\theta)(\frac{4^3}{3}-0)\,\mathrm{d}\theta\\&=\frac{64}{3}\int_{0}^{\frac{\pi}{2}}7(\cos\theta-\sin\theta)\,\mathrm{d}\theta\\&=\frac{64}{3}\left[7(\sin\theta+\cos\theta)\right]_{0}^{\frac{\pi}{2}}\\&=\frac{64}{3}((7(\sin(\frac{\pi}{2})+\cos(\frac{\pi}{2})))-(7(\sin(0)+\cos(0))))\\&=\frac{64}{3}((7+(0))-(0+(7)))\\&=0\end{aligned}
$$

### Authored variant quarter_difference / moderate

Parameters: `{'R': 2, 'c': 2}`; complete authored profile; metadata is not learner content.

Integrate the function $f(x,y)=2 x - 2 y$ over the portion of the disk of radius $2$ centered at the origin, where $x\ge0$ and $y\ge0.$

- $- \frac{16}{3}$
- $- \frac{32}{3}$
- $\frac{16}{3}$
- $0$ **correct**
- $\frac{32}{3}$

We will use the change of variables formula in the form

$$
\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.
$$

First, let's sketch our region $D:$

![]( /home/jake/Developer/Course_Academy/generate/scratch/17592186129200/plots/4d224e57769f9e38be0e.png)

In polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
\Delta=\{(r,\theta):0\le r\le 2,\ 0\le\theta\le \frac{\pi}{2}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}\iint_D 2 x - 2 y\,\mathrm{d}A &=\iint_\Delta 2(r\cos\theta-r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta\\
&=\int_{0}^{\frac{\pi}{2}}\int_0^{2}r^{2}2(\cos\theta-\sin\theta)\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}2(\cos\theta-\sin\theta)\int_0^{2}r^2\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}2(\cos\theta-\sin\theta)\left[\frac{r^3}{3}\right]_0^{2}\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}2(\cos\theta-\sin\theta)(\frac{2^3}{3}-0)\,\mathrm{d}\theta\\&=\frac{8}{3}\int_{0}^{\frac{\pi}{2}}2(\cos\theta-\sin\theta)\,\mathrm{d}\theta\\&=\frac{8}{3}\left[2(\sin\theta+\cos\theta)\right]_{0}^{\frac{\pi}{2}}\\&=\frac{8}{3}((2(\sin(\frac{\pi}{2})+\cos(\frac{\pi}{2})))-(2(\sin(0)+\cos(0))))\\&=\frac{8}{3}((2+(0))-(0+(2)))\\&=0\end{aligned}
$$

