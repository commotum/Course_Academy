# Vector chain-rule review

Sources are preserved below in original notation; replays and variants are labeled. Normal mathematics uses normalized TeX; four teaching typos are repaired.

---

## Original q-32498

If $f(u)=[\begin{aligned}2u \\ {u}^{2} \\ 3\end{aligned}]$ and $u(t)=2t+2$, then $(f∘u)^{′}(t)=$

- $[\begin{aligned}4 \\ 8t+8 \\ 0\end{aligned}]$ **correct**
- $[\begin{aligned}2 \\ 4t+4 \\ 0\end{aligned}]$
- $[\begin{aligned}4 \\ 8t \\ 0\end{aligned}]$
- $[\begin{aligned}2 \\ 2t \\ 0\end{aligned}]$
- $[\begin{aligned}4 \\ 4t+4 \\ 0\end{aligned}]$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)={f}^{′}(u(t)){u}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}(2u) \\ \frac{\text{d}}{\text{d}u}\,({u}^{2}) \\ \frac{\text{d}}{\text{d}u}(3)\end{aligned}]=[\begin{aligned}2 \\ 2u \\ 0\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2t+2)=2\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}2 \\ 2u(t) \\ 0\end{aligned}]\cdot {u}^{′}(t) \\  & =[\begin{aligned}2 \\ 2(2t+2) \\ 0\end{aligned}]\cdot 2 \\  & =[\begin{aligned}4 \\ 8t+8 \\ 0\end{aligned}]\end{aligned}
$$

---

**Source replay — notation normalized, repairs listed in metadata**

## linear_quadratic_affine — easy (observed)

If $f(u)=[\begin{aligned}2 u \\ u^{2} \\ 3\end{aligned}]$ and $u(t)=2 t + 2$, then $(f∘u)^{′}(t)=$

- $[\begin{aligned}2 \\ 2 t \\ 0\end{aligned}]$
- $[\begin{aligned}4 \\ 8 t \\ 0\end{aligned}]$
- $[\begin{aligned}2 \\ 4 t + 4 \\ 0\end{aligned}]$
- $[\begin{aligned}4 \\ 8 t + 8 \\ 0\end{aligned}]$ **correct**
- $[\begin{aligned}4 \\ 4 t + 4 \\ 0\end{aligned}]$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(2 u\right) \\ \frac{\text{d}}{\text{d}u}\left(u^{2}\right) \\ \frac{\text{d}}{\text{d}u}\left(3\right)\end{aligned}]=[\begin{aligned}2 \\ 2 u \\ 0\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(2 t + 2\right)=2\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}2 \\ 2 u(t) \\ 0\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}2 \\ 4 t + 4 \\ 0\end{aligned}]\cdot \left(2\right) \\  & =[\begin{aligned}4 \\ 8 t + 8 \\ 0\end{aligned}]\end{aligned}
$$

---

## Original q-32866

If $f(t)=\operatorname{cos}⁡u\,i+(1-{u}^{2})\,j+12\,k$ and $u(t)={t}^{3}$ then $(f∘u)^{′}(t)=$

- $-\operatorname{sin}⁡3{t}^{2}\,i-6{t}^{2}\,j$
- $-3{t}^{2}\operatorname{sin}⁡{t}^{3}\,i-6{t}^{5}\,j$ **correct**
- $-2{t}^{2}\operatorname{sin}⁡{t}^{3}\,i-2{t}^{5}\,j$
- $-\operatorname{sin}⁡u\,i-2u\,j$
- $-\operatorname{sin}⁡{t}^{3}\,i-6{t}^{3}\,j$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)={f}^{′}(u(t)){u}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(u) & =\frac{\text{d}}{\text{d}u}(\operatorname{cos}⁡u)\,i+\frac{\text{d}}{\text{d}u}(1-{u}^{2})\,j+\frac{\text{d}}{\text{d}u}(12)\,k \\  & =-\operatorname{sin}⁡u\,i-2u\,j+0\,k \\  & =-\operatorname{sin}⁡u\,i-2u\,j \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{3})=3{t}^{2}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & ={f}^{′}(u(t))\cdot {u}^{′}(t) \\  & =(-\operatorname{sin}⁡(u(t))\,i-2(u(t))\,j)\cdot {u}^{′}(t) \\  & =(-\operatorname{sin}⁡({t}^{3})\,i-2({t}^{3})\,j)\cdot 3{t}^{2} \\  & =-3{t}^{2}\operatorname{sin}⁡{t}^{3}\,i-6{t}^{5}\,j\end{aligned}
$$

---

**Source replay — notation normalized, repairs listed in metadata**

## cos_quadratic_power — easy (observed)

If $f(u)=\cos{\left(u \right)}\,i+\left(1 - u^{2}\right)\,j+12\,k$ and $u(t)=t^{3}$ then $(f∘u)^{′}(t)=$

- $-\sin{\left(u \right)}\,i-2 u\,j$
- $-2 t^{2} \sin{\left(t^{3} \right)}\,i-2 t^{5}\,j$
- $-3 t^{2} \sin{\left(t^{3} \right)}\,i-6 t^{5}\,j$ **correct**
- $-\sin{\left(3 t^{2} \right)}\,i-6 t^{2}\,j$
- $-\sin{\left(t^{3} \right)}\,i-6 t^{3}\,j$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\frac{\text{d}}{\text{d}u}\left(\cos{\left(u \right)}\right)\,i+\frac{\text{d}}{\text{d}u}\left(1 - u^{2}\right)\,j+\frac{\text{d}}{\text{d}u}\left(12\right)\,k \\  & =-\sin{\left(u \right)}\,i-2 u\,j+0\,k \\  & =-\sin{\left(u \right)}\,i-2 u\,j \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(t^{3}\right)=3 t^{2}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\left(-\sin{\left(u(t) \right)}\,i-2 u(t)\,j\right)\cdot \left(u^{′}(t)\right) \\  & =\left(-\sin{\left(t^{3} \right)}\,i-2 t^{3}\,j\right)\cdot \left(3 t^{2}\right) \\  & =-3 t^{2} \sin{\left(t^{3} \right)}\,i-6 t^{5}\,j\end{aligned}
$$

---

## Original q-128563

If $g(u)=⟨\operatorname{sin}⁡u,\,\operatorname{ln}⁡2u,\,\operatorname{tan}⁡u⟩$ and $u(t)={t}^{2},$ then $(g∘u)^{′}(t)=$

- $⟨\operatorname{cos}⁡({t}^{2}),\,\frac{1}{{t}^{2}},\,t{sec}^{2}⁡({t}^{2})⟩$
- $⟨\operatorname{cos}⁡({t}^{2}),\,\frac{1}{t},\,2t⟩$
- $⟨2t\operatorname{sin}⁡({t}^{2}),\,\frac{1}{t},\,2t{cos}^{2}⁡({t}^{2})⟩$
- $⟨2t\operatorname{sec}⁡({t}^{2}),\,\frac{1}{t},\,2t\operatorname{sin}⁡({t}^{2})⟩$
- $⟨2t\operatorname{cos}⁡({t}^{2}),\,\frac{2}{t},\,2t{sec}^{2}⁡({t}^{2})⟩$ **correct**

By the chain rule, we have 

$$
(g∘u)^{′}(t)=g′(u(t))u′(t).
$$

Now, let's find the derivatives of each function:

$$
\begin{aligned}{g}^{′}(u) & =⟨\frac{\text{d}}{\text{d}u}(\operatorname{sin}⁡u),\,\frac{\text{d}}{\text{d}u}(\operatorname{ln}⁡2u),\,\frac{\text{d}}{\text{d}u}(\operatorname{tan}⁡u)⟩ \\  & =⟨\operatorname{cos}⁡u,\,\frac{1}{u},\,{sec}^{2}⁡u⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{2})=2t\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(g∘u)^{′}(t) & =g′(u(t))u′(t) \\  & =⟨\operatorname{cos}⁡(u(t)),\,\frac{1}{u(t)},\,{sec}^{2}⁡(u(t))⟩\cdot {u}^{′}(t) \\  & =⟨\operatorname{cos}⁡({t}^{2}),\,\frac{1}{{t}^{2}},\,{sec}^{2}⁡({t}^{2})⟩\cdot 2t \\  & =⟨2t\operatorname{cos}⁡({t}^{2}),\,\frac{2}{t},\,2t{sec}^{2}⁡({t}^{2})⟩.\end{aligned}
$$

---

**Source replay — notation normalized, repairs listed in metadata**

## sin_log_tan_power — easy (observed)

If $g(u)=⟨\sin{\left(u \right)},\,\log{\left(2 u \right)},\,\tan{\left(u \right)}⟩$ and $u(t)=t^{2}$ then $(g∘u)^{′}(t)=$

- $⟨2 t \sec{\left(t^{2} \right)},\,\frac{1}{t},\,2 t \sin{\left(t^{2} \right)}⟩$
- $⟨2 t \sin{\left(t^{2} \right)},\,\frac{1}{t},\,2 t \cos^{2}{\left(t^{2} \right)}⟩$
- $⟨\cos{\left(t^{2} \right)},\,\frac{1}{t},\,2 t⟩$
- $⟨\cos{\left(t^{2} \right)},\,\frac{1}{t^{2}},\,t \sec^{2}{\left(t^{2} \right)}⟩$
- $⟨2 t \cos{\left(t^{2} \right)},\,\frac{2}{t},\,\frac{2 t}{\cos^{2}{\left(t^{2} \right)}}⟩$ **correct**

By the chain rule, we have 

$$
(g∘u)^{′}(t)=g′(u(t))u′(t)
$$

Now, let's find the derivatives of each function:

$$
\begin{aligned}g^{′}(u) & =⟨\frac{\text{d}}{\text{d}u}\left(\sin{\left(u \right)}\right),\,\frac{\text{d}}{\text{d}u}\left(\log{\left(2 u \right)}\right),\,\frac{\text{d}}{\text{d}u}\left(\tan{\left(u \right)}\right)⟩ \\  & =⟨\cos{\left(u \right)},\,\frac{1}{u},\,\tan^{2}{\left(u \right)} + 1⟩ \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(t^{2}\right)=2 t\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(g∘u)^{′}(t) & =g′(u(t))u′(t) \\  & =⟨\cos{\left(u(t) \right)},\,\frac{1}{u(t)},\,\tan^{2}{\left(u(t) \right)} + 1⟩\cdot \left(u^{′}(t)\right) \\  & =⟨\cos{\left(t^{2} \right)},\,\frac{1}{t^{2}},\,\tan^{2}{\left(t^{2} \right)} + 1⟩\cdot \left(2 t\right) \\  & =⟨2 t \cos{\left(t^{2} \right)},\,\frac{2}{t},\,\frac{2 t}{\cos^{2}{\left(t^{2} \right)}}⟩\end{aligned}
$$

---

## Original q-128572

If $f(u)=[\begin{aligned}u \\ {u}^{2} \\ 6\end{aligned}]$ and $u(t)={e}^{t}$, then $(f∘u)^{′}(t)=$

- $[\begin{aligned}1 \\ 2{e}^{t} \\ 0\end{aligned}]$
- $[\begin{aligned}{e}^{t} \\ 2{e}^{2t} \\ 0\end{aligned}]$ **correct**
- $[\begin{aligned}{e}^{t} \\ 2{e}^{t} \\ 0\end{aligned}]$
- $[\begin{aligned}t \\ 2{e}^{t} \\ 0\end{aligned}]$
- $[\begin{aligned}1 \\ 3{e}^{t} \\ 0\end{aligned}]$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)={f}^{′}(u(t)){u}^{′}(t).
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}(u) \\ \frac{\text{d}}{\text{d}u}\,({u}^{2}) \\ \frac{\text{d}}{\text{d}u}(6)\end{aligned}]=[\begin{aligned}1 \\ 2u \\ 0\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{t})={e}^{t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}1 \\ 2u(t) \\ 0\end{aligned}]\cdot {u}^{′}(t) \\  & =[\begin{aligned}1 \\ 2({e}^{t}) \\ 0\end{aligned}]\cdot {e}^{t} \\  & =[\begin{aligned}{e}^{t} \\ 2{e}^{2t} \\ 0\end{aligned}].\end{aligned}
$$

---

**Source replay — notation normalized, repairs listed in metadata**

## linear_quadratic_exp — easy (observed)

If $f(u)=[\begin{aligned}u \\ u^{2} \\ 6\end{aligned}]$ and $u(t)=e^{t}$, then $(f∘u)^{′}(t)=$

- $[\begin{aligned}t \\ 2 e^{t} \\ 0\end{aligned}]$
- $[\begin{aligned}e^{t} \\ 2 e^{t} \\ 0\end{aligned}]$
- $[\begin{aligned}e^{t} \\ 2 e^{2 t} \\ 0\end{aligned}]$ **correct**
- $[\begin{aligned}1 \\ 2 e^{t} \\ 0\end{aligned}]$
- $[\begin{aligned}1 \\ 3 e^{t} \\ 0\end{aligned}]$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(u\right) \\ \frac{\text{d}}{\text{d}u}\left(u^{2}\right) \\ \frac{\text{d}}{\text{d}u}\left(6\right)\end{aligned}]=[\begin{aligned}1 \\ 2 u \\ 0\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(e^{t}\right)=e^{t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}1 \\ 2 u(t) \\ 0\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}1 \\ 2 e^{t} \\ 0\end{aligned}]\cdot \left(e^{t}\right) \\  & =[\begin{aligned}e^{t} \\ 2 e^{2 t} \\ 0\end{aligned}]\end{aligned}
$$

---

## Original q-32502

If  $f(u)=u\,i+2u\,j+3u\,k$ and $u(t)={t}^{2}$, then $(f∘u)^{′}(t)=$

- $2t\,i+4t\,j+6t\,k$ **correct**
- $4t\,i+4t\,j+4t\,k$
- $4t\,i+8t\,j+12t\,k$
- ${t}^{2}i+2{t}^{2}\,j+3{t}^{2}\,k$
- $i+2\,j+3\,k$

Using the chain rule, we can write 

$$
(f∘u)^{′}(t)={f}^{′}(u(t)){u}^{′}(t)
$$

Now, let's find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(u) & =\frac{\text{d}}{\text{d}u}u\,i+\frac{\text{d}}{\text{d}u}2u\,j+\frac{\text{d}}{\text{d}t}3u\,k \\  & =i+2\,j+3\,k \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{2}) \\  & =2t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =(i+2\,j+3\,k)2t \\  & =2t\,i+4t\,j+6t\,k\end{aligned}
$$

---

**Source replay — notation normalized, repairs listed in metadata**

## linear_vector_power — easy (observed)

