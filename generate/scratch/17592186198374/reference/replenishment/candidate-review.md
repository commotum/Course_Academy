Use a change of variables to evaluate the double integral 

$$
\iint_D y^{2} \left(x + 2 y\right)\,\mathrm{d}x\,\mathrm{d}y,
$$

where $D$ is the quadrilateral region with vertices $(2,1)$, $(4,1)$, $(-2,4)$ and $(-4,4)$.

1. $420$
2. $210$
3. $-210$
4. $630$
5. $42$

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
f(x,y)=y^{2} \left(x + 2 y\right)
$$

suggests that we use the change of variables 

$$
u=x + 2 y,\qquad v=y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y)\mapsto (u(x,y),v(x,y)).
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

The vertices of our domain $Δ$ in the $uv$-plane are as follows:

$$
\begin{aligned}T^{-1}(2,1)&=(\left(1\right)\cdot \left(2\right)+\left(2\right)\cdot \left(1\right)+\left(0\right),\left(0\right)\cdot \left(2\right)+\left(1\right)\cdot \left(1\right)+\left(0\right)) \\ &=(4,1) \\ T^{-1}(4,1)&=(\left(1\right)\cdot \left(4\right)+\left(2\right)\cdot \left(1\right)+\left(0\right),\left(0\right)\cdot \left(4\right)+\left(1\right)\cdot \left(1\right)+\left(0\right)) \\ &=(6,1) \\ T^{-1}(-2,4)&=(\left(1\right)\cdot \left(-2\right)+\left(2\right)\cdot \left(4\right)+\left(0\right),\left(0\right)\cdot \left(-2\right)+\left(1\right)\cdot \left(4\right)+\left(0\right)) \\ &=(6,4) \\ T^{-1}(-4,4)&=(\left(1\right)\cdot \left(-4\right)+\left(2\right)\cdot \left(4\right)+\left(0\right),\left(0\right)\cdot \left(-4\right)+\left(1\right)\cdot \left(4\right)+\left(0\right)) \\ &=(4,4)\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v):4\le u\le 6,\ 1\le v\le 4\}
$$

![](images/64/642ee19399f1c37417b256bffc49b4b1458b83b7ea9d1f758e18cac7f1fa620f.png)

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)}&=\begin{vmatrix}\partial u/\partial x&\partial u/\partial y\\\partial v/\partial x&\partial v/\partial y\end{vmatrix} \\ &=\begin{vmatrix}1&2\\0&1\end{vmatrix} \\ &=1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=1
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving these affine equations also gives

$$
x=u - 2 v,\qquad y=v.
$$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D y^{2} \left(x + 2 y\right)\,\mathrm{d}x\,\mathrm{d}y&=\iint_\Delta u v^{2}\,\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=\iint_\Delta u v^{2}\,\left|1\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=1\cdot \int_{1}^{4}\int_{4}^{6}u v^{2}\,\mathrm{d}u\,\mathrm{d}v \\ &=1\cdot \int_{1}^{4}v^{2}\,\mathrm{d}v\cdot \int_{4}^{6}u\,\mathrm{d}u \\ &=1\cdot \left[\frac{v^{3}}{3}\right]_{1}^{4}\cdot \left[\frac{u^{2}}{2}\right]_{4}^{6} \\ &=1\cdot \left(\left(4\right)^{3}/3-\left(\left(1\right)^{3}/3\right)\right)\cdot \left(\left(6\right)^{2}/2-\left(\left(4\right)^{2}/2\right)\right) \\ &=1\cdot \left(\left(\frac{64}{3}\right)-\left(\frac{1}{3}\right)\right)\cdot \left(\left(18\right)-\left(8\right)\right) \\ &=1\cdot \left(21\right)\cdot \left(10\right) \\ &=210.\end{aligned}
$$



---

Use a change of variables to evaluate the double integral 

$$
\iint_D 3 y^{2} \left(x + 2 y\right)\,\mathrm{d}x\,\mathrm{d}y,
$$

