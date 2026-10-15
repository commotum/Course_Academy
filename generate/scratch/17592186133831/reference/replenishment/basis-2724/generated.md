## authored-extension — easy
Template `exponential_root`, profile `authored_exponential_root`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(- x y^{2})\,i+(- 8 y)\,j$ and $C$ is the path $r(t)=(e^{t})\,i+(\sqrt{t})\,j$ for $t\in [1,2]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{1}^{2}(- 8 \sqrt{t} - t e^{t})\,dt$
- $\int_{1}^{2}(-4)\,dt$
- $\int_{1}^{2}(t e^{2 t} + 4)\,dt$
- $\int_{1}^{2}(- t e^{2 t} - 4)\,dt$ **Correct**
- $\int_{1}^{2}(- t e^{2 t})\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=e^{t},\,y=\sqrt{t}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- x y^{2})\,i+(- 8 y)\,j \\  & =(- (e^{t}) (\sqrt{t})^{2})\,i+(- 8 (\sqrt{t}))\,j \\  & =(- t e^{t})\,i+(- 8 \sqrt{t})\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(e^{t})i+\frac{\mathrm{d}}{\mathrm{d}t}(\sqrt{t})j \\  & =(e^{t})\,i+(\frac{1}{2 \sqrt{t}})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((- t e^{t})\,i+(- 8 \sqrt{t})\,j)\cdot ((e^{t})\,i+(\frac{1}{2 \sqrt{t}})\,j) \\  & =(- t e^{t})\cdot (e^{t})+(- 8 \sqrt{t})\cdot (\frac{1}{2 \sqrt{t}}) \\  & =- t e^{2 t} - 4.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{1}^{2}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{1}^{2}(- t e^{2 t} - 4)\,dt.\end{aligned}
$$

---

## authored-extension — easy
Template `rotation`, profile `authored_rotation`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(y)\,i+(- x)\,j$ and $C$ is the path $r(t)=(\cos{\left(t \right)})\,i+(\sin{\left(t \right)})\,j$ for $t\in [0,\frac{2 \pi}{3}]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{\frac{2 \pi}{3}}(1)\,dt$
- $\int_{0}^{\frac{2 \pi}{3}}(\sin{\left(t \right)} - \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{2 \pi}{3}}(-1)\,dt$ **Correct**
- $\int_{0}^{\frac{2 \pi}{3}}(- \cos^{2}{\left(t \right)})\,dt$
- $\int_{0}^{\frac{2 \pi}{3}}(- \sin^{2}{\left(t \right)})\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=\cos{\left(t \right)},\,y=\sin{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(y)\,i+(- x)\,j \\  & =((\sin{\left(t \right)}))\,i+(- (\cos{\left(t \right)}))\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(\cos{\left(t \right)})i+\frac{\mathrm{d}}{\mathrm{d}t}(\sin{\left(t \right)})j \\  & =(- \sin{\left(t \right)})\,i+(\cos{\left(t \right)})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((\sin{\left(t \right)})\,i+(- \cos{\left(t \right)})\,j)\cdot ((- \sin{\left(t \right)})\,i+(\cos{\left(t \right)})\,j) \\  & =(\sin{\left(t \right)})\cdot (- \sin{\left(t \right)})+(- \cos{\left(t \right)})\cdot (\cos{\left(t \right)}) \\  & =-1.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{\frac{2 \pi}{3}}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{\frac{2 \pi}{3}}(-1)\,dt.\end{aligned}
$$

---

## authored-extension — easy
Template `exponential_root`, profile `authored_exponential_root`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(x y^{2})\,i+(2 y)\,j$ and $C$ is the path $r(t)=(e^{t})\,i+(\sqrt{t})\,j$ for $t\in [1,3]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{1}^{3}(t e^{2 t})\,dt$
- $\int_{1}^{3}(- t e^{2 t} - 1)\,dt$
- $\int_{1}^{3}(2 \sqrt{t} + t e^{t})\,dt$
- $\int_{1}^{3}(1)\,dt$
- $\int_{1}^{3}(t e^{2 t} + 1)\,dt$ **Correct**

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=e^{t},\,y=\sqrt{t}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(x y^{2})\,i+(2 y)\,j \\  & =((e^{t}) (\sqrt{t})^{2})\,i+(2 (\sqrt{t}))\,j \\  & =(t e^{t})\,i+(2 \sqrt{t})\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(e^{t})i+\frac{\mathrm{d}}{\mathrm{d}t}(\sqrt{t})j \\  & =(e^{t})\,i+(\frac{1}{2 \sqrt{t}})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((t e^{t})\,i+(2 \sqrt{t})\,j)\cdot ((e^{t})\,i+(\frac{1}{2 \sqrt{t}})\,j) \\  & =(t e^{t})\cdot (e^{t})+(2 \sqrt{t})\cdot (\frac{1}{2 \sqrt{t}}) \\  & =t e^{2 t} + 1.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{1}^{3}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{1}^{3}(t e^{2 t} + 1)\,dt.\end{aligned}
$$

---

## authored-extension — moderate
Template `monomial`, profile `authored_monomial`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(- y^{2})\,i+(4 x^{2})\,j$ and $C$ is the path $r(t)=(t^{2})\,i+(t^{3})\,j$ for $t\in [0,2]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{2}(12 t^{6})\,dt$
- $\int_{0}^{2}(2 t^{7} - 12 t^{6})\,dt$
- $\int_{0}^{2}(- t^{6} + 4 t^{4})\,dt$
- $\int_{0}^{2}(- 2 t^{7})\,dt$
- $\int_{0}^{2}(- 2 t^{7} + 12 t^{6})\,dt$ **Correct**

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t^{2},\,y=t^{3}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- y^{2})\,i+(4 x^{2})\,j \\  & =(- (t^{3})^{2})\,i+(4 (t^{2})^{2})\,j \\  & =(- t^{6})\,i+(4 t^{4})\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(t^{2})i+\frac{\mathrm{d}}{\mathrm{d}t}(t^{3})j \\  & =(2 t)\,i+(3 t^{2})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((- t^{6})\,i+(4 t^{4})\,j)\cdot ((2 t)\,i+(3 t^{2})\,j) \\  & =(- t^{6})\cdot (2 t)+(4 t^{4})\cdot (3 t^{2}) \\  & =- 2 t^{7} + 12 t^{6}.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{2}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{2}(- 2 t^{7} + 12 t^{6})\,dt.\end{aligned}
$$

