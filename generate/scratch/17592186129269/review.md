# Inverse Jacobian review

Raw source profiles are evidence only. Coordinate-transport variants preserve every opaque historical option without asserting its original error intention. Normal method variants use actual derivative-row mistakes.

## Observed original q-39300

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}\frac{1}{x} \\ \sqrt{y}+z \\ {y}^{2}\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x\ne 0$ and $y>0.$*

- $\frac{{u}^{2}}{2\sqrt{w}}$
- $\frac{\sqrt{w}{u}^{2}}{2}$
- $-\frac{{u}^{2}}{2\sqrt{w}}$
- $-\frac{1}{2{u}^{2}\sqrt{w}}$
- $\frac{1}{2{u}^{2}\sqrt{w}}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=\frac{1}{x},\,y(x,y,z)=\sqrt{y}+z,\,z(x,y,z)={y}^{2}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =-\frac{1}{{x}^{2}} & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =\frac{1}{2\sqrt{y}} & \,\frac{∂v}{∂z} & =1 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =2y & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}-\frac{1}{{x}^{2}} & 0 & 0 \\ 0 & \frac{1}{2\sqrt{y}} & 1 \\ 0 & 2y & 0\end{aligned}| \\  & =-\frac{1}{{x}^{2}}|\begin{aligned}\frac{1}{2\sqrt{y}} & 1 \\ 2y & 0\end{aligned}| \\  & =\frac{2y}{{x}^{2}}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}\frac{2y}{{x}^{2}} & =(\frac{1}{x})^{2}\cdot 2\sqrt{{y}^{2}} \\  & ={u}^{2}\cdot 2\sqrt{w} \\  & =2{u}^{2}\sqrt{w}.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{2{u}^{2}\sqrt{w}}.\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-39300 1

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}2\left(\frac{1}{x}\right) \\ \sqrt{y}+z \\ {y}^{2}\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x\ne 0$ and $y>0.$*

- $\frac{1}{2}\left(\frac{{\left(\frac{u}{2}\right)}^{2}}{2\sqrt{w}}\right)$
- $\frac{1}{2}\left(\frac{\sqrt{w}{\left(\frac{u}{2}\right)}^{2}}{2}\right)$
- $\frac{1}{2}\left(-\frac{1}{2{\left(\frac{u}{2}\right)}^{2}\sqrt{w}}\right)$
- $\frac{1}{2}\left(\frac{1}{2{\left(\frac{u}{2}\right)}^{2}\sqrt{w}}\right)$
- $\frac{1}{2}\left(-\frac{{\left(\frac{u}{2}\right)}^{2}}{2\sqrt{w}}\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=2\left(\frac{1}{x}\right),\,y(x,y,z)=\sqrt{y}+z,\,z(x,y,z)={y}^{2}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =2\left(-\frac{1}{{x}^{2}}\right) & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =\frac{1}{2\sqrt{y}} & \,\frac{∂v}{∂z} & =1 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =2y & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2\left(-\frac{1}{{x}^{2}}\right) & 0 & 0 \\ 0 & \frac{1}{2\sqrt{y}} & 1 \\ 0 & 2y & 0\end{aligned}| \\  & =2\left(-\frac{1}{{x}^{2}}|\begin{aligned}\frac{1}{2\sqrt{y}} & 1 \\ 2y & 0\end{aligned}|\right)\\  & =\frac{4 y}{x^{2}}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}2\left(\frac{2y}{{x}^{2}}\right) & =2\left((\frac{1}{x})^{2}\cdot 2\sqrt{{y}^{2}}\right) \\  & =2\left({\left(\frac{u}{2}\right)}^{2}\cdot 2\sqrt{w}\right) \\  & =2\left(2{\left(\frac{u}{2}\right)}^{2}\sqrt{w}\right).\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{u^{2} \sqrt{w}}.\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-39300 2

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}4\left(\frac{1}{x}\right) \\ 4\left(\sqrt{y}+z\right) \\ 2\left({y}^{2}\right)\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x\ne 0$ and $y>0.$*

- $\frac{1}{32}\left(\frac{{\left(\frac{u}{4}\right)}^{2}}{2\sqrt{\left(\frac{w}{2}\right)}}\right)$
- $\frac{1}{32}\left(\frac{1}{2{\left(\frac{u}{4}\right)}^{2}\sqrt{\left(\frac{w}{2}\right)}}\right)$
- $\frac{1}{32}\left(-\frac{1}{2{\left(\frac{u}{4}\right)}^{2}\sqrt{\left(\frac{w}{2}\right)}}\right)$
- $\frac{1}{32}\left(\frac{\sqrt{\left(\frac{w}{2}\right)}{\left(\frac{u}{4}\right)}^{2}}{2}\right)$
- $\frac{1}{32}\left(-\frac{{\left(\frac{u}{4}\right)}^{2}}{2\sqrt{\left(\frac{w}{2}\right)}}\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=4\left(\frac{1}{x}\right),\,y(x,y,z)=4\left(\sqrt{y}+z\right),\,z(x,y,z)=2\left({y}^{2}\right).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =4\left(-\frac{1}{{x}^{2}}\right) & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =4\left(\frac{1}{2\sqrt{y}}\right) & \,\frac{∂v}{∂z} & =4\left(1\right) \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =2\left(2y\right) & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $4, 4, 2$ multiplies the determinant by $32$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}4\left(-\frac{1}{{x}^{2}}\right) & 0 & 0 \\ 0 & 4\left(\frac{1}{2\sqrt{y}}\right) & 4\left(1\right) \\ 0 & 2\left(2y\right) & 0\end{aligned}| \\  & =32\left(-\frac{1}{{x}^{2}}|\begin{aligned}\frac{1}{2\sqrt{y}} & 1 \\ 2y & 0\end{aligned}|\right)\\  & =\frac{64 y}{x^{2}}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}32\left(\frac{2y}{{x}^{2}}\right) & =32\left((\frac{1}{x})^{2}\cdot 2\sqrt{{y}^{2}}\right) \\  & =32\left({\left(\frac{u}{4}\right)}^{2}\cdot 2\sqrt{\left(\frac{w}{2}\right)}\right) \\  & =32\left(2{\left(\frac{u}{4}\right)}^{2}\sqrt{\left(\frac{w}{2}\right)}\right).\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{\sqrt{2}}{4 u^{2} \sqrt{w}}.\end{aligned}
$$

---

## Generated method coordinate-scale variant q-39300 1

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}2\left(\frac{1}{x}\right) \\ \sqrt{y}+z \\ {y}^{2}\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x\ne 0$ and $y>0.$*

- $- \frac{1}{u^{2} \sqrt{w}}$
- $u^{2} \sqrt{w}$
- $\frac{1}{2 u^{2} \sqrt{w}}$
- $\frac{2}{u^{2} \sqrt{w}}$
- $\frac{1}{u^{2} \sqrt{w}}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=2\left(\frac{1}{x}\right),\,v(x,y,z)=\sqrt{y}+z,\,w(x,y,z)={y}^{2}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =2\left(-\frac{1}{{x}^{2}}\right) & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =\frac{1}{2\sqrt{y}} & \,\frac{∂v}{∂z} & =1 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =2y & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2\left(-\frac{1}{{x}^{2}}\right) & 0 & 0 \\ 0 & \frac{1}{2\sqrt{y}} & 1 \\ 0 & 2y & 0\end{aligned}| \\  & =2\left(-\frac{1}{{x}^{2}}|\begin{aligned}\frac{1}{2\sqrt{y}} & 1 \\ 2y & 0\end{aligned}|\right)\\  & =\frac{4 y}{x^{2}}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}2\left(\frac{2y}{{x}^{2}}\right) & =2\left((\frac{1}{x})^{2}\cdot 2\sqrt{{y}^{2}}\right) \\  & =2\left({\left(\frac{u}{2}\right)}^{2}\cdot 2\sqrt{w}\right) \\  & =2\left(2{\left(\frac{u}{2}\right)}^{2}\sqrt{w}\right).\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{u^{2} \sqrt{w}}.\end{aligned}
$$

---

## Generated method coordinate-scale variant q-39300 2

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}4\left(\frac{1}{x}\right) \\ 4\left(\sqrt{y}+z\right) \\ 2\left({y}^{2}\right)\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x\ne 0$ and $y>0.$*

- $- \frac{\sqrt{2}}{4 u^{2} \sqrt{w}}$
- $\frac{\sqrt{2}}{u^{2} \sqrt{w}}$
- $\frac{\sqrt{2}}{16 u^{2} \sqrt{w}}$
- $2 \sqrt{2} u^{2} \sqrt{w}$
- $\frac{\sqrt{2}}{4 u^{2} \sqrt{w}}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=4\left(\frac{1}{x}\right),\,v(x,y,z)=4\left(\sqrt{y}+z\right),\,w(x,y,z)=2\left({y}^{2}\right).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =4\left(-\frac{1}{{x}^{2}}\right) & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =4\left(\frac{1}{2\sqrt{y}}\right) & \,\frac{∂v}{∂z} & =4\left(1\right) \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =2\left(2y\right) & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $4, 4, 2$ multiplies the determinant by $32$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}4\left(-\frac{1}{{x}^{2}}\right) & 0 & 0 \\ 0 & 4\left(\frac{1}{2\sqrt{y}}\right) & 4\left(1\right) \\ 0 & 2\left(2y\right) & 0\end{aligned}| \\  & =32\left(-\frac{1}{{x}^{2}}|\begin{aligned}\frac{1}{2\sqrt{y}} & 1 \\ 2y & 0\end{aligned}|\right)\\  & =\frac{64 y}{x^{2}}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}32\left(\frac{2y}{{x}^{2}}\right) & =32\left((\frac{1}{x})^{2}\cdot 2\sqrt{{y}^{2}}\right) \\  & =32\left({\left(\frac{u}{4}\right)}^{2}\cdot 2\sqrt{\left(\frac{w}{2}\right)}\right) \\  & =32\left(2{\left(\frac{u}{4}\right)}^{2}\sqrt{\left(\frac{w}{2}\right)}\right).\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{\sqrt{2}}{4 u^{2} \sqrt{w}}.\end{aligned}
$$

---

## Repaired evidence profile q-39300

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}\frac{1}{x} \\ \sqrt{y}+z \\ {y}^{2}\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x\ne 0$ and $y>0.$*

- $\frac{{u}^{2}}{2\sqrt{w}}$
- $\frac{\sqrt{w}{u}^{2}}{2}$
- $-\frac{{u}^{2}}{2\sqrt{w}}$
- $-\frac{1}{2{u}^{2}\sqrt{w}}$
- $\frac{1}{2{u}^{2}\sqrt{w}}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=\frac{1}{x},\,v(x,y,z)=\sqrt{y}+z,\,w(x,y,z)={y}^{2}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =-\frac{1}{{x}^{2}} & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =\frac{1}{2\sqrt{y}} & \,\frac{∂v}{∂z} & =1 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =2y & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}-\frac{1}{{x}^{2}} & 0 & 0 \\ 0 & \frac{1}{2\sqrt{y}} & 1 \\ 0 & 2y & 0\end{aligned}| \\  & =-\frac{1}{{x}^{2}}|\begin{aligned}\frac{1}{2\sqrt{y}} & 1 \\ 2y & 0\end{aligned}| \\  & =\frac{2y}{{x}^{2}}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}\frac{2y}{{x}^{2}} & =(\frac{1}{x})^{2}\cdot 2\sqrt{{y}^{2}} \\  & ={u}^{2}\cdot 2\sqrt{w} \\  & =2{u}^{2}\sqrt{w}.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{2{u}^{2}\sqrt{w}}.\end{aligned}
$$

---

## Observed original q-39669

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=2x+y,\,v=-x+3y-2z,\,w=3y+4z.
$$

- $\frac{1}{16}$
- $16$
- $8$
- $40$
- $\frac{1}{40}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =2 & \,\frac{∂u}{∂y} & =1 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =-1 & \,\frac{∂v}{∂y} & =3 & \,\frac{∂v}{∂z} & =-2 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =3 & \,\frac{∂w}{∂z} & =4\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2 & 1 & 0 \\ -1 & 3 & -2 \\ 0 & 3 & 4\end{aligned}| \\  & =2|\begin{aligned}3 & -2 \\ 3 & 4\end{aligned}|-1|\begin{aligned}-1 & -2 \\ 0 & 4\end{aligned}| \\  & =2(12+6)-1(-4-0) \\  & =40.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{40}.\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-39669 1

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=2\left(2x+y\right),\,v=-x+3y-2z,\,w=3y+4z.
$$

