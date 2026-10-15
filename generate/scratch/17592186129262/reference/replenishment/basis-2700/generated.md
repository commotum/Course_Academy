Use a change of variables to calculate the area of the finite region $D$ in the first quadrant bounded by the following curves and lines.
$y = \frac{1}{x}, y = \frac{4}{x}, y = 3x, y = 4x$

- $\frac{1}{2}$
- $\frac{3}{2}\operatorname{ln}⁡4$
- $\frac{3}{8}\operatorname{ln}⁡\frac{4}{3}$
- $\frac{3}{2}\operatorname{ln}⁡\frac{4}{3}$
- $3\operatorname{ln}⁡\frac{4}{3}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

We'll assume this transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv,
$$

  

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

To compute the required area, we proceed in five steps:

**Step 1**: Find a suitable change of variables.

Notice that we can rewrite the equations of our curves as follows:

$$
xy=1,\,xy=4,\,\frac{y}{x}=3,\,\frac{y}{x}=4
$$

This suggests the following change of variables:

$$
u=xy,\,v=\frac{y}{x}
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=xy$ into the equations of the first and second curves:

$$
\begin{aligned} & xy=1\,⟹\,u=1 \\  & xy=4\,⟹\,u=4\end{aligned}
$$

And we substitute $v=\frac{y}{x}$ into the equations of the third and fourth curves:

$$
\begin{aligned} & \frac{y}{x}=3\,⟹\,v=3 \\  & \frac{y}{x}=4\,⟹\,v=4\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
Δ=\{(u,v)\,:\,1\le u\le 4,\,3\le v\le 4\}
$$

![](images/88/88750e49134feaa087b1f48ddee12faeb30ca8a31dd3b5bebb989f4c7c891ae7.png)

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}y & x \\ -\frac{y}{x^2} & \frac{1}{x}\end{aligned}| \\  & =\frac{y}{x}+\frac{y}{x} \\  & =2v.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{2v}.
$$

Note that $\frac{∂(u,v)}{∂(x,y)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 5**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}\frac{1}{2v}\,\text{d}u\text{d}v \\  & =\frac{1}{2}{\int }_{1}^{4}\,\text{d}u{\int }_{3}^{4}\frac{1}{v}\,\text{d}v \\  & =\frac{1}{2}\cdot (4-1)\cdot (\operatorname{ln}⁡4-\operatorname{ln}⁡3) \\  & =\frac{3}{2}\operatorname{ln}⁡\frac{4}{3}\end{aligned}
$$

---

Use a change of variables to calculate the area of the finite region $D$ in the first quadrant bounded by the following curves and lines.
$y = \frac{3}{x}, y = \frac{7}{x}, y = 4x, y = 5x$

- $2\operatorname{ln}⁡\frac{5}{4}$
- $\frac{2}{5}\operatorname{ln}⁡\frac{5}{4}$
- $4\operatorname{ln}⁡\frac{5}{4}$
- $2\operatorname{ln}⁡5$
- $\frac{1}{2}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

We'll assume this transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv,
$$

  

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

To compute the required area, we proceed in five steps:

**Step 1**: Find a suitable change of variables.

Notice that we can rewrite the equations of our curves as follows:

$$
xy=3,\,xy=7,\,\frac{y}{x}=4,\,\frac{y}{x}=5
$$

This suggests the following change of variables:

$$
u=xy,\,v=\frac{y}{x}
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=xy$ into the equations of the first and second curves:

$$
\begin{aligned} & xy=3\,⟹\,u=3 \\  & xy=7\,⟹\,u=7\end{aligned}
$$

And we substitute $v=\frac{y}{x}$ into the equations of the third and fourth curves:

$$
\begin{aligned} & \frac{y}{x}=4\,⟹\,v=4 \\  & \frac{y}{x}=5\,⟹\,v=5\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
Δ=\{(u,v)\,:\,3\le u\le 7,\,4\le v\le 5\}
$$

![](images/3d/3dc524083463c8c370ff1f79d68093f0d3f2c2fe1ceb5cd47824782e35a0bac9.png)

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}y & x \\ -\frac{y}{x^2} & \frac{1}{x}\end{aligned}| \\  & =\frac{y}{x}+\frac{y}{x} \\  & =2v.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{2v}.
$$

Note that $\frac{∂(u,v)}{∂(x,y)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 5**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}\frac{1}{2v}\,\text{d}u\text{d}v \\  & =\frac{1}{2}{\int }_{3}^{7}\,\text{d}u{\int }_{4}^{5}\frac{1}{v}\,\text{d}v \\  & =\frac{1}{2}\cdot (7-3)\cdot (\operatorname{ln}⁡5-\operatorname{ln}⁡4) \\  & =2\operatorname{ln}⁡\frac{5}{4}\end{aligned}
$$