---

## authored-extension — moderate
Template `monomial`, profile `authored_monomial`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(y^{2})\,i+(- 2 x^{2})\,j$ and $C$ is the path $r(t)=(t^{4})\,i+(t^{3})\,j$ for $t\in [0,3]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{3}(- 2 t^{8} + t^{6})\,dt$
- $\int_{0}^{3}(- 6 t^{10} + 4 t^{9})\,dt$ **Correct**
- $\int_{0}^{3}(4 t^{9})\,dt$
- $\int_{0}^{3}(6 t^{10} - 4 t^{9})\,dt$
- $\int_{0}^{3}(- 6 t^{10})\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t^{4},\,y=t^{3}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(y^{2})\,i+(- 2 x^{2})\,j \\  & =((t^{3})^{2})\,i+(- 2 (t^{4})^{2})\,j \\  & =(t^{6})\,i+(- 2 t^{8})\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(t^{4})i+\frac{\mathrm{d}}{\mathrm{d}t}(t^{3})j \\  & =(4 t^{3})\,i+(3 t^{2})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((t^{6})\,i+(- 2 t^{8})\,j)\cdot ((4 t^{3})\,i+(3 t^{2})\,j) \\  & =(t^{6})\cdot (4 t^{3})+(- 2 t^{8})\cdot (3 t^{2}) \\  & =- 6 t^{10} + 4 t^{9}.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{3}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{3}(- 6 t^{10} + 4 t^{9})\,dt.\end{aligned}
$$

---

