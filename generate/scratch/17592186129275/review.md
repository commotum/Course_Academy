# Source originals and generated variants

Source basis1356; old unrated correct refs/solutions are authored repairs. Observed replays include only TeX presentation normalization. Setup variants state the response criterion. Scalar equality is not setup eligibility.


## difference — raw original 17592186129513

If $D = {(x, y): (x - 3)^{2} + y^{2} \le 9}$, then $∬_(D)(x^{2} - y^{2})dA =$

- $\displaystyle \int_{- π/2}^{π/2}\displaystyle \int_{0}^{6\cos θ}r^{2}\cos 2θdrdθ$
- $\displaystyle \int_{- π/2}^{π/2}\displaystyle \int_{0}^{3}r^{3}drdθ$
- $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{6\cos θ}r^{3}drdθ$
- $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{3}r^{3}\cos 2θdrdθ$
- $\displaystyle \int_{- π/2}^{π/2}\displaystyle \int_{0}^{6\cos θ}r^{3}\cos 2θdrdθ$

[No observed worked solution/correct designation.]

### Presentation-normalized source replay

If $D = \{(x, y): (x - 3)^{2} + y^{2} \le 9\}$, then $∬_(D)(x^{2} - y^{2})dA =$

- $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{6\cos θ}r^{3}drdθ$
- $\displaystyle \int_{- π/2}^{π/2}\displaystyle \int_{0}^{3}r^{3}drdθ$
- $\displaystyle \int_{- π/2}^{π/2}\displaystyle \int_{0}^{6\cos θ}r^{2}\cos 2θdrdθ$
- *Correct:* $\displaystyle \int_{- π/2}^{π/2}\displaystyle \int_{0}^{6\cos θ}r^{3}\cos 2θdrdθ$
- $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{3}r^{3}\cos 2θdrdθ$

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/055acba8301fa2b03007-region.png)

Notice that the region $D$ represents the disk of radius $3$ centered at $(3,0).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\cos\theta \\ y=r\sin\theta\end{aligned}
$$

With that in mind, let's now write the $(x-3)^{2}+y^{2}=9$ in polar coordinates:

$$
\begin{aligned}(x-3)^{2}+y^{2}&=9\\(r\cos\theta-3)^2+(r\sin\theta)^2&=9\\r^2\cos^2\theta-6r\cos\theta+9+r^2\sin^2\theta&=9\\r^2(\cos^2\theta+\sin^2\theta)-6r\cos\theta&=0\\r^2-6r\cos\theta&=0\\r(r-6\cos\theta)&=0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire circle, we must have $r=6 \cos{\left(\theta \right)}.$

Now, let's determine the limits for $r$ and $\theta.$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=6 \cos{\left(\theta \right)}$ (at the boundary of the region):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/055acba8301fa2b03007-radius.png)

Secondly, $\theta$ can vary between $\theta=- \frac{\pi}{2}$ and $\theta=\frac{\pi}{2}.$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/055acba8301fa2b03007-angle.png)

So, in polar coordinates $(r,\theta),$ the region can be expressed as

$$
\Delta=\{(r,\theta)\,:\,0\le r\le 6 \cos{\left(\theta \right)},\,- \frac{\pi}{2}\le\theta\le \frac{\pi}{2}\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iint_D x^{2} - y^{2}\,dA&=\iint_\Delta (- r^{2} \sin^{2}{\left(\theta \right)} + r^{2} \cos^{2}{\left(\theta \right)})\,r\,dr\,d\theta\\&=\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\int_{0}^{6 \cos{\left(\theta \right)}}r^3(\cos^2\theta-\sin^2\theta)\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\int_{0}^{6 \cos{\left(\theta \right)}}r^{3} \cos{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta.\end{aligned}
$$


## xsqrt — raw original 17592186129628

If $D = {(x, y): (x - 1)^{2} + y^{2} \le 1, y \ge 0}$, then $∬_(D)x\sqrt{x^{2} + y^{2}}dA =$

- $\displaystyle \int_{0}^{π}\cos θ\displaystyle \int_{0}^{2\cos θ}r^{3}drdθ$
- $\displaystyle \int_{0}^{π}\cos θ\displaystyle \int_{0}^{2\cos θ}r^{2}drdθ$
- $\displaystyle \int_{0}^{π/2}\cos θ\displaystyle \int_{0}^{1}r^{2}drdθ$
- $\displaystyle \int_{0}^{π/2}\cos θ\displaystyle \int_{0}^{1}rdrdθ$
- $\displaystyle \int_{0}^{π/2}\cos θ\displaystyle \int_{0}^{2\cos θ}r^{3}drdθ$

[No observed worked solution/correct designation.]

### Presentation-normalized source replay

If $D = \{(x, y): (x - 1)^{2} + y^{2} \le 1, y \ge 0\}$, then $∬_(D)x\sqrt{x^{2} + y^{2}}dA =$

- $\displaystyle \int_{0}^{π/2}\cos θ\displaystyle \int_{0}^{1}r^{2}drdθ$
- $\displaystyle \int_{0}^{π}\cos θ\displaystyle \int_{0}^{2\cos θ}r^{2}drdθ$
- $\displaystyle \int_{0}^{π}\cos θ\displaystyle \int_{0}^{2\cos θ}r^{3}drdθ$
- *Correct:* $\displaystyle \int_{0}^{π/2}\cos θ\displaystyle \int_{0}^{2\cos θ}r^{3}drdθ$
- $\displaystyle \int_{0}^{π/2}\cos θ\displaystyle \int_{0}^{1}rdrdθ$

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/66408d977690172e233a-region.png)

Notice that the region $D$ represents a portion of the disk of radius $1$ centered at $(1,0).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\cos\theta \\ y=r\sin\theta\end{aligned}
$$

With that in mind, let's now write the $(x-1)^{2}+y^{2}=1$ in polar coordinates:

$$
\begin{aligned}(x-1)^{2}+y^{2}&=1\\(r\cos\theta-1)^2+(r\sin\theta)^2&=1\\r^2\cos^2\theta-2r\cos\theta+1+r^2\sin^2\theta&=1\\r^2(\cos^2\theta+\sin^2\theta)-2r\cos\theta&=0\\r^2-2r\cos\theta&=0\\r(r-2\cos\theta)&=0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=2 \cos{\left(\theta \right)}.$

Now, let's determine the limits for $r$ and $\theta.$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=2 \cos{\left(\theta \right)}$ (at the boundary of the region):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/66408d977690172e233a-radius.png)

Secondly, $\theta$ can vary between $\theta=0$ and $\theta=\frac{\pi}{2}.$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/66408d977690172e233a-angle.png)

So, in polar coordinates $(r,\theta),$ the region can be expressed as

