Evaluate the triple integral

$$
\iiint_R 2\cdot \sqrt{(x)^{2}+(y)^{2}}\,\mathrm{d}V
$$

over the region $R$ enclosed inside the cylinder $x^2+y^2=9$ and between the surfaces $z=0$ and $z=1.$

- $72\cdot \pi$
- $\frac{9}{2}\cdot \pi$
- $36\cdot \pi$
- $81\cdot \pi$
- $18\cdot \pi$

We will use the change of variables formula in the form

$$
\iiint_R f(x,y,z)\,dV=\iiint_\Delta f(r\cos\theta,r\sin\theta,z)\,r\,dz\,dr\,d\theta.
$$

If $(r,\theta,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\cos\theta,\quad y=r\sin\theta,\quad z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129278/assets/2e5f535e082c5a993b7aa8bd.png)

The region $R$ is a right vertical cylinder of radius $3$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0=0,$ and

- bounded above by $z=1=1.$

As a result, in cylindrical polar coordinates, our region can be expressed as

$$
\Delta=\{(r,\theta,z):0\le r\le 3,\ 0\le\theta<2\cdot \pi,\ 0\le z\le 1\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iiint_R 2\cdot \sqrt{(x)^{2}+(y)^{2}}\,dV &=\iiint_\Delta (2\cdot \sqrt{(r\cdot \cos(\theta))^2+(r\cdot \sin(\theta))^2})\cdot r\,dz\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{3}\int_{0}^{1}2\cdot (r)^{2}\,dz\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{3}2\cdot (r)^{2}[z]_{z=0}^{z=1}\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{3}2\cdot (r)^{2}((1)-(0))\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{3}2\cdot (r)^{2}\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}[\frac{2}{3}\cdot (r)^{3}]_{r=0}^{r=3}\,d\theta \\ &=\int_{0}^{2\cdot \pi}(\frac{2}{3}\cdot ((3))^{3})-(\frac{2}{3}\cdot ((0))^{3})\,d\theta \\ &=\int_{0}^{2\cdot \pi}(18)-(0)\,d\theta \\ &=\int_{0}^{2\cdot \pi}18\,d\theta \\ &=[18\cdot \theta]_{\theta=0}^{\theta=2\cdot \pi} \\ &=(36\cdot \pi)-(0) \\ &=36\cdot \pi\end{aligned}
$$

---

Evaluate the triple integral

$$
\iiint_R \sqrt{(x)^{2}+(y)^{2}}\,\mathrm{d}V
$$

over the region $R$ enclosed inside the cylinder $x^2+y^2=1$ and between the surfaces $z=0$ and $z=3.$

- $2\cdot \pi$
- $\frac{1}{4}\cdot \pi$
- $4\cdot \pi$
- $\pi$
- $\frac{3}{2}\cdot \pi$

We will use the change of variables formula in the form

$$
\iiint_R f(x,y,z)\,dV=\iiint_\Delta f(r\cos\theta,r\sin\theta,z)\,r\,dz\,dr\,d\theta.
$$

If $(r,\theta,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\cos\theta,\quad y=r\sin\theta,\quad z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129278/assets/38fe82f02a8d8618201b4bb6.png)

The region $R$ is a right vertical cylinder of radius $1$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0=0,$ and

- bounded above by $z=3=3.$

As a result, in cylindrical polar coordinates, our region can be expressed as

$$
\Delta=\{(r,\theta,z):0\le r\le 1,\ 0\le\theta<2\cdot \pi,\ 0\le z\le 3\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iiint_R \sqrt{(x)^{2}+(y)^{2}}\,dV &=\iiint_\Delta (\sqrt{(r\cdot \cos(\theta))^2+(r\cdot \sin(\theta))^2})\cdot r\,dz\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{1}\int_{0}^{3}(r)^{2}\,dz\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{1}(r)^{2}[z]_{z=0}^{z=3}\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{1}(r)^{2}((3)-(0))\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{1}3\cdot (r)^{2}\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}[(r)^{3}]_{r=0}^{r=1}\,d\theta \\ &=\int_{0}^{2\cdot \pi}(((1))^{3})-(((0))^{3})\,d\theta \\ &=\int_{0}^{2\cdot \pi}(1)-(0)\,d\theta \\ &=\int_{0}^{2\cdot \pi}1\,d\theta \\ &=[\theta]_{\theta=0}^{\theta=2\cdot \pi} \\ &=(2\cdot \pi)-(0) \\ &=2\cdot \pi\end{aligned}
$$

