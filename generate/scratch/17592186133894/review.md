# Space-curve vector-field evaluation review

Basis 1356; raw historical evidence is explicitly ineligible. Generated defaults use direct substitution, differentiation, dot product and definite integration.

## ORIGINAL PUBLIC EVIDENCE — INELIGIBLE

### product — ORIGINAL EVIDENCE (INELIGIBLE)

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y,z)=yz\,i+xz\,j+xy\,k$ and $C$ is the path $r(t)=t\,i+{t}^{2}\,j+{t}^{3}\,k$ for $t\in [0,1].$

- $\frac{1}{4}$

- $1$ **correct**

- $0$

- $\frac{1}{3}$

- $\frac{1}{2}$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=t,\,y={t}^{2},\,z={t}^{3}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =yz\,i+xz\,j+xy\,k \\  & ={t}^{2}\cdot {t}^{3}\,i+t\cdot {t}^{3}\,j+t\cdot {t}^{2}\,k \\  & ={t}^{5}\,i+{t}^{4}\,j+{t}^{3}\,k.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({t}^{2})j+\frac{\text{d}}{\text{d}t}({t}^{3})j \\  & =i+2t\,j+3{t}^{2}\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =({t}^{5}\,i+{t}^{4}\,j+{t}^{3}\,k)\cdot (i+2t\,j+3{t}^{2}\,k) \\  & ={t}^{5}+2{t}^{5}+3{t}^{5} \\  & =6{t}^{5}.\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{1}6{t}^{5}\,dt \\  & ={{t}^{6}|}_{0}^{1} \\  & =1\end{aligned}
$$

## GENERATED HISTORICAL LINEAR-LIFT VARIANT — INELIGIBLE

### product — ORIGINAL EVIDENCE (INELIGIBLE)

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y,z)=\left(2\right)\cdot\left(yz\,i+xz\,j+xy\,k\right)$ and $C$ is the path $r(t)=t\,i+{t}^{2}\,j+{t}^{3}\,k$ for $t\in [0,1].$

- $\left(2\right)\cdot\left(\frac{1}{4}\right)$

- $\left(2\right)\cdot\left(1\right)$ **correct**

- $\left(2\right)\cdot\left(0\right)$

- $\left(2\right)\cdot\left(\frac{1}{3}\right)$

- $\left(2\right)\cdot\left(\frac{1}{2}\right)$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=t,\,y={t}^{2},\,z={t}^{3}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(2\right)\cdot\left(yz\,i+xz\,j+xy\,k\right) \\  & =\left(2\right)\cdot\left({t}^{2}\cdot {t}^{3}\,i+t\cdot {t}^{3}\,j+t\cdot {t}^{2}\,k\right) \\  & =\left(2\right)\cdot\left({t}^{5}\,i+{t}^{4}\,j+{t}^{3}\,k\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({t}^{2})j+\frac{\text{d}}{\text{d}t}({t}^{3})j \\  & =i+2t\,j+3{t}^{2}\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =\left(2\right)\cdot\left(({t}^{5}\,i+{t}^{4}\,j+{t}^{3}\,k)\cdot (i+2t\,j+3{t}^{2}\,k)\right) \\  & =\left(2\right)\cdot\left({t}^{5}+2{t}^{5}+3{t}^{5}\right) \\  & =\left(2\right)\cdot\left(6{t}^{5}\right).\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =\left(2\right)\cdot\left({\int }_{0}^{1}6{t}^{5}\,dt\right) \\  & =\left(2\right)\cdot\left({{t}^{6}|}_{0}^{1}\right) \\  & =\left(2\right)\cdot\left(1\right)\end{aligned}
$$

## GENERATED METHOD-BANK VARIANT

### product — GENERATED VARIANT

Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)=\left(y z\right)\,i+\left(x z\right)\,j+\left(x y\right)\,k$ and $C$ is the path $r(t)=\left(- 2 t\right)\,i+\left(3 t^{2}\right)\,j+\left(- t^{3}\right)\,k$ for $t\in [0,1]$.

- $3$

- $- \frac{8}{5}$

- $6$ **correct**

- $4$

- $5$

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=- 2 t,\qquad y=3 t^{2},\qquad z=- t^{3}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(y z\right)\,i+\left(x z\right)\,j+\left(x y\right)\,k \\ & =\left(\left(3 t^{2}\right) \left(- t^{3}\right)\right)\,i+\left(\left(- 2 t\right) \left(- t^{3}\right)\right)\,j+\left(\left(- 2 t\right) \left(3 t^{2}\right)\right)\,k \\ & =\left(- 3 t^{5}\right)\,i+\left(2 t^{4}\right)\,j+\left(- 6 t^{3}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ & =\frac{\mathrm{d}}{\mathrm{d}t}\left(- 2 t\right)\,i+\frac{\mathrm{d}}{\mathrm{d}t}\left(3 t^{2}\right)\,j+\frac{\mathrm{d}}{\mathrm{d}t}\left(- t^{3}\right)\,k \\ & =\left(-2\right)\,i+\left(6 t\right)\,j+\left(- 3 t^{2}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(- 3 t^{5}\right)\,i+\left(2 t^{4}\right)\,j+\left(- 6 t^{3}\right)\,k\right)\cdot\left(\left(-2\right)\,i+\left(6 t\right)\,j+\left(- 3 t^{2}\right)\,k\right) \\ & =\left(\left(- 3 t^{5}\right)\cdot\left(-2\right)\right)+\left(\left(2 t^{4}\right)\cdot\left(6 t\right)\right)+\left(\left(- 6 t^{3}\right)\cdot\left(- 3 t^{2}\right)\right) \\ & =\left(6 t^{5}\right)+\left(12 t^{5}\right)+\left(18 t^{5}\right) \\ & =36 t^{5}\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\ & =\int_{0}^{1}\left(36 t^{5}\right)\,\mathrm{d}t \\ & =\left[6 t^{6}\right]_{0}^{1} \\ & =\left(6 \left(1\right)^{6}\right)+\left(-\left(6 \left(0\right)^{6}\right)\right) \\ & =\left(6\right)+\left(0\right) \\ & =6\end{aligned}
$$

## GENERATED METHOD-BANK VARIANT

### product — GENERATED VARIANT

Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)=\left(y z\right)\,i+\left(x z\right)\,j+\left(x y\right)\,k$ and $C$ is the path $r(t)=\left(- 2 t\right)\,i+\left(- 3 t^{2}\right)\,j+\left(- t^{3}\right)\,k$ for $t\in [0,1]$.

- $-4$

- $-3$

- $\frac{12}{5}$

- $-6$ **correct**

- $-5$

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=- 2 t,\qquad y=- 3 t^{2},\qquad z=- t^{3}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(y z\right)\,i+\left(x z\right)\,j+\left(x y\right)\,k \\ & =\left(\left(- 3 t^{2}\right) \left(- t^{3}\right)\right)\,i+\left(\left(- 2 t\right) \left(- t^{3}\right)\right)\,j+\left(\left(- 2 t\right) \left(- 3 t^{2}\right)\right)\,k \\ & =\left(3 t^{5}\right)\,i+\left(2 t^{4}\right)\,j+\left(6 t^{3}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ & =\frac{\mathrm{d}}{\mathrm{d}t}\left(- 2 t\right)\,i+\frac{\mathrm{d}}{\mathrm{d}t}\left(- 3 t^{2}\right)\,j+\frac{\mathrm{d}}{\mathrm{d}t}\left(- t^{3}\right)\,k \\ & =\left(-2\right)\,i+\left(- 6 t\right)\,j+\left(- 3 t^{2}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(3 t^{5}\right)\,i+\left(2 t^{4}\right)\,j+\left(6 t^{3}\right)\,k\right)\cdot\left(\left(-2\right)\,i+\left(- 6 t\right)\,j+\left(- 3 t^{2}\right)\,k\right) \\ & =\left(\left(3 t^{5}\right)\cdot\left(-2\right)\right)+\left(\left(2 t^{4}\right)\cdot\left(- 6 t\right)\right)+\left(\left(6 t^{3}\right)\cdot\left(- 3 t^{2}\right)\right) \\ & =\left(- 6 t^{5}\right)+\left(- 12 t^{5}\right)+\left(- 18 t^{5}\right) \\ & =- 36 t^{5}\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\ & =\int_{0}^{1}\left(- 36 t^{5}\right)\,\mathrm{d}t \\ & =\left[- 6 t^{6}\right]_{0}^{1} \\ & =\left(- 6 \left(1\right)^{6}\right)+\left(-\left(- 6 \left(0\right)^{6}\right)\right) \\ & =\left(-6\right)+\left(0\right) \\ & =-6\end{aligned}
$$

## ORIGINAL PUBLIC EVIDENCE — INELIGIBLE

### helix_root — ORIGINAL EVIDENCE (INELIGIBLE)

Evaluate $\displaystyle \int_{C}F \cdot dr$ given that $F(x, y, z) = xi + yj + zk$ and $C$ is the path $r(t) = \cos ti + \sin tj + 2\sqrt{t}k$ for $t ∈ [0, π]$.

- $π$

- $π^{2}$

- $\frac{π}{2}$

- $4π$

- $2π$

[No original worked solution; no correct designation; unrated.]

## GENERATED HISTORICAL LINEAR-LIFT VARIANT — INELIGIBLE

### helix_root — ORIGINAL EVIDENCE (INELIGIBLE)

Evaluate $\displaystyle \int_{C}F \cdot dr$ given that $F(x, y, z) =\left(2\right)\cdot\left( xi + yj + zk\right)$ and $C$ is the path $r(t) = \cos ti + \sin tj + 2\sqrt{t}k$ for $t ∈ [0, π]$.

- $\left(2\right)\cdot\left(π\right)$

- $\left(2\right)\cdot\left(π^{2}\right)$

- $\left(2\right)\cdot\left(\frac{π}{2}\right)$

- $\left(2\right)\cdot\left(4π\right)$

- $\left(2\right)\cdot\left(2π\right)$

[No original worked solution; no correct designation; unrated.]

## GENERATED METHOD-BANK VARIANT

### helix_root — GENERATED VARIANT

Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)=\left(x\right)\,i+\left(y\right)\,j+\left(z\right)\,k$ and $C$ is the path $r(t)=\left(\cos{\left(t \right)}\right)\,i+\left(\sin{\left(t \right)}\right)\,j+\left(2 \sqrt{t}\right)\,k$ for $t\in [2,\pi]$.

- $- 4 \sqrt{2} + 4 \sqrt{\pi}$

- $-4 + \pi^{2}$

- $-4 + 2 \pi$ **correct**

- $-8 + 4 \pi$

