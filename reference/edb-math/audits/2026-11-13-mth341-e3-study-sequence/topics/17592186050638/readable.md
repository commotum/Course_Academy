# 17592186050638 Expressing the Coordinates of a Vector in a Given Basis

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186121042 — Introduction

Given a subspace $H$ with a basis $\mathcal B = \{ \mathbf b_1, \mathbf b_2 \}$ and a vector $\mathbf x \in H,$ the **coordinates of the vector** $\mathbf{x}$ **relative to the basis** $\mathcal{B}$ are the coefficients ${\color{red} x_1}$ and ${\color{blue} x_2}$ such that

$$
{\color{red}x_1} \mathbf{b}_1+{\color{blue}x_2} \mathbf{b}_2 = \mathbf{x}.
$$

We can write the vector $\mathbf x$ relative to the basis $\mathcal B$ using these coordinates, as follows:

$$
[\mathbf{x}]_{\mathcal{B}} = {\left[ \begin{array}{c}{\color{red}{x}_{1}} \\ {\color{blue}{x}_{2}}\end{array} \right]}
$$

To demonstrate, consider the basis $\mathcal{B}=\{ \mathbf{b}_1, \mathbf{b}_2 \},$ where 

$$
\mathbf{b}_1={\left[ \begin{array}{c}2 \\ 0 \\ 0\end{array} \right]}, \qquad
	\mathbf{b}_2={\left[ \begin{array}{c}1 \\ 2 \\ 0\end{array} \right]}.
$$

Also let $H = \textrm{span} \{ \mathbf b_1, \mathbf b_2 \},$ and consider the vector $\mathbf{x} = {\left[ \begin{array}{c}8 \\ 4 \\ 0\end{array} \right]}\in H.$

The vector $\mathbf x$ can be expressed as a unique linear combination of $\mathbf b_1$ and $\mathbf b_2.$ That is to say, there exist *unique coefficients* $\color{red}x_1$ and $\color{blue}x_2$ such that

$$
\begin{aligned}{\color{red}{{x}_{1}}}{\mathbf{b}}_{1}+{\color{blue}{{x}_{2}}}{\mathbf{b}}_{2} & =\mathbf{x} \\ {\color{red}{{x}_{1}}}\begin{bmatrix}2 \\ 0 \\ 0\end{bmatrix}+{\color{blue}{{x}_{2}}}\begin{bmatrix}1 \\ 2 \\ 0\end{bmatrix} & =\begin{bmatrix}8 \\ 4 \\ 0\end{bmatrix}.\end{aligned}
$$

Let's solve for these coefficients. From the above, we get the following system:

