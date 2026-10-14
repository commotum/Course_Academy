# Performing a Change of Variables: review

Frozen source: math, basis1356. Raw originals preserve missing attributes; observed replays are evidence-only. Normal variants are authored complete banks.


## Original 17592186198948 / difference

Consider the finite region $D$ in the $xy$-plane, given by

$D = {(x, y): 0 \le x + y \le 3, 0 \le y - x \le 2}$.

By performing the change of variables
$u = x + y$
and
$v = y - x$,
the integral
$∬_(D)(y^{2} - x^{2})dxdy$
can be written in terms of $u$ and $v$ as

- $\displaystyle \int_{0}^{3}\displaystyle \int_{0}^{2}uvdvdu$
- $\displaystyle \int_{0}^{3}\displaystyle \int_{0}^{2}(v^{2} - u^{2})dvdu$
- $\frac{1}{2}\displaystyle \int_{0}^{3}\displaystyle \int_{0}^{2}uvdvdu$
- $\frac{1}{2}\displaystyle \int_{0}^{3}\displaystyle \int_{0}^{2}(u^{2} - v^{2})dvdu$
- $2\displaystyle \int_{0}^{3}\displaystyle \int_{0}^{2}uvdvdu$



## Original 17592186198950 / sum_product_evidence

Using the change of variables $u = xy$ and $v = y + x$, evaluate the double integral

$∬_(D) \mid y - x \mid e^{xy}dxdy$,
where $D = {(x, y): 1 \le xy \le 4, 1 \le y + x \le 10}$.

- $10(e^{4} - 1)$
- $9(e^{4} - e)$
- $9(e^{3} - e)$
- $5(e^{4} - 1)$
- $5(1 - e^{3})$



## Original 17592186373909 / ratio_product

Using the change of variables $u=\frac{y}{{x}^{2}}$ and $v=xy,$ evaluate the double integral

$$
{∬}_{D}xy\,dx\,dy,
$$

where $D={(x,y)\,:\,{x}^{2}\le y\le 4{x}^{2},\,1\le xy\le 5}.$

- $3\operatorname{ln}⁡2$
- $\frac{11}{4}$
- $\frac{9}{2}$
- $8\operatorname{ln}⁡2$
- $6$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\,dx\,dy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=\frac{y}{{x}^{2}},\,v=xy
$$

 
gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows::

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,1\le u\le 4,\,1\le v\le 5}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-\frac{2y}{{x}^{3}} & \frac{1}{{x}^{2}} \\ y & \text{ }\text{ }x\end{aligned}| \\  & =-\frac{3y}{{x}^{2}}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{(-\frac{3y}{{x}^{2}})}=-\frac{1}{3u}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}xy\,dx\,dy & ={∬}_{Δ}v|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}v\cdot |\frac{1}{3u}|\,\text{d}u\,\text{d}v \\  & =\frac{1}{3}{\int }_{1}^{5}{\int }_{1}^{4}\frac{v}{u}\,\text{d}u\,\text{d}v \\  & =\frac{1}{3}{\int }_{1}^{5}v[{\int }_{1}^{4}\frac{1}{u}\,\text{d}u]\text{d}v \\  & =\frac{1}{3}{\int }_{1}^{5}v[\operatorname{ln}⁡|u|\,{|}_{1}^{4}]dv \\  & =\frac{1}{3}{\int }_{1}^{5}v(\operatorname{ln}⁡4-\operatorname{ln}⁡1)\,dv \\  & =\frac{2\operatorname{ln}⁡2}{3}{\int }_{1}^{5}v\,dv \\  & =\frac{2\operatorname{ln}⁡2}{3}\cdot \frac{1}{2}{v}^{2}\,{|}_{1}^{5} \\  & =\frac{\operatorname{ln}⁡2}{3}\cdot (25-1) \\  & =8\operatorname{ln}⁡2.\end{aligned}
$$



## Original 17592186375103 / triangular_quadratic

Consider the region $D$ in the $xy$-plane, given by

$$
D={(x,y)\,:\,0\le 2x+y\le 5,\,0\le y\le 1}.
$$

  

By performing the change of variables $u=2x+y$ and $v=y,$ the integral 

$$
{∬}_{D}(2xy+{x}^{2})\,dx\,dy
$$

can be written in terms of $u$ and $v$ as

- $\frac{1}{8}{\int }_{0}^{1}{\int }_{0}^{5}(uv-{v}^{2}+3{u}^{2})\,du\,dv$
- $\frac{1}{8}{\int }_{0}^{1}{\int }_{0}^{5}(2uv-3{v}^{2}+{u}^{2})\,du\,dv$
- $\frac{1}{2}{\int }_{0}^{1}{\int }_{0}^{5}(2uv-{u}^{2}+{v}^{2})\,du\,dv$
- $\frac{1}{4}{\int }_{0}^{1}{\int }_{0}^{5}(uv-5{v}^{2}-{u}^{2})\,du\,dv$
- $\frac{1}{4}{\int }_{0}^{1}{\int }_{0}^{5}(uv-2{v}^{2}+{v}^{2})\,du\,dv$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\text{ }dx\,dy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=2x+y,\,v=y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,0\le u\le 5,\,0\le v\le 1}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}2 & 1 \\ 0 & \text{ }\text{ }1\end{aligned}| \\  & =2.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{2}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

In this case, we first need to solve the transformation equations

$$
u=2x+y,\,v=y
$$

 
for $x$ and $y$, which gives

$$
x=\frac{u-v}{2},\,y=v.
$$

 

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}(2xy+{x}^{2})\,dx\,dy & ={∬}_{Δ}[2\cdot \frac{u-v}{2}\cdot v+{(\frac{u-v}{2})}^{2}]|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}(uv-{v}^{2}+\frac{{u}^{2}-2uv+{v}^{2}}{4})\frac{1}{2}\,du\,dv \\  & =\frac{1}{8}{\int }_{0}^{1}{\int }_{0}^{5}(2uv-3{v}^{2}+{u}^{2})\,du\,dv.\end{aligned}
$$



## Original 17592186375495 / product

Consider the region $D$ in the $xy$-plane, given by

$$
D={(x,y)\,:\,-1\le y-x\le 1,\,0\le x+y\le 1}.
$$

By performing the change of variables $u=y-x$ and $v=x+y,$ the integral

$$
{∬}_{D}8xy\,dx\,dy
$$

can be written in terms of $u$ and $v$ as

- $2{\int }_{0}^{1}{\int }_{-1}^{1}(v-u)^{2}\,du\,dv$
- ${\int }_{0}^{1}{\int }_{-1}^{1}({v}^{2}-{u}^{2})\,du\,dv$
- ${\int }_{0}^{1}{\int }_{-1}^{1}(v-u)^{4}\,du\,dv$
- $\frac{1}{2}{\int }_{0}^{1}{\int }_{-1}^{1}(v-u)^{2}\,du\,dv$
- $2{\int }_{0}^{1}{\int }_{-1}^{1}({v}^{2}-{u}^{2})\,du\,dv$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\text{ }dx\,dy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=y-x,\,v=x+y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,-1\le u\le 1,\,0\le v\le 1}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-1 & 1 \\ 1 & \text{ }\text{ }1\end{aligned}| \\  & =-2.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=-\frac{1}{2}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

