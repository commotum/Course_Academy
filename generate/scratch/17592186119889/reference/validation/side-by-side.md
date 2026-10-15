# q-105613

## Original

$$
{∬}_{D}\boxed{}\,\text{d}A,\,D={(u,v)\,:\,0\le u\le 1,\,0\le v\le \pi }
$$

The integral above gives the surface area of the parametric surface $r(u,v)=⟨2u\operatorname{sin}⁡v,\,3u\operatorname{cos}⁡v,\,u⟩$ for $0\le u\le 1$ and $0\le v\le \pi .$ What is the missing expression?

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(2u\operatorname{sin}⁡v),\,\frac{∂}{∂u}(3u\operatorname{cos}⁡v),\,\frac{∂}{∂u}(u)⟩ \\  & =⟨2\operatorname{sin}⁡v,\,3\operatorname{cos}⁡v,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(2u\operatorname{sin}⁡v),\,\frac{∂}{∂v}(3u\operatorname{cos}⁡v),\,\frac{∂}{∂v}(u)⟩ \\  & =⟨2u\operatorname{cos}⁡v,\,-3u\operatorname{sin}⁡v,\,0⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2\operatorname{sin}⁡v & 3\operatorname{cos}⁡v & 1 \\ 2u\operatorname{cos}⁡v & -3u\operatorname{sin}⁡v & 0\end{aligned}| \\  & =⟨|\begin{aligned}3\operatorname{cos}⁡v & 1 \\ -3u\operatorname{sin}⁡v & 0\end{aligned}|,\,-|\begin{aligned}2\operatorname{sin}⁡v & 1 \\ 2u\operatorname{cos}⁡v & 0\end{aligned}|,\,|\begin{aligned}2\operatorname{sin}⁡v & 3\operatorname{cos}⁡v \\ 2u\operatorname{cos}⁡v & -3u\operatorname{sin}⁡v\end{aligned}|⟩ \\  & =⟨3u\operatorname{sin}⁡v,\,2u\operatorname{cos}⁡v,\,-6u{sin}^{2}⁡v-6u{cos}^{2}⁡v⟩ \\  & =⟨3u\operatorname{sin}⁡v,\,2u\operatorname{cos}⁡v,\,-6u⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨3u\operatorname{sin}⁡v,\,2u\operatorname{cos}⁡v,\,-6u⟩‖ \\  & =\sqrt{(3u\operatorname{sin}⁡v)^{2}+(2u\operatorname{cos}⁡v)^{2}+(-6u)^{2}} \\  & =\sqrt{9{u}^{2}{sin}^{2}⁡v+4{u}^{2}{cos}^{2}⁡v+36{u}^{2}} \\  & =\sqrt{(5{u}^{2}{sin}^{2}⁡v+4{u}^{2}{sin}^{2}⁡v)+4{u}^{2}{cos}^{2}⁡v+36{u}^{2}} \\  & =\sqrt{5{u}^{2}{sin}^{2}⁡v+4{u}^{2}({sin}^{2}⁡v+{cos}^{2}⁡v)+36{u}^{2}} \\  & =\sqrt{5{u}^{2}{sin}^{2}⁡v+4{u}^{2}+36{u}^{2}} \\  & =\sqrt{5{u}^{2}{sin}^{2}⁡v+40{u}^{2}} \\  & =\sqrt{5{u}^{2}({sin}^{2}⁡v+8)} \\  & =\sqrt{5{u}^{2}}\sqrt{{sin}^{2}⁡v+8} \\  & =\sqrt{5}u\sqrt{{sin}^{2}⁡v+8}.\end{aligned}
$$

Notice that $\sqrt{{u}^{2}}=u$ since $u\ge 0$ on $D.$

Therefore, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\sqrt{5}u\sqrt{{sin}^{2}⁡v+8}\,\text{d}A\end{aligned}
$$

## replay

$$
\iint_D\boxed{}\,\mathrm{d}A,\quad D=\{(u,v):0\le u\le 1,\,0\le v\le \pi\}
$$

The integral above gives the surface area of the parametric surface $r(u,v)=\langle 2 u \sin{\left(v \right)},\,3 u \cos{\left(v \right)},\,u\rangle$ for $0\le u\le 1,\,0\le v\le \pi.$ What is the missing expression?

{'a': 2}

- $6 \sqrt{u^{2} \sin^{2}{\left(v \right)} + u^{2} + 1}$

- $\sqrt{u^{2} + 36}$

- $u \sqrt{5 \sin^{2}{\left(v \right)} + 40}$

- $\sqrt{3 u^{2} \cos^{2}{\left(v \right)} + 4 u^{2} + 36}$

- $6 \sqrt{u^{2} + 1}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
\iint_S\mathrm{d}S=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}\mathbf r_u &=\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\rangle \\  &=\langle \frac{\partial}{\partial u}\left(2 u \sin{\left(v \right)}\right),\,\frac{\partial}{\partial u}\left(3 u \cos{\left(v \right)}\right),\,\frac{\partial}{\partial u}\left(u\right)\rangle \\  &=\langle 2 \sin{\left(v \right)},\,3 \cos{\left(v \right)},\,1\rangle \\ \mathbf r_v &=\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\rangle \\  &=\langle \frac{\partial}{\partial v}\left(2 u \sin{\left(v \right)}\right),\,\frac{\partial}{\partial v}\left(3 u \cos{\left(v \right)}\right),\,\frac{\partial}{\partial v}\left(u\right)\rangle \\  &=\langle 2 u \cos{\left(v \right)},\,- 3 u \sin{\left(v \right)},\,0\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}\mathbf r_u\times\mathbf r_v &=\begin{vmatrix}i & j & k \\ 2 \sin{\left(v \right)} & 3 \cos{\left(v \right)} & 1 \\ 2 u \cos{\left(v \right)} & - 3 u \sin{\left(v \right)} & 0\end{vmatrix} \\  &=\langle \begin{vmatrix}3 \cos{\left(v \right)} & 1 \\ - 3 u \sin{\left(v \right)} & 0\end{vmatrix},\,-\begin{vmatrix}2 \sin{\left(v \right)} & 1 \\ 2 u \cos{\left(v \right)} & 0\end{vmatrix},\,\begin{vmatrix}2 \sin{\left(v \right)} & 3 \cos{\left(v \right)} \\ 2 u \cos{\left(v \right)} & - 3 u \sin{\left(v \right)}\end{vmatrix}\rangle \\  &=\langle 3 u \sin{\left(v \right)},\,2 u \cos{\left(v \right)},\,- 6 u \sin^{2}{\left(v \right)} - 6 u \cos^{2}{\left(v \right)}\rangle \\  &=\langle 3 u \sin{\left(v \right)},\,2 u \cos{\left(v \right)},\,- 6 u\rangle\end{aligned}
$$

and

$$
\begin{aligned}\left\|\mathbf r_u\times\mathbf r_v\right\| &=\left\|\langle 3 u \sin{\left(v \right)},\,2 u \cos{\left(v \right)},\,- 6 u\rangle\right\| \\  &=\sqrt{\left(3 u \sin{\left(v \right)}\right)^2+\left(2 u \cos{\left(v \right)}\right)^2+\left(- 6 u\right)^2} \\  &=\sqrt{9 u^{2} \sin^{2}{\left(v \right)}+4 u^{2} \cos^{2}{\left(v \right)}+36 u^{2}} \\  &=\sqrt{5 u^{2} \sin^{2}{\left(v \right)}+4 u^{2}\left(\sin^2 v+\cos^2 v\right)+36 u^{2}} \\  &=\sqrt{5 u^{2} \sin^{2}{\left(v \right)} + 40 u^{2}} \\  &=\sqrt{u^{2} \left(5 \sin^{2}{\left(v \right)} + 40\right)} \\  &=\sqrt{u^{2}}\sqrt{5 \sin^{2}{\left(v \right)} + 40} \\  &=u \sqrt{5 \sin^{2}{\left(v \right)} + 40}\end{aligned}
$$

Notice that $\sqrt{u^2}=u$ since $u\ge 0$ on $D.$

Therefore, the surface area is

$$
\begin{aligned}\iint_S\mathrm{d}S &=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A \\  &=\iint_D u \sqrt{5 \sin^{2}{\left(v \right)} + 40}\,\mathrm{d}A\end{aligned}
$$

## variant

$$
\iint_D\boxed{}\,\mathrm{d}A,\quad D=\{(u,v):0\le u\le 1,\,0\le v\le \pi\}
$$

