### polar_unhinted — hard
Author metadata: authored_cofactor; parameters `{'a': 2, 'b': 3, 'c': 3, 'h': 4, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 2 x,\,3 y,\,3 z\right\rangle,\quad r(u,v)=\left\langle u \cos{\left(v \right)},\,u \sin{\left(v \right)},\,4 u^{2}\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0,\ 0<v<2\pi\}$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

- $40 u^{3} \sin^{2}{\left(v \right)} - 4 u^{3}$
- $- 16 u^{3} \cos{\left(v \right)} - 24 u^{2} v \sin{\left(v \right)} + 3 u$
- $- 8 u^{3} \sin^{2}{\left(v \right)} - 4 u^{3}$ **correct**
- $12 u^{2} + 3 u \sin{\left(v \right)} + 2 u \cos{\left(v \right)}$
- $8 u^{3} \sin^{2}{\left(v \right)} + 4 u^{3}$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}r'_u & =\left\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\right\rangle \\  & =\left\langle \frac{\partial}{\partial u}(u \cos{\left(v \right)}),\,\frac{\partial}{\partial u}(u \sin{\left(v \right)}),\,\frac{\partial}{\partial u}(4 u^{2})\right\rangle \\  & =\left\langle \cos{\left(v \right)},\,\sin{\left(v \right)},\,8 u\right\rangle \\ r'_v & =\left\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\right\rangle \\  & =\left\langle \frac{\partial}{\partial v}(u \cos{\left(v \right)}),\,\frac{\partial}{\partial v}(u \sin{\left(v \right)}),\,\frac{\partial}{\partial v}(4 u^{2})\right\rangle \\  & =\left\langle - u \sin{\left(v \right)},\,u \cos{\left(v \right)},\,0\right\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}r'_u\times r'_v & =\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\\cos{\left(v \right)}&\sin{\left(v \right)}&8 u\\- u \sin{\left(v \right)}&u \cos{\left(v \right)}&0\end{vmatrix} \\  & =\left\langle \begin{vmatrix}\sin{\left(v \right)}&8 u\\u \cos{\left(v \right)}&0\end{vmatrix},-\begin{vmatrix}\cos{\left(v \right)}&8 u\\- u \sin{\left(v \right)}&0\end{vmatrix},\begin{vmatrix}\cos{\left(v \right)}&\sin{\left(v \right)}\\- u \sin{\left(v \right)}&u \cos{\left(v \right)}\end{vmatrix}\right\rangle \\  & =\left\langle - 8 u^{2} \cos{\left(v \right)},\,- 8 u^{2} \sin{\left(v \right)},\,u\right\rangle.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 2 x,\,3 y,\,3 z\right\rangle\big|_{x=u \cos{\left(v \right)},\,y=u \sin{\left(v \right)},\,z=4 u^{2}} \\  & =\left\langle 2 \left(u \cos{\left(v \right)}\right),\,3 \left(u \sin{\left(v \right)}\right),\,3 \left(4 u^{2}\right)\right\rangle \\  & =\left\langle 2 u \cos{\left(v \right)},\,3 u \sin{\left(v \right)},\,12 u^{2}\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 2 u \cos{\left(v \right)},\,3 u \sin{\left(v \right)},\,12 u^{2}\right\rangle\cdot \left\langle - 8 u^{2} \cos{\left(v \right)},\,- 8 u^{2} \sin{\left(v \right)},\,u\right\rangle \\  & =\left(2 u \cos{\left(v \right)}\right)\cdot\left(- 8 u^{2} \cos{\left(v \right)}\right)+\left(3 u \sin{\left(v \right)}\right)\cdot\left(- 8 u^{2} \sin{\left(v \right)}\right)+\left(12 u^{2}\right)\cdot\left(u\right) \\  & =\left(16 u^{3} \sin^{2}{\left(v \right)} - 16 u^{3}\right)+\left(- 24 u^{3} \sin^{2}{\left(v \right)}\right)+\left(12 u^{3}\right) \\  & =- 8 u^{3} \sin^{2}{\left(v \right)} - 4 u^{3}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D - 8 u^{3} \sin^{2}{\left(v \right)} - 4 u^{3}\,\mathrm{d}A.\end{aligned}
$$

---

### exponential_unhinted — hard
Author metadata: authored_cofactor; parameters `{'a': 1, 'b': 3, 'c': 1, 'p': 3, 'q': 4, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle x - \frac{3}{z},\,3 y + \frac{4}{z},\,z\right\rangle,\quad r(u,v)=\left\langle u e^{v},\,u e^{- v},\,u\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0\}$, so the vector field is defined on $S$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