In this case, we first need to solve the transformation equations

$$
u=y-x,\,v=x+y
$$

 
for $x$ and $y$, which gives

$$
x=\frac{v-u}{2},\,y=\frac{v+u}{2}.
$$

 

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}8xy\,dx\,dy & ={∬}_{Δ}8(\frac{v-u}{2})(\frac{v+u}{2})|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}2({v}^{2}-{u}^{2})|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}2({v}^{2}-{u}^{2})|-\frac{1}{2}|\text{d}u\,\text{d}v \\  & ={\int }_{0}^{1}{\int }_{-1}^{1}({v}^{2}-{u}^{2})\,du\,dv.\end{aligned}
$$



## Original 17592186375502 / exponential

Consider the region $D$ in the $xy$-plane, given by

$$
D={(x,y)\,:\,0\le 2x+5y\le 2,\,0\le x+3y\le 4}.
$$

By performing the change of variables $u=2x+5y$ and $v=x+3y,$ the integral

$$
{∬}_{D}{e}^{x+y}\,dx\,dy
$$

can be written in terms of $u$ and $v$ as

- ${\int }_{0}^{4}{\int }_{0}^{2}{e}^{2u-v}\,du\,dv$
- ${\int }_{0}^{4}{\int }_{0}^{2}{e}^{2u-3v}\,du\,dv$
- $2{\int }_{0}^{4}{\int }_{0}^{2}{e}^{3u-2v}\,du\,dv$
- $\frac{1}{2}{\int }_{0}^{4}{\int }_{0}^{2}{e}^{3u-2v}\,du\,dv$
- ${\int }_{0}^{4}{\int }_{0}^{2}{e}^{u+v}\,du\,dv$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\,dx\,dy={∬}_{Δ}f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=2x+5y,\,v=x+3y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,0\le u\le 2,\,0\le v\le 4}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}2 & 5 \\ 1 & \text{ }\text{ }3\end{aligned}| \\  & =1.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=1.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

In this case, we first need to solve the transformation equations

$$
u=2x+5y,\,v=x+3y
$$

 
for $x$ and $y$, which gives

$$
x=3u-5v,\,y=2v-u.
$$

 

Now, performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}{e}^{x+y}\,dx\,dy & ={∬}_{Δ}{e}^{3u-5v+2v-u}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\,\text{d}v \\  & ={∬}_{Δ}{e}^{2u-3v}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\,\text{d}v \\  & ={∬}_{Δ}{e}^{2u-3v}\cdot |1|\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{4}{\int }_{0}^{2}{e}^{2u-3v}\,du\,dv.\end{aligned}
$$



## Original 17592186375509 / sum_square

Consider the region $D$ in the $xy$-plane, given by

$$
D={(x,y)\,:\,-1\le x+y\le 3,\,-4\le y-x\le -1}.
$$

By performing the change of variables $u=x+y$ and $v=y-x,$ the integral

$$
{∬}_{D}3(x+y)^{2}\,dx\,dy
$$

can be written in terms of $u$ and $v$ as

- $\frac{3}{4}{\int }_{-1}^{3}{\int }_{-4}^{-1}(u+v)^{2}\,dv\,du$
- $\frac{3}{2}{\int }_{-1}^{3}{\int }_{-4}^{-1}(u+v)^{2}\,dv\,du$
- $6{\int }_{-1}^{3}{\int }_{-4}^{-1}{u}^{2}\,dv\,du$
- $\frac{9}{2}{\int }_{-1}^{3}{\int }_{-4}^{-1}{u}^{2}\,dv\,du$
- $\frac{3}{2}{\int }_{-1}^{3}{\int }_{-4}^{-1}{u}^{2}\,dv\,du$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\,dx\,dy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x+y,\,v=y-x
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,-1\le u\le 3,\,-4\le v\le -1}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}1 & 1 \\ -1 & \text{ }\text{ }1\end{aligned}| \\  & =2.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{2}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}3(x+y)^{2}\,dx\,dy & ={∬}_{Δ}3{u}^{2}|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}3{u}^{2}|\frac{1}{2}|\text{d}u\,\text{d}v \\  & =\frac{3}{2}{\int }_{-1}^{3}{\int }_{-4}^{-1}{u}^{2}\,dv\,du.\end{aligned}
$$



## Generated easy / difference / authored

Consider the finite region $D$ in the $xy$-plane, given by

$D = {(x, y): -4 \le x + y \le 0, -3 \le y - x \le 1}$.

By performing the change of variables
$u = x + y$
and
$v = y - x$,
the integral
$∬_(D)(y^{2} - x^{2})dxdy$
can be written in terms of $u$ and $v$ as

- ${\int }_{-4}^{0}{\int }_{-3}^{1}\frac{u^{2}}{2} - \frac{v^{2}}{2}\,dv\,du$
- ${\int }_{-4}^{0}{\int }_{-3}^{1}2 u v\,dv\,du$
- ${\int }_{-4}^{0}{\int }_{-3}^{1}- \frac{u v}{2}\,dv\,du$
- ${\int }_{-4}^{0}{\int }_{-3}^{1}\frac{u v}{2}\,dv\,du$
- ${\int }_{-4}^{0}{\int }_{-3}^{1}u v\,dv\,du$

Let's define a transformation $T$ as follows:

$$T:\begin{bmatrix}u\\v\end{bmatrix}\longmapsto\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix}$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$\iint_D f(x,y)\,dx\,dy=\iint_Δ f(x(u,v),y(u,v))\left|\frac{∂(x,y)}{∂(u,v)}\right|\,du\,dv.$$

The supplied change of variables gives us the inverse function $T^{-1}$.

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of $T^{-1}$.

$$Δ=\{(u,v):-4\le u\le 0,\ -3\le v\le 1\}.$$

**Step 2**: Compute the Jacobian determinant corresponding to $T^{-1}$.

$$\frac{∂(u,v)}{∂(x,y)}=\begin{vmatrix}\frac{∂u}{∂x}&\frac{∂u}{∂y}\\\frac{∂v}{∂x}&\frac{∂v}{∂y}\end{vmatrix}=\begin{vmatrix}1&1\\-1&1\end{vmatrix}=2.$$

**Step 3**: Compute the Jacobian determinant corresponding to $T$.

$$\frac{∂(x,y)}{∂(u,v)}=\left(\frac{∂(u,v)}{∂(x,y)}\right)^{-1}=\frac{1}{2}.$$