---

Evaluate the triple integral

$$
\iiint_R 4\cdot \sqrt{(x)^{2}+(y)^{2}}\,\mathrm{d}V
$$

over the region $R$ enclosed inside the cylinder $x^2+y^2=1$ and between the surfaces $z=0$ and $z=4.$

- $\frac{64}{3}\cdot \pi$
- $8\cdot \pi$
- $\frac{16}{3}\cdot \pi$
- $\frac{32}{3}\cdot \pi$
- $\frac{4}{3}\cdot \pi$

We will use the change of variables formula in the form

$$
\iiint_R f(x,y,z)\,dV=\iiint_\Delta f(r\cos\theta,r\sin\theta,z)\,r\,dz\,dr\,d\theta.
$$

If $(r,\theta,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\cos\theta,\quad y=r\sin\theta,\quad z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129278/assets/38fe82f02a8d8618201b4bb6.png)

The region $R$ is a right vertical cylinder of radius $1$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0=0,$ and

- bounded above by $z=4=4.$

As a result, in cylindrical polar coordinates, our region can be expressed as

$$
\Delta=\{(r,\theta,z):0\le r\le 1,\ 0\le\theta<2\cdot \pi,\ 0\le z\le 4\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iiint_R 4\cdot \sqrt{(x)^{2}+(y)^{2}}\,dV &=\iiint_\Delta (4\cdot \sqrt{(r\cdot \cos(\theta))^2+(r\cdot \sin(\theta))^2})\cdot r\,dz\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{1}\int_{0}^{4}4\cdot (r)^{2}\,dz\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{1}4\cdot (r)^{2}[z]_{z=0}^{z=4}\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{1}4\cdot (r)^{2}((4)-(0))\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{1}16\cdot (r)^{2}\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}[\frac{16}{3}\cdot (r)^{3}]_{r=0}^{r=1}\,d\theta \\ &=\int_{0}^{2\cdot \pi}(\frac{16}{3}\cdot ((1))^{3})-(\frac{16}{3}\cdot ((0))^{3})\,d\theta \\ &=\int_{0}^{2\cdot \pi}(\frac{16}{3})-(0)\,d\theta \\ &=\int_{0}^{2\cdot \pi}\frac{16}{3}\,d\theta \\ &=[\frac{16}{3}\cdot \theta]_{\theta=0}^{\theta=2\cdot \pi} \\ &=(\frac{32}{3}\cdot \pi)-(0) \\ &=\frac{32}{3}\cdot \pi\end{aligned}
$$

---

Evaluate the triple integral

$$
\iiint_R 4\cdot \sqrt{(x)^{2}+(y)^{2}}\,\mathrm{d}V
$$

over the region $R$ enclosed inside the cylinder $x^2+y^2=4$ and between the surfaces $z=0$ and $z=1.$

- $\frac{32}{3}\cdot \pi$
- $\frac{8}{3}\cdot \pi$
- $\frac{64}{3}\cdot \pi$
- $\frac{128}{3}\cdot \pi$
- $32\cdot \pi$

We will use the change of variables formula in the form

$$
\iiint_R f(x,y,z)\,dV=\iiint_\Delta f(r\cos\theta,r\sin\theta,z)\,r\,dz\,dr\,d\theta.
$$

If $(r,\theta,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\cos\theta,\quad y=r\sin\theta,\quad z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129278/assets/8a2f6b783e025b1eee0e1d65.png)

The region $R$ is a right vertical cylinder of radius $2$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0=0,$ and

- bounded above by $z=1=1.$

As a result, in cylindrical polar coordinates, our region can be expressed as

$$
\Delta=\{(r,\theta,z):0\le r\le 2,\ 0\le\theta<2\cdot \pi,\ 0\le z\le 1\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iiint_R 4\cdot \sqrt{(x)^{2}+(y)^{2}}\,dV &=\iiint_\Delta (4\cdot \sqrt{(r\cdot \cos(\theta))^2+(r\cdot \sin(\theta))^2})\cdot r\,dz\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{2}\int_{0}^{1}4\cdot (r)^{2}\,dz\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{2}4\cdot (r)^{2}[z]_{z=0}^{z=1}\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{2}4\cdot (r)^{2}((1)-(0))\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{2}4\cdot (r)^{2}\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}[\frac{4}{3}\cdot (r)^{3}]_{r=0}^{r=2}\,d\theta \\ &=\int_{0}^{2\cdot \pi}(\frac{4}{3}\cdot ((2))^{3})-(\frac{4}{3}\cdot ((0))^{3})\,d\theta \\ &=\int_{0}^{2\cdot \pi}(\frac{32}{3})-(0)\,d\theta \\ &=\int_{0}^{2\cdot \pi}\frac{32}{3}\,d\theta \\ &=[\frac{32}{3}\cdot \theta]_{\theta=0}^{\theta=2\cdot \pi} \\ &=(\frac{64}{3}\cdot \pi)-(0) \\ &=\frac{64}{3}\cdot \pi\end{aligned}
$$

