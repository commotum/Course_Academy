## mixed_quadratic_inner — moderate (authored)

If $f(u)=\begin{bmatrix}- 2 \sin{\left(u \right)} \\ - e^{u} \\ - 2 u^{2}\end{bmatrix}$ and $u(t)=- t^{2} - 2 t - 2$, then $(f∘u)^{′}(t)=$

- $\begin{bmatrix}\left(4 t + 4\right) \cos{\left(t^{2} + 2 t + 2 \right)} \\ - e^{- t^{2} - 2 t - 2} \\ 4 t^{2} + 8 t + 8\end{bmatrix}$
- $\begin{bmatrix}- 2 \cos{\left(u \right)} \\ - e^{u} \\ - 4 u\end{bmatrix}$
- $\begin{bmatrix}- 2 \left(- 2 t - 2\right)^{2} \cos{\left(t^{2} + 2 t + 2 \right)} \\ - \left(- 2 t - 2\right)^{2} e^{- t^{2} - 2 t - 2} \\ \left(- 2 t - 2\right)^{2} \left(4 t^{2} + 8 t + 8\right)\end{bmatrix}$
- $\begin{bmatrix}\left(4 t + 4\right) \cos{\left(t^{2} + 2 t + 2 \right)} \\ 2 \left(t + 1\right) e^{- t^{2} - 2 t - 2} \\ - 8 \left(t + 1\right) \left(t^{2} + 2 t + 2\right)\end{bmatrix}$ **correct**
- $\begin{bmatrix}- 2 \cos{\left(t^{2} + 2 t + 2 \right)} \\ - e^{- t^{2} - 2 t - 2} \\ 4 t^{2} + 8 t + 8\end{bmatrix}$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\begin{bmatrix}\frac{\text{d}}{\text{d}u}\left(- 2 \sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(- e^{u}\right) \\ \frac{\text{d}}{\text{d}u}\left(- 2 u^{2}\right)\end{bmatrix}=\begin{bmatrix}- 2 \cos{\left(u \right)} \\ - e^{u} \\ - 4 u\end{bmatrix} \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(- t^{2} - 2 t - 2\right)=- 2 t - 2\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\begin{bmatrix}- 2 \cos{\left(u(t) \right)} \\ - e^{u(t)} \\ - 4 u(t)\end{bmatrix}\cdot \left(u^{′}(t)\right) \\  & =\begin{bmatrix}- 2 \cos{\left(t^{2} + 2 t + 2 \right)} \\ - e^{- t^{2} - 2 t - 2} \\ 4 t^{2} + 8 t + 8\end{bmatrix}\cdot \left(- 2 t - 2\right) \\  & =\begin{bmatrix}\left(4 t + 4\right) \cos{\left(t^{2} + 2 t + 2 \right)} \\ 2 \left(t + 1\right) e^{- t^{2} - 2 t - 2} \\ - 8 \left(t + 1\right) \left(t^{2} + 2 t + 2\right)\end{bmatrix}\end{aligned}
$$

---

## mixed_quadratic_inner — moderate (authored)

If $f(u)=\begin{bmatrix}2 \sin{\left(u \right)} \\ e^{u} \\ - 2 u^{2}\end{bmatrix}$ and $u(t)=- t^{2} + 2 t - 2$, then $(f∘u)^{′}(t)=$

- $\begin{bmatrix}2 \cos{\left(u \right)} \\ e^{u} \\ - 4 u\end{bmatrix}$
- $\begin{bmatrix}\left(4 - 4 t\right) \cos{\left(t^{2} - 2 t + 2 \right)} \\ e^{- t^{2} + 2 t - 2} \\ 4 t^{2} - 8 t + 8\end{bmatrix}$
- $\begin{bmatrix}\left(4 - 4 t\right) \cos{\left(t^{2} - 2 t + 2 \right)} \\ 2 \left(1 - t\right) e^{- t^{2} + 2 t - 2} \\ - 8 \left(t - 1\right) \left(t^{2} - 2 t + 2\right)\end{bmatrix}$ **correct**
- $\begin{bmatrix}2 \left(2 - 2 t\right)^{2} \cos{\left(t^{2} - 2 t + 2 \right)} \\ \left(2 - 2 t\right)^{2} e^{- t^{2} + 2 t - 2} \\ \left(2 - 2 t\right)^{2} \left(4 t^{2} - 8 t + 8\right)\end{bmatrix}$
- $\begin{bmatrix}2 \cos{\left(t^{2} - 2 t + 2 \right)} \\ e^{- t^{2} + 2 t - 2} \\ 4 t^{2} - 8 t + 8\end{bmatrix}$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\begin{bmatrix}\frac{\text{d}}{\text{d}u}\left(2 \sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(e^{u}\right) \\ \frac{\text{d}}{\text{d}u}\left(- 2 u^{2}\right)\end{bmatrix}=\begin{bmatrix}2 \cos{\left(u \right)} \\ e^{u} \\ - 4 u\end{bmatrix} \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(- t^{2} + 2 t - 2\right)=2 - 2 t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\begin{bmatrix}2 \cos{\left(u(t) \right)} \\ e^{u(t)} \\ - 4 u(t)\end{bmatrix}\cdot \left(u^{′}(t)\right) \\  & =\begin{bmatrix}2 \cos{\left(t^{2} - 2 t + 2 \right)} \\ e^{- t^{2} + 2 t - 2} \\ 4 t^{2} - 8 t + 8\end{bmatrix}\cdot \left(2 - 2 t\right) \\  & =\begin{bmatrix}\left(4 - 4 t\right) \cos{\left(t^{2} - 2 t + 2 \right)} \\ 2 \left(1 - t\right) e^{- t^{2} + 2 t - 2} \\ - 8 \left(t - 1\right) \left(t^{2} - 2 t + 2\right)\end{bmatrix}\end{aligned}
$$

---

## mixed_quadratic_inner — moderate (authored)

If $f(u)=\begin{bmatrix}2 \sin{\left(u \right)} \\ 2 e^{u} \\ - 2 u^{2}\end{bmatrix}$ and $u(t)=- 2 t^{2} + t + 2$, then $(f∘u)^{′}(t)=$

- $\begin{bmatrix}\left(2 - 8 t\right) \cos{\left(- 2 t^{2} + t + 2 \right)} \\ 2 e^{- 2 t^{2} + t + 2} \\ 8 t^{2} - 4 t - 8\end{bmatrix}$
- $\begin{bmatrix}2 \cos{\left(- 2 t^{2} + t + 2 \right)} \\ 2 e^{- 2 t^{2} + t + 2} \\ 8 t^{2} - 4 t - 8\end{bmatrix}$
- $\begin{bmatrix}2 \left(1 - 4 t\right)^{2} \cos{\left(- 2 t^{2} + t + 2 \right)} \\ 2 \left(1 - 4 t\right)^{2} e^{- 2 t^{2} + t + 2} \\ \left(1 - 4 t\right)^{2} \left(8 t^{2} - 4 t - 8\right)\end{bmatrix}$
- $\begin{bmatrix}2 \cos{\left(u \right)} \\ 2 e^{u} \\ - 4 u\end{bmatrix}$
- $\begin{bmatrix}\left(2 - 8 t\right) \cos{\left(- 2 t^{2} + t + 2 \right)} \\ \left(2 - 8 t\right) e^{- 2 t^{2} + t + 2} \\ 4 \left(4 t - 1\right) \left(- 2 t^{2} + t + 2\right)\end{bmatrix}$ **correct**

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\begin{bmatrix}\frac{\text{d}}{\text{d}u}\left(2 \sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(2 e^{u}\right) \\ \frac{\text{d}}{\text{d}u}\left(- 2 u^{2}\right)\end{bmatrix}=\begin{bmatrix}2 \cos{\left(u \right)} \\ 2 e^{u} \\ - 4 u\end{bmatrix} \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(- 2 t^{2} + t + 2\right)=1 - 4 t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\begin{bmatrix}2 \cos{\left(u(t) \right)} \\ 2 e^{u(t)} \\ - 4 u(t)\end{bmatrix}\cdot \left(u^{′}(t)\right) \\  & =\begin{bmatrix}2 \cos{\left(- 2 t^{2} + t + 2 \right)} \\ 2 e^{- 2 t^{2} + t + 2} \\ 8 t^{2} - 4 t - 8\end{bmatrix}\cdot \left(1 - 4 t\right) \\  & =\begin{bmatrix}\left(2 - 8 t\right) \cos{\left(- 2 t^{2} + t + 2 \right)} \\ \left(2 - 8 t\right) e^{- 2 t^{2} + t + 2} \\ 4 \left(4 t - 1\right) \left(- 2 t^{2} + t + 2\right)\end{bmatrix}\end{aligned}
$$

---

## mixed_quadratic_inner — moderate (authored)

If $f(u)=\begin{bmatrix}\sin{\left(u \right)} \\ 2 e^{u} \\ - u^{2}\end{bmatrix}$ and $u(t)=t^{2} + 2 t + 1$, then $(f∘u)^{′}(t)=$

- $\begin{bmatrix}\left(2 t + 2\right) \cos{\left(t^{2} + 2 t + 1 \right)} \\ 4 \left(t + 1\right) e^{t^{2} + 2 t + 1} \\ - 4 \left(t + 1\right) \left(t^{2} + 2 t + 1\right)\end{bmatrix}$ **correct**
- $\begin{bmatrix}\cos{\left(t^{2} + 2 t + 1 \right)} \\ 2 e^{t^{2} + 2 t + 1} \\ - 2 t^{2} - 4 t - 2\end{bmatrix}$
- $\begin{bmatrix}\left(2 t + 2\right) \cos{\left(t^{2} + 2 t + 1 \right)} \\ 2 e^{t^{2} + 2 t + 1} \\ - 2 t^{2} - 4 t - 2\end{bmatrix}$
- $\begin{bmatrix}\left(2 t + 2\right)^{2} \cos{\left(t^{2} + 2 t + 1 \right)} \\ 2 \left(2 t + 2\right)^{2} e^{t^{2} + 2 t + 1} \\ \left(2 t + 2\right)^{2} \left(- 2 t^{2} - 4 t - 2\right)\end{bmatrix}$
- $\begin{bmatrix}\cos{\left(u \right)} \\ 2 e^{u} \\ - 2 u\end{bmatrix}$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\begin{bmatrix}\frac{\text{d}}{\text{d}u}\left(\sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(2 e^{u}\right) \\ \frac{\text{d}}{\text{d}u}\left(- u^{2}\right)\end{bmatrix}=\begin{bmatrix}\cos{\left(u \right)} \\ 2 e^{u} \\ - 2 u\end{bmatrix} \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(t^{2} + 2 t + 1\right)=2 t + 2\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\begin{bmatrix}\cos{\left(u(t) \right)} \\ 2 e^{u(t)} \\ - 2 u(t)\end{bmatrix}\cdot \left(u^{′}(t)\right) \\  & =\begin{bmatrix}\cos{\left(t^{2} + 2 t + 1 \right)} \\ 2 e^{t^{2} + 2 t + 1} \\ - 2 t^{2} - 4 t - 2\end{bmatrix}\cdot \left(2 t + 2\right) \\  & =\begin{bmatrix}\left(2 t + 2\right) \cos{\left(t^{2} + 2 t + 1 \right)} \\ 4 \left(t + 1\right) e^{t^{2} + 2 t + 1} \\ - 4 \left(t + 1\right) \left(t^{2} + 2 t + 1\right)\end{bmatrix}\end{aligned}
$$

---

## mixed_quadratic_inner — moderate (authored)

If $f(u)=\begin{bmatrix}\sin{\left(u \right)} \\ e^{u} \\ - 2 u^{2}\end{bmatrix}$ and $u(t)=- 2 t^{2} - 2 t + 1$, then $(f∘u)^{′}(t)=$

- $\begin{bmatrix}\left(- 4 t - 2\right)^{2} \cos{\left(2 t^{2} + 2 t - 1 \right)} \\ \left(- 4 t - 2\right)^{2} e^{- 2 t^{2} - 2 t + 1} \\ \left(- 4 t - 2\right)^{2} \left(8 t^{2} + 8 t - 4\right)\end{bmatrix}$
- $\begin{bmatrix}\cos{\left(u \right)} \\ e^{u} \\ - 4 u\end{bmatrix}$
- $\begin{bmatrix}\cos{\left(2 t^{2} + 2 t - 1 \right)} \\ e^{- 2 t^{2} - 2 t + 1} \\ 8 t^{2} + 8 t - 4\end{bmatrix}$
- $\begin{bmatrix}\left(- 4 t - 2\right) \cos{\left(2 t^{2} + 2 t - 1 \right)} \\ e^{- 2 t^{2} - 2 t + 1} \\ 8 t^{2} + 8 t - 4\end{bmatrix}$
- $\begin{bmatrix}\left(- 4 t - 2\right) \cos{\left(2 t^{2} + 2 t - 1 \right)} \\ \left(- 4 t - 2\right) e^{- 2 t^{2} - 2 t + 1} \\ - 32 t^{3} - 48 t^{2} + 8\end{bmatrix}$ **correct**

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\begin{bmatrix}\frac{\text{d}}{\text{d}u}\left(\sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(e^{u}\right) \\ \frac{\text{d}}{\text{d}u}\left(- 2 u^{2}\right)\end{bmatrix}=\begin{bmatrix}\cos{\left(u \right)} \\ e^{u} \\ - 4 u\end{bmatrix} \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(- 2 t^{2} - 2 t + 1\right)=- 4 t - 2\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\begin{bmatrix}\cos{\left(u(t) \right)} \\ e^{u(t)} \\ - 4 u(t)\end{bmatrix}\cdot \left(u^{′}(t)\right) \\  & =\begin{bmatrix}\cos{\left(2 t^{2} + 2 t - 1 \right)} \\ e^{- 2 t^{2} - 2 t + 1} \\ 8 t^{2} + 8 t - 4\end{bmatrix}\cdot \left(- 4 t - 2\right) \\  & =\begin{bmatrix}\left(- 4 t - 2\right) \cos{\left(2 t^{2} + 2 t - 1 \right)} \\ \left(- 4 t - 2\right) e^{- 2 t^{2} - 2 t + 1} \\ - 32 t^{3} - 48 t^{2} + 8\end{bmatrix}\end{aligned}
$$

---

## mixed_cubic_inner — hard (authored)

If $f(u)=\begin{bmatrix}- 2 \sin{\left(u \right)} \\ 2 e^{u} \\ - 3 u^{2}\end{bmatrix}$ and $u(t)=- 2 t^{3} + 3 t + 2$, then $(f∘u)^{′}(t)=$ Write the polynomial component in expanded form.

- $\begin{bmatrix}\left(12 t^{2} - 6\right) \cos{\left(- 2 t^{3} + 3 t + 2 \right)} \\ 2 e^{- 2 t^{3} + 3 t + 2} \\ 12 t^{3} - 18 t - 12\end{bmatrix}$
- $\begin{bmatrix}- 2 \cos{\left(u \right)} \\ 2 e^{u} \\ - 6 u\end{bmatrix}$
- $\begin{bmatrix}\left(12 t^{2} - 6\right) \cos{\left(- 2 t^{3} + 3 t + 2 \right)} \\ \left(6 - 12 t^{2}\right) e^{- 2 t^{3} + 3 t + 2} \\ - 72 t^{5} + 144 t^{3} + 72 t^{2} - 54 t - 36\end{bmatrix}$ **correct**
- $\begin{bmatrix}- 2 \left(3 - 6 t^{2}\right)^{2} \cos{\left(- 2 t^{3} + 3 t + 2 \right)} \\ 2 \left(3 - 6 t^{2}\right)^{2} e^{- 2 t^{3} + 3 t + 2} \\ 432 t^{7} - 1080 t^{5} - 432 t^{4} + 756 t^{3} + 432 t^{2} - 162 t - 108\end{bmatrix}$
- $\begin{bmatrix}- 2 \cos{\left(- 2 t^{3} + 3 t + 2 \right)} \\ 2 e^{- 2 t^{3} + 3 t + 2} \\ 12 t^{3} - 18 t - 12\end{bmatrix}$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\begin{bmatrix}\frac{\text{d}}{\text{d}u}\left(- 2 \sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(2 e^{u}\right) \\ \frac{\text{d}}{\text{d}u}\left(- 3 u^{2}\right)\end{bmatrix}=\begin{bmatrix}- 2 \cos{\left(u \right)} \\ 2 e^{u} \\ - 6 u\end{bmatrix} \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(- 2 t^{3} + 3 t + 2\right)=3 - 6 t^{2}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\begin{bmatrix}- 2 \cos{\left(u(t) \right)} \\ 2 e^{u(t)} \\ - 6 u(t)\end{bmatrix}\cdot \left(u^{′}(t)\right) \\  & =\begin{bmatrix}- 2 \cos{\left(- 2 t^{3} + 3 t + 2 \right)} \\ 2 e^{- 2 t^{3} + 3 t + 2} \\ 12 t^{3} - 18 t - 12\end{bmatrix}\cdot \left(3 - 6 t^{2}\right) \\  & =\begin{bmatrix}\left(12 t^{2} - 6\right) \cos{\left(- 2 t^{3} + 3 t + 2 \right)} \\ \left(6 - 12 t^{2}\right) e^{- 2 t^{3} + 3 t + 2} \\ - 72 t^{5} + 144 t^{3} + 72 t^{2} - 54 t - 36\end{bmatrix}\end{aligned}
$$

---

## mixed_cubic_inner — hard (authored)

If $f(u)=\begin{bmatrix}\sin{\left(u \right)} \\ - 2 e^{u} \\ - 3 u^{2}\end{bmatrix}$ and $u(t)=2 t^{3} - 3 t - 1$, then $(f∘u)^{′}(t)=$ Write the polynomial component in expanded form.

- $\begin{bmatrix}\cos{\left(u \right)} \\ - 2 e^{u} \\ - 6 u\end{bmatrix}$
- $\begin{bmatrix}\cos{\left(- 2 t^{3} + 3 t + 1 \right)} \\ - 2 e^{2 t^{3} - 3 t - 1} \\ - 12 t^{3} + 18 t + 6\end{bmatrix}$
- $\begin{bmatrix}\left(6 t^{2} - 3\right)^{2} \cos{\left(- 2 t^{3} + 3 t + 1 \right)} \\ - 2 \left(6 t^{2} - 3\right)^{2} e^{2 t^{3} - 3 t - 1} \\ - 432 t^{7} + 1080 t^{5} + 216 t^{4} - 756 t^{3} - 216 t^{2} + 162 t + 54\end{bmatrix}$
- $\begin{bmatrix}\left(6 t^{2} - 3\right) \cos{\left(- 2 t^{3} + 3 t + 1 \right)} \\ \left(6 - 12 t^{2}\right) e^{2 t^{3} - 3 t - 1} \\ - 72 t^{5} + 144 t^{3} + 36 t^{2} - 54 t - 18\end{bmatrix}$ **correct**
- $\begin{bmatrix}\left(6 t^{2} - 3\right) \cos{\left(- 2 t^{3} + 3 t + 1 \right)} \\ - 2 e^{2 t^{3} - 3 t - 1} \\ - 12 t^{3} + 18 t + 6\end{bmatrix}$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\begin{bmatrix}\frac{\text{d}}{\text{d}u}\left(\sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(- 2 e^{u}\right) \\ \frac{\text{d}}{\text{d}u}\left(- 3 u^{2}\right)\end{bmatrix}=\begin{bmatrix}\cos{\left(u \right)} \\ - 2 e^{u} \\ - 6 u\end{bmatrix} \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(2 t^{3} - 3 t - 1\right)=6 t^{2} - 3\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\begin{bmatrix}\cos{\left(u(t) \right)} \\ - 2 e^{u(t)} \\ - 6 u(t)\end{bmatrix}\cdot \left(u^{′}(t)\right) \\  & =\begin{bmatrix}\cos{\left(- 2 t^{3} + 3 t + 1 \right)} \\ - 2 e^{2 t^{3} - 3 t - 1} \\ - 12 t^{3} + 18 t + 6\end{bmatrix}\cdot \left(6 t^{2} - 3\right) \\  & =\begin{bmatrix}\left(6 t^{2} - 3\right) \cos{\left(- 2 t^{3} + 3 t + 1 \right)} \\ \left(6 - 12 t^{2}\right) e^{2 t^{3} - 3 t - 1} \\ - 72 t^{5} + 144 t^{3} + 36 t^{2} - 54 t - 18\end{bmatrix}\end{aligned}
$$

---

## mixed_cubic_inner — hard (authored)

If $f(u)=\begin{bmatrix}- \sin{\left(u \right)} \\ 3 e^{u} \\ u^{2}\end{bmatrix}$ and $u(t)=- t^{3} + t + 1$, then $(f∘u)^{′}(t)=$ Write the polynomial component in expanded form.

- $\begin{bmatrix}\left(3 t^{2} - 1\right) \cos{\left(- t^{3} + t + 1 \right)} \\ \left(3 - 9 t^{2}\right) e^{- t^{3} + t + 1} \\ 6 t^{5} - 8 t^{3} - 6 t^{2} + 2 t + 2\end{bmatrix}$ **correct**
- $\begin{bmatrix}- \cos{\left(- t^{3} + t + 1 \right)} \\ 3 e^{- t^{3} + t + 1} \\ - 2 t^{3} + 2 t + 2\end{bmatrix}$
- $\begin{bmatrix}\left(3 t^{2} - 1\right) \cos{\left(- t^{3} + t + 1 \right)} \\ 3 e^{- t^{3} + t + 1} \\ - 2 t^{3} + 2 t + 2\end{bmatrix}$
- $\begin{bmatrix}- \left(1 - 3 t^{2}\right)^{2} \cos{\left(- t^{3} + t + 1 \right)} \\ 3 \left(1 - 3 t^{2}\right)^{2} e^{- t^{3} + t + 1} \\ - 18 t^{7} + 30 t^{5} + 18 t^{4} - 14 t^{3} - 12 t^{2} + 2 t + 2\end{bmatrix}$
- $\begin{bmatrix}- \cos{\left(u \right)} \\ 3 e^{u} \\ 2 u\end{bmatrix}$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\begin{bmatrix}\frac{\text{d}}{\text{d}u}\left(- \sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(3 e^{u}\right) \\ \frac{\text{d}}{\text{d}u}\left(u^{2}\right)\end{bmatrix}=\begin{bmatrix}- \cos{\left(u \right)} \\ 3 e^{u} \\ 2 u\end{bmatrix} \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(- t^{3} + t + 1\right)=1 - 3 t^{2}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\begin{bmatrix}- \cos{\left(u(t) \right)} \\ 3 e^{u(t)} \\ 2 u(t)\end{bmatrix}\cdot \left(u^{′}(t)\right) \\  & =\begin{bmatrix}- \cos{\left(- t^{3} + t + 1 \right)} \\ 3 e^{- t^{3} + t + 1} \\ - 2 t^{3} + 2 t + 2\end{bmatrix}\cdot \left(1 - 3 t^{2}\right) \\  & =\begin{bmatrix}\left(3 t^{2} - 1\right) \cos{\left(- t^{3} + t + 1 \right)} \\ \left(3 - 9 t^{2}\right) e^{- t^{3} + t + 1} \\ 6 t^{5} - 8 t^{3} - 6 t^{2} + 2 t + 2\end{bmatrix}\end{aligned}
$$

---

## mixed_cubic_inner — hard (authored)

If $f(u)=\begin{bmatrix}- 2 \sin{\left(u \right)} \\ - e^{u} \\ 2 u^{2}\end{bmatrix}$ and $u(t)=3 t^{3} - 3 t + 1$, then $(f∘u)^{′}(t)=$ Write the polynomial component in expanded form.

- $\begin{bmatrix}- 2 \left(9 t^{2} - 3\right)^{2} \cos{\left(3 t^{3} - 3 t + 1 \right)} \\ - \left(9 t^{2} - 3\right)^{2} e^{3 t^{3} - 3 t + 1} \\ 972 t^{7} - 1620 t^{5} + 324 t^{4} + 756 t^{3} - 216 t^{2} - 108 t + 36\end{bmatrix}$
- $\begin{bmatrix}- 2 \cos{\left(3 t^{3} - 3 t + 1 \right)} \\ - e^{3 t^{3} - 3 t + 1} \\ 12 t^{3} - 12 t + 4\end{bmatrix}$
- $\begin{bmatrix}\left(6 - 18 t^{2}\right) \cos{\left(3 t^{3} - 3 t + 1 \right)} \\ - e^{3 t^{3} - 3 t + 1} \\ 12 t^{3} - 12 t + 4\end{bmatrix}$
- $\begin{bmatrix}- 2 \cos{\left(u \right)} \\ - e^{u} \\ 4 u\end{bmatrix}$
- $\begin{bmatrix}\left(6 - 18 t^{2}\right) \cos{\left(3 t^{3} - 3 t + 1 \right)} \\ \left(3 - 9 t^{2}\right) e^{3 t^{3} - 3 t + 1} \\ 108 t^{5} - 144 t^{3} + 36 t^{2} + 36 t - 12\end{bmatrix}$ **correct**

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\begin{bmatrix}\frac{\text{d}}{\text{d}u}\left(- 2 \sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(- e^{u}\right) \\ \frac{\text{d}}{\text{d}u}\left(2 u^{2}\right)\end{bmatrix}=\begin{bmatrix}- 2 \cos{\left(u \right)} \\ - e^{u} \\ 4 u\end{bmatrix} \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(3 t^{3} - 3 t + 1\right)=9 t^{2} - 3\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\begin{bmatrix}- 2 \cos{\left(u(t) \right)} \\ - e^{u(t)} \\ 4 u(t)\end{bmatrix}\cdot \left(u^{′}(t)\right) \\  & =\begin{bmatrix}- 2 \cos{\left(3 t^{3} - 3 t + 1 \right)} \\ - e^{3 t^{3} - 3 t + 1} \\ 12 t^{3} - 12 t + 4\end{bmatrix}\cdot \left(9 t^{2} - 3\right) \\  & =\begin{bmatrix}\left(6 - 18 t^{2}\right) \cos{\left(3 t^{3} - 3 t + 1 \right)} \\ \left(3 - 9 t^{2}\right) e^{3 t^{3} - 3 t + 1} \\ 108 t^{5} - 144 t^{3} + 36 t^{2} + 36 t - 12\end{bmatrix}\end{aligned}
$$

---

## mixed_cubic_inner — hard (authored)

If $f(u)=\begin{bmatrix}- \sin{\left(u \right)} \\ - 2 e^{u} \\ - u^{2}\end{bmatrix}$ and $u(t)=- 2 t^{3} - 3 t + 2$, then $(f∘u)^{′}(t)=$ Write the polynomial component in expanded form.

- $\begin{bmatrix}- \left(- 6 t^{2} - 3\right)^{2} \cos{\left(2 t^{3} + 3 t - 2 \right)} \\ - 2 \left(- 6 t^{2} - 3\right)^{2} e^{- 2 t^{3} - 3 t + 2} \\ 144 t^{7} + 360 t^{5} - 144 t^{4} + 252 t^{3} - 144 t^{2} + 54 t - 36\end{bmatrix}$
- $\begin{bmatrix}\left(6 t^{2} + 3\right) \cos{\left(2 t^{3} + 3 t - 2 \right)} \\ - 2 e^{- 2 t^{3} - 3 t + 2} \\ 4 t^{3} + 6 t - 4\end{bmatrix}$
- $\begin{bmatrix}- \cos{\left(u \right)} \\ - 2 e^{u} \\ - 2 u\end{bmatrix}$
- $\begin{bmatrix}\left(6 t^{2} + 3\right) \cos{\left(2 t^{3} + 3 t - 2 \right)} \\ \left(12 t^{2} + 6\right) e^{- 2 t^{3} - 3 t + 2} \\ - 24 t^{5} - 48 t^{3} + 24 t^{2} - 18 t + 12\end{bmatrix}$ **correct**
- $\begin{bmatrix}- \cos{\left(2 t^{3} + 3 t - 2 \right)} \\ - 2 e^{- 2 t^{3} - 3 t + 2} \\ 4 t^{3} + 6 t - 4\end{bmatrix}$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\begin{bmatrix}\frac{\text{d}}{\text{d}u}\left(- \sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(- 2 e^{u}\right) \\ \frac{\text{d}}{\text{d}u}\left(- u^{2}\right)\end{bmatrix}=\begin{bmatrix}- \cos{\left(u \right)} \\ - 2 e^{u} \\ - 2 u\end{bmatrix} \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(- 2 t^{3} - 3 t + 2\right)=- 6 t^{2} - 3\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\begin{bmatrix}- \cos{\left(u(t) \right)} \\ - 2 e^{u(t)} \\ - 2 u(t)\end{bmatrix}\cdot \left(u^{′}(t)\right) \\  & =\begin{bmatrix}- \cos{\left(2 t^{3} + 3 t - 2 \right)} \\ - 2 e^{- 2 t^{3} - 3 t + 2} \\ 4 t^{3} + 6 t - 4\end{bmatrix}\cdot \left(- 6 t^{2} - 3\right) \\  & =\begin{bmatrix}\left(6 t^{2} + 3\right) \cos{\left(2 t^{3} + 3 t - 2 \right)} \\ \left(12 t^{2} + 6\right) e^{- 2 t^{3} - 3 t + 2} \\ - 24 t^{5} - 48 t^{3} + 24 t^{2} - 18 t + 12\end{bmatrix}\end{aligned}
$$
