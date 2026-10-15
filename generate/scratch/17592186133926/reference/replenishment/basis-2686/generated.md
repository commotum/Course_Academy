### authored same-method extension — moderate
Template: `polynomial_sine`; profile: `authored-method`; eligible: True

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=\left(x + y\right)\,i+\left(0\right)\,j+\left(- z\right)\,k$ along the closed curve $C$ given by $r(t)=\left(2 - 2 t^{2}\right)\,i+\left(2 t^{2}\right)\,j+\left(\sin{\left(\pi t \right)}\right)\,k$ for $t\in [-1,1).$

- A. $-8$
- B. $0$ **Correct**
- C. $1$
- D. $8$
- E. $-1$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ=\oint_C F\cdot\mathrm dr=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm dt.
$$

Along the curve $C,$ we have

$$
x=2 - 2 t^{2},\quad y=2 t^{2},\quad z=\sin{\left(\pi t \right)}.
$$

So,

$$
\begin{aligned}F(r(t)) & =\left(x + y\right)\,i+\left(0\right)\,j+\left(- z\right)\,k \\ & =\left(2\right)\,i+\left(0\right)\,j+\left(- \sin{\left(\pi t \right)}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm d}{\mathrm dt}\left(2 - 2 t^{2}\right)\,i+\frac{\mathrm d}{\mathrm dt}\left(2 t^{2}\right)\,j+\frac{\mathrm d}{\mathrm dt}\left(\sin{\left(\pi t \right)}\right)\,k \\ & =\left(- 4 t\right)\,i+\left(4 t\right)\,j+\left(\pi \cos{\left(\pi t \right)}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(2\right)\,i+\left(0\right)\,j+\left(- \sin{\left(\pi t \right)}\right)\,k\right)\cdot\left(\left(- 4 t\right)\,i+\left(4 t\right)\,j+\left(\pi \cos{\left(\pi t \right)}\right)\,k\right) \\ & =\left(2\right)\cdot\left(- 4 t\right)+\left(0\right)\cdot\left(4 t\right)+\left(- \sin{\left(\pi t \right)}\right)\cdot\left(\pi \cos{\left(\pi t \right)}\right) \\ & =\left(- 8 t\right)+\left(0\right)+\left(- \pi \sin{\left(\pi t \right)} \cos{\left(\pi t \right)}\right) \\ & =- 8 t - \frac{\pi \sin{\left(2 \pi t \right)}}{2}\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ=\oint_C F\cdot\mathrm dr & =\int_{-1}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm dt \\ & =\int_{-1}^{1}\left(- 8 t - \frac{\pi \sin{\left(2 \pi t \right)}}{2}\right)\,\mathrm dt \\ & =\left[- 4 t^{2} + \frac{\cos{\left(2 \pi t \right)}}{4}\right]_{-1}^{1} \\ & =[\left(-4\right)+\left(\frac{1}{4}\right)]-[\left(-4\right)+\left(\frac{1}{4}\right)] \\ & =0\end{aligned}
$$

---

### authored same-method extension — moderate
Template: `xy_symmetric`; profile: `authored-method`; eligible: True

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=\left(y\right)\,i+\left(x\right)\,j+\left(0\right)\,k$ along the closed curve $C$ given by $r(t)=\left(4 \sin{\left(t \right)}\right)\,i+\left(3 \cos{\left(t \right)}\right)\,j+\left(2 \sin{\left(t \right)}\right)\,k$ for $t\in [0,2 \pi).$

- A. $12 \pi$
- B. $- 24 \pi$
- C. $- 12 \pi$
- D. $24 \pi$
- E. $0$ **Correct**

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ=\oint_C F\cdot\mathrm dr=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm dt.
$$

Along the curve $C,$ we have

$$
x=4 \sin{\left(t \right)},\quad y=3 \cos{\left(t \right)},\quad z=2 \sin{\left(t \right)}.
$$

So,

