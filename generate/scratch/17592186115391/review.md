# Scalar function multiple rule review

All originals below come from math basis 1356. Coordinate-scaled observed bank variants are evidence profiles, not default inferred error intent. Normal practice uses labeled authored operation banks.

## Original q-32286

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}\operatorname{sin}⁡t \\ 2t-8 \\ {5}^{t}\end{aligned}]$ and $u(t)={t}^{2}.$

- $[\begin{aligned}{t}^{2}\operatorname{cos}⁡t+2t\operatorname{sin}⁡t \\ 6{t}^{2}-16t \\ {5}^{t}+\operatorname{ln}⁡5\end{aligned}]$
- $[\begin{aligned}{t}^{2}\operatorname{cos}⁡t+2t\operatorname{sin}⁡t \\ {t}^{2}-t \\ {5}^{t}+{5}^{t}\cdot 2t\end{aligned}]$
- $[\begin{aligned}{t}^{2}\operatorname{sin}⁡t-4t\operatorname{cos}⁡t \\ 6{t}^{2}-16t \\ {5}^{t}{t}^{2}\operatorname{ln}⁡5+{5}^{t}\cdot 2t\end{aligned}]$
- $[\begin{aligned}{t}^{2}\operatorname{cos}⁡t+2t\operatorname{sin}⁡t \\ 12{t}^{2}+36 \\ {5}^{t}{t}^{2}\operatorname{ln}⁡5+{5}^{t}\cdot 2t\end{aligned}]$
- $[\begin{aligned}{t}^{2}\operatorname{cos}⁡t+2t\operatorname{sin}⁡t \\ 6{t}^{2}-16t \\ {5}^{t}{t}^{2}\operatorname{ln}⁡5+{5}^{t}\cdot 2t\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t) \\ \frac{\text{d}}{\text{d}t}(2t-8) \\ \frac{\text{d}}{\text{d}t}({5}^{t})\end{aligned}]=[\begin{aligned}\operatorname{cos}⁡t \\ 2 \\ {5}^{t}\operatorname{ln}⁡5\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{2})=2t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & ={t}^{2}[\begin{aligned}\operatorname{cos}⁡t \\ 2 \\ {5}^{t}\operatorname{ln}⁡5\end{aligned}]+2t[\begin{aligned}\operatorname{sin}⁡t \\ 2t-8 \\ {5}^{t}\end{aligned}] \\  & =[\begin{aligned}{t}^{2}\operatorname{cos}⁡t \\ 2{t}^{2} \\ {5}^{t}{t}^{2}\operatorname{ln}⁡5\end{aligned}]+[\begin{aligned}2t\operatorname{sin}⁡t \\ 4{t}^{2}-16t \\ {5}^{t}\cdot 2t\end{aligned}] \\  & =[\begin{aligned}{t}^{2}\operatorname{cos}⁡t+2t\operatorname{sin}⁡t \\ 6{t}^{2}-16t \\ {5}^{t}{t}^{2}\operatorname{ln}⁡5+{5}^{t}\cdot 2t\end{aligned}]\end{aligned}
$$

### Generated observed_q-32286 {"scales": [2, -1, 3]}

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}2 \sin{\left(t \right)}\\8 - 2 t\\3 \cdot 5^{t}\end{aligned}]$ and $u(t)={t}^{2}.$

- $[\begin{aligned}2 t^{2} \sin{\left(t \right)} - 8 t \cos{\left(t \right)}\\- 6 t^{2} + 16 t\\3 \cdot 5^{t} t^{2} \ln{\left(5 \right)} + 6 \cdot 5^{t} t\end{aligned}]$
- $[\begin{aligned}2 t^{2} \cos{\left(t \right)} + 4 t \sin{\left(t \right)}\\- t^{2} + t\\6 \cdot 5^{t} t + 3 \cdot 5^{t}\end{aligned}]$
- $[\begin{aligned}2 t^{2} \cos{\left(t \right)} + 4 t \sin{\left(t \right)}\\- 6 t^{2} + 16 t\\3 \cdot 5^{t} + 3 \ln{\left(5 \right)}\end{aligned}]$
- $[\begin{aligned}2 t^{2} \cos{\left(t \right)} + 4 t \sin{\left(t \right)}\\- 6 t^{2} + 16 t\\3 \cdot 5^{t} t^{2} \ln{\left(5 \right)} + 6 \cdot 5^{t} t\end{aligned}]$
- $[\begin{aligned}2 t^{2} \cos{\left(t \right)} + 4 t \sin{\left(t \right)}\\- 12 t^{2} - 36\\3 \cdot 5^{t} t^{2} \ln{\left(5 \right)} + 6 \cdot 5^{t} t\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 \sin{\left(t \right)})\\ \frac{\text{d}}{\text{d}t}(8 - 2 t)\\ \frac{\text{d}}{\text{d}t}(3 \cdot 5^{t})\end{aligned}]=[\begin{aligned}2 \cos{\left(t \right)}\\-2\\3 \cdot 5^{t} \ln{\left(5 \right)}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{2})=2t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & ={t}^{2}[\begin{aligned}2 \cos{\left(t \right)}\\-2\\3 \cdot 5^{t} \ln{\left(5 \right)}\end{aligned}]+2t[\begin{aligned}2 \sin{\left(t \right)}\\8 - 2 t\\3 \cdot 5^{t}\end{aligned}] \\  & =[\begin{aligned}2 t^{2} \cos{\left(t \right)}\\- 2 t^{2}\\3 \cdot 5^{t} t^{2} \ln{\left(5 \right)}\end{aligned}]+[\begin{aligned}4 t \sin{\left(t \right)}\\- 4 t^{2} + 16 t\\6 \cdot 5^{t} t\end{aligned}] \\  & =[\begin{aligned}2 t^{2} \cos{\left(t \right)} + 4 t \sin{\left(t \right)}\\- 6 t^{2} + 16 t\\3 \cdot 5^{t} t^{2} \ln{\left(5 \right)} + 6 \cdot 5^{t} t\end{aligned}]\end{aligned}
$$

### Generated observed_q-32286 {"scales": [-3, 2, -2]}

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}- 3 \sin{\left(t \right)}\\4 t - 16\\- 2 \cdot 5^{t}\end{aligned}]$ and $u(t)={t}^{2}.$

- $[\begin{aligned}- 3 t^{2} \sin{\left(t \right)} + 12 t \cos{\left(t \right)}\\12 t^{2} - 32 t\\- 2 \cdot 5^{t} t^{2} \ln{\left(5 \right)} - 4 \cdot 5^{t} t\end{aligned}]$
- $[\begin{aligned}- 3 t^{2} \cos{\left(t \right)} - 6 t \sin{\left(t \right)}\\2 t^{2} - 2 t\\- 4 \cdot 5^{t} t - 2 \cdot 5^{t}\end{aligned}]$
- $[\begin{aligned}- 3 t^{2} \cos{\left(t \right)} - 6 t \sin{\left(t \right)}\\12 t^{2} - 32 t\\- 2 \cdot 5^{t} - 2 \ln{\left(5 \right)}\end{aligned}]$
- $[\begin{aligned}- 3 t^{2} \cos{\left(t \right)} - 6 t \sin{\left(t \right)}\\12 t^{2} - 32 t\\- 2 \cdot 5^{t} t^{2} \ln{\left(5 \right)} - 4 \cdot 5^{t} t\end{aligned}]$
- $[\begin{aligned}- 3 t^{2} \cos{\left(t \right)} - 6 t \sin{\left(t \right)}\\24 t^{2} + 72\\- 2 \cdot 5^{t} t^{2} \ln{\left(5 \right)} - 4 \cdot 5^{t} t\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(- 3 \sin{\left(t \right)})\\ \frac{\text{d}}{\text{d}t}(4 t - 16)\\ \frac{\text{d}}{\text{d}t}(- 2 \cdot 5^{t})\end{aligned}]=[\begin{aligned}- 3 \cos{\left(t \right)}\\4\\- 2 \cdot 5^{t} \ln{\left(5 \right)}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{2})=2t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & ={t}^{2}[\begin{aligned}- 3 \cos{\left(t \right)}\\4\\- 2 \cdot 5^{t} \ln{\left(5 \right)}\end{aligned}]+2t[\begin{aligned}- 3 \sin{\left(t \right)}\\4 t - 16\\- 2 \cdot 5^{t}\end{aligned}] \\  & =[\begin{aligned}- 3 t^{2} \cos{\left(t \right)}\\4 t^{2}\\- 2 \cdot 5^{t} t^{2} \ln{\left(5 \right)}\end{aligned}]+[\begin{aligned}- 6 t \sin{\left(t \right)}\\8 t^{2} - 32 t\\- 4 \cdot 5^{t} t\end{aligned}] \\  & =[\begin{aligned}- 3 t^{2} \cos{\left(t \right)} - 6 t \sin{\left(t \right)}\\12 t^{2} - 32 t\\- 2 \cdot 5^{t} t^{2} \ln{\left(5 \right)} - 4 \cdot 5^{t} t\end{aligned}]\end{aligned}
$$

### Generated authored_product_errors {"scales": [2, -1, 3]}

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}2 \sin{\left(t \right)}\\8 - 2 t\\3 \cdot 5^{t}\end{aligned}]$ and $u(t)={t}^{2}.$

- $[\begin{aligned}4 t \sin{\left(t \right)} \\ - 4 t^{2} + 16 t \\ 6 \cdot 5^{t} t\end{aligned}]$
- $[\begin{aligned}2 t^{2} \cos{\left(t \right)} \\ - 2 t^{2} \\ 3 \cdot 5^{t} t^{2} \ln{\left(5 \right)}\end{aligned}]$
- $[\begin{aligned}2 t^{2} \cos{\left(t \right)} + 4 t \sin{\left(t \right)} \\ - 6 t^{2} + 16 t \\ 3 \cdot 5^{t} t^{2} \ln{\left(5 \right)} + 6 \cdot 5^{t} t\end{aligned}]$
- $[\begin{aligned}4 t \cos{\left(t \right)} \\ - 4 t \\ 6 \cdot 5^{t} t \ln{\left(5 \right)}\end{aligned}]$
- $[\begin{aligned}- 2 t^{2} \cos{\left(t \right)} + 4 t \sin{\left(t \right)} \\ - 2 t^{2} + 16 t \\ - 3 \cdot 5^{t} t^{2} \ln{\left(5 \right)} + 6 \cdot 5^{t} t\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 \sin{\left(t \right)})\\ \frac{\text{d}}{\text{d}t}(8 - 2 t)\\ \frac{\text{d}}{\text{d}t}(3 \cdot 5^{t})\end{aligned}]=[\begin{aligned}2 \cos{\left(t \right)}\\-2\\3 \cdot 5^{t} \ln{\left(5 \right)}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{2})=2t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & ={t}^{2}[\begin{aligned}2 \cos{\left(t \right)}\\-2\\3 \cdot 5^{t} \ln{\left(5 \right)}\end{aligned}]+2t[\begin{aligned}2 \sin{\left(t \right)}\\8 - 2 t\\3 \cdot 5^{t}\end{aligned}] \\  & =[\begin{aligned}2 t^{2} \cos{\left(t \right)}\\- 2 t^{2}\\3 \cdot 5^{t} t^{2} \ln{\left(5 \right)}\end{aligned}]+[\begin{aligned}4 t \sin{\left(t \right)}\\- 4 t^{2} + 16 t\\6 \cdot 5^{t} t\end{aligned}] \\  & =[\begin{aligned}2 t^{2} \cos{\left(t \right)} + 4 t \sin{\left(t \right)}\\- 6 t^{2} + 16 t\\3 \cdot 5^{t} t^{2} \ln{\left(5 \right)} + 6 \cdot 5^{t} t\end{aligned}]\end{aligned}
$$

## Original q-32501

Find $(u(t)g(t))^{′}$ where $g(t) = ⟨3t^{2}, 3 - t, 3t⟩$ and $u(t) = t^{3}$.

- $⟨15t^{4}, 9t^{2} - 4t^{3}, 12t^{3}⟩$
- $⟨6t^{4},-t^{3}, 3t^{3}⟩$
- $⟨6t,-1, 3⟩$
- $⟨3t^{2}, 3 - t, 3t⟩$
- $⟨5t^{4}, 3t^{2}, 4t^{3}⟩$

Original solution/correct designation/difficulty absent. Derived repair follows in generated records.

### Generated observed_q-32501 {"scales": [2, -1, 3]}

Find $(u(t)g(t))^{′}$ where $g(t) = ⟨6 t^{2},t - 3,9 t⟩$ and $u(t) = t^{3}$.

- $⟨12 t,1,9⟩$
- $⟨12 t^{4},t^{3},9 t^{3}⟩$
- $⟨30 t^{4},4 t^{3} - 9 t^{2},36 t^{3}⟩$
- $⟨10 t^{4},- 3 t^{2},12 t^{3}⟩$
- $⟨6 t^{2},t - 3,9 t⟩$

Using the scalar function multiple rule, we can write

$$
(u(t)g(t))^{′}=u^{′}(t)g(t)+u(t)g^{′}(t).
$$

Let's find $u^{′}(t)$ and $g^{′}(t).$

$$
\begin{aligned}g^{′}(t)&=⟨\frac{\text{d}}{\text{d}t}(6 t^{2}),\,\frac{\text{d}}{\text{d}t}(t - 3),\,\frac{\text{d}}{\text{d}t}(9 t)⟩=⟨12 t,\,1,\,9⟩\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{3})=3 t^{2}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)g(t))^{′}&=u^{′}(t)g(t)+u(t)g^{′}(t)\\&=(3 t^{2})⟨6 t^{2},\,t - 3,\,9 t⟩+(t^{3})⟨12 t,\,1,\,9⟩\\&=⟨18 t^{4},\,3 t^{2} \left(t - 3\right),\,27 t^{3}⟩+⟨12 t^{4},\,t^{3},\,9 t^{3}⟩\\&=⟨30 t^{4},\,t^{2} \left(4 t - 9\right),\,36 t^{3}⟩\end{aligned}
$$

### Generated observed_q-32501 {"scales": [-3, 2, -2]}

Find $(u(t)g(t))^{′}$ where $g(t) = ⟨- 9 t^{2},6 - 2 t,- 6 t⟩$ and $u(t) = t^{3}$.

- $⟨- 18 t,-2,-6⟩$
- $⟨- 18 t^{4},- 2 t^{3},- 6 t^{3}⟩$
- $⟨- 45 t^{4},- 8 t^{3} + 18 t^{2},- 24 t^{3}⟩$
- $⟨- 15 t^{4},6 t^{2},- 8 t^{3}⟩$
- $⟨- 9 t^{2},6 - 2 t,- 6 t⟩$

Using the scalar function multiple rule, we can write

$$
(u(t)g(t))^{′}=u^{′}(t)g(t)+u(t)g^{′}(t).
$$

Let's find $u^{′}(t)$ and $g^{′}(t).$

$$
\begin{aligned}g^{′}(t)&=⟨\frac{\text{d}}{\text{d}t}(- 9 t^{2}),\,\frac{\text{d}}{\text{d}t}(6 - 2 t),\,\frac{\text{d}}{\text{d}t}(- 6 t)⟩=⟨- 18 t,\,-2,\,-6⟩\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{3})=3 t^{2}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)g(t))^{′}&=u^{′}(t)g(t)+u(t)g^{′}(t)\\&=(3 t^{2})⟨- 9 t^{2},\,6 - 2 t,\,- 6 t⟩+(t^{3})⟨- 18 t,\,-2,\,-6⟩\\&=⟨- 27 t^{4},\,3 t^{2} \left(6 - 2 t\right),\,- 18 t^{3}⟩+⟨- 18 t^{4},\,- 2 t^{3},\,- 6 t^{3}⟩\\&=⟨- 45 t^{4},\,t^{2} \left(18 - 8 t\right),\,- 24 t^{3}⟩\end{aligned}
$$

### Generated authored_product_errors {"scales": [2, -1, 3]}

Find $(u(t)g(t))^{′}$ where $g(t) = ⟨6 t^{2},t - 3,9 t⟩$ and $u(t) = t^{3}$.

- $⟨18 t^{4},\,3 t^{3} - 9 t^{2},\,27 t^{3}⟩$
- $⟨12 t^{4},\,t^{3},\,9 t^{3}⟩$
- $⟨30 t^{4},\,4 t^{3} - 9 t^{2},\,36 t^{3}⟩$
- $⟨36 t^{3},\,3 t^{2},\,27 t^{2}⟩$
- $⟨6 t^{4},\,2 t^{3} - 9 t^{2},\,18 t^{3}⟩$

Using the scalar function multiple rule, we can write

$$
(u(t)g(t))^{′}=u^{′}(t)g(t)+u(t)g^{′}(t).
$$

Let's find $u^{′}(t)$ and $g^{′}(t).$

$$
\begin{aligned}g^{′}(t)&=⟨\frac{\text{d}}{\text{d}t}(6 t^{2}),\,\frac{\text{d}}{\text{d}t}(t - 3),\,\frac{\text{d}}{\text{d}t}(9 t)⟩=⟨12 t,\,1,\,9⟩\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{3})=3 t^{2}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)g(t))^{′}&=u^{′}(t)g(t)+u(t)g^{′}(t)\\&=(3 t^{2})⟨6 t^{2},\,t - 3,\,9 t⟩+(t^{3})⟨12 t,\,1,\,9⟩\\&=⟨18 t^{4},\,3 t^{2} \left(t - 3\right),\,27 t^{3}⟩+⟨12 t^{4},\,t^{3},\,9 t^{3}⟩\\&=⟨30 t^{4},\,t^{2} \left(4 t - 9\right),\,36 t^{3}⟩\end{aligned}
$$

## Original q-128473

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}\operatorname{sin}⁡t \\ \operatorname{tan}⁡t \\ 1\end{aligned}]$ and $u(t)=-\operatorname{cos}⁡t.$

- $[\begin{aligned}1 \\ \operatorname{sin}⁡t\operatorname{tan}⁡t \\ \operatorname{sin}⁡t\end{aligned}]$
- $[\begin{aligned}\operatorname{cos}⁡t \\ \operatorname{sin}⁡t\operatorname{tan}⁡t+\operatorname{csc}⁡t \\ 1\end{aligned}]$
- $[\begin{aligned}1 \\ \operatorname{tan}⁡t+\operatorname{sec}⁡t \\ \operatorname{cos}⁡t\end{aligned}]$
- $[\begin{aligned}-1 \\ \operatorname{sin}⁡t\operatorname{tan}⁡t+\operatorname{sec}⁡t \\ \operatorname{cot}⁡t\end{aligned}]$
- $[\begin{aligned}-\operatorname{cos}⁡2t \\ \operatorname{sin}⁡t\operatorname{tan}⁡t-\operatorname{sec}⁡t \\ \operatorname{sin}⁡t\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t).
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t) \\ \frac{\text{d}}{\text{d}t}(\operatorname{tan}⁡t) \\ \frac{\text{d}}{\text{d}t}(1)\end{aligned}]=[\begin{aligned}\operatorname{cos}⁡t \\ {sec}^{2}⁡t \\ 0\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(-\operatorname{cos}⁡t)=\operatorname{sin}⁡t\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)f(t))^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =\operatorname{sin}⁡t[\begin{aligned}\operatorname{sin}⁡t \\ \operatorname{tan}⁡t \\ 1\end{aligned}]-\operatorname{cos}⁡t[\begin{aligned}\operatorname{cos}⁡t \\ {sec}^{2}⁡t \\ 0\end{aligned}] \\  & =[\begin{aligned}{sin}^{2}⁡t \\ \operatorname{sin}⁡t\operatorname{tan}⁡t \\ \operatorname{sin}⁡t\end{aligned}]-[\begin{aligned}{cos}^{2}⁡t \\ \operatorname{sec}⁡t \\ 0\end{aligned}] \\  & =[\begin{aligned}{sin}^{2}⁡t-{cos}^{2}⁡t \\ \operatorname{sin}⁡t\operatorname{tan}⁡t-\operatorname{sec}⁡t \\ \operatorname{sin}⁡t\end{aligned}] \\  & =[\begin{aligned}-\operatorname{cos}⁡2t \\ \operatorname{sin}⁡t\operatorname{tan}⁡t-\operatorname{sec}⁡t \\ \operatorname{sin}⁡t\end{aligned}].\end{aligned}
$$

### Generated observed_q-128473 {"scales": [2, -1, 3]}

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}2 \sin{\left(t \right)}\\- \tan{\left(t \right)}\\3\end{aligned}]$ and $u(t)=-\operatorname{cos}⁡t.$

- $[\begin{aligned}2\\- \tan{\left(t \right)} - \sec{\left(t \right)}\\3 \cos{\left(t \right)}\end{aligned}]$
- $[\begin{aligned}2 \cos{\left(t \right)}\\- \sin{\left(t \right)} \tan{\left(t \right)} - \csc{\left(t \right)}\\3\end{aligned}]$
- $[\begin{aligned}2\\- \sin{\left(t \right)} \tan{\left(t \right)}\\3 \sin{\left(t \right)}\end{aligned}]$
- $[\begin{aligned}- 2 \cos{\left(2 t \right)}\\- \sin{\left(t \right)} \tan{\left(t \right)} + \sec{\left(t \right)}\\3 \sin{\left(t \right)}\end{aligned}]$
- $[\begin{aligned}-2\\- \sin{\left(t \right)} \tan{\left(t \right)} - \sec{\left(t \right)}\\3 \cot{\left(t \right)}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t).
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 \sin{\left(t \right)})\\ \frac{\text{d}}{\text{d}t}(- \tan{\left(t \right)})\\ \frac{\text{d}}{\text{d}t}(3)\end{aligned}]=[\begin{aligned}2 \cos{\left(t \right)}\\- \sec^{2}{\left(t \right)}\\0\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(-\operatorname{cos}⁡t)=\operatorname{sin}⁡t\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)f(t))^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =\operatorname{sin}⁡t[\begin{aligned}2 \sin{\left(t \right)}\\- \tan{\left(t \right)}\\3\end{aligned}]-\operatorname{cos}⁡t[\begin{aligned}2 \cos{\left(t \right)}\\- \sec^{2}{\left(t \right)}\\0\end{aligned}] \\  & =[\begin{aligned}2 \sin^{2}{\left(t \right)}\\- \sin{\left(t \right)} \tan{\left(t \right)}\\3 \sin{\left(t \right)}\end{aligned}]-[\begin{aligned}2 \cos^{2}{\left(t \right)}\\- \sec{\left(t \right)}\\0\end{aligned}] \\  & =[\begin{aligned}2 \sin^{2}{\left(t \right)} - 2 \cos^{2}{\left(t \right)}\\- \sin{\left(t \right)} \tan{\left(t \right)} + \sec{\left(t \right)}\\3 \sin{\left(t \right)}\end{aligned}] \\  & =[\begin{aligned}- 2 \cos{\left(2 t \right)}\\- \sin{\left(t \right)} \tan{\left(t \right)} + \sec{\left(t \right)}\\3 \sin{\left(t \right)}\end{aligned}].\end{aligned}
$$

### Generated observed_q-128473 {"scales": [-3, 2, -2]}

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}- 3 \sin{\left(t \right)}\\2 \tan{\left(t \right)}\\-2\end{aligned}]$ and $u(t)=-\operatorname{cos}⁡t.$

- $[\begin{aligned}-3\\2 \tan{\left(t \right)} + 2 \sec{\left(t \right)}\\- 2 \cos{\left(t \right)}\end{aligned}]$
- $[\begin{aligned}- 3 \cos{\left(t \right)}\\2 \sin{\left(t \right)} \tan{\left(t \right)} + 2 \csc{\left(t \right)}\\-2\end{aligned}]$
- $[\begin{aligned}-3\\2 \sin{\left(t \right)} \tan{\left(t \right)}\\- 2 \sin{\left(t \right)}\end{aligned}]$
- $[\begin{aligned}3 \cos{\left(2 t \right)}\\2 \sin{\left(t \right)} \tan{\left(t \right)} - 2 \sec{\left(t \right)}\\- 2 \sin{\left(t \right)}\end{aligned}]$
- $[\begin{aligned}3\\2 \sin{\left(t \right)} \tan{\left(t \right)} + 2 \sec{\left(t \right)}\\- 2 \cot{\left(t \right)}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t).
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(- 3 \sin{\left(t \right)})\\ \frac{\text{d}}{\text{d}t}(2 \tan{\left(t \right)})\\ \frac{\text{d}}{\text{d}t}(-2)\end{aligned}]=[\begin{aligned}- 3 \cos{\left(t \right)}\\2 \sec^{2}{\left(t \right)}\\0\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(-\operatorname{cos}⁡t)=\operatorname{sin}⁡t\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)f(t))^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =\operatorname{sin}⁡t[\begin{aligned}- 3 \sin{\left(t \right)}\\2 \tan{\left(t \right)}\\-2\end{aligned}]-\operatorname{cos}⁡t[\begin{aligned}- 3 \cos{\left(t \right)}\\2 \sec^{2}{\left(t \right)}\\0\end{aligned}] \\  & =[\begin{aligned}- 3 \sin^{2}{\left(t \right)}\\2 \sin{\left(t \right)} \tan{\left(t \right)}\\- 2 \sin{\left(t \right)}\end{aligned}]-[\begin{aligned}- 3 \cos^{2}{\left(t \right)}\\2 \sec{\left(t \right)}\\0\end{aligned}] \\  & =[\begin{aligned}- 3 \sin^{2}{\left(t \right)} + 3 \cos^{2}{\left(t \right)}\\2 \sin{\left(t \right)} \tan{\left(t \right)} - 2 \sec{\left(t \right)}\\- 2 \sin{\left(t \right)}\end{aligned}] \\  & =[\begin{aligned}3 \cos{\left(2 t \right)}\\2 \sin{\left(t \right)} \tan{\left(t \right)} - 2 \sec{\left(t \right)}\\- 2 \sin{\left(t \right)}\end{aligned}].\end{aligned}
$$

