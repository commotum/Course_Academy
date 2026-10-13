# Line-segment one-form generator review

Local author preview at math basis 1356. Observed source masks and banks are separate from authored defaults. Raw q-124663 has an endpoint typo; generated versions repair +10 to +1.


## Original q-124654

If the path $C$ is the line segment $\overset{―}{MN}$ traversed from the point $M(-1,0)$ to the point $N(2,4),$ then ${\int }_{C}y\,dx-x\,dy=$


Bank: $2$, $\frac{11}{6}$, $\frac{4}{3}$, $4$, $3$


The position vectors of the endpoints of our line segment are $a=-i$ and $b=2\,i+4\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =-i+t(2\,i+4\,j-(-i)) \\  & =-i+t(3\,i+4\,j) \\  & =(3t-1)\,i+4t\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=3t-1$ and $y(t)=4t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=3\,i+4\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_{C}y\,dx-x\,dy & ={\int }_{0}^{1}y\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-x\,\frac{\text{d}y}{\text{d}t}\,dt \\  & ={\int }_{0}^{1}(y\,\frac{\text{d}x}{\text{d}t}-x\,\frac{\text{d}y}{\text{d}t})dt \\  & ={\int }_{0}^{1}4t(3)-(3t-1)(4)\,dt \\  & ={\int }_{0}^{1}4\,dt \\  & =4t\,{|}_{0}^{1} \\  & =4(1-0) \\  & =4\end{aligned}
$$


### Generated original-parameter replay

## q-124654 — easy
Author preview: observed; profile `q-124654_observed`; parameters `{'k': 1}`.

If the path $C$ is the line segment $\overset{―}{MN}$ traversed from the point $M(-1,0)$ to the point $N(2,4),$ then ${\int }_{C}y\,dx-x\,dy=$

- A. $\frac{4}{3}$
- B. $\frac{11}{6}$
- C. $2$
- D. $3$
- E. $4$ **correct**

**Worked solution**

The position vectors of the endpoints of our line segment are $a=-i$ and $b=2\,i+4\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =-i+t(2\,i+4\,j-(-i)) \\  & =-i+t(3\,i+4\,j) \\  & =(3t-1)\,i+4t\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=3t-1$ and $y(t)=4t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=3\,i+4\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_{C}y\,dx-x\,dy & ={\int }_{0}^{1}y\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-x\,\frac{\text{d}y}{\text{d}t}\,dt \\  & ={\int }_{0}^{1}(y\,\frac{\text{d}x}{\text{d}t}-x\,\frac{\text{d}y}{\text{d}t})dt \\  & ={\int }_{0}^{1}4t(3)-(3t-1)(4)\,dt \\  & ={\int }_{0}^{1}4\,dt \\  & =4t\,{|}_{0}^{1} \\  & =4(1-0) \\  & =4\end{aligned}
$$


### Generated observed-profile variant (uniform one-form multiplier)

## q-124654 — easy
Author preview: observed; profile `q-124654_observed`; parameters `{'k': -3}`.

If the path $C$ is the line segment $\overset{―}{MN}$ traversed from the point $M(-1,0)$ to the point $N(2,4),$ then $-3\left({\int }_{C}y\,dx-x\,dy\right)=$

