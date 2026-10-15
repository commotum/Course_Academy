## Generated variant / easy / exp

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): 1\le x + 2 y\le 2,\quad 0\le - x + y\le 1,\quad 0\le z\le 4\}.
$$

Given the change of variables

$$
u=x + 2 y,\quad v=- x + y,\quad w=z,
$$

Which of the following could be the missing part of the expression below?

$$
\iiint_R \left(x + 2 y\right) e^{- x + y}\,dV=\int_{1}^{2}\int_{0}^{1}\int_{0}^{4}\left(\boxed{?}\right)\,dw\,dv\,du
$$

- $\frac{e^{v}}{3}$
- $u e^{v}$
- $\frac{v e^{u}}{3}$
- $\frac{e^{u}}{3}$
- $\frac{u e^{v}}{3}$ **correct**

Let's define a transformation $T$ as follows:

$$
T:(u,v,w)\longmapsto (x(u,v,w),y(u,v,w),z(u,v,w)).
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To find the required integral, we can use the change of variables formula

$$
\iiint_R f(x,y,z)\,dV=\iiint_Δ f(x(u,v,w),y(u,v,w),z(u,v,w))\left|\frac{\partial(x,y,z)}{\partial(u,v,w)}\right|\,du\,dv\,dw
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x + 2 y,\quad v=- x + y,\quad w=z
$$

gives us the *inverse* function ${T}^{-1}$.

