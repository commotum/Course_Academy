# Originals and generated variants

Database math, basis 1356. Raw originals are ineligible evidence. Generated variants use authored method banks.

## Original q-38377

Use a change of variables to evaluate the double integral 

$$
{∬}_{D}\frac{1}{1+(x-y)^{2}}\,dxdy,
$$

where $D={(x,y)\,:\,0\le x\le 2,\,0\le x-y\le 2}.$

- $\arctan (4) - \arctan (2)$

- $\ln (2) + \arctan (2)$

- $2\arctan (2)$

- $2 - 2\arctan (2)$

- $\arctan (2)$

- $2\operatorname{arctan}⁡(2)$

- $\operatorname{arctan}⁡(4)-\operatorname{arctan}⁡(2)$

- $2-2\operatorname{arctan}⁡(2)$

- $\operatorname{arctan}⁡(2)$

- $\operatorname{ln}⁡(2)+\operatorname{arctan}⁡(2)$

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

The inequalities that define the region $D,$

$$
0\le x\le 2,\,0\le x-y\le 2,
$$

suggest that we use the change of variables 

$$
u=x\,\text{and}\,v=x-y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,0\le u\le 2,\,0\le v\le 2}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}1 & \text{ }\text{ }0 \\ 1 & -1\end{aligned}| \\  & =-1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=-1.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}\frac{1}{1+(x-y)^{2}}\,\text{d}x\text{d}y & ={∬}_{Δ}\frac{1}{1+{v}^{2}}\,|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}\frac{1}{1+{v}^{2}}\,|-1|\,\text{d}u\text{d}v \\  & ={\int }_{0}^{2}[{\int }_{0}^{2}\frac{1}{1+{v}^{2}}\,du]dv \\  & ={\int }_{0}^{2}\frac{1}{1+{v}^{2}}[{\int }_{0}^{2}du]dv \\  & ={\int }_{0}^{2}\frac{1}{1+{v}^{2}}[u]_{0}^{2}\,dv \\  & =2{\int }_{0}^{2}\frac{1}{1+{v}^{2}}\,dv \\  & =2[\operatorname{arctan}⁡v]_{0}^{2} \\  & =2\operatorname{arctan}⁡(2).\end{aligned}
$$

## Original q-82916

Use a change of variables to evaluate the double integral
$∬_(D)(x + 2y)e^{(x + 2y)^{2}}dxdy$,
where $D = {(x, y): 1 \le x \le 5, 0 \le x + 2y \le 1}$.

- $\frac{e^{2} - e}{4}$

- $e^{2} - 1$

- $\frac{e - 2}{2}$

- $e$

- $e - 1$

## Original q-160911

Use a change of variables to evaluate the double integral 

$$
{∬}_{D}(x-1){e}^{2x+2y}\,dxdy,
$$

where $D={(x,y)\,:\,1\le x\le 3,\,-1\le x+y\le 1}.$

- ${e}^{2}-{e}^{-2}$

- $\frac{2({e}^{2}-{e}^{-2})}{3}$

- $2(e-{e}^{-1})$

- $3({e}^{2}-1)$

- $1-{e}^{-2}$

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

The inequalities that define the region $D,$

$$
1\le x\le 3,\,-1\le x+y\le 1,
$$

suggest that we use the change of variables 

$$
u=x\,\text{and}\,v=x+y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,1\le u\le 3,\,-1\le v\le 1}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}1 & 0 \\ 1 & 1\end{aligned}| \\  & =1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=1.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}(x-1){e}^{2x+2y}\,\text{d}x\text{d}y & ={∬}_{Δ}(u-1){e}^{2v}|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\text{d}v \\  & ={∬}_{Δ}(u-1){e}^{2v}|1|\text{d}u\text{d}v \\  & ={\int }_{1}^{3}(u-1)[{\int }_{-1}^{1}{e}^{2v}\,dv]du \\  & ={\int }_{1}^{3}(u-1){[\frac{1}{2}{e}^{2v}]}_{-1}^{1}\,dv \\  & =\frac{{e}^{2}-{e}^{-2}}{2}{\int }_{1}^{3}(u-1)\,dv \\  & =\frac{{e}^{2}-{e}^{-2}}{2}{[\frac{1}{2}{u}^{2}-u]}_{1}^{3} \\  & =\frac{{e}^{2}-{e}^{-2}}{2}\cdot 2 \\  & ={e}^{2}-{e}^{-2}.\end{aligned}
$$

## Original q-160919

Use a change of variables to evaluate the double integral 

$$
{∬}_{D}x{y}^{2}\,dxdy,
$$

where $D={(x,y)\,:\,0\le \frac{x}{\sqrt{4-{y}^{2}}}\le 1,\,-1\le y\le 1}.$

- $\frac{17}{15}$

- $\frac{23}{12}$

- $\frac{25}{18}$

- $\frac{13}{10}$

- $\frac{19}{14}$

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

The inequalities that define the region $D,$

$$
0\le \frac{x}{\sqrt{4-{y}^{2}}}\le 1,\,-1\le y\le 1,
$$

suggest that we use the change of variables 

$$
u=\frac{x}{\sqrt{4-{y}^{2}}}\,\text{and}\,v=y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,0\le u\le 1,\,-1\le v\le 1}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}\frac{1}{\sqrt{4-{y}^{2}}} & \frac{xy}{\sqrt{{(4-{y}^{2})}^{3}}} \\ 0 & 1\end{aligned}| \\  & =\frac{1}{\sqrt{4-{y}^{2}}}.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\sqrt{4-{y}^{2}}=\sqrt{4-{v}^{2}}
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}x{y}^{2}\,\text{d}x\text{d}y & ={∬}_{Δ}u\sqrt{4-{v}^{2}}\cdot {v}^{2}\,|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}u\sqrt{4-{v}^{2}}\cdot {v}^{2}\cdot |\sqrt{4-{v}^{2}}|\text{d}u\text{d}v \\  & ={∬}_{Δ}u{v}^{2}(4-{v}^{2})\,\text{d}u\text{d}v \\  & ={\int }_{0}^{1}u[{\int }_{-1}^{1}(4{v}^{2}-{v}^{4})\,dv]du \\  & ={\int }_{0}^{1}u\cdot {[\frac{4}{3}{v}^{3}-\frac{1}{5}{v}^{5}]}_{-1}^{1}\,du \\  & ={\int }_{0}^{1}u\cdot \frac{34}{15}\,du \\  & =\frac{34}{15}{[\frac{1}{2}{u}^{2}]}_{0}^{1} \\  & =\frac{17}{15}\cdot (1-0) \\  & =\frac{17}{15}.\end{aligned}
$$

## Original q-160920

Use a change of variables to evaluate the double integral 

$$
{∬}_{D}{e}^{{x}^{2}+x+y}\,dxdy,
$$

where $D={(x,y)\,:\,0\le x\le 1,\,0\le y+{x}^{2}\le 2}.$

- $2{e}^{2}-3$

- $4{e}^{3}-1$

- $2{e}^{4}-{e}^{2}+2$

- ${e}^{3}-e+1$

- ${e}^{3}-{e}^{2}-e+1$

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

The inequalities that define the region $D,$

$$
0\le x\le 1,\,0\le y+{x}^{2}\le 2,
$$

suggest that we use the change of variables 

$$
u=x\,\text{and}\,v=y+{x}^{2}.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,0\le u\le 1,\,0\le v\le 2}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}1 & 0 \\ 2x & 1\end{aligned}| \\  & =1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=1
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}{e}^{{x}^{2}+x+y}\,\text{d}x\text{d}y & ={∬}_{D}{e}^{x+(y+{x}^{2})}\text{d}x\text{d}y \\  & ={∬}_{Δ}{e}^{u+v}|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\text{d}v \\  & ={∬}_{Δ}{e}^{u+v}\cdot |1|\text{d}u\text{d}v \\  & ={\int }_{0}^{1}[{\int }_{0}^{2}{e}^{u+v}\,dv]du \\  & ={\int }_{0}^{1}{e}^{u}[{\int }_{0}^{2}{e}^{v}\,dv]du \\  & ={\int }_{0}^{1}{e}^{u}[{e}^{v}]_{0}^{2}\,du \\  & =({e}^{2}-1){\int }_{0}^{1}{e}^{u}\,du \\  & =({e}^{2}-1)[{e}^{u}]_{0}^{1} \\  & =({e}^{2}-1)(e-1) \\  & ={e}^{3}-{e}^{2}-e+1.\end{aligned}
$$

## Original q-83651

Use a change of variables to evaluate the double integral 

$$
{∬}_{D}x\operatorname{sin}⁡(x+y)\,dxdy,
$$

where $D={(x,y)\,:\,1\le x\le 3,\,|x+y|\le \frac{\pi }{2}}.$

- $-4$

- $0$

- $4$

- $-6$

- $8$

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

The inequalities that define the region $D,$

$$
1\le x\le 3,\,-\frac{\pi }{2}\le x+y\le \frac{\pi }{2},
$$

suggest that we use the change of variables 

$$
u=x\,\text{and}\,v=x+y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,1\le u\le 3,\,-\frac{\pi }{2}\le v\le \frac{\pi }{2}}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}1 & \text{ }\text{ }0 \\ 1 & 1\end{aligned}| \\  & =1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=1.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}x\operatorname{sin}⁡(x+y)\,\text{d}x\text{d}y & ={∬}_{Δ}u\operatorname{sin}⁡v\,|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}u\operatorname{sin}⁡v\,|1|\,\text{d}u\text{d}v \\  & ={\int }_{-\pi /2}^{\pi /2}\operatorname{sin}⁡v[{\int }_{1}^{3}u\,du]dv \\  & ={\int }_{-\pi /2}^{\pi /2}\operatorname{sin}⁡v{[\frac{{u}^{2}}{2}]}_{1}^{3}dv \\  & =4{\int }_{-\pi /2}^{\pi /2}\operatorname{sin}⁡v\,dv \\  & =4[-\operatorname{cos}⁡v]_{-\pi /2}^{\pi /2} \\  & =0.\end{aligned}
$$

## Generated homogeneous source evidence k=2 / q-38377

Use a change of variables to evaluate the double integral 

$$
{∬}_{D}2\left(\frac{1}{1+(x-y)^{2}}\right)\,dxdy,
$$

where $D={(x,y)\,:\,0\le x\le 2,\,0\le x-y\le 2}.$

- $2\left(2\arctan (2)\right)$

- $2\left(\arctan (4) - \arctan (2)\right)$

- $2\left(\arctan (2)\right)$

- $2\left(2 - 2\arctan (2)\right)$

- $2\left(\ln (2) + \arctan (2)\right)$

- $2\left(2-2\operatorname{arctan}⁡(2)\right)$

