# Jacobian review

Basis 1356; all ten original complete banks. Values normalize standard LaTeX. Original raw evidence retained in source.json.

## Original q-38078

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}2u\operatorname{cos}⁡v \\ 3u\operatorname{sin}⁡v\end{aligned}].
$$

Original choices:
- $-3u$
- $2u$
- $\frac{2}{3}u$
- $-\frac{3}{2}u$
- $6u$

Original worked solution:
Given a transformation 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y)}{∂(u,v)},$ is given by

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}|.\end{aligned}
$$

Here, we have $x(u,v)=2u\operatorname{cos}⁡v$ and $y(u,v)=3u\operatorname{sin}⁡v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2\operatorname{cos}⁡v & \,\frac{∂x}{∂v} & =-2u\operatorname{sin}⁡v \\ \frac{∂y}{∂u} & =3\operatorname{sin}⁡v & \,\frac{∂y}{∂v} & =3u\operatorname{cos}⁡v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2\operatorname{cos}⁡v & -2u\operatorname{sin}⁡v \\ 3\operatorname{sin}⁡v & 3u\operatorname{cos}⁡v\end{aligned}| \\  & =2\operatorname{cos}⁡v\cdot 3u\operatorname{cos}⁡v-(-2u\operatorname{sin}⁡v)\cdot 3\operatorname{sin}⁡v \\  & =6u({cos}^{2}⁡v+{cos}^{2}⁡v) \\  & =6u.\end{aligned}
$$

## Generated easy — polar
Author metadata: profile `observed_polar`, parameters `{'a': 2, 'b': 3}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}2 u \cos{\left(v \right)}\\3 u \sin{\left(v \right)}\end{bmatrix}.
$$

- $\frac{2 u}{3}$
- $2 u$
- $- 3 u$
- $6 u$ **correct**
- $- \frac{3 u}{2}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=2 u \cos{\left(v \right)}$ and $y(u,v)=3 u \sin{\left(v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=2 \cos{\left(v \right)}&\quad \frac{\partial x}{\partial v}&=- 2 u \sin{\left(v \right)}\\\frac{\partial y}{\partial u}&=3 \sin{\left(v \right)}&\quad \frac{\partial y}{\partial v}&=3 u \cos{\left(v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}2 \cos{\left(v \right)}&- 2 u \sin{\left(v \right)}\\3 \sin{\left(v \right)}&3 u \cos{\left(v \right)}\end{matrix}\right|\\&=\left(2 \cos{\left(v \right)}\right)\cdot\left(3 u \cos{\left(v \right)}\right)-\left(- 2 u \sin{\left(v \right)}\right)\cdot\left(3 \sin{\left(v \right)}\right)\\&=6 u\left(\cos^2 v+\sin^2 v\right)\\&=6 u.\end{aligned}
$$


## Original q-160381

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}3u+2v \\ u+3v\end{aligned}].
$$

Original choices:
- $u+2v$
- $11$
- $7$
- $9u$
- $3u-v$

Original worked solution:
Given a transformation 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y)}{∂(u,v)},$ is given by

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}|.\end{aligned}
$$

Here, we have $x(u,v)=3u+2v$ and $y(u,v)=u+3v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =3 & \,\frac{∂x}{∂v} & =2 \\ \frac{∂y}{∂u} & =1 & \,\frac{∂y}{∂v} & =3\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}3 & 2 \\ 1 & 3\end{aligned}| \\  & =3\cdot 3-1\cdot 2 \\  & =9-2 \\  & =7.\end{aligned}
$$

## Generated easy — linear
Author metadata: profile `observed_linear`, parameters `{'a': 3, 'b': 2, 'c': 1, 'd': 3}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}3 u + 2 v\\u + 3 v\end{bmatrix}.
$$

- $7$ **correct**
- $11$
- $u + 2 v$
- $3 u - v$
- $9 u$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=3 u + 2 v$ and $y(u,v)=u + 3 v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=3&\quad \frac{\partial x}{\partial v}&=2\\\frac{\partial y}{\partial u}&=1&\quad \frac{\partial y}{\partial v}&=3\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}3&2\\1&3\end{matrix}\right|\\&=\left(3\right)\cdot\left(3\right)-\left(2\right)\cdot\left(1\right)\\&=9-2\\&=7.\end{aligned}
$$


## Original q-160404

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}3u-5v \\ \operatorname{ln}⁡(u+v)\end{aligned}].
$$

Original choices:
- $\frac{8}{u+v}$
- $\frac{u}{u+v}$
- $\frac{v}{u+v}$
- $\frac{6}{u+v}$
- $u+v$

Original worked solution:
Given a transformation 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y)}{∂(u,v)},$ is given by

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}|.\end{aligned}
$$

Here, we have $x(u,v)=3u-5v$ and $y(u,v)=\operatorname{ln}⁡(u+v).$  

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =3 & \,\frac{∂x}{∂v} & =-5 \\ \frac{∂y}{∂u} & =\frac{1}{u+v} & \,\frac{∂y}{∂v} & =\frac{1}{u+v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}3 & -5 \\ \frac{1}{u+v} & \frac{1}{u+v}\end{aligned}| \\  & =3\cdot (\frac{1}{u+v})-(-5)\cdot (\frac{1}{u+v}) \\  & =\frac{8}{u+v}.\end{aligned}
$$

## Generated easy — linear_log
Author metadata: profile `observed_linear_log`, parameters `{'a': 3, 'b': -5}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}3 u - 5 v\\\log{\left(u + v \right)}\end{bmatrix}.
$$

- $\frac{v}{u + v}$
- $\frac{u}{u + v}$
- $\frac{8}{u + v}$ **correct**
- $u + v$
- $\frac{6}{u + v}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=3 u - 5 v$ and $y(u,v)=\log{\left(u + v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=3&\quad \frac{\partial x}{\partial v}&=-5\\\frac{\partial y}{\partial u}&=\frac{1}{u + v}&\quad \frac{\partial y}{\partial v}&=\frac{1}{u + v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}3&-5\\\frac{1}{u + v}&\frac{1}{u + v}\end{matrix}\right|\\&=\left(3\right)\cdot\left(\frac{1}{u + v}\right)-\left(-5\right)\cdot\left(\frac{1}{u + v}\right)\\&=\frac{8}{u + v}.\end{aligned}
$$


## Original q-38241

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\operatorname{cos}⁡v\operatorname{tan}⁡(\frac{u}{2}) \\ \operatorname{sin}⁡v\end{aligned}].
$$

Original choices:
- $\frac{{cos}^{2}⁡v}{2{cos}^{2}⁡(\frac{u}{2})}$
- $\frac{2{cos}^{2}⁡v}{{cos}^{2}⁡(\frac{u}{2})}$
- $\frac{{cos}^{2}⁡v}{{cos}^{2}⁡u}$
- $\frac{{cos}^{2}⁡v}{{cos}^{2}⁡(\frac{u}{2})}-\operatorname{cos}⁡v$
- $\frac{2{cos}^{2}⁡v}{{cos}^{2}⁡(\frac{u}{2})}+\operatorname{cos}⁡v$

Original worked solution:
Given a transformation 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y)}{∂(u,v)},$ is given by

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}|.\end{aligned}
$$

Here, we have $x(u,v)=\operatorname{cos}⁡v\operatorname{tan}⁡(\frac{u}{2})$ and $y(u,v)=\operatorname{sin}⁡v.$

First, we find the partial derivatives: 

$$
\begin{aligned}\frac{∂x}{∂u} & =\frac{\operatorname{cos}⁡v}{2{cos}^{2}⁡(\frac{u}{2})} & \,\frac{∂x}{∂v} & =-\operatorname{sin}⁡v\operatorname{tan}⁡(\frac{u}{2}) \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =\operatorname{cos}⁡v\end{aligned}
$$

 

Therefore, the corresponding Jacobian determinant is 

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}\frac{\operatorname{cos}⁡v}{2{cos}^{2}⁡(u/2)} & -\operatorname{sin}⁡v\operatorname{tan}⁡(\frac{u}{2}) \\ \,0\, & \,\text{ }\text{ }\operatorname{cos}⁡v\end{aligned}| \\  & =\frac{{cos}^{2}⁡v}{2{cos}^{2}⁡(\frac{u}{2})}.\end{aligned}
$$

## Generated easy — tan_product
Author metadata: profile `observed_tan_product`, parameters `{'k': 2}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}\cos{\left(v \right)} \tan{\left(\frac{u}{2} \right)}\\\sin{\left(v \right)}\end{bmatrix}.
$$

- $\frac{\cos^{2}{\left(v \right)}}{\cos^{2}{\left(u \right)}}$
- $\frac{2 \cos^{2}{\left(v \right)}}{\cos^{2}{\left(\frac{u}{2} \right)}}$
- $\frac{\cos^{2}{\left(v \right)}}{2 \cos^{2}{\left(\frac{u}{2} \right)}}$ **correct**
- $\cos{\left(v \right)} + \frac{2 \cos^{2}{\left(v \right)}}{\cos^{2}{\left(\frac{u}{2} \right)}}$
- $- \cos{\left(v \right)} + \frac{\cos^{2}{\left(v \right)}}{\cos^{2}{\left(\frac{u}{2} \right)}}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=\cos{\left(v \right)} \tan{\left(\frac{u}{2} \right)}$ and $y(u,v)=\sin{\left(v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=\left(\frac{\tan^{2}{\left(\frac{u}{2} \right)}}{2} + \frac{1}{2}\right) \cos{\left(v \right)}&\quad \frac{\partial x}{\partial v}&=- \sin{\left(v \right)} \tan{\left(\frac{u}{2} \right)}\\\frac{\partial y}{\partial u}&=0&\quad \frac{\partial y}{\partial v}&=\cos{\left(v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}\left(\frac{\tan^{2}{\left(\frac{u}{2} \right)}}{2} + \frac{1}{2}\right) \cos{\left(v \right)}&- \sin{\left(v \right)} \tan{\left(\frac{u}{2} \right)}\\0&\cos{\left(v \right)}\end{matrix}\right|\\&=\frac{\cos^{2}{\left(v \right)}}{2 \cos^{2}{\left(\frac{u}{2} \right)}}.\end{aligned}
$$


## Original q-81264

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{u}^{2}-{v}^{2} \\ {u}^{2}+{v}^{2}\end{aligned}].
$$

Original choices:
- $2({u}^{2}-{v}^{2})$
- ${u}^{2}-uv+{v}^{2}$
- $8uv$
- $4(u-v)$
- $0$

Original worked solution:
Given a transformation 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y)}{∂(u,v)},$ is given by

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}|.\end{aligned}
$$

 

