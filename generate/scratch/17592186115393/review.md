# Product-rule generator review

Database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The unchanged wrapper/record is in `source.json`; canonical example is e-2480 and is not counted as practice.

Original captures are followed by explicitly authored variants. The originals retain their source errors; generated records apply the two supported repairs. Parameter metadata and recipe descriptions are author evidence, not learner content.

## Original — q-128586 / scalar_log

Find $(v(t)f(t))^{′}$ given that  $f(t)=⟨\operatorname{ln}⁡t,\,{t}^{2},\,t⟩$ and $v(t)=2t.$

Captured bank 0

- $2⟨\operatorname{ln}⁡t,\,3{t}^{2},\,\sqrt{t}⟩$
- $2⟨\operatorname{ln}⁡t+1,\,3{t}^{2},\,2t⟩$ **source correct**
- $⟨\operatorname{ln}⁡t+1,\,t,\,3t⟩$
- $2⟨\operatorname{ln}⁡t+1,\,3t,\,{t}^{2}⟩$
- $⟨\operatorname{ln}⁡t,\,3{t}^{2},\,{t}^{2}⟩$

By the scalar function multiple rule, we have

$$
(v(t)f(t))^{′}=v(t){f}^{′}(t)+{v}^{′}(t)f(t).
$$

Let's find ${v}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡t),\,\frac{\text{d}}{\text{d}t}({t}^{2}),\,\frac{\text{d}}{\text{d}t}(t)⟩ \\  & =⟨\frac{1}{t},\,2t,\,1⟩ \\ {v}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2t)=2\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(v(t)f(t))^{′} & =v(t){f}^{′}(t)+{v}^{′}(t)f(t) \\  & =2t⟨\frac{1}{t},\,2t,\,1⟩+2⟨\operatorname{ln}⁡t,\,{t}^{2},\,t⟩ \\  & =⟨2,\,4{t}^{2},\,2t⟩+⟨2\operatorname{ln}⁡t,\,2{t}^{2},\,2t⟩ \\  & =2⟨\operatorname{ln}⁡t+1,\,3{t}^{2},\,2t⟩.\end{aligned}
$$

### Generated variant — observed bank, seed 101

Parameters: `{"c": 5, "m": 3, "n": 1}`. Complete profile `scalar_log_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated easy — scalar_log

Find $(v(t)f(t))^{′}$ given that  $f(t)=⟨\ln{(t )},\,t,\,t^{3}⟩$ and $v(t)=5 t.$

- A. $⟨5 \ln{(t )},\,10 t,\,5 t^{\frac{3}{2}}⟩$
- B. $⟨\ln{(t )},\,2 t,\,t⟩$
- C. $⟨5 \ln{(t )} + 5,\,10 t,\,20 t^{3}⟩$ **correct**
- D. $⟨5 \ln{(t )} + 5,\,10 t^{3},\,5 t⟩$
- E. $⟨\ln{(t )} + 1,\,t^{3},\,2 t^{3}⟩$

By the scalar function multiple rule, we have

$$
(v(t)f(t))^{′}=v(t){f}^{′}(t)+{v}^{′}(t)f(t).
$$

Let's find ${v}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(\ln{(t )}),\,\frac{\text{d}}{\text{d}t}(t),\,\frac{\text{d}}{\text{d}t}(t^{3})⟩ \\  & =⟨\frac{1}{t},\,1,\,3 t^{2}⟩ \\ {v}^{′}(t) & =\frac{\text{d}}{\text{d}t}(5 t)=5\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(v(t)f(t))^{′} & =v(t){f}^{′}(t)+{v}^{′}(t)f(t) \\  & =5 t⟨\frac{1}{t},\,1,\,3 t^{2}⟩+5⟨\ln{(t )},\,t,\,t^{3}⟩ \\  & =⟨5,\,5 t,\,15 t^{3}⟩+⟨5 \ln{(t )},\,5 t,\,5 t^{3}⟩ \\  & =⟨5 \ln{(t )} + 5,\,10 t,\,20 t^{3}⟩.\end{aligned}
$$

### Generated variant — observed bank, seed 102

Parameters: `{"c": 3, "m": 3, "n": 1}`. Complete profile `scalar_log_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated easy — scalar_log

Find $(v(t)f(t))^{′}$ given that  $f(t)=⟨\ln{(t )},\,t,\,t^{3}⟩$ and $v(t)=3 t.$

- A. $⟨3 \ln{(t )} + 3,\,6 t,\,12 t^{3}⟩$ **correct**
- B. $⟨\ln{(t )} + 1,\,t^{3},\,2 t^{3}⟩$
- C. $⟨3 \ln{(t )} + 3,\,6 t^{3},\,3 t⟩$
- D. $⟨3 \ln{(t )},\,6 t,\,3 t^{\frac{3}{2}}⟩$
- E. $⟨\ln{(t )},\,2 t,\,t⟩$

By the scalar function multiple rule, we have

$$
(v(t)f(t))^{′}=v(t){f}^{′}(t)+{v}^{′}(t)f(t).
$$

Let's find ${v}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(\ln{(t )}),\,\frac{\text{d}}{\text{d}t}(t),\,\frac{\text{d}}{\text{d}t}(t^{3})⟩ \\  & =⟨\frac{1}{t},\,1,\,3 t^{2}⟩ \\ {v}^{′}(t) & =\frac{\text{d}}{\text{d}t}(3 t)=3\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(v(t)f(t))^{′} & =v(t){f}^{′}(t)+{v}^{′}(t)f(t) \\  & =3 t⟨\frac{1}{t},\,1,\,3 t^{2}⟩+3⟨\ln{(t )},\,t,\,t^{3}⟩ \\  & =⟨3,\,3 t,\,9 t^{3}⟩+⟨3 \ln{(t )},\,3 t,\,3 t^{3}⟩ \\  & =⟨3 \ln{(t )} + 3,\,6 t,\,12 t^{3}⟩.\end{aligned}
$$

### Generated variant — authored bank, seed 101

Parameters: `{"c": 5, "m": 3, "n": 1}`. Complete profile `scalar_log_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated easy — scalar_log

Find $(v(t)f(t))^{′}$ given that  $f(t)=⟨\ln{(t )},\,t,\,t^{3}⟩$ and $v(t)=5 t.$

- A. $⟨5,\,5 t,\,15 t^{3}⟩$
- B. $⟨5 \ln{(t )} + 10,\,15 t,\,35 t^{3}⟩$
- C. $⟨5 \ln{(t )} + 5,\,10 t,\,20 t^{3}⟩$ **correct**
- D. $⟨5 - 5 \ln{(t )},\,0,\,10 t^{3}⟩$
- E. $⟨5 \ln{(t )},\,5 t,\,5 t^{3}⟩$

By the scalar function multiple rule, we have

$$
(v(t)f(t))^{′}=v(t){f}^{′}(t)+{v}^{′}(t)f(t).
$$

Let's find ${v}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(\ln{(t )}),\,\frac{\text{d}}{\text{d}t}(t),\,\frac{\text{d}}{\text{d}t}(t^{3})⟩ \\  & =⟨\frac{1}{t},\,1,\,3 t^{2}⟩ \\ {v}^{′}(t) & =\frac{\text{d}}{\text{d}t}(5 t)=5\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(v(t)f(t))^{′} & =v(t){f}^{′}(t)+{v}^{′}(t)f(t) \\  & =5 t⟨\frac{1}{t},\,1,\,3 t^{2}⟩+5⟨\ln{(t )},\,t,\,t^{3}⟩ \\  & =⟨5,\,5 t,\,15 t^{3}⟩+⟨5 \ln{(t )},\,5 t,\,5 t^{3}⟩ \\  & =⟨5 \ln{(t )} + 5,\,10 t,\,20 t^{3}⟩.\end{aligned}
$$

### Generated variant — authored bank, seed 102

Parameters: `{"c": 3, "m": 3, "n": 1}`. Complete profile `scalar_log_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated easy — scalar_log

Find $(v(t)f(t))^{′}$ given that  $f(t)=⟨\ln{(t )},\,t,\,t^{3}⟩$ and $v(t)=3 t.$

- A. $⟨3 \ln{(t )} + 3,\,6 t,\,12 t^{3}⟩$ **correct**
- B. $⟨3 \ln{(t )},\,3 t,\,3 t^{3}⟩$
- C. $⟨3 - 3 \ln{(t )},\,0,\,6 t^{3}⟩$
- D. $⟨3,\,3 t,\,9 t^{3}⟩$
- E. $⟨3 \ln{(t )} + 6,\,9 t,\,21 t^{3}⟩$

By the scalar function multiple rule, we have

$$
(v(t)f(t))^{′}=v(t){f}^{′}(t)+{v}^{′}(t)f(t).
$$

Let's find ${v}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(\ln{(t )}),\,\frac{\text{d}}{\text{d}t}(t),\,\frac{\text{d}}{\text{d}t}(t^{3})⟩ \\  & =⟨\frac{1}{t},\,1,\,3 t^{2}⟩ \\ {v}^{′}(t) & =\frac{\text{d}}{\text{d}t}(3 t)=3\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(v(t)f(t))^{′} & =v(t){f}^{′}(t)+{v}^{′}(t)f(t) \\  & =3 t⟨\frac{1}{t},\,1,\,3 t^{2}⟩+3⟨\ln{(t )},\,t,\,t^{3}⟩ \\  & =⟨3,\,3 t,\,9 t^{3}⟩+⟨3 \ln{(t )},\,3 t,\,3 t^{3}⟩ \\  & =⟨3 \ln{(t )} + 3,\,6 t,\,12 t^{3}⟩.\end{aligned}
$$

## Original — q-128587 / scalar_power

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨t,\,{t}^{2},\,2{t}^{3}⟩$ and $u(t)={t}^{3}.$

Captured bank 0

- $⟨2t,\,5{t}^{3},\,9{t}^{4}⟩$
- $⟨{t}^{4},\,{t}^{3},\,{t}^{2}⟩$
- $⟨2t,\,5{t}^{4},\,3{t}^{5}⟩$
- $⟨4{t}^{3},\,5{t}^{2},\,9{t}^{4}⟩$
- $⟨4{t}^{3},\,5{t}^{4},\,12{t}^{5}⟩$ **source correct**

By the scalar function multiple rule, we have

$$
(ug(t))^{′}=u(t){g}^{′}(t)+{u}^{′}(t)g(t).
$$

Let's find the ${u}^{′}(t)$ and ${g}^{′}(t).$

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t),\,\frac{\text{d}}{\text{d}t}({t}^{2}),\,\frac{\text{d}}{\text{d}t}(2{t}^{3})⟩ \\  & =⟨1,\,2t,\,6{t}^{2}⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{3})=3{t}^{2}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)g(t))^{′} & =u(t){g}^{′}(t)+{u}^{′}(t)g(t) \\  & ={t}^{3}⟨1,\,2t,\,6{t}^{2}⟩+3{t}^{2}⟨t,\,{t}^{2},\,2{t}^{3}⟩ \\  & =⟨{t}^{3},\,2{t}^{4},\,6{t}^{5}⟩+⟨3{t}^{3},\,3{t}^{4},\,6{t}^{5}⟩ \\  & =⟨4{t}^{3},\,5{t}^{4},\,12{t}^{5}⟩.\end{aligned}
$$

### Generated variant — observed bank, seed 101

Parameters: `{"a": 5, "b": 2, "c": 5, "n": 3, "p": 2, "q": 3, "r": 4}`. Complete profile `scalar_power_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated easy — scalar_power

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨5 t^{2},\,2 t^{3},\,5 t^{4}⟩$ and $u(t)=t^{3}.$

- A. $⟨5 t^{2},\,12 t^{5},\,3 t^{6}⟩$
- B. $⟨25 t^{4},\,12 t^{5},\,35 t^{6}⟩$ **correct**
- C. $⟨25 t^{4},\,12 t^{3},\,12 t^{5}⟩$
- D. $⟨t^{5},\,t^{3},\,t^{3}⟩$
- E. $⟨5 t^{2},\,12 t^{3},\,12 t^{5}⟩$

By the scalar function multiple rule, we have

$$
(u(t)g(t))^{′}=u(t){g}^{′}(t)+{u}^{′}(t)g(t).
$$

Let's find the ${u}^{′}(t)$ and ${g}^{′}(t).$

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(5 t^{2}),\,\frac{\text{d}}{\text{d}t}(2 t^{3}),\,\frac{\text{d}}{\text{d}t}(5 t^{4})⟩ \\  & =⟨10 t,\,6 t^{2},\,20 t^{3}⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t^{3})=3 t^{2}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)g(t))^{′} & =u(t){g}^{′}(t)+{u}^{′}(t)g(t) \\  & =t^{3}⟨10 t,\,6 t^{2},\,20 t^{3}⟩+3 t^{2}⟨5 t^{2},\,2 t^{3},\,5 t^{4}⟩ \\  & =⟨10 t^{4},\,6 t^{5},\,20 t^{6}⟩+⟨15 t^{4},\,6 t^{5},\,15 t^{6}⟩ \\  & =⟨25 t^{4},\,12 t^{5},\,35 t^{6}⟩.\end{aligned}
$$

### Generated variant — observed bank, seed 102

Parameters: `{"a": 2, "b": 6, "c": 5, "n": 3, "p": 2, "q": 3, "r": 4}`. Complete profile `scalar_power_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated easy — scalar_power

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨2 t^{2},\,6 t^{3},\,5 t^{4}⟩$ and $u(t)=t^{3}.$

- A. $⟨5 t^{2},\,36 t^{3},\,12 t^{5}⟩$
- B. $⟨5 t^{2},\,36 t^{5},\,3 t^{6}⟩$
- C. $⟨t^{5},\,t^{3},\,t^{3}⟩$
- D. $⟨10 t^{4},\,36 t^{5},\,35 t^{6}⟩$ **correct**
- E. $⟨10 t^{4},\,36 t^{3},\,12 t^{5}⟩$

By the scalar function multiple rule, we have

$$
(u(t)g(t))^{′}=u(t){g}^{′}(t)+{u}^{′}(t)g(t).
$$

Let's find the ${u}^{′}(t)$ and ${g}^{′}(t).$

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 t^{2}),\,\frac{\text{d}}{\text{d}t}(6 t^{3}),\,\frac{\text{d}}{\text{d}t}(5 t^{4})⟩ \\  & =⟨4 t,\,18 t^{2},\,20 t^{3}⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t^{3})=3 t^{2}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)g(t))^{′} & =u(t){g}^{′}(t)+{u}^{′}(t)g(t) \\  & =t^{3}⟨4 t,\,18 t^{2},\,20 t^{3}⟩+3 t^{2}⟨2 t^{2},\,6 t^{3},\,5 t^{4}⟩ \\  & =⟨4 t^{4},\,18 t^{5},\,20 t^{6}⟩+⟨6 t^{4},\,18 t^{5},\,15 t^{6}⟩ \\  & =⟨10 t^{4},\,36 t^{5},\,35 t^{6}⟩.\end{aligned}
$$

### Generated variant — authored bank, seed 101

Parameters: `{"a": 5, "b": 2, "c": 5, "n": 3, "p": 2, "q": 3, "r": 4}`. Complete profile `scalar_power_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated easy — scalar_power

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨5 t^{2},\,2 t^{3},\,5 t^{4}⟩$ and $u(t)=t^{3}.$

- A. $⟨- 5 t^{4},\,0,\,5 t^{6}⟩$
- B. $⟨25 t^{4},\,12 t^{5},\,35 t^{6}⟩$ **correct**
- C. $⟨35 t^{4},\,18 t^{5},\,55 t^{6}⟩$
- D. $⟨15 t^{4},\,6 t^{5},\,15 t^{6}⟩$
- E. $⟨10 t^{4},\,6 t^{5},\,20 t^{6}⟩$

By the scalar function multiple rule, we have

$$
(u(t)g(t))^{′}=u(t){g}^{′}(t)+{u}^{′}(t)g(t).
$$

Let's find the ${u}^{′}(t)$ and ${g}^{′}(t).$

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(5 t^{2}),\,\frac{\text{d}}{\text{d}t}(2 t^{3}),\,\frac{\text{d}}{\text{d}t}(5 t^{4})⟩ \\  & =⟨10 t,\,6 t^{2},\,20 t^{3}⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t^{3})=3 t^{2}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)g(t))^{′} & =u(t){g}^{′}(t)+{u}^{′}(t)g(t) \\  & =t^{3}⟨10 t,\,6 t^{2},\,20 t^{3}⟩+3 t^{2}⟨5 t^{2},\,2 t^{3},\,5 t^{4}⟩ \\  & =⟨10 t^{4},\,6 t^{5},\,20 t^{6}⟩+⟨15 t^{4},\,6 t^{5},\,15 t^{6}⟩ \\  & =⟨25 t^{4},\,12 t^{5},\,35 t^{6}⟩.\end{aligned}
$$

### Generated variant — authored bank, seed 102

Parameters: `{"a": 2, "b": 6, "c": 5, "n": 3, "p": 2, "q": 3, "r": 4}`. Complete profile `scalar_power_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated easy — scalar_power

Find  $(u(t)g(t))^{′}$ where $g(t)=⟨2 t^{2},\,6 t^{3},\,5 t^{4}⟩$ and $u(t)=t^{3}.$

- A. $⟨4 t^{4},\,18 t^{5},\,20 t^{6}⟩$
- B. $⟨- 2 t^{4},\,0,\,5 t^{6}⟩$
- C. $⟨6 t^{4},\,18 t^{5},\,15 t^{6}⟩$
- D. $⟨10 t^{4},\,36 t^{5},\,35 t^{6}⟩$ **correct**
- E. $⟨14 t^{4},\,54 t^{5},\,55 t^{6}⟩$

By the scalar function multiple rule, we have

$$
(u(t)g(t))^{′}=u(t){g}^{′}(t)+{u}^{′}(t)g(t).
$$

Let's find the ${u}^{′}(t)$ and ${g}^{′}(t).$

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 t^{2}),\,\frac{\text{d}}{\text{d}t}(6 t^{3}),\,\frac{\text{d}}{\text{d}t}(5 t^{4})⟩ \\  & =⟨4 t,\,18 t^{2},\,20 t^{3}⟩ \\ {u}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t^{3})=3 t^{2}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(u(t)g(t))^{′} & =u(t){g}^{′}(t)+{u}^{′}(t)g(t) \\  & =t^{3}⟨4 t,\,18 t^{2},\,20 t^{3}⟩+3 t^{2}⟨2 t^{2},\,6 t^{3},\,5 t^{4}⟩ \\  & =⟨4 t^{4},\,18 t^{5},\,20 t^{6}⟩+⟨6 t^{4},\,18 t^{5},\,15 t^{6}⟩ \\  & =⟨10 t^{4},\,36 t^{5},\,35 t^{6}⟩.\end{aligned}
$$

## Original — q-128894 / scalar_exp

Find $(v(t)f(t))^{′}$ given that  $f(t)=⟨{e}^{t+1},\,{e}^{-t},\,{e}^{2t}⟩$ and $v(t)={e}^{t}.$

Captured bank 0

- $⟨2{e}^{t+1},\,2,\,4{e}^{3t}⟩$
- $⟨{e}^{2t+1},\,0,\,-3{e}^{3t}⟩$
- $⟨{e}^{2t+1},\,-2,\,2{e}^{3t}⟩$
- $⟨{e}^{2t+1},\,1,\,2{e}^{3t}⟩$
- $⟨2{e}^{2t+1},\,0,\,3{e}^{3t}⟩$ **source correct**

By the scalar function multiple rule, we have

$$
(v(t)f(t))^{′}=v(t){f}^{′}(t)+{v}^{′}(t)f(t).
$$

Let's find ${v}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}({e}^{t+1}),\,\frac{\text{d}}{\text{d}t}({e}^{-t}),\,\frac{\text{d}}{\text{d}t}({e}^{2t})⟩ \\  & =⟨{e}^{t+1},\,-{e}^{-t},\,2{e}^{2t}⟩ \\ {v}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{t})={e}^{t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(v(t)f(t))^{′} & =v(t){f}^{′}(t)+{v}^{′}(t)f(t) \\  & ={e}^{t}⟨{e}^{t+1},\,-{e}^{-t},\,2{e}^{2t}⟩+{e}^{t}⟨{e}^{t+1},\,{e}^{-t},\,{e}^{2t}⟩ \\  & =⟨{e}^{2t+1},\,-1,\,2{e}^{3t}⟩+⟨{e}^{2t+1},\,1,\,{e}^{3t}⟩ \\  & =⟨2{e}^{2t+1},\,0,\,3{e}^{3t}⟩.\end{aligned}
$$

### Generated variant — observed bank, seed 101

Parameters: `{"a": 2, "b": 2, "s": 5}`. Complete profile `scalar_exp_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated easy — scalar_exp

Find $(v(t)f(t))^{′}$ given that  $f(t)=⟨e^{2 t + 5},\,e^{- 2 t},\,e^{2 t}⟩$ and $v(t)=e^{2 t}.$

- A. $⟨2 e^{4 t + 5},\,-4,\,2 e^{4 t}⟩$
- B. $⟨2 e^{4 t + 5},\,2,\,2 e^{4 t}⟩$
- C. $⟨2 e^{4 t + 5},\,0,\,- 4 e^{4 t}⟩$
- D. $⟨4 e^{2 t + 5},\,4,\,4 e^{4 t}⟩$
- E. $⟨4 e^{4 t + 5},\,0,\,4 e^{4 t}⟩$ **correct**

By the scalar function multiple rule, we have

$$
(v(t)f(t))^{′}=v(t){f}^{′}(t)+{v}^{′}(t)f(t).
$$

Let's find ${v}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(e^{2 t + 5}),\,\frac{\text{d}}{\text{d}t}(e^{- 2 t}),\,\frac{\text{d}}{\text{d}t}(e^{2 t})⟩ \\  & =⟨2 e^{2 t + 5},\,- 2 e^{- 2 t},\,2 e^{2 t}⟩ \\ {v}^{′}(t) & =\frac{\text{d}}{\text{d}t}(e^{2 t})=2 e^{2 t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(v(t)f(t))^{′} & =v(t){f}^{′}(t)+{v}^{′}(t)f(t) \\  & =e^{2 t}⟨2 e^{2 t + 5},\,- 2 e^{- 2 t},\,2 e^{2 t}⟩+2 e^{2 t}⟨e^{2 t + 5},\,e^{- 2 t},\,e^{2 t}⟩ \\  & =⟨2 e^{4 t + 5},\,-2,\,2 e^{4 t}⟩+⟨2 e^{4 t + 5},\,2,\,2 e^{4 t}⟩ \\  & =⟨4 e^{4 t + 5},\,0,\,4 e^{4 t}⟩.\end{aligned}
$$

### Generated variant — observed bank, seed 102

Parameters: `{"a": 1, "b": 2, "s": 5}`. Complete profile `scalar_exp_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated easy — scalar_exp

