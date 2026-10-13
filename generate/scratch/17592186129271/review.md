# Direct 3D Jacobian review
All generated records are labeled. Raw source strings remain in source.json. Source math notation is normalized; prose and ordered teaching stages are retained.

## Original — q-39666 (easy)
Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}4v \\ 3{u}^{2}+2\operatorname{cos}⁡(vw) \\ vw\end{aligned}].
$$

- $12uv$
- $-2vw\operatorname{cos}⁡(vw)$
- $4vw$
- $4vw\operatorname{cos}⁡(vw)$
- $-24uv$ **Correct**

**Original worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

Here, we have 

$$
x(u,v,w)=4v,\,y(u,v,w)=3{u}^{2}+2\operatorname{cos}⁡(vw),\,z(u,v,w)=vw.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =0 & \,\frac{∂x}{∂v} & =4 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =6u & \,\frac{∂y}{∂v} & =-2w\operatorname{sin}⁡(vw) & \,\frac{∂y}{∂w} & =-2v\operatorname{sin}⁡(vw) \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =w, & \,\frac{∂z}{∂w} & =v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}0 & 4 & 0 \\ 6u & -2w\operatorname{sin}⁡(vw) & -2v\operatorname{sin}⁡(vw) \\ 0 & w & v\end{aligned}| \\  & =4(-1)^{1+2}|\begin{aligned}6u & -2v\operatorname{sin}⁡(vw) \\ 0 & v\end{aligned}| \\  & =-4(6uv-0) \\  & =-24uv.\end{aligned}
$$

### Generated — easy
Template: `sparse_trig`; bank: `sparse_trig-observed`; evidence-only replay.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}4 v \\ 3 u^{2} + 2 \cos{\left(v w \right)} \\ v w\end{aligned}].
$$

- $4 v w$
- $- 2 v w \cos{\left(v w \right)}$
- $12 u v$
- $- 24 u v$ **Correct**
- $4 v w \cos{\left(v w \right)}$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

Here, we have 

$$
x(u,v,w)=4 v\, y(u,v,w)=3 u^{2} + 2 \cos{\left(v w \right)}\, z(u,v,w)=v w.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =0 & \frac{∂x}{∂v} & =4 & \frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =6 u & \frac{∂y}{∂v} & =- 2 w \sin{\left(v w \right)} & \frac{∂y}{∂w} & =- 2 v \sin{\left(v w \right)} \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =w, & \frac{∂z}{∂w} & =v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}0 & 4 & 0 \\ 6 u & - 2 w \sin{\left(v w \right)} & - 2 v \sin{\left(v w \right)} \\ 0 & w & v\end{aligned}| \\  & =\left(4\right)(-1)^{1+2}|\begin{aligned}6 u & - 2 v \sin{\left(v w \right)} \\ 0 & v\end{aligned}| \\  & =\left(-4\right)\left(6 u v-\left(0\right)\right) \\  & =- 24 u v.\end{aligned}
$$

### Generated — easy
Template: `sparse_trig`; bank: `sparse_trig-observed`; evidence-only replay.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}2 v \\ - 4 u^{2} + \cos{\left(v w \right)} \\ - 2 v w\end{aligned}].
$$

- $- 32 u v$ **Correct**
- $2 v w \cos{\left(v w \right)}$
- $- v w \cos{\left(v w \right)}$
- $- 8 u v$
- $2 v w$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

Here, we have 

$$
x(u,v,w)=2 v\, y(u,v,w)=- 4 u^{2} + \cos{\left(v w \right)}\, z(u,v,w)=- 2 v w.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =0 & \frac{∂x}{∂v} & =2 & \frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =- 8 u & \frac{∂y}{∂v} & =- w \sin{\left(v w \right)} & \frac{∂y}{∂w} & =- v \sin{\left(v w \right)} \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =- 2 w, & \frac{∂z}{∂w} & =- 2 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}0 & 2 & 0 \\ - 8 u & - w \sin{\left(v w \right)} & - v \sin{\left(v w \right)} \\ 0 & - 2 w & - 2 v\end{aligned}| \\  & =\left(2\right)(-1)^{1+2}|\begin{aligned}- 8 u & - v \sin{\left(v w \right)} \\ 0 & - 2 v\end{aligned}| \\  & =\left(-2\right)\left(16 u v-\left(0\right)\right) \\  & =- 32 u v.\end{aligned}
$$

### Generated — easy
Template: `sparse_trig`; bank: `sparse_trig-method`; eligible learner variant.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}3 v \\ u^{2} + 2 \cos{\left(v w \right)} \\ v w\end{aligned}].
$$

- $- 6 u v$ **Correct**
- $- 3 u v$
- $6 u v$
- $- 6 u w$
- $- 2 u v$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

Here, we have 

$$
x(u,v,w)=3 v\, y(u,v,w)=u^{2} + 2 \cos{\left(v w \right)}\, z(u,v,w)=v w.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =0 & \frac{∂x}{∂v} & =3 & \frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =2 u & \frac{∂y}{∂v} & =- 2 w \sin{\left(v w \right)} & \frac{∂y}{∂w} & =- 2 v \sin{\left(v w \right)} \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =w, & \frac{∂z}{∂w} & =v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}0 & 3 & 0 \\ 2 u & - 2 w \sin{\left(v w \right)} & - 2 v \sin{\left(v w \right)} \\ 0 & w & v\end{aligned}| \\  & =\left(3\right)(-1)^{1+2}|\begin{aligned}2 u & - 2 v \sin{\left(v w \right)} \\ 0 & v\end{aligned}| \\  & =\left(-3\right)\left(2 u v-\left(0\right)\right) \\  & =- 6 u v.\end{aligned}
$$

### Generated — easy
Template: `sparse_trig`; bank: `sparse_trig-method`; eligible learner variant.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}- 3 v \\ 3 u^{2} + 2 \cos{\left(v w \right)} \\ 3 v w\end{aligned}].
$$

- $54 u w$
- $54 u v$ **Correct**
- $- 18 u v$
- $27 u v$
- $- 54 u v$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

Here, we have 

$$
x(u,v,w)=- 3 v\, y(u,v,w)=3 u^{2} + 2 \cos{\left(v w \right)}\, z(u,v,w)=3 v w.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =0 & \frac{∂x}{∂v} & =-3 & \frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =6 u & \frac{∂y}{∂v} & =- 2 w \sin{\left(v w \right)} & \frac{∂y}{∂w} & =- 2 v \sin{\left(v w \right)} \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =3 w, & \frac{∂z}{∂w} & =3 v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}0 & -3 & 0 \\ 6 u & - 2 w \sin{\left(v w \right)} & - 2 v \sin{\left(v w \right)} \\ 0 & 3 w & 3 v\end{aligned}| \\  & =\left(-3\right)(-1)^{1+2}|\begin{aligned}6 u & - 2 v \sin{\left(v w \right)} \\ 0 & 3 v\end{aligned}| \\  & =\left(3\right)\left(18 u v-\left(0\right)\right) \\  & =54 u v.\end{aligned}
$$

## Original — q-161793 (easy)
Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u{e}^{w} \\ w-u \\ w{e}^{u}-3v\end{aligned}].
$$

- ${e}^{w}$
- $3{e}^{w}(1+u)$ **Correct**
- $-uw{e}^{u+w}$
- ${e}^{u+v}-3{e}^{w}$
- $3w{e}^{u+v}$

**Original worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

Here, we have 

$$
x(u,v,w)=u{e}^{w},\,y(u,v,w)=w-u,\,z(u,v,w)=w{e}^{u}-3v.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & ={e}^{w} & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =u{e}^{w} \\ \frac{∂y}{∂u} & =-1 & \,\frac{∂y}{∂v} & =0 & \,\frac{∂y}{∂w} & =1 \\ \frac{∂z}{∂u} & =w{e}^{u} & \,\frac{∂z}{∂v} & =-3, & \,\frac{∂z}{∂w} & ={e}^{u}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}{e}^{w} & 0 & u{e}^{w} \\ -1 & 0 & 1 \\ w{e}^{u} & -3 & {e}^{u}\end{aligned}| \\  & =(-3)(-1)^{3+2}|\begin{aligned}{e}^{w} & u{e}^{w} \\ -1 & 1\end{aligned}| \\  & =3({e}^{w}+u{e}^{w}) \\  & =3{e}^{w}(1+u).\end{aligned}
$$

