Use a change of variables to evaluate the double integral 

$$
\iint_D 2 y^{2} \left(2 x + 2 y\right)\,\mathrm{d}x\,\mathrm{d}y,
$$

where $D$ is the quadrilateral region with vertices $(\frac{3}{2},0)$, $(\frac{5}{2},0)$, $(- \frac{1}{2},3)$ and $(- \frac{3}{2},3)$.

1. $144$
2. $72$
3. $-72$
4. $216$
5. $18$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\text{ }dxdy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))\,|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

To compute the required integral, we proceed as follows:

**Step 1**: Find a suitable change of variables.

The integrand

$$
f(x,y)=2 y^{2} \left(2 x + 2 y\right)
$$

suggests that we use the change of variables 

$$
u=2 x + 2 y,\qquad v=y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y)\mapsto (u(x,y),v(x,y)).
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

The vertices of our domain $Δ$ in the $uv$-plane are as follows:

$$
\begin{aligned}T^{-1}(\frac{3}{2},0)&=(\left(2\right)\cdot \left(\frac{3}{2}\right)+\left(2\right)\cdot \left(0\right)+\left(0\right),\left(0\right)\cdot \left(\frac{3}{2}\right)+\left(1\right)\cdot \left(0\right)+\left(0\right)) \\ &=(3,0) \\ T^{-1}(\frac{5}{2},0)&=(\left(2\right)\cdot \left(\frac{5}{2}\right)+\left(2\right)\cdot \left(0\right)+\left(0\right),\left(0\right)\cdot \left(\frac{5}{2}\right)+\left(1\right)\cdot \left(0\right)+\left(0\right)) \\ &=(5,0) \\ T^{-1}(- \frac{1}{2},3)&=(\left(2\right)\cdot \left(- \frac{1}{2}\right)+\left(2\right)\cdot \left(3\right)+\left(0\right),\left(0\right)\cdot \left(- \frac{1}{2}\right)+\left(1\right)\cdot \left(3\right)+\left(0\right)) \\ &=(5,3) \\ T^{-1}(- \frac{3}{2},3)&=(\left(2\right)\cdot \left(- \frac{3}{2}\right)+\left(2\right)\cdot \left(3\right)+\left(0\right),\left(0\right)\cdot \left(- \frac{3}{2}\right)+\left(1\right)\cdot \left(3\right)+\left(0\right)) \\ &=(3,3)\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v):3\le u\le 5,\ 0\le v\le 3\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186198374/plots/0368e0c9d77542498254.png)

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)}&=\begin{vmatrix}\partial u/\partial x&\partial u/\partial y\\\partial v/\partial x&\partial v/\partial y\end{vmatrix} \\ &=\begin{vmatrix}2&2\\0&1\end{vmatrix} \\ &=2.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=\frac{1}{2}
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving these affine equations also gives

$$
x=\frac{u}{2} - v,\qquad y=v.
$$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D 2 y^{2} \left(2 x + 2 y\right)\,\mathrm{d}x\,\mathrm{d}y&=\iint_\Delta 2 u v^{2}\,\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=\iint_\Delta 2 u v^{2}\,\left|\frac{1}{2}\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=1\cdot \int_{0}^{3}\int_{3}^{5}u v^{2}\,\mathrm{d}u\,\mathrm{d}v \\ &=1\cdot \int_{0}^{3}v^{2}\,\mathrm{d}v\cdot \int_{3}^{5}u\,\mathrm{d}u \\ &=1\cdot \left[\frac{v^{3}}{3}\right]_{0}^{3}\cdot \left[\frac{u^{2}}{2}\right]_{3}^{5} \\ &=1\cdot \left(\left(3\right)^{3}/3-\left(\left(0\right)^{3}/3\right)\right)\cdot \left(\left(5\right)^{2}/2-\left(\left(3\right)^{2}/2\right)\right) \\ &=1\cdot \left(\left(9\right)-\left(0\right)\right)\cdot \left(\left(\frac{25}{2}\right)-\left(\frac{9}{2}\right)\right) \\ &=1\cdot \left(9\right)\cdot \left(8\right) \\ &=72.\end{aligned}
$$