$$
\begin{aligned}F(r(t)) & =\left(y\right)\,i+\left(x\right)\,j+\left(0\right)\,k \\ & =\left(3 \cos{\left(t \right)}\right)\,i+\left(4 \sin{\left(t \right)}\right)\,j+\left(0\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm d}{\mathrm dt}\left(4 \sin{\left(t \right)}\right)\,i+\frac{\mathrm d}{\mathrm dt}\left(3 \cos{\left(t \right)}\right)\,j+\frac{\mathrm d}{\mathrm dt}\left(2 \sin{\left(t \right)}\right)\,k \\ & =\left(4 \cos{\left(t \right)}\right)\,i+\left(- 3 \sin{\left(t \right)}\right)\,j+\left(2 \cos{\left(t \right)}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(3 \cos{\left(t \right)}\right)\,i+\left(4 \sin{\left(t \right)}\right)\,j+\left(0\right)\,k\right)\cdot\left(\left(4 \cos{\left(t \right)}\right)\,i+\left(- 3 \sin{\left(t \right)}\right)\,j+\left(2 \cos{\left(t \right)}\right)\,k\right) \\ & =\left(3 \cos{\left(t \right)}\right)\cdot\left(4 \cos{\left(t \right)}\right)+\left(4 \sin{\left(t \right)}\right)\cdot\left(- 3 \sin{\left(t \right)}\right)+\left(0\right)\cdot\left(2 \cos{\left(t \right)}\right) \\ & =\left(12 \cos^{2}{\left(t \right)}\right)+\left(- 12 \sin^{2}{\left(t \right)}\right)+\left(0\right) \\ & =12 \cos{\left(2 t \right)}\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ=\oint_C F\cdot\mathrm dr & =\int_{0}^{2 \pi}F(r(t))\cdot r^{\prime}(t)\,\mathrm dt \\ & =\int_{0}^{2 \pi}\left(12 \cos{\left(2 t \right)}\right)\,\mathrm dt \\ & =\left[6 \sin{\left(2 t \right)}\right]_{0}^{2 \pi} \\ & =[\left(0\right)]-[\left(0\right)] \\ & =0\end{aligned}
$$

---

### authored same-method extension — moderate
Template: `polynomial_sine`; profile: `authored-method`; eligible: True

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=\left(x + y\right)\,i+\left(0\right)\,j+\left(- z\right)\,k$ along the closed curve $C$ given by $r(t)=\left(4 - 4 t^{2}\right)\,i+\left(4 t^{2}\right)\,j+\left(\sin{\left(\pi t \right)}\right)\,k$ for $t\in [-1,1).$

- A. $1$
- B. $-32$
- C. $-1$
- D. $0$ **Correct**
- E. $32$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ=\oint_C F\cdot\mathrm dr=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm dt.
$$

Along the curve $C,$ we have

$$
x=4 - 4 t^{2},\quad y=4 t^{2},\quad z=\sin{\left(\pi t \right)}.
$$

So,

$$
\begin{aligned}F(r(t)) & =\left(x + y\right)\,i+\left(0\right)\,j+\left(- z\right)\,k \\ & =\left(4\right)\,i+\left(0\right)\,j+\left(- \sin{\left(\pi t \right)}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm d}{\mathrm dt}\left(4 - 4 t^{2}\right)\,i+\frac{\mathrm d}{\mathrm dt}\left(4 t^{2}\right)\,j+\frac{\mathrm d}{\mathrm dt}\left(\sin{\left(\pi t \right)}\right)\,k \\ & =\left(- 8 t\right)\,i+\left(8 t\right)\,j+\left(\pi \cos{\left(\pi t \right)}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(4\right)\,i+\left(0\right)\,j+\left(- \sin{\left(\pi t \right)}\right)\,k\right)\cdot\left(\left(- 8 t\right)\,i+\left(8 t\right)\,j+\left(\pi \cos{\left(\pi t \right)}\right)\,k\right) \\ & =\left(4\right)\cdot\left(- 8 t\right)+\left(0\right)\cdot\left(8 t\right)+\left(- \sin{\left(\pi t \right)}\right)\cdot\left(\pi \cos{\left(\pi t \right)}\right) \\ & =\left(- 32 t\right)+\left(0\right)+\left(- \pi \sin{\left(\pi t \right)} \cos{\left(\pi t \right)}\right) \\ & =- 32 t - \frac{\pi \sin{\left(2 \pi t \right)}}{2}\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ=\oint_C F\cdot\mathrm dr & =\int_{-1}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm dt \\ & =\int_{-1}^{1}\left(- 32 t - \frac{\pi \sin{\left(2 \pi t \right)}}{2}\right)\,\mathrm dt \\ & =\left[- 16 t^{2} + \frac{\cos{\left(2 \pi t \right)}}{4}\right]_{-1}^{1} \\ & =[\left(-16\right)+\left(\frac{1}{4}\right)]-[\left(-16\right)+\left(\frac{1}{4}\right)] \\ & =0\end{aligned}
$$

---