where $D$ is the quadrilateral region with vertices $(4,0)$, $(5,0)$, $(-3,4)$ and $(-4,4)$.

1. $576$
2. $288$
3. $64$
4. $864$
5. $-288$

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
f(x,y)=3 y^{2} \left(x + 2 y\right)
$$

suggests that we use the change of variables 

$$
u=x + 2 y,\qquad v=y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y)\mapsto (u(x,y),v(x,y)).
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

The vertices of our domain $Δ$ in the $uv$-plane are as follows:

$$
\begin{aligned}T^{-1}(4,0)&=(\left(1\right)\cdot \left(4\right)+\left(2\right)\cdot \left(0\right)+\left(0\right),\left(0\right)\cdot \left(4\right)+\left(1\right)\cdot \left(0\right)+\left(0\right)) \\ &=(4,0) \\ T^{-1}(5,0)&=(\left(1\right)\cdot \left(5\right)+\left(2\right)\cdot \left(0\right)+\left(0\right),\left(0\right)\cdot \left(5\right)+\left(1\right)\cdot \left(0\right)+\left(0\right)) \\ &=(5,0) \\ T^{-1}(-3,4)&=(\left(1\right)\cdot \left(-3\right)+\left(2\right)\cdot \left(4\right)+\left(0\right),\left(0\right)\cdot \left(-3\right)+\left(1\right)\cdot \left(4\right)+\left(0\right)) \\ &=(5,4) \\ T^{-1}(-4,4)&=(\left(1\right)\cdot \left(-4\right)+\left(2\right)\cdot \left(4\right)+\left(0\right),\left(0\right)\cdot \left(-4\right)+\left(1\right)\cdot \left(4\right)+\left(0\right)) \\ &=(4,4)\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v):4\le u\le 5,\ 0\le v\le 4\}
$$

![](images/31/31a73ea464a3b414e81849dbcd7b5a8361544eaa22a55b895ceb231ca2c1b42c.png)

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)}&=\begin{vmatrix}\partial u/\partial x&\partial u/\partial y\\\partial v/\partial x&\partial v/\partial y\end{vmatrix} \\ &=\begin{vmatrix}1&2\\0&1\end{vmatrix} \\ &=1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=1
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving these affine equations also gives

$$
x=u - 2 v,\qquad y=v.
$$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D 3 y^{2} \left(x + 2 y\right)\,\mathrm{d}x\,\mathrm{d}y&=\iint_\Delta 3 u v^{2}\,\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=\iint_\Delta 3 u v^{2}\,\left|1\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=3\cdot \int_{0}^{4}\int_{4}^{5}u v^{2}\,\mathrm{d}u\,\mathrm{d}v \\ &=3\cdot \int_{0}^{4}v^{2}\,\mathrm{d}v\cdot \int_{4}^{5}u\,\mathrm{d}u \\ &=3\cdot \left[\frac{v^{3}}{3}\right]_{0}^{4}\cdot \left[\frac{u^{2}}{2}\right]_{4}^{5} \\ &=3\cdot \left(\left(4\right)^{3}/3-\left(\left(0\right)^{3}/3\right)\right)\cdot \left(\left(5\right)^{2}/2-\left(\left(4\right)^{2}/2\right)\right) \\ &=3\cdot \left(\left(\frac{64}{3}\right)-\left(0\right)\right)\cdot \left(\left(\frac{25}{2}\right)-\left(8\right)\right) \\ &=3\cdot \left(\frac{64}{3}\right)\cdot \left(\frac{9}{2}\right) \\ &=288.\end{aligned}
$$



---

Use a change of variables to evaluate the double integral 

$$
\iint_D 3 y^{2} \left(x + 2 y\right)\,\mathrm{d}x\,\mathrm{d}y,
$$

where $D$ is the quadrilateral region with vertices $(2,0)$, $(4,0)$, $(-4,4)$ and $(-6,4)$.

1. $128$
2. $384$
3. $-384$
4. $768$
5. $1152$

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
f(x,y)=3 y^{2} \left(x + 2 y\right)
$$

