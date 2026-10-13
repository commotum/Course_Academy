# Clearly labeled source and generated review

Raw evidence-only originals retain historical banks and missing attributes. Translations use the same normal API and fixed stage masks. Authored defaults use method banks.


## Original replay q-161819

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: observed
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{u}^{2}-{w}^{2} \\ w{e}^{u} \\ u-v\end{aligned}].
$$

Field 1 — original correct ref ABSENT; designation not inferred
- The critical points lie on the plane $u = w$.
- The critical points lie on the parabolic cylinder $u =-w^{2}$.
- The critical points lie on the plane $u = 2v$.
- The critical points lie on the parabolic cylinder $u = 2w^{2}$.
- The critical points lie on the $vw -$plane.

Field 2:
- The critical points lie on the $vw-$plane.
- The critical points lie on the plane $u=2v.$
- The critical points lie on the parabolic cylinder $u=2{w}^{2}.$
- The critical points lie on the parabolic cylinder $u=-{w}^{2}.$ [correct]
- The critical points lie on the plane $u=w.$

Worked solution:
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
x(u,v,w)={u}^{2}-{w}^{2},\,y(u,v,w)=w{e}^{u},\,z(u,v,w)=u-v.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2u & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =-2w \\ \frac{∂y}{∂u} & =w{e}^{u} & \,\frac{∂y}{∂v} & =0 & \,\frac{∂y}{∂w} & ={e}^{u} \\ \frac{∂z}{∂u} & =1 & \,\frac{∂z}{∂v} & =-1 & \,\frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2u & 0 & -2w \\ w{e}^{u} & 0 & {e}^{u} \\ 1 & -1 & 0\end{aligned}| \\  & =2u|\begin{aligned}0 & {e}^{u} \\ -1 & 0\end{aligned}|-2w|\begin{aligned}w{e}^{u} & 0 \\ 1 & -1\end{aligned}| \\  & =2u(0+{e}^{u})-2w(-w{e}^{u}-0) \\  & =2u{e}^{u}+2{w}^{2}{e}^{u} \\  & =2{e}^{u}({w}^{2}+u).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 2{e}^{u}({w}^{2}+u) & =0 \\ {w}^{2}+u & =0.\end{aligned}
$$

The equation ${w}^{2}+u=0$ defines the parabolic cylinder $u=-{w}^{2}.$


## GENERATED evidence-only translated variant q-161819 #1

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{(u+2)}^{2}-{(w-3)}^{2} \\ (w-3){e}^{(u+2)} \\ (u+2)-(v-1)\end{aligned}].
$$

Field 1:
- The critical points lie on the parabolic cylinder $(u+2)=2{(w-3)}^{2}.$
- The critical points lie on the parabolic cylinder $(u+2)=-{(w-3)}^{2}.$ [correct]
- The critical points lie on the plane $(u+2)=2(v-1).$
- The critical points lie on the plane $(u+2)=(w-3).$
- The critical points lie on the plane $u=-2$.

Worked solution:
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
x(u,v,w)={(u+2)}^{2}-{(w-3)}^{2},\,y(u,v,w)=(w-3){e}^{(u+2)},\,z(u,v,w)=(u+2)-(v-1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2(u+2) & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =-2(w-3) \\ \frac{∂y}{∂u} & =(w-3){e}^{(u+2)} & \,\frac{∂y}{∂v} & =0 & \,\frac{∂y}{∂w} & ={e}^{(u+2)} \\ \frac{∂z}{∂u} & =1 & \,\frac{∂z}{∂v} & =-1 & \,\frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2(u+2) & 0 & -2(w-3) \\ (w-3){e}^{(u+2)} & 0 & {e}^{(u+2)} \\ 1 & -1 & 0\end{aligned}| \\  & =2(u+2)|\begin{aligned}0 & {e}^{(u+2)} \\ -1 & 0\end{aligned}|-2(w-3)|\begin{aligned}(w-3){e}^{(u+2)} & 0 \\ 1 & -1\end{aligned}| \\  & =2(u+2)(0+{e}^{(u+2)})-2(w-3)(-(w-3){e}^{(u+2)}-0) \\  & =2(u+2){e}^{(u+2)}+2{(w-3)}^{2}{e}^{(u+2)} \\  & =2{e}^{(u+2)}({(w-3)}^{2}+(u+2)).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 2{e}^{(u+2)}({(w-3)}^{2}+(u+2)) & =0 \\ {(w-3)}^{2}+(u+2) & =0.\end{aligned}
$$

The equation ${(w-3)}^{2}+(u+2)=0$ defines the parabolic cylinder $(u+2)=-{(w-3)}^{2}.$


## GENERATED evidence-only translated variant q-161819 #2

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{(u-2)}^{2}-{(w+1)}^{2} \\ (w+1){e}^{(u-2)} \\ (u-2)-(v+3)\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $(u-2)=(w+1).$
- The critical points lie on the plane $u=2$.
- The critical points lie on the parabolic cylinder $(u-2)=-{(w+1)}^{2}.$ [correct]
- The critical points lie on the plane $(u-2)=2(v+3).$
- The critical points lie on the parabolic cylinder $(u-2)=2{(w+1)}^{2}.$

Worked solution:
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
x(u,v,w)={(u-2)}^{2}-{(w+1)}^{2},\,y(u,v,w)=(w+1){e}^{(u-2)},\,z(u,v,w)=(u-2)-(v+3).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2(u-2) & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =-2(w+1) \\ \frac{∂y}{∂u} & =(w+1){e}^{(u-2)} & \,\frac{∂y}{∂v} & =0 & \,\frac{∂y}{∂w} & ={e}^{(u-2)} \\ \frac{∂z}{∂u} & =1 & \,\frac{∂z}{∂v} & =-1 & \,\frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2(u-2) & 0 & -2(w+1) \\ (w+1){e}^{(u-2)} & 0 & {e}^{(u-2)} \\ 1 & -1 & 0\end{aligned}| \\  & =2(u-2)|\begin{aligned}0 & {e}^{(u-2)} \\ -1 & 0\end{aligned}|-2(w+1)|\begin{aligned}(w+1){e}^{(u-2)} & 0 \\ 1 & -1\end{aligned}| \\  & =2(u-2)(0+{e}^{(u-2)})-2(w+1)(-(w+1){e}^{(u-2)}-0) \\  & =2(u-2){e}^{(u-2)}+2{(w+1)}^{2}{e}^{(u-2)} \\  & =2{e}^{(u-2)}({(w+1)}^{2}+(u-2)).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 2{e}^{(u-2)}({(w+1)}^{2}+(u-2)) & =0 \\ {(w+1)}^{2}+(u-2) & =0.\end{aligned}
$$

The equation ${(w+1)}^{2}+(u-2)=0$ defines the parabolic cylinder $(u-2)=-{(w+1)}^{2}.$


## Original replay q-39709

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: observed
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{u}^{2}-v \\ {u}^{2}+v \\ {e}^{w}\end{aligned}].
$$

Field 1:
- The critical points lie on the parabolic cylinder ${w}^{2}=2u.$
- The critical points lie on the sphere ${u}^{2}+{v}^{2}+{w}^{2}=1.$
- The critical points lie on the $vw-$plane. [correct]
- The critical points lie on the $uv-$plane.
- The critical points lie on the plane $w=u.$

Worked solution:
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
x(u,v,w)={u}^{2}-v,\,y(u,v,w)={u}^{2}+v,\,z(u,v,w)={e}^{w}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2u & \,\frac{∂x}{∂v} & =-1 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =2u & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & ={e}^{w}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2u & -1 & 0 \\ 2u & 1 & 0 \\ 0 & 0 & {e}^{w}\end{aligned}| \\  & ={e}^{w}|\begin{aligned}2u & -1 \\ 2u & 1\end{aligned}| \\  & ={e}^{w}(2u+2u) \\  & =4u{e}^{w}.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 4u{e}^{w} & =0 \\ u & =0.\end{aligned}
$$

The equation $u=0$ defines the plane $u=0,$ i.e., $vw$-plane.


## GENERATED evidence-only translated variant q-39709 #1

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{(u+2)}^{2}-(v-1) \\ {(u+2)}^{2}+(v-1) \\ {e}^{(w-3)}\end{aligned}].
$$

Field 1:
- The critical points lie on the sphere ${(u+2)}^{2}+{(v-1)}^{2}+{(w-3)}^{2}=1.$
- The critical points lie on the plane $(w-3)=(u+2).$
- The critical points lie on the parabolic cylinder ${(w-3)}^{2}=2(u+2).$
- The critical points lie on the plane $w=3$.
- The critical points lie on the plane $u=-2$. [correct]

Worked solution:
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
x(u,v,w)={(u+2)}^{2}-(v-1),\,y(u,v,w)={(u+2)}^{2}+(v-1),\,z(u,v,w)={e}^{(w-3)}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2(u+2) & \,\frac{∂x}{∂v} & =-1 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =2(u+2) & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & ={e}^{(w-3)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2(u+2) & -1 & 0 \\ 2(u+2) & 1 & 0 \\ 0 & 0 & {e}^{(w-3)}\end{aligned}| \\  & ={e}^{(w-3)}|\begin{aligned}2(u+2) & -1 \\ 2(u+2) & 1\end{aligned}| \\  & ={e}^{(w-3)}(2(u+2)+2(u+2)) \\  & =4(u+2){e}^{(w-3)}.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 4(u+2){e}^{(w-3)} & =0 \\ (u+2) & =0.\end{aligned}
$$

The equation $(u+2)=0$ defines the plane $(u+2)=0,$ i.e., plane $u=-2$.


## GENERATED evidence-only translated variant q-39709 #2

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{(u-2)}^{2}-(v+3) \\ {(u-2)}^{2}+(v+3) \\ {e}^{(w+1)}\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $w=-1$.
- The critical points lie on the plane $u=2$. [correct]
- The critical points lie on the plane $(w+1)=(u-2).$
- The critical points lie on the parabolic cylinder ${(w+1)}^{2}=2(u-2).$
- The critical points lie on the sphere ${(u-2)}^{2}+{(v+3)}^{2}+{(w+1)}^{2}=1.$

Worked solution:
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
x(u,v,w)={(u-2)}^{2}-(v+3),\,y(u,v,w)={(u-2)}^{2}+(v+3),\,z(u,v,w)={e}^{(w+1)}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2(u-2) & \,\frac{∂x}{∂v} & =-1 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =2(u-2) & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & ={e}^{(w+1)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2(u-2) & -1 & 0 \\ 2(u-2) & 1 & 0 \\ 0 & 0 & {e}^{(w+1)}\end{aligned}| \\  & ={e}^{(w+1)}|\begin{aligned}2(u-2) & -1 \\ 2(u-2) & 1\end{aligned}| \\  & ={e}^{(w+1)}(2(u-2)+2(u-2)) \\  & =4(u-2){e}^{(w+1)}.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 4(u-2){e}^{(w+1)} & =0 \\ (u-2) & =0.\end{aligned}
$$

The equation $(u-2)=0$ defines the plane $(u-2)=0,$ i.e., plane $u=2$.


## Original replay q-161809

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: observed
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}uv \\ u+v \\ w\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $v=u.$ [correct]
- The critical points lie on the $uv-$plane.
- The critical points lie on the cylinder ${v}^{2}+{u}^{2}=1.$
- The critical points lie on the $uw-$plane.
- The critical points lie on the parabolic cylinder $v={u}^{2}.$

Worked solution:
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
x(u,v,w)=uv,\,y(u,v,w)=u+v,\,z(u,v,w)=w.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =v & \,\frac{∂x}{∂v} & =u & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =1 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}v & u & 0 \\ 1 & 1 & 0 \\ 0 & 0 & 1\end{aligned}| \\  & =1|\begin{aligned}v & u \\ 1 & 1\end{aligned}| \\  & =v-u.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ v-u & =0.\end{aligned}
$$

The equation $v-u=0$ defines the plane $v=u..$


## GENERATED evidence-only translated variant q-161809 #1

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u+2)(v-1) \\ (u+2)+(v-1) \\ (w-3)\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $w=3$.
- The critical points lie on the parabolic cylinder $(v-1)={(u+2)}^{2}.$
- The critical points lie on the plane $(v-1)=(u+2).$ [correct]
- The critical points lie on the plane $v=1$.
- The critical points lie on the cylinder ${(v-1)}^{2}+{(u+2)}^{2}=1.$

Worked solution:
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
x(u,v,w)=(u+2)(v-1),\,y(u,v,w)=(u+2)+(v-1),\,z(u,v,w)=(w-3).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =(v-1) & \,\frac{∂x}{∂v} & =(u+2) & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =1 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}(v-1) & (u+2) & 0 \\ 1 & 1 & 0 \\ 0 & 0 & 1\end{aligned}| \\  & =1|\begin{aligned}(v-1) & (u+2) \\ 1 & 1\end{aligned}| \\  & =(v-1)-(u+2).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ (v-1)-(u+2) & =0.\end{aligned}
$$

The equation $(v-1)-(u+2)=0$ defines the plane $(v-1)=(u+2)..$


## GENERATED evidence-only translated variant q-161809 #2

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u-2)(v+3) \\ (u-2)+(v+3) \\ (w+1)\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $v=-3$.
- The critical points lie on the cylinder ${(v+3)}^{2}+{(u-2)}^{2}=1.$
- The critical points lie on the parabolic cylinder $(v+3)={(u-2)}^{2}.$
- The critical points lie on the plane $(v+3)=(u-2).$ [correct]
- The critical points lie on the plane $w=-1$.

Worked solution:
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
x(u,v,w)=(u-2)(v+3),\,y(u,v,w)=(u-2)+(v+3),\,z(u,v,w)=(w+1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =(v+3) & \,\frac{∂x}{∂v} & =(u-2) & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =1 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}(v+3) & (u-2) & 0 \\ 1 & 1 & 0 \\ 0 & 0 & 1\end{aligned}| \\  & =1|\begin{aligned}(v+3) & (u-2) \\ 1 & 1\end{aligned}| \\  & =(v+3)-(u-2).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ (v+3)-(u-2) & =0.\end{aligned}
$$

The equation $(v+3)-(u-2)=0$ defines the plane $(v+3)=(u-2)..$


## Original replay q-161812

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: observed
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u \\ {v}^{3}+{w}^{3} \\ v+w\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $v=2w.$
- The critical points lie on the $vw-$plane.
- The critical points lie on the parabolic cylinder $v={w}^{2}.$
- The critical points lie on the plane $v=u.$
- The critical points lie on the planes $v=\pm w.$ [correct]

Worked solution:
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
x(u,v,w)=u,\,y(u,v,w)={v}^{3}+{w}^{3},\,z(u,v,w)=v+w.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =3{v}^{2} & \,\frac{∂y}{∂w} & =3{w}^{2} \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =1 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 0 \\ 0 & 3{v}^{2} & 3{w}^{2} \\ 0 & 1 & 1\end{aligned}| \\  & =1|\begin{aligned}3{v}^{2} & 3{w}^{2} \\ 1 & 1\end{aligned}| \\  & =1(3{v}^{2}-3{w}^{2}) \\  & =3({v}^{2}-{w}^{2}).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 3({v}^{2}-{w}^{2}) & =0 \\ {v}^{2}-{w}^{2} & =0.\end{aligned}
$$

