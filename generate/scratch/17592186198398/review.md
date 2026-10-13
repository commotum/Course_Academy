# Triple integral evaluation review



Raw original evidence is ineligible for learning. Generated method banks are authored.



### Original 17592186198623



## power — unrated evidence

Use the change of variables
$u = 3x - 2y, v = y + 2z, w = z$
to evaluate the triple integral
$∭_(R)(3x - 2y)^{2}(y + 2z)dV$,
where the region $R$ is given by
$R = {(x, y, z): 0 \le 3x - 2y \le 3, 0 \le y + 2z \le 2, 0 \le 2z \le 1}$.

- A. $4$
- B. $-2$
- C. $3$
- D. $1$
- E. $2$

Correct: absent in raw source

Worked solution absent in raw source.



### Generated moderate variants — power



## power — moderate

Use the change of variables 

$$
u=3 x + 3 y,\quad v=y + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(3 x + 3 y\right)^{2} \left(y + z\right)\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):0\le 3 x + 3 y\le 3,\quad 0\le y + z\le 2,\quad 0\le z\le 2\}.
$$

- A. $432$
- B. $72$
- C. $12$
- D. $24$
- E. $36$

Correct: 12

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
u=3 x + 3 y,\quad v=y + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):0\le u\le 3,\quad 0\le v\le 2,\quad 0\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}3 & 3 & 0 \\ 0 & 1 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}3 & 3 \\ 0 & 1\end{vmatrix} \\  & =\left(2\right)\left(\left(3\right)\cdot \left(1\right)-\left(3\right)\cdot \left(0\right)\right) \\  & =6.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=\frac{1}{6}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(3 x + 3 y\right)^{2} \left(y + z\right)\right)\,\mathrm{d}V & =\iiint_\Delta \left(u^{2} v\right)\cdot \left|\frac{1}{6}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{u^{2} v}{6}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{3}\int_{0}^{2}\int_{0}^{4}\left(\frac{u^{2} v}{6}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{2}\left(\left[\frac{u^{2} v w}{6}\right]_{w=0}^{w=4}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{2}\left(\left(\frac{u^{2} v \left(4\right)}{6}\right)-\left(\frac{u^{2} v \left(0\right)}{6}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{2}\left(\left(\frac{2 u^{2} v}{3}\right)-\left(0\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{2}\left(\frac{2 u^{2} v}{3}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\left[\frac{u^{2} v^{2}}{3}\right]_{v=0}^{v=2}\right)\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\left(\frac{u^{2} \left(2\right)^{2}}{3}\right)-\left(\frac{u^{2} \left(0\right)^{2}}{3}\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\left(\frac{4 u^{2}}{3}\right)-\left(0\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\frac{4 u^{2}}{3}\right)\,\mathrm{d}u \\  & =\left[\frac{4 u^{3}}{9}\right]_{u=0}^{u=3} \\  & =\left(\frac{4 \left(3\right)^{3}}{9}\right)-\left(\frac{4 \left(0\right)^{3}}{9}\right) \\  & =\left(12\right)-\left(0\right) \\  & =12\end{aligned}
$$

## power — moderate

Use the change of variables 

$$
u=- 2 x + 4 y,\quad v=y + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(- 2 x + 4 y\right)^{2} \left(y + z\right)\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):0\le - 2 x + 4 y\le 1,\quad 0\le y + z\le 2,\quad 0\le z\le 2\}.
$$

- A. $\frac{32}{3}$
- B. $2$
- C. $\frac{4}{3}$
- D. $\frac{2}{3}$
- E. $\frac{8}{3}$

Correct: \frac{2}{3}

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
u=- 2 x + 4 y,\quad v=y + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):0\le u\le 1,\quad 0\le v\le 2,\quad 0\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}-2 & 4 & 0 \\ 0 & 1 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}-2 & 4 \\ 0 & 1\end{vmatrix} \\  & =\left(2\right)\left(\left(-2\right)\cdot \left(1\right)-\left(4\right)\cdot \left(0\right)\right) \\  & =-4.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{4}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(- 2 x + 4 y\right)^{2} \left(y + z\right)\right)\,\mathrm{d}V & =\iiint_\Delta \left(u^{2} v\right)\cdot \left|- \frac{1}{4}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{u^{2} v}{4}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{1}\int_{0}^{2}\int_{0}^{4}\left(\frac{u^{2} v}{4}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{2}\left(\left[\frac{u^{2} v w}{4}\right]_{w=0}^{w=4}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{2}\left(\left(\frac{u^{2} v \left(4\right)}{4}\right)-\left(\frac{u^{2} v \left(0\right)}{4}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{2}\left(\left(u^{2} v\right)-\left(0\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{2}\left(u^{2} v\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\left[\frac{u^{2} v^{2}}{2}\right]_{v=0}^{v=2}\right)\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\left(\frac{u^{2} \left(2\right)^{2}}{2}\right)-\left(\frac{u^{2} \left(0\right)^{2}}{2}\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\left(2 u^{2}\right)-\left(0\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{1}\left(2 u^{2}\right)\,\mathrm{d}u \\  & =\left[\frac{2 u^{3}}{3}\right]_{u=0}^{u=1} \\  & =\left(\frac{2 \left(1\right)^{3}}{3}\right)-\left(\frac{2 \left(0\right)^{3}}{3}\right) \\  & =\left(\frac{2}{3}\right)-\left(0\right) \\  & =\frac{2}{3}\end{aligned}
$$



### Original 17592186198964



## vcosu — unrated evidence

Use the change of variables
$u = x^{2} + y, v = x + z, w = z$
to evaluate the triple integral
$∭_(R)(x + z)\cos (x^{2} + y)dV$,
where the region $R$ is given by
$R = {(x, y, z): \frac{π}{6} \le x^{2} + y \le \frac{π}{2}, 0 \le x + z \le 2,-1 \le z \le 1}$.

- A. $\frac{\ln 2}{4}$
- B. $2\sqrt{3}$
- C. $2$
- D. $\ln 2$
- E. $\sqrt{2}$

Correct: absent in raw source

Worked solution absent in raw source.



### Generated moderate variants — vcosu



## vcosu — moderate

Use the change of variables 

$$
u=x^{2} + 3 y,\quad v=x + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(x + z\right) \cos{\left(x^{2} + 3 y \right)}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):\frac{\pi}{6}\le x^{2} + 3 y\le \pi,\quad 0\le x + z\le 2,\quad 0\le z\le 2\}.
$$

- A. $-24$
- B. $-4$
- C. $- \frac{2}{3}$
- D. $- \frac{4}{3}$
- E. $- \frac{4}{3} - \frac{2 \sqrt{3}}{3}$

Correct: - \frac{2}{3}

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
u=x^{2} + 3 y,\quad v=x + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):\frac{\pi}{6}\le u\le \pi,\quad 0\le v\le 2,\quad 0\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}2 x & 3 & 0 \\ 1 & 0 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}2 x & 3 \\ 1 & 0\end{vmatrix} \\  & =\left(2\right)\left(\left(2 x\right)\cdot \left(0\right)-\left(3\right)\cdot \left(1\right)\right) \\  & =-6.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{6}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(x + z\right) \cos{\left(x^{2} + 3 y \right)}\right)\,\mathrm{d}V & =\iiint_\Delta \left(v \cos{\left(u \right)}\right)\cdot \left|- \frac{1}{6}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{v \cos{\left(u \right)}}{6}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{0}^{2}\int_{0}^{4}\left(\frac{v \cos{\left(u \right)}}{6}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{0}^{2}\left(\left[\frac{v w \cos{\left(u \right)}}{6}\right]_{w=0}^{w=4}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{0}^{2}\left(\left(\frac{v \left(4\right) \cos{\left(u \right)}}{6}\right)-\left(\frac{v \left(0\right) \cos{\left(u \right)}}{6}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{0}^{2}\left(\left(\frac{2 v \cos{\left(u \right)}}{3}\right)-\left(0\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{0}^{2}\left(\frac{2 v \cos{\left(u \right)}}{3}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left[\frac{v^{2} \cos{\left(u \right)}}{3}\right]_{v=0}^{v=2}\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left(\frac{\left(2\right)^{2} \cos{\left(u \right)}}{3}\right)-\left(\frac{\left(0\right)^{2} \cos{\left(u \right)}}{3}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left(\frac{4 \cos{\left(u \right)}}{3}\right)-\left(0\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\frac{4 \cos{\left(u \right)}}{3}\right)\,\mathrm{d}u \\  & =\left[\frac{4 \sin{\left(u \right)}}{3}\right]_{u=\frac{\pi}{6}}^{u=\pi} \\  & =\left(\frac{4 \sin{\left(\left(\pi\right) \right)}}{3}\right)-\left(\frac{4 \sin{\left(\left(\frac{\pi}{6}\right) \right)}}{3}\right) \\  & =\left(0\right)-\left(\frac{2}{3}\right) \\  & =- \frac{2}{3}\end{aligned}
$$

## vcosu — moderate

Use the change of variables 

$$
u=x^{2} + 4 y,\quad v=x + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(x + z\right) \cos{\left(x^{2} + 4 y \right)}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):\frac{\pi}{6}\le x^{2} + 4 y\le \pi,\quad 0\le x + z\le 2,\quad 0\le z\le 2\}.
$$

- A. $-32$
- B. $-1 - \frac{\sqrt{3}}{2}$
- C. $-1$
- D. $- \frac{1}{2}$
- E. $-4$

Correct: - \frac{1}{2}

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
u=x^{2} + 4 y,\quad v=x + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):\frac{\pi}{6}\le u\le \pi,\quad 0\le v\le 2,\quad 0\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}2 x & 4 & 0 \\ 1 & 0 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}2 x & 4 \\ 1 & 0\end{vmatrix} \\  & =\left(2\right)\left(\left(2 x\right)\cdot \left(0\right)-\left(4\right)\cdot \left(1\right)\right) \\  & =-8.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{8}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(x + z\right) \cos{\left(x^{2} + 4 y \right)}\right)\,\mathrm{d}V & =\iiint_\Delta \left(v \cos{\left(u \right)}\right)\cdot \left|- \frac{1}{8}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{v \cos{\left(u \right)}}{8}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{0}^{2}\int_{0}^{4}\left(\frac{v \cos{\left(u \right)}}{8}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{0}^{2}\left(\left[\frac{v w \cos{\left(u \right)}}{8}\right]_{w=0}^{w=4}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{0}^{2}\left(\left(\frac{v \left(4\right) \cos{\left(u \right)}}{8}\right)-\left(\frac{v \left(0\right) \cos{\left(u \right)}}{8}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{0}^{2}\left(\left(\frac{v \cos{\left(u \right)}}{2}\right)-\left(0\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{0}^{2}\left(\frac{v \cos{\left(u \right)}}{2}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left[\frac{v^{2} \cos{\left(u \right)}}{4}\right]_{v=0}^{v=2}\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left(\frac{\left(2\right)^{2} \cos{\left(u \right)}}{4}\right)-\left(\frac{\left(0\right)^{2} \cos{\left(u \right)}}{4}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left(\cos{\left(u \right)}\right)-\left(0\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\cos{\left(u \right)}\right)\,\mathrm{d}u \\  & =\left[\sin{\left(u \right)}\right]_{u=\frac{\pi}{6}}^{u=\pi} \\  & =\left(\sin{\left(\left(\pi\right) \right)}\right)-\left(\sin{\left(\left(\frac{\pi}{6}\right) \right)}\right) \\  & =\left(0\right)-\left(\frac{1}{2}\right) \\  & =- \frac{1}{2}\end{aligned}
$$



### Original 17592186374090



## ucosv — moderate

Use the change of variables 

$$
u={x}^{2}+2y,\,v=x-z,\,w=z
$$

to evaluate the triple integral

$$
{∭}_{R}({x}^{2}+2y)\operatorname{cos}⁡(x-z)\,dV,
$$

 
where the region $R$ is given by

$$
R={(x,y,z)\,:\,0\le {x}^{2}+2y\le 2,\,0\le x-z\le \frac{\pi }{2},\,-1\le z\le 1}.
$$

- A. $\frac{1}{2}$
- B. $3$
- C. $\frac{2}{3}$
- D. $5$
- E. $2$

Correct: 2

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
u={x}^{2}+2y,\,v=x-z,\,w=z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\begin{aligned}Δ & ={(u,v,w)\,:\,0\le u\le 2,\,0\le v\le \frac{\pi }{2},\,-1\le w\le 1}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2x & 2 & 0 \\ 1 & 0 & -1 \\ 0 & 0 & 1\end{aligned}| \\  & =1(-1)^{3+3}|\begin{aligned}2x & 2 \\ 1 & 0\end{aligned}| \\  & =0-2 \\  & =-2.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}=-\frac{1}{2}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}{∭}_{R}({x}^{2}+2y)\operatorname{cos}⁡(x-z)\,dV & ={∭}_{Δ}u\operatorname{cos}⁡v\cdot |-\frac{1}{2}|\,\text{d}u\text{d}v\text{d}w \\  & ={∭}_{Δ}\frac{1}{2}u\operatorname{cos}⁡v\,\text{d}u\text{d}v\text{d}w \\  & =\frac{1}{2}{\int }_{0}^{2}{\int }_{0}^{\pi /2}{\int }_{-1}^{1}u\operatorname{cos}⁡v\,dw\,dv\,du \\  & =\frac{1}{2}{\int }_{0}^{2}u\,du\cdot {\int }_{0}^{\pi /2}\operatorname{cos}⁡v\,dv\cdot {\int }_{-1}^{1}dw \\  & =\frac{1}{2}[\frac{{u}^{2}}{2}]_{u=0}^{u=2}\cdot {[\operatorname{sin}⁡v]}_{v=0}^{v=\pi /2}\cdot [w]_{w=-1}^{w=1} \\  & =\frac{1}{2}(2-0)\cdot (1-0)\cdot (1-(-1) \\  & =2\end{aligned}
$$



### Generated moderate variants — ucosv



## ucosv — moderate

Use the change of variables 

$$
u=x^{2} + 3 y,\quad v=x + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(x^{2} + 3 y\right) \cos{\left(x + z \right)}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):0\le x^{2} + 3 y\le 3,\quad 0\le x + z\le \frac{\pi}{2},\quad -1\le z\le 2\}.
$$

- A. $162$
- B. $27$
- C. $\frac{9}{2}$
- D. $- \frac{9}{2}$
- E. $9$

Correct: \frac{9}{2}

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
u=x^{2} + 3 y,\quad v=x + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):0\le u\le 3,\quad 0\le v\le \frac{\pi}{2},\quad -2\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}2 x & 3 & 0 \\ 1 & 0 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}2 x & 3 \\ 1 & 0\end{vmatrix} \\  & =\left(2\right)\left(\left(2 x\right)\cdot \left(0\right)-\left(3\right)\cdot \left(1\right)\right) \\  & =-6.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{6}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(x^{2} + 3 y\right) \cos{\left(x + z \right)}\right)\,\mathrm{d}V & =\iiint_\Delta \left(u \cos{\left(v \right)}\right)\cdot \left|- \frac{1}{6}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{u \cos{\left(v \right)}}{6}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{3}\int_{0}^{\frac{\pi}{2}}\int_{-2}^{4}\left(\frac{u \cos{\left(v \right)}}{6}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{\frac{\pi}{2}}\left(\left[\frac{u w \cos{\left(v \right)}}{6}\right]_{w=-2}^{w=4}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{\frac{\pi}{2}}\left(\left(\frac{u \left(4\right) \cos{\left(v \right)}}{6}\right)-\left(\frac{u \left(-2\right) \cos{\left(v \right)}}{6}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{\frac{\pi}{2}}\left(\left(\frac{2 u \cos{\left(v \right)}}{3}\right)-\left(- \frac{u \cos{\left(v \right)}}{3}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{\frac{\pi}{2}}\left(u \cos{\left(v \right)}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\left[u \sin{\left(v \right)}\right]_{v=0}^{v=\frac{\pi}{2}}\right)\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\left(u \sin{\left(\left(\frac{\pi}{2}\right) \right)}\right)-\left(u \sin{\left(\left(0\right) \right)}\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\left(u\right)-\left(0\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{3}\left(u\right)\,\mathrm{d}u \\  & =\left[\frac{u^{2}}{2}\right]_{u=0}^{u=3} \\  & =\left(\frac{\left(3\right)^{2}}{2}\right)-\left(\frac{\left(0\right)^{2}}{2}\right) \\  & =\left(\frac{9}{2}\right)-\left(0\right) \\  & =\frac{9}{2}\end{aligned}
$$

## ucosv — moderate

Use the change of variables 

$$
u=x^{2} + 4 y,\quad v=x + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(x^{2} + 4 y\right) \cos{\left(x + z \right)}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):0\le x^{2} + 4 y\le 1,\quad 0\le x + z\le \frac{\pi}{2},\quad -1\le z\le 2\}.
$$

- A. $24$
- B. $\frac{3}{4}$
- C. $- \frac{3}{8}$
- D. $\frac{3}{8}$
- E. $3$

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
u=x^{2} + 4 y,\quad v=x + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):0\le u\le 1,\quad 0\le v\le \frac{\pi}{2},\quad -2\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}2 x & 4 & 0 \\ 1 & 0 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}2 x & 4 \\ 1 & 0\end{vmatrix} \\  & =\left(2\right)\left(\left(2 x\right)\cdot \left(0\right)-\left(4\right)\cdot \left(1\right)\right) \\  & =-8.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{8}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(x^{2} + 4 y\right) \cos{\left(x + z \right)}\right)\,\mathrm{d}V & =\iiint_\Delta \left(u \cos{\left(v \right)}\right)\cdot \left|- \frac{1}{8}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{u \cos{\left(v \right)}}{8}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{1}\int_{0}^{\frac{\pi}{2}}\int_{-2}^{4}\left(\frac{u \cos{\left(v \right)}}{8}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{\frac{\pi}{2}}\left(\left[\frac{u w \cos{\left(v \right)}}{8}\right]_{w=-2}^{w=4}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{\frac{\pi}{2}}\left(\left(\frac{u \left(4\right) \cos{\left(v \right)}}{8}\right)-\left(\frac{u \left(-2\right) \cos{\left(v \right)}}{8}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{\frac{\pi}{2}}\left(\left(\frac{u \cos{\left(v \right)}}{2}\right)-\left(- \frac{u \cos{\left(v \right)}}{4}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{\frac{\pi}{2}}\left(\frac{3 u \cos{\left(v \right)}}{4}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\left[\frac{3 u \sin{\left(v \right)}}{4}\right]_{v=0}^{v=\frac{\pi}{2}}\right)\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\left(\frac{3 u \sin{\left(\left(\frac{\pi}{2}\right) \right)}}{4}\right)-\left(\frac{3 u \sin{\left(\left(0\right) \right)}}{4}\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\left(\frac{3 u}{4}\right)-\left(0\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\frac{3 u}{4}\right)\,\mathrm{d}u \\  & =\left[\frac{3 u^{2}}{8}\right]_{u=0}^{u=1} \\  & =\left(\frac{3 \left(1\right)^{2}}{8}\right)-\left(\frac{3 \left(0\right)^{2}}{8}\right) \\  & =\left(\frac{3}{8}\right)-\left(0\right) \\  & =\frac{3}{8}\end{aligned}
$$



### Original 17592186374097



## sum — moderate

Use the change of variables 

$$
u=\frac{2x-y}{2},\,v=\frac{y}{2},\,w=\frac{z}{3}
$$

to evaluate the triple integral

$$
{∭}_{R}(\frac{2x-y}{2}+\frac{z}{3})\,dV
$$

 
where the region $R$ is given by

$$
R={(x,y,z)\,:\,0\le \frac{2x-y}{2}\le 1,\,0\le \frac{y}{2}\le 2,\,0\le z\le 3}.
$$

- A. $15$
- B. $10$
- C. $12$
- D. $7$
- E. $8$

Correct: 12

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
u=\frac{2x-y}{2},\,v=\frac{y}{2},\,w=\frac{z}{3}
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\begin{aligned}Δ & ={(u,v,w)\,:\,0\le u\le 1,\,0\le v\le 2,\,0\le w\le 1}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & -\frac{1}{2} & 0 \\ 0 & \,\,\,\frac{1}{2} & 0 \\ 0 & 0 & \frac{1}{3}\end{aligned}| \\  & =1\cdot \frac{1}{2}\cdot \frac{1}{3} \\  & =\frac{1}{6}.\end{aligned}
$$

 

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}=6.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}{∭}_{R}(\frac{2x-y}{2}+\frac{z}{3})\,dV & ={∭}_{Δ}(u+w)\cdot |6|\,\text{d}u\text{d}v\text{d}w \\  & ={\int }_{0}^{1}{\int }_{0}^{2}{\int }_{0}^{1}\,(6u+6w)\,dw\,dv\,du \\  & ={\int }_{0}^{1}{\int }_{0}^{2}[6uw+3{w}^{2}]_{w=0}^{w=1}\,dv\,du \\  & ={\int }_{0}^{1}{\int }_{0}^{2}(6u(1-0)+3({1}^{2}-{0}^{2}))\,dv\,du \\  & ={\int }_{0}^{1}{\int }_{0}^{2}(6u+3)\,dv\,du \\  & ={\int }_{0}^{1}(6u+3)[v]_{v=0}^{v=2}\,du \\  & ={\int }_{0}^{1}(6u+3)\cdot 2\,du \\  & ={\int }_{0}^{1}(12u+6)\,du \\  & =[6{u}^{2}+6u]_{u=0}^{u=1} \\  & =6({1}^{2}-{0}^{2})+6(1-0) \\  & =12\end{aligned}
$$



### Generated moderate variants — sum



## sum — moderate

Use the change of variables 

$$
u=x - \frac{y}{3},\quad v=\frac{y}{3},\quad w=\frac{z}{3}
$$

to evaluate the triple integral

$$
\iiint_R \left(x - \frac{y}{3} + \frac{z}{3}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):0\le x - \frac{y}{3}\le 3,\quad 0\le \frac{y}{3}\le 2,\quad 0\le z\le 2\}.
$$

- A. $\frac{22}{27}$
- B. $\frac{22}{3}$
- C. $66$
- D. $54$
- E. $12$

Correct: 66

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
u=x - \frac{y}{3},\quad v=\frac{y}{3},\quad w=\frac{z}{3}
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):0\le u\le 3,\quad 0\le v\le 2,\quad 0\le w\le \frac{2}{3}\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}1 & - \frac{1}{3} & 0 \\ 0 & \frac{1}{3} & 0 \\ 0 & 0 & \frac{1}{3}\end{vmatrix} \\  & =\left(\frac{1}{3}\right)(-1)^{3+3}\begin{vmatrix}1 & - \frac{1}{3} \\ 0 & \frac{1}{3}\end{vmatrix} \\  & =\left(\frac{1}{3}\right)\left(\left(1\right)\cdot \left(\frac{1}{3}\right)-\left(- \frac{1}{3}\right)\cdot \left(0\right)\right) \\  & =\frac{1}{9}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=9.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(x - \frac{y}{3} + \frac{z}{3}\right)\,\mathrm{d}V & =\iiint_\Delta \left(u + w\right)\cdot \left|9\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(9 u + 9 w\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{3}\int_{0}^{2}\int_{0}^{\frac{2}{3}}\left(9 u + 9 w\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{2}\left(\left[9 u w + \frac{9 w^{2}}{2}\right]_{w=0}^{w=\frac{2}{3}}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{2}\left(\left(\frac{9 \left(\frac{2}{3}\right)^{2}}{2}\right)-\left(\frac{9 \left(0\right)^{2}}{2}\right)+\left(9 u \left(\frac{2}{3}\right)\right)-\left(9 u \left(0\right)\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{2}\left(\left(2\right)-\left(0\right)+\left(6 u\right)-\left(0\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{2}\left(6 u + 2\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\left[v \left(6 u + 2\right)\right]_{v=0}^{v=2}\right)\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\left(2 \left(2\right)\right)-\left(2 \left(0\right)\right)+\left(6 u \left(2\right)\right)-\left(6 u \left(0\right)\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\left(4\right)-\left(0\right)+\left(12 u\right)-\left(0\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{3}\left(12 u + 4\right)\,\mathrm{d}u \\  & =\left[6 u^{2} + 4 u\right]_{u=0}^{u=3} \\  & =\left(4 \left(3\right)\right)-\left(4 \left(0\right)\right)+\left(6 \left(3\right)^{2}\right)-\left(6 \left(0\right)^{2}\right) \\  & =\left(12\right)-\left(0\right)+\left(54\right)-\left(0\right) \\  & =66\end{aligned}
$$

## sum — moderate

Use the change of variables 

$$
u=x - \frac{y}{4},\quad v=\frac{y}{4},\quad w=\frac{z}{3}
$$

to evaluate the triple integral

$$
\iiint_R \left(x - \frac{y}{4} + \frac{z}{3}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):0\le x - \frac{y}{4}\le 1,\quad 0\le \frac{y}{4}\le 2,\quad 0\le z\le 2\}.
$$

- A. $\frac{5}{54}$
- B. $\frac{16}{3}$
- C. $8$
- D. $\frac{40}{3}$
- E. $\frac{10}{9}$

Correct: \frac{40}{3}

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
u=x - \frac{y}{4},\quad v=\frac{y}{4},\quad w=\frac{z}{3}
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):0\le u\le 1,\quad 0\le v\le 2,\quad 0\le w\le \frac{2}{3}\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}1 & - \frac{1}{4} & 0 \\ 0 & \frac{1}{4} & 0 \\ 0 & 0 & \frac{1}{3}\end{vmatrix} \\  & =\left(\frac{1}{3}\right)(-1)^{3+3}\begin{vmatrix}1 & - \frac{1}{4} \\ 0 & \frac{1}{4}\end{vmatrix} \\  & =\left(\frac{1}{3}\right)\left(\left(1\right)\cdot \left(\frac{1}{4}\right)-\left(- \frac{1}{4}\right)\cdot \left(0\right)\right) \\  & =\frac{1}{12}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=12.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(x - \frac{y}{4} + \frac{z}{3}\right)\,\mathrm{d}V & =\iiint_\Delta \left(u + w\right)\cdot \left|12\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(12 u + 12 w\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{1}\int_{0}^{2}\int_{0}^{\frac{2}{3}}\left(12 u + 12 w\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{2}\left(\left[12 u w + 6 w^{2}\right]_{w=0}^{w=\frac{2}{3}}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{2}\left(\left(6 \left(\frac{2}{3}\right)^{2}\right)-\left(6 \left(0\right)^{2}\right)+\left(12 u \left(\frac{2}{3}\right)\right)-\left(12 u \left(0\right)\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{2}\left(\left(\frac{8}{3}\right)-\left(0\right)+\left(8 u\right)-\left(0\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{2}\left(8 u + \frac{8}{3}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\left[v \left(8 u + \frac{8}{3}\right)\right]_{v=0}^{v=2}\right)\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\left(\frac{8 \left(2\right)}{3}\right)-\left(\frac{8 \left(0\right)}{3}\right)+\left(8 u \left(2\right)\right)-\left(8 u \left(0\right)\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\left(\frac{16}{3}\right)-\left(0\right)+\left(16 u\right)-\left(0\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{1}\left(16 u + \frac{16}{3}\right)\,\mathrm{d}u \\  & =\left[8 u^{2} + \frac{16 u}{3}\right]_{u=0}^{u=1} \\  & =\left(8 \left(1\right)^{2}\right)-\left(8 \left(0\right)^{2}\right)+\left(\frac{16 \left(1\right)}{3}\right)-\left(\frac{16 \left(0\right)}{3}\right) \\  & =\left(8\right)-\left(0\right)+\left(\frac{16}{3}\right)-\left(0\right) \\  & =\frac{40}{3}\end{aligned}
$$



### Original 17592186374125



## exp — moderate

Use the change of variables 

$$
u=x+{y}^{2},\,v=y+z,\,w=2z
$$

to evaluate the triple integral

$$
{∭}_{R}(y+z){e}^{x+{y}^{2}}\,dV,
$$

 
where the region $R$ is given by

$$
R={(x,y,z)\,:\,0\le x+{y}^{2}\le 3,\,0\le y+z\le 1,\,\,0\le z\le 4}.
$$

- A. $({e}^{3}-1)$
- B. $2{e}^{3}$
- C. $\sqrt{2}({e}^{3}-2)$
- D. $2({e}^{3}-1)$
- E. $4({e}^{3}-2)$

Correct: 2({e}^{3}-1)

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
u=x+{y}^{2},\,v=y+z,\,w=2z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\begin{aligned}Δ & ={(u,v,w)\,:\,0\le u\le 3,\,0\le v\le 1,\,0\le w\le 8}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & 2y & 0 \\ 0 & 1 & 1 \\ 0 & 0 & 2\end{aligned}| \\  & =1\cdot 1\cdot 2 \\  & =2.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}=\frac{1}{2}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}{∭}_{R}(y+z){e}^{x+{y}^{2}}\,dV & ={∭}_{Δ}v{e}^{u}\cdot |\frac{1}{2}|\,\text{d}u\text{d}v\text{d}w \\  & ={∭}_{Δ}\frac{1}{2}v{e}^{u}\,\text{d}u\text{d}v\text{d}w \\  & ={\int }_{0}^{3}{\int }_{0}^{1}{\int }_{0}^{8}\frac{1}{2}v{e}^{u}\,dw\,dv\,du \\  & =\frac{1}{2}{\int }_{0}^{3}{e}^{u}\,du\cdot {\int }_{0}^{1}v\,dv\cdot {\int }_{0}^{8}dw \\  & =\frac{1}{2}[{e}^{u}]_{u=0}^{u=3}\cdot {[\frac{{v}^{2}}{2}]}_{v=0}^{v=1}\cdot [w]_{w=0}^{w=8} \\  & =\frac{1}{2}({e}^{3}-1)\cdot (\frac{1}{2}-0)\cdot (8-0) \\  & =2({e}^{3}-1)\end{aligned}
$$



### Generated moderate variants — exp



## exp — moderate

Use the change of variables 

$$
u=x + y^{2},\quad v=y - z,\quad w=3 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(y - z\right) e^{x + y^{2}}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):0\le x + y^{2}\le 3,\quad 0\le y - z\le 1,\quad 0\le z\le 2\}.
$$

- A. $-9 + 9 e^{3}$
- B. $-3 + 3 e^{3}$
- C. $-1 + e^{3}$
- D. $-2 + 2 e^{3}$
- E. $e^{3}$

Correct: -1 + e^{3}

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
u=x + y^{2},\quad v=y - z,\quad w=3 z
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
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}1 & 2 y & 0 \\ 0 & 1 & -1 \\ 0 & 0 & 3\end{vmatrix} \\  & =\left(3\right)(-1)^{3+3}\begin{vmatrix}1 & 2 y \\ 0 & 1\end{vmatrix} \\  & =\left(3\right)\left(\left(1\right)\cdot \left(1\right)-\left(2 y\right)\cdot \left(0\right)\right) \\  & =3.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=\frac{1}{3}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(y - z\right) e^{x + y^{2}}\right)\,\mathrm{d}V & =\iiint_\Delta \left(v e^{u}\right)\cdot \left|\frac{1}{3}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{v e^{u}}{3}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{3}\int_{0}^{1}\int_{0}^{6}\left(\frac{v e^{u}}{3}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{1}\left(\left[\frac{v w e^{u}}{3}\right]_{w=0}^{w=6}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{1}\left(\left(\frac{v \left(6\right) e^{u}}{3}\right)-\left(\frac{v \left(0\right) e^{u}}{3}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{1}\left(\left(2 v e^{u}\right)-\left(0\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{1}\left(2 v e^{u}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\left[v^{2} e^{u}\right]_{v=0}^{v=1}\right)\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\left(\left(1\right)^{2} e^{u}\right)-\left(\left(0\right)^{2} e^{u}\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\left(e^{u}\right)-\left(0\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{3}\left(e^{u}\right)\,\mathrm{d}u \\  & =\left[e^{u}\right]_{u=0}^{u=3} \\  & =\left(e^{\left(3\right)}\right)-\left(e^{\left(0\right)}\right) \\  & =\left(e^{3}\right)-\left(1\right) \\  & =-1 + e^{3}\end{aligned}
$$

## exp — moderate

Use the change of variables 

$$
u=x + y^{2},\quad v=y - z,\quad w=3 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(y - z\right) e^{x + y^{2}}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):0\le x + y^{2}\le 1,\quad 0\le y - z\le 2,\quad 0\le z\le 1\}.
$$

- A. $-18 + 18 e$
- B. $2 e$
- C. $-4 + 4 e$
- D. $-2 + 2 e$
- E. $-6 + 6 e$

Correct: -2 + 2 e

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
u=x + y^{2},\quad v=y - z,\quad w=3 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):0\le u\le 1,\quad 0\le v\le 2,\quad 0\le w\le 3\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}1 & 2 y & 0 \\ 0 & 1 & -1 \\ 0 & 0 & 3\end{vmatrix} \\  & =\left(3\right)(-1)^{3+3}\begin{vmatrix}1 & 2 y \\ 0 & 1\end{vmatrix} \\  & =\left(3\right)\left(\left(1\right)\cdot \left(1\right)-\left(2 y\right)\cdot \left(0\right)\right) \\  & =3.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=\frac{1}{3}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(y - z\right) e^{x + y^{2}}\right)\,\mathrm{d}V & =\iiint_\Delta \left(v e^{u}\right)\cdot \left|\frac{1}{3}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{v e^{u}}{3}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{1}\int_{0}^{2}\int_{0}^{3}\left(\frac{v e^{u}}{3}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{2}\left(\left[\frac{v w e^{u}}{3}\right]_{w=0}^{w=3}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{2}\left(\left(\frac{v \left(3\right) e^{u}}{3}\right)-\left(\frac{v \left(0\right) e^{u}}{3}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{2}\left(\left(v e^{u}\right)-\left(0\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{2}\left(v e^{u}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\left[\frac{v^{2} e^{u}}{2}\right]_{v=0}^{v=2}\right)\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\left(\frac{\left(2\right)^{2} e^{u}}{2}\right)-\left(\frac{\left(0\right)^{2} e^{u}}{2}\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\left(2 e^{u}\right)-\left(0\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{1}\left(2 e^{u}\right)\,\mathrm{d}u \\  & =\left[2 e^{u}\right]_{u=0}^{u=1} \\  & =\left(2 e^{\left(1\right)}\right)-\left(2 e^{\left(0\right)}\right) \\  & =\left(2 e\right)-\left(2\right) \\  & =-2 + 2 e\end{aligned}
$$



### Original 17592186374132



## zcosu — moderate

Use the change of variables 

$$
u=2x+3y,\,v=-2x+z,\,w=\frac{z}{2}
$$

to evaluate the triple integral

$$
{∭}_{R}{z}^{2}\operatorname{cos}⁡(2x+3y)\,dV,
$$

 
where the region $R$ is given by

$$
R={(x,y,z)\,:\,\frac{\pi }{6}\le 2x+3y\le 2\pi ,\,0\le -2x+z\le 1,\,0\le z\le 6}.
$$

- A. $\frac{1}{6}$
- B. $-\frac{2}{3}$
- C. $9$
- D. $-\frac{1}{9}$
- E. $-6$

Correct: -6

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
u=2x+3y,\,v=-2x+z,\,w=\frac{z}{2}
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\begin{aligned}Δ & ={(u,v,w)\,:\,\frac{\pi }{6}\le u\le 2\pi ,\,0\le v\le 1,\,0\le w\le 3}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}\,2 & 3 & 0 \\ -2 & 0 & 1 \\ 0 & 0 & \frac{1}{2}\end{aligned}| \\  & =\frac{1}{2}(-1)^{3+3}|\begin{aligned}2 & 3 \\ -2 & 0\end{aligned}| \\  & =\frac{1}{2}(0-(-6)) \\  & =3.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}=\frac{1}{3}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}{∭}_{R}{z}^{2}\operatorname{cos}⁡(2x+3y)\,dV & ={∭}_{Δ}4{w}^{2}\operatorname{cos}⁡u\cdot |\frac{1}{3}|\,\text{d}u\text{d}v\text{d}w \\  & ={∭}_{Δ}\frac{4}{3}{w}^{2}\operatorname{cos}⁡u\,\text{d}u\text{d}v\text{d}w \\  & ={\int }_{\pi /6}^{2\pi }{\int }_{0}^{1}{\int }_{0}^{3}\frac{4}{3}{w}^{2}\operatorname{cos}⁡u\,dw\,dv\,du \\  & ={\int }_{\pi /6}^{2\pi }\operatorname{cos}⁡u\,du\cdot {\int }_{0}^{1}\,dv\cdot {\int }_{0}^{3}\frac{4{w}^{2}}{3}dw \\  & =[\operatorname{sin}⁡u]_{u=\pi /6}^{u=2\pi }\cdot {[v]}_{v=0}^{v=1}\cdot [\frac{4{w}^{3}}{9}]_{w=0}^{w=3} \\  & =(0-\frac{1}{2})\cdot (1-0)\cdot (12-0) \\  & =-6\end{aligned}
$$



### Generated moderate variants — zcosu



## zcosu — moderate

Use the change of variables 

$$
u=3 x + 3 y,\quad v=x + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(z^{2} \cos{\left(3 x + 3 y \right)}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):\frac{\pi}{6}\le 3 x + 3 y\le \pi,\quad 0\le x + z\le 2,\quad 0\le z\le 2\}.
$$

- A. $-32$
- B. $- \frac{16}{3}$
- C. $- \frac{8}{9}$
- D. $- \frac{8}{3}$
- E. $- \frac{32}{9}$

Correct: - \frac{8}{9}

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
u=3 x + 3 y,\quad v=x + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):\frac{\pi}{6}\le u\le \pi,\quad 0\le v\le 2,\quad 0\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}3 & 3 & 0 \\ 1 & 0 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}3 & 3 \\ 1 & 0\end{vmatrix} \\  & =\left(2\right)\left(\left(3\right)\cdot \left(0\right)-\left(3\right)\cdot \left(1\right)\right) \\  & =-6.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{6}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(z^{2} \cos{\left(3 x + 3 y \right)}\right)\,\mathrm{d}V & =\iiint_\Delta \left(\frac{w^{2} \cos{\left(u \right)}}{4}\right)\cdot \left|- \frac{1}{6}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{w^{2} \cos{\left(u \right)}}{24}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{0}^{2}\int_{0}^{4}\left(\frac{w^{2} \cos{\left(u \right)}}{24}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{0}^{2}\left(\left[\frac{w^{3} \cos{\left(u \right)}}{72}\right]_{w=0}^{w=4}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{0}^{2}\left(\left(\frac{\left(4\right)^{3} \cos{\left(u \right)}}{72}\right)-\left(\frac{\left(0\right)^{3} \cos{\left(u \right)}}{72}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{0}^{2}\left(\left(\frac{8 \cos{\left(u \right)}}{9}\right)-\left(0\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{0}^{2}\left(\frac{8 \cos{\left(u \right)}}{9}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left[\frac{8 v \cos{\left(u \right)}}{9}\right]_{v=0}^{v=2}\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left(\frac{8 \left(2\right) \cos{\left(u \right)}}{9}\right)-\left(\frac{8 \left(0\right) \cos{\left(u \right)}}{9}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left(\frac{16 \cos{\left(u \right)}}{9}\right)-\left(0\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\frac{16 \cos{\left(u \right)}}{9}\right)\,\mathrm{d}u \\  & =\left[\frac{16 \sin{\left(u \right)}}{9}\right]_{u=\frac{\pi}{6}}^{u=\pi} \\  & =\left(\frac{16 \sin{\left(\left(\pi\right) \right)}}{9}\right)-\left(\frac{16 \sin{\left(\left(\frac{\pi}{6}\right) \right)}}{9}\right) \\  & =\left(0\right)-\left(\frac{8}{9}\right) \\  & =- \frac{8}{9}\end{aligned}
$$

## zcosu — moderate

Use the change of variables 

$$
u=- 2 x + 4 y,\quad v=x + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(z^{2} \cos{\left(2 x - 4 y \right)}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):\frac{\pi}{6}\le - 2 x + 4 y\le \pi,\quad 0\le x + z\le 2,\quad 0\le z\le 2\}.
$$

- A. $- \frac{128}{3}$
- B. $- \frac{8}{3}$
- C. $-2$
- D. $- \frac{2}{3}$
- E. $- \frac{16}{3}$

Correct: - \frac{2}{3}

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
u=- 2 x + 4 y,\quad v=x + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):\frac{\pi}{6}\le u\le \pi,\quad 0\le v\le 2,\quad 0\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}-2 & 4 & 0 \\ 1 & 0 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}-2 & 4 \\ 1 & 0\end{vmatrix} \\  & =\left(2\right)\left(\left(-2\right)\cdot \left(0\right)-\left(4\right)\cdot \left(1\right)\right) \\  & =-8.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{8}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(z^{2} \cos{\left(2 x - 4 y \right)}\right)\,\mathrm{d}V & =\iiint_\Delta \left(\frac{w^{2} \cos{\left(u \right)}}{4}\right)\cdot \left|- \frac{1}{8}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{w^{2} \cos{\left(u \right)}}{32}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{0}^{2}\int_{0}^{4}\left(\frac{w^{2} \cos{\left(u \right)}}{32}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{0}^{2}\left(\left[\frac{w^{3} \cos{\left(u \right)}}{96}\right]_{w=0}^{w=4}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{0}^{2}\left(\left(\frac{\left(4\right)^{3} \cos{\left(u \right)}}{96}\right)-\left(\frac{\left(0\right)^{3} \cos{\left(u \right)}}{96}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{0}^{2}\left(\left(\frac{2 \cos{\left(u \right)}}{3}\right)-\left(0\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{0}^{2}\left(\frac{2 \cos{\left(u \right)}}{3}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left[\frac{2 v \cos{\left(u \right)}}{3}\right]_{v=0}^{v=2}\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left(\frac{2 \left(2\right) \cos{\left(u \right)}}{3}\right)-\left(\frac{2 \left(0\right) \cos{\left(u \right)}}{3}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left(\frac{4 \cos{\left(u \right)}}{3}\right)-\left(0\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\frac{4 \cos{\left(u \right)}}{3}\right)\,\mathrm{d}u \\  & =\left[\frac{4 \sin{\left(u \right)}}{3}\right]_{u=\frac{\pi}{6}}^{u=\pi} \\  & =\left(\frac{4 \sin{\left(\left(\pi\right) \right)}}{3}\right)-\left(\frac{4 \sin{\left(\left(\frac{\pi}{6}\right) \right)}}{3}\right) \\  & =\left(0\right)-\left(\frac{2}{3}\right) \\  & =- \frac{2}{3}\end{aligned}
$$



### Original 17592186374139



## sinsin — moderate

Use the change of variables 

$$
u={x}^{2}+2y,\,v=x-2z,\,w=4z
$$

to evaluate the triple integral

$$
{∭}_{R}\operatorname{sin}⁡(x-2z)\operatorname{sin}⁡({x}^{2}+2y)\,dV,
$$

 
where the region $R$ is given by

$$
R={(x,y,z)\,:\,\frac{\pi }{2}\le {x}^{2}+2y\le \pi ,\,\pi \le x-2z\le 2\pi ,\,0\le z\le 1}.
$$

- A. $-\frac{1}{4}$
- B. $-\frac{1}{2}$
- C. $-8$
- D. $-2$
- E. $-1$

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
u={x}^{2}+2y,\,v=x-2z,\,w=4z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\begin{aligned}Δ & ={(u,v,w)\,:\,\frac{\pi }{2}\le u\le \pi ,\,\pi \le v\le 2\pi ,\,0\le w\le 4}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2x & 2 & 0 \\ 1 & 0 & -2 \\ 0 & 0 & 4\end{aligned}| \\  & =4(-1)^{3+3}|\begin{aligned}2x & 2 \\ 1 & 0\end{aligned}| \\  & =4(0-2) \\  & =-8.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}=-\frac{1}{8}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}{∭}_{R}\operatorname{sin}⁡(x-2z)\operatorname{sin}⁡({x}^{2}+2y)\,dV & ={∭}_{Δ}\operatorname{sin}⁡v\operatorname{sin}⁡u\cdot |-\frac{1}{8}|\,\text{d}u\text{d}v\text{d}w \\  & ={∭}_{Δ}\frac{1}{8}\operatorname{sin}⁡v\operatorname{sin}⁡u\,\text{d}u\text{d}v\text{d}w \\  & =\frac{1}{8}{\int }_{\pi /2}^{\pi }{\int }_{\pi }^{2\pi }{\int }_{0}^{4}\operatorname{sin}⁡v\operatorname{sin}⁡u\,dw\,dv\,du \\  & =\frac{1}{8}{\int }_{\pi /2}^{\pi }\operatorname{sin}⁡u\,du\cdot {\int }_{\pi }^{2\pi }\operatorname{sin}⁡v\,dv\cdot {\int }_{0}^{4}dw \\  & =\frac{1}{8}[-\operatorname{cos}⁡u]_{u=\pi /2}^{u=\pi }\cdot {[-\operatorname{cos}⁡v]}_{v=\pi }^{v=2\pi }\cdot [w]_{w=0}^{w=4} \\  & =\frac{1}{8}(1+0)\cdot (-1+(-1))\cdot (4-0) \\  & =-1\end{aligned}
$$



### Generated moderate variants — sinsin



## sinsin — moderate

Use the change of variables 

$$
u=x^{2} + 3 y,\quad v=x + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\sin{\left(x + z \right)} \sin{\left(x^{2} + 3 y \right)}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):\frac{\pi}{2}\le x^{2} + 3 y\le \pi,\quad \pi\le x + z\le 2 \pi,\quad 0\le z\le 2\}.
$$

- A. $-48$
- B. $-8$
- C. $- \frac{4}{3}$
- D. $\frac{4}{3}$
- E. $- \frac{2}{3}$

Correct: - \frac{4}{3}

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
u=x^{2} + 3 y,\quad v=x + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):\frac{\pi}{2}\le u\le \pi,\quad \pi\le v\le 2 \pi,\quad 0\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}2 x & 3 & 0 \\ 1 & 0 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}2 x & 3 \\ 1 & 0\end{vmatrix} \\  & =\left(2\right)\left(\left(2 x\right)\cdot \left(0\right)-\left(3\right)\cdot \left(1\right)\right) \\  & =-6.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{6}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\sin{\left(x + z \right)} \sin{\left(x^{2} + 3 y \right)}\right)\,\mathrm{d}V & =\iiint_\Delta \left(\sin{\left(u \right)} \sin{\left(v \right)}\right)\cdot \left|- \frac{1}{6}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{\sin{\left(u \right)} \sin{\left(v \right)}}{6}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{\frac{\pi}{2}}^{\pi}\int_{\pi}^{2 \pi}\int_{0}^{4}\left(\frac{\sin{\left(u \right)} \sin{\left(v \right)}}{6}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{2}}^{\pi}\int_{\pi}^{2 \pi}\left(\left[\frac{w \sin{\left(u \right)} \sin{\left(v \right)}}{6}\right]_{w=0}^{w=4}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{2}}^{\pi}\int_{\pi}^{2 \pi}\left(\left(\frac{\left(4\right) \sin{\left(u \right)} \sin{\left(v \right)}}{6}\right)-\left(\frac{\left(0\right) \sin{\left(u \right)} \sin{\left(v \right)}}{6}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{2}}^{\pi}\int_{\pi}^{2 \pi}\left(\left(\frac{2 \sin{\left(u \right)} \sin{\left(v \right)}}{3}\right)-\left(0\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{2}}^{\pi}\int_{\pi}^{2 \pi}\left(\frac{2 \sin{\left(u \right)} \sin{\left(v \right)}}{3}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{2}}^{\pi}\left(\left[- \frac{2 \sin{\left(u \right)} \cos{\left(v \right)}}{3}\right]_{v=\pi}^{v=2 \pi}\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{2}}^{\pi}\left(\left(- \frac{2 \sin{\left(u \right)} \cos{\left(\left(2 \pi\right) \right)}}{3}\right)-\left(- \frac{2 \sin{\left(u \right)} \cos{\left(\left(\pi\right) \right)}}{3}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{2}}^{\pi}\left(\left(- \frac{2 \sin{\left(u \right)}}{3}\right)-\left(\frac{2 \sin{\left(u \right)}}{3}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{2}}^{\pi}\left(- \frac{4 \sin{\left(u \right)}}{3}\right)\,\mathrm{d}u \\  & =\left[\frac{4 \cos{\left(u \right)}}{3}\right]_{u=\frac{\pi}{2}}^{u=\pi} \\  & =\left(\frac{4 \cos{\left(\left(\pi\right) \right)}}{3}\right)-\left(\frac{4 \cos{\left(\left(\frac{\pi}{2}\right) \right)}}{3}\right) \\  & =\left(- \frac{4}{3}\right)-\left(0\right) \\  & =- \frac{4}{3}\end{aligned}
$$

## sinsin — moderate

Use the change of variables 

$$
u=x^{2} + 4 y,\quad v=x + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\sin{\left(x + z \right)} \sin{\left(x^{2} + 4 y \right)}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):\frac{\pi}{2}\le x^{2} + 4 y\le \pi,\quad \pi\le x + z\le 2 \pi,\quad 0\le z\le 2\}.
$$

- A. $-64$
- B. $- \frac{1}{2}$
- C. $1$
- D. $-1$
- E. $-8$

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
u=x^{2} + 4 y,\quad v=x + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):\frac{\pi}{2}\le u\le \pi,\quad \pi\le v\le 2 \pi,\quad 0\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}2 x & 4 & 0 \\ 1 & 0 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}2 x & 4 \\ 1 & 0\end{vmatrix} \\  & =\left(2\right)\left(\left(2 x\right)\cdot \left(0\right)-\left(4\right)\cdot \left(1\right)\right) \\  & =-8.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{8}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\sin{\left(x + z \right)} \sin{\left(x^{2} + 4 y \right)}\right)\,\mathrm{d}V & =\iiint_\Delta \left(\sin{\left(u \right)} \sin{\left(v \right)}\right)\cdot \left|- \frac{1}{8}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{\sin{\left(u \right)} \sin{\left(v \right)}}{8}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{\frac{\pi}{2}}^{\pi}\int_{\pi}^{2 \pi}\int_{0}^{4}\left(\frac{\sin{\left(u \right)} \sin{\left(v \right)}}{8}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{2}}^{\pi}\int_{\pi}^{2 \pi}\left(\left[\frac{w \sin{\left(u \right)} \sin{\left(v \right)}}{8}\right]_{w=0}^{w=4}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{2}}^{\pi}\int_{\pi}^{2 \pi}\left(\left(\frac{\left(4\right) \sin{\left(u \right)} \sin{\left(v \right)}}{8}\right)-\left(\frac{\left(0\right) \sin{\left(u \right)} \sin{\left(v \right)}}{8}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{2}}^{\pi}\int_{\pi}^{2 \pi}\left(\left(\frac{\sin{\left(u \right)} \sin{\left(v \right)}}{2}\right)-\left(0\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{2}}^{\pi}\int_{\pi}^{2 \pi}\left(\frac{\sin{\left(u \right)} \sin{\left(v \right)}}{2}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{2}}^{\pi}\left(\left[- \frac{\sin{\left(u \right)} \cos{\left(v \right)}}{2}\right]_{v=\pi}^{v=2 \pi}\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{2}}^{\pi}\left(\left(- \frac{\sin{\left(u \right)} \cos{\left(\left(2 \pi\right) \right)}}{2}\right)-\left(- \frac{\sin{\left(u \right)} \cos{\left(\left(\pi\right) \right)}}{2}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{2}}^{\pi}\left(\left(- \frac{\sin{\left(u \right)}}{2}\right)-\left(\frac{\sin{\left(u \right)}}{2}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{2}}^{\pi}\left(- \sin{\left(u \right)}\right)\,\mathrm{d}u \\  & =\left[\cos{\left(u \right)}\right]_{u=\frac{\pi}{2}}^{u=\pi} \\  & =\left(\cos{\left(\left(\pi\right) \right)}\right)-\left(\cos{\left(\left(\frac{\pi}{2}\right) \right)}\right) \\  & =\left(-1\right)-\left(0\right) \\  & =-1\end{aligned}
$$



### Authored easy examples



## power — easy

Use the change of variables 

$$
u=2 x + 2 y,\quad v=y + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(2 x + 2 y\right) \left(y + z\right)\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):0\le 2 x + 2 y\le 3,\quad 0\le y + z\le 2,\quad 0\le z\le 2\}.
$$

- A. $144$
- B. $36$
- C. $9$
- D. $\frac{9}{2}$
- E. $18$

Correct: 9

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
u=2 x + 2 y,\quad v=y + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):0\le u\le 3,\quad 0\le v\le 2,\quad 0\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}2 & 2 & 0 \\ 0 & 1 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}2 & 2 \\ 0 & 1\end{vmatrix} \\  & =\left(2\right)\left(\left(2\right)\cdot \left(1\right)-\left(2\right)\cdot \left(0\right)\right) \\  & =4.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=\frac{1}{4}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(2 x + 2 y\right) \left(y + z\right)\right)\,\mathrm{d}V & =\iiint_\Delta \left(u v\right)\cdot \left|\frac{1}{4}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{u v}{4}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{3}\int_{0}^{2}\int_{0}^{4}\left(\frac{u v}{4}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{2}\left(\left[\frac{u v w}{4}\right]_{w=0}^{w=4}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{2}\left(\left(\frac{u v \left(4\right)}{4}\right)-\left(\frac{u v \left(0\right)}{4}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{2}\left(\left(u v\right)-\left(0\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\int_{0}^{2}\left(u v\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\left[\frac{u v^{2}}{2}\right]_{v=0}^{v=2}\right)\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\left(\frac{u \left(2\right)^{2}}{2}\right)-\left(\frac{u \left(0\right)^{2}}{2}\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{3}\left(\left(2 u\right)-\left(0\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{3}\left(2 u\right)\,\mathrm{d}u \\  & =\left[u^{2}\right]_{u=0}^{u=3} \\  & =\left(\left(3\right)^{2}\right)-\left(\left(0\right)^{2}\right) \\  & =\left(9\right)-\left(0\right) \\  & =9\end{aligned}
$$

## power — easy

Use the change of variables 

$$
u=3 x + 2 y,\quad v=y + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(3 x + 2 y\right) \left(y + z\right)\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):0\le 3 x + 2 y\le 1,\quad 0\le y + z\le 2,\quad 0\le z\le 2\}.
$$

- A. $24$
- B. $\frac{4}{3}$
- C. $\frac{1}{3}$
- D. $\frac{2}{3}$
- E. $4$

Correct: \frac{2}{3}

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
u=3 x + 2 y,\quad v=y + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):0\le u\le 1,\quad 0\le v\le 2,\quad 0\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}3 & 2 & 0 \\ 0 & 1 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}3 & 2 \\ 0 & 1\end{vmatrix} \\  & =\left(2\right)\left(\left(3\right)\cdot \left(1\right)-\left(2\right)\cdot \left(0\right)\right) \\  & =6.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=\frac{1}{6}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(3 x + 2 y\right) \left(y + z\right)\right)\,\mathrm{d}V & =\iiint_\Delta \left(u v\right)\cdot \left|\frac{1}{6}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{u v}{6}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{1}\int_{0}^{2}\int_{0}^{4}\left(\frac{u v}{6}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{2}\left(\left[\frac{u v w}{6}\right]_{w=0}^{w=4}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{2}\left(\left(\frac{u v \left(4\right)}{6}\right)-\left(\frac{u v \left(0\right)}{6}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{2}\left(\left(\frac{2 u v}{3}\right)-\left(0\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\int_{0}^{2}\left(\frac{2 u v}{3}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\left[\frac{u v^{2}}{3}\right]_{v=0}^{v=2}\right)\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\left(\frac{u \left(2\right)^{2}}{3}\right)-\left(\frac{u \left(0\right)^{2}}{3}\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\left(\frac{4 u}{3}\right)-\left(0\right)\right)\,\mathrm{d}u \\  & =\int_{0}^{1}\left(\frac{4 u}{3}\right)\,\mathrm{d}u \\  & =\left[\frac{2 u^{2}}{3}\right]_{u=0}^{u=1} \\  & =\left(\frac{2 \left(1\right)^{2}}{3}\right)-\left(\frac{2 \left(0\right)^{2}}{3}\right) \\  & =\left(\frac{2}{3}\right)-\left(0\right) \\  & =\frac{2}{3}\end{aligned}
$$



### Authored hard examples



## power — hard

Use the change of variables 

$$
u=3 x + 3 y,\quad v=y + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(3 x + 3 y\right)^{2} \left(y + z\right)\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):1\le 3 x + 3 y\le 3,\quad 1\le y + z\le 3,\quad 1\le z\le 3\}.
$$

- A. $832$
- B. $\frac{416}{3}$
- C. $\frac{208}{9}$
- D. $\frac{416}{9}$
- E. $\frac{208}{3}$

Correct: \frac{208}{9}

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
u=3 x + 3 y,\quad v=y + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):1\le u\le 3,\quad 1\le v\le 3,\quad 2\le w\le 6\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}3 & 3 & 0 \\ 0 & 1 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}3 & 3 \\ 0 & 1\end{vmatrix} \\  & =\left(2\right)\left(\left(3\right)\cdot \left(1\right)-\left(3\right)\cdot \left(0\right)\right) \\  & =6.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=\frac{1}{6}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(3 x + 3 y\right)^{2} \left(y + z\right)\right)\,\mathrm{d}V & =\iiint_\Delta \left(u^{2} v\right)\cdot \left|\frac{1}{6}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{u^{2} v}{6}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{1}^{3}\int_{1}^{3}\int_{2}^{6}\left(\frac{u^{2} v}{6}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{3}\left(\left[\frac{u^{2} v w}{6}\right]_{w=2}^{w=6}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{3}\left(\left(\frac{u^{2} v \left(6\right)}{6}\right)-\left(\frac{u^{2} v \left(2\right)}{6}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{3}\left(\left(u^{2} v\right)-\left(\frac{u^{2} v}{3}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{3}\left(\frac{2 u^{2} v}{3}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left[\frac{u^{2} v^{2}}{3}\right]_{v=1}^{v=3}\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left(\frac{u^{2} \left(3\right)^{2}}{3}\right)-\left(\frac{u^{2} \left(1\right)^{2}}{3}\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left(3 u^{2}\right)-\left(\frac{u^{2}}{3}\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\frac{8 u^{2}}{3}\right)\,\mathrm{d}u \\  & =\left[\frac{8 u^{3}}{9}\right]_{u=1}^{u=3} \\  & =\left(\frac{8 \left(3\right)^{3}}{9}\right)-\left(\frac{8 \left(1\right)^{3}}{9}\right) \\  & =\left(24\right)-\left(\frac{8}{9}\right) \\  & =\frac{208}{9}\end{aligned}
$$

## power — hard

Use the change of variables 

$$
u=- 2 x + 4 y,\quad v=y + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(- 2 x + 4 y\right)^{2} \left(y + z\right)\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):1\le - 2 x + 4 y\le 3,\quad 1\le y + z\le 4,\quad 1\le z\le 3\}.
$$

- A. $1040$
- B. $195$
- C. $130$
- D. $65$
- E. $260$

Correct: 65

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
u=- 2 x + 4 y,\quad v=y + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):1\le u\le 3,\quad 1\le v\le 4,\quad 2\le w\le 6\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}-2 & 4 & 0 \\ 0 & 1 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}-2 & 4 \\ 0 & 1\end{vmatrix} \\  & =\left(2\right)\left(\left(-2\right)\cdot \left(1\right)-\left(4\right)\cdot \left(0\right)\right) \\  & =-4.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{4}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(- 2 x + 4 y\right)^{2} \left(y + z\right)\right)\,\mathrm{d}V & =\iiint_\Delta \left(u^{2} v\right)\cdot \left|- \frac{1}{4}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{u^{2} v}{4}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{1}^{3}\int_{1}^{4}\int_{2}^{6}\left(\frac{u^{2} v}{4}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{4}\left(\left[\frac{u^{2} v w}{4}\right]_{w=2}^{w=6}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{4}\left(\left(\frac{u^{2} v \left(6\right)}{4}\right)-\left(\frac{u^{2} v \left(2\right)}{4}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{4}\left(\left(\frac{3 u^{2} v}{2}\right)-\left(\frac{u^{2} v}{2}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{4}\left(u^{2} v\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left[\frac{u^{2} v^{2}}{2}\right]_{v=1}^{v=4}\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left(\frac{u^{2} \left(4\right)^{2}}{2}\right)-\left(\frac{u^{2} \left(1\right)^{2}}{2}\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left(8 u^{2}\right)-\left(\frac{u^{2}}{2}\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\frac{15 u^{2}}{2}\right)\,\mathrm{d}u \\  & =\left[\frac{5 u^{3}}{2}\right]_{u=1}^{u=3} \\  & =\left(\frac{5 \left(3\right)^{3}}{2}\right)-\left(\frac{5 \left(1\right)^{3}}{2}\right) \\  & =\left(\frac{135}{2}\right)-\left(\frac{5}{2}\right) \\  & =65\end{aligned}
$$

## vcosu — hard

Use the change of variables 

$$
u=x^{2} + 3 y,\quad v=x + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(x + z\right) \cos{\left(x^{2} + 3 y \right)}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):\frac{\pi}{6}\le x^{2} + 3 y\le \frac{\pi}{2},\quad 1\le x + z\le 3,\quad 1\le z\le 4\}.
$$

- A. $72$
- B. $12$
- C. $2$
- D. $4$
- E. $- 2 \sqrt{3}$

Correct: 2

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
u=x^{2} + 3 y,\quad v=x + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):\frac{\pi}{6}\le u\le \frac{\pi}{2},\quad 1\le v\le 3,\quad 2\le w\le 8\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}2 x & 3 & 0 \\ 1 & 0 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}2 x & 3 \\ 1 & 0\end{vmatrix} \\  & =\left(2\right)\left(\left(2 x\right)\cdot \left(0\right)-\left(3\right)\cdot \left(1\right)\right) \\  & =-6.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{6}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(x + z\right) \cos{\left(x^{2} + 3 y \right)}\right)\,\mathrm{d}V & =\iiint_\Delta \left(v \cos{\left(u \right)}\right)\cdot \left|- \frac{1}{6}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{v \cos{\left(u \right)}}{6}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\int_{1}^{3}\int_{2}^{8}\left(\frac{v \cos{\left(u \right)}}{6}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\int_{1}^{3}\left(\left[\frac{v w \cos{\left(u \right)}}{6}\right]_{w=2}^{w=8}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\int_{1}^{3}\left(\left(\frac{v \left(8\right) \cos{\left(u \right)}}{6}\right)-\left(\frac{v \left(2\right) \cos{\left(u \right)}}{6}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\int_{1}^{3}\left(\left(\frac{4 v \cos{\left(u \right)}}{3}\right)-\left(\frac{v \cos{\left(u \right)}}{3}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\int_{1}^{3}\left(v \cos{\left(u \right)}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\left(\left[\frac{v^{2} \cos{\left(u \right)}}{2}\right]_{v=1}^{v=3}\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\left(\left(\frac{\left(3\right)^{2} \cos{\left(u \right)}}{2}\right)-\left(\frac{\left(1\right)^{2} \cos{\left(u \right)}}{2}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\left(\left(\frac{9 \cos{\left(u \right)}}{2}\right)-\left(\frac{\cos{\left(u \right)}}{2}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\left(4 \cos{\left(u \right)}\right)\,\mathrm{d}u \\  & =\left[4 \sin{\left(u \right)}\right]_{u=\frac{\pi}{6}}^{u=\frac{\pi}{2}} \\  & =\left(4 \sin{\left(\left(\frac{\pi}{2}\right) \right)}\right)-\left(4 \sin{\left(\left(\frac{\pi}{6}\right) \right)}\right) \\  & =\left(4\right)-\left(2\right) \\  & =2\end{aligned}
$$

## vcosu — hard

Use the change of variables 

$$
u=x^{2} + 4 y,\quad v=x + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(x + z\right) \cos{\left(x^{2} + 4 y \right)}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):\frac{\pi}{6}\le x^{2} + 4 y\le \pi,\quad 1\le x + z\le 2,\quad 1\le z\le 2\}.
$$

- A. $-12$
- B. $- \frac{3}{8} - \frac{3 \sqrt{3}}{16}$
- C. $- \frac{3}{8}$
- D. $- \frac{3}{16}$
- E. $- \frac{3}{2}$

Correct: - \frac{3}{16}

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
u=x^{2} + 4 y,\quad v=x + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):\frac{\pi}{6}\le u\le \pi,\quad 1\le v\le 2,\quad 2\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}2 x & 4 & 0 \\ 1 & 0 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}2 x & 4 \\ 1 & 0\end{vmatrix} \\  & =\left(2\right)\left(\left(2 x\right)\cdot \left(0\right)-\left(4\right)\cdot \left(1\right)\right) \\  & =-8.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{8}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(x + z\right) \cos{\left(x^{2} + 4 y \right)}\right)\,\mathrm{d}V & =\iiint_\Delta \left(v \cos{\left(u \right)}\right)\cdot \left|- \frac{1}{8}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{v \cos{\left(u \right)}}{8}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{1}^{2}\int_{2}^{4}\left(\frac{v \cos{\left(u \right)}}{8}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{1}^{2}\left(\left[\frac{v w \cos{\left(u \right)}}{8}\right]_{w=2}^{w=4}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{1}^{2}\left(\left(\frac{v \left(4\right) \cos{\left(u \right)}}{8}\right)-\left(\frac{v \left(2\right) \cos{\left(u \right)}}{8}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{1}^{2}\left(\left(\frac{v \cos{\left(u \right)}}{2}\right)-\left(\frac{v \cos{\left(u \right)}}{4}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{1}^{2}\left(\frac{v \cos{\left(u \right)}}{4}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left[\frac{v^{2} \cos{\left(u \right)}}{8}\right]_{v=1}^{v=2}\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left(\frac{\left(2\right)^{2} \cos{\left(u \right)}}{8}\right)-\left(\frac{\left(1\right)^{2} \cos{\left(u \right)}}{8}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left(\frac{\cos{\left(u \right)}}{2}\right)-\left(\frac{\cos{\left(u \right)}}{8}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\frac{3 \cos{\left(u \right)}}{8}\right)\,\mathrm{d}u \\  & =\left[\frac{3 \sin{\left(u \right)}}{8}\right]_{u=\frac{\pi}{6}}^{u=\pi} \\  & =\left(\frac{3 \sin{\left(\left(\pi\right) \right)}}{8}\right)-\left(\frac{3 \sin{\left(\left(\frac{\pi}{6}\right) \right)}}{8}\right) \\  & =\left(0\right)-\left(\frac{3}{16}\right) \\  & =- \frac{3}{16}\end{aligned}
$$

## ucosv — hard

Use the change of variables 

$$
u=x^{2} + 3 y,\quad v=x + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(x^{2} + 3 y\right) \cos{\left(x + z \right)}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):1\le x^{2} + 3 y\le 3,\quad \frac{\pi}{6}\le x + z\le 2 \pi,\quad 1\le z\le 3\}.
$$

- A. $-48$
- B. $-8$
- C. $- \frac{4}{3}$
- D. $- \frac{4 \sqrt{3}}{3} + \frac{8}{3}$
- E. $- \frac{8}{3}$

Correct: - \frac{4}{3}

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
u=x^{2} + 3 y,\quad v=x + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):1\le u\le 3,\quad \frac{\pi}{6}\le v\le 2 \pi,\quad 2\le w\le 6\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}2 x & 3 & 0 \\ 1 & 0 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}2 x & 3 \\ 1 & 0\end{vmatrix} \\  & =\left(2\right)\left(\left(2 x\right)\cdot \left(0\right)-\left(3\right)\cdot \left(1\right)\right) \\  & =-6.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{6}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(x^{2} + 3 y\right) \cos{\left(x + z \right)}\right)\,\mathrm{d}V & =\iiint_\Delta \left(u \cos{\left(v \right)}\right)\cdot \left|- \frac{1}{6}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{u \cos{\left(v \right)}}{6}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{1}^{3}\int_{\frac{\pi}{6}}^{2 \pi}\int_{2}^{6}\left(\frac{u \cos{\left(v \right)}}{6}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{\frac{\pi}{6}}^{2 \pi}\left(\left[\frac{u w \cos{\left(v \right)}}{6}\right]_{w=2}^{w=6}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{\frac{\pi}{6}}^{2 \pi}\left(\left(\frac{u \left(6\right) \cos{\left(v \right)}}{6}\right)-\left(\frac{u \left(2\right) \cos{\left(v \right)}}{6}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{\frac{\pi}{6}}^{2 \pi}\left(\left(u \cos{\left(v \right)}\right)-\left(\frac{u \cos{\left(v \right)}}{3}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{\frac{\pi}{6}}^{2 \pi}\left(\frac{2 u \cos{\left(v \right)}}{3}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left[\frac{2 u \sin{\left(v \right)}}{3}\right]_{v=\frac{\pi}{6}}^{v=2 \pi}\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left(\frac{2 u \sin{\left(\left(2 \pi\right) \right)}}{3}\right)-\left(\frac{2 u \sin{\left(\left(\frac{\pi}{6}\right) \right)}}{3}\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left(0\right)-\left(\frac{u}{3}\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(- \frac{u}{3}\right)\,\mathrm{d}u \\  & =\left[- \frac{u^{2}}{6}\right]_{u=1}^{u=3} \\  & =\left(- \frac{\left(3\right)^{2}}{6}\right)-\left(- \frac{\left(1\right)^{2}}{6}\right) \\  & =\left(- \frac{3}{2}\right)-\left(- \frac{1}{6}\right) \\  & =- \frac{4}{3}\end{aligned}
$$

## ucosv — hard

Use the change of variables 

$$
u=x^{2} + 4 y,\quad v=x + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(x^{2} + 4 y\right) \cos{\left(x + z \right)}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):1\le x^{2} + 4 y\le 3,\quad \frac{\pi}{6}\le x + z\le \frac{\pi}{2},\quad 1\le z\le 3\}.
$$

- A. $64$
- B. $2$
- C. $- \sqrt{3}$
- D. $1$
- E. $8$

Correct: 1

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
u=x^{2} + 4 y,\quad v=x + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):1\le u\le 3,\quad \frac{\pi}{6}\le v\le \frac{\pi}{2},\quad 2\le w\le 6\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}2 x & 4 & 0 \\ 1 & 0 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}2 x & 4 \\ 1 & 0\end{vmatrix} \\  & =\left(2\right)\left(\left(2 x\right)\cdot \left(0\right)-\left(4\right)\cdot \left(1\right)\right) \\  & =-8.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{8}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(x^{2} + 4 y\right) \cos{\left(x + z \right)}\right)\,\mathrm{d}V & =\iiint_\Delta \left(u \cos{\left(v \right)}\right)\cdot \left|- \frac{1}{8}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{u \cos{\left(v \right)}}{8}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{1}^{3}\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\int_{2}^{6}\left(\frac{u \cos{\left(v \right)}}{8}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\left(\left[\frac{u w \cos{\left(v \right)}}{8}\right]_{w=2}^{w=6}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\left(\left(\frac{u \left(6\right) \cos{\left(v \right)}}{8}\right)-\left(\frac{u \left(2\right) \cos{\left(v \right)}}{8}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\left(\left(\frac{3 u \cos{\left(v \right)}}{4}\right)-\left(\frac{u \cos{\left(v \right)}}{4}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\left(\frac{u \cos{\left(v \right)}}{2}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left[\frac{u \sin{\left(v \right)}}{2}\right]_{v=\frac{\pi}{6}}^{v=\frac{\pi}{2}}\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left(\frac{u \sin{\left(\left(\frac{\pi}{2}\right) \right)}}{2}\right)-\left(\frac{u \sin{\left(\left(\frac{\pi}{6}\right) \right)}}{2}\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left(\frac{u}{2}\right)-\left(\frac{u}{4}\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\frac{u}{4}\right)\,\mathrm{d}u \\  & =\left[\frac{u^{2}}{8}\right]_{u=1}^{u=3} \\  & =\left(\frac{\left(3\right)^{2}}{8}\right)-\left(\frac{\left(1\right)^{2}}{8}\right) \\  & =\left(\frac{9}{8}\right)-\left(\frac{1}{8}\right) \\  & =1\end{aligned}
$$

## sum — hard

Use the change of variables 

$$
u=x - \frac{y}{3},\quad v=\frac{y}{3},\quad w=\frac{z}{3}
$$

to evaluate the triple integral

$$
\iiint_R \left(x - \frac{y}{3} + \frac{z}{3}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):1\le x - \frac{y}{3}\le 3,\quad 1\le \frac{y}{3}\le 3,\quad 1\le z\le 4\}.
$$

- A. $\frac{34}{27}$
- B. $\frac{34}{3}$
- C. $102$
- D. $72$
- E. $30$

Correct: 102

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
u=x - \frac{y}{3},\quad v=\frac{y}{3},\quad w=\frac{z}{3}
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):1\le u\le 3,\quad 1\le v\le 3,\quad \frac{1}{3}\le w\le \frac{4}{3}\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}1 & - \frac{1}{3} & 0 \\ 0 & \frac{1}{3} & 0 \\ 0 & 0 & \frac{1}{3}\end{vmatrix} \\  & =\left(\frac{1}{3}\right)(-1)^{3+3}\begin{vmatrix}1 & - \frac{1}{3} \\ 0 & \frac{1}{3}\end{vmatrix} \\  & =\left(\frac{1}{3}\right)\left(\left(1\right)\cdot \left(\frac{1}{3}\right)-\left(- \frac{1}{3}\right)\cdot \left(0\right)\right) \\  & =\frac{1}{9}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=9.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(x - \frac{y}{3} + \frac{z}{3}\right)\,\mathrm{d}V & =\iiint_\Delta \left(u + w\right)\cdot \left|9\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(9 u + 9 w\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{1}^{3}\int_{1}^{3}\int_{\frac{1}{3}}^{\frac{4}{3}}\left(9 u + 9 w\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{3}\left(\left[9 u w + \frac{9 w^{2}}{2}\right]_{w=\frac{1}{3}}^{w=\frac{4}{3}}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{3}\left(\left(\frac{9 \left(\frac{4}{3}\right)^{2}}{2}\right)-\left(\frac{9 \left(\frac{1}{3}\right)^{2}}{2}\right)+\left(9 u \left(\frac{4}{3}\right)\right)-\left(9 u \left(\frac{1}{3}\right)\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{3}\left(\left(8\right)-\left(\frac{1}{2}\right)+\left(12 u\right)-\left(3 u\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{3}\left(9 u + \frac{15}{2}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left[v \left(9 u + \frac{15}{2}\right)\right]_{v=1}^{v=3}\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left(\frac{15 \left(3\right)}{2}\right)-\left(\frac{15 \left(1\right)}{2}\right)+\left(9 u \left(3\right)\right)-\left(9 u \left(1\right)\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left(\frac{45}{2}\right)-\left(\frac{15}{2}\right)+\left(27 u\right)-\left(9 u\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(18 u + 15\right)\,\mathrm{d}u \\  & =\left[9 u^{2} + 15 u\right]_{u=1}^{u=3} \\  & =\left(9 \left(3\right)^{2}\right)-\left(9 \left(1\right)^{2}\right)+\left(15 \left(3\right)\right)-\left(15 \left(1\right)\right) \\  & =\left(81\right)-\left(9\right)+\left(45\right)-\left(15\right) \\  & =102\end{aligned}
$$

## sum — hard

Use the change of variables 

$$
u=x - \frac{y}{4},\quad v=\frac{y}{4},\quad w=\frac{z}{3}
$$

to evaluate the triple integral

$$
\iiint_R \left(x - \frac{y}{4} + \frac{z}{3}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):1\le x - \frac{y}{4}\le 3,\quad 1\le \frac{y}{4}\le 2,\quad 1\le z\le 2\}.
$$

- A. $\frac{5}{36}$
- B. $4$
- C. $16$
- D. $20$
- E. $\frac{5}{3}$

Correct: 20

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
u=x - \frac{y}{4},\quad v=\frac{y}{4},\quad w=\frac{z}{3}
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):1\le u\le 3,\quad 1\le v\le 2,\quad \frac{1}{3}\le w\le \frac{2}{3}\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}1 & - \frac{1}{4} & 0 \\ 0 & \frac{1}{4} & 0 \\ 0 & 0 & \frac{1}{3}\end{vmatrix} \\  & =\left(\frac{1}{3}\right)(-1)^{3+3}\begin{vmatrix}1 & - \frac{1}{4} \\ 0 & \frac{1}{4}\end{vmatrix} \\  & =\left(\frac{1}{3}\right)\left(\left(1\right)\cdot \left(\frac{1}{4}\right)-\left(- \frac{1}{4}\right)\cdot \left(0\right)\right) \\  & =\frac{1}{12}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=12.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(x - \frac{y}{4} + \frac{z}{3}\right)\,\mathrm{d}V & =\iiint_\Delta \left(u + w\right)\cdot \left|12\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(12 u + 12 w\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{1}^{3}\int_{1}^{2}\int_{\frac{1}{3}}^{\frac{2}{3}}\left(12 u + 12 w\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{2}\left(\left[12 u w + 6 w^{2}\right]_{w=\frac{1}{3}}^{w=\frac{2}{3}}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{2}\left(\left(6 \left(\frac{2}{3}\right)^{2}\right)-\left(6 \left(\frac{1}{3}\right)^{2}\right)+\left(12 u \left(\frac{2}{3}\right)\right)-\left(12 u \left(\frac{1}{3}\right)\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{2}\left(\left(\frac{8}{3}\right)-\left(\frac{2}{3}\right)+\left(8 u\right)-\left(4 u\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{2}\left(4 u + 2\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left[v \left(4 u + 2\right)\right]_{v=1}^{v=2}\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left(2 \left(2\right)\right)-\left(2 \left(1\right)\right)+\left(4 u \left(2\right)\right)-\left(4 u \left(1\right)\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left(4\right)-\left(2\right)+\left(8 u\right)-\left(4 u\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(4 u + 2\right)\,\mathrm{d}u \\  & =\left[2 u^{2} + 2 u\right]_{u=1}^{u=3} \\  & =\left(2 \left(3\right)\right)-\left(2 \left(1\right)\right)+\left(2 \left(3\right)^{2}\right)-\left(2 \left(1\right)^{2}\right) \\  & =\left(6\right)-\left(2\right)+\left(18\right)-\left(2\right) \\  & =20\end{aligned}
$$

## exp — hard

Use the change of variables 

$$
u=x + y^{2},\quad v=y - z,\quad w=4 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(y - z\right) e^{x + y^{2}}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):1\le x + y^{2}\le 3,\quad 1\le y - z\le 2,\quad 1\le z\le 4\}.
$$

- A. $- 72 e \left(- e^{2} + 1\right)$
- B. $- 18 e \left(- e^{2} + 1\right)$
- C. $- \frac{9 e \left(- e^{2} + 1\right)}{2}$
- D. $- 9 e \left(- e^{2} + 1\right)$
- E. $\frac{9 e^{3}}{2}$

Correct: - \frac{9 e \left(- e^{2} + 1\right)}{2}

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
u=x + y^{2},\quad v=y - z,\quad w=4 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):1\le u\le 3,\quad 1\le v\le 2,\quad 4\le w\le 16\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}1 & 2 y & 0 \\ 0 & 1 & -1 \\ 0 & 0 & 4\end{vmatrix} \\  & =\left(4\right)(-1)^{3+3}\begin{vmatrix}1 & 2 y \\ 0 & 1\end{vmatrix} \\  & =\left(4\right)\left(\left(1\right)\cdot \left(1\right)-\left(2 y\right)\cdot \left(0\right)\right) \\  & =4.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=\frac{1}{4}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(y - z\right) e^{x + y^{2}}\right)\,\mathrm{d}V & =\iiint_\Delta \left(v e^{u}\right)\cdot \left|\frac{1}{4}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{v e^{u}}{4}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{1}^{3}\int_{1}^{2}\int_{4}^{16}\left(\frac{v e^{u}}{4}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{2}\left(\left[\frac{v w e^{u}}{4}\right]_{w=4}^{w=16}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{2}\left(\left(\frac{v \left(16\right) e^{u}}{4}\right)-\left(\frac{v \left(4\right) e^{u}}{4}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{2}\left(\left(4 v e^{u}\right)-\left(v e^{u}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\int_{1}^{2}\left(3 v e^{u}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left[\frac{3 v^{2} e^{u}}{2}\right]_{v=1}^{v=2}\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left(\frac{3 \left(2\right)^{2} e^{u}}{2}\right)-\left(\frac{3 \left(1\right)^{2} e^{u}}{2}\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\left(6 e^{u}\right)-\left(\frac{3 e^{u}}{2}\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{3}\left(\frac{9 e^{u}}{2}\right)\,\mathrm{d}u \\  & =\left[\frac{9 e^{u}}{2}\right]_{u=1}^{u=3} \\  & =\left(\frac{9 e^{\left(3\right)}}{2}\right)-\left(\frac{9 e^{\left(1\right)}}{2}\right) \\  & =\left(\frac{9 e^{3}}{2}\right)-\left(\frac{9 e}{2}\right) \\  & =- \frac{9 e \left(- e^{2} + 1\right)}{2}\end{aligned}
$$

## exp — hard

Use the change of variables 

$$
u=x + y^{2},\quad v=y - 2 z,\quad w=3 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\left(y - 2 z\right) e^{x + y^{2}}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):1\le x + y^{2}\le 2,\quad 1\le y - 2 z\le 4,\quad 1\le z\le 3\}.
$$

- A. $135 e \left(-1 + e\right)$
- B. $15 e^{2}$
- C. $30 e \left(-1 + e\right)$
- D. $15 e \left(-1 + e\right)$
- E. $45 e \left(-1 + e\right)$

Correct: 15 e \left(-1 + e\right)

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
u=x + y^{2},\quad v=y - 2 z,\quad w=3 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):1\le u\le 2,\quad 1\le v\le 4,\quad 3\le w\le 9\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}1 & 2 y & 0 \\ 0 & 1 & -2 \\ 0 & 0 & 3\end{vmatrix} \\  & =\left(3\right)(-1)^{3+3}\begin{vmatrix}1 & 2 y \\ 0 & 1\end{vmatrix} \\  & =\left(3\right)\left(\left(1\right)\cdot \left(1\right)-\left(2 y\right)\cdot \left(0\right)\right) \\  & =3.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=\frac{1}{3}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\left(y - 2 z\right) e^{x + y^{2}}\right)\,\mathrm{d}V & =\iiint_\Delta \left(v e^{u}\right)\cdot \left|\frac{1}{3}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{v e^{u}}{3}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{1}^{2}\int_{1}^{4}\int_{3}^{9}\left(\frac{v e^{u}}{3}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{2}\int_{1}^{4}\left(\left[\frac{v w e^{u}}{3}\right]_{w=3}^{w=9}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{2}\int_{1}^{4}\left(\left(\frac{v \left(9\right) e^{u}}{3}\right)-\left(\frac{v \left(3\right) e^{u}}{3}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{2}\int_{1}^{4}\left(\left(3 v e^{u}\right)-\left(v e^{u}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{2}\int_{1}^{4}\left(2 v e^{u}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{1}^{2}\left(\left[v^{2} e^{u}\right]_{v=1}^{v=4}\right)\,\mathrm{d}u \\  & =\int_{1}^{2}\left(\left(\left(4\right)^{2} e^{u}\right)-\left(\left(1\right)^{2} e^{u}\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{2}\left(\left(16 e^{u}\right)-\left(e^{u}\right)\right)\,\mathrm{d}u \\  & =\int_{1}^{2}\left(15 e^{u}\right)\,\mathrm{d}u \\  & =\left[15 e^{u}\right]_{u=1}^{u=2} \\  & =\left(15 e^{\left(2\right)}\right)-\left(15 e^{\left(1\right)}\right) \\  & =\left(15 e^{2}\right)-\left(15 e\right) \\  & =15 e \left(-1 + e\right)\end{aligned}
$$

## zcosu — hard

Use the change of variables 

$$
u=3 x + 3 y,\quad v=x + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(z^{2} \cos{\left(3 x + 3 y \right)}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):\frac{\pi}{6}\le 3 x + 3 y\le \frac{\pi}{2},\quad 1\le x + z\le 3,\quad 1\le z\le 4\}.
$$

- A. $252$
- B. $42$
- C. $7$
- D. $21$
- E. $28$

Correct: 7

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
u=3 x + 3 y,\quad v=x + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):\frac{\pi}{6}\le u\le \frac{\pi}{2},\quad 1\le v\le 3,\quad 2\le w\le 8\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}3 & 3 & 0 \\ 1 & 0 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}3 & 3 \\ 1 & 0\end{vmatrix} \\  & =\left(2\right)\left(\left(3\right)\cdot \left(0\right)-\left(3\right)\cdot \left(1\right)\right) \\  & =-6.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{6}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(z^{2} \cos{\left(3 x + 3 y \right)}\right)\,\mathrm{d}V & =\iiint_\Delta \left(\frac{w^{2} \cos{\left(u \right)}}{4}\right)\cdot \left|- \frac{1}{6}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{w^{2} \cos{\left(u \right)}}{24}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\int_{1}^{3}\int_{2}^{8}\left(\frac{w^{2} \cos{\left(u \right)}}{24}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\int_{1}^{3}\left(\left[\frac{w^{3} \cos{\left(u \right)}}{72}\right]_{w=2}^{w=8}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\int_{1}^{3}\left(\left(\frac{\left(8\right)^{3} \cos{\left(u \right)}}{72}\right)-\left(\frac{\left(2\right)^{3} \cos{\left(u \right)}}{72}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\int_{1}^{3}\left(\left(\frac{64 \cos{\left(u \right)}}{9}\right)-\left(\frac{\cos{\left(u \right)}}{9}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\int_{1}^{3}\left(7 \cos{\left(u \right)}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\left(\left[7 v \cos{\left(u \right)}\right]_{v=1}^{v=3}\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\left(\left(7 \left(3\right) \cos{\left(u \right)}\right)-\left(7 \left(1\right) \cos{\left(u \right)}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\left(\left(21 \cos{\left(u \right)}\right)-\left(7 \cos{\left(u \right)}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}}\left(14 \cos{\left(u \right)}\right)\,\mathrm{d}u \\  & =\left[14 \sin{\left(u \right)}\right]_{u=\frac{\pi}{6}}^{u=\frac{\pi}{2}} \\  & =\left(14 \sin{\left(\left(\frac{\pi}{2}\right) \right)}\right)-\left(14 \sin{\left(\left(\frac{\pi}{6}\right) \right)}\right) \\  & =\left(14\right)-\left(7\right) \\  & =7\end{aligned}
$$

## zcosu — hard

Use the change of variables 

$$
u=- 2 x + 4 y,\quad v=x + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(z^{2} \cos{\left(2 x - 4 y \right)}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):\frac{\pi}{6}\le - 2 x + 4 y\le \pi,\quad 1\le x + z\le 2,\quad 1\le z\le 2\}.
$$

- A. $- \frac{56}{3}$
- B. $- \frac{7}{6}$
- C. $- \frac{7}{8}$
- D. $- \frac{7}{24}$
- E. $- \frac{7}{3}$

Correct: - \frac{7}{24}

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
u=- 2 x + 4 y,\quad v=x + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):\frac{\pi}{6}\le u\le \pi,\quad 1\le v\le 2,\quad 2\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}-2 & 4 & 0 \\ 1 & 0 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}-2 & 4 \\ 1 & 0\end{vmatrix} \\  & =\left(2\right)\left(\left(-2\right)\cdot \left(0\right)-\left(4\right)\cdot \left(1\right)\right) \\  & =-8.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{8}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(z^{2} \cos{\left(2 x - 4 y \right)}\right)\,\mathrm{d}V & =\iiint_\Delta \left(\frac{w^{2} \cos{\left(u \right)}}{4}\right)\cdot \left|- \frac{1}{8}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{w^{2} \cos{\left(u \right)}}{32}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{1}^{2}\int_{2}^{4}\left(\frac{w^{2} \cos{\left(u \right)}}{32}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{1}^{2}\left(\left[\frac{w^{3} \cos{\left(u \right)}}{96}\right]_{w=2}^{w=4}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{1}^{2}\left(\left(\frac{\left(4\right)^{3} \cos{\left(u \right)}}{96}\right)-\left(\frac{\left(2\right)^{3} \cos{\left(u \right)}}{96}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{1}^{2}\left(\left(\frac{2 \cos{\left(u \right)}}{3}\right)-\left(\frac{\cos{\left(u \right)}}{12}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{1}^{2}\left(\frac{7 \cos{\left(u \right)}}{12}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left[\frac{7 v \cos{\left(u \right)}}{12}\right]_{v=1}^{v=2}\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left(\frac{7 \left(2\right) \cos{\left(u \right)}}{12}\right)-\left(\frac{7 \left(1\right) \cos{\left(u \right)}}{12}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left(\frac{7 \cos{\left(u \right)}}{6}\right)-\left(\frac{7 \cos{\left(u \right)}}{12}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\frac{7 \cos{\left(u \right)}}{12}\right)\,\mathrm{d}u \\  & =\left[\frac{7 \sin{\left(u \right)}}{12}\right]_{u=\frac{\pi}{6}}^{u=\pi} \\  & =\left(\frac{7 \sin{\left(\left(\pi\right) \right)}}{12}\right)-\left(\frac{7 \sin{\left(\left(\frac{\pi}{6}\right) \right)}}{12}\right) \\  & =\left(0\right)-\left(\frac{7}{24}\right) \\  & =- \frac{7}{24}\end{aligned}
$$

## sinsin — hard

Use the change of variables 

$$
u=x^{2} + 3 y,\quad v=x + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\sin{\left(x + z \right)} \sin{\left(x^{2} + 3 y \right)}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):\frac{\pi}{6}\le x^{2} + 3 y\le \pi,\quad \pi\le x + z\le 2 \pi,\quad 1\le z\le 3\}.
$$

- A. $-48 - 24 \sqrt{3}$
- B. $-8 - 4 \sqrt{3}$
- C. $- \frac{4}{3} - \frac{2 \sqrt{3}}{3}$
- D. $\frac{2 \sqrt{3}}{3} + \frac{4}{3}$
- E. $- \frac{2}{3} - \frac{\sqrt{3}}{3}$

Correct: - \frac{4}{3} - \frac{2 \sqrt{3}}{3}

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
u=x^{2} + 3 y,\quad v=x + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):\frac{\pi}{6}\le u\le \pi,\quad \pi\le v\le 2 \pi,\quad 2\le w\le 6\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}2 x & 3 & 0 \\ 1 & 0 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}2 x & 3 \\ 1 & 0\end{vmatrix} \\  & =\left(2\right)\left(\left(2 x\right)\cdot \left(0\right)-\left(3\right)\cdot \left(1\right)\right) \\  & =-6.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{6}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\sin{\left(x + z \right)} \sin{\left(x^{2} + 3 y \right)}\right)\,\mathrm{d}V & =\iiint_\Delta \left(\sin{\left(u \right)} \sin{\left(v \right)}\right)\cdot \left|- \frac{1}{6}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{\sin{\left(u \right)} \sin{\left(v \right)}}{6}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{\pi}^{2 \pi}\int_{2}^{6}\left(\frac{\sin{\left(u \right)} \sin{\left(v \right)}}{6}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{\pi}^{2 \pi}\left(\left[\frac{w \sin{\left(u \right)} \sin{\left(v \right)}}{6}\right]_{w=2}^{w=6}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{\pi}^{2 \pi}\left(\left(\frac{\left(6\right) \sin{\left(u \right)} \sin{\left(v \right)}}{6}\right)-\left(\frac{\left(2\right) \sin{\left(u \right)} \sin{\left(v \right)}}{6}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{\pi}^{2 \pi}\left(\left(\sin{\left(u \right)} \sin{\left(v \right)}\right)-\left(\frac{\sin{\left(u \right)} \sin{\left(v \right)}}{3}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{\pi}^{2 \pi}\left(\frac{2 \sin{\left(u \right)} \sin{\left(v \right)}}{3}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left[- \frac{2 \sin{\left(u \right)} \cos{\left(v \right)}}{3}\right]_{v=\pi}^{v=2 \pi}\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left(- \frac{2 \sin{\left(u \right)} \cos{\left(\left(2 \pi\right) \right)}}{3}\right)-\left(- \frac{2 \sin{\left(u \right)} \cos{\left(\left(\pi\right) \right)}}{3}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left(- \frac{2 \sin{\left(u \right)}}{3}\right)-\left(\frac{2 \sin{\left(u \right)}}{3}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(- \frac{4 \sin{\left(u \right)}}{3}\right)\,\mathrm{d}u \\  & =\left[\frac{4 \cos{\left(u \right)}}{3}\right]_{u=\frac{\pi}{6}}^{u=\pi} \\  & =\left(\frac{4 \cos{\left(\left(\pi\right) \right)}}{3}\right)-\left(\frac{4 \cos{\left(\left(\frac{\pi}{6}\right) \right)}}{3}\right) \\  & =\left(- \frac{4}{3}\right)-\left(\frac{2 \sqrt{3}}{3}\right) \\  & =- \frac{4}{3} - \frac{2 \sqrt{3}}{3}\end{aligned}
$$

## sinsin — hard

Use the change of variables 

$$
u=x^{2} + 4 y,\quad v=x + z,\quad w=2 z
$$

to evaluate the triple integral

$$
\iiint_R \left(\sin{\left(x + z \right)} \sin{\left(x^{2} + 4 y \right)}\right)\,\mathrm{d}V,
$$

 
where the region $R$ is given by

$$
R=\{(x,y,z):\frac{\pi}{6}\le x^{2} + 4 y\le \pi,\quad \pi\le x + z\le 2 \pi,\quad 1\le z\le 3\}.
$$

- A. $-64 - 32 \sqrt{3}$
- B. $- \frac{1}{2} - \frac{\sqrt{3}}{4}$
- C. $\frac{\sqrt{3}}{2} + 1$
- D. $-1 - \frac{\sqrt{3}}{2}$
- E. $-8 - 4 \sqrt{3}$

Correct: -1 - \frac{\sqrt{3}}{2}

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
u=x^{2} + 4 y,\quad v=x + z,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\Delta=\{(u,v,w):\frac{\pi}{6}\le u\le \pi,\quad \pi\le v\le 2 \pi,\quad 2\le w\le 6\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}2 x & 4 & 0 \\ 1 & 0 & 1 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{3+3}\begin{vmatrix}2 x & 4 \\ 1 & 0\end{vmatrix} \\  & =\left(2\right)\left(\left(2 x\right)\cdot \left(0\right)-\left(4\right)\cdot \left(1\right)\right) \\  & =-8.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{8}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(\sin{\left(x + z \right)} \sin{\left(x^{2} + 4 y \right)}\right)\,\mathrm{d}V & =\iiint_\Delta \left(\sin{\left(u \right)} \sin{\left(v \right)}\right)\cdot \left|- \frac{1}{8}\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\iiint_\Delta \left(\frac{\sin{\left(u \right)} \sin{\left(v \right)}}{8}\right)\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{\pi}^{2 \pi}\int_{2}^{6}\left(\frac{\sin{\left(u \right)} \sin{\left(v \right)}}{8}\right)\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{\pi}^{2 \pi}\left(\left[\frac{w \sin{\left(u \right)} \sin{\left(v \right)}}{8}\right]_{w=2}^{w=6}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{\pi}^{2 \pi}\left(\left(\frac{\left(6\right) \sin{\left(u \right)} \sin{\left(v \right)}}{8}\right)-\left(\frac{\left(2\right) \sin{\left(u \right)} \sin{\left(v \right)}}{8}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{\pi}^{2 \pi}\left(\left(\frac{3 \sin{\left(u \right)} \sin{\left(v \right)}}{4}\right)-\left(\frac{\sin{\left(u \right)} \sin{\left(v \right)}}{4}\right)\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\int_{\pi}^{2 \pi}\left(\frac{\sin{\left(u \right)} \sin{\left(v \right)}}{2}\right)\,\mathrm{d}v\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left[- \frac{\sin{\left(u \right)} \cos{\left(v \right)}}{2}\right]_{v=\pi}^{v=2 \pi}\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left(- \frac{\sin{\left(u \right)} \cos{\left(\left(2 \pi\right) \right)}}{2}\right)-\left(- \frac{\sin{\left(u \right)} \cos{\left(\left(\pi\right) \right)}}{2}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(\left(- \frac{\sin{\left(u \right)}}{2}\right)-\left(\frac{\sin{\left(u \right)}}{2}\right)\right)\,\mathrm{d}u \\  & =\int_{\frac{\pi}{6}}^{\pi}\left(- \sin{\left(u \right)}\right)\,\mathrm{d}u \\  & =\left[\cos{\left(u \right)}\right]_{u=\frac{\pi}{6}}^{u=\pi} \\  & =\left(\cos{\left(\left(\pi\right) \right)}\right)-\left(\cos{\left(\left(\frac{\pi}{6}\right) \right)}\right) \\  & =\left(-1\right)-\left(\frac{\sqrt{3}}{2}\right) \\  & =-1 - \frac{\sqrt{3}}{2}\end{aligned}
$$
