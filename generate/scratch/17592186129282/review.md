# Local area review

Originals are raw evidence. Replays normalize mathematical notation and repair duplicate/stale fields, with original-bank values and designation counts reported separately.

## Original q-161788

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{u}^{2}+v \\ 2u-{v}^{3}\end{aligned}]?
$$

Raw field 0; correct designation: MISSING

- $2δA$
- $36δA$
- $14δA$
- $26δA$
- $5δA$
Raw field 1; correct designation: 26\,\delta A

- $36\,\delta A$
- $26\,\delta A$
- $5\,\delta A$
- $2\,\delta A$
- $14\,\delta A$

Original worked solution:
Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))≈|\frac{∂(x,y)}{∂(u,v)}|\cdot {{\text{Area}(Δ)}_{⏟}}_{\delta A}
$$

 

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}2u & 1 \\ 2 & -3{v}^{2}\end{aligned}| \\  & =2u\cdot (-3{v}^{2})-1\cdot 2 \\  & =-6u{v}^{2}-2 \\ {\frac{∂(x,y)}{∂(u,v)}|}_{(1,2)} & =(-6u{v}^{2}-2)\,{|}_{u=1\,v=2} \\  & =-6(1)(2)^{2}-2 \\  & =-26\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & ≈|-26|\cdot \delta A \\  & =26\,\delta A.\end{aligned}
$$

### Parameterized source replay (single repaired field)
### easy / poly_sum / observed_poly_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u^{2} + v\\2 u - v^{3}\end{aligned}]?
$$

- $14\,\delta A$
- $36\,\delta A$
- $2\,\delta A$
- $5\,\delta A$
- $26\,\delta A$ **correct**

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}2 u&1\\2&- 3 v^{2}\end{matrix}\right|\\& =(2 u)\cdot (- 3 v^{2})-(1)\cdot (2)\\& =-6uv^{2}-2\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,2)} & =\left(- 2 \left(3 u v^{2} + 1\right)\right)\big|_{u=1,v=2}\\& =- 2 \left(3 (1) (2)^{2} + 1\right)\\& =-26\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-26|\cdot\delta A\\ & =26\,\delta A.\end{aligned}
$$

## Original q-161832

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,5)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\operatorname{ln}⁡(uv) \\ u{v}^{2}\end{aligned}]?
$$

Raw field 0; correct designation: 5\,\delta A

- $5\,\delta A$
- $\delta A$
- $11\,\delta A$
- $8\,\delta A$
- $3\,\delta A$

Original worked solution:
Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))≈|\frac{∂(x,y)}{∂(u,v)}|\cdot {{\text{Area}(Δ)}_{⏟}}_{\delta A}
$$

 

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}\frac{1}{u} & \frac{1}{v} \\ {v}^{2} & 2uv\end{aligned}| \\  & =\frac{1}{u}\cdot 2uv-\frac{1}{v}\cdot {v}^{2} \\  & =2v-v \\  & =v \\ {\frac{∂(x,y)}{∂(u,v)}|}_{(1,5)} & =v\,{|}_{u=1\,v=5} \\  & =5\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & ≈|5|\cdot \delta A \\  & =5\,\delta A.\end{aligned}
$$

### Parameterized source replay (single repaired field)
### easy / log_product / observed_log_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,5)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\log{\left(u v \right)}\\u v^{2}\end{aligned}]?
$$

- $11\,\delta A$
- $\delta A$
- $5\,\delta A$ **correct**
- $3\,\delta A$
- $8\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{1}{u}&\frac{1}{v}\\v^{2}&2 u v\end{matrix}\right|\\& =(\frac{1}{u})\cdot (2 u v)-(\frac{1}{v})\cdot (v^{2})\\& =2v-v\\& =v\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,5)} & =\left(v\right)\big|_{u=1,v=5}\\& =5\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|5|\cdot\delta A\\ & =5\,\delta A.\end{aligned}
$$

## Original q-161831

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-1,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}v{e}^{u} \\ u{e}^{v}\end{aligned}]?
$$

Raw field 0; correct designation: \delta A

- $\frac{1}{2}\,\delta A$
- $\delta A$
- $4\,\delta A$
- $3\,\delta A$
- $2\,\delta A$
Raw field 1; correct designation: 2\,\delta A

- $\frac{1}{2}\,\delta A$
- $3\,\delta A$
- $4\,\delta A$
- $2\,\delta A$
- $\delta A$

Original worked solution:
Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))≈|\frac{∂(x,y)}{∂(u,v)}|\cdot {{\text{Area}(Δ)}_{⏟}}_{\delta A}
$$

 

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}v{e}^{u} & {e}^{u} \\ {e}^{v} & u{e}^{v}\end{aligned}| \\  & =v{e}^{u}\cdot u{e}^{v}-{e}^{v}\cdot {e}^{u} \\  & =uv{e}^{u+v}-{e}^{u+v} \\  & =(uv-1){e}^{u+v} \\ {\frac{∂(x,y)}{∂(u,v)}|}_{(-1,1)} & =(uv-1){e}^{u+v}\,{|}_{u=-1\,v=1} \\  & =(-1\cdot 1-1){e}^{-1+1} \\  & =-2\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & ≈|-2|\cdot \delta A \\  & =2\,\delta A.\end{aligned}
$$

### Parameterized source replay (single repaired field)
### easy / exp_product / observed_exp_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-1,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}v e^{u}\\u e^{v}\end{aligned}]?
$$

- $4\,\delta A$
- $\delta A$
- $\frac{1}{2}\,\delta A$
- $2\,\delta A$ **correct**
- $3\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}v e^{u}&e^{u}\\e^{v}&u e^{v}\end{matrix}\right|\\& =(v e^{u})\cdot (u e^{v})-(e^{u})\cdot (e^{v})\\& =uv e^{u+v}-e^{u+v}\\& =(uv-1)e^{u+v}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-1,1)} & =\left(\left(u v - 1\right) e^{u} e^{v}\right)\big|_{u=-1,v=1}\\& =\left((-1) (1) - 1\right) e^{(-1)} e^{(1)}\\& =-2\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-2|\cdot\delta A\\ & =2\,\delta A.\end{aligned}
$$

## Original q-161873

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(2,2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\frac{1}{u}-v \\ {u}^{2}v\end{aligned}]?
$$

Raw field 0; correct designation: 7\,\delta A

- $14\,\delta A$
- $7\,\delta A$
- $6\,\delta A$
- $9\,\delta A$
- $5\,\delta A$

Original worked solution:
Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))≈|\frac{∂(x,y)}{∂(u,v)}|\cdot {{\text{Area}(Δ)}_{⏟}}_{\delta A}
$$

 

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}-\frac{1}{{u}^{2}} & -1 \\ 2uv & {u}^{2}\end{aligned}| \\  & =(-\frac{1}{{u}^{2}})\cdot ({u}^{2})-2uv\cdot (-1) \\  & =-1+2uv \\ {\frac{∂(x,y)}{∂(u,v)}|}_{(2,2)} & =(-1+2uv)\,{|}_{u=2\,v=2} \\  & =-1+2(2)(2) \\  & =7\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & ≈|7|\cdot \delta A \\  & =7\,\delta A.\end{aligned}
$$

### Parameterized source replay (single repaired field)
### easy / reciprocal_product / observed_reciprocal_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(2,2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}- v + \frac{1}{u}\\u^{2} v\end{aligned}]?
$$

- $6\,\delta A$
- $7\,\delta A$ **correct**
- $14\,\delta A$
- $5\,\delta A$
- $9\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}- \frac{1}{u^{2}}&-1\\2 u v&u^{2}\end{matrix}\right|\\& =(- \frac{1}{u^{2}})\cdot (u^{2})-(-1)\cdot (2 u v)\\& =-1+2uv\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(2,2)} & =\left(2 u v - 1\right)\big|_{u=2,v=2}\\& =2 (2) (2) - 1\\& =7\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|7|\cdot\delta A\\ & =7\,\delta A.\end{aligned}
$$

## Original q-161874

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\sqrt{u}+{v}^{2} \\ uv\end{aligned}]?
$$

Raw field 0; correct designation: 7\,\delta A

- $15\,\delta A$
- $7\,\delta A$
- $21\,\delta A$
- $3\,\delta A$
- $12\,\delta A$

Original worked solution:
Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))≈|\frac{∂(x,y)}{∂(u,v)}|\cdot {{\text{Area}(Δ)}_{⏟}}_{\delta A}
$$

 

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}\frac{1}{2\sqrt{u}} & 2v \\ v & u\end{aligned}| \\  & =\frac{1}{2\sqrt{u}}\cdot u-v\cdot 2v \\  & =\frac{1}{2}\sqrt{u}-2{v}^{2} \\ {\frac{∂(x,y)}{∂(u,v)}|}_{(4,2)} & ={\frac{1}{2}\sqrt{u}-2{v}^{2}\,|}_{u=4\,v=2} \\  & =\frac{1}{2}\sqrt{4}-2(2)^{2} \\  & =-7\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & ≈|-7|\cdot \delta A \\  & =7\,\delta A.\end{aligned}
$$

### Parameterized source replay (single repaired field)
### easy / sqrt_sum / observed_sqrt_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\sqrt{u} + v^{2}\\u v\end{aligned}]?
$$

- $21\,\delta A$
- $7\,\delta A$ **correct**
- $15\,\delta A$
- $12\,\delta A$
- $3\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{1}{2 \sqrt{u}}&2 v\\v&u\end{matrix}\right|\\& =(\frac{1}{2 \sqrt{u}})\cdot (u)-(2 v)\cdot (v)\\& =\frac{1}{2}\sqrt{u}-2v^{2}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,2)} & =\left(- \frac{- \sqrt{u} + 4 v^{2}}{2}\right)\big|_{u=4,v=2}\\& =- \frac{4 (2)^{2} - \sqrt{(4)}}{2}\\& =-7\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-7|\cdot\delta A\\ & =7\,\delta A.\end{aligned}
$$

## Original q-161875

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(0,3)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\operatorname{cos}⁡u-{v}^{2} \\ u+v\end{aligned}]?
$$

Raw field 0; correct designation: 6\,\delta A

- $12\,\delta A$
- $6\,\delta A$
- $16\,\delta A$
- $9\,\delta A$
- $3\,\delta A$

Original worked solution:
Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))≈|\frac{∂(x,y)}{∂(u,v)}|\cdot {{\text{Area}(Δ)}_{⏟}}_{\delta A}
$$

 

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}-\operatorname{sin}⁡u & -2v \\ 1 & 1\end{aligned}| \\  & =(-\operatorname{sin}⁡u)\cdot 1-1\cdot (-2v) \\  & =-\operatorname{sin}⁡u+2v \\ {\frac{∂(x,y)}{∂(u,v)}|}_{(0,3)} & =(-\operatorname{sin}⁡u+2v)\,{|}_{u=0\,v=3} \\  & =-\operatorname{sin}⁡0+2(3) \\  & =6\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & ≈|6|\cdot \delta A \\  & =6\,\delta A.\end{aligned}
$$

