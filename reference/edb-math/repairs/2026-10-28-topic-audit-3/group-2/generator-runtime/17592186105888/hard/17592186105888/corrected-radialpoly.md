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