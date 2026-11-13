# 17592186048819 The Eigenvalues and Eigenvectors of a 2x2 Matrix

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186107090 — Introduction

Given a matrix $A,$ an **eigenvector** of $A$ is a *non-zero* vector $\mathbf{v}$ such that 

$$
A \mathbf{v} = \lambda \mathbf{v}
$$

for some scalar $\lambda \in \mathbb{R}.$ The scalar $\lambda$ is called the **eigenvalue** corresponding to the eigenvector $\mathbf{v}.$

For example, consider the matrix 
$$
A = 
	{\left[ \begin{array}{cc}2 & 2 \\ 2 & - 1\end{array} \right]}
$$ 
and the vector $\color{blue}\mathbf{v} = {\left[ \begin{array}{c}1 \\ - 2\end{array} \right]}.$ Computing the product $A \cdot \mathbf{v},$ we get

$$
\begin{aligned}Av & =\begin{bmatrix}2 & 2 \\ 2 & -1\end{bmatrix}\cdot \begin{bmatrix}1 \\ -2\end{bmatrix} \\  & =\begin{bmatrix}-2 \\ 4\end{bmatrix} \\  & =(-2)\cdot \begin{bmatrix}1 \\ -2\end{bmatrix} \\  & =-2v.\end{aligned}
$$

We've discovered that $A {\color{blue}\mathbf{v}} = {\color{red}-2} {\color{blue}\mathbf{v}}.$ Therefore,

- the vector $\color{blue}\mathbf{v} = {\left[ \begin{array}{c}1 \\ - 2\end{array} \right]}$ is an *eigenvector* of $A,$ and

- the scalar $\color{red}\lambda=-2$ is the *eigenvalue* corresponding to the eigenvector ${\color{blue}\mathbf{v}}.$

**Caution:** Remember that an eigenvector must be a *non-zero* vector. This is very important.



### example 17592186105620 — Finding the Eigenvalue that Corresponds to a Given Eigenvector

Determine if $\mathbf{v}=\left[{\begin{array}{c}1 \\ 1\end{array}}\right]$ is an eigenvector of the matrix $A = \left[{\begin{array}{cc}1 & 3 \\ 3 & 1\end{array}} \right].$ If so, then what is the corresponding eigenvalue?

The eigenvectors of $A$ are the non-zero vectors $\mathbf{v}$ such that $A\mathbf{v}=\lambda \mathbf{v}.$ We have

$$
\begin{aligned}Av & =\begin{bmatrix}1 & 3 \\ 3 & 1\end{bmatrix}\begin{bmatrix}1 \\ 1\end{bmatrix} \\  & =\begin{bmatrix}4 \\ 4\end{bmatrix} \\  & =4\cdot \begin{bmatrix}1 \\ 1\end{bmatrix} \\  & =4v.\end{aligned}
$$

Since $A\mathbf{v}=4 \mathbf{v},$ we conclude that $\mathbf{v}$ is an eigenvector of $A$ and the corresponding eigenvalue is $\lambda=4.$

### tutorial 17592186107098 — The Geometric Interpretation of Eigenvalues and Eigenvectors

Eigenvectors and eigenvalues can be interpreted geometrically.

First, recall that if the matrix $A$ is the standard matrix of some linear transformation $T,$ then the product $A\mathbf x$ gives the image of $\mathbf x$ under the action of $T.$ The image of $\mathbf x$ under the action of $T$ can appear quite different from the original vector $\mathbf x.$

However, for an eigenvector $\mathbf v$ with corresponding eigenvalue $\lambda,$ we get

$$
A\mathbf{v}=\lambda \mathbf{v}.
$$

In other words, when the matrix $A$ is applied to an eigenvector $\mathbf v,$ the image of $\mathbf v$ is a scaled version of the original vector $\mathbf v$, and the scale factor is $\lambda.$

To demonstrate, consider once again the following matrix:

$$
A = 
	{\left[ \begin{array}{cc}2 & 2 \\ 2 & - 1\end{array} \right]}