### Parameterized source replay (single repaired field)
### easy / cos_sum / observed_cos_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(0,3)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}- v^{2} + \cos{\left(u \right)}\\u + v\end{aligned}]?
$$

- $16\,\delta A$
- $6\,\delta A$ **correct**
- $12\,\delta A$
- $3\,\delta A$
- $9\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}- \sin{\left(u \right)}&- 2 v\\1&1\end{matrix}\right|\\& =(- \sin{\left(u \right)})\cdot (1)-(- 2 v)\cdot (1)\\& =-\sin u+2v\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(0,3)} & =\left(2 v - \sin{\left(u \right)}\right)\big|_{u=0,v=3}\\& =2 (3) - \sin{\left((0) \right)}\\& =6\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|6|\cdot\delta A\\ & =6\,\delta A.\end{aligned}
$$

## Original q-161885

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(2,4)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\frac{{u}^{2}}{v} \\ uv\end{aligned}]?
$$

Raw field 0; correct designation: 3\,\delta A

- $3\,\delta A$
- $\delta A$
- $9\,\delta A$
- $6\,\delta A$
- $12\,\delta A$

Original worked solution:
Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))≈|\frac{∂(x,y)}{∂(u,v)}|\cdot {{\text{Area}(Δ)}_{⏟}}_{\delta A}
$$

 

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}\frac{2u}{v} & -\frac{{u}^{2}}{{v}^{2}} \\ v & u\end{aligned}| \\  & =\frac{2u}{v}\cdot u-v\cdot (-\frac{{u}^{2}}{{v}^{2}}) \\  & =\frac{2{u}^{2}}{v}+\frac{{u}^{2}}{v} \\  & =\frac{3{u}^{2}}{v} \\ {\frac{∂(x,y)}{∂(u,v)}|}_{(2,4)} & =(\frac{3{u}^{2}}{v})\,{|}_{u=2\,v=4} \\  & =\frac{3(2)^{2}}{4} \\  & =3\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & ≈|3|\cdot \delta A \\  & =3\,\delta A.\end{aligned}
$$

### Parameterized source replay (single repaired field)
### easy / quotient_product / observed_quotient_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(2,4)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\frac{u^{2}}{v}\\u v\end{aligned}]?
$$

- $9\,\delta A$
- $\delta A$
- $3\,\delta A$ **correct**
- $12\,\delta A$
- $6\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{2 u}{v}&- \frac{u^{2}}{v^{2}}\\v&u\end{matrix}\right|\\& =(\frac{2 u}{v})\cdot (u)-(- \frac{u^{2}}{v^{2}})\cdot (v)\\& =\frac{2u^{2}}{v}+\frac{u^{2}}{v}\\& =\frac{3u^{2}}{v}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(2,4)} & =\left(\frac{3 u^{2}}{v}\right)\big|_{u=2,v=4}\\& =\frac{3 (2)^{2}}{(4)}\\& =3\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|3|\cdot\delta A\\ & =3\,\delta A.\end{aligned}
$$

## Original q-161887

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,4)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\sqrt{uv} \\ u{v}^{2}\end{aligned}]?
$$

Raw field 0; correct designation: 4\,\delta A

- $16\,\delta A$
- $8\,\delta A$
- $12\,\delta A$
- $4\,\delta A$
- $2\,\delta A$

Original worked solution:
Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))≈|\frac{∂(x,y)}{∂(u,v)}|\cdot {{\text{Area}(Δ)}_{⏟}}_{\delta A}
$$

 

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}\frac{\sqrt{v}}{2\sqrt{u}} & \frac{\sqrt{u}}{2\sqrt{v}} \\ {v}^{2} & 2uv\end{aligned}| \\  & =\frac{\sqrt{v}}{2\sqrt{u}}\cdot 2uv-{v}^{2}\cdot \frac{\sqrt{u}}{2\sqrt{v}} \\  & =v\sqrt{uv}-\frac{1}{2}v\sqrt{uv} \\  & =\frac{1}{2}v\sqrt{uv} \\ {\frac{∂(x,y)}{∂(u,v)}|}_{(1,4)} & ={(\frac{1}{2}v\sqrt{uv})\,|}_{u=1\,v=4} \\  & =\frac{1}{2}(4)\sqrt{(1)(4)} \\  & =4\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & ≈|4|\cdot \delta A \\  & =4\,\delta A.\end{aligned}
$$

### Parameterized source replay (single repaired field)
### easy / sqrt_product / observed_sqrt_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,4)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\sqrt{u v}\\u v^{2}\end{aligned}]?
$$

- $12\,\delta A$
- $8\,\delta A$
- $16\,\delta A$
- $2\,\delta A$
- $4\,\delta A$ **correct**

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{\sqrt{u v}}{2 u}&\frac{\sqrt{u v}}{2 v}\\v^{2}&2 u v\end{matrix}\right|\\& =(\frac{\sqrt{u v}}{2 u})\cdot (2 u v)-(\frac{\sqrt{u v}}{2 v})\cdot (v^{2})\\& =v\sqrt{uv}-\frac{1}{2}v\sqrt{uv}\\& =\frac{1}{2}v\sqrt{uv}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,4)} & =\left(\frac{v \sqrt{u v}}{2}\right)\big|_{u=1,v=4}\\& =\frac{(4) \sqrt{(1) (4)}}{2}\\& =4\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|4|\cdot\delta A\\ & =4\,\delta A.\end{aligned}
$$

## Original q-161877

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(2,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}\operatorname{ln}⁡(u-v) \\ v-{u}^{2}\end{aligned}]?
$$

Raw field 0; correct designation: 3\,\delta A

- $12\,\delta A$
- $5\,\delta A$
- $3\,\delta A$
- $6\,\delta A$
- $\delta A$

Original worked solution:
Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))≈|\frac{∂(x,y)}{∂(u,v)}|\cdot {{\text{Area}(Δ)}_{⏟}}_{\delta A}
$$

 

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}\frac{1}{u-v} & -\frac{1}{u-v} \\ -2u & 1\end{aligned}| \\  & =\frac{1}{u-v}\cdot 1-(-2u)\cdot (-\frac{1}{u-v}) \\  & =\frac{1-2u}{u-v} \\ {\frac{∂(x,y)}{∂(u,v)}|}_{(2,1)} & ={(\frac{1-2u}{u-v})\,|}_{u=2\,v=1} \\  & =\frac{1-2(2)}{2-1} \\  & =-3\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & ≈|-3|\cdot \delta A \\  & =3\,\delta A.\end{aligned}
$$

### Parameterized source replay (single repaired field)
### easy / log_difference / observed_log_difference

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(2,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\log{\left(u - v \right)}\\- u^{2} + v\end{aligned}]?
$$

- $3\,\delta A$ **correct**
- $5\,\delta A$
- $12\,\delta A$
- $\delta A$
- $6\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{1}{u - v}&- \frac{1}{u - v}\\- 2 u&1\end{matrix}\right|\\& =(\frac{1}{u - v})\cdot (1)-(- \frac{1}{u - v})\cdot (- 2 u)\\& =\frac{1-2u}{u-v}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(2,1)} & =\left(- \frac{2 u - 1}{u - v}\right)\big|_{u=2,v=1}\\& =- \frac{2 (2) - 1}{- (1) + (2)}\\& =-3\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-3|\cdot\delta A\\ & =3\,\delta A.\end{aligned}
$$

## Original q-161878

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-3,3)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}u+{v}^{2} \\ \operatorname{sin}⁡(u+v)\end{aligned}]?
$$

Raw field 0; correct designation: 5\,\delta A

- $12\,\delta A$
- $5\,\delta A$
- $6\,\delta A$
- $2\,\delta A$
- $7\,\delta A$

Original worked solution:
Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))≈|\frac{∂(x,y)}{∂(u,v)}|\cdot {{\text{Area}(Δ)}_{⏟}}_{\delta A}
$$

 

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}1 & 2v \\ \operatorname{cos}⁡(u+v) & \operatorname{cos}⁡(u+v)\end{aligned}| \\  & =1\cdot \operatorname{cos}⁡(u+v)-\operatorname{cos}⁡(u+v)\cdot 2v \\  & =(1-2v)\operatorname{cos}⁡(u+v) \\ {\frac{∂(x,y)}{∂(u,v)}|}_{(-3,3)} & =(1-2v)\operatorname{cos}⁡(u+v)\,{|}_{u=-3\,v=3} \\  & =(1-2(3))\operatorname{cos}⁡(-3+3) \\  & =-5\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & ≈|-5|\cdot \delta A \\  & =5\,\delta A.\end{aligned}
$$

### Parameterized source replay (single repaired field)
### easy / sin_sum / observed_sin_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-3,3)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u + v^{2}\\\sin{\left(u + v \right)}\end{aligned}]?
$$

- $6\,\delta A$
- $5\,\delta A$ **correct**
- $12\,\delta A$
- $7\,\delta A$
- $2\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}1&2 v\\\cos{\left(u + v \right)}&\cos{\left(u + v \right)}\end{matrix}\right|\\& =(1)\cdot (\cos{\left(u + v \right)})-(2 v)\cdot (\cos{\left(u + v \right)})\\& =(1-2v)\cos(u+v)\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-3,3)} & =\left(- \left(2 v - 1\right) \cos{\left(u + v \right)}\right)\big|_{u=-3,v=3}\\& =- \left(2 (3) - 1\right) \cos{\left((-3) + (3) \right)}\\& =-5\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-5|\cdot\delta A\\ & =5\,\delta A.\end{aligned}
$$

## Original q-161876

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-2,2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]⟶[\begin{aligned}{e}^{u+v} \\ {u}^{3}+v\end{aligned}]?
$$

Raw field 0; correct designation: 11\,\delta A

- $21\,\delta A$
- $18\,\delta A$
- $13\,\delta A$
- $11\,\delta A$
- $17\,\delta A$

Original worked solution:
Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))≈|\frac{∂(x,y)}{∂(u,v)}|\cdot {{\text{Area}(Δ)}_{⏟}}_{\delta A}
$$

 

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}{e}^{u+v} & {e}^{u+v} \\ 3{u}^{2} & 1\end{aligned}| \\  & ={e}^{u+v}\cdot 1-3{u}^{2}\cdot {e}^{u+v} \\  & ={e}^{u+v}(1-3{u}^{2}) \\ {\frac{∂(x,y)}{∂(u,v)}|}_{(-2,2)} & ={e}^{u+v}(1-3{u}^{2})\,{|}_{u=-2\,v=2} \\  & ={e}^{-2+2}(1-3(-2)^{2}) \\  & =-11\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & ≈|-11|\cdot \delta A \\  & =11\,\delta A.\end{aligned}
$$