Note that the Jacobian determinant is nonzero everywhere inside $Δ$.

**Step 4**: Perform the change of variables.

In this case, we first need to solve the transformation equations for $x$ and $y$, which gives

$$x=\frac{u}{2} - \frac{v}{2},\qquad y=\frac{u}{2} + \frac{v}{2}.$$

Performing the change of variables, we obtain

$$\begin{aligned}\iint_D(y^2-x^2)\,dx\,dy&=\iint_Δ\left[\left(\frac{u+v}{2}\right)^2-\left(\frac{u-v}{2}\right)^2\right]\left|\frac{∂(x,y)}{∂(u,v)}\right|\,du\,dv\\&=\iint_Δuv\left|\frac12\right|\,du\,dv\\&={\int }_{-4}^{0}{\int }_{-3}^{1}\frac{u v}{2}\,dv\,du.\end{aligned}$$



## Generated easy / difference / authored

Consider the finite region $D$ in the $xy$-plane, given by

$D = {(x, y): -3 \le x + y \le -1, -2 \le y - x \le 1}$.

By performing the change of variables
$u = x + y$
and
$v = y - x$,
the integral
$∬_(D)(y^{2} - x^{2})dxdy$
can be written in terms of $u$ and $v$ as

- ${\int }_{-3}^{-1}{\int }_{-2}^{1}\frac{u^{2}}{2} - \frac{v^{2}}{2}\,dv\,du$
- ${\int }_{-3}^{-1}{\int }_{-2}^{1}2 u v\,dv\,du$
- ${\int }_{-3}^{-1}{\int }_{-2}^{1}\frac{u v}{2}\,dv\,du$
- ${\int }_{-3}^{-1}{\int }_{-2}^{1}- \frac{u v}{2}\,dv\,du$
- ${\int }_{-3}^{-1}{\int }_{-2}^{1}u v\,dv\,du$

Let's define a transformation $T$ as follows:

$$T:\begin{bmatrix}u\\v\end{bmatrix}\longmapsto\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix}$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$\iint_D f(x,y)\,dx\,dy=\iint_Δ f(x(u,v),y(u,v))\left|\frac{∂(x,y)}{∂(u,v)}\right|\,du\,dv.$$

The supplied change of variables gives us the inverse function $T^{-1}$.

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of $T^{-1}$.

$$Δ=\{(u,v):-3\le u\le -1,\ -2\le v\le 1\}.$$

**Step 2**: Compute the Jacobian determinant corresponding to $T^{-1}$.

$$\frac{∂(u,v)}{∂(x,y)}=\begin{vmatrix}\frac{∂u}{∂x}&\frac{∂u}{∂y}\\\frac{∂v}{∂x}&\frac{∂v}{∂y}\end{vmatrix}=\begin{vmatrix}1&1\\-1&1\end{vmatrix}=2.$$

**Step 3**: Compute the Jacobian determinant corresponding to $T$.

$$\frac{∂(x,y)}{∂(u,v)}=\left(\frac{∂(u,v)}{∂(x,y)}\right)^{-1}=\frac{1}{2}.$$

Note that the Jacobian determinant is nonzero everywhere inside $Δ$.

**Step 4**: Perform the change of variables.

In this case, we first need to solve the transformation equations for $x$ and $y$, which gives

$$x=\frac{u}{2} - \frac{v}{2},\qquad y=\frac{u}{2} + \frac{v}{2}.$$

Performing the change of variables, we obtain

$$\begin{aligned}\iint_D(y^2-x^2)\,dx\,dy&=\iint_Δ\left[\left(\frac{u+v}{2}\right)^2-\left(\frac{u-v}{2}\right)^2\right]\left|\frac{∂(x,y)}{∂(u,v)}\right|\,du\,dv\\&=\iint_Δuv\left|\frac12\right|\,du\,dv\\&={\int }_{-3}^{-1}{\int }_{-2}^{1}\frac{u v}{2}\,dv\,du.\end{aligned}$$



## Generated easy / triangular_quadratic / authored

Consider the region $D$ in the $xy$-plane, given by

$$
D={(x,y)\,:\,-4\le 2x+y\le 0,\,-3\le y\le 1}.
$$

  

By performing the change of variables $u=2x+y$ and $v=y,$ the integral 

$$
{∬}_{D}(2xy+{x}^{2})\,dx\,dy
$$

can be written in terms of $u$ and $v$ as

- ${\int }_{-3}^{1}{\int }_{-4}^{0}\frac{u v}{2} - \frac{v^{2}}{2}\,du\,dv$
- ${\int }_{-3}^{1}{\int }_{-4}^{0}\frac{u^{2}}{2} + u v - \frac{3 v^{2}}{2}\,du\,dv$
- ${\int }_{-3}^{1}{\int }_{-4}^{0}\frac{u^{2}}{8} + \frac{3 u v}{4} + \frac{5 v^{2}}{8}\,du\,dv$
- ${\int }_{-3}^{1}{\int }_{-4}^{0}\frac{u^{2}}{8} + \frac{u v}{4} - \frac{3 v^{2}}{8}\,du\,dv$
- ${\int }_{-3}^{1}{\int }_{-4}^{0}\frac{u^{2}}{4} + \frac{u v}{2} - \frac{3 v^{2}}{4}\,du\,dv$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\text{ }dx\,dy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=2x+y,\,v=y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,-4\le u\le 0,\,-3\le v\le 1}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}2 & 1 \\ 0 & \text{ }\text{ }1\end{aligned}| \\  & =2.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{2}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

In this case, we first need to solve the transformation equations

$$
u=2x+y,\,v=y
$$

 
for $x$ and $y$, which gives

$$
x=\frac{u-v}{2},\,y=v.
$$

 

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}(2xy+{x}^{2})\,dx\,dy & ={∬}_{Δ}[2\cdot \frac{u-v}{2}\cdot v+{(\frac{u-v}{2})}^{2}]|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}(uv-{v}^{2}+\frac{{u}^{2}-2uv+{v}^{2}}{4})\frac{1}{2}\,du\,dv \\  & =\frac{1}{8}{\int }_{-3}^{1}{\int }_{-4}^{0}(2uv-3{v}^{2}+{u}^{2})\,du\,dv.\end{aligned}
$$



## Generated easy / triangular_quadratic / authored

Consider the region $D$ in the $xy$-plane, given by

$$
D={(x,y)\,:\,-3\le 2x+y\le -1,\,-2\le y\le 1}.
$$

  

By performing the change of variables $u=2x+y$ and $v=y,$ the integral 

$$
{∬}_{D}(2xy+{x}^{2})\,dx\,dy
$$

can be written in terms of $u$ and $v$ as

