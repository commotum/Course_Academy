# Evaluating Jacobian review

Original raw records below; all variants explicitly labeled. Standard matrix and trig notation normalization; one source typo repaired.

## Original q-160380

For the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}2u\operatorname{cos}⁡v \\ 3u\operatorname{sin}⁡v\end{aligned}]
$$

compute the value of the Jacobian determinant at the point where $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}1 \\ 2\end{aligned}].$

Original choices: $0$, $4$, $12$, $8$, $6$

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

Finally, when $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}1 \\ 2\end{aligned}],$ the value of our Jacobian determinant is

$$
{\frac{∂(x,y)}{∂(u,v)}|}_{(1,2)}=6(1)=6.
$$

### Generated source-parameter replay

## Generated easy — polar
Review metadata: `observed_polar`, `{'a': 2, 'b': 3, 'U': '1', 'V': '2'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}2 u \cos{\left(v \right)}\\3 u \sin{\left(v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix}.$

- $12$
- $4$
- $0$
- $6$ **correct**
- $8$

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

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,2)}=6 \left(1\right)=6.
$$

## Original q-160394

For the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{e}^{u+v} \\ {e}^{u-v}\end{aligned}].
$$

compute the value of the Jacobian determinant at the point where $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}0 \\ -5\end{aligned}].$

Original choices: $3$, $-2$, $-1$, $1$, $-3$

Original worked solution:
Given a transformation 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y)}{∂(u,v)},$ is given by

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}|.\end{aligned}
$$

Here, we have $x(u,v)={e}^{u+v}$ and $y(u,v)={e}^{u-v}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & ={e}^{u+v} & \,\frac{∂x}{∂v} & ={e}^{u+v} \\ \frac{∂y}{∂u} & ={e}^{u-v} & \,\frac{∂y}{∂v} & =-{e}^{u-v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}{e}^{u+v} & {e}^{u+v} \\ {e}^{u-v} & -{e}^{u-v}\end{aligned}| \\  & ={e}^{u+v}\cdot (-{e}^{u-v})-{e}^{u+v}\cdot {e}^{u-v} \\  & =-{e}^{2u}-{e}^{2u} \\  & =-2{e}^{2u}.\end{aligned}
$$

Finally, when $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}0 \\ -5\end{aligned}],$ the value of our Jacobian determinant is

$$
{\frac{∂(x,y)}{∂(u,v)}|}_{(0,-5)}=-2{e}^{2(0)}=-2.
$$

### Generated source-parameter replay

## Generated easy — exp_pair
Review metadata: `observed_exp_pair`, `{'a': 1, 'b': 1, 'U': '0', 'V': '-5'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}e^{u + v}\\e^{u - v}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}0\\-5\end{bmatrix}.$

- $-1$
- $-2$ **correct**
- $3$
- $-3$
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

Here, we have $x(u,v)=e^{u + v}$ and $y(u,v)=e^{u - v}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=e^{u + v}&\quad \frac{\partial x}{\partial v}&=e^{u + v}\\\frac{\partial y}{\partial u}&=e^{u - v}&\quad \frac{\partial y}{\partial v}&=- e^{u - v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}e^{u + v}&e^{u + v}\\e^{u - v}&- e^{u - v}\end{matrix}\right|\\&=\left(e^{u + v}\right)\cdot\left(- e^{u - v}\right)-\left(e^{u + v}\right)\cdot\left(e^{u - v}\right)\\&=- e^{u - v} e^{u + v}-\left(e^{u - v} e^{u + v}\right)\\&=- 2 e^{2 u}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}0\\-5\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(0,-5)}=- 2 e^{2 \left(0\right)}=-2.
$$

## Original q-160383

For the transformation $T,$ defined as 

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}uv \\ \frac{v}{u}\end{aligned}]
$$

 

compute the value of the Jacobian determinant at the point where $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}-2 \\ 3\end{aligned}].$

Original choices: $-4$, $-3$, $3$, $1$, $2$

Original worked solution:
Given a transformation 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y)}{∂(u,v)},$ is given by

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}|.\end{aligned}
$$

Here, we have $x=uv$ and $y=\frac{v}{u}.$ 

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =v & \,\frac{∂x}{∂v} & =u \\ \frac{∂y}{∂u} & =-\frac{v}{{u}^{2}} & \,\frac{∂y}{∂v} & =\frac{1}{u}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}v & u \\ -\frac{v}{{u}^{2}}\, & \frac{1}{u}\end{aligned}| \\  & =v\cdot \frac{1}{u}\text{ }-u\cdot (-\frac{v}{{u}^{2}}) \\  & =\frac{2v}{u}.\end{aligned}
$$

Finally, when $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}-2 \\ 3\end{aligned}],$ the value of our Jacobian determinant is

$$
{\frac{∂(x,y)}{∂(u,v)}|}_{(-2,3)}=\frac{2(3)}{-2}=-3.
$$

### Generated source-parameter replay

## Generated easy — quotient
Review metadata: `observed_quotient`, `{'a': 1, 'b': 1, 'U': '-2', 'V': '3'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}u v\\\frac{v}{u}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}-2\\3\end{bmatrix}.$

- $3$
- $-3$ **correct**
- $-4$
- $2$
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

Here, we have $x(u,v)=u v$ and $y(u,v)=\frac{v}{u}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=v&\quad \frac{\partial x}{\partial v}&=u\\\frac{\partial y}{\partial u}&=- \frac{v}{u^{2}}&\quad \frac{\partial y}{\partial v}&=\frac{1}{u}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}v&u\\- \frac{v}{u^{2}}&\frac{1}{u}\end{matrix}\right|\\&=\left(v\right)\cdot\left(\frac{1}{u}\right)-\left(u\right)\cdot\left(- \frac{v}{u^{2}}\right)\\&=\frac{2 v}{u}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}-2\\3\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-2,3)}=\frac{2 \left(3\right)}{\left(-2\right)}=-3.
$$

## Original q-160402

For the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{e}^{u-v} \\ \operatorname{ln}⁡(uv)\end{aligned}].
$$

compute the value of the Jacobian determinant at the point where $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}1 \\ 1\end{aligned}].$

Original choices: $2$, $0$, $1$, $3$, $-1$

Original worked solution:
Given a transformation 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y)}{∂(u,v)},$ is given by

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}|.\end{aligned}
$$

Here, we have $x(u,v)={e}^{u-v}$ and $y(u,v)=\operatorname{ln}⁡(uv).$  

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & ={e}^{u-v} & \,\frac{∂x}{∂v} & =-{e}^{u-v} \\ \frac{∂y}{∂u} & =\frac{1}{u} & \,\frac{∂y}{∂v} & =\frac{1}{v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}{e}^{u-v} & -{e}^{u-v} \\ \frac{1}{u} & \frac{1}{v}\end{aligned}| \\  & ={e}^{u-v}\cdot (\frac{1}{v})-(-{e}^{u-v})\cdot \frac{1}{u} \\  & =\frac{{e}^{u-v}}{v}+\frac{{e}^{u-v}}{u}.\end{aligned}
$$

Finally, when $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}1 \\ 1\end{aligned}],$ the value of our Jacobian determinant is

$$
{\frac{∂(x,y)}{∂(u,v)}|}_{(1,1)}=\frac{{e}^{(1)-(1)}}{(1)}+\frac{{e}^{(1)-(1)}}{(1)}=2.
$$

### Generated source-parameter replay

## Generated easy — exp_log
Review metadata: `observed_exp_log`, `{'a': 1, 'b': 1, 'U': '1', 'V': '1'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}e^{u - v}\\\log{\left(u v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\1\end{bmatrix}.$

- $1$
- $0$
- $2$ **correct**
- $-1$
- $3$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=e^{u - v}$ and $y(u,v)=\log{\left(u v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=e^{u - v}&\quad \frac{\partial x}{\partial v}&=- e^{u - v}\\\frac{\partial y}{\partial u}&=\frac{1}{u}&\quad \frac{\partial y}{\partial v}&=\frac{1}{v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}e^{u - v}&- e^{u - v}\\\frac{1}{u}&\frac{1}{v}\end{matrix}\right|\\&=\left(e^{u - v}\right)\cdot\left(\frac{1}{v}\right)-\left(- e^{u - v}\right)\cdot\left(\frac{1}{u}\right)\\&=\frac{\left(u + v\right) e^{u} e^{- v}}{u v}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\1\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,1)}=\frac{\left(\left(1\right) + \left(1\right)\right) e^{\left(1\right)} e^{- \left(1\right)}}{\left(1\right) \left(1\right)}=2.
$$

## Original q-160427

For the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{u}^{2}+{v}^{2} \\ {u}^{2}-{v}^{2}\end{aligned}]
$$

compute the value of the Jacobian determinant at the point where $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}-2 \\ 1\end{aligned}].$

Original choices: $16$, $-8$, $14$, $12$, $18$

Original worked solution:
Given a transformation 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y)}{∂(u,v)},$ is given by

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}|.\end{aligned}
$$

Here, we have $x(u,v)={u}^{2}+{v}^{2}$ and $y(u,v)={u}^{2}-{v}^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2u & \,\frac{∂x}{∂v} & =2v \\ \frac{∂y}{∂u} & =2u & \,\frac{∂y}{∂v} & =-2v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2u & 2v \\ 2u & -2v\end{aligned}| \\  & =2u\cdot (-2v)-2v\cdot 2u \\  & =-4uv-4uv \\  & =-8uv.\end{aligned}
$$

Finally, when $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}-2 \\ 1\end{aligned}],$ the value of our Jacobian determinant is

$$
{\frac{∂(x,y)}{∂(u,v)}|}_{(-2,1)}=-8(-2)(1)=16.
$$

### Generated source-parameter replay