Here, we have $x(u,v)={u}^{2}-{v}^{2}$ and $y(u,v)={u}^{2}+{v}^{2}.$  

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2u & \,\frac{∂x}{∂v} & =-2v \\ \frac{∂y}{∂u} & =2u & \,\frac{∂y}{∂v} & =2v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2u & -2v \\ 2u & 2v\end{aligned}| \\  & =2u\cdot 2v-(-2v)\cdot 2u \\  & =4uv+4uv \\  & =8uv.\end{aligned}
$$

## Generated easy — quadratic
Author metadata: profile `observed_quadratic`, parameters `{'a': 1, 'b': 1}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}u^{2} - v^{2}\\u^{2} + v^{2}\end{bmatrix}.
$$

- $8 u v$ **correct**
- $u^{2} - u v + v^{2}$
- $2 u^{2} - 2 v^{2}$
- $0$
- $4 u - 4 v$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=u^{2} - v^{2}$ and $y(u,v)=u^{2} + v^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=2 u&\quad \frac{\partial x}{\partial v}&=- 2 v\\\frac{\partial y}{\partial u}&=2 u&\quad \frac{\partial y}{\partial v}&=2 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}2 u&- 2 v\\2 u&2 v\end{matrix}\right|\\&=\left(2 u\right)\cdot\left(2 v\right)-\left(- 2 v\right)\cdot\left(2 u\right)\\&=4 u v+4 u v\\&=8 u v.\end{aligned}
$$


## Original q-160403

Find the Jacobian determinant of the transformation $T([\begin{aligned}u \\ v\end{aligned}])=[\begin{aligned}{e}^{u+v} \\ \operatorname{ln}⁡(uv)\end{aligned}].$

Original choices:
- $0$
- ${e}^{u+v}$
- $1$
- $\frac{{e}^{u+v}(u-v)}{vu}$
- $\frac{{e}^{u+v}}{vu}$

Original worked solution:
Given a transformation 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y)}{∂(u,v)},$ is given by

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}|.\end{aligned}
$$

Here, we have $x(u,v)={e}^{u+v}$ and $y(u,v)=\operatorname{ln}⁡(uv).$  

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & ={e}^{u+v} & \,\frac{∂x}{∂v} & ={e}^{u+v} \\ \frac{∂y}{∂u} & =\frac{1}{u} & \,\frac{∂y}{∂v} & =\frac{1}{v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}{e}^{u+v} & {e}^{u+v} \\ \frac{1}{u} & \frac{1}{v}\end{aligned}| \\  & ={e}^{u+v}\cdot (\frac{1}{v})-{e}^{u+v}\cdot (\frac{1}{u}) \\  & =\frac{{e}^{u+v}}{v}-\frac{{e}^{u+v}}{u} \\  & =\frac{{e}^{u+v}(u-v)}{vu}.\end{aligned}
$$

## Generated moderate — exp_log
Author metadata: profile `observed_exp_log`, parameters `{'a': 1, 'b': 1}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}e^{u + v}\\\log{\left(u v \right)}\end{bmatrix}.$

- $1$
- $e^{u + v}$
- $0$
- $\frac{e^{u + v}}{u v}$
- $\frac{\left(u - v\right) e^{u} e^{v}}{u v}$ **correct**

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=e^{u + v}$ and $y(u,v)=\log{\left(u v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=e^{u + v}&\quad \frac{\partial x}{\partial v}&=e^{u + v}\\\frac{\partial y}{\partial u}&=\frac{1}{u}&\quad \frac{\partial y}{\partial v}&=\frac{1}{v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}e^{u + v}&e^{u + v}\\\frac{1}{u}&\frac{1}{v}\end{matrix}\right|\\&=\left(e^{u + v}\right)\cdot\left(\frac{1}{v}\right)-\left(e^{u + v}\right)\cdot\left(\frac{1}{u}\right)\\&=\frac{e^{u + v}}{v}-\frac{e^{u + v}}{u}\\&=\frac{\left(u - v\right) e^{u} e^{v}}{u v}.\end{aligned}
$$


## Original q-160405

Find the Jacobian determinant of the transformation $T([\begin{aligned}u \\ v\end{aligned}])=[\begin{aligned}\operatorname{cos}⁡(u+v) \\ 4u+6v\end{aligned}].$

Original choices:
- $4\operatorname{sin}⁡(u-v)$
- $\operatorname{cos}⁡(u+v)$
- $-\operatorname{cos}⁡(u-v)$
- $-\operatorname{sin}⁡(u+v)$
- $-2\operatorname{sin}⁡(u+v)$

Original worked solution:
Given a transformation 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y)}{∂(u,v)},$ is given by

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}|.\end{aligned}
$$

Here, we have $x=\operatorname{cos}⁡(u+v)$ and $y=4u+6v.$ 

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =-\operatorname{sin}⁡(u+v) & \,\frac{∂x}{∂v} & =-\operatorname{sin}⁡(u+v) \\ \frac{∂y}{∂u} & =4 & \,\frac{∂y}{∂v} & =6\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}-\operatorname{sin}⁡(u+v) & -\operatorname{sin}⁡(u+v) \\ \,\text{ }4\, & \,\text{ }6\end{aligned}| \\  & =-\operatorname{sin}⁡(u+v)\cdot 6-(-\operatorname{sin}⁡(u+v))\cdot 4 \\  & =-2\operatorname{sin}⁡(u+v).\end{aligned}
$$

## Generated moderate — cos_linear
Author metadata: profile `observed_cos_linear`, parameters `{'a': 4, 'b': 6}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}\cos{\left(u + v \right)}\\4 u + 6 v\end{bmatrix}.$

- $- \cos{\left(u - v \right)}$
- $\cos{\left(u + v \right)}$
- $4 \sin{\left(u - v \right)}$
- $- 2 \sin{\left(u + v \right)}$ **correct**
- $- \sin{\left(u + v \right)}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=\cos{\left(u + v \right)}$ and $y=4 u + 6 v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=- \sin{\left(u + v \right)}&\quad \frac{\partial x}{\partial v}&=- \sin{\left(u + v \right)}\\\frac{\partial y}{\partial u}&=4&\quad \frac{\partial y}{\partial v}&=6\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}- \sin{\left(u + v \right)}&- \sin{\left(u + v \right)}\\4&6\end{matrix}\right|\\&=\left(- \sin{\left(u + v \right)}\right)\cdot\left(6\right)-\left(- \sin{\left(u + v \right)}\right)\cdot\left(4\right)\\&=- 2 \sin{\left(u + v \right)}.\end{aligned}
$$


## Original q-81252

Find the Jacobian determinant of the transformation $T([\begin{aligned}u \\ v\end{aligned}])=[\begin{aligned}\operatorname{sin}⁡(u+v) \\ \operatorname{cos}⁡(u-v)\end{aligned}].$

Original choices:
- $\operatorname{cos}⁡(u+v)\operatorname{sin}⁡(u-v)$
- $2\operatorname{cos}⁡(u+v)\operatorname{sin}⁡(u-v)$
- $\operatorname{cos}⁡(u-v)\operatorname{sin}⁡(u+v)$
- $2\operatorname{cos}⁡(u-v)\operatorname{sin}⁡(u+v)$
- ${cos}^{2}⁡(u+v){sin}^{2}⁡(u-v)$

Original worked solution:
Given a transformation 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y)}{∂(u,v)},$ is given by

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}|.\end{aligned}
$$

 

Here, we have $x=\operatorname{sin}⁡(u+v)$ and $y=\operatorname{cos}⁡(u-v).$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =\operatorname{cos}⁡(u+v) & \,\frac{∂x}{∂v} & =\operatorname{cos}⁡(u+v) \\ \frac{∂y}{∂u} & =-\operatorname{sin}⁡(u-v) & \,\frac{∂y}{∂v} & =\operatorname{sin}⁡(u-v)\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}\operatorname{cos}⁡(u+v) & \operatorname{cos}⁡(u+v) \\ -\operatorname{sin}⁡(u-v)\, & \operatorname{sin}⁡(u-v)\end{aligned}| \\  & =\operatorname{cos}⁡(u+v)\cdot \operatorname{sin}⁡(u-v)-\operatorname{cos}⁡(u+v)\cdot (-\operatorname{sin}⁡(u-v)) \\  & =2\operatorname{cos}⁡(u+v)\operatorname{sin}⁡(u-v).\end{aligned}
$$

## Generated moderate — trig_pair
Author metadata: profile `observed_trig_pair`, parameters `{'a': 1, 'b': 1}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}\sin{\left(u + v \right)}\\\cos{\left(u - v \right)}\end{bmatrix}.$