$$
\left\{\begin{aligned}2{\color{red}{{x}_{1}}}+{\color{blue}{{x}_{2}}} &=8 \\ 2{\color{blue}{{x}_{2}}} &=4\end{aligned}\right.
$$

The unique solution of this system is 

$$
[\mathbf{x}]_{\mathcal{B}} = {\left[ \begin{array}{c}{\color{red}{x}_{1}} \\ {\color{blue}{x}_{2}}\end{array} \right]} = {\left[ \begin{array}{c}{\color{red}3} \\ {\color{blue}2}\end{array} \right]}.
$$

Therefore, we have that 

$$
\mathbf{x} = {\color{red}3} \mathbf{b}_1+ {\color{blue}2} \mathbf{b}_2,
$$

which can be visualized as shown below.

![](images/94/94b2934727a32284e9790e59ccd301bd858a0258843314a2968285a5eda7a302.png)



### example 17592186119631 — Finding a Vector Given Its Coordinates Relative To a Given Basis

Find the vector $\mathbf{x}$ if $\,\mathcal{B}=\{ \mathbf{b}_1, \mathbf{b}_2 \}$ is a basis of $\textrm{Span}\{ \mathbf{b}_1, \mathbf{b}_2 \},$ and
$$
\mathbf{b_1}={\left[ \begin{array}{c}3 \\ - 4 \\ 0\end{array} \right]}, 
	\qquad 
	\mathbf{b_2}={\left[ \begin{array}{c}1 \\ 0 \\ 2\end{array} \right]},
	\qquad
	[\mathbf{x}]_{\mathcal{B}}={\left[ \begin{array}{c}- 1 \\ 3\end{array} \right]}.
$$

We know that any vector in  $\textrm{Span}\{ \mathbf{b}_1, \mathbf{b}_2 \}$ has the form

$$
\begin{aligned}{x}_{1}\begin{bmatrix}3 \\ -4 \\ 0\end{bmatrix}+{x}_{2}\begin{bmatrix}1 \\ 0 \\ 2\end{bmatrix}\end{aligned}
$$

where $x_1$ and $x_2$ are the coordinates relative to the basis $\,\mathcal{B}.$ Since we are told that $[\mathbf{x}]_{\mathcal{B}} = {\left[ \begin{array}{c}- 1 \\ 3\end{array} \right]},$ we obtain

$$
\begin{aligned}\mathbf{x} & =\underbrace{(-1)}_{{x}_{1}}\begin{bmatrix}3 \\ -4 \\ 0\end{bmatrix}+\underbrace{(\hspace{0.222em}3\hspace{0.222em})}_{{x}_{2}}\begin{bmatrix}1 \\ 0 \\ 2\end{bmatrix} \\  & =\begin{bmatrix}-3 \\ 4 \\ 0\end{bmatrix}+\begin{bmatrix}3 \\ 0 \\ 6\end{bmatrix} \\  & =\begin{bmatrix}0 \\ 4 \\ 6\end{bmatrix}.\end{aligned}
$$

### example 17592186119674 — Finding the Coordinates of a Vector Relative To a Given Basis by Inspection

Find the coordinates of the vector $\mathbf{x}$ relative to the basis $\mathcal{B}=\{ \mathbf{b}_1, \mathbf{b}_2 \},$ where
$$
\mathbf{b_1}={\left[ \begin{array}{c}0 \\ 0 \\ 1\end{array} \right]}, \qquad
	\mathbf{b_2}={\left[ \begin{array}{c}0 \\ 1 \\ 0\end{array} \right]}, \qquad
	\mathbf{x}={\left[ \begin{array}{c}0 \\ 2 \\ - 5\end{array} \right]}.
$$

Remember, the order of the vectors in a basis is important.

Notice that 

$$
\underbrace{ {\left[ \begin{array}{c}0 \\ 2 \\ - 5\end{array} \right]}}_{\mathbf{x}} = \underbrace{(\,-5\,)}_{x_1} \cdot \underbrace{ {\left[ \begin{array}{c}0 \\ 0 \\ 1\end{array} \right]}}_{\mathbf{b}_1} + \underbrace{(\:2\:)}_{x_2} \cdot \underbrace{ {\left[ \begin{array}{c}0 \\ 1 \\ 0\end{array} \right]}}_{\mathbf{b}_2}
$$

which means that

$$
\mathbf{x} = (-5) \cdot \mathbf{b}_1 + 2 \cdot \mathbf{b}_2
$$

and therefore

$$
[\mathbf{x}]_{\mathcal{B}} = {\left[ \begin{array}{c}- 5 \\ 2\end{array} \right]}.
$$

### example 17592186119632 — Finding the Coordinates of a Vector Relative To a Given Basis Containing Two Vectors

Find the coordinates of the vector $\mathbf{x}$ relative to the basis $\mathcal{B}=\{ \mathbf{b}_1, \mathbf{b}_2 \},$ where
$$
\mathbf{b_1}={\left[ \begin{array}{c}1 \\ 3 \\ 4\end{array} \right]}, \qquad
	\mathbf{b_2}={\left[ \begin{array}{c}3 \\ 5 \\ 0\end{array} \right]}, \qquad
	\mathbf{x}={\left[ \begin{array}{c}- 5 \\ - 11 \\ - 8\end{array} \right]}.
$$

We need to find $x_1$ and $x_2$ such that 

$$
\begin{aligned}{x}_{1}{\mathbf{b}}_{1}+{x}_{2}{\mathbf{b}}_{2} & =\mathbf{x} \\ {x}_{1}\begin{bmatrix}1 \\ 3 \\ 4\end{bmatrix}+{x}_{2}\begin{bmatrix}3 \\ 5 \\ 0\end{bmatrix} & =\begin{bmatrix}-5 \\ -11 \\ -8\end{bmatrix}.\end{aligned}
$$

The equation above gives the system with the augmented matrix
$$
M =	 \left[{\begin{array}{cc|c}1 & 3 & - 5 \\ 3 & 5 & - 11 \\ 4 & 0 & - 8\end{array}}\right].
$$

Row-reducing the matrix using Gaussian elimination, we obtain the following:

$$
\begin{aligned}M & =\left[\begin{array}{cc|c}1 & 3 & -5 \\ 3 & 5 & -11 \\ 4 & 0 & -8\end{array}\right] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 3 & -5 \\ 0 & -4 & 4 \\ 4 & 0 & -8\end{array}\right] & {R}_{3} & :={R}_{3}+(-4){R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 3 & -5 \\ 0 & -4 & 4 \\ 0 & -12 & 12\end{array}\right] & {R}_{3} & :={R}_{3}+(-3){R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & 3 & -5 \\ 0 & -4 & 4 \\ 0 & 0 & 0\end{array}\right]\end{aligned}
$$

The augmented matrix above corresponds to the following system of equations: 

$$
\left\{\begin{aligned}{x}_{1}+3{x}_{2} &=-5 \\ -4{x}_{2} &=4\end{aligned}\right.
$$

From the second equation, we get $x_2 =-1.$ Substituting this into the first equation, we obtain

$$
x_1 + 3 \left( -1 \right)  = -5
\qquad \Longrightarrow \qquad
x_1 = -2.
$$

Therefore, $[\mathbf{x}]_{\mathcal{B}} = {\left[ \begin{array}{c}- 2 \\ - 1\end{array} \right]}.$

### example 17592186119633 — Finding the Coordinates of a Vector Relative To a Given Basis Containing More Than Two Vectors

Find the coordinates of the vector $\mathbf{x}$ relative to the basis $\mathcal{B}=\{ \mathbf{b}_1, \mathbf{b}_2, \mathbf{b}_3 \},$ where
$$
\mathbf{b_1}={\left[ \begin{array}{c}1 \\ 0 \\ 1\end{array} \right]}, \quad
	\mathbf{b_2}={\left[ \begin{array}{c}3 \\ - 9 \\ 0\end{array} \right]}, \quad
	\mathbf{b_3}={\left[ \begin{array}{c}0 \\ - 1 \\ 1\end{array} \right]}, \quad
	\mathbf{x}={\left[ \begin{array}{c}1 \\ 7 \\ 6\end{array} \right]}.
$$

We need to find $x_1,$ $x_2,$ and $x_3$ such that 

$$
\begin{aligned}{x}_{1}{\mathbf{b}}_{\mathbf{1}}+{x}_{2}{\mathbf{b}}_{\mathbf{2}}+{x}_{3}{\mathbf{b}}_{\mathbf{3}} & =\mathbf{x} \\ {x}_{1}\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix}+{x}_{2}\begin{bmatrix}3 \\ -9 \\ 0\end{bmatrix}+{x}_{3}\begin{bmatrix}0 \\ -1 \\ 1\end{bmatrix} & =\begin{bmatrix}1 \\ 7 \\ 6\end{bmatrix}.\end{aligned}
$$