suggests that we use the change of variables 

$$
u=x + 2 y,\qquad v=y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y)\mapsto (u(x,y),v(x,y)).
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

The vertices of our domain $Δ$ in the $uv$-plane are as follows:

$$
\begin{aligned}T^{-1}(2,0)&=(\left(1\right)\cdot \left(2\right)+\left(2\right)\cdot \left(0\right)+\left(0\right),\left(0\right)\cdot \left(2\right)+\left(1\right)\cdot \left(0\right)+\left(0\right)) \\ &=(2,0) \\ T^{-1}(4,0)&=(\left(1\right)\cdot \left(4\right)+\left(2\right)\cdot \left(0\right)+\left(0\right),\left(0\right)\cdot \left(4\right)+\left(1\right)\cdot \left(0\right)+\left(0\right)) \\ &=(4,0) \\ T^{-1}(-4,4)&=(\left(1\right)\cdot \left(-4\right)+\left(2\right)\cdot \left(4\right)+\left(0\right),\left(0\right)\cdot \left(-4\right)+\left(1\right)\cdot \left(4\right)+\left(0\right)) \\ &=(4,4) \\ T^{-1}(-6,4)&=(\left(1\right)\cdot \left(-6\right)+\left(2\right)\cdot \left(4\right)+\left(0\right),\left(0\right)\cdot \left(-6\right)+\left(1\right)\cdot \left(4\right)+\left(0\right)) \\ &=(2,4)\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v):2\le u\le 4,\ 0\le v\le 4\}
$$

![](images/2f/2f38ba39afcd37730bd37cbaca5b8a37feae8aa84f6f79be32a548aed4048482.png)

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)}&=\begin{vmatrix}\partial u/\partial x&\partial u/\partial y\\\partial v/\partial x&\partial v/\partial y\end{vmatrix} \\ &=\begin{vmatrix}1&2\\0&1\end{vmatrix} \\ &=1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=1
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving these affine equations also gives

$$
x=u - 2 v,\qquad y=v.
$$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D 3 y^{2} \left(x + 2 y\right)\,\mathrm{d}x\,\mathrm{d}y&=\iint_\Delta 3 u v^{2}\,\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=\iint_\Delta 3 u v^{2}\,\left|1\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=3\cdot \int_{0}^{4}\int_{2}^{4}u v^{2}\,\mathrm{d}u\,\mathrm{d}v \\ &=3\cdot \int_{0}^{4}v^{2}\,\mathrm{d}v\cdot \int_{2}^{4}u\,\mathrm{d}u \\ &=3\cdot \left[\frac{v^{3}}{3}\right]_{0}^{4}\cdot \left[\frac{u^{2}}{2}\right]_{2}^{4} \\ &=3\cdot \left(\left(4\right)^{3}/3-\left(\left(0\right)^{3}/3\right)\right)\cdot \left(\left(4\right)^{2}/2-\left(\left(2\right)^{2}/2\right)\right) \\ &=3\cdot \left(\left(\frac{64}{3}\right)-\left(0\right)\right)\cdot \left(\left(8\right)-\left(2\right)\right) \\ &=3\cdot \left(\frac{64}{3}\right)\cdot \left(6\right) \\ &=384.\end{aligned}
$$



---

Use a change of variables to evaluate the double integral 

$$
\iint_D y^{2} \left(3 x + 2 y\right)\,\mathrm{d}x\,\mathrm{d}y,
$$

where $D$ is the quadrilateral region with vertices $(- \frac{1}{3},1)$, $(\frac{2}{3},1)$, $(- \frac{4}{3},4)$ and $(- \frac{7}{3},4)$.

1. $105$
2. $- \frac{105}{2}$
3. $\frac{105}{2}$
4. $21$
5. $\frac{315}{2}$

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
f(x,y)=y^{2} \left(3 x + 2 y\right)
$$

suggests that we use the change of variables 