- A. $-12$ **correct**
- B. $- \frac{11}{2}$
- C. $-9$
- D. $-6$
- E. $-4$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=-i$ and $b=2\,i+4\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =-i+t(2\,i+4\,j-(-i)) \\  & =-i+t(3\,i+4\,j) \\  & =(3t-1)\,i+4t\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=3t-1$ and $y(t)=4t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=3\,i+4\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}-3\left({\int }_{C}y\,dx-x\,dy\right) & =-3\left({\int }_{0}^{1}y\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-x\,\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =-3\left({\int }_{0}^{1}(y\,\frac{\text{d}x}{\text{d}t}-x\,\frac{\text{d}y}{\text{d}t})dt\right) \\  & =-3\left({\int }_{0}^{1}4t(3)-(3t-1)(4)\,dt\right) \\  & =-3\left({\int }_{0}^{1}4\,dt\right) \\  & =-3\left(4t\,{|}_{0}^{1}\right) \\  & =-3\left(4(1-0)\right) \\  & =-3\left(4\right)\end{aligned}
$$


### Generated observed-profile variant (uniform one-form multiplier)

## q-124654 — easy
Author preview: observed; profile `q-124654_observed`; parameters `{'k': 2}`.

If the path $C$ is the line segment $\overset{―}{MN}$ traversed from the point $M(-1,0)$ to the point $N(2,4),$ then $2\left({\int }_{C}y\,dx-x\,dy\right)=$

- A. $8$ **correct**
- B. $\frac{11}{3}$
- C. $6$
- D. $4$
- E. $\frac{8}{3}$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=-i$ and $b=2\,i+4\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =-i+t(2\,i+4\,j-(-i)) \\  & =-i+t(3\,i+4\,j) \\  & =(3t-1)\,i+4t\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=3t-1$ and $y(t)=4t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=3\,i+4\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}2\left({\int }_{C}y\,dx-x\,dy\right) & =2\left({\int }_{0}^{1}y\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-x\,\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =2\left({\int }_{0}^{1}(y\,\frac{\text{d}x}{\text{d}t}-x\,\frac{\text{d}y}{\text{d}t})dt\right) \\  & =2\left({\int }_{0}^{1}4t(3)-(3t-1)(4)\,dt\right) \\  & =2\left({\int }_{0}^{1}4\,dt\right) \\  & =2\left(4t\,{|}_{0}^{1}\right) \\  & =2\left(4(1-0)\right) \\  & =2\left(4\right)\end{aligned}
$$


### Generated authored method-bank variant

## q-124654 — easy
Author preview: observed; profile `method`; parameters `{'k': 2}`.

If the path $C$ is the line segment $\overset{―}{MN}$ traversed from the point $M(-1,0)$ to the point $N(2,4),$ then $2\left({\int }_{C}y\,dx-x\,dy\right)=$

- A. $-8$
- B. $8$ **correct**
- C. $12$
- D. $-4$
- E. $16$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=-i$ and $b=2\,i+4\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =-i+t(2\,i+4\,j-(-i)) \\  & =-i+t(3\,i+4\,j) \\  & =(3t-1)\,i+4t\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=3t-1$ and $y(t)=4t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=3\,i+4\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}2\left({\int }_{C}y\,dx-x\,dy\right) & =2\left({\int }_{0}^{1}y\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-x\,\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =2\left({\int }_{0}^{1}(y\,\frac{\text{d}x}{\text{d}t}-x\,\frac{\text{d}y}{\text{d}t})dt\right) \\  & =2\left({\int }_{0}^{1}4t(3)-(3t-1)(4)\,dt\right) \\  & =2\left({\int }_{0}^{1}4\,dt\right) \\  & =2\left(4t\,{|}_{0}^{1}\right) \\  & =2\left(4(1-0)\right) \\  & =2\left(4\right)\end{aligned}
$$


## Original q-81096

If the path $C$ is the line segment $\overset{―}{MN}$ traversed from the point $M(0,1)$ to the point $N(3,3),$ then ${\int }_{C}{x}^{2}\,dx-y\,dy=$


Bank: $5$, $10$, $25$, $15$, $20$


The position vectors of the endpoints of our line segment are $a=j$ and $b=3\,i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =j+t(3\,i+3\,j-j) \\  & =j+t(3\,i+2\,j) \\  & =3t\,i+(1+2t)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=3t$ and $y(t)=1+2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=3\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_{C}{x}^{2}\,dx-y\,dy & ={\int }_{0}^{1}{x}^{2}\frac{\text{d}x}{\text{d}t}\,\text{d}t-y\frac{\text{d}y}{\text{d}t}\,dt \\  & ={\int }_{0}^{1}({x}^{2}\frac{\text{d}x}{\text{d}t}-y\frac{\text{d}y}{\text{d}t})\,dt \\  & ={\int }_{0}^{1}(3t)^{2}\cdot 3-(1+2t)\cdot 2\,dt \\  & ={\int }_{0}^{1}27{t}^{2}-2-4t\,dt \\  & ={[9{t}^{3}-2t-2{t}^{2}]}_{0}^{1} \\  & =[9(1)^{3}-2(1)-2(1)^{2}]-[0] \\  & =5\end{aligned}
$$


### Generated original-parameter replay

## q-81096 — easy
Author preview: observed; profile `q-81096_observed`; parameters `{'k': 1}`.

If the path $C$ is the line segment $\overset{―}{MN}$ traversed from the point $M(0,1)$ to the point $N(3,3),$ then ${\int }_{C}{x}^{2}\,dx-y\,dy=$

- A. $25$
- B. $10$
- C. $5$ **correct**
- D. $20$
- E. $15$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=j$ and $b=3\,i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =j+t(3\,i+3\,j-j) \\  & =j+t(3\,i+2\,j) \\  & =3t\,i+(1+2t)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=3t$ and $y(t)=1+2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=3\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_{C}{x}^{2}\,dx-y\,dy & ={\int }_{0}^{1}{x}^{2}\frac{\text{d}x}{\text{d}t}\,\text{d}t-y\frac{\text{d}y}{\text{d}t}\,dt \\  & ={\int }_{0}^{1}({x}^{2}\frac{\text{d}x}{\text{d}t}-y\frac{\text{d}y}{\text{d}t})\,dt \\  & ={\int }_{0}^{1}(3t)^{2}\cdot 3-(1+2t)\cdot 2\,dt \\  & ={\int }_{0}^{1}27{t}^{2}-2-4t\,dt \\  & ={[9{t}^{3}-2t-2{t}^{2}]}_{0}^{1} \\  & =[9(1)^{3}-2(1)-2(1)^{2}]-[0] \\  & =5\end{aligned}
$$


### Generated observed-profile variant (uniform one-form multiplier)

## q-81096 — easy
Author preview: observed; profile `q-81096_observed`; parameters `{'k': -3}`.

If the path $C$ is the line segment $\overset{―}{MN}$ traversed from the point $M(0,1)$ to the point $N(3,3),$ then $-3\left({\int }_{C}{x}^{2}\,dx-y\,dy\right)=$

- A. $-45$
- B. $-30$
- C. $-60$
- D. $-15$ **correct**
- E. $-75$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=j$ and $b=3\,i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =j+t(3\,i+3\,j-j) \\  & =j+t(3\,i+2\,j) \\  & =3t\,i+(1+2t)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=3t$ and $y(t)=1+2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=3\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}-3\left({\int }_{C}{x}^{2}\,dx-y\,dy\right) & =-3\left({\int }_{0}^{1}{x}^{2}\frac{\text{d}x}{\text{d}t}\,\text{d}t-y\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =-3\left({\int }_{0}^{1}({x}^{2}\frac{\text{d}x}{\text{d}t}-y\frac{\text{d}y}{\text{d}t})\,dt\right) \\  & =-3\left({\int }_{0}^{1}(3t)^{2}\cdot 3-(1+2t)\cdot 2\,dt\right) \\  & =-3\left({\int }_{0}^{1}27{t}^{2}-2-4t\,dt\right) \\  & =-3\left({[9{t}^{3}-2t-2{t}^{2}]}_{0}^{1}\right) \\  & =-3\left([9(1)^{3}-2(1)-2(1)^{2}]-[0]\right) \\  & =-3\left(5\right)\end{aligned}
$$


### Generated observed-profile variant (uniform one-form multiplier)

## q-81096 — easy
Author preview: observed; profile `q-81096_observed`; parameters `{'k': 2}`.

If the path $C$ is the line segment $\overset{―}{MN}$ traversed from the point $M(0,1)$ to the point $N(3,3),$ then $2\left({\int }_{C}{x}^{2}\,dx-y\,dy\right)=$

- A. $30$
- B. $20$
- C. $40$
- D. $10$ **correct**
- E. $50$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=j$ and $b=3\,i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =j+t(3\,i+3\,j-j) \\  & =j+t(3\,i+2\,j) \\  & =3t\,i+(1+2t)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=3t$ and $y(t)=1+2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=3\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}2\left({\int }_{C}{x}^{2}\,dx-y\,dy\right) & =2\left({\int }_{0}^{1}{x}^{2}\frac{\text{d}x}{\text{d}t}\,\text{d}t-y\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =2\left({\int }_{0}^{1}({x}^{2}\frac{\text{d}x}{\text{d}t}-y\frac{\text{d}y}{\text{d}t})\,dt\right) \\  & =2\left({\int }_{0}^{1}(3t)^{2}\cdot 3-(1+2t)\cdot 2\,dt\right) \\  & =2\left({\int }_{0}^{1}27{t}^{2}-2-4t\,dt\right) \\  & =2\left({[9{t}^{3}-2t-2{t}^{2}]}_{0}^{1}\right) \\  & =2\left([9(1)^{3}-2(1)-2(1)^{2}]-[0]\right) \\  & =2\left(5\right)\end{aligned}
$$


### Generated authored method-bank variant

## q-81096 — easy
Author preview: observed; profile `method`; parameters `{'k': 2}`.

If the path $C$ is the line segment $\overset{―}{MN}$ traversed from the point $M(0,1)$ to the point $N(3,3),$ then $2\left({\int }_{C}{x}^{2}\,dx-y\,dy\right)=$

- A. $-10$
- B. $10$ **correct**
- C. $18$
- D. $-8$
- E. $26$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=j$ and $b=3\,i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =j+t(3\,i+3\,j-j) \\  & =j+t(3\,i+2\,j) \\  & =3t\,i+(1+2t)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=3t$ and $y(t)=1+2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=3\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}2\left({\int }_{C}{x}^{2}\,dx-y\,dy\right) & =2\left({\int }_{0}^{1}{x}^{2}\frac{\text{d}x}{\text{d}t}\,\text{d}t-y\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =2\left({\int }_{0}^{1}({x}^{2}\frac{\text{d}x}{\text{d}t}-y\frac{\text{d}y}{\text{d}t})\,dt\right) \\  & =2\left({\int }_{0}^{1}(3t)^{2}\cdot 3-(1+2t)\cdot 2\,dt\right) \\  & =2\left({\int }_{0}^{1}27{t}^{2}-2-4t\,dt\right) \\  & =2\left({[9{t}^{3}-2t-2{t}^{2}]}_{0}^{1}\right) \\  & =2\left([9(1)^{3}-2(1)-2(1)^{2}]-[0]\right) \\  & =2\left(5\right)\end{aligned}
$$


## Original q-124652

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(-1,2)$ to the point $B(1,0),$ then ${\int }_{C}xy\,dx+dy=$


Bank: $-\frac{3}{2}$, $2$, $-1$, $\frac{3}{4}$, $-\frac{8}{3}$


The position vectors of the endpoints of our line segment are $a=-i+2\,j$ and $b=i.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =-i+2\,j+t(i-(-i+2\,j)) \\  & =-i+2\,j+t(2\,i-2\,j) \\  & =(2t-1)\,i+(2-2t)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=2t-1$ and $y(t)=2-2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=2\,i-2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_{C}xy\,dx+dy & ={\int }_{0}^{1}xy\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+\frac{\text{d}y}{\text{d}t}\,dt \\  & ={\int }_{0}^{1}(xy\,\frac{\text{d}x}{\text{d}t}+\frac{\text{d}y}{\text{d}t})dt \\  & ={\int }_{0}^{1}(2t-1)(2-2t)(2)+(-2)\,dt \\  & =2{\int }_{0}^{1}(2t-1)(2-2t)-1\,dt \\  & =2{\int }_{0}^{1}-4{t}^{2}+6t-3\,dt \\  & =2{[-\frac{4{t}^{3}}{3}+3{t}^{2}-3t]}_{0}^{1} \\  & =2[-\frac{4}{3}+3-3]-2[0] \\  & =2[-\frac{4}{3}] \\  & =-\frac{8}{3}\end{aligned}
$$


### Generated original-parameter replay

## q-124652 — easy
Author preview: observed; profile `q-124652_observed`; parameters `{'k': 1}`.

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(-1,2)$ to the point $B(1,0),$ then ${\int }_{C}xy\,dx+dy=$

- A. $-1$
- B. $2$
- C. $-\frac{3}{2}$
- D. $-\frac{8}{3}$ **correct**
- E. $\frac{3}{4}$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=-i+2\,j$ and $b=i.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =-i+2\,j+t(i-(-i+2\,j)) \\  & =-i+2\,j+t(2\,i-2\,j) \\  & =(2t-1)\,i+(2-2t)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=2t-1$ and $y(t)=2-2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=2\,i-2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_{C}xy\,dx+dy & ={\int }_{0}^{1}xy\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+\frac{\text{d}y}{\text{d}t}\,dt \\  & ={\int }_{0}^{1}(xy\,\frac{\text{d}x}{\text{d}t}+\frac{\text{d}y}{\text{d}t})dt \\  & ={\int }_{0}^{1}(2t-1)(2-2t)(2)+(-2)\,dt \\  & =2{\int }_{0}^{1}(2t-1)(2-2t)-1\,dt \\  & =2{\int }_{0}^{1}-4{t}^{2}+6t-3\,dt \\  & =2{[-\frac{4{t}^{3}}{3}+3{t}^{2}-3t]}_{0}^{1} \\  & =2[-\frac{4}{3}+3-3]-2[0] \\  & =2[-\frac{4}{3}] \\  & =-\frac{8}{3}\end{aligned}
$$


### Generated observed-profile variant (uniform one-form multiplier)

## q-124652 — easy
Author preview: observed; profile `q-124652_observed`; parameters `{'k': -3}`.

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(-1,2)$ to the point $B(1,0),$ then $-3\left({\int }_{C}xy\,dx+dy\right)=$

- A. $- \frac{9}{4}$
- B. $-6$
- C. $8$ **correct**
- D. $\frac{9}{2}$
- E. $3$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=-i+2\,j$ and $b=i.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =-i+2\,j+t(i-(-i+2\,j)) \\  & =-i+2\,j+t(2\,i-2\,j) \\  & =(2t-1)\,i+(2-2t)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=2t-1$ and $y(t)=2-2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=2\,i-2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}-3\left({\int }_{C}xy\,dx+dy\right) & =-3\left({\int }_{0}^{1}xy\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =-3\left({\int }_{0}^{1}(xy\,\frac{\text{d}x}{\text{d}t}+\frac{\text{d}y}{\text{d}t})dt\right) \\  & =-3\left({\int }_{0}^{1}(2t-1)(2-2t)(2)+(-2)\,dt\right) \\  & =-3\left(2{\int }_{0}^{1}(2t-1)(2-2t)-1\,dt\right) \\  & =-3\left(2{\int }_{0}^{1}-4{t}^{2}+6t-3\,dt\right) \\  & =-3\left(2{[-\frac{4{t}^{3}}{3}+3{t}^{2}-3t]}_{0}^{1}\right) \\  & =-3\left(2[-\frac{4}{3}+3-3]-2[0]\right) \\  & =-3\left(2[-\frac{4}{3}]\right) \\  & =-3\left(-\frac{8}{3}\right)\end{aligned}
$$


### Generated observed-profile variant (uniform one-form multiplier)

## q-124652 — easy
Author preview: observed; profile `q-124652_observed`; parameters `{'k': 2}`.

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(-1,2)$ to the point $B(1,0),$ then $2\left({\int }_{C}xy\,dx+dy\right)=$

- A. $\frac{3}{2}$
- B. $4$
- C. $- \frac{16}{3}$ **correct**
- D. $-3$
- E. $-2$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=-i+2\,j$ and $b=i.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =-i+2\,j+t(i-(-i+2\,j)) \\  & =-i+2\,j+t(2\,i-2\,j) \\  & =(2t-1)\,i+(2-2t)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=2t-1$ and $y(t)=2-2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=2\,i-2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}2\left({\int }_{C}xy\,dx+dy\right) & =2\left({\int }_{0}^{1}xy\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =2\left({\int }_{0}^{1}(xy\,\frac{\text{d}x}{\text{d}t}+\frac{\text{d}y}{\text{d}t})dt\right) \\  & =2\left({\int }_{0}^{1}(2t-1)(2-2t)(2)+(-2)\,dt\right) \\  & =2\left(2{\int }_{0}^{1}(2t-1)(2-2t)-1\,dt\right) \\  & =2\left(2{\int }_{0}^{1}-4{t}^{2}+6t-3\,dt\right) \\  & =2\left(2{[-\frac{4{t}^{3}}{3}+3{t}^{2}-3t]}_{0}^{1}\right) \\  & =2\left(2[-\frac{4}{3}+3-3]-2[0]\right) \\  & =2\left(2[-\frac{4}{3}]\right) \\  & =2\left(-\frac{8}{3}\right)\end{aligned}
$$


### Generated authored method-bank variant

## q-124652 — easy
Author preview: observed; profile `method`; parameters `{'k': 2}`.

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(-1,2)$ to the point $B(1,0),$ then $2\left({\int }_{C}xy\,dx+dy\right)=$

- A. $\frac{16}{3}$
- B. $- \frac{16}{3}$ **correct**
- C. $- \frac{4}{3}$
- D. $-4$
- E. $\frac{8}{3}$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=-i+2\,j$ and $b=i.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =-i+2\,j+t(i-(-i+2\,j)) \\  & =-i+2\,j+t(2\,i-2\,j) \\  & =(2t-1)\,i+(2-2t)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=2t-1$ and $y(t)=2-2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=2\,i-2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}2\left({\int }_{C}xy\,dx+dy\right) & =2\left({\int }_{0}^{1}xy\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =2\left({\int }_{0}^{1}(xy\,\frac{\text{d}x}{\text{d}t}+\frac{\text{d}y}{\text{d}t})dt\right) \\  & =2\left({\int }_{0}^{1}(2t-1)(2-2t)(2)+(-2)\,dt\right) \\  & =2\left(2{\int }_{0}^{1}(2t-1)(2-2t)-1\,dt\right) \\  & =2\left(2{\int }_{0}^{1}-4{t}^{2}+6t-3\,dt\right) \\  & =2\left(2{[-\frac{4{t}^{3}}{3}+3{t}^{2}-3t]}_{0}^{1}\right) \\  & =2\left(2[-\frac{4}{3}+3-3]-2[0]\right) \\  & =2\left(2[-\frac{4}{3}]\right) \\  & =2\left(-\frac{8}{3}\right)\end{aligned}
$$


## Original q-124658

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(0,0)$ to the point $B(4,2),$ then ${\int }_{C}{e}^{x+y}\,dx-{e}^{x+y}\,dy=$


Bank: $\frac{3{e}^{4}-1}{2}$, $\frac{{e}^{4}-2}{3}$, $\frac{{e}^{6}-3}{2}$, $\frac{2{e}^{6}-1}{3}$, $\frac{{e}^{6}-1}{3}$


The position vectors of the endpoints of our line segment are $a=0\,i+0\,j$ and $b=4\,i+2\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =0\,i+0\,j+t(4\,i+2\,j-(0\,i+0\,j)) \\  & =4t\,i+2t\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=4t$ and $y(t)=2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=4\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_{C}{e}^{x+y}\,dx-{e}^{x+y}\,dy & ={\int }_{0}^{1}{e}^{x+y}\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-{e}^{x+y}\,\frac{\text{d}y}{\text{d}t}\,dt \\  & ={\int }_{0}^{1}{e}^{x+y}(\frac{\text{d}x}{\text{d}t}-\frac{\text{d}y}{\text{d}t})\text{d}t \\  & ={\int }_{0}^{1}{e}^{4t+2t}(4-2)\,\text{d}t \\  & =2{\int }_{0}^{1}{e}^{6t}\,\text{d}t \\  & =\frac{{e}^{6t}}{3}\,{|}_{0}^{1} \\  & =\frac{{e}^{6(1)}}{3}-\frac{{e}^{6(0)}}{3} \\  & =\frac{{e}^{6}}{3}-\frac{1}{3} \\  & =\frac{{e}^{6}-1}{3}\end{aligned}
$$


### Generated original-parameter replay

## q-124658 — easy
Author preview: observed; profile `q-124658_observed`; parameters `{'k': 1}`.

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(0,0)$ to the point $B(4,2),$ then ${\int }_{C}{e}^{x+y}\,dx-{e}^{x+y}\,dy=$

- A. $\frac{{e}^{6}-3}{2}$
- B. $\frac{{e}^{4}-2}{3}$
- C. $\frac{3{e}^{4}-1}{2}$
- D. $\frac{{e}^{6}-1}{3}$ **correct**
- E. $\frac{2{e}^{6}-1}{3}$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=0\,i+0\,j$ and $b=4\,i+2\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =0\,i+0\,j+t(4\,i+2\,j-(0\,i+0\,j)) \\  & =4t\,i+2t\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=4t$ and $y(t)=2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=4\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_{C}{e}^{x+y}\,dx-{e}^{x+y}\,dy & ={\int }_{0}^{1}{e}^{x+y}\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-{e}^{x+y}\,\frac{\text{d}y}{\text{d}t}\,dt \\  & ={\int }_{0}^{1}{e}^{x+y}(\frac{\text{d}x}{\text{d}t}-\frac{\text{d}y}{\text{d}t})\text{d}t \\  & ={\int }_{0}^{1}{e}^{4t+2t}(4-2)\,\text{d}t \\  & =2{\int }_{0}^{1}{e}^{6t}\,\text{d}t \\  & =\frac{{e}^{6t}}{3}\,{|}_{0}^{1} \\  & =\frac{{e}^{6(1)}}{3}-\frac{{e}^{6(0)}}{3} \\  & =\frac{{e}^{6}}{3}-\frac{1}{3} \\  & =\frac{{e}^{6}-1}{3}\end{aligned}
$$


### Generated observed-profile variant (uniform one-form multiplier)

## q-124658 — easy
Author preview: observed; profile `q-124658_observed`; parameters `{'k': -3}`.

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(0,0)$ to the point $B(4,2),$ then $-3\left({\int }_{C}{e}^{x+y}\,dx-{e}^{x+y}\,dy\right)=$

- A. $1 - 2 e^{6}$
- B. $2 - e^{4}$
- C. $1 - e^{6}$ **correct**
- D. $\frac{3}{2} - \frac{9 e^{4}}{2}$
- E. $\frac{9}{2} - \frac{3 e^{6}}{2}$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=0\,i+0\,j$ and $b=4\,i+2\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =0\,i+0\,j+t(4\,i+2\,j-(0\,i+0\,j)) \\  & =4t\,i+2t\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=4t$ and $y(t)=2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=4\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}-3\left({\int }_{C}{e}^{x+y}\,dx-{e}^{x+y}\,dy\right) & =-3\left({\int }_{0}^{1}{e}^{x+y}\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-{e}^{x+y}\,\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =-3\left({\int }_{0}^{1}{e}^{x+y}(\frac{\text{d}x}{\text{d}t}-\frac{\text{d}y}{\text{d}t})\text{d}t\right) \\  & =-3\left({\int }_{0}^{1}{e}^{4t+2t}(4-2)\,\text{d}t\right) \\  & =-3\left(2{\int }_{0}^{1}{e}^{6t}\,\text{d}t\right) \\  & =-3\left(\frac{{e}^{6t}}{3}\,{|}_{0}^{1}\right) \\  & =-3\left(\frac{{e}^{6(1)}}{3}-\frac{{e}^{6(0)}}{3}\right) \\  & =-3\left(\frac{{e}^{6}}{3}-\frac{1}{3}\right) \\  & =-3\left(\frac{{e}^{6}-1}{3}\right)\end{aligned}
$$


### Generated observed-profile variant (uniform one-form multiplier)

## q-124658 — easy
Author preview: observed; profile `q-124658_observed`; parameters `{'k': 2}`.

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(0,0)$ to the point $B(4,2),$ then $2\left({\int }_{C}{e}^{x+y}\,dx-{e}^{x+y}\,dy\right)=$

- A. $- \frac{2}{3} + \frac{4 e^{6}}{3}$
- B. $- \frac{4}{3} + \frac{2 e^{4}}{3}$
- C. $- \frac{2}{3} + \frac{2 e^{6}}{3}$ **correct**
- D. $-1 + 3 e^{4}$
- E. $-3 + e^{6}$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=0\,i+0\,j$ and $b=4\,i+2\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =0\,i+0\,j+t(4\,i+2\,j-(0\,i+0\,j)) \\  & =4t\,i+2t\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=4t$ and $y(t)=2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=4\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}2\left({\int }_{C}{e}^{x+y}\,dx-{e}^{x+y}\,dy\right) & =2\left({\int }_{0}^{1}{e}^{x+y}\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-{e}^{x+y}\,\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =2\left({\int }_{0}^{1}{e}^{x+y}(\frac{\text{d}x}{\text{d}t}-\frac{\text{d}y}{\text{d}t})\text{d}t\right) \\  & =2\left({\int }_{0}^{1}{e}^{4t+2t}(4-2)\,\text{d}t\right) \\  & =2\left(2{\int }_{0}^{1}{e}^{6t}\,\text{d}t\right) \\  & =2\left(\frac{{e}^{6t}}{3}\,{|}_{0}^{1}\right) \\  & =2\left(\frac{{e}^{6(1)}}{3}-\frac{{e}^{6(0)}}{3}\right) \\  & =2\left(\frac{{e}^{6}}{3}-\frac{1}{3}\right) \\  & =2\left(\frac{{e}^{6}-1}{3}\right)\end{aligned}
$$


### Generated authored method-bank variant

## q-124658 — easy
Author preview: observed; profile `method`; parameters `{'k': 2}`.

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(0,0)$ to the point $B(4,2),$ then $2\left({\int }_{C}{e}^{x+y}\,dx-{e}^{x+y}\,dy\right)=$

- A. $\frac{2 e^{6}}{3}$
- B. $- \frac{2}{3} + \frac{2 e^{6}}{3}$ **correct**
- C. $- \frac{4}{3} + \frac{4 e^{6}}{3}$
- D. $\frac{2}{3} - \frac{2 e^{6}}{3}$
- E. $-2 + 2 e^{6}$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=0\,i+0\,j$ and $b=4\,i+2\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =0\,i+0\,j+t(4\,i+2\,j-(0\,i+0\,j)) \\  & =4t\,i+2t\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=4t$ and $y(t)=2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=4\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}2\left({\int }_{C}{e}^{x+y}\,dx-{e}^{x+y}\,dy\right) & =2\left({\int }_{0}^{1}{e}^{x+y}\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-{e}^{x+y}\,\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =2\left({\int }_{0}^{1}{e}^{x+y}(\frac{\text{d}x}{\text{d}t}-\frac{\text{d}y}{\text{d}t})\text{d}t\right) \\  & =2\left({\int }_{0}^{1}{e}^{4t+2t}(4-2)\,\text{d}t\right) \\  & =2\left(2{\int }_{0}^{1}{e}^{6t}\,\text{d}t\right) \\  & =2\left(\frac{{e}^{6t}}{3}\,{|}_{0}^{1}\right) \\  & =2\left(\frac{{e}^{6(1)}}{3}-\frac{{e}^{6(0)}}{3}\right) \\  & =2\left(\frac{{e}^{6}}{3}-\frac{1}{3}\right) \\  & =2\left(\frac{{e}^{6}-1}{3}\right)\end{aligned}
$$


## Original q-124663

If the path $C$ is the line segment $\overset{―}{MN}$ traversed from the point $M(-1,1)$ to the point $N(1,3),$ then ${\int }_{C}{y}^{2}\,dx+{x}^{2}\,dy=$


Bank: $\frac{28}{3}$, $\frac{25}{2}$, $\frac{20}{3}$, $9$, $7$


The position vectors of the endpoints of our line segment are $a=-i+j$ and $b=i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =-i+j+t(i+3\,j-(-i+j)) \\  & =-i+j+t(2\,i+2\,j) \\  & =(2t-1)\,i+(2t+1)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=2t-1$ and $y(t)=2t+1$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=2\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_{C}{y}^{2}\,dx+{x}^{2}\,dy & ={\int }_{0}^{1}{y}^{2}\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+{x}^{2}\,\frac{\text{d}y}{\text{d}t}\,dt \\  & ={\int }_{0}^{1}({y}^{2}\,\frac{\text{d}x}{\text{d}t}+{x}^{2}\,\frac{\text{d}y}{\text{d}t})dt \\  & ={\int }_{0}^{1}(2t+1)^{2}\cdot 2+(2t-1)^{2}\cdot 2\,dt \\  & =2{\int }_{0}^{1}(4{t}^{2}+4t+1)+(4{t}^{2}-4t+1)\,dt \\  & =2{\int }_{0}^{1}8{t}^{2}+2\,dt \\  & =4{\int }_{0}^{1}4{t}^{2}+1\,dt \\  & =4{[\frac{4{t}^{3}}{3}+t]}_{0}^{1} \\  & =4[\frac{4}{3}+10]-4[0] \\  & =\frac{28}{3}\end{aligned}
$$


### Generated original-parameter replay

## q-124663 — easy
Author preview: observed; profile `q-124663_observed`; parameters `{'k': 1}`.

If the path $C$ is the line segment $\overset{―}{MN}$ traversed from the point $M(-1,1)$ to the point $N(1,3),$ then ${\int }_{C}{y}^{2}\,dx+{x}^{2}\,dy=$

- A. $\frac{20}{3}$
- B. $\frac{25}{2}$
- C. $\frac{28}{3}$ **correct**
- D. $7$
- E. $9$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=-i+j$ and $b=i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =-i+j+t(i+3\,j-(-i+j)) \\  & =-i+j+t(2\,i+2\,j) \\  & =(2t-1)\,i+(2t+1)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=2t-1$ and $y(t)=2t+1$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=2\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_{C}{y}^{2}\,dx+{x}^{2}\,dy & ={\int }_{0}^{1}{y}^{2}\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+{x}^{2}\,\frac{\text{d}y}{\text{d}t}\,dt \\  & ={\int }_{0}^{1}({y}^{2}\,\frac{\text{d}x}{\text{d}t}+{x}^{2}\,\frac{\text{d}y}{\text{d}t})dt \\  & ={\int }_{0}^{1}(2t+1)^{2}\cdot 2+(2t-1)^{2}\cdot 2\,dt \\  & =2{\int }_{0}^{1}(4{t}^{2}+4t+1)+(4{t}^{2}-4t+1)\,dt \\  & =2{\int }_{0}^{1}8{t}^{2}+2\,dt \\  & =4{\int }_{0}^{1}4{t}^{2}+1\,dt \\  & =4{[\frac{4{t}^{3}}{3}+t]}_{0}^{1} \\  & =4[\frac{4}{3}+1]-4[0] \\  & =\frac{28}{3}\end{aligned}
$$


### Generated observed-profile variant (uniform one-form multiplier)

## q-124663 — easy
Author preview: observed; profile `q-124663_observed`; parameters `{'k': -3}`.

If the path $C$ is the line segment $\overset{―}{MN}$ traversed from the point $M(-1,1)$ to the point $N(1,3),$ then $-3\left({\int }_{C}{y}^{2}\,dx+{x}^{2}\,dy\right)=$

- A. $-27$
- B. $- \frac{75}{2}$
- C. $-21$
- D. $-28$ **correct**
- E. $-20$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=-i+j$ and $b=i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =-i+j+t(i+3\,j-(-i+j)) \\  & =-i+j+t(2\,i+2\,j) \\  & =(2t-1)\,i+(2t+1)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=2t-1$ and $y(t)=2t+1$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=2\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}-3\left({\int }_{C}{y}^{2}\,dx+{x}^{2}\,dy\right) & =-3\left({\int }_{0}^{1}{y}^{2}\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+{x}^{2}\,\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =-3\left({\int }_{0}^{1}({y}^{2}\,\frac{\text{d}x}{\text{d}t}+{x}^{2}\,\frac{\text{d}y}{\text{d}t})dt\right) \\  & =-3\left({\int }_{0}^{1}(2t+1)^{2}\cdot 2+(2t-1)^{2}\cdot 2\,dt\right) \\  & =-3\left(2{\int }_{0}^{1}(4{t}^{2}+4t+1)+(4{t}^{2}-4t+1)\,dt\right) \\  & =-3\left(2{\int }_{0}^{1}8{t}^{2}+2\,dt\right) \\  & =-3\left(4{\int }_{0}^{1}4{t}^{2}+1\,dt\right) \\  & =-3\left(4{[\frac{4{t}^{3}}{3}+t]}_{0}^{1}\right) \\  & =-3\left(4[\frac{4}{3}+1]-4[0]\right) \\  & =-3\left(\frac{28}{3}\right)\end{aligned}
$$


### Generated observed-profile variant (uniform one-form multiplier)

## q-124663 — easy
Author preview: observed; profile `q-124663_observed`; parameters `{'k': 2}`.

If the path $C$ is the line segment $\overset{―}{MN}$ traversed from the point $M(-1,1)$ to the point $N(1,3),$ then $2\left({\int }_{C}{y}^{2}\,dx+{x}^{2}\,dy\right)=$

- A. $18$
- B. $25$
- C. $14$
- D. $\frac{56}{3}$ **correct**
- E. $\frac{40}{3}$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=-i+j$ and $b=i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =-i+j+t(i+3\,j-(-i+j)) \\  & =-i+j+t(2\,i+2\,j) \\  & =(2t-1)\,i+(2t+1)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=2t-1$ and $y(t)=2t+1$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=2\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}2\left({\int }_{C}{y}^{2}\,dx+{x}^{2}\,dy\right) & =2\left({\int }_{0}^{1}{y}^{2}\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+{x}^{2}\,\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =2\left({\int }_{0}^{1}({y}^{2}\,\frac{\text{d}x}{\text{d}t}+{x}^{2}\,\frac{\text{d}y}{\text{d}t})dt\right) \\  & =2\left({\int }_{0}^{1}(2t+1)^{2}\cdot 2+(2t-1)^{2}\cdot 2\,dt\right) \\  & =2\left(2{\int }_{0}^{1}(4{t}^{2}+4t+1)+(4{t}^{2}-4t+1)\,dt\right) \\  & =2\left(2{\int }_{0}^{1}8{t}^{2}+2\,dt\right) \\  & =2\left(4{\int }_{0}^{1}4{t}^{2}+1\,dt\right) \\  & =2\left(4{[\frac{4{t}^{3}}{3}+t]}_{0}^{1}\right) \\  & =2\left(4[\frac{4}{3}+1]-4[0]\right) \\  & =2\left(\frac{28}{3}\right)\end{aligned}
$$


### Generated authored method-bank variant

## q-124663 — easy
Author preview: observed; profile `method`; parameters `{'k': 2}`.

If the path $C$ is the line segment $\overset{―}{MN}$ traversed from the point $M(-1,1)$ to the point $N(1,3),$ then $2\left({\int }_{C}{y}^{2}\,dx+{x}^{2}\,dy\right)=$

- A. $- \frac{56}{3}$
- B. $\frac{56}{3}$ **correct**
- C. $\frac{52}{3}$
- D. $\frac{4}{3}$
- E. $16$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=-i+j$ and $b=i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =-i+j+t(i+3\,j-(-i+j)) \\  & =-i+j+t(2\,i+2\,j) \\  & =(2t-1)\,i+(2t+1)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=2t-1$ and $y(t)=2t+1$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=2\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}2\left({\int }_{C}{y}^{2}\,dx+{x}^{2}\,dy\right) & =2\left({\int }_{0}^{1}{y}^{2}\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+{x}^{2}\,\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =2\left({\int }_{0}^{1}({y}^{2}\,\frac{\text{d}x}{\text{d}t}+{x}^{2}\,\frac{\text{d}y}{\text{d}t})dt\right) \\  & =2\left({\int }_{0}^{1}(2t+1)^{2}\cdot 2+(2t-1)^{2}\cdot 2\,dt\right) \\  & =2\left(2{\int }_{0}^{1}(4{t}^{2}+4t+1)+(4{t}^{2}-4t+1)\,dt\right) \\  & =2\left(2{\int }_{0}^{1}8{t}^{2}+2\,dt\right) \\  & =2\left(4{\int }_{0}^{1}4{t}^{2}+1\,dt\right) \\  & =2\left(4{[\frac{4{t}^{3}}{3}+t]}_{0}^{1}\right) \\  & =2\left(4[\frac{4}{3}+1]-4[0]\right) \\  & =2\left(\frac{28}{3}\right)\end{aligned}
$$


## Original q-39345

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(1,2)$ to the point $B(3,4),$ then ${\int }_{C}x\,dx+y\,dy=$


Bank: $12$, $9$, $16$, $10$, $18$


The position vectors of the endpoints of our line segment are $a=i+2\,j$ and $b=3\,i+4\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =i+2\,j+t(3\,i+4\,j-(i+2\,j)) \\  & =i+2\,j+t(2\,i+2\,j) \\  & =(1+2t)\,i+(2+2t)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=1+2t$ and $y(t)=2+2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=2\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_{C}x\,dx+y\,dy & ={\int }_{0}^{1}x\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+y\,\frac{\text{d}y}{\text{d}t}\,dt \\  & ={\int }_{0}^{1}(x\frac{\text{d}x}{\text{d}t}+y\frac{\text{d}y}{\text{d}t})dt \\  & ={\int }_{0}^{1}(1+2t)\cdot 2+(2+2t)\cdot 2\,dt \\  & ={\int }_{0}^{1}6+8t\,dt \\  & ={[6t+4{t}^{2}]}_{0}^{1} \\  & =[6(1)+4(1)^{2}]-[0] \\  & =10\end{aligned}
$$


### Generated original-parameter replay

## q-39345 — easy
Author preview: observed; profile `q-39345_observed`; parameters `{'k': 1}`.

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(1,2)$ to the point $B(3,4),$ then ${\int }_{C}x\,dx+y\,dy=$

- A. $16$
- B. $9$
- C. $12$
- D. $18$
- E. $10$ **correct**

**Worked solution**

The position vectors of the endpoints of our line segment are $a=i+2\,j$ and $b=3\,i+4\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =i+2\,j+t(3\,i+4\,j-(i+2\,j)) \\  & =i+2\,j+t(2\,i+2\,j) \\  & =(1+2t)\,i+(2+2t)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=1+2t$ and $y(t)=2+2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=2\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_{C}x\,dx+y\,dy & ={\int }_{0}^{1}x\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+y\,\frac{\text{d}y}{\text{d}t}\,dt \\  & ={\int }_{0}^{1}(x\frac{\text{d}x}{\text{d}t}+y\frac{\text{d}y}{\text{d}t})dt \\  & ={\int }_{0}^{1}(1+2t)\cdot 2+(2+2t)\cdot 2\,dt \\  & ={\int }_{0}^{1}6+8t\,dt \\  & ={[6t+4{t}^{2}]}_{0}^{1} \\  & =[6(1)+4(1)^{2}]-[0] \\  & =10\end{aligned}
$$


### Generated observed-profile variant (uniform one-form multiplier)

## q-39345 — easy
Author preview: observed; profile `q-39345_observed`; parameters `{'k': -3}`.

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(1,2)$ to the point $B(3,4),$ then $-3\left({\int }_{C}x\,dx+y\,dy\right)=$

- A. $-30$ **correct**
- B. $-27$
- C. $-54$
- D. $-36$
- E. $-48$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=i+2\,j$ and $b=3\,i+4\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =i+2\,j+t(3\,i+4\,j-(i+2\,j)) \\  & =i+2\,j+t(2\,i+2\,j) \\  & =(1+2t)\,i+(2+2t)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=1+2t$ and $y(t)=2+2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=2\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}-3\left({\int }_{C}x\,dx+y\,dy\right) & =-3\left({\int }_{0}^{1}x\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+y\,\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =-3\left({\int }_{0}^{1}(x\frac{\text{d}x}{\text{d}t}+y\frac{\text{d}y}{\text{d}t})dt\right) \\  & =-3\left({\int }_{0}^{1}(1+2t)\cdot 2+(2+2t)\cdot 2\,dt\right) \\  & =-3\left({\int }_{0}^{1}6+8t\,dt\right) \\  & =-3\left({[6t+4{t}^{2}]}_{0}^{1}\right) \\  & =-3\left([6(1)+4(1)^{2}]-[0]\right) \\  & =-3\left(10\right)\end{aligned}
$$


### Generated observed-profile variant (uniform one-form multiplier)

## q-39345 — easy
Author preview: observed; profile `q-39345_observed`; parameters `{'k': 2}`.

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(1,2)$ to the point $B(3,4),$ then $2\left({\int }_{C}x\,dx+y\,dy\right)=$

- A. $20$ **correct**
- B. $18$
- C. $36$
- D. $24$
- E. $32$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=i+2\,j$ and $b=3\,i+4\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =i+2\,j+t(3\,i+4\,j-(i+2\,j)) \\  & =i+2\,j+t(2\,i+2\,j) \\  & =(1+2t)\,i+(2+2t)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=1+2t$ and $y(t)=2+2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=2\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}2\left({\int }_{C}x\,dx+y\,dy\right) & =2\left({\int }_{0}^{1}x\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+y\,\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =2\left({\int }_{0}^{1}(x\frac{\text{d}x}{\text{d}t}+y\frac{\text{d}y}{\text{d}t})dt\right) \\  & =2\left({\int }_{0}^{1}(1+2t)\cdot 2+(2+2t)\cdot 2\,dt\right) \\  & =2\left({\int }_{0}^{1}6+8t\,dt\right) \\  & =2\left({[6t+4{t}^{2}]}_{0}^{1}\right) \\  & =2\left([6(1)+4(1)^{2}]-[0]\right) \\  & =2\left(10\right)\end{aligned}
$$


### Generated authored method-bank variant

## q-39345 — easy
Author preview: observed; profile `method`; parameters `{'k': 2}`.

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(1,2)$ to the point $B(3,4),$ then $2\left({\int }_{C}x\,dx+y\,dy\right)=$

- A. $-20$
- B. $20$ **correct**
- C. $8$
- D. $12$
- E. $-4$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=i+2\,j$ and $b=3\,i+4\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =i+2\,j+t(3\,i+4\,j-(i+2\,j)) \\  & =i+2\,j+t(2\,i+2\,j) \\  & =(1+2t)\,i+(2+2t)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=1+2t$ and $y(t)=2+2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=2\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}2\left({\int }_{C}x\,dx+y\,dy\right) & =2\left({\int }_{0}^{1}x\,\frac{\text{d}x}{\text{d}t}\,\text{d}t+y\,\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =2\left({\int }_{0}^{1}(x\frac{\text{d}x}{\text{d}t}+y\frac{\text{d}y}{\text{d}t})dt\right) \\  & =2\left({\int }_{0}^{1}(1+2t)\cdot 2+(2+2t)\cdot 2\,dt\right) \\  & =2\left({\int }_{0}^{1}6+8t\,dt\right) \\  & =2\left({[6t+4{t}^{2}]}_{0}^{1}\right) \\  & =2\left([6(1)+4(1)^{2}]-[0]\right) \\  & =2\left(10\right)\end{aligned}
$$


## Original q-81102

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(0,1)$ to the point $B(2,3),$ then ${\int }_{C}{e}^{x}\,dx-\pi \operatorname{sin}⁡(\frac{\pi y}{2})\,dy=$


Bank: ${e}^{2}-\frac{\pi }{2}$, ${e}^{2}-1$, $e+1$, $e-\frac{\pi }{2}$, ${e}^{2}$


The position vectors of the endpoints of our line segment are $a=j$ and $b=2\,i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =j+t(2\,i+3\,j-j) \\  & =j+t(2\,i+2j) \\  & =2t\,i+(1+2t)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=2t$ and $y(t)=1+2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=2\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_{C}{e}^{x}\,dx-\pi \operatorname{sin}⁡(\frac{\pi y}{2})\,dy & ={\int }_{0}^{1}{e}^{x}\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-\pi \operatorname{sin}⁡(\frac{\pi y}{2})\,\frac{\text{d}y}{\text{d}t}\,dt \\  & ={\int }_{0}^{1}({e}^{x}\,\frac{\text{d}x}{\text{d}t}-\pi \operatorname{sin}⁡(\frac{\pi y}{2})\,\frac{\text{d}y}{\text{d}t})\text{d}t \\  & ={\int }_{0}^{1}{e}^{2t}\cdot 2-\pi \operatorname{sin}⁡(\frac{\pi (1+2t)}{2})\cdot 2\,dt \\  & ={\int }_{0}^{1}(2{e}^{2t}-2\pi \operatorname{sin}⁡(\frac{\pi }{2}+\pi t))dt \\  & ={[{e}^{2t}+2\operatorname{cos}⁡(\frac{\pi }{2}+\pi t)]}_{0}^{1} \\  & =[{e}^{2(1)}+2\operatorname{cos}⁡(\frac{\pi }{2}+\pi (1))]-[{e}^{2(0)}+2\operatorname{cos}⁡(\frac{\pi }{2}+\pi (0))] \\  & =[{e}^{2}+2\operatorname{cos}⁡(\frac{3\pi }{2})]-[1+2\operatorname{cos}⁡(\frac{\pi }{2})] \\  & =[{e}^{2}+0]-[1+0] \\  & ={e}^{2}-1\end{aligned}
$$


### Generated original-parameter replay

## q-81102 — easy
Author preview: observed; profile `q-81102_observed`; parameters `{'k': 1}`.

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(0,1)$ to the point $B(2,3),$ then ${\int }_{C}{e}^{x}\,dx-\pi \operatorname{sin}⁡(\frac{\pi y}{2})\,dy=$

- A. $e+1$
- B. ${e}^{2}-1$ **correct**
- C. ${e}^{2}-\frac{\pi }{2}$
- D. ${e}^{2}$
- E. $e-\frac{\pi }{2}$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=j$ and $b=2\,i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =j+t(2\,i+3\,j-j) \\  & =j+t(2\,i+2j) \\  & =2t\,i+(1+2t)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=2t$ and $y(t)=1+2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=2\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_{C}{e}^{x}\,dx-\pi \operatorname{sin}⁡(\frac{\pi y}{2})\,dy & ={\int }_{0}^{1}{e}^{x}\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-\pi \operatorname{sin}⁡(\frac{\pi y}{2})\,\frac{\text{d}y}{\text{d}t}\,dt \\  & ={\int }_{0}^{1}({e}^{x}\,\frac{\text{d}x}{\text{d}t}-\pi \operatorname{sin}⁡(\frac{\pi y}{2})\,\frac{\text{d}y}{\text{d}t})\text{d}t \\  & ={\int }_{0}^{1}{e}^{2t}\cdot 2-\pi \operatorname{sin}⁡(\frac{\pi (1+2t)}{2})\cdot 2\,dt \\  & ={\int }_{0}^{1}(2{e}^{2t}-2\pi \operatorname{sin}⁡(\frac{\pi }{2}+\pi t))dt \\  & ={[{e}^{2t}+2\operatorname{cos}⁡(\frac{\pi }{2}+\pi t)]}_{0}^{1} \\  & =[{e}^{2(1)}+2\operatorname{cos}⁡(\frac{\pi }{2}+\pi (1))]-[{e}^{2(0)}+2\operatorname{cos}⁡(\frac{\pi }{2}+\pi (0))] \\  & =[{e}^{2}+2\operatorname{cos}⁡(\frac{3\pi }{2})]-[1+2\operatorname{cos}⁡(\frac{\pi }{2})] \\  & =[{e}^{2}+0]-[1+0] \\  & ={e}^{2}-1\end{aligned}
$$


### Generated observed-profile variant (uniform one-form multiplier)

## q-81102 — easy
Author preview: observed; profile `q-81102_observed`; parameters `{'k': -3}`.

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(0,1)$ to the point $B(2,3),$ then $-3\left({\int }_{C}{e}^{x}\,dx-\pi \operatorname{sin}⁡(\frac{\pi y}{2})\,dy\right)=$

- A. $- 3 e + \frac{3 \pi}{2}$
- B. $3 - 3 e^{2}$ **correct**
- C. $- 3 e^{2}$
- D. $- 3 e^{2} + \frac{3 \pi}{2}$
- E. $- 3 e - 3$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=j$ and $b=2\,i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =j+t(2\,i+3\,j-j) \\  & =j+t(2\,i+2j) \\  & =2t\,i+(1+2t)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=2t$ and $y(t)=1+2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=2\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}-3\left({\int }_{C}{e}^{x}\,dx-\pi \operatorname{sin}⁡(\frac{\pi y}{2})\,dy\right) & =-3\left({\int }_{0}^{1}{e}^{x}\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-\pi \operatorname{sin}⁡(\frac{\pi y}{2})\,\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =-3\left({\int }_{0}^{1}({e}^{x}\,\frac{\text{d}x}{\text{d}t}-\pi \operatorname{sin}⁡(\frac{\pi y}{2})\,\frac{\text{d}y}{\text{d}t})\text{d}t\right) \\  & =-3\left({\int }_{0}^{1}{e}^{2t}\cdot 2-\pi \operatorname{sin}⁡(\frac{\pi (1+2t)}{2})\cdot 2\,dt\right) \\  & =-3\left({\int }_{0}^{1}(2{e}^{2t}-2\pi \operatorname{sin}⁡(\frac{\pi }{2}+\pi t))dt\right) \\  & =-3\left({[{e}^{2t}+2\operatorname{cos}⁡(\frac{\pi }{2}+\pi t)]}_{0}^{1}\right) \\  & =-3\left([{e}^{2(1)}+2\operatorname{cos}⁡(\frac{\pi }{2}+\pi (1))]-[{e}^{2(0)}+2\operatorname{cos}⁡(\frac{\pi }{2}+\pi (0))]\right) \\  & =-3\left([{e}^{2}+2\operatorname{cos}⁡(\frac{3\pi }{2})]-[1+2\operatorname{cos}⁡(\frac{\pi }{2})]\right) \\  & =-3\left([{e}^{2}+0]-[1+0]\right) \\  & =-3\left({e}^{2}-1\right)\end{aligned}
$$


### Generated observed-profile variant (uniform one-form multiplier)

## q-81102 — easy
Author preview: observed; profile `q-81102_observed`; parameters `{'k': 2}`.

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(0,1)$ to the point $B(2,3),$ then $2\left({\int }_{C}{e}^{x}\,dx-\pi \operatorname{sin}⁡(\frac{\pi y}{2})\,dy\right)=$

- A. $- \pi + 2 e$
- B. $-2 + 2 e^{2}$ **correct**
- C. $2 e^{2}$
- D. $- \pi + 2 e^{2}$
- E. $2 + 2 e$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=j$ and $b=2\,i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =j+t(2\,i+3\,j-j) \\  & =j+t(2\,i+2j) \\  & =2t\,i+(1+2t)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=2t$ and $y(t)=1+2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=2\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}2\left({\int }_{C}{e}^{x}\,dx-\pi \operatorname{sin}⁡(\frac{\pi y}{2})\,dy\right) & =2\left({\int }_{0}^{1}{e}^{x}\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-\pi \operatorname{sin}⁡(\frac{\pi y}{2})\,\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =2\left({\int }_{0}^{1}({e}^{x}\,\frac{\text{d}x}{\text{d}t}-\pi \operatorname{sin}⁡(\frac{\pi y}{2})\,\frac{\text{d}y}{\text{d}t})\text{d}t\right) \\  & =2\left({\int }_{0}^{1}{e}^{2t}\cdot 2-\pi \operatorname{sin}⁡(\frac{\pi (1+2t)}{2})\cdot 2\,dt\right) \\  & =2\left({\int }_{0}^{1}(2{e}^{2t}-2\pi \operatorname{sin}⁡(\frac{\pi }{2}+\pi t))dt\right) \\  & =2\left({[{e}^{2t}+2\operatorname{cos}⁡(\frac{\pi }{2}+\pi t)]}_{0}^{1}\right) \\  & =2\left([{e}^{2(1)}+2\operatorname{cos}⁡(\frac{\pi }{2}+\pi (1))]-[{e}^{2(0)}+2\operatorname{cos}⁡(\frac{\pi }{2}+\pi (0))]\right) \\  & =2\left([{e}^{2}+2\operatorname{cos}⁡(\frac{3\pi }{2})]-[1+2\operatorname{cos}⁡(\frac{\pi }{2})]\right) \\  & =2\left([{e}^{2}+0]-[1+0]\right) \\  & =2\left({e}^{2}-1\right)\end{aligned}
$$


### Generated authored method-bank variant

## q-81102 — easy
Author preview: observed; profile `method`; parameters `{'k': 2}`.

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(0,1)$ to the point $B(2,3),$ then $2\left({\int }_{C}{e}^{x}\,dx-\pi \operatorname{sin}⁡(\frac{\pi y}{2})\,dy\right)=$

- A. $-2 + 2 e$
- B. $-2 + 2 e^{2}$ **correct**
- C. $2 - 2 e^{2}$
- D. $2 e^{2}$
- E. $-1 + e^{2}$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=j$ and $b=2\,i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =j+t(2\,i+3\,j-j) \\  & =j+t(2\,i+2j) \\  & =2t\,i+(1+2t)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=2t$ and $y(t)=1+2t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=2\,i+2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}2\left({\int }_{C}{e}^{x}\,dx-\pi \operatorname{sin}⁡(\frac{\pi y}{2})\,dy\right) & =2\left({\int }_{0}^{1}{e}^{x}\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-\pi \operatorname{sin}⁡(\frac{\pi y}{2})\,\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =2\left({\int }_{0}^{1}({e}^{x}\,\frac{\text{d}x}{\text{d}t}-\pi \operatorname{sin}⁡(\frac{\pi y}{2})\,\frac{\text{d}y}{\text{d}t})\text{d}t\right) \\  & =2\left({\int }_{0}^{1}{e}^{2t}\cdot 2-\pi \operatorname{sin}⁡(\frac{\pi (1+2t)}{2})\cdot 2\,dt\right) \\  & =2\left({\int }_{0}^{1}(2{e}^{2t}-2\pi \operatorname{sin}⁡(\frac{\pi }{2}+\pi t))dt\right) \\  & =2\left({[{e}^{2t}+2\operatorname{cos}⁡(\frac{\pi }{2}+\pi t)]}_{0}^{1}\right) \\  & =2\left([{e}^{2(1)}+2\operatorname{cos}⁡(\frac{\pi }{2}+\pi (1))]-[{e}^{2(0)}+2\operatorname{cos}⁡(\frac{\pi }{2}+\pi (0))]\right) \\  & =2\left([{e}^{2}+2\operatorname{cos}⁡(\frac{3\pi }{2})]-[1+2\operatorname{cos}⁡(\frac{\pi }{2})]\right) \\  & =2\left([{e}^{2}+0]-[1+0]\right) \\  & =2\left({e}^{2}-1\right)\end{aligned}
$$


## Original q-124660

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(0,0)$ to the point $B(1,1),$ then ${\int }_{C}\operatorname{sin}⁡\pi y\,dx-\operatorname{cos}⁡\pi x\,dy=$


Bank: $\frac{2}{\pi }$, $\frac{1}{\pi }$, $2\pi $, $\pi $, $\frac{\pi }{2}$


The position vectors of the endpoints of our line segment are $a=0\,i+0\,j$ and $b=i+j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =0\,i+0\,j+t(i+j-(0\,i+0\,j)) \\  & =t\,i+t\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=t$ and $y(t)=t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=i+j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_{C}\operatorname{sin}⁡\pi y\,dx-\operatorname{cos}⁡\pi x\,dy & ={\int }_{0}^{1}\operatorname{sin}⁡\pi y\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-\operatorname{cos}⁡\pi x\,\frac{\text{d}y}{\text{d}t}\,dt \\  & ={\int }_{0}^{1}(\operatorname{sin}⁡\pi y\,\frac{\text{d}x}{\text{d}t}-\operatorname{cos}⁡\pi x\,\frac{\text{d}y}{\text{d}t})dt \\  & ={\int }_{0}^{1}\operatorname{sin}⁡\pi t\cdot 1-\operatorname{cos}⁡\pi t\cdot 1\,dt \\  & ={\int }_{0}^{1}\operatorname{sin}⁡\pi t-\operatorname{cos}⁡\pi t\,dt \\  & ={[-\frac{\operatorname{cos}⁡\pi t}{\pi }-\frac{\operatorname{sin}⁡\pi t}{\pi }]}_{0}^{1} \\  & =-\frac{1}{\pi }[\operatorname{cos}⁡(\pi )+\operatorname{sin}⁡(\pi )-\operatorname{cos}⁡(0)-\operatorname{sin}⁡(0)] \\  & =-\frac{1}{\pi }[-1+0-1-0] \\  & =\frac{2}{\pi }\end{aligned}
$$


### Generated original-parameter replay

## q-124660 — easy
Author preview: observed; profile `q-124660_observed`; parameters `{'k': 1}`.

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(0,0)$ to the point $B(1,1),$ then ${\int }_{C}\operatorname{sin}⁡\pi y\,dx-\operatorname{cos}⁡\pi x\,dy=$

- A. $2\pi $
- B. $\frac{1}{\pi }$
- C. $\frac{2}{\pi }$ **correct**
- D. $\frac{\pi }{2}$
- E. $\pi $

**Worked solution**

The position vectors of the endpoints of our line segment are $a=0\,i+0\,j$ and $b=i+j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =0\,i+0\,j+t(i+j-(0\,i+0\,j)) \\  & =t\,i+t\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=t$ and $y(t)=t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=i+j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_{C}\operatorname{sin}⁡\pi y\,dx-\operatorname{cos}⁡\pi x\,dy & ={\int }_{0}^{1}\operatorname{sin}⁡\pi y\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-\operatorname{cos}⁡\pi x\,\frac{\text{d}y}{\text{d}t}\,dt \\  & ={\int }_{0}^{1}(\operatorname{sin}⁡\pi y\,\frac{\text{d}x}{\text{d}t}-\operatorname{cos}⁡\pi x\,\frac{\text{d}y}{\text{d}t})dt \\  & ={\int }_{0}^{1}\operatorname{sin}⁡\pi t\cdot 1-\operatorname{cos}⁡\pi t\cdot 1\,dt \\  & ={\int }_{0}^{1}\operatorname{sin}⁡\pi t-\operatorname{cos}⁡\pi t\,dt \\  & ={[-\frac{\operatorname{cos}⁡\pi t}{\pi }-\frac{\operatorname{sin}⁡\pi t}{\pi }]}_{0}^{1} \\  & =-\frac{1}{\pi }[\operatorname{cos}⁡(\pi )+\operatorname{sin}⁡(\pi )-\operatorname{cos}⁡(0)-\operatorname{sin}⁡(0)] \\  & =-\frac{1}{\pi }[-1+0-1-0] \\  & =\frac{2}{\pi }\end{aligned}
$$


### Generated observed-profile variant (uniform one-form multiplier)

## q-124660 — easy
Author preview: observed; profile `q-124660_observed`; parameters `{'k': -3}`.

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(0,0)$ to the point $B(1,1),$ then $-3\left({\int }_{C}\operatorname{sin}⁡\pi y\,dx-\operatorname{cos}⁡\pi x\,dy\right)=$

- A. $- 3 \pi$
- B. $- \frac{3}{\pi}$
- C. $- \frac{3 \pi}{2}$
- D. $- \frac{6}{\pi}$ **correct**
- E. $- 6 \pi$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=0\,i+0\,j$ and $b=i+j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =0\,i+0\,j+t(i+j-(0\,i+0\,j)) \\  & =t\,i+t\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=t$ and $y(t)=t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=i+j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}-3\left({\int }_{C}\operatorname{sin}⁡\pi y\,dx-\operatorname{cos}⁡\pi x\,dy\right) & =-3\left({\int }_{0}^{1}\operatorname{sin}⁡\pi y\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-\operatorname{cos}⁡\pi x\,\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =-3\left({\int }_{0}^{1}(\operatorname{sin}⁡\pi y\,\frac{\text{d}x}{\text{d}t}-\operatorname{cos}⁡\pi x\,\frac{\text{d}y}{\text{d}t})dt\right) \\  & =-3\left({\int }_{0}^{1}\operatorname{sin}⁡\pi t\cdot 1-\operatorname{cos}⁡\pi t\cdot 1\,dt\right) \\  & =-3\left({\int }_{0}^{1}\operatorname{sin}⁡\pi t-\operatorname{cos}⁡\pi t\,dt\right) \\  & =-3\left({[-\frac{\operatorname{cos}⁡\pi t}{\pi }-\frac{\operatorname{sin}⁡\pi t}{\pi }]}_{0}^{1}\right) \\  & =-3\left(-\frac{1}{\pi }[\operatorname{cos}⁡(\pi )+\operatorname{sin}⁡(\pi )-\operatorname{cos}⁡(0)-\operatorname{sin}⁡(0)]\right) \\  & =-3\left(-\frac{1}{\pi }[-1+0-1-0]\right) \\  & =-3\left(\frac{2}{\pi }\right)\end{aligned}
$$


### Generated observed-profile variant (uniform one-form multiplier)

## q-124660 — easy
Author preview: observed; profile `q-124660_observed`; parameters `{'k': 2}`.

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(0,0)$ to the point $B(1,1),$ then $2\left({\int }_{C}\operatorname{sin}⁡\pi y\,dx-\operatorname{cos}⁡\pi x\,dy\right)=$

- A. $2 \pi$
- B. $\frac{2}{\pi}$
- C. $\pi$
- D. $\frac{4}{\pi}$ **correct**
- E. $4 \pi$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=0\,i+0\,j$ and $b=i+j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =0\,i+0\,j+t(i+j-(0\,i+0\,j)) \\  & =t\,i+t\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=t$ and $y(t)=t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=i+j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}2\left({\int }_{C}\operatorname{sin}⁡\pi y\,dx-\operatorname{cos}⁡\pi x\,dy\right) & =2\left({\int }_{0}^{1}\operatorname{sin}⁡\pi y\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-\operatorname{cos}⁡\pi x\,\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =2\left({\int }_{0}^{1}(\operatorname{sin}⁡\pi y\,\frac{\text{d}x}{\text{d}t}-\operatorname{cos}⁡\pi x\,\frac{\text{d}y}{\text{d}t})dt\right) \\  & =2\left({\int }_{0}^{1}\operatorname{sin}⁡\pi t\cdot 1-\operatorname{cos}⁡\pi t\cdot 1\,dt\right) \\  & =2\left({\int }_{0}^{1}\operatorname{sin}⁡\pi t-\operatorname{cos}⁡\pi t\,dt\right) \\  & =2\left({[-\frac{\operatorname{cos}⁡\pi t}{\pi }-\frac{\operatorname{sin}⁡\pi t}{\pi }]}_{0}^{1}\right) \\  & =2\left(-\frac{1}{\pi }[\operatorname{cos}⁡(\pi )+\operatorname{sin}⁡(\pi )-\operatorname{cos}⁡(0)-\operatorname{sin}⁡(0)]\right) \\  & =2\left(-\frac{1}{\pi }[-1+0-1-0]\right) \\  & =2\left(\frac{2}{\pi }\right)\end{aligned}
$$


### Generated authored method-bank variant

## q-124660 — easy
Author preview: observed; profile `method`; parameters `{'k': 2}`.

If the path $C$ is the line segment $\overset{―}{AB}$ traversed from the point $A(0,0)$ to the point $B(1,1),$ then $2\left({\int }_{C}\operatorname{sin}⁡\pi y\,dx-\operatorname{cos}⁡\pi x\,dy\right)=$

- A. $\frac{2}{\pi}$
- B. $\frac{4}{\pi}$ **correct**
- C. $- \frac{4}{\pi}$
- D. $4$
- E. $4 \pi$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=0\,i+0\,j$ and $b=i+j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =0\,i+0\,j+t(i+j-(0\,i+0\,j)) \\  & =t\,i+t\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=t$ and $y(t)=t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=i+j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}2\left({\int }_{C}\operatorname{sin}⁡\pi y\,dx-\operatorname{cos}⁡\pi x\,dy\right) & =2\left({\int }_{0}^{1}\operatorname{sin}⁡\pi y\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-\operatorname{cos}⁡\pi x\,\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =2\left({\int }_{0}^{1}(\operatorname{sin}⁡\pi y\,\frac{\text{d}x}{\text{d}t}-\operatorname{cos}⁡\pi x\,\frac{\text{d}y}{\text{d}t})dt\right) \\  & =2\left({\int }_{0}^{1}\operatorname{sin}⁡\pi t\cdot 1-\operatorname{cos}⁡\pi t\cdot 1\,dt\right) \\  & =2\left({\int }_{0}^{1}\operatorname{sin}⁡\pi t-\operatorname{cos}⁡\pi t\,dt\right) \\  & =2\left({[-\frac{\operatorname{cos}⁡\pi t}{\pi }-\frac{\operatorname{sin}⁡\pi t}{\pi }]}_{0}^{1}\right) \\  & =2\left(-\frac{1}{\pi }[\operatorname{cos}⁡(\pi )+\operatorname{sin}⁡(\pi )-\operatorname{cos}⁡(0)-\operatorname{sin}⁡(0)]\right) \\  & =2\left(-\frac{1}{\pi }[-1+0-1-0]\right) \\  & =2\left(\frac{2}{\pi }\right)\end{aligned}
$$


## Original q-90714

If the path $C$ is the line segment $\overset{―}{FG}$ traversed from the point $F(1,0)$ to the point $G(2,3),$ then ${\int }_{C}x\,dx-xy\,dy=$


Bank: $-8$, $-6$, $6$, $-9$, $5$


The position vectors of the endpoints of our line segment are $a=i$ and $b=2\,i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =i+t(2\,i+3\,j-i) \\  & =i+t(i+3\,j) \\  & =(1+t)\,i+3t\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=1+t$ and $y(t)=3t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=i+3\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_{C}x\,dx-xy\,dy & ={\int }_{0}^{1}x\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-xy\,\frac{\text{d}y}{\text{d}t}\,dt \\  & ={\int }_{0}^{1}(x\,\frac{\text{d}x}{\text{d}t}-xy\,\frac{\text{d}y}{\text{d}t})\text{d}t \\  & ={\int }_{0}^{1}(1+t)\cdot 1-(1+t)\cdot 3t\cdot 3\,dt \\  & ={\int }_{0}^{1}1-8t-9{t}^{2}\,dt \\  & ={[t-4{t}^{2}-3{t}^{3}]}_{0}^{1} \\  & =[1-4(1)^{2}-3(1)^{3}]-[0] \\  & =-6\end{aligned}
$$


### Generated original-parameter replay

## q-90714 — easy
Author preview: observed; profile `q-90714_observed`; parameters `{'k': 1}`.

If the path $C$ is the line segment $\overset{―}{FG}$ traversed from the point $F(1,0)$ to the point $G(2,3),$ then ${\int }_{C}x\,dx-xy\,dy=$

- A. $6$
- B. $-6$ **correct**
- C. $-8$
- D. $5$
- E. $-9$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=i$ and $b=2\,i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =i+t(2\,i+3\,j-i) \\  & =i+t(i+3\,j) \\  & =(1+t)\,i+3t\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=1+t$ and $y(t)=3t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=i+3\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_{C}x\,dx-xy\,dy & ={\int }_{0}^{1}x\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-xy\,\frac{\text{d}y}{\text{d}t}\,dt \\  & ={\int }_{0}^{1}(x\,\frac{\text{d}x}{\text{d}t}-xy\,\frac{\text{d}y}{\text{d}t})\text{d}t \\  & ={\int }_{0}^{1}(1+t)\cdot 1-(1+t)\cdot 3t\cdot 3\,dt \\  & ={\int }_{0}^{1}1-8t-9{t}^{2}\,dt \\  & ={[t-4{t}^{2}-3{t}^{3}]}_{0}^{1} \\  & =[1-4(1)^{2}-3(1)^{3}]-[0] \\  & =-6\end{aligned}
$$


### Generated observed-profile variant (uniform one-form multiplier)

## q-90714 — easy
Author preview: observed; profile `q-90714_observed`; parameters `{'k': -3}`.

If the path $C$ is the line segment $\overset{―}{FG}$ traversed from the point $F(1,0)$ to the point $G(2,3),$ then $-3\left({\int }_{C}x\,dx-xy\,dy\right)=$

- A. $27$
- B. $18$ **correct**
- C. $-15$
- D. $24$
- E. $-18$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=i$ and $b=2\,i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =i+t(2\,i+3\,j-i) \\  & =i+t(i+3\,j) \\  & =(1+t)\,i+3t\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=1+t$ and $y(t)=3t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=i+3\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}-3\left({\int }_{C}x\,dx-xy\,dy\right) & =-3\left({\int }_{0}^{1}x\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-xy\,\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =-3\left({\int }_{0}^{1}(x\,\frac{\text{d}x}{\text{d}t}-xy\,\frac{\text{d}y}{\text{d}t})\text{d}t\right) \\  & =-3\left({\int }_{0}^{1}(1+t)\cdot 1-(1+t)\cdot 3t\cdot 3\,dt\right) \\  & =-3\left({\int }_{0}^{1}1-8t-9{t}^{2}\,dt\right) \\  & =-3\left({[t-4{t}^{2}-3{t}^{3}]}_{0}^{1}\right) \\  & =-3\left([1-4(1)^{2}-3(1)^{3}]-[0]\right) \\  & =-3\left(-6\right)\end{aligned}
$$


### Generated observed-profile variant (uniform one-form multiplier)

## q-90714 — easy
Author preview: observed; profile `q-90714_observed`; parameters `{'k': 2}`.

If the path $C$ is the line segment $\overset{―}{FG}$ traversed from the point $F(1,0)$ to the point $G(2,3),$ then $2\left({\int }_{C}x\,dx-xy\,dy\right)=$

- A. $-18$
- B. $-12$ **correct**
- C. $10$
- D. $-16$
- E. $12$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=i$ and $b=2\,i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =i+t(2\,i+3\,j-i) \\  & =i+t(i+3\,j) \\  & =(1+t)\,i+3t\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=1+t$ and $y(t)=3t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=i+3\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}2\left({\int }_{C}x\,dx-xy\,dy\right) & =2\left({\int }_{0}^{1}x\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-xy\,\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =2\left({\int }_{0}^{1}(x\,\frac{\text{d}x}{\text{d}t}-xy\,\frac{\text{d}y}{\text{d}t})\text{d}t\right) \\  & =2\left({\int }_{0}^{1}(1+t)\cdot 1-(1+t)\cdot 3t\cdot 3\,dt\right) \\  & =2\left({\int }_{0}^{1}1-8t-9{t}^{2}\,dt\right) \\  & =2\left({[t-4{t}^{2}-3{t}^{3}]}_{0}^{1}\right) \\  & =2\left([1-4(1)^{2}-3(1)^{3}]-[0]\right) \\  & =2\left(-6\right)\end{aligned}
$$


### Generated authored method-bank variant

## q-90714 — easy
Author preview: observed; profile `method`; parameters `{'k': 2}`.

If the path $C$ is the line segment $\overset{―}{FG}$ traversed from the point $F(1,0)$ to the point $G(2,3),$ then $2\left({\int }_{C}x\,dx-xy\,dy\right)=$

- A. $12$
- B. $-12$ **correct**
- C. $3$
- D. $-15$
- E. $18$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=i$ and $b=2\,i+3\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\  & =i+t(2\,i+3\,j-i) \\  & =i+t(i+3\,j) \\  & =(1+t)\,i+3t\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=1+t$ and $y(t)=3t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=i+3\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}2\left({\int }_{C}x\,dx-xy\,dy\right) & =2\left({\int }_{0}^{1}x\,\frac{\text{d}x}{\text{d}t}\,\text{d}t-xy\,\frac{\text{d}y}{\text{d}t}\,dt\right) \\  & =2\left({\int }_{0}^{1}(x\,\frac{\text{d}x}{\text{d}t}-xy\,\frac{\text{d}y}{\text{d}t})\text{d}t\right) \\  & =2\left({\int }_{0}^{1}(1+t)\cdot 1-(1+t)\cdot 3t\cdot 3\,dt\right) \\  & =2\left({\int }_{0}^{1}1-8t-9{t}^{2}\,dt\right) \\  & =2\left({[t-4{t}^{2}-3{t}^{3}]}_{0}^{1}\right) \\  & =2\left([1-4(1)^{2}-3(1)^{3}]-[0]\right) \\  & =2\left(-6\right)\end{aligned}
$$