- ${\int }_{-2}^{1}{\int }_{-3}^{-1}\frac{u v}{2} - \frac{v^{2}}{2}\,du\,dv$
- ${\int }_{-2}^{1}{\int }_{-3}^{-1}\frac{u^{2}}{2} + u v - \frac{3 v^{2}}{2}\,du\,dv$
- ${\int }_{-2}^{1}{\int }_{-3}^{-1}\frac{u^{2}}{8} + \frac{u v}{4} - \frac{3 v^{2}}{8}\,du\,dv$
- ${\int }_{-2}^{1}{\int }_{-3}^{-1}\frac{u^{2}}{8} + \frac{3 u v}{4} + \frac{5 v^{2}}{8}\,du\,dv$
- ${\int }_{-2}^{1}{\int }_{-3}^{-1}\frac{u^{2}}{4} + \frac{u v}{2} - \frac{3 v^{2}}{4}\,du\,dv$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\text{ }dx\,dy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=2x+y,\,v=y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,-3\le u\le -1,\,-2\le v\le 1}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}2 & 1 \\ 0 & \text{ }\text{ }1\end{aligned}| \\  & =2.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{2}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

In this case, we first need to solve the transformation equations

$$
u=2x+y,\,v=y
$$

 
for $x$ and $y$, which gives

$$
x=\frac{u-v}{2},\,y=v.
$$

 

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}(2xy+{x}^{2})\,dx\,dy & ={∬}_{Δ}[2\cdot \frac{u-v}{2}\cdot v+{(\frac{u-v}{2})}^{2}]|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}(uv-{v}^{2}+\frac{{u}^{2}-2uv+{v}^{2}}{4})\frac{1}{2}\,du\,dv \\  & =\frac{1}{8}{\int }_{-2}^{1}{\int }_{-3}^{-1}(2uv-3{v}^{2}+{u}^{2})\,du\,dv.\end{aligned}
$$



## Generated easy / product / authored

Consider the region $D$ in the $xy$-plane, given by

$$
D={(x,y)\,:\,-4\le y-x\le 0,\,-3\le x+y\le 1}.
$$

By performing the change of variables $u=y-x$ and $v=x+y,$ the integral

$$
{∬}_{D}8xy\,dx\,dy
$$

can be written in terms of $u$ and $v$ as

- ${\int }_{-3}^{1}{\int }_{-4}^{0}\left(u + v\right)^{2}\,du\,dv$
- ${\int }_{-3}^{1}{\int }_{-4}^{0}- 4 u^{2} + 4 v^{2}\,du\,dv$
- ${\int }_{-3}^{1}{\int }_{-4}^{0}\left(- u + v\right)^{2}\,du\,dv$
- ${\int }_{-3}^{1}{\int }_{-4}^{0}- u^{2} + v^{2}\,du\,dv$
- ${\int }_{-3}^{1}{\int }_{-4}^{0}- 2 u^{2} + 2 v^{2}\,du\,dv$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\text{ }dx\,dy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=y-x,\,v=x+y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,-4\le u\le 0,\,-3\le v\le 1}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-1 & 1 \\ 1 & \text{ }\text{ }1\end{aligned}| \\  & =-2.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=-\frac{1}{2}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

In this case, we first need to solve the transformation equations

$$
u=y-x,\,v=x+y
$$

 
for $x$ and $y$, which gives

$$
x=\frac{v-u}{2},\,y=\frac{v+u}{2}.
$$

 

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}8xy\,dx\,dy & ={∬}_{Δ}8(\frac{v-u}{2})(\frac{v+u}{2})|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}2({v}^{2}-{u}^{2})|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}2({v}^{2}-{u}^{2})|-\frac{1}{2}|\text{d}u\,\text{d}v \\  & ={\int }_{-3}^{1}{\int }_{-4}^{0}({v}^{2}-{u}^{2})\,du\,dv.\end{aligned}
$$



## Generated easy / product / authored

Consider the region $D$ in the $xy$-plane, given by

$$
D={(x,y)\,:\,-3\le y-x\le -1,\,-2\le x+y\le 1}.
$$

By performing the change of variables $u=y-x$ and $v=x+y,$ the integral

$$
{∬}_{D}8xy\,dx\,dy
$$

can be written in terms of $u$ and $v$ as

- ${\int }_{-2}^{1}{\int }_{-3}^{-1}\left(u + v\right)^{2}\,du\,dv$
- ${\int }_{-2}^{1}{\int }_{-3}^{-1}- 4 u^{2} + 4 v^{2}\,du\,dv$
- ${\int }_{-2}^{1}{\int }_{-3}^{-1}- u^{2} + v^{2}\,du\,dv$
- ${\int }_{-2}^{1}{\int }_{-3}^{-1}\left(- u + v\right)^{2}\,du\,dv$
- ${\int }_{-2}^{1}{\int }_{-3}^{-1}- 2 u^{2} + 2 v^{2}\,du\,dv$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\text{ }dx\,dy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=y-x,\,v=x+y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,-3\le u\le -1,\,-2\le v\le 1}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-1 & 1 \\ 1 & \text{ }\text{ }1\end{aligned}| \\  & =-2.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=-\frac{1}{2}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

In this case, we first need to solve the transformation equations

$$
u=y-x,\,v=x+y
$$

 
for $x$ and $y$, which gives

$$
x=\frac{v-u}{2},\,y=\frac{v+u}{2}.
$$

 

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}8xy\,dx\,dy & ={∬}_{Δ}8(\frac{v-u}{2})(\frac{v+u}{2})|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}2({v}^{2}-{u}^{2})|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}2({v}^{2}-{u}^{2})|-\frac{1}{2}|\text{d}u\,\text{d}v \\  & ={\int }_{-2}^{1}{\int }_{-3}^{-1}({v}^{2}-{u}^{2})\,du\,dv.\end{aligned}
$$



## Generated easy / exponential / authored

Consider the region $D$ in the $xy$-plane, given by

$$
D={(x,y)\,:\,-4\le 2x+5y\le 0,\,-3\le x+3y\le 1}.
$$

By performing the change of variables $u=2x+5y$ and $v=x+3y,$ the integral

$$
{∬}_{D}{e}^{x+y}\,dx\,dy
$$

can be written in terms of $u$ and $v$ as

- ${\int }_{-3}^{1}{\int }_{-4}^{0}\frac{e^{3 u - 2 v}}{2}\,du\,dv$
- ${\int }_{-3}^{1}{\int }_{-4}^{0}e^{2 u - v}\,du\,dv$
- ${\int }_{-3}^{1}{\int }_{-4}^{0}e^{u + v}\,du\,dv$
- ${\int }_{-3}^{1}{\int }_{-4}^{0}e^{2 u} e^{- 3 v}\,du\,dv$
- ${\int }_{-3}^{1}{\int }_{-4}^{0}2 e^{3 u - 2 v}\,du\,dv$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\,dx\,dy={∬}_{Δ}f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=2x+5y,\,v=x+3y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,-4\le u\le 0,\,-3\le v\le 1}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}2 & 5 \\ 1 & \text{ }\text{ }3\end{aligned}| \\  & =1.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=1.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