The integral above gives the surface area of the parametric surface $r(u,v)=\langle 3 u \sin{\left(v \right)},\,4 u \cos{\left(v \right)},\,u\rangle$ for $0\le u\le 1,\,0\le v\le \pi.$ What is the missing expression?

{'a': 3}

- $12 \sqrt{u^{2} \sin^{2}{\left(v \right)} + u^{2} + 1}$

- $\sqrt{u^{2} + 144}$

- $\sqrt{4 u^{2} \cos^{2}{\left(v \right)} + 9 u^{2} + 144}$

- $12 \sqrt{u^{2} + 1}$

- $u \sqrt{7 \sin^{2}{\left(v \right)} + 153}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
\iint_S\mathrm{d}S=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}\mathbf r_u &=\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\rangle \\  &=\langle \frac{\partial}{\partial u}\left(3 u \sin{\left(v \right)}\right),\,\frac{\partial}{\partial u}\left(4 u \cos{\left(v \right)}\right),\,\frac{\partial}{\partial u}\left(u\right)\rangle \\  &=\langle 3 \sin{\left(v \right)},\,4 \cos{\left(v \right)},\,1\rangle \\ \mathbf r_v &=\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\rangle \\  &=\langle \frac{\partial}{\partial v}\left(3 u \sin{\left(v \right)}\right),\,\frac{\partial}{\partial v}\left(4 u \cos{\left(v \right)}\right),\,\frac{\partial}{\partial v}\left(u\right)\rangle \\  &=\langle 3 u \cos{\left(v \right)},\,- 4 u \sin{\left(v \right)},\,0\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}\mathbf r_u\times\mathbf r_v &=\begin{vmatrix}i & j & k \\ 3 \sin{\left(v \right)} & 4 \cos{\left(v \right)} & 1 \\ 3 u \cos{\left(v \right)} & - 4 u \sin{\left(v \right)} & 0\end{vmatrix} \\  &=\langle \begin{vmatrix}4 \cos{\left(v \right)} & 1 \\ - 4 u \sin{\left(v \right)} & 0\end{vmatrix},\,-\begin{vmatrix}3 \sin{\left(v \right)} & 1 \\ 3 u \cos{\left(v \right)} & 0\end{vmatrix},\,\begin{vmatrix}3 \sin{\left(v \right)} & 4 \cos{\left(v \right)} \\ 3 u \cos{\left(v \right)} & - 4 u \sin{\left(v \right)}\end{vmatrix}\rangle \\  &=\langle 4 u \sin{\left(v \right)},\,3 u \cos{\left(v \right)},\,- 12 u \sin^{2}{\left(v \right)} - 12 u \cos^{2}{\left(v \right)}\rangle \\  &=\langle 4 u \sin{\left(v \right)},\,3 u \cos{\left(v \right)},\,- 12 u\rangle\end{aligned}
$$

and

$$
\begin{aligned}\left\|\mathbf r_u\times\mathbf r_v\right\| &=\left\|\langle 4 u \sin{\left(v \right)},\,3 u \cos{\left(v \right)},\,- 12 u\rangle\right\| \\  &=\sqrt{\left(4 u \sin{\left(v \right)}\right)^2+\left(3 u \cos{\left(v \right)}\right)^2+\left(- 12 u\right)^2} \\  &=\sqrt{16 u^{2} \sin^{2}{\left(v \right)}+9 u^{2} \cos^{2}{\left(v \right)}+144 u^{2}} \\  &=\sqrt{7 u^{2} \sin^{2}{\left(v \right)}+9 u^{2}\left(\sin^2 v+\cos^2 v\right)+144 u^{2}} \\  &=\sqrt{7 u^{2} \sin^{2}{\left(v \right)} + 153 u^{2}} \\  &=\sqrt{u^{2} \left(7 \sin^{2}{\left(v \right)} + 153\right)} \\  &=\sqrt{u^{2}}\sqrt{7 \sin^{2}{\left(v \right)} + 153} \\  &=u \sqrt{7 \sin^{2}{\left(v \right)} + 153}\end{aligned}
$$

Notice that $\sqrt{u^2}=u$ since $u\ge 0$ on $D.$

Therefore, the surface area is

$$
\begin{aligned}\iint_S\mathrm{d}S &=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A \\  &=\iint_D u \sqrt{7 \sin^{2}{\left(v \right)} + 153}\,\mathrm{d}A\end{aligned}
$$

# q-109941

## Original

$$
{∬}_{D}\boxed{}\,\text{d}A,\,D={(u,v)\,:\,0\le u\le 2,\,0\le v\le 2}
$$

The integral above gives the surface area of the parametric surface $r(u,v)=⟨{u}^{2},\,u-{v}^{2},\,{v}^{2}⟩$ for $0\le u\le 2$ and $0\le v\le 2.$ What is the missing expression?

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}({u}^{2}),\,\frac{∂}{∂u}(u-{v}^{2}),\,\frac{∂}{∂u}({v}^{2})⟩ \\  & =⟨2u,\,1,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}({u}^{2}),\,\frac{∂}{∂v}(u-{v}^{2}),\,\frac{∂}{∂v}({v}^{2})⟩ \\  & =⟨0,\,-2v,\,2v⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2u & 1 & 0 \\ 0 & -2v & 2v\end{aligned}| \\  & =⟨|\begin{aligned}1 & 0 \\ -2v & 2v\end{aligned}|,\,-|\begin{aligned}2u & 0 \\ 0 & 2v\end{aligned}|,\,|\begin{aligned}2u & 1 \\ 0 & -2v\end{aligned}|⟩ \\  & =⟨2v,\,-4uv,\,-4uv⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨2v,\,-4uv,\,-4uv⟩‖ \\  & =\sqrt{(2v)^{2}+(-4uv)^{2}+(-4uv)^{2}} \\  & =\sqrt{4{v}^{2}+16{u}^{2}{v}^{2}+16{u}^{2}{v}^{2}} \\  & =\sqrt{4{v}^{2}+32{u}^{2}{v}^{2}} \\  & =\sqrt{4{v}^{2}(1+8{u}^{2})} \\  & =\sqrt{4{v}^{2}}\sqrt{1+8{u}^{2}} \\  & =2v\sqrt{1+8{u}^{2}}.\end{aligned}
$$

Notice that $\sqrt{{v}^{2}}=v$ since $v\ge 0$ on $D.$

Therefore, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}2v\sqrt{1+8{u}^{2}}\,\text{d}A\end{aligned}
$$

## replay

$$
\iint_D\boxed{}\,\mathrm{d}A,\quad D=\{(u,v):0\le u\le 2,\,0\le v\le 2\}
$$

The integral above gives the surface area of the parametric surface $r(u,v)=\langle u^{2},\,u - v^{2},\,v^{2}\rangle$ for $0\le u\le 2,\,0\le v\le 2.$ What is the missing expression?

{'a': 1}

- $\sqrt{- u^{2} + v^{2}}$

- $u \sqrt{4 v + 1}$

- $2 v \sqrt{8 u^{2} + 1}$

- $v^{2} \sqrt{4 u^{2} + 1}$

- $\sqrt{u^{2} + v^{2}}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
\iint_S\mathrm{d}S=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}\mathbf r_u &=\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\rangle \\  &=\langle \frac{\partial}{\partial u}\left(u^{2}\right),\,\frac{\partial}{\partial u}\left(u - v^{2}\right),\,\frac{\partial}{\partial u}\left(v^{2}\right)\rangle \\  &=\langle 2 u,\,1,\,0\rangle \\ \mathbf r_v &=\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\rangle \\  &=\langle \frac{\partial}{\partial v}\left(u^{2}\right),\,\frac{\partial}{\partial v}\left(u - v^{2}\right),\,\frac{\partial}{\partial v}\left(v^{2}\right)\rangle \\  &=\langle 0,\,- 2 v,\,2 v\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}\mathbf r_u\times\mathbf r_v &=\begin{vmatrix}i & j & k \\ 2 u & 1 & 0 \\ 0 & - 2 v & 2 v\end{vmatrix} \\  &=\langle \begin{vmatrix}1 & 0 \\ - 2 v & 2 v\end{vmatrix},\,-\begin{vmatrix}2 u & 0 \\ 0 & 2 v\end{vmatrix},\,\begin{vmatrix}2 u & 1 \\ 0 & - 2 v\end{vmatrix}\rangle \\  &=\langle 2 v,\,- 4 u v,\,- 4 u v\rangle\end{aligned}
$$

