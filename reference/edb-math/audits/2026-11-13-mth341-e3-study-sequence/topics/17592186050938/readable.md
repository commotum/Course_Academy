# 17592186050938 Calculating the Dot Product Using Angle and Magnitude

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186060917 — Introduction

The **dot product** (or **scalar product**) of two vectors $\mathbf{a}$ and $\mathbf{b}$ is defined as

$$
\mathbf{a} \cdot \mathbf{b} = |\,\mathbf{a}\,| \cdot |\,\mathbf{b}\,| \cdot \cos\theta,
$$

where $\theta$ is the angle formed between the vectors when their tails are placed at the same point.

![](images/87/87395f5fe6657cec5dd98eed9c3c535a5f6dc9f259d4558c86a4d618c904e5c1.png)

For example, suppose we know that

$$
\begin{aligned}
\mid \mathbf{a} &= 2
\end{aligned}
$$

$$
\begin{aligned}
\mid \mathbf{b} &= 4
\end{aligned}
$$

and

$$
\theta = \dfrac{2\pi}{3}
$$

We can now define the **dot product** (or **scalar product**) of $\mathbf{a}$ and $\mathbf{b}$ as follows:

$$
\begin{aligned}\mathbf{a}\cdot \mathbf{b} & =|\hspace{0.167em}\mathbf{a}\hspace{0.167em}|\cdot |\hspace{0.167em}\mathbf{b}\hspace{0.167em}|\cdot \operatorname{cos}\theta  \\  & =2\cdot 4\cdot \operatorname{cos}\left(\frac{2\pi }{3}\right) \\  & =2\cdot 4\cdot \left(-\frac{1}{2}\right) \\  & =-4\end{aligned}
$$



### example 17592186059539 — Calculating the Dot Product of Two Vectors Given Their Magnitudes and Angle

For two vectors $\mathbf a$ and $\mathbf b$, we have $\mid \mathbf{a}|=45$, $\mid \mathbf{b}|=12$, and the angle between the vectors is $\theta=77^\circ$. Find $\mathbf{a}\cdot\mathbf{b}$ rounded to $3$ decimal places.

Using the formula for the dot product, we obtain:

$$
\begin{aligned}\mathbf{a}\cdot \mathbf{b} & =|\hspace{0.167em}\mathbf{a}\hspace{0.167em}|\cdot |\hspace{0.167em}\mathbf{b}\hspace{0.167em}|\cdot \operatorname{cos}\theta  \\  & =45\cdot 12\cdot \operatorname{cos}{77}^{∘} \\  & \approx 45\cdot 12\cdot 0.224\hspace{0.167em}951 \\  & \approx 121.474\end{aligned}
$$

### example 17592186059540 — Calculating the Dot Product of Two Vectors Given Their Magnitudes and Directions

Suppose that the vectors $\mathbf a$ and $\mathbf b$ are two vectors defined in the $x$-$y$ plane. The vector $\mathbf{a}$ makes a counterclockwise angle of $127^\circ$ with the positive $x$-axis and has $\mid \mathbf{a}|=4$, while the vector $\mathbf{b}$ makes a clockwise angle of $23^\circ$ with the positive $x$-axis and has $\mid \mathbf{b}|=3$. Find $\mathbf{a} \cdot \mathbf{b}$.

If $\mathbf{a}$ makes an angle of $127^\circ$ with the positive $x$-axis and $\mathbf{b}$ makes an angle of $-23^\circ$ with the positive $x$-axis, then the angle between the vectors is

$$
\begin{aligned}
θ &= \mid 127^{∘} - (-23^{∘})|= 150^{∘}
\end{aligned}
$$

![](images/e1/e16c58888810038f7ef5b5794e74d87fe8af6b273f0d527be94181cb79f5477f.png)

Now, using the formula for the dot product, we obtain:

$$
\begin{aligned}\mathbf{a}\cdot \mathbf{b} & =|\hspace{0.167em}\mathbf{a}\hspace{0.167em}|\cdot |\hspace{0.167em}\mathbf{b}\hspace{0.167em}|\cdot \operatorname{cos}\theta  \\  & =4\cdot 3\cdot \operatorname{cos}{150}^{∘} \\  & =4\cdot 3\cdot \left(-\frac{\sqrt{3}}{2}\right) \\  & =-6\sqrt{3}\end{aligned}
$$

### tutorial 17592186060918 — Important Properties

The dot product satisfies many properties that we would normally expect multiplication to satisfy. Given the vectors $\mathbf{a},\mathbf{b},\mathbf{c}$ and any scalar $\lambda$, the following properties hold.

- The dot product distributes over addition:
$$
\begin{aligned}(\mathbf{a}+\mathbf{b})\cdot \mathbf{c} & =\mathbf{a}\cdot \mathbf{c}+\mathbf{b}\cdot \mathbf{c} \\ \mathbf{c}\cdot (\mathbf{a}+\mathbf{b}) & =\mathbf{c}\cdot \mathbf{a}+\mathbf{c}\cdot \mathbf{b}\end{aligned}
$$
- The dot product is associative with respect to scalar multiplication:
$$
\begin{aligned}(\lambda \mathbf{a})\cdot \mathbf{b} & =\lambda (\mathbf{a}\cdot \mathbf{b}) \\ \mathbf{a}\cdot (\lambda \mathbf{b}) & =\lambda (\mathbf{a}\cdot \mathbf{b})\end{aligned}
$$
- The dot product is commutative:
$\mathbf{a} \cdot \mathbf{b} = \mathbf{b} \cdot \mathbf{a}$



### example 17592186059541 — Calculating Dot Product Expressions Using the Properties of the Dot Product

Find $(2\mathbf{a}-\mathbf{b}) \cdot \mathbf{c}$, if $\mathbf{a} \cdot \mathbf{c} = 2$ and $\mathbf{b} \cdot \mathbf{c} = -5$.

Using the properties of the dot product, we have:

$$
\begin{aligned}
(2a - b) \cdot c &= (2a) \cdot c - b \cdot c \\
&= 2(a \cdot c) - b \cdot c \\
&= 2 \cdot 2 - (-5) \\
&= 9
\end{aligned}
$$

### tutorial 17592186060919 — The Dot Product of Perpendicular Vectors

Two nonzero vectors $\mathbf{a}$ and $\mathbf{b}$ are **perpendicular** if the angle between them is

$$
\theta=90^\circ
$$

We can denote that two vectors are perpendicular using the symbol $\perp$, as follows:

$$
\mathbf{a} \perp \mathbf{b}
$$

In general, the dot product of two perpendicular vectors is $0$. If $\mathbf{a} \perp \mathbf{b}$, and

$$
\theta = 90^\circ
$$

then

$$
\begin{aligned}\mathbf{a}\cdot \mathbf{b} & =|\hspace{0.167em}\mathbf{a}\hspace{0.167em}|\cdot |\hspace{0.167em}\mathbf{b}\hspace{0.167em}|\cdot \operatorname{cos}{90}^{∘} \\  & =|\hspace{0.167em}\mathbf{a}\hspace{0.167em}|\cdot |\hspace{0.167em}\mathbf{b}\hspace{0.167em}|\cdot 0 \\  & =0.\end{aligned}
$$

The converse is also true. If $\mathbf a$ and $\mathbf b$ are nonzero vectors, then

$$
\mathbf{a} \perp \mathbf{b} \quad\Leftrightarrow\quad \mathbf{a} \cdot \mathbf{b} = 0
$$



### example 17592186059542 — Calculating the Dot Product of Perpendicular Vectors

Let $\mathbf{a}$ and $\mathbf{b}$ be two vectors with magnitudes $\mid \mathbf{a}|=13\sqrt{17}$ and $\mid \mathbf{b}|=146$, and let the angle between the vectors be $\theta=\dfrac{\pi}{2}$. Find $\mathbf{a}\cdot\mathbf{b}$.

Since the angle between the vectors is