In this case, we first need to solve the transformation equations

$$
u=2x+5y,\,v=x+3y
$$

 
for $x$ and $y$, which gives

$$
x=3u-5v,\,y=2v-u.
$$

 

Now, performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}{e}^{x+y}\,dx\,dy & ={∬}_{Δ}{e}^{3u-5v+2v-u}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\,\text{d}v \\  & ={∬}_{Δ}{e}^{2u-3v}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\,\text{d}v \\  & ={∬}_{Δ}{e}^{2u-3v}\cdot |1|\,\text{d}u\,\text{d}v \\  & ={\int }_{-3}^{1}{\int }_{-4}^{0}{e}^{2u-3v}\,du\,dv.\end{aligned}
$$



## Generated easy / exponential / authored

Consider the region $D$ in the $xy$-plane, given by

$$
D={(x,y)\,:\,-3\le 2x+5y\le -1,\,-2\le x+3y\le 1}.
$$

By performing the change of variables $u=2x+5y$ and $v=x+3y,$ the integral

$$
{∬}_{D}{e}^{x+y}\,dx\,dy
$$

can be written in terms of $u$ and $v$ as

- ${\int }_{-2}^{1}{\int }_{-3}^{-1}\frac{e^{3 u - 2 v}}{2}\,du\,dv$
- ${\int }_{-2}^{1}{\int }_{-3}^{-1}e^{2 u - v}\,du\,dv$
- ${\int }_{-2}^{1}{\int }_{-3}^{-1}e^{2 u} e^{- 3 v}\,du\,dv$
- ${\int }_{-2}^{1}{\int }_{-3}^{-1}e^{u + v}\,du\,dv$
- ${\int }_{-2}^{1}{\int }_{-3}^{-1}2 e^{3 u - 2 v}\,du\,dv$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\,dx\,dy={∬}_{Δ}f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=2x+5y,\,v=x+3y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,-3\le u\le -1,\,-2\le v\le 1}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}2 & 5 \\ 1 & \text{ }\text{ }3\end{aligned}| \\  & =1.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=1.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

In this case, we first need to solve the transformation equations

$$
u=2x+5y,\,v=x+3y
$$

 
for $x$ and $y$, which gives

$$
x=3u-5v,\,y=2v-u.
$$

 

Now, performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}{e}^{x+y}\,dx\,dy & ={∬}_{Δ}{e}^{3u-5v+2v-u}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\,\text{d}v \\  & ={∬}_{Δ}{e}^{2u-3v}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\,\text{d}v \\  & ={∬}_{Δ}{e}^{2u-3v}\cdot |1|\,\text{d}u\,\text{d}v \\  & ={\int }_{-2}^{1}{\int }_{-3}^{-1}{e}^{2u-3v}\,du\,dv.\end{aligned}
$$



## Generated easy / sum_square / authored

Consider the region $D$ in the $xy$-plane, given by

$$
D={(x,y)\,:\,-4\le x+y\le 0,\,-3\le y-x\le 1}.
$$

By performing the change of variables $u=x+y$ and $v=y-x,$ the integral

$$
{∬}_{D}3(x+y)^{2}\,dx\,dy
$$

can be written in terms of $u$ and $v$ as

- ${\int }_{-4}^{0}{\int }_{-3}^{1}\frac{9 u^{2}}{2}\,dv\,du$
- ${\int }_{-4}^{0}{\int }_{-3}^{1}\frac{3 \left(u + v\right)^{2}}{2}\,dv\,du$
- ${\int }_{-4}^{0}{\int }_{-3}^{1}\frac{3 \left(u + v\right)^{2}}{4}\,dv\,du$
- ${\int }_{-4}^{0}{\int }_{-3}^{1}\frac{3 u^{2}}{2}\,dv\,du$
- ${\int }_{-4}^{0}{\int }_{-3}^{1}6 u^{2}\,dv\,du$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\,dx\,dy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x+y,\,v=y-x
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,-4\le u\le 0,\,-3\le v\le 1}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}1 & 1 \\ -1 & \text{ }\text{ }1\end{aligned}| \\  & =2.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{2}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}3(x+y)^{2}\,dx\,dy & ={∬}_{Δ}3{u}^{2}|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}3{u}^{2}|\frac{1}{2}|\text{d}u\,\text{d}v \\  & =\frac{3}{2}{\int }_{-4}^{0}{\int }_{-3}^{1}{u}^{2}\,dv\,du.\end{aligned}
$$



## Generated easy / sum_square / authored

Consider the region $D$ in the $xy$-plane, given by

$$
D={(x,y)\,:\,-3\le x+y\le -1,\,-2\le y-x\le 1}.
$$

By performing the change of variables $u=x+y$ and $v=y-x,$ the integral

$$
{∬}_{D}3(x+y)^{2}\,dx\,dy
$$

can be written in terms of $u$ and $v$ as

- ${\int }_{-3}^{-1}{\int }_{-2}^{1}\frac{9 u^{2}}{2}\,dv\,du$
- ${\int }_{-3}^{-1}{\int }_{-2}^{1}\frac{3 \left(u + v\right)^{2}}{2}\,dv\,du$
- ${\int }_{-3}^{-1}{\int }_{-2}^{1}\frac{3 u^{2}}{2}\,dv\,du$
- ${\int }_{-3}^{-1}{\int }_{-2}^{1}\frac{3 \left(u + v\right)^{2}}{4}\,dv\,du$
- ${\int }_{-3}^{-1}{\int }_{-2}^{1}6 u^{2}\,dv\,du$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\,dx\,dy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x+y,\,v=y-x
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,-3\le u\le -1,\,-2\le v\le 1}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}1 & 1 \\ -1 & \text{ }\text{ }1\end{aligned}| \\  & =2.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{2}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}3(x+y)^{2}\,dx\,dy & ={∬}_{Δ}3{u}^{2}|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}3{u}^{2}|\frac{1}{2}|\text{d}u\,\text{d}v \\  & =\frac{3}{2}{\int }_{-3}^{-1}{\int }_{-2}^{1}{u}^{2}\,dv\,du.\end{aligned}
$$



## Generated moderate / ratio_product / authored

Using the change of variables $u=\frac{y}{{x}^{2}}$ and $v=xy,$ evaluate the double integral

$$
{∬}_{D}xy\,dx\,dy,
$$

where $D={(x,y)\,:\,{x}^{2}\le y\le 9{x}^{2},\,1\le xy\le 8}.$