and

$$
\begin{aligned}\left\|\mathbf r_u\times\mathbf r_v\right\| &=\left\|\langle 2 v,\,- 4 u v,\,- 4 u v\rangle\right\| \\  &=\sqrt{\left(2 v\right)^2+\left(- 4 u v\right)^2+\left(- 4 u v\right)^2} \\  &=\sqrt{4 v^{2}+16 u^{2} v^{2}+16 u^{2} v^{2}} \\  &=\sqrt{32 u^{2} v^{2} + 4 v^{2}} \\  &=\sqrt{4 v^{2} \left(8 u^{2} + 1\right)} \\  &=\sqrt{4 v^{2}}\sqrt{8 u^{2} + 1} \\  &=2 v \sqrt{8 u^{2} + 1}\end{aligned}
$$

Notice that $\sqrt{v^2}=v$ since $v\ge 0$ on $D.$

Therefore, the surface area is

$$
\begin{aligned}\iint_S\mathrm{d}S &=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A \\  &=\iint_D 2 v \sqrt{8 u^{2} + 1}\,\mathrm{d}A\end{aligned}
$$

## variant

$$
\iint_D\boxed{}\,\mathrm{d}A,\quad D=\{(u,v):0\le u\le 2,\,0\le v\le 2\}
$$

The integral above gives the surface area of the parametric surface $r(u,v)=\langle 2 u^{2},\,u - v^{2},\,v^{2}\rangle$ for $0\le u\le 2,\,0\le v\le 2.$ What is the missing expression?

{'a': 2}

- $\sqrt{- 4 u^{2} + v^{2}}$

- $u \sqrt{16 v + 1}$

- $v^{2} \sqrt{16 u^{2} + 1}$

- $\sqrt{4 u^{2} + v^{2}}$

- $2 v \sqrt{32 u^{2} + 1}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
\iint_S\mathrm{d}S=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}\mathbf r_u &=\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\rangle \\  &=\langle \frac{\partial}{\partial u}\left(2 u^{2}\right),\,\frac{\partial}{\partial u}\left(u - v^{2}\right),\,\frac{\partial}{\partial u}\left(v^{2}\right)\rangle \\  &=\langle 4 u,\,1,\,0\rangle \\ \mathbf r_v &=\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\rangle \\  &=\langle \frac{\partial}{\partial v}\left(2 u^{2}\right),\,\frac{\partial}{\partial v}\left(u - v^{2}\right),\,\frac{\partial}{\partial v}\left(v^{2}\right)\rangle \\  &=\langle 0,\,- 2 v,\,2 v\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}\mathbf r_u\times\mathbf r_v &=\begin{vmatrix}i & j & k \\ 4 u & 1 & 0 \\ 0 & - 2 v & 2 v\end{vmatrix} \\  &=\langle \begin{vmatrix}1 & 0 \\ - 2 v & 2 v\end{vmatrix},\,-\begin{vmatrix}4 u & 0 \\ 0 & 2 v\end{vmatrix},\,\begin{vmatrix}4 u & 1 \\ 0 & - 2 v\end{vmatrix}\rangle \\  &=\langle 2 v,\,- 8 u v,\,- 8 u v\rangle\end{aligned}
$$

and

$$
\begin{aligned}\left\|\mathbf r_u\times\mathbf r_v\right\| &=\left\|\langle 2 v,\,- 8 u v,\,- 8 u v\rangle\right\| \\  &=\sqrt{\left(2 v\right)^2+\left(- 8 u v\right)^2+\left(- 8 u v\right)^2} \\  &=\sqrt{4 v^{2}+64 u^{2} v^{2}+64 u^{2} v^{2}} \\  &=\sqrt{128 u^{2} v^{2} + 4 v^{2}} \\  &=\sqrt{4 v^{2} \left(32 u^{2} + 1\right)} \\  &=\sqrt{4 v^{2}}\sqrt{32 u^{2} + 1} \\  &=2 v \sqrt{32 u^{2} + 1}\end{aligned}
$$

Notice that $\sqrt{v^2}=v$ since $v\ge 0$ on $D.$

Therefore, the surface area is

$$
\begin{aligned}\iint_S\mathrm{d}S &=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A \\  &=\iint_D 2 v \sqrt{32 u^{2} + 1}\,\mathrm{d}A\end{aligned}
$$

# q-109948

## Original

$$
{∬}_{D}\boxed{}\,\text{d}A,\,D={(u,v)\,:\,0\le u\le 4,\,0\le v\le \pi }
$$

The integral above gives the surface area of the parametric surface $r(u,v)=⟨u,\,{e}^{u}\operatorname{sin}⁡v,\,{e}^{u}\operatorname{cos}⁡v⟩$ for $0\le u\le 4$ and $0\le v\le \pi .$ What is the missing expression?

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}({e}^{u}\operatorname{sin}⁡v),\,\frac{∂}{∂u}({e}^{u}\operatorname{cos}⁡v)⟩ \\  & =⟨1,\,{e}^{u}\operatorname{sin}⁡v,\,{e}^{u}\operatorname{cos}⁡v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}({e}^{u}\operatorname{sin}⁡v),\,\frac{∂}{∂v}({e}^{u}\operatorname{cos}⁡v)⟩ \\  & =⟨0,\,{e}^{u}\operatorname{cos}⁡v,\,-{e}^{u}\operatorname{sin}⁡v⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & {e}^{u}\operatorname{sin}⁡v & {e}^{u}\operatorname{cos}⁡v \\ 0 & {e}^{u}\operatorname{cos}⁡v & -{e}^{u}\operatorname{sin}⁡v\end{aligned}| \\  & =⟨|\begin{aligned}{e}^{u}\operatorname{sin}⁡v & {e}^{u}\operatorname{cos}⁡v \\ {e}^{u}\operatorname{cos}⁡v & -{e}^{u}\operatorname{sin}⁡v\end{aligned}|,\,-|\begin{aligned}1 & {e}^{u}\operatorname{cos}⁡v \\ 0 & -{e}^{u}\operatorname{sin}⁡v\end{aligned}|,\,|\begin{aligned}1 & {e}^{u}\operatorname{sin}⁡v \\ 0 & {e}^{u}\operatorname{cos}⁡v\end{aligned}|⟩ \\  & =⟨-{e}^{2u}({sin}^{2}⁡v+{cos}^{2}⁡v),\,{e}^{u}\operatorname{sin}⁡v,\,{e}^{u}\operatorname{cos}⁡v⟩ \\  & =⟨-{e}^{2u},\,{e}^{u}\operatorname{sin}⁡v,\,{e}^{u}\operatorname{cos}⁡v⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨-{e}^{2u},\,{e}^{u}\operatorname{sin}⁡v,\,{e}^{u}\operatorname{cos}⁡v⟩‖ \\  & =\sqrt{(-{e}^{2u})^{2}+({e}^{u}\operatorname{sin}⁡v)^{2}+({e}^{u}\operatorname{cos}⁡v)^{2}} \\  & =\sqrt{{e}^{4u}+{e}^{2u}{sin}^{2}⁡v+{e}^{2u}{cos}^{2}⁡v} \\  & =\sqrt{{e}^{4u}+{e}^{2u}({sin}^{2}⁡v+{cos}^{2}⁡v)} \\  & =\sqrt{{e}^{4u}+{e}^{2u}} \\  & =\sqrt{{e}^{2u}({e}^{2u}+1)} \\  & =\sqrt{{e}^{2u}}\sqrt{{e}^{2u}+1} \\  & ={e}^{u}\sqrt{{e}^{2u}+1}.\end{aligned}
$$

Therefore, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}{e}^{u}\sqrt{{e}^{2u}+1}\,\text{d}A\end{aligned}
$$

## replay

$$
\iint_D\boxed{}\,\mathrm{d}A,\quad D=\{(u,v):0\le u\le 4,\,0\le v\le \pi\}
$$

The integral above gives the surface area of the parametric surface $r(u,v)=\langle u,\,e^{u} \sin{\left(v \right)},\,e^{u} \cos{\left(v \right)}\rangle$ for $0\le u\le 4,\,0\le v\le \pi.$ What is the missing expression?

{'a': 1}

- $\sqrt{e^{2 u} + 1} e^{u}$

- $\sqrt{\sin{\left(v \right)} + \cos{\left(v \right)}} e^{2 u}$

- $\sqrt{u + 1} e^{u}$