### Parameterized source replay (single repaired field)
### easy / exp_sum / observed_exp_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-2,2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}e^{u + v}\\u^{3} + v\end{aligned}]?
$$

- $13\,\delta A$
- $18\,\delta A$
- $21\,\delta A$
- $17\,\delta A$
- $11\,\delta A$ **correct**

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}e^{u} e^{v}&e^{u} e^{v}\\3 u^{2}&1\end{matrix}\right|\\& =(e^{u} e^{v})\cdot (1)-(e^{u} e^{v})\cdot (3 u^{2})\\& =e^{u+v}(1-3u^{2})\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-2,2)} & =\left(- \left(3 u^{2} - 1\right) e^{u} e^{v}\right)\big|_{u=-2,v=2}\\& =- \left(3 (-2)^{2} - 1\right) e^{(-2)} e^{(2)}\\& =-11\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-11|\cdot\delta A\\ & =11\,\delta A.\end{aligned}
$$

# Clearly labeled generated variants

Observed profile variants are proportional-shape replay extensions with unresolved original distractor intent; authored profiles and missing levels are labeled in each record.

### easy / poly_sum / observed_poly_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u^{2} + v\\2 u - v^{3}\end{aligned}]?
$$

- $8\,\delta A$ **correct**
- $\frac{8}{13}\,\delta A$
- $\frac{56}{13}\,\delta A$
- $\frac{20}{13}\,\delta A$
- $\frac{144}{13}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}2 u&1\\2&- 3 v^{2}\end{matrix}\right|\\& =(2 u)\cdot (- 3 v^{2})-(1)\cdot (2)\\& =-6uv^{2}-2\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,1)} & =\left(- 2 \left(3 u v^{2} + 1\right)\right)\big|_{u=1,v=1}\\& =- 2 \left(3 (1) (1)^{2} + 1\right)\\& =-8\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-8|\cdot\delta A\\ & =8\,\delta A.\end{aligned}
$$

### easy / poly_sum / observed_poly_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u^{2} + v\\2 u - v^{3}\end{aligned}]?
$$

- $26\,\delta A$ **correct**
- $5\,\delta A$
- $2\,\delta A$
- $36\,\delta A$
- $14\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}2 u&1\\2&- 3 v^{2}\end{matrix}\right|\\& =(2 u)\cdot (- 3 v^{2})-(1)\cdot (2)\\& =-6uv^{2}-2\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,1)} & =\left(- 2 \left(3 u v^{2} + 1\right)\right)\big|_{u=4,v=1}\\& =- 2 \left(3 (1)^{2} (4) + 1\right)\\& =-26\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-26|\cdot\delta A\\ & =26\,\delta A.\end{aligned}
$$

### easy / log_product / observed_log_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(2,8)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\log{\left(u v \right)}\\u v^{2}\end{aligned}]?
$$

- $\frac{64}{5}\,\delta A$
- $\frac{88}{5}\,\delta A$
- $8\,\delta A$ **correct**
- $\frac{24}{5}\,\delta A$
- $\frac{8}{5}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{1}{u}&\frac{1}{v}\\v^{2}&2 u v\end{matrix}\right|\\& =(\frac{1}{u})\cdot (2 u v)-(\frac{1}{v})\cdot (v^{2})\\& =2v-v\\& =v\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(2,8)} & =\left(v\right)\big|_{u=2,v=8}\\& =8\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|8|\cdot\delta A\\ & =8\,\delta A.\end{aligned}
$$

### easy / log_product / observed_log_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(3,4)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\log{\left(u v \right)}\\u v^{2}\end{aligned}]?
$$

- $\frac{32}{5}\,\delta A$
- $\frac{44}{5}\,\delta A$
- $\frac{4}{5}\,\delta A$
- $\frac{12}{5}\,\delta A$
- $4\,\delta A$ **correct**

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{1}{u}&\frac{1}{v}\\v^{2}&2 u v\end{matrix}\right|\\& =(\frac{1}{u})\cdot (2 u v)-(\frac{1}{v})\cdot (v^{2})\\& =2v-v\\& =v\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(3,4)} & =\left(v\right)\big|_{u=3,v=4}\\& =4\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|4|\cdot\delta A\\ & =4\,\delta A.\end{aligned}
$$

### easy / exp_product / observed_exp_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,-1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}v e^{u}\\u e^{v}\end{aligned}]?
$$

- $3\,\delta A$
- $\frac{1}{2}\,\delta A$
- $4\,\delta A$
- $2\,\delta A$ **correct**
- $\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}v e^{u}&e^{u}\\e^{v}&u e^{v}\end{matrix}\right|\\& =(v e^{u})\cdot (u e^{v})-(e^{u})\cdot (e^{v})\\& =uv e^{u+v}-e^{u+v}\\& =(uv-1)e^{u+v}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,-1)} & =\left(\left(u v - 1\right) e^{u} e^{v}\right)\big|_{u=1,v=-1}\\& =\left((-1) (1) - 1\right) e^{(-1)} e^{(1)}\\& =-2\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-2|\cdot\delta A\\ & =2\,\delta A.\end{aligned}
$$

### easy / exp_product / observed_exp_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,-4)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}v e^{u}\\u e^{v}\end{aligned}]?
$$

- $\frac{51}{2}\,\delta A$
- $17\,\delta A$ **correct**
- $\frac{17}{4}\,\delta A$
- $\frac{17}{2}\,\delta A$
- $34\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}v e^{u}&e^{u}\\e^{v}&u e^{v}\end{matrix}\right|\\& =(v e^{u})\cdot (u e^{v})-(e^{u})\cdot (e^{v})\\& =uv e^{u+v}-e^{u+v}\\& =(uv-1)e^{u+v}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,-4)} & =\left(\left(u v - 1\right) e^{u} e^{v}\right)\big|_{u=4,v=-4}\\& =\left((-4) (4) - 1\right) e^{(-4)} e^{(4)}\\& =-17\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-17|\cdot\delta A\\ & =17\,\delta A.\end{aligned}
$$

### easy / reciprocal_product / observed_reciprocal_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}- v + \frac{1}{u}\\u^{2} v\end{aligned}]?
$$

- $\frac{9}{7}\,\delta A$
- $2\,\delta A$
- $\frac{6}{7}\,\delta A$
- $\frac{5}{7}\,\delta A$
- $\delta A$ **correct**

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}- \frac{1}{u^{2}}&-1\\2 u v&u^{2}\end{matrix}\right|\\& =(- \frac{1}{u^{2}})\cdot (u^{2})-(-1)\cdot (2 u v)\\& =-1+2uv\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,1)} & =\left(2 u v - 1\right)\big|_{u=1,v=1}\\& =2 (1) (1) - 1\\& =1\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|1|\cdot\delta A\\ & =\delta A.\end{aligned}
$$

### easy / reciprocal_product / observed_reciprocal_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}- v + \frac{1}{u}\\u^{2} v\end{aligned}]?
$$

- $9\,\delta A$
- $5\,\delta A$
- $14\,\delta A$
- $7\,\delta A$ **correct**
- $6\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}- \frac{1}{u^{2}}&-1\\2 u v&u^{2}\end{matrix}\right|\\& =(- \frac{1}{u^{2}})\cdot (u^{2})-(-1)\cdot (2 u v)\\& =-1+2uv\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,1)} & =\left(2 u v - 1\right)\big|_{u=4,v=1}\\& =2 (1) (4) - 1\\& =7\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|7|\cdot\delta A\\ & =7\,\delta A.\end{aligned}
$$

### easy / sqrt_sum / observed_sqrt_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(9,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\sqrt{u} + v^{2}\\u v\end{aligned}]?
$$

- $\frac{3}{14}\,\delta A$
- $\frac{15}{14}\,\delta A$
- $\frac{3}{2}\,\delta A$
- $\frac{6}{7}\,\delta A$
- $\frac{1}{2}\,\delta A$ **correct**

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{1}{2 \sqrt{u}}&2 v\\v&u\end{matrix}\right|\\& =(\frac{1}{2 \sqrt{u}})\cdot (u)-(2 v)\cdot (v)\\& =\frac{1}{2}\sqrt{u}-2v^{2}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(9,1)} & =\left(- \frac{- \sqrt{u} + 4 v^{2}}{2}\right)\big|_{u=9,v=1}\\& =- \frac{4 (1)^{2} - \sqrt{(9)}}{2}\\& =- \frac{1}{2}\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|- \frac{1}{2}|\cdot\delta A\\ & =\frac{1}{2}\,\delta A.\end{aligned}
$$

### easy / sqrt_sum / observed_sqrt_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\sqrt{u} + v^{2}\\u v\end{aligned}]?
$$

- $3\,\delta A$
- $\frac{12}{7}\,\delta A$
- $\frac{3}{7}\,\delta A$
- $\frac{15}{7}\,\delta A$
- $\delta A$ **correct**

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{1}{2 \sqrt{u}}&2 v\\v&u\end{matrix}\right|\\& =(\frac{1}{2 \sqrt{u}})\cdot (u)-(2 v)\cdot (v)\\& =\frac{1}{2}\sqrt{u}-2v^{2}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,1)} & =\left(- \frac{- \sqrt{u} + 4 v^{2}}{2}\right)\big|_{u=4,v=1}\\& =- \frac{4 (1)^{2} - \sqrt{(4)}}{2}\\& =-1\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-1|\cdot\delta A\\ & =\delta A.\end{aligned}
$$

### easy / cos_sum / observed_cos_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(0,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}- v^{2} + \cos{\left(u \right)}\\u + v\end{aligned}]?
$$

- $3\,\delta A$
- $4\,\delta A$
- $\frac{16}{3}\,\delta A$
- $\delta A$
- $2\,\delta A$ **correct**

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}- \sin{\left(u \right)}&- 2 v\\1&1\end{matrix}\right|\\& =(- \sin{\left(u \right)})\cdot (1)-(- 2 v)\cdot (1)\\& =-\sin u+2v\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(0,1)} & =\left(2 v - \sin{\left(u \right)}\right)\big|_{u=0,v=1}\\& =2 (1) - \sin{\left((0) \right)}\\& =2\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|2|\cdot\delta A\\ & =2\,\delta A.\end{aligned}
$$

### easy / cos_sum / observed_cos_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(0,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}- v^{2} + \cos{\left(u \right)}\\u + v\end{aligned}]?
$$