### Generated — easy
Template: `sparse_exp`; bank: `sparse_exp-observed`; evidence-only replay.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u e^{w} \\ - u + w \\ - 3 v + w e^{u}\end{aligned}].
$$

- $- u w e^{u + w}$
- $3 u e^{w} + 3 e^{w}$ **Correct**
- $e^{w}$
- $3 w e^{u + v}$
- $- 3 e^{w} + e^{u + v}$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

Here, we have 

$$
x(u,v,w)=u e^{w}\, y(u,v,w)=- u + w\, z(u,v,w)=- 3 v + w e^{u}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =e^{w} & \frac{∂x}{∂v} & =0 & \frac{∂x}{∂w} & =u e^{w} \\ \frac{∂y}{∂u} & =-1 & \frac{∂y}{∂v} & =0 & \frac{∂y}{∂w} & =1 \\ \frac{∂z}{∂u} & =w e^{u} & \frac{∂z}{∂v} & =-3, & \frac{∂z}{∂w} & =e^{u}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}e^{w} & 0 & u e^{w} \\ -1 & 0 & 1 \\ w e^{u} & -3 & e^{u}\end{aligned}| \\  & =\left(-3\right)(-1)^{3+2}|\begin{aligned}e^{w} & u e^{w} \\ -1 & 1\end{aligned}| \\  & =\left(3\right)\left(e^{w}-\left(- u e^{w}\right)\right) \\  & =3 \left(u + 1\right) e^{w}.\end{aligned}
$$

### Generated — easy
Template: `sparse_exp`; bank: `sparse_exp-observed`; evidence-only replay.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}2 u e^{w} \\ 4 u + w \\ 2 v + w e^{u}\end{aligned}].
$$

- $- 2 w e^{u + v}$
- $2 e^{w} + e^{u + v}$
- $16 u e^{w} - 4 e^{w}$ **Correct**
- $2 e^{w}$
- $- 2 u w e^{u + w}$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

Here, we have 

$$
x(u,v,w)=2 u e^{w}\, y(u,v,w)=4 u + w\, z(u,v,w)=2 v + w e^{u}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2 e^{w} & \frac{∂x}{∂v} & =0 & \frac{∂x}{∂w} & =2 u e^{w} \\ \frac{∂y}{∂u} & =4 & \frac{∂y}{∂v} & =0 & \frac{∂y}{∂w} & =1 \\ \frac{∂z}{∂u} & =w e^{u} & \frac{∂z}{∂v} & =2, & \frac{∂z}{∂w} & =e^{u}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2 e^{w} & 0 & 2 u e^{w} \\ 4 & 0 & 1 \\ w e^{u} & 2 & e^{u}\end{aligned}| \\  & =\left(2\right)(-1)^{3+2}|\begin{aligned}2 e^{w} & 2 u e^{w} \\ 4 & 1\end{aligned}| \\  & =\left(-2\right)\left(2 e^{w}-\left(8 u e^{w}\right)\right) \\  & =4 \left(4 u - 1\right) e^{w}.\end{aligned}
$$

### Generated — easy
Template: `sparse_exp`; bank: `sparse_exp-method`; eligible learner variant.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}- 2 u e^{w} \\ - u - 3 w \\ 4 v + w e^{u}\end{aligned}].
$$

- $8 u e^{w} - 24 e^{w}$ **Correct**
- $- 24 e^{w}$
- $- 8 u e^{w} + 24 e^{w}$
- $8 u e^{w}$
- $- 2 \left(u - 3\right) e^{w}$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

Here, we have 

$$
x(u,v,w)=- 2 u e^{w}\, y(u,v,w)=- u - 3 w\, z(u,v,w)=4 v + w e^{u}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =- 2 e^{w} & \frac{∂x}{∂v} & =0 & \frac{∂x}{∂w} & =- 2 u e^{w} \\ \frac{∂y}{∂u} & =-1 & \frac{∂y}{∂v} & =0 & \frac{∂y}{∂w} & =-3 \\ \frac{∂z}{∂u} & =w e^{u} & \frac{∂z}{∂v} & =4, & \frac{∂z}{∂w} & =e^{u}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}- 2 e^{w} & 0 & - 2 u e^{w} \\ -1 & 0 & -3 \\ w e^{u} & 4 & e^{u}\end{aligned}| \\  & =\left(4\right)(-1)^{3+2}|\begin{aligned}- 2 e^{w} & - 2 u e^{w} \\ -1 & -3\end{aligned}| \\  & =\left(-4\right)\left(6 e^{w}-\left(2 u e^{w}\right)\right) \\  & =8 \left(u - 3\right) e^{w}.\end{aligned}
$$

### Generated — easy
Template: `sparse_exp`; bank: `sparse_exp-method`; eligible learner variant.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}- u e^{w} \\ - u + 3 w \\ 4 v + w e^{u}\end{aligned}].
$$

- $4 u e^{w}$
- $4 u e^{w} + 12 e^{w}$ **Correct**
- $- \left(u + 3\right) e^{w}$
- $12 e^{w}$
- $- 4 u e^{w} - 12 e^{w}$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

Here, we have 

$$
x(u,v,w)=- u e^{w}\, y(u,v,w)=- u + 3 w\, z(u,v,w)=4 v + w e^{u}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =- e^{w} & \frac{∂x}{∂v} & =0 & \frac{∂x}{∂w} & =- u e^{w} \\ \frac{∂y}{∂u} & =-1 & \frac{∂y}{∂v} & =0 & \frac{∂y}{∂w} & =3 \\ \frac{∂z}{∂u} & =w e^{u} & \frac{∂z}{∂v} & =4, & \frac{∂z}{∂w} & =e^{u}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}- e^{w} & 0 & - u e^{w} \\ -1 & 0 & 3 \\ w e^{u} & 4 & e^{u}\end{aligned}| \\  & =\left(4\right)(-1)^{3+2}|\begin{aligned}- e^{w} & - u e^{w} \\ -1 & 3\end{aligned}| \\  & =\left(-4\right)\left(- 3 e^{w}-\left(u e^{w}\right)\right) \\  & =4 \left(u + 3\right) e^{w}.\end{aligned}
$$

## Original — q-161794 (easy)
Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{u}^{2}+{v}^{2} \\ u+3w \\ -v\end{aligned}].
$$

- $2(u-v)$
- $-2u$
- $6u$ **Correct**
- $6u-2v$
- $0$

**Original worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

Here, we have 

$$
x(u,v,w)={u}^{2}+{v}^{2},\,y(u,v,w)=u+3w,\,z(u,v,w)=-v.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2u & \,\frac{∂x}{∂v} & =2v & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =1 & \,\frac{∂y}{∂v} & =0 & \,\frac{∂y}{∂w} & =3 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =-1, & \,\frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2u & 2v & 0 \\ 1 & 0 & 3 \\ 0 & -1 & 0\end{aligned}| \\  & =(-1)(-1)^{3+2}|\begin{aligned}2u & 0 \\ 1 & 3\end{aligned}| \\  & =6u-0 \\  & =6u.\end{aligned}
$$

### Generated — easy
Template: `sparse_square`; bank: `sparse_square-observed`; evidence-only replay.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u^{2} + v^{2} \\ u + 3 w \\ - v\end{aligned}].
$$

- $6 u$ **Correct**
- $- 2 u$
- $2 u - 2 v$
- $0$
- $6 u - 2 v$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

Here, we have 

$$
x(u,v,w)=u^{2} + v^{2}\, y(u,v,w)=u + 3 w\, z(u,v,w)=- v.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2 u & \frac{∂x}{∂v} & =2 v & \frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =1 & \frac{∂y}{∂v} & =0 & \frac{∂y}{∂w} & =3 \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =-1, & \frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2 u & 2 v & 0 \\ 1 & 0 & 3 \\ 0 & -1 & 0\end{aligned}| \\  & =\left(-1\right)(-1)^{3+2}|\begin{aligned}2 u & 0 \\ 1 & 3\end{aligned}| \\  & =\left(6 u-\left(0\right)\right) \\  & =6 u.\end{aligned}
$$