Writing the above system as an augmented matrix $M$ and reducing using Gaussian elimination, we get the following:

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}1 & 3 & 0 & 1 \\ 0 & -9 & -1 & 7 \\ 1 & 0 & 1 & 6\end{array}\right] & {R}_{3} & :={R}_{3}+(-1){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 3 & 0 & 1 \\ 0 & -9 & -1 & 7 \\ 0 & -3 & 1 & 5\end{array}\right] & {R}_{3} & :={R}_{3}+\left(-\frac{1}{3}\right){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 3 & 0 & 1 \\ 0 & -9 & -1 & 7 \\ 0 & 0 & \frac{4}{3} & \frac{8}{3}\end{array}\right]\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}{x}_{1}+3{x}_{2} &=1 \\ -9{x}_{2}-{x}_{3} &=7 \\ \frac{4}{3}{x}_{3} &=\frac{8}{3}.\end{aligned}\right.
$$

From the third equation, we get $x_3 =2.$ Substituting this into the second equation, we obtain

$$
-9x_2 - 2 = 7 \qquad\Longrightarrow\qquad x_2 = -1,
$$

and substituting $x_2=-1$ into the first equation, we get

$$
x_1+3(-1) = 1 \qquad\Longrightarrow\quad x_1 = 4.
$$

Therefore, $[\mathbf{x}]_{\mathcal{B}}={\left[ \begin{array}{c}4 \\ - 1 \\ 2\end{array} \right]}.$

### tutorial 17592186121066 — The Standard Basis

Let's consider a set of vectors
$$
\mathcal{S} = 
	\Bigg\{
		\underbrace{\color{blue} {\left[ \begin{array}{c}1 \\ 0 \\ 0\end{array} \right]}}_{\color{blue} \mathbf{e}_1}, 
		\underbrace{\color{blue} {\left[ \begin{array}{c}0 \\ 1 \\ 0\end{array} \right]}}_{\color{blue} \mathbf{e}_2}, 
		\underbrace{\color{blue} {\left[ \begin{array}{c}0 \\ 0 \\ 1\end{array} \right]}}_{\color{blue} \mathbf{e}_3}
	\Bigg\}.
$$

Notice that the set $\mathcal{S}$ is linearly independent since the vector equation $x_1\mathbf{e}_1+x_2\mathbf{e}_2+x_3\mathbf{e}_3=\mathbf{0}$ leads to the system

