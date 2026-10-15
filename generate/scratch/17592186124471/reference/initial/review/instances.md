### quadratic_affine / quadratic_affine_operations

Compute the rate of change of the function $f(x,y)=3 x^{2} - 3 y^{2}$ with respect to $t$ along the curve $r(t)=⟨- 3 t + 2,2 t - 1⟩$ at the point $t=-2.$

- $-144$
- $-204$
- $78$
- $-84$ **correct**
- $60$

The rate of change of $f(x,y)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(3 x^{2} - 3 y^{2}),\frac{∂}{∂y}(3 x^{2} - 3 y^{2})⟩ \\  & =⟨6 x,- 6 y⟩\end{aligned}
$$

Next, we substitute $x=- 3 t + 2$, $y=2 t - 1$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨6 \left(- 3 t + 2\right),- 6 \left(2 t - 1\right)⟩ \\  & =⟨- 18 t + 12,- 12 t + 6⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 3 t + 2),\frac{\text{d}}{\text{d}t}(2 t - 1)⟩ \\  & =⟨-3,2⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨- 18 t + 12,- 12 t + 6⟩\cdot ⟨-3,2⟩ \\  & =\left(- 18 t + 12\right)\cdot \left(-3\right)+\left(- 12 t + 6\right)\cdot \left(2\right) \\  & =30 t - 24.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=-2$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(-2))] & =30 (-2) - 24 \\  & =-84.\end{aligned}
$$

---

### quadratic_affine / quadratic_affine_operations

Compute the rate of change of the function $f(x,y)=- 3 x^{2} + 3 y^{2}$ with respect to $t$ along the curve $r(t)=⟨- t + 2,2 t⟩$ at the point $t=-1.$

- $-30$
- $18$
- $-24$
- $42$
- $-6$ **correct**

The rate of change of $f(x,y)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(- 3 x^{2} + 3 y^{2}),\frac{∂}{∂y}(- 3 x^{2} + 3 y^{2})⟩ \\  & =⟨- 6 x,6 y⟩\end{aligned}
$$

Next, we substitute $x=- t + 2$, $y=2 t$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨- 6 \left(- t + 2\right),6 \cdot 2 t⟩ \\  & =⟨6 t - 12,12 t⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- t + 2),\frac{\text{d}}{\text{d}t}(2 t)⟩ \\  & =⟨-1,2⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨6 t - 12,12 t⟩\cdot ⟨-1,2⟩ \\  & =\left(6 t - 12\right)\cdot \left(-1\right)+\left(12 t\right)\cdot \left(2\right) \\  & =18 t + 12.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=-1$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(-1))] & =18 (-1) + 12 \\  & =-6.\end{aligned}
$$

---

### quadratic_affine / quadratic_affine_operations

Compute the rate of change of the function $f(x,y)=- 3 x^{2} - 2 y^{2}$ with respect to $t$ along the curve $r(t)=⟨t - 2,3 t + 2⟩$ at the point $t=0.$

- $12$
- $4$
- $-12$ **correct**
- $-24$
- $36$

The rate of change of $f(x,y)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(- 3 x^{2} - 2 y^{2}),\frac{∂}{∂y}(- 3 x^{2} - 2 y^{2})⟩ \\  & =⟨- 6 x,- 4 y⟩\end{aligned}
$$

Next, we substitute $x=t - 2$, $y=3 t + 2$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨- 6 \left(t - 2\right),- 4 \left(3 t + 2\right)⟩ \\  & =⟨- 6 t + 12,- 12 t - 8⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t - 2),\frac{\text{d}}{\text{d}t}(3 t + 2)⟩ \\  & =⟨1,3⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨- 6 t + 12,- 12 t - 8⟩\cdot ⟨1,3⟩ \\  & =\left(- 6 t + 12\right)\cdot \left(1\right)+\left(- 12 t - 8\right)\cdot \left(3\right) \\  & =- 42 t - 12.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=0$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(0))] & =- 42 (0) - 12 \\  & =-12.\end{aligned}
$$

---

### quadratic_affine / quadratic_affine_operations

Compute the rate of change of the function $f(x,y)=x^{2} - y^{2}$ with respect to $t$ along the curve $r(t)=⟨- 3 t + 1,- t - 1⟩$ at the point $t=-2.$

- $-40$ **correct**
- $2$
- $12$
- $-42$
- $-44$

The rate of change of $f(x,y)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(x^{2} - y^{2}),\frac{∂}{∂y}(x^{2} - y^{2})⟩ \\  & =⟨2 x,- 2 y⟩\end{aligned}
$$