### Generated — easy
Template: `sparse_square`; bank: `sparse_square-observed`; evidence-only replay.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}2 u^{2} - 4 v^{2} \\ u - 2 w \\ v\end{aligned}].
$$

- $0$
- $8 u + 8 v$
- $- 4 u$
- $4 u + 8 v$
- $8 u$ **Correct**

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

Here, we have 

$$
x(u,v,w)=2 u^{2} - 4 v^{2}\, y(u,v,w)=u - 2 w\, z(u,v,w)=v.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =4 u & \frac{∂x}{∂v} & =- 8 v & \frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =1 & \frac{∂y}{∂v} & =0 & \frac{∂y}{∂w} & =-2 \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =1, & \frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}4 u & - 8 v & 0 \\ 1 & 0 & -2 \\ 0 & 1 & 0\end{aligned}| \\  & =\left(1\right)(-1)^{3+2}|\begin{aligned}4 u & 0 \\ 1 & -2\end{aligned}| \\  & =\left(-1\right)\left(- 8 u-\left(0\right)\right) \\  & =8 u.\end{aligned}
$$

### Generated — easy
Template: `sparse_square`; bank: `sparse_square-method`; eligible learner variant.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}3 u^{2} + v^{2} \\ 2 u + 3 w \\ 2 v\end{aligned}].
$$

- $- 36 u$ **Correct**
- $- 12 u$
- $36 u$
- $- 36 v$
- $0$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

Here, we have 

$$
x(u,v,w)=3 u^{2} + v^{2}\, y(u,v,w)=2 u + 3 w\, z(u,v,w)=2 v.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =6 u & \frac{∂x}{∂v} & =2 v & \frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =2 & \frac{∂y}{∂v} & =0 & \frac{∂y}{∂w} & =3 \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =2, & \frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}6 u & 2 v & 0 \\ 2 & 0 & 3 \\ 0 & 2 & 0\end{aligned}| \\  & =\left(2\right)(-1)^{3+2}|\begin{aligned}6 u & 0 \\ 2 & 3\end{aligned}| \\  & =\left(-2\right)\left(18 u-\left(0\right)\right) \\  & =- 36 u.\end{aligned}
$$

### Generated — easy
Template: `sparse_square`; bank: `sparse_square-method`; eligible learner variant.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}- u^{2} + v^{2} \\ 3 u - 4 w \\ v\end{aligned}].
$$

- $- 8 v$
- $- 8 u$ **Correct**
- $0$
- $2 u$
- $8 u$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

Here, we have 

$$
x(u,v,w)=- u^{2} + v^{2}\, y(u,v,w)=3 u - 4 w\, z(u,v,w)=v.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =- 2 u & \frac{∂x}{∂v} & =2 v & \frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =3 & \frac{∂y}{∂v} & =0 & \frac{∂y}{∂w} & =-4 \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =1, & \frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}- 2 u & 2 v & 0 \\ 3 & 0 & -4 \\ 0 & 1 & 0\end{aligned}| \\  & =\left(1\right)(-1)^{3+2}|\begin{aligned}- 2 u & 0 \\ 3 & -4\end{aligned}| \\  & =\left(-1\right)\left(8 u-\left(0\right)\right) \\  & =- 8 u.\end{aligned}
$$

## Original — q-161796 (easy)
Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}\operatorname{ln}⁡(u\,v\,w) \\ u+2w \\ uv\end{aligned}].
$$

- $\frac{1}{w}$
- $-\frac{uv}{w}$
- $0$
- $\frac{u}{w}-\frac{1}{v}$
- $\frac{u}{w}$ **Correct**

**Original worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

Here, we have 

$$
x(u,v,w)=\operatorname{ln}⁡(u\,v\,w),\,y(u,v,w)=u+2w,\,z(u,v,w)=uv.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =\frac{1}{u} & \,\frac{∂x}{∂v} & =\frac{1}{v} & \,\frac{∂x}{∂w} & =\frac{1}{w} \\ \frac{∂y}{∂u} & =1 & \,\frac{∂y}{∂v} & =0 & \,\frac{∂y}{∂w} & =2 \\ \frac{∂z}{∂u} & =v & \,\frac{∂z}{∂v} & =u & \,\frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{1}{u} & \frac{1}{v} & \frac{1}{w} \\ 1 & 0 & 2 \\ v & u & 0\end{aligned}| \\  & =\frac{1}{w}(-1)^{1+3}|\begin{aligned}1 & 0 \\ v & u\end{aligned}|+2(-1)^{2+3}|\begin{aligned}\frac{1}{u} & \frac{1}{v} \\ v & u\end{aligned}| \\  & =\frac{1}{w}(u-0)-2(1-1) \\  & =\frac{u}{w}.\end{aligned}
$$

### Generated — easy
Template: `log_product`; bank: `log_product-observed`; evidence-only replay.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}\ln{\left(u v w \right)} \\ u + 2 w \\ u v\end{aligned}].
$$

- $0$
- $- \frac{u v}{w}$
- $\frac{1}{w}$
- $\frac{u}{w}$ **Correct**
- $\frac{u}{w} - \frac{1}{v}$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

Here, we have 

$$
x(u,v,w)=\ln{\left(u v w \right)}\, y(u,v,w)=u + 2 w\, z(u,v,w)=u v.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =\frac{1}{u} & \frac{∂x}{∂v} & =\frac{1}{v} & \frac{∂x}{∂w} & =\frac{1}{w} \\ \frac{∂y}{∂u} & =1 & \frac{∂y}{∂v} & =0 & \frac{∂y}{∂w} & =2 \\ \frac{∂z}{∂u} & =v & \frac{∂z}{∂v} & =u, & \frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{1}{u} & \frac{1}{v} & \frac{1}{w} \\ 1 & 0 & 2 \\ v & u & 0\end{aligned}| \\  & =\left(\frac{1}{w}\right)(-1)^{1+3}|\begin{aligned}1 & 0 \\ v & u\end{aligned}|+\left(2\right)(-1)^{2+3}|\begin{aligned}\frac{1}{u} & \frac{1}{v} \\ v & u\end{aligned}| \\  & =\left(\frac{1}{w}\right)\left(u-\left(0\right)\right)+\left(-2\right)\left(1-\left(1\right)\right) \\  & =\frac{u}{w}.\end{aligned}
$$

### Generated — easy
Template: `log_product`; bank: `log_product-observed`; evidence-only replay.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}2 \ln{\left(u v w \right)} \\ - 4 u + w \\ - 2 u v\end{aligned}].
$$

- $\frac{16 u}{w}$ **Correct**
- $\frac{16 u}{w} - \frac{2}{v}$
- $- \frac{16 u v}{w}$
- $\frac{2}{w}$
- $0$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

Here, we have 

$$
x(u,v,w)=2 \ln{\left(u v w \right)}\, y(u,v,w)=- 4 u + w\, z(u,v,w)=- 2 u v.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =\frac{2}{u} & \frac{∂x}{∂v} & =\frac{2}{v} & \frac{∂x}{∂w} & =\frac{2}{w} \\ \frac{∂y}{∂u} & =-4 & \frac{∂y}{∂v} & =0 & \frac{∂y}{∂w} & =1 \\ \frac{∂z}{∂u} & =- 2 v & \frac{∂z}{∂v} & =- 2 u, & \frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{2}{u} & \frac{2}{v} & \frac{2}{w} \\ -4 & 0 & 1 \\ - 2 v & - 2 u & 0\end{aligned}| \\  & =\left(\frac{2}{w}\right)(-1)^{1+3}|\begin{aligned}-4 & 0 \\ - 2 v & - 2 u\end{aligned}|+\left(1\right)(-1)^{2+3}|\begin{aligned}\frac{2}{u} & \frac{2}{v} \\ - 2 v & - 2 u\end{aligned}| \\  & =\left(\frac{2}{w}\right)\left(8 u-\left(0\right)\right)+\left(-1\right)\left(-4-\left(-4\right)\right) \\  & =\frac{16 u}{w}.\end{aligned}
$$