$$
\left\{\begin{aligned}{x}_{1} &=0 \\ {x}_{2} &=0 \\ {x}_{3} &=0,\end{aligned}\right.
$$

which has only the zero solution. 

Also, notice that any vector in $\mathbb{R}^3$ can be written as a linear combination of $\mathbf{e}_1,$ $\mathbf{e}_2,$ and $\mathbf{e}_3.$ For instance,
$$
\mathbf{v} = 
	{\left[ \begin{array}{c}{\color{red}- 2} \\ {\color{red}0} \\ {\color{red}5}\end{array} \right]} = 
	{\color{red}-2} \cdot {\color{blue} {\left[ \begin{array}{c}1 \\ 0 \\ 0\end{array} \right]}} +
	{\color{red}0} \cdot {\color{blue} {\left[ \begin{array}{c}0 \\ 1 \\ 0\end{array} \right]}} +
	{\color{red}5} {\color{blue} {\left[ \begin{array}{c}0 \\ 0 \\ 1\end{array} \right]}}.
$$

In particular, the equation above tells us that 
$$
[ \mathbf{v} ]_{\mathcal{S}} =  {\left[ \begin{array}{c}{\color{red}- 2} \\ {\color{red}0} \\ {\color{red}5}\end{array} \right]},
$$
that is to say, the numbers $\color{red}-2,$ $\color{red}0,$ $\color{red}5$ are the coordinates of $\mathbf{v}$ relative to the basis $\mathcal{S}.$ 

The basis $\mathcal{S}$ is somewhat special, since the coordinates of a vector relative to this basis coincide with the components of the vector. We refer to $\mathcal{S}$ as the **standard basis**. Remember that in $\mathbb{R}^2$ and $\mathbb{R}^3$ we even have special notations for the vectors of the standard basis:
$$
\mathbb{R}^2:
	\Bigg\{
		\underbrace{\color{blue} {\left[ \begin{array}{c}1 \\ 0\end{array} \right]}}_{\color{blue}\mathbf{i}}, 
		\underbrace{\color{blue} {\left[ \begin{array}{c}0 \\ 1\end{array} \right]}}_{\color{blue}\mathbf{j}}
	\Bigg\},
	\qquad\qquad
	\mathbb{R}^3:
	\Bigg\{
		\underbrace{\color{blue} {\left[ \begin{array}{c}1 \\ 0 \\ 0\end{array} \right]}}_{\color{blue}\mathbf{i}}, 
		\underbrace{\color{blue} {\left[ \begin{array}{c}0 \\ 1 \\ 0\end{array} \right]}}_{\color{blue}\mathbf{j}}, 
		\underbrace{\color{blue} {\left[ \begin{array}{c}0 \\ 0 \\ 1\end{array} \right]}}_{\color{blue}\mathbf{k}}
	\Bigg\}.
$$

![](images/dd/dd96e0b70173adf8983feb4975c351ab3e417c34ed4a6a944bc391e33db4c8e9.png)

In general, the standard basis of $\mathbb{R}^n$ is

$$
\left\{
{\left[ \begin{array}{c}1 \\ 0 \\ 0 \\ \vdots  \\ 0\end{array} \right]}, \:
{\left[ \begin{array}{c}0 \\ 1 \\ 0 \\ \vdots  \\ 0\end{array} \right]}, \:
{\left[ \begin{array}{c}0 \\ 0 \\ 1 \\ \vdots  \\ 0\end{array} \right]}, 
\quad \cdots \quad
{\left[ \begin{array}{c}0 \\ 0 \\ 0 \\ \vdots  \\ 1\end{array} \right]}
\right\}\!.
$$



## Representative practice (first three per skill; full bank in practice.json)

### Finding a Vector Given Its Coordinates Relative To a Given Basis (12 captured questions)

Question 17592186120379 — question.difficulty/easy

Find the vector $\mathbf{x}$, if $\mathcal{B}=\{{\mathbf{b}}_{1},{\mathbf{b}}_{2}\}$ is a basis of $\text{Span}\{{\mathbf{b}}_{1},{\mathbf{b}}_{2}\},$ and 

$$
{\mathbf{b}}_{1}=\begin{bmatrix}3 \\ -2 \\ 3\end{bmatrix},\hspace{2em}{\mathbf{b}}_{2}=\begin{bmatrix}5 \\ 3 \\ 4\end{bmatrix},\hspace{2em}[\mathbf{x}]_{\mathcal{B}}=\begin{bmatrix}-3 \\ 5\end{bmatrix}.
$$

Solution: We know that any vector in  $\text{Span}\{{b}_{1},{b}_{2}\}$ has the form

$$
\begin{aligned}{x}_{1}\begin{bmatrix}3 \\ -2 \\ 3\end{bmatrix}+{x}_{2}\begin{bmatrix}5 \\ 3 \\ 4\end{bmatrix}\end{aligned}
$$

where ${x}_{1}$ and ${x}_{2}$ are the coordinates relative to the basis $\,B.$ Since we are told that $[x]_{B}=\begin{bmatrix}-3 \\ 5\end{bmatrix},$ we obtain

$$
\begin{aligned}x & =\underbrace{(\,-3\,)}_{{x}_{1}}\begin{bmatrix}3 \\ -2 \\ 3\end{bmatrix}+\underbrace{(\,5\,)}_{{x}_{2}}\begin{bmatrix}5 \\ 3 \\ 4\end{bmatrix} \\  & =\begin{bmatrix}-9 \\ 6 \\ -9\end{bmatrix}+\begin{bmatrix}25 \\ 15 \\ 20\end{bmatrix} \\  & =\begin{bmatrix}16 \\ 21 \\ 11\end{bmatrix}.\end{aligned}
$$

Answer selection: \begin{bmatrix}16 \\ 21 \\ 11\end{bmatrix}

Question 17592186120382 — None

Find the vector $\mathbf{x}$, if $\mathcal{B}=\{{\mathbf{b}}_{1},{\mathbf{b}}_{2}\}$ is a basis of $\text{Span}\{{\mathbf{b}}_{1},{\mathbf{b}}_{2}\}$, and
$$
{\mathbf{b}}_{1}=\begin{bmatrix}3 \\ 2 \\ 5\end{bmatrix},\hspace{2em}{\mathbf{b}}_{2}=\begin{bmatrix}2 \\ 4 \\ 3\end{bmatrix},\hspace{2em}[\mathbf{x}]_{\mathcal{B}}=\begin{bmatrix}5 \\ -7\end{bmatrix}.
$$

Solution: The entries of $[x]_B$ are the coefficients of $b_1$ and $b_2$. Therefore,

$$
x=5b_1-7b_2=5\begin{bmatrix}3\\2\\5\end{bmatrix}-7\begin{bmatrix}2\\4\\3\end{bmatrix}=\begin{bmatrix}15-14\\10-28\\25-21\end{bmatrix}=\begin{bmatrix}1\\-18\\4\end{bmatrix}.
$$

Answer selection: \begin{bmatrix}1 \\ -18 \\ 4\end{bmatrix}

Question 17592186247247 — question.difficulty/easy

Find the vector $\mathbf{x}$, if $\mathcal{B}=\{{\mathbf{b}}_{1},{\mathbf{b}}_{2}\}$ is a basis of $\text{Span}\{{\mathbf{b}}_{1},{\mathbf{b}}_{2}\},$ and 

$$
{\mathbf{b}}_{1}=\begin{bmatrix}1 \\ -5 \\ -3\end{bmatrix},\hspace{2em}{\mathbf{b}}_{2}=\begin{bmatrix}2 \\ -3 \\ -1\end{bmatrix},\hspace{2em}[\mathbf{x}]_{\mathcal{B}}=\begin{bmatrix}6 \\ -7\end{bmatrix}.
$$

Solution: We know that any vector in  $\text{Span}\{{\mathbf{b}}_{1},{\mathbf{b}}_{2}\}$ has the form

$$
\begin{aligned}{x}_{1}\begin{bmatrix}1 \\ -5 \\ -3\end{bmatrix}+{x}_{2}\begin{bmatrix}2 \\ -3 \\ -1\end{bmatrix}\end{aligned}
$$

 

where ${x}_{1}$ and ${x}_{2}$ are the coordinates relative to the basis $\hspace{0.167em}\mathcal{B}.$ Since we are told that $[\mathbf{x}]_{\mathcal{B}}=\begin{bmatrix}6 \\ -7\end{bmatrix},$ we obtain

$$
\begin{aligned}\mathbf{x} & =\underbrace{(\hspace{0.167em}6\hspace{0.167em})}_{{x}_{1}}\begin{bmatrix}1 \\ -5 \\ -3\end{bmatrix}+\underbrace{(\hspace{0.222em}-7\hspace{0.222em})}_{{x}_{2}}\begin{bmatrix}2 \\ -3 \\ -1\end{bmatrix} \\  & =\begin{bmatrix}6 \\ -30 \\ -18\end{bmatrix}+\begin{bmatrix}-14 \\ 21 \\ 7\end{bmatrix} \\  & =\begin{bmatrix}-8 \\ -9 \\ -11\end{bmatrix}.\end{aligned}
$$

Answer selection: \begin{bmatrix}-8 \\ -9 \\ -11\end{bmatrix}

### Finding the Coordinates of a Vector Relative To a Given Basis by Inspection (14 captured questions)

Question 17592186120525 — question.difficulty/easy

Find the coordinates of the vector $\mathbf{x}$ relative to the basis $\mathcal{B}=\{{\mathbf{b}}_{1},{\mathbf{b}}_{2}\},$ where

$$
{\mathbf{b}}_{\mathbf{1}}=\begin{bmatrix}0 \\ 0 \\ 1\end{bmatrix},\hspace{2em}{\mathbf{b}}_{\mathbf{2}}=\begin{bmatrix}0 \\ 1 \\ 0\end{bmatrix},\hspace{2em}\mathbf{x}=\begin{bmatrix}0 \\ -4 \\ 2\end{bmatrix}.
$$

If $[\mathbf{x}]_{\mathcal{B}}=\begin{bmatrix}{x}_{1} \\ {x}_{2}\end{bmatrix}$ then what is the value of ${x}_{2}?$

Solution: Remember, the order of the vectors in a basis is important.

Notice that 

$$
\underbrace{\begin{bmatrix}0 \\ -4 \\ 2\end{bmatrix}}_{x}=\underbrace{(\,2\,)}_{{x}_{1}}\cdot \underbrace{\begin{bmatrix}0 \\ 0 \\ 1\end{bmatrix}}_{{b}_{1}}+\underbrace{(\,-4\,)}_{{x}_{2}}\cdot \underbrace{\begin{bmatrix}0 \\ 1 \\ 0\end{bmatrix}}_{{b}_{2}}
$$

which means that

$$
x=2\cdot {b}_{1}+(-4)\cdot {b}_{2}
$$

and therefore

$$
[x]_{B}=\begin{bmatrix}2 \\ -4\end{bmatrix}.
$$

Finally, we have that ${x}_{2}=-4.$

Answer selection: -4

Question 17592186120526 — question.difficulty/moderate

Find the coordinates of the vector $\mathbf{x}$ relative to the basis $\mathcal{B}=\{{\mathbf{b}}_{1},{\mathbf{b}}_{2},{\mathbf{b}}_{3}\}$, where
$$
{\mathbf{b}}_{\mathbf{1}}=\begin{bmatrix}0 \\ 0 \\ 1\end{bmatrix},\hspace{1em}{\mathbf{b}}_{\mathbf{2}}=\begin{bmatrix}0 \\ 1 \\ 0\end{bmatrix},\hspace{1em}{\mathbf{b}}_{\mathbf{3}}=\begin{bmatrix}1 \\ 0 \\ 0\end{bmatrix},\hspace{1em}\mathbf{x}=\begin{bmatrix}-3 \\ 0 \\ 1\end{bmatrix}.
$$
If $[\mathbf{x}]_{\mathcal{B}}=\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3}\end{bmatrix}$ then what is the value of $x_{1}$?