The equation ${v}^{2}-{w}^{2}=0$ defines a pair of intersecting planes $v=w$ and $v=-w.$


## GENERATED evidence-only translated variant q-161812 #1

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u+2) \\ {(v-1)}^{3}+{(w-3)}^{3} \\ (v-1)+(w-3)\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $u=-2$.
- The critical points lie on the planes $(v-1)=\pm (w-3).$ [correct]
- The critical points lie on the plane $(v-1)=2(w-3).$
- The critical points lie on the plane $(v-1)=(u+2).$
- The critical points lie on the parabolic cylinder $(v-1)={(w-3)}^{2}.$

Worked solution:
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
x(u,v,w)=(u+2),\,y(u,v,w)={(v-1)}^{3}+{(w-3)}^{3},\,z(u,v,w)=(v-1)+(w-3).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =3{(v-1)}^{2} & \,\frac{∂y}{∂w} & =3{(w-3)}^{2} \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =1 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 0 \\ 0 & 3{(v-1)}^{2} & 3{(w-3)}^{2} \\ 0 & 1 & 1\end{aligned}| \\  & =1|\begin{aligned}3{(v-1)}^{2} & 3{(w-3)}^{2} \\ 1 & 1\end{aligned}| \\  & =1(3{(v-1)}^{2}-3{(w-3)}^{2}) \\  & =3({(v-1)}^{2}-{(w-3)}^{2}).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 3({(v-1)}^{2}-{(w-3)}^{2}) & =0 \\ {(v-1)}^{2}-{(w-3)}^{2} & =0.\end{aligned}
$$

The equation ${(v-1)}^{2}-{(w-3)}^{2}=0$ defines a pair of intersecting planes $(v-1)=(w-3)$ and $(v-1)=-(w-3).$


## GENERATED evidence-only translated variant q-161812 #2

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u-2) \\ {(v+3)}^{3}+{(w+1)}^{3} \\ (v+3)+(w+1)\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $(v+3)=(u-2).$
- The critical points lie on the parabolic cylinder $(v+3)={(w+1)}^{2}.$
- The critical points lie on the planes $(v+3)=\pm (w+1).$ [correct]
- The critical points lie on the plane $(v+3)=2(w+1).$
- The critical points lie on the plane $u=2$.

Worked solution:
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
x(u,v,w)=(u-2),\,y(u,v,w)={(v+3)}^{3}+{(w+1)}^{3},\,z(u,v,w)=(v+3)+(w+1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =3{(v+3)}^{2} & \,\frac{∂y}{∂w} & =3{(w+1)}^{2} \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =1 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 0 \\ 0 & 3{(v+3)}^{2} & 3{(w+1)}^{2} \\ 0 & 1 & 1\end{aligned}| \\  & =1|\begin{aligned}3{(v+3)}^{2} & 3{(w+1)}^{2} \\ 1 & 1\end{aligned}| \\  & =1(3{(v+3)}^{2}-3{(w+1)}^{2}) \\  & =3({(v+3)}^{2}-{(w+1)}^{2}).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 3({(v+3)}^{2}-{(w+1)}^{2}) & =0 \\ {(v+3)}^{2}-{(w+1)}^{2} & =0.\end{aligned}
$$

The equation ${(v+3)}^{2}-{(w+1)}^{2}=0$ defines a pair of intersecting planes $(v+3)=(w+1)$ and $(v+3)=-(w+1).$


## Original replay q-161815

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: observed
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}\sqrt{u} \\ vw \\ u+w\end{aligned}].
$$

Field 1:
- The critical points lie on the $uv-$plane. [correct]
- The critical points lie on the $vw-$plane.
- The critical points lie on the parabolic cylinder $v={w}^{2}.$
- The critical points lie on the plane $u=w.$
- The critical points lie on the sphere ${u}^{2}+{v}^{2}+{w}^{2}=2.$

Worked solution:
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
x(u,v,w)=\sqrt{u},\,y(u,v,w)=vw,\,z(u,v,w)=u+w.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =\frac{1}{2\sqrt{u}} & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =w & \,\frac{∂y}{∂w} & =v \\ \frac{∂z}{∂u} & =1 & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{1}{2\sqrt{u}} & 0 & 0 \\ 0 & w & v \\ 1 & 0 & 1\end{aligned}| \\  & =\frac{1}{2\sqrt{u}}|\begin{aligned}w & v \\ 0 & 1\end{aligned}|+1|\begin{aligned}0 & 0 \\ w & v\end{aligned}| \\  & =\frac{1}{2\sqrt{u}}(w-0)+0 \\  & =\frac{w}{2\sqrt{u}}.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ \frac{w}{2\sqrt{u}} & =0 \\ w & =0.\end{aligned}
$$

The equation $w=0$ defines the plane $w=0,$ i.e., $uv$-plane.


## GENERATED evidence-only translated variant q-161815 #1

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}\sqrt{(u+2)} \\ (v-1)(w-3) \\ (u+2)+(w-3)\end{aligned}].
$$

Assume $u>-2$.

Field 1:
- The critical points lie on the plane $u=-2$.
- The critical points lie on the sphere ${(u+2)}^{2}+{(v-1)}^{2}+{(w-3)}^{2}=2.$
- The critical points lie on the plane $w=3$. [correct]
- The critical points lie on the plane $(u+2)=(w-3).$
- The critical points lie on the parabolic cylinder $(v-1)={(w-3)}^{2}.$

Worked solution:
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
x(u,v,w)=\sqrt{(u+2)},\,y(u,v,w)=(v-1)(w-3),\,z(u,v,w)=(u+2)+(w-3).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =\frac{1}{2\sqrt{(u+2)}} & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =(w-3) & \,\frac{∂y}{∂w} & =(v-1) \\ \frac{∂z}{∂u} & =1 & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{1}{2\sqrt{(u+2)}} & 0 & 0 \\ 0 & (w-3) & (v-1) \\ 1 & 0 & 1\end{aligned}| \\  & =\frac{1}{2\sqrt{(u+2)}}|\begin{aligned}(w-3) & (v-1) \\ 0 & 1\end{aligned}|+1|\begin{aligned}0 & 0 \\ (w-3) & (v-1)\end{aligned}| \\  & =\frac{1}{2\sqrt{(u+2)}}((w-3)-0)+0 \\  & =\frac{(w-3)}{2\sqrt{(u+2)}}.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ \frac{(w-3)}{2\sqrt{(u+2)}} & =0 \\ (w-3) & =0.\end{aligned}
$$

The equation $(w-3)=0$ defines the plane $(w-3)=0,$ i.e., plane $w=3$.


## GENERATED evidence-only translated variant q-161815 #2

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}\sqrt{(u-2)} \\ (v+3)(w+1) \\ (u-2)+(w+1)\end{aligned}].
$$

Assume $u>2$.

Field 1:
- The critical points lie on the plane $(u-2)=(w+1).$
- The critical points lie on the parabolic cylinder $(v+3)={(w+1)}^{2}.$
- The critical points lie on the sphere ${(u-2)}^{2}+{(v+3)}^{2}+{(w+1)}^{2}=2.$
- The critical points lie on the plane $w=-1$. [correct]
- The critical points lie on the plane $u=2$.

Worked solution:
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
x(u,v,w)=\sqrt{(u-2)},\,y(u,v,w)=(v+3)(w+1),\,z(u,v,w)=(u-2)+(w+1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =\frac{1}{2\sqrt{(u-2)}} & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =(w+1) & \,\frac{∂y}{∂w} & =(v+3) \\ \frac{∂z}{∂u} & =1 & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{1}{2\sqrt{(u-2)}} & 0 & 0 \\ 0 & (w+1) & (v+3) \\ 1 & 0 & 1\end{aligned}| \\  & =\frac{1}{2\sqrt{(u-2)}}|\begin{aligned}(w+1) & (v+3) \\ 0 & 1\end{aligned}|+1|\begin{aligned}0 & 0 \\ (w+1) & (v+3)\end{aligned}| \\  & =\frac{1}{2\sqrt{(u-2)}}((w+1)-0)+0 \\  & =\frac{(w+1)}{2\sqrt{(u-2)}}.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ \frac{(w+1)}{2\sqrt{(u-2)}} & =0 \\ (w+1) & =0.\end{aligned}
$$

The equation $(w+1)=0$ defines the plane $(w+1)=0,$ i.e., plane $w=-1$.


## Original replay q-161817

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: observed
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u \\ v{e}^{w} \\ 2u+v+3w\end{aligned}].
$$

Field 1:
- The critical points lie on the cylinder ${v}^{2}+{w}^{2}=0.$
- The critical points lie on the plane $v=3.$ [correct]
- The critical points lie on the sphere ${u}^{2}+{v}^{2}+{w}^{2}=3.$
- The critical points lie on the $uv-$plane.
- The critical points lie on the $uw-$plane.

Worked solution:
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
x(u,v,w)=u,\,y(u,v,w)=v{e}^{w},\,z(u,v,w)=2u+v+3w.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & ={e}^{w} & \,\frac{∂y}{∂w} & =v{e}^{w} \\ \frac{∂z}{∂u} & =2 & \,\frac{∂z}{∂v} & =1 & \,\frac{∂z}{∂w} & =3\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 0 \\ 0 & {e}^{w} & v{e}^{w} \\ 2 & 1 & 3\end{aligned}| \\  & =1|\begin{aligned}{e}^{w} & v{e}^{w} \\ 1 & 3\end{aligned}| \\  & =1(3{e}^{w}-v{e}^{w}) \\  & ={e}^{w}(3-v).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ {e}^{w}(3-v) & =0 \\ 3-v & =0.\end{aligned}
$$

The equation $3-v=0$ defines the plane $v=3.$


## GENERATED evidence-only translated variant q-161817 #1

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u+2) \\ (v-1){e}^{(w-3)} \\ 2(u+2)+(v-1)+3(w-3)\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $(v-1)=3.$ [correct]
- The critical points lie on the plane $v=1$.
- The critical points lie on the cylinder ${(v-1)}^{2}+{(w-3)}^{2}=0.$
- The critical points lie on the plane $w=3$.
- The critical points lie on the sphere ${(u+2)}^{2}+{(v-1)}^{2}+{(w-3)}^{2}=3.$

Worked solution:
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
x(u,v,w)=(u+2),\,y(u,v,w)=(v-1){e}^{(w-3)},\,z(u,v,w)=2(u+2)+(v-1)+3(w-3).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & ={e}^{(w-3)} & \,\frac{∂y}{∂w} & =(v-1){e}^{(w-3)} \\ \frac{∂z}{∂u} & =2 & \,\frac{∂z}{∂v} & =1 & \,\frac{∂z}{∂w} & =3\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 0 \\ 0 & {e}^{(w-3)} & (v-1){e}^{(w-3)} \\ 2 & 1 & 3\end{aligned}| \\  & =1|\begin{aligned}{e}^{(w-3)} & (v-1){e}^{(w-3)} \\ 1 & 3\end{aligned}| \\  & =1(3{e}^{(w-3)}-(v-1){e}^{(w-3)}) \\  & ={e}^{(w-3)}(3-(v-1)).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ {e}^{(w-3)}(3-(v-1)) & =0 \\ 3-(v-1) & =0.\end{aligned}
$$

The equation $3-(v-1)=0$ defines the plane $(v-1)=3.$


## GENERATED evidence-only translated variant q-161817 #2

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u-2) \\ (v+3){e}^{(w+1)} \\ 2(u-2)+(v+3)+3(w+1)\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $w=-1$.
- The critical points lie on the sphere ${(u-2)}^{2}+{(v+3)}^{2}+{(w+1)}^{2}=3.$
- The critical points lie on the plane $v=-3$.
- The critical points lie on the cylinder ${(v+3)}^{2}+{(w+1)}^{2}=0.$
- The critical points lie on the plane $(v+3)=3.$ [correct]

Worked solution:
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
x(u,v,w)=(u-2),\,y(u,v,w)=(v+3){e}^{(w+1)},\,z(u,v,w)=2(u-2)+(v+3)+3(w+1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & ={e}^{(w+1)} & \,\frac{∂y}{∂w} & =(v+3){e}^{(w+1)} \\ \frac{∂z}{∂u} & =2 & \,\frac{∂z}{∂v} & =1 & \,\frac{∂z}{∂w} & =3\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 0 \\ 0 & {e}^{(w+1)} & (v+3){e}^{(w+1)} \\ 2 & 1 & 3\end{aligned}| \\  & =1|\begin{aligned}{e}^{(w+1)} & (v+3){e}^{(w+1)} \\ 1 & 3\end{aligned}| \\  & =1(3{e}^{(w+1)}-(v+3){e}^{(w+1)}) \\  & ={e}^{(w+1)}(3-(v+3)).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ {e}^{(w+1)}(3-(v+3)) & =0 \\ 3-(v+3) & =0.\end{aligned}
$$

The equation $3-(v+3)=0$ defines the plane $(v+3)=3.$


## Original replay q-161818

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: observed
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u+3w \\ v+2w \\ {v}^{2}-u\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $v=u.$
- The critical points lie on the planes $v=\pm w.$
- The critical points lie on the parabolic cylinder $w=\frac{{v}^{2}}{2}.$
- The critical points lie on the plane $v=\frac{3}{4}.$ [correct]
- The critical points lie on the $uw-$ plane.

Worked solution:
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
x(u,v,w)=u+3w,\,y(u,v,w)=v+2w,\,z(u,v,w)={v}^{2}-u.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =3 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =2 \\ \frac{∂z}{∂u} & =-1 & \,\frac{∂z}{∂v} & =2v & \,\frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 3 \\ 0 & 1 & 2 \\ -1 & 2v & 0\end{aligned}| \\  & =1|\begin{aligned}1 & 2 \\ 2v & 0\end{aligned}|+3|\begin{aligned}0 & 1 \\ -1 & 2v\end{aligned}| \\  & =1(0-4v)+3(0+1) \\  & =3-4v.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 3-4v & =0.\end{aligned}
$$

The equation $3-4v=0$ defines the plane $v=\frac{3}{4}.$


## GENERATED evidence-only translated variant q-161818 #1

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u+2)+3(w-3) \\ (v-1)+2(w-3) \\ {(v-1)}^{2}-(u+2)\end{aligned}].
$$

Field 1:
- The critical points lie on the planes $(v-1)=\pm (w-3).$
- The critical points lie on the plane $v=1$.
- The critical points lie on the plane $(v-1)=(u+2).$
- The critical points lie on the plane $(v-1)=\frac{3}{4}.$ [correct]
- The critical points lie on the parabolic cylinder $(w-3)=\frac{{(v-1)}^{2}}{2}.$