---

Use a change of variables to evaluate the double integral 

$$
\iint_D 2 \left(x + 2 y\right)^{2} \left(3 x + 3\right)\,\mathrm{d}x\,\mathrm{d}y,
$$

where $D$ is the quadrilateral region with vertices $(0,\frac{1}{2})$, $(\frac{2}{3},\frac{1}{6})$, $(\frac{2}{3},\frac{5}{3})$ and $(0,2)$.

1. $112$
2. $56$
3. $-56$
4. $168$
5. $14$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\text{ }dxdy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))\,|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

To compute the required integral, we proceed as follows:

**Step 1**: Find a suitable change of variables.

The integrand

$$
f(x,y)=2 \left(x + 2 y\right)^{2} \left(3 x + 3\right)
$$

suggests that we use the change of variables 

$$
u=3 x + 3,\qquad v=x + 2 y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y)\mapsto (u(x,y),v(x,y)).
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

The vertices of our domain $Δ$ in the $uv$-plane are as follows:

$$
\begin{aligned}T^{-1}(0,\frac{1}{2})&=(\left(3\right)\cdot \left(0\right)+\left(0\right)\cdot \left(\frac{1}{2}\right)+\left(3\right),\left(1\right)\cdot \left(0\right)+\left(2\right)\cdot \left(\frac{1}{2}\right)+\left(0\right)) \\ &=(3,1) \\ T^{-1}(\frac{2}{3},\frac{1}{6})&=(\left(3\right)\cdot \left(\frac{2}{3}\right)+\left(0\right)\cdot \left(\frac{1}{6}\right)+\left(3\right),\left(1\right)\cdot \left(\frac{2}{3}\right)+\left(2\right)\cdot \left(\frac{1}{6}\right)+\left(0\right)) \\ &=(5,1) \\ T^{-1}(\frac{2}{3},\frac{5}{3})&=(\left(3\right)\cdot \left(\frac{2}{3}\right)+\left(0\right)\cdot \left(\frac{5}{3}\right)+\left(3\right),\left(1\right)\cdot \left(\frac{2}{3}\right)+\left(2\right)\cdot \left(\frac{5}{3}\right)+\left(0\right)) \\ &=(5,4) \\ T^{-1}(0,2)&=(\left(3\right)\cdot \left(0\right)+\left(0\right)\cdot \left(2\right)+\left(3\right),\left(1\right)\cdot \left(0\right)+\left(2\right)\cdot \left(2\right)+\left(0\right)) \\ &=(3,4)\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v):3\le u\le 5,\ 1\le v\le 4\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186198374/plots/aecef0bb6bbfbe33dcf4.png)

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)}&=\begin{vmatrix}\partial u/\partial x&\partial u/\partial y\\\partial v/\partial x&\partial v/\partial y\end{vmatrix} \\ &=\begin{vmatrix}3&0\\1&2\end{vmatrix} \\ &=6.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=\frac{1}{6}
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving these affine equations also gives

$$
x=\frac{u}{3} - 1,\qquad y=- \frac{u}{6} + \frac{v}{2} + \frac{1}{2}.
$$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D 2 \left(x + 2 y\right)^{2} \left(3 x + 3\right)\,\mathrm{d}x\,\mathrm{d}y&=\iint_\Delta 2 u v^{2}\,\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=\iint_\Delta 2 u v^{2}\,\left|\frac{1}{6}\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=\frac{1}{3}\cdot \int_{1}^{4}\int_{3}^{5}u v^{2}\,\mathrm{d}u\,\mathrm{d}v \\ &=\frac{1}{3}\cdot \int_{1}^{4}v^{2}\,\mathrm{d}v\cdot \int_{3}^{5}u\,\mathrm{d}u \\ &=\frac{1}{3}\cdot \left[\frac{v^{3}}{3}\right]_{1}^{4}\cdot \left[\frac{u^{2}}{2}\right]_{3}^{5} \\ &=\frac{1}{3}\cdot \left(\left(4\right)^{3}/3-\left(\left(1\right)^{3}/3\right)\right)\cdot \left(\left(5\right)^{2}/2-\left(\left(3\right)^{2}/2\right)\right) \\ &=\frac{1}{3}\cdot \left(\left(\frac{64}{3}\right)-\left(\frac{1}{3}\right)\right)\cdot \left(\left(\frac{25}{2}\right)-\left(\frac{9}{2}\right)\right) \\ &=\frac{1}{3}\cdot \left(21\right)\cdot \left(8\right) \\ &=56.\end{aligned}
$$



