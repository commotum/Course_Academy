Using the change of variables

$$
u=- 2 x + y,\qquad v=x + y,
$$

calculate the area of the finite region $D$ bounded by the lines

$$
y=2 x,\qquad y=2 x + 2,\qquad y=3 - x,\qquad y=4 - x.
$$

- $2$
- $6$
- $1$
- $\frac{2}{3}$
- $\frac{1}{3}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=- 2 x + y,\,v=x + y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=- 2 x + y$ into the equations of the first and second lines:

$$
\begin{aligned} & y=2 x & ⟹\, & - 2 x + y=0 & ⟹\, & u=0 \\  & y=2 x + 2 & ⟹\, & - 2 x + y=2 & ⟹\, & u=2\end{aligned}
$$

And we substitute $v=x + y$ into the equations of the third and fourth lines:

$$
\begin{aligned} & y=3 - x & ⟹\, & x + y=3 & ⟹\, & v=3 \\  & y=4 - x & ⟹\, & x + y=4 & ⟹\, & v=4\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v)\,:\,0\le u\le 2,\,3\le v\le 4\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/a90897a90fff9d86565f9a6cb76068450007b36a6abc7d9cbe6d4fee841c87b4.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-2 & 1 \\ 1 & 1\end{aligned}| \\  & =-3.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=- \frac{1}{3}=- \frac{1}{3}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|- \frac{1}{3}|\,\text{d}u\text{d}v \\  & =\frac{1}{3}{∬}_{Δ}\,\text{d}u\text{d}v \\  & =\frac{1}{3}\cdot \text{Area}(Δ) \\  & =\frac{1}{3}\cdot 2\cdot 1 \\  & =\frac{2}{3}\end{aligned}
$$

---

Using the change of variables

$$
u=- 2 x + y,\qquad v=4 x + y,
$$

calculate the area of the finite region $D$ bounded by the lines

$$
y=2 x - 2,\qquad y=2 x + 2,\qquad y=2 - 4 x,\qquad y=4 - 4 x.
$$

- $4$
- $2$
- $8$
- $\frac{4}{3}$
- $48$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=- 2 x + y,\,v=4 x + y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=- 2 x + y$ into the equations of the first and second lines:

$$
\begin{aligned} & y=2 x - 2 & ⟹\, & - 2 x + y=-2 & ⟹\, & u=-2 \\  & y=2 x + 2 & ⟹\, & - 2 x + y=2 & ⟹\, & u=2\end{aligned}
$$

And we substitute $v=4 x + y$ into the equations of the third and fourth lines:

$$
\begin{aligned} & y=2 - 4 x & ⟹\, & 4 x + y=2 & ⟹\, & v=2 \\  & y=4 - 4 x & ⟹\, & 4 x + y=4 & ⟹\, & v=4\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v)\,:\,-2\le u\le 2,\,2\le v\le 4\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/776efab6daa56a457ac77161f3cd364a866b4c3e8ff7aabf7a8fbd8bde5cd051.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-2 & 1 \\ 4 & 1\end{aligned}| \\  & =-6.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=- \frac{1}{6}=- \frac{1}{6}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|- \frac{1}{6}|\,\text{d}u\text{d}v \\  & =\frac{1}{6}{∬}_{Δ}\,\text{d}u\text{d}v \\  & =\frac{1}{6}\cdot \text{Area}(Δ) \\  & =\frac{1}{6}\cdot 4\cdot 2 \\  & =\frac{4}{3}\end{aligned}
$$

---

Using the change of variables

$$
u=- 2 x + y,\qquad v=4 x + y,
$$

calculate the area of the finite region $D$ bounded by the lines

$$
y=2 x,\qquad y=2 x + 3,\qquad y=1 - 4 x,\qquad y=5 - 4 x.
$$

- $12$
- $3$
- $2$
- $72$
- $6$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=- 2 x + y,\,v=4 x + y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=- 2 x + y$ into the equations of the first and second lines:

$$
\begin{aligned} & y=2 x & ⟹\, & - 2 x + y=0 & ⟹\, & u=0 \\  & y=2 x + 3 & ⟹\, & - 2 x + y=3 & ⟹\, & u=3\end{aligned}
$$

And we substitute $v=4 x + y$ into the equations of the third and fourth lines:

$$
\begin{aligned} & y=1 - 4 x & ⟹\, & 4 x + y=1 & ⟹\, & v=1 \\  & y=5 - 4 x & ⟹\, & 4 x + y=5 & ⟹\, & v=5\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v)\,:\,0\le u\le 3,\,1\le v\le 5\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/0155df6bcfae071544a23cc49f311fce777d4ef240a8fd9cd7de66dbdd737579.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-2 & 1 \\ 4 & 1\end{aligned}| \\  & =-6.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=- \frac{1}{6}=- \frac{1}{6}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|- \frac{1}{6}|\,\text{d}u\text{d}v \\  & =\frac{1}{6}{∬}_{Δ}\,\text{d}u\text{d}v \\  & =\frac{1}{6}\cdot \text{Area}(Δ) \\  & =\frac{1}{6}\cdot 3\cdot 4 \\  & =2\end{aligned}
$$

---

Using the change of variables

$$
u=- 2 x + y,\qquad v=3 x + y,
$$

calculate the area of the finite region $D$ bounded by the lines

$$
y=2 x - 4,\qquad y=2 x + 4,\qquad y=3 - 3 x,\qquad y=5 - 3 x.
$$

- $16$
- $80$
- $\frac{16}{5}$
- $8$
- $\frac{16}{3}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=- 2 x + y,\,v=3 x + y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=- 2 x + y$ into the equations of the first and second lines:

$$
\begin{aligned} & y=2 x - 4 & ⟹\, & - 2 x + y=-4 & ⟹\, & u=-4 \\  & y=2 x + 4 & ⟹\, & - 2 x + y=4 & ⟹\, & u=4\end{aligned}
$$

And we substitute $v=3 x + y$ into the equations of the third and fourth lines:

$$
\begin{aligned} & y=3 - 3 x & ⟹\, & 3 x + y=3 & ⟹\, & v=3 \\  & y=5 - 3 x & ⟹\, & 3 x + y=5 & ⟹\, & v=5\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v)\,:\,-4\le u\le 4,\,3\le v\le 5\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/6c6a6d1ba0e4b5374481cef4439e2947b1b6d40f3623540fcf3f591dd78c51c2.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}-2 & 1 \\ 3 & 1\end{aligned}| \\  & =-5.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=- \frac{1}{5}=- \frac{1}{5}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|- \frac{1}{5}|\,\text{d}u\text{d}v \\  & =\frac{1}{5}{∬}_{Δ}\,\text{d}u\text{d}v \\  & =\frac{1}{5}\cdot \text{Area}(Δ) \\  & =\frac{1}{5}\cdot 8\cdot 2 \\  & =\frac{16}{5}\end{aligned}
$$

---

Using the change of variables

$$
u=\frac{1}{x y},\qquad v=x^{2} y,
$$

calculate the area of the finite region $D$ in the first quadrant bounded by the curves

$$
y=\frac{1}{3 x},\qquad y=\frac{1}{8 x},\qquad y=\frac{1}{x^{2}},\qquad y=\frac{4}{x^{2}}.
$$

- $\frac{5}{8}$
- $2 \ln{\left(2 \right)}$
- $\frac{\ln{\left(2 \right)}}{4}$
- $\frac{5 \ln{\left(2 \right)}}{12}$
- $\frac{2 \ln{\left(2 \right)}}{3}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=\frac{1}{x y},\,v=x^{2} y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=\frac{1}{x y}$ into the equations of the first and second curves:

$$
\begin{aligned} & y=\frac{1}{3 x} & ⟹\, & \frac{1}{x y}=3 & ⟹\, & u=3 \\  & y=\frac{1}{8 x} & ⟹\, & \frac{1}{x y}=8 & ⟹\, & u=8\end{aligned}
$$

And we substitute $v=x^{2} y$ into the equations of the third and fourth curves:

$$
\begin{aligned} & y=\frac{1}{x^{2}} & ⟹\, & x^{2} y=1 & ⟹\, & v=1 \\  & y=\frac{4}{x^{2}} & ⟹\, & x^{2} y=4 & ⟹\, & v=4\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v)\,:\,3\le u\le 8,\,1\le v\le 4\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/ab4783536278e8306454b0e3d5ba51d783114021423869cd9a2adb109563598c.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}- \frac{1}{x^{2} y} & - \frac{1}{x y^{2}} \\ 2 x y & x^{2}\end{aligned}| \\  & =\frac{1}{y}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=y=\frac{x^{2} y^{2}}{x^{2} y}=\frac{1}{u^{2} v}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|\frac{1}{u^{2} v}|\,\text{d}u\text{d}v \\  & =\int_{3}^{8}\int_{1}^{4}\frac{1}{u^{2} v}\,\mathrm d v\,\mathrm d u \\  & =\int_{3}^{8}\frac{1}{u^{2}}\,\mathrm d u\int_{1}^{4}\frac{1}{v}\,\mathrm d v \\  & =(- \frac{1}{8}+\frac{1}{3})\cdot (\ln 4-\ln 1) \\  & =\frac{5 \ln{\left(2 \right)}}{12}.\end{aligned}
$$