If  $f(u)=u\,i+2 u\,j+3 u\,k$ and $u(t)=t^{2}$, then $(f∘u)^{′}(t)=$

- $t^{2}\,i+2 t^{2}\,j+3 t^{2}\,k$
- $4 t\,i+8 t\,j+12 t\,k$
- $4 t\,i+4 t\,j+4 t\,k$
- $2 t\,i+4 t\,j+6 t\,k$ **correct**
- $\,i+2\,j+3\,k$

Using the chain rule, we can write 

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Now, let's find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\frac{\text{d}}{\text{d}u}\left(u\right)\,i+\frac{\text{d}}{\text{d}u}\left(2 u\right)\,j+\frac{\text{d}}{\text{d}u}\left(3 u\right)\,k \\  & =\,i+2\,j+3\,k \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(t^{2}\right) \\  & =2 t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\left(\,i+2\,j+3\,k\right)\cdot \left(2 t\right) \\  & =2 t\,i+4 t\,j+6 t\,k\end{aligned}
$$

---

## Original q-32860

If $g(u)=[\begin{aligned}\operatorname{ln}⁡u \\ 5 \\ {u}^{2}\end{aligned}]$ and $u(t)=\operatorname{ln}⁡t$, then  $(g∘u)^{′}(t)=$

- $[\begin{aligned}\frac{1}{\operatorname{ln}⁡t} \\ 0 \\ 2\operatorname{ln}⁡t\end{aligned}]$
- $[\begin{aligned}\frac{1}{u} \\ 0 \\ 2u\end{aligned}]$
- $[\begin{aligned}\frac{1}{\operatorname{ln}⁡t} \\ 0 \\ \frac{2\operatorname{ln}⁡t}{t}\end{aligned}]$
- $[\begin{aligned}\frac{1}{t\operatorname{ln}⁡t} \\ 0 \\ \frac{2\operatorname{ln}⁡t}{t}\end{aligned}]$ **correct**
- $[\begin{aligned}u \\ 5 \\ 2u\end{aligned}]$

By the chain rule, we have 