## Generated easy — square_pair
Review metadata: `observed_square_pair`, `{'a': 1, 'b': 1, 'U': '-2', 'V': '1'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}u^{2} + v^{2}\\u^{2} - v^{2}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}-2\\1\end{bmatrix}.$

- $14$
- $-8$
- $16$ **correct**
- $18$
- $12$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=u^{2} + v^{2}$ and $y(u,v)=u^{2} - v^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=2 u&\quad \frac{\partial x}{\partial v}&=2 v\\\frac{\partial y}{\partial u}&=2 u&\quad \frac{\partial y}{\partial v}&=- 2 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}2 u&2 v\\2 u&- 2 v\end{matrix}\right|\\&=\left(2 u\right)\cdot\left(- 2 v\right)-\left(2 v\right)\cdot\left(2 u\right)\\&=- 4 u v-\left(4 u v\right)\\&=- 8 u v.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}-2\\1\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-2,1)}=- 8 \left(-2\right) \left(1\right)=16.
$$

## Original q-160428

For the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\frac{{u}^{2}-{v}^{2}}{2} \\ uv\end{aligned}]
$$

compute the value of the Jacobian determinant at the point where $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}-1 \\ -2\end{aligned}].$

Original choices: $5$, $-2$, $2$, $3$, $8$

Original worked solution:
Given a transformation 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y)}{∂(u,v)},$ is given by

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}|.\end{aligned}
$$

Here, we have $x(u,v)=\frac{{u}^{2}-{v}^{2}}{2}$ and $y(u,v)=uv.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =u & \,\frac{∂x}{∂v} & =-v \\ \frac{∂y}{∂u} & =v & \,\frac{∂y}{∂v} & =u\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}u & -v \\ v & u\end{aligned}| \\  & =u\cdot u-(-v)\cdot v \\  & ={u}^{2}+{v}^{2}.\end{aligned}
$$

Finally, when $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}-1 \\ -2\end{aligned}],$ the value of our Jacobian determinant is

$$
{\frac{∂(x,y)}{∂(u,v)}|}_{(-1,-2)}=(-1)^{2}+(-2)^{2}=5.
$$

### Generated source-parameter replay

## Generated easy — complex_square
Review metadata: `observed_complex_square`, `{'a': 1, 'b': 1, 'U': '-1', 'V': '-2'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}\frac{u^{2}}{2} - \frac{v^{2}}{2}\\u v\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}-1\\-2\end{bmatrix}.$

- $2$
- $-2$
- $5$ **correct**
- $8$
- $3$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=\frac{u^{2}}{2} - \frac{v^{2}}{2}$ and $y(u,v)=u v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=u&\quad \frac{\partial x}{\partial v}&=- v\\\frac{\partial y}{\partial u}&=v&\quad \frac{\partial y}{\partial v}&=u\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}u&- v\\v&u\end{matrix}\right|\\&=\left(u\right)\cdot\left(u\right)-\left(- v\right)\cdot\left(v\right)\\&=u^{2} + v^{2}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}-1\\-2\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-1,-2)}=\left(-1\right)^{2} + \left(-2\right)^{2}=5.
$$

## Original q-160431

For the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{v}^{2}+uv \\ v-u\end{aligned}]
$$

compute the value of the Jacobian determinant at the point where $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}8 \\ -2\end{aligned}].$

Original choices: $4$, $6$, $1$, $2$, $3$

Original worked solution:
Given a transformation 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y)}{∂(u,v)},$ is given by

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}|.\end{aligned}
$$

Here, we have $x(u,v)={v}^{2}+uv$ and $y(u,v)=v-u.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =v & \,\frac{∂x}{∂v} & =2v+u \\ \frac{∂y}{∂u} & =-1 & \,\frac{∂y}{∂v} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}v & 2v+u \\ -1 & 1\end{aligned}| \\  & =v\cdot 1-(2v+u)\cdot (-1) \\  & =v+2v+u \\  & =3v+u.\end{aligned}
$$

Finally, when $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}8 \\ -2\end{aligned}],$ the value of our Jacobian determinant is

$$
{\frac{∂(x,y)}{∂(u,v)}|}_{(8,-2)}=3(-2)+8=2.
$$

### Generated source-parameter replay

## Generated easy — mixed_linear
Review metadata: `observed_mixed_linear`, `{'a': 1, 'b': 1, 'U': '8', 'V': '-2'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}u v + v^{2}\\- u + v\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}8\\-2\end{bmatrix}.$

- $1$
- $6$
- $4$
- $3$
- $2$ **correct**

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=u v + v^{2}$ and $y(u,v)=- u + v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=v&\quad \frac{\partial x}{\partial v}&=u + 2 v\\\frac{\partial y}{\partial u}&=-1&\quad \frac{\partial y}{\partial v}&=1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}v&u + 2 v\\-1&1\end{matrix}\right|\\&=\left(v\right)\cdot\left(1\right)-\left(u + 2 v\right)\cdot\left(-1\right)\\&=v-\left(- u - 2 v\right)\\&=u + 3 v.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}8\\-2\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(8,-2)}=\left(8\right) + 3 \left(-2\right)=2.
$$

## Original q-160440

For the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\operatorname{cos}⁡u \\ \operatorname{sin}⁡v\end{aligned}]
$$

compute the value of the Jacobian determinant at the point where $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}\pi /6 \\ 0\end{aligned}].$

Original choices: $-1$, $0$, $\frac{1}{2}$, $1$, $-\frac{1}{2}$

Original worked solution:
Given a transformation 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y)}{∂(u,v)},$ is given by

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}|.\end{aligned}
$$

Here, we have $x(u,v)=\operatorname{cos}⁡u$ and $y(u,v)=\operatorname{sin}⁡v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =-\operatorname{sin}⁡u & \,\frac{∂x}{∂v} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =\operatorname{cos}⁡v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}-\operatorname{sin}⁡u & 0 \\ 0 & \operatorname{cos}⁡v\end{aligned}| \\  & =(-\operatorname{sin}⁡u)\cdot \operatorname{cos}⁡v-0\cdot 0 \\  & =-\operatorname{sin}⁡u\operatorname{cos}⁡v.\end{aligned}
$$

Finally, when $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}\pi /6 \\ 0\end{aligned}],$ the value of our Jacobian determinant is

$$
{\frac{∂(x,y)}{∂(u,v)}|}_{(\frac{\pi }{6},0)}=-\operatorname{sin}⁡(\frac{\pi }{6})\operatorname{cos}⁡(0)=-\frac{1}{2}.
$$

### Generated source-parameter replay

## Generated easy — diagonal_trig
Review metadata: `observed_diagonal_trig`, `{'a': 1, 'b': 1, 'U': 'pi/6', 'V': '0'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}\cos{\left(u \right)}\\\sin{\left(v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{6}\\0\end{bmatrix}.$

- $\frac{1}{2}$
- $0$
- $-1$
- $- \frac{1}{2}$ **correct**
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

Here, we have $x(u,v)=\cos{\left(u \right)}$ and $y(u,v)=\sin{\left(v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=- \sin{\left(u \right)}&\quad \frac{\partial x}{\partial v}&=0\\\frac{\partial y}{\partial u}&=0&\quad \frac{\partial y}{\partial v}&=\cos{\left(v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}- \sin{\left(u \right)}&0\\0&\cos{\left(v \right)}\end{matrix}\right|\\&=\left(- \sin{\left(u \right)}\right)\cdot\left(\cos{\left(v \right)}\right)-\left(0\right)\cdot\left(0\right)\\&=- \sin{\left(u \right)} \cos{\left(v \right)}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{6}\\0\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(\frac{\pi}{6},0)}=- \sin{\left(\left(\frac{\pi}{6}\right) \right)} \cos{\left(\left(0\right) \right)}=- \frac{1}{2}.
$$

## Original q-160445

For the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}2\operatorname{cos}⁡u \\ -3\operatorname{sin}⁡v\end{aligned}]
$$

compute the value of the Jacobian determinant at the point where $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}\pi /4 \\ \pi /4\end{aligned}].$

Original choices: $3$, $2$, $6$, $4$, $-6$

Original worked solution:
Given a transformation 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y)}{∂(u,v)},$ is given by

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}|.\end{aligned}
$$

Here, we have $x(u,v)=2\operatorname{cos}⁡u$ and $y(u,v)=-3\operatorname{sin}⁡v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =-2\operatorname{sin}⁡u & \,\frac{∂x}{∂v} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =-3\operatorname{cos}⁡v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}-2\operatorname{sin}⁡u & 0 \\ 0 & -3\operatorname{cos}⁡v\end{aligned}| \\  & =(-2\operatorname{sin}⁡u)\cdot (-3\operatorname{cos}⁡v)-0\cdot 0 \\  & =6\operatorname{sin}⁡u\operatorname{cos}⁡v.\end{aligned}
$$

Finally, when $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}\pi /4 \\ \pi /4\end{aligned}],$ the value of our Jacobian determinant is

$$
{\frac{∂(x,y)}{∂(u,v)}|}_{(\frac{\pi }{4},\frac{\pi }{4})}=6\operatorname{sin}⁡(\frac{\pi }{4})\operatorname{cos}⁡(\frac{\pi }{4})=3.
$$

### Generated source-parameter replay

