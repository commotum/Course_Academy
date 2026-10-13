# Flux-integral generator review


Author preview. Original questions, full source banks and full solutions follow; generated records are clearly labeled. Legacy math notation is normalized in generated variants. Explicit domain repairs are documented in extraction.


## Original q-160839

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=⟨xz,\,2y,\,1⟩,\,r(u,v)=⟨uv,\,u+v,\,1-v⟩,\,(u,v)\in D⊂{R}^{2}.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}au{v}^{2}+b{v}^{2}+cuv-u+v\,\text{d}A
$$

what is the value of $a+b+c?$


Original complete bank:

- $4$ **correct**

- $2$

- $5$

- $8$

- $3$


Original worked solution:

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(uv),\,\frac{∂}{∂u}(u+v),\,\frac{∂}{∂u}(1-v)⟩ \\  & =⟨v,\,1,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(uv),\,\frac{∂}{∂v}(u+v),\,\frac{∂}{∂v}(1-v)⟩ \\  & =⟨u,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ v & 1 & 0 \\ u & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}1 & 0 \\ 1 & -1\end{aligned}|,\,-|\begin{aligned}v & 0 \\ u & -1\end{aligned}|,\,|\begin{aligned}v & 1 \\ u & 1\end{aligned}|⟩ \\  & =⟨-1,v,v-u⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨xz,\,2y,\,1⟩{|}_{x=uv\,y=u+v\,z=1-v} \\  & =⟨uv\cdot (1-v),\,2(u+v),\,1⟩ \\  & =⟨uv-u{v}^{2},\,2u+2v,\,1⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨uv-u{v}^{2},\,2u+2v,\,1⟩\cdot ⟨-1,\,v,\,v-u⟩ \\  & =(uv-u{v}^{2})\cdot (-1)+(2u+2v)\cdot v+1\cdot (v-u) \\  & =u{v}^{2}-uv+2uv+2{v}^{2}+v-u \\  & =u{v}^{2}+2{v}^{2}+uv-u+v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}1\cdot u{v}^{2}+2\cdot {v}^{2}+1\cdot uv-u+v\,\text{d}A.\end{aligned}
$$

Finally, 

$$
a+b+c=1+2+1=4.
$$


## Parameterized source replay q-160839

### product_affine — moderate
Author metadata: observed; parameters `{'a': 1, 'b': 2, 'c': 1, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle x z,\,2 y,\,1\right\rangle,\quad r(u,v)=\left\langle u v,\,u + v,\,1 - v\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D a u v^{2} + b v^{2} + c u v - u + v\,\mathrm{d}A
$$

what is the value of $a+b+c?$

- $5$
- $2$
- $4$ **correct**
- $3$
- $8$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}r'_u & =\left\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\right\rangle \\  & =\left\langle \frac{\partial}{\partial u}(u v),\,\frac{\partial}{\partial u}(u + v),\,\frac{\partial}{\partial u}(1 - v)\right\rangle \\  & =\left\langle v,\,1,\,0\right\rangle \\ r'_v & =\left\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\right\rangle \\  & =\left\langle \frac{\partial}{\partial v}(u v),\,\frac{\partial}{\partial v}(u + v),\,\frac{\partial}{\partial v}(1 - v)\right\rangle \\  & =\left\langle u,\,1,\,-1\right\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}r'_u\times r'_v & =\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\v&1&0\\u&1&-1\end{vmatrix} \\  & =\left\langle \begin{vmatrix}1&0\\1&-1\end{vmatrix},-\begin{vmatrix}v&0\\u&-1\end{vmatrix},\begin{vmatrix}v&1\\u&1\end{vmatrix}\right\rangle \\  & =\left\langle -1,\,v,\,- u + v\right\rangle.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle x z,\,2 y,\,1\right\rangle\big|_{x=u v,\,y=u + v,\,z=1 - v} \\  & =\left\langle \left(u v\right) \left(1 - v\right),\,2 \left(u + v\right),\,1\right\rangle \\  & =\left\langle - u v^{2} + u v,\,2 u + 2 v,\,1\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle - u v^{2} + u v,\,2 u + 2 v,\,1\right\rangle\cdot \left\langle -1,\,v,\,- u + v\right\rangle \\  & =\left(- u v^{2} + u v\right)\cdot\left(-1\right)+\left(2 u + 2 v\right)\cdot\left(v\right)+\left(1\right)\cdot\left(- u + v\right) \\  & =\left(u v^{2} - u v\right)+\left(2 u v + 2 v^{2}\right)+\left(- u + v\right) \\  & =u v^{2} + u v - u + 2 v^{2} + v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D u v^{2} + u v - u + 2 v^{2} + v\,\mathrm{d}A.\end{aligned}
$$

Finally, 

$$
a+b+c=(1)+(2)+(1)=4.
$$


## Generated observed-pattern bank variation q-160839

### product_affine — moderate
Author metadata: observed; parameters `{'a': 1, 'b': 2, 'c': 1, 'scale': 2}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 2 x z,\,4 y,\,2\right\rangle,\quad r(u,v)=\left\langle u v,\,u + v,\,1 - v\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D a u v^{2} + b v^{2} + c u v - 2 u + 2 v\,\mathrm{d}A
$$

what is the value of $a+b+c?$

- $10$
- $4$
- $8$ **correct**
- $6$
- $16$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}r'_u & =\left\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\right\rangle \\  & =\left\langle \frac{\partial}{\partial u}(u v),\,\frac{\partial}{\partial u}(u + v),\,\frac{\partial}{\partial u}(1 - v)\right\rangle \\  & =\left\langle v,\,1,\,0\right\rangle \\ r'_v & =\left\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\right\rangle \\  & =\left\langle \frac{\partial}{\partial v}(u v),\,\frac{\partial}{\partial v}(u + v),\,\frac{\partial}{\partial v}(1 - v)\right\rangle \\  & =\left\langle u,\,1,\,-1\right\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}r'_u\times r'_v & =\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\v&1&0\\u&1&-1\end{vmatrix} \\  & =\left\langle \begin{vmatrix}1&0\\1&-1\end{vmatrix},-\begin{vmatrix}v&0\\u&-1\end{vmatrix},\begin{vmatrix}v&1\\u&1\end{vmatrix}\right\rangle \\  & =\left\langle -1,\,v,\,- u + v\right\rangle.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 2 x z,\,4 y,\,2\right\rangle\big|_{x=u v,\,y=u + v,\,z=1 - v} \\  & =\left\langle 2 \left(u v\right) \left(1 - v\right),\,4 \left(u + v\right),\,2\right\rangle \\  & =\left\langle - 2 u v^{2} + 2 u v,\,4 u + 4 v,\,2\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle - 2 u v^{2} + 2 u v,\,4 u + 4 v,\,2\right\rangle\cdot \left\langle -1,\,v,\,- u + v\right\rangle \\  & =\left(- 2 u v^{2} + 2 u v\right)\cdot\left(-1\right)+\left(4 u + 4 v\right)\cdot\left(v\right)+\left(2\right)\cdot\left(- u + v\right) \\  & =\left(2 u v^{2} - 2 u v\right)+\left(4 u v + 4 v^{2}\right)+\left(- 2 u + 2 v\right) \\  & =2 u v^{2} + 2 u v - 2 u + 4 v^{2} + 2 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 2 u v^{2} + 2 u v - 2 u + 4 v^{2} + 2 v\,\mathrm{d}A.\end{aligned}
$$

Finally, 

$$
a+b+c=(2)+(4)+(2)=8.
$$


## Generated authored-default variant q-160839

### product_affine — moderate
Author metadata: authored_tangents; parameters `{'a': 3, 'b': 2, 'c': 1, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 3 x z,\,2 y,\,1\right\rangle,\quad r(u,v)=\left\langle u v,\,u + v,\,1 - v\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D a u v^{2} + b v^{2} + c u v - u + v\,\mathrm{d}A
$$

what is the value of $a+b+c?$

- $3$
- $4$ **correct**
- $-4$
- $2$
- $0$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}r'_u & =\left\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\right\rangle \\  & =\left\langle \frac{\partial}{\partial u}(u v),\,\frac{\partial}{\partial u}(u + v),\,\frac{\partial}{\partial u}(1 - v)\right\rangle \\  & =\left\langle v,\,1,\,0\right\rangle \\ r'_v & =\left\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\right\rangle \\  & =\left\langle \frac{\partial}{\partial v}(u v),\,\frac{\partial}{\partial v}(u + v),\,\frac{\partial}{\partial v}(1 - v)\right\rangle \\  & =\left\langle u,\,1,\,-1\right\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}r'_u\times r'_v & =\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\v&1&0\\u&1&-1\end{vmatrix} \\  & =\left\langle \begin{vmatrix}1&0\\1&-1\end{vmatrix},-\begin{vmatrix}v&0\\u&-1\end{vmatrix},\begin{vmatrix}v&1\\u&1\end{vmatrix}\right\rangle \\  & =\left\langle -1,\,v,\,- u + v\right\rangle.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 3 x z,\,2 y,\,1\right\rangle\big|_{x=u v,\,y=u + v,\,z=1 - v} \\  & =\left\langle 3 \left(u v\right) \left(1 - v\right),\,2 \left(u + v\right),\,1\right\rangle \\  & =\left\langle - 3 u v^{2} + 3 u v,\,2 u + 2 v,\,1\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle - 3 u v^{2} + 3 u v,\,2 u + 2 v,\,1\right\rangle\cdot \left\langle -1,\,v,\,- u + v\right\rangle \\  & =\left(- 3 u v^{2} + 3 u v\right)\cdot\left(-1\right)+\left(2 u + 2 v\right)\cdot\left(v\right)+\left(1\right)\cdot\left(- u + v\right) \\  & =\left(3 u v^{2} - 3 u v\right)+\left(2 u v + 2 v^{2}\right)+\left(- u + v\right) \\  & =3 u v^{2} - u v - u + 2 v^{2} + v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 3 u v^{2} - u v - u + 2 v^{2} + v\,\mathrm{d}A.\end{aligned}
$$

Finally, 

$$
a+b+c=(3)+(2)+(-1)=4.
$$


## Generated authored-default variant q-160839

### product_affine — moderate
Author metadata: authored_tangents; parameters `{'a': 1, 'b': 3, 'c': 3, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle x z,\,3 y,\,3\right\rangle,\quad r(u,v)=\left\langle u v,\,u + v,\,1 - v\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D a u v^{2} + b v^{2} + c u v - 3 u + 3 v\,\mathrm{d}A
$$

what is the value of $a+b+c?$

- $0$
- $1$
- $-6$
- $6$ **correct**
- $3$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}r'_u & =\left\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\right\rangle \\  & =\left\langle \frac{\partial}{\partial u}(u v),\,\frac{\partial}{\partial u}(u + v),\,\frac{\partial}{\partial u}(1 - v)\right\rangle \\  & =\left\langle v,\,1,\,0\right\rangle \\ r'_v & =\left\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\right\rangle \\  & =\left\langle \frac{\partial}{\partial v}(u v),\,\frac{\partial}{\partial v}(u + v),\,\frac{\partial}{\partial v}(1 - v)\right\rangle \\  & =\left\langle u,\,1,\,-1\right\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}r'_u\times r'_v & =\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\v&1&0\\u&1&-1\end{vmatrix} \\  & =\left\langle \begin{vmatrix}1&0\\1&-1\end{vmatrix},-\begin{vmatrix}v&0\\u&-1\end{vmatrix},\begin{vmatrix}v&1\\u&1\end{vmatrix}\right\rangle \\  & =\left\langle -1,\,v,\,- u + v\right\rangle.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle x z,\,3 y,\,3\right\rangle\big|_{x=u v,\,y=u + v,\,z=1 - v} \\  & =\left\langle \left(u v\right) \left(1 - v\right),\,3 \left(u + v\right),\,3\right\rangle \\  & =\left\langle - u v^{2} + u v,\,3 u + 3 v,\,3\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle - u v^{2} + u v,\,3 u + 3 v,\,3\right\rangle\cdot \left\langle -1,\,v,\,- u + v\right\rangle \\  & =\left(- u v^{2} + u v\right)\cdot\left(-1\right)+\left(3 u + 3 v\right)\cdot\left(v\right)+\left(3\right)\cdot\left(- u + v\right) \\  & =\left(u v^{2} - u v\right)+\left(3 u v + 3 v^{2}\right)+\left(- 3 u + 3 v\right) \\  & =u v^{2} + 2 u v - 3 u + 3 v^{2} + 3 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D u v^{2} + 2 u v - 3 u + 3 v^{2} + 3 v\,\mathrm{d}A.\end{aligned}
$$

Finally, 

$$
a+b+c=(1)+(3)+(2)=6.
$$


## Original q-160840

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=⟨2x+y,\,2z,\,y+z⟩,\,r(u,v)=⟨-{u}^{2},\,2{u}^{2}-{v}^{2},\,{v}^{2}⟩,\,(u,v)\in D⊂{R}^{2}.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

what is the missing expression?

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨8uv,\,4uv,\,4uv⟩.$*


Original complete bank:

- $8u{v}^{3}+8{u}^{3}v$

- $8u{v}^{3}$

- $2u{v}^{3}+4{u}^{3}v$

- $4u{v}^{3}+2{u}^{3}v$

- $8{u}^{3}v$ **correct**


