# 17592186048499 Linear Combinations of Vectors in N-Dimensional Euclidean Space

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186121034 — Introduction

Consider a vector $\mathbf{u}$ which is given in terms of the vectors $\mathbf{v_1}$ and $\mathbf{v_2}$ as follows:

$$
{\color{red}3}{\color{blue}\mathbf{v_1}}+({\color{red}-2}){\color{blue}\mathbf{v_2}} = \mathbf{u}
$$

Here, we say that $\mathbf{u}$ is a **linear combination** of the vectors ${\color{blue}\mathbf{v_1}}$ and ${\color{blue}\mathbf{v_2}}$ with coefficients ${\color{red}3}$ and ${\color{red}-2}$ respectively. 

In general, a linear combination of $n$ vectors $\mathbf{v_1},\mathbf{v_2},\dots,\mathbf{v_n}$ is the *weighted sum*

$$
{\color{red}x_1}\mathbf{\color{blue}v_1}+{\color{red}x_2}\mathbf{\color{blue}v_2}+\cdots + {\color{red}x_n}\mathbf{\color{blue}v_n} = \mathbf{u},
$$

where ${\color{red}x_1},{\color{red}x_2},\dots,{\color{red}x_n}\in\mathbb{R}.$ We say that $\mathbf{u}$ is a linear combination of the vectors $\mathbf{\color{blue}v_1},\mathbf{\color{blue}v_2},\dots,\mathbf{\color{blue}v_n}$ with coefficients (or *weights*) ${\color{red}x_1},{\color{red}x_2},\dots,{\color{red}x_n},$ respectively.

For instance, 


$$
{\color{red}2} \cdot \underbrace{\begin{bmatrix}1 \\ -1\end{bmatrix}}_{\large\color{blue}\mathbf{v}_1} + {\color{red}0} \cdot \underbrace{\begin{bmatrix}\sqrt{2} \\ 3\end{bmatrix}}_{\large\color{blue}\mathbf{v}_2} + {\color{red}\dfrac{1}{2}} \cdot \underbrace{\begin{bmatrix}8 \\ 0\end{bmatrix}}_{\large\color{blue}\mathbf{v}_3}
$$


is the linear combination of vectors $\mathbf{\color{blue}v_1},\mathbf{\color{blue}v_2},\mathbf{\color{blue}v_3}$ with coefficients ${\color{red}2}, {\color{red}0}, {\color{red}\dfrac{1}{2}},$ respectively.



### example 17592186119616 — Solving for One Coefficient in a Linear Combination

Find $s,$ if $3\mathbf{a_1}+s\mathbf{a_2} = \mathbf{b}$ and


$$
\mathbf{a_1}=\begin{bmatrix}-1 \\ 2 \\ 1\end{bmatrix}, \quad \mathbf{a_2}=\begin{bmatrix}4 \\ 0 \\ -2\end{bmatrix}, \quad \mathbf{b}=\begin{bmatrix}13 \\ 6 \\ -5\end{bmatrix}.
$$



Using the properties of addition/subtraction and scalar multiplication of vectors to isolate the $s$ term, we get

$$
\begin{aligned}3{a}_{1}+s{a}_{2} & =b \\ 3\begin{bmatrix}-1 \\ 2 \\ 1\end{bmatrix}+s\begin{bmatrix}4 \\ 0 \\ -2\end{bmatrix} & =\begin{bmatrix}13 \\ 6 \\ -5\end{bmatrix} \\ s\begin{bmatrix}4 \\ 0 \\ -2\end{bmatrix} & =\begin{bmatrix}13 \\ 6 \\ -5\end{bmatrix}-3\begin{bmatrix}-1 \\ 2 \\ 1\end{bmatrix} \\ s\begin{bmatrix}4 \\ 0 \\ -2\end{bmatrix} & =\begin{bmatrix}16 \\ 0 \\ -8\end{bmatrix}.\end{aligned}
$$

From the final equation above, we can tell that $s=4.$

### example 17592186119617 — Solving for a Vector in a Linear Combination

Find $\mathbf{x},$ if $\mathbf{a}+2\mathbf{x} = \mathbf{b}$ and


$$
\mathbf{a}=\begin{bmatrix}12 \\ -11 \\ -5\end{bmatrix}, \quad \mathbf{b}=\begin{bmatrix}24 \\ -9 \\ 13\end{bmatrix}.
$$



Using the properties of addition/subtraction and scalar multiplication of vectors to isolate $\mathbf{x},$ we get

$$
\begin{aligned}a+2x & =b \\ 2x & =b-a \\ x & =\frac{1}{2}(b-a) \\ x & =\frac{1}{2}\left(\begin{bmatrix}24 \\ -9 \\ 13\end{bmatrix}-\begin{bmatrix}12 \\ -11 \\ -5\end{bmatrix}\right) \\ x & =\frac{1}{2}\begin{bmatrix}12 \\ 2 \\ 18\end{bmatrix} \\ x & =\begin{bmatrix}6 \\ 1 \\ 9\end{bmatrix}.\end{aligned}
$$