### authored same-method extension — moderate
Template: `polynomial_sine`; profile: `authored-method`; eligible: True

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=\left(x + y\right)\,i+\left(0\right)\,j+\left(- z\right)\,k$ along the closed curve $C$ given by $r(t)=\left(3 - 3 t^{2}\right)\,i+\left(3 t^{2}\right)\,j+\left(4 \sin{\left(\pi t \right)}\right)\,k$ for $t\in [-1,1).$

- A. $-18$
- B. $-16$
- C. $0$ **Correct**
- D. $16$
- E. $18$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ=\oint_C F\cdot\mathrm dr=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm dt.
$$

Along the curve $C,$ we have

$$
x=3 - 3 t^{2},\quad y=3 t^{2},\quad z=4 \sin{\left(\pi t \right)}.
$$

So,

$$
\begin{aligned}F(r(t)) & =\left(x + y\right)\,i+\left(0\right)\,j+\left(- z\right)\,k \\ & =\left(3\right)\,i+\left(0\right)\,j+\left(- 4 \sin{\left(\pi t \right)}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm d}{\mathrm dt}\left(3 - 3 t^{2}\right)\,i+\frac{\mathrm d}{\mathrm dt}\left(3 t^{2}\right)\,j+\frac{\mathrm d}{\mathrm dt}\left(4 \sin{\left(\pi t \right)}\right)\,k \\ & =\left(- 6 t\right)\,i+\left(6 t\right)\,j+\left(4 \pi \cos{\left(\pi t \right)}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(3\right)\,i+\left(0\right)\,j+\left(- 4 \sin{\left(\pi t \right)}\right)\,k\right)\cdot\left(\left(- 6 t\right)\,i+\left(6 t\right)\,j+\left(4 \pi \cos{\left(\pi t \right)}\right)\,k\right) \\ & =\left(3\right)\cdot\left(- 6 t\right)+\left(0\right)\cdot\left(6 t\right)+\left(- 4 \sin{\left(\pi t \right)}\right)\cdot\left(4 \pi \cos{\left(\pi t \right)}\right) \\ & =\left(- 18 t\right)+\left(0\right)+\left(- 16 \pi \sin{\left(\pi t \right)} \cos{\left(\pi t \right)}\right) \\ & =- 18 t - 8 \pi \sin{\left(2 \pi t \right)}\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ=\oint_C F\cdot\mathrm dr & =\int_{-1}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm dt \\ & =\int_{-1}^{1}\left(- 18 t - 8 \pi \sin{\left(2 \pi t \right)}\right)\,\mathrm dt \\ & =\left[- 9 t^{2} + 4 \cos{\left(2 \pi t \right)}\right]_{-1}^{1} \\ & =[\left(-9\right)+\left(4\right)]-[\left(-9\right)+\left(4\right)] \\ & =0\end{aligned}
$$

---

### authored same-method extension — hard
Template: `polynomial_loop`; profile: `authored-method`; eligible: True

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=\left(- 5 x + 6 y\right)\,i+\left(0\right)\,j+\left(0\right)\,k$ along the closed curve $C$ given by $r(t)=\left(6 t^{2} - 6 t\right)\,i+\left(5 t^{3} - 5 t\right)\,j+\left(\sin{\left(2 \pi t \right)}\right)\,k$ for $t\in [0,1).$

- A. $0$
- B. $-3$ **Correct**
- C. $-30$
- D. $3$
- E. $-18$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ=\oint_C F\cdot\mathrm dr=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm dt.
$$

Along the curve $C,$ we have

$$
x=6 t^{2} - 6 t,\quad y=5 t^{3} - 5 t,\quad z=\sin{\left(2 \pi t \right)}.
$$

So,