Original worked solution:

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨8uv,\,4uv,\,4uv⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2x+y,\,2z,\,y+z⟩{|}_{x=-{u}^{2}\,y=2{u}^{2}-{v}^{2}\,z={v}^{2}} \\  & =⟨2(-{u}^{2})+(2{u}^{2}-{v}^{2}),\,2({v}^{2}),\,(2{u}^{2}-{v}^{2})+{v}^{2}⟩ \\  & =⟨-{v}^{2},\,2{v}^{2},\,2{u}^{2}⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨-{v}^{2},\,2{v}^{2},\,2{u}^{2}⟩\cdot ⟨8uv,\,4uv,\,4uv⟩ \\  & =(-{v}^{2})\cdot 8uv+2{v}^{2}\cdot 4uv+2{u}^{2}\cdot 4uv \\  & =-8u{v}^{3}+8u{v}^{3}+8{u}^{3}v \\  & =8{u}^{3}v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}\,8{u}^{3}v\,\text{d}A.\end{aligned}
$$


## Parameterized source replay q-160840

### quadratic_cancel — easy
Author metadata: observed; parameters `{'a': 2, 'b': 1, 'c': 2, 'd': 1, 'e': 1, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 2 x + y,\,2 z,\,y + z\right\rangle,\quad r(u,v)=\left\langle - u^{2},\,2 u^{2} - v^{2},\,v^{2}\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0,\ v>0\}$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

*Hint: You can use the fact that $r'_u\times r'_v=\left\langle 8 u v,\,4 u v,\,4 u v\right\rangle.$*

- $4 u^{3} v + 2 u v^{3}$
- $8 u v^{3}$
- $8 u^{3} v + 8 u v^{3}$
- $8 u^{3} v$ **correct**
- $2 u^{3} v + 4 u v^{3}$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
r'_u\times r'_v=\left\langle 8 u v,\,4 u v,\,4 u v\right\rangle.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 2 x + y,\,2 z,\,y + z\right\rangle\big|_{x=- u^{2},\,y=2 u^{2} - v^{2},\,z=v^{2}} \\  & =\left\langle 2 \left(- u^{2}\right) + \left(2 u^{2} - v^{2}\right),\,2 \left(v^{2}\right),\,\left(2 u^{2} - v^{2}\right) + \left(v^{2}\right)\right\rangle \\  & =\left\langle - v^{2},\,2 v^{2},\,2 u^{2}\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle - v^{2},\,2 v^{2},\,2 u^{2}\right\rangle\cdot \left\langle 8 u v,\,4 u v,\,4 u v\right\rangle \\  & =\left(- v^{2}\right)\cdot\left(8 u v\right)+\left(2 v^{2}\right)\cdot\left(4 u v\right)+\left(2 u^{2}\right)\cdot\left(4 u v\right) \\  & =\left(- 8 u v^{3}\right)+\left(8 u v^{3}\right)+\left(8 u^{3} v\right) \\  & =8 u^{3} v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 8 u^{3} v\,\mathrm{d}A.\end{aligned}
$$


## Generated observed-pattern bank variation q-160840

### quadratic_cancel — easy
Author metadata: observed; parameters `{'a': 2, 'b': 1, 'c': 2, 'd': 1, 'e': 1, 'scale': 2}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 4 x + 2 y,\,4 z,\,2 y + 2 z\right\rangle,\quad r(u,v)=\left\langle - u^{2},\,2 u^{2} - v^{2},\,v^{2}\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0,\ v>0\}$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

*Hint: You can use the fact that $r'_u\times r'_v=\left\langle 8 u v,\,4 u v,\,4 u v\right\rangle.$*

- $8 u^{3} v + 4 u v^{3}$
- $16 u v^{3}$
- $16 u^{3} v + 16 u v^{3}$
- $16 u^{3} v$ **correct**
- $4 u^{3} v + 8 u v^{3}$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
r'_u\times r'_v=\left\langle 8 u v,\,4 u v,\,4 u v\right\rangle.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 4 x + 2 y,\,4 z,\,2 y + 2 z\right\rangle\big|_{x=- u^{2},\,y=2 u^{2} - v^{2},\,z=v^{2}} \\  & =\left\langle 4 \left(- u^{2}\right) + 2 \left(2 u^{2} - v^{2}\right),\,4 \left(v^{2}\right),\,2 \left(2 u^{2} - v^{2}\right) + 2 \left(v^{2}\right)\right\rangle \\  & =\left\langle - 2 v^{2},\,4 v^{2},\,4 u^{2}\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle - 2 v^{2},\,4 v^{2},\,4 u^{2}\right\rangle\cdot \left\langle 8 u v,\,4 u v,\,4 u v\right\rangle \\  & =\left(- 2 v^{2}\right)\cdot\left(8 u v\right)+\left(4 v^{2}\right)\cdot\left(4 u v\right)+\left(4 u^{2}\right)\cdot\left(4 u v\right) \\  & =\left(- 16 u v^{3}\right)+\left(16 u v^{3}\right)+\left(16 u^{3} v\right) \\  & =16 u^{3} v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 16 u^{3} v\,\mathrm{d}A.\end{aligned}
$$


## Generated authored-default variant q-160840

### quadratic_cancel — easy
Author metadata: authored_cofactor; parameters `{'a': 4, 'b': 4, 'c': 4, 'd': 2, 'e': 2, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 4 x + 4 y,\,4 z,\,2 y + 2 z\right\rangle,\quad r(u,v)=\left\langle - u^{2},\,2 u^{2} - v^{2},\,v^{2}\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0,\ v>0\}$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

*Hint: You can use the fact that $r'_u\times r'_v=\left\langle 8 u v,\,4 u v,\,4 u v\right\rangle.$*

- $48 u^{3} v - 48 u v^{3}$
- $48 u^{3} v - 16 u v^{3}$ **correct**
- $- 48 u^{3} v + 16 u v^{3}$
- $8 u^{2}$
- $32 u^{2} v + 40 u v^{2} + 24 u v$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
r'_u\times r'_v=\left\langle 8 u v,\,4 u v,\,4 u v\right\rangle.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 4 x + 4 y,\,4 z,\,2 y + 2 z\right\rangle\big|_{x=- u^{2},\,y=2 u^{2} - v^{2},\,z=v^{2}} \\  & =\left\langle 4 \left(- u^{2}\right) + 4 \left(2 u^{2} - v^{2}\right),\,4 \left(v^{2}\right),\,2 \left(2 u^{2} - v^{2}\right) + 2 \left(v^{2}\right)\right\rangle \\  & =\left\langle 4 u^{2} - 4 v^{2},\,4 v^{2},\,4 u^{2}\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 4 u^{2} - 4 v^{2},\,4 v^{2},\,4 u^{2}\right\rangle\cdot \left\langle 8 u v,\,4 u v,\,4 u v\right\rangle \\  & =\left(4 u^{2} - 4 v^{2}\right)\cdot\left(8 u v\right)+\left(4 v^{2}\right)\cdot\left(4 u v\right)+\left(4 u^{2}\right)\cdot\left(4 u v\right) \\  & =\left(32 u^{3} v - 32 u v^{3}\right)+\left(16 u v^{3}\right)+\left(16 u^{3} v\right) \\  & =48 u^{3} v - 16 u v^{3}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 48 u^{3} v - 16 u v^{3}\,\mathrm{d}A.\end{aligned}
$$


## Generated authored-default variant q-160840

### quadratic_cancel — easy
Author metadata: authored_cofactor; parameters `{'a': 1, 'b': 3, 'c': 3, 'd': 1, 'e': 3, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle x + 3 y,\,3 z,\,y + 3 z\right\rangle,\quad r(u,v)=\left\langle - u^{2},\,2 u^{2} - v^{2},\,v^{2}\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0,\ v>0\}$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

*Hint: You can use the fact that $r'_u\times r'_v=\left\langle 8 u v,\,4 u v,\,4 u v\right\rangle.$*

- $8 u^{2} v + 28 u v^{2} + 24 u v$
- $48 u^{3} v - 28 u v^{3}$
- $- 48 u^{3} v + 4 u v^{3}$
- $48 u^{3} v - 4 u v^{3}$ **correct**
- $7 u^{2} + 2 v^{2}$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
r'_u\times r'_v=\left\langle 8 u v,\,4 u v,\,4 u v\right\rangle.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle x + 3 y,\,3 z,\,y + 3 z\right\rangle\big|_{x=- u^{2},\,y=2 u^{2} - v^{2},\,z=v^{2}} \\  & =\left\langle \left(- u^{2}\right) + 3 \left(2 u^{2} - v^{2}\right),\,3 \left(v^{2}\right),\,\left(2 u^{2} - v^{2}\right) + 3 \left(v^{2}\right)\right\rangle \\  & =\left\langle 5 u^{2} - 3 v^{2},\,3 v^{2},\,2 u^{2} + 2 v^{2}\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 5 u^{2} - 3 v^{2},\,3 v^{2},\,2 u^{2} + 2 v^{2}\right\rangle\cdot \left\langle 8 u v,\,4 u v,\,4 u v\right\rangle \\  & =\left(5 u^{2} - 3 v^{2}\right)\cdot\left(8 u v\right)+\left(3 v^{2}\right)\cdot\left(4 u v\right)+\left(2 u^{2} + 2 v^{2}\right)\cdot\left(4 u v\right) \\  & =\left(40 u^{3} v - 24 u v^{3}\right)+\left(12 u v^{3}\right)+\left(8 u^{3} v + 8 u v^{3}\right) \\  & =48 u^{3} v - 4 u v^{3}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 48 u^{3} v - 4 u v^{3}\,\mathrm{d}A.\end{aligned}
$$


## Original q-161249

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=⟨2x,\,2y,\,z⟩,\,r(u,v)=⟨{u}^{2},\,-uv,\,{v}^{2}⟩,\,(u,v)\in D⊂{R}^{2}.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

what is the missing expression?

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨-2{v}^{2},\,-4uv,\,-2{u}^{2}⟩.$*


Original complete bank:

- $2{u}^{2}{v}^{2}$ **correct**

- ${u}^{3}v+u{v}^{3}$

- $-2{u}^{3}v-2u{v}^{3}$

- $6{u}^{2}{v}^{2}$

- ${u}^{2}v-2{u}^{2}{v}^{2}+u{v}^{2}$


Original worked solution:

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨-2{v}^{2},\,-4uv,\,-2{u}^{2}⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2x,\,2y,\,z⟩{|}_{x={u}^{2}\,y=-uv\,z={v}^{2}} \\  & =⟨2{u}^{2},\,-2uv,\,{v}^{2}⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2{u}^{2},\,-2uv,\,{v}^{2}⟩\cdot ⟨-2{v}^{2},\,-4uv,\,-2{u}^{2}⟩ \\  & =2{u}^{2}\cdot (-2{v}^{2})+(-2uv)\cdot (-4uv)+{v}^{2}\cdot (-2{u}^{2}) \\  & =-4{u}^{2}{v}^{2}+8{u}^{2}{v}^{2}-2{u}^{2}{v}^{2} \\  & =2{u}^{2}{v}^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}\,2{u}^{2}{v}^{2}\,\text{d}A.\end{aligned}
$$


## Parameterized source replay q-161249

### quadratic_diagonal — easy
Author metadata: observed; parameters `{'a': 2, 'b': 2, 'c': 1, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 2 x,\,2 y,\,z\right\rangle,\quad r(u,v)=\left\langle u^{2},\,- u v,\,v^{2}\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0,\ v>0\}$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

*Hint: You can use the fact that $r'_u\times r'_v=\left\langle - 2 v^{2},\,- 4 u v,\,- 2 u^{2}\right\rangle.$*

- $- 2 u^{3} v - 2 u v^{3}$
- $u^{3} v + u v^{3}$
- $2 u^{2} v^{2}$ **correct**
- $- 2 u^{2} v^{2} + u^{2} v + u v^{2}$
- $6 u^{2} v^{2}$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
r'_u\times r'_v=\left\langle - 2 v^{2},\,- 4 u v,\,- 2 u^{2}\right\rangle.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 2 x,\,2 y,\,z\right\rangle\big|_{x=u^{2},\,y=- u v,\,z=v^{2}} \\  & =\left\langle 2 \left(u^{2}\right),\,2 \left(- u v\right),\,\left(v^{2}\right)\right\rangle \\  & =\left\langle 2 u^{2},\,- 2 u v,\,v^{2}\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 2 u^{2},\,- 2 u v,\,v^{2}\right\rangle\cdot \left\langle - 2 v^{2},\,- 4 u v,\,- 2 u^{2}\right\rangle \\  & =\left(2 u^{2}\right)\cdot\left(- 2 v^{2}\right)+\left(- 2 u v\right)\cdot\left(- 4 u v\right)+\left(v^{2}\right)\cdot\left(- 2 u^{2}\right) \\  & =\left(- 4 u^{2} v^{2}\right)+\left(8 u^{2} v^{2}\right)+\left(- 2 u^{2} v^{2}\right) \\  & =2 u^{2} v^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 2 u^{2} v^{2}\,\mathrm{d}A.\end{aligned}
$$


## Generated observed-pattern bank variation q-161249

### quadratic_diagonal — easy
Author metadata: observed; parameters `{'a': 2, 'b': 2, 'c': 1, 'scale': 2}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 4 x,\,4 y,\,2 z\right\rangle,\quad r(u,v)=\left\langle u^{2},\,- u v,\,v^{2}\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0,\ v>0\}$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

*Hint: You can use the fact that $r'_u\times r'_v=\left\langle - 2 v^{2},\,- 4 u v,\,- 2 u^{2}\right\rangle.$*