---

Use a change of variables to evaluate the double integral 

$$
\iint_D \frac{2 \left(x + y\right)^{2}}{3 x + y}\,\mathrm{d}x\,\mathrm{d}y,
$$

where $D$ is the quadrilateral region with vertices $(0,3)$, $(-1,6)$, $(0,5)$ and $(1,2)$.

1. $\frac{196}{3}$
2. $- \frac{98 \ln{\left(5 \right)}}{3} + \frac{98 \ln{\left(3 \right)}}{3}$
3. $\ln{\left(\frac{25}{9} \right)}$
4. $\ln{\left(\frac{315544362088404722164691426113114491869282574043609201908111572265625}{57264168970223481226273458862846808078011946889} \right)}$
5. $\frac{98 \ln{\left(\frac{5}{3} \right)}}{3}$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\text{ }dxdy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))\,|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

To compute the required integral, we proceed as follows:

**Step 1**: Find a suitable change of variables.

The integrand

$$
f(x,y)=\frac{2 \left(x + y\right)^{2}}{3 x + y}
$$

suggests that we use the change of variables 

$$
u=x + y,\qquad v=3 x + y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y)\mapsto (u(x,y),v(x,y)).
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

The vertices of our domain $Δ$ in the $uv$-plane are as follows:

$$
\begin{aligned}T^{-1}(0,3)&=(\left(1\right)\cdot \left(0\right)+\left(1\right)\cdot \left(3\right)+\left(0\right),\left(3\right)\cdot \left(0\right)+\left(1\right)\cdot \left(3\right)+\left(0\right)) \\ &=(3,3) \\ T^{-1}(-1,6)&=(\left(1\right)\cdot \left(-1\right)+\left(1\right)\cdot \left(6\right)+\left(0\right),\left(3\right)\cdot \left(-1\right)+\left(1\right)\cdot \left(6\right)+\left(0\right)) \\ &=(5,3) \\ T^{-1}(0,5)&=(\left(1\right)\cdot \left(0\right)+\left(1\right)\cdot \left(5\right)+\left(0\right),\left(3\right)\cdot \left(0\right)+\left(1\right)\cdot \left(5\right)+\left(0\right)) \\ &=(5,5) \\ T^{-1}(1,2)&=(\left(1\right)\cdot \left(1\right)+\left(1\right)\cdot \left(2\right)+\left(0\right),\left(3\right)\cdot \left(1\right)+\left(1\right)\cdot \left(2\right)+\left(0\right)) \\ &=(3,5)\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v):3\le u\le 5,\ 3\le v\le 5\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186198374/plots/deef48969aa633648d27.png)

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)}&=\begin{vmatrix}\partial u/\partial x&\partial u/\partial y\\\partial v/\partial x&\partial v/\partial y\end{vmatrix} \\ &=\begin{vmatrix}1&1\\3&1\end{vmatrix} \\ &=-2.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=- \frac{1}{2}
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving these affine equations also gives

