# Template extraction

## Stage 1: describe every original

Database math, basis 1356, captured lineage preserved in source.json. Every vector below is the complete original expression, not component fragments.

### q-32286 (:question.difficulty/easy)

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}\operatorname{sin}⁡t \\ 2t-8 \\ {5}^{t}\end{aligned}]$ and $u(t)={t}^{2}.$

One radio selection field; five full vectors. Original bank:

- $[\begin{aligned}{t}^{2}\operatorname{cos}⁡t+2t\operatorname{sin}⁡t \\ 6{t}^{2}-16t \\ {5}^{t}+\operatorname{ln}⁡5\end{aligned}]$

- $[\begin{aligned}{t}^{2}\operatorname{cos}⁡t+2t\operatorname{sin}⁡t \\ {t}^{2}-t \\ {5}^{t}+{5}^{t}\cdot 2t\end{aligned}]$

- $[\begin{aligned}{t}^{2}\operatorname{sin}⁡t-4t\operatorname{cos}⁡t \\ 6{t}^{2}-16t \\ {5}^{t}{t}^{2}\operatorname{ln}⁡5+{5}^{t}\cdot 2t\end{aligned}]$

- $[\begin{aligned}{t}^{2}\operatorname{cos}⁡t+2t\operatorname{sin}⁡t \\ 12{t}^{2}+36 \\ {5}^{t}{t}^{2}\operatorname{ln}⁡5+{5}^{t}\cdot 2t\end{aligned}]$

- $[\begin{aligned}{t}^{2}\operatorname{cos}⁡t+2t\operatorname{sin}⁡t \\ 6{t}^{2}-16t \\ {5}^{t}{t}^{2}\operatorname{ln}⁡5+{5}^{t}\cdot 2t\end{aligned}]$

Original fixed solution sequence:

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

### q-32501 (unrated)

Find $(u(t)g(t))^{′}$ where $g(t) = ⟨3t^{2}, 3 - t, 3t⟩$ and $u(t) = t^{3}$.

One radio selection field; five full vectors. Original bank:

- $⟨15t^{4}, 9t^{2} - 4t^{3}, 12t^{3}⟩$

- $⟨6t^{4},-t^{3}, 3t^{3}⟩$

- $⟨6t,-1, 3⟩$

- $⟨3t^{2}, 3 - t, 3t⟩$

- $⟨5t^{4}, 3t^{2}, 4t^{3}⟩$

No original solution, difficulty, or correct reference. Widget evidence is retained separately.

### q-128473 (:question.difficulty/moderate)

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}\operatorname{sin}⁡t \\ \operatorname{tan}⁡t \\ 1\end{aligned}]$ and $u(t)=-\operatorname{cos}⁡t.$

One radio selection field; five full vectors. Original bank:

- $[\begin{aligned}1 \\ \operatorname{sin}⁡t\operatorname{tan}⁡t \\ \operatorname{sin}⁡t\end{aligned}]$

- $[\begin{aligned}\operatorname{cos}⁡t \\ \operatorname{sin}⁡t\operatorname{tan}⁡t+\operatorname{csc}⁡t \\ 1\end{aligned}]$

- $[\begin{aligned}1 \\ \operatorname{tan}⁡t+\operatorname{sec}⁡t \\ \operatorname{cos}⁡t\end{aligned}]$

- $[\begin{aligned}-1 \\ \operatorname{sin}⁡t\operatorname{tan}⁡t+\operatorname{sec}⁡t \\ \operatorname{cot}⁡t\end{aligned}]$

- $[\begin{aligned}-\operatorname{cos}⁡2t \\ \operatorname{sin}⁡t\operatorname{tan}⁡t-\operatorname{sec}⁡t \\ \operatorname{sin}⁡t\end{aligned}]$

Original fixed solution sequence:

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

### q-128477 (:question.difficulty/easy)

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨\sqrt{t},\,{t}^{2},\,t⟩$ and $u(t)=2\sqrt{t}.$

One radio selection field; five full vectors. Original bank:

- $⟨2,\,5t\sqrt{t},\,3\sqrt{t}⟩$

- $⟨{t}^{2},\,5\sqrt{t},\,3{t}^{2}\sqrt{t}⟩$

- $⟨\frac{1}{\sqrt{t}},\,5t\sqrt{t},\,3\sqrt{t}⟩$

- $⟨2t,\,\sqrt{t},\,\sqrt{t}⟩$

- $⟨1,\,2t\sqrt{t},\,\sqrt{t}⟩$

Original fixed solution sequence:

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

### q-128479 (:question.difficulty/easy)

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨t,\,1+t,\,{t}^{2}⟩$ and $u(t)=1-t.$

