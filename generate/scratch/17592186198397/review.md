# Triple integral setup review

Raw evidence profiles retain source errors and are ineligible for learning. Generated method profiles contain supported repairs.

## Original public parameterized replay q-38941

Consider the finite region $R$ in the $xyz$-space, given by
$R = {(x, y, z): 1 \le x + y \le 2, 1 \le x - y \le 2, 1 \le z \le (x - y)(x + y)}$.
By performing the change of variables
$u = x + y, v = x - y, w = \sqrt{z}$,
the triple integral
$∭_(R)3\sqrt{z}dV$
can be written in terms of $u$, $v$, and $w$ as

- $\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{2}3 wdwdvdu$
- $\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{u v}3 w 2dwdvdu$
- $\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{2}3 w 2dwdvdu$
- $\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{u v}3 wdwdvdu$
- $\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{u + v}3 wdwdvdu$

*No source worked solution.*

---

## Raw changed-amplitude evidence only q-38941

Consider the finite region $R$ in the $xyz$-space, given by
$R = {(x, y, z): 1 \le x + y \le 2, 1 \le x - y \le 2, 1 \le z \le (x - y)(x + y)}$.
By performing the change of variables
$u = x + y, v = x - y, w = \sqrt{z}$,
the triple integral
$∭_(R)2\left(3\sqrt{z}\right)dV$
can be written in terms of $u$, $v$, and $w$ as

- $\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{u v}2\left(3 w 2\right)dwdvdu$
- $\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{2}2\left(3 w 2\right)dwdvdu$
- $\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{u v}2\left(3 w\right)dwdvdu$
- $\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{u + v}2\left(3 w\right)dwdvdu$
- $\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{2}\displaystyle \int_{1}^{2}2\left(3 w\right)dwdvdu$

*No source worked solution.*

---

## Original public parameterized replay q-39054

Consider the finite region $R$ in the $xyz$-space, given by
$R = {(x, y, z): \frac{3π}{4} \le 2x + y \le π, 0 \le y + z \le \frac{π}{2},-1 \le z \le 1}$.
Given the change of variables
$u = 2x + y, v = y + z, w = z$,
which of the following could be the missing part of the expression below?
$∭_(R)\sin (2x + y)\cos (y + z)dV = \displaystyle \int_{3π/4}^{π}\displaystyle \int_{0}^{π/2}\displaystyle \int_{-1}^{1}A A A A A Adwdvdu$

- $3\sin u\cos v$
- $\frac{1}{2}\sin u\cos v$
- $2\sin u\cos v$
- $\sin u\cos v$
- $\frac{1}{3}\sin u\cos v$

*No source worked solution.*

---

## Raw changed-amplitude evidence only q-39054

Consider the finite region $R$ in the $xyz$-space, given by
$R = {(x, y, z): \frac{3π}{4} \le 2x + y \le π, 0 \le y + z \le \frac{π}{2},-1 \le z \le 1}$.
Given the change of variables
$u = 2x + y, v = y + z, w = z$,
which of the following could be the missing part of the expression below?
$∭_(R)2\left(\sin (2x + y)\cos (y + z)\right)dV = \displaystyle \int_{3π/4}^{π}\displaystyle \int_{0}^{π/2}\displaystyle \int_{-1}^{1}A A A A A Adwdvdu$

- $2\left(\frac{1}{2}\sin u\cos v\right)$
- $2\left(2\sin u\cos v\right)$
- $2\left(\sin u\cos v\right)$
- $2\left(\frac{1}{3}\sin u\cos v\right)$
- $2\left(3\sin u\cos v\right)$

*No source worked solution.*

---

## Original public parameterized replay q-161880

Consider the finite region $R$ in the $xyz$-space, given by

$$
R={(x,y,z)\,:\,1\le x+y\le 2,\,0\le y-x\le 1,\,0\le z\le 3}.
$$

Given the change of variables

$$
u=x+y,\,v=y-x,\,w=z,
$$

which of the following could be the missing part of the expression below?

$$
{∭}_{R}2(x+y){e}^{y-x}\,dV={\int }_{1}^{2}{\int }_{0}^{1}{\int }_{0}^{3}\,dw\,dv\,du
$$

- $\frac{{e}^{v}}{2}$
- $\frac{v{e}^{u}}{2}$
- $u{e}^{v}$ **correct**
- $\frac{{e}^{u}}{2}$
- $2u{e}^{v}$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To find the required integral, we can use the change of variables formula

$$
{∭}_{R}f(x,y,z)\text{ }dV={∭}_{Δ}\text{ }f(x(u,v,w),y(u,v,w),z(u,v,w))\,|\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x+y,\,v=y-x,\,w=z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\begin{aligned}Δ & ={(u,v,w)\,:\,0\le u\le 1,\,0\le v\le 1,\,0\le w\le 3}.\end{aligned}
$$

   

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & 1 & 0 \\ -1 & 1 & 0 \\ 0 & 0 & 1\end{aligned}| \\  & =1|\begin{aligned}1 & 1 \\ -1 & 1\end{aligned}| \\  & =1(1+1) \\  & =2.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}=\frac{1}{2}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}{∭}_{R}2(x+y){e}^{y-x}\,dV & ={∭}_{Δ}2u{e}^{v}\cdot |\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w \\  & ={∭}_{Δ}2u{e}^{v}\cdot |\frac{1}{2}|\,\text{d}u\text{d}v\text{d}w \\  & ={\int }_{1}^{2}{\int }_{0}^{1}{\int }_{0}^{3}\,u{e}^{v}\,\,dw\,dv\,du\end{aligned}
$$

