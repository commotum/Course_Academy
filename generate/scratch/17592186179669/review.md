![](images/0e/0e4a78829ce8d1135d46dda1db59c968c0306937d9c5a45b24fa41648a679ea4.png)

The path ${C}_{1}$ consists of a line segment from the point $O(0,0)$ to the point $A(2,0),$ and the path ${C}_{2}$ consists of a line segment from the point $A(2,0)$ to the point $B(1,1).$

Given that ${\int }_{{C}_{1}}F\cdot \text{d}r=2,$ evaluate ${\int }_{C}F\cdot \text{d}r,$ where $F(x,y)=(x+y)\,i+(x-y)\,j,$ and $C={C}_{1}\cup {C}_{2}.$

2
1
3
4
6

We will use the fact that

$$
{\int }_{C}F\cdot \text{d}r={\int }_{{C}_{1}}F\cdot \text{d}r+{\int }_{{C}_{2}}F\cdot \text{d}r.
$$

We're given the value of the first integral, so we only need to work out the second.

The path ${C}_{2}$ is the line segment from $A$ to $B.$ It can be parametrized as

$$
\begin{aligned}{r}_{2}(t) & =a+t(b-a) \\  & =⟨2,0⟩+t(⟨1,1⟩-⟨2,0⟩) \\  & =⟨2-t,t⟩ \\  & =(2-t)\,i+t\,j,\end{aligned}
$$

where $0<t<1.$ Along this segment, we have $x=2-t$ and $y=t.$ Therefore, 

$$
\begin{aligned}F({r}_{2}(t)) & =(x+y)\,i+(x-y)\,j \\  & =(2-t+t)\,i+(2-t-t)\,j \\  & =2\,i+(2-2t)\,j.\end{aligned}
$$

Computing the derivative, we get the following:

$$
\begin{aligned}{r}_{2}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2-t)i+\frac{\text{d}}{\text{d}t}(t)j \\  & =-i+j\end{aligned}
$$

We can now compute the dot product:

$$
\begin{aligned}F({r}_{2}(t))\cdot {r}_{2}^{′}(t) & =(2\,i+(2-2t)\,j)\cdot (-i+j) \\  & =-2+(2-2t) \\  & =-2t\end{aligned}
$$

Finally, we can evaluate the integral, as follows: 

$$
\begin{aligned}{\int }_{C}F\cdot \text{d}r & ={\int }_{{C}_{1}}F\cdot \text{d}r+{\int }_{{C}_{2}}F\cdot \text{d}r \\  & =2+{\int }_{0}^{1}F({r}_{2}(t))\cdot {r}_{2}^{′}(t)\,\text{d}t \\  & =2+{\int }_{0}^{1}(-2t)\,\text{d}t \\  & =2-{t}^{2}{|}_{0}^{1} \\  & =2-(1-0) \\  & =1\end{aligned}
$$

---

![](images/0e/0e4a78829ce8d1135d46dda1db59c968c0306937d9c5a45b24fa41648a679ea4.png)

The path ${C}_{1}$ consists of a line segment from the point $O(0,0)$ to the point $A(2,0),$ and the path ${C}_{2}$ consists of a line segment from the point $A(2,0)$ to the point $B(1,1).$

Given that ${\int }_{{C}_{1}}F\cdot \text{d}r=-4,$ evaluate ${\int }_{C}F\cdot \text{d}r,$ where $F(x,y)=(- 2 x - 2 y)\,i+(- 2 x + 2 y)\,j,$ and $C={C}_{1}\cup {C}_{2}.$

-4
-2
-6
-8
-12

We will use the fact that

$$\int_C F\cdot\mathrm{d}r=\int_{C_1}F\cdot\mathrm{d}r+\int_{C_2}F\cdot\mathrm{d}r.$$

We're given the value of the first integral, so we only need to work out the second.

The path $C_2$ can be parametrized as

$$r_2(t)=(2 - t)\,i+(t)\,j,$$

with $t$ running from $0$ to $1$. Along this path, $x=2 - t$ and $y=t$. Therefore,