- $\frac{1}{2}\left(\frac{1}{16}\right)$
- $\frac{1}{2}\left(16\right)$
- $\frac{1}{2}\left(40\right)$
- $\frac{1}{2}\left(\frac{1}{40}\right)$
- $\frac{1}{2}\left(8\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =2\left(2\right) & \,\frac{∂u}{∂y} & =2\left(1\right) & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =-1 & \,\frac{∂v}{∂y} & =3 & \,\frac{∂v}{∂z} & =-2 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =3 & \,\frac{∂w}{∂z} & =4\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2\left(2\right) & 2\left(1\right) & 0 \\ -1 & 3 & -2 \\ 0 & 3 & 4\end{aligned}| \\  & =2\left(2|\begin{aligned}3 & -2 \\ 3 & 4\end{aligned}|-1|\begin{aligned}-1 & -2 \\ 0 & 4\end{aligned}|\right)\\  & =2\left(2(12+6)-1(-4-0)\right)\\  & =80.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{80}.\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-39669 2

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=3\left(2x+y\right),\,v=-x+3y-2z,\,w=3y+4z.
$$

- $\frac{1}{3}\left(\frac{1}{16}\right)$
- $\frac{1}{3}\left(\frac{1}{40}\right)$
- $\frac{1}{3}\left(40\right)$
- $\frac{1}{3}\left(16\right)$
- $\frac{1}{3}\left(8\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =3\left(2\right) & \,\frac{∂u}{∂y} & =3\left(1\right) & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =-1 & \,\frac{∂v}{∂y} & =3 & \,\frac{∂v}{∂z} & =-2 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =3 & \,\frac{∂w}{∂z} & =4\end{aligned}
$$

Scaling the three derivative rows by $3, 1, 1$ multiplies the determinant by $3$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}3\left(2\right) & 3\left(1\right) & 0 \\ -1 & 3 & -2 \\ 0 & 3 & 4\end{aligned}| \\  & =3\left(2|\begin{aligned}3 & -2 \\ 3 & 4\end{aligned}|-1|\begin{aligned}-1 & -2 \\ 0 & 4\end{aligned}|\right)\\  & =3\left(2(12+6)-1(-4-0)\right)\\  & =120.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{120}.\end{aligned}
$$

---

## Generated method coordinate-scale variant q-39669 1

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=2\left(2x+y\right),\,v=-x+3y-2z,\,w=3y+4z.
$$

- $- \frac{1}{80}$
- $80$
- $\frac{1}{160}$
- $\frac{1}{40}$
- $\frac{1}{80}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =2\left(2\right) & \,\frac{∂u}{∂y} & =2\left(1\right) & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =-1 & \,\frac{∂v}{∂y} & =3 & \,\frac{∂v}{∂z} & =-2 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =3 & \,\frac{∂w}{∂z} & =4\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2\left(2\right) & 2\left(1\right) & 0 \\ -1 & 3 & -2 \\ 0 & 3 & 4\end{aligned}| \\  & =2\left(2|\begin{aligned}3 & -2 \\ 3 & 4\end{aligned}|-1|\begin{aligned}-1 & -2 \\ 0 & 4\end{aligned}|\right)\\  & =2\left(2(12+6)-1(-4-0)\right)\\  & =80.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{80}.\end{aligned}
$$

---

## Generated method coordinate-scale variant q-39669 2

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=3\left(2x+y\right),\,v=-x+3y-2z,\,w=3y+4z.
$$

- $- \frac{1}{120}$
- $\frac{1}{40}$
- $\frac{1}{360}$
- $120$
- $\frac{1}{120}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =3\left(2\right) & \,\frac{∂u}{∂y} & =3\left(1\right) & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =-1 & \,\frac{∂v}{∂y} & =3 & \,\frac{∂v}{∂z} & =-2 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =3 & \,\frac{∂w}{∂z} & =4\end{aligned}
$$

Scaling the three derivative rows by $3, 1, 1$ multiplies the determinant by $3$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}3\left(2\right) & 3\left(1\right) & 0 \\ -1 & 3 & -2 \\ 0 & 3 & 4\end{aligned}| \\  & =3\left(2|\begin{aligned}3 & -2 \\ 3 & 4\end{aligned}|-1|\begin{aligned}-1 & -2 \\ 0 & 4\end{aligned}|\right)\\  & =3\left(2(12+6)-1(-4-0)\right)\\  & =120.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{120}.\end{aligned}
$$

---

## Repaired evidence profile q-39669

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=2x+y,\,v=-x+3y-2z,\,w=3y+4z.
$$

- $\frac{1}{16}$
- $16$
- $8$
- $40$
- $\frac{1}{40}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =2 & \,\frac{∂u}{∂y} & =1 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =-1 & \,\frac{∂v}{∂y} & =3 & \,\frac{∂v}{∂z} & =-2 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =3 & \,\frac{∂w}{∂z} & =4\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2 & 1 & 0 \\ -1 & 3 & -2 \\ 0 & 3 & 4\end{aligned}| \\  & =2|\begin{aligned}3 & -2 \\ 3 & 4\end{aligned}|-1|\begin{aligned}-1 & -2 \\ 0 & 4\end{aligned}| \\  & =2(12+6)-1(-4-0) \\  & =40.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{40}.\end{aligned}
$$

---

## Observed original q-161798

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=x+y,\,v=z,\,w=4y-2{z}^{2}.
$$

- $2$
- $-\frac{1}{4}$
- $-\frac{1}{2}$
- $-8$
- $\frac{1}{8}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =1 & \,\frac{∂u}{∂y} & =1 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =1 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =4 & \,\frac{∂w}{∂z} & =-4z\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & 1 & 0 \\ 0 & 0 & 1 \\ 0 & 4 & -4z\end{aligned}| \\  & =1|\begin{aligned}0 & 1 \\ 4 & -4z\end{aligned}| \\  & =1(0-4) \\  & =-4.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{(-4)} \\  & =-\frac{1}{4}\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-161798 1

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=2\left(x+y\right),\,v=z,\,w=4y-2{z}^{2}.
$$

- $\frac{1}{2}\left(2\right)$
- $\frac{1}{2}\left(-\frac{1}{4}\right)$
- $\frac{1}{2}\left(-8\right)$
- $\frac{1}{2}\left(\frac{1}{8}\right)$
- $\frac{1}{2}\left(-\frac{1}{2}\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =2\left(1\right) & \,\frac{∂u}{∂y} & =2\left(1\right) & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =1 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =4 & \,\frac{∂w}{∂z} & =-4z\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2\left(1\right) & 2\left(1\right) & 0 \\ 0 & 0 & 1 \\ 0 & 4 & -4z\end{aligned}| \\  & =2\left(1|\begin{aligned}0 & 1 \\ 4 & -4z\end{aligned}|\right)\\  & =2\left(1(0-4)\right)\\  & =-8.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{2}\left(\frac{1}{(-4)}\right) \\  & =- \frac{1}{8}\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-161798 2

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=4\left(x+y\right),\,v=4\left(z\right),\,w=4y-2{z}^{2}.
$$

- $\frac{1}{16}\left(2\right)$
- $\frac{1}{16}\left(\frac{1}{8}\right)$
- $\frac{1}{16}\left(-8\right)$
- $\frac{1}{16}\left(-\frac{1}{4}\right)$
- $\frac{1}{16}\left(-\frac{1}{2}\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =4\left(1\right) & \,\frac{∂u}{∂y} & =4\left(1\right) & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =4\left(1\right) \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =4 & \,\frac{∂w}{∂z} & =-4z\end{aligned}
$$

Scaling the three derivative rows by $4, 4, 1$ multiplies the determinant by $16$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}4\left(1\right) & 4\left(1\right) & 0 \\ 0 & 0 & 4\left(1\right) \\ 0 & 4 & -4z\end{aligned}| \\  & =16\left(1|\begin{aligned}0 & 1 \\ 4 & -4z\end{aligned}|\right)\\  & =16\left(1(0-4)\right)\\  & =-64.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{16}\left(\frac{1}{(-4)}\right) \\  & =- \frac{1}{64}\end{aligned}
$$

---

## Generated method coordinate-scale variant q-161798 1

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=2\left(x+y\right),\,v=z,\,w=4y-2{z}^{2}.
$$

- $\frac{1}{8}$
- $-8$
- $- \frac{1}{16}$
- $- \frac{1}{4}$
- $- \frac{1}{8}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =2\left(1\right) & \,\frac{∂u}{∂y} & =2\left(1\right) & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =1 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =4 & \,\frac{∂w}{∂z} & =-4z\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2\left(1\right) & 2\left(1\right) & 0 \\ 0 & 0 & 1 \\ 0 & 4 & -4z\end{aligned}| \\  & =2\left(1|\begin{aligned}0 & 1 \\ 4 & -4z\end{aligned}|\right)\\  & =2\left(1(0-4)\right)\\  & =-8.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{2}\left(\frac{1}{(-4)}\right) \\  & =- \frac{1}{8}\end{aligned}
$$

---

## Generated method coordinate-scale variant q-161798 2

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=4\left(x+y\right),\,v=4\left(z\right),\,w=4y-2{z}^{2}.
$$

- $\frac{1}{64}$
- $- \frac{1}{16}$
- $- \frac{1}{256}$
- $-64$
- $- \frac{1}{64}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =4\left(1\right) & \,\frac{∂u}{∂y} & =4\left(1\right) & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =4\left(1\right) \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =4 & \,\frac{∂w}{∂z} & =-4z\end{aligned}
$$

Scaling the three derivative rows by $4, 4, 1$ multiplies the determinant by $16$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}4\left(1\right) & 4\left(1\right) & 0 \\ 0 & 0 & 4\left(1\right) \\ 0 & 4 & -4z\end{aligned}| \\  & =16\left(1|\begin{aligned}0 & 1 \\ 4 & -4z\end{aligned}|\right)\\  & =16\left(1(0-4)\right)\\  & =-64.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{16}\left(\frac{1}{(-4)}\right) \\  & =- \frac{1}{64}\end{aligned}
$$

---

## Repaired evidence profile q-161798

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=x+y,\,v=z,\,w=4y-2{z}^{2}.
$$

- $2$
- $-\frac{1}{4}$
- $-\frac{1}{2}$
- $-8$
- $\frac{1}{8}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =1 & \,\frac{∂u}{∂y} & =1 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =1 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =4 & \,\frac{∂w}{∂z} & =-4z\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & 1 & 0 \\ 0 & 0 & 1 \\ 0 & 4 & -4z\end{aligned}| \\  & =1|\begin{aligned}0 & 1 \\ 4 & -4z\end{aligned}| \\  & =1(0-4) \\  & =-4.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{(-4)} \\  & =-\frac{1}{4}\end{aligned}
$$

---

## Observed original q-161800

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=z-y,\,v=x+z,\,w=-3x.
$$

- $1$
- $\frac{1}{3}$
- $-2$
- $6$
- $-\frac{1}{6}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =-1 & \,\frac{∂u}{∂z} & =1 \\ \frac{∂v}{∂x} & =1 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =1 \\ \frac{∂w}{∂x} & =-3 & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & -1 & 1 \\ 1 & 0 & 1 \\ -3 & 0 & 0\end{aligned}| \\  & =-(-1)|\begin{aligned}1 & 1 \\ -3 & 0\end{aligned}|+1|\begin{aligned}1 & 0 \\ -3 & 0\end{aligned}| \\  & =1(0+3)+1(0-0) \\  & =3\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{3}\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-161800 1

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=2\left(z-y\right),\,v=x+z,\,w=-3x.
$$

