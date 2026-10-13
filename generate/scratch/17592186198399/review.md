# Review: originals and labeled generated variants


## Original 17592186198624 — linear_yz

Find the volume bounded by the region $R,$ given by

$$
R={(x,y,z)\,:\,0\le x\le 1,\,-1\le 2y+z\le 1,\,1\le y-2z\le 4}.
$$

Original complete bank: $\frac{6}{5}$, $\frac{8}{5}$, $15$, $2$, $\frac{2}{5}$

Original complete bank: $15$, $\frac{6}{5}$, $\frac{2}{5}$, $2$, $\frac{8}{5}$

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
0\le x\le 1,\,-1\le 2y+z\le 1,\,1\le y-2z\le 4,
$$

suggest that we use the change of variables

$$
u=x,\,v=2y+z,\,w=y-2z.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\begin{aligned}Δ & ={(u,v,w)\,:\,0\le u\le 1,\,-1\le v\le 1,\,1\le w\le 4}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & 0 & 0 \\ 0 & 2 & 1 \\ 0 & 1 & -2\end{aligned}| \\  & =1(-1)^{1+1}|\begin{aligned}2 & 1 \\ 1 & -2\end{aligned}| \\  & =-5.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}=-\frac{1}{5}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}{∭}_{R}dV & ={∭}_{Δ}1\cdot |-\frac{1}{5}|\,\text{d}u\text{d}v\text{d}w \\  & ={\int }_{0}^{1}{\int }_{-1}^{1}{\int }_{1}^{4}\frac{1}{5}\,dw\,dv\,du \\  & =\frac{1}{5}{\int }_{0}^{1}du\cdot {\int }_{-1}^{1}dv\cdot {\int }_{1}^{4}dw \\  & =\frac{1}{5}[u]_{0}^{1}\cdot [v]_{-1}^{1}\cdot [w]_{1}^{4} \\  & =\frac{1}{5}\cdot (1-0)\cdot (1-(-1))\cdot (4-1) \\  & =\frac{6}{5}.\end{aligned}
$$

### Generated raw evidence variant h=2 — ineligible

Find the volume bounded by the region $R,$ given by

$$
R={(x,y,z)\,:\,0\le x\le 1,\,-2\le 2y+z\le 2,\,1\le y-2z\le 4}.
$$

 - $30$

 - $\frac{16}{5}$

 - $\frac{12}{5}$

 - $\frac{4}{5}$

 - $4$

 - $\frac{4}{5}$

 - $4$

 - $\frac{16}{5}$

 - $30$

 - $\frac{12}{5}$

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
0\le x\le 1,\,-2\le 2y+z\le 2,\,1\le y-2z\le 4,
$$

suggest that we use the change of variables

$$
u=x,\,v=2y+z,\,w=y-2z.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\begin{aligned}Δ & ={(u,v,w)\,:\,0\le u\le 1,\,-2\le v\le 2,\,1\le w\le 4}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & 0 & 0 \\ 0 & 2 & 1 \\ 0 & 1 & -2\end{aligned}| \\  & =1(-1)^{1+1}|\begin{aligned}2 & 1 \\ 1 & -2\end{aligned}| \\  & =-5.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}=-\frac{1}{5}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}{∭}_{R}dV & ={∭}_{Δ}1\cdot |-\frac{1}{5}|\,\text{d}u\text{d}v\text{d}w \\  & ={\int }_{0}^{1}{\int }_{-2}^{2}{\int }_{1}^{4}\frac{1}{5}\,dw\,dv\,du \\  & =\frac{1}{5}{\int }_{0}^{1}du\cdot {\int }_{-2}^{2}dv\cdot {\int }_{1}^{4}dw \\  & =\frac{1}{5}[u]_{0}^{1}\cdot [v]_{-2}^{2}\cdot [w]_{1}^{4} \\  & =\frac{1}{5}\cdot (1-0)\cdot (2-(-2))\cdot (4-1) \\  & =\frac{12}{5}.\end{aligned}
$$

## Original 17592186198965 — reciprocal

Find the volume bounded by the region $R$, given by
$R = {(x, y, z): 1 \le y \le 2, 1 \le \sqrt{y} + x \le 2, 1 \le \frac{1}{z + 1} \le 5}$.

Original complete bank: $4$, $1$, $\frac{4}{5}$, $2$, $-\frac{2}{5}$

Original solution absent. Original difficulty/correct designation absent.

### Generated raw evidence variant h=2 — ineligible

Find the volume bounded by the region $R$, given by
$R = {(x, y, z): 1 \le y \le 2, 2 \le \sqrt{y} + x \le 4, 1 \le \frac{1}{z + 1} \le 5}$.

 - $\frac{8}{5}$

 - $2$

 - $8$

 - $- \frac{4}{5}$

 - $4$

## Original 17592186374152 — log

Find the volume bounded by the region $R,$ given by

$$
R={(x,y,z)\,:\,\frac{1}{2}\le x\le 1,\,3\le y+{x}^{2}\le 10,\,1\le xz\le 2}.
$$

Original complete bank: $28$, $2\operatorname{ln}⁡2$, $7\operatorname{ln}⁡2$, $14$, $30$

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
\frac{1}{2}\le x\le 1,\,3\le y+{x}^{2}\le 10,\,1\le xz\le 2,
$$

suggest that we use the change of variables

$$
u=x,\,v=y+{x}^{2},\,w=xz.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\begin{aligned}Δ & ={(u,v,w)\,:\,\frac{1}{2}\le u\le 1,\,3\le v\le 10,\,1\le w\le 2}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & 0 & 0 \\ 2x & 1 & 0 \\ z & 0 & x\end{aligned}| \\  & =1(-1)^{1+1}|\begin{aligned}1 & 0 \\ 0 & x\end{aligned}| \\  & =x \\  & =u.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}=\frac{1}{u}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}{∭}_{R}dV & ={∭}_{Δ}1\cdot |\frac{1}{u}|\,\text{d}u\text{d}v\text{d}w \\  & ={\int }_{1/2}^{1}{\int }_{3}^{10}{\int }_{1}^{2}\frac{1}{u}\,dw\,dv\,du \\  & ={\int }_{1/2}^{1}\frac{1}{u}du\cdot {\int }_{3}^{10}dv\cdot {\int }_{1}^{2}dw \\  & =[\operatorname{ln}⁡u]_{u=1/2}^{u=1}\cdot [v]_{v=3}^{v=10}\cdot [w]_{w=1}^{w=2} \\  & =-\operatorname{ln}⁡(\frac{1}{2})\cdot (10-3)\cdot (2-1) \\  & =7\operatorname{ln}⁡2.\end{aligned}
$$

### Generated raw evidence variant h=2 — ineligible

Find the volume bounded by the region $R,$ given by

$$
R={(x,y,z)\,:\,\frac{1}{2}\le x\le 1,\,6\le y+{x}^{2}\le 20,\,1\le xz\le 2}.
$$

 - $14\operatorname{ln}⁡2$

 - $4\operatorname{ln}⁡2$

 - $56$

 - $60$

 - $28$

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
\frac{1}{2}\le x\le 1,\,6\le y+{x}^{2}\le 20,\,1\le xz\le 2,
$$

suggest that we use the change of variables