### Generated authored easy example

## easy_linear — easy
Author preview: authored; profile `method`; parameters `{'x0': 2, 'y0': 0, 'x1': 3, 'y1': 1, 'a': 2, 'b': -2}`.

If the path $C$ is the line segment $\overline{AB}$ traversed from the point $A(2,0)$ to the point $B(3,1),$ then ${\int }_C \left(2 x\right)\,dx+\left(- 2 y\right)\,dy=$

- A. $-1$
- B. $4$ **correct**
- C. $6$
- D. $5$
- E. $-4$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=2\,i$ and $b=3\,i+j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =2\,i+t\left(3\,i+j-\left(2\,i\right)\right) \\   & =2\,i+t\left(i+j\right) \\   & =\left(t + 2\right)\,i+\left(t\right)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=t + 2$ and $y(t)=t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=i+j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_C \left(2 x\right)\,dx+\left(- 2 y\right)\,dy & ={\int }_{0}^{1}\left(2 x\right)\frac{\text{d}x}{\text{d}t}+\left(- 2 y\right)\frac{\text{d}y}{\text{d}t}\,dt \\   & ={\int }_{0}^{1}\left(\left(2 x\right)\frac{\text{d}x}{\text{d}t}+\left(- 2 y\right)\frac{\text{d}y}{\text{d}t}\right)\,dt \\   & ={\int }_{0}^{1}\left(2\right)\cdot \left(t + 2\right)\cdot \left(1\right)+\left(-2\right)\cdot \left(t\right)\cdot \left(1\right)\,dt \\   & ={\int }_{0}^{1}\left(2 t + 4\right)+\left(- 2 t\right)\,dt \\   & ={\int }_{0}^{1}4\,dt \\   & =\left[4 t\right]_0^1 \\   & =\left(4 \left(1\right)\right)-\left(4 \left(0\right)\right) \\   & =\left(\left(4\right)\right)-\left(\left(0\right)\right) \\   & =4\end{aligned}
$$