$$
x=- \frac{u}{2} + \frac{v}{2},\qquad y=\frac{3 u}{2} - \frac{v}{2}.
$$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D \frac{2 \left(x + y\right)^{2}}{3 x + y}\,\mathrm{d}x\,\mathrm{d}y&=\iint_\Delta \frac{2 u^{2}}{v}\,\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=\iint_\Delta \frac{2 u^{2}}{v}\,\left|- \frac{1}{2}\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=\iint_\Delta \frac{u^{2}}{v}\,\mathrm{d}u\,\mathrm{d}v \\ &=1\cdot \int_{3}^{5}\int_{3}^{5}\frac{u^{2}}{v}\,\mathrm{d}u\,\mathrm{d}v \\ &=1\cdot \int_{3}^{5}u^{2}\,\mathrm{d}u\cdot \int_{3}^{5}\frac{1}{v}\,\mathrm{d}v \\ &=1\cdot \left[\frac{u^{3}}{3}\right]_{3}^{5}\cdot \left[\ln{\left(v \right)}\right]_{3}^{5} \\ &=1\cdot \left(\left(5\right)^{3}/3-\left(\left(3\right)^{3}/3\right)\right)\cdot \left(\ln \left(5\right)-\left(\ln \left(3\right)\right)\right) \\ &=1\cdot \left(\left(\frac{125}{3}\right)-\left(9\right)\right)\cdot \left(\left(\ln{\left(5 \right)}\right)-\left(\ln{\left(3 \right)}\right)\right) \\ &=1\cdot \left(\frac{98}{3}\right)\cdot \left(\ln{\left(\frac{5}{3} \right)}\right) \\ &=\frac{98 \ln{\left(\frac{5}{3} \right)}}{3}.\end{aligned}
$$



---

Use a change of variables to evaluate the double integral 

$$
\iint_D 2 x \sin{\left(\pi \left(2 x + y\right) \right)}\,\mathrm{d}x\,\mathrm{d}y,
$$

where $D$ is the quadrilateral region with vertices $(3,-6)$, $(6,-12)$, $(6,-11)$ and $(3,-5)$.

1. $\frac{12}{\pi}$
2. $- \frac{54}{\pi}$
3. $54 \pi$
4. $54$
5. $\frac{54}{\pi}$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\text{ }dxdy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))\,|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

To compute the required integral, we proceed as follows:

**Step 1**: Find a suitable change of variables.

The integrand

$$
f(x,y)=2 x \sin{\left(\pi \left(2 x + y\right) \right)}
$$

suggests that we use the change of variables 

$$
u=x,\qquad v=2 x + y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y)\mapsto (u(x,y),v(x,y)).
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

The vertices of our domain $Δ$ in the $uv$-plane are as follows:

$$
\begin{aligned}T^{-1}(3,-6)&=(\left(1\right)\cdot \left(3\right)+\left(0\right)\cdot \left(-6\right)+\left(0\right),\left(2\right)\cdot \left(3\right)+\left(1\right)\cdot \left(-6\right)+\left(0\right)) \\ &=(3,0) \\ T^{-1}(6,-12)&=(\left(1\right)\cdot \left(6\right)+\left(0\right)\cdot \left(-12\right)+\left(0\right),\left(2\right)\cdot \left(6\right)+\left(1\right)\cdot \left(-12\right)+\left(0\right)) \\ &=(6,0) \\ T^{-1}(6,-11)&=(\left(1\right)\cdot \left(6\right)+\left(0\right)\cdot \left(-11\right)+\left(0\right),\left(2\right)\cdot \left(6\right)+\left(1\right)\cdot \left(-11\right)+\left(0\right)) \\ &=(6,1) \\ T^{-1}(3,-5)&=(\left(1\right)\cdot \left(3\right)+\left(0\right)\cdot \left(-5\right)+\left(0\right),\left(2\right)\cdot \left(3\right)+\left(1\right)\cdot \left(-5\right)+\left(0\right)) \\ &=(3,1)\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v):3\le u\le 6,\ 0\le v\le 1\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186198374/plots/2e9ba8e0a46265dc3d0e.png)

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)}&=\begin{vmatrix}\partial u/\partial x&\partial u/\partial y\\\partial v/\partial x&\partial v/\partial y\end{vmatrix} \\ &=\begin{vmatrix}1&0\\2&1\end{vmatrix} \\ &=1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=1
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving these affine equations also gives