- $\frac{1022 \ln{\left(3 \right)}}{9}$
- $21 \ln{\left(3 \right)}$
- $- 21 \ln{\left(3 \right)}$
- $63 \ln{\left(3 \right)}$
- $\frac{14 \ln{\left(3 \right)}}{3}$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\,dx\,dy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=\frac{y}{{x}^{2}},\,v=xy
$$

 
gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,1\le u\le 9,\,1\le v\le 8}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-\frac{2y}{{x}^{3}} & \frac{1}{{x}^{2}} \\ y & \text{ }\text{ }x\end{aligned}| \\  & =-\frac{3y}{{x}^{2}}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{(-\frac{3y}{{x}^{2}})}=-\frac{1}{3u}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}xy\,dx\,dy & ={∬}_{Δ}v|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}v\cdot |\frac{1}{3u}|\,\text{d}u\,\text{d}v \\  & =\frac{1}{3}{\int }_{1}^{8}{\int }_{1}^{9}\frac{v}{u}\,\text{d}u\,\text{d}v \\  & =\frac{1}{3}{\int }_{1}^{8}v[{\int }_{1}^{9}\frac{1}{u}\,\text{d}u]\text{d}v \\  & =\frac{1}{3}{\int }_{1}^{8}v[\operatorname{ln}⁡|u|\,{|}_{1}^{9}]dv \\  & =\frac{1}{3}{\int }_{1}^{8}v(\operatorname{ln}⁡9-\operatorname{ln}⁡1)\,dv \\  & =\frac{2\operatorname{ln}⁡3}{3}{\int }_{1}^{8}v\,dv \\  & =\frac{2\operatorname{ln}⁡3}{3}\cdot \frac{1}{2}{v}^{2}\,{|}_{1}^{8} \\  & =\frac{\operatorname{ln}⁡3}{3}\cdot (64-1) \\  & =21\operatorname{ln}⁡3.\end{aligned}
$$



## Generated moderate / ratio_product / authored

Using the change of variables $u=\frac{y}{{x}^{2}}$ and $v=xy,$ evaluate the double integral

$$
{∬}_{D}xy\,dx\,dy,
$$

where $D={(x,y)\,:\,{x}^{2}\le y\le 4{x}^{2},\,2\le xy\le 5}.$

- $26 \ln{\left(2 \right)}$
- $- 7 \ln{\left(2 \right)}$
- $7 \ln{\left(2 \right)}$
- $2 \ln{\left(2 \right)}$
- $21 \ln{\left(2 \right)}$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\,dx\,dy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=\frac{y}{{x}^{2}},\,v=xy
$$

 
gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,1\le u\le 4,\,2\le v\le 5}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-\frac{2y}{{x}^{3}} & \frac{1}{{x}^{2}} \\ y & \text{ }\text{ }x\end{aligned}| \\  & =-\frac{3y}{{x}^{2}}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{(-\frac{3y}{{x}^{2}})}=-\frac{1}{3u}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}xy\,dx\,dy & ={∬}_{Δ}v|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}v\cdot |\frac{1}{3u}|\,\text{d}u\,\text{d}v \\  & =\frac{1}{3}{\int }_{2}^{5}{\int }_{1}^{4}\frac{v}{u}\,\text{d}u\,\text{d}v \\  & =\frac{1}{3}{\int }_{2}^{5}v[{\int }_{1}^{4}\frac{1}{u}\,\text{d}u]\text{d}v \\  & =\frac{1}{3}{\int }_{2}^{5}v[\operatorname{ln}⁡|u|\,{|}_{1}^{4}]dv \\  & =\frac{1}{3}{\int }_{2}^{5}v(\operatorname{ln}⁡4-\operatorname{ln}⁡1)\,dv \\  & =\frac{2\operatorname{ln}⁡2}{3}{\int }_{2}^{5}v\,dv \\  & =\frac{2\operatorname{ln}⁡2}{3}\cdot \frac{1}{2}{v}^{2}\,{|}_{2}^{5} \\  & =\frac{\operatorname{ln}⁡2}{3}\cdot (25-4) \\  & =7\operatorname{ln}⁡2.\end{aligned}
$$



## Generated hard / ratio_product_squared / authored

Using the change of variables $u=\frac{y}{{x}^{2}}$ and $v=xy,$ evaluate the double integral

$$
{∬}_{D}(xy)^{2}\,dx\,dy,
$$

where $D={(x,y)\,:\,{x}^{2}\le y\le 9{x}^{2},\,1\le xy\le 5}.$

- $104 \ln{\left(3 \right)}$
- $- \frac{248 \ln{\left(3 \right)}}{9}$
- $\frac{8 \ln{\left(3 \right)}}{3}$
- $\frac{248 \ln{\left(3 \right)}}{9}$
- $\frac{248 \ln{\left(3 \right)}}{3}$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\,dx\,dy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=\frac{y}{{x}^{2}},\,v=xy
$$

 
gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,1\le u\le 9,\,1\le v\le 5}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-\frac{2y}{{x}^{3}} & \frac{1}{{x}^{2}} \\ y & \text{ }\text{ }x\end{aligned}| \\  & =-\frac{3y}{{x}^{2}}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{(-\frac{3y}{{x}^{2}})}=-\frac{1}{3u}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}(xy)^{2}\,dx\,dy & ={∬}_{Δ}{v}^{2}|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}{v}^{2}\cdot |\frac{1}{3u}|\,\text{d}u\,\text{d}v \\  & =\frac{1}{3}{\int }_{1}^{5}{\int }_{1}^{9}\frac{{v}^{2}}{u}\,\text{d}u\,\text{d}v \\  & =\frac{1}{3}{\int }_{1}^{5}{v}^{2}[{\int }_{1}^{9}\frac{1}{u}\,\text{d}u]\text{d}v \\  & =\frac{1}{3}{\int }_{1}^{5}{v}^{2}[\operatorname{ln}⁡|u|\,{|}_{1}^{9}]dv \\  & =\frac{1}{3}{\int }_{1}^{5}{v}^{2}(\operatorname{ln}⁡9-\operatorname{ln}⁡1)\,dv \\  & =\frac{2\operatorname{ln}⁡3}{3}{\int }_{1}^{5}{v}^{2}\,dv \\  & =\frac{2\operatorname{ln}⁡3}{3}\cdot \frac{1}{3}{v}^{3}\,{|}_{1}^{5} \\  & =\frac{2\operatorname{ln}⁡3}{9}\cdot (125-1) \\  & =\frac{248\operatorname{ln}⁡3}{9}.\end{aligned}
$$



## Generated hard / ratio_product_squared / authored

Using the change of variables $u=\frac{y}{{x}^{2}}$ and $v=xy,$ evaluate the double integral

$$
{∬}_{D}(xy)^{2}\,dx\,dy,
$$

where $D={(x,y)\,:\,{x}^{2}\le y\le 4{x}^{2},\,2\le xy\le 5}.$