- $\sin{\left(u + v \right)} \cos{\left(u - v \right)}$
- $2 \sin{\left(u - v \right)} \cos{\left(u + v \right)}$ **correct**
- $\sin{\left(u - v \right)} \cos{\left(u + v \right)}$
- $\sin^{2}{\left(u - v \right)} \cos^{2}{\left(u + v \right)}$
- $2 \sin{\left(u + v \right)} \cos{\left(u - v \right)}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=\sin{\left(u + v \right)}$ and $y=\cos{\left(u - v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=\cos{\left(u + v \right)}&\quad \frac{\partial x}{\partial v}&=\cos{\left(u + v \right)}\\\frac{\partial y}{\partial u}&=- \sin{\left(u - v \right)}&\quad \frac{\partial y}{\partial v}&=\sin{\left(u - v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}\cos{\left(u + v \right)}&\cos{\left(u + v \right)}\\- \sin{\left(u - v \right)}&\sin{\left(u - v \right)}\end{matrix}\right|\\&=\left(\cos{\left(u + v \right)}\right)\cdot\left(\sin{\left(u - v \right)}\right)-\left(\cos{\left(u + v \right)}\right)\cdot\left(- \sin{\left(u - v \right)}\right)\\&=2 \sin{\left(u - v \right)} \cos{\left(u + v \right)}.\end{aligned}
$$


## Original q-160406

Find the Jacobian determinant of the transformation $T([\begin{aligned}u \\ v\end{aligned}])=[\begin{aligned}{e}^{u+v} \\ {u}^{2}+{v}^{2}\end{aligned}].$

Original choices:
- ${e}^{u+v}(u+v)$
- $2{e}^{u+v}(u+v)$
- ${e}^{u+v}(uv)$
- $2{e}^{u+v}(v-u)$
- $2{e}^{u+v}(u-v)$

Original worked solution:
Given a transformation 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y)}{∂(u,v)},$ is given by

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}|.\end{aligned}
$$

Here, we have $x={e}^{u+v}$ and $y={u}^{2}+{v}^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & ={e}^{u+v} & \,\frac{∂x}{∂v} & ={e}^{u+v} \\ \frac{∂y}{∂u} & =2u & \,\frac{∂y}{∂v} & =2v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}{e}^{u+v} & {e}^{u+v} \\ \,\text{ }2u\, & \,\text{ }2v\end{aligned}| \\  & ={e}^{u+v}\cdot 2v-{e}^{u+v}\cdot 2u \\  & =2{e}^{u+v}(v-u).\end{aligned}
$$

## Generated moderate — exp_quadratic
Author metadata: profile `observed_exp_quadratic`, parameters `{'a': 1, 'b': 1}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}e^{u + v}\\u^{2} + v^{2}\end{bmatrix}.$

- $u v e^{u + v}$
- $2 \left(u + v\right) e^{u + v}$
- $\left(u + v\right) e^{u + v}$
- $2 \left(u - v\right) e^{u} e^{v}$
- $- 2 \left(u - v\right) e^{u} e^{v}$ **correct**

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=e^{u + v}$ and $y=u^{2} + v^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=e^{u + v}&\quad \frac{\partial x}{\partial v}&=e^{u + v}\\\frac{\partial y}{\partial u}&=2 u&\quad \frac{\partial y}{\partial v}&=2 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}e^{u + v}&e^{u + v}\\2 u&2 v\end{matrix}\right|\\&=\left(e^{u + v}\right)\cdot\left(2 v\right)-\left(e^{u + v}\right)\cdot\left(2 u\right)\\&=- 2 \left(u - v\right) e^{u} e^{v}.\end{aligned}
$$


## Original q-38244

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u \\ v\end{bmatrix}) = \begin{bmatrix}\ln (2u + v) \\ uv\end{bmatrix}$.

Original choices:
- $\frac{u - v}{2u + v}$
- $\frac{u + v}{2u + v}$
- $\frac{2v - u}{2u + v}$
- $1$
- $\frac{2u - v}{2u + v}$

Original worked solution:
Absent in captured source.

## Generated moderate — log_product
Author metadata: profile `observed_log_product`, parameters `{'a': 2, 'b': 1}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}\log{\left(2 u + v \right)}\\u v\end{bmatrix}.$

- $\frac{- u + 2 v}{2 u + v}$
- $\frac{u + v}{2 u + v}$
- $\frac{u - v}{2 u + v}$
- $\frac{2 u - v}{2 u + v}$ **correct**
- $1$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=\log{\left(2 u + v \right)}$ and $y=u v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=\frac{2}{2 u + v}&\quad \frac{\partial x}{\partial v}&=\frac{1}{2 u + v}\\\frac{\partial y}{\partial u}&=v&\quad \frac{\partial y}{\partial v}&=u\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}\frac{2}{2 u + v}&\frac{1}{2 u + v}\\v&u\end{matrix}\right|\\&=\left(\frac{2}{2 u + v}\right)\cdot\left(u\right)-\left(\frac{1}{2 u + v}\right)\cdot\left(v\right)\\&=\frac{2 u - v}{2 u + v}.\end{aligned}
$$


# Clearly labeled generated variants

## Generated easy — polar
Author metadata: profile `observed_polar`, parameters `{'a': 5, 'b': 4}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u \cos{\left(v \right)}\\4 u \sin{\left(v \right)}\end{bmatrix}.
$$

- $- 4 u$
- $\frac{5 u}{4}$
- $5 u$
- $- \frac{4 u}{5}$
- $20 u$ **correct**

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u \cos{\left(v \right)}$ and $y(u,v)=4 u \sin{\left(v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 \cos{\left(v \right)}&\quad \frac{\partial x}{\partial v}&=- 5 u \sin{\left(v \right)}\\\frac{\partial y}{\partial u}&=4 \sin{\left(v \right)}&\quad \frac{\partial y}{\partial v}&=4 u \cos{\left(v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 \cos{\left(v \right)}&- 5 u \sin{\left(v \right)}\\4 \sin{\left(v \right)}&4 u \cos{\left(v \right)}\end{matrix}\right|\\&=\left(5 \cos{\left(v \right)}\right)\cdot\left(4 u \cos{\left(v \right)}\right)-\left(- 5 u \sin{\left(v \right)}\right)\cdot\left(4 \sin{\left(v \right)}\right)\\&=20 u\left(\cos^2 v+\sin^2 v\right)\\&=20 u.\end{aligned}
$$

## Generated easy — polar
Author metadata: profile `observed_polar`, parameters `{'a': 3, 'b': 5}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}3 u \cos{\left(v \right)}\\5 u \sin{\left(v \right)}\end{bmatrix}.
$$