- $\frac{1}{2}\left(1\right)$
- $\frac{1}{2}\left(\frac{1}{3}\right)$
- $\frac{1}{2}\left(6\right)$
- $\frac{1}{2}\left(-\frac{1}{6}\right)$
- $\frac{1}{2}\left(-2\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =2\left(-1\right) & \,\frac{∂u}{∂z} & =2\left(1\right) \\ \frac{∂v}{∂x} & =1 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =1 \\ \frac{∂w}{∂x} & =-3 & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & 2\left(-1\right) & 2\left(1\right) \\ 1 & 0 & 1 \\ -3 & 0 & 0\end{aligned}| \\  & =2\left(-(-1)|\begin{aligned}1 & 1 \\ -3 & 0\end{aligned}|+1|\begin{aligned}1 & 0 \\ -3 & 0\end{aligned}|\right)\\  & =2\left(1(0+3)+1(0-0)\right)\\  & =6\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{6}\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-161800 2

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=4\left(z-y\right),\,v=4\left(x+z\right),\,w=2\left(-3x\right).
$$

- $\frac{1}{32}\left(1\right)$
- $\frac{1}{32}\left(-\frac{1}{6}\right)$
- $\frac{1}{32}\left(6\right)$
- $\frac{1}{32}\left(\frac{1}{3}\right)$
- $\frac{1}{32}\left(-2\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =4\left(-1\right) & \,\frac{∂u}{∂z} & =4\left(1\right) \\ \frac{∂v}{∂x} & =4\left(1\right) & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =4\left(1\right) \\ \frac{∂w}{∂x} & =2\left(-3\right) & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $4, 4, 2$ multiplies the determinant by $32$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & 4\left(-1\right) & 4\left(1\right) \\ 4\left(1\right) & 0 & 4\left(1\right) \\ 2\left(-3\right) & 0 & 0\end{aligned}| \\  & =32\left(-(-1)|\begin{aligned}1 & 1 \\ -3 & 0\end{aligned}|+1|\begin{aligned}1 & 0 \\ -3 & 0\end{aligned}|\right)\\  & =32\left(1(0+3)+1(0-0)\right)\\  & =96\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{96}\end{aligned}
$$

---

## Generated method coordinate-scale variant q-161800 1

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=2\left(z-y\right),\,v=x+z,\,w=-3x.
$$

- $- \frac{1}{6}$
- $6$
- $\frac{1}{12}$
- $\frac{1}{3}$
- $\frac{1}{6}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =2\left(-1\right) & \,\frac{∂u}{∂z} & =2\left(1\right) \\ \frac{∂v}{∂x} & =1 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =1 \\ \frac{∂w}{∂x} & =-3 & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & 2\left(-1\right) & 2\left(1\right) \\ 1 & 0 & 1 \\ -3 & 0 & 0\end{aligned}| \\  & =2\left(-(-1)|\begin{aligned}1 & 1 \\ -3 & 0\end{aligned}|+1|\begin{aligned}1 & 0 \\ -3 & 0\end{aligned}|\right)\\  & =2\left(1(0+3)+1(0-0)\right)\\  & =6\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{6}\end{aligned}
$$

---

## Generated method coordinate-scale variant q-161800 2

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=4\left(z-y\right),\,v=4\left(x+z\right),\,w=2\left(-3x\right).
$$

- $- \frac{1}{96}$
- $\frac{1}{24}$
- $\frac{1}{384}$
- $96$
- $\frac{1}{96}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =4\left(-1\right) & \,\frac{∂u}{∂z} & =4\left(1\right) \\ \frac{∂v}{∂x} & =4\left(1\right) & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =4\left(1\right) \\ \frac{∂w}{∂x} & =2\left(-3\right) & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $4, 4, 2$ multiplies the determinant by $32$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & 4\left(-1\right) & 4\left(1\right) \\ 4\left(1\right) & 0 & 4\left(1\right) \\ 2\left(-3\right) & 0 & 0\end{aligned}| \\  & =32\left(-(-1)|\begin{aligned}1 & 1 \\ -3 & 0\end{aligned}|+1|\begin{aligned}1 & 0 \\ -3 & 0\end{aligned}|\right)\\  & =32\left(1(0+3)+1(0-0)\right)\\  & =96\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{96}\end{aligned}
$$

---

## Repaired evidence profile q-161800

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=z-y,\,v=x+z,\,w=-3x.
$$

- $1$
- $\frac{1}{3}$
- $-2$
- $6$
- $-\frac{1}{6}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =-1 & \,\frac{∂u}{∂z} & =1 \\ \frac{∂v}{∂x} & =1 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =1 \\ \frac{∂w}{∂x} & =-3 & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & -1 & 1 \\ 1 & 0 & 1 \\ -3 & 0 & 0\end{aligned}| \\  & =-(-1)|\begin{aligned}1 & 1 \\ -3 & 0\end{aligned}|+1|\begin{aligned}1 & 0 \\ -3 & 0\end{aligned}| \\  & =1(0+3)+1(0-0) \\  & =3\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{3}\end{aligned}
$$

---

## Observed original q-161801

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=y-3z,\,v=x+2z,\,w=3x-y.
$$

- $1$
- $-\frac{1}{6}$
- $3$
- $\frac{1}{9}$
- $-2$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =1 & \,\frac{∂u}{∂z} & =-3 \\ \frac{∂v}{∂x} & =1 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =2 \\ \frac{∂w}{∂x} & =3 & \,\frac{∂w}{∂y} & =-1 & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & 1 & -3 \\ 1 & 0 & 2 \\ 3 & -1 & 0\end{aligned}| \\  & =-1|\begin{aligned}1 & 2 \\ 3 & 0\end{aligned}|-3|\begin{aligned}1 & 0 \\ 3 & -1\end{aligned}| \\  & =-1(0-6)-3(-1-0) \\  & =6+3 \\  & =9\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{9}\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-161801 1

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=2\left(y-3z\right),\,v=x+2z,\,w=3x-y.
$$

- $\frac{1}{2}\left(1\right)$
- $\frac{1}{2}\left(-\frac{1}{6}\right)$
- $\frac{1}{2}\left(\frac{1}{9}\right)$
- $\frac{1}{2}\left(-2\right)$
- $\frac{1}{2}\left(3\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =2\left(1\right) & \,\frac{∂u}{∂z} & =2\left(-3\right) \\ \frac{∂v}{∂x} & =1 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =2 \\ \frac{∂w}{∂x} & =3 & \,\frac{∂w}{∂y} & =-1 & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & 2\left(1\right) & 2\left(-3\right) \\ 1 & 0 & 2 \\ 3 & -1 & 0\end{aligned}| \\  & =2\left(-1|\begin{aligned}1 & 2 \\ 3 & 0\end{aligned}|-3|\begin{aligned}1 & 0 \\ 3 & -1\end{aligned}|\right)\\  & =2\left(-1(0-6)-3(-1-0)\right)\\  & =2\left(6+3\right)\\  & =18\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{18}\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-161801 2

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=4\left(y-3z\right),\,v=3\left(x+2z\right),\,w=3x-y.
$$

- $\frac{1}{12}\left(1\right)$
- $\frac{1}{12}\left(-2\right)$
- $\frac{1}{12}\left(\frac{1}{9}\right)$
- $\frac{1}{12}\left(-\frac{1}{6}\right)$
- $\frac{1}{12}\left(3\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =4\left(1\right) & \,\frac{∂u}{∂z} & =4\left(-3\right) \\ \frac{∂v}{∂x} & =3\left(1\right) & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =3\left(2\right) \\ \frac{∂w}{∂x} & =3 & \,\frac{∂w}{∂y} & =-1 & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $4, 3, 1$ multiplies the determinant by $12$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & 4\left(1\right) & 4\left(-3\right) \\ 3\left(1\right) & 0 & 3\left(2\right) \\ 3 & -1 & 0\end{aligned}| \\  & =12\left(-1|\begin{aligned}1 & 2 \\ 3 & 0\end{aligned}|-3|\begin{aligned}1 & 0 \\ 3 & -1\end{aligned}|\right)\\  & =12\left(-1(0-6)-3(-1-0)\right)\\  & =12\left(6+3\right)\\  & =108\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{108}\end{aligned}
$$

---

## Generated method coordinate-scale variant q-161801 1

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=2\left(y-3z\right),\,v=x+2z,\,w=3x-y.
$$

- $- \frac{1}{18}$
- $18$
- $\frac{1}{36}$
- $\frac{1}{9}$
- $\frac{1}{18}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =2\left(1\right) & \,\frac{∂u}{∂z} & =2\left(-3\right) \\ \frac{∂v}{∂x} & =1 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =2 \\ \frac{∂w}{∂x} & =3 & \,\frac{∂w}{∂y} & =-1 & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & 2\left(1\right) & 2\left(-3\right) \\ 1 & 0 & 2 \\ 3 & -1 & 0\end{aligned}| \\  & =2\left(-1|\begin{aligned}1 & 2 \\ 3 & 0\end{aligned}|-3|\begin{aligned}1 & 0 \\ 3 & -1\end{aligned}|\right)\\  & =2\left(-1(0-6)-3(-1-0)\right)\\  & =2\left(6+3\right)\\  & =18\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{18}\end{aligned}
$$

---

## Generated method coordinate-scale variant q-161801 2

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=4\left(y-3z\right),\,v=3\left(x+2z\right),\,w=3x-y.
$$

- $- \frac{1}{108}$
- $\frac{1}{27}$
- $\frac{1}{432}$
- $108$
- $\frac{1}{108}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =4\left(1\right) & \,\frac{∂u}{∂z} & =4\left(-3\right) \\ \frac{∂v}{∂x} & =3\left(1\right) & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =3\left(2\right) \\ \frac{∂w}{∂x} & =3 & \,\frac{∂w}{∂y} & =-1 & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $4, 3, 1$ multiplies the determinant by $12$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & 4\left(1\right) & 4\left(-3\right) \\ 3\left(1\right) & 0 & 3\left(2\right) \\ 3 & -1 & 0\end{aligned}| \\  & =12\left(-1|\begin{aligned}1 & 2 \\ 3 & 0\end{aligned}|-3|\begin{aligned}1 & 0 \\ 3 & -1\end{aligned}|\right)\\  & =12\left(-1(0-6)-3(-1-0)\right)\\  & =12\left(6+3\right)\\  & =108\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{108}\end{aligned}
$$

---

## Repaired evidence profile q-161801

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=y-3z,\,v=x+2z,\,w=3x-y.
$$

- $1$
- $-\frac{1}{6}$
- $3$
- $\frac{1}{9}$
- $-2$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =1 & \,\frac{∂u}{∂z} & =-3 \\ \frac{∂v}{∂x} & =1 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =2 \\ \frac{∂w}{∂x} & =3 & \,\frac{∂w}{∂y} & =-1 & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & 1 & -3 \\ 1 & 0 & 2 \\ 3 & -1 & 0\end{aligned}| \\  & =-1|\begin{aligned}1 & 2 \\ 3 & 0\end{aligned}|-3|\begin{aligned}1 & 0 \\ 3 & -1\end{aligned}| \\  & =-1(0-6)-3(-1-0) \\  & =6+3 \\  & =9\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{9}\end{aligned}
$$

---

## Observed original q-161802

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=3x+yz,\,v=z,\,w=-y.
$$

- $-\frac{1}{3}$
- $3$
- $-3$
- $\frac{1}{3}$
- $-1$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =3 & \,\frac{∂u}{∂y} & =z & \,\frac{∂u}{∂z} & =y \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =1 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =-1 & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}3 & z & y \\ 0 & 0 & 1 \\ 0 & -1 & 0\end{aligned}| \\  & =3|\begin{aligned}0 & 1 \\ -1 & 0\end{aligned}| \\  & =3(0+1) \\  & =3\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{3}\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-161802 1

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=2\left(3x+yz\right),\,v=z,\,w=-y.
$$

- $\frac{1}{2}\left(-\frac{1}{3}\right)$
- $\frac{1}{2}\left(3\right)$
- $\frac{1}{2}\left(\frac{1}{3}\right)$
- $\frac{1}{2}\left(-1\right)$
- $\frac{1}{2}\left(-3\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =2\left(3\right) & \,\frac{∂u}{∂y} & =2\left(z\right) & \,\frac{∂u}{∂z} & =2\left(y\right) \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =1 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =-1 & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2\left(3\right) & 2\left(z\right) & 2\left(y\right) \\ 0 & 0 & 1 \\ 0 & -1 & 0\end{aligned}| \\  & =2\left(3|\begin{aligned}0 & 1 \\ -1 & 0\end{aligned}|\right)\\  & =2\left(3(0+1)\right)\\  & =6\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{6}\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-161802 2

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=4\left(3x+yz\right),\,v=4\left(z\right),\,w=2\left(-y\right).
$$

- $\frac{1}{32}\left(-\frac{1}{3}\right)$
- $\frac{1}{32}\left(-1\right)$
- $\frac{1}{32}\left(\frac{1}{3}\right)$
- $\frac{1}{32}\left(3\right)$
- $\frac{1}{32}\left(-3\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =4\left(3\right) & \,\frac{∂u}{∂y} & =4\left(z\right) & \,\frac{∂u}{∂z} & =4\left(y\right) \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =4\left(1\right) \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =2\left(-1\right) & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $4, 4, 2$ multiplies the determinant by $32$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}4\left(3\right) & 4\left(z\right) & 4\left(y\right) \\ 0 & 0 & 4\left(1\right) \\ 0 & 2\left(-1\right) & 0\end{aligned}| \\  & =32\left(3|\begin{aligned}0 & 1 \\ -1 & 0\end{aligned}|\right)\\  & =32\left(3(0+1)\right)\\  & =96\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{96}\end{aligned}
$$

---

## Generated method coordinate-scale variant q-161802 1

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=2\left(3x+yz\right),\,v=z,\,w=-y.
$$

- $- \frac{1}{6}$
- $6$
- $\frac{1}{12}$
- $\frac{1}{3}$
- $\frac{1}{6}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =2\left(3\right) & \,\frac{∂u}{∂y} & =2\left(z\right) & \,\frac{∂u}{∂z} & =2\left(y\right) \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =1 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =-1 & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2\left(3\right) & 2\left(z\right) & 2\left(y\right) \\ 0 & 0 & 1 \\ 0 & -1 & 0\end{aligned}| \\  & =2\left(3|\begin{aligned}0 & 1 \\ -1 & 0\end{aligned}|\right)\\  & =2\left(3(0+1)\right)\\  & =6\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{6}\end{aligned}
$$

---

## Generated method coordinate-scale variant q-161802 2

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=4\left(3x+yz\right),\,v=4\left(z\right),\,w=2\left(-y\right).
$$

- $- \frac{1}{96}$
- $\frac{1}{24}$
- $\frac{1}{384}$
- $96$
- $\frac{1}{96}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =4\left(3\right) & \,\frac{∂u}{∂y} & =4\left(z\right) & \,\frac{∂u}{∂z} & =4\left(y\right) \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =4\left(1\right) \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =2\left(-1\right) & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $4, 4, 2$ multiplies the determinant by $32$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}4\left(3\right) & 4\left(z\right) & 4\left(y\right) \\ 0 & 0 & 4\left(1\right) \\ 0 & 2\left(-1\right) & 0\end{aligned}| \\  & =32\left(3|\begin{aligned}0 & 1 \\ -1 & 0\end{aligned}|\right)\\  & =32\left(3(0+1)\right)\\  & =96\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{96}\end{aligned}
$$

---

## Repaired evidence profile q-161802

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=3x+yz,\,v=z,\,w=-y.
$$

- $-\frac{1}{3}$
- $3$
- $-3$
- $\frac{1}{3}$
- $-1$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =3 & \,\frac{∂u}{∂y} & =z & \,\frac{∂u}{∂z} & =y \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =1 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =-1 & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}3 & z & y \\ 0 & 0 & 1 \\ 0 & -1 & 0\end{aligned}| \\  & =3|\begin{aligned}0 & 1 \\ -1 & 0\end{aligned}| \\  & =3(0+1) \\  & =3\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{3}\end{aligned}
$$

---

## Observed original q-161804

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}{e}^{x} \\ {e}^{x+y} \\ {e}^{x+y+z}\end{aligned}].
$$

Find the Jacobian determinant of $T.$

- ${e}^{uvw}$
- ${e}^{u+v+w}$
- $\frac{1}{u+v+w}$
- $\frac{1}{uvw}$
- $u+v+w$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)={e}^{x},\,v(x,y,z)={e}^{x+y},\,w(x,y,z)={e}^{x+y+z}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & ={e}^{x} & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & ={e}^{x+y} & \,\frac{∂v}{∂y} & ={e}^{x+y} & \,\frac{∂v}{∂z} & =0 \\ \frac{∂w}{∂x} & ={e}^{x+y+z} & \,\frac{∂w}{∂y} & ={e}^{x+y+z} & \,\frac{∂w}{∂z} & ={e}^{x+y+z}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}{e}^{x} & 0 & 0 \\ {e}^{x+y} & {e}^{x+y} & 0 \\ {e}^{x+y+z} & {e}^{x+y+z} & {e}^{x+y+z}\end{aligned}| \\  & ={e}^{x}|\begin{aligned}{e}^{x+y} & 0 \\ {e}^{x+y+z} & {e}^{x+y+z}\end{aligned}| \\  & ={e}^{x}({e}^{2x+2y+z}-0) \\  & ={e}^{3x+2y+z}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}{e}^{3x+2y+z} & ={e}^{x+(x+y)+(x+y+z)} \\  & ={e}^{x}\cdot {e}^{x+y}\cdot {e}^{x+y+z} \\  & =uvw\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{uvw}\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-161804 1

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}2\left({e}^{x}\right) \\ {e}^{x+y} \\ {e}^{x+y+z}\end{aligned}].
$$

Find the Jacobian determinant of $T.$