Worked solution:
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
x(u,v,w)=(u+2)+3(w-3),\,y(u,v,w)=(v-1)+2(w-3),\,z(u,v,w)={(v-1)}^{2}-(u+2).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =3 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =2 \\ \frac{∂z}{∂u} & =-1 & \,\frac{∂z}{∂v} & =2(v-1) & \,\frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 3 \\ 0 & 1 & 2 \\ -1 & 2(v-1) & 0\end{aligned}| \\  & =1|\begin{aligned}1 & 2 \\ 2(v-1) & 0\end{aligned}|+3|\begin{aligned}0 & 1 \\ -1 & 2(v-1)\end{aligned}| \\  & =1(0-4(v-1))+3(0+1) \\  & =3-4(v-1).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 3-4(v-1) & =0.\end{aligned}
$$

The equation $3-4(v-1)=0$ defines the plane $(v-1)=\frac{3}{4}.$


## GENERATED evidence-only translated variant q-161818 #2

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u-2)+3(w+1) \\ (v+3)+2(w+1) \\ {(v+3)}^{2}-(u-2)\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $(v+3)=\frac{3}{4}.$ [correct]
- The critical points lie on the parabolic cylinder $(w+1)=\frac{{(v+3)}^{2}}{2}.$
- The critical points lie on the plane $v=-3$.
- The critical points lie on the plane $(v+3)=(u-2).$
- The critical points lie on the planes $(v+3)=\pm (w+1).$

Worked solution:
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
x(u,v,w)=(u-2)+3(w+1),\,y(u,v,w)=(v+3)+2(w+1),\,z(u,v,w)={(v+3)}^{2}-(u-2).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =3 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =2 \\ \frac{∂z}{∂u} & =-1 & \,\frac{∂z}{∂v} & =2(v+3) & \,\frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 3 \\ 0 & 1 & 2 \\ -1 & 2(v+3) & 0\end{aligned}| \\  & =1|\begin{aligned}1 & 2 \\ 2(v+3) & 0\end{aligned}|+3|\begin{aligned}0 & 1 \\ -1 & 2(v+3)\end{aligned}| \\  & =1(0-4(v+3))+3(0+1) \\  & =3-4(v+3).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 3-4(v+3) & =0.\end{aligned}
$$

The equation $3-4(v+3)=0$ defines the plane $(v+3)=\frac{3}{4}.$


## Original replay q-161813

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: observed
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}\frac{1}{u} \\ {v}^{2}+w \\ vw\end{aligned}].
$$

Field 1:
- The critical points lie on the parabolic cylinder $w=2{v}^{2}.$ [correct]
- The critical points lie on the plane $w=v.$
- The critical points lie on the $wv-$plane.
- The critical points lie on the $uv-$plane.
- The critical points lie on the plane $w=-2v.$

Worked solution:
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
x(u,v,w)=\frac{1}{u},\,y(u,v,w)={v}^{2}+w,\,z(u,v,w)=vw.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =-\frac{1}{{u}^{2}} & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =2v & \,\frac{∂y}{∂w} & =1 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =w & \,\frac{∂z}{∂w} & =v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}-\frac{1}{{u}^{2}} & 0 & 0 \\ 0 & 2v & 1 \\ 0 & w & v\end{aligned}| \\  & =-\frac{1}{{u}^{2}}|\begin{aligned}2v & 1 \\ w & v\end{aligned}| \\  & =-\frac{1}{{u}^{2}}(2{v}^{2}-w).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ -\frac{1}{{u}^{2}}(2{v}^{2}-w) & =0 \\ w-2{v}^{2} & =0.\end{aligned}
$$

The equation $w-2{v}^{2}=0$ defines the parabolic cylinder $w=2{v}^{2}.$


## GENERATED evidence-only translated variant q-161813 #1

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}\frac{1}{(u+2)} \\ {(v-1)}^{2}+(w-3) \\ (v-1)(w-3)\end{aligned}].
$$

Assume $u\ne -2$.

Field 1:
- The critical points lie on the plane $(w-3)=(v-1).$
- The critical points lie on the plane $(w-3)=-2(v-1).$
- The critical points lie on the parabolic cylinder $(w-3)=2{(v-1)}^{2}.$ [correct]
- The critical points lie on the plane $w=3$.
- The critical points lie on the plane $u=-2$.

Worked solution:
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
x(u,v,w)=\frac{1}{(u+2)},\,y(u,v,w)={(v-1)}^{2}+(w-3),\,z(u,v,w)=(v-1)(w-3).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =-\frac{1}{{(u+2)}^{2}} & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =2(v-1) & \,\frac{∂y}{∂w} & =1 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =(w-3) & \,\frac{∂z}{∂w} & =(v-1)\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}-\frac{1}{{(u+2)}^{2}} & 0 & 0 \\ 0 & 2(v-1) & 1 \\ 0 & (w-3) & (v-1)\end{aligned}| \\  & =-\frac{1}{{(u+2)}^{2}}|\begin{aligned}2(v-1) & 1 \\ (w-3) & (v-1)\end{aligned}| \\  & =-\frac{1}{{(u+2)}^{2}}(2{(v-1)}^{2}-(w-3)).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ -\frac{1}{{(u+2)}^{2}}(2{(v-1)}^{2}-(w-3)) & =0 \\ (w-3)-2{(v-1)}^{2} & =0.\end{aligned}
$$

The equation $(w-3)-2{(v-1)}^{2}=0$ defines the parabolic cylinder $(w-3)=2{(v-1)}^{2}.$


## GENERATED evidence-only translated variant q-161813 #2

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}\frac{1}{(u-2)} \\ {(v+3)}^{2}+(w+1) \\ (v+3)(w+1)\end{aligned}].
$$

Assume $u\ne 2$.

Field 1:
- The critical points lie on the plane $w=-1$.
- The critical points lie on the plane $u=2$.
- The critical points lie on the plane $(w+1)=-2(v+3).$
- The critical points lie on the parabolic cylinder $(w+1)=2{(v+3)}^{2}.$ [correct]
- The critical points lie on the plane $(w+1)=(v+3).$

Worked solution:
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
x(u,v,w)=\frac{1}{(u-2)},\,y(u,v,w)={(v+3)}^{2}+(w+1),\,z(u,v,w)=(v+3)(w+1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =-\frac{1}{{(u-2)}^{2}} & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =2(v+3) & \,\frac{∂y}{∂w} & =1 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =(w+1) & \,\frac{∂z}{∂w} & =(v+3)\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}-\frac{1}{{(u-2)}^{2}} & 0 & 0 \\ 0 & 2(v+3) & 1 \\ 0 & (w+1) & (v+3)\end{aligned}| \\  & =-\frac{1}{{(u-2)}^{2}}|\begin{aligned}2(v+3) & 1 \\ (w+1) & (v+3)\end{aligned}| \\  & =-\frac{1}{{(u-2)}^{2}}(2{(v+3)}^{2}-(w+1)).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ -\frac{1}{{(u-2)}^{2}}(2{(v+3)}^{2}-(w+1)) & =0 \\ (w+1)-2{(v+3)}^{2} & =0.\end{aligned}
$$

The equation $(w+1)-2{(v+3)}^{2}=0$ defines the parabolic cylinder $(w+1)=2{(v+3)}^{2}.$


## Original replay q-161814

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: observed
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u+2w \\ v-u \\ uw\end{aligned}].
$$

Field 1:
- The critical points lie on the parabolic cylinder $v={u}^{2}.$
- The critical points lie on the elliptic cylinder ${u}^{2}+2{w}^{2}=1.$
- The critical points lie on the plane $u+v-2w=0.$
- The critical points lie on the plane $u=2w.$ [correct]
- The critical points lie on the $vw-$ plane.

Worked solution:
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
x(u,v,w)=u+2w,\,y(u,v,w)=v-u,\,z(u,v,w)=uw.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =2 \\ \frac{∂y}{∂u} & =-1 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =w & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & =u\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 2 \\ -1 & 1 & 0 \\ w & 0 & u\end{aligned}| \\  & =1|\begin{aligned}1 & 0 \\ 0 & u\end{aligned}|+2|\begin{aligned}-1 & 1 \\ w & 0\end{aligned}| \\  & =1(u-0)+2(0-w) \\  & =u-2w.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ u-2w & =0.\end{aligned}
$$

The equation $u-2w=0$ defines the plane $u=2w.$


## GENERATED evidence-only translated variant q-161814 #1

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u+2)+2(w-3) \\ (v-1)-(u+2) \\ (u+2)(w-3)\end{aligned}].
$$

Field 1:
- The critical points lie on the elliptic cylinder ${(u+2)}^{2}+2{(w-3)}^{2}=1.$
- The critical points lie on the plane $u=-2$.
- The critical points lie on the parabolic cylinder $(v-1)={(u+2)}^{2}.$
- The critical points lie on the plane $(u+2)=2(w-3).$ [correct]
- The critical points lie on the plane $(u+2)+(v-1)-2(w-3)=0.$

Worked solution:
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
x(u,v,w)=(u+2)+2(w-3),\,y(u,v,w)=(v-1)-(u+2),\,z(u,v,w)=(u+2)(w-3).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =2 \\ \frac{∂y}{∂u} & =-1 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =(w-3) & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & =(u+2)\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 2 \\ -1 & 1 & 0 \\ (w-3) & 0 & (u+2)\end{aligned}| \\  & =1|\begin{aligned}1 & 0 \\ 0 & (u+2)\end{aligned}|+2|\begin{aligned}-1 & 1 \\ (w-3) & 0\end{aligned}| \\  & =1((u+2)-0)+2(0-(w-3)) \\  & =(u+2)-2(w-3).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ (u+2)-2(w-3) & =0.\end{aligned}
$$

The equation $(u+2)-2(w-3)=0$ defines the plane $(u+2)=2(w-3).$


## GENERATED evidence-only translated variant q-161814 #2

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u-2)+2(w+1) \\ (v+3)-(u-2) \\ (u-2)(w+1)\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $(u-2)=2(w+1).$ [correct]
- The critical points lie on the plane $(u-2)+(v+3)-2(w+1)=0.$
- The critical points lie on the plane $u=2$.
- The critical points lie on the parabolic cylinder $(v+3)={(u-2)}^{2}.$
- The critical points lie on the elliptic cylinder ${(u-2)}^{2}+2{(w+1)}^{2}=1.$

Worked solution:
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
x(u,v,w)=(u-2)+2(w+1),\,y(u,v,w)=(v+3)-(u-2),\,z(u,v,w)=(u-2)(w+1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =2 \\ \frac{∂y}{∂u} & =-1 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =(w+1) & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & =(u-2)\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 2 \\ -1 & 1 & 0 \\ (w+1) & 0 & (u-2)\end{aligned}| \\  & =1|\begin{aligned}1 & 0 \\ 0 & (u-2)\end{aligned}|+2|\begin{aligned}-1 & 1 \\ (w+1) & 0\end{aligned}| \\  & =1((u-2)-0)+2(0-(w+1)) \\  & =(u-2)-2(w+1).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ (u-2)-2(w+1) & =0.\end{aligned}
$$

The equation $(u-2)-2(w+1)=0$ defines the plane $(u-2)=2(w+1).$


## Original replay q-161816

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: observed
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{e}^{u} \\ {e}^{u+w} \\ uv+w\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $2u+v+w=0.$
- The critical points lie on the parabolic cylinder $w=-2{v}^{2}.$
- The critical points lie on the $vw-$plane. [correct]
- The critical points lie on the parabolic cylinder $w={u}^{2}.$
- The critical points lie on the plane $w=-2u.$

Worked solution:
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
x(u,v,w)={e}^{u},\,y(u,v,w)={e}^{u+w},\,z(u,v,w)=uv+w.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & ={e}^{u} & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & ={e}^{u+w} & \,\frac{∂y}{∂v} & =0 & \,\frac{∂y}{∂w} & ={e}^{u+w} \\ \frac{∂z}{∂u} & =v & \,\frac{∂z}{∂v} & =u & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}{e}^{u} & 0 & 0 \\ {e}^{u+w} & 0 & {e}^{u+w} \\ v & u & 1\end{aligned}| \\  & ={e}^{u}|\begin{aligned}0 & {e}^{u+w} \\ u & 1\end{aligned}| \\  & ={e}^{u}(0-u{e}^{u+w}) \\  & =-u{e}^{2u+w}.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ -u{e}^{2u+w} & =0 \\ u & =0.\end{aligned}
$$

The equation $u=0$ defines the plane $u=0,$ i.e., $vw$-plane.


## GENERATED evidence-only translated variant q-161816 #1

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{e}^{(u+2)} \\ {e}^{(u+2)+(w-3)} \\ (u+2)(v-1)+(w-3)\end{aligned}].
$$

Field 1:
- The critical points lie on the parabolic cylinder $(w-3)=-2{(v-1)}^{2}.$
- The critical points lie on the plane $(w-3)=-2(u+2).$
- The critical points lie on the plane $2(u+2)+(v-1)+(w-3)=0.$
- The critical points lie on the parabolic cylinder $(w-3)={(u+2)}^{2}.$
- The critical points lie on the plane $u=-2$. [correct]

Worked solution:
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
x(u,v,w)={e}^{(u+2)},\,y(u,v,w)={e}^{(u+2)+(w-3)},\,z(u,v,w)=(u+2)(v-1)+(w-3).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & ={e}^{(u+2)} & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & ={e}^{(u+2)+(w-3)} & \,\frac{∂y}{∂v} & =0 & \,\frac{∂y}{∂w} & ={e}^{(u+2)+(w-3)} \\ \frac{∂z}{∂u} & =(v-1) & \,\frac{∂z}{∂v} & =(u+2) & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}{e}^{(u+2)} & 0 & 0 \\ {e}^{(u+2)+(w-3)} & 0 & {e}^{(u+2)+(w-3)} \\ (v-1) & (u+2) & 1\end{aligned}| \\  & ={e}^{(u+2)}|\begin{aligned}0 & {e}^{(u+2)+(w-3)} \\ (u+2) & 1\end{aligned}| \\  & ={e}^{(u+2)}(0-(u+2){e}^{(u+2)+(w-3)}) \\  & =-(u+2){e}^{2(u+2)+(w-3)}.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ -(u+2){e}^{2(u+2)+(w-3)} & =0 \\ (u+2) & =0.\end{aligned}
$$

The equation $(u+2)=0$ defines the plane $(u+2)=0,$ i.e., plane $u=-2$.


## GENERATED evidence-only translated variant q-161816 #2

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{e}^{(u-2)} \\ {e}^{(u-2)+(w+1)} \\ (u-2)(v+3)+(w+1)\end{aligned}].
$$

Field 1:
- The critical points lie on the parabolic cylinder $(w+1)={(u-2)}^{2}.$
- The critical points lie on the plane $u=2$. [correct]
- The critical points lie on the plane $(w+1)=-2(u-2).$
- The critical points lie on the plane $2(u-2)+(v+3)+(w+1)=0.$
- The critical points lie on the parabolic cylinder $(w+1)=-2{(v+3)}^{2}.$