$$F(r_2(t))=(-4)\,i+(4 t - 4)\,j.$$

Computing the derivative, we get

$$r_2'(t)=(-1)\,i+(1)\,j.$$

We can now compute the dot product:

$$F(r_2(t))\cdot r_2'(t)=(-4)(-1)+(4 t - 4)(1)=4 t.$$

Finally, we can evaluate the integral, as follows:

$$\int_{C_2}F\cdot\mathrm{d}r=\int_{0}^{1}(4 t)\,\mathrm{d}t=\left[2 t^{2}\right]_{0}^{1}=2.$$

$$\int_C F\cdot\mathrm{d}r=(-4)+(2)=-2.$$

---

![](images/0e/0e4a78829ce8d1135d46dda1db59c968c0306937d9c5a45b24fa41648a679ea4.png)

The path ${C}_{1}$ consists of a line segment from the point $O(0,0)$ to the point $A(2,0),$ and the path ${C}_{2}$ consists of a line segment from the point $A(2,0)$ to the point $B(1,1).$

Given that ${\int }_{{C}_{1}}F\cdot \text{d}r=6,$ evaluate ${\int }_{C}F\cdot \text{d}r,$ where $F(x,y)=(3 x + 3 y)\,i+(3 x - 3 y)\,j,$ and $C={C}_{1}\cup {C}_{2}.$

6
3
9
12
18

We will use the fact that

$$\int_C F\cdot\mathrm{d}r=\int_{C_1}F\cdot\mathrm{d}r+\int_{C_2}F\cdot\mathrm{d}r.$$

We're given the value of the first integral, so we only need to work out the second.

The path $C_2$ can be parametrized as

$$r_2(t)=(2 - t)\,i+(t)\,j,$$

with $t$ running from $0$ to $1$. Along this path, $x=2 - t$ and $y=t$. Therefore,

$$F(r_2(t))=(6)\,i+(6 - 6 t)\,j.$$

Computing the derivative, we get

$$r_2'(t)=(-1)\,i+(1)\,j.$$

We can now compute the dot product:

$$F(r_2(t))\cdot r_2'(t)=(6)(-1)+(6 - 6 t)(1)=- 6 t.$$

Finally, we can evaluate the integral, as follows:

$$\int_{C_2}F\cdot\mathrm{d}r=\int_{0}^{1}(- 6 t)\,\mathrm{d}t=\left[- 3 t^{2}\right]_{0}^{1}=-3.$$

$$\int_C F\cdot\mathrm{d}r=(6)+(-3)=3.$$

---

![](images/60/6087da076e65bda5240c428ff67c570ad59ae9a8e5a5a3c9e8406184998de56a.png)

The path ${C}_{1}$ consists of a the line segment from the point $O(0,0)$ to the point $A(1,0),$ and the path ${C}_{2}$ consists of a line segment from the point $A(1,0)$ to the point $B(0,-2).$

Given that ${\int }_{{C}_{2}}F\cdot \text{d}r=\frac{7}{3},$ evaluate ${\int }_{C}F\cdot \text{d}r,$ where $F(x,y)=({x}^{2}+y)\,i+(x-{y}^{2})\,j,$ and $C={C}_{1}\cup {C}_{2}.$

\frac{8}{3}
\frac{8}{5}
\frac{5}{2}
2
5

We will use the fact that

$$
{\int }_{C}F\cdot \text{d}r={\int }_{{C}_{1}}F\cdot \text{d}r+{\int }_{{C}_{2}}F\cdot \text{d}r.
$$

We're given the value of the second integral, so we only need to work out the first.

The path ${C}_{1}$ is the horizontal line segment from $O$ to $A.$ It can be parametrized as

$$
\begin{aligned}{r}_{1}(t) & =0+t(a-0) \\  & =⟨0,0⟩+t(⟨1,0⟩-⟨0,0⟩) \\  & =⟨t,0⟩ \\  & =t\,i,\end{aligned}
$$

where $0<t<1.$ Along this segment, we have $x=t$ and $y=0.$ Therefore, 