---

## Raw changed-amplitude evidence only q-161880

Consider the finite region $R$ in the $xyz$-space, given by

$$
R={(x,y,z)\,:\,1\le x+y\le 2,\,0\le y-x\le 1,\,0\le z\le 3}.
$$

Given the change of variables

$$
u=x+y,\,v=y-x,\,w=z,
$$

which of the following could be the missing part of the expression below?

$$
{∭}_{R}2\left(2(x+y){e}^{y-x}\right)\,dV={\int }_{1}^{2}{\int }_{0}^{1}{\int }_{0}^{3}\,dw\,dv\,du
$$

- $2\left(\frac{v{e}^{u}}{2}\right)$
- $2\left(u{e}^{v}\right)$ **correct**
- $2\left(\frac{{e}^{u}}{2}\right)$
- $2\left(2u{e}^{v}\right)$
- $2\left(\frac{{e}^{v}}{2}\right)$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To find the required integral, we can use the change of variables formula

$$
{∭}_{R}f(x,y,z)\text{ }dV={∭}_{Δ}\text{ }f(x(u,v,w),y(u,v,w),z(u,v,w))\,|\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x+y,\,v=y-x,\,w=z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\begin{aligned}Δ & ={(u,v,w)\,:\,0\le u\le 1,\,0\le v\le 1,\,0\le w\le 3}.\end{aligned}
$$

   

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & 1 & 0 \\ -1 & 1 & 0 \\ 0 & 0 & 1\end{aligned}| \\  & =1|\begin{aligned}1 & 1 \\ -1 & 1\end{aligned}| \\  & =1(1+1) \\  & =2.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}=\frac{1}{2}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}{∭}_{R}2\left(2(x+y){e}^{y-x}\right)\,dV & ={∭}_{Δ}2\left(2u{e}^{v}\right)\cdot |\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w \\  & ={∭}_{Δ}2\left(2u{e}^{v}\right)\cdot |\frac{1}{2}|\,\text{d}u\text{d}v\text{d}w \\  & ={\int }_{1}^{2}{\int }_{0}^{1}{\int }_{0}^{3}\,2\left(u{e}^{v}\right)\,\,dw\,dv\,du\end{aligned}
$$

---

## Original public parameterized replay q-39057

Consider the finite region $R$ in the $xyz$-space, given by 

$$
R={(x,y,z)\,:\,1\le {x}^{2}+y\le 2,\,-1\le x\le 1,\,1\le z\le 4}.
$$

 

Given the change of variables

$$
u={x}^{2}+y,\,v=2x+z,\,w=z,
$$

which of the following could be the missing part of the expression below?

$$
{∭}_{R}(2x+z)\operatorname{ln}⁡({x}^{2}+y)\,dV={\int }_{1}^{2}{\int }_{-1}^{6}{\int }_{1}^{4}\,dw\,dv\,du
$$

- $2u\operatorname{ln}⁡v$
- $u\operatorname{ln}⁡v$
- $\frac{1}{2}v\operatorname{ln}⁡u$ **correct**
- $\frac{1}{3}v\operatorname{ln}⁡u$
- $3v\operatorname{ln}⁡u$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To find the required integral, we can use the change of variables formula

$$
{∭}_{R}f(x,y,z)\text{ }dV={∭}_{Δ}\text{ }f(x(u,v,w),y(u,v,w),z(u,v,w))\,|\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$ 

Note that the change of variables

$$
u={x}^{2}+y,\,v=2x+z,\,w=z,
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\begin{aligned}Δ & ={(u,v,w)\,:\,1\le u\le 2,\,-1\le v\le 6,\,1\le w\le 4}.\end{aligned}
$$

 

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$ 

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2x & 1 & 0 \\ 2 & 0 & 1 \\ 0 & 0 & 1\end{aligned}| \\  & =-|\begin{aligned}2 & 1 \\ 0 & 1\end{aligned}| \\  & =-(2-0) \\  & =-2.\end{aligned}
$$

 

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}=-\frac{1}{2}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}{∭}_{R}(2x+z)\operatorname{ln}⁡({x}^{2}+y)\,dV & ={∭}_{Δ}\operatorname{sin}⁡u\operatorname{cos}⁡v\cdot |\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w \\  & ={∭}_{Δ}v\operatorname{ln}⁡u\cdot |-\frac{1}{2}|\,\text{d}u\text{d}v\text{d}w \\  & ={\int }_{1}^{2}{\int }_{-1}^{6}{\int }_{1}^{4}\,\frac{1}{2}v\operatorname{ln}⁡u\,\,dw\,dv\,du\end{aligned}
$$

---

## Raw changed-amplitude evidence only q-39057

Consider the finite region $R$ in the $xyz$-space, given by 

$$
R={(x,y,z)\,:\,1\le {x}^{2}+y\le 2,\,-1\le x\le 1,\,1\le z\le 4}.
$$

 

Given the change of variables

$$
u={x}^{2}+y,\,v=2x+z,\,w=z,
$$

which of the following could be the missing part of the expression below?

$$
{∭}_{R}2\left((2x+z)\operatorname{ln}⁡({x}^{2}+y)\right)\,dV={\int }_{1}^{2}{\int }_{-1}^{6}{\int }_{1}^{4}\,dw\,dv\,du
$$

