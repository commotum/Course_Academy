# 17592186050830 The Cartesian Equation of a Plane

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186121050 — Introduction

If we are given an equation of a plane using the dot product, we can always obtain an equation in terms of $x,$ $y,$ and $z.$ For example, suppose we have the plane that passes through the point $P(-7,5,-2)$ and is perpendicular to the vector $\mathbf{n}=\langle 3,-6,5 \rangle.$

First, we note that the position vector of the point $P$ is $\mathbf{p}=\langle -7,5,-2 \rangle,$ and we can write down the equation of the plane using the dot product:

$$
\begin{aligned}(\mathbf{r}-\mathbf{p})\cdot \mathbf{n} & =0 \\ \mathbf{r}\cdot \mathbf{n} & =\mathbf{p}\cdot \mathbf{n} \\ \mathbf{r}\cdot ⟨3,-6,5⟩ & =⟨-7,5,-2⟩\cdot ⟨3,-6,5⟩ \\ \mathbf{r}\cdot ⟨3,-6,5⟩ & =-61\end{aligned}
$$

Now, to obtain the Cartesian equation, we substitute $\mathbf{r}=\langle x,y,z \rangle$ into the equation above and get

$$
\begin{aligned}⟨x,y,z⟩\cdot ⟨3,-6,5⟩ & =-61 \\ 3x-6y+5z & =-61 \\ 3x-6y+5z+61 & =0.\end{aligned}
$$

This final equation is called the **Cartesian equation of the plane**.

![](images/77/77f18981dda500889655225eabbec730b7b295e6b16cec1700d56c2e27e0ac91.png)

Note that in the equation 

$$
{\color{blue}3}x+({\color{blue}-6})y+{\color{blue}5}z+61 = 0,
$$

the coefficients next to $x,$ $y,$ and $z$ are the coordinates of the normal vector 

$$
\mathbf{n}=\langle {\color{blue}3},{\color{blue}-6},{\color{blue}5} \rangle
$$

.



### example 17592186119643 — Finding the Cartesian Equation of the Plane Perpendicular To a Given Vector

Find a Cartesian equation of the plane that passes through the point $P(9,-2,3)$ and is perpendicular to the vector $\mathbf{n}=3\mathbf{i}-4\mathbf{j}+7\mathbf{k}.$

First, we note that the position vector of the point $P$ is $\mathbf{p}=\langle 9,-2,3 \rangle$ and the normal vector of the plane is $\mathbf{n}=\langle 3,-4,7 \rangle.$

Using the dot product, we can find the equation of the plane as follows:

$$
\begin{aligned}(\mathbf{r}-\mathbf{p})\cdot \mathbf{n} & =0 \\ \mathbf{r}\cdot \mathbf{n} & =\mathbf{p}\cdot \mathbf{n} \\ \mathbf{r}\cdot ⟨3,-4,7⟩ & =⟨9,-2,3⟩\cdot ⟨3,-4,7⟩ \\ \mathbf{r}\cdot ⟨3,-4,7⟩ & =56.\end{aligned}
$$

Now, to obtain the Cartesian equation of the plane, we substitute $\mathbf{r}=\langle x,y,z \rangle$ into the equation above and get

$$
\begin{aligned}⟨x,y,z⟩\cdot ⟨3,-4,7⟩ & =56 \\ 3x-4y+7z & =56 \\ 3x-4y+7z-56 & =0.\end{aligned}
$$

### example 17592186119644 — Finding the Cartesian Equation of the Plane Perpendicular To a Given Line

Find a Cartesian equation of the plane that passes through the point $P(-1,4,8)$ and is perpendicular to the line 
$$
\dfrac{x+3}{-5}=\dfrac{y-1}{3}=\dfrac{z+2}{2}.
$$

First, we note that the position vector of $P$ is $\mathbf{p}=\langle -1,4,8 \rangle.$ From the canonical equation, we find that the line is parallel to the vector $\langle -5,3,2 \rangle.$ So, the normal vector of the plane is 

$$
\mathbf{n}=\langle -5,3,2 \rangle.
$$

Using the dot product, we can find the equation of the plane as follows:

$$
\begin{aligned}(\mathbf{r}-\mathbf{p})\cdot \mathbf{n} & =0 \\ \mathbf{r}\cdot \mathbf{n} & =\mathbf{p}\cdot \mathbf{n} \\ \mathbf{r}\cdot ⟨-5,3,2⟩ & =⟨-1,4,8⟩\cdot ⟨-5,3,2⟩ \\ \mathbf{r}\cdot ⟨-5,3,2⟩ & =33\end{aligned}
$$

Now, to obtain the Cartesian equation of the plane, we substitute $\mathbf{r}=\langle x,y,z \rangle$ into the equation above and get

$$
\begin{aligned}⟨x,y,z⟩\cdot ⟨-5,3,2⟩ & =33 \\ -5x+3y+2z & =33 \\ -5x+3y+2z-33 & =0.\end{aligned}
$$

### example 17592186119645 — Finding the Vector Equation of a Plane Given Its Cartesian Equation

Given the Cartesian equation $2x-y+z+13=0$ of the plane $\Pi,$ find an equation of $\Pi$ in the form $(\mathbf{r}-\mathbf{p})\cdot\mathbf{n}=0.$

First, from the coefficients in equation of the plane, we get that the normal vector of $\Pi$ is $\mathbf{n}=\langle 2,-1,1 \rangle.$

Now, we solve the Cartesian equation of $\Pi$ for $z\mathbin{:}$

$$
\begin{aligned}2x-y+z+13 & =0 \\ z & =-2x+y-13\end{aligned}
$$

If we put, say, $x=0$ and $y=0,$ we get $z=-13.$ So, the point $P(0,0,-13)$ lies on $\Pi.$ Note that the position vector of $P$ is $\mathbf{p}=\langle 0,0,-13 \rangle.$

Finally, we obtain

$$
\begin{aligned}(\mathbf{r}-\mathbf{p})\cdot \mathbf{n} & =0 \\ (\mathbf{r}-⟨0,0,-13⟩)\cdot ⟨2,-1,1⟩ & =0.\end{aligned}
$$

### example 17592186119646 — Finding the Cartesian Equation of the Plane Parallel To Two Vectors

Find a Cartesian equation of the plane that passes through the point $P(-3,2,-6)$ and is parallel to the vectors $\mathbf{v_1}=\langle -3, 5, 2 \rangle$ and $\mathbf{v_2}=\langle 1, 3, -2 \rangle.$

First, we note that the position vector of the point $P$ is $\mathbf{p}=\langle -3,2,-6 \rangle.$

Now, we need to find the normal vector of the plane. To do that, we use the cross product of $\mathbf{v_1}$ and $\mathbf{v_2}$ as follows:

$$
\begin{aligned}\mathbf{n} & ={\mathbf{v}}_{\mathbf{1}}\times {\mathbf{v}}_{\mathbf{2}} \\  & =\begin{bmatrix}-3 \\ 5 \\ 2\end{bmatrix}\times \begin{bmatrix}1 \\ 3 \\ -2\end{bmatrix} \\  & =\enclose{left right}{\begin{array}{ccc}\mathbf{i} & \mathbf{j} & \mathbf{k} \\ -3 & 5 & 2 \\ 1 & 3 & -2\end{array}} \\  & =-16\mathbf{i}-4\mathbf{j}-14\mathbf{k} \\  & =⟨-16,-4,-14⟩\end{aligned}
$$

Then, using the dot product, we can find the equation of the plane:

$$
\begin{aligned}(\mathbf{r}-\mathbf{p})\cdot \mathbf{n} & =0 \\ \mathbf{r}\cdot \mathbf{n} & =\mathbf{p}\cdot \mathbf{n} \\ \mathbf{r}\cdot ⟨-16,-4,-14⟩ & =⟨-3,2,-6⟩\cdot ⟨-16,-4,-14⟩ \\ \mathbf{r}\cdot ⟨-16,-4,-14⟩ & =124\end{aligned}
$$

Finally, to obtain the Cartesian equation of the plane, we substitute $\mathbf{r}=\langle x,y,z \rangle$ into the equation above and get

$$
\begin{aligned}⟨x,y,z⟩\cdot ⟨-16,-4,-14⟩ & =124 \\ -16x-4y-14z & =124 \\ -16x-4y-14z-124 & =0 \\ 8x+2y+7z+62 & =0.\end{aligned}
$$

## Representative practice (first three per skill; full bank in practice.json)