- $2\left(\operatorname{arctan}⁡(4)-\operatorname{arctan}⁡(2)\right)$

- $2\left(2\operatorname{arctan}⁡(2)\right)$

- $2\left(\operatorname{arctan}⁡(2)\right)$

- $2\left(\operatorname{ln}⁡(2)+\operatorname{arctan}⁡(2)\right)$

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

The inequalities that define the region $D,$

$$
0\le x\le 2,\,0\le x-y\le 2,
$$

suggest that we use the change of variables 

$$
u=x\,\text{and}\,v=x-y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,0\le u\le 2,\,0\le v\le 2}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}1 & \text{ }\text{ }0 \\ 1 & -1\end{aligned}| \\  & =-1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=-1.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}2\left({∬}_{D}\frac{1}{1+(x-y)^{2}}\,\text{d}x\text{d}y\right) & =2\left({∬}_{Δ}\frac{1}{1+{v}^{2}}\,|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v\right) \\  & =2\left({∬}_{Δ}\frac{1}{1+{v}^{2}}\,|-1|\,\text{d}u\text{d}v\right) \\  & =2\left({\int }_{0}^{2}[{\int }_{0}^{2}\frac{1}{1+{v}^{2}}\,du]dv\right) \\  & =2\left({\int }_{0}^{2}\frac{1}{1+{v}^{2}}[{\int }_{0}^{2}du]dv\right) \\  & =2\left({\int }_{0}^{2}\frac{1}{1+{v}^{2}}[u]_{0}^{2}\,dv\right) \\  & =2\left(2{\int }_{0}^{2}\frac{1}{1+{v}^{2}}\,dv\right) \\  & =2\left(2[\operatorname{arctan}⁡v]_{0}^{2}\right) \\  & =2\left(2\operatorname{arctan}⁡(2).\right)\end{aligned}
$$

## Generated homogeneous source evidence k=2 / q-82916

Use a change of variables to evaluate the double integral
$∬_(D)2\left((x + 2y)e^{(x + 2y)^{2}}\right)dxdy$,
where $D = {(x, y): 1 \le x \le 5, 0 \le x + 2y \le 1}$.

- $2\left(\frac{e - 2}{2}\right)$

- $2\left(\frac{e^{2} - e}{4}\right)$

- $2\left(e - 1\right)$

- $2\left(e\right)$

- $2\left(e^{2} - 1\right)$

## Generated homogeneous source evidence k=2 / q-160911

Use a change of variables to evaluate the double integral 

$$
{∬}_{D}2\left((x-1){e}^{2x+2y}\right)\,dxdy,
$$

where $D={(x,y)\,:\,1\le x\le 3,\,-1\le x+y\le 1}.$

- $2\left(2(e-{e}^{-1})\right)$

- $2\left({e}^{2}-{e}^{-2}\right)$

- $2\left(1-{e}^{-2}\right)$

- $2\left(3({e}^{2}-1)\right)$

- $2\left(\frac{2({e}^{2}-{e}^{-2})}{3}\right)$

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

The inequalities that define the region $D,$

$$
1\le x\le 3,\,-1\le x+y\le 1,
$$

suggest that we use the change of variables 

$$
u=x\,\text{and}\,v=x+y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,1\le u\le 3,\,-1\le v\le 1}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}1 & 0 \\ 1 & 1\end{aligned}| \\  & =1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=1.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}2\left({∬}_{D}(x-1){e}^{2x+2y}\,\text{d}x\text{d}y\right) & =2\left({∬}_{Δ}(u-1){e}^{2v}|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\text{d}v\right) \\  & =2\left({∬}_{Δ}(u-1){e}^{2v}|1|\text{d}u\text{d}v\right) \\  & =2\left({\int }_{1}^{3}(u-1)[{\int }_{-1}^{1}{e}^{2v}\,dv]du\right) \\  & =2\left({\int }_{1}^{3}(u-1){[\frac{1}{2}{e}^{2v}]}_{-1}^{1}\,dv\right) \\  & =2\left(\frac{{e}^{2}-{e}^{-2}}{2}{\int }_{1}^{3}(u-1)\,dv\right) \\  & =2\left(\frac{{e}^{2}-{e}^{-2}}{2}{[\frac{1}{2}{u}^{2}-u]}_{1}^{3}\right) \\  & =2\left(\frac{{e}^{2}-{e}^{-2}}{2}\cdot 2\right) \\  & =2\left({e}^{2}-{e}^{-2}.\right)\end{aligned}
$$

## Generated homogeneous source evidence k=2 / q-160919

Use a change of variables to evaluate the double integral 

$$
{∬}_{D}2\left(x{y}^{2}\right)\,dxdy,
$$

where $D={(x,y)\,:\,0\le \frac{x}{\sqrt{4-{y}^{2}}}\le 1,\,-1\le y\le 1}.$

- $2\left(\frac{25}{18}\right)$

- $2\left(\frac{17}{15}\right)$

- $2\left(\frac{19}{14}\right)$

- $2\left(\frac{13}{10}\right)$

- $2\left(\frac{23}{12}\right)$

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

The inequalities that define the region $D,$

$$
0\le \frac{x}{\sqrt{4-{y}^{2}}}\le 1,\,-1\le y\le 1,
$$

suggest that we use the change of variables 

$$
u=\frac{x}{\sqrt{4-{y}^{2}}}\,\text{and}\,v=y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,0\le u\le 1,\,-1\le v\le 1}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}\frac{1}{\sqrt{4-{y}^{2}}} & \frac{xy}{\sqrt{{(4-{y}^{2})}^{3}}} \\ 0 & 1\end{aligned}| \\  & =\frac{1}{\sqrt{4-{y}^{2}}}.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\sqrt{4-{y}^{2}}=\sqrt{4-{v}^{2}}
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}2\left({∬}_{D}x{y}^{2}\,\text{d}x\text{d}y\right) & =2\left({∬}_{Δ}u\sqrt{4-{v}^{2}}\cdot {v}^{2}\,|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v\right) \\  & =2\left({∬}_{Δ}u\sqrt{4-{v}^{2}}\cdot {v}^{2}\cdot |\sqrt{4-{v}^{2}}|\text{d}u\text{d}v\right) \\  & =2\left({∬}_{Δ}u{v}^{2}(4-{v}^{2})\,\text{d}u\text{d}v\right) \\  & =2\left({\int }_{0}^{1}u[{\int }_{-1}^{1}(4{v}^{2}-{v}^{4})\,dv]du\right) \\  & =2\left({\int }_{0}^{1}u\cdot {[\frac{4}{3}{v}^{3}-\frac{1}{5}{v}^{5}]}_{-1}^{1}\,du\right) \\  & =2\left({\int }_{0}^{1}u\cdot \frac{34}{15}\,du\right) \\  & =2\left(\frac{34}{15}{[\frac{1}{2}{u}^{2}]}_{0}^{1}\right) \\  & =2\left(\frac{17}{15}\cdot (1-0)\right) \\  & =2\left(\frac{17}{15}.\right)\end{aligned}
$$

## Generated homogeneous source evidence k=2 / q-160920

Use a change of variables to evaluate the double integral 

$$
{∬}_{D}2\left({e}^{{x}^{2}+x+y}\right)\,dxdy,
$$

where $D={(x,y)\,:\,0\le x\le 1,\,0\le y+{x}^{2}\le 2}.$

- $2\left(2{e}^{4}-{e}^{2}+2\right)$

- $2\left(2{e}^{2}-3\right)$

- $2\left({e}^{3}-{e}^{2}-e+1\right)$

- $2\left({e}^{3}-e+1\right)$

- $2\left(4{e}^{3}-1\right)$

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

The inequalities that define the region $D,$

$$
0\le x\le 1,\,0\le y+{x}^{2}\le 2,
$$

suggest that we use the change of variables 

$$
u=x\,\text{and}\,v=y+{x}^{2}.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,0\le u\le 1,\,0\le v\le 2}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}1 & 0 \\ 2x & 1\end{aligned}| \\  & =1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=1
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}2\left({∬}_{D}{e}^{{x}^{2}+x+y}\,\text{d}x\text{d}y\right) & =2\left({∬}_{D}{e}^{x+(y+{x}^{2})}\text{d}x\text{d}y\right) \\  & =2\left({∬}_{Δ}{e}^{u+v}|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\text{d}v\right) \\  & =2\left({∬}_{Δ}{e}^{u+v}\cdot |1|\text{d}u\text{d}v\right) \\  & =2\left({\int }_{0}^{1}[{\int }_{0}^{2}{e}^{u+v}\,dv]du\right) \\  & =2\left({\int }_{0}^{1}{e}^{u}[{\int }_{0}^{2}{e}^{v}\,dv]du\right) \\  & =2\left({\int }_{0}^{1}{e}^{u}[{e}^{v}]_{0}^{2}\,du\right) \\  & =2\left(({e}^{2}-1){\int }_{0}^{1}{e}^{u}\,du\right) \\  & =2\left(({e}^{2}-1)[{e}^{u}]_{0}^{1}\right) \\  & =2\left(({e}^{2}-1)(e-1)\right) \\  & =2\left({e}^{3}-{e}^{2}-e+1.\right)\end{aligned}
$$

## Generated homogeneous source evidence k=2 / q-83651

Use a change of variables to evaluate the double integral 

$$
{∬}_{D}2\left(x\operatorname{sin}⁡(x+y)\right)\,dxdy,
$$

where $D={(x,y)\,:\,1\le x\le 3,\,|x+y|\le \frac{\pi }{2}}.$

- $2\left(4\right)$

- $2\left(-4\right)$

- $2\left(8\right)$

- $2\left(-6\right)$

- $2\left(0\right)$

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

The inequalities that define the region $D,$

$$
1\le x\le 3,\,-\frac{\pi }{2}\le x+y\le \frac{\pi }{2},
$$

suggest that we use the change of variables 

$$
u=x\,\text{and}\,v=x+y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,1\le u\le 3,\,-\frac{\pi }{2}\le v\le \frac{\pi }{2}}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}1 & \text{ }\text{ }0 \\ 1 & 1\end{aligned}| \\  & =1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=1.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}2\left({∬}_{D}x\operatorname{sin}⁡(x+y)\,\text{d}x\text{d}y\right) & =2\left({∬}_{Δ}u\operatorname{sin}⁡v\,|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v\right) \\  & =2\left({∬}_{Δ}u\operatorname{sin}⁡v\,|1|\,\text{d}u\text{d}v\right) \\  & =2\left({\int }_{-\pi /2}^{\pi /2}\operatorname{sin}⁡v[{\int }_{1}^{3}u\,du]dv\right) \\  & =2\left({\int }_{-\pi /2}^{\pi /2}\operatorname{sin}⁡v{[\frac{{u}^{2}}{2}]}_{1}^{3}dv\right) \\  & =2\left(4{\int }_{-\pi /2}^{\pi /2}\operatorname{sin}⁡v\,dv\right) \\  & =2\left(4[-\operatorname{cos}⁡v]_{-\pi /2}^{\pi /2}\right) \\  & =2\left(0.\right)\end{aligned}
$$

