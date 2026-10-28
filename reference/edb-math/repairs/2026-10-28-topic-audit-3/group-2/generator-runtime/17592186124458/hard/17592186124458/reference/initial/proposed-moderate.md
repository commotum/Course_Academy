Find the directional derivative of the function $f(x,y)=4 x^{2} y + 2 x e^{y}$ at the point $A(2,0)$ in the direction towards the point $B(4,1).$

- $- \frac{16 \sqrt{5}}{5}$
- $\frac{24 \sqrt{5}}{5}$
- $24$
- $\frac{4 \sqrt{5}}{5}$
- $\frac{24}{5}$

The directional derivative ${f}_{u}^{′}(a,b)$ of a function $f(x,y)$ at the point $(a,b)$ in the direction of the vector $v$ is given by

$$
{f}_{u}^{′}(a,b)=∇f(a,b)\cdot u
$$

where $u$ is a unit vector in the direction of $v.$

First, we find the direction vector and the corresponding unit vector:

$$
\begin{aligned}\overset{\to }{AB} & =⟨4,1⟩-⟨2,0⟩ \\  & =⟨2,1⟩ \\ u & =\frac{\overset{\to }{AB}}{‖\overset{\to }{AB}‖} \\  & =\frac{1}{\sqrt{(2)^{2}+(1)^{2}}}⟨2,1⟩ \\  & =\frac{1}{\sqrt{5}}⟨2,1⟩\end{aligned}
$$

Now, we calculate the gradient $∇f(x,y)$ and evaluate it at the point $A(2,0):$

$$
\begin{aligned}∇f(x,y) & =⟨\frac{∂}{∂x}(4 x^{2} y + 2 x e^{y}),\frac{∂}{∂y}(4 x^{2} y + 2 x e^{y})⟩ \\  & =⟨8 x y + 2 e^{y},2 x \left(2 x + e^{y}\right)⟩ \\ ∇f(2,0) & =⟨8 (2) (0) + 2 e^{(0)},4 (2)^{2} + 2 (2) e^{(0)}⟩ \\  & =⟨2,20⟩\end{aligned}
$$

Therefore, the directional derivative is:

$$
\begin{aligned}{f}_{u}^{′}(2,0) & =∇f(2,0)\cdot u \\  & =⟨2,20⟩\cdot ⟨\frac{2 \sqrt{5}}{5},\frac{\sqrt{5}}{5}⟩ \\  & =\frac{24 \sqrt{5}}{5}.\end{aligned}
$$