One radio selection field; five full vectors. Original bank:

- $⟨t-2,\,-t,\,t-2{t}^{2}⟩$

- $⟨1+t,\,2+t,\,t+3{t}^{2}⟩$

- $⟨1-2t,\,-1,\,2t-3{t}^{2}⟩$

- $⟨1-2t,\,-2t,\,2t-3{t}^{2}⟩$

- $⟨t,\,-2{t}^{2},\,2t-3{t}^{2}⟩$

Original fixed solution sequence:

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

### q-128481 (:question.difficulty/easy)

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨4\sqrt{t},\,{t}^{3},\,t+{t}^{2}⟩$ and $u(t)=2t.$

One radio selection field; five full vectors. Original bank:

- $⟨12\sqrt{t},\,8{t}^{3}+2t,\,4{t}^{2}+6{t}^{3}⟩$

- $⟨6\sqrt{t},\,{t}^{3},\,t+6{t}^{2}⟩$

- $⟨12\sqrt{t},\,8{t}^{3},\,4t+6{t}^{2}⟩$

- $⟨6\sqrt{t},\,2{t}^{2},\,10{t}^{2}⟩$

- $⟨5\sqrt{t},\,4{t}^{3},\,3t+6{t}^{2}⟩$

Original fixed solution sequence:

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

### q-128485 (:question.difficulty/easy)

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨2{e}^{-t},\,4\operatorname{ln}⁡t,\,2⟩$ and $u(t)=\frac{1}{2}{t}^{2}.$

One radio selection field; five full vectors. Original bank:

- $⟨{e}^{-t},\,2\operatorname{ln}⁡t,\,2t-1⟩$

- $⟨t{e}^{-t},\,1+2\operatorname{ln}⁡t,\,2t⟩$

- $⟨{t}^{2}{e}^{-t},\,{t}^{2}(1+2\operatorname{ln}⁡t),\,1⟩$

- $⟨t{e}^{-t}(2-t),\,2t(1+2\operatorname{ln}⁡t),\,2t⟩$

- $⟨2-t,\,2(1+2\operatorname{ln}⁡t),\,t⟩$

Original fixed solution sequence:

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

### q-70685 (:question.difficulty/easy)

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}t \\ {t}^{2} \\ {t}^{3}\end{aligned}]$ and $u(t)=\operatorname{ln}⁡t.$

One radio selection field; five full vectors. Original bank:

- $[\begin{aligned}1+\operatorname{ln}⁡t \\ t+2t\operatorname{ln}⁡t \\ {t}^{2}+3{t}^{2}\operatorname{ln}⁡t\end{aligned}]$

- $[\begin{aligned}\frac{1}{t}+\operatorname{ln}⁡t \\ \frac{2}{{t}^{2}}+2t\operatorname{ln}⁡t \\ \frac{3}{{t}^{3}}+3{t}^{2}\operatorname{ln}⁡t\end{aligned}]$

- $[\begin{aligned}\operatorname{ln}⁡t \\ 3t\operatorname{ln}⁡t \\ 4{t}^{2}\operatorname{ln}⁡t\end{aligned}]$

- $[\begin{aligned}t+\frac{1}{t} \\ {t}^{2}+2 \\ {t}^{3}+3t\end{aligned}]$

- $[\begin{aligned}t+\operatorname{ln}⁡t \\ {t}^{2}+2t\operatorname{ln}⁡t \\ {t}^{3}+3{t}^{2}\operatorname{ln}⁡t\end{aligned}]$

Original fixed solution sequence:

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

### q-71225 (:question.difficulty/easy)

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}4t-1 \\ 3t+2 \\ 5t+6\end{aligned}]$ and $u(t)=2t-3.$

One radio selection field; five full vectors. Original bank:

- $[\begin{aligned}10t-8 \\ 12t-4 \\ 6t-5\end{aligned}]$

- $[\begin{aligned}4t-7 \\ 3t-2 \\ 5t-1\end{aligned}]$

- $[\begin{aligned}16t-14 \\ 12t-5 \\ 20t-3\end{aligned}]$

- $[\begin{aligned}8t-14 \\ 6t-5 \\ 10t-3\end{aligned}]$

- $[\begin{aligned}12t-15 \\ 14t-7 \\ 18t-2\end{aligned}]$

Original fixed solution sequence:

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

### q-71230 (:question.difficulty/easy)

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}{e}^{t} \\ 8 \\ {e}^{-t}\end{aligned}]$ and $u(t)={t}^{2}.$

One radio selection field; five full vectors. Original bank:

- $[\begin{aligned}3t{e}^{t} \\ -8t \\ -3t{e}^{-t}\end{aligned}]$