- $- 4 u^{3} v - 4 u v^{3}$
- $2 u^{3} v + 2 u v^{3}$
- $4 u^{2} v^{2}$ **correct**
- $- 4 u^{2} v^{2} + 2 u^{2} v + 2 u v^{2}$
- $12 u^{2} v^{2}$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
r'_u\times r'_v=\left\langle - 2 v^{2},\,- 4 u v,\,- 2 u^{2}\right\rangle.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 4 x,\,4 y,\,2 z\right\rangle\big|_{x=u^{2},\,y=- u v,\,z=v^{2}} \\  & =\left\langle 4 \left(u^{2}\right),\,4 \left(- u v\right),\,2 \left(v^{2}\right)\right\rangle \\  & =\left\langle 4 u^{2},\,- 4 u v,\,2 v^{2}\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 4 u^{2},\,- 4 u v,\,2 v^{2}\right\rangle\cdot \left\langle - 2 v^{2},\,- 4 u v,\,- 2 u^{2}\right\rangle \\  & =\left(4 u^{2}\right)\cdot\left(- 2 v^{2}\right)+\left(- 4 u v\right)\cdot\left(- 4 u v\right)+\left(2 v^{2}\right)\cdot\left(- 2 u^{2}\right) \\  & =\left(- 8 u^{2} v^{2}\right)+\left(16 u^{2} v^{2}\right)+\left(- 4 u^{2} v^{2}\right) \\  & =4 u^{2} v^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 4 u^{2} v^{2}\,\mathrm{d}A.\end{aligned}
$$


## Generated authored-default variant q-161249

### quadratic_diagonal — easy
Author metadata: authored_cofactor; parameters `{'a': 2, 'b': 2, 'c': 4, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 2 x,\,2 y,\,4 z\right\rangle,\quad r(u,v)=\left\langle u^{2},\,- u v,\,v^{2}\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0,\ v>0\}$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

*Hint: You can use the fact that $r'_u\times r'_v=\left\langle - 2 v^{2},\,- 4 u v,\,- 2 u^{2}\right\rangle.$*

- $- 20 u^{2} v^{2}$
- $- 4 u^{2} v^{2}$ **correct**
- $4 u^{2} v^{2}$
- $2 u^{2} - 2 u v + 4 v^{2}$
- $- 8 u^{2} - 12 u v^{2}$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
r'_u\times r'_v=\left\langle - 2 v^{2},\,- 4 u v,\,- 2 u^{2}\right\rangle.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 2 x,\,2 y,\,4 z\right\rangle\big|_{x=u^{2},\,y=- u v,\,z=v^{2}} \\  & =\left\langle 2 \left(u^{2}\right),\,2 \left(- u v\right),\,4 \left(v^{2}\right)\right\rangle \\  & =\left\langle 2 u^{2},\,- 2 u v,\,4 v^{2}\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 2 u^{2},\,- 2 u v,\,4 v^{2}\right\rangle\cdot \left\langle - 2 v^{2},\,- 4 u v,\,- 2 u^{2}\right\rangle \\  & =\left(2 u^{2}\right)\cdot\left(- 2 v^{2}\right)+\left(- 2 u v\right)\cdot\left(- 4 u v\right)+\left(4 v^{2}\right)\cdot\left(- 2 u^{2}\right) \\  & =\left(- 4 u^{2} v^{2}\right)+\left(8 u^{2} v^{2}\right)+\left(- 8 u^{2} v^{2}\right) \\  & =- 4 u^{2} v^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D - 4 u^{2} v^{2}\,\mathrm{d}A.\end{aligned}
$$


## Generated authored-default variant q-161249

### quadratic_diagonal — easy
Author metadata: authored_cofactor; parameters `{'a': 1, 'b': 3, 'c': 3, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle x,\,3 y,\,3 z\right\rangle,\quad r(u,v)=\left\langle u^{2},\,- u v,\,v^{2}\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0,\ v>0\}$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

*Hint: You can use the fact that $r'_u\times r'_v=\left\langle - 2 v^{2},\,- 4 u v,\,- 2 u^{2}\right\rangle.$*

- $- 6 u^{2} - 14 u v^{2}$
- $- 20 u^{2} v^{2}$
- $- 4 u^{2} v^{2}$
- $4 u^{2} v^{2}$ **correct**
- $u^{2} - 3 u v + 3 v^{2}$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
r'_u\times r'_v=\left\langle - 2 v^{2},\,- 4 u v,\,- 2 u^{2}\right\rangle.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle x,\,3 y,\,3 z\right\rangle\big|_{x=u^{2},\,y=- u v,\,z=v^{2}} \\  & =\left\langle \left(u^{2}\right),\,3 \left(- u v\right),\,3 \left(v^{2}\right)\right\rangle \\  & =\left\langle u^{2},\,- 3 u v,\,3 v^{2}\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle u^{2},\,- 3 u v,\,3 v^{2}\right\rangle\cdot \left\langle - 2 v^{2},\,- 4 u v,\,- 2 u^{2}\right\rangle \\  & =\left(u^{2}\right)\cdot\left(- 2 v^{2}\right)+\left(- 3 u v\right)\cdot\left(- 4 u v\right)+\left(3 v^{2}\right)\cdot\left(- 2 u^{2}\right) \\  & =\left(- 2 u^{2} v^{2}\right)+\left(12 u^{2} v^{2}\right)+\left(- 6 u^{2} v^{2}\right) \\  & =4 u^{2} v^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 4 u^{2} v^{2}\,\mathrm{d}A.\end{aligned}
$$


## Original q-161303

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=⟨1,\,0,\,2⟩,\,r(u,v)=⟨u+v,\,{u}^{2}+2v,\,{u}^{3}+3v⟩,\,(u,v)\in D⊂{R}^{2}.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}a{u}^{2}+bu+c\,\text{d}A
$$

what is the value of $a+b+c?$


Original complete bank:

- $4$

- $-2$

- $0$ **correct**

- $-4$

- $2$


Original worked solution:

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u+v),\,\frac{∂}{∂u}({u}^{2}+2v),\,\frac{∂}{∂u}({u}^{3}+3v)⟩ \\  & =⟨1,\,2u,\,3{u}^{2}⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u+v),\,\frac{∂}{∂v}({u}^{2}+2v),\,\frac{∂}{∂v}({u}^{3}+3v)⟩ \\  & =⟨1,\,2,\,3⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 2u & 3{u}^{2} \\ 1 & 2 & 3\end{aligned}| \\  & =⟨|\begin{aligned}2u & 3{u}^{2} \\ 2 & 3\end{aligned}|,\,-|\begin{aligned}1 & 3{u}^{2} \\ 1 & 3\end{aligned}|,\,|\begin{aligned}1 & 2u \\ 1 & 2\end{aligned}|⟩ \\  & =⟨6u-6{u}^{2},\,3{u}^{2}-3,\,2-2u⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨1,\,0,\,2⟩{|}_{x=u+v\,y={u}^{2}+2v\,z={u}^{3}+3v} \\  & =⟨1,\,0,\,2⟩.\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨1,\,0,\,2⟩\cdot ⟨6u-6{u}^{2},\,3{u}^{2}-3,\,2-2u⟩ \\  & =1\cdot (6u-6{u}^{2})+0\cdot (3{u}^{2}-3)+2\cdot (2-2u) \\  & =6u-6{u}^{2}+4-4u \\  & =-6{u}^{2}+2u+4.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-6)\cdot {u}^{2}+2\cdot u+4\,\text{d}A.\end{aligned}
$$

Finally, 

$$
a+b+c=-6+2+4=0.
$$


## Parameterized source replay q-161303

### cubic_ruled — moderate
Author metadata: observed; parameters `{'a': 1, 'b': 2, 'c': 2, 'd': 3, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 1,\,0,\,2\right\rangle,\quad r(u,v)=\left\langle u + v,\,u^{2} + 2 v,\,u^{3} + 3 v\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D$ excludes $u=1$, where the parametrization is singular.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D a u^{2} + b u + c\,\mathrm{d}A
$$

what is the value of $a+b+c?$

- $0$ **correct**
- $-2$
- $4$
- $2$
- $-4$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}r'_u & =\left\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\right\rangle \\  & =\left\langle \frac{\partial}{\partial u}(u + v),\,\frac{\partial}{\partial u}(u^{2} + 2 v),\,\frac{\partial}{\partial u}(u^{3} + 3 v)\right\rangle \\  & =\left\langle 1,\,2 u,\,3 u^{2}\right\rangle \\ r'_v & =\left\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\right\rangle \\  & =\left\langle \frac{\partial}{\partial v}(u + v),\,\frac{\partial}{\partial v}(u^{2} + 2 v),\,\frac{\partial}{\partial v}(u^{3} + 3 v)\right\rangle \\  & =\left\langle 1,\,2,\,3\right\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}r'_u\times r'_v & =\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\1&2 u&3 u^{2}\\1&2&3\end{vmatrix} \\  & =\left\langle \begin{vmatrix}2 u&3 u^{2}\\2&3\end{vmatrix},-\begin{vmatrix}1&3 u^{2}\\1&3\end{vmatrix},\begin{vmatrix}1&2 u\\1&2\end{vmatrix}\right\rangle \\  & =\left\langle - 6 u^{2} + 6 u,\,3 u^{2} - 3,\,2 - 2 u\right\rangle.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 1,\,0,\,2\right\rangle\big|_{x=u + v,\,y=u^{2} + 2 v,\,z=u^{3} + 3 v} \\  & =\left\langle 1,\,0,\,2\right\rangle \\  & =\left\langle 1,\,0,\,2\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 1,\,0,\,2\right\rangle\cdot \left\langle - 6 u^{2} + 6 u,\,3 u^{2} - 3,\,2 - 2 u\right\rangle \\  & =\left(1\right)\cdot\left(- 6 u^{2} + 6 u\right)+\left(0\right)\cdot\left(3 u^{2} - 3\right)+\left(2\right)\cdot\left(2 - 2 u\right) \\  & =\left(- 6 u^{2} + 6 u\right)+\left(0\right)+\left(4 - 4 u\right) \\  & =- 6 u^{2} + 2 u + 4.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D - 6 u^{2} + 2 u + 4\,\mathrm{d}A.\end{aligned}
$$

Finally, 

$$
a+b+c=(-6)+(2)+(4)=0.
$$


## Generated observed-pattern bank variation q-161303

### cubic_ruled — moderate
Author metadata: observed; parameters `{'a': 1, 'b': 2, 'c': 2, 'd': 3, 'scale': 2}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 2,\,0,\,4\right\rangle,\quad r(u,v)=\left\langle u + v,\,u^{2} + 2 v,\,u^{3} + 3 v\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D$ excludes $u=1$, where the parametrization is singular.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D a u^{2} + b u + c\,\mathrm{d}A
$$

what is the value of $a+b+c?$

- $0$ **correct**
- $-4$
- $8$
- $4$
- $-8$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}r'_u & =\left\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\right\rangle \\  & =\left\langle \frac{\partial}{\partial u}(u + v),\,\frac{\partial}{\partial u}(u^{2} + 2 v),\,\frac{\partial}{\partial u}(u^{3} + 3 v)\right\rangle \\  & =\left\langle 1,\,2 u,\,3 u^{2}\right\rangle \\ r'_v & =\left\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\right\rangle \\  & =\left\langle \frac{\partial}{\partial v}(u + v),\,\frac{\partial}{\partial v}(u^{2} + 2 v),\,\frac{\partial}{\partial v}(u^{3} + 3 v)\right\rangle \\  & =\left\langle 1,\,2,\,3\right\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}r'_u\times r'_v & =\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\1&2 u&3 u^{2}\\1&2&3\end{vmatrix} \\  & =\left\langle \begin{vmatrix}2 u&3 u^{2}\\2&3\end{vmatrix},-\begin{vmatrix}1&3 u^{2}\\1&3\end{vmatrix},\begin{vmatrix}1&2 u\\1&2\end{vmatrix}\right\rangle \\  & =\left\langle - 6 u^{2} + 6 u,\,3 u^{2} - 3,\,2 - 2 u\right\rangle.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 2,\,0,\,4\right\rangle\big|_{x=u + v,\,y=u^{2} + 2 v,\,z=u^{3} + 3 v} \\  & =\left\langle 2,\,0,\,4\right\rangle \\  & =\left\langle 2,\,0,\,4\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 2,\,0,\,4\right\rangle\cdot \left\langle - 6 u^{2} + 6 u,\,3 u^{2} - 3,\,2 - 2 u\right\rangle \\  & =\left(2\right)\cdot\left(- 6 u^{2} + 6 u\right)+\left(0\right)\cdot\left(3 u^{2} - 3\right)+\left(4\right)\cdot\left(2 - 2 u\right) \\  & =\left(- 12 u^{2} + 12 u\right)+\left(0\right)+\left(8 - 8 u\right) \\  & =- 12 u^{2} + 4 u + 8.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D - 12 u^{2} + 4 u + 8\,\mathrm{d}A.\end{aligned}
$$

Finally, 

$$
a+b+c=(-12)+(4)+(8)=0.
$$


## Generated authored-default variant q-161303