## Generated easy — diagonal_trig
Review metadata: `observed_diagonal_trig_scaled`, `{'a': 2, 'b': -3, 'U': 'pi/4', 'V': 'pi/4'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}2 \cos{\left(u \right)}\\- 3 \sin{\left(v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{4}\\\frac{\pi}{4}\end{bmatrix}.$

- $6$
- $2$
- $3$ **correct**
- $-6$
- $4$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=2 \cos{\left(u \right)}$ and $y(u,v)=- 3 \sin{\left(v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=- 2 \sin{\left(u \right)}&\quad \frac{\partial x}{\partial v}&=0\\\frac{\partial y}{\partial u}&=0&\quad \frac{\partial y}{\partial v}&=- 3 \cos{\left(v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}- 2 \sin{\left(u \right)}&0\\0&- 3 \cos{\left(v \right)}\end{matrix}\right|\\&=\left(- 2 \sin{\left(u \right)}\right)\cdot\left(- 3 \cos{\left(v \right)}\right)-\left(0\right)\cdot\left(0\right)\\&=6 \sin{\left(u \right)} \cos{\left(v \right)}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{4}\\\frac{\pi}{4}\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(\frac{\pi}{4},\frac{\pi}{4})}=6 \sin{\left(\left(\frac{\pi}{4}\right) \right)} \cos{\left(\left(\frac{\pi}{4}\right) \right)}=3.
$$

## Original q-160434

For the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\operatorname{cos}⁡(u+v) \\ \operatorname{sin}⁡(u-v)\end{aligned}]
$$

compute the value of the Jacobian determinant at the point where $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}\pi /4 \\ \pi /4\end{aligned}].$

Original choices: $2$, $1$, $4$, $-1$, $-2$

Original worked solution:
Given a transformation 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y)}{∂(u,v)},$ is given by

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}|.\end{aligned}
$$

Here, we have $x(u,v)=\operatorname{cos}⁡(u+v)$ and $y(u,v)=\operatorname{sin}⁡(u-v).$ 

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =-\operatorname{sin}⁡(u+v) & \,\frac{∂x}{∂v} & =-\operatorname{sin}⁡(u+v) \\ \frac{∂y}{∂u} & =\operatorname{cos}⁡(u-v) & \,\frac{∂y}{∂v} & =-\operatorname{cos}⁡(u-v)\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}-\operatorname{sin}⁡(u+v) & -\operatorname{sin}⁡(u+v) \\ \operatorname{cos}⁡(u-v) & -\operatorname{cos}⁡(u-v)\end{aligned}| \\  & =(-\operatorname{sin}⁡(u+v))\cdot (-\operatorname{cos}⁡(u-v))-(-\operatorname{sin}⁡(u+v))\cdot \operatorname{cos}⁡(u-v) \\  & =\operatorname{sin}⁡(u+v)\operatorname{cos}⁡(u-v)+\operatorname{sin}⁡(u+v)\operatorname{cos}⁡(u-v) \\  & =2\operatorname{sin}⁡(u+v)\operatorname{cos}⁡(u-v).\end{aligned}
$$

Finally, when $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}\pi /4 \\ \pi /4\end{aligned}],$ the value of our Jacobian determinant is 

$$
{\frac{∂(x,y)}{∂(u,v)}|}_{(\frac{\pi }{4},\frac{\pi }{4})}=2\operatorname{sin}⁡(\frac{\pi }{2})\operatorname{cos}⁡(0)=2.
$$

### Generated source-parameter replay

## Generated easy — coupled_trig
Review metadata: `observed_coupled_trig`, `{'a': 1, 'b': 1, 'U': 'pi/4', 'V': 'pi/4'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}\cos{\left(u + v \right)}\\\sin{\left(u - v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{4}\\\frac{\pi}{4}\end{bmatrix}.$

- $4$
- $1$
- $2$ **correct**
- $-2$
- $-1$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=\cos{\left(u + v \right)}$ and $y(u,v)=\sin{\left(u - v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=- \sin{\left(u + v \right)}&\quad \frac{\partial x}{\partial v}&=- \sin{\left(u + v \right)}\\\frac{\partial y}{\partial u}&=\cos{\left(u - v \right)}&\quad \frac{\partial y}{\partial v}&=- \cos{\left(u - v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}- \sin{\left(u + v \right)}&- \sin{\left(u + v \right)}\\\cos{\left(u - v \right)}&- \cos{\left(u - v \right)}\end{matrix}\right|\\&=\left(- \sin{\left(u + v \right)}\right)\cdot\left(- \cos{\left(u - v \right)}\right)-\left(- \sin{\left(u + v \right)}\right)\cdot\left(\cos{\left(u - v \right)}\right)\\&=\sin{\left(u + v \right)} \cos{\left(u - v \right)}-\left(- \sin{\left(u + v \right)} \cos{\left(u - v \right)}\right)\\&=2 \sin{\left(u + v \right)} \cos{\left(u - v \right)}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{4}\\\frac{\pi}{4}\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(\frac{\pi}{4},\frac{\pi}{4})}=2 \sin{\left(\left(\frac{\pi}{4}\right) + \left(\frac{\pi}{4}\right) \right)} \cos{\left(\left(\frac{\pi}{4}\right) - \left(\frac{\pi}{4}\right) \right)}=2.
$$

## Original q-160387

For the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}3{u}^{2}+2v \\ u+2{v}^{2}\end{aligned}].
$$

compute the value of the Jacobian determinant at the point where
$[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}1 \\ 1\end{aligned}].$

Original choices: $20$, $24$, $12$, $22$, $16$

Original worked solution:
Given a transformation 

$$
T:[\begin{aligned}u \\ v\end{aligned}]\to [\begin{aligned}x(u,v) \\ y(u,v)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y)}{∂(u,v)},$ is given by

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}|.\end{aligned}
$$

Here, we have $x(u,v)=3{u}^{2}+2v$ and $y(u,v)=u+2{v}^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =6u & \,\frac{∂x}{∂v} & =2 \\ \frac{∂y}{∂u} & =1 & \,\frac{∂y}{∂v} & =4v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}6u & 2 \\ 1 & 4v\end{aligned}| \\  & =6u\cdot 4v-2\cdot 1 \\  & =24uv-2.\end{aligned}
$$

Finally, when $[\begin{aligned}u \\ v\end{aligned}]=[\begin{aligned}1 \\ 1\end{aligned}],$ the value of our Jacobian determinant is

$$
{\frac{∂(x,y)}{∂(u,v)}|}_{(1,1)}=24(1)(1)-2=22.
$$

### Generated source-parameter replay

## Generated easy — quadratic_linear
Review metadata: `observed_quadratic_linear`, `{'a': 3, 'b': 2, 'c': 1, 'd': 2, 'U': '1', 'V': '1'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}3 u^{2} + 2 v\\u + 2 v^{2}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\1\end{bmatrix}.$

- $12$
- $24$
- $20$
- $16$
- $22$ **correct**

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=3 u^{2} + 2 v$ and $y(u,v)=u + 2 v^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=6 u&\quad \frac{\partial x}{\partial v}&=2\\\frac{\partial y}{\partial u}&=1&\quad \frac{\partial y}{\partial v}&=4 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}6 u&2\\1&4 v\end{matrix}\right|\\&=\left(6 u\right)\cdot\left(4 v\right)-\left(2\right)\cdot\left(1\right)\\&=2 \left(12 u v - 1\right).\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\1\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,1)}=24 \left(1\right) \left(1\right) - 2=22.
$$

# Clearly labeled generated variants

## Generated easy — polar
Review metadata: `observed_polar`, `{'a': 5, 'b': 4, 'U': '1', 'V': '2'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u \cos{\left(v \right)}\\4 u \sin{\left(v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix}.$

- $0$
- $40$
- $\frac{40}{3}$
- $\frac{80}{3}$
- $20$ **correct**

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

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,2)}=20 \left(1\right)=20.
$$

## Generated easy — polar
Review metadata: `observed_polar`, `{'a': 5, 'b': 1, 'U': '2', 'V': '1'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u \cos{\left(v \right)}\\u \sin{\left(v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix}.$

- $\frac{40}{3}$
- $20$
- $\frac{20}{3}$
- $0$
- $10$ **correct**

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

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(2,1)}=5 \left(2\right)=10.
$$

## Generated easy — exp_pair
Review metadata: `observed_exp_pair`, `{'a': 5, 'b': 4, 'U': '0', 'V': '2'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}e^{5 u + 4 v}\\e^{5 u - 4 v}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}0\\2\end{bmatrix}.$

- $60$
- $-20$
- $-40$ **correct**
- $20$
- $-60$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=e^{5 u + 4 v}$ and $y(u,v)=e^{5 u - 4 v}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 e^{5 u + 4 v}&\quad \frac{\partial x}{\partial v}&=4 e^{5 u + 4 v}\\\frac{\partial y}{\partial u}&=5 e^{5 u - 4 v}&\quad \frac{\partial y}{\partial v}&=- 4 e^{5 u - 4 v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 e^{5 u + 4 v}&4 e^{5 u + 4 v}\\5 e^{5 u - 4 v}&- 4 e^{5 u - 4 v}\end{matrix}\right|\\&=\left(5 e^{5 u + 4 v}\right)\cdot\left(- 4 e^{5 u - 4 v}\right)-\left(4 e^{5 u + 4 v}\right)\cdot\left(5 e^{5 u - 4 v}\right)\\&=- 20 e^{5 u - 4 v} e^{5 u + 4 v}-\left(20 e^{5 u - 4 v} e^{5 u + 4 v}\right)\\&=- 40 e^{10 u}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}0\\2\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(0,2)}=- 40 e^{10 \left(0\right)}=-40.
$$

## Generated easy — exp_pair
Review metadata: `observed_exp_pair`, `{'a': 5, 'b': 1, 'U': '0', 'V': '1'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}e^{5 u + v}\\e^{5 u - v}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}0\\1\end{bmatrix}.$

- $5$
- $-5$
- $-10$ **correct**
- $15$
- $-15$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=e^{5 u + v}$ and $y(u,v)=e^{5 u - v}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 e^{5 u + v}&\quad \frac{\partial x}{\partial v}&=e^{5 u + v}\\\frac{\partial y}{\partial u}&=5 e^{5 u - v}&\quad \frac{\partial y}{\partial v}&=- e^{5 u - v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 e^{5 u + v}&e^{5 u + v}\\5 e^{5 u - v}&- e^{5 u - v}\end{matrix}\right|\\&=\left(5 e^{5 u + v}\right)\cdot\left(- e^{5 u - v}\right)-\left(e^{5 u + v}\right)\cdot\left(5 e^{5 u - v}\right)\\&=- 5 e^{5 u - v} e^{5 u + v}-\left(5 e^{5 u - v} e^{5 u + v}\right)\\&=- 10 e^{10 u}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}0\\1\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(0,1)}=- 10 e^{10 \left(0\right)}=-10.
$$

## Generated easy — quotient
Review metadata: `observed_quotient`, `{'a': 5, 'b': 4, 'U': '1', 'V': '2'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u v\\\frac{4 v}{u}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix}.$

- $\frac{320}{3}$
- $-80$
- $80$ **correct**
- $- \frac{80}{3}$
- $- \frac{160}{3}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u v$ and $y(u,v)=\frac{4 v}{u}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 v&\quad \frac{\partial x}{\partial v}&=5 u\\\frac{\partial y}{\partial u}&=- \frac{4 v}{u^{2}}&\quad \frac{\partial y}{\partial v}&=\frac{4}{u}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 v&5 u\\- \frac{4 v}{u^{2}}&\frac{4}{u}\end{matrix}\right|\\&=\left(5 v\right)\cdot\left(\frac{4}{u}\right)-\left(5 u\right)\cdot\left(- \frac{4 v}{u^{2}}\right)\\&=\frac{40 v}{u}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,2)}=\frac{40 \left(2\right)}{\left(1\right)}=80.
$$