- $0$

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=\cos{\left(t \right)},\qquad y=\sin{\left(t \right)},\qquad z=2 \sqrt{t}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(x\right)\,i+\left(y\right)\,j+\left(z\right)\,k \\ & =\left(\left(\cos{\left(t \right)}\right)\right)\,i+\left(\left(\sin{\left(t \right)}\right)\right)\,j+\left(\left(2 \sqrt{t}\right)\right)\,k \\ & =\left(\cos{\left(t \right)}\right)\,i+\left(\sin{\left(t \right)}\right)\,j+\left(2 \sqrt{t}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ & =\frac{\mathrm{d}}{\mathrm{d}t}\left(\cos{\left(t \right)}\right)\,i+\frac{\mathrm{d}}{\mathrm{d}t}\left(\sin{\left(t \right)}\right)\,j+\frac{\mathrm{d}}{\mathrm{d}t}\left(2 \sqrt{t}\right)\,k \\ & =\left(- \sin{\left(t \right)}\right)\,i+\left(\cos{\left(t \right)}\right)\,j+\left(\frac{1}{\sqrt{t}}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(\cos{\left(t \right)}\right)\,i+\left(\sin{\left(t \right)}\right)\,j+\left(2 \sqrt{t}\right)\,k\right)\cdot\left(\left(- \sin{\left(t \right)}\right)\,i+\left(\cos{\left(t \right)}\right)\,j+\left(\frac{1}{\sqrt{t}}\right)\,k\right) \\ & =\left(\left(\cos{\left(t \right)}\right)\cdot\left(- \sin{\left(t \right)}\right)\right)+\left(\left(\sin{\left(t \right)}\right)\cdot\left(\cos{\left(t \right)}\right)\right)+\left(\left(2 \sqrt{t}\right)\cdot\left(\frac{1}{\sqrt{t}}\right)\right) \\ & =\left(- \sin{\left(t \right)} \cos{\left(t \right)}\right)+\left(\sin{\left(t \right)} \cos{\left(t \right)}\right)+\left(2\right) \\ & =2\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_{2}^{\pi}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\ & =\int_{2}^{\pi}\left(2\right)\,\mathrm{d}t \\ & =\left[2 t\right]_{2}^{\pi} \\ & =\left(2 \left(\pi\right)\right)+\left(-\left(2 \left(2\right)\right)\right) \\ & =\left(2 \pi\right)+\left(-4\right) \\ & =-4 + 2 \pi\end{aligned}
$$

## GENERATED METHOD-BANK VARIANT

### helix_root — GENERATED VARIANT

Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)=\left(x\right)\,i+\left(y\right)\,j+\left(z\right)\,k$ and $C$ is the path $r(t)=\left(\cos{\left(t \right)}\right)\,i+\left(\sin{\left(t \right)}\right)\,j+\left(2 \sqrt{t}\right)\,k$ for $t\in [1,\pi]$.

- $-4 + 4 \pi$

- $-4 + 4 \sqrt{\pi}$

- $-1 + \pi^{2}$

- $-2 + 2 \pi$ **correct**

- $0$

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=\cos{\left(t \right)},\qquad y=\sin{\left(t \right)},\qquad z=2 \sqrt{t}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(x\right)\,i+\left(y\right)\,j+\left(z\right)\,k \\ & =\left(\left(\cos{\left(t \right)}\right)\right)\,i+\left(\left(\sin{\left(t \right)}\right)\right)\,j+\left(\left(2 \sqrt{t}\right)\right)\,k \\ & =\left(\cos{\left(t \right)}\right)\,i+\left(\sin{\left(t \right)}\right)\,j+\left(2 \sqrt{t}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ & =\frac{\mathrm{d}}{\mathrm{d}t}\left(\cos{\left(t \right)}\right)\,i+\frac{\mathrm{d}}{\mathrm{d}t}\left(\sin{\left(t \right)}\right)\,j+\frac{\mathrm{d}}{\mathrm{d}t}\left(2 \sqrt{t}\right)\,k \\ & =\left(- \sin{\left(t \right)}\right)\,i+\left(\cos{\left(t \right)}\right)\,j+\left(\frac{1}{\sqrt{t}}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(\cos{\left(t \right)}\right)\,i+\left(\sin{\left(t \right)}\right)\,j+\left(2 \sqrt{t}\right)\,k\right)\cdot\left(\left(- \sin{\left(t \right)}\right)\,i+\left(\cos{\left(t \right)}\right)\,j+\left(\frac{1}{\sqrt{t}}\right)\,k\right) \\ & =\left(\left(\cos{\left(t \right)}\right)\cdot\left(- \sin{\left(t \right)}\right)\right)+\left(\left(\sin{\left(t \right)}\right)\cdot\left(\cos{\left(t \right)}\right)\right)+\left(\left(2 \sqrt{t}\right)\cdot\left(\frac{1}{\sqrt{t}}\right)\right) \\ & =\left(- \sin{\left(t \right)} \cos{\left(t \right)}\right)+\left(\sin{\left(t \right)} \cos{\left(t \right)}\right)+\left(2\right) \\ & =2\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_{1}^{\pi}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\ & =\int_{1}^{\pi}\left(2\right)\,\mathrm{d}t \\ & =\left[2 t\right]_{1}^{\pi} \\ & =\left(2 \left(\pi\right)\right)+\left(-\left(2 \left(1\right)\right)\right) \\ & =\left(2 \pi\right)+\left(-2\right) \\ & =-2 + 2 \pi\end{aligned}
$$

## ORIGINAL PUBLIC EVIDENCE — INELIGIBLE

### mixed_polynomial — ORIGINAL EVIDENCE (INELIGIBLE)

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y,z)=(x+z)\,i+(z-y)\,j+{z}^{2}\,k$ and $C$ is the path $r(t)={t}^{2}\,i+3{t}^{2}\,j+2t\,k$ for $t\in [0,1].$

- $4$ **correct**

- $6$

- $16$

- $5$

- $8$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x={t}^{2},\,y=3{t}^{2},\,z=2t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(2t+{t}^{2})\,i+(2t-3{t}^{2})\,j+(2t)^{2}\,k \\  & =(2t+{t}^{2})\,i+(2t-3{t}^{2})\,j+4{t}^{2}\,k.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}({t}^{2})i+\frac{\text{d}}{\text{d}t}(3{t}^{2})j+\frac{\text{d}}{\text{d}t}(2t)j \\  & =2ti+6t\,j+2\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =((2t+{t}^{2})\,i+(2t-3{t}^{2})\,j+4{t}^{2}\,k)\cdot (2ti+6t\,j+2\,k) \\  & =4{t}^{2}+2{t}^{3}+12{t}^{2}-18{t}^{3}+8{t}^{2} \\  & =24{t}^{2}-16{t}^{3}.\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{1}(24{t}^{2}-16{t}^{3})\,dt \\  & ={8{t}^{3}-4{t}^{4}|}_{0}^{1} \\  & =8-4 \\  & =4\end{aligned}
$$

## GENERATED HISTORICAL LINEAR-LIFT VARIANT — INELIGIBLE

### mixed_polynomial — ORIGINAL EVIDENCE (INELIGIBLE)

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y,z)=\left(2\right)\cdot\left((x+z)\,i+(z-y)\,j+{z}^{2}\,k\right)$ and $C$ is the path $r(t)={t}^{2}\,i+3{t}^{2}\,j+2t\,k$ for $t\in [0,1].$

- $\left(2\right)\cdot\left(4\right)$ **correct**

- $\left(2\right)\cdot\left(6\right)$

- $\left(2\right)\cdot\left(16\right)$

- $\left(2\right)\cdot\left(5\right)$

- $\left(2\right)\cdot\left(8\right)$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x={t}^{2},\,y=3{t}^{2},\,z=2t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(2\right)\cdot\left((2t+{t}^{2})\,i+(2t-3{t}^{2})\,j+(2t)^{2}\,k\right) \\  & =\left(2\right)\cdot\left((2t+{t}^{2})\,i+(2t-3{t}^{2})\,j+4{t}^{2}\,k\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}({t}^{2})i+\frac{\text{d}}{\text{d}t}(3{t}^{2})j+\frac{\text{d}}{\text{d}t}(2t)j \\  & =2ti+6t\,j+2\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =\left(2\right)\cdot\left(((2t+{t}^{2})\,i+(2t-3{t}^{2})\,j+4{t}^{2}\,k)\cdot (2ti+6t\,j+2\,k)\right) \\  & =\left(2\right)\cdot\left(4{t}^{2}+2{t}^{3}+12{t}^{2}-18{t}^{3}+8{t}^{2}\right) \\  & =\left(2\right)\cdot\left(24{t}^{2}-16{t}^{3}\right).\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =\left(2\right)\cdot\left({\int }_{0}^{1}(24{t}^{2}-16{t}^{3})\,dt\right) \\  & =\left(2\right)\cdot\left({8{t}^{3}-4{t}^{4}|}_{0}^{1}\right) \\  & =\left(2\right)\cdot\left(8-4\right) \\  & =\left(2\right)\cdot\left(4\right)\end{aligned}
$$

## GENERATED METHOD-BANK VARIANT

### mixed_polynomial — GENERATED VARIANT

Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)=\left(x + z\right)\,i+\left(- y + z\right)\,j+\left(z^{2}\right)\,k$ and $C$ is the path $r(t)=\left(- 2 t^{2}\right)\,i+\left(3 t^{2}\right)\,j+\left(- t\right)\,k$ for $t\in [0,1]$.

- $- \frac{19}{6}$

- $- \frac{7}{3}$

- $- \frac{7}{2}$ **correct**

- $3$

- $- \frac{41}{6}$

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=- 2 t^{2},\qquad y=3 t^{2},\qquad z=- t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(x + z\right)\,i+\left(- y + z\right)\,j+\left(z^{2}\right)\,k \\ & =\left(\left(- 2 t^{2}\right) + \left(- t\right)\right)\,i+\left(- \left(3 t^{2}\right) + \left(- t\right)\right)\,j+\left(\left(- t\right)^{2}\right)\,k \\ & =\left(t \left(- 2 t - 1\right)\right)\,i+\left(t \left(- 3 t - 1\right)\right)\,j+\left(t^{2}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ & =\frac{\mathrm{d}}{\mathrm{d}t}\left(- 2 t^{2}\right)\,i+\frac{\mathrm{d}}{\mathrm{d}t}\left(3 t^{2}\right)\,j+\frac{\mathrm{d}}{\mathrm{d}t}\left(- t\right)\,k \\ & =\left(- 4 t\right)\,i+\left(6 t\right)\,j+\left(-1\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(t \left(- 2 t - 1\right)\right)\,i+\left(t \left(- 3 t - 1\right)\right)\,j+\left(t^{2}\right)\,k\right)\cdot\left(\left(- 4 t\right)\,i+\left(6 t\right)\,j+\left(-1\right)\,k\right) \\ & =\left(\left(t \left(- 2 t - 1\right)\right)\cdot\left(- 4 t\right)\right)+\left(\left(t \left(- 3 t - 1\right)\right)\cdot\left(6 t\right)\right)+\left(\left(t^{2}\right)\cdot\left(-1\right)\right) \\ & =\left(4 t^{2}\right)+\left(8 t^{3}\right)+\left(- 18 t^{3}\right)+\left(- 6 t^{2}\right)+\left(- t^{2}\right) \\ & =t^{2} \left(- 10 t - 3\right)\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\ & =\int_{0}^{1}\left(t^{2} \left(- 10 t - 3\right)\right)\,\mathrm{d}t \\ & =\left[- \frac{5 t^{4}}{2} - t^{3}\right]_{0}^{1} \\ & =\left(- \left(1\right)^{3}\right)+\left(-\left(- \left(0\right)^{3}\right)\right)+\left(- \frac{5 \left(1\right)^{4}}{2}\right)+\left(-\left(- \frac{5 \left(0\right)^{4}}{2}\right)\right) \\ & =\left(-1\right)+\left(0\right)+\left(- \frac{5}{2}\right)+\left(0\right) \\ & =- \frac{7}{2}\end{aligned}
$$

## GENERATED METHOD-BANK VARIANT

### mixed_polynomial — GENERATED VARIANT

Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)=\left(x + z\right)\,i+\left(- y + z\right)\,j+\left(z^{2}\right)\,k$ and $C$ is the path $r(t)=\left(- 2 t^{2}\right)\,i+\left(- 3 t^{2}\right)\,j+\left(- t\right)\,k$ for $t\in [0,1]$.