- $3\,\delta A$
- $\delta A$
- $4\,\delta A$
- $2\,\delta A$ **correct**
- $\frac{16}{3}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}- \sin{\left(u \right)}&- 2 v\\1&1\end{matrix}\right|\\& =(- \sin{\left(u \right)})\cdot (1)-(- 2 v)\cdot (1)\\& =-\sin u+2v\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(0,1)} & =\left(2 v - \sin{\left(u \right)}\right)\big|_{u=0,v=1}\\& =2 (1) - \sin{\left((0) \right)}\\& =2\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|2|\cdot\delta A\\ & =2\,\delta A.\end{aligned}
$$

### easy / quotient_product / observed_quotient_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\frac{u^{2}}{v}\\u v\end{aligned}]?
$$

- $6\,\delta A$
- $3\,\delta A$ **correct**
- $9\,\delta A$
- $12\,\delta A$
- $\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{2 u}{v}&- \frac{u^{2}}{v^{2}}\\v&u\end{matrix}\right|\\& =(\frac{2 u}{v})\cdot (u)-(- \frac{u^{2}}{v^{2}})\cdot (v)\\& =\frac{2u^{2}}{v}+\frac{u^{2}}{v}\\& =\frac{3u^{2}}{v}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,1)} & =\left(\frac{3 u^{2}}{v}\right)\big|_{u=1,v=1}\\& =\frac{3 (1)^{2}}{(1)}\\& =3\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|3|\cdot\delta A\\ & =3\,\delta A.\end{aligned}
$$

### easy / quotient_product / observed_quotient_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\frac{u^{2}}{v}\\u v\end{aligned}]?
$$

- $96\,\delta A$
- $192\,\delta A$
- $48\,\delta A$ **correct**
- $16\,\delta A$
- $144\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{2 u}{v}&- \frac{u^{2}}{v^{2}}\\v&u\end{matrix}\right|\\& =(\frac{2 u}{v})\cdot (u)-(- \frac{u^{2}}{v^{2}})\cdot (v)\\& =\frac{2u^{2}}{v}+\frac{u^{2}}{v}\\& =\frac{3u^{2}}{v}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,1)} & =\left(\frac{3 u^{2}}{v}\right)\big|_{u=4,v=1}\\& =\frac{3 (4)^{2}}{(1)}\\& =48\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|48|\cdot\delta A\\ & =48\,\delta A.\end{aligned}
$$

### easy / sqrt_product / observed_sqrt_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(9,9)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\sqrt{u v}\\u v^{2}\end{aligned}]?
$$

- $\frac{81}{2}\,\delta A$ **correct**
- $162\,\delta A$
- $\frac{243}{2}\,\delta A$
- $\frac{81}{4}\,\delta A$
- $81\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{\sqrt{u v}}{2 u}&\frac{\sqrt{u v}}{2 v}\\v^{2}&2 u v\end{matrix}\right|\\& =(\frac{\sqrt{u v}}{2 u})\cdot (2 u v)-(\frac{\sqrt{u v}}{2 v})\cdot (v^{2})\\& =v\sqrt{uv}-\frac{1}{2}v\sqrt{uv}\\& =\frac{1}{2}v\sqrt{uv}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(9,9)} & =\left(\frac{v \sqrt{u v}}{2}\right)\big|_{u=9,v=9}\\& =\frac{(9) \sqrt{(9) (9)}}{2}\\& =\frac{81}{2}\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|\frac{81}{2}|\cdot\delta A\\ & =\frac{81}{2}\,\delta A.\end{aligned}
$$

### easy / sqrt_product / observed_sqrt_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\sqrt{u v}\\u v^{2}\end{aligned}]?
$$

- $\delta A$ **correct**
- $3\,\delta A$
- $2\,\delta A$
- $\frac{1}{2}\,\delta A$
- $4\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{\sqrt{u v}}{2 u}&\frac{\sqrt{u v}}{2 v}\\v^{2}&2 u v\end{matrix}\right|\\& =(\frac{\sqrt{u v}}{2 u})\cdot (2 u v)-(\frac{\sqrt{u v}}{2 v})\cdot (v^{2})\\& =v\sqrt{uv}-\frac{1}{2}v\sqrt{uv}\\& =\frac{1}{2}v\sqrt{uv}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,1)} & =\left(\frac{v \sqrt{u v}}{2}\right)\big|_{u=4,v=1}\\& =\frac{(1) \sqrt{(1) (4)}}{2}\\& =1\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|1|\cdot\delta A\\ & =\delta A.\end{aligned}
$$

### easy / log_difference / observed_log_difference

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(3,2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\log{\left(u - v \right)}\\- u^{2} + v\end{aligned}]?
$$

- $10\,\delta A$
- $5\,\delta A$ **correct**
- $20\,\delta A$
- $\frac{5}{3}\,\delta A$
- $\frac{25}{3}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{1}{u - v}&- \frac{1}{u - v}\\- 2 u&1\end{matrix}\right|\\& =(\frac{1}{u - v})\cdot (1)-(- \frac{1}{u - v})\cdot (- 2 u)\\& =\frac{1-2u}{u-v}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(3,2)} & =\left(- \frac{2 u - 1}{u - v}\right)\big|_{u=3,v=2}\\& =- \frac{2 (3) - 1}{- (2) + (3)}\\& =-5\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-5|\cdot\delta A\\ & =5\,\delta A.\end{aligned}
$$

### easy / log_difference / observed_log_difference

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,-2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\log{\left(u - v \right)}\\- u^{2} + v\end{aligned}]?
$$

- $\frac{7}{3}\,\delta A$
- $\frac{7}{6}\,\delta A$ **correct**
- $\frac{35}{18}\,\delta A$
- $\frac{7}{18}\,\delta A$
- $\frac{14}{3}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{1}{u - v}&- \frac{1}{u - v}\\- 2 u&1\end{matrix}\right|\\& =(\frac{1}{u - v})\cdot (1)-(- \frac{1}{u - v})\cdot (- 2 u)\\& =\frac{1-2u}{u-v}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,-2)} & =\left(- \frac{2 u - 1}{u - v}\right)\big|_{u=4,v=-2}\\& =- \frac{2 (4) - 1}{- (-2) + (4)}\\& =- \frac{7}{6}\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|- \frac{7}{6}|\cdot\delta A\\ & =\frac{7}{6}\,\delta A.\end{aligned}
$$

### easy / sin_sum / observed_sin_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,-1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u + v^{2}\\\sin{\left(u + v \right)}\end{aligned}]?
$$

- $\frac{6}{5}\,\delta A$
- $\frac{36}{5}\,\delta A$
- $\frac{18}{5}\,\delta A$
- $\frac{21}{5}\,\delta A$
- $3\,\delta A$ **correct**

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}1&2 v\\\cos{\left(u + v \right)}&\cos{\left(u + v \right)}\end{matrix}\right|\\& =(1)\cdot (\cos{\left(u + v \right)})-(2 v)\cdot (\cos{\left(u + v \right)})\\& =(1-2v)\cos(u+v)\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,-1)} & =\left(- \left(2 v - 1\right) \cos{\left(u + v \right)}\right)\big|_{u=1,v=-1}\\& =- \left(2 (-1) - 1\right) \cos{\left((-1) + (1) \right)}\\& =3\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|3|\cdot\delta A\\ & =3\,\delta A.\end{aligned}
$$

### easy / sin_sum / observed_sin_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,-4)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u + v^{2}\\\sin{\left(u + v \right)}\end{aligned}]?
$$

- $\frac{18}{5}\,\delta A$
- $\frac{63}{5}\,\delta A$
- $\frac{108}{5}\,\delta A$
- $9\,\delta A$ **correct**
- $\frac{54}{5}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}1&2 v\\\cos{\left(u + v \right)}&\cos{\left(u + v \right)}\end{matrix}\right|\\& =(1)\cdot (\cos{\left(u + v \right)})-(2 v)\cdot (\cos{\left(u + v \right)})\\& =(1-2v)\cos(u+v)\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,-4)} & =\left(- \left(2 v - 1\right) \cos{\left(u + v \right)}\right)\big|_{u=4,v=-4}\\& =- \left(2 (-4) - 1\right) \cos{\left((-4) + (4) \right)}\\& =9\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|9|\cdot\delta A\\ & =9\,\delta A.\end{aligned}
$$

### easy / exp_sum / observed_exp_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,-1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}e^{u + v}\\u^{3} + v\end{aligned}]?
$$

- $2\,\delta A$ **correct**
- $\frac{42}{11}\,\delta A$
- $\frac{26}{11}\,\delta A$
- $\frac{34}{11}\,\delta A$
- $\frac{36}{11}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}e^{u} e^{v}&e^{u} e^{v}\\3 u^{2}&1\end{matrix}\right|\\& =(e^{u} e^{v})\cdot (1)-(e^{u} e^{v})\cdot (3 u^{2})\\& =e^{u+v}(1-3u^{2})\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,-1)} & =\left(- \left(3 u^{2} - 1\right) e^{u} e^{v}\right)\big|_{u=1,v=-1}\\& =- \left(3 (1)^{2} - 1\right) e^{(-1)} e^{(1)}\\& =-2\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-2|\cdot\delta A\\ & =2\,\delta A.\end{aligned}
$$

### easy / exp_sum / observed_exp_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,-4)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}e^{u + v}\\u^{3} + v\end{aligned}]?
$$

- $47\,\delta A$ **correct**
- $\frac{799}{11}\,\delta A$
- $\frac{987}{11}\,\delta A$
- $\frac{846}{11}\,\delta A$
- $\frac{611}{11}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}e^{u} e^{v}&e^{u} e^{v}\\3 u^{2}&1\end{matrix}\right|\\& =(e^{u} e^{v})\cdot (1)-(e^{u} e^{v})\cdot (3 u^{2})\\& =e^{u+v}(1-3u^{2})\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,-4)} & =\left(- \left(3 u^{2} - 1\right) e^{u} e^{v}\right)\big|_{u=4,v=-4}\\& =- \left(3 (4)^{2} - 1\right) e^{(-4)} e^{(4)}\\& =-47\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-47|\cdot\delta A\\ & =47\,\delta A.\end{aligned}
$$

### easy / poly_sum / legacy_poly_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u^{2} + v\\2 u - v^{3}\end{aligned}]?
$$

- $8\,\delta A$ **correct**
- $\frac{8}{13}\,\delta A$
- $\frac{56}{13}\,\delta A$
- $\frac{20}{13}\,\delta A$
- $\frac{144}{13}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}2 u&1\\2&- 3 v^{2}\end{matrix}\right|\\& =(2 u)\cdot (- 3 v^{2})-(1)\cdot (2)\\& =-6uv^{2}-2\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,1)} & =\left(- 2 \left(3 u v^{2} + 1\right)\right)\big|_{u=1,v=1}\\& =- 2 \left(3 (1) (1)^{2} + 1\right)\\& =-8\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-8|\cdot\delta A\\ & =8\,\delta A.\end{aligned}
$$