$$
(f∘u)^{′}(t)={f}^{′}(u(t)){u}^{′}(t).
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{g}^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\operatorname{ln}⁡u \\ \frac{\text{d}}{\text{d}u}\,\,5\,\, \\ \frac{\text{d}}{\text{d}u}\,\,{u}^{2}\,\,\end{aligned}]=[\begin{aligned}\frac{1}{u} \\ 0 \\ 2u\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡t)=\frac{1}{t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(g∘u)^{′}(t) & =g′(u(t))u′(t) \\  & =[\begin{aligned}\frac{1}{u(t)} \\ 0 \\ 2u(t)\end{aligned}]{u}^{′}(t) \\  & =\frac{1}{t}[\begin{aligned}\frac{1}{\operatorname{ln}⁡t} \\ 0 \\ 2\operatorname{ln}⁡t\end{aligned}] \\  & =[\begin{aligned}\frac{1}{t\operatorname{ln}⁡t} \\ 0 \\ \frac{2\operatorname{ln}⁡t}{t}\end{aligned}]\end{aligned}
$$

---

**Source replay — notation normalized, repairs listed in metadata**

## log_quadratic_log — easy (observed)

If $g(u)=[\begin{aligned}\log{\left(u \right)} \\ 5 \\ u^{2}\end{aligned}]$ and $u(t)=\log{\left(t \right)}$, then  $(g∘u)^{′}(t)=$

- $[\begin{aligned}\frac{1}{t \log{\left(t \right)}} \\ 0 \\ \frac{2 \log{\left(t \right)}}{t}\end{aligned}]$ **correct**
- $[\begin{aligned}\frac{1}{\log{\left(t \right)}} \\ 0 \\ \frac{2 \log{\left(t \right)}}{t}\end{aligned}]$
- $[\begin{aligned}\frac{1}{u} \\ 0 \\ 2 u\end{aligned}]$
- $[\begin{aligned}\frac{1}{\log{\left(t \right)}} \\ 0 \\ 2 \log{\left(t \right)}\end{aligned}]$
- $[\begin{aligned}u \\ 5 \\ 2 u\end{aligned}]$

By the chain rule, we have 

$$
(g∘u)^{′}(t)=g′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}g^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(\log{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(5\right) \\ \frac{\text{d}}{\text{d}u}\left(u^{2}\right)\end{aligned}]=[\begin{aligned}\frac{1}{u} \\ 0 \\ 2 u\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(\log{\left(t \right)}\right)=\frac{1}{t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(g∘u)^{′}(t) & =g′(u(t))u′(t) \\  & =[\begin{aligned}\frac{1}{u(t)} \\ 0 \\ 2 u(t)\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}\frac{1}{\log{\left(t \right)}} \\ 0 \\ 2 \log{\left(t \right)}\end{aligned}]\cdot \left(\frac{1}{t}\right) \\  & =[\begin{aligned}\frac{1}{t \log{\left(t \right)}} \\ 0 \\ \frac{2 \log{\left(t \right)}}{t}\end{aligned}]\end{aligned}
$$

---

## Original q-32869

If $g(u)=⟨\operatorname{ln}⁡u,\,0,\,\frac{1}{u}⟩$ and $u(t)={e}^{2t}$, then $(g∘u)^{′}(t)=$

- $⟨2,\,0,\,-2{e}^{2t}⟩$
- $⟨{e}^{-2t},\,0,\,-{e}^{-4t}⟩$
- $⟨2,\,0,\,-2{e}^{-2t}⟩$ **correct**
- $⟨2,\,0,\,2{e}^{2t}⟩$
- $⟨{e}^{-2t},\,0,\,{e}^{-4t}⟩$

By the chain rule, we have 

$$
(g∘u)^{′}(t)=g′(u(t))u′(t)
$$

Now, let's find the derivatives of each function:

$$
\begin{aligned}{g}^{′}(u) & =⟨\frac{\text{d}}{\text{d}u}\operatorname{ln}⁡u,\,\frac{\text{d}}{\text{d}u}0,\,\frac{\text{d}}{\text{d}u}(\frac{1}{u})⟩ \\  & =⟨\frac{1}{u},\,0,\,-\frac{1}{{u}^{2}}⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{2t})=2{e}^{2t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(g∘u)^{′}(t) & =g′(u(t))u′(t) \\  & =⟨\frac{1}{u(t)},\,0,\,-\frac{1}{{u}^{2}(t)}⟩{u}^{′}(t) \\  & =2{e}^{2t}⟨\frac{1}{{e}^{2t}},\,0,\,-\frac{1}{({e}^{2t})^{2}}⟩ \\  & =⟨\frac{2{e}^{2t}}{{e}^{2t}},\,0,\,-\frac{2{e}^{2t}}{{e}^{4t}}⟩ \\  & =⟨2,\,0,\,-2{e}^{-2t}⟩\end{aligned}
$$

---

**Source replay — notation normalized, repairs listed in metadata**

## log_reciprocal_exp — easy (observed)

If $g(u)=⟨\log{\left(u \right)},\,0,\,\frac{1}{u}⟩$ and $u(t)=e^{2 t}$, then $(g∘u)^{′}(t)=$

- $⟨2,\,0,\,2 e^{2 t}⟩$
- $⟨2,\,0,\,- 2 e^{- 2 t}⟩$ **correct**
- $⟨e^{- 2 t},\,0,\,- e^{- 4 t}⟩$
- $⟨2,\,0,\,- 2 e^{2 t}⟩$
- $⟨e^{- 2 t},\,0,\,e^{- 4 t}⟩$

By the chain rule, we have 

$$
(g∘u)^{′}(t)=g′(u(t))u′(t)
$$

Now, let's find the derivatives of each function:

$$
\begin{aligned}g^{′}(u) & =⟨\frac{\text{d}}{\text{d}u}\left(\log{\left(u \right)}\right),\,\frac{\text{d}}{\text{d}u}\left(0\right),\,\frac{\text{d}}{\text{d}u}\left(\frac{1}{u}\right)⟩ \\  & =⟨\frac{1}{u},\,0,\,- \frac{1}{u^{2}}⟩ \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(e^{2 t}\right)=2 e^{2 t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(g∘u)^{′}(t) & =g′(u(t))u′(t) \\  & =⟨\frac{1}{u(t)},\,0,\,- \frac{1}{u(t)^{2}}⟩\cdot \left(u^{′}(t)\right) \\  & =⟨e^{- 2 t},\,0,\,- e^{- 4 t}⟩\cdot \left(2 e^{2 t}\right) \\  & =⟨e^{- 2 t} 2 e^{2 t},\,0 \cdot 2 e^{2 t},\,- e^{- 4 t} 2 e^{2 t}⟩ \\  & =⟨2,\,0,\,- 2 e^{- 2 t}⟩\end{aligned}
$$

---

## Original q-33260

If $f(u)={e}^{u+1}\,i+{e}^{2u}\,j+\frac{1}{e}\,k$ and $u(t)=2{t}^{2}$ then $(f∘u)^{′}(t)=$

- $t{e}^{2t+1}\,i+2t{e}^{4t}\,j$
- $t{e}^{t+1}\,i+2t{e}^{2t}\,j$
- $4t{e}^{2{t}^{2}+1}\,i+8t{e}^{4{t}^{2}}\,j$ **correct**
- $4t{e}^{t+1}\,i+6t{e}^{2t}\,j$
- $4{e}^{2{t}^{2}+1}\,i-8{e}^{4{t}^{2}}\,j$

By the chain rule, we have

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function:

$$
\begin{aligned}{f}^{′}(u) & =\frac{\text{d}}{\text{d}u}({e}^{u+1})\,i+\frac{\text{d}}{\text{d}u}({e}^{2u})\,j+\frac{\text{d}}{\text{d}u}\frac{1}{e}\,k \\  & ={e}^{u+1}\,i+2{e}^{2u}\,j+0\,k \\  & ={e}^{u+1}\,i+2{e}^{2t}\,j \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2{t}^{2})=4t\end{aligned}
$$

 
Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\ (f∘u)^{′}(t) & =({e}^{2{t}^{2}+1}\,i+2{e}^{4{t}^{2}}\,j)4t \\  & =4t{e}^{2{t}^{2}+1}\,i+8t{e}^{4{t}^{2}}\,j\end{aligned}
$$

---

**Source replay — notation normalized, repairs listed in metadata**

## two_exp_power — easy (observed)

If $f(u)=e^{u + 1}\,i+e^{2 u}\,j+e^{-1}\,k$ and $u(t)=2 t^{2}$ then $(f∘u)^{′}(t)=$

- $4 t e^{t + 1}\,i+6 t e^{2 t}\,j$
- $4 t e^{2 t^{2} + 1}\,i+8 t e^{4 t^{2}}\,j$ **correct**
- $t e^{t + 1}\,i+2 t e^{2 t}\,j$
- $t e^{2 t + 1}\,i+2 t e^{4 t}\,j$
- $4 e^{2 t^{2} + 1}\,i-8 e^{4 t^{2}}\,j$

By the chain rule, we have

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function:

$$
\begin{aligned}f^{′}(u) & =\frac{\text{d}}{\text{d}u}\left(e^{u + 1}\right)\,i+\frac{\text{d}}{\text{d}u}\left(e^{2 u}\right)\,j+\frac{\text{d}}{\text{d}u}\left(e^{-1}\right)\,k \\  & =e^{u + 1}\,i+2 e^{2 u}\,j+0\,k \\  & =e^{u + 1}\,i+2 e^{2 u}\,j \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(2 t^{2}\right)=4 t\end{aligned}
$$

 
Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\ (f∘u)^{′}(t) & =\left(e^{2 t^{2} + 1}\,i+2 e^{4 t^{2}}\,j\right)\cdot \left(4 t\right) \\  & =4 t e^{2 t^{2} + 1}\,i+8 t e^{4 t^{2}}\,j\end{aligned}
$$

---

## Original q-71222

If $f(u)=[\begin{aligned}\operatorname{sin}⁡u \\ \operatorname{cos}⁡u \\ {e}^{u}\end{aligned}]$ and $u(t)=4t-3,$ then $(f∘u)^{′}(t)=$

- $[\begin{aligned}4\operatorname{sin}⁡(4t-3) \\ -4\operatorname{cos}⁡(4t-3) \\ 4{e}^{4t-3}\end{aligned}]$
- $[\begin{aligned}-\operatorname{sin}⁡(4t-3) \\ \operatorname{cos}⁡(4t-3) \\ (4t-3){e}^{t}\end{aligned}]$
- $[\begin{aligned}4\operatorname{cos}⁡(4t-3) \\ -4\operatorname{sin}⁡(4t-3) \\ 4{e}^{4t-3}\end{aligned}]$ **correct**
- $[\begin{aligned}-8\operatorname{sin}⁡(4t-3) \\ 8\operatorname{cos}⁡(4t-3) \\ (4t-3){e}^{t}\end{aligned}]$
- $[\begin{aligned}\operatorname{cos}⁡(4t-3) \\ -\operatorname{sin}⁡(4t-3) \\ {e}^{4t-3}\end{aligned}]$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)={f}^{′}(u(t)){u}^{′}(t).
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}(\operatorname{sin}⁡u) \\ \frac{\text{d}}{\text{d}u}\,(\operatorname{cos}⁡u) \\ \frac{\text{d}}{\text{d}u}({e}^{u})\end{aligned}]=[\begin{aligned}\operatorname{cos}⁡u \\ -\operatorname{sin}⁡u \\ {e}^{u}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(4t-3)=4\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & ={f}^{′}(u(t)){u}^{′}(t) \\  & =[\begin{aligned}\operatorname{cos}⁡(u(t)) \\ -\operatorname{sin}⁡(u(t)) \\ {e}^{u(t)}\end{aligned}]\cdot {u}^{′}(t) \\  & =[\begin{aligned}\operatorname{cos}⁡(4t-3) \\ -\operatorname{sin}⁡(4t-3) \\ {e}^{4t-3}\end{aligned}]\cdot 4 \\  & =[\begin{aligned}4\operatorname{cos}⁡(4t-3) \\ -4\operatorname{sin}⁡(4t-3) \\ 4{e}^{4t-3}\end{aligned}]\end{aligned}
$$

---

**Source replay — notation normalized, repairs listed in metadata**

## sin_cos_exp_affine — easy (observed)

If $f(u)=[\begin{aligned}\sin{\left(u \right)} \\ \cos{\left(u \right)} \\ e^{u}\end{aligned}]$ and $u(t)=4 t - 3$ then $(f∘u)^{′}(t)=$

- $[\begin{aligned}- 8 \sin{\left(4 t - 3 \right)} \\ 8 \cos{\left(4 t - 3 \right)} \\ \left(4 t - 3\right) e^{t}\end{aligned}]$
- $[\begin{aligned}4 \cos{\left(4 t - 3 \right)} \\ - 4 \sin{\left(4 t - 3 \right)} \\ 4 e^{4 t - 3}\end{aligned}]$ **correct**
- $[\begin{aligned}- \sin{\left(4 t - 3 \right)} \\ \cos{\left(4 t - 3 \right)} \\ \left(4 t - 3\right) e^{t}\end{aligned}]$
- $[\begin{aligned}4 \sin{\left(4 t - 3 \right)} \\ - 4 \cos{\left(4 t - 3 \right)} \\ 4 e^{4 t - 3}\end{aligned}]$
- $[\begin{aligned}\cos{\left(4 t - 3 \right)} \\ - \sin{\left(4 t - 3 \right)} \\ e^{4 t - 3}\end{aligned}]$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(\sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(\cos{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(e^{u}\right)\end{aligned}]=[\begin{aligned}\cos{\left(u \right)} \\ - \sin{\left(u \right)} \\ e^{u}\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(4 t - 3\right)=4\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}\cos{\left(u(t) \right)} \\ - \sin{\left(u(t) \right)} \\ e^{u(t)}\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}\cos{\left(4 t - 3 \right)} \\ - \sin{\left(4 t - 3 \right)} \\ e^{4 t - 3}\end{aligned}]\cdot \left(4\right) \\  & =[\begin{aligned}4 \cos{\left(4 t - 3 \right)} \\ - 4 \sin{\left(4 t - 3 \right)} \\ 4 e^{4 t - 3}\end{aligned}]\end{aligned}
$$

---

## Original q-128561

If $f(u)=\operatorname{ln}⁡u\,i+{u}^{2}\,j+\sqrt{u}\,k$ and $u(t)={e}^{-t},$ then $(f∘u)^{′}(t)=$

- $\,i-4{e}^{-2t}\,j-2{e}^{-3t/2}\,k$
- $-\,i-{e}^{-2t}\,j-2{e}^{-t/2}\,k$
- $\,i-2{e}^{-t}\,j-\frac{1}{4}{e}^{-t/2}\,k$
- $-\,i-2{e}^{-2t}\,j-\frac{1}{2}{e}^{-t/2}\,k$ **correct**
- $-\,i-2{e}^{2t}\,j-\frac{1}{2}{e}^{t}\,k$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)={f}^{′}(u(t)){u}^{′}(t).
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(u) & =\frac{\text{d}}{\text{d}u}(\operatorname{ln}⁡u)i+\frac{\text{d}}{\text{d}u}({u}^{2})j+\frac{\text{d}}{\text{d}u}(\sqrt{u})k \\  & =\frac{1}{u}\,i+2u\,j+\frac{1}{2\sqrt{u}}\,k \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{-t})=-{e}^{-t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(f∘u)^{′}(t) & ={f}^{′}(u(t))\cdot {u}^{′}(t) \\  & =(\frac{1}{u(t)}\,i+2u(t)\,j+\frac{1}{2\sqrt{u(t)}}\,k)\cdot {u}^{′}(t) \\  & =(\frac{1}{{e}^{-t}}\,i+2{e}^{-t}\,j+\frac{1}{2\sqrt{{e}^{-t}}}\,k)\cdot (-{e}^{-t}) \\  & =({e}^{t}\,i+2{e}^{-t}\,j+\frac{1}{2}{e}^{t/2}\,k)\cdot (-{e}^{-t}) \\  & =-\,i-2{e}^{-2t}\,j-\frac{1}{2}{e}^{-t/2}\,k.\end{aligned}
$$

---

**Source replay — notation normalized, repairs listed in metadata**

## log_power_root_exp — easy (observed)

If $f(u)=\log{\left(u \right)}\,i+u^{2}\,j+\sqrt{u}\,k$ and $u(t)=e^{- t}$ then $(f∘u)^{′}(t)=$

- $-\,i-2 e^{- 2 t}\,j-\frac{e^{- \frac{t}{2}}}{2}\,k$ **correct**
- $\,i-2 e^{- t}\,j-\frac{e^{- \frac{t}{2}}}{4}\,k$
- $-\,i-e^{- 2 t}\,j-2 e^{- \frac{t}{2}}\,k$
- $\,i-4 e^{- 2 t}\,j-2 e^{- \frac{3 t}{2}}\,k$
- $-\,i-2 e^{2 t}\,j-\frac{e^{t}}{2}\,k$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\frac{\text{d}}{\text{d}u}\left(\log{\left(u \right)}\right)\,i+\frac{\text{d}}{\text{d}u}\left(u^{2}\right)\,j+\frac{\text{d}}{\text{d}u}\left(\sqrt{u}\right)\,k \\  & =\frac{1}{u}\,i+2 u\,j+\frac{1}{2 \sqrt{u}}\,k \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(e^{- t}\right)=- e^{- t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\left(\frac{1}{u(t)}\,i+2 u(t)\,j+\frac{1}{2 \sqrt{u(t)}}\,k\right)\cdot \left(u^{′}(t)\right) \\  & =\left(e^{t}\,i+2 e^{- t}\,j+\frac{e^{\frac{t}{2}}}{2}\,k\right)\cdot \left(- e^{- t}\right) \\  & =\left(e^{t}\,i+2 e^{- t}\,j+\frac{e^{\frac{t}{2}}}{2}\,k\right)\cdot \left(- e^{- t}\right) \\  & =-\,i-2 e^{- 2 t}\,j-\frac{e^{- \frac{t}{2}}}{2}\,k\end{aligned}
$$

---

## Original q-128570

If $g(u)=⟨\frac{1}{u},\,\operatorname{ln}⁡(u+1),\,1⟩$ and $u(t)=\frac{1}{t}$, then $(g∘u)^{′}(t)=$

- $⟨-1,-\frac{t}{2+{t}^{2}},0⟩$
- $⟨-\frac{1}{{t}^{2}},-\frac{{t}^{2}}{1+{t}^{2}},0⟩$
- $⟨1,-\frac{1}{t+{t}^{2}},0⟩$ **correct**
- $⟨\frac{1}{t},-\frac{1}{t+{t}^{2}},0⟩$
- $⟨1,-\frac{t}{1+{t}^{2}},0⟩$

By the chain rule, we have 

$$
(g∘u)^{′}(t)=g′(u(t))u′(t).
$$

Now, let's find the derivatives of each function:

$$
\begin{aligned}{g}^{′}(u) & =⟨\frac{\text{d}}{\text{d}u}(\frac{1}{u}),\,\frac{\text{d}}{\text{d}u}(\operatorname{ln}⁡(u+1)),\,\frac{\text{d}}{\text{d}u}(1)⟩ \\  & =⟨-\frac{1}{{u}^{2}},\,\frac{1}{u+1},\,0⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\frac{1}{t})=-\frac{1}{{t}^{2}}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(g∘u)^{′}(t) & =g′(u(t))u′(t) \\  & =⟨-\frac{1}{(u(t))^{2}},\,\frac{1}{u(t)+1},\,0⟩\cdot {u}^{′}(t) \\  & =⟨-{t}^{2},\,\frac{t}{1+t},\,0⟩\cdot (-\frac{1}{{t}^{2}}) \\  & =⟨1,-\frac{1}{t+{t}^{2}},0⟩.\end{aligned}
$$

---

**Source replay — notation normalized, repairs listed in metadata**

## reciprocal_log_reciprocal — easy (observed)

If $g(u)=⟨\frac{1}{u},\,\log{\left(u + 1 \right)},\,1⟩$ and $u(t)=\frac{1}{t}$, then $(g∘u)^{′}(t)=$

- $⟨\frac{1}{t},\,- \frac{1}{t \left(t + 1\right)},\,0⟩$
- $⟨1,\,- \frac{1}{t \left(t + 1\right)},\,0⟩$ **correct**
- $⟨- \frac{1}{t^{2}},\,- \frac{t^{2}}{t^{2} + 1},\,0⟩$
- $⟨-1,\,- \frac{t}{t^{2} + 2},\,0⟩$
- $⟨1,\,- \frac{t}{t^{2} + 1},\,0⟩$

By the chain rule, we have 

$$
(g∘u)^{′}(t)=g′(u(t))u′(t)
$$

Now, let's find the derivatives of each function:

$$
\begin{aligned}g^{′}(u) & =⟨\frac{\text{d}}{\text{d}u}\left(\frac{1}{u}\right),\,\frac{\text{d}}{\text{d}u}\left(\log{\left(u + 1 \right)}\right),\,\frac{\text{d}}{\text{d}u}\left(1\right)⟩ \\  & =⟨- \frac{1}{u^{2}},\,\frac{1}{u + 1},\,0⟩ \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(\frac{1}{t}\right)=- \frac{1}{t^{2}}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(g∘u)^{′}(t) & =g′(u(t))u′(t) \\  & =⟨- \frac{1}{u(t)^{2}},\,\frac{1}{u(t) + 1},\,0⟩\cdot \left(u^{′}(t)\right) \\  & =⟨- t^{2},\,\frac{1}{1 + \frac{1}{t}},\,0⟩\cdot \left(- \frac{1}{t^{2}}\right) \\  & =⟨1,\,- \frac{1}{t \left(t + 1\right)},\,0⟩\end{aligned}
$$

---

## Original q-70695

If $f(u)=[\begin{aligned}\operatorname{cos}⁡u \\ {u}^{3} \\ \operatorname{ln}⁡u\end{aligned}]$ and $u(t)={e}^{t}$, then $(f∘u)^{′}(t)=$

- $[\begin{aligned}-\operatorname{cos}⁡({e}^{t}){e}^{t} \\ 3{e}^{t} \\ 1\end{aligned}]$
- $[\begin{aligned}-\operatorname{sin}⁡({e}^{2t}) \\ 3{e}^{2t} \\ 1\end{aligned}]$
- $[\begin{aligned}\operatorname{cos}⁡({e}^{t}){e}^{t} \\ 3{e}^{3t} \\ {e}^{2t}\end{aligned}]$
- $[\begin{aligned}\operatorname{sin}⁡({e}^{2t}) \\ {e}^{3t} \\ \frac{1}{{e}^{2t}}\end{aligned}]$
- $[\begin{aligned}-\operatorname{sin}⁡({e}^{t}){e}^{t} \\ 3{e}^{3t} \\ 1\end{aligned}]$ **correct**

Using the chain rule, we can write

$$
(f∘u)^{′}(t)={f}^{′}(u(t)){u}^{′}(t).
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}(\operatorname{cos}⁡u) \\ \frac{\text{d}}{\text{d}u}\,({u}^{3}) \\ \frac{\text{d}}{\text{d}u}(\operatorname{ln}⁡u)\end{aligned}]=[\begin{aligned}-\operatorname{sin}⁡u \\ 3{u}^{2} \\ \frac{1}{u}\end{aligned}] \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{t})={e}^{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & ={f}^{′}(u(t)){u}^{′}(t) \\  & =[\begin{aligned}-\operatorname{sin}⁡(u(t)) \\ 3(u(t))^{2} \\ \frac{1}{u(t)}\end{aligned}]\cdot {u}^{′}(t) \\  & =[\begin{aligned}-\operatorname{sin}⁡({e}^{t}) \\ 3({e}^{t})^{2} \\ \frac{1}{{e}^{t}}\end{aligned}]\cdot {e}^{t} \\  & =[\begin{aligned}-\operatorname{sin}⁡({e}^{t}) \\ 3{e}^{2t} \\ \frac{1}{{e}^{t}}\end{aligned}]\cdot {e}^{t} \\  & =[\begin{aligned}-\operatorname{sin}⁡({e}^{t}){e}^{t} \\ 3{e}^{3t} \\ 1\end{aligned}]\end{aligned}
$$

---

**Source replay — notation normalized, repairs listed in metadata**

## cos_cube_log_exp — easy (observed)

If $f(u)=[\begin{aligned}\cos{\left(u \right)} \\ u^{3} \\ \log{\left(u \right)}\end{aligned}]$ and $u(t)=e^{t}$, then $(f∘u)^{′}(t)=$

- $[\begin{aligned}\sin{\left(e^{2 t} \right)} \\ e^{3 t} \\ e^{- 2 t}\end{aligned}]$
- $[\begin{aligned}e^{t} \cos{\left(e^{t} \right)} \\ 3 e^{3 t} \\ e^{2 t}\end{aligned}]$
- $[\begin{aligned}- \sin{\left(e^{2 t} \right)} \\ 3 e^{2 t} \\ 1\end{aligned}]$
- $[\begin{aligned}- e^{t} \cos{\left(e^{t} \right)} \\ 3 e^{t} \\ 1\end{aligned}]$
- $[\begin{aligned}- e^{t} \sin{\left(e^{t} \right)} \\ 3 e^{3 t} \\ 1\end{aligned}]$ **correct**

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(\cos{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(u^{3}\right) \\ \frac{\text{d}}{\text{d}u}\left(\log{\left(u \right)}\right)\end{aligned}]=[\begin{aligned}- \sin{\left(u \right)} \\ 3 u^{2} \\ \frac{1}{u}\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(e^{t}\right)=e^{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}- \sin{\left(u(t) \right)} \\ 3 u(t)^{2} \\ \frac{1}{u(t)}\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}- \sin{\left(e^{t} \right)} \\ 3 e^{2 t} \\ e^{- t}\end{aligned}]\cdot \left(e^{t}\right) \\  & =[\begin{aligned}- \sin{\left(e^{t} \right)} \\ 3 e^{2 t} \\ e^{- t}\end{aligned}]\cdot \left(e^{t}\right) \\  & =[\begin{aligned}- e^{t} \sin{\left(e^{t} \right)} \\ 3 e^{3 t} \\ 1\end{aligned}]\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## linear_quadratic_affine — easy (authored)

If $f(u)=[\begin{aligned}3 u \\ u^{2} \\ 2\end{aligned}]$ and $u(t)=4 t + 2$, then $(f∘u)^{′}(t)=$

- $[\begin{aligned}12 \\ 32 t + 16 \\ 0\end{aligned}]$ **correct**
- $[\begin{aligned}3 \\ 2 u \\ 0\end{aligned}]$
- $[\begin{aligned}3 \\ 8 t + 4 \\ 0\end{aligned}]$
- $[\begin{aligned}48 \\ 128 t + 64 \\ 0\end{aligned}]$
- $[\begin{aligned}12 \\ 8 t + 4 \\ 0\end{aligned}]$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(3 u\right) \\ \frac{\text{d}}{\text{d}u}\left(u^{2}\right) \\ \frac{\text{d}}{\text{d}u}\left(2\right)\end{aligned}]=[\begin{aligned}3 \\ 2 u \\ 0\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(4 t + 2\right)=4\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}3 \\ 2 u(t) \\ 0\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}3 \\ 8 t + 4 \\ 0\end{aligned}]\cdot \left(4\right) \\  & =[\begin{aligned}12 \\ 32 t + 16 \\ 0\end{aligned}]\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## linear_quadratic_affine — easy (authored)