- $\sqrt{\sin{\left(v \right)} \cos{\left(v \right)}} e^{\frac{u}{2}}$

- $e^{u} \sin{\left(v \right)} \cos{\left(v \right)}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
\iint_S\mathrm{d}S=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}\mathbf r_u &=\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\rangle \\  &=\langle \frac{\partial}{\partial u}\left(u\right),\,\frac{\partial}{\partial u}\left(e^{u} \sin{\left(v \right)}\right),\,\frac{\partial}{\partial u}\left(e^{u} \cos{\left(v \right)}\right)\rangle \\  &=\langle 1,\,e^{u} \sin{\left(v \right)},\,e^{u} \cos{\left(v \right)}\rangle \\ \mathbf r_v &=\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\rangle \\  &=\langle \frac{\partial}{\partial v}\left(u\right),\,\frac{\partial}{\partial v}\left(e^{u} \sin{\left(v \right)}\right),\,\frac{\partial}{\partial v}\left(e^{u} \cos{\left(v \right)}\right)\rangle \\  &=\langle 0,\,e^{u} \cos{\left(v \right)},\,- e^{u} \sin{\left(v \right)}\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}\mathbf r_u\times\mathbf r_v &=\begin{vmatrix}i & j & k \\ 1 & e^{u} \sin{\left(v \right)} & e^{u} \cos{\left(v \right)} \\ 0 & e^{u} \cos{\left(v \right)} & - e^{u} \sin{\left(v \right)}\end{vmatrix} \\  &=\langle \begin{vmatrix}e^{u} \sin{\left(v \right)} & e^{u} \cos{\left(v \right)} \\ e^{u} \cos{\left(v \right)} & - e^{u} \sin{\left(v \right)}\end{vmatrix},\,-\begin{vmatrix}1 & e^{u} \cos{\left(v \right)} \\ 0 & - e^{u} \sin{\left(v \right)}\end{vmatrix},\,\begin{vmatrix}1 & e^{u} \sin{\left(v \right)} \\ 0 & e^{u} \cos{\left(v \right)}\end{vmatrix}\rangle \\  &=\langle - e^{2 u} \sin^{2}{\left(v \right)} - e^{2 u} \cos^{2}{\left(v \right)},\,e^{u} \sin{\left(v \right)},\,e^{u} \cos{\left(v \right)}\rangle \\  &=\langle - e^{2 u},\,e^{u} \sin{\left(v \right)},\,e^{u} \cos{\left(v \right)}\rangle\end{aligned}
$$

and

$$
\begin{aligned}\left\|\mathbf r_u\times\mathbf r_v\right\| &=\left\|\langle - e^{2 u},\,e^{u} \sin{\left(v \right)},\,e^{u} \cos{\left(v \right)}\rangle\right\| \\  &=\sqrt{\left(- e^{2 u}\right)^2+\left(e^{u} \sin{\left(v \right)}\right)^2+\left(e^{u} \cos{\left(v \right)}\right)^2} \\  &=\sqrt{e^{4 u}+e^{2 u} \sin^{2}{\left(v \right)}+e^{2 u} \cos^{2}{\left(v \right)}} \\  &=\sqrt{e^{4 u}+e^{2 u}\left(\sin^2 v+\cos^2 v\right)} \\  &=\sqrt{e^{4 u} + e^{2 u}} \\  &=\sqrt{e^{2 u}}\sqrt{e^{2 u} + 1} \\  &=\sqrt{e^{2 u} + 1} e^{u}\end{aligned}
$$

Therefore, the surface area is

$$
\begin{aligned}\iint_S\mathrm{d}S &=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A \\  &=\iint_D \sqrt{e^{2 u} + 1} e^{u}\,\mathrm{d}A\end{aligned}
$$

## variant

$$
\iint_D\boxed{}\,\mathrm{d}A,\quad D=\{(u,v):0\le u\le 4,\,0\le v\le \pi\}
$$

The integral above gives the surface area of the parametric surface $r(u,v)=\langle 2 u,\,e^{u} \sin{\left(v \right)},\,e^{u} \cos{\left(v \right)}\rangle$ for $0\le u\le 4,\,0\le v\le \pi.$ What is the missing expression?

{'a': 2}

- $\sqrt{e^{2 u} + 4} e^{u}$

- $\sqrt{\sin{\left(v \right)} + \cos{\left(v \right)}} e^{2 u}$

- $\sqrt{\sin{\left(v \right)} \cos{\left(v \right)}} e^{\frac{u}{2}}$

- $e^{u} \sin{\left(v \right)} \cos{\left(v \right)}$

- $\sqrt{u + 4} e^{u}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
\iint_S\mathrm{d}S=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}\mathbf r_u &=\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\rangle \\  &=\langle \frac{\partial}{\partial u}\left(2 u\right),\,\frac{\partial}{\partial u}\left(e^{u} \sin{\left(v \right)}\right),\,\frac{\partial}{\partial u}\left(e^{u} \cos{\left(v \right)}\right)\rangle \\  &=\langle 2,\,e^{u} \sin{\left(v \right)},\,e^{u} \cos{\left(v \right)}\rangle \\ \mathbf r_v &=\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\rangle \\  &=\langle \frac{\partial}{\partial v}\left(2 u\right),\,\frac{\partial}{\partial v}\left(e^{u} \sin{\left(v \right)}\right),\,\frac{\partial}{\partial v}\left(e^{u} \cos{\left(v \right)}\right)\rangle \\  &=\langle 0,\,e^{u} \cos{\left(v \right)},\,- e^{u} \sin{\left(v \right)}\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}\mathbf r_u\times\mathbf r_v &=\begin{vmatrix}i & j & k \\ 2 & e^{u} \sin{\left(v \right)} & e^{u} \cos{\left(v \right)} \\ 0 & e^{u} \cos{\left(v \right)} & - e^{u} \sin{\left(v \right)}\end{vmatrix} \\  &=\langle \begin{vmatrix}e^{u} \sin{\left(v \right)} & e^{u} \cos{\left(v \right)} \\ e^{u} \cos{\left(v \right)} & - e^{u} \sin{\left(v \right)}\end{vmatrix},\,-\begin{vmatrix}2 & e^{u} \cos{\left(v \right)} \\ 0 & - e^{u} \sin{\left(v \right)}\end{vmatrix},\,\begin{vmatrix}2 & e^{u} \sin{\left(v \right)} \\ 0 & e^{u} \cos{\left(v \right)}\end{vmatrix}\rangle \\  &=\langle - e^{2 u} \sin^{2}{\left(v \right)} - e^{2 u} \cos^{2}{\left(v \right)},\,2 e^{u} \sin{\left(v \right)},\,2 e^{u} \cos{\left(v \right)}\rangle \\  &=\langle - e^{2 u},\,2 e^{u} \sin{\left(v \right)},\,2 e^{u} \cos{\left(v \right)}\rangle\end{aligned}
$$

and

$$
\begin{aligned}\left\|\mathbf r_u\times\mathbf r_v\right\| &=\left\|\langle - e^{2 u},\,2 e^{u} \sin{\left(v \right)},\,2 e^{u} \cos{\left(v \right)}\rangle\right\| \\  &=\sqrt{\left(- e^{2 u}\right)^2+\left(2 e^{u} \sin{\left(v \right)}\right)^2+\left(2 e^{u} \cos{\left(v \right)}\right)^2} \\  &=\sqrt{e^{4 u}+4 e^{2 u} \sin^{2}{\left(v \right)}+4 e^{2 u} \cos^{2}{\left(v \right)}} \\  &=\sqrt{e^{4 u}+4 e^{2 u}\left(\sin^2 v+\cos^2 v\right)} \\  &=\sqrt{\left(e^{2 u} + 4\right) e^{2 u}} \\  &=\sqrt{e^{2 u}}\sqrt{e^{2 u} + 4} \\  &=\sqrt{e^{2 u} + 4} e^{u}\end{aligned}
$$

Therefore, the surface area is

$$
\begin{aligned}\iint_S\mathrm{d}S &=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A \\  &=\iint_D \sqrt{e^{2 u} + 4} e^{u}\,\mathrm{d}A\end{aligned}
$$

# q-110019

## Original

$$
{∬}_{D}\boxed{}\,\text{d}A,\,D={(u,v)\,:\,0\le u\le 2,\,0\le v\le \pi }
$$

