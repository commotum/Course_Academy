# 17592186049436 The Vector Equation of a Plane

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186121049 — Introduction

Suppose we know that a plane $\Pi$ passes through the point $P(1,1,2)$ and that the vector $\mathbf{n}=\langle 0,0,3 \rangle$ is perpendicular to the plane. Let's write down an equation of this plane using the dot product.

![](images/0f/0f8353480099369ad92701d1799f72d46eab4bbe5c17add8cb37a4f34074311b.png)

We start by considering an arbitrary point $R(x,y,z)$ that lies on the plane. The position vectors of the points $R$ and $P$ are $\mathbf{r}=\langle x,y,z \rangle$ and $\mathbf{p}=\langle 1,1,2 \rangle$ respectively. So, the vector

$$
\begin{aligned}\overset{\to }{PR} & =\mathbf{r}-\mathbf{p} \\  & =\mathbf{r}-⟨1,1,2⟩\end{aligned}
$$

is parallel to the plane. Therefore, $\overrightarrow{PR} \perp \mathbf{n},$ as shown below.

![](images/28/28b6770bd681257b1030679a421b80e3f3d1e8fbb86d2060b64c7301d0878c5c.png)

Now, recall that if two nonzero vectors are perpendicular, then their dot product is zero:

$$
\overrightarrow{PR}\perp \mathbf{n} \quad \Leftrightarrow \quad \overrightarrow{PR}\cdot \mathbf{n} = 0
$$

So, we get the equation

$$
\begin{aligned}(\mathbf{r}-\mathbf{p})\cdot \mathbf{n} & =0.\end{aligned}
$$

This equation is called the **vector equation of the plane** that passes through the point $P(x_0,y_0,z_0)$ and is perpendicular to the vector $\mathbf{n}.$ In our case, we obtain

$$
(\mathbf{r} - \langle 1,1,2 \rangle) \cdot \langle 0,0,3 \rangle = 0.
$$

**Note:** Using the properties of the dot product, we can arrive at an alternative vector equation given by

$$
\begin{aligned}(\mathbf{r}-\mathbf{p})\cdot \mathbf{n} & =0 \\ \mathbf{r}\cdot \mathbf{n}-\mathbf{p}\cdot \mathbf{n} & =0 \\ \mathbf{r}\cdot \mathbf{n} & =\mathbf{p}\cdot \mathbf{n} \\ \mathbf{r}\cdot \mathbf{n} & =c\end{aligned}
$$

where $c = \mathbf{p} \cdot \mathbf{n}$ is a (scalar) constant.



### example 17592186119640 — Finding the Vector Equation of the Plane Perpendicular to a Given Vector

Find an equation of the plane that contains the point $P(-3,2,1)$ and is perpendicular to the vector $\mathbf{n}= \langle 0, 2, 0 \rangle.$

First, we note that the position vector of $P$ is $\mathbf{p}=\langle -3,2,1 \rangle$ and $\mathbf{n}=\langle 0,2,0 \rangle$ is normal to the plane.

The equation of the plane that passes through the point $P(x_0,y_0,z_0)$ and is perpendicular to the vector $\mathbf{n}$ can be given as

$$
(\mathbf{r} - \mathbf{p}) \cdot \mathbf{n} = 0,
$$

where $\mathbf{r}$ is the position vector of any point on the plane, and $\mathbf p$ is the position vector of $P.$

So, we have

$$
\begin{aligned}(\mathbf{r}-\mathbf{p})\cdot \mathbf{n} & =0 \\ \mathbf{r}\cdot \mathbf{n}-\mathbf{p}\cdot \mathbf{n} & =0 \\ \mathbf{r}\cdot \mathbf{n} & =\mathbf{p}\cdot \mathbf{n} \\ \mathbf{r}\cdot ⟨0,2,0⟩ & =⟨-3,2,1⟩\cdot ⟨0,2,0⟩ \\ \mathbf{r}\cdot ⟨0,2,0⟩ & =4.\end{aligned}
$$

### tutorial 17592186121120 — A Vector Parallel To a Plane

Suppose we have a plane with the following normal vector: 

$$
\mathbf{n}=\langle -1,2,1 \rangle
$$

Let's use the scalar product to find a vector that is parallel to this plane.