## Generated easy — quotient
Review metadata: `observed_quotient`, `{'a': 5, 'b': 1, 'U': '2', 'V': '1'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u v\\\frac{v}{u}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix}.$

- $- \frac{5}{3}$
- $-5$
- $5$ **correct**
- $\frac{20}{3}$
- $- \frac{10}{3}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u v$ and $y(u,v)=\frac{v}{u}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 v&\quad \frac{\partial x}{\partial v}&=5 u\\\frac{\partial y}{\partial u}&=- \frac{v}{u^{2}}&\quad \frac{\partial y}{\partial v}&=\frac{1}{u}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 v&5 u\\- \frac{v}{u^{2}}&\frac{1}{u}\end{matrix}\right|\\&=\left(5 v\right)\cdot\left(\frac{1}{u}\right)-\left(5 u\right)\cdot\left(- \frac{v}{u^{2}}\right)\\&=\frac{10 v}{u}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(2,1)}=\frac{10 \left(1\right)}{\left(2\right)}=5.
$$

## Generated easy — exp_log
Review metadata: `observed_exp_log`, `{'a': 2, 'b': 5, 'U': '5', 'V': '2'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}e^{2 u - 5 v}\\\log{\left(u v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}5\\2\end{bmatrix}.$

- $2$ **correct**
- $1$
- $0$
- $3$
- $-1$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=e^{2 u - 5 v}$ and $y(u,v)=\log{\left(u v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=2 e^{2 u - 5 v}&\quad \frac{\partial x}{\partial v}&=- 5 e^{2 u - 5 v}\\\frac{\partial y}{\partial u}&=\frac{1}{u}&\quad \frac{\partial y}{\partial v}&=\frac{1}{v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}2 e^{2 u - 5 v}&- 5 e^{2 u - 5 v}\\\frac{1}{u}&\frac{1}{v}\end{matrix}\right|\\&=\left(2 e^{2 u - 5 v}\right)\cdot\left(\frac{1}{v}\right)-\left(- 5 e^{2 u - 5 v}\right)\cdot\left(\frac{1}{u}\right)\\&=\frac{\left(2 u + 5 v\right) e^{2 u} e^{- 5 v}}{u v}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}5\\2\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(5,2)}=\frac{\left(2 \left(5\right) + 5 \left(2\right)\right) e^{2 \left(5\right)} e^{- 5 \left(2\right)}}{\left(5\right) \left(2\right)}=2.
$$

## Generated easy — exp_log
Review metadata: `observed_exp_log`, `{'a': 5, 'b': 1, 'U': '1', 'V': '5'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}e^{5 u - v}\\\log{\left(u v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\5\end{bmatrix}.$

- $3$
- $1$
- $0$
- $2$ **correct**
- $-1$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=e^{5 u - v}$ and $y(u,v)=\log{\left(u v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 e^{5 u - v}&\quad \frac{\partial x}{\partial v}&=- e^{5 u - v}\\\frac{\partial y}{\partial u}&=\frac{1}{u}&\quad \frac{\partial y}{\partial v}&=\frac{1}{v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 e^{5 u - v}&- e^{5 u - v}\\\frac{1}{u}&\frac{1}{v}\end{matrix}\right|\\&=\left(5 e^{5 u - v}\right)\cdot\left(\frac{1}{v}\right)-\left(- e^{5 u - v}\right)\cdot\left(\frac{1}{u}\right)\\&=\frac{\left(5 u + v\right) e^{5 u} e^{- v}}{u v}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\5\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,5)}=\frac{\left(5 \left(1\right) + \left(5\right)\right) e^{5 \left(1\right)} e^{- \left(5\right)}}{\left(1\right) \left(5\right)}=2.
$$

## Generated easy — square_pair
Review metadata: `observed_square_pair`, `{'a': 5, 'b': 4, 'U': '1', 'V': '2'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u^{2} + 4 v^{2}\\5 u^{2} - 4 v^{2}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix}.$

- $-320$ **correct**
- $-280$
- $160$
- $-240$
- $-360$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u^{2} + 4 v^{2}$ and $y(u,v)=5 u^{2} - 4 v^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=10 u&\quad \frac{\partial x}{\partial v}&=8 v\\\frac{\partial y}{\partial u}&=10 u&\quad \frac{\partial y}{\partial v}&=- 8 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}10 u&8 v\\10 u&- 8 v\end{matrix}\right|\\&=\left(10 u\right)\cdot\left(- 8 v\right)-\left(8 v\right)\cdot\left(10 u\right)\\&=- 80 u v-\left(80 u v\right)\\&=- 160 u v.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,2)}=- 160 \left(1\right) \left(2\right)=-320.
$$

## Generated easy — square_pair
Review metadata: `observed_square_pair`, `{'a': 5, 'b': 1, 'U': '2', 'V': '1'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u^{2} + v^{2}\\5 u^{2} - v^{2}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix}.$

- $-60$
- $-70$
- $40$
- $-80$ **correct**
- $-90$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u^{2} + v^{2}$ and $y(u,v)=5 u^{2} - v^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=10 u&\quad \frac{\partial x}{\partial v}&=2 v\\\frac{\partial y}{\partial u}&=10 u&\quad \frac{\partial y}{\partial v}&=- 2 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}10 u&2 v\\10 u&- 2 v\end{matrix}\right|\\&=\left(10 u\right)\cdot\left(- 2 v\right)-\left(2 v\right)\cdot\left(10 u\right)\\&=- 20 u v-\left(20 u v\right)\\&=- 40 u v.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(2,1)}=- 40 \left(2\right) \left(1\right)=-80.
$$

## Generated easy — complex_square
Review metadata: `observed_complex_square`, `{'a': 5, 'b': 4, 'U': '1', 'V': '2'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}\frac{5 u^{2}}{2} - \frac{5 v^{2}}{2}\\4 u v\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix}.$

- $100$ **correct**
- $40$
- $-40$
- $60$
- $160$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=\frac{5 u^{2}}{2} - \frac{5 v^{2}}{2}$ and $y(u,v)=4 u v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 u&\quad \frac{\partial x}{\partial v}&=- 5 v\\\frac{\partial y}{\partial u}&=4 v&\quad \frac{\partial y}{\partial v}&=4 u\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 u&- 5 v\\4 v&4 u\end{matrix}\right|\\&=\left(5 u\right)\cdot\left(4 u\right)-\left(- 5 v\right)\cdot\left(4 v\right)\\&=20 \left(u^{2} + v^{2}\right).\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,2)}=20 \left(1\right)^{2} + 20 \left(2\right)^{2}=100.
$$

## Generated easy — complex_square
Review metadata: `observed_complex_square`, `{'a': 5, 'b': 1, 'U': '2', 'V': '1'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}\frac{5 u^{2}}{2} - \frac{5 v^{2}}{2}\\u v\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix}.$

- $15$
- $10$
- $-10$
- $25$ **correct**
- $40$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=\frac{5 u^{2}}{2} - \frac{5 v^{2}}{2}$ and $y(u,v)=u v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 u&\quad \frac{\partial x}{\partial v}&=- 5 v\\\frac{\partial y}{\partial u}&=v&\quad \frac{\partial y}{\partial v}&=u\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 u&- 5 v\\v&u\end{matrix}\right|\\&=\left(5 u\right)\cdot\left(u\right)-\left(- 5 v\right)\cdot\left(v\right)\\&=5 \left(u^{2} + v^{2}\right).\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(2,1)}=5 \left(2\right)^{2} + 5 \left(1\right)^{2}=25.
$$

## Generated easy — mixed_linear
Review metadata: `observed_mixed_linear`, `{'a': 5, 'b': 4, 'U': '1', 'V': '2'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}4 u v + 5 v^{2}\\- u + v\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix}.$

- $64$
- $16$
- $96$
- $32$ **correct**
- $48$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=4 u v + 5 v^{2}$ and $y(u,v)=- u + v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=4 v&\quad \frac{\partial x}{\partial v}&=4 u + 10 v\\\frac{\partial y}{\partial u}&=-1&\quad \frac{\partial y}{\partial v}&=1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}4 v&4 u + 10 v\\-1&1\end{matrix}\right|\\&=\left(4 v\right)\cdot\left(1\right)-\left(4 u + 10 v\right)\cdot\left(-1\right)\\&=4 v-\left(- 4 u - 10 v\right)\\&=2 \left(2 u + 7 v\right).\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,2)}=4 \left(1\right) + 14 \left(2\right)=32.
$$

