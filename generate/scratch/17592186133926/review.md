# Circulation over space curves — author review

Original profiles preserve captured anomalies and are evidence only. Generated normal records are authored, with actual difficulty and correct choice labels. Raw q-162238 stays unrated and lacks an original correct key/solution. Independent inferred value: $-1/60$.

### original parameterized evidence — easy
Template: `xy_rotation`; profile: `raw:q-161925`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=y\,i-x\,j$ along the closed curve $C$ given by $r(t)=\operatorname{cos}⁡(\pi t)\,i+\operatorname{sin}⁡(\pi t)\,j+(1-{t}^{2})\,k$ for $t\in [-1,1).$

- A. $-1$
- B. $-2\pi $ **Correct**
- C. $\frac{\pi }{2}$
- D. $4$
- E. $4\pi $

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ={∮}_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=\operatorname{cos}⁡(\pi t),\,y=\operatorname{sin}⁡(\pi t),\,z=1-{t}^{2}.
$$

So,

$$
\begin{aligned}F(r(t)) & =y\,i-x\,j \\  & =\operatorname{sin}⁡(\pi t)\,i-\operatorname{cos}⁡(\pi t)\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡(\pi t))\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(\pi t))\,j+\frac{\text{d}}{\text{d}t}(1-{t}^{2})\,k \\  & =-\pi \operatorname{sin}⁡(\pi t)\,i+\pi \operatorname{cos}⁡(\pi t)\,j-2t\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(\operatorname{sin}⁡(\pi t)\,i-\operatorname{cos}⁡(\pi t)\,j)\cdot (-\pi \operatorname{sin}⁡(\pi t)\,i+\pi \operatorname{cos}⁡(\pi t)\,j-2t\,k) \\  & =\operatorname{sin}⁡(\pi t)\cdot (-\pi \operatorname{sin}⁡(\pi t))+(-\operatorname{cos}⁡(\pi t))\cdot \pi \operatorname{cos}⁡(\pi t)+0\cdot (-2t) \\  & =-\pi {sin}^{2}⁡(\pi t)-\pi {cos}^{2}⁡(\pi t) \\  & =-\pi .\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ={∮}_{C}F\cdot \text{d}r & ={\int }_{-1}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{-1}^{1}(-\pi )\,\text{d}t \\  & =-\pi [t]_{-1}^{1} \\  & =-\pi (1-(-1)) \\  & =-2\pi \end{aligned}
$$

---

### generated opaque evidence pattern — easy
Template: `xy_rotation`; profile: `raw:q-161925`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=2\left(y\,i-x\,j\right)$ along the closed curve $C$ given by $r(t)=\operatorname{cos}⁡(\pi t)\,i+\operatorname{sin}⁡(\pi t)\,j+(1-{t}^{2})\,k$ for $t\in [-1,1).$

- A. $8 \pi$
- B. $8$
- C. $- 4 \pi$ **Correct**
- D. $-2$
- E. $\pi$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ={∮}_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=\operatorname{cos}⁡(\pi t),\,y=\operatorname{sin}⁡(\pi t),\,z=1-{t}^{2}.
$$

So,

$$
\begin{aligned}F(r(t)) & =2\left(y\,i-x\,j\right) \\  & =2\left(\operatorname{sin}⁡(\pi t)\,i-\operatorname{cos}⁡(\pi t)\,j\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡(\pi t))\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(\pi t))\,j+\frac{\text{d}}{\text{d}t}(1-{t}^{2})\,k \\  & =-\pi \operatorname{sin}⁡(\pi t)\,i+\pi \operatorname{cos}⁡(\pi t)\,j-2t\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =2\left((\operatorname{sin}⁡(\pi t)\,i-\operatorname{cos}⁡(\pi t)\,j)\cdot (-\pi \operatorname{sin}⁡(\pi t)\,i+\pi \operatorname{cos}⁡(\pi t)\,j-2t\,k)\right) \\  & =2\left(\operatorname{sin}⁡(\pi t)\cdot (-\pi \operatorname{sin}⁡(\pi t))+(-\operatorname{cos}⁡(\pi t))\cdot \pi \operatorname{cos}⁡(\pi t)+0\cdot (-2t)\right) \\  & =2\left(-\pi {sin}^{2}⁡(\pi t)-\pi {cos}^{2}⁡(\pi t)\right) \\  & =2\left(-\pi\right) .\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ={∮}_{C}F\cdot \text{d}r & ={\int }_{-1}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =2\left({\int }_{-1}^{1}(-\pi )\,\text{d}t\right) \\  & =2\left(-\pi [t]_{-1}^{1}\right) \\  & =2\left(-\pi (1-(-1))\right) \\  & =2\left(-2\pi\right) \end{aligned}
$$

---

### generated opaque evidence pattern — easy
Template: `xy_rotation`; profile: `raw:q-161925`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=-2\left(y\,i-x\,j\right)$ along the closed curve $C$ given by $r(t)=\operatorname{cos}⁡(\pi t)\,i+\operatorname{sin}⁡(\pi t)\,j+(1-{t}^{2})\,k$ for $t\in [-1,1).$

- A. $- 8 \pi$
- B. $-8$
- C. $4 \pi$ **Correct**
- D. $2$
- E. $- \pi$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ={∮}_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=\operatorname{cos}⁡(\pi t),\,y=\operatorname{sin}⁡(\pi t),\,z=1-{t}^{2}.
$$

So,

$$
\begin{aligned}F(r(t)) & =-2\left(y\,i-x\,j\right) \\  & =-2\left(\operatorname{sin}⁡(\pi t)\,i-\operatorname{cos}⁡(\pi t)\,j\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡(\pi t))\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(\pi t))\,j+\frac{\text{d}}{\text{d}t}(1-{t}^{2})\,k \\  & =-\pi \operatorname{sin}⁡(\pi t)\,i+\pi \operatorname{cos}⁡(\pi t)\,j-2t\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =-2\left((\operatorname{sin}⁡(\pi t)\,i-\operatorname{cos}⁡(\pi t)\,j)\cdot (-\pi \operatorname{sin}⁡(\pi t)\,i+\pi \operatorname{cos}⁡(\pi t)\,j-2t\,k)\right) \\  & =-2\left(\operatorname{sin}⁡(\pi t)\cdot (-\pi \operatorname{sin}⁡(\pi t))+(-\operatorname{cos}⁡(\pi t))\cdot \pi \operatorname{cos}⁡(\pi t)+0\cdot (-2t)\right) \\  & =-2\left(-\pi {sin}^{2}⁡(\pi t)-\pi {cos}^{2}⁡(\pi t)\right) \\  & =-2\left(-\pi\right) .\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ={∮}_{C}F\cdot \text{d}r & ={\int }_{-1}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =-2\left({\int }_{-1}^{1}(-\pi )\,\text{d}t\right) \\  & =-2\left(-\pi [t]_{-1}^{1}\right) \\  & =-2\left(-\pi (1-(-1))\right) \\  & =-2\left(-2\pi\right) \end{aligned}
$$

---

### original parameterized evidence — unrated
Template: `polynomial_loop`; profile: `raw:q-162238`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x, y, z) = (y - x)i$ along the closed curve $C$ given by $r(t) = (t^{2} - t)i + (t^{3} - t)j + \sin (2πt)k$ for $t ∈ [0, 1)$.

- A. $100$
- B. $-\frac{1}{60}$
- C. $-\frac{1}{100}$
- D. $10$
- E. $-\frac{1}{6}$

Original correct designation absent; inferred separately.

Original worked solution absent.

---

### generated opaque evidence pattern — unrated
Template: `polynomial_loop`; profile: `raw:q-162238`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x, y, z) = 2\left((y - x)i\right)$ along the closed curve $C$ given by $r(t) = (t^{2} - t)i + (t^{3} - t)j + \sin (2πt)k$ for $t ∈ [0, 1)$.

- A. $- \frac{1}{3}$
- B. $20$
- C. $- \frac{1}{30}$
- D. $200$
- E. $- \frac{1}{50}$

Original correct designation absent; inferred separately.

Original worked solution absent.

---

### generated opaque evidence pattern — unrated
Template: `polynomial_loop`; profile: `raw:q-162238`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x, y, z) = -2\left((y - x)i\right)$ along the closed curve $C$ given by $r(t) = (t^{2} - t)i + (t^{3} - t)j + \sin (2πt)k$ for $t ∈ [0, 1)$.

- A. $\frac{1}{3}$
- B. $-20$
- C. $\frac{1}{30}$
- D. $-200$
- E. $\frac{1}{50}$

Original correct designation absent; inferred separately.

Original worked solution absent.

---

### original parameterized evidence — moderate
Template: `xy_symmetric`; profile: `raw:q-162220`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=y\,i+x\,j$ along the closed curve $C$ given by $r(t)=\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j+2\operatorname{sin}⁡t\,k$ for $t\in [0,2\pi ).$

- A. $\pi $
- B. $2\pi $
- C. $4$
- D. $0$ **Correct**
- E. $1$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ={∮}_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=\operatorname{sin}⁡t,\,y=\operatorname{cos}⁡t,\,z=2\operatorname{sin}⁡t.
$$

So,

