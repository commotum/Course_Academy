# Source evidence at basis 2286

Applying Independence of Parametrization and Orientation


## q-122478

Suppose $\displaystyle \int_{C_{1}}f(x, y)ds = 2$ for some function $f(x, y)$, where $C_{1}$ is parametrized by $r_{1}(t) = ⟨t, t^{2}⟩$ for $0 \le t \le 1$.

Which of the following must be true?

1. $\displaystyle \int_{-C_{1}}f(x, y)ds =-2$
2. $\displaystyle \int_{-C_{1}}f(x, y)ds = 2$
3. $\displaystyle \int_{C_{2}}f(x, y)ds = 4$, where $C_{2}$ is parametrized by $r_{2}(u) = ⟨2u, 4u^{2}⟩$ for $0 \le u \le \frac{1}{2}$.


Worked solution:
Missing


Fields: [{"key": "selection", "type": ":answer-field.type/radio", "choices": ["I and III only", "I only", "III only", "II and III only", "II only"], "correct": null}]


## q-122571

Consider the curves $C_{1}$ and $C_{2}$, defined parametrically as follows:

$\begin{bmatrix}C_{1}:r_{1}(t)|= ⟨\sin t, \cos t⟩, & 0 \le t \le 2π \\ C_{2}:r_{2}(θ)|= ⟨\sin 2θ, \cos 2θ⟩, & 0 \le θ \le π\end{bmatrix}$

Now suppose $\displaystyle \int_{C_{1}}f(x, y)ds = k$ for some function $f(x, y)$ and real number $k$. Which of the following must be true?

1. $\displaystyle \int_{-C_{1}}f(x, y)ds = k$
2. $\displaystyle \int_{C_{2}}f(x, y)ds = k$
3. $\displaystyle \int_{C_{2}}f(x, y)ds = \frac{1}{2}k$


Worked solution:
Missing


Fields: [{"key": "selection", "type": ":answer-field.type/radio", "choices": ["I only", "II only", "II and III only", "I and II only", "I and III only"], "correct": null}]


## q-122814

Suppose ${\int }_{{C}_{1}}f(x,y)\,\text{d}s=4$ for some function $f(x,y),$ where ${C}_{1}$ is parametrized by ${r}_{1}(t)=⟨{t}^{4}-3{t}^{2},\,t⟩$ for $0\le t\le 2.$

Which of the following must be true?
- **I.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=-4$
- **II.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=8,$ where ${C}_{2}$ is parametrized by ${r}_{2}(u)=⟨16{u}^{4}-12{u}^{2},\,2u⟩$ for $0\le u\le 1.$
- **III.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=4$

Select all that apply.


Worked solution:
Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is false, while statement III is true. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=4.
$$

- Statement II is false. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=4.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we can convert each parametrization to Cartesian form. In doing so, we find that both parameterizations give the Cartesian curve

$$
x={y}^{4}-3{y}^{2},\,0\le y\le 2.
$$

Therefore, the correct answer is "III only."


Fields: [{"key": "I", "type": ":answer-field.type/checkbox", "choices": ["false", "true"], "correct": "false"}, {"key": "II", "type": ":answer-field.type/checkbox", "choices": ["false", "true"], "correct": "false"}, {"key": "III", "type": ":answer-field.type/checkbox", "choices": ["false", "true"], "correct": "true"}]


## q-122815

Suppose ${\int }_{{C}_{1}}f(x,y)\,\text{d}s=1$ for some function $f(x,y),$ where ${C}_{1}$ is parametrized by ${r}_{1}(u)=⟨\operatorname{cos}⁡(\frac{u}{2}),\,\operatorname{sin}⁡(\frac{u}{2})⟩$ for $0\le u\le 2\pi .$ 

Which of the following must be true?
- **I.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=2,$ where ${C}_{2}$ is parametrized by ${r}_{2}(t)=⟨\operatorname{cos}⁡t,\,\operatorname{sin}⁡t⟩$ for $0\le t\le \pi .$
- **II.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=-1$
- **III.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=1$

Select all that apply.


Worked solution:
Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is false. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=1.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we note that both parameterizations traverse a half-circle of radius $1$ centered at $O$ between $0$ and $\pi .$

- Statement II is false, while statement III is true. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=1.
$$

Therefore, the correct answer is "III only."


Fields: [{"key": "I", "type": ":answer-field.type/checkbox", "choices": ["false", "true"], "correct": "false"}, {"key": "II", "type": ":answer-field.type/checkbox", "choices": ["false", "true"], "correct": "false"}, {"key": "III", "type": ":answer-field.type/checkbox", "choices": ["false", "true"], "correct": "true"}]


## q-122816

Suppose ${\int }_{{C}_{1}}f(x,y)\,\text{d}s=3$ for some function $f(x,y),$ where ${C}_{1}$ is parametrized by ${r}_{1}(t)=⟨t,\,{t}^{3/2}⟩$ for $0\le t\le 4.$

Which of the following must be true?
- **I.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=3$
- **II.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=-3$
- **III.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=12,$ where ${C}_{2}$ is parametrized by ${r}_{2}(u)=⟨4u,\,8{u}^{3/2}⟩$ for $0\le u\le 1.$