Solution: The order of the basis vectors matters. Here

$$
x=1b_1+0b_2-3b_3.
$$

Therefore, $[x]_B=\begin{bmatrix}1\\0\\-3\end{bmatrix}$, so $x_1=1$.

Answer selection: 1

Question 17592186247248 — question.difficulty/easy

Find the coordinates of the vector $\mathbf{x}$ relative to the basis $\mathcal{B}=\{{\mathbf{b}}_{1},{\mathbf{b}}_{2}\},$ where

$$
{\mathbf{b}}_{\mathbf{1}}=\begin{bmatrix}0 \\ 0 \\ 1\end{bmatrix},\hspace{2em}{\mathbf{b}}_{\mathbf{2}}=\begin{bmatrix}0 \\ 1 \\ 0\end{bmatrix},\hspace{2em}\mathbf{x}=\begin{bmatrix}0 \\ 8 \\ 3\end{bmatrix}.
$$

If $[\mathbf{x}]_{\mathcal{B}}=\begin{bmatrix}{x}_{1} \\ {x}_{2}\end{bmatrix}$ then what is the value of ${x}_{1}?$

Solution: Remember, the order of the vectors in a basis is important.

Notice that 

$$
\underbrace{\begin{bmatrix}0 \\ 8 \\ 3\end{bmatrix}}_{\mathbf{x}}=\underbrace{(\hspace{0.222em}3\hspace{0.222em})}_{{x}_{1}}\cdot \underbrace{\begin{bmatrix}0 \\ 0 \\ 1\end{bmatrix}}_{{\mathbf{b}}_{1}}+\underbrace{(\hspace{0.167em}8\hspace{0.167em})}_{{x}_{2}}\cdot \underbrace{\begin{bmatrix}0 \\ 1 \\ 0\end{bmatrix}}_{{\mathbf{b}}_{2}}
$$