### Finding the Cartesian Equation of the Plane Perpendicular To a Given Vector (14 captured questions)

Question 17592186120231 — None

Find a Cartesian equation of the plane that passes through the point $P(3,1,-4)$ and is perpendicular to the vector $\mathbf{n}=\mathbf{i}-2\mathbf{j}+5\mathbf{k}.$.

Solution: The normal vector is $\mathbf{n}=\langle1,-2,5\rangle$ and the plane passes through $P(3,1,-4)$. Use $\mathbf{n}\cdot(\mathbf{r}-\mathbf{p})=0$:

$$
(x-3)-2(y-1)+5(z+4)=0.
$$

Expanding and collecting the constants gives

$$
x-2y+5z+19=0.
$$

Answer selection: x - 2y + 5z + 19 = 0

Question 17592186120285 — None

Find a Cartesian equation of the plane that passes through the point $P(1,0,6)$ and is perpendicular to the vector $\mathbf{n}=⟨1,1,-1⟩.$.

Solution: Use the normal vector $\mathbf{n}=\langle1,1,-1\rangle$ and the point $P(1,0,6)$:

$$
\mathbf{n}\cdot(\mathbf{r}-\mathbf{p})=0\quad\Longrightarrow\quad(x-1)+y-(z-6)=0.
$$

Simplifying gives

$$
x+y-z+5=0.
$$

Answer selection: x + y - z + 5 = 0

Question 17592186262860 — question.difficulty/easy

Find a Cartesian equation of the plane that passes through the point $P(5,2,-1)$ and is perpendicular to the vector $\mathbf{n}=3\mathbf{i}-\mathbf{j}+2\mathbf{k}.$

Solution: First, we note that the position vector of the point $P$ is $\mathbf{p}=⟨5,2,-1⟩$ and the normal vector of the plane is $\mathbf{n}=⟨3,-1,2⟩.$

Using the dot product, we can find the equation of the plane as follows:

$$
\begin{aligned}(\mathbf{r}-\mathbf{p})\cdot \mathbf{n} & =0 \\ \mathbf{r}\cdot \mathbf{n} & =\mathbf{p}\cdot \mathbf{n} \\ \mathbf{r}\cdot ⟨3,-1,2⟩ & =⟨5,2,-1⟩\cdot ⟨3,-1,2⟩ \\ \mathbf{r}\cdot ⟨3,-1,2⟩ & =11.\end{aligned}
$$

Now, to obtain the Cartesian equation of the plane, we substitute $\mathbf{r}=⟨x,y,z⟩$ into the equation above and get

$$
\begin{aligned}⟨x,y,z⟩\cdot ⟨3,-1,2⟩ & =11 \\ 3x-y+2z & =11 \\ 3x-y+2z-11 & =0.\end{aligned}
$$

Answer selection: 3x-y+2z-11=0

### Finding the Cartesian Equation of the Plane Perpendicular To a Given Line (21 captured questions)

Question 17592186120233 — question.difficulty/easy

Find a Cartesian equation of the plane that passes through the point $P(0,2,1)$ and is perpendicular to the line 
$$
\frac{x-1}{-2}=\frac{y-3}{1}=\frac{z}{5}.
$$

Solution: First, we note that the position vector of $P$ is $p=⟨0,2,1⟩.$ From the canonical equation, we find that the line is parallel to the vector $⟨-2,1,5⟩.$ So, the normal vector of the plane is 

$$
n=⟨-2,1,5⟩.
$$

Using the dot product, we can find the equation of the plane as follows:

$$
\begin{aligned}(r-p)\cdot n & =0 \\ r\cdot n & =p\cdot n \\ r\cdot ⟨-2,1,5⟩ & =⟨0,2,1⟩\cdot ⟨-2,1,5⟩ \\ r\cdot ⟨-2,1,5⟩ & =7\end{aligned}
$$

Now, to obtain the Cartesian equation of the plane, we substitute $r=⟨x,y,z⟩$ into the equation above and get

$$
\begin{aligned}⟨x,y,z⟩\cdot ⟨-2,1,5⟩ & =7 \\ -2x+y+5z & =7 \\ -2x+y+5z-7 & =0 \\ 2x-y-5z+7 & =0.\end{aligned}
$$

Answer selection: 2x-y-5z+7=0

Question 17592186120237 — question.difficulty/easy