- $- 2 u^{2} - 4 e^{v} + 3 e^{- v}$
- $- 4 u^{2} - 4 e^{v} - 3 e^{- v}$
- $2 u^{2} + 4 e^{v} - 3 e^{- v}$ **correct**
- $u e^{v} + u + 3 u e^{- v} + \frac{1}{u}$
- $u^{2} e^{- v} + 3 u v e^{v} + 4 u e^{v} - 2 u - 3 u e^{- v}$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}r'_u & =\left\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\right\rangle \\  & =\left\langle \frac{\partial}{\partial u}(u e^{v}),\,\frac{\partial}{\partial u}(u e^{- v}),\,\frac{\partial}{\partial u}(u)\right\rangle \\  & =\left\langle e^{v},\,e^{- v},\,1\right\rangle \\ r'_v & =\left\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\right\rangle \\  & =\left\langle \frac{\partial}{\partial v}(u e^{v}),\,\frac{\partial}{\partial v}(u e^{- v}),\,\frac{\partial}{\partial v}(u)\right\rangle \\  & =\left\langle u e^{v},\,- u e^{- v},\,0\right\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}r'_u\times r'_v & =\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\e^{v}&e^{- v}&1\\u e^{v}&- u e^{- v}&0\end{vmatrix} \\  & =\left\langle \begin{vmatrix}e^{- v}&1\\- u e^{- v}&0\end{vmatrix},-\begin{vmatrix}e^{v}&1\\u e^{v}&0\end{vmatrix},\begin{vmatrix}e^{v}&e^{- v}\\u e^{v}&- u e^{- v}\end{vmatrix}\right\rangle \\  & =\left\langle u e^{- v},\,u e^{v},\,- 2 u\right\rangle.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle x - \frac{3}{z},\,3 y + \frac{4}{z},\,z\right\rangle\big|_{x=u e^{v},\,y=u e^{- v},\,z=u} \\  & =\left\langle \left(u e^{v}\right) - \frac{3}{\left(u\right)},\,3 \left(u e^{- v}\right) + \frac{4}{\left(u\right)},\,\left(u\right)\right\rangle \\  & =\left\langle u e^{v} - \frac{3}{u},\,3 u e^{- v} + \frac{4}{u},\,u\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle u e^{v} - \frac{3}{u},\,3 u e^{- v} + \frac{4}{u},\,u\right\rangle\cdot \left\langle u e^{- v},\,u e^{v},\,- 2 u\right\rangle \\  & =\left(u e^{v} - \frac{3}{u}\right)\cdot\left(u e^{- v}\right)+\left(3 u e^{- v} + \frac{4}{u}\right)\cdot\left(u e^{v}\right)+\left(u\right)\cdot\left(- 2 u\right) \\  & =\left(u^{2} - 3 e^{- v}\right)+\left(3 u^{2} + 4 e^{v}\right)+\left(- 2 u^{2}\right) \\  & =2 u^{2} + 4 e^{v} - 3 e^{- v}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 2 u^{2} + 4 e^{v} - 3 e^{- v}\,\mathrm{d}A.\end{aligned}
$$

---