### easy / poly_sum / legacy_poly_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u^{2} + v\\2 u - v^{3}\end{aligned}]?
$$

- $26\,\delta A$ **correct**
- $5\,\delta A$
- $2\,\delta A$
- $36\,\delta A$
- $14\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}2 u&1\\2&- 3 v^{2}\end{matrix}\right|\\& =(2 u)\cdot (- 3 v^{2})-(1)\cdot (2)\\& =-6uv^{2}-2\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,1)} & =\left(- 2 \left(3 u v^{2} + 1\right)\right)\big|_{u=4,v=1}\\& =- 2 \left(3 (1)^{2} (4) + 1\right)\\& =-26\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-26|\cdot\delta A\\ & =26\,\delta A.\end{aligned}
$$

### easy / exp_product / legacy_exp_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,-1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}v e^{u}\\u e^{v}\end{aligned}]?
$$

- $3\,\delta A$
- $\frac{1}{2}\,\delta A$
- $4\,\delta A$
- $2\,\delta A$ **correct**
- $\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}v e^{u}&e^{u}\\e^{v}&u e^{v}\end{matrix}\right|\\& =(v e^{u})\cdot (u e^{v})-(e^{u})\cdot (e^{v})\\& =uv e^{u+v}-e^{u+v}\\& =(uv-1)e^{u+v}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,-1)} & =\left(\left(u v - 1\right) e^{u} e^{v}\right)\big|_{u=1,v=-1}\\& =\left((-1) (1) - 1\right) e^{(-1)} e^{(1)}\\& =-2\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-2|\cdot\delta A\\ & =2\,\delta A.\end{aligned}
$$

### easy / exp_product / legacy_exp_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,-4)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}v e^{u}\\u e^{v}\end{aligned}]?
$$

- $\frac{51}{2}\,\delta A$
- $17\,\delta A$ **correct**
- $\frac{17}{4}\,\delta A$
- $\frac{17}{2}\,\delta A$
- $34\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}v e^{u}&e^{u}\\e^{v}&u e^{v}\end{matrix}\right|\\& =(v e^{u})\cdot (u e^{v})-(e^{u})\cdot (e^{v})\\& =uv e^{u+v}-e^{u+v}\\& =(uv-1)e^{u+v}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,-4)} & =\left(\left(u v - 1\right) e^{u} e^{v}\right)\big|_{u=4,v=-4}\\& =\left((-4) (4) - 1\right) e^{(-4)} e^{(4)}\\& =-17\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-17|\cdot\delta A\\ & =17\,\delta A.\end{aligned}
$$

### easy / poly_sum / authored_area_poly_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u^{2} + v\\2 u - v^{3}\end{aligned}]?
$$

- $16\,\delta A$
- $8\,\delta A$ **correct**
- $\frac{1}{8}\,\delta A$
- $4\,\delta A$
- $64\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}2 u&1\\2&- 3 v^{2}\end{matrix}\right|\\& =(2 u)\cdot (- 3 v^{2})-(1)\cdot (2)\\& =-6uv^{2}-2\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,1)} & =\left(- 2 \left(3 u v^{2} + 1\right)\right)\big|_{u=1,v=1}\\& =- 2 \left(3 (1) (1)^{2} + 1\right)\\& =-8\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-8|\cdot\delta A\\ & =8\,\delta A.\end{aligned}
$$

### easy / poly_sum / authored_area_poly_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u^{2} + v\\2 u - v^{3}\end{aligned}]?
$$

- $52\,\delta A$
- $13\,\delta A$
- $26\,\delta A$ **correct**
- $676\,\delta A$
- $\frac{1}{26}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}2 u&1\\2&- 3 v^{2}\end{matrix}\right|\\& =(2 u)\cdot (- 3 v^{2})-(1)\cdot (2)\\& =-6uv^{2}-2\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,1)} & =\left(- 2 \left(3 u v^{2} + 1\right)\right)\big|_{u=4,v=1}\\& =- 2 \left(3 (1)^{2} (4) + 1\right)\\& =-26\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-26|\cdot\delta A\\ & =26\,\delta A.\end{aligned}
$$

### easy / poly_sum / authored_determinant_poly_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u^{2} + v\\2 u - v^{3}\end{aligned}]?
$$

- $2\,\delta A$
- $8\,\delta A$ **correct**
- $6\,\delta A$
- $14\,\delta A$
- $4\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}2 u&1\\2&- 3 v^{2}\end{matrix}\right|\\& =(2 u)\cdot (- 3 v^{2})-(1)\cdot (2)\\& =-6uv^{2}-2\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,1)} & =\left(- 2 \left(3 u v^{2} + 1\right)\right)\big|_{u=1,v=1}\\& =- 2 \left(3 (1) (1)^{2} + 1\right)\\& =-8\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-8|\cdot\delta A\\ & =8\,\delta A.\end{aligned}
$$

### easy / poly_sum / authored_determinant_poly_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u^{2} + v\\2 u - v^{3}\end{aligned}]?
$$

- $2\,\delta A$
- $50\,\delta A$
- $26\,\delta A$ **correct**
- $22\,\delta A$
- $24\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}2 u&1\\2&- 3 v^{2}\end{matrix}\right|\\& =(2 u)\cdot (- 3 v^{2})-(1)\cdot (2)\\& =-6uv^{2}-2\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,1)} & =\left(- 2 \left(3 u v^{2} + 1\right)\right)\big|_{u=4,v=1}\\& =- 2 \left(3 (1)^{2} (4) + 1\right)\\& =-26\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-26|\cdot\delta A\\ & =26\,\delta A.\end{aligned}
$$

### easy / log_product / authored_area_log_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(2,8)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\log{\left(u v \right)}\\u v^{2}\end{aligned}]?
$$

- $16\,\delta A$
- $\frac{1}{8}\,\delta A$
- $8\,\delta A$ **correct**
- $4\,\delta A$
- $64\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{1}{u}&\frac{1}{v}\\v^{2}&2 u v\end{matrix}\right|\\& =(\frac{1}{u})\cdot (2 u v)-(\frac{1}{v})\cdot (v^{2})\\& =2v-v\\& =v\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(2,8)} & =\left(v\right)\big|_{u=2,v=8}\\& =8\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|8|\cdot\delta A\\ & =8\,\delta A.\end{aligned}
$$

### easy / log_product / authored_area_log_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(3,4)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\log{\left(u v \right)}\\u v^{2}\end{aligned}]?
$$

- $8\,\delta A$
- $\frac{1}{4}\,\delta A$
- $16\,\delta A$
- $2\,\delta A$
- $4\,\delta A$ **correct**

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{1}{u}&\frac{1}{v}\\v^{2}&2 u v\end{matrix}\right|\\& =(\frac{1}{u})\cdot (2 u v)-(\frac{1}{v})\cdot (v^{2})\\& =2v-v\\& =v\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(3,4)} & =\left(v\right)\big|_{u=3,v=4}\\& =4\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|4|\cdot\delta A\\ & =4\,\delta A.\end{aligned}
$$

### easy / exp_product / authored_area_exp_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-2,2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}v e^{u}\\u e^{v}\end{aligned}]?
$$

- $10\,\delta A$
- $5\,\delta A$ **correct**
- $\frac{1}{5}\,\delta A$
- $\frac{5}{2}\,\delta A$
- $25\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}v e^{u}&e^{u}\\e^{v}&u e^{v}\end{matrix}\right|\\& =(v e^{u})\cdot (u e^{v})-(e^{u})\cdot (e^{v})\\& =uv e^{u+v}-e^{u+v}\\& =(uv-1)e^{u+v}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-2,2)} & =\left(\left(u v - 1\right) e^{u} e^{v}\right)\big|_{u=-2,v=2}\\& =\left((-2) (2) - 1\right) e^{(-2)} e^{(2)}\\& =-5\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-5|\cdot\delta A\\ & =5\,\delta A.\end{aligned}
$$

### easy / exp_product / authored_area_exp_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,-4)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}v e^{u}\\u e^{v}\end{aligned}]?
$$

- $34\,\delta A$
- $\frac{17}{2}\,\delta A$
- $17\,\delta A$ **correct**
- $289\,\delta A$
- $\frac{1}{17}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}v e^{u}&e^{u}\\e^{v}&u e^{v}\end{matrix}\right|\\& =(v e^{u})\cdot (u e^{v})-(e^{u})\cdot (e^{v})\\& =uv e^{u+v}-e^{u+v}\\& =(uv-1)e^{u+v}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,-4)} & =\left(\left(u v - 1\right) e^{u} e^{v}\right)\big|_{u=4,v=-4}\\& =\left((-4) (4) - 1\right) e^{(-4)} e^{(4)}\\& =-17\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-17|\cdot\delta A\\ & =17\,\delta A.\end{aligned}
$$

### easy / exp_product / authored_determinant_exp_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-2,2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}v e^{u}\\u e^{v}\end{aligned}]?
$$

- $\delta A$
- $5\,\delta A$ **correct**
- $4\,\delta A$
- $9\,\delta A$
- $3\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}v e^{u}&e^{u}\\e^{v}&u e^{v}\end{matrix}\right|\\& =(v e^{u})\cdot (u e^{v})-(e^{u})\cdot (e^{v})\\& =uv e^{u+v}-e^{u+v}\\& =(uv-1)e^{u+v}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-2,2)} & =\left(\left(u v - 1\right) e^{u} e^{v}\right)\big|_{u=-2,v=2}\\& =\left((-2) (2) - 1\right) e^{(-2)} e^{(2)}\\& =-5\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-5|\cdot\delta A\\ & =5\,\delta A.\end{aligned}
$$

### easy / exp_product / authored_determinant_exp_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,-4)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}v e^{u}\\u e^{v}\end{aligned}]?
$$

- $\delta A$
- $33\,\delta A$
- $17\,\delta A$ **correct**
- $15\,\delta A$
- $16\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}v e^{u}&e^{u}\\e^{v}&u e^{v}\end{matrix}\right|\\& =(v e^{u})\cdot (u e^{v})-(e^{u})\cdot (e^{v})\\& =uv e^{u+v}-e^{u+v}\\& =(uv-1)e^{u+v}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,-4)} & =\left(\left(u v - 1\right) e^{u} e^{v}\right)\big|_{u=4,v=-4}\\& =\left((-4) (4) - 1\right) e^{(-4)} e^{(4)}\\& =-17\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-17|\cdot\delta A\\ & =17\,\delta A.\end{aligned}
$$

### easy / reciprocal_product / authored_area_reciprocal_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-2,-1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}- v + \frac{1}{u}\\u^{2} v\end{aligned}]?
$$

