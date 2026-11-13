# 17592186048459 Introduction to Linear Transformations

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186088928 — Introduction

Consider the function $f(x),$ defined as

$$
f(x) = 2x+1.
$$

This function $f$ takes a real number $x$ as input, and it outputs a real number. We can describe this fact using the following notation:

$$
f: x \longrightarrow 2x+1
$$

Similarly, we can define a function $\mathbf T,$ also called a **transformation** or a **map**, that takes a 2D-vector (or 3D-vector) as input and outputs a new 2D-vector (or, respectively, 3D-vector). 

For example, let's consider the following transformation: 

$$
\mathbf{T}: \begin{bmatrix}x \\ y\end{bmatrix} \longrightarrow \begin{bmatrix}x+y \\ 2y\end{bmatrix}
$$

This means that for any 2D-vector $\begin{bmatrix}x \\ y\end{bmatrix}$ the corresponding image $\mathbf{T}\begin{bmatrix}x \\ y\end{bmatrix}$ under the action of $\mathbf{T}$ can be found as follows:

$$
\mathbf{T}\begin{bmatrix}x \\ y\end{bmatrix} = \begin{bmatrix}x+y \\ 2y\end{bmatrix}
$$

We can evaluate this transformation just like we would with any other function. For example, applying the transformation $\mathbf{T}$ to the input vector 
$$
\begin{bmatrix}x \\ y\end{bmatrix} = \begin{bmatrix}-1 \\ 3\end{bmatrix},
$$
we get

$$
\begin{aligned}T\begin{bmatrix}-1 \\ 3\end{bmatrix}=\begin{bmatrix}-1+3 \\ 2\cdot 3\end{bmatrix}=\begin{bmatrix}2 \\ 6\end{bmatrix}.\end{aligned}
$$

We say that the transformation $\mathbf T$ *maps* the input vector $\begin{bmatrix}-1 \\ 3\end{bmatrix}$ to the output vector $\begin{bmatrix}2 \\ 6\end{bmatrix}$



### tutorial 17592186088940 — Linear Transformations

A transformation $\mathbf{T}$ is called a **linear transformation** (or **linear map**) if the following two properties are satisfied:

- $\mathbf{T}(k\mathbf{v})=k\mathbf{T}(\mathbf{v})$ for any vector $\mathbf{v}$ and any scalar $k$

- $\mathbf{T}(\mathbf{v}_1+\mathbf{v}_2)=\mathbf{T}(\mathbf{v}_1)+\mathbf{T}(\mathbf{v}_2)$ for any vectors $\mathbf{v}_1$ and $\mathbf{v}_2$

If we let $\mathbf{v}=\begin{bmatrix}x \\ y\end{bmatrix},$ $\mathbf{v}_1=\begin{bmatrix}{x}_{1} \\ {y}_{1}\end{bmatrix},$ $\mathbf{v}_2=\begin{bmatrix}{x}_{2} \\ {y}_{2}\end{bmatrix},$ then the conditions above can be written as follows:

- $\mathbf{T}\begin{bmatrix}kx \\ ky\end{bmatrix} = k
\mathbf{T} \begin{bmatrix}x \\ y\end{bmatrix}$

- $\mathbf{T}\begin{bmatrix}{x}_{1}+{x}_{2} \\ {y}_{1}+{y}_{2}\end{bmatrix} = \mathbf{T}
\begin{bmatrix}{x}_{1} \\ {y}_{1}\end{bmatrix} + \mathbf{T} \begin{bmatrix}{x}_{2} \\ {y}_{2}\end{bmatrix}$

We can determine whether the transformation $\mathbf{T}: \begin{bmatrix}x \\ y\end{bmatrix} \rightarrow \begin{bmatrix}x+y \\ 2y\end{bmatrix}$ is linear by checking if these two conditions are true.

- Checking the first condition, we have

$$
\begin{aligned}T\begin{bmatrix}kx \\ ky\end{bmatrix} & =\begin{bmatrix}(kx)+(ky) \\ 2(ky)\end{bmatrix} \\  & =\begin{bmatrix}k(x+y) \\ k(2y)\end{bmatrix} \\  & =k\begin{bmatrix}x+y \\ 2y\end{bmatrix} \\  & =kT\begin{bmatrix}x \\ y\end{bmatrix}.\,✓\end{aligned}
$$

- Checking the second condition, we have

$$
\begin{aligned}T\begin{bmatrix}{x}_{1}+{x}_{2} \\ {y}_{1}+{y}_{2}\end{bmatrix} & =\begin{bmatrix}({x}_{1}+{x}_{2})+({y}_{1}+{y}_{2}) \\ 2({y}_{1}+{y}_{2})\end{bmatrix} \\  & =\begin{bmatrix}({x}_{1}+{y}_{1})+({x}_{2}+{y}_{2}) \\ 2{y}_{1}+2{y}_{2}\end{bmatrix} \\  & =\begin{bmatrix}{x}_{1}+{y}_{1} \\ 2{y}_{1}\end{bmatrix}+\begin{bmatrix}{x}_{2}+{y}_{2} \\ 2{y}_{2}\end{bmatrix} \\  & =T\begin{bmatrix}{x}_{1} \\ {y}_{1}\end{bmatrix}+T\begin{bmatrix}{x}_{2} \\ {y}_{2}\end{bmatrix}.\,✓\end{aligned}
$$

Both conditions are satisfied, so this transformation is linear.



### example 17592186087563 — Determining the Image of a Vector Under a Map Using the Scalar Multiplication Property