If $f(u)=[\begin{aligned}u \\ u^{2} \\ 1\end{aligned}]$ and $u(t)=4 t - 4$, then $(f∘u)^{′}(t)=$

- $[\begin{aligned}16 \\ 128 t - 128 \\ 0\end{aligned}]$
- $[\begin{aligned}1 \\ 2 u \\ 0\end{aligned}]$
- $[\begin{aligned}1 \\ 8 t - 8 \\ 0\end{aligned}]$
- $[\begin{aligned}4 \\ 32 t - 32 \\ 0\end{aligned}]$ **correct**
- $[\begin{aligned}4 \\ 8 t - 8 \\ 0\end{aligned}]$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(u\right) \\ \frac{\text{d}}{\text{d}u}\left(u^{2}\right) \\ \frac{\text{d}}{\text{d}u}\left(1\right)\end{aligned}]=[\begin{aligned}1 \\ 2 u \\ 0\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(4 t - 4\right)=4\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}1 \\ 2 u(t) \\ 0\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}1 \\ 8 t - 8 \\ 0\end{aligned}]\cdot \left(4\right) \\  & =[\begin{aligned}4 \\ 32 t - 32 \\ 0\end{aligned}]\end{aligned}
$$

---

**Generated variant — observed workload; observed bank**

## linear_quadratic_affine — easy (observed)

If $f(u)=[\begin{aligned}u \\ u^{2} \\ 2\end{aligned}]$ and $u(t)=2 t + 4$, then $(f∘u)^{′}(t)=$

- $[\begin{aligned}2 \\ 8 t + 16 \\ 0\end{aligned}]$ **correct**
- $[\begin{aligned}1 \\ 2 t \\ 0\end{aligned}]$
- $[\begin{aligned}2 \\ 8 t \\ 0\end{aligned}]$
- $[\begin{aligned}1 \\ 4 t + 8 \\ 0\end{aligned}]$
- $[\begin{aligned}2 \\ 4 t + 8 \\ 0\end{aligned}]$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(u\right) \\ \frac{\text{d}}{\text{d}u}\left(u^{2}\right) \\ \frac{\text{d}}{\text{d}u}\left(2\right)\end{aligned}]=[\begin{aligned}1 \\ 2 u \\ 0\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(2 t + 4\right)=2\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}1 \\ 2 u(t) \\ 0\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}1 \\ 4 t + 8 \\ 0\end{aligned}]\cdot \left(2\right) \\  & =[\begin{aligned}2 \\ 8 t + 16 \\ 0\end{aligned}]\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## cos_quadratic_power — easy (authored)

If $f(u)=\cos{\left(u \right)}\,i+\left(3 - u^{2}\right)\,j+3\,k$ and $u(t)=4 t^{3}$ then $(f∘u)^{′}(t)=$

- $-12 t^{2} \sin{\left(4 t^{3} \right)}\,i-96 t^{5}\,j$ **correct**
- $-\sin{\left(u \right)}\,i-2 u\,j$
- $-\sin{\left(4 t^{3} \right)}\,i-8 t^{3}\,j$
- $-144 t^{4} \sin{\left(4 t^{3} \right)}\,i-1152 t^{7}\,j$
- $-12 t^{2} \sin{\left(4 t^{3} \right)}\,i-8 t^{3}\,j$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\frac{\text{d}}{\text{d}u}\left(\cos{\left(u \right)}\right)\,i+\frac{\text{d}}{\text{d}u}\left(3 - u^{2}\right)\,j+\frac{\text{d}}{\text{d}u}\left(3\right)\,k \\  & =-\sin{\left(u \right)}\,i-2 u\,j+0\,k \\  & =-\sin{\left(u \right)}\,i-2 u\,j \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(4 t^{3}\right)=12 t^{2}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\left(-\sin{\left(u(t) \right)}\,i-2 u(t)\,j\right)\cdot \left(u^{′}(t)\right) \\  & =\left(-\sin{\left(4 t^{3} \right)}\,i-8 t^{3}\,j\right)\cdot \left(12 t^{2}\right) \\  & =-12 t^{2} \sin{\left(4 t^{3} \right)}\,i-96 t^{5}\,j\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## cos_quadratic_power — easy (authored)

If $f(u)=\cos{\left(u \right)}\,i+\left(3 - u^{2}\right)\,j+3\,k$ and $u(t)=t^{3}$ then $(f∘u)^{′}(t)=$

- $-9 t^{4} \sin{\left(t^{3} \right)}\,i-18 t^{7}\,j$
- $-\sin{\left(u \right)}\,i-2 u\,j$
- $-\sin{\left(t^{3} \right)}\,i-2 t^{3}\,j$
- $-3 t^{2} \sin{\left(t^{3} \right)}\,i-6 t^{5}\,j$ **correct**
- $-3 t^{2} \sin{\left(t^{3} \right)}\,i-2 t^{3}\,j$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\frac{\text{d}}{\text{d}u}\left(\cos{\left(u \right)}\right)\,i+\frac{\text{d}}{\text{d}u}\left(3 - u^{2}\right)\,j+\frac{\text{d}}{\text{d}u}\left(3\right)\,k \\  & =-\sin{\left(u \right)}\,i-2 u\,j+0\,k \\  & =-\sin{\left(u \right)}\,i-2 u\,j \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(t^{3}\right)=3 t^{2}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\left(-\sin{\left(u(t) \right)}\,i-2 u(t)\,j\right)\cdot \left(u^{′}(t)\right) \\  & =\left(-\sin{\left(t^{3} \right)}\,i-2 t^{3}\,j\right)\cdot \left(3 t^{2}\right) \\  & =-3 t^{2} \sin{\left(t^{3} \right)}\,i-6 t^{5}\,j\end{aligned}
$$

---

**Generated variant — observed workload; observed bank**

## cos_quadratic_power — easy (observed)

If $f(u)=\cos{\left(u \right)}\,i+\left(3 - u^{2}\right)\,j+4\,k$ and $u(t)=2 t^{3}$ then $(f∘u)^{′}(t)=$

- $-\sin{\left(6 t^{2} \right)}\,i-12 t^{2}\,j$
- $-\sin{\left(u \right)}\,i-2 u\,j$
- $-4 t^{2} \sin{\left(2 t^{3} \right)}\,i-8 t^{5}\,j$
- $-6 t^{2} \sin{\left(2 t^{3} \right)}\,i-24 t^{5}\,j$ **correct**
- $-\sin{\left(2 t^{3} \right)}\,i-12 t^{3}\,j$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\frac{\text{d}}{\text{d}u}\left(\cos{\left(u \right)}\right)\,i+\frac{\text{d}}{\text{d}u}\left(3 - u^{2}\right)\,j+\frac{\text{d}}{\text{d}u}\left(4\right)\,k \\  & =-\sin{\left(u \right)}\,i-2 u\,j+0\,k \\  & =-\sin{\left(u \right)}\,i-2 u\,j \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(2 t^{3}\right)=6 t^{2}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\left(-\sin{\left(u(t) \right)}\,i-2 u(t)\,j\right)\cdot \left(u^{′}(t)\right) \\  & =\left(-\sin{\left(2 t^{3} \right)}\,i-4 t^{3}\,j\right)\cdot \left(6 t^{2}\right) \\  & =-6 t^{2} \sin{\left(2 t^{3} \right)}\,i-24 t^{5}\,j\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## sin_log_tan_power — easy (authored)

If $g(u)=⟨\sin{\left(u \right)},\,\log{\left(3 u \right)},\,\tan{\left(u \right)}⟩$ and $u(t)=4 t^{2}$ then $(g∘u)^{′}(t)=$

- $⟨8 t \cos{\left(4 t^{2} \right)},\,\frac{2}{t},\,\frac{8 t}{\cos^{2}{\left(4 t^{2} \right)}}⟩$ **correct**
- $⟨\cos{\left(u \right)},\,\frac{1}{u},\,\tan^{2}{\left(u \right)} + 1⟩$
- $⟨\cos{\left(4 t^{2} \right)},\,\frac{1}{4 t^{2}},\,\tan^{2}{\left(4 t^{2} \right)} + 1⟩$
- $⟨64 t^{2} \cos{\left(4 t^{2} \right)},\,16,\,64 t^{2} \left(\tan^{2}{\left(4 t^{2} \right)} + 1\right)⟩$
- $⟨8 t \cos{\left(4 t^{2} \right)},\,\frac{1}{4 t^{2}},\,\tan^{2}{\left(4 t^{2} \right)} + 1⟩$

By the chain rule, we have 

$$
(g∘u)^{′}(t)=g′(u(t))u′(t)
$$

Now, let's find the derivatives of each function:

$$
\begin{aligned}g^{′}(u) & =⟨\frac{\text{d}}{\text{d}u}\left(\sin{\left(u \right)}\right),\,\frac{\text{d}}{\text{d}u}\left(\log{\left(3 u \right)}\right),\,\frac{\text{d}}{\text{d}u}\left(\tan{\left(u \right)}\right)⟩ \\  & =⟨\cos{\left(u \right)},\,\frac{1}{u},\,\tan^{2}{\left(u \right)} + 1⟩ \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(4 t^{2}\right)=8 t\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(g∘u)^{′}(t) & =g′(u(t))u′(t) \\  & =⟨\cos{\left(u(t) \right)},\,\frac{1}{u(t)},\,\tan^{2}{\left(u(t) \right)} + 1⟩\cdot \left(u^{′}(t)\right) \\  & =⟨\cos{\left(4 t^{2} \right)},\,\frac{1}{4 t^{2}},\,\tan^{2}{\left(4 t^{2} \right)} + 1⟩\cdot \left(8 t\right) \\  & =⟨8 t \cos{\left(4 t^{2} \right)},\,\frac{2}{t},\,\frac{8 t}{\cos^{2}{\left(4 t^{2} \right)}}⟩\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## sin_log_tan_power — easy (authored)

If $g(u)=⟨\sin{\left(u \right)},\,\log{\left(3 u \right)},\,\tan{\left(u \right)}⟩$ and $u(t)=t^{2}$ then $(g∘u)^{′}(t)=$

- $⟨4 t^{2} \cos{\left(t^{2} \right)},\,4,\,4 t^{2} \left(\tan^{2}{\left(t^{2} \right)} + 1\right)⟩$
- $⟨\cos{\left(u \right)},\,\frac{1}{u},\,\tan^{2}{\left(u \right)} + 1⟩$
- $⟨\cos{\left(t^{2} \right)},\,\frac{1}{t^{2}},\,\tan^{2}{\left(t^{2} \right)} + 1⟩$
- $⟨2 t \cos{\left(t^{2} \right)},\,\frac{2}{t},\,\frac{2 t}{\cos^{2}{\left(t^{2} \right)}}⟩$ **correct**
- $⟨2 t \cos{\left(t^{2} \right)},\,\frac{1}{t^{2}},\,\tan^{2}{\left(t^{2} \right)} + 1⟩$

By the chain rule, we have 

$$
(g∘u)^{′}(t)=g′(u(t))u′(t)
$$

Now, let's find the derivatives of each function:

$$
\begin{aligned}g^{′}(u) & =⟨\frac{\text{d}}{\text{d}u}\left(\sin{\left(u \right)}\right),\,\frac{\text{d}}{\text{d}u}\left(\log{\left(3 u \right)}\right),\,\frac{\text{d}}{\text{d}u}\left(\tan{\left(u \right)}\right)⟩ \\  & =⟨\cos{\left(u \right)},\,\frac{1}{u},\,\tan^{2}{\left(u \right)} + 1⟩ \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(t^{2}\right)=2 t\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(g∘u)^{′}(t) & =g′(u(t))u′(t) \\  & =⟨\cos{\left(u(t) \right)},\,\frac{1}{u(t)},\,\tan^{2}{\left(u(t) \right)} + 1⟩\cdot \left(u^{′}(t)\right) \\  & =⟨\cos{\left(t^{2} \right)},\,\frac{1}{t^{2}},\,\tan^{2}{\left(t^{2} \right)} + 1⟩\cdot \left(2 t\right) \\  & =⟨2 t \cos{\left(t^{2} \right)},\,\frac{2}{t},\,\frac{2 t}{\cos^{2}{\left(t^{2} \right)}}⟩\end{aligned}
$$

---

**Generated variant — observed workload; observed bank**

## sin_log_tan_power — easy (observed)

If $g(u)=⟨\sin{\left(u \right)},\,\log{\left(3 u \right)},\,\tan{\left(u \right)}⟩$ and $u(t)=2 t^{2}$ then $(g∘u)^{′}(t)=$

- $⟨\cos{\left(2 t^{2} \right)},\,\frac{1}{2 t^{2}},\,2 t \sec^{2}{\left(2 t^{2} \right)}⟩$
- $⟨4 t \sec{\left(2 t^{2} \right)},\,\frac{1}{t},\,4 t \sin{\left(2 t^{2} \right)}⟩$
- $⟨4 t \sin{\left(2 t^{2} \right)},\,\frac{1}{t},\,4 t \cos^{2}{\left(2 t^{2} \right)}⟩$
- $⟨\cos{\left(2 t^{2} \right)},\,\frac{1}{t},\,4 t⟩$
- $⟨4 t \cos{\left(2 t^{2} \right)},\,\frac{2}{t},\,\frac{4 t}{\cos^{2}{\left(2 t^{2} \right)}}⟩$ **correct**

By the chain rule, we have 

$$
(g∘u)^{′}(t)=g′(u(t))u′(t)
$$

Now, let's find the derivatives of each function:

$$
\begin{aligned}g^{′}(u) & =⟨\frac{\text{d}}{\text{d}u}\left(\sin{\left(u \right)}\right),\,\frac{\text{d}}{\text{d}u}\left(\log{\left(3 u \right)}\right),\,\frac{\text{d}}{\text{d}u}\left(\tan{\left(u \right)}\right)⟩ \\  & =⟨\cos{\left(u \right)},\,\frac{1}{u},\,\tan^{2}{\left(u \right)} + 1⟩ \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(2 t^{2}\right)=4 t\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(g∘u)^{′}(t) & =g′(u(t))u′(t) \\  & =⟨\cos{\left(u(t) \right)},\,\frac{1}{u(t)},\,\tan^{2}{\left(u(t) \right)} + 1⟩\cdot \left(u^{′}(t)\right) \\  & =⟨\cos{\left(2 t^{2} \right)},\,\frac{1}{2 t^{2}},\,\tan^{2}{\left(2 t^{2} \right)} + 1⟩\cdot \left(4 t\right) \\  & =⟨4 t \cos{\left(2 t^{2} \right)},\,\frac{2}{t},\,\frac{4 t}{\cos^{2}{\left(2 t^{2} \right)}}⟩\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## linear_quadratic_exp — easy (authored)