Find $(v(t)f(t))^{′}$ given that  $f(t)=⟨e^{t + 5},\,e^{- t},\,e^{2 t}⟩$ and $v(t)=e^{t}.$

- A. $⟨2 e^{2 t + 5},\,0,\,3 e^{3 t}⟩$ **correct**
- B. $⟨e^{2 t + 5},\,0,\,- 3 e^{3 t}⟩$
- C. $⟨e^{2 t + 5},\,-2,\,2 e^{3 t}⟩$
- D. $⟨2 e^{t + 5},\,2,\,4 e^{3 t}⟩$
- E. $⟨e^{2 t + 5},\,1,\,2 e^{3 t}⟩$

By the scalar function multiple rule, we have

$$
(v(t)f(t))^{′}=v(t){f}^{′}(t)+{v}^{′}(t)f(t).
$$

Let's find ${v}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(e^{t + 5}),\,\frac{\text{d}}{\text{d}t}(e^{- t}),\,\frac{\text{d}}{\text{d}t}(e^{2 t})⟩ \\  & =⟨e^{t + 5},\,- e^{- t},\,2 e^{2 t}⟩ \\ {v}^{′}(t) & =\frac{\text{d}}{\text{d}t}(e^{t})=e^{t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(v(t)f(t))^{′} & =v(t){f}^{′}(t)+{v}^{′}(t)f(t) \\  & =e^{t}⟨e^{t + 5},\,- e^{- t},\,2 e^{2 t}⟩+e^{t}⟨e^{t + 5},\,e^{- t},\,e^{2 t}⟩ \\  & =⟨e^{2 t + 5},\,-1,\,2 e^{3 t}⟩+⟨e^{2 t + 5},\,1,\,e^{3 t}⟩ \\  & =⟨2 e^{2 t + 5},\,0,\,3 e^{3 t}⟩.\end{aligned}
$$

### Generated variant — authored bank, seed 101

Parameters: `{"a": 2, "b": 2, "s": 5}`. Complete profile `scalar_exp_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated easy — scalar_exp

Find $(v(t)f(t))^{′}$ given that  $f(t)=⟨e^{2 t + 5},\,e^{- 2 t},\,e^{2 t}⟩$ and $v(t)=e^{2 t}.$

- A. $⟨0,\,-4,\,0⟩$
- B. $⟨6 e^{4 t + 5},\,-2,\,6 e^{4 t}⟩$
- C. $⟨2 e^{4 t + 5},\,2,\,2 e^{4 t}⟩$
- D. $⟨2 e^{4 t + 5},\,-2,\,2 e^{4 t}⟩$
- E. $⟨4 e^{4 t + 5},\,0,\,4 e^{4 t}⟩$ **correct**

By the scalar function multiple rule, we have

$$
(v(t)f(t))^{′}=v(t){f}^{′}(t)+{v}^{′}(t)f(t).
$$

Let's find ${v}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(e^{2 t + 5}),\,\frac{\text{d}}{\text{d}t}(e^{- 2 t}),\,\frac{\text{d}}{\text{d}t}(e^{2 t})⟩ \\  & =⟨2 e^{2 t + 5},\,- 2 e^{- 2 t},\,2 e^{2 t}⟩ \\ {v}^{′}(t) & =\frac{\text{d}}{\text{d}t}(e^{2 t})=2 e^{2 t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(v(t)f(t))^{′} & =v(t){f}^{′}(t)+{v}^{′}(t)f(t) \\  & =e^{2 t}⟨2 e^{2 t + 5},\,- 2 e^{- 2 t},\,2 e^{2 t}⟩+2 e^{2 t}⟨e^{2 t + 5},\,e^{- 2 t},\,e^{2 t}⟩ \\  & =⟨2 e^{4 t + 5},\,-2,\,2 e^{4 t}⟩+⟨2 e^{4 t + 5},\,2,\,2 e^{4 t}⟩ \\  & =⟨4 e^{4 t + 5},\,0,\,4 e^{4 t}⟩.\end{aligned}
$$

### Generated variant — authored bank, seed 102

Parameters: `{"a": 1, "b": 2, "s": 5}`. Complete profile `scalar_exp_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated easy — scalar_exp

Find $(v(t)f(t))^{′}$ given that  $f(t)=⟨e^{t + 5},\,e^{- t},\,e^{2 t}⟩$ and $v(t)=e^{t}.$

- A. $⟨2 e^{2 t + 5},\,0,\,3 e^{3 t}⟩$ **correct**
- B. $⟨e^{2 t + 5},\,1,\,e^{3 t}⟩$
- C. $⟨0,\,-2,\,e^{3 t}⟩$
- D. $⟨e^{2 t + 5},\,-1,\,2 e^{3 t}⟩$
- E. $⟨3 e^{2 t + 5},\,-1,\,5 e^{3 t}⟩$

By the scalar function multiple rule, we have

$$
(v(t)f(t))^{′}=v(t){f}^{′}(t)+{v}^{′}(t)f(t).
$$

Let's find ${v}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(e^{t + 5}),\,\frac{\text{d}}{\text{d}t}(e^{- t}),\,\frac{\text{d}}{\text{d}t}(e^{2 t})⟩ \\  & =⟨e^{t + 5},\,- e^{- t},\,2 e^{2 t}⟩ \\ {v}^{′}(t) & =\frac{\text{d}}{\text{d}t}(e^{t})=e^{t}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(v(t)f(t))^{′} & =v(t){f}^{′}(t)+{v}^{′}(t)f(t) \\  & =e^{t}⟨e^{t + 5},\,- e^{- t},\,2 e^{2 t}⟩+e^{t}⟨e^{t + 5},\,e^{- t},\,e^{2 t}⟩ \\  & =⟨e^{2 t + 5},\,-1,\,2 e^{3 t}⟩+⟨e^{2 t + 5},\,1,\,e^{3 t}⟩ \\  & =⟨2 e^{2 t + 5},\,0,\,3 e^{3 t}⟩.\end{aligned}
$$

## Original — q-33446 / scalar_base

Find $(v(t)f(t))^{′}$ given that  $f(t)=⟨{2}^{t},\,{2}^{t+1},\,{2}^{2t}+1⟩$ and $v(t)=\frac{1}{{2}^{t}}.$

Captured bank 0

- $⟨0,\,0,\,\frac{({2}^{2t}-1)\operatorname{ln}⁡2}{{2}^{t}}⟩$ **source correct**
- $⟨\operatorname{ln}⁡2,\,\operatorname{ln}⁡2,\,({2}^{2t}-1)\operatorname{ln}⁡2⟩$
- $⟨0,\,-\frac{\operatorname{ln}⁡2}{{2}^{t}},\,0⟩$
- $⟨{2}^{t},\,0,\,\frac{({2}^{2t}-1)\operatorname{ln}⁡2}{{2}^{t}}⟩$
- $⟨0,\,\operatorname{ln}⁡2,\,-\frac{\operatorname{ln}⁡2}{{2}^{t}}⟩$

By the scalar function multiple rule, we have

$$
(v(t)f(t))^{′}=v(t){f}^{′}(t)+{v}^{′}(t)f(t)
$$

Let's find ${v}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}({2}^{t}),\,\frac{\text{d}}{\text{d}t}({2}^{t+1}),\,\frac{\text{d}}{\text{d}t}({2}^{2t}+1)⟩ \\  & =⟨{2}^{t}\operatorname{ln}⁡2,\,{2}^{t+1}\operatorname{ln}⁡2,\,2\cdot {2}^{2t}\operatorname{ln}⁡2⟩ \\ {v}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\frac{1}{{2}^{t}})=-\frac{\operatorname{ln}⁡2}{{2}^{t}}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(v(t)f(t))^{′} & =v(t){f}^{′}(t)+{v}^{′}(t)f(t) \\  & =\frac{1}{{2}^{t}}⟨{2}^{t}\operatorname{ln}⁡2,\,{2}^{t+1}\operatorname{ln}⁡2,\,2\cdot {2}^{2t}\operatorname{ln}⁡2⟩-\frac{\operatorname{ln}⁡2}{{2}^{t}}⟨{2}^{t},\,{2}^{t+1},\,{2}^{2t}+1⟩ \\  & =⟨\frac{{2}^{t}\operatorname{ln}⁡2}{{2}^{t}},\,\frac{{2}^{t+1}\operatorname{ln}⁡2}{{2}^{t}},\,\frac{2\cdot {2}^{2t}\operatorname{ln}⁡2}{{2}^{t}}⟩-⟨\frac{{2}^{t}\operatorname{ln}⁡2}{{2}^{t}},\,\frac{{2}^{t+1}2\operatorname{ln}⁡2}{{2}^{t}},\,\frac{({2}^{2t}+1)\operatorname{ln}⁡2}{{2}^{t}}⟩ \\  & =⟨0,\,0,\,\frac{({2}^{2t}-1)\operatorname{ln}⁡2}{{2}^{t}}⟩\end{aligned}
$$

### Generated variant — observed bank, seed 101

Parameters: `{"base": 3, "c": 3, "s": 2}`. Complete profile `scalar_base_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated easy — scalar_base

Find $(v(t)f(t))^{′}$ given that  $f(t)=⟨3^{t},\,3^{t + 2},\,9^{t} + 3⟩$ and $v(t)=3^{- t}.$

- A. $⟨3^{t},\,0,\,3^{- t} (9^{t} - 3) \ln{(3 )}⟩$
- B. $⟨0,\,\ln{(3 )},\,- 3^{1 - t} \ln{(3 )}⟩$
- C. $⟨0,\,- 3^{- t} \ln{(3 )},\,0⟩$
- D. $⟨\ln{(3 )},\,\ln{(3 )},\,(9^{t} - 3) \ln{(3 )}⟩$
- E. $⟨0,\,0,\,3^{- t} (9^{t} - 3) \ln{(3 )}⟩$ **correct**

By the scalar function multiple rule, we have

$$
(v(t)f(t))^{′}=v(t){f}^{′}(t)+{v}^{′}(t)f(t)
$$

Let's find ${v}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(3^{t}),\,\frac{\text{d}}{\text{d}t}(3^{t + 2}),\,\frac{\text{d}}{\text{d}t}(9^{t} + 3)⟩ \\  & =⟨3^{t} \ln{(3 )},\,3^{t + 2} \ln{(3 )},\,2 \cdot 9^{t} \ln{(3 )}⟩ \\ {v}^{′}(t) & =\frac{\text{d}}{\text{d}t}(3^{- t})=- 3^{- t} \ln{(3 )}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(v(t)f(t))^{′} & =v(t){f}^{′}(t)+{v}^{′}(t)f(t) \\  & =3^{- t}⟨3^{t} \ln{(3 )},\,3^{t + 2} \ln{(3 )},\,2 \cdot 9^{t} \ln{(3 )}⟩+- 3^{- t} \ln{(3 )}⟨3^{t},\,3^{t + 2},\,9^{t} + 3⟩ \\  & =⟨\ln{(3 )},\,9 \ln{(3 )},\,2 \cdot 3^{t} \ln{(3 )}⟩+⟨- \ln{(3 )},\,- 9 \ln{(3 )},\,3^{- t} (- 9^{t} - 3) \ln{(3 )}⟩ \\  & =⟨0,\,0,\,3^{- t} (9^{t} - 3) \ln{(3 )}⟩\end{aligned}
$$

### Generated variant — observed bank, seed 102

Parameters: `{"base": 3, "c": 5, "s": 2}`. Complete profile `scalar_base_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated easy — scalar_base

Find $(v(t)f(t))^{′}$ given that  $f(t)=⟨3^{t},\,3^{t + 2},\,9^{t} + 5⟩$ and $v(t)=3^{- t}.$

- A. $⟨0,\,0,\,3^{- t} (9^{t} - 5) \ln{(3 )}⟩$ **correct**
- B. $⟨0,\,- 3^{- t} \ln{(3 )},\,0⟩$
- C. $⟨3^{t},\,0,\,3^{- t} (9^{t} - 5) \ln{(3 )}⟩$
- D. $⟨0,\,\ln{(3 )},\,- 5 \cdot 3^{- t} \ln{(3 )}⟩$
- E. $⟨\ln{(3 )},\,\ln{(3 )},\,(9^{t} - 5) \ln{(3 )}⟩$

By the scalar function multiple rule, we have

$$
(v(t)f(t))^{′}=v(t){f}^{′}(t)+{v}^{′}(t)f(t)
$$

Let's find ${v}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(3^{t}),\,\frac{\text{d}}{\text{d}t}(3^{t + 2}),\,\frac{\text{d}}{\text{d}t}(9^{t} + 5)⟩ \\  & =⟨3^{t} \ln{(3 )},\,3^{t + 2} \ln{(3 )},\,2 \cdot 9^{t} \ln{(3 )}⟩ \\ {v}^{′}(t) & =\frac{\text{d}}{\text{d}t}(3^{- t})=- 3^{- t} \ln{(3 )}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(v(t)f(t))^{′} & =v(t){f}^{′}(t)+{v}^{′}(t)f(t) \\  & =3^{- t}⟨3^{t} \ln{(3 )},\,3^{t + 2} \ln{(3 )},\,2 \cdot 9^{t} \ln{(3 )}⟩+- 3^{- t} \ln{(3 )}⟨3^{t},\,3^{t + 2},\,9^{t} + 5⟩ \\  & =⟨\ln{(3 )},\,9 \ln{(3 )},\,2 \cdot 3^{t} \ln{(3 )}⟩+⟨- \ln{(3 )},\,- 9 \ln{(3 )},\,3^{- t} (- 9^{t} - 5) \ln{(3 )}⟩ \\  & =⟨0,\,0,\,3^{- t} (9^{t} - 5) \ln{(3 )}⟩\end{aligned}
$$

### Generated variant — authored bank, seed 101

Parameters: `{"base": 3, "c": 3, "s": 2}`. Complete profile `scalar_base_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated easy — scalar_base

Find $(v(t)f(t))^{′}$ given that  $f(t)=⟨3^{t},\,3^{t + 2},\,9^{t} + 3⟩$ and $v(t)=3^{- t}.$

- A. $⟨2 \ln{(3 )},\,18 \ln{(3 )},\,3^{1 - t} (9^{t} + 1) \ln{(3 )}⟩$
- B. $⟨\ln{(3 )},\,9 \ln{(3 )},\,3^{1 - t} (9^{t} - 1) \ln{(3 )}⟩$
- C. $⟨- \ln{(3 )},\,- 9 \ln{(3 )},\,3^{- t} (- 9^{t} - 3) \ln{(3 )}⟩$
- D. $⟨\ln{(3 )},\,9 \ln{(3 )},\,2 \cdot 3^{t} \ln{(3 )}⟩$
- E. $⟨0,\,0,\,3^{- t} (9^{t} - 3) \ln{(3 )}⟩$ **correct**

By the scalar function multiple rule, we have

$$
(v(t)f(t))^{′}=v(t){f}^{′}(t)+{v}^{′}(t)f(t)
$$

Let's find ${v}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(3^{t}),\,\frac{\text{d}}{\text{d}t}(3^{t + 2}),\,\frac{\text{d}}{\text{d}t}(9^{t} + 3)⟩ \\  & =⟨3^{t} \ln{(3 )},\,3^{t + 2} \ln{(3 )},\,2 \cdot 9^{t} \ln{(3 )}⟩ \\ {v}^{′}(t) & =\frac{\text{d}}{\text{d}t}(3^{- t})=- 3^{- t} \ln{(3 )}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(v(t)f(t))^{′} & =v(t){f}^{′}(t)+{v}^{′}(t)f(t) \\  & =3^{- t}⟨3^{t} \ln{(3 )},\,3^{t + 2} \ln{(3 )},\,2 \cdot 9^{t} \ln{(3 )}⟩+- 3^{- t} \ln{(3 )}⟨3^{t},\,3^{t + 2},\,9^{t} + 3⟩ \\  & =⟨\ln{(3 )},\,9 \ln{(3 )},\,2 \cdot 3^{t} \ln{(3 )}⟩+⟨- \ln{(3 )},\,- 9 \ln{(3 )},\,3^{- t} (- 9^{t} - 3) \ln{(3 )}⟩ \\  & =⟨0,\,0,\,3^{- t} (9^{t} - 3) \ln{(3 )}⟩\end{aligned}
$$

### Generated variant — authored bank, seed 102

Parameters: `{"base": 3, "c": 5, "s": 2}`. Complete profile `scalar_base_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated easy — scalar_base

Find $(v(t)f(t))^{′}$ given that  $f(t)=⟨3^{t},\,3^{t + 2},\,9^{t} + 5⟩$ and $v(t)=3^{- t}.$

- A. $⟨0,\,0,\,3^{- t} (9^{t} - 5) \ln{(3 )}⟩$ **correct**
- B. $⟨- \ln{(3 )},\,- 9 \ln{(3 )},\,3^{- t} (- 9^{t} - 5) \ln{(3 )}⟩$
- C. $⟨2 \ln{(3 )},\,18 \ln{(3 )},\,3^{- t} (3^{2 t + 1} + 5) \ln{(3 )}⟩$
- D. $⟨\ln{(3 )},\,9 \ln{(3 )},\,3^{- t} (3^{2 t + 1} - 5) \ln{(3 )}⟩$
- E. $⟨\ln{(3 )},\,9 \ln{(3 )},\,2 \cdot 3^{t} \ln{(3 )}⟩$

By the scalar function multiple rule, we have

$$
(v(t)f(t))^{′}=v(t){f}^{′}(t)+{v}^{′}(t)f(t)
$$

Let's find ${v}^{′}(t)$ and ${f}^{′}(t).$

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(3^{t}),\,\frac{\text{d}}{\text{d}t}(3^{t + 2}),\,\frac{\text{d}}{\text{d}t}(9^{t} + 5)⟩ \\  & =⟨3^{t} \ln{(3 )},\,3^{t + 2} \ln{(3 )},\,2 \cdot 9^{t} \ln{(3 )}⟩ \\ {v}^{′}(t) & =\frac{\text{d}}{\text{d}t}(3^{- t})=- 3^{- t} \ln{(3 )}\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}(v(t)f(t))^{′} & =v(t){f}^{′}(t)+{v}^{′}(t)f(t) \\  & =3^{- t}⟨3^{t} \ln{(3 )},\,3^{t + 2} \ln{(3 )},\,2 \cdot 9^{t} \ln{(3 )}⟩+- 3^{- t} \ln{(3 )}⟨3^{t},\,3^{t + 2},\,9^{t} + 5⟩ \\  & =⟨\ln{(3 )},\,9 \ln{(3 )},\,2 \cdot 3^{t} \ln{(3 )}⟩+⟨- \ln{(3 )},\,- 9 \ln{(3 )},\,3^{- t} (- 9^{t} - 5) \ln{(3 )}⟩ \\  & =⟨0,\,0,\,3^{- t} (9^{t} - 5) \ln{(3 )}⟩\end{aligned}
$$

## Original — q-32298 / dot_polynomial

Find $(f\cdot g)^{′}(t)$, given that 

$$
\begin{aligned}f(t) & =20t\,i-2t\,j+(2+5t)\,k \\ g(t) & ={t}^{3}\,i+t\,j+({t}^{2}+t)\,k\end{aligned}
$$

Captured bank 0

- $80{t}^{3}+11{t}^{2}+12t+2$
- $80{t}^{3}+6{t}^{2}+10t+2$
- $60{t}^{3}+15{t}^{2}+14t+2$
- $60{t}^{3}+7{t}^{2}+10t+2$
- $80{t}^{3}+15{t}^{2}+10t+2$ **source correct**

Using the dot product rule, we can write:

$$
(f\cdot g)^{′}(t)={f}^{′}(t)\cdot g(t)+f(t)\cdot {g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(20t)\,i-\frac{\text{d}}{\text{d}t}(2t)\,j+\frac{\text{d}}{\text{d}t}(2+5t)\,k \\  & =20\,i-2\,j+5\,k \\ {g}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{3})\,i+\frac{\text{d}}{\text{d}t}(t)\,j+\frac{\text{d}}{\text{d}t}({t}^{2}+t)\,k \\  & =3{t}^{2}\,i+j+(2t+1)\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f\cdot g)^{′}(t) & ={f}^{′}(t)\cdot g(t)+f(t)\cdot {g}^{′}(t) \\  & =(20\,i-2\,j+5\,k)\cdot ({t}^{3}\,i+t\,j+({t}^{2}+t)\,k)+(20t\,i-2t\,j+(2+5t)\,k)\cdot (3{t}^{2}\,i+j+(2t+1)\,k) \\  & =(20{t}^{3}-2t+5({t}^{2}+t))+(60{t}^{3}-2t+(2+5t)(2t+1)) \\  & =80{t}^{3}+15{t}^{2}+10t+2\end{aligned}
$$

### Generated variant — observed bank, seed 101