- $\frac{1}{2}\left({e}^{\left(\frac{u}{2}\right)vw}\right)$
- $\frac{1}{2}\left({e}^{\left(\frac{u}{2}\right)+v+w}\right)$
- $\frac{1}{2}\left(\frac{1}{\left(\frac{u}{2}\right)vw}\right)$
- $\frac{1}{2}\left(\left(\frac{u}{2}\right)+v+w\right)$
- $\frac{1}{2}\left(\frac{1}{\left(\frac{u}{2}\right)+v+w}\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=2\left({e}^{x}\right),\,v(x,y,z)={e}^{x+y},\,w(x,y,z)={e}^{x+y+z}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =2\left({e}^{x}\right) & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & ={e}^{x+y} & \,\frac{∂v}{∂y} & ={e}^{x+y} & \,\frac{∂v}{∂z} & =0 \\ \frac{∂w}{∂x} & ={e}^{x+y+z} & \,\frac{∂w}{∂y} & ={e}^{x+y+z} & \,\frac{∂w}{∂z} & ={e}^{x+y+z}\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2\left({e}^{x}\right) & 0 & 0 \\ {e}^{x+y} & {e}^{x+y} & 0 \\ {e}^{x+y+z} & {e}^{x+y+z} & {e}^{x+y+z}\end{aligned}| \\  & =2\left({e}^{x}|\begin{aligned}{e}^{x+y} & 0 \\ {e}^{x+y+z} & {e}^{x+y+z}\end{aligned}|\right)\\  & =2\left({e}^{x}({e}^{2x+2y+z}-0)\right)\\  & =2 e^{x} e^{x + y} e^{x + y + z}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}2\left({e}^{3x+2y+z}\right) & =2\left({e}^{x+(x+y)+(x+y+z)}\right) \\  & =2\left({e}^{x}\cdot {e}^{x+y}\cdot {e}^{x+y+z}\right) \\  & =2\left(\left(\frac{u}{2}\right)vw\right)\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{u v w}\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-161804 2

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}4\left({e}^{x}\right) \\ 4\left({e}^{x+y}\right) \\ 2\left({e}^{x+y+z}\right)\end{aligned}].
$$

Find the Jacobian determinant of $T.$

- $\frac{1}{32}\left({e}^{\left(\frac{u}{4}\right)\left(\frac{v}{4}\right)\left(\frac{w}{2}\right)}\right)$
- $\frac{1}{32}\left(\left(\frac{u}{4}\right)+\left(\frac{v}{4}\right)+\left(\frac{w}{2}\right)\right)$
- $\frac{1}{32}\left(\frac{1}{\left(\frac{u}{4}\right)\left(\frac{v}{4}\right)\left(\frac{w}{2}\right)}\right)$
- $\frac{1}{32}\left({e}^{\left(\frac{u}{4}\right)+\left(\frac{v}{4}\right)+\left(\frac{w}{2}\right)}\right)$
- $\frac{1}{32}\left(\frac{1}{\left(\frac{u}{4}\right)+\left(\frac{v}{4}\right)+\left(\frac{w}{2}\right)}\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=4\left({e}^{x}\right),\,v(x,y,z)=4\left({e}^{x+y}\right),\,w(x,y,z)=2\left({e}^{x+y+z}\right).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =4\left({e}^{x}\right) & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =4\left({e}^{x+y}\right) & \,\frac{∂v}{∂y} & =4\left({e}^{x+y}\right) & \,\frac{∂v}{∂z} & =0 \\ \frac{∂w}{∂x} & =2\left({e}^{x+y+z}\right) & \,\frac{∂w}{∂y} & =2\left({e}^{x+y+z}\right) & \,\frac{∂w}{∂z} & =2\left({e}^{x+y+z}\right)\end{aligned}
$$

Scaling the three derivative rows by $4, 4, 2$ multiplies the determinant by $32$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}4\left({e}^{x}\right) & 0 & 0 \\ 4\left({e}^{x+y}\right) & 4\left({e}^{x+y}\right) & 0 \\ 2\left({e}^{x+y+z}\right) & 2\left({e}^{x+y+z}\right) & 2\left({e}^{x+y+z}\right)\end{aligned}| \\  & =32\left({e}^{x}|\begin{aligned}{e}^{x+y} & 0 \\ {e}^{x+y+z} & {e}^{x+y+z}\end{aligned}|\right)\\  & =32\left({e}^{x}({e}^{2x+2y+z}-0)\right)\\  & =32 e^{x} e^{x + y} e^{x + y + z}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}32\left({e}^{3x+2y+z}\right) & =32\left({e}^{x+(x+y)+(x+y+z)}\right) \\  & =32\left({e}^{x}\cdot {e}^{x+y}\cdot {e}^{x+y+z}\right) \\  & =32\left(\left(\frac{u}{4}\right)\left(\frac{v}{4}\right)\left(\frac{w}{2}\right)\right)\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{u v w}\end{aligned}
$$

---

## Generated method coordinate-scale variant q-161804 1

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}2\left({e}^{x}\right) \\ {e}^{x+y} \\ {e}^{x+y+z}\end{aligned}].
$$

Find the Jacobian determinant of $T.$

- $- \frac{1}{u v w}$
- $u v w$
- $\frac{1}{2 u v w}$
- $\frac{2}{u v w}$
- $\frac{1}{u v w}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=2\left({e}^{x}\right),\,v(x,y,z)={e}^{x+y},\,w(x,y,z)={e}^{x+y+z}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =2\left({e}^{x}\right) & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & ={e}^{x+y} & \,\frac{∂v}{∂y} & ={e}^{x+y} & \,\frac{∂v}{∂z} & =0 \\ \frac{∂w}{∂x} & ={e}^{x+y+z} & \,\frac{∂w}{∂y} & ={e}^{x+y+z} & \,\frac{∂w}{∂z} & ={e}^{x+y+z}\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2\left({e}^{x}\right) & 0 & 0 \\ {e}^{x+y} & {e}^{x+y} & 0 \\ {e}^{x+y+z} & {e}^{x+y+z} & {e}^{x+y+z}\end{aligned}| \\  & =2\left({e}^{x}|\begin{aligned}{e}^{x+y} & 0 \\ {e}^{x+y+z} & {e}^{x+y+z}\end{aligned}|\right)\\  & =2\left({e}^{x}({e}^{2x+2y+z}-0)\right)\\  & =2 e^{x} e^{x + y} e^{x + y + z}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}2\left({e}^{3x+2y+z}\right) & =2\left({e}^{x+(x+y)+(x+y+z)}\right) \\  & =2\left({e}^{x}\cdot {e}^{x+y}\cdot {e}^{x+y+z}\right) \\  & =2\left(\left(\frac{u}{2}\right)vw\right)\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{u v w}\end{aligned}
$$

---

## Generated method coordinate-scale variant q-161804 2

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}4\left({e}^{x}\right) \\ 4\left({e}^{x+y}\right) \\ 2\left({e}^{x+y+z}\right)\end{aligned}].
$$

Find the Jacobian determinant of $T.$

- $- \frac{1}{u v w}$
- $\frac{4}{u v w}$
- $\frac{1}{4 u v w}$
- $u v w$
- $\frac{1}{u v w}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=4\left({e}^{x}\right),\,v(x,y,z)=4\left({e}^{x+y}\right),\,w(x,y,z)=2\left({e}^{x+y+z}\right).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =4\left({e}^{x}\right) & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =4\left({e}^{x+y}\right) & \,\frac{∂v}{∂y} & =4\left({e}^{x+y}\right) & \,\frac{∂v}{∂z} & =0 \\ \frac{∂w}{∂x} & =2\left({e}^{x+y+z}\right) & \,\frac{∂w}{∂y} & =2\left({e}^{x+y+z}\right) & \,\frac{∂w}{∂z} & =2\left({e}^{x+y+z}\right)\end{aligned}
$$

Scaling the three derivative rows by $4, 4, 2$ multiplies the determinant by $32$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}4\left({e}^{x}\right) & 0 & 0 \\ 4\left({e}^{x+y}\right) & 4\left({e}^{x+y}\right) & 0 \\ 2\left({e}^{x+y+z}\right) & 2\left({e}^{x+y+z}\right) & 2\left({e}^{x+y+z}\right)\end{aligned}| \\  & =32\left({e}^{x}|\begin{aligned}{e}^{x+y} & 0 \\ {e}^{x+y+z} & {e}^{x+y+z}\end{aligned}|\right)\\  & =32\left({e}^{x}({e}^{2x+2y+z}-0)\right)\\  & =32 e^{x} e^{x + y} e^{x + y + z}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}32\left({e}^{3x+2y+z}\right) & =32\left({e}^{x+(x+y)+(x+y+z)}\right) \\  & =32\left({e}^{x}\cdot {e}^{x+y}\cdot {e}^{x+y+z}\right) \\  & =32\left(\left(\frac{u}{4}\right)\left(\frac{v}{4}\right)\left(\frac{w}{2}\right)\right)\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{u v w}\end{aligned}
$$

---

## Repaired evidence profile q-161804

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}{e}^{x} \\ {e}^{x+y} \\ {e}^{x+y+z}\end{aligned}].
$$

Find the Jacobian determinant of $T.$

- ${e}^{uvw}$
- ${e}^{u+v+w}$
- $\frac{1}{u+v+w}$
- $\frac{1}{uvw}$
- $u+v+w$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)={e}^{x},\,v(x,y,z)={e}^{x+y},\,w(x,y,z)={e}^{x+y+z}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & ={e}^{x} & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & ={e}^{x+y} & \,\frac{∂v}{∂y} & ={e}^{x+y} & \,\frac{∂v}{∂z} & =0 \\ \frac{∂w}{∂x} & ={e}^{x+y+z} & \,\frac{∂w}{∂y} & ={e}^{x+y+z} & \,\frac{∂w}{∂z} & ={e}^{x+y+z}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}{e}^{x} & 0 & 0 \\ {e}^{x+y} & {e}^{x+y} & 0 \\ {e}^{x+y+z} & {e}^{x+y+z} & {e}^{x+y+z}\end{aligned}| \\  & ={e}^{x}|\begin{aligned}{e}^{x+y} & 0 \\ {e}^{x+y+z} & {e}^{x+y+z}\end{aligned}| \\  & ={e}^{x}({e}^{2x+2y+z}-0) \\  & ={e}^{3x+2y+z}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}{e}^{3x+2y+z} & ={e}^{x+(x+y)+(x+y+z)} \\  & ={e}^{x}\cdot {e}^{x+y}\cdot {e}^{x+y+z} \\  & =uvw\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{uvw}\end{aligned}
$$

---

## Observed original q-161805

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}x \\ z-y \\ xy\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x\ne 0.$*

- $u(w-v)$
- $-\frac{v+w}{u}$
- $-\frac{1}{u}$
- $\frac{1}{{u}^{2}}$
- $uv$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=x,\,v(x,y,z)=z-y,\,w(x,y,z)=xy.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =1 & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =-1 & \,\frac{∂v}{∂z} & =1 \\ \frac{∂w}{∂x} & =y & \,\frac{∂w}{∂y} & =x & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & 0 & 0 \\ 0 & -1 & 1 \\ y & x & 0\end{aligned}| \\  & =1|\begin{aligned}-1 & 1 \\ x & 0\end{aligned}| \\  & =1(0-x) \\  & =-x.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}-x & =-u\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{(-u)} \\  & =-\frac{1}{u}\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-161805 1

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}2\left(x\right) \\ z-y \\ xy\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x\ne 0.$*

- $\frac{1}{2}\left(\left(\frac{u}{2}\right)(w-v)\right)$
- $\frac{1}{2}\left(-\frac{v+w}{\left(\frac{u}{2}\right)}\right)$
- $\frac{1}{2}\left(\frac{1}{{\left(\frac{u}{2}\right)}^{2}}\right)$
- $\frac{1}{2}\left(\left(\frac{u}{2}\right)v\right)$
- $\frac{1}{2}\left(-\frac{1}{\left(\frac{u}{2}\right)}\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=2\left(x\right),\,v(x,y,z)=z-y,\,w(x,y,z)=xy.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =2\left(1\right) & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =-1 & \,\frac{∂v}{∂z} & =1 \\ \frac{∂w}{∂x} & =y & \,\frac{∂w}{∂y} & =x & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2\left(1\right) & 0 & 0 \\ 0 & -1 & 1 \\ y & x & 0\end{aligned}| \\  & =2\left(1|\begin{aligned}-1 & 1 \\ x & 0\end{aligned}|\right)\\  & =2\left(1(0-x)\right)\\  & =- 2 x.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}2\left(-x\right) & =2\left(-\left(\frac{u}{2}\right)\right)\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{2}\left(\frac{1}{(-\left(\frac{u}{2}\right))}\right) \\  & =- \frac{1}{u}\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-161805 2

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}4\left(x\right) \\ 4\left(z-y\right) \\ 2\left(xy\right)\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x\ne 0.$*

- $\frac{1}{32}\left(\left(\frac{u}{4}\right)(\left(\frac{w}{2}\right)-\left(\frac{v}{4}\right))\right)$
- $\frac{1}{32}\left(\left(\frac{u}{4}\right)\left(\frac{v}{4}\right)\right)$
- $\frac{1}{32}\left(\frac{1}{{\left(\frac{u}{4}\right)}^{2}}\right)$
- $\frac{1}{32}\left(-\frac{\left(\frac{v}{4}\right)+\left(\frac{w}{2}\right)}{\left(\frac{u}{4}\right)}\right)$
- $\frac{1}{32}\left(-\frac{1}{\left(\frac{u}{4}\right)}\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=4\left(x\right),\,v(x,y,z)=4\left(z-y\right),\,w(x,y,z)=2\left(xy\right).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =4\left(1\right) & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =4\left(-1\right) & \,\frac{∂v}{∂z} & =4\left(1\right) \\ \frac{∂w}{∂x} & =2\left(y\right) & \,\frac{∂w}{∂y} & =2\left(x\right) & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $4, 4, 2$ multiplies the determinant by $32$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}4\left(1\right) & 0 & 0 \\ 0 & 4\left(-1\right) & 4\left(1\right) \\ 2\left(y\right) & 2\left(x\right) & 0\end{aligned}| \\  & =32\left(1|\begin{aligned}-1 & 1 \\ x & 0\end{aligned}|\right)\\  & =32\left(1(0-x)\right)\\  & =- 32 x.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}32\left(-x\right) & =32\left(-\left(\frac{u}{4}\right)\right)\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{32}\left(\frac{1}{(-\left(\frac{u}{4}\right))}\right) \\  & =- \frac{1}{8 u}\end{aligned}
$$

---

## Generated method coordinate-scale variant q-161805 1

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}2\left(x\right) \\ z-y \\ xy\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x\ne 0.$*