$$
x=u,\qquad y=- 2 u + v.
$$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D 2 x \sin{\left(\pi \left(2 x + y\right) \right)}\,\mathrm{d}x\,\mathrm{d}y&=\iint_\Delta 2 u \sin{\left(\pi v \right)}\,\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=\iint_\Delta 2 u \sin{\left(\pi v \right)}\,\left|1\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=2\cdot \int_{0}^{1}\int_{3}^{6}u \sin{\left(\pi v \right)}\,\mathrm{d}u\,\mathrm{d}v \\ &=2\cdot \int_{0}^{1}\sin{\left(\pi v \right)}\,\mathrm{d}v\cdot \int_{3}^{6}u\,\mathrm{d}u \\ &=2\cdot \left[- \frac{\cos{\left(\pi v \right)}}{\pi}\right]_{0}^{1}\cdot \left[\frac{u^{2}}{2}\right]_{3}^{6} \\ &=2\cdot \left(-\cos\left(\pi\cdot \left(1\right)\right)/\pi-\left(-\cos\left(\pi\cdot \left(0\right)\right)/\pi\right)\right)\cdot \left(\left(6\right)^{2}/2-\left(\left(3\right)^{2}/2\right)\right) \\ &=2\cdot \left(\left(\frac{1}{\pi}\right)-\left(- \frac{1}{\pi}\right)\right)\cdot \left(\left(18\right)-\left(\frac{9}{2}\right)\right) \\ &=2\cdot \left(\frac{2}{\pi}\right)\cdot \left(\frac{27}{2}\right) \\ &=\frac{54}{\pi}.\end{aligned}
$$



---

Use a change of variables to evaluate the double integral 

$$
\iint_D 2 \left(x + y\right) e^{x + 3 y}\,\mathrm{d}x\,\mathrm{d}y,
$$

where $D$ is the quadrilateral region with vertices $(4,-1)$, $(7,-2)$, $(\frac{13}{2},- \frac{3}{2})$ and $(\frac{7}{2},- \frac{1}{2})$.

1. $8 e \left(1 + e\right)$
2. $8 e \left(-1 + e\right)$
3. $8 e \left(1 - e\right)$
4. $2 e \left(-1 + e\right)$
5. $16 e \left(-1 + e\right)$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\text{ }dxdy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))\,|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

To compute the required integral, we proceed as follows:

**Step 1**: Find a suitable change of variables.

The integrand

$$
f(x,y)=2 \left(x + y\right) e^{x + 3 y}
$$

suggests that we use the change of variables 

$$
u=x + y,\qquad v=x + 3 y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y)\mapsto (u(x,y),v(x,y)).
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

The vertices of our domain $Δ$ in the $uv$-plane are as follows:

$$
\begin{aligned}T^{-1}(4,-1)&=(\left(1\right)\cdot \left(4\right)+\left(1\right)\cdot \left(-1\right)+\left(0\right),\left(1\right)\cdot \left(4\right)+\left(3\right)\cdot \left(-1\right)+\left(0\right)) \\ &=(3,1) \\ T^{-1}(7,-2)&=(\left(1\right)\cdot \left(7\right)+\left(1\right)\cdot \left(-2\right)+\left(0\right),\left(1\right)\cdot \left(7\right)+\left(3\right)\cdot \left(-2\right)+\left(0\right)) \\ &=(5,1) \\ T^{-1}(\frac{13}{2},- \frac{3}{2})&=(\left(1\right)\cdot \left(\frac{13}{2}\right)+\left(1\right)\cdot \left(- \frac{3}{2}\right)+\left(0\right),\left(1\right)\cdot \left(\frac{13}{2}\right)+\left(3\right)\cdot \left(- \frac{3}{2}\right)+\left(0\right)) \\ &=(5,2) \\ T^{-1}(\frac{7}{2},- \frac{1}{2})&=(\left(1\right)\cdot \left(\frac{7}{2}\right)+\left(1\right)\cdot \left(- \frac{1}{2}\right)+\left(0\right),\left(1\right)\cdot \left(\frac{7}{2}\right)+\left(3\right)\cdot \left(- \frac{1}{2}\right)+\left(0\right)) \\ &=(3,2)\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v):3\le u\le 5,\ 1\le v\le 2\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186198374/plots/e40f3449ba35cf4e271c.png)

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)}&=\begin{vmatrix}\partial u/\partial x&\partial u/\partial y\\\partial v/\partial x&\partial v/\partial y\end{vmatrix} \\ &=\begin{vmatrix}1&1\\1&3\end{vmatrix} \\ &=2.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=\frac{1}{2}
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving these affine equations also gives