### example 17592186119618 — Solving for Two Coefficients in a Linear Combination

Consider the vectors



$$
\mathbf{c_1}=\begin{bmatrix}4 \\ -1 \\ 3\end{bmatrix}, \quad \mathbf{c_2}=\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix}, \quad \mathbf{d}=\begin{bmatrix}5 \\ -5 \\ 0\end{bmatrix}.
$$



If $x_1 \mathbf{c}_1 + x_2\mathbf{c}_2  = \mathbf d,$ then what is $x_1+x_2?$

If $x_1 \mathbf{c}_1 + x_2\mathbf{c}_2  = \mathbf d,$ then we have

$$
\begin{aligned}{x}_{1}\begin{bmatrix}4 \\ -1 \\ 3\end{bmatrix}+{x}_{2}\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix} & =\begin{bmatrix}5 \\ -5 \\ 0\end{bmatrix} \\ \begin{bmatrix}4{x}_{1}+{x}_{2} \\ -{x}_{1} \\ 3{x}_{1}+{x}_{2}\end{bmatrix} & =\begin{bmatrix}5 \\ -5 \\ 0\end{bmatrix}.\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}4{x}_{1}+{x}_{2} &=5 \\ -{x}_{1} &=-5 \\ 3{x}_{1}+{x}_{2} &=0\end{aligned}\right.
$$

From the second equation, we obtain $x_1=5,$ which we substitute into the first equation to get 

$$
\begin{aligned}4{x}_{1}+{x}_{2} & =5 \\ 4(5)+{x}_{2} & =5 \\ {x}_{2} & =-15.\end{aligned}
$$

Finally, we substitute $x_1=5$ and $x_2=-15$ into the third equation to get

$$
\begin{aligned}3{x}_{1}+{x}_{2} & =0 \\ 3(5)+(-15) & =0 \\ 0 & =0,\end{aligned}
$$

which gives a true statement. 

So the solution of the system is $x_1=5$ and $x_2=-15,$ which means

$$
5 \mathbf{c_1}-15 \mathbf{c_2} = \mathbf{d}.
$$

Consequently,

$$
x_1+x_2=5-15=-10.
$$

### example 17592186119669 — Solving for Three Coefficients in a Linear Combination

Consider the vectors



$$
\mathbf{a_1}=\begin{bmatrix}0 \\ 1 \\ 0\end{bmatrix}, \quad \mathbf{a_2}=\begin{bmatrix}1 \\ 0 \\ -1\end{bmatrix}, \quad \mathbf{a_3}=\begin{bmatrix}1 \\ 2 \\ 3\end{bmatrix}, \quad \mathbf{b}=\begin{bmatrix}1 \\ 1 \\ 7\end{bmatrix}.
$$



If $x_1 \mathbf{a}_1 + x_2\mathbf{a}_2 + x_3\mathbf{a}_3 = \mathbf b,$ then what is $x_1+x_2+x_3?$

Since $\mathbf{b}$ is a linear combination of vectors $\mathbf{a_1}, \,\mathbf{a_2}$ and $\mathbf{a_3}$ with coefficients $x_1,\, x_2$ and $x_3,$ respectively, we have

$$
\begin{aligned}{x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3} & =b \\ {x}_{1}\begin{bmatrix}0 \\ 1 \\ 0\end{bmatrix}+{x}_{2}\begin{bmatrix}1 \\ 0 \\ -1\end{bmatrix}+{x}_{3}\begin{bmatrix}1 \\ 2 \\ 3\end{bmatrix} & =\begin{bmatrix}1 \\ 1 \\ 7\end{bmatrix} \\ \begin{bmatrix}0 \\ {x}_{1} \\ 0\end{bmatrix}+\begin{bmatrix}{x}_{2} \\ 0 \\ -{x}_{2}\end{bmatrix}+\begin{bmatrix}{x}_{3} \\ 2{x}_{3} \\ 3{x}_{3}\end{bmatrix} & =\begin{bmatrix}1 \\ 1 \\ 7\end{bmatrix} \\ \begin{bmatrix}{x}_{2}+{x}_{3} \\ {x}_{1}+2{x}_{3} \\ -{x}_{2}+3{x}_{3}\end{bmatrix} & =\begin{bmatrix}1 \\ 1 \\ 7\end{bmatrix}.\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}{x}_{2}+{x}_{3} &=1 \\ {x}_{1}+2{x}_{3} &=1 \\ -{x}_{2}+3{x}_{3} &=7\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:



$$
M= \left[ \begin{array}{ccc|c}0 & 1 & 1 & 1 \\ 1 & 0 & 2 & 1 \\ 0 & -1 & 3 & 7\end{array} \right]
$$