## Generated easy — mixed_linear
Review metadata: `observed_mixed_linear`, `{'a': 5, 'b': 1, 'U': '2', 'V': '1'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}u v + 5 v^{2}\\- u + v\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix}.$

- $13$ **correct**
- $\frac{13}{2}$
- $39$
- $26$
- $\frac{39}{2}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=u v + 5 v^{2}$ and $y(u,v)=- u + v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=v&\quad \frac{\partial x}{\partial v}&=u + 10 v\\\frac{\partial y}{\partial u}&=-1&\quad \frac{\partial y}{\partial v}&=1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}v&u + 10 v\\-1&1\end{matrix}\right|\\&=\left(v\right)\cdot\left(1\right)-\left(u + 10 v\right)\cdot\left(-1\right)\\&=v-\left(- u - 10 v\right)\\&=u + 11 v.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(2,1)}=\left(2\right) + 11 \left(1\right)=13.
$$

## Generated easy — diagonal_trig
Review metadata: `observed_diagonal_trig`, `{'a': 5, 'b': 4, 'U': 'pi/3', 'V': 'pi/4'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 \cos{\left(u \right)}\\4 \sin{\left(v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{3}\\\frac{\pi}{4}\end{bmatrix}.$

- $- 10 \sqrt{6}$
- $5 \sqrt{6}$
- $0$
- $10 \sqrt{6}$
- $- 5 \sqrt{6}$ **correct**

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 \cos{\left(u \right)}$ and $y(u,v)=4 \sin{\left(v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=- 5 \sin{\left(u \right)}&\quad \frac{\partial x}{\partial v}&=0\\\frac{\partial y}{\partial u}&=0&\quad \frac{\partial y}{\partial v}&=4 \cos{\left(v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}- 5 \sin{\left(u \right)}&0\\0&4 \cos{\left(v \right)}\end{matrix}\right|\\&=\left(- 5 \sin{\left(u \right)}\right)\cdot\left(4 \cos{\left(v \right)}\right)-\left(0\right)\cdot\left(0\right)\\&=- 20 \sin{\left(u \right)} \cos{\left(v \right)}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{3}\\\frac{\pi}{4}\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(\frac{\pi}{3},\frac{\pi}{4})}=- 20 \sin{\left(\left(\frac{\pi}{3}\right) \right)} \cos{\left(\left(\frac{\pi}{4}\right) \right)}=- 5 \sqrt{6}.
$$

## Generated easy — diagonal_trig
Review metadata: `observed_diagonal_trig`, `{'a': 5, 'b': 1, 'U': 'pi/3', 'V': 'pi/4'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 \cos{\left(u \right)}\\\sin{\left(v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{3}\\\frac{\pi}{4}\end{bmatrix}.$

- $\frac{5 \sqrt{6}}{2}$
- $\frac{5 \sqrt{6}}{4}$
- $0$
- $- \frac{5 \sqrt{6}}{2}$
- $- \frac{5 \sqrt{6}}{4}$ **correct**

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 \cos{\left(u \right)}$ and $y(u,v)=\sin{\left(v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=- 5 \sin{\left(u \right)}&\quad \frac{\partial x}{\partial v}&=0\\\frac{\partial y}{\partial u}&=0&\quad \frac{\partial y}{\partial v}&=\cos{\left(v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}- 5 \sin{\left(u \right)}&0\\0&\cos{\left(v \right)}\end{matrix}\right|\\&=\left(- 5 \sin{\left(u \right)}\right)\cdot\left(\cos{\left(v \right)}\right)-\left(0\right)\cdot\left(0\right)\\&=- 5 \sin{\left(u \right)} \cos{\left(v \right)}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{3}\\\frac{\pi}{4}\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(\frac{\pi}{3},\frac{\pi}{4})}=- 5 \sin{\left(\left(\frac{\pi}{3}\right) \right)} \cos{\left(\left(\frac{\pi}{4}\right) \right)}=- \frac{5 \sqrt{6}}{4}.
$$

## Generated easy — diagonal_trig
Review metadata: `observed_diagonal_trig_scaled`, `{'a': 5, 'b': 4, 'U': 'pi/3', 'V': 'pi/4'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 \cos{\left(u \right)}\\4 \sin{\left(v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{3}\\\frac{\pi}{4}\end{bmatrix}.$

- $- 5 \sqrt{6}$ **correct**
- $- 10 \sqrt{6}$
- $- \frac{10 \sqrt{6}}{3}$
- $- \frac{20 \sqrt{6}}{3}$
- $10 \sqrt{6}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 \cos{\left(u \right)}$ and $y(u,v)=4 \sin{\left(v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=- 5 \sin{\left(u \right)}&\quad \frac{\partial x}{\partial v}&=0\\\frac{\partial y}{\partial u}&=0&\quad \frac{\partial y}{\partial v}&=4 \cos{\left(v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}- 5 \sin{\left(u \right)}&0\\0&4 \cos{\left(v \right)}\end{matrix}\right|\\&=\left(- 5 \sin{\left(u \right)}\right)\cdot\left(4 \cos{\left(v \right)}\right)-\left(0\right)\cdot\left(0\right)\\&=- 20 \sin{\left(u \right)} \cos{\left(v \right)}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{3}\\\frac{\pi}{4}\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(\frac{\pi}{3},\frac{\pi}{4})}=- 20 \sin{\left(\left(\frac{\pi}{3}\right) \right)} \cos{\left(\left(\frac{\pi}{4}\right) \right)}=- 5 \sqrt{6}.
$$

## Generated easy — diagonal_trig
Review metadata: `observed_diagonal_trig_scaled`, `{'a': 5, 'b': 1, 'U': 'pi/3', 'V': 'pi/4'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 \cos{\left(u \right)}\\\sin{\left(v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{3}\\\frac{\pi}{4}\end{bmatrix}.$

- $- \frac{5 \sqrt{6}}{3}$
- $- \frac{5 \sqrt{6}}{2}$
- $- \frac{5 \sqrt{6}}{6}$
- $- \frac{5 \sqrt{6}}{4}$ **correct**
- $\frac{5 \sqrt{6}}{2}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 \cos{\left(u \right)}$ and $y(u,v)=\sin{\left(v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=- 5 \sin{\left(u \right)}&\quad \frac{\partial x}{\partial v}&=0\\\frac{\partial y}{\partial u}&=0&\quad \frac{\partial y}{\partial v}&=\cos{\left(v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}- 5 \sin{\left(u \right)}&0\\0&\cos{\left(v \right)}\end{matrix}\right|\\&=\left(- 5 \sin{\left(u \right)}\right)\cdot\left(\cos{\left(v \right)}\right)-\left(0\right)\cdot\left(0\right)\\&=- 5 \sin{\left(u \right)} \cos{\left(v \right)}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{3}\\\frac{\pi}{4}\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(\frac{\pi}{3},\frac{\pi}{4})}=- 5 \sin{\left(\left(\frac{\pi}{3}\right) \right)} \cos{\left(\left(\frac{\pi}{4}\right) \right)}=- \frac{5 \sqrt{6}}{4}.
$$

## Generated easy — coupled_trig
Review metadata: `observed_coupled_trig`, `{'a': 4, 'b': 2, 'U': '-pi/4', 'V': '0'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}4 \cos{\left(u + v \right)}\\2 \sin{\left(u - v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}- \frac{\pi}{4}\\0\end{bmatrix}.$

- $-8$ **correct**
- $-16$
- $-4$
- $4$
- $8$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=4 \cos{\left(u + v \right)}$ and $y(u,v)=2 \sin{\left(u - v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=- 4 \sin{\left(u + v \right)}&\quad \frac{\partial x}{\partial v}&=- 4 \sin{\left(u + v \right)}\\\frac{\partial y}{\partial u}&=2 \cos{\left(u - v \right)}&\quad \frac{\partial y}{\partial v}&=- 2 \cos{\left(u - v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}- 4 \sin{\left(u + v \right)}&- 4 \sin{\left(u + v \right)}\\2 \cos{\left(u - v \right)}&- 2 \cos{\left(u - v \right)}\end{matrix}\right|\\&=\left(- 4 \sin{\left(u + v \right)}\right)\cdot\left(- 2 \cos{\left(u - v \right)}\right)-\left(- 4 \sin{\left(u + v \right)}\right)\cdot\left(2 \cos{\left(u - v \right)}\right)\\&=8 \sin{\left(u + v \right)} \cos{\left(u - v \right)}-\left(- 8 \sin{\left(u + v \right)} \cos{\left(u - v \right)}\right)\\&=16 \sin{\left(u + v \right)} \cos{\left(u - v \right)}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}- \frac{\pi}{4}\\0\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(- \frac{\pi}{4},0)}=16 \sin{\left(\left(- \frac{\pi}{4}\right) + \left(0\right) \right)} \cos{\left(\left(- \frac{\pi}{4}\right) - \left(0\right) \right)}=-8.
$$

## Generated easy — coupled_trig
Review metadata: `observed_coupled_trig`, `{'a': 4, 'b': 1, 'U': 'pi/6', 'V': '0'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}4 \cos{\left(u + v \right)}\\\sin{\left(u - v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{6}\\0\end{bmatrix}.$

- $- \sqrt{3}$
- $4 \sqrt{3}$
- $\sqrt{3}$
- $2 \sqrt{3}$ **correct**
- $- 2 \sqrt{3}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=4 \cos{\left(u + v \right)}$ and $y(u,v)=\sin{\left(u - v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=- 4 \sin{\left(u + v \right)}&\quad \frac{\partial x}{\partial v}&=- 4 \sin{\left(u + v \right)}\\\frac{\partial y}{\partial u}&=\cos{\left(u - v \right)}&\quad \frac{\partial y}{\partial v}&=- \cos{\left(u - v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}- 4 \sin{\left(u + v \right)}&- 4 \sin{\left(u + v \right)}\\\cos{\left(u - v \right)}&- \cos{\left(u - v \right)}\end{matrix}\right|\\&=\left(- 4 \sin{\left(u + v \right)}\right)\cdot\left(- \cos{\left(u - v \right)}\right)-\left(- 4 \sin{\left(u + v \right)}\right)\cdot\left(\cos{\left(u - v \right)}\right)\\&=4 \sin{\left(u + v \right)} \cos{\left(u - v \right)}-\left(- 4 \sin{\left(u + v \right)} \cos{\left(u - v \right)}\right)\\&=8 \sin{\left(u + v \right)} \cos{\left(u - v \right)}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{6}\\0\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(\frac{\pi}{6},0)}=8 \sin{\left(\left(\frac{\pi}{6}\right) + \left(0\right) \right)} \cos{\left(\left(\frac{\pi}{6}\right) - \left(0\right) \right)}=2 \sqrt{3}.
$$

## Generated easy — quadratic_linear
Review metadata: `observed_quadratic_linear`, `{'a': 5, 'b': 4, 'c': 2, 'd': 1, 'U': '1', 'V': '2'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u^{2} + 4 v\\2 u + v^{2}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix}.$

- $\frac{320}{11}$
- $\frac{192}{11}$
- $\frac{384}{11}$
- $32$ **correct**
- $\frac{256}{11}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u^{2} + 4 v$ and $y(u,v)=2 u + v^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=10 u&\quad \frac{\partial x}{\partial v}&=4\\\frac{\partial y}{\partial u}&=2&\quad \frac{\partial y}{\partial v}&=2 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}10 u&4\\2&2 v\end{matrix}\right|\\&=\left(10 u\right)\cdot\left(2 v\right)-\left(4\right)\cdot\left(2\right)\\&=4 \left(5 u v - 2\right).\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,2)}=20 \left(1\right) \left(2\right) - 8=32.
$$

## Generated easy — quadratic_linear
Review metadata: `observed_quadratic_linear`, `{'a': 5, 'b': 1, 'c': 1, 'd': 3, 'U': '2', 'V': '1'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u^{2} + v\\u + 3 v^{2}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix}.$

- $119$ **correct**
- $\frac{714}{11}$
- $\frac{1428}{11}$
- $\frac{1190}{11}$
- $\frac{952}{11}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u^{2} + v$ and $y(u,v)=u + 3 v^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=10 u&\quad \frac{\partial x}{\partial v}&=1\\\frac{\partial y}{\partial u}&=1&\quad \frac{\partial y}{\partial v}&=6 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}10 u&1\\1&6 v\end{matrix}\right|\\&=\left(10 u\right)\cdot\left(6 v\right)-\left(1\right)\cdot\left(1\right)\\&=60 u v - 1.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(2,1)}=60 \left(2\right) \left(1\right) - 1=119.
$$

## Generated easy — polar
Review metadata: `authored_polar`, `{'a': 5, 'b': 4, 'U': '1', 'V': '2'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u \cos{\left(v \right)}\\4 u \sin{\left(v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix}.$

- $20$ **correct**
- $20 \cos^{2}{\left(2 \right)}$
- $-20$
- $5 \cos{\left(2 \right)} + 20 \sin^{2}{\left(2 \right)}$
- $4 \cos{\left(2 \right)} + 20 \sin^{2}{\left(2 \right)}$

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

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,2)}=20 \left(1\right)=20.
$$

## Generated easy — polar
Review metadata: `authored_polar`, `{'a': 5, 'b': 1, 'U': '2', 'V': '1'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u \cos{\left(v \right)}\\u \sin{\left(v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix}.$

- $5 \cos{\left(1 \right)} + 10 \sin^{2}{\left(1 \right)}$
- $10 \cos^{2}{\left(1 \right)}$
- $-10$
- $10$ **correct**
- $2 \cos{\left(1 \right)} + 10 \sin^{2}{\left(1 \right)}$

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

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(2,1)}=5 \left(2\right)=10.
$$

## Generated easy — exp_pair
Review metadata: `authored_exp_pair`, `{'a': 5, 'b': 4, 'U': '0', 'V': '2'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}e^{5 u + 4 v}\\e^{5 u - 4 v}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}0\\2\end{bmatrix}.$

- $-40$ **correct**
- $-20$
- $40$
- $-20 + 5 e^{8}$
- $-20 - \frac{4}{e^{8}}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=e^{5 u + 4 v}$ and $y(u,v)=e^{5 u - 4 v}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 e^{5 u + 4 v}&\quad \frac{\partial x}{\partial v}&=4 e^{5 u + 4 v}\\\frac{\partial y}{\partial u}&=5 e^{5 u - 4 v}&\quad \frac{\partial y}{\partial v}&=- 4 e^{5 u - 4 v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 e^{5 u + 4 v}&4 e^{5 u + 4 v}\\5 e^{5 u - 4 v}&- 4 e^{5 u - 4 v}\end{matrix}\right|\\&=\left(5 e^{5 u + 4 v}\right)\cdot\left(- 4 e^{5 u - 4 v}\right)-\left(4 e^{5 u + 4 v}\right)\cdot\left(5 e^{5 u - 4 v}\right)\\&=- 20 e^{5 u - 4 v} e^{5 u + 4 v}-\left(20 e^{5 u - 4 v} e^{5 u + 4 v}\right)\\&=- 40 e^{10 u}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}0\\2\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(0,2)}=- 40 e^{10 \left(0\right)}=-40.
$$

## Generated easy — exp_pair
Review metadata: `authored_exp_pair`, `{'a': 5, 'b': 1, 'U': '0', 'V': '1'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}e^{5 u + v}\\e^{5 u - v}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}0\\1\end{bmatrix}.$

- $-5 + 5 e$
- $-5$
- $10$
- $-10$ **correct**
- $-5 - e^{-1}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=e^{5 u + v}$ and $y(u,v)=e^{5 u - v}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 e^{5 u + v}&\quad \frac{\partial x}{\partial v}&=e^{5 u + v}\\\frac{\partial y}{\partial u}&=5 e^{5 u - v}&\quad \frac{\partial y}{\partial v}&=- e^{5 u - v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 e^{5 u + v}&e^{5 u + v}\\5 e^{5 u - v}&- e^{5 u - v}\end{matrix}\right|\\&=\left(5 e^{5 u + v}\right)\cdot\left(- e^{5 u - v}\right)-\left(e^{5 u + v}\right)\cdot\left(5 e^{5 u - v}\right)\\&=- 5 e^{5 u - v} e^{5 u + v}-\left(5 e^{5 u - v} e^{5 u + v}\right)\\&=- 10 e^{10 u}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}0\\1\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(0,1)}=- 10 e^{10 \left(0\right)}=-10.
$$

## Generated easy — quotient
Review metadata: `authored_quotient`, `{'a': 5, 'b': 4, 'U': '1', 'V': '2'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u v\\\frac{4 v}{u}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix}.$

- $80$ **correct**
- $40$
- $-80$
- $50$
- $44$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u v$ and $y(u,v)=\frac{4 v}{u}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 v&\quad \frac{\partial x}{\partial v}&=5 u\\\frac{\partial y}{\partial u}&=- \frac{4 v}{u^{2}}&\quad \frac{\partial y}{\partial v}&=\frac{4}{u}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 v&5 u\\- \frac{4 v}{u^{2}}&\frac{4}{u}\end{matrix}\right|\\&=\left(5 v\right)\cdot\left(\frac{4}{u}\right)-\left(5 u\right)\cdot\left(- \frac{4 v}{u^{2}}\right)\\&=\frac{40 v}{u}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,2)}=\frac{40 \left(2\right)}{\left(1\right)}=80.
$$

## Generated easy — quotient
Review metadata: `authored_quotient`, `{'a': 5, 'b': 1, 'U': '2', 'V': '1'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u v\\\frac{v}{u}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix}.$

- $\frac{15}{2}$
- $\frac{5}{2}$
- $-5$
- $5$ **correct**
- $3$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u v$ and $y(u,v)=\frac{v}{u}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 v&\quad \frac{\partial x}{\partial v}&=5 u\\\frac{\partial y}{\partial u}&=- \frac{v}{u^{2}}&\quad \frac{\partial y}{\partial v}&=\frac{1}{u}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 v&5 u\\- \frac{v}{u^{2}}&\frac{1}{u}\end{matrix}\right|\\&=\left(5 v\right)\cdot\left(\frac{1}{u}\right)-\left(5 u\right)\cdot\left(- \frac{v}{u^{2}}\right)\\&=\frac{10 v}{u}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(2,1)}=\frac{10 \left(1\right)}{\left(2\right)}=5.
$$

## Generated easy — exp_log
Review metadata: `authored_exp_log`, `{'a': 2, 'b': 5, 'U': '5', 'V': '2'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}e^{2 u - 5 v}\\\log{\left(u v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}5\\2\end{bmatrix}.$

- $2$ **correct**
- $1$
- $-2$
- $3$
- $\frac{3}{2}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=e^{2 u - 5 v}$ and $y(u,v)=\log{\left(u v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=2 e^{2 u - 5 v}&\quad \frac{\partial x}{\partial v}&=- 5 e^{2 u - 5 v}\\\frac{\partial y}{\partial u}&=\frac{1}{u}&\quad \frac{\partial y}{\partial v}&=\frac{1}{v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}2 e^{2 u - 5 v}&- 5 e^{2 u - 5 v}\\\frac{1}{u}&\frac{1}{v}\end{matrix}\right|\\&=\left(2 e^{2 u - 5 v}\right)\cdot\left(\frac{1}{v}\right)-\left(- 5 e^{2 u - 5 v}\right)\cdot\left(\frac{1}{u}\right)\\&=\frac{\left(2 u + 5 v\right) e^{2 u} e^{- 5 v}}{u v}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}5\\2\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(5,2)}=\frac{\left(2 \left(5\right) + 5 \left(2\right)\right) e^{2 \left(5\right)} e^{- 5 \left(2\right)}}{\left(5\right) \left(2\right)}=2.
$$

## Generated easy — exp_log
Review metadata: `authored_exp_log`, `{'a': 5, 'b': 1, 'U': '1', 'V': '5'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}e^{5 u - v}\\\log{\left(u v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\5\end{bmatrix}.$

- $6$
- $1$
- $-2$
- $2$ **correct**
- $\frac{6}{5}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=e^{5 u - v}$ and $y(u,v)=\log{\left(u v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 e^{5 u - v}&\quad \frac{\partial x}{\partial v}&=- e^{5 u - v}\\\frac{\partial y}{\partial u}&=\frac{1}{u}&\quad \frac{\partial y}{\partial v}&=\frac{1}{v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 e^{5 u - v}&- e^{5 u - v}\\\frac{1}{u}&\frac{1}{v}\end{matrix}\right|\\&=\left(5 e^{5 u - v}\right)\cdot\left(\frac{1}{v}\right)-\left(- e^{5 u - v}\right)\cdot\left(\frac{1}{u}\right)\\&=\frac{\left(5 u + v\right) e^{5 u} e^{- v}}{u v}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\5\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,5)}=\frac{\left(5 \left(1\right) + \left(5\right)\right) e^{5 \left(1\right)} e^{- \left(5\right)}}{\left(1\right) \left(5\right)}=2.
$$

## Generated easy — square_pair
Review metadata: `authored_square_pair`, `{'a': 5, 'b': 4, 'U': '1', 'V': '2'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u^{2} + 4 v^{2}\\5 u^{2} - 4 v^{2}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix}.$

- $-320$ **correct**
- $-160$
- $320$
- $-150$
- $-176$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u^{2} + 4 v^{2}$ and $y(u,v)=5 u^{2} - 4 v^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=10 u&\quad \frac{\partial x}{\partial v}&=8 v\\\frac{\partial y}{\partial u}&=10 u&\quad \frac{\partial y}{\partial v}&=- 8 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}10 u&8 v\\10 u&- 8 v\end{matrix}\right|\\&=\left(10 u\right)\cdot\left(- 8 v\right)-\left(8 v\right)\cdot\left(10 u\right)\\&=- 80 u v-\left(80 u v\right)\\&=- 160 u v.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,2)}=- 160 \left(1\right) \left(2\right)=-320.
$$

## Generated easy — square_pair
Review metadata: `authored_square_pair`, `{'a': 5, 'b': 1, 'U': '2', 'V': '1'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u^{2} + v^{2}\\5 u^{2} - v^{2}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix}.$

- $-20$
- $-40$
- $80$
- $-80$ **correct**
- $-42$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u^{2} + v^{2}$ and $y(u,v)=5 u^{2} - v^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=10 u&\quad \frac{\partial x}{\partial v}&=2 v\\\frac{\partial y}{\partial u}&=10 u&\quad \frac{\partial y}{\partial v}&=- 2 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}10 u&2 v\\10 u&- 2 v\end{matrix}\right|\\&=\left(10 u\right)\cdot\left(- 2 v\right)-\left(2 v\right)\cdot\left(10 u\right)\\&=- 20 u v-\left(20 u v\right)\\&=- 40 u v.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(2,1)}=- 40 \left(2\right) \left(1\right)=-80.
$$

## Generated easy — complex_square
Review metadata: `authored_complex_square`, `{'a': 5, 'b': 4, 'U': '1', 'V': '2'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}\frac{5 u^{2}}{2} - \frac{5 v^{2}}{2}\\4 u v\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix}.$

- $100$ **correct**
- $-100$
- $-60$
- $20$
- $80$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=\frac{5 u^{2}}{2} - \frac{5 v^{2}}{2}$ and $y(u,v)=4 u v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 u&\quad \frac{\partial x}{\partial v}&=- 5 v\\\frac{\partial y}{\partial u}&=4 v&\quad \frac{\partial y}{\partial v}&=4 u\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 u&- 5 v\\4 v&4 u\end{matrix}\right|\\&=\left(5 u\right)\cdot\left(4 u\right)-\left(- 5 v\right)\cdot\left(4 v\right)\\&=20 \left(u^{2} + v^{2}\right).\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,2)}=20 \left(1\right)^{2} + 20 \left(2\right)^{2}=100.
$$