The integral above gives the surface area of the parametric surface $r(u,v)=⟨{u}^{2},\,2u\operatorname{sin}⁡v,\,u\operatorname{cos}⁡v⟩$ for $0\le u\le 1$ and $0\le v\le \pi .$ What is the missing expression?

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}({u}^{2}),\,\frac{∂}{∂u}(2u\operatorname{sin}⁡v),\,\frac{∂}{∂u}(u\operatorname{cos}⁡v)⟩ \\  & =⟨2u,\,2\operatorname{sin}⁡v,\,\operatorname{cos}⁡v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}({u}^{2}),\,\frac{∂}{∂v}(2u\operatorname{sin}⁡v),\,\frac{∂}{∂v}(u\operatorname{cos}⁡v)⟩ \\  & =⟨0,\,2u\operatorname{cos}⁡v,\,-u\operatorname{sin}⁡v⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2u & 2\operatorname{sin}⁡v & \operatorname{cos}⁡v \\ 0 & 2u\operatorname{cos}⁡v & -u\operatorname{sin}⁡v\end{aligned}| \\  & =⟨|\begin{aligned}2\operatorname{sin}⁡v & \operatorname{cos}⁡v \\ 2u\operatorname{cos}⁡v & -u\operatorname{sin}⁡v\end{aligned}|,\,-|\begin{aligned}2u & \operatorname{cos}⁡v \\ 0 & -u\operatorname{sin}⁡v\end{aligned}|,\,|\begin{aligned}2u & 2\operatorname{sin}⁡v \\ 0 & 2u\operatorname{cos}⁡v\end{aligned}|⟩ \\  & =⟨-2u{sin}^{2}⁡v-2u{cos}^{2}⁡v,\,2{u}^{2}\operatorname{sin}⁡v,\,4{u}^{2}\operatorname{cos}⁡v⟩ \\  & =⟨-2u,\,2{u}^{2}\operatorname{sin}⁡v,\,4{u}^{2}\operatorname{cos}⁡v⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨-2u,\,2{u}^{2}\operatorname{sin}⁡v,\,4{u}^{2}\operatorname{cos}⁡v⟩‖ \\  & =\sqrt{(2u)^{2}+(2{u}^{2}\operatorname{sin}⁡v)^{2}+(4{u}^{2}\operatorname{cos}⁡v)^{2}} \\  & =\sqrt{4{u}^{2}+4{u}^{4}{sin}^{2}⁡v+16{u}^{4}{cos}^{2}⁡v} \\  & =\sqrt{4{u}^{2}+4{u}^{4}({sin}^{2}⁡v+{cos}^{2}⁡v)+12{u}^{4}{cos}^{2}⁡v} \\  & =\sqrt{4{u}^{2}+4{u}^{4}+12{u}^{4}{cos}^{2}⁡v} \\  & =\sqrt{4{u}^{2}(1+{u}^{2}+3{u}^{2}{cos}^{2}⁡v)} \\  & =\sqrt{4{u}^{2}}\sqrt{1+{u}^{2}+3{u}^{2}{cos}^{2}⁡v} \\  & =2u\sqrt{1+{u}^{2}+3{u}^{2}{cos}^{2}⁡v}.\end{aligned}
$$

Notice that $\sqrt{{u}^{2}}=u$ since $u\ge 0$ on $D.$

Therefore, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}2u\sqrt{1+{u}^{2}+3{u}^{2}{cos}^{2}⁡v}\,\text{d}A\end{aligned}
$$

## replay

$$
\iint_D\boxed{}\,\mathrm{d}A,\quad D=\{(u,v):0\le u\le 1,\,0\le v\le \pi\}
$$

The integral above gives the surface area of the parametric surface $r(u,v)=\langle u^{2},\,2 u \sin{\left(v \right)},\,u \cos{\left(v \right)}\rangle$ for $0\le u\le 1,\,0\le v\le \pi.$ What is the missing expression?

{'a': 2}

- $2 u \sqrt{u^{2} \cos^{2}{\left(v \right)} + 1}$

- $\sqrt{2 u^{2} + 1}$

- $u \sqrt{u^{2} + \cos^{2}{\left(v \right)}}$

- $u \sqrt{12 u^{2} \cos^{2}{\left(v \right)} + 4 u^{2} + 4}$

- $\sqrt{u^{2} + 1} \cos{\left(v \right)}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
\iint_S\mathrm{d}S=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}\mathbf r_u &=\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\rangle \\  &=\langle \frac{\partial}{\partial u}\left(u^{2}\right),\,\frac{\partial}{\partial u}\left(2 u \sin{\left(v \right)}\right),\,\frac{\partial}{\partial u}\left(u \cos{\left(v \right)}\right)\rangle \\  &=\langle 2 u,\,2 \sin{\left(v \right)},\,\cos{\left(v \right)}\rangle \\ \mathbf r_v &=\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\rangle \\  &=\langle \frac{\partial}{\partial v}\left(u^{2}\right),\,\frac{\partial}{\partial v}\left(2 u \sin{\left(v \right)}\right),\,\frac{\partial}{\partial v}\left(u \cos{\left(v \right)}\right)\rangle \\  &=\langle 0,\,2 u \cos{\left(v \right)},\,- u \sin{\left(v \right)}\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}\mathbf r_u\times\mathbf r_v &=\begin{vmatrix}i & j & k \\ 2 u & 2 \sin{\left(v \right)} & \cos{\left(v \right)} \\ 0 & 2 u \cos{\left(v \right)} & - u \sin{\left(v \right)}\end{vmatrix} \\  &=\langle \begin{vmatrix}2 \sin{\left(v \right)} & \cos{\left(v \right)} \\ 2 u \cos{\left(v \right)} & - u \sin{\left(v \right)}\end{vmatrix},\,-\begin{vmatrix}2 u & \cos{\left(v \right)} \\ 0 & - u \sin{\left(v \right)}\end{vmatrix},\,\begin{vmatrix}2 u & 2 \sin{\left(v \right)} \\ 0 & 2 u \cos{\left(v \right)}\end{vmatrix}\rangle \\  &=\langle - 2 u \sin^{2}{\left(v \right)} - 2 u \cos^{2}{\left(v \right)},\,2 u^{2} \sin{\left(v \right)},\,4 u^{2} \cos{\left(v \right)}\rangle \\  &=\langle - 2 u,\,2 u^{2} \sin{\left(v \right)},\,4 u^{2} \cos{\left(v \right)}\rangle\end{aligned}
$$

and

$$
\begin{aligned}\left\|\mathbf r_u\times\mathbf r_v\right\| &=\left\|\langle - 2 u,\,2 u^{2} \sin{\left(v \right)},\,4 u^{2} \cos{\left(v \right)}\rangle\right\| \\  &=\sqrt{\left(- 2 u\right)^2+\left(2 u^{2} \sin{\left(v \right)}\right)^2+\left(4 u^{2} \cos{\left(v \right)}\right)^2} \\  &=\sqrt{4 u^{2}+4 u^{4} \sin^{2}{\left(v \right)}+16 u^{4} \cos^{2}{\left(v \right)}} \\  &=\sqrt{4 u^{2}+4 u^{4}\left(\sin^2 v+\cos^2 v\right)+12 u^{4} \cos^{2}{\left(v \right)}} \\  &=\sqrt{12 u^{4} \cos^{2}{\left(v \right)} + 4 u^{4} + 4 u^{2}} \\  &=\sqrt{u^{2}}\sqrt{12 u^{2} \cos^{2}{\left(v \right)} + 4 u^{2} + 4} \\  &=u \sqrt{12 u^{2} \cos^{2}{\left(v \right)} + 4 u^{2} + 4}\end{aligned}
$$

Notice that $\sqrt{u^2}=u$ since $u\ge 0$ on $D.$

Therefore, the surface area is

$$
\begin{aligned}\iint_S\mathrm{d}S &=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A \\  &=\iint_D u \sqrt{12 u^{2} \cos^{2}{\left(v \right)} + 4 u^{2} + 4}\,\mathrm{d}A\end{aligned}
$$

## variant

$$
\iint_D\boxed{}\,\mathrm{d}A,\quad D=\{(u,v):0\le u\le 1,\,0\le v\le \pi\}
$$

The integral above gives the surface area of the parametric surface $r(u,v)=\langle u^{2},\,3 u \sin{\left(v \right)},\,u \cos{\left(v \right)}\rangle$ for $0\le u\le 1,\,0\le v\le \pi.$ What is the missing expression?

{'a': 3}

- $3 u \sqrt{u^{2} \cos^{2}{\left(v \right)} + 1}$

- $\sqrt{3 u^{2} + 1}$

