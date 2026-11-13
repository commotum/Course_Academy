# 17592186048954 Calculating the Dot Product Using Components

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186060920 — Introduction

Given two vectors $\mathbf{a}$ and $\mathbf{b},$ we know that the dot product can be computed using the formula

$$
\mathbf{a} \cdot \mathbf{b} = |\,\mathbf{a}\,| \cdot |\,\mathbf{b}\,| \cdot \cos\theta,
$$

where $\theta$ is the angle formed between the vectors when their tails are placed at the same point.

However, there is another formula for the dot product that we can use if the two vectors are given in component form. If the components of our two vectors are

$$
\mathbf{a} = \langle {\color{red}a_x},{\color{blue}a_y}, a_z \rangle,
	\qquad
	\mathbf{b} = \langle {\color{red}b_x},{\color{blue}b_y}, b_z \rangle,
$$

then the dot product can be computed by summing up the products of corresponding components:

$$
\mathbf{a} \cdot \mathbf{b} = {\color{red}a_x} \cdot {\color{red}b_x} + {\color{blue}a_y} \cdot  {\color{blue}b_y} + a_z \cdot b_z
$$

For example, if we have two vectors 

$$
\mathbf{a} = \langle {\color{red}3},{\color{blue}-5},2 \rangle,
	\qquad
	\mathbf{b} = \langle {\color{red}4},{\color{blue}6},7 \rangle,
$$

Then we can find the dot product of $\mathbf{a}$ and $\mathbf{b}$ as follows:

$$
\begin{aligned}\mathbf{a}\cdot \mathbf{b} & ={\color{red}3}\cdot {\color{red}4}+({\color{blue}-5})\cdot {\color{blue}6}+2\cdot 7 \\  & =12-30+14 \\  & =-4\end{aligned}
$$

**Note:** The procedure for computing the dot product works for vectors of any number of components. For example,

$$
\begin{aligned}⟨{\color{red}3},{\color{blue}-5}⟩\cdot ⟨{\color{red}4},{\color{blue}6}⟩ & ={\color{red}3}\cdot {\color{red}4}+({\color{blue}-5})\cdot {\color{blue}6} \\  & =12-30 \\  & =-18\end{aligned}
$$

and 

$$
\begin{aligned}⟨{\color{red}3},{\color{blue}-5},2,1⟩\cdot ⟨{\color{red}4},{\color{blue}6},7,9⟩ & ={\color{red}3}\cdot {\color{red}4}+({\color{blue}-5})\cdot {\color{blue}6}+2\cdot 7+1\cdot 9 \\  & =12-30+14+9 \\  & =5.\end{aligned}
$$



### example 17592186059543 — Calculating the Dot Product Using the General Formula

Let $\mathbf{a}=\langle 0,-0.4,11 \rangle$ and $\mathbf{b}=\langle 2,5,2 \rangle.$ Find $\mathbf{a} \cdot \mathbf{b}.$

Summing up the products of corresponding components, we obtain:

$$
\begin{aligned}\mathbf{a}\cdot \mathbf{b} & ={a}_{x}\cdot {b}_{x}+{a}_{y}\cdot {b}_{y}+{a}_{z}\cdot {b}_{z} \\  & =0\cdot 2+(-0.4)\cdot 5+11\cdot 2 \\  & =0-2+22 \\  & =20\end{aligned}
$$

### example 17592186059544 — Solving for an Unknown Given Two Perpendicular Vectors

Let $\mathbf{a} = {\left[ \begin{array}{c}4 \\ - 2 \\ 1\end{array} \right]}$ and $\mathbf{b} = {\left[ \begin{array}{c}- 2 \\ 5 \\ t\end{array} \right]}$. Given that $\mathbf{a} \perp \mathbf{b}$, find the value of $t$.

We know that $\mathbf{a} \perp \mathbf{b}$ ($\mathbf{a}$ and $\mathbf{b}$ are perpendicular) if and only if $\mathbf{a} \cdot \mathbf{b} = 0.$

Computing the dot product, we have

$$
\begin{aligned}\mathbf{a}\cdot \mathbf{b} & ={a}_{x}\cdot {b}_{x}+{a}_{y}\cdot {b}_{y}+{a}_{z}\cdot {b}_{z} \\  & =4\cdot (-2)+(-2)\cdot 5+1\cdot t \\  & =-8-10+t \\  & =t-18.\end{aligned}
$$

Setting the dot product equal to $0,$ we obtain:

$$
\begin{aligned}\mathbf{a}\cdot \mathbf{b} & =0 \\ t-18 & =0 \\ t & =18\end{aligned}
$$

