![](/home/jake/Developer/Course_Academy/generate/scratch/17592186105888/plots/6385f17950d6e41f410131df0889429bb9ae37cbb1dc832c3a1b04883d3081a1.png)

Evaluate the surface integral

$$\iint_S \frac{3 x}{x^{2} + y^{2}}\,\mathrm{d}S,$$

where $S$ is defined by $z=\sqrt{2} x + \sqrt{2} y$ and whose domain is the quarter-circle in the second quadrant of radius $3$ centered at $O$, as shown above. Give an exact answer. The value at $O$ may be assigned arbitrarily; it does not affect the integral.

- $- 9 \sqrt{5}$
- $- \frac{9 \sqrt{5}}{2}$
- $-45$
- $\frac{9 \sqrt{5} \left(-2 + \sqrt{2}\right)}{2}$
- $-9$

For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by

$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$

For the partial derivatives, we have

$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2},$$

and

$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}(\sqrt{2} x + \sqrt{2} y)=\sqrt{2}.$$

Therefore, the surface integral can be expressed as follows:

$$
\begin{aligned}\iint_S{\frac{3 x}{x^{2} + y^{2}}}\,\mathrm{d}S & =\iint_D{f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}}\,\mathrm{d}A \\ & =\iint_D{(\frac{3 x}{x^{2} + y^{2}})\cdot\sqrt{1+(\sqrt{2})^2+(\sqrt{2})^2}}\,\mathrm{d}A \\ & =\iint_D{(\frac{3 x}{x^{2} + y^{2}})\cdot\sqrt{5}}\,\mathrm{d}A \\ & =(\sqrt{5})\iint_D{\frac{3 x}{x^{2} + y^{2}}}\,\mathrm{d}A.\end{aligned}
$$

Notice that in polar coordinates $(r,\theta),$ our domain can be expressed as

$$\Delta=\{(r,\theta):0\le r\le 3,\ \frac{\pi}{2}\le\theta\le \pi\}.$$

Therefore, using the change of variables formula for polar coordinates, where $x=r\cos\theta$ and $y=r\sin\theta,$ we obtain

$$
\begin{aligned}(\sqrt{5})\iint_D{\frac{3 x}{x^{2} + y^{2}}}\,\mathrm{d}A & =(\sqrt{5})\iint_\Delta{f(r\cos\theta,r\sin\theta)\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{(\frac{3(r\cos\theta)}{r^2\cos^2\theta+r^2\sin^2\theta})\cdot r}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{\frac{3r^2\cos\theta}{r^2(\cos^2\theta+\sin^2\theta)}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(\sqrt{5})\iint_\Delta{3 \cos{\left(\theta \right)}}\,\mathrm{d}r\,\mathrm{d}\theta \\ & =(3 \sqrt{5})\int_{0}^{3}{\int_{\frac{\pi}{2}}^{\pi}{\cos{\left(\theta \right)}}\,\mathrm{d}\theta}\,\mathrm{d}r \\ & =(3 \sqrt{5})\int_{0}^{3}{\left[\sin{\left(\theta \right)}\right]_{\frac{\pi}{2}}^{\pi}}\,\mathrm{d}r \\ & =(3 \sqrt{5})\int_{0}^{3}{\left[((0))-((1))\right]}\,\mathrm{d}r \\ & =(3 \sqrt{5})\int_{0}^{3}{-1}\,\mathrm{d}r \\ & =(- \sqrt{5})\left[3 r\right]_{0}^{3} \\ & =(- \sqrt{5})\left[((9))-((0))\right] \\ & =(\sqrt{5})\cdot(-1)\cdot(9) \\ & =- 9 \sqrt{5}.\end{aligned}
$$

Therefore, the surface integral is $- 9 \sqrt{5}$.