Worked solution:
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
x(u,v,w)={e}^{(u-2)},\,y(u,v,w)={e}^{(u-2)+(w+1)},\,z(u,v,w)=(u-2)(v+3)+(w+1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & ={e}^{(u-2)} & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & ={e}^{(u-2)+(w+1)} & \,\frac{∂y}{∂v} & =0 & \,\frac{∂y}{∂w} & ={e}^{(u-2)+(w+1)} \\ \frac{∂z}{∂u} & =(v+3) & \,\frac{∂z}{∂v} & =(u-2) & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}{e}^{(u-2)} & 0 & 0 \\ {e}^{(u-2)+(w+1)} & 0 & {e}^{(u-2)+(w+1)} \\ (v+3) & (u-2) & 1\end{aligned}| \\  & ={e}^{(u-2)}|\begin{aligned}0 & {e}^{(u-2)+(w+1)} \\ (u-2) & 1\end{aligned}| \\  & ={e}^{(u-2)}(0-(u-2){e}^{(u-2)+(w+1)}) \\  & =-(u-2){e}^{2(u-2)+(w+1)}.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ -(u-2){e}^{2(u-2)+(w+1)} & =0 \\ (u-2) & =0.\end{aligned}
$$

The equation $(u-2)=0$ defines the plane $(u-2)=0,$ i.e., plane $u=2$.


## Original replay q-161810

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: observed
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u+vw \\ {v}^{2} \\ w+v\end{aligned}].
$$

Field 1:
- The critical points lie on the $vw-$plane.
- The critical points lie on the sphere ${x}^{2}+{y}^{2}+{z}^{2}=1.$
- The critical points lie on the $uw-$plane. [correct]
- The critical points lie on the plane $v=u.$
- The critical points lie on the plane $v=1.$

Worked solution:
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
x(u,v,w)=u+vw,\,y(u,v,w)={v}^{2},\,z(u,v,w)=w+v.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =w & \,\frac{∂x}{∂w} & =v \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =2v & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =1 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & w & v \\ 0 & 2v & 0 \\ 0 & 1 & 1\end{aligned}| \\  & =1|\begin{aligned}2v & 0 \\ 1 & 1\end{aligned}| \\  & =1(2v-0) \\  & =2v.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 2v & =0 \\ v & =0.\end{aligned}
$$

The equation $v=0$ defines the plane $v=0,$ i.e., $uw$-plane.


## GENERATED evidence-only translated variant q-161810 #1

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u+2)+(v-1)(w-3) \\ {(v-1)}^{2} \\ (w-3)+(v-1)\end{aligned}].
$$

Field 1:
- The critical points lie on the sphere ${x}^{2}+{y}^{2}+{z}^{2}=1.$
- The critical points lie on the plane $(v-1)=1.$
- The critical points lie on the plane $u=-2$.
- The critical points lie on the plane $(v-1)=(u+2).$
- The critical points lie on the plane $v=1$. [correct]

Worked solution:
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
x(u,v,w)=(u+2)+(v-1)(w-3),\,y(u,v,w)={(v-1)}^{2},\,z(u,v,w)=(w-3)+(v-1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =(w-3) & \,\frac{∂x}{∂w} & =(v-1) \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =2(v-1) & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =1 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & (w-3) & (v-1) \\ 0 & 2(v-1) & 0 \\ 0 & 1 & 1\end{aligned}| \\  & =1|\begin{aligned}2(v-1) & 0 \\ 1 & 1\end{aligned}| \\  & =1(2(v-1)-0) \\  & =2(v-1).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 2(v-1) & =0 \\ (v-1) & =0.\end{aligned}
$$

The equation $(v-1)=0$ defines the plane $(v-1)=0,$ i.e., plane $v=1$.


## GENERATED evidence-only translated variant q-161810 #2

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u-2)+(v+3)(w+1) \\ {(v+3)}^{2} \\ (w+1)+(v+3)\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $(v+3)=(u-2).$
- The critical points lie on the plane $v=-3$. [correct]
- The critical points lie on the plane $(v+3)=1.$
- The critical points lie on the plane $u=2$.
- The critical points lie on the sphere ${x}^{2}+{y}^{2}+{z}^{2}=1.$

Worked solution:
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
x(u,v,w)=(u-2)+(v+3)(w+1),\,y(u,v,w)={(v+3)}^{2},\,z(u,v,w)=(w+1)+(v+3).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =(w+1) & \,\frac{∂x}{∂w} & =(v+3) \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =2(v+3) & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =1 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & (w+1) & (v+3) \\ 0 & 2(v+3) & 0 \\ 0 & 1 & 1\end{aligned}| \\  & =1|\begin{aligned}2(v+3) & 0 \\ 1 & 1\end{aligned}| \\  & =1(2(v+3)-0) \\  & =2(v+3).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 2(v+3) & =0 \\ (v+3) & =0.\end{aligned}
$$

The equation $(v+3)=0$ defines the plane $(v+3)=0,$ i.e., plane $v=-3$.


## Original replay q-161811

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: observed
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{e}^{u}+v \\ v+w \\ vw\end{aligned}].
$$

Field 1:
- The critical points lie on the $vw-$plane.
- The critical points lie on the plane $v=w.$ [correct]
- The critical points lie on the parabolic cylinder $v=2{w}^{2}.$
- The critical points lie on the sphere ${x}^{2}+{y}^{2}+{z}^{2}=4.$
- The critical points lie on the $uv-$plane.

Worked solution:
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
x(u,v,w)={e}^{u}+v,\,y(u,v,w)=v+w,\,z(u,v,w)=vw.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & ={e}^{u} & \,\frac{∂x}{∂v} & =1 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =1 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =w & \,\frac{∂z}{∂w} & =v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}{e}^{u} & 1 & 0 \\ 0 & 1 & 1 \\ 0 & w & v\end{aligned}| \\  & ={e}^{u}|\begin{aligned}1 & 1 \\ w & v\end{aligned}| \\  & ={e}^{u}(v-w).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ {e}^{u}(v-w) & =0 \\ v-w & =0.\end{aligned}
$$

The equation $v-w=0$ defines the plane $v=w.$


## GENERATED evidence-only translated variant q-161811 #1

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{e}^{(u+2)}+(v-1) \\ (v-1)+(w-3) \\ (v-1)(w-3)\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $(v-1)=(w-3).$ [correct]
- The critical points lie on the plane $w=3$.
- The critical points lie on the plane $u=-2$.
- The critical points lie on the sphere ${x}^{2}+{y}^{2}+{z}^{2}=4.$
- The critical points lie on the parabolic cylinder $(v-1)=2{(w-3)}^{2}.$

Worked solution:
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
x(u,v,w)={e}^{(u+2)}+(v-1),\,y(u,v,w)=(v-1)+(w-3),\,z(u,v,w)=(v-1)(w-3).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & ={e}^{(u+2)} & \,\frac{∂x}{∂v} & =1 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =1 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =(w-3) & \,\frac{∂z}{∂w} & =(v-1)\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}{e}^{(u+2)} & 1 & 0 \\ 0 & 1 & 1 \\ 0 & (w-3) & (v-1)\end{aligned}| \\  & ={e}^{(u+2)}|\begin{aligned}1 & 1 \\ (w-3) & (v-1)\end{aligned}| \\  & ={e}^{(u+2)}((v-1)-(w-3)).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ {e}^{(u+2)}((v-1)-(w-3)) & =0 \\ (v-1)-(w-3) & =0.\end{aligned}
$$

The equation $(v-1)-(w-3)=0$ defines the plane $(v-1)=(w-3).$


## GENERATED evidence-only translated variant q-161811 #2

Difficulty: moderate | EVIDENCE ONLY | Origin: observed translated template | Profile: repaired
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{e}^{(u-2)}+(v+3) \\ (v+3)+(w+1) \\ (v+3)(w+1)\end{aligned}].
$$

Field 1:
- The critical points lie on the sphere ${x}^{2}+{y}^{2}+{z}^{2}=4.$
- The critical points lie on the parabolic cylinder $(v+3)=2{(w+1)}^{2}.$
- The critical points lie on the plane $w=-1$.
- The critical points lie on the plane $u=2$.
- The critical points lie on the plane $(v+3)=(w+1).$ [correct]

Worked solution:
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
x(u,v,w)={e}^{(u-2)}+(v+3),\,y(u,v,w)=(v+3)+(w+1),\,z(u,v,w)=(v+3)(w+1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & ={e}^{(u-2)} & \,\frac{∂x}{∂v} & =1 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =1 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =(w+1) & \,\frac{∂z}{∂w} & =(v+3)\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}{e}^{(u-2)} & 1 & 0 \\ 0 & 1 & 1 \\ 0 & (w+1) & (v+3)\end{aligned}| \\  & ={e}^{(u-2)}|\begin{aligned}1 & 1 \\ (w+1) & (v+3)\end{aligned}| \\  & ={e}^{(u-2)}((v+3)-(w+1)).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ {e}^{(u-2)}((v+3)-(w+1)) & =0 \\ (v+3)-(w+1) & =0.\end{aligned}
$$

The equation $(v+3)-(w+1)=0$ defines the plane $(v+3)=(w+1).$


## GENERATED authored easy #1

Difficulty: easy | GENERATED normal learning record | Origin: authored missing-level extension | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}\left(u - 2\right)^{2} \\ v \\ w\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $u - 2=0.$ [correct]
- The critical points lie on the plane $u=0.$
- The critical points lie on the plane $v - 2=0.$
- The critical points lie on the plane $u + 2=0.$
- The critical points lie on the plane $w - 2=0.$

Worked solution:
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
x(u,v,w)=\left(u - 2\right)^{2},\,y(u,v,w)=v,\,z(u,v,w)=w.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2 u - 4 & \frac{∂x}{∂v} & =0 & \frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \frac{∂y}{∂v} & =1 & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =0 & \frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2 u - 4 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{aligned}| \\  & =(2 u - 4)|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}| \\  & =(2 u - 4)(1\cdot(1)-(0)\cdot(0)) \\  & =2 \left(u - 2\right).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 2 \left(u - 2\right) & =0.\end{aligned}
$$

The critical points lie on the plane $u - 2=0.$


## GENERATED authored easy #2

Difficulty: easy | GENERATED normal learning record | Origin: authored missing-level extension | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}\left(u - 5\right)^{2} \\ v \\ w\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $u + 5=0.$
- The critical points lie on the plane $u=0.$
- The critical points lie on the plane $v - 5=0.$
- The critical points lie on the plane $u - 5=0.$ [correct]
- The critical points lie on the plane $w - 5=0.$

Worked solution:
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
x(u,v,w)=\left(u - 5\right)^{2},\,y(u,v,w)=v,\,z(u,v,w)=w.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2 u - 10 & \frac{∂x}{∂v} & =0 & \frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \frac{∂y}{∂v} & =1 & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =0 & \frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2 u - 10 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{aligned}| \\  & =(2 u - 10)|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}| \\  & =(2 u - 10)(1\cdot(1)-(0)\cdot(0)) \\  & =2 \left(u - 5\right).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 2 \left(u - 5\right) & =0.\end{aligned}
$$

The critical points lie on the plane $u - 5=0.$


## GENERATED authored easy #3

Difficulty: easy | GENERATED normal learning record | Origin: authored missing-level extension | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}\left(u + 4\right)^{2} \\ v \\ w\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $u + 4=0.$ [correct]
- The critical points lie on the plane $u - 4=0.$
- The critical points lie on the plane $u=0.$
- The critical points lie on the plane $v + 4=0.$
- The critical points lie on the plane $w + 4=0.$

Worked solution:
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
x(u,v,w)=\left(u + 4\right)^{2},\,y(u,v,w)=v,\,z(u,v,w)=w.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2 u + 8 & \frac{∂x}{∂v} & =0 & \frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \frac{∂y}{∂v} & =1 & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =0 & \frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2 u + 8 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{aligned}| \\  & =(2 u + 8)|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}| \\  & =(2 u + 8)(1\cdot(1)-(0)\cdot(0)) \\  & =2 \left(u + 4\right).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 2 \left(u + 4\right) & =0.\end{aligned}
$$

The critical points lie on the plane $u + 4=0.$


## GENERATED authored moderate #1

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u-3) \\ v{e}^{(w+3)} \\ 2(u-3)+v+3(w+3)\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $3 - v=0.$ [correct]
- The critical points are exactly the domain points satisfying $- w=0.$
- The critical points are exactly the domain points satisfying $v + 3=0.$
- The critical points are exactly the domain points satisfying $w + 3=0.$
- The critical points are exactly the domain points satisfying $v=0.$

Worked solution:
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
x(u,v,w)=(u-3),\,y(u,v,w)=v{e}^{(w+3)},\,z(u,v,w)=2(u-3)+v+3(w+3).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & ={e}^{(w+3)} & \,\frac{∂y}{∂w} & =v{e}^{(w+3)} \\ \frac{∂z}{∂u} & =2 & \,\frac{∂z}{∂v} & =1 & \,\frac{∂z}{∂w} & =3\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 0 \\ 0 & {e}^{(w+3)} & v{e}^{(w+3)} \\ 2 & 1 & 3\end{aligned}| \\  & =1|\begin{aligned}{e}^{(w+3)} & v{e}^{(w+3)} \\ 1 & 3\end{aligned}| \\  & =1(3{e}^{(w+3)}-v{e}^{(w+3)}) \\  & ={e}^{(w+3)}(3-v).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ {e}^{(w+3)}(3-v) & =0 \\ 3-v & =0.\end{aligned}
$$

The equation $3-v=0$ defines the plane $v=3.$


## GENERATED authored moderate #2

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{(u-1)}^{2}-(v-3) \\ {(u-1)}^{2}+(v-3) \\ {e}^{(w-3)}\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $u^{2} - 2 u - v + 4=0.$
- The critical points are exactly the domain points satisfying $w - 3=0.$
- The critical points are exactly the domain points satisfying $u^{2} - 2 u + v - 2=0.$
- The critical points are exactly the domain points satisfying $v - 3=0.$
- The critical points are exactly the domain points satisfying $u - 1=0.$ [correct]

Worked solution:
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
x(u,v,w)={(u-1)}^{2}-(v-3),\,y(u,v,w)={(u-1)}^{2}+(v-3),\,z(u,v,w)={e}^{(w-3)}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2(u-1) & \,\frac{∂x}{∂v} & =-1 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =2(u-1) & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & ={e}^{(w-3)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2(u-1) & -1 & 0 \\ 2(u-1) & 1 & 0 \\ 0 & 0 & {e}^{(w-3)}\end{aligned}| \\  & ={e}^{(w-3)}|\begin{aligned}2(u-1) & -1 \\ 2(u-1) & 1\end{aligned}| \\  & ={e}^{(w-3)}(2(u-1)+2(u-1)) \\  & =4(u-1){e}^{(w-3)}.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 4(u-1){e}^{(w-3)} & =0 \\ (u-1) & =0.\end{aligned}
$$

The equation $(u-1)=0$ defines the plane $(u-1)=0,$ i.e., plane $u=1$.


## GENERATED authored moderate #3

Difficulty: moderate | GENERATED normal learning record | Origin: authored bank and template extension | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u v \\ 3 u + 7 v \\ w\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $3 u + 7 v=0.$
- The critical points lie on the plane $- 3 u + 7 v=0.$ [correct]
- The critical points lie on the plane $- u + 7 v=0.$
- The critical points lie on the plane $7 u - 3 v=0.$
- The critical points lie on the plane $- 3 u + v=0.$

Worked solution:
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
x(u,v,w)=u v,\,y(u,v,w)=3 u + 7 v,\,z(u,v,w)=w.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =v & \frac{∂x}{∂v} & =u & \frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =3 & \frac{∂y}{∂v} & =7 & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \frac{∂z}{∂v} & =0 & \frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}v & u & 0 \\ 3 & 7 & 0 \\ 0 & 0 & 1\end{aligned}| \\  & =(v)|\begin{aligned}7 & 0 \\ 0 & 1\end{aligned}|+(- u)|\begin{aligned}3 & 0 \\ 0 & 1\end{aligned}| \\  & =(v)(7\cdot(1)-(0)\cdot(0))+(- u)(3\cdot(1)-(0)\cdot(0)) \\  & =- 3 u + 7 v.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ - 3 u + 7 v & =0.\end{aligned}
$$