which means that

$$
\mathbf{x}=3\cdot {\mathbf{b}}_{1}+8\cdot {\mathbf{b}}_{2}
$$

and therefore

$$
[\mathbf{x}]_{\mathcal{B}}=\begin{bmatrix}3 \\ 8\end{bmatrix}.
$$

Finally, we have that ${x}_{1}=3.$

Answer selection: 3

### Finding the Coordinates of a Vector Relative To a Given Basis Containing Two Vectors (15 captured questions)

Question 17592186120352 — question.difficulty/easy

Find the coordinates of the vector $\mathbf{x}$ relative to the basis $\mathcal{B}=\{{\mathbf{b}}_{1},{\mathbf{b}}_{2}\},$ where

$$
{\mathbf{b}}_{1}=\begin{bmatrix}1 \\ -2\end{bmatrix},\hspace{2em}{\mathbf{b}}_{2}=\begin{bmatrix}2 \\ 1\end{bmatrix},\hspace{2em}\mathbf{x}=\begin{bmatrix}2 \\ 6\end{bmatrix}.
$$

If $[\mathbf{x}]_{\mathcal{B}}=\begin{bmatrix}{x}_{1} \\ {x}_{2}\end{bmatrix}$ then what is the value of ${x}_{1}+{x}_{2}?$

Solution: We need to find ${x}_{1}$ and ${x}_{2}$ such that 

$$
\begin{aligned}{x}_{1}{\mathbf{b}}_{1}+{x}_{2}{\mathbf{b}}_{2} & =\mathbf{x} \\ {x}_{1}\begin{bmatrix}1 \\ -2\end{bmatrix}+{x}_{2}\begin{bmatrix}2 \\ 1\end{bmatrix} & =\begin{bmatrix}2 \\ 6\end{bmatrix}.\end{aligned}
$$

The equation above gives the system with the augmented matrix

$$
M=\left[\begin{array}{cc|c}1 & 2 & 2 \\ -2 & 1 & 6\end{array}\right].
$$

Row-reducing the matrix using Gaussian elimination, we obtain the following:

$$
\begin{aligned}M & =\left[\begin{array}{cc|c}1 & 2 & 2 \\ -2 & 1 & 6\end{array}\right] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 2 & 2 \\ 0 & 5 & 10\end{array}\right]\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}{x}_{1}+2{x}_{2} &=2 \\ 5{x}_{2} &=10.\end{aligned}\right.
$$

From the second equation, we get ${x}_{2}=2.$ Substituting this into the first equation, we obtain

$$
{x}_{1}+2(2)=2\,⟹\,{x}_{1}=-2.
$$

Therefore, $[\mathbf{x}]_{\mathcal{B}}=\begin{bmatrix}-2 \\ 2\end{bmatrix}.$

Finally, ${x}_{1}+{x}_{2}=(-2)+2=0.$

Answer selection: 0

Question 17592186120380 — question.difficulty/moderate

Find the coordinates of the vector $\mathbf{x}$ relative to the basis $\mathcal{B}=\{{\mathbf{b}}_{1},{\mathbf{b}}_{2}\}$, where
$$
{\mathbf{b}}_{1}=\begin{bmatrix}1 \\ 4 \\ -2\end{bmatrix},\hspace{2em}{\mathbf{b}}_{2}=\begin{bmatrix}-3 \\ -10 \\ 6\end{bmatrix},\hspace{2em}\mathbf{x}=\begin{bmatrix}10 \\ 8 \\ -20\end{bmatrix}.
$$
If $[\mathbf{x}]_{\mathcal{B}}=\begin{bmatrix}{x}_{1} \\ {x}_{2}\end{bmatrix}$ then what is the value of $x_{1} + x_{2}$?

Solution: Find $x_1,x_2$ such that $x_1b_1+x_2b_2=x$. This gives

$$
\left\{\begin{aligned}x_1-3x_2&=10\\4x_1-10x_2&=8\\-2x_1+6x_2&=-20.\end{aligned}\right.
$$

Subtracting four times the first equation from the second gives $2x_2=-32$, so $x_2=-16$. Then $x_1=10+3(-16)=-38$. These values also satisfy the third equation.

Therefore, $[x]_B=\begin{bmatrix}-38\\-16\end{bmatrix}$ and $x_1+x_2=-54$.

Answer selection: -54

Question 17592186247252 — question.difficulty/easy

Find the coordinates of the vector $\mathbf{x}$ relative to the basis $\mathcal{B}=\{{\mathbf{b}}_{1},{\mathbf{b}}_{2}\},$ where

$$
{\mathbf{b}}_{1}=\begin{bmatrix}1 \\ -5\end{bmatrix},\hspace{2em}{\mathbf{b}}_{2}=\begin{bmatrix}-3 \\ 2\end{bmatrix},\hspace{2em}\mathbf{x}=\begin{bmatrix}-3 \\ 41\end{bmatrix}.
$$

If $[\mathbf{x}]_{\mathcal{B}}=\begin{bmatrix}{x}_{1} \\ {x}_{2}\end{bmatrix}$ then what is the value of ${x}_{1}+{x}_{2}?$

Solution: We need to find ${x}_{1}$ and ${x}_{2}$ such that 

$$
\begin{aligned}{x}_{1}{\mathbf{b}}_{1}+{x}_{2}{\mathbf{b}}_{2} & =\mathbf{x} \\ {x}_{1}\begin{bmatrix}1 \\ -5\end{bmatrix}+{x}_{2}\begin{bmatrix}-3 \\ 2\end{bmatrix} & =\begin{bmatrix}-3 \\ 41\end{bmatrix}.\end{aligned}
$$

The equation above gives the system with the augmented matrix

$$
M=\left[\begin{array}{cc|c}1 & -3 & -3 \\ -5 & 2 & 41\end{array}\right].
$$

Row-reducing the matrix using Gaussian elimination, we obtain the following:

$$
\begin{aligned}M & =\left[\begin{array}{cc|c}1 & -3 & -3 \\ -5 & 2 & 41\end{array}\right] & {R}_{2} & :={R}_{2}+5{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -3 & -3 \\ 0 & -13 & 26\end{array}\right]\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}{x}_{1}-3{x}_{2} &=-3 \\ -13{x}_{2} &=26.\end{aligned}\right.
$$