$$
x=\frac{3 u}{2} - \frac{v}{2},\qquad y=- \frac{u}{2} + \frac{v}{2}.
$$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D 2 \left(x + y\right) e^{x + 3 y}\,\mathrm{d}x\,\mathrm{d}y&=\iint_\Delta 2 u e^{v}\,\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=\iint_\Delta 2 u e^{v}\,\left|\frac{1}{2}\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=1\cdot \int_{1}^{2}\int_{3}^{5}u e^{v}\,\mathrm{d}u\,\mathrm{d}v \\ &=1\cdot \int_{1}^{2}e^{v}\,\mathrm{d}v\cdot \int_{3}^{5}u\,\mathrm{d}u \\ &=1\cdot \left[e^{v}\right]_{1}^{2}\cdot \left[\frac{u^{2}}{2}\right]_{3}^{5} \\ &=1\cdot \left(e^{2}-\left(e^{1}\right)\right)\cdot \left(\left(5\right)^{2}/2-\left(\left(3\right)^{2}/2\right)\right) \\ &=1\cdot \left(\left(e^{2}\right)-\left(e\right)\right)\cdot \left(\left(\frac{25}{2}\right)-\left(\frac{9}{2}\right)\right) \\ &=1\cdot \left(- e + e^{2}\right)\cdot \left(8\right) \\ &=8 e \left(-1 + e\right).\end{aligned}
$$



---

Use a change of variables to evaluate the double integral 

$$
\iint_D 2 \left(2 x - y\right) e^{\left(2 x - y\right)^{2}}\,\mathrm{d}x\,\mathrm{d}y,
$$

where $D$ is the quadrilateral region with vertices $(3,4)$, $(5,8)$, $(5,7)$ and $(3,3)$.

1. $2 \left(1 + e^{5}\right) e^{4}$
2. $- 2 \left(1 - e^{5}\right) e^{4}$
3. $2 \left(1 - e^{5}\right) e^{4}$
4. $- 4 \left(1 - e\right) e^{2}$
5. $- 4 \left(1 - e^{5}\right) e^{4}$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\text{ }dxdy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))\,|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

To compute the required integral, we proceed as follows:

**Step 1**: Find a suitable change of variables.

The integrand

$$
f(x,y)=2 \left(2 x - y\right) e^{\left(2 x - y\right)^{2}}
$$

suggests that we use the change of variables 

$$
u=x,\qquad v=2 x - y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y)\mapsto (u(x,y),v(x,y)).
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

The vertices of our domain $Δ$ in the $uv$-plane are as follows:

$$
\begin{aligned}T^{-1}(3,4)&=(\left(1\right)\cdot \left(3\right)+\left(0\right)\cdot \left(4\right)+\left(0\right),\left(2\right)\cdot \left(3\right)+\left(-1\right)\cdot \left(4\right)+\left(0\right)) \\ &=(3,2) \\ T^{-1}(5,8)&=(\left(1\right)\cdot \left(5\right)+\left(0\right)\cdot \left(8\right)+\left(0\right),\left(2\right)\cdot \left(5\right)+\left(-1\right)\cdot \left(8\right)+\left(0\right)) \\ &=(5,2) \\ T^{-1}(5,7)&=(\left(1\right)\cdot \left(5\right)+\left(0\right)\cdot \left(7\right)+\left(0\right),\left(2\right)\cdot \left(5\right)+\left(-1\right)\cdot \left(7\right)+\left(0\right)) \\ &=(5,3) \\ T^{-1}(3,3)&=(\left(1\right)\cdot \left(3\right)+\left(0\right)\cdot \left(3\right)+\left(0\right),\left(2\right)\cdot \left(3\right)+\left(-1\right)\cdot \left(3\right)+\left(0\right)) \\ &=(3,3)\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v):3\le u\le 5,\ 2\le v\le 3\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186198374/plots/f0d458601a066470923d.png)

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)}&=\begin{vmatrix}\partial u/\partial x&\partial u/\partial y\\\partial v/\partial x&\partial v/\partial y\end{vmatrix} \\ &=\begin{vmatrix}1&0\\2&-1\end{vmatrix} \\ &=-1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=-1
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving these affine equations also gives