$$
\theta = \dfrac\pi 2
$$

the vectors are perpendicular and thus

$$
\mathbf{a} \cdot \mathbf{b} = 0
$$

We can confirm this. Using the formula for the dot product, we obtain:

$$
\begin{aligned}\mathbf{a}\cdot \mathbf{b} & =|\hspace{0.167em}\mathbf{a}\hspace{0.167em}|\cdot |\hspace{0.167em}\mathbf{b}\hspace{0.167em}|\cdot \operatorname{cos}\theta  \\  & =13\sqrt{17}\cdot 146\cdot \operatorname{cos}\left(\frac{\pi }{2}\right) \\  & =13\sqrt{17}\cdot 146\cdot 0 \\  & =0\end{aligned}
$$

## Representative practice (first three per skill; full bank in practice.json)

### Calculating the Dot Product of Two Vectors Given Their Magnitudes and Angle (2 captured questions)

Question 17592186060182 — None

For two vectors $u$ and $v$, we have $\mid u|= 12$, $\mid v|= 3$, and the angle between the vectors is $120^{∘}$. Find $u \cdot v$.

> A scientific calculator is required to answer this question.

Solution: 

Question 17592186060183 — None

For two vectors $u$ and $v$, we have $\mid u|= 8$, $\mid v|= 2$, and the angle between the vectors is $150^{∘}$. Find $u \cdot v$.

> A scientific calculator is required to answer this question.

Solution: 

### Calculating the Dot Product of Two Vectors Given Their Magnitudes and Directions (2 captured questions)

Question 17592186060033 — None

Suppose that the vectors $a$ and $b$ are two vectors defined in the $x$-$y$ plane. The vector $a$ makes a counterclockwise angle of $11^{∘}$ with the positive $x$-axis and has $\mid a|= 20$, while the vector $b$ makes a counterclockwise angle of $28^{∘}$ with the positive $x$-axis and has $\mid b|= 9$. Find $a \cdot b$ rounded to $3$ decimal places.

> A scientific calculator is required to answer this question.

Solution: 

Question 17592186060034 — None

Suppose that the vectors $a$ and $b$ are two vectors defined in the $x$-$y$ plane. The vector $a$ makes a counterclockwise angle of $160^{∘}$ with the positive $x$-axis and has $\mid a|= 18$, while the vector $b$ makes a counterclockwise angle of $160^{∘}$ with the positive $x$-axis and has $\mid b|= 0.5$. Find $a \cdot b$.

> A scientific calculator is required to answer this question.

Solution: 

### Calculating Dot Product Expressions Using the Properties of the Dot Product (2 captured questions)

Question 17592186060156 — None

Find $(5a + 2b) \cdot c$, if $a \cdot c =-1$ and $b \cdot c = 2$.

Solution: 

Question 17592186060180 — None

Find $(3a + 4b) \cdot c$, if $c \cdot a = 3$ and $b \cdot c = 4$.

Solution: 

### Calculating the Dot Product of Perpendicular Vectors (7 captured questions)

Question 17592186060032 — None

Let $u$ and $v$ be two vectors with magnitudes $\mid u|= 7$ and $\mid v|= 5$, and let the angle between the vectors be $θ = 90^{∘}$. Find $u \cdot v$.

Solution: 

Question 17592186060181 — None

Find $(5a - 2b) \cdot c$, knowing that $a⊥c$ and $b \cdot c = 2$.

Solution: 

Question 17592186677698 — question.difficulty/moderate

Find $(5a + 8b) \cdot c$, knowing that $b \perp c$ and $a \cdot c = 3$.

Solution: Since $b \perp c$, we have $b \cdot c = 0$. Distribute the dot product and take the scalar coefficients outside:

$$
\begin{aligned}
(5a + 8b) \cdot c &= 5(a \cdot c) + 8(b \cdot c) \\
&= 5 \cdot (3) + 8 \cdot (0) \\
&= (15) + 0 \\
&= 15
\end{aligned}
$$

Answer selection: 15