## Generated easy / linear

Use a change of variables to evaluate the double integral

$$
\iint_D x + y\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):0\le x\le 8,\quad 0\le x + y\le 5\}.$

- $-100$

- $\frac{25}{2}$

- $100$

- $200$

- $20$

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

The inequalities that define the region $D,$

$$
0\le x\le 8,\quad 0\le x + y\le 5,
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x + y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):0\le u\le 8,\,0\le v\le 5\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\1 & 1\end{matrix}\right]\right|\\&=1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=1=1.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=- u + v$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D x + y\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta v\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(v\right)\cdot \left(1\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =1\int_{0}^{5} [\int_{0}^{8} v\,\mathrm{d}u]\,\mathrm{d}v \\ & =1\int_{0}^{5} v[\int_{0}^{8} 1\,\mathrm{d}u]\,\mathrm{d}v \\ & =1\int_{0}^{5} v\left[u\right]_{0}^{8}\,\mathrm{d}v \\ & =1\int_{0}^{5} v\left(\left(8\right)-(\left(0\right))\right)\,\mathrm{d}v \\ & =\left(1\right)\cdot \left(8\right)\int_{0}^{5} v\,\mathrm{d}v \\ & =\left(1\right)\cdot \left(8\right)\left[\frac{v^{2}}{2}\right]_{0}^{5} \\ & =\left(1\right)\cdot \left(8\right)\left(\left(\frac{25}{2}\right)-(\left(0\right))\right) \\ & =\left(1\right)\cdot \left(8\right)\cdot \left(\frac{25}{2}\right) \\ & =100\end{aligned}
$$

## Generated easy / linear

Use a change of variables to evaluate the double integral

$$
\iint_D x + y\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):0\le x\le 3,\quad 0\le x + y\le 6\}.$

- $-54$

- $9$

- $108$

- $54$

- $18$

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

The inequalities that define the region $D,$

$$
0\le x\le 3,\quad 0\le x + y\le 6,
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x + y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):0\le u\le 3,\,0\le v\le 6\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\1 & 1\end{matrix}\right]\right|\\&=1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=1=1.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=- u + v$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D x + y\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta v\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(v\right)\cdot \left(1\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =1\int_{0}^{6} [\int_{0}^{3} v\,\mathrm{d}u]\,\mathrm{d}v \\ & =1\int_{0}^{6} v[\int_{0}^{3} 1\,\mathrm{d}u]\,\mathrm{d}v \\ & =1\int_{0}^{6} v\left[u\right]_{0}^{3}\,\mathrm{d}v \\ & =1\int_{0}^{6} v\left(\left(3\right)-(\left(0\right))\right)\,\mathrm{d}v \\ & =\left(1\right)\cdot \left(3\right)\int_{0}^{6} v\,\mathrm{d}v \\ & =\left(1\right)\cdot \left(3\right)\left[\frac{v^{2}}{2}\right]_{0}^{6} \\ & =\left(1\right)\cdot \left(3\right)\left(\left(18\right)-(\left(0\right))\right) \\ & =\left(1\right)\cdot \left(3\right)\cdot \left(18\right) \\ & =54\end{aligned}
$$

## Generated moderate / arctan

Use a change of variables to evaluate the double integral

$$
\iint_D \frac{1}{\left(x - y\right)^{2} + 1}\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):0\le x\le 5,\quad 0\le x - y\le 4\}.$

- $- 5 \arctan{\left(4 \right)}$

- $\arctan{\left(4 \right)}$

- $5 \arctan{\left(4 \right)}$

- $\frac{20}{17}$

- $5 \arctan{\left(16 \right)}$

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

The inequalities that define the region $D,$

$$
0\le x\le 5,\quad 0\le x - y\le 4,
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x - y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):0\le u\le 5,\,0\le v\le 4\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\1 & -1\end{matrix}\right]\right|\\&=-1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=-1=-1.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=u - v$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D \frac{1}{\left(x - y\right)^{2} + 1}\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta \frac{1}{v^{2} + 1}\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(\frac{1}{v^{2} + 1}\right)\cdot \left(1\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =1\int_{0}^{4} [\int_{0}^{5} \frac{1}{v^{2} + 1}\,\mathrm{d}u]\,\mathrm{d}v \\ & =1\int_{0}^{4} \frac{1}{v^{2} + 1}[\int_{0}^{5} 1\,\mathrm{d}u]\,\mathrm{d}v \\ & =1\int_{0}^{4} \frac{1}{v^{2} + 1}\left[u\right]_{0}^{5}\,\mathrm{d}v \\ & =1\int_{0}^{4} \frac{1}{v^{2} + 1}\left(\left(5\right)-(\left(0\right))\right)\,\mathrm{d}v \\ & =\left(1\right)\cdot \left(5\right)\int_{0}^{4} \frac{1}{v^{2} + 1}\,\mathrm{d}v \\ & =\left(1\right)\cdot \left(5\right)\left[\arctan{\left(v \right)}\right]_{0}^{4} \\ & =\left(1\right)\cdot \left(5\right)\left(\left(\arctan{\left(4 \right)}\right)-(\left(0\right))\right) \\ & =\left(1\right)\cdot \left(5\right)\cdot \left(\arctan{\left(4 \right)}\right) \\ & =5 \arctan{\left(4 \right)}\end{aligned}
$$

## Generated moderate / arctan

Use a change of variables to evaluate the double integral

$$
\iint_D \frac{1}{\left(x - y\right)^{2} + 1}\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):0\le x\le 8,\quad 0\le x - y\le 5\}.$

- $- 8 \arctan{\left(5 \right)}$

- $8 \arctan{\left(25 \right)}$

- $\frac{20}{13}$

- $8 \arctan{\left(5 \right)}$

- $\arctan{\left(5 \right)}$

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

The inequalities that define the region $D,$

$$
0\le x\le 8,\quad 0\le x - y\le 5,
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x - y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):0\le u\le 8,\,0\le v\le 5\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\1 & -1\end{matrix}\right]\right|\\&=-1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=-1=-1.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=u - v$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D \frac{1}{\left(x - y\right)^{2} + 1}\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta \frac{1}{v^{2} + 1}\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(\frac{1}{v^{2} + 1}\right)\cdot \left(1\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =1\int_{0}^{5} [\int_{0}^{8} \frac{1}{v^{2} + 1}\,\mathrm{d}u]\,\mathrm{d}v \\ & =1\int_{0}^{5} \frac{1}{v^{2} + 1}[\int_{0}^{8} 1\,\mathrm{d}u]\,\mathrm{d}v \\ & =1\int_{0}^{5} \frac{1}{v^{2} + 1}\left[u\right]_{0}^{8}\,\mathrm{d}v \\ & =1\int_{0}^{5} \frac{1}{v^{2} + 1}\left(\left(8\right)-(\left(0\right))\right)\,\mathrm{d}v \\ & =\left(1\right)\cdot \left(8\right)\int_{0}^{5} \frac{1}{v^{2} + 1}\,\mathrm{d}v \\ & =\left(1\right)\cdot \left(8\right)\left[\arctan{\left(v \right)}\right]_{0}^{5} \\ & =\left(1\right)\cdot \left(8\right)\left(\left(\arctan{\left(5 \right)}\right)-(\left(0\right))\right) \\ & =\left(1\right)\cdot \left(8\right)\cdot \left(\arctan{\left(5 \right)}\right) \\ & =8 \arctan{\left(5 \right)}\end{aligned}
$$

## Generated moderate / gaussian

Use a change of variables to evaluate the double integral

$$
\iint_D e^{\left(x + 2 y\right)^{2}} \left(x + 2 y\right)\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):2\le x\le 5,\quad 0\le x + 2 y\le 2\}.$

- $\frac{3 e^{2}}{4} - \frac{3}{4}$

- $\frac{3 e^{4}}{2} - \frac{3}{2}$

- $\frac{3 e^{4}}{4} - \frac{3}{4}$

- $\frac{3 e^{4}}{4}$

- $\frac{3 e^{4}}{4} + \frac{3}{4}$

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

The inequalities that define the region $D,$

$$
2\le x\le 5,\quad 0\le x + 2 y\le 2,
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x + 2 y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):2\le u\le 5,\,0\le v\le 2\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\1 & 2\end{matrix}\right]\right|\\&=2.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=\frac{1}{2}=\frac{1}{2}.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=- \frac{u}{2} + \frac{v}{2}$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D e^{\left(x + 2 y\right)^{2}} \left(x + 2 y\right)\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta e^{v^{2}} v\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(e^{v^{2}} v\right)\cdot \left(\frac{1}{2}\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =\frac{1}{2}\int_{0}^{2} [\int_{2}^{5} e^{v^{2}} v\,\mathrm{d}u]\,\mathrm{d}v \\ & =\frac{1}{2}\int_{0}^{2} e^{v^{2}} v[\int_{2}^{5} 1\,\mathrm{d}u]\,\mathrm{d}v \\ & =\frac{1}{2}\int_{0}^{2} e^{v^{2}} v\left[u\right]_{2}^{5}\,\mathrm{d}v \\ & =\frac{1}{2}\int_{0}^{2} e^{v^{2}} v\left(\left(5\right)-(\left(2\right))\right)\,\mathrm{d}v \\ & =\left(\frac{1}{2}\right)\cdot \left(3\right)\int_{0}^{2} e^{v^{2}} v\,\mathrm{d}v \\ & =\left(\frac{1}{2}\right)\cdot \left(3\right)\left[\frac{e^{v^{2}}}{2}\right]_{0}^{2} \\ & =\left(\frac{1}{2}\right)\cdot \left(3\right)\left(\left(\frac{e^{4}}{2}\right)-(\left(\frac{1}{2}\right))\right) \\ & =\left(\frac{1}{2}\right)\cdot \left(3\right)\cdot \left(\frac{e^{4}}{2} - \frac{1}{2}\right) \\ & =\frac{3 e^{4}}{4} - \frac{3}{4}\end{aligned}
$$

## Generated moderate / gaussian

Use a change of variables to evaluate the double integral

$$
\iint_D e^{\left(x + 2 y\right)^{2}} \left(x + 2 y\right)\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):1\le x\le 2,\quad 0\le x + 2 y\le 2\}.$

- $\frac{e^{2}}{4} - \frac{1}{4}$

- $\frac{e^{4}}{4} + \frac{1}{4}$

- $\frac{e^{4}}{4}$