---

Use a change of variables to calculate the area of the finite region $D$ in the first quadrant bounded by the following curves and lines.
$y = \frac{2}{x}, y = \frac{5}{x}, y = 2x, y = 3x$

- $\frac{3}{2}\operatorname{ln}⁡\frac{3}{2}$
- $\frac{3}{2}\operatorname{ln}⁡3$
- $\frac{3}{4}$
- $3\operatorname{ln}⁡\frac{3}{2}$
- $\frac{1}{2}\operatorname{ln}⁡\frac{3}{2}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

We'll assume this transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv,
$$

  

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

To compute the required area, we proceed in five steps:

**Step 1**: Find a suitable change of variables.

Notice that we can rewrite the equations of our curves as follows:

$$
xy=2,\,xy=5,\,\frac{y}{x}=2,\,\frac{y}{x}=3
$$

This suggests the following change of variables:

$$
u=xy,\,v=\frac{y}{x}
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=xy$ into the equations of the first and second curves:

$$
\begin{aligned} & xy=2\,⟹\,u=2 \\  & xy=5\,⟹\,u=5\end{aligned}
$$

And we substitute $v=\frac{y}{x}$ into the equations of the third and fourth curves:

$$
\begin{aligned} & \frac{y}{x}=2\,⟹\,v=2 \\  & \frac{y}{x}=3\,⟹\,v=3\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
Δ=\{(u,v)\,:\,2\le u\le 5,\,2\le v\le 3\}
$$

![](images/2c/2cdd0431c256b72ded23c14fac4098b518a46603d46d5dfd238c54b3a46c66db.png)

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}y & x \\ -\frac{y}{x^2} & \frac{1}{x}\end{aligned}| \\  & =\frac{y}{x}+\frac{y}{x} \\  & =2v.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{2v}.
$$

Note that $\frac{∂(u,v)}{∂(x,y)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 5**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}\frac{1}{2v}\,\text{d}u\text{d}v \\  & =\frac{1}{2}{\int }_{2}^{5}\,\text{d}u{\int }_{2}^{3}\frac{1}{v}\,\text{d}v \\  & =\frac{1}{2}\cdot (5-2)\cdot (\operatorname{ln}⁡3-\operatorname{ln}⁡2) \\  & =\frac{3}{2}\operatorname{ln}⁡\frac{3}{2}\end{aligned}
$$

---

Use a change of variables to calculate the area of the finite region $D$ in the first quadrant bounded by the following curves and lines.
$y = \frac{3}{x}, y = \frac{7}{x}, y = 3x, y = 5x$

- $2\operatorname{ln}⁡5$
- $4\operatorname{ln}⁡\frac{5}{3}$
- $2\operatorname{ln}⁡\frac{5}{3}$
- $\frac{2}{3}$
- $\frac{2}{5}\operatorname{ln}⁡\frac{5}{3}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

We'll assume this transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv,
$$

  

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

To compute the required area, we proceed in five steps:

**Step 1**: Find a suitable change of variables.

Notice that we can rewrite the equations of our curves as follows:

$$
xy=3,\,xy=7,\,\frac{y}{x}=3,\,\frac{y}{x}=5
$$

This suggests the following change of variables:

$$
u=xy,\,v=\frac{y}{x}
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=xy$ into the equations of the first and second curves:

$$
\begin{aligned} & xy=3\,⟹\,u=3 \\  & xy=7\,⟹\,u=7\end{aligned}
$$

And we substitute $v=\frac{y}{x}$ into the equations of the third and fourth curves:

$$
\begin{aligned} & \frac{y}{x}=3\,⟹\,v=3 \\  & \frac{y}{x}=5\,⟹\,v=5\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
Δ=\{(u,v)\,:\,3\le u\le 7,\,3\le v\le 5\}
$$

![](images/cf/cf598751d1bb1edda1bb65fd5b94d2ad5805289c48716f69a71394fd3684e920.png)

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}y & x \\ -\frac{y}{x^2} & \frac{1}{x}\end{aligned}| \\  & =\frac{y}{x}+\frac{y}{x} \\  & =2v.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{2v}.
$$

Note that $\frac{∂(u,v)}{∂(x,y)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 5**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}\frac{1}{2v}\,\text{d}u\text{d}v \\  & =\frac{1}{2}{\int }_{3}^{7}\,\text{d}u{\int }_{3}^{5}\frac{1}{v}\,\text{d}v \\  & =\frac{1}{2}\cdot (7-3)\cdot (\operatorname{ln}⁡5-\operatorname{ln}⁡3) \\  & =2\operatorname{ln}⁡\frac{5}{3}\end{aligned}
$$

---

Use a change of variables to calculate the area of the finite region $D$ in the first quadrant bounded by the following curves and lines.
$y = \frac{4}{x}, y = \frac{5}{x}, y = 3x, y = 5x$