## Generated easy — complex_square
Review metadata: `authored_complex_square`, `{'a': 5, 'b': 1, 'U': '2', 'V': '1'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}\frac{5 u^{2}}{2} - \frac{5 v^{2}}{2}\\u v\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix}.$

- $20$
- $-25$
- $15$
- $25$ **correct**
- $5$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=\frac{5 u^{2}}{2} - \frac{5 v^{2}}{2}$ and $y(u,v)=u v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=5 u&\quad \frac{\partial x}{\partial v}&=- 5 v\\\frac{\partial y}{\partial u}&=v&\quad \frac{\partial y}{\partial v}&=u\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}5 u&- 5 v\\v&u\end{matrix}\right|\\&=\left(5 u\right)\cdot\left(u\right)-\left(- 5 v\right)\cdot\left(v\right)\\&=5 \left(u^{2} + v^{2}\right).\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(2,1)}=5 \left(2\right)^{2} + 5 \left(1\right)^{2}=25.
$$

## Generated easy — mixed_linear
Review metadata: `authored_mixed_linear`, `{'a': 5, 'b': 4, 'U': '1', 'V': '2'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}4 u v + 5 v^{2}\\- u + v\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix}.$

- $32$ **correct**
- $-32$
- $-16$
- $8$
- $24$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=4 u v + 5 v^{2}$ and $y(u,v)=- u + v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=4 v&\quad \frac{\partial x}{\partial v}&=4 u + 10 v\\\frac{\partial y}{\partial u}&=-1&\quad \frac{\partial y}{\partial v}&=1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}4 v&4 u + 10 v\\-1&1\end{matrix}\right|\\&=\left(4 v\right)\cdot\left(1\right)-\left(4 u + 10 v\right)\cdot\left(-1\right)\\&=4 v-\left(- 4 u - 10 v\right)\\&=2 \left(2 u + 7 v\right).\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,2)}=4 \left(1\right) + 14 \left(2\right)=32.
$$