- $\frac{1}{u}$
- $- u$
- $- \frac{1}{2 u}$
- $- \frac{2}{u}$
- $- \frac{1}{u}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=2\left(x\right),\,v(x,y,z)=z-y,\,w(x,y,z)=xy.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =2\left(1\right) & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =-1 & \,\frac{∂v}{∂z} & =1 \\ \frac{∂w}{∂x} & =y & \,\frac{∂w}{∂y} & =x & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2\left(1\right) & 0 & 0 \\ 0 & -1 & 1 \\ y & x & 0\end{aligned}| \\  & =2\left(1|\begin{aligned}-1 & 1 \\ x & 0\end{aligned}|\right)\\  & =2\left(1(0-x)\right)\\  & =- 2 x.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}2\left(-x\right) & =2\left(-\left(\frac{u}{2}\right)\right)\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{2}\left(\frac{1}{(-\left(\frac{u}{2}\right))}\right) \\  & =- \frac{1}{u}\end{aligned}
$$

---

## Generated method coordinate-scale variant q-161805 2

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}4\left(x\right) \\ 4\left(z-y\right) \\ 2\left(xy\right)\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x\ne 0.$*

- $\frac{1}{8 u}$
- $- \frac{1}{2 u}$
- $- \frac{1}{32 u}$
- $- 8 u$
- $- \frac{1}{8 u}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=4\left(x\right),\,v(x,y,z)=4\left(z-y\right),\,w(x,y,z)=2\left(xy\right).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =4\left(1\right) & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =4\left(-1\right) & \,\frac{∂v}{∂z} & =4\left(1\right) \\ \frac{∂w}{∂x} & =2\left(y\right) & \,\frac{∂w}{∂y} & =2\left(x\right) & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $4, 4, 2$ multiplies the determinant by $32$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}4\left(1\right) & 0 & 0 \\ 0 & 4\left(-1\right) & 4\left(1\right) \\ 2\left(y\right) & 2\left(x\right) & 0\end{aligned}| \\  & =32\left(1|\begin{aligned}-1 & 1 \\ x & 0\end{aligned}|\right)\\  & =32\left(1(0-x)\right)\\  & =- 32 x.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}32\left(-x\right) & =32\left(-\left(\frac{u}{4}\right)\right)\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{32}\left(\frac{1}{(-\left(\frac{u}{4}\right))}\right) \\  & =- \frac{1}{8 u}\end{aligned}
$$

---

## Repaired evidence profile q-161805

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}x \\ z-y \\ xy\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x\ne 0.$*

- $u(w-v)$
- $-\frac{v+w}{u}$
- $-\frac{1}{u}$
- $\frac{1}{{u}^{2}}$
- $uv$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=x,\,v(x,y,z)=z-y,\,w(x,y,z)=xy.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =1 & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =-1 & \,\frac{∂v}{∂z} & =1 \\ \frac{∂w}{∂x} & =y & \,\frac{∂w}{∂y} & =x & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & 0 & 0 \\ 0 & -1 & 1 \\ y & x & 0\end{aligned}| \\  & =1|\begin{aligned}-1 & 1 \\ x & 0\end{aligned}| \\  & =1(0-x) \\  & =-x.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}-x & =-u\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{(-u)} \\  & =-\frac{1}{u}\end{aligned}
$$

---

## Observed original q-161806

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}xy \\ yz \\ xz\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x,y,z>0.$*

- $\sqrt{uvw}$
- $\frac{1}{2\sqrt{uvw}}$
- $\frac{2}{\sqrt{uvw}}$
- $\frac{1}{uvw}$
- $4uvw$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=xy,\,v(x,y,z)=yz,\,w(x,y,z)=xz.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =y & \,\frac{∂u}{∂y} & =x & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =z & \,\frac{∂v}{∂z} & =y \\ \frac{∂w}{∂x} & =z & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =x\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}y & x & 0 \\ 0 & z & y \\ z & 0 & x\end{aligned}| \\  & =y|\begin{aligned}z & y \\ 0 & x\end{aligned}|-x|\begin{aligned}0 & y \\ z & x\end{aligned}| \\  & =y(xz-0)-x(0-yz) \\  & =xyz+xyz \\  & =2xyz.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}2xyz & =2\sqrt{(xyz)^{2}} \\  & =2\sqrt{{x}^{2}{y}^{2}{z}^{2}} \\  & =2\sqrt{xy(yz)(xz)} \\  & =2\sqrt{uvw}\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{2\sqrt{uvw}}\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-161806 1

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}2\left(xy\right) \\ yz \\ xz\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x,y,z>0.$*

- $\frac{1}{2}\left(\sqrt{\left(\frac{u}{2}\right)vw}\right)$
- $\frac{1}{2}\left(\frac{1}{2\sqrt{\left(\frac{u}{2}\right)vw}}\right)$
- $\frac{1}{2}\left(\frac{1}{\left(\frac{u}{2}\right)vw}\right)$
- $\frac{1}{2}\left(4\left(\frac{u}{2}\right)vw\right)$
- $\frac{1}{2}\left(\frac{2}{\sqrt{\left(\frac{u}{2}\right)vw}}\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=2\left(xy\right),\,v(x,y,z)=yz,\,w(x,y,z)=xz.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =2\left(y\right) & \,\frac{∂u}{∂y} & =2\left(x\right) & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =z & \,\frac{∂v}{∂z} & =y \\ \frac{∂w}{∂x} & =z & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =x\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2\left(y\right) & 2\left(x\right) & 0 \\ 0 & z & y \\ z & 0 & x\end{aligned}| \\  & =2\left(y|\begin{aligned}z & y \\ 0 & x\end{aligned}|-x|\begin{aligned}0 & y \\ z & x\end{aligned}|\right)\\  & =2\left(y(xz-0)-x(0-yz)\right)\\  & =2\left(xyz+xyz\right)\\  & =4 x y z.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}2\left(2xyz\right) & =2\left(2\sqrt{(xyz)^{2}}\right) \\  & =2\left(2\sqrt{{x}^{2}{y}^{2}{z}^{2}}\right) \\  & =2\left(2\sqrt{xy(yz)(xz)}\right) \\  & =2\left(2\sqrt{\left(\frac{u}{2}\right)vw}\right)\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{\sqrt{2}}{4 \sqrt{u v w}}\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-161806 2

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}4\left(xy\right) \\ 4\left(yz\right) \\ 2\left(xz\right)\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x,y,z>0.$*

- $\frac{1}{32}\left(\sqrt{\left(\frac{u}{4}\right)\left(\frac{v}{4}\right)\left(\frac{w}{2}\right)}\right)$
- $\frac{1}{32}\left(4\left(\frac{u}{4}\right)\left(\frac{v}{4}\right)\left(\frac{w}{2}\right)\right)$
- $\frac{1}{32}\left(\frac{1}{\left(\frac{u}{4}\right)\left(\frac{v}{4}\right)\left(\frac{w}{2}\right)}\right)$
- $\frac{1}{32}\left(\frac{1}{2\sqrt{\left(\frac{u}{4}\right)\left(\frac{v}{4}\right)\left(\frac{w}{2}\right)}}\right)$
- $\frac{1}{32}\left(\frac{2}{\sqrt{\left(\frac{u}{4}\right)\left(\frac{v}{4}\right)\left(\frac{w}{2}\right)}}\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=4\left(xy\right),\,v(x,y,z)=4\left(yz\right),\,w(x,y,z)=2\left(xz\right).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =4\left(y\right) & \,\frac{∂u}{∂y} & =4\left(x\right) & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =4\left(z\right) & \,\frac{∂v}{∂z} & =4\left(y\right) \\ \frac{∂w}{∂x} & =2\left(z\right) & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =2\left(x\right)\end{aligned}
$$

Scaling the three derivative rows by $4, 4, 2$ multiplies the determinant by $32$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}4\left(y\right) & 4\left(x\right) & 0 \\ 0 & 4\left(z\right) & 4\left(y\right) \\ 2\left(z\right) & 0 & 2\left(x\right)\end{aligned}| \\  & =32\left(y|\begin{aligned}z & y \\ 0 & x\end{aligned}|-x|\begin{aligned}0 & y \\ z & x\end{aligned}|\right)\\  & =32\left(y(xz-0)-x(0-yz)\right)\\  & =32\left(xyz+xyz\right)\\  & =64 x y z.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}32\left(2xyz\right) & =32\left(2\sqrt{(xyz)^{2}}\right) \\  & =32\left(2\sqrt{{x}^{2}{y}^{2}{z}^{2}}\right) \\  & =32\left(2\sqrt{xy(yz)(xz)}\right) \\  & =32\left(2\sqrt{\left(\frac{u}{4}\right)\left(\frac{v}{4}\right)\left(\frac{w}{2}\right)}\right)\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{\sqrt{2}}{16 \sqrt{u v w}}\end{aligned}
$$

---

## Generated method coordinate-scale variant q-161806 1

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}2\left(xy\right) \\ yz \\ xz\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x,y,z>0.$*

- $- \frac{\sqrt{2}}{4 \sqrt{u v w}}$
- $2 \sqrt{2} \sqrt{u v w}$
- $\frac{\sqrt{2}}{8 \sqrt{u v w}}$
- $\frac{\sqrt{2}}{2 \sqrt{u v w}}$
- $\frac{\sqrt{2}}{4 \sqrt{u v w}}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=2\left(xy\right),\,v(x,y,z)=yz,\,w(x,y,z)=xz.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =2\left(y\right) & \,\frac{∂u}{∂y} & =2\left(x\right) & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =z & \,\frac{∂v}{∂z} & =y \\ \frac{∂w}{∂x} & =z & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =x\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2\left(y\right) & 2\left(x\right) & 0 \\ 0 & z & y \\ z & 0 & x\end{aligned}| \\  & =2\left(y|\begin{aligned}z & y \\ 0 & x\end{aligned}|-x|\begin{aligned}0 & y \\ z & x\end{aligned}|\right)\\  & =2\left(y(xz-0)-x(0-yz)\right)\\  & =2\left(xyz+xyz\right)\\  & =4 x y z.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}2\left(2xyz\right) & =2\left(2\sqrt{(xyz)^{2}}\right) \\  & =2\left(2\sqrt{{x}^{2}{y}^{2}{z}^{2}}\right) \\  & =2\left(2\sqrt{xy(yz)(xz)}\right) \\  & =2\left(2\sqrt{\left(\frac{u}{2}\right)vw}\right)\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{\sqrt{2}}{4 \sqrt{u v w}}\end{aligned}
$$

---

## Generated method coordinate-scale variant q-161806 2

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}4\left(xy\right) \\ 4\left(yz\right) \\ 2\left(xz\right)\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x,y,z>0.$*

- $- \frac{\sqrt{2}}{16 \sqrt{u v w}}$
- $\frac{\sqrt{2}}{4 \sqrt{u v w}}$
- $\frac{\sqrt{2}}{64 \sqrt{u v w}}$
- $8 \sqrt{2} \sqrt{u v w}$
- $\frac{\sqrt{2}}{16 \sqrt{u v w}}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=4\left(xy\right),\,v(x,y,z)=4\left(yz\right),\,w(x,y,z)=2\left(xz\right).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =4\left(y\right) & \,\frac{∂u}{∂y} & =4\left(x\right) & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =4\left(z\right) & \,\frac{∂v}{∂z} & =4\left(y\right) \\ \frac{∂w}{∂x} & =2\left(z\right) & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =2\left(x\right)\end{aligned}
$$

Scaling the three derivative rows by $4, 4, 2$ multiplies the determinant by $32$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}4\left(y\right) & 4\left(x\right) & 0 \\ 0 & 4\left(z\right) & 4\left(y\right) \\ 2\left(z\right) & 0 & 2\left(x\right)\end{aligned}| \\  & =32\left(y|\begin{aligned}z & y \\ 0 & x\end{aligned}|-x|\begin{aligned}0 & y \\ z & x\end{aligned}|\right)\\  & =32\left(y(xz-0)-x(0-yz)\right)\\  & =32\left(xyz+xyz\right)\\  & =64 x y z.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}32\left(2xyz\right) & =32\left(2\sqrt{(xyz)^{2}}\right) \\  & =32\left(2\sqrt{{x}^{2}{y}^{2}{z}^{2}}\right) \\  & =32\left(2\sqrt{xy(yz)(xz)}\right) \\  & =32\left(2\sqrt{\left(\frac{u}{4}\right)\left(\frac{v}{4}\right)\left(\frac{w}{2}\right)}\right)\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{\sqrt{2}}{16 \sqrt{u v w}}\end{aligned}
$$

---

## Repaired evidence profile q-161806

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}xy \\ yz \\ xz\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x,y,z>0.$*

- $\sqrt{uvw}$
- $\frac{1}{2\sqrt{uvw}}$
- $\frac{2}{\sqrt{uvw}}$
- $\frac{1}{uvw}$
- $4uvw$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=xy,\,v(x,y,z)=yz,\,w(x,y,z)=xz.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =y & \,\frac{∂u}{∂y} & =x & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =z & \,\frac{∂v}{∂z} & =y \\ \frac{∂w}{∂x} & =z & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =x\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}y & x & 0 \\ 0 & z & y \\ z & 0 & x\end{aligned}| \\  & =y|\begin{aligned}z & y \\ 0 & x\end{aligned}|-x|\begin{aligned}0 & y \\ z & x\end{aligned}| \\  & =y(xz-0)-x(0-yz) \\  & =xyz+xyz \\  & =2xyz.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}2xyz & =2\sqrt{(xyz)^{2}} \\  & =2\sqrt{{x}^{2}{y}^{2}{z}^{2}} \\  & =2\sqrt{xy(yz)(xz)} \\  & =2\sqrt{uvw}\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{2\sqrt{uvw}}\end{aligned}
$$

---

## Observed original q-161807

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}y{z}^{2} \\ z{x}^{2} \\ x{y}^{2}\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x,y,z\ne 0.$*