### Generated authored_product_errors {"scales": [2, -1, 3]}

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}2 \sin{\left(t \right)}\\- \tan{\left(t \right)}\\3\end{aligned}]$ and $u(t)=-\operatorname{cos}⁡t.$

- $[\begin{aligned}2 \sin^{2}{\left(t \right)} \\ - \sin{\left(t \right)} \tan{\left(t \right)} \\ 3 \sin{\left(t \right)}\end{aligned}]$
- $[\begin{aligned}- 2 \cos^{2}{\left(t \right)} \\ \cos{\left(t \right)} \tan^{2}{\left(t \right)} + \cos{\left(t \right)} \\ 0\end{aligned}]$
- $[\begin{aligned}2 \sin^{2}{\left(t \right)} - 2 \cos^{2}{\left(t \right)} \\ - \sin{\left(t \right)} \tan{\left(t \right)} + \cos{\left(t \right)} \tan^{2}{\left(t \right)} + \cos{\left(t \right)} \\ 3 \sin{\left(t \right)}\end{aligned}]$
- $[\begin{aligned}2 \sin^{2}{\left(t \right)} + 2 \cos{\left(t \right)} \\ - \sin{\left(t \right)} \tan{\left(t \right)} - \tan^{2}{\left(t \right)} - 1 \\ 3 \sin{\left(t \right)}\end{aligned}]$
- $[\begin{aligned}2 \sin^{2}{\left(t \right)} + 2 \cos^{2}{\left(t \right)} \\ - \sin{\left(t \right)} \tan{\left(t \right)} - \cos{\left(t \right)} \tan^{2}{\left(t \right)} - \cos{\left(t \right)} \\ 3 \sin{\left(t \right)}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t).
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 \sin{\left(t \right)})\\ \frac{\text{d}}{\text{d}t}(- \tan{\left(t \right)})\\ \frac{\text{d}}{\text{d}t}(3)\end{aligned}]=[\begin{aligned}2 \cos{\left(t \right)}\\- \sec^{2}{\left(t \right)}\\0\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(-\operatorname{cos}⁡t)=\operatorname{sin}⁡t\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)f(t))^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =\operatorname{sin}⁡t[\begin{aligned}2 \sin{\left(t \right)}\\- \tan{\left(t \right)}\\3\end{aligned}]-\operatorname{cos}⁡t[\begin{aligned}2 \cos{\left(t \right)}\\- \sec^{2}{\left(t \right)}\\0\end{aligned}] \\  & =[\begin{aligned}2 \sin^{2}{\left(t \right)}\\- \sin{\left(t \right)} \tan{\left(t \right)}\\3 \sin{\left(t \right)}\end{aligned}]-[\begin{aligned}2 \cos^{2}{\left(t \right)}\\- \sec{\left(t \right)}\\0\end{aligned}] \\  & =[\begin{aligned}2 \sin^{2}{\left(t \right)} - 2 \cos^{2}{\left(t \right)}\\- \sin{\left(t \right)} \tan{\left(t \right)} + \sec{\left(t \right)}\\3 \sin{\left(t \right)}\end{aligned}] \\  & =[\begin{aligned}- 2 \cos{\left(2 t \right)}\\- \sin{\left(t \right)} \tan{\left(t \right)} + \sec{\left(t \right)}\\3 \sin{\left(t \right)}\end{aligned}].\end{aligned}
$$

## Original q-128477

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨\sqrt{t},\,{t}^{2},\,t⟩$ and $u(t)=2\sqrt{t}.$

- $⟨2,\,5t\sqrt{t},\,3\sqrt{t}⟩$
- $⟨{t}^{2},\,5\sqrt{t},\,3{t}^{2}\sqrt{t}⟩$
- $⟨\frac{1}{\sqrt{t}},\,5t\sqrt{t},\,3\sqrt{t}⟩$
- $⟨2t,\,\sqrt{t},\,\sqrt{t}⟩$
- $⟨1,\,2t\sqrt{t},\,\sqrt{t}⟩$

By the scalar function multiple rule, we have
 

$$
(u(t)g(t))^{′}=u(t){g}^{′}(t)+{u}^{′}(t)g(t).
$$

Let's find ${u}^{′}(t)$ and ${g}^{′}(t).$ 

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(\sqrt{t}),\,\frac{\text{d}}{\text{d}t}({t}^{2}),\,\frac{\text{d}}{\text{d}t}(t)⟩ \\  & =⟨\frac{1}{2\sqrt{t}},\,2t,\,1⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2\sqrt{t}) \\  & =\frac{1}{\sqrt{t}}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)g(t))^{′} & =u(t){g}^{′}(t)+{u}^{′}(t)g(t) \\  & =2\sqrt{t}⟨\frac{1}{2\sqrt{t}},\,2t,\,1⟩+\frac{1}{\sqrt{t}}⟨\sqrt{t},\,{t}^{2},\,t⟩ \\  & =⟨1,\,4t\sqrt{t},\,2\sqrt{t}⟩+⟨1,\,t\sqrt{t},\,\sqrt{t}⟩ \\  & =⟨2,\,5t\sqrt{t},\,3\sqrt{t}⟩.\end{aligned}
$$

### Generated observed_q-128477 {"scales": [2, -1, 3]}

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨2 \sqrt{t},- t^{2},3 t⟩$ and $u(t)=2\sqrt{t}.$

- $⟨\frac{2}{\sqrt{t}},- 5 t^{\frac{3}{2}},9 \sqrt{t}⟩$
- $⟨2 t^{2},- 5 \sqrt{t},9 t^{\frac{5}{2}}⟩$
- $⟨4,- 5 t^{\frac{3}{2}},9 \sqrt{t}⟩$
- $⟨2,- 2 t^{\frac{3}{2}},3 \sqrt{t}⟩$
- $⟨4 t,- \sqrt{t},3 \sqrt{t}⟩$

By the scalar function multiple rule, we have
 

$$
(u(t)g(t))^{′}=u(t){g}^{′}(t)+{u}^{′}(t)g(t).
$$

Let's find ${u}^{′}(t)$ and ${g}^{′}(t).$ 

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 \sqrt{t}),\,\frac{\text{d}}{\text{d}t}(- t^{2}),\,\frac{\text{d}}{\text{d}t}(3 t)⟩ \\  & =⟨\frac{1}{\sqrt{t}},- 2 t,3⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2\sqrt{t}) \\  & =\frac{1}{\sqrt{t}}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)g(t))^{′} & =u(t){g}^{′}(t)+{u}^{′}(t)g(t) \\  & =2\sqrt{t}⟨\frac{1}{\sqrt{t}},- 2 t,3⟩+\frac{1}{\sqrt{t}}⟨2 \sqrt{t},- t^{2},3 t⟩ \\  & =⟨2,- 4 t^{\frac{3}{2}},6 \sqrt{t}⟩+⟨2,- t^{\frac{3}{2}},3 \sqrt{t}⟩ \\  & =⟨4,- 5 t^{\frac{3}{2}},9 \sqrt{t}⟩.\end{aligned}
$$

### Generated observed_q-128477 {"scales": [-3, 2, -2]}

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨- 3 \sqrt{t},2 t^{2},- 2 t⟩$ and $u(t)=2\sqrt{t}.$

- $⟨- \frac{3}{\sqrt{t}},10 t^{\frac{3}{2}},- 6 \sqrt{t}⟩$
- $⟨- 3 t^{2},10 \sqrt{t},- 6 t^{\frac{5}{2}}⟩$
- $⟨-6,10 t^{\frac{3}{2}},- 6 \sqrt{t}⟩$
- $⟨-3,4 t^{\frac{3}{2}},- 2 \sqrt{t}⟩$
- $⟨- 6 t,2 \sqrt{t},- 2 \sqrt{t}⟩$

By the scalar function multiple rule, we have
 

$$
(u(t)g(t))^{′}=u(t){g}^{′}(t)+{u}^{′}(t)g(t).
$$

Let's find ${u}^{′}(t)$ and ${g}^{′}(t).$ 

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 3 \sqrt{t}),\,\frac{\text{d}}{\text{d}t}(2 t^{2}),\,\frac{\text{d}}{\text{d}t}(- 2 t)⟩ \\  & =⟨- \frac{3}{2 \sqrt{t}},4 t,-2⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2\sqrt{t}) \\  & =\frac{1}{\sqrt{t}}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)g(t))^{′} & =u(t){g}^{′}(t)+{u}^{′}(t)g(t) \\  & =2\sqrt{t}⟨- \frac{3}{2 \sqrt{t}},4 t,-2⟩+\frac{1}{\sqrt{t}}⟨- 3 \sqrt{t},2 t^{2},- 2 t⟩ \\  & =⟨-3,8 t^{\frac{3}{2}},- 4 \sqrt{t}⟩+⟨-3,2 t^{\frac{3}{2}},- 2 \sqrt{t}⟩ \\  & =⟨-6,10 t^{\frac{3}{2}},- 6 \sqrt{t}⟩.\end{aligned}
$$

### Generated authored_product_errors {"scales": [2, -1, 3]}

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨2 \sqrt{t},- t^{2},3 t⟩$ and $u(t)=2\sqrt{t}.$

- $⟨2,\,- t^{\frac{3}{2}},\,3 \sqrt{t}⟩$
- $⟨2,\,- 4 t^{\frac{3}{2}},\,6 \sqrt{t}⟩$
- $⟨4,\,- 5 t^{\frac{3}{2}},\,9 \sqrt{t}⟩$
- $⟨\frac{1}{t},\,- 2 \sqrt{t},\,\frac{3}{\sqrt{t}}⟩$
- $⟨0,\,3 t^{\frac{3}{2}},\,- 3 \sqrt{t}⟩$

By the scalar function multiple rule, we have
 

$$
(u(t)g(t))^{′}=u(t){g}^{′}(t)+{u}^{′}(t)g(t).
$$

Let's find ${u}^{′}(t)$ and ${g}^{′}(t).$ 

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 \sqrt{t}),\,\frac{\text{d}}{\text{d}t}(- t^{2}),\,\frac{\text{d}}{\text{d}t}(3 t)⟩ \\  & =⟨\frac{1}{\sqrt{t}},- 2 t,3⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2\sqrt{t}) \\  & =\frac{1}{\sqrt{t}}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)g(t))^{′} & =u(t){g}^{′}(t)+{u}^{′}(t)g(t) \\  & =2\sqrt{t}⟨\frac{1}{\sqrt{t}},- 2 t,3⟩+\frac{1}{\sqrt{t}}⟨2 \sqrt{t},- t^{2},3 t⟩ \\  & =⟨2,- 4 t^{\frac{3}{2}},6 \sqrt{t}⟩+⟨2,- t^{\frac{3}{2}},3 \sqrt{t}⟩ \\  & =⟨4,- 5 t^{\frac{3}{2}},9 \sqrt{t}⟩.\end{aligned}
$$

## Original q-128479

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨t,\,1+t,\,{t}^{2}⟩$ and $u(t)=1-t.$

- $⟨t-2,\,-t,\,t-2{t}^{2}⟩$
- $⟨1+t,\,2+t,\,t+3{t}^{2}⟩$
- $⟨1-2t,\,-1,\,2t-3{t}^{2}⟩$
- $⟨1-2t,\,-2t,\,2t-3{t}^{2}⟩$
- $⟨t,\,-2{t}^{2},\,2t-3{t}^{2}⟩$

By the scalar function multiple rule, we have

$$
(u(t)g(t))^{′}=u(t){g}^{′}(t)+{u}^{′}(t)g(t).
$$

Let's find ${u}^{′}(t)$ and ${g}^{′}(t).$ 

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t),\,\frac{\text{d}}{\text{d}t}(1+t),\,\frac{\text{d}}{\text{d}t}({t}^{2})⟩ \\  & =⟨1,\,1,\,2t⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(1-t) \\  & =-1\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)g(t))^{′} & =u(t){g}^{′}(t)+{u}^{′}(t)g(t) \\  & =(1-t)⟨1,\,1,\,2t⟩-⟨t,\,1+t,\,{t}^{2}⟩ \\  & =⟨1-t,\,1-t,\,2t-2{t}^{2}⟩-⟨t,\,1+t,\,{t}^{2}⟩ \\  & =⟨1-2t,\,-2t,\,2t-3{t}^{2}⟩.\end{aligned}
$$

### Generated observed_q-128479 {"scales": [2, -1, 3]}

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨2 t,- t - 1,3 t^{2}⟩$ and $u(t)=1-t.$

- $⟨2 - 4 t,1,- 9 t^{2} + 6 t⟩$
- $⟨2 t + 2,- t - 2,9 t^{2} + 3 t⟩$
- $⟨2 t - 4,t,- 6 t^{2} + 3 t⟩$
- $⟨2 t,2 t^{2},- 9 t^{2} + 6 t⟩$
- $⟨2 - 4 t,2 t,- 9 t^{2} + 6 t⟩$

By the scalar function multiple rule, we have

$$
(u(t)g(t))^{′}=u(t){g}^{′}(t)+{u}^{′}(t)g(t).
$$

Let's find ${u}^{′}(t)$ and ${g}^{′}(t).$ 

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 t),\,\frac{\text{d}}{\text{d}t}(- t - 1),\,\frac{\text{d}}{\text{d}t}(3 t^{2})⟩ \\  & =⟨2,-1,6 t⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(1-t) \\  & =-1\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)g(t))^{′} & =u(t){g}^{′}(t)+{u}^{′}(t)g(t) \\  & =(1-t)⟨2,-1,6 t⟩-⟨2 t,- t - 1,3 t^{2}⟩ \\  & =⟨2 - 2 t,t - 1,- 6 t^{2} + 6 t⟩-⟨2 t,- t - 1,3 t^{2}⟩ \\  & =⟨2 - 4 t,2 t,- 9 t^{2} + 6 t⟩.\end{aligned}
$$

### Generated observed_q-128479 {"scales": [-3, 2, -2]}

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨- 3 t,2 t + 2,- 2 t^{2}⟩$ and $u(t)=1-t.$

- $⟨6 t - 3,-2,6 t^{2} - 4 t⟩$
- $⟨- 3 t - 3,2 t + 4,- 6 t^{2} - 2 t⟩$
- $⟨6 - 3 t,- 2 t,4 t^{2} - 2 t⟩$
- $⟨- 3 t,- 4 t^{2},6 t^{2} - 4 t⟩$
- $⟨6 t - 3,- 4 t,6 t^{2} - 4 t⟩$

By the scalar function multiple rule, we have

$$
(u(t)g(t))^{′}=u(t){g}^{′}(t)+{u}^{′}(t)g(t).
$$

Let's find ${u}^{′}(t)$ and ${g}^{′}(t).$ 

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 3 t),\,\frac{\text{d}}{\text{d}t}(2 t + 2),\,\frac{\text{d}}{\text{d}t}(- 2 t^{2})⟩ \\  & =⟨-3,2,- 4 t⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(1-t) \\  & =-1\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)g(t))^{′} & =u(t){g}^{′}(t)+{u}^{′}(t)g(t) \\  & =(1-t)⟨-3,2,- 4 t⟩-⟨- 3 t,2 t + 2,- 2 t^{2}⟩ \\  & =⟨3 t - 3,2 - 2 t,4 t^{2} - 4 t⟩-⟨- 3 t,2 t + 2,- 2 t^{2}⟩ \\  & =⟨6 t - 3,- 4 t,6 t^{2} - 4 t⟩.\end{aligned}
$$

### Generated authored_product_errors {"scales": [2, -1, 3]}

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨2 t,- t - 1,3 t^{2}⟩$ and $u(t)=1-t.$

- $⟨- 2 t,\,t + 1,\,- 3 t^{2}⟩$
- $⟨2 - 2 t,\,t - 1,\,- 6 t^{2} + 6 t⟩$
- $⟨2 - 4 t,\,2 t,\,- 9 t^{2} + 6 t⟩$
- $⟨-2,\,1,\,- 6 t⟩$
- $⟨-2,\,2,\,3 t^{2} - 6 t⟩$

By the scalar function multiple rule, we have

$$
(u(t)g(t))^{′}=u(t){g}^{′}(t)+{u}^{′}(t)g(t).
$$

Let's find ${u}^{′}(t)$ and ${g}^{′}(t).$ 

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 t),\,\frac{\text{d}}{\text{d}t}(- t - 1),\,\frac{\text{d}}{\text{d}t}(3 t^{2})⟩ \\  & =⟨2,-1,6 t⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(1-t) \\  & =-1\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)g(t))^{′} & =u(t){g}^{′}(t)+{u}^{′}(t)g(t) \\  & =(1-t)⟨2,-1,6 t⟩-⟨2 t,- t - 1,3 t^{2}⟩ \\  & =⟨2 - 2 t,t - 1,- 6 t^{2} + 6 t⟩-⟨2 t,- t - 1,3 t^{2}⟩ \\  & =⟨2 - 4 t,2 t,- 9 t^{2} + 6 t⟩.\end{aligned}
$$

## Original q-128481

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨4\sqrt{t},\,{t}^{3},\,t+{t}^{2}⟩$ and $u(t)=2t.$

- $⟨12\sqrt{t},\,8{t}^{3}+2t,\,4{t}^{2}+6{t}^{3}⟩$
- $⟨6\sqrt{t},\,{t}^{3},\,t+6{t}^{2}⟩$
- $⟨12\sqrt{t},\,8{t}^{3},\,4t+6{t}^{2}⟩$
- $⟨6\sqrt{t},\,2{t}^{2},\,10{t}^{2}⟩$
- $⟨5\sqrt{t},\,4{t}^{3},\,3t+6{t}^{2}⟩$

By the scalar function multiple rule, we have
 

$$
(u(t)g(t))^{′}=u(t){g}^{′}(t)+{u}^{′}(t)g(t).
$$

Let's find ${u}^{′}(t)$ and ${g}^{′}(t).$ 

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(4\sqrt{t}),\,\frac{\text{d}}{\text{d}t}({t}^{3}),\,\frac{\text{d}}{\text{d}t}(t+{t}^{2})⟩ \\  & =⟨\frac{2}{\sqrt{t}},\,3{t}^{2},\,1+2t⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2t) \\  & =2\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)g(t))^{′} & =u(t){g}^{′}(t)+{u}^{′}(t)g(t) \\  & =2t⟨\frac{2}{\sqrt{t}},\,3{t}^{2},\,1+2t⟩+2⟨4\sqrt{t},\,{t}^{3},\,t+{t}^{2}⟩ \\  & =⟨4\sqrt{t},\,6{t}^{3},\,2t+4{t}^{2}⟩+⟨8\sqrt{t},\,2{t}^{3},\,2t+2{t}^{2}⟩ \\  & =⟨12\sqrt{t},\,8{t}^{3},\,4t+6{t}^{2}⟩.\end{aligned}
$$

### Generated observed_q-128481 {"scales": [2, -1, 3]}

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨8 \sqrt{t},- t^{3},3 t^{2} + 3 t⟩$ and $u(t)=2t.$

- $⟨24 \sqrt{t},- 8 t^{3},18 t^{2} + 12 t⟩$
- $⟨12 \sqrt{t},- t^{3},18 t^{2} + 3 t⟩$
- $⟨24 \sqrt{t},- 8 t^{3} - 2 t,18 t^{3} + 12 t^{2}⟩$
- $⟨10 \sqrt{t},- 4 t^{3},18 t^{2} + 9 t⟩$
- $⟨12 \sqrt{t},- 2 t^{2},30 t^{2}⟩$

By the scalar function multiple rule, we have
 

$$
(u(t)g(t))^{′}=u(t){g}^{′}(t)+{u}^{′}(t)g(t).
$$

Let's find ${u}^{′}(t)$ and ${g}^{′}(t).$ 

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(8 \sqrt{t}),\,\frac{\text{d}}{\text{d}t}(- t^{3}),\,\frac{\text{d}}{\text{d}t}(3 t^{2} + 3 t)⟩ \\  & =⟨\frac{4}{\sqrt{t}},- 3 t^{2},6 t + 3⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2t) \\  & =2\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)g(t))^{′} & =u(t){g}^{′}(t)+{u}^{′}(t)g(t) \\  & =2t⟨\frac{4}{\sqrt{t}},- 3 t^{2},6 t + 3⟩+2⟨8 \sqrt{t},- t^{3},3 t^{2} + 3 t⟩ \\  & =⟨8 \sqrt{t},- 6 t^{3},12 t^{2} + 6 t⟩+⟨16 \sqrt{t},- 2 t^{3},6 t^{2} + 6 t⟩ \\  & =⟨24 \sqrt{t},- 8 t^{3},18 t^{2} + 12 t⟩.\end{aligned}
$$

### Generated observed_q-128481 {"scales": [-3, 2, -2]}

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨- 12 \sqrt{t},2 t^{3},- 2 t^{2} - 2 t⟩$ and $u(t)=2t.$

- $⟨- 36 \sqrt{t},16 t^{3},- 12 t^{2} - 8 t⟩$
- $⟨- 18 \sqrt{t},2 t^{3},- 12 t^{2} - 2 t⟩$
- $⟨- 36 \sqrt{t},16 t^{3} + 4 t,- 12 t^{3} - 8 t^{2}⟩$
- $⟨- 15 \sqrt{t},8 t^{3},- 12 t^{2} - 6 t⟩$
- $⟨- 18 \sqrt{t},4 t^{2},- 20 t^{2}⟩$

By the scalar function multiple rule, we have
 

$$
(u(t)g(t))^{′}=u(t){g}^{′}(t)+{u}^{′}(t)g(t).
$$

Let's find ${u}^{′}(t)$ and ${g}^{′}(t).$ 

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 12 \sqrt{t}),\,\frac{\text{d}}{\text{d}t}(2 t^{3}),\,\frac{\text{d}}{\text{d}t}(- 2 t^{2} - 2 t)⟩ \\  & =⟨- \frac{6}{\sqrt{t}},6 t^{2},- 4 t - 2⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2t) \\  & =2\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)g(t))^{′} & =u(t){g}^{′}(t)+{u}^{′}(t)g(t) \\  & =2t⟨- \frac{6}{\sqrt{t}},6 t^{2},- 4 t - 2⟩+2⟨- 12 \sqrt{t},2 t^{3},- 2 t^{2} - 2 t⟩ \\  & =⟨- 12 \sqrt{t},12 t^{3},- 8 t^{2} - 4 t⟩+⟨- 24 \sqrt{t},4 t^{3},- 4 t^{2} - 4 t⟩ \\  & =⟨- 36 \sqrt{t},16 t^{3},- 12 t^{2} - 8 t⟩.\end{aligned}
$$

### Generated authored_product_errors {"scales": [2, -1, 3]}

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨8 \sqrt{t},- t^{3},3 t^{2} + 3 t⟩$ and $u(t)=2t.$

- $⟨16 \sqrt{t},\,- 2 t^{3},\,6 t^{2} + 6 t⟩$
- $⟨8 \sqrt{t},\,- 6 t^{3},\,12 t^{2} + 6 t⟩$
- $⟨24 \sqrt{t},\,- 8 t^{3},\,18 t^{2} + 12 t⟩$
- $⟨\frac{8}{\sqrt{t}},\,- 6 t^{2},\,12 t + 6⟩$
- $⟨8 \sqrt{t},\,4 t^{3},\,- 6 t^{2}⟩$

By the scalar function multiple rule, we have
 

$$
(u(t)g(t))^{′}=u(t){g}^{′}(t)+{u}^{′}(t)g(t).
$$

Let's find ${u}^{′}(t)$ and ${g}^{′}(t).$ 

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(8 \sqrt{t}),\,\frac{\text{d}}{\text{d}t}(- t^{3}),\,\frac{\text{d}}{\text{d}t}(3 t^{2} + 3 t)⟩ \\  & =⟨\frac{4}{\sqrt{t}},- 3 t^{2},6 t + 3⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2t) \\  & =2\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)g(t))^{′} & =u(t){g}^{′}(t)+{u}^{′}(t)g(t) \\  & =2t⟨\frac{4}{\sqrt{t}},- 3 t^{2},6 t + 3⟩+2⟨8 \sqrt{t},- t^{3},3 t^{2} + 3 t⟩ \\  & =⟨8 \sqrt{t},- 6 t^{3},12 t^{2} + 6 t⟩+⟨16 \sqrt{t},- 2 t^{3},6 t^{2} + 6 t⟩ \\  & =⟨24 \sqrt{t},- 8 t^{3},18 t^{2} + 12 t⟩.\end{aligned}
$$

## Original q-128485

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨2{e}^{-t},\,4\operatorname{ln}⁡t,\,2⟩$ and $u(t)=\frac{1}{2}{t}^{2}.$

- $⟨{e}^{-t},\,2\operatorname{ln}⁡t,\,2t-1⟩$
- $⟨t{e}^{-t},\,1+2\operatorname{ln}⁡t,\,2t⟩$
- $⟨{t}^{2}{e}^{-t},\,{t}^{2}(1+2\operatorname{ln}⁡t),\,1⟩$
- $⟨t{e}^{-t}(2-t),\,2t(1+2\operatorname{ln}⁡t),\,2t⟩$
- $⟨2-t,\,2(1+2\operatorname{ln}⁡t),\,t⟩$

By the scalar function multiple rule, we have

$$
(u(t)g(t))^{′}=u(t){g}^{′}(t)+{u}^{′}(t)g(t).
$$