- $2\left(u\operatorname{ln}⁡v\right)$
- $2\left(\frac{1}{2}v\operatorname{ln}⁡u\right)$ **correct**
- $2\left(\frac{1}{3}v\operatorname{ln}⁡u\right)$
- $2\left(3v\operatorname{ln}⁡u\right)$
- $2\left(2u\operatorname{ln}⁡v\right)$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To find the required integral, we can use the change of variables formula

$$
{∭}_{R}f(x,y,z)\text{ }dV={∭}_{Δ}\text{ }f(x(u,v,w),y(u,v,w),z(u,v,w))\,|\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$ 

Note that the change of variables

$$
u={x}^{2}+y,\,v=2x+z,\,w=z,
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\begin{aligned}Δ & ={(u,v,w)\,:\,1\le u\le 2,\,-1\le v\le 6,\,1\le w\le 4}.\end{aligned}
$$

 

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$ 

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2x & 1 & 0 \\ 2 & 0 & 1 \\ 0 & 0 & 1\end{aligned}| \\  & =-|\begin{aligned}2 & 1 \\ 0 & 1\end{aligned}| \\  & =-(2-0) \\  & =-2.\end{aligned}
$$

 

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}=-\frac{1}{2}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}{∭}_{R}2\left((2x+z)\operatorname{ln}⁡({x}^{2}+y)\right)\,dV & ={∭}_{Δ}2\left(\operatorname{sin}⁡u\operatorname{cos}⁡v\right)\cdot |\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w \\  & ={∭}_{Δ}2\left(v\operatorname{ln}⁡u\right)\cdot |-\frac{1}{2}|\,\text{d}u\text{d}v\text{d}w \\  & ={\int }_{1}^{2}{\int }_{-1}^{6}{\int }_{1}^{4}\,2\left(\frac{1}{2}v\operatorname{ln}⁡u\right)\,\,dw\,dv\,du\end{aligned}
$$

---

## Original public parameterized replay q-161879

Consider the finite region $R$ in the $xyz$-space, given by

$$
R={(x,y,z)\,:\,0\le x+3y\le \frac{\pi }{2},\,0\le z-3y\le \frac{\pi }{2},\,0\le z\le 2}.
$$

Given the change of variables

$$
u=x+3y,\,v=z-3y,\,w=z,
$$

which of the following could be the missing part of the expression below?

$$
{∭}_{R}{cos}^{2}⁡(x+z)\operatorname{cos}⁡(z-3y)\,dV={\int }_{0}^{\pi /2}{\int }_{0}^{\pi /2}{\int }_{0}^{2}\,dw\,dv\,du
$$

- $\frac{1}{3}{cos}^{2}⁡(u)\operatorname{cos}⁡v$
- $\frac{1}{2}{cos}^{2}⁡(u-v)\operatorname{cos}⁡v$
- $\frac{1}{2}{cos}^{2}⁡v\operatorname{cos}⁡v$
- $\frac{1}{3}{cos}^{2}⁡(u+v)\operatorname{cos}⁡v$ **correct**
- $\frac{1}{4}{cos}^{2}⁡(uv)\operatorname{cos}⁡v-u$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To find the required integral, we can use the change of variables formula

$$
{∭}_{R}f(x,y,z)\text{ }dV={∭}_{Δ}\text{ }f(x(u,v,w),y(u,v,w),z(u,v,w))\,|\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x+3y,\,v=z-3y,\,w=z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\begin{aligned}Δ & ={(x,y,z)\,:\,0\le u\le \frac{\pi }{2},\,0\le v\le \frac{\pi }{2},\,0\le w\le 2}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & 3 & 0 \\ 0 & -3 & 1 \\ 0 & 0 & 1\end{aligned}| \\  & =1|\begin{aligned}-3 & 1 \\ 0 & 1\end{aligned}| \\  & =1(-3-0) \\  & =-3.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}=-\frac{1}{3}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}{∭}_{R}{cos}^{2}⁡(x+z)\operatorname{cos}⁡(z-3y)\,dV & ={∭}_{Δ}{cos}^{2}⁡(u+v)\operatorname{cos}⁡v\cdot |\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w \\  & ={∭}_{Δ}{cos}^{2}⁡(u+v)\operatorname{cos}⁡v\cdot |-\frac{1}{3}|\,\text{d}u\text{d}v\text{d}w \\  & ={\int }_{0}^{\pi /2}{\int }_{0}^{\pi /2}{\int }_{0}^{2}\,\frac{1}{3}{cos}^{2}⁡(u+v)\operatorname{cos}⁡v\,\,dw\,dv\,du\end{aligned}
$$

---

## Raw changed-amplitude evidence only q-161879

Consider the finite region $R$ in the $xyz$-space, given by

$$
R={(x,y,z)\,:\,0\le x+3y\le \frac{\pi }{2},\,0\le z-3y\le \frac{\pi }{2},\,0\le z\le 2}.
$$

Given the change of variables

$$
u=x+3y,\,v=z-3y,\,w=z,
$$

which of the following could be the missing part of the expression below?

$$
{∭}_{R}2\left({cos}^{2}⁡(x+z)\operatorname{cos}⁡(z-3y)\right)\,dV={\int }_{0}^{\pi /2}{\int }_{0}^{\pi /2}{\int }_{0}^{2}\,dw\,dv\,du
$$

- $2\left(\frac{1}{2}{cos}^{2}⁡(u-v)\operatorname{cos}⁡v\right)$
- $2\left(\frac{1}{2}{cos}^{2}⁡v\operatorname{cos}⁡v\right)$
- $2\left(\frac{1}{3}{cos}^{2}⁡(u+v)\operatorname{cos}⁡v\right)$ **correct**
- $2\left(\frac{1}{4}{cos}^{2}⁡(uv)\operatorname{cos}⁡v-u\right)$
- $2\left(\frac{1}{3}{cos}^{2}⁡(u)\operatorname{cos}⁡v\right)$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.