- $\frac{e^{4}}{4} - \frac{1}{4}$

- $\frac{e^{4}}{2} - \frac{1}{2}$

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

The inequalities that define the region $D,$

$$
1\le x\le 2,\quad 0\le x + 2 y\le 2,
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x + 2 y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):1\le u\le 2,\,0\le v\le 2\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\1 & 2\end{matrix}\right]\right|\\&=2.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=\frac{1}{2}=\frac{1}{2}.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=- \frac{u}{2} + \frac{v}{2}$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D e^{\left(x + 2 y\right)^{2}} \left(x + 2 y\right)\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta e^{v^{2}} v\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(e^{v^{2}} v\right)\cdot \left(\frac{1}{2}\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =\frac{1}{2}\int_{0}^{2} [\int_{1}^{2} e^{v^{2}} v\,\mathrm{d}u]\,\mathrm{d}v \\ & =\frac{1}{2}\int_{0}^{2} e^{v^{2}} v[\int_{1}^{2} 1\,\mathrm{d}u]\,\mathrm{d}v \\ & =\frac{1}{2}\int_{0}^{2} e^{v^{2}} v\left[u\right]_{1}^{2}\,\mathrm{d}v \\ & =\frac{1}{2}\int_{0}^{2} e^{v^{2}} v\left(\left(2\right)-(\left(1\right))\right)\,\mathrm{d}v \\ & =\left(\frac{1}{2}\right)\cdot \left(1\right)\int_{0}^{2} e^{v^{2}} v\,\mathrm{d}v \\ & =\left(\frac{1}{2}\right)\cdot \left(1\right)\left[\frac{e^{v^{2}}}{2}\right]_{0}^{2} \\ & =\left(\frac{1}{2}\right)\cdot \left(1\right)\left(\left(\frac{e^{4}}{2}\right)-(\left(\frac{1}{2}\right))\right) \\ & =\left(\frac{1}{2}\right)\cdot \left(1\right)\cdot \left(\frac{e^{4}}{2} - \frac{1}{2}\right) \\ & =\frac{e^{4}}{4} - \frac{1}{4}\end{aligned}
$$

## Generated moderate / linear_exp

Use a change of variables to evaluate the double integral

$$
\iint_D e^{2 x + 2 y} \left(x - 2\right)\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):2\le x\le 6,\quad 0\le x + y\le 2\}.$

- $4 e^{4} + 4$

- $4 e^{4}$

- $4 e^{4} - 4$

- $16$

- $32 e^{4}$

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

The inequalities that define the region $D,$

$$
2\le x\le 6,\quad 0\le x + y\le 2,
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x + y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):2\le u\le 6,\,0\le v\le 2\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\1 & 1\end{matrix}\right]\right|\\&=1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=1=1.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=- u + v$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D e^{2 x + 2 y} \left(x - 2\right)\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta e^{2 v} \left(u - 2\right)\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(e^{2 v} \left(u - 2\right)\right)\cdot \left(1\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =1\int_{2}^{6} [\int_{0}^{2} e^{2 v} \left(u - 2\right)\,\mathrm{d}v]\,\mathrm{d}u \\ & =1\int_{2}^{6} \left(u - 2\right)[\int_{0}^{2} e^{2 v}\,\mathrm{d}v]\,\mathrm{d}u \\ & =1\int_{2}^{6} \left(u - 2\right)\left[\frac{e^{2 v}}{2}\right]_{0}^{2}\,\mathrm{d}u \\ & =1\int_{2}^{6} \left(u - 2\right)\left(\left(\frac{e^{4}}{2}\right)-(\left(\frac{1}{2}\right))\right)\,\mathrm{d}u \\ & =\left(1\right)\cdot \left(\frac{e^{4}}{2} - \frac{1}{2}\right)\int_{2}^{6} u - 2\,\mathrm{d}u \\ & =\left(1\right)\cdot \left(\frac{e^{4}}{2} - \frac{1}{2}\right)\left[\frac{u^{2}}{2} - 2 u\right]_{2}^{6} \\ & =\left(1\right)\cdot \left(\frac{e^{4}}{2} - \frac{1}{2}\right)\left(\left(18\right)+\left(-12\right)-(\left(2\right)+\left(-4\right))\right) \\ & =\left(1\right)\cdot \left(8\right)\cdot \left(\frac{e^{4}}{2} - \frac{1}{2}\right) \\ & =4 e^{4} - 4\end{aligned}
$$

## Generated moderate / linear_exp

Use a change of variables to evaluate the double integral

$$
\iint_D e^{2 x + 2 y} \left(x - 1\right)\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):1\le x\le 2,\quad 0\le x + y\le 2\}.$

- $\frac{e^{4}}{4} + \frac{1}{4}$

- $2 e^{4}$

- $1$

- $\frac{e^{4}}{4} - \frac{1}{4}$

- $\frac{e^{4}}{4}$

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

The inequalities that define the region $D,$

$$
1\le x\le 2,\quad 0\le x + y\le 2,
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x + y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):1\le u\le 2,\,0\le v\le 2\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\1 & 1\end{matrix}\right]\right|\\&=1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=1=1.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=- u + v$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D e^{2 x + 2 y} \left(x - 1\right)\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta e^{2 v} \left(u - 1\right)\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(e^{2 v} \left(u - 1\right)\right)\cdot \left(1\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =1\int_{1}^{2} [\int_{0}^{2} e^{2 v} \left(u - 1\right)\,\mathrm{d}v]\,\mathrm{d}u \\ & =1\int_{1}^{2} \left(u - 1\right)[\int_{0}^{2} e^{2 v}\,\mathrm{d}v]\,\mathrm{d}u \\ & =1\int_{1}^{2} \left(u - 1\right)\left[\frac{e^{2 v}}{2}\right]_{0}^{2}\,\mathrm{d}u \\ & =1\int_{1}^{2} \left(u - 1\right)\left(\left(\frac{e^{4}}{2}\right)-(\left(\frac{1}{2}\right))\right)\,\mathrm{d}u \\ & =\left(1\right)\cdot \left(\frac{e^{4}}{2} - \frac{1}{2}\right)\int_{1}^{2} u - 1\,\mathrm{d}u \\ & =\left(1\right)\cdot \left(\frac{e^{4}}{2} - \frac{1}{2}\right)\left[\frac{u^{2}}{2} - u\right]_{1}^{2} \\ & =\left(1\right)\cdot \left(\frac{e^{4}}{2} - \frac{1}{2}\right)\left(\left(2\right)+\left(-2\right)-(\left(\frac{1}{2}\right)+\left(-1\right))\right) \\ & =\left(1\right)\cdot \left(\frac{1}{2}\right)\cdot \left(\frac{e^{4}}{2} - \frac{1}{2}\right) \\ & =\frac{e^{4}}{4} - \frac{1}{4}\end{aligned}
$$

## Generated moderate / radical

Use a change of variables to evaluate the double integral

$$
\iint_D x y^{2}\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):0\le \frac{x}{\sqrt{16 - y^{2}}}\le 3,\quad -2\le y\le 2\}.$

- $\frac{2208}{5}$

- $384$

- $\frac{1632}{5}$

- $\frac{1088}{5}$

- $\frac{3264}{5}$

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

The inequalities that define the region $D,$

$$
0\le \frac{x}{\sqrt{16 - y^{2}}}\le 3,\quad -2\le y\le 2,
$$

suggest that we use the change of variables

$$
u=\frac{x}{\sqrt{16 - y^{2}}}\,\text{and}\,v=y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):0\le u\le 3,\,-2\le v\le 2\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}\frac{1}{\sqrt{16 - y^{2}}} & \frac{x y}{\left(16 - y^{2}\right)^{\frac{3}{2}}}\\0 & 1\end{matrix}\right]\right|\\&=\frac{1}{\sqrt{16 - y^{2}}}.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=\sqrt{16 - y^{2}}=\sqrt{16 - v^{2}}.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u \sqrt{16 - v^{2}},\ y=v$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D x y^{2}\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta u v^{2} \sqrt{16 - v^{2}}\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(u v^{2} \sqrt{16 - v^{2}}\right)\cdot \left(\sqrt{16 - v^{2}}\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta u v^2(16-v^2)\,\mathrm{d}u\,\mathrm{d}v \\ & =\int_{0}^{3} \left(u\right)[\int_{-2}^{2} - v^{4} + 16 v^{2}\,\mathrm{d}v]\,\mathrm{d}u \\ & =1\int_{0}^{3} \left(u\right)\left[- \frac{v^{5}}{5} + \frac{16 v^{3}}{3}\right]_{-2}^{2}\,\mathrm{d}u \\ & =1\int_{0}^{3} \left(u\right)\left(\left(- \frac{32}{5}\right)+\left(\frac{128}{3}\right)-(\left(\frac{32}{5}\right)+\left(- \frac{128}{3}\right))\right)\,\mathrm{d}u \\ & =\left(1\right)\cdot \left(\frac{1088}{15}\right)\int_{0}^{3} u\,\mathrm{d}u \\ & =\left(1\right)\cdot \left(\frac{1088}{15}\right)\left[\frac{u^{2}}{2}\right]_{0}^{3} \\ & =\left(1\right)\cdot \left(\frac{1088}{15}\right)\left(\left(\frac{9}{2}\right)-(\left(0\right))\right) \\ & =\left(1\right)\cdot \left(\frac{9}{2}\right)\cdot \left(\frac{1088}{15}\right) \\ & =\frac{1632}{5}\end{aligned}
$$

## Generated moderate / radical

Use a change of variables to evaluate the double integral

$$
\iint_D x y^{2}\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):0\le \frac{x}{\sqrt{25 - y^{2}}}\le 4,\quad -2\le y\le 2\}.$

- $\frac{17536}{15}$

- $\frac{28928}{15}$

- $\frac{7232}{15}$

- $\frac{14464}{15}$

- $\frac{3200}{3}$

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

The inequalities that define the region $D,$

$$
0\le \frac{x}{\sqrt{25 - y^{2}}}\le 4,\quad -2\le y\le 2,
$$

suggest that we use the change of variables

