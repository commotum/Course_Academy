![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/6385f17950d6e41f410131df0889429bb9ae37cbb1dc832c3a1b04883d3081a1.png)

Evaluate the surface integral

$$\iint_S 3 x y\,\mathrm{d}S,$$

where $S$ is defined by $z=\sqrt{2} x + \sqrt{2} y$ and whose domain is the quarter-circle in the second quadrant of radius $3$ centered at $O$, as shown above. Give an exact answer.

- $- \frac{243 \sqrt{5}}{8}$
- $- \frac{243 \sqrt{5}}{128}$
- $- \frac{1215}{8}$
- $- \frac{243 \sqrt{5}}{16}$
- $- \frac{243}{8}$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2},$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2}.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{3 x y}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(3 x y)\cdot\sqrt{1+(\sqrt{2})^2+(\sqrt{2})^2}}\,\mathrm{d}A \\ & =\iint_D{(3 x y)\cdot\sqrt{5}}\,\mathrm{d}A \\ & =(\sqrt{5})\iint_D{3 x y}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 3,\ \frac{\pi}{2}\le\theta\le \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(\sqrt{5})\iint_D{3 x y}\,\mathrm{d}A & =(\sqrt{5})\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{(3(r\cos\theta)(r\sin\theta))\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{\frac{3 r^{3} \sin{\left(2 \theta \right)}}{2}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{\pi}{2}}^{\pi}{(\sin{\left(2 \theta \right)})\int_{0}^{3}{\frac{3 r^{3}}{2}}\,\mathrm{d}r}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{\pi}{2}}^{\pi}{(\sin{\left(2 \theta \right)})\left[\frac{3 r^{4}}{8}\right]_{0}^{3}}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{\pi}{2}}^{\pi}{(\sin{\left(2 \theta \right)})\left[((\frac{243}{8}))-((0))\right]}\,\mathrm{d}\theta \\ & =(\sqrt{5})\int_{\frac{\pi}{2}}^{\pi}{\frac{243 \sin{\left(2 \theta \right)}}{8}}\,\mathrm{d}\theta \\ & =(\frac{243 \sqrt{5}}{16})\left[- \cos{\left(2 \theta \right)}\right]_{\frac{\pi}{2}}^{\pi} \\ & =(\frac{243 \sqrt{5}}{16})\left[((-1))-((1))\right] \\ & =(\frac{243 \sqrt{5}}{16})\cdot((-1)-(1)) \\ & =- \frac{243 \sqrt{5}}{8}.\end{aligned}
$$

Therefore, the surface integral is $- \frac{243 \sqrt{5}}{8}$.