Row-reducing the augmented matrix, we get

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}0 & 1 & 1 & 1 \\ 1 & 0 & 2 & 1 \\ 0 & -1 & 3 & 7\end{array}\right] & {R}_{1} & ↔{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 2 & 1 \\ 0 & 1 & 1 & 1 \\ 0 & -1 & 3 & 7\end{array}\right] & {R}_{3} & :={R}_{3}+{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 2 & 1 \\ 0 & 1 & 1 & 1 \\ 0 & 0 & 4 & 8\end{array}\right] & {R}_{3} & :=\frac{1}{4}{R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 2 & 1 \\ 0 & 1 & 1 & 1 \\ 0 & 0 & 1 & 2\end{array}\right].\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}{x}_{1}+2{x}_{3} &=1 \\ {x}_{2}+{x}_{3} &=1 \\ {x}_{3} &=2.\end{aligned}\right.
$$

From the third equation, we get $x_3 = 2.$ Substituting this into the second equation, we get

$$
x_2+(2) = 1 \quad\Rightarrow\quad x_2 = -1,
$$

and substituting $x_3=2$ into the first equation, we get

$$
x_1+2(2) = 1 \quad\Rightarrow\quad x_1 = -3.
$$

So the solution of the system is $x_1=-3, x_2=-1, x_3=2,$ which means

$$
-3 \mathbf{a_1}- \mathbf{a_2} +2 \mathbf{a_3}= \mathbf{b}.
$$

Consequently,

$$
x_1+x_2+x_3=-3-1+2=-2.
$$

## Representative practice (first three per skill; full bank in practice.json)

### Solving for One Coefficient in a Linear Combination (29 captured questions)

Question 17592186120311 — question.difficulty/easy

Find $l$, if $5{\mathbf{a}}_{\mathbf{1}}+l{\mathbf{a}}_{\mathbf{2}}=\mathbf{b}$ and

$$
{\mathbf{a}}_{\mathbf{1}}=\begin{bmatrix}9 \\ -2 \\ 0 \\ 7\end{bmatrix},\hspace{1em}{\mathbf{a}}_{\mathbf{2}}=\begin{bmatrix}0 \\ 5 \\ -2 \\ 8\end{bmatrix},\hspace{1em}\mathbf{b}=\begin{bmatrix}45 \\ -20 \\ 4 \\ 19\end{bmatrix}.
$$

Solution: Using the properties of addition/subtraction and scalar multiplication of vectors to isolate the $l$ term, we get

$$
\begin{aligned}5{\mathbf{a}}_{\mathbf{1}}+l{\mathbf{a}}_{\mathbf{2}} & =\mathbf{b} \\ 5\begin{bmatrix}9 \\ -2 \\ 0 \\ 7\end{bmatrix}+l\begin{bmatrix}0 \\ 5 \\ -2 \\ 8\end{bmatrix} & =\begin{bmatrix}45 \\ -20 \\ 4 \\ 19\end{bmatrix} \\ l\begin{bmatrix}0 \\ 5 \\ -2 \\ 8\end{bmatrix} & =\begin{bmatrix}45 \\ -20 \\ 4 \\ 19\end{bmatrix}-5\begin{bmatrix}9 \\ -2 \\ 0 \\ 7\end{bmatrix} \\ l\begin{bmatrix}0 \\ 5 \\ -2 \\ 8\end{bmatrix} & =\begin{bmatrix}0 \\ -10 \\ 4 \\ -16\end{bmatrix}.\end{aligned}
$$

From the final equation above, we can tell that $l=-2.$

Answer selection: -2

Question 17592186120312 — None

Find $q$, if $7{\mathbf{a}}_{\mathbf{1}}+q{\mathbf{a}}_{\mathbf{2}}=\mathbf{b}$ and
$$
{\mathbf{a}}_{\mathbf{1}}=\begin{bmatrix}0 \\ -1\end{bmatrix},\hspace{1em}{\mathbf{a}}_{\mathbf{2}}=\begin{bmatrix}8 \\ 6\end{bmatrix},\hspace{1em}\mathbf{b}=\begin{bmatrix}32 \\ 17\end{bmatrix}.
$$

Solution: Using the properties of addition/subtraction and scalar multiplication of vectors to isolate the $q$ term, we get

$$
\begin{aligned}
q a_2&=b-7a_1\\
q\begin{bmatrix}8\\6\end{bmatrix}
&=\begin{bmatrix}32\\17\end{bmatrix}-7\begin{bmatrix}0\\-1\end{bmatrix}\\
&=\begin{bmatrix}32\\24\end{bmatrix}.
\end{aligned}
$$

Both coordinates give $q=4$.

Answer selection: 4

Question 17592186240984 — question.difficulty/easy

Find $h$, if $3{\mathbf{a}}_{\mathbf{1}}+h{\mathbf{a}}_{\mathbf{2}}=\mathbf{b}$ and

$$
{\mathbf{a}}_{\mathbf{1}}=\begin{bmatrix}1 \\ -1 \\ 2 \\ 1\end{bmatrix},\hspace{1em}{\mathbf{a}}_{\mathbf{2}}=\begin{bmatrix}-3 \\ 2 \\ 4 \\ 1\end{bmatrix},\hspace{1em}\mathbf{b}=\begin{bmatrix}-3 \\ 1 \\ 14 \\ 5\end{bmatrix}.
$$