$$
x=u,\qquad y=2 u - v.
$$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D 2 \left(2 x - y\right) e^{\left(2 x - y\right)^{2}}\,\mathrm{d}x\,\mathrm{d}y&=\iint_\Delta 2 v e^{v^{2}}\,\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=\iint_\Delta 2 v e^{v^{2}}\,\left|-1\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=2\cdot \int_{2}^{3}\int_{3}^{5}v e^{v^{2}}\,\mathrm{d}u\,\mathrm{d}v \\ &=2\cdot \int_{2}^{3}v e^{v^{2}}\,\mathrm{d}v\cdot \int_{3}^{5}1\,\mathrm{d}u \\ &=2\cdot \left[\frac{e^{v^{2}}}{2}\right]_{2}^{3}\cdot \left[u\right]_{3}^{5} \\ &=2\cdot \left(e^{\left(3\right)^{2}}/2-\left(e^{\left(2\right)^{2}}/2\right)\right)\cdot \left(\left(5\right)-\left(\left(3\right)\right)\right) \\ &=2\cdot \left(\left(\frac{e^{9}}{2}\right)-\left(\frac{e^{4}}{2}\right)\right)\cdot \left(\left(5\right)-\left(3\right)\right) \\ &=2\cdot \left(- \frac{\left(1 - e^{5}\right) e^{4}}{2}\right)\cdot \left(2\right) \\ &=- 2 \left(1 - e^{5}\right) e^{4}.\end{aligned}
$$



---

Use a change of variables to evaluate the double integral 

$$
\iint_D \left(2 x^{2} - 2 y^{2}\right) \cos{\left(\left(x + y\right)^{2} \right)}\,\mathrm{d}x\,\mathrm{d}y,
$$

where $D$ is the quadrilateral region with vertices $(\frac{3}{2},- \frac{3}{2})$, $(\frac{5}{2},- \frac{5}{2})$, $(\frac{\pi}{6} + \frac{5}{2},- \frac{5}{2} + \frac{\pi}{6})$ and $(\frac{\pi}{6} + \frac{3}{2},- \frac{3}{2} + \frac{\pi}{6})$.

1. $\sin{\left(\frac{\pi^{2}}{9} \right)}$
2. $8 \sin{\left(\frac{\pi^{2}}{9} \right)}$
3. $- 4 \sin{\left(\frac{\pi^{2}}{9} \right)}$
4. $4 \sin{\left(\frac{\pi^{2}}{9} \right)}$
5. $4 \sqrt{3}$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\text{ }dxdy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))\,|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

To compute the required integral, we proceed as follows:

**Step 1**: Find a suitable change of variables.

The integrand

$$
f(x,y)=\left(2 x^{2} - 2 y^{2}\right) \cos{\left(\left(x + y\right)^{2} \right)}=2(x-y)(x+y)\cos((x+y)^2)
$$

suggests that we use the change of variables 

$$
u=x - y,\qquad v=x + y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y)\mapsto (u(x,y),v(x,y)).
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

The vertices of our domain $Δ$ in the $uv$-plane are as follows:

$$
\begin{aligned}T^{-1}(\frac{3}{2},- \frac{3}{2})&=(\left(1\right)\cdot \left(\frac{3}{2}\right)+\left(-1\right)\cdot \left(- \frac{3}{2}\right)+\left(0\right),\left(1\right)\cdot \left(\frac{3}{2}\right)+\left(1\right)\cdot \left(- \frac{3}{2}\right)+\left(0\right)) \\ &=(3,0) \\ T^{-1}(\frac{5}{2},- \frac{5}{2})&=(\left(1\right)\cdot \left(\frac{5}{2}\right)+\left(-1\right)\cdot \left(- \frac{5}{2}\right)+\left(0\right),\left(1\right)\cdot \left(\frac{5}{2}\right)+\left(1\right)\cdot \left(- \frac{5}{2}\right)+\left(0\right)) \\ &=(5,0) \\ T^{-1}(\frac{\pi}{6} + \frac{5}{2},- \frac{5}{2} + \frac{\pi}{6})&=(\left(1\right)\cdot \left(\frac{\pi}{6} + \frac{5}{2}\right)+\left(-1\right)\cdot \left(- \frac{5}{2} + \frac{\pi}{6}\right)+\left(0\right),\left(1\right)\cdot \left(\frac{\pi}{6} + \frac{5}{2}\right)+\left(1\right)\cdot \left(- \frac{5}{2} + \frac{\pi}{6}\right)+\left(0\right)) \\ &=(5,\frac{\pi}{3}) \\ T^{-1}(\frac{\pi}{6} + \frac{3}{2},- \frac{3}{2} + \frac{\pi}{6})&=(\left(1\right)\cdot \left(\frac{\pi}{6} + \frac{3}{2}\right)+\left(-1\right)\cdot \left(- \frac{3}{2} + \frac{\pi}{6}\right)+\left(0\right),\left(1\right)\cdot \left(\frac{\pi}{6} + \frac{3}{2}\right)+\left(1\right)\cdot \left(- \frac{3}{2} + \frac{\pi}{6}\right)+\left(0\right)) \\ &=(3,\frac{\pi}{3})\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v):3\le u\le 5,\ 0\le v\le \frac{\pi}{3}\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186198374/plots/1185115172da1769e0b4.png)

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)}&=\begin{vmatrix}\partial u/\partial x&\partial u/\partial y\\\partial v/\partial x&\partial v/\partial y\end{vmatrix} \\ &=\begin{vmatrix}1&-1\\1&1\end{vmatrix} \\ &=2.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=\frac{1}{2}
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving these affine equations also gives

$$
x=\frac{u}{2} + \frac{v}{2},\qquad y=- \frac{u}{2} + \frac{v}{2}.
$$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D \left(2 x^{2} - 2 y^{2}\right) \cos{\left(\left(x + y\right)^{2} \right)}\,\mathrm{d}x\,\mathrm{d}y&=\iint_D 2(x-y)(x+y)\cos((x+y)^2)\,\mathrm{d}x\,\mathrm{d}y \\ &=\iint_\Delta 2 u v \cos{\left(v^{2} \right)}\,\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=\iint_\Delta 2 u v \cos{\left(v^{2} \right)}\,\left|\frac{1}{2}\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=1\cdot \int_{0}^{\frac{\pi}{3}}\int_{3}^{5}u v \cos{\left(v^{2} \right)}\,\mathrm{d}u\,\mathrm{d}v \\ &=1\cdot \int_{0}^{\frac{\pi}{3}}v \cos{\left(v^{2} \right)}\,\mathrm{d}v\cdot \int_{3}^{5}u\,\mathrm{d}u \\ &=1\cdot \left[\frac{\sin{\left(v^{2} \right)}}{2}\right]_{0}^{\frac{\pi}{3}}\cdot \left[\frac{u^{2}}{2}\right]_{3}^{5} \\ &=1\cdot \left(\sin\left(\left(\frac{\pi}{3}\right)^{2}\right)/2-\left(\sin\left(\left(0\right)^{2}\right)/2\right)\right)\cdot \left(\left(5\right)^{2}/2-\left(\left(3\right)^{2}/2\right)\right) \\ &=1\cdot \left(\left(\frac{\sin{\left(\frac{\pi^{2}}{9} \right)}}{2}\right)-\left(0\right)\right)\cdot \left(\left(\frac{25}{2}\right)-\left(\frac{9}{2}\right)\right) \\ &=1\cdot \left(\frac{\sin{\left(\frac{\pi^{2}}{9} \right)}}{2}\right)\cdot \left(8\right) \\ &=4 \sin{\left(\frac{\pi^{2}}{9} \right)}.\end{aligned}
$$