$$
\begin{aligned}F(r(t)) & =y\,i+x\,j \\  & =\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)\,j+\frac{\text{d}}{\text{d}t}(2\operatorname{sin}⁡t)\,k \\  & =\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j+2\operatorname{cos}⁡t\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j)\cdot (\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j+2\operatorname{cos}⁡t\,k) \\  & =\operatorname{cos}⁡t\cdot \operatorname{cos}⁡t+\operatorname{sin}⁡t\cdot (-\operatorname{sin}⁡t)+0\cdot 2\operatorname{cos}⁡t \\  & ={cos}^{2}⁡t-{sin}^{2}⁡t.\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ={∮}_{C}F\cdot \text{d}r & ={\int }_{0}^{2\pi }F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{2\pi }({cos}^{2}⁡t-{sin}^{2}⁡t)\,\text{d}t \\  & ={\int }_{0}^{2\pi }\operatorname{cos}⁡(2t)\,\text{d}t \\  & =[\frac{\operatorname{sin}⁡(2t)}{2}]_{0}^{2\pi } \\  & =0\end{aligned}
$$

---

### generated opaque evidence pattern — moderate
Template: `xy_symmetric`; profile: `raw:q-162220`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=2\left(y\,i+x\,j\right)$ along the closed curve $C$ given by $r(t)=\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j+2\operatorname{sin}⁡t\,k$ for $t\in [0,2\pi ).$

- A. $2$
- B. $0$ **Correct**
- C. $4 \pi$
- D. $2 \pi$
- E. $8$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ={∮}_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=\operatorname{sin}⁡t,\,y=\operatorname{cos}⁡t,\,z=2\operatorname{sin}⁡t.
$$

So,

$$
\begin{aligned}F(r(t)) & =2\left(y\,i+x\,j\right) \\  & =2\left(\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)\,j+\frac{\text{d}}{\text{d}t}(2\operatorname{sin}⁡t)\,k \\  & =\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j+2\operatorname{cos}⁡t\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =2\left((\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j)\cdot (\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j+2\operatorname{cos}⁡t\,k)\right) \\  & =2\left(\operatorname{cos}⁡t\cdot \operatorname{cos}⁡t+\operatorname{sin}⁡t\cdot (-\operatorname{sin}⁡t)+0\cdot 2\operatorname{cos}⁡t\right) \\  & =2\left({cos}^{2}⁡t-{sin}^{2}⁡t\right).\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ={∮}_{C}F\cdot \text{d}r & ={\int }_{0}^{2\pi }F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =2\left({\int }_{0}^{2\pi }({cos}^{2}⁡t-{sin}^{2}⁡t)\,\text{d}t\right) \\  & =2\left({\int }_{0}^{2\pi }\operatorname{cos}⁡(2t)\,\text{d}t\right) \\  & =2\left([\frac{\operatorname{sin}⁡(2t)}{2}]_{0}^{2\pi }\right) \\  & =2\left(0\right)\end{aligned}
$$

---

### generated opaque evidence pattern — moderate
Template: `xy_symmetric`; profile: `raw:q-162220`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=-2\left(y\,i+x\,j\right)$ along the closed curve $C$ given by $r(t)=\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j+2\operatorname{sin}⁡t\,k$ for $t\in [0,2\pi ).$

- A. $-2$
- B. $0$ **Correct**
- C. $- 4 \pi$
- D. $- 2 \pi$
- E. $-8$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ={∮}_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=\operatorname{sin}⁡t,\,y=\operatorname{cos}⁡t,\,z=2\operatorname{sin}⁡t.
$$

So,

$$
\begin{aligned}F(r(t)) & =-2\left(y\,i+x\,j\right) \\  & =-2\left(\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)\,j+\frac{\text{d}}{\text{d}t}(2\operatorname{sin}⁡t)\,k \\  & =\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j+2\operatorname{cos}⁡t\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =-2\left((\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j)\cdot (\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j+2\operatorname{cos}⁡t\,k)\right) \\  & =-2\left(\operatorname{cos}⁡t\cdot \operatorname{cos}⁡t+\operatorname{sin}⁡t\cdot (-\operatorname{sin}⁡t)+0\cdot 2\operatorname{cos}⁡t\right) \\  & =-2\left({cos}^{2}⁡t-{sin}^{2}⁡t\right).\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ={∮}_{C}F\cdot \text{d}r & ={\int }_{0}^{2\pi }F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =-2\left({\int }_{0}^{2\pi }({cos}^{2}⁡t-{sin}^{2}⁡t)\,\text{d}t\right) \\  & =-2\left({\int }_{0}^{2\pi }\operatorname{cos}⁡(2t)\,\text{d}t\right) \\  & =-2\left([\frac{\operatorname{sin}⁡(2t)}{2}]_{0}^{2\pi }\right) \\  & =-2\left(0\right)\end{aligned}
$$

---

### original parameterized evidence — easy
Template: `xy_rotation_z`; profile: `raw:q-162230`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=y\,i-x\,j+z\,k$ along the closed curve $C$ given by $r(t)=\operatorname{sin}⁡(t)\,i+\operatorname{cos}⁡(t)\,j+{t}^{2}\,k$ for $t\in [-\pi ,\pi ).$

- A. $2\pi $ **Correct**
- B. $5\pi $
- C. $3\pi $
- D. $\pi $
- E. $4\pi $

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ={∮}_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=\operatorname{sin}⁡(t),\,y=\operatorname{cos}⁡(t),\,z={t}^{2}.
$$

So,

$$
\begin{aligned}F(r(t)) & =y\,i-x\,j+z\,k \\  & =\operatorname{cos}⁡(t)\,i-\operatorname{sin}⁡(t)\,j+{t}^{2}\,k.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(t))\,i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡(t))\,j+\frac{\text{d}}{\text{d}t}({t}^{2})\,k \\  & =\operatorname{cos}⁡(t)\,i-\operatorname{sin}⁡(t)\,j+2t\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(\operatorname{cos}⁡(t)\,i-\operatorname{sin}⁡(t)\,j+{t}^{2}\,k)\cdot (\operatorname{cos}⁡(t)\,i-\operatorname{sin}⁡(t)\,j+2t\,k) \\  & =\operatorname{cos}⁡(t)\cdot \operatorname{cos}⁡(t)+(-\operatorname{sin}⁡(t))\cdot (-\operatorname{sin}⁡(t))+{t}^{2}\cdot 2t \\  & ={cos}^{2}⁡(\pi t)+{sin}^{2}⁡(t)+2{t}^{3} \\  & =1+2{t}^{3}.\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ={∮}_{C}F\cdot \text{d}r & ={\int }_{-\pi }^{\pi }F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{-\pi }^{\pi }(1+2{t}^{3})\,\text{d}t \\  & ={[t+\frac{{t}^{4}}{2}]}_{-\pi }^{\pi } \\  & =((\pi -(-\pi ))+\frac{{\pi }^{4}-(-\pi )^{4}}{2}) \\  & =2\pi \end{aligned}
$$

---

### generated opaque evidence pattern — easy
Template: `xy_rotation_z`; profile: `raw:q-162230`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=2\left(y\,i-x\,j+z\,k\right)$ along the closed curve $C$ given by $r(t)=\operatorname{sin}⁡(t)\,i+\operatorname{cos}⁡(t)\,j+{t}^{2}\,k$ for $t\in [-\pi ,\pi ).$

- A. $8 \pi$
- B. $2 \pi$
- C. $10 \pi$
- D. $4 \pi$ **Correct**
- E. $6 \pi$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ={∮}_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=\operatorname{sin}⁡(t),\,y=\operatorname{cos}⁡(t),\,z={t}^{2}.
$$

So,

$$
\begin{aligned}F(r(t)) & =2\left(y\,i-x\,j+z\,k\right) \\  & =2\left(\operatorname{cos}⁡(t)\,i-\operatorname{sin}⁡(t)\,j+{t}^{2}\,k\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(t))\,i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡(t))\,j+\frac{\text{d}}{\text{d}t}({t}^{2})\,k \\  & =\operatorname{cos}⁡(t)\,i-\operatorname{sin}⁡(t)\,j+2t\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =2\left((\operatorname{cos}⁡(t)\,i-\operatorname{sin}⁡(t)\,j+{t}^{2}\,k)\cdot (\operatorname{cos}⁡(t)\,i-\operatorname{sin}⁡(t)\,j+2t\,k)\right) \\  & =2\left(\operatorname{cos}⁡(t)\cdot \operatorname{cos}⁡(t)+(-\operatorname{sin}⁡(t))\cdot (-\operatorname{sin}⁡(t))+{t}^{2}\cdot 2t\right) \\  & =2\left({cos}^{2}⁡(\pi t)+{sin}^{2}⁡(t)+2{t}^{3}\right) \\  & =2\left(1+2{t}^{3}\right).\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ={∮}_{C}F\cdot \text{d}r & ={\int }_{-\pi }^{\pi }F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =2\left({\int }_{-\pi }^{\pi }(1+2{t}^{3})\,\text{d}t\right) \\  & =2\left({[t+\frac{{t}^{4}}{2}]}_{-\pi }^{\pi }\right) \\  & =2\left(((\pi -(-\pi ))+\frac{{\pi }^{4}-(-\pi )^{4}}{2})\right) \\  & =2\left(2\pi\right) \end{aligned}
$$

---

### generated opaque evidence pattern — easy
Template: `xy_rotation_z`; profile: `raw:q-162230`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=-2\left(y\,i-x\,j+z\,k\right)$ along the closed curve $C$ given by $r(t)=\operatorname{sin}⁡(t)\,i+\operatorname{cos}⁡(t)\,j+{t}^{2}\,k$ for $t\in [-\pi ,\pi ).$

- A. $- 8 \pi$
- B. $- 2 \pi$
- C. $- 10 \pi$
- D. $- 4 \pi$ **Correct**
- E. $- 6 \pi$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ={∮}_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=\operatorname{sin}⁡(t),\,y=\operatorname{cos}⁡(t),\,z={t}^{2}.
$$

So,