---

Using the change of variables

$$
u=\frac{y}{x^{2}},\qquad v=x y,
$$

calculate the area of the finite region $D$ in the first quadrant bounded by the curves

$$
y=3 x^{2},\qquad y=7 x^{2},\qquad y=\frac{1}{x},\qquad y=\frac{8}{x}.
$$

- $\frac{7 \ln{\left(3 \right)}}{3}$
- $- 7 \ln{\left(3 \right)} + 7 \ln{\left(7 \right)}$
- $7 \ln{\left(7 \right)}$
- $- \frac{7 \ln{\left(3 \right)}}{3} + \frac{7 \ln{\left(7 \right)}}{3}$
- $- 4 \ln{\left(3 \right)} + \frac{\ln{\left(21 \right)}}{2} + 3 \ln{\left(7 \right)}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=\frac{y}{x^{2}},\,v=x y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=\frac{y}{x^{2}}$ into the equations of the first and second curves:

$$
\begin{aligned} & y=3 x^{2} & ⟹\, & \frac{y}{x^{2}}=3 & ⟹\, & u=3 \\  & y=7 x^{2} & ⟹\, & \frac{y}{x^{2}}=7 & ⟹\, & u=7\end{aligned}
$$

And we substitute $v=x y$ into the equations of the third and fourth curves:

$$
\begin{aligned} & y=\frac{1}{x} & ⟹\, & x y=1 & ⟹\, & v=1 \\  & y=\frac{8}{x} & ⟹\, & x y=8 & ⟹\, & v=8\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v)\,:\,3\le u\le 7,\,1\le v\le 8\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/9ca72d641428f1587ad142d7c7a771c63d278de4a48956723899c1f34bc79964.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}- \frac{2 y}{x^{3}} & \frac{1}{x^{2}} \\ y & x\end{aligned}| \\  & =- \frac{3 y}{x^{2}}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=- \frac{x^{2}}{3 y}=- \frac{1}{3 u}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|- \frac{1}{3 u}|\,\text{d}u\text{d}v \\  & =\int_{3}^{7}\int_{1}^{8}\frac{1}{3 u}\,\mathrm d v\,\mathrm d u \\  & =\frac{1}{3}\int_{3}^{7}\frac{1}{u}\,\mathrm d u\int_{1}^{8}1\,\mathrm d v \\  & =\frac{1}{3}\cdot (\ln 7-\ln 3)\cdot (8-1) \\  & =- \frac{7 \ln{\left(3 \right)}}{3} + \frac{7 \ln{\left(7 \right)}}{3}.\end{aligned}
$$

---

Using the change of variables

$$
u=\frac{2}{x y},\qquad v=4 x^{3} y,
$$

calculate the area of the finite region $D$ in the first quadrant bounded by the curves

$$
y=\frac{2}{3 x},\qquad y=\frac{1}{4 x},\qquad y=\frac{1}{4 x^{3}},\qquad y=\frac{1}{x^{3}}.
$$

- $\frac{5}{8}$
- $\frac{\ln{\left(2 \right)}}{4}$
- $2 \ln{\left(2 \right)}$
- $\frac{2 \ln{\left(2 \right)}}{3}$
- $\frac{5 \ln{\left(2 \right)}}{12}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=\frac{2}{x y},\,v=4 x^{3} y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=\frac{2}{x y}$ into the equations of the first and second curves:

$$
\begin{aligned} & y=\frac{2}{3 x} & ⟹\, & \frac{2}{x y}=3 & ⟹\, & u=3 \\  & y=\frac{1}{4 x} & ⟹\, & \frac{2}{x y}=8 & ⟹\, & u=8\end{aligned}
$$

And we substitute $v=4 x^{3} y$ into the equations of the third and fourth curves:

$$
\begin{aligned} & y=\frac{1}{4 x^{3}} & ⟹\, & 4 x^{3} y=1 & ⟹\, & v=1 \\  & y=\frac{1}{x^{3}} & ⟹\, & 4 x^{3} y=4 & ⟹\, & v=4\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v)\,:\,3\le u\le 8,\,1\le v\le 4\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/ab4783536278e8306454b0e3d5ba51d783114021423869cd9a2adb109563598c.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}- \frac{2}{x^{2} y} & - \frac{2}{x y^{2}} \\ 12 x^{2} y & 4 x^{3}\end{aligned}| \\  & =\frac{16 x}{y}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{y}{16 x}=\frac{x^{2} y^{2}}{16 x^{3} y}=\frac{1}{u^{2} v}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|\frac{1}{u^{2} v}|\,\text{d}u\text{d}v \\  & =\int_{3}^{8}\int_{1}^{4}\frac{1}{u^{2} v}\,\mathrm d v\,\mathrm d u \\  & =\int_{3}^{8}\frac{1}{u^{2}}\,\mathrm d u\int_{1}^{4}\frac{1}{v}\,\mathrm d v \\  & =(- \frac{1}{8}+\frac{1}{3})\cdot (\ln 4-\ln 1) \\  & =\frac{5 \ln{\left(2 \right)}}{12}.\end{aligned}
$$

---

Using the change of variables

$$
u=\frac{3}{x y},\qquad v=3 x^{3} y,
$$

calculate the area of the finite region $D$ in the first quadrant bounded by the curves

$$
y=\frac{3}{x},\qquad y=\frac{3}{8 x},\qquad y=\frac{1}{x^{3}},\qquad y=\frac{5}{3 x^{3}}.
$$

- $- 2 \ln{\left(3 \right)} + \frac{\ln{\left(15 \right)}}{2} + \ln{\left(5 \right)}$
- $\frac{21 \ln{\left(5 \right)}}{16}$
- $\frac{21 \ln{\left(3 \right)}}{16}$
- $- \frac{3 \ln{\left(3 \right)}}{16} + \frac{3 \ln{\left(5 \right)}}{16}$
- $- \frac{21 \ln{\left(3 \right)}}{16} + \frac{21 \ln{\left(5 \right)}}{16}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=\frac{3}{x y},\,v=3 x^{3} y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=\frac{3}{x y}$ into the equations of the first and second curves:

$$
\begin{aligned} & y=\frac{3}{x} & ⟹\, & \frac{3}{x y}=1 & ⟹\, & u=1 \\  & y=\frac{3}{8 x} & ⟹\, & \frac{3}{x y}=8 & ⟹\, & u=8\end{aligned}
$$

And we substitute $v=3 x^{3} y$ into the equations of the third and fourth curves:

$$
\begin{aligned} & y=\frac{1}{x^{3}} & ⟹\, & 3 x^{3} y=3 & ⟹\, & v=3 \\  & y=\frac{5}{3 x^{3}} & ⟹\, & 3 x^{3} y=5 & ⟹\, & v=5\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v)\,:\,1\le u\le 8,\,3\le v\le 5\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/a852b46e00457d3db106b3ceed05bb794a2758997731459915535253850e65b3.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}- \frac{3}{x^{2} y} & - \frac{3}{x y^{2}} \\ 9 x^{2} y & 3 x^{3}\end{aligned}| \\  & =\frac{18 x}{y}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{y}{18 x}=\frac{x^{2} y^{2}}{18 x^{3} y}=\frac{3}{2 u^{2} v}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|\frac{3}{2 u^{2} v}|\,\text{d}u\text{d}v \\  & =\int_{1}^{8}\int_{3}^{5}\frac{3}{2 u^{2} v}\,\mathrm d v\,\mathrm d u \\  & =\frac{3}{2}\int_{1}^{8}\frac{1}{u^{2}}\,\mathrm d u\int_{3}^{5}\frac{1}{v}\,\mathrm d v \\  & =\frac{3}{2}\cdot (- \frac{1}{8}+1)\cdot (\ln 5-\ln 3) \\  & =- \frac{21 \ln{\left(3 \right)}}{16} + \frac{21 \ln{\left(5 \right)}}{16}.\end{aligned}
$$

---

Using the change of variables

$$
u=\frac{3}{x y},\qquad v=2 x^{3} y,
$$

calculate the area of the finite region $D$ in the first quadrant bounded by the curves

$$
y=\frac{3}{4 x},\qquad y=\frac{1}{3 x},\qquad y=\frac{1}{x^{3}},\qquad y=\frac{7}{2 x^{3}}.
$$