The critical points lie on the plane $- 3 u + 7 v=0.$


## GENERATED authored hard #1

Difficulty: hard | GENERATED normal learning record | Origin: authored missing-level extension | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u + 3 v - 4 w \\ u^{2} + v \\ 4 u^{2} + 3 u + w\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $26 u + 12=0.$
- The critical points lie on the plane $26 u + 13=0.$ [correct]
- The critical points lie on the plane $32 u + 13=0.$
- The critical points lie on the plane $38 u + 13=0.$
- The critical points lie on the plane $1 - 6 u=0.$

Worked solution:
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
x(u,v,w)=u + 3 v - 4 w,\,y(u,v,w)=u^{2} + v,\,z(u,v,w)=4 u^{2} + 3 u + w.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \frac{∂x}{∂v} & =3 & \frac{∂x}{∂w} & =-4 \\ \frac{∂y}{∂u} & =2 u & \frac{∂y}{∂v} & =1 & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =8 u + 3 & \frac{∂z}{∂v} & =0 & \frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 3 & -4 \\ 2 u & 1 & 0 \\ 8 u + 3 & 0 & 1\end{aligned}| \\  & =(1)|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|+(-3)|\begin{aligned}2 u & 0 \\ 8 u + 3 & 1\end{aligned}|+(-4)|\begin{aligned}2 u & 1 \\ 8 u + 3 & 0\end{aligned}| \\  & =(1)(1\cdot(1)-(0)\cdot(0))+(-3)(2 u\cdot(1)-(0)\cdot(8 u + 3))+(-4)(2 u\cdot(0)-(1)\cdot(8 u + 3)) \\  & =13 \left(2 u + 1\right).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 13 \left(2 u + 1\right) & =0.\end{aligned}
$$

The critical points lie on the plane $26 u + 13=0.$


## GENERATED authored hard #2

Difficulty: hard | GENERATED normal learning record | Origin: authored missing-level extension | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u - 3 v + w \\ - 3 u^{2} + v \\ 4 u^{2} + 4 u + w\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $- 8 u - 3=0.$
- The critical points lie on the plane $1 - 18 u=0.$
- The critical points lie on the plane $- 26 u - 3=0.$ [correct]
- The critical points lie on the plane $- 26 u - 4=0.$
- The critical points lie on the plane $10 u - 3=0.$

Worked solution:
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
x(u,v,w)=u - 3 v + w,\,y(u,v,w)=- 3 u^{2} + v,\,z(u,v,w)=4 u^{2} + 4 u + w.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \frac{∂x}{∂v} & =-3 & \frac{∂x}{∂w} & =1 \\ \frac{∂y}{∂u} & =- 6 u & \frac{∂y}{∂v} & =1 & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =8 u + 4 & \frac{∂z}{∂v} & =0 & \frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & -3 & 1 \\ - 6 u & 1 & 0 \\ 8 u + 4 & 0 & 1\end{aligned}| \\  & =(1)|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|+(3)|\begin{aligned}- 6 u & 0 \\ 8 u + 4 & 1\end{aligned}|+(1)|\begin{aligned}- 6 u & 1 \\ 8 u + 4 & 0\end{aligned}| \\  & =(1)(1\cdot(1)-(0)\cdot(0))+(3)(- 6 u\cdot(1)-(0)\cdot(8 u + 4))+(1)(- 6 u\cdot(0)-(1)\cdot(8 u + 4)) \\  & =- 26 u - 3.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ - 26 u - 3 & =0.\end{aligned}
$$

The critical points lie on the plane $- 26 u - 3=0.$


## GENERATED authored hard #3

Difficulty: hard | GENERATED normal learning record | Origin: authored missing-level extension | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u + v - w \\ - 4 u^{2} + v \\ - 2 u^{2} + 3 u + w\end{aligned}].
$$

Field 1:
- The critical points lie on the plane $4 u + 4=0.$ [correct]
- The critical points lie on the plane $4 - 4 u=0.$
- The critical points lie on the plane $4 u + 3=0.$
- The critical points lie on the plane $8 u + 1=0.$
- The critical points lie on the plane $4 - 12 u=0.$

Worked solution:
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
x(u,v,w)=u + v - w,\,y(u,v,w)=- 4 u^{2} + v,\,z(u,v,w)=- 2 u^{2} + 3 u + w.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \frac{∂x}{∂v} & =1 & \frac{∂x}{∂w} & =-1 \\ \frac{∂y}{∂u} & =- 8 u & \frac{∂y}{∂v} & =1 & \frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =3 - 4 u & \frac{∂z}{∂v} & =0 & \frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 1 & -1 \\ - 8 u & 1 & 0 \\ 3 - 4 u & 0 & 1\end{aligned}| \\  & =(1)|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|+(-1)|\begin{aligned}- 8 u & 0 \\ 3 - 4 u & 1\end{aligned}|+(-1)|\begin{aligned}- 8 u & 1 \\ 3 - 4 u & 0\end{aligned}| \\  & =(1)(1\cdot(1)-(0)\cdot(0))+(-1)(- 8 u\cdot(1)-(0)\cdot(3 - 4 u))+(-1)(- 8 u\cdot(0)-(1)\cdot(3 - 4 u)) \\  & =4 \left(u + 1\right).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 4 \left(u + 1\right) & =0.\end{aligned}
$$

The critical points lie on the plane $4 u + 4=0.$


## GENERATED normal authored method bank q-161819 #1

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{u}^{2}-{w}^{2} \\ w{e}^{u} \\ u-v\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $u + w=0.$
- The critical points are exactly the domain points satisfying $u - w^{2}=0.$
- The critical points are exactly the domain points satisfying $u + w^{2}=0.$ [correct]
- The critical points are exactly the domain points satisfying $u=0.$
- The critical points are exactly the domain points satisfying $w=0.$

Worked solution:
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
x(u,v,w)={u}^{2}-{w}^{2},\,y(u,v,w)=w{e}^{u},\,z(u,v,w)=u-v.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2u & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =-2w \\ \frac{∂y}{∂u} & =w{e}^{u} & \,\frac{∂y}{∂v} & =0 & \,\frac{∂y}{∂w} & ={e}^{u} \\ \frac{∂z}{∂u} & =1 & \,\frac{∂z}{∂v} & =-1 & \,\frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2u & 0 & -2w \\ w{e}^{u} & 0 & {e}^{u} \\ 1 & -1 & 0\end{aligned}| \\  & =2u|\begin{aligned}0 & {e}^{u} \\ -1 & 0\end{aligned}|-2w|\begin{aligned}w{e}^{u} & 0 \\ 1 & -1\end{aligned}| \\  & =2u(0+{e}^{u})-2w(-w{e}^{u}-0) \\  & =2u{e}^{u}+2{w}^{2}{e}^{u} \\  & =2{e}^{u}({w}^{2}+u).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 2{e}^{u}({w}^{2}+u) & =0 \\ {w}^{2}+u & =0.\end{aligned}
$$

The equation ${w}^{2}+u=0$ defines the parabolic cylinder $u=-{w}^{2}.$


## GENERATED normal authored method bank q-161819 #2

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{(u+3)}^{2}-{(w+1)}^{2} \\ (w+1){e}^{(u+3)} \\ (u+3)-(v-2)\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $u + w + 4=0.$
- The critical points are exactly the domain points satisfying $w + 1=0.$
- The critical points are exactly the domain points satisfying $u + 3=0.$
- The critical points are exactly the domain points satisfying $u + w^{2} + 2 w + 4=0.$ [correct]
- The critical points are exactly the domain points satisfying $u - w^{2} - 2 w + 2=0.$

Worked solution:
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
x(u,v,w)={(u+3)}^{2}-{(w+1)}^{2},\,y(u,v,w)=(w+1){e}^{(u+3)},\,z(u,v,w)=(u+3)-(v-2).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2(u+3) & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =-2(w+1) \\ \frac{∂y}{∂u} & =(w+1){e}^{(u+3)} & \,\frac{∂y}{∂v} & =0 & \,\frac{∂y}{∂w} & ={e}^{(u+3)} \\ \frac{∂z}{∂u} & =1 & \,\frac{∂z}{∂v} & =-1 & \,\frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2(u+3) & 0 & -2(w+1) \\ (w+1){e}^{(u+3)} & 0 & {e}^{(u+3)} \\ 1 & -1 & 0\end{aligned}| \\  & =2(u+3)|\begin{aligned}0 & {e}^{(u+3)} \\ -1 & 0\end{aligned}|-2(w+1)|\begin{aligned}(w+1){e}^{(u+3)} & 0 \\ 1 & -1\end{aligned}| \\  & =2(u+3)(0+{e}^{(u+3)})-2(w+1)(-(w+1){e}^{(u+3)}-0) \\  & =2(u+3){e}^{(u+3)}+2{(w+1)}^{2}{e}^{(u+3)} \\  & =2{e}^{(u+3)}({(w+1)}^{2}+(u+3)).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 2{e}^{(u+3)}({(w+1)}^{2}+(u+3)) & =0 \\ {(w+1)}^{2}+(u+3) & =0.\end{aligned}
$$

The equation ${(w+1)}^{2}+(u+3)=0$ defines the parabolic cylinder $(u+3)=-{(w+1)}^{2}.$


## GENERATED normal authored method bank q-161819 #3

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{(u-3)}^{2}-{(w-1)}^{2} \\ (w-1){e}^{(u-3)} \\ (u-3)-(v+2)\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $u + w - 4=0.$
- The critical points are exactly the domain points satisfying $u - w^{2} + 2 w - 4=0.$
- The critical points are exactly the domain points satisfying $w - 1=0.$
- The critical points are exactly the domain points satisfying $u - 3=0.$
- The critical points are exactly the domain points satisfying $u + w^{2} - 2 w - 2=0.$ [correct]

Worked solution:
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
x(u,v,w)={(u-3)}^{2}-{(w-1)}^{2},\,y(u,v,w)=(w-1){e}^{(u-3)},\,z(u,v,w)=(u-3)-(v+2).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2(u-3) & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =-2(w-1) \\ \frac{∂y}{∂u} & =(w-1){e}^{(u-3)} & \,\frac{∂y}{∂v} & =0 & \,\frac{∂y}{∂w} & ={e}^{(u-3)} \\ \frac{∂z}{∂u} & =1 & \,\frac{∂z}{∂v} & =-1 & \,\frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2(u-3) & 0 & -2(w-1) \\ (w-1){e}^{(u-3)} & 0 & {e}^{(u-3)} \\ 1 & -1 & 0\end{aligned}| \\  & =2(u-3)|\begin{aligned}0 & {e}^{(u-3)} \\ -1 & 0\end{aligned}|-2(w-1)|\begin{aligned}(w-1){e}^{(u-3)} & 0 \\ 1 & -1\end{aligned}| \\  & =2(u-3)(0+{e}^{(u-3)})-2(w-1)(-(w-1){e}^{(u-3)}-0) \\  & =2(u-3){e}^{(u-3)}+2{(w-1)}^{2}{e}^{(u-3)} \\  & =2{e}^{(u-3)}({(w-1)}^{2}+(u-3)).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 2{e}^{(u-3)}({(w-1)}^{2}+(u-3)) & =0 \\ {(w-1)}^{2}+(u-3) & =0.\end{aligned}
$$

The equation ${(w-1)}^{2}+(u-3)=0$ defines the parabolic cylinder $(u-3)=-{(w-1)}^{2}.$


## GENERATED normal authored method bank q-39709 #1

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{u}^{2}-v \\ {u}^{2}+v \\ {e}^{w}\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $v=0.$
- The critical points are exactly the domain points satisfying $w=0.$
- The critical points are exactly the domain points satisfying $u=0.$ [correct]
- The critical points are exactly the domain points satisfying $u^{2} + v=0.$
- The critical points are exactly the domain points satisfying $u^{2} - v=0.$

Worked solution:
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
x(u,v,w)={u}^{2}-v,\,y(u,v,w)={u}^{2}+v,\,z(u,v,w)={e}^{w}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2u & \,\frac{∂x}{∂v} & =-1 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =2u & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & ={e}^{w}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2u & -1 & 0 \\ 2u & 1 & 0 \\ 0 & 0 & {e}^{w}\end{aligned}| \\  & ={e}^{w}|\begin{aligned}2u & -1 \\ 2u & 1\end{aligned}| \\  & ={e}^{w}(2u+2u) \\  & =4u{e}^{w}.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 4u{e}^{w} & =0 \\ u & =0.\end{aligned}
$$

The equation $u=0$ defines the plane $u=0,$ i.e., $vw$-plane.


## GENERATED normal authored method bank q-39709 #2

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{(u+3)}^{2}-(v-2) \\ {(u+3)}^{2}+(v-2) \\ {e}^{(w+1)}\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $v - 2=0.$
- The critical points are exactly the domain points satisfying $u^{2} + 6 u - v + 11=0.$
- The critical points are exactly the domain points satisfying $u^{2} + 6 u + v + 7=0.$
- The critical points are exactly the domain points satisfying $u + 3=0.$ [correct]
- The critical points are exactly the domain points satisfying $w + 1=0.$

