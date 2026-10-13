## Original q-160888

Evaluate the surface integral

$$
{∬}_{S}⟨z+y,\,2y+z,\,xy⟩\cdot \text{d}S
$$

where the surface $S$ is defined by $z=x-y$ for $0\le x\le 1$ and $0\le y\le 2.$

- $3$ (correct)
- $12$
- $\frac{9}{2}$
- $8$
- $\frac{9}{4}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}(x-y)=1 \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}(x-y)=-1\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =⟨z+y,\,2y+z,\,xy⟩{|}_{z=x-y} \\  & =⟨(x-y)+y,\,2y+(x-y),\,xy⟩ \\  & =⟨{{x}_{⏟}}_{P},\,{{x+y}_{⏟}}_{Q},\,{{xy}_{⏟}}_{R}⟩\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}{∬}_{S}⟨z+y,\,2y+z,\,xy⟩\cdot \text{d}S & ={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A \\  & ={∬}_{D}(-(x)\cdot 1-(x+y)\cdot (-1)+xy)\,\text{d}A \\  & ={∬}_{D}(-x+x+y+xy)\,\text{d}A \\  & ={∬}_{D}(y+xy)\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{0}^{2}(y+xy)\,\text{d}y\,\text{d}x \\  & ={\int }_{0}^{1}{[\frac{1}{2}{y}^{2}+\frac{1}{2}x{y}^{2}]}_{y=0}^{y=2}\,\text{d}x \\  & ={\int }_{0}^{1}(2+2x)\,\text{d}x \\  & =[2x+{x}^{2}]_{0}^{1} \\  & =(2(1)+{1}^{2})-0 \\  & =3.\end{aligned}
$$

### Generated observed-profile replay q-160888

Evaluate the surface integral

$$
\iint_S \left\langle y + z,\,2 y + z,\,x y\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the surface $S$ is defined by $z=x - y$ for $0\le x\le 1$ and $0\le y\le 2.$

- $\frac{9}{2}$
- $12$
- $3$
- $\frac{9}{4}$
- $8$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(x - y\right)=1 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(x - y\right)=-1\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle y + z,\,2 y + z,\,x y\right\rangle\big|_{z=x - y} \\  & =\left\langle y + \left(x - y\right),\,2 y + \left(x - y\right),\,x y\right\rangle \\  & =\left\langle \underbrace{x}_{P},\,\underbrace{x + y}_{Q},\,\underbrace{x y}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle y + z,\,2 y + z,\,x y\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(x\right)\left(1\right)-\left(x + y\right)\left(-1\right)+\left(x y\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(x y - x + x + y\right)\,\mathrm{d}A \\  & =\iint_D\left(y \left(x + 1\right)\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{0}^{2}\left(y \left(x + 1\right)\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[y^{2} \left(\frac{x}{2} + \frac{1}{2}\right)\right]_{y=0}^{y=2}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(2 x + 2\right) + 0\right)\,\mathrm{d}x \\  & =\left[x^{2} + 2 x\right]_{x=0}^{x=1} \\  & =0 + 3 \\  & =3\end{aligned}
$$

### Generated variant of observed bank q-160888 (uniform scaling; error intent unresolved)

Evaluate the surface integral

$$
\iint_S \left\langle 2 y + 2 z,\,4 y + 2 z,\,2 x y\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the surface $S$ is defined by $z=x - y$ for $0\le x\le 1$ and $0\le y\le 2.$

- $9$
- $24$
- $6$
- $\frac{9}{2}$
- $16$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(x - y\right)=1 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(x - y\right)=-1\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 2 y + 2 z,\,4 y + 2 z,\,2 x y\right\rangle\big|_{z=x - y} \\  & =\left\langle 2 y + 2 \left(x - y\right),\,4 y + 2 \left(x - y\right),\,2 x y\right\rangle \\  & =\left\langle \underbrace{2 x}_{P},\,\underbrace{2 x + 2 y}_{Q},\,\underbrace{2 x y}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 2 y + 2 z,\,4 y + 2 z,\,2 x y\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2 x\right)\left(1\right)-\left(2 x + 2 y\right)\left(-1\right)+\left(2 x y\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(2 x y - 2 x + 2 x + 2 y\right)\,\mathrm{d}A \\  & =\iint_D\left(2 y \left(x + 1\right)\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{0}^{2}\left(2 y \left(x + 1\right)\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[y^{2} \left(x + 1\right)\right]_{y=0}^{y=2}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(4 x + 4\right) + 0\right)\,\mathrm{d}x \\  & =\left[2 x^{2} + 4 x\right]_{x=0}^{x=1} \\  & =0 + 6 \\  & =6\end{aligned}
$$

## Original q-161553

Calculate the flux of the vector field

$$
F(x,y,z)=⟨{e}^{x},\,{e}^{y},\,z+1⟩,
$$

where the surface $S$ is defined by $z=-x-y$ for $0\le x\le 1$ and $0\le y\le 1.$

- $3e-2$
- $e-3$
- $2e-2$ (correct)
- $2e-3$
- $e-2$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}(-x-y)=-1 \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}(-x-y)=-1\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
{∬}_{S}⟨{e}^{x},\,{e}^{y},\,z+1⟩\cdot \text{d}S
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =⟨{e}^{x},\,{e}^{y},\,z+1⟩{|}_{z=-x-y} \\  & =⟨{{{e}^{x}}_{⏟}}_{P},\,{{{e}^{y}}_{⏟}}_{Q},\,{{1-x-y}_{⏟}}_{R}⟩\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}{∬}_{S}⟨{e}^{x},\,{e}^{y},\,z+1⟩\cdot \text{d}S & ={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A \\  & ={∬}_{D}(-({e}^{x})\cdot (-1)-({e}^{y})\cdot (-1)+1-x-y)\,\text{d}A \\  & ={∬}_{D}({e}^{x}+{e}^{y}+1-x-y)\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{0}^{1}({e}^{x}+{e}^{y}+1-x-y)\,\text{d}y\,\text{d}x \\  & ={\int }_{0}^{1}{[{e}^{x}y+{e}^{y}+y-xy-\frac{{y}^{2}}{2}]}_{0}^{1}\,\text{d}x \\  & ={\int }_{0}^{1}({e}^{x}+e+1-x-\frac{1}{2}-1)\,\text{d}x \\  & ={\int }_{0}^{1}({e}^{x}-x-\frac{1}{2}+e)\,\text{d}x \\  & ={[{e}^{x}-\frac{{x}^{2}}{2}-\frac{x}{2}+ex]}_{0}^{1} \\  & =e-\frac{1}{2}-\frac{1}{2}+e-1 \\  & =2e-2\end{aligned}
$$

### Generated observed-profile replay q-161553

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle e^{x},\,e^{y},\,z + 1\right\rangle,
$$

where the surface $S$ is defined by $z=- x - y$ for $0\le x\le 1$ and $0\le y\le 1.$

- $-2 + 2 e$
- $-3 + e$
- $-2 + 3 e$
- $-2 + e$
- $-3 + 2 e$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(- x - y\right)=-1 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(- x - y\right)=-1\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle e^{x},\,e^{y},\,z + 1\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle e^{x},\,e^{y},\,z + 1\right\rangle\big|_{z=- x - y} \\  & =\left\langle \underbrace{e^{x}}_{P},\,\underbrace{e^{y}}_{Q},\,\underbrace{- x - y + 1}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle e^{x},\,e^{y},\,z + 1\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(e^{x}\right)\left(-1\right)-\left(e^{y}\right)\left(-1\right)+\left(- x - y + 1\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- x - y + e^{x} + e^{y} + 1\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{0}^{1}\left(- x - y + e^{x} + e^{y} + 1\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[- \frac{y^{2}}{2} + y \left(- x + e^{x} + 1\right) + e^{y}\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(- x + e^{x} + \frac{1}{2} + e\right) - 1\right)\,\mathrm{d}x \\  & =\int_{0}^{1}\left(- x + e^{x} - \frac{1}{2} + e\right)\,\mathrm{d}x \\  & =\left[- \frac{x^{2}}{2} + x \left(- \frac{1}{2} + e\right) + e^{x}\right]_{x=0}^{x=1} \\  & =-1 - \left(1 - 2 e\right) \\  & =-2 + 2 e\end{aligned}
$$

### Generated variant of observed bank q-161553 (uniform scaling; error intent unresolved)

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle 2 e^{x},\,2 e^{y},\,2 z + 2\right\rangle,
$$

where the surface $S$ is defined by $z=- x - y$ for $0\le x\le 1$ and $0\le y\le 1.$

- $-4 + 4 e$
- $-6 + 2 e$
- $-4 + 6 e$
- $-4 + 2 e$
- $-6 + 4 e$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(- x - y\right)=-1 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(- x - y\right)=-1\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle 2 e^{x},\,2 e^{y},\,2 z + 2\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 2 e^{x},\,2 e^{y},\,2 z + 2\right\rangle\big|_{z=- x - y} \\  & =\left\langle \underbrace{2 e^{x}}_{P},\,\underbrace{2 e^{y}}_{Q},\,\underbrace{- 2 x - 2 y + 2}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 2 e^{x},\,2 e^{y},\,2 z + 2\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2 e^{x}\right)\left(-1\right)-\left(2 e^{y}\right)\left(-1\right)+\left(- 2 x - 2 y + 2\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- 2 x - 2 y + 2 e^{x} + 2 e^{y} + 2\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{0}^{1}\left(- 2 x - 2 y + 2 e^{x} + 2 e^{y} + 2\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[- y^{2} + y \left(- 2 x + 2 e^{x} + 2\right) + 2 e^{y}\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(- 2 x + 2 e^{x} + 1 + 2 e\right) - 2\right)\,\mathrm{d}x \\  & =\int_{0}^{1}\left(- 2 x + 2 e^{x} - 1 + 2 e\right)\,\mathrm{d}x \\  & =\left[- x^{2} + x \left(-1 + 2 e\right) + 2 e^{x}\right]_{x=0}^{x=1} \\  & =-2 - \left(2 - 4 e\right) \\  & =-4 + 4 e\end{aligned}
$$

## Original q-161382

Evaluate the surface integral

$$
{∬}_{S}⟨-x,\,-y,\,xyz⟩\cdot \text{d}S
$$

where the surface $S$ is defined by $z=2x+y$ for $0\le x\le 1$ and $0\le y\le 1.$

- $3$
- $\frac{3}{2}$
- $\frac{11}{6}$
- $\frac{5}{6}$
- $2$ (correct)

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}(2x+y)=2 \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}(2x+y)=1\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =⟨-x,\,-y,\,xyz⟩{|}_{z=2x+y} \\  & =⟨-x,\,-y,\,xy(2x+y)⟩ \\  & =⟨{{-x}_{⏟}}_{P},\,{{-y}_{⏟}}_{Q},\,{{xy(2x+y)}_{⏟}}_{R}⟩\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}{∬}_{S}⟨-x,\,-y,\,xyz⟩\cdot \text{d}S & ={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A \\  & ={∬}_{D}(-(-x)\cdot 2-(-y)\cdot (1)+xy(2x+y))\,\text{d}A \\  & ={∬}_{D}(2x+y+2{x}^{2}y+x{y}^{2})\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{0}^{1}(2x+y+2{x}^{2}y+x{y}^{2})\,\text{d}y\,\text{d}x \\  & ={\int }_{0}^{1}{[2xy+\frac{{y}^{2}}{2}+{x}^{2}{y}^{2}+\frac{x{y}^{3}}{3}]}_{y=0}^{y=1}\,\text{d}x \\  & ={\int }_{0}^{1}(2x+\frac{1}{2}+{x}^{2}+\frac{x}{3})\,\text{d}x \\  & ={\int }_{0}^{1}({x}^{2}+\frac{7x}{3}+\frac{1}{2})\,\text{d}x \\  & ={[\frac{{x}^{3}}{3}+\frac{7{x}^{2}}{6}+\frac{x}{2}]}_{0}^{1} \\  & =\frac{1}{3}+\frac{7}{6}+\frac{1}{2} \\  & =2.\end{aligned}
$$

### Generated observed-profile replay q-161382

Evaluate the surface integral

$$
\iint_S \left\langle - x,\,- y,\,x y z\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the surface $S$ is defined by $z=2 x + y$ for $0\le x\le 1$ and $0\le y\le 1.$

- $\frac{11}{6}$
- $\frac{3}{2}$
- $3$
- $2$
- $\frac{5}{6}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(2 x + y\right)=2 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(2 x + y\right)=1\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle - x,\,- y,\,x y z\right\rangle\big|_{z=2 x + y} \\  & =\left\langle - x,\,- y,\,x y \left(2 x + y\right)\right\rangle \\  & =\left\langle \underbrace{- x}_{P},\,\underbrace{- y}_{Q},\,\underbrace{x y \left(2 x + y\right)}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle - x,\,- y,\,x y z\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(- x\right)\left(2\right)-\left(- y\right)\left(1\right)+\left(x y \left(2 x + y\right)\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(x y \left(2 x + y\right) + 2 x + y\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{0}^{1}\left(x y \left(2 x + y\right) + 2 x + y\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[\frac{x y^{3}}{3} + 2 x y + y^{2} \left(x^{2} + \frac{1}{2}\right)\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(x^{2} + \frac{7 x}{3} + \frac{1}{2}\right) + 0\right)\,\mathrm{d}x \\  & =\int_{0}^{1}\left(x^{2} + \frac{7 x}{3} + \frac{1}{2}\right)\,\mathrm{d}x \\  & =\left[\frac{x^{3}}{3} + \frac{7 x^{2}}{6} + \frac{x}{2}\right]_{x=0}^{x=1} \\  & =0 + 2 \\  & =2\end{aligned}
$$

### Generated variant of observed bank q-161382 (uniform scaling; error intent unresolved)

Evaluate the surface integral

$$
\iint_S \left\langle - 2 x,\,- 2 y,\,2 x y z\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the surface $S$ is defined by $z=2 x + y$ for $0\le x\le 1$ and $0\le y\le 1.$

- $\frac{11}{3}$
- $3$
- $6$
- $4$
- $\frac{5}{3}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(2 x + y\right)=2 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(2 x + y\right)=1\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle - 2 x,\,- 2 y,\,2 x y z\right\rangle\big|_{z=2 x + y} \\  & =\left\langle - 2 x,\,- 2 y,\,2 x y \left(2 x + y\right)\right\rangle \\  & =\left\langle \underbrace{- 2 x}_{P},\,\underbrace{- 2 y}_{Q},\,\underbrace{2 x y \left(2 x + y\right)}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle - 2 x,\,- 2 y,\,2 x y z\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(- 2 x\right)\left(2\right)-\left(- 2 y\right)\left(1\right)+\left(2 x y \left(2 x + y\right)\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(2 x y \left(2 x + y\right) + 4 x + 2 y\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{0}^{1}\left(2 x y \left(2 x + y\right) + 4 x + 2 y\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[\frac{2 x y^{3}}{3} + 4 x y + y^{2} \left(2 x^{2} + 1\right)\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(2 x^{2} + \frac{14 x}{3} + 1\right) + 0\right)\,\mathrm{d}x \\  & =\int_{0}^{1}\left(2 x^{2} + \frac{14 x}{3} + 1\right)\,\mathrm{d}x \\  & =\left[\frac{2 x^{3}}{3} + \frac{7 x^{2}}{3} + x\right]_{x=0}^{x=1} \\  & =0 + 4 \\  & =4\end{aligned}
$$

## Original q-161435

Evaluate the surface integral

$$
{∬}_{S}⟨xy,\,x+y,\,{e}^{z}⟩\cdot \text{d}S
$$

where the surface $S$ is defined by $z=x+y$ for $0\le x\le 1$ and $0\le y\le x.$

- $\frac{4{e}^{2}-8e}{8}$
- $\frac{4{e}^{2}-8e-1}{8}$ (correct)
- $\frac{8e-1}{8}$
- $\frac{4{e}^{2}-1}{8}$
- $\frac{4{e}^{2}+1}{8}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}(x+y)=1 \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}(x+y)=1\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =⟨xy,\,x+y,\,{e}^{z}⟩{|}_{z=x+y} \\  & =⟨xy,\,x+y,\,{e}^{x+y}⟩ \\  & =⟨{{xy}_{⏟}}_{P},\,{{x+y}_{⏟}}_{Q},\,{{{e}^{x+y}}_{⏟}}_{R}⟩\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}{∬}_{S}⟨xy,\,x+y,\,{e}^{z}⟩\cdot \text{d}S & ={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A \\  & ={∬}_{D}(-(xy)\cdot 1-(x+y)\cdot 1+{e}^{x+y})\,\text{d}A \\  & ={∬}_{D}(-xy-x-y+{e}^{x+y})\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{0}^{x}(-xy-x-y+{e}^{x+y})\,\text{d}y\,\text{d}x \\  & ={\int }_{0}^{1}{[-\frac{x{y}^{2}}{2}-xy-\frac{{y}^{2}}{2}+{e}^{x+y}]}_{y=0}^{y=x}\,\text{d}x \\  & ={\int }_{0}^{1}(-\frac{{x}^{3}}{2}-{x}^{2}-\frac{{x}^{2}}{2}+{e}^{2x}-{e}^{x})\,\text{d}x \\  & ={\int }_{0}^{1}(-\frac{{x}^{3}}{2}-\frac{3{x}^{2}}{2}+{e}^{2x}-{e}^{x})\,\text{d}x \\  & ={[-\frac{{x}^{4}}{8}-\frac{{x}^{3}}{2}+\frac{{e}^{2x}}{2}-{e}^{x}]}_{0}^{1} \\  & =(-\frac{1}{8}-\frac{1}{2}+\frac{{e}^{2}}{2}-e)-(0+\frac{1}{2}-1) \\  & =\frac{4{e}^{2}-8e-1}{8}.\end{aligned}
$$

### Generated observed-profile replay q-161435

Evaluate the surface integral

$$
\iint_S \left\langle x y,\,x + y,\,e^{z}\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the surface $S$ is defined by $z=x + y$ for $0\le x\le 1$ and $0\le y\le x.$

- $- \frac{1}{8} + e$
- $- e - \frac{1}{8} + \frac{e^{2}}{2}$
- $- e + \frac{e^{2}}{2}$
- $\frac{1}{8} + \frac{e^{2}}{2}$
- $- \frac{1}{8} + \frac{e^{2}}{2}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(x + y\right)=1 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(x + y\right)=1\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle x y,\,x + y,\,e^{z}\right\rangle\big|_{z=x + y} \\  & =\left\langle x y,\,x + y,\,e^{\left(x + y\right)}\right\rangle \\  & =\left\langle \underbrace{x y}_{P},\,\underbrace{x + y}_{Q},\,\underbrace{e^{x + y}}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle x y,\,x + y,\,e^{z}\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(x y\right)\left(1\right)-\left(x + y\right)\left(1\right)+\left(e^{x + y}\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- x y - x - y + e^{x + y}\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{0}^{x}\left(- x y - x - y + e^{x + y}\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[- x y + y^{2} \left(- \frac{x}{2} - \frac{1}{2}\right) + e^{x + y}\right]_{y=0}^{y=x}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(x^{2} \left(- \frac{x}{2} - \frac{1}{2}\right) - x^{2} + e^{2 x}\right) - e^{x}\right)\,\mathrm{d}x \\  & =\int_{0}^{1}\left(- \frac{x^{3}}{2} - \frac{3 x^{2}}{2} + e^{2 x} - e^{x}\right)\,\mathrm{d}x \\  & =\left[- \frac{x^{4}}{8} - \frac{x^{3}}{2} + \frac{e^{2 x}}{2} - e^{x}\right]_{x=0}^{x=1} \\  & =\left(- e - \frac{5}{8} + \frac{e^{2}}{2}\right) + \frac{1}{2} \\  & =- e - \frac{1}{8} + \frac{e^{2}}{2}\end{aligned}
$$

### Generated variant of observed bank q-161435 (uniform scaling; error intent unresolved)

Evaluate the surface integral

$$
\iint_S \left\langle 2 x y,\,2 x + 2 y,\,2 e^{z}\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the surface $S$ is defined by $z=x + y$ for $0\le x\le 1$ and $0\le y\le x.$

- $- \frac{1}{4} + 2 e$
- $- 2 e - \frac{1}{4} + e^{2}$
- $- 2 e + e^{2}$
- $\frac{1}{4} + e^{2}$
- $- \frac{1}{4} + e^{2}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(x + y\right)=1 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(x + y\right)=1\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 2 x y,\,2 x + 2 y,\,2 e^{z}\right\rangle\big|_{z=x + y} \\  & =\left\langle 2 x y,\,2 x + 2 y,\,2 e^{\left(x + y\right)}\right\rangle \\  & =\left\langle \underbrace{2 x y}_{P},\,\underbrace{2 x + 2 y}_{Q},\,\underbrace{2 e^{x + y}}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 2 x y,\,2 x + 2 y,\,2 e^{z}\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2 x y\right)\left(1\right)-\left(2 x + 2 y\right)\left(1\right)+\left(2 e^{x + y}\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- 2 x y - 2 x - 2 y + 2 e^{x + y}\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{0}^{x}\left(- 2 x y - 2 x - 2 y + 2 e^{x + y}\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[- 2 x y + y^{2} \left(- x - 1\right) + 2 e^{x + y}\right]_{y=0}^{y=x}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(x^{2} \left(- x - 1\right) - 2 x^{2} + 2 e^{2 x}\right) - 2 e^{x}\right)\,\mathrm{d}x \\  & =\int_{0}^{1}\left(- x^{3} - 3 x^{2} + 2 e^{2 x} - 2 e^{x}\right)\,\mathrm{d}x \\  & =\left[- \frac{x^{4}}{4} - x^{3} + e^{2 x} - 2 e^{x}\right]_{x=0}^{x=1} \\  & =\left(- 2 e - \frac{5}{4} + e^{2}\right) + 1 \\  & =- 2 e - \frac{1}{4} + e^{2}\end{aligned}
$$

## Original q-161481

Evaluate the surface integral

$$
{∬}_{S}⟨1,\,0,\,y⟩\cdot \text{d}S
$$

where the surface $S$ is defined by $z=\operatorname{cos}⁡(x+y)$ for $-\pi \le x\le 0$ and $-x\le y\le 0.$

- $\pi +\frac{{\pi }^{2}}{3}$
- $\pi -\frac{{\pi }^{3}}{6}$ (correct)
- $\pi +\frac{{\pi }^{2}}{12}$
- $\frac{\pi }{4}$
- $\frac{\pi }{2}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}\operatorname{cos}⁡(x+y)=-\operatorname{sin}⁡(x+y) \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}\operatorname{cos}⁡(x+y)=-\operatorname{sin}⁡(x+y)\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =⟨1,\,0,\,y⟩{|}_{z=\operatorname{cos}⁡(x+y)} \\  & =⟨{{1}_{⏟}}_{P},\,{{0}_{⏟}}_{Q},\,{{y}_{⏟}}_{R}⟩\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}{∬}_{S}⟨1,\,0,\,y⟩\cdot \text{d}S & ={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A \\  & ={∬}_{D}(-1\cdot (-\operatorname{sin}⁡(x+y))-0\cdot (-\operatorname{sin}⁡(x+y))+y)\,\text{d}A \\  & ={∬}_{D}(\operatorname{sin}⁡(x+y)+y)\,\text{d}A \\  & ={\int }_{-\pi }^{0}{\int }_{-x}^{0}(\operatorname{sin}⁡(x+y)+y)\,\text{d}y\,\text{d}x \\  & ={\int }_{-\pi }^{0}{[-\operatorname{cos}⁡(x+y)+\frac{{y}^{2}}{2}]}_{y=-x}^{y=0}\,\text{d}x \\  & ={\int }_{-\pi }^{0}(-\operatorname{cos}⁡x+0)-(-\operatorname{cos}⁡0+\frac{{x}^{2}}{2})\,\text{d}x \\  & ={\int }_{-\pi }^{0}(-\operatorname{cos}⁡x+1-\frac{{x}^{2}}{2})\,\text{d}x \\  & ={[-\operatorname{sin}⁡x+x-\frac{{x}^{3}}{6}]}_{-\pi }^{0} \\  & =0-(-0+(-\pi )-\frac{(-\pi )^{3}}{6}) \\  & =\pi -\frac{{\pi }^{3}}{6}\end{aligned}
$$

### Generated observed-profile replay q-161481 — QUARANTINED formal integral; original geometric domain is empty

Evaluate the surface integral

$$
\iint_S \left\langle 1,\,0,\,y\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the surface $S$ is defined by $z=\cos{\left(x + y \right)}$ for $- \pi\le x\le 0$ and $- x\le y\le 0.$

- $\frac{\pi^{2}}{12} + \pi$
- $\pi - \frac{\pi^{3}}{6}$
- $\pi + \frac{\pi^{2}}{3}$
- $\frac{\pi}{2}$
- $\frac{\pi}{4}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(\cos{\left(x + y \right)}\right)=- \sin{\left(x + y \right)} \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(\cos{\left(x + y \right)}\right)=- \sin{\left(x + y \right)}\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 1,\,0,\,y\right\rangle\big|_{z=\cos{\left(x + y \right)}} \\  & =\left\langle \underbrace{1}_{P},\,\underbrace{0}_{Q},\,\underbrace{y}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 1,\,0,\,y\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(1\right)\left(- \sin{\left(x + y \right)}\right)-\left(0\right)\left(- \sin{\left(x + y \right)}\right)+\left(y\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(y + \sin{\left(x + y \right)} + 0\right)\,\mathrm{d}A \\  & =\int_{- \pi}^{0}\int_{- x}^{0}\left(y + \sin{\left(x + y \right)}\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{- \pi}^{0}\left[\frac{y^{2}}{2} - \cos{\left(x + y \right)}\right]_{y=- x}^{y=0}\,\mathrm{d}x \\  & =\int_{- \pi}^{0}\left(\left(1 - \frac{x^{2}}{2}\right) - \cos{\left(x \right)}\right)\,\mathrm{d}x \\  & =\int_{- \pi}^{0}\left(- \frac{x^{2}}{2} - \cos{\left(x \right)} + 1\right)\,\mathrm{d}x \\  & =\left[- \frac{x^{3}}{6} + x - \sin{\left(x \right)}\right]_{x=- \pi}^{x=0} \\  & =\left(\pi - \frac{\pi^{3}}{6}\right) + 0 \\  & =\pi - \frac{\pi^{3}}{6}\end{aligned}
$$

### Generated variant of observed bank q-161481 (uniform scaling; error intent unresolved; QUARANTINED formal integral)

Evaluate the surface integral

$$
\iint_S \left\langle 2,\,0,\,2 y\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the surface $S$ is defined by $z=\cos{\left(x + y \right)}$ for $- \pi\le x\le 0$ and $- x\le y\le 0.$

- $\frac{\pi^{2}}{6} + 2 \pi$
- $- \frac{\pi^{3}}{3} + 2 \pi$
- $2 \pi + \frac{2 \pi^{2}}{3}$
- $\pi$
- $\frac{\pi}{2}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(\cos{\left(x + y \right)}\right)=- \sin{\left(x + y \right)} \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(\cos{\left(x + y \right)}\right)=- \sin{\left(x + y \right)}\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 2,\,0,\,2 y\right\rangle\big|_{z=\cos{\left(x + y \right)}} \\  & =\left\langle \underbrace{2}_{P},\,\underbrace{0}_{Q},\,\underbrace{2 y}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 2,\,0,\,2 y\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2\right)\left(- \sin{\left(x + y \right)}\right)-\left(0\right)\left(- \sin{\left(x + y \right)}\right)+\left(2 y\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(2 y + 2 \sin{\left(x + y \right)} + 0\right)\,\mathrm{d}A \\  & =\int_{- \pi}^{0}\int_{- x}^{0}\left(2 y + 2 \sin{\left(x + y \right)}\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{- \pi}^{0}\left[y^{2} - 2 \cos{\left(x + y \right)}\right]_{y=- x}^{y=0}\,\mathrm{d}x \\  & =\int_{- \pi}^{0}\left(\left(2 - x^{2}\right) - 2 \cos{\left(x \right)}\right)\,\mathrm{d}x \\  & =\int_{- \pi}^{0}\left(- x^{2} - 2 \cos{\left(x \right)} + 2\right)\,\mathrm{d}x \\  & =\left[- \frac{x^{3}}{3} + 2 x - 2 \sin{\left(x \right)}\right]_{x=- \pi}^{x=0} \\  & =\left(- \frac{\pi^{3}}{3} + 2 \pi\right) + 0 \\  & =\frac{\pi \left(6 - \pi^{2}\right)}{3}\end{aligned}
$$

## Original q-161536

Calculate the flux of the vector field

$$
F(x,y,z)=⟨y,\,x+z,\,0⟩,
$$

where the surface $S$ is defined by $z={e}^{x}$ for $-1\le x\le 1$ and $0\le y\le 1.$

- $\frac{3e-{e}^{-1}}{4}$
- $\frac{{e}^{-1}-e}{2}$ (correct)
- $-\frac{5e+2{e}^{-1}}{4}$
- $\frac{7e-{e}^{-1}}{2}$
- $-\frac{3e+{e}^{-1}}{2}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}({e}^{x})={e}^{x} \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}({e}^{x})=0\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
{∬}_{S}⟨y,\,x+z,\,0⟩\cdot \text{d}S
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =⟨y,\,x+z,\,0⟩{|}_{z={e}^{x}} \\  & =⟨{{y}_{⏟}}_{P},\,{{x+{e}^{x}}_{⏟}}_{Q},\,{{0}_{⏟}}_{R}⟩\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}{∬}_{S}⟨y,\,x+z,\,0⟩\cdot \text{d}S & ={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A \\  & ={∬}_{D}(-y\cdot ({e}^{x})-(x+{e}^{x})\cdot 0+0)\,\text{d}A \\  & ={∬}_{D}(-y{e}^{x})\,\text{d}A \\  & ={\int }_{-1}^{1}{\int }_{0}^{1}(-y{e}^{x})\,\text{d}y\,\text{d}x \\  & ={\int }_{-1}^{1}{[-\frac{{y}^{2}{e}^{x}}{2}]}_{y=0}^{y=1}\,\text{d}x \\  & =-\frac{1}{2}{\int }_{-1}^{1}{e}^{x}\,\text{d}x \\  & =-\frac{1}{2}{[{e}^{x}]}_{-1}^{1} \\  & =\frac{{e}^{-1}-e}{2}\end{aligned}
$$

### Generated observed-profile replay q-161536

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle y,\,x + z,\,0\right\rangle,
$$

where the surface $S$ is defined by $z=e^{x}$ for $-1\le x\le 1$ and $0\le y\le 1.$

- $- \frac{5 e}{4} - \frac{1}{2 e}$
- $- \frac{e}{2} + \frac{1}{2 e}$
- $- \frac{1}{4 e} + \frac{3 e}{4}$
- $- \frac{3 e}{2} - \frac{1}{2 e}$
- $- \frac{1}{2 e} + \frac{7 e}{2}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(e^{x}\right)=e^{x} \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(e^{x}\right)=0\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle y,\,x + z,\,0\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle y,\,x + z,\,0\right\rangle\big|_{z=e^{x}} \\  & =\left\langle \underbrace{y}_{P},\,\underbrace{x + e^{x}}_{Q},\,\underbrace{0}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle y,\,x + z,\,0\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(y\right)\left(e^{x}\right)-\left(x + e^{x}\right)\left(0\right)+\left(0\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- y e^{x} + 0 + 0\right)\,\mathrm{d}A \\  & =\int_{-1}^{1}\int_{0}^{1}\left(- y e^{x}\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{-1}^{1}\left[- \frac{y^{2} e^{x}}{2}\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{-1}^{1}\left(- \frac{e^{x}}{2} + 0\right)\,\mathrm{d}x \\  & =\left[- \frac{e^{x}}{2}\right]_{x=-1}^{x=1} \\  & =- \frac{e}{2} + \frac{1}{2 e}\end{aligned}
$$

### Generated variant of observed bank q-161536 (uniform scaling; error intent unresolved)

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle 2 y,\,2 x + 2 z,\,0\right\rangle,
$$

where the surface $S$ is defined by $z=e^{x}$ for $-1\le x\le 1$ and $0\le y\le 1.$

- $- \frac{5 e}{2} - e^{-1}$
- $- e + e^{-1}$
- $- \frac{1}{2 e} + \frac{3 e}{2}$
- $- 3 e - e^{-1}$
- $- \frac{1}{e} + 7 e$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(e^{x}\right)=e^{x} \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(e^{x}\right)=0\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle 2 y,\,2 x + 2 z,\,0\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 2 y,\,2 x + 2 z,\,0\right\rangle\big|_{z=e^{x}} \\  & =\left\langle \underbrace{2 y}_{P},\,\underbrace{2 x + 2 e^{x}}_{Q},\,\underbrace{0}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 2 y,\,2 x + 2 z,\,0\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2 y\right)\left(e^{x}\right)-\left(2 x + 2 e^{x}\right)\left(0\right)+\left(0\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- 2 y e^{x} + 0 + 0\right)\,\mathrm{d}A \\  & =\int_{-1}^{1}\int_{0}^{1}\left(- 2 y e^{x}\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{-1}^{1}\left[- y^{2} e^{x}\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{-1}^{1}\left(- e^{x} + 0\right)\,\mathrm{d}x \\  & =\left[- e^{x}\right]_{x=-1}^{x=1} \\  & =- e + e^{-1}\end{aligned}
$$

## Original q-161539

Calculate the flux of the vector field

$$
F(x,y,z)=⟨{cos}^{2}⁡(xy),\,{cos}^{2}⁡(xy),\,1⟩,
$$

where the surface $S$ is defined by $z=\operatorname{tan}⁡(xy)$ for $0\le x\le 1$ and $-x\le y\le 0.$

- $\frac{1}{3}$ (correct)
- $\frac{\pi }{2}$
- $\frac{5}{6}$
- $\pi -1$
- $0$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}(\operatorname{tan}⁡(xy))=\frac{y}{{cos}^{2}⁡(xy)} \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}(\operatorname{tan}⁡(xy))=\frac{x}{{cos}^{2}⁡(xy)}\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
{∬}_{S}⟨{cos}^{2}⁡(xy),\,{cos}^{2}⁡(xy),\,1⟩\cdot \text{d}S
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =⟨{cos}^{2}⁡(xy),\,{cos}^{2}⁡(xy),\,1⟩{|}_{z=\operatorname{tan}⁡(xy)} \\  & =⟨{{{cos}^{2}⁡(xy)}_{⏟}}_{P},\,{{{cos}^{2}⁡(xy)}_{⏟}}_{Q},\,{{1}_{⏟}}_{R}⟩\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}{∬}_{S}⟨{cos}^{2}⁡(xy),\,{cos}^{2}⁡(xy),\,1⟩\cdot \text{d}S & ={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A \\  & ={∬}_{D}(-({cos}^{2}⁡(xy))\cdot (\frac{y}{{cos}^{2}⁡(xy)})-({cos}^{2}⁡(xy))\cdot (\frac{x}{{cos}^{2}⁡(xy)})+1)\,\text{d}A \\  & ={∬}_{D}(-y-x+1)\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{-x}^{0}(-y-x+1)\,dy\,dx \\  & ={\int }_{0}^{1}{[-\frac{{y}^{2}}{2}-xy+y]}_{y=-x}^{y=0}\,dx \\  & ={\int }_{0}^{1}(\frac{{x}^{2}}{2}-{x}^{2}+x)\,dx \\  & ={\int }_{0}^{1}(-\frac{{x}^{2}}{2}+x)\,dx \\  & ={[-\frac{{x}^{3}}{6}+\frac{{x}^{2}}{2}]}_{0}^{1} \\  & =-\frac{1}{6}+\frac{1}{2} \\  & =\frac{1}{3}\end{aligned}
$$

### Generated observed-profile replay q-161539

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle \cos^{2}{\left(x y \right)},\,\cos^{2}{\left(x y \right)},\,1\right\rangle,
$$

where the surface $S$ is defined by $z=\tan{\left(x y \right)}$ for $0\le x\le 1$ and $- x\le y\le 0.$

- $\frac{5}{6}$
- $\frac{\pi}{2}$
- $\frac{1}{3}$
- $0$
- $-1 + \pi$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(\tan{\left(x y \right)}\right)=y \left(\tan^{2}{\left(x y \right)} + 1\right) \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(\tan{\left(x y \right)}\right)=x \left(\tan^{2}{\left(x y \right)} + 1\right)\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle \cos^{2}{\left(x y \right)},\,\cos^{2}{\left(x y \right)},\,1\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle \cos^{2}{\left(x y \right)},\,\cos^{2}{\left(x y \right)},\,1\right\rangle\big|_{z=\tan{\left(x y \right)}} \\  & =\left\langle \underbrace{\cos^{2}{\left(x y \right)}}_{P},\,\underbrace{\cos^{2}{\left(x y \right)}}_{Q},\,\underbrace{1}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle \cos^{2}{\left(x y \right)},\,\cos^{2}{\left(x y \right)},\,1\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(\cos^{2}{\left(x y \right)}\right)\left(y \left(\tan^{2}{\left(x y \right)} + 1\right)\right)-\left(\cos^{2}{\left(x y \right)}\right)\left(x \left(\tan^{2}{\left(x y \right)} + 1\right)\right)+\left(1\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- x - y + 1\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{- x}^{0}\left(- x - y + 1\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[- \frac{y^{2}}{2} + y \left(1 - x\right)\right]_{y=- x}^{y=0}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(\frac{x^{2}}{2} + x \left(1 - x\right)\right) + 0\right)\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\frac{x \left(2 - x\right)}{2}\right)\,\mathrm{d}x \\  & =\left[- \frac{x^{3}}{6} + \frac{x^{2}}{2}\right]_{x=0}^{x=1} \\  & =0 + \frac{1}{3} \\  & =\frac{1}{3}\end{aligned}
$$

### Generated variant of observed bank q-161539 (uniform scaling; error intent unresolved)

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle 2 \cos^{2}{\left(x y \right)},\,2 \cos^{2}{\left(x y \right)},\,2\right\rangle,
$$

where the surface $S$ is defined by $z=\tan{\left(x y \right)}$ for $0\le x\le 1$ and $- x\le y\le 0.$

- $\frac{5}{3}$
- $\pi$
- $\frac{2}{3}$
- $0$
- $-2 + 2 \pi$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(\tan{\left(x y \right)}\right)=y \left(\tan^{2}{\left(x y \right)} + 1\right) \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(\tan{\left(x y \right)}\right)=x \left(\tan^{2}{\left(x y \right)} + 1\right)\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle 2 \cos^{2}{\left(x y \right)},\,2 \cos^{2}{\left(x y \right)},\,2\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 2 \cos^{2}{\left(x y \right)},\,2 \cos^{2}{\left(x y \right)},\,2\right\rangle\big|_{z=\tan{\left(x y \right)}} \\  & =\left\langle \underbrace{2 \cos^{2}{\left(x y \right)}}_{P},\,\underbrace{2 \cos^{2}{\left(x y \right)}}_{Q},\,\underbrace{2}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 2 \cos^{2}{\left(x y \right)},\,2 \cos^{2}{\left(x y \right)},\,2\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2 \cos^{2}{\left(x y \right)}\right)\left(y \left(\tan^{2}{\left(x y \right)} + 1\right)\right)-\left(2 \cos^{2}{\left(x y \right)}\right)\left(x \left(\tan^{2}{\left(x y \right)} + 1\right)\right)+\left(2\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- 2 x - 2 y + 2\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{- x}^{0}\left(- 2 x - 2 y + 2\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[- y^{2} + y \left(2 - 2 x\right)\right]_{y=- x}^{y=0}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(x^{2} + x \left(2 - 2 x\right)\right) + 0\right)\,\mathrm{d}x \\  & =\int_{0}^{1}\left(x \left(2 - x\right)\right)\,\mathrm{d}x \\  & =\left[- \frac{x^{3}}{3} + x^{2}\right]_{x=0}^{x=1} \\  & =0 + \frac{2}{3} \\  & =\frac{2}{3}\end{aligned}
$$

## Original q-161541

Calculate the flux of the vector field

$$
F(x,y,z)=⟨\sqrt{\frac{x}{y}},\,\sqrt{\frac{x}{y}},\,{z}^{2}+1⟩,
$$

where the surface $S$ is defined by $z=2\sqrt{xy}$ for $3\le x\le 4$ and $1\le y\le 2.$

- $\frac{7(3-\operatorname{ln}⁡2)}{2}$
- $\frac{7(2-\operatorname{ln}⁡4)}{2}$
- $\frac{7(3-\operatorname{ln}⁡4)}{2}$
- $\frac{7(6-\operatorname{ln}⁡2)}{2}$ (correct)
- $\frac{4(3-\operatorname{ln}⁡2)}{2}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}(2\sqrt{xy})=\sqrt{\frac{y}{x}} \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}(2\sqrt{xy})=\sqrt{\frac{x}{y}}\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
{∬}_{S}⟨\sqrt{\frac{x}{y}},\,\sqrt{\frac{x}{y}},\,{z}^{2}+1⟩\cdot \text{d}S
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =⟨\sqrt{\frac{x}{y}},\,\sqrt{\frac{x}{y}},\,{z}^{2}+1⟩{|}_{z=2\sqrt{xy}} \\  & =⟨{{\sqrt{\frac{x}{y}}}_{⏟}}_{P},\,{{\sqrt{\frac{x}{y}}}_{⏟}}_{Q},\,{{4xy+1}_{⏟}}_{R}⟩\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}{∬}_{S}⟨\sqrt{\frac{x}{y}},\,\sqrt{\frac{x}{y}},\,{z}^{2}+1⟩\cdot \text{d}S & ={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A \\  & ={∬}_{D}(-\sqrt{\frac{x}{y}}\cdot \sqrt{\frac{y}{x}}-\sqrt{\frac{x}{y}}\cdot \sqrt{\frac{x}{y}}+4xy+1)\,\text{d}A \\  & ={∬}_{D}(-1-\frac{x}{y}+4xy+1)\,\text{d}A \\  & ={∬}_{D}(-\frac{x}{y}+4xy)\,\text{d}A \\  & ={\int }_{3}^{4}{\int }_{1}^{2}(-\frac{x}{y}+4xy)\,\text{d}y\,\text{d}x \\  & ={\int }_{3}^{4}{[-x\operatorname{ln}⁡y+2x{y}^{2}]}_{y=1}^{y=2}\,\text{d}x \\  & ={\int }_{3}^{4}(-x\operatorname{ln}⁡2+8x+0-2x)\,\text{d}x \\  & ={\int }_{3}^{4}(6-\operatorname{ln}⁡2)x\,\text{d}x \\  & =(6-\operatorname{ln}⁡2){[\frac{{x}^{2}}{2}]}_{3}^{4} \\  & =\frac{7(6-\operatorname{ln}⁡2)}{2}\end{aligned}
$$

### Generated observed-profile replay q-161541

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle \sqrt{\frac{x}{y}},\,\sqrt{\frac{x}{y}},\,z^{2} + 1\right\rangle,
$$

where the surface $S$ is defined by $z=2 \sqrt{x y}$ for $3\le x\le 4$ and $1\le y\le 2.$

- $\frac{21}{2} - \frac{7 \log{\left(4 \right)}}{2}$
- $7 - \frac{7 \log{\left(4 \right)}}{2}$
- $\frac{21}{2} - \frac{7 \log{\left(2 \right)}}{2}$
- $6 - 2 \log{\left(2 \right)}$
- $21 - \frac{7 \log{\left(2 \right)}}{2}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(2 \sqrt{x y}\right)=\frac{\sqrt{x y}}{x} \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(2 \sqrt{x y}\right)=\frac{\sqrt{x y}}{y}\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle \sqrt{\frac{x}{y}},\,\sqrt{\frac{x}{y}},\,z^{2} + 1\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle \sqrt{\frac{x}{y}},\,\sqrt{\frac{x}{y}},\,z^{2} + 1\right\rangle\big|_{z=2 \sqrt{x y}} \\  & =\left\langle \underbrace{\sqrt{\frac{x}{y}}}_{P},\,\underbrace{\sqrt{\frac{x}{y}}}_{Q},\,\underbrace{4 x y + 1}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle \sqrt{\frac{x}{y}},\,\sqrt{\frac{x}{y}},\,z^{2} + 1\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(\sqrt{\frac{x}{y}}\right)\left(\frac{\sqrt{x y}}{x}\right)-\left(\sqrt{\frac{x}{y}}\right)\left(\frac{\sqrt{x y}}{y}\right)+\left(4 x y + 1\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(4 x y - \frac{x}{y} - 1 + 1\right)\,\mathrm{d}A \\  & =\iint_D\left(4 x y - \frac{x}{y}\right)\,\mathrm{d}A \\  & =\int_{3}^{4}\int_{1}^{2}\left(4 x y - \frac{x}{y}\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{3}^{4}\left[2 x y^{2} - x \log{\left(y \right)}\right]_{y=1}^{y=2}\,\mathrm{d}x \\  & =\int_{3}^{4}\left(- 2 x + \left(- x \log{\left(2 \right)} + 8 x\right)\right)\,\mathrm{d}x \\  & =\int_{3}^{4}\left(x \left(6 - \log{\left(2 \right)}\right)\right)\,\mathrm{d}x \\  & =\left[x^{2} \left(3 - \frac{\log{\left(2 \right)}}{2}\right)\right]_{x=3}^{x=4} \\  & =21 - \frac{7 \log{\left(2 \right)}}{2}\end{aligned}
$$

### Generated variant of observed bank q-161541 (uniform scaling; error intent unresolved)

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle 2 \sqrt{\frac{x}{y}},\,2 \sqrt{\frac{x}{y}},\,2 z^{2} + 2\right\rangle,
$$

where the surface $S$ is defined by $z=2 \sqrt{x y}$ for $3\le x\le 4$ and $1\le y\le 2.$

- $21 - 7 \log{\left(4 \right)}$
- $14 - 7 \log{\left(4 \right)}$
- $21 - 7 \log{\left(2 \right)}$
- $12 - 4 \log{\left(2 \right)}$
- $42 - 7 \log{\left(2 \right)}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(2 \sqrt{x y}\right)=\frac{\sqrt{x y}}{x} \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(2 \sqrt{x y}\right)=\frac{\sqrt{x y}}{y}\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle 2 \sqrt{\frac{x}{y}},\,2 \sqrt{\frac{x}{y}},\,2 z^{2} + 2\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 2 \sqrt{\frac{x}{y}},\,2 \sqrt{\frac{x}{y}},\,2 z^{2} + 2\right\rangle\big|_{z=2 \sqrt{x y}} \\  & =\left\langle \underbrace{2 \sqrt{\frac{x}{y}}}_{P},\,\underbrace{2 \sqrt{\frac{x}{y}}}_{Q},\,\underbrace{8 x y + 2}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 2 \sqrt{\frac{x}{y}},\,2 \sqrt{\frac{x}{y}},\,2 z^{2} + 2\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2 \sqrt{\frac{x}{y}}\right)\left(\frac{\sqrt{x y}}{x}\right)-\left(2 \sqrt{\frac{x}{y}}\right)\left(\frac{\sqrt{x y}}{y}\right)+\left(8 x y + 2\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(8 x y - \frac{2 x}{y} - 2 + 2\right)\,\mathrm{d}A \\  & =\iint_D\left(8 x y - \frac{2 x}{y}\right)\,\mathrm{d}A \\  & =\int_{3}^{4}\int_{1}^{2}\left(8 x y - \frac{2 x}{y}\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{3}^{4}\left[4 x y^{2} - 2 x \log{\left(y \right)}\right]_{y=1}^{y=2}\,\mathrm{d}x \\  & =\int_{3}^{4}\left(- 4 x + \left(- 2 x \log{\left(2 \right)} + 16 x\right)\right)\,\mathrm{d}x \\  & =\int_{3}^{4}\left(2 x \left(6 - \log{\left(2 \right)}\right)\right)\,\mathrm{d}x \\  & =\left[x^{2} \left(6 - \log{\left(2 \right)}\right)\right]_{x=3}^{x=4} \\  & =42 - 7 \log{\left(2 \right)}\end{aligned}
$$

## Original q-161542

Calculate the flux of the vector field

$$
F(x,y,z)=⟨x+y,\,y-x,\,z⟩,
$$

where the surface $S$ is defined by $z=1+{x}^{2}+{y}^{2}$ for $-1\le x\le 1$ and $-1\le y\le 1.$

- $2$
- $4$
- $\frac{8}{3}$
- $0$
- $\frac{4}{3}$ (correct)

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}(1+{x}^{2}+{y}^{2})=2x \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}(1+{x}^{2}+{y}^{2})=2y\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
{∬}_{S}⟨x+y,\,y-x,\,z⟩\cdot \text{d}S
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =⟨x+y,\,y-x,\,z⟩{|}_{z=1+{x}^{2}+{y}^{2}} \\  & =⟨{{x+y}_{⏟}}_{P},\,{{y-x}_{⏟}}_{Q},\,{{1+{x}^{2}+{y}^{2}}_{⏟}}_{R}⟩\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}{∬}_{S}⟨x+y,\,y-x,\,z⟩\cdot \text{d}S & ={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A \\  & ={∬}_{D}(-(x+y)\cdot (2x)-(y-x)\cdot (2y)+1+{x}^{2}+{y}^{2})\,\text{d}A \\  & ={∬}_{D}(-2{x}^{2}-2xy-2{y}^{2}+2xy+1+{x}^{2}+{y}^{2})\,\text{d}A \\  & ={\int }_{-1}^{1}{\int }_{-1}^{1}(1-{x}^{2}-{y}^{2})\,\text{d}y\,\text{d}x \\  & ={\int }_{-1}^{1}{[y-{x}^{2}y-\frac{{y}^{3}}{3}]}_{y=-1}^{y=1}\,\text{d}x \\  & ={\int }_{-1}^{1}[(1-{x}^{2}-\frac{1}{3})-(-1+{x}^{2}+\frac{1}{3})]\,\text{d}x \\  & ={\int }_{-1}^{1}(2-2{x}^{2}-\frac{2}{3})\,\text{d}x \\  & ={[2x-\frac{2{x}^{3}}{3}-\frac{2}{3}x]}_{-1}^{1} \\  & =(2-\frac{2}{3}-\frac{2}{3})-(-2+\frac{2}{3}+\frac{2}{3}) \\  & =\frac{4}{3}\end{aligned}
$$

### Generated observed-profile replay q-161542

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle x + y,\,- x + y,\,z\right\rangle,
$$

where the surface $S$ is defined by $z=x^{2} + y^{2} + 1$ for $-1\le x\le 1$ and $-1\le y\le 1.$

- $\frac{8}{3}$
- $4$
- $2$
- $\frac{4}{3}$
- $0$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(x^{2} + y^{2} + 1\right)=2 x \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(x^{2} + y^{2} + 1\right)=2 y\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle x + y,\,- x + y,\,z\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle x + y,\,- x + y,\,z\right\rangle\big|_{z=x^{2} + y^{2} + 1} \\  & =\left\langle \underbrace{x + y}_{P},\,\underbrace{- x + y}_{Q},\,\underbrace{x^{2} + y^{2} + 1}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle x + y,\,- x + y,\,z\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(x + y\right)\left(2 x\right)-\left(- x + y\right)\left(2 y\right)+\left(x^{2} + y^{2} + 1\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(x^{2} + 2 x \left(- x - y\right) + y^{2} + 2 y \left(x - y\right) + 1\right)\,\mathrm{d}A \\  & =\int_{-1}^{1}\int_{-1}^{1}\left(- x^{2} - y^{2} + 1\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{-1}^{1}\left[- \frac{y^{3}}{3} + y \left(1 - x^{2}\right)\right]_{y=-1}^{y=1}\,\mathrm{d}x \\  & =\int_{-1}^{1}\left(\left(\frac{2}{3} - x^{2}\right) - \left(x^{2} - \frac{2}{3}\right)\right)\,\mathrm{d}x \\  & =\int_{-1}^{1}\left(\frac{4}{3} - 2 x^{2}\right)\,\mathrm{d}x \\  & =\left[- \frac{2 x^{3}}{3} + \frac{4 x}{3}\right]_{x=-1}^{x=1} \\  & =\frac{2}{3} + \frac{2}{3} \\  & =\frac{4}{3}\end{aligned}
$$

### Generated variant of observed bank q-161542 (uniform scaling; error intent unresolved)

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle 2 x + 2 y,\,- 2 x + 2 y,\,2 z\right\rangle,
$$

where the surface $S$ is defined by $z=x^{2} + y^{2} + 1$ for $-1\le x\le 1$ and $-1\le y\le 1.$

- $\frac{16}{3}$
- $8$
- $4$
- $\frac{8}{3}$
- $0$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(x^{2} + y^{2} + 1\right)=2 x \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(x^{2} + y^{2} + 1\right)=2 y\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle 2 x + 2 y,\,- 2 x + 2 y,\,2 z\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 2 x + 2 y,\,- 2 x + 2 y,\,2 z\right\rangle\big|_{z=x^{2} + y^{2} + 1} \\  & =\left\langle \underbrace{2 x + 2 y}_{P},\,\underbrace{- 2 x + 2 y}_{Q},\,\underbrace{2 x^{2} + 2 y^{2} + 2}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 2 x + 2 y,\,- 2 x + 2 y,\,2 z\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2 x + 2 y\right)\left(2 x\right)-\left(- 2 x + 2 y\right)\left(2 y\right)+\left(2 x^{2} + 2 y^{2} + 2\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(2 x^{2} + 4 x \left(- x - y\right) + 2 y^{2} + 4 y \left(x - y\right) + 2\right)\,\mathrm{d}A \\  & =\int_{-1}^{1}\int_{-1}^{1}\left(- 2 x^{2} - 2 y^{2} + 2\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{-1}^{1}\left[- \frac{2 y^{3}}{3} + y \left(2 - 2 x^{2}\right)\right]_{y=-1}^{y=1}\,\mathrm{d}x \\  & =\int_{-1}^{1}\left(\left(\frac{4}{3} - 2 x^{2}\right) - \left(2 x^{2} - \frac{4}{3}\right)\right)\,\mathrm{d}x \\  & =\int_{-1}^{1}\left(\frac{8}{3} - 4 x^{2}\right)\,\mathrm{d}x \\  & =\left[- \frac{4 x^{3}}{3} + \frac{8 x}{3}\right]_{x=-1}^{x=1} \\  & =\frac{4}{3} + \frac{4}{3} \\  & =\frac{8}{3}\end{aligned}
$$

## Original q-161552

Calculate the flux of the vector field

$$
F(x,y,z)=⟨3{x}^{3}y,\,2yz,\,2x(y+z)⟩,
$$

where the surface $S$ is defined by $z=2x+y$ for $0\le x\le 2$ and $0\le y\le 1.$

- $-\frac{8}{3}$ (correct)
- $\frac{7}{3}$
- $-\frac{10}{3}$
- $-2$
- $-8$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}(2x+y)=2 \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}(2x+y)=1\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
{∬}_{S}⟨3{x}^{3}y,\,2yz,\,2x(y+z)⟩\cdot \text{d}S
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =⟨3{x}^{3}y,\,2yz,\,2xz⟩{|}_{z=2x+y} \\ F(x,y,g(x,y)) & =⟨3{x}^{3}y,\,2y(2x+y),\,2x(y+2x+y)⟩{|}_{z=2x+y} \\  & =⟨{{3{x}^{3}y}_{⏟}}_{P},\,{{4xy+2{y}^{2}}_{⏟}}_{Q},\,{{4xy+4{x}^{2}}_{⏟}}_{R}⟩\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}{∬}_{S}⟨3{x}^{3}y,\,2yz,\,2x(y+z)⟩\cdot \text{d}S & ={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A \\  & ={∬}_{D}(-(3{x}^{3}y)\cdot (2)-(4xy+2{y}^{2})\cdot (1)+4xy+4{x}^{2})\,\text{d}A \\  & ={∬}_{D}(-6{x}^{3}y-2{y}^{2}+4{x}^{2})\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{0}^{1}(-6{x}^{3}y-2{y}^{2}+4{x}^{2})\,\text{d}y\,\text{d}x \\  & ={\int }_{0}^{2}{[-3{x}^{3}{y}^{2}-\frac{2{y}^{3}}{3}+4{x}^{2}y]}_{0}^{1}\,\text{d}x \\  & ={\int }_{0}^{2}(-3{x}^{3}-\frac{2}{3}+4{x}^{2})\,\text{d}x \\  & ={[-\frac{3{x}^{4}}{4}-\frac{2x}{3}+\frac{4{x}^{3}}{3}]}_{0}^{2} \\  & =-12-\frac{4}{3}+\frac{32}{3} \\  & =-\frac{8}{3}\end{aligned}
$$

### Generated observed-profile replay q-161552 — first substitution vector repaired

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle 3 x^{3} y,\,2 y z,\,2 x \left(y + z\right)\right\rangle,
$$

where the surface $S$ is defined by $z=2 x + y$ for $0\le x\le 2$ and $0\le y\le 1.$

- $- \frac{10}{3}$
- $\frac{7}{3}$
- $- \frac{8}{3}$
- $-8$
- $-2$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(2 x + y\right)=2 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(2 x + y\right)=1\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle 3 x^{3} y,\,2 y z,\,2 x \left(y + z\right)\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 3 x^{3} y,\,2 y z,\,2 x \left(y + z\right)\right\rangle\big|_{z=2 x + y} \\  & =\left\langle 3 x^{3} y,\,2 y \left(2 x + y\right),\,2 x \left(y + \left(2 x + y\right)\right)\right\rangle \\  & =\left\langle \underbrace{3 x^{3} y}_{P},\,\underbrace{2 y \left(2 x + y\right)}_{Q},\,\underbrace{4 x \left(x + y\right)}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 3 x^{3} y,\,2 y z,\,2 x \left(y + z\right)\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(3 x^{3} y\right)\left(2\right)-\left(2 y \left(2 x + y\right)\right)\left(1\right)+\left(4 x \left(x + y\right)\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- 6 x^{3} y + 4 x \left(x + y\right) + 2 y \left(- 2 x - y\right)\right)\,\mathrm{d}A \\  & =\int_{0}^{2}\int_{0}^{1}\left(- 6 x^{3} y + 4 x^{2} - 2 y^{2}\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{2}\left[- 3 x^{3} y^{2} + 4 x^{2} y - \frac{2 y^{3}}{3}\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{0}^{2}\left(\left(- 3 x^{3} + 4 x^{2} - \frac{2}{3}\right) + 0\right)\,\mathrm{d}x \\  & =\left[- \frac{3 x^{4}}{4} + \frac{4 x^{3}}{3} - \frac{2 x}{3}\right]_{x=0}^{x=2} \\  & =- \frac{8}{3} + 0 \\  & =- \frac{8}{3}\end{aligned}
$$

### Generated variant of observed bank q-161552 (uniform scaling; error intent unresolved)

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle 6 x^{3} y,\,4 y z,\,4 x \left(y + z\right)\right\rangle,
$$

where the surface $S$ is defined by $z=2 x + y$ for $0\le x\le 2$ and $0\le y\le 1.$

- $- \frac{20}{3}$
- $\frac{14}{3}$
- $- \frac{16}{3}$
- $-16$
- $-4$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(2 x + y\right)=2 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(2 x + y\right)=1\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle 6 x^{3} y,\,4 y z,\,4 x \left(y + z\right)\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 6 x^{3} y,\,4 y z,\,4 x \left(y + z\right)\right\rangle\big|_{z=2 x + y} \\  & =\left\langle 6 x^{3} y,\,4 y \left(2 x + y\right),\,4 x \left(y + \left(2 x + y\right)\right)\right\rangle \\  & =\left\langle \underbrace{6 x^{3} y}_{P},\,\underbrace{4 y \left(2 x + y\right)}_{Q},\,\underbrace{8 x \left(x + y\right)}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 6 x^{3} y,\,4 y z,\,4 x \left(y + z\right)\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(6 x^{3} y\right)\left(2\right)-\left(4 y \left(2 x + y\right)\right)\left(1\right)+\left(8 x \left(x + y\right)\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- 12 x^{3} y + 8 x \left(x + y\right) + 4 y \left(- 2 x - y\right)\right)\,\mathrm{d}A \\  & =\int_{0}^{2}\int_{0}^{1}\left(- 12 x^{3} y + 8 x^{2} - 4 y^{2}\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{2}\left[- 6 x^{3} y^{2} + 8 x^{2} y - \frac{4 y^{3}}{3}\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{0}^{2}\left(\left(- 6 x^{3} + 8 x^{2} - \frac{4}{3}\right) + 0\right)\,\mathrm{d}x \\  & =\left[- \frac{3 x^{4}}{2} + \frac{8 x^{3}}{3} - \frac{4 x}{3}\right]_{x=0}^{x=2} \\  & =- \frac{16}{3} + 0 \\  & =- \frac{16}{3}\end{aligned}
$$

## Original q-161447

Evaluate the surface integral

$$
{∬}_{S}⟨y,\,x+z,\,z+2x⟩\cdot \text{d}S
$$

where the surface $S$ is defined by $z=y-2x$ for $1\le x\le 2$ and $0\le y\le 1.$

- $\frac{7}{2}$
- $\frac{5}{2}$ (correct)
- $\frac{1}{2}$
- $1$
- $0$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}(y-2x)=-2 \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}(y-2x)=1\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =⟨y,\,x+z,\,z+2x⟩{|}_{z=y-2x} \\  & =⟨y,\,x+(y-2x),\,y-2x+2x⟩ \\  & =⟨{{y}_{⏟}}_{P},\,{{y-x}_{⏟}}_{Q},\,{{y}_{⏟}}_{R}⟩\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}{∬}_{S}⟨y,\,x+z,\,z+2x⟩\cdot \text{d}S & ={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A \\  & ={∬}_{D}(-y\cdot (-2)-(y-x)\cdot (1)+y)\,\text{d}A \\  & ={∬}_{D}(2y-y+x+y)\,\text{d}A \\  & ={∬}_{D}(2y+x)\,\text{d}A \\  & ={\int }_{1}^{2}{\int }_{0}^{1}(2y+x)\,\text{d}y\,\text{d}x \\  & ={\int }_{1}^{2}{[{y}^{2}+xy]}_{y=0}^{y=1}\,\text{d}x \\  & ={\int }_{1}^{2}(1+x)\,\text{d}x \\  & ={[x+\frac{{x}^{2}}{2}]}_{1}^{2} \\  & =2+2-1-\frac{1}{2} \\  & =\frac{5}{2}\end{aligned}
$$

### Generated observed-profile replay q-161447

Evaluate the surface integral

$$
\iint_S \left\langle y,\,x + z,\,2 x + z\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the surface $S$ is defined by $z=- 2 x + y$ for $1\le x\le 2$ and $0\le y\le 1.$

- $\frac{1}{2}$
- $\frac{5}{2}$
- $\frac{7}{2}$
- $0$
- $1$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(- 2 x + y\right)=-2 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(- 2 x + y\right)=1\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle y,\,x + z,\,2 x + z\right\rangle\big|_{z=- 2 x + y} \\  & =\left\langle y,\,x + \left(- 2 x + y\right),\,2 x + \left(- 2 x + y\right)\right\rangle \\  & =\left\langle \underbrace{y}_{P},\,\underbrace{- x + y}_{Q},\,\underbrace{y}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle y,\,x + z,\,2 x + z\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(y\right)\left(-2\right)-\left(- x + y\right)\left(1\right)+\left(y\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(x - y + y + 2 y\right)\,\mathrm{d}A \\  & =\iint_D\left(x + 2 y\right)\,\mathrm{d}A \\  & =\int_{1}^{2}\int_{0}^{1}\left(x + 2 y\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{1}^{2}\left[x y + y^{2}\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{1}^{2}\left(\left(x + 1\right) + 0\right)\,\mathrm{d}x \\  & =\left[\frac{x^{2}}{2} + x\right]_{x=1}^{x=2} \\  & =- \frac{3}{2} + 4 \\  & =\frac{5}{2}\end{aligned}
$$

### Generated variant of observed bank q-161447 (uniform scaling; error intent unresolved)

Evaluate the surface integral

$$
\iint_S \left\langle 2 y,\,2 x + 2 z,\,4 x + 2 z\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the surface $S$ is defined by $z=- 2 x + y$ for $1\le x\le 2$ and $0\le y\le 1.$

- $1$
- $5$
- $7$
- $0$
- $2$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(- 2 x + y\right)=-2 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(- 2 x + y\right)=1\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 2 y,\,2 x + 2 z,\,4 x + 2 z\right\rangle\big|_{z=- 2 x + y} \\  & =\left\langle 2 y,\,2 x + 2 \left(- 2 x + y\right),\,4 x + 2 \left(- 2 x + y\right)\right\rangle \\  & =\left\langle \underbrace{2 y}_{P},\,\underbrace{- 2 x + 2 y}_{Q},\,\underbrace{2 y}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 2 y,\,2 x + 2 z,\,4 x + 2 z\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2 y\right)\left(-2\right)-\left(- 2 x + 2 y\right)\left(1\right)+\left(2 y\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(2 x - 2 y + 2 y + 4 y\right)\,\mathrm{d}A \\  & =\iint_D\left(2 x + 4 y\right)\,\mathrm{d}A \\  & =\int_{1}^{2}\int_{0}^{1}\left(2 x + 4 y\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{1}^{2}\left[2 x y + 2 y^{2}\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{1}^{2}\left(\left(2 x + 2\right) + 0\right)\,\mathrm{d}x \\  & =\left[x^{2} + 2 x\right]_{x=1}^{x=2} \\  & =-3 + 8 \\  & =5\end{aligned}
$$

## Original q-161476

Evaluate the surface integral

$$
{∬}_{S}⟨\frac{1}{z},\,\frac{xy}{z},\,z⟩\cdot \text{d}S
$$

where the surface $S$ is defined by $z={e}^{x-y}$ for $0\le x\le 1$ and $0\le y\le x.$

- ${e}^{2}-\frac{17}{8}$
- ${e}^{2}+e-\frac{19}{8}$
- $e-\frac{19}{8}$ (correct)
- $e-\frac{15}{8}$
- ${e}^{2}-e-\frac{13}{8}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{∂g}{∂x} & =\frac{∂}{∂x}{e}^{x-y}={e}^{x-y} \\ \frac{∂g}{∂y} & =\frac{∂}{∂y}{e}^{x-y}=-{e}^{x-y}\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =⟨\frac{1}{z},\,\frac{xy}{z},\,z⟩{|}_{z={e}^{x-y}} \\  & =⟨{e}^{-(x-y)},\,xy{e}^{-(x-y)},\,{e}^{x-y}⟩ \\  & =⟨{{{e}^{y-x}}_{⏟}}_{P},\,{{xy{e}^{y-x}}_{⏟}}_{Q},\,{{{e}^{x-y}}_{⏟}}_{R}⟩\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}{∬}_{S}⟨\frac{1}{z},\,\frac{xy}{z},\,z⟩\cdot \text{d}S & ={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\text{d}A \\  & ={∬}_{D}(-{e}^{y-x}\cdot {e}^{x-y}-(xy{e}^{y-x})\cdot (-{e}^{x-y})+{e}^{x-y})\,\text{d}A \\  & ={∬}_{D}(-1+xy+{e}^{x-y})\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{0}^{x}(-1+xy+{e}^{x-y})\,\text{d}y\,\text{d}x \\  & ={\int }_{0}^{1}{[-y+\frac{x{y}^{2}}{2}-{e}^{x-y}]}_{y=0}^{y=x}\,\text{d}x \\  & ={\int }_{0}^{1}(-x+\frac{{x}^{3}}{2}-1+{e}^{x})\,\text{d}x \\  & ={[-\frac{{x}^{2}}{2}+\frac{{x}^{4}}{8}-x+{e}^{x}]}_{0}^{1} \\  & =(-\frac{1}{2}+\frac{1}{8}-1+e)-1 \\  & =-\frac{19}{8}+e\end{aligned}
$$

### Generated observed-profile replay q-161476

Evaluate the surface integral

$$
\iint_S \left\langle \frac{1}{z},\,\frac{x y}{z},\,z\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the surface $S$ is defined by $z=e^{x - y}$ for $0\le x\le 1$ and $0\le y\le x.$

- $- \frac{19}{8} + e$
- $- \frac{19}{8} + e + e^{2}$
- $- \frac{17}{8} + e^{2}$
- $- e - \frac{13}{8} + e^{2}$
- $- \frac{15}{8} + e$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(e^{x - y}\right)=e^{x - y} \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(e^{x - y}\right)=- e^{x - y}\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle \frac{1}{z},\,\frac{x y}{z},\,z\right\rangle\big|_{z=e^{x - y}} \\  & =\left\langle \frac{1}{\left(e^{x - y}\right)},\,\frac{x y}{\left(e^{x - y}\right)},\,\left(e^{x - y}\right)\right\rangle \\  & =\left\langle \underbrace{e^{- x + y}}_{P},\,\underbrace{x y e^{- x + y}}_{Q},\,\underbrace{e^{x - y}}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle \frac{1}{z},\,\frac{x y}{z},\,z\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(e^{- x + y}\right)\left(e^{x - y}\right)-\left(x y e^{- x + y}\right)\left(- e^{x - y}\right)+\left(e^{x - y}\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(x y + e^{x - y} - 1\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{0}^{x}\left(x y + e^{x - y} - 1\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[\frac{x y^{2}}{2} - y - e^{x - y}\right]_{y=0}^{y=x}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(\frac{x^{3}}{2} - x - 1\right) + e^{x}\right)\,\mathrm{d}x \\  & =\left[\frac{x^{4}}{8} - \frac{x^{2}}{2} - x + e^{x}\right]_{x=0}^{x=1} \\  & =-1 - \left(\frac{11}{8} - e\right) \\  & =- \frac{19}{8} + e\end{aligned}
$$

### Generated variant of observed bank q-161476 (uniform scaling; error intent unresolved)

Evaluate the surface integral

$$
\iint_S \left\langle \frac{2}{z},\,\frac{2 x y}{z},\,2 z\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the surface $S$ is defined by $z=e^{x - y}$ for $0\le x\le 1$ and $0\le y\le x.$

- $- \frac{19}{4} + 2 e$
- $- \frac{19}{4} + 2 e + 2 e^{2}$
- $- \frac{17}{4} + 2 e^{2}$
- $- 2 e - \frac{13}{4} + 2 e^{2}$
- $- \frac{15}{4} + 2 e$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(e^{x - y}\right)=e^{x - y} \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(e^{x - y}\right)=- e^{x - y}\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle \frac{2}{z},\,\frac{2 x y}{z},\,2 z\right\rangle\big|_{z=e^{x - y}} \\  & =\left\langle \frac{2}{\left(e^{x - y}\right)},\,\frac{2 x y}{\left(e^{x - y}\right)},\,2 \left(e^{x - y}\right)\right\rangle \\  & =\left\langle \underbrace{2 e^{- x + y}}_{P},\,\underbrace{2 x y e^{- x + y}}_{Q},\,\underbrace{2 e^{x - y}}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle \frac{2}{z},\,\frac{2 x y}{z},\,2 z\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2 e^{- x + y}\right)\left(e^{x - y}\right)-\left(2 x y e^{- x + y}\right)\left(- e^{x - y}\right)+\left(2 e^{x - y}\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(2 x y + 2 e^{x - y} - 2\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{0}^{x}\left(2 x y + 2 e^{x - y} - 2\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[x y^{2} - 2 y - 2 e^{x - y}\right]_{y=0}^{y=x}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(x^{3} - 2 x - 2\right) + 2 e^{x}\right)\,\mathrm{d}x \\  & =\left[\frac{x^{4}}{4} - x^{2} - 2 x + 2 e^{x}\right]_{x=0}^{x=1} \\  & =-2 - \left(\frac{11}{4} - 2 e\right) \\  & =- \frac{19}{4} + 2 e\end{aligned}
$$

### Generated authored default easy easy_affine seed 27

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle 2 y,\,- x,\,z - 1\right\rangle,
$$

where the upward-oriented surface $S$ is defined by $z=x + y - 1$ for $0\le x\le 2$ and $0\le y\le 1.$

- $-5$
- $1$
- $3$
- $-1$
- $0$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(x + y - 1\right)=1 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(x + y - 1\right)=1\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 2 y,\,- x,\,z - 1\right\rangle\big|_{z=x + y - 1} \\  & =\left\langle 2 y,\,- x,\,\left(x + y - 1\right) - 1\right\rangle \\  & =\left\langle \underbrace{2 y}_{P},\,\underbrace{- x}_{Q},\,\underbrace{x + y - 2}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 2 y,\,- x,\,z - 1\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2 y\right)\left(1\right)-\left(- x\right)\left(1\right)+\left(x + y - 2\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(x + x - 2 y + y - 2\right)\,\mathrm{d}A \\  & =\int_{0}^{2}\int_{0}^{1}\left(2 x - y - 2\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{2}\left[- \frac{y^{2}}{2} + y \left(2 x - 2\right)\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{0}^{2}\left(\left(2 x - \frac{5}{2}\right) + 0\right)\,\mathrm{d}x \\  & =\left[x^{2} - \frac{5 x}{2}\right]_{x=0}^{x=2} \\  & =-1 + 0 \\  & =-1\end{aligned}
$$

### Generated authored default easy easy_affine seed 53

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle 2 y,\,x,\,z - 2\right\rangle,
$$

where the upward-oriented surface $S$ is defined by $z=- x + 2 y + 1$ for $0\le x\le 1$ and $0\le y\le 1.$

- $0$
- $- \frac{1}{2}$
- $\frac{3}{2}$
- $\frac{1}{2}$
- $- \frac{5}{2}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(- x + 2 y + 1\right)=-1 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(- x + 2 y + 1\right)=2\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 2 y,\,x,\,z - 2\right\rangle\big|_{z=- x + 2 y + 1} \\  & =\left\langle 2 y,\,x,\,\left(- x + 2 y + 1\right) - 2\right\rangle \\  & =\left\langle \underbrace{2 y}_{P},\,\underbrace{x}_{Q},\,\underbrace{- x + 2 y - 1}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 2 y,\,x,\,z - 2\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2 y\right)\left(-1\right)-\left(x\right)\left(2\right)+\left(- x + 2 y - 1\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- 2 x - x + 2 y + 2 y - 1\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{0}^{1}\left(- 3 x + 4 y - 1\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[2 y^{2} + y \left(- 3 x - 1\right)\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(1 - 3 x\right) + 0\right)\,\mathrm{d}x \\  & =\left[- \frac{3 x^{2}}{2} + x\right]_{x=0}^{x=1} \\  & =- \frac{1}{2} + 0 \\  & =- \frac{1}{2}\end{aligned}
$$

### Generated authored default moderate q-160888 seed 27

Evaluate the surface integral

$$
\iint_S \left\langle - y - z,\,- 2 y - z,\,- 2 x y\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the upward-oriented surface $S$ is defined by $z=x - y$ for $0\le x\le 1$ and $0\le y\le 2.$

- $2$
- $-6$
- $4$
- $-2$
- $-4$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(x - y\right)=1 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(x - y\right)=-1\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle - y - z,\,- 2 y - z,\,- 2 x y\right\rangle\big|_{z=x - y} \\  & =\left\langle - y - \left(x - y\right),\,- 2 y - \left(x - y\right),\,- 2 x y\right\rangle \\  & =\left\langle \underbrace{- x}_{P},\,\underbrace{- x - y}_{Q},\,\underbrace{- 2 x y}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle - y - z,\,- 2 y - z,\,- 2 x y\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(- x\right)\left(1\right)-\left(- x - y\right)\left(-1\right)+\left(- 2 x y\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- 2 x y - x + x - y\right)\,\mathrm{d}A \\  & =\iint_D\left(y \left(- 2 x - 1\right)\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{0}^{2}\left(y \left(- 2 x - 1\right)\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[y^{2} \left(- x - \frac{1}{2}\right)\right]_{y=0}^{y=2}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(- 4 x - 2\right) + 0\right)\,\mathrm{d}x \\  & =\left[- 2 x^{2} - 2 x\right]_{x=0}^{x=1} \\  & =-4 + 0 \\  & =-4\end{aligned}
$$

### Generated authored default moderate q-160888 seed 53

Evaluate the surface integral

$$
\iint_S \left\langle 2 y + 2 z,\,- 4 y - 2 z,\,x y\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the upward-oriented surface $S$ is defined by $z=x - y$ for $0\le x\le 1$ and $0\le y\le 2.$

- $-7$
- $7$
- $-3$
- $5$
- $-8$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(x - y\right)=1 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(x - y\right)=-1\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 2 y + 2 z,\,- 4 y - 2 z,\,x y\right\rangle\big|_{z=x - y} \\  & =\left\langle 2 y + 2 \left(x - y\right),\,- 4 y - 2 \left(x - y\right),\,x y\right\rangle \\  & =\left\langle \underbrace{2 x}_{P},\,\underbrace{- 2 x - 2 y}_{Q},\,\underbrace{x y}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 2 y + 2 z,\,- 4 y - 2 z,\,x y\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2 x\right)\left(1\right)-\left(- 2 x - 2 y\right)\left(-1\right)+\left(x y\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(x y - 2 x - 2 x - 2 y\right)\,\mathrm{d}A \\  & =\iint_D\left(x y - 4 x - 2 y\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{0}^{2}\left(x y - 4 x - 2 y\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[- 4 x y + y^{2} \left(\frac{x}{2} - 1\right)\right]_{y=0}^{y=2}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(- 6 x - 4\right) + 0\right)\,\mathrm{d}x \\  & =\left[- 3 x^{2} - 4 x\right]_{x=0}^{x=1} \\  & =-7 + 0 \\  & =-7\end{aligned}
$$

### Generated authored default moderate q-161382 seed 27

Evaluate the surface integral

$$
\iint_S \left\langle - 3 x,\,- y,\,3 x y z\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the upward-oriented surface $S$ is defined by $z=2 x + y$ for $0\le x\le 1$ and $0\le y\le 1.$

- $-5$
- $4$
- $5$
- $\frac{7}{2}$
- $-1$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(2 x + y\right)=2 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(2 x + y\right)=1\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle - 3 x,\,- y,\,3 x y z\right\rangle\big|_{z=2 x + y} \\  & =\left\langle - 3 x,\,- y,\,3 x y \left(2 x + y\right)\right\rangle \\  & =\left\langle \underbrace{- 3 x}_{P},\,\underbrace{- y}_{Q},\,\underbrace{3 x y \left(2 x + y\right)}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle - 3 x,\,- y,\,3 x y z\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(- 3 x\right)\left(2\right)-\left(- y\right)\left(1\right)+\left(3 x y \left(2 x + y\right)\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(3 x y \left(2 x + y\right) + 6 x + y\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{0}^{1}\left(3 x y \left(2 x + y\right) + 6 x + y\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[x y^{3} + 6 x y + y^{2} \left(3 x^{2} + \frac{1}{2}\right)\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(3 x^{2} + 7 x + \frac{1}{2}\right) + 0\right)\,\mathrm{d}x \\  & =\int_{0}^{1}\left(3 x^{2} + 7 x + \frac{1}{2}\right)\,\mathrm{d}x \\  & =\left[x^{3} + \frac{7 x^{2}}{2} + \frac{x}{2}\right]_{x=0}^{x=1} \\  & =0 + 5 \\  & =5\end{aligned}
$$

### Generated authored default moderate q-161382 seed 53

Evaluate the surface integral

$$
\iint_S \left\langle - 2 x,\,2 y,\,x y z\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the upward-oriented surface $S$ is defined by $z=2 x + y$ for $0\le x\le 1$ and $0\le y\le 1.$

- $\frac{3}{2}$
- $- \frac{3}{2}$
- $- \frac{5}{2}$
- $\frac{7}{2}$
- $1$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(2 x + y\right)=2 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(2 x + y\right)=1\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle - 2 x,\,2 y,\,x y z\right\rangle\big|_{z=2 x + y} \\  & =\left\langle - 2 x,\,2 y,\,x y \left(2 x + y\right)\right\rangle \\  & =\left\langle \underbrace{- 2 x}_{P},\,\underbrace{2 y}_{Q},\,\underbrace{x y \left(2 x + y\right)}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle - 2 x,\,2 y,\,x y z\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(- 2 x\right)\left(2\right)-\left(2 y\right)\left(1\right)+\left(x y \left(2 x + y\right)\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(x y \left(2 x + y\right) + 4 x - 2 y\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{0}^{1}\left(x y \left(2 x + y\right) + 4 x - 2 y\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[\frac{x y^{3}}{3} + 4 x y + y^{2} \left(x^{2} - 1\right)\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(x^{2} + \frac{13 x}{3} - 1\right) + 0\right)\,\mathrm{d}x \\  & =\int_{0}^{1}\left(x^{2} + \frac{13 x}{3} - 1\right)\,\mathrm{d}x \\  & =\left[\frac{x^{3}}{3} + \frac{13 x^{2}}{6} - x\right]_{x=0}^{x=1} \\  & =0 + \frac{3}{2} \\  & =\frac{3}{2}\end{aligned}
$$

### Generated authored default moderate q-161435 seed 27

Evaluate the surface integral

$$
\iint_S \left\langle 3 x y,\,x + y,\,3 e^{z}\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the upward-oriented surface $S$ is defined by $z=x + y$ for $0\le x\le 1$ and $0\le y\le x.$

- $- \frac{3 e^{2}}{2} - \frac{5}{8} + 3 e$
- $- 3 e + \frac{13}{8} + \frac{3 e^{2}}{2}$
- $- 3 e + \frac{5}{8} + \frac{3 e^{2}}{2}$
- $- \frac{7}{8}$
- $- 3 e + \frac{11}{8} + \frac{3 e^{2}}{2}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(x + y\right)=1 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(x + y\right)=1\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 3 x y,\,x + y,\,3 e^{z}\right\rangle\big|_{z=x + y} \\  & =\left\langle 3 x y,\,x + y,\,3 e^{\left(x + y\right)}\right\rangle \\  & =\left\langle \underbrace{3 x y}_{P},\,\underbrace{x + y}_{Q},\,\underbrace{3 e^{x + y}}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 3 x y,\,x + y,\,3 e^{z}\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(3 x y\right)\left(1\right)-\left(x + y\right)\left(1\right)+\left(3 e^{x + y}\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- 3 x y - x - y + 3 e^{x + y}\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{0}^{x}\left(- 3 x y - x - y + 3 e^{x + y}\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[- x y + y^{2} \left(- \frac{3 x}{2} - \frac{1}{2}\right) + 3 e^{x + y}\right]_{y=0}^{y=x}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(x^{2} \left(- \frac{3 x}{2} - \frac{1}{2}\right) - x^{2} + 3 e^{2 x}\right) - 3 e^{x}\right)\,\mathrm{d}x \\  & =\int_{0}^{1}\left(- \frac{3 x^{3}}{2} - \frac{3 x^{2}}{2} + 3 e^{2 x} - 3 e^{x}\right)\,\mathrm{d}x \\  & =\left[- \frac{3 x^{4}}{8} - \frac{x^{3}}{2} + \frac{3 e^{2 x}}{2} - 3 e^{x}\right]_{x=0}^{x=1} \\  & =\frac{3}{2} - \left(- \frac{3 e^{2}}{2} + \frac{7}{8} + 3 e\right) \\  & =- 3 e + \frac{5}{8} + \frac{3 e^{2}}{2}\end{aligned}
$$

### Generated authored default moderate q-161435 seed 53

Evaluate the surface integral

$$
\iint_S \left\langle 2 x y,\,- 2 x - 2 y,\,e^{z}\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the upward-oriented surface $S$ is defined by $z=x + y$ for $0\le x\le 1$ and $0\le y\le x.$

- $- e + \frac{5}{4} + \frac{e^{2}}{2}$
- $- \frac{e^{2}}{2} - \frac{5}{4} + e$
- $- e + \frac{7}{4} + \frac{e^{2}}{2}$
- $- e - \frac{3}{4} + \frac{e^{2}}{2}$
- $\frac{3}{4}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(x + y\right)=1 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(x + y\right)=1\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 2 x y,\,- 2 x - 2 y,\,e^{z}\right\rangle\big|_{z=x + y} \\  & =\left\langle 2 x y,\,- 2 x - 2 y,\,e^{\left(x + y\right)}\right\rangle \\  & =\left\langle \underbrace{2 x y}_{P},\,\underbrace{- 2 x - 2 y}_{Q},\,\underbrace{e^{x + y}}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 2 x y,\,- 2 x - 2 y,\,e^{z}\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2 x y\right)\left(1\right)-\left(- 2 x - 2 y\right)\left(1\right)+\left(e^{x + y}\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- 2 x y + 2 x + 2 y + e^{x + y}\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{0}^{x}\left(- 2 x y + 2 x + 2 y + e^{x + y}\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[2 x y + y^{2} \left(1 - x\right) + e^{x + y}\right]_{y=0}^{y=x}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(x^{2} \left(1 - x\right) + 2 x^{2} + e^{2 x}\right) - e^{x}\right)\,\mathrm{d}x \\  & =\int_{0}^{1}\left(- x^{3} + 3 x^{2} + e^{2 x} - e^{x}\right)\,\mathrm{d}x \\  & =\left[- \frac{x^{4}}{4} + x^{3} + \frac{e^{2 x}}{2} - e^{x}\right]_{x=0}^{x=1} \\  & =\frac{1}{2} + \left(- e + \frac{3}{4} + \frac{e^{2}}{2}\right) \\  & =- e + \frac{5}{4} + \frac{e^{2}}{2}\end{aligned}
$$

### Generated authored default moderate q-161481 seed 27

Evaluate the surface integral

$$
\iint_S \left\langle 3,\,0,\,3 y\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the upward-oriented surface $S$ is defined by $z=\cos{\left(x + y \right)}$ for $- \pi\le x\le 0$ and $0\le y\le - x.$

- $\frac{\pi \left(6 - \pi^{2}\right)}{2}$
- $\frac{3 \pi^{2}}{2}$
- $\frac{\pi \left(-6 + \pi^{2}\right)}{2}$
- $0$
- $\frac{\pi^{3}}{2}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(\cos{\left(x + y \right)}\right)=- \sin{\left(x + y \right)} \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(\cos{\left(x + y \right)}\right)=- \sin{\left(x + y \right)}\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 3,\,0,\,3 y\right\rangle\big|_{z=\cos{\left(x + y \right)}} \\  & =\left\langle \underbrace{3}_{P},\,\underbrace{0}_{Q},\,\underbrace{3 y}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 3,\,0,\,3 y\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(3\right)\left(- \sin{\left(x + y \right)}\right)-\left(0\right)\left(- \sin{\left(x + y \right)}\right)+\left(3 y\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(3 y + 3 \sin{\left(x + y \right)} + 0\right)\,\mathrm{d}A \\  & =\int_{- \pi}^{0}\int_{0}^{- x}\left(3 y + 3 \sin{\left(x + y \right)}\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{- \pi}^{0}\left[\frac{3 y^{2}}{2} - 3 \cos{\left(x + y \right)}\right]_{y=0}^{y=- x}\,\mathrm{d}x \\  & =\int_{- \pi}^{0}\left(\left(\frac{3 x^{2}}{2} - 3\right) + 3 \cos{\left(x \right)}\right)\,\mathrm{d}x \\  & =\int_{- \pi}^{0}\left(\frac{3 x^{2}}{2} + 3 \cos{\left(x \right)} - 3\right)\,\mathrm{d}x \\  & =\left[\frac{x^{3}}{2} - 3 x + 3 \sin{\left(x \right)}\right]_{x=- \pi}^{x=0} \\  & =0 - \left(- \frac{\pi^{3}}{2} + 3 \pi\right) \\  & =\frac{\pi \left(-6 + \pi^{2}\right)}{2}\end{aligned}
$$

### Generated authored default moderate q-161481 seed 53

Evaluate the surface integral

$$
\iint_S \left\langle 2,\,0,\,y\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the upward-oriented surface $S$ is defined by $z=\cos{\left(x + y \right)}$ for $- \pi\le x\le 0$ and $0\le y\le - x.$

- $\frac{\pi \left(-12 + \pi^{2}\right)}{6}$
- $\frac{\pi \left(12 - \pi^{2}\right)}{6}$
- $\frac{\pi^{3}}{6}$
- $\pi^{2}$
- $0$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(\cos{\left(x + y \right)}\right)=- \sin{\left(x + y \right)} \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(\cos{\left(x + y \right)}\right)=- \sin{\left(x + y \right)}\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 2,\,0,\,y\right\rangle\big|_{z=\cos{\left(x + y \right)}} \\  & =\left\langle \underbrace{2}_{P},\,\underbrace{0}_{Q},\,\underbrace{y}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 2,\,0,\,y\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2\right)\left(- \sin{\left(x + y \right)}\right)-\left(0\right)\left(- \sin{\left(x + y \right)}\right)+\left(y\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(y + 2 \sin{\left(x + y \right)} + 0\right)\,\mathrm{d}A \\  & =\int_{- \pi}^{0}\int_{0}^{- x}\left(y + 2 \sin{\left(x + y \right)}\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{- \pi}^{0}\left[\frac{y^{2}}{2} - 2 \cos{\left(x + y \right)}\right]_{y=0}^{y=- x}\,\mathrm{d}x \\  & =\int_{- \pi}^{0}\left(\left(\frac{x^{2}}{2} - 2\right) + 2 \cos{\left(x \right)}\right)\,\mathrm{d}x \\  & =\int_{- \pi}^{0}\left(\frac{x^{2}}{2} + 2 \cos{\left(x \right)} - 2\right)\,\mathrm{d}x \\  & =\left[\frac{x^{3}}{6} - 2 x + 2 \sin{\left(x \right)}\right]_{x=- \pi}^{x=0} \\  & =\left(- 2 \pi + \frac{\pi^{3}}{6}\right) + 0 \\  & =\frac{\pi \left(-12 + \pi^{2}\right)}{6}\end{aligned}
$$

### Generated authored default moderate q-161447 seed 27

Evaluate the surface integral

$$
\iint_S \left\langle 3 y,\,x + z,\,6 x + 3 z\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the upward-oriented surface $S$ is defined by $z=- 2 x + y$ for $1\le x\le 2$ and $0\le y\le 1.$

- $- \frac{11}{2}$
- $\frac{7}{2}$
- $\frac{11}{2}$
- $4$
- $- \frac{1}{2}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(- 2 x + y\right)=-2 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(- 2 x + y\right)=1\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 3 y,\,x + z,\,6 x + 3 z\right\rangle\big|_{z=- 2 x + y} \\  & =\left\langle 3 y,\,x + \left(- 2 x + y\right),\,6 x + 3 \left(- 2 x + y\right)\right\rangle \\  & =\left\langle \underbrace{3 y}_{P},\,\underbrace{- x + y}_{Q},\,\underbrace{3 y}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 3 y,\,x + z,\,6 x + 3 z\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(3 y\right)\left(-2\right)-\left(- x + y\right)\left(1\right)+\left(3 y\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(x - y + 3 y + 6 y\right)\,\mathrm{d}A \\  & =\iint_D\left(x + 8 y\right)\,\mathrm{d}A \\  & =\int_{1}^{2}\int_{0}^{1}\left(x + 8 y\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{1}^{2}\left[x y + 4 y^{2}\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{1}^{2}\left(\left(x + 4\right) + 0\right)\,\mathrm{d}x \\  & =\left[\frac{x^{2}}{2} + 4 x\right]_{x=1}^{x=2} \\  & =- \frac{9}{2} + 10 \\  & =\frac{11}{2}\end{aligned}
$$

### Generated authored default moderate q-161447 seed 53

Evaluate the surface integral

$$
\iint_S \left\langle 2 y,\,- 2 x - 2 z,\,2 x + z\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the upward-oriented surface $S$ is defined by $z=- 2 x + y$ for $1\le x\le 2$ and $0\le y\le 1.$

- $\frac{1}{2}$
- $- \frac{1}{2}$
- $- \frac{7}{2}$
- $\frac{9}{2}$
- $0$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(- 2 x + y\right)=-2 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(- 2 x + y\right)=1\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 2 y,\,- 2 x - 2 z,\,2 x + z\right\rangle\big|_{z=- 2 x + y} \\  & =\left\langle 2 y,\,- 2 x - 2 \left(- 2 x + y\right),\,2 x + \left(- 2 x + y\right)\right\rangle \\  & =\left\langle \underbrace{2 y}_{P},\,\underbrace{2 x - 2 y}_{Q},\,\underbrace{y}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 2 y,\,- 2 x - 2 z,\,2 x + z\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2 y\right)\left(-2\right)-\left(2 x - 2 y\right)\left(1\right)+\left(y\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- 2 x + y + 2 y + 4 y\right)\,\mathrm{d}A \\  & =\iint_D\left(- 2 x + 7 y\right)\,\mathrm{d}A \\  & =\int_{1}^{2}\int_{0}^{1}\left(- 2 x + 7 y\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{1}^{2}\left[- 2 x y + \frac{7 y^{2}}{2}\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{1}^{2}\left(\left(\frac{7}{2} - 2 x\right) + 0\right)\,\mathrm{d}x \\  & =\left[- x^{2} + \frac{7 x}{2}\right]_{x=1}^{x=2} \\  & =- \frac{5}{2} + 3 \\  & =\frac{1}{2}\end{aligned}
$$

### Generated authored default moderate q-161476 seed 27

Evaluate the surface integral

$$
\iint_S \left\langle \frac{3}{z},\,\frac{x y}{z},\,3 z\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the upward-oriented surface $S$ is defined by $z=e^{x - y}$ for $0\le x\le 1$ and $0\le y\le x.$

- $\frac{59}{8} - 3 e$
- $- \frac{61}{8} + 3 e$
- $- \frac{59}{8} + 3 e$
- $- \frac{11}{8}$
- $- \frac{35}{8} + 3 e$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(e^{x - y}\right)=e^{x - y} \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(e^{x - y}\right)=- e^{x - y}\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle \frac{3}{z},\,\frac{x y}{z},\,3 z\right\rangle\big|_{z=e^{x - y}} \\  & =\left\langle \frac{3}{\left(e^{x - y}\right)},\,\frac{x y}{\left(e^{x - y}\right)},\,3 \left(e^{x - y}\right)\right\rangle \\  & =\left\langle \underbrace{3 e^{- x + y}}_{P},\,\underbrace{x y e^{- x + y}}_{Q},\,\underbrace{3 e^{x - y}}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle \frac{3}{z},\,\frac{x y}{z},\,3 z\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(3 e^{- x + y}\right)\left(e^{x - y}\right)-\left(x y e^{- x + y}\right)\left(- e^{x - y}\right)+\left(3 e^{x - y}\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(x y + 3 e^{x - y} - 3\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{0}^{x}\left(x y + 3 e^{x - y} - 3\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[\frac{x y^{2}}{2} - 3 y - 3 e^{x - y}\right]_{y=0}^{y=x}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(\frac{x^{3}}{2} - 3 x - 3\right) + 3 e^{x}\right)\,\mathrm{d}x \\  & =\left[\frac{x^{4}}{8} - \frac{3 x^{2}}{2} - 3 x + 3 e^{x}\right]_{x=0}^{x=1} \\  & =-3 - \left(\frac{35}{8} - 3 e\right) \\  & =- \frac{59}{8} + 3 e\end{aligned}
$$

### Generated authored default moderate q-161476 seed 53

Evaluate the surface integral

$$
\iint_S \left\langle \frac{2}{z},\,- \frac{2 x y}{z},\,z\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

where the upward-oriented surface $S$ is defined by $z=e^{x - y}$ for $0\le x\le 1$ and $0\le y\le x.$

- $- \frac{13}{4} + e$
- $\frac{13}{4} - e$
- $- \frac{5}{4} + e$
- $- \frac{11}{4} + e$
- $- \frac{5}{4}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(e^{x - y}\right)=e^{x - y} \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(e^{x - y}\right)=- e^{x - y}\end{aligned}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle \frac{2}{z},\,- \frac{2 x y}{z},\,z\right\rangle\big|_{z=e^{x - y}} \\  & =\left\langle \frac{2}{\left(e^{x - y}\right)},\,- \frac{2 x y}{\left(e^{x - y}\right)},\,\left(e^{x - y}\right)\right\rangle \\  & =\left\langle \underbrace{2 e^{- x + y}}_{P},\,\underbrace{- 2 x y e^{- x + y}}_{Q},\,\underbrace{e^{x - y}}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle \frac{2}{z},\,- \frac{2 x y}{z},\,z\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2 e^{- x + y}\right)\left(e^{x - y}\right)-\left(- 2 x y e^{- x + y}\right)\left(- e^{x - y}\right)+\left(e^{x - y}\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- 2 x y + e^{x - y} - 2\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{0}^{x}\left(- 2 x y + e^{x - y} - 2\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[- x y^{2} - 2 y - e^{x - y}\right]_{y=0}^{y=x}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(- x^{3} - 2 x - 1\right) + e^{x}\right)\,\mathrm{d}x \\  & =\left[- \frac{x^{4}}{4} - x^{2} - x + e^{x}\right]_{x=0}^{x=1} \\  & =-1 - \left(\frac{9}{4} - e\right) \\  & =- \frac{13}{4} + e\end{aligned}
$$

### Generated authored default hard q-161553 seed 27

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle 3 e^{x},\,e^{y},\,3 z + 3\right\rangle,
$$

where the upward-oriented surface $S$ is defined by $z=- x - y$ for $0\le x\le 1$ and $0\le y\le 1.$

- $4 - 4 e$
- $0$
- $-4 + 4 e$
- $-3 + 3 e$
- $-1 + e$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(- x - y\right)=-1 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(- x - y\right)=-1\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle 3 e^{x},\,e^{y},\,3 z + 3\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 3 e^{x},\,e^{y},\,3 z + 3\right\rangle\big|_{z=- x - y} \\  & =\left\langle \underbrace{3 e^{x}}_{P},\,\underbrace{e^{y}}_{Q},\,\underbrace{- 3 x - 3 y + 3}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 3 e^{x},\,e^{y},\,3 z + 3\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(3 e^{x}\right)\left(-1\right)-\left(e^{y}\right)\left(-1\right)+\left(- 3 x - 3 y + 3\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- 3 x - 3 y + 3 e^{x} + e^{y} + 3\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{0}^{1}\left(- 3 x - 3 y + 3 e^{x} + e^{y} + 3\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[- \frac{3 y^{2}}{2} + y \left(- 3 x + 3 e^{x} + 3\right) + e^{y}\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(- 3 x + 3 e^{x} + \frac{3}{2} + e\right) - 1\right)\,\mathrm{d}x \\  & =\int_{0}^{1}\left(- 3 x + 3 e^{x} + \frac{1}{2} + e\right)\,\mathrm{d}x \\  & =\left[- \frac{3 x^{2}}{2} + x \left(\frac{1}{2} + e\right) + 3 e^{x}\right]_{x=0}^{x=1} \\  & =-3 - \left(1 - 4 e\right) \\  & =-4 + 4 e\end{aligned}
$$

### Generated authored default hard q-161553 seed 53

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle 2 e^{x},\,3 e^{y},\,z + 1\right\rangle,
$$

where the upward-oriented surface $S$ is defined by $z=- x - y$ for $0\le x\le 1$ and $0\le y\le 1.$

- $-5 + 5 e$
- $5 - 5 e$
- $0$
- $-3 + 3 e$
- $-2 + 2 e$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(- x - y\right)=-1 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(- x - y\right)=-1\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle 2 e^{x},\,3 e^{y},\,z + 1\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 2 e^{x},\,3 e^{y},\,z + 1\right\rangle\big|_{z=- x - y} \\  & =\left\langle \underbrace{2 e^{x}}_{P},\,\underbrace{3 e^{y}}_{Q},\,\underbrace{- x - y + 1}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 2 e^{x},\,3 e^{y},\,z + 1\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2 e^{x}\right)\left(-1\right)-\left(3 e^{y}\right)\left(-1\right)+\left(- x - y + 1\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- x - y + 2 e^{x} + 3 e^{y} + 1\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{0}^{1}\left(- x - y + 2 e^{x} + 3 e^{y} + 1\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[- \frac{y^{2}}{2} + y \left(- x + 2 e^{x} + 1\right) + 3 e^{y}\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(- x + 2 e^{x} + \frac{1}{2} + 3 e\right) - 3\right)\,\mathrm{d}x \\  & =\int_{0}^{1}\left(- x + 2 e^{x} - \frac{5}{2} + 3 e\right)\,\mathrm{d}x \\  & =\left[- \frac{x^{2}}{2} + x \left(- \frac{5}{2} + 3 e\right) + 2 e^{x}\right]_{x=0}^{x=1} \\  & =-2 - \left(3 - 5 e\right) \\  & =-5 + 5 e\end{aligned}
$$

### Generated authored default hard q-161536 seed 27

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle 3 y,\,x + z,\,0\right\rangle,
$$

where the upward-oriented surface $S$ is defined by $z=e^{x}$ for $-1\le x\le 1$ and $0\le y\le 1.$

- $- \frac{3}{2 e} + \frac{3 e}{2}$
- $3$
- $- \frac{3 e}{2} + \frac{3}{2 e}$
- $e - e^{-1}$
- $0$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(e^{x}\right)=e^{x} \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(e^{x}\right)=0\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle 3 y,\,x + z,\,0\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 3 y,\,x + z,\,0\right\rangle\big|_{z=e^{x}} \\  & =\left\langle \underbrace{3 y}_{P},\,\underbrace{x + e^{x}}_{Q},\,\underbrace{0}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 3 y,\,x + z,\,0\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(3 y\right)\left(e^{x}\right)-\left(x + e^{x}\right)\left(0\right)+\left(0\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- 3 y e^{x} + 0 + 0\right)\,\mathrm{d}A \\  & =\int_{-1}^{1}\int_{0}^{1}\left(- 3 y e^{x}\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{-1}^{1}\left[- \frac{3 y^{2} e^{x}}{2}\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{-1}^{1}\left(- \frac{3 e^{x}}{2} + 0\right)\,\mathrm{d}x \\  & =\left[- \frac{3 e^{x}}{2}\right]_{x=-1}^{x=1} \\  & =- \frac{3 e}{2} + \frac{3}{2 e}\end{aligned}
$$

### Generated authored default hard q-161536 seed 53

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle 2 y,\,- 2 x - 2 z,\,0\right\rangle,
$$

where the upward-oriented surface $S$ is defined by $z=e^{x}$ for $-1\le x\le 1$ and $0\le y\le 1.$

- $- e + e^{-1}$
- $e - e^{-1}$
- $0$
- $2$
- $- 2 e + \frac{2}{e}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(e^{x}\right)=e^{x} \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(e^{x}\right)=0\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle 2 y,\,- 2 x - 2 z,\,0\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 2 y,\,- 2 x - 2 z,\,0\right\rangle\big|_{z=e^{x}} \\  & =\left\langle \underbrace{2 y}_{P},\,\underbrace{- 2 x - 2 e^{x}}_{Q},\,\underbrace{0}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 2 y,\,- 2 x - 2 z,\,0\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2 y\right)\left(e^{x}\right)-\left(- 2 x - 2 e^{x}\right)\left(0\right)+\left(0\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- 2 y e^{x} + 0 + 0\right)\,\mathrm{d}A \\  & =\int_{-1}^{1}\int_{0}^{1}\left(- 2 y e^{x}\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{-1}^{1}\left[- y^{2} e^{x}\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{-1}^{1}\left(- e^{x} + 0\right)\,\mathrm{d}x \\  & =\left[- e^{x}\right]_{x=-1}^{x=1} \\  & =- e + e^{-1}\end{aligned}
$$

### Generated authored default hard q-161539 seed 27

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle 3 \cos^{2}{\left(x y \right)},\,\cos^{2}{\left(x y \right)},\,3\right\rangle,
$$

where the upward-oriented surface $S$ is defined by $z=\tan{\left(x y \right)}$ for $0\le x\le 1$ and $- x\le y\le 0.$

- $- \frac{5}{3}$
- $\frac{7}{3}$
- $\frac{5}{3}$
- $\frac{1}{6}$
- $\frac{2}{3}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(\tan{\left(x y \right)}\right)=y \left(\tan^{2}{\left(x y \right)} + 1\right) \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(\tan{\left(x y \right)}\right)=x \left(\tan^{2}{\left(x y \right)} + 1\right)\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle 3 \cos^{2}{\left(x y \right)},\,\cos^{2}{\left(x y \right)},\,3\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 3 \cos^{2}{\left(x y \right)},\,\cos^{2}{\left(x y \right)},\,3\right\rangle\big|_{z=\tan{\left(x y \right)}} \\  & =\left\langle \underbrace{3 \cos^{2}{\left(x y \right)}}_{P},\,\underbrace{\cos^{2}{\left(x y \right)}}_{Q},\,\underbrace{3}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 3 \cos^{2}{\left(x y \right)},\,\cos^{2}{\left(x y \right)},\,3\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(3 \cos^{2}{\left(x y \right)}\right)\left(y \left(\tan^{2}{\left(x y \right)} + 1\right)\right)-\left(\cos^{2}{\left(x y \right)}\right)\left(x \left(\tan^{2}{\left(x y \right)} + 1\right)\right)+\left(3\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- x - 3 y + 3\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{- x}^{0}\left(- x - 3 y + 3\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[- \frac{3 y^{2}}{2} + y \left(3 - x\right)\right]_{y=- x}^{y=0}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(\frac{3 x^{2}}{2} + x \left(3 - x\right)\right) + 0\right)\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\frac{x \left(x + 6\right)}{2}\right)\,\mathrm{d}x \\  & =\left[\frac{x^{3}}{6} + \frac{3 x^{2}}{2}\right]_{x=0}^{x=1} \\  & =0 + \frac{5}{3} \\  & =\frac{5}{3}\end{aligned}
$$

### Generated authored default hard q-161539 seed 53

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle 2 \cos^{2}{\left(x y \right)},\,- 2 \cos^{2}{\left(x y \right)},\,1\right\rangle,
$$

where the upward-oriented surface $S$ is defined by $z=\tan{\left(x y \right)}$ for $0\le x\le 1$ and $- x\le y\le 0.$

- $\frac{3}{2}$
- $- \frac{3}{2}$
- $\frac{5}{6}$
- $\frac{1}{6}$
- $1$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(\tan{\left(x y \right)}\right)=y \left(\tan^{2}{\left(x y \right)} + 1\right) \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(\tan{\left(x y \right)}\right)=x \left(\tan^{2}{\left(x y \right)} + 1\right)\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle 2 \cos^{2}{\left(x y \right)},\,- 2 \cos^{2}{\left(x y \right)},\,1\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 2 \cos^{2}{\left(x y \right)},\,- 2 \cos^{2}{\left(x y \right)},\,1\right\rangle\big|_{z=\tan{\left(x y \right)}} \\  & =\left\langle \underbrace{2 \cos^{2}{\left(x y \right)}}_{P},\,\underbrace{- 2 \cos^{2}{\left(x y \right)}}_{Q},\,\underbrace{1}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 2 \cos^{2}{\left(x y \right)},\,- 2 \cos^{2}{\left(x y \right)},\,1\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2 \cos^{2}{\left(x y \right)}\right)\left(y \left(\tan^{2}{\left(x y \right)} + 1\right)\right)-\left(- 2 \cos^{2}{\left(x y \right)}\right)\left(x \left(\tan^{2}{\left(x y \right)} + 1\right)\right)+\left(1\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(2 x - 2 y + 1\right)\,\mathrm{d}A \\  & =\int_{0}^{1}\int_{- x}^{0}\left(2 x - 2 y + 1\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{1}\left[- y^{2} + y \left(2 x + 1\right)\right]_{y=- x}^{y=0}\,\mathrm{d}x \\  & =\int_{0}^{1}\left(\left(x^{2} + x \left(2 x + 1\right)\right) + 0\right)\,\mathrm{d}x \\  & =\int_{0}^{1}\left(x \left(3 x + 1\right)\right)\,\mathrm{d}x \\  & =\left[x^{3} + \frac{x^{2}}{2}\right]_{x=0}^{x=1} \\  & =0 + \frac{3}{2} \\  & =\frac{3}{2}\end{aligned}
$$

### Generated authored default hard q-161541 seed 27

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle 3 \sqrt{\frac{x}{y}},\,\sqrt{\frac{x}{y}},\,3 z^{2} + 3\right\rangle,
$$

where the upward-oriented surface $S$ is defined by $z=2 \sqrt{x y}$ for $3\le x\le 4$ and $1\le y\le 2.$

- $-63 + \frac{7 \log{\left(2 \right)}}{2}$
- $\frac{7 \log{\left(2 \right)}}{2} + 63$
- $63 - \frac{7 \log{\left(2 \right)}}{2}$
- $-3 - \frac{7 \log{\left(2 \right)}}{2}$
- $69 - \frac{7 \log{\left(2 \right)}}{2}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(2 \sqrt{x y}\right)=\frac{\sqrt{x y}}{x} \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(2 \sqrt{x y}\right)=\frac{\sqrt{x y}}{y}\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle 3 \sqrt{\frac{x}{y}},\,\sqrt{\frac{x}{y}},\,3 z^{2} + 3\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 3 \sqrt{\frac{x}{y}},\,\sqrt{\frac{x}{y}},\,3 z^{2} + 3\right\rangle\big|_{z=2 \sqrt{x y}} \\  & =\left\langle \underbrace{3 \sqrt{\frac{x}{y}}}_{P},\,\underbrace{\sqrt{\frac{x}{y}}}_{Q},\,\underbrace{12 x y + 3}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 3 \sqrt{\frac{x}{y}},\,\sqrt{\frac{x}{y}},\,3 z^{2} + 3\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(3 \sqrt{\frac{x}{y}}\right)\left(\frac{\sqrt{x y}}{x}\right)-\left(\sqrt{\frac{x}{y}}\right)\left(\frac{\sqrt{x y}}{y}\right)+\left(12 x y + 3\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(12 x y - \frac{x}{y} - 3 + 3\right)\,\mathrm{d}A \\  & =\iint_D\left(12 x y - \frac{x}{y}\right)\,\mathrm{d}A \\  & =\int_{3}^{4}\int_{1}^{2}\left(12 x y - \frac{x}{y}\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{3}^{4}\left[6 x y^{2} - x \log{\left(y \right)}\right]_{y=1}^{y=2}\,\mathrm{d}x \\  & =\int_{3}^{4}\left(- 6 x + \left(- x \log{\left(2 \right)} + 24 x\right)\right)\,\mathrm{d}x \\  & =\int_{3}^{4}\left(x \left(18 - \log{\left(2 \right)}\right)\right)\,\mathrm{d}x \\  & =\left[x^{2} \left(9 - \frac{\log{\left(2 \right)}}{2}\right)\right]_{x=3}^{x=4} \\  & =63 - \frac{7 \log{\left(2 \right)}}{2}\end{aligned}
$$

### Generated authored default hard q-161541 seed 53

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle 2 \sqrt{\frac{x}{y}},\,- 2 \sqrt{\frac{x}{y}},\,z^{2} + 1\right\rangle,
$$

where the upward-oriented surface $S$ is defined by $z=2 \sqrt{x y}$ for $3\le x\le 4$ and $1\le y\le 2.$

- $\log{\left(128 \right)} + 20$
- $-20 - \log{\left(128 \right)}$
- $\log{\left(128 \right)} + 24$
- $20 - \log{\left(128 \right)}$
- $-2 + \log{\left(128 \right)}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(2 \sqrt{x y}\right)=\frac{\sqrt{x y}}{x} \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(2 \sqrt{x y}\right)=\frac{\sqrt{x y}}{y}\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle 2 \sqrt{\frac{x}{y}},\,- 2 \sqrt{\frac{x}{y}},\,z^{2} + 1\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 2 \sqrt{\frac{x}{y}},\,- 2 \sqrt{\frac{x}{y}},\,z^{2} + 1\right\rangle\big|_{z=2 \sqrt{x y}} \\  & =\left\langle \underbrace{2 \sqrt{\frac{x}{y}}}_{P},\,\underbrace{- 2 \sqrt{\frac{x}{y}}}_{Q},\,\underbrace{4 x y + 1}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 2 \sqrt{\frac{x}{y}},\,- 2 \sqrt{\frac{x}{y}},\,z^{2} + 1\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2 \sqrt{\frac{x}{y}}\right)\left(\frac{\sqrt{x y}}{x}\right)-\left(- 2 \sqrt{\frac{x}{y}}\right)\left(\frac{\sqrt{x y}}{y}\right)+\left(4 x y + 1\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(4 x y + \frac{2 x}{y} - 2 + 1\right)\,\mathrm{d}A \\  & =\iint_D\left(4 x y + \frac{2 x}{y} - 1\right)\,\mathrm{d}A \\  & =\int_{3}^{4}\int_{1}^{2}\left(4 x y + \frac{2 x}{y} - 1\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{3}^{4}\left[2 x y^{2} + 2 x \log{\left(y \right)} - y\right]_{y=1}^{y=2}\,\mathrm{d}x \\  & =\int_{3}^{4}\left(\left(1 - 2 x\right) + \left(2 x \log{\left(2 \right)} + 8 x - 2\right)\right)\,\mathrm{d}x \\  & =\int_{3}^{4}\left(2 x \log{\left(2 \right)} + 6 x - 1\right)\,\mathrm{d}x \\  & =\left[x^{2} \left(\log{\left(2 \right)} + 3\right) - x\right]_{x=3}^{x=4} \\  & =\log{\left(128 \right)} + 20\end{aligned}
$$

### Generated authored default hard q-161542 seed 27

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle 3 x + 3 y,\,- x + y,\,3 z\right\rangle,
$$

where the upward-oriented surface $S$ is defined by $z=x^{2} + y^{2} + 1$ for $-1\le x\le 1$ and $-1\le y\le 1.$

- $- \frac{28}{3}$
- $\frac{44}{3}$
- $\frac{28}{3}$
- $- \frac{32}{3}$
- $\frac{76}{3}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(x^{2} + y^{2} + 1\right)=2 x \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(x^{2} + y^{2} + 1\right)=2 y\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle 3 x + 3 y,\,- x + y,\,3 z\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 3 x + 3 y,\,- x + y,\,3 z\right\rangle\big|_{z=x^{2} + y^{2} + 1} \\  & =\left\langle \underbrace{3 x + 3 y}_{P},\,\underbrace{- x + y}_{Q},\,\underbrace{3 x^{2} + 3 y^{2} + 3}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 3 x + 3 y,\,- x + y,\,3 z\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(3 x + 3 y\right)\left(2 x\right)-\left(- x + y\right)\left(2 y\right)+\left(3 x^{2} + 3 y^{2} + 3\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(3 x^{2} + 6 x \left(- x - y\right) + 3 y^{2} + 2 y \left(x - y\right) + 3\right)\,\mathrm{d}A \\  & =\int_{-1}^{1}\int_{-1}^{1}\left(- 3 x^{2} - 4 x y + y^{2} + 3\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{-1}^{1}\left[- 2 x y^{2} + \frac{y^{3}}{3} + y \left(3 - 3 x^{2}\right)\right]_{y=-1}^{y=1}\,\mathrm{d}x \\  & =\int_{-1}^{1}\left(\left(- 3 x^{2} - 2 x + \frac{10}{3}\right) + \left(- 3 x^{2} + 2 x + \frac{10}{3}\right)\right)\,\mathrm{d}x \\  & =\int_{-1}^{1}\left(\frac{20}{3} - 6 x^{2}\right)\,\mathrm{d}x \\  & =\left[- 2 x^{3} + \frac{20 x}{3}\right]_{x=-1}^{x=1} \\  & =\frac{14}{3} + \frac{14}{3} \\  & =\frac{28}{3}\end{aligned}
$$

### Generated authored default hard q-161542 seed 53

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle 2 x + 2 y,\,2 x - 2 y,\,z\right\rangle,
$$

where the upward-oriented surface $S$ is defined by $z=x^{2} + y^{2} + 1$ for $-1\le x\le 1$ and $-1\le y\le 1.$

- $\frac{20}{3}$
- $- \frac{20}{3}$
- $\frac{52}{3}$
- $-4$
- $0$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(x^{2} + y^{2} + 1\right)=2 x \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(x^{2} + y^{2} + 1\right)=2 y\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle 2 x + 2 y,\,2 x - 2 y,\,z\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 2 x + 2 y,\,2 x - 2 y,\,z\right\rangle\big|_{z=x^{2} + y^{2} + 1} \\  & =\left\langle \underbrace{2 x + 2 y}_{P},\,\underbrace{2 x - 2 y}_{Q},\,\underbrace{x^{2} + y^{2} + 1}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 2 x + 2 y,\,2 x - 2 y,\,z\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(2 x + 2 y\right)\left(2 x\right)-\left(2 x - 2 y\right)\left(2 y\right)+\left(x^{2} + y^{2} + 1\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(x^{2} + 4 x \left(- x - y\right) + y^{2} + 4 y \left(- x + y\right) + 1\right)\,\mathrm{d}A \\  & =\int_{-1}^{1}\int_{-1}^{1}\left(- 3 x^{2} - 8 x y + 5 y^{2} + 1\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{-1}^{1}\left[- 4 x y^{2} + \frac{5 y^{3}}{3} + y \left(1 - 3 x^{2}\right)\right]_{y=-1}^{y=1}\,\mathrm{d}x \\  & =\int_{-1}^{1}\left(\left(- 3 x^{2} - 4 x + \frac{8}{3}\right) + \left(- 3 x^{2} + 4 x + \frac{8}{3}\right)\right)\,\mathrm{d}x \\  & =\int_{-1}^{1}\left(\frac{16}{3} - 6 x^{2}\right)\,\mathrm{d}x \\  & =\left[- 2 x^{3} + \frac{16 x}{3}\right]_{x=-1}^{x=1} \\  & =\frac{10}{3} + \frac{10}{3} \\  & =\frac{20}{3}\end{aligned}
$$

### Generated authored default hard q-161552 seed 27

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle 9 x^{3} y,\,2 y z,\,6 x \left(y + z\right)\right\rangle,
$$

where the upward-oriented surface $S$ is defined by $z=2 x + y$ for $0\le x\le 2$ and $0\le y\le 1.$

- $- \frac{8}{3}$
- $\frac{40}{3}$
- $\frac{8}{3}$
- $- \frac{124}{3}$
- $\frac{224}{3}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(2 x + y\right)=2 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(2 x + y\right)=1\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle 9 x^{3} y,\,2 y z,\,6 x \left(y + z\right)\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 9 x^{3} y,\,2 y z,\,6 x \left(y + z\right)\right\rangle\big|_{z=2 x + y} \\  & =\left\langle 9 x^{3} y,\,2 y \left(2 x + y\right),\,6 x \left(y + \left(2 x + y\right)\right)\right\rangle \\  & =\left\langle \underbrace{9 x^{3} y}_{P},\,\underbrace{2 y \left(2 x + y\right)}_{Q},\,\underbrace{12 x \left(x + y\right)}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 9 x^{3} y,\,2 y z,\,6 x \left(y + z\right)\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(9 x^{3} y\right)\left(2\right)-\left(2 y \left(2 x + y\right)\right)\left(1\right)+\left(12 x \left(x + y\right)\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- 18 x^{3} y + 12 x \left(x + y\right) + 2 y \left(- 2 x - y\right)\right)\,\mathrm{d}A \\  & =\int_{0}^{2}\int_{0}^{1}\left(- 18 x^{3} y + 12 x \left(x + y\right) - 2 y \left(2 x + y\right)\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{2}\left[12 x^{2} y - \frac{2 y^{3}}{3} + y^{2} \left(- 9 x^{3} + 4 x\right)\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{0}^{2}\left(\left(- 9 x^{3} + 12 x^{2} + 4 x - \frac{2}{3}\right) + 0\right)\,\mathrm{d}x \\  & =\left[- \frac{9 x^{4}}{4} + 4 x^{3} + 2 x^{2} - \frac{2 x}{3}\right]_{x=0}^{x=2} \\  & =0 + \frac{8}{3} \\  & =\frac{8}{3}\end{aligned}
$$

### Generated authored default hard q-161552 seed 53

Calculate the flux of the vector field

$$
F(x,y,z)=\left\langle 6 x^{3} y,\,- 4 y z,\,2 x \left(y + z\right)\right\rangle,
$$

where the upward-oriented surface $S$ is defined by $z=2 x + y$ for $0\le x\le 2$ and $0\le y\le 1.$

- $\frac{4}{3}$
- $- \frac{4}{3}$
- $\frac{148}{3}$
- $-20$
- $- \frac{40}{3}$

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of a vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
\iint_S F\cdot\mathrm{d}\mathbf{S}=\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A.
$$

We first compute the partial derivatives of the graph $z=g(x,y):$

$$
\begin{aligned}\frac{\partial g}{\partial x} & =\frac{\partial}{\partial x}\left(2 x + y\right)=2 \\ \frac{\partial g}{\partial y} & =\frac{\partial}{\partial y}\left(2 x + y\right)=1\end{aligned}
$$

In this case, the flux of $F$ through $S$ is given by 

$$
\iint_S \left\langle 6 x^{3} y,\,- 4 y z,\,2 x \left(y + z\right)\right\rangle\cdot\mathrm{d}\mathbf{S}
$$

Next, we substitute the equation $z=g(x,y)$ into $F(x,y,z):$

$$
\begin{aligned}F(x,y,g(x,y)) & =\left\langle 6 x^{3} y,\,- 4 y z,\,2 x \left(y + z\right)\right\rangle\big|_{z=2 x + y} \\  & =\left\langle 6 x^{3} y,\,- 4 y \left(2 x + y\right),\,2 x \left(y + \left(2 x + y\right)\right)\right\rangle \\  & =\left\langle \underbrace{6 x^{3} y}_{P},\,\underbrace{- 4 y \left(2 x + y\right)}_{Q},\,\underbrace{4 x \left(x + y\right)}_{R}\right\rangle\end{aligned}
$$

Therefore, we can evaluate our surface integral as follows:

$$
\begin{aligned}\iint_S \left\langle 6 x^{3} y,\,- 4 y z,\,2 x \left(y + z\right)\right\rangle\cdot\mathrm{d}\mathbf{S} & =\iint_D\left(-P\frac{\partial g}{\partial x}-Q\frac{\partial g}{\partial y}+R\right)\mathrm{d}A \\  & =\iint_D\left(-\left(6 x^{3} y\right)\left(2\right)-\left(- 4 y \left(2 x + y\right)\right)\left(1\right)+\left(4 x \left(x + y\right)\right)\right)\,\mathrm{d}A \\  & =\iint_D\left(- 12 x^{3} y + 4 x \left(x + y\right) + 4 y \left(2 x + y\right)\right)\,\mathrm{d}A \\  & =\int_{0}^{2}\int_{0}^{1}\left(- 12 x^{3} y + 4 x \left(x + y\right) + 4 y \left(2 x + y\right)\right)\,\mathrm{d}y\,\mathrm{d}x \\  & =\int_{0}^{2}\left[4 x^{2} y + \frac{4 y^{3}}{3} + y^{2} \left(- 6 x^{3} + 6 x\right)\right]_{y=0}^{y=1}\,\mathrm{d}x \\  & =\int_{0}^{2}\left(\left(- 6 x^{3} + 4 x^{2} + 6 x + \frac{4}{3}\right) + 0\right)\,\mathrm{d}x \\  & =\left[- \frac{3 x^{4}}{2} + \frac{4 x^{3}}{3} + 3 x^{2} + \frac{4 x}{3}\right]_{x=0}^{x=2} \\  & =0 + \frac{4}{3} \\  & =\frac{4}{3}\end{aligned}
$$