If $f(u)=[\begin{aligned}3 u \\ u^{2} \\ 3\end{aligned}]$ and $u(t)=e^{4 t}$, then $(f∘u)^{′}(t)=$

- $[\begin{aligned}12 e^{4 t} \\ 8 e^{8 t} \\ 0\end{aligned}]$ **correct**
- $[\begin{aligned}3 \\ 2 u \\ 0\end{aligned}]$
- $[\begin{aligned}3 \\ 2 e^{4 t} \\ 0\end{aligned}]$
- $[\begin{aligned}48 e^{8 t} \\ 32 e^{12 t} \\ 0\end{aligned}]$
- $[\begin{aligned}12 e^{4 t} \\ 2 e^{4 t} \\ 0\end{aligned}]$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(3 u\right) \\ \frac{\text{d}}{\text{d}u}\left(u^{2}\right) \\ \frac{\text{d}}{\text{d}u}\left(3\right)\end{aligned}]=[\begin{aligned}3 \\ 2 u \\ 0\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(e^{4 t}\right)=4 e^{4 t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}3 \\ 2 u(t) \\ 0\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}3 \\ 2 e^{4 t} \\ 0\end{aligned}]\cdot \left(4 e^{4 t}\right) \\  & =[\begin{aligned}12 e^{4 t} \\ 8 e^{8 t} \\ 0\end{aligned}]\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## linear_quadratic_exp — easy (authored)

If $f(u)=[\begin{aligned}3 u \\ u^{2} \\ 1\end{aligned}]$ and $u(t)=e^{t}$, then $(f∘u)^{′}(t)=$

- $[\begin{aligned}3 e^{2 t} \\ 2 e^{3 t} \\ 0\end{aligned}]$
- $[\begin{aligned}3 \\ 2 u \\ 0\end{aligned}]$
- $[\begin{aligned}3 \\ 2 e^{t} \\ 0\end{aligned}]$
- $[\begin{aligned}3 e^{t} \\ 2 e^{2 t} \\ 0\end{aligned}]$ **correct**
- $[\begin{aligned}3 e^{t} \\ 2 e^{t} \\ 0\end{aligned}]$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(3 u\right) \\ \frac{\text{d}}{\text{d}u}\left(u^{2}\right) \\ \frac{\text{d}}{\text{d}u}\left(1\right)\end{aligned}]=[\begin{aligned}3 \\ 2 u \\ 0\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(e^{t}\right)=e^{t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}3 \\ 2 u(t) \\ 0\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}3 \\ 2 e^{t} \\ 0\end{aligned}]\cdot \left(e^{t}\right) \\  & =[\begin{aligned}3 e^{t} \\ 2 e^{2 t} \\ 0\end{aligned}]\end{aligned}
$$

---

**Generated variant — observed workload; observed bank**

## linear_quadratic_exp — easy (observed)

If $f(u)=[\begin{aligned}4 u \\ u^{2} \\ 1\end{aligned}]$ and $u(t)=e^{2 t}$, then $(f∘u)^{′}(t)=$

- $[\begin{aligned}4 \\ 2 e^{2 t} \\ 0\end{aligned}]$
- $[\begin{aligned}4 t \\ 2 e^{2 t} \\ 0\end{aligned}]$
- $[\begin{aligned}8 e^{2 t} \\ 2 e^{2 t} \\ 0\end{aligned}]$
- $[\begin{aligned}8 e^{2 t} \\ 4 e^{4 t} \\ 0\end{aligned}]$ **correct**
- $[\begin{aligned}4 \\ 3 e^{2 t} \\ 0\end{aligned}]$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(4 u\right) \\ \frac{\text{d}}{\text{d}u}\left(u^{2}\right) \\ \frac{\text{d}}{\text{d}u}\left(1\right)\end{aligned}]=[\begin{aligned}4 \\ 2 u \\ 0\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(e^{2 t}\right)=2 e^{2 t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}4 \\ 2 u(t) \\ 0\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}4 \\ 2 e^{2 t} \\ 0\end{aligned}]\cdot \left(2 e^{2 t}\right) \\  & =[\begin{aligned}8 e^{2 t} \\ 4 e^{4 t} \\ 0\end{aligned}]\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## linear_vector_power — easy (authored)

If  $f(u)=3 u\,i+u\,j+u\,k$ and $u(t)=2 t^{2}$, then $(f∘u)^{′}(t)=$

- $12 t\,i+4 t\,j+4 t\,k$ **correct**
- $6 t^{2}\,i+2 t^{2}\,j+2 t^{2}\,k$
- $3\,i+\,j+\,k$
- $24 t\,i+8 t\,j+8 t\,k$
- $12 t\,i+12 t\,j+12 t\,k$

Using the chain rule, we can write 

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Now, let's find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\frac{\text{d}}{\text{d}u}\left(3 u\right)\,i+\frac{\text{d}}{\text{d}u}\left(u\right)\,j+\frac{\text{d}}{\text{d}u}\left(u\right)\,k \\  & =3\,i+\,j+\,k \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(2 t^{2}\right) \\  & =4 t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\left(3\,i+\,j+\,k\right)\cdot \left(4 t\right) \\  & =12 t\,i+4 t\,j+4 t\,k\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## linear_vector_power — easy (authored)

If  $f(u)=3 u\,i+3 u\,j+u\,k$ and $u(t)=t^{2}$, then $(f∘u)^{′}(t)=$

- $12 t\,i+12 t\,j+4 t\,k$
- $3 t^{2}\,i+3 t^{2}\,j+t^{2}\,k$
- $3\,i+3\,j+\,k$
- $6 t\,i+6 t\,j+2 t\,k$ **correct**
- $6 t\,i+6 t\,j+6 t\,k$

Using the chain rule, we can write 

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Now, let's find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\frac{\text{d}}{\text{d}u}\left(3 u\right)\,i+\frac{\text{d}}{\text{d}u}\left(3 u\right)\,j+\frac{\text{d}}{\text{d}u}\left(u\right)\,k \\  & =3\,i+3\,j+\,k \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(t^{2}\right) \\  & =2 t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\left(3\,i+3\,j+\,k\right)\cdot \left(2 t\right) \\  & =6 t\,i+6 t\,j+2 t\,k\end{aligned}
$$

---

**Generated variant — observed workload; observed bank**

## linear_vector_power — easy (observed)

If  $f(u)=3 u\,i+4 u\,j+u\,k$ and $u(t)=2 t^{2}$, then $(f∘u)^{′}(t)=$

- $12 t\,i+16 t\,j+4 t\,k$ **correct**
- $6 t^{2}\,i+8 t^{2}\,j+2 t^{2}\,k$
- $24 t\,i+32 t\,j+8 t\,k$
- $8 t\,i+8 t\,j+8 t\,k$
- $3\,i+4\,j+\,k$

Using the chain rule, we can write 

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Now, let's find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\frac{\text{d}}{\text{d}u}\left(3 u\right)\,i+\frac{\text{d}}{\text{d}u}\left(4 u\right)\,j+\frac{\text{d}}{\text{d}u}\left(u\right)\,k \\  & =3\,i+4\,j+\,k \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(2 t^{2}\right) \\  & =4 t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\left(3\,i+4\,j+\,k\right)\cdot \left(4 t\right) \\  & =12 t\,i+16 t\,j+4 t\,k\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## log_quadratic_log — easy (authored)

If $g(u)=[\begin{aligned}\log{\left(u \right)} \\ 3 \\ u^{2}\end{aligned}]$ and $u(t)=4 \log{\left(t \right)}$, then  $(g∘u)^{′}(t)=$

- $[\begin{aligned}\frac{1}{t \log{\left(t \right)}} \\ 0 \\ \frac{32 \log{\left(t \right)}}{t}\end{aligned}]$ **correct**
- $[\begin{aligned}\frac{1}{u} \\ 0 \\ 2 u\end{aligned}]$
- $[\begin{aligned}\frac{1}{4 \log{\left(t \right)}} \\ 0 \\ 8 \log{\left(t \right)}\end{aligned}]$
- $[\begin{aligned}\frac{4}{t^{2} \log{\left(t \right)}} \\ 0 \\ \frac{128 \log{\left(t \right)}}{t^{2}}\end{aligned}]$
- $[\begin{aligned}\frac{1}{t \log{\left(t \right)}} \\ 0 \\ 8 \log{\left(t \right)}\end{aligned}]$

By the chain rule, we have 