Parameters: `{"a": 5, "b": -2, "c": 5, "d": 3}`. Complete profile `dot_polynomial_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated moderate — dot_polynomial

Find $(f\cdotg)^{′}(t)$, given that 

$$
\begin{aligned}f(t) & =5 t\,i- 2 t\,j+(3 t + 5)\,k \\ g(t) & =t^{3}\,i+t\,j+(t (t + 1))\,k\end{aligned}
$$

- A. $20 t^{3} + 7 t^{2} + 11 t + 5$
- B. $15 t^{3} + 8 t^{2} + 12 t + 5$
- C. $20 t^{3} + 15 t^{2} + 12 t + 5$
- D. $20 t^{3} + 9 t^{2} + 12 t + 5$ **correct**
- E. $15 t^{3} + 9 t^{2} + 16 t + 5$

Using the dot product rule, we can write:

$$
(f\cdotg)^{′}(t)={f}^{′}(t)\cdotg(t)+f(t)\cdot{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(5 t)\,i+\frac{\text{d}}{\text{d}t}(- 2 t)\,j+\frac{\text{d}}{\text{d}t}(3 t + 5)\,k \\  & =5\,i-2\,j+3\,k \\ {g}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t^{3})\,i+\frac{\text{d}}{\text{d}t}(t)\,j+\frac{\text{d}}{\text{d}t}(t (t + 1))\,k \\  & =3 t^{2}\,i+\,j+(2 t + 1)\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f\cdotg)^{′}(t) & ={f}^{′}(t)\cdotg(t)+f(t)\cdot{g}^{′}(t) \\  & =(5\,i-2\,j+3\,k)\cdot(t^{3}\,i+t\,j+(t (t + 1))\,k)+(5 t\,i- 2 t\,j+(3 t + 5)\,k)\cdot(3 t^{2}\,i+\,j+(2 t + 1)\,k) \\  & =((5)(t^{3})+(-2)(t)+(3)(t (t + 1)))+((5 t)(3 t^{2})+(- 2 t)(1)+(3 t + 5)(2 t + 1)) \\  & =t (5 t^{2} + 3 t + 1)+15 t^{3} + 6 t^{2} + 11 t + 5 \\  & =20 t^{3} + 9 t^{2} + 12 t + 5\end{aligned}
$$

### Generated variant — observed bank, seed 102

Parameters: `{"a": 2, "b": -6, "c": 5, "d": 3}`. Complete profile `dot_polynomial_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated moderate — dot_polynomial

Find $(f\cdotg)^{′}(t)$, given that 

$$
\begin{aligned}f(t) & =2 t\,i- 6 t\,j+(3 t + 5)\,k \\ g(t) & =t^{3}\,i+t\,j+(t (t + 1))\,k\end{aligned}
$$

- A. $8 t^{3} + 9 t^{2} + 4 t + 5$ **correct**
- B. $8 t^{3} + 15 t^{2} + 4 t + 5$
- C. $6 t^{3} + 9 t^{2} + 16 t + 5$
- D. $6 t^{3} + 8 t^{2} + 4 t + 5$
- E. $8 t^{3} + 7 t^{2} + 11 t + 5$

Using the dot product rule, we can write:

$$
(f\cdotg)^{′}(t)={f}^{′}(t)\cdotg(t)+f(t)\cdot{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2 t)\,i+\frac{\text{d}}{\text{d}t}(- 6 t)\,j+\frac{\text{d}}{\text{d}t}(3 t + 5)\,k \\  & =2\,i-6\,j+3\,k \\ {g}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t^{3})\,i+\frac{\text{d}}{\text{d}t}(t)\,j+\frac{\text{d}}{\text{d}t}(t (t + 1))\,k \\  & =3 t^{2}\,i+\,j+(2 t + 1)\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f\cdotg)^{′}(t) & ={f}^{′}(t)\cdotg(t)+f(t)\cdot{g}^{′}(t) \\  & =(2\,i-6\,j+3\,k)\cdot(t^{3}\,i+t\,j+(t (t + 1))\,k)+(2 t\,i- 6 t\,j+(3 t + 5)\,k)\cdot(3 t^{2}\,i+\,j+(2 t + 1)\,k) \\  & =((2)(t^{3})+(-6)(t)+(3)(t (t + 1)))+((2 t)(3 t^{2})+(- 6 t)(1)+(3 t + 5)(2 t + 1)) \\  & =t (2 t^{2} + 3 t - 3)+6 t^{3} + 6 t^{2} + 7 t + 5 \\  & =8 t^{3} + 9 t^{2} + 4 t + 5\end{aligned}
$$

### Generated variant — authored bank, seed 101

Parameters: `{"a": 5, "b": -2, "c": 5, "d": 3}`. Complete profile `dot_polynomial_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated moderate — dot_polynomial

Find $(f\cdotg)^{′}(t)$, given that 

$$
\begin{aligned}f(t) & =5 t\,i- 2 t\,j+(3 t + 5)\,k \\ g(t) & =t^{3}\,i+t\,j+(t (t + 1))\,k\end{aligned}
$$

- A. $t (5 t^{2} + 3 t + 1)$
- B. $15 t^{2} + 6 t + 1$
- C. $15 t^{3} + 6 t^{2} + 11 t + 5$
- D. $20 t^{3} + 9 t^{2} + 12 t + 5$ **correct**
- E. $- 20 t^{3} - 9 t^{2} - 12 t - 5$

Using the dot product rule, we can write:

$$
(f\cdotg)^{′}(t)={f}^{′}(t)\cdotg(t)+f(t)\cdot{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(5 t)\,i+\frac{\text{d}}{\text{d}t}(- 2 t)\,j+\frac{\text{d}}{\text{d}t}(3 t + 5)\,k \\  & =5\,i-2\,j+3\,k \\ {g}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t^{3})\,i+\frac{\text{d}}{\text{d}t}(t)\,j+\frac{\text{d}}{\text{d}t}(t (t + 1))\,k \\  & =3 t^{2}\,i+\,j+(2 t + 1)\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f\cdotg)^{′}(t) & ={f}^{′}(t)\cdotg(t)+f(t)\cdot{g}^{′}(t) \\  & =(5\,i-2\,j+3\,k)\cdot(t^{3}\,i+t\,j+(t (t + 1))\,k)+(5 t\,i- 2 t\,j+(3 t + 5)\,k)\cdot(3 t^{2}\,i+\,j+(2 t + 1)\,k) \\  & =((5)(t^{3})+(-2)(t)+(3)(t (t + 1)))+((5 t)(3 t^{2})+(- 2 t)(1)+(3 t + 5)(2 t + 1)) \\  & =t (5 t^{2} + 3 t + 1)+15 t^{3} + 6 t^{2} + 11 t + 5 \\  & =20 t^{3} + 9 t^{2} + 12 t + 5\end{aligned}
$$

### Generated variant — authored bank, seed 102

Parameters: `{"a": 2, "b": -6, "c": 5, "d": 3}`. Complete profile `dot_polynomial_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated moderate — dot_polynomial

Find $(f\cdotg)^{′}(t)$, given that 

$$
\begin{aligned}f(t) & =2 t\,i- 6 t\,j+(3 t + 5)\,k \\ g(t) & =t^{3}\,i+t\,j+(t (t + 1))\,k\end{aligned}
$$

- A. $8 t^{3} + 9 t^{2} + 4 t + 5$ **correct**
- B. $6 t^{3} + 6 t^{2} + 7 t + 5$
- C. $- 8 t^{3} - 9 t^{2} - 4 t - 5$
- D. $6 t^{2} + 6 t - 3$
- E. $t (2 t^{2} + 3 t - 3)$

Using the dot product rule, we can write:

$$
(f\cdotg)^{′}(t)={f}^{′}(t)\cdotg(t)+f(t)\cdot{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2 t)\,i+\frac{\text{d}}{\text{d}t}(- 6 t)\,j+\frac{\text{d}}{\text{d}t}(3 t + 5)\,k \\  & =2\,i-6\,j+3\,k \\ {g}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t^{3})\,i+\frac{\text{d}}{\text{d}t}(t)\,j+\frac{\text{d}}{\text{d}t}(t (t + 1))\,k \\  & =3 t^{2}\,i+\,j+(2 t + 1)\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f\cdotg)^{′}(t) & ={f}^{′}(t)\cdotg(t)+f(t)\cdot{g}^{′}(t) \\  & =(2\,i-6\,j+3\,k)\cdot(t^{3}\,i+t\,j+(t (t + 1))\,k)+(2 t\,i- 6 t\,j+(3 t + 5)\,k)\cdot(3 t^{2}\,i+\,j+(2 t + 1)\,k) \\  & =((2)(t^{3})+(-6)(t)+(3)(t (t + 1)))+((2 t)(3 t^{2})+(- 6 t)(1)+(3 t + 5)(2 t + 1)) \\  & =t (2 t^{2} + 3 t - 3)+6 t^{3} + 6 t^{2} + 7 t + 5 \\  & =8 t^{3} + 9 t^{2} + 4 t + 5\end{aligned}
$$

## Original — q-32804 / dot_self_cubic

Given $f(t)=2{t}^{3}\,i-2t\,j+(1+5{t}^{2})\,k$, find $({f}^{′}\cdot f)^{′}(t).$

Captured bank 0

- $12{t}^{4}+150{t}^{2}+14$
- $60{t}^{4}+50{t}^{2}+6$
- $60{t}^{4}+150{t}^{2}+14$ **source correct**
- $12{t}^{4}+50{t}^{2}+14$
- $60{t}^{4}+150{t}^{2}-10$

Using the dot product rule, we can write:

$$
({f}^{′}\cdot f)^{′}(t)={f}^{″}(t)\cdot f(t)+{f}^{′}(t)\cdot {f}^{′}(t)
$$

Let's now find the first and second derivative of the function.

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2{t}^{3})\,i-\frac{\text{d}}{\text{d}t}(2t)\,j+\frac{\text{d}}{\text{d}t}(1+5{t}^{2})\,k \\  & =2\cdot 3{t}^{2}\,i-2\,j+5\cdot 2t\,k \\  & =6{t}^{2}\,i-2\,j+10t\,k \\ {f}^{″}(t) & =\frac{\text{d}}{\text{d}t}(6{t}^{2})\,i-\frac{\text{d}}{\text{d}t}(2)\,j+\frac{\text{d}}{\text{d}t}(10t)\,k \\  & =6\cdot 2t\,i+(0)j+(10)\,k \\  & =12t\,i+10\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}({f}^{′}\cdot f)^{′}(t) & ={f}^{″}(t)\cdot f(t)+{f}^{′}(t)\cdot {f}^{′}(t) \\  & =(12t\,i+10\,k)\cdot (2{t}^{3}\,i-2t\,j+(1+5{t}^{2})\,k)+(6{t}^{2}\,i-2\,j+10t\,k)\cdot (6{t}^{2}\,i-2\,j+10t\,k) \\  & =(12t\cdot 2{t}^{3}+0\cdot (-2t)+10\cdot (1+5{t}^{2}))+((6{t}^{2})^{2}+(-2)^{2}+(10t)^{2}) \\  & =24{t}^{4}+0+10+50{t}^{2}+36{t}^{4}+4+100{t}^{2} \\  & =60{t}^{4}+150{t}^{2}+14\end{aligned}
$$

### Generated variant — observed bank, seed 101

Parameters: `{"a": 5, "b": -2, "c": 5, "d": 3}`. Complete profile `dot_self_cubic_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated moderate — dot_self_cubic

Given $f(t)=5 t^{3}\,i- 2 t\,j+(3 t^{2} + 5)\,k$, find $({f}^{′}\cdotf)^{′}(t).$

- A. $75 t^{4} + 54 t^{2} + 34$
- B. $375 t^{4} + 54 t^{2} - 30$
- C. $375 t^{4} + 18 t^{2} + 14$
- D. $375 t^{4} + 54 t^{2} + 34$ **correct**
- E. $75 t^{4} + 18 t^{2} + 34$

Using the dot product rule, we can write:

$$
({f}^{′}\cdotf)^{′}(t)={f}^{″}(t)\cdotf(t)+{f}^{′}(t)\cdot{f}^{′}(t)
$$

Let's now find the first and second derivative of the function.

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(5 t^{3})\,i+\frac{\text{d}}{\text{d}t}(- 2 t)\,j+\frac{\text{d}}{\text{d}t}(3 t^{2} + 5)\,k \\  & =15 t^{2}\,i-2\,j+6 t\,k \\ {f}^{″}(t) & =\frac{\text{d}}{\text{d}t}(15 t^{2})\,i+\frac{\text{d}}{\text{d}t}(-2)\,j+\frac{\text{d}}{\text{d}t}(6 t)\,k \\  & =30 t\,i+6\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}({f}^{′}\cdotf)^{′}(t) & ={f}^{″}(t)\cdotf(t)+{f}^{′}(t)\cdot{f}^{′}(t) \\  & =(30 t\,i+6\,k)\cdot(5 t^{3}\,i- 2 t\,j+(3 t^{2} + 5)\,k)+(15 t^{2}\,i-2\,j+6 t\,k)\cdot(15 t^{2}\,i-2\,j+6 t\,k) \\  & =((30 t)(5 t^{3})+(0)(- 2 t)+(6)(3 t^{2} + 5))+((15 t^{2})(15 t^{2})+(-2)(-2)+(6 t)(6 t)) \\  & =150 t^{4} + 18 t^{2} + 30+225 t^{4} + 36 t^{2} + 4 \\  & =375 t^{4} + 54 t^{2} + 34\end{aligned}
$$

### Generated variant — observed bank, seed 102

Parameters: `{"a": 2, "b": -6, "c": 5, "d": 3}`. Complete profile `dot_self_cubic_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated moderate — dot_self_cubic

Given $f(t)=2 t^{3}\,i- 6 t\,j+(3 t^{2} + 5)\,k$, find $({f}^{′}\cdotf)^{′}(t).$

- A. $60 t^{4} + 54 t^{2} + 66$ **correct**
- B. $60 t^{4} + 18 t^{2} + 46$
- C. $12 t^{4} + 18 t^{2} + 66$
- D. $60 t^{4} + 54 t^{2} - 30$
- E. $12 t^{4} + 54 t^{2} + 66$

Using the dot product rule, we can write:

$$
({f}^{′}\cdotf)^{′}(t)={f}^{″}(t)\cdotf(t)+{f}^{′}(t)\cdot{f}^{′}(t)
$$

Let's now find the first and second derivative of the function.

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2 t^{3})\,i+\frac{\text{d}}{\text{d}t}(- 6 t)\,j+\frac{\text{d}}{\text{d}t}(3 t^{2} + 5)\,k \\  & =6 t^{2}\,i-6\,j+6 t\,k \\ {f}^{″}(t) & =\frac{\text{d}}{\text{d}t}(6 t^{2})\,i+\frac{\text{d}}{\text{d}t}(-6)\,j+\frac{\text{d}}{\text{d}t}(6 t)\,k \\  & =12 t\,i+6\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}({f}^{′}\cdotf)^{′}(t) & ={f}^{″}(t)\cdotf(t)+{f}^{′}(t)\cdot{f}^{′}(t) \\  & =(12 t\,i+6\,k)\cdot(2 t^{3}\,i- 6 t\,j+(3 t^{2} + 5)\,k)+(6 t^{2}\,i-6\,j+6 t\,k)\cdot(6 t^{2}\,i-6\,j+6 t\,k) \\  & =((12 t)(2 t^{3})+(0)(- 6 t)+(6)(3 t^{2} + 5))+((6 t^{2})(6 t^{2})+(-6)(-6)+(6 t)(6 t)) \\  & =24 t^{4} + 18 t^{2} + 30+36 t^{4} + 36 t^{2} + 36 \\  & =60 t^{4} + 54 t^{2} + 66\end{aligned}
$$

### Generated variant — authored bank, seed 101

Parameters: `{"a": 5, "b": -2, "c": 5, "d": 3}`. Complete profile `dot_self_cubic_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated moderate — dot_self_cubic

Given $f(t)=5 t^{3}\,i- 2 t\,j+(3 t^{2} + 5)\,k$, find $({f}^{′}\cdotf)^{′}(t).$

- A. $150 t^{4} + 18 t^{2} + 30$
- B. $450 t^{3} + 36 t$
- C. $225 t^{4} + 36 t^{2} + 4$
- D. $375 t^{4} + 54 t^{2} + 34$ **correct**
- E. $- 375 t^{4} - 54 t^{2} - 34$

Using the dot product rule, we can write:

$$
({f}^{′}\cdotf)^{′}(t)={f}^{″}(t)\cdotf(t)+{f}^{′}(t)\cdot{f}^{′}(t)
$$

Let's now find the first and second derivative of the function.

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(5 t^{3})\,i+\frac{\text{d}}{\text{d}t}(- 2 t)\,j+\frac{\text{d}}{\text{d}t}(3 t^{2} + 5)\,k \\  & =15 t^{2}\,i-2\,j+6 t\,k \\ {f}^{″}(t) & =\frac{\text{d}}{\text{d}t}(15 t^{2})\,i+\frac{\text{d}}{\text{d}t}(-2)\,j+\frac{\text{d}}{\text{d}t}(6 t)\,k \\  & =30 t\,i+6\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}({f}^{′}\cdotf)^{′}(t) & ={f}^{″}(t)\cdotf(t)+{f}^{′}(t)\cdot{f}^{′}(t) \\  & =(30 t\,i+6\,k)\cdot(5 t^{3}\,i- 2 t\,j+(3 t^{2} + 5)\,k)+(15 t^{2}\,i-2\,j+6 t\,k)\cdot(15 t^{2}\,i-2\,j+6 t\,k) \\  & =((30 t)(5 t^{3})+(0)(- 2 t)+(6)(3 t^{2} + 5))+((15 t^{2})(15 t^{2})+(-2)(-2)+(6 t)(6 t)) \\  & =150 t^{4} + 18 t^{2} + 30+225 t^{4} + 36 t^{2} + 4 \\  & =375 t^{4} + 54 t^{2} + 34\end{aligned}
$$

### Generated variant — authored bank, seed 102

Parameters: `{"a": 2, "b": -6, "c": 5, "d": 3}`. Complete profile `dot_self_cubic_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated moderate — dot_self_cubic

Given $f(t)=2 t^{3}\,i- 6 t\,j+(3 t^{2} + 5)\,k$, find $({f}^{′}\cdotf)^{′}(t).$

- A. $60 t^{4} + 54 t^{2} + 66$ **correct**
- B. $36 t^{4} + 36 t^{2} + 36$
- C. $- 60 t^{4} - 54 t^{2} - 66$
- D. $72 t^{3} + 36 t$
- E. $24 t^{4} + 18 t^{2} + 30$

Using the dot product rule, we can write:

$$
({f}^{′}\cdotf)^{′}(t)={f}^{″}(t)\cdotf(t)+{f}^{′}(t)\cdot{f}^{′}(t)
$$

Let's now find the first and second derivative of the function.

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2 t^{3})\,i+\frac{\text{d}}{\text{d}t}(- 6 t)\,j+\frac{\text{d}}{\text{d}t}(3 t^{2} + 5)\,k \\  & =6 t^{2}\,i-6\,j+6 t\,k \\ {f}^{″}(t) & =\frac{\text{d}}{\text{d}t}(6 t^{2})\,i+\frac{\text{d}}{\text{d}t}(-6)\,j+\frac{\text{d}}{\text{d}t}(6 t)\,k \\  & =12 t\,i+6\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}({f}^{′}\cdotf)^{′}(t) & ={f}^{″}(t)\cdotf(t)+{f}^{′}(t)\cdot{f}^{′}(t) \\  & =(12 t\,i+6\,k)\cdot(2 t^{3}\,i- 6 t\,j+(3 t^{2} + 5)\,k)+(6 t^{2}\,i-6\,j+6 t\,k)\cdot(6 t^{2}\,i-6\,j+6 t\,k) \\  & =((12 t)(2 t^{3})+(0)(- 6 t)+(6)(3 t^{2} + 5))+((6 t^{2})(6 t^{2})+(-6)(-6)+(6 t)(6 t)) \\  & =24 t^{4} + 18 t^{2} + 30+36 t^{4} + 36 t^{2} + 36 \\  & =60 t^{4} + 54 t^{2} + 66\end{aligned}
$$

## Original — q-32835 / dot_self_shifted

Given $f(t)=⟨{t}^{2}-1\,,\,2t\,,\,{t}^{3}-1⟩$, find $({f}^{′}\cdot f)^{′}(t).$

Captured bank 0

- $3{t}^{4}-2{t}^{2}+6t+2$
- $15{t}^{4}+6{t}^{2}+2$
- $15{t}^{4}-6t+2$
- $3{t}^{4}+2{t}^{2}-6t+2$
- $15{t}^{4}+6{t}^{2}-6t+2$ **source correct**

Using the dot product rule, we can write: 

$$
({f}^{′}\cdot f)^{′}(t)={f}^{″}(t)\cdot f(t)+{f}^{′}(t)\cdot {f}^{′}(t)
$$

Let's now find the first and second derivative of the function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}({t}^{2}-1)\,,\,\frac{\text{d}}{\text{d}t}(2t)\,,\,\frac{\text{d}}{\text{d}t}({t}^{3}-1)⟩ \\  & =⟨2t\,,\,2\,,\,3{t}^{2}⟩ \\ {f}^{″}(t) & =⟨\frac{\text{d}}{\text{d}t}(2t)\,,\,\frac{\text{d}}{\text{d}t}(2)\,,\,\frac{\text{d}}{\text{d}t}(3{t}^{2})⟩ \\  & =⟨2\,,\,0\,,\,6t⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}({f}^{′}\cdot f)^{′}(t) & ={f}^{″}(t)\cdot f(t)+{f}^{′}(t)\cdot {f}^{′}(t) \\  & =⟨2\,,\,0\,,\,6t⟩\cdot ⟨{t}^{2}-1\,,\,2t\,,\,{t}^{3}-1⟩+⟨2t\,,\,2\,,\,3{t}^{2}⟩\cdot ⟨2t\,,\,2\,,\,3{t}^{2}⟩ \\  & =(2\cdot ({t}^{2}-1)+0\cdot (2t)+6t\cdot ({t}^{3}-1))+((2t)^{2}+{2}^{2}+(3{t}^{2})^{2}) \\  & =2{t}^{2}-2+0+6{t}^{4}-6t+4{t}^{2}+4+9{t}^{4} \\  & =15{t}^{4}+6{t}^{2}-6t+2\end{aligned}
$$