### cubic_ruled — moderate
Author metadata: authored_cubic; parameters `{'a': 4, 'b': 4, 'c': 4, 'd': 2, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 4,\,0,\,4\right\rangle,\quad r(u,v)=\left\langle u + v,\,u^{2} + 4 v,\,u^{3} + 2 v\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D a u^{2} + b u + c\,\mathrm{d}A
$$

what is the value of $a+b+c?$

- $40$
- $-24$ **correct**
- $24$
- $12$
- $-40$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}r'_u & =\left\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\right\rangle \\  & =\left\langle \frac{\partial}{\partial u}(u + v),\,\frac{\partial}{\partial u}(u^{2} + 4 v),\,\frac{\partial}{\partial u}(u^{3} + 2 v)\right\rangle \\  & =\left\langle 1,\,2 u,\,3 u^{2}\right\rangle \\ r'_v & =\left\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\right\rangle \\  & =\left\langle \frac{\partial}{\partial v}(u + v),\,\frac{\partial}{\partial v}(u^{2} + 4 v),\,\frac{\partial}{\partial v}(u^{3} + 2 v)\right\rangle \\  & =\left\langle 1,\,4,\,2\right\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}r'_u\times r'_v & =\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\1&2 u&3 u^{2}\\1&4&2\end{vmatrix} \\  & =\left\langle \begin{vmatrix}2 u&3 u^{2}\\4&2\end{vmatrix},-\begin{vmatrix}1&3 u^{2}\\1&2\end{vmatrix},\begin{vmatrix}1&2 u\\1&4\end{vmatrix}\right\rangle \\  & =\left\langle - 12 u^{2} + 4 u,\,3 u^{2} - 2,\,4 - 2 u\right\rangle.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 4,\,0,\,4\right\rangle\big|_{x=u + v,\,y=u^{2} + 4 v,\,z=u^{3} + 2 v} \\  & =\left\langle 4,\,0,\,4\right\rangle \\  & =\left\langle 4,\,0,\,4\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 4,\,0,\,4\right\rangle\cdot \left\langle - 12 u^{2} + 4 u,\,3 u^{2} - 2,\,4 - 2 u\right\rangle \\  & =\left(4\right)\cdot\left(- 12 u^{2} + 4 u\right)+\left(0\right)\cdot\left(3 u^{2} - 2\right)+\left(4\right)\cdot\left(4 - 2 u\right) \\  & =\left(- 48 u^{2} + 16 u\right)+\left(0\right)+\left(16 - 8 u\right) \\  & =- 48 u^{2} + 8 u + 16.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D - 48 u^{2} + 8 u + 16\,\mathrm{d}A.\end{aligned}
$$

Finally, 

$$
a+b+c=(-48)+(8)+(16)=-24.
$$


## Generated authored-default variant q-161303

### cubic_ruled — moderate
Author metadata: authored_cubic; parameters `{'a': 3, 'b': 4, 'c': 4, 'd': 1, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 3,\,0,\,4\right\rangle,\quad r(u,v)=\left\langle u + v,\,u^{2} + 4 v,\,u^{3} + v\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D a u^{2} + b u + c\,\mathrm{d}A
$$

what is the value of $a+b+c?$

- $-38$
- $38$
- $22$
- $-22$ **correct**
- $7$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}r'_u & =\left\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\right\rangle \\  & =\left\langle \frac{\partial}{\partial u}(u + v),\,\frac{\partial}{\partial u}(u^{2} + 4 v),\,\frac{\partial}{\partial u}(u^{3} + v)\right\rangle \\  & =\left\langle 1,\,2 u,\,3 u^{2}\right\rangle \\ r'_v & =\left\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\right\rangle \\  & =\left\langle \frac{\partial}{\partial v}(u + v),\,\frac{\partial}{\partial v}(u^{2} + 4 v),\,\frac{\partial}{\partial v}(u^{3} + v)\right\rangle \\  & =\left\langle 1,\,4,\,1\right\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}r'_u\times r'_v & =\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\1&2 u&3 u^{2}\\1&4&1\end{vmatrix} \\  & =\left\langle \begin{vmatrix}2 u&3 u^{2}\\4&1\end{vmatrix},-\begin{vmatrix}1&3 u^{2}\\1&1\end{vmatrix},\begin{vmatrix}1&2 u\\1&4\end{vmatrix}\right\rangle \\  & =\left\langle - 12 u^{2} + 2 u,\,3 u^{2} - 1,\,4 - 2 u\right\rangle.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 3,\,0,\,4\right\rangle\big|_{x=u + v,\,y=u^{2} + 4 v,\,z=u^{3} + v} \\  & =\left\langle 3,\,0,\,4\right\rangle \\  & =\left\langle 3,\,0,\,4\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 3,\,0,\,4\right\rangle\cdot \left\langle - 12 u^{2} + 2 u,\,3 u^{2} - 1,\,4 - 2 u\right\rangle \\  & =\left(3\right)\cdot\left(- 12 u^{2} + 2 u\right)+\left(0\right)\cdot\left(3 u^{2} - 1\right)+\left(4\right)\cdot\left(4 - 2 u\right) \\  & =\left(- 36 u^{2} + 6 u\right)+\left(0\right)+\left(16 - 8 u\right) \\  & =- 36 u^{2} - 2 u + 16.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D - 36 u^{2} - 2 u + 16\,\mathrm{d}A.\end{aligned}
$$

Finally, 

$$
a+b+c=(-36)+(-2)+(16)=-22.
$$


## Original q-161306

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=⟨x-\frac{1}{z},\,y+\frac{1}{z},\,z⟩,\,r(u,v)=⟨u{e}^{v},\,u{e}^{-v},\,u⟩,\,(u,v)\in D⊂{R}^{2}.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}a{e}^{v}+b{e}^{-v}\,\text{d}A
$$

what is the value of $a+b?$


Original complete bank:

- $-2$

- $-1$

- $0$ **correct**

- $1$

- $2$


Original worked solution:

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u{e}^{v}),\,\frac{∂}{∂u}(u{e}^{-v}),\,\frac{∂}{∂u}(u)⟩ \\  & =⟨{e}^{v},\,{e}^{-v},\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u{e}^{v}),\,\frac{∂}{∂v}(u{e}^{-v}),\,\frac{∂}{∂v}(u)⟩ \\  & =⟨u{e}^{v},\,-u{e}^{-v},\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ {e}^{v} & {e}^{-v} & 1 \\ u{e}^{v} & -u{e}^{-v} & 0\end{aligned}| \\  & =⟨|\begin{aligned}{e}^{-v} & 1 \\ -u{e}^{-v} & 0\end{aligned}|,\,-|\begin{aligned}{e}^{v} & 1 \\ u{e}^{v} & 0\end{aligned}|,\,|\begin{aligned}{e}^{v} & {e}^{-v} \\ u{e}^{v} & -u{e}^{-v}\end{aligned}|⟩ \\  & =⟨u{e}^{-v},\,u{e}^{v},\,-2u⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨x-\frac{1}{z},\,y+\frac{1}{z},\,z⟩{|}_{x=u{e}^{v}\,y=u{e}^{-v}\,z=u} \\  & =⟨u{e}^{v}-\frac{1}{u},\,u{e}^{-v}+\frac{1}{u},\,u⟩.\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u{e}^{v}-\frac{1}{u},\,u{e}^{-v}+\frac{1}{u},\,u⟩\cdot ⟨u{e}^{-v},\,u{e}^{v},\,-2u⟩ \\  & =(u{e}^{v}-\frac{1}{u})\cdot u{e}^{-v}+(u{e}^{-v}+\frac{1}{u})\cdot u{e}^{v}+u\cdot (-2u) \\  & ={u}^{2}-{e}^{-v}+{u}^{2}+{e}^{v}-2{u}^{2} \\  & ={e}^{v}-{e}^{-v}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}1\cdot {e}^{v}+(-1)\cdot {e}^{-v}\,\text{d}A.\end{aligned}
$$

Finally, 

$$
a+b=1-1=0.
$$


## Parameterized source replay q-161306

### exponential_sum — moderate
Author metadata: observed; parameters `{'a': 1, 'b': 1, 'k': 1, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle x - \frac{1}{z},\,y + \frac{1}{z},\,z\right\rangle,\quad r(u,v)=\left\langle u e^{v},\,u e^{- v},\,u\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0\}$, so the vector field is defined on $S$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D a e^{v} + b e^{- v}\,\mathrm{d}A
$$

what is the value of $a+b?$

- $0$ **correct**
- $-1$
- $-2$
- $2$
- $1$

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
\begin{aligned}F(r(u,v)) & =\left\langle x - \frac{1}{z},\,y + \frac{1}{z},\,z\right\rangle\big|_{x=u e^{v},\,y=u e^{- v},\,z=u} \\  & =\left\langle \left(u e^{v}\right) - \frac{1}{\left(u\right)},\,\left(u e^{- v}\right) + \frac{1}{\left(u\right)},\,\left(u\right)\right\rangle \\  & =\left\langle u e^{v} - \frac{1}{u},\,u e^{- v} + \frac{1}{u},\,u\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle u e^{v} - \frac{1}{u},\,u e^{- v} + \frac{1}{u},\,u\right\rangle\cdot \left\langle u e^{- v},\,u e^{v},\,- 2 u\right\rangle \\  & =\left(u e^{v} - \frac{1}{u}\right)\cdot\left(u e^{- v}\right)+\left(u e^{- v} + \frac{1}{u}\right)\cdot\left(u e^{v}\right)+\left(u\right)\cdot\left(- 2 u\right) \\  & =\left(u^{2} - e^{- v}\right)+\left(u^{2} + e^{v}\right)+\left(- 2 u^{2}\right) \\  & =e^{v} - e^{- v}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D e^{v} - e^{- v}\,\mathrm{d}A.\end{aligned}
$$

Finally, 

$$
a+b=(1)+(-1)=0.
$$


## Generated observed-pattern bank variation q-161306

### exponential_sum — moderate
Author metadata: observed; parameters `{'a': 1, 'b': 1, 'k': 1, 'scale': 2}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 2 x - \frac{2}{z},\,2 y + \frac{2}{z},\,2 z\right\rangle,\quad r(u,v)=\left\langle u e^{v},\,u e^{- v},\,u\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0\}$, so the vector field is defined on $S$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D a e^{v} + b e^{- v}\,\mathrm{d}A
$$

what is the value of $a+b?$

- $0$ **correct**
- $-2$
- $-4$
- $4$
- $2$

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
\begin{aligned}F(r(u,v)) & =\left\langle 2 x - \frac{2}{z},\,2 y + \frac{2}{z},\,2 z\right\rangle\big|_{x=u e^{v},\,y=u e^{- v},\,z=u} \\  & =\left\langle 2 \left(u e^{v}\right) - \frac{2}{\left(u\right)},\,2 \left(u e^{- v}\right) + \frac{2}{\left(u\right)},\,2 \left(u\right)\right\rangle \\  & =\left\langle 2 u e^{v} - \frac{2}{u},\,2 u e^{- v} + \frac{2}{u},\,2 u\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 2 u e^{v} - \frac{2}{u},\,2 u e^{- v} + \frac{2}{u},\,2 u\right\rangle\cdot \left\langle u e^{- v},\,u e^{v},\,- 2 u\right\rangle \\  & =\left(2 u e^{v} - \frac{2}{u}\right)\cdot\left(u e^{- v}\right)+\left(2 u e^{- v} + \frac{2}{u}\right)\cdot\left(u e^{v}\right)+\left(2 u\right)\cdot\left(- 2 u\right) \\  & =\left(2 u^{2} - 2 e^{- v}\right)+\left(2 u^{2} + 2 e^{v}\right)+\left(- 4 u^{2}\right) \\  & =2 e^{v} - 2 e^{- v}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 2 e^{v} - 2 e^{- v}\,\mathrm{d}A.\end{aligned}
$$

Finally, 

$$
a+b=(2)+(-2)=0.
$$


## Generated authored-default variant q-161306

### exponential_sum — moderate
Author metadata: authored_tangents; parameters `{'a': 2, 'b': 1, 'k': 4, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 4 x - \frac{2}{z},\,4 y + \frac{1}{z},\,4 z\right\rangle,\quad r(u,v)=\left\langle u e^{v},\,u e^{- v},\,u\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0\}$, so the vector field is defined on $S$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D a e^{v} + b e^{- v}\,\mathrm{d}A
$$

what is the value of $a+b?$

- $- \frac{1}{u}$
- $-1$ **correct**
- $1$
- $4 u^{2} + 4 u v - u$
- $-3$

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
\begin{aligned}F(r(u,v)) & =\left\langle 4 x - \frac{2}{z},\,4 y + \frac{1}{z},\,4 z\right\rangle\big|_{x=u e^{v},\,y=u e^{- v},\,z=u} \\  & =\left\langle 4 \left(u e^{v}\right) - \frac{2}{\left(u\right)},\,4 \left(u e^{- v}\right) + \frac{1}{\left(u\right)},\,4 \left(u\right)\right\rangle \\  & =\left\langle 4 u e^{v} - \frac{2}{u},\,4 u e^{- v} + \frac{1}{u},\,4 u\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 4 u e^{v} - \frac{2}{u},\,4 u e^{- v} + \frac{1}{u},\,4 u\right\rangle\cdot \left\langle u e^{- v},\,u e^{v},\,- 2 u\right\rangle \\  & =\left(4 u e^{v} - \frac{2}{u}\right)\cdot\left(u e^{- v}\right)+\left(4 u e^{- v} + \frac{1}{u}\right)\cdot\left(u e^{v}\right)+\left(4 u\right)\cdot\left(- 2 u\right) \\  & =\left(4 u^{2} - 2 e^{- v}\right)+\left(4 u^{2} + e^{v}\right)+\left(- 8 u^{2}\right) \\  & =e^{v} - 2 e^{- v}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D e^{v} - 2 e^{- v}\,\mathrm{d}A.\end{aligned}
$$

Finally, 

$$
a+b=(1)+(-2)=-1.
$$


## Generated authored-default variant q-161306

### exponential_sum — moderate
Author metadata: authored_tangents; parameters `{'a': 1, 'b': 3, 'k': 3, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 3 x - \frac{1}{z},\,3 y + \frac{3}{z},\,3 z\right\rangle,\quad r(u,v)=\left\langle u e^{v},\,u e^{- v},\,u\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0\}$, so the vector field is defined on $S$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D a e^{v} + b e^{- v}\,\mathrm{d}A
$$

what is the value of $a+b?$