- $\operatorname{ln}⁡\frac{5}{3}$
- $\frac{1}{6}$
- $\frac{1}{2}\operatorname{ln}⁡\frac{5}{3}$
- $\frac{1}{10}\operatorname{ln}⁡\frac{5}{3}$
- $\frac{1}{2}\operatorname{ln}⁡5$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

We'll assume this transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv,
$$

  

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

To compute the required area, we proceed in five steps:

**Step 1**: Find a suitable change of variables.

Notice that we can rewrite the equations of our curves as follows:

$$
xy=4,\,xy=5,\,\frac{y}{x}=3,\,\frac{y}{x}=5
$$

This suggests the following change of variables:

$$
u=xy,\,v=\frac{y}{x}
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=xy$ into the equations of the first and second curves:

$$
\begin{aligned} & xy=4\,⟹\,u=4 \\  & xy=5\,⟹\,u=5\end{aligned}
$$

And we substitute $v=\frac{y}{x}$ into the equations of the third and fourth curves:

$$
\begin{aligned} & \frac{y}{x}=3\,⟹\,v=3 \\  & \frac{y}{x}=5\,⟹\,v=5\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
Δ=\{(u,v)\,:\,4\le u\le 5,\,3\le v\le 5\}
$$

![](images/56/560d4d074d9d07eb034d92b8f1dfabfc3e59d659c91d80c3fedf68367a575e41.png)

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}y & x \\ -\frac{y}{x^2} & \frac{1}{x}\end{aligned}| \\  & =\frac{y}{x}+\frac{y}{x} \\  & =2v.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{2v}.
$$

Note that $\frac{∂(u,v)}{∂(x,y)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 5**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}\frac{1}{2v}\,\text{d}u\text{d}v \\  & =\frac{1}{2}{\int }_{4}^{5}\,\text{d}u{\int }_{3}^{5}\frac{1}{v}\,\text{d}v \\  & =\frac{1}{2}\cdot (5-4)\cdot (\operatorname{ln}⁡5-\operatorname{ln}⁡3) \\  & =\frac{1}{2}\operatorname{ln}⁡\frac{5}{3}\end{aligned}
$$

---

Use a change of variables to calculate the area of the finite region $D$ in the first quadrant bounded by the following curves and lines.

$$
y=\frac{3}{{x}^{2}},\,y=\frac{6}{{x}^{2}},\,y=\frac{2}{x},\,y=\frac{6}{x}
$$

- $\frac{1}{4}\operatorname{ln}⁡2$
- $-4\operatorname{ln}⁡2$
- $4\operatorname{ln}⁡2$
- $12$
- $6\operatorname{ln}⁡2$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

We'll assume this transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv,
$$

  

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

To compute the required area, we proceed in five steps:

**Step 1**: Find a suitable change of variables.

Notice that we can rewrite the equations of our curves as follows:

$$
{x}^{2}y=3,\,{x}^{2}y=6,\,xy=2,\,xy=6
$$

This suggests the following change of variables:

$$
u={x}^{2}y,\,v=xy
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u={x}^{2}y$ into the equations of the first and second curves:

$$
\begin{aligned} & {x}^{2}y=3\,⟹\,u=3 \\  & {x}^{2}y=6\,⟹\,u=6\end{aligned}
$$

And we substitute $v=xy$ into the equations of the third and fourth curves:

$$
\begin{aligned} & xy=2\,⟹\,v=2 \\  & xy=6\,⟹\,v=6\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
Δ=\{(u,v)\,:\,3\le u\le 6,\,2\le v\le 6\}
$$

![](images/a4/a42d50fe797c9450b27acde75ac7b69ed3e4ea5acc6c9dc93cd6df18b9ed1882.png)

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}2xy & {x}^{2} \\ y & x\end{aligned}| \\  & =2{x}^{2}y-{x}^{2}y \\  & =u.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{u}.
$$

Note that $\frac{∂(u,v)}{∂(x,y)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 5**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|\frac{1}{u}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}\frac{1}{u}\,\text{d}u\text{d}v \\  & ={\int }_{3}^{6}\frac{1}{u}\,\text{d}u{\int }_{2}^{6}\,\text{d}v \\  & =(\operatorname{ln}⁡6-\operatorname{ln}⁡3)\cdot (6-2) \\  & =4\operatorname{ln}⁡2\end{aligned}
$$

---

Use a change of variables to calculate the area of the finite region $D$ in the first quadrant bounded by the following curves and lines.

$$
y=\frac{4}{{x}^{2}},\,y=\frac{7}{{x}^{2}},\,y=\frac{4}{x},\,y=\frac{8}{x}
$$