$$
\begin{aligned}F({r}_{1}(t)) & =({x}^{2}+y)\,i+(x-{y}^{2})\,j \\  & =({t}^{2}+0)\,i+(t-{0}^{2})\,j \\  & ={t}^{2}\,i+t\,j.\end{aligned}
$$

Computing the derivative, we get the following:

$$
\begin{aligned}{r}_{1}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(0)j \\  & =i\end{aligned}
$$

We can now compute the dot product:

$$
\begin{aligned}F({r}_{1}(t))\cdot {r}_{1}^{′}(t) & =({t}^{2}\,i+t\,j)\cdot (i) \\  & ={t}^{2}\end{aligned}
$$

Finally, we can evaluate the integral, as follows: 

$$
\begin{aligned}{\int }_{C}F\cdot \text{d}r & ={\int }_{{C}_{1}}F\cdot \text{d}r+{\int }_{{C}_{2}}F\cdot \text{d}r \\  & ={\int }_{0}^{1}F({r}_{1}(t))\cdot {r}_{1}^{′}(t)\,\text{d}t+\frac{7}{3} \\  & ={\int }_{0}^{1}{t}^{2}\,\text{d}t+\frac{7}{3} \\  & =\frac{1}{3}{t}^{3}\,{|}_{0}^{1}+\frac{7}{3} \\  & =(\frac{1}{3}-0)+\frac{7}{3} \\  & =\frac{1}{3}+\frac{7}{3} \\  & =\frac{8}{3}\end{aligned}
$$

---

![](images/60/6087da076e65bda5240c428ff67c570ad59ae9a8e5a5a3c9e8406184998de56a.png)

The path ${C}_{1}$ consists of a the line segment from the point $O(0,0)$ to the point $A(1,0),$ and the path ${C}_{2}$ consists of a line segment from the point $A(1,0)$ to the point $B(0,-2).$

Given that ${\int }_{{C}_{2}}F\cdot \text{d}r=- \frac{14}{3},$ evaluate ${\int }_{C}F\cdot \text{d}r,$ where $F(x,y)=(- 2 x^{2} - 2 y)\,i+(- 2 x + 2 y^{2})\,j,$ and $C={C}_{1}\cup {C}_{2}.$

- \frac{16}{3}
- \frac{16}{5}
-5
-4
-10

We will use the fact that

$$\int_C F\cdot\mathrm{d}r=\int_{C_1}F\cdot\mathrm{d}r+\int_{C_2}F\cdot\mathrm{d}r.$$

We're given the value of the second integral, so we only need to work out the first.

The path $C_1$ can be parametrized as

$$r_1(t)=(t)\,i+(0)\,j,$$

with $t$ running from $0$ to $1$. Along this path, $x=t$ and $y=0$. Therefore,

$$F(r_1(t))=(- 2 t^{2})\,i+(- 2 t)\,j.$$

Computing the derivative, we get

$$r_1'(t)=(1)\,i+(0)\,j.$$

We can now compute the dot product:

$$F(r_1(t))\cdot r_1'(t)=(- 2 t^{2})(1)+(- 2 t)(0)=- 2 t^{2}.$$

Finally, we can evaluate the integral, as follows:

$$\int_{C_1}F\cdot\mathrm{d}r=\int_{0}^{1}(- 2 t^{2})\,\mathrm{d}t=\left[- \frac{2 t^{3}}{3}\right]_{0}^{1}=- \frac{2}{3}.$$

$$\int_C F\cdot\mathrm{d}r=(- \frac{2}{3})+(- \frac{14}{3})=- \frac{16}{3}.$$

---

![](images/60/6087da076e65bda5240c428ff67c570ad59ae9a8e5a5a3c9e8406184998de56a.png)

The path ${C}_{1}$ consists of a the line segment from the point $O(0,0)$ to the point $A(1,0),$ and the path ${C}_{2}$ consists of a line segment from the point $A(1,0)$ to the point $B(0,-2).$