- $- \frac{5 \ln{\left(2 \right)}}{24} + \frac{5 \ln{\left(7 \right)}}{24}$
- $\frac{5 \ln{\left(7 \right)}}{24}$
- $- \frac{\ln{\left(2 \right)}}{6} + \frac{\ln{\left(7 \right)}}{6}$
- $\frac{5 \ln{\left(2 \right)}}{24}$
- $- \frac{3 \ln{\left(2 \right)}}{8} + \frac{3 \ln{\left(7 \right)}}{8}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=\frac{3}{x y},\,v=2 x^{3} y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=\frac{3}{x y}$ into the equations of the first and second curves:

$$
\begin{aligned} & y=\frac{3}{4 x} & ⟹\, & \frac{3}{x y}=4 & ⟹\, & u=4 \\  & y=\frac{1}{3 x} & ⟹\, & \frac{3}{x y}=9 & ⟹\, & u=9\end{aligned}
$$

And we substitute $v=2 x^{3} y$ into the equations of the third and fourth curves:

$$
\begin{aligned} & y=\frac{1}{x^{3}} & ⟹\, & 2 x^{3} y=2 & ⟹\, & v=2 \\  & y=\frac{7}{2 x^{3}} & ⟹\, & 2 x^{3} y=7 & ⟹\, & v=7\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v)\,:\,4\le u\le 9,\,2\le v\le 7\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/c90ad4ffeb580c6e4aee8d920fba3f570145cc4dee3223159a24b26de75d758d.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}- \frac{3}{x^{2} y} & - \frac{3}{x y^{2}} \\ 6 x^{2} y & 2 x^{3}\end{aligned}| \\  & =\frac{12 x}{y}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{y}{12 x}=\frac{x^{2} y^{2}}{12 x^{3} y}=\frac{3}{2 u^{2} v}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|\frac{3}{2 u^{2} v}|\,\text{d}u\text{d}v \\  & =\int_{4}^{9}\int_{2}^{7}\frac{3}{2 u^{2} v}\,\mathrm d v\,\mathrm d u \\  & =\frac{3}{2}\int_{4}^{9}\frac{1}{u^{2}}\,\mathrm d u\int_{2}^{7}\frac{1}{v}\,\mathrm d v \\  & =\frac{3}{2}\cdot (- \frac{1}{9}+\frac{1}{4})\cdot (\ln 7-\ln 2) \\  & =- \frac{5 \ln{\left(2 \right)}}{24} + \frac{5 \ln{\left(7 \right)}}{24}.\end{aligned}
$$

---

Using the change of variables

$$
u=\frac{2}{x y},\qquad v=2 x^{3} y,
$$

calculate the area of the finite region $D$ in the first quadrant bounded by the curves

$$
y=\frac{2}{x},\qquad y=\frac{1}{3 x},\qquad y=\frac{1}{x^{3}},\qquad y=\frac{3}{x^{3}}.
$$

- $\frac{5 \ln{\left(3 \right)}}{6}$
- $\ln{\left(3 \right)}$
- $\frac{5 \ln{\left(6 \right)}}{6}$
- $\frac{\ln{\left(3 \right)}}{6}$
- $\frac{5 \ln{\left(2 \right)}}{6}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=\frac{2}{x y},\,v=2 x^{3} y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=\frac{2}{x y}$ into the equations of the first and second curves:

$$
\begin{aligned} & y=\frac{2}{x} & ⟹\, & \frac{2}{x y}=1 & ⟹\, & u=1 \\  & y=\frac{1}{3 x} & ⟹\, & \frac{2}{x y}=6 & ⟹\, & u=6\end{aligned}
$$

And we substitute $v=2 x^{3} y$ into the equations of the third and fourth curves:

$$
\begin{aligned} & y=\frac{1}{x^{3}} & ⟹\, & 2 x^{3} y=2 & ⟹\, & v=2 \\  & y=\frac{3}{x^{3}} & ⟹\, & 2 x^{3} y=6 & ⟹\, & v=6\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v)\,:\,1\le u\le 6,\,2\le v\le 6\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/5e874f3fe0111eedb94adee7933bb5a686343b8caec1c58ab8d70cb31c49483f.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}- \frac{2}{x^{2} y} & - \frac{2}{x y^{2}} \\ 6 x^{2} y & 2 x^{3}\end{aligned}| \\  & =\frac{8 x}{y}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{y}{8 x}=\frac{x^{2} y^{2}}{8 x^{3} y}=\frac{1}{u^{2} v}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|\frac{1}{u^{2} v}|\,\text{d}u\text{d}v \\  & =\int_{1}^{6}\int_{2}^{6}\frac{1}{u^{2} v}\,\mathrm d v\,\mathrm d u \\  & =\int_{1}^{6}\frac{1}{u^{2}}\,\mathrm d u\int_{2}^{6}\frac{1}{v}\,\mathrm d v \\  & =(- \frac{1}{6}+1)\cdot (\ln 6-\ln 2) \\  & =\frac{5 \ln{\left(3 \right)}}{6}.\end{aligned}
$$