---

Evaluate the triple integral

$$
\iiint_R \sqrt{(x)^{2}+(y)^{2}}\,\mathrm{d}V
$$

over the region $R$ enclosed inside the cylinder $x^2+y^2=16$ and between the surfaces $z=0$ and $z=3.$

- $16\cdot \pi$
- $256\cdot \pi$
- $64\cdot \pi$
- $128\cdot \pi$
- $384\cdot \pi$

We will use the change of variables formula in the form

$$
\iiint_R f(x,y,z)\,dV=\iiint_\Delta f(r\cos\theta,r\sin\theta,z)\,r\,dz\,dr\,d\theta.
$$

If $(r,\theta,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\cos\theta,\quad y=r\sin\theta,\quad z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129278/assets/2b0ce93bf4613b316d131b31.png)

The region $R$ is a right vertical cylinder of radius $4$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0=0,$ and

- bounded above by $z=3=3.$

As a result, in cylindrical polar coordinates, our region can be expressed as

$$
\Delta=\{(r,\theta,z):0\le r\le 4,\ 0\le\theta<2\cdot \pi,\ 0\le z\le 3\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iiint_R \sqrt{(x)^{2}+(y)^{2}}\,dV &=\iiint_\Delta (\sqrt{(r\cdot \cos(\theta))^2+(r\cdot \sin(\theta))^2})\cdot r\,dz\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{4}\int_{0}^{3}(r)^{2}\,dz\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{4}(r)^{2}[z]_{z=0}^{z=3}\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{4}(r)^{2}((3)-(0))\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{4}3\cdot (r)^{2}\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}[(r)^{3}]_{r=0}^{r=4}\,d\theta \\ &=\int_{0}^{2\cdot \pi}(((4))^{3})-(((0))^{3})\,d\theta \\ &=\int_{0}^{2\cdot \pi}(64)-(0)\,d\theta \\ &=\int_{0}^{2\cdot \pi}64\,d\theta \\ &=[64\cdot \theta]_{\theta=0}^{\theta=2\cdot \pi} \\ &=(128\cdot \pi)-(0) \\ &=128\cdot \pi\end{aligned}
$$

---

Evaluate the triple integral

$$
\iiint_R 2\cdot z\cdot ((x)^{2}+(y)^{2})^{-\frac{1}{2}}\,\mathrm{d}V
$$

over the region $R$ enclosed inside the cylinder $x^2+y^2=9$ and between the surfaces $z=0$ and $z=\sqrt{-(x)^{2}+(y)^{2}+14}.$

- $66\cdot \pi$
- $42\cdot \pi$
- $84\cdot \pi$
- $252\cdot \pi$
- $168\cdot \pi$

We will use the change of variables formula in the form

$$
\iiint_R f(x,y,z)\,dV=\iiint_\Delta f(r\cos\theta,r\sin\theta,z)\,r\,dz\,dr\,d\theta.
$$

If $(r,\theta,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\cos\theta,\quad y=r\sin\theta,\quad z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129278/assets/2e5f535e082c5a993b7aa8bd.png)

The region $R$ is a right vertical cylinder of radius $3$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0=0,$ and

- bounded above by $z=\sqrt{-(x)^{2}+(y)^{2}+14}=\sqrt{-(r)^{2}\cdot \cos(2\cdot \theta)+14}.$

As a result, in cylindrical polar coordinates, our region can be expressed as