From the second equation, we get ${x}_{2}=-2.$ Substituting this into the first equation, we obtain

$$
{x}_{1}-3(-2)=-3\,⟹\,{x}_{1}=-9.
$$

Therefore, $[\mathbf{x}]_{\mathcal{B}}=\begin{bmatrix}-9 \\ -2\end{bmatrix}.$

Finally, ${x}_{1}+{x}_{2}=(-9)+(-2)=-11.$

Answer selection: -11

### Finding the Coordinates of a Vector Relative To a Given Basis Containing More Than Two Vectors (14 captured questions)

Question 17592186120357 — question.difficulty/hard

Find the coordinates of the vector $\mathbf{x}$ relative to the basis $\mathcal{B}=\{{\mathbf{b}}_{1},{\mathbf{b}}_{2},{\mathbf{b}}_{3}\}$, where
$$
{\mathbf{b}}_{1}=\begin{bmatrix}1 \\ -2 \\ 4\end{bmatrix},\hspace{1em}{\mathbf{b}}_{2}=\begin{bmatrix}2 \\ 1 \\ -2\end{bmatrix},\hspace{1em}{\mathbf{b}}_{3}=\begin{bmatrix}0 \\ 0 \\ 3\end{bmatrix},\hspace{1em}\mathbf{x}=\begin{bmatrix}5 \\ 10 \\ -17\end{bmatrix}.
$$
If $[\mathbf{x}]_{\mathcal{B}}=\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3}\end{bmatrix}$ then what is the value of $x_{1} + x_{2} + x_{3}$?

Solution: Find $x_1,x_2,x_3$ such that $x_1b_1+x_2b_2+x_3b_3=x$. The corresponding system is

$$
\left\{\begin{aligned}x_1+2x_2&=5\\-2x_1+x_2&=10\\4x_1-2x_2+3x_3&=-17.\end{aligned}\right.
$$

Adding twice the first equation to the second gives $5x_2=20$, so $x_2=4$. Then $x_1=5-8=-3$. The third equation becomes $-12-8+3x_3=-17$, giving $x_3=1$.

Thus $[x]_B=\begin{bmatrix}-3\\4\\1\end{bmatrix}$, and $x_1+x_2+x_3=-3+4+1=2$.

Answer selection: 2

Question 17592186120358 — question.difficulty/hard

Find the coordinates of the vector $\mathbf{x}$ relative to the basis $\mathcal{B}=\{{\mathbf{b}}_{1},{\mathbf{b}}_{2},{\mathbf{b}}_{3}\},$ where

$$
{\mathbf{b}}_{1}=\begin{bmatrix}1 \\ -1 \\ 2 \\ 0\end{bmatrix},\hspace{1em}{\mathbf{b}}_{2}=\begin{bmatrix}2 \\ 0 \\ 0 \\ 4\end{bmatrix},\hspace{1em}{\mathbf{b}}_{3}=\begin{bmatrix}0 \\ 0 \\ -1 \\ 0\end{bmatrix},\hspace{1em}\mathbf{x}=\begin{bmatrix}2 \\ 2 \\ -5 \\ 4\end{bmatrix}.
$$

If $[\mathbf{x}]_{\mathcal{B}}=\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3}\end{bmatrix}$ then what is the value of ${x}_{1}+{x}_{2}+{x}_{3}?$

Solution: We need to find ${x}_{1}$,  ${x}_{2}$, and ${x}_{3}$ such that 

$$
\begin{aligned}{x}_{1}{\mathbf{b}}_{1}+{x}_{2}{\mathbf{b}}_{2}+{x}_{3}{\mathbf{b}}_{3} & =\mathbf{x} \\ {x}_{1}\begin{bmatrix}1 \\ -1 \\ 2 \\ 0\end{bmatrix}+{x}_{2}\begin{bmatrix}2 \\ 0 \\ 0 \\ 4\end{bmatrix}+{x}_{3}\begin{bmatrix}0 \\ 0 \\ -1 \\ 0\end{bmatrix} & =\begin{bmatrix}2 \\ 2 \\ -5 \\ 4\end{bmatrix}\end{aligned}
$$

From this, we get the system with the augmented matrix $M$, which we reduce using Gaussian elimination:

$$
\begin{aligned}M= & \left[\begin{array}{ccc|c}1 & 2 & 0 & 2 \\ -1 & 0 & 0 & 2 \\ 2 & 0 & -1 & -5 \\ 0 & 4 & 0 & 4\end{array}\right] & {R}_{2} & :={R}_{2}+{R}_{1} \\ ∼ & \left[\begin{array}{ccc|c}1 & 2 & 0 & 2 \\ 0 & 2 & 0 & 4 \\ 2 & 0 & -1 & -5 \\ 0 & 4 & 0 & 4\end{array}\right] & {R}_{3} & :={R}_{3}+(-2){R}_{1} \\ ∼ & \left[\begin{array}{ccc|c}1 & 2 & 0 & 2 \\ 0 & 2 & 0 & 4 \\ 0 & -4 & -1 & -9 \\ 0 & 4 & 0 & 4\end{array}\right] & {R}_{3} & :={R}_{3}+2{R}_{2} \\ ∼ & \left[\begin{array}{ccc|c}1 & 2 & 0 & 2 \\ 0 & 2 & 0 & 4 \\ 0 & 0 & -1 & -1 \\ 0 & 4 & 0 & 4\end{array}\right] & {R}_{4} & :={R}_{4}+(-2){R}_{2} \\ ∼ & \left[\begin{array}{ccc|c}1 & 2 & 0 & 2 \\ 0 & 2 & 0 & 4 \\ 0 & 0 & -1 & -1 \\ 0 & 0 & 0 & -4\end{array}\right]\end{aligned}
$$

 
The system is now 

$$
\left\{\begin{aligned}{x}_{1}+2{x}_{2} &=2 \\ 2{x}_{2} &=4 \\ -{x}_{3} &=-1 \\ 0 &=4,\end{aligned}\right.
$$

where the fourth equation is always false. Therefore, the system has no solution and we conclude that 

$$
\mathbf{x}\notin \text{Span}\{{\mathbf{b}}_{1},{\mathbf{b}}_{2},{\mathbf{b}}_{3}\}.
$$

Answer selection: \mathbf{x}\notin \text{Span}\{{\mathbf{b}}_{1},{\mathbf{b}}_{2},{\mathbf{b}}_{3}\}

Question 17592186247255 — question.difficulty/hard

Find the coordinates of the vector $\mathbf{x}$ relative to the basis $\mathcal{B}=\{{\mathbf{b}}_{1},{\mathbf{b}}_{2},{\mathbf{b}}_{3}\},$ where

$$
{\mathbf{b}}_{1}=\begin{bmatrix}1 \\ 1 \\ 1\end{bmatrix},\hspace{1em}{\mathbf{b}}_{2}=\begin{bmatrix}2 \\ 2 \\ 1\end{bmatrix},\hspace{1em}{\mathbf{b}}_{3}=\begin{bmatrix}2 \\ 1 \\ 0\end{bmatrix},\hspace{1em}\mathbf{x}=\begin{bmatrix}2 \\ 3 \\ -1\end{bmatrix}.
$$

If $[\mathbf{x}]_{\mathcal{B}}=\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3}\end{bmatrix}$ then what is the value of ${x}_{1}+{x}_{2}+{x}_{3}?$

Solution: We need to find ${x}_{1}$,  ${x}_{2}$, and ${x}_{3}$ such that 

$$
\begin{aligned}{x}_{1}{\mathbf{b}}_{1}+{x}_{2}{\mathbf{b}}_{2}+{x}_{3}{\mathbf{b}}_{3} & =\mathbf{x} \\ {x}_{1}\begin{bmatrix}1 \\ 1 \\ 1\end{bmatrix}+{x}_{2}\begin{bmatrix}2 \\ 2 \\ 1\end{bmatrix}+{x}_{3}\begin{bmatrix}2 \\ 1 \\ 0\end{bmatrix} & =\begin{bmatrix}2 \\ 3 \\ -1\end{bmatrix}.\end{aligned}
$$

From this, we get the system with the augmented matrix $M$, which we reduce using Gaussian elimination:

$$
\begin{aligned}M= & \left[\begin{array}{ccc|c}1 & 2 & 2 & 2 \\ 1 & 2 & 1 & 3 \\ 1 & 1 & 0 & -1\end{array}\right] & {R}_{2} & :={R}_{2}+(-1){R}_{1} \\ ∼ & \left[\begin{array}{ccc|c}1 & 2 & 2 & 2 \\ 0 & 0 & -1 & 1 \\ 1 & 1 & 0 & -1\end{array}\right] & {R}_{3} & :={R}_{3}+(-1){R}_{1} \\ ∼ & \left[\begin{array}{ccc|c}1 & 2 & 2 & 2 \\ 0 & 0 & -1 & 1 \\ 0 & -1 & -2 & -3\end{array}\right] & {R}_{2} & ↔{R}_{3} \\ ∼ & \left[\begin{array}{ccc|c}1 & 2 & 2 & 2 \\ 0 & -1 & -2 & -3 \\ 0 & 0 & -1 & 1\end{array}\right]\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}{x}_{1}+2{x}_{2}+2{x}_{3} &=2 \\ -{x}_{2}-2{x}_{3} &=-3 \\ -{x}_{3} &=1.\end{aligned}\right.
$$

From third equation we get ${x}_{3}=-1$ and substituting this value into the second equation yields ${x}_{2}=-2(-1)+3=5.$ Finally, substituting ${x}_{2}=5$ and ${x}_{3}=-1$ into the first equation, we obtain

$$
{x}_{1}+2(5)+2(-1)=2\,⟹\,{x}_{1}=-6.
$$

Therefore, $[\mathbf{x}]_{\mathcal{B}}=\begin{bmatrix}-6 \\ 5 \\ -1\end{bmatrix}.$

Finally, 

$$
{x}_{1}+{x}_{2}+{x}_{3}=(-6)+5+(-1)=-2.
$$

Answer selection: -2