Let's find ${u}^{′}(t)$ and ${g}^{′}(t).$ 

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2{e}^{-t}),\,\frac{\text{d}}{\text{d}t}(4\operatorname{ln}⁡t),\,\frac{\text{d}}{\text{d}t}(2)⟩ \\  & =⟨-2{e}^{-t},\,\frac{4}{t},\,0⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\frac{1}{2}{t}^{2}) \\  & =t\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)g(t))^{′} & =u(t){g}^{′}(t)+{u}^{′}(t)g(t) \\  & =\frac{1}{2}{t}^{2}⟨-2{e}^{-t},\,\frac{4}{t},\,0⟩+t⟨2{e}^{-t},\,4\operatorname{ln}⁡t,\,2⟩ \\  & =⟨-{t}^{2}{e}^{-t},\,2t,\,0⟩+⟨2t{e}^{-t},\,4t\operatorname{ln}⁡t,\,2t⟩ \\  & =⟨2t{e}^{-t}-{t}^{2}{e}^{-t},\,2t+4t\operatorname{ln}⁡t,\,2t⟩ \\  & =⟨t{e}^{-t}(2-t),\,2t(1+2\operatorname{ln}⁡t),\,2t⟩.\end{aligned}
$$

### Generated observed_q-128485 {"scales": [2, -1, 3]}

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨4 e^{- t},- 4 \ln{\left(t \right)},6⟩$ and $u(t)=\frac{1}{2}{t}^{2}.$

- $⟨2 t^{2} e^{- t},- t^{2} \left(2 \ln{\left(t \right)} + 1\right),3⟩$
- $⟨2 t e^{- t},- 2 \ln{\left(t \right)} - 1,6 t⟩$
- $⟨2 e^{- t},- 2 \ln{\left(t \right)},6 t - 3⟩$
- $⟨4 - 2 t,- 4 \ln{\left(t \right)} - 2,3 t⟩$
- $⟨2 t \left(2 - t\right) e^{- t},- 2 t \left(2 \ln{\left(t \right)} + 1\right),6 t⟩$

By the scalar function multiple rule, we have

$$
(u(t)g(t))^{′}=u(t){g}^{′}(t)+{u}^{′}(t)g(t).
$$

Let's find ${u}^{′}(t)$ and ${g}^{′}(t).$ 

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(4 e^{- t}),\,\frac{\text{d}}{\text{d}t}(- 4 \ln{\left(t \right)}),\,\frac{\text{d}}{\text{d}t}(6)⟩ \\  & =⟨- 4 e^{- t},- \frac{4}{t},0⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\frac{1}{2}{t}^{2}) \\  & =t\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)g(t))^{′} & =u(t){g}^{′}(t)+{u}^{′}(t)g(t) \\  & =\frac{1}{2}{t}^{2}⟨- 4 e^{- t},- \frac{4}{t},0⟩+t⟨4 e^{- t},- 4 \ln{\left(t \right)},6⟩ \\  & =⟨- 2 t^{2} e^{- t},- 2 t,0⟩+⟨4 t e^{- t},- 4 t \ln{\left(t \right)},6 t⟩ \\  & =⟨- 2 t^{2} e^{- t} + 4 t e^{- t},- 4 t \ln{\left(t \right)} - 2 t,6 t⟩ \\  & =⟨2 t \left(2 - t\right) e^{- t},- 2 t \left(2 \ln{\left(t \right)} + 1\right),6 t⟩.\end{aligned}
$$

### Generated observed_q-128485 {"scales": [-3, 2, -2]}

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨- 6 e^{- t},8 \ln{\left(t \right)},-4⟩$ and $u(t)=\frac{1}{2}{t}^{2}.$

- $⟨- 3 t^{2} e^{- t},2 t^{2} \left(2 \ln{\left(t \right)} + 1\right),-2⟩$
- $⟨- 3 t e^{- t},4 \ln{\left(t \right)} + 2,- 4 t⟩$
- $⟨- 3 e^{- t},4 \ln{\left(t \right)},2 - 4 t⟩$
- $⟨3 t - 6,8 \ln{\left(t \right)} + 4,- 2 t⟩$
- $⟨- 3 t \left(2 - t\right) e^{- t},4 t \left(2 \ln{\left(t \right)} + 1\right),- 4 t⟩$

By the scalar function multiple rule, we have

$$
(u(t)g(t))^{′}=u(t){g}^{′}(t)+{u}^{′}(t)g(t).
$$

Let's find ${u}^{′}(t)$ and ${g}^{′}(t).$ 

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 6 e^{- t}),\,\frac{\text{d}}{\text{d}t}(8 \ln{\left(t \right)}),\,\frac{\text{d}}{\text{d}t}(-4)⟩ \\  & =⟨6 e^{- t},\frac{8}{t},0⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\frac{1}{2}{t}^{2}) \\  & =t\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)g(t))^{′} & =u(t){g}^{′}(t)+{u}^{′}(t)g(t) \\  & =\frac{1}{2}{t}^{2}⟨6 e^{- t},\frac{8}{t},0⟩+t⟨- 6 e^{- t},8 \ln{\left(t \right)},-4⟩ \\  & =⟨3 t^{2} e^{- t},4 t,0⟩+⟨- 6 t e^{- t},8 t \ln{\left(t \right)},- 4 t⟩ \\  & =⟨3 t^{2} e^{- t} - 6 t e^{- t},8 t \ln{\left(t \right)} + 4 t,- 4 t⟩ \\  & =⟨- 3 t \left(2 - t\right) e^{- t},4 t \left(2 \ln{\left(t \right)} + 1\right),- 4 t⟩.\end{aligned}
$$

### Generated authored_product_errors {"scales": [2, -1, 3]}

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨4 e^{- t},- 4 \ln{\left(t \right)},6⟩$ and $u(t)=\frac{1}{2}{t}^{2}.$

- $⟨4 t e^{- t},\,- 4 t \ln{\left(t \right)},\,6 t⟩$
- $⟨- 2 t^{2} e^{- t},\,- 2 t,\,0⟩$
- $⟨- 2 t^{2} e^{- t} + 4 t e^{- t},\,- 4 t \ln{\left(t \right)} - 2 t,\,6 t⟩$
- $⟨- 4 t e^{- t},\,-4,\,0⟩$
- $⟨2 t^{2} e^{- t} + 4 t e^{- t},\,- 4 t \ln{\left(t \right)} + 2 t,\,6 t⟩$

By the scalar function multiple rule, we have

$$
(u(t)g(t))^{′}=u(t){g}^{′}(t)+{u}^{′}(t)g(t).
$$

Let's find ${u}^{′}(t)$ and ${g}^{′}(t).$ 

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(4 e^{- t}),\,\frac{\text{d}}{\text{d}t}(- 4 \ln{\left(t \right)}),\,\frac{\text{d}}{\text{d}t}(6)⟩ \\  & =⟨- 4 e^{- t},- \frac{4}{t},0⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\frac{1}{2}{t}^{2}) \\  & =t\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)g(t))^{′} & =u(t){g}^{′}(t)+{u}^{′}(t)g(t) \\  & =\frac{1}{2}{t}^{2}⟨- 4 e^{- t},- \frac{4}{t},0⟩+t⟨4 e^{- t},- 4 \ln{\left(t \right)},6⟩ \\  & =⟨- 2 t^{2} e^{- t},- 2 t,0⟩+⟨4 t e^{- t},- 4 t \ln{\left(t \right)},6 t⟩ \\  & =⟨- 2 t^{2} e^{- t} + 4 t e^{- t},- 4 t \ln{\left(t \right)} - 2 t,6 t⟩ \\  & =⟨2 t \left(2 - t\right) e^{- t},- 2 t \left(2 \ln{\left(t \right)} + 1\right),6 t⟩.\end{aligned}
$$

## Original q-70685

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}t \\ {t}^{2} \\ {t}^{3}\end{aligned}]$ and $u(t)=\operatorname{ln}⁡t.$

- $[\begin{aligned}1+\operatorname{ln}⁡t \\ t+2t\operatorname{ln}⁡t \\ {t}^{2}+3{t}^{2}\operatorname{ln}⁡t\end{aligned}]$
- $[\begin{aligned}\frac{1}{t}+\operatorname{ln}⁡t \\ \frac{2}{{t}^{2}}+2t\operatorname{ln}⁡t \\ \frac{3}{{t}^{3}}+3{t}^{2}\operatorname{ln}⁡t\end{aligned}]$
- $[\begin{aligned}\operatorname{ln}⁡t \\ 3t\operatorname{ln}⁡t \\ 4{t}^{2}\operatorname{ln}⁡t\end{aligned}]$
- $[\begin{aligned}t+\frac{1}{t} \\ {t}^{2}+2 \\ {t}^{3}+3t\end{aligned}]$
- $[\begin{aligned}t+\operatorname{ln}⁡t \\ {t}^{2}+2t\operatorname{ln}⁡t \\ {t}^{3}+3{t}^{2}\operatorname{ln}⁡t\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(t) \\ \frac{\text{d}}{\text{d}t}({t}^{2}) \\ \frac{\text{d}}{\text{d}t}({t}^{3})\end{aligned}]=[\begin{aligned}1 \\ 2t \\ 3{t}^{2}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡t)=\frac{1}{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =\frac{1}{t}[\begin{aligned}t \\ {t}^{2} \\ {t}^{3}\end{aligned}]+\operatorname{ln}⁡t[\begin{aligned}1 \\ 2t \\ 3{t}^{2}\end{aligned}] \\  & =[\begin{aligned}1 \\ t \\ {t}^{2}\end{aligned}]+[\begin{aligned}\operatorname{ln}⁡t \\ 2t\operatorname{ln}⁡t \\ 3{t}^{2}\operatorname{ln}⁡t\end{aligned}] \\  & =[\begin{aligned}1+\operatorname{ln}⁡t \\ t+2t\operatorname{ln}⁡t \\ {t}^{2}+3{t}^{2}\operatorname{ln}⁡t\end{aligned}]\end{aligned}
$$

### Generated observed_q-70685 {"scales": [2, -1, 3]}

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}2 t\\- t^{2}\\3 t^{3}\end{aligned}]$ and $u(t)=\operatorname{ln}⁡t.$

- $[\begin{aligned}2 \ln{\left(t \right)}\\- 3 t \ln{\left(t \right)}\\12 t^{2} \ln{\left(t \right)}\end{aligned}]$
- $[\begin{aligned}2 \ln{\left(t \right)} + \frac{2}{t}\\- 2 t \ln{\left(t \right)} - \frac{2}{t^{2}}\\9 t^{2} \ln{\left(t \right)} + \frac{9}{t^{3}}\end{aligned}]$
- $[\begin{aligned}2 \ln{\left(t \right)} + 2\\- 2 t \ln{\left(t \right)} - t\\9 t^{2} \ln{\left(t \right)} + 3 t^{2}\end{aligned}]$
- $[\begin{aligned}2 t + 2 \ln{\left(t \right)}\\- t^{2} - 2 t \ln{\left(t \right)}\\3 t^{3} + 9 t^{2} \ln{\left(t \right)}\end{aligned}]$
- $[\begin{aligned}2 t + \frac{2}{t}\\- t^{2} - 2\\3 t^{3} + 9 t\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 t)\\ \frac{\text{d}}{\text{d}t}(- t^{2})\\ \frac{\text{d}}{\text{d}t}(3 t^{3})\end{aligned}]=[\begin{aligned}2\\- 2 t\\9 t^{2}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡t)=\frac{1}{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =\frac{1}{t}[\begin{aligned}2 t\\- t^{2}\\3 t^{3}\end{aligned}]+\operatorname{ln}⁡t[\begin{aligned}2\\- 2 t\\9 t^{2}\end{aligned}] \\  & =[\begin{aligned}2\\- t\\3 t^{2}\end{aligned}]+[\begin{aligned}2 \ln{\left(t \right)}\\- 2 t \ln{\left(t \right)}\\9 t^{2} \ln{\left(t \right)}\end{aligned}] \\  & =[\begin{aligned}2 \ln{\left(t \right)} + 2\\- 2 t \ln{\left(t \right)} - t\\9 t^{2} \ln{\left(t \right)} + 3 t^{2}\end{aligned}]\end{aligned}
$$

### Generated observed_q-70685 {"scales": [-3, 2, -2]}

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}- 3 t\\2 t^{2}\\- 2 t^{3}\end{aligned}]$ and $u(t)=\operatorname{ln}⁡t.$

- $[\begin{aligned}- 3 \ln{\left(t \right)}\\6 t \ln{\left(t \right)}\\- 8 t^{2} \ln{\left(t \right)}\end{aligned}]$
- $[\begin{aligned}- 3 \ln{\left(t \right)} - \frac{3}{t}\\4 t \ln{\left(t \right)} + \frac{4}{t^{2}}\\- 6 t^{2} \ln{\left(t \right)} - \frac{6}{t^{3}}\end{aligned}]$
- $[\begin{aligned}- 3 \ln{\left(t \right)} - 3\\4 t \ln{\left(t \right)} + 2 t\\- 6 t^{2} \ln{\left(t \right)} - 2 t^{2}\end{aligned}]$
- $[\begin{aligned}- 3 t - 3 \ln{\left(t \right)}\\2 t^{2} + 4 t \ln{\left(t \right)}\\- 2 t^{3} - 6 t^{2} \ln{\left(t \right)}\end{aligned}]$
- $[\begin{aligned}- 3 t - \frac{3}{t}\\2 t^{2} + 4\\- 2 t^{3} - 6 t\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(- 3 t)\\ \frac{\text{d}}{\text{d}t}(2 t^{2})\\ \frac{\text{d}}{\text{d}t}(- 2 t^{3})\end{aligned}]=[\begin{aligned}-3\\4 t\\- 6 t^{2}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡t)=\frac{1}{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =\frac{1}{t}[\begin{aligned}- 3 t\\2 t^{2}\\- 2 t^{3}\end{aligned}]+\operatorname{ln}⁡t[\begin{aligned}-3\\4 t\\- 6 t^{2}\end{aligned}] \\  & =[\begin{aligned}-3\\2 t\\- 2 t^{2}\end{aligned}]+[\begin{aligned}- 3 \ln{\left(t \right)}\\4 t \ln{\left(t \right)}\\- 6 t^{2} \ln{\left(t \right)}\end{aligned}] \\  & =[\begin{aligned}- 3 \ln{\left(t \right)} - 3\\4 t \ln{\left(t \right)} + 2 t\\- 6 t^{2} \ln{\left(t \right)} - 2 t^{2}\end{aligned}]\end{aligned}
$$

### Generated authored_product_errors {"scales": [2, -1, 3]}

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}2 t\\- t^{2}\\3 t^{3}\end{aligned}]$ and $u(t)=\operatorname{ln}⁡t.$

- $[\begin{aligned}2 \\ - t \\ 3 t^{2}\end{aligned}]$
- $[\begin{aligned}2 \ln{\left(t \right)} \\ - 2 t \ln{\left(t \right)} \\ 9 t^{2} \ln{\left(t \right)}\end{aligned}]$
- $[\begin{aligned}2 \ln{\left(t \right)} + 2 \\ - 2 t \ln{\left(t \right)} - t \\ 9 t^{2} \ln{\left(t \right)} + 3 t^{2}\end{aligned}]$
- $[\begin{aligned}\frac{2}{t} \\ -2 \\ 9 t\end{aligned}]$
- $[\begin{aligned}2 - 2 \ln{\left(t \right)} \\ 2 t \ln{\left(t \right)} - t \\ - 9 t^{2} \ln{\left(t \right)} + 3 t^{2}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 t)\\ \frac{\text{d}}{\text{d}t}(- t^{2})\\ \frac{\text{d}}{\text{d}t}(3 t^{3})\end{aligned}]=[\begin{aligned}2\\- 2 t\\9 t^{2}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡t)=\frac{1}{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =\frac{1}{t}[\begin{aligned}2 t\\- t^{2}\\3 t^{3}\end{aligned}]+\operatorname{ln}⁡t[\begin{aligned}2\\- 2 t\\9 t^{2}\end{aligned}] \\  & =[\begin{aligned}2\\- t\\3 t^{2}\end{aligned}]+[\begin{aligned}2 \ln{\left(t \right)}\\- 2 t \ln{\left(t \right)}\\9 t^{2} \ln{\left(t \right)}\end{aligned}] \\  & =[\begin{aligned}2 \ln{\left(t \right)} + 2\\- 2 t \ln{\left(t \right)} - t\\9 t^{2} \ln{\left(t \right)} + 3 t^{2}\end{aligned}]\end{aligned}
$$

## Original q-71225

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}4t-1 \\ 3t+2 \\ 5t+6\end{aligned}]$ and $u(t)=2t-3.$

- $[\begin{aligned}10t-8 \\ 12t-4 \\ 6t-5\end{aligned}]$
- $[\begin{aligned}4t-7 \\ 3t-2 \\ 5t-1\end{aligned}]$
- $[\begin{aligned}16t-14 \\ 12t-5 \\ 20t-3\end{aligned}]$
- $[\begin{aligned}8t-14 \\ 6t-5 \\ 10t-3\end{aligned}]$
- $[\begin{aligned}12t-15 \\ 14t-7 \\ 18t-2\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
{(u(t)f(t))}^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(4t-1) \\ \frac{\text{d}}{\text{d}t}(3t+2) \\ \frac{\text{d}}{\text{d}t}(5t+6)\end{aligned}]=[\begin{aligned}4 \\ 3 \\ 5\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2t-3)=2\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{(u(t)f(t))}^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =2[\begin{aligned}4t-1 \\ 3t+2 \\ 5t+6\end{aligned}]+(2t-3)[\begin{aligned}4 \\ 3 \\ 5\end{aligned}] \\  & =[\begin{aligned}8t-2 \\ 6t+4 \\ 10t+12\end{aligned}]+[\begin{aligned}8t-12 \\ 6t-9 \\ 10t-15\end{aligned}] \\  & =[\begin{aligned}16t-14 \\ 12t-5 \\ 20t-3\end{aligned}]\end{aligned}
$$

### Generated observed_q-71225 {"scales": [2, -1, 3]}

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}8 t - 2\\- 3 t - 2\\15 t + 18\end{aligned}]$ and $u(t)=2t-3.$

- $[\begin{aligned}32 t - 28\\5 - 12 t\\60 t - 9\end{aligned}]$
- $[\begin{aligned}8 t - 14\\2 - 3 t\\15 t - 3\end{aligned}]$
- $[\begin{aligned}20 t - 16\\4 - 12 t\\18 t - 15\end{aligned}]$
- $[\begin{aligned}24 t - 30\\7 - 14 t\\54 t - 6\end{aligned}]$
- $[\begin{aligned}16 t - 28\\5 - 6 t\\30 t - 9\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
{(u(t)f(t))}^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(8 t - 2)\\ \frac{\text{d}}{\text{d}t}(- 3 t - 2)\\ \frac{\text{d}}{\text{d}t}(15 t + 18)\end{aligned}]=[\begin{aligned}8\\-3\\15\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2t-3)=2\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{(u(t)f(t))}^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =2[\begin{aligned}8 t - 2\\- 3 t - 2\\15 t + 18\end{aligned}]+(2t-3)[\begin{aligned}8\\-3\\15\end{aligned}] \\  & =[\begin{aligned}16 t - 4\\- 6 t - 4\\30 t + 36\end{aligned}]+[\begin{aligned}16 t - 24\\9 - 6 t\\30 t - 45\end{aligned}] \\  & =[\begin{aligned}32 t - 28\\5 - 12 t\\60 t - 9\end{aligned}]\end{aligned}
$$

### Generated observed_q-71225 {"scales": [-3, 2, -2]}

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}3 - 12 t\\6 t + 4\\- 10 t - 12\end{aligned}]$ and $u(t)=2t-3.$

- $[\begin{aligned}42 - 48 t\\24 t - 10\\6 - 40 t\end{aligned}]$
- $[\begin{aligned}21 - 12 t\\6 t - 4\\2 - 10 t\end{aligned}]$
- $[\begin{aligned}24 - 30 t\\24 t - 8\\10 - 12 t\end{aligned}]$
- $[\begin{aligned}45 - 36 t\\28 t - 14\\4 - 36 t\end{aligned}]$
- $[\begin{aligned}42 - 24 t\\12 t - 10\\6 - 20 t\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
{(u(t)f(t))}^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(3 - 12 t)\\ \frac{\text{d}}{\text{d}t}(6 t + 4)\\ \frac{\text{d}}{\text{d}t}(- 10 t - 12)\end{aligned}]=[\begin{aligned}-12\\6\\-10\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2t-3)=2\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{(u(t)f(t))}^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =2[\begin{aligned}3 - 12 t\\6 t + 4\\- 10 t - 12\end{aligned}]+(2t-3)[\begin{aligned}-12\\6\\-10\end{aligned}] \\  & =[\begin{aligned}6 - 24 t\\12 t + 8\\- 20 t - 24\end{aligned}]+[\begin{aligned}36 - 24 t\\12 t - 18\\30 - 20 t\end{aligned}] \\  & =[\begin{aligned}42 - 48 t\\24 t - 10\\6 - 40 t\end{aligned}]\end{aligned}
$$

### Generated authored_product_errors {"scales": [2, -1, 3]}

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}8 t - 2\\- 3 t - 2\\15 t + 18\end{aligned}]$ and $u(t)=2t-3.$

- $[\begin{aligned}16 t - 4 \\ - 6 t - 4 \\ 30 t + 36\end{aligned}]$
- $[\begin{aligned}16 t - 24 \\ 9 - 6 t \\ 30 t - 45\end{aligned}]$
- $[\begin{aligned}32 t - 28 \\ 5 - 12 t \\ 60 t - 9\end{aligned}]$
- $[\begin{aligned}16 \\ -6 \\ 30\end{aligned}]$
- $[\begin{aligned}20 \\ -13 \\ 81\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
{(u(t)f(t))}^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(8 t - 2)\\ \frac{\text{d}}{\text{d}t}(- 3 t - 2)\\ \frac{\text{d}}{\text{d}t}(15 t + 18)\end{aligned}]=[\begin{aligned}8\\-3\\15\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2t-3)=2\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{(u(t)f(t))}^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =2[\begin{aligned}8 t - 2\\- 3 t - 2\\15 t + 18\end{aligned}]+(2t-3)[\begin{aligned}8\\-3\\15\end{aligned}] \\  & =[\begin{aligned}16 t - 4\\- 6 t - 4\\30 t + 36\end{aligned}]+[\begin{aligned}16 t - 24\\9 - 6 t\\30 t - 45\end{aligned}] \\  & =[\begin{aligned}32 t - 28\\5 - 12 t\\60 t - 9\end{aligned}]\end{aligned}
$$

## Original q-71230

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}{e}^{t} \\ 8 \\ {e}^{-t}\end{aligned}]$ and $u(t)={t}^{2}.$

- $[\begin{aligned}3t{e}^{t} \\ -8t \\ -3t{e}^{-t}\end{aligned}]$
- $[\begin{aligned}(2t+{t}^{2}){e}^{t} \\ 16t \\ (2t-{t}^{2}){e}^{-t}\end{aligned}]$
- $[\begin{aligned}3{t}^{3}{e}^{t} \\ -16t \\ -{t}^{3}{e}^{-t}\end{aligned}]$
- $[\begin{aligned}({t}^{2}+{t}^{3}){e}^{t} \\ 4t \\ {t}^{3}{e}^{-t}\end{aligned}]$
- $[\begin{aligned}(1-{t}^{2}){e}^{t} \\ 8t \\ (t+{t}^{2}){e}^{-t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
{(u(t)f(t))}^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}({e}^{t}) \\ \frac{\text{d}}{\text{d}t}(8) \\ \frac{\text{d}}{\text{d}t}({e}^{-t})\end{aligned}]=[\begin{aligned}{e}^{t} \\ 0 \\ -{e}^{-t}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{2})=2t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{(u(t)f(t))}^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =2t[\begin{aligned}{e}^{t} \\ 8 \\ {e}^{-t}\end{aligned}]+{t}^{2}[\begin{aligned}{e}^{t} \\ 0 \\ -{e}^{-t}\end{aligned}] \\  & =[\begin{aligned}2t{e}^{t} \\ 16t \\ 2t{e}^{-t}\end{aligned}]+[\begin{aligned}{t}^{2}{e}^{t} \\ 0 \\ -{t}^{2}{e}^{-t}\end{aligned}] \\  & =[\begin{aligned}(2t+{t}^{2}){e}^{t} \\ 16t \\ (2t-{t}^{2}){e}^{-t}\end{aligned}]\end{aligned}
$$

### Generated observed_q-71230 {"scales": [2, -1, 3]}

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}2 e^{t}\\-8\\3 e^{- t}\end{aligned}]$ and $u(t)={t}^{2}.$

- $[\begin{aligned}6 t^{3} e^{t}\\16 t\\- 3 t^{3} e^{- t}\end{aligned}]$
- $[\begin{aligned}2 \left(t^{2} + 2 t\right) e^{t}\\- 16 t\\3 \left(- t^{2} + 2 t\right) e^{- t}\end{aligned}]$
- $[\begin{aligned}6 t e^{t}\\8 t\\- 9 t e^{- t}\end{aligned}]$
- $[\begin{aligned}2 \left(1 - t^{2}\right) e^{t}\\- 8 t\\3 \left(t^{2} + t\right) e^{- t}\end{aligned}]$
- $[\begin{aligned}2 \left(t^{3} + t^{2}\right) e^{t}\\- 4 t\\3 t^{3} e^{- t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
{(u(t)f(t))}^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 e^{t})\\ \frac{\text{d}}{\text{d}t}(-8)\\ \frac{\text{d}}{\text{d}t}(3 e^{- t})\end{aligned}]=[\begin{aligned}2 e^{t}\\0\\- 3 e^{- t}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{2})=2t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{(u(t)f(t))}^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =2t[\begin{aligned}2 e^{t}\\-8\\3 e^{- t}\end{aligned}]+{t}^{2}[\begin{aligned}2 e^{t}\\0\\- 3 e^{- t}\end{aligned}] \\  & =[\begin{aligned}4 t e^{t}\\- 16 t\\6 t e^{- t}\end{aligned}]+[\begin{aligned}2 t^{2} e^{t}\\0\\- 3 t^{2} e^{- t}\end{aligned}] \\  & =[\begin{aligned}2 \left(t^{2} + 2 t\right) e^{t}\\- 16 t\\3 \left(- t^{2} + 2 t\right) e^{- t}\end{aligned}]\end{aligned}
$$