### polar_unhinted — hard
Author metadata: authored_cofactor; parameters `{'a': 3, 'b': 2, 'c': 1, 'h': 3, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 3 x,\,2 y,\,z\right\rangle,\quad r(u,v)=\left\langle u \cos{\left(v \right)},\,u \sin{\left(v \right)},\,3 u^{2}\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0,\ 0<v<2\pi\}$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

- $3 u^{2} + 2 u \sin{\left(v \right)} + 3 u \cos{\left(v \right)}$
- $- 18 u^{3} \cos{\left(v \right)} - 12 u^{2} v \sin{\left(v \right)} + u$
- $- 6 u^{3} \sin^{2}{\left(v \right)} + 15 u^{3}$
- $30 u^{3} \sin^{2}{\left(v \right)} - 15 u^{3}$
- $6 u^{3} \sin^{2}{\left(v \right)} - 15 u^{3}$ **correct**

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}r'_u & =\left\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\right\rangle \\  & =\left\langle \frac{\partial}{\partial u}(u \cos{\left(v \right)}),\,\frac{\partial}{\partial u}(u \sin{\left(v \right)}),\,\frac{\partial}{\partial u}(3 u^{2})\right\rangle \\  & =\left\langle \cos{\left(v \right)},\,\sin{\left(v \right)},\,6 u\right\rangle \\ r'_v & =\left\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\right\rangle \\  & =\left\langle \frac{\partial}{\partial v}(u \cos{\left(v \right)}),\,\frac{\partial}{\partial v}(u \sin{\left(v \right)}),\,\frac{\partial}{\partial v}(3 u^{2})\right\rangle \\  & =\left\langle - u \sin{\left(v \right)},\,u \cos{\left(v \right)},\,0\right\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}r'_u\times r'_v & =\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\\cos{\left(v \right)}&\sin{\left(v \right)}&6 u\\- u \sin{\left(v \right)}&u \cos{\left(v \right)}&0\end{vmatrix} \\  & =\left\langle \begin{vmatrix}\sin{\left(v \right)}&6 u\\u \cos{\left(v \right)}&0\end{vmatrix},-\begin{vmatrix}\cos{\left(v \right)}&6 u\\- u \sin{\left(v \right)}&0\end{vmatrix},\begin{vmatrix}\cos{\left(v \right)}&\sin{\left(v \right)}\\- u \sin{\left(v \right)}&u \cos{\left(v \right)}\end{vmatrix}\right\rangle \\  & =\left\langle - 6 u^{2} \cos{\left(v \right)},\,- 6 u^{2} \sin{\left(v \right)},\,u\right\rangle.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 3 x,\,2 y,\,z\right\rangle\big|_{x=u \cos{\left(v \right)},\,y=u \sin{\left(v \right)},\,z=3 u^{2}} \\  & =\left\langle 3 \left(u \cos{\left(v \right)}\right),\,2 \left(u \sin{\left(v \right)}\right),\,\left(3 u^{2}\right)\right\rangle \\  & =\left\langle 3 u \cos{\left(v \right)},\,2 u \sin{\left(v \right)},\,3 u^{2}\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 3 u \cos{\left(v \right)},\,2 u \sin{\left(v \right)},\,3 u^{2}\right\rangle\cdot \left\langle - 6 u^{2} \cos{\left(v \right)},\,- 6 u^{2} \sin{\left(v \right)},\,u\right\rangle \\  & =\left(3 u \cos{\left(v \right)}\right)\cdot\left(- 6 u^{2} \cos{\left(v \right)}\right)+\left(2 u \sin{\left(v \right)}\right)\cdot\left(- 6 u^{2} \sin{\left(v \right)}\right)+\left(3 u^{2}\right)\cdot\left(u\right) \\  & =\left(18 u^{3} \sin^{2}{\left(v \right)} - 18 u^{3}\right)+\left(- 12 u^{3} \sin^{2}{\left(v \right)}\right)+\left(3 u^{3}\right) \\  & =6 u^{3} \sin^{2}{\left(v \right)} - 15 u^{3}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 6 u^{3} \sin^{2}{\left(v \right)} - 15 u^{3}\,\mathrm{d}A.\end{aligned}
$$

---

### exponential_unhinted — hard
Author metadata: authored_cofactor; parameters `{'a': 4, 'b': 4, 'c': 3, 'p': 1, 'q': 2, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 4 x - \frac{1}{z},\,4 y + \frac{2}{z},\,3 z\right\rangle,\quad r(u,v)=\left\langle u e^{v},\,u e^{- v},\,u\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0\}$, so the vector field is defined on $S$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