- $-4$
- $\frac{2}{u}$
- $-2$
- $2$ **correct**
- $3 u^{2} + 3 u v + 2 u$

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
\begin{aligned}F(r(u,v)) & =\left\langle 3 x - \frac{1}{z},\,3 y + \frac{3}{z},\,3 z\right\rangle\big|_{x=u e^{v},\,y=u e^{- v},\,z=u} \\  & =\left\langle 3 \left(u e^{v}\right) - \frac{1}{\left(u\right)},\,3 \left(u e^{- v}\right) + \frac{3}{\left(u\right)},\,3 \left(u\right)\right\rangle \\  & =\left\langle 3 u e^{v} - \frac{1}{u},\,3 u e^{- v} + \frac{3}{u},\,3 u\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 3 u e^{v} - \frac{1}{u},\,3 u e^{- v} + \frac{3}{u},\,3 u\right\rangle\cdot \left\langle u e^{- v},\,u e^{v},\,- 2 u\right\rangle \\  & =\left(3 u e^{v} - \frac{1}{u}\right)\cdot\left(u e^{- v}\right)+\left(3 u e^{- v} + \frac{3}{u}\right)\cdot\left(u e^{v}\right)+\left(3 u\right)\cdot\left(- 2 u\right) \\  & =\left(3 u^{2} - e^{- v}\right)+\left(3 u^{2} + 3 e^{v}\right)+\left(- 6 u^{2}\right) \\  & =3 e^{v} - e^{- v}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 3 e^{v} - e^{- v}\,\mathrm{d}A.\end{aligned}
$$

Finally, 

$$
a+b=(3)+(-1)=2.
$$


## Original q-161384

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=⟨{z}^{2},\,{y}^{2},\,x⟩,\,r(u,v)=⟨{u}^{2},\,v,\,u⟩,\,(u,v)\in D⊂{R}^{2}.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

what is the missing expression?

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨-1,\,0,\,2u⟩.$*


Original complete bank:

- $2{u}^{2}$

- $u{v}^{2}-2{v}^{3}$

- $2{u}^{2}+uv$

- ${u}^{2}-{v}^{2}$

- $2{u}^{3}-{u}^{2}$ **correct**


Original worked solution:

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨-1,\,0,\,2u⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨{z}^{2},\,{y}^{2},\,x⟩{|}_{x={u}^{2}\,y=v\,z=u} \\  & =⟨{u}^{2},\,{v}^{2},\,{u}^{2}⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨{u}^{2},\,{v}^{2},\,{u}^{2}⟩\cdot ⟨-1,\,0,\,2u⟩ \\  & ={u}^{2}\cdot (-1)+{v}^{2}\cdot 0+{u}^{2}\cdot 2u \\  & =2{u}^{3}-{u}^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}\,2{u}^{3}-{u}^{2}\,\text{d}A.\end{aligned}
$$


## Parameterized source replay q-161384

### ruled_square — easy
Author metadata: observed; parameters `{'a': 1, 'b': 1, 'c': 1, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle z^{2},\,y^{2},\,x\right\rangle,\quad r(u,v)=\left\langle u^{2},\,v,\,u\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

*Hint: You can use the fact that $r'_u\times r'_v=\left\langle -1,\,0,\,2 u\right\rangle.$*

- $2 u^{2} + u v$
- $u v^{2} - 2 v^{3}$
- $2 u^{2}$
- $2 u^{3} - u^{2}$ **correct**
- $u^{2} - v^{2}$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
r'_u\times r'_v=\left\langle -1,\,0,\,2 u\right\rangle.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle z^{2},\,y^{2},\,x\right\rangle\big|_{x=u^{2},\,y=v,\,z=u} \\  & =\left\langle \left(u\right)^{2},\,\left(v\right)^{2},\,\left(u^{2}\right)\right\rangle \\  & =\left\langle u^{2},\,v^{2},\,u^{2}\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle u^{2},\,v^{2},\,u^{2}\right\rangle\cdot \left\langle -1,\,0,\,2 u\right\rangle \\  & =\left(u^{2}\right)\cdot\left(-1\right)+\left(v^{2}\right)\cdot\left(0\right)+\left(u^{2}\right)\cdot\left(2 u\right) \\  & =\left(- u^{2}\right)+\left(0\right)+\left(2 u^{3}\right) \\  & =2 u^{3} - u^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 2 u^{3} - u^{2}\,\mathrm{d}A.\end{aligned}
$$


## Generated observed-pattern bank variation q-161384

### ruled_square — easy
Author metadata: observed; parameters `{'a': 1, 'b': 1, 'c': 1, 'scale': 2}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 2 z^{2},\,2 y^{2},\,2 x\right\rangle,\quad r(u,v)=\left\langle u^{2},\,v,\,u\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

*Hint: You can use the fact that $r'_u\times r'_v=\left\langle -1,\,0,\,2 u\right\rangle.$*

- $4 u^{2} + 2 u v$
- $2 u v^{2} - 4 v^{3}$
- $4 u^{2}$
- $4 u^{3} - 2 u^{2}$ **correct**
- $2 u^{2} - 2 v^{2}$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
r'_u\times r'_v=\left\langle -1,\,0,\,2 u\right\rangle.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 2 z^{2},\,2 y^{2},\,2 x\right\rangle\big|_{x=u^{2},\,y=v,\,z=u} \\  & =\left\langle 2 \left(u\right)^{2},\,2 \left(v\right)^{2},\,2 \left(u^{2}\right)\right\rangle \\  & =\left\langle 2 u^{2},\,2 v^{2},\,2 u^{2}\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 2 u^{2},\,2 v^{2},\,2 u^{2}\right\rangle\cdot \left\langle -1,\,0,\,2 u\right\rangle \\  & =\left(2 u^{2}\right)\cdot\left(-1\right)+\left(2 v^{2}\right)\cdot\left(0\right)+\left(2 u^{2}\right)\cdot\left(2 u\right) \\  & =\left(- 2 u^{2}\right)+\left(0\right)+\left(4 u^{3}\right) \\  & =4 u^{3} - 2 u^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 4 u^{3} - 2 u^{2}\,\mathrm{d}A.\end{aligned}
$$


## Generated authored-default variant q-161384

### ruled_square — easy
Author metadata: authored_tangents; parameters `{'a': 4, 'b': 4, 'c': 4, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 4 z^{2},\,4 y^{2},\,4 x\right\rangle,\quad r(u,v)=\left\langle u^{2},\,v,\,u\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

*Hint: You can use the fact that $r'_u\times r'_v=\left\langle -1,\,0,\,2 u\right\rangle.$*

- $8 u^{3} + 4 u^{2}$
- $8 u^{3} - 4 u^{2}$ **correct**
- $- 8 u^{3} + 4 u^{2}$
- $8 u^{2} - 4$
- $4 v^{2}$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
r'_u\times r'_v=\left\langle -1,\,0,\,2 u\right\rangle.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 4 z^{2},\,4 y^{2},\,4 x\right\rangle\big|_{x=u^{2},\,y=v,\,z=u} \\  & =\left\langle 4 \left(u\right)^{2},\,4 \left(v\right)^{2},\,4 \left(u^{2}\right)\right\rangle \\  & =\left\langle 4 u^{2},\,4 v^{2},\,4 u^{2}\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 4 u^{2},\,4 v^{2},\,4 u^{2}\right\rangle\cdot \left\langle -1,\,0,\,2 u\right\rangle \\  & =\left(4 u^{2}\right)\cdot\left(-1\right)+\left(4 v^{2}\right)\cdot\left(0\right)+\left(4 u^{2}\right)\cdot\left(2 u\right) \\  & =\left(- 4 u^{2}\right)+\left(0\right)+\left(8 u^{3}\right) \\  & =8 u^{3} - 4 u^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 8 u^{3} - 4 u^{2}\,\mathrm{d}A.\end{aligned}
$$


## Generated authored-default variant q-161384

### ruled_square — easy
Author metadata: authored_tangents; parameters `{'a': 1, 'b': 3, 'c': 3, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle z^{2},\,3 y^{2},\,3 x\right\rangle,\quad r(u,v)=\left\langle u^{2},\,v,\,u\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

*Hint: You can use the fact that $r'_u\times r'_v=\left\langle -1,\,0,\,2 u\right\rangle.$*

- $3 v^{2}$
- $2 u^{3} + 3 u^{2}$
- $- 6 u^{3} + u^{2}$
- $6 u^{3} - u^{2}$ **correct**
- $6 u^{2} - 1$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
r'_u\times r'_v=\left\langle -1,\,0,\,2 u\right\rangle.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle z^{2},\,3 y^{2},\,3 x\right\rangle\big|_{x=u^{2},\,y=v,\,z=u} \\  & =\left\langle \left(u\right)^{2},\,3 \left(v\right)^{2},\,3 \left(u^{2}\right)\right\rangle \\  & =\left\langle u^{2},\,3 v^{2},\,3 u^{2}\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle u^{2},\,3 v^{2},\,3 u^{2}\right\rangle\cdot \left\langle -1,\,0,\,2 u\right\rangle \\  & =\left(u^{2}\right)\cdot\left(-1\right)+\left(3 v^{2}\right)\cdot\left(0\right)+\left(3 u^{2}\right)\cdot\left(2 u\right) \\  & =\left(- u^{2}\right)+\left(0\right)+\left(6 u^{3}\right) \\  & =6 u^{3} - u^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 6 u^{3} - u^{2}\,\mathrm{d}A.\end{aligned}
$$


## Original q-161251

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=⟨3x,\,3y,\,z⟩,\,r(u,v)=⟨u\operatorname{cos}⁡v,\,u\operatorname{sin}⁡v,\,{u}^{2}⟩,\,(u,v)\in D⊂{R}^{2}.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

what is the missing expression?

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨-2{u}^{2}\operatorname{cos}⁡v,\,-2{u}^{2}\operatorname{sin}⁡v,\,u⟩.$*


Original complete bank:

- $6{u}^{3}$

- ${u}^{3}\operatorname{sin}⁡v\operatorname{cos}⁡v$

- $2{u}^{2}\operatorname{sin}⁡v\operatorname{cos}⁡v$

- $-5{u}^{3}$ **correct**

- $-3{u}^{2}$


Original worked solution:

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨-2{u}^{2}\operatorname{cos}⁡v,\,-2{u}^{2}\operatorname{sin}⁡v,\,u⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨3x,\,3y,\,z⟩{|}_{x=u\operatorname{cos}⁡v\,y=u\operatorname{sin}⁡v\,z={u}^{2}} \\  & =⟨3u\operatorname{cos}⁡v,\,3u\operatorname{sin}⁡v,\,{u}^{2}⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3u\operatorname{cos}⁡v,\,3u\operatorname{sin}⁡v,\,{u}^{2}⟩\cdot ⟨-2{u}^{2}\operatorname{cos}⁡v,\,-2{u}^{2}\operatorname{sin}⁡v,\,u⟩ \\  & =3u\operatorname{cos}⁡v\cdot (-2{u}^{2}\operatorname{cos}⁡v)+3u\operatorname{sin}⁡v\cdot (-2{u}^{2}\operatorname{sin}⁡v)+{u}^{2}\cdot u \\  & =-6{u}^{3}({cos}^{2}⁡v+{sin}^{2}⁡v)+{u}^{3} \\  & =-5{u}^{3}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}\,-5{u}^{3}\,\text{d}A.\end{aligned}
$$


## Parameterized source replay q-161251

### polar_hint — easy
Author metadata: observed; parameters `{'a': 3, 'b': 3, 'c': 1, 'h': 1, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 3 x,\,3 y,\,z\right\rangle,\quad r(u,v)=\left\langle u \cos{\left(v \right)},\,u \sin{\left(v \right)},\,u^{2}\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0,\ 0<v<2\pi\}$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

*Hint: You can use the fact that $r'_u\times r'_v=\left\langle - 2 u^{2} \cos{\left(v \right)},\,- 2 u^{2} \sin{\left(v \right)},\,u\right\rangle.$*

- $2 u^{2} \sin{\left(v \right)} \cos{\left(v \right)}$
- $u^{3} \sin{\left(v \right)} \cos{\left(v \right)}$
- $6 u^{3}$
- $- 3 u^{2}$
- $- 5 u^{3}$ **correct**

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
r'_u\times r'_v=\left\langle - 2 u^{2} \cos{\left(v \right)},\,- 2 u^{2} \sin{\left(v \right)},\,u\right\rangle.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 3 x,\,3 y,\,z\right\rangle\big|_{x=u \cos{\left(v \right)},\,y=u \sin{\left(v \right)},\,z=u^{2}} \\  & =\left\langle 3 \left(u \cos{\left(v \right)}\right),\,3 \left(u \sin{\left(v \right)}\right),\,\left(u^{2}\right)\right\rangle \\  & =\left\langle 3 u \cos{\left(v \right)},\,3 u \sin{\left(v \right)},\,u^{2}\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 3 u \cos{\left(v \right)},\,3 u \sin{\left(v \right)},\,u^{2}\right\rangle\cdot \left\langle - 2 u^{2} \cos{\left(v \right)},\,- 2 u^{2} \sin{\left(v \right)},\,u\right\rangle \\  & =\left(3 u \cos{\left(v \right)}\right)\cdot\left(- 2 u^{2} \cos{\left(v \right)}\right)+\left(3 u \sin{\left(v \right)}\right)\cdot\left(- 2 u^{2} \sin{\left(v \right)}\right)+\left(u^{2}\right)\cdot\left(u\right) \\  & =\left(6 u^{3} \sin^{2}{\left(v \right)} - 6 u^{3}\right)+\left(- 6 u^{3} \sin^{2}{\left(v \right)}\right)+\left(u^{3}\right) \\  & =- 6 u^{3}\left(\cos^2 v+\sin^2 v\right)+u^{3} \\  & =- 5 u^{3}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D - 5 u^{3}\,\mathrm{d}A.\end{aligned}
$$


## Generated observed-pattern bank variation q-161251

### polar_hint — easy
Author metadata: observed; parameters `{'a': 3, 'b': 3, 'c': 1, 'h': 1, 'scale': 2}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 6 x,\,6 y,\,2 z\right\rangle,\quad r(u,v)=\left\langle u \cos{\left(v \right)},\,u \sin{\left(v \right)},\,u^{2}\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0,\ 0<v<2\pi\}$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