- $- \frac{5 u}{3}$
- $\frac{3 u}{5}$
- $3 u$
- $- 5 u$
- $15 u$ **correct**

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=3 u \cos{\left(v \right)}$ and $y(u,v)=5 u \sin{\left(v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=3 \cos{\left(v \right)}&\quad \frac{\partial x}{\partial v}&=- 3 u \sin{\left(v \right)}\\\frac{\partial y}{\partial u}&=5 \sin{\left(v \right)}&\quad \frac{\partial y}{\partial v}&=5 u \cos{\left(v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}3 \cos{\left(v \right)}&- 3 u \sin{\left(v \right)}\\5 \sin{\left(v \right)}&5 u \cos{\left(v \right)}\end{matrix}\right|\\&=\left(3 \cos{\left(v \right)}\right)\cdot\left(5 u \cos{\left(v \right)}\right)-\left(- 3 u \sin{\left(v \right)}\right)\cdot\left(5 \sin{\left(v \right)}\right)\\&=15 u\left(\cos^2 v+\sin^2 v\right)\\&=15 u.\end{aligned}
$$

## Generated easy — linear
Author metadata: profile `observed_linear`, parameters `{'a': 5, 'b': 4, 'c': 3, 'd': 3}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u + 4 v\\3 u + 3 v\end{bmatrix}.
$$

- $3 u + 4 v$
- $3$ **correct**
- $27$
- $15 u$
- $5 u - 3 v$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u + 4 v$ and $y(u,v)=3 u + 3 v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5&\quad \frac{\partial x}{\partial v}&=4\\\frac{\partial y}{\partial u}&=3&\quad \frac{\partial y}{\partial v}&=3\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5&4\\3&3\end{matrix}\right|\\&=\left(5\right)\cdot\left(3\right)-\left(4\right)\cdot\left(3\right)\\&=15-12\\&=3.\end{aligned}
$$

## Generated easy — linear
Author metadata: profile `observed_linear`, parameters `{'a': 5, 'b': 1, 'c': 3, 'd': 5}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u + v\\3 u + 5 v\end{bmatrix}.
$$

- $25 u$
- $22$ **correct**
- $28$
- $3 u + v$
- $5 u - 3 v$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u + v$ and $y(u,v)=3 u + 5 v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5&\quad \frac{\partial x}{\partial v}&=1\\\frac{\partial y}{\partial u}&=3&\quad \frac{\partial y}{\partial v}&=5\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5&1\\3&5\end{matrix}\right|\\&=\left(5\right)\cdot\left(5\right)-\left(1\right)\cdot\left(3\right)\\&=25-3\\&=22.\end{aligned}
$$

## Generated easy — linear_log
Author metadata: profile `observed_linear_log`, parameters `{'a': 6, 'b': -5}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}6 u - 5 v\\\log{\left(u + v \right)}\end{bmatrix}.
$$

- $\frac{11}{u + v}$ **correct**
- $\frac{v}{u + v}$
- $\frac{u}{u + v}$
- $\frac{12}{u + v}$
- $u + v$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=6 u - 5 v$ and $y(u,v)=\log{\left(u + v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=6&\quad \frac{\partial x}{\partial v}&=-5\\\frac{\partial y}{\partial u}&=\frac{1}{u + v}&\quad \frac{\partial y}{\partial v}&=\frac{1}{u + v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}6&-5\\\frac{1}{u + v}&\frac{1}{u + v}\end{matrix}\right|\\&=\left(6\right)\cdot\left(\frac{1}{u + v}\right)-\left(-5\right)\cdot\left(\frac{1}{u + v}\right)\\&=\frac{11}{u + v}.\end{aligned}
$$

## Generated easy — linear_log
Author metadata: profile `observed_linear_log`, parameters `{'a': 6, 'b': -2}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}6 u - 2 v\\\log{\left(u + v \right)}\end{bmatrix}.
$$

- $\frac{12}{u + v}$
- $\frac{v}{u + v}$
- $\frac{u}{u + v}$
- $\frac{8}{u + v}$ **correct**
- $u + v$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=6 u - 2 v$ and $y(u,v)=\log{\left(u + v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=6&\quad \frac{\partial x}{\partial v}&=-2\\\frac{\partial y}{\partial u}&=\frac{1}{u + v}&\quad \frac{\partial y}{\partial v}&=\frac{1}{u + v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}6&-2\\\frac{1}{u + v}&\frac{1}{u + v}\end{matrix}\right|\\&=\left(6\right)\cdot\left(\frac{1}{u + v}\right)-\left(-2\right)\cdot\left(\frac{1}{u + v}\right)\\&=\frac{8}{u + v}.\end{aligned}
$$

## Generated easy — tan_product
Author metadata: profile `observed_tan_product`, parameters `{'k': 5}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}\cos{\left(v \right)} \tan{\left(\frac{u}{5} \right)}\\\sin{\left(v \right)}\end{bmatrix}.
$$

- $\frac{\cos^{2}{\left(v \right)}}{5 \cos^{2}{\left(\frac{u}{5} \right)}}$ **correct**
- $\frac{\cos^{2}{\left(v \right)}}{\cos^{2}{\left(u \right)}}$
- $\frac{5 \cos^{2}{\left(v \right)}}{\cos^{2}{\left(\frac{u}{5} \right)}}$
- $- \cos{\left(v \right)} + \frac{\cos^{2}{\left(v \right)}}{\cos^{2}{\left(\frac{u}{5} \right)}}$
- $\cos{\left(v \right)} + \frac{5 \cos^{2}{\left(v \right)}}{\cos^{2}{\left(\frac{u}{5} \right)}}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=\cos{\left(v \right)} \tan{\left(\frac{u}{5} \right)}$ and $y(u,v)=\sin{\left(v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=\left(\frac{\tan^{2}{\left(\frac{u}{5} \right)}}{5} + \frac{1}{5}\right) \cos{\left(v \right)}&\quad \frac{\partial x}{\partial v}&=- \sin{\left(v \right)} \tan{\left(\frac{u}{5} \right)}\\\frac{\partial y}{\partial u}&=0&\quad \frac{\partial y}{\partial v}&=\cos{\left(v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}\left(\frac{\tan^{2}{\left(\frac{u}{5} \right)}}{5} + \frac{1}{5}\right) \cos{\left(v \right)}&- \sin{\left(v \right)} \tan{\left(\frac{u}{5} \right)}\\0&\cos{\left(v \right)}\end{matrix}\right|\\&=\frac{\cos^{2}{\left(v \right)}}{5 \cos^{2}{\left(\frac{u}{5} \right)}}.\end{aligned}
$$

## Generated easy — tan_product
Author metadata: profile `observed_tan_product`, parameters `{'k': 2}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}\cos{\left(v \right)} \tan{\left(\frac{u}{2} \right)}\\\sin{\left(v \right)}\end{bmatrix}.
$$

- $- \cos{\left(v \right)} + \frac{\cos^{2}{\left(v \right)}}{\cos^{2}{\left(\frac{u}{2} \right)}}$
- $\frac{\cos^{2}{\left(v \right)}}{\cos^{2}{\left(u \right)}}$
- $\frac{2 \cos^{2}{\left(v \right)}}{\cos^{2}{\left(\frac{u}{2} \right)}}$
- $\frac{\cos^{2}{\left(v \right)}}{2 \cos^{2}{\left(\frac{u}{2} \right)}}$ **correct**
- $\cos{\left(v \right)} + \frac{2 \cos^{2}{\left(v \right)}}{\cos^{2}{\left(\frac{u}{2} \right)}}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=\cos{\left(v \right)} \tan{\left(\frac{u}{2} \right)}$ and $y(u,v)=\sin{\left(v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=\left(\frac{\tan^{2}{\left(\frac{u}{2} \right)}}{2} + \frac{1}{2}\right) \cos{\left(v \right)}&\quad \frac{\partial x}{\partial v}&=- \sin{\left(v \right)} \tan{\left(\frac{u}{2} \right)}\\\frac{\partial y}{\partial u}&=0&\quad \frac{\partial y}{\partial v}&=\cos{\left(v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}\left(\frac{\tan^{2}{\left(\frac{u}{2} \right)}}{2} + \frac{1}{2}\right) \cos{\left(v \right)}&- \sin{\left(v \right)} \tan{\left(\frac{u}{2} \right)}\\0&\cos{\left(v \right)}\end{matrix}\right|\\&=\frac{\cos^{2}{\left(v \right)}}{2 \cos^{2}{\left(\frac{u}{2} \right)}}.\end{aligned}
$$

## Generated easy — quadratic
Author metadata: profile `observed_quadratic`, parameters `{'a': 5, 'b': 4}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u^{2} - 4 v^{2}\\5 u^{2} + 4 v^{2}\end{bmatrix}.
$$

- $10 u^{2} - 8 v^{2}$
- $160 u v$ **correct**
- $5 u^{2} - 20 u v + 4 v^{2}$
- $20 u - 16 v$
- $0$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u^{2} - 4 v^{2}$ and $y(u,v)=5 u^{2} + 4 v^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=10 u&\quad \frac{\partial x}{\partial v}&=- 8 v\\\frac{\partial y}{\partial u}&=10 u&\quad \frac{\partial y}{\partial v}&=8 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}10 u&- 8 v\\10 u&8 v\end{matrix}\right|\\&=\left(10 u\right)\cdot\left(8 v\right)-\left(- 8 v\right)\cdot\left(10 u\right)\\&=80 u v+80 u v\\&=160 u v.\end{aligned}
$$

## Generated easy — quadratic
Author metadata: profile `observed_quadratic`, parameters `{'a': 5, 'b': 1}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u^{2} - v^{2}\\5 u^{2} + v^{2}\end{bmatrix}.
$$

- $20 u - 4 v$
- $40 u v$ **correct**
- $5 u^{2} - 5 u v + v^{2}$
- $10 u^{2} - 2 v^{2}$
- $0$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u^{2} - v^{2}$ and $y(u,v)=5 u^{2} + v^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=10 u&\quad \frac{\partial x}{\partial v}&=- 2 v\\\frac{\partial y}{\partial u}&=10 u&\quad \frac{\partial y}{\partial v}&=2 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}10 u&- 2 v\\10 u&2 v\end{matrix}\right|\\&=\left(10 u\right)\cdot\left(2 v\right)-\left(- 2 v\right)\cdot\left(10 u\right)\\&=20 u v+20 u v\\&=40 u v.\end{aligned}
$$

## Generated moderate — exp_log
Author metadata: profile `observed_exp_log`, parameters `{'a': 5, 'b': 4}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}e^{5 u + 4 v}\\\log{\left(u v \right)}\end{bmatrix}.$

- $0$
- $1$
- $e^{5 u + 4 v}$
- $\frac{\left(5 u - 4 v\right) e^{5 u} e^{4 v}}{u v}$ **correct**
- $\frac{e^{5 u + 4 v}}{u v}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=e^{5 u + 4 v}$ and $y(u,v)=\log{\left(u v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 e^{5 u + 4 v}&\quad \frac{\partial x}{\partial v}&=4 e^{5 u + 4 v}\\\frac{\partial y}{\partial u}&=\frac{1}{u}&\quad \frac{\partial y}{\partial v}&=\frac{1}{v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 e^{5 u + 4 v}&4 e^{5 u + 4 v}\\\frac{1}{u}&\frac{1}{v}\end{matrix}\right|\\&=\left(5 e^{5 u + 4 v}\right)\cdot\left(\frac{1}{v}\right)-\left(4 e^{5 u + 4 v}\right)\cdot\left(\frac{1}{u}\right)\\&=\frac{5 e^{5 u + 4 v}}{v}-\frac{4 e^{5 u + 4 v}}{u}\\&=\frac{\left(5 u - 4 v\right) e^{5 u} e^{4 v}}{u v}.\end{aligned}
$$

## Generated moderate — exp_log
Author metadata: profile `observed_exp_log`, parameters `{'a': 5, 'b': 1}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}e^{5 u + v}\\\log{\left(u v \right)}\end{bmatrix}.$

- $\frac{\left(5 u - v\right) e^{5 u} e^{v}}{u v}$ **correct**
- $1$
- $e^{5 u + v}$
- $0$
- $\frac{e^{5 u + v}}{u v}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=e^{5 u + v}$ and $y(u,v)=\log{\left(u v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 e^{5 u + v}&\quad \frac{\partial x}{\partial v}&=e^{5 u + v}\\\frac{\partial y}{\partial u}&=\frac{1}{u}&\quad \frac{\partial y}{\partial v}&=\frac{1}{v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 e^{5 u + v}&e^{5 u + v}\\\frac{1}{u}&\frac{1}{v}\end{matrix}\right|\\&=\left(5 e^{5 u + v}\right)\cdot\left(\frac{1}{v}\right)-\left(e^{5 u + v}\right)\cdot\left(\frac{1}{u}\right)\\&=\frac{5 e^{5 u + v}}{v}-\frac{e^{5 u + v}}{u}\\&=\frac{\left(5 u - v\right) e^{5 u} e^{v}}{u v}.\end{aligned}
$$

## Generated moderate — cos_linear
Author metadata: profile `observed_cos_linear`, parameters `{'a': 6, 'b': 5}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}\cos{\left(u + v \right)}\\6 u + 5 v\end{bmatrix}.$

- $6 \sin{\left(u - v \right)}$
- $- \cos{\left(u - v \right)}$
- $\cos{\left(u + v \right)}$
- $- \sin{\left(u + v \right)}$
- $\sin{\left(u + v \right)}$ **correct**

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=\cos{\left(u + v \right)}$ and $y=6 u + 5 v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=- \sin{\left(u + v \right)}&\quad \frac{\partial x}{\partial v}&=- \sin{\left(u + v \right)}\\\frac{\partial y}{\partial u}&=6&\quad \frac{\partial y}{\partial v}&=5\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}- \sin{\left(u + v \right)}&- \sin{\left(u + v \right)}\\6&5\end{matrix}\right|\\&=\left(- \sin{\left(u + v \right)}\right)\cdot\left(5\right)-\left(- \sin{\left(u + v \right)}\right)\cdot\left(6\right)\\&=\sin{\left(u + v \right)}.\end{aligned}
$$

## Generated moderate — cos_linear
Author metadata: profile `observed_cos_linear`, parameters `{'a': 6, 'b': 2}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}\cos{\left(u + v \right)}\\6 u + 2 v\end{bmatrix}.$

- $- \sin{\left(u + v \right)}$
- $- \cos{\left(u - v \right)}$
- $\cos{\left(u + v \right)}$
- $6 \sin{\left(u - v \right)}$
- $4 \sin{\left(u + v \right)}$ **correct**

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=\cos{\left(u + v \right)}$ and $y=6 u + 2 v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=- \sin{\left(u + v \right)}&\quad \frac{\partial x}{\partial v}&=- \sin{\left(u + v \right)}\\\frac{\partial y}{\partial u}&=6&\quad \frac{\partial y}{\partial v}&=2\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}- \sin{\left(u + v \right)}&- \sin{\left(u + v \right)}\\6&2\end{matrix}\right|\\&=\left(- \sin{\left(u + v \right)}\right)\cdot\left(2\right)-\left(- \sin{\left(u + v \right)}\right)\cdot\left(6\right)\\&=4 \sin{\left(u + v \right)}.\end{aligned}
$$

## Generated moderate — trig_pair
Author metadata: profile `observed_trig_pair`, parameters `{'a': 5, 'b': 4}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}5 \sin{\left(u + v \right)}\\4 \cos{\left(u - v \right)}\end{bmatrix}.$

- $20 \sin{\left(u - v \right)} \cos{\left(u + v \right)}$
- $20 \sin{\left(u + v \right)} \cos{\left(u - v \right)}$
- $40 \sin{\left(u - v \right)} \cos{\left(u + v \right)}$ **correct**
- $40 \sin{\left(u + v \right)} \cos{\left(u - v \right)}$
- $400 \sin^{2}{\left(u - v \right)} \cos^{2}{\left(u + v \right)}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=5 \sin{\left(u + v \right)}$ and $y=4 \cos{\left(u - v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 \cos{\left(u + v \right)}&\quad \frac{\partial x}{\partial v}&=5 \cos{\left(u + v \right)}\\\frac{\partial y}{\partial u}&=- 4 \sin{\left(u - v \right)}&\quad \frac{\partial y}{\partial v}&=4 \sin{\left(u - v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 \cos{\left(u + v \right)}&5 \cos{\left(u + v \right)}\\- 4 \sin{\left(u - v \right)}&4 \sin{\left(u - v \right)}\end{matrix}\right|\\&=\left(5 \cos{\left(u + v \right)}\right)\cdot\left(4 \sin{\left(u - v \right)}\right)-\left(5 \cos{\left(u + v \right)}\right)\cdot\left(- 4 \sin{\left(u - v \right)}\right)\\&=40 \sin{\left(u - v \right)} \cos{\left(u + v \right)}.\end{aligned}
$$

## Generated moderate — trig_pair
Author metadata: profile `observed_trig_pair`, parameters `{'a': 5, 'b': 1}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}5 \sin{\left(u + v \right)}\\\cos{\left(u - v \right)}\end{bmatrix}.$

- $10 \sin{\left(u + v \right)} \cos{\left(u - v \right)}$
- $5 \sin{\left(u + v \right)} \cos{\left(u - v \right)}$
- $10 \sin{\left(u - v \right)} \cos{\left(u + v \right)}$ **correct**
- $5 \sin{\left(u - v \right)} \cos{\left(u + v \right)}$
- $25 \sin^{2}{\left(u - v \right)} \cos^{2}{\left(u + v \right)}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=5 \sin{\left(u + v \right)}$ and $y=\cos{\left(u - v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 \cos{\left(u + v \right)}&\quad \frac{\partial x}{\partial v}&=5 \cos{\left(u + v \right)}\\\frac{\partial y}{\partial u}&=- \sin{\left(u - v \right)}&\quad \frac{\partial y}{\partial v}&=\sin{\left(u - v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 \cos{\left(u + v \right)}&5 \cos{\left(u + v \right)}\\- \sin{\left(u - v \right)}&\sin{\left(u - v \right)}\end{matrix}\right|\\&=\left(5 \cos{\left(u + v \right)}\right)\cdot\left(\sin{\left(u - v \right)}\right)-\left(5 \cos{\left(u + v \right)}\right)\cdot\left(- \sin{\left(u - v \right)}\right)\\&=10 \sin{\left(u - v \right)} \cos{\left(u + v \right)}.\end{aligned}
$$

## Generated moderate — exp_quadratic
Author metadata: profile `observed_exp_quadratic`, parameters `{'a': 5, 'b': 4}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}e^{u + v}\\5 u^{2} + 4 v^{2}\end{bmatrix}.$

- $\left(5 u + 4 v\right) e^{u + v}$
- $20 u v e^{u + v}$
- $2 \left(5 u + 4 v\right) e^{u + v}$
- $- 2 \left(5 u - 4 v\right) e^{u} e^{v}$ **correct**
- $2 \left(5 u - 4 v\right) e^{u} e^{v}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=e^{u + v}$ and $y=5 u^{2} + 4 v^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=e^{u + v}&\quad \frac{\partial x}{\partial v}&=e^{u + v}\\\frac{\partial y}{\partial u}&=10 u&\quad \frac{\partial y}{\partial v}&=8 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}e^{u + v}&e^{u + v}\\10 u&8 v\end{matrix}\right|\\&=\left(e^{u + v}\right)\cdot\left(8 v\right)-\left(e^{u + v}\right)\cdot\left(10 u\right)\\&=- 2 \left(5 u - 4 v\right) e^{u} e^{v}.\end{aligned}
$$

## Generated moderate — exp_quadratic
Author metadata: profile `observed_exp_quadratic`, parameters `{'a': 5, 'b': 1}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}e^{u + v}\\5 u^{2} + v^{2}\end{bmatrix}.$

- $- 2 \left(5 u - v\right) e^{u} e^{v}$ **correct**
- $5 u v e^{u + v}$
- $2 \left(5 u + v\right) e^{u + v}$
- $\left(5 u + v\right) e^{u + v}$
- $2 \left(5 u - v\right) e^{u} e^{v}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=e^{u + v}$ and $y=5 u^{2} + v^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=e^{u + v}&\quad \frac{\partial x}{\partial v}&=e^{u + v}\\\frac{\partial y}{\partial u}&=10 u&\quad \frac{\partial y}{\partial v}&=2 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}e^{u + v}&e^{u + v}\\10 u&2 v\end{matrix}\right|\\&=\left(e^{u + v}\right)\cdot\left(2 v\right)-\left(e^{u + v}\right)\cdot\left(10 u\right)\\&=- 2 \left(5 u - v\right) e^{u} e^{v}.\end{aligned}
$$

## Generated moderate — log_product
Author metadata: profile `observed_log_product`, parameters `{'a': 5, 'b': 4}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}\log{\left(5 u + 4 v \right)}\\u v\end{bmatrix}.$

- $\frac{4 u - 4 v}{5 u + 4 v}$
- $\frac{- 4 u + 5 v}{5 u + 4 v}$
- $\frac{4 u + 4 v}{5 u + 4 v}$
- $1$
- $\frac{5 u - 4 v}{5 u + 4 v}$ **correct**

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=\log{\left(5 u + 4 v \right)}$ and $y=u v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=\frac{5}{5 u + 4 v}&\quad \frac{\partial x}{\partial v}&=\frac{4}{5 u + 4 v}\\\frac{\partial y}{\partial u}&=v&\quad \frac{\partial y}{\partial v}&=u\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}\frac{5}{5 u + 4 v}&\frac{4}{5 u + 4 v}\\v&u\end{matrix}\right|\\&=\left(\frac{5}{5 u + 4 v}\right)\cdot\left(u\right)-\left(\frac{4}{5 u + 4 v}\right)\cdot\left(v\right)\\&=\frac{5 u - 4 v}{5 u + 4 v}.\end{aligned}
$$

## Generated moderate — log_product
Author metadata: profile `observed_log_product`, parameters `{'a': 5, 'b': 1}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}\log{\left(5 u + v \right)}\\u v\end{bmatrix}.$

- $1$
- $\frac{- u + 5 v}{5 u + v}$
- $\frac{u + v}{5 u + v}$
- $\frac{u - v}{5 u + v}$
- $\frac{5 u - v}{5 u + v}$ **correct**

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=\log{\left(5 u + v \right)}$ and $y=u v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=\frac{5}{5 u + v}&\quad \frac{\partial x}{\partial v}&=\frac{1}{5 u + v}\\\frac{\partial y}{\partial u}&=v&\quad \frac{\partial y}{\partial v}&=u\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}\frac{5}{5 u + v}&\frac{1}{5 u + v}\\v&u\end{matrix}\right|\\&=\left(\frac{5}{5 u + v}\right)\cdot\left(u\right)-\left(\frac{1}{5 u + v}\right)\cdot\left(v\right)\\&=\frac{5 u - v}{5 u + v}.\end{aligned}
$$

## Generated easy — polar
Author metadata: profile `authored_polar`, parameters `{'a': 5, 'b': 4}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u \cos{\left(v \right)}\\4 u \sin{\left(v \right)}\end{bmatrix}.
$$

- $20 u$ **correct**
- $20 u \cos^{2}{\left(v \right)}$
- $- 20 u$
- $- 20 u \left(2 \sin^{2}{\left(v \right)} - 1\right)$
- $- 400 u^{2} \sin^{2}{\left(v \right)} \cos^{2}{\left(v \right)}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u \cos{\left(v \right)}$ and $y(u,v)=4 u \sin{\left(v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 \cos{\left(v \right)}&\quad \frac{\partial x}{\partial v}&=- 5 u \sin{\left(v \right)}\\\frac{\partial y}{\partial u}&=4 \sin{\left(v \right)}&\quad \frac{\partial y}{\partial v}&=4 u \cos{\left(v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 \cos{\left(v \right)}&- 5 u \sin{\left(v \right)}\\4 \sin{\left(v \right)}&4 u \cos{\left(v \right)}\end{matrix}\right|\\&=\left(5 \cos{\left(v \right)}\right)\cdot\left(4 u \cos{\left(v \right)}\right)-\left(- 5 u \sin{\left(v \right)}\right)\cdot\left(4 \sin{\left(v \right)}\right)\\&=20 u\left(\cos^2 v+\sin^2 v\right)\\&=20 u.\end{aligned}
$$

## Generated easy — polar
Author metadata: profile `authored_polar`, parameters `{'a': 5, 'b': 1}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u \cos{\left(v \right)}\\u \sin{\left(v \right)}\end{bmatrix}.
$$

- $- 5 u \left(2 \sin^{2}{\left(v \right)} - 1\right)$
- $5 u \cos^{2}{\left(v \right)}$
- $- 5 u$
- $5 u$ **correct**
- $- 25 u^{2} \sin^{2}{\left(v \right)} \cos^{2}{\left(v \right)}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u \cos{\left(v \right)}$ and $y(u,v)=u \sin{\left(v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 \cos{\left(v \right)}&\quad \frac{\partial x}{\partial v}&=- 5 u \sin{\left(v \right)}\\\frac{\partial y}{\partial u}&=\sin{\left(v \right)}&\quad \frac{\partial y}{\partial v}&=u \cos{\left(v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 \cos{\left(v \right)}&- 5 u \sin{\left(v \right)}\\\sin{\left(v \right)}&u \cos{\left(v \right)}\end{matrix}\right|\\&=\left(5 \cos{\left(v \right)}\right)\cdot\left(u \cos{\left(v \right)}\right)-\left(- 5 u \sin{\left(v \right)}\right)\cdot\left(\sin{\left(v \right)}\right)\\&=5 u\left(\cos^2 v+\sin^2 v\right)\\&=5 u.\end{aligned}
$$

## Generated easy — linear
Author metadata: profile `authored_linear`, parameters `{'a': 5, 'b': 4, 'c': 3, 'd': 3}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u + 4 v\\3 u + 3 v\end{bmatrix}.
$$

- $3$ **correct**
- $-3$
- $27$
- $15$
- $-12$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u + 4 v$ and $y(u,v)=3 u + 3 v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5&\quad \frac{\partial x}{\partial v}&=4\\\frac{\partial y}{\partial u}&=3&\quad \frac{\partial y}{\partial v}&=3\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5&4\\3&3\end{matrix}\right|\\&=\left(5\right)\cdot\left(3\right)-\left(4\right)\cdot\left(3\right)\\&=15-12\\&=3.\end{aligned}
$$

## Generated easy — linear
Author metadata: profile `authored_linear`, parameters `{'a': 5, 'b': 1, 'c': 3, 'd': 5}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u + v\\3 u + 5 v\end{bmatrix}.
$$

- $25$
- $-22$
- $28$
- $22$ **correct**
- $-3$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u + v$ and $y(u,v)=3 u + 5 v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5&\quad \frac{\partial x}{\partial v}&=1\\\frac{\partial y}{\partial u}&=3&\quad \frac{\partial y}{\partial v}&=5\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5&1\\3&5\end{matrix}\right|\\&=\left(5\right)\cdot\left(5\right)-\left(1\right)\cdot\left(3\right)\\&=25-3\\&=22.\end{aligned}
$$

## Generated easy — linear_log
Author metadata: profile `authored_linear_log`, parameters `{'a': 6, 'b': -5}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}6 u - 5 v\\\log{\left(u + v \right)}\end{bmatrix}.
$$

- $\frac{11}{u + v}$ **correct**
- $- \frac{11}{u + v}$
- $\frac{1}{u + v}$
- $\frac{6}{u + v}$
- $\frac{5}{u + v}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=6 u - 5 v$ and $y(u,v)=\log{\left(u + v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=6&\quad \frac{\partial x}{\partial v}&=-5\\\frac{\partial y}{\partial u}&=\frac{1}{u + v}&\quad \frac{\partial y}{\partial v}&=\frac{1}{u + v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}6&-5\\\frac{1}{u + v}&\frac{1}{u + v}\end{matrix}\right|\\&=\left(6\right)\cdot\left(\frac{1}{u + v}\right)-\left(-5\right)\cdot\left(\frac{1}{u + v}\right)\\&=\frac{11}{u + v}.\end{aligned}
$$

## Generated easy — linear_log
Author metadata: profile `authored_linear_log`, parameters `{'a': 6, 'b': -2}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}6 u - 2 v\\\log{\left(u + v \right)}\end{bmatrix}.
$$

- $\frac{6}{u + v}$
- $- \frac{8}{u + v}$
- $\frac{4}{u + v}$
- $\frac{8}{u + v}$ **correct**
- $\frac{2}{u + v}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=6 u - 2 v$ and $y(u,v)=\log{\left(u + v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=6&\quad \frac{\partial x}{\partial v}&=-2\\\frac{\partial y}{\partial u}&=\frac{1}{u + v}&\quad \frac{\partial y}{\partial v}&=\frac{1}{u + v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}6&-2\\\frac{1}{u + v}&\frac{1}{u + v}\end{matrix}\right|\\&=\left(6\right)\cdot\left(\frac{1}{u + v}\right)-\left(-2\right)\cdot\left(\frac{1}{u + v}\right)\\&=\frac{8}{u + v}.\end{aligned}
$$

## Generated easy — tan_product
Author metadata: profile `authored_tan_product`, parameters `{'k': 5}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}\cos{\left(v \right)} \tan{\left(\frac{u}{5} \right)}\\\sin{\left(v \right)}\end{bmatrix}.
$$

- $\frac{\cos^{2}{\left(v \right)}}{5 \cos^{2}{\left(\frac{u}{5} \right)}}$ **correct**
- $\frac{5 \cos^{2}{\left(v \right)}}{\cos^{2}{\left(\frac{u}{5} \right)}}$
- $\frac{\cos^{2}{\left(v \right)}}{\cos^{2}{\left(\frac{u}{5} \right)}}$
- $- \frac{\cos^{2}{\left(v \right)}}{5 \cos^{2}{\left(\frac{u}{5} \right)}}$
- $\left(\frac{\tan^{2}{\left(\frac{u}{5} \right)}}{5} + \frac{1}{5}\right) \cos{\left(v \right)}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=\cos{\left(v \right)} \tan{\left(\frac{u}{5} \right)}$ and $y(u,v)=\sin{\left(v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=\left(\frac{\tan^{2}{\left(\frac{u}{5} \right)}}{5} + \frac{1}{5}\right) \cos{\left(v \right)}&\quad \frac{\partial x}{\partial v}&=- \sin{\left(v \right)} \tan{\left(\frac{u}{5} \right)}\\\frac{\partial y}{\partial u}&=0&\quad \frac{\partial y}{\partial v}&=\cos{\left(v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}\left(\frac{\tan^{2}{\left(\frac{u}{5} \right)}}{5} + \frac{1}{5}\right) \cos{\left(v \right)}&- \sin{\left(v \right)} \tan{\left(\frac{u}{5} \right)}\\0&\cos{\left(v \right)}\end{matrix}\right|\\&=\frac{\cos^{2}{\left(v \right)}}{5 \cos^{2}{\left(\frac{u}{5} \right)}}.\end{aligned}
$$

## Generated easy — tan_product
Author metadata: profile `authored_tan_product`, parameters `{'k': 2}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}\cos{\left(v \right)} \tan{\left(\frac{u}{2} \right)}\\\sin{\left(v \right)}\end{bmatrix}.
$$

- $- \frac{\cos^{2}{\left(v \right)}}{2 \cos^{2}{\left(\frac{u}{2} \right)}}$
- $\frac{2 \cos^{2}{\left(v \right)}}{\cos^{2}{\left(\frac{u}{2} \right)}}$
- $\frac{\cos^{2}{\left(v \right)}}{\cos^{2}{\left(\frac{u}{2} \right)}}$
- $\frac{\cos^{2}{\left(v \right)}}{2 \cos^{2}{\left(\frac{u}{2} \right)}}$ **correct**
- $\left(\frac{\tan^{2}{\left(\frac{u}{2} \right)}}{2} + \frac{1}{2}\right) \cos{\left(v \right)}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=\cos{\left(v \right)} \tan{\left(\frac{u}{2} \right)}$ and $y(u,v)=\sin{\left(v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=\left(\frac{\tan^{2}{\left(\frac{u}{2} \right)}}{2} + \frac{1}{2}\right) \cos{\left(v \right)}&\quad \frac{\partial x}{\partial v}&=- \sin{\left(v \right)} \tan{\left(\frac{u}{2} \right)}\\\frac{\partial y}{\partial u}&=0&\quad \frac{\partial y}{\partial v}&=\cos{\left(v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}\left(\frac{\tan^{2}{\left(\frac{u}{2} \right)}}{2} + \frac{1}{2}\right) \cos{\left(v \right)}&- \sin{\left(v \right)} \tan{\left(\frac{u}{2} \right)}\\0&\cos{\left(v \right)}\end{matrix}\right|\\&=\frac{\cos^{2}{\left(v \right)}}{2 \cos^{2}{\left(\frac{u}{2} \right)}}.\end{aligned}
$$

## Generated easy — quadratic
Author metadata: profile `authored_quadratic`, parameters `{'a': 5, 'b': 4}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u^{2} - 4 v^{2}\\5 u^{2} + 4 v^{2}\end{bmatrix}.
$$

- $160 u v$ **correct**
- $80 u v$
- $- 160 u v$
- $0$
- $- 6400 u^{2} v^{2}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u^{2} - 4 v^{2}$ and $y(u,v)=5 u^{2} + 4 v^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=10 u&\quad \frac{\partial x}{\partial v}&=- 8 v\\\frac{\partial y}{\partial u}&=10 u&\quad \frac{\partial y}{\partial v}&=8 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}10 u&- 8 v\\10 u&8 v\end{matrix}\right|\\&=\left(10 u\right)\cdot\left(8 v\right)-\left(- 8 v\right)\cdot\left(10 u\right)\\&=80 u v+80 u v\\&=160 u v.\end{aligned}
$$

## Generated easy — quadratic
Author metadata: profile `authored_quadratic`, parameters `{'a': 5, 'b': 1}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u^{2} - v^{2}\\5 u^{2} + v^{2}\end{bmatrix}.
$$

- $0$
- $20 u v$
- $- 40 u v$
- $40 u v$ **correct**
- $- 400 u^{2} v^{2}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u^{2} - v^{2}$ and $y(u,v)=5 u^{2} + v^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=10 u&\quad \frac{\partial x}{\partial v}&=- 2 v\\\frac{\partial y}{\partial u}&=10 u&\quad \frac{\partial y}{\partial v}&=2 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}10 u&- 2 v\\10 u&2 v\end{matrix}\right|\\&=\left(10 u\right)\cdot\left(2 v\right)-\left(- 2 v\right)\cdot\left(10 u\right)\\&=20 u v+20 u v\\&=40 u v.\end{aligned}
$$

## Generated moderate — exp_log
Author metadata: profile `authored_exp_log`, parameters `{'a': 5, 'b': 4}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}e^{5 u + 4 v}\\\log{\left(u v \right)}\end{bmatrix}.$

- $\frac{\left(5 u - 4 v\right) e^{5 u} e^{4 v}}{u v}$ **correct**
- $- \frac{\left(5 u - 4 v\right) e^{5 u} e^{4 v}}{u v}$
- $\frac{\left(5 u + 4 v\right) e^{5 u} e^{4 v}}{u v}$
- $\frac{5 e^{5 u} e^{4 v}}{v}$
- $- \frac{4 e^{5 u} e^{4 v}}{u}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=e^{5 u + 4 v}$ and $y(u,v)=\log{\left(u v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 e^{5 u + 4 v}&\quad \frac{\partial x}{\partial v}&=4 e^{5 u + 4 v}\\\frac{\partial y}{\partial u}&=\frac{1}{u}&\quad \frac{\partial y}{\partial v}&=\frac{1}{v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 e^{5 u + 4 v}&4 e^{5 u + 4 v}\\\frac{1}{u}&\frac{1}{v}\end{matrix}\right|\\&=\left(5 e^{5 u + 4 v}\right)\cdot\left(\frac{1}{v}\right)-\left(4 e^{5 u + 4 v}\right)\cdot\left(\frac{1}{u}\right)\\&=\frac{5 e^{5 u + 4 v}}{v}-\frac{4 e^{5 u + 4 v}}{u}\\&=\frac{\left(5 u - 4 v\right) e^{5 u} e^{4 v}}{u v}.\end{aligned}
$$

## Generated moderate — exp_log
Author metadata: profile `authored_exp_log`, parameters `{'a': 5, 'b': 1}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}e^{5 u + v}\\\log{\left(u v \right)}\end{bmatrix}.$

- $\frac{5 e^{5 u} e^{v}}{v}$
- $- \frac{\left(5 u - v\right) e^{5 u} e^{v}}{u v}$
- $\frac{\left(5 u + v\right) e^{5 u} e^{v}}{u v}$
- $\frac{\left(5 u - v\right) e^{5 u} e^{v}}{u v}$ **correct**
- $- \frac{e^{5 u} e^{v}}{u}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=e^{5 u + v}$ and $y(u,v)=\log{\left(u v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 e^{5 u + v}&\quad \frac{\partial x}{\partial v}&=e^{5 u + v}\\\frac{\partial y}{\partial u}&=\frac{1}{u}&\quad \frac{\partial y}{\partial v}&=\frac{1}{v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 e^{5 u + v}&e^{5 u + v}\\\frac{1}{u}&\frac{1}{v}\end{matrix}\right|\\&=\left(5 e^{5 u + v}\right)\cdot\left(\frac{1}{v}\right)-\left(e^{5 u + v}\right)\cdot\left(\frac{1}{u}\right)\\&=\frac{5 e^{5 u + v}}{v}-\frac{e^{5 u + v}}{u}\\&=\frac{\left(5 u - v\right) e^{5 u} e^{v}}{u v}.\end{aligned}
$$

## Generated moderate — cos_linear
Author metadata: profile `authored_cos_linear`, parameters `{'a': 6, 'b': 5}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}\cos{\left(u + v \right)}\\6 u + 5 v\end{bmatrix}.$

- $\sin{\left(u + v \right)}$ **correct**
- $- \sin{\left(u + v \right)}$
- $- 11 \sin{\left(u + v \right)}$
- $- 5 \sin{\left(u + v \right)}$
- $6 \sin{\left(u + v \right)}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=\cos{\left(u + v \right)}$ and $y=6 u + 5 v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=- \sin{\left(u + v \right)}&\quad \frac{\partial x}{\partial v}&=- \sin{\left(u + v \right)}\\\frac{\partial y}{\partial u}&=6&\quad \frac{\partial y}{\partial v}&=5\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}- \sin{\left(u + v \right)}&- \sin{\left(u + v \right)}\\6&5\end{matrix}\right|\\&=\left(- \sin{\left(u + v \right)}\right)\cdot\left(5\right)-\left(- \sin{\left(u + v \right)}\right)\cdot\left(6\right)\\&=\sin{\left(u + v \right)}.\end{aligned}
$$

## Generated moderate — cos_linear
Author metadata: profile `authored_cos_linear`, parameters `{'a': 6, 'b': 2}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}\cos{\left(u + v \right)}\\6 u + 2 v\end{bmatrix}.$

- $- 2 \sin{\left(u + v \right)}$
- $- 4 \sin{\left(u + v \right)}$
- $- 8 \sin{\left(u + v \right)}$
- $4 \sin{\left(u + v \right)}$ **correct**
- $6 \sin{\left(u + v \right)}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=\cos{\left(u + v \right)}$ and $y=6 u + 2 v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=- \sin{\left(u + v \right)}&\quad \frac{\partial x}{\partial v}&=- \sin{\left(u + v \right)}\\\frac{\partial y}{\partial u}&=6&\quad \frac{\partial y}{\partial v}&=2\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}- \sin{\left(u + v \right)}&- \sin{\left(u + v \right)}\\6&2\end{matrix}\right|\\&=\left(- \sin{\left(u + v \right)}\right)\cdot\left(2\right)-\left(- \sin{\left(u + v \right)}\right)\cdot\left(6\right)\\&=4 \sin{\left(u + v \right)}.\end{aligned}
$$

## Generated moderate — trig_pair
Author metadata: profile `authored_trig_pair`, parameters `{'a': 5, 'b': 4}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}5 \sin{\left(u + v \right)}\\4 \cos{\left(u - v \right)}\end{bmatrix}.$

- $40 \sin{\left(u - v \right)} \cos{\left(u + v \right)}$ **correct**
- $20 \sin{\left(u - v \right)} \cos{\left(u + v \right)}$
- $- 40 \sin{\left(u - v \right)} \cos{\left(u + v \right)}$
- $0$
- $- 400 \sin^{2}{\left(u - v \right)} \cos^{2}{\left(u + v \right)}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=5 \sin{\left(u + v \right)}$ and $y=4 \cos{\left(u - v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 \cos{\left(u + v \right)}&\quad \frac{\partial x}{\partial v}&=5 \cos{\left(u + v \right)}\\\frac{\partial y}{\partial u}&=- 4 \sin{\left(u - v \right)}&\quad \frac{\partial y}{\partial v}&=4 \sin{\left(u - v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 \cos{\left(u + v \right)}&5 \cos{\left(u + v \right)}\\- 4 \sin{\left(u - v \right)}&4 \sin{\left(u - v \right)}\end{matrix}\right|\\&=\left(5 \cos{\left(u + v \right)}\right)\cdot\left(4 \sin{\left(u - v \right)}\right)-\left(5 \cos{\left(u + v \right)}\right)\cdot\left(- 4 \sin{\left(u - v \right)}\right)\\&=40 \sin{\left(u - v \right)} \cos{\left(u + v \right)}.\end{aligned}
$$

## Generated moderate — trig_pair
Author metadata: profile `authored_trig_pair`, parameters `{'a': 5, 'b': 1}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}5 \sin{\left(u + v \right)}\\\cos{\left(u - v \right)}\end{bmatrix}.$

- $0$
- $5 \sin{\left(u - v \right)} \cos{\left(u + v \right)}$
- $- 10 \sin{\left(u - v \right)} \cos{\left(u + v \right)}$
- $10 \sin{\left(u - v \right)} \cos{\left(u + v \right)}$ **correct**
- $- 25 \sin^{2}{\left(u - v \right)} \cos^{2}{\left(u + v \right)}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=5 \sin{\left(u + v \right)}$ and $y=\cos{\left(u - v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 \cos{\left(u + v \right)}&\quad \frac{\partial x}{\partial v}&=5 \cos{\left(u + v \right)}\\\frac{\partial y}{\partial u}&=- \sin{\left(u - v \right)}&\quad \frac{\partial y}{\partial v}&=\sin{\left(u - v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 \cos{\left(u + v \right)}&5 \cos{\left(u + v \right)}\\- \sin{\left(u - v \right)}&\sin{\left(u - v \right)}\end{matrix}\right|\\&=\left(5 \cos{\left(u + v \right)}\right)\cdot\left(\sin{\left(u - v \right)}\right)-\left(5 \cos{\left(u + v \right)}\right)\cdot\left(- \sin{\left(u - v \right)}\right)\\&=10 \sin{\left(u - v \right)} \cos{\left(u + v \right)}.\end{aligned}
$$

## Generated moderate — exp_quadratic
Author metadata: profile `authored_exp_quadratic`, parameters `{'a': 5, 'b': 4}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}e^{u + v}\\5 u^{2} + 4 v^{2}\end{bmatrix}.$

- $- 2 \left(5 u - 4 v\right) e^{u} e^{v}$ **correct**
- $2 \left(5 u - 4 v\right) e^{u} e^{v}$
- $2 \left(5 u + 4 v\right) e^{u} e^{v}$
- $8 v e^{u} e^{v}$
- $- 10 u e^{u} e^{v}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=e^{u + v}$ and $y=5 u^{2} + 4 v^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=e^{u + v}&\quad \frac{\partial x}{\partial v}&=e^{u + v}\\\frac{\partial y}{\partial u}&=10 u&\quad \frac{\partial y}{\partial v}&=8 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}e^{u + v}&e^{u + v}\\10 u&8 v\end{matrix}\right|\\&=\left(e^{u + v}\right)\cdot\left(8 v\right)-\left(e^{u + v}\right)\cdot\left(10 u\right)\\&=- 2 \left(5 u - 4 v\right) e^{u} e^{v}.\end{aligned}
$$

## Generated moderate — exp_quadratic
Author metadata: profile `authored_exp_quadratic`, parameters `{'a': 5, 'b': 1}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}e^{u + v}\\5 u^{2} + v^{2}\end{bmatrix}.$

- $2 v e^{u} e^{v}$
- $2 \left(5 u - v\right) e^{u} e^{v}$
- $2 \left(5 u + v\right) e^{u} e^{v}$
- $- 2 \left(5 u - v\right) e^{u} e^{v}$ **correct**
- $- 10 u e^{u} e^{v}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=e^{u + v}$ and $y=5 u^{2} + v^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=e^{u + v}&\quad \frac{\partial x}{\partial v}&=e^{u + v}\\\frac{\partial y}{\partial u}&=10 u&\quad \frac{\partial y}{\partial v}&=2 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}e^{u + v}&e^{u + v}\\10 u&2 v\end{matrix}\right|\\&=\left(e^{u + v}\right)\cdot\left(2 v\right)-\left(e^{u + v}\right)\cdot\left(10 u\right)\\&=- 2 \left(5 u - v\right) e^{u} e^{v}.\end{aligned}
$$

## Generated moderate — log_product
Author metadata: profile `authored_log_product`, parameters `{'a': 5, 'b': 4}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}\log{\left(5 u + 4 v \right)}\\u v\end{bmatrix}.$

- $\frac{5 u - 4 v}{5 u + 4 v}$ **correct**
- $- \frac{5 u - 4 v}{5 u + 4 v}$
- $1$
- $\frac{5 u}{5 u + 4 v}$
- $- \frac{4 v}{5 u + 4 v}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=\log{\left(5 u + 4 v \right)}$ and $y=u v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=\frac{5}{5 u + 4 v}&\quad \frac{\partial x}{\partial v}&=\frac{4}{5 u + 4 v}\\\frac{\partial y}{\partial u}&=v&\quad \frac{\partial y}{\partial v}&=u\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}\frac{5}{5 u + 4 v}&\frac{4}{5 u + 4 v}\\v&u\end{matrix}\right|\\&=\left(\frac{5}{5 u + 4 v}\right)\cdot\left(u\right)-\left(\frac{4}{5 u + 4 v}\right)\cdot\left(v\right)\\&=\frac{5 u - 4 v}{5 u + 4 v}.\end{aligned}
$$

## Generated moderate — log_product
Author metadata: profile `authored_log_product`, parameters `{'a': 5, 'b': 1}`.

Find the Jacobian determinant of the transformation $T(\begin{bmatrix}u\\v\end{bmatrix})=\begin{bmatrix}\log{\left(5 u + v \right)}\\u v\end{bmatrix}.$

- $\frac{5 u}{5 u + v}$
- $- \frac{5 u - v}{5 u + v}$
- $1$
- $\frac{5 u - v}{5 u + v}$ **correct**
- $- \frac{v}{5 u + v}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=\log{\left(5 u + v \right)}$ and $y=u v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=\frac{5}{5 u + v}&\quad \frac{\partial x}{\partial v}&=\frac{1}{5 u + v}\\\frac{\partial y}{\partial u}&=v&\quad \frac{\partial y}{\partial v}&=u\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}\frac{5}{5 u + v}&\frac{1}{5 u + v}\\v&u\end{matrix}\right|\\&=\left(\frac{5}{5 u + v}\right)\cdot\left(u\right)-\left(\frac{1}{5 u + v}\right)\cdot\left(v\right)\\&=\frac{5 u - v}{5 u + v}.\end{aligned}
$$

## Generated hard — powers
Author metadata: profile `authored_powers`, parameters `{'a': 3, 'b': 2, 'm': 2, 'n': 3, 'p': 2, 'q': 2, 'r': 1, 's': 2}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}3 \left(2 u + 2 v\right)^{2}\\2 \left(u - 2 v\right)^{3}\end{bmatrix}.
$$

- $- 432 \left(u - 2 v\right)^{2} \left(u + v\right)$ **correct**
- $- 288 \left(u - 2 v\right)^{2} \left(u + v\right)$
- $432 \left(u - 2 v\right)^{2} \left(u + v\right)$
- $- 144 \left(u - 2 v\right)^{2} \left(u + v\right)$
- $- 41472 \left(u - 2 v\right)^{4} \left(u + v\right)^{2}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=3 \left(2 u + 2 v\right)^{2}$ and $y=2 \left(u - 2 v\right)^{3}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=24 u + 24 v&\quad \frac{\partial x}{\partial v}&=24 u + 24 v\\\frac{\partial y}{\partial u}&=6 \left(u - 2 v\right)^{2}&\quad \frac{\partial y}{\partial v}&=- 12 \left(u - 2 v\right)^{2}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}24 u + 24 v&24 u + 24 v\\6 \left(u - 2 v\right)^{2}&- 12 \left(u - 2 v\right)^{2}\end{matrix}\right|\\&=\left(24 u + 24 v\right)\cdot\left(- 12 \left(u - 2 v\right)^{2}\right)-\left(24 u + 24 v\right)\cdot\left(6 \left(u - 2 v\right)^{2}\right)\\&=- 432 \left(u - 2 v\right)^{2} \left(u + v\right).\end{aligned}
$$

## Generated hard — powers
Author metadata: profile `authored_powers`, parameters `{'a': 3, 'b': 1, 'm': 2, 'n': 3, 'p': 2, 'q': 1, 'r': 2, 's': 2}`.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}3 \left(2 u + v\right)^{2}\\\left(2 u - 2 v\right)^{3}\end{bmatrix}.
$$

- $- 144 \left(u - v\right)^{2} \left(2 u + v\right)$
- $- 288 \left(u - v\right)^{2} \left(2 u + v\right)$
- $432 \left(u - v\right)^{2} \left(2 u + v\right)$
- $- 432 \left(u - v\right)^{2} \left(2 u + v\right)$ **correct**
- $- 41472 \left(u - v\right)^{4} \left(2 u + v\right)^{2}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x=3 \left(2 u + v\right)^{2}$ and $y=\left(2 u - 2 v\right)^{3}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=24 u + 12 v&\quad \frac{\partial x}{\partial v}&=12 u + 6 v\\\frac{\partial y}{\partial u}&=6 \left(2 u - 2 v\right)^{2}&\quad \frac{\partial y}{\partial v}&=- 6 \left(2 u - 2 v\right)^{2}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}24 u + 12 v&12 u + 6 v\\6 \left(2 u - 2 v\right)^{2}&- 6 \left(2 u - 2 v\right)^{2}\end{matrix}\right|\\&=\left(24 u + 12 v\right)\cdot\left(- 6 \left(2 u - 2 v\right)^{2}\right)-\left(12 u + 6 v\right)\cdot\left(6 \left(2 u - 2 v\right)^{2}\right)\\&=- 432 \left(u - v\right)^{2} \left(2 u + v\right).\end{aligned}
$$