### Generated observed_q-71230 {"scales": [-3, 2, -2]}

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}- 3 e^{t}\\16\\- 2 e^{- t}\end{aligned}]$ and $u(t)={t}^{2}.$

- $[\begin{aligned}- 9 t^{3} e^{t}\\- 32 t\\2 t^{3} e^{- t}\end{aligned}]$
- $[\begin{aligned}- 3 \left(t^{2} + 2 t\right) e^{t}\\32 t\\- 2 \left(- t^{2} + 2 t\right) e^{- t}\end{aligned}]$
- $[\begin{aligned}- 9 t e^{t}\\- 16 t\\6 t e^{- t}\end{aligned}]$
- $[\begin{aligned}- 3 \left(1 - t^{2}\right) e^{t}\\16 t\\- 2 \left(t^{2} + t\right) e^{- t}\end{aligned}]$
- $[\begin{aligned}- 3 \left(t^{3} + t^{2}\right) e^{t}\\8 t\\- 2 t^{3} e^{- t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
{(u(t)f(t))}^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(- 3 e^{t})\\ \frac{\text{d}}{\text{d}t}(16)\\ \frac{\text{d}}{\text{d}t}(- 2 e^{- t})\end{aligned}]=[\begin{aligned}- 3 e^{t}\\0\\2 e^{- t}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{2})=2t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{(u(t)f(t))}^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =2t[\begin{aligned}- 3 e^{t}\\16\\- 2 e^{- t}\end{aligned}]+{t}^{2}[\begin{aligned}- 3 e^{t}\\0\\2 e^{- t}\end{aligned}] \\  & =[\begin{aligned}- 6 t e^{t}\\32 t\\- 4 t e^{- t}\end{aligned}]+[\begin{aligned}- 3 t^{2} e^{t}\\0\\2 t^{2} e^{- t}\end{aligned}] \\  & =[\begin{aligned}- 3 \left(t^{2} + 2 t\right) e^{t}\\32 t\\- 2 \left(- t^{2} + 2 t\right) e^{- t}\end{aligned}]\end{aligned}
$$

### Generated authored_product_errors {"scales": [2, -1, 3]}

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}2 e^{t}\\-8\\3 e^{- t}\end{aligned}]$ and $u(t)={t}^{2}.$

- $[\begin{aligned}4 t e^{t} \\ - 16 t \\ 6 t e^{- t}\end{aligned}]$
- $[\begin{aligned}2 t^{2} e^{t} \\ 0 \\ - 3 t^{2} e^{- t}\end{aligned}]$
- $[\begin{aligned}2 t^{2} e^{t} + 4 t e^{t} \\ - 16 t \\ - 3 t^{2} e^{- t} + 6 t e^{- t}\end{aligned}]$
- $[\begin{aligned}4 t e^{t} \\ 0 \\ - 6 t e^{- t}\end{aligned}]$
- $[\begin{aligned}- 2 t^{2} e^{t} + 4 t e^{t} \\ - 16 t \\ 3 t^{2} e^{- t} + 6 t e^{- t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
{(u(t)f(t))}^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 e^{t})\\ \frac{\text{d}}{\text{d}t}(-8)\\ \frac{\text{d}}{\text{d}t}(3 e^{- t})\end{aligned}]=[\begin{aligned}2 e^{t}\\0\\- 3 e^{- t}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{2})=2t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{(u(t)f(t))}^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =2t[\begin{aligned}2 e^{t}\\-8\\3 e^{- t}\end{aligned}]+{t}^{2}[\begin{aligned}2 e^{t}\\0\\- 3 e^{- t}\end{aligned}] \\  & =[\begin{aligned}4 t e^{t}\\- 16 t\\6 t e^{- t}\end{aligned}]+[\begin{aligned}2 t^{2} e^{t}\\0\\- 3 t^{2} e^{- t}\end{aligned}] \\  & =[\begin{aligned}2 \left(t^{2} + 2 t\right) e^{t}\\- 16 t\\3 \left(- t^{2} + 2 t\right) e^{- t}\end{aligned}]\end{aligned}
$$

## Original q-128488

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}{e}^{t} \\ {t}^{3} \\ {e}^{2t}\end{aligned}]$ and $u(t)={e}^{-t}.$

- $[\begin{aligned}0 \\ {t}^{2}{e}^{-t}(3-t) \\ {e}^{t}\end{aligned}]$
- $[\begin{aligned}0 \\ 3-t \\ {t}^{2}{e}^{t}\end{aligned}]$
- $[\begin{aligned}-1 \\ {t}^{2}{e}^{-t}(1-t) \\ {e}^{t}\end{aligned}]$
- $[\begin{aligned}t \\ t{e}^{-t}(3-t) \\ t{e}^{t}\end{aligned}]$
- $[\begin{aligned}-1 \\ {t}^{2}{e}^{-t} \\ {e}^{t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
{(u(t)f(t))}^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t).
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}({e}^{t}) \\ \frac{\text{d}}{\text{d}t}({t}^{3}) \\ \frac{\text{d}}{\text{d}t}({e}^{2t})\end{aligned}]=[\begin{aligned}{e}^{t} \\ 3{t}^{2} \\ 2{e}^{2t}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{-t})=-{e}^{-t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}{(u(t)f(t))}^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =-{e}^{-t}[\begin{aligned}{e}^{t} \\ {t}^{3} \\ {e}^{2t}\end{aligned}]+{e}^{-t}[\begin{aligned}{e}^{t} \\ 3{t}^{2} \\ 2{e}^{2t}\end{aligned}] \\  & =[\begin{aligned}-1 \\ -{t}^{3}{e}^{-t} \\ -{e}^{t}\end{aligned}]+[\begin{aligned}1 \\ 3{t}^{2}{e}^{-t} \\ 2{e}^{t}\end{aligned}] \\  & =[\begin{aligned}0 \\ 3{t}^{2}{e}^{-t}-{t}^{3}{e}^{-t} \\ {e}^{t}\end{aligned}] \\  & =[\begin{aligned}0 \\ {t}^{2}{e}^{-t}(3-t) \\ {e}^{t}\end{aligned}].\end{aligned}
$$

### Generated observed_q-128488 {"scales": [2, -1, 3]}

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}2 e^{t}\\- t^{3}\\3 e^{2 t}\end{aligned}]$ and $u(t)={e}^{-t}.$

- $[\begin{aligned}-2\\- t^{2} \left(1 - t\right) e^{- t}\\3 e^{t}\end{aligned}]$
- $[\begin{aligned}0\\t - 3\\3 t^{2} e^{t}\end{aligned}]$
- $[\begin{aligned}0\\- t^{2} \left(3 - t\right) e^{- t}\\3 e^{t}\end{aligned}]$
- $[\begin{aligned}-2\\- t^{2} e^{- t}\\3 e^{t}\end{aligned}]$
- $[\begin{aligned}2 t\\- t \left(3 - t\right) e^{- t}\\3 t e^{t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
{(u(t)f(t))}^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t).
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 e^{t})\\ \frac{\text{d}}{\text{d}t}(- t^{3})\\ \frac{\text{d}}{\text{d}t}(3 e^{2 t})\end{aligned}]=[\begin{aligned}2 e^{t}\\- 3 t^{2}\\6 e^{2 t}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{-t})=-{e}^{-t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}{(u(t)f(t))}^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =-{e}^{-t}[\begin{aligned}2 e^{t}\\- t^{3}\\3 e^{2 t}\end{aligned}]+{e}^{-t}[\begin{aligned}2 e^{t}\\- 3 t^{2}\\6 e^{2 t}\end{aligned}] \\  & =[\begin{aligned}-2\\t^{3} e^{- t}\\- 3 e^{t}\end{aligned}]+[\begin{aligned}2\\- 3 t^{2} e^{- t}\\6 e^{t}\end{aligned}] \\  & =[\begin{aligned}0\\t^{3} e^{- t} - 3 t^{2} e^{- t}\\3 e^{t}\end{aligned}] \\  & =[\begin{aligned}0\\- t^{2} \left(3 - t\right) e^{- t}\\3 e^{t}\end{aligned}].\end{aligned}
$$

### Generated observed_q-128488 {"scales": [-3, 2, -2]}

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}- 3 e^{t}\\2 t^{3}\\- 2 e^{2 t}\end{aligned}]$ and $u(t)={e}^{-t}.$

- $[\begin{aligned}3\\2 t^{2} \left(1 - t\right) e^{- t}\\- 2 e^{t}\end{aligned}]$
- $[\begin{aligned}0\\6 - 2 t\\- 2 t^{2} e^{t}\end{aligned}]$
- $[\begin{aligned}0\\2 t^{2} \left(3 - t\right) e^{- t}\\- 2 e^{t}\end{aligned}]$
- $[\begin{aligned}3\\2 t^{2} e^{- t}\\- 2 e^{t}\end{aligned}]$
- $[\begin{aligned}- 3 t\\2 t \left(3 - t\right) e^{- t}\\- 2 t e^{t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
{(u(t)f(t))}^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t).
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(- 3 e^{t})\\ \frac{\text{d}}{\text{d}t}(2 t^{3})\\ \frac{\text{d}}{\text{d}t}(- 2 e^{2 t})\end{aligned}]=[\begin{aligned}- 3 e^{t}\\6 t^{2}\\- 4 e^{2 t}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{-t})=-{e}^{-t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}{(u(t)f(t))}^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =-{e}^{-t}[\begin{aligned}- 3 e^{t}\\2 t^{3}\\- 2 e^{2 t}\end{aligned}]+{e}^{-t}[\begin{aligned}- 3 e^{t}\\6 t^{2}\\- 4 e^{2 t}\end{aligned}] \\  & =[\begin{aligned}3\\- 2 t^{3} e^{- t}\\2 e^{t}\end{aligned}]+[\begin{aligned}-3\\6 t^{2} e^{- t}\\- 4 e^{t}\end{aligned}] \\  & =[\begin{aligned}0\\- 2 t^{3} e^{- t} + 6 t^{2} e^{- t}\\- 2 e^{t}\end{aligned}] \\  & =[\begin{aligned}0\\2 t^{2} \left(3 - t\right) e^{- t}\\- 2 e^{t}\end{aligned}].\end{aligned}
$$

### Generated authored_product_errors {"scales": [2, -1, 3]}

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}2 e^{t}\\- t^{3}\\3 e^{2 t}\end{aligned}]$ and $u(t)={e}^{-t}.$

- $[\begin{aligned}-2 \\ t^{3} e^{- t} \\ - 3 e^{t}\end{aligned}]$
- $[\begin{aligned}2 \\ - 3 t^{2} e^{- t} \\ 6 e^{t}\end{aligned}]$
- $[\begin{aligned}0 \\ t^{3} e^{- t} - 3 t^{2} e^{- t} \\ 3 e^{t}\end{aligned}]$
- $[\begin{aligned}2 e^{t} - 2 \\ t^{3} e^{- t} - 3 t^{2} \\ 6 e^{2 t} - 3 e^{t}\end{aligned}]$
- $[\begin{aligned}-4 \\ t^{3} e^{- t} + 3 t^{2} e^{- t} \\ - 9 e^{t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
{(u(t)f(t))}^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t).
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 e^{t})\\ \frac{\text{d}}{\text{d}t}(- t^{3})\\ \frac{\text{d}}{\text{d}t}(3 e^{2 t})\end{aligned}]=[\begin{aligned}2 e^{t}\\- 3 t^{2}\\6 e^{2 t}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{-t})=-{e}^{-t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}{(u(t)f(t))}^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =-{e}^{-t}[\begin{aligned}2 e^{t}\\- t^{3}\\3 e^{2 t}\end{aligned}]+{e}^{-t}[\begin{aligned}2 e^{t}\\- 3 t^{2}\\6 e^{2 t}\end{aligned}] \\  & =[\begin{aligned}-2\\t^{3} e^{- t}\\- 3 e^{t}\end{aligned}]+[\begin{aligned}2\\- 3 t^{2} e^{- t}\\6 e^{t}\end{aligned}] \\  & =[\begin{aligned}0\\t^{3} e^{- t} - 3 t^{2} e^{- t}\\3 e^{t}\end{aligned}] \\  & =[\begin{aligned}0\\- t^{2} \left(3 - t\right) e^{- t}\\3 e^{t}\end{aligned}].\end{aligned}
$$

## Original q-70688

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}2\operatorname{sin}⁡t \\ \operatorname{cos}⁡t \\ {e}^{t}\end{aligned}]$ and $u(t)=\operatorname{sin}⁡t.$

- $[\begin{aligned}0 \\ 1 \\ {e}^{t}(\operatorname{cos}⁡t+\operatorname{sin}⁡t)\end{aligned}]$
- $[\begin{aligned}\operatorname{sin}⁡2t \\ 1 \\ {e}^{t}(\operatorname{cos}⁡t+\operatorname{sin}⁡t)\end{aligned}]$
- $[\begin{aligned}2\operatorname{sin}⁡2t \\ \operatorname{cos}⁡2t \\ {e}^{t}(\operatorname{cos}⁡t+\operatorname{sin}⁡t)\end{aligned}]$
- $[\begin{aligned}\operatorname{sin}⁡4t \\ {cos}^{2}⁡t-{sin}^{2}⁡t \\ {e}^{t}(\operatorname{cos}⁡t-\operatorname{sin}⁡t)\end{aligned}]$
- $[\begin{aligned}0 \\ {cos}^{2}⁡t-{sin}^{2}⁡t \\ {e}^{t}(\operatorname{cos}⁡t-\operatorname{sin}⁡t)\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t).
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(2\operatorname{sin}⁡t) \\ \frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t) \\ \frac{\text{d}}{\text{d}t}({e}^{t})\end{aligned}]=[\begin{aligned}2\operatorname{cos}⁡t \\ -\operatorname{sin}⁡t \\ {e}^{t}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)=\operatorname{cos}⁡t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =\operatorname{cos}⁡t[\begin{aligned}2\operatorname{sin}⁡t \\ \operatorname{cos}⁡t \\ {e}^{t}\end{aligned}]+\operatorname{sin}⁡t[\begin{aligned}2\operatorname{cos}⁡t \\ -\operatorname{sin}⁡t \\ {e}^{t}\end{aligned}] \\  & =[\begin{aligned}2\operatorname{sin}⁡t\operatorname{cos}⁡t \\ \operatorname{cos}⁡t\operatorname{cos}⁡t \\ {e}^{t}\operatorname{cos}⁡t\end{aligned}]+[\begin{aligned}2\operatorname{sin}⁡t\operatorname{cos}⁡t \\ -\operatorname{sin}⁡t\operatorname{sin}⁡t \\ {e}^{t}\operatorname{sin}⁡t\end{aligned}] \\  & =[\begin{aligned}\operatorname{sin}⁡2t \\ {cos}^{2}⁡t \\ {e}^{t}\operatorname{cos}⁡t\end{aligned}]+[\begin{aligned}\operatorname{sin}⁡2t \\ -{sin}^{2}⁡t \\ {e}^{t}\operatorname{sin}⁡t\end{aligned}] \\  & =[\begin{aligned}2\operatorname{sin}⁡2t \\ {cos}^{2}⁡t-{sin}^{2}⁡t \\ {e}^{t}\operatorname{cos}⁡t+{e}^{t}\operatorname{sin}⁡t\end{aligned}] \\  & =[\begin{aligned}2\operatorname{sin}⁡2t \\ \operatorname{cos}⁡2t \\ {e}^{t}(\operatorname{cos}⁡t+\operatorname{sin}⁡t)\end{aligned}]\end{aligned}
$$

### Generated observed_q-70688 {"scales": [2, -1, 3]}

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}4 \sin{\left(t \right)}\\- \cos{\left(t \right)}\\3 e^{t}\end{aligned}]$ and $u(t)=\operatorname{sin}⁡t.$

- $[\begin{aligned}4 \sin{\left(2 t \right)}\\- \cos{\left(2 t \right)}\\3 \left(\sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{t}\end{aligned}]$
- $[\begin{aligned}2 \sin{\left(2 t \right)}\\-1\\3 \left(\sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{t}\end{aligned}]$
- $[\begin{aligned}0\\-1\\3 \left(\sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{t}\end{aligned}]$
- $[\begin{aligned}0\\\sin^{2}{\left(t \right)} - \cos^{2}{\left(t \right)}\\3 \left(- \sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{t}\end{aligned}]$
- $[\begin{aligned}2 \sin{\left(4 t \right)}\\\sin^{2}{\left(t \right)} - \cos^{2}{\left(t \right)}\\3 \left(- \sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t).
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(4 \sin{\left(t \right)})\\ \frac{\text{d}}{\text{d}t}(- \cos{\left(t \right)})\\ \frac{\text{d}}{\text{d}t}(3 e^{t})\end{aligned}]=[\begin{aligned}4 \cos{\left(t \right)}\\\sin{\left(t \right)}\\3 e^{t}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)=\operatorname{cos}⁡t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =\operatorname{cos}⁡t[\begin{aligned}4 \sin{\left(t \right)}\\- \cos{\left(t \right)}\\3 e^{t}\end{aligned}]+\operatorname{sin}⁡t[\begin{aligned}4 \cos{\left(t \right)}\\\sin{\left(t \right)}\\3 e^{t}\end{aligned}] \\  & =[\begin{aligned}4 \sin{\left(t \right)} \cos{\left(t \right)}\\- \cos^{2}{\left(t \right)}\\3 e^{t} \cos{\left(t \right)}\end{aligned}]+[\begin{aligned}4 \sin{\left(t \right)} \cos{\left(t \right)}\\\sin^{2}{\left(t \right)}\\3 e^{t} \sin{\left(t \right)}\end{aligned}] \\  & =[\begin{aligned}2 \sin{\left(2 t \right)}\\- \cos^{2}{\left(t \right)}\\3 e^{t} \cos{\left(t \right)}\end{aligned}]+[\begin{aligned}2 \sin{\left(2 t \right)}\\\sin^{2}{\left(t \right)}\\3 e^{t} \sin{\left(t \right)}\end{aligned}] \\  & =[\begin{aligned}4 \sin{\left(2 t \right)}\\\sin^{2}{\left(t \right)} - \cos^{2}{\left(t \right)}\\3 e^{t} \sin{\left(t \right)} + 3 e^{t} \cos{\left(t \right)}\end{aligned}] \\  & =[\begin{aligned}4 \sin{\left(2 t \right)}\\- \cos{\left(2 t \right)}\\3 \left(\sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{t}\end{aligned}]\end{aligned}
$$

### Generated observed_q-70688 {"scales": [-3, 2, -2]}

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}- 6 \sin{\left(t \right)}\\2 \cos{\left(t \right)}\\- 2 e^{t}\end{aligned}]$ and $u(t)=\operatorname{sin}⁡t.$

- $[\begin{aligned}- 6 \sin{\left(2 t \right)}\\2 \cos{\left(2 t \right)}\\- 2 \left(\sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{t}\end{aligned}]$
- $[\begin{aligned}- 3 \sin{\left(2 t \right)}\\2\\- 2 \left(\sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{t}\end{aligned}]$
- $[\begin{aligned}0\\2\\- 2 \left(\sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{t}\end{aligned}]$
- $[\begin{aligned}0\\- 2 \sin^{2}{\left(t \right)} + 2 \cos^{2}{\left(t \right)}\\- 2 \left(- \sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{t}\end{aligned}]$
- $[\begin{aligned}- 3 \sin{\left(4 t \right)}\\- 2 \sin^{2}{\left(t \right)} + 2 \cos^{2}{\left(t \right)}\\- 2 \left(- \sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t).
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(- 6 \sin{\left(t \right)})\\ \frac{\text{d}}{\text{d}t}(2 \cos{\left(t \right)})\\ \frac{\text{d}}{\text{d}t}(- 2 e^{t})\end{aligned}]=[\begin{aligned}- 6 \cos{\left(t \right)}\\- 2 \sin{\left(t \right)}\\- 2 e^{t}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)=\operatorname{cos}⁡t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =\operatorname{cos}⁡t[\begin{aligned}- 6 \sin{\left(t \right)}\\2 \cos{\left(t \right)}\\- 2 e^{t}\end{aligned}]+\operatorname{sin}⁡t[\begin{aligned}- 6 \cos{\left(t \right)}\\- 2 \sin{\left(t \right)}\\- 2 e^{t}\end{aligned}] \\  & =[\begin{aligned}- 6 \sin{\left(t \right)} \cos{\left(t \right)}\\2 \cos^{2}{\left(t \right)}\\- 2 e^{t} \cos{\left(t \right)}\end{aligned}]+[\begin{aligned}- 6 \sin{\left(t \right)} \cos{\left(t \right)}\\- 2 \sin^{2}{\left(t \right)}\\- 2 e^{t} \sin{\left(t \right)}\end{aligned}] \\  & =[\begin{aligned}- 3 \sin{\left(2 t \right)}\\2 \cos^{2}{\left(t \right)}\\- 2 e^{t} \cos{\left(t \right)}\end{aligned}]+[\begin{aligned}- 3 \sin{\left(2 t \right)}\\- 2 \sin^{2}{\left(t \right)}\\- 2 e^{t} \sin{\left(t \right)}\end{aligned}] \\  & =[\begin{aligned}- 6 \sin{\left(2 t \right)}\\- 2 \sin^{2}{\left(t \right)} + 2 \cos^{2}{\left(t \right)}\\- 2 e^{t} \sin{\left(t \right)} - 2 e^{t} \cos{\left(t \right)}\end{aligned}] \\  & =[\begin{aligned}- 6 \sin{\left(2 t \right)}\\2 \cos{\left(2 t \right)}\\- 2 \left(\sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{t}\end{aligned}]\end{aligned}
$$

### Generated authored_product_errors {"scales": [2, -1, 3]}

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}4 \sin{\left(t \right)}\\- \cos{\left(t \right)}\\3 e^{t}\end{aligned}]$ and $u(t)=\operatorname{sin}⁡t.$

- $[\begin{aligned}4 \sin{\left(t \right)} \cos{\left(t \right)} \\ - \cos^{2}{\left(t \right)} \\ 3 e^{t} \cos{\left(t \right)}\end{aligned}]$
- $[\begin{aligned}4 \sin{\left(t \right)} \cos{\left(t \right)} \\ \sin^{2}{\left(t \right)} \\ 3 e^{t} \sin{\left(t \right)}\end{aligned}]$
- $[\begin{aligned}8 \sin{\left(t \right)} \cos{\left(t \right)} \\ \sin^{2}{\left(t \right)} - \cos^{2}{\left(t \right)} \\ 3 e^{t} \sin{\left(t \right)} + 3 e^{t} \cos{\left(t \right)}\end{aligned}]$
- $[\begin{aligned}4 \sin{\left(t \right)} \cos{\left(t \right)} + 4 \cos{\left(t \right)} \\ \sin{\left(t \right)} - \cos^{2}{\left(t \right)} \\ 3 e^{t} \cos{\left(t \right)} + 3 e^{t}\end{aligned}]$
- $[\begin{aligned}0 \\ - \sin^{2}{\left(t \right)} - \cos^{2}{\left(t \right)} \\ - 3 e^{t} \sin{\left(t \right)} + 3 e^{t} \cos{\left(t \right)}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t).
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(4 \sin{\left(t \right)})\\ \frac{\text{d}}{\text{d}t}(- \cos{\left(t \right)})\\ \frac{\text{d}}{\text{d}t}(3 e^{t})\end{aligned}]=[\begin{aligned}4 \cos{\left(t \right)}\\\sin{\left(t \right)}\\3 e^{t}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)=\operatorname{cos}⁡t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =\operatorname{cos}⁡t[\begin{aligned}4 \sin{\left(t \right)}\\- \cos{\left(t \right)}\\3 e^{t}\end{aligned}]+\operatorname{sin}⁡t[\begin{aligned}4 \cos{\left(t \right)}\\\sin{\left(t \right)}\\3 e^{t}\end{aligned}] \\  & =[\begin{aligned}4 \sin{\left(t \right)} \cos{\left(t \right)}\\- \cos^{2}{\left(t \right)}\\3 e^{t} \cos{\left(t \right)}\end{aligned}]+[\begin{aligned}4 \sin{\left(t \right)} \cos{\left(t \right)}\\\sin^{2}{\left(t \right)}\\3 e^{t} \sin{\left(t \right)}\end{aligned}] \\  & =[\begin{aligned}2 \sin{\left(2 t \right)}\\- \cos^{2}{\left(t \right)}\\3 e^{t} \cos{\left(t \right)}\end{aligned}]+[\begin{aligned}2 \sin{\left(2 t \right)}\\\sin^{2}{\left(t \right)}\\3 e^{t} \sin{\left(t \right)}\end{aligned}] \\  & =[\begin{aligned}4 \sin{\left(2 t \right)}\\\sin^{2}{\left(t \right)} - \cos^{2}{\left(t \right)}\\3 e^{t} \sin{\left(t \right)} + 3 e^{t} \cos{\left(t \right)}\end{aligned}] \\  & =[\begin{aligned}4 \sin{\left(2 t \right)}\\- \cos{\left(2 t \right)}\\3 \left(\sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{t}\end{aligned}]\end{aligned}
$$

## Original q-71227

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}{e}^{3t} \\ {e}^{4t} \\ {e}^{5t}\end{aligned}]$ and $u(t)=t.$

- $[\begin{aligned}3{e}^{3t} \\ 4{e}^{4t} \\ 5{e}^{5t}\end{aligned}]$
- $[\begin{aligned}(t+3){e}^{3t} \\ (t+4){e}^{4t} \\ (t+5){e}^{5t}\end{aligned}]$
- $[\begin{aligned}3t{e}^{3t} \\ 4t{e}^{4t} \\ 5t{e}^{5t}\end{aligned}]$
- $[\begin{aligned}({t}^{2}+1){e}^{3t} \\ ({t}^{2}+2){e}^{4t} \\ ({t}^{2}+3){e}^{5t}\end{aligned}]$
- $[\begin{aligned}(3t+1){e}^{3t} \\ (4t+1){e}^{4t} \\ (5t+1){e}^{5t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
{(u(t)f(t))}^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}({e}^{3t}) \\ \frac{\text{d}}{\text{d}t}({e}^{4t}) \\ \frac{\text{d}}{\text{d}t}({e}^{5t})\end{aligned}]=[\begin{aligned}3{e}^{3t} \\ 4{e}^{4t} \\ 5{e}^{5t}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t)=1\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{(u(t)f(t))}^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =1\cdot [\begin{aligned}{e}^{3t} \\ {e}^{4t} \\ {e}^{5t}\end{aligned}]+t[\begin{aligned}3{e}^{3t} \\ 4{e}^{4t} \\ 5{e}^{5t}\end{aligned}] \\  & =[\begin{aligned}{e}^{3t} \\ {e}^{4t} \\ {e}^{5t}\end{aligned}]+[\begin{aligned}3t{e}^{3t} \\ 4t{e}^{4t} \\ 5t{e}^{5t}\end{aligned}] \\  & =[\begin{aligned}(3t+1){e}^{3t} \\ (4t+1){e}^{4t} \\ (5t+1){e}^{5t}\end{aligned}]\end{aligned}
$$

### Generated observed_q-71227 {"scales": [2, -1, 3]}

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}2 e^{3 t}\\- e^{4 t}\\3 e^{5 t}\end{aligned}]$ and $u(t)=t.$

- $[\begin{aligned}6 t e^{3 t}\\- 4 t e^{4 t}\\15 t e^{5 t}\end{aligned}]$
- $[\begin{aligned}2 \left(t + 3\right) e^{3 t}\\- \left(t + 4\right) e^{4 t}\\3 \left(t + 5\right) e^{5 t}\end{aligned}]$
- $[\begin{aligned}6 e^{3 t}\\- 4 e^{4 t}\\15 e^{5 t}\end{aligned}]$
- $[\begin{aligned}2 \left(3 t + 1\right) e^{3 t}\\- \left(4 t + 1\right) e^{4 t}\\3 \left(5 t + 1\right) e^{5 t}\end{aligned}]$
- $[\begin{aligned}2 \left(t^{2} + 1\right) e^{3 t}\\- \left(t^{2} + 2\right) e^{4 t}\\3 \left(t^{2} + 3\right) e^{5 t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
{(u(t)f(t))}^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 e^{3 t})\\ \frac{\text{d}}{\text{d}t}(- e^{4 t})\\ \frac{\text{d}}{\text{d}t}(3 e^{5 t})\end{aligned}]=[\begin{aligned}6 e^{3 t}\\- 4 e^{4 t}\\15 e^{5 t}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t)=1\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{(u(t)f(t))}^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =1\cdot [\begin{aligned}2 e^{3 t}\\- e^{4 t}\\3 e^{5 t}\end{aligned}]+t[\begin{aligned}6 e^{3 t}\\- 4 e^{4 t}\\15 e^{5 t}\end{aligned}] \\  & =[\begin{aligned}2 e^{3 t}\\- e^{4 t}\\3 e^{5 t}\end{aligned}]+[\begin{aligned}6 t e^{3 t}\\- 4 t e^{4 t}\\15 t e^{5 t}\end{aligned}] \\  & =[\begin{aligned}2 \left(3 t + 1\right) e^{3 t}\\- \left(4 t + 1\right) e^{4 t}\\3 \left(5 t + 1\right) e^{5 t}\end{aligned}]\end{aligned}
$$

### Generated observed_q-71227 {"scales": [-3, 2, -2]}

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}- 3 e^{3 t}\\2 e^{4 t}\\- 2 e^{5 t}\end{aligned}]$ and $u(t)=t.$