- $\frac{203 \ln{\left(2 \right)}}{2}$
- $- 26 \ln{\left(2 \right)}$
- $26 \ln{\left(2 \right)}$
- $2 \ln{\left(2 \right)}$
- $78 \ln{\left(2 \right)}$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\,dx\,dy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=\frac{y}{{x}^{2}},\,v=xy
$$

 
gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,1\le u\le 4,\,2\le v\le 5}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-\frac{2y}{{x}^{3}} & \frac{1}{{x}^{2}} \\ y & \text{ }\text{ }x\end{aligned}| \\  & =-\frac{3y}{{x}^{2}}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{(-\frac{3y}{{x}^{2}})}=-\frac{1}{3u}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}(xy)^{2}\,dx\,dy & ={∬}_{Δ}{v}^{2}|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}{v}^{2}\cdot |\frac{1}{3u}|\,\text{d}u\,\text{d}v \\  & =\frac{1}{3}{\int }_{2}^{5}{\int }_{1}^{4}\frac{{v}^{2}}{u}\,\text{d}u\,\text{d}v \\  & =\frac{1}{3}{\int }_{2}^{5}{v}^{2}[{\int }_{1}^{4}\frac{1}{u}\,\text{d}u]\text{d}v \\  & =\frac{1}{3}{\int }_{2}^{5}{v}^{2}[\operatorname{ln}⁡|u|\,{|}_{1}^{4}]dv \\  & =\frac{1}{3}{\int }_{2}^{5}{v}^{2}(\operatorname{ln}⁡4-\operatorname{ln}⁡1)\,dv \\  & =\frac{2\operatorname{ln}⁡2}{3}{\int }_{2}^{5}{v}^{2}\,dv \\  & =\frac{2\operatorname{ln}⁡2}{3}\cdot \frac{1}{3}{v}^{3}\,{|}_{2}^{5} \\  & =\frac{2\operatorname{ln}⁡2}{9}\cdot (125-8) \\  & =26\operatorname{ln}⁡2.\end{aligned}
$$



## Generated easy / difference / observed

Consider the finite region $D$ in the $xy$-plane, given by

$D = {(x, y): 0 \le x + y \le 3, 0 \le y - x \le 3}$.

By performing the change of variables
$u = x + y$
and
$v = y - x$,
the integral
$∬_(D)(y^{2} - x^{2})dxdy$
can be written in terms of $u$ and $v$ as

- $2\displaystyle \int_{0}^{3}\displaystyle \int_{0}^{3}uvdvdu$
- $\frac{1}{2}\displaystyle \int_{0}^{3}\displaystyle \int_{0}^{3}uvdvdu$
- $\displaystyle \int_{0}^{3}\displaystyle \int_{0}^{3}uvdvdu$
- $\displaystyle \int_{0}^{3}\displaystyle \int_{0}^{3}(v^{2} - u^{2})dvdu$
- $\frac{1}{2}\displaystyle \int_{0}^{3}\displaystyle \int_{0}^{3}(u^{2} - v^{2})dvdu$



## Generated moderate / sum_product_evidence / observed

Using the change of variables $u = xy$ and $v = y + x$, evaluate the double integral

$∬_(D) \mid y - x \mid e^{xy}dxdy$,
where $D = {(x, y): 1 \le xy \le 5, 1 \le y + x \le 10}$.

- $5(1 - e^{4})$
- $9(e^{4} - e)$
- $10(e^{5} - 1)$
- $9(e^{5} - e)$
- $5(e^{5} - 1)$



## Generated moderate / ratio_product / observed

Using the change of variables $u=\frac{y}{{x}^{2}}$ and $v=xy,$ evaluate the double integral

$$
{∬}_{D}xy\,dx\,dy,
$$

where $D={(x,y)\,:\,{x}^{2}\le y\le 4{x}^{2},\,1\le xy\le 6}.$

- $6$
- $\frac{9}{2}$
- $3\operatorname{ln}⁡2$
- $\frac{11}{4}$
- $\frac{35\operatorname{ln}⁡2}{3}$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\,dx\,dy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=\frac{y}{{x}^{2}},\,v=xy
$$

 
gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows::

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,1\le u\le 4,\,1\le v\le 6}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-\frac{2y}{{x}^{3}} & \frac{1}{{x}^{2}} \\ y & \text{ }\text{ }x\end{aligned}| \\  & =-\frac{3y}{{x}^{2}}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{(-\frac{3y}{{x}^{2}})}=-\frac{1}{3u}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}xy\,dx\,dy & ={∬}_{Δ}v|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}v\cdot |\frac{1}{3u}|\,\text{d}u\,\text{d}v \\  & =\frac{1}{3}{\int }_{1}^{6}{\int }_{1}^{4}\frac{v}{u}\,\text{d}u\,\text{d}v \\  & =\frac{1}{3}{\int }_{1}^{6}v[{\int }_{1}^{4}\frac{1}{u}\,\text{d}u]\text{d}v \\  & =\frac{1}{3}{\int }_{1}^{6}v[\operatorname{ln}⁡|u|\,{|}_{1}^{4}]dv \\  & =\frac{1}{3}{\int }_{1}^{6}v(\operatorname{ln}⁡4-\operatorname{ln}⁡1)\,dv \\  & =\frac{2\operatorname{ln}⁡2}{3}{\int }_{1}^{6}v\,dv \\  & =\frac{2\operatorname{ln}⁡2}{3}\cdot \frac{1}{2}{v}^{2}\,{|}_{1}^{6} \\  & =\frac{\operatorname{ln}⁡2}{3}\cdot (36-1) \\  & =\frac{35\operatorname{ln}⁡2}{3}.\end{aligned}
$$



## Generated easy / triangular_quadratic / observed

Consider the region $D$ in the $xy$-plane, given by

$$
D={(x,y)\,:\,0\le 2x+y\le 5,\,0\le y\le 2}.
$$

  

By performing the change of variables $u=2x+y$ and $v=y,$ the integral 

$$
{∬}_{D}(2xy+{x}^{2})\,dx\,dy
$$

can be written in terms of $u$ and $v$ as

- $\frac{1}{4}{\int }_{0}^{2}{\int }_{0}^{5}(uv-2{v}^{2}+{v}^{2})\,du\,dv$
- $\frac{1}{2}{\int }_{0}^{2}{\int }_{0}^{5}(2uv-{u}^{2}+{v}^{2})\,du\,dv$
- $\frac{1}{8}{\int }_{0}^{2}{\int }_{0}^{5}(uv-{v}^{2}+3{u}^{2})\,du\,dv$
- $\frac{1}{8}{\int }_{0}^{2}{\int }_{0}^{5}(2uv-3{v}^{2}+{u}^{2})\,du\,dv$
- $\frac{1}{4}{\int }_{0}^{2}{\int }_{0}^{5}(uv-5{v}^{2}-{u}^{2})\,du\,dv$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\text{ }dx\,dy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=2x+y,\,v=y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,0\le u\le 5,\,0\le v\le 2}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}2 & 1 \\ 0 & \text{ }\text{ }1\end{aligned}| \\  & =2.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{2}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

In this case, we first need to solve the transformation equations