Worked solution:
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
x(u,v,w)={(u+3)}^{2}-(v-2),\,y(u,v,w)={(u+3)}^{2}+(v-2),\,z(u,v,w)={e}^{(w+1)}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2(u+3) & \,\frac{∂x}{∂v} & =-1 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =2(u+3) & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & ={e}^{(w+1)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2(u+3) & -1 & 0 \\ 2(u+3) & 1 & 0 \\ 0 & 0 & {e}^{(w+1)}\end{aligned}| \\  & ={e}^{(w+1)}|\begin{aligned}2(u+3) & -1 \\ 2(u+3) & 1\end{aligned}| \\  & ={e}^{(w+1)}(2(u+3)+2(u+3)) \\  & =4(u+3){e}^{(w+1)}.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 4(u+3){e}^{(w+1)} & =0 \\ (u+3) & =0.\end{aligned}
$$

The equation $(u+3)=0$ defines the plane $(u+3)=0,$ i.e., plane $u=-3$.


## GENERATED normal authored method bank q-39709 #3

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{(u-3)}^{2}-(v+2) \\ {(u-3)}^{2}+(v+2) \\ {e}^{(w-1)}\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $v + 2=0.$
- The critical points are exactly the domain points satisfying $w - 1=0.$
- The critical points are exactly the domain points satisfying $u^{2} - 6 u - v + 7=0.$
- The critical points are exactly the domain points satisfying $u^{2} - 6 u + v + 11=0.$
- The critical points are exactly the domain points satisfying $u - 3=0.$ [correct]

Worked solution:
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
x(u,v,w)={(u-3)}^{2}-(v+2),\,y(u,v,w)={(u-3)}^{2}+(v+2),\,z(u,v,w)={e}^{(w-1)}.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =2(u-3) & \,\frac{∂x}{∂v} & =-1 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =2(u-3) & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & ={e}^{(w-1)}\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}2(u-3) & -1 & 0 \\ 2(u-3) & 1 & 0 \\ 0 & 0 & {e}^{(w-1)}\end{aligned}| \\  & ={e}^{(w-1)}|\begin{aligned}2(u-3) & -1 \\ 2(u-3) & 1\end{aligned}| \\  & ={e}^{(w-1)}(2(u-3)+2(u-3)) \\  & =4(u-3){e}^{(w-1)}.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 4(u-3){e}^{(w-1)} & =0 \\ (u-3) & =0.\end{aligned}
$$

The equation $(u-3)=0$ defines the plane $(u-3)=0,$ i.e., plane $u=3$.


## GENERATED normal authored method bank q-161809 #1

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}uv \\ u+v \\ w\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $v=0.$
- The critical points are exactly the domain points satisfying $u + v=0.$
- The critical points are exactly the domain points satisfying $- u + v=0.$ [correct]
- The critical points are exactly the domain points satisfying $u v=0.$
- The critical points are exactly the domain points satisfying $u=0.$

Worked solution:
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
x(u,v,w)=uv,\,y(u,v,w)=u+v,\,z(u,v,w)=w.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =v & \,\frac{∂x}{∂v} & =u & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =1 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}v & u & 0 \\ 1 & 1 & 0 \\ 0 & 0 & 1\end{aligned}| \\  & =1|\begin{aligned}v & u \\ 1 & 1\end{aligned}| \\  & =v-u.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ v-u & =0.\end{aligned}
$$

The equation $v-u=0$ defines the plane $v=u.$


## GENERATED normal authored method bank q-161809 #2

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u+3)(v-2) \\ (u+3)+(v-2) \\ (w+1)\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $v - 2=0.$
- The critical points are exactly the domain points satisfying $u + 3=0.$
- The critical points are exactly the domain points satisfying $u v - 2 u + 3 v - 6=0.$
- The critical points are exactly the domain points satisfying $- u + v - 5=0.$ [correct]
- The critical points are exactly the domain points satisfying $u + v + 1=0.$

Worked solution:
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
x(u,v,w)=(u+3)(v-2),\,y(u,v,w)=(u+3)+(v-2),\,z(u,v,w)=(w+1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =(v-2) & \,\frac{∂x}{∂v} & =(u+3) & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =1 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}(v-2) & (u+3) & 0 \\ 1 & 1 & 0 \\ 0 & 0 & 1\end{aligned}| \\  & =1|\begin{aligned}(v-2) & (u+3) \\ 1 & 1\end{aligned}| \\  & =(v-2)-(u+3).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ (v-2)-(u+3) & =0.\end{aligned}
$$

The equation $(v-2)-(u+3)=0$ defines the plane $(v-2)=(u+3)..$


## GENERATED normal authored method bank q-161809 #3

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u-3)(v+2) \\ (u-3)+(v+2) \\ (w-1)\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $v + 2=0.$
- The critical points are exactly the domain points satisfying $u + v - 1=0.$
- The critical points are exactly the domain points satisfying $u - 3=0.$
- The critical points are exactly the domain points satisfying $u v + 2 u - 3 v - 6=0.$
- The critical points are exactly the domain points satisfying $- u + v + 5=0.$ [correct]

Worked solution:
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
x(u,v,w)=(u-3)(v+2),\,y(u,v,w)=(u-3)+(v+2),\,z(u,v,w)=(w-1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =(v+2) & \,\frac{∂x}{∂v} & =(u-3) & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =1 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}(v+2) & (u-3) & 0 \\ 1 & 1 & 0 \\ 0 & 0 & 1\end{aligned}| \\  & =1|\begin{aligned}(v+2) & (u-3) \\ 1 & 1\end{aligned}| \\  & =(v+2)-(u-3).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ (v+2)-(u-3) & =0.\end{aligned}
$$

The equation $(v+2)-(u-3)=0$ defines the plane $(v+2)=(u-3)..$


## GENERATED normal authored method bank q-161812 #1

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u \\ {v}^{3}+{w}^{3} \\ v+w\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $v - w^{2}=0.$
- The critical points are exactly the domain points satisfying $v^{2} + w^{2}=0.$
- The critical points are exactly the domain points satisfying $v^{2} - w^{2}=0.$ [correct]
- The critical points are exactly the domain points satisfying $v=0.$
- The critical points are exactly the domain points satisfying $v^{2} - w=0.$

Worked solution:
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
x(u,v,w)=u,\,y(u,v,w)={v}^{3}+{w}^{3},\,z(u,v,w)=v+w.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =3{v}^{2} & \,\frac{∂y}{∂w} & =3{w}^{2} \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =1 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 0 \\ 0 & 3{v}^{2} & 3{w}^{2} \\ 0 & 1 & 1\end{aligned}| \\  & =1|\begin{aligned}3{v}^{2} & 3{w}^{2} \\ 1 & 1\end{aligned}| \\  & =1(3{v}^{2}-3{w}^{2}) \\  & =3({v}^{2}-{w}^{2}).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 3({v}^{2}-{w}^{2}) & =0 \\ {v}^{2}-{w}^{2} & =0.\end{aligned}
$$

The equation ${v}^{2}-{w}^{2}=0$ defines a pair of intersecting planes $v=w$ and $v=-w.$


## GENERATED normal authored method bank q-161812 #2

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u+3) \\ {(v-2)}^{3}+{(w+1)}^{3} \\ (v-2)+(w+1)\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $v - w^{2} - 2 w - 3=0.$
- The critical points are exactly the domain points satisfying $v^{2} - 4 v - w + 3=0.$
- The critical points are exactly the domain points satisfying $v - 2=0.$
- The critical points are exactly the domain points satisfying $v^{2} - 4 v - w^{2} - 2 w + 3=0.$ [correct]
- The critical points are exactly the domain points satisfying $v^{2} - 4 v + w^{2} + 2 w + 5=0.$

Worked solution:
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
x(u,v,w)=(u+3),\,y(u,v,w)={(v-2)}^{3}+{(w+1)}^{3},\,z(u,v,w)=(v-2)+(w+1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =3{(v-2)}^{2} & \,\frac{∂y}{∂w} & =3{(w+1)}^{2} \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =1 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 0 \\ 0 & 3{(v-2)}^{2} & 3{(w+1)}^{2} \\ 0 & 1 & 1\end{aligned}| \\  & =1|\begin{aligned}3{(v-2)}^{2} & 3{(w+1)}^{2} \\ 1 & 1\end{aligned}| \\  & =1(3{(v-2)}^{2}-3{(w+1)}^{2}) \\  & =3({(v-2)}^{2}-{(w+1)}^{2}).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 3({(v-2)}^{2}-{(w+1)}^{2}) & =0 \\ {(v-2)}^{2}-{(w+1)}^{2} & =0.\end{aligned}
$$

The equation ${(v-2)}^{2}-{(w+1)}^{2}=0$ defines a pair of intersecting planes $(v-2)=(w+1)$ and $(v-2)=-(w+1).$


## GENERATED normal authored method bank q-161812 #3

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u-3) \\ {(v+2)}^{3}+{(w-1)}^{3} \\ (v+2)+(w-1)\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $v - w^{2} + 2 w + 1=0.$
- The critical points are exactly the domain points satisfying $v^{2} + 4 v + w^{2} - 2 w + 5=0.$
- The critical points are exactly the domain points satisfying $v^{2} + 4 v - w + 5=0.$
- The critical points are exactly the domain points satisfying $v + 2=0.$
- The critical points are exactly the domain points satisfying $v^{2} + 4 v - w^{2} + 2 w + 3=0.$ [correct]

Worked solution:
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
x(u,v,w)=(u-3),\,y(u,v,w)={(v+2)}^{3}+{(w-1)}^{3},\,z(u,v,w)=(v+2)+(w-1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =3{(v+2)}^{2} & \,\frac{∂y}{∂w} & =3{(w-1)}^{2} \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =1 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 0 \\ 0 & 3{(v+2)}^{2} & 3{(w-1)}^{2} \\ 0 & 1 & 1\end{aligned}| \\  & =1|\begin{aligned}3{(v+2)}^{2} & 3{(w-1)}^{2} \\ 1 & 1\end{aligned}| \\  & =1(3{(v+2)}^{2}-3{(w-1)}^{2}) \\  & =3({(v+2)}^{2}-{(w-1)}^{2}).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 3({(v+2)}^{2}-{(w-1)}^{2}) & =0 \\ {(v+2)}^{2}-{(w-1)}^{2} & =0.\end{aligned}
$$

The equation ${(v+2)}^{2}-{(w-1)}^{2}=0$ defines a pair of intersecting planes $(v+2)=(w-1)$ and $(v+2)=-(w-1).$


## GENERATED normal authored method bank q-161815 #1

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}\sqrt{u} \\ vw \\ u+w\end{aligned}].
$$

Assume $u>0$.

Field 1:
- The critical points are exactly the domain points satisfying $u=0.$
- The critical points are exactly the domain points satisfying $v=0.$
- The critical points are exactly the domain points satisfying $w=0.$ [correct]
- The critical points are exactly the domain points satisfying $u + w=0.$
- The critical points are exactly the domain points satisfying $v w=0.$

Worked solution:
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
x(u,v,w)=\sqrt{u},\,y(u,v,w)=vw,\,z(u,v,w)=u+w.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =\frac{1}{2\sqrt{u}} & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =w & \,\frac{∂y}{∂w} & =v \\ \frac{∂z}{∂u} & =1 & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{1}{2\sqrt{u}} & 0 & 0 \\ 0 & w & v \\ 1 & 0 & 1\end{aligned}| \\  & =\frac{1}{2\sqrt{u}}|\begin{aligned}w & v \\ 0 & 1\end{aligned}|+1|\begin{aligned}0 & 0 \\ w & v\end{aligned}| \\  & =\frac{1}{2\sqrt{u}}(w-0)+0 \\  & =\frac{w}{2\sqrt{u}}.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ \frac{w}{2\sqrt{u}} & =0 \\ w & =0.\end{aligned}
$$

The equation $w=0$ defines the plane $w=0,$ i.e., $uv$-plane.


## GENERATED normal authored method bank q-161815 #2

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}\sqrt{(u+3)} \\ (v-2)(w+1) \\ (u+3)+(w+1)\end{aligned}].
$$

Assume $u>-3$.

Field 1:
- The critical points are exactly the domain points satisfying $u + 3=0.$
- The critical points are exactly the domain points satisfying $v w + v - 2 w - 2=0.$
- The critical points are exactly the domain points satisfying $u + w + 4=0.$
- The critical points are exactly the domain points satisfying $w + 1=0.$ [correct]
- The critical points are exactly the domain points satisfying $v - 2=0.$

Worked solution:
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
x(u,v,w)=\sqrt{(u+3)},\,y(u,v,w)=(v-2)(w+1),\,z(u,v,w)=(u+3)+(w+1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =\frac{1}{2\sqrt{(u+3)}} & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =(w+1) & \,\frac{∂y}{∂w} & =(v-2) \\ \frac{∂z}{∂u} & =1 & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{1}{2\sqrt{(u+3)}} & 0 & 0 \\ 0 & (w+1) & (v-2) \\ 1 & 0 & 1\end{aligned}| \\  & =\frac{1}{2\sqrt{(u+3)}}|\begin{aligned}(w+1) & (v-2) \\ 0 & 1\end{aligned}|+1|\begin{aligned}0 & 0 \\ (w+1) & (v-2)\end{aligned}| \\  & =\frac{1}{2\sqrt{(u+3)}}((w+1)-0)+0 \\  & =\frac{(w+1)}{2\sqrt{(u+3)}}.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ \frac{(w+1)}{2\sqrt{(u+3)}} & =0 \\ (w+1) & =0.\end{aligned}
$$

The equation $(w+1)=0$ defines the plane $(w+1)=0,$ i.e., plane $w=-1$.


## GENERATED normal authored method bank q-161815 #3

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}\sqrt{(u-3)} \\ (v+2)(w-1) \\ (u-3)+(w-1)\end{aligned}].
$$

Assume $u>3$.

Field 1:
- The critical points are exactly the domain points satisfying $u - 3=0.$
- The critical points are exactly the domain points satisfying $v + 2=0.$
- The critical points are exactly the domain points satisfying $v w - v + 2 w - 2=0.$
- The critical points are exactly the domain points satisfying $u + w - 4=0.$
- The critical points are exactly the domain points satisfying $w - 1=0.$ [correct]

Worked solution:
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
x(u,v,w)=\sqrt{(u-3)},\,y(u,v,w)=(v+2)(w-1),\,z(u,v,w)=(u-3)+(w-1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =\frac{1}{2\sqrt{(u-3)}} & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =(w-1) & \,\frac{∂y}{∂w} & =(v+2) \\ \frac{∂z}{∂u} & =1 & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}\frac{1}{2\sqrt{(u-3)}} & 0 & 0 \\ 0 & (w-1) & (v+2) \\ 1 & 0 & 1\end{aligned}| \\  & =\frac{1}{2\sqrt{(u-3)}}|\begin{aligned}(w-1) & (v+2) \\ 0 & 1\end{aligned}|+1|\begin{aligned}0 & 0 \\ (w-1) & (v+2)\end{aligned}| \\  & =\frac{1}{2\sqrt{(u-3)}}((w-1)-0)+0 \\  & =\frac{(w-1)}{2\sqrt{(u-3)}}.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ \frac{(w-1)}{2\sqrt{(u-3)}} & =0 \\ (w-1) & =0.\end{aligned}
$$

The equation $(w-1)=0$ defines the plane $(w-1)=0,$ i.e., plane $w=1$.


## GENERATED normal authored method bank q-161817 #1

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u \\ v{e}^{w} \\ 2u+v+3w\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $v=0.$
- The critical points are exactly the domain points satisfying $v + 3=0.$
- The critical points are exactly the domain points satisfying $3 - v=0.$ [correct]
- The critical points are exactly the domain points satisfying $3 - w=0.$
- The critical points are exactly the domain points satisfying $w=0.$