Select all that apply.


Worked solution:
Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is true, while statement II is false. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=3.
$$

- Statement III is false. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=3.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we can convert each parametrization to Cartesian form. In doing so, we find that both parameterizations give the Cartesian curve

$$
y={x}^{3/2},\,0\le x\le 4.
$$

Therefore, the correct answer is "I only."


Fields: [{"key": "I", "type": ":answer-field.type/checkbox", "choices": ["false", "true"], "correct": "true"}, {"key": "II", "type": ":answer-field.type/checkbox", "choices": ["false", "true"], "correct": "false"}, {"key": "III", "type": ":answer-field.type/checkbox", "choices": ["false", "true"], "correct": "false"}]


## q-122851

Consider the curves ${C}_{1}$ and ${C}_{2},$ defined parametrically as follows:

$$
\begin{aligned}{C}_{1}:\,{r}_{1}(t) & =⟨\sqrt{9{t}^{2}+1},\,3t⟩, & 0\le t\le \frac{1}{3} \\ {C}_{2}:\,{r}_{2}(u) & =⟨\sqrt{4{u}^{2}+1},\,2u⟩, & 0\le u\le \frac{1}{2}\end{aligned}
$$

Now suppose ${\int }_{{C}_{1}}f(x,y)\,\text{d}s=k$ for some function $f(x,y)$ and real number $k.$ Which of the following must be true?
- **I.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=-k$
- **II.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=\frac{2k}{3}$
- **III.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=k$

Select all that apply.


Worked solution:
Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is false. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=k.
$$

- Statement II is false, while statement III is true. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=k.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we can convert each parametrization to Cartesian form. In doing so, we find that both parameterizations give the Cartesian curve

$$
x=\sqrt{{y}^{2}+1},\,0\le y\le 1.
$$

Therefore, the correct answer is "III only."


Fields: [{"key": "I", "type": ":answer-field.type/checkbox", "choices": ["false", "true"], "correct": "false"}, {"key": "II", "type": ":answer-field.type/checkbox", "choices": ["false", "true"], "correct": "false"}, {"key": "III", "type": ":answer-field.type/checkbox", "choices": ["false", "true"], "correct": "true"}]


## q-122868

Consider the curves ${C}_{1}$ and ${C}_{2},$ defined parametrically as follows:

$$
\begin{aligned}{C}_{1}:\,{r}_{1}(t) & =⟨2t,\,2\sqrt{t}⟩, & 0\le t\le 2 \\ {C}_{2}:\,{r}_{2}(u) & =⟨4u,\,2\sqrt{2u}⟩, & 0\le u\le 1\end{aligned}
$$

Now suppose ${\int }_{{C}_{1}}f(x,y)\,\text{d}s=k$ for some function $f(x,y)$ and real number $k.$ Which of the following must be true?
- **I.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=k$
- **II.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=2k$
- **III.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=k$

Select all that apply.


Worked solution:
Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is true, while statement II is false. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=k.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we can convert each parametrization to Cartesian form. In doing so, we find that both parameterizations give the Cartesian curve

$$
y=\sqrt{2x},\,0\le x\le 4.
$$

- Statement III is true. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=k.
$$

Therefore, the correct answer is "I and III only."


Fields: [{"key": "I", "type": ":answer-field.type/checkbox", "choices": ["false", "true"], "correct": "true"}, {"key": "II", "type": ":answer-field.type/checkbox", "choices": ["false", "true"], "correct": "false"}, {"key": "III", "type": ":answer-field.type/checkbox", "choices": ["false", "true"], "correct": "true"}]


## e-9472

Consider the curves $C_1$ and $C_2,$ defined parametrically as follows:

$$
\begin{aligned}{C}_{1}:\,{r}_{1}(t) & =⟨\frac{1}{9}{t}^{3},\,t⟩, & 0\le t\le 3 \\ {C}_{2}:\,{r}_{2}(u) & =⟨3{u}^{3},\,3u⟩, & 0\le u\le 1\end{aligned}
$$

Now suppose $\displaystyle\int_{C_1} f(x,y)\,\textrm ds = k$ for some function $f(x,y)$ and real number $k.$ Which of the following must be true?

- $\displaystyle\int_{C_2} f(x,y)\,\textrm ds = 3k$

- $\displaystyle\int_{C_2} f(x,y)\,\textrm ds = k$

- $\displaystyle\int_{-C_1} f(x,y)\,\textrm ds = k$


Worked solution:
Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is false, while statement II is true. Notice that $C_1$ and $C_2$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
\int_{C_2} f(x,y)\,\textrm ds = k.
$$

 
To see that $C_1$ and $C_2$ represent the same curve, we can convert each parametrization to Cartesian form. In doing so, we find that both parameterizations give the Cartesian curve

$$
x = \dfrac{1}{9}y^3, \quad 0\leq y\leq 3.
$$

- Statement III is true. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
\int_{-C_1} f(x,y)\,\textrm ds  = \int_{C_1} f(x,y)\,\textrm ds = k.
$$

Therefore, the correct answer is "II and III only."


Fields: []