- $3$

- $\frac{5}{6}$

- $- \frac{1}{3}$

- $\frac{1}{2}$ **correct**

- $- \frac{17}{6}$

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=- 2 t^{2},\qquad y=- 3 t^{2},\qquad z=- t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(x + z\right)\,i+\left(- y + z\right)\,j+\left(z^{2}\right)\,k \\ & =\left(\left(- 2 t^{2}\right) + \left(- t\right)\right)\,i+\left(- \left(- 3 t^{2}\right) + \left(- t\right)\right)\,j+\left(\left(- t\right)^{2}\right)\,k \\ & =\left(t \left(- 2 t - 1\right)\right)\,i+\left(t \left(3 t - 1\right)\right)\,j+\left(t^{2}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ & =\frac{\mathrm{d}}{\mathrm{d}t}\left(- 2 t^{2}\right)\,i+\frac{\mathrm{d}}{\mathrm{d}t}\left(- 3 t^{2}\right)\,j+\frac{\mathrm{d}}{\mathrm{d}t}\left(- t\right)\,k \\ & =\left(- 4 t\right)\,i+\left(- 6 t\right)\,j+\left(-1\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(t \left(- 2 t - 1\right)\right)\,i+\left(t \left(3 t - 1\right)\right)\,j+\left(t^{2}\right)\,k\right)\cdot\left(\left(- 4 t\right)\,i+\left(- 6 t\right)\,j+\left(-1\right)\,k\right) \\ & =\left(\left(t \left(- 2 t - 1\right)\right)\cdot\left(- 4 t\right)\right)+\left(\left(t \left(3 t - 1\right)\right)\cdot\left(- 6 t\right)\right)+\left(\left(t^{2}\right)\cdot\left(-1\right)\right) \\ & =\left(4 t^{2}\right)+\left(8 t^{3}\right)+\left(- 18 t^{3}\right)+\left(6 t^{2}\right)+\left(- t^{2}\right) \\ & =t^{2} \left(9 - 10 t\right)\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\ & =\int_{0}^{1}\left(t^{2} \left(9 - 10 t\right)\right)\,\mathrm{d}t \\ & =\left[- \frac{5 t^{4}}{2} + 3 t^{3}\right]_{0}^{1} \\ & =\left(3 \left(1\right)^{3}\right)+\left(-\left(3 \left(0\right)^{3}\right)\right)+\left(- \frac{5 \left(1\right)^{4}}{2}\right)+\left(-\left(- \frac{5 \left(0\right)^{4}}{2}\right)\right) \\ & =\left(3\right)+\left(0\right)+\left(- \frac{5}{2}\right)+\left(0\right) \\ & =\frac{1}{2}\end{aligned}
$$

## ORIGINAL PUBLIC EVIDENCE — INELIGIBLE

### trig_cancel — ORIGINAL EVIDENCE (INELIGIBLE)

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y,z)=x\,i+z\,j+y\,k$ and $C$ is the path $r(t)=-\operatorname{sin}⁡t\,i+\operatorname{sec}⁡t\,j+\operatorname{cos}⁡t\,k$ for $t\in [0,\frac{\pi }{6}].$

- $\frac{1}{9}$

- $\frac{1}{8}$ **correct**

- $\frac{1}{3}$

- $\frac{1}{2}$

- $\frac{1}{4}$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=-\operatorname{sin}⁡t,\,y=\operatorname{sec}⁡t,\,z=\operatorname{cos}⁡t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =x\,i+z\,j+y\,k \\  & =-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j+\operatorname{sec}⁡t\,k.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(-\operatorname{sin}⁡t)i+\frac{\text{d}}{\text{d}t}(\operatorname{sec}⁡t)j+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)j \\  & =-\operatorname{cos}⁡t\,i+\operatorname{tan}⁡x\operatorname{sec}⁡x\,j-\operatorname{sin}⁡t\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j+\operatorname{sec}⁡t\,k)\cdot (-\operatorname{cos}⁡t\,i+\operatorname{tan}⁡x\operatorname{sec}⁡x\,j-\operatorname{sin}⁡t\,k) \\  & =\operatorname{sin}⁡t\operatorname{cos}⁡t+\operatorname{tan}⁡t-\operatorname{tan}⁡t \\  & =\operatorname{sin}⁡t\operatorname{cos}⁡t.\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{\pi /6}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{\pi /6}\operatorname{sin}⁡t\operatorname{cos}⁡t\,dt \\  & ={\int }_{0}^{\pi /6}\frac{\operatorname{sin}⁡(2t)}{2}\,dt \\  & ={-\frac{\operatorname{cos}⁡(2t)}{4}|}_{0}^{\pi /6} \\  & =-\frac{\operatorname{cos}⁡(\frac{\pi }{3})}{4}+\frac{\operatorname{cos}⁡(0)}{4} \\  & =-\frac{1}{8}+\frac{1}{4} \\  & =\frac{1}{8}\end{aligned}
$$

## GENERATED HISTORICAL LINEAR-LIFT VARIANT — INELIGIBLE

### trig_cancel — ORIGINAL EVIDENCE (INELIGIBLE)

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y,z)=\left(2\right)\cdot\left(x\,i+z\,j+y\,k\right)$ and $C$ is the path $r(t)=-\operatorname{sin}⁡t\,i+\operatorname{sec}⁡t\,j+\operatorname{cos}⁡t\,k$ for $t\in [0,\frac{\pi }{6}].$

- $\left(2\right)\cdot\left(\frac{1}{9}\right)$

- $\left(2\right)\cdot\left(\frac{1}{8}\right)$ **correct**

- $\left(2\right)\cdot\left(\frac{1}{3}\right)$

- $\left(2\right)\cdot\left(\frac{1}{2}\right)$

- $\left(2\right)\cdot\left(\frac{1}{4}\right)$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=-\operatorname{sin}⁡t,\,y=\operatorname{sec}⁡t,\,z=\operatorname{cos}⁡t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(2\right)\cdot\left(x\,i+z\,j+y\,k\right) \\  & =\left(2\right)\cdot\left(-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j+\operatorname{sec}⁡t\,k\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(-\operatorname{sin}⁡t)i+\frac{\text{d}}{\text{d}t}(\operatorname{sec}⁡t)j+\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)j \\  & =-\operatorname{cos}⁡t\,i+\operatorname{tan}⁡x\operatorname{sec}⁡x\,j-\operatorname{sin}⁡t\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =\left(2\right)\cdot\left((-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j+\operatorname{sec}⁡t\,k)\cdot (-\operatorname{cos}⁡t\,i+\operatorname{tan}⁡x\operatorname{sec}⁡x\,j-\operatorname{sin}⁡t\,k)\right) \\  & =\left(2\right)\cdot\left(\operatorname{sin}⁡t\operatorname{cos}⁡t+\operatorname{tan}⁡t-\operatorname{tan}⁡t\right) \\  & =\left(2\right)\cdot\left(\operatorname{sin}⁡t\operatorname{cos}⁡t\right).\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{\pi /6}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =\left(2\right)\cdot\left({\int }_{0}^{\pi /6}\operatorname{sin}⁡t\operatorname{cos}⁡t\,dt\right) \\  & =\left(2\right)\cdot\left({\int }_{0}^{\pi /6}\frac{\operatorname{sin}⁡(2t)}{2}\,dt\right) \\  & =\left(2\right)\cdot\left({-\frac{\operatorname{cos}⁡(2t)}{4}|}_{0}^{\pi /6}\right) \\  & =\left(2\right)\cdot\left(-\frac{\operatorname{cos}⁡(\frac{\pi }{3})}{4}+\frac{\operatorname{cos}⁡(0)}{4}\right) \\  & =\left(2\right)\cdot\left(-\frac{1}{8}+\frac{1}{4}\right) \\  & =\left(2\right)\cdot\left(\frac{1}{8}\right)\end{aligned}
$$

## GENERATED METHOD-BANK VARIANT

### trig_cancel — GENERATED VARIANT

Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)=\left(x\right)\,i+\left(z\right)\,j+\left(y\right)\,k$ and $C$ is the path $r(t)=\left(2 \sin{\left(t \right)}\right)\,i+\left(3 \sec{\left(t \right)}\right)\,j+\left(- \cos{\left(t \right)}\right)\,k$ for $t\in [0,\frac{\pi}{3}]$.

- $\sqrt{3}$

- $\frac{1}{2}$

- $\frac{3}{2}$ **correct**

- $3$