---

Using the change of variables

$$
u=\frac{2}{x y},\qquad v=4 x^{3} y,
$$

calculate the area of the finite region $D$ in the first quadrant bounded by the curves

$$
y=\frac{1}{x},\qquad y=\frac{2}{5 x},\qquad y=\frac{1}{4 x^{3}},\qquad y=\frac{7}{4 x^{3}}.
$$

- $\frac{\ln{\left(7 \right)}}{2}$
- $\frac{9}{5}$
- $\frac{3 \ln{\left(7 \right)}}{10}$
- $\frac{\ln{\left(7 \right)}}{5}$
- $\ln{\left(7 \right)}$

The area of the required region is given by

$$
{∬}_{D}dxdy.
$$

Let's define a transformation $T$ as follows: 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}]
$$

This transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.

To compute the required area, we will use the change of variables formula

$$
{∬}_{D}dxdy={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\text{ }dudv
$$

where $\frac{∂(x,y)}{∂(u,v)}$ is the Jacobian determinant corresponding to $T.$  

Note that the changes of variables

$$
u=\frac{2}{x y},\,v=4 x^{3} y
$$

 

gives us the *inverse* function ${T}^{-1},$ that is

$$
{T}^{-1}:[\begin{aligned}x \\ y\end{aligned}]\to [\begin{aligned}u(x,y) \\ v(x,y)\end{aligned}].
$$

To compute the required area, we proceed in four steps:

**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$ 

We substitute $u=\frac{2}{x y}$ into the equations of the first and second curves:

$$
\begin{aligned} & y=\frac{1}{x} & ⟹\, & \frac{2}{x y}=2 & ⟹\, & u=2 \\  & y=\frac{2}{5 x} & ⟹\, & \frac{2}{x y}=5 & ⟹\, & u=5\end{aligned}
$$

And we substitute $v=4 x^{3} y$ into the equations of the third and fourth curves:

$$
\begin{aligned} & y=\frac{1}{4 x^{3}} & ⟹\, & 4 x^{3} y=1 & ⟹\, & v=1 \\  & y=\frac{7}{4 x^{3}} & ⟹\, & 4 x^{3} y=7 & ⟹\, & v=7\end{aligned}
$$

Therefore, our domain in the $uv$-plane is the following rectangle:

$$
\Delta=\{(u,v)\,:\,2\le u\le 5,\,1\le v\le 7\}
$$

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186129261/plots/d064d942fcb837b7292b0a8c68433bfb23f953ecfce66b319681da746dcd6b7e.png)

**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$

The Jacobian determinant corresponding to ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}- \frac{2}{x^{2} y} & - \frac{2}{x y^{2}} \\ 12 x^{2} y & 4 x^{3}\end{aligned}| \\  & =\frac{16 x}{y}.\end{aligned}
$$

**Step 3**: Compute the Jacobian determinant corresponding to $T:$

The Jacobian determinant corresponding to $T$ is

$$
\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{y}{16 x}=\frac{x^{2} y^{2}}{16 x^{3} y}=\frac{1}{u^{2} v}.
$$

Note that $\frac{∂(x,y)}{∂(u,v)}\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$

**Step 4**: Compute the required area.

We calculate the required area by performing the change of variables:

$$
\begin{aligned}{∬}_{D}\text{d}x\text{d}y & ={∬}_{Δ}|\frac{∂(x,y)}{∂(u,v)}|\,\text{d}u\text{d}v \\  & ={∬}_{Δ}|\frac{1}{u^{2} v}|\,\text{d}u\text{d}v \\  & =\int_{2}^{5}\int_{1}^{7}\frac{1}{u^{2} v}\,\mathrm d v\,\mathrm d u \\  & =\int_{2}^{5}\frac{1}{u^{2}}\,\mathrm d u\int_{1}^{7}\frac{1}{v}\,\mathrm d v \\  & =(- \frac{1}{5}+\frac{1}{2})\cdot (\ln 7-\ln 1) \\  & =\frac{3 \ln{\left(7 \right)}}{10}.\end{aligned}
$$