$$
\begin{aligned}F(r(t)) & =-2\left(y\,i-x\,j+z\,k\right) \\  & =-2\left(\operatorname{cos}⁡(t)\,i-\operatorname{sin}⁡(t)\,j+{t}^{2}\,k\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(t))\,i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡(t))\,j+\frac{\text{d}}{\text{d}t}({t}^{2})\,k \\  & =\operatorname{cos}⁡(t)\,i-\operatorname{sin}⁡(t)\,j+2t\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =-2\left((\operatorname{cos}⁡(t)\,i-\operatorname{sin}⁡(t)\,j+{t}^{2}\,k)\cdot (\operatorname{cos}⁡(t)\,i-\operatorname{sin}⁡(t)\,j+2t\,k)\right) \\  & =-2\left(\operatorname{cos}⁡(t)\cdot \operatorname{cos}⁡(t)+(-\operatorname{sin}⁡(t))\cdot (-\operatorname{sin}⁡(t))+{t}^{2}\cdot 2t\right) \\  & =-2\left({cos}^{2}⁡(\pi t)+{sin}^{2}⁡(t)+2{t}^{3}\right) \\  & =-2\left(1+2{t}^{3}\right).\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ={∮}_{C}F\cdot \text{d}r & ={\int }_{-\pi }^{\pi }F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =-2\left({\int }_{-\pi }^{\pi }(1+2{t}^{3})\,\text{d}t\right) \\  & =-2\left({[t+\frac{{t}^{4}}{2}]}_{-\pi }^{\pi }\right) \\  & =-2\left(((\pi -(-\pi ))+\frac{{\pi }^{4}-(-\pi )^{4}}{2})\right) \\  & =-2\left(2\pi\right) \end{aligned}
$$

---

### original parameterized evidence — moderate
Template: `polynomial_sine`; profile: `raw:q-162235`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=(x+y)\,i-z\,k$ along the closed curve $C$ given by $r(t)=(1-{t}^{2})\,i+{t}^{2}\,j+\operatorname{sin}⁡(\pi t)\,k$ for $t\in [-1,1).$

- A. $0$ **Correct**
- B. $2$
- C. $-2\pi $
- D. $-2$
- E. $-\pi $

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ={∮}_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=1-{t}^{2},\,y={t}^{2},\,z=\operatorname{sin}⁡(\pi t).
$$

So,

$$
\begin{aligned}F(r(t)) & =(x+y)\,i-z\,k \\  & =(1-{t}^{2}+{t}^{2})\,i-\operatorname{sin}⁡(\pi t)\,k \\  & =i-\operatorname{sin}⁡(\pi t)\,k.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(1-{t}^{2})\,i+\frac{\text{d}}{\text{d}t}({t}^{2})\,j+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(\pi t))\,k \\  & =-2t\,i+2t\,j+\pi \operatorname{cos}⁡(\pi t)\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(i-\operatorname{sin}⁡(\pi t)\,k)\cdot (-2t\,i+2t\,j+\pi \operatorname{cos}⁡(\pi t)\,k) \\  & =1\cdot (-2t)+0\cdot 2t+\operatorname{sin}⁡(\pi t)\cdot \pi \operatorname{cos}⁡(\pi t) \\  & =-2t+\frac{\pi }{2}\operatorname{sin}⁡(2\pi t).\end{aligned}
$$

 

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ={∮}_{C}F\cdot \text{d}r & ={\int }_{-1}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{-1}^{1}(-2t+\frac{\pi }{2}\operatorname{sin}⁡(2\pi t))\,\text{d}t \\  & ={[-{t}^{2}-\frac{\operatorname{cos}⁡(2\pi t)}{4}]}_{-1}^{1} \\  & =(-1-\frac{1}{4})-(-1-\frac{1}{4}) \\  & =0\end{aligned}
$$

---

### generated opaque evidence pattern — moderate
Template: `polynomial_sine`; profile: `raw:q-162235`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=2\left((x+y)\,i-z\,k\right)$ along the closed curve $C$ given by $r(t)=(1-{t}^{2})\,i+{t}^{2}\,j+\operatorname{sin}⁡(\pi t)\,k$ for $t\in [-1,1).$

- A. $- 2 \pi$
- B. $-4$
- C. $4$
- D. $0$ **Correct**
- E. $- 4 \pi$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ={∮}_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=1-{t}^{2},\,y={t}^{2},\,z=\operatorname{sin}⁡(\pi t).
$$

So,

$$
\begin{aligned}F(r(t)) & =2\left((x+y)\,i-z\,k\right) \\  & =2\left((1-{t}^{2}+{t}^{2})\,i-\operatorname{sin}⁡(\pi t)\,k\right) \\  & =2\left(i-\operatorname{sin}⁡(\pi t)\,k\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(1-{t}^{2})\,i+\frac{\text{d}}{\text{d}t}({t}^{2})\,j+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(\pi t))\,k \\  & =-2t\,i+2t\,j+\pi \operatorname{cos}⁡(\pi t)\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =2\left((i-\operatorname{sin}⁡(\pi t)\,k)\cdot (-2t\,i+2t\,j+\pi \operatorname{cos}⁡(\pi t)\,k)\right) \\  & =2\left(1\cdot (-2t)+0\cdot 2t+\operatorname{sin}⁡(\pi t)\cdot \pi \operatorname{cos}⁡(\pi t)\right) \\  & =2\left(-2t+\frac{\pi }{2}\operatorname{sin}⁡(2\pi t)\right).\end{aligned}
$$

 

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ={∮}_{C}F\cdot \text{d}r & ={\int }_{-1}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =2\left({\int }_{-1}^{1}(-2t+\frac{\pi }{2}\operatorname{sin}⁡(2\pi t))\,\text{d}t\right) \\  & =2\left({[-{t}^{2}-\frac{\operatorname{cos}⁡(2\pi t)}{4}]}_{-1}^{1}\right) \\  & =2\left((-1-\frac{1}{4})-(-1-\frac{1}{4})\right) \\  & =2\left(0\right)\end{aligned}
$$

---

### generated opaque evidence pattern — moderate
Template: `polynomial_sine`; profile: `raw:q-162235`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=-2\left((x+y)\,i-z\,k\right)$ along the closed curve $C$ given by $r(t)=(1-{t}^{2})\,i+{t}^{2}\,j+\operatorname{sin}⁡(\pi t)\,k$ for $t\in [-1,1).$

- A. $2 \pi$
- B. $4$
- C. $-4$
- D. $0$ **Correct**
- E. $4 \pi$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ={∮}_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=1-{t}^{2},\,y={t}^{2},\,z=\operatorname{sin}⁡(\pi t).
$$

So,

$$
\begin{aligned}F(r(t)) & =-2\left((x+y)\,i-z\,k\right) \\  & =-2\left((1-{t}^{2}+{t}^{2})\,i-\operatorname{sin}⁡(\pi t)\,k\right) \\  & =-2\left(i-\operatorname{sin}⁡(\pi t)\,k\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(1-{t}^{2})\,i+\frac{\text{d}}{\text{d}t}({t}^{2})\,j+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(\pi t))\,k \\  & =-2t\,i+2t\,j+\pi \operatorname{cos}⁡(\pi t)\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =-2\left((i-\operatorname{sin}⁡(\pi t)\,k)\cdot (-2t\,i+2t\,j+\pi \operatorname{cos}⁡(\pi t)\,k)\right) \\  & =-2\left(1\cdot (-2t)+0\cdot 2t+\operatorname{sin}⁡(\pi t)\cdot \pi \operatorname{cos}⁡(\pi t)\right) \\  & =-2\left(-2t+\frac{\pi }{2}\operatorname{sin}⁡(2\pi t)\right).\end{aligned}
$$

 

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ={∮}_{C}F\cdot \text{d}r & ={\int }_{-1}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =-2\left({\int }_{-1}^{1}(-2t+\frac{\pi }{2}\operatorname{sin}⁡(2\pi t))\,\text{d}t\right) \\  & =-2\left({[-{t}^{2}-\frac{\operatorname{cos}⁡(2\pi t)}{4}]}_{-1}^{1}\right) \\  & =-2\left((-1-\frac{1}{4})-(-1-\frac{1}{4})\right) \\  & =-2\left(0\right)\end{aligned}
$$

---

### original parameterized evidence — easy
Template: `yz_rotation`; profile: `raw:q-162237`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=-z\,j+y\,k$ along the closed curve $C$ given by $r(t)=\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j+\operatorname{sin}⁡t\,k$ for $t\in [0,2\pi ).$

- A. $4\pi $
- B. $0$
- C. $\pi $
- D. $2\pi $ **Correct**
- E. $-\pi $

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ={∮}_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=\operatorname{sin}⁡t,\,y=\operatorname{cos}⁡t,\,z=\operatorname{sin}⁡t.
$$

So,

$$
\begin{aligned}F(r(t)) & =-z\,j+y\,k \\  & =-\operatorname{sin}⁡t\,j+\operatorname{cos}⁡t\,k.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)\,j+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,k \\  & =\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j+\operatorname{cos}⁡t\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(-\operatorname{sin}⁡t\,j+\operatorname{cos}⁡t\,k)\cdot (\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j+\operatorname{cos}⁡t\,k) \\  & =0\cdot \operatorname{cos}⁡t+(-\operatorname{sin}⁡t)\cdot (-\operatorname{sin}⁡t)+\operatorname{cos}⁡t\cdot \operatorname{cos}⁡t \\  & ={sin}^{2}⁡t+{cos}^{2}⁡t. \\  & =1.\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ={∮}_{C}F\cdot \text{d}r & ={\int }_{0}^{2\pi }F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{2\pi }1\,\text{d}t \\  & =[t]_{0}^{2\pi } \\  & =2\pi \end{aligned}
$$

---