### Generated variant — observed bank, seed 101

Parameters: `{"a": 5, "b": 5, "c": 3, "h": 2, "k": 4}`. Complete profile `dot_self_shifted_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated moderate — dot_self_shifted

Given $f(t)=⟨5 t^{2} - 2,\,5 t,\,3 t^{3} - 4⟩$, find $({f}^{′}\cdotf)^{′}(t).$

- A. $135 t^{4} - 72 t + 5$
- B. $27 t^{4} + 50 t^{2} - 72 t + 5$
- C. $135 t^{4} + 150 t^{2} + 5$
- D. $27 t^{4} - 50 t^{2} + 72 t + 5$
- E. $135 t^{4} + 150 t^{2} - 72 t + 5$ **correct**

Using the dot product rule, we can write:

$$
({f}^{′}\cdotf)^{′}(t)={f}^{″}(t)\cdotf(t)+{f}^{′}(t)\cdot{f}^{′}(t)
$$

Let's now find the first and second derivative of the function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(5 t^{2} - 2),\,\frac{\text{d}}{\text{d}t}(5 t),\,\frac{\text{d}}{\text{d}t}(3 t^{3} - 4)⟩ \\  & =⟨10 t,\,5,\,9 t^{2}⟩ \\ {f}^{″}(t) & =⟨\frac{\text{d}}{\text{d}t}(10 t),\,\frac{\text{d}}{\text{d}t}(5),\,\frac{\text{d}}{\text{d}t}(9 t^{2})⟩ \\  & =⟨10,\,0,\,18 t⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}({f}^{′}\cdotf)^{′}(t) & ={f}^{″}(t)\cdotf(t)+{f}^{′}(t)\cdot{f}^{′}(t) \\  & =⟨10,\,0,\,18 t⟩\cdot⟨5 t^{2} - 2,\,5 t,\,3 t^{3} - 4⟩+⟨10 t,\,5,\,9 t^{2}⟩\cdot⟨10 t,\,5,\,9 t^{2}⟩ \\  & =((10)(5 t^{2} - 2)+(0)(5 t)+(18 t)(3 t^{3} - 4))+((10 t)(10 t)+(5)(5)+(9 t^{2})(9 t^{2})) \\  & =54 t^{4} + 50 t^{2} - 72 t - 20+81 t^{4} + 100 t^{2} + 25 \\  & =135 t^{4} + 150 t^{2} - 72 t + 5\end{aligned}
$$

### Generated variant — observed bank, seed 102

Parameters: `{"a": 2, "b": 5, "c": 3, "h": 6, "k": 2}`. Complete profile `dot_self_shifted_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated moderate — dot_self_shifted

Given $f(t)=⟨2 t^{2} - 6,\,5 t,\,3 t^{3} - 2⟩$, find $({f}^{′}\cdotf)^{′}(t).$

- A. $135 t^{4} + 24 t^{2} - 36 t + 1$ **correct**
- B. $135 t^{4} + 24 t^{2} + 1$
- C. $135 t^{4} - 36 t + 1$
- D. $27 t^{4} - 8 t^{2} + 36 t + 1$
- E. $27 t^{4} + 8 t^{2} - 36 t + 1$

Using the dot product rule, we can write:

$$
({f}^{′}\cdotf)^{′}(t)={f}^{″}(t)\cdotf(t)+{f}^{′}(t)\cdot{f}^{′}(t)
$$

Let's now find the first and second derivative of the function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 t^{2} - 6),\,\frac{\text{d}}{\text{d}t}(5 t),\,\frac{\text{d}}{\text{d}t}(3 t^{3} - 2)⟩ \\  & =⟨4 t,\,5,\,9 t^{2}⟩ \\ {f}^{″}(t) & =⟨\frac{\text{d}}{\text{d}t}(4 t),\,\frac{\text{d}}{\text{d}t}(5),\,\frac{\text{d}}{\text{d}t}(9 t^{2})⟩ \\  & =⟨4,\,0,\,18 t⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}({f}^{′}\cdotf)^{′}(t) & ={f}^{″}(t)\cdotf(t)+{f}^{′}(t)\cdot{f}^{′}(t) \\  & =⟨4,\,0,\,18 t⟩\cdot⟨2 t^{2} - 6,\,5 t,\,3 t^{3} - 2⟩+⟨4 t,\,5,\,9 t^{2}⟩\cdot⟨4 t,\,5,\,9 t^{2}⟩ \\  & =((4)(2 t^{2} - 6)+(0)(5 t)+(18 t)(3 t^{3} - 2))+((4 t)(4 t)+(5)(5)+(9 t^{2})(9 t^{2})) \\  & =54 t^{4} + 8 t^{2} - 36 t - 24+81 t^{4} + 16 t^{2} + 25 \\  & =135 t^{4} + 24 t^{2} - 36 t + 1\end{aligned}
$$

### Generated variant — authored bank, seed 101

Parameters: `{"a": 5, "b": 5, "c": 3, "h": 2, "k": 4}`. Complete profile `dot_self_shifted_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated moderate — dot_self_shifted

Given $f(t)=⟨5 t^{2} - 2,\,5 t,\,3 t^{3} - 4⟩$, find $({f}^{′}\cdotf)^{′}(t).$

- A. $- 135 t^{4} - 150 t^{2} + 72 t - 5$
- B. $162 t^{3} + 100 t$
- C. $81 t^{4} + 100 t^{2} + 25$
- D. $54 t^{4} + 50 t^{2} - 72 t - 20$
- E. $135 t^{4} + 150 t^{2} - 72 t + 5$ **correct**

Using the dot product rule, we can write:

$$
({f}^{′}\cdotf)^{′}(t)={f}^{″}(t)\cdotf(t)+{f}^{′}(t)\cdot{f}^{′}(t)
$$

Let's now find the first and second derivative of the function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(5 t^{2} - 2),\,\frac{\text{d}}{\text{d}t}(5 t),\,\frac{\text{d}}{\text{d}t}(3 t^{3} - 4)⟩ \\  & =⟨10 t,\,5,\,9 t^{2}⟩ \\ {f}^{″}(t) & =⟨\frac{\text{d}}{\text{d}t}(10 t),\,\frac{\text{d}}{\text{d}t}(5),\,\frac{\text{d}}{\text{d}t}(9 t^{2})⟩ \\  & =⟨10,\,0,\,18 t⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}({f}^{′}\cdotf)^{′}(t) & ={f}^{″}(t)\cdotf(t)+{f}^{′}(t)\cdot{f}^{′}(t) \\  & =⟨10,\,0,\,18 t⟩\cdot⟨5 t^{2} - 2,\,5 t,\,3 t^{3} - 4⟩+⟨10 t,\,5,\,9 t^{2}⟩\cdot⟨10 t,\,5,\,9 t^{2}⟩ \\  & =((10)(5 t^{2} - 2)+(0)(5 t)+(18 t)(3 t^{3} - 4))+((10 t)(10 t)+(5)(5)+(9 t^{2})(9 t^{2})) \\  & =54 t^{4} + 50 t^{2} - 72 t - 20+81 t^{4} + 100 t^{2} + 25 \\  & =135 t^{4} + 150 t^{2} - 72 t + 5\end{aligned}
$$

### Generated variant — authored bank, seed 102

Parameters: `{"a": 2, "b": 5, "c": 3, "h": 6, "k": 2}`. Complete profile `dot_self_shifted_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated moderate — dot_self_shifted

Given $f(t)=⟨2 t^{2} - 6,\,5 t,\,3 t^{3} - 2⟩$, find $({f}^{′}\cdotf)^{′}(t).$

- A. $135 t^{4} + 24 t^{2} - 36 t + 1$ **correct**
- B. $81 t^{4} + 16 t^{2} + 25$
- C. $- 135 t^{4} - 24 t^{2} + 36 t - 1$
- D. $54 t^{4} + 8 t^{2} - 36 t - 24$
- E. $162 t^{3} + 16 t$

Using the dot product rule, we can write:

$$
({f}^{′}\cdotf)^{′}(t)={f}^{″}(t)\cdotf(t)+{f}^{′}(t)\cdot{f}^{′}(t)
$$

Let's now find the first and second derivative of the function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 t^{2} - 6),\,\frac{\text{d}}{\text{d}t}(5 t),\,\frac{\text{d}}{\text{d}t}(3 t^{3} - 2)⟩ \\  & =⟨4 t,\,5,\,9 t^{2}⟩ \\ {f}^{″}(t) & =⟨\frac{\text{d}}{\text{d}t}(4 t),\,\frac{\text{d}}{\text{d}t}(5),\,\frac{\text{d}}{\text{d}t}(9 t^{2})⟩ \\  & =⟨4,\,0,\,18 t⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}({f}^{′}\cdotf)^{′}(t) & ={f}^{″}(t)\cdotf(t)+{f}^{′}(t)\cdot{f}^{′}(t) \\  & =⟨4,\,0,\,18 t⟩\cdot⟨2 t^{2} - 6,\,5 t,\,3 t^{3} - 2⟩+⟨4 t,\,5,\,9 t^{2}⟩\cdot⟨4 t,\,5,\,9 t^{2}⟩ \\  & =((4)(2 t^{2} - 6)+(0)(5 t)+(18 t)(3 t^{3} - 2))+((4 t)(4 t)+(5)(5)+(9 t^{2})(9 t^{2})) \\  & =54 t^{4} + 8 t^{2} - 36 t - 24+81 t^{4} + 16 t^{2} + 25 \\  & =135 t^{4} + 24 t^{2} - 36 t + 1\end{aligned}
$$

## Original — q-32837 / dot_self_evaluate

Given $f(t)=({t}^{3}-1)\,i+({t}^{2}-2)\,j+4{t}^{2}\,k$, evaluate $({f}^{′}\cdot f)^{′}(0).$

Captured bank 0

- $4$
- $-8$
- $-4$ **source correct**
- $0$
- $8$

Using the dot product rule, we can write:

$$
({f}^{′}\cdot f)^{′}(t)={f}^{″}(t)\cdot f(t)+{f}^{′}(t)\cdot {f}^{′}(t)
$$

Let's now find the first and second derivative of the function.

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{3}-1)\,i+\frac{\text{d}}{\text{d}t}({t}^{2}-2)\,j+\frac{\text{d}}{\text{d}t}(4{t}^{2})\,k \\  & =3{t}^{2}\,i+2t\,j+4\cdot 2t\,k \\  & =3{t}^{2}\,i+2t\,j+8t\,k \\ {f}^{″}(t) & =\frac{\text{d}}{\text{d}t}(3{t}^{2})\,i+\frac{\text{d}}{\text{d}t}(2t)\,j+\frac{\text{d}}{\text{d}t}(8t)\,k \\  & =3\cdot 2t\,i+2j+8\,k \\  & =6t\,i+2j+8\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}({f}^{′}\cdot f)^{′}(0) & ={f}^{″}(0)\cdot f(0)+{f}^{′}(0)\cdot {f}^{′}(0) \\  & =(6(0)\,i+2\,j+8\,k)\cdot (({0}^{3}-1)\,i+({0}^{2}-2)\,j+4(0)^{2}\,k)+(3(0)^{2}\,i+2(0)\,j+8(0)\,k)\cdot (3(0)^{2}\,i+2(0)\,j+8(0)\,k) \\  & =(2\,j+8\,k)\cdot (-i-2\,j) \\  & =0(-1)+2(-2)+(0) \\  & =-4\end{aligned}
$$

### Generated variant — observed bank, seed 101

Parameters: `{"a": 5, "b": 5, "c": 4, "h": 2, "k": 3, "x": -1}`. Complete profile `dot_self_evaluate_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated moderate — dot_self_evaluate

Given $f(t)=(5 t^{3} - 2)\,i+(5 t^{2} - 3)\,j+4 t^{2}\,k$, evaluate $({f}^{′}\cdotf)^{′}(-1).$

- A. $0$
- B. $651$ **correct**
- C. $1302$
- D. $-651$
- E. $-1302$

Using the dot product rule, we can write:

$$
({f}^{′}\cdotf)^{′}(t)={f}^{″}(t)\cdotf(t)+{f}^{′}(t)\cdot{f}^{′}(t)
$$

Let's now find the first and second derivative of the function.

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(5 t^{3} - 2)\,i+\frac{\text{d}}{\text{d}t}(5 t^{2} - 3)\,j+\frac{\text{d}}{\text{d}t}(4 t^{2})\,k \\  & =15 t^{2}\,i+10 t\,j+8 t\,k \\ {f}^{″}(t) & =\frac{\text{d}}{\text{d}t}(15 t^{2})\,i+\frac{\text{d}}{\text{d}t}(10 t)\,j+\frac{\text{d}}{\text{d}t}(8 t)\,k \\  & =30 t\,i+10\,j+8\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}({f}^{′}\cdotf)^{′}(-1) & ={f}^{″}(-1)\cdotf(-1)+{f}^{′}(-1)\cdot{f}^{′}(-1) \\  & =(-30\,i+10\,j+8\,k)\cdot(-7\,i+2\,j+4\,k)+(15\,i-10\,j-8\,k)\cdot(15\,i-10\,j-8\,k) \\  & =(-30)(-7)+(10)(2)+(8)(4)+(15)(15)+(-10)(-10)+(-8)(-8) \\  & =262+389 \\  & =651\end{aligned}
$$

### Generated variant — observed bank, seed 102

Parameters: `{"a": 2, "b": 5, "c": 2, "h": 6, "k": 3, "x": 1}`. Complete profile `dot_self_evaluate_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated moderate — dot_self_evaluate

Given $f(t)=(2 t^{3} - 6)\,i+(5 t^{2} - 3)\,j+2 t^{2}\,k$, evaluate $({f}^{′}\cdotf)^{′}(1).$

- A. $132$ **correct**
- B. $264$
- C. $0$
- D. $-132$
- E. $-264$

Using the dot product rule, we can write:

$$
({f}^{′}\cdotf)^{′}(t)={f}^{″}(t)\cdotf(t)+{f}^{′}(t)\cdot{f}^{′}(t)
$$

Let's now find the first and second derivative of the function.

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2 t^{3} - 6)\,i+\frac{\text{d}}{\text{d}t}(5 t^{2} - 3)\,j+\frac{\text{d}}{\text{d}t}(2 t^{2})\,k \\  & =6 t^{2}\,i+10 t\,j+4 t\,k \\ {f}^{″}(t) & =\frac{\text{d}}{\text{d}t}(6 t^{2})\,i+\frac{\text{d}}{\text{d}t}(10 t)\,j+\frac{\text{d}}{\text{d}t}(4 t)\,k \\  & =12 t\,i+10\,j+4\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}({f}^{′}\cdotf)^{′}(1) & ={f}^{″}(1)\cdotf(1)+{f}^{′}(1)\cdot{f}^{′}(1) \\  & =(12\,i+10\,j+4\,k)\cdot(-4\,i+2\,j+2\,k)+(6\,i+10\,j+4\,k)\cdot(6\,i+10\,j+4\,k) \\  & =(12)(-4)+(10)(2)+(4)(2)+(6)(6)+(10)(10)+(4)(4) \\  & =-20+152 \\  & =132\end{aligned}
$$

### Generated variant — authored bank, seed 101

Parameters: `{"a": 5, "b": 5, "c": 4, "h": 2, "k": 3, "x": -1}`. Complete profile `dot_self_evaluate_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated moderate — dot_self_evaluate

Given $f(t)=(5 t^{3} - 2)\,i+(5 t^{2} - 3)\,j+4 t^{2}\,k$, evaluate $({f}^{′}\cdotf)^{′}(-1).$

- A. $913$
- B. $651$ **correct**
- C. $127$
- D. $389$
- E. $520$

Using the dot product rule, we can write:

$$
({f}^{′}\cdotf)^{′}(t)={f}^{″}(t)\cdotf(t)+{f}^{′}(t)\cdot{f}^{′}(t)
$$

Let's now find the first and second derivative of the function.

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(5 t^{3} - 2)\,i+\frac{\text{d}}{\text{d}t}(5 t^{2} - 3)\,j+\frac{\text{d}}{\text{d}t}(4 t^{2})\,k \\  & =15 t^{2}\,i+10 t\,j+8 t\,k \\ {f}^{″}(t) & =\frac{\text{d}}{\text{d}t}(15 t^{2})\,i+\frac{\text{d}}{\text{d}t}(10 t)\,j+\frac{\text{d}}{\text{d}t}(8 t)\,k \\  & =30 t\,i+10\,j+8\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}({f}^{′}\cdotf)^{′}(-1) & ={f}^{″}(-1)\cdotf(-1)+{f}^{′}(-1)\cdot{f}^{′}(-1) \\  & =(-30\,i+10\,j+8\,k)\cdot(-7\,i+2\,j+4\,k)+(15\,i-10\,j-8\,k)\cdot(15\,i-10\,j-8\,k) \\  & =(-30)(-7)+(10)(2)+(8)(4)+(15)(15)+(-10)(-10)+(-8)(-8) \\  & =262+389 \\  & =651\end{aligned}
$$

### Generated variant — authored bank, seed 102

Parameters: `{"a": 2, "b": 5, "c": 2, "h": 6, "k": 3, "x": 1}`. Complete profile `dot_self_evaluate_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated moderate — dot_self_evaluate

Given $f(t)=(2 t^{3} - 6)\,i+(5 t^{2} - 3)\,j+2 t^{2}\,k$, evaluate $({f}^{′}\cdotf)^{′}(1).$

- A. $132$ **correct**
- B. $172$
- C. $112$
- D. $152$
- E. $142$

Using the dot product rule, we can write:

$$
({f}^{′}\cdotf)^{′}(t)={f}^{″}(t)\cdotf(t)+{f}^{′}(t)\cdot{f}^{′}(t)
$$

Let's now find the first and second derivative of the function.

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2 t^{3} - 6)\,i+\frac{\text{d}}{\text{d}t}(5 t^{2} - 3)\,j+\frac{\text{d}}{\text{d}t}(2 t^{2})\,k \\  & =6 t^{2}\,i+10 t\,j+4 t\,k \\ {f}^{″}(t) & =\frac{\text{d}}{\text{d}t}(6 t^{2})\,i+\frac{\text{d}}{\text{d}t}(10 t)\,j+\frac{\text{d}}{\text{d}t}(4 t)\,k \\  & =12 t\,i+10\,j+4\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}({f}^{′}\cdotf)^{′}(1) & ={f}^{″}(1)\cdotf(1)+{f}^{′}(1)\cdot{f}^{′}(1) \\  & =(12\,i+10\,j+4\,k)\cdot(-4\,i+2\,j+2\,k)+(6\,i+10\,j+4\,k)\cdot(6\,i+10\,j+4\,k) \\  & =(12)(-4)+(10)(2)+(4)(2)+(6)(6)+(10)(10)+(4)(4) \\  & =-20+152 \\  & =132\end{aligned}
$$

## Original — q-33336 / dot_log_reciprocal

Find $(f\cdot g)^{′}(t)$, given that

$$
\begin{aligned}f(t) & =\operatorname{ln}⁡t\,i+\frac{1}{t}\,j+t\,k \\ g(t) & =t\,i+\frac{1}{t}\,j+\operatorname{ln}⁡t\,k\end{aligned}
$$

Captured bank 0

- $2\operatorname{ln}⁡t+\frac{2}{{t}^{3}}$
- $\operatorname{ln}⁡t+1-\frac{1}{{t}^{3}}$
- $\operatorname{ln}⁡t+1+\frac{1}{{t}^{3}}$
- $2\operatorname{ln}⁡t+2-\frac{2}{{t}^{3}}$ **source correct**
- $0$

Using the dot product rule, we can write:

$$
(f\cdot g)^{′}(t)={f}^{′}(t)\cdot g(t)+f(t)\cdot {g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡t)\,i+\frac{\text{d}}{\text{d}t}(\frac{1}{t})\,j+\frac{\text{d}}{\text{d}t}(t)\,k \\  & =\frac{1}{t}\,i+(-\frac{1}{{t}^{2}})\,j+1\,k \\  & =\frac{1}{t}\,i-\frac{1}{{t}^{2}}\,j+k \\ {g}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t)\,i+\frac{\text{d}}{\text{d}t}(\frac{1}{t})\,j+\frac{\text{d}}{\text{d}t}(\operatorname{ln}⁡t)\,k \\  & =1\,i+(-\frac{1}{{t}^{2}})\,j+\frac{1}{t}\,k \\  & =i-\frac{1}{{t}^{2}}\,j+\frac{1}{t}\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f\cdot g)^{′}(t) & ={f}^{′}(t)\cdot g(t)+f(t)\cdot {g}^{′}(t) \\  & =(\frac{1}{t}\,i-\frac{1}{{t}^{2}}\,j+k)\cdot (t\,i+\frac{1}{t}\,j+\operatorname{ln}⁡t\,k)+(\operatorname{ln}⁡t\,i+\frac{1}{t}\,j+t\,k)\cdot (i-\frac{1}{{t}^{2}}\,j+\frac{1}{t}\,k) \\  & =(\frac{1}{t}\cdot t-\frac{1}{{t}^{2}}\cdot \frac{1}{t}+1\cdot \operatorname{ln}⁡t)+(\operatorname{ln}⁡t\cdot 1+\frac{1}{t}(-\frac{1}{{t}^{2}})+t\cdot \frac{1}{t}) \\  & =1-\frac{1}{{t}^{3}}+\operatorname{ln}⁡t+\operatorname{ln}⁡t-\frac{1}{{t}^{3}}+1 \\  & =2\operatorname{ln}⁡t+2-\frac{2}{{t}^{3}}\end{aligned}
$$

### Generated variant — observed bank, seed 101