$$
u=\frac{x}{\sqrt{25 - y^{2}}}\,\text{and}\,v=y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):0\le u\le 4,\,-2\le v\le 2\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}\frac{1}{\sqrt{25 - y^{2}}} & \frac{x y}{\left(25 - y^{2}\right)^{\frac{3}{2}}}\\0 & 1\end{matrix}\right]\right|\\&=\frac{1}{\sqrt{25 - y^{2}}}.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=\sqrt{25 - y^{2}}=\sqrt{25 - v^{2}}.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u \sqrt{25 - v^{2}},\ y=v$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D x y^{2}\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta u v^{2} \sqrt{25 - v^{2}}\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(u v^{2} \sqrt{25 - v^{2}}\right)\cdot \left(\sqrt{25 - v^{2}}\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta u v^2(25-v^2)\,\mathrm{d}u\,\mathrm{d}v \\ & =\int_{0}^{4} \left(u\right)[\int_{-2}^{2} - v^{4} + 25 v^{2}\,\mathrm{d}v]\,\mathrm{d}u \\ & =1\int_{0}^{4} \left(u\right)\left[- \frac{v^{5}}{5} + \frac{25 v^{3}}{3}\right]_{-2}^{2}\,\mathrm{d}u \\ & =1\int_{0}^{4} \left(u\right)\left(\left(- \frac{32}{5}\right)+\left(\frac{200}{3}\right)-(\left(\frac{32}{5}\right)+\left(- \frac{200}{3}\right))\right)\,\mathrm{d}u \\ & =\left(1\right)\cdot \left(\frac{1808}{15}\right)\int_{0}^{4} u\,\mathrm{d}u \\ & =\left(1\right)\cdot \left(\frac{1808}{15}\right)\left[\frac{u^{2}}{2}\right]_{0}^{4} \\ & =\left(1\right)\cdot \left(\frac{1808}{15}\right)\left(\left(8\right)-(\left(0\right))\right) \\ & =\left(1\right)\cdot \left(8\right)\cdot \left(\frac{1808}{15}\right) \\ & =\frac{14464}{15}\end{aligned}
$$

## Generated moderate / quadratic_exp

Use a change of variables to evaluate the double integral

$$
\iint_D e^{x^{2} + x + y}\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):0\le x\le 4,\quad 0\le x^{2} + y\le 3\}.$

- $- e^{3} + e^{4} + e^{7} - 1$

- $- e^{3} + e^{7}$

- $- e^{3} - e^{4} + e^{7} + 1$

- $3 e^{4} - 3$

- $12 e^{7}$

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

The inequalities that define the region $D,$

$$
0\le x\le 4,\quad 0\le x^{2} + y\le 3,
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x^{2} + y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):0\le u\le 4,\,0\le v\le 3\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\2 x & 1\end{matrix}\right]\right|\\&=1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=1=1.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=- u^{2} + v$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D e^{x^{2} + x + y}\,\mathrm{d}x\,\mathrm{d}y & =\iint_D e^{x+(x^{2} + y)}\,\mathrm{d}x\,\mathrm{d}y \\ & =\iint_\Delta e^{u + v}\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(e^{u + v}\right)\cdot \left(1\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =1\int_{0}^{4} [\int_{0}^{3} e^{u} e^{v}\,\mathrm{d}v]\,\mathrm{d}u \\ & =1\int_{0}^{4} \left(e^{u}\right)[\int_{0}^{3} e^{v}\,\mathrm{d}v]\,\mathrm{d}u \\ & =1\int_{0}^{4} \left(e^{u}\right)\left[e^{v}\right]_{0}^{3}\,\mathrm{d}u \\ & =1\int_{0}^{4} \left(e^{u}\right)\left(\left(e^{3}\right)-(\left(1\right))\right)\,\mathrm{d}u \\ & =\left(1\right)\cdot \left(e^{3} - 1\right)\int_{0}^{4} e^{u}\,\mathrm{d}u \\ & =\left(1\right)\cdot \left(e^{3} - 1\right)\left[e^{u}\right]_{0}^{4} \\ & =\left(1\right)\cdot \left(e^{3} - 1\right)\left(\left(e^{4}\right)-(\left(1\right))\right) \\ & =\left(1\right)\cdot \left(e^{4} - 1\right)\cdot \left(e^{3} - 1\right) \\ & =- e^{3} - e^{4} + e^{7} + 1\end{aligned}
$$

## Generated moderate / quadratic_exp

Use a change of variables to evaluate the double integral

$$
\iint_D e^{x^{2} + x + y}\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):0\le x\le 4,\quad 0\le x^{2} + y\le 4\}.$

- $e^{8} - 1$

- $16 e^{8}$

- $4 e^{4} - 4$

- $- 2 e^{4} + e^{8} + 1$

- $- e^{4} + e^{8}$

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

The inequalities that define the region $D,$

$$
0\le x\le 4,\quad 0\le x^{2} + y\le 4,
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x^{2} + y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):0\le u\le 4,\,0\le v\le 4\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\2 x & 1\end{matrix}\right]\right|\\&=1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=1=1.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=- u^{2} + v$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D e^{x^{2} + x + y}\,\mathrm{d}x\,\mathrm{d}y & =\iint_D e^{x+(x^{2} + y)}\,\mathrm{d}x\,\mathrm{d}y \\ & =\iint_\Delta e^{u + v}\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(e^{u + v}\right)\cdot \left(1\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =1\int_{0}^{4} [\int_{0}^{4} e^{u} e^{v}\,\mathrm{d}v]\,\mathrm{d}u \\ & =1\int_{0}^{4} \left(e^{u}\right)[\int_{0}^{4} e^{v}\,\mathrm{d}v]\,\mathrm{d}u \\ & =1\int_{0}^{4} \left(e^{u}\right)\left[e^{v}\right]_{0}^{4}\,\mathrm{d}u \\ & =1\int_{0}^{4} \left(e^{u}\right)\left(\left(e^{4}\right)-(\left(1\right))\right)\,\mathrm{d}u \\ & =\left(1\right)\cdot \left(e^{4} - 1\right)\int_{0}^{4} e^{u}\,\mathrm{d}u \\ & =\left(1\right)\cdot \left(e^{4} - 1\right)\left[e^{u}\right]_{0}^{4} \\ & =\left(1\right)\cdot \left(e^{4} - 1\right)\left(\left(e^{4}\right)-(\left(1\right))\right) \\ & =\left(1\right)\cdot \left(e^{4} - 1\right)\cdot \left(e^{4} - 1\right) \\ & =- 2 e^{4} + e^{8} + 1\end{aligned}
$$

## Generated moderate / sine

Use a change of variables to evaluate the double integral

$$
\iint_D x \sin{\left(x + y \right)}\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):2\le x\le 6,\quad - \frac{\pi}{2}\le x + y\le \frac{\pi}{2}\}.$

- $-32$

- $32$

- $0$

- $4 \pi$

- $36$

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

The inequalities that define the region $D,$

$$
2\le x\le 6,\quad - \frac{\pi}{2}\le x + y\le \frac{\pi}{2},
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x + y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):2\le u\le 6,\,- \frac{\pi}{2}\le v\le \frac{\pi}{2}\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\1 & 1\end{matrix}\right]\right|\\&=1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=1=1.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=- u + v$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D x \sin{\left(x + y \right)}\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta u \sin{\left(v \right)}\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(u \sin{\left(v \right)}\right)\cdot \left(1\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =1\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} [\int_{2}^{6} u \sin{\left(v \right)}\,\mathrm{d}u]\,\mathrm{d}v \\ & =1\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} \sin{\left(v \right)}[\int_{2}^{6} u\,\mathrm{d}u]\,\mathrm{d}v \\ & =1\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} \sin{\left(v \right)}\left[\frac{u^{2}}{2}\right]_{2}^{6}\,\mathrm{d}v \\ & =1\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} \sin{\left(v \right)}\left(\left(18\right)-(\left(2\right))\right)\,\mathrm{d}v \\ & =\left(1\right)\cdot \left(16\right)\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} \sin{\left(v \right)}\,\mathrm{d}v \\ & =\left(1\right)\cdot \left(16\right)\left[- \cos{\left(v \right)}\right]_{- \frac{\pi}{2}}^{\frac{\pi}{2}} \\ & =\left(1\right)\cdot \left(16\right)\left(\left(0\right)-(\left(0\right))\right) \\ & =\left(1\right)\cdot \left(16\right)\cdot \left(0\right) \\ & =0\end{aligned}
$$

## Generated moderate / sine

Use a change of variables to evaluate the double integral

$$
\iint_D x \sin{\left(x + y \right)}\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):1\le x\le 2,\quad - \frac{\pi}{2}\le x + y\le \frac{\pi}{2}\}.$

- $-3$

- $4$

- $\pi$

- $0$

- $3$

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

The inequalities that define the region $D,$

$$
1\le x\le 2,\quad - \frac{\pi}{2}\le x + y\le \frac{\pi}{2},
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x + y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):1\le u\le 2,\,- \frac{\pi}{2}\le v\le \frac{\pi}{2}\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\1 & 1\end{matrix}\right]\right|\\&=1.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=1=1.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=- u + v$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D x \sin{\left(x + y \right)}\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta u \sin{\left(v \right)}\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(u \sin{\left(v \right)}\right)\cdot \left(1\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =1\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} [\int_{1}^{2} u \sin{\left(v \right)}\,\mathrm{d}u]\,\mathrm{d}v \\ & =1\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} \sin{\left(v \right)}[\int_{1}^{2} u\,\mathrm{d}u]\,\mathrm{d}v \\ & =1\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} \sin{\left(v \right)}\left[\frac{u^{2}}{2}\right]_{1}^{2}\,\mathrm{d}v \\ & =1\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} \sin{\left(v \right)}\left(\left(2\right)-(\left(\frac{1}{2}\right))\right)\,\mathrm{d}v \\ & =\left(1\right)\cdot \left(\frac{3}{2}\right)\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} \sin{\left(v \right)}\,\mathrm{d}v \\ & =\left(1\right)\cdot \left(\frac{3}{2}\right)\left[- \cos{\left(v \right)}\right]_{- \frac{\pi}{2}}^{\frac{\pi}{2}} \\ & =\left(1\right)\cdot \left(\frac{3}{2}\right)\left(\left(0\right)-(\left(0\right))\right) \\ & =\left(1\right)\cdot \left(\frac{3}{2}\right)\cdot \left(0\right) \\ & =0\end{aligned}
$$

## Generated hard / arctan

Use a change of variables to evaluate the double integral

$$
\iint_D \frac{1}{\left(x - 4 y\right)^{2} + 1}\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):2\le x\le 6,\quad 1\le x - 4 y\le 4\}.$

- $\frac{\pi}{4} + \arctan{\left(4 \right)}$

- $\arctan{\left(4 \right)}$

- $- \frac{\pi}{4} + \arctan{\left(4 \right)}$

- $3$

- $\frac{3}{17}$

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

The inequalities that define the region $D,$