Worked solution:
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
x(u,v,w)=u,\,y(u,v,w)=v{e}^{w},\,z(u,v,w)=2u+v+3w.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & ={e}^{w} & \,\frac{∂y}{∂w} & =v{e}^{w} \\ \frac{∂z}{∂u} & =2 & \,\frac{∂z}{∂v} & =1 & \,\frac{∂z}{∂w} & =3\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 0 \\ 0 & {e}^{w} & v{e}^{w} \\ 2 & 1 & 3\end{aligned}| \\  & =1|\begin{aligned}{e}^{w} & v{e}^{w} \\ 1 & 3\end{aligned}| \\  & =1(3{e}^{w}-v{e}^{w}) \\  & ={e}^{w}(3-v).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ {e}^{w}(3-v) & =0 \\ 3-v & =0.\end{aligned}
$$

The equation $3-v=0$ defines the plane $v=3.$


## GENERATED normal authored method bank q-161817 #2

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u+3) \\ (v-2){e}^{(w+1)} \\ 2(u+3)+(v-2)+3(w+1)\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $v - 2=0.$
- The critical points are exactly the domain points satisfying $w + 1=0.$
- The critical points are exactly the domain points satisfying $2 - w=0.$
- The critical points are exactly the domain points satisfying $5 - v=0.$ [correct]
- The critical points are exactly the domain points satisfying $v + 1=0.$

Worked solution:
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
x(u,v,w)=(u+3),\,y(u,v,w)=(v-2){e}^{(w+1)},\,z(u,v,w)=2(u+3)+(v-2)+3(w+1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & ={e}^{(w+1)} & \,\frac{∂y}{∂w} & =(v-2){e}^{(w+1)} \\ \frac{∂z}{∂u} & =2 & \,\frac{∂z}{∂v} & =1 & \,\frac{∂z}{∂w} & =3\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 0 \\ 0 & {e}^{(w+1)} & (v-2){e}^{(w+1)} \\ 2 & 1 & 3\end{aligned}| \\  & =1|\begin{aligned}{e}^{(w+1)} & (v-2){e}^{(w+1)} \\ 1 & 3\end{aligned}| \\  & =1(3{e}^{(w+1)}-(v-2){e}^{(w+1)}) \\  & ={e}^{(w+1)}(3-(v-2)).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ {e}^{(w+1)}(3-(v-2)) & =0 \\ 3-(v-2) & =0.\end{aligned}
$$

The equation $3-(v-2)=0$ defines the plane $(v-2)=3.$


## GENERATED normal authored method bank q-161817 #3

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u-3) \\ (v+2){e}^{(w-1)} \\ 2(u-3)+(v+2)+3(w-1)\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $v + 2=0.$
- The critical points are exactly the domain points satisfying $v + 5=0.$
- The critical points are exactly the domain points satisfying $w - 1=0.$
- The critical points are exactly the domain points satisfying $4 - w=0.$
- The critical points are exactly the domain points satisfying $1 - v=0.$ [correct]

Worked solution:
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
x(u,v,w)=(u-3),\,y(u,v,w)=(v+2){e}^{(w-1)},\,z(u,v,w)=2(u-3)+(v+2)+3(w-1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & ={e}^{(w-1)} & \,\frac{∂y}{∂w} & =(v+2){e}^{(w-1)} \\ \frac{∂z}{∂u} & =2 & \,\frac{∂z}{∂v} & =1 & \,\frac{∂z}{∂w} & =3\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 0 \\ 0 & {e}^{(w-1)} & (v+2){e}^{(w-1)} \\ 2 & 1 & 3\end{aligned}| \\  & =1|\begin{aligned}{e}^{(w-1)} & (v+2){e}^{(w-1)} \\ 1 & 3\end{aligned}| \\  & =1(3{e}^{(w-1)}-(v+2){e}^{(w-1)}) \\  & ={e}^{(w-1)}(3-(v+2)).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ {e}^{(w-1)}(3-(v+2)) & =0 \\ 3-(v+2) & =0.\end{aligned}
$$

The equation $3-(v+2)=0$ defines the plane $(v+2)=3.$


## GENERATED normal authored method bank q-161818 #1

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u+3w \\ v+2w \\ {v}^{2}-u\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $3 - 2 v=0.$
- The critical points are exactly the domain points satisfying $4 v + 3=0.$
- The critical points are exactly the domain points satisfying $3 - 4 v=0.$ [correct]
- The critical points are exactly the domain points satisfying $3 - 4 w=0.$
- The critical points are exactly the domain points satisfying $v=0.$

Worked solution:
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
x(u,v,w)=u+3w,\,y(u,v,w)=v+2w,\,z(u,v,w)={v}^{2}-u.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =3 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =2 \\ \frac{∂z}{∂u} & =-1 & \,\frac{∂z}{∂v} & =2v & \,\frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 3 \\ 0 & 1 & 2 \\ -1 & 2v & 0\end{aligned}| \\  & =1|\begin{aligned}1 & 2 \\ 2v & 0\end{aligned}|+3|\begin{aligned}0 & 1 \\ -1 & 2v\end{aligned}| \\  & =1(0-4v)+3(0+1) \\  & =3-4v.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 3-4v & =0.\end{aligned}
$$

The equation $3-4v=0$ defines the plane $v=\frac{3}{4}.$


## GENERATED normal authored method bank q-161818 #2

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u+3)+3(w+1) \\ (v-2)+2(w+1) \\ {(v-2)}^{2}-(u+3)\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $7 - 2 v=0.$
- The critical points are exactly the domain points satisfying $v - 2=0.$
- The critical points are exactly the domain points satisfying $- 4 w - 1=0.$
- The critical points are exactly the domain points satisfying $11 - 4 v=0.$ [correct]
- The critical points are exactly the domain points satisfying $4 v - 5=0.$

Worked solution:
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
x(u,v,w)=(u+3)+3(w+1),\,y(u,v,w)=(v-2)+2(w+1),\,z(u,v,w)={(v-2)}^{2}-(u+3).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =3 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =2 \\ \frac{∂z}{∂u} & =-1 & \,\frac{∂z}{∂v} & =2(v-2) & \,\frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 3 \\ 0 & 1 & 2 \\ -1 & 2(v-2) & 0\end{aligned}| \\  & =1|\begin{aligned}1 & 2 \\ 2(v-2) & 0\end{aligned}|+3|\begin{aligned}0 & 1 \\ -1 & 2(v-2)\end{aligned}| \\  & =1(0-4(v-2))+3(0+1) \\  & =3-4(v-2).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 3-4(v-2) & =0.\end{aligned}
$$

The equation $3-4(v-2)=0$ defines the plane $(v-2)=\frac{3}{4}.$


## GENERATED normal authored method bank q-161818 #3

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u-3)+3(w-1) \\ (v+2)+2(w-1) \\ {(v+2)}^{2}-(u-3)\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $- 2 v - 1=0.$
- The critical points are exactly the domain points satisfying $4 v + 11=0.$
- The critical points are exactly the domain points satisfying $v + 2=0.$
- The critical points are exactly the domain points satisfying $7 - 4 w=0.$
- The critical points are exactly the domain points satisfying $- 4 v - 5=0.$ [correct]

Worked solution:
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
x(u,v,w)=(u-3)+3(w-1),\,y(u,v,w)=(v+2)+2(w-1),\,z(u,v,w)={(v+2)}^{2}-(u-3).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =3 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =2 \\ \frac{∂z}{∂u} & =-1 & \,\frac{∂z}{∂v} & =2(v+2) & \,\frac{∂z}{∂w} & =0\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 3 \\ 0 & 1 & 2 \\ -1 & 2(v+2) & 0\end{aligned}| \\  & =1|\begin{aligned}1 & 2 \\ 2(v+2) & 0\end{aligned}|+3|\begin{aligned}0 & 1 \\ -1 & 2(v+2)\end{aligned}| \\  & =1(0-4(v+2))+3(0+1) \\  & =3-4(v+2).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 3-4(v+2) & =0.\end{aligned}
$$

The equation $3-4(v+2)=0$ defines the plane $(v+2)=\frac{3}{4}.$


## GENERATED normal authored method bank q-161813 #1

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}\frac{1}{u} \\ {v}^{2}+w \\ vw\end{aligned}].
$$

Assume $u\ne 0$.

Field 1:
- The critical points are exactly the domain points satisfying $v^{2} - w=0.$
- The critical points are exactly the domain points satisfying $2 v^{2} + w=0.$
- The critical points are exactly the domain points satisfying $2 v^{2} - w=0.$ [correct]
- The critical points are exactly the domain points satisfying $w=0.$
- The critical points are exactly the domain points satisfying $v=0.$

Worked solution:
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
x(u,v,w)=\frac{1}{u},\,y(u,v,w)={v}^{2}+w,\,z(u,v,w)=vw.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =-\frac{1}{{u}^{2}} & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =2v & \,\frac{∂y}{∂w} & =1 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =w & \,\frac{∂z}{∂w} & =v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}-\frac{1}{{u}^{2}} & 0 & 0 \\ 0 & 2v & 1 \\ 0 & w & v\end{aligned}| \\  & =-\frac{1}{{u}^{2}}|\begin{aligned}2v & 1 \\ w & v\end{aligned}| \\  & =-\frac{1}{{u}^{2}}(2{v}^{2}-w).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ -\frac{1}{{u}^{2}}(2{v}^{2}-w) & =0 \\ w-2{v}^{2} & =0.\end{aligned}
$$

The equation $w-2{v}^{2}=0$ defines the parabolic cylinder $w=2{v}^{2}.$


## GENERATED normal authored method bank q-161813 #2

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}\frac{1}{(u+3)} \\ {(v-2)}^{2}+(w+1) \\ (v-2)(w+1)\end{aligned}].
$$

Assume $u\ne -3$.

Field 1:
- The critical points are exactly the domain points satisfying $v^{2} - 4 v - w + 3=0.$
- The critical points are exactly the domain points satisfying $v - 2=0.$
- The critical points are exactly the domain points satisfying $w + 1=0.$
- The critical points are exactly the domain points satisfying $2 v^{2} - 8 v - w + 7=0.$ [correct]
- The critical points are exactly the domain points satisfying $2 v^{2} - 8 v + w + 9=0.$

Worked solution:
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
x(u,v,w)=\frac{1}{(u+3)},\,y(u,v,w)={(v-2)}^{2}+(w+1),\,z(u,v,w)=(v-2)(w+1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =-\frac{1}{{(u+3)}^{2}} & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =2(v-2) & \,\frac{∂y}{∂w} & =1 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =(w+1) & \,\frac{∂z}{∂w} & =(v-2)\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}-\frac{1}{{(u+3)}^{2}} & 0 & 0 \\ 0 & 2(v-2) & 1 \\ 0 & (w+1) & (v-2)\end{aligned}| \\  & =-\frac{1}{{(u+3)}^{2}}|\begin{aligned}2(v-2) & 1 \\ (w+1) & (v-2)\end{aligned}| \\  & =-\frac{1}{{(u+3)}^{2}}(2{(v-2)}^{2}-(w+1)).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ -\frac{1}{{(u+3)}^{2}}(2{(v-2)}^{2}-(w+1)) & =0 \\ (w+1)-2{(v-2)}^{2} & =0.\end{aligned}
$$

The equation $(w+1)-2{(v-2)}^{2}=0$ defines the parabolic cylinder $(w+1)=2{(v-2)}^{2}.$


## GENERATED normal authored method bank q-161813 #3

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}\frac{1}{(u-3)} \\ {(v+2)}^{2}+(w-1) \\ (v+2)(w-1)\end{aligned}].
$$

Assume $u\ne 3$.

Field 1:
- The critical points are exactly the domain points satisfying $v^{2} + 4 v - w + 5=0.$
- The critical points are exactly the domain points satisfying $2 v^{2} + 8 v + w + 7=0.$
- The critical points are exactly the domain points satisfying $v + 2=0.$
- The critical points are exactly the domain points satisfying $w - 1=0.$
- The critical points are exactly the domain points satisfying $2 v^{2} + 8 v - w + 9=0.$ [correct]

Worked solution:
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
x(u,v,w)=\frac{1}{(u-3)},\,y(u,v,w)={(v+2)}^{2}+(w-1),\,z(u,v,w)=(v+2)(w-1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =-\frac{1}{{(u-3)}^{2}} & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =2(v+2) & \,\frac{∂y}{∂w} & =1 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =(w-1) & \,\frac{∂z}{∂w} & =(v+2)\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}-\frac{1}{{(u-3)}^{2}} & 0 & 0 \\ 0 & 2(v+2) & 1 \\ 0 & (w-1) & (v+2)\end{aligned}| \\  & =-\frac{1}{{(u-3)}^{2}}|\begin{aligned}2(v+2) & 1 \\ (w-1) & (v+2)\end{aligned}| \\  & =-\frac{1}{{(u-3)}^{2}}(2{(v+2)}^{2}-(w-1)).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ -\frac{1}{{(u-3)}^{2}}(2{(v+2)}^{2}-(w-1)) & =0 \\ (w-1)-2{(v+2)}^{2} & =0.\end{aligned}
$$

The equation $(w-1)-2{(v+2)}^{2}=0$ defines the parabolic cylinder $(w-1)=2{(v+2)}^{2}.$


## GENERATED normal authored method bank q-161814 #1

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u+2w \\ v-u \\ uw\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $u - w=0.$
- The critical points are exactly the domain points satisfying $u + 2 w=0.$
- The critical points are exactly the domain points satisfying $u - 2 w=0.$ [correct]
- The critical points are exactly the domain points satisfying $w=0.$
- The critical points are exactly the domain points satisfying $u=0.$

Worked solution:
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
x(u,v,w)=u+2w,\,y(u,v,w)=v-u,\,z(u,v,w)=uw.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =2 \\ \frac{∂y}{∂u} & =-1 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =w & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & =u\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 2 \\ -1 & 1 & 0 \\ w & 0 & u\end{aligned}| \\  & =1|\begin{aligned}1 & 0 \\ 0 & u\end{aligned}|+2|\begin{aligned}-1 & 1 \\ w & 0\end{aligned}| \\  & =1(u-0)+2(0-w) \\  & =u-2w.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ u-2w & =0.\end{aligned}
$$

The equation $u-2w=0$ defines the plane $u=2w.$


## GENERATED normal authored method bank q-161814 #2

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u+3)+2(w+1) \\ (v-2)-(u+3) \\ (u+3)(w+1)\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $u - w + 2=0.$
- The critical points are exactly the domain points satisfying $u + 3=0.$
- The critical points are exactly the domain points satisfying $w + 1=0.$
- The critical points are exactly the domain points satisfying $u - 2 w + 1=0.$ [correct]
- The critical points are exactly the domain points satisfying $u + 2 w + 5=0.$

Worked solution:
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
x(u,v,w)=(u+3)+2(w+1),\,y(u,v,w)=(v-2)-(u+3),\,z(u,v,w)=(u+3)(w+1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =2 \\ \frac{∂y}{∂u} & =-1 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =(w+1) & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & =(u+3)\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 2 \\ -1 & 1 & 0 \\ (w+1) & 0 & (u+3)\end{aligned}| \\  & =1|\begin{aligned}1 & 0 \\ 0 & (u+3)\end{aligned}|+2|\begin{aligned}-1 & 1 \\ (w+1) & 0\end{aligned}| \\  & =1((u+3)-0)+2(0-(w+1)) \\  & =(u+3)-2(w+1).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ (u+3)-2(w+1) & =0.\end{aligned}
$$

The equation $(u+3)-2(w+1)=0$ defines the plane $(u+3)=2(w+1).$


## GENERATED normal authored method bank q-161814 #3

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u-3)+2(w-1) \\ (v+2)-(u-3) \\ (u-3)(w-1)\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $u - w - 2=0.$
- The critical points are exactly the domain points satisfying $u + 2 w - 5=0.$
- The critical points are exactly the domain points satisfying $u - 3=0.$
- The critical points are exactly the domain points satisfying $w - 1=0.$
- The critical points are exactly the domain points satisfying $u - 2 w - 1=0.$ [correct]