$$
\begin{aligned}F(r(t)) & =\left(- 5 x + 6 y\right)\,i+\left(0\right)\,j+\left(0\right)\,k \\ & =\left(30 t^{3} - 30 t^{2}\right)\,i+\left(0\right)\,j+\left(0\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm d}{\mathrm dt}\left(6 t^{2} - 6 t\right)\,i+\frac{\mathrm d}{\mathrm dt}\left(5 t^{3} - 5 t\right)\,j+\frac{\mathrm d}{\mathrm dt}\left(\sin{\left(2 \pi t \right)}\right)\,k \\ & =\left(12 t - 6\right)\,i+\left(15 t^{2} - 5\right)\,j+\left(2 \pi \cos{\left(2 \pi t \right)}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(30 t^{3} - 30 t^{2}\right)\,i+\left(0\right)\,j+\left(0\right)\,k\right)\cdot\left(\left(12 t - 6\right)\,i+\left(15 t^{2} - 5\right)\,j+\left(2 \pi \cos{\left(2 \pi t \right)}\right)\,k\right) \\ & =\left(30 t^{3} - 30 t^{2}\right)\cdot\left(12 t - 6\right)+\left(0\right)\cdot\left(15 t^{2} - 5\right)+\left(0\right)\cdot\left(2 \pi \cos{\left(2 \pi t \right)}\right) \\ & =\left(360 t^{4} - 540 t^{3} + 180 t^{2}\right)+\left(0\right)+\left(0\right) \\ & =\left(12 t - 6\right) \left(30 t^{3} - 30 t^{2}\right)\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ=\oint_C F\cdot\mathrm dr & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm dt \\ & =\int_{0}^{1}\left(\left(12 t - 6\right) \left(30 t^{3} - 30 t^{2}\right)\right)\,\mathrm dt \\ & =\left[72 t^{5} - 135 t^{4} + 60 t^{3}\right]_{0}^{1} \\ & =[\left(60\right)+\left(-135\right)+\left(72\right)]-[\left(0\right)+\left(0\right)+\left(0\right)] \\ & =-3\end{aligned}
$$

---

### authored same-method extension — hard
Template: `polynomial_loop`; profile: `authored-method`; eligible: True

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=\left(- 6 x + 5 y\right)\,i+\left(0\right)\,j+\left(0\right)\,k$ along the closed curve $C$ given by $r(t)=\left(5 t^{2} - 5 t\right)\,i+\left(6 t^{3} - 6 t\right)\,j+\left(\sin{\left(2 \pi t \right)}\right)\,k$ for $t\in [0,1).$

- A. $-25$
- B. $0$
- C. $-15$
- D. $\frac{5}{2}$
- E. $- \frac{5}{2}$ **Correct**

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ=\oint_C F\cdot\mathrm dr=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm dt.
$$

Along the curve $C,$ we have

$$
x=5 t^{2} - 5 t,\quad y=6 t^{3} - 6 t,\quad z=\sin{\left(2 \pi t \right)}.
$$

So,

$$
\begin{aligned}F(r(t)) & =\left(- 6 x + 5 y\right)\,i+\left(0\right)\,j+\left(0\right)\,k \\ & =\left(30 t^{3} - 30 t^{2}\right)\,i+\left(0\right)\,j+\left(0\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm d}{\mathrm dt}\left(5 t^{2} - 5 t\right)\,i+\frac{\mathrm d}{\mathrm dt}\left(6 t^{3} - 6 t\right)\,j+\frac{\mathrm d}{\mathrm dt}\left(\sin{\left(2 \pi t \right)}\right)\,k \\ & =\left(10 t - 5\right)\,i+\left(18 t^{2} - 6\right)\,j+\left(2 \pi \cos{\left(2 \pi t \right)}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(30 t^{3} - 30 t^{2}\right)\,i+\left(0\right)\,j+\left(0\right)\,k\right)\cdot\left(\left(10 t - 5\right)\,i+\left(18 t^{2} - 6\right)\,j+\left(2 \pi \cos{\left(2 \pi t \right)}\right)\,k\right) \\ & =\left(30 t^{3} - 30 t^{2}\right)\cdot\left(10 t - 5\right)+\left(0\right)\cdot\left(18 t^{2} - 6\right)+\left(0\right)\cdot\left(2 \pi \cos{\left(2 \pi t \right)}\right) \\ & =\left(300 t^{4} - 450 t^{3} + 150 t^{2}\right)+\left(0\right)+\left(0\right) \\ & =\left(10 t - 5\right) \left(30 t^{3} - 30 t^{2}\right)\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ=\oint_C F\cdot\mathrm dr & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm dt \\ & =\int_{0}^{1}\left(\left(10 t - 5\right) \left(30 t^{3} - 30 t^{2}\right)\right)\,\mathrm dt \\ & =\left[60 t^{5} - \frac{225 t^{4}}{2} + 50 t^{3}\right]_{0}^{1} \\ & =[\left(50\right)+\left(- \frac{225}{2}\right)+\left(60\right)]-[\left(0\right)+\left(0\right)+\left(0\right)] \\ & =- \frac{5}{2}\end{aligned}
$$

---

### authored same-method extension — hard
Template: `polynomial_loop`; profile: `authored-method`; eligible: True

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=\left(- x + 4 y\right)\,i+\left(0\right)\,j+\left(0\right)\,k$ along the closed curve $C$ given by $r(t)=\left(4 t^{2} - 4 t\right)\,i+\left(t^{3} - t\right)\,j+\left(\sin{\left(2 \pi t \right)}\right)\,k$ for $t\in [0,1).$