$$
u=x,\,v=y+{x}^{2},\,w=xz.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\begin{aligned}Δ & ={(u,v,w)\,:\,\frac{1}{2}\le u\le 1,\,6\le v\le 20,\,1\le w\le 2}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & 0 & 0 \\ 2x & 1 & 0 \\ z & 0 & x\end{aligned}| \\  & =1(-1)^{1+1}|\begin{aligned}1 & 0 \\ 0 & x\end{aligned}| \\  & =x \\  & =u.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}=\frac{1}{u}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}{∭}_{R}dV & ={∭}_{Δ}1\cdot |\frac{1}{u}|\,\text{d}u\text{d}v\text{d}w \\  & ={\int }_{1/2}^{1}{\int }_{6}^{20}{\int }_{1}^{2}\frac{1}{u}\,dw\,dv\,du \\  & ={\int }_{1/2}^{1}\frac{1}{u}du\cdot {\int }_{6}^{20}dv\cdot {\int }_{1}^{2}dw \\  & =[\operatorname{ln}⁡u]_{u=1/2}^{u=1}\cdot [v]_{v=6}^{v=20}\cdot [w]_{w=1}^{w=2} \\  & =-\operatorname{ln}⁡(\frac{1}{2})\cdot (20-6)\cdot (2-1) \\  & =14\operatorname{ln}⁡2.\end{aligned}
$$

## Original 17592186374159 — shear

Find the volume bounded by the region $R,$ given by

$$
R={(x,y,z)\,:\,0\le x\le 1,\,0\le x+y\le 1,\,-1\le z+{x}^{2}+{y}^{2}\le 1}.
$$

Original complete bank: $3$, $\frac{1}{2}$, $2$, $1$, $4$

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
0\le x\le 1,\,0\le x+y\le 1,\,-1\le z+{x}^{2}+{y}^{2}\le 1,
$$

suggest that we use the change of variables

$$
u=x,\,v=x+y,\,w=z+{x}^{2}+{y}^{2}.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\begin{aligned}Δ & ={(u,v,w)\,:\,0\le u\le 1,\,0\le v\le 1,\,-1\le w\le 1}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & 0 & 0 \\ 1 & 1 & 0 \\ 2x & 2y & 1\end{aligned}| \\  & =1.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}=1.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}{∭}_{R}dV & ={∭}_{Δ}1\cdot |1|\,\text{d}u\text{d}v\text{d}w \\  & ={\int }_{0}^{1}{\int }_{0}^{1}{\int }_{-1}^{1}dw\,dv\,du \\  & ={\int }_{0}^{1}du\cdot {\int }_{0}^{1}dv\cdot {\int }_{-1}^{1}dw \\  & =[u]_{u=0}^{u=1}\cdot [v]_{v=0}^{v=1}\cdot [w]_{w=-1}^{w=1} \\  & =(1-0)\cdot (1-0)\cdot (1-(-1)) \\  & =2.\end{aligned}
$$

### Generated raw evidence variant h=2 — ineligible

Find the volume bounded by the region $R,$ given by

$$
R={(x,y,z)\,:\,0\le x\le 1,\,0\le x+y\le 2,\,-1\le z+{x}^{2}+{y}^{2}\le 1}.
$$

 - $4$

 - $1$

 - $6$

 - $8$

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
0\le x\le 1,\,0\le x+y\le 2,\,-1\le z+{x}^{2}+{y}^{2}\le 1,
$$

suggest that we use the change of variables

$$
u=x,\,v=x+y,\,w=z+{x}^{2}+{y}^{2}.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\begin{aligned}Δ & ={(u,v,w)\,:\,0\le u\le 1,\,0\le v\le 2,\,-1\le w\le 1}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & 0 & 0 \\ 1 & 1 & 0 \\ 2x & 2y & 1\end{aligned}| \\  & =1.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}=1.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}{∭}_{R}dV & ={∭}_{Δ}1\cdot |1|\,\text{d}u\text{d}v\text{d}w \\  & ={\int }_{0}^{2}{\int }_{0}^{2}{\int }_{-1}^{1}dw\,dv\,du \\  & ={\int }_{0}^{2}du\cdot {\int }_{0}^{2}dv\cdot {\int }_{-1}^{1}dw \\  & =[u]_{u=0}^{u=1}\cdot [v]_{v=0}^{v=2}\cdot [w]_{w=-1}^{w=1} \\  & =(2-0)\cdot (2-0)\cdot (1-(-1)) \\  & =4.\end{aligned}
$$

## Original 17592186374166 — linear_xz

Find the volume bounded by the region $R,$ given by

$$
R={(x,y,z)\,:\,-5\le x+z\le 5,\,0\le y\le 10,\,0\le y-z\le 6}.
$$

Original complete bank: $60$, $120$, $600$, $100$, $200$

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
-5\le x+z\le 5,,\,0\le y\le 10,\,0\le y-z\le 6,
$$

suggest that we use the change of variables

$$
u=x+z,\,v=y,\,w=y-z.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\begin{aligned}Δ & ={(u,v,w)\,:\,-5\le u\le 5,\,0\le v\le 10,\,0\le w\le 6}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & 0 & 1 \\ 0 & 1 & 0 \\ 0 & 1 & -1\end{aligned}| \\  & =-1.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}=-1.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}{∭}_{R}dV & ={∭}_{Δ}1\cdot |-1|\,\text{d}u\text{d}v\text{d}w \\  & ={\int }_{-5}^{5}{\int }_{0}^{10}{\int }_{0}^{6}dw\,dv\,du \\  & ={\int }_{-5}^{5}du\cdot {\int }_{0}^{10}dv\cdot {\int }_{0}^{6}dw \\  & =[u]_{u=-5}^{u=5}\cdot [v]_{v=0}^{v=10}\cdot [w]_{w=0}^{w=6} \\  & =(5-(-5))\cdot (10-0)\cdot (6-0) \\  & =600.\end{aligned}
$$

### Generated raw evidence variant h=2 — ineligible

Find the volume bounded by the region $R,$ given by

$$
R={(x,y,z)\,:\,-5\le x+z\le 5,\,0\le y\le 20,\,0\le y-z\le 6}.
$$

 - $1200$

 - $240$

 - $120$

 - $400$

 - $200$

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
-5\le x+z\le 5,,\,0\le y\le 20,\,0\le y-z\le 6,
$$

suggest that we use the change of variables

$$
u=x+z,\,v=y,\,w=y-z.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\begin{aligned}Δ & ={(u,v,w)\,:\,-5\le u\le 5,\,0\le v\le 20,\,0\le w\le 6}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & 0 & 1 \\ 0 & 1 & 0 \\ 0 & 1 & -1\end{aligned}| \\  & =-1.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}=-1.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}{∭}_{R}dV & ={∭}_{Δ}1\cdot |-1|\,\text{d}u\text{d}v\text{d}w \\  & ={\int }_{-5}^{5}{\int }_{0}^{20}{\int }_{0}^{6}dw\,dv\,du \\  & ={\int }_{-5}^{5}du\cdot {\int }_{0}^{20}dv\cdot {\int }_{0}^{6}dw \\  & =[u]_{u=-5}^{u=5}\cdot [v]_{v=0}^{v=20}\cdot [w]_{w=0}^{w=6} \\  & =(5-(-5))\cdot (20-0)\cdot (6-0) \\  & =1200.\end{aligned}
$$

## Original 17592186374173 — sqrt

Find the volume bounded by the region $R,$ given by

$$
R={(x,y,z)\,:\,-2\le x\le 2,\,0\le {x}^{2}-y-z\le 1,\,1\le \sqrt{z}\le 4}.
$$

Original complete bank: $12$, $60$, $36$, $6$, $30$

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
-2\le x\le 2,\,0\le {x}^{2}-y-z\le 1,\,1\le \sqrt{z}\le 4,
$$

suggest that we use the change of variables