- $3(uvw)^{3}$
- $\frac{1}{9(uvw)^{2/3}}$
- $3(uvw)^{1/3}$
- $\frac{9}{(uvw)^{2}}$
- $(uvw)^{2/3}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=y{z}^{2},\,v(x,y,z)=z{x}^{2},\,w(x,y,z)=x{y}^{2}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & ={z}^{2} & \,\frac{∂u}{∂z} & =2yz \\ \frac{∂v}{∂x} & =2xz & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & ={x}^{2} \\ \frac{∂w}{∂x} & ={y}^{2} & \,\frac{∂w}{∂y} & =2xy & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & {z}^{2} & 2yz \\ 2xz & 0 & {x}^{2} \\ {y}^{2} & 2xy & 0\end{aligned}| \\  & =-{z}^{2}|\begin{aligned}2xy & {x}^{2} \\ {y}^{2} & 0\end{aligned}|+2yz|\begin{aligned}2xz & 0 \\ {y}^{2} & 2xy\end{aligned}| \\  & =-{z}^{2}(0-{x}^{2}{y}^{2})+2yz(4{x}^{2}yz-0) \\  & ={x}^{2}{y}^{2}{z}^{2}+8{x}^{2}{y}^{2}{z}^{2} \\  & =9{x}^{2}{y}^{2}{z}^{2}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}9{x}^{2}{y}^{2}{z}^{2} & =9{({x}^{3}{y}^{3}{z}^{3})}^{2/3} \\  & =9{(y{z}^{2}\cdot z{x}^{2}\cdot x{y}^{2})}^{2/3} \\  & =9(uvw)^{2/3}.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{9(uvw)^{2/3}}\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-161807 1

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}2\left(y{z}^{2}\right) \\ z{x}^{2} \\ x{y}^{2}\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x,y,z\ne 0.$*

- $\frac{1}{2}\left(3(\left(\frac{u}{2}\right)vw)^{3}\right)$
- $\frac{1}{2}\left(\frac{1}{9(\left(\frac{u}{2}\right)vw)^{2/3}}\right)$
- $\frac{1}{2}\left(\frac{9}{(\left(\frac{u}{2}\right)vw)^{2}}\right)$
- $\frac{1}{2}\left((\left(\frac{u}{2}\right)vw)^{2/3}\right)$
- $\frac{1}{2}\left(3(\left(\frac{u}{2}\right)vw)^{1/3}\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=2\left(y{z}^{2}\right),\,v(x,y,z)=z{x}^{2},\,w(x,y,z)=x{y}^{2}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =2\left({z}^{2}\right) & \,\frac{∂u}{∂z} & =2\left(2yz\right) \\ \frac{∂v}{∂x} & =2xz & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & ={x}^{2} \\ \frac{∂w}{∂x} & ={y}^{2} & \,\frac{∂w}{∂y} & =2xy & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & 2\left({z}^{2}\right) & 2\left(2yz\right) \\ 2xz & 0 & {x}^{2} \\ {y}^{2} & 2xy & 0\end{aligned}| \\  & =2\left(-{z}^{2}|\begin{aligned}2xy & {x}^{2} \\ {y}^{2} & 0\end{aligned}|+2yz|\begin{aligned}2xz & 0 \\ {y}^{2} & 2xy\end{aligned}|\right)\\  & =2\left(-{z}^{2}(0-{x}^{2}{y}^{2})+2yz(4{x}^{2}yz-0)\right)\\  & =2\left({x}^{2}{y}^{2}{z}^{2}+8{x}^{2}{y}^{2}{z}^{2}\right)\\  & =18 x^{2} y^{2} z^{2}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}2\left(9{x}^{2}{y}^{2}{z}^{2}\right) & =2\left(9{({x}^{3}{y}^{3}{z}^{3})}^{2/3}\right) \\  & =2\left(9{(y{z}^{2}\cdot z{x}^{2}\cdot x{y}^{2})}^{2/3}\right) \\  & =2\left(9(\left(\frac{u}{2}\right)vw)^{2/3}\right).\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{2^{\frac{2}{3}}}{18 \left(u v w\right)^{\frac{2}{3}}}\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-161807 2

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}4\left(y{z}^{2}\right) \\ 4\left(z{x}^{2}\right) \\ 2\left(x{y}^{2}\right)\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x,y,z\ne 0.$*

- $\frac{1}{32}\left(3(\left(\frac{u}{4}\right)\left(\frac{v}{4}\right)\left(\frac{w}{2}\right))^{3}\right)$
- $\frac{1}{32}\left((\left(\frac{u}{4}\right)\left(\frac{v}{4}\right)\left(\frac{w}{2}\right))^{2/3}\right)$
- $\frac{1}{32}\left(\frac{9}{(\left(\frac{u}{4}\right)\left(\frac{v}{4}\right)\left(\frac{w}{2}\right))^{2}}\right)$
- $\frac{1}{32}\left(\frac{1}{9(\left(\frac{u}{4}\right)\left(\frac{v}{4}\right)\left(\frac{w}{2}\right))^{2/3}}\right)$
- $\frac{1}{32}\left(3(\left(\frac{u}{4}\right)\left(\frac{v}{4}\right)\left(\frac{w}{2}\right))^{1/3}\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=4\left(y{z}^{2}\right),\,v(x,y,z)=4\left(z{x}^{2}\right),\,w(x,y,z)=2\left(x{y}^{2}\right).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =4\left({z}^{2}\right) & \,\frac{∂u}{∂z} & =4\left(2yz\right) \\ \frac{∂v}{∂x} & =4\left(2xz\right) & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =4\left({x}^{2}\right) \\ \frac{∂w}{∂x} & =2\left({y}^{2}\right) & \,\frac{∂w}{∂y} & =2\left(2xy\right) & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $4, 4, 2$ multiplies the determinant by $32$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & 4\left({z}^{2}\right) & 4\left(2yz\right) \\ 4\left(2xz\right) & 0 & 4\left({x}^{2}\right) \\ 2\left({y}^{2}\right) & 2\left(2xy\right) & 0\end{aligned}| \\  & =32\left(-{z}^{2}|\begin{aligned}2xy & {x}^{2} \\ {y}^{2} & 0\end{aligned}|+2yz|\begin{aligned}2xz & 0 \\ {y}^{2} & 2xy\end{aligned}|\right)\\  & =32\left(-{z}^{2}(0-{x}^{2}{y}^{2})+2yz(4{x}^{2}yz-0)\right)\\  & =32\left({x}^{2}{y}^{2}{z}^{2}+8{x}^{2}{y}^{2}{z}^{2}\right)\\  & =288 x^{2} y^{2} z^{2}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}32\left(9{x}^{2}{y}^{2}{z}^{2}\right) & =32\left(9{({x}^{3}{y}^{3}{z}^{3})}^{2/3}\right) \\  & =32\left(9{(y{z}^{2}\cdot z{x}^{2}\cdot x{y}^{2})}^{2/3}\right) \\  & =32\left(9(\left(\frac{u}{4}\right)\left(\frac{v}{4}\right)\left(\frac{w}{2}\right))^{2/3}\right).\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{\sqrt[3]{2}}{36 \left(u v w\right)^{\frac{2}{3}}}\end{aligned}
$$

---

## Generated method coordinate-scale variant q-161807 1

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}2\left(y{z}^{2}\right) \\ z{x}^{2} \\ x{y}^{2}\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x,y,z>0.$*

- $- \frac{2^{\frac{2}{3}}}{18 \left(u v w\right)^{\frac{2}{3}}}$
- $9 \sqrt[3]{2} \left(u v w\right)^{\frac{2}{3}}$
- $\frac{2^{\frac{2}{3}}}{36 \left(u v w\right)^{\frac{2}{3}}}$
- $\frac{2^{\frac{2}{3}}}{9 \left(u v w\right)^{\frac{2}{3}}}$
- $\frac{2^{\frac{2}{3}}}{18 \left(u v w\right)^{\frac{2}{3}}}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=2\left(y{z}^{2}\right),\,v(x,y,z)=z{x}^{2},\,w(x,y,z)=x{y}^{2}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =2\left({z}^{2}\right) & \,\frac{∂u}{∂z} & =2\left(2yz\right) \\ \frac{∂v}{∂x} & =2xz & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & ={x}^{2} \\ \frac{∂w}{∂x} & ={y}^{2} & \,\frac{∂w}{∂y} & =2xy & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & 2\left({z}^{2}\right) & 2\left(2yz\right) \\ 2xz & 0 & {x}^{2} \\ {y}^{2} & 2xy & 0\end{aligned}| \\  & =2\left(-{z}^{2}|\begin{aligned}2xz & {x}^{2} \\ {y}^{2} & 0\end{aligned}|+2yz|\begin{aligned}2xz & 0 \\ {y}^{2} & 2xy\end{aligned}|\right)\\  & =2\left(-{z}^{2}(0-{x}^{2}{y}^{2})+2yz(4{x}^{2}yz-0)\right)\\  & =2\left({x}^{2}{y}^{2}{z}^{2}+8{x}^{2}{y}^{2}{z}^{2}\right)\\  & =18 x^{2} y^{2} z^{2}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}2\left(9{x}^{2}{y}^{2}{z}^{2}\right) & =2\left(9{({x}^{3}{y}^{3}{z}^{3})}^{2/3}\right) \\  & =2\left(9{(y{z}^{2}\cdot z{x}^{2}\cdot x{y}^{2})}^{2/3}\right) \\  & =2\left(9(\left(\frac{u}{2}\right)vw)^{2/3}\right).\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{2^{\frac{2}{3}}}{18 \left(u v w\right)^{\frac{2}{3}}}\end{aligned}
$$

---

## Generated method coordinate-scale variant q-161807 2

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}4\left(y{z}^{2}\right) \\ 4\left(z{x}^{2}\right) \\ 2\left(x{y}^{2}\right)\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x,y,z>0.$*

- $- \frac{\sqrt[3]{2}}{36 \left(u v w\right)^{\frac{2}{3}}}$
- $\frac{\sqrt[3]{2}}{9 \left(u v w\right)^{\frac{2}{3}}}$
- $\frac{\sqrt[3]{2}}{144 \left(u v w\right)^{\frac{2}{3}}}$
- $18 \cdot 2^{\frac{2}{3}} \left(u v w\right)^{\frac{2}{3}}$
- $\frac{\sqrt[3]{2}}{36 \left(u v w\right)^{\frac{2}{3}}}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=4\left(y{z}^{2}\right),\,v(x,y,z)=4\left(z{x}^{2}\right),\,w(x,y,z)=2\left(x{y}^{2}\right).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =4\left({z}^{2}\right) & \,\frac{∂u}{∂z} & =4\left(2yz\right) \\ \frac{∂v}{∂x} & =4\left(2xz\right) & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =4\left({x}^{2}\right) \\ \frac{∂w}{∂x} & =2\left({y}^{2}\right) & \,\frac{∂w}{∂y} & =2\left(2xy\right) & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $4, 4, 2$ multiplies the determinant by $32$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & 4\left({z}^{2}\right) & 4\left(2yz\right) \\ 4\left(2xz\right) & 0 & 4\left({x}^{2}\right) \\ 2\left({y}^{2}\right) & 2\left(2xy\right) & 0\end{aligned}| \\  & =32\left(-{z}^{2}|\begin{aligned}2xz & {x}^{2} \\ {y}^{2} & 0\end{aligned}|+2yz|\begin{aligned}2xz & 0 \\ {y}^{2} & 2xy\end{aligned}|\right)\\  & =32\left(-{z}^{2}(0-{x}^{2}{y}^{2})+2yz(4{x}^{2}yz-0)\right)\\  & =32\left({x}^{2}{y}^{2}{z}^{2}+8{x}^{2}{y}^{2}{z}^{2}\right)\\  & =288 x^{2} y^{2} z^{2}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}32\left(9{x}^{2}{y}^{2}{z}^{2}\right) & =32\left(9{({x}^{3}{y}^{3}{z}^{3})}^{2/3}\right) \\  & =32\left(9{(y{z}^{2}\cdot z{x}^{2}\cdot x{y}^{2})}^{2/3}\right) \\  & =32\left(9(\left(\frac{u}{4}\right)\left(\frac{v}{4}\right)\left(\frac{w}{2}\right))^{2/3}\right).\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{\sqrt[3]{2}}{36 \left(u v w\right)^{\frac{2}{3}}}\end{aligned}
$$

---

## Repaired evidence profile q-161807

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}y{z}^{2} \\ z{x}^{2} \\ x{y}^{2}\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $x,y,z>0.$*

- $3(uvw)^{3}$
- $\frac{1}{9(uvw)^{2/3}}$
- $3(uvw)^{1/3}$
- $\frac{9}{(uvw)^{2}}$
- $(uvw)^{2/3}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=y{z}^{2},\,v(x,y,z)=z{x}^{2},\,w(x,y,z)=x{y}^{2}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & ={z}^{2} & \,\frac{∂u}{∂z} & =2yz \\ \frac{∂v}{∂x} & =2xz & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & ={x}^{2} \\ \frac{∂w}{∂x} & ={y}^{2} & \,\frac{∂w}{∂y} & =2xy & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & {z}^{2} & 2yz \\ 2xz & 0 & {x}^{2} \\ {y}^{2} & 2xy & 0\end{aligned}| \\  & =-{z}^{2}|\begin{aligned}2xz & {x}^{2} \\ {y}^{2} & 0\end{aligned}|+2yz|\begin{aligned}2xz & 0 \\ {y}^{2} & 2xy\end{aligned}| \\  & =-{z}^{2}(0-{x}^{2}{y}^{2})+2yz(4{x}^{2}yz-0) \\  & ={x}^{2}{y}^{2}{z}^{2}+8{x}^{2}{y}^{2}{z}^{2} \\  & =9{x}^{2}{y}^{2}{z}^{2}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}9{x}^{2}{y}^{2}{z}^{2} & =9{({x}^{3}{y}^{3}{z}^{3})}^{2/3} \\  & =9{(y{z}^{2}\cdot z{x}^{2}\cdot x{y}^{2})}^{2/3} \\  & =9(uvw)^{2/3}.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{9(uvw)^{2/3}}\end{aligned}
$$

---

## Observed original q-161808

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}\frac{z}{y} \\ y \\ xz\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $y,z\ne 0.$*