*Hint: You can use the fact that $r'_u\times r'_v=\left\langle - 2 u^{2} \cos{\left(v \right)},\,- 2 u^{2} \sin{\left(v \right)},\,u\right\rangle.$*

- $4 u^{2} \sin{\left(v \right)} \cos{\left(v \right)}$
- $2 u^{3} \sin{\left(v \right)} \cos{\left(v \right)}$
- $12 u^{3}$
- $- 6 u^{2}$
- $- 10 u^{3}$ **correct**

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
r'_u\times r'_v=\left\langle - 2 u^{2} \cos{\left(v \right)},\,- 2 u^{2} \sin{\left(v \right)},\,u\right\rangle.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 6 x,\,6 y,\,2 z\right\rangle\big|_{x=u \cos{\left(v \right)},\,y=u \sin{\left(v \right)},\,z=u^{2}} \\  & =\left\langle 6 \left(u \cos{\left(v \right)}\right),\,6 \left(u \sin{\left(v \right)}\right),\,2 \left(u^{2}\right)\right\rangle \\  & =\left\langle 6 u \cos{\left(v \right)},\,6 u \sin{\left(v \right)},\,2 u^{2}\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 6 u \cos{\left(v \right)},\,6 u \sin{\left(v \right)},\,2 u^{2}\right\rangle\cdot \left\langle - 2 u^{2} \cos{\left(v \right)},\,- 2 u^{2} \sin{\left(v \right)},\,u\right\rangle \\  & =\left(6 u \cos{\left(v \right)}\right)\cdot\left(- 2 u^{2} \cos{\left(v \right)}\right)+\left(6 u \sin{\left(v \right)}\right)\cdot\left(- 2 u^{2} \sin{\left(v \right)}\right)+\left(2 u^{2}\right)\cdot\left(u\right) \\  & =\left(12 u^{3} \sin^{2}{\left(v \right)} - 12 u^{3}\right)+\left(- 12 u^{3} \sin^{2}{\left(v \right)}\right)+\left(2 u^{3}\right) \\  & =- 12 u^{3}\left(\cos^2 v+\sin^2 v\right)+2 u^{3} \\  & =- 10 u^{3}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D - 10 u^{3}\,\mathrm{d}A.\end{aligned}
$$


## Generated authored-default variant q-161251

### polar_hint — easy
Author metadata: authored_cofactor; parameters `{'a': 4, 'b': 4, 'c': 4, 'h': 2, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 4 x,\,4 y,\,4 z\right\rangle,\quad r(u,v)=\left\langle u \cos{\left(v \right)},\,u \sin{\left(v \right)},\,2 u^{2}\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0,\ 0<v<2\pi\}$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

*Hint: You can use the fact that $r'_u\times r'_v=\left\langle - 4 u^{2} \cos{\left(v \right)},\,- 4 u^{2} \sin{\left(v \right)},\,u\right\rangle.$*

- $32 u^{3} \sin^{2}{\left(v \right)} - 8 u^{3}$
- $- 8 u^{3}$ **correct**
- $8 u^{3}$
- $8 u^{2} + 4 u \sin{\left(v \right)} + 4 u \cos{\left(v \right)}$
- $- 16 u^{3} \cos{\left(v \right)} - 16 u^{2} v \sin{\left(v \right)} + 4 u$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
r'_u\times r'_v=\left\langle - 4 u^{2} \cos{\left(v \right)},\,- 4 u^{2} \sin{\left(v \right)},\,u\right\rangle.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 4 x,\,4 y,\,4 z\right\rangle\big|_{x=u \cos{\left(v \right)},\,y=u \sin{\left(v \right)},\,z=2 u^{2}} \\  & =\left\langle 4 \left(u \cos{\left(v \right)}\right),\,4 \left(u \sin{\left(v \right)}\right),\,4 \left(2 u^{2}\right)\right\rangle \\  & =\left\langle 4 u \cos{\left(v \right)},\,4 u \sin{\left(v \right)},\,8 u^{2}\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 4 u \cos{\left(v \right)},\,4 u \sin{\left(v \right)},\,8 u^{2}\right\rangle\cdot \left\langle - 4 u^{2} \cos{\left(v \right)},\,- 4 u^{2} \sin{\left(v \right)},\,u\right\rangle \\  & =\left(4 u \cos{\left(v \right)}\right)\cdot\left(- 4 u^{2} \cos{\left(v \right)}\right)+\left(4 u \sin{\left(v \right)}\right)\cdot\left(- 4 u^{2} \sin{\left(v \right)}\right)+\left(8 u^{2}\right)\cdot\left(u\right) \\  & =\left(16 u^{3} \sin^{2}{\left(v \right)} - 16 u^{3}\right)+\left(- 16 u^{3} \sin^{2}{\left(v \right)}\right)+\left(8 u^{3}\right) \\  & =- 16 u^{3}\left(\cos^2 v+\sin^2 v\right)+8 u^{3} \\  & =- 8 u^{3}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D - 8 u^{3}\,\mathrm{d}A.\end{aligned}
$$


## Generated authored-default variant q-161251

### polar_hint — easy
Author metadata: authored_cofactor; parameters `{'a': 1, 'b': 3, 'c': 3, 'h': 1, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle x,\,3 y,\,3 z\right\rangle,\quad r(u,v)=\left\langle u \cos{\left(v \right)},\,u \sin{\left(v \right)},\,u^{2}\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0,\ 0<v<2\pi\}$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

*Hint: You can use the fact that $r'_u\times r'_v=\left\langle - 2 u^{2} \cos{\left(v \right)},\,- 2 u^{2} \sin{\left(v \right)},\,u\right\rangle.$*

- $- 2 u^{3} \cos{\left(v \right)} - 6 u^{2} v \sin{\left(v \right)} + 3 u$
- $8 u^{3} \sin^{2}{\left(v \right)} + u^{3}$
- $4 u^{3} \sin^{2}{\left(v \right)} - u^{3}$
- $- 4 u^{3} \sin^{2}{\left(v \right)} + u^{3}$ **correct**
- $3 u^{2} + 3 u \sin{\left(v \right)} + u \cos{\left(v \right)}$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
r'_u\times r'_v=\left\langle - 2 u^{2} \cos{\left(v \right)},\,- 2 u^{2} \sin{\left(v \right)},\,u\right\rangle.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle x,\,3 y,\,3 z\right\rangle\big|_{x=u \cos{\left(v \right)},\,y=u \sin{\left(v \right)},\,z=u^{2}} \\  & =\left\langle \left(u \cos{\left(v \right)}\right),\,3 \left(u \sin{\left(v \right)}\right),\,3 \left(u^{2}\right)\right\rangle \\  & =\left\langle u \cos{\left(v \right)},\,3 u \sin{\left(v \right)},\,3 u^{2}\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle u \cos{\left(v \right)},\,3 u \sin{\left(v \right)},\,3 u^{2}\right\rangle\cdot \left\langle - 2 u^{2} \cos{\left(v \right)},\,- 2 u^{2} \sin{\left(v \right)},\,u\right\rangle \\  & =\left(u \cos{\left(v \right)}\right)\cdot\left(- 2 u^{2} \cos{\left(v \right)}\right)+\left(3 u \sin{\left(v \right)}\right)\cdot\left(- 2 u^{2} \sin{\left(v \right)}\right)+\left(3 u^{2}\right)\cdot\left(u\right) \\  & =\left(2 u^{3} \sin^{2}{\left(v \right)} - 2 u^{3}\right)+\left(- 6 u^{3} \sin^{2}{\left(v \right)}\right)+\left(3 u^{3}\right) \\  & =- 4 u^{3} \sin^{2}{\left(v \right)} + u^{3}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D - 4 u^{3} \sin^{2}{\left(v \right)} + u^{3}\,\mathrm{d}A.\end{aligned}
$$


## Original q-161383

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=⟨xz,\,y,\,xz⟩,\,r(u,v)=⟨u,\,uv,\,v⟩,\,(u,v)\in D⊂{R}^{2}.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}\boxed{}\,\text{d}A
$$

what is the missing expression?

*Hint: You can use the fact that ${r}_{u}^{′}\times {r}_{v}^{′}=⟨v,\,-1,\,u⟩.$*


Original complete bank:

- ${u}^{2}v$

- $u{v}^{2}-{u}^{2}v$

- ${u}^{2}{v}^{2}-2uv$

- $u{v}^{2}+uv+2{u}^{2}v$

- $u{v}^{2}-uv+{u}^{2}v$ **correct**


Original worked solution:

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
{r}_{u}^{′}\times {r}_{v}^{′}=⟨v,\,-1,\,u⟩.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨xz,\,y,\,xz⟩{|}_{x=u\,y=uv\,z=v} \\  & =⟨uv,\,uv,\,uv⟩\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨uv,\,uv,\,uv⟩\cdot ⟨v,\,-1,\,u⟩ \\  & =uv\cdot v+uv\cdot (-1)+uv\cdot u \\  & =u{v}^{2}-uv+{u}^{2}v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}\,u{v}^{2}-uv+{u}^{2}v\,\text{d}A.\end{aligned}
$$


## Parameterized source replay q-161383

### bilinear_hint — easy
Author metadata: observed; parameters `{'a': 1, 'b': 1, 'c': 1, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle x z,\,y,\,x z\right\rangle,\quad r(u,v)=\left\langle u,\,u v,\,v\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

*Hint: You can use the fact that $r'_u\times r'_v=\left\langle v,\,-1,\,u\right\rangle.$*

- $u^{2} v^{2} - 2 u v$
- $- u^{2} v + u v^{2}$
- $u^{2} v$
- $u^{2} v + u v^{2} - u v$ **correct**
- $2 u^{2} v + u v^{2} + u v$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
r'_u\times r'_v=\left\langle v,\,-1,\,u\right\rangle.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle x z,\,y,\,x z\right\rangle\big|_{x=u,\,y=u v,\,z=v} \\  & =\left\langle \left(u\right) \left(v\right),\,\left(u v\right),\,\left(u\right) \left(v\right)\right\rangle \\  & =\left\langle u v,\,u v,\,u v\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle u v,\,u v,\,u v\right\rangle\cdot \left\langle v,\,-1,\,u\right\rangle \\  & =\left(u v\right)\cdot\left(v\right)+\left(u v\right)\cdot\left(-1\right)+\left(u v\right)\cdot\left(u\right) \\  & =\left(u v^{2}\right)+\left(- u v\right)+\left(u^{2} v\right) \\  & =u^{2} v + u v^{2} - u v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D u^{2} v + u v^{2} - u v\,\mathrm{d}A.\end{aligned}
$$


## Generated observed-pattern bank variation q-161383

### bilinear_hint — easy
Author metadata: observed; parameters `{'a': 1, 'b': 1, 'c': 1, 'scale': 2}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 2 x z,\,2 y,\,2 x z\right\rangle,\quad r(u,v)=\left\langle u,\,u v,\,v\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

*Hint: You can use the fact that $r'_u\times r'_v=\left\langle v,\,-1,\,u\right\rangle.$*

- $2 u^{2} v^{2} - 4 u v$
- $- 2 u^{2} v + 2 u v^{2}$
- $2 u^{2} v$
- $2 u^{2} v + 2 u v^{2} - 2 u v$ **correct**
- $4 u^{2} v + 2 u v^{2} + 2 u v$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
r'_u\times r'_v=\left\langle v,\,-1,\,u\right\rangle.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 2 x z,\,2 y,\,2 x z\right\rangle\big|_{x=u,\,y=u v,\,z=v} \\  & =\left\langle 2 \left(u\right) \left(v\right),\,2 \left(u v\right),\,2 \left(u\right) \left(v\right)\right\rangle \\  & =\left\langle 2 u v,\,2 u v,\,2 u v\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 2 u v,\,2 u v,\,2 u v\right\rangle\cdot \left\langle v,\,-1,\,u\right\rangle \\  & =\left(2 u v\right)\cdot\left(v\right)+\left(2 u v\right)\cdot\left(-1\right)+\left(2 u v\right)\cdot\left(u\right) \\  & =\left(2 u v^{2}\right)+\left(- 2 u v\right)+\left(2 u^{2} v\right) \\  & =2 u^{2} v + 2 u v^{2} - 2 u v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 2 u^{2} v + 2 u v^{2} - 2 u v\,\mathrm{d}A.\end{aligned}
$$


## Generated authored-default variant q-161383

