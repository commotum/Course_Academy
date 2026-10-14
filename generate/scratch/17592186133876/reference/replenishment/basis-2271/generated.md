### log_difference — observed; authored default bank/standalone presentation

Consider the vector field $F=\left(2 \ln{\left(x + y \right)}\right)\,i+\left(3 \ln{\left(x - y \right)}\right)\,j.$ 
Evaluate $\nabla\cdot F$ at the point $(3,1).$

- $-1$ **correct**
- $- \frac{1}{2}$
- $\frac{1}{2}$
- $2$
- $1$

If $F=P\,i+Q\,j$ is a vector field on ${R}^{2}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=\nabla\cdot F=\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}.
$$

When differentiating $P$ with respect to $x$, hold $y$ constant; when differentiating $Q$ with respect to $y$, hold $x$ constant.

Therefore, we have

$$
\begin{aligned}\nabla\cdot F & =\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y} \\  & =\frac{\partial}{\partial x}(2 \ln{\left(x + y \right)})+\frac{\partial}{\partial y}(3 \ln{\left(x - y \right)}) \\  & =\frac{2}{x + y}+\left(- \frac{3}{x - y}\right) \\  & =- \frac{x + 5 y}{\left(x - y\right) \left(x + y\right)}.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(3,1),$ and obtain

$$
\begin{aligned}(\nabla\cdot F)(3,1) & =- \frac{5 (1) + (3)}{\left(- (1) + (3)\right) \left((1) + (3)\right)} \\ & =\frac{1}{2}+\left(- \frac{3}{2}\right) \\ & =-1.\end{aligned}
$$

---

### affine_squares — authored missing level; authored default bank/standalone presentation

Consider the vector field $F=\left(\left(3 x + 2 y\right)^{2}\right)\,i+\left(\left(2 x + 3 y\right)^{2}\right)\,j.$ 
Evaluate $\nabla\cdot F$ at the point $(2,1).$

- $90$ **correct**
- $138$
- $48$
- $6$
- $-90$

If $F=P\,i+Q\,j$ is a vector field on ${R}^{2}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=\nabla\cdot F=\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}.
$$

When differentiating $P$ with respect to $x$, hold $y$ constant; when differentiating $Q$ with respect to $y$, hold $x$ constant.

Therefore, we have

$$
\begin{aligned}\nabla\cdot F & =\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y} \\  & =\frac{\partial}{\partial x}(\left(3 x + 2 y\right)^{2})+\frac{\partial}{\partial y}(\left(2 x + 3 y\right)^{2}) \\  & =18 x + 12 y+\left(12 x + 18 y\right) \\  & =30 \left(x + y\right).\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(2,1),$ and obtain

$$
\begin{aligned}(\nabla\cdot F)(2,1) & =30 (1) + 30 (2) \\ & =48+\left(42\right) \\ & =90.\end{aligned}
$$

---

### affine_squares — authored missing level; authored default bank/standalone presentation

Consider the vector field $F=\left(\left(4 x + y\right)^{2}\right)\,i+\left(\left(3 x + 4 y\right)^{2}\right)\,j.$ 
Evaluate $\nabla\cdot F$ at the point $(2,1).$

- $-8$
- $152$ **correct**
- $72$
- $-152$
- $224$

If $F=P\,i+Q\,j$ is a vector field on ${R}^{2}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=\nabla\cdot F=\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}.
$$

When differentiating $P$ with respect to $x$, hold $y$ constant; when differentiating $Q$ with respect to $y$, hold $x$ constant.

Therefore, we have

$$
\begin{aligned}\nabla\cdot F & =\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y} \\  & =\frac{\partial}{\partial x}(\left(4 x + y\right)^{2})+\frac{\partial}{\partial y}(\left(3 x + 4 y\right)^{2}) \\  & =32 x + 8 y+\left(24 x + 32 y\right) \\  & =8 \left(7 x + 5 y\right).\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(2,1),$ and obtain

$$
\begin{aligned}(\nabla\cdot F)(2,1) & =40 (1) + 56 (2) \\ & =72+\left(80\right) \\ & =152.\end{aligned}
$$

---

### affine_log_exp — authored missing level; authored default bank/standalone presentation