### Generated authored easy example

## easy_linear — easy
Author preview: authored; profile `method`; parameters `{'x0': 4, 'y0': -4, 'x1': 2, 'y1': -1, 'a': 1, 'b': 3}`.

If the path $C$ is the line segment $\overline{AB}$ traversed from the point $A(4,-4)$ to the point $B(2,-1),$ then ${\int }_C \left(x\right)\,dx+\left(3 y\right)\,dy=$

- A. $\frac{57}{2}$
- B. $- \frac{45}{2}$
- C. $\frac{33}{2}$
- D. $-6$
- E. $- \frac{57}{2}$ **correct**

**Worked solution**

The position vectors of the endpoints of our line segment are $a=4\,i-4\,j$ and $b=2\,i-j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =4\,i-4\,j+t\left(2\,i-j-\left(4\,i-4\,j\right)\right) \\   & =4\,i-4\,j+t\left(-2\,i+3\,j\right) \\   & =\left(4 - 2 t\right)\,i+\left(3 t - 4\right)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=4 - 2 t$ and $y(t)=3 t - 4$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-2\,i+3\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_C \left(x\right)\,dx+\left(3 y\right)\,dy & ={\int }_{0}^{1}\left(x\right)\frac{\text{d}x}{\text{d}t}+\left(3 y\right)\frac{\text{d}y}{\text{d}t}\,dt \\   & ={\int }_{0}^{1}\left(\left(x\right)\frac{\text{d}x}{\text{d}t}+\left(3 y\right)\frac{\text{d}y}{\text{d}t}\right)\,dt \\   & ={\int }_{0}^{1}\left(1\right)\cdot \left(4 - 2 t\right)\cdot \left(-2\right)+\left(3\right)\cdot \left(3 t - 4\right)\cdot \left(3\right)\,dt \\   & ={\int }_{0}^{1}\left(4 t - 8\right)+\left(27 t - 36\right)\,dt \\   & ={\int }_{0}^{1}31 t - 44\,dt \\   & =\left[\frac{31 t^{2}}{2} - 44 t\right]_0^1 \\   & =\left(\frac{31 \left(1\right)^{2}}{2} - 44 \left(1\right)\right)-\left(\frac{31 \left(0\right)^{2}}{2} - 44 \left(0\right)\right) \\   & =\left(\left(\frac{31}{2}\right)+\left(-44\right)\right)-\left(\left(0\right)+\left(0\right)\right) \\   & =- \frac{57}{2}\end{aligned}
$$


