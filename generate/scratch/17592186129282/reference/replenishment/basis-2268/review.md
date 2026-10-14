### moderate / canonical_monomial / authored_area_canonical_monomial

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-2,-1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}2 u v^{3}\\u^{2} + v^{2}\end{aligned}]?
$$

- $88\,\delta A$
- $22\,\delta A$
- $1936\,\delta A$
- $44\,\delta A$ **correct**
- $\frac{1}{44}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}2 v^{3}&6 u v^{2}\\2 u&2 v\end{matrix}\right|\\& =(2 v^{3})\cdot (2 v)-(6 u v^{2})\cdot (2 u)\\& =- 12 u^{2} v^{2} + 4 v^{4}\\& =- 4 v^{2} \left(3 u^{2} - v^{2}\right)\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-2,-1)} & =\left(- 4 v^{2} \left(3 u^{2} - v^{2}\right)\right)\big|_{u=-2,v=-1}\\& =- 4 (-1)^{2} \left(- (-1)^{2} + 3 (-2)^{2}\right)\\& =-44\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-44|\cdot\delta A\\ & =44\,\delta A.\end{aligned}
$$

### moderate / canonical_monomial / authored_area_canonical_monomial

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-1,2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}2 u v^{3}\\3 u^{2} + v^{2}\end{aligned}]?
$$

- $\frac{1}{80}\,\delta A$
- $40\,\delta A$
- $80\,\delta A$ **correct**
- $160\,\delta A$
- $6400\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}2 v^{3}&6 u v^{2}\\6 u&2 v\end{matrix}\right|\\& =(2 v^{3})\cdot (2 v)-(6 u v^{2})\cdot (6 u)\\& =- 36 u^{2} v^{2} + 4 v^{4}\\& =- 4 v^{2} \left(3 u - v\right) \left(3 u + v\right)\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-1,2)} & =\left(- 4 v^{2} \left(3 u - v\right) \left(3 u + v\right)\right)\big|_{u=-1,v=2}\\& =- 4 (2)^{2} \left(3 (-1) - (2)\right) \left(3 (-1) + (2)\right)\\& =-80\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-80|\cdot\delta A\\ & =80\,\delta A.\end{aligned}
$$

### moderate / canonical_monomial / authored_area_canonical_monomial

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(2,-1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}3 u v^{3}\\u^{2} + 2 v^{2}\end{aligned}]?
$$

- $\frac{1}{60}\,\delta A$
- $120\,\delta A$
- $60\,\delta A$ **correct**
- $3600\,\delta A$
- $30\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}3 v^{3}&9 u v^{2}\\2 u&4 v\end{matrix}\right|\\& =(3 v^{3})\cdot (4 v)-(9 u v^{2})\cdot (2 u)\\& =- 18 u^{2} v^{2} + 12 v^{4}\\& =- 6 v^{2} \left(3 u^{2} - 2 v^{2}\right)\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(2,-1)} & =\left(- 6 v^{2} \left(3 u^{2} - 2 v^{2}\right)\right)\big|_{u=2,v=-1}\\& =- 6 (-1)^{2} \left(- 2 (-1)^{2} + 3 (2)^{2}\right)\\& =-60\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-60|\cdot\delta A\\ & =60\,\delta A.\end{aligned}
$$

### moderate / canonical_monomial / authored_area_canonical_monomial

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(3,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}3 u v^{3}\\u^{2} + 2 v^{2}\end{aligned}]?
$$

- $75\,\delta A$
- $150\,\delta A$ **correct**
- $300\,\delta A$
- $22500\,\delta A$
- $\frac{1}{150}\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}3 v^{3}&9 u v^{2}\\2 u&4 v\end{matrix}\right|\\& =(3 v^{3})\cdot (4 v)-(9 u v^{2})\cdot (2 u)\\& =- 18 u^{2} v^{2} + 12 v^{4}\\& =- 6 v^{2} \left(3 u^{2} - 2 v^{2}\right)\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(3,1)} & =\left(- 6 v^{2} \left(3 u^{2} - 2 v^{2}\right)\right)\big|_{u=3,v=1}\\& =- 6 (1)^{2} \left(- 2 (1)^{2} + 3 (3)^{2}\right)\\& =-150\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-150|\cdot\delta A\\ & =150\,\delta A.\end{aligned}
$$