$$
\Delta=\{(r,\theta)\,:\,0\le r\le 2 \cos{\left(\theta \right)},\,0\le\theta\le \frac{\pi}{2}\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iint_D x \sqrt{x^{2} + y^{2}}\,dA&=\iint_\Delta (r \sqrt{r^{2} \sin^{2}{\left(\theta \right)} + r^{2} \cos^{2}{\left(\theta \right)}} \cos{\left(\theta \right)})\,r\,dr\,d\theta\\&=\int_{0}^{\frac{\pi}{2}}\int_{0}^{2 \cos{\left(\theta \right)}}r^2\cos\theta\sqrt{r^2(\cos^2\theta+\sin^2\theta)}\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}\int_{0}^{2 \cos{\left(\theta \right)}}r^3\cos\theta\sqrt{\cos^2\theta+\sin^2\theta}\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}\int_{0}^{2 \cos{\left(\theta \right)}}r^{3} \cos{\left(\theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta.\end{aligned}
$$


## linear — raw original 17592186278369

If $D={(x,y)\,:\,{x}^{2}+(y-1)^{2}\le 1},$ then ${∬}_{D}x\,\text{d}A=$

- ${\int }_{0}^{2\pi }{\int }_{0}^{2\operatorname{cos}⁡\theta }r\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{2\pi }{\int }_{0}^{2\operatorname{sin}⁡\theta }{r}^{2}\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{0}^{2\operatorname{sin}⁡\theta }r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{0}^{2\operatorname{sin}⁡\theta }{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{0}^{2\operatorname{cos}⁡\theta }{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\,dr\,d\theta .
$$

First, let's sketch our region $D:$

![](images/f0/f0417011f46d3860b7de86fe652a7d80dd9787cb05c2057601b41c17e0c2b423.png)

Notice that the region $D$ represents the disk of radius $1$ centered at $(0,1).$

Cartesian and polar coordinates are connected by the following equations:

$$
{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the ${x}^{2}+(y-1)^{2}=1$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+(y-1)^{2} & =1 \\ {(r\operatorname{cos}⁡\theta )}^{2}+{(r\operatorname{sin}⁡\theta -1)}^{2} & =1 \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -2r\operatorname{sin}⁡\theta +1 & =1 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-2r\operatorname{sin}⁡\theta  & =0 \\ {r}^{2}-2r\operatorname{sin}⁡\theta  & =0 \\ r(r-2\operatorname{sin}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire circle, we must have $r=2\operatorname{sin}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=2\operatorname{sin}⁡\theta $ (at the boundary of the region): 

![](images/3f/3f4bb1428a6cc9b7e191e1904636d654145d9a1f2fb1dd40843d8cd878194772.png)

Secondly, $\theta $ can vary between $\theta =0$ (the positive $x$-axis) and $\theta =\pi $ (the negative $x$-axis):

![](images/d6/d6f4e054767650cd2a3d348aee8210af421e2df21792d79f42c5a58b5f4e82e6.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ={(r,\theta )\,:\,0\le r\le 2\operatorname{sin}⁡\theta ,\,0\le \theta \le \pi }.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}x\,\text{d}A & ={∬}_{Δ}r\operatorname{cos}⁡\theta \cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{\pi }{\int }_{0}^{2\operatorname{sin}⁡\theta }{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$

### Presentation-normalized source replay

If $D=\{(x,y)\,:\,{x}^{2}+(y-1)^{2}\le 1\},$ then ${∬}_{D}x\,\text{d}A=$

- ${\int }_{0}^{\pi }{\int }_{0}^{2\operatorname{sin}⁡\theta }r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{2\pi }{\int }_{0}^{2\operatorname{sin}⁡\theta }{r}^{2}\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{2\pi }{\int }_{0}^{2\operatorname{cos}⁡\theta }r\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{0}^{2\operatorname{cos}⁡\theta }{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $
- *Correct:* ${\int }_{0}^{\pi }{\int }_{0}^{2\operatorname{sin}⁡\theta }{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\,dr\,d\theta .
$$

First, let's sketch our region $D:$

![](/media/jake/SSD/EDB/math/images/f0/f0417011f46d3860b7de86fe652a7d80dd9787cb05c2057601b41c17e0c2b423.png)

Notice that the region $D$ represents the disk of radius $1$ centered at $(0,1).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the ${x}^{2}+(y-1)^{2}=1$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+(y-1)^{2} & =1 \\ {(r\operatorname{cos}⁡\theta )}^{2}+{(r\operatorname{sin}⁡\theta -1)}^{2} & =1 \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -2r\operatorname{sin}⁡\theta +1 & =1 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-2r\operatorname{sin}⁡\theta  & =0 \\ {r}^{2}-2r\operatorname{sin}⁡\theta  & =0 \\ r(r-2\operatorname{sin}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire circle, we must have $r=2\operatorname{sin}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=2\operatorname{sin}⁡\theta $ (at the boundary of the region): 

![](/media/jake/SSD/EDB/math/images/3f/3f4bb1428a6cc9b7e191e1904636d654145d9a1f2fb1dd40843d8cd878194772.png)

Secondly, $\theta $ can vary between $\theta =0$ (the positive $x$-axis) and $\theta =\pi $ (the negative $x$-axis):

![](/media/jake/SSD/EDB/math/images/d6/d6f4e054767650cd2a3d348aee8210af421e2df21792d79f42c5a58b5f4e82e6.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 2\operatorname{sin}⁡\theta ,\,0\le \theta \le \pi \}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}x\,\text{d}A & ={∬}_{Δ}r\operatorname{cos}⁡\theta \cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{\pi }{\int }_{0}^{2\operatorname{sin}⁡\theta }{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$


## x2y — raw original 17592186278370

If $D=\{(x,y)\,:\,(x-2)^{2}+{y}^{2}\le 4\},$ then ${∬}_{D}{x}^{2}y\,\text{d}A=$

- ${\int }_{0}^{2\pi }{\int }_{0}^{2}{r}^{4}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2}{r}^{3}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{4\operatorname{cos}⁡\theta }{r}^{4}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{2\pi }{\int }_{0}^{4\operatorname{cos}⁡\theta }{r}^{4}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{4\operatorname{cos}⁡\theta }{r}^{3}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\,dr\,d\theta .
$$

First, let's sketch our region $D:$

![](images/86/86036fd86096355b969da695f812c9bf835880edd68f7991183b70a6234e3eb4.png)

Notice that the region $D$ represents the disk of radius $2$ centered at $(2,0).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the $(x-2)^{2}+{y}^{2}=4$ in polar coordinates:

$$
\begin{aligned}(x-2)^{2}+{y}^{2} & =4 \\ {(r\operatorname{cos}⁡\theta -2)}^{2}+{(r\operatorname{sin}⁡\theta )}^{2} & =4 \\ {r}^{2}{cos}^{2}⁡\theta -4r\operatorname{cos}⁡\theta +4+{r}^{2}{sin}^{2}⁡\theta  & =4 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-4r\operatorname{cos}⁡\theta  & =0 \\ {r}^{2}-4r\operatorname{cos}⁡\theta  & =0 \\ r(r-4\operatorname{cos}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire circle, we must have $r=4\operatorname{cos}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=4\operatorname{cos}⁡\theta $ (at the boundary of the region): 

![](images/9e/9ef22dcc15175664331d989bd50d9a8d60a354a0780dbaf9465caca04f28c2d9.png)

Secondly, $\theta $ can vary between $\theta =-\frac{\pi }{2}$ (the negative $y$-axis) and $\theta =\frac{\pi }{2}$ (the positive $y$-axis):

![](images/f7/f724daf8321195815c9e413aab2106c611bc9d2e9653939266fc828aebeca68c.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 4\operatorname{cos}⁡\theta ,\,-\frac{\pi }{2}\le \theta \le \frac{\pi }{2}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}{x}^{2}y\,\text{d}A & ={∬}_{Δ}(r\operatorname{cos}⁡\theta )^{2}(r\operatorname{sin}⁡\theta )\,r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{4\operatorname{cos}⁡\theta }{r}^{4}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$

### Presentation-normalized source replay

If $D=\{(x,y)\,:\,(x-2)^{2}+{y}^{2}\le 4\},$ then ${∬}_{D}{x}^{2}y\,\text{d}A=$

- *Correct:* ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{4\operatorname{cos}⁡\theta }{r}^{4}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2}{r}^{3}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{2\pi }{\int }_{0}^{2}{r}^{4}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{4\operatorname{cos}⁡\theta }{r}^{3}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{2\pi }{\int }_{0}^{4\operatorname{cos}⁡\theta }{r}^{4}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\,dr\,d\theta .
$$

First, let's sketch our region $D:$

![](/media/jake/SSD/EDB/math/images/86/86036fd86096355b969da695f812c9bf835880edd68f7991183b70a6234e3eb4.png)

Notice that the region $D$ represents the disk of radius $2$ centered at $(2,0).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the $(x-2)^{2}+{y}^{2}=4$ in polar coordinates:

$$
\begin{aligned}(x-2)^{2}+{y}^{2} & =4 \\ {(r\operatorname{cos}⁡\theta -2)}^{2}+{(r\operatorname{sin}⁡\theta )}^{2} & =4 \\ {r}^{2}{cos}^{2}⁡\theta -4r\operatorname{cos}⁡\theta +4+{r}^{2}{sin}^{2}⁡\theta  & =4 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-4r\operatorname{cos}⁡\theta  & =0 \\ {r}^{2}-4r\operatorname{cos}⁡\theta  & =0 \\ r(r-4\operatorname{cos}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire circle, we must have $r=4\operatorname{cos}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=4\operatorname{cos}⁡\theta $ (at the boundary of the region): 

![](/media/jake/SSD/EDB/math/images/9e/9ef22dcc15175664331d989bd50d9a8d60a354a0780dbaf9465caca04f28c2d9.png)

Secondly, $\theta $ can vary between $\theta =-\frac{\pi }{2}$ (the negative $y$-axis) and $\theta =\frac{\pi }{2}$ (the positive $y$-axis):

![](/media/jake/SSD/EDB/math/images/f7/f724daf8321195815c9e413aab2106c611bc9d2e9653939266fc828aebeca68c.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 4\operatorname{cos}⁡\theta ,\,-\frac{\pi }{2}\le \theta \le \frac{\pi }{2}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}{x}^{2}y\,\text{d}A & ={∬}_{Δ}(r\operatorname{cos}⁡\theta )^{2}(r\operatorname{sin}⁡\theta )\,r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{4\operatorname{cos}⁡\theta }{r}^{4}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$


## expdiff — raw original 17592186278371

If $D=\{(x,y)\,:\,(x-4)^{2}+{y}^{2}\le 16,\,y\le 0\},$ then ${∬}_{D}{e}^{{x}^{2}-{y}^{2}}\,\text{d}A=$

- ${\int }_{3\pi /2}^{2\pi }{\int }_{0}^{8\operatorname{cos}⁡\theta }r{e}^{{r}^{2}\operatorname{cos}⁡2\theta }\,\text{d}r\,\text{d}\theta $
- ${\int }_{3\pi /2}^{2\pi }{\int }_{0}^{4}r{e}^{{r}^{2}\operatorname{cos}⁡2\theta }\,\text{d}r\,\text{d}\theta $
- ${\int }_{3\pi /2}^{2\pi }{\int }_{0}^{8\operatorname{cos}⁡\theta }{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{2\pi }{\int }_{0}^{8\operatorname{cos}⁡\theta }{e}^{{r}^{2}\operatorname{cos}⁡2\theta }\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{2\pi }{\int }_{0}^{4}r{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\,dr\,d\theta .
$$

First, let's sketch our region $D:$

![](images/d8/d882bf70ecb7b94eee0eeeffbf63874ca8607268167f96278deb4678ec3b827a.png)

Notice that the region $D$ represents a portion of the disk of radius $4$ centered at $(4,0).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the $(x-4)^{2}+{y}^{2}=16$ in polar coordinates:

$$
\begin{aligned}(x-4)^{2}+{y}^{2} & =16 \\ {(r\operatorname{cos}⁡\theta -4)}^{2}+{(r\operatorname{sin}⁡\theta )}^{2} & =16 \\ {r}^{2}{cos}^{2}⁡\theta -8r\operatorname{cos}⁡\theta +16+{r}^{2}{sin}^{2}⁡\theta  & =16 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-8r\operatorname{cos}⁡\theta  & =0 \\ {r}^{2}-8r\operatorname{cos}⁡\theta  & =0 \\ r(r-8\operatorname{cos}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire circle, we must have $r=8\operatorname{cos}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=8\operatorname{cos}⁡\theta $ (at the boundary of the region): 

![](images/60/605d9ce1c9030d1ac83c0a320bd648b42893f222279dd2d56b111acd9957c202.png)

Secondly, $\theta $ can vary between $\theta =-\frac{\pi }{2}$ (the negative $y$-axis) and $\theta =0$ (the positive $x$-axis):

![](images/f3/f37e34042338af2b1ba5f0c214ebf046eeba068b0b3238b662910a868c069ee4.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 8\operatorname{cos}⁡\theta ,\,\frac{3\pi }{2}\le \theta \le 2\pi \}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}{e}^{{x}^{2}-{y}^{2}}\,\text{d}A & ={∬}_{Δ}{e}^{{x}^{2}-{y}^{2}}\,r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{3\pi /2}^{2\pi }{\int }_{0}^{8\operatorname{cos}⁡\theta }r{e}^{{r}^{2}{cos}^{2}⁡\theta -{r}^{2}{sin}^{2}⁡\theta }\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{3\pi /2}^{2\pi }{\int }_{0}^{8\operatorname{cos}⁡\theta }r{e}^{{r}^{2}({cos}^{2}⁡\theta -{sin}^{2}⁡\theta )}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{3\pi /2}^{2\pi }{\int }_{0}^{8\operatorname{cos}⁡\theta }r{e}^{{r}^{2}\operatorname{cos}⁡2\theta }\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

### Presentation-normalized source replay

If $D=\{(x,y)\,:\,(x-4)^{2}+{y}^{2}\le 16,\,y\le 0\},$ then ${∬}_{D}{e}^{{x}^{2}-{y}^{2}}\,\text{d}A=$

- ${\int }_{3\pi /2}^{2\pi }{\int }_{0}^{8\operatorname{cos}⁡\theta }{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $
- ${\int }_{3\pi /2}^{2\pi }{\int }_{0}^{4}r{e}^{{r}^{2}\operatorname{cos}⁡2\theta }\,\text{d}r\,\text{d}\theta $
- *Correct:* ${\int }_{3\pi /2}^{2\pi }{\int }_{0}^{8\operatorname{cos}⁡\theta }r{e}^{{r}^{2}\operatorname{cos}⁡2\theta }\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{2\pi }{\int }_{0}^{4}r{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{2\pi }{\int }_{0}^{8\operatorname{cos}⁡\theta }{e}^{{r}^{2}\operatorname{cos}⁡2\theta }\,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\,dr\,d\theta .
$$

First, let's sketch our region $D:$

![](/media/jake/SSD/EDB/math/images/d8/d882bf70ecb7b94eee0eeeffbf63874ca8607268167f96278deb4678ec3b827a.png)

Notice that the region $D$ represents a portion of the disk of radius $4$ centered at $(4,0).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the $(x-4)^{2}+{y}^{2}=16$ in polar coordinates:

$$
\begin{aligned}(x-4)^{2}+{y}^{2} & =16 \\ {(r\operatorname{cos}⁡\theta -4)}^{2}+{(r\operatorname{sin}⁡\theta )}^{2} & =16 \\ {r}^{2}{cos}^{2}⁡\theta -8r\operatorname{cos}⁡\theta +16+{r}^{2}{sin}^{2}⁡\theta  & =16 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-8r\operatorname{cos}⁡\theta  & =0 \\ {r}^{2}-8r\operatorname{cos}⁡\theta  & =0 \\ r(r-8\operatorname{cos}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire circle, we must have $r=8\operatorname{cos}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=8\operatorname{cos}⁡\theta $ (at the boundary of the region): 

![](/media/jake/SSD/EDB/math/images/60/605d9ce1c9030d1ac83c0a320bd648b42893f222279dd2d56b111acd9957c202.png)

Secondly, $\theta $ can vary between $\theta =-\frac{\pi }{2}$ (the negative $y$-axis) and $\theta =0$ (the positive $x$-axis):

![](/media/jake/SSD/EDB/math/images/f3/f37e34042338af2b1ba5f0c214ebf046eeba068b0b3238b662910a868c069ee4.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 8\operatorname{cos}⁡\theta ,\,\frac{3\pi }{2}\le \theta \le 2\pi \}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}{e}^{{x}^{2}-{y}^{2}}\,\text{d}A & ={∬}_{Δ}{e}^{{x}^{2}-{y}^{2}}\,r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{3\pi /2}^{2\pi }{\int }_{0}^{8\operatorname{cos}⁡\theta }r{e}^{{r}^{2}{cos}^{2}⁡\theta -{r}^{2}{sin}^{2}⁡\theta }\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{3\pi /2}^{2\pi }{\int }_{0}^{8\operatorname{cos}⁡\theta }r{e}^{{r}^{2}({cos}^{2}⁡\theta -{sin}^{2}⁡\theta )}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{3\pi /2}^{2\pi }{\int }_{0}^{8\operatorname{cos}⁡\theta }r{e}^{{r}^{2}\operatorname{cos}⁡2\theta }\,\text{d}r\,\text{d}\theta .\end{aligned}
$$


## sqrt — raw original 17592186351514

If $D={(x,y)\,:\,{x}^{2}+(y-2)^{2}\le 4,\,x\ge 0},$ then ${∬}_{D}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}A=$

- ${\int }_{0}^{\pi /2}{\int }_{0}^{4\operatorname{sin}⁡\theta }r\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{0}^{4\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi /2}{\int }_{0}^{4\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi /2}{\int }_{0}^{2\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{0}^{2\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](images/96/968419bad65410864c75e8abe766d21ac4d4acd835c73ea84118cf21ac066f79.png)

Notice that the region $D$ represents a portion of the disk of radius $2$ centered at $(0,2).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the ${x}^{2}+(y-2)^{2}=4$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+(y-2)^{2} & =4 \\ (r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta -2)^{2} & =4 \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -4r\operatorname{sin}⁡\theta +4 & =4 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-4r\operatorname{sin}⁡\theta  & =0 \\ {r}^{2}-4r\operatorname{sin}⁡\theta  & =0 \\ r(r-4\operatorname{sin}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=4\operatorname{sin}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=4\operatorname{sin}⁡\theta $ (at the boundary of the region): 

![](images/2f/2fe33fb6e1be8b6107cb667e9453613af906bd4da7d67f9d9323d49cce5ae06c.png)

Secondly, $\theta $ can vary between $\theta =0$ (the positive $x$-axis) and $\theta =\frac{\pi }{2}$ (the positive $y$-axis):

![](images/e2/e2b5e7b4433cbfb50ac7a9f991e4e4bc0cf8deecfefeeef0a4c9606ab6183cce.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ={(r,\theta )\,:\,0\le r\le 4\operatorname{sin}⁡\theta ,\,0\le \theta \le \frac{\pi }{2}}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}A & ={∬}_{Δ}\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}{\int }_{0}^{4\operatorname{sin}⁡\theta }\sqrt{{r}^{2}}\,r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}{\int }_{0}^{4\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

### Presentation-normalized source replay

If $D=\{(x,y)\,:\,{x}^{2}+(y-2)^{2}\le 4,\,x\ge 0\},$ then ${∬}_{D}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}A=$

- *Correct:* ${\int }_{0}^{\pi /2}{\int }_{0}^{4\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{0}^{4\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi /2}{\int }_{0}^{4\operatorname{sin}⁡\theta }r\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{0}^{2\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi /2}{\int }_{0}^{2\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](/media/jake/SSD/EDB/math/images/96/968419bad65410864c75e8abe766d21ac4d4acd835c73ea84118cf21ac066f79.png)

Notice that the region $D$ represents a portion of the disk of radius $2$ centered at $(0,2).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the ${x}^{2}+(y-2)^{2}=4$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+(y-2)^{2} & =4 \\ (r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta -2)^{2} & =4 \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -4r\operatorname{sin}⁡\theta +4 & =4 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-4r\operatorname{sin}⁡\theta  & =0 \\ {r}^{2}-4r\operatorname{sin}⁡\theta  & =0 \\ r(r-4\operatorname{sin}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=4\operatorname{sin}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=4\operatorname{sin}⁡\theta $ (at the boundary of the region): 

![](/media/jake/SSD/EDB/math/images/2f/2fe33fb6e1be8b6107cb667e9453613af906bd4da7d67f9d9323d49cce5ae06c.png)

Secondly, $\theta $ can vary between $\theta =0$ (the positive $x$-axis) and $\theta =\frac{\pi }{2}$ (the positive $y$-axis):

![](/media/jake/SSD/EDB/math/images/e2/e2b5e7b4433cbfb50ac7a9f991e4e4bc0cf8deecfefeeef0a4c9606ab6183cce.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 4\operatorname{sin}⁡\theta ,\,0\le \theta \le \frac{\pi }{2}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}A & ={∬}_{Δ}\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}{\int }_{0}^{4\operatorname{sin}⁡\theta }\sqrt{{r}^{2}}\,r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}{\int }_{0}^{4\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$


## xy2 — raw original 17592186394504

If $D={(x,y)\,:\,(x+\frac{1}{2})^{2}+{y}^{2}\le \frac{1}{4},\,y\le 0},$ then ${∬}_{D}x{y}^{2}\,\text{d}A=$

- ${\int }_{0}^{\pi /2}{\int }_{1}^{2\operatorname{sin}⁡\theta }{r}^{4}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{\operatorname{sec}⁡\theta }^{2\operatorname{sin}⁡\theta }{r}^{3}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{0}^{\operatorname{sin}⁡\theta }{r}^{4}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi /2}{\int }_{1}^{-\operatorname{cos}⁡\theta }{r}^{2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{\pi }^{3\pi /2}{\int }_{0}^{-\operatorname{cos}⁡\theta }{r}^{4}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](images/61/617a69d44661d03e1c170b0c397d11f6437a7222c286df5023154371ec90ab4d.png)

Notice that the region $D$ represents a portion of the disk of radius $\frac{1}{2}$ centered at $(-\frac{1}{2},0).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the ${(x+\frac{1}{2})}^{2}+{y}^{2}=\frac{1}{4}$ in polar coordinates:

$$
\begin{aligned}{(x+\frac{1}{2})}^{2}+{y}^{2} & =\frac{1}{4} \\ {(r\operatorname{cos}⁡\theta +\frac{1}{2})}^{2}+(r\operatorname{sin}⁡\theta )^{2} & =\frac{1}{4} \\ {r}^{2}{cos}^{2}⁡\theta +r\operatorname{cos}⁡\theta +\frac{1}{4}+{r}^{2}{sin}^{2}⁡\theta  & =\frac{1}{4} \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+r\operatorname{cos}⁡\theta  & =0 \\ {r}^{2}+r\operatorname{cos}⁡\theta  & =0 \\ r(r+\operatorname{cos}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=-\operatorname{cos}⁡\theta .$ 

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=-\operatorname{cos}⁡\theta $ (at the boundary of the region): 

![](images/fe/fe82880fec605db684a2b5cb0da5c88a38da5b4fb4faad1f80c4d5b0691fde21.png)

Secondly, $\theta $ can vary between $\theta =\pi $ (the negative $x$-axis) and $\theta =\frac{3\pi }{2}$ (the negative $y$-axis):

![](images/9e/9e1693005c8930a7b2b8a3b47bc96f5441bf72ee6c5b67f3b8c97d87cfa2e34b.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ={(r,\theta )\,:\,0\le r\le -\operatorname{cos}⁡\theta ,\,\pi \le \theta \le \frac{3\pi }{2}}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}x{y}^{2}\,\text{d}A & ={∬}_{Δ}(r\operatorname{cos}⁡\theta )(r\operatorname{sin}⁡\theta )^{2}\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{\pi }^{3\pi /2}{\int }_{0}^{-\operatorname{cos}⁡\theta }{r}^{4}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$

### Presentation-normalized source replay

If $D=\{(x,y)\,:\,(x+\frac{1}{2})^{2}+{y}^{2}\le \frac{1}{4},\,y\le 0\},$ then ${∬}_{D}x{y}^{2}\,\text{d}A=$

- ${\int }_{0}^{\pi }{\int }_{0}^{\operatorname{sin}⁡\theta }{r}^{4}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{\operatorname{sec}⁡\theta }^{2\operatorname{sin}⁡\theta }{r}^{3}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi /2}{\int }_{1}^{2\operatorname{sin}⁡\theta }{r}^{4}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $
- *Correct:* ${\int }_{\pi }^{3\pi /2}{\int }_{0}^{-\operatorname{cos}⁡\theta }{r}^{4}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi /2}{\int }_{1}^{-\operatorname{cos}⁡\theta }{r}^{2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](/media/jake/SSD/EDB/math/images/61/617a69d44661d03e1c170b0c397d11f6437a7222c286df5023154371ec90ab4d.png)

Notice that the region $D$ represents a portion of the disk of radius $\frac{1}{2}$ centered at $(-\frac{1}{2},0).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the ${(x+\frac{1}{2})}^{2}+{y}^{2}=\frac{1}{4}$ in polar coordinates:

$$
\begin{aligned}{(x+\frac{1}{2})}^{2}+{y}^{2} & =\frac{1}{4} \\ {(r\operatorname{cos}⁡\theta +\frac{1}{2})}^{2}+(r\operatorname{sin}⁡\theta )^{2} & =\frac{1}{4} \\ {r}^{2}{cos}^{2}⁡\theta +r\operatorname{cos}⁡\theta +\frac{1}{4}+{r}^{2}{sin}^{2}⁡\theta  & =\frac{1}{4} \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+r\operatorname{cos}⁡\theta  & =0 \\ {r}^{2}+r\operatorname{cos}⁡\theta  & =0 \\ r(r+\operatorname{cos}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=-\operatorname{cos}⁡\theta .$ 

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=-\operatorname{cos}⁡\theta $ (at the boundary of the region): 

![](/media/jake/SSD/EDB/math/images/fe/fe82880fec605db684a2b5cb0da5c88a38da5b4fb4faad1f80c4d5b0691fde21.png)

Secondly, $\theta $ can vary between $\theta =\pi $ (the negative $x$-axis) and $\theta =\frac{3\pi }{2}$ (the negative $y$-axis):

![](/media/jake/SSD/EDB/math/images/9e/9e1693005c8930a7b2b8a3b47bc96f5441bf72ee6c5b67f3b8c97d87cfa2e34b.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le -\operatorname{cos}⁡\theta ,\,\pi \le \theta \le \frac{3\pi }{2}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}x{y}^{2}\,\text{d}A & ={∬}_{Δ}(r\operatorname{cos}⁡\theta )(r\operatorname{sin}⁡\theta )^{2}\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{\pi }^{3\pi /2}{\int }_{0}^{-\operatorname{cos}⁡\theta }{r}^{4}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$


## radial2 — raw original 17592186394545

If $D={(x,y)\,:\,{x}^{2}+{(y-\frac{1}{2})}^{2}\le \frac{1}{4},\,x\le 0},$ then ${∬}_{D}({x}^{2}+{y}^{2})\,\text{d}A=$

- ${\int }_{\pi /2}^{\pi }{\int }_{0}^{\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{0}^{\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $
- ${\int }_{-\pi /2}^{\pi }{\int }_{0}^{\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta $
- ${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{\operatorname{sin}⁡\theta }r\,\text{d}r\,\text{d}\theta $
- ${\int }_{\pi }^{2\pi }{\int }_{0}^{\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](images/32/32c4bf490df51121ddf1575df8211033185d392fd5b08519971723b820da191f.png)

Notice that the region $D$ represents a portion of the disk of radius $\frac{1}{2}$ centered at $(0,\frac{1}{2}).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the ${x}^{2}+{(y-\frac{1}{2})}^{2}=\frac{1}{4}$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+{(y-\frac{1}{2})}^{2} & =\frac{1}{4} \\ (r\operatorname{cos}⁡\theta )^{2}+{(r\operatorname{sin}⁡\theta -\frac{1}{2})}^{2} & =\frac{1}{4} \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -r\operatorname{sin}⁡\theta +\frac{1}{4} & =\frac{1}{4} \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-r\operatorname{sin}⁡\theta  & =0 \\ {r}^{2}-r\operatorname{sin}⁡\theta  & =0 \\ r(r-\operatorname{sin}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=\operatorname{sin}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=\operatorname{sin}⁡\theta $ (at the boundary of the region): 

![](images/b1/b1e2eac0041d0b0cb802561b3fb83fd8fab1b940cb6c42f698879837c06cbff0.png)

Secondly, $\theta $ can vary between $\theta =\frac{\pi }{2}$ (the positive $y$-axis) and $\theta =\pi $ (the negative $x$-axis):

![](images/19/193601785ff94605d12b91b7cab1e7390af532ba1912530bd8d3f492324e2788.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ={(r,\theta )\,:\,0\le r\le \operatorname{sin}⁡\theta ,\,\frac{\pi }{2}\le \theta \le \pi }.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}({x}^{2}+{y}^{2})\,\text{d}A & ={∬}_{Δ}((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2})\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{\pi /2}^{\pi }{\int }_{0}^{\operatorname{sin}⁡\theta }{r}^{3}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{\pi /2}^{\pi }{\int }_{0}^{\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

### Presentation-normalized source replay

If $D=\{(x,y)\,:\,{x}^{2}+{(y-\frac{1}{2})}^{2}\le \frac{1}{4},\,x\le 0\},$ then ${∬}_{D}({x}^{2}+{y}^{2})\,\text{d}A=$

- ${\int }_{-\pi /2}^{\pi }{\int }_{0}^{\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{0}^{\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $
- *Correct:* ${\int }_{\pi /2}^{\pi }{\int }_{0}^{\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta $
- ${\int }_{\pi }^{2\pi }{\int }_{0}^{\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $
- ${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{\operatorname{sin}⁡\theta }r\,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](/media/jake/SSD/EDB/math/images/32/32c4bf490df51121ddf1575df8211033185d392fd5b08519971723b820da191f.png)

Notice that the region $D$ represents a portion of the disk of radius $\frac{1}{2}$ centered at $(0,\frac{1}{2}).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the ${x}^{2}+{(y-\frac{1}{2})}^{2}=\frac{1}{4}$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+{(y-\frac{1}{2})}^{2} & =\frac{1}{4} \\ (r\operatorname{cos}⁡\theta )^{2}+{(r\operatorname{sin}⁡\theta -\frac{1}{2})}^{2} & =\frac{1}{4} \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -r\operatorname{sin}⁡\theta +\frac{1}{4} & =\frac{1}{4} \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-r\operatorname{sin}⁡\theta  & =0 \\ {r}^{2}-r\operatorname{sin}⁡\theta  & =0 \\ r(r-\operatorname{sin}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=\operatorname{sin}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=\operatorname{sin}⁡\theta $ (at the boundary of the region): 

![](/media/jake/SSD/EDB/math/images/b1/b1e2eac0041d0b0cb802561b3fb83fd8fab1b940cb6c42f698879837c06cbff0.png)

Secondly, $\theta $ can vary between $\theta =\frac{\pi }{2}$ (the positive $y$-axis) and $\theta =\pi $ (the negative $x$-axis):

![](/media/jake/SSD/EDB/math/images/19/193601785ff94605d12b91b7cab1e7390af532ba1912530bd8d3f492324e2788.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le \operatorname{sin}⁡\theta ,\,\frac{\pi }{2}\le \theta \le \pi \}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}({x}^{2}+{y}^{2})\,\text{d}A & ={∬}_{Δ}((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2})\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{\pi /2}^{\pi }{\int }_{0}^{\operatorname{sin}⁡\theta }{r}^{3}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{\pi /2}^{\pi }{\int }_{0}^{\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$


## log — raw original 17592186394552

If $D={(x,y)\,:\,(x-1)^{2}+{y}^{2}\le 1,\,y\le 0},$ then ${∬}_{D}\operatorname{ln}⁡({x}^{2}+{y}^{2}+1)\,\text{d}A=$

- ${\int }_{-\pi }^{0}{\int }_{0}^{2\operatorname{cos}⁡\theta }2r\operatorname{ln}⁡(r+1)\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{0}^{\operatorname{cos}⁡\theta }{r}^{2}\operatorname{ln}⁡(r+1)\,\text{d}r\,\text{d}\theta $
- ${\int }_{-\pi /2}^{0}{\int }_{0}^{2\operatorname{cos}⁡\theta }r\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{cos}⁡\theta }\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $
- ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2\operatorname{cos}⁡\theta }r\operatorname{ln}⁡({r}^{2})\,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](images/bf/bf84eed655256e63439ca907610c4b0b022c6c480d5ab0b6c12d6826af9f0907.png)

Notice that the region $D$ represents a portion of the disk of radius $1$ centered at $(1,0).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the $(x-1)^{2}+{y}^{2}=1$ in polar coordinates:

$$
\begin{aligned}(x-1)^{2}+{y}^{2} & =1 \\ (r\operatorname{cos}⁡\theta -1)^{2}+{(r\operatorname{sin}⁡\theta )}^{2} & =1 \\ {r}^{2}{cos}^{2}⁡\theta -2r\operatorname{cos}⁡\theta +1+{r}^{2}{sin}^{2}⁡\theta  & =1 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-2r\operatorname{cos}⁡\theta  & =0 \\ {r}^{2}-2r\operatorname{cos}⁡\theta  & =0 \\ r(r-2\operatorname{cos}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=2\operatorname{cos}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=2\operatorname{cos}⁡\theta $ (at the boundary of the region): 

![](images/6d/6de2b6e2b9925577f8cf0961f8466707f770ddca175a04dac9b592542aac16e8.png)

Secondly, $\theta $ can vary between $\theta =-\frac{\pi }{2}$ (the negative $y$-axis) and $\theta =0$ (the positive $x$-axis):

![](images/4a/4a56d4023b03b40b4c1be5f22809963d6c745fd90ed3d860cf69d555b3e869ae.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ={(r,\theta )\,:\,0\le r\le 2\operatorname{cos}⁡\theta ,\,-\frac{\pi }{2}\le \theta \le 0}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}\operatorname{ln}⁡({x}^{2}+{y}^{2}+1)\,\text{d}A & ={∬}_{Δ}\operatorname{ln}⁡((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}+1)\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{-\pi /2}^{0}{\int }_{0}^{2\operatorname{cos}⁡\theta }r\operatorname{ln}⁡({r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+1)\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{-\pi /2}^{0}{\int }_{0}^{2\operatorname{cos}⁡\theta }r\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

### Presentation-normalized source replay

If $D=\{(x,y)\,:\,(x-1)^{2}+{y}^{2}\le 1,\,y\le 0\},$ then ${∬}_{D}\operatorname{ln}⁡({x}^{2}+{y}^{2}+1)\,\text{d}A=$

- *Correct:* ${\int }_{-\pi /2}^{0}{\int }_{0}^{2\operatorname{cos}⁡\theta }r\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{0}^{\operatorname{cos}⁡\theta }{r}^{2}\operatorname{ln}⁡(r+1)\,\text{d}r\,\text{d}\theta $
- ${\int }_{-\pi }^{0}{\int }_{0}^{2\operatorname{cos}⁡\theta }2r\operatorname{ln}⁡(r+1)\,\text{d}r\,\text{d}\theta $
- ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2\operatorname{cos}⁡\theta }r\operatorname{ln}⁡({r}^{2})\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{cos}⁡\theta }\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](/media/jake/SSD/EDB/math/images/bf/bf84eed655256e63439ca907610c4b0b022c6c480d5ab0b6c12d6826af9f0907.png)

Notice that the region $D$ represents a portion of the disk of radius $1$ centered at $(1,0).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the $(x-1)^{2}+{y}^{2}=1$ in polar coordinates:

$$
\begin{aligned}(x-1)^{2}+{y}^{2} & =1 \\ (r\operatorname{cos}⁡\theta -1)^{2}+{(r\operatorname{sin}⁡\theta )}^{2} & =1 \\ {r}^{2}{cos}^{2}⁡\theta -2r\operatorname{cos}⁡\theta +1+{r}^{2}{sin}^{2}⁡\theta  & =1 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-2r\operatorname{cos}⁡\theta  & =0 \\ {r}^{2}-2r\operatorname{cos}⁡\theta  & =0 \\ r(r-2\operatorname{cos}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=2\operatorname{cos}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=2\operatorname{cos}⁡\theta $ (at the boundary of the region): 

![](/media/jake/SSD/EDB/math/images/6d/6de2b6e2b9925577f8cf0961f8466707f770ddca175a04dac9b592542aac16e8.png)

Secondly, $\theta $ can vary between $\theta =-\frac{\pi }{2}$ (the negative $y$-axis) and $\theta =0$ (the positive $x$-axis):

![](/media/jake/SSD/EDB/math/images/4a/4a56d4023b03b40b4c1be5f22809963d6c745fd90ed3d860cf69d555b3e869ae.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 2\operatorname{cos}⁡\theta ,\,-\frac{\pi }{2}\le \theta \le 0\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}\operatorname{ln}⁡({x}^{2}+{y}^{2}+1)\,\text{d}A & ={∬}_{Δ}\operatorname{ln}⁡((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}+1)\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{-\pi /2}^{0}{\int }_{0}^{2\operatorname{cos}⁡\theta }r\operatorname{ln}⁡({r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+1)\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{-\pi /2}^{0}{\int }_{0}^{2\operatorname{cos}⁡\theta }r\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta .\end{aligned}
$$


## Generated easy constant_right radius 2

If $D=\{(x,y)\,:\,(x-2)^{2}+y^{2}\le 4\},$ then $\iint_D 1\,\mathrm{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- $\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\int_{0}^{4 \cos{\left(\theta \right)}}1\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{0}^{2 \pi}\int_{0}^{4 \cos{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- *Correct:* $\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\int_{0}^{4 \cos{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\int_{0}^{- 4 \cos{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\int_{0}^{2}r\,\mathrm{d}r\,\mathrm{d}\theta$

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/68ba463cfa2a81445838-region.png)

Notice that the region $D$ represents the disk of radius $2$ centered at $(2,0).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\cos\theta \\ y=r\sin\theta\end{aligned}
$$

With that in mind, let's now write the $(x-2)^{2}+y^{2}=4$ in polar coordinates:

$$
\begin{aligned}(x-2)^{2}+y^{2}&=4\\(r\cos\theta-2)^2+(r\sin\theta)^2&=4\\r^2\cos^2\theta-4r\cos\theta+4+r^2\sin^2\theta&=4\\r^2(\cos^2\theta+\sin^2\theta)-4r\cos\theta&=0\\r^2-4r\cos\theta&=0\\r(r-4\cos\theta)&=0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire circle, we must have $r=4 \cos{\left(\theta \right)}.$

Now, let's determine the limits for $r$ and $\theta.$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=4 \cos{\left(\theta \right)}$ (at the boundary of the region):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/68ba463cfa2a81445838-radius.png)

Secondly, $\theta$ can vary between $\theta=- \frac{\pi}{2}$ and $\theta=\frac{\pi}{2}.$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/68ba463cfa2a81445838-angle.png)

So, in polar coordinates $(r,\theta),$ the region can be expressed as

$$
\Delta=\{(r,\theta)\,:\,0\le r\le 4 \cos{\left(\theta \right)},\,- \frac{\pi}{2}\le\theta\le \frac{\pi}{2}\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iint_D 1\,dA&=\iint_\Delta (1)\,r\,dr\,d\theta\\&=\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\int_{0}^{4 \cos{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta.\end{aligned}
$$


## Generated easy constant_right radius 4

If $D=\{(x,y)\,:\,(x-4)^{2}+y^{2}\le 16\},$ then $\iint_D 1\,\mathrm{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- $\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\int_{0}^{8 \cos{\left(\theta \right)}}1\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{0}^{2 \pi}\int_{0}^{8 \cos{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- *Correct:* $\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\int_{0}^{8 \cos{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\int_{0}^{- 8 \cos{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\int_{0}^{4}r\,\mathrm{d}r\,\mathrm{d}\theta$

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/030000d23280b593c8a7-region.png)

Notice that the region $D$ represents the disk of radius $4$ centered at $(4,0).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\cos\theta \\ y=r\sin\theta\end{aligned}
$$

With that in mind, let's now write the $(x-4)^{2}+y^{2}=16$ in polar coordinates:

$$
\begin{aligned}(x-4)^{2}+y^{2}&=16\\(r\cos\theta-4)^2+(r\sin\theta)^2&=16\\r^2\cos^2\theta-8r\cos\theta+16+r^2\sin^2\theta&=16\\r^2(\cos^2\theta+\sin^2\theta)-8r\cos\theta&=0\\r^2-8r\cos\theta&=0\\r(r-8\cos\theta)&=0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire circle, we must have $r=8 \cos{\left(\theta \right)}.$

Now, let's determine the limits for $r$ and $\theta.$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=8 \cos{\left(\theta \right)}$ (at the boundary of the region):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/030000d23280b593c8a7-radius.png)

Secondly, $\theta$ can vary between $\theta=- \frac{\pi}{2}$ and $\theta=\frac{\pi}{2}.$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/030000d23280b593c8a7-angle.png)

So, in polar coordinates $(r,\theta),$ the region can be expressed as

$$
\Delta=\{(r,\theta)\,:\,0\le r\le 8 \cos{\left(\theta \right)},\,- \frac{\pi}{2}\le\theta\le \frac{\pi}{2}\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iint_D 1\,dA&=\iint_\Delta (1)\,r\,dr\,d\theta\\&=\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\int_{0}^{8 \cos{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta.\end{aligned}
$$


## Generated easy constant_left radius 2

If $D=\{(x,y)\,:\,(x+2)^{2}+y^{2}\le 4\},$ then $\iint_D 1\,\mathrm{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- $\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}\int_{0}^{- 4 \cos{\left(\theta \right)}}1\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{0}^{2 \pi}\int_{0}^{- 4 \cos{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- *Correct:* $\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}\int_{0}^{- 4 \cos{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}\int_{0}^{4 \cos{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}\int_{0}^{2}r\,\mathrm{d}r\,\mathrm{d}\theta$

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/2b760fb1fe775ce05cfa-region.png)

Notice that the region $D$ represents the disk of radius $2$ centered at $(-2,0).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\cos\theta \\ y=r\sin\theta\end{aligned}
$$

With that in mind, let's now write the $(x+2)^{2}+y^{2}=4$ in polar coordinates:

$$
\begin{aligned}(x+2)^{2}+y^{2}&=4\\(r\cos\theta+2)^2+(r\sin\theta)^2&=4\\r^2\cos^2\theta+4r\cos\theta+4+r^2\sin^2\theta&=4\\r^2(\cos^2\theta+\sin^2\theta)+4r\cos\theta&=0\\r^2+4r\cos\theta&=0\\r(r+4\cos\theta)&=0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire circle, we must have $r=- 4 \cos{\left(\theta \right)}.$

Now, let's determine the limits for $r$ and $\theta.$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=- 4 \cos{\left(\theta \right)}$ (at the boundary of the region):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/2b760fb1fe775ce05cfa-radius.png)

Secondly, $\theta$ can vary between $\theta=\frac{\pi}{2}$ and $\theta=\frac{3 \pi}{2}.$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/2b760fb1fe775ce05cfa-angle.png)

So, in polar coordinates $(r,\theta),$ the region can be expressed as

$$
\Delta=\{(r,\theta)\,:\,0\le r\le - 4 \cos{\left(\theta \right)},\,\frac{\pi}{2}\le\theta\le \frac{3 \pi}{2}\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iint_D 1\,dA&=\iint_\Delta (1)\,r\,dr\,d\theta\\&=\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}\int_{0}^{- 4 \cos{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta.\end{aligned}
$$


## Generated easy constant_left radius 4

If $D=\{(x,y)\,:\,(x+4)^{2}+y^{2}\le 16\},$ then $\iint_D 1\,\mathrm{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- $\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}\int_{0}^{- 8 \cos{\left(\theta \right)}}1\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{0}^{2 \pi}\int_{0}^{- 8 \cos{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- *Correct:* $\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}\int_{0}^{- 8 \cos{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}\int_{0}^{8 \cos{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}\int_{0}^{4}r\,\mathrm{d}r\,\mathrm{d}\theta$

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/36ee9daa13f87ed7aa67-region.png)

Notice that the region $D$ represents the disk of radius $4$ centered at $(-4,0).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\cos\theta \\ y=r\sin\theta\end{aligned}
$$

With that in mind, let's now write the $(x+4)^{2}+y^{2}=16$ in polar coordinates:

$$
\begin{aligned}(x+4)^{2}+y^{2}&=16\\(r\cos\theta+4)^2+(r\sin\theta)^2&=16\\r^2\cos^2\theta+8r\cos\theta+16+r^2\sin^2\theta&=16\\r^2(\cos^2\theta+\sin^2\theta)+8r\cos\theta&=0\\r^2+8r\cos\theta&=0\\r(r+8\cos\theta)&=0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire circle, we must have $r=- 8 \cos{\left(\theta \right)}.$

Now, let's determine the limits for $r$ and $\theta.$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=- 8 \cos{\left(\theta \right)}$ (at the boundary of the region):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/36ee9daa13f87ed7aa67-radius.png)

Secondly, $\theta$ can vary between $\theta=\frac{\pi}{2}$ and $\theta=\frac{3 \pi}{2}.$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/36ee9daa13f87ed7aa67-angle.png)

So, in polar coordinates $(r,\theta),$ the region can be expressed as

$$
\Delta=\{(r,\theta)\,:\,0\le r\le - 8 \cos{\left(\theta \right)},\,\frac{\pi}{2}\le\theta\le \frac{3 \pi}{2}\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iint_D 1\,dA&=\iint_\Delta (1)\,r\,dr\,d\theta\\&=\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}}\int_{0}^{- 8 \cos{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta.\end{aligned}
$$


## Generated easy constant_above radius 2

If $D=\{(x,y)\,:\,x^{2}+(y-2)^{2}\le 4\},$ then $\iint_D 1\,\mathrm{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- $\int_{0}^{\pi}\int_{0}^{4 \sin{\left(\theta \right)}}1\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{0}^{2 \pi}\int_{0}^{4 \sin{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- *Correct:* $\int_{0}^{\pi}\int_{0}^{4 \sin{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{0}^{\pi}\int_{0}^{- 4 \sin{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{0}^{\pi}\int_{0}^{2}r\,\mathrm{d}r\,\mathrm{d}\theta$

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/d6d7924940535fee18a6-region.png)

Notice that the region $D$ represents the disk of radius $2$ centered at $(0,2).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\cos\theta \\ y=r\sin\theta\end{aligned}
$$

With that in mind, let's now write the $x^{2}+(y-2)^{2}=4$ in polar coordinates:

$$
\begin{aligned}x^{2}+(y-2)^{2}&=4\\(r\cos\theta)^2+(r\sin\theta-2)^2&=4\\r^2\cos^2\theta+r^2\sin^2\theta-4r\sin\theta+4&=4\\r^2(\cos^2\theta+\sin^2\theta)-4r\sin\theta&=0\\r^2-4r\sin\theta&=0\\r(r-4\sin\theta)&=0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire circle, we must have $r=4 \sin{\left(\theta \right)}.$

Now, let's determine the limits for $r$ and $\theta.$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=4 \sin{\left(\theta \right)}$ (at the boundary of the region):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/d6d7924940535fee18a6-radius.png)

Secondly, $\theta$ can vary between $\theta=0$ and $\theta=\pi.$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/d6d7924940535fee18a6-angle.png)

So, in polar coordinates $(r,\theta),$ the region can be expressed as

$$
\Delta=\{(r,\theta)\,:\,0\le r\le 4 \sin{\left(\theta \right)},\,0\le\theta\le \pi\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iint_D 1\,dA&=\iint_\Delta (1)\,r\,dr\,d\theta\\&=\int_{0}^{\pi}\int_{0}^{4 \sin{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta.\end{aligned}
$$


## Generated easy constant_above radius 4

If $D=\{(x,y)\,:\,x^{2}+(y-4)^{2}\le 16\},$ then $\iint_D 1\,\mathrm{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- $\int_{0}^{\pi}\int_{0}^{8 \sin{\left(\theta \right)}}1\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{0}^{2 \pi}\int_{0}^{8 \sin{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- *Correct:* $\int_{0}^{\pi}\int_{0}^{8 \sin{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{0}^{\pi}\int_{0}^{- 8 \sin{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{0}^{\pi}\int_{0}^{4}r\,\mathrm{d}r\,\mathrm{d}\theta$

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/7e54a91a5b41bf5538e1-region.png)

Notice that the region $D$ represents the disk of radius $4$ centered at $(0,4).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\cos\theta \\ y=r\sin\theta\end{aligned}
$$

With that in mind, let's now write the $x^{2}+(y-4)^{2}=16$ in polar coordinates:

$$
\begin{aligned}x^{2}+(y-4)^{2}&=16\\(r\cos\theta)^2+(r\sin\theta-4)^2&=16\\r^2\cos^2\theta+r^2\sin^2\theta-8r\sin\theta+16&=16\\r^2(\cos^2\theta+\sin^2\theta)-8r\sin\theta&=0\\r^2-8r\sin\theta&=0\\r(r-8\sin\theta)&=0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire circle, we must have $r=8 \sin{\left(\theta \right)}.$

Now, let's determine the limits for $r$ and $\theta.$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=8 \sin{\left(\theta \right)}$ (at the boundary of the region):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/7e54a91a5b41bf5538e1-radius.png)

Secondly, $\theta$ can vary between $\theta=0$ and $\theta=\pi.$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/7e54a91a5b41bf5538e1-angle.png)

So, in polar coordinates $(r,\theta),$ the region can be expressed as

$$
\Delta=\{(r,\theta)\,:\,0\le r\le 8 \sin{\left(\theta \right)},\,0\le\theta\le \pi\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iint_D 1\,dA&=\iint_\Delta (1)\,r\,dr\,d\theta\\&=\int_{0}^{\pi}\int_{0}^{8 \sin{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta.\end{aligned}
$$


## Generated easy constant_below radius 2

If $D=\{(x,y)\,:\,x^{2}+(y+2)^{2}\le 4\},$ then $\iint_D 1\,\mathrm{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- $\int_{\pi}^{2 \pi}\int_{0}^{- 4 \sin{\left(\theta \right)}}1\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{0}^{2 \pi}\int_{0}^{- 4 \sin{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- *Correct:* $\int_{\pi}^{2 \pi}\int_{0}^{- 4 \sin{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{\pi}^{2 \pi}\int_{0}^{4 \sin{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{\pi}^{2 \pi}\int_{0}^{2}r\,\mathrm{d}r\,\mathrm{d}\theta$

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/7b017b882827b83ea093-region.png)

Notice that the region $D$ represents the disk of radius $2$ centered at $(0,-2).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\cos\theta \\ y=r\sin\theta\end{aligned}
$$

With that in mind, let's now write the $x^{2}+(y+2)^{2}=4$ in polar coordinates:

$$
\begin{aligned}x^{2}+(y+2)^{2}&=4\\(r\cos\theta)^2+(r\sin\theta+2)^2&=4\\r^2\cos^2\theta+r^2\sin^2\theta+4r\sin\theta+4&=4\\r^2(\cos^2\theta+\sin^2\theta)+4r\sin\theta&=0\\r^2+4r\sin\theta&=0\\r(r+4\sin\theta)&=0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire circle, we must have $r=- 4 \sin{\left(\theta \right)}.$

Now, let's determine the limits for $r$ and $\theta.$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=- 4 \sin{\left(\theta \right)}$ (at the boundary of the region):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/7b017b882827b83ea093-radius.png)

Secondly, $\theta$ can vary between $\theta=\pi$ and $\theta=2 \pi.$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/7b017b882827b83ea093-angle.png)

So, in polar coordinates $(r,\theta),$ the region can be expressed as

$$
\Delta=\{(r,\theta)\,:\,0\le r\le - 4 \sin{\left(\theta \right)},\,\pi\le\theta\le 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iint_D 1\,dA&=\iint_\Delta (1)\,r\,dr\,d\theta\\&=\int_{\pi}^{2 \pi}\int_{0}^{- 4 \sin{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta.\end{aligned}
$$


## Generated easy constant_below radius 4

If $D=\{(x,y)\,:\,x^{2}+(y+4)^{2}\le 16\},$ then $\iint_D 1\,\mathrm{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- $\int_{\pi}^{2 \pi}\int_{0}^{- 8 \sin{\left(\theta \right)}}1\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{0}^{2 \pi}\int_{0}^{- 8 \sin{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- *Correct:* $\int_{\pi}^{2 \pi}\int_{0}^{- 8 \sin{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{\pi}^{2 \pi}\int_{0}^{8 \sin{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta$
- $\int_{\pi}^{2 \pi}\int_{0}^{4}r\,\mathrm{d}r\,\mathrm{d}\theta$

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/2250d5e3608b8d4bc67c-region.png)

Notice that the region $D$ represents the disk of radius $4$ centered at $(0,-4).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\cos\theta \\ y=r\sin\theta\end{aligned}
$$

With that in mind, let's now write the $x^{2}+(y+4)^{2}=16$ in polar coordinates:

$$
\begin{aligned}x^{2}+(y+4)^{2}&=16\\(r\cos\theta)^2+(r\sin\theta+4)^2&=16\\r^2\cos^2\theta+r^2\sin^2\theta+8r\sin\theta+16&=16\\r^2(\cos^2\theta+\sin^2\theta)+8r\sin\theta&=0\\r^2+8r\sin\theta&=0\\r(r+8\sin\theta)&=0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire circle, we must have $r=- 8 \sin{\left(\theta \right)}.$

Now, let's determine the limits for $r$ and $\theta.$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=- 8 \sin{\left(\theta \right)}$ (at the boundary of the region):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/2250d5e3608b8d4bc67c-radius.png)

Secondly, $\theta$ can vary between $\theta=\pi$ and $\theta=2 \pi.$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/2250d5e3608b8d4bc67c-angle.png)

So, in polar coordinates $(r,\theta),$ the region can be expressed as

$$
\Delta=\{(r,\theta)\,:\,0\le r\le - 8 \sin{\left(\theta \right)},\,\pi\le\theta\le 2 \pi\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iint_D 1\,dA&=\iint_\Delta (1)\,r\,dr\,d\theta\\&=\int_{\pi}^{2 \pi}\int_{0}^{- 8 \sin{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta.\end{aligned}
$$


## Generated moderate difference radius 3/2

If $D = \{(x, y): (x - \frac{3}{2})^{2} + y^{2} \le \frac{9}{4}\}$, then $∬_(D)(x^{2} - y^{2})dA =$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- $\displaystyle \int_{- π/2}^{π/2}\displaystyle \int_{0}^{\frac{3}{2}}r^{3}drdθ$
- $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{\frac{3}{2}}r^{3}\cos 2θdrdθ$
- $\displaystyle \int_{- π/2}^{π/2}\displaystyle \int_{0}^{3\cos θ}r^{2}\cos 2θdrdθ$
- *Correct:* $\displaystyle \int_{- π/2}^{π/2}\displaystyle \int_{0}^{3\cos θ}r^{3}\cos 2θdrdθ$
- $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{3\cos θ}r^{3}drdθ$

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/b28179cd67405ebf5225-region.png)

Notice that the region $D$ represents the disk of radius $\frac{3}{2}$ centered at $(\frac{3}{2},0).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\cos\theta \\ y=r\sin\theta\end{aligned}
$$

With that in mind, let's now write the $(x-\frac{3}{2})^{2}+y^{2}=\frac{9}{4}$ in polar coordinates:

$$
\begin{aligned}(x-\frac{3}{2})^{2}+y^{2}&=\frac{9}{4}\\(r\cos\theta-\frac{3}{2})^2+(r\sin\theta)^2&=\frac{9}{4}\\r^2\cos^2\theta-3r\cos\theta+\frac{9}{4}+r^2\sin^2\theta&=\frac{9}{4}\\r^2(\cos^2\theta+\sin^2\theta)-3r\cos\theta&=0\\r^2-3r\cos\theta&=0\\r(r-3\cos\theta)&=0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire circle, we must have $r=3 \cos{\left(\theta \right)}.$

Now, let's determine the limits for $r$ and $\theta.$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=3 \cos{\left(\theta \right)}$ (at the boundary of the region):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/b28179cd67405ebf5225-radius.png)

Secondly, $\theta$ can vary between $\theta=- \frac{\pi}{2}$ and $\theta=\frac{\pi}{2}.$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/b28179cd67405ebf5225-angle.png)

So, in polar coordinates $(r,\theta),$ the region can be expressed as

$$
\Delta=\{(r,\theta)\,:\,0\le r\le 3 \cos{\left(\theta \right)},\,- \frac{\pi}{2}\le\theta\le \frac{\pi}{2}\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iint_D x^{2} - y^{2}\,dA&=\iint_\Delta (- r^{2} \sin^{2}{\left(\theta \right)} + r^{2} \cos^{2}{\left(\theta \right)})\,r\,dr\,d\theta\\&=\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\int_{0}^{3 \cos{\left(\theta \right)}}r^3(\cos^2\theta-\sin^2\theta)\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\int_{0}^{3 \cos{\left(\theta \right)}}r^{3} \cos{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta.\end{aligned}
$$


## Generated moderate difference radius 5/2

If $D = \{(x, y): (x - \frac{5}{2})^{2} + y^{2} \le \frac{25}{4}\}$, then $∬_(D)(x^{2} - y^{2})dA =$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- $\displaystyle \int_{- π/2}^{π/2}\displaystyle \int_{0}^{\frac{5}{2}}r^{3}drdθ$
- $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{\frac{5}{2}}r^{3}\cos 2θdrdθ$
- $\displaystyle \int_{- π/2}^{π/2}\displaystyle \int_{0}^{5\cos θ}r^{2}\cos 2θdrdθ$
- *Correct:* $\displaystyle \int_{- π/2}^{π/2}\displaystyle \int_{0}^{5\cos θ}r^{3}\cos 2θdrdθ$
- $\displaystyle \int_{0}^{2π}\displaystyle \int_{0}^{5\cos θ}r^{3}drdθ$

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/6177a7444d39477ea588-region.png)

Notice that the region $D$ represents the disk of radius $\frac{5}{2}$ centered at $(\frac{5}{2},0).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\cos\theta \\ y=r\sin\theta\end{aligned}
$$

With that in mind, let's now write the $(x-\frac{5}{2})^{2}+y^{2}=\frac{25}{4}$ in polar coordinates:

$$
\begin{aligned}(x-\frac{5}{2})^{2}+y^{2}&=\frac{25}{4}\\(r\cos\theta-\frac{5}{2})^2+(r\sin\theta)^2&=\frac{25}{4}\\r^2\cos^2\theta-5r\cos\theta+\frac{25}{4}+r^2\sin^2\theta&=\frac{25}{4}\\r^2(\cos^2\theta+\sin^2\theta)-5r\cos\theta&=0\\r^2-5r\cos\theta&=0\\r(r-5\cos\theta)&=0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire circle, we must have $r=5 \cos{\left(\theta \right)}.$

Now, let's determine the limits for $r$ and $\theta.$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=5 \cos{\left(\theta \right)}$ (at the boundary of the region):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/6177a7444d39477ea588-radius.png)

Secondly, $\theta$ can vary between $\theta=- \frac{\pi}{2}$ and $\theta=\frac{\pi}{2}.$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/6177a7444d39477ea588-angle.png)

So, in polar coordinates $(r,\theta),$ the region can be expressed as

$$
\Delta=\{(r,\theta)\,:\,0\le r\le 5 \cos{\left(\theta \right)},\,- \frac{\pi}{2}\le\theta\le \frac{\pi}{2}\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iint_D x^{2} - y^{2}\,dA&=\iint_\Delta (- r^{2} \sin^{2}{\left(\theta \right)} + r^{2} \cos^{2}{\left(\theta \right)})\,r\,dr\,d\theta\\&=\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\int_{0}^{5 \cos{\left(\theta \right)}}r^3(\cos^2\theta-\sin^2\theta)\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}}\int_{0}^{5 \cos{\left(\theta \right)}}r^{3} \cos{\left(2 \theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta.\end{aligned}
$$


## Generated moderate linear radius 3/2

If $D=\{(x,y)\,:\,{x}^{2}+(y-\frac{3}{2})^{2}\le \frac{9}{4}\},$ then ${∬}_{D}x\,\text{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- ${\int }_{0}^{2\pi }{\int }_{0}^{3\operatorname{sin}⁡\theta }{r}^{2}\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- *Correct:* ${\int }_{0}^{\pi }{\int }_{0}^{3\operatorname{sin}⁡\theta }{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{2\pi }{\int }_{0}^{3\operatorname{cos}⁡\theta }r\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{0}^{3\operatorname{cos}⁡\theta }{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{0}^{3\operatorname{sin}⁡\theta }r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\,dr\,d\theta .
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/8ffadd84a24165abf232-region.png)

Notice that the region $D$ represents the disk of radius $\frac{3}{2}$ centered at $(0,\frac{3}{2}).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the ${x}^{2}+(y-\frac{3}{2})^{2}=\frac{9}{4}$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+(y-\frac{3}{2})^{2} & =\frac{9}{4} \\ {(r\operatorname{cos}⁡\theta )}^{2}+{(r\operatorname{sin}⁡\theta -\frac{3}{2})}^{2} & =\frac{9}{4} \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -3r\operatorname{sin}⁡\theta +\frac{9}{4} & =\frac{9}{4} \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-3r\operatorname{sin}⁡\theta  & =0 \\ {r}^{2}-3r\operatorname{sin}⁡\theta  & =0 \\ r(r-3\operatorname{sin}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire circle, we must have $r=3\operatorname{sin}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=3\operatorname{sin}⁡\theta $ (at the boundary of the region): 

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/8ffadd84a24165abf232-radius.png)

Secondly, $\theta $ can vary between $\theta =0$ (the positive $x$-axis) and $\theta =\pi $ (the negative $x$-axis):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/8ffadd84a24165abf232-angle.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 3\operatorname{sin}⁡\theta ,\,0\le \theta \le \pi \}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}x\,\text{d}A & ={∬}_{Δ}r\operatorname{cos}⁡\theta \cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{\pi }{\int }_{0}^{3\operatorname{sin}⁡\theta }{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$


## Generated moderate linear radius 5/2

If $D=\{(x,y)\,:\,{x}^{2}+(y-\frac{5}{2})^{2}\le \frac{25}{4}\},$ then ${∬}_{D}x\,\text{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- ${\int }_{0}^{2\pi }{\int }_{0}^{5\operatorname{sin}⁡\theta }{r}^{2}\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- *Correct:* ${\int }_{0}^{\pi }{\int }_{0}^{5\operatorname{sin}⁡\theta }{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{2\pi }{\int }_{0}^{5\operatorname{cos}⁡\theta }r\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{0}^{5\operatorname{cos}⁡\theta }{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{0}^{5\operatorname{sin}⁡\theta }r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\,dr\,d\theta .
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/ec98187f0ff386ac3d62-region.png)

Notice that the region $D$ represents the disk of radius $\frac{5}{2}$ centered at $(0,\frac{5}{2}).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the ${x}^{2}+(y-\frac{5}{2})^{2}=\frac{25}{4}$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+(y-\frac{5}{2})^{2} & =\frac{25}{4} \\ {(r\operatorname{cos}⁡\theta )}^{2}+{(r\operatorname{sin}⁡\theta -\frac{5}{2})}^{2} & =\frac{25}{4} \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -5r\operatorname{sin}⁡\theta +\frac{25}{4} & =\frac{25}{4} \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-5r\operatorname{sin}⁡\theta  & =0 \\ {r}^{2}-5r\operatorname{sin}⁡\theta  & =0 \\ r(r-5\operatorname{sin}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire circle, we must have $r=5\operatorname{sin}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=5\operatorname{sin}⁡\theta $ (at the boundary of the region): 

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/ec98187f0ff386ac3d62-radius.png)

Secondly, $\theta $ can vary between $\theta =0$ (the positive $x$-axis) and $\theta =\pi $ (the negative $x$-axis):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/ec98187f0ff386ac3d62-angle.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 5\operatorname{sin}⁡\theta ,\,0\le \theta \le \pi \}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}x\,\text{d}A & ={∬}_{Δ}r\operatorname{cos}⁡\theta \cdot r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{\pi }{\int }_{0}^{5\operatorname{sin}⁡\theta }{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$


## Generated moderate x2y radius 3/2

If $D=\{(x,y)\,:\,(x-\frac{3}{2})^{2}+{y}^{2}\le \frac{9}{4}\},$ then ${∬}_{D}{x}^{2}y\,\text{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{\frac{3}{2}}{r}^{3}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{2\pi }{\int }_{0}^{3\operatorname{cos}⁡\theta }{r}^{4}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{2\pi }{\int }_{0}^{\frac{3}{2}}{r}^{4}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{3\operatorname{cos}⁡\theta }{r}^{3}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- *Correct:* ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{3\operatorname{cos}⁡\theta }{r}^{4}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\,dr\,d\theta .
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/b28179cd67405ebf5225-region.png)

Notice that the region $D$ represents the disk of radius $\frac{3}{2}$ centered at $(\frac{3}{2},0).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the $(x-\frac{3}{2})^{2}+{y}^{2}=\frac{9}{4}$ in polar coordinates:

$$
\begin{aligned}(x-\frac{3}{2})^{2}+{y}^{2} & =\frac{9}{4} \\ {(r\operatorname{cos}⁡\theta -\frac{3}{2})}^{2}+{(r\operatorname{sin}⁡\theta )}^{2} & =\frac{9}{4} \\ {r}^{2}{cos}^{2}⁡\theta -3r\operatorname{cos}⁡\theta +\frac{9}{4}+{r}^{2}{sin}^{2}⁡\theta  & =\frac{9}{4} \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-3r\operatorname{cos}⁡\theta  & =0 \\ {r}^{2}-3r\operatorname{cos}⁡\theta  & =0 \\ r(r-3\operatorname{cos}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire circle, we must have $r=3\operatorname{cos}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=3\operatorname{cos}⁡\theta $ (at the boundary of the region): 

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/b28179cd67405ebf5225-radius.png)

Secondly, $\theta $ can vary between $\theta =-\frac{\pi }{2}$ (the negative $y$-axis) and $\theta =\frac{\pi }{2}$ (the positive $y$-axis):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/b28179cd67405ebf5225-angle.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 3\operatorname{cos}⁡\theta ,\,-\frac{\pi }{2}\le \theta \le \frac{\pi }{2}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}{x}^{2}y\,\text{d}A & ={∬}_{Δ}(r\operatorname{cos}⁡\theta )^{2}(r\operatorname{sin}⁡\theta )\,r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{3\operatorname{cos}⁡\theta }{r}^{4}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$


## Generated moderate x2y radius 5/2

If $D=\{(x,y)\,:\,(x-\frac{5}{2})^{2}+{y}^{2}\le \frac{25}{4}\},$ then ${∬}_{D}{x}^{2}y\,\text{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{\frac{5}{2}}{r}^{3}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{2\pi }{\int }_{0}^{5\operatorname{cos}⁡\theta }{r}^{4}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{2\pi }{\int }_{0}^{\frac{5}{2}}{r}^{4}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{5\operatorname{cos}⁡\theta }{r}^{3}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- *Correct:* ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{5\operatorname{cos}⁡\theta }{r}^{4}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\,dr\,d\theta .
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/6177a7444d39477ea588-region.png)

Notice that the region $D$ represents the disk of radius $\frac{5}{2}$ centered at $(\frac{5}{2},0).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the $(x-\frac{5}{2})^{2}+{y}^{2}=\frac{25}{4}$ in polar coordinates:

$$
\begin{aligned}(x-\frac{5}{2})^{2}+{y}^{2} & =\frac{25}{4} \\ {(r\operatorname{cos}⁡\theta -\frac{5}{2})}^{2}+{(r\operatorname{sin}⁡\theta )}^{2} & =\frac{25}{4} \\ {r}^{2}{cos}^{2}⁡\theta -5r\operatorname{cos}⁡\theta +\frac{25}{4}+{r}^{2}{sin}^{2}⁡\theta  & =\frac{25}{4} \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-5r\operatorname{cos}⁡\theta  & =0 \\ {r}^{2}-5r\operatorname{cos}⁡\theta  & =0 \\ r(r-5\operatorname{cos}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire circle, we must have $r=5\operatorname{cos}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=5\operatorname{cos}⁡\theta $ (at the boundary of the region): 

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/6177a7444d39477ea588-radius.png)

Secondly, $\theta $ can vary between $\theta =-\frac{\pi }{2}$ (the negative $y$-axis) and $\theta =\frac{\pi }{2}$ (the positive $y$-axis):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/6177a7444d39477ea588-angle.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 5\operatorname{cos}⁡\theta ,\,-\frac{\pi }{2}\le \theta \le \frac{\pi }{2}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}{x}^{2}y\,\text{d}A & ={∬}_{Δ}(r\operatorname{cos}⁡\theta )^{2}(r\operatorname{sin}⁡\theta )\,r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{5\operatorname{cos}⁡\theta }{r}^{4}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$


## Generated hard xsqrt radius 3/2

If $D = \{(x, y): (x - \frac{3}{2})^{2} + y^{2} \le \frac{9}{4}, y \ge 0\}$, then $∬_(D)x\sqrt{x^{2} + y^{2}}dA =$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- $\displaystyle \int_{0}^{π}\cos θ\displaystyle \int_{0}^{3\cos θ}r^{2}drdθ$
- $\displaystyle \int_{0}^{π/2}\cos θ\displaystyle \int_{0}^{\frac{3}{2}}rdrdθ$
- $\displaystyle \int_{0}^{π}\cos θ\displaystyle \int_{0}^{3\cos θ}r^{3}drdθ$
- *Correct:* $\displaystyle \int_{0}^{π/2}\cos θ\displaystyle \int_{0}^{3\cos θ}r^{3}drdθ$
- $\displaystyle \int_{0}^{π/2}\cos θ\displaystyle \int_{0}^{\frac{3}{2}}r^{2}drdθ$

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/3d52dcdd0aad08aee991-region.png)

Notice that the region $D$ represents a portion of the disk of radius $\frac{3}{2}$ centered at $(\frac{3}{2},0).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\cos\theta \\ y=r\sin\theta\end{aligned}
$$

With that in mind, let's now write the $(x-\frac{3}{2})^{2}+y^{2}=\frac{9}{4}$ in polar coordinates:

$$
\begin{aligned}(x-\frac{3}{2})^{2}+y^{2}&=\frac{9}{4}\\(r\cos\theta-\frac{3}{2})^2+(r\sin\theta)^2&=\frac{9}{4}\\r^2\cos^2\theta-3r\cos\theta+\frac{9}{4}+r^2\sin^2\theta&=\frac{9}{4}\\r^2(\cos^2\theta+\sin^2\theta)-3r\cos\theta&=0\\r^2-3r\cos\theta&=0\\r(r-3\cos\theta)&=0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=3 \cos{\left(\theta \right)}.$

Now, let's determine the limits for $r$ and $\theta.$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=3 \cos{\left(\theta \right)}$ (at the boundary of the region):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/3d52dcdd0aad08aee991-radius.png)

Secondly, $\theta$ can vary between $\theta=0$ and $\theta=\frac{\pi}{2}.$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/3d52dcdd0aad08aee991-angle.png)

So, in polar coordinates $(r,\theta),$ the region can be expressed as

$$
\Delta=\{(r,\theta)\,:\,0\le r\le 3 \cos{\left(\theta \right)},\,0\le\theta\le \frac{\pi}{2}\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iint_D x \sqrt{x^{2} + y^{2}}\,dA&=\iint_\Delta (r \sqrt{r^{2} \sin^{2}{\left(\theta \right)} + r^{2} \cos^{2}{\left(\theta \right)}} \cos{\left(\theta \right)})\,r\,dr\,d\theta\\&=\int_{0}^{\frac{\pi}{2}}\int_{0}^{3 \cos{\left(\theta \right)}}r^2\cos\theta\sqrt{r^2(\cos^2\theta+\sin^2\theta)}\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}\int_{0}^{3 \cos{\left(\theta \right)}}r^3\cos\theta\sqrt{\cos^2\theta+\sin^2\theta}\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}\int_{0}^{3 \cos{\left(\theta \right)}}r^{3} \cos{\left(\theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta.\end{aligned}
$$


## Generated hard xsqrt radius 5/2

If $D = \{(x, y): (x - \frac{5}{2})^{2} + y^{2} \le \frac{25}{4}, y \ge 0\}$, then $∬_(D)x\sqrt{x^{2} + y^{2}}dA =$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- $\displaystyle \int_{0}^{π}\cos θ\displaystyle \int_{0}^{5\cos θ}r^{2}drdθ$
- $\displaystyle \int_{0}^{π/2}\cos θ\displaystyle \int_{0}^{\frac{5}{2}}rdrdθ$
- $\displaystyle \int_{0}^{π}\cos θ\displaystyle \int_{0}^{5\cos θ}r^{3}drdθ$
- *Correct:* $\displaystyle \int_{0}^{π/2}\cos θ\displaystyle \int_{0}^{5\cos θ}r^{3}drdθ$
- $\displaystyle \int_{0}^{π/2}\cos θ\displaystyle \int_{0}^{\frac{5}{2}}r^{2}drdθ$

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,dr\,d\theta.
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/2f9d58ac8c450eadffee-region.png)

Notice that the region $D$ represents a portion of the disk of radius $\frac{5}{2}$ centered at $(\frac{5}{2},0).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\cos\theta \\ y=r\sin\theta\end{aligned}
$$

With that in mind, let's now write the $(x-\frac{5}{2})^{2}+y^{2}=\frac{25}{4}$ in polar coordinates:

$$
\begin{aligned}(x-\frac{5}{2})^{2}+y^{2}&=\frac{25}{4}\\(r\cos\theta-\frac{5}{2})^2+(r\sin\theta)^2&=\frac{25}{4}\\r^2\cos^2\theta-5r\cos\theta+\frac{25}{4}+r^2\sin^2\theta&=\frac{25}{4}\\r^2(\cos^2\theta+\sin^2\theta)-5r\cos\theta&=0\\r^2-5r\cos\theta&=0\\r(r-5\cos\theta)&=0\end{aligned}
$$

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=5 \cos{\left(\theta \right)}.$

Now, let's determine the limits for $r$ and $\theta.$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=5 \cos{\left(\theta \right)}$ (at the boundary of the region):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/2f9d58ac8c450eadffee-radius.png)

Secondly, $\theta$ can vary between $\theta=0$ and $\theta=\frac{\pi}{2}.$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/2f9d58ac8c450eadffee-angle.png)

So, in polar coordinates $(r,\theta),$ the region can be expressed as

$$
\Delta=\{(r,\theta)\,:\,0\le r\le 5 \cos{\left(\theta \right)},\,0\le\theta\le \frac{\pi}{2}\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iint_D x \sqrt{x^{2} + y^{2}}\,dA&=\iint_\Delta (r \sqrt{r^{2} \sin^{2}{\left(\theta \right)} + r^{2} \cos^{2}{\left(\theta \right)}} \cos{\left(\theta \right)})\,r\,dr\,d\theta\\&=\int_{0}^{\frac{\pi}{2}}\int_{0}^{5 \cos{\left(\theta \right)}}r^2\cos\theta\sqrt{r^2(\cos^2\theta+\sin^2\theta)}\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}\int_{0}^{5 \cos{\left(\theta \right)}}r^3\cos\theta\sqrt{\cos^2\theta+\sin^2\theta}\,\mathrm{d}r\,\mathrm{d}\theta\\&=\int_{0}^{\frac{\pi}{2}}\int_{0}^{5 \cos{\left(\theta \right)}}r^{3} \cos{\left(\theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta.\end{aligned}
$$


## Generated hard expdiff radius 3/2

If $D=\{(x,y)\,:\,(x-\frac{3}{2})^{2}+{y}^{2}\le \frac{9}{4},\,y\le 0\},$ then ${∬}_{D}{e}^{{x}^{2}-{y}^{2}}\,\text{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- ${\int }_{3\pi /2}^{2\pi }{\int }_{0}^{\frac{3}{2}}r{e}^{{r}^{2}\operatorname{cos}⁡2\theta }\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{2\pi }{\int }_{0}^{3\operatorname{cos}⁡\theta }{e}^{{r}^{2}\operatorname{cos}⁡2\theta }\,\text{d}r\,\text{d}\theta $
- *Correct:* ${\int }_{3\pi /2}^{2\pi }{\int }_{0}^{3\operatorname{cos}⁡\theta }r{e}^{{r}^{2}\operatorname{cos}⁡2\theta }\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{2\pi }{\int }_{0}^{\frac{3}{2}}r{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $
- ${\int }_{3\pi /2}^{2\pi }{\int }_{0}^{3\operatorname{cos}⁡\theta }{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\,dr\,d\theta .
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/900ae26817f289c9cf87-region.png)

Notice that the region $D$ represents a portion of the disk of radius $\frac{3}{2}$ centered at $(\frac{3}{2},0).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the $(x-\frac{3}{2})^{2}+{y}^{2}=\frac{9}{4}$ in polar coordinates:

$$
\begin{aligned}(x-\frac{3}{2})^{2}+{y}^{2} & =\frac{9}{4} \\ {(r\operatorname{cos}⁡\theta -\frac{3}{2})}^{2}+{(r\operatorname{sin}⁡\theta )}^{2} & =\frac{9}{4} \\ {r}^{2}{cos}^{2}⁡\theta -3r\operatorname{cos}⁡\theta +\frac{9}{4}+{r}^{2}{sin}^{2}⁡\theta  & =\frac{9}{4} \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-3r\operatorname{cos}⁡\theta  & =0 \\ {r}^{2}-3r\operatorname{cos}⁡\theta  & =0 \\ r(r-3\operatorname{cos}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire circle, we must have $r=3\operatorname{cos}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=3\operatorname{cos}⁡\theta $ (at the boundary of the region): 

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/900ae26817f289c9cf87-radius.png)

Secondly, $\theta $ can vary between $\theta =-\frac{\pi }{2}$ (the negative $y$-axis) and $\theta =0$ (the positive $x$-axis):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/900ae26817f289c9cf87-angle.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 3\operatorname{cos}⁡\theta ,\,\frac{3\pi }{2}\le \theta \le 2\pi \}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}{e}^{{x}^{2}-{y}^{2}}\,\text{d}A & ={∬}_{Δ}{e}^{{x}^{2}-{y}^{2}}\,r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{3\pi /2}^{2\pi }{\int }_{0}^{3\operatorname{cos}⁡\theta }r{e}^{{r}^{2}{cos}^{2}⁡\theta -{r}^{2}{sin}^{2}⁡\theta }\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{3\pi /2}^{2\pi }{\int }_{0}^{3\operatorname{cos}⁡\theta }r{e}^{{r}^{2}({cos}^{2}⁡\theta -{sin}^{2}⁡\theta )}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{3\pi /2}^{2\pi }{\int }_{0}^{3\operatorname{cos}⁡\theta }r{e}^{{r}^{2}\operatorname{cos}⁡2\theta }\,\text{d}r\,\text{d}\theta .\end{aligned}
$$


## Generated hard expdiff radius 5/2

If $D=\{(x,y)\,:\,(x-\frac{5}{2})^{2}+{y}^{2}\le \frac{25}{4},\,y\le 0\},$ then ${∬}_{D}{e}^{{x}^{2}-{y}^{2}}\,\text{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- ${\int }_{3\pi /2}^{2\pi }{\int }_{0}^{\frac{5}{2}}r{e}^{{r}^{2}\operatorname{cos}⁡2\theta }\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{2\pi }{\int }_{0}^{5\operatorname{cos}⁡\theta }{e}^{{r}^{2}\operatorname{cos}⁡2\theta }\,\text{d}r\,\text{d}\theta $
- *Correct:* ${\int }_{3\pi /2}^{2\pi }{\int }_{0}^{5\operatorname{cos}⁡\theta }r{e}^{{r}^{2}\operatorname{cos}⁡2\theta }\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{2\pi }{\int }_{0}^{\frac{5}{2}}r{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $
- ${\int }_{3\pi /2}^{2\pi }{\int }_{0}^{5\operatorname{cos}⁡\theta }{e}^{{r}^{2}}\,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\,dA={∬}_{Δ}\,f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\,dr\,d\theta .
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/209968c9a524c710b8e6-region.png)

Notice that the region $D$ represents a portion of the disk of radius $\frac{5}{2}$ centered at $(\frac{5}{2},0).$

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the $(x-\frac{5}{2})^{2}+{y}^{2}=\frac{25}{4}$ in polar coordinates:

$$
\begin{aligned}(x-\frac{5}{2})^{2}+{y}^{2} & =\frac{25}{4} \\ {(r\operatorname{cos}⁡\theta -\frac{5}{2})}^{2}+{(r\operatorname{sin}⁡\theta )}^{2} & =\frac{25}{4} \\ {r}^{2}{cos}^{2}⁡\theta -5r\operatorname{cos}⁡\theta +\frac{25}{4}+{r}^{2}{sin}^{2}⁡\theta  & =\frac{25}{4} \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-5r\operatorname{cos}⁡\theta  & =0 \\ {r}^{2}-5r\operatorname{cos}⁡\theta  & =0 \\ r(r-5\operatorname{cos}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire circle, we must have $r=5\operatorname{cos}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=5\operatorname{cos}⁡\theta $ (at the boundary of the region): 

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/209968c9a524c710b8e6-radius.png)

Secondly, $\theta $ can vary between $\theta =-\frac{\pi }{2}$ (the negative $y$-axis) and $\theta =0$ (the positive $x$-axis):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/209968c9a524c710b8e6-angle.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 5\operatorname{cos}⁡\theta ,\,\frac{3\pi }{2}\le \theta \le 2\pi \}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}{e}^{{x}^{2}-{y}^{2}}\,\text{d}A & ={∬}_{Δ}{e}^{{x}^{2}-{y}^{2}}\,r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{3\pi /2}^{2\pi }{\int }_{0}^{5\operatorname{cos}⁡\theta }r{e}^{{r}^{2}{cos}^{2}⁡\theta -{r}^{2}{sin}^{2}⁡\theta }\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{3\pi /2}^{2\pi }{\int }_{0}^{5\operatorname{cos}⁡\theta }r{e}^{{r}^{2}({cos}^{2}⁡\theta -{sin}^{2}⁡\theta )}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{3\pi /2}^{2\pi }{\int }_{0}^{5\operatorname{cos}⁡\theta }r{e}^{{r}^{2}\operatorname{cos}⁡2\theta }\,\text{d}r\,\text{d}\theta .\end{aligned}
$$


## Generated hard sqrt radius 3/2

If $D=\{(x,y)\,:\,{x}^{2}+(y-\frac{3}{2})^{2}\le \frac{9}{4},\,x\ge 0\},$ then ${∬}_{D}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- ${\int }_{0}^{\pi }{\int }_{0}^{3\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi /2}{\int }_{0}^{\frac{3}{2}\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi /2}{\int }_{0}^{3\operatorname{sin}⁡\theta }r\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{0}^{\frac{3}{2}\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta $
- *Correct:* ${\int }_{0}^{\pi /2}{\int }_{0}^{3\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/9440477802ab376051c1-region.png)

Notice that the region $D$ represents a portion of the disk of radius $\frac{3}{2}$ centered at $(0,\frac{3}{2}).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the ${x}^{2}+(y-\frac{3}{2})^{2}=\frac{9}{4}$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+(y-\frac{3}{2})^{2} & =\frac{9}{4} \\ (r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta -\frac{3}{2})^{2} & =\frac{9}{4} \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -3r\operatorname{sin}⁡\theta +\frac{9}{4} & =\frac{9}{4} \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-3r\operatorname{sin}⁡\theta  & =0 \\ {r}^{2}-3r\operatorname{sin}⁡\theta  & =0 \\ r(r-3\operatorname{sin}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=3\operatorname{sin}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=3\operatorname{sin}⁡\theta $ (at the boundary of the region): 

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/9440477802ab376051c1-radius.png)

Secondly, $\theta $ can vary between $\theta =0$ (the positive $x$-axis) and $\theta =\frac{\pi }{2}$ (the positive $y$-axis):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/9440477802ab376051c1-angle.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 3\operatorname{sin}⁡\theta ,\,0\le \theta \le \frac{\pi }{2}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}A & ={∬}_{Δ}\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}{\int }_{0}^{3\operatorname{sin}⁡\theta }\sqrt{{r}^{2}}\,r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}{\int }_{0}^{3\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$


## Generated hard sqrt radius 5/2

If $D=\{(x,y)\,:\,{x}^{2}+(y-\frac{5}{2})^{2}\le \frac{25}{4},\,x\ge 0\},$ then ${∬}_{D}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- ${\int }_{0}^{\pi }{\int }_{0}^{5\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi /2}{\int }_{0}^{\frac{5}{2}\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi /2}{\int }_{0}^{5\operatorname{sin}⁡\theta }r\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{0}^{\frac{5}{2}\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta $
- *Correct:* ${\int }_{0}^{\pi /2}{\int }_{0}^{5\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/f9f68f7148a138aa3cea-region.png)

Notice that the region $D$ represents a portion of the disk of radius $\frac{5}{2}$ centered at $(0,\frac{5}{2}).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the ${x}^{2}+(y-\frac{5}{2})^{2}=\frac{25}{4}$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+(y-\frac{5}{2})^{2} & =\frac{25}{4} \\ (r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta -\frac{5}{2})^{2} & =\frac{25}{4} \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -5r\operatorname{sin}⁡\theta +\frac{25}{4} & =\frac{25}{4} \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-5r\operatorname{sin}⁡\theta  & =0 \\ {r}^{2}-5r\operatorname{sin}⁡\theta  & =0 \\ r(r-5\operatorname{sin}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=5\operatorname{sin}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=5\operatorname{sin}⁡\theta $ (at the boundary of the region): 

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/f9f68f7148a138aa3cea-radius.png)

Secondly, $\theta $ can vary between $\theta =0$ (the positive $x$-axis) and $\theta =\frac{\pi }{2}$ (the positive $y$-axis):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/f9f68f7148a138aa3cea-angle.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 5\operatorname{sin}⁡\theta ,\,0\le \theta \le \frac{\pi }{2}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}A & ={∬}_{Δ}\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}{\int }_{0}^{5\operatorname{sin}⁡\theta }\sqrt{{r}^{2}}\,r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}{\int }_{0}^{5\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$


## Generated hard xy2 radius 3/2

If $D=\{(x,y)\,:\,(x+\frac{3}{2})^{2}+{y}^{2}\le \frac{9}{4},\,y\le 0\},$ then ${∬}_{D}x{y}^{2}\,\text{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- ${\int }_{0}^{\pi }{\int }_{3\operatorname{sec}⁡\theta }^{6\operatorname{sin}⁡\theta }{r}^{3}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi /2}{\int }_{3}^{-3\operatorname{cos}⁡\theta }{r}^{2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi /2}{\int }_{3}^{6\operatorname{sin}⁡\theta }{r}^{4}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $
- *Correct:* ${\int }_{\pi }^{3\pi /2}{\int }_{0}^{-3\operatorname{cos}⁡\theta }{r}^{4}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{0}^{3\operatorname{sin}⁡\theta }{r}^{4}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/71fc634dbeca98109737-region.png)

Notice that the region $D$ represents a portion of the disk of radius $\frac{3}{2}$ centered at $(-\frac{3}{2},0).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the ${(x+\frac{3}{2})}^{2}+{y}^{2}=\frac{9}{4}$ in polar coordinates:

$$
\begin{aligned}{(x+\frac{3}{2})}^{2}+{y}^{2} & =\frac{9}{4} \\ {(r\operatorname{cos}⁡\theta +\frac{3}{2})}^{2}+(r\operatorname{sin}⁡\theta )^{2} & =\frac{9}{4} \\ {r}^{2}{cos}^{2}⁡\theta +3r\operatorname{cos}⁡\theta +\frac{9}{4}+{r}^{2}{sin}^{2}⁡\theta  & =\frac{9}{4} \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+3r\operatorname{cos}⁡\theta  & =0 \\ {r}^{2}+3r\operatorname{cos}⁡\theta  & =0 \\ r(r+3\operatorname{cos}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=-3\operatorname{cos}⁡\theta .$ 

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=-3\operatorname{cos}⁡\theta $ (at the boundary of the region): 

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/71fc634dbeca98109737-radius.png)

Secondly, $\theta $ can vary between $\theta =\pi $ (the negative $x$-axis) and $\theta =\frac{3\pi }{2}$ (the negative $y$-axis):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/71fc634dbeca98109737-angle.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le -3\operatorname{cos}⁡\theta ,\,\pi \le \theta \le \frac{3\pi }{2}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}x{y}^{2}\,\text{d}A & ={∬}_{Δ}(r\operatorname{cos}⁡\theta )(r\operatorname{sin}⁡\theta )^{2}\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{\pi }^{3\pi /2}{\int }_{0}^{-3\operatorname{cos}⁡\theta }{r}^{4}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$


## Generated hard xy2 radius 5/2

If $D=\{(x,y)\,:\,(x+\frac{5}{2})^{2}+{y}^{2}\le \frac{25}{4},\,y\le 0\},$ then ${∬}_{D}x{y}^{2}\,\text{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- ${\int }_{0}^{\pi }{\int }_{5\operatorname{sec}⁡\theta }^{10\operatorname{sin}⁡\theta }{r}^{3}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi /2}{\int }_{5}^{-5\operatorname{cos}⁡\theta }{r}^{2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi /2}{\int }_{5}^{10\operatorname{sin}⁡\theta }{r}^{4}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $
- *Correct:* ${\int }_{\pi }^{3\pi /2}{\int }_{0}^{-5\operatorname{cos}⁡\theta }{r}^{4}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi }{\int }_{0}^{5\operatorname{sin}⁡\theta }{r}^{4}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/bd1d8e6664a2927470c8-region.png)

Notice that the region $D$ represents a portion of the disk of radius $\frac{5}{2}$ centered at $(-\frac{5}{2},0).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the ${(x+\frac{5}{2})}^{2}+{y}^{2}=\frac{25}{4}$ in polar coordinates:

$$
\begin{aligned}{(x+\frac{5}{2})}^{2}+{y}^{2} & =\frac{25}{4} \\ {(r\operatorname{cos}⁡\theta +\frac{5}{2})}^{2}+(r\operatorname{sin}⁡\theta )^{2} & =\frac{25}{4} \\ {r}^{2}{cos}^{2}⁡\theta +5r\operatorname{cos}⁡\theta +\frac{25}{4}+{r}^{2}{sin}^{2}⁡\theta  & =\frac{25}{4} \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+5r\operatorname{cos}⁡\theta  & =0 \\ {r}^{2}+5r\operatorname{cos}⁡\theta  & =0 \\ r(r+5\operatorname{cos}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=-5\operatorname{cos}⁡\theta .$ 

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=-5\operatorname{cos}⁡\theta $ (at the boundary of the region): 

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/bd1d8e6664a2927470c8-radius.png)

Secondly, $\theta $ can vary between $\theta =\pi $ (the negative $x$-axis) and $\theta =\frac{3\pi }{2}$ (the negative $y$-axis):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/bd1d8e6664a2927470c8-angle.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le -5\operatorname{cos}⁡\theta ,\,\pi \le \theta \le \frac{3\pi }{2}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}x{y}^{2}\,\text{d}A & ={∬}_{Δ}(r\operatorname{cos}⁡\theta )(r\operatorname{sin}⁡\theta )^{2}\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{\pi }^{3\pi /2}{\int }_{0}^{-5\operatorname{cos}⁡\theta }{r}^{4}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta .\end{aligned}
$$


## Generated hard radial2 radius 3/2

If $D=\{(x,y)\,:\,{x}^{2}+{(y-\frac{3}{2})}^{2}\le \frac{9}{4},\,x\le 0\},$ then ${∬}_{D}({x}^{2}+{y}^{2})\,\text{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- ${\int }_{0}^{\pi }{\int }_{0}^{3\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $
- ${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{3\operatorname{sin}⁡\theta }r\,\text{d}r\,\text{d}\theta $
- *Correct:* ${\int }_{\pi /2}^{\pi }{\int }_{0}^{3\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta $
- ${\int }_{\pi }^{2\pi }{\int }_{0}^{3\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $
- ${\int }_{-\pi /2}^{\pi }{\int }_{0}^{3\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/50667948644cf065158a-region.png)

Notice that the region $D$ represents a portion of the disk of radius $\frac{3}{2}$ centered at $(0,\frac{3}{2}).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the ${x}^{2}+{(y-\frac{3}{2})}^{2}=\frac{9}{4}$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+{(y-\frac{3}{2})}^{2} & =\frac{9}{4} \\ (r\operatorname{cos}⁡\theta )^{2}+{(r\operatorname{sin}⁡\theta -\frac{3}{2})}^{2} & =\frac{9}{4} \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -3r\operatorname{sin}⁡\theta +\frac{9}{4} & =\frac{9}{4} \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-3r\operatorname{sin}⁡\theta  & =0 \\ {r}^{2}-3r\operatorname{sin}⁡\theta  & =0 \\ r(r-3\operatorname{sin}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=3\operatorname{sin}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=3\operatorname{sin}⁡\theta $ (at the boundary of the region): 

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/50667948644cf065158a-radius.png)

Secondly, $\theta $ can vary between $\theta =\frac{\pi }{2}$ (the positive $y$-axis) and $\theta =\pi $ (the negative $x$-axis):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/50667948644cf065158a-angle.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 3\operatorname{sin}⁡\theta ,\,\frac{\pi }{2}\le \theta \le \pi \}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}({x}^{2}+{y}^{2})\,\text{d}A & ={∬}_{Δ}((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2})\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{\pi /2}^{\pi }{\int }_{0}^{3\operatorname{sin}⁡\theta }{r}^{3}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{\pi /2}^{\pi }{\int }_{0}^{3\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$


## Generated hard radial2 radius 5/2

If $D=\{(x,y)\,:\,{x}^{2}+{(y-\frac{5}{2})}^{2}\le \frac{25}{4},\,x\le 0\},$ then ${∬}_{D}({x}^{2}+{y}^{2})\,\text{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- ${\int }_{0}^{\pi }{\int }_{0}^{5\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $
- ${\int }_{\pi /2}^{3\pi /2}{\int }_{0}^{5\operatorname{sin}⁡\theta }r\,\text{d}r\,\text{d}\theta $
- *Correct:* ${\int }_{\pi /2}^{\pi }{\int }_{0}^{5\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta $
- ${\int }_{\pi }^{2\pi }{\int }_{0}^{5\operatorname{sin}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta $
- ${\int }_{-\pi /2}^{\pi }{\int }_{0}^{5\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/cd529289c4a1300ed05b-region.png)

Notice that the region $D$ represents a portion of the disk of radius $\frac{5}{2}$ centered at $(0,\frac{5}{2}).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the ${x}^{2}+{(y-\frac{5}{2})}^{2}=\frac{25}{4}$ in polar coordinates:

$$
\begin{aligned}{x}^{2}+{(y-\frac{5}{2})}^{2} & =\frac{25}{4} \\ (r\operatorname{cos}⁡\theta )^{2}+{(r\operatorname{sin}⁡\theta -\frac{5}{2})}^{2} & =\frac{25}{4} \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -5r\operatorname{sin}⁡\theta +\frac{25}{4} & =\frac{25}{4} \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-5r\operatorname{sin}⁡\theta  & =0 \\ {r}^{2}-5r\operatorname{sin}⁡\theta  & =0 \\ r(r-5\operatorname{sin}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=5\operatorname{sin}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=5\operatorname{sin}⁡\theta $ (at the boundary of the region): 

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/cd529289c4a1300ed05b-radius.png)

Secondly, $\theta $ can vary between $\theta =\frac{\pi }{2}$ (the positive $y$-axis) and $\theta =\pi $ (the negative $x$-axis):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/cd529289c4a1300ed05b-angle.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 5\operatorname{sin}⁡\theta ,\,\frac{\pi }{2}\le \theta \le \pi \}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}({x}^{2}+{y}^{2})\,\text{d}A & ={∬}_{Δ}((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2})\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{\pi /2}^{\pi }{\int }_{0}^{5\operatorname{sin}⁡\theta }{r}^{3}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{\pi /2}^{\pi }{\int }_{0}^{5\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$


## Generated hard log radius 3/2

If $D=\{(x,y)\,:\,(x-\frac{3}{2})^{2}+{y}^{2}\le \frac{9}{4},\,y\le 0\},$ then ${∬}_{D}\operatorname{ln}⁡({x}^{2}+{y}^{2}+1)\,\text{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- ${\int }_{0}^{\pi }{\int }_{0}^{\frac{3}{2}\operatorname{cos}⁡\theta }{r}^{2}\operatorname{ln}⁡(r+1)\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi /2}{\int }_{0}^{\frac{3}{2}\operatorname{cos}⁡\theta }\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $
- ${\int }_{-\pi }^{0}{\int }_{0}^{3\operatorname{cos}⁡\theta }2r\operatorname{ln}⁡(r+1)\,\text{d}r\,\text{d}\theta $
- ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{3\operatorname{cos}⁡\theta }r\operatorname{ln}⁡({r}^{2})\,\text{d}r\,\text{d}\theta $
- *Correct:* ${\int }_{-\pi /2}^{0}{\int }_{0}^{3\operatorname{cos}⁡\theta }r\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/900ae26817f289c9cf87-region.png)

Notice that the region $D$ represents a portion of the disk of radius $\frac{3}{2}$ centered at $(\frac{3}{2},0).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the $(x-\frac{3}{2})^{2}+{y}^{2}=\frac{9}{4}$ in polar coordinates:

$$
\begin{aligned}(x-\frac{3}{2})^{2}+{y}^{2} & =\frac{9}{4} \\ (r\operatorname{cos}⁡\theta -\frac{3}{2})^{2}+{(r\operatorname{sin}⁡\theta )}^{2} & =\frac{9}{4} \\ {r}^{2}{cos}^{2}⁡\theta -3r\operatorname{cos}⁡\theta +\frac{9}{4}+{r}^{2}{sin}^{2}⁡\theta  & =\frac{9}{4} \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-3r\operatorname{cos}⁡\theta  & =0 \\ {r}^{2}-3r\operatorname{cos}⁡\theta  & =0 \\ r(r-3\operatorname{cos}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=3\operatorname{cos}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=3\operatorname{cos}⁡\theta $ (at the boundary of the region): 

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/900ae26817f289c9cf87-radius.png)

Secondly, $\theta $ can vary between $\theta =-\frac{\pi }{2}$ (the negative $y$-axis) and $\theta =0$ (the positive $x$-axis):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/900ae26817f289c9cf87-angle.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 3\operatorname{cos}⁡\theta ,\,-\frac{\pi }{2}\le \theta \le 0\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}\operatorname{ln}⁡({x}^{2}+{y}^{2}+1)\,\text{d}A & ={∬}_{Δ}\operatorname{ln}⁡((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}+1)\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{-\pi /2}^{0}{\int }_{0}^{3\operatorname{cos}⁡\theta }r\operatorname{ln}⁡({r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+1)\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{-\pi /2}^{0}{\int }_{0}^{3\operatorname{cos}⁡\theta }r\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta .\end{aligned}
$$


## Generated hard log radius 5/2

If $D=\{(x,y)\,:\,(x-\frac{5}{2})^{2}+{y}^{2}\le \frac{25}{4},\,y\le 0\},$ then ${∬}_{D}\operatorname{ln}⁡({x}^{2}+{y}^{2}+1)\,\text{d}A=$

Choose the polar setup whose bounds describe $D$ with $r\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$

- ${\int }_{0}^{\pi }{\int }_{0}^{\frac{5}{2}\operatorname{cos}⁡\theta }{r}^{2}\operatorname{ln}⁡(r+1)\,\text{d}r\,\text{d}\theta $
- ${\int }_{0}^{\pi /2}{\int }_{0}^{\frac{5}{2}\operatorname{cos}⁡\theta }\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $
- ${\int }_{-\pi }^{0}{\int }_{0}^{5\operatorname{cos}⁡\theta }2r\operatorname{ln}⁡(r+1)\,\text{d}r\,\text{d}\theta $
- ${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{5\operatorname{cos}⁡\theta }r\operatorname{ln}⁡({r}^{2})\,\text{d}r\,\text{d}\theta $
- *Correct:* ${\int }_{-\pi /2}^{0}{\int }_{0}^{5\operatorname{cos}⁡\theta }r\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta $

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

First, let's sketch our region $D:$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/209968c9a524c710b8e6-region.png)

Notice that the region $D$ represents a portion of the disk of radius $\frac{5}{2}$ centered at $(\frac{5}{2},0).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\{\begin{aligned}x=r\operatorname{cos}⁡\theta  \\ y=r\operatorname{sin}⁡\theta \end{aligned}
$$

With that in mind, let's now write the $(x-\frac{5}{2})^{2}+{y}^{2}=\frac{25}{4}$ in polar coordinates:

$$
\begin{aligned}(x-\frac{5}{2})^{2}+{y}^{2} & =\frac{25}{4} \\ (r\operatorname{cos}⁡\theta -\frac{5}{2})^{2}+{(r\operatorname{sin}⁡\theta )}^{2} & =\frac{25}{4} \\ {r}^{2}{cos}^{2}⁡\theta -5r\operatorname{cos}⁡\theta +\frac{25}{4}+{r}^{2}{sin}^{2}⁡\theta  & =\frac{25}{4} \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-5r\operatorname{cos}⁡\theta  & =0 \\ {r}^{2}-5r\operatorname{cos}⁡\theta  & =0 \\ r(r-5\operatorname{cos}⁡\theta ) & =0\end{aligned}
$$

 

Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=5\operatorname{cos}⁡\theta .$

Now, let's determine the limits for $r$ and $\theta .$ First of all, $r$ can vary from $r=0$ (at the origin) to $r=5\operatorname{cos}⁡\theta $ (at the boundary of the region): 

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/209968c9a524c710b8e6-radius.png)

Secondly, $\theta $ can vary between $\theta =-\frac{\pi }{2}$ (the negative $y$-axis) and $\theta =0$ (the positive $x$-axis):

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129275/plots/209968c9a524c710b8e6-angle.png)

So, in polar coordinates $(r,\theta ),$ the region can be expressed as 

$$
Δ=\{(r,\theta )\,:\,0\le r\le 5\operatorname{cos}⁡\theta ,\,-\frac{\pi }{2}\le \theta \le 0\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}\operatorname{ln}⁡({x}^{2}+{y}^{2}+1)\,\text{d}A & ={∬}_{Δ}\operatorname{ln}⁡((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}+1)\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{-\pi /2}^{0}{\int }_{0}^{5\operatorname{cos}⁡\theta }r\operatorname{ln}⁡({r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+1)\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{-\pi /2}^{0}{\int }_{0}^{5\operatorname{cos}⁡\theta }r\operatorname{ln}⁡({r}^{2}+1)\,\text{d}r\,\text{d}\theta .\end{aligned}
$$