Given that ${\int }_{{C}_{2}}F\cdot \text{d}r=7,$ evaluate ${\int }_{C}F\cdot \text{d}r,$ where $F(x,y)=(3 x^{2} + 3 y)\,i+(3 x - 3 y^{2})\,j,$ and $C={C}_{1}\cup {C}_{2}.$

8
\frac{24}{5}
\frac{15}{2}
6
15

We will use the fact that

$$\int_C F\cdot\mathrm{d}r=\int_{C_1}F\cdot\mathrm{d}r+\int_{C_2}F\cdot\mathrm{d}r.$$

We're given the value of the second integral, so we only need to work out the first.

The path $C_1$ can be parametrized as

$$r_1(t)=(t)\,i+(0)\,j,$$

with $t$ running from $0$ to $1$. Along this path, $x=t$ and $y=0$. Therefore,

$$F(r_1(t))=(3 t^{2})\,i+(3 t)\,j.$$

Computing the derivative, we get

$$r_1'(t)=(1)\,i+(0)\,j.$$

We can now compute the dot product:

$$F(r_1(t))\cdot r_1'(t)=(3 t^{2})(1)+(3 t)(0)=3 t^{2}.$$

Finally, we can evaluate the integral, as follows:

$$\int_{C_1}F\cdot\mathrm{d}r=\int_{0}^{1}(3 t^{2})\,\mathrm{d}t=\left[t^{3}\right]_{0}^{1}=1.$$

$$\int_C F\cdot\mathrm{d}r=(1)+(7)=8.$$

---

![](images/b4/b4ce481ac8babb7a3e5707f1ef44417b12e73abe4b4c2143c19b45332642c6d2.png)

The path ${C}_{1}$ consists of a line segment  from the point $B(0,8)$ to the point $A(-2,8),$ and the path ${C}_{2}$ consists of a section of the curve $y=-{x}^{3}$ from the point $A(-2,8)$ to the point $O(0,0).$

Given that ${\int }_{{C}_{1}}F\cdot \text{d}r=16,$ evaluate ${\int }_{C}F\cdot \text{d}r,$ where $F(x,y)=xy\,i+y\,j$ and $C={C}_{1}\cup {C}_{2}.$

-\frac{51}{5}
-\frac{112}{5}
\frac{32}{5}
-\frac{23}{5}
\frac{8}{5}

We will use the fact that

$$
{\int }_{C}F\cdot \text{d}r={\int }_{{C}_{1}}F\cdot \text{d}r+{\int }_{{C}_{2}}F\cdot \text{d}r.
$$

We're given the value of the first integral, so we only need to work out the second.

The path ${C}_{2}$ is the section of the curve $y=-{x}^{3}$ from $A$ to $O.$ It can be parametrized as

$$
\begin{aligned}{r}_{2}(t)=t\,i-{t}^{3}\,j,\end{aligned}
$$

where $-2\le t\le 0.$ Along this curve, we have $x=t$ and $y=-{t}^{3}.$ Therefore, 

$$
\begin{aligned}F({r}_{2}(t)) & =xy\,i+y\,j \\  & =-{t}^{4}\,i-{t}^{3}\,j.\end{aligned}
$$

Computing the derivative, we get the following:

$$
\begin{aligned}{r}_{2}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(-{t}^{3})j \\  & =i-3{t}^{2}\,j\end{aligned}
$$

We can now compute the dot product:

$$
\begin{aligned}F({r}_{2}(t))\cdot {r}_{2}^{′}(t) & =(-{t}^{4}\,i-{t}^{3}\,j)\cdot (i-3{t}^{2}\,j) \\  & =-{t}^{4}+3{t}^{5}\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F\cdot \text{d}r & ={\int }_{{C}_{1}}F\cdot \text{d}r+{\int }_{{C}_{2}}F\cdot \text{d}r \\  & =16+{\int }_{-2}^{0}F({r}_{2}(t))\cdot {r}_{2}^{′}(t)\,\text{d}t \\  & =16+{\int }_{-2}^{0}(-{t}^{4}+3{t}^{5})\,\text{d}t \\  & =16+{[-\frac{1}{5}{t}^{5}+\frac{1}{2}{t}^{6}]}_{-2}^{0} \\  & =16+[0-(-\frac{(-{2}^{5})}{5}+\frac{(-2)^{6}}{2})] \\  & =16-\frac{192}{5} \\  & =-\frac{112}{5}\end{aligned}
$$

