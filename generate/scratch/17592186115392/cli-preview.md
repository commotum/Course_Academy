## reciprocal_log_reciprocal — easy (authored)

If $g(u)=⟨\frac{1}{u},\,\log{\left(u + 1 \right)},\,3⟩$ and $u(t)=\frac{1}{t}$, then $(g∘u)^{′}(t)=$

- $⟨- \frac{1}{t^{2}},\,\frac{1}{t^{4} \left(1 + \frac{1}{t}\right)},\,0⟩$
- $⟨- t^{2},\,\frac{1}{1 + \frac{1}{t}},\,0⟩$
- $⟨- \frac{1}{u^{2}},\,\frac{1}{u + 1},\,0⟩$
- $⟨1,\,\frac{1}{1 + \frac{1}{t}},\,0⟩$
- $⟨1,\,- \frac{1}{t \left(t + 1\right)},\,0⟩$ **correct**

By the chain rule, we have 

$$
(g∘u)^{′}(t)=g′(u(t))u′(t)
$$

Now, let's find the derivatives of each function:

$$
\begin{aligned}g^{′}(u) & =⟨\frac{\text{d}}{\text{d}u}\left(\frac{1}{u}\right),\,\frac{\text{d}}{\text{d}u}\left(\log{\left(u + 1 \right)}\right),\,\frac{\text{d}}{\text{d}u}\left(3\right)⟩ \\  & =⟨- \frac{1}{u^{2}},\,\frac{1}{u + 1},\,0⟩ \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(\frac{1}{t}\right)=- \frac{1}{t^{2}}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(g∘u)^{′}(t) & =g′(u(t))u′(t) \\  & =⟨- \frac{1}{u(t)^{2}},\,\frac{1}{u(t) + 1},\,0⟩\cdot \left(u^{′}(t)\right) \\  & =⟨- t^{2},\,\frac{1}{1 + \frac{1}{t}},\,0⟩\cdot \left(- \frac{1}{t^{2}}\right) \\  & =⟨1,\,- \frac{1}{t \left(t + 1\right)},\,0⟩\end{aligned}
$$

---

## linear_quadratic_affine — easy (authored)

If $f(u)=[\begin{aligned}2 u \\ u^{2} \\ 1\end{aligned}]$ and $u(t)=3 t + 3$, then $(f∘u)^{′}(t)=$

- $[\begin{aligned}2 \\ 6 t + 6 \\ 0\end{aligned}]$
- $[\begin{aligned}6 \\ 6 t + 6 \\ 0\end{aligned}]$
- $[\begin{aligned}18 \\ 54 t + 54 \\ 0\end{aligned}]$
- $[\begin{aligned}2 \\ 2 u \\ 0\end{aligned}]$
- $[\begin{aligned}6 \\ 18 t + 18 \\ 0\end{aligned}]$ **correct**

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(2 u\right) \\ \frac{\text{d}}{\text{d}u}\left(u^{2}\right) \\ \frac{\text{d}}{\text{d}u}\left(1\right)\end{aligned}]=[\begin{aligned}2 \\ 2 u \\ 0\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(3 t + 3\right)=3\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}2 \\ 2 u(t) \\ 0\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}2 \\ 6 t + 6 \\ 0\end{aligned}]\cdot \left(3\right) \\  & =[\begin{aligned}6 \\ 18 t + 18 \\ 0\end{aligned}]\end{aligned}
$$

---

## mixed_quadratic_inner — moderate (authored)

If $f(u)=[\begin{aligned}- \sin{\left(u \right)} \\ - e^{u} \\ - u^{2}\end{aligned}]$ and $u(t)=- 2 t^{2} - 2 t$, then $(f∘u)^{′}(t)=$