Solution: Using the properties of addition/subtraction and scalar multiplication of vectors to isolate the $h$ term, we get

$$
\begin{aligned}3{\mathbf{a}}_{\mathbf{1}}+h{\mathbf{a}}_{\mathbf{2}} & =\mathbf{b} \\ 3\begin{bmatrix}1 \\ -1 \\ 2 \\ 1\end{bmatrix}+h\begin{bmatrix}-3 \\ 2 \\ 4 \\ 1\end{bmatrix} & =\begin{bmatrix}-3 \\ 1 \\ 14 \\ 5\end{bmatrix} \\ h\begin{bmatrix}-3 \\ 2 \\ 4 \\ 1\end{bmatrix} & =\begin{bmatrix}-3 \\ 1 \\ 14 \\ 5\end{bmatrix}-3\begin{bmatrix}1 \\ -1 \\ 2 \\ 1\end{bmatrix} \\ h\begin{bmatrix}-3 \\ 2 \\ 4 \\ 1\end{bmatrix} & =\begin{bmatrix}-6 \\ 4 \\ 8 \\ 2\end{bmatrix}.\end{aligned}
$$

From the final equation above, we can tell that $h=2.$

Answer selection: 2

### Solving for a Vector in a Linear Combination (32 captured questions)

Question 17592186120310 — question.difficulty/easy

Find $\mathbf{x}$, if $4\mathbf{a}+6\mathbf{x}=\mathbf{b}$ and

$$
\mathbf{a}=\begin{bmatrix}-3 \\ 0 \\ -7\end{bmatrix},\hspace{1em}\mathbf{b}=\begin{bmatrix}24 \\ -6 \\ -10\end{bmatrix}.
$$

Solution: Using the properties of addition/subtraction and scalar multiplication of vectors to isolate $\mathbf{x},$ we get

$$
\begin{aligned}4\mathbf{a}+6\mathbf{x} & =\mathbf{b} \\ 6\mathbf{x} & =\mathbf{b}-4\mathbf{a} \\ \mathbf{x} & =\frac{1}{6}(\mathbf{b}-4\mathbf{a}) \\ \mathbf{x} & =\frac{1}{6}\left(\begin{bmatrix}24 \\ -6 \\ -10\end{bmatrix}-4\begin{bmatrix}-3 \\ 0 \\ -7\end{bmatrix}\right) \\ \mathbf{x} & =\frac{1}{6}\begin{bmatrix}36 \\ -6 \\ 18\end{bmatrix} \\ \mathbf{x} & =\begin{bmatrix}6 \\ -1 \\ 3\end{bmatrix}.\end{aligned}
$$

Answer selection: \begin{bmatrix}6 \\ -1 \\ 3\end{bmatrix}

Question 17592186120351 — question.difficulty/easy

Find the value of $x_{1} + x_{2}$ given that $2\mathbf{a}-6\mathbf{x}=\mathbf{b}$ and
$$
\mathbf{a}=\begin{bmatrix}-2 \\ 5 \\ 1 \\ 3\end{bmatrix},\hspace{1em}\mathbf{x}=\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3} \\ {x}_{4}\end{bmatrix},\hspace{1em}\mathbf{b}=\begin{bmatrix}8 \\ 4 \\ -22 \\ -6\end{bmatrix}.
$$

Solution: Using the properties of addition/subtraction and scalar multiplication of vectors to isolate $x$, we get

$$
\begin{aligned}
2a-6x&=b\\
x&=\frac16(2a-b)\\
&=\frac16\left(\begin{bmatrix}-4\\10\\2\\6\end{bmatrix}-\begin{bmatrix}8\\4\\-22\\-6\end{bmatrix}\right)\\
&=\frac16\begin{bmatrix}-12\\6\\24\\12\end{bmatrix}
=\begin{bmatrix}-2\\1\\4\\2\end{bmatrix}.
\end{aligned}
$$

Therefore, $x_1+x_2=-2+1=-1$.

Answer selection: -1

Question 17592186240986 — question.difficulty/easy

Find $\mathbf{x}$, if $4\mathbf{a}+3\mathbf{x}=\mathbf{b}$ and

$$
\mathbf{a}=\begin{bmatrix}3 \\ -1 \\ -4\end{bmatrix},\hspace{1em}\mathbf{b}=\begin{bmatrix}3 \\ 2 \\ -1\end{bmatrix}.
$$

Solution: Using the properties of addition/subtraction and scalar multiplication of vectors to isolate $\mathbf{x},$ we get

$$
\begin{aligned}4\mathbf{a}+3\mathbf{x} & =\mathbf{b} \\ 3\mathbf{x} & =\mathbf{b}-4\mathbf{a} \\ \mathbf{x} & =\frac{1}{3}(\mathbf{b}-4\mathbf{a}) \\ \mathbf{x} & =\frac{1}{3}\left(\begin{bmatrix}3 \\ 2 \\ -1\end{bmatrix}-4\begin{bmatrix}3 \\ -1 \\ -4\end{bmatrix}\right) \\ \mathbf{x} & =\frac{1}{3}\begin{bmatrix}-9 \\ 6 \\ 15\end{bmatrix} \\ \mathbf{x} & =\begin{bmatrix}-3 \\ 2 \\ 5\end{bmatrix}.\end{aligned}
$$

