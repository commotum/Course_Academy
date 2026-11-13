# 17592186051014 Linear Combinations of Vectors and Their Properties

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186097835 — Introduction

A **linear combination** of two vectors $\mathbf{a}$ and $\mathbf{b}$ is a sum of multiples of the two vectors. 

For example, let's consider the vectors $\mathbf a$ and $\mathbf b,$ shown below:

![](images/00/0091edb7bcd026737e7bdf9d56e5a9932970d62902a185f76599cdf18bfd9d45.png)

One particular linear combination of these vectors is 

$$
2 \mathbf{a} + 3 \mathbf{b} = 2 \cdot \mathbf{a} + 3 \cdot \mathbf{b}.
$$

If we draw this linear combination in the coordinate plane, we get the following:

![](images/73/73a73b7e90c9e82e57f88d04079a69fa2cce082fc6d7f4667fae1cb4190ea46a.png)



### example 17592186096449 — Finding a Linear Combination of Two Vectors

Given the vectors $\mathbf{a}$ and $\mathbf{b}$ shown below, draw the linear combination $2\mathbf{a}+3\mathbf{b}$.

![](images/32/325e4a450d89ee1f5db4afd237dbc7d58efafec72d080386788f0491cc35950b.png)

- The vector $2\mathbf{a}$ has the same direction as $\mathbf{a}$ but twice the magnitude.
- Likewise, the vector $3\mathbf{b}$ has the same direction as $\mathbf{b}$ but three times the magnitude.

![](images/06/066784522a39671fe57b157c6c692f5c56295126b8ec6f150d917e783ab63400.png)

Now, we can draw $3\mathbf{b}$ starting from the head of $2\mathbf{a}$. The resultant
$2\mathbf{a}+3\mathbf{b}$
goes from the tail of $2\mathbf{a}$ to the head of $3\mathbf{b}$.

![](images/d1/d1dd084ad4f8f717afac515471bcba679fbe545f266435a57fb1c94d0d5c9cca.png)

### tutorial 17592186097836 — An Important Property of Linear Combinations

If two vectors are not parallel, then each linear combination can only be written in one way. 

For example, if we have two vectors $\mathbf{a},\mathbf{b}$ with $\mathbf{a} \nparallel \mathbf{b},$ and two real numbers $\alpha,\beta,$ then the equality

$$
2 \mathbf{a} + 3 \mathbf{b} = \alpha \mathbf{a} + \beta \mathbf{b}
$$

holds if and only if $\alpha=2$ and $\beta=3$.

In other words, the pair of numbers $\alpha,\beta$ defines a unique vector $\alpha \mathbf{a} + \beta \mathbf{b}.$ That is to say, if

$$
\alpha_1 \mathbf{a} + \beta_1 \mathbf{b} = \alpha_2 \mathbf{a} + \beta_2 \mathbf{b},
$$

then $\alpha_1 = \alpha_2$ and $\beta_1 = \beta_2.$

**Watch out!** This property holds only if two vectors *are not parallel*.



### example 17592186096450 — Solving a Statement With Linear Combinations Whose Coefficients Are Linear Functions

Suppose we are given two vectors $\mathbf{a}$ and $\mathbf{b}$ where $\mathbf{a} \nparallel \mathbf{b}$. Find $\alpha$ and $\beta$, if

$\mathbf{a}+7\mathbf{b}=(2\alpha+\beta)\mathbf{a}-\beta\mathbf{b}$.

Since $\mathbf{a} \nparallel \mathbf{b}$, the linear combination can only be written in one way. So, the coefficients of $\mathbf{a}$ must be equal, and the coefficients of $\mathbf{b}$ must be equal.

Equating the coefficients, we get:

$$
{\left\{  \begin{array}{l}1 = 2 \alpha  + \beta  \\ 7 = - \beta \end{array} \right. }
$$

From the second equation, we obtain

$$
\begin{aligned}
β &= -7
\end{aligned}
$$

Substituting back into the first equation, we get:

$$
\begin{aligned}
1 &= 2α + β \\
1 &= 2α + (-7) \\
8 &= 2α \\
α &= 4
\end{aligned}
$$

So, we conclude that $\alpha = 4$ and $\beta = -7$.

## Representative practice (first three per skill; full bank in practice.json)

### Finding a Linear Combination of Two Vectors (20 captured questions)

Question 17592186097163 — None

![](images/cc/cced81f954aede18a47dbc0816e7045e82cf4ed5443fa1e4e8865d5583697f08.png)

Given the vectors $a$ and $b$ shown above, which of the following could be the linear combination $2a - b$?

Solution: 

Question 17592186097180 — None

![](images/67/6707c6a7967fd53d53897bcf10e6174ee11865f269743883c9a9ff487a23ef0f.png)

Given the vectors $a$ and $b$ shown above, which of the following could be the linear combination $3a + 2b$?

Solution: 

Question 17592186572677 — question.difficulty/moderate

![](images/21/212a339585b98f156d68f2e4260c0acbb474c51782b6d72acf0b89fd5c1fe69e.png)

Given the vectors $a$ and $b$ shown above, which of the following could be the linear combination $2a-2b?$

Solution: First, recall that

$$
2a-2b=2a+(-2b).
$$

- The vector $2a$ has the same direction as $a$ but twice the magnitude.

- The vector $-2b$ has the direction that is opposite to $b$ but twice the magnitude.

![](images/c1/c1cc845ddfe16f12169625e5f8404d3d92558b885ffde8c3ab02cdb2c096f699.png)

Now, we can draw $-2b$ starting from the head of $2a.$ The resultant 

$$
2a-2b
$$

goes from the tail of $2a$ to the head of $-2b.$

![](images/5d/5d22db7e37ff1c5b55f1ec595da919f987a6c1fea4247cf5a075f27c198ba545.png)

Answer selection: images/de/de03a1be920089723cdf3ab761a7ab02a3bbfe085ac9eb927a7dcd7163b458b1.png

### Solving a Statement With Linear Combinations Whose Coefficients Are Linear Functions (19 captured questions)

Question 17592186096970 — question.difficulty/easy

Suppose we are given two vectors $a$ and $b$ where $a∦b$. Find $s$ and $t$, if
$5a + 4b = (2s + t)a + (s - t)b$.

Solution: 

Question 17592186097047 — None

Suppose we are given two vectors $a$ and $b$ where $a∦b$. Find $λ$ and $μ$, if
$(1 + λ)a + 2λb = μa + 4μb$.

Solution: 

Question 17592186572716 — question.difficulty/easy

Suppose we are given two vectors $a$ and $b$ where $a∦b.$ Find $\lambda$ and $\mu ,$ if 

$$
a-2b=(3\lambda -\mu )a-(\lambda -4\mu )b.
$$

$\lambda =$
{{field-1}}$,\,\mu =$
{{field-2}}

Solution: Since $a∦b,$ the linear combination can only be written in one way. So, the coefficients of $a$ must be equal, and the coefficients of $b$ must be equal.

Equating the coefficients, we get:

$$
\left\{\begin{aligned}3\lambda -\mu &=1 \\ \lambda -4\mu &=2\end{aligned}\right.
$$

From the first equation, we obtain:

$$
\mu =3\lambda -1
$$

Substituting back into the second equation, we get:

$$
\begin{aligned}\lambda -4\mu  & =2 \\ \lambda -4(3\lambda -1) & =2 \\ \lambda -12\lambda +4 & =2 \\ -11\lambda  & =-2 \\ \lambda  & =\frac{2}{11}\end{aligned}
$$

Finally, we have

$$
\begin{aligned}\mu  & =3\lambda -1 \\  & =3\cdot \frac{2}{11}-1 \\  & =-\frac{5}{11}.\end{aligned}
$$

Answer field-1: \frac{2}{11}

Answer field-2: -\frac{5}{11}