### Generated — easy
Template: `log_product`; bank: `log_product-method`; eligible learner variant.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}3 \ln{\left(u v w \right)} \\ u + 2 w \\ u v\end{aligned}].
$$

- $\frac{3 u}{w}$ **Correct**
- $\frac{3}{w}$
- $- \frac{3 u}{w}$
- $\frac{3 u}{v}$
- $0$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

Here, we have 

$$
x(u,v,w)=3 \ln{\left(u v w \right)}\, y(u,v,w)=u + 2 w\, z(u,v,w)=u v.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =\frac{3}{u} & \frac{∂x}{∂v} & =\frac{3}{v} & \frac{∂x}{∂w} & =\frac{3}{w} \\ \frac{∂y}{∂u} & =1 & \frac{∂y}{∂v} & =0 & \frac{∂y}{∂w} & =2 \\ \frac{∂z}{∂u} & =v & \frac{∂z}{∂v} & =u, & \frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{3}{u} & \frac{3}{v} & \frac{3}{w} \\ 1 & 0 & 2 \\ v & u & 0\end{aligned}| \\  & =\left(\frac{3}{w}\right)(-1)^{1+3}|\begin{aligned}1 & 0 \\ v & u\end{aligned}|+\left(2\right)(-1)^{2+3}|\begin{aligned}\frac{3}{u} & \frac{3}{v} \\ v & u\end{aligned}| \\  & =\left(\frac{3}{w}\right)\left(u-\left(0\right)\right)+\left(-2\right)\left(3-\left(3\right)\right) \\  & =\frac{3 u}{w}.\end{aligned}
$$

### Generated — easy
Template: `log_product`; bank: `log_product-method`; eligible learner variant.

Find the Jacobian determinant of the transformation $T,$ defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}- \ln{\left(u v w \right)} \\ u + 3 w \\ - 4 u v\end{aligned}].
$$

- $\frac{4 u}{v}$
- $\frac{4 u}{w}$ **Correct**
- $0$
- $\frac{4}{w}$
- $- \frac{4 u}{w}$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

Here, we have 

$$
x(u,v,w)=- \ln{\left(u v w \right)}\, y(u,v,w)=u + 3 w\, z(u,v,w)=- 4 u v.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =- \frac{1}{u} & \frac{∂x}{∂v} & =- \frac{1}{v} & \frac{∂x}{∂w} & =- \frac{1}{w} \\ \frac{∂y}{∂u} & =1 & \frac{∂y}{∂v} & =0 & \frac{∂y}{∂w} & =3 \\ \frac{∂z}{∂u} & =- 4 v & \frac{∂z}{∂v} & =- 4 u, & \frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}- \frac{1}{u} & - \frac{1}{v} & - \frac{1}{w} \\ 1 & 0 & 3 \\ - 4 v & - 4 u & 0\end{aligned}| \\  & =\left(- \frac{1}{w}\right)(-1)^{1+3}|\begin{aligned}1 & 0 \\ - 4 v & - 4 u\end{aligned}|+\left(3\right)(-1)^{2+3}|\begin{aligned}- \frac{1}{u} & - \frac{1}{v} \\ - 4 v & - 4 u\end{aligned}| \\  & =\left(- \frac{1}{w}\right)\left(- 4 u-\left(0\right)\right)+\left(-3\right)\left(4-\left(4\right)\right) \\  & =\frac{4 u}{w}.\end{aligned}
$$

## Original — q-39299 (moderate)
Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=u\operatorname{cos}⁡\theta +v\operatorname{sin}⁡\theta ,\,y=v\operatorname{cos}⁡\theta -u\operatorname{sin}⁡\theta ,\,z=w.
$$

You may assume that $\theta $ is a fixed constant.

- $\operatorname{cos}⁡\theta $
- $\operatorname{sin}⁡\theta $
- $0$
- $1$ **Correct**
- $\operatorname{sin}⁡\theta \operatorname{cos}⁡\theta $

**Original worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =\operatorname{cos}⁡\theta  & \,\frac{∂x}{∂v} & =\operatorname{sin}⁡\theta  & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =-\operatorname{sin}⁡\theta  & \,\frac{∂y}{∂v} & =\operatorname{cos}⁡\theta  & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\operatorname{cos}⁡\theta  & \operatorname{sin}⁡\theta  & 0 \\ -\operatorname{sin}⁡\theta  & \operatorname{cos}⁡\theta  & 0 \\ 0 & 0 & 1\end{aligned}| \\  & =1(-1)^{3+3}|\begin{aligned}\operatorname{cos}⁡\theta  & \operatorname{sin}⁡\theta  \\ -\operatorname{sin}⁡\theta  & \operatorname{cos}⁡\theta \end{aligned}| \\  & ={cos}^{2}⁡\theta +{sin}^{2}⁡\theta  \\  & =1.\end{aligned}
$$

### Generated — moderate
Template: `rotation`; bank: `rotation-observed`; evidence-only replay.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=u \cos{\left(\theta \right)} + v \sin{\left(\theta \right)}\, y=- u \sin{\left(\theta \right)} + v \cos{\left(\theta \right)}\, z=w.
$$

You may assume that $\theta $ is a fixed constant.

- $0$
- $\sin{\left(\theta \right)}$
- $\cos{\left(\theta \right)}$
- $\sin{\left(\theta \right)} \cos{\left(\theta \right)}$
- $1$ **Correct**

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =\cos{\left(\theta \right)} & \frac{∂x}{∂v} & =\sin{\left(\theta \right)} & \frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =- \sin{\left(\theta \right)} & \frac{∂y}{∂v} & =\cos{\left(\theta \right)} & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =0 & \frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\cos{\left(\theta \right)} & \sin{\left(\theta \right)} & 0 \\ - \sin{\left(\theta \right)} & \cos{\left(\theta \right)} & 0 \\ 0 & 0 & 1\end{aligned}| \\  & =\left(1\right)(-1)^{3+3}|\begin{aligned}\cos{\left(\theta \right)} & \sin{\left(\theta \right)} \\ - \sin{\left(\theta \right)} & \cos{\left(\theta \right)}\end{aligned}| \\  & =\left(\cos^{2}{\left(\theta \right)}\right)+\left(\sin^{2}{\left(\theta \right)}\right) \\  & =1.\end{aligned}
$$

### Generated — moderate
Template: `rotation`; bank: `rotation-observed`; evidence-only replay.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=2 u \cos{\left(\theta \right)} + 2 v \sin{\left(\theta \right)}\, y=4 u \sin{\left(\theta \right)} - 4 v \cos{\left(\theta \right)}\, z=w.
$$

You may assume that $\theta $ is a fixed constant.

- $- 8 \sin{\left(\theta \right)} \cos{\left(\theta \right)}$
- $-8$ **Correct**
- $- 8 \sin{\left(\theta \right)}$
- $- 8 \cos{\left(\theta \right)}$
- $0$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2 \cos{\left(\theta \right)} & \frac{∂x}{∂v} & =2 \sin{\left(\theta \right)} & \frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =4 \sin{\left(\theta \right)} & \frac{∂y}{∂v} & =- 4 \cos{\left(\theta \right)} & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =0 & \frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2 \cos{\left(\theta \right)} & 2 \sin{\left(\theta \right)} & 0 \\ 4 \sin{\left(\theta \right)} & - 4 \cos{\left(\theta \right)} & 0 \\ 0 & 0 & 1\end{aligned}| \\  & =\left(1\right)(-1)^{3+3}|\begin{aligned}2 \cos{\left(\theta \right)} & 2 \sin{\left(\theta \right)} \\ 4 \sin{\left(\theta \right)} & - 4 \cos{\left(\theta \right)}\end{aligned}| \\  & =\left(- 8 \cos^{2}{\left(\theta \right)}\right)+\left(- 8 \sin^{2}{\left(\theta \right)}\right) \\  & =-8.\end{aligned}
$$