### generated opaque evidence pattern — easy
Template: `yz_rotation`; profile: `raw:q-162237`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=2\left(-z\,j+y\,k\right)$ along the closed curve $C$ given by $r(t)=\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j+\operatorname{sin}⁡t\,k$ for $t\in [0,2\pi ).$

- A. $- 2 \pi$
- B. $4 \pi$ **Correct**
- C. $0$
- D. $8 \pi$
- E. $2 \pi$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ={∮}_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=\operatorname{sin}⁡t,\,y=\operatorname{cos}⁡t,\,z=\operatorname{sin}⁡t.
$$

So,

$$
\begin{aligned}F(r(t)) & =2\left(-z\,j+y\,k\right) \\  & =2\left(-\operatorname{sin}⁡t\,j+\operatorname{cos}⁡t\,k\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)\,j+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,k \\  & =\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j+\operatorname{cos}⁡t\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =2\left((-\operatorname{sin}⁡t\,j+\operatorname{cos}⁡t\,k)\cdot (\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j+\operatorname{cos}⁡t\,k)\right) \\  & =2\left(0\cdot \operatorname{cos}⁡t+(-\operatorname{sin}⁡t)\cdot (-\operatorname{sin}⁡t)+\operatorname{cos}⁡t\cdot \operatorname{cos}⁡t\right) \\  & =2\left({sin}^{2}⁡t+{cos}^{2}⁡t\right). \\  & =2\left(1\right).\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ={∮}_{C}F\cdot \text{d}r & ={\int }_{0}^{2\pi }F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =2\left({\int }_{0}^{2\pi }1\,\text{d}t\right) \\  & =2\left([t]_{0}^{2\pi }\right) \\  & =2\left(2\pi\right) \end{aligned}
$$

---

### generated opaque evidence pattern — easy
Template: `yz_rotation`; profile: `raw:q-162237`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=-2\left(-z\,j+y\,k\right)$ along the closed curve $C$ given by $r(t)=\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j+\operatorname{sin}⁡t\,k$ for $t\in [0,2\pi ).$

- A. $2 \pi$
- B. $- 4 \pi$ **Correct**
- C. $0$
- D. $- 8 \pi$
- E. $- 2 \pi$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ={∮}_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=\operatorname{sin}⁡t,\,y=\operatorname{cos}⁡t,\,z=\operatorname{sin}⁡t.
$$

So,

$$
\begin{aligned}F(r(t)) & =-2\left(-z\,j+y\,k\right) \\  & =-2\left(-\operatorname{sin}⁡t\,j+\operatorname{cos}⁡t\,k\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)\,j+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,k \\  & =\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j+\operatorname{cos}⁡t\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =-2\left((-\operatorname{sin}⁡t\,j+\operatorname{cos}⁡t\,k)\cdot (\operatorname{cos}⁡t\,i-\operatorname{sin}⁡t\,j+\operatorname{cos}⁡t\,k)\right) \\  & =-2\left(0\cdot \operatorname{cos}⁡t+(-\operatorname{sin}⁡t)\cdot (-\operatorname{sin}⁡t)+\operatorname{cos}⁡t\cdot \operatorname{cos}⁡t\right) \\  & =-2\left({sin}^{2}⁡t+{cos}^{2}⁡t\right). \\  & =-2\left(1\right).\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ={∮}_{C}F\cdot \text{d}r & ={\int }_{0}^{2\pi }F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =-2\left({\int }_{0}^{2\pi }1\,\text{d}t\right) \\  & =-2\left([t]_{0}^{2\pi }\right) \\  & =-2\left(2\pi\right) \end{aligned}
$$

---

### original parameterized evidence — easy
Template: `xy_rotation`; profile: `raw:q-162229`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=-y\,i+x\,j$ along the closed curve $C$ given by $r(t)=2\operatorname{cos}⁡(\pi t)\,i+\operatorname{sin}⁡(\pi t)\,j+2\,k$ for $t\in [0,2).$

- A. $-2\pi $
- B. $\frac{\pi }{2}$
- C. $\pi $
- D. $4\pi $ **Correct**
- E. $-\frac{2}{\pi }$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ={∮}_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=2\operatorname{cos}⁡(\pi t),\,y=\operatorname{sin}⁡(\pi t),\,z=2.
$$

So,

$$
\begin{aligned}F(r(t)) & =-y\,i+x\,j \\  & =-\operatorname{sin}⁡(\pi t)\,i+2\operatorname{cos}⁡(\pi t)\,j.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2\operatorname{cos}⁡(\pi t))\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(\pi t))\,j+\frac{\text{d}}{\text{d}t}(2)\,k \\  & =-2\pi \operatorname{sin}⁡(\pi t)\,i+\pi \operatorname{cos}⁡(\pi t)\,j+0\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(-\operatorname{sin}⁡(\pi t)\,i+2\operatorname{cos}⁡(\pi t)\,j)\cdot (-2\pi \operatorname{sin}⁡(\pi t)\,i+\pi \operatorname{cos}⁡(\pi t)\,j+0\,k) \\  & =-\operatorname{sin}⁡(\pi t)\cdot (-2\pi \operatorname{sin}⁡(\pi t))+2\operatorname{cos}⁡(\pi t)\cdot \pi \operatorname{cos}⁡(\pi t)+0\cdot 0 \\  & =2\pi {sin}^{2}⁡(\pi t)+2\pi {cos}^{2}⁡(\pi t) \\  & =2\pi .\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ={∮}_{C}F\cdot \text{d}r & ={\int }_{0}^{2}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{2}2\pi \,\text{d}t \\  & =2\pi [t]_{0}^{2} \\  & =2\pi (2-0) \\  & =4\pi \end{aligned}
$$

---

### generated opaque evidence pattern — easy
Template: `xy_rotation`; profile: `raw:q-162229`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=2\left(-y\,i+x\,j\right)$ along the closed curve $C$ given by $r(t)=2\operatorname{cos}⁡(\pi t)\,i+\operatorname{sin}⁡(\pi t)\,j+2\,k$ for $t\in [0,2).$

- A. $- \frac{4}{\pi}$
- B. $8 \pi$ **Correct**
- C. $\pi$
- D. $- 4 \pi$
- E. $2 \pi$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ={∮}_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=2\operatorname{cos}⁡(\pi t),\,y=\operatorname{sin}⁡(\pi t),\,z=2.
$$

So,

$$
\begin{aligned}F(r(t)) & =2\left(-y\,i+x\,j\right) \\  & =2\left(-\operatorname{sin}⁡(\pi t)\,i+2\operatorname{cos}⁡(\pi t)\,j\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2\operatorname{cos}⁡(\pi t))\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(\pi t))\,j+\frac{\text{d}}{\text{d}t}(2)\,k \\  & =-2\pi \operatorname{sin}⁡(\pi t)\,i+\pi \operatorname{cos}⁡(\pi t)\,j+0\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =2\left((-\operatorname{sin}⁡(\pi t)\,i+2\operatorname{cos}⁡(\pi t)\,j)\cdot (-2\pi \operatorname{sin}⁡(\pi t)\,i+\pi \operatorname{cos}⁡(\pi t)\,j+0\,k)\right) \\  & =2\left(-\operatorname{sin}⁡(\pi t)\cdot (-2\pi \operatorname{sin}⁡(\pi t))+2\operatorname{cos}⁡(\pi t)\cdot \pi \operatorname{cos}⁡(\pi t)+0\cdot 0\right) \\  & =2\left(2\pi {sin}^{2}⁡(\pi t)+2\pi {cos}^{2}⁡(\pi t)\right) \\  & =2\left(2\pi\right) .\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ={∮}_{C}F\cdot \text{d}r & ={\int }_{0}^{2}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =2\left({\int }_{0}^{2}2\pi \,\text{d}t\right) \\  & =2\left(2\pi [t]_{0}^{2}\right) \\  & =2\left(2\pi (2-0)\right) \\  & =2\left(4\pi\right) \end{aligned}
$$

---

### generated opaque evidence pattern — easy
Template: `xy_rotation`; profile: `raw:q-162229`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=-2\left(-y\,i+x\,j\right)$ along the closed curve $C$ given by $r(t)=2\operatorname{cos}⁡(\pi t)\,i+\operatorname{sin}⁡(\pi t)\,j+2\,k$ for $t\in [0,2).$

- A. $\frac{4}{\pi}$
- B. $- 8 \pi$ **Correct**
- C. $- \pi$
- D. $4 \pi$
- E. $- 2 \pi$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ={∮}_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x=2\operatorname{cos}⁡(\pi t),\,y=\operatorname{sin}⁡(\pi t),\,z=2.
$$

So,

$$
\begin{aligned}F(r(t)) & =-2\left(-y\,i+x\,j\right) \\  & =-2\left(-\operatorname{sin}⁡(\pi t)\,i+2\operatorname{cos}⁡(\pi t)\,j\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}(2\operatorname{cos}⁡(\pi t))\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(\pi t))\,j+\frac{\text{d}}{\text{d}t}(2)\,k \\  & =-2\pi \operatorname{sin}⁡(\pi t)\,i+\pi \operatorname{cos}⁡(\pi t)\,j+0\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =-2\left((-\operatorname{sin}⁡(\pi t)\,i+2\operatorname{cos}⁡(\pi t)\,j)\cdot (-2\pi \operatorname{sin}⁡(\pi t)\,i+\pi \operatorname{cos}⁡(\pi t)\,j+0\,k)\right) \\  & =-2\left(-\operatorname{sin}⁡(\pi t)\cdot (-2\pi \operatorname{sin}⁡(\pi t))+2\operatorname{cos}⁡(\pi t)\cdot \pi \operatorname{cos}⁡(\pi t)+0\cdot 0\right) \\  & =-2\left(2\pi {sin}^{2}⁡(\pi t)+2\pi {cos}^{2}⁡(\pi t)\right) \\  & =-2\left(2\pi\right) .\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ={∮}_{C}F\cdot \text{d}r & ={\int }_{0}^{2}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =-2\left({\int }_{0}^{2}2\pi \,\text{d}t\right) \\  & =-2\left(2\pi [t]_{0}^{2}\right) \\  & =-2\left(2\pi (2-0)\right) \\  & =-2\left(4\pi\right) \end{aligned}
$$