$$
\Delta=\{(r,\theta,z):0\le r\le 3,\ 0\le\theta<2\cdot \pi,\ 0\le z\le \sqrt{-(r)^{2}\cdot \cos(2\cdot \theta)+14}\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iiint_R 2\cdot z\cdot ((x)^{2}+(y)^{2})^{-\frac{1}{2}}\,dV &=\iiint_\Delta (2\cdot \frac{z}{\sqrt{(r\cdot \cos(\theta))^2+(r\cdot \sin(\theta))^2}})\cdot r\,dz\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{3}\int_{0}^{\sqrt{-(r)^{2}\cdot \cos(2\cdot \theta)+14}}2\cdot z\,dz\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{3}[(z)^{2}]_{z=0}^{z=\sqrt{-(r)^{2}\cdot \cos(2\cdot \theta)+14}}\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{3}(((\sqrt{-(r)^{2}\cdot \cos(2\cdot \theta)+14}))^{2})-(((0))^{2})\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{3}-(r)^{2}\cdot \cos(2\cdot \theta)+14\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}[-\frac{1}{3}\cdot (r)^{3}\cdot \cos(2\cdot \theta)+14\cdot r]_{r=0}^{r=3}\,d\theta \\ &=\int_{0}^{2\cdot \pi}(-\frac{1}{3}\cdot ((3))^{3}\cdot \cos(2\cdot \theta))-(-\frac{1}{3}\cdot ((0))^{3}\cdot \cos(2\cdot \theta))+(14\cdot (3))-(14\cdot (0))\,d\theta \\ &=\int_{0}^{2\cdot \pi}(-9\cdot \cos(2\cdot \theta))-(0)+(42)-(0)\,d\theta \\ &=\int_{0}^{2\cdot \pi}42-9\cdot \cos(2\cdot \theta)\,d\theta \\ &=[42\cdot \theta-9\cdot \cos(\theta)\cdot \sin(\theta)]_{\theta=0}^{\theta=2\cdot \pi} \\ &=(84\cdot \pi)-(0)+(0)-(0) \\ &=84\cdot \pi\end{aligned}
$$

---

Evaluate the triple integral

$$
\iiint_R \sqrt{(x)^{2}+(y)^{2}}\,\mathrm{d}V
$$

over the region $R$ enclosed inside the cylinder $x^2+y^2=1$ and between the surfaces $z=0$ and $z=9-2\cdot y.$

- $6\cdot \pi$
- $\frac{3}{4}\cdot \pi$
- $12\cdot \pi$
- $-1+3\cdot \pi$
- $\frac{9}{2}\cdot \pi$

We will use the change of variables formula in the form

$$
\iiint_R f(x,y,z)\,dV=\iiint_\Delta f(r\cos\theta,r\sin\theta,z)\,r\,dz\,dr\,d\theta.
$$

If $(r,\theta,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\cos\theta,\quad y=r\sin\theta,\quad z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129278/assets/38fe82f02a8d8618201b4bb6.png)

The region $R$ is a right vertical cylinder of radius $1$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0=0,$ and

- bounded above by $z=9-2\cdot y=-2\cdot r\cdot \sin(\theta)+9.$

As a result, in cylindrical polar coordinates, our region can be expressed as

$$
\Delta=\{(r,\theta,z):0\le r\le 1,\ 0\le\theta<2\cdot \pi,\ 0\le z\le -2\cdot r\cdot \sin(\theta)+9\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iiint_R \sqrt{(x)^{2}+(y)^{2}}\,dV &=\iiint_\Delta (\sqrt{(r\cdot \cos(\theta))^2+(r\cdot \sin(\theta))^2})\cdot r\,dz\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{1}\int_{0}^{-2\cdot r\cdot \sin(\theta)+9}(r)^{2}\,dz\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{1}(r)^{2}[z]_{z=0}^{z=-2\cdot r\cdot \sin(\theta)+9}\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{1}(r)^{2}((-2\cdot r\cdot \sin(\theta)+9)-(0))\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{1}-2\cdot (r)^{3}\cdot \sin(\theta)+9\cdot (r)^{2}\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}[-\frac{1}{2}\cdot (r)^{4}\cdot \sin(\theta)+3\cdot (r)^{3}]_{r=0}^{r=1}\,d\theta \\ &=\int_{0}^{2\cdot \pi}(-\frac{1}{2}\cdot ((1))^{4}\cdot \sin(\theta))-(-\frac{1}{2}\cdot ((0))^{4}\cdot \sin(\theta))+(3\cdot ((1))^{3})-(3\cdot ((0))^{3})\,d\theta \\ &=\int_{0}^{2\cdot \pi}(-\frac{1}{2}\cdot \sin(\theta))-(0)+(3)-(0)\,d\theta \\ &=\int_{0}^{2\cdot \pi}3-\frac{1}{2}\cdot \sin(\theta)\,d\theta \\ &=[3\cdot \theta+\frac{1}{2}\cdot \cos(\theta)]_{\theta=0}^{\theta=2\cdot \pi} \\ &=(6\cdot \pi)-(0)+(\frac{1}{2})-(\frac{1}{2}) \\ &=6\cdot \pi\end{aligned}
$$