$$
u=2x+y,\,v=y
$$

 
for $x$ and $y$, which gives

$$
x=\frac{u-v}{2},\,y=v.
$$

 

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}(2xy+{x}^{2})\,dx\,dy & ={∬}_{Δ}[2\cdot \frac{u-v}{2}\cdot v+{(\frac{u-v}{2})}^{2}]|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}(uv-{v}^{2}+\frac{{u}^{2}-2uv+{v}^{2}}{4})\frac{1}{2}\,du\,dv \\  & =\frac{1}{8}{\int }_{0}^{2}{\int }_{0}^{5}(2uv-3{v}^{2}+{u}^{2})\,du\,dv.\end{aligned}
$$



## Generated easy / product / observed

Consider the region $D$ in the $xy$-plane, given by

$$
D={(x,y)\,:\,-1\le y-x\le 1,\,0\le x+y\le 2}.
$$

By performing the change of variables $u=y-x$ and $v=x+y,$ the integral

$$
{∬}_{D}8xy\,dx\,dy
$$

can be written in terms of $u$ and $v$ as

- $2{\int }_{0}^{2}{\int }_{-1}^{1}({v}^{2}-{u}^{2})\,du\,dv$
- ${\int }_{0}^{2}{\int }_{-1}^{1}(v-u)^{4}\,du\,dv$
- $2{\int }_{0}^{2}{\int }_{-1}^{1}(v-u)^{2}\,du\,dv$
- ${\int }_{0}^{2}{\int }_{-1}^{1}({v}^{2}-{u}^{2})\,du\,dv$
- $\frac{1}{2}{\int }_{0}^{2}{\int }_{-1}^{1}(v-u)^{2}\,du\,dv$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\text{ }dx\,dy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=y-x,\,v=x+y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,-1\le u\le 1,\,0\le v\le 2}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-1 & 1 \\ 1 & \text{ }\text{ }1\end{aligned}| \\  & =-2.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=-\frac{1}{2}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

In this case, we first need to solve the transformation equations

$$
u=y-x,\,v=x+y
$$

 
for $x$ and $y$, which gives

$$
x=\frac{v-u}{2},\,y=\frac{v+u}{2}.
$$

 

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}8xy\,dx\,dy & ={∬}_{Δ}8(\frac{v-u}{2})(\frac{v+u}{2})|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}2({v}^{2}-{u}^{2})|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}2({v}^{2}-{u}^{2})|-\frac{1}{2}|\text{d}u\,\text{d}v \\  & ={\int }_{0}^{2}{\int }_{-1}^{1}({v}^{2}-{u}^{2})\,du\,dv.\end{aligned}
$$



## Generated easy / exponential / observed

Consider the region $D$ in the $xy$-plane, given by

$$
D={(x,y)\,:\,0\le 2x+5y\le 2,\,0\le x+3y\le 5}.
$$

By performing the change of variables $u=2x+5y$ and $v=x+3y,$ the integral

$$
{∬}_{D}{e}^{x+y}\,dx\,dy
$$

can be written in terms of $u$ and $v$ as

- ${\int }_{0}^{5}{\int }_{0}^{2}{e}^{u+v}\,du\,dv$
- $2{\int }_{0}^{5}{\int }_{0}^{2}{e}^{3u-2v}\,du\,dv$
- ${\int }_{0}^{5}{\int }_{0}^{2}{e}^{2u-v}\,du\,dv$
- ${\int }_{0}^{5}{\int }_{0}^{2}{e}^{2u-3v}\,du\,dv$
- $\frac{1}{2}{\int }_{0}^{5}{\int }_{0}^{2}{e}^{3u-2v}\,du\,dv$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\,dx\,dy={∬}_{Δ}f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=2x+5y,\,v=x+3y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,0\le u\le 2,\,0\le v\le 5}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}2 & 5 \\ 1 & \text{ }\text{ }3\end{aligned}| \\  & =1.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=1.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

In this case, we first need to solve the transformation equations

$$
u=2x+5y,\,v=x+3y
$$

 
for $x$ and $y$, which gives

$$
x=3u-5v,\,y=2v-u.
$$

 

Now, performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}{e}^{x+y}\,dx\,dy & ={∬}_{Δ}{e}^{3u-5v+2v-u}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\,\text{d}v \\  & ={∬}_{Δ}{e}^{2u-3v}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\,\text{d}v \\  & ={∬}_{Δ}{e}^{2u-3v}\cdot |1|\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{5}{\int }_{0}^{2}{e}^{2u-3v}\,du\,dv.\end{aligned}
$$



## Generated easy / sum_square / observed

Consider the region $D$ in the $xy$-plane, given by

$$
D={(x,y)\,:\,-1\le x+y\le 3,\,-4\le y-x\le 0}.
$$

By performing the change of variables $u=x+y$ and $v=y-x,$ the integral

$$
{∬}_{D}3(x+y)^{2}\,dx\,dy
$$

can be written in terms of $u$ and $v$ as

- $\frac{3}{2}{\int }_{-1}^{3}{\int }_{-4}^{0}{u}^{2}\,dv\,du$
- $6{\int }_{-1}^{3}{\int }_{-4}^{0}{u}^{2}\,dv\,du$
- $\frac{3}{4}{\int }_{-1}^{3}{\int }_{-4}^{0}(u+v)^{2}\,dv\,du$
- $\frac{3}{2}{\int }_{-1}^{3}{\int }_{-4}^{0}(u+v)^{2}\,dv\,du$
- $\frac{9}{2}{\int }_{-1}^{3}{\int }_{-4}^{0}{u}^{2}\,dv\,du$

Let's define a transformation $T$ as follows:

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required integral, we can use the change of variables formula

$$
{∬}_{D}f(x,y)\,dx\,dy={∬}_{Δ}\text{ }f(x(u,v),y(u,v))|\frac{∂(x,y)}{∂(u,v)}|du\,dv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

Note that the change of variables

$$
u=x+y,\,v=y-x
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required integral, we proceed as follows:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

Our domain in the $uv$-plane is

$$
\begin{aligned}Δ & ={(u,v)\,:\,-1\le u\le 3,\,-4\le v\le 0}.\end{aligned}
$$

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}1 & 1 \\ -1 & \text{ }\text{ }1\end{aligned}| \\  & =2.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{2}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Perform the change of variables:

Performing the change of variables, we obtain

$$
\begin{aligned}{∬}_{D}3(x+y)^{2}\,dx\,dy & ={∬}_{Δ}3{u}^{2}|\frac{∂(x,y)}{∂(u,v)}|\text{d}u\,\text{d}v \\  & ={∬}_{Δ}3{u}^{2}|\frac{1}{2}|\text{d}u\,\text{d}v \\  & =\frac{3}{2}{\int }_{-1}^{3}{\int }_{-4}^{0}{u}^{2}\,dv\,du.\end{aligned}
$$