If $\mathbf{T}$ is a linear transformation and $$
\mathbf{T}\left(\begin{bmatrix}12 \\ 24\end{bmatrix}\right)=\begin{bmatrix}18 \\ -30\end{bmatrix},
$$ then find $\mathbf{T}\left(\begin{bmatrix}2 \\ 4\end{bmatrix}\right).$

Since $\mathbf{T}$ is a linear transformation, it must satisfy $\mathbf{T}(k\mathbf{v})=k\mathbf{T}(\mathbf{v}).$ Noting that $\begin{bmatrix}12 \\ 24\end{bmatrix}=6\begin{bmatrix}2 \\ 4\end{bmatrix},$ we have

$$
\begin{aligned}\mathbf{T}\left(\begin{bmatrix}12 \\ 24\end{bmatrix}\right) & =\mathbf{T}\left(6\begin{bmatrix}2 \\ 4\end{bmatrix}\right)=6\mathbf{T}\left(\begin{bmatrix}2 \\ 4\end{bmatrix}\right).\end{aligned}
$$

Now, since we're told that 

$$
\mathbf{T}\left(\begin{bmatrix}12 \\ 24\end{bmatrix}\right)=\begin{bmatrix}18 \\ -30\end{bmatrix},
$$

we must have

$$
\begin{aligned}6\mathbf{T}\left(\begin{bmatrix}2 \\ 4\end{bmatrix}\right) & =\begin{bmatrix}18 \\ -30\end{bmatrix} \\ \mathbf{T}\left(\begin{bmatrix}2 \\ 4\end{bmatrix}\right) & =\frac{1}{6}\begin{bmatrix}18 \\ -30\end{bmatrix} \\ \mathbf{T}\left(\begin{bmatrix}2 \\ 4\end{bmatrix}\right) & =\begin{bmatrix}3 \\ -5\end{bmatrix}.\end{aligned}
$$

### example 17592186087564 — Determining the Image of a Vector Under a Map Using Vector Addition and Scalar Multiplication

Consider a linear transformation $\mathbf{T}.$ If $\mathbf{T}(4\mathbf{v}_1+\mathbf{v}_2)=\begin{bmatrix}-18 \\ 24\end{bmatrix}$ and $\mathbf{T}(\mathbf{v}_2)=\begin{bmatrix}14 \\ -12\end{bmatrix},$ then find $\mathbf{T}(\mathbf{v}_1).$

Since $\mathbf{T}$ is a linear transformation, we have that

$$
\begin{aligned}\mathbf{T}(k\mathbf{v}+\mathbf{w}) &=\mathbf{T}(k\mathbf{v})+\mathbf{T}(\mathbf{w})=k\mathbf{T}(\mathbf{v})+\mathbf{T}(\mathbf{w})\end{aligned}
$$

for any vectors $\mathbf{v}$ and $\mathbf{w}.$ Therefore,

$$
\begin{aligned}\mathbf{T}(4{\mathbf{v}}_{1}+{\mathbf{v}}_{2}) & =4\mathbf{T}({\mathbf{v}}_{1})+\mathbf{T}({\mathbf{v}}_{2}) \\ \begin{bmatrix}-18 \\ 24\end{bmatrix} & =4\mathbf{T}({\mathbf{v}}_{1})+\begin{bmatrix}14 \\ -12\end{bmatrix} \\ 4\mathbf{T}({\mathbf{v}}_{1}) & =\begin{bmatrix}-18 \\ 24\end{bmatrix}-\begin{bmatrix}14 \\ -12\end{bmatrix} \\ 4\mathbf{T}({\mathbf{v}}_{1}) & =\begin{bmatrix}-32 \\ 36\end{bmatrix} \\ \mathbf{T}({\mathbf{v}}_{1}) & =\frac{1}{4}\begin{bmatrix}-32 \\ 36\end{bmatrix} \\ \mathbf{T}({\mathbf{v}}_{1}) & =\begin{bmatrix}-8 \\ 9\end{bmatrix}.\end{aligned}
$$

### example 17592186087565 — Determining the Image of a Vector Sum Under a Map Using Vector Addition and Scalar Multiplication

Consider a linear transformation $\mathbf{T}.$ If $\mathbf{v}_1 + \mathbf{v}_2=\mathbf{0}$ and $\mathbf{T}(\mathbf{v}_1)=\begin{bmatrix}9 \\ -12 \\ 8\end{bmatrix},$ then find $\mathbf{T}(17\mathbf{v}_1+12\mathbf{v}_2).$

First, since $\mathbf{v}_1 + \mathbf{v}_2=\mathbf{0},$ we have that 

$$
\begin{aligned}17{\mathbf{v}}_{1}+12{\mathbf{v}}_{2} & =5{\mathbf{v}}_{1}+12{\mathbf{v}}_{1}+12{\mathbf{v}}_{2} \\  & =5{\mathbf{v}}_{1}+12({\mathbf{v}}_{1}+{\mathbf{v}}_{2}) \\  & =5{\mathbf{v}}_{1}+12(\mathbf{0}) \\  & =5{\mathbf{v}}_{1}.\end{aligned}
$$

Therefore, we have

$$
\mathbf{T}(17\mathbf{v}_1+12\mathbf{v}_2)=\mathbf{T}(5\mathbf{v}_1).
$$

Now, since $\mathbf{T}$ is a linear transformation, we have that $\mathbf{T}(k\mathbf{v})=k\mathbf{T}(\mathbf{v}).$ So 

$$
\begin{aligned}\mathbf{T}(5{\mathbf{v}}_{1}) & =5\mathbf{T}({\mathbf{v}}_{1}) \\  & =5\begin{bmatrix}9 \\ -12 \\ 8\end{bmatrix} \\  & =\begin{bmatrix}45 \\ -60 \\ 40\end{bmatrix}.\end{aligned}
$$