- $- \frac{3}{2}$

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=2 \sin{\left(t \right)},\qquad y=3 \sec{\left(t \right)},\qquad z=- \cos{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(x\right)\,i+\left(z\right)\,j+\left(y\right)\,k \\ & =\left(\left(2 \sin{\left(t \right)}\right)\right)\,i+\left(\left(- \cos{\left(t \right)}\right)\right)\,j+\left(\left(3 \sec{\left(t \right)}\right)\right)\,k \\ & =\left(2 \sin{\left(t \right)}\right)\,i+\left(- \cos{\left(t \right)}\right)\,j+\left(3 \sec{\left(t \right)}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ & =\frac{\mathrm{d}}{\mathrm{d}t}\left(2 \sin{\left(t \right)}\right)\,i+\frac{\mathrm{d}}{\mathrm{d}t}\left(3 \sec{\left(t \right)}\right)\,j+\frac{\mathrm{d}}{\mathrm{d}t}\left(- \cos{\left(t \right)}\right)\,k \\ & =\left(2 \cos{\left(t \right)}\right)\,i+\left(3 \tan{\left(t \right)} \sec{\left(t \right)}\right)\,j+\left(\sin{\left(t \right)}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(2 \sin{\left(t \right)}\right)\,i+\left(- \cos{\left(t \right)}\right)\,j+\left(3 \sec{\left(t \right)}\right)\,k\right)\cdot\left(\left(2 \cos{\left(t \right)}\right)\,i+\left(3 \tan{\left(t \right)} \sec{\left(t \right)}\right)\,j+\left(\sin{\left(t \right)}\right)\,k\right) \\ & =\left(\left(2 \sin{\left(t \right)}\right)\cdot\left(2 \cos{\left(t \right)}\right)\right)+\left(\left(- \cos{\left(t \right)}\right)\cdot\left(3 \tan{\left(t \right)} \sec{\left(t \right)}\right)\right)+\left(\left(3 \sec{\left(t \right)}\right)\cdot\left(\sin{\left(t \right)}\right)\right) \\ & =\left(4 \sin{\left(t \right)} \cos{\left(t \right)}\right)+\left(- 3 \cos{\left(t \right)} \tan{\left(t \right)} \sec{\left(t \right)}\right)+\left(3 \sin{\left(t \right)} \sec{\left(t \right)}\right) \\ & =2 \sin{\left(2 t \right)}\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_{0}^{\frac{\pi}{3}}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\ & =\int_{0}^{\frac{\pi}{3}}\left(2 \sin{\left(2 t \right)}\right)\,\mathrm{d}t \\ & =\left[- \cos{\left(2 t \right)}\right]_{0}^{\frac{\pi}{3}} \\ & =\left(- \cos{\left(2 \left(\frac{\pi}{3}\right) \right)}\right)+\left(-\left(- \cos{\left(2 \left(0\right) \right)}\right)\right) \\ & =\left(\frac{1}{2}\right)+\left(1\right) \\ & =\frac{3}{2}\end{aligned}
$$

## GENERATED METHOD-BANK VARIANT

### trig_cancel — GENERATED VARIANT

Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)=\left(x\right)\,i+\left(z\right)\,j+\left(y\right)\,k$ and $C$ is the path $r(t)=\left(2 \sin{\left(t \right)}\right)\,i+\left(- 3 \sec{\left(t \right)}\right)\,j+\left(- \cos{\left(t \right)}\right)\,k$ for $t\in [0,\frac{\pi}{3}]$.

- $3$

- $\sqrt{3}$

- $\frac{1}{2}$

- $\frac{3}{2}$ **correct**

- $- \frac{3}{2}$

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=2 \sin{\left(t \right)},\qquad y=- 3 \sec{\left(t \right)},\qquad z=- \cos{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(x\right)\,i+\left(z\right)\,j+\left(y\right)\,k \\ & =\left(\left(2 \sin{\left(t \right)}\right)\right)\,i+\left(\left(- \cos{\left(t \right)}\right)\right)\,j+\left(\left(- 3 \sec{\left(t \right)}\right)\right)\,k \\ & =\left(2 \sin{\left(t \right)}\right)\,i+\left(- \cos{\left(t \right)}\right)\,j+\left(- 3 \sec{\left(t \right)}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ & =\frac{\mathrm{d}}{\mathrm{d}t}\left(2 \sin{\left(t \right)}\right)\,i+\frac{\mathrm{d}}{\mathrm{d}t}\left(- 3 \sec{\left(t \right)}\right)\,j+\frac{\mathrm{d}}{\mathrm{d}t}\left(- \cos{\left(t \right)}\right)\,k \\ & =\left(2 \cos{\left(t \right)}\right)\,i+\left(- 3 \tan{\left(t \right)} \sec{\left(t \right)}\right)\,j+\left(\sin{\left(t \right)}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(2 \sin{\left(t \right)}\right)\,i+\left(- \cos{\left(t \right)}\right)\,j+\left(- 3 \sec{\left(t \right)}\right)\,k\right)\cdot\left(\left(2 \cos{\left(t \right)}\right)\,i+\left(- 3 \tan{\left(t \right)} \sec{\left(t \right)}\right)\,j+\left(\sin{\left(t \right)}\right)\,k\right) \\ & =\left(\left(2 \sin{\left(t \right)}\right)\cdot\left(2 \cos{\left(t \right)}\right)\right)+\left(\left(- \cos{\left(t \right)}\right)\cdot\left(- 3 \tan{\left(t \right)} \sec{\left(t \right)}\right)\right)+\left(\left(- 3 \sec{\left(t \right)}\right)\cdot\left(\sin{\left(t \right)}\right)\right) \\ & =\left(4 \sin{\left(t \right)} \cos{\left(t \right)}\right)+\left(3 \cos{\left(t \right)} \tan{\left(t \right)} \sec{\left(t \right)}\right)+\left(- 3 \sin{\left(t \right)} \sec{\left(t \right)}\right) \\ & =2 \sin{\left(2 t \right)}\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_{0}^{\frac{\pi}{3}}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\ & =\int_{0}^{\frac{\pi}{3}}\left(2 \sin{\left(2 t \right)}\right)\,\mathrm{d}t \\ & =\left[- \cos{\left(2 t \right)}\right]_{0}^{\frac{\pi}{3}} \\ & =\left(- \cos{\left(2 \left(\frac{\pi}{3}\right) \right)}\right)+\left(-\left(- \cos{\left(2 \left(0\right) \right)}\right)\right) \\ & =\left(\frac{1}{2}\right)+\left(1\right) \\ & =\frac{3}{2}\end{aligned}
$$

## ORIGINAL PUBLIC EVIDENCE — INELIGIBLE

### exp_cancel_xy — ORIGINAL EVIDENCE (INELIGIBLE)

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y,z)=y\,i+x\,j+z\,k$ and $C$ is the path $r(t)={e}^{-t}\,i+{e}^{t}\,j+{e}^{2t}\,k$ for $t\in [0,1].$

- $\frac{{e}^{2}-1}{4}$

- $\frac{{e}^{4}-1}{2}$ **correct**

- $\frac{e-1}{4}$

- $\frac{{e}^{2}-1}{2}$

- $\frac{{e}^{4}-1}{4}$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x={e}^{-t},\,y={e}^{t},\,z={e}^{2t}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =y\,i+x\,j+z\,k \\  & ={e}^{t}\,i+{e}^{-t}\,j+{e}^{2t}\,k.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}({e}^{-t})i+\frac{\text{d}}{\text{d}t}({e}^{t})j+\frac{\text{d}}{\text{d}t}({e}^{2t})j \\  & =-{e}^{-t}i+{e}^{t}\,j+2{e}^{2t}\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =({e}^{t}\,i+{e}^{-t}\,j+{e}^{2t}\,k)\cdot (-{e}^{-t}i+{e}^{t}\,j+2{e}^{2t}\,k) \\  & =-1+1+2{e}^{4t} \\  & =2{e}^{4t}.\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{1}2{e}^{4t}\,dt \\  & ={\frac{{e}^{4t}}{2}|}_{0}^{1} \\  & =\frac{{e}^{4}-1}{2}\end{aligned}
$$

## GENERATED HISTORICAL LINEAR-LIFT VARIANT — INELIGIBLE

### exp_cancel_xy — ORIGINAL EVIDENCE (INELIGIBLE)

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y,z)=\left(2\right)\cdot\left(y\,i+x\,j+z\,k\right)$ and $C$ is the path $r(t)={e}^{-t}\,i+{e}^{t}\,j+{e}^{2t}\,k$ for $t\in [0,1].$

- $\left(2\right)\cdot\left(\frac{{e}^{2}-1}{4}\right)$

- $\left(2\right)\cdot\left(\frac{{e}^{4}-1}{2}\right)$ **correct**

- $\left(2\right)\cdot\left(\frac{e-1}{4}\right)$

- $\left(2\right)\cdot\left(\frac{{e}^{2}-1}{2}\right)$

- $\left(2\right)\cdot\left(\frac{{e}^{4}-1}{4}\right)$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x={e}^{-t},\,y={e}^{t},\,z={e}^{2t}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(2\right)\cdot\left(y\,i+x\,j+z\,k\right) \\  & =\left(2\right)\cdot\left({e}^{t}\,i+{e}^{-t}\,j+{e}^{2t}\,k\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}({e}^{-t})i+\frac{\text{d}}{\text{d}t}({e}^{t})j+\frac{\text{d}}{\text{d}t}({e}^{2t})j \\  & =-{e}^{-t}i+{e}^{t}\,j+2{e}^{2t}\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =\left(2\right)\cdot\left(({e}^{t}\,i+{e}^{-t}\,j+{e}^{2t}\,k)\cdot (-{e}^{-t}i+{e}^{t}\,j+2{e}^{2t}\,k)\right) \\  & =\left(2\right)\cdot\left(-1+1+2{e}^{4t}\right) \\  & =\left(2\right)\cdot\left(2{e}^{4t}\right).\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =\left(2\right)\cdot\left({\int }_{0}^{1}2{e}^{4t}\,dt\right) \\  & =\left(2\right)\cdot\left({\frac{{e}^{4t}}{2}|}_{0}^{1}\right) \\  & =\left(2\right)\cdot\left(\frac{{e}^{4}-1}{2}\right)\end{aligned}
$$

## GENERATED METHOD-BANK VARIANT

### exp_cancel_xy — GENERATED VARIANT

Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)=\left(y\right)\,i+\left(x\right)\,j+\left(z\right)\,k$ and $C$ is the path $r(t)=\left(- 2 e^{- 3 t}\right)\,i+\left(3 e^{3 t}\right)\,j+\left(- e^{2 t}\right)\,k$ for $t\in [0,1]$.

- $0$

- $- \frac{e^{2}}{2} - \frac{7}{6} + \frac{2}{3 e^{3}} + e^{3}$

- $- \frac{1}{2} + \frac{e^{4}}{2}$ **correct**

- $\frac{35}{2} + \frac{e^{4}}{2}$

- $- \frac{37}{2} + \frac{e^{4}}{2}$

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=- 2 e^{- 3 t},\qquad y=3 e^{3 t},\qquad z=- e^{2 t}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(y\right)\,i+\left(x\right)\,j+\left(z\right)\,k \\ & =\left(\left(3 e^{3 t}\right)\right)\,i+\left(\left(- 2 e^{- 3 t}\right)\right)\,j+\left(\left(- e^{2 t}\right)\right)\,k \\ & =\left(3 e^{3 t}\right)\,i+\left(- 2 e^{- 3 t}\right)\,j+\left(- e^{2 t}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ & =\frac{\mathrm{d}}{\mathrm{d}t}\left(- 2 e^{- 3 t}\right)\,i+\frac{\mathrm{d}}{\mathrm{d}t}\left(3 e^{3 t}\right)\,j+\frac{\mathrm{d}}{\mathrm{d}t}\left(- e^{2 t}\right)\,k \\ & =\left(6 e^{- 3 t}\right)\,i+\left(9 e^{3 t}\right)\,j+\left(- 2 e^{2 t}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(3 e^{3 t}\right)\,i+\left(- 2 e^{- 3 t}\right)\,j+\left(- e^{2 t}\right)\,k\right)\cdot\left(\left(6 e^{- 3 t}\right)\,i+\left(9 e^{3 t}\right)\,j+\left(- 2 e^{2 t}\right)\,k\right) \\ & =\left(\left(3 e^{3 t}\right)\cdot\left(6 e^{- 3 t}\right)\right)+\left(\left(- 2 e^{- 3 t}\right)\cdot\left(9 e^{3 t}\right)\right)+\left(\left(- e^{2 t}\right)\cdot\left(- 2 e^{2 t}\right)\right) \\ & =\left(18\right)+\left(-18\right)+\left(2 e^{4 t}\right) \\ & =2 e^{4 t}\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\ & =\int_{0}^{1}\left(2 e^{4 t}\right)\,\mathrm{d}t \\ & =\left[\frac{e^{4 t}}{2}\right]_{0}^{1} \\ & =\left(\frac{e^{4 \left(1\right)}}{2}\right)+\left(-\left(\frac{e^{4 \left(0\right)}}{2}\right)\right) \\ & =\left(\frac{e^{4}}{2}\right)+\left(- \frac{1}{2}\right) \\ & =- \frac{1}{2} + \frac{e^{4}}{2}\end{aligned}
$$

## GENERATED METHOD-BANK VARIANT

### exp_cancel_xy — GENERATED VARIANT

Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)=\left(y\right)\,i+\left(x\right)\,j+\left(z\right)\,k$ and $C$ is the path $r(t)=\left(- 2 e^{- 3 t}\right)\,i+\left(- 3 e^{3 t}\right)\,j+\left(- e^{t}\right)\,k$ for $t\in [0,1]$.