Answer selection: \begin{bmatrix}-3 \\ 2 \\ 5\end{bmatrix}

### Solving for Two Coefficients in a Linear Combination (31 captured questions)

Question 17592186120293 — question.difficulty/moderate

Consider the vectors

$$
{\mathbf{a}}_{\mathbf{1}}=\begin{bmatrix}-1 \\ -1 \\ 0\end{bmatrix},\hspace{1em}{\mathbf{a}}_{\mathbf{2}}=\begin{bmatrix}2 \\ 1 \\ 1\end{bmatrix},\hspace{1em}\mathbf{b}=\begin{bmatrix}5 \\ 3 \\ 2\end{bmatrix}.
$$

If ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}=\mathbf{b},$ then what is ${x}_{1}+{x}_{2}?$

Solution: If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}=b$, then we have

$$
\begin{aligned}{x}_{1}\begin{bmatrix}-1 \\ -1 \\ 0\end{bmatrix}+{x}_{2}\begin{bmatrix}2 \\ 1 \\ 1\end{bmatrix} & =\begin{bmatrix}5 \\ 3 \\ 2\end{bmatrix} \\ \begin{bmatrix}-{x}_{1} \\ -{x}_{1} \\ 0\end{bmatrix}+\begin{bmatrix}2{x}_{2} \\ {x}_{2} \\ {x}_{2}\end{bmatrix} & =\begin{bmatrix}5 \\ 3 \\ 2\end{bmatrix} \\ \begin{bmatrix}-{x}_{1}+2{x}_{2} \\ -{x}_{1}+{x}_{2} \\ {x}_{2}\end{bmatrix} & =\begin{bmatrix}5 \\ 3 \\ 2\end{bmatrix}.\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}-{x}_{1}+2{x}_{2} &=5 \\ -{x}_{1}+{x}_{2} &=3 \\ {x}_{2} &=2\end{aligned}\right.
$$

From the third equation we get ${x}_{2}=2$, which we substitute into the second equation to get 

$$
\begin{aligned}-{x}_{1}+{x}_{2} & =3 \\ -{x}_{1}+2 & =3 \\ {x}_{1} & =-1.\end{aligned}
$$

Finally, we substitute ${x}_{1}=-1$ and ${x}_{2}=2$ into the first equation to get

$$
\begin{aligned}-{x}_{1}+2{x}_{2} & =5 \\ -(-1)+2(2) & =5 \\ 5 & =5,\end{aligned}
$$

which gives a true statement. 

So the solution of the system is ${x}_{1}=-1$ and ${x}_{2}=2,$ which means

$$
-{a}_{1}+2{a}_{2}=b.
$$

Consequently, 

$$
{x}_{1}+{x}_{2}=-1+2=1.
$$

Answer selection: 1

Question 17592186120350 — question.difficulty/moderate

Consider the vectors

$$
{\mathbf{c}}_{\mathbf{1}}=\begin{bmatrix}-1 \\ 3 \\ 5\end{bmatrix},\hspace{1em}{\mathbf{c}}_{\mathbf{2}}=\begin{bmatrix}4 \\ 1 \\ 2\end{bmatrix},\hspace{1em}\mathbf{d}=\begin{bmatrix}3 \\ 4 \\ 5\end{bmatrix}.
$$

If ${x}_{1}{\mathbf{c}}_{1}+{x}_{2}{\mathbf{c}}_{2}=\mathbf{d},$ then what is ${x}_{1}+{x}_{2}?$

Solution: If ${x}_{1}{\mathbf{c}}_{1}+{x}_{2}{\mathbf{c}}_{2}=\mathbf{d},$ then we have

$$
\begin{aligned}{x}_{1}\begin{bmatrix}-1 \\ 3 \\ 5\end{bmatrix}+{x}_{2}\begin{bmatrix}4 \\ 1 \\ 2\end{bmatrix} & =\begin{bmatrix}3 \\ 4 \\ 5\end{bmatrix} \\ \begin{bmatrix}-{x}_{1} \\ 3{x}_{1} \\ 5{x}_{1}\end{bmatrix}+\begin{bmatrix}4{x}_{2} \\ {x}_{2} \\ 2{x}_{2}\end{bmatrix} & =\begin{bmatrix}3 \\ 4 \\ 5\end{bmatrix} \\ \begin{bmatrix}-{x}_{1}+4{x}_{2} \\ 3{x}_{1}+{x}_{2} \\ 5{x}_{1}+2{x}_{2}\end{bmatrix} & =\begin{bmatrix}3 \\ 4 \\ 5\end{bmatrix}.\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}-{x}_{1}+4{x}_{2} &=3 \\ 3{x}_{1}+{x}_{2} &=4 \\ 5{x}_{1}+2{x}_{2} &=5\end{aligned}\right.
$$