### tutorial 17592186060921 — Intuition Behind the Formula

To understand the reasoning behind the formula for the dot product of two vectors, it's helpful to write the two vectors in terms of their elementary unit vectors and carry out the computation the long way.

For example, suppose we want to find the dot product $\mathbf{a} \cdot \mathbf{b}$ for $\mathbf{a} = \langle 3,-5 \rangle$ and $\mathbf{b}=\langle 4,6 \rangle.$

Expressing the vectors in terms of their elementary unit vectors, we have

$$
\begin{aligned}\mathbf{a} &=3\mathbf{i}-5\mathbf{j},\hspace{2em}\mathbf{b}=4\mathbf{i}+6\mathbf{j}.\end{aligned}
$$

Now, using properties of the dot product we obtain

$$
\begin{aligned}\mathbf{a}\cdot \mathbf{b} & =({\color{red}3}\mathbf{i}+({\color{blue}-5})\mathbf{j})\cdot ({\color{red}4}\mathbf{i}+{\color{blue}6}\mathbf{j}) \\  & =({\color{red}3}\cdot {\color{red}4})\mathbf{i}\cdot \mathbf{i}+({\color{red}3}\cdot {\color{blue}6})\mathbf{i}\cdot \mathbf{j}+({\color{blue}-5}\cdot {\color{red}4})\mathbf{j}\cdot \mathbf{i}+({\color{blue}-5}\cdot {\color{blue}6})\mathbf{j}\cdot \mathbf{j}.\end{aligned}
$$

Remember that $\mathbf{i},\mathbf{j}$ are perpendicular, meaning the angle between them is $\theta=90^\circ$ and consequently their dot product is zero:

$$
\begin{aligned}\mathbf{i}\cdot \mathbf{j} & =|\hspace{0.167em}\mathbf{i}\hspace{0.167em}|\cdot |\hspace{0.167em}\mathbf{j}\hspace{0.167em}|\cdot \operatorname{cos}{90}^{∘} \\  & =1\cdot 1\cdot 0 \\  & =0\end{aligned}
$$

On the other hand, since the angle between a vector and itself is $\theta=0,$ we have

$$
\begin{aligned}\mathbf{i}\cdot \mathbf{i} & =|\hspace{0.167em}\mathbf{i}\hspace{0.167em}|\cdot |\hspace{0.167em}\mathbf{i}\hspace{0.167em}|\cdot \operatorname{cos}{0}^{∘} \\  & =1\cdot 1\cdot 1 \\  & =1\end{aligned}
$$

and

$$
\begin{aligned}\mathbf{j}\cdot \mathbf{j} & =|\hspace{0.167em}\mathbf{j}\hspace{0.167em}|\cdot |\hspace{0.167em}\mathbf{j}\hspace{0.167em}|\cdot \operatorname{cos}{0}^{∘} \\  & =1\cdot 1\cdot 1 \\  & =1.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}i\cdot j & =j\cdot i=0, \\ i\cdot i & =j\cdot j=1,\end{aligned}
$$

and our computation reduces to

$$
\begin{aligned}\mathbf{a}\cdot \mathbf{b} & =({\color{red}3}\cdot {\color{red}4})\overbrace{\mathbf{i}\cdot \mathbf{i}}^{=1}+({\color{red}3}\cdot {\color{blue}6})\overbrace{\mathbf{i}\cdot \mathbf{j}}^{=0}+({\color{blue}-5}\cdot {\color{red}4})\overbrace{\mathbf{j}\cdot \mathbf{i}}^{=0}+({\color{blue}-5}\cdot {\color{blue}6})\overbrace{\mathbf{j}\cdot \mathbf{j}}^{=1} \\  & =({\color{red}3}\cdot {\color{red}4})\cdot 1+({\color{red}3}\cdot {\color{blue}6})\cdot 0+({\color{blue}-5}\cdot {\color{red}4})\cdot 0+({\color{blue}-5}\cdot {\color{blue}6})\cdot 1 \\  & =({\color{red}3}\cdot {\color{red}4})+({\color{blue}-5}\cdot {\color{blue}6}).\end{aligned}
$$

So, we have that

$$
\begin{aligned}\mathbf{a}\cdot \mathbf{b} & =⟨{\color{red}3},{\color{blue}-5}⟩\cdot ⟨{\color{red}4},{\color{blue}6}⟩ \\  & =({\color{red}3}\cdot {\color{red}4})+({\color{blue}-5}\cdot {\color{blue}6}).\end{aligned}
$$



## Representative practice (first three per skill; full bank in practice.json)