### Generated authored easy example

## easy_product — easy
Author preview: authored; profile `method`; parameters `{'x0': 2, 'y0': 0, 'x1': 3, 'y1': 1, 'a': 2, 'b': -2}`.

If the path $C$ is the line segment $\overline{AB}$ traversed from the point $A(2,0)$ to the point $B(3,1),$ then ${\int }_C \left(2 x\right)\,dx+\left(- 2 x y\right)\,dy=$

- A. $- \frac{8}{3}$
- B. $\frac{7}{3}$ **correct**
- C. $\frac{23}{3}$
- D. $5$
- E. $- \frac{7}{3}$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=2\,i$ and $b=3\,i+j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =2\,i+t\left(3\,i+j-\left(2\,i\right)\right) \\   & =2\,i+t\left(i+j\right) \\   & =\left(t + 2\right)\,i+\left(t\right)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=t + 2$ and $y(t)=t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=i+j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_C \left(2 x\right)\,dx+\left(- 2 x y\right)\,dy & ={\int }_{0}^{1}\left(2 x\right)\frac{\text{d}x}{\text{d}t}+\left(- 2 x y\right)\frac{\text{d}y}{\text{d}t}\,dt \\   & ={\int }_{0}^{1}\left(\left(2 x\right)\frac{\text{d}x}{\text{d}t}+\left(- 2 x y\right)\frac{\text{d}y}{\text{d}t}\right)\,dt \\   & ={\int }_{0}^{1}\left(2\right)\cdot \left(t + 2\right)\cdot \left(1\right)+\left(-2\right)\cdot \left(t + 2\right)\cdot \left(t\right)\cdot \left(1\right)\,dt \\   & ={\int }_{0}^{1}\left(2 t + 4\right)+\left(- 2 t^{2} - 4 t\right)\,dt \\   & ={\int }_{0}^{1}- 2 t^{2} - 2 t + 4\,dt \\   & =\left[- \frac{2 t^{3}}{3} - t^{2} + 4 t\right]_0^1 \\   & =\left(- \frac{2 \left(1\right)^{3}}{3} - \left(1\right)^{2} + 4 \left(1\right)\right)-\left(- \frac{2 \left(0\right)^{3}}{3} - \left(0\right)^{2} + 4 \left(0\right)\right) \\   & =\left(\left(- \frac{2}{3}\right)+\left(-1\right)+\left(4\right)\right)-\left(\left(0\right)+\left(0\right)+\left(0\right)\right) \\   & =\frac{7}{3}\end{aligned}
$$