Parameters: `{"a": 5, "b": 2, "c": 5, "d": 3, "e": 4, "h": 1}`. Complete profile `dot_log_reciprocal_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated moderate — dot_log_reciprocal

Find $(f\cdotg)^{′}(t)$, given that

$$
\begin{aligned}f(t) & =5 \ln{(t )}\,i+\frac{2}{t}\,j+5 t\,k \\ g(t) & =3 t\,i+\frac{4}{t}\,j+\ln{(t )}\,k\end{aligned}
$$

- A. $10 \ln{(t )} + 10 + \frac{8}{t^{3}}$
- B. $20 \ln{(t )} + 20 - \frac{16}{t^{3}}$ **correct**
- C. $10 \ln{(t )} + 10 - \frac{8}{t^{3}}$
- D. $20 \ln{(t )} + \frac{16}{t^{3}}$
- E. $0$

Using the dot product rule, we can write:

$$
(f\cdotg)^{′}(t)={f}^{′}(t)\cdotg(t)+f(t)\cdot{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(5 \ln{(t )})\,i+\frac{\text{d}}{\text{d}t}(\frac{2}{t})\,j+\frac{\text{d}}{\text{d}t}(5 t)\,k \\  & =\frac{5}{t}\,i- \frac{2}{t^{2}}\,j+5\,k \\ {g}^{′}(t) & =\frac{\text{d}}{\text{d}t}(3 t)\,i+\frac{\text{d}}{\text{d}t}(\frac{4}{t})\,j+\frac{\text{d}}{\text{d}t}(\ln{(t )})\,k \\  & =3\,i- \frac{4}{t^{2}}\,j+\frac{1}{t}\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f\cdotg)^{′}(t) & ={f}^{′}(t)\cdotg(t)+f(t)\cdot{g}^{′}(t) \\  & =(\frac{5}{t}\,i- \frac{2}{t^{2}}\,j+5\,k)\cdot(3 t\,i+\frac{4}{t}\,j+\ln{(t )}\,k)+(5 \ln{(t )}\,i+\frac{2}{t}\,j+5 t\,k)\cdot(3\,i- \frac{4}{t^{2}}\,j+\frac{1}{t}\,k) \\  & =((\frac{5}{t})(3 t)+(- \frac{2}{t^{2}})(\frac{4}{t})+(5)(\ln{(t )}))+((5 \ln{(t )})(3)+(\frac{2}{t})(- \frac{4}{t^{2}})+(5 t)(\frac{1}{t})) \\  & =5 \ln{(t )} + 15 - \frac{8}{t^{3}}+15 \ln{(t )} + 5 - \frac{8}{t^{3}} \\  & =20 \ln{(t )} + 20 - \frac{16}{t^{3}}\end{aligned}
$$

### Generated variant — observed bank, seed 102

Parameters: `{"a": 2, "b": 6, "c": 5, "d": 3, "e": 2, "h": 5}`. Complete profile `dot_log_reciprocal_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated moderate — dot_log_reciprocal

Find $(f\cdotg)^{′}(t)$, given that

$$
\begin{aligned}f(t) & =2 \ln{(t )}\,i+\frac{6}{t}\,j+5 t\,k \\ g(t) & =3 t\,i+\frac{2}{t}\,j+5 \ln{(t )}\,k\end{aligned}
$$

- A. $31 \ln{(t )} + 31 - \frac{24}{t^{3}}$ **correct**
- B. $\frac{31 \ln{(t )}}{2} + \frac{31}{2} - \frac{12}{t^{3}}$
- C. $\frac{31 \ln{(t )}}{2} + \frac{31}{2} + \frac{12}{t^{3}}$
- D. $31 \ln{(t )} + \frac{24}{t^{3}}$
- E. $0$

Using the dot product rule, we can write:

$$
(f\cdotg)^{′}(t)={f}^{′}(t)\cdotg(t)+f(t)\cdot{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2 \ln{(t )})\,i+\frac{\text{d}}{\text{d}t}(\frac{6}{t})\,j+\frac{\text{d}}{\text{d}t}(5 t)\,k \\  & =\frac{2}{t}\,i- \frac{6}{t^{2}}\,j+5\,k \\ {g}^{′}(t) & =\frac{\text{d}}{\text{d}t}(3 t)\,i+\frac{\text{d}}{\text{d}t}(\frac{2}{t})\,j+\frac{\text{d}}{\text{d}t}(5 \ln{(t )})\,k \\  & =3\,i- \frac{2}{t^{2}}\,j+\frac{5}{t}\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f\cdotg)^{′}(t) & ={f}^{′}(t)\cdotg(t)+f(t)\cdot{g}^{′}(t) \\  & =(\frac{2}{t}\,i- \frac{6}{t^{2}}\,j+5\,k)\cdot(3 t\,i+\frac{2}{t}\,j+5 \ln{(t )}\,k)+(2 \ln{(t )}\,i+\frac{6}{t}\,j+5 t\,k)\cdot(3\,i- \frac{2}{t^{2}}\,j+\frac{5}{t}\,k) \\  & =((\frac{2}{t})(3 t)+(- \frac{6}{t^{2}})(\frac{2}{t})+(5)(5 \ln{(t )}))+((2 \ln{(t )})(3)+(\frac{6}{t})(- \frac{2}{t^{2}})+(5 t)(\frac{5}{t})) \\  & =25 \ln{(t )} + 6 - \frac{12}{t^{3}}+6 \ln{(t )} + 25 - \frac{12}{t^{3}} \\  & =31 \ln{(t )} + 31 - \frac{24}{t^{3}}\end{aligned}
$$

### Generated variant — authored bank, seed 101

Parameters: `{"a": 5, "b": 2, "c": 5, "d": 3, "e": 4, "h": 1}`. Complete profile `dot_log_reciprocal_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated moderate — dot_log_reciprocal

Find $(f\cdotg)^{′}(t)$, given that

$$
\begin{aligned}f(t) & =5 \ln{(t )}\,i+\frac{2}{t}\,j+5 t\,k \\ g(t) & =3 t\,i+\frac{4}{t}\,j+\ln{(t )}\,k\end{aligned}
$$

- A. $- 20 \ln{(t )} - 20 + \frac{16}{t^{3}}$
- B. $20 \ln{(t )} + 20 - \frac{16}{t^{3}}$ **correct**
- C. $- 5 \ln{(t )} - 15 + \frac{8}{t^{3}}$
- D. $5 \ln{(t )} + 15 - \frac{8}{t^{3}}$
- E. $\frac{20}{t} + \frac{8}{t^{4}}$

Using the dot product rule, we can write:

$$
(f\cdotg)^{′}(t)={f}^{′}(t)\cdotg(t)+f(t)\cdot{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(5 \ln{(t )})\,i+\frac{\text{d}}{\text{d}t}(\frac{2}{t})\,j+\frac{\text{d}}{\text{d}t}(5 t)\,k \\  & =\frac{5}{t}\,i- \frac{2}{t^{2}}\,j+5\,k \\ {g}^{′}(t) & =\frac{\text{d}}{\text{d}t}(3 t)\,i+\frac{\text{d}}{\text{d}t}(\frac{4}{t})\,j+\frac{\text{d}}{\text{d}t}(\ln{(t )})\,k \\  & =3\,i- \frac{4}{t^{2}}\,j+\frac{1}{t}\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f\cdotg)^{′}(t) & ={f}^{′}(t)\cdotg(t)+f(t)\cdot{g}^{′}(t) \\  & =(\frac{5}{t}\,i- \frac{2}{t^{2}}\,j+5\,k)\cdot(3 t\,i+\frac{4}{t}\,j+\ln{(t )}\,k)+(5 \ln{(t )}\,i+\frac{2}{t}\,j+5 t\,k)\cdot(3\,i- \frac{4}{t^{2}}\,j+\frac{1}{t}\,k) \\  & =((\frac{5}{t})(3 t)+(- \frac{2}{t^{2}})(\frac{4}{t})+(5)(\ln{(t )}))+((5 \ln{(t )})(3)+(\frac{2}{t})(- \frac{4}{t^{2}})+(5 t)(\frac{1}{t})) \\  & =5 \ln{(t )} + 15 - \frac{8}{t^{3}}+15 \ln{(t )} + 5 - \frac{8}{t^{3}} \\  & =20 \ln{(t )} + 20 - \frac{16}{t^{3}}\end{aligned}
$$

### Generated variant — authored bank, seed 102

Parameters: `{"a": 2, "b": 6, "c": 5, "d": 3, "e": 2, "h": 5}`. Complete profile `dot_log_reciprocal_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated moderate — dot_log_reciprocal

Find $(f\cdotg)^{′}(t)$, given that

$$
\begin{aligned}f(t) & =2 \ln{(t )}\,i+\frac{6}{t}\,j+5 t\,k \\ g(t) & =3 t\,i+\frac{2}{t}\,j+5 \ln{(t )}\,k\end{aligned}
$$

- A. $31 \ln{(t )} + 31 - \frac{24}{t^{3}}$ **correct**
- B. $- 25 \ln{(t )} - 6 + \frac{12}{t^{3}}$
- C. $- 31 \ln{(t )} - 31 + \frac{24}{t^{3}}$
- D. $25 \ln{(t )} + 6 - \frac{12}{t^{3}}$
- E. $\frac{31}{t} + \frac{12}{t^{4}}$

Using the dot product rule, we can write:

$$
(f\cdotg)^{′}(t)={f}^{′}(t)\cdotg(t)+f(t)\cdot{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2 \ln{(t )})\,i+\frac{\text{d}}{\text{d}t}(\frac{6}{t})\,j+\frac{\text{d}}{\text{d}t}(5 t)\,k \\  & =\frac{2}{t}\,i- \frac{6}{t^{2}}\,j+5\,k \\ {g}^{′}(t) & =\frac{\text{d}}{\text{d}t}(3 t)\,i+\frac{\text{d}}{\text{d}t}(\frac{2}{t})\,j+\frac{\text{d}}{\text{d}t}(5 \ln{(t )})\,k \\  & =3\,i- \frac{2}{t^{2}}\,j+\frac{5}{t}\,k\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}(f\cdotg)^{′}(t) & ={f}^{′}(t)\cdotg(t)+f(t)\cdot{g}^{′}(t) \\  & =(\frac{2}{t}\,i- \frac{6}{t^{2}}\,j+5\,k)\cdot(3 t\,i+\frac{2}{t}\,j+5 \ln{(t )}\,k)+(2 \ln{(t )}\,i+\frac{6}{t}\,j+5 t\,k)\cdot(3\,i- \frac{2}{t^{2}}\,j+\frac{5}{t}\,k) \\  & =((\frac{2}{t})(3 t)+(- \frac{6}{t^{2}})(\frac{2}{t})+(5)(5 \ln{(t )}))+((2 \ln{(t )})(3)+(\frac{6}{t})(- \frac{2}{t^{2}})+(5 t)(\frac{5}{t})) \\  & =25 \ln{(t )} + 6 - \frac{12}{t^{3}}+6 \ln{(t )} + 25 - \frac{12}{t^{3}} \\  & =31 \ln{(t )} + 31 - \frac{24}{t^{3}}\end{aligned}
$$

## Original — q-32353 / cross_matrix

Find $(f\times g)^{′}(t)$ where

$$
f(t)=[\begin{aligned}3{t}^{2} \\ t+4 \\ 8\end{aligned}],\,g(t)=[\begin{aligned}t+2 \\ -2{t}^{2} \\ 5t\end{aligned}]
$$

Captured bank 0 (legacy duplicate, absent correct designation)

- $\begin{bmatrix}-24t^{3} - 2t - 6 \\ 8 - 45t^{2} \\ 42t + 20\end{bmatrix}$
- $\begin{bmatrix}-42t - 20 \\ 8 - 45t^{2} \\ 24t^{3} + 2t + 6\end{bmatrix}$
- $\begin{bmatrix}42t + 20 \\ 8 - 45t^{2} \\ -24t^{3} - 2t - 6\end{bmatrix}$
- $\begin{bmatrix}8 - 45t^{2} \\ 42t + 20 \\ -24t^{3} - 2t - 6\end{bmatrix}$
- $\begin{bmatrix}21t + 10 \\ 45t^{2} \\ -24t^{3} - 2t - 6\end{bmatrix}$
Captured bank 1

- $[\begin{aligned}21t+10 \\ 45{t}^{2} \\ -24{t}^{3}-2t-6\end{aligned}]$
- $[\begin{aligned}8-45{t}^{2} \\ 42t+20 \\ -24{t}^{3}-2t-6\end{aligned}]$
- $[\begin{aligned}-42t-20 \\ 8-45{t}^{2} \\ 24{t}^{3}+2t+6\end{aligned}]$
- $[\begin{aligned}-24{t}^{3}-2t-6 \\ 8-45{t}^{2} \\ 42t+20\end{aligned}]$
- $[\begin{aligned}42t+20 \\ 8-45{t}^{2} \\ -24{t}^{3}-2t-6\end{aligned}]$ **source correct**

Using the cross product rule, we can write:

$$
(f\times g)^{′}(t)={f}^{′}(t)\times g(t)+f(t)\times {g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(3{t}^{2}) \\ \frac{\text{d}}{\text{d}t}(t+4) \\ \frac{\text{d}}{\text{d}t}(8)\end{aligned}]=[\begin{aligned}6t \\ 1 \\ 0\end{aligned}] \\ {g}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(t+2) \\ \frac{\text{d}}{\text{d}t}(-2{t}^{2}) \\ \frac{\text{d}}{\text{d}t}(5t)\end{aligned}]=[\begin{aligned}1 \\ -4t \\ 5\end{aligned}]\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{f}^{′}(t)\times g(t) & =|\begin{aligned}i & j & k \\ 6t & 1 & 0 \\ t+2 & -2{t}^{2} & 5t\end{aligned}| \\  & =|\begin{aligned}1 & 0 \\ -2{t}^{2} & 5t\end{aligned}|i-|\begin{aligned}6t & 0 \\ t+2 & 5t\end{aligned}|j+|\begin{aligned}6t & 1 \\ t+2 & -2{t}^{2}\end{aligned}|k \\  & =[\begin{aligned}5t \\ -30{t}^{2} \\ -12{t}^{3}-t-2\end{aligned}] \\ f(t)\times {g}^{′}(t) & =|\begin{aligned}i & j & k \\ 3{t}^{2} & t+4 & 8 \\ 1 & -4t & 5\end{aligned}| \\  & =|\begin{aligned}t+4 & 8 \\ -4t & 5\end{aligned}|i-|\begin{aligned}3{t}^{2} & 8 \\ 1 & 5\end{aligned}|j+|\begin{aligned}3{t}^{2} & t+4 \\ 1 & -4t\end{aligned}|k \\  & =[\begin{aligned}37t+20 \\ 8-15{t}^{2} \\ -12{t}^{3}-t-4\end{aligned}]\end{aligned}
$$

Finally,

$$
\begin{aligned}(f\times g)^{′}(t) & =[\begin{aligned}5t \\ -30{t}^{2} \\ -12{t}^{3}-t-2\end{aligned}]+[\begin{aligned}37t+20 \\ 8-15{t}^{2} \\ -12{t}^{3}-t-4\end{aligned}]=[\begin{aligned}42t+20 \\ 8-45{t}^{2} \\ -24{t}^{3}-2t-6\end{aligned}]\end{aligned}
$$

### Generated variant — observed bank, seed 101

Parameters: `{"a": 5, "b": 2, "c": 5, "d": 3, "e": -4, "h": 1}`. Complete profile `cross_matrix_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated hard — cross_matrix

Find $(f\timesg)^{′}(t)$ where

$$
f(t)=[\begin{aligned}5 t^{2} \\ t + 2 \\ 5\end{aligned}],\,g(t)=[\begin{aligned}t + 3 \\ - 4 t^{2} \\ t\end{aligned}]
$$

- A. $[\begin{aligned}5 - 15 t^{2} \\ 42 t + 2 \\ - 80 t^{3} - 2 t - 5\end{aligned}]$
- B. $[\begin{aligned}42 t + 2 \\ 5 - 15 t^{2} \\ - 80 t^{3} - 2 t - 5\end{aligned}]$ **correct**
- C. $[\begin{aligned}- 42 t - 2 \\ 5 - 15 t^{2} \\ 80 t^{3} + 2 t + 5\end{aligned}]$
- D. $[\begin{aligned}- 80 t^{3} - 2 t - 5 \\ 5 - 15 t^{2} \\ 42 t + 2\end{aligned}]$
- E. $[\begin{aligned}21 t + 1 \\ 15 t^{2} \\ - 80 t^{3} - 2 t - 5\end{aligned}]$

Using the cross product rule, we can write:

$$
(f\timesg)^{′}(t)={f}^{′}(t)\timesg(t)+f(t)\times{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(5 t^{2}) \\ \frac{\text{d}}{\text{d}t}(t + 2) \\ \frac{\text{d}}{\text{d}t}(5)\end{aligned}]=[\begin{aligned}10 t \\ 1 \\ 0\end{aligned}] \\ {g}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(t + 3) \\ \frac{\text{d}}{\text{d}t}(- 4 t^{2}) \\ \frac{\text{d}}{\text{d}t}(t)\end{aligned}]=[\begin{aligned}1 \\ - 8 t \\ 1\end{aligned}]\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{f}^{′}(t)\timesg(t) & =|\begin{aligned}i & j & k \\ 10 t & 1 & 0 \\ t + 3 & - 4 t^{2} & t\end{aligned}| \\  & =|\begin{aligned}1 & 0 \\ - 4 t^{2} & t\end{aligned}|i-|\begin{aligned}10 t & 0 \\ t + 3 & t\end{aligned}|j+|\begin{aligned}10 t & 1 \\ t + 3 & - 4 t^{2}\end{aligned}|k \\  & =[\begin{aligned}t \\ - 10 t^{2} \\ - 40 t^{3} - t - 3\end{aligned}] \\ f(t)\times{g}^{′}(t) & =|\begin{aligned}i & j & k \\ 5 t^{2} & t + 2 & 5 \\ 1 & - 8 t & 1\end{aligned}| \\  & =|\begin{aligned}t + 2 & 5 \\ - 8 t & 1\end{aligned}|i-|\begin{aligned}5 t^{2} & 5 \\ 1 & 1\end{aligned}|j+|\begin{aligned}5 t^{2} & t + 2 \\ 1 & - 8 t\end{aligned}|k \\  & =[\begin{aligned}41 t + 2 \\ 5 - 5 t^{2} \\ - 40 t^{3} - t - 2\end{aligned}]\end{aligned}
$$

Finally,

$$
\begin{aligned}(f\timesg)^{′}(t) & =[\begin{aligned}t \\ - 10 t^{2} \\ - 40 t^{3} - t - 3\end{aligned}]+[\begin{aligned}41 t + 2 \\ 5 - 5 t^{2} \\ - 40 t^{3} - t - 2\end{aligned}] \\  & =[\begin{aligned}42 t + 2 \\ 5 - 15 t^{2} \\ - 80 t^{3} - 2 t - 5\end{aligned}]\end{aligned}
$$

### Generated variant — observed bank, seed 102

Parameters: `{"a": 2, "b": 6, "c": 5, "d": 3, "e": -2, "h": 5}`. Complete profile `cross_matrix_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated hard — cross_matrix

Find $(f\timesg)^{′}(t)$ where

$$
f(t)=[\begin{aligned}2 t^{2} \\ t + 6 \\ 5\end{aligned}],\,g(t)=[\begin{aligned}t + 3 \\ - 2 t^{2} \\ 5 t\end{aligned}]
$$

- A. $[\begin{aligned}30 t + 30 \\ 5 - 30 t^{2} \\ - 16 t^{3} - 2 t - 9\end{aligned}]$ **correct**
- B. $[\begin{aligned}- 30 t - 30 \\ 5 - 30 t^{2} \\ 16 t^{3} + 2 t + 9\end{aligned}]$
- C. $[\begin{aligned}5 - 30 t^{2} \\ 30 t + 30 \\ - 16 t^{3} - 2 t - 9\end{aligned}]$
- D. $[\begin{aligned}- 16 t^{3} - 2 t - 9 \\ 5 - 30 t^{2} \\ 30 t + 30\end{aligned}]$
- E. $[\begin{aligned}15 t + 15 \\ 30 t^{2} \\ - 16 t^{3} - 2 t - 9\end{aligned}]$

Using the cross product rule, we can write:

$$
(f\timesg)^{′}(t)={f}^{′}(t)\timesg(t)+f(t)\times{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 t^{2}) \\ \frac{\text{d}}{\text{d}t}(t + 6) \\ \frac{\text{d}}{\text{d}t}(5)\end{aligned}]=[\begin{aligned}4 t \\ 1 \\ 0\end{aligned}] \\ {g}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(t + 3) \\ \frac{\text{d}}{\text{d}t}(- 2 t^{2}) \\ \frac{\text{d}}{\text{d}t}(5 t)\end{aligned}]=[\begin{aligned}1 \\ - 4 t \\ 5\end{aligned}]\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{f}^{′}(t)\timesg(t) & =|\begin{aligned}i & j & k \\ 4 t & 1 & 0 \\ t + 3 & - 2 t^{2} & 5 t\end{aligned}| \\  & =|\begin{aligned}1 & 0 \\ - 2 t^{2} & 5 t\end{aligned}|i-|\begin{aligned}4 t & 0 \\ t + 3 & 5 t\end{aligned}|j+|\begin{aligned}4 t & 1 \\ t + 3 & - 2 t^{2}\end{aligned}|k \\  & =[\begin{aligned}5 t \\ - 20 t^{2} \\ - 8 t^{3} - t - 3\end{aligned}] \\ f(t)\times{g}^{′}(t) & =|\begin{aligned}i & j & k \\ 2 t^{2} & t + 6 & 5 \\ 1 & - 4 t & 5\end{aligned}| \\  & =|\begin{aligned}t + 6 & 5 \\ - 4 t & 5\end{aligned}|i-|\begin{aligned}2 t^{2} & 5 \\ 1 & 5\end{aligned}|j+|\begin{aligned}2 t^{2} & t + 6 \\ 1 & - 4 t\end{aligned}|k \\  & =[\begin{aligned}25 t + 30 \\ 5 - 10 t^{2} \\ - 8 t^{3} - t - 6\end{aligned}]\end{aligned}
$$