We denote our parallel vector as $\mathbf{v} = \langle t_1,t_2,t_3 \rangle.$ Now, since $\mathbf{v} \perp \mathbf{n},$ we must have

$$
\begin{aligned}\mathbf{v}\cdot \mathbf{n} & =0 \\ ⟨{t}_{1},{t}_{2},{t}_{3}⟩\cdot ⟨-1,2,1⟩ & =0 \\ -{t}_{1}+2{t}_{2}+{t}_{3} & =0\end{aligned}
$$

We now need to find a nonzero solution to this equation. To do that, we solve the equation for *one* of the variables (it doesn't matter which one). For example, let's solve our equation for the variable $t_1\mathbin{:}$

$$
\begin{aligned}{t}_{1} & =2{t}_{2}+{t}_{3}\end{aligned}
$$

Here, the variable $t_1$ depends on $t_2$ and $t_3,$ which, in turn, can be *any* real numbers. The variables $t_2$ and $t_3$ are called **free variables**.

Hence, the general form of our vector $\mathbf{v}$ is

$$
\mathbf{v}=\langle 2t_2+t_3, \, t_2, \, t_3 \rangle,
$$

where $t_2, t_3 \in (-\infty,\infty).$

To find a particular vector parallel to the plane, we can substitute any values for $t_2$ and $t_3\mathbin{:}$

- For example, setting $t_2=0$ and $t_3=1$, we get

$$
\mathbf{v}_1= \langle 1, 0, 1 \rangle.
$$

- Or, we could set $t_2=1$ and $t_3=0$ and get

$$
\mathbf{v}_2 = \langle 2, 1, 0 \rangle.
$$

**Note:** There are infinitely many vectors parallel to a given plane. In our example, we found only two particular vectors.



### example 17592186119641 — Finding a Vector That Is Parallel To a Plane

A nonzero vector $\langle 0,\, \bbox[2pt,Gainsboro]{b}, \: \bbox[2pt,Gainsboro]{c} \rangle$ is parallel to the plane $\mathbf{r} \cdot \langle 2, -1, 4 \rangle  = 3.$ What is the value of $\dfrac{b}{c}?$

We need a vector $\mathbf{v} = \langle t_1,t_2,t_3 \rangle$ that is parallel to the given plane. 

From the equation $\mathbf{r} \cdot \langle 2, -1, 4 \rangle  = 3$ of the plane, we get the normal vector $\mathbf{n}=\langle 2, -1, 4 \rangle.$ So, $\mathbf{v} \perp \mathbf{n}$ and we have the following:

$$
\begin{aligned}\mathbf{v}\cdot \mathbf{n} & =0 \\ ⟨{t}_{1},{t}_{2},{t}_{3}⟩\cdot ⟨2,-1,4⟩ & =0 \\ 2{t}_{1}-{t}_{2}+4{t}_{3} & =0 \\ {t}_{2} & =2{t}_{1}+4{t}_{3}\end{aligned}
$$

Hence, we obtain 

$$
\mathbf{v}=\langle t_1, 2t_1 + 4t_3, t_3 \rangle,
$$

where $t_1,t_3 \in (-\infty,\infty).$ 

We are told that the first component of $\mathbf{v}$ equals $0.$ So, we must set $t_1=0.$ 

Since $\mathbf{v}$ is nonzero, we can pick any $t_3 \neq 0.$ For example, setting $t_3=1$, we get

$$
\mathbf{v} = \langle 0,\, \bbox[2pt,Gainsboro]{4}, \, \bbox[2pt,Gainsboro]{1} \rangle.
$$

Therefore, $\dfrac{b}{c} = 4.$

### example 17592186119642 — Finding the Vector Equation of the Plane Perpendicular to a Given Straight Line

Find an equation of the plane that passes through the point $Q(\sqrt{2},0,-5)$ and is perpendicular to the line

$$
\left\{\begin{aligned}x &=3 \\ y &=-1+\sqrt{3}t \\ z &=5-t.\end{aligned}\right.
$$

Note that the position vector of $Q$ is $\mathbf{q}=\langle \sqrt{2},0,-5 \rangle.$ Converting the parametric equations of the line to vector form, we get
$$
{\left\{  \begin{array}{l}x = 3 \\ y = - 1 + \sqrt{3} t \\ z = 5 - t\end{array} \right. } \qquad  \Longrightarrow \qquad

\langle x, y, z \rangle= \langle 3, -1 , 5 \rangle
+t \ \underbrace{\langle 0 , \sqrt{3} , -1 \rangle}_{\large \mathbf{v}} .
$$

The direction vector of the line is $\mathbf{v}=\langle  0 , \sqrt{3} , -1\rangle,$ so a normal vector to the plane is 

$$
\mathbf{n}=\mathbf{v}=\langle  0 , \sqrt{3} , -1 \rangle.
$$

Therefore, the equation of the plane is given by

$$
\begin{aligned}(r-q)\cdot n & =0 \\ r\cdot n-q\cdot n & =0 \\ r\cdot n & =q\cdot n \\ r\cdot ⟨0,\sqrt{3},-1⟩ & =⟨\sqrt{2},0,-5⟩\cdot ⟨0,\sqrt{3},-1⟩ \\ r\cdot ⟨0,\sqrt{3},-1⟩ & =5.\end{aligned}
$$

## Representative practice (first three per skill; full bank in practice.json)

### Finding the Vector Equation of the Plane Perpendicular to a Given Vector (16 captured questions)

Question 17592186120217 — question.difficulty/easy

Find an equation of the plane that contains the point $P(2,-5,3)$ and is perpendicular to the vector $\mathbf{n}=⟨-1,2,-3⟩.$

Solution: First, we note that the position vector of $P$ is $\mathbf{p}=⟨2,-5,3⟩,$ and $\mathbf{n}=⟨-1,2,-3⟩$ is normal to the plane.

The equation of the plane that passes through the point $P({x}_{0},{y}_{0},{z}_{0})$ and is perpendicular to the vector $\mathbf{n}$ can be given as

$$
(\mathbf{r}-\mathbf{p})\cdot \mathbf{n}=0,
$$

where $\mathbf{r}$ is the position vector of any point on the plane, and $\mathbf{p}$ is the position vector of $P.$

So, we have

$$
\begin{aligned}(\mathbf{r}-\mathbf{p})\cdot \mathbf{n} & =0 \\ \mathbf{r}\cdot \mathbf{n}-\mathbf{p}\cdot \mathbf{n} & =0 \\ \mathbf{r}\cdot \mathbf{n} & =\mathbf{p}\cdot \mathbf{n} \\ \mathbf{r}\cdot ⟨-1,2,-3⟩ & =⟨2,-5,3⟩\cdot ⟨-1,2,-3⟩ \\ \mathbf{r}\cdot ⟨-1,2,-3⟩ & =-21.\end{aligned}
$$

Answer selection: r\cdot ⟨-1,2,-3⟩=-21

Question 17592186120222 — question.difficulty/easy

Find an equation of the plane that contains the point $P(\sqrt{2},3,4)$ and is perpendicular to the vector $\mathbf{n}=2\sqrt{2}\mathbf{i}+7\mathbf{j}-6\mathbf{k}.$

Solution: First, we note that the position vector of $P$ is $p=\sqrt{2}i+3j+4k,$ and $n=2\sqrt{2}i+7j-6k$ is normal to the plane.

The equation of the plane that passes through the point $P({x}_{0},{y}_{0},{z}_{0})$ and is perpendicular to the vector $n$ can be given as

$$
(r-p)\cdot n=0,
$$

where $r$ is the position vector of any point on the plane, and $p$ is the position vector of $P.$

So, we have

$$
\begin{aligned}(r-p)\cdot n & =0 \\ r\cdot n-p\cdot n & =0 \\ r\cdot n & =p\cdot n \\ r\cdot (2\sqrt{2}i+7j-6k) & =(\sqrt{2}i+3j+4k)\cdot (2\sqrt{2}i+7j-6k) \\ r\cdot (2\sqrt{2}i+7j-6k) & =1.\end{aligned}
$$

Answer selection: r\cdot (2\sqrt{2}i+7j-6k)=1

Question 17592186262809 — question.difficulty/easy

Find an equation of the plane that contains the point $P(\sqrt{5},-1,2)$ and is perpendicular to the vector $\mathbf{n}=\sqrt{5}\mathbf{i}-3\mathbf{j}+2\mathbf{k}.$

Solution: First, we note that the position vector of $P$ is $\mathbf{p}=\sqrt{5}\mathbf{i}-\mathbf{j}+2\mathbf{k},$ and $\mathbf{n}=\sqrt{5}\mathbf{i}-3\mathbf{j}+2\mathbf{k}$ is normal to the plane.

The equation of the plane that passes through the point $P({x}_{0},{y}_{0},{z}_{0})$ and is perpendicular to the vector $\mathbf{n}$ can be given as

$$
(\mathbf{r}-\mathbf{p})\cdot \mathbf{n}=0,
$$

where $\mathbf{r}$ is the position vector of any point on the plane, and $\mathbf{p}$ is the position vector of $P.$

So, we have

$$
\begin{aligned}(\mathbf{r}-\mathbf{p})\cdot \mathbf{n} & =0 \\ \mathbf{r}\cdot \mathbf{n}-\mathbf{p}\cdot \mathbf{n} & =0 \\ \mathbf{r}\cdot \mathbf{n} & =\mathbf{p}\cdot \mathbf{n} \\ \mathbf{r}\cdot (\sqrt{5}\mathbf{i}-3\mathbf{j}+2\mathbf{k}) & =(\sqrt{5}\mathbf{i}-\mathbf{j}+2\mathbf{k})\cdot (\sqrt{5}\mathbf{i}-3\mathbf{j}+2\mathbf{k}) \\ \mathbf{r}\cdot (\sqrt{5}\mathbf{i}-3\mathbf{j}+2\mathbf{k}) & =12.\end{aligned}
$$

Answer selection: r\cdot (\sqrt{5}i-3j+2k)=12

### Finding a Vector That Is Parallel To a Plane (17 captured questions)

Question 17592186120248 — question.difficulty/moderate

A nonzero vector $⟨\bbox[Gainsboro, 2pt]{a},\hspace{0.222em}\bbox[Gainsboro, 2pt]{b},\hspace{0.222em}0⟩$ is parallel to the plane $\mathbf{r}\cdot ⟨6,-2,0⟩=-14.$ What is the value of $\frac{a}{b}?$

Solution: We need a vector $\mathbf{v}=⟨{t}_{1},{t}_{2},{t}_{3}⟩$ that is parallel to the given plane. 

From the equation $\mathbf{r}\cdot ⟨6,-2,0⟩=-14$ of the plane, we get the normal vector $\mathbf{n}=⟨6,-2,0⟩.$ So, $\mathbf{v}⊥\mathbf{n}$ and we have the following:

$$
\begin{aligned}\mathbf{v}\cdot \mathbf{n} & =0 \\ ⟨{t}_{1},{t}_{2},{t}_{3}⟩\cdot ⟨6,-2,0⟩ & =0 \\ 6{t}_{1}-2{t}_{2} & =0 \\ {t}_{2} & =3{t}_{1}\end{aligned}
$$

Hence, we obtain 

$$
\mathbf{v}=⟨{t}_{1},3{t}_{1},{t}_{3}⟩,
$$

where ${t}_{1},{t}_{3}\in (-\mathrm{∞},\mathrm{∞}).$ 

We are told that the third component of $\mathbf{v}$ eqauls $0.$ So, we must set ${t}_{3}=0.$ 

Since $\mathbf{v}$ is nonzero, we can pick any ${t}_{1}\ne 0.$ For example, setting ${t}_{1}=1$, we get

$$
\mathbf{v}=⟨\bbox[Gainsboro, 2pt]{1},\hspace{0.167em}\bbox[Gainsboro, 2pt]{3},\hspace{0.167em}0⟩.
$$

Therefore, $\frac{a}{b}=\frac{1}{3}.$

Answer selection: \frac{1}{3}

Question 17592186120508 — question.difficulty/moderate

A nonzero vector $⟨\bbox[Gainsboro, 2pt]{a},\hspace{0.222em}0,\hspace{0.222em}\bbox[Gainsboro, 2pt]{c}⟩$ is parallel to the plane $\mathbf{r}\cdot ⟨3,-3,1⟩=-12.$ What is the value of $\frac{a}{c}?$

Solution: We need a vector $\mathbf{v}=⟨{t}_{1},{t}_{2},{t}_{3}⟩$ that is parallel to the given plane. 

From the equation of the plane, $\mathbf{r}\cdot ⟨3,-3,1⟩=-12,$  we get the normal vector $\mathbf{n}=⟨3,-3,1⟩.$ So, $\mathbf{v}⊥\mathbf{n}$ and we have the following:

$$
\begin{aligned}\mathbf{v}\cdot \mathbf{n} & =0 \\ ⟨{t}_{1},{t}_{2},{t}_{3}⟩\cdot ⟨3,-3,1⟩ & =0 \\ 3{t}_{1}-3{t}_{2}+{t}_{3} & =0 \\ {t}_{3} & =3{t}_{2}-3{t}_{1}\end{aligned}
$$

Hence, we obtain 

$$
\mathbf{v}=⟨{t}_{1},{t}_{2},3{t}_{2}-3{t}_{1}⟩,
$$

where ${t}_{1},{t}_{2}\in (-\mathrm{∞},\mathrm{∞}).$ 

We are told that the second component of $\mathbf{v}$ eqauls $0.$ So, we must set ${t}_{2}=0.$ 

Since $\mathbf{v}$ is nonzero, we can pick any ${t}_{1}\ne 0.$ For example, setting ${t}_{1}=1$, we get

$$
\mathbf{v}=⟨\bbox[Gainsboro, 2pt]{1},\hspace{0.167em}0,\bbox[Gainsboro, 2pt]{-3}⟩.
$$

Therefore, $\frac{a}{c}=\frac{1}{-3}=-\frac{1}{3}.$

Answer selection: -\frac{1}{3}

Question 17592186262837 — question.difficulty/moderate

A nonzero vector $⟨0,\hspace{0.167em}\bbox[Gainsboro, 2pt]{b},\hspace{0.222em}\bbox[Gainsboro, 2pt]{c}⟩$ is parallel to the plane $\mathbf{r}\cdot ⟨-3,1,-2⟩=7.$ What is the value of $\frac{b}{c}?$

Solution: We need a vector $\mathbf{v}=⟨{t}_{1},{t}_{2},{t}_{3}⟩$ that is parallel to the given plane. 

From the equation $\mathbf{r}\cdot ⟨-3,1,-2⟩=7$ of the plane, we get the normal vector $\mathbf{n}=⟨-3,1,-2⟩.$ So, $\mathbf{v}⊥\mathbf{n}$ and we have the following:

$$
\begin{aligned}\mathbf{v}\cdot \mathbf{n} & =0 \\ ⟨{t}_{1},{t}_{2},{t}_{3}⟩\cdot ⟨-3,1,-2⟩ & =0 \\ -3{t}_{1}+{t}_{2}-2{t}_{3} & =0 \\ {t}_{2} & =3{t}_{1}+2{t}_{3}\end{aligned}
$$

Hence, we obtain 

$$
\mathbf{v}=⟨{t}_{1},\hspace{0.167em}3{t}_{1}+2{t}_{3},\hspace{0.167em}{t}_{3}⟩,
$$

where ${t}_{1},{t}_{3}\in (-\mathrm{∞},\mathrm{∞}).$ 

We are told that the first component of $\mathbf{v}$ equals $0.$ So, we must set ${t}_{1}=0.$ 

Since $\mathbf{v}$ is nonzero, we can pick any ${t}_{3}\ne 0.$ For example, setting ${t}_{3}=1$, we get

$$
\mathbf{v}=⟨0,\hspace{0.167em}\bbox[Gainsboro, 2pt]{2},\hspace{0.167em}\bbox[Gainsboro, 2pt]{1}⟩.
$$

Therefore, $\frac{b}{c}=2.$

Answer selection: 2

### Finding the Vector Equation of the Plane Perpendicular to a Given Straight Line (17 captured questions)

Question 17592186120224 — question.difficulty/moderate

Find an equation of the plane that passes through the point $Q(2,-3,5)$ and is perpendicular to the line that goes through the points 
$A(3,2,-8)$ and $B(1,2,-5).$

Solution: First, we note that the position vector of $Q$ is $q=⟨2,-3,5⟩.$

Since the line  passes through the points $A(3,2,-8)$ and $B(1,2,-5)$, we can find a vector that is parallel to the line:

$$
\begin{aligned}\overset{\to }{AB} & =⟨1,2,-5⟩-⟨3,2,-8⟩ \\  & =⟨-2,0,3⟩\end{aligned}
$$

 

So, a normal vector to the plane is $n=⟨-2,0,3⟩.$

Therefore, the equation of the plane is given by 

$$
\begin{aligned}(r-q)\cdot n & =0 \\ r\cdot n-q\cdot n & =0 \\ r\cdot n & =q\cdot n \\ r\cdot ⟨-2,0,3⟩ & =⟨2,-3,5⟩\cdot ⟨-2,0,3⟩ \\ r\cdot ⟨-2,0,3⟩ & =11.\end{aligned}
$$

Answer selection: r\cdot ⟨-2,0,3⟩=11

Question 17592186120247 — question.difficulty/hard

Find an equation of the plane that passes through the point $Q(-2,2,0)$ and is perpendicular to the line 

$$
\left\{\begin{aligned}x &=3-4t \\ y &=1+6t \\ z &=-1+2t.\end{aligned}\right.
$$

Solution: Note that the position vector of $Q$ is $\mathbf{q}=⟨-2,2,0⟩.$ Converting the parametric equations of the line to vector form, we get

$$
\left\{\begin{aligned}x &=3-4t \\ y &=1+6t \\ z &=-1+2t\end{aligned}\right.\hspace{2em}⟹\hspace{2em}⟨x,y,z⟩=⟨3,1,-1⟩+t\text{ }\underbrace{⟨-4,6,2⟩}_{\mathbf{v}}.
$$

 

The direction vector of the line is $\mathbf{v}=⟨-4,6,2⟩,$ so a normal vector to the plane is 

$$
\mathbf{n}=\mathbf{v}=⟨-4,6,2⟩.
$$

Therefore, the equation of the plane is given by

$$
\begin{aligned}(\mathbf{r}-\mathbf{q})\cdot \mathbf{n} & =0 \\ \mathbf{r}\cdot \mathbf{n}-\mathbf{q}\cdot \mathbf{n} & =0 \\ \mathbf{r}\cdot \mathbf{n} & =\mathbf{q}\cdot \mathbf{n} \\ \mathbf{r}\cdot ⟨-4,6,2⟩ & =⟨-2,2,0⟩\cdot ⟨-4,6,2⟩ \\ \mathbf{r}\cdot ⟨-4,6,2⟩ & =20.\end{aligned}
$$

Answer selection: r\cdot ⟨-4,6,2⟩=20

Question 17592186262853 — question.difficulty/moderate

Find an equation of the plane that passes through the point $Q(1,-2,3)$ and is perpendicular to the line that goes through the points 
$A(4,1,-3)$ and $B(7,-3,1).$

Solution: First, we note that the position vector of $Q$ is $\mathbf{q}=⟨1,-2,3⟩.$

Since the line  passes through the points $A(4,1,-3)$ and $B(7,-3,1)$, we can find a vector that is parallel to the line:

$$
\begin{aligned}\overset{\to }{AB} & =⟨7,-3,1⟩-⟨4,1,-3⟩ \\  & =⟨3,-4,4⟩\end{aligned}
$$

 

So, a normal vector to the plane is $\mathbf{n}=⟨3,-4,4⟩.$

Therefore, the equation of the plane is given by 

$$
\begin{aligned}(\mathbf{r}-\mathbf{q})\cdot \mathbf{n} & =0 \\ \mathbf{r}\cdot \mathbf{n}-\mathbf{q}\cdot \mathbf{n} & =0 \\ \mathbf{r}\cdot \mathbf{n} & =\mathbf{q}\cdot \mathbf{n} \\ \mathbf{r}\cdot ⟨3,-4,4⟩ & =⟨1,-2,3⟩\cdot ⟨3,-4,4⟩ \\ \mathbf{r}\cdot ⟨3,-4,4⟩ & =23.\end{aligned}
$$

Answer selection: r\cdot ⟨3,-4,4⟩=23
