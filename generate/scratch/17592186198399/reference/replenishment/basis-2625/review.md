## Generated variant / easy / affine

Find the volume bounded by the region $R,$ given by

$$
R=\big\{(x,y,z)\, :\, 0\le 2 x\le 5,\quad 0\le - 3 x + y\le 2,\quad 0\le 3 z\le 3\big\}.
$$

 - $\frac{5}{2}$

 - $180$

 - $30$

 - $5$ **CORRECT**

 - $1$

Recall that the volume of $R$ can be found as 

$$
V={∭}_{R}\text{d}V.
$$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To compute the required volume, we can use the change of variables formula

$$
{∭}_{R}f(x,y,z)\text{ }dV={∭}_{Δ}\text{ }f(x(u,v,w),y(u,v,w),z(u,v,w))\,|\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

The inequalities that define the region $R,$

$$
0\le 2 x\le 5,\quad 0\le - 3 x + y\le 2,\quad 0\le 3 z\le 3,
$$

suggest that we use the change of variables

$$
u=2 x,\quad v=- 3 x + y,\quad w=3 z.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y,z)\longmapsto(u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
\Delta=\big\{(u,v,w):0\le u\le 5,\quad 0\le v\le 2,\quad 0\le w\le 3\big\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}2 & 0 & 0 \\ -3 & 1 & 0 \\ 0 & 0 & 3\end{vmatrix} \\  & =\left(2\right)(-1)^{1+1}\begin{vmatrix}1 & 0 \\ 0 & 3\end{vmatrix}+\left(0\right)(-1)^{1+2}\begin{vmatrix}-3 & 0 \\ 0 & 3\end{vmatrix}+\left(0\right)(-1)^{1+3}\begin{vmatrix}-3 & 1 \\ 0 & 0\end{vmatrix} \\  & =6\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=\frac{1}{6}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

The map to $R$ is

$$
T(u,v,w)=\left(\frac{u}{2},\frac{3 u}{2} + v,\frac{w}{3}\right).
$$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R\mathrm{d}V & =\iiint_\Delta 1\cdot |\frac{1}{6}|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{5}\int_{0}^{2}\int_{0}^{3}\frac{1}{6}\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\frac{1}{6}\cdot \int_{0}^{5}1\,\mathrm{d}u\cdot \int_{0}^{2}1\,\mathrm{d}v\cdot \int_{0}^{3}1\,\mathrm{d}w \\  & =\frac{1}{6}\cdot [u]_{0}^{5}\cdot [v]_{0}^{2}\cdot [w]_{0}^{3} \\  & =\frac{1}{6}\cdot \left(\left(\left(5\right)\right)-\left(\left(0\right)\right)\right)\cdot \left(\left(\left(2\right)\right)-\left(\left(0\right)\right)\right)\cdot \left(\left(\left(3\right)\right)-\left(\left(0\right)\right)\right) \\  & =\frac{1}{6}\cdot \left(\left(5\right)-\left(0\right)\right)\cdot \left(\left(2\right)-\left(0\right)\right)\cdot \left(\left(3\right)-\left(0\right)\right) \\  & =5\end{aligned}
$$

---

## Generated variant / easy / affine

Find the volume bounded by the region $R,$ given by

$$
R=\big\{(x,y,z)\, :\, 0\le 2 x\le 2,\quad 0\le x + y\le 3,\quad 0\le 2 z\le 6\big\}.
$$

 - $144$

 - $\frac{9}{2}$

 - $3$

 - $36$

 - $9$ **CORRECT**

Recall that the volume of $R$ can be found as 

$$
V={∭}_{R}\text{d}V.
$$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To compute the required volume, we can use the change of variables formula

$$
{∭}_{R}f(x,y,z)\text{ }dV={∭}_{Δ}\text{ }f(x(u,v,w),y(u,v,w),z(u,v,w))\,|\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

The inequalities that define the region $R,$

$$
0\le 2 x\le 2,\quad 0\le x + y\le 3,\quad 0\le 2 z\le 6,
$$

suggest that we use the change of variables

$$
u=2 x,\quad v=x + y,\quad w=2 z.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y,z)\longmapsto(u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
\Delta=\big\{(u,v,w):0\le u\le 2,\quad 0\le v\le 3,\quad 0\le w\le 6\big\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}2 & 0 & 0 \\ 1 & 1 & 0 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{1+1}\begin{vmatrix}1 & 0 \\ 0 & 2\end{vmatrix}+\left(0\right)(-1)^{1+2}\begin{vmatrix}1 & 0 \\ 0 & 2\end{vmatrix}+\left(0\right)(-1)^{1+3}\begin{vmatrix}1 & 1 \\ 0 & 0\end{vmatrix} \\  & =4\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=\frac{1}{4}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

The map to $R$ is

$$
T(u,v,w)=\left(\frac{u}{2},- \frac{u}{2} + v,\frac{w}{2}\right).
$$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R\mathrm{d}V & =\iiint_\Delta 1\cdot |\frac{1}{4}|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{2}\int_{0}^{3}\int_{0}^{6}\frac{1}{4}\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\frac{1}{4}\cdot \int_{0}^{2}1\,\mathrm{d}u\cdot \int_{0}^{3}1\,\mathrm{d}v\cdot \int_{0}^{6}1\,\mathrm{d}w \\  & =\frac{1}{4}\cdot [u]_{0}^{2}\cdot [v]_{0}^{3}\cdot [w]_{0}^{6} \\  & =\frac{1}{4}\cdot \left(\left(\left(2\right)\right)-\left(\left(0\right)\right)\right)\cdot \left(\left(\left(3\right)\right)-\left(\left(0\right)\right)\right)\cdot \left(\left(\left(6\right)\right)-\left(\left(0\right)\right)\right) \\  & =\frac{1}{4}\cdot \left(\left(2\right)-\left(0\right)\right)\cdot \left(\left(3\right)-\left(0\right)\right)\cdot \left(\left(6\right)-\left(0\right)\right) \\  & =9\end{aligned}
$$

---

## Generated variant / easy / affine

Find the volume bounded by the region $R,$ given by

$$
R=\big\{(x,y,z)\, :\, 0\le 2 x\le 6,\quad 0\le - 2 x + y\le 5,\quad 0\le 2 z\le 2\big\}.
$$

 - $60$

 - $240$

 - $15$ **CORRECT**

 - $\frac{5}{2}$

 - $3$

Recall that the volume of $R$ can be found as 

$$
V={∭}_{R}\text{d}V.
$$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To compute the required volume, we can use the change of variables formula

$$
{∭}_{R}f(x,y,z)\text{ }dV={∭}_{Δ}\text{ }f(x(u,v,w),y(u,v,w),z(u,v,w))\,|\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

The inequalities that define the region $R,$

$$
0\le 2 x\le 6,\quad 0\le - 2 x + y\le 5,\quad 0\le 2 z\le 2,
$$

suggest that we use the change of variables

$$
u=2 x,\quad v=- 2 x + y,\quad w=2 z.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y,z)\longmapsto(u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
\Delta=\big\{(u,v,w):0\le u\le 6,\quad 0\le v\le 5,\quad 0\le w\le 2\big\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}2 & 0 & 0 \\ -2 & 1 & 0 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{1+1}\begin{vmatrix}1 & 0 \\ 0 & 2\end{vmatrix}+\left(0\right)(-1)^{1+2}\begin{vmatrix}-2 & 0 \\ 0 & 2\end{vmatrix}+\left(0\right)(-1)^{1+3}\begin{vmatrix}-2 & 1 \\ 0 & 0\end{vmatrix} \\  & =4\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=\frac{1}{4}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

The map to $R$ is

$$
T(u,v,w)=\left(\frac{u}{2},u + v,\frac{w}{2}\right).
$$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R\mathrm{d}V & =\iiint_\Delta 1\cdot |\frac{1}{4}|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{6}\int_{0}^{5}\int_{0}^{2}\frac{1}{4}\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\frac{1}{4}\cdot \int_{0}^{6}1\,\mathrm{d}u\cdot \int_{0}^{5}1\,\mathrm{d}v\cdot \int_{0}^{2}1\,\mathrm{d}w \\  & =\frac{1}{4}\cdot [u]_{0}^{6}\cdot [v]_{0}^{5}\cdot [w]_{0}^{2} \\  & =\frac{1}{4}\cdot \left(\left(\left(6\right)\right)-\left(\left(0\right)\right)\right)\cdot \left(\left(\left(5\right)\right)-\left(\left(0\right)\right)\right)\cdot \left(\left(\left(2\right)\right)-\left(\left(0\right)\right)\right) \\  & =\frac{1}{4}\cdot \left(\left(6\right)-\left(0\right)\right)\cdot \left(\left(5\right)-\left(0\right)\right)\cdot \left(\left(2\right)-\left(0\right)\right) \\  & =15\end{aligned}
$$

---

## Generated variant / easy / affine

Find the volume bounded by the region $R,$ given by

$$
R=\big\{(x,y,z)\, :\, 0\le 3 x\le 5,\quad 0\le x + y\le 4,\quad 0\le 2 z\le 2\big\}.
$$

 - $\frac{5}{3}$

 - $40$

 - $\frac{20}{3}$ **CORRECT**

 - $240$

 - $\frac{4}{3}$

Recall that the volume of $R$ can be found as 

$$
V={∭}_{R}\text{d}V.
$$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To compute the required volume, we can use the change of variables formula

$$
{∭}_{R}f(x,y,z)\text{ }dV={∭}_{Δ}\text{ }f(x(u,v,w),y(u,v,w),z(u,v,w))\,|\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

The inequalities that define the region $R,$

$$
0\le 3 x\le 5,\quad 0\le x + y\le 4,\quad 0\le 2 z\le 2,
$$

suggest that we use the change of variables

$$
u=3 x,\quad v=x + y,\quad w=2 z.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y,z)\longmapsto(u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
\Delta=\big\{(u,v,w):0\le u\le 5,\quad 0\le v\le 4,\quad 0\le w\le 2\big\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}3 & 0 & 0 \\ 1 & 1 & 0 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(3\right)(-1)^{1+1}\begin{vmatrix}1 & 0 \\ 0 & 2\end{vmatrix}+\left(0\right)(-1)^{1+2}\begin{vmatrix}1 & 0 \\ 0 & 2\end{vmatrix}+\left(0\right)(-1)^{1+3}\begin{vmatrix}1 & 1 \\ 0 & 0\end{vmatrix} \\  & =6\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=\frac{1}{6}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

The map to $R$ is

$$
T(u,v,w)=\left(\frac{u}{3},- \frac{u}{3} + v,\frac{w}{2}\right).
$$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R\mathrm{d}V & =\iiint_\Delta 1\cdot |\frac{1}{6}|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{5}\int_{0}^{4}\int_{0}^{2}\frac{1}{6}\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\frac{1}{6}\cdot \int_{0}^{5}1\,\mathrm{d}u\cdot \int_{0}^{4}1\,\mathrm{d}v\cdot \int_{0}^{2}1\,\mathrm{d}w \\  & =\frac{1}{6}\cdot [u]_{0}^{5}\cdot [v]_{0}^{4}\cdot [w]_{0}^{2} \\  & =\frac{1}{6}\cdot \left(\left(\left(5\right)\right)-\left(\left(0\right)\right)\right)\cdot \left(\left(\left(4\right)\right)-\left(\left(0\right)\right)\right)\cdot \left(\left(\left(2\right)\right)-\left(\left(0\right)\right)\right) \\  & =\frac{1}{6}\cdot \left(\left(5\right)-\left(0\right)\right)\cdot \left(\left(4\right)-\left(0\right)\right)\cdot \left(\left(2\right)-\left(0\right)\right) \\  & =\frac{20}{3}\end{aligned}
$$

---

## Generated variant / easy / affine

Find the volume bounded by the region $R,$ given by

$$
R=\big\{(x,y,z)\, :\, 0\le 2 x\le 5,\quad 0\le 2 x + y\le 2,\quad 0\le 2 z\le 4\big\}.
$$

 - $40$

 - $5$

 - $160$

 - $10$ **CORRECT**

 - $2$

Recall that the volume of $R$ can be found as 

$$
V={∭}_{R}\text{d}V.
$$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To compute the required volume, we can use the change of variables formula

$$
{∭}_{R}f(x,y,z)\text{ }dV={∭}_{Δ}\text{ }f(x(u,v,w),y(u,v,w),z(u,v,w))\,|\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

The inequalities that define the region $R,$

$$
0\le 2 x\le 5,\quad 0\le 2 x + y\le 2,\quad 0\le 2 z\le 4,
$$

suggest that we use the change of variables

$$
u=2 x,\quad v=2 x + y,\quad w=2 z.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y,z)\longmapsto(u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
\Delta=\big\{(u,v,w):0\le u\le 5,\quad 0\le v\le 2,\quad 0\le w\le 4\big\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}2 & 0 & 0 \\ 2 & 1 & 0 \\ 0 & 0 & 2\end{vmatrix} \\  & =\left(2\right)(-1)^{1+1}\begin{vmatrix}1 & 0 \\ 0 & 2\end{vmatrix}+\left(0\right)(-1)^{1+2}\begin{vmatrix}2 & 0 \\ 0 & 2\end{vmatrix}+\left(0\right)(-1)^{1+3}\begin{vmatrix}2 & 1 \\ 0 & 0\end{vmatrix} \\  & =4\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=\frac{1}{4}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

The map to $R$ is

$$
T(u,v,w)=\left(\frac{u}{2},- u + v,\frac{w}{2}\right).
$$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R\mathrm{d}V & =\iiint_\Delta 1\cdot |\frac{1}{4}|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{5}\int_{0}^{2}\int_{0}^{4}\frac{1}{4}\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\frac{1}{4}\cdot \int_{0}^{5}1\,\mathrm{d}u\cdot \int_{0}^{2}1\,\mathrm{d}v\cdot \int_{0}^{4}1\,\mathrm{d}w \\  & =\frac{1}{4}\cdot [u]_{0}^{5}\cdot [v]_{0}^{2}\cdot [w]_{0}^{4} \\  & =\frac{1}{4}\cdot \left(\left(\left(5\right)\right)-\left(\left(0\right)\right)\right)\cdot \left(\left(\left(2\right)\right)-\left(\left(0\right)\right)\right)\cdot \left(\left(\left(4\right)\right)-\left(\left(0\right)\right)\right) \\  & =\frac{1}{4}\cdot \left(\left(5\right)-\left(0\right)\right)\cdot \left(\left(2\right)-\left(0\right)\right)\cdot \left(\left(4\right)-\left(0\right)\right) \\  & =10\end{aligned}
$$