$$
u=3 x + 2 y,\qquad v=y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y)\mapsto (u(x,y),v(x,y)).
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

The vertices of our domain $Δ$ in the $uv$-plane are as follows:

$$
\begin{aligned}T^{-1}(- \frac{1}{3},1)&=(\left(3\right)\cdot \left(- \frac{1}{3}\right)+\left(2\right)\cdot \left(1\right)+\left(0\right),\left(0\right)\cdot \left(- \frac{1}{3}\right)+\left(1\right)\cdot \left(1\right)+\left(0\right)) \\ &=(1,1) \\ T^{-1}(\frac{2}{3},1)&=(\left(3\right)\cdot \left(\frac{2}{3}\right)+\left(2\right)\cdot \left(1\right)+\left(0\right),\left(0\right)\cdot \left(\frac{2}{3}\right)+\left(1\right)\cdot \left(1\right)+\left(0\right)) \\ &=(4,1) \\ T^{-1}(- \frac{4}{3},4)&=(\left(3\right)\cdot \left(- \frac{4}{3}\right)+\left(2\right)\cdot \left(4\right)+\left(0\right),\left(0\right)\cdot \left(- \frac{4}{3}\right)+\left(1\right)\cdot \left(4\right)+\left(0\right)) \\ &=(4,4) \\ T^{-1}(- \frac{7}{3},4)&=(\left(3\right)\cdot \left(- \frac{7}{3}\right)+\left(2\right)\cdot \left(4\right)+\left(0\right),\left(0\right)\cdot \left(- \frac{7}{3}\right)+\left(1\right)\cdot \left(4\right)+\left(0\right)) \\ &=(1,4)\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v):1\le u\le 4,\ 1\le v\le 4\}
$$

![](images/35/35d966f8a5a8e6e04353e202788230edbe6581fa7820e04fbe86406285c2194d.png)

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)}&=\begin{vmatrix}\partial u/\partial x&\partial u/\partial y\\\partial v/\partial x&\partial v/\partial y\end{vmatrix} \\ &=\begin{vmatrix}3&2\\0&1\end{vmatrix} \\ &=3.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=\frac{1}{3}
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving these affine equations also gives

$$
x=\frac{u}{3} - \frac{2 v}{3},\qquad y=v.
$$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D y^{2} \left(3 x + 2 y\right)\,\mathrm{d}x\,\mathrm{d}y&=\iint_\Delta u v^{2}\,\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=\iint_\Delta u v^{2}\,\left|\frac{1}{3}\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=\frac{1}{3}\cdot \int_{1}^{4}\int_{1}^{4}u v^{2}\,\mathrm{d}u\,\mathrm{d}v \\ &=\frac{1}{3}\cdot \int_{1}^{4}v^{2}\,\mathrm{d}v\cdot \int_{1}^{4}u\,\mathrm{d}u \\ &=\frac{1}{3}\cdot \left[\frac{v^{3}}{3}\right]_{1}^{4}\cdot \left[\frac{u^{2}}{2}\right]_{1}^{4} \\ &=\frac{1}{3}\cdot \left(\left(4\right)^{3}/3-\left(\left(1\right)^{3}/3\right)\right)\cdot \left(\left(4\right)^{2}/2-\left(\left(1\right)^{2}/2\right)\right) \\ &=\frac{1}{3}\cdot \left(\left(\frac{64}{3}\right)-\left(\frac{1}{3}\right)\right)\cdot \left(\left(8\right)-\left(\frac{1}{2}\right)\right) \\ &=\frac{1}{3}\cdot \left(21\right)\cdot \left(\frac{15}{2}\right) \\ &=\frac{105}{2}.\end{aligned}
$$



---

Use a change of variables to evaluate the double integral 

$$
\iint_D y^{2} \left(3 x - 2 y\right)\,\mathrm{d}x\,\mathrm{d}y,
$$

where $D$ is the quadrilateral region with vertices $(\frac{5}{3},1)$, $(\frac{7}{3},1)$, $(\frac{11}{3},3)$ and $(3,3)$.