- $[\begin{aligned}(2t+{t}^{2}){e}^{t} \\ 16t \\ (2t-{t}^{2}){e}^{-t}\end{aligned}]$

- $[\begin{aligned}3{t}^{3}{e}^{t} \\ -16t \\ -{t}^{3}{e}^{-t}\end{aligned}]$

- $[\begin{aligned}({t}^{2}+{t}^{3}){e}^{t} \\ 4t \\ {t}^{3}{e}^{-t}\end{aligned}]$

- $[\begin{aligned}(1-{t}^{2}){e}^{t} \\ 8t \\ (t+{t}^{2}){e}^{-t}\end{aligned}]$

Original fixed solution sequence:

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

### q-128488 (:question.difficulty/moderate)

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}{e}^{t} \\ {t}^{3} \\ {e}^{2t}\end{aligned}]$ and $u(t)={e}^{-t}.$

One radio selection field; five full vectors. Original bank:

- $[\begin{aligned}0 \\ {t}^{2}{e}^{-t}(3-t) \\ {e}^{t}\end{aligned}]$

- $[\begin{aligned}0 \\ 3-t \\ {t}^{2}{e}^{t}\end{aligned}]$

- $[\begin{aligned}-1 \\ {t}^{2}{e}^{-t}(1-t) \\ {e}^{t}\end{aligned}]$

- $[\begin{aligned}t \\ t{e}^{-t}(3-t) \\ t{e}^{t}\end{aligned}]$

- $[\begin{aligned}-1 \\ {t}^{2}{e}^{-t} \\ {e}^{t}\end{aligned}]$

Original fixed solution sequence:

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

### q-70688 (:question.difficulty/moderate)

Find $(u(t)f(t))^{′}$ where $f(t)=[\begin{aligned}2\operatorname{sin}⁡t \\ \operatorname{cos}⁡t \\ {e}^{t}\end{aligned}]$ and $u(t)=\operatorname{sin}⁡t.$

One radio selection field; five full vectors. Original bank:

- $[\begin{aligned}0 \\ 1 \\ {e}^{t}(\operatorname{cos}⁡t+\operatorname{sin}⁡t)\end{aligned}]$

- $[\begin{aligned}\operatorname{sin}⁡2t \\ 1 \\ {e}^{t}(\operatorname{cos}⁡t+\operatorname{sin}⁡t)\end{aligned}]$

- $[\begin{aligned}2\operatorname{sin}⁡2t \\ \operatorname{cos}⁡2t \\ {e}^{t}(\operatorname{cos}⁡t+\operatorname{sin}⁡t)\end{aligned}]$

- $[\begin{aligned}\operatorname{sin}⁡4t \\ {cos}^{2}⁡t-{sin}^{2}⁡t \\ {e}^{t}(\operatorname{cos}⁡t-\operatorname{sin}⁡t)\end{aligned}]$

- $[\begin{aligned}0 \\ {cos}^{2}⁡t-{sin}^{2}⁡t \\ {e}^{t}(\operatorname{cos}⁡t-\operatorname{sin}⁡t)\end{aligned}]$

Original fixed solution sequence:

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

### q-71227 (:question.difficulty/easy)

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}{e}^{3t} \\ {e}^{4t} \\ {e}^{5t}\end{aligned}]$ and $u(t)=t.$

One radio selection field; five full vectors. Original bank:

- $[\begin{aligned}3{e}^{3t} \\ 4{e}^{4t} \\ 5{e}^{5t}\end{aligned}]$

- $[\begin{aligned}(t+3){e}^{3t} \\ (t+4){e}^{4t} \\ (t+5){e}^{5t}\end{aligned}]$

- $[\begin{aligned}3t{e}^{3t} \\ 4t{e}^{4t} \\ 5t{e}^{5t}\end{aligned}]$

- $[\begin{aligned}({t}^{2}+1){e}^{3t} \\ ({t}^{2}+2){e}^{4t} \\ ({t}^{2}+3){e}^{5t}\end{aligned}]$

- $[\begin{aligned}(3t+1){e}^{3t} \\ (4t+1){e}^{4t} \\ (5t+1){e}^{5t}\end{aligned}]$

Original fixed solution sequence:

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

### q-71233 (:question.difficulty/moderate)

Find ${(u(t)f(t))}^{′}$ where $f(t)=[\begin{aligned}2{t}^{3}-3 \\ {t}^{2}+1 \\ 4t-7\end{aligned}]$ and $u(t)={e}^{t}.$

One radio selection field; five full vectors. Original bank:

- $[\begin{aligned}(4{t}^{2}+t){e}^{t} \\ ({t}^{2}-1){e}^{t} \\ {e}^{t}\end{aligned}]$