- $8\operatorname{ln}⁡\frac{7}{4}$
- $12$
- $4\operatorname{ln}⁡\frac{7}{4}$
- $\frac{1}{4}\operatorname{ln}⁡\frac{7}{4}$
- $-4\operatorname{ln}⁡\frac{7}{4}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

We'll assume this transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv,
$$

  

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

To compute the required area, we proceed in five steps:

**Step 1**: Find a suitable change of variables.

Notice that we can rewrite the equations of our curves as follows:

$$
{x}^{2}y=4,\,{x}^{2}y=7,\,xy=4,\,xy=8
$$

This suggests the following change of variables:

$$
u={x}^{2}y,\,v=xy
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u={x}^{2}y$ into the equations of the first and second curves:

$$
\begin{aligned} & {x}^{2}y=4\,⟹\,u=4 \\  & {x}^{2}y=7\,⟹\,u=7\end{aligned}
$$

And we substitute $v=xy$ into the equations of the third and fourth curves:

$$
\begin{aligned} & xy=4\,⟹\,v=4 \\  & xy=8\,⟹\,v=8\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
Δ=\{(u,v)\,:\,4\le u\le 7,\,4\le v\le 8\}
$$

![](images/47/475635e9575bd2f30069f2ee5f3b29bd6d7bf47db0cb6d5a96f981e36b8117c6.png)

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}2xy & {x}^{2} \\ y & x\end{aligned}| \\  & =2{x}^{2}y-{x}^{2}y \\  & =u.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{u}.
$$

Note that $\frac{∂(u,v)}{∂(x,y)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 5**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|\frac{1}{u}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}\frac{1}{u}\,\text{d}u\text{d}v \\  & ={\int }_{4}^{7}\frac{1}{u}\,\text{d}u{\int }_{4}^{8}\,\text{d}v \\  & =(\operatorname{ln}⁡7-\operatorname{ln}⁡4)\cdot (8-4) \\  & =4\operatorname{ln}⁡\frac{7}{4}\end{aligned}
$$

---

Use a change of variables to calculate the area of the finite region $D$ in the first quadrant bounded by the following curves and lines.

$$
y=\frac{2}{x},\,y=\frac{5}{x},\,x=2{y}^{2},\,x=3{y}^{2}
$$

- $\operatorname{ln}⁡\frac{3}{2}$
- $\operatorname{ln}⁡3$
- $\frac{1}{3}\operatorname{ln}⁡\frac{3}{2}$
- $-\operatorname{ln}⁡\frac{3}{2}$
- $3\operatorname{ln}⁡\frac{3}{2}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

We'll assume this transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv,
$$

  

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$

To compute the required area, we proceed in five steps:

**Step 1**: Find a suitable change of variables.

Notice that we can rewrite the equations of our curves as follows:

$$
xy=2,\,xy=5,\,\frac{x}{{y}^{2}}=2,\,\frac{x}{{y}^{2}}=3
$$

This suggests the following change of variables:

$$
u=xy,\,v=\frac{x}{{y}^{2}}
$$

This change of variables gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

**Step 2**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=xy$ into the equations of the first and second curves:

$$
\begin{aligned} & xy=2\,⟹\,u=2 \\  & xy=5\,⟹\,u=5\end{aligned}
$$

And we substitute $v=\frac{x}{{y}^{2}}$ into the equations of the third and fourth curves:

$$
\begin{aligned} & \frac{x}{{y}^{2}}=2\,⟹\,v=2 \\  & \frac{x}{{y}^{2}}=3\,⟹\,v=3\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
Δ=\{(u,v)\,:\,2\le u\le 5,\,2\le v\le 3\}
$$

![](images/2c/2cdd0431c256b72ded23c14fac4098b518a46603d46d5dfd238c54b3a46c66db.png)

**Step 3**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}y & x \\ \frac{1}{{y}^{2}} & -\frac{2x}{{y}^{3}}\end{aligned}| \\  & =-\frac{2x}{{y}^{2}}-\frac{x}{{y}^{2}} \\  & =-\frac{3x}{{y}^{2}} \\  & =-3v.\end{aligned}
$$

**Step 4**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=-\frac{1}{3v}.
$$

Note that $\frac{∂(u,v)}{∂(x,y)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 5**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|-\frac{1}{3v}|\,\text{d}u\text{d}v \\  & =\frac{1}{3}{∬}_{Δ}\frac{1}{v}\,\text{d}u\text{d}v \\  & =\frac{1}{3}{\int }_{2}^{5}\,\text{d}u{\int }_{2}^{3}\frac{1}{v}\,\text{d}v \\  & =\frac{1}{3}\cdot (5-2)\cdot (\operatorname{ln}⁡3-\operatorname{ln}⁡2) \\  & =\operatorname{ln}⁡\frac{3}{2}\end{aligned}
$$