- $4 u e^{v} + 3 u + 4 u e^{- v} + \frac{1}{u}$
- $2 u^{2} + 2 e^{v} - e^{- v}$ **correct**
- $- 6 u^{2} - 2 e^{v} - e^{- v}$
- $- 2 u^{2} - 2 e^{v} + e^{- v}$
- $4 u^{2} e^{- v} + 4 u v e^{v} + 2 u e^{v} - 6 u - u e^{- v}$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}r'_u & =\left\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\right\rangle \\  & =\left\langle \frac{\partial}{\partial u}(u e^{v}),\,\frac{\partial}{\partial u}(u e^{- v}),\,\frac{\partial}{\partial u}(u)\right\rangle \\  & =\left\langle e^{v},\,e^{- v},\,1\right\rangle \\ r'_v & =\left\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\right\rangle \\  & =\left\langle \frac{\partial}{\partial v}(u e^{v}),\,\frac{\partial}{\partial v}(u e^{- v}),\,\frac{\partial}{\partial v}(u)\right\rangle \\  & =\left\langle u e^{v},\,- u e^{- v},\,0\right\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}r'_u\times r'_v & =\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\e^{v}&e^{- v}&1\\u e^{v}&- u e^{- v}&0\end{vmatrix} \\  & =\left\langle \begin{vmatrix}e^{- v}&1\\- u e^{- v}&0\end{vmatrix},-\begin{vmatrix}e^{v}&1\\u e^{v}&0\end{vmatrix},\begin{vmatrix}e^{v}&e^{- v}\\u e^{v}&- u e^{- v}\end{vmatrix}\right\rangle \\  & =\left\langle u e^{- v},\,u e^{v},\,- 2 u\right\rangle.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 4 x - \frac{1}{z},\,4 y + \frac{2}{z},\,3 z\right\rangle\big|_{x=u e^{v},\,y=u e^{- v},\,z=u} \\  & =\left\langle 4 \left(u e^{v}\right) - \frac{1}{\left(u\right)},\,4 \left(u e^{- v}\right) + \frac{2}{\left(u\right)},\,3 \left(u\right)\right\rangle \\  & =\left\langle 4 u e^{v} - \frac{1}{u},\,4 u e^{- v} + \frac{2}{u},\,3 u\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 4 u e^{v} - \frac{1}{u},\,4 u e^{- v} + \frac{2}{u},\,3 u\right\rangle\cdot \left\langle u e^{- v},\,u e^{v},\,- 2 u\right\rangle \\  & =\left(4 u e^{v} - \frac{1}{u}\right)\cdot\left(u e^{- v}\right)+\left(4 u e^{- v} + \frac{2}{u}\right)\cdot\left(u e^{v}\right)+\left(3 u\right)\cdot\left(- 2 u\right) \\  & =\left(4 u^{2} - e^{- v}\right)+\left(4 u^{2} + 2 e^{v}\right)+\left(- 6 u^{2}\right) \\  & =2 u^{2} + 2 e^{v} - e^{- v}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 2 u^{2} + 2 e^{v} - e^{- v}\,\mathrm{d}A.\end{aligned}
$$

---