Finally,

$$
\begin{aligned}(f\timesg)^{′}(t) & =[\begin{aligned}5 t \\ - 20 t^{2} \\ - 8 t^{3} - t - 3\end{aligned}]+[\begin{aligned}25 t + 30 \\ 5 - 10 t^{2} \\ - 8 t^{3} - t - 6\end{aligned}] \\  & =[\begin{aligned}30 t + 30 \\ 5 - 30 t^{2} \\ - 16 t^{3} - 2 t - 9\end{aligned}]\end{aligned}
$$

### Generated variant — authored bank, seed 101

Parameters: `{"a": 5, "b": 2, "c": 5, "d": 3, "e": -4, "h": 1}`. Complete profile `cross_matrix_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated hard — cross_matrix

Find $(f\timesg)^{′}(t)$ where

$$
f(t)=[\begin{aligned}5 t^{2} \\ t + 2 \\ 5\end{aligned}],\,g(t)=[\begin{aligned}t + 3 \\ - 4 t^{2} \\ t\end{aligned}]
$$

- A. $[\begin{aligned}- 42 t - 2 \\ 15 t^{2} - 5 \\ 80 t^{3} + 2 t + 5\end{aligned}]$
- B. $[\begin{aligned}42 t + 2 \\ 5 - 15 t^{2} \\ - 80 t^{3} - 2 t - 5\end{aligned}]$ **correct**
- C. $[\begin{aligned}41 t + 2 \\ 5 - 5 t^{2} \\ - 40 t^{3} - t - 2\end{aligned}]$
- D. $[\begin{aligned}t \\ - 10 t^{2} \\ - 40 t^{3} - t - 3\end{aligned}]$
- E. $[\begin{aligned}42 t + 2 \\ 15 t^{2} - 5 \\ - 80 t^{3} - 2 t - 5\end{aligned}]$

Using the cross product rule, we can write:

$$
(f\timesg)^{′}(t)={f}^{′}(t)\timesg(t)+f(t)\times{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(5 t^{2}) \\ \frac{\text{d}}{\text{d}t}(t + 2) \\ \frac{\text{d}}{\text{d}t}(5)\end{aligned}]=[\begin{aligned}10 t \\ 1 \\ 0\end{aligned}] \\ {g}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(t + 3) \\ \frac{\text{d}}{\text{d}t}(- 4 t^{2}) \\ \frac{\text{d}}{\text{d}t}(t)\end{aligned}]=[\begin{aligned}1 \\ - 8 t \\ 1\end{aligned}]\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{f}^{′}(t)\timesg(t) & =|\begin{aligned}i & j & k \\ 10 t & 1 & 0 \\ t + 3 & - 4 t^{2} & t\end{aligned}| \\  & =|\begin{aligned}1 & 0 \\ - 4 t^{2} & t\end{aligned}|i-|\begin{aligned}10 t & 0 \\ t + 3 & t\end{aligned}|j+|\begin{aligned}10 t & 1 \\ t + 3 & - 4 t^{2}\end{aligned}|k \\  & =[\begin{aligned}t \\ - 10 t^{2} \\ - 40 t^{3} - t - 3\end{aligned}] \\ f(t)\times{g}^{′}(t) & =|\begin{aligned}i & j & k \\ 5 t^{2} & t + 2 & 5 \\ 1 & - 8 t & 1\end{aligned}| \\  & =|\begin{aligned}t + 2 & 5 \\ - 8 t & 1\end{aligned}|i-|\begin{aligned}5 t^{2} & 5 \\ 1 & 1\end{aligned}|j+|\begin{aligned}5 t^{2} & t + 2 \\ 1 & - 8 t\end{aligned}|k \\  & =[\begin{aligned}41 t + 2 \\ 5 - 5 t^{2} \\ - 40 t^{3} - t - 2\end{aligned}]\end{aligned}
$$

Finally,

$$
\begin{aligned}(f\timesg)^{′}(t) & =[\begin{aligned}t \\ - 10 t^{2} \\ - 40 t^{3} - t - 3\end{aligned}]+[\begin{aligned}41 t + 2 \\ 5 - 5 t^{2} \\ - 40 t^{3} - t - 2\end{aligned}] \\  & =[\begin{aligned}42 t + 2 \\ 5 - 15 t^{2} \\ - 80 t^{3} - 2 t - 5\end{aligned}]\end{aligned}
$$

### Generated variant — authored bank, seed 102

Parameters: `{"a": 2, "b": 6, "c": 5, "d": 3, "e": -2, "h": 5}`. Complete profile `cross_matrix_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated hard — cross_matrix

Find $(f\timesg)^{′}(t)$ where

$$
f(t)=[\begin{aligned}2 t^{2} \\ t + 6 \\ 5\end{aligned}],\,g(t)=[\begin{aligned}t + 3 \\ - 2 t^{2} \\ 5 t\end{aligned}]
$$

- A. $[\begin{aligned}30 t + 30 \\ 5 - 30 t^{2} \\ - 16 t^{3} - 2 t - 9\end{aligned}]$ **correct**
- B. $[\begin{aligned}25 t + 30 \\ 5 - 10 t^{2} \\ - 8 t^{3} - t - 6\end{aligned}]$
- C. $[\begin{aligned}- 30 t - 30 \\ 30 t^{2} - 5 \\ 16 t^{3} + 2 t + 9\end{aligned}]$
- D. $[\begin{aligned}5 t \\ - 20 t^{2} \\ - 8 t^{3} - t - 3\end{aligned}]$
- E. $[\begin{aligned}30 t + 30 \\ 30 t^{2} - 5 \\ - 16 t^{3} - 2 t - 9\end{aligned}]$

Using the cross product rule, we can write:

$$
(f\timesg)^{′}(t)={f}^{′}(t)\timesg(t)+f(t)\times{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(2 t^{2}) \\ \frac{\text{d}}{\text{d}t}(t + 6) \\ \frac{\text{d}}{\text{d}t}(5)\end{aligned}]=[\begin{aligned}4 t \\ 1 \\ 0\end{aligned}] \\ {g}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(t + 3) \\ \frac{\text{d}}{\text{d}t}(- 2 t^{2}) \\ \frac{\text{d}}{\text{d}t}(5 t)\end{aligned}]=[\begin{aligned}1 \\ - 4 t \\ 5\end{aligned}]\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{f}^{′}(t)\timesg(t) & =|\begin{aligned}i & j & k \\ 4 t & 1 & 0 \\ t + 3 & - 2 t^{2} & 5 t\end{aligned}| \\  & =|\begin{aligned}1 & 0 \\ - 2 t^{2} & 5 t\end{aligned}|i-|\begin{aligned}4 t & 0 \\ t + 3 & 5 t\end{aligned}|j+|\begin{aligned}4 t & 1 \\ t + 3 & - 2 t^{2}\end{aligned}|k \\  & =[\begin{aligned}5 t \\ - 20 t^{2} \\ - 8 t^{3} - t - 3\end{aligned}] \\ f(t)\times{g}^{′}(t) & =|\begin{aligned}i & j & k \\ 2 t^{2} & t + 6 & 5 \\ 1 & - 4 t & 5\end{aligned}| \\  & =|\begin{aligned}t + 6 & 5 \\ - 4 t & 5\end{aligned}|i-|\begin{aligned}2 t^{2} & 5 \\ 1 & 5\end{aligned}|j+|\begin{aligned}2 t^{2} & t + 6 \\ 1 & - 4 t\end{aligned}|k \\  & =[\begin{aligned}25 t + 30 \\ 5 - 10 t^{2} \\ - 8 t^{3} - t - 6\end{aligned}]\end{aligned}
$$

Finally,

$$
\begin{aligned}(f\timesg)^{′}(t) & =[\begin{aligned}5 t \\ - 20 t^{2} \\ - 8 t^{3} - t - 3\end{aligned}]+[\begin{aligned}25 t + 30 \\ 5 - 10 t^{2} \\ - 8 t^{3} - t - 6\end{aligned}] \\  & =[\begin{aligned}30 t + 30 \\ 5 - 30 t^{2} \\ - 16 t^{3} - 2 t - 9\end{aligned}]\end{aligned}
$$

### Generated legacy-bank evidence variant — 103

This is one radio field, and its correct ref is inferred from mathematics; the original missing designation remains recorded.

## Generated hard — cross_matrix

Find $(f\timesg)^{′}(t)$ where

$$
f(t)=[\begin{aligned}6 t^{2} \\ t + 4 \\ 6\end{aligned}],\,g(t)=[\begin{aligned}t + 6 \\ - 6 t^{2} \\ 2 t\end{aligned}]
$$

- A. $\begin{bmatrix}6 - 36 t^{2} \\ 76 t + 8 \\ - 144 t^{3} - 2 t - 10\end{bmatrix}$
- B. $\begin{bmatrix}- 144 t^{3} - 2 t - 10 \\ 6 - 36 t^{2} \\ 76 t + 8\end{bmatrix}$
- C. $\begin{bmatrix}- 76 t - 8 \\ 6 - 36 t^{2} \\ 144 t^{3} + 2 t + 10\end{bmatrix}$
- D. $\begin{bmatrix}38 t + 4 \\ 36 t^{2} \\ - 144 t^{3} - 2 t - 10\end{bmatrix}$
- E. $\begin{bmatrix}76 t + 8 \\ 6 - 36 t^{2} \\ - 144 t^{3} - 2 t - 10\end{bmatrix}$ **correct**

Using the cross product rule, we can write:

$$
(f\timesg)^{′}(t)={f}^{′}(t)\timesg(t)+f(t)\times{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(6 t^{2}) \\ \frac{\text{d}}{\text{d}t}(t + 4) \\ \frac{\text{d}}{\text{d}t}(6)\end{aligned}]=[\begin{aligned}12 t \\ 1 \\ 0\end{aligned}] \\ {g}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(t + 6) \\ \frac{\text{d}}{\text{d}t}(- 6 t^{2}) \\ \frac{\text{d}}{\text{d}t}(2 t)\end{aligned}]=[\begin{aligned}1 \\ - 12 t \\ 2\end{aligned}]\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{f}^{′}(t)\timesg(t) & =|\begin{aligned}i & j & k \\ 12 t & 1 & 0 \\ t + 6 & - 6 t^{2} & 2 t\end{aligned}| \\  & =|\begin{aligned}1 & 0 \\ - 6 t^{2} & 2 t\end{aligned}|i-|\begin{aligned}12 t & 0 \\ t + 6 & 2 t\end{aligned}|j+|\begin{aligned}12 t & 1 \\ t + 6 & - 6 t^{2}\end{aligned}|k \\  & =[\begin{aligned}2 t \\ - 24 t^{2} \\ - 72 t^{3} - t - 6\end{aligned}] \\ f(t)\times{g}^{′}(t) & =|\begin{aligned}i & j & k \\ 6 t^{2} & t + 4 & 6 \\ 1 & - 12 t & 2\end{aligned}| \\  & =|\begin{aligned}t + 4 & 6 \\ - 12 t & 2\end{aligned}|i-|\begin{aligned}6 t^{2} & 6 \\ 1 & 2\end{aligned}|j+|\begin{aligned}6 t^{2} & t + 4 \\ 1 & - 12 t\end{aligned}|k \\  & =[\begin{aligned}74 t + 8 \\ 6 - 12 t^{2} \\ - 72 t^{3} - t - 4\end{aligned}]\end{aligned}
$$

Finally,

$$
\begin{aligned}(f\timesg)^{′}(t) & =[\begin{aligned}2 t \\ - 24 t^{2} \\ - 72 t^{3} - t - 6\end{aligned}]+[\begin{aligned}74 t + 8 \\ 6 - 12 t^{2} \\ - 72 t^{3} - t - 4\end{aligned}] \\  & =[\begin{aligned}76 t + 8 \\ 6 - 36 t^{2} \\ - 144 t^{3} - 2 t - 10\end{aligned}]\end{aligned}
$$

### Generated legacy-bank evidence variant — 104

This is one radio field, and its correct ref is inferred from mathematics; the original missing designation remains recorded.

## Generated hard — cross_matrix

Find $(f\timesg)^{′}(t)$ where

$$
f(t)=[\begin{aligned}t^{2} \\ t + 2 \\ 6\end{aligned}],\,g(t)=[\begin{aligned}t + 2 \\ - 4 t^{2} \\ 3 t\end{aligned}]
$$

- A. $\begin{bmatrix}6 - 9 t^{2} \\ 54 t + 6 \\ - 16 t^{3} - 2 t - 4\end{bmatrix}$
- B. $\begin{bmatrix}- 54 t - 6 \\ 6 - 9 t^{2} \\ 16 t^{3} + 2 t + 4\end{bmatrix}$
- C. $\begin{bmatrix}27 t + 3 \\ 9 t^{2} \\ - 16 t^{3} - 2 t - 4\end{bmatrix}$
- D. $\begin{bmatrix}- 16 t^{3} - 2 t - 4 \\ 6 - 9 t^{2} \\ 54 t + 6\end{bmatrix}$
- E. $\begin{bmatrix}54 t + 6 \\ 6 - 9 t^{2} \\ - 16 t^{3} - 2 t - 4\end{bmatrix}$ **correct**

Using the cross product rule, we can write:

$$
(f\timesg)^{′}(t)={f}^{′}(t)\timesg(t)+f(t)\times{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(t^{2}) \\ \frac{\text{d}}{\text{d}t}(t + 2) \\ \frac{\text{d}}{\text{d}t}(6)\end{aligned}]=[\begin{aligned}2 t \\ 1 \\ 0\end{aligned}] \\ {g}^{′}(t) & =[\begin{aligned}\frac{\text{d}}{\text{d}t}(t + 2) \\ \frac{\text{d}}{\text{d}t}(- 4 t^{2}) \\ \frac{\text{d}}{\text{d}t}(3 t)\end{aligned}]=[\begin{aligned}1 \\ - 8 t \\ 3\end{aligned}]\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{f}^{′}(t)\timesg(t) & =|\begin{aligned}i & j & k \\ 2 t & 1 & 0 \\ t + 2 & - 4 t^{2} & 3 t\end{aligned}| \\  & =|\begin{aligned}1 & 0 \\ - 4 t^{2} & 3 t\end{aligned}|i-|\begin{aligned}2 t & 0 \\ t + 2 & 3 t\end{aligned}|j+|\begin{aligned}2 t & 1 \\ t + 2 & - 4 t^{2}\end{aligned}|k \\  & =[\begin{aligned}3 t \\ - 6 t^{2} \\ - 8 t^{3} - t - 2\end{aligned}] \\ f(t)\times{g}^{′}(t) & =|\begin{aligned}i & j & k \\ t^{2} & t + 2 & 6 \\ 1 & - 8 t & 3\end{aligned}| \\  & =|\begin{aligned}t + 2 & 6 \\ - 8 t & 3\end{aligned}|i-|\begin{aligned}t^{2} & 6 \\ 1 & 3\end{aligned}|j+|\begin{aligned}t^{2} & t + 2 \\ 1 & - 8 t\end{aligned}|k \\  & =[\begin{aligned}51 t + 6 \\ 6 - 3 t^{2} \\ - 8 t^{3} - t - 2\end{aligned}]\end{aligned}
$$

Finally,

$$
\begin{aligned}(f\timesg)^{′}(t) & =[\begin{aligned}3 t \\ - 6 t^{2} \\ - 8 t^{3} - t - 2\end{aligned}]+[\begin{aligned}51 t + 6 \\ 6 - 3 t^{2} \\ - 8 t^{3} - t - 2\end{aligned}] \\  & =[\begin{aligned}54 t + 6 \\ 6 - 9 t^{2} \\ - 16 t^{3} - 2 t - 4\end{aligned}]\end{aligned}
$$

## Original — q-128896 / cross_monomials

Find $(f\times g)^{′}(t)$ given that

$$
\begin{aligned}f(t) & =⟨t,\,5,\,{t}^{4}⟩, \\ g(t) & =⟨{t}^{2},\,{t}^{3},\,t⟩.\end{aligned}
$$

Captured bank 0

- $⟨5{t}^{6},\,{t}^{5}+4{t}^{2},\,4{t}^{3}⟩$
- $⟨{t}^{6}-5,\,4{t}^{5}+2t,\,4{t}^{3}-10t⟩$
- $⟨2{t}^{6}+1,\,4{t}^{5},\,{t}^{3}-5t⟩$
- $⟨-7{t}^{6}+5,\,6{t}^{5}-2t,\,4{t}^{3}-10t⟩$ **source correct**
- $⟨7{t}^{6},\,6{t}^{5}-5,\,4{t}^{3}+2t⟩$

Using the cross product rule, we can write:

$$
(f\times g)^{′}(t)={f}^{′}(t)\times g(t)+f(t)\times {g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t),\,\frac{\text{d}}{\text{d}t}(5),\,\frac{\text{d}}{\text{d}t}({t}^{4})⟩ \\  & =⟨1,\,0,\,4{t}^{3}⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}({t}^{2}),\,\frac{\text{d}}{\text{d}t}({t}^{3}),\,\frac{\text{d}}{\text{d}t}(t)⟩ \\  & =⟨2t,\,3{t}^{2},\,1⟩\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}{f}^{′}(t)\times g(t) & =|\begin{aligned}i & j & k \\ 1 & 0 & 4{t}^{3} \\ {t}^{2} & {t}^{3} & t\end{aligned}| \\  & =|\begin{aligned}0 & 4{t}^{3} \\ {t}^{3} & t\end{aligned}|i-|\begin{aligned}1 & 4{t}^{3} \\ {t}^{2} & t\end{aligned}|j+|\begin{aligned}1 & 0 \\ {t}^{2} & {t}^{3}\end{aligned}|k \\  & =⟨-4{t}^{6},\,4{t}^{5}-t,\,{t}^{3}⟩, \\ f(t)\times {g}^{′}(t) & =|\begin{aligned}i & j & k \\ t & 5 & {t}^{4} \\ 2t & 3{t}^{2} & 1\end{aligned}| \\  & =|\begin{aligned}5 & {t}^{4} \\ 3{t}^{2} & 1\end{aligned}|i-|\begin{aligned}t & {t}^{4} \\ 2t & 1\end{aligned}|j+|\begin{aligned}t & 5 \\ 2t & 3{t}^{2}\end{aligned}|k \\  & =⟨5-3{t}^{6},\,2{t}^{5}-t,\,3{t}^{3}-10t⟩.\end{aligned}
$$

Finally,

$$
\begin{aligned}(f\times g)^{′}(t) & =⟨-4{t}^{6},\,4{t}^{5}-t,\,{t}^{3}⟩+⟨5-3{t}^{6},\,2{t}^{5}-t,\,3{t}^{3}-10t⟩ \\  & =⟨-7{t}^{6}+5,\,6{t}^{5}-2t,\,4{t}^{3}-10t⟩.\end{aligned}
$$

### Generated variant — observed bank, seed 101

Parameters: `{"a": 5, "b": 2, "c": 5, "d": 3, "e": 4, "h": 1, "n": 3, "p": 2, "q": 3}`. Complete profile `cross_monomials_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated hard — cross_monomials

Find $(f\timesg)^{′}(t)$ given that

$$
\begin{aligned}f(t) & =⟨5 t,\,2,\,5 t^{3}⟩ \\ g(t) & =⟨3 t^{2},\,4 t^{3},\,t⟩\end{aligned}
$$

- A. $⟨2 - 120 t^{5},\,75 t^{4} - 10 t,\,80 t^{3} - 12 t⟩$ **correct**
- B. $⟨20 t^{5} - 2,\,45 t^{4} + 10 t,\,80 t^{3} - 12 t⟩$
- C. $⟨120 t^{5},\,75 t^{4} - 2,\,80 t^{3} + 10 t⟩$
- D. $⟨40 t^{5},\,15 t^{2} (t^{2} + 1),\,80 t^{3}⟩$
- E. $⟨40 t^{5} + 5,\,45 t^{4},\,20 t^{3} - 6 t⟩$

Using the cross product rule, we can write:

$$
(f\timesg)^{′}(t)={f}^{′}(t)\timesg(t)+f(t)\times{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(5 t),\,\frac{\text{d}}{\text{d}t}(2),\,\frac{\text{d}}{\text{d}t}(5 t^{3})⟩ \\  & =⟨5,\,0,\,15 t^{2}⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(3 t^{2}),\,\frac{\text{d}}{\text{d}t}(4 t^{3}),\,\frac{\text{d}}{\text{d}t}(t)⟩ \\  & =⟨6 t,\,12 t^{2},\,1⟩\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}{f}^{′}(t)\timesg(t) & =|\begin{aligned}i & j & k \\ 5 & 0 & 15 t^{2} \\ 3 t^{2} & 4 t^{3} & t\end{aligned}| \\  & =|\begin{aligned}0 & 15 t^{2} \\ 4 t^{3} & t\end{aligned}|i-|\begin{aligned}5 & 15 t^{2} \\ 3 t^{2} & t\end{aligned}|j+|\begin{aligned}5 & 0 \\ 3 t^{2} & 4 t^{3}\end{aligned}|k \\  & =⟨- 60 t^{5},\,45 t^{4} - 5 t,\,20 t^{3}⟩ \\ f(t)\times{g}^{′}(t) & =|\begin{aligned}i & j & k \\ 5 t & 2 & 5 t^{3} \\ 6 t & 12 t^{2} & 1\end{aligned}| \\  & =|\begin{aligned}2 & 5 t^{3} \\ 12 t^{2} & 1\end{aligned}|i-|\begin{aligned}5 t & 5 t^{3} \\ 6 t & 1\end{aligned}|j+|\begin{aligned}5 t & 2 \\ 6 t & 12 t^{2}\end{aligned}|k \\  & =⟨2 - 60 t^{5},\,30 t^{4} - 5 t,\,60 t^{3} - 12 t⟩\end{aligned}
$$

Finally,

$$
\begin{aligned}(f\timesg)^{′}(t) & =⟨- 60 t^{5},\,45 t^{4} - 5 t,\,20 t^{3}⟩+⟨2 - 60 t^{5},\,30 t^{4} - 5 t,\,60 t^{3} - 12 t⟩ \\  & =⟨2 - 120 t^{5},\,75 t^{4} - 10 t,\,80 t^{3} - 12 t⟩\end{aligned}
$$

### Generated variant — observed bank, seed 102

Parameters: `{"a": 2, "b": 6, "c": 5, "d": 3, "e": 2, "h": 5, "n": 3, "p": 2, "q": 3}`. Complete profile `cross_monomials_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated hard — cross_monomials