- $[\begin{aligned}- 9 t e^{3 t}\\8 t e^{4 t}\\- 10 t e^{5 t}\end{aligned}]$
- $[\begin{aligned}- 3 \left(t + 3\right) e^{3 t}\\2 \left(t + 4\right) e^{4 t}\\- 2 \left(t + 5\right) e^{5 t}\end{aligned}]$
- $[\begin{aligned}- 9 e^{3 t}\\8 e^{4 t}\\- 10 e^{5 t}\end{aligned}]$
- $[\begin{aligned}- 3 \left(3 t + 1\right) e^{3 t}\\2 \left(4 t + 1\right) e^{4 t}\\- 2 \left(5 t + 1\right) e^{5 t}\end{aligned}]$
- $[\begin{aligned}- 3 \left(t^{2} + 1\right) e^{3 t}\\2 \left(t^{2} + 2\right) e^{4 t}\\- 2 \left(t^{2} + 3\right) e^{5 t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
{(u(t)f(t))}^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(- 3 e^{3 t})\\ \frac{\text{d}}{\text{d}t}(2 e^{4 t})\\ \frac{\text{d}}{\text{d}t}(- 2 e^{5 t})\end{aligned}]=[\begin{aligned}- 9 e^{3 t}\\8 e^{4 t}\\- 10 e^{5 t}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t)=1\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{(u(t)f(t))}^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =1\cdot [\begin{aligned}- 3 e^{3 t}\\2 e^{4 t}\\- 2 e^{5 t}\end{aligned}]+t[\begin{aligned}- 9 e^{3 t}\\8 e^{4 t}\\- 10 e^{5 t}\end{aligned}] \\  & =[\begin{aligned}- 3 e^{3 t}\\2 e^{4 t}\\- 2 e^{5 t}\end{aligned}]+[\begin{aligned}- 9 t e^{3 t}\\8 t e^{4 t}\\- 10 t e^{5 t}\end{aligned}] \\  & =[\begin{aligned}- 3 \left(3 t + 1\right) e^{3 t}\\2 \left(4 t + 1\right) e^{4 t}\\- 2 \left(5 t + 1\right) e^{5 t}\end{aligned}]\end{aligned}
$$

### Generated authored_product_errors {"scales": [2, -1, 3]}

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}2 e^{3 t}\\- e^{4 t}\\3 e^{5 t}\end{aligned}]$ and $u(t)=t.$

- $[\begin{aligned}2 e^{3 t} \\ - e^{4 t} \\ 3 e^{5 t}\end{aligned}]$
- $[\begin{aligned}6 t e^{3 t} \\ - 4 t e^{4 t} \\ 15 t e^{5 t}\end{aligned}]$
- $[\begin{aligned}6 t e^{3 t} + 2 e^{3 t} \\ - 4 t e^{4 t} - e^{4 t} \\ 15 t e^{5 t} + 3 e^{5 t}\end{aligned}]$
- $[\begin{aligned}6 e^{3 t} \\ - 4 e^{4 t} \\ 15 e^{5 t}\end{aligned}]$
- $[\begin{aligned}- 6 t e^{3 t} + 2 e^{3 t} \\ 4 t e^{4 t} - e^{4 t} \\ - 15 t e^{5 t} + 3 e^{5 t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
{(u(t)f(t))}^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 e^{3 t})\\ \frac{\text{d}}{\text{d}t}(- e^{4 t})\\ \frac{\text{d}}{\text{d}t}(3 e^{5 t})\end{aligned}]=[\begin{aligned}6 e^{3 t}\\- 4 e^{4 t}\\15 e^{5 t}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t)=1\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{(u(t)f(t))}^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & =1\cdot [\begin{aligned}2 e^{3 t}\\- e^{4 t}\\3 e^{5 t}\end{aligned}]+t[\begin{aligned}6 e^{3 t}\\- 4 e^{4 t}\\15 e^{5 t}\end{aligned}] \\  & =[\begin{aligned}2 e^{3 t}\\- e^{4 t}\\3 e^{5 t}\end{aligned}]+[\begin{aligned}6 t e^{3 t}\\- 4 t e^{4 t}\\15 t e^{5 t}\end{aligned}] \\  & =[\begin{aligned}2 \left(3 t + 1\right) e^{3 t}\\- \left(4 t + 1\right) e^{4 t}\\3 \left(5 t + 1\right) e^{5 t}\end{aligned}]\end{aligned}
$$

## Original q-71233

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}2{t}^{3}-3 \\ {t}^{2}+1 \\ 4t-7\end{aligned}]$ and $u(t)={e}^{t}.$

- $[\begin{aligned}(4{t}^{2}+t){e}^{t} \\ ({t}^{2}-1){e}^{t} \\ {e}^{t}\end{aligned}]$
- $[\begin{aligned}(2{t}^{3}+6{t}^{2}-3){e}^{t} \\ ({t}^{2}+2t+1){e}^{t} \\ (4t-3){e}^{t}\end{aligned}]$
- $[\begin{aligned}(-5{t}^{3}-3{t}^{2}+1){e}^{t} \\ (3{t}^{2}-t-1){e}^{t} \\ (t+2){e}^{t}\end{aligned}]$
- $[\begin{aligned}({t}^{2}-4t+4) \\ ({t}^{2}-1) \\ (2t+3)\end{aligned}]$
- $[\begin{aligned}7{t}^{3}{e}^{t} \\ {t}^{2}{e}^{t} \\ 4t{e}^{t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
{(u(t)f(t))}^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(2{t}^{3}-3) \\ \frac{\text{d}}{\text{d}t}({t}^{2}+1) \\ \frac{\text{d}}{\text{d}t}(4t-7)\end{aligned}]=[\begin{aligned}6{t}^{2} \\ 2t \\ 4\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{t})={e}^{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{(u(t)f(t))}^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & ={e}^{t}[\begin{aligned}2{t}^{3}-3 \\ {t}^{2}+1 \\ 4t-7\end{aligned}]+{e}^{t}[\begin{aligned}6{t}^{2} \\ 2t \\ 4\end{aligned}] \\  & =[\begin{aligned}(2{t}^{3}-3){e}^{t} \\ ({t}^{2}+1){e}^{t} \\ (4t-7){e}^{t}\end{aligned}]+[\begin{aligned}6{t}^{2}{e}^{t} \\ 2t{e}^{t} \\ 4{e}^{t}\end{aligned}] \\  & =[\begin{aligned}(2{t}^{3}+6{t}^{2}-3){e}^{t} \\ ({t}^{2}+2t+1){e}^{t} \\ (4t-3){e}^{t}\end{aligned}]\end{aligned}
$$

### Generated observed_q-71233 {"scales": [2, -1, 3]}

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}4 t^{3} - 6\\- t^{2} - 1\\12 t - 21\end{aligned}]$ and $u(t)={e}^{t}.$

- $[\begin{aligned}2 \left(- 5 t^{3} - 3 t^{2} + 1\right) e^{t}\\- \left(3 t^{2} - t - 1\right) e^{t}\\3 \left(t + 2\right) e^{t}\end{aligned}]$
- $[\begin{aligned}2 \left(2 t^{3} + 6 t^{2} - 3\right) e^{t}\\- \left(t^{2} + 2 t + 1\right) e^{t}\\3 \left(4 t - 3\right) e^{t}\end{aligned}]$
- $[\begin{aligned}2 \left(4 t^{2} + t\right) e^{t}\\- \left(t^{2} - 1\right) e^{t}\\3 e^{t}\end{aligned}]$
- $[\begin{aligned}14 t^{3} e^{t}\\- t^{2} e^{t}\\12 t e^{t}\end{aligned}]$
- $[\begin{aligned}2 t^{2} - 8 t + 8\\1 - t^{2}\\6 t + 9\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
{(u(t)f(t))}^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(4 t^{3} - 6)\\ \frac{\text{d}}{\text{d}t}(- t^{2} - 1)\\ \frac{\text{d}}{\text{d}t}(12 t - 21)\end{aligned}]=[\begin{aligned}12 t^{2}\\- 2 t\\12\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{t})={e}^{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{(u(t)f(t))}^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & ={e}^{t}[\begin{aligned}4 t^{3} - 6\\- t^{2} - 1\\12 t - 21\end{aligned}]+{e}^{t}[\begin{aligned}12 t^{2}\\- 2 t\\12\end{aligned}] \\  & =[\begin{aligned}2 \left(2 t^{3} - 3\right) e^{t}\\- \left(t^{2} + 1\right) e^{t}\\3 \left(4 t - 7\right) e^{t}\end{aligned}]+[\begin{aligned}12 t^{2} e^{t}\\- 2 t e^{t}\\12 e^{t}\end{aligned}] \\  & =[\begin{aligned}2 \left(2 t^{3} + 6 t^{2} - 3\right) e^{t}\\- \left(t^{2} + 2 t + 1\right) e^{t}\\3 \left(4 t - 3\right) e^{t}\end{aligned}]\end{aligned}
$$

### Generated observed_q-71233 {"scales": [-3, 2, -2]}

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}9 - 6 t^{3}\\2 t^{2} + 2\\14 - 8 t\end{aligned}]$ and $u(t)={e}^{t}.$

- $[\begin{aligned}- 3 \left(- 5 t^{3} - 3 t^{2} + 1\right) e^{t}\\2 \left(3 t^{2} - t - 1\right) e^{t}\\- 2 \left(t + 2\right) e^{t}\end{aligned}]$
- $[\begin{aligned}- 3 \left(2 t^{3} + 6 t^{2} - 3\right) e^{t}\\2 \left(t^{2} + 2 t + 1\right) e^{t}\\- 2 \left(4 t - 3\right) e^{t}\end{aligned}]$
- $[\begin{aligned}- 3 \left(4 t^{2} + t\right) e^{t}\\2 \left(t^{2} - 1\right) e^{t}\\- 2 e^{t}\end{aligned}]$
- $[\begin{aligned}- 21 t^{3} e^{t}\\2 t^{2} e^{t}\\- 8 t e^{t}\end{aligned}]$
- $[\begin{aligned}- 3 t^{2} + 12 t - 12\\2 t^{2} - 2\\- 4 t - 6\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
{(u(t)f(t))}^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(9 - 6 t^{3})\\ \frac{\text{d}}{\text{d}t}(2 t^{2} + 2)\\ \frac{\text{d}}{\text{d}t}(14 - 8 t)\end{aligned}]=[\begin{aligned}- 18 t^{2}\\4 t\\-8\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{t})={e}^{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{(u(t)f(t))}^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & ={e}^{t}[\begin{aligned}9 - 6 t^{3}\\2 t^{2} + 2\\14 - 8 t\end{aligned}]+{e}^{t}[\begin{aligned}- 18 t^{2}\\4 t\\-8\end{aligned}] \\  & =[\begin{aligned}- 3 \left(2 t^{3} - 3\right) e^{t}\\2 \left(t^{2} + 1\right) e^{t}\\- 2 \left(4 t - 7\right) e^{t}\end{aligned}]+[\begin{aligned}- 18 t^{2} e^{t}\\4 t e^{t}\\- 8 e^{t}\end{aligned}] \\  & =[\begin{aligned}- 3 \left(2 t^{3} + 6 t^{2} - 3\right) e^{t}\\2 \left(t^{2} + 2 t + 1\right) e^{t}\\- 2 \left(4 t - 3\right) e^{t}\end{aligned}]\end{aligned}
$$

### Generated authored_product_errors {"scales": [2, -1, 3]}

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}4 t^{3} - 6\\- t^{2} - 1\\12 t - 21\end{aligned}]$ and $u(t)={e}^{t}.$

- $[\begin{aligned}4 t^{3} e^{t} - 6 e^{t} \\ - t^{2} e^{t} - e^{t} \\ 12 t e^{t} - 21 e^{t}\end{aligned}]$
- $[\begin{aligned}12 t^{2} e^{t} \\ - 2 t e^{t} \\ 12 e^{t}\end{aligned}]$
- $[\begin{aligned}4 t^{3} e^{t} + 12 t^{2} e^{t} - 6 e^{t} \\ - t^{2} e^{t} - 2 t e^{t} - e^{t} \\ 12 t e^{t} - 9 e^{t}\end{aligned}]$
- $[\begin{aligned}4 t^{3} e^{t} + 12 t^{2} - 6 e^{t} \\ - t^{2} e^{t} - 2 t - e^{t} \\ 12 t e^{t} - 21 e^{t} + 12\end{aligned}]$
- $[\begin{aligned}4 t^{3} e^{t} - 12 t^{2} e^{t} - 6 e^{t} \\ - t^{2} e^{t} + 2 t e^{t} - e^{t} \\ 12 t e^{t} - 33 e^{t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
{(u(t)f(t))}^{′}={u}^{′}(t)f(t)+u(t){f}^{′}(t)
$$

Let's find ${u}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(4 t^{3} - 6)\\ \frac{\text{d}}{\text{d}t}(- t^{2} - 1)\\ \frac{\text{d}}{\text{d}t}(12 t - 21)\end{aligned}]=[\begin{aligned}12 t^{2}\\- 2 t\\12\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{t})={e}^{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{(u(t)f(t))}^{′} & ={u}^{′}(t)f(t)+u(t){f}^{′}(t) \\  & ={e}^{t}[\begin{aligned}4 t^{3} - 6\\- t^{2} - 1\\12 t - 21\end{aligned}]+{e}^{t}[\begin{aligned}12 t^{2}\\- 2 t\\12\end{aligned}] \\  & =[\begin{aligned}2 \left(2 t^{3} - 3\right) e^{t}\\- \left(t^{2} + 1\right) e^{t}\\3 \left(4 t - 7\right) e^{t}\end{aligned}]+[\begin{aligned}12 t^{2} e^{t}\\- 2 t e^{t}\\12 e^{t}\end{aligned}] \\  & =[\begin{aligned}2 \left(2 t^{3} + 6 t^{2} - 3\right) e^{t}\\- \left(t^{2} + 2 t + 1\right) e^{t}\\3 \left(4 t - 3\right) e^{t}\end{aligned}]\end{aligned}
$$

## Generated authored_easy seed 0

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}t + 1 \\ - 3 e^{t} \\ - t^{3}\end{aligned}]$ and $u(t)=t^{2}.$

- $[\begin{aligned}3 t^{2} + 2 t \\ - 3 t^{2} e^{t} - 6 t e^{t} \\ - 5 t^{4}\end{aligned}]$
- $[\begin{aligned}2 t^{2} + 2 t \\ - 6 t e^{t} \\ - 2 t^{4}\end{aligned}]$
- $[\begin{aligned}t^{2} \\ - 3 t^{2} e^{t} \\ - 3 t^{4}\end{aligned}]$
- $[\begin{aligned}t^{2} + 2 t \\ 3 t^{2} e^{t} - 6 t e^{t} \\ t^{4}\end{aligned}]$
- $[\begin{aligned}2 t \\ - 6 t e^{t} \\ - 6 t^{3}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(t + 1) \\ \frac{\text{d}}{\text{d}t}(- 3 e^{t}) \\ \frac{\text{d}}{\text{d}t}(- t^{3})\end{aligned}]=[\begin{aligned}1 \\ - 3 e^{t} \\ - 3 t^{2}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2})=2 t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t)[\begin{aligned}t + 1 \\ - 3 e^{t} \\ - t^{3}\end{aligned}]+(t^{2})[\begin{aligned}1 \\ - 3 e^{t} \\ - 3 t^{2}\end{aligned}]\\&=[\begin{aligned}2 t \left(t + 1\right) \\ - 6 t e^{t} \\ - 2 t^{4}\end{aligned}]+[\begin{aligned}t^{2} \\ - 3 t^{2} e^{t} \\ - 3 t^{4}\end{aligned}]\\&=[\begin{aligned}t \left(3 t + 2\right) \\ 3 t \left(- t - 2\right) e^{t} \\ - 5 t^{4}\end{aligned}]\end{aligned}
$$

## Generated authored_easy seed 1

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}2 - 2 t \\ - 3 e^{t} \\ - t^{3}\end{aligned}]$ and $u(t)=t^{2}.$

- $[\begin{aligned}- 4 t \\ - 6 t e^{t} \\ - 6 t^{3}\end{aligned}]$
- $[\begin{aligned}- 4 t^{2} + 4 t \\ - 6 t e^{t} \\ - 2 t^{4}\end{aligned}]$
- $[\begin{aligned}- 2 t^{2} \\ - 3 t^{2} e^{t} \\ - 3 t^{4}\end{aligned}]$
- $[\begin{aligned}- 2 t^{2} + 4 t \\ 3 t^{2} e^{t} - 6 t e^{t} \\ t^{4}\end{aligned}]$
- $[\begin{aligned}- 6 t^{2} + 4 t \\ - 3 t^{2} e^{t} - 6 t e^{t} \\ - 5 t^{4}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 - 2 t) \\ \frac{\text{d}}{\text{d}t}(- 3 e^{t}) \\ \frac{\text{d}}{\text{d}t}(- t^{3})\end{aligned}]=[\begin{aligned}-2 \\ - 3 e^{t} \\ - 3 t^{2}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2})=2 t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t)[\begin{aligned}2 - 2 t \\ - 3 e^{t} \\ - t^{3}\end{aligned}]+(t^{2})[\begin{aligned}-2 \\ - 3 e^{t} \\ - 3 t^{2}\end{aligned}]\\&=[\begin{aligned}2 t \left(2 - 2 t\right) \\ - 6 t e^{t} \\ - 2 t^{4}\end{aligned}]+[\begin{aligned}- 2 t^{2} \\ - 3 t^{2} e^{t} \\ - 3 t^{4}\end{aligned}]\\&=[\begin{aligned}2 t \left(2 - 3 t\right) \\ 3 t \left(- t - 2\right) e^{t} \\ - 5 t^{4}\end{aligned}]\end{aligned}
$$

## Generated authored_easy seed 2

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}- 3 t - 3 \\ - 3 e^{t} \\ - t^{3}\end{aligned}]$ and $u(t)=t^{2}.$

- $[\begin{aligned}- 3 t^{2} - 6 t \\ 3 t^{2} e^{t} - 6 t e^{t} \\ t^{4}\end{aligned}]$
- $[\begin{aligned}- 9 t^{2} - 6 t \\ - 3 t^{2} e^{t} - 6 t e^{t} \\ - 5 t^{4}\end{aligned}]$
- $[\begin{aligned}- 6 t \\ - 6 t e^{t} \\ - 6 t^{3}\end{aligned}]$
- $[\begin{aligned}- 6 t^{2} - 6 t \\ - 6 t e^{t} \\ - 2 t^{4}\end{aligned}]$
- $[\begin{aligned}- 3 t^{2} \\ - 3 t^{2} e^{t} \\ - 3 t^{4}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(- 3 t - 3) \\ \frac{\text{d}}{\text{d}t}(- 3 e^{t}) \\ \frac{\text{d}}{\text{d}t}(- t^{3})\end{aligned}]=[\begin{aligned}-3 \\ - 3 e^{t} \\ - 3 t^{2}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2})=2 t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t)[\begin{aligned}- 3 t - 3 \\ - 3 e^{t} \\ - t^{3}\end{aligned}]+(t^{2})[\begin{aligned}-3 \\ - 3 e^{t} \\ - 3 t^{2}\end{aligned}]\\&=[\begin{aligned}2 t \left(- 3 t - 3\right) \\ - 6 t e^{t} \\ - 2 t^{4}\end{aligned}]+[\begin{aligned}- 3 t^{2} \\ - 3 t^{2} e^{t} \\ - 3 t^{4}\end{aligned}]\\&=[\begin{aligned}3 t \left(- 3 t - 2\right) \\ 3 t \left(- t - 2\right) e^{t} \\ - 5 t^{4}\end{aligned}]\end{aligned}
$$

## Generated authored_easy seed 3

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}2 - 2 t \\ 2 e^{t} \\ - 2 t^{3}\end{aligned}]$ and $u(t)=t^{2}.$

- $[\begin{aligned}- 2 t^{2} \\ 2 t^{2} e^{t} \\ - 6 t^{4}\end{aligned}]$
- $[\begin{aligned}- 6 t^{2} + 4 t \\ 2 t^{2} e^{t} + 4 t e^{t} \\ - 10 t^{4}\end{aligned}]$
- $[\begin{aligned}- 4 t \\ 4 t e^{t} \\ - 12 t^{3}\end{aligned}]$
- $[\begin{aligned}- 2 t^{2} + 4 t \\ - 2 t^{2} e^{t} + 4 t e^{t} \\ 2 t^{4}\end{aligned}]$
- $[\begin{aligned}- 4 t^{2} + 4 t \\ 4 t e^{t} \\ - 4 t^{4}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 - 2 t) \\ \frac{\text{d}}{\text{d}t}(2 e^{t}) \\ \frac{\text{d}}{\text{d}t}(- 2 t^{3})\end{aligned}]=[\begin{aligned}-2 \\ 2 e^{t} \\ - 6 t^{2}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2})=2 t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t)[\begin{aligned}2 - 2 t \\ 2 e^{t} \\ - 2 t^{3}\end{aligned}]+(t^{2})[\begin{aligned}-2 \\ 2 e^{t} \\ - 6 t^{2}\end{aligned}]\\&=[\begin{aligned}2 t \left(2 - 2 t\right) \\ 4 t e^{t} \\ - 4 t^{4}\end{aligned}]+[\begin{aligned}- 2 t^{2} \\ 2 t^{2} e^{t} \\ - 6 t^{4}\end{aligned}]\\&=[\begin{aligned}2 t \left(2 - 3 t\right) \\ 2 t \left(t + 2\right) e^{t} \\ - 10 t^{4}\end{aligned}]\end{aligned}
$$