$$
2\le x\le 6,\quad 1\le x - 4 y\le 4,
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x - 4 y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):2\le u\le 6,\,1\le v\le 4\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\1 & -4\end{matrix}\right]\right|\\&=-4.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=- \frac{1}{4}=- \frac{1}{4}.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=\frac{u}{4} - \frac{v}{4}$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D \frac{1}{\left(x - 4 y\right)^{2} + 1}\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta \frac{1}{v^{2} + 1}\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(\frac{1}{v^{2} + 1}\right)\cdot \left(\frac{1}{4}\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =\frac{1}{4}\int_{1}^{4} [\int_{2}^{6} \frac{1}{v^{2} + 1}\,\mathrm{d}u]\,\mathrm{d}v \\ & =\frac{1}{4}\int_{1}^{4} \frac{1}{v^{2} + 1}[\int_{2}^{6} 1\,\mathrm{d}u]\,\mathrm{d}v \\ & =\frac{1}{4}\int_{1}^{4} \frac{1}{v^{2} + 1}\left[u\right]_{2}^{6}\,\mathrm{d}v \\ & =\frac{1}{4}\int_{1}^{4} \frac{1}{v^{2} + 1}\left(\left(6\right)-(\left(2\right))\right)\,\mathrm{d}v \\ & =\left(\frac{1}{4}\right)\cdot \left(4\right)\int_{1}^{4} \frac{1}{v^{2} + 1}\,\mathrm{d}v \\ & =\left(\frac{1}{4}\right)\cdot \left(4\right)\left[\arctan{\left(v \right)}\right]_{1}^{4} \\ & =\left(\frac{1}{4}\right)\cdot \left(4\right)\left(\left(\arctan{\left(4 \right)}\right)-(\left(\frac{\pi}{4}\right))\right) \\ & =\left(\frac{1}{4}\right)\cdot \left(4\right)\cdot \left(- \frac{\pi}{4} + \arctan{\left(4 \right)}\right) \\ & =- \frac{\pi}{4} + \arctan{\left(4 \right)}\end{aligned}
$$

## Generated hard / arctan

Use a change of variables to evaluate the double integral

$$
\iint_D \frac{1}{\left(x - 4 y\right)^{2} + 1}\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):1\le x\le 2,\quad 2\le x - 4 y\le 3\}.$

- $\frac{\arctan{\left(2 \right)}}{4} + \frac{\arctan{\left(3 \right)}}{4}$

- $\frac{1}{40}$

- $\frac{1}{4}$

- $- \frac{\arctan{\left(2 \right)}}{4} + \frac{\arctan{\left(3 \right)}}{4}$

- $\frac{\arctan{\left(3 \right)}}{4}$

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

The inequalities that define the region $D,$

$$
1\le x\le 2,\quad 2\le x - 4 y\le 3,
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x - 4 y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):1\le u\le 2,\,2\le v\le 3\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\1 & -4\end{matrix}\right]\right|\\&=-4.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=- \frac{1}{4}=- \frac{1}{4}.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=\frac{u}{4} - \frac{v}{4}$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D \frac{1}{\left(x - 4 y\right)^{2} + 1}\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta \frac{1}{v^{2} + 1}\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(\frac{1}{v^{2} + 1}\right)\cdot \left(\frac{1}{4}\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =\frac{1}{4}\int_{2}^{3} [\int_{1}^{2} \frac{1}{v^{2} + 1}\,\mathrm{d}u]\,\mathrm{d}v \\ & =\frac{1}{4}\int_{2}^{3} \frac{1}{v^{2} + 1}[\int_{1}^{2} 1\,\mathrm{d}u]\,\mathrm{d}v \\ & =\frac{1}{4}\int_{2}^{3} \frac{1}{v^{2} + 1}\left[u\right]_{1}^{2}\,\mathrm{d}v \\ & =\frac{1}{4}\int_{2}^{3} \frac{1}{v^{2} + 1}\left(\left(2\right)-(\left(1\right))\right)\,\mathrm{d}v \\ & =\left(\frac{1}{4}\right)\cdot \left(1\right)\int_{2}^{3} \frac{1}{v^{2} + 1}\,\mathrm{d}v \\ & =\left(\frac{1}{4}\right)\cdot \left(1\right)\left[\arctan{\left(v \right)}\right]_{2}^{3} \\ & =\left(\frac{1}{4}\right)\cdot \left(1\right)\left(\left(\arctan{\left(3 \right)}\right)-(\left(\arctan{\left(2 \right)}\right))\right) \\ & =\left(\frac{1}{4}\right)\cdot \left(1\right)\cdot \left(- \arctan{\left(2 \right)} + \arctan{\left(3 \right)}\right) \\ & =- \frac{\arctan{\left(2 \right)}}{4} + \frac{\arctan{\left(3 \right)}}{4}\end{aligned}
$$

## Generated hard / gaussian

Use a change of variables to evaluate the double integral

$$
\iint_D e^{\left(x + 4 y\right)^{2}} \left(x + 4 y\right)\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):2\le x\le 6,\quad 1\le x + 4 y\le 4\}.$

- $\frac{e^{4}}{2} - \frac{e}{2}$

- $2 e^{16} - 2 e$

- $\frac{e^{16}}{2} - \frac{e}{2}$

- $\frac{e^{16}}{2}$

- $\frac{e^{16}}{2} + \frac{e}{2}$

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

The inequalities that define the region $D,$

$$
2\le x\le 6,\quad 1\le x + 4 y\le 4,
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x + 4 y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):2\le u\le 6,\,1\le v\le 4\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\1 & 4\end{matrix}\right]\right|\\&=4.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=\frac{1}{4}=\frac{1}{4}.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=- \frac{u}{4} + \frac{v}{4}$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D e^{\left(x + 4 y\right)^{2}} \left(x + 4 y\right)\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta e^{v^{2}} v\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(e^{v^{2}} v\right)\cdot \left(\frac{1}{4}\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =\frac{1}{4}\int_{1}^{4} [\int_{2}^{6} e^{v^{2}} v\,\mathrm{d}u]\,\mathrm{d}v \\ & =\frac{1}{4}\int_{1}^{4} e^{v^{2}} v[\int_{2}^{6} 1\,\mathrm{d}u]\,\mathrm{d}v \\ & =\frac{1}{4}\int_{1}^{4} e^{v^{2}} v\left[u\right]_{2}^{6}\,\mathrm{d}v \\ & =\frac{1}{4}\int_{1}^{4} e^{v^{2}} v\left(\left(6\right)-(\left(2\right))\right)\,\mathrm{d}v \\ & =\left(\frac{1}{4}\right)\cdot \left(4\right)\int_{1}^{4} e^{v^{2}} v\,\mathrm{d}v \\ & =\left(\frac{1}{4}\right)\cdot \left(4\right)\left[\frac{e^{v^{2}}}{2}\right]_{1}^{4} \\ & =\left(\frac{1}{4}\right)\cdot \left(4\right)\left(\left(\frac{e^{16}}{2}\right)-(\left(\frac{e}{2}\right))\right) \\ & =\left(\frac{1}{4}\right)\cdot \left(4\right)\cdot \left(\frac{e^{16}}{2} - \frac{e}{2}\right) \\ & =\frac{e^{16}}{2} - \frac{e}{2}\end{aligned}
$$

## Generated hard / gaussian

Use a change of variables to evaluate the double integral

$$
\iint_D e^{\left(x + 4 y\right)^{2}} \left(x + 4 y\right)\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):1\le x\le 2,\quad 2\le x + 4 y\le 3\}.$

- $- \frac{e^{2}}{8} + \frac{e^{3}}{8}$

- $\frac{e^{4}}{8} + \frac{e^{9}}{8}$

- $\frac{e^{9}}{8}$

- $- \frac{e^{4}}{8} + \frac{e^{9}}{8}$

- $- \frac{e^{4}}{2} + \frac{e^{9}}{2}$

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

The inequalities that define the region $D,$

$$
1\le x\le 2,\quad 2\le x + 4 y\le 3,
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x + 4 y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):1\le u\le 2,\,2\le v\le 3\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\1 & 4\end{matrix}\right]\right|\\&=4.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=\frac{1}{4}=\frac{1}{4}.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=- \frac{u}{4} + \frac{v}{4}$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D e^{\left(x + 4 y\right)^{2}} \left(x + 4 y\right)\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta e^{v^{2}} v\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(e^{v^{2}} v\right)\cdot \left(\frac{1}{4}\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =\frac{1}{4}\int_{2}^{3} [\int_{1}^{2} e^{v^{2}} v\,\mathrm{d}u]\,\mathrm{d}v \\ & =\frac{1}{4}\int_{2}^{3} e^{v^{2}} v[\int_{1}^{2} 1\,\mathrm{d}u]\,\mathrm{d}v \\ & =\frac{1}{4}\int_{2}^{3} e^{v^{2}} v\left[u\right]_{1}^{2}\,\mathrm{d}v \\ & =\frac{1}{4}\int_{2}^{3} e^{v^{2}} v\left(\left(2\right)-(\left(1\right))\right)\,\mathrm{d}v \\ & =\left(\frac{1}{4}\right)\cdot \left(1\right)\int_{2}^{3} e^{v^{2}} v\,\mathrm{d}v \\ & =\left(\frac{1}{4}\right)\cdot \left(1\right)\left[\frac{e^{v^{2}}}{2}\right]_{2}^{3} \\ & =\left(\frac{1}{4}\right)\cdot \left(1\right)\left(\left(\frac{e^{9}}{2}\right)-(\left(\frac{e^{4}}{2}\right))\right) \\ & =\left(\frac{1}{4}\right)\cdot \left(1\right)\cdot \left(- \frac{e^{4}}{2} + \frac{e^{9}}{2}\right) \\ & =- \frac{e^{4}}{8} + \frac{e^{9}}{8}\end{aligned}
$$

## Generated hard / linear_exp

Use a change of variables to evaluate the double integral

$$
\iint_D e^{2 x + 8 y} \left(x - 2\right)\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):2\le x\le 6,\quad 1\le x + 4 y\le 4\}.$

- $e^{2} + e^{8}$

- $e^{8}$

- $- e^{2} + e^{8}$

- $6$

- $12 e^{8}$

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

The inequalities that define the region $D,$

