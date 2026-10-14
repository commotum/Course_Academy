Which of the following vector fields are conservative on $\mathbb R^{2}?$

Select all that apply.

- **I.** $F=(x e^{x y})\,i+(y e^{x y})\,j$
- **II.** $G=(4 x y + 2 y^{2})\,i+(4 x^{2} + 2 x y)\,j$
- **III.** $H=(\cos{\left(x - y \right)})\,i+(- \cos{\left(x - y \right)})\,j$

Let $F(x,y)=P(x,y)\,i+Q(x,y)\,j$ be a vector field with domain $D=\mathbb R^{2},$ where $P$ and $Q$ have continuous first-order partial derivatives everywhere on $D.$ Then, we have the following theorem:

$F$ *is conservative if and only if $\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}$ everywhere on $D.$*

Note that for each of our functions, $D=\mathbb R^{2}.$ With this in mind, let's check each of the vector fields.

- For the vector field $F,$ we have $P=x e^{x y}$ and $Q=y e^{x y}$. Computing the partial derivatives, we get

$$
\frac{\partial P}{\partial y}=x^{2} e^{x y},\qquad \frac{\partial Q}{\partial x}=y^{2} e^{x y}.
$$

Since the partial derivatives are not equal everywhere, we conclude that $F$ is not conservative on $\mathbb R^{2}.$

- For the vector field $G,$ we have $P=4 x y + 2 y^{2}$ and $Q=4 x^{2} + 2 x y$. Computing the partial derivatives, we get

$$
\frac{\partial P}{\partial y}=4 x + 4 y,\qquad \frac{\partial Q}{\partial x}=8 x + 2 y.
$$

Since the partial derivatives are not equal everywhere, we conclude that $G$ is not conservative on $\mathbb R^{2}.$

- For the vector field $H,$ we have $P=\cos{\left(x - y \right)}$ and $Q=- \cos{\left(x - y \right)}$. Computing the partial derivatives, we get

$$
\frac{\partial P}{\partial y}=\sin{\left(x - y \right)},\qquad \frac{\partial Q}{\partial x}=\sin{\left(x - y \right)}.
$$

Since the partial derivatives are continuous and equal everywhere on $\mathbb R^{2},$ we conclude that $H$ is conservative on $\mathbb R^{2}.$

Therefore, the correct answer is "III only."

---

Which of the following vector fields are conservative on $\mathbb R^{2}?$

Select all that apply.

- **I.** $F=(- x^{2} + 2 y)\,i+(- x^{2} + 2 y)\,j$
- **II.** $G=(4 y e^{2 x} + 4)\,i+(16 y + 2 e^{2 x})\,j$
- **III.** $H=(4 y)\,i+(4 x)\,j$

Let $F(x,y)=P(x,y)\,i+Q(x,y)\,j$ be a vector field with domain $D=\mathbb R^{2},$ where $P$ and $Q$ have continuous first-order partial derivatives everywhere on $D.$ Then, we have the following theorem:

$F$ *is conservative if and only if $\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}$ everywhere on $D.$*

Note that for each of our functions, $D=\mathbb R^{2}.$ With this in mind, let's check each of the vector fields.

- For the vector field $F,$ we have $P=- x^{2} + 2 y$ and $Q=- x^{2} + 2 y$. Computing the partial derivatives, we get

$$
\frac{\partial P}{\partial y}=2,\qquad \frac{\partial Q}{\partial x}=- 2 x.
$$

Since the partial derivatives are not equal everywhere, we conclude that $F$ is not conservative on $\mathbb R^{2}.$

- For the vector field $G,$ we have $P=4 y e^{2 x} + 4$ and $Q=16 y + 2 e^{2 x}$. Computing the partial derivatives, we get

$$
\frac{\partial P}{\partial y}=4 e^{2 x},\qquad \frac{\partial Q}{\partial x}=4 e^{2 x}.
$$

Since the partial derivatives are continuous and equal everywhere on $\mathbb R^{2},$ we conclude that $G$ is conservative on $\mathbb R^{2}.$

- For the vector field $H,$ we have $P=4 y$ and $Q=4 x$. Computing the partial derivatives, we get

$$
\frac{\partial P}{\partial y}=4,\qquad \frac{\partial Q}{\partial x}=4.
$$

Since the partial derivatives are continuous and equal everywhere on $\mathbb R^{2},$ we conclude that $H$ is conservative on $\mathbb R^{2}.$

Therefore, the correct answer is "II and III only."