---

![](images/b4/b4ce481ac8babb7a3e5707f1ef44417b12e73abe4b4c2143c19b45332642c6d2.png)

The path ${C}_{1}$ consists of a line segment  from the point $B(0,8)$ to the point $A(-2,8),$ and the path ${C}_{2}$ consists of a section of the curve $y=-{x}^{3}$ from the point $A(-2,8)$ to the point $O(0,0).$

Given that ${\int }_{{C}_{1}}F\cdot \text{d}r=-32,$ evaluate ${\int }_{C}F\cdot \text{d}r,$ where $F(x,y)=(- 2 x y)\,i+(- 2 y)\,j$ and $C={C}_{1}\cup {C}_{2}.$

\frac{102}{5}
\frac{224}{5}
- \frac{64}{5}
\frac{46}{5}
- \frac{16}{5}

We will use the fact that

$$\int_C F\cdot\mathrm{d}r=\int_{C_1}F\cdot\mathrm{d}r+\int_{C_2}F\cdot\mathrm{d}r.$$

We're given the value of the first integral, so we only need to work out the second.

The path $C_2$ can be parametrized as

$$r_2(t)=(t)\,i+(- t^{3})\,j,$$

with $t$ running from $-2$ to $0$. Along this path, $x=t$ and $y=- t^{3}$. Therefore,

$$F(r_2(t))=(2 t^{4})\,i+(2 t^{3})\,j.$$

Computing the derivative, we get

$$r_2'(t)=(1)\,i+(- 3 t^{2})\,j.$$

We can now compute the dot product:

$$F(r_2(t))\cdot r_2'(t)=(2 t^{4})(1)+(2 t^{3})(- 3 t^{2})=- 6 t^{5} + 2 t^{4}.$$

Finally, we can evaluate the integral, as follows:

$$\int_{C_2}F\cdot\mathrm{d}r=\int_{-2}^{0}(- 6 t^{5} + 2 t^{4})\,\mathrm{d}t=\left[- t^{6} + \frac{2 t^{5}}{5}\right]_{-2}^{0}=\frac{384}{5}.$$

$$\int_C F\cdot\mathrm{d}r=(-32)+(\frac{384}{5})=\frac{224}{5}.$$

---

![](images/b4/b4ce481ac8babb7a3e5707f1ef44417b12e73abe4b4c2143c19b45332642c6d2.png)

The path ${C}_{1}$ consists of a line segment  from the point $B(0,8)$ to the point $A(-2,8),$ and the path ${C}_{2}$ consists of a section of the curve $y=-{x}^{3}$ from the point $A(-2,8)$ to the point $O(0,0).$

Given that ${\int }_{{C}_{1}}F\cdot \text{d}r=48,$ evaluate ${\int }_{C}F\cdot \text{d}r,$ where $F(x,y)=(3 x y)\,i+(3 y)\,j$ and $C={C}_{1}\cup {C}_{2}.$

- \frac{153}{5}
- \frac{336}{5}
\frac{96}{5}
- \frac{69}{5}
\frac{24}{5}

We will use the fact that

$$\int_C F\cdot\mathrm{d}r=\int_{C_1}F\cdot\mathrm{d}r+\int_{C_2}F\cdot\mathrm{d}r.$$

We're given the value of the first integral, so we only need to work out the second.

The path $C_2$ can be parametrized as

$$r_2(t)=(t)\,i+(- t^{3})\,j,$$

with $t$ running from $-2$ to $0$. Along this path, $x=t$ and $y=- t^{3}$. Therefore,

$$F(r_2(t))=(- 3 t^{4})\,i+(- 3 t^{3})\,j.$$

Computing the derivative, we get

$$r_2'(t)=(1)\,i+(- 3 t^{2})\,j.$$