In conclusion, $\mathbf{T}(17\mathbf{v}_1+12\mathbf{v}_2)=\begin{bmatrix}45 \\ -60 \\ 40\end{bmatrix}.$

### example 17592186087562 — Identifying Linear Transformations

Are the following transformations linear?

$$
\mathbf{T}_1:
\begin{bmatrix}x \\ y\end{bmatrix}	
\longrightarrow 
\begin{bmatrix}{x}^{2} \\ xy\end{bmatrix},\quad

\mathbf{T}_2:
\begin{bmatrix}x \\ y\end{bmatrix}	
\longrightarrow 
\begin{bmatrix}3x \\ x+2y\end{bmatrix}.
$$

A linear transformation $\mathbf{T}$ satisfies two properties:

$$
\begin{aligned} & \mathbf{T}\begin{bmatrix}kx \\ ky\end{bmatrix}=k\mathbf{T}\begin{bmatrix}x \\ y\end{bmatrix}, \\  & \mathbf{T}\begin{bmatrix}{x}_{1}+{x}_{2} \\ {y}_{1}+{y}_{2}\end{bmatrix}=\mathbf{T}\begin{bmatrix}{x}_{1} \\ {y}_{1}\end{bmatrix}+\mathbf{T}\begin{bmatrix}{x}_{2} \\ {y}_{2}\end{bmatrix}.\end{aligned}
$$

First, let's consider $\mathbf{T}_1.$ Checking the first condition, we have

$$
\begin{aligned}{\mathbf{T}}_{1}\begin{bmatrix}kx \\ ky\end{bmatrix} & =\begin{bmatrix}(kx)^{2} \\ (kx)(ky)\end{bmatrix} \\  & =\begin{bmatrix}{k}^{2}{x}^{2} \\ {k}^{2}xy\end{bmatrix} \\  & =k\begin{bmatrix}k{x}^{2} \\ kxy\end{bmatrix} \\  & \ne k{\mathbf{T}}_{1}\begin{bmatrix}x \\ y\end{bmatrix}.\,\times \end{aligned}
$$

Therefore, $\textbf{T}_1$ is not a linear transformation.

Now, let's consider $\mathbf{T}_2.$

- Checking the first condition, we have

$$
\begin{aligned}{\mathbf{T}}_{2}\begin{bmatrix}kx \\ ky\end{bmatrix} & =\begin{bmatrix}3kx \\ kx+2ky\end{bmatrix} \\  & =\begin{bmatrix}k(3x) \\ k(x+2y)\end{bmatrix} \\  & =k\begin{bmatrix}3x \\ x+2y\end{bmatrix} \\  & =k{\mathbf{T}}_{2}\begin{bmatrix}x \\ y\end{bmatrix}.\,✓\end{aligned}
$$

- Checking the second condition, we have

$$
\begin{aligned}{\mathbf{T}}_{2}\begin{bmatrix}{x}_{1}+{x}_{2} \\ {y}_{1}+{y}_{2}\end{bmatrix} & =\begin{bmatrix}3({x}_{1}+{x}_{2}) \\ ({x}_{1}+{x}_{2})+2({y}_{1}+{y}_{2})\end{bmatrix} \\  & =\begin{bmatrix}3{x}_{1}+3{x}_{2} \\ ({x}_{1}+2{y}_{1})+({x}_{2}+2{y}_{2})\end{bmatrix} \\  & =\begin{bmatrix}3{x}_{1} \\ {x}_{1}+2{y}_{1}\end{bmatrix}+\begin{bmatrix}3{x}_{2} \\ {x}_{2}+2{y}_{2}\end{bmatrix} \\  & ={\mathbf{T}}_{2}\begin{bmatrix}{x}_{1} \\ {y}_{1}\end{bmatrix}+{\mathbf{T}}_{2}\begin{bmatrix}{x}_{2} \\ {y}_{2}\end{bmatrix}.\,✓\end{aligned}
$$

Therefore, $\textbf{T}_2$ is a linear transformation.

## Representative practice (first three per skill; full bank in practice.json)

### Determining the Image of a Vector Under a Map Using the Scalar Multiplication Property (10 captured questions)

Question 17592186088151 — question.difficulty/easy

If $\,\mathbf{T}\,$ is a linear transformation and $\,\mathbf{T}\left(\begin{bmatrix}-9 \\ 15\end{bmatrix}\right)=\begin{bmatrix}12 \\ -18\end{bmatrix}$, then find $\,\mathbf{T}\left(\begin{bmatrix}-3 \\ 5\end{bmatrix}\right).$

Solution: Since $\mathbf{T}$ is a linear transformation, it must satisfy $\mathbf{T}(k\mathbf{v})=k\mathbf{T}(\mathbf{v}).$ Noting that $\begin{bmatrix}-9 \\ 15\end{bmatrix}=3\begin{bmatrix}-3 \\ 5\end{bmatrix},$ we have

$$
\begin{aligned}\mathbf{T}\left(\begin{bmatrix}-9 \\ 15\end{bmatrix}\right) & =\mathbf{T}\left(3\begin{bmatrix}-3 \\ 5\end{bmatrix}\right)=3\mathbf{T}\left(\begin{bmatrix}-3 \\ 5\end{bmatrix}\right).\end{aligned}
$$

Now, since we're told that 

$$
\mathbf{T}\left(\begin{bmatrix}-9 \\ 15\end{bmatrix}\right)=\begin{bmatrix}12 \\ -18\end{bmatrix},
$$

we must have