- $6\,\delta A$
- $3\,\delta A$ **correct**
- $\frac{1}{3}\,\delta A$
- $\frac{3}{2}\,\delta A$
- $9\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}- \frac{1}{u^{2}}&-1\\2 u v&u^{2}\end{matrix}\right|\\& =(- \frac{1}{u^{2}})\cdot (u^{2})-(-1)\cdot (2 u v)\\& =-1+2uv\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-2,-1)} & =\left(2 u v - 1\right)\big|_{u=-2,v=-1}\\& =2 (-1) (-2) - 1\\& =3\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|3|\cdot\delta A\\ & =3\,\delta A.\end{aligned}
$$

### easy / reciprocal_product / authored_area_reciprocal_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}- v + \frac{1}{u}\\u^{2} v\end{aligned}]?
$$

- $14\,\delta A$
- $\frac{7}{2}\,\delta A$
- $7\,\delta A$ **correct**
- $49\,\delta A$
- $\frac{1}{7}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}- \frac{1}{u^{2}}&-1\\2 u v&u^{2}\end{matrix}\right|\\& =(- \frac{1}{u^{2}})\cdot (u^{2})-(-1)\cdot (2 u v)\\& =-1+2uv\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,1)} & =\left(2 u v - 1\right)\big|_{u=4,v=1}\\& =2 (1) (4) - 1\\& =7\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|7|\cdot\delta A\\ & =7\,\delta A.\end{aligned}
$$

### easy / reciprocal_product / authored_determinant_reciprocal_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-2,-1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}- v + \frac{1}{u}\\u^{2} v\end{aligned}]?
$$

- $4\,\delta A$
- $3\,\delta A$ **correct**
- $\delta A$
- $2\,\delta A$
- $5\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}- \frac{1}{u^{2}}&-1\\2 u v&u^{2}\end{matrix}\right|\\& =(- \frac{1}{u^{2}})\cdot (u^{2})-(-1)\cdot (2 u v)\\& =-1+2uv\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-2,-1)} & =\left(2 u v - 1\right)\big|_{u=-2,v=-1}\\& =2 (-1) (-2) - 1\\& =3\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|3|\cdot\delta A\\ & =3\,\delta A.\end{aligned}
$$

### easy / reciprocal_product / authored_determinant_reciprocal_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}- v + \frac{1}{u}\\u^{2} v\end{aligned}]?
$$

- $8\,\delta A$
- $6\,\delta A$
- $7\,\delta A$ **correct**
- $9\,\delta A$
- $\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}- \frac{1}{u^{2}}&-1\\2 u v&u^{2}\end{matrix}\right|\\& =(- \frac{1}{u^{2}})\cdot (u^{2})-(-1)\cdot (2 u v)\\& =-1+2uv\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,1)} & =\left(2 u v - 1\right)\big|_{u=4,v=1}\\& =2 (1) (4) - 1\\& =7\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|7|\cdot\delta A\\ & =7\,\delta A.\end{aligned}
$$

### easy / sqrt_sum / authored_area_sqrt_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,-2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\sqrt{u} + v^{2}\\u v\end{aligned}]?
$$

- $\frac{15}{2}\,\delta A$ **correct**
- $15\,\delta A$
- $\frac{2}{15}\,\delta A$
- $\frac{225}{4}\,\delta A$
- $\frac{15}{4}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{1}{2 \sqrt{u}}&2 v\\v&u\end{matrix}\right|\\& =(\frac{1}{2 \sqrt{u}})\cdot (u)-(2 v)\cdot (v)\\& =\frac{1}{2}\sqrt{u}-2v^{2}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,-2)} & =\left(- \frac{- \sqrt{u} + 4 v^{2}}{2}\right)\big|_{u=1,v=-2}\\& =- \frac{4 (-2)^{2} - \sqrt{(1)}}{2}\\& =- \frac{15}{2}\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|- \frac{15}{2}|\cdot\delta A\\ & =\frac{15}{2}\,\delta A.\end{aligned}
$$

### easy / sqrt_sum / authored_area_sqrt_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,-3)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\sqrt{u} + v^{2}\\u v\end{aligned}]?
$$

- $\frac{35}{2}\,\delta A$ **correct**
- $35\,\delta A$
- $\frac{1225}{4}\,\delta A$
- $\frac{35}{4}\,\delta A$
- $\frac{2}{35}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{1}{2 \sqrt{u}}&2 v\\v&u\end{matrix}\right|\\& =(\frac{1}{2 \sqrt{u}})\cdot (u)-(2 v)\cdot (v)\\& =\frac{1}{2}\sqrt{u}-2v^{2}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,-3)} & =\left(- \frac{- \sqrt{u} + 4 v^{2}}{2}\right)\big|_{u=1,v=-3}\\& =- \frac{4 (-3)^{2} - \sqrt{(1)}}{2}\\& =- \frac{35}{2}\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|- \frac{35}{2}|\cdot\delta A\\ & =\frac{35}{2}\,\delta A.\end{aligned}
$$

### easy / sqrt_sum / authored_determinant_sqrt_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(9,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\sqrt{u} + v^{2}\\u v\end{aligned}]?
$$

- $2\,\delta A$
- $\frac{1}{2}\,\delta A$ **correct**
- $\frac{3}{2}\,\delta A$
- $\delta A$
- $\frac{7}{2}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{1}{2 \sqrt{u}}&2 v\\v&u\end{matrix}\right|\\& =(\frac{1}{2 \sqrt{u}})\cdot (u)-(2 v)\cdot (v)\\& =\frac{1}{2}\sqrt{u}-2v^{2}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(9,1)} & =\left(- \frac{- \sqrt{u} + 4 v^{2}}{2}\right)\big|_{u=9,v=1}\\& =- \frac{4 (1)^{2} - \sqrt{(9)}}{2}\\& =- \frac{1}{2}\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|- \frac{1}{2}|\cdot\delta A\\ & =\frac{1}{2}\,\delta A.\end{aligned}
$$

### easy / sqrt_sum / authored_determinant_sqrt_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,-3)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\sqrt{u} + v^{2}\\u v\end{aligned}]?
$$

- $\frac{35}{2}\,\delta A$ **correct**
- $18\,\delta A$
- $\frac{37}{2}\,\delta A$
- $17\,\delta A$
- $\frac{1}{2}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{1}{2 \sqrt{u}}&2 v\\v&u\end{matrix}\right|\\& =(\frac{1}{2 \sqrt{u}})\cdot (u)-(2 v)\cdot (v)\\& =\frac{1}{2}\sqrt{u}-2v^{2}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,-3)} & =\left(- \frac{- \sqrt{u} + 4 v^{2}}{2}\right)\big|_{u=1,v=-3}\\& =- \frac{4 (-3)^{2} - \sqrt{(1)}}{2}\\& =- \frac{35}{2}\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|- \frac{35}{2}|\cdot\delta A\\ & =\frac{35}{2}\,\delta A.\end{aligned}
$$

### easy / cos_sum / authored_area_cos_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(0,-2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}- v^{2} + \cos{\left(u \right)}\\u + v\end{aligned}]?
$$

- $2\,\delta A$
- $8\,\delta A$
- $\frac{1}{4}\,\delta A$
- $16\,\delta A$
- $4\,\delta A$ **correct**

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}- \sin{\left(u \right)}&- 2 v\\1&1\end{matrix}\right|\\& =(- \sin{\left(u \right)})\cdot (1)-(- 2 v)\cdot (1)\\& =-\sin u+2v\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(0,-2)} & =\left(2 v - \sin{\left(u \right)}\right)\big|_{u=0,v=-2}\\& =2 (-2) - \sin{\left((0) \right)}\\& =-4\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-4|\cdot\delta A\\ & =4\,\delta A.\end{aligned}
$$

### easy / cos_sum / authored_area_cos_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(0,-3)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}- v^{2} + \cos{\left(u \right)}\\u + v\end{aligned}]?
$$

- $6\,\delta A$ **correct**
- $12\,\delta A$
- $36\,\delta A$
- $3\,\delta A$
- $\frac{1}{6}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}- \sin{\left(u \right)}&- 2 v\\1&1\end{matrix}\right|\\& =(- \sin{\left(u \right)})\cdot (1)-(- 2 v)\cdot (1)\\& =-\sin u+2v\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(0,-3)} & =\left(2 v - \sin{\left(u \right)}\right)\big|_{u=0,v=-3}\\& =2 (-3) - \sin{\left((0) \right)}\\& =-6\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-6|\cdot\delta A\\ & =6\,\delta A.\end{aligned}
$$

### easy / quotient_product / authored_area_quotient_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\frac{u^{2}}{v}\\u v\end{aligned}]?
$$

- $6\,\delta A$
- $3\,\delta A$ **correct**
- $\frac{1}{3}\,\delta A$
- $\frac{3}{2}\,\delta A$
- $9\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{2 u}{v}&- \frac{u^{2}}{v^{2}}\\v&u\end{matrix}\right|\\& =(\frac{2 u}{v})\cdot (u)-(- \frac{u^{2}}{v^{2}})\cdot (v)\\& =\frac{2u^{2}}{v}+\frac{u^{2}}{v}\\& =\frac{3u^{2}}{v}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,1)} & =\left(\frac{3 u^{2}}{v}\right)\big|_{u=1,v=1}\\& =\frac{3 (1)^{2}}{(1)}\\& =3\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|3|\cdot\delta A\\ & =3\,\delta A.\end{aligned}
$$

### easy / quotient_product / authored_area_quotient_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\frac{u^{2}}{v}\\u v\end{aligned}]?
$$

- $96\,\delta A$
- $24\,\delta A$
- $48\,\delta A$ **correct**
- $2304\,\delta A$
- $\frac{1}{48}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{2 u}{v}&- \frac{u^{2}}{v^{2}}\\v&u\end{matrix}\right|\\& =(\frac{2 u}{v})\cdot (u)-(- \frac{u^{2}}{v^{2}})\cdot (v)\\& =\frac{2u^{2}}{v}+\frac{u^{2}}{v}\\& =\frac{3u^{2}}{v}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,1)} & =\left(\frac{3 u^{2}}{v}\right)\big|_{u=4,v=1}\\& =\frac{3 (4)^{2}}{(1)}\\& =48\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|48|\cdot\delta A\\ & =48\,\delta A.\end{aligned}
$$

### easy / sqrt_product / authored_area_sqrt_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(9,9)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\sqrt{u v}\\u v^{2}\end{aligned}]?
$$