### Generated — moderate
Template: `rotation`; bank: `rotation-method`; eligible learner variant.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=3 u \cos{\left(\theta \right)} + 3 v \sin{\left(\theta \right)}\, y=- u \sin{\left(\theta \right)} + v \cos{\left(\theta \right)}\, z=2 w.
$$

You may assume that $\theta $ is a fixed constant.

- $6$ **Correct**
- $6 \cos^{2}{\left(\theta \right)}$
- $-6$
- $6 \sin^{2}{\left(\theta \right)}$
- $0$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =3 \cos{\left(\theta \right)} & \frac{∂x}{∂v} & =3 \sin{\left(\theta \right)} & \frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =- \sin{\left(\theta \right)} & \frac{∂y}{∂v} & =\cos{\left(\theta \right)} & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =0 & \frac{∂z}{∂w} & =2\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}3 \cos{\left(\theta \right)} & 3 \sin{\left(\theta \right)} & 0 \\ - \sin{\left(\theta \right)} & \cos{\left(\theta \right)} & 0 \\ 0 & 0 & 2\end{aligned}| \\  & =\left(2\right)(-1)^{3+3}|\begin{aligned}3 \cos{\left(\theta \right)} & 3 \sin{\left(\theta \right)} \\ - \sin{\left(\theta \right)} & \cos{\left(\theta \right)}\end{aligned}| \\  & =\left(6 \cos^{2}{\left(\theta \right)}\right)+\left(6 \sin^{2}{\left(\theta \right)}\right) \\  & =6.\end{aligned}
$$

### Generated — moderate
Template: `rotation`; bank: `rotation-method`; eligible learner variant.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=- u \cos{\left(\theta \right)} - v \sin{\left(\theta \right)}\, y=- u \sin{\left(\theta \right)} + v \cos{\left(\theta \right)}\, z=3 w.
$$

You may assume that $\theta $ is a fixed constant.

- $- 3 \sin^{2}{\left(\theta \right)}$
- $-3$ **Correct**
- $0$
- $- 3 \cos^{2}{\left(\theta \right)}$
- $3$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =- \cos{\left(\theta \right)} & \frac{∂x}{∂v} & =- \sin{\left(\theta \right)} & \frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =- \sin{\left(\theta \right)} & \frac{∂y}{∂v} & =\cos{\left(\theta \right)} & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =0 & \frac{∂z}{∂w} & =3\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}- \cos{\left(\theta \right)} & - \sin{\left(\theta \right)} & 0 \\ - \sin{\left(\theta \right)} & \cos{\left(\theta \right)} & 0 \\ 0 & 0 & 3\end{aligned}| \\  & =\left(3\right)(-1)^{3+3}|\begin{aligned}- \cos{\left(\theta \right)} & - \sin{\left(\theta \right)} \\ - \sin{\left(\theta \right)} & \cos{\left(\theta \right)}\end{aligned}| \\  & =\left(- 3 \cos^{2}{\left(\theta \right)}\right)+\left(- 3 \sin^{2}{\left(\theta \right)}\right) \\  & =-3.\end{aligned}
$$

## Original — q-161792 (moderate)
Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=u{v}^{2}+w,\,y={u}^{3}+v,\,z=uv.
$$

- $6{u}^{3}v-{v}^{2}$
- $v(3{u}^{2}+2)$
- $3{u}^{3}-v$ **Correct**
- $2{u}^{2}{v}^{2}$
- $-u{v}^{2}$

**Original worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & ={v}^{2} & \,\frac{∂x}{∂v} & =2uv & \,\frac{∂x}{∂w} & =1 \\ \frac{∂y}{∂u} & =3{u}^{2} & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =v & \,\frac{∂z}{∂v} & =u & \,\frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}{v}^{2} & 2uv & 1 \\ 3{u}^{2} & 1 & 0 \\ v & u & 0\end{aligned}| \\  & =1(-1)^{1+3}|\begin{aligned}3{u}^{2} & 1 \\ v & u\end{aligned}| \\  & =3{u}^{3}-v.\end{aligned}
$$

### Generated — moderate
Template: `polynomial_column`; bank: `polynomial_column-observed`; evidence-only replay.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=u v^{2} + w\, y=u^{3} + v\, z=u v.
$$

- $3 u^{3} - v$ **Correct**
- $v \left(3 u^{2} + 2\right)$
- $6 u^{3} v - v^{2}$
- $- u v^{2}$
- $2 u^{2} v^{2}$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =v^{2} & \frac{∂x}{∂v} & =2 u v & \frac{∂x}{∂w} & =1 \\ \frac{∂y}{∂u} & =3 u^{2} & \frac{∂y}{∂v} & =1 & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =v & \frac{∂z}{∂v} & =u & \frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}v^{2} & 2 u v & 1 \\ 3 u^{2} & 1 & 0 \\ v & u & 0\end{aligned}| \\  & =\left(1\right)(-1)^{1+3}|\begin{aligned}3 u^{2} & 1 \\ v & u\end{aligned}| \\  & =3 u^{3} - v.\end{aligned}
$$

### Generated — moderate
Template: `polynomial_column`; bank: `polynomial_column-observed`; evidence-only replay.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=2 u v^{2} - 4 w\, y=u^{3} - 2 v\, z=- u v.
$$

- $2 u v^{2}$
- $- 4 u^{2} v^{2}$
- $v \left(3 u^{2} + 4\right)$
- $12 u^{3} v + 4 v^{2}$
- $12 u^{3} + 8 v$ **Correct**

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2 v^{2} & \frac{∂x}{∂v} & =4 u v & \frac{∂x}{∂w} & =-4 \\ \frac{∂y}{∂u} & =3 u^{2} & \frac{∂y}{∂v} & =-2 & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =- v & \frac{∂z}{∂v} & =- u & \frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2 v^{2} & 4 u v & -4 \\ 3 u^{2} & -2 & 0 \\ - v & - u & 0\end{aligned}| \\  & =\left(-4\right)(-1)^{1+3}|\begin{aligned}3 u^{2} & -2 \\ - v & - u\end{aligned}| \\  & =12 u^{3} + 8 v.\end{aligned}
$$

### Generated — moderate
Template: `polynomial_column`; bank: `polynomial_column-method`; eligible learner variant.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=3 u v^{2} + w\, y=2 u^{3} + v\, z=- 2 u v.
$$

- $- 12 u^{3} + 2 v$ **Correct**
- $- 4 u^{3} + 2 v$
- $12 u^{3} - 2 v$
- $- 12 u^{3} - 2 v$
- $- 12 u^{3}$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =3 v^{2} & \frac{∂x}{∂v} & =6 u v & \frac{∂x}{∂w} & =1 \\ \frac{∂y}{∂u} & =6 u^{2} & \frac{∂y}{∂v} & =1 & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =- 2 v & \frac{∂z}{∂v} & =- 2 u & \frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}3 v^{2} & 6 u v & 1 \\ 6 u^{2} & 1 & 0 \\ - 2 v & - 2 u & 0\end{aligned}| \\  & =\left(1\right)(-1)^{1+3}|\begin{aligned}6 u^{2} & 1 \\ - 2 v & - 2 u\end{aligned}| \\  & =- 12 u^{3} + 2 v.\end{aligned}
$$

### Generated — moderate
Template: `polynomial_column`; bank: `polynomial_column-method`; eligible learner variant.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=- u v^{2} + w\, y=3 u^{3} - 4 v\, z=- u v.
$$

- $- 9 u^{3} + 4 v$
- $- 9 u^{3} - 4 v$ **Correct**
- $- 9 u^{3}$
- $- 3 u^{3} - 4 v$
- $9 u^{3} + 4 v$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =- v^{2} & \frac{∂x}{∂v} & =- 2 u v & \frac{∂x}{∂w} & =1 \\ \frac{∂y}{∂u} & =9 u^{2} & \frac{∂y}{∂v} & =-4 & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =- v & \frac{∂z}{∂v} & =- u & \frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}- v^{2} & - 2 u v & 1 \\ 9 u^{2} & -4 & 0 \\ - v & - u & 0\end{aligned}| \\  & =\left(1\right)(-1)^{1+3}|\begin{aligned}9 u^{2} & -4 \\ - v & - u\end{aligned}| \\  & =- 9 u^{3} - 4 v.\end{aligned}
$$

