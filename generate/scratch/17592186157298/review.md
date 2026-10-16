# q-83789

## Source

![](images/8b/8b694a0907a5cb1c33d44c921b01b8e351059ce3e695485d79b72051f7ed764a.png)

The region $D$ is enclosed between the curve ${x}^{2}+(y-1)^{2}=1$ and the line $y=1,$ as shown above. What is
${∬}_{D}{y}^{2}\,\text{d}A$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Notice that the region $D$ represents a portion of the disk of radius $1$ centered at $(0,1).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\left\{\begin{aligned}x &=r\operatorname{cos}⁡\theta \\ y &=r\operatorname{sin}⁡\theta\end{aligned}\right.
$$

With that in mind, let's now write our curves in polar coordinates.

- For ${x}^{2}+(y-1)^{2}=1,$ we obtain

$$
\begin{aligned}{x}^{2}+(y-1)^{2} & =1 \\ (r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta -1)^{2} & =1 \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -2r\operatorname{sin}⁡\theta +1 & =1 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-2r\operatorname{sin}⁡\theta  & =0 \\ {r}^{2}-2r\operatorname{sin}⁡\theta  & =0 \\ r(r-2\operatorname{sin}⁡\theta ) & =0.\end{aligned}
$$

 
Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=2\operatorname{sin}⁡\theta .$

- For $y=1,$ we get

$$
\begin{aligned}y & =1 \\ r\operatorname{sin}⁡\theta  & =1 \\ r & =\frac{1}{\operatorname{sin}⁡\theta } \\ r & =\operatorname{csc}⁡\theta .\end{aligned}
$$

Now, let's find the limits for the parameter $\theta .$ Our curves intersect at the points $(-1,1)$ and $(1,1).$ So, the entire region $D$ lies between the polar lines $\theta =\frac{\pi }{4}$ and $\theta =\frac{3\pi }{4},$ as depicted below.  

![](images/68/68f70968b0dd256159dbfdcbfde4f2f63578237db1770e019c8fb19a5a638eaa.png)

As a result, the region can be expressed in polar coordinates $(r,\theta )$ as 

$$
Δ=\{(r,\theta )\,:\,\operatorname{csc}⁡\theta \le r\le 2\operatorname{sin}⁡\theta ,\,\frac{\pi }{4}\le \theta \le \frac{3\pi }{4}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}{y}^{2}\,\text{d}A & ={∬}_{Δ}(r\operatorname{sin}⁡\theta )^{2}\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{\pi /4}^{3\pi /4}{\int }_{\operatorname{csc}⁡\theta }^{2\operatorname{sin}⁡\theta }{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta  \\  & ={\int }_{\pi /4}^{3\pi /4}{sin}^{2}⁡\theta {\int }_{\operatorname{csc}⁡\theta }^{2\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

## Scale 1 replay

![](generate/scratch/17592186157298/assets/289416f3bd1d544810420fa4-prompt.png)

The region $D$ is enclosed between the curve $x^{2} + \left(y - 1\right)^{2}=1$ and the line $y=1$, as shown above. What is
$$\iint_D y^{2}\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $1$ centered at $(0,1)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $x^{2} + \left(y - 1\right)^{2}=1$, we obtain

$$r \left(r - 2 \sin{\left(\theta \right)}\right)=0\quad\Longleftrightarrow\quad r\left(r-\left(2 \sin{\left(\theta \right)}\right)\right)=0.$$

The boundary arc has $r=2 \sin{\left(\theta \right)}$ for $r>0$.

- For $y=1$, we get

$$r \sin{\left(\theta \right)}=1\quad\Longrightarrow\quad r=\frac{1}{\sin{\left(\theta \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(1,1)$ and $(-1,1)$. So the shaded region lies between the polar lines $\theta=\frac{\pi}{4}$ and $\theta=\frac{3 \pi}{4}$.

![](generate/scratch/17592186157298/assets/289416f3bd1d544810420fa4-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):\frac{1}{\sin{\left(\theta \right)}}\leq r\leq 2 \sin{\left(\theta \right)},\ \frac{\pi}{4}\leq\theta\leq \frac{3 \pi}{4}\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D y^{2}\,\mathrm{d}A=\iint_\Delta r^{3} \sin^{2}{\left(\theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{\frac{\pi}{4}}^{\frac{3 \pi}{4}}\left(\sin^{2}{\left(\theta \right)}\right)\int_{\csc{\left(\theta \right)}}^{2 \sin{\left(\theta \right)}}r^{3}\,\mathrm{d}r\,\mathrm{d}\theta.$$

## Scale 3 variant

![](generate/scratch/17592186157298/assets/22608b3c2f0c2c20380d86c2-prompt.png)

The region $D$ is enclosed between the curve $x^{2} + \left(y - 3\right)^{2}=9$ and the line $y=3$, as shown above. What is
$$\iint_D y^{2}\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $3$ centered at $(0,3)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $x^{2} + \left(y - 3\right)^{2}=9$, we obtain

$$r \left(r - 6 \sin{\left(\theta \right)}\right)=0\quad\Longleftrightarrow\quad r\left(r-\left(6 \sin{\left(\theta \right)}\right)\right)=0.$$

The boundary arc has $r=6 \sin{\left(\theta \right)}$ for $r>0$.

- For $y=3$, we get

$$r \sin{\left(\theta \right)}=3\quad\Longrightarrow\quad r=\frac{3}{\sin{\left(\theta \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(3,3)$ and $(-3,3)$. So the shaded region lies between the polar lines $\theta=\frac{\pi}{4}$ and $\theta=\frac{3 \pi}{4}$.

![](generate/scratch/17592186157298/assets/22608b3c2f0c2c20380d86c2-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):\frac{3}{\sin{\left(\theta \right)}}\leq r\leq 6 \sin{\left(\theta \right)},\ \frac{\pi}{4}\leq\theta\leq \frac{3 \pi}{4}\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D y^{2}\,\mathrm{d}A=\iint_\Delta r^{3} \sin^{2}{\left(\theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{\frac{\pi}{4}}^{\frac{3 \pi}{4}}\left(\sin^{2}{\left(\theta \right)}\right)\int_{3 \csc{\left(\theta \right)}}^{6 \sin{\left(\theta \right)}}r^{3}\,\mathrm{d}r\,\mathrm{d}\theta.$$

# q-83980

## Source

![](images/92/928fb72015b78436f95895799c2846d1a0b34242b7216d31a6ed6bdda46728a1.png)

The region $D$ is enclosed between the curve ${x}^{2}+{y}^{2}=16$ and the line $x=2\sqrt{2},$ as shown above. What is
${∬}_{D}\frac{y}{x}\,\text{d}A$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Notice that the region $D$ represents a portion of the disk of radius $4$ centered at $(0,0).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\left\{\begin{aligned}x &=r\operatorname{cos}⁡\theta \\ y &=r\operatorname{sin}⁡\theta\end{aligned}\right.
$$

With that in mind, let's now write our curves in polar coordinates.

- For ${x}^{2}+{y}^{2}=16,$ we obtain $r=4.$

- For $x=2\sqrt{2},$ we get

$$
\begin{aligned}x & =2\sqrt{2} \\ r\operatorname{cos}⁡\theta  & =2\sqrt{2} \\ r & =\frac{2\sqrt{2}}{\operatorname{cos}⁡\theta } \\ r & =2\sqrt{2}\operatorname{sec}⁡\theta .\end{aligned}
$$

Now, let's find the limits for the parameter $\theta .$ Our curves intersect at the point $(2\sqrt{2},2\sqrt{2}).$ So, the entire region $D$ lies between the polar lines $\theta =0$ and $\theta =\frac{\pi }{4},$ as depicted below.  

![](images/37/375e270ce444d9f62b50f9a25abfae781113fdad895833d693061ffffe93f5d3.png)

As a result, the region can be expressed in polar coordinates $(r,\theta )$ as 

$$
Δ=\{(r,\theta )\,:\,2\sqrt{2}\operatorname{sec}⁡\theta \le r\le 4,\,0\le \theta \le \frac{\pi }{4}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}\frac{y}{x}\,\text{d}A & ={∬}_{Δ}\frac{r\operatorname{sin}⁡\theta }{r\operatorname{cos}⁡\theta }\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{0}^{\pi /4}{\int }_{2\sqrt{2}\operatorname{sec}⁡\theta }^{4}r\operatorname{tan}⁡\theta \,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{\pi /4}\operatorname{tan}⁡\theta {\int }_{2\sqrt{2}\operatorname{sec}⁡\theta }^{4}r\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

## Scale 1 replay

![](generate/scratch/17592186157298/assets/f05f4de34187062738d1963e-prompt.png)

The region $D$ is enclosed between the curve $x^{2} + y^{2}=16$ and the line $x=2 \sqrt{2}$, as shown above. What is
$$\iint_D \frac{y}{x}\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $4$ centered at $(0,0)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $x^{2} + y^{2}=16$, we obtain $r=4$.

- For $x=2 \sqrt{2}$, we get

$$r \cos{\left(\theta \right)}=2 \sqrt{2}\quad\Longrightarrow\quad r=\frac{2 \sqrt{2}}{\cos{\left(\theta \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(4,0)$ and $(2 \sqrt{2},2 \sqrt{2})$. So the shaded region lies between the polar lines $\theta=0$ and $\theta=\frac{\pi}{4}$.

![](generate/scratch/17592186157298/assets/f05f4de34187062738d1963e-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):\frac{2 \sqrt{2}}{\cos{\left(\theta \right)}}\leq r\leq 4,\ 0\leq\theta\leq \frac{\pi}{4}\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D \frac{y}{x}\,\mathrm{d}A=\iint_\Delta r \tan{\left(\theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{0}^{\frac{\pi}{4}}\left(\tan{\left(\theta \right)}\right)\int_{2 \sqrt{2} \sec{\left(\theta \right)}}^{4}r\,\mathrm{d}r\,\mathrm{d}\theta.$$

## Scale 3 variant

![](generate/scratch/17592186157298/assets/281bc752fb6f07533b26358c-prompt.png)

The region $D$ is enclosed between the curve $x^{2} + y^{2}=144$ and the line $x=6 \sqrt{2}$, as shown above. What is
$$\iint_D \frac{y}{x}\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $12$ centered at $(0,0)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $x^{2} + y^{2}=144$, we obtain $r=12$.

- For $x=6 \sqrt{2}$, we get

$$r \cos{\left(\theta \right)}=6 \sqrt{2}\quad\Longrightarrow\quad r=\frac{6 \sqrt{2}}{\cos{\left(\theta \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(12,0)$ and $(6 \sqrt{2},6 \sqrt{2})$. So the shaded region lies between the polar lines $\theta=0$ and $\theta=\frac{\pi}{4}$.

![](generate/scratch/17592186157298/assets/281bc752fb6f07533b26358c-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):\frac{6 \sqrt{2}}{\cos{\left(\theta \right)}}\leq r\leq 12,\ 0\leq\theta\leq \frac{\pi}{4}\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D \frac{y}{x}\,\mathrm{d}A=\iint_\Delta r \tan{\left(\theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{0}^{\frac{\pi}{4}}\left(\tan{\left(\theta \right)}\right)\int_{6 \sqrt{2} \sec{\left(\theta \right)}}^{12}r\,\mathrm{d}r\,\mathrm{d}\theta.$$

# q-161101

## Source

![](images/ae/aed70cc2e5495fcfd9f42ff5d79c3371fb17b62e12ab1909c7738071e59f1a23.png)

The region $D$ is enclosed between the curve $(x+1)^{2}+(y-1)^{2}=2$ and the line $y=x+2,$ as shown above. What is
${∬}_{D}xy\,\text{d}A$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Notice that the region $D$ represents a portion of the disk of radius $\sqrt{2}$ centered at $(-1,1).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\left\{\begin{aligned}x &=r\operatorname{cos}⁡\theta \\ y &=r\operatorname{sin}⁡\theta\end{aligned}\right.
$$

With that in mind, let's now write our curves in polar coordinates.

- For $(x+1)^{2}+(y-1)^{2}=2,$ we obtain

$$
\begin{aligned}(x+1)^{2}+(y-1)^{2} & =2 \\ (r\operatorname{cos}⁡\theta +1)^{2}+(r\operatorname{sin}⁡\theta -1)^{2} & =2 \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta +2r\operatorname{cos}⁡\theta -2r\operatorname{sin}⁡\theta +2 & =2 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-2r(\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta ) & =0 \\ {r}^{2}-2r(\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta ) & =0 \\ r(r-2(\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta )) & =0.\end{aligned}
$$

 
Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=2(\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta ).$

- For $y=x+2,$ we get

$$
\begin{aligned}y & =x+2 \\ r\operatorname{sin}⁡\theta  & =r\operatorname{cos}⁡\theta +2 \\ r(\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta ) & =2 \\ r & =\frac{2}{\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta }.\end{aligned}
$$

Now, let's find the limits for the parameter $\theta .$ Our curves intersect at the points $(-2,0)$ and $(0,2).$ So, the entire region $D$ lies between the polar lines $\theta =\frac{\pi }{2}$ and $\theta =\pi ,$ as depicted below.  

![](images/b9/b9c2cd48302ef8d4e2d5e65a56d19506600c5e6552a4d9a1ef7d578a09a21557.png)

As a result, the region can be expressed in polar coordinates $(r,\theta )$ as 

$$
Δ={(r,\theta )\,:\,\frac{2}{\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta }\le r\le 2(\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta ),\,\frac{\pi }{2}\le \theta \le \pi }.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}xy\,\text{d}A & ={∬}_{Δ}{r}^{2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \cdot r\,\text{d}r\text{d}\theta  \\  & ={\int }_{\pi /2}^{\pi }{\int }_{2/(\operatorname{sin}⁡\theta -\operatorname{sin}⁡\theta )}^{2(\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta )}{r}^{3}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta  \\  & ={\int }_{\pi /2}^{\pi }\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta {\int }_{2/(\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta )}^{2(\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta )}{r}^{3}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

## Scale 1 replay

![](generate/scratch/17592186157298/assets/4ff37cb219bdce632f16d0f7-prompt.png)

The region $D$ is enclosed between the curve $\left(x + 1\right)^{2} + \left(y - 1\right)^{2}=2$ and the line $- x + y=2$, as shown above. What is
$$\iint_D x y\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $\sqrt{2}$ centered at $(-1,1)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $\left(x + 1\right)^{2} + \left(y - 1\right)^{2}=2$, we obtain

$$r \left(r + 2 \sqrt{2} \cos{\left(\theta + \frac{\pi}{4} \right)}\right)=0\quad\Longleftrightarrow\quad r\left(r-\left(- 2 \sqrt{2} \cos{\left(\theta + \frac{\pi}{4} \right)}\right)\right)=0.$$

The boundary arc has $r=- 2 \sqrt{2} \cos{\left(\theta + \frac{\pi}{4} \right)}$ for $r>0$.

- For $- x + y=2$, we get

$$r \left(\sin{\left(\theta \right)} - \cos{\left(\theta \right)}\right)=2\quad\Longrightarrow\quad r=\frac{2}{\sin{\left(\theta \right)} - \cos{\left(\theta \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(0,2)$ and $(-2,0)$. So the shaded region lies between the polar lines $\theta=\frac{\pi}{2}$ and $\theta=\pi$.

![](generate/scratch/17592186157298/assets/4ff37cb219bdce632f16d0f7-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):\frac{2}{\sin{\left(\theta \right)} - \cos{\left(\theta \right)}}\leq r\leq - 2 \sqrt{2} \cos{\left(\theta + \frac{\pi}{4} \right)},\ \frac{\pi}{2}\leq\theta\leq \pi\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D x y\,\mathrm{d}A=\iint_\Delta \frac{r^{3} \sin{\left(2 \theta \right)}}{2}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{\frac{\pi}{2}}^{\pi}\left(\frac{\sin{\left(2 \theta \right)}}{2}\right)\int_{\frac{2}{\sin{\left(\theta \right)} - \cos{\left(\theta \right)}}}^{- 2 \sqrt{2} \cos{\left(\theta + \frac{\pi}{4} \right)}}r^{3}\,\mathrm{d}r\,\mathrm{d}\theta.$$

## Scale 3 variant

![](generate/scratch/17592186157298/assets/ea02bd4980bce3d88b504924-prompt.png)

The region $D$ is enclosed between the curve $\left(x + 3\right)^{2} + \left(y - 3\right)^{2}=18$ and the line $- x + y=6$, as shown above. What is
$$\iint_D x y\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $3 \sqrt{2}$ centered at $(-3,3)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $\left(x + 3\right)^{2} + \left(y - 3\right)^{2}=18$, we obtain

$$r \left(r + 6 \sqrt{2} \cos{\left(\theta + \frac{\pi}{4} \right)}\right)=0\quad\Longleftrightarrow\quad r\left(r-\left(- 6 \sqrt{2} \cos{\left(\theta + \frac{\pi}{4} \right)}\right)\right)=0.$$

The boundary arc has $r=- 6 \sqrt{2} \cos{\left(\theta + \frac{\pi}{4} \right)}$ for $r>0$.

- For $- x + y=6$, we get

$$r \left(\sin{\left(\theta \right)} - \cos{\left(\theta \right)}\right)=6\quad\Longrightarrow\quad r=\frac{6}{\sin{\left(\theta \right)} - \cos{\left(\theta \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(0,6)$ and $(-6,0)$. So the shaded region lies between the polar lines $\theta=\frac{\pi}{2}$ and $\theta=\pi$.

![](generate/scratch/17592186157298/assets/ea02bd4980bce3d88b504924-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):\frac{6}{\sin{\left(\theta \right)} - \cos{\left(\theta \right)}}\leq r\leq - 6 \sqrt{2} \cos{\left(\theta + \frac{\pi}{4} \right)},\ \frac{\pi}{2}\leq\theta\leq \pi\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D x y\,\mathrm{d}A=\iint_\Delta \frac{r^{3} \sin{\left(2 \theta \right)}}{2}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{\frac{\pi}{2}}^{\pi}\left(\frac{\sin{\left(2 \theta \right)}}{2}\right)\int_{\frac{6}{\sin{\left(\theta \right)} - \cos{\left(\theta \right)}}}^{- 6 \sqrt{2} \cos{\left(\theta + \frac{\pi}{4} \right)}}r^{3}\,\mathrm{d}r\,\mathrm{d}\theta.$$

# q-85065

## Source

![](images/15/15e58073c87bd249473950680a49e8fc4cb4be94277a7001c0ab9f96ab3a46df.png)

The region $D$ is enclosed between the curve $(x+2)^{2}+{y}^{2}=4$ and the line $x=-3,$ as shown above. What is
${∬}_{D}xy\,\text{d}A$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Notice that the region $D$ represents a portion of the disk of radius $2$ centered at $(-2,0).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\left\{\begin{aligned}x &=r\operatorname{cos}⁡\theta \\ y &=r\operatorname{sin}⁡\theta\end{aligned}\right.
$$

With that in mind, let's now write our curves in polar coordinates.

- For $(x+2)^{2}+{y}^{2}=4,$ we obtain

$$
\begin{aligned}(x+2)^{2}+{y}^{2} & =4 \\ (r\operatorname{cos}⁡\theta +2)^{2}+(r\operatorname{sin}⁡\theta )^{2} & =4 \\ {r}^{2}{cos}^{2}⁡\theta +4r\operatorname{cos}⁡\theta +4+{r}^{2}{sin}^{2}⁡\theta  & =4 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+4r\operatorname{cos}⁡\theta  & =0 \\ {r}^{2}+4r\operatorname{cos}⁡\theta  & =0 \\ r(r+4\operatorname{cos}⁡\theta ) & =0.\end{aligned}
$$

 
Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=-4\operatorname{cos}⁡\theta .$

- For $x=-3,$ we get

$$
\begin{aligned}x & =-3 \\ r\operatorname{cos}⁡\theta  & =-3 \\ r & =-\frac{3}{\operatorname{cos}⁡\theta } \\ r & =-3\operatorname{sec}⁡\theta .\end{aligned}
$$

Now, let's find the limits for the parameter $\theta .$ Our curves intersect at the points $(-3,-\sqrt{3})$ and $(-3,\sqrt{3}).$ So, the entire region $D$ lies between the polar lines $\theta =\frac{5\pi }{6}$ and $\theta =\frac{7\pi }{6},$ as depicted below.  

![](images/92/928c6dc79f44a2185ccf217c0cf9210630b6554a698f805ef2c77500f9ddc76b.png)

As a result, the region can be expressed in polar coordinates $(r,\theta )$ as 

$$
Δ=\{(r,\theta )\,:\,-3\operatorname{sec}⁡\theta \le r\le -4\operatorname{cos}⁡\theta ,\,\frac{5\pi }{6}\le \theta \le \frac{7\pi }{6}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}xy\,\text{d}A & ={∬}_{Δ}(r\operatorname{cos}⁡\theta )(r\operatorname{sin}⁡\theta )\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{5\pi /6}^{7\pi /6}{\int }_{-3\operatorname{sec}⁡\theta }^{-4\operatorname{cos}⁡\theta }{r}^{3}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta  \\  & ={\int }_{5\pi /6}^{7\pi /6}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta {\int }_{-3\operatorname{sec}⁡\theta }^{-4\operatorname{cos}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

## Scale 1 replay

![](generate/scratch/17592186157298/assets/91a7c38f58ff02c1c744ec97-prompt.png)

The region $D$ is enclosed between the curve $y^{2} + \left(x + 2\right)^{2}=4$ and the line $- x=3$, as shown above. What is
$$\iint_D x y\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $2$ centered at $(-2,0)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $y^{2} + \left(x + 2\right)^{2}=4$, we obtain

$$r \left(r + 4 \cos{\left(\theta \right)}\right)=0\quad\Longleftrightarrow\quad r\left(r-\left(- 4 \cos{\left(\theta \right)}\right)\right)=0.$$

The boundary arc has $r=- 4 \cos{\left(\theta \right)}$ for $r>0$.

- For $- x=3$, we get

$$- r \cos{\left(\theta \right)}=3\quad\Longrightarrow\quad r=- \frac{3}{\cos{\left(\theta \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(-3,\sqrt{3})$ and $(-3,- \sqrt{3})$. So the shaded region lies between the polar lines $\theta=\frac{5 \pi}{6}$ and $\theta=\frac{7 \pi}{6}$.

![](generate/scratch/17592186157298/assets/91a7c38f58ff02c1c744ec97-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):- \frac{3}{\cos{\left(\theta \right)}}\leq r\leq - 4 \cos{\left(\theta \right)},\ \frac{5 \pi}{6}\leq\theta\leq \frac{7 \pi}{6}\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D x y\,\mathrm{d}A=\iint_\Delta \frac{r^{3} \sin{\left(2 \theta \right)}}{2}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{\frac{5 \pi}{6}}^{\frac{7 \pi}{6}}\left(\frac{\sin{\left(2 \theta \right)}}{2}\right)\int_{- 3 \sec{\left(\theta \right)}}^{- 4 \cos{\left(\theta \right)}}r^{3}\,\mathrm{d}r\,\mathrm{d}\theta.$$

## Scale 3 variant

![](generate/scratch/17592186157298/assets/f350d3ba6b0867ef0e338478-prompt.png)

The region $D$ is enclosed between the curve $y^{2} + \left(x + 6\right)^{2}=36$ and the line $- x=9$, as shown above. What is
$$\iint_D x y\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $6$ centered at $(-6,0)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $y^{2} + \left(x + 6\right)^{2}=36$, we obtain

$$r \left(r + 12 \cos{\left(\theta \right)}\right)=0\quad\Longleftrightarrow\quad r\left(r-\left(- 12 \cos{\left(\theta \right)}\right)\right)=0.$$

The boundary arc has $r=- 12 \cos{\left(\theta \right)}$ for $r>0$.

- For $- x=9$, we get

$$- r \cos{\left(\theta \right)}=9\quad\Longrightarrow\quad r=- \frac{9}{\cos{\left(\theta \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(-9,3 \sqrt{3})$ and $(-9,- 3 \sqrt{3})$. So the shaded region lies between the polar lines $\theta=\frac{5 \pi}{6}$ and $\theta=\frac{7 \pi}{6}$.

![](generate/scratch/17592186157298/assets/f350d3ba6b0867ef0e338478-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):- \frac{9}{\cos{\left(\theta \right)}}\leq r\leq - 12 \cos{\left(\theta \right)},\ \frac{5 \pi}{6}\leq\theta\leq \frac{7 \pi}{6}\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D x y\,\mathrm{d}A=\iint_\Delta \frac{r^{3} \sin{\left(2 \theta \right)}}{2}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{\frac{5 \pi}{6}}^{\frac{7 \pi}{6}}\left(\frac{\sin{\left(2 \theta \right)}}{2}\right)\int_{- 9 \sec{\left(\theta \right)}}^{- 12 \cos{\left(\theta \right)}}r^{3}\,\mathrm{d}r\,\mathrm{d}\theta.$$

# q-85067

## Source

![](images/dc/dc35d0362ef95d11402ad44cded01abf46686d3088e9d852bd0b9a7ba2454e16.png)

The region $D$ is enclosed between the curve ${x}^{2}+{y}^{2}=1$ and the line $x=-\frac{\sqrt{2}}{2},$ as shown above. What is
${∬}_{D}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}A$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Notice that the region $D$ represents a portion of the disk of radius $1$ centered at $(0,0).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\left\{\begin{aligned}x &=r\operatorname{cos}⁡\theta \\ y &=r\operatorname{sin}⁡\theta\end{aligned}\right.
$$

With that in mind, let's now write our curves in polar coordinates.

- For ${x}^{2}+{y}^{2}=1,$ we obtain $r=1.$

- For $x=-\frac{\sqrt{2}}{2},$ we get

$$
\begin{aligned}x & =-\frac{\sqrt{2}}{2} \\ r\operatorname{cos}⁡\theta  & =-\frac{\sqrt{2}}{2} \\ r & =-\frac{\sqrt{2}}{2\operatorname{cos}⁡\theta } \\ r & =-\frac{\operatorname{sec}⁡\theta }{\sqrt{2}}.\end{aligned}
$$

Now, let's find the limits for the parameter $\theta .$ Our curves intersect at the point $(-\frac{\sqrt{2}}{2},\frac{\sqrt{2}}{2}).$ So, the entire region $D$ lies between the polar lines $\theta =\frac{3\pi }{4}$ and $\theta =\pi ,$ as depicted below.  

![](images/ca/ca09f228fc218ef1b57196c6b6b1e740c10173b7cd38b1c27407726eccd783f1.png)

As a result, the region can be expressed in polar coordinates $(r,\theta )$ as 

$$
Δ=\{(r,\theta )\,:\,-\frac{\operatorname{sec}⁡\theta }{\sqrt{2}}\le r\le 1,\,\frac{3\pi }{4}\le \theta \le \pi \}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}\sqrt{{x}^{2}+{y}^{2}}\,\text{d}A & ={∬}_{Δ}\sqrt{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{3\pi /4}^{\pi }{\int }_{-\operatorname{sec}⁡\theta /\sqrt{2}}^{1}\sqrt{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{3\pi /4}^{\pi }{\int }_{-\operatorname{sec}⁡\theta /\sqrt{2}}^{1}{r}^{2}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

## Scale 1 replay

![](generate/scratch/17592186157298/assets/6417166eca1f67f6398de810-prompt.png)

The region $D$ is enclosed between the curve $x^{2} + y^{2}=1$ and the line $- x=\frac{\sqrt{2}}{2}$, as shown above. What is
$$\iint_D \sqrt{x^{2} + y^{2}}\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $1$ centered at $(0,0)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $x^{2} + y^{2}=1$, we obtain $r=1$.

- For $- x=\frac{\sqrt{2}}{2}$, we get

$$- r \cos{\left(\theta \right)}=\frac{\sqrt{2}}{2}\quad\Longrightarrow\quad r=- \frac{\sqrt{2}}{2 \cos{\left(\theta \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(- \frac{\sqrt{2}}{2},\frac{\sqrt{2}}{2})$ and $(-1,0)$. So the shaded region lies between the polar lines $\theta=\frac{3 \pi}{4}$ and $\theta=\pi$.

![](generate/scratch/17592186157298/assets/6417166eca1f67f6398de810-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):- \frac{\sqrt{2}}{2 \cos{\left(\theta \right)}}\leq r\leq 1,\ \frac{3 \pi}{4}\leq\theta\leq \pi\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D \sqrt{x^{2} + y^{2}}\,\mathrm{d}A=\iint_\Delta r^{2}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{\frac{3 \pi}{4}}^{\pi}\int_{- \frac{\sqrt{2} \sec{\left(\theta \right)}}{2}}^{1}r^{2}\,\mathrm{d}r\,\mathrm{d}\theta.$$

## Scale 3 variant

![](generate/scratch/17592186157298/assets/38a296c0f1f21a76c2ac65ad-prompt.png)

The region $D$ is enclosed between the curve $x^{2} + y^{2}=9$ and the line $- x=\frac{3 \sqrt{2}}{2}$, as shown above. What is
$$\iint_D \sqrt{x^{2} + y^{2}}\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $3$ centered at $(0,0)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $x^{2} + y^{2}=9$, we obtain $r=3$.

- For $- x=\frac{3 \sqrt{2}}{2}$, we get

$$- r \cos{\left(\theta \right)}=\frac{3 \sqrt{2}}{2}\quad\Longrightarrow\quad r=- \frac{3 \sqrt{2}}{2 \cos{\left(\theta \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(- \frac{3 \sqrt{2}}{2},\frac{3 \sqrt{2}}{2})$ and $(-3,0)$. So the shaded region lies between the polar lines $\theta=\frac{3 \pi}{4}$ and $\theta=\pi$.

![](generate/scratch/17592186157298/assets/38a296c0f1f21a76c2ac65ad-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):- \frac{3 \sqrt{2}}{2 \cos{\left(\theta \right)}}\leq r\leq 3,\ \frac{3 \pi}{4}\leq\theta\leq \pi\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D \sqrt{x^{2} + y^{2}}\,\mathrm{d}A=\iint_\Delta r^{2}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{\frac{3 \pi}{4}}^{\pi}\int_{- \frac{3 \sqrt{2} \sec{\left(\theta \right)}}{2}}^{3}r^{2}\,\mathrm{d}r\,\mathrm{d}\theta.$$

# q-85182

## Source

![](images/51/51439321ae9d3760eb48d54351dbd519efe290c77d9197ca55aa590ce79e91a8.png)

The region $D$ is enclosed between the curve $(x-2)^{2}+{y}^{2}=4$ and the line $x=3,$ as shown above. What is
${∬}_{D}\frac{y}{{x}^{2}}\,\text{d}A$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Notice that the region $D$ represents a portion of the disk of radius $2$ centered at $(2,0).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\left\{\begin{aligned}x &=r\operatorname{cos}⁡\theta \\ y &=r\operatorname{sin}⁡\theta\end{aligned}\right.
$$

With that in mind, let's now write our curves in polar coordinates.

- For $(x-2)^{2}+{y}^{2}=4,$ we obtain

$$
\begin{aligned}(x-2)^{2}+{y}^{2} & =4 \\ (r\operatorname{cos}⁡\theta -2)^{2}+(r\operatorname{sin}⁡\theta )^{2} & =4 \\ {r}^{2}{cos}^{2}⁡\theta -4r\operatorname{cos}⁡\theta +4+{r}^{2}{sin}^{2}⁡\theta  & =4 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-4r\operatorname{cos}⁡\theta  & =0 \\ {r}^{2}-4r\operatorname{cos}⁡\theta  & =0 \\ r(r-4\operatorname{cos}⁡\theta ) & =0.\end{aligned}
$$

 
Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=4\operatorname{cos}⁡\theta .$

- For $x=3,$ we get

$$
\begin{aligned}x & =3 \\ r\operatorname{cos}⁡\theta  & =3 \\ r & =\frac{3}{\operatorname{cos}⁡\theta } \\ r & =3\operatorname{sec}⁡\theta .\end{aligned}
$$

Now, let's find the limits for the parameter $\theta .$ Our curves intersect at the point $(3,-\sqrt{3}).$ So, the entire region $D$ lies between the polar lines $\theta =-\frac{\pi }{6}$ and $\theta =0,$ as depicted below.  

![](images/bf/bf2d20acbb93d3c61e9890a49d1c15a08c2b4e18b474da421bded7cf3dafc297.png)

As a result, the region can be expressed in polar coordinates $(r,\theta )$ as 

$$
Δ=\{(r,\theta )\,:\,3\operatorname{sec}⁡\theta \le r\le 4\operatorname{cos}⁡\theta ,\,-\frac{\pi }{6}\le \theta \le 0\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}\frac{y}{{x}^{2}}\,\text{d}A & ={∬}_{Δ}\frac{r\operatorname{sin}⁡\theta }{(r\operatorname{cos}⁡\theta )^{2}}\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{-\pi /6}^{0}{\int }_{3\operatorname{sec}⁡\theta }^{4\operatorname{cos}⁡\theta }\frac{{r}^{2}\operatorname{sin}⁡\theta }{{r}^{2}{cos}^{2}⁡\theta }\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{-\pi /6}^{0}\operatorname{sec}⁡\theta \operatorname{tan}⁡\theta {\int }_{3\operatorname{sec}⁡\theta }^{4\operatorname{cos}⁡\theta }\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

## Scale 1 replay

![](generate/scratch/17592186157298/assets/d406182a0bdc91e1b65dd5bf-prompt.png)

The region $D$ is enclosed between the curve $y^{2} + \left(x - 2\right)^{2}=4$ and the line $x=3$, as shown above. What is
$$\iint_D \frac{y}{x^{2}}\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $2$ centered at $(2,0)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $y^{2} + \left(x - 2\right)^{2}=4$, we obtain

$$r \left(r - 4 \cos{\left(\theta \right)}\right)=0\quad\Longleftrightarrow\quad r\left(r-\left(4 \cos{\left(\theta \right)}\right)\right)=0.$$

The boundary arc has $r=4 \cos{\left(\theta \right)}$ for $r>0$.

- For $x=3$, we get

$$r \cos{\left(\theta \right)}=3\quad\Longrightarrow\quad r=\frac{3}{\cos{\left(\theta \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(3,- \sqrt{3})$ and $(4,0)$. So the shaded region lies between the polar lines $\theta=- \frac{\pi}{6}$ and $\theta=0$.

![](generate/scratch/17592186157298/assets/d406182a0bdc91e1b65dd5bf-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):\frac{3}{\cos{\left(\theta \right)}}\leq r\leq 4 \cos{\left(\theta \right)},\ - \frac{\pi}{6}\leq\theta\leq 0\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D \frac{y}{x^{2}}\,\mathrm{d}A=\iint_\Delta \frac{\sin{\left(\theta \right)}}{\cos^{2}{\left(\theta \right)}}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{- \frac{\pi}{6}}^{0}\left(\tan{\left(\theta \right)} \sec{\left(\theta \right)}\right)\int_{3 \sec{\left(\theta \right)}}^{4 \cos{\left(\theta \right)}}\,\mathrm{d}r\,\mathrm{d}\theta.$$

## Scale 3 variant

![](generate/scratch/17592186157298/assets/0daf83dea27dcb0755756eed-prompt.png)

The region $D$ is enclosed between the curve $y^{2} + \left(x - 6\right)^{2}=36$ and the line $x=9$, as shown above. What is
$$\iint_D \frac{y}{x^{2}}\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $6$ centered at $(6,0)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $y^{2} + \left(x - 6\right)^{2}=36$, we obtain

$$r \left(r - 12 \cos{\left(\theta \right)}\right)=0\quad\Longleftrightarrow\quad r\left(r-\left(12 \cos{\left(\theta \right)}\right)\right)=0.$$

The boundary arc has $r=12 \cos{\left(\theta \right)}$ for $r>0$.

- For $x=9$, we get

$$r \cos{\left(\theta \right)}=9\quad\Longrightarrow\quad r=\frac{9}{\cos{\left(\theta \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(9,- 3 \sqrt{3})$ and $(12,0)$. So the shaded region lies between the polar lines $\theta=- \frac{\pi}{6}$ and $\theta=0$.

![](generate/scratch/17592186157298/assets/0daf83dea27dcb0755756eed-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):\frac{9}{\cos{\left(\theta \right)}}\leq r\leq 12 \cos{\left(\theta \right)},\ - \frac{\pi}{6}\leq\theta\leq 0\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D \frac{y}{x^{2}}\,\mathrm{d}A=\iint_\Delta \frac{\sin{\left(\theta \right)}}{\cos^{2}{\left(\theta \right)}}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{- \frac{\pi}{6}}^{0}\left(\tan{\left(\theta \right)} \sec{\left(\theta \right)}\right)\int_{9 \sec{\left(\theta \right)}}^{12 \cos{\left(\theta \right)}}\,\mathrm{d}r\,\mathrm{d}\theta.$$

# q-161100

## Source

![](images/6d/6ddc0b2138025b07ffdb7bf34afabeba578400b194922bec7a733cc9246c7c0f.png)

The region $D$ is enclosed between the curve $(x-1)^{2}+(y-1)^{2}=2$ and the line $y=2-x,$ as shown above. What is
${∬}_{D}x\,\text{d}A$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Notice that the region $D$ represents a portion of the disk of radius $\sqrt{2}$ centered at $(1,1).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\left\{\begin{aligned}x &=r\operatorname{cos}⁡\theta \\ y &=r\operatorname{sin}⁡\theta\end{aligned}\right.
$$

With that in mind, let's now write our curves in polar coordinates.

- For $(x-1)^{2}+(y-1)^{2}=2,$ we obtain

$$
\begin{aligned}(x-1)^{2}+(y-1)^{2} & =2 \\ (r\operatorname{cos}⁡\theta -1)^{2}+(r\operatorname{sin}⁡\theta -1)^{2} & =2 \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -2r\operatorname{cos}⁡\theta -2r\operatorname{sin}⁡\theta +2 & =2 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-2r(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta ) & =0 \\ {r}^{2}-2r(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta ) & =0 \\ r(r-2(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )) & =0.\end{aligned}
$$

 
Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=2(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta ).$

- For $y=2-x,$ we get

$$
\begin{aligned}y & =2-x \\ r\operatorname{sin}⁡\theta  & =2-r\operatorname{cos}⁡\theta  \\ r(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta ) & =2 \\ r & =\frac{2}{\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta }.\end{aligned}
$$

Now, let's find the limits for the parameter $\theta .$ Our curves intersect at the points $(2,0)$ and $(0,2).$ So, the entire region $D$ lies between the polar lines $\theta =0$ and $\theta =\frac{\pi }{2},$ as depicted below.  

![](images/58/587c299c1bdf89061be205cf185d6335fba865d2e30c81cac5b9d223fc84b486.png)

As a result, the region can be expressed in polar coordinates $(r,\theta )$ as 

$$
Δ={(r,\theta )\,:\,\frac{2}{\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta }\le r\le 2(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta ),\,0\le \theta \le \frac{\pi }{2}}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}x\,\text{d}A & ={∬}_{Δ}r\operatorname{cos}⁡\theta \cdot r\,\text{d}r\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}{\int }_{2/(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )}^{2(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )}{r}^{2}\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta {\int }_{2/(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )}^{2(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )}{r}^{2}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

## Scale 1 replay

![](generate/scratch/17592186157298/assets/b6612f465905091266ffa010-prompt.png)

The region $D$ is enclosed between the curve $\left(x - 1\right)^{2} + \left(y - 1\right)^{2}=2$ and the line $x + y=2$, as shown above. What is
$$\iint_D x\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $\sqrt{2}$ centered at $(1,1)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $\left(x - 1\right)^{2} + \left(y - 1\right)^{2}=2$, we obtain

$$r \left(r - 2 \sqrt{2} \sin{\left(\theta + \frac{\pi}{4} \right)}\right)=0\quad\Longleftrightarrow\quad r\left(r-\left(2 \sqrt{2} \sin{\left(\theta + \frac{\pi}{4} \right)}\right)\right)=0.$$

The boundary arc has $r=2 \sqrt{2} \sin{\left(\theta + \frac{\pi}{4} \right)}$ for $r>0$.

- For $x + y=2$, we get

$$r \left(\sin{\left(\theta \right)} + \cos{\left(\theta \right)}\right)=2\quad\Longrightarrow\quad r=\frac{\sqrt{2}}{\sin{\left(\theta + \frac{\pi}{4} \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(2,0)$ and $(0,2)$. So the shaded region lies between the polar lines $\theta=0$ and $\theta=\frac{\pi}{2}$.

![](generate/scratch/17592186157298/assets/b6612f465905091266ffa010-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):\frac{\sqrt{2}}{\sin{\left(\theta + \frac{\pi}{4} \right)}}\leq r\leq 2 \sqrt{2} \sin{\left(\theta + \frac{\pi}{4} \right)},\ 0\leq\theta\leq \frac{\pi}{2}\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D x\,\mathrm{d}A=\iint_\Delta r^{2} \cos{\left(\theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{0}^{\frac{\pi}{2}}\left(\cos{\left(\theta \right)}\right)\int_{\frac{\sqrt{2}}{\sin{\left(\theta + \frac{\pi}{4} \right)}}}^{2 \sqrt{2} \sin{\left(\theta + \frac{\pi}{4} \right)}}r^{2}\,\mathrm{d}r\,\mathrm{d}\theta.$$

## Scale 3 variant

![](generate/scratch/17592186157298/assets/8ac8254442b889ee81811843-prompt.png)

The region $D$ is enclosed between the curve $\left(x - 3\right)^{2} + \left(y - 3\right)^{2}=18$ and the line $x + y=6$, as shown above. What is
$$\iint_D x\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $3 \sqrt{2}$ centered at $(3,3)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $\left(x - 3\right)^{2} + \left(y - 3\right)^{2}=18$, we obtain

$$r \left(r - 6 \sqrt{2} \sin{\left(\theta + \frac{\pi}{4} \right)}\right)=0\quad\Longleftrightarrow\quad r\left(r-\left(6 \sqrt{2} \sin{\left(\theta + \frac{\pi}{4} \right)}\right)\right)=0.$$

The boundary arc has $r=6 \sqrt{2} \sin{\left(\theta + \frac{\pi}{4} \right)}$ for $r>0$.

- For $x + y=6$, we get

$$r \left(\sin{\left(\theta \right)} + \cos{\left(\theta \right)}\right)=6\quad\Longrightarrow\quad r=\frac{6}{\sin{\left(\theta \right)} + \cos{\left(\theta \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(6,0)$ and $(0,6)$. So the shaded region lies between the polar lines $\theta=0$ and $\theta=\frac{\pi}{2}$.

![](generate/scratch/17592186157298/assets/8ac8254442b889ee81811843-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):\frac{6}{\sin{\left(\theta \right)} + \cos{\left(\theta \right)}}\leq r\leq 6 \sqrt{2} \sin{\left(\theta + \frac{\pi}{4} \right)},\ 0\leq\theta\leq \frac{\pi}{2}\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D x\,\mathrm{d}A=\iint_\Delta r^{2} \cos{\left(\theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{0}^{\frac{\pi}{2}}\left(\cos{\left(\theta \right)}\right)\int_{\frac{6}{\sin{\left(\theta \right)} + \cos{\left(\theta \right)}}}^{6 \sqrt{2} \sin{\left(\theta + \frac{\pi}{4} \right)}}r^{2}\,\mathrm{d}r\,\mathrm{d}\theta.$$

# q-85062

## Source

![](images/ac/acb2f50d01df6ebec6003cc7b9c944b759113b9f364455fb62eede389b335229.png)

The region $D$ is enclosed between the curve ${x}^{2}+(y+2)^{2}=4$ and the line $y=-3,$ as shown above. What is
${∬}_{D}({x}^{2}+{y}^{2})\,\text{d}A$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Notice that the region $D$ represents a portion of the disk of radius $2$ centered at $(0,-2).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\left\{\begin{aligned}x &=r\operatorname{cos}⁡\theta \\ y &=r\operatorname{sin}⁡\theta\end{aligned}\right.
$$

With that in mind, let's now write our curves in polar coordinates.

- For ${x}^{2}+(y+2)^{2}=4,$ we obtain

$$
\begin{aligned}{x}^{2}+(y+2)^{2} & =4 \\ (r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta +2)^{2} & =4 \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta +4r\operatorname{sin}⁡\theta +4 & =4 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )+4r\operatorname{sin}⁡\theta  & =0 \\ {r}^{2}+4r\operatorname{sin}⁡\theta  & =0 \\ r(r+4\operatorname{sin}⁡\theta ) & =0.\end{aligned}
$$

 
Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=-4\operatorname{sin}⁡\theta .$

- For $y=-3,$ we get

$$
\begin{aligned}y & =-3 \\ r\operatorname{sin}⁡\theta  & =-3 \\ r & =-\frac{3}{\operatorname{sin}⁡\theta } \\ r & =-3\operatorname{csc}⁡\theta .\end{aligned}
$$

Now, let's find the limits for the parameter $\theta .$ Our curves intersect at the points $(-\sqrt{3},-3)$ and $(\sqrt{3},-3).$ So, the entire region $D$ lies between the polar lines $\theta =-\frac{2\pi }{3}$ and $\theta =-\frac{\pi }{3},$ as depicted below.  

![](images/59/5991463a56d8358164d32b15f73e938573463d8d706d2b9c8fc06803326a5f0f.png)

As a result, the region can be expressed in polar coordinates $(r,\theta )$ as 

$$
Δ={(r,\theta )\,:\,-3\operatorname{csc}⁡\theta \le r\le -4\operatorname{sin}⁡\theta ,\,-2\frac{\pi }{3}\le \theta \le -\frac{\pi }{3}}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}({x}^{2}+{y}^{2})\,\text{d}A & ={∬}_{Δ}((r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2})\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{-2\pi /3}^{-\pi /3}{\int }_{-3\operatorname{csc}⁡\theta }^{-4\operatorname{sin}⁡\theta }{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )\,r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{-2\pi /3}^{-\pi /3}{\int }_{-3\operatorname{csc}⁡\theta }^{-4\operatorname{sin}⁡\theta }{r}^{3}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

## Scale 1 replay

![](generate/scratch/17592186157298/assets/136a77280ccfab15802e57ff-prompt.png)

The region $D$ is enclosed between the curve $x^{2} + \left(y + 2\right)^{2}=4$ and the line $- y=3$, as shown above. What is
$$\iint_D x^{2} + y^{2}\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $2$ centered at $(0,-2)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $x^{2} + \left(y + 2\right)^{2}=4$, we obtain

$$r \left(r + 4 \sin{\left(\theta \right)}\right)=0\quad\Longleftrightarrow\quad r\left(r-\left(- 4 \sin{\left(\theta \right)}\right)\right)=0.$$

The boundary arc has $r=- 4 \sin{\left(\theta \right)}$ for $r>0$.

- For $- y=3$, we get

$$- r \sin{\left(\theta \right)}=3\quad\Longrightarrow\quad r=- \frac{3}{\sin{\left(\theta \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(- \sqrt{3},-3)$ and $(\sqrt{3},-3)$. So the shaded region lies between the polar lines $\theta=- \frac{2 \pi}{3}$ and $\theta=- \frac{\pi}{3}$.

![](generate/scratch/17592186157298/assets/136a77280ccfab15802e57ff-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):- \frac{3}{\sin{\left(\theta \right)}}\leq r\leq - 4 \sin{\left(\theta \right)},\ - \frac{2 \pi}{3}\leq\theta\leq - \frac{\pi}{3}\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D x^{2} + y^{2}\,\mathrm{d}A=\iint_\Delta r^{3}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{- \frac{2 \pi}{3}}^{- \frac{\pi}{3}}\int_{- 3 \csc{\left(\theta \right)}}^{- 4 \sin{\left(\theta \right)}}r^{3}\,\mathrm{d}r\,\mathrm{d}\theta.$$

## Scale 3 variant

![](generate/scratch/17592186157298/assets/eeb14264f6b0c691485bf75c-prompt.png)

The region $D$ is enclosed between the curve $x^{2} + \left(y + 6\right)^{2}=36$ and the line $- y=9$, as shown above. What is
$$\iint_D x^{2} + y^{2}\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $6$ centered at $(0,-6)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $x^{2} + \left(y + 6\right)^{2}=36$, we obtain

$$r \left(r + 12 \sin{\left(\theta \right)}\right)=0\quad\Longleftrightarrow\quad r\left(r-\left(- 12 \sin{\left(\theta \right)}\right)\right)=0.$$

The boundary arc has $r=- 12 \sin{\left(\theta \right)}$ for $r>0$.

- For $- y=9$, we get

$$- r \sin{\left(\theta \right)}=9\quad\Longrightarrow\quad r=- \frac{9}{\sin{\left(\theta \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(- 3 \sqrt{3},-9)$ and $(3 \sqrt{3},-9)$. So the shaded region lies between the polar lines $\theta=- \frac{2 \pi}{3}$ and $\theta=- \frac{\pi}{3}$.

![](generate/scratch/17592186157298/assets/eeb14264f6b0c691485bf75c-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):- \frac{9}{\sin{\left(\theta \right)}}\leq r\leq - 12 \sin{\left(\theta \right)},\ - \frac{2 \pi}{3}\leq\theta\leq - \frac{\pi}{3}\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D x^{2} + y^{2}\,\mathrm{d}A=\iint_\Delta r^{3}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{- \frac{2 \pi}{3}}^{- \frac{\pi}{3}}\int_{- 9 \csc{\left(\theta \right)}}^{- 12 \sin{\left(\theta \right)}}r^{3}\,\mathrm{d}r\,\mathrm{d}\theta.$$

# q-85181

## Source

![](images/3d/3d5542933934102149c58153c3108d55d9c615e991db8aca8d8fc1e60837917f.png)

The region $D$ is enclosed between the curve ${x}^{2}+(y-2)^{2}=4$ and the line $y=3,$ as shown above. What is
${∬}_{D}\frac{{x}^{2}}{{x}^{2}+{y}^{2}}\,\text{d}A$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Notice that the region $D$ represents a portion of the disk of radius $2$ centered at $(0,2).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\left\{\begin{aligned}x &=r\operatorname{cos}⁡\theta \\ y &=r\operatorname{sin}⁡\theta\end{aligned}\right.
$$

With that in mind, let's now write our curves in polar coordinates.

- For ${x}^{2}+(y-2)^{2}=4,$ we obtain

$$
\begin{aligned}{x}^{2}+(y-2)^{2} & =4 \\ (r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta -2)^{2} & =4 \\ {r}^{2}{cos}^{2}⁡\theta +{r}^{2}{sin}^{2}⁡\theta -4r\operatorname{sin}⁡\theta +4 & =4 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-4r\operatorname{sin}⁡\theta  & =0 \\ {r}^{2}-4r\operatorname{sin}⁡\theta  & =0 \\ r(r-4\operatorname{sin}⁡\theta ) & =0.\end{aligned}
$$

 
Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=4\operatorname{sin}⁡\theta .$

- For $y=3,$ we get

$$
\begin{aligned}y & =3 \\ r\operatorname{sin}⁡\theta  & =3 \\ r & =\frac{3}{\operatorname{sin}⁡\theta } \\ r & =3\operatorname{csc}⁡\theta .\end{aligned}
$$

Now, let's find the limits for the parameter $\theta .$ Our curves intersect at the point $(-\sqrt{3},3).$ So, the entire region $D$ lies between the polar lines $\theta =\frac{\pi }{2}$ and $\theta =\frac{2\pi }{3},$ as depicted below.  

![](images/49/4903ca2ba8cde3f7874e10998a0741035ec7b2dea69a7804eaca64cb552fc572.png)

As a result, the region can be expressed in polar coordinates $(r,\theta )$ as 

$$
Δ=\{(r,\theta )\,:\,3\operatorname{csc}⁡\theta \le r\le 4\operatorname{sin}⁡\theta ,\,\frac{\pi }{2}\le \theta \le \frac{2\pi }{3}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}\frac{{x}^{2}}{{x}^{2}+{y}^{2}}\,\text{d}A & ={∬}_{Δ}\frac{(r\operatorname{cos}⁡\theta )^{2}}{(r\operatorname{cos}⁡\theta )^{2}+(r\operatorname{sin}⁡\theta )^{2}}\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{\pi /2}^{2\pi /3}{\int }_{3\operatorname{csc}⁡\theta }^{4\operatorname{sin}⁡\theta }\frac{{r}^{3}{cos}^{2}⁡\theta }{{r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{\pi /2}^{2\pi /3}{\int }_{3\operatorname{csc}⁡\theta }^{4\operatorname{sin}⁡\theta }r{cos}^{2}⁡\theta \,\text{d}r\,\text{d}\theta  \\  & ={\int }_{\pi /2}^{2\pi /3}{cos}^{2}⁡\theta {\int }_{3\operatorname{csc}⁡\theta }^{4\operatorname{sin}⁡\theta }r\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

## Scale 1 replay

![](generate/scratch/17592186157298/assets/7f4077608f7a638294f45720-prompt.png)

The region $D$ is enclosed between the curve $x^{2} + \left(y - 2\right)^{2}=4$ and the line $y=3$, as shown above. What is
$$\iint_D \frac{x^{2}}{x^{2} + y^{2}}\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $2$ centered at $(0,2)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $x^{2} + \left(y - 2\right)^{2}=4$, we obtain

$$r \left(r - 4 \sin{\left(\theta \right)}\right)=0\quad\Longleftrightarrow\quad r\left(r-\left(4 \sin{\left(\theta \right)}\right)\right)=0.$$

The boundary arc has $r=4 \sin{\left(\theta \right)}$ for $r>0$.

- For $y=3$, we get

$$r \sin{\left(\theta \right)}=3\quad\Longrightarrow\quad r=\frac{3}{\sin{\left(\theta \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(0,4)$ and $(- \sqrt{3},3)$. So the shaded region lies between the polar lines $\theta=\frac{\pi}{2}$ and $\theta=\frac{2 \pi}{3}$.

![](generate/scratch/17592186157298/assets/7f4077608f7a638294f45720-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):\frac{3}{\sin{\left(\theta \right)}}\leq r\leq 4 \sin{\left(\theta \right)},\ \frac{\pi}{2}\leq\theta\leq \frac{2 \pi}{3}\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D \frac{x^{2}}{x^{2} + y^{2}}\,\mathrm{d}A=\iint_\Delta r \cos^{2}{\left(\theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{\frac{\pi}{2}}^{\frac{2 \pi}{3}}\left(\cos^{2}{\left(\theta \right)}\right)\int_{3 \csc{\left(\theta \right)}}^{4 \sin{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta.$$

## Scale 3 variant

![](generate/scratch/17592186157298/assets/581cd8ea2a674ec3a5f89b78-prompt.png)

The region $D$ is enclosed between the curve $x^{2} + \left(y - 6\right)^{2}=36$ and the line $y=9$, as shown above. What is
$$\iint_D \frac{x^{2}}{x^{2} + y^{2}}\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $6$ centered at $(0,6)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $x^{2} + \left(y - 6\right)^{2}=36$, we obtain

$$r \left(r - 12 \sin{\left(\theta \right)}\right)=0\quad\Longleftrightarrow\quad r\left(r-\left(12 \sin{\left(\theta \right)}\right)\right)=0.$$

The boundary arc has $r=12 \sin{\left(\theta \right)}$ for $r>0$.

- For $y=9$, we get

$$r \sin{\left(\theta \right)}=9\quad\Longrightarrow\quad r=\frac{9}{\sin{\left(\theta \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(0,12)$ and $(- 3 \sqrt{3},9)$. So the shaded region lies between the polar lines $\theta=\frac{\pi}{2}$ and $\theta=\frac{2 \pi}{3}$.

![](generate/scratch/17592186157298/assets/581cd8ea2a674ec3a5f89b78-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):\frac{9}{\sin{\left(\theta \right)}}\leq r\leq 12 \sin{\left(\theta \right)},\ \frac{\pi}{2}\leq\theta\leq \frac{2 \pi}{3}\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D \frac{x^{2}}{x^{2} + y^{2}}\,\mathrm{d}A=\iint_\Delta r \cos^{2}{\left(\theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{\frac{\pi}{2}}^{\frac{2 \pi}{3}}\left(\cos^{2}{\left(\theta \right)}\right)\int_{9 \csc{\left(\theta \right)}}^{12 \sin{\left(\theta \right)}}r\,\mathrm{d}r\,\mathrm{d}\theta.$$

# q-83979

## Source

![](images/8a/8a51719e208dafaa32d7f28c338885313942513493bd9fe0392b1ef06004e91e.png)

The region $D$ is enclosed between the curve $(x-1)^{2}+{y}^{2}=1$ and the line $x=1,$ as shown above. What is
${∬}_{D}(x+y)\,dA$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Notice that the region $D$ represents a portion of the disk of radius $1$ centered at $(1,0).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\left\{\begin{aligned}x &=r\operatorname{cos}⁡\theta \\ y &=r\operatorname{sin}⁡\theta\end{aligned}\right.
$$

With that in mind, let's now write our curves in polar coordinates.

- For $(x-1)^{2}+{y}^{2}=1,$ we obtain

$$
\begin{aligned}(x-1)^{2}+{y}^{2} & =1 \\ (r\operatorname{cos}⁡\theta -1)^{2}+(r\operatorname{sin}⁡\theta )^{2} & =1 \\ {r}^{2}{cos}^{2}⁡\theta -2r\operatorname{cos}⁡\theta +1+{r}^{2}{sin}^{2}⁡\theta  & =1 \\ {r}^{2}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )-2r\operatorname{cos}⁡\theta  & =0 \\ {r}^{2}-2r\operatorname{cos}⁡\theta  & =0 \\ r(r-2\operatorname{cos}⁡\theta ) & =0.\end{aligned}
$$

 
Since $r$ cannot be identical to zero on the entire semicircle, we must have $r=2\operatorname{cos}⁡\theta .$

- For $x=1,$ we get

$$
\begin{aligned}x & =1 \\ r\operatorname{cos}⁡\theta  & =1 \\ r & =\frac{1}{\operatorname{cos}⁡\theta } \\ r & =\operatorname{sec}⁡\theta .\end{aligned}
$$

Now, let's find the limits for the parameter $\theta .$ Our curves intersect at the points $(1,-1)$ and $(1,1).$ So, the entire region $D$ lies between the polar lines $\theta =-\frac{\pi }{4}$ and $\theta =\frac{\pi }{4},$ as depicted below.  

![](images/43/4371a691b81b2ed1cb5d3468f68cd24f41e8a6b87d378a3206238d58e61791f0.png)

As a result, the region can be expressed in polar coordinates $(r,\theta )$ as 

$$
Δ=\{(r,\theta )\,:\,\operatorname{sec}⁡\theta \le r\le 2\operatorname{cos}⁡\theta ,\,-\frac{\pi }{4}\le \theta \le \frac{\pi }{4}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}x+y\,\text{d}A & ={∬}_{Δ}(r\operatorname{cos}⁡\theta +r\operatorname{sin}⁡\theta )\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{-\pi /4}^{\pi /4}{\int }_{\operatorname{sec}⁡\theta }^{2\operatorname{cos}⁡\theta }{r}^{2}(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta )\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{-\pi /4}^{\pi /4}(\operatorname{cos}⁡\theta +\operatorname{sin}⁡\theta ){\int }_{\operatorname{sec}⁡\theta }^{2\operatorname{cos}⁡\theta }{r}^{2}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

## Scale 1 replay

![](generate/scratch/17592186157298/assets/4dd14b23b680f531dd4633fa-prompt.png)

The region $D$ is enclosed between the curve $y^{2} + \left(x - 1\right)^{2}=1$ and the line $x=1$, as shown above. What is
$$\iint_D x + y\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $1$ centered at $(1,0)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $y^{2} + \left(x - 1\right)^{2}=1$, we obtain

$$r \left(r - 2 \cos{\left(\theta \right)}\right)=0\quad\Longleftrightarrow\quad r\left(r-\left(2 \cos{\left(\theta \right)}\right)\right)=0.$$

The boundary arc has $r=2 \cos{\left(\theta \right)}$ for $r>0$.

- For $x=1$, we get

$$r \cos{\left(\theta \right)}=1\quad\Longrightarrow\quad r=\frac{1}{\cos{\left(\theta \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(1,-1)$ and $(1,1)$. So the shaded region lies between the polar lines $\theta=- \frac{\pi}{4}$ and $\theta=\frac{\pi}{4}$.

![](generate/scratch/17592186157298/assets/4dd14b23b680f531dd4633fa-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):\frac{1}{\cos{\left(\theta \right)}}\leq r\leq 2 \cos{\left(\theta \right)},\ - \frac{\pi}{4}\leq\theta\leq \frac{\pi}{4}\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D x + y\,\mathrm{d}A=\iint_\Delta \sqrt{2} r^{2} \sin{\left(\theta + \frac{\pi}{4} \right)}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{- \frac{\pi}{4}}^{\frac{\pi}{4}}\left(\sin{\left(\theta \right)} + \cos{\left(\theta \right)}\right)\int_{\sec{\left(\theta \right)}}^{2 \cos{\left(\theta \right)}}r^{2}\,\mathrm{d}r\,\mathrm{d}\theta.$$

## Scale 3 variant

![](generate/scratch/17592186157298/assets/6778b2eff7065b9a1c0affba-prompt.png)

The region $D$ is enclosed between the curve $y^{2} + \left(x - 3\right)^{2}=9$ and the line $x=3$, as shown above. What is
$$\iint_D x + y\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $3$ centered at $(3,0)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $y^{2} + \left(x - 3\right)^{2}=9$, we obtain

$$r \left(r - 6 \cos{\left(\theta \right)}\right)=0\quad\Longleftrightarrow\quad r\left(r-\left(6 \cos{\left(\theta \right)}\right)\right)=0.$$

The boundary arc has $r=6 \cos{\left(\theta \right)}$ for $r>0$.

- For $x=3$, we get

$$r \cos{\left(\theta \right)}=3\quad\Longrightarrow\quad r=\frac{3}{\cos{\left(\theta \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(3,-3)$ and $(3,3)$. So the shaded region lies between the polar lines $\theta=- \frac{\pi}{4}$ and $\theta=\frac{\pi}{4}$.

![](generate/scratch/17592186157298/assets/6778b2eff7065b9a1c0affba-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):\frac{3}{\cos{\left(\theta \right)}}\leq r\leq 6 \cos{\left(\theta \right)},\ - \frac{\pi}{4}\leq\theta\leq \frac{\pi}{4}\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D x + y\,\mathrm{d}A=\iint_\Delta \sqrt{2} r^{2} \sin{\left(\theta + \frac{\pi}{4} \right)}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{- \frac{\pi}{4}}^{\frac{\pi}{4}}\left(\sin{\left(\theta \right)} + \cos{\left(\theta \right)}\right)\int_{3 \sec{\left(\theta \right)}}^{6 \cos{\left(\theta \right)}}r^{2}\,\mathrm{d}r\,\mathrm{d}\theta.$$

# q-83975

## Source

![](images/37/37a6eb13f8a6f6ab46040495894dedeec4951b4814aad19f45bfbd4ed7040767.png)

The region $D$ is enclosed between the curve ${x}^{2}+{y}^{2}=4$ and the line $y=\sqrt{2},$ as shown above. What is
${∬}_{D}{x}^{2}\,\text{d}A$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$
{∬}_{D}f(x,y)\text{ }dA={∬}_{Δ}\text{ }f(r\operatorname{cos}⁡\theta ,r\operatorname{sin}⁡\theta )\,r\text{ }drd\theta .
$$

Notice that the region $D$ represents a portion of the disk of radius $2$ centered at $(0,0).$ 

Cartesian and polar coordinates are connected by the following equations:

$$
\left\{\begin{aligned}x &=r\operatorname{cos}⁡\theta \\ y &=r\operatorname{sin}⁡\theta\end{aligned}\right.
$$

With that in mind, let's now write our curves in polar coordinates.

- For ${x}^{2}+{y}^{2}=4,$ we obtain $r=2.$

- For $y=\sqrt{2},$ we get

$$
\begin{aligned}y & =\sqrt{2} \\ r\operatorname{sin}⁡\theta  & =\sqrt{2} \\ r & =\frac{\sqrt{2}}{\operatorname{sin}⁡\theta } \\ r & =\sqrt{2}\operatorname{csc}⁡\theta .\end{aligned}
$$

Now, let's find the limits for the parameter $\theta .$ Our curves intersect at the point $(\sqrt{2},\sqrt{2}).$ So, the entire region $D$ lies between the polar lines $\theta =\frac{\pi }{4}$ and $\theta =\frac{\pi }{2},$ as depicted below.  

![](images/89/897028515a29fdc4174d2a101439a81a30895db41ac3d29f311d53e0e6a79e29.png)

As a result, the region can be expressed in polar coordinates $(r,\theta )$ as 

$$
Δ=\{(r,\theta )\,:\,\sqrt{2}\operatorname{csc}⁡\theta \le r\le 2,\,\frac{\pi }{4}\le \theta \le \frac{\pi }{2}\}.
$$

Therefore, using the change of variables formula, we obtain 

$$
\begin{aligned}{∬}_{D}{x}^{2}\,\text{d}A & ={∬}_{Δ}(r\operatorname{cos}⁡\theta )^{2}\,r\,\text{d}r\text{d}\theta  \\  & ={\int }_{\pi /4}^{\pi /2}{\int }_{\sqrt{2}\operatorname{csc}⁡\theta }^{2}{r}^{3}{sin}^{2}⁡\theta \,\text{d}r\,\text{d}\theta  \\  & ={\int }_{\pi /4}^{\pi /2}{cos}^{2}⁡\theta {\int }_{\sqrt{2}\operatorname{csc}⁡\theta }^{2}{r}^{3}\,\text{d}r\,\text{d}\theta .\end{aligned}
$$

## Scale 1 replay

![](generate/scratch/17592186157298/assets/be4df47f3dc96f0e401e1357-prompt.png)

The region $D$ is enclosed between the curve $x^{2} + y^{2}=4$ and the line $y=\sqrt{2}$, as shown above. What is
$$\iint_D x^{2}\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $2$ centered at $(0,0)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $x^{2} + y^{2}=4$, we obtain $r=2$.

- For $y=\sqrt{2}$, we get

$$r \sin{\left(\theta \right)}=\sqrt{2}\quad\Longrightarrow\quad r=\frac{\sqrt{2}}{\sin{\left(\theta \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(\sqrt{2},\sqrt{2})$ and $(0,2)$. So the shaded region lies between the polar lines $\theta=\frac{\pi}{4}$ and $\theta=\frac{\pi}{2}$.

![](generate/scratch/17592186157298/assets/be4df47f3dc96f0e401e1357-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):\frac{\sqrt{2}}{\sin{\left(\theta \right)}}\leq r\leq 2,\ \frac{\pi}{4}\leq\theta\leq \frac{\pi}{2}\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D x^{2}\,\mathrm{d}A=\iint_\Delta r^{3} \cos^{2}{\left(\theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{\frac{\pi}{4}}^{\frac{\pi}{2}}\left(\cos^{2}{\left(\theta \right)}\right)\int_{\sqrt{2} \csc{\left(\theta \right)}}^{2}r^{3}\,\mathrm{d}r\,\mathrm{d}\theta.$$

## Scale 3 variant

![](generate/scratch/17592186157298/assets/d16d7bbeaadb2ea5b7228871-prompt.png)

The region $D$ is enclosed between the curve $x^{2} + y^{2}=36$ and the line $y=3 \sqrt{2}$, as shown above. What is
$$\iint_D x^{2}\,\mathrm{d}A$$
expressed in polar coordinates?

We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form

$$\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.$$

Notice that the region $D$ represents a portion of the disk of radius $6$ centered at $(0,0)$.

Cartesian and polar coordinates are connected by the following equations:

$$x=r\cos\theta,\qquad y=r\sin\theta.$$

With that in mind, let's now write our curves in polar coordinates.

- For $x^{2} + y^{2}=36$, we obtain $r=6$.

- For $y=3 \sqrt{2}$, we get

$$r \sin{\left(\theta \right)}=3 \sqrt{2}\quad\Longrightarrow\quad r=\frac{3 \sqrt{2}}{\sin{\left(\theta \right)}}.$$

Now, let's find the limits for the parameter $\theta$. The endpoints of the selected arc are $(3 \sqrt{2},3 \sqrt{2})$ and $(0,6)$. So the shaded region lies between the polar lines $\theta=\frac{\pi}{4}$ and $\theta=\frac{\pi}{2}$.

![](generate/scratch/17592186157298/assets/d16d7bbeaadb2ea5b7228871-solution.png)

As a result, the region can be expressed in polar coordinates as

$$\Delta=\{(r,\theta):\frac{3 \sqrt{2}}{\sin{\left(\theta \right)}}\leq r\leq 6,\ \frac{\pi}{4}\leq\theta\leq \frac{\pi}{2}\}.$$

Therefore, using the change of variables formula, we obtain

$$\iint_D x^{2}\,\mathrm{d}A=\iint_\Delta r^{3} \cos^{2}{\left(\theta \right)}\,\mathrm{d}r\,\mathrm{d}\theta=\int_{\frac{\pi}{4}}^{\frac{\pi}{2}}\left(\cos^{2}{\left(\theta \right)}\right)\int_{3 \sqrt{2} \csc{\left(\theta \right)}}^{6}r^{3}\,\mathrm{d}r\,\mathrm{d}\theta.$$