### moderate / canonical_monomial / authored_area_canonical_monomial

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-3,-1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}3 u v^{2}\\u^{2} + 2 v^{2}\end{aligned}]?
$$

- $192\,\delta A$
- $9216\,\delta A$
- $96\,\delta A$ **correct**
- $\frac{1}{96}\,\delta A$
- $48\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}3 v^{2}&6 u v\\2 u&4 v\end{matrix}\right|\\& =(3 v^{2})\cdot (4 v)-(6 u v)\cdot (2 u)\\& =- 12 u^{2} v + 12 v^{3}\\& =- 12 v \left(u - v\right) \left(u + v\right)\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-3,-1)} & =\left(- 12 v \left(u - v\right) \left(u + v\right)\right)\big|_{u=-3,v=-1}\\& =- 12 (-1) \left(- (-1) + (-3)\right) \left((-1) + (-3)\right)\\& =96\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|96|\cdot\delta A\\ & =96\,\delta A.\end{aligned}
$$

### hard / powers / authored_area_powers

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}2 \left(u + 2 v\right)^{2}\\\left(u - v\right)^{3}\end{aligned}]?
$$

- $360\,\delta A$
- $90\,\delta A$
- $\frac{1}{180}\,\delta A$
- $32400\,\delta A$
- $180\,\delta A$ **correct**

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}4 \left(u + 2 v\right)&8 \left(u + 2 v\right)\\3 \left(u - v\right)^{2}&- 3 \left(u - v\right)^{2}\end{matrix}\right|\\& =(4 \left(u + 2 v\right))\cdot (- 3 \left(u - v\right)^{2})-(8 \left(u + 2 v\right))\cdot (3 \left(u - v\right)^{2})\\& =- 36 u^{3} + 108 u v^{2} - 72 v^{3}\\& =- 36 \left(u - v\right)^{2} \left(u + 2 v\right)\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,2)} & =\left(- 36 \left(u - v\right)^{2} \left(u + 2 v\right)\right)\big|_{u=1,v=2}\\& =- 36 \left((1) - (2)\right)^{2} \left((1) + 2 (2)\right)\\& =-180\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-180|\cdot\delta A\\ & =180\,\delta A.\end{aligned}
$$

### hard / powers / authored_area_powers

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-2,-1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}2 \left(2 u + v\right)^{2}\\\left(u - v\right)^{3}\end{aligned}]?
$$

- $90\,\delta A$
- $32400\,\delta A$
- $\frac{1}{180}\,\delta A$
- $360\,\delta A$
- $180\,\delta A$ **correct**

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}8 \left(2 u + v\right)&4 \left(2 u + v\right)\\3 \left(u - v\right)^{2}&- 3 \left(u - v\right)^{2}\end{matrix}\right|\\& =(8 \left(2 u + v\right))\cdot (- 3 \left(u - v\right)^{2})-(4 \left(2 u + v\right))\cdot (3 \left(u - v\right)^{2})\\& =- 72 u^{3} + 108 u^{2} v - 36 v^{3}\\& =- 36 \left(u - v\right)^{2} \left(2 u + v\right)\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-2,-1)} & =\left(- 36 \left(u - v\right)^{2} \left(2 u + v\right)\right)\big|_{u=-2,v=-1}\\& =- 36 \left(- (-1) + (-2)\right)^{2} \left((-1) + 2 (-2)\right)\\& =180\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|180|\cdot\delta A\\ & =180\,\delta A.\end{aligned}
$$

### hard / powers / authored_area_powers

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(1,-1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}2 \left(2 u + v\right)^{2}\\\left(u - v\right)^{3}\end{aligned}]?
$$