## Original — q-39710 (moderate)
Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x={u}^{2}+vw,\,y=2-uv,\,z={v}^{2}-w.
$$

- $2uv-2u{v}^{2}-vu$
- $2{u}^{2}-2{v}^{3}-vw$ **Correct**
- $2vw$
- $2uv-2u{v}^{2}+vu$
- $2{u}^{2}-2{v}^{3}+vw$

**Original worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2u & \,\frac{∂x}{∂v} & =w & \,\frac{∂x}{∂w} & =v \\ \frac{∂y}{∂u} & =-v & \,\frac{∂y}{∂v} & =-u & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =2v & \,\frac{∂z}{∂w} & =-1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2u & w & v \\ -v & -u & 0 \\ 0 & 2v & -1\end{aligned}| \\  & =2u(-1)^{1+1}|\begin{aligned}-u & 0 \\ 2v & -1\end{aligned}|+(-v)(-1)^{2+1}|\begin{aligned}w & v \\ 2v & -1\end{aligned}| \\  & =2u(u-0)+v(-w-2{v}^{2}) \\  & =2{u}^{2}-2{v}^{3}-vw.\end{aligned}
$$

### Generated — moderate
Template: `polynomial_mixed`; bank: `polynomial_mixed-observed`; evidence-only replay.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=u^{2} + v w\, y=- u v + 2\, z=v^{2} - w.
$$

- $2 v w$
- $2 u^{2} - 2 v^{3} - v w$ **Correct**
- $- 2 u v^{2} + u v$
- $2 u^{2} - 2 v^{3} + v w$
- $- 2 u v^{2} + 3 u v$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2 u & \frac{∂x}{∂v} & =w & \frac{∂x}{∂w} & =v \\ \frac{∂y}{∂u} & =- v & \frac{∂y}{∂v} & =- u & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =2 v & \frac{∂z}{∂w} & =-1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2 u & w & v \\ - v & - u & 0 \\ 0 & 2 v & -1\end{aligned}| \\  & =\left(2 u\right)(-1)^{1+1}|\begin{aligned}- u & 0 \\ 2 v & -1\end{aligned}|+\left(- v\right)(-1)^{2+1}|\begin{aligned}w & v \\ 2 v & -1\end{aligned}| \\  & =\left(2 u\right)\left(u-\left(0\right)\right)+\left(v\right)\left(- w-\left(2 v^{2}\right)\right) \\  & =2 u^{2} - 2 v^{3} - v w.\end{aligned}
$$

### Generated — moderate
Template: `polynomial_mixed`; bank: `polynomial_mixed-observed`; evidence-only replay.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=2 u^{2} - 4 v w\, y=- u v - 1\, z=- 2 v^{2} - w.
$$

- $4 u^{2} - 16 v^{3} - 4 v w$
- $- 16 u v^{2} + 5 u v$
- $4 u^{2} - 16 v^{3} + 4 v w$ **Correct**
- $- 16 u v^{2} + 3 u v$
- $- 8 v w$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =4 u & \frac{∂x}{∂v} & =- 4 w & \frac{∂x}{∂w} & =- 4 v \\ \frac{∂y}{∂u} & =- v & \frac{∂y}{∂v} & =- u & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =- 4 v & \frac{∂z}{∂w} & =-1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}4 u & - 4 w & - 4 v \\ - v & - u & 0 \\ 0 & - 4 v & -1\end{aligned}| \\  & =\left(4 u\right)(-1)^{1+1}|\begin{aligned}- u & 0 \\ - 4 v & -1\end{aligned}|+\left(- v\right)(-1)^{2+1}|\begin{aligned}- 4 w & - 4 v \\ - 4 v & -1\end{aligned}| \\  & =\left(4 u\right)\left(u-\left(0\right)\right)+\left(v\right)\left(4 w-\left(16 v^{2}\right)\right) \\  & =4 u^{2} - 16 v^{3} + 4 v w.\end{aligned}
$$

### Generated — moderate
Template: `polynomial_mixed`; bank: `polynomial_mixed-method`; eligible learner variant.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=3 u^{2} + v w\, y=- 2 u v - 2\, z=v^{2} - w.
$$

- $12 u^{2} - 4 v^{3} - 2 v w$ **Correct**
- $12 u^{2} + 4 v^{3} + 2 v w$
- $- 12 u^{2} + 4 v^{3} + 2 v w$
- $12 u^{2} - 4 v^{3} + 2 v w$
- $12 u^{2} - 2 v w$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =6 u & \frac{∂x}{∂v} & =w & \frac{∂x}{∂w} & =v \\ \frac{∂y}{∂u} & =- 2 v & \frac{∂y}{∂v} & =- 2 u & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =2 v & \frac{∂z}{∂w} & =-1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}6 u & w & v \\ - 2 v & - 2 u & 0 \\ 0 & 2 v & -1\end{aligned}| \\  & =\left(6 u\right)(-1)^{1+1}|\begin{aligned}- 2 u & 0 \\ 2 v & -1\end{aligned}|+\left(- 2 v\right)(-1)^{2+1}|\begin{aligned}w & v \\ 2 v & -1\end{aligned}| \\  & =\left(6 u\right)\left(2 u-\left(0\right)\right)+\left(2 v\right)\left(- w-\left(2 v^{2}\right)\right) \\  & =12 u^{2} - 4 v^{3} - 2 v w.\end{aligned}
$$

### Generated — moderate
Template: `polynomial_mixed`; bank: `polynomial_mixed-method`; eligible learner variant.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=- u^{2} + v w\, y=- 3 u v - 1\, z=- 4 v^{2} - w.
$$

- $- 6 u^{2} + 24 v^{3} + 3 v w$
- $- 6 u^{2} + 24 v^{3} - 3 v w$ **Correct**
- $- 6 u^{2} - 3 v w$
- $- 6 u^{2} - 24 v^{3} + 3 v w$
- $6 u^{2} - 24 v^{3} + 3 v w$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =- 2 u & \frac{∂x}{∂v} & =w & \frac{∂x}{∂w} & =v \\ \frac{∂y}{∂u} & =- 3 v & \frac{∂y}{∂v} & =- 3 u & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =- 8 v & \frac{∂z}{∂w} & =-1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}- 2 u & w & v \\ - 3 v & - 3 u & 0 \\ 0 & - 8 v & -1\end{aligned}| \\  & =\left(- 2 u\right)(-1)^{1+1}|\begin{aligned}- 3 u & 0 \\ - 8 v & -1\end{aligned}|+\left(- 3 v\right)(-1)^{2+1}|\begin{aligned}w & v \\ - 8 v & -1\end{aligned}| \\  & =\left(- 2 u\right)\left(3 u-\left(0\right)\right)+\left(3 v\right)\left(- w-\left(- 8 v^{2}\right)\right) \\  & =- 6 u^{2} + 24 v^{3} - 3 v w.\end{aligned}
$$

## Original — q-39294 (moderate)
Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=v+w,\,y=u+w,\,z=u+v.
$$

- $2$ **Correct**
- $0$
- $-1$
- $-2$
- $1$

**Original worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =0 & \,\frac{∂x}{∂v} & =1 & \,\frac{∂x}{∂w} & =1 \\ \frac{∂y}{∂u} & =1 & \,\frac{∂y}{∂v} & =0 & \,\frac{∂y}{∂w} & =1 \\ \frac{∂z}{∂u} & =1 & \,\frac{∂z}{∂v} & =1 & \,\frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}0 & 1 & 1 \\ 1 & 0 & 1 \\ 1 & 1 & 0\end{aligned}| \\  & =1(-1)^{1+2}|\begin{aligned}1 & 1 \\ 1 & 0\end{aligned}|+1(-1)^{1+3}|\begin{aligned}1 & 0 \\ 1 & 1\end{aligned}| \\  & =(-1)(0-1)+(1-0) \\  & =2.\end{aligned}
$$

### Generated — moderate
Template: `linear_offdiag`; bank: `linear_offdiag-observed`; evidence-only replay.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=v + w\, y=u + w\, z=u + v.
$$