## Generated easy — mixed_linear
Review metadata: `authored_mixed_linear`, `{'a': 5, 'b': 1, 'U': '2', 'V': '1'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}u v + 5 v^{2}\\- u + v\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix}.$

- $1$
- $-13$
- $-11$
- $13$ **correct**
- $12$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=u v + 5 v^{2}$ and $y(u,v)=- u + v.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=v&\quad \frac{\partial x}{\partial v}&=u + 10 v\\\frac{\partial y}{\partial u}&=-1&\quad \frac{\partial y}{\partial v}&=1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}v&u + 10 v\\-1&1\end{matrix}\right|\\&=\left(v\right)\cdot\left(1\right)-\left(u + 10 v\right)\cdot\left(-1\right)\\&=v-\left(- u - 10 v\right)\\&=u + 11 v.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(2,1)}=\left(2\right) + 11 \left(1\right)=13.
$$

## Generated easy — diagonal_trig
Review metadata: `authored_diagonal_trig`, `{'a': 3, 'b': 5, 'U': 'pi/6', 'V': '0'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}3 \cos{\left(u \right)}\\5 \sin{\left(v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{6}\\0\end{bmatrix}.$

- $- \frac{15}{2}$ **correct**
- $-15$
- $\frac{15}{2}$
- $\frac{15 \sqrt{3}}{2}$
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

Here, we have $x(u,v)=3 \cos{\left(u \right)}$ and $y(u,v)=5 \sin{\left(v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=- 3 \sin{\left(u \right)}&\quad \frac{\partial x}{\partial v}&=0\\\frac{\partial y}{\partial u}&=0&\quad \frac{\partial y}{\partial v}&=5 \cos{\left(v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}- 3 \sin{\left(u \right)}&0\\0&5 \cos{\left(v \right)}\end{matrix}\right|\\&=\left(- 3 \sin{\left(u \right)}\right)\cdot\left(5 \cos{\left(v \right)}\right)-\left(0\right)\cdot\left(0\right)\\&=- 15 \sin{\left(u \right)} \cos{\left(v \right)}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{6}\\0\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(\frac{\pi}{6},0)}=- 15 \sin{\left(\left(\frac{\pi}{6}\right) \right)} \cos{\left(\left(0\right) \right)}=- \frac{15}{2}.
$$

## Generated easy — diagonal_trig
Review metadata: `authored_diagonal_trig`, `{'a': 1, 'b': 5, 'U': 'pi/3', 'V': '-pi/6'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}\cos{\left(u \right)}\\5 \sin{\left(v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{3}\\- \frac{\pi}{6}\end{bmatrix}.$

- $\frac{5 \sqrt{3}}{4}$
- $-5$
- $\frac{15}{4}$
- $- \frac{15}{4}$ **correct**
- $- \frac{5 \sqrt{3}}{4}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=\cos{\left(u \right)}$ and $y(u,v)=5 \sin{\left(v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=- \sin{\left(u \right)}&\quad \frac{\partial x}{\partial v}&=0\\\frac{\partial y}{\partial u}&=0&\quad \frac{\partial y}{\partial v}&=5 \cos{\left(v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}- \sin{\left(u \right)}&0\\0&5 \cos{\left(v \right)}\end{matrix}\right|\\&=\left(- \sin{\left(u \right)}\right)\cdot\left(5 \cos{\left(v \right)}\right)-\left(0\right)\cdot\left(0\right)\\&=- 5 \sin{\left(u \right)} \cos{\left(v \right)}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{3}\\- \frac{\pi}{6}\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(\frac{\pi}{3},- \frac{\pi}{6})}=- 5 \sin{\left(\left(\frac{\pi}{3}\right) \right)} \cos{\left(\left(- \frac{\pi}{6}\right) \right)}=- \frac{15}{4}.
$$

## Generated easy — coupled_trig
Review metadata: `authored_coupled_trig`, `{'a': 4, 'b': 2, 'U': '-pi/4', 'V': '0'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}4 \cos{\left(u + v \right)}\\2 \sin{\left(u - v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}- \frac{\pi}{4}\\0\end{bmatrix}.$

- $-8$ **correct**
- $-4$
- $8$
- $-4 + 2 \sqrt{2}$
- $-4 - \sqrt{2}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=4 \cos{\left(u + v \right)}$ and $y(u,v)=2 \sin{\left(u - v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=- 4 \sin{\left(u + v \right)}&\quad \frac{\partial x}{\partial v}&=- 4 \sin{\left(u + v \right)}\\\frac{\partial y}{\partial u}&=2 \cos{\left(u - v \right)}&\quad \frac{\partial y}{\partial v}&=- 2 \cos{\left(u - v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}- 4 \sin{\left(u + v \right)}&- 4 \sin{\left(u + v \right)}\\2 \cos{\left(u - v \right)}&- 2 \cos{\left(u - v \right)}\end{matrix}\right|\\&=\left(- 4 \sin{\left(u + v \right)}\right)\cdot\left(- 2 \cos{\left(u - v \right)}\right)-\left(- 4 \sin{\left(u + v \right)}\right)\cdot\left(2 \cos{\left(u - v \right)}\right)\\&=8 \sin{\left(u + v \right)} \cos{\left(u - v \right)}-\left(- 8 \sin{\left(u + v \right)} \cos{\left(u - v \right)}\right)\\&=16 \sin{\left(u + v \right)} \cos{\left(u - v \right)}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}- \frac{\pi}{4}\\0\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(- \frac{\pi}{4},0)}=16 \sin{\left(\left(- \frac{\pi}{4}\right) + \left(0\right) \right)} \cos{\left(\left(- \frac{\pi}{4}\right) - \left(0\right) \right)}=-8.
$$

## Generated easy — coupled_trig
Review metadata: `authored_coupled_trig`, `{'a': 4, 'b': 1, 'U': 'pi/6', 'V': '0'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}4 \cos{\left(u + v \right)}\\\sin{\left(u - v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{6}\\0\end{bmatrix}.$

- $-2 + \sqrt{3}$
- $\sqrt{3}$
- $- 2 \sqrt{3}$
- $2 \sqrt{3}$ **correct**
- $\frac{\sqrt{3}}{2}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=4 \cos{\left(u + v \right)}$ and $y(u,v)=\sin{\left(u - v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=- 4 \sin{\left(u + v \right)}&\quad \frac{\partial x}{\partial v}&=- 4 \sin{\left(u + v \right)}\\\frac{\partial y}{\partial u}&=\cos{\left(u - v \right)}&\quad \frac{\partial y}{\partial v}&=- \cos{\left(u - v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}- 4 \sin{\left(u + v \right)}&- 4 \sin{\left(u + v \right)}\\\cos{\left(u - v \right)}&- \cos{\left(u - v \right)}\end{matrix}\right|\\&=\left(- 4 \sin{\left(u + v \right)}\right)\cdot\left(- \cos{\left(u - v \right)}\right)-\left(- 4 \sin{\left(u + v \right)}\right)\cdot\left(\cos{\left(u - v \right)}\right)\\&=4 \sin{\left(u + v \right)} \cos{\left(u - v \right)}-\left(- 4 \sin{\left(u + v \right)} \cos{\left(u - v \right)}\right)\\&=8 \sin{\left(u + v \right)} \cos{\left(u - v \right)}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{6}\\0\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(\frac{\pi}{6},0)}=8 \sin{\left(\left(\frac{\pi}{6}\right) + \left(0\right) \right)} \cos{\left(\left(\frac{\pi}{6}\right) - \left(0\right) \right)}=2 \sqrt{3}.
$$

## Generated easy — quadratic_linear
Review metadata: `authored_quadratic_linear`, `{'a': 5, 'b': 4, 'c': 2, 'd': 1, 'U': '1', 'V': '2'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u^{2} + 4 v\\2 u + v^{2}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix}.$

- $32$ **correct**
- $-32$
- $48$
- $40$
- $-8$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u^{2} + 4 v$ and $y(u,v)=2 u + v^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=10 u&\quad \frac{\partial x}{\partial v}&=4\\\frac{\partial y}{\partial u}&=2&\quad \frac{\partial y}{\partial v}&=2 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}10 u&4\\2&2 v\end{matrix}\right|\\&=\left(10 u\right)\cdot\left(2 v\right)-\left(4\right)\cdot\left(2\right)\\&=4 \left(5 u v - 2\right).\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,2)}=20 \left(1\right) \left(2\right) - 8=32.
$$

## Generated easy — quadratic_linear
Review metadata: `authored_quadratic_linear`, `{'a': 5, 'b': 1, 'c': 1, 'd': 3, 'U': '2', 'V': '1'}`, observed.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}5 u^{2} + v\\u + 3 v^{2}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix}.$

- $120$
- $-119$
- $121$
- $119$ **correct**
- $-1$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=5 u^{2} + v$ and $y(u,v)=u + 3 v^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=10 u&\quad \frac{\partial x}{\partial v}&=1\\\frac{\partial y}{\partial u}&=1&\quad \frac{\partial y}{\partial v}&=6 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}10 u&1\\1&6 v\end{matrix}\right|\\&=\left(10 u\right)\cdot\left(6 v\right)-\left(1\right)\cdot\left(1\right)\\&=60 u v - 1.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(2,1)}=60 \left(2\right) \left(1\right) - 1=119.
$$