- $288\,\delta A$
- $72\,\delta A$
- $20736\,\delta A$
- $\frac{1}{144}\,\delta A$
- $144\,\delta A$ **correct**

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}8 \left(2 u + v\right)&4 \left(2 u + v\right)\\3 \left(u - v\right)^{2}&- 3 \left(u - v\right)^{2}\end{matrix}\right|\\& =(8 \left(2 u + v\right))\cdot (- 3 \left(u - v\right)^{2})-(4 \left(2 u + v\right))\cdot (3 \left(u - v\right)^{2})\\& =- 72 u^{3} + 108 u^{2} v - 36 v^{3}\\& =- 36 \left(u - v\right)^{2} \left(2 u + v\right)\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(1,-1)} & =\left(- 36 \left(u - v\right)^{2} \left(2 u + v\right)\right)\big|_{u=1,v=-1}\\& =- 36 \left(- (-1) + (1)\right)^{2} \left((-1) + 2 (1)\right)\\& =-144\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|-144|\cdot\delta A\\ & =144\,\delta A.\end{aligned}
$$

### hard / powers / authored_area_powers

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-1,2)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}\left(u + 2 v\right)^{3}\\\left(u - v\right)^{2}\end{aligned}]?
$$

- $486\,\delta A$ **correct**
- $\frac{1}{486}\,\delta A$
- $243\,\delta A$
- $236196\,\delta A$
- $972\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}3 \left(u + 2 v\right)^{2}&6 \left(u + 2 v\right)^{2}\\2 \left(u - v\right)&- 2 \left(u - v\right)\end{matrix}\right|\\& =(3 \left(u + 2 v\right)^{2})\cdot (- 2 \left(u - v\right))-(6 \left(u + 2 v\right)^{2})\cdot (2 \left(u - v\right))\\& =- 18 u^{3} - 54 u^{2} v + 72 v^{3}\\& =- 18 \left(u - v\right) \left(u + 2 v\right)^{2}\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-1,2)} & =\left(- 18 \left(u - v\right) \left(u + 2 v\right)^{2}\right)\big|_{u=-1,v=2}\\& =- 18 \left((-1) - (2)\right) \left((-1) + 2 (2)\right)^{2}\\& =486\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|486|\cdot\delta A\\ & =486\,\delta A.\end{aligned}
$$

### hard / powers / authored_area_powers

Consider a small rectangle $Δ$ whose bottom-left corner is located at the point $(-2,1)$ with sides parallel to the coordinate axes in the $uv$-plane and whose area is $\delta A.$ Which of the following gives the best approximation for the area of the image of this rectangle under the action of the transformation $T,$ given by

$$
T:[\begin{aligned}u \\ v\end{aligned}]\longrightarrow[\begin{aligned}2 \left(u + v\right)^{3}\\\left(2 u - v\right)^{2}\end{aligned}]?
$$

- $180\,\delta A$ **correct**
- $32400\,\delta A$
- $360\,\delta A$
- $\frac{1}{180}\,\delta A$
- $90\,\delta A$

Recall that the absolute value of the Jacobian determinant gives the local area scale factor of the transformation at that point:

$$
\text{Area}(T(Δ))\approx\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\cdot\underbrace{\text{Area}(Δ)}_{\delta A}
$$

Computing the corresponding Jacobian determinant, we obtain the following:

$$
\begin{aligned}\frac{\partial(x,y)}{\partial(u,v)} & =\left|\begin{matrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{matrix}\right|\\& =\left|\begin{matrix}6 \left(u + v\right)^{2}&6 \left(u + v\right)^{2}\\4 \left(2 u - v\right)&- 2 \left(2 u - v\right)\end{matrix}\right|\\& =(6 \left(u + v\right)^{2})\cdot (- 2 \left(2 u - v\right))-(6 \left(u + v\right)^{2})\cdot (4 \left(2 u - v\right))\\& =- 72 u^{3} - 108 u^{2} v + 36 v^{3}\\& =- 36 \left(u + v\right)^{2} \left(2 u - v\right)\\\left.\frac{\partial(x,y)}{\partial(u,v)}\right|_{(-2,1)} & =\left(- 36 \left(u + v\right)^{2} \left(2 u - v\right)\right)\big|_{u=-2,v=1}\\& =- 36 \left((-2) + (1)\right)^{2} \left(2 (-2) - (1)\right)\\& =180\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\text{Area}(T(Δ)) & \approx|180|\cdot\delta A\\ & =180\,\delta A.\end{aligned}
$$