---

### original parameterized evidence — easy
Template: `yz_rotation`; profile: `raw:q-162228`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=z\,j-y\,k$ along the closed curve $C$ given by $r(t)=({t}^{2}-t)\,i+\operatorname{cos}⁡(2\pi t)\,j+\operatorname{sin}⁡(2\pi t)\,k$ for $t\in [0,1)$

- A. $0$
- B. $-\pi $
- C. $-2\pi $ **Correct**
- D. $2\pi $
- E. $4\pi $

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ={∮}_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x={t}^{2}-t,\,y=\operatorname{cos}⁡(2\pi t),\,z=\operatorname{sin}⁡(2\pi t).
$$

So,

$$
\begin{aligned}F(r(t)) & =z\,j-y\,k \\  & =\operatorname{sin}⁡(2\pi t)\,j-\operatorname{cos}⁡(2\pi t)\,k.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{2}-t)\,i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡(2\pi t))\,j+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(2\pi t))\,k \\  & =(2t-1)\,i-2\pi \operatorname{sin}⁡(2\pi t)\,j+2\pi \operatorname{cos}⁡(2\pi t)\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(\operatorname{sin}⁡(2\pi t)\,j-\operatorname{cos}⁡(2\pi t)\,k)\cdot ((2t-1)\,i-2\pi \operatorname{sin}⁡(2\pi t)\,j+2\pi \operatorname{cos}⁡(2\pi t)\,k) \\  & =0\cdot (2t-1)+\operatorname{sin}⁡(2\pi t)\cdot (-2\pi \operatorname{sin}⁡(2\pi t))+(-\operatorname{cos}⁡(2\pi t))\cdot 2\pi \operatorname{cos}⁡(2\pi t) \\  & =-2\pi {sin}^{2}⁡(2\pi t)-2\pi {cos}^{2}⁡(2\pi t) \\  & =-2\pi .\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ={∮}_{C}F\cdot \text{d}r & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{1}(-2\pi )\,\text{d}t \\  & =-2\pi [t]_{0}^{1} \\  & =-2\pi (1-0) \\  & =-2\pi \end{aligned}
$$

---

### generated opaque evidence pattern — easy
Template: `yz_rotation`; profile: `raw:q-162228`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=2\left(z\,j-y\,k\right)$ along the closed curve $C$ given by $r(t)=({t}^{2}-t)\,i+\operatorname{cos}⁡(2\pi t)\,j+\operatorname{sin}⁡(2\pi t)\,k$ for $t\in [0,1)$

- A. $8 \pi$
- B. $4 \pi$
- C. $- 2 \pi$
- D. $0$
- E. $- 4 \pi$ **Correct**

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ={∮}_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x={t}^{2}-t,\,y=\operatorname{cos}⁡(2\pi t),\,z=\operatorname{sin}⁡(2\pi t).
$$

So,

$$
\begin{aligned}F(r(t)) & =2\left(z\,j-y\,k\right) \\  & =2\left(\operatorname{sin}⁡(2\pi t)\,j-\operatorname{cos}⁡(2\pi t)\,k\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{2}-t)\,i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡(2\pi t))\,j+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(2\pi t))\,k \\  & =(2t-1)\,i-2\pi \operatorname{sin}⁡(2\pi t)\,j+2\pi \operatorname{cos}⁡(2\pi t)\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =2\left((\operatorname{sin}⁡(2\pi t)\,j-\operatorname{cos}⁡(2\pi t)\,k)\cdot ((2t-1)\,i-2\pi \operatorname{sin}⁡(2\pi t)\,j+2\pi \operatorname{cos}⁡(2\pi t)\,k)\right) \\  & =2\left(0\cdot (2t-1)+\operatorname{sin}⁡(2\pi t)\cdot (-2\pi \operatorname{sin}⁡(2\pi t))+(-\operatorname{cos}⁡(2\pi t))\cdot 2\pi \operatorname{cos}⁡(2\pi t)\right) \\  & =2\left(-2\pi {sin}^{2}⁡(2\pi t)-2\pi {cos}^{2}⁡(2\pi t)\right) \\  & =2\left(-2\pi\right) .\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ={∮}_{C}F\cdot \text{d}r & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =2\left({\int }_{0}^{1}(-2\pi )\,\text{d}t\right) \\  & =2\left(-2\pi [t]_{0}^{1}\right) \\  & =2\left(-2\pi (1-0)\right) \\  & =2\left(-2\pi\right) \end{aligned}
$$

---

### generated opaque evidence pattern — easy
Template: `yz_rotation`; profile: `raw:q-162228`; eligible: False

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=-2\left(z\,j-y\,k\right)$ along the closed curve $C$ given by $r(t)=({t}^{2}-t)\,i+\operatorname{cos}⁡(2\pi t)\,j+\operatorname{sin}⁡(2\pi t)\,k$ for $t\in [0,1)$

- A. $- 8 \pi$
- B. $- 4 \pi$
- C. $2 \pi$
- D. $0$
- E. $4 \pi$ **Correct**

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ={∮}_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have

$$
x={t}^{2}-t,\,y=\operatorname{cos}⁡(2\pi t),\,z=\operatorname{sin}⁡(2\pi t).
$$

So,

$$
\begin{aligned}F(r(t)) & =-2\left(z\,j-y\,k\right) \\  & =-2\left(\operatorname{sin}⁡(2\pi t)\,j-\operatorname{cos}⁡(2\pi t)\,k\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{2}-t)\,i+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡(2\pi t))\,j+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡(2\pi t))\,k \\  & =(2t-1)\,i-2\pi \operatorname{sin}⁡(2\pi t)\,j+2\pi \operatorname{cos}⁡(2\pi t)\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =-2\left((\operatorname{sin}⁡(2\pi t)\,j-\operatorname{cos}⁡(2\pi t)\,k)\cdot ((2t-1)\,i-2\pi \operatorname{sin}⁡(2\pi t)\,j+2\pi \operatorname{cos}⁡(2\pi t)\,k)\right) \\  & =-2\left(0\cdot (2t-1)+\operatorname{sin}⁡(2\pi t)\cdot (-2\pi \operatorname{sin}⁡(2\pi t))+(-\operatorname{cos}⁡(2\pi t))\cdot 2\pi \operatorname{cos}⁡(2\pi t)\right) \\  & =-2\left(-2\pi {sin}^{2}⁡(2\pi t)-2\pi {cos}^{2}⁡(2\pi t)\right) \\  & =-2\left(-2\pi\right) .\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ={∮}_{C}F\cdot \text{d}r & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =-2\left({\int }_{0}^{1}(-2\pi )\,\text{d}t\right) \\  & =-2\left(-2\pi [t]_{0}^{1}\right) \\  & =-2\left(-2\pi (1-0)\right) \\  & =-2\left(-2\pi\right) \end{aligned}
$$

---

### authored same-method extension — easy
Template: `xy_rotation`; profile: `authored-method`; eligible: True

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=\left(- y\right)\,i+\left(x\right)\,j+\left(0\right)\,k$ along the closed curve $C$ given by $r(t)=\left(4 \cos{\left(\pi t \right)}\right)\,i+\left(3 \sin{\left(\pi t \right)}\right)\,j+\left(1 - t^{2}\right)\,k$ for $t\in [-1,1).$

- A. $48 \pi$
- B. $24 \pi$ **Correct**
- C. $- 24 \pi$
- D. $12 \pi$
- E. $0$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ=\oint_C F\cdot\mathrm dr=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm dt.
$$

Along the curve $C,$ we have

$$
x=4 \cos{\left(\pi t \right)},\quad y=3 \sin{\left(\pi t \right)},\quad z=1 - t^{2}.
$$

So,

$$
\begin{aligned}F(r(t)) & =\left(- y\right)\,i+\left(x\right)\,j+\left(0\right)\,k \\ & =\left(- 3 \sin{\left(\pi t \right)}\right)\,i+\left(4 \cos{\left(\pi t \right)}\right)\,j+\left(0\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm d}{\mathrm dt}\left(4 \cos{\left(\pi t \right)}\right)\,i+\frac{\mathrm d}{\mathrm dt}\left(3 \sin{\left(\pi t \right)}\right)\,j+\frac{\mathrm d}{\mathrm dt}\left(1 - t^{2}\right)\,k \\ & =\left(- 4 \pi \sin{\left(\pi t \right)}\right)\,i+\left(3 \pi \cos{\left(\pi t \right)}\right)\,j+\left(- 2 t\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(- 3 \sin{\left(\pi t \right)}\right)\,i+\left(4 \cos{\left(\pi t \right)}\right)\,j+\left(0\right)\,k\right)\cdot\left(\left(- 4 \pi \sin{\left(\pi t \right)}\right)\,i+\left(3 \pi \cos{\left(\pi t \right)}\right)\,j+\left(- 2 t\right)\,k\right) \\ & =\left(- 3 \sin{\left(\pi t \right)}\right)\cdot\left(- 4 \pi \sin{\left(\pi t \right)}\right)+\left(4 \cos{\left(\pi t \right)}\right)\cdot\left(3 \pi \cos{\left(\pi t \right)}\right)+\left(0\right)\cdot\left(- 2 t\right) \\ & =\left(12 \pi \sin^{2}{\left(\pi t \right)}\right)+\left(12 \pi \cos^{2}{\left(\pi t \right)}\right)+\left(0\right) \\ & =12 \pi\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ=\oint_C F\cdot\mathrm dr & =\int_{-1}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm dt \\ & =\int_{-1}^{1}\left(12 \pi\right)\,\mathrm dt \\ & =\left[12 \pi t\right]_{-1}^{1} \\ & =[\left(12 \pi\right)]-[\left(- 12 \pi\right)] \\ & =24 \pi\end{aligned}
$$