Find a Cartesian equation of the plane that passes through the point $P(8,3,-1)$ and is perpendicular to the line 
$$
\frac{x+2}{4}=\frac{y-1}{3}=\frac{z-2}{-1}.
$$

Solution: First, we note that the position vector of $P$ is $\mathbf{p}=⟨8,3,-1⟩.$ From the canonical equation, we find that the line is parallel to the vector $⟨4,3,-1⟩.$ So, the normal vector of the plane is 

$$
\mathbf{n}=⟨4,3,-1⟩.
$$

Using the dot product, we can find the equation of the plane as follows:

$$
\begin{aligned}(\mathbf{r}-\mathbf{p})\cdot \mathbf{n} & =0 \\ \mathbf{r}\cdot \mathbf{n} & =\mathbf{p}\cdot \mathbf{n} \\ \mathbf{r}\cdot ⟨4,3,-1⟩ & =⟨8,3,-1⟩\cdot ⟨4,3,-1⟩ \\ \mathbf{r}\cdot ⟨4,3,-1⟩ & =42\end{aligned}
$$

Now, to obtain the Cartesian equation of the plane, we substitute $\mathbf{r}=⟨x,y,z⟩$ into the equation above and get

$$
\begin{aligned}⟨x,y,z⟩\cdot ⟨4,3,-1⟩ & =42 \\ 4x+3y-z & =42 \\ 4x+3y-z-42 & =0.\end{aligned}
$$

Answer selection: 4x+3y-z-42=0

Question 17592186262887 — question.difficulty/moderate

