## q-33143 — moderate
Profile: `authored-operations`; parameters: `{"scales": [1, -3, -2]}`.

Find the value of $(3h(t) - 2g(t))^{′}$ at $t = 2$, if
$h(t)= ⟨2 t^{2},\,9 - 3 t,\,- 2 t^{3} - 16⟩; g(t)= ⟨t \left(t + 2\right),\,-24,\,- 4 t^{3}⟩$

- $⟨-36,\,9,\,168⟩$
- $⟨-12,\,0,\,96⟩$
- $⟨8,\,57,\,-32⟩$
- $⟨12,\,-9,\,24⟩$ **correct**
- $⟨24,\,-9,\,-72⟩$

Using the constant multiple rule and the sum rule, we have

$$
(3h(t)-2g(t))'=3h'(\!t)-2g'(\!t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}h'(t)&=⟨\frac{\text{d}}{\text{d}t}(2 t^{2}),\,\frac{\text{d}}{\text{d}t}(9 - 3 t),\,\frac{\text{d}}{\text{d}t}(- 2 t^{3} - 16)⟩ \\ &=⟨4 t,\,-3,\,- 6 t^{2}⟩ \\ g'(t)&=⟨\frac{\text{d}}{\text{d}t}(t \left(t + 2\right)),\,\frac{\text{d}}{\text{d}t}(-24),\,\frac{\text{d}}{\text{d}t}(- 4 t^{3})⟩ \\ &=⟨2 t + 2,\,0,\,- 12 t^{2}⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(3h(t)-2g(t))'\big|_{t=2}&=3h'(\!2)-2g'(\!2) \\ &=3\left(⟨8,\,-3,\,-24⟩\right)-2\left(⟨6,\,0,\,-48⟩\right) \\ &=\left(⟨24,\,-9,\,-72⟩\right)+\left(⟨-12,\,0,\,96⟩\right) \\ &=⟨12,\,-9,\,24⟩.\end{aligned}
$$

---

## q-33143 — moderate
Profile: `authored-operations`; parameters: `{"scales": [3, -1, 3]}`.

Find the value of $(3h(t) - 2g(t))^{′}$ at $t = 2$, if
$h(t)= ⟨6 t^{2},\,3 - t,\,3 t^{3} + 24⟩; g(t)= ⟨3 t \left(t + 2\right),\,-8,\,6 t^{3}⟩$

- $⟨36,\,-3,\,-36⟩$ **correct**
- $⟨72,\,-3,\,108⟩$
- $⟨24,\,19,\,48⟩$
- $⟨-36,\,0,\,-144⟩$
- $⟨-108,\,3,\,-252⟩$

Using the constant multiple rule and the sum rule, we have

$$
(3h(t)-2g(t))'=3h'(\!t)-2g'(\!t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}h'(t)&=⟨\frac{\text{d}}{\text{d}t}(6 t^{2}),\,\frac{\text{d}}{\text{d}t}(3 - t),\,\frac{\text{d}}{\text{d}t}(3 t^{3} + 24)⟩ \\ &=⟨12 t,\,-1,\,9 t^{2}⟩ \\ g'(t)&=⟨\frac{\text{d}}{\text{d}t}(3 t \left(t + 2\right)),\,\frac{\text{d}}{\text{d}t}(-8),\,\frac{\text{d}}{\text{d}t}(6 t^{3})⟩ \\ &=⟨6 t + 6,\,0,\,18 t^{2}⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(3h(t)-2g(t))'\big|_{t=2}&=3h'(\!2)-2g'(\!2) \\ &=3\left(⟨24,\,-1,\,36⟩\right)-2\left(⟨18,\,0,\,72⟩\right) \\ &=\left(⟨72,\,-3,\,108⟩\right)+\left(⟨-36,\,0,\,-144⟩\right) \\ &=⟨36,\,-3,\,-36⟩.\end{aligned}
$$

---