---

Evaluate the triple integral

$$
\iiint_R 4\cdot \sqrt{(x)^{2}+(y)^{2}}\,\mathrm{d}V
$$

over the region $R$ enclosed inside the cylinder $x^2+y^2=2$ and between the surfaces $z=0$ and $z=5-2\cdot y.$

- $-16+\frac{40}{3}\cdot \pi\cdot \sqrt{2}$
- $40\cdot \pi$
- $\frac{10}{3}\cdot \pi\cdot \sqrt{2}$
- $\frac{160}{3}\cdot \pi\cdot \sqrt{2}$
- $\frac{80}{3}\cdot \pi\cdot \sqrt{2}$

We will use the change of variables formula in the form

$$
\iiint_R f(x,y,z)\,dV=\iiint_\Delta f(r\cos\theta,r\sin\theta,z)\,r\,dz\,dr\,d\theta.
$$

If $(r,\theta,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\cos\theta,\quad y=r\sin\theta,\quad z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129278/assets/af599b3c1605940d549ea99d.png)

The region $R$ is a right vertical cylinder of radius $\sqrt{2}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=0=0,$ and

- bounded above by $z=5-2\cdot y=-2\cdot r\cdot \sin(\theta)+5.$

As a result, in cylindrical polar coordinates, our region can be expressed as

$$
\Delta=\{(r,\theta,z):0\le r\le \sqrt{2},\ 0\le\theta<2\cdot \pi,\ 0\le z\le -2\cdot r\cdot \sin(\theta)+5\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iiint_R 4\cdot \sqrt{(x)^{2}+(y)^{2}}\,dV &=\iiint_\Delta (4\cdot \sqrt{(r\cdot \cos(\theta))^2+(r\cdot \sin(\theta))^2})\cdot r\,dz\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{\sqrt{2}}\int_{0}^{-2\cdot r\cdot \sin(\theta)+5}4\cdot (r)^{2}\,dz\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{\sqrt{2}}4\cdot (r)^{2}[z]_{z=0}^{z=-2\cdot r\cdot \sin(\theta)+5}\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{\sqrt{2}}4\cdot (r)^{2}((-2\cdot r\cdot \sin(\theta)+5)-(0))\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}\int_0^{\sqrt{2}}-8\cdot (r)^{3}\cdot \sin(\theta)+20\cdot (r)^{2}\,dr\,d\theta \\ &=\int_{0}^{2\cdot \pi}[-2\cdot (r)^{4}\cdot \sin(\theta)+\frac{20}{3}\cdot (r)^{3}]_{r=0}^{r=\sqrt{2}}\,d\theta \\ &=\int_{0}^{2\cdot \pi}(-2\cdot ((\sqrt{2}))^{4}\cdot \sin(\theta))-(-2\cdot ((0))^{4}\cdot \sin(\theta))+(\frac{20}{3}\cdot ((\sqrt{2}))^{3})-(\frac{20}{3}\cdot ((0))^{3})\,d\theta \\ &=\int_{0}^{2\cdot \pi}(-8\cdot \sin(\theta))-(0)+(\frac{40}{3}\cdot \sqrt{2})-(0)\,d\theta \\ &=\int_{0}^{2\cdot \pi}-8\cdot \sin(\theta)+\frac{40}{3}\cdot \sqrt{2}\,d\theta \\ &=[\frac{40}{3}\cdot \theta\cdot \sqrt{2}+8\cdot \cos(\theta)]_{\theta=0}^{\theta=2\cdot \pi} \\ &=(\frac{80}{3}\cdot \pi\cdot \sqrt{2})-(0)+(8)-(8) \\ &=\frac{80}{3}\cdot \pi\cdot \sqrt{2}\end{aligned}
$$

---

Evaluate the triple integral

$$
\iiint_R 2\cdot x\cdot z\,\mathrm{d}V
$$

over the region $R$ enclosed inside the cylinder $x^2+y^2=6$ for $y\ge 0$ and between the surfaces $z=-x$ and $z=x+10.$

- $180\cdot \pi$
- $\frac{45}{8}\cdot \pi$
- $90\cdot \pi$
- $72\cdot \pi\cdot \sqrt{6}$
- $45\cdot \pi+200\cdot \sqrt{6}$

We will use the change of variables formula in the form