- $[\begin{aligned}(2{t}^{3}+6{t}^{2}-3){e}^{t} \\ ({t}^{2}+2t+1){e}^{t} \\ (4t-3){e}^{t}\end{aligned}]$

- $[\begin{aligned}(-5{t}^{3}-3{t}^{2}+1){e}^{t} \\ (3{t}^{2}-t-1){e}^{t} \\ (t+2){e}^{t}\end{aligned}]$

- $[\begin{aligned}({t}^{2}-4t+4) \\ ({t}^{2}-1) \\ (2t+3)\end{aligned}]$

- $[\begin{aligned}7{t}^{3}{e}^{t} \\ {t}^{2}{e}^{t} \\ 4t{e}^{t}\end{aligned}]$

Original fixed solution sequence:

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

## Stage 2: generalized mathematical family

Find the first derivative of a scalar elementary function multiplied by a three-coordinate elementary vector function. Differentiate u and each coordinate, form both product-rule vector terms, distribute coordinatewise, add/subtract using the displayed signs, and retain the original final simplification structure. Angle/column notation, sentence punctuation and additional trigonometric/factorization rows distinguish retained presentation templates. No point evaluation is introduced.

## Stage 3: components and complete source bank mapping

Each source has prompt scalar u(t), vector components g_i(t), derivative inputs and results, the two distributed vectors, and one or more summed/simplified vectors. Source solution prose is fixed and never depends on selected wrong answers. `choice-mapping.json` enumerates every original answer UUID, whole original vector, parsed symbolic components, recipe category and component operation names. It maps 70/70 displayed options including 56 distractors. Every source/profile stays a complete bank; it is not merged with a pooled distractor set.

The candidate exact operations are C=u'g+ug', A=ug', B=u'g, B−A, A−B, u'g', g', g, ug, u'g+g', and g+ug'. Whole-vector equality is checked first; otherwise each coordinate is compared to these exact operations. Equality supports a mathematical expression recipe, but a source-coordinate equality alone is not proof of original author intent. Component operations may mix these listed formulas, preserving the complete original vector. Where no operation matches a coordinate, its observed symbolic expression r_i(t) is retained explicitly as an unresolved expression pattern; no polynomial fitting or arbitrary perturbation is used.

Source profiles parameterize independent coordinate factors s_i, so complete wrong operation expressions involving g_i and g_i' transform covariantly. A residual expression is s_i*r_i(t). This is an honest evidence-only expression recipe with unresolved teaching intent. It reproduces all original bank members and retains signed/constant/function structure at s=(1,1,1). These profiles do not become default learner generation. `validation.json` separates whole/component operations from partially unresolved options.

## Stage 4: reusable Markdown/value templates

For observed templates replace complete vector-coordinate slots only: g_i→s_i g_i; derivative argument g_i→s_i g_i; g_i'→s_i g_i'; each distributed/summed vector coordinate x_i→s_i x_i. Scalar u, scalar derivative and the scalar-vector multiplication formula remain unchanged. Vector boundaries are parsed before any substitution. This preserves all original outer rows, signs, equalities and shared prose. s_i are nonzero signed integers with |s_i|≤3. Explicit source replay uses s=(1,1,1). No branch returns the source payload: every vector and bank is rendered through the same parameterized component recipes. Correctness is derived first from u'g+ug', never from a lookup ref.

Source q32501 gets a derived authored solution because none was captured. The original MA widget confirms five angle-vector options. Differentiate t³ times each coordinate independently to obtain <15t⁴,9t²−4t³,12t³>. Assigning easy and marking this option correct are authored repairs, not matched observed labels.

Normal authored templates are documented precisely in classification.md, with a,b,c,d nonzero signed integers and absolute bounds ≤3. Easy/hard use the complete bank {C,A,B,B−A,u'g'}. Moderate uses {C,A,B,B−A,u'g+g'} because u=e^t makes u'g'=ug' and would otherwise duplicate an option. This profile distinction is selected before constructing the bank. Every member is then derived; collisions reject the whole instance. All explicit invalid inputs raise rather than silently resample.

No learner-facing error diagnosis is added. Generation metadata includes source IDs, profile, parameters, mathematical fingerprint, content identity version, domain and dependency versions. UUIDs depend on displayed prompt, fixed solution, complete bank and domain; seed/order changes cannot change fixed content identity. Additional metadata remains outside learner content.

## Plot extraction and scope

Plot rating none. Canonical equation image inspected; see plot-extraction.md. Missing hard is a provisional authored difficulty claim supported by canonical elementary functions, prior sum rule and the product-rule prerequisite. Its greater fixed bookkeeping demand is three nonzero terms in u=t²+a t+b across three nonconstant vector coordinates, never a new calculus operation or progression.