- $u \sqrt{32 u^{2} \cos^{2}{\left(v \right)} + 4 u^{2} + 9}$

- $\sqrt{u^{2} + 1} \cos{\left(v \right)}$

- $u \sqrt{u^{2} + \cos^{2}{\left(v \right)}}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
\iint_S\mathrm{d}S=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}\mathbf r_u &=\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\rangle \\  &=\langle \frac{\partial}{\partial u}\left(u^{2}\right),\,\frac{\partial}{\partial u}\left(3 u \sin{\left(v \right)}\right),\,\frac{\partial}{\partial u}\left(u \cos{\left(v \right)}\right)\rangle \\  &=\langle 2 u,\,3 \sin{\left(v \right)},\,\cos{\left(v \right)}\rangle \\ \mathbf r_v &=\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\rangle \\  &=\langle \frac{\partial}{\partial v}\left(u^{2}\right),\,\frac{\partial}{\partial v}\left(3 u \sin{\left(v \right)}\right),\,\frac{\partial}{\partial v}\left(u \cos{\left(v \right)}\right)\rangle \\  &=\langle 0,\,3 u \cos{\left(v \right)},\,- u \sin{\left(v \right)}\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}\mathbf r_u\times\mathbf r_v &=\begin{vmatrix}i & j & k \\ 2 u & 3 \sin{\left(v \right)} & \cos{\left(v \right)} \\ 0 & 3 u \cos{\left(v \right)} & - u \sin{\left(v \right)}\end{vmatrix} \\  &=\langle \begin{vmatrix}3 \sin{\left(v \right)} & \cos{\left(v \right)} \\ 3 u \cos{\left(v \right)} & - u \sin{\left(v \right)}\end{vmatrix},\,-\begin{vmatrix}2 u & \cos{\left(v \right)} \\ 0 & - u \sin{\left(v \right)}\end{vmatrix},\,\begin{vmatrix}2 u & 3 \sin{\left(v \right)} \\ 0 & 3 u \cos{\left(v \right)}\end{vmatrix}\rangle \\  &=\langle - 3 u \sin^{2}{\left(v \right)} - 3 u \cos^{2}{\left(v \right)},\,2 u^{2} \sin{\left(v \right)},\,6 u^{2} \cos{\left(v \right)}\rangle \\  &=\langle - 3 u,\,2 u^{2} \sin{\left(v \right)},\,6 u^{2} \cos{\left(v \right)}\rangle\end{aligned}
$$

and

$$
\begin{aligned}\left\|\mathbf r_u\times\mathbf r_v\right\| &=\left\|\langle - 3 u,\,2 u^{2} \sin{\left(v \right)},\,6 u^{2} \cos{\left(v \right)}\rangle\right\| \\  &=\sqrt{\left(- 3 u\right)^2+\left(2 u^{2} \sin{\left(v \right)}\right)^2+\left(6 u^{2} \cos{\left(v \right)}\right)^2} \\  &=\sqrt{9 u^{2}+4 u^{4} \sin^{2}{\left(v \right)}+36 u^{4} \cos^{2}{\left(v \right)}} \\  &=\sqrt{9 u^{2}+4 u^{4}\left(\sin^2 v+\cos^2 v\right)+32 u^{4} \cos^{2}{\left(v \right)}} \\  &=\sqrt{32 u^{4} \cos^{2}{\left(v \right)} + 4 u^{4} + 9 u^{2}} \\  &=\sqrt{u^{2}}\sqrt{32 u^{2} \cos^{2}{\left(v \right)} + 4 u^{2} + 9} \\  &=u \sqrt{32 u^{2} \cos^{2}{\left(v \right)} + 4 u^{2} + 9}\end{aligned}
$$

Notice that $\sqrt{u^2}=u$ since $u\ge 0$ on $D.$

Therefore, the surface area is

$$
\begin{aligned}\iint_S\mathrm{d}S &=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A \\  &=\iint_D u \sqrt{32 u^{2} \cos^{2}{\left(v \right)} + 4 u^{2} + 9}\,\mathrm{d}A\end{aligned}
$$

# q-109943

## Original

$$
{∬}_{D}\boxed{}\,\text{d}A,\,D={(u,v)\,:\,0\le u\le 1,\,0\le v\le 2}
$$

The integral above gives the surface area of the parametric surface $r(u,v)=⟨u+v,\,3-v,\,1+4u+5v⟩$ for $0\le u\le 1$ and $0\le v\le 2.$ What is the missing expression?

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u+v),\,\frac{∂}{∂u}(3-v),\,\frac{∂}{∂u}(1+4u+5v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u+v),\,\frac{∂}{∂v}(3-v),\,\frac{∂}{∂v}(1+4u+5v)⟩ \\  & =⟨1,\,-1,\,5⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 1 & -1 & 5\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ -1 & 5\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 1 & 5\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 1 & -1\end{aligned}|⟩ \\  & =⟨4,\,-1,\,-1⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨4,\,-1,\,-1⟩‖ \\  & =\sqrt{(4)^{2}+(-1)^{2}+(-1)^{2}} \\  & =\sqrt{16+1+1} \\  & =\sqrt{18} \\  & =3\sqrt{2}.\end{aligned}
$$

Therefore, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}3\sqrt{2}\,\text{d}A\end{aligned}
$$

## replay

$$
\iint_D\boxed{}\,\mathrm{d}A,\quad D=\{(u,v):0\le u\le 1,\,0\le v\le 2\}
$$

The integral above gives the surface area of the parametric surface $r(u,v)=\langle u + v,\,3 - v,\,4 u + 5 v + 1\rangle$ for $0\le u\le 1,\,0\le v\le 2.$ What is the missing expression?

{'a': 4, 'b': 5}

- $u \sqrt{v^{2} + 1}$

- $\sqrt{3}$

- $\sqrt{10}$

- $3 \sqrt{2}$

- $2 \sqrt{u + v}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
\iint_S\mathrm{d}S=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}\mathbf r_u &=\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\rangle \\  &=\langle \frac{\partial}{\partial u}\left(u + v\right),\,\frac{\partial}{\partial u}\left(3 - v\right),\,\frac{\partial}{\partial u}\left(4 u + 5 v + 1\right)\rangle \\  &=\langle 1,\,0,\,4\rangle \\ \mathbf r_v &=\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\rangle \\  &=\langle \frac{\partial}{\partial v}\left(u + v\right),\,\frac{\partial}{\partial v}\left(3 - v\right),\,\frac{\partial}{\partial v}\left(4 u + 5 v + 1\right)\rangle \\  &=\langle 1,\,-1,\,5\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}\mathbf r_u\times\mathbf r_v &=\begin{vmatrix}i & j & k \\ 1 & 0 & 4 \\ 1 & -1 & 5\end{vmatrix} \\  &=\langle \begin{vmatrix}0 & 4 \\ -1 & 5\end{vmatrix},\,-\begin{vmatrix}1 & 4 \\ 1 & 5\end{vmatrix},\,\begin{vmatrix}1 & 0 \\ 1 & -1\end{vmatrix}\rangle \\  &=\langle 4,\,-1,\,-1\rangle\end{aligned}
$$

and

$$
\begin{aligned}\left\|\mathbf r_u\times\mathbf r_v\right\| &=\left\|\langle 4,\,-1,\,-1\rangle\right\| \\  &=\sqrt{\left(4\right)^2+\left(-1\right)^2+\left(-1\right)^2} \\  &=\sqrt{16+1+1} \\  &=\sqrt{18} \\  &=3 \sqrt{2}\end{aligned}
$$

Therefore, the surface area is

$$
\begin{aligned}\iint_S\mathrm{d}S &=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A \\  &=\iint_D 3 \sqrt{2}\,\mathrm{d}A\end{aligned}
$$

## variant

$$
\iint_D\boxed{}\,\mathrm{d}A,\quad D=\{(u,v):0\le u\le 1,\,0\le v\le 2\}
$$

The integral above gives the surface area of the parametric surface $r(u,v)=\langle u + v,\,3 - v,\,2 u + 4 v + 1\rangle$ for $0\le u\le 1,\,0\le v\le 2.$ What is the missing expression?

{'a': 2, 'b': 4}

- $u \sqrt{v^{2} + 1}$

- $2$

- $3$

- $2 \sqrt{u + v}$