Consider the vector field $F=\left(\ln{\left(3 x + y \right)}\right)\,i+\left(3 x^{2} e^{3 y}\right)\,j.$ 
Evaluate $\nabla\cdot F$ at the point $(2,0).$

- $- \frac{73}{2}$
- $\frac{1}{2}$
- $\frac{73}{2}$ **correct**
- $- \frac{71}{2}$
- $37$

If $F=P\,i+Q\,j$ is a vector field on ${R}^{2}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=\nabla\cdot F=\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}.
$$

When differentiating $P$ with respect to $x$, hold $y$ constant; when differentiating $Q$ with respect to $y$, hold $x$ constant.

Therefore, we have

$$
\begin{aligned}\nabla\cdot F & =\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y} \\  & =\frac{\partial}{\partial x}(\ln{\left(3 x + y \right)})+\frac{\partial}{\partial y}(3 x^{2} e^{3 y}) \\  & =\frac{3}{3 x + y}+\left(9 x^{2} e^{3 y}\right) \\  & =\frac{3 \left(9 x^{3} e^{3 y} + 3 x^{2} y e^{3 y} + 1\right)}{3 x + y}.\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(2,0),$ and obtain

$$
\begin{aligned}(\nabla\cdot F)(2,0) & =\frac{3 \left(3 (0) (2)^{2} e^{3 (0)} + 9 (2)^{3} e^{3 (0)} + 1\right)}{(0) + 3 (2)} \\ & =\frac{1}{2}+\left(36\right) \\ & =\frac{73}{2}.\end{aligned}
$$

---

### affine_squares — authored missing level; authored default bank/standalone presentation

Consider the vector field $F=\left(\left(3 x + 4 y\right)^{2}\right)\,i+\left(\left(4 x + 3 y\right)^{2}\right)\,j.$ 
Evaluate $\nabla\cdot F$ at the point $(2,1).$

- $126$ **correct**
- $-126$
- $186$
- $-6$
- $60$

If $F=P\,i+Q\,j$ is a vector field on ${R}^{2}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=\nabla\cdot F=\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}.
$$

When differentiating $P$ with respect to $x$, hold $y$ constant; when differentiating $Q$ with respect to $y$, hold $x$ constant.

Therefore, we have

$$
\begin{aligned}\nabla\cdot F & =\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y} \\  & =\frac{\partial}{\partial x}(\left(3 x + 4 y\right)^{2})+\frac{\partial}{\partial y}(\left(4 x + 3 y\right)^{2}) \\  & =18 x + 24 y+\left(24 x + 18 y\right) \\  & =42 \left(x + y\right).\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(2,1),$ and obtain

$$
\begin{aligned}(\nabla\cdot F)(2,1) & =42 (1) + 42 (2) \\ & =60+\left(66\right) \\ & =126.\end{aligned}
$$

---

### affine_squares — authored missing level; authored default bank/standalone presentation

Consider the vector field $F=\left(\left(3 x + 2 y\right)^{2}\right)\,i+\left(\left(3 x + 4 y\right)^{2}\right)\,j.$ 
Evaluate $\nabla\cdot F$ at the point $(2,1).$

- $176$
- $-32$
- $48$
- $128$ **correct**
- $-128$

If $F=P\,i+Q\,j$ is a vector field on ${R}^{2}$ and the partial derivatives of the components of $F$ all exist, then the divergence of $F$ is the scalar field given by

$$
\text{div}\,F=\nabla\cdot F=\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}.
$$

When differentiating $P$ with respect to $x$, hold $y$ constant; when differentiating $Q$ with respect to $y$, hold $x$ constant.

Therefore, we have

$$
\begin{aligned}\nabla\cdot F & =\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y} \\  & =\frac{\partial}{\partial x}(\left(3 x + 2 y\right)^{2})+\frac{\partial}{\partial y}(\left(3 x + 4 y\right)^{2}) \\  & =18 x + 12 y+\left(24 x + 32 y\right) \\  & =2 \left(21 x + 22 y\right).\end{aligned}
$$

Finally, we evaluate $\text{div}\,F$ at the point $(2,1),$ and obtain

$$
\begin{aligned}(\nabla\cdot F)(2,1) & =44 (1) + 42 (2) \\ & =48+\left(80\right) \\ & =128.\end{aligned}
$$