Multiplying the first equation by $3$ and adding the result to the second equation, we get

$$
\begin{aligned}13{x}_{2} & =13\,⟹\,{x}_{2}=1.\end{aligned}
$$

Substituting ${x}_{2}=1$ into the first equation, we get

$$
\begin{aligned}-{x}_{1}+4(1) & =3\,⟹\,{x}_{1}=1.\end{aligned}
$$

Finally, substituting ${x}_{1}=1$ and ${x}_{2}=1$ into the third equation, we obtain

$$
\begin{aligned}5{x}_{1}+2{x}_{2} & =5 \\ 5(1)+2(1) & =5 \\ 7 & =5,\end{aligned}
$$

which gives a false statement. 

So, the system has no solution.

Answer selection: No solution

Question 17592186240990 — question.difficulty/moderate

Consider the vectors

$$
{\mathbf{a}}_{\mathbf{1}}=\begin{bmatrix}1 \\ -2 \\ 3\end{bmatrix},\hspace{1em}{\mathbf{a}}_{\mathbf{2}}=\begin{bmatrix}2 \\ -3 \\ 5\end{bmatrix},\hspace{1em}\mathbf{b}=\begin{bmatrix}-3 \\ 1 \\ -4\end{bmatrix}.
$$

If ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}=\mathbf{b},$ then what is ${x}_{1}+{x}_{2}?$

Solution: If ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}=\mathbf{b}$, then we have

$$
\begin{aligned}{x}_{1}\begin{bmatrix}1 \\ -2 \\ 3\end{bmatrix}+{x}_{2}\begin{bmatrix}2 \\ -3 \\ 5\end{bmatrix} & =\begin{bmatrix}-3 \\ 1 \\ -4\end{bmatrix} \\ \begin{bmatrix}{x}_{1} \\ -2{x}_{1} \\ 3{x}_{1}\end{bmatrix}+\begin{bmatrix}2{x}_{2} \\ -3{x}_{2} \\ 5{x}_{2}\end{bmatrix} & =\begin{bmatrix}-3 \\ 1 \\ -4\end{bmatrix} \\ \begin{bmatrix}{x}_{1}+2{x}_{2} \\ -2{x}_{1}-3{x}_{2} \\ 3{x}_{1}+5{x}_{2}\end{bmatrix} & =\begin{bmatrix}-3 \\ 1 \\ -4\end{bmatrix}.\end{aligned}
$$

 

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}{x}_{1}+2{x}_{2} &=-3 \\ -2{x}_{1}-3{x}_{2} &=1 \\ 3{x}_{1}+5{x}_{2} &=-4\end{aligned}\right.
$$

Multiplying the first equation by $2$ and adding the resulting equations, we obtain 

$$
\begin{aligned}{x}_{2} & =-5,\end{aligned}
$$

which we substitute into the second equation to get 

$$
\begin{aligned}-2{x}_{1}-3{x}_{2}=1 \\ -2{x}_{1}-3(-5) & =1 \\ -2{x}_{1} & =-14 \\ {x}_{1} & =7.\end{aligned}
$$

Finally, we substitute ${x}_{1}=7$ and ${x}_{2}=-5$ into the third equation and obtain

$$
\begin{aligned}3{x}_{1}+5{x}_{2}=-4 \\ 3(7)+5(-5) & =-4 \\ -4 & =-4,\end{aligned}
$$

which gives a true statement. 

So the solution of the system is ${x}_{1}=7$ and ${x}_{2}=-5,$ which means

$$
7{\mathbf{a}}_{\mathbf{1}}-5{\mathbf{a}}_{\mathbf{2}}=\mathbf{b}.
$$

Consequently, 

$$
{x}_{1}+{x}_{2}=7+(-5)=2.
$$

Answer selection: 2

### Solving for Three Coefficients in a Linear Combination (28 captured questions)

Question 17592186120309 — question.difficulty/moderate

Consider the vectors

$$
{\mathbf{a}}_{\mathbf{1}}=\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix},\hspace{1em}{\mathbf{a}}_{\mathbf{2}}=\begin{bmatrix}-1 \\ 1 \\ 1\end{bmatrix},\hspace{1em}{\mathbf{a}}_{\mathbf{3}}=\begin{bmatrix}2 \\ 0 \\ 5\end{bmatrix},\hspace{1em}\mathbf{b}=\begin{bmatrix}2 \\ 3 \\ -1\end{bmatrix}.
$$

If ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{b},$ then what is ${x}_{1}+{x}_{2}+{x}_{3}?$

Solution: If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b$, then we have  