## canonical-mixed — hard
Profile: `authored-operations`; parameters: `{"a": 4, "b": 1, "A": -2, "B": 2, "n": 2, "h": 3, "u": 3, "v": 4}`.

Find the derivative of $-2f(t)+2g(t)$ with respect to $t$, where

$$
\begin{aligned}f(t)&=(4 t^{2} + 1)\,i- \frac{4}{t - 3}\,j+\cos{\left(3 t \right)}\,k \\ g(t)&=(t - 4)\,i+e^{4 t}\,j+\cos{\left(3 t \right)}\,k\end{aligned}
$$

- $- 16 t\,i- \frac{8}{\left(t - 3\right)^{2}}\,j+6 \sin{\left(3 t \right)}\,k$
- $(2 - 16 t)\,i+(8 e^{4 t} - \frac{8}{\left(t - 3\right)^{2}})\,j$ **correct**
- $(16 t + 2)\,i+(8 e^{4 t} + \frac{8}{\left(t - 3\right)^{2}})\,j- 12 \sin{\left(3 t \right)}\,k$
- $2\,i+8 e^{4 t}\,j- 6 \sin{\left(3 t \right)}\,k$
- $(- 8 t^{2} + 2 t - 10)\,i+\frac{2 \left(\left(t - 3\right) e^{4 t} + 4\right)}{t - 3}\,j$

Using the constant multiple rule and the sum rule, we have

$$
(-2f(t)+2g(t))'=-2f'(\!t)+2g'(\!t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}f'(t)&=⟨\frac{\text{d}}{\text{d}t}(4 t^{2} + 1),\,\frac{\text{d}}{\text{d}t}(- \frac{4}{t - 3}),\,\frac{\text{d}}{\text{d}t}(\cos{\left(3 t \right)})⟩ \\ &=8 t\,i+\frac{4}{\left(t - 3\right)^{2}}\,j- 3 \sin{\left(3 t \right)}\,k \\ g'(t)&=⟨\frac{\text{d}}{\text{d}t}(t - 4),\,\frac{\text{d}}{\text{d}t}(e^{4 t}),\,\frac{\text{d}}{\text{d}t}(\cos{\left(3 t \right)})⟩ \\ &=1\,i+4 e^{4 t}\,j- 3 \sin{\left(3 t \right)}\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(-2f(t)+2g(t))'&=-2f'(\!t)+2g'(\!t) \\ &=-2\left(8 t\,i+\frac{4}{\left(t - 3\right)^{2}}\,j- 3 \sin{\left(3 t \right)}\,k\right)+2\left(1\,i+4 e^{4 t}\,j- 3 \sin{\left(3 t \right)}\,k\right) \\ &=\left(- 16 t\,i- \frac{8}{\left(t - 3\right)^{2}}\,j+6 \sin{\left(3 t \right)}\,k\right)+\left(2\,i+8 e^{4 t}\,j- 6 \sin{\left(3 t \right)}\,k\right) \\ &=(2 - 16 t)\,i+(8 e^{4 t} - \frac{8}{\left(t - 3\right)^{2}})\,j.\end{aligned}
$$

---

## canonical-mixed — hard
Profile: `authored-operations`; parameters: `{"a": 3, "b": 4, "A": -2, "B": 2, "n": 3, "h": -3, "u": 4, "v": 2}`.

Find the derivative of $-2f(t)+2g(t)$ with respect to $t$, where

$$
\begin{aligned}f(t)&=(3 t^{3} + 4)\,i- \frac{3}{t + 3}\,j+\cos{\left(4 t \right)}\,k \\ g(t)&=(4 t - 3)\,i+e^{2 t}\,j+\cos{\left(4 t \right)}\,k\end{aligned}
$$