- A. $- \frac{8}{3}$
- B. $0$
- C. $- \frac{8}{5}$
- D. $- \frac{4}{15}$ **Correct**
- E. $\frac{4}{15}$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ=\oint_C F\cdot\mathrm dr=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm dt.
$$

Along the curve $C,$ we have

$$
x=4 t^{2} - 4 t,\quad y=t^{3} - t,\quad z=\sin{\left(2 \pi t \right)}.
$$

So,

$$
\begin{aligned}F(r(t)) & =\left(- x + 4 y\right)\,i+\left(0\right)\,j+\left(0\right)\,k \\ & =\left(4 t^{3} - 4 t^{2}\right)\,i+\left(0\right)\,j+\left(0\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm d}{\mathrm dt}\left(4 t^{2} - 4 t\right)\,i+\frac{\mathrm d}{\mathrm dt}\left(t^{3} - t\right)\,j+\frac{\mathrm d}{\mathrm dt}\left(\sin{\left(2 \pi t \right)}\right)\,k \\ & =\left(8 t - 4\right)\,i+\left(3 t^{2} - 1\right)\,j+\left(2 \pi \cos{\left(2 \pi t \right)}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(4 t^{3} - 4 t^{2}\right)\,i+\left(0\right)\,j+\left(0\right)\,k\right)\cdot\left(\left(8 t - 4\right)\,i+\left(3 t^{2} - 1\right)\,j+\left(2 \pi \cos{\left(2 \pi t \right)}\right)\,k\right) \\ & =\left(4 t^{3} - 4 t^{2}\right)\cdot\left(8 t - 4\right)+\left(0\right)\cdot\left(3 t^{2} - 1\right)+\left(0\right)\cdot\left(2 \pi \cos{\left(2 \pi t \right)}\right) \\ & =\left(32 t^{4} - 48 t^{3} + 16 t^{2}\right)+\left(0\right)+\left(0\right) \\ & =\left(8 t - 4\right) \left(4 t^{3} - 4 t^{2}\right)\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ=\oint_C F\cdot\mathrm dr & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm dt \\ & =\int_{0}^{1}\left(\left(8 t - 4\right) \left(4 t^{3} - 4 t^{2}\right)\right)\,\mathrm dt \\ & =\left[\frac{32 t^{5}}{5} - 12 t^{4} + \frac{16 t^{3}}{3}\right]_{0}^{1} \\ & =[\left(\frac{16}{3}\right)+\left(-12\right)+\left(\frac{32}{5}\right)]-[\left(0\right)+\left(0\right)+\left(0\right)] \\ & =- \frac{4}{15}\end{aligned}
$$

---

### authored same-method extension — hard
Template: `polynomial_loop`; profile: `authored-method`; eligible: True

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=\left(- 3 x + y\right)\,i+\left(0\right)\,j+\left(0\right)\,k$ along the closed curve $C$ given by $r(t)=\left(t^{2} - t\right)\,i+\left(3 t^{3} - 3 t\right)\,j+\left(\sin{\left(2 \pi t \right)}\right)\,k$ for $t\in [0,1).$

- A. $0$
- B. $- \frac{3}{10}$
- C. $- \frac{1}{20}$ **Correct**
- D. $- \frac{1}{2}$
- E. $\frac{1}{20}$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ=\oint_C F\cdot\mathrm dr=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm dt.
$$

Along the curve $C,$ we have

$$
x=t^{2} - t,\quad y=3 t^{3} - 3 t,\quad z=\sin{\left(2 \pi t \right)}.
$$

So,