### bilinear_hint — easy
Author metadata: authored_cofactor; parameters `{'a': 4, 'b': 4, 'c': 4, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 4 x z,\,4 y,\,4 x z\right\rangle,\quad r(u,v)=\left\langle u,\,u v,\,v\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

*Hint: You can use the fact that $r'_u\times r'_v=\left\langle v,\,-1,\,u\right\rangle.$*

- $4 u^{2} v + 4 u v^{2} + 4 u v$
- $4 u^{2} v + 4 u v^{2} - 4 u v$ **correct**
- $- 4 u^{2} v - 4 u v^{2} + 4 u v$
- $12 u v$
- $4 u^{2} + 4 u v - 4 v$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
r'_u\times r'_v=\left\langle v,\,-1,\,u\right\rangle.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 4 x z,\,4 y,\,4 x z\right\rangle\big|_{x=u,\,y=u v,\,z=v} \\  & =\left\langle 4 \left(u\right) \left(v\right),\,4 \left(u v\right),\,4 \left(u\right) \left(v\right)\right\rangle \\  & =\left\langle 4 u v,\,4 u v,\,4 u v\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 4 u v,\,4 u v,\,4 u v\right\rangle\cdot \left\langle v,\,-1,\,u\right\rangle \\  & =\left(4 u v\right)\cdot\left(v\right)+\left(4 u v\right)\cdot\left(-1\right)+\left(4 u v\right)\cdot\left(u\right) \\  & =\left(4 u v^{2}\right)+\left(- 4 u v\right)+\left(4 u^{2} v\right) \\  & =4 u^{2} v + 4 u v^{2} - 4 u v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 4 u^{2} v + 4 u v^{2} - 4 u v\,\mathrm{d}A.\end{aligned}
$$


## Generated authored-default variant q-161383

### bilinear_hint — easy
Author metadata: authored_cofactor; parameters `{'a': 1, 'b': 3, 'c': 3, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle x z,\,3 y,\,3 x z\right\rangle,\quad r(u,v)=\left\langle u,\,u v,\,v\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

*Hint: You can use the fact that $r'_u\times r'_v=\left\langle v,\,-1,\,u\right\rangle.$*

- $3 u^{2} + u v - 3 v$
- $3 u^{2} v + u v^{2} + 3 u v$
- $- 3 u^{2} v - u v^{2} + 3 u v$
- $3 u^{2} v + u v^{2} - 3 u v$ **correct**
- $7 u v$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

Notice we are told that the fundamental vector product for our surface is

$$
r'_u\times r'_v=\left\langle v,\,-1,\,u\right\rangle.
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle x z,\,3 y,\,3 x z\right\rangle\big|_{x=u,\,y=u v,\,z=v} \\  & =\left\langle \left(u\right) \left(v\right),\,3 \left(u v\right),\,3 \left(u\right) \left(v\right)\right\rangle \\  & =\left\langle u v,\,3 u v,\,3 u v\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle u v,\,3 u v,\,3 u v\right\rangle\cdot \left\langle v,\,-1,\,u\right\rangle \\  & =\left(u v\right)\cdot\left(v\right)+\left(3 u v\right)\cdot\left(-1\right)+\left(3 u v\right)\cdot\left(u\right) \\  & =\left(u v^{2}\right)+\left(- 3 u v\right)+\left(3 u^{2} v\right) \\  & =3 u^{2} v + u v^{2} - 3 u v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 3 u^{2} v + u v^{2} - 3 u v\,\mathrm{d}A.\end{aligned}
$$


## Original q-161304

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=⟨{x}^{2},\,xy,\,z⟩,\,r(u,v)=⟨u,\,v,\,2uv⟩,\,(u,v)\in D⊂{R}^{2}.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}auv+b{u}^{2}v\,\text{d}A
$$

what is the value of $a+b?$


Original complete bank:

- $3$

- $-2$ **correct**

- $-4$

- $0$

- $1$


Original worked solution:

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}2uv)⟩ \\  & =⟨1,\,0,\,2v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(2uv)⟩ \\  & =⟨0,\,1,\,2u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 2v \\ 0 & 1 & 2u\end{aligned}| \\  & =⟨|\begin{aligned}0 & 2v \\ 1 & 2u\end{aligned}|,\,-|\begin{aligned}1 & 2v \\ 0 & 2u\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-2v,\,-2u,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨{x}^{2},\,xy,\,z⟩{|}_{x=u\,y=v\,z=2uv} \\  & =⟨{u}^{2},\,uv,\,2uv⟩.\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨{u}^{2},\,uv,\,2uv⟩\cdot ⟨-2v,\,-2u,\,1⟩ \\  & ={u}^{2}\cdot (-2v)+uv\cdot (-2u)+2uv\cdot 1 \\  & =-2{u}^{2}v-2{u}^{2}v+2uv \\  & =2uv-4{u}^{2}v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}2\cdot uv+(-4)\cdot {u}^{2}v\,\text{d}A.\end{aligned}
$$

Finally, 

$$
a+b=2-4=-2.
$$


## Parameterized source replay q-161304

### graph_sum — moderate
Author metadata: observed; parameters `{'a': 1, 'b': 1, 'c': 1, 'h': 2, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle x^{2},\,x y,\,z\right\rangle,\quad r(u,v)=\left\langle u,\,v,\,2 u v\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D a u v + b u^{2} v\,\mathrm{d}A
$$

what is the value of $a+b?$

- $-4$
- $-2$ **correct**
- $3$
- $1$
- $0$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}r'_u & =\left\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\right\rangle \\  & =\left\langle \frac{\partial}{\partial u}(u),\,\frac{\partial}{\partial u}(v),\,\frac{\partial}{\partial u}(2 u v)\right\rangle \\  & =\left\langle 1,\,0,\,2 v\right\rangle \\ r'_v & =\left\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\right\rangle \\  & =\left\langle \frac{\partial}{\partial v}(u),\,\frac{\partial}{\partial v}(v),\,\frac{\partial}{\partial v}(2 u v)\right\rangle \\  & =\left\langle 0,\,1,\,2 u\right\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}r'_u\times r'_v & =\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\1&0&2 v\\0&1&2 u\end{vmatrix} \\  & =\left\langle \begin{vmatrix}0&2 v\\1&2 u\end{vmatrix},-\begin{vmatrix}1&2 v\\0&2 u\end{vmatrix},\begin{vmatrix}1&0\\0&1\end{vmatrix}\right\rangle \\  & =\left\langle - 2 v,\,- 2 u,\,1\right\rangle.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle x^{2},\,x y,\,z\right\rangle\big|_{x=u,\,y=v,\,z=2 u v} \\  & =\left\langle \left(u\right)^{2},\,\left(u\right) \left(v\right),\,\left(2 u v\right)\right\rangle \\  & =\left\langle u^{2},\,u v,\,2 u v\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle u^{2},\,u v,\,2 u v\right\rangle\cdot \left\langle - 2 v,\,- 2 u,\,1\right\rangle \\  & =\left(u^{2}\right)\cdot\left(- 2 v\right)+\left(u v\right)\cdot\left(- 2 u\right)+\left(2 u v\right)\cdot\left(1\right) \\  & =\left(- 2 u^{2} v\right)+\left(- 2 u^{2} v\right)+\left(2 u v\right) \\  & =- 4 u^{2} v + 2 u v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D - 4 u^{2} v + 2 u v\,\mathrm{d}A.\end{aligned}
$$

Finally, 

$$
a+b=(2)+(-4)=-2.
$$


## Generated observed-pattern bank variation q-161304

### graph_sum — moderate
Author metadata: observed; parameters `{'a': 1, 'b': 1, 'c': 1, 'h': 2, 'scale': 2}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 2 x^{2},\,2 x y,\,2 z\right\rangle,\quad r(u,v)=\left\langle u,\,v,\,2 u v\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D a u v + b u^{2} v\,\mathrm{d}A
$$

what is the value of $a+b?$

- $-8$
- $-4$ **correct**
- $6$
- $2$
- $0$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}r'_u & =\left\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\right\rangle \\  & =\left\langle \frac{\partial}{\partial u}(u),\,\frac{\partial}{\partial u}(v),\,\frac{\partial}{\partial u}(2 u v)\right\rangle \\  & =\left\langle 1,\,0,\,2 v\right\rangle \\ r'_v & =\left\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\right\rangle \\  & =\left\langle \frac{\partial}{\partial v}(u),\,\frac{\partial}{\partial v}(v),\,\frac{\partial}{\partial v}(2 u v)\right\rangle \\  & =\left\langle 0,\,1,\,2 u\right\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}r'_u\times r'_v & =\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\1&0&2 v\\0&1&2 u\end{vmatrix} \\  & =\left\langle \begin{vmatrix}0&2 v\\1&2 u\end{vmatrix},-\begin{vmatrix}1&2 v\\0&2 u\end{vmatrix},\begin{vmatrix}1&0\\0&1\end{vmatrix}\right\rangle \\  & =\left\langle - 2 v,\,- 2 u,\,1\right\rangle.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 2 x^{2},\,2 x y,\,2 z\right\rangle\big|_{x=u,\,y=v,\,z=2 u v} \\  & =\left\langle 2 \left(u\right)^{2},\,2 \left(u\right) \left(v\right),\,2 \left(2 u v\right)\right\rangle \\  & =\left\langle 2 u^{2},\,2 u v,\,4 u v\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 2 u^{2},\,2 u v,\,4 u v\right\rangle\cdot \left\langle - 2 v,\,- 2 u,\,1\right\rangle \\  & =\left(2 u^{2}\right)\cdot\left(- 2 v\right)+\left(2 u v\right)\cdot\left(- 2 u\right)+\left(4 u v\right)\cdot\left(1\right) \\  & =\left(- 4 u^{2} v\right)+\left(- 4 u^{2} v\right)+\left(4 u v\right) \\  & =- 8 u^{2} v + 4 u v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D - 8 u^{2} v + 4 u v\,\mathrm{d}A.\end{aligned}
$$

Finally, 

$$
a+b=(4)+(-8)=-4.
$$


## Generated authored-default variant q-161304

### graph_sum — moderate
Author metadata: authored_tangents; parameters `{'a': 4, 'b': 4, 'c': 4, 'h': 2, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 4 x^{2},\,4 x y,\,4 z\right\rangle,\quad r(u,v)=\left\langle u,\,v,\,2 u v\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D a u v + b u^{2} v\,\mathrm{d}A
$$

what is the value of $a+b?$

- $0$
- $-8$ **correct**
- $8$
- $-16$
- $20$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}r'_u & =\left\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\right\rangle \\  & =\left\langle \frac{\partial}{\partial u}(u),\,\frac{\partial}{\partial u}(v),\,\frac{\partial}{\partial u}(2 u v)\right\rangle \\  & =\left\langle 1,\,0,\,2 v\right\rangle \\ r'_v & =\left\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\right\rangle \\  & =\left\langle \frac{\partial}{\partial v}(u),\,\frac{\partial}{\partial v}(v),\,\frac{\partial}{\partial v}(2 u v)\right\rangle \\  & =\left\langle 0,\,1,\,2 u\right\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}r'_u\times r'_v & =\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\1&0&2 v\\0&1&2 u\end{vmatrix} \\  & =\left\langle \begin{vmatrix}0&2 v\\1&2 u\end{vmatrix},-\begin{vmatrix}1&2 v\\0&2 u\end{vmatrix},\begin{vmatrix}1&0\\0&1\end{vmatrix}\right\rangle \\  & =\left\langle - 2 v,\,- 2 u,\,1\right\rangle.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 4 x^{2},\,4 x y,\,4 z\right\rangle\big|_{x=u,\,y=v,\,z=2 u v} \\  & =\left\langle 4 \left(u\right)^{2},\,4 \left(u\right) \left(v\right),\,4 \left(2 u v\right)\right\rangle \\  & =\left\langle 4 u^{2},\,4 u v,\,8 u v\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 4 u^{2},\,4 u v,\,8 u v\right\rangle\cdot \left\langle - 2 v,\,- 2 u,\,1\right\rangle \\  & =\left(4 u^{2}\right)\cdot\left(- 2 v\right)+\left(4 u v\right)\cdot\left(- 2 u\right)+\left(8 u v\right)\cdot\left(1\right) \\  & =\left(- 8 u^{2} v\right)+\left(- 8 u^{2} v\right)+\left(8 u v\right) \\  & =- 16 u^{2} v + 8 u v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D - 16 u^{2} v + 8 u v\,\mathrm{d}A.\end{aligned}
$$

Finally, 

$$
a+b=(8)+(-16)=-8.
$$


## Generated authored-default variant q-161304

### graph_sum — moderate
Author metadata: authored_tangents; parameters `{'a': 1, 'b': 3, 'c': 3, 'h': 1, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle x^{2},\,3 x y,\,3 z\right\rangle,\quad r(u,v)=\left\langle u,\,v,\,u v\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D a u v + b u^{2} v\,\mathrm{d}A
$$

what is the value of $a+b?$

- $6$
- $0$
- $1$
- $-1$ **correct**
- $-4$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}r'_u & =\left\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\right\rangle \\  & =\left\langle \frac{\partial}{\partial u}(u),\,\frac{\partial}{\partial u}(v),\,\frac{\partial}{\partial u}(u v)\right\rangle \\  & =\left\langle 1,\,0,\,v\right\rangle \\ r'_v & =\left\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\right\rangle \\  & =\left\langle \frac{\partial}{\partial v}(u),\,\frac{\partial}{\partial v}(v),\,\frac{\partial}{\partial v}(u v)\right\rangle \\  & =\left\langle 0,\,1,\,u\right\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}r'_u\times r'_v & =\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\1&0&v\\0&1&u\end{vmatrix} \\  & =\left\langle \begin{vmatrix}0&v\\1&u\end{vmatrix},-\begin{vmatrix}1&v\\0&u\end{vmatrix},\begin{vmatrix}1&0\\0&1\end{vmatrix}\right\rangle \\  & =\left\langle - v,\,- u,\,1\right\rangle.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle x^{2},\,3 x y,\,3 z\right\rangle\big|_{x=u,\,y=v,\,z=u v} \\  & =\left\langle \left(u\right)^{2},\,3 \left(u\right) \left(v\right),\,3 \left(u v\right)\right\rangle \\  & =\left\langle u^{2},\,3 u v,\,3 u v\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle u^{2},\,3 u v,\,3 u v\right\rangle\cdot \left\langle - v,\,- u,\,1\right\rangle \\  & =\left(u^{2}\right)\cdot\left(- v\right)+\left(3 u v\right)\cdot\left(- u\right)+\left(3 u v\right)\cdot\left(1\right) \\  & =\left(- u^{2} v\right)+\left(- 3 u^{2} v\right)+\left(3 u v\right) \\  & =- 4 u^{2} v + 3 u v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D - 4 u^{2} v + 3 u v\,\mathrm{d}A.\end{aligned}
$$