---

### authored same-method extension — easy
Template: `xy_rotation`; profile: `authored-method`; eligible: True

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=\left(- y\right)\,i+\left(x\right)\,j+\left(0\right)\,k$ along the closed curve $C$ given by $r(t)=\left(2 \cos{\left(\pi t \right)}\right)\,i+\left(3 \sin{\left(\pi t \right)}\right)\,j+\left(1 - t^{2}\right)\,k$ for $t\in [-1,1).$

- A. $24 \pi$
- B. $12 \pi$ **Correct**
- C. $- 12 \pi$
- D. $6 \pi$
- E. $0$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ=\oint_C F\cdot\mathrm dr=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm dt.
$$

Along the curve $C,$ we have

$$
x=2 \cos{\left(\pi t \right)},\quad y=3 \sin{\left(\pi t \right)},\quad z=1 - t^{2}.
$$

So,

$$
\begin{aligned}F(r(t)) & =\left(- y\right)\,i+\left(x\right)\,j+\left(0\right)\,k \\ & =\left(- 3 \sin{\left(\pi t \right)}\right)\,i+\left(2 \cos{\left(\pi t \right)}\right)\,j+\left(0\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm d}{\mathrm dt}\left(2 \cos{\left(\pi t \right)}\right)\,i+\frac{\mathrm d}{\mathrm dt}\left(3 \sin{\left(\pi t \right)}\right)\,j+\frac{\mathrm d}{\mathrm dt}\left(1 - t^{2}\right)\,k \\ & =\left(- 2 \pi \sin{\left(\pi t \right)}\right)\,i+\left(3 \pi \cos{\left(\pi t \right)}\right)\,j+\left(- 2 t\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(- 3 \sin{\left(\pi t \right)}\right)\,i+\left(2 \cos{\left(\pi t \right)}\right)\,j+\left(0\right)\,k\right)\cdot\left(\left(- 2 \pi \sin{\left(\pi t \right)}\right)\,i+\left(3 \pi \cos{\left(\pi t \right)}\right)\,j+\left(- 2 t\right)\,k\right) \\ & =\left(- 3 \sin{\left(\pi t \right)}\right)\cdot\left(- 2 \pi \sin{\left(\pi t \right)}\right)+\left(2 \cos{\left(\pi t \right)}\right)\cdot\left(3 \pi \cos{\left(\pi t \right)}\right)+\left(0\right)\cdot\left(- 2 t\right) \\ & =\left(6 \pi \sin^{2}{\left(\pi t \right)}\right)+\left(6 \pi \cos^{2}{\left(\pi t \right)}\right)+\left(0\right) \\ & =6 \pi\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ=\oint_C F\cdot\mathrm dr & =\int_{-1}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm dt \\ & =\int_{-1}^{1}\left(6 \pi\right)\,\mathrm dt \\ & =\left[6 \pi t\right]_{-1}^{1} \\ & =[\left(6 \pi\right)]-[\left(- 6 \pi\right)] \\ & =12 \pi\end{aligned}
$$

---

### authored same-method extension — easy
Template: `xy_rotation_z`; profile: `authored-method`; eligible: True

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=\left(y\right)\,i+\left(- x\right)\,j+\left(z\right)\,k$ along the closed curve $C$ given by $r(t)=\left(4 \sin{\left(t \right)}\right)\,i+\left(3 \cos{\left(t \right)}\right)\,j+\left(t^{2}\right)\,k$ for $t\in [- \pi,\pi).$

- A. $48 \pi$
- B. $24 \pi$ **Correct**
- C. $- 24 \pi$
- D. $12 \pi$
- E. $0$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ=\oint_C F\cdot\mathrm dr=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm dt.
$$

Along the curve $C,$ we have

$$
x=4 \sin{\left(t \right)},\quad y=3 \cos{\left(t \right)},\quad z=t^{2}.
$$

So,

$$
\begin{aligned}F(r(t)) & =\left(y\right)\,i+\left(- x\right)\,j+\left(z\right)\,k \\ & =\left(3 \cos{\left(t \right)}\right)\,i+\left(- 4 \sin{\left(t \right)}\right)\,j+\left(t^{2}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm d}{\mathrm dt}\left(4 \sin{\left(t \right)}\right)\,i+\frac{\mathrm d}{\mathrm dt}\left(3 \cos{\left(t \right)}\right)\,j+\frac{\mathrm d}{\mathrm dt}\left(t^{2}\right)\,k \\ & =\left(4 \cos{\left(t \right)}\right)\,i+\left(- 3 \sin{\left(t \right)}\right)\,j+\left(2 t\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(3 \cos{\left(t \right)}\right)\,i+\left(- 4 \sin{\left(t \right)}\right)\,j+\left(t^{2}\right)\,k\right)\cdot\left(\left(4 \cos{\left(t \right)}\right)\,i+\left(- 3 \sin{\left(t \right)}\right)\,j+\left(2 t\right)\,k\right) \\ & =\left(3 \cos{\left(t \right)}\right)\cdot\left(4 \cos{\left(t \right)}\right)+\left(- 4 \sin{\left(t \right)}\right)\cdot\left(- 3 \sin{\left(t \right)}\right)+\left(t^{2}\right)\cdot\left(2 t\right) \\ & =\left(12 \cos^{2}{\left(t \right)}\right)+\left(12 \sin^{2}{\left(t \right)}\right)+\left(2 t^{3}\right) \\ & =2 t^{3} + 12\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ=\oint_C F\cdot\mathrm dr & =\int_{- \pi}^{\pi}F(r(t))\cdot r^{\prime}(t)\,\mathrm dt \\ & =\int_{- \pi}^{\pi}\left(2 t^{3} + 12\right)\,\mathrm dt \\ & =\left[\frac{t^{4}}{2} + 12 t\right]_{- \pi}^{\pi} \\ & =[\left(12 \pi\right)+\left(\frac{\pi^{4}}{2}\right)]-[\left(- 12 \pi\right)+\left(\frac{\pi^{4}}{2}\right)] \\ & =24 \pi\end{aligned}
$$

---

### authored same-method extension — easy
Template: `xy_rotation_z`; profile: `authored-method`; eligible: True

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=\left(y\right)\,i+\left(- x\right)\,j+\left(z\right)\,k$ along the closed curve $C$ given by $r(t)=\left(2 \sin{\left(t \right)}\right)\,i+\left(3 \cos{\left(t \right)}\right)\,j+\left(t^{2}\right)\,k$ for $t\in [- \pi,\pi).$

- A. $24 \pi$
- B. $12 \pi$ **Correct**
- C. $- 12 \pi$
- D. $6 \pi$
- E. $0$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ=\oint_C F\cdot\mathrm dr=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm dt.
$$

Along the curve $C,$ we have

$$
x=2 \sin{\left(t \right)},\quad y=3 \cos{\left(t \right)},\quad z=t^{2}.
$$

So,

$$
\begin{aligned}F(r(t)) & =\left(y\right)\,i+\left(- x\right)\,j+\left(z\right)\,k \\ & =\left(3 \cos{\left(t \right)}\right)\,i+\left(- 2 \sin{\left(t \right)}\right)\,j+\left(t^{2}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm d}{\mathrm dt}\left(2 \sin{\left(t \right)}\right)\,i+\frac{\mathrm d}{\mathrm dt}\left(3 \cos{\left(t \right)}\right)\,j+\frac{\mathrm d}{\mathrm dt}\left(t^{2}\right)\,k \\ & =\left(2 \cos{\left(t \right)}\right)\,i+\left(- 3 \sin{\left(t \right)}\right)\,j+\left(2 t\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(3 \cos{\left(t \right)}\right)\,i+\left(- 2 \sin{\left(t \right)}\right)\,j+\left(t^{2}\right)\,k\right)\cdot\left(\left(2 \cos{\left(t \right)}\right)\,i+\left(- 3 \sin{\left(t \right)}\right)\,j+\left(2 t\right)\,k\right) \\ & =\left(3 \cos{\left(t \right)}\right)\cdot\left(2 \cos{\left(t \right)}\right)+\left(- 2 \sin{\left(t \right)}\right)\cdot\left(- 3 \sin{\left(t \right)}\right)+\left(t^{2}\right)\cdot\left(2 t\right) \\ & =\left(6 \cos^{2}{\left(t \right)}\right)+\left(6 \sin^{2}{\left(t \right)}\right)+\left(2 t^{3}\right) \\ & =2 t^{3} + 6\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ=\oint_C F\cdot\mathrm dr & =\int_{- \pi}^{\pi}F(r(t))\cdot r^{\prime}(t)\,\mathrm dt \\ & =\int_{- \pi}^{\pi}\left(2 t^{3} + 6\right)\,\mathrm dt \\ & =\left[\frac{t^{4}}{2} + 6 t\right]_{- \pi}^{\pi} \\ & =[\left(6 \pi\right)+\left(\frac{\pi^{4}}{2}\right)]-[\left(- 6 \pi\right)+\left(\frac{\pi^{4}}{2}\right)] \\ & =12 \pi\end{aligned}
$$