$$
(g∘u)^{′}(t)=g′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}g^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(\log{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(3\right) \\ \frac{\text{d}}{\text{d}u}\left(u^{2}\right)\end{aligned}]=[\begin{aligned}\frac{1}{u} \\ 0 \\ 2 u\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(4 \log{\left(t \right)}\right)=\frac{4}{t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(g∘u)^{′}(t) & =g′(u(t))u′(t) \\  & =[\begin{aligned}\frac{1}{u(t)} \\ 0 \\ 2 u(t)\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}\frac{1}{4 \log{\left(t \right)}} \\ 0 \\ 8 \log{\left(t \right)}\end{aligned}]\cdot \left(\frac{4}{t}\right) \\  & =[\begin{aligned}\frac{1}{t \log{\left(t \right)}} \\ 0 \\ \frac{32 \log{\left(t \right)}}{t}\end{aligned}]\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## log_quadratic_log — easy (authored)

If $g(u)=[\begin{aligned}\log{\left(u \right)} \\ 3 \\ u^{2}\end{aligned}]$ and $u(t)=\log{\left(t \right)}$, then  $(g∘u)^{′}(t)=$

- $[\begin{aligned}\frac{1}{t^{2} \log{\left(t \right)}} \\ 0 \\ \frac{2 \log{\left(t \right)}}{t^{2}}\end{aligned}]$
- $[\begin{aligned}\frac{1}{u} \\ 0 \\ 2 u\end{aligned}]$
- $[\begin{aligned}\frac{1}{\log{\left(t \right)}} \\ 0 \\ 2 \log{\left(t \right)}\end{aligned}]$
- $[\begin{aligned}\frac{1}{t \log{\left(t \right)}} \\ 0 \\ \frac{2 \log{\left(t \right)}}{t}\end{aligned}]$ **correct**
- $[\begin{aligned}\frac{1}{t \log{\left(t \right)}} \\ 0 \\ 2 \log{\left(t \right)}\end{aligned}]$

By the chain rule, we have 

$$
(g∘u)^{′}(t)=g′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}g^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(\log{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(3\right) \\ \frac{\text{d}}{\text{d}u}\left(u^{2}\right)\end{aligned}]=[\begin{aligned}\frac{1}{u} \\ 0 \\ 2 u\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(\log{\left(t \right)}\right)=\frac{1}{t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(g∘u)^{′}(t) & =g′(u(t))u′(t) \\  & =[\begin{aligned}\frac{1}{u(t)} \\ 0 \\ 2 u(t)\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}\frac{1}{\log{\left(t \right)}} \\ 0 \\ 2 \log{\left(t \right)}\end{aligned}]\cdot \left(\frac{1}{t}\right) \\  & =[\begin{aligned}\frac{1}{t \log{\left(t \right)}} \\ 0 \\ \frac{2 \log{\left(t \right)}}{t}\end{aligned}]\end{aligned}
$$

---

**Generated variant — observed workload; observed bank**

## log_quadratic_log — easy (observed)

If $g(u)=[\begin{aligned}\log{\left(u \right)} \\ 3 \\ u^{2}\end{aligned}]$ and $u(t)=2 \log{\left(t \right)}$, then  $(g∘u)^{′}(t)=$

- $[\begin{aligned}\frac{1}{2 \log{\left(t \right)}} \\ 0 \\ 4 \log{\left(t \right)}\end{aligned}]$
- $[\begin{aligned}\frac{1}{t \log{\left(t \right)}} \\ 0 \\ \frac{8 \log{\left(t \right)}}{t}\end{aligned}]$ **correct**
- $[\begin{aligned}\frac{1}{2 \log{\left(t \right)}} \\ 0 \\ \frac{8 \log{\left(t \right)}}{t}\end{aligned}]$
- $[\begin{aligned}\frac{1}{u} \\ 0 \\ 2 u\end{aligned}]$
- $[\begin{aligned}u \\ 3 \\ 2 u\end{aligned}]$

By the chain rule, we have 

$$
(g∘u)^{′}(t)=g′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}g^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(\log{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(3\right) \\ \frac{\text{d}}{\text{d}u}\left(u^{2}\right)\end{aligned}]=[\begin{aligned}\frac{1}{u} \\ 0 \\ 2 u\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(2 \log{\left(t \right)}\right)=\frac{2}{t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(g∘u)^{′}(t) & =g′(u(t))u′(t) \\  & =[\begin{aligned}\frac{1}{u(t)} \\ 0 \\ 2 u(t)\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}\frac{1}{2 \log{\left(t \right)}} \\ 0 \\ 4 \log{\left(t \right)}\end{aligned}]\cdot \left(\frac{2}{t}\right) \\  & =[\begin{aligned}\frac{1}{t \log{\left(t \right)}} \\ 0 \\ \frac{8 \log{\left(t \right)}}{t}\end{aligned}]\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## log_reciprocal_exp — easy (authored)

If $g(u)=⟨\log{\left(u \right)},\,0,\,\frac{1}{u}⟩$ and $u(t)=e^{4 t}$, then $(g∘u)^{′}(t)=$

- $⟨4,\,0,\,- 4 e^{- 4 t}⟩$ **correct**
- $⟨\frac{1}{u},\,0,\,- \frac{1}{u^{2}}⟩$
- $⟨e^{- 4 t},\,0,\,- e^{- 8 t}⟩$
- $⟨16 e^{4 t},\,0,\,-16⟩$
- $⟨4,\,0,\,- e^{- 8 t}⟩$

By the chain rule, we have 

$$
(g∘u)^{′}(t)=g′(u(t))u′(t)
$$

Now, let's find the derivatives of each function:

$$
\begin{aligned}g^{′}(u) & =⟨\frac{\text{d}}{\text{d}u}\left(\log{\left(u \right)}\right),\,\frac{\text{d}}{\text{d}u}\left(0\right),\,\frac{\text{d}}{\text{d}u}\left(\frac{1}{u}\right)⟩ \\  & =⟨\frac{1}{u},\,0,\,- \frac{1}{u^{2}}⟩ \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(e^{4 t}\right)=4 e^{4 t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(g∘u)^{′}(t) & =g′(u(t))u′(t) \\  & =⟨\frac{1}{u(t)},\,0,\,- \frac{1}{u(t)^{2}}⟩\cdot \left(u^{′}(t)\right) \\  & =⟨e^{- 4 t},\,0,\,- e^{- 8 t}⟩\cdot \left(4 e^{4 t}\right) \\  & =⟨e^{- 4 t} 4 e^{4 t},\,0 \cdot 4 e^{4 t},\,- e^{- 8 t} 4 e^{4 t}⟩ \\  & =⟨4,\,0,\,- 4 e^{- 4 t}⟩\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## log_reciprocal_exp — easy (authored)

If $g(u)=⟨\log{\left(u \right)},\,0,\,\frac{1}{u}⟩$ and $u(t)=e^{t}$, then $(g∘u)^{′}(t)=$

- $⟨e^{t},\,0,\,-1⟩$
- $⟨\frac{1}{u},\,0,\,- \frac{1}{u^{2}}⟩$
- $⟨e^{- t},\,0,\,- e^{- 2 t}⟩$
- $⟨1,\,0,\,- e^{- t}⟩$ **correct**
- $⟨1,\,0,\,- e^{- 2 t}⟩$

By the chain rule, we have 

$$
(g∘u)^{′}(t)=g′(u(t))u′(t)
$$

Now, let's find the derivatives of each function:

$$
\begin{aligned}g^{′}(u) & =⟨\frac{\text{d}}{\text{d}u}\left(\log{\left(u \right)}\right),\,\frac{\text{d}}{\text{d}u}\left(0\right),\,\frac{\text{d}}{\text{d}u}\left(\frac{1}{u}\right)⟩ \\  & =⟨\frac{1}{u},\,0,\,- \frac{1}{u^{2}}⟩ \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(e^{t}\right)=e^{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(g∘u)^{′}(t) & =g′(u(t))u′(t) \\  & =⟨\frac{1}{u(t)},\,0,\,- \frac{1}{u(t)^{2}}⟩\cdot \left(u^{′}(t)\right) \\  & =⟨e^{- t},\,0,\,- e^{- 2 t}⟩\cdot \left(e^{t}\right) \\  & =⟨e^{- t} e^{t},\,0 e^{t},\,- e^{- 2 t} e^{t}⟩ \\  & =⟨1,\,0,\,- e^{- t}⟩\end{aligned}
$$

---

**Generated variant — observed workload; observed bank**

## log_reciprocal_exp — easy (observed)

If $g(u)=⟨\log{\left(u \right)},\,0,\,\frac{1}{u}⟩$ and $u(t)=e^{2 t}$, then $(g∘u)^{′}(t)=$

- $⟨2,\,0,\,- 2 e^{2 t}⟩$
- $⟨2,\,0,\,2 e^{2 t}⟩$
- $⟨2,\,0,\,- 2 e^{- 2 t}⟩$ **correct**
- $⟨e^{- 2 t},\,0,\,- e^{- 4 t}⟩$
- $⟨e^{- 2 t},\,0,\,e^{- 4 t}⟩$

By the chain rule, we have 

$$
(g∘u)^{′}(t)=g′(u(t))u′(t)
$$

Now, let's find the derivatives of each function:

$$
\begin{aligned}g^{′}(u) & =⟨\frac{\text{d}}{\text{d}u}\left(\log{\left(u \right)}\right),\,\frac{\text{d}}{\text{d}u}\left(0\right),\,\frac{\text{d}}{\text{d}u}\left(\frac{1}{u}\right)⟩ \\  & =⟨\frac{1}{u},\,0,\,- \frac{1}{u^{2}}⟩ \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(e^{2 t}\right)=2 e^{2 t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(g∘u)^{′}(t) & =g′(u(t))u′(t) \\  & =⟨\frac{1}{u(t)},\,0,\,- \frac{1}{u(t)^{2}}⟩\cdot \left(u^{′}(t)\right) \\  & =⟨e^{- 2 t},\,0,\,- e^{- 4 t}⟩\cdot \left(2 e^{2 t}\right) \\  & =⟨e^{- 2 t} 2 e^{2 t},\,0 \cdot 2 e^{2 t},\,- e^{- 4 t} 2 e^{2 t}⟩ \\  & =⟨2,\,0,\,- 2 e^{- 2 t}⟩\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## two_exp_power — easy (authored)

If $f(u)=e^{u + 1}\,i+e^{3 u}\,j+e^{-1}\,k$ and $u(t)=4 t^{2}$ then $(f∘u)^{′}(t)=$

- $8 t e^{4 t^{2} + 1}\,i+24 t e^{12 t^{2}}\,j$ **correct**
- $e^{u + 1}\,i+3 e^{3 u}\,j$
- $e^{4 t^{2} + 1}\,i+3 e^{12 t^{2}}\,j$
- $64 t^{2} e^{4 t^{2} + 1}\,i+192 t^{2} e^{12 t^{2}}\,j$
- $8 t e^{4 t^{2} + 1}\,i+3 e^{12 t^{2}}\,j$

By the chain rule, we have

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function:

$$
\begin{aligned}f^{′}(u) & =\frac{\text{d}}{\text{d}u}\left(e^{u + 1}\right)\,i+\frac{\text{d}}{\text{d}u}\left(e^{3 u}\right)\,j+\frac{\text{d}}{\text{d}u}\left(e^{-1}\right)\,k \\  & =e^{u + 1}\,i+3 e^{3 u}\,j+0\,k \\  & =e^{u + 1}\,i+3 e^{3 u}\,j \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(4 t^{2}\right)=8 t\end{aligned}
$$

 
Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\ (f∘u)^{′}(t) & =\left(e^{4 t^{2} + 1}\,i+3 e^{12 t^{2}}\,j\right)\cdot \left(8 t\right) \\  & =8 t e^{4 t^{2} + 1}\,i+24 t e^{12 t^{2}}\,j\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## two_exp_power — easy (authored)

If $f(u)=e^{u + 2}\,i+e^{3 u}\,j+e^{-1}\,k$ and $u(t)=t^{2}$ then $(f∘u)^{′}(t)=$

- $4 t^{2} e^{t^{2} + 2}\,i+12 t^{2} e^{3 t^{2}}\,j$
- $e^{u + 2}\,i+3 e^{3 u}\,j$
- $e^{t^{2} + 2}\,i+3 e^{3 t^{2}}\,j$
- $2 t e^{t^{2} + 2}\,i+6 t e^{3 t^{2}}\,j$ **correct**
- $2 t e^{t^{2} + 2}\,i+3 e^{3 t^{2}}\,j$

By the chain rule, we have

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function:

$$
\begin{aligned}f^{′}(u) & =\frac{\text{d}}{\text{d}u}\left(e^{u + 2}\right)\,i+\frac{\text{d}}{\text{d}u}\left(e^{3 u}\right)\,j+\frac{\text{d}}{\text{d}u}\left(e^{-1}\right)\,k \\  & =e^{u + 2}\,i+3 e^{3 u}\,j+0\,k \\  & =e^{u + 2}\,i+3 e^{3 u}\,j \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(t^{2}\right)=2 t\end{aligned}
$$

 
Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\ (f∘u)^{′}(t) & =\left(e^{t^{2} + 2}\,i+3 e^{3 t^{2}}\,j\right)\cdot \left(2 t\right) \\  & =2 t e^{t^{2} + 2}\,i+6 t e^{3 t^{2}}\,j\end{aligned}
$$

---

**Generated variant — observed workload; observed bank**

## two_exp_power — easy (observed)

If $f(u)=e^{u + 2}\,i+e^{4 u}\,j+e^{-1}\,k$ and $u(t)=2 t^{2}$ then $(f∘u)^{′}(t)=$

- $t e^{2 t + 2}\,i+4 t e^{8 t}\,j$
- $4 t e^{t + 2}\,i+10 t e^{4 t}\,j$
- $4 t e^{2 t^{2} + 2}\,i+16 t e^{8 t^{2}}\,j$ **correct**
- $t e^{t + 2}\,i+4 t e^{4 t}\,j$
- $4 e^{2 t^{2} + 2}\,i-16 e^{8 t^{2}}\,j$

By the chain rule, we have

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function:

$$
\begin{aligned}f^{′}(u) & =\frac{\text{d}}{\text{d}u}\left(e^{u + 2}\right)\,i+\frac{\text{d}}{\text{d}u}\left(e^{4 u}\right)\,j+\frac{\text{d}}{\text{d}u}\left(e^{-1}\right)\,k \\  & =e^{u + 2}\,i+4 e^{4 u}\,j+0\,k \\  & =e^{u + 2}\,i+4 e^{4 u}\,j \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(2 t^{2}\right)=4 t\end{aligned}
$$

 
Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\ (f∘u)^{′}(t) & =\left(e^{2 t^{2} + 2}\,i+4 e^{8 t^{2}}\,j\right)\cdot \left(4 t\right) \\  & =4 t e^{2 t^{2} + 2}\,i+16 t e^{8 t^{2}}\,j\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## sin_cos_exp_affine — easy (authored)

If $f(u)=[\begin{aligned}\sin{\left(u \right)} \\ \cos{\left(u \right)} \\ e^{u}\end{aligned}]$ and $u(t)=4 t + 2$ then $(f∘u)^{′}(t)=$

- $[\begin{aligned}4 \cos{\left(4 t + 2 \right)} \\ - 4 \sin{\left(4 t + 2 \right)} \\ 4 e^{4 t + 2}\end{aligned}]$ **correct**
- $[\begin{aligned}\cos{\left(u \right)} \\ - \sin{\left(u \right)} \\ e^{u}\end{aligned}]$
- $[\begin{aligned}\cos{\left(4 t + 2 \right)} \\ - \sin{\left(4 t + 2 \right)} \\ e^{4 t + 2}\end{aligned}]$
- $[\begin{aligned}16 \cos{\left(4 t + 2 \right)} \\ - 16 \sin{\left(4 t + 2 \right)} \\ 16 e^{4 t + 2}\end{aligned}]$
- $[\begin{aligned}4 \cos{\left(4 t + 2 \right)} \\ - \sin{\left(4 t + 2 \right)} \\ e^{4 t + 2}\end{aligned}]$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(\sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(\cos{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(e^{u}\right)\end{aligned}]=[\begin{aligned}\cos{\left(u \right)} \\ - \sin{\left(u \right)} \\ e^{u}\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(4 t + 2\right)=4\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}\cos{\left(u(t) \right)} \\ - \sin{\left(u(t) \right)} \\ e^{u(t)}\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}\cos{\left(4 t + 2 \right)} \\ - \sin{\left(4 t + 2 \right)} \\ e^{4 t + 2}\end{aligned}]\cdot \left(4\right) \\  & =[\begin{aligned}4 \cos{\left(4 t + 2 \right)} \\ - 4 \sin{\left(4 t + 2 \right)} \\ 4 e^{4 t + 2}\end{aligned}]\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## sin_cos_exp_affine — easy (authored)

If $f(u)=[\begin{aligned}\sin{\left(u \right)} \\ \cos{\left(u \right)} \\ e^{u}\end{aligned}]$ and $u(t)=- 4 t - 4$ then $(f∘u)^{′}(t)=$

- $[\begin{aligned}16 \cos{\left(4 t + 4 \right)} \\ 16 \sin{\left(4 t + 4 \right)} \\ 16 e^{- 4 t - 4}\end{aligned}]$
- $[\begin{aligned}\cos{\left(u \right)} \\ - \sin{\left(u \right)} \\ e^{u}\end{aligned}]$
- $[\begin{aligned}\cos{\left(4 t + 4 \right)} \\ \sin{\left(4 t + 4 \right)} \\ e^{- 4 t - 4}\end{aligned}]$
- $[\begin{aligned}- 4 \cos{\left(4 t + 4 \right)} \\ - 4 \sin{\left(4 t + 4 \right)} \\ - 4 e^{- 4 t - 4}\end{aligned}]$ **correct**
- $[\begin{aligned}- 4 \cos{\left(4 t + 4 \right)} \\ \sin{\left(4 t + 4 \right)} \\ e^{- 4 t - 4}\end{aligned}]$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(\sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(\cos{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(e^{u}\right)\end{aligned}]=[\begin{aligned}\cos{\left(u \right)} \\ - \sin{\left(u \right)} \\ e^{u}\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(- 4 t - 4\right)=-4\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}\cos{\left(u(t) \right)} \\ - \sin{\left(u(t) \right)} \\ e^{u(t)}\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}\cos{\left(4 t + 4 \right)} \\ \sin{\left(4 t + 4 \right)} \\ e^{- 4 t - 4}\end{aligned}]\cdot \left(-4\right) \\  & =[\begin{aligned}- 4 \cos{\left(4 t + 4 \right)} \\ - 4 \sin{\left(4 t + 4 \right)} \\ - 4 e^{- 4 t - 4}\end{aligned}]\end{aligned}
$$

---

**Generated variant — observed workload; observed bank**

## sin_cos_exp_affine — easy (observed)

If $f(u)=[\begin{aligned}\sin{\left(u \right)} \\ \cos{\left(u \right)} \\ e^{u}\end{aligned}]$ and $u(t)=2 t + 4$ then $(f∘u)^{′}(t)=$

- $[\begin{aligned}2 \sin{\left(2 t + 4 \right)} \\ - 2 \cos{\left(2 t + 4 \right)} \\ 2 e^{2 t + 4}\end{aligned}]$
- $[\begin{aligned}- 4 \sin{\left(2 t + 4 \right)} \\ 4 \cos{\left(2 t + 4 \right)} \\ \left(2 t + 4\right) e^{t}\end{aligned}]$
- $[\begin{aligned}2 \cos{\left(2 t + 4 \right)} \\ - 2 \sin{\left(2 t + 4 \right)} \\ 2 e^{2 t + 4}\end{aligned}]$ **correct**
- $[\begin{aligned}- \sin{\left(2 t + 4 \right)} \\ \cos{\left(2 t + 4 \right)} \\ \left(2 t + 4\right) e^{t}\end{aligned}]$
- $[\begin{aligned}\cos{\left(2 t + 4 \right)} \\ - \sin{\left(2 t + 4 \right)} \\ e^{2 t + 4}\end{aligned}]$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(\sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(\cos{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(e^{u}\right)\end{aligned}]=[\begin{aligned}\cos{\left(u \right)} \\ - \sin{\left(u \right)} \\ e^{u}\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(2 t + 4\right)=2\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}\cos{\left(u(t) \right)} \\ - \sin{\left(u(t) \right)} \\ e^{u(t)}\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}\cos{\left(2 t + 4 \right)} \\ - \sin{\left(2 t + 4 \right)} \\ e^{2 t + 4}\end{aligned}]\cdot \left(2\right) \\  & =[\begin{aligned}2 \cos{\left(2 t + 4 \right)} \\ - 2 \sin{\left(2 t + 4 \right)} \\ 2 e^{2 t + 4}\end{aligned}]\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## log_power_root_exp — easy (authored)

If $f(u)=\log{\left(u \right)}\,i+u^{2}\,j+\sqrt{u}\,k$ and $u(t)=e^{4 t}$ then $(f∘u)^{′}(t)=$

- $4\,i+8 e^{8 t}\,j+2 e^{2 t}\,k$ **correct**
- $\frac{1}{u}\,i+2 u\,j+\frac{1}{2 \sqrt{u}}\,k$
- $e^{- 4 t}\,i+2 e^{4 t}\,j+\frac{e^{- 2 t}}{2}\,k$
- $16 e^{4 t}\,i+32 e^{12 t}\,j+8 e^{6 t}\,k$
- $4\,i+2 e^{4 t}\,j+\frac{e^{- 2 t}}{2}\,k$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\frac{\text{d}}{\text{d}u}\left(\log{\left(u \right)}\right)\,i+\frac{\text{d}}{\text{d}u}\left(u^{2}\right)\,j+\frac{\text{d}}{\text{d}u}\left(\sqrt{u}\right)\,k \\  & =\frac{1}{u}\,i+2 u\,j+\frac{1}{2 \sqrt{u}}\,k \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(e^{4 t}\right)=4 e^{4 t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\left(\frac{1}{u(t)}\,i+2 u(t)\,j+\frac{1}{2 \sqrt{u(t)}}\,k\right)\cdot \left(u^{′}(t)\right) \\  & =\left(e^{- 4 t}\,i+2 e^{4 t}\,j+\frac{e^{- 2 t}}{2}\,k\right)\cdot \left(4 e^{4 t}\right) \\  & =\left(e^{- 4 t}\,i+2 e^{4 t}\,j+\frac{e^{- 2 t}}{2}\,k\right)\cdot \left(4 e^{4 t}\right) \\  & =4\,i+8 e^{8 t}\,j+2 e^{2 t}\,k\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## log_power_root_exp — easy (authored)

If $f(u)=\log{\left(u \right)}\,i+u^{2}\,j+\sqrt{u}\,k$ and $u(t)=e^{t}$ then $(f∘u)^{′}(t)=$

- $e^{t}\,i+2 e^{3 t}\,j+\frac{e^{\frac{3 t}{2}}}{2}\,k$
- $\frac{1}{u}\,i+2 u\,j+\frac{1}{2 \sqrt{u}}\,k$
- $e^{- t}\,i+2 e^{t}\,j+\frac{e^{- \frac{t}{2}}}{2}\,k$
- $\,i+2 e^{2 t}\,j+\frac{e^{\frac{t}{2}}}{2}\,k$ **correct**
- $\,i+2 e^{t}\,j+\frac{e^{- \frac{t}{2}}}{2}\,k$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\frac{\text{d}}{\text{d}u}\left(\log{\left(u \right)}\right)\,i+\frac{\text{d}}{\text{d}u}\left(u^{2}\right)\,j+\frac{\text{d}}{\text{d}u}\left(\sqrt{u}\right)\,k \\  & =\frac{1}{u}\,i+2 u\,j+\frac{1}{2 \sqrt{u}}\,k \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(e^{t}\right)=e^{t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\left(\frac{1}{u(t)}\,i+2 u(t)\,j+\frac{1}{2 \sqrt{u(t)}}\,k\right)\cdot \left(u^{′}(t)\right) \\  & =\left(e^{- t}\,i+2 e^{t}\,j+\frac{e^{- \frac{t}{2}}}{2}\,k\right)\cdot \left(e^{t}\right) \\  & =\left(e^{- t}\,i+2 e^{t}\,j+\frac{e^{- \frac{t}{2}}}{2}\,k\right)\cdot \left(e^{t}\right) \\  & =\,i+2 e^{2 t}\,j+\frac{e^{\frac{t}{2}}}{2}\,k\end{aligned}
$$

---

**Generated variant — observed workload; observed bank**

## log_power_root_exp — easy (observed)

If $f(u)=\log{\left(u \right)}\,i+u^{2}\,j+\sqrt{u}\,k$ and $u(t)=e^{2 t}$ then $(f∘u)^{′}(t)=$

- $-2\,i+8 e^{4 t}\,j+4 e^{3 t}\,k$
- $2\,i+4 e^{4 t}\,j+e^{t}\,k$ **correct**
- $-2\,i+4 e^{2 t}\,j+\frac{e^{t}}{2}\,k$
- $2\,i+2 e^{4 t}\,j+4 e^{t}\,k$
- $2\,i+4 e^{- 4 t}\,j+e^{- 2 t}\,k$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =\frac{\text{d}}{\text{d}u}\left(\log{\left(u \right)}\right)\,i+\frac{\text{d}}{\text{d}u}\left(u^{2}\right)\,j+\frac{\text{d}}{\text{d}u}\left(\sqrt{u}\right)\,k \\  & =\frac{1}{u}\,i+2 u\,j+\frac{1}{2 \sqrt{u}}\,k \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(e^{2 t}\right)=2 e^{2 t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =\left(\frac{1}{u(t)}\,i+2 u(t)\,j+\frac{1}{2 \sqrt{u(t)}}\,k\right)\cdot \left(u^{′}(t)\right) \\  & =\left(e^{- 2 t}\,i+2 e^{2 t}\,j+\frac{e^{- t}}{2}\,k\right)\cdot \left(2 e^{2 t}\right) \\  & =\left(e^{- 2 t}\,i+2 e^{2 t}\,j+\frac{e^{- t}}{2}\,k\right)\cdot \left(2 e^{2 t}\right) \\  & =2\,i+4 e^{4 t}\,j+e^{t}\,k\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## reciprocal_log_reciprocal — easy (authored)

If $g(u)=⟨\frac{1}{u},\,\log{\left(u + 3 \right)},\,3⟩$ and $u(t)=\frac{4}{t}$, then $(g∘u)^{′}(t)=$

- $⟨\frac{1}{4},\,- \frac{4}{t \left(3 t + 4\right)},\,0⟩$ **correct**
- $⟨- \frac{1}{u^{2}},\,\frac{1}{u + 3},\,0⟩$
- $⟨- \frac{t^{2}}{16},\,\frac{1}{3 + \frac{4}{t}},\,0⟩$
- $⟨- \frac{1}{t^{2}},\,\frac{16}{t^{4} \left(3 + \frac{4}{t}\right)},\,0⟩$
- $⟨\frac{1}{4},\,\frac{1}{3 + \frac{4}{t}},\,0⟩$

By the chain rule, we have 

$$
(g∘u)^{′}(t)=g′(u(t))u′(t)
$$

Now, let's find the derivatives of each function:

$$
\begin{aligned}g^{′}(u) & =⟨\frac{\text{d}}{\text{d}u}\left(\frac{1}{u}\right),\,\frac{\text{d}}{\text{d}u}\left(\log{\left(u + 3 \right)}\right),\,\frac{\text{d}}{\text{d}u}\left(3\right)⟩ \\  & =⟨- \frac{1}{u^{2}},\,\frac{1}{u + 3},\,0⟩ \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(\frac{4}{t}\right)=- \frac{4}{t^{2}}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(g∘u)^{′}(t) & =g′(u(t))u′(t) \\  & =⟨- \frac{1}{u(t)^{2}},\,\frac{1}{u(t) + 3},\,0⟩\cdot \left(u^{′}(t)\right) \\  & =⟨- \frac{t^{2}}{16},\,\frac{1}{3 + \frac{4}{t}},\,0⟩\cdot \left(- \frac{4}{t^{2}}\right) \\  & =⟨\frac{1}{4},\,- \frac{4}{t \left(3 t + 4\right)},\,0⟩\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## reciprocal_log_reciprocal — easy (authored)

If $g(u)=⟨\frac{1}{u},\,\log{\left(u + 3 \right)},\,3⟩$ and $u(t)=\frac{1}{t}$, then $(g∘u)^{′}(t)=$

- $⟨- \frac{1}{t^{2}},\,\frac{1}{t^{4} \left(3 + \frac{1}{t}\right)},\,0⟩$
- $⟨- \frac{1}{u^{2}},\,\frac{1}{u + 3},\,0⟩$
- $⟨- t^{2},\,\frac{1}{3 + \frac{1}{t}},\,0⟩$
- $⟨1,\,- \frac{1}{t \left(3 t + 1\right)},\,0⟩$ **correct**
- $⟨1,\,\frac{1}{3 + \frac{1}{t}},\,0⟩$

By the chain rule, we have 

$$
(g∘u)^{′}(t)=g′(u(t))u′(t)
$$

Now, let's find the derivatives of each function:

$$
\begin{aligned}g^{′}(u) & =⟨\frac{\text{d}}{\text{d}u}\left(\frac{1}{u}\right),\,\frac{\text{d}}{\text{d}u}\left(\log{\left(u + 3 \right)}\right),\,\frac{\text{d}}{\text{d}u}\left(3\right)⟩ \\  & =⟨- \frac{1}{u^{2}},\,\frac{1}{u + 3},\,0⟩ \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(\frac{1}{t}\right)=- \frac{1}{t^{2}}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(g∘u)^{′}(t) & =g′(u(t))u′(t) \\  & =⟨- \frac{1}{u(t)^{2}},\,\frac{1}{u(t) + 3},\,0⟩\cdot \left(u^{′}(t)\right) \\  & =⟨- t^{2},\,\frac{1}{3 + \frac{1}{t}},\,0⟩\cdot \left(- \frac{1}{t^{2}}\right) \\  & =⟨1,\,- \frac{1}{t \left(3 t + 1\right)},\,0⟩\end{aligned}
$$

---

**Generated variant — observed workload; observed bank**

## reciprocal_log_reciprocal — easy (observed)

If $g(u)=⟨\frac{1}{u},\,\log{\left(u + 3 \right)},\,4⟩$ and $u(t)=\frac{2}{t}$, then $(g∘u)^{′}(t)=$

- $⟨- \frac{1}{2},\,- \frac{2 t}{t^{2} + 6},\,0⟩$
- $⟨\frac{2}{t},\,- \frac{2}{t \left(3 t + 2\right)},\,0⟩$
- $⟨\frac{1}{2},\,- \frac{2}{t \left(3 t + 2\right)},\,0⟩$ **correct**
- $⟨- \frac{2}{t^{2}},\,- \frac{t^{2}}{t^{2} + 3},\,0⟩$
- $⟨\frac{1}{2},\,- \frac{2 t}{t^{2} + 3},\,0⟩$

By the chain rule, we have 

$$
(g∘u)^{′}(t)=g′(u(t))u′(t)
$$

Now, let's find the derivatives of each function:

$$
\begin{aligned}g^{′}(u) & =⟨\frac{\text{d}}{\text{d}u}\left(\frac{1}{u}\right),\,\frac{\text{d}}{\text{d}u}\left(\log{\left(u + 3 \right)}\right),\,\frac{\text{d}}{\text{d}u}\left(4\right)⟩ \\  & =⟨- \frac{1}{u^{2}},\,\frac{1}{u + 3},\,0⟩ \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(\frac{2}{t}\right)=- \frac{2}{t^{2}}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(g∘u)^{′}(t) & =g′(u(t))u′(t) \\  & =⟨- \frac{1}{u(t)^{2}},\,\frac{1}{u(t) + 3},\,0⟩\cdot \left(u^{′}(t)\right) \\  & =⟨- \frac{t^{2}}{4},\,\frac{1}{3 + \frac{2}{t}},\,0⟩\cdot \left(- \frac{2}{t^{2}}\right) \\  & =⟨\frac{1}{2},\,- \frac{2}{t \left(3 t + 2\right)},\,0⟩\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## cos_cube_log_exp — easy (authored)

If $f(u)=[\begin{aligned}\cos{\left(u \right)} \\ u^{3} \\ \log{\left(u \right)}\end{aligned}]$ and $u(t)=e^{4 t}$, then $(f∘u)^{′}(t)=$

- $[\begin{aligned}- 4 e^{4 t} \sin{\left(e^{4 t} \right)} \\ 12 e^{12 t} \\ 4\end{aligned}]$ **correct**
- $[\begin{aligned}- \sin{\left(u \right)} \\ 3 u^{2} \\ \frac{1}{u}\end{aligned}]$
- $[\begin{aligned}- \sin{\left(e^{4 t} \right)} \\ 3 e^{8 t} \\ e^{- 4 t}\end{aligned}]$
- $[\begin{aligned}- 16 e^{8 t} \sin{\left(e^{4 t} \right)} \\ 48 e^{16 t} \\ 16 e^{4 t}\end{aligned}]$
- $[\begin{aligned}- 4 e^{4 t} \sin{\left(e^{4 t} \right)} \\ 3 e^{8 t} \\ e^{- 4 t}\end{aligned}]$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(\cos{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(u^{3}\right) \\ \frac{\text{d}}{\text{d}u}\left(\log{\left(u \right)}\right)\end{aligned}]=[\begin{aligned}- \sin{\left(u \right)} \\ 3 u^{2} \\ \frac{1}{u}\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(e^{4 t}\right)=4 e^{4 t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}- \sin{\left(u(t) \right)} \\ 3 u(t)^{2} \\ \frac{1}{u(t)}\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}- \sin{\left(e^{4 t} \right)} \\ 3 e^{8 t} \\ e^{- 4 t}\end{aligned}]\cdot \left(4 e^{4 t}\right) \\  & =[\begin{aligned}- \sin{\left(e^{4 t} \right)} \\ 3 e^{8 t} \\ e^{- 4 t}\end{aligned}]\cdot \left(4 e^{4 t}\right) \\  & =[\begin{aligned}- 4 e^{4 t} \sin{\left(e^{4 t} \right)} \\ 12 e^{12 t} \\ 4\end{aligned}]\end{aligned}
$$

---

**Generated variant — observed workload; authored bank**

## cos_cube_log_exp — easy (authored)

If $f(u)=[\begin{aligned}\cos{\left(u \right)} \\ u^{3} \\ \log{\left(u \right)}\end{aligned}]$ and $u(t)=e^{t}$, then $(f∘u)^{′}(t)=$

- $[\begin{aligned}- e^{2 t} \sin{\left(e^{t} \right)} \\ 3 e^{4 t} \\ e^{t}\end{aligned}]$
- $[\begin{aligned}- \sin{\left(u \right)} \\ 3 u^{2} \\ \frac{1}{u}\end{aligned}]$
- $[\begin{aligned}- \sin{\left(e^{t} \right)} \\ 3 e^{2 t} \\ e^{- t}\end{aligned}]$
- $[\begin{aligned}- e^{t} \sin{\left(e^{t} \right)} \\ 3 e^{3 t} \\ 1\end{aligned}]$ **correct**
- $[\begin{aligned}- e^{t} \sin{\left(e^{t} \right)} \\ 3 e^{2 t} \\ e^{- t}\end{aligned}]$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(\cos{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(u^{3}\right) \\ \frac{\text{d}}{\text{d}u}\left(\log{\left(u \right)}\right)\end{aligned}]=[\begin{aligned}- \sin{\left(u \right)} \\ 3 u^{2} \\ \frac{1}{u}\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(e^{t}\right)=e^{t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}- \sin{\left(u(t) \right)} \\ 3 u(t)^{2} \\ \frac{1}{u(t)}\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}- \sin{\left(e^{t} \right)} \\ 3 e^{2 t} \\ e^{- t}\end{aligned}]\cdot \left(e^{t}\right) \\  & =[\begin{aligned}- \sin{\left(e^{t} \right)} \\ 3 e^{2 t} \\ e^{- t}\end{aligned}]\cdot \left(e^{t}\right) \\  & =[\begin{aligned}- e^{t} \sin{\left(e^{t} \right)} \\ 3 e^{3 t} \\ 1\end{aligned}]\end{aligned}
$$

---

**Generated variant — observed workload; observed bank**

## cos_cube_log_exp — easy (observed)

If $f(u)=[\begin{aligned}\cos{\left(u \right)} \\ u^{3} \\ \log{\left(u \right)}\end{aligned}]$ and $u(t)=e^{2 t}$, then $(f∘u)^{′}(t)=$

- $[\begin{aligned}- 2 e^{2 t} \cos{\left(e^{2 t} \right)} \\ 3 e^{2 t} \\ 1\end{aligned}]$
- $[\begin{aligned}\sin{\left(e^{4 t} \right)} \\ e^{6 t} \\ e^{- 4 t}\end{aligned}]$
- $[\begin{aligned}2 e^{2 t} \cos{\left(e^{2 t} \right)} \\ 6 e^{6 t} \\ e^{4 t}\end{aligned}]$
- $[\begin{aligned}- \sin{\left(e^{4 t} \right)} \\ 3 e^{4 t} \\ 1\end{aligned}]$
- $[\begin{aligned}- 2 e^{2 t} \sin{\left(e^{2 t} \right)} \\ 6 e^{6 t} \\ 2\end{aligned}]$ **correct**

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(\cos{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(u^{3}\right) \\ \frac{\text{d}}{\text{d}u}\left(\log{\left(u \right)}\right)\end{aligned}]=[\begin{aligned}- \sin{\left(u \right)} \\ 3 u^{2} \\ \frac{1}{u}\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(e^{2 t}\right)=2 e^{2 t}\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}- \sin{\left(u(t) \right)} \\ 3 u(t)^{2} \\ \frac{1}{u(t)}\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}- \sin{\left(e^{2 t} \right)} \\ 3 e^{4 t} \\ e^{- 2 t}\end{aligned}]\cdot \left(2 e^{2 t}\right) \\  & =[\begin{aligned}- \sin{\left(e^{2 t} \right)} \\ 3 e^{4 t} \\ e^{- 2 t}\end{aligned}]\cdot \left(2 e^{2 t}\right) \\  & =[\begin{aligned}- 2 e^{2 t} \sin{\left(e^{2 t} \right)} \\ 6 e^{6 t} \\ 2\end{aligned}]\end{aligned}
$$

---

**Generated variant — authored level**

## mixed_quadratic_inner — moderate (authored)

If $f(u)=[\begin{aligned}\sin{\left(u \right)} \\ - e^{u} \\ u^{2}\end{aligned}]$ and $u(t)=2 t^{2} + t$, then $(f∘u)^{′}(t)=$

- $[\begin{aligned}\left(4 t + 1\right) \cos{\left(t \left(2 t + 1\right) \right)} \\ \left(- 4 t - 1\right) e^{t \left(2 t + 1\right)} \\ 2 t \left(2 t + 1\right) \left(4 t + 1\right)\end{aligned}]$ **correct**
- $[\begin{aligned}\cos{\left(u \right)} \\ - e^{u} \\ 2 u\end{aligned}]$
- $[\begin{aligned}\cos{\left(2 t^{2} + t \right)} \\ - e^{2 t^{2} + t} \\ 4 t^{2} + 2 t\end{aligned}]$
- $[\begin{aligned}\left(4 t + 1\right)^{2} \cos{\left(2 t^{2} + t \right)} \\ - \left(4 t + 1\right)^{2} e^{2 t^{2} + t} \\ \left(4 t + 1\right)^{2} \left(4 t^{2} + 2 t\right)\end{aligned}]$
- $[\begin{aligned}\left(4 t + 1\right) \cos{\left(t \left(2 t + 1\right) \right)} \\ - e^{2 t^{2} + t} \\ 4 t^{2} + 2 t\end{aligned}]$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(\sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(- e^{u}\right) \\ \frac{\text{d}}{\text{d}u}\left(u^{2}\right)\end{aligned}]=[\begin{aligned}\cos{\left(u \right)} \\ - e^{u} \\ 2 u\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(2 t^{2} + t\right)=4 t + 1\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}\cos{\left(u(t) \right)} \\ - e^{u(t)} \\ 2 u(t)\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}\cos{\left(2 t^{2} + t \right)} \\ - e^{2 t^{2} + t} \\ 4 t^{2} + 2 t\end{aligned}]\cdot \left(4 t + 1\right) \\  & =[\begin{aligned}\left(4 t + 1\right) \cos{\left(t \left(2 t + 1\right) \right)} \\ \left(- 4 t - 1\right) e^{t \left(2 t + 1\right)} \\ 2 t \left(2 t + 1\right) \left(4 t + 1\right)\end{aligned}]\end{aligned}
$$

---

**Generated variant — authored level**

## mixed_quadratic_inner — moderate (authored)

If $f(u)=[\begin{aligned}\sin{\left(u \right)} \\ - 2 e^{u} \\ u^{2}\end{aligned}]$ and $u(t)=- 2 t^{2} + t + 2$, then $(f∘u)^{′}(t)=$

- $[\begin{aligned}\left(1 - 4 t\right)^{2} \cos{\left(- 2 t^{2} + t + 2 \right)} \\ - 2 \left(1 - 4 t\right)^{2} e^{- 2 t^{2} + t + 2} \\ \left(1 - 4 t\right)^{2} \left(- 4 t^{2} + 2 t + 4\right)\end{aligned}]$
- $[\begin{aligned}\cos{\left(u \right)} \\ - 2 e^{u} \\ 2 u\end{aligned}]$
- $[\begin{aligned}\cos{\left(- 2 t^{2} + t + 2 \right)} \\ - 2 e^{- 2 t^{2} + t + 2} \\ - 4 t^{2} + 2 t + 4\end{aligned}]$
- $[\begin{aligned}\left(1 - 4 t\right) \cos{\left(- 2 t^{2} + t + 2 \right)} \\ \left(8 t - 2\right) e^{- 2 t^{2} + t + 2} \\ 16 t^{3} - 12 t^{2} - 14 t + 4\end{aligned}]$ **correct**
- $[\begin{aligned}\left(1 - 4 t\right) \cos{\left(- 2 t^{2} + t + 2 \right)} \\ - 2 e^{- 2 t^{2} + t + 2} \\ - 4 t^{2} + 2 t + 4\end{aligned}]$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(\sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(- 2 e^{u}\right) \\ \frac{\text{d}}{\text{d}u}\left(u^{2}\right)\end{aligned}]=[\begin{aligned}\cos{\left(u \right)} \\ - 2 e^{u} \\ 2 u\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(- 2 t^{2} + t + 2\right)=1 - 4 t\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}\cos{\left(u(t) \right)} \\ - 2 e^{u(t)} \\ 2 u(t)\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}\cos{\left(- 2 t^{2} + t + 2 \right)} \\ - 2 e^{- 2 t^{2} + t + 2} \\ - 4 t^{2} + 2 t + 4\end{aligned}]\cdot \left(1 - 4 t\right) \\  & =[\begin{aligned}\left(1 - 4 t\right) \cos{\left(- 2 t^{2} + t + 2 \right)} \\ \left(8 t - 2\right) e^{- 2 t^{2} + t + 2} \\ 16 t^{3} - 12 t^{2} - 14 t + 4\end{aligned}]\end{aligned}
$$

---

**Generated variant — authored level**

## mixed_cubic_inner — hard (authored)

If $f(u)=[\begin{aligned}- \sin{\left(u \right)} \\ - e^{u} \\ - 2 u^{2}\end{aligned}]$ and $u(t)=2 t^{3} + t + 1$, then $(f∘u)^{′}(t)=$ Write the polynomial component in expanded form.

- $[\begin{aligned}\left(- 6 t^{2} - 1\right) \cos{\left(2 t^{3} + t + 1 \right)} \\ \left(- 6 t^{2} - 1\right) e^{2 t^{3} + t + 1} \\ - 48 t^{5} - 32 t^{3} - 24 t^{2} - 4 t - 4\end{aligned}]$ **correct**
- $[\begin{aligned}- \cos{\left(u \right)} \\ - e^{u} \\ - 4 u\end{aligned}]$
- $[\begin{aligned}- \cos{\left(2 t^{3} + t + 1 \right)} \\ - e^{2 t^{3} + t + 1} \\ - 8 t^{3} - 4 t - 4\end{aligned}]$
- $[\begin{aligned}- \left(6 t^{2} + 1\right)^{2} \cos{\left(2 t^{3} + t + 1 \right)} \\ - \left(6 t^{2} + 1\right)^{2} e^{2 t^{3} + t + 1} \\ - 288 t^{7} - 240 t^{5} - 144 t^{4} - 56 t^{3} - 48 t^{2} - 4 t - 4\end{aligned}]$
- $[\begin{aligned}\left(- 6 t^{2} - 1\right) \cos{\left(2 t^{3} + t + 1 \right)} \\ - e^{2 t^{3} + t + 1} \\ - 8 t^{3} - 4 t - 4\end{aligned}]$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(- \sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(- e^{u}\right) \\ \frac{\text{d}}{\text{d}u}\left(- 2 u^{2}\right)\end{aligned}]=[\begin{aligned}- \cos{\left(u \right)} \\ - e^{u} \\ - 4 u\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(2 t^{3} + t + 1\right)=6 t^{2} + 1\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}- \cos{\left(u(t) \right)} \\ - e^{u(t)} \\ - 4 u(t)\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}- \cos{\left(2 t^{3} + t + 1 \right)} \\ - e^{2 t^{3} + t + 1} \\ - 8 t^{3} - 4 t - 4\end{aligned}]\cdot \left(6 t^{2} + 1\right) \\  & =[\begin{aligned}\left(- 6 t^{2} - 1\right) \cos{\left(2 t^{3} + t + 1 \right)} \\ \left(- 6 t^{2} - 1\right) e^{2 t^{3} + t + 1} \\ - 48 t^{5} - 32 t^{3} - 24 t^{2} - 4 t - 4\end{aligned}]\end{aligned}
$$

---

**Generated variant — authored level**

## mixed_cubic_inner — hard (authored)

If $f(u)=[\begin{aligned}2 \sin{\left(u \right)} \\ 2 e^{u} \\ - u^{2}\end{aligned}]$ and $u(t)=2 t^{3} - 3 t + 1$, then $(f∘u)^{′}(t)=$ Write the polynomial component in expanded form.

- $[\begin{aligned}2 \left(6 t^{2} - 3\right)^{2} \cos{\left(2 t^{3} - 3 t + 1 \right)} \\ 2 \left(6 t^{2} - 3\right)^{2} e^{2 t^{3} - 3 t + 1} \\ - 144 t^{7} + 360 t^{5} - 72 t^{4} - 252 t^{3} + 72 t^{2} + 54 t - 18\end{aligned}]$
- $[\begin{aligned}2 \cos{\left(u \right)} \\ 2 e^{u} \\ - 2 u\end{aligned}]$
- $[\begin{aligned}2 \cos{\left(2 t^{3} - 3 t + 1 \right)} \\ 2 e^{2 t^{3} - 3 t + 1} \\ - 4 t^{3} + 6 t - 2\end{aligned}]$
- $[\begin{aligned}\left(12 t^{2} - 6\right) \cos{\left(2 t^{3} - 3 t + 1 \right)} \\ \left(12 t^{2} - 6\right) e^{2 t^{3} - 3 t + 1} \\ - 24 t^{5} + 48 t^{3} - 12 t^{2} - 18 t + 6\end{aligned}]$ **correct**
- $[\begin{aligned}\left(12 t^{2} - 6\right) \cos{\left(2 t^{3} - 3 t + 1 \right)} \\ 2 e^{2 t^{3} - 3 t + 1} \\ - 4 t^{3} + 6 t - 2\end{aligned}]$

Using the chain rule, we can write

$$
(f∘u)^{′}(t)=f′(u(t))u′(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}f^{′}(u) & =[\begin{aligned}\frac{\text{d}}{\text{d}u}\left(2 \sin{\left(u \right)}\right) \\ \frac{\text{d}}{\text{d}u}\left(2 e^{u}\right) \\ \frac{\text{d}}{\text{d}u}\left(- u^{2}\right)\end{aligned}]=[\begin{aligned}2 \cos{\left(u \right)} \\ 2 e^{u} \\ - 2 u\end{aligned}] \\ u^{′}(t) & =\frac{\text{d}}{\text{d}t}\left(2 t^{3} - 3 t + 1\right)=6 t^{2} - 3\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f∘u)^{′}(t) & =f′(u(t))u′(t) \\  & =[\begin{aligned}2 \cos{\left(u(t) \right)} \\ 2 e^{u(t)} \\ - 2 u(t)\end{aligned}]\cdot \left(u^{′}(t)\right) \\  & =[\begin{aligned}2 \cos{\left(2 t^{3} - 3 t + 1 \right)} \\ 2 e^{2 t^{3} - 3 t + 1} \\ - 4 t^{3} + 6 t - 2\end{aligned}]\cdot \left(6 t^{2} - 3\right) \\  & =[\begin{aligned}\left(12 t^{2} - 6\right) \cos{\left(2 t^{3} - 3 t + 1 \right)} \\ \left(12 t^{2} - 6\right) e^{2 t^{3} - 3 t + 1} \\ - 24 t^{5} + 48 t^{3} - 12 t^{2} - 18 t + 6\end{aligned}]\end{aligned}
$$