$$
\begin{aligned}F(r(t)) & =\left(- 3 x + y\right)\,i+\left(0\right)\,j+\left(0\right)\,k \\ & =\left(3 t^{3} - 3 t^{2}\right)\,i+\left(0\right)\,j+\left(0\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm d}{\mathrm dt}\left(t^{2} - t\right)\,i+\frac{\mathrm d}{\mathrm dt}\left(3 t^{3} - 3 t\right)\,j+\frac{\mathrm d}{\mathrm dt}\left(\sin{\left(2 \pi t \right)}\right)\,k \\ & =\left(2 t - 1\right)\,i+\left(9 t^{2} - 3\right)\,j+\left(2 \pi \cos{\left(2 \pi t \right)}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(3 t^{3} - 3 t^{2}\right)\,i+\left(0\right)\,j+\left(0\right)\,k\right)\cdot\left(\left(2 t - 1\right)\,i+\left(9 t^{2} - 3\right)\,j+\left(2 \pi \cos{\left(2 \pi t \right)}\right)\,k\right) \\ & =\left(3 t^{3} - 3 t^{2}\right)\cdot\left(2 t - 1\right)+\left(0\right)\cdot\left(9 t^{2} - 3\right)+\left(0\right)\cdot\left(2 \pi \cos{\left(2 \pi t \right)}\right) \\ & =\left(6 t^{4} - 9 t^{3} + 3 t^{2}\right)+\left(0\right)+\left(0\right) \\ & =\left(2 t - 1\right) \left(3 t^{3} - 3 t^{2}\right)\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ=\oint_C F\cdot\mathrm dr & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm dt \\ & =\int_{0}^{1}\left(\left(2 t - 1\right) \left(3 t^{3} - 3 t^{2}\right)\right)\,\mathrm dt \\ & =\left[\frac{6 t^{5}}{5} - \frac{9 t^{4}}{4} + t^{3}\right]_{0}^{1} \\ & =[\left(1\right)+\left(- \frac{9}{4}\right)+\left(\frac{6}{5}\right)]-[\left(0\right)+\left(0\right)+\left(0\right)] \\ & =- \frac{1}{20}\end{aligned}
$$

---

### authored same-method extension — hard
Template: `polynomial_loop`; profile: `authored-method`; eligible: True

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=\left(- 5 x + 3 y\right)\,i+\left(0\right)\,j+\left(0\right)\,k$ along the closed curve $C$ given by $r(t)=\left(3 t^{2} - 3 t\right)\,i+\left(5 t^{3} - 5 t\right)\,j+\left(\sin{\left(2 \pi t \right)}\right)\,k$ for $t\in [0,1).$

- A. $- \frac{9}{2}$
- B. $\frac{3}{4}$
- C. $0$
- D. $- \frac{3}{4}$ **Correct**
- E. $- \frac{15}{2}$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ=\oint_C F\cdot\mathrm dr=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm dt.
$$

Along the curve $C,$ we have

$$
x=3 t^{2} - 3 t,\quad y=5 t^{3} - 5 t,\quad z=\sin{\left(2 \pi t \right)}.
$$

So,

$$
\begin{aligned}F(r(t)) & =\left(- 5 x + 3 y\right)\,i+\left(0\right)\,j+\left(0\right)\,k \\ & =\left(15 t^{3} - 15 t^{2}\right)\,i+\left(0\right)\,j+\left(0\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm d}{\mathrm dt}\left(3 t^{2} - 3 t\right)\,i+\frac{\mathrm d}{\mathrm dt}\left(5 t^{3} - 5 t\right)\,j+\frac{\mathrm d}{\mathrm dt}\left(\sin{\left(2 \pi t \right)}\right)\,k \\ & =\left(6 t - 3\right)\,i+\left(15 t^{2} - 5\right)\,j+\left(2 \pi \cos{\left(2 \pi t \right)}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(15 t^{3} - 15 t^{2}\right)\,i+\left(0\right)\,j+\left(0\right)\,k\right)\cdot\left(\left(6 t - 3\right)\,i+\left(15 t^{2} - 5\right)\,j+\left(2 \pi \cos{\left(2 \pi t \right)}\right)\,k\right) \\ & =\left(15 t^{3} - 15 t^{2}\right)\cdot\left(6 t - 3\right)+\left(0\right)\cdot\left(15 t^{2} - 5\right)+\left(0\right)\cdot\left(2 \pi \cos{\left(2 \pi t \right)}\right) \\ & =\left(90 t^{4} - 135 t^{3} + 45 t^{2}\right)+\left(0\right)+\left(0\right) \\ & =\left(6 t - 3\right) \left(15 t^{3} - 15 t^{2}\right)\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ=\oint_C F\cdot\mathrm dr & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm dt \\ & =\int_{0}^{1}\left(\left(6 t - 3\right) \left(15 t^{3} - 15 t^{2}\right)\right)\,\mathrm dt \\ & =\left[18 t^{5} - \frac{135 t^{4}}{4} + 15 t^{3}\right]_{0}^{1} \\ & =[\left(15\right)+\left(- \frac{135}{4}\right)+\left(18\right)]-[\left(0\right)+\left(0\right)+\left(0\right)] \\ & =- \frac{3}{4}\end{aligned}
$$