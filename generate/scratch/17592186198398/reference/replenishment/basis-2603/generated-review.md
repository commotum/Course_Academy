## Generated variant / power / easy

Use the change of variables 

$$
u=3 x - 2 y,\quad v=y + 2 z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(3 x - 2 y\right) \left(y + 2 z\right)\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):0\le 3 x - 2 y\le 1,\quad 0\le y + 2 z\le 3,\quad 0\le z\le 2\}.
$$

- A. $9$
- B. $54$
- C. $\frac{3}{4}$
- D. $3$
- E. $\frac{3}{2}$

Correct: \frac{3}{2}

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To compute the required integral, we can use the change of variables formula

$$
{∭}_{R}f(x,y,z)\text{ }dV={∭}_{Δ}\text{ }f(x(u,v,w),y(u,v,w),z(u,v,w))\,|\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=3 x - 2 y,\quad v=y + 2 z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):0\le u\le 1,\quad 0\le v\le 3,\quad 0\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}3 & -2 & 0 \\ 0 & 1 & 2 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}3 & -2 \\ 0 & 1\end{vmatrix} \\  & =\left(2\right)\left(\left(3\right)\cdot \left(1\right)-\left(-2\right)\cdot \left(0\right)\right) \\  & =6.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=\frac{1}{6}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(3 x - 2 y\right) \left(y + 2 z\right)\right)\,\mathrm{d}V & =\iiint_\Delta \left(u v\right)\cdot \left|\frac{1}{6}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{u v}{6}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{1}\int_{0}^{3}\int_{0}^{4}\left(\frac{u v}{6}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{3}\left(\left[\frac{u v w}{6}\right]_{w=0}^{w=4}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{3}\left(\left(\frac{u v \left(4\right)}{6}\right)-\left(\frac{u v \left(0\right)}{6}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{3}\left(\left(\frac{2 u v}{3}\right)-\left(0\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{3}\left(\frac{2 u v}{3}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\left[\frac{u v^{2}}{3}\right]_{v=0}^{v=3}\right)\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\left(\frac{u \left(3\right)^{2}}{3}\right)-\left(\frac{u \left(0\right)^{2}}{3}\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\left(3 u\right)-\left(0\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{1}\left(3 u\right)\,\mathrm{d}u \\  & =\left[\frac{3 u^{2}}{2}\right]_{u=0}^{u=1} \\  & =\left(\frac{3 \left(1\right)^{2}}{2}\right)-\left(\frac{3 \left(0\right)^{2}}{2}\right) \\  & =\left(\frac{3}{2}\right)-\left(0\right) \\  & =\frac{3}{2}\end{aligned}
$$

---

## Generated variant / power / easy

Use the change of variables 

$$
u=- 3 x + 2 y,\quad v=y - 2 z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(- 3 x + 2 y\right) \left(y - 2 z\right)\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):0\le - 3 x + 2 y\le 1,\quad 0\le y - 2 z\le 1,\quad 0\le z\le 1\}.
$$

- A. $\frac{1}{2}$
- B. $\frac{1}{12}$
- C. $3$
- D. $\frac{1}{24}$
- E. $\frac{1}{6}$

Correct: \frac{1}{12}

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To compute the required integral, we can use the change of variables formula

$$
{∭}_{R}f(x,y,z)\text{ }dV={∭}_{Δ}\text{ }f(x(u,v,w),y(u,v,w),z(u,v,w))\,|\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=- 3 x + 2 y,\quad v=y - 2 z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):0\le u\le 1,\quad 0\le v\le 1,\quad 0\le w\le 2\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}-3 & 2 & 0 \\ 0 & 1 & -2 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}-3 & 2 \\ 0 & 1\end{vmatrix} \\  & =\left(2\right)\left(\left(-3\right)\cdot \left(1\right)-\left(2\right)\cdot \left(0\right)\right) \\  & =-6.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{6}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(- 3 x + 2 y\right) \left(y - 2 z\right)\right)\,\mathrm{d}V & =\iiint_\Delta \left(u v\right)\cdot \left|- \frac{1}{6}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{u v}{6}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{1}\int_{0}^{1}\int_{0}^{2}\left(\frac{u v}{6}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{1}\left(\left[\frac{u v w}{6}\right]_{w=0}^{w=2}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{1}\left(\left(\frac{u v \left(2\right)}{6}\right)-\left(\frac{u v \left(0\right)}{6}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{1}\left(\left(\frac{u v}{3}\right)-\left(0\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{1}\left(\frac{u v}{3}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\left[\frac{u v^{2}}{6}\right]_{v=0}^{v=1}\right)\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\left(\frac{u \left(1\right)^{2}}{6}\right)-\left(\frac{u \left(0\right)^{2}}{6}\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\left(\frac{u}{6}\right)-\left(0\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\frac{u}{6}\right)\,\mathrm{d}u \\  & =\left[\frac{u^{2}}{12}\right]_{u=0}^{u=1} \\  & =\left(\frac{\left(1\right)^{2}}{12}\right)-\left(\frac{\left(0\right)^{2}}{12}\right) \\  & =\left(\frac{1}{12}\right)-\left(0\right) \\  & =\frac{1}{12}\end{aligned}
$$

---

## Generated variant / power / easy

Use the change of variables 

$$
u=2 x + y,\quad v=y + 2 z,\quad w=3 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(2 x + y\right) \left(y + 2 z\right)\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):0\le 2 x + y\le 2,\quad 0\le y + 2 z\le 2,\quad 0\le z\le 2\}.
$$

- A. $4$
- B. $24$
- C. $8$
- D. $\frac{4}{3}$
- E. $144$

Correct: 4

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To compute the required integral, we can use the change of variables formula

$$
{∭}_{R}f(x,y,z)\text{ }dV={∭}_{Δ}\text{ }f(x(u,v,w),y(u,v,w),z(u,v,w))\,|\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=2 x + y,\quad v=y + 2 z,\quad w=3 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):0\le u\le 2,\quad 0\le v\le 2,\quad 0\le w\le 6\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}2 & 1 & 0 \\ 0 & 1 & 2 \\ 0 & 0 & 3\end{vmatrix} \\  & =\left(3\right)(-1)^{3+3}\begin{vmatrix}2 & 1 \\ 0 & 1\end{vmatrix} \\  & =\left(3\right)\left(\left(2\right)\cdot \left(1\right)-\left(1\right)\cdot \left(0\right)\right) \\  & =6.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=\frac{1}{6}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(2 x + y\right) \left(y + 2 z\right)\right)\,\mathrm{d}V & =\iiint_\Delta \left(u v\right)\cdot \left|\frac{1}{6}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{u v}{6}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{2}\int_{0}^{2}\int_{0}^{6}\left(\frac{u v}{6}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{2}\int_{0}^{2}\left(\left[\frac{u v w}{6}\right]_{w=0}^{w=6}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{2}\int_{0}^{2}\left(\left(\frac{u v \left(6\right)}{6}\right)-\left(\frac{u v \left(0\right)}{6}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{2}\int_{0}^{2}\left(\left(u v\right)-\left(0\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{2}\int_{0}^{2}\left(u v\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{2}\left(\left[\frac{u v^{2}}{2}\right]_{v=0}^{v=2}\right)\,\mathrm{d}u \\  & =\int_{0}^{2}\left(\left(\frac{u \left(2\right)^{2}}{2}\right)-\left(\frac{u \left(0\right)^{2}}{2}\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{2}\left(\left(2 u\right)-\left(0\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{2}\left(2 u\right)\,\mathrm{d}u \\  & =\left[u^{2}\right]_{u=0}^{u=2} \\  & =\left(\left(2\right)^{2}\right)-\left(\left(0\right)^{2}\right) \\  & =\left(4\right)-\left(0\right) \\  & =4\end{aligned}
$$

---

## Generated variant / power / easy

Use the change of variables 

$$
u=- 3 x - y,\quad v=y + 2 z,\quad w=3 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(- 3 x - y\right) \left(y + 2 z\right)\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):0\le - 3 x - y\le 3,\quad 0\le y + 2 z\le 1,\quad 0\le z\le 2\}.
$$

- A. $\frac{3}{2}$
- B. $\frac{243}{2}$
- C. $3$
- D. $\frac{1}{2}$
- E. $\frac{27}{2}$

Correct: \frac{3}{2}

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To compute the required integral, we can use the change of variables formula

$$
{∭}_{R}f(x,y,z)\text{ }dV={∭}_{Δ}\text{ }f(x(u,v,w),y(u,v,w),z(u,v,w))\,|\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=- 3 x - y,\quad v=y + 2 z,\quad w=3 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):0\le u\le 3,\quad 0\le v\le 1,\quad 0\le w\le 6\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}-3 & -1 & 0 \\ 0 & 1 & 2 \\ 0 & 0 & 3\end{vmatrix} \\  & =\left(3\right)(-1)^{3+3}\begin{vmatrix}-3 & -1 \\ 0 & 1\end{vmatrix} \\  & =\left(3\right)\left(\left(-3\right)\cdot \left(1\right)-\left(-1\right)\cdot \left(0\right)\right) \\  & =-9.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{9}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(- 3 x - y\right) \left(y + 2 z\right)\right)\,\mathrm{d}V & =\iiint_\Delta \left(u v\right)\cdot \left|- \frac{1}{9}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{u v}{9}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{3}\int_{0}^{1}\int_{0}^{6}\left(\frac{u v}{9}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{1}\left(\left[\frac{u v w}{9}\right]_{w=0}^{w=6}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{1}\left(\left(\frac{u v \left(6\right)}{9}\right)-\left(\frac{u v \left(0\right)}{9}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{1}\left(\left(\frac{2 u v}{3}\right)-\left(0\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{1}\left(\frac{2 u v}{3}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\left[\frac{u v^{2}}{3}\right]_{v=0}^{v=1}\right)\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\left(\frac{u \left(1\right)^{2}}{3}\right)-\left(\frac{u \left(0\right)^{2}}{3}\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\left(\frac{u}{3}\right)-\left(0\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\frac{u}{3}\right)\,\mathrm{d}u \\  & =\left[\frac{u^{2}}{6}\right]_{u=0}^{u=3} \\  & =\left(\frac{\left(3\right)^{2}}{6}\right)-\left(\frac{\left(0\right)^{2}}{6}\right) \\  & =\left(\frac{3}{2}\right)-\left(0\right) \\  & =\frac{3}{2}\end{aligned}
$$

---

## Generated variant / power / easy

Use the change of variables 

$$
u=- 3 x - y,\quad v=y + 2 z,\quad w=3 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(- 3 x - y\right) \left(y + 2 z\right)\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):0\le - 3 x - y\le 3,\quad 0\le y + 2 z\le 1,\quad 0\le z\le 1\}.
$$

- A. $\frac{3}{2}$
- B. $\frac{1}{4}$
- C. $\frac{243}{4}$
- D. $\frac{3}{4}$
- E. $\frac{27}{4}$

Correct: \frac{3}{4}

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To compute the required integral, we can use the change of variables formula

$$
{∭}_{R}f(x,y,z)\text{ }dV={∭}_{Δ}\text{ }f(x(u,v,w),y(u,v,w),z(u,v,w))\,|\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=- 3 x - y,\quad v=y + 2 z,\quad w=3 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):0\le u\le 3,\quad 0\le v\le 1,\quad 0\le w\le 3\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}-3 & -1 & 0 \\ 0 & 1 & 2 \\ 0 & 0 & 3\end{vmatrix} \\  & =\left(3\right)(-1)^{3+3}\begin{vmatrix}-3 & -1 \\ 0 & 1\end{vmatrix} \\  & =\left(3\right)\left(\left(-3\right)\cdot \left(1\right)-\left(-1\right)\cdot \left(0\right)\right) \\  & =-9.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{9}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(- 3 x - y\right) \left(y + 2 z\right)\right)\,\mathrm{d}V & =\iiint_\Delta \left(u v\right)\cdot \left|- \frac{1}{9}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{u v}{9}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{3}\int_{0}^{1}\int_{0}^{3}\left(\frac{u v}{9}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{1}\left(\left[\frac{u v w}{9}\right]_{w=0}^{w=3}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{1}\left(\left(\frac{u v \left(3\right)}{9}\right)-\left(\frac{u v \left(0\right)}{9}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{1}\left(\left(\frac{u v}{3}\right)-\left(0\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{1}\left(\frac{u v}{3}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\left[\frac{u v^{2}}{6}\right]_{v=0}^{v=1}\right)\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\left(\frac{u \left(1\right)^{2}}{6}\right)-\left(\frac{u \left(0\right)^{2}}{6}\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\left(\frac{u}{6}\right)-\left(0\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\frac{u}{6}\right)\,\mathrm{d}u \\  & =\left[\frac{u^{2}}{12}\right]_{u=0}^{u=3} \\  & =\left(\frac{\left(3\right)^{2}}{12}\right)-\left(\frac{\left(0\right)^{2}}{12}\right) \\  & =\left(\frac{3}{4}\right)-\left(0\right) \\  & =\frac{3}{4}\end{aligned}
$$

---

## Generated variant / power / hard

Use the change of variables 

$$
u=3 x + 2 y,\quad v=y + 2 z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(3 x + 2 y\right)^{2} \left(y + 2 z\right)\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):1\le 3 x + 2 y\le 3,\quad 1\le y + 2 z\le 2,\quad 1\le z\le 3\}.
$$

- A. $52$
- B. $312$
- C. $\frac{52}{3}$
- D. $26$
- E. $\frac{26}{3}$

Correct: \frac{26}{3}

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To compute the required integral, we can use the change of variables formula

$$
{∭}_{R}f(x,y,z)\text{ }dV={∭}_{Δ}\text{ }f(x(u,v,w),y(u,v,w),z(u,v,w))\,|\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=3 x + 2 y,\quad v=y + 2 z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):1\le u\le 3,\quad 1\le v\le 2,\quad 2\le w\le 6\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}3 & 2 & 0 \\ 0 & 1 & 2 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}3 & 2 \\ 0 & 1\end{vmatrix} \\  & =\left(2\right)\left(\left(3\right)\cdot \left(1\right)-\left(2\right)\cdot \left(0\right)\right) \\  & =6.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=\frac{1}{6}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(3 x + 2 y\right)^{2} \left(y + 2 z\right)\right)\,\mathrm{d}V & =\iiint_\Delta \left(u^{2} v\right)\cdot \left|\frac{1}{6}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{u^{2} v}{6}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{1}^{3}\int_{1}^{2}\int_{2}^{6}\left(\frac{u^{2} v}{6}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{2}\left(\left[\frac{u^{2} v w}{6}\right]_{w=2}^{w=6}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{2}\left(\left(\frac{u^{2} v \left(6\right)}{6}\right)-\left(\frac{u^{2} v \left(2\right)}{6}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{2}\left(\left(u^{2} v\right)-\left(\frac{u^{2} v}{3}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{2}\left(\frac{2 u^{2} v}{3}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left[\frac{u^{2} v^{2}}{3}\right]_{v=1}^{v=2}\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left(\frac{u^{2} \left(2\right)^{2}}{3}\right)-\left(\frac{u^{2} \left(1\right)^{2}}{3}\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left(\frac{4 u^{2}}{3}\right)-\left(\frac{u^{2}}{3}\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(u^{2}\right)\,\mathrm{d}u \\  & =\left[\frac{u^{3}}{3}\right]_{u=1}^{u=3} \\  & =\left(\frac{\left(3\right)^{3}}{3}\right)-\left(\frac{\left(1\right)^{3}}{3}\right) \\  & =\left(9\right)-\left(\frac{1}{3}\right) \\  & =\frac{26}{3}\end{aligned}
$$

---

## Generated variant / sum / hard

Use the change of variables 

$$
u=x - \frac{y}{4},\quad v=\frac{y}{4},\quad w=\frac{z}{2}
$$

to evaluate the triple integral

$$
\iiint_R \left(x - \frac{y}{4} + \frac{z}{2}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):1\le x - \frac{y}{4}\le 3,\quad 1\le \frac{y}{4}\le 3,\quad 1\le z\le 2\}.
$$

- A. $\frac{11}{2}$
- B. $44$
- C. $\frac{11}{16}$
- D. $32$
- E. $12$

Correct: 44

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To compute the required integral, we can use the change of variables formula

$$
{∭}_{R}f(x,y,z)\text{ }dV={∭}_{Δ}\text{ }f(x(u,v,w),y(u,v,w),z(u,v,w))\,|\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x - \frac{y}{4},\quad v=\frac{y}{4},\quad w=\frac{z}{2}
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):1\le u\le 3,\quad 1\le v\le 3,\quad \frac{1}{2}\le w\le 1\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}1 & - \frac{1}{4} & 0 \\ 0 & \frac{1}{4} & 0 \\ 0 & 0 & \frac{1}{2}\end{vmatrix} \\  & =\left(\frac{1}{2}\right)(-1)^{3+3}\begin{vmatrix}1 & - \frac{1}{4} \\ 0 & \frac{1}{4}\end{vmatrix} \\  & =\left(\frac{1}{2}\right)\left(\left(1\right)\cdot \left(\frac{1}{4}\right)-\left(- \frac{1}{4}\right)\cdot \left(0\right)\right) \\  & =\frac{1}{8}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=8.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(x - \frac{y}{4} + \frac{z}{2}\right)\,\mathrm{d}V & =\iiint_\Delta \left(u + w\right)\cdot \left|8\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(8 u + 8 w\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{1}^{3}\int_{1}^{3}\int_{\frac{1}{2}}^{1}\left(8 u + 8 w\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{3}\left(\left[8 u w + 4 w^{2}\right]_{w=\frac{1}{2}}^{w=1}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{3}\left(\left(4 \left(1\right)^{2}\right)-\left(4 \left(\frac{1}{2}\right)^{2}\right)+\left(8 u \left(1\right)\right)-\left(8 u \left(\frac{1}{2}\right)\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{3}\left(\left(4\right)-\left(1\right)+\left(8 u\right)-\left(4 u\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{3}\left(4 u + 3\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left[v \left(4 u + 3\right)\right]_{v=1}^{v=3}\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left(3 \left(3\right)\right)-\left(3 \left(1\right)\right)+\left(4 u \left(3\right)\right)-\left(4 u \left(1\right)\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left(9\right)-\left(3\right)+\left(12 u\right)-\left(4 u\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(8 u + 6\right)\,\mathrm{d}u \\  & =\left[4 u^{2} + 6 u\right]_{u=1}^{u=3} \\  & =\left(4 \left(3\right)^{2}\right)-\left(4 \left(1\right)^{2}\right)+\left(6 \left(3\right)\right)-\left(6 \left(1\right)\right) \\  & =\left(36\right)-\left(4\right)+\left(18\right)-\left(6\right) \\  & =44\end{aligned}
$$

---

## Generated variant / ucosv / hard

Use the change of variables 

$$
u=x^{2} + 4 y,\quad v=x + 2 z,\quad w=3 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(x^{2} + 4 y\right) \cos{\left(x + 2 z \right)}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):1\le x^{2} + 4 y\le 3,\quad \frac{\pi}{6}\le x + 2 z\le 2 \pi,\quad 1\le z\le 3\}.
$$

- A. $-1$
- B. $-12$
- C. $-2$
- D. $- \sqrt{3} + 2$
- E. $-144$

Correct: -1

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To compute the required integral, we can use the change of variables formula

$$
{∭}_{R}f(x,y,z)\text{ }dV={∭}_{Δ}\text{ }f(x(u,v,w),y(u,v,w),z(u,v,w))\,|\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x^{2} + 4 y,\quad v=x + 2 z,\quad w=3 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):1\le u\le 3,\quad \frac{\pi}{6}\le v\le 2 \pi,\quad 3\le w\le 9\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}2 x & 4 & 0 \\ 1 & 0 & 2 \\ 0 & 0 & 3\end{vmatrix} \\  & =\left(3\right)(-1)^{3+3}\begin{vmatrix}2 x & 4 \\ 1 & 0\end{vmatrix} \\  & =\left(3\right)\left(\left(2 x\right)\cdot \left(0\right)-\left(4\right)\cdot \left(1\right)\right) \\  & =-12.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{12}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(x^{2} + 4 y\right) \cos{\left(x + 2 z \right)}\right)\,\mathrm{d}V & =\iiint_\Delta \left(u \cos{\left(v \right)}\right)\cdot \left|- \frac{1}{12}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{u \cos{\left(v \right)}}{12}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{1}^{3}\int_{\frac{\pi}{6}}^{2 \pi}\int_{3}^{9}\left(\frac{u \cos{\left(v \right)}}{12}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{\frac{\pi}{6}}^{2 \pi}\left(\left[\frac{u w \cos{\left(v \right)}}{12}\right]_{w=3}^{w=9}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{\frac{\pi}{6}}^{2 \pi}\left(\left(\frac{u \left(9\right) \cos{\left(v \right)}}{12}\right)-\left(\frac{u \left(3\right) \cos{\left(v \right)}}{12}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{\frac{\pi}{6}}^{2 \pi}\left(\left(\frac{3 u \cos{\left(v \right)}}{4}\right)-\left(\frac{u \cos{\left(v \right)}}{4}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{\frac{\pi}{6}}^{2 \pi}\left(\frac{u \cos{\left(v \right)}}{2}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left[\frac{u \sin{\left(v \right)}}{2}\right]_{v=\frac{\pi}{6}}^{v=2 \pi}\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left(\frac{u \sin{\left(\left(2 \pi\right) \right)}}{2}\right)-\left(\frac{u \sin{\left(\left(\frac{\pi}{6}\right) \right)}}{2}\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left(0\right)-\left(\frac{u}{4}\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(- \frac{u}{4}\right)\,\mathrm{d}u \\  & =\left[- \frac{u^{2}}{8}\right]_{u=1}^{u=3} \\  & =\left(- \frac{\left(3\right)^{2}}{8}\right)-\left(- \frac{\left(1\right)^{2}}{8}\right) \\  & =\left(- \frac{9}{8}\right)-\left(- \frac{1}{8}\right) \\  & =-1\end{aligned}
$$

---

## Generated variant / vcosu / hard

Use the change of variables 

$$
u=x^{2} + 3 y,\quad v=x + 2 z,\quad w=3 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(x + 2 z\right) \cos{\left(x^{2} + 3 y \right)}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):\frac{\pi}{6}\le x^{2} + 3 y\le \frac{\pi}{2},\quad 1\le x + 2 z\le 4,\quad 1\le z\le 3\}.
$$

- A. $\frac{5}{2}$
- B. $\frac{405}{2}$
- C. $- \frac{5 \sqrt{3}}{2}$
- D. $5$
- E. $\frac{45}{2}$

Correct: \frac{5}{2}

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To compute the required integral, we can use the change of variables formula

$$
{∭}_{R}f(x,y,z)\text{ }dV={∭}_{Δ}\text{ }f(x(u,v,w),y(u,v,w),z(u,v,w))\,|\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x^{2} + 3 y,\quad v=x + 2 z,\quad w=3 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):\frac{\pi}{6}\le u\le \frac{\pi}{2},\quad 1\le v\le 4,\quad 3\le w\le 9\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}2 x & 3 & 0 \\ 1 & 0 & 2 \\ 0 & 0 & 3\end{vmatrix} \\  & =\left(3\right)(-1)^{3+3}\begin{vmatrix}2 x & 3 \\ 1 & 0\end{vmatrix} \\  & =\left(3\right)\left(\left(2 x\right)\cdot \left(0\right)-\left(3\right)\cdot \left(1\right)\right) \\  & =-9.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{9}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(x + 2 z\right) \cos{\left(x^{2} + 3 y \right)}\right)\,\mathrm{d}V & =\iiint_\Delta \left(v \cos{\left(u \right)}\right)\cdot \left|- \frac{1}{9}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{v \cos{\left(u \right)}}{9}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\int_{1}^{4}\int_{3}^{9}\left(\frac{v \cos{\left(u \right)}}{9}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\int_{1}^{4}\left(\left[\frac{v w \cos{\left(u \right)}}{9}\right]_{w=3}^{w=9}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\int_{1}^{4}\left(\left(\frac{v \left(9\right) \cos{\left(u \right)}}{9}\right)-\left(\frac{v \left(3\right) \cos{\left(u \right)}}{9}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\int_{1}^{4}\left(\left(v \cos{\left(u \right)}\right)-\left(\frac{v \cos{\left(u \right)}}{3}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\int_{1}^{4}\left(\frac{2 v \cos{\left(u \right)}}{3}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\left(\left[\frac{v^{2} \cos{\left(u \right)}}{3}\right]_{v=1}^{v=4}\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\left(\left(\frac{\left(4\right)^{2} \cos{\left(u \right)}}{3}\right)-\left(\frac{\left(1\right)^{2} \cos{\left(u \right)}}{3}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\left(\left(\frac{16 \cos{\left(u \right)}}{3}\right)-\left(\frac{\cos{\left(u \right)}}{3}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\left(5 \cos{\left(u \right)}\right)\,\mathrm{d}u \\  & =\left[5 \sin{\left(u \right)}\right]_{u=\frac{\pi}{6}}^{u=\frac{\pi}{2}} \\  & =\left(5 \sin{\left(\left(\frac{\pi}{2}\right) \right)}\right)-\left(5 \sin{\left(\left(\frac{\pi}{6}\right) \right)}\right) \\  & =\left(5\right)-\left(\frac{5}{2}\right) \\  & =\frac{5}{2}\end{aligned}
$$

---

## Generated variant / vcosu / hard

Use the change of variables 

$$
u=x^{2} + 4 y,\quad v=x + 2 z,\quad w=3 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(x + 2 z\right) \cos{\left(x^{2} + 4 y \right)}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):\frac{\pi}{6}\le x^{2} + 4 y\le \frac{\pi}{2},\quad 1\le x + 2 z\le 2,\quad 1\le z\le 3\}.
$$

- A. $- \frac{3 \sqrt{3}}{8}$
- B. $\frac{3}{4}$
- C. $54$
- D. $\frac{3}{8}$
- E. $\frac{9}{2}$

Correct: \frac{3}{8}

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To compute the required integral, we can use the change of variables formula

$$
{∭}_{R}f(x,y,z)\text{ }dV={∭}_{Δ}\text{ }f(x(u,v,w),y(u,v,w),z(u,v,w))\,|\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x^{2} + 4 y,\quad v=x + 2 z,\quad w=3 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):\frac{\pi}{6}\le u\le \frac{\pi}{2},\quad 1\le v\le 2,\quad 3\le w\le 9\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}2 x & 4 & 0 \\ 1 & 0 & 2 \\ 0 & 0 & 3\end{vmatrix} \\  & =\left(3\right)(-1)^{3+3}\begin{vmatrix}2 x & 4 \\ 1 & 0\end{vmatrix} \\  & =\left(3\right)\left(\left(2 x\right)\cdot \left(0\right)-\left(4\right)\cdot \left(1\right)\right) \\  & =-12.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{12}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(x + 2 z\right) \cos{\left(x^{2} + 4 y \right)}\right)\,\mathrm{d}V & =\iiint_\Delta \left(v \cos{\left(u \right)}\right)\cdot \left|- \frac{1}{12}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{v \cos{\left(u \right)}}{12}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\int_{1}^{2}\int_{3}^{9}\left(\frac{v \cos{\left(u \right)}}{12}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\int_{1}^{2}\left(\left[\frac{v w \cos{\left(u \right)}}{12}\right]_{w=3}^{w=9}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\int_{1}^{2}\left(\left(\frac{v \left(9\right) \cos{\left(u \right)}}{12}\right)-\left(\frac{v \left(3\right) \cos{\left(u \right)}}{12}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\int_{1}^{2}\left(\left(\frac{3 v \cos{\left(u \right)}}{4}\right)-\left(\frac{v \cos{\left(u \right)}}{4}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\int_{1}^{2}\left(\frac{v \cos{\left(u \right)}}{2}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\left(\left[\frac{v^{2} \cos{\left(u \right)}}{4}\right]_{v=1}^{v=2}\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\left(\left(\frac{\left(2\right)^{2} \cos{\left(u \right)}}{4}\right)-\left(\frac{\left(1\right)^{2} \cos{\left(u \right)}}{4}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\left(\left(\cos{\left(u \right)}\right)-\left(\frac{\cos{\left(u \right)}}{4}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\left(\frac{3 \cos{\left(u \right)}}{4}\right)\,\mathrm{d}u \\  & =\left[\frac{3 \sin{\left(u \right)}}{4}\right]_{u=\frac{\pi}{6}}^{u=\frac{\pi}{2}} \\  & =\left(\frac{3 \sin{\left(\left(\frac{\pi}{2}\right) \right)}}{4}\right)-\left(\frac{3 \sin{\left(\left(\frac{\pi}{6}\right) \right)}}{4}\right) \\  & =\left(\frac{3}{4}\right)-\left(\frac{3}{8}\right) \\  & =\frac{3}{8}\end{aligned}
$$