## Generated authored_easy seed 4

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}- 2 t - 1 \\ - 3 e^{t} \\ 3 t^{3}\end{aligned}]$ and $u(t)=t^{2}.$

- $[\begin{aligned}- 2 t^{2} \\ - 3 t^{2} e^{t} \\ 9 t^{4}\end{aligned}]$
- $[\begin{aligned}- 4 t^{2} - 2 t \\ - 6 t e^{t} \\ 6 t^{4}\end{aligned}]$
- $[\begin{aligned}- 6 t^{2} - 2 t \\ - 3 t^{2} e^{t} - 6 t e^{t} \\ 15 t^{4}\end{aligned}]$
- $[\begin{aligned}- 4 t \\ - 6 t e^{t} \\ 18 t^{3}\end{aligned}]$
- $[\begin{aligned}- 2 t^{2} - 2 t \\ 3 t^{2} e^{t} - 6 t e^{t} \\ - 3 t^{4}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(- 2 t - 1) \\ \frac{\text{d}}{\text{d}t}(- 3 e^{t}) \\ \frac{\text{d}}{\text{d}t}(3 t^{3})\end{aligned}]=[\begin{aligned}-2 \\ - 3 e^{t} \\ 9 t^{2}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2})=2 t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t)[\begin{aligned}- 2 t - 1 \\ - 3 e^{t} \\ 3 t^{3}\end{aligned}]+(t^{2})[\begin{aligned}-2 \\ - 3 e^{t} \\ 9 t^{2}\end{aligned}]\\&=[\begin{aligned}2 t \left(- 2 t - 1\right) \\ - 6 t e^{t} \\ 6 t^{4}\end{aligned}]+[\begin{aligned}- 2 t^{2} \\ - 3 t^{2} e^{t} \\ 9 t^{4}\end{aligned}]\\&=[\begin{aligned}2 t \left(- 3 t - 1\right) \\ 3 t \left(- t - 2\right) e^{t} \\ 15 t^{4}\end{aligned}]\end{aligned}
$$

## Generated authored_easy seed 5

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}2 t - 1 \\ 3 e^{t} \\ - t^{3}\end{aligned}]$ and $u(t)=t^{2}.$

- $[\begin{aligned}4 t^{2} - 2 t \\ 6 t e^{t} \\ - 2 t^{4}\end{aligned}]$
- $[\begin{aligned}2 t^{2} - 2 t \\ - 3 t^{2} e^{t} + 6 t e^{t} \\ t^{4}\end{aligned}]$
- $[\begin{aligned}2 t^{2} \\ 3 t^{2} e^{t} \\ - 3 t^{4}\end{aligned}]$
- $[\begin{aligned}6 t^{2} - 2 t \\ 3 t^{2} e^{t} + 6 t e^{t} \\ - 5 t^{4}\end{aligned}]$
- $[\begin{aligned}4 t \\ 6 t e^{t} \\ - 6 t^{3}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 t - 1) \\ \frac{\text{d}}{\text{d}t}(3 e^{t}) \\ \frac{\text{d}}{\text{d}t}(- t^{3})\end{aligned}]=[\begin{aligned}2 \\ 3 e^{t} \\ - 3 t^{2}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2})=2 t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t)[\begin{aligned}2 t - 1 \\ 3 e^{t} \\ - t^{3}\end{aligned}]+(t^{2})[\begin{aligned}2 \\ 3 e^{t} \\ - 3 t^{2}\end{aligned}]\\&=[\begin{aligned}2 t \left(2 t - 1\right) \\ 6 t e^{t} \\ - 2 t^{4}\end{aligned}]+[\begin{aligned}2 t^{2} \\ 3 t^{2} e^{t} \\ - 3 t^{4}\end{aligned}]\\&=[\begin{aligned}2 t \left(3 t - 1\right) \\ 3 t \left(t + 2\right) e^{t} \\ - 5 t^{4}\end{aligned}]\end{aligned}
$$

## Generated authored_easy seed 6

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}2 t - 3 \\ e^{t} \\ - t^{3}\end{aligned}]$ and $u(t)=t^{2}.$

- $[\begin{aligned}4 t^{2} - 6 t \\ 2 t e^{t} \\ - 2 t^{4}\end{aligned}]$
- $[\begin{aligned}2 t^{2} \\ t^{2} e^{t} \\ - 3 t^{4}\end{aligned}]$
- $[\begin{aligned}2 t^{2} - 6 t \\ - t^{2} e^{t} + 2 t e^{t} \\ t^{4}\end{aligned}]$
- $[\begin{aligned}4 t \\ 2 t e^{t} \\ - 6 t^{3}\end{aligned}]$
- $[\begin{aligned}6 t^{2} - 6 t \\ t^{2} e^{t} + 2 t e^{t} \\ - 5 t^{4}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 t - 3) \\ \frac{\text{d}}{\text{d}t}(e^{t}) \\ \frac{\text{d}}{\text{d}t}(- t^{3})\end{aligned}]=[\begin{aligned}2 \\ e^{t} \\ - 3 t^{2}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2})=2 t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t)[\begin{aligned}2 t - 3 \\ e^{t} \\ - t^{3}\end{aligned}]+(t^{2})[\begin{aligned}2 \\ e^{t} \\ - 3 t^{2}\end{aligned}]\\&=[\begin{aligned}2 t \left(2 t - 3\right) \\ 2 t e^{t} \\ - 2 t^{4}\end{aligned}]+[\begin{aligned}2 t^{2} \\ t^{2} e^{t} \\ - 3 t^{4}\end{aligned}]\\&=[\begin{aligned}6 t \left(t - 1\right) \\ t \left(t + 2\right) e^{t} \\ - 5 t^{4}\end{aligned}]\end{aligned}
$$

## Generated authored_easy seed 7

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}- t - 2 \\ e^{t} \\ 3 t^{3}\end{aligned}]$ and $u(t)=t^{2}.$

- $[\begin{aligned}- t^{2} \\ t^{2} e^{t} \\ 9 t^{4}\end{aligned}]$
- $[\begin{aligned}- t^{2} - 4 t \\ - t^{2} e^{t} + 2 t e^{t} \\ - 3 t^{4}\end{aligned}]$
- $[\begin{aligned}- 2 t^{2} - 4 t \\ 2 t e^{t} \\ 6 t^{4}\end{aligned}]$
- $[\begin{aligned}- 2 t \\ 2 t e^{t} \\ 18 t^{3}\end{aligned}]$
- $[\begin{aligned}- 3 t^{2} - 4 t \\ t^{2} e^{t} + 2 t e^{t} \\ 15 t^{4}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(- t - 2) \\ \frac{\text{d}}{\text{d}t}(e^{t}) \\ \frac{\text{d}}{\text{d}t}(3 t^{3})\end{aligned}]=[\begin{aligned}-1 \\ e^{t} \\ 9 t^{2}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2})=2 t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t)[\begin{aligned}- t - 2 \\ e^{t} \\ 3 t^{3}\end{aligned}]+(t^{2})[\begin{aligned}-1 \\ e^{t} \\ 9 t^{2}\end{aligned}]\\&=[\begin{aligned}2 t \left(- t - 2\right) \\ 2 t e^{t} \\ 6 t^{4}\end{aligned}]+[\begin{aligned}- t^{2} \\ t^{2} e^{t} \\ 9 t^{4}\end{aligned}]\\&=[\begin{aligned}t \left(- 3 t - 4\right) \\ t \left(t + 2\right) e^{t} \\ 15 t^{4}\end{aligned}]\end{aligned}
$$

## Generated authored_easy seed 8

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}- 2 t - 1 \\ e^{t} \\ - 2 t^{3}\end{aligned}]$ and $u(t)=t^{2}.$

- $[\begin{aligned}- 4 t \\ 2 t e^{t} \\ - 12 t^{3}\end{aligned}]$
- $[\begin{aligned}- 4 t^{2} - 2 t \\ 2 t e^{t} \\ - 4 t^{4}\end{aligned}]$
- $[\begin{aligned}- 2 t^{2} - 2 t \\ - t^{2} e^{t} + 2 t e^{t} \\ 2 t^{4}\end{aligned}]$
- $[\begin{aligned}- 6 t^{2} - 2 t \\ t^{2} e^{t} + 2 t e^{t} \\ - 10 t^{4}\end{aligned}]$
- $[\begin{aligned}- 2 t^{2} \\ t^{2} e^{t} \\ - 6 t^{4}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(- 2 t - 1) \\ \frac{\text{d}}{\text{d}t}(e^{t}) \\ \frac{\text{d}}{\text{d}t}(- 2 t^{3})\end{aligned}]=[\begin{aligned}-2 \\ e^{t} \\ - 6 t^{2}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2})=2 t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t)[\begin{aligned}- 2 t - 1 \\ e^{t} \\ - 2 t^{3}\end{aligned}]+(t^{2})[\begin{aligned}-2 \\ e^{t} \\ - 6 t^{2}\end{aligned}]\\&=[\begin{aligned}2 t \left(- 2 t - 1\right) \\ 2 t e^{t} \\ - 4 t^{4}\end{aligned}]+[\begin{aligned}- 2 t^{2} \\ t^{2} e^{t} \\ - 6 t^{4}\end{aligned}]\\&=[\begin{aligned}2 t \left(- 3 t - 1\right) \\ t \left(t + 2\right) e^{t} \\ - 10 t^{4}\end{aligned}]\end{aligned}
$$

## Generated authored_easy seed 9

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}t + 2 \\ - e^{t} \\ - t^{3}\end{aligned}]$ and $u(t)=t^{2}.$

- $[\begin{aligned}t^{2} + 4 t \\ t^{2} e^{t} - 2 t e^{t} \\ t^{4}\end{aligned}]$
- $[\begin{aligned}3 t^{2} + 4 t \\ - t^{2} e^{t} - 2 t e^{t} \\ - 5 t^{4}\end{aligned}]$
- $[\begin{aligned}2 t^{2} + 4 t \\ - 2 t e^{t} \\ - 2 t^{4}\end{aligned}]$
- $[\begin{aligned}2 t \\ - 2 t e^{t} \\ - 6 t^{3}\end{aligned}]$
- $[\begin{aligned}t^{2} \\ - t^{2} e^{t} \\ - 3 t^{4}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(t + 2) \\ \frac{\text{d}}{\text{d}t}(- e^{t}) \\ \frac{\text{d}}{\text{d}t}(- t^{3})\end{aligned}]=[\begin{aligned}1 \\ - e^{t} \\ - 3 t^{2}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2})=2 t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t)[\begin{aligned}t + 2 \\ - e^{t} \\ - t^{3}\end{aligned}]+(t^{2})[\begin{aligned}1 \\ - e^{t} \\ - 3 t^{2}\end{aligned}]\\&=[\begin{aligned}2 t \left(t + 2\right) \\ - 2 t e^{t} \\ - 2 t^{4}\end{aligned}]+[\begin{aligned}t^{2} \\ - t^{2} e^{t} \\ - 3 t^{4}\end{aligned}]\\&=[\begin{aligned}t \left(3 t + 4\right) \\ t \left(- t - 2\right) e^{t} \\ - 5 t^{4}\end{aligned}]\end{aligned}
$$

## Generated authored_easy seed 10

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}2 t - 3 \\ e^{t} \\ t^{3}\end{aligned}]$ and $u(t)=t^{2}.$

- $[\begin{aligned}4 t^{2} - 6 t \\ 2 t e^{t} \\ 2 t^{4}\end{aligned}]$
- $[\begin{aligned}2 t^{2} \\ t^{2} e^{t} \\ 3 t^{4}\end{aligned}]$
- $[\begin{aligned}2 t^{2} - 6 t \\ - t^{2} e^{t} + 2 t e^{t} \\ - t^{4}\end{aligned}]$
- $[\begin{aligned}6 t^{2} - 6 t \\ t^{2} e^{t} + 2 t e^{t} \\ 5 t^{4}\end{aligned}]$
- $[\begin{aligned}4 t \\ 2 t e^{t} \\ 6 t^{3}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 t - 3) \\ \frac{\text{d}}{\text{d}t}(e^{t}) \\ \frac{\text{d}}{\text{d}t}(t^{3})\end{aligned}]=[\begin{aligned}2 \\ e^{t} \\ 3 t^{2}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2})=2 t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t)[\begin{aligned}2 t - 3 \\ e^{t} \\ t^{3}\end{aligned}]+(t^{2})[\begin{aligned}2 \\ e^{t} \\ 3 t^{2}\end{aligned}]\\&=[\begin{aligned}2 t \left(2 t - 3\right) \\ 2 t e^{t} \\ 2 t^{4}\end{aligned}]+[\begin{aligned}2 t^{2} \\ t^{2} e^{t} \\ 3 t^{4}\end{aligned}]\\&=[\begin{aligned}6 t \left(t - 1\right) \\ t \left(t + 2\right) e^{t} \\ 5 t^{4}\end{aligned}]\end{aligned}
$$

## Generated authored_easy seed 11

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}t + 2 \\ e^{t} \\ t^{3}\end{aligned}]$ and $u(t)=t^{2}.$

- $[\begin{aligned}2 t^{2} + 4 t \\ 2 t e^{t} \\ 2 t^{4}\end{aligned}]$
- $[\begin{aligned}t^{2} + 4 t \\ - t^{2} e^{t} + 2 t e^{t} \\ - t^{4}\end{aligned}]$
- $[\begin{aligned}3 t^{2} + 4 t \\ t^{2} e^{t} + 2 t e^{t} \\ 5 t^{4}\end{aligned}]$
- $[\begin{aligned}t^{2} \\ t^{2} e^{t} \\ 3 t^{4}\end{aligned}]$
- $[\begin{aligned}2 t \\ 2 t e^{t} \\ 6 t^{3}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(t + 2) \\ \frac{\text{d}}{\text{d}t}(e^{t}) \\ \frac{\text{d}}{\text{d}t}(t^{3})\end{aligned}]=[\begin{aligned}1 \\ e^{t} \\ 3 t^{2}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2})=2 t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t)[\begin{aligned}t + 2 \\ e^{t} \\ t^{3}\end{aligned}]+(t^{2})[\begin{aligned}1 \\ e^{t} \\ 3 t^{2}\end{aligned}]\\&=[\begin{aligned}2 t \left(t + 2\right) \\ 2 t e^{t} \\ 2 t^{4}\end{aligned}]+[\begin{aligned}t^{2} \\ t^{2} e^{t} \\ 3 t^{4}\end{aligned}]\\&=[\begin{aligned}t \left(3 t + 4\right) \\ t \left(t + 2\right) e^{t} \\ 5 t^{4}\end{aligned}]\end{aligned}
$$

## Generated authored_moderate seed 0

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}t^{3} + 1 \\ 1 - 3 t^{2} \\ - t - 2\end{aligned}]$ and $u(t)=e^{t}.$

- $[\begin{aligned}t^{3} e^{t} + 3 t^{2} e^{t} + e^{t} \\ - 3 t^{2} e^{t} - 6 t e^{t} + e^{t} \\ - t e^{t} - 3 e^{t}\end{aligned}]$
- $[\begin{aligned}t^{3} e^{t} + e^{t} \\ - 3 t^{2} e^{t} + e^{t} \\ - t e^{t} - 2 e^{t}\end{aligned}]$
- $[\begin{aligned}3 t^{2} e^{t} \\ - 6 t e^{t} \\ - e^{t}\end{aligned}]$
- $[\begin{aligned}t^{3} e^{t} - 3 t^{2} e^{t} + e^{t} \\ - 3 t^{2} e^{t} + 6 t e^{t} + e^{t} \\ - t e^{t} - e^{t}\end{aligned}]$
- $[\begin{aligned}t^{3} e^{t} + 3 t^{2} + e^{t} \\ - 3 t^{2} e^{t} - 6 t + e^{t} \\ - t e^{t} - 2 e^{t} - 1\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(t^{3} + 1) \\ \frac{\text{d}}{\text{d}t}(1 - 3 t^{2}) \\ \frac{\text{d}}{\text{d}t}(- t - 2)\end{aligned}]=[\begin{aligned}3 t^{2} \\ - 6 t \\ -1\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(e^{t})=e^{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(e^{t})[\begin{aligned}t^{3} + 1 \\ 1 - 3 t^{2} \\ - t - 2\end{aligned}]+(e^{t})[\begin{aligned}3 t^{2} \\ - 6 t \\ -1\end{aligned}]\\&=[\begin{aligned}\left(t^{3} + 1\right) e^{t} \\ \left(1 - 3 t^{2}\right) e^{t} \\ \left(- t - 2\right) e^{t}\end{aligned}]+[\begin{aligned}3 t^{2} e^{t} \\ - 6 t e^{t} \\ - e^{t}\end{aligned}]\\&=[\begin{aligned}\left(t^{3} + 3 t^{2} + 1\right) e^{t} \\ \left(- 3 t^{2} - 6 t + 1\right) e^{t} \\ \left(- t - 3\right) e^{t}\end{aligned}]\end{aligned}
$$

## Generated authored_moderate seed 1

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}2 - 2 t^{3} \\ 1 - 3 t^{2} \\ - t - 2\end{aligned}]$ and $u(t)=e^{t}.$

- $[\begin{aligned}- 2 t^{3} e^{t} - 6 t^{2} + 2 e^{t} \\ - 3 t^{2} e^{t} - 6 t + e^{t} \\ - t e^{t} - 2 e^{t} - 1\end{aligned}]$
- $[\begin{aligned}- 2 t^{3} e^{t} + 2 e^{t} \\ - 3 t^{2} e^{t} + e^{t} \\ - t e^{t} - 2 e^{t}\end{aligned}]$
- $[\begin{aligned}- 6 t^{2} e^{t} \\ - 6 t e^{t} \\ - e^{t}\end{aligned}]$
- $[\begin{aligned}- 2 t^{3} e^{t} + 6 t^{2} e^{t} + 2 e^{t} \\ - 3 t^{2} e^{t} + 6 t e^{t} + e^{t} \\ - t e^{t} - e^{t}\end{aligned}]$
- $[\begin{aligned}- 2 t^{3} e^{t} - 6 t^{2} e^{t} + 2 e^{t} \\ - 3 t^{2} e^{t} - 6 t e^{t} + e^{t} \\ - t e^{t} - 3 e^{t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 - 2 t^{3}) \\ \frac{\text{d}}{\text{d}t}(1 - 3 t^{2}) \\ \frac{\text{d}}{\text{d}t}(- t - 2)\end{aligned}]=[\begin{aligned}- 6 t^{2} \\ - 6 t \\ -1\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(e^{t})=e^{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(e^{t})[\begin{aligned}2 - 2 t^{3} \\ 1 - 3 t^{2} \\ - t - 2\end{aligned}]+(e^{t})[\begin{aligned}- 6 t^{2} \\ - 6 t \\ -1\end{aligned}]\\&=[\begin{aligned}\left(2 - 2 t^{3}\right) e^{t} \\ \left(1 - 3 t^{2}\right) e^{t} \\ \left(- t - 2\right) e^{t}\end{aligned}]+[\begin{aligned}- 6 t^{2} e^{t} \\ - 6 t e^{t} \\ - e^{t}\end{aligned}]\\&=[\begin{aligned}2 \left(- t^{3} - 3 t^{2} + 1\right) e^{t} \\ \left(- 3 t^{2} - 6 t + 1\right) e^{t} \\ \left(- t - 3\right) e^{t}\end{aligned}]\end{aligned}
$$

## Generated authored_moderate seed 2

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}- 3 t^{3} - 3 \\ 1 - 3 t^{2} \\ - t - 2\end{aligned}]$ and $u(t)=e^{t}.$