To find the required integral, we can use the change of variables formula

$$
{∭}_{R}f(x,y,z)\text{ }dV={∭}_{Δ}\text{ }f(x(u,v,w),y(u,v,w),z(u,v,w))\,|\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w
$$

where $\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x+3y,\,v=z-3y,\,w=z
$$

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\begin{aligned}Δ & ={(x,y,z)\,:\,0\le u\le \frac{\pi }{2},\,0\le v\le \frac{\pi }{2},\,0\le w\le 2}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & 3 & 0 \\ 0 & -3 & 1 \\ 0 & 0 & 1\end{aligned}| \\  & =1|\begin{aligned}-3 & 1 \\ 0 & 1\end{aligned}| \\  & =1(-3-0) \\  & =-3.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}=-\frac{1}{3}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}{∭}_{R}2\left({cos}^{2}⁡(x+z)\operatorname{cos}⁡(z-3y)\right)\,dV & ={∭}_{Δ}2\left({cos}^{2}⁡(u+v)\operatorname{cos}⁡v\right)\cdot |\frac{∂(x,y,z)}{∂(u,v,w)}|\,\text{d}u\text{d}v\text{d}w \\  & ={∭}_{Δ}2\left({cos}^{2}⁡(u+v)\operatorname{cos}⁡v\right)\cdot |-\frac{1}{3}|\,\text{d}u\text{d}v\text{d}w \\  & ={\int }_{0}^{\pi /2}{\int }_{0}^{\pi /2}{\int }_{0}^{2}\,2\left(\frac{1}{3}{cos}^{2}⁡(u+v)\operatorname{cos}⁡v\right)\,\,dw\,dv\,du\end{aligned}
$$

---

## Generated easy exp

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): 1\le x + 5 y\le 2,\quad 0\le - x + y\le 1,\quad 0\le z\le 2\}.
$$

Given the change of variables

$$
u=x + 5 y,\quad v=- x + y,\quad w=z,
$$

Which of the following could be the missing part of the expression below?

$$
\iiint_R \left(4 x + 20 y\right) e^{- x + y}\,dV=\int_{1}^{2}\int_{0}^{1}\int_{0}^{2}\left(\boxed{?}\right)\,dw\,dv\,du
$$

- $\frac{2 v e^{u}}{3}$
- $4 u e^{v}$
- $\frac{2 u e^{v}}{3}$ **correct**
- $\frac{2 e^{u}}{3}$
- $\frac{2 e^{v}}{3}$

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
u=x + 5 y,\quad v=- x + y,\quad w=z
$$

gives us the *inverse* function ${T}^{-1}$.

$$
T^{-1}:(x,y,z)\longmapsto (u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
Δ=\{(u,v,w): 1\le u\le 2,\quad 0\le v\le 1,\quad 0\le w\le 2\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}1 & 5 & 0\\-1 & 1 & 0\\0 & 0 & 1\end{vmatrix}\\ &=(1)\begin{vmatrix}1 & 0\\0 & 1\end{vmatrix}-(5)\begin{vmatrix}-1 & 0\\0 & 1\end{vmatrix}+(0)\begin{vmatrix}-1 & 1\\0 & 0\end{vmatrix}\\ &=6\\ &=6.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=\frac{1}{6}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(4 x + 20 y\right) e^{- x + y}\,dV &=\iiint_Δ \left(4 u e^{v}\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(4 u e^{v}\right)\left|\frac{1}{6}\right|\,du\,dv\,dw\\ &=\int_{1}^{2}\int_{0}^{1}\int_{0}^{2}\left(\frac{2 u e^{v}}{3}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated easy exp

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): 1\le x + 3 y\le 2,\quad 0\le - x + y\le 1,\quad 0\le z\le 4\}.
$$

Given the change of variables

$$
u=x + 3 y,\quad v=- x + y,\quad w=z,
$$

Which of the following could be the missing part of the expression below?

$$
\iiint_R \left(x + 3 y\right) e^{- x + y}\,dV=\int_{1}^{2}\int_{0}^{1}\int_{0}^{4}\left(\boxed{?}\right)\,dw\,dv\,du
$$

- $\frac{v e^{u}}{4}$
- $\frac{e^{v}}{4}$
- $\frac{e^{u}}{4}$
- $\frac{u e^{v}}{4}$ **correct**
- $u e^{v}$

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
u=x + 3 y,\quad v=- x + y,\quad w=z
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
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}1 & 3 & 0\\-1 & 1 & 0\\0 & 0 & 1\end{vmatrix}\\ &=(1)\begin{vmatrix}1 & 0\\0 & 1\end{vmatrix}-(3)\begin{vmatrix}-1 & 0\\0 & 1\end{vmatrix}+(0)\begin{vmatrix}-1 & 1\\0 & 0\end{vmatrix}\\ &=4\\ &=4.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=\frac{1}{4}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(x + 3 y\right) e^{- x + y}\,dV &=\iiint_Δ \left(u e^{v}\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(u e^{v}\right)\left|\frac{1}{4}\right|\,du\,dv\,dw\\ &=\int_{1}^{2}\int_{0}^{1}\int_{0}^{4}\left(\frac{u e^{v}}{4}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated easy log

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): 1\le x^{2} + y\le 2,\quad -1\le 5 x + z\le 9,\quad 1\le z\le 2\}.
$$