- $\sqrt{7}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
\iint_S\mathrm{d}S=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}\mathbf r_u &=\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\rangle \\  &=\langle \frac{\partial}{\partial u}\left(u + v\right),\,\frac{\partial}{\partial u}\left(3 - v\right),\,\frac{\partial}{\partial u}\left(2 u + 4 v + 1\right)\rangle \\  &=\langle 1,\,0,\,2\rangle \\ \mathbf r_v &=\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\rangle \\  &=\langle \frac{\partial}{\partial v}\left(u + v\right),\,\frac{\partial}{\partial v}\left(3 - v\right),\,\frac{\partial}{\partial v}\left(2 u + 4 v + 1\right)\rangle \\  &=\langle 1,\,-1,\,4\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}\mathbf r_u\times\mathbf r_v &=\begin{vmatrix}i & j & k \\ 1 & 0 & 2 \\ 1 & -1 & 4\end{vmatrix} \\  &=\langle \begin{vmatrix}0 & 2 \\ -1 & 4\end{vmatrix},\,-\begin{vmatrix}1 & 2 \\ 1 & 4\end{vmatrix},\,\begin{vmatrix}1 & 0 \\ 1 & -1\end{vmatrix}\rangle \\  &=\langle 2,\,-2,\,-1\rangle\end{aligned}
$$

and

$$
\begin{aligned}\left\|\mathbf r_u\times\mathbf r_v\right\| &=\left\|\langle 2,\,-2,\,-1\rangle\right\| \\  &=\sqrt{\left(2\right)^2+\left(-2\right)^2+\left(-1\right)^2} \\  &=\sqrt{4+4+1} \\  &=\sqrt{9} \\  &=3\end{aligned}
$$

Therefore, the surface area is

$$
\begin{aligned}\iint_S\mathrm{d}S &=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A \\  &=\iint_D 3\,\mathrm{d}A\end{aligned}
$$

# q-109947

## Original

$$
{∬}_{D}\boxed{}\,\text{d}A,\,D={(u,v)\,:\,0\le u\le 1,\,0\le v\le 1}
$$

The integral above gives the surface area of the parametric surface $r(u,v)=⟨u+v,\,3{u}^{2},\,u-v⟩$ for $0\le u\le 1$ and $0\le v\le 1.$ What is the missing expression?

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u+v),\,\frac{∂}{∂u}(3{u}^{2}),\,\frac{∂}{∂u}(u-v)⟩ \\  & =⟨1,\,6u,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u+v),\,\frac{∂}{∂v}(3{u}^{2}),\,\frac{∂}{∂v}(u-v)⟩ \\  & =⟨1,\,0,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 6u & 1 \\ 1 & 0 & -1\end{aligned}| \\  & =⟨|\begin{aligned}6u & 1 \\ 0 & -1\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 1 & -1\end{aligned}|,\,|\begin{aligned}1 & 6u \\ 1 & 0\end{aligned}|⟩ \\  & =⟨-6u,\,2,\,-6u⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨-6u,\,2,\,-6u⟩‖ \\  & =\sqrt{(-6u)^{2}+(2)^{2}+(-6u)^{2}} \\  & =\sqrt{36{u}^{2}+4+36{u}^{2}} \\  & =\sqrt{72{u}^{2}+4} \\  & =\sqrt{4(18{u}^{2}+1)} \\  & =2\sqrt{18{u}^{2}+1}.\end{aligned}
$$

Therefore, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}2\sqrt{18{u}^{2}+1}\,\text{d}A\end{aligned}
$$

## replay

$$
\iint_D\boxed{}\,\mathrm{d}A,\quad D=\{(u,v):0\le u\le 1,\,0\le v\le 1\}
$$

The integral above gives the surface area of the parametric surface $r(u,v)=\langle u + v,\,3 u^{2},\,u - v\rangle$ for $0\le u\le 1,\,0\le v\le 1.$ What is the missing expression?

{'a': 3}

- $2 \sqrt{u^{2} + 1}$

- $2 u \sqrt{9 u^{2} + 1}$

- $\sqrt{u^{2} + 4}$

- $u \sqrt{u^{2} + 4}$

- $2 \sqrt{18 u^{2} + 1}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
\iint_S\mathrm{d}S=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}\mathbf r_u &=\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\rangle \\  &=\langle \frac{\partial}{\partial u}\left(u + v\right),\,\frac{\partial}{\partial u}\left(3 u^{2}\right),\,\frac{\partial}{\partial u}\left(u - v\right)\rangle \\  &=\langle 1,\,6 u,\,1\rangle \\ \mathbf r_v &=\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\rangle \\  &=\langle \frac{\partial}{\partial v}\left(u + v\right),\,\frac{\partial}{\partial v}\left(3 u^{2}\right),\,\frac{\partial}{\partial v}\left(u - v\right)\rangle \\  &=\langle 1,\,0,\,-1\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}\mathbf r_u\times\mathbf r_v &=\begin{vmatrix}i & j & k \\ 1 & 6 u & 1 \\ 1 & 0 & -1\end{vmatrix} \\  &=\langle \begin{vmatrix}6 u & 1 \\ 0 & -1\end{vmatrix},\,-\begin{vmatrix}1 & 1 \\ 1 & -1\end{vmatrix},\,\begin{vmatrix}1 & 6 u \\ 1 & 0\end{vmatrix}\rangle \\  &=\langle - 6 u,\,2,\,- 6 u\rangle\end{aligned}
$$

and

$$
\begin{aligned}\left\|\mathbf r_u\times\mathbf r_v\right\| &=\left\|\langle - 6 u,\,2,\,- 6 u\rangle\right\| \\  &=\sqrt{\left(- 6 u\right)^2+\left(2\right)^2+\left(- 6 u\right)^2} \\  &=\sqrt{36 u^{2}+4+36 u^{2}} \\  &=\sqrt{72 u^{2} + 4} \\  &=\sqrt{4\left(18 u^{2} + 1\right)} \\  &=2 \sqrt{18 u^{2} + 1}\end{aligned}
$$

Therefore, the surface area is

$$
\begin{aligned}\iint_S\mathrm{d}S &=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A \\  &=\iint_D 2 \sqrt{18 u^{2} + 1}\,\mathrm{d}A\end{aligned}
$$

## variant

$$
\iint_D\boxed{}\,\mathrm{d}A,\quad D=\{(u,v):0\le u\le 1,\,0\le v\le 1\}
$$

The integral above gives the surface area of the parametric surface $r(u,v)=\langle u + v,\,4 u^{2},\,u - v\rangle$ for $0\le u\le 1,\,0\le v\le 1.$ What is the missing expression?

{'a': 4}

- $2 \sqrt{u^{2} + 1}$

- $2 u \sqrt{16 u^{2} + 1}$

- $u \sqrt{u^{2} + 4}$

- $2 \sqrt{32 u^{2} + 1}$

- $\sqrt{u^{2} + 4}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
\iint_S\mathrm{d}S=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}\mathbf r_u &=\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\rangle \\  &=\langle \frac{\partial}{\partial u}\left(u + v\right),\,\frac{\partial}{\partial u}\left(4 u^{2}\right),\,\frac{\partial}{\partial u}\left(u - v\right)\rangle \\  &=\langle 1,\,8 u,\,1\rangle \\ \mathbf r_v &=\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\rangle \\  &=\langle \frac{\partial}{\partial v}\left(u + v\right),\,\frac{\partial}{\partial v}\left(4 u^{2}\right),\,\frac{\partial}{\partial v}\left(u - v\right)\rangle \\  &=\langle 1,\,0,\,-1\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}\mathbf r_u\times\mathbf r_v &=\begin{vmatrix}i & j & k \\ 1 & 8 u & 1 \\ 1 & 0 & -1\end{vmatrix} \\  &=\langle \begin{vmatrix}8 u & 1 \\ 0 & -1\end{vmatrix},\,-\begin{vmatrix}1 & 1 \\ 1 & -1\end{vmatrix},\,\begin{vmatrix}1 & 8 u \\ 1 & 0\end{vmatrix}\rangle \\  &=\langle - 8 u,\,2,\,- 8 u\rangle\end{aligned}
$$

and

$$
\begin{aligned}\left\|\mathbf r_u\times\mathbf r_v\right\| &=\left\|\langle - 8 u,\,2,\,- 8 u\rangle\right\| \\  &=\sqrt{\left(- 8 u\right)^2+\left(2\right)^2+\left(- 8 u\right)^2} \\  &=\sqrt{64 u^{2}+4+64 u^{2}} \\  &=\sqrt{128 u^{2} + 4} \\  &=\sqrt{4\left(32 u^{2} + 1\right)} \\  &=2 \sqrt{32 u^{2} + 1}\end{aligned}
$$

