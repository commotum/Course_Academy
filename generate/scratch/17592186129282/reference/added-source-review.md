# Added source and replay



Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(3,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:\begin{bmatrix}u \\ v\end{bmatrix}⟶\begin{bmatrix}{u}^{3}-v \\ v-u\end{bmatrix}?
$$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))≈|\frac{∂(x,y)}{∂(u,v)}|\cdot {{\text{Area}(Δ)}_{⏟}}_{\delta A}
$$

 

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{∂(x,y)}{∂(u,v)} & =|\begin{aligned}\frac{∂x}{∂u} & \frac{∂x}{∂v} \\ \frac{∂y}{∂u} & \frac{∂y}{∂v}\end{aligned}| \\  & =|\begin{aligned}3{u}^{2} & -1 \\ -1 & 1\end{aligned}| \\  & =3{u}^{2}\cdot 1-(-1)\cdot (-1) \\  & =3{u}^{2}-1 \\ {\frac{∂(x,y)}{∂(u,v)}|}_{(3,1)} & =(3{u}^{2}-1)\,{|}_{u=3\,v=1} \\  & =3(3)^{2}-1 \\  & =26\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & ≈|26|\cdot \delta A \\  & =26\,\delta A.\end{aligned}
$$

## Complete source bank



8\,\delta A

5\,\delta A

18\,\delta A

13\,\delta A

26\,\delta A



## Generated source replay



### easy / cubic_difference / observed_cubic_difference

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(3,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u^{3} - v\\- u + v\end{aligned}]?
$$

- $18\,\delta A$
- $5\,\delta A$
- $8\,\delta A$
- $26\,\delta A$ **correct**
- $13\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}3 u^{2}&-1\\-1&1\end{matrix}\right|\\& =(3 u^{2})\cdot (1)-(-1)\cdot (-1)\\& =3u^{2}-1\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(3,1)} & =\left(3 u^{2} - 1\right)\big|_{u=3,v=1}\\& =3 (3)^{2} - 1\\& =26\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|26|\cdot\delta A\\ & =26\,\delta A.\end{aligned}
$$



## Changed parameter samples



### easy / cubic_difference / authored_area_cubic_difference

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-3,-2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u^{3} - v\\- u + v\end{aligned}]?
$$

- $26\,\delta A$ **correct**
- $\frac{1}{26}\,\delta A$
- $13\,\delta A$
- $52\,\delta A$
- $676\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}3 u^{2}&-1\\-1&1\end{matrix}\right|\\& =(3 u^{2})\cdot (1)-(-1)\cdot (-1)\\& =3u^{2}-1\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-3,-2)} & =\left(3 u^{2} - 1\right)\big|_{u=-3,v=-2}\\& =3 (-3)^{2} - 1\\& =26\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|26|\cdot\delta A\\ & =26\,\delta A.\end{aligned}
$$

### easy / cubic_difference / authored_area_cubic_difference

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(3,5)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}u^{3} - v\\- u + v\end{aligned}]?
$$

- $676\,\delta A$
- $26\,\delta A$ **correct**
- $52\,\delta A$
- $\frac{1}{26}\,\delta A$
- $13\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}3 u^{2}&-1\\-1&1\end{matrix}\right|\\& =(3 u^{2})\cdot (1)-(-1)\cdot (-1)\\& =3u^{2}-1\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(3,5)} & =\left(3 u^{2} - 1\right)\big|_{u=3,v=5}\\& =3 (3)^{2} - 1\\& =26\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|26|\cdot\delta A\\ & =26\,\delta A.\end{aligned}
$$