- $(8 - 18 t^{2})\,i+(4 e^{2 t} - \frac{6}{\left(t + 3\right)^{2}})\,j$ **correct**
- $- 18 t^{2}\,i- \frac{6}{\left(t + 3\right)^{2}}\,j+8 \sin{\left(4 t \right)}\,k$
- $8\,i+4 e^{2 t}\,j- 8 \sin{\left(4 t \right)}\,k$
- $(18 t^{2} + 8)\,i+(4 e^{2 t} + \frac{6}{\left(t + 3\right)^{2}})\,j- 16 \sin{\left(4 t \right)}\,k$
- $(- 6 t^{3} + 8 t - 14)\,i+\frac{2 \left(\left(t + 3\right) e^{2 t} + 3\right)}{t + 3}\,j$

Using the constant multiple rule and the sum rule, we have

$$
(-2f(t)+2g(t))'=-2f'(\!t)+2g'(\!t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}f'(t)&=⟨\frac{\text{d}}{\text{d}t}(3 t^{3} + 4),\,\frac{\text{d}}{\text{d}t}(- \frac{3}{t + 3}),\,\frac{\text{d}}{\text{d}t}(\cos{\left(4 t \right)})⟩ \\ &=9 t^{2}\,i+\frac{3}{\left(t + 3\right)^{2}}\,j- 4 \sin{\left(4 t \right)}\,k \\ g'(t)&=⟨\frac{\text{d}}{\text{d}t}(4 t - 3),\,\frac{\text{d}}{\text{d}t}(e^{2 t}),\,\frac{\text{d}}{\text{d}t}(\cos{\left(4 t \right)})⟩ \\ &=4\,i+2 e^{2 t}\,j- 4 \sin{\left(4 t \right)}\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(-2f(t)+2g(t))'&=-2f'(\!t)+2g'(\!t) \\ &=-2\left(9 t^{2}\,i+\frac{3}{\left(t + 3\right)^{2}}\,j- 4 \sin{\left(4 t \right)}\,k\right)+2\left(4\,i+2 e^{2 t}\,j- 4 \sin{\left(4 t \right)}\,k\right) \\ &=\left(- 18 t^{2}\,i- \frac{6}{\left(t + 3\right)^{2}}\,j+8 \sin{\left(4 t \right)}\,k\right)+\left(8\,i+4 e^{2 t}\,j- 8 \sin{\left(4 t \right)}\,k\right) \\ &=(8 - 18 t^{2})\,i+(4 e^{2 t} - \frac{6}{\left(t + 3\right)^{2}})\,j.\end{aligned}
$$

---

## canonical-mixed — hard
Profile: `authored-operations`; parameters: `{"a": 4, "b": 2, "A": -2, "B": 2, "n": 2, "h": -3, "u": 3, "v": 2}`.

Find the derivative of $-2f(t)+2g(t)$ with respect to $t$, where

$$
\begin{aligned}f(t)&=(4 t^{2} + 2)\,i- \frac{4}{t + 3}\,j+\cos{\left(3 t \right)}\,k \\ g(t)&=(2 t - 4)\,i+e^{2 t}\,j+\cos{\left(3 t \right)}\,k\end{aligned}
$$

- $(4 - 16 t)\,i+(4 e^{2 t} - \frac{8}{\left(t + 3\right)^{2}})\,j$ **correct**
- $(- 8 t^{2} + 4 t - 12)\,i+\frac{2 \left(\left(t + 3\right) e^{2 t} + 4\right)}{t + 3}\,j$
- $4\,i+4 e^{2 t}\,j- 6 \sin{\left(3 t \right)}\,k$
- $(16 t + 4)\,i+(4 e^{2 t} + \frac{8}{\left(t + 3\right)^{2}})\,j- 12 \sin{\left(3 t \right)}\,k$
- $- 16 t\,i- \frac{8}{\left(t + 3\right)^{2}}\,j+6 \sin{\left(3 t \right)}\,k$

Using the constant multiple rule and the sum rule, we have