- $- \frac{37}{2} + \frac{e^{2}}{2}$

- $0$

- $- e^{3} - e + \frac{2}{3 e^{3}} + \frac{4}{3}$

- $- \frac{1}{2} + \frac{e^{2}}{2}$ **correct**

- $\frac{e^{2}}{2} + \frac{35}{2}$

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=- 2 e^{- 3 t},\qquad y=- 3 e^{3 t},\qquad z=- e^{t}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(y\right)\,i+\left(x\right)\,j+\left(z\right)\,k \\ & =\left(\left(- 3 e^{3 t}\right)\right)\,i+\left(\left(- 2 e^{- 3 t}\right)\right)\,j+\left(\left(- e^{t}\right)\right)\,k \\ & =\left(- 3 e^{3 t}\right)\,i+\left(- 2 e^{- 3 t}\right)\,j+\left(- e^{t}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ & =\frac{\mathrm{d}}{\mathrm{d}t}\left(- 2 e^{- 3 t}\right)\,i+\frac{\mathrm{d}}{\mathrm{d}t}\left(- 3 e^{3 t}\right)\,j+\frac{\mathrm{d}}{\mathrm{d}t}\left(- e^{t}\right)\,k \\ & =\left(6 e^{- 3 t}\right)\,i+\left(- 9 e^{3 t}\right)\,j+\left(- e^{t}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(- 3 e^{3 t}\right)\,i+\left(- 2 e^{- 3 t}\right)\,j+\left(- e^{t}\right)\,k\right)\cdot\left(\left(6 e^{- 3 t}\right)\,i+\left(- 9 e^{3 t}\right)\,j+\left(- e^{t}\right)\,k\right) \\ & =\left(\left(- 3 e^{3 t}\right)\cdot\left(6 e^{- 3 t}\right)\right)+\left(\left(- 2 e^{- 3 t}\right)\cdot\left(- 9 e^{3 t}\right)\right)+\left(\left(- e^{t}\right)\cdot\left(- e^{t}\right)\right) \\ & =\left(-18\right)+\left(18\right)+\left(e^{2 t}\right) \\ & =e^{2 t}\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\ & =\int_{0}^{1}\left(e^{2 t}\right)\,\mathrm{d}t \\ & =\left[\frac{e^{2 t}}{2}\right]_{0}^{1} \\ & =\left(\frac{e^{2 \left(1\right)}}{2}\right)+\left(-\left(\frac{e^{2 \left(0\right)}}{2}\right)\right) \\ & =\left(\frac{e^{2}}{2}\right)+\left(- \frac{1}{2}\right) \\ & =- \frac{1}{2} + \frac{e^{2}}{2}\end{aligned}
$$

## ORIGINAL PUBLIC EVIDENCE — INELIGIBLE

### exp_cancel_yz — ORIGINAL EVIDENCE (INELIGIBLE)

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y,z)=x\,i+z\,j+y\,k$ and $C$ is the path $r(t)=2{e}^{t}\,i+3{e}^{2t}\,j+{e}^{-2t}\,k$ for $t\in [0,1].$

- $2{e}^{2}-1$

- $4{e}^{4}-4$

- $4{e}^{2}-1$

- $2{e}^{2}-2$ **correct**

- $4{e}^{2}-2$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=2{e}^{t},\,y=3{e}^{2t},\,z={e}^{-2t}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =x\,i+z\,j+y\,k \\  & =2{e}^{t}\,i+{e}^{-2t}\,j+3{e}^{2t}\,k.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(2{e}^{t})i+\frac{\text{d}}{\text{d}t}(3{e}^{2t})j+\frac{\text{d}}{\text{d}t}({e}^{-2t})j \\  & =2{e}^{t}i+6{e}^{2t}\,j-2{e}^{-2t}\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(2{e}^{t}\,i+{e}^{-2t}\,j+3{e}^{2t}\,k)\cdot (2{e}^{t}i+6{e}^{2t}\,j-2{e}^{-2t}\,k) \\  & =4{e}^{2t}+6-6 \\  & =4{e}^{2t}.\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{1}4{e}^{2t}\,dt \\  & =2{e}^{2t}{|}_{0}^{1} \\  & =2{e}^{2}-2\end{aligned}
$$

## GENERATED HISTORICAL LINEAR-LIFT VARIANT — INELIGIBLE

### exp_cancel_yz — ORIGINAL EVIDENCE (INELIGIBLE)

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y,z)=\left(2\right)\cdot\left(x\,i+z\,j+y\,k\right)$ and $C$ is the path $r(t)=2{e}^{t}\,i+3{e}^{2t}\,j+{e}^{-2t}\,k$ for $t\in [0,1].$

- $\left(2\right)\cdot\left(2{e}^{2}-1\right)$

- $\left(2\right)\cdot\left(4{e}^{4}-4\right)$

- $\left(2\right)\cdot\left(4{e}^{2}-1\right)$

- $\left(2\right)\cdot\left(2{e}^{2}-2\right)$ **correct**

- $\left(2\right)\cdot\left(4{e}^{2}-2\right)$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=2{e}^{t},\,y=3{e}^{2t},\,z={e}^{-2t}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(2\right)\cdot\left(x\,i+z\,j+y\,k\right) \\  & =\left(2\right)\cdot\left(2{e}^{t}\,i+{e}^{-2t}\,j+3{e}^{2t}\,k\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(2{e}^{t})i+\frac{\text{d}}{\text{d}t}(3{e}^{2t})j+\frac{\text{d}}{\text{d}t}({e}^{-2t})j \\  & =2{e}^{t}i+6{e}^{2t}\,j-2{e}^{-2t}\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =\left(2\right)\cdot\left((2{e}^{t}\,i+{e}^{-2t}\,j+3{e}^{2t}\,k)\cdot (2{e}^{t}i+6{e}^{2t}\,j-2{e}^{-2t}\,k)\right) \\  & =\left(2\right)\cdot\left(4{e}^{2t}+6-6\right) \\  & =\left(2\right)\cdot\left(4{e}^{2t}\right).\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =\left(2\right)\cdot\left({\int }_{0}^{1}4{e}^{2t}\,dt\right) \\  & =\left(2\right)\cdot\left(2{e}^{2t}{|}_{0}^{1}\right) \\  & =\left(2\right)\cdot\left(2{e}^{2}-2\right)\end{aligned}
$$

## GENERATED METHOD-BANK VARIANT

### exp_cancel_yz — GENERATED VARIANT

Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)=\left(x\right)\,i+\left(z\right)\,j+\left(y\right)\,k$ and $C$ is the path $r(t)=\left(- 2 e^{3 t}\right)\,i+\left(3 e^{2 t}\right)\,j+\left(- e^{- 2 t}\right)\,k$ for $t\in [0,1]$.

- $-8 + 2 e^{6}$

- $\frac{\left(- 4 e^{3} - 8 + 9 e^{2}\right) e^{2} + 3}{6 e^{2}}$

- $-2 + 2 e^{6}$ **correct**

- $4 + 2 e^{6}$

- $0$

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=- 2 e^{3 t},\qquad y=3 e^{2 t},\qquad z=- e^{- 2 t}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(x\right)\,i+\left(z\right)\,j+\left(y\right)\,k \\ & =\left(\left(- 2 e^{3 t}\right)\right)\,i+\left(\left(- e^{- 2 t}\right)\right)\,j+\left(\left(3 e^{2 t}\right)\right)\,k \\ & =\left(- 2 e^{3 t}\right)\,i+\left(- e^{- 2 t}\right)\,j+\left(3 e^{2 t}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ & =\frac{\mathrm{d}}{\mathrm{d}t}\left(- 2 e^{3 t}\right)\,i+\frac{\mathrm{d}}{\mathrm{d}t}\left(3 e^{2 t}\right)\,j+\frac{\mathrm{d}}{\mathrm{d}t}\left(- e^{- 2 t}\right)\,k \\ & =\left(- 6 e^{3 t}\right)\,i+\left(6 e^{2 t}\right)\,j+\left(2 e^{- 2 t}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(- 2 e^{3 t}\right)\,i+\left(- e^{- 2 t}\right)\,j+\left(3 e^{2 t}\right)\,k\right)\cdot\left(\left(- 6 e^{3 t}\right)\,i+\left(6 e^{2 t}\right)\,j+\left(2 e^{- 2 t}\right)\,k\right) \\ & =\left(\left(- 2 e^{3 t}\right)\cdot\left(- 6 e^{3 t}\right)\right)+\left(\left(- e^{- 2 t}\right)\cdot\left(6 e^{2 t}\right)\right)+\left(\left(3 e^{2 t}\right)\cdot\left(2 e^{- 2 t}\right)\right) \\ & =\left(12 e^{6 t}\right)+\left(-6\right)+\left(6\right) \\ & =12 e^{6 t}\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\ & =\int_{0}^{1}\left(12 e^{6 t}\right)\,\mathrm{d}t \\ & =\left[2 e^{6 t}\right]_{0}^{1} \\ & =\left(2 e^{6 \left(1\right)}\right)+\left(-\left(2 e^{6 \left(0\right)}\right)\right) \\ & =\left(2 e^{6}\right)+\left(-2\right) \\ & =-2 + 2 e^{6}\end{aligned}
$$

## GENERATED METHOD-BANK VARIANT

### exp_cancel_yz — GENERATED VARIANT

Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)=\left(x\right)\,i+\left(z\right)\,j+\left(y\right)\,k$ and $C$ is the path $r(t)=\left(- 2 e^{3 t}\right)\,i+\left(- 3 e^{t}\right)\,j+\left(- e^{- t}\right)\,k$ for $t\in [0,1]$.

- $-5 + 2 e^{6}$

- $1 + 2 e^{6}$

- $- \frac{2 e^{3}}{3} - 3 e + e^{-1} + \frac{8}{3}$