$$

We've already seen that $A$ has an eigenvector $\color{black}\mathbf{v} = {\left[ \begin{array}{c}1 \\ - 2\end{array} \right]}$ with corresponding eigenvalue $\lambda=-2.$ So we have

$$
A\mathbf{v} = -2\mathbf{v} = {\left[ \begin{array}{c}- 2 \\ 4\end{array} \right]}.
$$

Plotting the vector $\mathbf v$ and its image $-2\mathbf v$ in the plane, we get the following picture.

![](images/9a/9aca41e0597b0b1698e8ec24da9966fd9b7e5fee3951081d8abdb0cc0caaac7b.png)

In general, when we apply a matrix $A$ to an eigenvector $\mathbf v,$ the resulting vector $A\mathbf{v}=\lambda\mathbf{v}$ always lies on the same line as $\mathbf v.$

If $|\lambda| > 1,$ then the matrix stretches the vector. For $|\lambda| < 1,$ the matrix compresses the vector. In addition, a negative eigenvalue $\lambda<0$ means that $\mathbf v$ is flipped in the opposite direction as well as scaled.



### example 17592186105628 — Plotting the Product of a Matrix and an Eigenvector Given its Corresponding Eigenvalue

![](images/fd/fdfa0528b5476ed0246679c45fd31824470063a68f33c4c9af0f714ad201538f.png)

The vector $\mathbf{v}$ is an eigenvector of a $2 \times 2$ matrix $A$ corresponding to the eigenvalue $2.$ Find the vector $A\mathbf{v}.$

The eigenvector $\mathbf{v}={\left[ \begin{array}{c}1 \\ 2\end{array} \right]}$ corresponds to the eigenvalue $\lambda=2.$ So, 

$$
\begin{aligned}Av=2v.\end{aligned}
$$

Therefore, we have the following picture:

![](images/78/78e1e3c015adad2c826a64e255bd982941dc9fe50679acc2bae3f00b31bd9f39.png)

### example 17592186105622 — Determining the Value of an Unknown Given an Eigenvalue and Eigenvector of a Matrix

An eigenvector of $A =
\left[{\begin{array}{cc}2 & 1 \\ 1 & 2\end{array}}\right]$ corresponding to an eigenvalue $\lambda=6c$ is  $\left[{\begin{array}{c}1 \\ 2 c\end{array}}\right].$ Determine the value of $c.$

Remember that the eigenvectors of $A$ are the non-zero vectors $\mathbf{v}$ such that $A\mathbf{v}=\lambda \mathbf{v}.$ So, we have

$$
\begin{aligned}Av & =\lambda v \\ \begin{bmatrix}2 & 1 \\ 1 & 2\end{bmatrix}\begin{bmatrix}1 \\ 2c\end{bmatrix} & =6c\begin{bmatrix}1 \\ 2c\end{bmatrix} \\ \begin{bmatrix}2+2c \\ 1+4c\end{bmatrix} & =\begin{bmatrix}6c \\ 12{c}^{2}\end{bmatrix}.\end{aligned}
$$

This gives us the following system of linear equations:

$$
\left\{\begin{aligned}2+2c &=6c \\ 1+4c &=12{c}^{2}\end{aligned}\right.
$$

Solving for $c$ in the first equation, we get

$$
2+2c=6c \qquad \Longrightarrow \qquad c = \dfrac{1}{2}.
$$

Now, substituting $c=\dfrac{1}{2}$ into the second equation, we get

$$
\begin{aligned}1+4c & =12{c}^{2} \\ 1+4\cdot \frac{1}{2} & =12{\left(\frac{1}{2}\right)}^{2} \\ 3 & =3,\end{aligned}
$$

which is a true statement.

Therefore, the solutions of the system is $c=\dfrac{1}{2}$.

### example 17592186105621 — Identifying True Statements About Eigenvalues and Eigenvectors

Which of the following statements are true?

- $\mathbf{v}={\left[ \begin{array}{c}1 \\ 4\end{array} \right]}$ is an eigenvector of $A={\left[ \begin{array}{cc}2 & 0 \\ 4 & 1\end{array} \right]}$ that corresponds to the eigenvalue $2.$

- $\mathbf{v}={\left[ \begin{array}{c}0 \\ 0\end{array} \right]}$ is an eigenvector of $A={\left[ \begin{array}{cc}1 & 1 \\ 1 & 1\end{array} \right]}$ that corresponds to the eigenvalue $0.$

- If $\mathbf{v}$ is an eigenvector of a matrix $A$ corresponding to the eigenvalue $\lambda = 5,$ then $2\mathbf{v}$ is also an eigenvector of $A$ corresponding to $\lambda = 5.$

Remember that the eigenvectors of $A$ are the non-zero vectors $\mathbf{v}$ such that $A\mathbf{v}=\lambda \mathbf{v}.$ With that in mind, let's examine the statements one by one.

- Statement I is true. We have

$$
\begin{aligned}Av & =\begin{bmatrix}2 & 0 \\ 4 & 1\end{bmatrix}\begin{bmatrix}1 \\ 4\end{bmatrix} \\  & =\begin{bmatrix}2 \\ 8\end{bmatrix} \\  & =2\cdot \begin{bmatrix}1 \\ 4\end{bmatrix} \\  & =2v.\end{aligned}
$$

Since $A\mathbf{v}=2 \mathbf{v},$ we conclude that $\mathbf{v}$ is an eigenvector of $A$ and the corresponding eigenvalue is $\lambda=2.$

- Statement II is false. An eigenvector must be a *non-zero* vector.

- Statement III is true. We have

$$
\begin{aligned}A(2v)=2Av=2(5v)=5(2v).\end{aligned}
$$

Since, $A(2\mathbf{v})=5( 2 \mathbf{v} ),$ and $2 \mathbf{v} \neq \mathbf{0},$ this implies that $2 \mathbf{v}$ is an eigenvector of $A$ and the corresponding eigenvalue is $\lambda = 5.$

Therefore, the correct answer is, "I and III only."

**Note:** Statement III is true in the general case, too. In general, any non-zero multiple of an eigenvector is again an eigenvector, and the corresponding eigenvalue is the same.

## Representative practice (first three per skill; full bank in practice.json)

### Finding the Eigenvalue that Corresponds to a Given Eigenvector (10 captured questions)

Question 17592186106092 — question.difficulty/easy

Determine if $v = \begin{bmatrix}-4 \\ 1\end{bmatrix}$ is an eigenvector of the matrix
$$
\displaystyle A = \begin{bmatrix}-1 & 8 \\ -1 & -7\end{bmatrix}.
$$
If so, then what is the corresponding eigenvalue?

Solution: 

Question 17592186106296 — question.difficulty/easy

Determine if $v=\begin{bmatrix}-1 \\ 1\end{bmatrix}$  is an eigenvector of the matrix 
$$
\displaystyle A=\begin{bmatrix}-1 & -6 \\ -3 & 2\end{bmatrix}.
$$
If so, then what is the corresponding eigenvalue?

Solution: The eigenvectors of $A$ are the non-zero vectors $v$ such that $Av=\lambda v.$ We have

$$
\begin{aligned}Av & =\begin{bmatrix}-1 & -6 \\ -3 & 2\end{bmatrix}\begin{bmatrix}-1 \\ 1\end{bmatrix} \\  & =\begin{bmatrix}-5 \\ 5\end{bmatrix} \\  & =5\cdot \begin{bmatrix}-1 \\ 1\end{bmatrix} \\  & =5v.\end{aligned}
$$

Since $Av=5v,$ we conclude that $v$ is an eigenvector of $A$ and the corresponding eigenvalue is $\lambda =5.$

Answer selection: 5

Question 17592186243944 — question.difficulty/moderate

Determine if $v=\begin{bmatrix}1 \\ -1\end{bmatrix}$ is an eigenvector of the matrix 
$$
\displaystyle A=\begin{bmatrix}-1 & -2 \\ 2 & 4\end{bmatrix}.
$$
If so, then what is the corresponding eigenvalue?

Solution: The eigenvectors of $A$ are the non-zero vectors $v$ such that $Av=\lambda v.$ We have

$$
\begin{aligned}Av & =\begin{bmatrix}-1 & -2 \\ 2 & 4\end{bmatrix}\begin{bmatrix}1 \\ -1\end{bmatrix} \\  & =\begin{bmatrix}1 \\ -2\end{bmatrix}.\end{aligned}
$$

If $v$ is an eigenvector, then there must exist a real number $\lambda $ such that $Av=\lambda v.$ Hence, we have

$$
\begin{bmatrix}1 \\ -2\end{bmatrix}=\lambda \begin{bmatrix}1 \\ -1\end{bmatrix}.
$$

This leads to the following system of equations for $\lambda :$

$$
\left\{\begin{aligned}1 &=\lambda \\ -2 &=-\lambda\end{aligned}\right.
$$

This system has no solution. Therefore, $v$ is not an eigenvector of $A.$

Answer selection: $v$ is not an eigenvector of $A$

### Plotting the Product of a Matrix and an Eigenvector Given its Corresponding Eigenvalue (13 captured questions)

Question 17592186106295 — None

![](images/61/619622638af3f29441b51526e3885bdc51b3ad04819c5f7ac06a5ca7833fcb48.png)

The vector $v$ is an eigenvector of a $2 \cdot 2$ matrix $A$ corresponding to the eigenvalue $-2$. Find the vector $Av$.

Solution: 

Question 17592186106299 — question.difficulty/easy

![](images/19/190af2ef92a8c23efb6fc15c6effebf5db929d8d133da6809bd27f77a6e9292b.png)

The vector $v$ is an eigenvector of a $2\times 2$ matrix $A$ corresponding to the eigenvalue $-1.$ Find the vector $Av.$

Solution: The eigenvector $v=\begin{bmatrix}0 \\ 2\end{bmatrix}$ corresponds to the eigenvalue $\lambda =-1.$ So, 

$$
\begin{aligned}Av & =-1v.\end{aligned}
$$

Therefore, we have the following picture:

![](images/1f/1f778e38d2dd4d2e33675bfa45bbe13c9596b1818092ef6129e8f35b1741157e.png)

Answer selection: images/1f/1f778e38d2dd4d2e33675bfa45bbe13c9596b1818092ef6129e8f35b1741157e.png

Question 17592186243973 — question.difficulty/easy

![](images/4a/4adc01d460f42f134f2e6c8da1e2fe516c8e6cfb64bcfeb7a5db89cf93f1fc11.png)

The vector $v$ is an eigenvector of a $2\times 2$ matrix $C$ corresponding to the eigenvalue $-4.$ Find the vector $Cv.$

Solution: The eigenvector $v=\begin{bmatrix}-1 \\ 1\end{bmatrix}$ corresponds to the eigenvalue $\lambda =-4.$ So, 

$$
\begin{aligned}Cv & =-4v.\end{aligned}
$$

Therefore, we have the following picture:

![](images/99/99e3776bfa4048703042970a2479a86c749e3e2a547dce966fceb23b671d66f2.png)

Answer selection: images/99/99e3776bfa4048703042970a2479a86c749e3e2a547dce966fceb23b671d66f2.png

### Determining the Value of an Unknown Given an Eigenvalue and Eigenvector of a Matrix (15 captured questions)

Question 17592186106091 — None

An eigenvector of $A = \begin{bmatrix}-2 & -1 \\ 4 & 3\end{bmatrix}$ corresponding to an eigenvalue $λ = 2$ is $\begin{bmatrix}4 \\ -2c\end{bmatrix}$. Determine the value of $c$.

Solution: 

Question 17592186106093 — None

An eigenvector of
$$
\displaystyle A = \begin{bmatrix}1 & 5 \\ 4 & 0\end{bmatrix}
$$
corresponding to an eigenvalue $λ = 2k + 1$ is $\begin{bmatrix}5 \\ 3k - 2\end{bmatrix}$. Determine the value of $k$.

Solution: 

Question 17592186243959 — question.difficulty/hard

The eigenvector of $A=\begin{bmatrix}-4 & 0 \\ -k & -1\end{bmatrix}$ corresponding to the eigenvalue $\lambda =k-1$ is  $\begin{bmatrix}4 \\ -4\end{bmatrix}.$ Determine the value of $k.$

Solution: Remember that the eigenvectors of $A$ are the non-zero vectors $v$ such that $Av=\lambda v.$ So, we have

$$
\begin{aligned}Av & =\lambda v \\ \begin{bmatrix}-4 & 0 \\ -k & -1\end{bmatrix}\begin{bmatrix}4 \\ -4\end{bmatrix} & =(k-1)\begin{bmatrix}4 \\ -4\end{bmatrix} \\ \begin{bmatrix}-16 \\ -4k+4\end{bmatrix} & =\begin{bmatrix}4k-4 \\ -4k+4\end{bmatrix}.\end{aligned}
$$

This gives us the following system of linear equations:

$$
\left\{\begin{aligned}-16 &=4k-4, \\ -4k+4 &=-4k+4\end{aligned}\right.
$$

Solving for $k$ in the first equation, we get

$$
-12=4k\,⟹\,k=-3.
$$

The second equation is true for any value of $k.$

Therefore, the solution of the system is $k=-3.$

Answer selection: -3

### Identifying True Statements About Eigenvalues and Eigenvectors (13 captured questions)

Question 17592186106297 — question.difficulty/moderate

Which of the following statements are true?

Select all that apply.

Solution: Remember that the eigenvectors of $A$ are the non-zero vectors $v$ such that $Av=\lambda v.$ With that in mind, let's examine the statements one by one.

- Statement “$v=\begin{bmatrix}0 \\ -1\end{bmatrix}$ is an eigenvector of $A=\begin{bmatrix}2 & 0 \\ 2 & 1\end{bmatrix}$ that corresponds to the eigenvalue $\lambda =2.$” is false. We have

$$
\begin{aligned}Av & =\begin{bmatrix}2 & 0 \\ 2 & 1\end{bmatrix}\begin{bmatrix}0 \\ -1\end{bmatrix} \\  & =\begin{bmatrix}0 \\ -1\end{bmatrix} \\  & =1\cdot \begin{bmatrix}0 \\ -1\end{bmatrix} \\  & =1v.\end{aligned}
$$

 
Since $Av=v,$ we conclude that $v$ is an eigenvector of $A$ and the corresponding eigenvalue is $\lambda =1$ (but not $2$).

- Statement “$v=\begin{bmatrix}-1 \\ 1\end{bmatrix}$ is an eigenvector of $A=\begin{bmatrix}1 & 1 \\ 2 & 2\end{bmatrix}$ that corresponds to the eigenvalue $\lambda =0.$” is true. We have

$$
\begin{aligned}A{v}_{1} & =\begin{bmatrix}1 & 1 \\ 2 & 2\end{bmatrix}\begin{bmatrix}-1 \\ 1\end{bmatrix} \\  & =\begin{bmatrix}0 \\ 0\end{bmatrix} \\  & =0\cdot \begin{bmatrix}-1 \\ 1\end{bmatrix} \\  & =0{v}_{1}.\end{aligned}
$$

 
Since $Av=0v,$ we conclude that $v$ is an eigenvector of $A$ and the corresponding eigenvalue is $\lambda =0.$

- Statement “If $v$ is an eigenvector of a matrix $A$ corresponding to the eigenvalue $\lambda =2,$ then $3v$ is an eigenvector of $A$ corresponding to $\lambda =6.$” is false. We have

$$
\begin{aligned}A(3v)=3Av=3(2v)=2(3v).\end{aligned}
$$

Since, $A(3v)=2(3v),$ and $3v\ne 0,$ this implies that $3v$ is an eigenvector of $A$ and the corresponding eigenvalue is $\lambda =2$ (but not $6$).

**Note:** In general, any non-zero multiple of an eigenvector is again an eigenvector, and the corresponding eigenvalue is the same.

Therefore, the correct answer is “$v=\begin{bmatrix}-1 \\ 1\end{bmatrix}$ is an eigenvector of $A=\begin{bmatrix}1 & 1 \\ 2 & 2\end{bmatrix}$ that corresponds to the eigenvalue $\lambda =0.$” only.

Answer $v=\begin{bmatrix}-1 \\ 1\end{bmatrix}$ is an eigenvector of $A=\begin{bmatrix}1 & 1 \\ 2 & 2\end{bmatrix}$ that corresponds to the eigenvalue $\lambda =0.$: true

Answer $v=\begin{bmatrix}0 \\ -1\end{bmatrix}$ is an eigenvector of $A=\begin{bmatrix}2 & 0 \\ 2 & 1\end{bmatrix}$ that corresponds to the eigenvalue $\lambda =2.$: false

Answer If $v$ is an eigenvector of a matrix $A$ corresponding to the eigenvalue $\lambda =2,$ then $3v$ is an eigenvector of $A$ corresponding to $\lambda =6.$: false

Answer None of the above: false

Question 17592186106298 — question.difficulty/moderate

Which of the following statements are true?

Select all that apply.

Solution: Remember that the eigenvectors of $A$ are the non-zero vectors $v$ such that $Av=\lambda v.$ With that in mind, let's examine the statements one by one.

- Statement “$v=\begin{bmatrix}-1 \\ 1\end{bmatrix}$ is an eigenvector of $A=\begin{bmatrix}0 & -1 \\ 1 & 2\end{bmatrix}$ that corresponds to the eigenvalue $\lambda =1.$” is true. We have

$$
\begin{aligned}Av & =\begin{bmatrix}0 & -1 \\ 1 & 2\end{bmatrix}\begin{bmatrix}-1 \\ 1\end{bmatrix} \\  & =\begin{bmatrix}-1 \\ 1\end{bmatrix} \\  & =1\cdot \begin{bmatrix}-1 \\ 1\end{bmatrix} \\  & =1v.\end{aligned}
$$

- Statement “If $v$ is an eigenvector of a matrix $A$ corresponding to the eigenvalue $\lambda =-7$ then $3v$ is also an eigenvector corresponding to $\lambda =-7.$” is true. We have

$$
\begin{aligned}A(3v)=3Av=3(-7v)=-7(3v).\end{aligned}
$$

Since, $A(3v)=-7(3v),$ and $3v\ne 0,$ this implies that $3v$ is an eigenvector of $A$ and the corresponding eigenvalue is $\lambda =-7.$

**Note:** In general, any non-zero multiple of an eigenvector is again an eigenvector, and the corresponding eigenvalue is the same.

- Statement “$v=\begin{bmatrix}0 \\ 0\end{bmatrix}$ is an eigenvector of $A=\begin{bmatrix}-1 & -1 \\ 1 & 1\end{bmatrix}$ that corresponds to the eigenvalue $0.$” is false. An eigenvector must be a *non-zero* vector.

Therefore, the correct answer is “$v=\begin{bmatrix}-1 \\ 1\end{bmatrix}$ is an eigenvector of $A=\begin{bmatrix}0 & -1 \\ 1 & 2\end{bmatrix}$ that corresponds to the eigenvalue $\lambda =1.$”; “If $v$ is an eigenvector of a matrix $A$ corresponding to the eigenvalue $\lambda =-7$ then $3v$ is also an eigenvector corresponding to $\lambda =-7.$” only.

Answer $v=\begin{bmatrix}-1 \\ 1\end{bmatrix}$ is an eigenvector of $A=\begin{bmatrix}0 & -1 \\ 1 & 2\end{bmatrix}$ that corresponds to the eigenvalue $\lambda =1.$: true

Answer $v=\begin{bmatrix}0 \\ 0\end{bmatrix}$ is an eigenvector of $A=\begin{bmatrix}-1 & -1 \\ 1 & 1\end{bmatrix}$ that corresponds to the eigenvalue $0.$: false

Answer If $v$ is an eigenvector of a matrix $A$ corresponding to the eigenvalue $\lambda =-7$ then $3v$ is also an eigenvector corresponding to $\lambda =-7.$: true

Answer None of the above: false

Question 17592186244030 — question.difficulty/hard

Which of the following statements are true?

Select all that apply.

Solution: Remember that the eigenvectors of $A$ are the non-zero vectors $v$ such that $Av=\lambda v.$ With that in mind, let's examine the statements one by one.

- Statement is true. By the definition of an eigenvector, we have 

$$
Av=5v.
$$

 
Multiplying it by ${A}^{-1}$ from the left, we obtain 

$$
v=5{A}^{-1}v.
$$

Dividing both sides by $5$, we get 

$$
{A}^{-1}v=\frac{1}{5}v.
$$

 
So, $v$ is an eigenvector  of ${A}^{-1}$ that corresponds to the eigenvalue $\frac{1}{5}.$

**Note:** In general, an eigenvector of an invertible matrix $A$ that corresponds to an eigenvalue $\lambda $ is an eigenvector of ${A}^{-1}$ that corresponds to the eigenvalue $\frac{1}{\lambda }.$

- Statement “An eigenvector of an invertible matrix $A$ that corresponds to the eigenvalue $\lambda =6$ is also an eigenvector of the inverse ${A}^{-1}$ that corresponds to the same eigenvalue $\lambda =6.$” is false. According to the statement above, an eigenvector of $A$ that corresponds to the eigenvalue $\lambda =6$ is an eigenvector of ${A}^{-1}$ that corresponds to $\lambda =\frac{1}{6}.$

- Statement “If $v$ is an eigenvector of a matrix $A$ corresponding to the eigenvalue $\lambda =2,$ then $7v$ is also an eigenvector of $A$ corresponding to $\lambda =2.$” is true. We have

$$
\begin{aligned}A(7v)=7Av=7(2v)=2(7v).\end{aligned}
$$

Since, $A(7v)=2(7v),$ and $7v\ne 0,$ this implies that $7v$ is an eigenvector of $A$ and the corresponding eigenvalue is $\lambda =2.$

**Note:** In general, any non-zero multiple of an eigenvector is again an eigenvector, and the corresponding eigenvalue is the same.

Therefore, the correct answer is “If $v$ is an eigenvector of an invertible matrix $A$ that corresponds to the eigenvalue $\lambda =5$ then $v$ is also an eigenvector of the matrix ${A}^{-1}$ that corresponds to $\lambda =\frac{1}{5}.$”; “If $v$ is an eigenvector of a matrix $A$ corresponding to the eigenvalue $\lambda =2,$ then $7v$ is also an eigenvector of $A$ corresponding to $\lambda =2.$” only.

Answer An eigenvector of an invertible matrix $A$ that corresponds to the eigenvalue $\lambda =6$ is also an eigenvector of the inverse ${A}^{-1}$ that corresponds to the same eigenvalue $\lambda =6.$: false

Answer If $v$ is an eigenvector of a matrix $A$ corresponding to the eigenvalue $\lambda =2,$ then $7v$ is also an eigenvector of $A$ corresponding to $\lambda =2.$: true

Answer If $v$ is an eigenvector of an invertible matrix $A$ that corresponds to the eigenvalue $\lambda =5$ then $v$ is also an eigenvector of the matrix ${A}^{-1}$ that corresponds to $\lambda =\frac{1}{5}.$: true