$$
\begin{aligned}3\mathbf{T}\left(\begin{bmatrix}-3 \\ 5\end{bmatrix}\right) & =\begin{bmatrix}12 \\ -18\end{bmatrix} \\ \mathbf{T}\left(\begin{bmatrix}-3 \\ 5\end{bmatrix}\right) & =\frac{1}{3}\begin{bmatrix}12 \\ -18\end{bmatrix} \\ \mathbf{T}\left(\begin{bmatrix}-3 \\ 5\end{bmatrix}\right) & =\begin{bmatrix}4 \\ -6\end{bmatrix}.\end{aligned}
$$

Answer selection: \begin{bmatrix}4 \\ -6\end{bmatrix}

Question 17592186088152 — None

If $\mathbf{T}$ is a linear transformation and $\mathbf{T}\left(\begin{bmatrix}5 \\ 7\end{bmatrix}\right) = \begin{bmatrix}-8 \\ 3\end{bmatrix}$, then find $\mathbf{T}\left(\begin{bmatrix}10 \\ 14\end{bmatrix}\right)$.

Solution: Since $\mathbf{T}$ is a linear transformation, it satisfies $\mathbf{T}(k\mathbf{v})=k\mathbf{T}(\mathbf{v}).$ Noting that

$$
\begin{bmatrix}10\\14\end{bmatrix}=2\begin{bmatrix}5\\7\end{bmatrix},
$$

we have

$$
\begin{aligned}
\mathbf{T}\left(\begin{bmatrix}10\\14\end{bmatrix}\right)
&=\mathbf{T}\left(2\begin{bmatrix}5\\7\end{bmatrix}\right)\\
&=2\mathbf{T}\left(\begin{bmatrix}5\\7\end{bmatrix}\right)\\
&=2\begin{bmatrix}-8\\3\end{bmatrix}\\
&=\begin{bmatrix}-16\\6\end{bmatrix}.
\end{aligned}
$$

Answer selection: \begin{bmatrix}-16 \\ 6\end{bmatrix}

Question 17592186284655 — question.difficulty/easy

If $\,\mathbf{T}\,$ is a linear transformation and $\,\mathbf{T}\left(\begin{bmatrix}8 \\ -12\end{bmatrix}\right)=\begin{bmatrix}16 \\ -20\end{bmatrix}$, then find $\,\mathbf{T}\left(\begin{bmatrix}2 \\ -3\end{bmatrix}\right).$

Solution: Since $\mathbf{T}$ is a linear transformation, it must satisfy $\mathbf{T}(k\mathbf{v})=k\mathbf{T}(\mathbf{v}).$ Noting that $\begin{bmatrix}8 \\ -12\end{bmatrix}=4\begin{bmatrix}2 \\ -3\end{bmatrix},$ we have

$$
\begin{aligned}\mathbf{T}\left(\begin{bmatrix}8 \\ -12\end{bmatrix}\right) & =\mathbf{T}\left(4\begin{bmatrix}2 \\ -3\end{bmatrix}\right)=4\mathbf{T}\left(\begin{bmatrix}2 \\ -3\end{bmatrix}\right).\end{aligned}
$$

Now, since we're told that 

$$
\mathbf{T}\left(\begin{bmatrix}8 \\ -12\end{bmatrix}\right)=\begin{bmatrix}16 \\ -20\end{bmatrix},
$$

we must have

$$
\begin{aligned}4\mathbf{T}\left(\begin{bmatrix}2 \\ -3\end{bmatrix}\right) & =\begin{bmatrix}16 \\ -20\end{bmatrix} \\ \mathbf{T}\left(\begin{bmatrix}2 \\ -3\end{bmatrix}\right) & =\frac{1}{4}\begin{bmatrix}16 \\ -20\end{bmatrix} \\ \mathbf{T}\left(\begin{bmatrix}2 \\ -3\end{bmatrix}\right) & =\begin{bmatrix}4 \\ -5\end{bmatrix}.\end{aligned}
$$

Answer selection: \begin{bmatrix}4 \\ -5\end{bmatrix}

### Determining the Image of a Vector Under a Map Using Vector Addition and Scalar Multiplication (15 captured questions)

Question 17592186088147 — question.difficulty/moderate

Consider a linear transformation $\,\mathbf{T}\,.$ If $\,\mathbf{T}(2{\mathbf{v}}_{1}+{\mathbf{v}}_{2})=\begin{bmatrix}11 \\ 3\end{bmatrix}\,$ and $\,\mathbf{T}({\mathbf{v}}_{2})=\begin{bmatrix}5 \\ -19\end{bmatrix}$, then find $\,\mathbf{T}({\mathbf{v}}_{1}).$

Solution: Since $\mathbf{T}$ is a linear transformation, we have that

$$
\begin{aligned}\mathbf{T}(k\mathbf{v}+\mathbf{w}) &=\mathbf{T}(k\mathbf{v})+\mathbf{T}(\mathbf{w})=k\mathbf{T}(\mathbf{v})+\mathbf{T}(\mathbf{w})\end{aligned}
$$

for any vectors $\mathbf{v}$ and $\mathbf{w}.$ Therefore,