---

### authored same-method extension — easy
Template: `yz_rotation`; profile: `authored-method`; eligible: True

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=\left(0\right)\,i+\left(z\right)\,j+\left(- y\right)\,k$ along the closed curve $C$ given by $r(t)=\left(t^{2} - t\right)\,i+\left(4 \cos{\left(2 \pi t \right)}\right)\,j+\left(3 \sin{\left(2 \pi t \right)}\right)\,k$ for $t\in [0,1).$

- A. $- 48 \pi$
- B. $- 24 \pi$ **Correct**
- C. $24 \pi$
- D. $- 12 \pi$
- E. $0$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ=\oint_C F\cdot\mathrm dr=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm dt.
$$

Along the curve $C,$ we have

$$
x=t^{2} - t,\quad y=4 \cos{\left(2 \pi t \right)},\quad z=3 \sin{\left(2 \pi t \right)}.
$$

So,

$$
\begin{aligned}F(r(t)) & =\left(0\right)\,i+\left(z\right)\,j+\left(- y\right)\,k \\ & =\left(0\right)\,i+\left(3 \sin{\left(2 \pi t \right)}\right)\,j+\left(- 4 \cos{\left(2 \pi t \right)}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm d}{\mathrm dt}\left(t^{2} - t\right)\,i+\frac{\mathrm d}{\mathrm dt}\left(4 \cos{\left(2 \pi t \right)}\right)\,j+\frac{\mathrm d}{\mathrm dt}\left(3 \sin{\left(2 \pi t \right)}\right)\,k \\ & =\left(2 t - 1\right)\,i+\left(- 8 \pi \sin{\left(2 \pi t \right)}\right)\,j+\left(6 \pi \cos{\left(2 \pi t \right)}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(0\right)\,i+\left(3 \sin{\left(2 \pi t \right)}\right)\,j+\left(- 4 \cos{\left(2 \pi t \right)}\right)\,k\right)\cdot\left(\left(2 t - 1\right)\,i+\left(- 8 \pi \sin{\left(2 \pi t \right)}\right)\,j+\left(6 \pi \cos{\left(2 \pi t \right)}\right)\,k\right) \\ & =\left(0\right)\cdot\left(2 t - 1\right)+\left(3 \sin{\left(2 \pi t \right)}\right)\cdot\left(- 8 \pi \sin{\left(2 \pi t \right)}\right)+\left(- 4 \cos{\left(2 \pi t \right)}\right)\cdot\left(6 \pi \cos{\left(2 \pi t \right)}\right) \\ & =\left(0\right)+\left(- 24 \pi \sin^{2}{\left(2 \pi t \right)}\right)+\left(- 24 \pi \cos^{2}{\left(2 \pi t \right)}\right) \\ & =- 24 \pi\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ=\oint_C F\cdot\mathrm dr & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm dt \\ & =\int_{0}^{1}\left(- 24 \pi\right)\,\mathrm dt \\ & =\left[- 24 \pi t\right]_{0}^{1} \\ & =[\left(- 24 \pi\right)]-[\left(0\right)] \\ & =- 24 \pi\end{aligned}
$$

---

### authored same-method extension — easy
Template: `yz_rotation`; profile: `authored-method`; eligible: True

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=\left(0\right)\,i+\left(z\right)\,j+\left(- y\right)\,k$ along the closed curve $C$ given by $r(t)=\left(t^{2} - t\right)\,i+\left(2 \cos{\left(2 \pi t \right)}\right)\,j+\left(3 \sin{\left(2 \pi t \right)}\right)\,k$ for $t\in [0,1).$

- A. $- 24 \pi$
- B. $- 12 \pi$ **Correct**
- C. $12 \pi$
- D. $- 6 \pi$
- E. $0$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ=\oint_C F\cdot\mathrm dr=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm dt.
$$

Along the curve $C,$ we have

$$
x=t^{2} - t,\quad y=2 \cos{\left(2 \pi t \right)},\quad z=3 \sin{\left(2 \pi t \right)}.
$$

So,

$$
\begin{aligned}F(r(t)) & =\left(0\right)\,i+\left(z\right)\,j+\left(- y\right)\,k \\ & =\left(0\right)\,i+\left(3 \sin{\left(2 \pi t \right)}\right)\,j+\left(- 2 \cos{\left(2 \pi t \right)}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm d}{\mathrm dt}\left(t^{2} - t\right)\,i+\frac{\mathrm d}{\mathrm dt}\left(2 \cos{\left(2 \pi t \right)}\right)\,j+\frac{\mathrm d}{\mathrm dt}\left(3 \sin{\left(2 \pi t \right)}\right)\,k \\ & =\left(2 t - 1\right)\,i+\left(- 4 \pi \sin{\left(2 \pi t \right)}\right)\,j+\left(6 \pi \cos{\left(2 \pi t \right)}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(0\right)\,i+\left(3 \sin{\left(2 \pi t \right)}\right)\,j+\left(- 2 \cos{\left(2 \pi t \right)}\right)\,k\right)\cdot\left(\left(2 t - 1\right)\,i+\left(- 4 \pi \sin{\left(2 \pi t \right)}\right)\,j+\left(6 \pi \cos{\left(2 \pi t \right)}\right)\,k\right) \\ & =\left(0\right)\cdot\left(2 t - 1\right)+\left(3 \sin{\left(2 \pi t \right)}\right)\cdot\left(- 4 \pi \sin{\left(2 \pi t \right)}\right)+\left(- 2 \cos{\left(2 \pi t \right)}\right)\cdot\left(6 \pi \cos{\left(2 \pi t \right)}\right) \\ & =\left(0\right)+\left(- 12 \pi \sin^{2}{\left(2 \pi t \right)}\right)+\left(- 12 \pi \cos^{2}{\left(2 \pi t \right)}\right) \\ & =- 12 \pi\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ=\oint_C F\cdot\mathrm dr & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm dt \\ & =\int_{0}^{1}\left(- 12 \pi\right)\,\mathrm dt \\ & =\left[- 12 \pi t\right]_{0}^{1} \\ & =[\left(- 12 \pi\right)]-[\left(0\right)] \\ & =- 12 \pi\end{aligned}
$$

---

### authored same-method extension — moderate
Template: `xy_symmetric`; profile: `authored-method`; eligible: True

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=\left(y\right)\,i+\left(x\right)\,j+\left(0\right)\,k$ along the closed curve $C$ given by $r(t)=\left(4 \sin{\left(t \right)}\right)\,i+\left(3 \cos{\left(t \right)}\right)\,j+\left(2 \sin{\left(t \right)}\right)\,k$ for $t\in [0,2 \pi).$

- A. $- 12 \pi$
- B. $0$ **Correct**
- C. $24 \pi$
- D. $- 24 \pi$
- E. $12 \pi$

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
Template: `xy_symmetric`; profile: `authored-method`; eligible: True

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=\left(y\right)\,i+\left(x\right)\,j+\left(0\right)\,k$ along the closed curve $C$ given by $r(t)=\left(2 \sin{\left(t \right)}\right)\,i+\left(3 \cos{\left(t \right)}\right)\,j+\left(2 \sin{\left(t \right)}\right)\,k$ for $t\in [0,2 \pi).$

- A. $- 6 \pi$
- B. $0$ **Correct**
- C. $12 \pi$
- D. $- 12 \pi$
- E. $6 \pi$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ=\oint_C F\cdot\mathrm dr=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm dt.
$$

Along the curve $C,$ we have

$$
x=2 \sin{\left(t \right)},\quad y=3 \cos{\left(t \right)},\quad z=2 \sin{\left(t \right)}.
$$

So,

$$
\begin{aligned}F(r(t)) & =\left(y\right)\,i+\left(x\right)\,j+\left(0\right)\,k \\ & =\left(3 \cos{\left(t \right)}\right)\,i+\left(2 \sin{\left(t \right)}\right)\,j+\left(0\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm d}{\mathrm dt}\left(2 \sin{\left(t \right)}\right)\,i+\frac{\mathrm d}{\mathrm dt}\left(3 \cos{\left(t \right)}\right)\,j+\frac{\mathrm d}{\mathrm dt}\left(2 \sin{\left(t \right)}\right)\,k \\ & =\left(2 \cos{\left(t \right)}\right)\,i+\left(- 3 \sin{\left(t \right)}\right)\,j+\left(2 \cos{\left(t \right)}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(3 \cos{\left(t \right)}\right)\,i+\left(2 \sin{\left(t \right)}\right)\,j+\left(0\right)\,k\right)\cdot\left(\left(2 \cos{\left(t \right)}\right)\,i+\left(- 3 \sin{\left(t \right)}\right)\,j+\left(2 \cos{\left(t \right)}\right)\,k\right) \\ & =\left(3 \cos{\left(t \right)}\right)\cdot\left(2 \cos{\left(t \right)}\right)+\left(2 \sin{\left(t \right)}\right)\cdot\left(- 3 \sin{\left(t \right)}\right)+\left(0\right)\cdot\left(2 \cos{\left(t \right)}\right) \\ & =\left(6 \cos^{2}{\left(t \right)}\right)+\left(- 6 \sin^{2}{\left(t \right)}\right)+\left(0\right) \\ & =6 \cos{\left(2 t \right)}\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ=\oint_C F\cdot\mathrm dr & =\int_{0}^{2 \pi}F(r(t))\cdot r^{\prime}(t)\,\mathrm dt \\ & =\int_{0}^{2 \pi}\left(6 \cos{\left(2 t \right)}\right)\,\mathrm dt \\ & =\left[3 \sin{\left(2 t \right)}\right]_{0}^{2 \pi} \\ & =[\left(0\right)]-[\left(0\right)] \\ & =0\end{aligned}
$$