### polar_unhinted — hard
Author metadata: authored_cofactor; parameters `{'a': 3, 'b': 1, 'c': 3, 'h': 2, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 3 x,\,y,\,3 z\right\rangle,\quad r(u,v)=\left\langle u \cos{\left(v \right)},\,u \sin{\left(v \right)},\,2 u^{2}\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0,\ 0<v<2\pi\}$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

- $6 u^{2} + u \sin{\left(v \right)} + 3 u \cos{\left(v \right)}$
- $- 12 u^{3} \cos{\left(v \right)} - 4 u^{2} v \sin{\left(v \right)} + 3 u$
- $- 8 u^{3} \sin^{2}{\left(v \right)} + 6 u^{3}$
- $8 u^{3} \sin^{2}{\left(v \right)} - 6 u^{3}$ **correct**
- $16 u^{3} \sin^{2}{\left(v \right)} - 6 u^{3}$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}r'_u & =\left\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\right\rangle \\  & =\left\langle \frac{\partial}{\partial u}(u \cos{\left(v \right)}),\,\frac{\partial}{\partial u}(u \sin{\left(v \right)}),\,\frac{\partial}{\partial u}(2 u^{2})\right\rangle \\  & =\left\langle \cos{\left(v \right)},\,\sin{\left(v \right)},\,4 u\right\rangle \\ r'_v & =\left\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\right\rangle \\  & =\left\langle \frac{\partial}{\partial v}(u \cos{\left(v \right)}),\,\frac{\partial}{\partial v}(u \sin{\left(v \right)}),\,\frac{\partial}{\partial v}(2 u^{2})\right\rangle \\  & =\left\langle - u \sin{\left(v \right)},\,u \cos{\left(v \right)},\,0\right\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}r'_u\times r'_v & =\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\\cos{\left(v \right)}&\sin{\left(v \right)}&4 u\\- u \sin{\left(v \right)}&u \cos{\left(v \right)}&0\end{vmatrix} \\  & =\left\langle \begin{vmatrix}\sin{\left(v \right)}&4 u\\u \cos{\left(v \right)}&0\end{vmatrix},-\begin{vmatrix}\cos{\left(v \right)}&4 u\\- u \sin{\left(v \right)}&0\end{vmatrix},\begin{vmatrix}\cos{\left(v \right)}&\sin{\left(v \right)}\\- u \sin{\left(v \right)}&u \cos{\left(v \right)}\end{vmatrix}\right\rangle \\  & =\left\langle - 4 u^{2} \cos{\left(v \right)},\,- 4 u^{2} \sin{\left(v \right)},\,u\right\rangle.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 3 x,\,y,\,3 z\right\rangle\big|_{x=u \cos{\left(v \right)},\,y=u \sin{\left(v \right)},\,z=2 u^{2}} \\  & =\left\langle 3 \left(u \cos{\left(v \right)}\right),\,\left(u \sin{\left(v \right)}\right),\,3 \left(2 u^{2}\right)\right\rangle \\  & =\left\langle 3 u \cos{\left(v \right)},\,u \sin{\left(v \right)},\,6 u^{2}\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 3 u \cos{\left(v \right)},\,u \sin{\left(v \right)},\,6 u^{2}\right\rangle\cdot \left\langle - 4 u^{2} \cos{\left(v \right)},\,- 4 u^{2} \sin{\left(v \right)},\,u\right\rangle \\  & =\left(3 u \cos{\left(v \right)}\right)\cdot\left(- 4 u^{2} \cos{\left(v \right)}\right)+\left(u \sin{\left(v \right)}\right)\cdot\left(- 4 u^{2} \sin{\left(v \right)}\right)+\left(6 u^{2}\right)\cdot\left(u\right) \\  & =\left(12 u^{3} \sin^{2}{\left(v \right)} - 12 u^{3}\right)+\left(- 4 u^{3} \sin^{2}{\left(v \right)}\right)+\left(6 u^{3}\right) \\  & =8 u^{3} \sin^{2}{\left(v \right)} - 6 u^{3}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 8 u^{3} \sin^{2}{\left(v \right)} - 6 u^{3}\,\mathrm{d}A.\end{aligned}
$$