### Generated authored easy example

## easy_product — easy
Author preview: authored; profile `method`; parameters `{'x0': 4, 'y0': -4, 'x1': 2, 'y1': -1, 'a': 1, 'b': 3}`.

If the path $C$ is the line segment $\overline{AB}$ traversed from the point $A(4,-4)$ to the point $B(2,-1),$ then ${\int }_C \left(x\right)\,dx+\left(3 x y\right)\,dy=$

- A. $78$
- B. $-72$
- C. $66$
- D. $-6$
- E. $-78$ **correct**

**Worked solution**

The position vectors of the endpoints of our line segment are $a=4\,i-4\,j$ and $b=2\,i-j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =4\,i-4\,j+t\left(2\,i-j-\left(4\,i-4\,j\right)\right) \\   & =4\,i-4\,j+t\left(-2\,i+3\,j\right) \\   & =\left(4 - 2 t\right)\,i+\left(3 t - 4\right)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=4 - 2 t$ and $y(t)=3 t - 4$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-2\,i+3\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_C \left(x\right)\,dx+\left(3 x y\right)\,dy & ={\int }_{0}^{1}\left(x\right)\frac{\text{d}x}{\text{d}t}+\left(3 x y\right)\frac{\text{d}y}{\text{d}t}\,dt \\   & ={\int }_{0}^{1}\left(\left(x\right)\frac{\text{d}x}{\text{d}t}+\left(3 x y\right)\frac{\text{d}y}{\text{d}t}\right)\,dt \\   & ={\int }_{0}^{1}\left(1\right)\cdot \left(4 - 2 t\right)\cdot \left(-2\right)+\left(3\right)\cdot \left(4 - 2 t\right)\cdot \left(3 t - 4\right)\cdot \left(3\right)\,dt \\   & ={\int }_{0}^{1}\left(4 t - 8\right)+\left(- 54 t^{2} + 180 t - 144\right)\,dt \\   & ={\int }_{0}^{1}- 54 t^{2} + 184 t - 152\,dt \\   & =\left[- 18 t^{3} + 92 t^{2} - 152 t\right]_0^1 \\   & =\left(- 18 \left(1\right)^{3} + 92 \left(1\right)^{2} - 152 \left(1\right)\right)-\left(- 18 \left(0\right)^{3} + 92 \left(0\right)^{2} - 152 \left(0\right)\right) \\   & =\left(\left(-18\right)+\left(92\right)+\left(-152\right)\right)-\left(\left(0\right)+\left(0\right)+\left(0\right)\right) \\   & =-78\end{aligned}
$$