## authored-extension — moderate
Template `monomial`, profile `authored_monomial`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(y^{2})\,i+(- x^{2})\,j$ and $C$ is the path $r(t)=(t^{3})\,i+(t^{2})\,j$ for $t\in [0,1]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{1}(3 t^{6})\,dt$
- $\int_{0}^{1}(2 t^{7} - 3 t^{6})\,dt$
- $\int_{0}^{1}(- 2 t^{7} + 3 t^{6})\,dt$ **Correct**
- $\int_{0}^{1}(- 2 t^{7})\,dt$
- $\int_{0}^{1}(- t^{6} + t^{4})\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t^{3},\,y=t^{2}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(y^{2})\,i+(- x^{2})\,j \\  & =((t^{2})^{2})\,i+(- (t^{3})^{2})\,j \\  & =(t^{4})\,i+(- t^{6})\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(t^{3})i+\frac{\mathrm{d}}{\mathrm{d}t}(t^{2})j \\  & =(3 t^{2})\,i+(2 t)\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((t^{4})\,i+(- t^{6})\,j)\cdot ((3 t^{2})\,i+(2 t)\,j) \\  & =(t^{4})\cdot (3 t^{2})+(- t^{6})\cdot (2 t) \\  & =- 2 t^{7} + 3 t^{6}.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{1}(- 2 t^{7} + 3 t^{6})\,dt.\end{aligned}
$$

---

## authored-extension — moderate
Template `monomial`, profile `authored_monomial`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(- 3 y^{2})\,i+(- 3 x^{2})\,j$ and $C$ is the path $r(t)=(t^{2})\,i+(t^{4})\,j$ for $t\in [0,1]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{1}(- 3 t^{8} - 3 t^{4})\,dt$
- $\int_{0}^{1}(- 12 t^{7})\,dt$
- $\int_{0}^{1}(- 6 t^{9})\,dt$
- $\int_{0}^{1}(6 t^{9} + 12 t^{7})\,dt$
- $\int_{0}^{1}(- 6 t^{9} - 12 t^{7})\,dt$ **Correct**

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t^{2},\,y=t^{4}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- 3 y^{2})\,i+(- 3 x^{2})\,j \\  & =(- 3 (t^{4})^{2})\,i+(- 3 (t^{2})^{2})\,j \\  & =(- 3 t^{8})\,i+(- 3 t^{4})\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(t^{2})i+\frac{\mathrm{d}}{\mathrm{d}t}(t^{4})j \\  & =(2 t)\,i+(4 t^{3})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((- 3 t^{8})\,i+(- 3 t^{4})\,j)\cdot ((2 t)\,i+(4 t^{3})\,j) \\  & =(- 3 t^{8})\cdot (2 t)+(- 3 t^{4})\cdot (4 t^{3}) \\  & =- 6 t^{9} - 12 t^{7}.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{1}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{1}(- 6 t^{9} - 12 t^{7})\,dt.\end{aligned}
$$

---

## authored-extension — moderate
Template `monomial`, profile `authored_monomial`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(- 2 y^{2})\,i+(- 4 x^{2})\,j$ and $C$ is the path $r(t)=(t^{2})\,i+(t^{3})\,j$ for $t\in [0,3]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{3}(- 2 t^{6} - 4 t^{4})\,dt$
- $\int_{0}^{3}(- 4 t^{7} - 12 t^{6})\,dt$ **Correct**
- $\int_{0}^{3}(4 t^{7} + 12 t^{6})\,dt$
- $\int_{0}^{3}(- 4 t^{7})\,dt$
- $\int_{0}^{3}(- 12 t^{6})\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t^{2},\,y=t^{3}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- 2 y^{2})\,i+(- 4 x^{2})\,j \\  & =(- 2 (t^{3})^{2})\,i+(- 4 (t^{2})^{2})\,j \\  & =(- 2 t^{6})\,i+(- 4 t^{4})\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(t^{2})i+\frac{\mathrm{d}}{\mathrm{d}t}(t^{3})j \\  & =(2 t)\,i+(3 t^{2})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((- 2 t^{6})\,i+(- 4 t^{4})\,j)\cdot ((2 t)\,i+(3 t^{2})\,j) \\  & =(- 2 t^{6})\cdot (2 t)+(- 4 t^{4})\cdot (3 t^{2}) \\  & =- 4 t^{7} - 12 t^{6}.\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{3}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{3}(- 4 t^{7} - 12 t^{6})\,dt.\end{aligned}
$$

---