- $81\,\delta A$
- $\frac{81}{2}\,\delta A$ **correct**
- $\frac{2}{81}\,\delta A$
- $\frac{81}{4}\,\delta A$
- $\frac{6561}{4}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{\sqrt{u v}}{2 u}&\frac{\sqrt{u v}}{2 v}\\v^{2}&2 u v\end{matrix}\right|\\& =(\frac{\sqrt{u v}}{2 u})\cdot (2 u v)-(\frac{\sqrt{u v}}{2 v})\cdot (v^{2})\\& =v\sqrt{uv}-\frac{1}{2}v\sqrt{uv}\\& =\frac{1}{2}v\sqrt{uv}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(9,9)} & =\left(\frac{v \sqrt{u v}}{2}\right)\big|_{u=9,v=9}\\& =\frac{(9) \sqrt{(9) (9)}}{2}\\& =\frac{81}{2}\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|\frac{81}{2}|\cdot\delta A\\ & =\frac{81}{2}\,\delta A.\end{aligned}
$$

### easy / sqrt_product / authored_area_sqrt_product

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,9)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\sqrt{u v}\\u v^{2}\end{aligned}]?
$$

- $27\,\delta A$ **correct**
- $54\,\delta A$
- $729\,\delta A$
- $\frac{27}{2}\,\delta A$
- $\frac{1}{27}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{\sqrt{u v}}{2 u}&\frac{\sqrt{u v}}{2 v}\\v^{2}&2 u v\end{matrix}\right|\\& =(\frac{\sqrt{u v}}{2 u})\cdot (2 u v)-(\frac{\sqrt{u v}}{2 v})\cdot (v^{2})\\& =v\sqrt{uv}-\frac{1}{2}v\sqrt{uv}\\& =\frac{1}{2}v\sqrt{uv}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,9)} & =\left(\frac{v \sqrt{u v}}{2}\right)\big|_{u=4,v=9}\\& =\frac{(9) \sqrt{(4) (9)}}{2}\\& =27\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|27|\cdot\delta A\\ & =27\,\delta A.\end{aligned}
$$

### easy / log_difference / authored_area_log_difference

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(3,2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\log{\left(u - v \right)}\\- u^{2} + v\end{aligned}]?
$$

- $10\,\delta A$
- $\frac{1}{5}\,\delta A$
- $5\,\delta A$ **correct**
- $\frac{5}{2}\,\delta A$
- $25\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{1}{u - v}&- \frac{1}{u - v}\\- 2 u&1\end{matrix}\right|\\& =(\frac{1}{u - v})\cdot (1)-(- \frac{1}{u - v})\cdot (- 2 u)\\& =\frac{1-2u}{u-v}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(3,2)} & =\left(- \frac{2 u - 1}{u - v}\right)\big|_{u=3,v=2}\\& =- \frac{2 (3) - 1}{- (2) + (3)}\\& =-5\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-5|\cdot\delta A\\ & =5\,\delta A.\end{aligned}
$$

### easy / log_difference / authored_area_log_difference

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,-2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\log{\left(u - v \right)}\\- u^{2} + v\end{aligned}]?
$$

- $\frac{7}{3}\,\delta A$
- $\frac{6}{7}\,\delta A$
- $\frac{49}{36}\,\delta A$
- $\frac{7}{12}\,\delta A$
- $\frac{7}{6}\,\delta A$ **correct**

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{1}{u - v}&- \frac{1}{u - v}\\- 2 u&1\end{matrix}\right|\\& =(\frac{1}{u - v})\cdot (1)-(- \frac{1}{u - v})\cdot (- 2 u)\\& =\frac{1-2u}{u-v}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,-2)} & =\left(- \frac{2 u - 1}{u - v}\right)\big|_{u=4,v=-2}\\& =- \frac{2 (4) - 1}{- (-2) + (4)}\\& =- \frac{7}{6}\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|- \frac{7}{6}|\cdot\delta A\\ & =\frac{7}{6}\,\delta A.\end{aligned}
$$

### easy / log_difference / authored_determinant_log_difference

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(3,2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\log{\left(u - v \right)}\\- u^{2} + v\end{aligned}]?
$$

- $6\,\delta A$
- $\delta A$
- $5\,\delta A$ **correct**
- $4\,\delta A$
- $7\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{1}{u - v}&- \frac{1}{u - v}\\- 2 u&1\end{matrix}\right|\\& =(\frac{1}{u - v})\cdot (1)-(- \frac{1}{u - v})\cdot (- 2 u)\\& =\frac{1-2u}{u-v}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(3,2)} & =\left(- \frac{2 u - 1}{u - v}\right)\big|_{u=3,v=2}\\& =- \frac{2 (3) - 1}{- (2) + (3)}\\& =-5\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-5|\cdot\delta A\\ & =5\,\delta A.\end{aligned}
$$

### easy / log_difference / authored_determinant_log_difference

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,-2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\log{\left(u - v \right)}\\- u^{2} + v\end{aligned}]?
$$

- $\frac{4}{3}\,\delta A$
- $\frac{1}{6}\,\delta A$
- $\frac{3}{2}\,\delta A$
- $\delta A$
- $\frac{7}{6}\,\delta A$ **correct**

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}\frac{1}{u - v}&- \frac{1}{u - v}\\- 2 u&1\end{matrix}\right|\\& =(\frac{1}{u - v})\cdot (1)-(- \frac{1}{u - v})\cdot (- 2 u)\\& =\frac{1-2u}{u-v}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,-2)} & =\left(- \frac{2 u - 1}{u - v}\right)\big|_{u=4,v=-2}\\& =- \frac{2 (4) - 1}{- (-2) + (4)}\\& =- \frac{7}{6}\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|- \frac{7}{6}|\cdot\delta A\\ & =\frac{7}{6}\,\delta A.\end{aligned}
$$

### easy / sin_sum / authored_area_sin_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,-1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u + v^{2}\\\sin{\left(u + v \right)}\end{aligned}]?
$$

- $6\,\delta A$
- $3\,\delta A$ **correct**
- $\frac{1}{3}\,\delta A$
- $\frac{3}{2}\,\delta A$
- $9\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}1&2 v\\\cos{\left(u + v \right)}&\cos{\left(u + v \right)}\end{matrix}\right|\\& =(1)\cdot (\cos{\left(u + v \right)})-(2 v)\cdot (\cos{\left(u + v \right)})\\& =(1-2v)\cos(u+v)\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,-1)} & =\left(- \left(2 v - 1\right) \cos{\left(u + v \right)}\right)\big|_{u=1,v=-1}\\& =- \left(2 (-1) - 1\right) \cos{\left((-1) + (1) \right)}\\& =3\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|3|\cdot\delta A\\ & =3\,\delta A.\end{aligned}
$$

### easy / sin_sum / authored_area_sin_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,-4)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u + v^{2}\\\sin{\left(u + v \right)}\end{aligned}]?
$$

- $18\,\delta A$
- $\frac{9}{2}\,\delta A$
- $9\,\delta A$ **correct**
- $81\,\delta A$
- $\frac{1}{9}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}1&2 v\\\cos{\left(u + v \right)}&\cos{\left(u + v \right)}\end{matrix}\right|\\& =(1)\cdot (\cos{\left(u + v \right)})-(2 v)\cdot (\cos{\left(u + v \right)})\\& =(1-2v)\cos(u+v)\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,-4)} & =\left(- \left(2 v - 1\right) \cos{\left(u + v \right)}\right)\big|_{u=4,v=-4}\\& =- \left(2 (-4) - 1\right) \cos{\left((-4) + (4) \right)}\\& =9\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|9|\cdot\delta A\\ & =9\,\delta A.\end{aligned}
$$

### easy / sin_sum / authored_determinant_sin_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-2,2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u + v^{2}\\\sin{\left(u + v \right)}\end{aligned}]?
$$

- $4\,\delta A$
- $3\,\delta A$ **correct**
- $\delta A$
- $2\,\delta A$
- $5\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}1&2 v\\\cos{\left(u + v \right)}&\cos{\left(u + v \right)}\end{matrix}\right|\\& =(1)\cdot (\cos{\left(u + v \right)})-(2 v)\cdot (\cos{\left(u + v \right)})\\& =(1-2v)\cos(u+v)\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-2,2)} & =\left(- \left(2 v - 1\right) \cos{\left(u + v \right)}\right)\big|_{u=-2,v=2}\\& =- \left(2 (2) - 1\right) \cos{\left((-2) + (2) \right)}\\& =-3\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-3|\cdot\delta A\\ & =3\,\delta A.\end{aligned}
$$

### easy / sin_sum / authored_determinant_sin_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,-4)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u + v^{2}\\\sin{\left(u + v \right)}\end{aligned}]?
$$

- $8\,\delta A$
- $10\,\delta A$
- $9\,\delta A$ **correct**
- $7\,\delta A$
- $\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}1&2 v\\\cos{\left(u + v \right)}&\cos{\left(u + v \right)}\end{matrix}\right|\\& =(1)\cdot (\cos{\left(u + v \right)})-(2 v)\cdot (\cos{\left(u + v \right)})\\& =(1-2v)\cos(u+v)\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,-4)} & =\left(- \left(2 v - 1\right) \cos{\left(u + v \right)}\right)\big|_{u=4,v=-4}\\& =- \left(2 (-4) - 1\right) \cos{\left((-4) + (4) \right)}\\& =9\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|9|\cdot\delta A\\ & =9\,\delta A.\end{aligned}
$$

### easy / exp_sum / authored_area_exp_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-2,2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}e^{u + v}\\u^{3} + v\end{aligned}]?
$$

- $22\,\delta A$
- $11\,\delta A$ **correct**
- $\frac{1}{11}\,\delta A$
- $\frac{11}{2}\,\delta A$
- $121\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}e^{u} e^{v}&e^{u} e^{v}\\3 u^{2}&1\end{matrix}\right|\\& =(e^{u} e^{v})\cdot (1)-(e^{u} e^{v})\cdot (3 u^{2})\\& =e^{u+v}(1-3u^{2})\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-2,2)} & =\left(- \left(3 u^{2} - 1\right) e^{u} e^{v}\right)\big|_{u=-2,v=2}\\& =- \left(3 (-2)^{2} - 1\right) e^{(-2)} e^{(2)}\\& =-11\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-11|\cdot\delta A\\ & =11\,\delta A.\end{aligned}
$$

### easy / exp_sum / authored_area_exp_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,-4)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}e^{u + v}\\u^{3} + v\end{aligned}]?
$$

- $94\,\delta A$
- $\frac{47}{2}\,\delta A$
- $47\,\delta A$ **correct**
- $2209\,\delta A$
- $\frac{1}{47}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}e^{u} e^{v}&e^{u} e^{v}\\3 u^{2}&1\end{matrix}\right|\\& =(e^{u} e^{v})\cdot (1)-(e^{u} e^{v})\cdot (3 u^{2})\\& =e^{u+v}(1-3u^{2})\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,-4)} & =\left(- \left(3 u^{2} - 1\right) e^{u} e^{v}\right)\big|_{u=4,v=-4}\\& =- \left(3 (4)^{2} - 1\right) e^{(-4)} e^{(4)}\\& =-47\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-47|\cdot\delta A\\ & =47\,\delta A.\end{aligned}
$$