### Generated authored moderate example

## moderate_canonical — moderate
Author preview: authored; profile `method`; parameters `{'x0': 2, 'y0': 1, 'x1': -1, 'y1': 4, 'a': 1, 'b': 1}`.

If the path $C$ is the line segment $\overline{AB}$ traversed from the point $A(2,1)$ to the point $B(-1,4),$ then ${\int }_C \left(x^{2} y\right)\,dx+\left(x y\right)\,dy=$

- A. $- \frac{21}{4}$
- B. $- \frac{27}{4}$
- C. $- \frac{15}{4}$ **correct**
- D. $\frac{3}{2}$
- E. $\frac{15}{4}$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=2\,i+j$ and $b=-i+4\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =2\,i+j+t\left(-i+4\,j-\left(2\,i+j\right)\right) \\   & =2\,i+j+t\left(-3\,i+3\,j\right) \\   & =\left(2 - 3 t\right)\,i+\left(3 t + 1\right)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=2 - 3 t$ and $y(t)=3 t + 1$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-3\,i+3\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_C \left(x^{2} y\right)\,dx+\left(x y\right)\,dy & ={\int }_{0}^{1}\left(x^{2} y\right)\frac{\text{d}x}{\text{d}t}+\left(x y\right)\frac{\text{d}y}{\text{d}t}\,dt \\   & ={\int }_{0}^{1}\left(\left(x^{2} y\right)\frac{\text{d}x}{\text{d}t}+\left(x y\right)\frac{\text{d}y}{\text{d}t}\right)\,dt \\   & ={\int }_{0}^{1}\left(1\right)\cdot \left(2 - 3 t\right)^{2}\cdot \left(3 t + 1\right)\cdot \left(-3\right)+\left(1\right)\cdot \left(2 - 3 t\right)\cdot \left(3 t + 1\right)\cdot \left(3\right)\,dt \\   & ={\int }_{0}^{1}\left(- 81 t^{3} + 81 t^{2} - 12\right)+\left(- 27 t^{2} + 9 t + 6\right)\,dt \\   & ={\int }_{0}^{1}- 81 t^{3} + 54 t^{2} + 9 t - 6\,dt \\   & =\left[- \frac{81 t^{4}}{4} + 18 t^{3} + \frac{9 t^{2}}{2} - 6 t\right]_0^1 \\   & =\left(- \frac{81 \left(1\right)^{4}}{4} + 18 \left(1\right)^{3} + \frac{9 \left(1\right)^{2}}{2} - 6 \left(1\right)\right)-\left(- \frac{81 \left(0\right)^{4}}{4} + 18 \left(0\right)^{3} + \frac{9 \left(0\right)^{2}}{2} - 6 \left(0\right)\right) \\   & =\left(\left(- \frac{81}{4}\right)+\left(18\right)+\left(\frac{9}{2}\right)+\left(-6\right)\right)-\left(\left(0\right)+\left(0\right)+\left(0\right)+\left(0\right)\right) \\   & =- \frac{15}{4}\end{aligned}
$$