$$
\begin{aligned}\mathbf{T}(2{\mathbf{v}}_{1}+{\mathbf{v}}_{2}) & =2\mathbf{T}({\mathbf{v}}_{1})+\mathbf{T}({\mathbf{v}}_{2}) \\ \begin{bmatrix}11 \\ 3\end{bmatrix} & =2\mathbf{T}({\mathbf{v}}_{1})+\begin{bmatrix}5 \\ -19\end{bmatrix} \\ 2\mathbf{T}({\mathbf{v}}_{1}) & =\begin{bmatrix}11 \\ 3\end{bmatrix}-\begin{bmatrix}5 \\ -19\end{bmatrix} \\ 2\mathbf{T}({\mathbf{v}}_{1}) & =\begin{bmatrix}6 \\ 22\end{bmatrix} \\ \mathbf{T}({\mathbf{v}}_{1}) & =\frac{1}{2}\begin{bmatrix}6 \\ 22\end{bmatrix} \\ \mathbf{T}({\mathbf{v}}_{1}) & =\begin{bmatrix}3 \\ 11\end{bmatrix}.\end{aligned}
$$

Answer selection: \begin{bmatrix}3 \\ 11\end{bmatrix}

Question 17592186088149 — question.difficulty/moderate

Consider a linear transformation $\,\mathbf{T}\,.$ If $\,\mathbf{T}({\mathbf{v}}_{1}+3{\mathbf{v}}_{2})=\begin{bmatrix}15 \\ 6\end{bmatrix}\,$ and $\,\mathbf{T}({\mathbf{v}}_{1})=\begin{bmatrix}6 \\ -12\end{bmatrix}$, then find $\,\mathbf{T}({\mathbf{v}}_{2}).$

Solution: Since $\mathbf{T}$ is a linear transformation, we have that

$$
\begin{aligned}\mathbf{T}(\mathbf{v}+k\mathbf{w}) &=\mathbf{T}(\mathbf{v})+\mathbf{T}(k\mathbf{w})=\mathbf{T}(\mathbf{v})+k\mathbf{T}(\mathbf{w})\end{aligned}
$$

for any vectors $\mathbf{v}$ and $\mathbf{w}.$ Therefore,

$$
\begin{aligned}\mathbf{T}({\mathbf{v}}_{1}+3{\mathbf{v}}_{2}) & =\mathbf{T}({\mathbf{v}}_{1})+3\mathbf{T}({\mathbf{v}}_{2}) \\ \begin{bmatrix}15 \\ 6\end{bmatrix} & =\begin{bmatrix}6 \\ -12\end{bmatrix}+3\mathbf{T}({\mathbf{v}}_{2}) \\ 3\mathbf{T}({\mathbf{v}}_{2}) & =\begin{bmatrix}15 \\ 6\end{bmatrix}-\begin{bmatrix}6 \\ -12\end{bmatrix} \\ 3\mathbf{T}({\mathbf{v}}_{2}) & =\begin{bmatrix}9 \\ 18\end{bmatrix} \\ \mathbf{T}({\mathbf{v}}_{2}) & =\frac{1}{3}\begin{bmatrix}9 \\ 18\end{bmatrix} \\ \mathbf{T}({\mathbf{v}}_{2}) & =\begin{bmatrix}3 \\ 6\end{bmatrix}.\end{aligned}
$$

Answer selection: \begin{bmatrix}3 \\ 6\end{bmatrix}

Question 17592186235515 — question.difficulty/moderate

An ambulance service helicopter takes off from a hospital helipad three times on a particular day. The helicopter's location a few seconds after these takeoffs are given by points $P,$ $Q,$ and $R.$

The helicopter's pilot wants to consider the effect of a linear transformation $\mathbf{T}$ such that $\mathbf{T}(\mathbf{r})=⟨-8,17,3⟩$ and $\mathbf{T}(3\mathbf{q}+\mathbf{r})=⟨10,17,9⟩.$ Find the image of $\mathbf{q}$ under the action of $\mathbf{T}.$

$\mathbf{T}(\mathbf{q})=\langle$ {{field-1}} $,\,$ {{field-2}} $,\,$ {{field-3}} $\rangle.$

Solution: Since $\mathbf{T}$ is a linear transformation, we have that

$$
\begin{aligned}\mathbf{T}(k\mathbf{q}+h\mathbf{r}) &=\mathbf{T}(k\mathbf{q})+\mathbf{T}(h\mathbf{r})=k\mathbf{T}(\mathbf{q})+h\mathbf{T}(\mathbf{r})\end{aligned}
$$

for any vectors $\mathbf{q}$ and $\mathbf{r}.$ Therefore,

$$
\begin{aligned}\mathbf{T}(3\mathbf{q}+\mathbf{r}) & =3\mathbf{T}(\mathbf{q})+\mathbf{T}(\mathbf{r}) \\ ⟨10,17,9⟩ & =3\mathbf{T}(\mathbf{q})+⟨-8,17,3⟩ \\ 3\mathbf{T}(\mathbf{q}) & =⟨10,17,9⟩-⟨-8,17,3⟩ \\ 3\mathbf{T}(\mathbf{q}) & =⟨18,0,6⟩ \\ \mathbf{T}(\mathbf{q}) & =\frac{1}{3}⟨18,0,6⟩ \\ \mathbf{T}(\mathbf{q}) & =⟨6,0,2⟩.\end{aligned}
$$

Answer field-1: 6

Answer field-2: 0

Answer field-3: 2

### Determining the Image of a Vector Sum Under a Map Using Vector Addition and Scalar Multiplication (15 captured questions)

Question 17592186088148 — question.difficulty/moderate

Consider a linear transformation $\,\mathbf{T}\,.$ If $\,{\mathbf{v}}_{1}+{\mathbf{v}}_{2}=\mathbf{0}\,$ and $\,\mathbf{T}({\mathbf{v}}_{1})=\begin{bmatrix}54 \\ -36 \\ 30\end{bmatrix}\,$, find $\,\mathbf{T}(21{\mathbf{v}}_{1}+18{\mathbf{v}}_{2}).$

Solution: First, since ${\mathbf{v}}_{1}+{\mathbf{v}}_{2}=\mathbf{0},$ we have that 