- $-2 + 2 e^{6}$ **correct**

- $0$

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=- 2 e^{3 t},\qquad y=- 3 e^{t},\qquad z=- e^{- t}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(x\right)\,i+\left(z\right)\,j+\left(y\right)\,k \\ & =\left(\left(- 2 e^{3 t}\right)\right)\,i+\left(\left(- e^{- t}\right)\right)\,j+\left(\left(- 3 e^{t}\right)\right)\,k \\ & =\left(- 2 e^{3 t}\right)\,i+\left(- e^{- t}\right)\,j+\left(- 3 e^{t}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ & =\frac{\mathrm{d}}{\mathrm{d}t}\left(- 2 e^{3 t}\right)\,i+\frac{\mathrm{d}}{\mathrm{d}t}\left(- 3 e^{t}\right)\,j+\frac{\mathrm{d}}{\mathrm{d}t}\left(- e^{- t}\right)\,k \\ & =\left(- 6 e^{3 t}\right)\,i+\left(- 3 e^{t}\right)\,j+\left(e^{- t}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(- 2 e^{3 t}\right)\,i+\left(- e^{- t}\right)\,j+\left(- 3 e^{t}\right)\,k\right)\cdot\left(\left(- 6 e^{3 t}\right)\,i+\left(- 3 e^{t}\right)\,j+\left(e^{- t}\right)\,k\right) \\ & =\left(\left(- 2 e^{3 t}\right)\cdot\left(- 6 e^{3 t}\right)\right)+\left(\left(- e^{- t}\right)\cdot\left(- 3 e^{t}\right)\right)+\left(\left(- 3 e^{t}\right)\cdot\left(e^{- t}\right)\right) \\ & =\left(12 e^{6 t}\right)+\left(3\right)+\left(-3\right) \\ & =12 e^{6 t}\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\ & =\int_{0}^{1}\left(12 e^{6 t}\right)\,\mathrm{d}t \\ & =\left[2 e^{6 t}\right]_{0}^{1} \\ & =\left(2 e^{6 \left(1\right)}\right)+\left(-\left(2 e^{6 \left(0\right)}\right)\right) \\ & =\left(2 e^{6}\right)+\left(-2\right) \\ & =-2 + 2 e^{6}\end{aligned}
$$

## ORIGINAL PUBLIC EVIDENCE — INELIGIBLE

### quotient_exp — ORIGINAL EVIDENCE (INELIGIBLE)

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y,z)=\frac{z}{x}\,i+\frac{z}{y}\,j+k$ and $C$ is the path $r(t)={e}^{t}\,i+{e}^{t}\,j+t\,k$ for $t\in [0,1].$

- $2$ **correct**

- $2+e$

- $1$

- $2+{e}^{2}$

- $1+e$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x={e}^{t},\,y={e}^{t},\,z=t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\frac{z}{x}\,i+\frac{z}{y}\,j+k \\  & =t{e}^{-t}\,i+t{e}^{-t}\,j+k.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}({e}^{t})i+\frac{\text{d}}{\text{d}t}({e}^{t})j+\frac{\text{d}}{\text{d}t}(t)k \\  & ={e}^{t}\,i+{e}^{t}\,j+k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(t{e}^{-t}\,i+t{e}^{-t}\,j+k)\cdot ({e}^{t}\,i+{e}^{t}\,j+k) \\  & =t+t+1 \\  & =2t+1.\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{0}^{1}(2t+1)\,dt \\  & ={[{t}^{2}+t]}_{0}^{1} \\  & =2\end{aligned}
$$

## GENERATED HISTORICAL LINEAR-LIFT VARIANT — INELIGIBLE

### quotient_exp — ORIGINAL EVIDENCE (INELIGIBLE)

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y,z)=\left(2\right)\cdot\left(\frac{z}{x}\,i+\frac{z}{y}\,j+k\right)$ and $C$ is the path $r(t)={e}^{t}\,i+{e}^{t}\,j+t\,k$ for $t\in [0,1].$

- $\left(2\right)\cdot\left(2\right)$ **correct**

- $\left(2\right)\cdot\left(2+e\right)$

- $\left(2\right)\cdot\left(1\right)$

- $\left(2\right)\cdot\left(2+{e}^{2}\right)$

- $\left(2\right)\cdot\left(1+e\right)$

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x={e}^{t},\,y={e}^{t},\,z=t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(2\right)\cdot\left(\frac{z}{x}\,i+\frac{z}{y}\,j+k\right) \\  & =\left(2\right)\cdot\left(t{e}^{-t}\,i+t{e}^{-t}\,j+k\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}({e}^{t})i+\frac{\text{d}}{\text{d}t}({e}^{t})j+\frac{\text{d}}{\text{d}t}(t)k \\  & ={e}^{t}\,i+{e}^{t}\,j+k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =\left(2\right)\cdot\left((t{e}^{-t}\,i+t{e}^{-t}\,j+k)\cdot ({e}^{t}\,i+{e}^{t}\,j+k)\right) \\  & =\left(2\right)\cdot\left(t+t+1\right) \\  & =\left(2\right)\cdot\left(2t+1\right).\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{0}^{1}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =\left(2\right)\cdot\left({\int }_{0}^{1}(2t+1)\,dt\right) \\  & =\left(2\right)\cdot\left({[{t}^{2}+t]}_{0}^{1}\right) \\  & =\left(2\right)\cdot\left(2\right)\end{aligned}
$$

## GENERATED METHOD-BANK VARIANT

### quotient_exp — GENERATED VARIANT

Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)=\left(\frac{z}{x}\right)\,i+\left(\frac{z}{y}\right)\,j+\left(1\right)\,k$ and $C$ is the path $r(t)=\left(- 2 e^{3 t}\right)\,i+\left(3 e^{2 t}\right)\,j+\left(- t\right)\,k$ for $t\in [0,1]$.

- $- \frac{7}{3} + \frac{4}{3 e^{3}}$

- $\frac{- 11 e^{3} + 8 + 9 e}{6 e^{3}}$

- $- \frac{7}{2}$ **correct**

- $- \frac{5}{2}$

- $-1$

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=- 2 e^{3 t},\qquad y=3 e^{2 t},\qquad z=- t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(\frac{z}{x}\right)\,i+\left(\frac{z}{y}\right)\,j+\left(1\right)\,k \\ & =\left(\frac{\left(- t\right)}{\left(- 2 e^{3 t}\right)}\right)\,i+\left(\frac{\left(- t\right)}{\left(3 e^{2 t}\right)}\right)\,j+\left(1\right)\,k \\ & =\left(\frac{t e^{- 3 t}}{2}\right)\,i+\left(- \frac{t e^{- 2 t}}{3}\right)\,j+\left(1\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ & =\frac{\mathrm{d}}{\mathrm{d}t}\left(- 2 e^{3 t}\right)\,i+\frac{\mathrm{d}}{\mathrm{d}t}\left(3 e^{2 t}\right)\,j+\frac{\mathrm{d}}{\mathrm{d}t}\left(- t\right)\,k \\ & =\left(- 6 e^{3 t}\right)\,i+\left(6 e^{2 t}\right)\,j+\left(-1\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(\frac{t e^{- 3 t}}{2}\right)\,i+\left(- \frac{t e^{- 2 t}}{3}\right)\,j+\left(1\right)\,k\right)\cdot\left(\left(- 6 e^{3 t}\right)\,i+\left(6 e^{2 t}\right)\,j+\left(-1\right)\,k\right) \\ & =\left(\left(\frac{t e^{- 3 t}}{2}\right)\cdot\left(- 6 e^{3 t}\right)\right)+\left(\left(- \frac{t e^{- 2 t}}{3}\right)\cdot\left(6 e^{2 t}\right)\right)+\left(\left(1\right)\cdot\left(-1\right)\right) \\ & =\left(- 3 t\right)+\left(- 2 t\right)+\left(-1\right) \\ & =- 5 t - 1\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\ & =\int_{0}^{1}\left(- 5 t - 1\right)\,\mathrm{d}t \\ & =\left[- \frac{5 t^{2}}{2} - t\right]_{0}^{1} \\ & =\left(- \left(1\right)\right)+\left(-\left(- \left(0\right)\right)\right)+\left(- \frac{5 \left(1\right)^{2}}{2}\right)+\left(-\left(- \frac{5 \left(0\right)^{2}}{2}\right)\right) \\ & =\left(-1\right)+\left(0\right)+\left(- \frac{5}{2}\right)+\left(0\right) \\ & =- \frac{7}{2}\end{aligned}
$$

## GENERATED METHOD-BANK VARIANT

### quotient_exp — GENERATED VARIANT

Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)=\left(\frac{z}{x}\right)\,i+\left(\frac{z}{y}\right)\,j+\left(1\right)\,k$ and $C$ is the path $r(t)=\left(- 2 e^{3 t}\right)\,i+\left(- 3 e^{t}\right)\,j+\left(- t\right)\,k$ for $t\in [0,1]$.

- $-2$

- $- \frac{11}{6} + \frac{4}{3 e^{3}}$

- $- \frac{7}{3} + \frac{4}{3 e^{3}} + \frac{2}{e}$

- $-3$ **correct**

- $-1$

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=- 2 e^{3 t},\qquad y=- 3 e^{t},\qquad z=- t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(\frac{z}{x}\right)\,i+\left(\frac{z}{y}\right)\,j+\left(1\right)\,k \\ & =\left(\frac{\left(- t\right)}{\left(- 2 e^{3 t}\right)}\right)\,i+\left(\frac{\left(- t\right)}{\left(- 3 e^{t}\right)}\right)\,j+\left(1\right)\,k \\ & =\left(\frac{t e^{- 3 t}}{2}\right)\,i+\left(\frac{t e^{- t}}{3}\right)\,j+\left(1\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ & =\frac{\mathrm{d}}{\mathrm{d}t}\left(- 2 e^{3 t}\right)\,i+\frac{\mathrm{d}}{\mathrm{d}t}\left(- 3 e^{t}\right)\,j+\frac{\mathrm{d}}{\mathrm{d}t}\left(- t\right)\,k \\ & =\left(- 6 e^{3 t}\right)\,i+\left(- 3 e^{t}\right)\,j+\left(-1\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(\frac{t e^{- 3 t}}{2}\right)\,i+\left(\frac{t e^{- t}}{3}\right)\,j+\left(1\right)\,k\right)\cdot\left(\left(- 6 e^{3 t}\right)\,i+\left(- 3 e^{t}\right)\,j+\left(-1\right)\,k\right) \\ & =\left(\left(\frac{t e^{- 3 t}}{2}\right)\cdot\left(- 6 e^{3 t}\right)\right)+\left(\left(\frac{t e^{- t}}{3}\right)\cdot\left(- 3 e^{t}\right)\right)+\left(\left(1\right)\cdot\left(-1\right)\right) \\ & =\left(- 3 t\right)+\left(- t\right)+\left(-1\right) \\ & =- 4 t - 1\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\ & =\int_{0}^{1}\left(- 4 t - 1\right)\,\mathrm{d}t \\ & =\left[- 2 t^{2} - t\right]_{0}^{1} \\ & =\left(- \left(1\right)\right)+\left(-\left(- \left(0\right)\right)\right)+\left(- 2 \left(1\right)^{2}\right)+\left(-\left(- 2 \left(0\right)^{2}\right)\right) \\ & =\left(-1\right)+\left(0\right)+\left(-2\right)+\left(0\right) \\ & =-3\end{aligned}
$$

## ORIGINAL PUBLIC EVIDENCE — INELIGIBLE

### radical_power — ORIGINAL EVIDENCE (INELIGIBLE)

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y,z)=\sqrt{x}\,i+\sqrt{y}\,j+z\,k$ and $C$ is the path $r(t)=t\,i+t\,j+{t}^{2}\,k$ for $t\in [1,2].$