### Generated authored moderate example

## moderate_canonical — moderate
Author preview: authored; profile `method`; parameters `{'x0': -1, 'y0': -3, 'x1': 1, 'y1': -4, 'a': -3, 'b': -3}`.

If the path $C$ is the line segment $\overline{AB}$ traversed from the point $A(-1,-3)$ to the point $B(1,-4),$ then ${\int }_C \left(- 3 x^{2} y\right)\,dx+\left(- 3 x y\right)\,dy=$

- A. $- \frac{1}{2}$
- B. $\frac{15}{2}$
- C. $7$
- D. $\frac{13}{2}$ **correct**
- E. $- \frac{13}{2}$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=-i-3\,j$ and $b=i-4\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =-i-3\,j+t\left(i-4\,j-\left(-i-3\,j\right)\right) \\   & =-i-3\,j+t\left(2\,i-j\right) \\   & =\left(2 t - 1\right)\,i+\left(- t - 3\right)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=2 t - 1$ and $y(t)=- t - 3$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=2\,i-j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_C \left(- 3 x^{2} y\right)\,dx+\left(- 3 x y\right)\,dy & ={\int }_{0}^{1}\left(- 3 x^{2} y\right)\frac{\text{d}x}{\text{d}t}+\left(- 3 x y\right)\frac{\text{d}y}{\text{d}t}\,dt \\   & ={\int }_{0}^{1}\left(\left(- 3 x^{2} y\right)\frac{\text{d}x}{\text{d}t}+\left(- 3 x y\right)\frac{\text{d}y}{\text{d}t}\right)\,dt \\   & ={\int }_{0}^{1}\left(-3\right)\cdot \left(2 t - 1\right)^{2}\cdot \left(- t - 3\right)\cdot \left(2\right)+\left(-3\right)\cdot \left(2 t - 1\right)\cdot \left(- t - 3\right)\cdot \left(-1\right)\,dt \\   & ={\int }_{0}^{1}\left(24 t^{3} + 48 t^{2} - 66 t + 18\right)+\left(- 6 t^{2} - 15 t + 9\right)\,dt \\   & ={\int }_{0}^{1}24 t^{3} + 42 t^{2} - 81 t + 27\,dt \\   & =\left[6 t^{4} + 14 t^{3} - \frac{81 t^{2}}{2} + 27 t\right]_0^1 \\   & =\left(6 \left(1\right)^{4} + 14 \left(1\right)^{3} - \frac{81 \left(1\right)^{2}}{2} + 27 \left(1\right)\right)-\left(6 \left(0\right)^{4} + 14 \left(0\right)^{3} - \frac{81 \left(0\right)^{2}}{2} + 27 \left(0\right)\right) \\   & =\left(\left(6\right)+\left(14\right)+\left(- \frac{81}{2}\right)+\left(27\right)\right)-\left(\left(0\right)+\left(0\right)+\left(0\right)+\left(0\right)\right) \\   & =\frac{13}{2}\end{aligned}
$$


### Generated authored hard example

## hard_coupled — hard
Author preview: authored; profile `method`; parameters `{'x0': -2, 'y0': 3, 'x1': -3, 'y1': 1, 'a': -1, 'b': 2}`.

If the path $C$ is the line segment $\overline{AB}$ traversed from the point $A(-2,3)$ to the point $B(-3,1),$ then ${\int }_C \left(- x^{2} y\right)\,dx+\left(2 x y^{2}\right)\,dy=$

- A. $\frac{122}{3}$
- B. $\frac{105}{2}$ **correct**
- C. $- \frac{173}{6}$
- D. $\frac{71}{6}$
- E. $- \frac{105}{2}$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=-2\,i+3\,j$ and $b=-3\,i+j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =-2\,i+3\,j+t\left(-3\,i+j-\left(-2\,i+3\,j\right)\right) \\   & =-2\,i+3\,j+t\left(-i-2\,j\right) \\   & =\left(- t - 2\right)\,i+\left(3 - 2 t\right)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=- t - 2$ and $y(t)=3 - 2 t$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-i-2\,j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_C \left(- x^{2} y\right)\,dx+\left(2 x y^{2}\right)\,dy & ={\int }_{0}^{1}\left(- x^{2} y\right)\frac{\text{d}x}{\text{d}t}+\left(2 x y^{2}\right)\frac{\text{d}y}{\text{d}t}\,dt \\   & ={\int }_{0}^{1}\left(\left(- x^{2} y\right)\frac{\text{d}x}{\text{d}t}+\left(2 x y^{2}\right)\frac{\text{d}y}{\text{d}t}\right)\,dt \\   & ={\int }_{0}^{1}\left(-1\right)\cdot \left(- t - 2\right)^{2}\cdot \left(3 - 2 t\right)\cdot \left(-1\right)+\left(2\right)\cdot \left(- t - 2\right)\cdot \left(3 - 2 t\right)^{2}\cdot \left(-2\right)\,dt \\   & ={\int }_{0}^{1}\left(- 2 t^{3} - 5 t^{2} + 4 t + 12\right)+\left(16 t^{3} - 16 t^{2} - 60 t + 72\right)\,dt \\   & ={\int }_{0}^{1}14 t^{3} - 21 t^{2} - 56 t + 84\,dt \\   & =\left[\frac{7 t^{4}}{2} - 7 t^{3} - 28 t^{2} + 84 t\right]_0^1 \\   & =\left(\frac{7 \left(1\right)^{4}}{2} - 7 \left(1\right)^{3} - 28 \left(1\right)^{2} + 84 \left(1\right)\right)-\left(\frac{7 \left(0\right)^{4}}{2} - 7 \left(0\right)^{3} - 28 \left(0\right)^{2} + 84 \left(0\right)\right) \\   & =\left(\left(\frac{7}{2}\right)+\left(-7\right)+\left(-28\right)+\left(84\right)\right)-\left(\left(0\right)+\left(0\right)+\left(0\right)+\left(0\right)\right) \\   & =\frac{105}{2}\end{aligned}
$$


### Generated authored hard example

## hard_coupled — hard
Author preview: authored; profile `method`; parameters `{'x0': 2, 'y0': -3, 'x1': 1, 'y1': -2, 'a': 1, 'b': 1}`.

If the path $C$ is the line segment $\overline{AB}$ traversed from the point $A(2,-3)$ to the point $B(1,-2),$ then ${\int }_C \left(x^{2} y\right)\,dx+\left(x y^{2}\right)\,dy=$

- A. $\frac{119}{12}$
- B. $16$ **correct**
- C. $- \frac{23}{6}$
- D. $\frac{73}{12}$
- E. $-16$

**Worked solution**

The position vectors of the endpoints of our line segment are $a=2\,i-3\,j$ and $b=i-2\,j.$ So, the parametrization of the line segment is given by

$$
\begin{aligned}r(t) & =a+t\,(b-a) \\   & =2\,i-3\,j+t\left(i-2\,j-\left(2\,i-3\,j\right)\right) \\   & =2\,i-3\,j+t\left(-i+j\right) \\   & =\left(2 - t\right)\,i+\left(t - 3\right)\,j,\end{aligned}
$$

where $0\le t\le 1.$ Thus, we have that $x(t)=2 - t$ and $y(t)=t - 3$ along the segment.

The derivative of $r(t)$ is given by

$$
\begin{aligned}{r}^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j=-i+j.\end{aligned}
$$

We can now evaluate the line integral:

$$
\begin{aligned}{\int }_C \left(x^{2} y\right)\,dx+\left(x y^{2}\right)\,dy & ={\int }_{0}^{1}\left(x^{2} y\right)\frac{\text{d}x}{\text{d}t}+\left(x y^{2}\right)\frac{\text{d}y}{\text{d}t}\,dt \\   & ={\int }_{0}^{1}\left(\left(x^{2} y\right)\frac{\text{d}x}{\text{d}t}+\left(x y^{2}\right)\frac{\text{d}y}{\text{d}t}\right)\,dt \\   & ={\int }_{0}^{1}\left(1\right)\cdot \left(2 - t\right)^{2}\cdot \left(t - 3\right)\cdot \left(-1\right)+\left(1\right)\cdot \left(2 - t\right)\cdot \left(t - 3\right)^{2}\cdot \left(1\right)\,dt \\   & ={\int }_{0}^{1}\left(- t^{3} + 7 t^{2} - 16 t + 12\right)+\left(- t^{3} + 8 t^{2} - 21 t + 18\right)\,dt \\   & ={\int }_{0}^{1}- 2 t^{3} + 15 t^{2} - 37 t + 30\,dt \\   & =\left[- \frac{t^{4}}{2} + 5 t^{3} - \frac{37 t^{2}}{2} + 30 t\right]_0^1 \\   & =\left(- \frac{\left(1\right)^{4}}{2} + 5 \left(1\right)^{3} - \frac{37 \left(1\right)^{2}}{2} + 30 \left(1\right)\right)-\left(- \frac{\left(0\right)^{4}}{2} + 5 \left(0\right)^{3} - \frac{37 \left(0\right)^{2}}{2} + 30 \left(0\right)\right) \\   & =\left(\left(- \frac{1}{2}\right)+\left(5\right)+\left(- \frac{37}{2}\right)+\left(30\right)\right)-\left(\left(0\right)+\left(0\right)+\left(0\right)+\left(0\right)\right) \\   & =16\end{aligned}
$$