$$
\begin{aligned}21{\mathbf{v}}_{1}+18{\mathbf{v}}_{2} & =18{\mathbf{v}}_{1}+3{\mathbf{v}}_{1}+18{\mathbf{v}}_{2} \\  & =18({\mathbf{v}}_{1}+{\mathbf{v}}_{2})+3{\mathbf{v}}_{1} \\  & =18(\mathbf{0})+3{\mathbf{v}}_{1} \\  & =3{\mathbf{v}}_{1}.\end{aligned}
$$

Therefore, we have

$$
\mathbf{T}(21{\mathbf{v}}_{1}+18{\mathbf{v}}_{2})=\mathbf{T}(3{\mathbf{v}}_{1}).
$$

Now, since $\mathbf{T}$ is a linear transformation, we have that $\mathbf{T}(k\mathbf{v})=k\mathbf{T}(\mathbf{v}).$ So 

$$
\begin{aligned}\mathbf{T}(3{\mathbf{v}}_{1}) & =3\mathbf{T}({\mathbf{v}}_{1}) \\  & =3\begin{bmatrix}54 \\ -36 \\ 30\end{bmatrix} \\  & =\begin{bmatrix}162 \\ -108 \\ 90\end{bmatrix}.\end{aligned}
$$

In conclusion, $\mathbf{T}(21{\mathbf{v}}_{1}+18{\mathbf{v}}_{2})=\begin{bmatrix}162 \\ -108 \\ 90\end{bmatrix}.$

Answer selection: \begin{bmatrix}162 \\ -108 \\ 90\end{bmatrix}

Question 17592186088150 — None

Consider a linear transformation $\mathbf{T}$. If $\mathbf{v}_{1} + \mathbf{v}_{2} = \mathbf{0}$ and $\mathbf{T}(\mathbf{v}_{2}) = \begin{bmatrix}-12 \\ 9 \\ 15\end{bmatrix}$, find $\mathbf{T}(15\mathbf{v}_{1} + 19\mathbf{v}_{2})$.

Solution: First, since $\mathbf{v}_1+\mathbf{v}_2=\mathbf{0},$ we have

$$
\begin{aligned}
15\mathbf{v}_1+19\mathbf{v}_2
&=15\mathbf{v}_1+15\mathbf{v}_2+4\mathbf{v}_2\\
&=15(\mathbf{v}_1+\mathbf{v}_2)+4\mathbf{v}_2\\
&=15\mathbf{0}+4\mathbf{v}_2\\
&=4\mathbf{v}_2.
\end{aligned}
$$

Therefore, $\mathbf{T}(15\mathbf{v}_1+19\mathbf{v}_2)=\mathbf{T}(4\mathbf{v}_2).$ Since $\mathbf{T}$ is linear, it satisfies $\mathbf{T}(k\mathbf{v})=k\mathbf{T}(\mathbf{v}).$ Thus

$$
\begin{aligned}
\mathbf{T}(15\mathbf{v}_1+19\mathbf{v}_2)
&=4\mathbf{T}(\mathbf{v}_2)\\
&=4\begin{bmatrix}-12\\9\\15\end{bmatrix}\\
&=\begin{bmatrix}-48\\36\\60\end{bmatrix}.
\end{aligned}
$$

Answer selection: \begin{bmatrix}-48 \\ 36 \\ 60\end{bmatrix}

Question 17592186284659 — question.difficulty/moderate

Consider a linear transformation $\,\mathbf{T}\,.$ If $\,{\mathbf{v}}_{1}+{\mathbf{v}}_{2}=\mathbf{0}\,$ and $\,\mathbf{T}({\mathbf{v}}_{1})=\begin{bmatrix}-25 \\ 16 \\ 20\end{bmatrix}\,$, find $\,\mathbf{T}(15{\mathbf{v}}_{1}+12{\mathbf{v}}_{2}).$

Solution: First, since ${\mathbf{v}}_{1}+{\mathbf{v}}_{2}=\mathbf{0},$ we have that 

$$
\begin{aligned}15{\mathbf{v}}_{1}+12{\mathbf{v}}_{2} & =12{\mathbf{v}}_{1}+3{\mathbf{v}}_{1}+12{\mathbf{v}}_{2} \\  & =12({\mathbf{v}}_{1}+{\mathbf{v}}_{2})+3{\mathbf{v}}_{1} \\  & =12(\mathbf{0})+3{\mathbf{v}}_{1} \\  & =3{\mathbf{v}}_{1}.\end{aligned}
$$

Therefore, we have

$$
\mathbf{T}(15{\mathbf{v}}_{1}+12{\mathbf{v}}_{2})=\mathbf{T}(3{\mathbf{v}}_{1}).
$$

Now, since $\mathbf{T}$ is a linear transformation, we have that $\mathbf{T}(k\mathbf{v})=k\mathbf{T}(\mathbf{v}).$ So 

$$
\begin{aligned}\mathbf{T}(3{\mathbf{v}}_{1}) & =3\mathbf{T}({\mathbf{v}}_{1}) \\  & =3\begin{bmatrix}-25 \\ 16 \\ 20\end{bmatrix} \\  & =\begin{bmatrix}-75 \\ 48 \\ 60\end{bmatrix}.\end{aligned}
$$

In conclusion, $\mathbf{T}(15{\mathbf{v}}_{1}+12{\mathbf{v}}_{2})=\begin{bmatrix}-75 \\ 48 \\ 60\end{bmatrix}.$

Answer selection: \begin{bmatrix}-75 \\ 48 \\ 60\end{bmatrix}

### Identifying Linear Transformations (10 captured questions)