$$
T^{-1}:(x,y,z)\longmapsto (u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
Δ=\{(u,v,w): 1\le u\le 2,\quad 0\le v\le 1,\quad 0\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}1 & 2 & 0\\-1 & 1 & 0\\0 & 0 & 1\end{vmatrix}\\ &=(1)\begin{vmatrix}1 & 0\\0 & 1\end{vmatrix}-(2)\begin{vmatrix}-1 & 0\\0 & 1\end{vmatrix}+(0)\begin{vmatrix}-1 & 1\\0 & 0\end{vmatrix}\\ &=3\\ &=3.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=\frac{1}{3}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(x + 2 y\right) e^{- x + y}\,dV &=\iiint_Δ \left(u e^{v}\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(u e^{v}\right)\left|\frac{1}{3}\right|\,du\,dv\,dw\\ &=\int_{1}^{2}\int_{0}^{1}\int_{0}^{4}\left(\frac{u e^{v}}{3}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated variant / easy / exp

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): 1\le x + 4 y\le 2,\quad 0\le - x + y\le 1,\quad 0\le z\le 5\}.
$$

Given the change of variables

$$
u=x + 4 y,\quad v=- x + y,\quad w=z,
$$

Which of the following could be the missing part of the expression below?

$$
\iiint_R \left(x + 4 y\right) e^{- x + y}\,dV=\int_{1}^{2}\int_{0}^{1}\int_{0}^{5}\left(\boxed{?}\right)\,dw\,dv\,du
$$

- $\frac{e^{v}}{5}$
- $\frac{e^{u}}{5}$
- $u e^{v}$
- $\frac{u e^{v}}{5}$ **correct**
- $\frac{v e^{u}}{5}$

Let's define a transformation $T$ as follows:

$$
T:(u,v,w)\longmapsto (x(u,v,w),y(u,v,w),z(u,v,w)).
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To find the required integral, we can use the change of variables formula

$$
\iiint_R f(x,y,z)\,dV=\iiint_Δ f(x(u,v,w),y(u,v,w),z(u,v,w))\left|\frac{\partial(x,y,z)}{\partial(u,v,w)}\right|\,du\,dv\,dw
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x + 4 y,\quad v=- x + y,\quad w=z
$$

gives us the *inverse* function ${T}^{-1}$.

$$
T^{-1}:(x,y,z)\longmapsto (u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
Δ=\{(u,v,w): 1\le u\le 2,\quad 0\le v\le 1,\quad 0\le w\le 5\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}1 & 4 & 0\\-1 & 1 & 0\\0 & 0 & 1\end{vmatrix}\\ &=(1)\begin{vmatrix}1 & 0\\0 & 1\end{vmatrix}-(4)\begin{vmatrix}-1 & 0\\0 & 1\end{vmatrix}+(0)\begin{vmatrix}-1 & 1\\0 & 0\end{vmatrix}\\ &=5\\ &=5.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=\frac{1}{5}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(x + 4 y\right) e^{- x + y}\,dV &=\iiint_Δ \left(u e^{v}\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(u e^{v}\right)\left|\frac{1}{5}\right|\,du\,dv\,dw\\ &=\int_{1}^{2}\int_{0}^{1}\int_{0}^{5}\left(\frac{u e^{v}}{5}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated variant / easy / log

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): 1\le x^{2} + y\le 2,\quad -1\le 2 x + z\le 6,\quad 1\le z\le 4\}.
$$

Given the change of variables

$$
u=x^{2} + y,\quad v=2 x + z,\quad w=z,
$$

Which of the following could be the missing part of the expression below?

$$
\iiint_R \left(2 x + z\right) \ln{\left(x^{2} + y \right)}\,dV=\int_{1}^{2}\int_{-1}^{6}\int_{1}^{4}\left(\boxed{?}\right)\,dw\,dv\,du
$$

- $\frac{u \ln{\left(u \right)}}{2}$
- $v \ln{\left(u \right)}$
- $2 v \ln{\left(u \right)}$
- $- \frac{v \ln{\left(u \right)}}{2}$
- $\frac{v \ln{\left(u \right)}}{2}$ **correct**

Let's define a transformation $T$ as follows:

$$
T:(u,v,w)\longmapsto (x(u,v,w),y(u,v,w),z(u,v,w)).
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To find the required integral, we can use the change of variables formula

$$
\iiint_R f(x,y,z)\,dV=\iiint_Δ f(x(u,v,w),y(u,v,w),z(u,v,w))\left|\frac{\partial(x,y,z)}{\partial(u,v,w)}\right|\,du\,dv\,dw
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x^{2} + y,\quad v=2 x + z,\quad w=z
$$

gives us the *inverse* function ${T}^{-1}$.

$$
T^{-1}:(x,y,z)\longmapsto (u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
Δ=\{(u,v,w): 1\le u\le 2,\quad -1\le v\le 6,\quad 1\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}2 x & 1 & 0\\2 & 0 & 1\\0 & 0 & 1\end{vmatrix}\\ &=(2 x)\begin{vmatrix}0 & 1\\0 & 1\end{vmatrix}-(1)\begin{vmatrix}2 & 1\\0 & 1\end{vmatrix}+(0)\begin{vmatrix}2 & 0\\0 & 0\end{vmatrix}\\ &=-2\\ &=-2.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=- \frac{1}{2}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(2 x + z\right) \ln{\left(x^{2} + y \right)}\,dV &=\iiint_Δ \left(v \ln{\left(u \right)}\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(v \ln{\left(u \right)}\right)\left|- \frac{1}{2}\right|\,du\,dv\,dw\\ &=\int_{1}^{2}\int_{-1}^{6}\int_{1}^{4}\left(\frac{v \ln{\left(u \right)}}{2}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated variant / easy / log

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): 1\le x^{2} + y\le 2,\quad -1\le 4 x + z\le 8,\quad 1\le z\le 5\}.
$$

Given the change of variables

$$
u=x^{2} + y,\quad v=4 x + z,\quad w=z,
$$

Which of the following could be the missing part of the expression below?

$$
\iiint_R \left(4 x + z\right) \ln{\left(x^{2} + y \right)}\,dV=\int_{1}^{2}\int_{-1}^{8}\int_{1}^{5}\left(\boxed{?}\right)\,dw\,dv\,du
$$

- $\frac{u \ln{\left(u \right)}}{4}$
- $- \frac{v \ln{\left(u \right)}}{4}$
- $v \ln{\left(u \right)}$
- $\frac{v \ln{\left(u \right)}}{4}$ **correct**
- $4 v \ln{\left(u \right)}$

Let's define a transformation $T$ as follows:

$$
T:(u,v,w)\longmapsto (x(u,v,w),y(u,v,w),z(u,v,w)).
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To find the required integral, we can use the change of variables formula

$$
\iiint_R f(x,y,z)\,dV=\iiint_Δ f(x(u,v,w),y(u,v,w),z(u,v,w))\left|\frac{\partial(x,y,z)}{\partial(u,v,w)}\right|\,du\,dv\,dw
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x^{2} + y,\quad v=4 x + z,\quad w=z
$$

gives us the *inverse* function ${T}^{-1}$.

$$
T^{-1}:(x,y,z)\longmapsto (u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
Δ=\{(u,v,w): 1\le u\le 2,\quad -1\le v\le 8,\quad 1\le w\le 5\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}2 x & 1 & 0\\4 & 0 & 1\\0 & 0 & 1\end{vmatrix}\\ &=(2 x)\begin{vmatrix}0 & 1\\0 & 1\end{vmatrix}-(1)\begin{vmatrix}4 & 1\\0 & 1\end{vmatrix}+(0)\begin{vmatrix}4 & 0\\0 & 0\end{vmatrix}\\ &=-4\\ &=-4.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=- \frac{1}{4}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(4 x + z\right) \ln{\left(x^{2} + y \right)}\,dV &=\iiint_Δ \left(v \ln{\left(u \right)}\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(v \ln{\left(u \right)}\right)\left|- \frac{1}{4}\right|\,du\,dv\,dw\\ &=\int_{1}^{2}\int_{-1}^{8}\int_{1}^{5}\left(\frac{v \ln{\left(u \right)}}{4}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated variant / easy / cos2

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): 0\le x + 2 y\le \frac{\pi}{2},\quad 0\le - 2 y + z\le \frac{\pi}{2},\quad 0\le z\le 4\}.
$$

Given the change of variables

$$
u=x + 2 y,\quad v=- 2 y + z,\quad w=z,
$$

Which of the following could be the missing part of the expression below?

$$
\iiint_R \cos^{2}{\left(x + z \right)} \cos{\left(2 y - z \right)}\,dV=\int_{0}^{\frac{\pi}{2}}\int_{0}^{\frac{\pi}{2}}\int_{0}^{4}\left(\boxed{?}\right)\,dw\,dv\,du
$$

- $\frac{\cos{\left(v \right)} \cos^{2}{\left(u - v \right)}}{2}$
- $\cos{\left(v \right)} \cos^{2}{\left(u + v \right)}$
- $2 \cos{\left(v \right)} \cos^{2}{\left(u + v \right)}$
- $\frac{\cos^{2}{\left(u \right)} \cos{\left(v \right)}}{2}$
- $\frac{\cos{\left(v \right)} \cos^{2}{\left(u + v \right)}}{2}$ **correct**

Let's define a transformation $T$ as follows:

$$
T:(u,v,w)\longmapsto (x(u,v,w),y(u,v,w),z(u,v,w)).
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To find the required integral, we can use the change of variables formula

$$
\iiint_R f(x,y,z)\,dV=\iiint_Δ f(x(u,v,w),y(u,v,w),z(u,v,w))\left|\frac{\partial(x,y,z)}{\partial(u,v,w)}\right|\,du\,dv\,dw
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x + 2 y,\quad v=- 2 y + z,\quad w=z
$$

gives us the *inverse* function ${T}^{-1}$.

$$
T^{-1}:(x,y,z)\longmapsto (u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
Δ=\{(u,v,w): 0\le u\le \frac{\pi}{2},\quad 0\le v\le \frac{\pi}{2},\quad 0\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}1 & 2 & 0\\0 & -2 & 1\\0 & 0 & 1\end{vmatrix}\\ &=(1)\begin{vmatrix}-2 & 1\\0 & 1\end{vmatrix}-(2)\begin{vmatrix}0 & 1\\0 & 1\end{vmatrix}+(0)\begin{vmatrix}0 & -2\\0 & 0\end{vmatrix}\\ &=-2\\ &=-2.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=- \frac{1}{2}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \cos^{2}{\left(x + z \right)} \cos{\left(2 y - z \right)}\,dV &=\iiint_Δ \left(\cos{\left(v \right)} \cos^{2}{\left(u + v \right)}\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(\cos{\left(v \right)} \cos^{2}{\left(u + v \right)}\right)\left|- \frac{1}{2}\right|\,du\,dv\,dw\\ &=\int_{0}^{\frac{\pi}{2}}\int_{0}^{\frac{\pi}{2}}\int_{0}^{4}\left(\frac{\cos{\left(v \right)} \cos^{2}{\left(u + v \right)}}{2}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated variant / easy / cos2

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): 0\le x + 4 y\le \frac{\pi}{2},\quad 0\le - 4 y + z\le \frac{\pi}{2},\quad 0\le z\le 5\}.
$$

Given the change of variables

$$
u=x + 4 y,\quad v=- 4 y + z,\quad w=z,
$$

Which of the following could be the missing part of the expression below?

$$
\iiint_R \cos^{2}{\left(x + z \right)} \cos{\left(4 y - z \right)}\,dV=\int_{0}^{\frac{\pi}{2}}\int_{0}^{\frac{\pi}{2}}\int_{0}^{5}\left(\boxed{?}\right)\,dw\,dv\,du
$$

- $\frac{\cos{\left(v \right)} \cos^{2}{\left(u - v \right)}}{4}$
- $\frac{\cos^{2}{\left(u \right)} \cos{\left(v \right)}}{4}$
- $\cos{\left(v \right)} \cos^{2}{\left(u + v \right)}$
- $\frac{\cos{\left(v \right)} \cos^{2}{\left(u + v \right)}}{4}$ **correct**
- $4 \cos{\left(v \right)} \cos^{2}{\left(u + v \right)}$

Let's define a transformation $T$ as follows:

$$
T:(u,v,w)\longmapsto (x(u,v,w),y(u,v,w),z(u,v,w)).
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To find the required integral, we can use the change of variables formula

$$
\iiint_R f(x,y,z)\,dV=\iiint_Δ f(x(u,v,w),y(u,v,w),z(u,v,w))\left|\frac{\partial(x,y,z)}{\partial(u,v,w)}\right|\,du\,dv\,dw
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x + 4 y,\quad v=- 4 y + z,\quad w=z
$$

gives us the *inverse* function ${T}^{-1}$.

$$
T^{-1}:(x,y,z)\longmapsto (u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
Δ=\{(u,v,w): 0\le u\le \frac{\pi}{2},\quad 0\le v\le \frac{\pi}{2},\quad 0\le w\le 5\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}1 & 4 & 0\\0 & -4 & 1\\0 & 0 & 1\end{vmatrix}\\ &=(1)\begin{vmatrix}-4 & 1\\0 & 1\end{vmatrix}-(4)\begin{vmatrix}0 & 1\\0 & 1\end{vmatrix}+(0)\begin{vmatrix}0 & -4\\0 & 0\end{vmatrix}\\ &=-4\\ &=-4.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=- \frac{1}{4}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \cos^{2}{\left(x + z \right)} \cos{\left(4 y - z \right)}\,dV &=\iiint_Δ \left(\cos{\left(v \right)} \cos^{2}{\left(u + v \right)}\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(\cos{\left(v \right)} \cos^{2}{\left(u + v \right)}\right)\left|- \frac{1}{4}\right|\,du\,dv\,dw\\ &=\int_{0}^{\frac{\pi}{2}}\int_{0}^{\frac{\pi}{2}}\int_{0}^{5}\left(\frac{\cos{\left(v \right)} \cos^{2}{\left(u + v \right)}}{4}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated variant / easy / sin

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): \frac{3 \pi}{4}\le 2 x + y\le \pi,\quad 0\le y + z\le \frac{\pi}{2},\quad -1\le z\le 4\}.
$$

Given the change of variables

$$
u=2 x + y,\quad v=y + z,\quad w=z,
$$

Which of the following could be the missing part of the expression below?

$$
\iiint_R \sin{\left(2 x + y \right)} \cos{\left(y + z \right)}\,dV=\int_{\frac{3 \pi}{4}}^{\pi}\int_{0}^{\frac{\pi}{2}}\int_{-1}^{4}\left(\boxed{?}\right)\,dw\,dv\,du
$$

- $\frac{\sin{\left(v \right)} \cos{\left(u \right)}}{2}$
- $\sin{\left(u \right)} \cos{\left(v \right)}$
- $2 \sin{\left(u \right)} \cos{\left(v \right)}$
- $\frac{\sin{\left(u \right)} \sin{\left(v \right)}}{2}$
- $\frac{\sin{\left(u \right)} \cos{\left(v \right)}}{2}$ **correct**

Let's define a transformation $T$ as follows:

$$
T:(u,v,w)\longmapsto (x(u,v,w),y(u,v,w),z(u,v,w)).
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To find the required integral, we can use the change of variables formula

$$
\iiint_R f(x,y,z)\,dV=\iiint_Δ f(x(u,v,w),y(u,v,w),z(u,v,w))\left|\frac{\partial(x,y,z)}{\partial(u,v,w)}\right|\,du\,dv\,dw
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=2 x + y,\quad v=y + z,\quad w=z
$$

gives us the *inverse* function ${T}^{-1}$.

$$
T^{-1}:(x,y,z)\longmapsto (u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
Δ=\{(u,v,w): \frac{3 \pi}{4}\le u\le \pi,\quad 0\le v\le \frac{\pi}{2},\quad -1\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}2 & 1 & 0\\0 & 1 & 1\\0 & 0 & 1\end{vmatrix}\\ &=(2)\begin{vmatrix}1 & 1\\0 & 1\end{vmatrix}-(1)\begin{vmatrix}0 & 1\\0 & 1\end{vmatrix}+(0)\begin{vmatrix}0 & 1\\0 & 0\end{vmatrix}\\ &=2\\ &=2.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=\frac{1}{2}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \sin{\left(2 x + y \right)} \cos{\left(y + z \right)}\,dV &=\iiint_Δ \left(\sin{\left(u \right)} \cos{\left(v \right)}\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(\sin{\left(u \right)} \cos{\left(v \right)}\right)\left|\frac{1}{2}\right|\,du\,dv\,dw\\ &=\int_{\frac{3 \pi}{4}}^{\pi}\int_{0}^{\frac{\pi}{2}}\int_{-1}^{4}\left(\frac{\sin{\left(u \right)} \cos{\left(v \right)}}{2}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated variant / easy / sin

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): \frac{3 \pi}{4}\le 4 x + y\le \pi,\quad 0\le y + z\le \frac{\pi}{2},\quad -1\le z\le 5\}.
$$

Given the change of variables

$$
u=4 x + y,\quad v=y + z,\quad w=z,
$$

Which of the following could be the missing part of the expression below?

$$
\iiint_R \sin{\left(4 x + y \right)} \cos{\left(y + z \right)}\,dV=\int_{\frac{3 \pi}{4}}^{\pi}\int_{0}^{\frac{\pi}{2}}\int_{-1}^{5}\left(\boxed{?}\right)\,dw\,dv\,du
$$

- $\frac{\sin{\left(v \right)} \cos{\left(u \right)}}{4}$
- $\frac{\sin{\left(u \right)} \sin{\left(v \right)}}{4}$
- $\sin{\left(u \right)} \cos{\left(v \right)}$
- $\frac{\sin{\left(u \right)} \cos{\left(v \right)}}{4}$ **correct**
- $4 \sin{\left(u \right)} \cos{\left(v \right)}$

Let's define a transformation $T$ as follows:

$$
T:(u,v,w)\longmapsto (x(u,v,w),y(u,v,w),z(u,v,w)).
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To find the required integral, we can use the change of variables formula

$$
\iiint_R f(x,y,z)\,dV=\iiint_Δ f(x(u,v,w),y(u,v,w),z(u,v,w))\left|\frac{\partial(x,y,z)}{\partial(u,v,w)}\right|\,du\,dv\,dw
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=4 x + y,\quad v=y + z,\quad w=z
$$

gives us the *inverse* function ${T}^{-1}$.

$$
T^{-1}:(x,y,z)\longmapsto (u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
Δ=\{(u,v,w): \frac{3 \pi}{4}\le u\le \pi,\quad 0\le v\le \frac{\pi}{2},\quad -1\le w\le 5\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}4 & 1 & 0\\0 & 1 & 1\\0 & 0 & 1\end{vmatrix}\\ &=(4)\begin{vmatrix}1 & 1\\0 & 1\end{vmatrix}-(1)\begin{vmatrix}0 & 1\\0 & 1\end{vmatrix}+(0)\begin{vmatrix}0 & 1\\0 & 0\end{vmatrix}\\ &=4\\ &=4.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=\frac{1}{4}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \sin{\left(4 x + y \right)} \cos{\left(y + z \right)}\,dV &=\iiint_Δ \left(\sin{\left(u \right)} \cos{\left(v \right)}\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(\sin{\left(u \right)} \cos{\left(v \right)}\right)\left|\frac{1}{4}\right|\,du\,dv\,dw\\ &=\int_{\frac{3 \pi}{4}}^{\pi}\int_{0}^{\frac{\pi}{2}}\int_{-1}^{5}\left(\frac{\sin{\left(u \right)} \cos{\left(v \right)}}{4}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated variant / moderate / product

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): 1\le x y\le 2,\quad 1\le y\le 2,\quad 0\le z\le 1\}.
$$

Given the change of variables

$$
u=x y,\quad v=y,\quad w=4 z,
$$

Write the triple integral

$$
\iiint_R x y^{2} + y z\,dV
$$

as a repeated integral in terms of $u$, $v$, and $w$.

- $\int_{1}^{2}\int_{1}^{2}\int_{0}^{4}\left(\frac{u}{4 v} + \frac{w}{16}\right)\,dw\,dv\,du$
- $\int_{1}^{2}\int_{1}^{2}\int_{0}^{4}\left(\frac{v \left(4 u + w\right)}{4}\right)\,dw\,dv\,du$
- $\int_{1}^{2}\int_{1}^{2}\int_{0}^{4}\left(v^{2} \left(4 u + w\right)\right)\,dw\,dv\,du$
- $\int_{1}^{2}\int_{1}^{2}\int_{0}^{4}\left(\frac{u}{4} + \frac{w}{4}\right)\,dw\,dv\,du$
- $\int_{1}^{2}\int_{1}^{2}\int_{0}^{4}\left(\frac{u}{4} + \frac{w}{16}\right)\,dw\,dv\,du$ **correct**

Let's define a transformation $T$ as follows:

$$
T:(u,v,w)\longmapsto (x(u,v,w),y(u,v,w),z(u,v,w)).
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To find the required integral, we can use the change of variables formula

$$
\iiint_R f(x,y,z)\,dV=\iiint_Δ f(x(u,v,w),y(u,v,w),z(u,v,w))\left|\frac{\partial(x,y,z)}{\partial(u,v,w)}\right|\,du\,dv\,dw
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x y,\quad v=y,\quad w=4 z
$$

gives us the *inverse* function ${T}^{-1}$.

$$
T^{-1}:(x,y,z)\longmapsto (u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
Δ=\{(u,v,w): 1\le u\le 2,\quad 1\le v\le 2,\quad 0\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}y & x & 0\\0 & 1 & 0\\0 & 0 & 4\end{vmatrix}\\ &=(y)\begin{vmatrix}1 & 0\\0 & 4\end{vmatrix}-(x)\begin{vmatrix}0 & 0\\0 & 4\end{vmatrix}+(0)\begin{vmatrix}0 & 1\\0 & 0\end{vmatrix}\\ &=4 y\\ &=4 v.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=\frac{1}{4 v}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$ The sign of $v$ is fixed throughout $Δ$.

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R x y^{2} + y z\,dV &=\iiint_Δ \left(\frac{v \left(4 u + w\right)}{4}\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(\frac{v \left(4 u + w\right)}{4}\right)\left|\frac{1}{4 v}\right|\,du\,dv\,dw\\ &=\int_{1}^{2}\int_{1}^{2}\int_{0}^{4}\left(\frac{u}{4} + \frac{w}{16}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated variant / moderate / product

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): 1\le x y\le 2,\quad 1\le y\le 2,\quad 0\le z\le 3\}.
$$

Given the change of variables

$$
u=x y,\quad v=y,\quad w=3 z,
$$

Write the triple integral

$$
\iiint_R x y^{2} + 4 y z\,dV
$$

as a repeated integral in terms of $u$, $v$, and $w$.

- $\int_{1}^{2}\int_{1}^{2}\int_{0}^{9}\left(\frac{u}{3 v} + \frac{4 w}{9}\right)\,dw\,dv\,du$
- $\int_{1}^{2}\int_{1}^{2}\int_{0}^{9}\left(\frac{u}{3} + \frac{4 w}{3}\right)\,dw\,dv\,du$
- $\int_{1}^{2}\int_{1}^{2}\int_{0}^{9}\left(\frac{v \left(3 u + 4 w\right)}{3}\right)\,dw\,dv\,du$
- $\int_{1}^{2}\int_{1}^{2}\int_{0}^{9}\left(\frac{u}{3} + \frac{4 w}{9}\right)\,dw\,dv\,du$ **correct**
- $\int_{1}^{2}\int_{1}^{2}\int_{0}^{9}\left(v^{2} \left(3 u + 4 w\right)\right)\,dw\,dv\,du$

Let's define a transformation $T$ as follows:

$$
T:(u,v,w)\longmapsto (x(u,v,w),y(u,v,w),z(u,v,w)).
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To find the required integral, we can use the change of variables formula

$$
\iiint_R f(x,y,z)\,dV=\iiint_Δ f(x(u,v,w),y(u,v,w),z(u,v,w))\left|\frac{\partial(x,y,z)}{\partial(u,v,w)}\right|\,du\,dv\,dw
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x y,\quad v=y,\quad w=3 z
$$

gives us the *inverse* function ${T}^{-1}$.

$$
T^{-1}:(x,y,z)\longmapsto (u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
Δ=\{(u,v,w): 1\le u\le 2,\quad 1\le v\le 2,\quad 0\le w\le 9\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}y & x & 0\\0 & 1 & 0\\0 & 0 & 3\end{vmatrix}\\ &=(y)\begin{vmatrix}1 & 0\\0 & 3\end{vmatrix}-(x)\begin{vmatrix}0 & 0\\0 & 3\end{vmatrix}+(0)\begin{vmatrix}0 & 1\\0 & 0\end{vmatrix}\\ &=3 y\\ &=3 v.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=\frac{1}{3 v}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$ The sign of $v$ is fixed throughout $Δ$.

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R x y^{2} + 4 y z\,dV &=\iiint_Δ \left(\frac{v \left(3 u + 4 w\right)}{3}\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(\frac{v \left(3 u + 4 w\right)}{3}\right)\left|\frac{1}{3 v}\right|\,du\,dv\,dw\\ &=\int_{1}^{2}\int_{1}^{2}\int_{0}^{9}\left(\frac{u}{3} + \frac{4 w}{9}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated variant / moderate / sqrt

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): 1\le x + 3 y\le 2,\quad 1\le x - 3 y\le 2,\quad 1\le z\le \left(x - 3 y\right) \left(x + 3 y\right)\}.
$$

Given the change of variables

$$
u=x + 3 y,\quad v=x - 3 y,\quad w=\sqrt{z},
$$

Write the triple integral

$$
\iiint_R \sqrt{z}\,dV
$$

as a repeated integral in terms of $u$, $v$, and $w$.

- $\int_{1}^{2}\int_{1}^{2}\int_{1}^{\sqrt{u + v}}\left(\frac{w^{2}}{3}\right)\,dw\,dv\,du$
- $\int_{1}^{2}\int_{1}^{2}\int_{1}^{\sqrt{u v}}\left(w\right)\,dw\,dv\,du$
- $\int_{1}^{2}\int_{1}^{2}\int_{1}^{u v}\left(\frac{w^{2}}{3}\right)\,dw\,dv\,du$
- $\int_{1}^{2}\int_{1}^{2}\int_{1}^{\sqrt{u v}}\left(\frac{w}{6}\right)\,dw\,dv\,du$
- $\int_{1}^{2}\int_{1}^{2}\int_{1}^{\sqrt{u v}}\left(\frac{w^{2}}{3}\right)\,dw\,dv\,du$ **correct**

Let's define a transformation $T$ as follows:

$$
T:(u,v,w)\longmapsto (x(u,v,w),y(u,v,w),z(u,v,w)).
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To find the required integral, we can use the change of variables formula

$$
\iiint_R f(x,y,z)\,dV=\iiint_Δ f(x(u,v,w),y(u,v,w),z(u,v,w))\left|\frac{\partial(x,y,z)}{\partial(u,v,w)}\right|\,du\,dv\,dw
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x + 3 y,\quad v=x - 3 y,\quad w=\sqrt{z}
$$

gives us the *inverse* function ${T}^{-1}$.

$$
T^{-1}:(x,y,z)\longmapsto (u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
Δ=\{(u,v,w): 1\le u\le 2,\quad 1\le v\le 2,\quad 1\le w\le \sqrt{u v}\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}1 & 3 & 0\\1 & -3 & 0\\0 & 0 & \frac{1}{2 \sqrt{z}}\end{vmatrix}\\ &=(1)\begin{vmatrix}-3 & 0\\0 & \frac{1}{2 \sqrt{z}}\end{vmatrix}-(3)\begin{vmatrix}1 & 0\\0 & \frac{1}{2 \sqrt{z}}\end{vmatrix}+(0)\begin{vmatrix}1 & -3\\0 & 0\end{vmatrix}\\ &=- \frac{3}{\sqrt{z}}\\ &=- \frac{3}{w}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=- \frac{w}{3}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$ Since $z\ge1$ and $w=\sqrt z$, the branch is $w>0$.

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \sqrt{z}\,dV &=\iiint_Δ \left(w\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(w\right)\left|- \frac{w}{3}\right|\,du\,dv\,dw\\ &=\int_{1}^{2}\int_{1}^{2}\int_{1}^{\sqrt{u v}}\left(\frac{w^{2}}{3}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated variant / moderate / sqrt

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): 1\le x + 2 y\le 3,\quad 1\le x - 2 y\le 3,\quad 1\le z\le \left(x - 2 y\right) \left(x + 2 y\right)\}.
$$

Given the change of variables

$$
u=x + 2 y,\quad v=x - 2 y,\quad w=\sqrt{z},
$$

Write the triple integral

$$
\iiint_R \sqrt{z}\,dV
$$

as a repeated integral in terms of $u$, $v$, and $w$.

- $\int_{1}^{3}\int_{1}^{3}\int_{1}^{\sqrt{u + v}}\left(\frac{w^{2}}{2}\right)\,dw\,dv\,du$
- $\int_{1}^{3}\int_{1}^{3}\int_{1}^{\sqrt{u v}}\left(\frac{w}{4}\right)\,dw\,dv\,du$
- $\int_{1}^{3}\int_{1}^{3}\int_{1}^{\sqrt{u v}}\left(w\right)\,dw\,dv\,du$
- $\int_{1}^{3}\int_{1}^{3}\int_{1}^{\sqrt{u v}}\left(\frac{w^{2}}{2}\right)\,dw\,dv\,du$ **correct**
- $\int_{1}^{3}\int_{1}^{3}\int_{1}^{u v}\left(\frac{w^{2}}{2}\right)\,dw\,dv\,du$

Let's define a transformation $T$ as follows:

$$
T:(u,v,w)\longmapsto (x(u,v,w),y(u,v,w),z(u,v,w)).
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To find the required integral, we can use the change of variables formula

$$
\iiint_R f(x,y,z)\,dV=\iiint_Δ f(x(u,v,w),y(u,v,w),z(u,v,w))\left|\frac{\partial(x,y,z)}{\partial(u,v,w)}\right|\,du\,dv\,dw
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x + 2 y,\quad v=x - 2 y,\quad w=\sqrt{z}
$$

gives us the *inverse* function ${T}^{-1}$.

$$
T^{-1}:(x,y,z)\longmapsto (u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
Δ=\{(u,v,w): 1\le u\le 3,\quad 1\le v\le 3,\quad 1\le w\le \sqrt{u v}\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}1 & 2 & 0\\1 & -2 & 0\\0 & 0 & \frac{1}{2 \sqrt{z}}\end{vmatrix}\\ &=(1)\begin{vmatrix}-2 & 0\\0 & \frac{1}{2 \sqrt{z}}\end{vmatrix}-(2)\begin{vmatrix}1 & 0\\0 & \frac{1}{2 \sqrt{z}}\end{vmatrix}+(0)\begin{vmatrix}1 & -2\\0 & 0\end{vmatrix}\\ &=- \frac{2}{\sqrt{z}}\\ &=- \frac{2}{w}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=- \frac{w}{2}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$ Since $z\ge1$ and $w=\sqrt z$, the branch is $w>0$.

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \sqrt{z}\,dV &=\iiint_Δ \left(w\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(w\right)\left|- \frac{w}{2}\right|\,du\,dv\,dw\\ &=\int_{1}^{3}\int_{1}^{3}\int_{1}^{\sqrt{u v}}\left(\frac{w^{2}}{2}\right)\,dw\,dv\,du.\end{aligned}
$$