Finally, 

$$
a+b=(3)+(-4)=-1.
$$


## Generated authored missing-hard variant

### polar_unhinted — hard
Author metadata: authored_cofactor; parameters `{'a': 2, 'b': 4, 'c': 2, 'h': 1, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 2 x,\,4 y,\,2 z\right\rangle,\quad r(u,v)=\left\langle u \cos{\left(v \right)},\,u \sin{\left(v \right)},\,u^{2}\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0,\ 0<v<2\pi\}$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

- $12 u^{3} \sin^{2}{\left(v \right)} - 2 u^{3}$
- $- 4 u^{3} \sin^{2}{\left(v \right)} - 2 u^{3}$ **correct**
- $4 u^{3} \sin^{2}{\left(v \right)} + 2 u^{3}$
- $2 u^{2} + 4 u \sin{\left(v \right)} + 2 u \cos{\left(v \right)}$
- $- 4 u^{3} \cos{\left(v \right)} - 8 u^{2} v \sin{\left(v \right)} + 2 u$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}r'_u & =\left\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\right\rangle \\  & =\left\langle \frac{\partial}{\partial u}(u \cos{\left(v \right)}),\,\frac{\partial}{\partial u}(u \sin{\left(v \right)}),\,\frac{\partial}{\partial u}(u^{2})\right\rangle \\  & =\left\langle \cos{\left(v \right)},\,\sin{\left(v \right)},\,2 u\right\rangle \\ r'_v & =\left\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\right\rangle \\  & =\left\langle \frac{\partial}{\partial v}(u \cos{\left(v \right)}),\,\frac{\partial}{\partial v}(u \sin{\left(v \right)}),\,\frac{\partial}{\partial v}(u^{2})\right\rangle \\  & =\left\langle - u \sin{\left(v \right)},\,u \cos{\left(v \right)},\,0\right\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}r'_u\times r'_v & =\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\\cos{\left(v \right)}&\sin{\left(v \right)}&2 u\\- u \sin{\left(v \right)}&u \cos{\left(v \right)}&0\end{vmatrix} \\  & =\left\langle \begin{vmatrix}\sin{\left(v \right)}&2 u\\u \cos{\left(v \right)}&0\end{vmatrix},-\begin{vmatrix}\cos{\left(v \right)}&2 u\\- u \sin{\left(v \right)}&0\end{vmatrix},\begin{vmatrix}\cos{\left(v \right)}&\sin{\left(v \right)}\\- u \sin{\left(v \right)}&u \cos{\left(v \right)}\end{vmatrix}\right\rangle \\  & =\left\langle - 2 u^{2} \cos{\left(v \right)},\,- 2 u^{2} \sin{\left(v \right)},\,u\right\rangle.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle 2 x,\,4 y,\,2 z\right\rangle\big|_{x=u \cos{\left(v \right)},\,y=u \sin{\left(v \right)},\,z=u^{2}} \\  & =\left\langle 2 \left(u \cos{\left(v \right)}\right),\,4 \left(u \sin{\left(v \right)}\right),\,2 \left(u^{2}\right)\right\rangle \\  & =\left\langle 2 u \cos{\left(v \right)},\,4 u \sin{\left(v \right)},\,2 u^{2}\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 2 u \cos{\left(v \right)},\,4 u \sin{\left(v \right)},\,2 u^{2}\right\rangle\cdot \left\langle - 2 u^{2} \cos{\left(v \right)},\,- 2 u^{2} \sin{\left(v \right)},\,u\right\rangle \\  & =\left(2 u \cos{\left(v \right)}\right)\cdot\left(- 2 u^{2} \cos{\left(v \right)}\right)+\left(4 u \sin{\left(v \right)}\right)\cdot\left(- 2 u^{2} \sin{\left(v \right)}\right)+\left(2 u^{2}\right)\cdot\left(u\right) \\  & =\left(4 u^{3} \sin^{2}{\left(v \right)} - 4 u^{3}\right)+\left(- 8 u^{3} \sin^{2}{\left(v \right)}\right)+\left(2 u^{3}\right) \\  & =- 4 u^{3} \sin^{2}{\left(v \right)} - 2 u^{3}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D - 4 u^{3} \sin^{2}{\left(v \right)} - 2 u^{3}\,\mathrm{d}A.\end{aligned}
$$


## Generated authored missing-hard variant

### polar_unhinted — hard
Author metadata: authored_cofactor; parameters `{'a': 1, 'b': 3, 'c': 3, 'h': 1, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle x,\,3 y,\,3 z\right\rangle,\quad r(u,v)=\left\langle u \cos{\left(v \right)},\,u \sin{\left(v \right)},\,u^{2}\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0,\ 0<v<2\pi\}$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

- $- 2 u^{3} \cos{\left(v \right)} - 6 u^{2} v \sin{\left(v \right)} + 3 u$
- $8 u^{3} \sin^{2}{\left(v \right)} + u^{3}$
- $4 u^{3} \sin^{2}{\left(v \right)} - u^{3}$
- $- 4 u^{3} \sin^{2}{\left(v \right)} + u^{3}$ **correct**
- $3 u^{2} + 3 u \sin{\left(v \right)} + u \cos{\left(v \right)}$

Worked solution:
For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_S F\cdot n\,\mathrm{d}S=\iint_D F(r(u,v))\cdot (r'_u\times r'_v)\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}r'_u & =\left\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\right\rangle \\  & =\left\langle \frac{\partial}{\partial u}(u \cos{\left(v \right)}),\,\frac{\partial}{\partial u}(u \sin{\left(v \right)}),\,\frac{\partial}{\partial u}(u^{2})\right\rangle \\  & =\left\langle \cos{\left(v \right)},\,\sin{\left(v \right)},\,2 u\right\rangle \\ r'_v & =\left\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\right\rangle \\  & =\left\langle \frac{\partial}{\partial v}(u \cos{\left(v \right)}),\,\frac{\partial}{\partial v}(u \sin{\left(v \right)}),\,\frac{\partial}{\partial v}(u^{2})\right\rangle \\  & =\left\langle - u \sin{\left(v \right)},\,u \cos{\left(v \right)},\,0\right\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}r'_u\times r'_v & =\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\\cos{\left(v \right)}&\sin{\left(v \right)}&2 u\\- u \sin{\left(v \right)}&u \cos{\left(v \right)}&0\end{vmatrix} \\  & =\left\langle \begin{vmatrix}\sin{\left(v \right)}&2 u\\u \cos{\left(v \right)}&0\end{vmatrix},-\begin{vmatrix}\cos{\left(v \right)}&2 u\\- u \sin{\left(v \right)}&0\end{vmatrix},\begin{vmatrix}\cos{\left(v \right)}&\sin{\left(v \right)}\\- u \sin{\left(v \right)}&u \cos{\left(v \right)}\end{vmatrix}\right\rangle \\  & =\left\langle - 2 u^{2} \cos{\left(v \right)},\,- 2 u^{2} \sin{\left(v \right)},\,u\right\rangle.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =\left\langle x,\,3 y,\,3 z\right\rangle\big|_{x=u \cos{\left(v \right)},\,y=u \sin{\left(v \right)},\,z=u^{2}} \\  & =\left\langle \left(u \cos{\left(v \right)}\right),\,3 \left(u \sin{\left(v \right)}\right),\,3 \left(u^{2}\right)\right\rangle \\  & =\left\langle u \cos{\left(v \right)},\,3 u \sin{\left(v \right)},\,3 u^{2}\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle u \cos{\left(v \right)},\,3 u \sin{\left(v \right)},\,3 u^{2}\right\rangle\cdot \left\langle - 2 u^{2} \cos{\left(v \right)},\,- 2 u^{2} \sin{\left(v \right)},\,u\right\rangle \\  & =\left(u \cos{\left(v \right)}\right)\cdot\left(- 2 u^{2} \cos{\left(v \right)}\right)+\left(3 u \sin{\left(v \right)}\right)\cdot\left(- 2 u^{2} \sin{\left(v \right)}\right)+\left(3 u^{2}\right)\cdot\left(u\right) \\  & =\left(2 u^{3} \sin^{2}{\left(v \right)} - 2 u^{3}\right)+\left(- 6 u^{3} \sin^{2}{\left(v \right)}\right)+\left(3 u^{3}\right) \\  & =- 4 u^{3} \sin^{2}{\left(v \right)} + u^{3}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D - 4 u^{3} \sin^{2}{\left(v \right)} + u^{3}\,\mathrm{d}A.\end{aligned}
$$


## Generated authored missing-hard variant

### exponential_unhinted — hard
Author metadata: authored_cofactor; parameters `{'a': 4, 'b': 2, 'c': 1, 'p': 4, 'q': 3, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle 4 x - \frac{4}{z},\,2 y + \frac{3}{z},\,z\right\rangle,\quad r(u,v)=\left\langle u e^{v},\,u e^{- v},\,u\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0\}$, so the vector field is defined on $S$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

- $- 3 e^{v} - 4 e^{- v}$
- $4 u^{2} + 3 e^{v} - 4 e^{- v}$ **correct**
- $- 4 u^{2} - 3 e^{v} + 4 e^{- v}$
- $4 u e^{v} + u + 2 u e^{- v} - \frac{1}{u}$
- $4 u^{2} e^{- v} + 2 u v e^{v} + 3 u e^{v} - 2 u - 4 u e^{- v}$

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
\begin{aligned}F(r(u,v)) & =\left\langle 4 x - \frac{4}{z},\,2 y + \frac{3}{z},\,z\right\rangle\big|_{x=u e^{v},\,y=u e^{- v},\,z=u} \\  & =\left\langle 4 \left(u e^{v}\right) - \frac{4}{\left(u\right)},\,2 \left(u e^{- v}\right) + \frac{3}{\left(u\right)},\,\left(u\right)\right\rangle \\  & =\left\langle 4 u e^{v} - \frac{4}{u},\,2 u e^{- v} + \frac{3}{u},\,u\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle 4 u e^{v} - \frac{4}{u},\,2 u e^{- v} + \frac{3}{u},\,u\right\rangle\cdot \left\langle u e^{- v},\,u e^{v},\,- 2 u\right\rangle \\  & =\left(4 u e^{v} - \frac{4}{u}\right)\cdot\left(u e^{- v}\right)+\left(2 u e^{- v} + \frac{3}{u}\right)\cdot\left(u e^{v}\right)+\left(u\right)\cdot\left(- 2 u\right) \\  & =\left(4 u^{2} - 4 e^{- v}\right)+\left(2 u^{2} + 3 e^{v}\right)+\left(- 2 u^{2}\right) \\  & =4 u^{2} + 3 e^{v} - 4 e^{- v}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D 4 u^{2} + 3 e^{v} - 4 e^{- v}\,\mathrm{d}A.\end{aligned}
$$


## Generated authored missing-hard variant

### exponential_unhinted — hard
Author metadata: authored_cofactor; parameters `{'a': 1, 'b': 3, 'c': 3, 'p': 1, 'q': 3, 'scale': 1}`.

Consider the vector field $F$ and the surface $S$ with parametrization $r(u,v),$ where

$$
F(x,y,z)=\left\langle x - \frac{1}{z},\,3 y + \frac{3}{z},\,3 z\right\rangle,\quad r(u,v)=\left\langle u e^{v},\,u e^{- v},\,u\right\rangle,\quad (u,v)\in D\subset\mathbb R^2.
$$

Assume $D\subset\{(u,v):u>0\}$, so the vector field is defined on $S$.

If the flux of $F$ across $S$ with respect to $n$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf S=\iint_D \boxed{}\,\mathrm{d}A
$$

what is the missing expression?

- $u^{2} e^{- v} + 3 u v e^{v} + 3 u e^{v} - 6 u - u e^{- v}$
- $- 8 u^{2} - 3 e^{v} - e^{- v}$
- $2 u^{2} - 3 e^{v} + e^{- v}$
- $- 2 u^{2} + 3 e^{v} - e^{- v}$ **correct**
- $u e^{v} + 3 u + 3 u e^{- v} + \frac{2}{u}$

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
\begin{aligned}F(r(u,v)) & =\left\langle x - \frac{1}{z},\,3 y + \frac{3}{z},\,3 z\right\rangle\big|_{x=u e^{v},\,y=u e^{- v},\,z=u} \\  & =\left\langle \left(u e^{v}\right) - \frac{1}{\left(u\right)},\,3 \left(u e^{- v}\right) + \frac{3}{\left(u\right)},\,3 \left(u\right)\right\rangle \\  & =\left\langle u e^{v} - \frac{1}{u},\,3 u e^{- v} + \frac{3}{u},\,3 u\right\rangle\end{aligned}
$$

Finally, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot (r'_u\times r'_v) & =\left\langle u e^{v} - \frac{1}{u},\,3 u e^{- v} + \frac{3}{u},\,3 u\right\rangle\cdot \left\langle u e^{- v},\,u e^{v},\,- 2 u\right\rangle \\  & =\left(u e^{v} - \frac{1}{u}\right)\cdot\left(u e^{- v}\right)+\left(3 u e^{- v} + \frac{3}{u}\right)\cdot\left(u e^{v}\right)+\left(3 u\right)\cdot\left(- 2 u\right) \\  & =\left(u^{2} - e^{- v}\right)+\left(3 u^{2} + 3 e^{v}\right)+\left(- 6 u^{2}\right) \\  & =- 2 u^{2} + 3 e^{v} - e^{- v}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}\iint_S F\cdot\mathrm{d}\mathbf S & =\iint_D F(r(u,v))\cdot(r'_u\times r'_v)\,\mathrm{d}A \\  & =\iint_D - 2 u^{2} + 3 e^{v} - e^{- v}\,\mathrm{d}A.\end{aligned}
$$