Question 17592186087995 — question.difficulty/hard

Let
$$
\displaystyle \mathbf{T}: \begin{bmatrix}x \\ y\end{bmatrix}⟶\begin{bmatrix}x^{2} + y^{2} \\ 2x + 7y\end{bmatrix}.
$$
Which of the following statements are true?

1. $\mathbf{T}(k\mathbf{v}) = k\mathbf{T}(\mathbf{v})$ for any real $2\times 1$ column vector $\mathbf{v}$ and real scalar $k$
2. $\mathbf{T}(\mathbf{v}_{1} + \mathbf{v}_{2}) = \mathbf{T}(\mathbf{v}_{1}) + \mathbf{T}(\mathbf{v}_{2})$ for any real $2\times 1$ column vectors $\mathbf{v}_{1}$ and $\mathbf{v}_{2}$
3. $\mathbf{T}$ is **NOT** a linear transformation

Solution: A linear transformation $\mathbf{T}$ satisfies two properties:

$$
\begin{aligned} & \mathbf{T}\begin{bmatrix}kx \\ ky\end{bmatrix}=k\mathbf{T}\begin{bmatrix}x \\ y\end{bmatrix}, \\  & \mathbf{T}\begin{bmatrix}{x}_{1}+{x}_{2} \\ {y}_{1}+{y}_{2}\end{bmatrix}=\mathbf{T}\begin{bmatrix}{x}_{1} \\ {y}_{1}\end{bmatrix}+\mathbf{T}\begin{bmatrix}{x}_{2} \\ {y}_{2}\end{bmatrix}.\end{aligned}
$$

- Checking the first condition, we have

$$
\begin{aligned}\mathbf{T}\begin{bmatrix}kx \\ ky\end{bmatrix} & =\begin{bmatrix}(kx)^{2}+(ky)^{2} \\ 2(kx)+7(ky)\end{bmatrix} \\  & =\begin{bmatrix}{k}^{2}({x}^{2}+{y}^{2}) \\ k(2x+7y)\end{bmatrix} \\  & =k\begin{bmatrix}k({x}^{2}+{y}^{2}) \\ 2x+7y\end{bmatrix} \\  & \ne k\mathbf{T}\begin{bmatrix}x \\ y\end{bmatrix}.\,{\color{red}\times }\end{aligned}
$$

Therefore, $\mathbf{\text{T}}$ is not a linear transformation.

- Checking the second condition, we have

$$
\begin{aligned}\mathbf{T}\begin{bmatrix}{x}_{1}+{x}_{2} \\ {y}_{1}+{y}_{2}\end{bmatrix} & =\begin{bmatrix}({x}_{1}+{x}_{2})^{2}+({y}_{1}+{y}_{2})^{2} \\ 2({x}_{1}+{x}_{2})+7({y}_{1}+{y}_{2})\end{bmatrix} \\  & =\begin{bmatrix}({x}_{1}^{2}+{y}_{1}^{2})+({x}_{2}^{2}+{y}_{2}^{2})+2({x}_{1}{x}_{2}+{y}_{1}{y}_{2}) \\ (2{x}_{1}+7{y}_{1})+(2{x}_{2}+7{y}_{2})\end{bmatrix} \\  & =\begin{bmatrix}{x}_{1}^{2}+{y}_{1}^{2} \\ 2{x}_{1}+7{y}_{1}\end{bmatrix}+\begin{bmatrix}{x}_{2}^{2}+{y}_{2}^{2} \\ 2{x}_{2}+7{y}_{2}\end{bmatrix}+\begin{bmatrix}2({x}_{1}{x}_{2}+{y}_{1}{y}_{2}) \\ 0\end{bmatrix} \\  & =\mathbf{T}\begin{bmatrix}{x}_{1} \\ {y}_{1}\end{bmatrix}+\mathbf{T}\begin{bmatrix}{x}_{2} \\ {y}_{2}\end{bmatrix}+\begin{bmatrix}2({x}_{1}{x}_{2}+{y}_{1}{y}_{2}) \\ 0\end{bmatrix} \\  & \ne \mathbf{T}\begin{bmatrix}{x}_{1} \\ {y}_{1}\end{bmatrix}+\mathbf{T}\begin{bmatrix}{x}_{2} \\ {y}_{2}\end{bmatrix}.\,{\color{red}\times }\end{aligned}
$$

As a result, only statement III is true.

Answer selection: III only

Question 17592186088417 — question.difficulty/moderate

Let 
$$
\displaystyle \mathbf{T}:\begin{bmatrix}x \\ y\end{bmatrix}⟶\begin{bmatrix}y \\ x\end{bmatrix}.
$$
Which of the following statements are true?

Select all that apply.

Solution: A linear transformation $\mathbf{T}$ satisfies two properties:

$$
\begin{aligned} & \mathbf{T}\begin{bmatrix}kx \\ ky\end{bmatrix}=k\mathbf{T}\begin{bmatrix}x \\ y\end{bmatrix}, \\  & \mathbf{T}\begin{bmatrix}{x}_{1}+{x}_{2} \\ {y}_{1}+{y}_{2}\end{bmatrix}=\mathbf{T}\begin{bmatrix}{x}_{1} \\ {y}_{1}\end{bmatrix}+\mathbf{T}\begin{bmatrix}{x}_{2} \\ {y}_{2}\end{bmatrix}.\end{aligned}
$$

- Checking the first condition, we have

$$
\begin{aligned}\mathbf{T}\begin{bmatrix}kx \\ ky\end{bmatrix} & =\begin{bmatrix}ky \\ kx\end{bmatrix} \\  & =k\begin{bmatrix}y \\ x\end{bmatrix} \\  & =k\mathbf{T}\begin{bmatrix}x \\ y\end{bmatrix}.\,✓\end{aligned}
$$