- $[\begin{aligned}- \left(- 4 t - 2\right)^{2} \cos{\left(2 t^{2} + 2 t \right)} \\ - \left(- 4 t - 2\right)^{2} e^{- 2 t^{2} - 2 t} \\ \left(- 4 t - 2\right)^{2} \left(4 t^{2} + 4 t\right)\end{aligned}]$
- $[\begin{aligned}- \cos{\left(2 t^{2} + 2 t \right)} \\ - e^{- 2 t^{2} - 2 t} \\ 4 t^{2} + 4 t\end{aligned}]$
- $[\begin{aligned}- \cos{\left(u \right)} \\ - e^{u} \\ - 2 u\end{aligned}]$
- $[\begin{aligned}\left(4 t + 2\right) \cos{\left(2 t \left(t + 1\right) \right)} \\ - e^{- 2 t^{2} - 2 t} \\ 4 t^{2} + 4 t\end{aligned}]$
- $[\begin{aligned}\left(4 t + 2\right) \cos{\left(2 t \left(t + 1\right) \right)} \\ 2 \left(2 t + 1\right) e^{- 2 t \left(t + 1\right)} \\ - 8 t \left(t + 1\right) \left(2 t + 1\right)\end{aligned}]$ **correct**

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(- \sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(- e^{u}\right) \\ \frac{\text{d}}{\text{d}u}\left(- u^{2}\right)\end{aligned}]=[\begin{aligned}- \cos{\left(u \right)} \\ - e^{u} \\ - 2 u\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(- 2 t^{2} - 2 t\right)=- 4 t - 2\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}- \cos{\left(u(t) \right)} \\ - e^{u(t)} \\ - 2 u(t)\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}- \cos{\left(2 t^{2} + 2 t \right)} \\ - e^{- 2 t^{2} - 2 t} \\ 4 t^{2} + 4 t\end{aligned}]\cdot \left(- 4 t - 2\right) \\  & =[\begin{aligned}\left(4 t + 2\right) \cos{\left(2 t \left(t + 1\right) \right)} \\ 2 \left(2 t + 1\right) e^{- 2 t \left(t + 1\right)} \\ - 8 t \left(t + 1\right) \left(2 t + 1\right)\end{aligned}]\end{aligned}
$$

---

## mixed_quadratic_inner — moderate (authored)

If $f(u)=[\begin{aligned}2 \sin{\left(u \right)} \\ e^{u} \\ - 2 u^{2}\end{aligned}]$ and $u(t)=- 2 t^{2} + t - 1$, then $(f∘u)^{′}(t)=$

- $[\begin{aligned}2 \cos{\left(2 t^{2} - t + 1 \right)} \\ e^{- 2 t^{2} + t - 1} \\ 8 t^{2} - 4 t + 4\end{aligned}]$
- $[\begin{aligned}\left(2 - 8 t\right) \cos{\left(2 t^{2} - t + 1 \right)} \\ e^{- 2 t^{2} + t - 1} \\ 8 t^{2} - 4 t + 4\end{aligned}]$
- $[\begin{aligned}2 \left(1 - 4 t\right)^{2} \cos{\left(2 t^{2} - t + 1 \right)} \\ \left(1 - 4 t\right)^{2} e^{- 2 t^{2} + t - 1} \\ \left(1 - 4 t\right)^{2} \left(8 t^{2} - 4 t + 4\right)\end{aligned}]$
- $[\begin{aligned}2 \cos{\left(u \right)} \\ e^{u} \\ - 4 u\end{aligned}]$
- $[\begin{aligned}\left(2 - 8 t\right) \cos{\left(2 t^{2} - t + 1 \right)} \\ \left(1 - 4 t\right) e^{- 2 t^{2} + t - 1} \\ - 32 t^{3} + 24 t^{2} - 20 t + 4\end{aligned}]$ **correct**

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(2 \sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(e^{u}\right) \\ \frac{\text{d}}{\text{d}u}\left(- 2 u^{2}\right)\end{aligned}]=[\begin{aligned}2 \cos{\left(u \right)} \\ e^{u} \\ - 4 u\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(- 2 t^{2} + t - 1\right)=1 - 4 t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}2 \cos{\left(u(t) \right)} \\ e^{u(t)} \\ - 4 u(t)\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}2 \cos{\left(2 t^{2} - t + 1 \right)} \\ e^{- 2 t^{2} + t - 1} \\ 8 t^{2} - 4 t + 4\end{aligned}]\cdot \left(1 - 4 t\right) \\  & =[\begin{aligned}\left(2 - 8 t\right) \cos{\left(2 t^{2} - t + 1 \right)} \\ \left(1 - 4 t\right) e^{- 2 t^{2} + t - 1} \\ - 32 t^{3} + 24 t^{2} - 20 t + 4\end{aligned}]\end{aligned}
$$

---

## mixed_cubic_inner — hard (authored)

If $f(u)=[\begin{aligned}3 \sin{\left(u \right)} \\ - e^{u} \\ - 2 u^{2}\end{aligned}]$ and $u(t)=3 t^{3} - 3 t - 2$, then $(f∘u)^{′}(t)=$ Write the polynomial component in expanded form.