$$
u=x,\,v={x}^{2}-y-z,\,w=\sqrt{z}.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\begin{aligned}Δ & ={(u,v,w)\,:\,-2\le u\le 2,\,0\le v\le 1,\,1\le w\le 4}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & 0 & 0 \\ 2x & -1 & -1 \\ 0 & 0 & \frac{1}{2\sqrt{z}}\end{aligned}| \\  & =1(-1)^{1+1}|\begin{aligned}-1 & -1 \\ 0 & \frac{1}{2\sqrt{z}}\end{aligned}| \\  & =-\frac{1}{2\sqrt{z}} \\  & =-\frac{1}{2w}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}=-2w.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}{∭}_{R}dV & ={∭}_{Δ}1\cdot |-2w|\,\text{d}u\text{d}v\text{d}w \\  & ={\int }_{-2}^{2}{\int }_{0}^{1}{\int }_{1}^{4}2w\,dw\,dv\,du \\  & ={\int }_{-2}^{2}du\cdot {\int }_{0}^{1}dv\cdot {\int }_{1}^{4}2w\,dw \\  & =[u]_{u=-2}^{u=2}\cdot [v]_{v=0}^{v=1}\cdot [{w}^{2}]_{w=1}^{w=4} \\  & =(2-(-2))\cdot (1-0)\cdot (16-1) \\  & =60.\end{aligned}
$$

### Generated raw evidence variant h=2 — ineligible

Find the volume bounded by the region $R,$ given by

$$
R={(x,y,z)\,:\,-2\le x\le 2,\,0\le {x}^{2}-y-z\le 2,\,1\le \sqrt{z}\le 4}.
$$

 - $72$

 - $120$

 - $24$

 - $60$

 - $12$

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
-2\le x\le 2,\,0\le {x}^{2}-y-z\le 2,\,1\le \sqrt{z}\le 4,
$$

suggest that we use the change of variables

$$
u=x,\,v={x}^{2}-y-z,\,w=\sqrt{z}.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]\to [\begin{aligned}u(x,y,z) \\ v(x,y,z) \\ w(x,y,z)\end{aligned}].
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ 

Our domain in the $uvw$-space is

$$
\begin{aligned}Δ & ={(u,v,w)\,:\,-2\le u\le 2,\,0\le v\le 2,\,1\le w\le 4}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & 0 & 0 \\ 2x & -1 & -1 \\ 0 & 0 & \frac{1}{2\sqrt{z}}\end{aligned}| \\  & =1(-1)^{1+1}|\begin{aligned}-1 & -1 \\ 0 & \frac{1}{2\sqrt{z}}\end{aligned}| \\  & =-\frac{1}{2\sqrt{z}} \\  & =-\frac{1}{2w}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}=-2w.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}{∭}_{R}dV & ={∭}_{Δ}1\cdot |-2w|\,\text{d}u\text{d}v\text{d}w \\  & ={\int }_{-2}^{2}{\int }_{0}^{2}{\int }_{1}^{4}2w\,dw\,dv\,du \\  & ={\int }_{-2}^{2}du\cdot {\int }_{0}^{2}dv\cdot {\int }_{1}^{4}2w\,dw \\  & =[u]_{u=-2}^{u=2}\cdot [v]_{v=0}^{v=2}\cdot [{w}^{2}]_{w=1}^{w=4} \\  & =(2-(-2))\cdot (2-0)\cdot (16-1) \\  & =120.\end{aligned}
$$

## Authored/default easy — affine

Find the volume bounded by the region $R,$ given by

$$
R=\big\{(x,y,z)\, :\, 0\le 2 x\le 5,\quad 0\le 2 x + y\le 6,\quad 0\le 2 z\le 2\big\}.
$$

 - $240$

 - $60$

 - $15$

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
0\le 2 x\le 5,\quad 0\le 2 x + y\le 6,\quad 0\le 2 z\le 2,
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
\Delta=\big\{(u,v,w):0\le u\le 5,\quad 0\le v\le 6,\quad 0\le w\le 2\big\}.
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
\begin{aligned}\iiint_R\mathrm{d}V & =\iiint_\Delta 1\cdot |\frac{1}{4}|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{5}\int_{0}^{6}\int_{0}^{2}\frac{1}{4}\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\frac{1}{4}\cdot \int_{0}^{5}1\,\mathrm{d}u\cdot \int_{0}^{6}1\,\mathrm{d}v\cdot \int_{0}^{2}1\,\mathrm{d}w \\  & =\frac{1}{4}\cdot [u]_{0}^{5}\cdot [v]_{0}^{6}\cdot [w]_{0}^{2} \\  & =\frac{1}{4}\cdot \left(\left(\left(5\right)\right)-\left(\left(0\right)\right)\right)\cdot \left(\left(\left(6\right)\right)-\left(\left(0\right)\right)\right)\cdot \left(\left(\left(2\right)\right)-\left(\left(0\right)\right)\right) \\  & =\frac{1}{4}\cdot \left(\left(5\right)-\left(0\right)\right)\cdot \left(\left(6\right)-\left(0\right)\right)\cdot \left(\left(2\right)-\left(0\right)\right) \\  & =15\end{aligned}
$$

## Authored/default easy — affine

Find the volume bounded by the region $R,$ given by

$$
R=\big\{(x,y,z)\, :\, 0\le 3 x\le 3,\quad 0\le x + y\le 2,\quad 0\le 2 z\le 6\big\}.
$$

 - $216$

 - $2$

 - $3$

 - $6$

 - $36$

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
0\le 3 x\le 3,\quad 0\le x + y\le 2,\quad 0\le 2 z\le 6,
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
\Delta=\big\{(u,v,w):0\le u\le 3,\quad 0\le v\le 2,\quad 0\le w\le 6\big\}.
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
\begin{aligned}\iiint_R\mathrm{d}V & =\iiint_\Delta 1\cdot |\frac{1}{6}|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{0}^{3}\int_{0}^{2}\int_{0}^{6}\frac{1}{6}\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\frac{1}{6}\cdot \int_{0}^{3}1\,\mathrm{d}u\cdot \int_{0}^{2}1\,\mathrm{d}v\cdot \int_{0}^{6}1\,\mathrm{d}w \\  & =\frac{1}{6}\cdot [u]_{0}^{3}\cdot [v]_{0}^{2}\cdot [w]_{0}^{6} \\  & =\frac{1}{6}\cdot \left(\left(\left(3\right)\right)-\left(\left(0\right)\right)\right)\cdot \left(\left(\left(2\right)\right)-\left(\left(0\right)\right)\right)\cdot \left(\left(\left(6\right)\right)-\left(\left(0\right)\right)\right) \\  & =\frac{1}{6}\cdot \left(\left(3\right)-\left(0\right)\right)\cdot \left(\left(2\right)-\left(0\right)\right)\cdot \left(\left(6\right)-\left(0\right)\right) \\  & =6\end{aligned}
$$

## Authored/default moderate — linear_yz

Find the volume bounded by the region $R,$ given by

$$
R=\big\{(x,y,z)\, :\, 1\le x\le 6,\quad 2\le - y + 2 z\le 8,\quad 1\le y + z\le 3\big\}.
$$

 - $\frac{10}{3}$

 - $4$

 - $20$

 - $24$

 - $10$

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
1\le x\le 6,\quad 2\le - y + 2 z\le 8,\quad 1\le y + z\le 3,
$$

suggest that we use the change of variables

