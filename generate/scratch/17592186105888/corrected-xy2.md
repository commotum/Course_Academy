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