- $[\begin{aligned}- 3 t^{3} e^{t} + 9 t^{2} e^{t} - 3 e^{t} \\ - 3 t^{2} e^{t} + 6 t e^{t} + e^{t} \\ - t e^{t} - e^{t}\end{aligned}]$
- $[\begin{aligned}- 3 t^{3} e^{t} - 9 t^{2} e^{t} - 3 e^{t} \\ - 3 t^{2} e^{t} - 6 t e^{t} + e^{t} \\ - t e^{t} - 3 e^{t}\end{aligned}]$
- $[\begin{aligned}- 3 t^{3} e^{t} - 9 t^{2} - 3 e^{t} \\ - 3 t^{2} e^{t} - 6 t + e^{t} \\ - t e^{t} - 2 e^{t} - 1\end{aligned}]$
- $[\begin{aligned}- 3 t^{3} e^{t} - 3 e^{t} \\ - 3 t^{2} e^{t} + e^{t} \\ - t e^{t} - 2 e^{t}\end{aligned}]$
- $[\begin{aligned}- 9 t^{2} e^{t} \\ - 6 t e^{t} \\ - e^{t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(- 3 t^{3} - 3) \\ \frac{\text{d}}{\text{d}t}(1 - 3 t^{2}) \\ \frac{\text{d}}{\text{d}t}(- t - 2)\end{aligned}]=[\begin{aligned}- 9 t^{2} \\ - 6 t \\ -1\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(e^{t})=e^{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(e^{t})[\begin{aligned}- 3 t^{3} - 3 \\ 1 - 3 t^{2} \\ - t - 2\end{aligned}]+(e^{t})[\begin{aligned}- 9 t^{2} \\ - 6 t \\ -1\end{aligned}]\\&=[\begin{aligned}\left(- 3 t^{3} - 3\right) e^{t} \\ \left(1 - 3 t^{2}\right) e^{t} \\ \left(- t - 2\right) e^{t}\end{aligned}]+[\begin{aligned}- 9 t^{2} e^{t} \\ - 6 t e^{t} \\ - e^{t}\end{aligned}]\\&=[\begin{aligned}3 \left(- t^{3} - 3 t^{2} - 1\right) e^{t} \\ \left(- 3 t^{2} - 6 t + 1\right) e^{t} \\ \left(- t - 3\right) e^{t}\end{aligned}]\end{aligned}
$$

## Generated authored_moderate seed 3

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}2 - 2 t^{3} \\ 2 t^{2} + 1 \\ - 2 t - 2\end{aligned}]$ and $u(t)=e^{t}.$

- $[\begin{aligned}- 6 t^{2} e^{t} \\ 4 t e^{t} \\ - 2 e^{t}\end{aligned}]$
- $[\begin{aligned}- 2 t^{3} e^{t} - 6 t^{2} e^{t} + 2 e^{t} \\ 2 t^{2} e^{t} + 4 t e^{t} + e^{t} \\ - 2 t e^{t} - 4 e^{t}\end{aligned}]$
- $[\begin{aligned}- 2 t^{3} e^{t} - 6 t^{2} + 2 e^{t} \\ 2 t^{2} e^{t} + 4 t + e^{t} \\ - 2 t e^{t} - 2 e^{t} - 2\end{aligned}]$
- $[\begin{aligned}- 2 t^{3} e^{t} + 6 t^{2} e^{t} + 2 e^{t} \\ 2 t^{2} e^{t} - 4 t e^{t} + e^{t} \\ - 2 t e^{t}\end{aligned}]$
- $[\begin{aligned}- 2 t^{3} e^{t} + 2 e^{t} \\ 2 t^{2} e^{t} + e^{t} \\ - 2 t e^{t} - 2 e^{t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 - 2 t^{3}) \\ \frac{\text{d}}{\text{d}t}(2 t^{2} + 1) \\ \frac{\text{d}}{\text{d}t}(- 2 t - 2)\end{aligned}]=[\begin{aligned}- 6 t^{2} \\ 4 t \\ -2\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(e^{t})=e^{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(e^{t})[\begin{aligned}2 - 2 t^{3} \\ 2 t^{2} + 1 \\ - 2 t - 2\end{aligned}]+(e^{t})[\begin{aligned}- 6 t^{2} \\ 4 t \\ -2\end{aligned}]\\&=[\begin{aligned}\left(2 - 2 t^{3}\right) e^{t} \\ \left(2 t^{2} + 1\right) e^{t} \\ \left(- 2 t - 2\right) e^{t}\end{aligned}]+[\begin{aligned}- 6 t^{2} e^{t} \\ 4 t e^{t} \\ - 2 e^{t}\end{aligned}]\\&=[\begin{aligned}2 \left(- t^{3} - 3 t^{2} + 1\right) e^{t} \\ \left(2 t^{2} + 4 t + 1\right) e^{t} \\ 2 \left(- t - 2\right) e^{t}\end{aligned}]\end{aligned}
$$

## Generated authored_moderate seed 4

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}- 2 t^{3} - 1 \\ 1 - 3 t^{2} \\ 3 t - 2\end{aligned}]$ and $u(t)=e^{t}.$

- $[\begin{aligned}- 6 t^{2} e^{t} \\ - 6 t e^{t} \\ 3 e^{t}\end{aligned}]$
- $[\begin{aligned}- 2 t^{3} e^{t} - e^{t} \\ - 3 t^{2} e^{t} + e^{t} \\ 3 t e^{t} - 2 e^{t}\end{aligned}]$
- $[\begin{aligned}- 2 t^{3} e^{t} - 6 t^{2} e^{t} - e^{t} \\ - 3 t^{2} e^{t} - 6 t e^{t} + e^{t} \\ 3 t e^{t} + e^{t}\end{aligned}]$
- $[\begin{aligned}- 2 t^{3} e^{t} - 6 t^{2} - e^{t} \\ - 3 t^{2} e^{t} - 6 t + e^{t} \\ 3 t e^{t} - 2 e^{t} + 3\end{aligned}]$
- $[\begin{aligned}- 2 t^{3} e^{t} + 6 t^{2} e^{t} - e^{t} \\ - 3 t^{2} e^{t} + 6 t e^{t} + e^{t} \\ 3 t e^{t} - 5 e^{t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(- 2 t^{3} - 1) \\ \frac{\text{d}}{\text{d}t}(1 - 3 t^{2}) \\ \frac{\text{d}}{\text{d}t}(3 t - 2)\end{aligned}]=[\begin{aligned}- 6 t^{2} \\ - 6 t \\ 3\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(e^{t})=e^{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(e^{t})[\begin{aligned}- 2 t^{3} - 1 \\ 1 - 3 t^{2} \\ 3 t - 2\end{aligned}]+(e^{t})[\begin{aligned}- 6 t^{2} \\ - 6 t \\ 3\end{aligned}]\\&=[\begin{aligned}\left(- 2 t^{3} - 1\right) e^{t} \\ \left(1 - 3 t^{2}\right) e^{t} \\ \left(3 t - 2\right) e^{t}\end{aligned}]+[\begin{aligned}- 6 t^{2} e^{t} \\ - 6 t e^{t} \\ 3 e^{t}\end{aligned}]\\&=[\begin{aligned}\left(- 2 t^{3} - 6 t^{2} - 1\right) e^{t} \\ \left(- 3 t^{2} - 6 t + 1\right) e^{t} \\ \left(3 t + 1\right) e^{t}\end{aligned}]\end{aligned}
$$

## Generated authored_moderate seed 5

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}2 t^{3} - 1 \\ 3 t^{2} + 1 \\ - t - 2\end{aligned}]$ and $u(t)=e^{t}.$

- $[\begin{aligned}2 t^{3} e^{t} - e^{t} \\ 3 t^{2} e^{t} + e^{t} \\ - t e^{t} - 2 e^{t}\end{aligned}]$
- $[\begin{aligned}2 t^{3} e^{t} - 6 t^{2} e^{t} - e^{t} \\ 3 t^{2} e^{t} - 6 t e^{t} + e^{t} \\ - t e^{t} - e^{t}\end{aligned}]$
- $[\begin{aligned}6 t^{2} e^{t} \\ 6 t e^{t} \\ - e^{t}\end{aligned}]$
- $[\begin{aligned}2 t^{3} e^{t} + 6 t^{2} e^{t} - e^{t} \\ 3 t^{2} e^{t} + 6 t e^{t} + e^{t} \\ - t e^{t} - 3 e^{t}\end{aligned}]$
- $[\begin{aligned}2 t^{3} e^{t} + 6 t^{2} - e^{t} \\ 3 t^{2} e^{t} + 6 t + e^{t} \\ - t e^{t} - 2 e^{t} - 1\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 t^{3} - 1) \\ \frac{\text{d}}{\text{d}t}(3 t^{2} + 1) \\ \frac{\text{d}}{\text{d}t}(- t - 2)\end{aligned}]=[\begin{aligned}6 t^{2} \\ 6 t \\ -1\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(e^{t})=e^{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(e^{t})[\begin{aligned}2 t^{3} - 1 \\ 3 t^{2} + 1 \\ - t - 2\end{aligned}]+(e^{t})[\begin{aligned}6 t^{2} \\ 6 t \\ -1\end{aligned}]\\&=[\begin{aligned}\left(2 t^{3} - 1\right) e^{t} \\ \left(3 t^{2} + 1\right) e^{t} \\ \left(- t - 2\right) e^{t}\end{aligned}]+[\begin{aligned}6 t^{2} e^{t} \\ 6 t e^{t} \\ - e^{t}\end{aligned}]\\&=[\begin{aligned}\left(2 t^{3} + 6 t^{2} - 1\right) e^{t} \\ \left(3 t^{2} + 6 t + 1\right) e^{t} \\ \left(- t - 3\right) e^{t}\end{aligned}]\end{aligned}
$$

## Generated authored_moderate seed 6

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}2 t^{3} - 3 \\ t^{2} + 1 \\ - t - 2\end{aligned}]$ and $u(t)=e^{t}.$

- $[\begin{aligned}2 t^{3} e^{t} - 3 e^{t} \\ t^{2} e^{t} + e^{t} \\ - t e^{t} - 2 e^{t}\end{aligned}]$
- $[\begin{aligned}6 t^{2} e^{t} \\ 2 t e^{t} \\ - e^{t}\end{aligned}]$
- $[\begin{aligned}2 t^{3} e^{t} - 6 t^{2} e^{t} - 3 e^{t} \\ t^{2} e^{t} - 2 t e^{t} + e^{t} \\ - t e^{t} - e^{t}\end{aligned}]$
- $[\begin{aligned}2 t^{3} e^{t} + 6 t^{2} - 3 e^{t} \\ t^{2} e^{t} + 2 t + e^{t} \\ - t e^{t} - 2 e^{t} - 1\end{aligned}]$
- $[\begin{aligned}2 t^{3} e^{t} + 6 t^{2} e^{t} - 3 e^{t} \\ t^{2} e^{t} + 2 t e^{t} + e^{t} \\ - t e^{t} - 3 e^{t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 t^{3} - 3) \\ \frac{\text{d}}{\text{d}t}(t^{2} + 1) \\ \frac{\text{d}}{\text{d}t}(- t - 2)\end{aligned}]=[\begin{aligned}6 t^{2} \\ 2 t \\ -1\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(e^{t})=e^{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(e^{t})[\begin{aligned}2 t^{3} - 3 \\ t^{2} + 1 \\ - t - 2\end{aligned}]+(e^{t})[\begin{aligned}6 t^{2} \\ 2 t \\ -1\end{aligned}]\\&=[\begin{aligned}\left(2 t^{3} - 3\right) e^{t} \\ \left(t^{2} + 1\right) e^{t} \\ \left(- t - 2\right) e^{t}\end{aligned}]+[\begin{aligned}6 t^{2} e^{t} \\ 2 t e^{t} \\ - e^{t}\end{aligned}]\\&=[\begin{aligned}\left(2 t^{3} + 6 t^{2} - 3\right) e^{t} \\ \left(t^{2} + 2 t + 1\right) e^{t} \\ \left(- t - 3\right) e^{t}\end{aligned}]\end{aligned}
$$

## Generated authored_moderate seed 7

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}- t^{3} - 2 \\ t^{2} + 1 \\ 3 t - 2\end{aligned}]$ and $u(t)=e^{t}.$

- $[\begin{aligned}- 3 t^{2} e^{t} \\ 2 t e^{t} \\ 3 e^{t}\end{aligned}]$
- $[\begin{aligned}- t^{3} e^{t} + 3 t^{2} e^{t} - 2 e^{t} \\ t^{2} e^{t} - 2 t e^{t} + e^{t} \\ 3 t e^{t} - 5 e^{t}\end{aligned}]$
- $[\begin{aligned}- t^{3} e^{t} - 2 e^{t} \\ t^{2} e^{t} + e^{t} \\ 3 t e^{t} - 2 e^{t}\end{aligned}]$
- $[\begin{aligned}- t^{3} e^{t} - 3 t^{2} - 2 e^{t} \\ t^{2} e^{t} + 2 t + e^{t} \\ 3 t e^{t} - 2 e^{t} + 3\end{aligned}]$
- $[\begin{aligned}- t^{3} e^{t} - 3 t^{2} e^{t} - 2 e^{t} \\ t^{2} e^{t} + 2 t e^{t} + e^{t} \\ 3 t e^{t} + e^{t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(- t^{3} - 2) \\ \frac{\text{d}}{\text{d}t}(t^{2} + 1) \\ \frac{\text{d}}{\text{d}t}(3 t - 2)\end{aligned}]=[\begin{aligned}- 3 t^{2} \\ 2 t \\ 3\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(e^{t})=e^{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(e^{t})[\begin{aligned}- t^{3} - 2 \\ t^{2} + 1 \\ 3 t - 2\end{aligned}]+(e^{t})[\begin{aligned}- 3 t^{2} \\ 2 t \\ 3\end{aligned}]\\&=[\begin{aligned}\left(- t^{3} - 2\right) e^{t} \\ \left(t^{2} + 1\right) e^{t} \\ \left(3 t - 2\right) e^{t}\end{aligned}]+[\begin{aligned}- 3 t^{2} e^{t} \\ 2 t e^{t} \\ 3 e^{t}\end{aligned}]\\&=[\begin{aligned}\left(- t^{3} - 3 t^{2} - 2\right) e^{t} \\ \left(t^{2} + 2 t + 1\right) e^{t} \\ \left(3 t + 1\right) e^{t}\end{aligned}]\end{aligned}
$$

## Generated authored_moderate seed 8

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}- 2 t^{3} - 1 \\ t^{2} + 1 \\ - 2 t - 2\end{aligned}]$ and $u(t)=e^{t}.$

- $[\begin{aligned}- 2 t^{3} e^{t} - 6 t^{2} - e^{t} \\ t^{2} e^{t} + 2 t + e^{t} \\ - 2 t e^{t} - 2 e^{t} - 2\end{aligned}]$
- $[\begin{aligned}- 2 t^{3} e^{t} - e^{t} \\ t^{2} e^{t} + e^{t} \\ - 2 t e^{t} - 2 e^{t}\end{aligned}]$
- $[\begin{aligned}- 2 t^{3} e^{t} + 6 t^{2} e^{t} - e^{t} \\ t^{2} e^{t} - 2 t e^{t} + e^{t} \\ - 2 t e^{t}\end{aligned}]$
- $[\begin{aligned}- 2 t^{3} e^{t} - 6 t^{2} e^{t} - e^{t} \\ t^{2} e^{t} + 2 t e^{t} + e^{t} \\ - 2 t e^{t} - 4 e^{t}\end{aligned}]$
- $[\begin{aligned}- 6 t^{2} e^{t} \\ 2 t e^{t} \\ - 2 e^{t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(- 2 t^{3} - 1) \\ \frac{\text{d}}{\text{d}t}(t^{2} + 1) \\ \frac{\text{d}}{\text{d}t}(- 2 t - 2)\end{aligned}]=[\begin{aligned}- 6 t^{2} \\ 2 t \\ -2\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(e^{t})=e^{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(e^{t})[\begin{aligned}- 2 t^{3} - 1 \\ t^{2} + 1 \\ - 2 t - 2\end{aligned}]+(e^{t})[\begin{aligned}- 6 t^{2} \\ 2 t \\ -2\end{aligned}]\\&=[\begin{aligned}\left(- 2 t^{3} - 1\right) e^{t} \\ \left(t^{2} + 1\right) e^{t} \\ \left(- 2 t - 2\right) e^{t}\end{aligned}]+[\begin{aligned}- 6 t^{2} e^{t} \\ 2 t e^{t} \\ - 2 e^{t}\end{aligned}]\\&=[\begin{aligned}\left(- 2 t^{3} - 6 t^{2} - 1\right) e^{t} \\ \left(t^{2} + 2 t + 1\right) e^{t} \\ 2 \left(- t - 2\right) e^{t}\end{aligned}]\end{aligned}
$$

## Generated authored_moderate seed 9

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}t^{3} + 2 \\ 1 - t^{2} \\ - t - 2\end{aligned}]$ and $u(t)=e^{t}.$

- $[\begin{aligned}t^{3} e^{t} - 3 t^{2} e^{t} + 2 e^{t} \\ - t^{2} e^{t} + 2 t e^{t} + e^{t} \\ - t e^{t} - e^{t}\end{aligned}]$
- $[\begin{aligned}t^{3} e^{t} + 3 t^{2} e^{t} + 2 e^{t} \\ - t^{2} e^{t} - 2 t e^{t} + e^{t} \\ - t e^{t} - 3 e^{t}\end{aligned}]$
- $[\begin{aligned}t^{3} e^{t} + 2 e^{t} \\ - t^{2} e^{t} + e^{t} \\ - t e^{t} - 2 e^{t}\end{aligned}]$
- $[\begin{aligned}t^{3} e^{t} + 3 t^{2} + 2 e^{t} \\ - t^{2} e^{t} - 2 t + e^{t} \\ - t e^{t} - 2 e^{t} - 1\end{aligned}]$
- $[\begin{aligned}3 t^{2} e^{t} \\ - 2 t e^{t} \\ - e^{t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(t^{3} + 2) \\ \frac{\text{d}}{\text{d}t}(1 - t^{2}) \\ \frac{\text{d}}{\text{d}t}(- t - 2)\end{aligned}]=[\begin{aligned}3 t^{2} \\ - 2 t \\ -1\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(e^{t})=e^{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(e^{t})[\begin{aligned}t^{3} + 2 \\ 1 - t^{2} \\ - t - 2\end{aligned}]+(e^{t})[\begin{aligned}3 t^{2} \\ - 2 t \\ -1\end{aligned}]\\&=[\begin{aligned}\left(t^{3} + 2\right) e^{t} \\ \left(1 - t^{2}\right) e^{t} \\ \left(- t - 2\right) e^{t}\end{aligned}]+[\begin{aligned}3 t^{2} e^{t} \\ - 2 t e^{t} \\ - e^{t}\end{aligned}]\\&=[\begin{aligned}\left(t^{3} + 3 t^{2} + 2\right) e^{t} \\ \left(- t^{2} - 2 t + 1\right) e^{t} \\ \left(- t - 3\right) e^{t}\end{aligned}]\end{aligned}
$$

## Generated authored_moderate seed 10

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}2 t^{3} - 3 \\ t^{2} + 1 \\ t - 2\end{aligned}]$ and $u(t)=e^{t}.$

- $[\begin{aligned}2 t^{3} e^{t} - 3 e^{t} \\ t^{2} e^{t} + e^{t} \\ t e^{t} - 2 e^{t}\end{aligned}]$
- $[\begin{aligned}6 t^{2} e^{t} \\ 2 t e^{t} \\ e^{t}\end{aligned}]$
- $[\begin{aligned}2 t^{3} e^{t} - 6 t^{2} e^{t} - 3 e^{t} \\ t^{2} e^{t} - 2 t e^{t} + e^{t} \\ t e^{t} - 3 e^{t}\end{aligned}]$
- $[\begin{aligned}2 t^{3} e^{t} + 6 t^{2} e^{t} - 3 e^{t} \\ t^{2} e^{t} + 2 t e^{t} + e^{t} \\ t e^{t} - e^{t}\end{aligned}]$
- $[\begin{aligned}2 t^{3} e^{t} + 6 t^{2} - 3 e^{t} \\ t^{2} e^{t} + 2 t + e^{t} \\ t e^{t} - 2 e^{t} + 1\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 t^{3} - 3) \\ \frac{\text{d}}{\text{d}t}(t^{2} + 1) \\ \frac{\text{d}}{\text{d}t}(t - 2)\end{aligned}]=[\begin{aligned}6 t^{2} \\ 2 t \\ 1\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(e^{t})=e^{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(e^{t})[\begin{aligned}2 t^{3} - 3 \\ t^{2} + 1 \\ t - 2\end{aligned}]+(e^{t})[\begin{aligned}6 t^{2} \\ 2 t \\ 1\end{aligned}]\\&=[\begin{aligned}\left(2 t^{3} - 3\right) e^{t} \\ \left(t^{2} + 1\right) e^{t} \\ \left(t - 2\right) e^{t}\end{aligned}]+[\begin{aligned}6 t^{2} e^{t} \\ 2 t e^{t} \\ e^{t}\end{aligned}]\\&=[\begin{aligned}\left(2 t^{3} + 6 t^{2} - 3\right) e^{t} \\ \left(t^{2} + 2 t + 1\right) e^{t} \\ \left(t - 1\right) e^{t}\end{aligned}]\end{aligned}
$$

## Generated authored_moderate seed 11

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}t^{3} + 2 \\ t^{2} + 1 \\ t - 2\end{aligned}]$ and $u(t)=e^{t}.$

- $[\begin{aligned}t^{3} e^{t} + 2 e^{t} \\ t^{2} e^{t} + e^{t} \\ t e^{t} - 2 e^{t}\end{aligned}]$
- $[\begin{aligned}t^{3} e^{t} - 3 t^{2} e^{t} + 2 e^{t} \\ t^{2} e^{t} - 2 t e^{t} + e^{t} \\ t e^{t} - 3 e^{t}\end{aligned}]$
- $[\begin{aligned}t^{3} e^{t} + 3 t^{2} e^{t} + 2 e^{t} \\ t^{2} e^{t} + 2 t e^{t} + e^{t} \\ t e^{t} - e^{t}\end{aligned}]$
- $[\begin{aligned}3 t^{2} e^{t} \\ 2 t e^{t} \\ e^{t}\end{aligned}]$
- $[\begin{aligned}t^{3} e^{t} + 3 t^{2} + 2 e^{t} \\ t^{2} e^{t} + 2 t + e^{t} \\ t e^{t} - 2 e^{t} + 1\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(t^{3} + 2) \\ \frac{\text{d}}{\text{d}t}(t^{2} + 1) \\ \frac{\text{d}}{\text{d}t}(t - 2)\end{aligned}]=[\begin{aligned}3 t^{2} \\ 2 t \\ 1\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(e^{t})=e^{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(e^{t})[\begin{aligned}t^{3} + 2 \\ t^{2} + 1 \\ t - 2\end{aligned}]+(e^{t})[\begin{aligned}3 t^{2} \\ 2 t \\ 1\end{aligned}]\\&=[\begin{aligned}\left(t^{3} + 2\right) e^{t} \\ \left(t^{2} + 1\right) e^{t} \\ \left(t - 2\right) e^{t}\end{aligned}]+[\begin{aligned}3 t^{2} e^{t} \\ 2 t e^{t} \\ e^{t}\end{aligned}]\\&=[\begin{aligned}\left(t^{3} + 3 t^{2} + 2\right) e^{t} \\ \left(t^{2} + 2 t + 1\right) e^{t} \\ \left(t - 1\right) e^{t}\end{aligned}]\end{aligned}
$$

## Generated authored_hard seed 0

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}- 3 \ln{\left(t \right)} \\ - e^{t} \\ \frac{1}{t}\end{aligned}]$ and $u(t)=t^{2} + t + 1.$

- $[\begin{aligned}- 6 t \ln{\left(t \right)} - 3 t - 3 \ln{\left(t \right)} - 3 - \frac{3}{t} \\ - t^{2} e^{t} - 3 t e^{t} - 2 e^{t} \\ 1 - \frac{1}{t^{2}}\end{aligned}]$
- $[\begin{aligned}- 6 t \ln{\left(t \right)} - 3 \ln{\left(t \right)} \\ - 2 t e^{t} - e^{t} \\ 2 + \frac{1}{t}\end{aligned}]$
- $[\begin{aligned}- 3 t - 3 - \frac{3}{t} \\ - t^{2} e^{t} - t e^{t} - e^{t} \\ -1 - \frac{1}{t} - \frac{1}{t^{2}}\end{aligned}]$
- $[\begin{aligned}- 6 t \ln{\left(t \right)} + 3 t - 3 \ln{\left(t \right)} + 3 + \frac{3}{t} \\ t^{2} e^{t} - t e^{t} \\ 3 + \frac{2}{t} + \frac{1}{t^{2}}\end{aligned}]$
- $[\begin{aligned}-6 - \frac{3}{t} \\ - 2 t e^{t} - e^{t} \\ - \frac{2}{t} - \frac{1}{t^{2}}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(- 3 \ln{\left(t \right)}) \\ \frac{\text{d}}{\text{d}t}(- e^{t}) \\ \frac{\text{d}}{\text{d}t}(\frac{1}{t})\end{aligned}]=[\begin{aligned}- \frac{3}{t} \\ - e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2} + t + 1)=2 t + 1\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t + 1)[\begin{aligned}- 3 \ln{\left(t \right)} \\ - e^{t} \\ \frac{1}{t}\end{aligned}]+(t^{2} + t + 1)[\begin{aligned}- \frac{3}{t} \\ - e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\&=[\begin{aligned}- 3 \left(2 t + 1\right) \ln{\left(t \right)} \\ - \left(2 t + 1\right) e^{t} \\ \frac{2 t + 1}{t}\end{aligned}]+[\begin{aligned}- \frac{3 \left(t^{2} + t + 1\right)}{t} \\ - \left(t^{2} + t + 1\right) e^{t} \\ - \frac{t^{2} + t + 1}{t^{2}}\end{aligned}]\\&=[\begin{aligned}- 6 t \ln{\left(t \right)} - 3 t - 3 \ln{\left(t \right)} - 3 - \frac{3}{t} \\ \left(- t^{2} - 3 t - 2\right) e^{t} \\ 1 - \frac{1}{t^{2}}\end{aligned}]\end{aligned}
$$

## Generated authored_hard seed 1

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}- 3 \ln{\left(t \right)} \\ - e^{t} \\ \frac{1}{t}\end{aligned}]$ and $u(t)=t^{2} - 2 t + 2.$

- $[\begin{aligned}-6 + \frac{6}{t} \\ - 2 t e^{t} + 2 e^{t} \\ - \frac{2}{t} + \frac{2}{t^{2}}\end{aligned}]$
- $[\begin{aligned}- 6 t \ln{\left(t \right)} + 6 \ln{\left(t \right)} \\ - 2 t e^{t} + 2 e^{t} \\ 2 - \frac{2}{t}\end{aligned}]$
- $[\begin{aligned}- 3 t + 6 - \frac{6}{t} \\ - t^{2} e^{t} + 2 t e^{t} - 2 e^{t} \\ -1 + \frac{2}{t} - \frac{2}{t^{2}}\end{aligned}]$
- $[\begin{aligned}- 6 t \ln{\left(t \right)} + 3 t + 6 \ln{\left(t \right)} - 6 + \frac{6}{t} \\ t^{2} e^{t} - 4 t e^{t} + 4 e^{t} \\ 3 - \frac{4}{t} + \frac{2}{t^{2}}\end{aligned}]$
- $[\begin{aligned}- 6 t \ln{\left(t \right)} - 3 t + 6 \ln{\left(t \right)} + 6 - \frac{6}{t} \\ - t^{2} e^{t} \\ 1 - \frac{2}{t^{2}}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(- 3 \ln{\left(t \right)}) \\ \frac{\text{d}}{\text{d}t}(- e^{t}) \\ \frac{\text{d}}{\text{d}t}(\frac{1}{t})\end{aligned}]=[\begin{aligned}- \frac{3}{t} \\ - e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2} - 2 t + 2)=2 t - 2\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t - 2)[\begin{aligned}- 3 \ln{\left(t \right)} \\ - e^{t} \\ \frac{1}{t}\end{aligned}]+(t^{2} - 2 t + 2)[\begin{aligned}- \frac{3}{t} \\ - e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\&=[\begin{aligned}- 3 \left(2 t - 2\right) \ln{\left(t \right)} \\ - \left(2 t - 2\right) e^{t} \\ \frac{2 t - 2}{t}\end{aligned}]+[\begin{aligned}- \frac{3 \left(t^{2} - 2 t + 2\right)}{t} \\ - \left(t^{2} - 2 t + 2\right) e^{t} \\ - \frac{t^{2} - 2 t + 2}{t^{2}}\end{aligned}]\\&=[\begin{aligned}- 6 t \ln{\left(t \right)} - 3 t + 6 \ln{\left(t \right)} + 6 - \frac{6}{t} \\ - t^{2} e^{t} \\ 1 - \frac{2}{t^{2}}\end{aligned}]\end{aligned}
$$

## Generated authored_hard seed 2

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}- 3 \ln{\left(t \right)} \\ - e^{t} \\ \frac{1}{t}\end{aligned}]$ and $u(t)=t^{2} - 3 t - 3.$

- $[\begin{aligned}- 6 t \ln{\left(t \right)} + 3 t + 9 \ln{\left(t \right)} - 9 - \frac{9}{t} \\ t^{2} e^{t} - 5 t e^{t} \\ 3 - \frac{6}{t} - \frac{3}{t^{2}}\end{aligned}]$
- $[\begin{aligned}- 6 t \ln{\left(t \right)} - 3 t + 9 \ln{\left(t \right)} + 9 + \frac{9}{t} \\ - t^{2} e^{t} + t e^{t} + 6 e^{t} \\ 1 + \frac{3}{t^{2}}\end{aligned}]$
- $[\begin{aligned}-6 + \frac{9}{t} \\ - 2 t e^{t} + 3 e^{t} \\ - \frac{2}{t} + \frac{3}{t^{2}}\end{aligned}]$
- $[\begin{aligned}- 6 t \ln{\left(t \right)} + 9 \ln{\left(t \right)} \\ - 2 t e^{t} + 3 e^{t} \\ 2 - \frac{3}{t}\end{aligned}]$
- $[\begin{aligned}- 3 t + 9 + \frac{9}{t} \\ - t^{2} e^{t} + 3 t e^{t} + 3 e^{t} \\ -1 + \frac{3}{t} + \frac{3}{t^{2}}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(- 3 \ln{\left(t \right)}) \\ \frac{\text{d}}{\text{d}t}(- e^{t}) \\ \frac{\text{d}}{\text{d}t}(\frac{1}{t})\end{aligned}]=[\begin{aligned}- \frac{3}{t} \\ - e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2} - 3 t - 3)=2 t - 3\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t - 3)[\begin{aligned}- 3 \ln{\left(t \right)} \\ - e^{t} \\ \frac{1}{t}\end{aligned}]+(t^{2} - 3 t - 3)[\begin{aligned}- \frac{3}{t} \\ - e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\&=[\begin{aligned}- 3 \left(2 t - 3\right) \ln{\left(t \right)} \\ - \left(2 t - 3\right) e^{t} \\ \frac{2 t - 3}{t}\end{aligned}]+[\begin{aligned}- \frac{3 \left(t^{2} - 3 t - 3\right)}{t} \\ - \left(t^{2} - 3 t - 3\right) e^{t} \\ - \frac{t^{2} - 3 t - 3}{t^{2}}\end{aligned}]\\&=[\begin{aligned}- 6 t \ln{\left(t \right)} - 3 t + 9 \ln{\left(t \right)} + 9 + \frac{9}{t} \\ \left(- t^{2} + t + 6\right) e^{t} \\ 1 + \frac{3}{t^{2}}\end{aligned}]\end{aligned}
$$

## Generated authored_hard seed 3

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}2 \ln{\left(t \right)} \\ - 2 e^{t} \\ \frac{1}{t}\end{aligned}]$ and $u(t)=t^{2} - 2 t + 2.$