$$
(-2f(t)+2g(t))'=-2f'(\!t)+2g'(\!t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}f'(t)&=⟨\frac{\text{d}}{\text{d}t}(4 t^{2} + 2),\,\frac{\text{d}}{\text{d}t}(- \frac{4}{t + 3}),\,\frac{\text{d}}{\text{d}t}(\cos{\left(3 t \right)})⟩ \\ &=8 t\,i+\frac{4}{\left(t + 3\right)^{2}}\,j- 3 \sin{\left(3 t \right)}\,k \\ g'(t)&=⟨\frac{\text{d}}{\text{d}t}(2 t - 4),\,\frac{\text{d}}{\text{d}t}(e^{2 t}),\,\frac{\text{d}}{\text{d}t}(\cos{\left(3 t \right)})⟩ \\ &=2\,i+2 e^{2 t}\,j- 3 \sin{\left(3 t \right)}\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(-2f(t)+2g(t))'&=-2f'(\!t)+2g'(\!t) \\ &=-2\left(8 t\,i+\frac{4}{\left(t + 3\right)^{2}}\,j- 3 \sin{\left(3 t \right)}\,k\right)+2\left(2\,i+2 e^{2 t}\,j- 3 \sin{\left(3 t \right)}\,k\right) \\ &=\left(- 16 t\,i- \frac{8}{\left(t + 3\right)^{2}}\,j+6 \sin{\left(3 t \right)}\,k\right)+\left(4\,i+4 e^{2 t}\,j- 6 \sin{\left(3 t \right)}\,k\right) \\ &=(4 - 16 t)\,i+(4 e^{2 t} - \frac{8}{\left(t + 3\right)^{2}})\,j.\end{aligned}
$$

---

## canonical-mixed — hard
Profile: `authored-operations`; parameters: `{"a": 1, "b": 2, "A": 3, "B": 3, "n": 3, "h": -2, "u": 3, "v": 4}`.

Find the derivative of $3f(t)+3g(t)$ with respect to $t$, where

$$
\begin{aligned}f(t)&=(t^{3} + 2)\,i- \frac{1}{t + 2}\,j+\cos{\left(3 t \right)}\,k \\ g(t)&=(2 t - 1)\,i+e^{4 t}\,j+\cos{\left(3 t \right)}\,k\end{aligned}
$$

- $9 t^{2}\,i+\frac{3}{\left(t + 2\right)^{2}}\,j- 9 \sin{\left(3 t \right)}\,k$
- $(3 t^{3} + 6 t + 3)\,i+\frac{3 \left(\left(t + 2\right) e^{4 t} - 1\right)}{t + 2}\,j+6 \cos{\left(3 t \right)}\,k$
- $(6 - 9 t^{2})\,i+(12 e^{4 t} - \frac{3}{\left(t + 2\right)^{2}})\,j$
- $(9 t^{2} + 6)\,i+(12 e^{4 t} + \frac{3}{\left(t + 2\right)^{2}})\,j- 18 \sin{\left(3 t \right)}\,k$ **correct**
- $6\,i+12 e^{4 t}\,j- 9 \sin{\left(3 t \right)}\,k$

Using the constant multiple rule and the sum rule, we have

$$
(3f(t)+3g(t))'=3f'(\!t)+3g'(\!t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}f'(t)&=⟨\frac{\text{d}}{\text{d}t}(t^{3} + 2),\,\frac{\text{d}}{\text{d}t}(- \frac{1}{t + 2}),\,\frac{\text{d}}{\text{d}t}(\cos{\left(3 t \right)})⟩ \\ &=3 t^{2}\,i+\frac{1}{\left(t + 2\right)^{2}}\,j- 3 \sin{\left(3 t \right)}\,k \\ g'(t)&=⟨\frac{\text{d}}{\text{d}t}(2 t - 1),\,\frac{\text{d}}{\text{d}t}(e^{4 t}),\,\frac{\text{d}}{\text{d}t}(\cos{\left(3 t \right)})⟩ \\ &=2\,i+4 e^{4 t}\,j- 3 \sin{\left(3 t \right)}\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(3f(t)+3g(t))'&=3f'(\!t)+3g'(\!t) \\ &=3\left(3 t^{2}\,i+\frac{1}{\left(t + 2\right)^{2}}\,j- 3 \sin{\left(3 t \right)}\,k\right)+3\left(2\,i+4 e^{4 t}\,j- 3 \sin{\left(3 t \right)}\,k\right) \\ &=\left(9 t^{2}\,i+\frac{3}{\left(t + 2\right)^{2}}\,j- 9 \sin{\left(3 t \right)}\,k\right)+\left(6\,i+12 e^{4 t}\,j- 9 \sin{\left(3 t \right)}\,k\right) \\ &=(9 t^{2} + 6)\,i+(12 e^{4 t} + \frac{3}{\left(t + 2\right)^{2}})\,j- 18 \sin{\left(3 t \right)}\,k.\end{aligned}
$$