Next, we substitute $x=- 3 t + 1$, $y=- t - 1$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨2 \left(- 3 t + 1\right),- 2 \left(- t - 1\right)⟩ \\  & =⟨- 6 t + 2,2 t + 2⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 3 t + 1),\frac{\text{d}}{\text{d}t}(- t - 1)⟩ \\  & =⟨-3,-1⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨- 6 t + 2,2 t + 2⟩\cdot ⟨-3,-1⟩ \\  & =\left(- 6 t + 2\right)\cdot \left(-3\right)+\left(2 t + 2\right)\cdot \left(-1\right) \\  & =16 t - 8.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=-2$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(-2))] & =16 (-2) - 8 \\  & =-40.\end{aligned}
$$

---

### quadratic_affine / quadratic_affine_operations

Compute the rate of change of the function $f(x,y)=x^{2} - 2 y^{2}$ with respect to $t$ along the curve $r(t)=⟨t,- 3 t + 1⟩$ at the point $t=1.$

- $-24$
- $2$
- $26$
- $10$
- $-22$ **correct**

The rate of change of $f(x,y)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(x^{2} - 2 y^{2}),\frac{∂}{∂y}(x^{2} - 2 y^{2})⟩ \\  & =⟨2 x,- 4 y⟩\end{aligned}
$$

Next, we substitute $x=t$, $y=- 3 t + 1$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨2 t,- 4 \left(- 3 t + 1\right)⟩ \\  & =⟨2 t,12 t - 4⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t),\frac{\text{d}}{\text{d}t}(- 3 t + 1)⟩ \\  & =⟨1,-3⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨2 t,12 t - 4⟩\cdot ⟨1,-3⟩ \\  & =\left(2 t\right)\cdot \left(1\right)+\left(12 t - 4\right)\cdot \left(-3\right) \\  & =- 34 t + 12.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=1$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(1))] & =- 34 (1) + 12 \\  & =-22.\end{aligned}
$$

---

### radical_square / radical_square_operations

Compute the rate of change of the function $f(x,y,z)=3 x z^{2} - 3 y^{3}$ with respect to $t$ along the curve $r(t)=⟨- 3 t,3,\sqrt{t^{2} - 3}⟩$ at the point $t=2.$

- $-9$
- $-117$
- $-114$
- $-81$ **correct**
- $-72$

The rate of change of $f(x,y,z)$ with respect to $t$ along the curve $r(t)$ is given by $\frac{\text{d}}{\text{d}t}[f(r(t))].$ To calculate this, we can use the chain rule.

The chain rule in vector form states that

$$
\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).
$$

First, we need to compute $∇f(x,y,z):$

$$
\begin{aligned}∇f(x,y,z) & =⟨\frac{∂}{∂x}(3 x z^{2} - 3 y^{3}),\frac{∂}{∂y}(3 x z^{2} - 3 y^{3}),\frac{∂}{∂z}(3 x z^{2} - 3 y^{3})⟩ \\  & =⟨3 z^{2},- 9 y^{2},6 x z⟩\end{aligned}
$$

Next, we substitute $x=- 3 t$, $y=3$, $z=\sqrt{t^{2} - 3}$ into the above to find $∇f(r(t)):$

$$
\begin{aligned}∇f(r(t)) & =⟨3 \left(\sqrt{t^{2} - 3}\right)^{2},- 9 \cdot 3^{2},6 \left(- 3 t\right) \sqrt{t^{2} - 3}⟩ \\  & =⟨3 t^{2} - 9,-81,- 18 t \sqrt{t^{2} - 3}⟩\end{aligned}
$$

Now, we calculate the derivative of $r(t),$ which is

$$
\begin{aligned}{r}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 3 t),\frac{\text{d}}{\text{d}t}(3),\frac{\text{d}}{\text{d}t}(\sqrt{t^{2} - 3})⟩ \\  & =⟨-3,0,\frac{t}{\sqrt{t^{2} - 3}}⟩.\end{aligned}
$$

Applying the chain rule, we get

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(t))] & =∇f(r(t))\cdot {r}^{′}(t) \\  & =⟨3 t^{2} - 9,-81,- 18 t \sqrt{t^{2} - 3}⟩\cdot ⟨-3,0,\frac{t}{\sqrt{t^{2} - 3}}⟩ \\  & =\left(3 t^{2} - 9\right)\cdot \left(-3\right)+\left(-81\right)\cdot \left(0\right)+\left(- 18 t \sqrt{t^{2} - 3}\right)\cdot \left(\frac{t}{\sqrt{t^{2} - 3}}\right) \\  & =- 9 t^{2} + 27+0- 18 t^{2} \\  & =- 27 t^{2} + 27.\end{aligned}
$$

Therefore, the rate of change of $f$ along the curve $r(t)$ at $t=2$ is

$$
\begin{aligned}\frac{\text{d}}{\text{d}t}[f(r(2))] & =- 27 (2)^{2} + 27 \\  & =-9+0-72 \\  & =-81.\end{aligned}
$$