$$
2\le x\le 6,\quad 1\le x + 4 y\le 4,
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x + 4 y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):2\le u\le 6,\,1\le v\le 4\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\1 & 4\end{matrix}\right]\right|\\&=4.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=\frac{1}{4}=\frac{1}{4}.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=- \frac{u}{4} + \frac{v}{4}$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D e^{2 x + 8 y} \left(x - 2\right)\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta e^{2 v} \left(u - 2\right)\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(e^{2 v} \left(u - 2\right)\right)\cdot \left(\frac{1}{4}\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =\frac{1}{4}\int_{2}^{6} [\int_{1}^{4} e^{2 v} \left(u - 2\right)\,\mathrm{d}v]\,\mathrm{d}u \\ & =\frac{1}{4}\int_{2}^{6} \left(u - 2\right)[\int_{1}^{4} e^{2 v}\,\mathrm{d}v]\,\mathrm{d}u \\ & =\frac{1}{4}\int_{2}^{6} \left(u - 2\right)\left[\frac{e^{2 v}}{2}\right]_{1}^{4}\,\mathrm{d}u \\ & =\frac{1}{4}\int_{2}^{6} \left(u - 2\right)\left(\left(\frac{e^{8}}{2}\right)-(\left(\frac{e^{2}}{2}\right))\right)\,\mathrm{d}u \\ & =\left(\frac{1}{4}\right)\cdot \left(- \frac{e^{2}}{2} + \frac{e^{8}}{2}\right)\int_{2}^{6} u - 2\,\mathrm{d}u \\ & =\left(\frac{1}{4}\right)\cdot \left(- \frac{e^{2}}{2} + \frac{e^{8}}{2}\right)\left[\frac{u^{2}}{2} - 2 u\right]_{2}^{6} \\ & =\left(\frac{1}{4}\right)\cdot \left(- \frac{e^{2}}{2} + \frac{e^{8}}{2}\right)\left(\left(18\right)+\left(-12\right)-(\left(2\right)+\left(-4\right))\right) \\ & =\left(\frac{1}{4}\right)\cdot \left(8\right)\cdot \left(- \frac{e^{2}}{2} + \frac{e^{8}}{2}\right) \\ & =- e^{2} + e^{8}\end{aligned}
$$

## Generated hard / linear_exp

Use a change of variables to evaluate the double integral

$$
\iint_D e^{2 x + 8 y} \left(x - 1\right)\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):1\le x\le 2,\quad 2\le x + 4 y\le 3\}.$

- $\frac{e^{4}}{16} + \frac{e^{6}}{16}$

- $\frac{e^{6}}{4}$

- $\frac{1}{8}$

- $- \frac{e^{4}}{16} + \frac{e^{6}}{16}$

- $\frac{e^{6}}{16}$

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

The inequalities that define the region $D,$

$$
1\le x\le 2,\quad 2\le x + 4 y\le 3,
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x + 4 y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):1\le u\le 2,\,2\le v\le 3\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\1 & 4\end{matrix}\right]\right|\\&=4.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=\frac{1}{4}=\frac{1}{4}.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=- \frac{u}{4} + \frac{v}{4}$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D e^{2 x + 8 y} \left(x - 1\right)\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta e^{2 v} \left(u - 1\right)\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(e^{2 v} \left(u - 1\right)\right)\cdot \left(\frac{1}{4}\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =\frac{1}{4}\int_{1}^{2} [\int_{2}^{3} e^{2 v} \left(u - 1\right)\,\mathrm{d}v]\,\mathrm{d}u \\ & =\frac{1}{4}\int_{1}^{2} \left(u - 1\right)[\int_{2}^{3} e^{2 v}\,\mathrm{d}v]\,\mathrm{d}u \\ & =\frac{1}{4}\int_{1}^{2} \left(u - 1\right)\left[\frac{e^{2 v}}{2}\right]_{2}^{3}\,\mathrm{d}u \\ & =\frac{1}{4}\int_{1}^{2} \left(u - 1\right)\left(\left(\frac{e^{6}}{2}\right)-(\left(\frac{e^{4}}{2}\right))\right)\,\mathrm{d}u \\ & =\left(\frac{1}{4}\right)\cdot \left(- \frac{e^{4}}{2} + \frac{e^{6}}{2}\right)\int_{1}^{2} u - 1\,\mathrm{d}u \\ & =\left(\frac{1}{4}\right)\cdot \left(- \frac{e^{4}}{2} + \frac{e^{6}}{2}\right)\left[\frac{u^{2}}{2} - u\right]_{1}^{2} \\ & =\left(\frac{1}{4}\right)\cdot \left(- \frac{e^{4}}{2} + \frac{e^{6}}{2}\right)\left(\left(2\right)+\left(-2\right)-(\left(\frac{1}{2}\right)+\left(-1\right))\right) \\ & =\left(\frac{1}{4}\right)\cdot \left(\frac{1}{2}\right)\cdot \left(- \frac{e^{4}}{2} + \frac{e^{6}}{2}\right) \\ & =- \frac{e^{4}}{16} + \frac{e^{6}}{16}\end{aligned}
$$

## Generated hard / radical

Use a change of variables to evaluate the double integral

$$
\iint_D x y^{2}\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):2\le \frac{x}{\sqrt{9 - y^{2}}}\le 4,\quad 1\le y\le 2\}.$

- $\frac{816}{5}$

- $126$

- $\frac{444}{5}$

- $\frac{592}{5}$

- $\frac{888}{5}$

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

The inequalities that define the region $D,$

$$
2\le \frac{x}{\sqrt{9 - y^{2}}}\le 4,\quad 1\le y\le 2,
$$

suggest that we use the change of variables

$$
u=\frac{x}{\sqrt{9 - y^{2}}}\,\text{and}\,v=y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):2\le u\le 4,\,1\le v\le 2\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}\frac{1}{\sqrt{9 - y^{2}}} & \frac{x y}{\left(9 - y^{2}\right)^{\frac{3}{2}}}\\0 & 1\end{matrix}\right]\right|\\&=\frac{1}{\sqrt{9 - y^{2}}}.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=\sqrt{9 - y^{2}}=\sqrt{9 - v^{2}}.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u \sqrt{9 - v^{2}},\ y=v$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D x y^{2}\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta u v^{2} \sqrt{9 - v^{2}}\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(u v^{2} \sqrt{9 - v^{2}}\right)\cdot \left(\sqrt{9 - v^{2}}\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta u v^2(9-v^2)\,\mathrm{d}u\,\mathrm{d}v \\ & =\int_{2}^{4} \left(u\right)[\int_{1}^{2} - v^{4} + 9 v^{2}\,\mathrm{d}v]\,\mathrm{d}u \\ & =1\int_{2}^{4} \left(u\right)\left[- \frac{v^{5}}{5} + 3 v^{3}\right]_{1}^{2}\,\mathrm{d}u \\ & =1\int_{2}^{4} \left(u\right)\left(\left(24\right)+\left(- \frac{32}{5}\right)-(\left(3\right)+\left(- \frac{1}{5}\right))\right)\,\mathrm{d}u \\ & =\left(1\right)\cdot \left(\frac{74}{5}\right)\int_{2}^{4} u\,\mathrm{d}u \\ & =\left(1\right)\cdot \left(\frac{74}{5}\right)\left[\frac{u^{2}}{2}\right]_{2}^{4} \\ & =\left(1\right)\cdot \left(\frac{74}{5}\right)\left(\left(8\right)-(\left(2\right))\right) \\ & =\left(1\right)\cdot \left(6\right)\cdot \left(\frac{74}{5}\right) \\ & =\frac{444}{5}\end{aligned}
$$

## Generated hard / radical

Use a change of variables to evaluate the double integral

$$
\iint_D x y^{2}\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):1\le \frac{x}{\sqrt{25 - y^{2}}}\le 2,\quad 1\le y\le 3\}.$

- $\frac{1988}{5}$

- $\frac{2524}{5}$

- $\frac{5048}{15}$

- $\frac{1262}{5}$

- $325$

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

The inequalities that define the region $D,$

$$
1\le \frac{x}{\sqrt{25 - y^{2}}}\le 2,\quad 1\le y\le 3,
$$

suggest that we use the change of variables

$$
u=\frac{x}{\sqrt{25 - y^{2}}}\,\text{and}\,v=y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):1\le u\le 2,\,1\le v\le 3\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}\frac{1}{\sqrt{25 - y^{2}}} & \frac{x y}{\left(25 - y^{2}\right)^{\frac{3}{2}}}\\0 & 1\end{matrix}\right]\right|\\&=\frac{1}{\sqrt{25 - y^{2}}}.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=\sqrt{25 - y^{2}}=\sqrt{25 - v^{2}}.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u \sqrt{25 - v^{2}},\ y=v$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D x y^{2}\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta u v^{2} \sqrt{25 - v^{2}}\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(u v^{2} \sqrt{25 - v^{2}}\right)\cdot \left(\sqrt{25 - v^{2}}\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta u v^2(25-v^2)\,\mathrm{d}u\,\mathrm{d}v \\ & =\int_{1}^{2} \left(u\right)[\int_{1}^{3} - v^{4} + 25 v^{2}\,\mathrm{d}v]\,\mathrm{d}u \\ & =1\int_{1}^{2} \left(u\right)\left[- \frac{v^{5}}{5} + \frac{25 v^{3}}{3}\right]_{1}^{3}\,\mathrm{d}u \\ & =1\int_{1}^{2} \left(u\right)\left(\left(- \frac{243}{5}\right)+\left(225\right)-(\left(- \frac{1}{5}\right)+\left(\frac{25}{3}\right))\right)\,\mathrm{d}u \\ & =\left(1\right)\cdot \left(\frac{2524}{15}\right)\int_{1}^{2} u\,\mathrm{d}u \\ & =\left(1\right)\cdot \left(\frac{2524}{15}\right)\left[\frac{u^{2}}{2}\right]_{1}^{2} \\ & =\left(1\right)\cdot \left(\frac{2524}{15}\right)\left(\left(2\right)-(\left(\frac{1}{2}\right))\right) \\ & =\left(1\right)\cdot \left(\frac{3}{2}\right)\cdot \left(\frac{2524}{15}\right) \\ & =\frac{1262}{5}\end{aligned}
$$

## Generated hard / quadratic_exp

Use a change of variables to evaluate the double integral

$$
\iint_D e^{x^{2} + x + 4 y}\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):2\le x\le 6,\quad 1\le x^{2} + 4 y\le 4\}.$

- $\frac{e^{10}}{4} - \frac{e^{3}}{4} - \frac{e^{6}}{4} + \frac{e^{7}}{4}$

- $\frac{e^{10}}{4} - \frac{e^{6}}{4}$

- $\frac{e^{10}}{4} + \frac{e^{3}}{4} - \frac{e^{6}}{4} - \frac{e^{7}}{4}$

- $- \frac{3 e^{2}}{4} + \frac{3 e^{6}}{4}$

- $3 e^{10}$

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

The inequalities that define the region $D,$