Find $(f\timesg)^{′}(t)$ given that

$$
\begin{aligned}f(t) & =⟨2 t,\,6,\,5 t^{3}⟩ \\ g(t) & =⟨3 t^{2},\,2 t^{3},\,5 t⟩\end{aligned}
$$

- A. $⟨60 t^{5},\,15 t^{2} (t^{2} + 2),\,16 t^{3}⟩$
- B. $⟨30 - 60 t^{5},\,75 t^{4} - 20 t,\,16 t^{3} - 36 t⟩$ **correct**
- C. $⟨60 t^{5},\,75 t^{4} - 6,\,16 t^{3} + 20 t⟩$
- D. $⟨20 t^{5} + 10,\,45 t^{4},\,4 t^{3} - 18 t⟩$
- E. $⟨10 t^{5} - 30,\,45 t^{4} + 20 t,\,16 t^{3} - 36 t⟩$

Using the cross product rule, we can write:

$$
(f\timesg)^{′}(t)={f}^{′}(t)\timesg(t)+f(t)\times{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 t),\,\frac{\text{d}}{\text{d}t}(6),\,\frac{\text{d}}{\text{d}t}(5 t^{3})⟩ \\  & =⟨2,\,0,\,15 t^{2}⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(3 t^{2}),\,\frac{\text{d}}{\text{d}t}(2 t^{3}),\,\frac{\text{d}}{\text{d}t}(5 t)⟩ \\  & =⟨6 t,\,6 t^{2},\,5⟩\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}{f}^{′}(t)\timesg(t) & =|\begin{aligned}i & j & k \\ 2 & 0 & 15 t^{2} \\ 3 t^{2} & 2 t^{3} & 5 t\end{aligned}| \\  & =|\begin{aligned}0 & 15 t^{2} \\ 2 t^{3} & 5 t\end{aligned}|i-|\begin{aligned}2 & 15 t^{2} \\ 3 t^{2} & 5 t\end{aligned}|j+|\begin{aligned}2 & 0 \\ 3 t^{2} & 2 t^{3}\end{aligned}|k \\  & =⟨- 30 t^{5},\,45 t^{4} - 10 t,\,4 t^{3}⟩ \\ f(t)\times{g}^{′}(t) & =|\begin{aligned}i & j & k \\ 2 t & 6 & 5 t^{3} \\ 6 t & 6 t^{2} & 5\end{aligned}| \\  & =|\begin{aligned}6 & 5 t^{3} \\ 6 t^{2} & 5\end{aligned}|i-|\begin{aligned}2 t & 5 t^{3} \\ 6 t & 5\end{aligned}|j+|\begin{aligned}2 t & 6 \\ 6 t & 6 t^{2}\end{aligned}|k \\  & =⟨30 - 30 t^{5},\,30 t^{4} - 10 t,\,12 t (t^{2} - 3)⟩\end{aligned}
$$

Finally,

$$
\begin{aligned}(f\timesg)^{′}(t) & =⟨- 30 t^{5},\,45 t^{4} - 10 t,\,4 t^{3}⟩+⟨30 - 30 t^{5},\,30 t^{4} - 10 t,\,12 t (t^{2} - 3)⟩ \\  & =⟨30 - 60 t^{5},\,75 t^{4} - 20 t,\,16 t^{3} - 36 t⟩\end{aligned}
$$

### Generated variant — authored bank, seed 101

Parameters: `{"a": 5, "b": 2, "c": 5, "d": 3, "e": 4, "h": 1, "n": 3, "p": 2, "q": 3}`. Complete profile `cross_monomials_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated hard — cross_monomials

Find $(f\timesg)^{′}(t)$ given that

$$
\begin{aligned}f(t) & =⟨5 t,\,2,\,5 t^{3}⟩ \\ g(t) & =⟨3 t^{2},\,4 t^{3},\,t⟩\end{aligned}
$$

- A. $⟨2 - 120 t^{5},\,75 t^{4} - 10 t,\,80 t^{3} - 12 t⟩$ **correct**
- B. $⟨2 - 60 t^{5},\,30 t^{4} - 5 t,\,60 t^{3} - 12 t⟩$
- C. $⟨2 - 120 t^{5},\,- 75 t^{4} + 10 t,\,80 t^{3} - 12 t⟩$
- D. $⟨- 60 t^{5},\,45 t^{4} - 5 t,\,20 t^{3}⟩$
- E. $⟨120 t^{5} - 2,\,- 75 t^{4} + 10 t,\,- 80 t^{3} + 12 t⟩$

Using the cross product rule, we can write:

$$
(f\timesg)^{′}(t)={f}^{′}(t)\timesg(t)+f(t)\times{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(5 t),\,\frac{\text{d}}{\text{d}t}(2),\,\frac{\text{d}}{\text{d}t}(5 t^{3})⟩ \\  & =⟨5,\,0,\,15 t^{2}⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(3 t^{2}),\,\frac{\text{d}}{\text{d}t}(4 t^{3}),\,\frac{\text{d}}{\text{d}t}(t)⟩ \\  & =⟨6 t,\,12 t^{2},\,1⟩\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}{f}^{′}(t)\timesg(t) & =|\begin{aligned}i & j & k \\ 5 & 0 & 15 t^{2} \\ 3 t^{2} & 4 t^{3} & t\end{aligned}| \\  & =|\begin{aligned}0 & 15 t^{2} \\ 4 t^{3} & t\end{aligned}|i-|\begin{aligned}5 & 15 t^{2} \\ 3 t^{2} & t\end{aligned}|j+|\begin{aligned}5 & 0 \\ 3 t^{2} & 4 t^{3}\end{aligned}|k \\  & =⟨- 60 t^{5},\,45 t^{4} - 5 t,\,20 t^{3}⟩ \\ f(t)\times{g}^{′}(t) & =|\begin{aligned}i & j & k \\ 5 t & 2 & 5 t^{3} \\ 6 t & 12 t^{2} & 1\end{aligned}| \\  & =|\begin{aligned}2 & 5 t^{3} \\ 12 t^{2} & 1\end{aligned}|i-|\begin{aligned}5 t & 5 t^{3} \\ 6 t & 1\end{aligned}|j+|\begin{aligned}5 t & 2 \\ 6 t & 12 t^{2}\end{aligned}|k \\  & =⟨2 - 60 t^{5},\,30 t^{4} - 5 t,\,60 t^{3} - 12 t⟩\end{aligned}
$$

Finally,

$$
\begin{aligned}(f\timesg)^{′}(t) & =⟨- 60 t^{5},\,45 t^{4} - 5 t,\,20 t^{3}⟩+⟨2 - 60 t^{5},\,30 t^{4} - 5 t,\,60 t^{3} - 12 t⟩ \\  & =⟨2 - 120 t^{5},\,75 t^{4} - 10 t,\,80 t^{3} - 12 t⟩\end{aligned}
$$

### Generated variant — authored bank, seed 102

Parameters: `{"a": 2, "b": 6, "c": 5, "d": 3, "e": 2, "h": 5, "n": 3, "p": 2, "q": 3}`. Complete profile `cross_monomials_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated hard — cross_monomials

Find $(f\timesg)^{′}(t)$ given that

$$
\begin{aligned}f(t) & =⟨2 t,\,6,\,5 t^{3}⟩ \\ g(t) & =⟨3 t^{2},\,2 t^{3},\,5 t⟩\end{aligned}
$$

- A. $⟨- 30 t^{5},\,45 t^{4} - 10 t,\,4 t^{3}⟩$
- B. $⟨30 - 60 t^{5},\,75 t^{4} - 20 t,\,16 t^{3} - 36 t⟩$ **correct**
- C. $⟨30 - 60 t^{5},\,- 75 t^{4} + 20 t,\,16 t^{3} - 36 t⟩$
- D. $⟨60 t^{5} - 30,\,- 75 t^{4} + 20 t,\,- 16 t^{3} + 36 t⟩$
- E. $⟨30 - 30 t^{5},\,30 t^{4} - 10 t,\,12 t (t^{2} - 3)⟩$

Using the cross product rule, we can write:

$$
(f\timesg)^{′}(t)={f}^{′}(t)\timesg(t)+f(t)\times{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 t),\,\frac{\text{d}}{\text{d}t}(6),\,\frac{\text{d}}{\text{d}t}(5 t^{3})⟩ \\  & =⟨2,\,0,\,15 t^{2}⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(3 t^{2}),\,\frac{\text{d}}{\text{d}t}(2 t^{3}),\,\frac{\text{d}}{\text{d}t}(5 t)⟩ \\  & =⟨6 t,\,6 t^{2},\,5⟩\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}{f}^{′}(t)\timesg(t) & =|\begin{aligned}i & j & k \\ 2 & 0 & 15 t^{2} \\ 3 t^{2} & 2 t^{3} & 5 t\end{aligned}| \\  & =|\begin{aligned}0 & 15 t^{2} \\ 2 t^{3} & 5 t\end{aligned}|i-|\begin{aligned}2 & 15 t^{2} \\ 3 t^{2} & 5 t\end{aligned}|j+|\begin{aligned}2 & 0 \\ 3 t^{2} & 2 t^{3}\end{aligned}|k \\  & =⟨- 30 t^{5},\,45 t^{4} - 10 t,\,4 t^{3}⟩ \\ f(t)\times{g}^{′}(t) & =|\begin{aligned}i & j & k \\ 2 t & 6 & 5 t^{3} \\ 6 t & 6 t^{2} & 5\end{aligned}| \\  & =|\begin{aligned}6 & 5 t^{3} \\ 6 t^{2} & 5\end{aligned}|i-|\begin{aligned}2 t & 5 t^{3} \\ 6 t & 5\end{aligned}|j+|\begin{aligned}2 t & 6 \\ 6 t & 6 t^{2}\end{aligned}|k \\  & =⟨30 - 30 t^{5},\,30 t^{4} - 10 t,\,12 t (t^{2} - 3)⟩\end{aligned}
$$

Finally,

$$
\begin{aligned}(f\timesg)^{′}(t) & =⟨- 30 t^{5},\,45 t^{4} - 10 t,\,4 t^{3}⟩+⟨30 - 30 t^{5},\,30 t^{4} - 10 t,\,12 t (t^{2} - 3)⟩ \\  & =⟨30 - 60 t^{5},\,75 t^{4} - 20 t,\,16 t^{3} - 36 t⟩\end{aligned}
$$

## Original — q-32347 / cross_shifted

Find $(f\times g)^{′}(t)$ given that

$$
\begin{aligned}f(t) & =⟨6{t}^{2},\,2t,\,6⟩ \\ g(t) & =⟨3,\,3{t}^{2},\,4t-1⟩\end{aligned}
$$

Captured bank 0

- $⟨20t-2,\,36{t}^{2}+12t,\,72{t}^{3}⟩$
- $⟨8t-2,\,-48{t}^{2}+12t,\,36{t}^{3}-6⟩$
- $⟨48t-2,\,-362{t}^{2}+12t,\,6⟩$
- $⟨-28t,\,-24{t}^{2},\,36{t}^{3}⟩$
- $⟨-20t-2,\,-72{t}^{2}+12t,\,72{t}^{3}-6⟩$ **source correct**

Using the cross product rule, we can write:

$$
(f\times g)^{′}(t)={f}^{′}(t)\times g(t)+f(t)\times {g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(6{t}^{2}),\,\frac{\text{d}}{\text{d}t}(2t),\,\frac{\text{d}}{\text{d}t}(6)⟩ \\  & =⟨12t,\,2,\,0⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(3),\,\frac{\text{d}}{\text{d}t}(3{t}^{2}),\,\frac{\text{d}}{\text{d}t}(4t-1)⟩ \\  & =⟨0,\,6t,\,4⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{f}^{′}(t)\times g(t) & =|\begin{aligned}i & j & k \\ 12t & 2 & 0 \\ 3 & 3{t}^{2} & (4t-1)\end{aligned}| \\  & =|\begin{aligned}2 & 0 \\ 3{t}^{2} & (4t-1)\end{aligned}|i-|\begin{aligned}12t & 0 \\ 3 & (4t-1)\end{aligned}|j+|\begin{aligned}12t & 2 \\ 3 & 3{t}^{2}\end{aligned}|k \\  & =⟨8t-2,\,12t-48{t}^{2},\,36{t}^{3}-6⟩ \\ f(t)\times {g}^{′}(t) & =|\begin{aligned}i & j & k \\ 6{t}^{2} & 2t & 6 \\ 0 & 6t & 4\end{aligned}| \\  & =|\begin{aligned}2t & 6 \\ 6t & 4\end{aligned}|i-|\begin{aligned}6{t}^{2} & 6 \\ 0 & 4\end{aligned}|j+|\begin{aligned}6{t}^{2} & 2t \\ 0 & 6t\end{aligned}|k \\  & =⟨-28t,\,-24{t}^{2},\,36{t}^{3}⟩\end{aligned}
$$

Finally,

$$
\begin{aligned}(f\times g)^{′}(t) & =⟨8t-2,\,12t-48{t}^{2},\,36{t}^{3}-6⟩+⟨-28t,\,-24{t}^{2},\,36{t}^{3}⟩ \\  & =⟨-20t-2,\,-72{t}^{2}+12t,\,72{t}^{3}-6⟩\end{aligned}
$$

### Generated variant — observed bank, seed 101

Parameters: `{"a": 5, "b": 2, "c": 5, "d": 3, "e": 4, "h": 1, "k": 6}`. Complete profile `cross_shifted_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated hard — cross_shifted

Find $(f\timesg)^{′}(t)$ given that

$$
\begin{aligned}f(t) & =⟨5 t^{2},\,2 t,\,5⟩ \\ g(t) & =⟨3,\,4 t^{2},\,t - 6⟩\end{aligned}
$$

- A. $⟨10 t - 12,\,6 t (10 - 67 t),\,6⟩$
- B. $⟨- 36 t - 12,\,15 t (4 - t),\,80 t^{3} - 6⟩$ **correct**
- C. $⟨2 t - 12,\,10 t (6 - t),\,40 t^{3} - 6⟩$
- D. $⟨5 t - 12,\,20 t (2 t + 3),\,80 t^{3}⟩$
- E. $⟨- 38 t,\,- 5 t^{2},\,40 t^{3}⟩$

Using the cross product rule, we can write:

$$
(f\timesg)^{′}(t)={f}^{′}(t)\timesg(t)+f(t)\times{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(5 t^{2}),\,\frac{\text{d}}{\text{d}t}(2 t),\,\frac{\text{d}}{\text{d}t}(5)⟩ \\  & =⟨10 t,\,2,\,0⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(3),\,\frac{\text{d}}{\text{d}t}(4 t^{2}),\,\frac{\text{d}}{\text{d}t}(t - 6)⟩ \\  & =⟨0,\,8 t,\,1⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{f}^{′}(t)\timesg(t) & =|\begin{aligned}i & j & k \\ 10 t & 2 & 0 \\ 3 & 4 t^{2} & t - 6\end{aligned}| \\  & =|\begin{aligned}2 & 0 \\ 4 t^{2} & t - 6\end{aligned}|i-|\begin{aligned}10 t & 0 \\ 3 & t - 6\end{aligned}|j+|\begin{aligned}10 t & 2 \\ 3 & 4 t^{2}\end{aligned}|k \\  & =⟨2 t - 12,\,10 t (6 - t),\,40 t^{3} - 6⟩ \\ f(t)\times{g}^{′}(t) & =|\begin{aligned}i & j & k \\ 5 t^{2} & 2 t & 5 \\ 0 & 8 t & 1\end{aligned}| \\  & =|\begin{aligned}2 t & 5 \\ 8 t & 1\end{aligned}|i-|\begin{aligned}5 t^{2} & 5 \\ 0 & 1\end{aligned}|j+|\begin{aligned}5 t^{2} & 2 t \\ 0 & 8 t\end{aligned}|k \\  & =⟨- 38 t,\,- 5 t^{2},\,40 t^{3}⟩\end{aligned}
$$

Finally,

$$
\begin{aligned}(f\timesg)^{′}(t) & =⟨2 t - 12,\,10 t (6 - t),\,40 t^{3} - 6⟩+⟨- 38 t,\,- 5 t^{2},\,40 t^{3}⟩ \\  & =⟨- 36 t - 12,\,15 t (4 - t),\,80 t^{3} - 6⟩\end{aligned}
$$

### Generated variant — observed bank, seed 102

Parameters: `{"a": 2, "b": 6, "c": 5, "d": 3, "e": 2, "h": 5, "k": 6}`. Complete profile `cross_shifted_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated hard — cross_shifted

Find $(f\timesg)^{′}(t)$ given that

$$
\begin{aligned}f(t) & =⟨2 t^{2},\,6 t,\,5⟩ \\ g(t) & =⟨3,\,2 t^{2},\,5 t - 6⟩\end{aligned}
$$

- A. $⟨40 t - 36,\,6 t (4 - 5 t),\,16 t^{3} - 18⟩$ **correct**
- B. $⟨30 t - 36,\,4 t (6 - 5 t),\,8 t^{3} - 18⟩$
- C. $⟨20 t - 36,\,2 t (12 - 43 t),\,18⟩$
- D. $⟨65 t - 36,\,8 t (t + 3),\,16 t^{3}⟩$
- E. $⟨10 t,\,- 10 t^{2},\,8 t^{3}⟩$

Using the cross product rule, we can write:

$$
(f\timesg)^{′}(t)={f}^{′}(t)\timesg(t)+f(t)\times{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 t^{2}),\,\frac{\text{d}}{\text{d}t}(6 t),\,\frac{\text{d}}{\text{d}t}(5)⟩ \\  & =⟨4 t,\,6,\,0⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(3),\,\frac{\text{d}}{\text{d}t}(2 t^{2}),\,\frac{\text{d}}{\text{d}t}(5 t - 6)⟩ \\  & =⟨0,\,4 t,\,5⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{f}^{′}(t)\timesg(t) & =|\begin{aligned}i & j & k \\ 4 t & 6 & 0 \\ 3 & 2 t^{2} & 5 t - 6\end{aligned}| \\  & =|\begin{aligned}6 & 0 \\ 2 t^{2} & 5 t - 6\end{aligned}|i-|\begin{aligned}4 t & 0 \\ 3 & 5 t - 6\end{aligned}|j+|\begin{aligned}4 t & 6 \\ 3 & 2 t^{2}\end{aligned}|k \\  & =⟨30 t - 36,\,4 t (6 - 5 t),\,8 t^{3} - 18⟩ \\ f(t)\times{g}^{′}(t) & =|\begin{aligned}i & j & k \\ 2 t^{2} & 6 t & 5 \\ 0 & 4 t & 5\end{aligned}| \\  & =|\begin{aligned}6 t & 5 \\ 4 t & 5\end{aligned}|i-|\begin{aligned}2 t^{2} & 5 \\ 0 & 5\end{aligned}|j+|\begin{aligned}2 t^{2} & 6 t \\ 0 & 4 t\end{aligned}|k \\  & =⟨10 t,\,- 10 t^{2},\,8 t^{3}⟩\end{aligned}
$$

Finally,

$$
\begin{aligned}(f\timesg)^{′}(t) & =⟨30 t - 36,\,4 t (6 - 5 t),\,8 t^{3} - 18⟩+⟨10 t,\,- 10 t^{2},\,8 t^{3}⟩ \\  & =⟨40 t - 36,\,6 t (4 - 5 t),\,16 t^{3} - 18⟩\end{aligned}
$$

### Generated variant — authored bank, seed 101

Parameters: `{"a": 5, "b": 2, "c": 5, "d": 3, "e": 4, "h": 1, "k": 6}`. Complete profile `cross_shifted_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated hard — cross_shifted

Find $(f\timesg)^{′}(t)$ given that

$$
\begin{aligned}f(t) & =⟨5 t^{2},\,2 t,\,5⟩ \\ g(t) & =⟨3,\,4 t^{2},\,t - 6⟩\end{aligned}
$$

- A. $⟨36 t + 12,\,15 t (t - 4),\,6 - 80 t^{3}⟩$
- B. $⟨- 36 t - 12,\,15 t (4 - t),\,80 t^{3} - 6⟩$ **correct**
- C. $⟨- 38 t,\,- 5 t^{2},\,40 t^{3}⟩$
- D. $⟨2 t - 12,\,10 t (6 - t),\,40 t^{3} - 6⟩$
- E. $⟨- 36 t - 12,\,15 t (t - 4),\,80 t^{3} - 6⟩$

Using the cross product rule, we can write:

$$
(f\timesg)^{′}(t)={f}^{′}(t)\timesg(t)+f(t)\times{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(5 t^{2}),\,\frac{\text{d}}{\text{d}t}(2 t),\,\frac{\text{d}}{\text{d}t}(5)⟩ \\  & =⟨10 t,\,2,\,0⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(3),\,\frac{\text{d}}{\text{d}t}(4 t^{2}),\,\frac{\text{d}}{\text{d}t}(t - 6)⟩ \\  & =⟨0,\,8 t,\,1⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{f}^{′}(t)\timesg(t) & =|\begin{aligned}i & j & k \\ 10 t & 2 & 0 \\ 3 & 4 t^{2} & t - 6\end{aligned}| \\  & =|\begin{aligned}2 & 0 \\ 4 t^{2} & t - 6\end{aligned}|i-|\begin{aligned}10 t & 0 \\ 3 & t - 6\end{aligned}|j+|\begin{aligned}10 t & 2 \\ 3 & 4 t^{2}\end{aligned}|k \\  & =⟨2 t - 12,\,10 t (6 - t),\,40 t^{3} - 6⟩ \\ f(t)\times{g}^{′}(t) & =|\begin{aligned}i & j & k \\ 5 t^{2} & 2 t & 5 \\ 0 & 8 t & 1\end{aligned}| \\  & =|\begin{aligned}2 t & 5 \\ 8 t & 1\end{aligned}|i-|\begin{aligned}5 t^{2} & 5 \\ 0 & 1\end{aligned}|j+|\begin{aligned}5 t^{2} & 2 t \\ 0 & 8 t\end{aligned}|k \\  & =⟨- 38 t,\,- 5 t^{2},\,40 t^{3}⟩\end{aligned}
$$

Finally,

$$
\begin{aligned}(f\timesg)^{′}(t) & =⟨2 t - 12,\,10 t (6 - t),\,40 t^{3} - 6⟩+⟨- 38 t,\,- 5 t^{2},\,40 t^{3}⟩ \\  & =⟨- 36 t - 12,\,15 t (4 - t),\,80 t^{3} - 6⟩\end{aligned}
$$

### Generated variant — authored bank, seed 102

Parameters: `{"a": 2, "b": 6, "c": 5, "d": 3, "e": 2, "h": 5, "k": 6}`. Complete profile `cross_shifted_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated hard — cross_shifted

Find $(f\timesg)^{′}(t)$ given that

$$
\begin{aligned}f(t) & =⟨2 t^{2},\,6 t,\,5⟩ \\ g(t) & =⟨3,\,2 t^{2},\,5 t - 6⟩\end{aligned}
$$

- A. $⟨40 t - 36,\,6 t (4 - 5 t),\,16 t^{3} - 18⟩$ **correct**
- B. $⟨10 t,\,- 10 t^{2},\,8 t^{3}⟩$
- C. $⟨36 - 40 t,\,6 t (5 t - 4),\,18 - 16 t^{3}⟩$
- D. $⟨30 t - 36,\,4 t (6 - 5 t),\,8 t^{3} - 18⟩$
- E. $⟨40 t - 36,\,6 t (5 t - 4),\,16 t^{3} - 18⟩$

Using the cross product rule, we can write:

$$
(f\timesg)^{′}(t)={f}^{′}(t)\timesg(t)+f(t)\times{g}^{′}(t)
$$

Let's now find the derivatives of each function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 t^{2}),\,\frac{\text{d}}{\text{d}t}(6 t),\,\frac{\text{d}}{\text{d}t}(5)⟩ \\  & =⟨4 t,\,6,\,0⟩ \\ {g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(3),\,\frac{\text{d}}{\text{d}t}(2 t^{2}),\,\frac{\text{d}}{\text{d}t}(5 t - 6)⟩ \\  & =⟨0,\,4 t,\,5⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{f}^{′}(t)\timesg(t) & =|\begin{aligned}i & j & k \\ 4 t & 6 & 0 \\ 3 & 2 t^{2} & 5 t - 6\end{aligned}| \\  & =|\begin{aligned}6 & 0 \\ 2 t^{2} & 5 t - 6\end{aligned}|i-|\begin{aligned}4 t & 0 \\ 3 & 5 t - 6\end{aligned}|j+|\begin{aligned}4 t & 6 \\ 3 & 2 t^{2}\end{aligned}|k \\  & =⟨30 t - 36,\,4 t (6 - 5 t),\,8 t^{3} - 18⟩ \\ f(t)\times{g}^{′}(t) & =|\begin{aligned}i & j & k \\ 2 t^{2} & 6 t & 5 \\ 0 & 4 t & 5\end{aligned}| \\  & =|\begin{aligned}6 t & 5 \\ 4 t & 5\end{aligned}|i-|\begin{aligned}2 t^{2} & 5 \\ 0 & 5\end{aligned}|j+|\begin{aligned}2 t^{2} & 6 t \\ 0 & 4 t\end{aligned}|k \\  & =⟨10 t,\,- 10 t^{2},\,8 t^{3}⟩\end{aligned}
$$

Finally,

$$
\begin{aligned}(f\timesg)^{′}(t) & =⟨30 t - 36,\,4 t (6 - 5 t),\,8 t^{3} - 18⟩+⟨10 t,\,- 10 t^{2},\,8 t^{3}⟩ \\  & =⟨40 t - 36,\,6 t (4 - 5 t),\,16 t^{3} - 18⟩\end{aligned}
$$

## Original — q-32836 / cross_self

Given $f(t)=⟨1-{t}^{2}\,,\,1-{t}^{3}\,,\,1-t⟩$, find $({f}^{′}\times f)^{′}(t).$

Captured bank 0

- $⟨-6t+6{t}^{2}\,,\,2-2t\,,\,-2+8{t}^{3}⟩$
- $⟨0\,,\,0\,,\,-2+6t-4{t}^{3}⟩$
- $⟨-6t+6{t}^{2}\,,\,2-2t\,,\,-2+6t-4{t}^{3}⟩$ **source correct**
- $⟨-6t+6{t}^{2}\,,\,-2+2t\,,\,-6t+8{t}^{3}⟩$
- $⟨-6+6{t}^{2}\,,\,-2t\,,\,-2+6t-4{t}^{3}⟩$

Using the cross product rule, we can write:

$$
({f}^{′}\times f)^{′}(t)={f}^{″}(t)\times f(t)+{f}^{′}(t)\times {f}^{′}(t)
$$

Let's now find the first and second derivative of the function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(1-{t}^{2})\,,\,\frac{\text{d}}{\text{d}t}(1-{t}^{3})\,,\,\frac{\text{d}}{\text{d}t}(1-t)⟩ \\  & =⟨-2t\,,\,-3{t}^{2}\,,\,-1⟩ \\ {f}^{″}(t) & =⟨\frac{\text{d}}{\text{d}t}(-2t)\,,\,\frac{\text{d}}{\text{d}t}(-3{t}^{2})\,,\,\frac{\text{d}}{\text{d}t}(-1)⟩ \\  & =⟨-2\,,\,-6t\,,\,0⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{f}^{″}(t)\times f(t) & =|\begin{aligned}i & j & k \\ -2 & -6t & 0 \\ 1-{t}^{2} & 1-{t}^{3} & 1-t\end{aligned}| \\  & =|\begin{aligned}-6t & 0 \\ 1-{t}^{3} & 1-t\end{aligned}|i-|\begin{aligned}-2 & 0 \\ 1-{t}^{2} & 1-t\end{aligned}|j+|\begin{aligned}-2 & -6t \\ 1-{t}^{2} & 1-{t}^{3}\end{aligned}|k \\  & =⟨-6t+6{t}^{2}\,,\,2-2t\,,\,-2+6t-4{t}^{3}⟩ \\ {f}^{′}(t)\times {f}^{′}(t) & =|\begin{aligned}i & j & k \\ -2t & -3{t}^{2} & -1 \\ -2t & -3{t}^{2} & -1\end{aligned}| \\  & =|\begin{aligned}-3{t}^{2} & -1 \\ -3{t}^{2} & -1\end{aligned}|i-|\begin{aligned}-2t & -1 \\ -2t & -1\end{aligned}|j+|\begin{aligned}-2t & -3{t}^{2} \\ -2t & -3{t}^{2}\end{aligned}|k \\  & =⟨0\,,\,0\,,\,0⟩\end{aligned}
$$

Finally,

$$
\begin{aligned}({f}^{′}\times f)^{′}(t) & =⟨-6t+6{t}^{2}\,,\,2-2t\,,\,-2+6t-4{t}^{3}⟩+⟨0\,,\,0\,,\,0⟩ \\  & =⟨-6t+6{t}^{2}\,,\,2-2t\,,\,-2+6t-4{t}^{3}⟩\end{aligned}
$$

### Generated variant — observed bank, seed 101

Parameters: `{"a": 5, "b": 2, "c": 5, "d": 3, "e": 4, "h": 1}`. Complete profile `cross_self_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated hard — cross_self

Given $f(t)=⟨5 - 2 t^{2},\,5 - 3 t^{3},\,4 - t⟩$, find $({f}^{′}\timesf)^{′}(t).$

- A. $⟨18 t (t - 4),\,4 t - 16,\,48 t^{3} - 90 t⟩$
- B. $⟨18 t (t - 4),\,16 - 4 t,\,- 24 t^{3} + 90 t - 20⟩$ **correct**
- C. $⟨0,\,0,\,- 24 t^{3} + 90 t - 20⟩$
- D. $⟨18 t (t - 4),\,16 - 4 t,\,48 t^{3} - 20⟩$
- E. $⟨18 t^{2} - 72,\,- 4 t,\,- 24 t^{3} + 90 t - 20⟩$

Using the cross product rule, we can write:

$$
({f}^{′}\timesf)^{′}(t)={f}^{″}(t)\timesf(t)+{f}^{′}(t)\times{f}^{′}(t)
$$

Let's now find the first and second derivative of the function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(5 - 2 t^{2}),\,\frac{\text{d}}{\text{d}t}(5 - 3 t^{3}),\,\frac{\text{d}}{\text{d}t}(4 - t)⟩ \\  & =⟨- 4 t,\,- 9 t^{2},\,-1⟩ \\ {f}^{″}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 4 t),\,\frac{\text{d}}{\text{d}t}(- 9 t^{2}),\,\frac{\text{d}}{\text{d}t}(-1)⟩ \\  & =⟨-4,\,- 18 t,\,0⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{f}^{″}(t)\timesf(t) & =|\begin{aligned}i & j & k \\ -4 & - 18 t & 0 \\ 5 - 2 t^{2} & 5 - 3 t^{3} & 4 - t\end{aligned}| \\  & =|\begin{aligned}- 18 t & 0 \\ 5 - 3 t^{3} & 4 - t\end{aligned}|i-|\begin{aligned}-4 & 0 \\ 5 - 2 t^{2} & 4 - t\end{aligned}|j+|\begin{aligned}-4 & - 18 t \\ 5 - 2 t^{2} & 5 - 3 t^{3}\end{aligned}|k \\  & =⟨18 t (t - 4),\,16 - 4 t,\,- 24 t^{3} + 90 t - 20⟩ \\ {f}^{′}(t)\times{f}^{′}(t) & =|\begin{aligned}i & j & k \\ - 4 t & - 9 t^{2} & -1 \\ - 4 t & - 9 t^{2} & -1\end{aligned}| \\  & =|\begin{aligned}- 9 t^{2} & -1 \\ - 9 t^{2} & -1\end{aligned}|i-|\begin{aligned}- 4 t & -1 \\ - 4 t & -1\end{aligned}|j+|\begin{aligned}- 4 t & - 9 t^{2} \\ - 4 t & - 9 t^{2}\end{aligned}|k \\  & =⟨0,\,0,\,0⟩\end{aligned}
$$

Finally,

$$
\begin{aligned}({f}^{′}\timesf)^{′}(t) & =⟨18 t (t - 4),\,16 - 4 t,\,- 24 t^{3} + 90 t - 20⟩+⟨0,\,0,\,0⟩ \\  & =⟨18 t (t - 4),\,16 - 4 t,\,- 24 t^{3} + 90 t - 20⟩\end{aligned}
$$

### Generated variant — observed bank, seed 102

Parameters: `{"a": 2, "b": 6, "c": 5, "d": 3, "e": 2, "h": 5}`. Complete profile `cross_self_observed`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated hard — cross_self

Given $f(t)=⟨2 - 6 t^{2},\,5 - 3 t^{3},\,2 - 5 t⟩$, find $({f}^{′}\timesf)^{′}(t).$

- A. $⟨18 t (5 t - 2),\,24 - 60 t,\,- 72 t^{3} + 36 t - 60⟩$ **correct**
- B. $⟨0,\,0,\,- 72 t^{3} + 36 t - 60⟩$
- C. $⟨18 t (5 t - 2),\,60 t - 24,\,144 t^{3} - 36 t⟩$
- D. $⟨18 t (5 t - 2),\,24 - 60 t,\,144 t^{3} - 60⟩$
- E. $⟨90 t^{2} - 36,\,- 60 t,\,- 72 t^{3} + 36 t - 60⟩$

Using the cross product rule, we can write:

$$
({f}^{′}\timesf)^{′}(t)={f}^{″}(t)\timesf(t)+{f}^{′}(t)\times{f}^{′}(t)
$$

Let's now find the first and second derivative of the function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 - 6 t^{2}),\,\frac{\text{d}}{\text{d}t}(5 - 3 t^{3}),\,\frac{\text{d}}{\text{d}t}(2 - 5 t)⟩ \\  & =⟨- 12 t,\,- 9 t^{2},\,-5⟩ \\ {f}^{″}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 12 t),\,\frac{\text{d}}{\text{d}t}(- 9 t^{2}),\,\frac{\text{d}}{\text{d}t}(-5)⟩ \\  & =⟨-12,\,- 18 t,\,0⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{f}^{″}(t)\timesf(t) & =|\begin{aligned}i & j & k \\ -12 & - 18 t & 0 \\ 2 - 6 t^{2} & 5 - 3 t^{3} & 2 - 5 t\end{aligned}| \\  & =|\begin{aligned}- 18 t & 0 \\ 5 - 3 t^{3} & 2 - 5 t\end{aligned}|i-|\begin{aligned}-12 & 0 \\ 2 - 6 t^{2} & 2 - 5 t\end{aligned}|j+|\begin{aligned}-12 & - 18 t \\ 2 - 6 t^{2} & 5 - 3 t^{3}\end{aligned}|k \\  & =⟨18 t (5 t - 2),\,24 - 60 t,\,- 72 t^{3} + 36 t - 60⟩ \\ {f}^{′}(t)\times{f}^{′}(t) & =|\begin{aligned}i & j & k \\ - 12 t & - 9 t^{2} & -5 \\ - 12 t & - 9 t^{2} & -5\end{aligned}| \\  & =|\begin{aligned}- 9 t^{2} & -5 \\ - 9 t^{2} & -5\end{aligned}|i-|\begin{aligned}- 12 t & -5 \\ - 12 t & -5\end{aligned}|j+|\begin{aligned}- 12 t & - 9 t^{2} \\ - 12 t & - 9 t^{2}\end{aligned}|k \\  & =⟨0,\,0,\,0⟩\end{aligned}
$$

Finally,

$$
\begin{aligned}({f}^{′}\timesf)^{′}(t) & =⟨18 t (5 t - 2),\,24 - 60 t,\,- 72 t^{3} + 36 t - 60⟩+⟨0,\,0,\,0⟩ \\  & =⟨18 t (5 t - 2),\,24 - 60 t,\,- 72 t^{3} + 36 t - 60⟩\end{aligned}
$$

### Generated variant — authored bank, seed 101

Parameters: `{"a": 5, "b": 2, "c": 5, "d": 3, "e": 4, "h": 1}`. Complete profile `cross_self_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated hard — cross_self

Given $f(t)=⟨5 - 2 t^{2},\,5 - 3 t^{3},\,4 - t⟩$, find $({f}^{′}\timesf)^{′}(t).$

- A. $⟨18 t (t - 4),\,4 t - 16,\,- 24 t^{3} + 90 t - 20⟩$
- B. $⟨18 t (t - 4),\,16 - 4 t,\,- 24 t^{3} + 90 t - 20⟩$ **correct**
- C. $⟨18 t (4 - t),\,4 t - 16,\,24 t^{3} - 90 t + 20⟩$
- D. $⟨0,\,0,\,0⟩$
- E. $⟨18 t,\,-4,\,- 36 t^{2}⟩$

Using the cross product rule, we can write:

$$
({f}^{′}\timesf)^{′}(t)={f}^{″}(t)\timesf(t)+{f}^{′}(t)\times{f}^{′}(t)
$$

Let's now find the first and second derivative of the function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(5 - 2 t^{2}),\,\frac{\text{d}}{\text{d}t}(5 - 3 t^{3}),\,\frac{\text{d}}{\text{d}t}(4 - t)⟩ \\  & =⟨- 4 t,\,- 9 t^{2},\,-1⟩ \\ {f}^{″}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 4 t),\,\frac{\text{d}}{\text{d}t}(- 9 t^{2}),\,\frac{\text{d}}{\text{d}t}(-1)⟩ \\  & =⟨-4,\,- 18 t,\,0⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{f}^{″}(t)\timesf(t) & =|\begin{aligned}i & j & k \\ -4 & - 18 t & 0 \\ 5 - 2 t^{2} & 5 - 3 t^{3} & 4 - t\end{aligned}| \\  & =|\begin{aligned}- 18 t & 0 \\ 5 - 3 t^{3} & 4 - t\end{aligned}|i-|\begin{aligned}-4 & 0 \\ 5 - 2 t^{2} & 4 - t\end{aligned}|j+|\begin{aligned}-4 & - 18 t \\ 5 - 2 t^{2} & 5 - 3 t^{3}\end{aligned}|k \\  & =⟨18 t (t - 4),\,16 - 4 t,\,- 24 t^{3} + 90 t - 20⟩ \\ {f}^{′}(t)\times{f}^{′}(t) & =|\begin{aligned}i & j & k \\ - 4 t & - 9 t^{2} & -1 \\ - 4 t & - 9 t^{2} & -1\end{aligned}| \\  & =|\begin{aligned}- 9 t^{2} & -1 \\ - 9 t^{2} & -1\end{aligned}|i-|\begin{aligned}- 4 t & -1 \\ - 4 t & -1\end{aligned}|j+|\begin{aligned}- 4 t & - 9 t^{2} \\ - 4 t & - 9 t^{2}\end{aligned}|k \\  & =⟨0,\,0,\,0⟩\end{aligned}
$$

Finally,

$$
\begin{aligned}({f}^{′}\timesf)^{′}(t) & =⟨18 t (t - 4),\,16 - 4 t,\,- 24 t^{3} + 90 t - 20⟩+⟨0,\,0,\,0⟩ \\  & =⟨18 t (t - 4),\,16 - 4 t,\,- 24 t^{3} + 90 t - 20⟩\end{aligned}
$$

### Generated variant — authored bank, seed 102

Parameters: `{"a": 2, "b": 6, "c": 5, "d": 3, "e": 2, "h": 5}`. Complete profile `cross_self_authored`. The authored profile is the learner-generation default; observed profile variants retain their inferred pattern for source replay review.

## Generated hard — cross_self

Given $f(t)=⟨2 - 6 t^{2},\,5 - 3 t^{3},\,2 - 5 t⟩$, find $({f}^{′}\timesf)^{′}(t).$

- A. $⟨18 t (5 t - 2),\,24 - 60 t,\,- 72 t^{3} + 36 t - 60⟩$ **correct**
- B. $⟨18 t (2 - 5 t),\,60 t - 24,\,72 t^{3} - 36 t + 60⟩$
- C. $⟨18 t (5 t - 2),\,60 t - 24,\,- 72 t^{3} + 36 t - 60⟩$
- D. $⟨0,\,0,\,0⟩$
- E. $⟨90 t,\,-60,\,- 108 t^{2}⟩$

Using the cross product rule, we can write:

$$
({f}^{′}\timesf)^{′}(t)={f}^{″}(t)\timesf(t)+{f}^{′}(t)\times{f}^{′}(t)
$$

Let's now find the first and second derivative of the function.

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(2 - 6 t^{2}),\,\frac{\text{d}}{\text{d}t}(5 - 3 t^{3}),\,\frac{\text{d}}{\text{d}t}(2 - 5 t)⟩ \\  & =⟨- 12 t,\,- 9 t^{2},\,-5⟩ \\ {f}^{″}(t) & =⟨\frac{\text{d}}{\text{d}t}(- 12 t),\,\frac{\text{d}}{\text{d}t}(- 9 t^{2}),\,\frac{\text{d}}{\text{d}t}(-5)⟩ \\  & =⟨-12,\,- 18 t,\,0⟩\end{aligned}
$$

Therefore, we obtain:

$$
\begin{aligned}{f}^{″}(t)\timesf(t) & =|\begin{aligned}i & j & k \\ -12 & - 18 t & 0 \\ 2 - 6 t^{2} & 5 - 3 t^{3} & 2 - 5 t\end{aligned}| \\  & =|\begin{aligned}- 18 t & 0 \\ 5 - 3 t^{3} & 2 - 5 t\end{aligned}|i-|\begin{aligned}-12 & 0 \\ 2 - 6 t^{2} & 2 - 5 t\end{aligned}|j+|\begin{aligned}-12 & - 18 t \\ 2 - 6 t^{2} & 5 - 3 t^{3}\end{aligned}|k \\  & =⟨18 t (5 t - 2),\,24 - 60 t,\,- 72 t^{3} + 36 t - 60⟩ \\ {f}^{′}(t)\times{f}^{′}(t) & =|\begin{aligned}i & j & k \\ - 12 t & - 9 t^{2} & -5 \\ - 12 t & - 9 t^{2} & -5\end{aligned}| \\  & =|\begin{aligned}- 9 t^{2} & -5 \\ - 9 t^{2} & -5\end{aligned}|i-|\begin{aligned}- 12 t & -5 \\ - 12 t & -5\end{aligned}|j+|\begin{aligned}- 12 t & - 9 t^{2} \\ - 12 t & - 9 t^{2}\end{aligned}|k \\  & =⟨0,\,0,\,0⟩\end{aligned}
$$

Finally,

$$
\begin{aligned}({f}^{′}\timesf)^{′}(t) & =⟨18 t (5 t - 2),\,24 - 60 t,\,- 72 t^{3} + 36 t - 60⟩+⟨0,\,0,\,0⟩ \\  & =⟨18 t (5 t - 2),\,24 - 60 t,\,- 72 t^{3} + 36 t - 60⟩\end{aligned}
$$