### Calculating the Dot Product Using the General Formula (29 captured questions)

Question 17592186060030 — question.difficulty/easy

Let $\mathbf{u}=⟨-3,2⟩$ and $\mathbf{v}=⟨7,9⟩.$ Find $\mathbf{u}\cdot \mathbf{v}.$

Solution: Summing up the products of corresponding components, we obtain:

$$
\begin{aligned}\mathbf{u}\cdot \mathbf{v} & ={u}_{x}\cdot {v}_{x}+{u}_{y}\cdot {v}_{y} \\  & =(-3)\cdot 7+2\cdot 9 \\  & =-21+18 \\  & =-3\end{aligned}
$$

Answer selection: -3

Question 17592186060031 — None

If $a = ⟨ - 1, 0, 6⟩$ and $b = ⟨10, 2,-5⟩$, then $a \cdot b =$

Solution: Multiply corresponding components and add:

$$
a\cdot b=(-1)(10)+(0)(2)+(6)(-5)=-10-30=-40.
$$

Answer selection: -40

Question 17592186235513 — question.difficulty/easy

An ambulance service helicopter takes off from a hospital helipad three times on a particular day. The helicopter's location a few seconds after these takeoffs are given by points $P,$ $Q,$ and $R.$

Find the dot product of the vectors $\mathbf{q}$ and $\mathbf{r}.$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
$\mathbf{q}\cdot \mathbf{r}=\hspace{0.167em}$

                                    
                                
                                    
                            
{{field-1}}

Solution: The dot product of two vectors given in component form can be computed by summing up the products of corresponding components of vectors:

$$
\begin{aligned}\mathbf{q}\cdot \mathbf{r} & ={q}_{x}\cdot {r}_{x}+{q}_{y}\cdot {r}_{y}+{q}_{z}\cdot {r}_{z}\end{aligned}
$$

From part 1, we have $\mathbf{q}=⟨0,-3,2⟩$ and $\mathbf{r}=⟨0,4,3⟩.$ Therefore, the formula for the dot product gives

$$
\begin{aligned}\mathbf{q}\cdot \mathbf{r} & =0\cdot 0+(-3)\cdot 4+2\cdot 3 \\  & =0-12+6 \\  & =-6.\end{aligned}
$$

Answer field-1: -6

### Solving for an Unknown Given Two Perpendicular Vectors (26 captured questions)

Question 17592186060184 — None

Let $u = \begin{bmatrix}x \\ -2\end{bmatrix}$ and $v = \begin{bmatrix}x \\ 2\end{bmatrix}$. Given that $u⊥v$ and $x > 0$, find the value of $x$.

Solution: Perpendicular vectors have dot product zero. Thus

$$
u\cdot v=x^2+(-2)(2)=x^2-4=0.
$$

The roots are $x=\pm2$. Since $x>0$, the required value is $x=2$.

Answer selection: 2

Question 17592186060185 — None

What is the value of $x$ given that $a = ⟨x,-6x, 3⟩, b = ⟨x, 1, 3⟩$ and $a⊥b$?

Solution: Since $a\perp b$, their dot product is zero:

$$
a\cdot b=x^2-6x+9=(x-3)^2=0.
$$

Therefore $x=3$.

Answer selection: 3

Question 17592186237827 — question.difficulty/moderate

Let $\mathbf{u}=\begin{bmatrix}9 \\ 2x\end{bmatrix}$ and $\mathbf{v}=\begin{bmatrix}-2 \\ x\end{bmatrix}.$ Given that $\mathbf{u}⊥\mathbf{v}$ and $x<0$, find the value of $x.$

Solution: We know that $\mathbf{u}⊥\mathbf{v}$ ($\mathbf{u}$ and $\mathbf{v}$ are perpendicular) if and only if $\mathbf{u}\cdot \mathbf{v}=0.$

Computing the dot product, we have

$$
\begin{aligned}\mathbf{u}\cdot \mathbf{v} & ={u}_{x}\cdot {v}_{x}+{u}_{y}\cdot {v}_{y} \\  & =9\cdot (-2)+2x\cdot x \\  & =-18+2{x}^{2}.\end{aligned}
$$

Setting the dot product equal to $0,$ we obtain:

$$
\begin{aligned}\mathbf{u}\cdot \mathbf{v} & =0 \\ -18+2{x}^{2} & =0 \\ 2{x}^{2} & =18 \\ {x}^{2} & =9 \\ x & =\pm 3\end{aligned}
$$

We disregard the positive solution since we are told that $x<0.$ Therefore, $x=-3.$

Answer selection: -3