$$
u=x,\quad v=- y + 2 z,\quad w=y + z.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y,z)\longmapsto(u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
\Delta=\big\{(u,v,w):1\le u\le 6,\quad 2\le v\le 8,\quad 1\le w\le 3\big\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}1 & 0 & 0 \\ 0 & -1 & 2 \\ 0 & 1 & 1\end{vmatrix} \\  & =\left(1\right)(-1)^{1+1}\begin{vmatrix}-1 & 2 \\ 1 & 1\end{vmatrix}+\left(0\right)(-1)^{1+2}\begin{vmatrix}0 & 2 \\ 0 & 1\end{vmatrix}+\left(0\right)(-1)^{1+3}\begin{vmatrix}0 & -1 \\ 0 & 1\end{vmatrix} \\  & =-3\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{3}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

The map to $R$ is

$$
T(u,v,w)=\left(u,- \frac{v}{3} + \frac{2 w}{3},\frac{v}{3} + \frac{w}{3}\right).
$$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R\mathrm{d}V & =\iiint_\Delta 1\cdot |- \frac{1}{3}|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{1}^{6}\int_{2}^{8}\int_{1}^{3}\frac{1}{3}\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\frac{1}{3}\cdot \int_{1}^{6}1\,\mathrm{d}u\cdot \int_{2}^{8}1\,\mathrm{d}v\cdot \int_{1}^{3}1\,\mathrm{d}w \\  & =\frac{1}{3}\cdot [u]_{1}^{6}\cdot [v]_{2}^{8}\cdot [w]_{1}^{3} \\  & =\frac{1}{3}\cdot \left(\left(\left(6\right)\right)-\left(\left(1\right)\right)\right)\cdot \left(\left(\left(8\right)\right)-\left(\left(2\right)\right)\right)\cdot \left(\left(\left(3\right)\right)-\left(\left(1\right)\right)\right) \\  & =\frac{1}{3}\cdot \left(\left(6\right)-\left(1\right)\right)\cdot \left(\left(8\right)-\left(2\right)\right)\cdot \left(\left(3\right)-\left(1\right)\right) \\  & =20\end{aligned}
$$

## Authored/default moderate — linear_yz

Find the volume bounded by the region $R,$ given by

$$
R=\big\{(x,y,z)\, :\, 2\le x\le 5,\quad -1\le - 3 y + z\le 1,\quad -2\le y + z\le 4\big\}.
$$

 - $\frac{9}{2}$

 - $\frac{3}{2}$

 - $15$

 - $9$

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
2\le x\le 5,\quad -1\le - 3 y + z\le 1,\quad -2\le y + z\le 4,
$$

suggest that we use the change of variables

$$
u=x,\quad v=- 3 y + z,\quad w=y + z.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y,z)\longmapsto(u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
\Delta=\big\{(u,v,w):2\le u\le 5,\quad -1\le v\le 1,\quad -2\le w\le 4\big\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}1 & 0 & 0 \\ 0 & -3 & 1 \\ 0 & 1 & 1\end{vmatrix} \\  & =\left(1\right)(-1)^{1+1}\begin{vmatrix}-3 & 1 \\ 1 & 1\end{vmatrix}+\left(0\right)(-1)^{1+2}\begin{vmatrix}0 & 1 \\ 0 & 1\end{vmatrix}+\left(0\right)(-1)^{1+3}\begin{vmatrix}0 & -3 \\ 0 & 1\end{vmatrix} \\  & =-4\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{4}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

The map to $R$ is

$$
T(u,v,w)=\left(u,- \frac{v}{4} + \frac{w}{4},\frac{v}{4} + \frac{3 w}{4}\right).
$$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R\mathrm{d}V & =\iiint_\Delta 1\cdot |- \frac{1}{4}|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{2}^{5}\int_{-1}^{1}\int_{-2}^{4}\frac{1}{4}\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\frac{1}{4}\cdot \int_{2}^{5}1\,\mathrm{d}u\cdot \int_{-1}^{1}1\,\mathrm{d}v\cdot \int_{-2}^{4}1\,\mathrm{d}w \\  & =\frac{1}{4}\cdot [u]_{2}^{5}\cdot [v]_{-1}^{1}\cdot [w]_{-2}^{4} \\  & =\frac{1}{4}\cdot \left(\left(\left(5\right)\right)-\left(\left(2\right)\right)\right)\cdot \left(\left(\left(1\right)\right)-\left(\left(-1\right)\right)\right)\cdot \left(\left(\left(4\right)\right)-\left(\left(-2\right)\right)\right) \\  & =\frac{1}{4}\cdot \left(\left(5\right)-\left(2\right)\right)\cdot \left(\left(1\right)-\left(-1\right)\right)\cdot \left(\left(4\right)-\left(-2\right)\right) \\  & =9\end{aligned}
$$

## Authored/default moderate — shear

Find the volume bounded by the region $R,$ given by

$$
R=\big\{(x,y,z)\, :\, 1\le x\le 6,\quad 2\le - x + y\le 8,\quad 1\le 2 x^{2} + y^{2} + z\le 3\big\}.
$$

 - $10$

 - $12$

 - $60$

 - $72$

 - $30$

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
1\le x\le 6,\quad 2\le - x + y\le 8,\quad 1\le 2 x^{2} + y^{2} + z\le 3,
$$

suggest that we use the change of variables

$$
u=x,\quad v=- x + y,\quad w=2 x^{2} + y^{2} + z.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y,z)\longmapsto(u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
\Delta=\big\{(u,v,w):1\le u\le 6,\quad 2\le v\le 8,\quad 1\le w\le 3\big\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}1 & 0 & 0 \\ -1 & 1 & 0 \\ 4 x & 2 y & 1\end{vmatrix} \\  & =\left(1\right)(-1)^{1+1}\begin{vmatrix}1 & 0 \\ 2 y & 1\end{vmatrix}+\left(0\right)(-1)^{1+2}\begin{vmatrix}-1 & 0 \\ 4 x & 1\end{vmatrix}+\left(0\right)(-1)^{1+3}\begin{vmatrix}-1 & 1 \\ 4 x & 2 y\end{vmatrix} \\  & =1\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=1.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

The map to $R$ is

$$
T(u,v,w)=\left(u,u + v,- 2 u^{2} + w - \left(u + v\right)^{2}\right).
$$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R\mathrm{d}V & =\iiint_\Delta 1\cdot |1|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{1}^{6}\int_{2}^{8}\int_{1}^{3}1\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =1\cdot \int_{1}^{6}1\,\mathrm{d}u\cdot \int_{2}^{8}1\,\mathrm{d}v\cdot \int_{1}^{3}1\,\mathrm{d}w \\  & =1\cdot [u]_{1}^{6}\cdot [v]_{2}^{8}\cdot [w]_{1}^{3} \\  & =1\cdot \left(\left(\left(6\right)\right)-\left(\left(1\right)\right)\right)\cdot \left(\left(\left(8\right)\right)-\left(\left(2\right)\right)\right)\cdot \left(\left(\left(3\right)\right)-\left(\left(1\right)\right)\right) \\  & =1\cdot \left(\left(6\right)-\left(1\right)\right)\cdot \left(\left(8\right)-\left(2\right)\right)\cdot \left(\left(3\right)-\left(1\right)\right) \\  & =60\end{aligned}
$$

## Authored/default moderate — shear

Find the volume bounded by the region $R,$ given by

$$
R=\big\{(x,y,z)\, :\, 2\le x\le 5,\quad -1\le - 3 x + y\le 1,\quad -2\le x^{2} + y^{2} + z\le 4\big\}.
$$

 - $18$

 - $6$

 - $60$

 - $36$

 - $12$

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
2\le x\le 5,\quad -1\le - 3 x + y\le 1,\quad -2\le x^{2} + y^{2} + z\le 4,
$$

suggest that we use the change of variables

$$
u=x,\quad v=- 3 x + y,\quad w=x^{2} + y^{2} + z.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y,z)\longmapsto(u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
\Delta=\big\{(u,v,w):2\le u\le 5,\quad -1\le v\le 1,\quad -2\le w\le 4\big\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}1 & 0 & 0 \\ -3 & 1 & 0 \\ 2 x & 2 y & 1\end{vmatrix} \\  & =\left(1\right)(-1)^{1+1}\begin{vmatrix}1 & 0 \\ 2 y & 1\end{vmatrix}+\left(0\right)(-1)^{1+2}\begin{vmatrix}-3 & 0 \\ 2 x & 1\end{vmatrix}+\left(0\right)(-1)^{1+3}\begin{vmatrix}-3 & 1 \\ 2 x & 2 y\end{vmatrix} \\  & =1\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=1.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

The map to $R$ is

$$
T(u,v,w)=\left(u,3 u + v,- u^{2} + w - \left(3 u + v\right)^{2}\right).
$$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R\mathrm{d}V & =\iiint_\Delta 1\cdot |1|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{2}^{5}\int_{-1}^{1}\int_{-2}^{4}1\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =1\cdot \int_{2}^{5}1\,\mathrm{d}u\cdot \int_{-1}^{1}1\,\mathrm{d}v\cdot \int_{-2}^{4}1\,\mathrm{d}w \\  & =1\cdot [u]_{2}^{5}\cdot [v]_{-1}^{1}\cdot [w]_{-2}^{4} \\  & =1\cdot \left(\left(\left(5\right)\right)-\left(\left(2\right)\right)\right)\cdot \left(\left(\left(1\right)\right)-\left(\left(-1\right)\right)\right)\cdot \left(\left(\left(4\right)\right)-\left(\left(-2\right)\right)\right) \\  & =1\cdot \left(\left(5\right)-\left(2\right)\right)\cdot \left(\left(1\right)-\left(-1\right)\right)\cdot \left(\left(4\right)-\left(-2\right)\right) \\  & =36\end{aligned}
$$

## Authored/default moderate — linear_xz

Find the volume bounded by the region $R,$ given by

$$
R=\big\{(x,y,z)\, :\, 1\le - x + 2 z\le 6,\quad 2\le y\le 8,\quad 1\le y + z\le 3\big\}.
$$

 - $10$

 - $12$

 - $60$

 - $72$

 - $30$

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
1\le - x + 2 z\le 6,\quad 2\le y\le 8,\quad 1\le y + z\le 3,
$$

suggest that we use the change of variables

$$
u=- x + 2 z,\quad v=y,\quad w=y + z.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y,z)\longmapsto(u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
\Delta=\big\{(u,v,w):1\le u\le 6,\quad 2\le v\le 8,\quad 1\le w\le 3\big\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}-1 & 0 & 2 \\ 0 & 1 & 0 \\ 0 & 1 & 1\end{vmatrix} \\  & =\left(-1\right)(-1)^{1+1}\begin{vmatrix}1 & 0 \\ 1 & 1\end{vmatrix}+\left(0\right)(-1)^{1+2}\begin{vmatrix}0 & 0 \\ 0 & 1\end{vmatrix}+\left(2\right)(-1)^{1+3}\begin{vmatrix}0 & 1 \\ 0 & 1\end{vmatrix} \\  & =-1\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=-1.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

The map to $R$ is

$$
T(u,v,w)=\left(- u - 2 v + 2 w,v,- v + w\right).
$$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R\mathrm{d}V & =\iiint_\Delta 1\cdot |-1|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{1}^{6}\int_{2}^{8}\int_{1}^{3}1\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =1\cdot \int_{1}^{6}1\,\mathrm{d}u\cdot \int_{2}^{8}1\,\mathrm{d}v\cdot \int_{1}^{3}1\,\mathrm{d}w \\  & =1\cdot [u]_{1}^{6}\cdot [v]_{2}^{8}\cdot [w]_{1}^{3} \\  & =1\cdot \left(\left(\left(6\right)\right)-\left(\left(1\right)\right)\right)\cdot \left(\left(\left(8\right)\right)-\left(\left(2\right)\right)\right)\cdot \left(\left(\left(3\right)\right)-\left(\left(1\right)\right)\right) \\  & =1\cdot \left(\left(6\right)-\left(1\right)\right)\cdot \left(\left(8\right)-\left(2\right)\right)\cdot \left(\left(3\right)-\left(1\right)\right) \\  & =60\end{aligned}
$$

## Authored/default moderate — linear_xz

Find the volume bounded by the region $R,$ given by

$$
R=\big\{(x,y,z)\, :\, 2\le - 3 x + z\le 5,\quad -1\le y\le 1,\quad -2\le y + z\le 4\big\}.
$$

 - $6$

 - $2$

 - $20$

 - $12$

 - $4$

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
2\le - 3 x + z\le 5,\quad -1\le y\le 1,\quad -2\le y + z\le 4,
$$

suggest that we use the change of variables

$$
u=- 3 x + z,\quad v=y,\quad w=y + z.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y,z)\longmapsto(u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
\Delta=\big\{(u,v,w):2\le u\le 5,\quad -1\le v\le 1,\quad -2\le w\le 4\big\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}-3 & 0 & 1 \\ 0 & 1 & 0 \\ 0 & 1 & 1\end{vmatrix} \\  & =\left(-3\right)(-1)^{1+1}\begin{vmatrix}1 & 0 \\ 1 & 1\end{vmatrix}+\left(0\right)(-1)^{1+2}\begin{vmatrix}0 & 0 \\ 0 & 1\end{vmatrix}+\left(1\right)(-1)^{1+3}\begin{vmatrix}0 & 1 \\ 0 & 1\end{vmatrix} \\  & =-3\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{3}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

The map to $R$ is

$$
T(u,v,w)=\left(- \frac{u}{3} - \frac{v}{3} + \frac{w}{3},v,- v + w\right).
$$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R\mathrm{d}V & =\iiint_\Delta 1\cdot |- \frac{1}{3}|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{2}^{5}\int_{-1}^{1}\int_{-2}^{4}\frac{1}{3}\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =\frac{1}{3}\cdot \int_{2}^{5}1\,\mathrm{d}u\cdot \int_{-1}^{1}1\,\mathrm{d}v\cdot \int_{-2}^{4}1\,\mathrm{d}w \\  & =\frac{1}{3}\cdot [u]_{2}^{5}\cdot [v]_{-1}^{1}\cdot [w]_{-2}^{4} \\  & =\frac{1}{3}\cdot \left(\left(\left(5\right)\right)-\left(\left(2\right)\right)\right)\cdot \left(\left(\left(1\right)\right)-\left(\left(-1\right)\right)\right)\cdot \left(\left(\left(4\right)\right)-\left(\left(-2\right)\right)\right) \\  & =\frac{1}{3}\cdot \left(\left(5\right)-\left(2\right)\right)\cdot \left(\left(1\right)-\left(-1\right)\right)\cdot \left(\left(4\right)-\left(-2\right)\right) \\  & =12\end{aligned}
$$

## Authored/default hard — log

Find the volume bounded by the region $R,$ given by

$$
R=\big\{(x,y,z)\, :\, \frac{1}{2}\le x\le 4,\quad 2\le - x^{2} + y\le 8,\quad 1\le 2 x z\le 3\big\}.
$$

 - $189$

 - $42$

 - $18 \ln{\left(2 \right)}$

 - $12 \ln{\left(2 \right)}$

 - $3 \ln{\left(2 \right)}$

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
\frac{1}{2}\le x\le 4,\quad 2\le - x^{2} + y\le 8,\quad 1\le 2 x z\le 3,
$$

suggest that we use the change of variables

$$
u=x,\quad v=- x^{2} + y,\quad w=2 x z.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y,z)\longmapsto(u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
\Delta=\big\{(u,v,w):\frac{1}{2}\le u\le 4,\quad 2\le v\le 8,\quad 1\le w\le 3\big\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}1 & 0 & 0 \\ - 2 x & 1 & 0 \\ 2 z & 0 & 2 x\end{vmatrix} \\  & =\left(1\right)(-1)^{1+1}\begin{vmatrix}1 & 0 \\ 0 & 2 x\end{vmatrix}+\left(0\right)(-1)^{1+2}\begin{vmatrix}- 2 x & 0 \\ 2 z & 2 x\end{vmatrix}+\left(0\right)(-1)^{1+3}\begin{vmatrix}- 2 x & 1 \\ 2 z & 0\end{vmatrix} \\  & =2 x \\  & =2 u\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=\frac{1}{2 u}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

The map to $R$ is

$$
T(u,v,w)=\left(u,u^{2} + v,\frac{w}{2 u}\right).
$$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R\mathrm{d}V & =\iiint_\Delta 1\cdot |\frac{1}{2 u}|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{\frac{1}{2}}^{4}\int_{2}^{8}\int_{1}^{3}\frac{1}{2 u}\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =1\cdot \int_{\frac{1}{2}}^{4}\frac{1}{2 u}\,\mathrm{d}u\cdot \int_{2}^{8}1\,\mathrm{d}v\cdot \int_{1}^{3}1\,\mathrm{d}w \\  & =1\cdot [\frac{\ln{\left(u \right)}}{2}]_{\frac{1}{2}}^{4}\cdot [v]_{2}^{8}\cdot [w]_{1}^{3} \\  & =1\cdot \left(\left(\frac{\ln{\left(\left(4\right) \right)}}{2}\right)-\left(\frac{\ln{\left(\left(\frac{1}{2}\right) \right)}}{2}\right)\right)\cdot \left(\left(\left(8\right)\right)-\left(\left(2\right)\right)\right)\cdot \left(\left(\left(3\right)\right)-\left(\left(1\right)\right)\right) \\  & =1\cdot \left(\left(\ln{\left(2 \right)}\right)-\left(- \frac{\ln{\left(2 \right)}}{2}\right)\right)\cdot \left(\left(8\right)-\left(2\right)\right)\cdot \left(\left(3\right)-\left(1\right)\right) \\  & =18 \ln{\left(2 \right)}\end{aligned}
$$

## Authored/default hard — log

Find the volume bounded by the region $R,$ given by

$$
R=\big\{(x,y,z)\, :\, \frac{1}{2}\le x\le 3,\quad -1\le - 3 x^{2} + y\le 1,\quad 1\le x z\le 7\big\}.
$$

 - $\frac{105}{2}$

 - $6 \ln{\left(6 \right)}$

 - $12 \ln{\left(3 \right)}$

 - $12 \ln{\left(6 \right)}$

 - $30$

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
\frac{1}{2}\le x\le 3,\quad -1\le - 3 x^{2} + y\le 1,\quad 1\le x z\le 7,
$$

suggest that we use the change of variables

$$
u=x,\quad v=- 3 x^{2} + y,\quad w=x z.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y,z)\longmapsto(u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
\Delta=\big\{(u,v,w):\frac{1}{2}\le u\le 3,\quad -1\le v\le 1,\quad 1\le w\le 7\big\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}1 & 0 & 0 \\ - 6 x & 1 & 0 \\ z & 0 & x\end{vmatrix} \\  & =\left(1\right)(-1)^{1+1}\begin{vmatrix}1 & 0 \\ 0 & x\end{vmatrix}+\left(0\right)(-1)^{1+2}\begin{vmatrix}- 6 x & 0 \\ z & x\end{vmatrix}+\left(0\right)(-1)^{1+3}\begin{vmatrix}- 6 x & 1 \\ z & 0\end{vmatrix} \\  & =x \\  & =u\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=\frac{1}{u}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

The map to $R$ is

$$
T(u,v,w)=\left(u,3 u^{2} + v,\frac{w}{u}\right).
$$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R\mathrm{d}V & =\iiint_\Delta 1\cdot |\frac{1}{u}|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{\frac{1}{2}}^{3}\int_{-1}^{1}\int_{1}^{7}\frac{1}{u}\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =1\cdot \int_{\frac{1}{2}}^{3}\frac{1}{u}\,\mathrm{d}u\cdot \int_{-1}^{1}1\,\mathrm{d}v\cdot \int_{1}^{7}1\,\mathrm{d}w \\  & =1\cdot [\ln{\left(u \right)}]_{\frac{1}{2}}^{3}\cdot [v]_{-1}^{1}\cdot [w]_{1}^{7} \\  & =1\cdot \left(\left(\ln{\left(\left(3\right) \right)}\right)-\left(\ln{\left(\left(\frac{1}{2}\right) \right)}\right)\right)\cdot \left(\left(\left(1\right)\right)-\left(\left(-1\right)\right)\right)\cdot \left(\left(\left(7\right)\right)-\left(\left(1\right)\right)\right) \\  & =1\cdot \left(\left(\ln{\left(3 \right)}\right)-\left(- \ln{\left(2 \right)}\right)\right)\cdot \left(\left(1\right)-\left(-1\right)\right)\cdot \left(\left(7\right)-\left(1\right)\right) \\  & =12 \ln{\left(6 \right)}\end{aligned}
$$

## Authored/default hard — sqrt

Find the volume bounded by the region $R,$ given by

$$
R=\big\{(x,y,z)\, :\, 1\le x\le 6,\quad 2\le - x^{2} - y - 2 z\le 8,\quad 1\le \sqrt{z}\le 5\big\}.
$$

 - $360$

 - $120$

 - $720$

 - $750$

 - $1240$

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
1\le x\le 6,\quad 2\le - x^{2} - y - 2 z\le 8,\quad 1\le \sqrt{z}\le 5,
$$

suggest that we use the change of variables

$$
u=x,\quad v=- x^{2} - y - 2 z,\quad w=\sqrt{z}.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y,z)\longmapsto(u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
\Delta=\big\{(u,v,w):1\le u\le 6,\quad 2\le v\le 8,\quad 1\le w\le 5\big\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}1 & 0 & 0 \\ - 2 x & -1 & -2 \\ 0 & 0 & \frac{1}{2 \sqrt{z}}\end{vmatrix} \\  & =\left(1\right)(-1)^{1+1}\begin{vmatrix}-1 & -2 \\ 0 & \frac{1}{2 \sqrt{z}}\end{vmatrix}+\left(0\right)(-1)^{1+2}\begin{vmatrix}- 2 x & -2 \\ 0 & \frac{1}{2 \sqrt{z}}\end{vmatrix}+\left(0\right)(-1)^{1+3}\begin{vmatrix}- 2 x & -1 \\ 0 & 0\end{vmatrix} \\  & =- \frac{1}{2 \sqrt{z}} \\  & =- \frac{1}{2 w}\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- 2 w.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

The map to $R$ is

$$
T(u,v,w)=\left(u,- u^{2} - v - 2 w^{2},w^{2}\right).
$$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R\mathrm{d}V & =\iiint_\Delta 1\cdot |- 2 w|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{1}^{6}\int_{2}^{8}\int_{1}^{5}2 w\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =1\cdot \int_{1}^{6}1\,\mathrm{d}u\cdot \int_{2}^{8}1\,\mathrm{d}v\cdot \int_{1}^{5}2 w\,\mathrm{d}w \\  & =1\cdot [u]_{1}^{6}\cdot [v]_{2}^{8}\cdot [w^{2}]_{1}^{5} \\  & =1\cdot \left(\left(\left(6\right)\right)-\left(\left(1\right)\right)\right)\cdot \left(\left(\left(8\right)\right)-\left(\left(2\right)\right)\right)\cdot \left(\left(\left(5\right)^{2}\right)-\left(\left(1\right)^{2}\right)\right) \\  & =1\cdot \left(\left(6\right)-\left(1\right)\right)\cdot \left(\left(8\right)-\left(2\right)\right)\cdot \left(\left(25\right)-\left(1\right)\right) \\  & =720\end{aligned}
$$

## Authored/default hard — sqrt

Find the volume bounded by the region $R,$ given by

$$
R=\big\{(x,y,z)\, :\, 2\le x\le 5,\quad -1\le - 3 x^{2} - y - z\le 1,\quad 1\le \sqrt{z}\le 4\big\}.
$$

 - $45$

 - $126$

 - $96$

 - $90$

 - $18$

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
2\le x\le 5,\quad -1\le - 3 x^{2} - y - z\le 1,\quad 1\le \sqrt{z}\le 4,
$$

suggest that we use the change of variables

$$
u=x,\quad v=- 3 x^{2} - y - z,\quad w=\sqrt{z}.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y,z)\longmapsto(u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
\Delta=\big\{(u,v,w):2\le u\le 5,\quad -1\le v\le 1,\quad 1\le w\le 4\big\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}1 & 0 & 0 \\ - 6 x & -1 & -1 \\ 0 & 0 & \frac{1}{2 \sqrt{z}}\end{vmatrix} \\  & =\left(1\right)(-1)^{1+1}\begin{vmatrix}-1 & -1 \\ 0 & \frac{1}{2 \sqrt{z}}\end{vmatrix}+\left(0\right)(-1)^{1+2}\begin{vmatrix}- 6 x & -1 \\ 0 & \frac{1}{2 \sqrt{z}}\end{vmatrix}+\left(0\right)(-1)^{1+3}\begin{vmatrix}- 6 x & -1 \\ 0 & 0\end{vmatrix} \\  & =- \frac{1}{2 \sqrt{z}} \\  & =- \frac{1}{2 w}\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- 2 w.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

The map to $R$ is

$$
T(u,v,w)=\left(u,- 3 u^{2} - v - w^{2},w^{2}\right).
$$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R\mathrm{d}V & =\iiint_\Delta 1\cdot |- 2 w|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{2}^{5}\int_{-1}^{1}\int_{1}^{4}2 w\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =1\cdot \int_{2}^{5}1\,\mathrm{d}u\cdot \int_{-1}^{1}1\,\mathrm{d}v\cdot \int_{1}^{4}2 w\,\mathrm{d}w \\  & =1\cdot [u]_{2}^{5}\cdot [v]_{-1}^{1}\cdot [w^{2}]_{1}^{4} \\  & =1\cdot \left(\left(\left(5\right)\right)-\left(\left(2\right)\right)\right)\cdot \left(\left(\left(1\right)\right)-\left(\left(-1\right)\right)\right)\cdot \left(\left(\left(4\right)^{2}\right)-\left(\left(1\right)^{2}\right)\right) \\  & =1\cdot \left(\left(5\right)-\left(2\right)\right)\cdot \left(\left(1\right)-\left(-1\right)\right)\cdot \left(\left(16\right)-\left(1\right)\right) \\  & =90\end{aligned}
$$

## Authored/default hard — reciprocal

Find the volume bounded by the region $R,$ given by

$$
R=\big\{(x,y,z)\, :\, 1\le y\le 6,\quad 2\le x + \sqrt{y}\le 8,\quad 1\le \frac{1}{z - 1}\le 5\big\}.
$$

 - $1240$

 - $120$

 - $24$

 - $\frac{144}{5}$

 - $6$

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
1\le y\le 6,\quad 2\le x + \sqrt{y}\le 8,\quad 1\le \frac{1}{z - 1}\le 5,
$$

suggest that we use the change of variables

$$
u=y,\quad v=x + \sqrt{y},\quad w=\frac{1}{z - 1}.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y,z)\longmapsto(u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
\Delta=\big\{(u,v,w):1\le u\le 6,\quad 2\le v\le 8,\quad 1\le w\le 5\big\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}0 & 1 & 0 \\ 1 & \frac{1}{2 \sqrt{y}} & 0 \\ 0 & 0 & - \frac{1}{\left(z - 1\right)^{2}}\end{vmatrix} \\  & =\left(0\right)(-1)^{1+1}\begin{vmatrix}\frac{1}{2 \sqrt{y}} & 0 \\ 0 & - \frac{1}{\left(z - 1\right)^{2}}\end{vmatrix}+\left(1\right)(-1)^{1+2}\begin{vmatrix}1 & 0 \\ 0 & - \frac{1}{\left(z - 1\right)^{2}}\end{vmatrix}+\left(0\right)(-1)^{1+3}\begin{vmatrix}1 & \frac{1}{2 \sqrt{y}} \\ 0 & 0\end{vmatrix} \\  & =\frac{1}{\left(z - 1\right)^{2}} \\  & =w^{2}\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=\frac{1}{w^{2}}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

The map to $R$ is

$$
T(u,v,w)=\left(- \sqrt{u} + v,u,1 + \frac{1}{w}\right).
$$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R\mathrm{d}V & =\iiint_\Delta 1\cdot |\frac{1}{w^{2}}|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{1}^{6}\int_{2}^{8}\int_{1}^{5}\frac{1}{w^{2}}\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =1\cdot \int_{1}^{6}1\,\mathrm{d}u\cdot \int_{2}^{8}1\,\mathrm{d}v\cdot \int_{1}^{5}\frac{1}{w^{2}}\,\mathrm{d}w \\  & =1\cdot [u]_{1}^{6}\cdot [v]_{2}^{8}\cdot [- \frac{1}{w}]_{1}^{5} \\  & =1\cdot \left(\left(\left(6\right)\right)-\left(\left(1\right)\right)\right)\cdot \left(\left(\left(8\right)\right)-\left(\left(2\right)\right)\right)\cdot \left(\left(- \frac{1}{\left(5\right)}\right)-\left(- \frac{1}{\left(1\right)}\right)\right) \\  & =1\cdot \left(\left(6\right)-\left(1\right)\right)\cdot \left(\left(8\right)-\left(2\right)\right)\cdot \left(\left(- \frac{1}{5}\right)-\left(-1\right)\right) \\  & =24\end{aligned}
$$

## Authored/default hard — reciprocal

Find the volume bounded by the region $R,$ given by

$$
R=\big\{(x,y,z)\, :\, 1\le y\le 4,\quad -1\le x + \sqrt{y}\le 1,\quad 1\le \frac{1}{z - 3}\le 4\big\}.
$$

 - $126$

 - $\frac{3}{2}$

 - $\frac{45}{8}$

 - $\frac{9}{2}$

 - $18$

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
1\le y\le 4,\quad -1\le x + \sqrt{y}\le 1,\quad 1\le \frac{1}{z - 3}\le 4,
$$

suggest that we use the change of variables

$$
u=y,\quad v=x + \sqrt{y},\quad w=\frac{1}{z - 3}.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y,z)\longmapsto(u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
\Delta=\big\{(u,v,w):1\le u\le 4,\quad -1\le v\le 1,\quad 1\le w\le 4\big\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}0 & 1 & 0 \\ 1 & \frac{1}{2 \sqrt{y}} & 0 \\ 0 & 0 & - \frac{1}{\left(z - 3\right)^{2}}\end{vmatrix} \\  & =\left(0\right)(-1)^{1+1}\begin{vmatrix}\frac{1}{2 \sqrt{y}} & 0 \\ 0 & - \frac{1}{\left(z - 3\right)^{2}}\end{vmatrix}+\left(1\right)(-1)^{1+2}\begin{vmatrix}1 & 0 \\ 0 & - \frac{1}{\left(z - 3\right)^{2}}\end{vmatrix}+\left(0\right)(-1)^{1+3}\begin{vmatrix}1 & \frac{1}{2 \sqrt{y}} \\ 0 & 0\end{vmatrix} \\  & =\frac{1}{\left(z - 3\right)^{2}} \\  & =w^{2}\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=\frac{1}{w^{2}}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

The map to $R$ is

$$
T(u,v,w)=\left(- \sqrt{u} + v,u,3 + \frac{1}{w}\right).
$$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R\mathrm{d}V & =\iiint_\Delta 1\cdot |\frac{1}{w^{2}}|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{1}^{4}\int_{-1}^{1}\int_{1}^{4}\frac{1}{w^{2}}\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =1\cdot \int_{1}^{4}1\,\mathrm{d}u\cdot \int_{-1}^{1}1\,\mathrm{d}v\cdot \int_{1}^{4}\frac{1}{w^{2}}\,\mathrm{d}w \\  & =1\cdot [u]_{1}^{4}\cdot [v]_{-1}^{1}\cdot [- \frac{1}{w}]_{1}^{4} \\  & =1\cdot \left(\left(\left(4\right)\right)-\left(\left(1\right)\right)\right)\cdot \left(\left(\left(1\right)\right)-\left(\left(-1\right)\right)\right)\cdot \left(\left(- \frac{1}{\left(4\right)}\right)-\left(- \frac{1}{\left(1\right)}\right)\right) \\  & =1\cdot \left(\left(4\right)-\left(1\right)\right)\cdot \left(\left(1\right)-\left(-1\right)\right)\cdot \left(\left(- \frac{1}{4}\right)-\left(-1\right)\right) \\  & =\frac{9}{2}\end{aligned}
$$

## Authored/default hard — cube

Find the volume bounded by the region $R,$ given by

$$
R=\big\{(x,y,z)\, :\, 1\le - 2 x - y\le 7,\quad -1\le - 2 x - 3 y\le 2,\quad 1\le z^{3}\le 8\big\}.
$$

 - $\frac{27}{2}$

 - $126$

 - $\frac{9}{2}$

 - $\frac{3}{4}$

 - $18$

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
1\le - 2 x - y\le 7,\quad -1\le - 2 x - 3 y\le 2,\quad 1\le z^{3}\le 8,
$$

suggest that we use the change of variables

$$
u=- 2 x - y,\quad v=- 2 x - 3 y,\quad w=z^{3}.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y,z)\longmapsto(u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
\Delta=\big\{(u,v,w):1\le u\le 7,\quad -1\le v\le 2,\quad 1\le w\le 8\big\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}-2 & -1 & 0 \\ -2 & -3 & 0 \\ 0 & 0 & 3 z^{2}\end{vmatrix} \\  & =\left(-2\right)(-1)^{1+1}\begin{vmatrix}-3 & 0 \\ 0 & 3 z^{2}\end{vmatrix}+\left(-1\right)(-1)^{1+2}\begin{vmatrix}-2 & 0 \\ 0 & 3 z^{2}\end{vmatrix}+\left(0\right)(-1)^{1+3}\begin{vmatrix}-2 & -3 \\ 0 & 0\end{vmatrix} \\  & =12 z^{2} \\  & =12 w^{\frac{2}{3}}\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=\frac{1}{12 w^{\frac{2}{3}}}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

The map to $R$ is

$$
T(u,v,w)=\left(- \frac{3 u}{4} + \frac{v}{4},\frac{u}{2} - \frac{v}{2},\sqrt[3]{w}\right).
$$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R\mathrm{d}V & =\iiint_\Delta 1\cdot |\frac{1}{12 w^{\frac{2}{3}}}|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{1}^{7}\int_{-1}^{2}\int_{1}^{8}\frac{1}{12 w^{\frac{2}{3}}}\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =1\cdot \int_{1}^{7}1\,\mathrm{d}u\cdot \int_{-1}^{2}1\,\mathrm{d}v\cdot \int_{1}^{8}\frac{1}{12 w^{\frac{2}{3}}}\,\mathrm{d}w \\  & =1\cdot [u]_{1}^{7}\cdot [v]_{-1}^{2}\cdot [\frac{\sqrt[3]{w}}{4}]_{1}^{8} \\  & =1\cdot \left(\left(\left(7\right)\right)-\left(\left(1\right)\right)\right)\cdot \left(\left(\left(2\right)\right)-\left(\left(-1\right)\right)\right)\cdot \left(\left(\frac{\sqrt[3]{\left(8\right)}}{4}\right)-\left(\frac{\sqrt[3]{\left(1\right)}}{4}\right)\right) \\  & =1\cdot \left(\left(7\right)-\left(1\right)\right)\cdot \left(\left(2\right)-\left(-1\right)\right)\cdot \left(\left(\frac{1}{2}\right)-\left(\frac{1}{4}\right)\right) \\  & =\frac{9}{2}\end{aligned}
$$

## Authored/default hard — cube

Find the volume bounded by the region $R,$ given by

$$
R=\big\{(x,y,z)\, :\, 2\le - 3 x + y\le 5,\quad -1\le x + y\le 1,\quad 1\le z^{3}\le 8\big\}.
$$

 - $\frac{9}{2}$

 - $6$

 - $\frac{1}{2}$

 - $\frac{3}{2}$

 - $42$

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
2\le - 3 x + y\le 5,\quad -1\le x + y\le 1,\quad 1\le z^{3}\le 8,
$$

suggest that we use the change of variables

$$
u=- 3 x + y,\quad v=x + y,\quad w=z^{3}.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
T^{-1}:(x,y,z)\longmapsto(u(x,y,z),v(x,y,z),w(x,y,z)).
$$

To compute the required volume, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$

Our domain in the $uvw$-space is

$$
\Delta=\big\{(u,v,w):2\le u\le 5,\quad -1\le v\le 1,\quad 1\le w\le 8\big\}.
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)} & =\begin{vmatrix}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{vmatrix} \\  & =\begin{vmatrix}-3 & 1 & 0 \\ 1 & 1 & 0 \\ 0 & 0 & 3 z^{2}\end{vmatrix} \\  & =\left(-3\right)(-1)^{1+1}\begin{vmatrix}1 & 0 \\ 0 & 3 z^{2}\end{vmatrix}+\left(1\right)(-1)^{1+2}\begin{vmatrix}1 & 0 \\ 0 & 3 z^{2}\end{vmatrix}+\left(0\right)(-1)^{1+3}\begin{vmatrix}1 & 1 \\ 0 & 0\end{vmatrix} \\  & =- 12 z^{2} \\  & =- 12 w^{\frac{2}{3}}\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}=- \frac{1}{12 w^{\frac{2}{3}}}.
$$