## Generated moderate — scaled_exp_log
Review metadata: `authored_scaled_exp_log`, `{'a': 4, 'b': 3, 'U': '3', 'V': '4'}`, authored missing level.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}e^{4 u - 3 v}\\\log{\left(u v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}3\\4\end{bmatrix}.$

- $2$ **correct**
- $1$
- $-2$
- $5$
- $\frac{5}{4}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=e^{4 u - 3 v}$ and $y(u,v)=\log{\left(u v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=4 e^{4 u - 3 v}&\quad \frac{\partial x}{\partial v}&=- 3 e^{4 u - 3 v}\\\frac{\partial y}{\partial u}&=\frac{1}{u}&\quad \frac{\partial y}{\partial v}&=\frac{1}{v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}4 e^{4 u - 3 v}&- 3 e^{4 u - 3 v}\\\frac{1}{u}&\frac{1}{v}\end{matrix}\right|\\&=\left(4 e^{4 u - 3 v}\right)\cdot\left(\frac{1}{v}\right)-\left(- 3 e^{4 u - 3 v}\right)\cdot\left(\frac{1}{u}\right)\\&=\frac{\left(4 u + 3 v\right) e^{4 u} e^{- 3 v}}{u v}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}3\\4\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(3,4)}=\frac{\left(4 \left(3\right) + 3 \left(4\right)\right) e^{4 \left(3\right)} e^{- 3 \left(4\right)}}{\left(3\right) \left(4\right)}=2.
$$

## Generated moderate — scaled_exp_log
Review metadata: `authored_scaled_exp_log`, `{'a': 2, 'b': 6, 'U': '6', 'V': '2'}`, authored missing level.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}e^{2 u - 6 v}\\\log{\left(u v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}6\\2\end{bmatrix}.$

- $3$
- $1$
- $-2$
- $2$ **correct**
- $\frac{3}{2}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=e^{2 u - 6 v}$ and $y(u,v)=\log{\left(u v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=2 e^{2 u - 6 v}&\quad \frac{\partial x}{\partial v}&=- 6 e^{2 u - 6 v}\\\frac{\partial y}{\partial u}&=\frac{1}{u}&\quad \frac{\partial y}{\partial v}&=\frac{1}{v}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}2 e^{2 u - 6 v}&- 6 e^{2 u - 6 v}\\\frac{1}{u}&\frac{1}{v}\end{matrix}\right|\\&=\left(2 e^{2 u - 6 v}\right)\cdot\left(\frac{1}{v}\right)-\left(- 6 e^{2 u - 6 v}\right)\cdot\left(\frac{1}{u}\right)\\&=\frac{2 \left(u + 3 v\right) e^{2 u} e^{- 6 v}}{u v}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}6\\2\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(6,2)}=\frac{2 \left(\left(6\right) + 3 \left(2\right)\right) e^{2 \left(6\right)} e^{- 6 \left(2\right)}}{\left(6\right) \left(2\right)}=2.
$$

## Generated moderate — scaled_coupled_trig
Review metadata: `authored_scaled_coupled_trig`, `{'a': 3, 'b': 2, 'c': 1, 'd': 2, 'U': 'pi/6', 'V': '0'}`, authored missing level.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}\cos{\left(3 u + 2 v \right)}\\\sin{\left(u - 2 v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{6}\\0\end{bmatrix}.$

- $4 \sqrt{3}$ **correct**
- $3 \sqrt{3}$
- $- 4 \sqrt{3}$
- $-3 + \sqrt{3}$
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

Here, we have $x(u,v)=\cos{\left(3 u + 2 v \right)}$ and $y(u,v)=\sin{\left(u - 2 v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=- 3 \sin{\left(3 u + 2 v \right)}&\quad \frac{\partial x}{\partial v}&=- 2 \sin{\left(3 u + 2 v \right)}\\\frac{\partial y}{\partial u}&=\cos{\left(u - 2 v \right)}&\quad \frac{\partial y}{\partial v}&=- 2 \cos{\left(u - 2 v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}- 3 \sin{\left(3 u + 2 v \right)}&- 2 \sin{\left(3 u + 2 v \right)}\\\cos{\left(u - 2 v \right)}&- 2 \cos{\left(u - 2 v \right)}\end{matrix}\right|\\&=\left(- 3 \sin{\left(3 u + 2 v \right)}\right)\cdot\left(- 2 \cos{\left(u - 2 v \right)}\right)-\left(- 2 \sin{\left(3 u + 2 v \right)}\right)\cdot\left(\cos{\left(u - 2 v \right)}\right)\\&=8 \sin{\left(3 u + 2 v \right)} \cos{\left(u - 2 v \right)}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{6}\\0\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(\frac{\pi}{6},0)}=8 \sin{\left(3 \left(\frac{\pi}{6}\right) + 2 \left(0\right) \right)} \cos{\left(\left(\frac{\pi}{6}\right) - 2 \left(0\right) \right)}=4 \sqrt{3}.
$$

## Generated moderate — scaled_coupled_trig
Review metadata: `authored_scaled_coupled_trig`, `{'a': 1, 'b': 2, 'c': 2, 'd': 3, 'U': 'pi/6', 'V': '0'}`, authored missing level.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}\cos{\left(u + 2 v \right)}\\\sin{\left(2 u - 3 v \right)}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{6}\\0\end{bmatrix}.$

- $\frac{1}{2}$
- $\frac{3}{4}$
- $- \frac{7}{4}$
- $\frac{7}{4}$ **correct**
- $- \frac{1}{2}$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=\cos{\left(u + 2 v \right)}$ and $y(u,v)=\sin{\left(2 u - 3 v \right)}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=- \sin{\left(u + 2 v \right)}&\quad \frac{\partial x}{\partial v}&=- 2 \sin{\left(u + 2 v \right)}\\\frac{\partial y}{\partial u}&=2 \cos{\left(2 u - 3 v \right)}&\quad \frac{\partial y}{\partial v}&=- 3 \cos{\left(2 u - 3 v \right)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}- \sin{\left(u + 2 v \right)}&- 2 \sin{\left(u + 2 v \right)}\\2 \cos{\left(2 u - 3 v \right)}&- 3 \cos{\left(2 u - 3 v \right)}\end{matrix}\right|\\&=\left(- \sin{\left(u + 2 v \right)}\right)\cdot\left(- 3 \cos{\left(2 u - 3 v \right)}\right)-\left(- 2 \sin{\left(u + 2 v \right)}\right)\cdot\left(2 \cos{\left(2 u - 3 v \right)}\right)\\&=7 \sin{\left(u + 2 v \right)} \cos{\left(2 u - 3 v \right)}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}\frac{\pi}{6}\\0\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(\frac{\pi}{6},0)}=7 \sin{\left(\left(\frac{\pi}{6}\right) + 2 \left(0\right) \right)} \cos{\left(2 \left(\frac{\pi}{6}\right) - 3 \left(0\right) \right)}=\frac{7}{4}.
$$

## Generated hard — powers
Review metadata: `authored_powers`, `{'a': 1, 'b': 3, 'm': 2, 'n': 3, 'U': '1', 'V': '2'}`, authored missing level.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}\left(u + v\right)^{2}\\3 \left(u - v\right)^{3}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix}.$

- $-108$ **correct**
- $-54$
- $108$
- $-48$
- $-63$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=\left(u + v\right)^{2}$ and $y(u,v)=3 \left(u - v\right)^{3}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=2 u + 2 v&\quad \frac{\partial x}{\partial v}&=2 u + 2 v\\\frac{\partial y}{\partial u}&=9 \left(u - v\right)^{2}&\quad \frac{\partial y}{\partial v}&=- 9 \left(u - v\right)^{2}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}2 u + 2 v&2 u + 2 v\\9 \left(u - v\right)^{2}&- 9 \left(u - v\right)^{2}\end{matrix}\right|\\&=\left(2 u + 2 v\right)\cdot\left(- 9 \left(u - v\right)^{2}\right)-\left(2 u + 2 v\right)\cdot\left(9 \left(u - v\right)^{2}\right)\\&=- 36 \left(u - v\right)^{2} \left(u + v\right).\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}1\\2\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,2)}=- 36 \left(\left(1\right) - \left(2\right)\right)^{2} \left(\left(1\right) + \left(2\right)\right)=-108.
$$

## Generated hard — powers
Review metadata: `authored_powers`, `{'a': 3, 'b': 2, 'm': 3, 'n': 2, 'U': '2', 'V': '1'}`, authored missing level.

For the transformation $T,$ defined as

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\longrightarrow\begin{bmatrix}3 \left(u + v\right)^{3}\\2 \left(u - v\right)^{2}\end{bmatrix}.
$$

compute the value of the Jacobian determinant at the point where $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix}.$

- $-243$
- $-324$
- $648$
- $-648$ **correct**
- $-328$

Worked solution:
Given a transformation 

$$
T:\begin{bmatrix}u\\v\end{bmatrix}\to\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix},
$$

the Jacobian determinant of $T,$ denoted $\frac{\partial(x,y)}{\partial(u,v)}$, is given by

$$
\frac{\partial(x,y)}{\partial(u,v)}=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|.
$$

Here, we have $x(u,v)=3 \left(u + v\right)^{3}$ and $y(u,v)=2 \left(u - v\right)^{2}.$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{\partial x}{\partial u}&=9 \left(u + v\right)^{2}&\quad \frac{\partial x}{\partial v}&=9 \left(u + v\right)^{2}\\\frac{\partial y}{\partial u}&=4 u - 4 v&\quad \frac{\partial y}{\partial v}&=- 4 u + 4 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)}&=\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\&=\left|\begin{matrix}9 \left(u + v\right)^{2}&9 \left(u + v\right)^{2}\\4 u - 4 v&- 4 u + 4 v\end{matrix}\right|\\&=\left(9 \left(u + v\right)^{2}\right)\cdot\left(- 4 u + 4 v\right)-\left(9 \left(u + v\right)^{2}\right)\cdot\left(4 u - 4 v\right)\\&=- 72 \left(u - v\right) \left(u + v\right)^{2}.\end{aligned}
$$

Finally, when $\begin{bmatrix}u\\v\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix},$ the value of our Jacobian determinant is

$$
\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(2,1)}=- 72 \left(\left(2\right) - \left(1\right)\right) \left(\left(2\right) + \left(1\right)\right)^{2}=-648.
$$