- $-1$
- $0$
- $2$ **Correct**
- $1$
- $-2$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =0 & \frac{∂x}{∂v} & =1 & \frac{∂x}{∂w} & =1 \\ \frac{∂y}{∂u} & =1 & \frac{∂y}{∂v} & =0 & \frac{∂y}{∂w} & =1 \\ \frac{∂z}{∂u} & =1 & \frac{∂z}{∂v} & =1 & \frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}0 & 1 & 1 \\ 1 & 0 & 1 \\ 1 & 1 & 0\end{aligned}| \\  & =\left(1\right)(-1)^{1+2}|\begin{aligned}1 & 1 \\ 1 & 0\end{aligned}|+\left(1\right)(-1)^{1+3}|\begin{aligned}1 & 0 \\ 1 & 1\end{aligned}| \\  & =\left(-1\right)\left(0-\left(1\right)\right)+\left(1-\left(0\right)\right) \\  & =2.\end{aligned}
$$

### Generated — moderate
Template: `linear_offdiag`; bank: `linear_offdiag-observed`; evidence-only replay.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=- 3 v - w\, y=- 4 u - w\, z=- 4 u + 2 v.
$$

- $-3$
- $4$
- $0$
- $-4$ **Correct**
- $3$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =0 & \frac{∂x}{∂v} & =-3 & \frac{∂x}{∂w} & =-1 \\ \frac{∂y}{∂u} & =-4 & \frac{∂y}{∂v} & =0 & \frac{∂y}{∂w} & =-1 \\ \frac{∂z}{∂u} & =-4 & \frac{∂z}{∂v} & =2 & \frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}0 & -3 & -1 \\ -4 & 0 & -1 \\ -4 & 2 & 0\end{aligned}| \\  & =\left(-3\right)(-1)^{1+2}|\begin{aligned}-4 & -1 \\ -4 & 0\end{aligned}|+\left(-1\right)(-1)^{1+3}|\begin{aligned}-4 & 0 \\ -4 & 2\end{aligned}| \\  & =\left(3\right)\left(0-\left(4\right)\right)+\left(-1\right)\left(-8-\left(0\right)\right) \\  & =-4.\end{aligned}
$$

### Generated — moderate
Template: `linear_offdiag`; bank: `linear_offdiag-method`; eligible learner variant.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=3 v + w\, y=2 u + w\, z=- 2 u + v.
$$

- $-4$ **Correct**
- $-8$
- $4$
- $-6$
- $2$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =0 & \frac{∂x}{∂v} & =3 & \frac{∂x}{∂w} & =1 \\ \frac{∂y}{∂u} & =2 & \frac{∂y}{∂v} & =0 & \frac{∂y}{∂w} & =1 \\ \frac{∂z}{∂u} & =-2 & \frac{∂z}{∂v} & =1 & \frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}0 & 3 & 1 \\ 2 & 0 & 1 \\ -2 & 1 & 0\end{aligned}| \\  & =\left(3\right)(-1)^{1+2}|\begin{aligned}2 & 1 \\ -2 & 0\end{aligned}|+\left(1\right)(-1)^{1+3}|\begin{aligned}2 & 0 \\ -2 & 1\end{aligned}| \\  & =\left(-3\right)\left(0-\left(-2\right)\right)+\left(2-\left(0\right)\right) \\  & =-4.\end{aligned}
$$

### Generated — moderate
Template: `linear_offdiag`; bank: `linear_offdiag-method`; eligible learner variant.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=- v + w\, y=3 u - 4 w\, z=- u - v.
$$

- $-4$
- $-7$ **Correct**
- $-3$
- $-1$
- $7$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =0 & \frac{∂x}{∂v} & =-1 & \frac{∂x}{∂w} & =1 \\ \frac{∂y}{∂u} & =3 & \frac{∂y}{∂v} & =0 & \frac{∂y}{∂w} & =-4 \\ \frac{∂z}{∂u} & =-1 & \frac{∂z}{∂v} & =-1 & \frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}0 & -1 & 1 \\ 3 & 0 & -4 \\ -1 & -1 & 0\end{aligned}| \\  & =\left(-1\right)(-1)^{1+2}|\begin{aligned}3 & -4 \\ -1 & 0\end{aligned}|+\left(1\right)(-1)^{1+3}|\begin{aligned}3 & 0 \\ -1 & -1\end{aligned}| \\  & =\left(0-\left(4\right)\right)+\left(-3-\left(0\right)\right) \\  & =-7.\end{aligned}
$$

## Original — q-39664 (moderate)
Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=au,\,y=bv,\,z=cw.
$$

You may assume that $a$, $b$ and $c$ are fixed constants.

- $-a-b-c$
- $-abc$
- $a+b+c$
- $abc$ **Correct**
- $0$

**Original worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =a & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =b & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & =c\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}a & 0 & 0 \\ 0 & b & 0 \\ 0 & 0 & c\end{aligned}| \\  & =a(-1)^{1+1}|\begin{aligned}b & 0 \\ 0 & c\end{aligned}| \\  & =a(bc-0) \\  & =abc.\end{aligned}
$$

### Generated — moderate
Template: `symbolic_diagonal`; bank: `symbolic_diagonal-observed`; evidence-only replay.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=a u\, y=b v\, z=c w.
$$

You may assume that $a$, $b$ and $c$ are fixed constants.

- $a + b + c$
- $- a b c$
- $- a - b - c$
- $0$
- $a b c$ **Correct**

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =a & \frac{∂x}{∂v} & =0 & \frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \frac{∂y}{∂v} & =b & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =0 & \frac{∂z}{∂w} & =c\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}a & 0 & 0 \\ 0 & b & 0 \\ 0 & 0 & c\end{aligned}| \\  & =\left(a\right)(-1)^{1+1}|\begin{aligned}b & 0 \\ 0 & c\end{aligned}| \\  & =\left(a\right)\left(b c-\left(0\right)\right) \\  & =a b c.\end{aligned}
$$

### Generated — moderate
Template: `symbolic_diagonal`; bank: `symbolic_diagonal-observed`; evidence-only replay.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=2 a u\, y=- 4 b v\, z=c w.
$$

You may assume that $a$, $b$ and $c$ are fixed constants.

- $0$
- $- 8 a b c$ **Correct**
- $8 a b c$
- $- 2 a + 4 b - c$
- $2 a - 4 b + c$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2 a & \frac{∂x}{∂v} & =0 & \frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \frac{∂y}{∂v} & =- 4 b & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =0 & \frac{∂z}{∂w} & =c\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2 a & 0 & 0 \\ 0 & - 4 b & 0 \\ 0 & 0 & c\end{aligned}| \\  & =\left(2 a\right)(-1)^{1+1}|\begin{aligned}- 4 b & 0 \\ 0 & c\end{aligned}| \\  & =\left(2 a\right)\left(- 4 b c-\left(0\right)\right) \\  & =- 8 a b c.\end{aligned}
$$

### Generated — moderate
Template: `symbolic_diagonal`; bank: `symbolic_diagonal-method`; eligible learner variant.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=3 a u\, y=b v\, z=2 c w.
$$

You may assume that $a$, $b$ and $c$ are fixed constants.

- $6 a b c$ **Correct**
- $3 a + b + 2 c$
- $- 6 a b c$
- $- 3 a - b - 2 c$
- $0$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =3 a & \frac{∂x}{∂v} & =0 & \frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \frac{∂y}{∂v} & =b & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =0 & \frac{∂z}{∂w} & =2 c\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}3 a & 0 & 0 \\ 0 & b & 0 \\ 0 & 0 & 2 c\end{aligned}| \\  & =\left(3 a\right)(-1)^{1+1}|\begin{aligned}b & 0 \\ 0 & 2 c\end{aligned}| \\  & =\left(3 a\right)\left(2 b c-\left(0\right)\right) \\  & =6 a b c.\end{aligned}
$$

### Generated — moderate
Template: `symbolic_diagonal`; bank: `symbolic_diagonal-method`; eligible learner variant.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=- a u\, y=b v\, z=3 c w.
$$

You may assume that $a$, $b$ and $c$ are fixed constants.