---

## canonical-mixed — hard
Profile: `authored-operations`; parameters: `{"a": 2, "b": 4, "A": 2, "B": 2, "n": 3, "h": 1, "u": 4, "v": 4}`.

Find the derivative of $2f(t)+2g(t)$ with respect to $t$, where

$$
\begin{aligned}f(t)&=(2 t^{3} + 4)\,i- \frac{2}{t - 1}\,j+\cos{\left(4 t \right)}\,k \\ g(t)&=(4 t - 2)\,i+e^{4 t}\,j+\cos{\left(4 t \right)}\,k\end{aligned}
$$

- $(12 t^{2} + 8)\,i+(8 e^{4 t} + \frac{4}{\left(t - 1\right)^{2}})\,j- 16 \sin{\left(4 t \right)}\,k$ **correct**
- $12 t^{2}\,i+\frac{4}{\left(t - 1\right)^{2}}\,j- 8 \sin{\left(4 t \right)}\,k$
- $(8 - 12 t^{2})\,i+(8 e^{4 t} - \frac{4}{\left(t - 1\right)^{2}})\,j$
- $8\,i+8 e^{4 t}\,j- 8 \sin{\left(4 t \right)}\,k$
- $(4 t^{3} + 8 t + 4)\,i+\frac{2 \left(\left(t - 1\right) e^{4 t} - 2\right)}{t - 1}\,j+4 \cos{\left(4 t \right)}\,k$

Using the constant multiple rule and the sum rule, we have

$$
(2f(t)+2g(t))'=2f'(\!t)+2g'(\!t).
$$

Let's find the derivatives of each function:

$$
\begin{aligned}f'(t)&=⟨\frac{\text{d}}{\text{d}t}(2 t^{3} + 4),\,\frac{\text{d}}{\text{d}t}(- \frac{2}{t - 1}),\,\frac{\text{d}}{\text{d}t}(\cos{\left(4 t \right)})⟩ \\ &=6 t^{2}\,i+\frac{2}{\left(t - 1\right)^{2}}\,j- 4 \sin{\left(4 t \right)}\,k \\ g'(t)&=⟨\frac{\text{d}}{\text{d}t}(4 t - 2),\,\frac{\text{d}}{\text{d}t}(e^{4 t}),\,\frac{\text{d}}{\text{d}t}(\cos{\left(4 t \right)})⟩ \\ &=4\,i+4 e^{4 t}\,j- 4 \sin{\left(4 t \right)}\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(2f(t)+2g(t))'&=2f'(\!t)+2g'(\!t) \\ &=2\left(6 t^{2}\,i+\frac{2}{\left(t - 1\right)^{2}}\,j- 4 \sin{\left(4 t \right)}\,k\right)+2\left(4\,i+4 e^{4 t}\,j- 4 \sin{\left(4 t \right)}\,k\right) \\ &=\left(12 t^{2}\,i+\frac{4}{\left(t - 1\right)^{2}}\,j- 8 \sin{\left(4 t \right)}\,k\right)+\left(8\,i+8 e^{4 t}\,j- 8 \sin{\left(4 t \right)}\,k\right) \\ &=(12 t^{2} + 8)\,i+(8 e^{4 t} + \frac{4}{\left(t - 1\right)^{2}})\,j- 16 \sin{\left(4 t \right)}\,k.\end{aligned}
$$