- $\frac{v}{{u}^{2}}$
- $\frac{4}{vw}$
- $-\frac{1}{u}$
- $-\frac{w}{v}$
- $\frac{2u}{v-w}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=\frac{z}{y},\,v(x,y,z)=y,\,w(x,y,z)=xz.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =-\frac{z}{{y}^{2}} & \,\frac{∂u}{∂z} & =\frac{1}{y} \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =1 & \,\frac{∂v}{∂z} & =0 \\ \frac{∂w}{∂x} & =z & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =x\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & -\frac{z}{{y}^{2}} & \frac{1}{y} \\ 0 & 1 & 0 \\ z & 0 & x\end{aligned}| \\  & =z|\begin{aligned}-\frac{z}{{y}^{2}} & \frac{1}{y} \\ 1 & 0\end{aligned}| \\  & =z(0-\frac{1}{y}) \\  & =-\frac{z}{y}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}-\frac{z}{y} & =-u.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{(-u)} \\  & =-\frac{1}{u}\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-161808 1

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}2\left(\frac{z}{y}\right) \\ y \\ xz\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $y,z\ne 0.$*

- $\frac{1}{2}\left(\frac{v}{{\left(\frac{u}{2}\right)}^{2}}\right)$
- $\frac{1}{2}\left(\frac{4}{vw}\right)$
- $\frac{1}{2}\left(-\frac{w}{v}\right)$
- $\frac{1}{2}\left(\frac{2\left(\frac{u}{2}\right)}{v-w}\right)$
- $\frac{1}{2}\left(-\frac{1}{\left(\frac{u}{2}\right)}\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=2\left(\frac{z}{y}\right),\,v(x,y,z)=y,\,w(x,y,z)=xz.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =2\left(-\frac{z}{{y}^{2}}\right) & \,\frac{∂u}{∂z} & =2\left(\frac{1}{y}\right) \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =1 & \,\frac{∂v}{∂z} & =0 \\ \frac{∂w}{∂x} & =z & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =x\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & 2\left(-\frac{z}{{y}^{2}}\right) & 2\left(\frac{1}{y}\right) \\ 0 & 1 & 0 \\ z & 0 & x\end{aligned}| \\  & =2\left(z|\begin{aligned}-\frac{z}{{y}^{2}} & \frac{1}{y} \\ 1 & 0\end{aligned}|\right)\\  & =2\left(z(0-\frac{1}{y})\right)\\  & =- \frac{2 z}{y}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}2\left(-\frac{z}{y}\right) & =2\left(-\left(\frac{u}{2}\right)\right).\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{2}\left(\frac{1}{(-\left(\frac{u}{2}\right))}\right) \\  & =- \frac{1}{u}\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-161808 2

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}4\left(\frac{z}{y}\right) \\ 4\left(y\right) \\ 2\left(xz\right)\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $y,z\ne 0.$*

- $\frac{1}{32}\left(\frac{\left(\frac{v}{4}\right)}{{\left(\frac{u}{4}\right)}^{2}}\right)$
- $\frac{1}{32}\left(\frac{2\left(\frac{u}{4}\right)}{\left(\frac{v}{4}\right)-\left(\frac{w}{2}\right)}\right)$
- $\frac{1}{32}\left(-\frac{\left(\frac{w}{2}\right)}{\left(\frac{v}{4}\right)}\right)$
- $\frac{1}{32}\left(\frac{4}{\left(\frac{v}{4}\right)\left(\frac{w}{2}\right)}\right)$
- $\frac{1}{32}\left(-\frac{1}{\left(\frac{u}{4}\right)}\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=4\left(\frac{z}{y}\right),\,v(x,y,z)=4\left(y\right),\,w(x,y,z)=2\left(xz\right).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =4\left(-\frac{z}{{y}^{2}}\right) & \,\frac{∂u}{∂z} & =4\left(\frac{1}{y}\right) \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =4\left(1\right) & \,\frac{∂v}{∂z} & =0 \\ \frac{∂w}{∂x} & =2\left(z\right) & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =2\left(x\right)\end{aligned}
$$

Scaling the three derivative rows by $4, 4, 2$ multiplies the determinant by $32$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & 4\left(-\frac{z}{{y}^{2}}\right) & 4\left(\frac{1}{y}\right) \\ 0 & 4\left(1\right) & 0 \\ 2\left(z\right) & 0 & 2\left(x\right)\end{aligned}| \\  & =32\left(z|\begin{aligned}-\frac{z}{{y}^{2}} & \frac{1}{y} \\ 1 & 0\end{aligned}|\right)\\  & =32\left(z(0-\frac{1}{y})\right)\\  & =- \frac{32 z}{y}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}32\left(-\frac{z}{y}\right) & =32\left(-\left(\frac{u}{4}\right)\right).\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{32}\left(\frac{1}{(-\left(\frac{u}{4}\right))}\right) \\  & =- \frac{1}{8 u}\end{aligned}
$$

---

## Generated method coordinate-scale variant q-161808 1

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}2\left(\frac{z}{y}\right) \\ y \\ xz\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $y,z\ne 0.$*

- $\frac{1}{u}$
- $- u$
- $- \frac{1}{2 u}$
- $- \frac{2}{u}$
- $- \frac{1}{u}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=2\left(\frac{z}{y}\right),\,v(x,y,z)=y,\,w(x,y,z)=xz.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =2\left(-\frac{z}{{y}^{2}}\right) & \,\frac{∂u}{∂z} & =2\left(\frac{1}{y}\right) \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =1 & \,\frac{∂v}{∂z} & =0 \\ \frac{∂w}{∂x} & =z & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =x\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & 2\left(-\frac{z}{{y}^{2}}\right) & 2\left(\frac{1}{y}\right) \\ 0 & 1 & 0 \\ z & 0 & x\end{aligned}| \\  & =2\left(z|\begin{aligned}-\frac{z}{{y}^{2}} & \frac{1}{y} \\ 1 & 0\end{aligned}|\right)\\  & =2\left(z(0-\frac{1}{y})\right)\\  & =- \frac{2 z}{y}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}2\left(-\frac{z}{y}\right) & =2\left(-\left(\frac{u}{2}\right)\right).\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{2}\left(\frac{1}{(-\left(\frac{u}{2}\right))}\right) \\  & =- \frac{1}{u}\end{aligned}
$$

---

## Generated method coordinate-scale variant q-161808 2

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}4\left(\frac{z}{y}\right) \\ 4\left(y\right) \\ 2\left(xz\right)\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $y,z\ne 0.$*

- $\frac{1}{8 u}$
- $- \frac{1}{2 u}$
- $- \frac{1}{32 u}$
- $- 8 u$
- $- \frac{1}{8 u}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=4\left(\frac{z}{y}\right),\,v(x,y,z)=4\left(y\right),\,w(x,y,z)=2\left(xz\right).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =4\left(-\frac{z}{{y}^{2}}\right) & \,\frac{∂u}{∂z} & =4\left(\frac{1}{y}\right) \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =4\left(1\right) & \,\frac{∂v}{∂z} & =0 \\ \frac{∂w}{∂x} & =2\left(z\right) & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =2\left(x\right)\end{aligned}
$$

Scaling the three derivative rows by $4, 4, 2$ multiplies the determinant by $32$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & 4\left(-\frac{z}{{y}^{2}}\right) & 4\left(\frac{1}{y}\right) \\ 0 & 4\left(1\right) & 0 \\ 2\left(z\right) & 0 & 2\left(x\right)\end{aligned}| \\  & =32\left(z|\begin{aligned}-\frac{z}{{y}^{2}} & \frac{1}{y} \\ 1 & 0\end{aligned}|\right)\\  & =32\left(z(0-\frac{1}{y})\right)\\  & =- \frac{32 z}{y}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}32\left(-\frac{z}{y}\right) & =32\left(-\left(\frac{u}{4}\right)\right).\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{32}\left(\frac{1}{(-\left(\frac{u}{4}\right))}\right) \\  & =- \frac{1}{8 u}\end{aligned}
$$

---

## Repaired evidence profile q-161808

Consider the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)).$ The inverse transformation ${T}^{-1}(x,y,z)\to (u(x,y,z),v(x,y,z),w(x,y,z))$ is given by

$$
{T}^{-1}:[\begin{aligned}x \\ y \\ z\end{aligned}]⟶[\begin{aligned}\frac{z}{y} \\ y \\ xz\end{aligned}].
$$

Find the Jacobian determinant of $T.$

*Hint: You can assume that $y,z\ne 0.$*

- $\frac{v}{{u}^{2}}$
- $\frac{4}{vw}$
- $-\frac{1}{u}$
- $-\frac{w}{v}$
- $\frac{2u}{v-w}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

Here, we have 

$$
u(x,y,z)=\frac{z}{y},\,v(x,y,z)=y,\,w(x,y,z)=xz.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =-\frac{z}{{y}^{2}} & \,\frac{∂u}{∂z} & =\frac{1}{y} \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =1 & \,\frac{∂v}{∂z} & =0 \\ \frac{∂w}{∂x} & =z & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =x\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & -\frac{z}{{y}^{2}} & \frac{1}{y} \\ 0 & 1 & 0 \\ z & 0 & x\end{aligned}| \\  & =z|\begin{aligned}-\frac{z}{{y}^{2}} & \frac{1}{y} \\ 1 & 0\end{aligned}| \\  & =z(0-\frac{1}{y}) \\  & =-\frac{z}{y}.\end{aligned}
$$

Writing down $\frac{∂(u,v,w)}{∂(x,y,z)}$ in terms of $u,$ $v,$ and $w,$ we obtain

$$
\begin{aligned}-\frac{z}{y} & =-u.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{(-u)} \\  & =-\frac{1}{u}\end{aligned}
$$

---

## Observed original q-161797

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=x,\,v=2y,\,w=3z.
$$

- $\frac{1}{3}$
- $3$
- $6$
- $12$
- $\frac{1}{6}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =1 & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =2 & \,\frac{∂v}{∂z} & =0 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =3\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 3\end{aligned}| \\  & =1|\begin{aligned}2 & 0 \\ 0 & 3\end{aligned}| \\  & =1(6-0) \\  & =6.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{6}\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-161797 1

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=2\left(x\right),\,v=2y,\,w=3z.
$$

- $\frac{1}{2}\left(\frac{1}{3}\right)$
- $\frac{1}{2}\left(3\right)$
- $\frac{1}{2}\left(12\right)$
- $\frac{1}{2}\left(\frac{1}{6}\right)$
- $\frac{1}{2}\left(6\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =2\left(1\right) & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =2 & \,\frac{∂v}{∂z} & =0 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =3\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2\left(1\right) & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 3\end{aligned}| \\  & =2\left(1|\begin{aligned}2 & 0 \\ 0 & 3\end{aligned}|\right)\\  & =2\left(1(6-0)\right)\\  & =12.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{12}\end{aligned}
$$

---

## Generated observed coordinate-scale variant q-161797 2

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=4\left(x\right),\,v=4\left(2y\right),\,w=3z.
$$

- $\frac{1}{16}\left(\frac{1}{3}\right)$
- $\frac{1}{16}\left(\frac{1}{6}\right)$
- $\frac{1}{16}\left(12\right)$
- $\frac{1}{16}\left(3\right)$
- $\frac{1}{16}\left(6\right)$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =4\left(1\right) & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =4\left(2\right) & \,\frac{∂v}{∂z} & =0 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =3\end{aligned}
$$

Scaling the three derivative rows by $4, 4, 1$ multiplies the determinant by $16$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}4\left(1\right) & 0 & 0 \\ 0 & 4\left(2\right) & 0 \\ 0 & 0 & 3\end{aligned}| \\  & =16\left(1|\begin{aligned}2 & 0 \\ 0 & 3\end{aligned}|\right)\\  & =16\left(1(6-0)\right)\\  & =96.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{96}\end{aligned}
$$

---

## Generated method coordinate-scale variant q-161797 1

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=2\left(x\right),\,v=2y,\,w=3z.
$$

- $- \frac{1}{12}$
- $12$
- $\frac{1}{24}$
- $\frac{1}{6}$
- $\frac{1}{12}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =2\left(1\right) & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =2 & \,\frac{∂v}{∂z} & =0 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =3\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2\left(1\right) & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 3\end{aligned}| \\  & =2\left(1|\begin{aligned}2 & 0 \\ 0 & 3\end{aligned}|\right)\\  & =2\left(1(6-0)\right)\\  & =12.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{12}\end{aligned}
$$

---

## Generated method coordinate-scale variant q-161797 2

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=4\left(x\right),\,v=4\left(2y\right),\,w=3z.
$$

- $- \frac{1}{96}$
- $\frac{1}{24}$
- $\frac{1}{384}$
- $96$
- $\frac{1}{96}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =4\left(1\right) & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =4\left(2\right) & \,\frac{∂v}{∂z} & =0 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =3\end{aligned}
$$

Scaling the three derivative rows by $4, 4, 1$ multiplies the determinant by $16$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}4\left(1\right) & 0 & 0 \\ 0 & 4\left(2\right) & 0 \\ 0 & 0 & 3\end{aligned}| \\  & =16\left(1|\begin{aligned}2 & 0 \\ 0 & 3\end{aligned}|\right)\\  & =16\left(1(6-0)\right)\\  & =96.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{96}\end{aligned}
$$

---

## Repaired evidence profile q-161797

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=x,\,v=2y,\,w=3z.
$$

- $\frac{1}{3}$
- $3$
- $6$
- $12$
- $\frac{1}{6}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =1 & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =2 & \,\frac{∂v}{∂z} & =0 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =3\end{aligned}
$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}1 & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 3\end{aligned}| \\  & =1|\begin{aligned}2 & 0 \\ 0 & 3\end{aligned}| \\  & =1(6-0) \\  & =6.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{6}\end{aligned}
$$

---

## Authored easy example 1

Find the Jacobian determinant of the transformation $T:(u,v,w)\to(x(u,v,w),y(u,v,w),z(u,v,w))$, given that

$$u=- 12 x\qquad v=y\qquad w=z.$$

- $\frac{1}{12}$
- $-12$
- $- \frac{1}{12}$
- $\frac{1}{144}$
- $1$

For a transformation

$$T:(u,v,w)\to(x(u,v,w),y(u,v,w),z(u,v,w)),$$

the Jacobian determinant of $T$ is $\frac{\partial(x,y,z)}{\partial(u,v,w)}$.

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{\partial(u,v,w)}{\partial(x,y,z)}$, the Jacobian determinant of ${T}^{-1}$.

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}.$$

First, we find the partial derivatives:

$$\begin{aligned}\frac{\partial u}{\partial x}=-12 & \frac{\partial u}{\partial y}=0 & \frac{\partial u}{\partial z}=0 \\ \frac{\partial v}{\partial x}=0 & \frac{\partial v}{\partial y}=1 & \frac{\partial v}{\partial z}=0 \\ \frac{\partial w}{\partial x}=0 & \frac{\partial w}{\partial y}=0 & \frac{\partial w}{\partial z}=1\end{aligned}$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)}&=|\begin{aligned}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{aligned}| \\ &=|\begin{aligned}-12 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{aligned}| \\ &=-12|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}| \\ &=-12\left(1\cdot 1-0\right) \\ &=-12\end{aligned}$$

Finally, we take the reciprocal:

$$\begin{aligned}\frac{\partial(x,y,z)}{\partial(u,v,w)}&=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1} \\ &=- \frac{1}{12}\end{aligned}$$

---

## Authored easy example 2

Find the Jacobian determinant of the transformation $T:(u,v,w)\to(x(u,v,w),y(u,v,w),z(u,v,w))$, given that

$$u=- 11 x\qquad v=y\qquad w=z.$$

- $\frac{1}{11}$
- $1$
- $\frac{1}{121}$
- $- \frac{1}{11}$
- $-11$

For a transformation

$$T:(u,v,w)\to(x(u,v,w),y(u,v,w),z(u,v,w)),$$

the Jacobian determinant of $T$ is $\frac{\partial(x,y,z)}{\partial(u,v,w)}$.

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{\partial(u,v,w)}{\partial(x,y,z)}$, the Jacobian determinant of ${T}^{-1}$.

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}.$$

First, we find the partial derivatives:

$$\begin{aligned}\frac{\partial u}{\partial x}=-11 & \frac{\partial u}{\partial y}=0 & \frac{\partial u}{\partial z}=0 \\ \frac{\partial v}{\partial x}=0 & \frac{\partial v}{\partial y}=1 & \frac{\partial v}{\partial z}=0 \\ \frac{\partial w}{\partial x}=0 & \frac{\partial w}{\partial y}=0 & \frac{\partial w}{\partial z}=1\end{aligned}$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)}&=|\begin{aligned}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{aligned}| \\ &=|\begin{aligned}-11 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{aligned}| \\ &=-11|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}| \\ &=-11\left(1\cdot 1-0\right) \\ &=-11\end{aligned}$$

Finally, we take the reciprocal:

$$\begin{aligned}\frac{\partial(x,y,z)}{\partial(u,v,w)}&=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1} \\ &=- \frac{1}{11}\end{aligned}$$

---

## Authored moderate example 1

Find the Jacobian determinant of the transformation $T:(u,v,w)\to(x(u,v,w),y(u,v,w),z(u,v,w))$, given that

$$u=- 8 x\qquad v=- 5 y\qquad w=z.$$

- $- \frac{1}{40}$
- $40$
- $\frac{1}{40}$
- $- \frac{1}{320}$
- $- \frac{1}{5}$

For a transformation

$$T:(u,v,w)\to(x(u,v,w),y(u,v,w),z(u,v,w)),$$

the Jacobian determinant of $T$ is $\frac{\partial(x,y,z)}{\partial(u,v,w)}$.

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{\partial(u,v,w)}{\partial(x,y,z)}$, the Jacobian determinant of ${T}^{-1}$.

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}.$$

First, we find the partial derivatives:

$$\begin{aligned}\frac{\partial u}{\partial x}=-8 & \frac{\partial u}{\partial y}=0 & \frac{\partial u}{\partial z}=0 \\ \frac{\partial v}{\partial x}=0 & \frac{\partial v}{\partial y}=-5 & \frac{\partial v}{\partial z}=0 \\ \frac{\partial w}{\partial x}=0 & \frac{\partial w}{\partial y}=0 & \frac{\partial w}{\partial z}=1\end{aligned}$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)}&=|\begin{aligned}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{aligned}| \\ &=|\begin{aligned}-8 & 0 & 0 \\ 0 & -5 & 0 \\ 0 & 0 & 1\end{aligned}| \\ &=-8|\begin{aligned}-5 & 0 \\ 0 & 1\end{aligned}| \\ &=-8\left(-5\cdot 1-0\right) \\ &=40\end{aligned}$$

Finally, we take the reciprocal:

$$\begin{aligned}\frac{\partial(x,y,z)}{\partial(u,v,w)}&=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1} \\ &=\frac{1}{40}\end{aligned}$$

---

## Authored moderate example 2

Find the Jacobian determinant of the transformation $T:(u,v,w)\to(x(u,v,w),y(u,v,w),z(u,v,w))$, given that

$$u=- 7 x\qquad v=3 y\qquad w=z.$$

- $\frac{1}{21}$
- $\frac{1}{3}$
- $\frac{1}{147}$
- $- \frac{1}{21}$
- $-21$

For a transformation

$$T:(u,v,w)\to(x(u,v,w),y(u,v,w),z(u,v,w)),$$

the Jacobian determinant of $T$ is $\frac{\partial(x,y,z)}{\partial(u,v,w)}$.

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{\partial(u,v,w)}{\partial(x,y,z)}$, the Jacobian determinant of ${T}^{-1}$.

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}.$$

First, we find the partial derivatives:

$$\begin{aligned}\frac{\partial u}{\partial x}=-7 & \frac{\partial u}{\partial y}=0 & \frac{\partial u}{\partial z}=0 \\ \frac{\partial v}{\partial x}=0 & \frac{\partial v}{\partial y}=3 & \frac{\partial v}{\partial z}=0 \\ \frac{\partial w}{\partial x}=0 & \frac{\partial w}{\partial y}=0 & \frac{\partial w}{\partial z}=1\end{aligned}$$

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$\begin{aligned}\frac{\partial(u,v,w)}{\partial(x,y,z)}&=|\begin{aligned}\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} & \frac{\partial u}{\partial z} \\ \frac{\partial v}{\partial x} & \frac{\partial v}{\partial y} & \frac{\partial v}{\partial z} \\ \frac{\partial w}{\partial x} & \frac{\partial w}{\partial y} & \frac{\partial w}{\partial z}\end{aligned}| \\ &=|\begin{aligned}-7 & 0 & 0 \\ 0 & 3 & 0 \\ 0 & 0 & 1\end{aligned}| \\ &=-7|\begin{aligned}3 & 0 \\ 0 & 1\end{aligned}| \\ &=-7\left(3\cdot 1-0\right) \\ &=-21\end{aligned}$$

Finally, we take the reciprocal:

$$\begin{aligned}\frac{\partial(x,y,z)}{\partial(u,v,w)}&=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1} \\ &=- \frac{1}{21}\end{aligned}$$

---

## Default moderate family source_161801, seed 0

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=3\left(y-3z\right),\,v=x+2z,\,w=4\left(3x-y\right).
$$

- $\frac{1}{324}$
- $108$
- $\frac{1}{36}$
- $- \frac{1}{108}$
- $\frac{1}{108}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =3\left(1\right) & \,\frac{∂u}{∂z} & =3\left(-3\right) \\ \frac{∂v}{∂x} & =1 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =2 \\ \frac{∂w}{∂x} & =4\left(3\right) & \,\frac{∂w}{∂y} & =4\left(-1\right) & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $3, 1, 4$ multiplies the determinant by $12$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & 3\left(1\right) & 3\left(-3\right) \\ 1 & 0 & 2 \\ 4\left(3\right) & 4\left(-1\right) & 0\end{aligned}| \\  & =12\left(-1|\begin{aligned}1 & 2 \\ 3 & 0\end{aligned}|-3|\begin{aligned}1 & 0 \\ 3 & -1\end{aligned}|\right)\\  & =12\left(-1(0-6)-3(-1-0)\right)\\  & =12\left(6+3\right)\\  & =108\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{108}\end{aligned}
$$

---

## Default moderate family source_161798, seed 1

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=2\left(x+y\right),\,v=2\left(z\right),\,w=2\left(4y-2{z}^{2}\right).
$$

- $- \frac{1}{16}$
- $- \frac{1}{64}$
- $-32$
- $- \frac{1}{32}$
- $\frac{1}{32}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =2\left(1\right) & \,\frac{∂u}{∂y} & =2\left(1\right) & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =2\left(1\right) \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =2\left(4\right) & \,\frac{∂w}{∂z} & =2\left(-4z\right)\end{aligned}
$$

Scaling the three derivative rows by $2, 2, 2$ multiplies the determinant by $8$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2\left(1\right) & 2\left(1\right) & 0 \\ 0 & 0 & 2\left(1\right) \\ 0 & 2\left(4\right) & 2\left(-4z\right)\end{aligned}| \\  & =8\left(1|\begin{aligned}0 & 1 \\ 4 & -4z\end{aligned}|\right)\\  & =8\left(1(0-4)\right)\\  & =-32.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{8}\left(\frac{1}{(-4)}\right) \\  & =- \frac{1}{32}\end{aligned}
$$

---

## Default moderate family source_39669, seed 2

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=2\left(2x+y\right),\,v=-x+3y-2z,\,w=3y+4z.
$$

- $\frac{1}{40}$
- $80$
- $\frac{1}{160}$
- $- \frac{1}{80}$
- $\frac{1}{80}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =2\left(2\right) & \,\frac{∂u}{∂y} & =2\left(1\right) & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =-1 & \,\frac{∂v}{∂y} & =3 & \,\frac{∂v}{∂z} & =-2 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =3 & \,\frac{∂w}{∂z} & =4\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 1$ multiplies the determinant by $2$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2\left(2\right) & 2\left(1\right) & 0 \\ -1 & 3 & -2 \\ 0 & 3 & 4\end{aligned}| \\  & =2\left(2|\begin{aligned}3 & -2 \\ 3 & 4\end{aligned}|-1|\begin{aligned}-1 & -2 \\ 0 & 4\end{aligned}|\right)\\  & =2\left(2(12+6)-1(-4-0)\right)\\  & =80.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{80}.\end{aligned}
$$

---

## Default moderate family source_161802, seed 5

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=3\left(3x+yz\right),\,v=z,\,w=-y.
$$

- $\frac{1}{27}$
- $\frac{1}{3}$
- $9$
- $\frac{1}{9}$
- $- \frac{1}{9}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =3\left(3\right) & \,\frac{∂u}{∂y} & =3\left(z\right) & \,\frac{∂u}{∂z} & =3\left(y\right) \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =1 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =-1 & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $3, 1, 1$ multiplies the determinant by $3$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}3\left(3\right) & 3\left(z\right) & 3\left(y\right) \\ 0 & 0 & 1 \\ 0 & -1 & 0\end{aligned}| \\  & =3\left(3|\begin{aligned}0 & 1 \\ -1 & 0\end{aligned}|\right)\\  & =3\left(3(0+1)\right)\\  & =9\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{9}\end{aligned}
$$

---

## Default moderate family source_161800, seed 7

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=2\left(z-y\right),\,v=3\left(x+z\right),\,w=2\left(-3x\right).
$$

- $36$
- $- \frac{1}{36}$
- $\frac{1}{72}$
- $\frac{1}{36}$
- $\frac{1}{18}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =0 & \,\frac{∂u}{∂y} & =2\left(-1\right) & \,\frac{∂u}{∂z} & =2\left(1\right) \\ \frac{∂v}{∂x} & =3\left(1\right) & \,\frac{∂v}{∂y} & =0 & \,\frac{∂v}{∂z} & =3\left(1\right) \\ \frac{∂w}{∂x} & =2\left(-3\right) & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =0\end{aligned}
$$

Scaling the three derivative rows by $2, 3, 2$ multiplies the determinant by $12$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}0 & 2\left(-1\right) & 2\left(1\right) \\ 3\left(1\right) & 0 & 3\left(1\right) \\ 2\left(-3\right) & 0 & 0\end{aligned}| \\  & =12\left(-(-1)|\begin{aligned}1 & 1 \\ -3 & 0\end{aligned}|+1|\begin{aligned}1 & 0 \\ -3 & 0\end{aligned}|\right)\\  & =12\left(1(0+3)+1(0-0)\right)\\  & =36\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{36}\end{aligned}
$$

---

## Default moderate family source_161797, seed 19

Find the Jacobian determinant of the transformation $T:(u,v,w)\to (x(u,v,w),y(u,v,w),z(u,v,w)),$ given that 

$$
u=2\left(x\right),\,v=2y,\,w=2\left(3z\right).
$$

- $24$
- $\frac{1}{12}$
- $- \frac{1}{24}$
- $\frac{1}{24}$
- $\frac{1}{48}$

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

In this case, we're only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:

- First, we compute $\frac{∂(u,v,w)}{∂(x,y,z)},$ the Jacobian determinant of ${T}^{-1}.$

- Then, we will compute the Jacobian determinant of $T$ using the relation

$$
\frac{∂(x,y,z)}{∂(u,v,w)}={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂u}{∂x} & =2\left(1\right) & \,\frac{∂u}{∂y} & =0 & \,\frac{∂u}{∂z} & =0 \\ \frac{∂v}{∂x} & =0 & \,\frac{∂v}{∂y} & =2 & \,\frac{∂v}{∂z} & =0 \\ \frac{∂w}{∂x} & =0 & \,\frac{∂w}{∂y} & =0 & \,\frac{∂w}{∂z} & =2\left(3\right)\end{aligned}
$$

Scaling the three derivative rows by $2, 1, 2$ multiplies the determinant by $4$.

Therefore, the corresponding Jacobian determinant of ${T}^{-1}$ is

$$
\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} & \frac{∂u}{∂z} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y} & \frac{∂v}{∂z} \\ \frac{∂w}{∂x} & \frac{∂w}{∂y} & \frac{∂w}{∂z}\end{aligned}| \\  & =|\begin{aligned}2\left(1\right) & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 2\left(3\right)\end{aligned}| \\  & =4\left(1|\begin{aligned}2 & 0 \\ 0 & 3\end{aligned}|\right)\\  & =4\left(1(6-0)\right)\\  & =24.\end{aligned}
$$

Finally, we take the reciprocal:

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ={(\frac{∂(u,v,w)}{∂(x,y,z)})}^{-1} \\  & =\frac{1}{24}\end{aligned}
$$