1. $\frac{208}{9}$
2. $\frac{52}{9}$
3. $\frac{416}{9}$
4. $- \frac{208}{9}$
5. $\frac{208}{3}$

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
f(x,y)=y^{2} \left(3 x - 2 y\right)
$$

suggests that we use the change of variables 

$$
u=3 x - 2 y,\qquad v=y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y)\mapsto (u(x,y),v(x,y)).
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

The vertices of our domain $Δ$ in the $uv$-plane are as follows:

$$
\begin{aligned}T^{-1}(\frac{5}{3},1)&=(\left(3\right)\cdot \left(\frac{5}{3}\right)+\left(-2\right)\cdot \left(1\right)+\left(0\right),\left(0\right)\cdot \left(\frac{5}{3}\right)+\left(1\right)\cdot \left(1\right)+\left(0\right)) \\ &=(3,1) \\ T^{-1}(\frac{7}{3},1)&=(\left(3\right)\cdot \left(\frac{7}{3}\right)+\left(-2\right)\cdot \left(1\right)+\left(0\right),\left(0\right)\cdot \left(\frac{7}{3}\right)+\left(1\right)\cdot \left(1\right)+\left(0\right)) \\ &=(5,1) \\ T^{-1}(\frac{11}{3},3)&=(\left(3\right)\cdot \left(\frac{11}{3}\right)+\left(-2\right)\cdot \left(3\right)+\left(0\right),\left(0\right)\cdot \left(\frac{11}{3}\right)+\left(1\right)\cdot \left(3\right)+\left(0\right)) \\ &=(5,3) \\ T^{-1}(3,3)&=(\left(3\right)\cdot \left(3\right)+\left(-2\right)\cdot \left(3\right)+\left(0\right),\left(0\right)\cdot \left(3\right)+\left(1\right)\cdot \left(3\right)+\left(0\right)) \\ &=(3,3)\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v):3\le u\le 5,\ 1\le v\le 3\}
$$

![](images/f9/f9dc752c5aeff34bc911428090212f09e0b3322041842726bd53dd7185563e7d.png)

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)}&=\begin{vmatrix}\partial u/\partial x&\partial u/\partial y\\\partial v/\partial x&\partial v/\partial y\end{vmatrix} \\ &=\begin{vmatrix}3&-2\\0&1\end{vmatrix} \\ &=3.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=\frac{1}{3}
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving these affine equations also gives

$$
x=\frac{u}{3} + \frac{2 v}{3},\qquad y=v.
$$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D y^{2} \left(3 x - 2 y\right)\,\mathrm{d}x\,\mathrm{d}y&=\iint_\Delta u v^{2}\,\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=\iint_\Delta u v^{2}\,\left|\frac{1}{3}\right|\,\mathrm{d}u\,\mathrm{d}v \\ &=\frac{1}{3}\cdot \int_{1}^{3}\int_{3}^{5}u v^{2}\,\mathrm{d}u\,\mathrm{d}v \\ &=\frac{1}{3}\cdot \int_{1}^{3}v^{2}\,\mathrm{d}v\cdot \int_{3}^{5}u\,\mathrm{d}u \\ &=\frac{1}{3}\cdot \left[\frac{v^{3}}{3}\right]_{1}^{3}\cdot \left[\frac{u^{2}}{2}\right]_{3}^{5} \\ &=\frac{1}{3}\cdot \left(\left(3\right)^{3}/3-\left(\left(1\right)^{3}/3\right)\right)\cdot \left(\left(5\right)^{2}/2-\left(\left(3\right)^{2}/2\right)\right) \\ &=\frac{1}{3}\cdot \left(\left(9\right)-\left(\frac{1}{3}\right)\right)\cdot \left(\left(\frac{25}{2}\right)-\left(\frac{9}{2}\right)\right) \\ &=\frac{1}{3}\cdot \left(\frac{26}{3}\right)\cdot \left(8\right) \\ &=\frac{208}{9}.\end{aligned}
$$