$$
\iiint_R f(x,y,z)\,dV=\iiint_\Delta f(r\cos\theta,r\sin\theta,z)\,r\,dz\,dr\,d\theta.
$$

If $(r,\theta,z)$ are the cylindrical polar coordinates of a point, then its Cartesian coordinates $(x,y,z)$ can be found by using the formulas

$$
x=r\cos\theta,\quad y=r\sin\theta,\quad z=z.
$$

First, let's sketch the projection of $R$ onto the $xy$-plane:

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129278/assets/9ba8eff9bde9cf83b3caf366.png)

The region $R$ is a right vertical cylinder of radius $\sqrt{6}$ whose axis passes through the point $(0,0)$ in the $xy$-plane, and is

- bounded below by $z=-x=-r\cdot \cos(\theta),$ and

- bounded above by $z=x+10=r\cdot \cos(\theta)+10.$

As a result, in cylindrical polar coordinates, our region can be expressed as

$$
\Delta=\{(r,\theta,z):0\le r\le \sqrt{6},\ 0\le\theta<\pi,\ -r\cdot \cos(\theta)\le z\le r\cdot \cos(\theta)+10\}.
$$

Therefore, using the change of variables formula, we obtain

$$
\begin{aligned}\iiint_R 2\cdot x\cdot z\,dV &=\iiint_\Delta (2\cdot z\cdot r\cdot \cos(\theta))\cdot r\,dz\,dr\,d\theta \\ &=\int_{0}^{\pi}\int_0^{\sqrt{6}}\int_{-r\cdot \cos(\theta)}^{r\cdot \cos(\theta)+10}2\cdot z\cdot (r)^{2}\cdot \cos(\theta)\,dz\,dr\,d\theta \\ &=\int_{0}^{\pi}\int_0^{\sqrt{6}}(r)^{2}\cdot \cos(\theta)[(z)^2]_{z=-r\cdot \cos(\theta)}^{z=r\cdot \cos(\theta)+10}\,dr\,d\theta \\ &=\int_{0}^{\pi}\int_0^{\sqrt{6}}(r)^{2}\cdot \cos(\theta)((r\cdot \cos(\theta)+10)^2-(-r\cdot \cos(\theta))^2)\,dr\,d\theta \\ &=\int_{0}^{\pi}\int_0^{\sqrt{6}}(r)^{2}\cdot \cos(\theta)((r)^{2}\cdot (\cos(\theta))^{2}+20\cdot r\cdot \cos(\theta)+100-((r)^{2}\cdot (\cos(\theta))^{2}))\,dr\,d\theta \\ &=\int_{0}^{\pi}\int_0^{\sqrt{6}}20\cdot (r)^{3}\cdot (\cos(\theta))^{2}+100\cdot (r)^{2}\cdot \cos(\theta)\,dr\,d\theta \\ &=\int_{0}^{\pi}[5\cdot (r)^{4}\cdot (\cos(\theta))^{2}+\frac{100}{3}\cdot (r)^{3}\cdot \cos(\theta)]_{r=0}^{r=\sqrt{6}}\,d\theta \\ &=\int_{0}^{\pi}(5\cdot ((\sqrt{6}))^{4}\cdot (\cos(\theta))^{2})-(5\cdot ((0))^{4}\cdot (\cos(\theta))^{2})+(\frac{100}{3}\cdot ((\sqrt{6}))^{3}\cdot \cos(\theta))-(\frac{100}{3}\cdot ((0))^{3}\cdot \cos(\theta))\,d\theta \\ &=\int_{0}^{\pi}(180\cdot (\cos(\theta))^{2})-(0)+(200\cdot \sqrt{6}\cdot \cos(\theta))-(0)\,d\theta \\ &=\int_{0}^{\pi}180\cdot (\cos(\theta))^{2}+200\cdot \sqrt{6}\cdot \cos(\theta)\,d\theta \\ &=\int_{0}^{\pi}180(\frac{1}{2}(1+\cos(2\cdot \theta)))+200\cdot \sqrt{6}\cdot \cos(\theta)\,d\theta \\ &=\int_{0}^{\pi}200\cdot \sqrt{6}\cdot \cos(\theta)+90\cdot \cos(2\cdot \theta)+90\,d\theta \\ &=[90\cdot \theta+200\cdot \sqrt{6}\cdot \sin(\theta)+45\cdot \sin(2\cdot \theta)]_{\theta=0}^{\theta=\pi} \\ &=(90\cdot \pi)-(0)+(0)-(0)+(0)-(0) \\ &=90\cdot \pi\end{aligned}
$$