---

### authored same-method extension — moderate
Template: `polynomial_sine`; profile: `authored-method`; eligible: True

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=\left(x + y\right)\,i+\left(0\right)\,j+\left(- z\right)\,k$ along the closed curve $C$ given by $r(t)=\left(4 - 4 t^{2}\right)\,i+\left(4 t^{2}\right)\,j+\left(3 \sin{\left(\pi t \right)}\right)\,k$ for $t\in [-1,1).$

- A. $-9$
- B. $0$ **Correct**
- C. $32$
- D. $-32$
- E. $9$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ=\oint_C F\cdot\mathrm dr=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm dt.
$$

Along the curve $C,$ we have

$$
x=4 - 4 t^{2},\quad y=4 t^{2},\quad z=3 \sin{\left(\pi t \right)}.
$$

So,

$$
\begin{aligned}F(r(t)) & =\left(x + y\right)\,i+\left(0\right)\,j+\left(- z\right)\,k \\ & =\left(4\right)\,i+\left(0\right)\,j+\left(- 3 \sin{\left(\pi t \right)}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm d}{\mathrm dt}\left(4 - 4 t^{2}\right)\,i+\frac{\mathrm d}{\mathrm dt}\left(4 t^{2}\right)\,j+\frac{\mathrm d}{\mathrm dt}\left(3 \sin{\left(\pi t \right)}\right)\,k \\ & =\left(- 8 t\right)\,i+\left(8 t\right)\,j+\left(3 \pi \cos{\left(\pi t \right)}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(4\right)\,i+\left(0\right)\,j+\left(- 3 \sin{\left(\pi t \right)}\right)\,k\right)\cdot\left(\left(- 8 t\right)\,i+\left(8 t\right)\,j+\left(3 \pi \cos{\left(\pi t \right)}\right)\,k\right) \\ & =\left(4\right)\cdot\left(- 8 t\right)+\left(0\right)\cdot\left(8 t\right)+\left(- 3 \sin{\left(\pi t \right)}\right)\cdot\left(3 \pi \cos{\left(\pi t \right)}\right) \\ & =\left(- 32 t\right)+\left(0\right)+\left(- 9 \pi \sin{\left(\pi t \right)} \cos{\left(\pi t \right)}\right) \\ & =- 32 t - \frac{9 \pi \sin{\left(2 \pi t \right)}}{2}\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ=\oint_C F\cdot\mathrm dr & =\int_{-1}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm dt \\ & =\int_{-1}^{1}\left(- 32 t - \frac{9 \pi \sin{\left(2 \pi t \right)}}{2}\right)\,\mathrm dt \\ & =\left[- 16 t^{2} + \frac{9 \cos{\left(2 \pi t \right)}}{4}\right]_{-1}^{1} \\ & =[\left(-16\right)+\left(\frac{9}{4}\right)]-[\left(-16\right)+\left(\frac{9}{4}\right)] \\ & =0\end{aligned}
$$

---

### authored same-method extension — moderate
Template: `polynomial_sine`; profile: `authored-method`; eligible: True

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=\left(x + y\right)\,i+\left(0\right)\,j+\left(- z\right)\,k$ along the closed curve $C$ given by $r(t)=\left(2 - 2 t^{2}\right)\,i+\left(2 t^{2}\right)\,j+\left(3 \sin{\left(\pi t \right)}\right)\,k$ for $t\in [-1,1).$

- A. $-9$
- B. $0$ **Correct**
- C. $8$
- D. $-8$
- E. $9$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ=\oint_C F\cdot\mathrm dr=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm dt.
$$

Along the curve $C,$ we have

$$
x=2 - 2 t^{2},\quad y=2 t^{2},\quad z=3 \sin{\left(\pi t \right)}.
$$

So,

$$
\begin{aligned}F(r(t)) & =\left(x + y\right)\,i+\left(0\right)\,j+\left(- z\right)\,k \\ & =\left(2\right)\,i+\left(0\right)\,j+\left(- 3 \sin{\left(\pi t \right)}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm d}{\mathrm dt}\left(2 - 2 t^{2}\right)\,i+\frac{\mathrm d}{\mathrm dt}\left(2 t^{2}\right)\,j+\frac{\mathrm d}{\mathrm dt}\left(3 \sin{\left(\pi t \right)}\right)\,k \\ & =\left(- 4 t\right)\,i+\left(4 t\right)\,j+\left(3 \pi \cos{\left(\pi t \right)}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(2\right)\,i+\left(0\right)\,j+\left(- 3 \sin{\left(\pi t \right)}\right)\,k\right)\cdot\left(\left(- 4 t\right)\,i+\left(4 t\right)\,j+\left(3 \pi \cos{\left(\pi t \right)}\right)\,k\right) \\ & =\left(2\right)\cdot\left(- 4 t\right)+\left(0\right)\cdot\left(4 t\right)+\left(- 3 \sin{\left(\pi t \right)}\right)\cdot\left(3 \pi \cos{\left(\pi t \right)}\right) \\ & =\left(- 8 t\right)+\left(0\right)+\left(- 9 \pi \sin{\left(\pi t \right)} \cos{\left(\pi t \right)}\right) \\ & =- 8 t - \frac{9 \pi \sin{\left(2 \pi t \right)}}{2}\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ=\oint_C F\cdot\mathrm dr & =\int_{-1}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm dt \\ & =\int_{-1}^{1}\left(- 8 t - \frac{9 \pi \sin{\left(2 \pi t \right)}}{2}\right)\,\mathrm dt \\ & =\left[- 4 t^{2} + \frac{9 \cos{\left(2 \pi t \right)}}{4}\right]_{-1}^{1} \\ & =[\left(-4\right)+\left(\frac{9}{4}\right)]-[\left(-4\right)+\left(\frac{9}{4}\right)] \\ & =0\end{aligned}
$$

---

### authored same-method extension — hard
Template: `polynomial_loop`; profile: `authored-method`; eligible: True

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=\left(- 5 x + 6 y\right)\,i+\left(0\right)\,j+\left(0\right)\,k$ along the closed curve $C$ given by $r(t)=\left(6 t^{2} - 6 t\right)\,i+\left(5 t^{3} - 5 t\right)\,j+\left(\sin{\left(2 \pi t \right)}\right)\,k$ for $t\in [0,1).$

- A. $-18$
- B. $-3$ **Correct**
- C. $3$
- D. $0$
- E. $-30$

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

Calculate the circulation $Γ$ of the vector field $F(x,y,z)=\left(- 4 x + 3 y\right)\,i+\left(0\right)\,j+\left(0\right)\,k$ along the closed curve $C$ given by $r(t)=\left(3 t^{2} - 3 t\right)\,i+\left(4 t^{3} - 4 t\right)\,j+\left(\sin{\left(2 \pi t \right)}\right)\,k$ for $t\in [0,1).$

- A. $- \frac{18}{5}$
- B. $- \frac{3}{5}$ **Correct**
- C. $\frac{3}{5}$
- D. $0$
- E. $-6$

**Worked solution**

The circulation $Γ$ measures the total work done by a force $F$ in moving a particle along a *closed* curve $C.$
It is given by the formula

$$
Γ=\oint_C F\cdot\mathrm dr=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm dt.
$$

Along the curve $C,$ we have

$$
x=3 t^{2} - 3 t,\quad y=4 t^{3} - 4 t,\quad z=\sin{\left(2 \pi t \right)}.
$$

So,

$$
\begin{aligned}F(r(t)) & =\left(- 4 x + 3 y\right)\,i+\left(0\right)\,j+\left(0\right)\,k \\ & =\left(12 t^{3} - 12 t^{2}\right)\,i+\left(0\right)\,j+\left(0\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm d}{\mathrm dt}\left(3 t^{2} - 3 t\right)\,i+\frac{\mathrm d}{\mathrm dt}\left(4 t^{3} - 4 t\right)\,j+\frac{\mathrm d}{\mathrm dt}\left(\sin{\left(2 \pi t \right)}\right)\,k \\ & =\left(6 t - 3\right)\,i+\left(12 t^{2} - 4\right)\,j+\left(2 \pi \cos{\left(2 \pi t \right)}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(12 t^{3} - 12 t^{2}\right)\,i+\left(0\right)\,j+\left(0\right)\,k\right)\cdot\left(\left(6 t - 3\right)\,i+\left(12 t^{2} - 4\right)\,j+\left(2 \pi \cos{\left(2 \pi t \right)}\right)\,k\right) \\ & =\left(12 t^{3} - 12 t^{2}\right)\cdot\left(6 t - 3\right)+\left(0\right)\cdot\left(12 t^{2} - 4\right)+\left(0\right)\cdot\left(2 \pi \cos{\left(2 \pi t \right)}\right) \\ & =\left(72 t^{4} - 108 t^{3} + 36 t^{2}\right)+\left(0\right)+\left(0\right) \\ & =\left(6 t - 3\right) \left(12 t^{3} - 12 t^{2}\right)\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}Γ=\oint_C F\cdot\mathrm dr & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm dt \\ & =\int_{0}^{1}\left(\left(6 t - 3\right) \left(12 t^{3} - 12 t^{2}\right)\right)\,\mathrm dt \\ & =\left[\frac{72 t^{5}}{5} - 27 t^{4} + 12 t^{3}\right]_{0}^{1} \\ & =[\left(12\right)+\left(-27\right)+\left(\frac{72}{5}\right)]-[\left(0\right)+\left(0\right)+\left(0\right)] \\ & =- \frac{3}{5}\end{aligned}
$$