Given the change of variables

$$
u=x^{2} + y,\quad v=5 x + z,\quad w=z,
$$

Which of the following could be the missing part of the expression below?

$$
\iiint_R \left(20 x + 4 z\right) \ln{\left(x^{2} + y \right)}\,dV=\int_{1}^{2}\int_{-1}^{9}\int_{1}^{2}\left(\boxed{?}\right)\,dw\,dv\,du
$$

- $20 v \ln{\left(u \right)}$
- $4 v \ln{\left(u \right)}$
- $\frac{4 v \ln{\left(u \right)}}{5}$ **correct**
- $- \frac{4 v \ln{\left(u \right)}}{5}$
- $\frac{4 u \ln{\left(u \right)}}{5}$

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
u=x^{2} + y,\quad v=5 x + z,\quad w=z
$$

gives us the *inverse* function ${T}^{-1}$.

$$
T^{-1}:(x,y,z)\longmapsto (u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
Δ=\{(u,v,w): 1\le u\le 2,\quad -1\le v\le 9,\quad 1\le w\le 2\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}2 x & 1 & 0\\5 & 0 & 1\\0 & 0 & 1\end{vmatrix}\\ &=(2 x)\begin{vmatrix}0 & 1\\0 & 1\end{vmatrix}-(1)\begin{vmatrix}5 & 1\\0 & 1\end{vmatrix}+(0)\begin{vmatrix}5 & 0\\0 & 0\end{vmatrix}\\ &=-5\\ &=-5.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=- \frac{1}{5}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(20 x + 4 z\right) \ln{\left(x^{2} + y \right)}\,dV &=\iiint_Δ \left(4 v \ln{\left(u \right)}\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(4 v \ln{\left(u \right)}\right)\left|- \frac{1}{5}\right|\,du\,dv\,dw\\ &=\int_{1}^{2}\int_{-1}^{9}\int_{1}^{2}\left(\frac{4 v \ln{\left(u \right)}}{5}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated easy log

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): 1\le x^{2} + y\le 2,\quad -1\le 3 x + z\le 7,\quad 1\le z\le 4\}.
$$

Given the change of variables

$$
u=x^{2} + y,\quad v=3 x + z,\quad w=z,
$$

Which of the following could be the missing part of the expression below?

$$
\iiint_R \left(3 x + z\right) \ln{\left(x^{2} + y \right)}\,dV=\int_{1}^{2}\int_{-1}^{7}\int_{1}^{4}\left(\boxed{?}\right)\,dw\,dv\,du
$$

- $3 v \ln{\left(u \right)}$
- $\frac{u \ln{\left(u \right)}}{3}$
- $- \frac{v \ln{\left(u \right)}}{3}$
- $\frac{v \ln{\left(u \right)}}{3}$ **correct**
- $v \ln{\left(u \right)}$

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
u=x^{2} + y,\quad v=3 x + z,\quad w=z
$$

gives us the *inverse* function ${T}^{-1}$.

$$
T^{-1}:(x,y,z)\longmapsto (u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
Δ=\{(u,v,w): 1\le u\le 2,\quad -1\le v\le 7,\quad 1\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}2 x & 1 & 0\\3 & 0 & 1\\0 & 0 & 1\end{vmatrix}\\ &=(2 x)\begin{vmatrix}0 & 1\\0 & 1\end{vmatrix}-(1)\begin{vmatrix}3 & 1\\0 & 1\end{vmatrix}+(0)\begin{vmatrix}3 & 0\\0 & 0\end{vmatrix}\\ &=-3\\ &=-3.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=- \frac{1}{3}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \left(3 x + z\right) \ln{\left(x^{2} + y \right)}\,dV &=\iiint_Δ \left(v \ln{\left(u \right)}\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(v \ln{\left(u \right)}\right)\left|- \frac{1}{3}\right|\,du\,dv\,dw\\ &=\int_{1}^{2}\int_{-1}^{7}\int_{1}^{4}\left(\frac{v \ln{\left(u \right)}}{3}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated easy cos2

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): 0\le x + 5 y\le \frac{\pi}{2},\quad 0\le - 5 y + z\le \frac{\pi}{2},\quad 0\le z\le 2\}.
$$

Given the change of variables

$$
u=x + 5 y,\quad v=- 5 y + z,\quad w=z,
$$

Which of the following could be the missing part of the expression below?

$$
\iiint_R 4 \cos^{2}{\left(x + z \right)} \cos{\left(5 y - z \right)}\,dV=\int_{0}^{\frac{\pi}{2}}\int_{0}^{\frac{\pi}{2}}\int_{0}^{2}\left(\boxed{?}\right)\,dw\,dv\,du
$$

- $20 \cos{\left(v \right)} \cos^{2}{\left(u + v \right)}$
- $4 \cos{\left(v \right)} \cos^{2}{\left(u + v \right)}$
- $\frac{4 \cos{\left(v \right)} \cos^{2}{\left(u + v \right)}}{5}$ **correct**
- $\frac{4 \cos^{2}{\left(u \right)} \cos{\left(v \right)}}{5}$
- $\frac{4 \cos{\left(v \right)} \cos^{2}{\left(u - v \right)}}{5}$

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
u=x + 5 y,\quad v=- 5 y + z,\quad w=z
$$

gives us the *inverse* function ${T}^{-1}$.

$$
T^{-1}:(x,y,z)\longmapsto (u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
Δ=\{(u,v,w): 0\le u\le \frac{\pi}{2},\quad 0\le v\le \frac{\pi}{2},\quad 0\le w\le 2\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}1 & 5 & 0\\0 & -5 & 1\\0 & 0 & 1\end{vmatrix}\\ &=(1)\begin{vmatrix}-5 & 1\\0 & 1\end{vmatrix}-(5)\begin{vmatrix}0 & 1\\0 & 1\end{vmatrix}+(0)\begin{vmatrix}0 & -5\\0 & 0\end{vmatrix}\\ &=-5\\ &=-5.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=- \frac{1}{5}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R 4 \cos^{2}{\left(x + z \right)} \cos{\left(5 y - z \right)}\,dV &=\iiint_Δ \left(4 \cos{\left(v \right)} \cos^{2}{\left(u + v \right)}\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(4 \cos{\left(v \right)} \cos^{2}{\left(u + v \right)}\right)\left|- \frac{1}{5}\right|\,du\,dv\,dw\\ &=\int_{0}^{\frac{\pi}{2}}\int_{0}^{\frac{\pi}{2}}\int_{0}^{2}\left(\frac{4 \cos{\left(v \right)} \cos^{2}{\left(u + v \right)}}{5}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated easy cos2

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): 0\le x + 3 y\le \frac{\pi}{2},\quad 0\le - 3 y + z\le \frac{\pi}{2},\quad 0\le z\le 4\}.
$$

Given the change of variables

$$
u=x + 3 y,\quad v=- 3 y + z,\quad w=z,
$$

Which of the following could be the missing part of the expression below?

$$
\iiint_R \cos^{2}{\left(x + z \right)} \cos{\left(3 y - z \right)}\,dV=\int_{0}^{\frac{\pi}{2}}\int_{0}^{\frac{\pi}{2}}\int_{0}^{4}\left(\boxed{?}\right)\,dw\,dv\,du
$$

- $3 \cos{\left(v \right)} \cos^{2}{\left(u + v \right)}$
- $\frac{\cos{\left(v \right)} \cos^{2}{\left(u - v \right)}}{3}$
- $\frac{\cos^{2}{\left(u \right)} \cos{\left(v \right)}}{3}$
- $\frac{\cos{\left(v \right)} \cos^{2}{\left(u + v \right)}}{3}$ **correct**
- $\cos{\left(v \right)} \cos^{2}{\left(u + v \right)}$

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
u=x + 3 y,\quad v=- 3 y + z,\quad w=z
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
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}1 & 3 & 0\\0 & -3 & 1\\0 & 0 & 1\end{vmatrix}\\ &=(1)\begin{vmatrix}-3 & 1\\0 & 1\end{vmatrix}-(3)\begin{vmatrix}0 & 1\\0 & 1\end{vmatrix}+(0)\begin{vmatrix}0 & -3\\0 & 0\end{vmatrix}\\ &=-3\\ &=-3.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=- \frac{1}{3}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \cos^{2}{\left(x + z \right)} \cos{\left(3 y - z \right)}\,dV &=\iiint_Δ \left(\cos{\left(v \right)} \cos^{2}{\left(u + v \right)}\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(\cos{\left(v \right)} \cos^{2}{\left(u + v \right)}\right)\left|- \frac{1}{3}\right|\,du\,dv\,dw\\ &=\int_{0}^{\frac{\pi}{2}}\int_{0}^{\frac{\pi}{2}}\int_{0}^{4}\left(\frac{\cos{\left(v \right)} \cos^{2}{\left(u + v \right)}}{3}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated easy sin

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): \frac{3 \pi}{4}\le 5 x + y\le \pi,\quad 0\le y + z\le \frac{\pi}{2},\quad -1\le z\le 2\}.
$$

Given the change of variables

$$
u=5 x + y,\quad v=y + z,\quad w=z,
$$

Which of the following could be the missing part of the expression below?

$$
\iiint_R 4 \sin{\left(5 x + y \right)} \cos{\left(y + z \right)}\,dV=\int_{\frac{3 \pi}{4}}^{\pi}\int_{0}^{\frac{\pi}{2}}\int_{-1}^{2}\left(\boxed{?}\right)\,dw\,dv\,du
$$

- $20 \sin{\left(u \right)} \cos{\left(v \right)}$
- $4 \sin{\left(u \right)} \cos{\left(v \right)}$
- $\frac{4 \sin{\left(u \right)} \cos{\left(v \right)}}{5}$ **correct**
- $\frac{4 \sin{\left(u \right)} \sin{\left(v \right)}}{5}$
- $\frac{4 \sin{\left(v \right)} \cos{\left(u \right)}}{5}$

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
u=5 x + y,\quad v=y + z,\quad w=z
$$

gives us the *inverse* function ${T}^{-1}$.

$$
T^{-1}:(x,y,z)\longmapsto (u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
Δ=\{(u,v,w): \frac{3 \pi}{4}\le u\le \pi,\quad 0\le v\le \frac{\pi}{2},\quad -1\le w\le 2\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}5 & 1 & 0\\0 & 1 & 1\\0 & 0 & 1\end{vmatrix}\\ &=(5)\begin{vmatrix}1 & 1\\0 & 1\end{vmatrix}-(1)\begin{vmatrix}0 & 1\\0 & 1\end{vmatrix}+(0)\begin{vmatrix}0 & 1\\0 & 0\end{vmatrix}\\ &=5\\ &=5.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=\frac{1}{5}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R 4 \sin{\left(5 x + y \right)} \cos{\left(y + z \right)}\,dV &=\iiint_Δ \left(4 \sin{\left(u \right)} \cos{\left(v \right)}\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(4 \sin{\left(u \right)} \cos{\left(v \right)}\right)\left|\frac{1}{5}\right|\,du\,dv\,dw\\ &=\int_{\frac{3 \pi}{4}}^{\pi}\int_{0}^{\frac{\pi}{2}}\int_{-1}^{2}\left(\frac{4 \sin{\left(u \right)} \cos{\left(v \right)}}{5}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated easy sin

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): \frac{3 \pi}{4}\le 3 x + y\le \pi,\quad 0\le y + z\le \frac{\pi}{2},\quad -1\le z\le 4\}.
$$

Given the change of variables

$$
u=3 x + y,\quad v=y + z,\quad w=z,
$$

Which of the following could be the missing part of the expression below?

$$
\iiint_R \sin{\left(3 x + y \right)} \cos{\left(y + z \right)}\,dV=\int_{\frac{3 \pi}{4}}^{\pi}\int_{0}^{\frac{\pi}{2}}\int_{-1}^{4}\left(\boxed{?}\right)\,dw\,dv\,du
$$

- $3 \sin{\left(u \right)} \cos{\left(v \right)}$
- $\frac{\sin{\left(v \right)} \cos{\left(u \right)}}{3}$
- $\frac{\sin{\left(u \right)} \sin{\left(v \right)}}{3}$
- $\frac{\sin{\left(u \right)} \cos{\left(v \right)}}{3}$ **correct**
- $\sin{\left(u \right)} \cos{\left(v \right)}$

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
u=3 x + y,\quad v=y + z,\quad w=z
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
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}3 & 1 & 0\\0 & 1 & 1\\0 & 0 & 1\end{vmatrix}\\ &=(3)\begin{vmatrix}1 & 1\\0 & 1\end{vmatrix}-(1)\begin{vmatrix}0 & 1\\0 & 1\end{vmatrix}+(0)\begin{vmatrix}0 & 1\\0 & 0\end{vmatrix}\\ &=3\\ &=3.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=\frac{1}{3}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \sin{\left(3 x + y \right)} \cos{\left(y + z \right)}\,dV &=\iiint_Δ \left(\sin{\left(u \right)} \cos{\left(v \right)}\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(\sin{\left(u \right)} \cos{\left(v \right)}\right)\left|\frac{1}{3}\right|\,du\,dv\,dw\\ &=\int_{\frac{3 \pi}{4}}^{\pi}\int_{0}^{\frac{\pi}{2}}\int_{-1}^{4}\left(\frac{\sin{\left(u \right)} \cos{\left(v \right)}}{3}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated moderate product

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
\iiint_R 4 x y^{2} + y z\,dV
$$

as a repeated integral in terms of $u$, $v$, and $w$.

- $\int_{1}^{2}\int_{1}^{2}\int_{0}^{9}\left(v^{2} \left(12 u + w\right)\right)\,dw\,dv\,du$
- $\int_{1}^{2}\int_{1}^{2}\int_{0}^{9}\left(\frac{v \left(12 u + w\right)}{3}\right)\,dw\,dv\,du$
- $\int_{1}^{2}\int_{1}^{2}\int_{0}^{9}\left(\frac{4 u}{3} + \frac{w}{9}\right)\,dw\,dv\,du$ **correct**
- $\int_{1}^{2}\int_{1}^{2}\int_{0}^{9}\left(\frac{4 u}{3} + \frac{w}{3}\right)\,dw\,dv\,du$
- $\int_{1}^{2}\int_{1}^{2}\int_{0}^{9}\left(\frac{12 u + v w}{9 v}\right)\,dw\,dv\,du$

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
\begin{aligned}\iiint_R 4 x y^{2} + y z\,dV &=\iiint_Δ \left(\frac{v \left(12 u + w\right)}{3}\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(\frac{v \left(12 u + w\right)}{3}\right)\left|\frac{1}{3 v}\right|\,du\,dv\,dw\\ &=\int_{1}^{2}\int_{1}^{2}\int_{0}^{9}\left(\frac{4 u}{3} + \frac{w}{9}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated moderate product

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): 1\le x y\le 2,\quad -2\le y\le -1,\quad 0\le z\le 2\}.
$$

Given the change of variables

$$
u=x y,\quad v=y,\quad w=2 z,
$$

Write the triple integral

$$
\iiint_R x y^{2} + 3 y z\,dV
$$

as a repeated integral in terms of $u$, $v$, and $w$.

- $\int_{1}^{2}\int_{-2}^{-1}\int_{0}^{4}\left(v^{2} \left(- 2 u - 3 w\right)\right)\,dw\,dv\,du$
- $\int_{1}^{2}\int_{-2}^{-1}\int_{0}^{4}\left(- \frac{u}{2 v} - \frac{3 w}{4}\right)\,dw\,dv\,du$
- $\int_{1}^{2}\int_{-2}^{-1}\int_{0}^{4}\left(- \frac{u}{2} - \frac{3 w}{2}\right)\,dw\,dv\,du$
- $\int_{1}^{2}\int_{-2}^{-1}\int_{0}^{4}\left(- \frac{u}{2} - \frac{3 w}{4}\right)\,dw\,dv\,du$ **correct**
- $\int_{1}^{2}\int_{-2}^{-1}\int_{0}^{4}\left(\frac{v \left(2 u + 3 w\right)}{2}\right)\,dw\,dv\,du$

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
u=x y,\quad v=y,\quad w=2 z
$$

gives us the *inverse* function ${T}^{-1}$.

$$
T^{-1}:(x,y,z)\longmapsto (u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To find the required integral, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
Δ=\{(u,v,w): 1\le u\le 2,\quad -2\le v\le -1,\quad 0\le w\le 4\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}y & x & 0\\0 & 1 & 0\\0 & 0 & 2\end{vmatrix}\\ &=(y)\begin{vmatrix}1 & 0\\0 & 2\end{vmatrix}-(x)\begin{vmatrix}0 & 0\\0 & 2\end{vmatrix}+(0)\begin{vmatrix}0 & 1\\0 & 0\end{vmatrix}\\ &=2 y\\ &=2 v.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=\frac{1}{2 v}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$ The sign of $v$ is fixed throughout $Δ$.

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R x y^{2} + 3 y z\,dV &=\iiint_Δ \left(\frac{v \left(2 u + 3 w\right)}{2}\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(\frac{v \left(2 u + 3 w\right)}{2}\right)\left|\frac{1}{2 v}\right|\,du\,dv\,dw\\ &=\int_{1}^{2}\int_{-2}^{-1}\int_{0}^{4}\left(- \frac{u}{2} - \frac{3 w}{4}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated hard sqrt

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): 1\le x + 2 y\le 2,\quad 1\le x - 2 y\le 2,\quad 1\le z\le \left(x - 2 y\right) \left(x + 2 y\right)\}.
$$

Given the change of variables

$$
u=x + 2 y,\quad v=x - 2 y,\quad w=\sqrt{z},
$$

Write the triple integral

$$
\iiint_R 4 \sqrt{z}\,dV
$$

as a repeated integral in terms of $u$, $v$, and $w$.

- $\int_{1}^{2}\int_{1}^{2}\int_{1}^{u v}\left(2 w^{2}\right)\,dw\,dv\,du$
- $\int_{1}^{2}\int_{1}^{2}\int_{1}^{\sqrt{u v}}\left(4 w\right)\,dw\,dv\,du$
- $\int_{1}^{2}\int_{1}^{2}\int_{1}^{\sqrt{u v}}\left(2 w^{2}\right)\,dw\,dv\,du$ **correct**
- $\int_{1}^{2}\int_{1}^{2}\int_{1}^{\sqrt{u v}}\left(w\right)\,dw\,dv\,du$
- $\int_{1}^{2}\int_{1}^{2}\int_{1}^{\sqrt{u + v}}\left(2 w^{2}\right)\,dw\,dv\,du$

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
Δ=\{(u,v,w): 1\le u\le 2,\quad 1\le v\le 2,\quad 1\le w\le \sqrt{u v}\}.
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
\begin{aligned}\iiint_R 4 \sqrt{z}\,dV &=\iiint_Δ \left(4 w\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(4 w\right)\left|- \frac{w}{2}\right|\,du\,dv\,dw\\ &=\int_{1}^{2}\int_{1}^{2}\int_{1}^{\sqrt{u v}}\left(2 w^{2}\right)\,dw\,dv\,du.\end{aligned}
$$

---

## Generated hard sqrt

Consider the finite region $R$ in the $xyz$-space, given by

$$
R=\{(x,y,z): 1\le x + y\le 3,\quad 1\le x - y\le 3,\quad 1\le z\le \left(x - y\right) \left(x + y\right)\}.
$$

Given the change of variables

$$
u=x + y,\quad v=x - y,\quad w=\sqrt{z},
$$

Write the triple integral

$$
\iiint_R \sqrt{z}\,dV
$$

as a repeated integral in terms of $u$, $v$, and $w$.

- $\int_{1}^{3}\int_{1}^{3}\int_{1}^{u v}\left(w^{2}\right)\,dw\,dv\,du$
- $\int_{1}^{3}\int_{1}^{3}\int_{1}^{\sqrt{u + v}}\left(w^{2}\right)\,dw\,dv\,du$
- $\int_{1}^{3}\int_{1}^{3}\int_{1}^{\sqrt{u v}}\left(\frac{w}{2}\right)\,dw\,dv\,du$
- $\int_{1}^{3}\int_{1}^{3}\int_{1}^{\sqrt{u v}}\left(w^{2}\right)\,dw\,dv\,du$ **correct**
- $\int_{1}^{3}\int_{1}^{3}\int_{1}^{\sqrt{u v}}\left(w\right)\,dw\,dv\,du$

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
u=x + y,\quad v=x - y,\quad w=\sqrt{z}
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
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &=\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z}\\\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z}\\\frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix}\\ &=\begin{vmatrix}1 & 1 & 0\\1 & -1 & 0\\0 & 0 & \frac{1}{2 \sqrt{z}}\end{vmatrix}\\ &=(1)\begin{vmatrix}-1 & 0\\0 & \frac{1}{2 \sqrt{z}}\end{vmatrix}-(1)\begin{vmatrix}1 & 0\\0 & \frac{1}{2 \sqrt{z}}\end{vmatrix}+(0)\begin{vmatrix}1 & -1\\0 & 0\end{vmatrix}\\ &=- \frac{1}{\sqrt{z}}\\ &=- \frac{1}{w}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}=- w.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$ Since $z\ge1$ and $w=\sqrt z$, the branch is $w>0$.

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R \sqrt{z}\,dV &=\iiint_Δ \left(w\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left(w\right)\left|- w\right|\,du\,dv\,dw\\ &=\int_{1}^{3}\int_{1}^{3}\int_{1}^{\sqrt{u v}}\left(w^{2}\right)\,dw\,dv\,du.\end{aligned}
$$