Therefore, the surface area is

$$
\begin{aligned}\iint_S\mathrm{d}S &=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A \\  &=\iint_D 2 \sqrt{32 u^{2} + 1}\,\mathrm{d}A\end{aligned}
$$

# q-109951

## Original

$$
{∬}_{D}\boxed{}\,\text{d}A,\,D={(u,v)\,:\,0\le u\le 2,\,0\le v\le 4}
$$

The integral above gives the surface area of the parametric surface $r(u,v)=⟨{u}^{2},\,{v}^{2},\,uv⟩$ for $0\le u\le 2$ and $0\le v\le 4.$ What is the missing expression?

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}({u}^{2}),\,\frac{∂}{∂u}({v}^{2}),\,\frac{∂}{∂u}(uv)⟩ \\  & =⟨2u,\,0,\,v⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}({u}^{2}),\,\frac{∂}{∂v}({v}^{2}),\,\frac{∂}{∂v}(uv)⟩ \\  & =⟨0,\,2v,\,u⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2u & 0 & v \\ 0 & 2v & u\end{aligned}| \\  & =⟨|\begin{aligned}0 & v \\ 2v & u\end{aligned}|,\,-|\begin{aligned}2u & v \\ 0 & u\end{aligned}|,\,|\begin{aligned}2u & 0 \\ 0 & 2v\end{aligned}|⟩ \\  & =⟨-2{v}^{2},\,-2{u}^{2},\,4uv⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨-2{v}^{2},\,-2{u}^{2},\,4uv⟩‖ \\  & =\sqrt{(-2{v}^{2})^{2}+(-2{u}^{2})^{2}+(4uv)^{2}} \\  & =\sqrt{4{v}^{4}+4{u}^{4}+16{u}^{2}{v}^{2}} \\  & =\sqrt{4({u}^{4}+{v}^{4}+4{u}^{2}{v}^{2})} \\  & =2\sqrt{{u}^{4}+{v}^{4}+4{u}^{2}{v}^{2}}.\end{aligned}
$$

Therefore, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}2\sqrt{{u}^{4}+{v}^{4}+4{u}^{2}{v}^{2}}\,\text{d}A\end{aligned}
$$

## replay

$$
\iint_D\boxed{}\,\mathrm{d}A,\quad D=\{(u,v):0\le u\le 2,\,0\le v\le 4\}
$$

The integral above gives the surface area of the parametric surface $r(u,v)=\langle u^{2},\,v^{2},\,u v\rangle$ for $0\le u\le 2,\,0\le v\le 4.$ What is the missing expression?

{'a': 1}

- $2 u^{2} v$

- $2 \sqrt{u^{4} + 4 u^{2} v^{2} + v^{4}}$

- $\sqrt{u^{2} + v^{2}}$

- $2 u \sqrt{u v + v^{2}}$

- $u \sqrt{u^{2} + 1}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
\iint_S\mathrm{d}S=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}\mathbf r_u &=\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\rangle \\  &=\langle \frac{\partial}{\partial u}\left(u^{2}\right),\,\frac{\partial}{\partial u}\left(v^{2}\right),\,\frac{\partial}{\partial u}\left(u v\right)\rangle \\  &=\langle 2 u,\,0,\,v\rangle \\ \mathbf r_v &=\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\rangle \\  &=\langle \frac{\partial}{\partial v}\left(u^{2}\right),\,\frac{\partial}{\partial v}\left(v^{2}\right),\,\frac{\partial}{\partial v}\left(u v\right)\rangle \\  &=\langle 0,\,2 v,\,u\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}\mathbf r_u\times\mathbf r_v &=\begin{vmatrix}i & j & k \\ 2 u & 0 & v \\ 0 & 2 v & u\end{vmatrix} \\  &=\langle \begin{vmatrix}0 & v \\ 2 v & u\end{vmatrix},\,-\begin{vmatrix}2 u & v \\ 0 & u\end{vmatrix},\,\begin{vmatrix}2 u & 0 \\ 0 & 2 v\end{vmatrix}\rangle \\  &=\langle - 2 v^{2},\,- 2 u^{2},\,4 u v\rangle\end{aligned}
$$

and

$$
\begin{aligned}\left\|\mathbf r_u\times\mathbf r_v\right\| &=\left\|\langle - 2 v^{2},\,- 2 u^{2},\,4 u v\rangle\right\| \\  &=\sqrt{\left(- 2 v^{2}\right)^2+\left(- 2 u^{2}\right)^2+\left(4 u v\right)^2} \\  &=\sqrt{4 v^{4}+4 u^{4}+16 u^{2} v^{2}} \\  &=\sqrt{4\left(u^{4} + 4 u^{2} v^{2} + v^{4}\right)} \\  &=2 \sqrt{u^{4} + 4 u^{2} v^{2} + v^{4}}\end{aligned}
$$

Therefore, the surface area is

$$
\begin{aligned}\iint_S\mathrm{d}S &=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A \\  &=\iint_D 2 \sqrt{u^{4} + 4 u^{2} v^{2} + v^{4}}\,\mathrm{d}A\end{aligned}
$$

## variant

$$
\iint_D\boxed{}\,\mathrm{d}A,\quad D=\{(u,v):0\le u\le 2,\,0\le v\le 4\}
$$

The integral above gives the surface area of the parametric surface $r(u,v)=\langle 2 u^{2},\,v^{2},\,u v\rangle$ for $0\le u\le 2,\,0\le v\le 4.$ What is the missing expression?

{'a': 2}

- $2 u^{2} v$

- $2 \sqrt{4 u^{4} + 16 u^{2} v^{2} + v^{4}}$

- $2 u \sqrt{u v + v^{2}}$

- $u \sqrt{u^{2} + 1}$

- $\sqrt{u^{2} + v^{2}}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
\iint_S\mathrm{d}S=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}\mathbf r_u &=\langle \frac{\partial x}{\partial u},\,\frac{\partial y}{\partial u},\,\frac{\partial z}{\partial u}\rangle \\  &=\langle \frac{\partial}{\partial u}\left(2 u^{2}\right),\,\frac{\partial}{\partial u}\left(v^{2}\right),\,\frac{\partial}{\partial u}\left(u v\right)\rangle \\  &=\langle 4 u,\,0,\,v\rangle \\ \mathbf r_v &=\langle \frac{\partial x}{\partial v},\,\frac{\partial y}{\partial v},\,\frac{\partial z}{\partial v}\rangle \\  &=\langle \frac{\partial}{\partial v}\left(2 u^{2}\right),\,\frac{\partial}{\partial v}\left(v^{2}\right),\,\frac{\partial}{\partial v}\left(u v\right)\rangle \\  &=\langle 0,\,2 v,\,u\rangle\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}\mathbf r_u\times\mathbf r_v &=\begin{vmatrix}i & j & k \\ 4 u & 0 & v \\ 0 & 2 v & u\end{vmatrix} \\  &=\langle \begin{vmatrix}0 & v \\ 2 v & u\end{vmatrix},\,-\begin{vmatrix}4 u & v \\ 0 & u\end{vmatrix},\,\begin{vmatrix}4 u & 0 \\ 0 & 2 v\end{vmatrix}\rangle \\  &=\langle - 2 v^{2},\,- 4 u^{2},\,8 u v\rangle\end{aligned}
$$

and

$$
\begin{aligned}\left\|\mathbf r_u\times\mathbf r_v\right\| &=\left\|\langle - 2 v^{2},\,- 4 u^{2},\,8 u v\rangle\right\| \\  &=\sqrt{\left(- 2 v^{2}\right)^2+\left(- 4 u^{2}\right)^2+\left(8 u v\right)^2} \\  &=\sqrt{4 v^{4}+16 u^{4}+64 u^{2} v^{2}} \\  &=\sqrt{4\left(4 u^{4} + 16 u^{2} v^{2} + v^{4}\right)} \\  &=2 \sqrt{4 u^{4} + 16 u^{2} v^{2} + v^{4}}\end{aligned}
$$

Therefore, the surface area is

$$
\begin{aligned}\iint_S\mathrm{d}S &=\iint_D\left\|\mathbf r_u\times\mathbf r_v\right\|\,\mathrm{d}A \\  &=\iint_D 2 \sqrt{4 u^{4} + 16 u^{2} v^{2} + v^{4}}\,\mathrm{d}A\end{aligned}
$$