- $[\begin{aligned}3 \left(9 t^{2} - 3\right)^{2} \cos{\left(- 3 t^{3} + 3 t + 2 \right)} \\ - \left(9 t^{2} - 3\right)^{2} e^{3 t^{3} - 3 t - 2} \\ - 972 t^{7} + 1620 t^{5} + 648 t^{4} - 756 t^{3} - 432 t^{2} + 108 t + 72\end{aligned}]$
- $[\begin{aligned}3 \cos{\left(- 3 t^{3} + 3 t + 2 \right)} \\ - e^{3 t^{3} - 3 t - 2} \\ - 12 t^{3} + 12 t + 8\end{aligned}]$
- $[\begin{aligned}3 \cos{\left(u \right)} \\ - e^{u} \\ - 4 u\end{aligned}]$
- $[\begin{aligned}\left(27 t^{2} - 9\right) \cos{\left(- 3 t^{3} + 3 t + 2 \right)} \\ - e^{3 t^{3} - 3 t - 2} \\ - 12 t^{3} + 12 t + 8\end{aligned}]$
- $[\begin{aligned}\left(27 t^{2} - 9\right) \cos{\left(- 3 t^{3} + 3 t + 2 \right)} \\ \left(3 - 9 t^{2}\right) e^{3 t^{3} - 3 t - 2} \\ - 108 t^{5} + 144 t^{3} + 72 t^{2} - 36 t - 24\end{aligned}]$ **correct**

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(3 \sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(- e^{u}\right) \\ \frac{\text{d}}{\text{d}u}\left(- 2 u^{2}\right)\end{aligned}]=[\begin{aligned}3 \cos{\left(u \right)} \\ - e^{u} \\ - 4 u\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(3 t^{3} - 3 t - 2\right)=9 t^{2} - 3\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}3 \cos{\left(u(t) \right)} \\ - e^{u(t)} \\ - 4 u(t)\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}3 \cos{\left(- 3 t^{3} + 3 t + 2 \right)} \\ - e^{3 t^{3} - 3 t - 2} \\ - 12 t^{3} + 12 t + 8\end{aligned}]\cdot \left(9 t^{2} - 3\right) \\  & =[\begin{aligned}\left(27 t^{2} - 9\right) \cos{\left(- 3 t^{3} + 3 t + 2 \right)} \\ \left(3 - 9 t^{2}\right) e^{3 t^{3} - 3 t - 2} \\ - 108 t^{5} + 144 t^{3} + 72 t^{2} - 36 t - 24\end{aligned}]\end{aligned}
$$

---

## mixed_cubic_inner — hard (authored)

If $f(u)=[\begin{aligned}\sin{\left(u \right)} \\ - e^{u} \\ 3 u^{2}\end{aligned}]$ and $u(t)=- 3 t^{3} - t - 1$, then $(f∘u)^{′}(t)=$ Write the polynomial component in expanded form.

- $[\begin{aligned}\cos{\left(3 t^{3} + t + 1 \right)} \\ - e^{- 3 t^{3} - t - 1} \\ - 18 t^{3} - 6 t - 6\end{aligned}]$
- $[\begin{aligned}\left(- 9 t^{2} - 1\right) \cos{\left(3 t^{3} + t + 1 \right)} \\ - e^{- 3 t^{3} - t - 1} \\ - 18 t^{3} - 6 t - 6\end{aligned}]$
- $[\begin{aligned}\left(- 9 t^{2} - 1\right)^{2} \cos{\left(3 t^{3} + t + 1 \right)} \\ - \left(- 9 t^{2} - 1\right)^{2} e^{- 3 t^{3} - t - 1} \\ - 1458 t^{7} - 810 t^{5} - 486 t^{4} - 126 t^{3} - 108 t^{2} - 6 t - 6\end{aligned}]$
- $[\begin{aligned}\cos{\left(u \right)} \\ - e^{u} \\ 6 u\end{aligned}]$
- $[\begin{aligned}\left(- 9 t^{2} - 1\right) \cos{\left(3 t^{3} + t + 1 \right)} \\ \left(9 t^{2} + 1\right) e^{- 3 t^{3} - t - 1} \\ 162 t^{5} + 72 t^{3} + 54 t^{2} + 6 t + 6\end{aligned}]$ **correct**

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(\sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(- e^{u}\right) \\ \frac{\text{d}}{\text{d}u}\left(3 u^{2}\right)\end{aligned}]=[\begin{aligned}\cos{\left(u \right)} \\ - e^{u} \\ 6 u\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(- 3 t^{3} - t - 1\right)=- 9 t^{2} - 1\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}\cos{\left(u(t) \right)} \\ - e^{u(t)} \\ 6 u(t)\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}\cos{\left(3 t^{3} + t + 1 \right)} \\ - e^{- 3 t^{3} - t - 1} \\ - 18 t^{3} - 6 t - 6\end{aligned}]\cdot \left(- 9 t^{2} - 1\right) \\  & =[\begin{aligned}\left(- 9 t^{2} - 1\right) \cos{\left(3 t^{3} + t + 1 \right)} \\ \left(9 t^{2} + 1\right) e^{- 3 t^{3} - t - 1} \\ 162 t^{5} + 72 t^{3} + 54 t^{2} + 6 t + 6\end{aligned}]\end{aligned}
$$