- $a - b - 3 c$
- $- 3 a b c$ **Correct**
- $0$
- $- a + b + 3 c$
- $3 a b c$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =- a & \frac{∂x}{∂v} & =0 & \frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \frac{∂y}{∂v} & =b & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =0 & \frac{∂z}{∂w} & =3 c\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}- a & 0 & 0 \\ 0 & b & 0 \\ 0 & 0 & 3 c\end{aligned}| \\  & =\left(- a\right)(-1)^{1+1}|\begin{aligned}b & 0 \\ 0 & 3 c\end{aligned}| \\  & =\left(- a\right)\left(3 b c-\left(0\right)\right) \\  & =- 3 a b c.\end{aligned}
$$

### Generated — hard
Template: `spherical`; bank: `spherical-method`; eligible learner variant.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=3 u \sin{\left(v \right)} \cos{\left(w \right)}\, y=u \sin{\left(v \right)} \sin{\left(w \right)}\, z=2 u \cos{\left(v \right)}.
$$

- $6 u^{2} \sin{\left(v \right)}$ **Correct**
- $6 u \sin{\left(v \right)}$
- $- 6 u^{2} \sin{\left(v \right)}$
- $6 u^{2} \sin^{3}{\left(v \right)}$
- $6 u^{2} \sin{\left(v \right)} \cos^{2}{\left(v \right)}$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =3 \sin{\left(v \right)} \cos{\left(w \right)} & \frac{∂x}{∂v} & =3 u \cos{\left(v \right)} \cos{\left(w \right)} & \frac{∂x}{∂w} & =- 3 u \sin{\left(v \right)} \sin{\left(w \right)} \\ \frac{∂y}{∂u} & =\sin{\left(v \right)} \sin{\left(w \right)} & \frac{∂y}{∂v} & =u \sin{\left(w \right)} \cos{\left(v \right)} & \frac{∂y}{∂w} & =u \sin{\left(v \right)} \cos{\left(w \right)} \\ \frac{∂z}{∂u} & =2 \cos{\left(v \right)} & \frac{∂z}{∂v} & =- 2 u \sin{\left(v \right)} & \frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}3 \sin{\left(v \right)} \cos{\left(w \right)} & 3 u \cos{\left(v \right)} \cos{\left(w \right)} & - 3 u \sin{\left(v \right)} \sin{\left(w \right)} \\ \sin{\left(v \right)} \sin{\left(w \right)} & u \sin{\left(w \right)} \cos{\left(v \right)} & u \sin{\left(v \right)} \cos{\left(w \right)} \\ 2 \cos{\left(v \right)} & - 2 u \sin{\left(v \right)} & 0\end{aligned}| \\  & =\left(2 \cos{\left(v \right)}\right)(-1)^{3+1}|\begin{aligned}3 u \cos{\left(v \right)} \cos{\left(w \right)} & - 3 u \sin{\left(v \right)} \sin{\left(w \right)} \\ u \sin{\left(w \right)} \cos{\left(v \right)} & u \sin{\left(v \right)} \cos{\left(w \right)}\end{aligned}|+\left(- 2 u \sin{\left(v \right)}\right)(-1)^{3+2}|\begin{aligned}3 \sin{\left(v \right)} \cos{\left(w \right)} & - 3 u \sin{\left(v \right)} \sin{\left(w \right)} \\ \sin{\left(v \right)} \sin{\left(w \right)} & u \sin{\left(v \right)} \cos{\left(w \right)}\end{aligned}| \\  & =\left(6 u^{2} \sin{\left(v \right)} \cos^{2}{\left(v \right)}\right)\left(\cos^2 w+\sin^2 w\right)+\left(6 u^{2} \sin^{3}{\left(v \right)}\right)\left(\cos^2 w+\sin^2 w\right) \\  & =\left(6 u^{2} \sin{\left(v \right)} \cos^{2}{\left(v \right)}\right)+\left(6 u^{2} \sin^{3}{\left(v \right)}\right) \\  & =6 u^{2} \sin{\left(v \right)}\left(\cos^2 v+\sin^2 v\right) \\  & =6 u^{2} \sin{\left(v \right)}.\end{aligned}
$$

### Generated — hard
Template: `spherical`; bank: `spherical-method`; eligible learner variant.

Find the Jacobian determinant of the transformation $T$ that maps the $uvw$-space into the $xyz$-space by means of the equations

$$
x=- u \sin{\left(v \right)} \cos{\left(w \right)}\, y=u \sin{\left(v \right)} \sin{\left(w \right)}\, z=3 u \cos{\left(v \right)}.
$$

- $- 3 u^{2} \sin^{3}{\left(v \right)}$
- $- 3 u^{2} \sin{\left(v \right)}$ **Correct**
- $- 3 u^{2} \sin{\left(v \right)} \cos^{2}{\left(v \right)}$
- $- 3 u \sin{\left(v \right)}$
- $3 u^{2} \sin{\left(v \right)}$

**Worked solution**

For a transformation 

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]\to [\begin{aligned}x(u,v,w) \\ y(u,v,w) \\ z(u,v,w)\end{aligned}],
$$

the Jacobian determinant of $T,$ denoted $\frac{∂(x,y,z)}{∂(u,v,w)},$ is given by

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} & \frac{∂x}{∂w} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v} & \frac{∂y}{∂w} \\ \frac{∂z}{∂u} & \frac{∂z}{∂v} & \frac{∂z}{∂w}\end{aligned}|.\end{aligned}
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =- \sin{\left(v \right)} \cos{\left(w \right)} & \frac{∂x}{∂v} & =- u \cos{\left(v \right)} \cos{\left(w \right)} & \frac{∂x}{∂w} & =u \sin{\left(v \right)} \sin{\left(w \right)} \\ \frac{∂y}{∂u} & =\sin{\left(v \right)} \sin{\left(w \right)} & \frac{∂y}{∂v} & =u \sin{\left(w \right)} \cos{\left(v \right)} & \frac{∂y}{∂w} & =u \sin{\left(v \right)} \cos{\left(w \right)} \\ \frac{∂z}{∂u} & =3 \cos{\left(v \right)} & \frac{∂z}{∂v} & =- 3 u \sin{\left(v \right)} & \frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}- \sin{\left(v \right)} \cos{\left(w \right)} & - u \cos{\left(v \right)} \cos{\left(w \right)} & u \sin{\left(v \right)} \sin{\left(w \right)} \\ \sin{\left(v \right)} \sin{\left(w \right)} & u \sin{\left(w \right)} \cos{\left(v \right)} & u \sin{\left(v \right)} \cos{\left(w \right)} \\ 3 \cos{\left(v \right)} & - 3 u \sin{\left(v \right)} & 0\end{aligned}| \\  & =\left(3 \cos{\left(v \right)}\right)(-1)^{3+1}|\begin{aligned}- u \cos{\left(v \right)} \cos{\left(w \right)} & u \sin{\left(v \right)} \sin{\left(w \right)} \\ u \sin{\left(w \right)} \cos{\left(v \right)} & u \sin{\left(v \right)} \cos{\left(w \right)}\end{aligned}|+\left(- 3 u \sin{\left(v \right)}\right)(-1)^{3+2}|\begin{aligned}- \sin{\left(v \right)} \cos{\left(w \right)} & u \sin{\left(v \right)} \sin{\left(w \right)} \\ \sin{\left(v \right)} \sin{\left(w \right)} & u \sin{\left(v \right)} \cos{\left(w \right)}\end{aligned}| \\  & =\left(- 3 u^{2} \sin{\left(v \right)} \cos^{2}{\left(v \right)}\right)\left(\cos^2 w+\sin^2 w\right)+\left(- 3 u^{2} \sin^{3}{\left(v \right)}\right)\left(\cos^2 w+\sin^2 w\right) \\  & =\left(- 3 u^{2} \sin{\left(v \right)} \cos^{2}{\left(v \right)}\right)+\left(- 3 u^{2} \sin^{3}{\left(v \right)}\right) \\  & =- 3 u^{2} \sin{\left(v \right)}\left(\cos^2 v+\sin^2 v\right) \\  & =- 3 u^{2} \sin{\left(v \right)}.\end{aligned}
$$