Note that $\frac{∂(x,y,z)}{∂(u,v,w)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

The map to $R$ is

$$
T(u,v,w)=\left(- \frac{u}{4} + \frac{v}{4},\frac{u}{4} + \frac{3 v}{4},\sqrt[3]{w}\right).
$$

**Step 4**: Perform the change of variables:

$$
\begin{aligned}\iiint_R\mathrm{d}V & =\iiint_\Delta 1\cdot |- \frac{1}{12 w^{\frac{2}{3}}}|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w \\  & =\int_{2}^{5}\int_{-1}^{1}\int_{1}^{8}\frac{1}{12 w^{\frac{2}{3}}}\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u \\  & =1\cdot \int_{2}^{5}1\,\mathrm{d}u\cdot \int_{-1}^{1}1\,\mathrm{d}v\cdot \int_{1}^{8}\frac{1}{12 w^{\frac{2}{3}}}\,\mathrm{d}w \\  & =1\cdot [u]_{2}^{5}\cdot [v]_{-1}^{1}\cdot [\frac{\sqrt[3]{w}}{4}]_{1}^{8} \\  & =1\cdot \left(\left(\left(5\right)\right)-\left(\left(2\right)\right)\right)\cdot \left(\left(\left(1\right)\right)-\left(\left(-1\right)\right)\right)\cdot \left(\left(\frac{\sqrt[3]{\left(8\right)}}{4}\right)-\left(\frac{\sqrt[3]{\left(1\right)}}{4}\right)\right) \\  & =1\cdot \left(\left(5\right)-\left(2\right)\right)\cdot \left(\left(1\right)-\left(-1\right)\right)\cdot \left(\left(\frac{1}{2}\right)-\left(\frac{1}{4}\right)\right) \\  & =\frac{3}{2}\end{aligned}
$$