### easy / exp_sum / authored_determinant_exp_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-2,2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}e^{u + v}\\u^{3} + v\end{aligned}]?
$$

- $12\,\delta A$
- $11\,\delta A$ **correct**
- $\delta A$
- $10\,\delta A$
- $13\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}e^{u} e^{v}&e^{u} e^{v}\\3 u^{2}&1\end{matrix}\right|\\& =(e^{u} e^{v})\cdot (1)-(e^{u} e^{v})\cdot (3 u^{2})\\& =e^{u+v}(1-3u^{2})\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-2,2)} & =\left(- \left(3 u^{2} - 1\right) e^{u} e^{v}\right)\big|_{u=-2,v=2}\\& =- \left(3 (-2)^{2} - 1\right) e^{(-2)} e^{(2)}\\& =-11\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-11|\cdot\delta A\\ & =11\,\delta A.\end{aligned}
$$

### easy / exp_sum / authored_determinant_exp_sum

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(4,-4)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}e^{u + v}\\u^{3} + v\end{aligned}]?
$$

- $48\,\delta A$
- $46\,\delta A$
- $47\,\delta A$ **correct**
- $49\,\delta A$
- $\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}e^{u} e^{v}&e^{u} e^{v}\\3 u^{2}&1\end{matrix}\right|\\& =(e^{u} e^{v})\cdot (1)-(e^{u} e^{v})\cdot (3 u^{2})\\& =e^{u+v}(1-3u^{2})\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(4,-4)} & =\left(- \left(3 u^{2} - 1\right) e^{u} e^{v}\right)\big|_{u=4,v=-4}\\& =- \left(3 (4)^{2} - 1\right) e^{(-4)} e^{(4)}\\& =-47\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-47|\cdot\delta A\\ & =47\,\delta A.\end{aligned}
$$

### moderate / canonical_monomial / authored_area_canonical_monomial

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(3,3)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u v^{2}\\3 u^{2} + v^{2}\end{aligned}]?
$$

- $540\,\delta A$
- $\frac{1}{270}\,\delta A$
- $270\,\delta A$ **correct**
- $135\,\delta A$
- $72900\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}v^{2}&2 u v\\6 u&2 v\end{matrix}\right|\\& =(v^{2})\cdot (2 v)-(2 u v)\cdot (6 u)\\& =- 12 u^{2} v + 2 v^{3}\\& =- 2 v \left(6 u^{2} - v^{2}\right)\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(3,3)} & =\left(- 2 v \left(6 u^{2} - v^{2}\right)\right)\big|_{u=3,v=3}\\& =- 2 (3) \left(- (3)^{2} + 6 (3)^{2}\right)\\& =-270\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-270|\cdot\delta A\\ & =270\,\delta A.\end{aligned}
$$

### moderate / canonical_monomial / authored_area_canonical_monomial

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-1,-2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u v^{3}\\u^{2} + 2 v^{2}\end{aligned}]?
$$

- $80\,\delta A$
- $40\,\delta A$ **correct**
- $1600\,\delta A$
- $20\,\delta A$
- $\frac{1}{40}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}v^{3}&3 u v^{2}\\2 u&4 v\end{matrix}\right|\\& =(v^{3})\cdot (4 v)-(3 u v^{2})\cdot (2 u)\\& =- 6 u^{2} v^{2} + 4 v^{4}\\& =- 2 v^{2} \left(3 u^{2} - 2 v^{2}\right)\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-1,-2)} & =\left(- 2 v^{2} \left(3 u^{2} - 2 v^{2}\right)\right)\big|_{u=-1,v=-2}\\& =- 2 (-2)^{2} \left(3 (-1)^{2} - 2 (-2)^{2}\right)\\& =40\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|40|\cdot\delta A\\ & =40\,\delta A.\end{aligned}
$$

### moderate / canonical_monomial / authored_determinant_canonical_monomial

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(3,3)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u v^{2}\\3 u^{2} + v^{2}\end{aligned}]?
$$

- $324\,\delta A$
- $54\,\delta A$
- $270\,\delta A$ **correct**
- $216\,\delta A$
- $378\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}v^{2}&2 u v\\6 u&2 v\end{matrix}\right|\\& =(v^{2})\cdot (2 v)-(2 u v)\cdot (6 u)\\& =- 12 u^{2} v + 2 v^{3}\\& =- 2 v \left(6 u^{2} - v^{2}\right)\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(3,3)} & =\left(- 2 v \left(6 u^{2} - v^{2}\right)\right)\big|_{u=3,v=3}\\& =- 2 (3) \left(- (3)^{2} + 6 (3)^{2}\right)\\& =-270\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-270|\cdot\delta A\\ & =270\,\delta A.\end{aligned}
$$

### moderate / canonical_monomial / authored_determinant_canonical_monomial

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-1,-2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u v^{3}\\u^{2} + 2 v^{2}\end{aligned}]?
$$

- $24\,\delta A$
- $40\,\delta A$ **correct**
- $88\,\delta A$
- $104\,\delta A$
- $64\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}v^{3}&3 u v^{2}\\2 u&4 v\end{matrix}\right|\\& =(v^{3})\cdot (4 v)-(3 u v^{2})\cdot (2 u)\\& =- 6 u^{2} v^{2} + 4 v^{4}\\& =- 2 v^{2} \left(3 u^{2} - 2 v^{2}\right)\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-1,-2)} & =\left(- 2 v^{2} \left(3 u^{2} - 2 v^{2}\right)\right)\big|_{u=-1,v=-2}\\& =- 2 (-2)^{2} \left(3 (-1)^{2} - 2 (-2)^{2}\right)\\& =40\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|40|\cdot\delta A\\ & =40\,\delta A.\end{aligned}
$$

### hard / powers / authored_area_powers

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-1,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}2 \left(2 u + v\right)^{3}\\2 \left(2 u - v\right)^{2}\end{aligned}]?
$$

- $288\,\delta A$ **correct**
- $144\,\delta A$
- $82944\,\delta A$
- $576\,\delta A$
- $\frac{1}{288}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}12 \left(2 u + v\right)^{2}&6 \left(2 u + v\right)^{2}\\8 \left(2 u - v\right)&- 4 \left(2 u - v\right)\end{matrix}\right|\\& =(12 \left(2 u + v\right)^{2})\cdot (- 4 \left(2 u - v\right))-(6 \left(2 u + v\right)^{2})\cdot (8 \left(2 u - v\right))\\& =- 768 u^{3} - 384 u^{2} v + 192 u v^{2} + 96 v^{3}\\& =- 96 \left(2 u - v\right) \left(2 u + v\right)^{2}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-1,1)} & =\left(- 96 \left(2 u - v\right) \left(2 u + v\right)^{2}\right)\big|_{u=-1,v=1}\\& =- 96 \left(2 (-1) - (1)\right) \left(2 (-1) + (1)\right)^{2}\\& =288\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|288|\cdot\delta A\\ & =288\,\delta A.\end{aligned}
$$

### hard / powers / authored_area_powers

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\left(u + v\right)^{2}\\2 \left(u - v\right)^{3}\end{aligned}]?
$$

- $72\,\delta A$ **correct**
- $\frac{1}{72}\,\delta A$
- $144\,\delta A$
- $36\,\delta A$
- $5184\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}2 \left(u + v\right)&2 \left(u + v\right)\\6 \left(u - v\right)^{2}&- 6 \left(u - v\right)^{2}\end{matrix}\right|\\& =(2 \left(u + v\right))\cdot (- 6 \left(u - v\right)^{2})-(2 \left(u + v\right))\cdot (6 \left(u - v\right)^{2})\\& =- 24 u^{3} + 24 u^{2} v + 24 u v^{2} - 24 v^{3}\\& =- 24 \left(u - v\right)^{2} \left(u + v\right)\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,2)} & =\left(- 24 \left(u - v\right)^{2} \left(u + v\right)\right)\big|_{u=1,v=2}\\& =- 24 \left((1) - (2)\right)^{2} \left((1) + (2)\right)\\& =-72\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-72|\cdot\delta A\\ & =72\,\delta A.\end{aligned}
$$

### hard / powers / authored_determinant_powers

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}2 \left(u + 2 v\right)^{2}\\\left(2 u - v\right)^{3}\end{aligned}]?
$$

- $216\,\delta A$
- $108\,\delta A$
- $180\,\delta A$ **correct**
- $36\,\delta A$
- $144\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}4 \left(u + 2 v\right)&8 \left(u + 2 v\right)\\6 \left(2 u - v\right)^{2}&- 3 \left(2 u - v\right)^{2}\end{matrix}\right|\\& =(4 \left(u + 2 v\right))\cdot (- 3 \left(2 u - v\right)^{2})-(8 \left(u + 2 v\right))\cdot (6 \left(2 u - v\right)^{2})\\& =- 240 u^{3} - 240 u^{2} v + 420 u v^{2} - 120 v^{3}\\& =- 60 \left(u + 2 v\right) \left(2 u - v\right)^{2}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,1)} & =\left(- 60 \left(u + 2 v\right) \left(2 u - v\right)^{2}\right)\big|_{u=1,v=1}\\& =- 60 \left(- (1) + 2 (1)\right)^{2} \left((1) + 2 (1)\right)\\& =-180\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-180|\cdot\delta A\\ & =180\,\delta A.\end{aligned}
$$

### hard / powers / authored_determinant_powers

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-1,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}2 \left(2 u + v\right)^{3}\\2 \left(u - 2 v\right)^{2}\end{aligned}]?
$$

- $288\,\delta A$
- $216\,\delta A$
- $360\,\delta A$ **correct**
- $72\,\delta A$
- $648\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}12 \left(2 u + v\right)^{2}&6 \left(2 u + v\right)^{2}\\4 \left(u - 2 v\right)&- 8 \left(u - 2 v\right)\end{matrix}\right|\\& =(12 \left(2 u + v\right)^{2})\cdot (- 8 \left(u - 2 v\right))-(6 \left(2 u + v\right)^{2})\cdot (4 \left(u - 2 v\right))\\& =- 480 u^{3} + 480 u^{2} v + 840 u v^{2} + 240 v^{3}\\& =- 120 \left(u - 2 v\right) \left(2 u + v\right)^{2}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-1,1)} & =\left(- 120 \left(u - 2 v\right) \left(2 u + v\right)^{2}\right)\big|_{u=-1,v=1}\\& =- 120 \left((-1) - 2 (1)\right) \left(2 (-1) + (1)\right)^{2}\\& =360\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|360|\cdot\delta A\\ & =360\,\delta A.\end{aligned}
$$