$$
\begin{aligned}{x}_{1}\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix}+{x}_{2}\begin{bmatrix}-1 \\ 1 \\ 1\end{bmatrix}+{x}_{3}\begin{bmatrix}2 \\ 0 \\ 5\end{bmatrix} & =\begin{bmatrix}2 \\ 3 \\ -1\end{bmatrix} \\ \begin{bmatrix}{x}_{1} \\ 0 \\ {x}_{1}\end{bmatrix}+\begin{bmatrix}-{x}_{2} \\ {x}_{2} \\ {x}_{2}\end{bmatrix}+\begin{bmatrix}2{x}_{3} \\ 0 \\ 5{x}_{3}\end{bmatrix} & =\begin{bmatrix}2 \\ 3 \\ -1\end{bmatrix} \\ \begin{bmatrix}{x}_{1}-{x}_{2}+2{x}_{3} \\ {x}_{2} \\ {x}_{1}+{x}_{2}+5{x}_{3}\end{bmatrix} & =\begin{bmatrix}2 \\ 3 \\ -1\end{bmatrix}.\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}{x}_{1}-{x}_{2}+2{x}_{3} &=2 \\ {x}_{2} &=3 \\ {x}_{1}+{x}_{2}+5{x}_{3} &=-1\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & -1 & 2 & 2 \\ 0 & 1 & 0 & 3 \\ 1 & 1 & 5 & -1\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}1 & -1 & 2 & 2 \\ 0 & 1 & 0 & 3 \\ 1 & 1 & 5 & -1\end{array}\right] & {R}_{3} & :={R}_{3}-{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 2 & 2 \\ 0 & 1 & 0 & 3 \\ 0 & 2 & 3 & -3\end{array}\right] & {R}_{3} & :={R}_{3}-2{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 2 & 2 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 3 & -9\end{array}\right] & {R}_{3} & :=\frac{1}{3}{R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 2 & 2 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 1 & -3\end{array}\right].\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}{x}_{1}-{x}_{2}+2{x}_{3} &=2 \\ {x}_{2} &=3 \\ {x}_{3} &=-3.\end{aligned}\right.
$$

From the third equation, we get ${x}_{3}=-3$ and from the second equation we get ${x}_{2}=3.$ Substituting these into the first equation, we obtain

$$
{x}_{1}-3+2(-3)=2\,⟹\,{x}_{1}=11.
$$

So, the solution of the system is ${x}_{1}=11$, ${x}_{2}=3$, and ${x}_{3}=-3,$ which means 

$$
11{a}_{1}+3{a}_{2}-3{a}_{3}=b.
$$

Consequently, 

$$
{x}_{1}+{x}_{2}+{x}_{3}=11+3-3=11.
$$

Answer selection: 11

Question 17592186120349 — question.difficulty/hard

Consider the vectors

$$
{\mathbf{a}}_{\mathbf{1}}=\begin{bmatrix}1 \\ 2 \\ 3\end{bmatrix},\hspace{1em}{\mathbf{a}}_{\mathbf{2}}=\begin{bmatrix}2 \\ 5 \\ 6\end{bmatrix},\hspace{1em}{\mathbf{a}}_{\mathbf{3}}=\begin{bmatrix}3 \\ 2 \\ 9\end{bmatrix},\hspace{1em}\mathbf{b}=\begin{bmatrix}-2 \\ -6 \\ 7\end{bmatrix}.
$$

If ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{b},$ then what is ${x}_{1}+{x}_{2}+{x}_{3}?$

Solution: If ${x}_{1}{\mathbf{a}}_{\mathbf{1}}+{x}_{2}{\mathbf{a}}_{\mathbf{2}}+{x}_{3}{\mathbf{a}}_{\mathbf{3}}=\mathbf{b}$, then we have

$$
\begin{aligned}{x}_{1}\begin{bmatrix}1 \\ 2 \\ 3\end{bmatrix}+{x}_{2}\begin{bmatrix}2 \\ 5 \\ 6\end{bmatrix}+{x}_{3}\begin{bmatrix}3 \\ 2 \\ 9\end{bmatrix} & =\begin{bmatrix}-2 \\ -6 \\ 7\end{bmatrix} \\ \begin{bmatrix}{x}_{1} \\ 2{x}_{1} \\ 3{x}_{1}\end{bmatrix}+\begin{bmatrix}2{x}_{2} \\ 5{x}_{2} \\ 6{x}_{2}\end{bmatrix}+\begin{bmatrix}3{x}_{3} \\ 2{x}_{3} \\ 9{x}_{3}\end{bmatrix} & =\begin{bmatrix}-2 \\ -6 \\ 7\end{bmatrix} \\ \begin{bmatrix}{x}_{1}+2{x}_{2}+3{x}_{3} \\ 2{x}_{1}+5{x}_{2}+2{x}_{3} \\ 3{x}_{1}+6{x}_{2}+9{x}_{3}\end{bmatrix} & =\begin{bmatrix}-2 \\ -6 \\ 7\end{bmatrix}.\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}{x}_{1}+2{x}_{2}+3{x}_{3} &=-2 \\ 2{x}_{1}+5{x}_{2}+2{x}_{3} &=-6 \\ 3{x}_{1}+6{x}_{2}+9{x}_{3} &=7\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & 2 & 3 & -2 \\ 2 & 5 & 2 & -6 \\ 3 & 6 & 9 & 7\end{array}\right].
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}1 & 2 & 3 & -2 \\ 2 & 5 & 2 & -6 \\ 3 & 6 & 9 & 7\end{array}\right] & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 2 & 3 & -2 \\ 0 & 1 & -4 & -2 \\ 3 & 6 & 9 & 7\end{array}\right] & {R}_{3} & :={R}_{3}+(-3){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 2 & 3 & -2 \\ 0 & 1 & -4 & -2 \\ 0 & 0 & 0 & 13\end{array}\right].\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}{x}_{1}+2{x}_{2}+3{x}_{3} &=-2 \\ {x}_{2}-4{x}_{3} &=-2 \\ 0 &=13.\end{aligned}\right.
$$