## authored-extension — hard
Template `mixed_spiral`, profile `authored_mixed_spiral`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(- x - 4 y)\,i+(x - 3 y)\,j$ and $C$ is the path $r(t)=(t \cos{\left(t \right)})\,i+(t \sin{\left(t \right)})\,j$ for $t\in [0,\frac{\pi}{3}]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{\frac{\pi}{3}}(t^{2} \left(4 \sin^{2}{\left(t \right)} - 2 \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right) + t \left(- 3 \sin^{2}{\left(t \right)} - 3 \sin{\left(t \right)} \cos{\left(t \right)} - \cos^{2}{\left(t \right)}\right))\,dt$ **Correct**
- $\int_{0}^{\frac{\pi}{3}}(- 3 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} + t^{2} \cos^{2}{\left(t \right)} - 3 t \sin^{2}{\left(t \right)} + t \sin{\left(t \right)} \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{\pi}{3}}(- 7 t \sin{\left(t \right)})\,dt$
- $\int_{0}^{\frac{\pi}{3}}(- t^{2} \left(4 \sin^{2}{\left(t \right)} - 2 \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right) - t \left(- 3 \sin^{2}{\left(t \right)} - 3 \sin{\left(t \right)} \cos{\left(t \right)} - \cos^{2}{\left(t \right)}\right))\,dt$
- $\int_{0}^{\frac{\pi}{3}}(4 t^{2} \sin^{2}{\left(t \right)} + t^{2} \sin{\left(t \right)} \cos{\left(t \right)} - 4 t \sin{\left(t \right)} \cos{\left(t \right)} - t \cos^{2}{\left(t \right)})\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t \cos{\left(t \right)},\,y=t \sin{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- x - 4 y)\,i+(x - 3 y)\,j \\  & =(- (t \cos{\left(t \right)}) - 4 (t \sin{\left(t \right)}))\,i+((t \cos{\left(t \right)}) - 3 (t \sin{\left(t \right)}))\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(t \cos{\left(t \right)})i+\frac{\mathrm{d}}{\mathrm{d}t}(t \sin{\left(t \right)})j \\  & =(- t \sin{\left(t \right)} + \cos{\left(t \right)})\,i+(t \cos{\left(t \right)} + \sin{\left(t \right)})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((- 4 t \sin{\left(t \right)} - t \cos{\left(t \right)})\,i+(- 3 t \sin{\left(t \right)} + t \cos{\left(t \right)})\,j)\cdot ((- t \sin{\left(t \right)} + \cos{\left(t \right)})\,i+(t \cos{\left(t \right)} + \sin{\left(t \right)})\,j) \\  & =(- 4 t \sin{\left(t \right)} - t \cos{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(- 3 t \sin{\left(t \right)} + t \cos{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)}) \\  & =(- t \cos{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(- 4 t \sin{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(t \cos{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)})+(- 3 t \sin{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)}) \\  & =4 t^{2} \sin^{2}{\left(t \right)} - 2 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} + t^{2} \cos^{2}{\left(t \right)} - 3 t \sin^{2}{\left(t \right)} - 3 t \sin{\left(t \right)} \cos{\left(t \right)} - t \cos^{2}{\left(t \right)} \\  & =t^{2} \left(4 \sin^{2}{\left(t \right)} - 2 \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right) + t \left(- 3 \sin^{2}{\left(t \right)} - 3 \sin{\left(t \right)} \cos{\left(t \right)} - \cos^{2}{\left(t \right)}\right).\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{\frac{\pi}{3}}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{\frac{\pi}{3}}(t^{2} \left(4 \sin^{2}{\left(t \right)} - 2 \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right) + t \left(- 3 \sin^{2}{\left(t \right)} - 3 \sin{\left(t \right)} \cos{\left(t \right)} - \cos^{2}{\left(t \right)}\right))\,dt.\end{aligned}
$$

---

## authored-extension — hard
Template `mixed_spiral`, profile `authored_mixed_spiral`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(x + 2 y)\,i+(x + 3 y)\,j$ and $C$ is the path $r(t)=(t \cos{\left(t \right)})\,i+(t \sin{\left(t \right)})\,j$ for $t\in [0,\frac{4 \pi}{3}]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{\frac{4 \pi}{3}}(- 2 t^{2} \sin^{2}{\left(t \right)} - t^{2} \sin{\left(t \right)} \cos{\left(t \right)} + 2 t \sin{\left(t \right)} \cos{\left(t \right)} + t \cos^{2}{\left(t \right)})\,dt$
- $\int_{0}^{\frac{4 \pi}{3}}(t^{2} \left(- 2 \sin^{2}{\left(t \right)} + 2 \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right) + t \left(3 \sin^{2}{\left(t \right)} + 3 \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right))\,dt$ **Correct**
- $\int_{0}^{\frac{4 \pi}{3}}(3 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} + t^{2} \cos^{2}{\left(t \right)} + 3 t \sin^{2}{\left(t \right)} + t \sin{\left(t \right)} \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{4 \pi}{3}}(5 t \sin{\left(t \right)} + 2 t \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{4 \pi}{3}}(- t^{2} \left(- 2 \sin^{2}{\left(t \right)} + 2 \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right) - t \left(3 \sin^{2}{\left(t \right)} + 3 \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right))\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t \cos{\left(t \right)},\,y=t \sin{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(x + 2 y)\,i+(x + 3 y)\,j \\  & =((t \cos{\left(t \right)}) + 2 (t \sin{\left(t \right)}))\,i+((t \cos{\left(t \right)}) + 3 (t \sin{\left(t \right)}))\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(t \cos{\left(t \right)})i+\frac{\mathrm{d}}{\mathrm{d}t}(t \sin{\left(t \right)})j \\  & =(- t \sin{\left(t \right)} + \cos{\left(t \right)})\,i+(t \cos{\left(t \right)} + \sin{\left(t \right)})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((2 t \sin{\left(t \right)} + t \cos{\left(t \right)})\,i+(3 t \sin{\left(t \right)} + t \cos{\left(t \right)})\,j)\cdot ((- t \sin{\left(t \right)} + \cos{\left(t \right)})\,i+(t \cos{\left(t \right)} + \sin{\left(t \right)})\,j) \\  & =(2 t \sin{\left(t \right)} + t \cos{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(3 t \sin{\left(t \right)} + t \cos{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)}) \\  & =(t \cos{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(2 t \sin{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(t \cos{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)})+(3 t \sin{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)}) \\  & =- 2 t^{2} \sin^{2}{\left(t \right)} + 2 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} + t^{2} \cos^{2}{\left(t \right)} + 3 t \sin^{2}{\left(t \right)} + 3 t \sin{\left(t \right)} \cos{\left(t \right)} + t \cos^{2}{\left(t \right)} \\  & =t^{2} \left(- 2 \sin^{2}{\left(t \right)} + 2 \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right) + t \left(3 \sin^{2}{\left(t \right)} + 3 \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right).\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{\frac{4 \pi}{3}}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{\frac{4 \pi}{3}}(t^{2} \left(- 2 \sin^{2}{\left(t \right)} + 2 \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right) + t \left(3 \sin^{2}{\left(t \right)} + 3 \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right))\,dt.\end{aligned}
$$

---

## authored-extension — hard
Template `mixed_spiral`, profile `authored_mixed_spiral`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(x + y)\,i+(- 4 x + 3 y)\,j$ and $C$ is the path $r(t)=(t \cos{\left(t \right)})\,i+(t \sin{\left(t \right)})\,j$ for $t\in [0,\frac{2 \pi}{3}]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{\frac{2 \pi}{3}}(t^{2} \left(- \sin^{2}{\left(t \right)} + 2 \sin{\left(t \right)} \cos{\left(t \right)} - 4 \cos^{2}{\left(t \right)}\right) + t \left(3 \sin^{2}{\left(t \right)} - 3 \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right))\,dt$ **Correct**
- $\int_{0}^{\frac{2 \pi}{3}}(4 t \sin{\left(t \right)} - 3 t \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{2 \pi}{3}}(- t^{2} \sin^{2}{\left(t \right)} - t^{2} \sin{\left(t \right)} \cos{\left(t \right)} + t \sin{\left(t \right)} \cos{\left(t \right)} + t \cos^{2}{\left(t \right)})\,dt$
- $\int_{0}^{\frac{2 \pi}{3}}(3 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} - 4 t^{2} \cos^{2}{\left(t \right)} + 3 t \sin^{2}{\left(t \right)} - 4 t \sin{\left(t \right)} \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{2 \pi}{3}}(- t^{2} \left(- \sin^{2}{\left(t \right)} + 2 \sin{\left(t \right)} \cos{\left(t \right)} - 4 \cos^{2}{\left(t \right)}\right) - t \left(3 \sin^{2}{\left(t \right)} - 3 \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right))\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t \cos{\left(t \right)},\,y=t \sin{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(x + y)\,i+(- 4 x + 3 y)\,j \\  & =((t \cos{\left(t \right)}) + (t \sin{\left(t \right)}))\,i+(- 4 (t \cos{\left(t \right)}) + 3 (t \sin{\left(t \right)}))\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(t \cos{\left(t \right)})i+\frac{\mathrm{d}}{\mathrm{d}t}(t \sin{\left(t \right)})j \\  & =(- t \sin{\left(t \right)} + \cos{\left(t \right)})\,i+(t \cos{\left(t \right)} + \sin{\left(t \right)})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((t \sin{\left(t \right)} + t \cos{\left(t \right)})\,i+(3 t \sin{\left(t \right)} - 4 t \cos{\left(t \right)})\,j)\cdot ((- t \sin{\left(t \right)} + \cos{\left(t \right)})\,i+(t \cos{\left(t \right)} + \sin{\left(t \right)})\,j) \\  & =(t \sin{\left(t \right)} + t \cos{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(3 t \sin{\left(t \right)} - 4 t \cos{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)}) \\  & =(t \cos{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(t \sin{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(- 4 t \cos{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)})+(3 t \sin{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)}) \\  & =- t^{2} \sin^{2}{\left(t \right)} + 2 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} - 4 t^{2} \cos^{2}{\left(t \right)} + 3 t \sin^{2}{\left(t \right)} - 3 t \sin{\left(t \right)} \cos{\left(t \right)} + t \cos^{2}{\left(t \right)} \\  & =t^{2} \left(- \sin^{2}{\left(t \right)} + 2 \sin{\left(t \right)} \cos{\left(t \right)} - 4 \cos^{2}{\left(t \right)}\right) + t \left(3 \sin^{2}{\left(t \right)} - 3 \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right).\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{\frac{2 \pi}{3}}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{\frac{2 \pi}{3}}(t^{2} \left(- \sin^{2}{\left(t \right)} + 2 \sin{\left(t \right)} \cos{\left(t \right)} - 4 \cos^{2}{\left(t \right)}\right) + t \left(3 \sin^{2}{\left(t \right)} - 3 \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right))\,dt.\end{aligned}
$$

---

## authored-extension — hard
Template `mixed_spiral`, profile `authored_mixed_spiral`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(- 3 x + 3 y)\,i+(- x - 4 y)\,j$ and $C$ is the path $r(t)=(t \cos{\left(t \right)})\,i+(t \sin{\left(t \right)})\,j$ for $t\in [0,\frac{\pi}{3}]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{\frac{\pi}{3}}(- 3 t^{2} \sin^{2}{\left(t \right)} + 3 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} + 3 t \sin{\left(t \right)} \cos{\left(t \right)} - 3 t \cos^{2}{\left(t \right)})\,dt$
- $\int_{0}^{\frac{\pi}{3}}(t^{2} \left(- 3 \sin^{2}{\left(t \right)} - \sin{\left(t \right)} \cos{\left(t \right)} - \cos^{2}{\left(t \right)}\right) + t \left(- 4 \sin^{2}{\left(t \right)} + 2 \sin{\left(t \right)} \cos{\left(t \right)} - 3 \cos^{2}{\left(t \right)}\right))\,dt$ **Correct**
- $\int_{0}^{\frac{\pi}{3}}(- t \sin{\left(t \right)} - 4 t \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{\pi}{3}}(- 4 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} - t^{2} \cos^{2}{\left(t \right)} - 4 t \sin^{2}{\left(t \right)} - t \sin{\left(t \right)} \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{\pi}{3}}(- t^{2} \left(- 3 \sin^{2}{\left(t \right)} - \sin{\left(t \right)} \cos{\left(t \right)} - \cos^{2}{\left(t \right)}\right) - t \left(- 4 \sin^{2}{\left(t \right)} + 2 \sin{\left(t \right)} \cos{\left(t \right)} - 3 \cos^{2}{\left(t \right)}\right))\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t \cos{\left(t \right)},\,y=t \sin{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- 3 x + 3 y)\,i+(- x - 4 y)\,j \\  & =(- 3 (t \cos{\left(t \right)}) + 3 (t \sin{\left(t \right)}))\,i+(- (t \cos{\left(t \right)}) - 4 (t \sin{\left(t \right)}))\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(t \cos{\left(t \right)})i+\frac{\mathrm{d}}{\mathrm{d}t}(t \sin{\left(t \right)})j \\  & =(- t \sin{\left(t \right)} + \cos{\left(t \right)})\,i+(t \cos{\left(t \right)} + \sin{\left(t \right)})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((3 t \sin{\left(t \right)} - 3 t \cos{\left(t \right)})\,i+(- 4 t \sin{\left(t \right)} - t \cos{\left(t \right)})\,j)\cdot ((- t \sin{\left(t \right)} + \cos{\left(t \right)})\,i+(t \cos{\left(t \right)} + \sin{\left(t \right)})\,j) \\  & =(3 t \sin{\left(t \right)} - 3 t \cos{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(- 4 t \sin{\left(t \right)} - t \cos{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)}) \\  & =(- 3 t \cos{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(3 t \sin{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(- t \cos{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)})+(- 4 t \sin{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)}) \\  & =- 3 t^{2} \sin^{2}{\left(t \right)} - t^{2} \sin{\left(t \right)} \cos{\left(t \right)} - t^{2} \cos^{2}{\left(t \right)} - 4 t \sin^{2}{\left(t \right)} + 2 t \sin{\left(t \right)} \cos{\left(t \right)} - 3 t \cos^{2}{\left(t \right)} \\  & =t^{2} \left(- 3 \sin^{2}{\left(t \right)} - \sin{\left(t \right)} \cos{\left(t \right)} - \cos^{2}{\left(t \right)}\right) + t \left(- 4 \sin^{2}{\left(t \right)} + 2 \sin{\left(t \right)} \cos{\left(t \right)} - 3 \cos^{2}{\left(t \right)}\right).\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{\frac{\pi}{3}}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{\frac{\pi}{3}}(t^{2} \left(- 3 \sin^{2}{\left(t \right)} - \sin{\left(t \right)} \cos{\left(t \right)} - \cos^{2}{\left(t \right)}\right) + t \left(- 4 \sin^{2}{\left(t \right)} + 2 \sin{\left(t \right)} \cos{\left(t \right)} - 3 \cos^{2}{\left(t \right)}\right))\,dt.\end{aligned}
$$

---

## authored-extension — hard
Template `mixed_spiral`, profile `authored_mixed_spiral`; eligible: True.

Which integral is obtained from $\int_C F\cdot\mathrm{d}r$ given that $F(x,y)=(- 2 x + 4 y)\,i+(2 x + 3 y)\,j$ and $C$ is the path $r(t)=(t \cos{\left(t \right)})\,i+(t \sin{\left(t \right)})\,j$ for $t\in [0,\frac{\pi}{3}]$? Use the supplied parameterization and limits to compute $F(r(t))\cdot r'(t)$. Do not evaluate the integral or change variables.

- $\int_{0}^{\frac{\pi}{3}}(- t^{2} \left(- 4 \sin^{2}{\left(t \right)} + 5 \sin{\left(t \right)} \cos{\left(t \right)} + 2 \cos^{2}{\left(t \right)}\right) - t \left(3 \sin^{2}{\left(t \right)} + 6 \sin{\left(t \right)} \cos{\left(t \right)} - 2 \cos^{2}{\left(t \right)}\right))\,dt$
- $\int_{0}^{\frac{\pi}{3}}(3 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} + 2 t^{2} \cos^{2}{\left(t \right)} + 3 t \sin^{2}{\left(t \right)} + 2 t \sin{\left(t \right)} \cos{\left(t \right)})\,dt$
- $\int_{0}^{\frac{\pi}{3}}(t^{2} \left(- 4 \sin^{2}{\left(t \right)} + 5 \sin{\left(t \right)} \cos{\left(t \right)} + 2 \cos^{2}{\left(t \right)}\right) + t \left(3 \sin^{2}{\left(t \right)} + 6 \sin{\left(t \right)} \cos{\left(t \right)} - 2 \cos^{2}{\left(t \right)}\right))\,dt$ **Correct**
- $\int_{0}^{\frac{\pi}{3}}(7 t \sin{\left(t \right)})\,dt$
- $\int_{0}^{\frac{\pi}{3}}(- 4 t^{2} \sin^{2}{\left(t \right)} + 2 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} + 4 t \sin{\left(t \right)} \cos{\left(t \right)} - 2 t \cos^{2}{\left(t \right)})\,dt$

Worked solution

We will use the formula

$$
\int_C F\cdot\mathrm{d}r=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t.
$$

Along the curve $C,$ we have 

$$
x=t \cos{\left(t \right)},\,y=t \sin{\left(t \right)}.
$$

Therefore,

$$
\begin{aligned}F(r(t)) & =(- 2 x + 4 y)\,i+(2 x + 3 y)\,j \\  & =(- 2 (t \cos{\left(t \right)}) + 4 (t \sin{\left(t \right)}))\,i+(2 (t \cos{\left(t \right)}) + 3 (t \sin{\left(t \right)}))\,j.\end{aligned}
$$

Computing $r'(t),$ we get 

$$
\begin{aligned}r^{\prime}(t) & =\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\  & =\frac{\mathrm{d}}{\mathrm{d}t}(t \cos{\left(t \right)})i+\frac{\mathrm{d}}{\mathrm{d}t}(t \sin{\left(t \right)})j \\  & =(- t \sin{\left(t \right)} + \cos{\left(t \right)})\,i+(t \cos{\left(t \right)} + \sin{\left(t \right)})\,j.\end{aligned}
$$

Therefore,

$$
\begin{aligned}F(r(t))\cdot r^{\prime}(t) & =((4 t \sin{\left(t \right)} - 2 t \cos{\left(t \right)})\,i+(3 t \sin{\left(t \right)} + 2 t \cos{\left(t \right)})\,j)\cdot ((- t \sin{\left(t \right)} + \cos{\left(t \right)})\,i+(t \cos{\left(t \right)} + \sin{\left(t \right)})\,j) \\  & =(4 t \sin{\left(t \right)} - 2 t \cos{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(3 t \sin{\left(t \right)} + 2 t \cos{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)}) \\  & =(- 2 t \cos{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(4 t \sin{\left(t \right)})\cdot (- t \sin{\left(t \right)} + \cos{\left(t \right)})+(2 t \cos{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)})+(3 t \sin{\left(t \right)})\cdot (t \cos{\left(t \right)} + \sin{\left(t \right)}) \\  & =- 4 t^{2} \sin^{2}{\left(t \right)} + 5 t^{2} \sin{\left(t \right)} \cos{\left(t \right)} + 2 t^{2} \cos^{2}{\left(t \right)} + 3 t \sin^{2}{\left(t \right)} + 6 t \sin{\left(t \right)} \cos{\left(t \right)} - 2 t \cos^{2}{\left(t \right)} \\  & =t^{2} \left(- 4 \sin^{2}{\left(t \right)} + 5 \sin{\left(t \right)} \cos{\left(t \right)} + 2 \cos^{2}{\left(t \right)}\right) + t \left(3 \sin^{2}{\left(t \right)} + 6 \sin{\left(t \right)} \cos{\left(t \right)} - 2 \cos^{2}{\left(t \right)}\right).\end{aligned}
$$

Finally, we can write the integral as follows:

$$
\begin{aligned}\int_C F(r)\cdot\mathrm{d}r & =\int_{0}^{\frac{\pi}{3}}F(r(t))\cdot r^{\prime}(t)\,\mathrm{d}t \\  & =\int_{0}^{\frac{\pi}{3}}(t^{2} \left(- 4 \sin^{2}{\left(t \right)} + 5 \sin{\left(t \right)} \cos{\left(t \right)} + 2 \cos^{2}{\left(t \right)}\right) + t \left(3 \sin^{2}{\left(t \right)} + 6 \sin{\left(t \right)} \cos{\left(t \right)} - 2 \cos^{2}{\left(t \right)}\right))\,dt.\end{aligned}
$$