$$
2\le x\le 6,\quad 1\le x^{2} + 4 y\le 4,
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x^{2} + 4 y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):2\le u\le 6,\,1\le v\le 4\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\2 x & 4\end{matrix}\right]\right|\\&=4.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=\frac{1}{4}=\frac{1}{4}.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=- \frac{u^{2}}{4} + \frac{v}{4}$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D e^{x^{2} + x + 4 y}\,\mathrm{d}x\,\mathrm{d}y & =\iint_D e^{x+(x^{2} + 4 y)}\,\mathrm{d}x\,\mathrm{d}y \\ & =\iint_\Delta e^{u + v}\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(e^{u + v}\right)\cdot \left(\frac{1}{4}\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =\frac{1}{4}\int_{2}^{6} [\int_{1}^{4} e^{u} e^{v}\,\mathrm{d}v]\,\mathrm{d}u \\ & =\frac{1}{4}\int_{2}^{6} \left(e^{u}\right)[\int_{1}^{4} e^{v}\,\mathrm{d}v]\,\mathrm{d}u \\ & =\frac{1}{4}\int_{2}^{6} \left(e^{u}\right)\left[e^{v}\right]_{1}^{4}\,\mathrm{d}u \\ & =\frac{1}{4}\int_{2}^{6} \left(e^{u}\right)\left(\left(e^{4}\right)-(\left(e\right))\right)\,\mathrm{d}u \\ & =\left(\frac{1}{4}\right)\cdot \left(e^{4} - e\right)\int_{2}^{6} e^{u}\,\mathrm{d}u \\ & =\left(\frac{1}{4}\right)\cdot \left(e^{4} - e\right)\left[e^{u}\right]_{2}^{6} \\ & =\left(\frac{1}{4}\right)\cdot \left(e^{4} - e\right)\left(\left(e^{6}\right)-(\left(e^{2}\right))\right) \\ & =\left(\frac{1}{4}\right)\cdot \left(- e^{2} + e^{6}\right)\cdot \left(e^{4} - e\right) \\ & =\frac{e^{10}}{4} + \frac{e^{3}}{4} - \frac{e^{6}}{4} - \frac{e^{7}}{4}\end{aligned}
$$

## Generated hard / quadratic_exp

Use a change of variables to evaluate the double integral

$$
\iint_D e^{x^{2} + x + 4 y}\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):1\le x\le 2,\quad 2\le x^{2} + 4 y\le 3\}.$

- $- \frac{e^{3}}{4} + \frac{e^{5}}{4}$

- $\frac{e^{5}}{4}$

- $\frac{e^{2}}{4} - \frac{e}{4}$

- $\frac{e^{3}}{4} - \frac{e^{4}}{2} + \frac{e^{5}}{4}$

- $- \frac{e^{4}}{4} + \frac{e^{5}}{4}$

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

The inequalities that define the region $D,$

$$
1\le x\le 2,\quad 2\le x^{2} + 4 y\le 3,
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x^{2} + 4 y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):1\le u\le 2,\,2\le v\le 3\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\2 x & 4\end{matrix}\right]\right|\\&=4.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=\frac{1}{4}=\frac{1}{4}.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=- \frac{u^{2}}{4} + \frac{v}{4}$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D e^{x^{2} + x + 4 y}\,\mathrm{d}x\,\mathrm{d}y & =\iint_D e^{x+(x^{2} + 4 y)}\,\mathrm{d}x\,\mathrm{d}y \\ & =\iint_\Delta e^{u + v}\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(e^{u + v}\right)\cdot \left(\frac{1}{4}\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =\frac{1}{4}\int_{1}^{2} [\int_{2}^{3} e^{u} e^{v}\,\mathrm{d}v]\,\mathrm{d}u \\ & =\frac{1}{4}\int_{1}^{2} \left(e^{u}\right)[\int_{2}^{3} e^{v}\,\mathrm{d}v]\,\mathrm{d}u \\ & =\frac{1}{4}\int_{1}^{2} \left(e^{u}\right)\left[e^{v}\right]_{2}^{3}\,\mathrm{d}u \\ & =\frac{1}{4}\int_{1}^{2} \left(e^{u}\right)\left(\left(e^{3}\right)-(\left(e^{2}\right))\right)\,\mathrm{d}u \\ & =\left(\frac{1}{4}\right)\cdot \left(- e^{2} + e^{3}\right)\int_{1}^{2} e^{u}\,\mathrm{d}u \\ & =\left(\frac{1}{4}\right)\cdot \left(- e^{2} + e^{3}\right)\left[e^{u}\right]_{1}^{2} \\ & =\left(\frac{1}{4}\right)\cdot \left(- e^{2} + e^{3}\right)\left(\left(e^{2}\right)-(\left(e\right))\right) \\ & =\left(\frac{1}{4}\right)\cdot \left(e^{2} - e\right)\cdot \left(- e^{2} + e^{3}\right) \\ & =\frac{e^{3}}{4} - \frac{e^{4}}{2} + \frac{e^{5}}{4}\end{aligned}
$$

## Generated hard / sine

Use a change of variables to evaluate the double integral

$$
\iint_D x \sin{\left(x + 4 y \right)}\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):2\le x\le 6,\quad \frac{\pi}{6}\le x + 4 y\le \frac{2 \pi}{3}\}.$

- $2 - 2 \sqrt{3}$

- $-2 + 2 \sqrt{3}$

- $2 + 2 \sqrt{3}$

- $\frac{\sqrt{3} \pi}{4}$

- $- \frac{9}{4} + \frac{9 \sqrt{3}}{4}$

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

The inequalities that define the region $D,$

$$
2\le x\le 6,\quad \frac{\pi}{6}\le x + 4 y\le \frac{2 \pi}{3},
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x + 4 y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):2\le u\le 6,\,\frac{\pi}{6}\le v\le \frac{2 \pi}{3}\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\1 & 4\end{matrix}\right]\right|\\&=4.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=\frac{1}{4}=\frac{1}{4}.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=- \frac{u}{4} + \frac{v}{4}$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D x \sin{\left(x + 4 y \right)}\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta u \sin{\left(v \right)}\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(u \sin{\left(v \right)}\right)\cdot \left(\frac{1}{4}\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =\frac{1}{4}\int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} [\int_{2}^{6} u \sin{\left(v \right)}\,\mathrm{d}u]\,\mathrm{d}v \\ & =\frac{1}{4}\int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} \sin{\left(v \right)}[\int_{2}^{6} u\,\mathrm{d}u]\,\mathrm{d}v \\ & =\frac{1}{4}\int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} \sin{\left(v \right)}\left[\frac{u^{2}}{2}\right]_{2}^{6}\,\mathrm{d}v \\ & =\frac{1}{4}\int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} \sin{\left(v \right)}\left(\left(18\right)-(\left(2\right))\right)\,\mathrm{d}v \\ & =\left(\frac{1}{4}\right)\cdot \left(16\right)\int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} \sin{\left(v \right)}\,\mathrm{d}v \\ & =\left(\frac{1}{4}\right)\cdot \left(16\right)\left[- \cos{\left(v \right)}\right]_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} \\ & =\left(\frac{1}{4}\right)\cdot \left(16\right)\left(\left(\frac{1}{2}\right)-(\left(- \frac{\sqrt{3}}{2}\right))\right) \\ & =\left(\frac{1}{4}\right)\cdot \left(16\right)\cdot \left(\frac{1}{2} + \frac{\sqrt{3}}{2}\right) \\ & =2 + 2 \sqrt{3}\end{aligned}
$$

## Generated hard / sine

Use a change of variables to evaluate the double integral

$$
\iint_D x \sin{\left(x + 4 y \right)}\,\mathrm{d}x\,\mathrm{d}y
$$

where $D=\{(x,y):1\le x\le 2,\quad \frac{\pi}{6}\le x + 4 y\le \frac{2 \pi}{3}\}.$

- $\frac{3}{16} - \frac{3 \sqrt{3}}{16}$

- $- \frac{1}{4} + \frac{\sqrt{3}}{4}$

- $\frac{\sqrt{3} \pi}{16}$

- $\frac{3}{16} + \frac{3 \sqrt{3}}{16}$

- $- \frac{3}{16} + \frac{3 \sqrt{3}}{16}$

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

The inequalities that define the region $D,$

$$
1\le x\le 2,\quad \frac{\pi}{6}\le x + 4 y\le \frac{2 \pi}{3},
$$

suggest that we use the change of variables

$$
u=x\,\text{and}\,v=x + 4 y.
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$

Our domain in the $uv$-plane is

$$
\Delta=\{(u,v):1\le u\le 2,\,\frac{\pi}{6}\le v\le \frac{2 \pi}{3}\}.
$$

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{\partial(u,v)}{\partial(x,y)} & =\left|\begin{matrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\\frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{matrix}\right|\\&=\left|\left[\begin{matrix}1 & 0\\1 & 4\end{matrix}\right]\right|\\&=4.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left(\frac{\partial(u,v)}{\partial(x,y)}\right)^{-1}=\frac{1}{4}=\frac{1}{4}.
$$

Note that $\frac{\partial(x,y)}{\partial(u,v)}\ne0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

Solving the transformation equations gives $x=u,\ y=- \frac{u}{4} + \frac{v}{4}$, so the transformation is one-to-one on this domain.

**Step 5**: Perform the change of variables, and evaluate the integral:

Performing the change of variables, we obtain

$$
\begin{aligned}\iint_D x \sin{\left(x + 4 y \right)}\,\mathrm{d}x\,\mathrm{d}y & =\iint_\Delta u \sin{\left(v \right)}\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,\mathrm{d}u\,\mathrm{d}v \\ & =\iint_\Delta \left(u \sin{\left(v \right)}\right)\cdot \left(\frac{1}{4}\right)\,\mathrm{d}u\,\mathrm{d}v \\ & =\frac{1}{4}\int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} [\int_{1}^{2} u \sin{\left(v \right)}\,\mathrm{d}u]\,\mathrm{d}v \\ & =\frac{1}{4}\int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} \sin{\left(v \right)}[\int_{1}^{2} u\,\mathrm{d}u]\,\mathrm{d}v \\ & =\frac{1}{4}\int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} \sin{\left(v \right)}\left[\frac{u^{2}}{2}\right]_{1}^{2}\,\mathrm{d}v \\ & =\frac{1}{4}\int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} \sin{\left(v \right)}\left(\left(2\right)-(\left(\frac{1}{2}\right))\right)\,\mathrm{d}v \\ & =\left(\frac{1}{4}\right)\cdot \left(\frac{3}{2}\right)\int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} \sin{\left(v \right)}\,\mathrm{d}v \\ & =\left(\frac{1}{4}\right)\cdot \left(\frac{3}{2}\right)\left[- \cos{\left(v \right)}\right]_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} \\ & =\left(\frac{1}{4}\right)\cdot \left(\frac{3}{2}\right)\left(\left(\frac{1}{2}\right)-(\left(- \frac{\sqrt{3}}{2}\right))\right) \\ & =\left(\frac{1}{4}\right)\cdot \left(\frac{3}{2}\right)\cdot \left(\frac{1}{2} + \frac{\sqrt{3}}{2}\right) \\ & =\frac{3}{16} + \frac{3 \sqrt{3}}{16}\end{aligned}
$$