Find a Cartesian equation of the plane that passes through the point $P(3,0,-2)$ and is perpendicular to the line 
$$
\left\{\begin{aligned}x &=7-2t \\ y &=7 \\ z &=7t\end{aligned}\right..
$$

Solution: First, we note that the position vector of $P$ is $\mathbf{p}=⟨3,0,-2⟩.$ From the parametrical equation, we find that the line is parallel to the vector $⟨-2,0,7⟩.$ So, the normal vector of the plane is 

$$
\mathbf{n}=⟨-2,0,7⟩.
$$

Using the dot product, we can find the equation of the plane as follows:

$$
\begin{aligned}(\mathbf{r}-\mathbf{p})\cdot \mathbf{n} & =0 \\ \mathbf{r}\cdot \mathbf{n} & =\mathbf{p}\cdot \mathbf{n} \\ \mathbf{r}\cdot ⟨-2,0,7⟩ & =⟨3,0,-2⟩\cdot ⟨-2,0,7⟩ \\ \mathbf{r}\cdot ⟨-2,0,7⟩ & =-20.\end{aligned}
$$

Now, to obtain the Cartesian equation of the plane, we substitute $\mathbf{r}=⟨x,y,z⟩$ into the equation above. Hence,

$$
\begin{aligned}⟨x,y,z⟩\cdot ⟨-2,0,7⟩ & =-20 \\ -2x+7z & =-20 \\ -2x+7z+20 & =0.\end{aligned}
$$

Answer selection: -2x+7z+20=0

### Finding the Vector Equation of a Plane Given Its Cartesian Equation (18 captured questions)

Question 17592186120282 — None

Given the Cartesian equation $x-3y+z+11=0$ of the plane $\mathrm{Π}$, find an equation of $\mathrm{Π}$ in the form $(\mathbf{r}-\mathbf{p})\cdot \mathbf{n}=0.$.

Solution: The coefficients in the Cartesian equation give a normal vector $\mathbf{n}=\langle1,-3,1\rangle$. Setting $x=y=0$ gives $z=-11$, so $P(0,0,-11)$ lies on the plane. Thus,

$$
(\mathbf{r}-\langle0,0,-11\rangle)\cdot\langle1,-3,1\rangle=0.
$$

Expanding recovers the given equation $x-3y+z+11=0$.

Answer selection: (r - ⟨0, 0,-11⟩) \cdot ⟨1,-3, 1⟩ = 0

Question 17592186120284 — question.difficulty/moderate

Given the Cartesian equation $x-y+4z+16=0$ of the plane $\mathrm{Π}$, find an equation of $\mathrm{Π}$ in the form $(\mathbf{r}-\mathbf{p})\cdot \mathbf{n}=0.$

Solution: First, from the equation of the plane we get that the normal vector of $\mathrm{Π}$ is $\mathbf{n}=⟨1,-1,4⟩.$

Now, we solve the Cartesian equation of $\mathrm{Π}$ for $z$:

$$
\begin{aligned}x-y+4z+16 & =0 \\ z & =-\frac{1}{4}x+\frac{1}{4}y-4.\end{aligned}
$$

If we put, say, $x=0$ and $y=0$, we get $z=-4.$ Hence, the point $P(0,0,-4)$ lies on $\mathrm{Π}.$ Note that the position vector of $P$ is $\mathbf{p}=⟨0,0,-4⟩.$

Finally, we obtain

$$
\begin{aligned}(\mathbf{r}-\mathbf{p})\cdot \mathbf{n} & =0 \\ (\mathbf{r}-⟨0,0,-4⟩)\cdot ⟨1,-1,4⟩ & =0.\end{aligned}
$$

Answer selection: (r-⟨0,0,-4⟩)\cdot ⟨1,-1,4⟩=0

Question 17592186262889 — question.difficulty/moderate

Given the Cartesian equation $4x+4y-2z=0$ of the plane $\mathrm{Π}$, find an equation of $\mathrm{Π}$ in the form $(\mathbf{r}-\mathbf{p})\cdot \mathbf{n}=0.$

Solution: First, from the equation of the plane we get that the normal vector of $\mathrm{Π}$ is $\mathbf{n}=⟨4,4,-2⟩.$

Now, we solve the Cartesian equation of $\mathrm{Π}$ for $z$:

$$
\begin{aligned}4x+4y-2z & =0 \\ 2z & =4x+4y \\ z & =2x+2y.\end{aligned}
$$

If we put, say, $x=0$ and $y=0$, we get $z=0.$ Hence, the point $P(0,0,0)$ lies on $\mathrm{Π}.$ Note that the position vector of $P$ is $\mathbf{p}=⟨0,0,0⟩.$

Finally, we obtain

$$
\begin{aligned}(\mathbf{r}-\mathbf{p})\cdot \mathbf{n} & =0 \\ (\mathbf{r}-⟨0,0,0⟩)\cdot ⟨4,4,-2⟩ & =0.\end{aligned}
$$

Answer selection: (r-⟨0,0,0⟩)\cdot ⟨4,4,-2⟩=0

### Finding the Cartesian Equation of the Plane Parallel To Two Vectors (16 captured questions)

Question 17592186120232 — None

Find a Cartesian equation of the plane that passes through the point $P(-3,2,4)$ and is parallel to the vectors ${\mathbf{v}}_{\mathbf{1}}=⟨1,-2,-5⟩$ and ${\mathbf{v}}_{\mathbf{2}}=⟨0,1,-7⟩.$.

Solution: Take the cross product of the two direction vectors to obtain a normal vector:

$$
\mathbf{n}=\langle1,-2,-5\rangle\times\langle0,1,-7\rangle=\langle19,7,1\rangle.
$$

Using the point $P(-3,2,4)$, we obtain

$$
19(x+3)+7(y-2)+(z-4)=0.
$$

Therefore, a Cartesian equation is

$$
19x+7y+z+39=0.
$$

Answer selection: 19x + 7y + z + 39 = 0

Question 17592186120283 — question.difficulty/moderate

Find a Cartesian equation of the plane that passes through the point $P(1,0,3)$ and is parallel to the vectors ${\mathbf{v}}_{\mathbf{1}}=⟨5,2,1⟩$ and ${\mathbf{v}}_{\mathbf{2}}=⟨0,3,3⟩.$

Solution: First, we note that the position vector of the point $P$ is $\mathbf{p}=⟨1,0,3⟩.$

Now, we need to find the normal vector of the plane. To do that, we use the cross product of ${\mathbf{v}}_{\mathbf{1}}$ and ${\mathbf{v}}_{\mathbf{2}}$ as follows:

$$
\begin{aligned}\mathbf{n} & ={\mathbf{v}}_{\mathbf{1}}\times {\mathbf{v}}_{\mathbf{2}} \\  & =\begin{bmatrix}5 \\ 2 \\ 1\end{bmatrix}\times \begin{bmatrix}0 \\ 3 \\ 3\end{bmatrix} \\  & =\enclose{left right}{\begin{array}{ccc}\mathbf{i} & \mathbf{j} & \mathbf{k} \\ 5 & 2 & 1 \\ 0 & 3 & 3\end{array}} \\  & =3\mathbf{i}-15\mathbf{j}+15\mathbf{k} \\  & =⟨3,-15,15⟩\end{aligned}
$$

Then, using the dot product, we can find the equation of the plane:

$$
\begin{aligned}(\mathbf{r}-\mathbf{p})\cdot \mathbf{n} & =0 \\ \mathbf{r}\cdot \mathbf{n} & =\mathbf{p}\cdot \mathbf{n} \\ \mathbf{r}\cdot ⟨3,-15,15⟩ & =⟨1,0,3⟩\cdot ⟨3,-15,15⟩ \\ \mathbf{r}\cdot ⟨3,-15,15⟩ & =48\end{aligned}
$$

Finally, to obtain the Cartesian equation of the plane, we substitute $\mathbf{r}=⟨x,y,z⟩$ into the equation above and get

$$
\begin{aligned}⟨x,y,z⟩\cdot ⟨3,-15,15⟩ & =48 \\ 3x-15y+15z & =48 \\ 3x-15y+15z-48 & =0 \\ x-5y+5z-16 & =0.\end{aligned}
$$

Answer selection: x-5y+5z-16=0

Question 17592186262901 — question.difficulty/hard

Find a Cartesian equation of the plane that passes through the points $A(1,-2,3)$, $P(3,-1,4)$ and $Q(-1,0,1).$

Solution: Note that the position vectors of the points $A,P$ and $Q$ are $\mathbf{a}=⟨1,-2,3⟩,\hspace{0.167em}\mathbf{p}=⟨3,-1,4⟩,$ and $\mathbf{q}=⟨-1,0,1⟩.$

First, using the $3$ points we build $2$ vectors parallel to the plane:

$$
\begin{aligned}{\mathbf{v}}_{\mathbf{1}} & =\overset{\to }{AP} \\  & =⟨3,-1,4⟩-⟨1,-2,3⟩ \\  & =⟨2,1,1⟩ \\ {\mathbf{v}}_{\mathbf{2}} & =\overset{\to }{AQ} \\  & =⟨-1,0,1⟩-⟨1,-2,3⟩ \\  & =⟨-2,2,-2⟩\end{aligned}
$$

 

Now,  we need to find the normal vector of the plane. To do that, we use the cross product of ${\mathbf{v}}_{\mathbf{1}}$ and ${\mathbf{v}}_{\mathbf{2}}$ as follows:

$$
\begin{aligned}\mathbf{n} & ={\mathbf{v}}_{\mathbf{1}}\times {\mathbf{v}}_{\mathbf{2}} \\  & =\begin{bmatrix}2 \\ 1 \\ 1\end{bmatrix}\times \begin{bmatrix}-2 \\ 2 \\ -2\end{bmatrix} \\  & =\enclose{left right}{\begin{array}{ccc}\mathbf{i} & \mathbf{j} & \mathbf{k} \\ 2 & 1 & 1 \\ -2 & 2 & -2\end{array}} \\  & =-4\mathbf{i}+2\mathbf{j}+6\mathbf{k} \\  & =⟨-4,2,6⟩\end{aligned}
$$

Then, using the dot product, we can find the equation of the plane:

$$
\begin{aligned}(\mathbf{r}-\mathbf{p})\cdot \mathbf{n} & =0 \\ \mathbf{r}\cdot \mathbf{n} & =\mathbf{p}\cdot \mathbf{n} \\ \mathbf{r}\cdot ⟨-4,2,6⟩ & =⟨3,-1,4⟩\cdot ⟨-4,2,6⟩ \\ \mathbf{r}\cdot ⟨-4,2,6⟩ & =10\end{aligned}
$$

Finally, to obtain the Cartesian equation of the plane, we substitute $\mathbf{r}=⟨x,y,z⟩$ into the equation above and get

$$
\begin{aligned}⟨x,y,z⟩\cdot ⟨-4,2,6⟩ & =10 \\ -4x+2y+6z & =10 \\ -4x+2y+6z-10 & =0 \\ 4x-2y-6z+10 & =0.\end{aligned}
$$

Answer selection: 4x-2y-6z+10=0