Worked solution:
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
x(u,v,w)=(u-3)+2(w-1),\,y(u,v,w)=(v+2)-(u-3),\,z(u,v,w)=(u-3)(w-1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =2 \\ \frac{∂y}{∂u} & =-1 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =(w-1) & \,\frac{∂z}{∂v} & =0 & \,\frac{∂z}{∂w} & =(u-3)\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & 0 & 2 \\ -1 & 1 & 0 \\ (w-1) & 0 & (u-3)\end{aligned}| \\  & =1|\begin{aligned}1 & 0 \\ 0 & (u-3)\end{aligned}|+2|\begin{aligned}-1 & 1 \\ (w-1) & 0\end{aligned}| \\  & =1((u-3)-0)+2(0-(w-1)) \\  & =(u-3)-2(w-1).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ (u-3)-2(w-1) & =0.\end{aligned}
$$

The equation $(u-3)-2(w-1)=0$ defines the plane $(u-3)=2(w-1).$


## GENERATED normal authored method bank q-161816 #1

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{e}^{u} \\ {e}^{u+w} \\ uv+w\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $w=0.$
- The critical points are exactly the domain points satisfying $v=0.$
- The critical points are exactly the domain points satisfying $u=0.$ [correct]
- The critical points are exactly the domain points satisfying $u v + w=0.$
- The critical points are exactly the domain points satisfying $2 u + w=0.$

Worked solution:
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
x(u,v,w)={e}^{u},\,y(u,v,w)={e}^{u+w},\,z(u,v,w)=uv+w.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & ={e}^{u} & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & ={e}^{u+w} & \,\frac{∂y}{∂v} & =0 & \,\frac{∂y}{∂w} & ={e}^{u+w} \\ \frac{∂z}{∂u} & =v & \,\frac{∂z}{∂v} & =u & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}{e}^{u} & 0 & 0 \\ {e}^{u+w} & 0 & {e}^{u+w} \\ v & u & 1\end{aligned}| \\  & ={e}^{u}|\begin{aligned}0 & {e}^{u+w} \\ u & 1\end{aligned}| \\  & ={e}^{u}(0-u{e}^{u+w}) \\  & =-u{e}^{2u+w}.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ -u{e}^{2u+w} & =0 \\ u & =0.\end{aligned}
$$

The equation $u=0$ defines the plane $u=0,$ i.e., $vw$-plane.


## GENERATED normal authored method bank q-161816 #2

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{e}^{(u+3)} \\ {e}^{(u+3)+(w+1)} \\ (u+3)(v-2)+(w+1)\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $w + 1=0.$
- The critical points are exactly the domain points satisfying $2 u + w + 7=0.$
- The critical points are exactly the domain points satisfying $u v - 2 u + 3 v + w - 5=0.$
- The critical points are exactly the domain points satisfying $u + 3=0.$ [correct]
- The critical points are exactly the domain points satisfying $v - 2=0.$

Worked solution:
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
x(u,v,w)={e}^{(u+3)},\,y(u,v,w)={e}^{(u+3)+(w+1)},\,z(u,v,w)=(u+3)(v-2)+(w+1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & ={e}^{(u+3)} & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & ={e}^{(u+3)+(w+1)} & \,\frac{∂y}{∂v} & =0 & \,\frac{∂y}{∂w} & ={e}^{(u+3)+(w+1)} \\ \frac{∂z}{∂u} & =(v-2) & \,\frac{∂z}{∂v} & =(u+3) & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}{e}^{(u+3)} & 0 & 0 \\ {e}^{(u+3)+(w+1)} & 0 & {e}^{(u+3)+(w+1)} \\ (v-2) & (u+3) & 1\end{aligned}| \\  & ={e}^{(u+3)}|\begin{aligned}0 & {e}^{(u+3)+(w+1)} \\ (u+3) & 1\end{aligned}| \\  & ={e}^{(u+3)}(0-(u+3){e}^{(u+3)+(w+1)}) \\  & =-(u+3){e}^{2(u+3)+(w+1)}.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ -(u+3){e}^{2(u+3)+(w+1)} & =0 \\ (u+3) & =0.\end{aligned}
$$

The equation $(u+3)=0$ defines the plane $(u+3)=0,$ i.e., plane $u=-3$.


## GENERATED normal authored method bank q-161816 #3

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{e}^{(u-3)} \\ {e}^{(u-3)+(w-1)} \\ (u-3)(v+2)+(w-1)\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $w - 1=0.$
- The critical points are exactly the domain points satisfying $v + 2=0.$
- The critical points are exactly the domain points satisfying $2 u + w - 7=0.$
- The critical points are exactly the domain points satisfying $u v + 2 u - 3 v + w - 7=0.$
- The critical points are exactly the domain points satisfying $u - 3=0.$ [correct]

Worked solution:
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
x(u,v,w)={e}^{(u-3)},\,y(u,v,w)={e}^{(u-3)+(w-1)},\,z(u,v,w)=(u-3)(v+2)+(w-1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & ={e}^{(u-3)} & \,\frac{∂x}{∂v} & =0 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & ={e}^{(u-3)+(w-1)} & \,\frac{∂y}{∂v} & =0 & \,\frac{∂y}{∂w} & ={e}^{(u-3)+(w-1)} \\ \frac{∂z}{∂u} & =(v+2) & \,\frac{∂z}{∂v} & =(u-3) & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}{e}^{(u-3)} & 0 & 0 \\ {e}^{(u-3)+(w-1)} & 0 & {e}^{(u-3)+(w-1)} \\ (v+2) & (u-3) & 1\end{aligned}| \\  & ={e}^{(u-3)}|\begin{aligned}0 & {e}^{(u-3)+(w-1)} \\ (u-3) & 1\end{aligned}| \\  & ={e}^{(u-3)}(0-(u-3){e}^{(u-3)+(w-1)}) \\  & =-(u-3){e}^{2(u-3)+(w-1)}.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ -(u-3){e}^{2(u-3)+(w-1)} & =0 \\ (u-3) & =0.\end{aligned}
$$

The equation $(u-3)=0$ defines the plane $(u-3)=0,$ i.e., plane $u=3$.


## GENERATED normal authored method bank q-161810 #1

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u+vw \\ {v}^{2} \\ w+v\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $w=0.$
- The critical points are exactly the domain points satisfying $u=0.$
- The critical points are exactly the domain points satisfying $v=0.$ [correct]
- The critical points are exactly the domain points satisfying $v + w=0.$
- The critical points are exactly the domain points satisfying $u + v w=0.$

Worked solution:
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
x(u,v,w)=u+vw,\,y(u,v,w)={v}^{2},\,z(u,v,w)=w+v.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =w & \,\frac{∂x}{∂w} & =v \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =2v & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =1 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & w & v \\ 0 & 2v & 0 \\ 0 & 1 & 1\end{aligned}| \\  & =1|\begin{aligned}2v & 0 \\ 1 & 1\end{aligned}| \\  & =1(2v-0) \\  & =2v.\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 2v & =0 \\ v & =0.\end{aligned}
$$

The equation $v=0$ defines the plane $v=0,$ i.e., $uw$-plane.


## GENERATED normal authored method bank q-161810 #2

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u+3)+(v-2)(w+1) \\ {(v-2)}^{2} \\ (w+1)+(v-2)\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $w + 1=0.$
- The critical points are exactly the domain points satisfying $u + v w + v - 2 w + 1=0.$
- The critical points are exactly the domain points satisfying $v + w - 1=0.$
- The critical points are exactly the domain points satisfying $v - 2=0.$ [correct]
- The critical points are exactly the domain points satisfying $u + 3=0.$

Worked solution:
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
x(u,v,w)=(u+3)+(v-2)(w+1),\,y(u,v,w)={(v-2)}^{2},\,z(u,v,w)=(w+1)+(v-2).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =(w+1) & \,\frac{∂x}{∂w} & =(v-2) \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =2(v-2) & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =1 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & (w+1) & (v-2) \\ 0 & 2(v-2) & 0 \\ 0 & 1 & 1\end{aligned}| \\  & =1|\begin{aligned}2(v-2) & 0 \\ 1 & 1\end{aligned}| \\  & =1(2(v-2)-0) \\  & =2(v-2).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 2(v-2) & =0 \\ (v-2) & =0.\end{aligned}
$$

The equation $(v-2)=0$ defines the plane $(v-2)=0,$ i.e., plane $v=2$.


## GENERATED normal authored method bank q-161810 #3

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}(u-3)+(v+2)(w-1) \\ {(v+2)}^{2} \\ (w-1)+(v+2)\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $w - 1=0.$
- The critical points are exactly the domain points satisfying $u - 3=0.$
- The critical points are exactly the domain points satisfying $u + v w - v + 2 w - 5=0.$
- The critical points are exactly the domain points satisfying $v + w + 1=0.$
- The critical points are exactly the domain points satisfying $v + 2=0.$ [correct]

Worked solution:
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
x(u,v,w)=(u-3)+(v+2)(w-1),\,y(u,v,w)={(v+2)}^{2},\,z(u,v,w)=(w-1)+(v+2).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & =1 & \,\frac{∂x}{∂v} & =(w-1) & \,\frac{∂x}{∂w} & =(v+2) \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =2(v+2) & \,\frac{∂y}{∂w} & =0 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =1 & \,\frac{∂z}{∂w} & =1\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}1 & (w-1) & (v+2) \\ 0 & 2(v+2) & 0 \\ 0 & 1 & 1\end{aligned}| \\  & =1|\begin{aligned}2(v+2) & 0 \\ 1 & 1\end{aligned}| \\  & =1(2(v+2)-0) \\  & =2(v+2).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ 2(v+2) & =0 \\ (v+2) & =0.\end{aligned}
$$

The equation $(v+2)=0$ defines the plane $(v+2)=0,$ i.e., plane $v=-2$.


## GENERATED normal authored method bank q-161811 #1

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{e}^{u}+v \\ v+w \\ vw\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $v=0.$
- The critical points are exactly the domain points satisfying $v + w=0.$
- The critical points are exactly the domain points satisfying $v - w=0.$ [correct]
- The critical points are exactly the domain points satisfying $v w=0.$
- The critical points are exactly the domain points satisfying $w=0.$

Worked solution:
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
x(u,v,w)={e}^{u}+v,\,y(u,v,w)=v+w,\,z(u,v,w)=vw.
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & ={e}^{u} & \,\frac{∂x}{∂v} & =1 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =1 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =w & \,\frac{∂z}{∂w} & =v\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}{e}^{u} & 1 & 0 \\ 0 & 1 & 1 \\ 0 & w & v\end{aligned}| \\  & ={e}^{u}|\begin{aligned}1 & 1 \\ w & v\end{aligned}| \\  & ={e}^{u}(v-w).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ {e}^{u}(v-w) & =0 \\ v-w & =0.\end{aligned}
$$

The equation $v-w=0$ defines the plane $v=w.$


## GENERATED normal authored method bank q-161811 #2

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{e}^{(u+3)}+(v-2) \\ (v-2)+(w+1) \\ (v-2)(w+1)\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $v - 2=0.$
- The critical points are exactly the domain points satisfying $w + 1=0.$
- The critical points are exactly the domain points satisfying $v w + v - 2 w - 2=0.$
- The critical points are exactly the domain points satisfying $v - w - 3=0.$ [correct]
- The critical points are exactly the domain points satisfying $v + w - 1=0.$

Worked solution:
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
x(u,v,w)={e}^{(u+3)}+(v-2),\,y(u,v,w)=(v-2)+(w+1),\,z(u,v,w)=(v-2)(w+1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & ={e}^{(u+3)} & \,\frac{∂x}{∂v} & =1 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =1 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =(w+1) & \,\frac{∂z}{∂w} & =(v-2)\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}{e}^{(u+3)} & 1 & 0 \\ 0 & 1 & 1 \\ 0 & (w+1) & (v-2)\end{aligned}| \\  & ={e}^{(u+3)}|\begin{aligned}1 & 1 \\ (w+1) & (v-2)\end{aligned}| \\  & ={e}^{(u+3)}((v-2)-(w+1)).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ {e}^{(u+3)}((v-2)-(w+1)) & =0 \\ (v-2)-(w+1) & =0.\end{aligned}
$$

The equation $(v-2)-(w+1)=0$ defines the plane $(v-2)=(w+1).$


## GENERATED normal authored method bank q-161811 #3

Difficulty: moderate | GENERATED normal learning record | Origin: observed template with authored method bank | Profile: method
Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{e}^{(u-3)}+(v+2) \\ (v+2)+(w-1) \\ (v+2)(w-1)\end{aligned}].
$$

Field 1:
- The critical points are exactly the domain points satisfying $v + 2=0.$
- The critical points are exactly the domain points satisfying $v + w + 1=0.$
- The critical points are exactly the domain points satisfying $w - 1=0.$
- The critical points are exactly the domain points satisfying $v w - v + 2 w - 2=0.$
- The critical points are exactly the domain points satisfying $v - w + 3=0.$ [correct]

Worked solution:
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
x(u,v,w)={e}^{(u-3)}+(v+2),\,y(u,v,w)=(v+2)+(w-1),\,z(u,v,w)=(v+2)(w-1).
$$

First, we find the partial derivatives:

$$
\begin{aligned}\frac{∂x}{∂u} & ={e}^{(u-3)} & \,\frac{∂x}{∂v} & =1 & \,\frac{∂x}{∂w} & =0 \\ \frac{∂y}{∂u} & =0 & \,\frac{∂y}{∂v} & =1 & \,\frac{∂y}{∂w} & =1 \\ \frac{∂z}{∂u} & =0 & \,\frac{∂z}{∂v} & =(w-1) & \,\frac{∂z}{∂w} & =(v+2)\end{aligned}
$$

Therefore, the corresponding Jacobian determinant is

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =|\begin{aligned}{e}^{(u-3)} & 1 & 0 \\ 0 & 1 & 1 \\ 0 & (w-1) & (v+2)\end{aligned}| \\  & ={e}^{(u-3)}|\begin{aligned}1 & 1 \\ (w-1) & (v+2)\end{aligned}| \\  & ={e}^{(u-3)}((v+2)-(w-1)).\end{aligned}
$$

The function has critical points when $\frac{∂(x,y,z)}{∂(u,v,w)}=0.$ So, we obtain

$$
\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & =0 \\ {e}^{(u-3)}((v+2)-(w-1)) & =0 \\ (v+2)-(w-1) & =0.\end{aligned}
$$

The equation $(v+2)-(w-1)=0$ defines the plane $(v+2)=(w-1).$