- $[\begin{aligned}2 t - 4 + \frac{4}{t} \\ - 2 t^{2} e^{t} + 4 t e^{t} - 4 e^{t} \\ -1 + \frac{2}{t} - \frac{2}{t^{2}}\end{aligned}]$
- $[\begin{aligned}4 t \ln{\left(t \right)} + 2 t - 4 \ln{\left(t \right)} - 4 + \frac{4}{t} \\ - 2 t^{2} e^{t} \\ 1 - \frac{2}{t^{2}}\end{aligned}]$
- $[\begin{aligned}4 - \frac{4}{t} \\ - 4 t e^{t} + 4 e^{t} \\ - \frac{2}{t} + \frac{2}{t^{2}}\end{aligned}]$
- $[\begin{aligned}4 t \ln{\left(t \right)} - 2 t - 4 \ln{\left(t \right)} + 4 - \frac{4}{t} \\ 2 t^{2} e^{t} - 8 t e^{t} + 8 e^{t} \\ 3 - \frac{4}{t} + \frac{2}{t^{2}}\end{aligned}]$
- $[\begin{aligned}4 t \ln{\left(t \right)} - 4 \ln{\left(t \right)} \\ - 4 t e^{t} + 4 e^{t} \\ 2 - \frac{2}{t}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 \ln{\left(t \right)}) \\ \frac{\text{d}}{\text{d}t}(- 2 e^{t}) \\ \frac{\text{d}}{\text{d}t}(\frac{1}{t})\end{aligned}]=[\begin{aligned}\frac{2}{t} \\ - 2 e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2} - 2 t + 2)=2 t - 2\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t - 2)[\begin{aligned}2 \ln{\left(t \right)} \\ - 2 e^{t} \\ \frac{1}{t}\end{aligned}]+(t^{2} - 2 t + 2)[\begin{aligned}\frac{2}{t} \\ - 2 e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\&=[\begin{aligned}2 \left(2 t - 2\right) \ln{\left(t \right)} \\ - 2 \left(2 t - 2\right) e^{t} \\ \frac{2 t - 2}{t}\end{aligned}]+[\begin{aligned}\frac{2 \left(t^{2} - 2 t + 2\right)}{t} \\ - 2 \left(t^{2} - 2 t + 2\right) e^{t} \\ - \frac{t^{2} - 2 t + 2}{t^{2}}\end{aligned}]\\&=[\begin{aligned}4 t \ln{\left(t \right)} + 2 t - 4 \ln{\left(t \right)} - 4 + \frac{4}{t} \\ - 2 t^{2} e^{t} \\ 1 - \frac{2}{t^{2}}\end{aligned}]\end{aligned}
$$

## Generated authored_hard seed 4

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}- 3 \ln{\left(t \right)} \\ 3 e^{t} \\ \frac{1}{t}\end{aligned}]$ and $u(t)=t^{2} - 2 t - 1.$

- $[\begin{aligned}- 3 t + 6 + \frac{3}{t} \\ 3 t^{2} e^{t} - 6 t e^{t} - 3 e^{t} \\ -1 + \frac{2}{t} + \frac{1}{t^{2}}\end{aligned}]$
- $[\begin{aligned}- 6 t \ln{\left(t \right)} + 6 \ln{\left(t \right)} \\ 6 t e^{t} - 6 e^{t} \\ 2 - \frac{2}{t}\end{aligned}]$
- $[\begin{aligned}- 6 t \ln{\left(t \right)} - 3 t + 6 \ln{\left(t \right)} + 6 + \frac{3}{t} \\ 3 t^{2} e^{t} - 9 e^{t} \\ 1 + \frac{1}{t^{2}}\end{aligned}]$
- $[\begin{aligned}-6 + \frac{6}{t} \\ 6 t e^{t} - 6 e^{t} \\ - \frac{2}{t} + \frac{2}{t^{2}}\end{aligned}]$
- $[\begin{aligned}- 6 t \ln{\left(t \right)} + 3 t + 6 \ln{\left(t \right)} - 6 - \frac{3}{t} \\ - 3 t^{2} e^{t} + 12 t e^{t} - 3 e^{t} \\ 3 - \frac{4}{t} - \frac{1}{t^{2}}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(- 3 \ln{\left(t \right)}) \\ \frac{\text{d}}{\text{d}t}(3 e^{t}) \\ \frac{\text{d}}{\text{d}t}(\frac{1}{t})\end{aligned}]=[\begin{aligned}- \frac{3}{t} \\ 3 e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2} - 2 t - 1)=2 t - 2\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t - 2)[\begin{aligned}- 3 \ln{\left(t \right)} \\ 3 e^{t} \\ \frac{1}{t}\end{aligned}]+(t^{2} - 2 t - 1)[\begin{aligned}- \frac{3}{t} \\ 3 e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\&=[\begin{aligned}- 3 \left(2 t - 2\right) \ln{\left(t \right)} \\ 3 \left(2 t - 2\right) e^{t} \\ \frac{2 t - 2}{t}\end{aligned}]+[\begin{aligned}- \frac{3 \left(t^{2} - 2 t - 1\right)}{t} \\ 3 \left(t^{2} - 2 t - 1\right) e^{t} \\ - \frac{t^{2} - 2 t - 1}{t^{2}}\end{aligned}]\\&=[\begin{aligned}- 6 t \ln{\left(t \right)} - 3 t + 6 \ln{\left(t \right)} + 6 + \frac{3}{t} \\ 3 \left(t^{2} - 3\right) e^{t} \\ 1 + \frac{1}{t^{2}}\end{aligned}]\end{aligned}
$$

## Generated authored_hard seed 5

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}3 \ln{\left(t \right)} \\ - e^{t} \\ \frac{1}{t}\end{aligned}]$ and $u(t)=t^{2} + 2 t - 1.$

- $[\begin{aligned}6 t \ln{\left(t \right)} + 6 \ln{\left(t \right)} \\ - 2 t e^{t} - 2 e^{t} \\ 2 + \frac{2}{t}\end{aligned}]$
- $[\begin{aligned}6 t \ln{\left(t \right)} - 3 t + 6 \ln{\left(t \right)} - 6 + \frac{3}{t} \\ t^{2} e^{t} - 3 e^{t} \\ 3 + \frac{4}{t} - \frac{1}{t^{2}}\end{aligned}]$
- $[\begin{aligned}3 t + 6 - \frac{3}{t} \\ - t^{2} e^{t} - 2 t e^{t} + e^{t} \\ -1 - \frac{2}{t} + \frac{1}{t^{2}}\end{aligned}]$
- $[\begin{aligned}6 t \ln{\left(t \right)} + 3 t + 6 \ln{\left(t \right)} + 6 - \frac{3}{t} \\ - t^{2} e^{t} - 4 t e^{t} - e^{t} \\ 1 + \frac{1}{t^{2}}\end{aligned}]$
- $[\begin{aligned}6 + \frac{6}{t} \\ - 2 t e^{t} - 2 e^{t} \\ - \frac{2}{t} - \frac{2}{t^{2}}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(3 \ln{\left(t \right)}) \\ \frac{\text{d}}{\text{d}t}(- e^{t}) \\ \frac{\text{d}}{\text{d}t}(\frac{1}{t})\end{aligned}]=[\begin{aligned}\frac{3}{t} \\ - e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2} + 2 t - 1)=2 t + 2\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t + 2)[\begin{aligned}3 \ln{\left(t \right)} \\ - e^{t} \\ \frac{1}{t}\end{aligned}]+(t^{2} + 2 t - 1)[\begin{aligned}\frac{3}{t} \\ - e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\&=[\begin{aligned}3 \left(2 t + 2\right) \ln{\left(t \right)} \\ - \left(2 t + 2\right) e^{t} \\ \frac{2 t + 2}{t}\end{aligned}]+[\begin{aligned}\frac{3 \left(t^{2} + 2 t - 1\right)}{t} \\ - \left(t^{2} + 2 t - 1\right) e^{t} \\ - \frac{t^{2} + 2 t - 1}{t^{2}}\end{aligned}]\\&=[\begin{aligned}6 t \ln{\left(t \right)} + 3 t + 6 \ln{\left(t \right)} + 6 - \frac{3}{t} \\ \left(- t^{2} - 4 t - 1\right) e^{t} \\ 1 + \frac{1}{t^{2}}\end{aligned}]\end{aligned}
$$

## Generated authored_hard seed 6

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}\ln{\left(t \right)} \\ - e^{t} \\ \frac{1}{t}\end{aligned}]$ and $u(t)=t^{2} + 2 t - 3.$

- $[\begin{aligned}2 t \ln{\left(t \right)} + 2 \ln{\left(t \right)} \\ - 2 t e^{t} - 2 e^{t} \\ 2 + \frac{2}{t}\end{aligned}]$
- $[\begin{aligned}t + 2 - \frac{3}{t} \\ - t^{2} e^{t} - 2 t e^{t} + 3 e^{t} \\ -1 - \frac{2}{t} + \frac{3}{t^{2}}\end{aligned}]$
- $[\begin{aligned}2 t \ln{\left(t \right)} - t + 2 \ln{\left(t \right)} - 2 + \frac{3}{t} \\ t^{2} e^{t} - 5 e^{t} \\ 3 + \frac{4}{t} - \frac{3}{t^{2}}\end{aligned}]$
- $[\begin{aligned}2 + \frac{2}{t} \\ - 2 t e^{t} - 2 e^{t} \\ - \frac{2}{t} - \frac{2}{t^{2}}\end{aligned}]$
- $[\begin{aligned}2 t \ln{\left(t \right)} + t + 2 \ln{\left(t \right)} + 2 - \frac{3}{t} \\ - t^{2} e^{t} - 4 t e^{t} + e^{t} \\ 1 + \frac{3}{t^{2}}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(\ln{\left(t \right)}) \\ \frac{\text{d}}{\text{d}t}(- e^{t}) \\ \frac{\text{d}}{\text{d}t}(\frac{1}{t})\end{aligned}]=[\begin{aligned}\frac{1}{t} \\ - e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2} + 2 t - 3)=2 t + 2\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t + 2)[\begin{aligned}\ln{\left(t \right)} \\ - e^{t} \\ \frac{1}{t}\end{aligned}]+(t^{2} + 2 t - 3)[\begin{aligned}\frac{1}{t} \\ - e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\&=[\begin{aligned}\left(2 t + 2\right) \ln{\left(t \right)} \\ - \left(2 t + 2\right) e^{t} \\ \frac{2 t + 2}{t}\end{aligned}]+[\begin{aligned}\frac{t^{2} + 2 t - 3}{t} \\ - \left(t^{2} + 2 t - 3\right) e^{t} \\ - \frac{t^{2} + 2 t - 3}{t^{2}}\end{aligned}]\\&=[\begin{aligned}2 t \ln{\left(t \right)} + t + 2 \ln{\left(t \right)} + 2 - \frac{3}{t} \\ \left(- t^{2} - 4 t + 1\right) e^{t} \\ 1 + \frac{3}{t^{2}}\end{aligned}]\end{aligned}
$$

## Generated authored_hard seed 7

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}\ln{\left(t \right)} \\ 3 e^{t} \\ \frac{1}{t}\end{aligned}]$ and $u(t)=t^{2} - t - 2.$

- $[\begin{aligned}t - 1 - \frac{2}{t} \\ 3 t^{2} e^{t} - 3 t e^{t} - 6 e^{t} \\ -1 + \frac{1}{t} + \frac{2}{t^{2}}\end{aligned}]$
- $[\begin{aligned}2 t \ln{\left(t \right)} - t - \ln{\left(t \right)} + 1 + \frac{2}{t} \\ - 3 t^{2} e^{t} + 9 t e^{t} + 3 e^{t} \\ 3 - \frac{2}{t} - \frac{2}{t^{2}}\end{aligned}]$
- $[\begin{aligned}2 t \ln{\left(t \right)} - \ln{\left(t \right)} \\ 6 t e^{t} - 3 e^{t} \\ 2 - \frac{1}{t}\end{aligned}]$
- $[\begin{aligned}2 - \frac{1}{t} \\ 6 t e^{t} - 3 e^{t} \\ - \frac{2}{t} + \frac{1}{t^{2}}\end{aligned}]$
- $[\begin{aligned}2 t \ln{\left(t \right)} + t - \ln{\left(t \right)} - 1 - \frac{2}{t} \\ 3 t^{2} e^{t} + 3 t e^{t} - 9 e^{t} \\ 1 + \frac{2}{t^{2}}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(\ln{\left(t \right)}) \\ \frac{\text{d}}{\text{d}t}(3 e^{t}) \\ \frac{\text{d}}{\text{d}t}(\frac{1}{t})\end{aligned}]=[\begin{aligned}\frac{1}{t} \\ 3 e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2} - t - 2)=2 t - 1\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t - 1)[\begin{aligned}\ln{\left(t \right)} \\ 3 e^{t} \\ \frac{1}{t}\end{aligned}]+(t^{2} - t - 2)[\begin{aligned}\frac{1}{t} \\ 3 e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\&=[\begin{aligned}\left(2 t - 1\right) \ln{\left(t \right)} \\ 3 \left(2 t - 1\right) e^{t} \\ \frac{2 t - 1}{t}\end{aligned}]+[\begin{aligned}\frac{t^{2} - t - 2}{t} \\ 3 \left(t^{2} - t - 2\right) e^{t} \\ - \frac{t^{2} - t - 2}{t^{2}}\end{aligned}]\\&=[\begin{aligned}2 t \ln{\left(t \right)} + t - \ln{\left(t \right)} - 1 - \frac{2}{t} \\ 3 \left(t^{2} + t - 3\right) e^{t} \\ 1 + \frac{2}{t^{2}}\end{aligned}]\end{aligned}
$$

## Generated authored_hard seed 8

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}\ln{\left(t \right)} \\ - 2 e^{t} \\ \frac{1}{t}\end{aligned}]$ and $u(t)=t^{2} - 2 t - 1.$

- $[\begin{aligned}2 - \frac{2}{t} \\ - 4 t e^{t} + 4 e^{t} \\ - \frac{2}{t} + \frac{2}{t^{2}}\end{aligned}]$
- $[\begin{aligned}2 t \ln{\left(t \right)} - 2 \ln{\left(t \right)} \\ - 4 t e^{t} + 4 e^{t} \\ 2 - \frac{2}{t}\end{aligned}]$
- $[\begin{aligned}2 t \ln{\left(t \right)} - t - 2 \ln{\left(t \right)} + 2 + \frac{1}{t} \\ 2 t^{2} e^{t} - 8 t e^{t} + 2 e^{t} \\ 3 - \frac{4}{t} - \frac{1}{t^{2}}\end{aligned}]$
- $[\begin{aligned}2 t \ln{\left(t \right)} + t - 2 \ln{\left(t \right)} - 2 - \frac{1}{t} \\ - 2 t^{2} e^{t} + 6 e^{t} \\ 1 + \frac{1}{t^{2}}\end{aligned}]$
- $[\begin{aligned}t - 2 - \frac{1}{t} \\ - 2 t^{2} e^{t} + 4 t e^{t} + 2 e^{t} \\ -1 + \frac{2}{t} + \frac{1}{t^{2}}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(\ln{\left(t \right)}) \\ \frac{\text{d}}{\text{d}t}(- 2 e^{t}) \\ \frac{\text{d}}{\text{d}t}(\frac{1}{t})\end{aligned}]=[\begin{aligned}\frac{1}{t} \\ - 2 e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2} - 2 t - 1)=2 t - 2\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t - 2)[\begin{aligned}\ln{\left(t \right)} \\ - 2 e^{t} \\ \frac{1}{t}\end{aligned}]+(t^{2} - 2 t - 1)[\begin{aligned}\frac{1}{t} \\ - 2 e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\&=[\begin{aligned}\left(2 t - 2\right) \ln{\left(t \right)} \\ - 2 \left(2 t - 2\right) e^{t} \\ \frac{2 t - 2}{t}\end{aligned}]+[\begin{aligned}\frac{t^{2} - 2 t - 1}{t} \\ - 2 \left(t^{2} - 2 t - 1\right) e^{t} \\ - \frac{t^{2} - 2 t - 1}{t^{2}}\end{aligned}]\\&=[\begin{aligned}2 t \ln{\left(t \right)} + t - 2 \ln{\left(t \right)} - 2 - \frac{1}{t} \\ 2 \left(3 - t^{2}\right) e^{t} \\ 1 + \frac{1}{t^{2}}\end{aligned}]\end{aligned}
$$

## Generated authored_hard seed 9

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}- \ln{\left(t \right)} \\ - e^{t} \\ \frac{1}{t}\end{aligned}]$ and $u(t)=t^{2} + t + 2.$

- $[\begin{aligned}- 2 t \ln{\left(t \right)} + t - \ln{\left(t \right)} + 1 + \frac{2}{t} \\ t^{2} e^{t} - t e^{t} + e^{t} \\ 3 + \frac{2}{t} + \frac{2}{t^{2}}\end{aligned}]$
- $[\begin{aligned}- 2 t \ln{\left(t \right)} - t - \ln{\left(t \right)} - 1 - \frac{2}{t} \\ - t^{2} e^{t} - 3 t e^{t} - 3 e^{t} \\ 1 - \frac{2}{t^{2}}\end{aligned}]$
- $[\begin{aligned}- 2 t \ln{\left(t \right)} - \ln{\left(t \right)} \\ - 2 t e^{t} - e^{t} \\ 2 + \frac{1}{t}\end{aligned}]$
- $[\begin{aligned}-2 - \frac{1}{t} \\ - 2 t e^{t} - e^{t} \\ - \frac{2}{t} - \frac{1}{t^{2}}\end{aligned}]$
- $[\begin{aligned}- t - 1 - \frac{2}{t} \\ - t^{2} e^{t} - t e^{t} - 2 e^{t} \\ -1 - \frac{1}{t} - \frac{2}{t^{2}}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(- \ln{\left(t \right)}) \\ \frac{\text{d}}{\text{d}t}(- e^{t}) \\ \frac{\text{d}}{\text{d}t}(\frac{1}{t})\end{aligned}]=[\begin{aligned}- \frac{1}{t} \\ - e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2} + t + 2)=2 t + 1\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t + 1)[\begin{aligned}- \ln{\left(t \right)} \\ - e^{t} \\ \frac{1}{t}\end{aligned}]+(t^{2} + t + 2)[\begin{aligned}- \frac{1}{t} \\ - e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\&=[\begin{aligned}- \left(2 t + 1\right) \ln{\left(t \right)} \\ - \left(2 t + 1\right) e^{t} \\ \frac{2 t + 1}{t}\end{aligned}]+[\begin{aligned}- \frac{t^{2} + t + 2}{t} \\ - \left(t^{2} + t + 2\right) e^{t} \\ - \frac{t^{2} + t + 2}{t^{2}}\end{aligned}]\\&=[\begin{aligned}- 2 t \ln{\left(t \right)} - t - \ln{\left(t \right)} - 1 - \frac{2}{t} \\ \left(- t^{2} - 3 t - 3\right) e^{t} \\ 1 - \frac{2}{t^{2}}\end{aligned}]\end{aligned}
$$

## Generated authored_hard seed 10

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}\ln{\left(t \right)} \\ e^{t} \\ \frac{1}{t}\end{aligned}]$ and $u(t)=t^{2} + 2 t - 3.$

- $[\begin{aligned}2 t \ln{\left(t \right)} + 2 \ln{\left(t \right)} \\ 2 t e^{t} + 2 e^{t} \\ 2 + \frac{2}{t}\end{aligned}]$
- $[\begin{aligned}t + 2 - \frac{3}{t} \\ t^{2} e^{t} + 2 t e^{t} - 3 e^{t} \\ -1 - \frac{2}{t} + \frac{3}{t^{2}}\end{aligned}]$
- $[\begin{aligned}2 t \ln{\left(t \right)} - t + 2 \ln{\left(t \right)} - 2 + \frac{3}{t} \\ - t^{2} e^{t} + 5 e^{t} \\ 3 + \frac{4}{t} - \frac{3}{t^{2}}\end{aligned}]$
- $[\begin{aligned}2 t \ln{\left(t \right)} + t + 2 \ln{\left(t \right)} + 2 - \frac{3}{t} \\ t^{2} e^{t} + 4 t e^{t} - e^{t} \\ 1 + \frac{3}{t^{2}}\end{aligned}]$
- $[\begin{aligned}2 + \frac{2}{t} \\ 2 t e^{t} + 2 e^{t} \\ - \frac{2}{t} - \frac{2}{t^{2}}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(\ln{\left(t \right)}) \\ \frac{\text{d}}{\text{d}t}(e^{t}) \\ \frac{\text{d}}{\text{d}t}(\frac{1}{t})\end{aligned}]=[\begin{aligned}\frac{1}{t} \\ e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2} + 2 t - 3)=2 t + 2\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t + 2)[\begin{aligned}\ln{\left(t \right)} \\ e^{t} \\ \frac{1}{t}\end{aligned}]+(t^{2} + 2 t - 3)[\begin{aligned}\frac{1}{t} \\ e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\&=[\begin{aligned}\left(2 t + 2\right) \ln{\left(t \right)} \\ \left(2 t + 2\right) e^{t} \\ \frac{2 t + 2}{t}\end{aligned}]+[\begin{aligned}\frac{t^{2} + 2 t - 3}{t} \\ \left(t^{2} + 2 t - 3\right) e^{t} \\ - \frac{t^{2} + 2 t - 3}{t^{2}}\end{aligned}]\\&=[\begin{aligned}2 t \ln{\left(t \right)} + t + 2 \ln{\left(t \right)} + 2 - \frac{3}{t} \\ \left(t^{2} + 4 t - 1\right) e^{t} \\ 1 + \frac{3}{t^{2}}\end{aligned}]\end{aligned}
$$

## Generated authored_hard seed 11

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}\ln{\left(t \right)} \\ e^{t} \\ \frac{1}{t}\end{aligned}]$ and $u(t)=t^{2} + t + 2.$

- $[\begin{aligned}2 t \ln{\left(t \right)} + \ln{\left(t \right)} \\ 2 t e^{t} + e^{t} \\ 2 + \frac{1}{t}\end{aligned}]$
- $[\begin{aligned}2 t \ln{\left(t \right)} - t + \ln{\left(t \right)} - 1 - \frac{2}{t} \\ - t^{2} e^{t} + t e^{t} - e^{t} \\ 3 + \frac{2}{t} + \frac{2}{t^{2}}\end{aligned}]$
- $[\begin{aligned}2 t \ln{\left(t \right)} + t + \ln{\left(t \right)} + 1 + \frac{2}{t} \\ t^{2} e^{t} + 3 t e^{t} + 3 e^{t} \\ 1 - \frac{2}{t^{2}}\end{aligned}]$
- $[\begin{aligned}t + 1 + \frac{2}{t} \\ t^{2} e^{t} + t e^{t} + 2 e^{t} \\ -1 - \frac{1}{t} - \frac{2}{t^{2}}\end{aligned}]$
- $[\begin{aligned}2 + \frac{1}{t} \\ 2 t e^{t} + e^{t} \\ - \frac{2}{t} - \frac{1}{t^{2}}\end{aligned}]$

Using the scalar function multiple rule, we can write

$$
(u(t)f(t))^{′}=u^{′}(t)f(t)+u(t)f^{′}(t).
$$

Let's find $u^{′}(t)$ and $f^{′}(t).$

$$
\begin{aligned}f^{′}(t)&=[\begin{aligned}\frac{\text{d}}{\text{d}t}(\ln{\left(t \right)}) \\ \frac{\text{d}}{\text{d}t}(e^{t}) \\ \frac{\text{d}}{\text{d}t}(\frac{1}{t})\end{aligned}]=[\begin{aligned}\frac{1}{t} \\ e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\u^{′}(t)&=\frac{\text{d}}{\text{d}t}(t^{2} + t + 2)=2 t + 1\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(u(t)f(t))^{′}&=u^{′}(t)f(t)+u(t)f^{′}(t)\\&=(2 t + 1)[\begin{aligned}\ln{\left(t \right)} \\ e^{t} \\ \frac{1}{t}\end{aligned}]+(t^{2} + t + 2)[\begin{aligned}\frac{1}{t} \\ e^{t} \\ - \frac{1}{t^{2}}\end{aligned}]\\&=[\begin{aligned}\left(2 t + 1\right) \ln{\left(t \right)} \\ \left(2 t + 1\right) e^{t} \\ \frac{2 t + 1}{t}\end{aligned}]+[\begin{aligned}\frac{t^{2} + t + 2}{t} \\ \left(t^{2} + t + 2\right) e^{t} \\ - \frac{t^{2} + t + 2}{t^{2}}\end{aligned}]\\&=[\begin{aligned}2 t \ln{\left(t \right)} + t + \ln{\left(t \right)} + 1 + \frac{2}{t} \\ \left(t^{2} + 3 t + 3\right) e^{t} \\ 1 - \frac{2}{t^{2}}\end{aligned}]\end{aligned}
$$