However, the final equation $0=13$  gives a false statement. So the system has no solution.

Answer selection: No solution

Question 17592186240992 — question.difficulty/moderate

Consider the vectors

$$
{\mathbf{a}}_{\mathbf{1}}=\begin{bmatrix}1 \\ 3 \\ -2\end{bmatrix},\hspace{1em}{\mathbf{a}}_{\mathbf{2}}=\begin{bmatrix}-3 \\ -8 \\ 6\end{bmatrix},\hspace{1em}{\mathbf{a}}_{\mathbf{3}}=\begin{bmatrix}2 \\ 5 \\ -3\end{bmatrix},\hspace{1em}\mathbf{b}=\begin{bmatrix}2 \\ 1 \\ 2\end{bmatrix}.
$$

If ${x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}=\mathbf{b},$ then what is ${x}_{1}+{x}_{2}+{x}_{3}?$

Solution: If ${x}_{1}{\mathbf{a}}_{\mathbf{1}}+{x}_{2}{\mathbf{a}}_{\mathbf{2}}+{x}_{3}{\mathbf{a}}_{\mathbf{3}}=\mathbf{b}$, then we have  

$$
\begin{aligned}{x}_{1}\begin{bmatrix}1 \\ 3 \\ -2\end{bmatrix}+{x}_{2}\begin{bmatrix}-3 \\ -8 \\ 6\end{bmatrix}+{x}_{3}\begin{bmatrix}2 \\ 5 \\ -3\end{bmatrix} & =\begin{bmatrix}2 \\ 1 \\ 2\end{bmatrix} \\ \begin{bmatrix}{x}_{1} \\ 3{x}_{1} \\ -2{x}_{1}\end{bmatrix}+\begin{bmatrix}-3{x}_{2} \\ -8{x}_{2} \\ 6{x}_{2}\end{bmatrix}+\begin{bmatrix}2{x}_{3} \\ 5{x}_{3} \\ -3{x}_{3}\end{bmatrix} & =\begin{bmatrix}2 \\ 1 \\ 2\end{bmatrix} \\ \begin{bmatrix}{x}_{1}-3{x}_{2}+2{x}_{3} \\ 3{x}_{1}-8{x}_{2}+5{x}_{3} \\ -2{x}_{1}+6{x}_{2}-3{x}_{3}\end{bmatrix} & =\begin{bmatrix}2 \\ 1 \\ 2\end{bmatrix}.\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}{x}_{1}-3{x}_{2}+2{x}_{3} &=2 \\ 3{x}_{1}-8{x}_{2}+5{x}_{3} &=1 \\ -2{x}_{1}+6{x}_{2}-3{x}_{3} &=2\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & -3 & 2 & 2 \\ 3 & -8 & 5 & 1 \\ -2 & 6 & -3 & 2\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}1 & -3 & 2 & 2 \\ 3 & -8 & 5 & 1 \\ -2 & 6 & -3 & 2\end{array}\right] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -3 & 2 & 2 \\ 0 & 1 & -1 & -5 \\ -2 & 6 & -3 & 2\end{array}\right] & {R}_{3} & :={R}_{3}+2{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -3 & 2 & 2 \\ 0 & 1 & -1 & -5 \\ 0 & 0 & 1 & 6\end{array}\right].\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}{x}_{1}-3{x}_{2}+2{x}_{3} &=2 \\ {x}_{2}-{x}_{3} &=-5 \\ {x}_{3} &=6.\end{aligned}\right.
$$

From the third equation, we get ${x}_{3}=6.$ Substituting ${x}_{3}=6$ into the second equation, we obtain

$$
{x}_{2}-6=-5\,⟹\,{x}_{2}=1.
$$

Now, substituting ${x}_{2}=1$ and ${x}_{3}=6$ into the first equation, we obtain

$$
{x}_{1}-3(1)+2(6)=2\,⟹\,{x}_{1}=-7.
$$

So, the solution of the system is ${x}_{1}=-7$, ${x}_{2}=1$, and ${x}_{3}=6,$ which means 

$$
-7{\mathbf{a}}_{\mathbf{1}}+{\mathbf{a}}_{\mathbf{2}}+6{\mathbf{a}}_{\mathbf{3}}=\mathbf{b}.
$$

Consequently, 

$$
{x}_{1}+{x}_{2}+{x}_{3}=-7+1+6=0.
$$

Answer selection: 0