- Checking the second condition, we have

$$
\begin{aligned}\mathbf{T}\begin{bmatrix}{x}_{1}+{x}_{2} \\ {y}_{1}+{y}_{2}\end{bmatrix} & =\begin{bmatrix}{y}_{1}+{y}_{2} \\ {x}_{1}+{x}_{2}\end{bmatrix} \\  & =\begin{bmatrix}{y}_{1} \\ {x}_{1}\end{bmatrix}+\begin{bmatrix}{y}_{2} \\ {x}_{2}\end{bmatrix} \\  & =\mathbf{T}\begin{bmatrix}{x}_{1} \\ {y}_{1}\end{bmatrix}+\mathbf{T}\begin{bmatrix}{x}_{2} \\ {y}_{2}\end{bmatrix}.\,✓\end{aligned}
$$

Therefore, $\text{T}$ is a linear transformation.

As a result, all three statements are true.

Answer $\mathbf{T}$ is a linear transformation: true

Answer $\mathbf{T}(k\mathbf{v})=k\mathbf{T}(\mathbf{v})$ for any real $2\times 1$ column vector $\mathbf{v}$ and real scalar $k$: true

Answer $\mathbf{T}({\mathbf{v}}_{1}+{\mathbf{v}}_{2})=\mathbf{T}({\mathbf{v}}_{1})+\mathbf{T}({\mathbf{v}}_{2})$ for any real $2\times 1$ column vectors ${\mathbf{v}}_{1}$ and ${\mathbf{v}}_{2}$: true

Answer None of the above: false

Question 17592186253648 — question.difficulty/hard

Let 
$$
\displaystyle \mathbf{T}:\begin{bmatrix}x \\ y\end{bmatrix}⟶\begin{bmatrix}{x}^{2} \\ 7y\end{bmatrix}.
$$
Which of the following statements are true?

Select all that apply.

Solution: A linear transformation $\mathbf{T}$ satisfies two properties:

$$
\begin{aligned} & \mathbf{T}\begin{bmatrix}kx \\ ky\end{bmatrix}=k\mathbf{T}\begin{bmatrix}x \\ y\end{bmatrix}, \\  & \mathbf{T}\begin{bmatrix}{x}_{1}+{x}_{2} \\ {y}_{1}+{y}_{2}\end{bmatrix}=\mathbf{T}\begin{bmatrix}{x}_{1} \\ {y}_{1}\end{bmatrix}+\mathbf{T}\begin{bmatrix}{x}_{2} \\ {y}_{2}\end{bmatrix}.\end{aligned}
$$

- Checking the first condition, we have

$$
\begin{aligned}\mathbf{T}\begin{bmatrix}kx \\ ky\end{bmatrix} & =\begin{bmatrix}(kx)^{2} \\ 7(ky)\end{bmatrix} \\  & =\begin{bmatrix}{k}^{2}({x}^{2}) \\ k(7y)\end{bmatrix} \\  & =k\begin{bmatrix}k({x}^{2}) \\ 7y\end{bmatrix} \\  & \ne k\mathbf{T}\begin{bmatrix}x \\ y\end{bmatrix}.\,\times \end{aligned}
$$

Therefore, $\text{T}$ is not a linear transformation.

- Checking the second condition, we have

$$
\begin{aligned}\mathbf{T}\begin{bmatrix}{x}_{1}+{x}_{2} \\ {y}_{1}+{y}_{2}\end{bmatrix} & =\begin{bmatrix}({x}_{1}+{x}_{2})^{2} \\ 7({y}_{1}+{y}_{2})\end{bmatrix} \\  & =\begin{bmatrix}{x}_{1}^{2}+{x}_{2}^{2}+2{x}_{1}{x}_{2} \\ 7{y}_{1}+7{y}_{2}\end{bmatrix} \\  & =\begin{bmatrix}{x}_{1}^{2} \\ 7{y}_{1}\end{bmatrix}+\begin{bmatrix}{x}_{2}^{2} \\ 7{y}_{2}\end{bmatrix}+\begin{bmatrix}2{x}_{1}{x}_{2} \\ 0\end{bmatrix} \\  & =\mathbf{T}\begin{bmatrix}{x}_{1} \\ {y}_{1}\end{bmatrix}+\mathbf{T}\begin{bmatrix}{x}_{2} \\ {y}_{2}\end{bmatrix}+\begin{bmatrix}2{x}_{1}{x}_{2} \\ 0\end{bmatrix} \\  & \ne \mathbf{T}\begin{bmatrix}{x}_{1} \\ {y}_{1}\end{bmatrix}+\mathbf{T}\begin{bmatrix}{x}_{2} \\ {y}_{2}\end{bmatrix}.\,\times \end{aligned}
$$

As a result, only statement “$\mathbf{T}$ is **NOT** a linear transformation” is true.

Answer $\mathbf{T}$ is **NOT** a linear transformation: true

Answer $\mathbf{T}(k\mathbf{v})=k\mathbf{T}(\mathbf{v})$ for any real $2\times 1$ column vector $\mathbf{v}$ and real scalar $k$: false

Answer $\mathbf{T}({\mathbf{v}}_{1}+{\mathbf{v}}_{2})=\mathbf{T}({\mathbf{v}}_{1})+\mathbf{T}({\mathbf{v}}_{2})$ for any real $2\times 1$ column vectors ${\mathbf{v}}_{1}$ and ${\mathbf{v}}_{2}$: false

Answer None of the above: false