We can now compute the dot product:

$$F(r_2(t))\cdot r_2'(t)=(- 3 t^{4})(1)+(- 3 t^{3})(- 3 t^{2})=9 t^{5} - 3 t^{4}.$$

Finally, we can evaluate the integral, as follows:

$$\int_{C_2}F\cdot\mathrm{d}r=\int_{-2}^{0}(9 t^{5} - 3 t^{4})\,\mathrm{d}t=\left[\frac{3 t^{6}}{2} - \frac{3 t^{5}}{5}\right]_{-2}^{0}=- \frac{576}{5}.$$

$$\int_C F\cdot\mathrm{d}r=(48)+(- \frac{576}{5})=- \frac{336}{5}.$$

---

![](images/4d/4d4c2c86ed8506ff034141ac20a5a56587a80370384ceeaf08c66f2ce3e8a315.png)

The path ${C}_{1}$ consists of a section of the parabola $y=-\sqrt{x}$ from the point $O(0,0)$ to the point $A(4,-2),$ and the path ${C}_{2}$ consists of a line segment from the point $A(4,-2)$ to the point $B(4,0).$

Given that ${\int }_{{C}_{2}}F\cdot \text{d}r=\frac{8}{3},$ evaluate ${\int }_{C}F\cdot \text{d}r,$ where $F(x,y)=x\,i+{y}^{2}\,j$ and $C={C}_{1}\cup {C}_{2}.$

32
8
5
4
16

We will use the fact that

$$
{\int }_{C}F\cdot \text{d}r={\int }_{{C}_{1}}F\cdot \text{d}r+{\int }_{{C}_{2}}F\cdot \text{d}r.
$$

We're given the value of the second integral, so we only need to work out the first.

The path ${C}_{1}$ is the section of the curve $y=-\sqrt{x}$ from $O$ to $A.$ It can be parametrized as

$$
\begin{aligned}{r}_{1}(t)=t\,i-\sqrt{t}\,j,\end{aligned}
$$

where $0\le t\le 4.$ Along this curve, we have $x=t$ and $y=-\sqrt{t}.$ Therefore, 

$$
\begin{aligned}F({r}_{1}(t)) & =x\,i+{y}^{2}\,j \\  & =t\,i+t\,j.\end{aligned}
$$

Computing the derivative, we get the following:

$$
\begin{aligned}{r}_{1}^{′}(t) & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(-\sqrt{t})j \\  & =i-\frac{1}{2\sqrt{t}}\,j\end{aligned}
$$

We can now compute the dot product:

$$
\begin{aligned}F({r}_{1}(t))\cdot {r}_{1}^{′}(t) & =(t\,i+t\,j)\cdot (i-\frac{1}{2\sqrt{t}}\,j) \\  & =t-\frac{\sqrt{t}}{2}\end{aligned}
$$

Finally, we can evaluate the integral, as follows:

$$
\begin{aligned}{\int }_{C}F\cdot \text{d}r & ={\int }_{{C}_{1}}F\cdot \text{d}r+{\int }_{{C}_{2}}F\cdot \text{d}r \\  & ={\int }_{0}^{4}F({r}_{1}(t))\cdot {r}_{1}^{′}(t)\,\text{d}t+\frac{8}{3} \\  & ={\int }_{0}^{4}(t-\frac{\sqrt{t}}{2})\text{d}t+\frac{8}{3} \\  & ={[\frac{{t}^{2}}{2}-\frac{{t}^{3/2}}{3}]}_{0}^{4}+\frac{8}{3} \\  & =(\frac{{4}^{2}}{2}-\frac{{4}^{3/2}}{3}-0)+\frac{8}{3} \\  & =\frac{16}{3}+\frac{8}{3} \\  & =8\end{aligned}
$$

---

![](images/4d/4d4c2c86ed8506ff034141ac20a5a56587a80370384ceeaf08c66f2ce3e8a315.png)

The path ${C}_{1}$ consists of a section of the parabola $y=-\sqrt{x}$ from the point $O(0,0)$ to the point $A(4,-2),$ and the path ${C}_{2}$ consists of a line segment from the point $A(4,-2)$ to the point $B(4,0).$