- $\frac{8\sqrt{2}+47}{6}$

- $\frac{5\sqrt{2}+31}{6}$

- $\frac{7\sqrt{2}+32}{6}$

- $\frac{10\sqrt{2}+45}{6}$

- $\frac{16\sqrt{2}+37}{6}$ **correct**

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=t,\,y=t,\,z={t}^{2}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\sqrt{x}\,i+\sqrt{y}\,j+z\,k \\  & =\sqrt{t}\,i+\sqrt{t}\,j+{t}^{2}\,k.\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(t)j+\frac{\text{d}}{\text{d}t}({t}^{2})j \\  & =i+j+2t\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =(\sqrt{t}\,i+\sqrt{t}\,j+{t}^{2}\,k)\cdot (i+j+2t\,k) \\  & =\sqrt{t}+\sqrt{t}+2{t}^{3} \\  & =2\sqrt{t}+2{t}^{3}.\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{1}^{2}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & ={\int }_{1}^{2}(2\sqrt{t}+2{t}^{3})\,dt \\  & ={[\frac{4}{3}{t}^{3/2}+\frac{{t}^{4}}{2}]}_{1}^{2} \\  & =\frac{4}{3}\cdot 2\sqrt{2}+8-\frac{4}{3}-\frac{1}{2} \\  & =\frac{16\sqrt{2}+37}{6}\end{aligned}
$$

## GENERATED HISTORICAL LINEAR-LIFT VARIANT — INELIGIBLE

### radical_power — ORIGINAL EVIDENCE (INELIGIBLE)

Evaluate ${\int }_{C}F\cdot \text{d}r$ given that $F(x,y,z)=\left(2\right)\cdot\left(\sqrt{x}\,i+\sqrt{y}\,j+z\,k\right)$ and $C$ is the path $r(t)=t\,i+t\,j+{t}^{2}\,k$ for $t\in [1,2].$

- $\left(2\right)\cdot\left(\frac{8\sqrt{2}+47}{6}\right)$

- $\left(2\right)\cdot\left(\frac{5\sqrt{2}+31}{6}\right)$

- $\left(2\right)\cdot\left(\frac{7\sqrt{2}+32}{6}\right)$

- $\left(2\right)\cdot\left(\frac{10\sqrt{2}+45}{6}\right)$

- $\left(2\right)\cdot\left(\frac{16\sqrt{2}+37}{6}\right)$ **correct**

We will use the formula

$$
{\int }_{C}F\cdot \text{d}r={\int }_{a}^{b}F(r(t))\cdot {r}^{′}(t)\,\text{d}t.
$$

Along the curve $C,$ we have 

$$
x=t,\,y=t,\,z={t}^{2}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(2\right)\cdot\left(\sqrt{x}\,i+\sqrt{y}\,j+z\,k\right) \\  & =\left(2\right)\cdot\left(\sqrt{t}\,i+\sqrt{t}\,j+{t}^{2}\,k\right).\end{aligned}
$$

Computing ${r}^{′}(t),$ we get 

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}(t)j+\frac{\text{d}}{\text{d}t}({t}^{2})j \\  & =i+j+2t\,k.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot {r}^{′}(t) & =\left(2\right)\cdot\left((\sqrt{t}\,i+\sqrt{t}\,j+{t}^{2}\,k)\cdot (i+j+2t\,k)\right) \\  & =\left(2\right)\cdot\left(\sqrt{t}+\sqrt{t}+2{t}^{3}\right) \\  & =\left(2\right)\cdot\left(2\sqrt{t}+2{t}^{3}\right).\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}{\int }_{C}F(r)\cdot \text{d}r & ={\int }_{1}^{2}F(r(t))\cdot {r}^{′}(t)\,\text{d}t \\  & =\left(2\right)\cdot\left({\int }_{1}^{2}(2\sqrt{t}+2{t}^{3})\,dt\right) \\  & =\left(2\right)\cdot\left({[\frac{4}{3}{t}^{3/2}+\frac{{t}^{4}}{2}]}_{1}^{2}\right) \\  & =\left(2\right)\cdot\left(\frac{4}{3}\cdot 2\sqrt{2}+8-\frac{4}{3}-\frac{1}{2}\right) \\  & =\left(2\right)\cdot\left(\frac{16\sqrt{2}+37}{6}\right)\end{aligned}
$$

## GENERATED METHOD-BANK VARIANT

### radical_power — GENERATED VARIANT

Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)=\left(\sqrt{x}\right)\,i+\left(\sqrt{y}\right)\,j+\left(z\right)\,k$ and $C$ is the path $r(t)=\left(t\right)\,i+\left(3 t\right)\,j+\left(2 t^{2}\right)\,k$ for $t\in [2,3]$.

- $- 4 \sqrt{6} - \frac{4 \sqrt{2}}{3} + 2 \sqrt{3} + 83$

- $-148 - 2 \sqrt{3} + \frac{4 \sqrt{2}}{3} + 4 \sqrt{6}$

- $- 4 \sqrt{6} - \frac{4 \sqrt{2}}{3} + 2 \sqrt{3} + 148$ **correct**

- $- 4 \sqrt{6} - \frac{4 \sqrt{2}}{3} + 2 \sqrt{3} + 18$

- $130$

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t,\qquad y=3 t,\qquad z=2 t^{2}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(\sqrt{x}\right)\,i+\left(\sqrt{y}\right)\,j+\left(z\right)\,k \\ & =\left(\sqrt{\left(t\right)}\right)\,i+\left(\sqrt{\left(3 t\right)}\right)\,j+\left(\left(2 t^{2}\right)\right)\,k \\ & =\left(\sqrt{t}\right)\,i+\left(\sqrt{3} \sqrt{t}\right)\,j+\left(2 t^{2}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ & =\frac{\mathrm{d}}{\mathrm{d}t}\left(t\right)\,i+\frac{\mathrm{d}}{\mathrm{d}t}\left(3 t\right)\,j+\frac{\mathrm{d}}{\mathrm{d}t}\left(2 t^{2}\right)\,k \\ & =\left(1\right)\,i+\left(3\right)\,j+\left(4 t\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(\sqrt{t}\right)\,i+\left(\sqrt{3} \sqrt{t}\right)\,j+\left(2 t^{2}\right)\,k\right)\cdot\left(\left(1\right)\,i+\left(3\right)\,j+\left(4 t\right)\,k\right) \\ & =\left(\left(\sqrt{t}\right)\cdot\left(1\right)\right)+\left(\left(\sqrt{3} \sqrt{t}\right)\cdot\left(3\right)\right)+\left(\left(2 t^{2}\right)\cdot\left(4 t\right)\right) \\ & =\left(\sqrt{t}\right)+\left(3 \sqrt{3} \sqrt{t}\right)+\left(8 t^{3}\right) \\ & =\sqrt{t} + 3 \sqrt{3} \sqrt{t} + 8 t^{3}\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_{2}^{3}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\ & =\int_{2}^{3}\left(\sqrt{t} + 3 \sqrt{3} \sqrt{t} + 8 t^{3}\right)\,\mathrm{d}t \\ & =\left[\frac{2 t^{\frac{3}{2}}}{3} + 2 \sqrt{3} t^{\frac{3}{2}} + 2 t^{4}\right]_{2}^{3} \\ & =\left(2 \left(3\right)^{4}\right)+\left(-\left(2 \left(2\right)^{4}\right)\right)+\left(\frac{2 \left(3\right)^{\frac{3}{2}}}{3}\right)+\left(-\left(\frac{2 \left(2\right)^{\frac{3}{2}}}{3}\right)\right)+\left(2 \sqrt{3} \left(3\right)^{\frac{3}{2}}\right)+\left(-\left(2 \sqrt{3} \left(2\right)^{\frac{3}{2}}\right)\right) \\ & =\left(162\right)+\left(-32\right)+\left(2 \sqrt{3}\right)+\left(- \frac{4 \sqrt{2}}{3}\right)+\left(18\right)+\left(- 4 \sqrt{6}\right) \\ & =- 4 \sqrt{6} - \frac{4 \sqrt{2}}{3} + 2 \sqrt{3} + 148\end{aligned}
$$

## GENERATED METHOD-BANK VARIANT

### radical_power — GENERATED VARIANT

Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)=\left(\sqrt{x}\right)\,i+\left(\sqrt{y}\right)\,j+\left(z\right)\,k$ and $C$ is the path $r(t)=\left(t\right)\,i+\left(t\right)\,j+\left(2 t^{2}\right)\,k$ for $t\in [1,3]$.

- $- \frac{4}{3} + 4 \sqrt{3}$

- $4 \sqrt{3} + \frac{236}{3}$

- $- \frac{476}{3} - 4 \sqrt{3}$

- $4 \sqrt{3} + \frac{476}{3}$ **correct**

- $160$

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t,\qquad y=t,\qquad z=2 t^{2}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(\sqrt{x}\right)\,i+\left(\sqrt{y}\right)\,j+\left(z\right)\,k \\ & =\left(\sqrt{\left(t\right)}\right)\,i+\left(\sqrt{\left(t\right)}\right)\,j+\left(\left(2 t^{2}\right)\right)\,k \\ & =\left(\sqrt{t}\right)\,i+\left(\sqrt{t}\right)\,j+\left(2 t^{2}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ & =\frac{\mathrm{d}}{\mathrm{d}t}\left(t\right)\,i+\frac{\mathrm{d}}{\mathrm{d}t}\left(t\right)\,j+\frac{\mathrm{d}}{\mathrm{d}t}\left(2 t^{2}\right)\,k \\ & =\left(1\right)\,i+\left(1\right)\,j+\left(4 t\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(\sqrt{t}\right)\,i+\left(\sqrt{t}\right)\,j+\left(2 t^{2}\right)\,k\right)\cdot\left(\left(1\right)\,i+\left(1\right)\,j+\left(4 t\right)\,k\right) \\ & =\left(\left(\sqrt{t}\right)\cdot\left(1\right)\right)+\left(\left(\sqrt{t}\right)\cdot\left(1\right)\right)+\left(\left(2 t^{2}\right)\cdot\left(4 t\right)\right) \\ & =\left(\sqrt{t}\right)+\left(\sqrt{t}\right)+\left(8 t^{3}\right) \\ & =2 \sqrt{t} + 8 t^{3}\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_{1}^{3}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\ & =\int_{1}^{3}\left(2 \sqrt{t} + 8 t^{3}\right)\,\mathrm{d}t \\ & =\left[\frac{4 t^{\frac{3}{2}}}{3} + 2 t^{4}\right]_{1}^{3} \\ & =\left(2 \left(3\right)^{4}\right)+\left(-\left(2 \left(1\right)^{4}\right)\right)+\left(\frac{4 \left(3\right)^{\frac{3}{2}}}{3}\right)+\left(-\left(\frac{4 \left(1\right)^{\frac{3}{2}}}{3}\right)\right) \\ & =\left(162\right)+\left(-2\right)+\left(4 \sqrt{3}\right)+\left(- \frac{4}{3}\right) \\ & =4 \sqrt{3} + \frac{476}{3}\end{aligned}
$$

## GENERATED AUTHORED EASY

### constant_affine — GENERATED VARIANT

Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)=\left(-2\right)\,i+\left(1\right)\,j+\left(-3\right)\,k$ and $C$ is the path $r(t)=\left(- 2 t - 1\right)\,i+\left(1 - 3 t\right)\,j+\left(3 t\right)\,k$ for $t\in [0,2]$.