Given that ${\int }_{{C}_{2}}F\cdot \text{d}r=- \frac{16}{3},$ evaluate ${\int }_{C}F\cdot \text{d}r,$ where $F(x,y)=(- 2 x)\,i+(- 2 y^{2})\,j$ and $C={C}_{1}\cup {C}_{2}.$

-64
-16
-10
-8
-32

We will use the fact that

$$\int_C F\cdot\mathrm{d}r=\int_{C_1}F\cdot\mathrm{d}r+\int_{C_2}F\cdot\mathrm{d}r.$$

We're given the value of the second integral, so we only need to work out the first.

The path $C_1$ can be parametrized as

$$r_1(t)=(t)\,i+(- \sqrt{t})\,j,$$

with $t$ running from $0$ to $4$. Along this path, $x=t$ and $y=- \sqrt{t}$. Therefore,

$$F(r_1(t))=(- 2 t)\,i+(- 2 t)\,j.$$

Computing the derivative, we get

$$r_1'(t)=(1)\,i+(- \frac{1}{2 \sqrt{t}})\,j.$$

We can now compute the dot product:

$$F(r_1(t))\cdot r_1'(t)=(- 2 t)(1)+(- 2 t)(- \frac{1}{2 \sqrt{t}})=\sqrt{t} - 2 t.$$

Finally, we can evaluate the integral, as follows:

$$\int_{C_1}F\cdot\mathrm{d}r=\int_{0}^{4}(\sqrt{t} - 2 t)\,\mathrm{d}t=\left[\frac{2 t^{\frac{3}{2}}}{3} - t^{2}\right]_{0}^{4}=- \frac{32}{3}.$$

$$\int_C F\cdot\mathrm{d}r=(- \frac{32}{3})+(- \frac{16}{3})=-16.$$

---

![](images/4d/4d4c2c86ed8506ff034141ac20a5a56587a80370384ceeaf08c66f2ce3e8a315.png)

The path ${C}_{1}$ consists of a section of the parabola $y=-\sqrt{x}$ from the point $O(0,0)$ to the point $A(4,-2),$ and the path ${C}_{2}$ consists of a line segment from the point $A(4,-2)$ to the point $B(4,0).$

Given that ${\int }_{{C}_{2}}F\cdot \text{d}r=8,$ evaluate ${\int }_{C}F\cdot \text{d}r,$ where $F(x,y)=(3 x)\,i+(3 y^{2})\,j$ and $C={C}_{1}\cup {C}_{2}.$

96
24
15
12
48

We will use the fact that

$$\int_C F\cdot\mathrm{d}r=\int_{C_1}F\cdot\mathrm{d}r+\int_{C_2}F\cdot\mathrm{d}r.$$

We're given the value of the second integral, so we only need to work out the first.

The path $C_1$ can be parametrized as

$$r_1(t)=(t)\,i+(- \sqrt{t})\,j,$$

with $t$ running from $0$ to $4$. Along this path, $x=t$ and $y=- \sqrt{t}$. Therefore,

$$F(r_1(t))=(3 t)\,i+(3 t)\,j.$$

Computing the derivative, we get

$$r_1'(t)=(1)\,i+(- \frac{1}{2 \sqrt{t}})\,j.$$

We can now compute the dot product:

$$F(r_1(t))\cdot r_1'(t)=(3 t)(1)+(3 t)(- \frac{1}{2 \sqrt{t}})=- \frac{3 \sqrt{t}}{2} + 3 t.$$

Finally, we can evaluate the integral, as follows:

$$\int_{C_1}F\cdot\mathrm{d}r=\int_{0}^{4}(- \frac{3 \sqrt{t}}{2} + 3 t)\,\mathrm{d}t=\left[- t^{\frac{3}{2}} + \frac{3 t^{2}}{2}\right]_{0}^{4}=16.$$

$$\int_C F\cdot\mathrm{d}r=(16)+(8)=24.$$