- $-10$

- $-16$ **correct**

- $2$

- $-24$

- $16$

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=- 2 t - 1,\qquad y=1 - 3 t,\qquad z=3 t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(-2\right)\,i+\left(1\right)\,j+\left(-3\right)\,k \\ & =\left(-2\right)\,i+\left(1\right)\,j+\left(-3\right)\,k \\ & =\left(-2\right)\,i+\left(1\right)\,j+\left(-3\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ & =\frac{\mathrm{d}}{\mathrm{d}t}\left(- 2 t - 1\right)\,i+\frac{\mathrm{d}}{\mathrm{d}t}\left(1 - 3 t\right)\,j+\frac{\mathrm{d}}{\mathrm{d}t}\left(3 t\right)\,k \\ & =\left(-2\right)\,i+\left(-3\right)\,j+\left(3\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(-2\right)\,i+\left(1\right)\,j+\left(-3\right)\,k\right)\cdot\left(\left(-2\right)\,i+\left(-3\right)\,j+\left(3\right)\,k\right) \\ & =\left(\left(-2\right)\cdot\left(-2\right)\right)+\left(\left(1\right)\cdot\left(-3\right)\right)+\left(\left(-3\right)\cdot\left(3\right)\right) \\ & =\left(4\right)+\left(-3\right)+\left(-9\right) \\ & =-8\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_{0}^{2}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\ & =\int_{0}^{2}\left(-8\right)\,\mathrm{d}t \\ & =\left[- 8 t\right]_{0}^{2} \\ & =\left(- 8 \left(2\right)\right)+\left(-\left(- 8 \left(0\right)\right)\right) \\ & =\left(-16\right)+\left(0\right) \\ & =-16\end{aligned}
$$

## GENERATED AUTHORED EASY

### constant_affine — GENERATED VARIANT

Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)=\left(3\right)\,i+\left(1\right)\,j+\left(-2\right)\,k$ and $C$ is the path $r(t)=\left(2 - 2 t\right)\,i+\left(1 - 2 t\right)\,j+\left(1 - 2 t\right)\,k$ for $t\in [0,1]$.

- $-4$ **correct**

- $2$

- $4$

- $-2$

- $-8$

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=2 - 2 t,\qquad y=1 - 2 t,\qquad z=1 - 2 t.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(3\right)\,i+\left(1\right)\,j+\left(-2\right)\,k \\ & =\left(3\right)\,i+\left(1\right)\,j+\left(-2\right)\,k \\ & =\left(3\right)\,i+\left(1\right)\,j+\left(-2\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ & =\frac{\mathrm{d}}{\mathrm{d}t}\left(2 - 2 t\right)\,i+\frac{\mathrm{d}}{\mathrm{d}t}\left(1 - 2 t\right)\,j+\frac{\mathrm{d}}{\mathrm{d}t}\left(1 - 2 t\right)\,k \\ & =\left(-2\right)\,i+\left(-2\right)\,j+\left(-2\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(3\right)\,i+\left(1\right)\,j+\left(-2\right)\,k\right)\cdot\left(\left(-2\right)\,i+\left(-2\right)\,j+\left(-2\right)\,k\right) \\ & =\left(\left(3\right)\cdot\left(-2\right)\right)+\left(\left(1\right)\cdot\left(-2\right)\right)+\left(\left(-2\right)\cdot\left(-2\right)\right) \\ & =\left(-6\right)+\left(-2\right)+\left(4\right) \\ & =-4\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\ & =\int_{0}^{1}\left(-4\right)\,\mathrm{d}t \\ & =\left[- 4 t\right]_{0}^{1} \\ & =\left(- 4 \left(1\right)\right)+\left(-\left(- 4 \left(0\right)\right)\right) \\ & =\left(-4\right)+\left(0\right) \\ & =-4\end{aligned}
$$

## GENERATED AUTHORED MODERATE

### diagonal_power — GENERATED VARIANT

Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)=\left(- x\right)\,i+\left(y\right)\,j+\left(- 2 z\right)\,k$ and $C$ is the path $r(t)=\left(t\right)\,i+\left(t^{2}\right)\,j+\left(t^{3}\right)\,k$ for $t\in [0,1]$.

- $- \frac{3}{2}$

- $-1$ **correct**

- $0$

- $- \frac{1}{2}$

- $1$

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t,\qquad y=t^{2},\qquad z=t^{3}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(- x\right)\,i+\left(y\right)\,j+\left(- 2 z\right)\,k \\ & =\left(- \left(t\right)\right)\,i+\left(\left(t^{2}\right)\right)\,j+\left(- 2 \left(t^{3}\right)\right)\,k \\ & =\left(- t\right)\,i+\left(t^{2}\right)\,j+\left(- 2 t^{3}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ & =\frac{\mathrm{d}}{\mathrm{d}t}\left(t\right)\,i+\frac{\mathrm{d}}{\mathrm{d}t}\left(t^{2}\right)\,j+\frac{\mathrm{d}}{\mathrm{d}t}\left(t^{3}\right)\,k \\ & =\left(1\right)\,i+\left(2 t\right)\,j+\left(3 t^{2}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(- t\right)\,i+\left(t^{2}\right)\,j+\left(- 2 t^{3}\right)\,k\right)\cdot\left(\left(1\right)\,i+\left(2 t\right)\,j+\left(3 t^{2}\right)\,k\right) \\ & =\left(\left(- t\right)\cdot\left(1\right)\right)+\left(\left(t^{2}\right)\cdot\left(2 t\right)\right)+\left(\left(- 2 t^{3}\right)\cdot\left(3 t^{2}\right)\right) \\ & =\left(- t\right)+\left(2 t^{3}\right)+\left(- 6 t^{5}\right) \\ & =- 6 t^{5} + 2 t^{3} - t\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\ & =\int_{0}^{1}\left(- 6 t^{5} + 2 t^{3} - t\right)\,\mathrm{d}t \\ & =\left[- t^{6} + \frac{t^{4}}{2} - \frac{t^{2}}{2}\right]_{0}^{1} \\ & =\left(\frac{\left(1\right)^{4}}{2}\right)+\left(-\left(\frac{\left(0\right)^{4}}{2}\right)\right)+\left(- \left(1\right)^{6}\right)+\left(-\left(- \left(0\right)^{6}\right)\right)+\left(- \frac{\left(1\right)^{2}}{2}\right)+\left(-\left(- \frac{\left(0\right)^{2}}{2}\right)\right) \\ & =\left(\frac{1}{2}\right)+\left(0\right)+\left(-1\right)+\left(0\right)+\left(- \frac{1}{2}\right)+\left(0\right) \\ & =-1\end{aligned}
$$

## GENERATED AUTHORED MODERATE

### diagonal_power — GENERATED VARIANT

Evaluate $\displaystyle\int_C F\cdot\mathrm{d}r$ given that $F(x,y,z)=\left(3 x\right)\,i+\left(3 y\right)\,j+\left(2 z\right)\,k$ and $C$ is the path $r(t)=\left(t\right)\,i+\left(t^{2}\right)\,j+\left(t^{3}\right)\,k$ for $t\in [0,2]$.

- $94$ **correct**

- $88$

- $-94$

- $70$

- $30$

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t,\qquad y=t^{2},\qquad z=t^{3}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =\left(3 x\right)\,i+\left(3 y\right)\,j+\left(2 z\right)\,k \\ & =\left(3 \left(t\right)\right)\,i+\left(3 \left(t^{2}\right)\right)\,j+\left(2 \left(t^{3}\right)\right)\,k \\ & =\left(3 t\right)\,i+\left(3 t^{2}\right)\,j+\left(2 t^{3}\right)\,k\end{aligned}
$$

Computing $r^{\prime}(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ & =\frac{\mathrm{d}}{\mathrm{d}t}\left(t\right)\,i+\frac{\mathrm{d}}{\mathrm{d}t}\left(t^{2}\right)\,j+\frac{\mathrm{d}}{\mathrm{d}t}\left(t^{3}\right)\,k \\ & =\left(1\right)\,i+\left(2 t\right)\,j+\left(3 t^{2}\right)\,k\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =\left(\left(3 t\right)\,i+\left(3 t^{2}\right)\,j+\left(2 t^{3}\right)\,k\right)\cdot\left(\left(1\right)\,i+\left(2 t\right)\,j+\left(3 t^{2}\right)\,k\right) \\ & =\left(\left(3 t\right)\cdot\left(1\right)\right)+\left(\left(3 t^{2}\right)\cdot\left(2 t\right)\right)+\left(\left(2 t^{3}\right)\cdot\left(3 t^{2}\right)\right) \\ & =\left(3 t\right)+\left(6 t^{3}\right)+\left(6 t^{5}\right) \\ & =6 t^{5} + 6 t^{3} + 3 t\end{aligned}
$$

Finally, we evaluate the integral as follows:

$$
\begin{aligned}\int_C F\cdot\mathrm{d}r & =\int_{0}^{2}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\ & =\int_{0}^{2}\left(6 t^{5} + 6 t^{3} + 3 t\right)\,\mathrm{d}t \\ & =\left[t^{6} + \frac{3 t^{4}}{2} + \frac{3 t^{2}}{2}\right]_{0}^{2} \\ & =\left(\left(2\right)^{6}\right)+\left(-\left(\left(0\right)^{6}\right)\right)+\left(\frac{3 \left(2\right)^{2}}{2}\right)+\left(-\left(\frac{3 \left(0\right)^{2}}{2}\right)\right)+\left(\frac{3 \left(2\right)^{4}}{2}\right)+\left(-\left(\frac{3 \left(0\right)^{4}}{2}\right)\right) \\ & =\left(64\right)+\left(0\right)+\left(6\right)+\left(0\right)+\left(24\right)+\left(0\right) \\ & =94\end{aligned}
$$
