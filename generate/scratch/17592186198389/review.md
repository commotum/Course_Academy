# Review: concrete Cartesian flux setup

All originals are easy. Moderate/hard headings denote authored scope, not recovered source labels. Source replay normalizes notation; q-161471 corrects its final LHS field.

## Original q-160887 / q-160887

Consider the vector field $F(x,y,z)=⟨z-y,\,2y-z,\,xy⟩$ and the surface $S$ defined by $z=x+y$ for $0\le x\le 4$ and $-2\le y\le 3.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{4}{\int }_{-2}^{3}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?


Original complete bank: $uv+v$, $uv-v$, ${u}^{2}+uv+{v}^{2}$, $2{u}^{2}v-uv+{v}^{2}$, $u+v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u+v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 4,\,-2\le v\le 3\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u+v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u+v)⟩ \\  & =⟨0,\,1,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & 1\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,-1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨z-y,\,2y-z,\,xy⟩{|}_{x=u,\,\,y=v,\,\,z=u+v} \\  & =⟨u+v-v,\,2v-(u+v),\,uv⟩ \\  & =⟨u,\,v-u,\,uv⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u,\,v-u,\,uv⟩\cdot ⟨-1,\,-1,\,1⟩ \\  & =u\cdot (-1)+(v-u)\cdot (-1)+uv\cdot 1 \\  & =-u-v+u+uv \\  & =uv-v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨z-y,\,2y-z,\,xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(uv-v)\,\text{d}A \\  & ={\int }_{0}^{4}{\int }_{-2}^{3}uv-v\,\text{d}v\,\text{d}u.\end{aligned}
$$

### Reconstructed at original parameters

Consider the vector field $F(x,y,z)=⟨- y + z,\,2 y - z,\,xy⟩$ and the surface $S$ defined by $z=x + y$ for $0\le x\le 4$ and $-2\le y\le 3.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{4}{\int }_{-2}^{3}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $2 u^{2} v - uv + v^{2}$
- $uv - v$
- $u^{2} + uv + v^{2}$
- $u + v$
- $uv + v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u + v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 4,\,-2\le v\le 3\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u + v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u + v)⟩ \\  & =⟨0,\,1,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & 1\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,-1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨- y + z,\,2 y - z,\,xy⟩{|}_{x=u,\,\,y=v,\,\,z=u + v} \\  & =⟨- v + (u + v),\,2 v - (u + v),\,uv⟩ \\  & =⟨u,\,- u + v,\,uv⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u,\,- u + v,\,uv⟩\cdot ⟨-1,\,-1,\,1⟩ \\  & =(u)\cdot (-1)+(- u + v)\cdot (-1)+(uv)\cdot (1) \\  & =- u+u - v+uv \\  & =uv - v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨- y + z,\,2 y - z,\,xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(uv - v)\,\text{d}A \\  & ={\int }_{0}^{4}{\int }_{-2}^{3}(uv - v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Original q-161360 / q-161360-legacy

Consider the vector field $F(x,y,z)=⟨{x}^{2},\,{y}^{2},\,{z}^{2}⟩$ and the surface $S$ defined by $z=x+y$ for $0\le x\le 2$ and $0\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{2}{\int }_{0}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?


Original complete bank: $u^{2} + v^{2}$, $u^{2} - v^{2}$, $u^{2} + uv + v^{2}$, $2uv$, $2(u + v)^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u+v⟩
$$

over the domain 

$$
D={(u,v)\,:\,0\le u\le 2,\,0\le v\le 2}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u+v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u+v)⟩ \\  & =⟨0,\,1,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & 1\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,-1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨{x}^{2},\,{y}^{2},\,{z}^{2}⟩{|}_{x=u,\,\,y=v,\,\,z=u+v} \\  & =⟨{u}^{2},\,{v}^{2},\,(u+v)^{2}⟩\end{aligned}
$$

 

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨{u}^{2},\,{v}^{2},\,(u+v)^{2}⟩\cdot ⟨-1,\,-1,\,1⟩ \\  & ={u}^{2}\cdot (-1)+{v}^{2}\cdot (-1)+(u+v)^{2}\cdot 1 \\  & =-{u}^{2}-{v}^{2}+{u}^{2}+2uv+{v}^{2} \\  & =2uv.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨{x}^{2},\,{y}^{2},\,{z}^{2}⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(2uv)\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{0}^{2}2uv\,\text{d}v\,\text{d}u.\end{aligned}
$$

### Reconstructed at original parameters

Consider the vector field $F(x,y,z)=⟨x^{2},\,y^{2},\,z^{2}⟩$ and the surface $S$ defined by $z=x + y$ for $0\le x\le 2$ and $0\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{2}{\int }_{0}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $u^{2} - v^{2}$
- $u^{2} + uv + v^{2}$
- $2 uv$
- $2 u^{2} + 4 uv + 2 v^{2}$
- $u^{2} + v^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u + v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 2,\,0\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u + v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u + v)⟩ \\  & =⟨0,\,1,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & 1\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,-1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨x^{2},\,y^{2},\,z^{2}⟩{|}_{x=u,\,\,y=v,\,\,z=u + v} \\  & =⟨u^{2},\,v^{2},\,(u + v)^{2}⟩\end{aligned}
$$

 

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u^{2},\,v^{2},\,(u + v)^{2}⟩\cdot ⟨-1,\,-1,\,1⟩ \\  & =(u^{2})\cdot (-1)+(v^{2})\cdot (-1)+((u + v)^{2})\cdot (1) \\  & =- u^{2}- v^{2}+u^{2} + 2 uv + v^{2} \\  & =2 uv.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨x^{2},\,y^{2},\,z^{2}⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(2 uv)\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{0}^{2}(2 uv)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Original q-161360 / q-161360

Consider the vector field $F(x,y,z)=⟨{x}^{2},\,{y}^{2},\,{z}^{2}⟩$ and the surface $S$ defined by $z=x+y$ for $0\le x\le 2$ and $0\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{2}{\int }_{0}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?


Original complete bank: ${u}^{2}+{v}^{2}$, ${u}^{2}+uv+{v}^{2}$, $2uv$, ${u}^{2}-{v}^{2}$, $2(u+v)^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u+v⟩
$$

over the domain 

$$
D={(u,v)\,:\,0\le u\le 2,\,0\le v\le 2}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u+v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u+v)⟩ \\  & =⟨0,\,1,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & 1\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,-1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨{x}^{2},\,{y}^{2},\,{z}^{2}⟩{|}_{x=u,\,\,y=v,\,\,z=u+v} \\  & =⟨{u}^{2},\,{v}^{2},\,(u+v)^{2}⟩\end{aligned}
$$

 

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨{u}^{2},\,{v}^{2},\,(u+v)^{2}⟩\cdot ⟨-1,\,-1,\,1⟩ \\  & ={u}^{2}\cdot (-1)+{v}^{2}\cdot (-1)+(u+v)^{2}\cdot 1 \\  & =-{u}^{2}-{v}^{2}+{u}^{2}+2uv+{v}^{2} \\  & =2uv.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨{x}^{2},\,{y}^{2},\,{z}^{2}⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(2uv)\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{0}^{2}2uv\,\text{d}v\,\text{d}u.\end{aligned}
$$

### Reconstructed at original parameters

Consider the vector field $F(x,y,z)=⟨x^{2},\,y^{2},\,z^{2}⟩$ and the surface $S$ defined by $z=x + y$ for $0\le x\le 2$ and $0\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{2}{\int }_{0}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $u^{2} - v^{2}$
- $u^{2} + uv + v^{2}$
- $2 uv$
- $2 u^{2} + 4 uv + 2 v^{2}$
- $u^{2} + v^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u + v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 2,\,0\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u + v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u + v)⟩ \\  & =⟨0,\,1,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & 1\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,-1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨x^{2},\,y^{2},\,z^{2}⟩{|}_{x=u,\,\,y=v,\,\,z=u + v} \\  & =⟨u^{2},\,v^{2},\,(u + v)^{2}⟩\end{aligned}
$$

 

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u^{2},\,v^{2},\,(u + v)^{2}⟩\cdot ⟨-1,\,-1,\,1⟩ \\  & =(u^{2})\cdot (-1)+(v^{2})\cdot (-1)+((u + v)^{2})\cdot (1) \\  & =- u^{2}- v^{2}+u^{2} + 2 uv + v^{2} \\  & =2 uv.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨x^{2},\,y^{2},\,z^{2}⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(2 uv)\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{0}^{2}(2 uv)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Original q-161358 / q-161358

Consider the vector field $F(x,y,z)=⟨z,\,-y,\,2x⟩$ and the surface $S$ defined by $z=3x-2y$ for $0\le x\le 5$ and $-3\le y\le 3.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{5}{\int }_{-3}^{3}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?


Original complete bank: $-7u+4v$, $4u+7v$, $7u+8v$, $8u-7v$, $-7u-8v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,3u-2v⟩
$$

over the domain 

$$
D={(u,v)\,:\,0\le u\le 5,\,-3\le v\le 3}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(3u-2v)⟩ \\  & =⟨1,\,0,\,3⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(3u-2v)⟩ \\  & =⟨0,\,1,\,-2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 3 \\ 0 & 1 & -2\end{aligned}| \\  & =⟨|\begin{aligned}0 & 3 \\ 1 & -2\end{aligned}|,\,-|\begin{aligned}1 & 3 \\ 0 & -2\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-3,\,2,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨z,\,-y,\,2x⟩{|}_{x=u,\,\,y=v,\,\,z=3u-2v} \\  & =⟨3u-2v,\,-v,\,2u⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3u-2v,\,-v,\,2u⟩\cdot ⟨-3,\,2,\,1⟩ \\  & =(3u-2v)\cdot (-3)+(-v)\cdot (2)+2u\cdot 1 \\  & =-9u+6v-2v+2u \\  & =-7u+4v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨z,\,-y,\,2x⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-7u+4v)\,\text{d}A \\  & ={\int }_{0}^{5}{\int }_{-3}^{3}(-7u+4v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

### Reconstructed at original parameters

Consider the vector field $F(x,y,z)=⟨z,\,- y,\,2 x⟩$ and the surface $S$ defined by $z=3 x - 2 y$ for $0\le x\le 5$ and $-3\le y\le 3.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{5}{\int }_{-3}^{3}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $8 u - 7 v$
- $4 u + 7 v$
- $7 u + 8 v$
- $- 7 u - 8 v$
- $- 7 u + 4 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,3 u - 2 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 5,\,-3\le v\le 3\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(3 u - 2 v)⟩ \\  & =⟨1,\,0,\,3⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(3 u - 2 v)⟩ \\  & =⟨0,\,1,\,-2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 3 \\ 0 & 1 & -2\end{aligned}| \\  & =⟨|\begin{aligned}0 & 3 \\ 1 & -2\end{aligned}|,\,-|\begin{aligned}1 & 3 \\ 0 & -2\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-3,\,2,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨z,\,- y,\,2 x⟩{|}_{x=u,\,\,y=v,\,\,z=3 u - 2 v} \\  & =⟨(3 u - 2 v),\,- v,\,2 u⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨(3 u - 2 v),\,- v,\,2 u⟩\cdot ⟨-3,\,2,\,1⟩ \\  & =((3 u - 2 v))\cdot (-3)+(- v)\cdot (2)+(2 u)\cdot (1) \\  & =- 9 u + 6 v- 2 v+2 u \\  & =- 7 u + 4 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨z,\,- y,\,2 x⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- 7 u + 4 v)\,\text{d}A \\  & ={\int }_{0}^{5}{\int }_{-3}^{3}(- 7 u + 4 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Original q-161441 / q-161441

Consider the vector field $F(x,y,z)=⟨x,\,y-z,\,x+y⟩$ and the surface $S$ defined by $z=x-2y$ for $0\le x\le 1$ and $-1\le y\le 1.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{1}{\int }_{-1}^{1}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?


Original complete bank: $-2u+7v$, $4u+v$, $4v-u$, $-2u+v$, $2u+4v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u-2v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 1,\,-1\le v\le 1\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u-2v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u-2v)⟩ \\  & =⟨0,\,1,\,-2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & -2\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & -2\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & -2\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,2,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨x,\,y-z,\,x+y⟩{|}_{x=u,\,\,y=v,\,\,z=u-2v} \\  & =⟨u,\,v-(u-2v),\,u+v⟩ \\  & =⟨u,\,3v-u,\,u+v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u,\,3v-u,\,u+v⟩\cdot ⟨-1,\,2,\,1⟩ \\  & =u\cdot (-1)+(3v-u)\cdot 2+(u+v)\cdot 1 \\  & =-u+6v-2u+u+v \\  & =-2u+7v.\end{aligned}
$$

 

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨x,\,y-z,\,x+y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(-2u+7v)\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{-1}^{1}(-2u+7v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

### Reconstructed at original parameters

Consider the vector field $F(x,y,z)=⟨x,\,y - z,\,x + y⟩$ and the surface $S$ defined by $z=x - 2 y$ for $0\le x\le 1$ and $-1\le y\le 1.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{1}{\int }_{-1}^{1}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $- 2 u + v$
- $4 u + v$
- $- u + 4 v$
- $2 u + 4 v$
- $- 2 u + 7 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u - 2 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 1,\,-1\le v\le 1\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u - 2 v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u - 2 v)⟩ \\  & =⟨0,\,1,\,-2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & -2\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & -2\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & -2\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,2,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨x,\,y - z,\,x + y⟩{|}_{x=u,\,\,y=v,\,\,z=u - 2 v} \\  & =⟨u,\,v - (u - 2 v),\,u + v⟩ \\  & =⟨u,\,- u + 3 v,\,u + v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u,\,- u + 3 v,\,u + v⟩\cdot ⟨-1,\,2,\,1⟩ \\  & =(u)\cdot (-1)+(- u + 3 v)\cdot (2)+(u + v)\cdot (1) \\  & =- u- 2 u + 6 v+u + v \\  & =- 2 u + 7 v.\end{aligned}
$$

 

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨x,\,y - z,\,x + y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- 2 u + 7 v)\,\text{d}A \\  & ={\int }_{0}^{1}{\int }_{-1}^{1}(- 2 u + 7 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Original q-161462 / q-161462

Consider the vector field $F(x,y,z)=⟨z,\,y+2z,\,2x-y⟩$ and the surface $S$ defined by $z=y-x$ for $0\le x\le 2$ and $-1\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as 

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{2}{\int }_{-1}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?


Original complete bank: $3u-3v$, $2u+v$, $u+2v$, $2u-3v$, $3v+u$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,v-u⟩
$$

over the domain 

$$
D={(u,v)\,:\,0\le u\le 2,\,-1\le v\le 2}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(v-u)⟩ \\  & =⟨1,\,0,\,-1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(v-u)⟩ \\  & =⟨0,\,1,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -1 \\ 0 & 1 & 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & -1 \\ 1 & 1\end{aligned}|,\,-|\begin{aligned}1 & -1 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨1,\,-1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨z,\,y+2z,\,2x-y⟩{|}_{x=u,\,\,y=v,\,\,z=v-u} \\  & =⟨v-u,\,v+2(v-u),\,2u-v⟩ \\  & =⟨v-u,\,3v-2u,\,2u-v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨v-u,\,3v-2u,\,2u-v⟩\cdot ⟨1,\,-1,\,1⟩ \\  & =(v-u)\cdot 1+(3v-2u)\cdot (-1)+(2u-v)\cdot 1 \\  & =v-u-3v+2u+2u-v \\  & =3u-3v.\end{aligned}
$$

 

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨z,\,y+2z,\,2x-y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(3u-3v)\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{2}(3u-3v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

### Reconstructed at original parameters

Consider the vector field $F(x,y,z)=⟨z,\,y + 2 z,\,2 x - y⟩$ and the surface $S$ defined by $z=- x + y$ for $0\le x\le 2$ and $-1\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{2}{\int }_{-1}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $2 u - 3 v$
- $2 u + v$
- $u + 2 v$
- $u + 3 v$
- $3 u - 3 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,- u + v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 2,\,-1\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(- u + v)⟩ \\  & =⟨1,\,0,\,-1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(- u + v)⟩ \\  & =⟨0,\,1,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -1 \\ 0 & 1 & 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & -1 \\ 1 & 1\end{aligned}|,\,-|\begin{aligned}1 & -1 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨1,\,-1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨z,\,y + 2 z,\,2 x - y⟩{|}_{x=u,\,\,y=v,\,\,z=- u + v} \\  & =⟨(- u + v),\,v + 2 (- u + v),\,2 u - v⟩ \\  & =⟨- u + v,\,- 2 u + 3 v,\,2 u - v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨- u + v,\,- 2 u + 3 v,\,2 u - v⟩\cdot ⟨1,\,-1,\,1⟩ \\  & =(- u + v)\cdot (1)+(- 2 u + 3 v)\cdot (-1)+(2 u - v)\cdot (1) \\  & =- u + v+2 u - 3 v+2 u - v \\  & =3 u - 3 v.\end{aligned}
$$

 

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨z,\,y + 2 z,\,2 x - y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(3 u - 3 v)\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{2}(3 u - 3 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Original q-161381 / q-161381

Consider the vector field $F(x,y,z)=⟨z+x,\,y+2z,\,x-4y⟩$ and the surface $S$ defined by $z=2x-4y$ for $-2\le x\le 0$ and $-1\le y\le 5.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{0}{\int }_{-1}^{5}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?


Original complete bank: $7uv-4v$, $11u-24v$, $11u+4v$, $u-v$, $24uv$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,2u-4v⟩
$$

over the domain 

$$
D={(u,v)\,:\,-2\le u\le 0,\,-1\le v\le 5}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(2u-4v)⟩ \\  & =⟨1,\,0,\,2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(2u-4v)⟩ \\  & =⟨0,\,1,\,-4⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 2 \\ 0 & 1 & -4\end{aligned}| \\  & =⟨|\begin{aligned}0 & 2 \\ 1 & -4\end{aligned}|,\,-|\begin{aligned}1 & 2 \\ 0 & -4\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-2,\,4,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨z+x,\,y+2z,\,x-4y⟩{|}_{x=u,\,\,y=v,\,\,z=2u-4v} \\  & =⟨2u-4v+u,\,v+2(2u-4v),\,u-4v⟩ \\  & =⟨3u-4v,\,4u-7v,\,u-4v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3u-4v,\,4u-7v,\,u-4v⟩\cdot ⟨-2,\,4,\,1⟩ \\  & =(3u-4v)\cdot (-2)+(4u-7v)\cdot 4+(u-4v)\cdot 1 \\  & =-6u+8v+16u-28v+u-4v \\  & =11u-24v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨z+x,\,y+2z,\,x-4y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(11u-24v)\,\text{d}A \\  & ={\int }_{-2}^{0}{\int }_{-1}^{5}(11u-24v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

### Reconstructed at original parameters

Consider the vector field $F(x,y,z)=⟨x + z,\,y + 2 z,\,x - 4 y⟩$ and the surface $S$ defined by $z=2 x - 4 y$ for $-2\le x\le 0$ and $-1\le y\le 5.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{0}{\int }_{-1}^{5}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $u - v$
- $11 u - 24 v$
- $11 u + 4 v$
- $24 uv$
- $7 uv - 4 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,2 u - 4 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 0,\,-1\le v\le 5\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(2 u - 4 v)⟩ \\  & =⟨1,\,0,\,2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(2 u - 4 v)⟩ \\  & =⟨0,\,1,\,-4⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 2 \\ 0 & 1 & -4\end{aligned}| \\  & =⟨|\begin{aligned}0 & 2 \\ 1 & -4\end{aligned}|,\,-|\begin{aligned}1 & 2 \\ 0 & -4\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-2,\,4,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨x + z,\,y + 2 z,\,x - 4 y⟩{|}_{x=u,\,\,y=v,\,\,z=2 u - 4 v} \\  & =⟨u + (2 u - 4 v),\,v + 2 (2 u - 4 v),\,u - 4 v⟩ \\  & =⟨3 u - 4 v,\,4 u - 7 v,\,u - 4 v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨3 u - 4 v,\,4 u - 7 v,\,u - 4 v⟩\cdot ⟨-2,\,4,\,1⟩ \\  & =(3 u - 4 v)\cdot (-2)+(4 u - 7 v)\cdot (4)+(u - 4 v)\cdot (1) \\  & =- 6 u + 8 v+16 u - 28 v+u - 4 v \\  & =11 u - 24 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨x + z,\,y + 2 z,\,x - 4 y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(11 u - 24 v)\,\text{d}A \\  & ={\int }_{-2}^{0}{\int }_{-1}^{5}(11 u - 24 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Original q-161467 / q-161467

Consider the vector field $F(x,y,z)=⟨2x-z,\,y-z,\,z+y⟩$ and the surface $S$ defined by $z=4x-y$ for $0\le x\le 2$ and $-1\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as 

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{2}{\int }_{-1}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?


Original complete bank: $8u$, $u-2v$, $8u-2v$, $-4v$, $2u+4v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4u-v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 2,\,-1\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4u-v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4u-v)⟩ \\  & =⟨0,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & -1\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & -1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2x-z,\,y-z,\,z+y⟩{|}_{x=u,\,\,y=v,\,\,z=4u-v} \\  & =⟨2u-(4u-v),\,v-(4u-v),\,4u-v+v⟩ \\  & =⟨-2u+v,\,-4u+2v,\,4u⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨-2u+v,\,-4u+2v,\,4u⟩\cdot ⟨-4,\,1,\,1⟩ \\  & =(-2u+v)\cdot (-4)+(-4u+2v)\cdot 1+4u\cdot 1 \\  & =8u-4v+-4u+2v+4u \\  & =8u-2v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2x-z,\,y-z,\,z+y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(8u-2v)\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{2}(8u-2v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

### Reconstructed at original parameters

Consider the vector field $F(x,y,z)=⟨2 x - z,\,y - z,\,y + z⟩$ and the surface $S$ defined by $z=4 x - y$ for $0\le x\le 2$ and $-1\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{2}{\int }_{-1}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $- 4 v$
- $u - 2 v$
- $8 u - 2 v$
- $2 u + 4 v$
- $8 u$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u - v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 2,\,-1\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u - v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u - v)⟩ \\  & =⟨0,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & -1\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & -1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 x - z,\,y - z,\,y + z⟩{|}_{x=u,\,\,y=v,\,\,z=4 u - v} \\  & =⟨2 u - (4 u - v),\,v - (4 u - v),\,v + (4 u - v)⟩ \\  & =⟨- 2 u + v,\,- 4 u + 2 v,\,4 u⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨- 2 u + v,\,- 4 u + 2 v,\,4 u⟩\cdot ⟨-4,\,1,\,1⟩ \\  & =(- 2 u + v)\cdot (-4)+(- 4 u + 2 v)\cdot (1)+(4 u)\cdot (1) \\  & =8 u - 4 v- 4 u + 2 v+4 u \\  & =8 u - 2 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 x - z,\,y - z,\,y + z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(8 u - 2 v)\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{2}(8 u - 2 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Original q-161357 / q-161357

Consider the vector field $F(x,y,z)=⟨x+y,\,2x-y,\,x+z⟩$ and the surface $S$ defined by $z=2x-2y$ for $0\le x\le 2$ and $-1\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{2}{\int }_{-1}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?


Original complete bank: $-2u+v$, $3uv$, $11uv$, $u+v$, $5u-6v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,2u-2v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 2,\,-1\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(2u-2v)⟩ \\  & =⟨1,\,0,\,2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(2u-2v)⟩ \\  & =⟨0,\,1,\,-2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 2 \\ 0 & 1 & -2\end{aligned}| \\  & =⟨|\begin{aligned}0 & 2 \\ 1 & -2\end{aligned}|,\,-|\begin{aligned}1 & 2 \\ 0 & -2\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-2,\,2,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨x+y,\,2x-y,\,x+z⟩{|}_{x=u,\,\,y=v,\,\,z=2u-2v} \\  & =⟨u+v,\,2u-v,\,u+(2u-2v)⟩ \\  & =⟨u+v,\,2u-v,\,3u-2v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u+v,\,2u-v,\,3u-2v⟩\cdot ⟨-2,\,2,\,1⟩ \\  & =(u+v)\cdot (-2)+(2u-v)\cdot (2)+(3u-2v)\cdot 1 \\  & =-2u-2v+4u-2v+3u-2v \\  & =5u-6v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨x+y,\,2x-y,\,x+z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(5u-6v)\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{2}(5u-6v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

### Reconstructed at original parameters

Consider the vector field $F(x,y,z)=⟨x + y,\,2 x - y,\,x + z⟩$ and the surface $S$ defined by $z=2 x - 2 y$ for $0\le x\le 2$ and $-1\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{2}{\int }_{-1}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $u + v$
- $3 uv$
- $11 uv$
- $5 u - 6 v$
- $- 2 u + v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,2 u - 2 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 2,\,-1\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(2 u - 2 v)⟩ \\  & =⟨1,\,0,\,2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(2 u - 2 v)⟩ \\  & =⟨0,\,1,\,-2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 2 \\ 0 & 1 & -2\end{aligned}| \\  & =⟨|\begin{aligned}0 & 2 \\ 1 & -2\end{aligned}|,\,-|\begin{aligned}1 & 2 \\ 0 & -2\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-2,\,2,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨x + y,\,2 x - y,\,x + z⟩{|}_{x=u,\,\,y=v,\,\,z=2 u - 2 v} \\  & =⟨u + v,\,2 u - v,\,u + (2 u - 2 v)⟩ \\  & =⟨u + v,\,2 u - v,\,3 u - 2 v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u + v,\,2 u - v,\,3 u - 2 v⟩\cdot ⟨-2,\,2,\,1⟩ \\  & =(u + v)\cdot (-2)+(2 u - v)\cdot (2)+(3 u - 2 v)\cdot (1) \\  & =- 2 u - 2 v+4 u - 2 v+3 u - 2 v \\  & =5 u - 6 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨x + y,\,2 x - y,\,x + z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(5 u - 6 v)\,\text{d}A \\  & ={\int }_{0}^{2}{\int }_{-1}^{2}(5 u - 6 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Original q-161359 / q-161359

Consider the vector field $F(x,y,z)=⟨zy,\,xz,\,xy⟩$ and the surface $S$ defined by $z=x-y$ for $-1\le x\le 1$ and $0\le y\le 1.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-1}^{1}{\int }_{0}^{1}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?


Original complete bank: ${u}^{2}-uv+{v}^{2}$, ${u}^{2}-{v}^{2}$, $(u+v)^{2}$, $(u-v)^{2}$, ${u}^{2}+uv-{v}^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u-v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-1\le u\le 1,\,0\le v\le 1\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u-v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u-v)⟩ \\  & =⟨0,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & -1\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & -1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨zy,\,xz,\,xy⟩{|}_{x=u,\,\,y=v,\,\,z=u-v} \\  & =⟨(u-v)v,\,(u-v)u,\,uv⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨(u-v)v,\,(u-v)u,\,uv⟩\cdot ⟨-1,\,1,\,1⟩ \\  & =(u-v)v\cdot (-1)+(u-v)u\cdot (1)+uv\cdot 1 \\  & =-uv+{v}^{2}+{u}^{2}-uv+uv \\  & ={u}^{2}-uv+{v}^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨zy,\,xz,\,xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}({u}^{2}-uv+{v}^{2})\,\text{d}A \\  & ={\int }_{-1}^{1}{\int }_{0}^{1}({u}^{2}-uv+{v}^{2})\,\text{d}v\,\text{d}u.\end{aligned}
$$

### Reconstructed at original parameters

Consider the vector field $F(x,y,z)=⟨y z,\,x z,\,xy⟩$ and the surface $S$ defined by $z=x - y$ for $-1\le x\le 1$ and $0\le y\le 1.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-1}^{1}{\int }_{0}^{1}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $u^{2} - 2 uv + v^{2}$
- $u^{2} - v^{2}$
- $u^{2} + 2 uv + v^{2}$
- $u^{2} + uv - v^{2}$
- $u^{2} - uv + v^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u - v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-1\le u\le 1,\,0\le v\le 1\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u - v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u - v)⟩ \\  & =⟨0,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & -1\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & -1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨y z,\,x z,\,xy⟩{|}_{x=u,\,\,y=v,\,\,z=u - v} \\  & =⟨v (u - v),\,u (u - v),\,uv⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨v (u - v),\,u (u - v),\,uv⟩\cdot ⟨-1,\,1,\,1⟩ \\  & =(v (u - v))\cdot (-1)+(u (u - v))\cdot (1)+(uv)\cdot (1) \\  & =- uv + v^{2}+u^{2} - uv+uv \\  & =u^{2} - uv + v^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨y z,\,x z,\,xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(u^{2} - uv + v^{2})\,\text{d}A \\  & ={\int }_{-1}^{1}{\int }_{0}^{1}(u^{2} - uv + v^{2})\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Original q-161377 / q-161377

Consider the vector field $F(x,y,z)=⟨{x}^{2}-{y}^{2},\,{y}^{2}-{z}^{2},\,{z}^{2}⟩$ and the surface $S$ defined by $z=-x-y$ for $-2\le x\le 2$ and $-2\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{2}{\int }_{-2}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?


Original complete bank: ${u}^{2}$, $4uv$, ${u}^{3}$, $2uv$, $3v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,-u-v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 2,\,-2\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(-u-v)⟩ \\  & =⟨1,\,0,\,-1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(-u-v)⟩ \\  & =⟨0,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -1 \\ 0 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}0 & -1 \\ 1 & -1\end{aligned}|,\,-|\begin{aligned}1 & -1 \\ 0 & -1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨1,\,1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨{x}^{2}-{y}^{2},\,{y}^{2}-{z}^{2},\,{z}^{2}⟩{|}_{x=u,\,\,y=v,\,\,z=-u-v} \\  & =⟨{u}^{2}-{v}^{2},\,{v}^{2}-(-u-v)^{2},\,(-u-v)^{2}⟩\end{aligned}
$$

 

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨{u}^{2}-{v}^{2},\,{v}^{2}-(-u-v)^{2},\,(-u-v)^{2}⟩\cdot ⟨1,\,1,\,1⟩ \\  & =({u}^{2}-{v}^{2})\cdot (1)+({v}^{2}-(-u-v)^{2})\cdot (1)+(-u-v)^{2}\cdot 1 \\  & ={u}^{2}-{v}^{2}+{v}^{2}-(-u-v)^{2}+(-u-v)^{2} \\  & ={u}^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨{x}^{2}-{y}^{2},\,{y}^{2}-{z}^{2},\,{z}^{2}⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}{u}^{2}\,\text{d}A \\  & ={\int }_{-2}^{2}{\int }_{-2}^{2}{u}^{2}\,\text{d}v\,\text{d}u.\end{aligned}
$$

### Reconstructed at original parameters

Consider the vector field $F(x,y,z)=⟨x^{2} - y^{2},\,y^{2} - z^{2},\,z^{2}⟩$ and the surface $S$ defined by $z=- x - y$ for $-2\le x\le 2$ and $-2\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{2}{\int }_{-2}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $2 uv$
- $4 uv$
- $u^{3}$
- $3 v$
- $u^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,- u - v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 2,\,-2\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(- u - v)⟩ \\  & =⟨1,\,0,\,-1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(- u - v)⟩ \\  & =⟨0,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -1 \\ 0 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}0 & -1 \\ 1 & -1\end{aligned}|,\,-|\begin{aligned}1 & -1 \\ 0 & -1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨1,\,1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨x^{2} - y^{2},\,y^{2} - z^{2},\,z^{2}⟩{|}_{x=u,\,\,y=v,\,\,z=- u - v} \\  & =⟨u^{2} - v^{2},\,v^{2} - (- u - v)^{2},\,(- u - v)^{2}⟩\end{aligned}
$$

 

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u^{2} - v^{2},\,v^{2} - (- u - v)^{2},\,(- u - v)^{2}⟩\cdot ⟨1,\,1,\,1⟩ \\  & =(u^{2} - v^{2})\cdot (1)+(v^{2} - (- u - v)^{2})\cdot (1)+((- u - v)^{2})\cdot (1) \\  & =u^{2} - v^{2}+v^{2} - \left(- u - v\right)^{2}+\left(- u - v\right)^{2} \\  & =u^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨x^{2} - y^{2},\,y^{2} - z^{2},\,z^{2}⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(u^{2})\,\text{d}A \\  & ={\int }_{-2}^{2}{\int }_{-2}^{2}(u^{2})\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Original q-161379 / q-161379

Consider the vector field $F(x,y,z)=⟨(x+y)^{2},\,(x-y)^{2},\,xy⟩$ and the surface $S$ defined by $z=y-x$ for $-1\le x\le 1$ and $-3\le y\le 0.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-1}^{1}{\int }_{-3}^{0}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?


Original complete bank: $-uv$, $5uv$, $3u{v}^{2}$, $uv+v$, $uv-v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,v-u⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-1\le u\le 1,\,-3\le v\le 0\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(v-u)⟩ \\  & =⟨1,\,0,\,-1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(v-u)⟩ \\  & =⟨0,\,1,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -1 \\ 0 & 1 & 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & -1 \\ 1 & 1\end{aligned}|,\,-|\begin{aligned}1 & -1 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨1,\,-1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨(x+y)^{2},\,(x-y)^{2},\,xy⟩{|}_{x=u,\,\,y=v,\,\,z=v-u} \\  & =⟨(u+v)^{2},\,(u-v)^{2},\,uv⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨(u+v)^{2},\,(u-v)^{2},\,uv⟩\cdot ⟨1,\,-1,\,1⟩ \\  & =(u+v)^{2}\cdot 1+(u-v)^{2}\cdot (-1)+uv\cdot 1 \\  & =5uv.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨(x+y)^{2},\,(x-y)^{2},\,xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(5uv)\,\text{d}A \\  & ={\int }_{-1}^{1}{\int }_{-3}^{0}5uv\,\text{d}v\,\text{d}u.\end{aligned}
$$

### Reconstructed at original parameters

Consider the vector field $F(x,y,z)=⟨\left(x + y\right)^{2},\,\left(x - y\right)^{2},\,xy⟩$ and the surface $S$ defined by $z=- x + y$ for $-1\le x\le 1$ and $-3\le y\le 0.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-1}^{1}{\int }_{-3}^{0}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $uv + v$
- $5 uv$
- $3 uv^{2}$
- $uv - v$
- $- uv$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,- u + v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-1\le u\le 1,\,-3\le v\le 0\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(- u + v)⟩ \\  & =⟨1,\,0,\,-1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(- u + v)⟩ \\  & =⟨0,\,1,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -1 \\ 0 & 1 & 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & -1 \\ 1 & 1\end{aligned}|,\,-|\begin{aligned}1 & -1 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨1,\,-1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨\left(x + y\right)^{2},\,\left(x - y\right)^{2},\,xy⟩{|}_{x=u,\,\,y=v,\,\,z=- u + v} \\  & =⟨\left(u + v\right)^{2},\,\left(u - v\right)^{2},\,uv⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨\left(u + v\right)^{2},\,\left(u - v\right)^{2},\,uv⟩\cdot ⟨1,\,-1,\,1⟩ \\  & =(\left(u + v\right)^{2})\cdot (1)+(\left(u - v\right)^{2})\cdot (-1)+(uv)\cdot (1) \\  & =5 uv.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨\left(x + y\right)^{2},\,\left(x - y\right)^{2},\,xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(5 uv)\,\text{d}A \\  & ={\int }_{-1}^{1}{\int }_{-3}^{0}(5 uv)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Original q-161471 / q-161471

Consider the vector field $F(x,y,z)=⟨x+z,\,2z,\,y+z⟩$ and the surface $S$ defined by $z=x-3y$ for $-1\le x\le 2$ and $-1\le y\le 3.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-1}^{2}{\int }_{-1}^{3}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?


Original complete bank: $8u-23v$, $12u-v$, $8u+14v$, $5u-17v$, $u-6v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u-3v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-1\le u\le 2,\,-1\le v\le 3\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u-3v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u-3v)⟩ \\  & =⟨0,\,1,\,-3⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & -3\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & -3\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & -3\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,3,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨x+z,\,2z,\,y+z⟩{|}_{x=u,\,\,y=v,\,\,z=u-3v} \\  & =⟨u+u-3v,\,2(u-3v),\,v+u-3v⟩ \\  & =⟨2u-3v,\,2u-6v,\,u-2v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2u-3v,\,2u-6v,\,u-2v⟩\cdot ⟨-1,\,3,\,1⟩ \\  & =(2u-3v)\cdot (-1)+(2u-6v)\cdot (3)+(u-2v)\cdot 1 \\  & =-2u+3v+6u-18v+u-2v \\  & =5u-17v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨z-y,\,2y-z,\,xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A \\  & ={∬}_{D}(5u-17v)\,\text{d}A \\  & ={\int }_{-1}^{2}{\int }_{-1}^{3}(5u-17v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

### Reconstructed at original parameters

Consider the vector field $F(x,y,z)=⟨x + z,\,2 z,\,y + z⟩$ and the surface $S$ defined by $z=x - 3 y$ for $-1\le x\le 2$ and $-1\le y\le 3.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-1}^{2}{\int }_{-1}^{3}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $5 u - 17 v$
- $12 u - v$
- $8 u + 14 v$
- $u - 6 v$
- $8 u - 23 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u - 3 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-1\le u\le 2,\,-1\le v\le 3\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u - 3 v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u - 3 v)⟩ \\  & =⟨0,\,1,\,-3⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & -3\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & -3\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & -3\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,3,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨x + z,\,2 z,\,y + z⟩{|}_{x=u,\,\,y=v,\,\,z=u - 3 v} \\  & =⟨u + (u - 3 v),\,2 (u - 3 v),\,v + (u - 3 v)⟩ \\  & =⟨2 u - 3 v,\,2 u - 6 v,\,u - 2 v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 u - 3 v,\,2 u - 6 v,\,u - 2 v⟩\cdot ⟨-1,\,3,\,1⟩ \\  & =(2 u - 3 v)\cdot (-1)+(2 u - 6 v)\cdot (3)+(u - 2 v)\cdot (1) \\  & =- 2 u + 3 v+6 u - 18 v+u - 2 v \\  & =5 u - 17 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨x + z,\,2 z,\,y + z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(5 u - 17 v)\,\text{d}A \\  & ={\int }_{-1}^{2}{\int }_{-1}^{3}(5 u - 17 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-160887 0

Consider the vector field $F(x,y,z)=⟨y - z,\,- 2 y + z,\,- xy⟩$ and the surface $S$ defined by $z=4 x + 3 y$ for $0\le x\le 5$ and $-3\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{5}{\int }_{-3}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $uv - 4 u - 5 v$
- $- uv + 4 u + 5 v$
- $4 u + 5 v$
- $- uv - 28 u - 11 v$
- $- uv + 28 u + 11 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 3 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 5,\,-3\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 3 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 3 v)⟩ \\  & =⟨0,\,1,\,3⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 3\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 3\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 3\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-3,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨y - z,\,- 2 y + z,\,- xy⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 3 v} \\  & =⟨v - (4 u + 3 v),\,- 2 v + (4 u + 3 v),\,- uv⟩ \\  & =⟨- 4 u - 2 v,\,4 u + v,\,- uv⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨- 4 u - 2 v,\,4 u + v,\,- uv⟩\cdot ⟨-4,\,-3,\,1⟩ \\  & =(- 4 u - 2 v)\cdot (-4)+(4 u + v)\cdot (-3)+(- uv)\cdot (1) \\  & =16 u + 8 v- 12 u - 3 v- uv \\  & =- uv + 4 u + 5 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨y - z,\,- 2 y + z,\,- xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- uv + 4 u + 5 v)\,\text{d}A \\  & ={\int }_{0}^{5}{\int }_{-3}^{4}(- uv + 4 u + 5 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-160887 1

Consider the vector field $F(x,y,z)=⟨- y + z,\,2 y - z,\,xy⟩$ and the surface $S$ defined by $z=4 x + 4 y$ for $-2\le x\le 2$ and $-1\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{2}{\int }_{-1}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $uv + 32 u + 20 v$
- $- 4 v$
- $uv - 4 v$
- $- uv + 4 v$
- $uv - 32 u - 20 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 4 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 2,\,-1\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 4 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 4 v)⟩ \\  & =⟨0,\,1,\,4⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 4\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 4\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 4\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-4,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨- y + z,\,2 y - z,\,xy⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 4 v} \\  & =⟨- v + (4 u + 4 v),\,2 v - (4 u + 4 v),\,uv⟩ \\  & =⟨4 u + 3 v,\,- 4 u - 2 v,\,uv⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨4 u + 3 v,\,- 4 u - 2 v,\,uv⟩\cdot ⟨-4,\,-4,\,1⟩ \\  & =(4 u + 3 v)\cdot (-4)+(- 4 u - 2 v)\cdot (-4)+(uv)\cdot (1) \\  & =- 16 u - 12 v+16 u + 8 v+uv \\  & =uv - 4 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨- y + z,\,2 y - z,\,xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(uv - 4 v)\,\text{d}A \\  & ={\int }_{-2}^{2}{\int }_{-1}^{2}(uv - 4 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161360 0

Consider the vector field $F(x,y,z)=⟨- x^{2},\,- y^{2},\,- z^{2}⟩$ and the surface $S$ defined by $z=4 x + 3 y$ for $0\le x\le 5$ and $-3\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{5}{\int }_{-3}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $12 u^{2} + 24 uv + 6 v^{2}$
- $- 12 u^{2} - 24 uv - 6 v^{2}$
- $4 u^{2} + 3 v^{2}$
- $- 20 u^{2} - 24 uv - 6 v^{2}$
- $- 12 u^{2} - 24 uv - 12 v^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 3 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 5,\,-3\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 3 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 3 v)⟩ \\  & =⟨0,\,1,\,3⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 3\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 3\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 3\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-3,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨- x^{2},\,- y^{2},\,- z^{2}⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 3 v} \\  & =⟨- u^{2},\,- v^{2},\,- (4 u + 3 v)^{2}⟩\end{aligned}
$$

 

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨- u^{2},\,- v^{2},\,- (4 u + 3 v)^{2}⟩\cdot ⟨-4,\,-3,\,1⟩ \\  & =(- u^{2})\cdot (-4)+(- v^{2})\cdot (-3)+(- (4 u + 3 v)^{2})\cdot (1) \\  & =4 u^{2}+3 v^{2}- 16 u^{2} - 24 uv - 9 v^{2} \\  & =- 12 u^{2} - 24 uv - 6 v^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨- x^{2},\,- y^{2},\,- z^{2}⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- 12 u^{2} - 24 uv - 6 v^{2})\,\text{d}A \\  & ={\int }_{0}^{5}{\int }_{-3}^{4}(- 12 u^{2} - 24 uv - 6 v^{2})\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161360 1

Consider the vector field $F(x,y,z)=⟨x^{2},\,y^{2},\,z^{2}⟩$ and the surface $S$ defined by $z=4 x + 4 y$ for $-2\le x\le 2$ and $-1\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{2}{\int }_{-1}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $20 u^{2} + 32 uv + 12 v^{2}$
- $- 4 u^{2} - 4 v^{2}$
- $12 u^{2} + 32 uv + 12 v^{2}$
- $- 12 u^{2} - 32 uv - 12 v^{2}$
- $12 u^{2} + 32 uv + 20 v^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 4 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 2,\,-1\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 4 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 4 v)⟩ \\  & =⟨0,\,1,\,4⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 4\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 4\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 4\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-4,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨x^{2},\,y^{2},\,z^{2}⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 4 v} \\  & =⟨u^{2},\,v^{2},\,(4 u + 4 v)^{2}⟩\end{aligned}
$$

 

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u^{2},\,v^{2},\,(4 u + 4 v)^{2}⟩\cdot ⟨-4,\,-4,\,1⟩ \\  & =(u^{2})\cdot (-4)+(v^{2})\cdot (-4)+((4 u + 4 v)^{2})\cdot (1) \\  & =- 4 u^{2}- 4 v^{2}+16 u^{2} + 32 uv + 16 v^{2} \\  & =12 u^{2} + 32 uv + 12 v^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨x^{2},\,y^{2},\,z^{2}⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(12 u^{2} + 32 uv + 12 v^{2})\,\text{d}A \\  & ={\int }_{-2}^{2}{\int }_{-1}^{2}(12 u^{2} + 32 uv + 12 v^{2})\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161358 0

Consider the vector field $F(x,y,z)=⟨- z,\,y,\,- 2 x⟩$ and the surface $S$ defined by $z=4 x + 3 y$ for $0\le x\le 5$ and $-3\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{5}{\int }_{-3}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $- 14 u - 9 v$
- $14 u + 9 v$
- $16 u + 9 v$
- $- 18 u - 15 v$
- $14 u + 15 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 3 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 5,\,-3\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 3 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 3 v)⟩ \\  & =⟨0,\,1,\,3⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 3\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 3\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 3\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-3,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨- z,\,y,\,- 2 x⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 3 v} \\  & =⟨- (4 u + 3 v),\,v,\,- 2 u⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨- (4 u + 3 v),\,v,\,- 2 u⟩\cdot ⟨-4,\,-3,\,1⟩ \\  & =(- (4 u + 3 v))\cdot (-4)+(v)\cdot (-3)+(- 2 u)\cdot (1) \\  & =16 u + 12 v- 3 v- 2 u \\  & =14 u + 9 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨- z,\,y,\,- 2 x⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(14 u + 9 v)\,\text{d}A \\  & ={\int }_{0}^{5}{\int }_{-3}^{4}(14 u + 9 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161358 1

Consider the vector field $F(x,y,z)=⟨z,\,- y,\,2 x⟩$ and the surface $S$ defined by $z=4 x + 4 y$ for $-2\le x\le 2$ and $-1\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{2}{\int }_{-1}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $18 u + 20 v$
- $- 16 u - 12 v$
- $- 14 u - 12 v$
- $14 u + 12 v$
- $- 14 u - 20 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 4 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 2,\,-1\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 4 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 4 v)⟩ \\  & =⟨0,\,1,\,4⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 4\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 4\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 4\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-4,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨z,\,- y,\,2 x⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 4 v} \\  & =⟨(4 u + 4 v),\,- v,\,2 u⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨(4 u + 4 v),\,- v,\,2 u⟩\cdot ⟨-4,\,-4,\,1⟩ \\  & =((4 u + 4 v))\cdot (-4)+(- v)\cdot (-4)+(2 u)\cdot (1) \\  & =- 16 u - 16 v+4 v+2 u \\  & =- 14 u - 12 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨z,\,- y,\,2 x⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- 14 u - 12 v)\,\text{d}A \\  & ={\int }_{-2}^{2}{\int }_{-1}^{2}(- 14 u - 12 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161441 0

Consider the vector field $F(x,y,z)=⟨- x,\,- y + z,\,- x - y⟩$ and the surface $S$ defined by $z=4 x + 3 y$ for $0\le x\le 5$ and $-3\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{5}{\int }_{-3}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $9 u + 7 v$
- $- 9 u - 7 v$
- $- 8 u - 6 v$
- $- 17 u - 7 v$
- $15 u + 5 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 3 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 5,\,-3\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 3 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 3 v)⟩ \\  & =⟨0,\,1,\,3⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 3\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 3\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 3\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-3,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨- x,\,- y + z,\,- x - y⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 3 v} \\  & =⟨- u,\,- v + (4 u + 3 v),\,- u - v⟩ \\  & =⟨- u,\,4 u + 2 v,\,- u - v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨- u,\,4 u + 2 v,\,- u - v⟩\cdot ⟨-4,\,-3,\,1⟩ \\  & =(- u)\cdot (-4)+(4 u + 2 v)\cdot (-3)+(- u - v)\cdot (1) \\  & =4 u- 12 u - 6 v- u - v \\  & =- 9 u - 7 v.\end{aligned}
$$

 

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨- x,\,- y + z,\,- x - y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- 9 u - 7 v)\,\text{d}A \\  & ={\int }_{0}^{5}{\int }_{-3}^{4}(- 9 u - 7 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161441 1

Consider the vector field $F(x,y,z)=⟨x,\,y - z,\,x + y⟩$ and the surface $S$ defined by $z=4 x + 4 y$ for $-2\le x\le 2$ and $-1\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{2}{\int }_{-1}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $21 u + 13 v$
- $12 u + 12 v$
- $13 u + 13 v$
- $- 13 u - 13 v$
- $- 19 u - 11 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 4 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 2,\,-1\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 4 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 4 v)⟩ \\  & =⟨0,\,1,\,4⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 4\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 4\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 4\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-4,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨x,\,y - z,\,x + y⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 4 v} \\  & =⟨u,\,v - (4 u + 4 v),\,u + v⟩ \\  & =⟨u,\,- 4 u - 3 v,\,u + v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u,\,- 4 u - 3 v,\,u + v⟩\cdot ⟨-4,\,-4,\,1⟩ \\  & =(u)\cdot (-4)+(- 4 u - 3 v)\cdot (-4)+(u + v)\cdot (1) \\  & =- 4 u+16 u + 12 v+u + v \\  & =13 u + 13 v.\end{aligned}
$$

 

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨x,\,y - z,\,x + y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(13 u + 13 v)\,\text{d}A \\  & ={\int }_{-2}^{2}{\int }_{-1}^{2}(13 u + 13 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161462 0

Consider the vector field $F(x,y,z)=⟨- z,\,- y - 2 z,\,- 2 x + y⟩$ and the surface $S$ defined by $z=4 x + 3 y$ for $0\le x\le 5$ and $-3\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{5}{\int }_{-3}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $- 38 u - 34 v$
- $38 u + 34 v$
- $40 u + 33 v$
- $6 u + 10 v$
- $- 10 u - 8 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 3 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 5,\,-3\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 3 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 3 v)⟩ \\  & =⟨0,\,1,\,3⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 3\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 3\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 3\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-3,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨- z,\,- y - 2 z,\,- 2 x + y⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 3 v} \\  & =⟨- (4 u + 3 v),\,- v - 2 (4 u + 3 v),\,- 2 u + v⟩ \\  & =⟨- 4 u - 3 v,\,- 8 u - 7 v,\,- 2 u + v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨- 4 u - 3 v,\,- 8 u - 7 v,\,- 2 u + v⟩\cdot ⟨-4,\,-3,\,1⟩ \\  & =(- 4 u - 3 v)\cdot (-4)+(- 8 u - 7 v)\cdot (-3)+(- 2 u + v)\cdot (1) \\  & =16 u + 12 v+24 u + 21 v- 2 u + v \\  & =38 u + 34 v.\end{aligned}
$$

 

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨- z,\,- y - 2 z,\,- 2 x + y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(38 u + 34 v)\,\text{d}A \\  & ={\int }_{0}^{5}{\int }_{-3}^{4}(38 u + 34 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161462 1

Consider the vector field $F(x,y,z)=⟨z,\,y + 2 z,\,2 x - y⟩$ and the surface $S$ defined by $z=4 x + 4 y$ for $-2\le x\le 2$ and $-1\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{2}{\int }_{-1}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $- 14 u - 21 v$
- $- 48 u - 52 v$
- $- 46 u - 53 v$
- $46 u + 53 v$
- $18 u + 19 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 4 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 2,\,-1\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 4 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 4 v)⟩ \\  & =⟨0,\,1,\,4⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 4\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 4\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 4\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-4,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨z,\,y + 2 z,\,2 x - y⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 4 v} \\  & =⟨(4 u + 4 v),\,v + 2 (4 u + 4 v),\,2 u - v⟩ \\  & =⟨4 u + 4 v,\,8 u + 9 v,\,2 u - v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨4 u + 4 v,\,8 u + 9 v,\,2 u - v⟩\cdot ⟨-4,\,-4,\,1⟩ \\  & =(4 u + 4 v)\cdot (-4)+(8 u + 9 v)\cdot (-4)+(2 u - v)\cdot (1) \\  & =- 16 u - 16 v- 32 u - 36 v+2 u - v \\  & =- 46 u - 53 v.\end{aligned}
$$

 

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨z,\,y + 2 z,\,2 x - y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- 46 u - 53 v)\,\text{d}A \\  & ={\int }_{-2}^{2}{\int }_{-1}^{2}(- 46 u - 53 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161381 0

Consider the vector field $F(x,y,z)=⟨- x - z,\,- y - 2 z,\,- x + 4 y⟩$ and the surface $S$ defined by $z=4 x + 3 y$ for $0\le x\le 5$ and $-3\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{5}{\int }_{-3}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $- 43 u - 37 v$
- $43 u + 37 v$
- $44 u + 33 v$
- $3 u + 13 v$
- $- 5 u - 5 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 3 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 5,\,-3\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 3 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 3 v)⟩ \\  & =⟨0,\,1,\,3⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 3\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 3\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 3\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-3,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨- x - z,\,- y - 2 z,\,- x + 4 y⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 3 v} \\  & =⟨- u - (4 u + 3 v),\,- v - 2 (4 u + 3 v),\,- u + 4 v⟩ \\  & =⟨- 5 u - 3 v,\,- 8 u - 7 v,\,- u + 4 v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨- 5 u - 3 v,\,- 8 u - 7 v,\,- u + 4 v⟩\cdot ⟨-4,\,-3,\,1⟩ \\  & =(- 5 u - 3 v)\cdot (-4)+(- 8 u - 7 v)\cdot (-3)+(- u + 4 v)\cdot (1) \\  & =20 u + 12 v+24 u + 21 v- u + 4 v \\  & =43 u + 37 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨- x - z,\,- y - 2 z,\,- x + 4 y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(43 u + 37 v)\,\text{d}A \\  & ={\int }_{0}^{5}{\int }_{-3}^{4}(43 u + 37 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161381 1

Consider the vector field $F(x,y,z)=⟨x + z,\,y + 2 z,\,x - 4 y⟩$ and the surface $S$ defined by $z=4 x + 4 y$ for $-2\le x\le 2$ and $-1\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{2}{\int }_{-1}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $- 11 u - 24 v$
- $- 52 u - 52 v$
- $- 51 u - 56 v$
- $51 u + 56 v$
- $13 u + 16 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 4 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 2,\,-1\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 4 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 4 v)⟩ \\  & =⟨0,\,1,\,4⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 4\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 4\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 4\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-4,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨x + z,\,y + 2 z,\,x - 4 y⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 4 v} \\  & =⟨u + (4 u + 4 v),\,v + 2 (4 u + 4 v),\,u - 4 v⟩ \\  & =⟨5 u + 4 v,\,8 u + 9 v,\,u - 4 v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨5 u + 4 v,\,8 u + 9 v,\,u - 4 v⟩\cdot ⟨-4,\,-4,\,1⟩ \\  & =(5 u + 4 v)\cdot (-4)+(8 u + 9 v)\cdot (-4)+(u - 4 v)\cdot (1) \\  & =- 20 u - 16 v- 32 u - 36 v+u - 4 v \\  & =- 51 u - 56 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨x + z,\,y + 2 z,\,x - 4 y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- 51 u - 56 v)\,\text{d}A \\  & ={\int }_{-2}^{2}{\int }_{-1}^{2}(- 51 u - 56 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161467 0

Consider the vector field $F(x,y,z)=⟨- 2 x + z,\,- y + z,\,- y - z⟩$ and the surface $S$ defined by $z=4 x + 3 y$ for $0\le x\le 5$ and $-3\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{5}{\int }_{-3}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $24 u + 22 v$
- $- 24 u - 22 v$
- $- 20 u - 18 v$
- $- 8 u + 2 v$
- $- 10 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 3 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 5,\,-3\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 3 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 3 v)⟩ \\  & =⟨0,\,1,\,3⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 3\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 3\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 3\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-3,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨- 2 x + z,\,- y + z,\,- y - z⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 3 v} \\  & =⟨- 2 u + (4 u + 3 v),\,- v + (4 u + 3 v),\,- v - (4 u + 3 v)⟩ \\  & =⟨2 u + 3 v,\,4 u + 2 v,\,- 4 u - 4 v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 u + 3 v,\,4 u + 2 v,\,- 4 u - 4 v⟩\cdot ⟨-4,\,-3,\,1⟩ \\  & =(2 u + 3 v)\cdot (-4)+(4 u + 2 v)\cdot (-3)+(- 4 u - 4 v)\cdot (1) \\  & =- 8 u - 12 v- 12 u - 6 v- 4 u - 4 v \\  & =- 24 u - 22 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨- 2 x + z,\,- y + z,\,- y - z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- 24 u - 22 v)\,\text{d}A \\  & ={\int }_{0}^{5}{\int }_{-3}^{4}(- 24 u - 22 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161467 1

Consider the vector field $F(x,y,z)=⟨2 x - z,\,y - z,\,y + z⟩$ and the surface $S$ defined by $z=4 x + 4 y$ for $-2\le x\le 2$ and $-1\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{2}{\int }_{-1}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $12 u + v$
- $24 u + 28 v$
- $28 u + 33 v$
- $- 28 u - 33 v$
- $- 4 u + 9 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 4 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 2,\,-1\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 4 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 4 v)⟩ \\  & =⟨0,\,1,\,4⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 4\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 4\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 4\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-4,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 x - z,\,y - z,\,y + z⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 4 v} \\  & =⟨2 u - (4 u + 4 v),\,v - (4 u + 4 v),\,v + (4 u + 4 v)⟩ \\  & =⟨- 2 u - 4 v,\,- 4 u - 3 v,\,4 u + 5 v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨- 2 u - 4 v,\,- 4 u - 3 v,\,4 u + 5 v⟩\cdot ⟨-4,\,-4,\,1⟩ \\  & =(- 2 u - 4 v)\cdot (-4)+(- 4 u - 3 v)\cdot (-4)+(4 u + 5 v)\cdot (1) \\  & =8 u + 16 v+16 u + 12 v+4 u + 5 v \\  & =28 u + 33 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 x - z,\,y - z,\,y + z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(28 u + 33 v)\,\text{d}A \\  & ={\int }_{-2}^{2}{\int }_{-1}^{2}(28 u + 33 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161357 0

Consider the vector field $F(x,y,z)=⟨- x - y,\,- 2 x + y,\,- x - z⟩$ and the surface $S$ defined by $z=4 x + 3 y$ for $0\le x\le 5$ and $-3\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{5}{\int }_{-3}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $- 5 u + 2 v$
- $5 u - 2 v$
- $10 u + v$
- $- 3 u - 10 v$
- $- 7 u + 4 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 3 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 5,\,-3\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 3 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 3 v)⟩ \\  & =⟨0,\,1,\,3⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 3\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 3\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 3\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-3,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨- x - y,\,- 2 x + y,\,- x - z⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 3 v} \\  & =⟨- u - v,\,- 2 u + v,\,- u - (4 u + 3 v)⟩ \\  & =⟨- u - v,\,- 2 u + v,\,- 5 u - 3 v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨- u - v,\,- 2 u + v,\,- 5 u - 3 v⟩\cdot ⟨-4,\,-3,\,1⟩ \\  & =(- u - v)\cdot (-4)+(- 2 u + v)\cdot (-3)+(- 5 u - 3 v)\cdot (1) \\  & =4 u + 4 v+6 u - 3 v- 5 u - 3 v \\  & =5 u - 2 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨- x - y,\,- 2 x + y,\,- x - z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(5 u - 2 v)\,\text{d}A \\  & ={\int }_{0}^{5}{\int }_{-3}^{4}(5 u - 2 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161357 1

Consider the vector field $F(x,y,z)=⟨x + y,\,2 x - y,\,x + z⟩$ and the surface $S$ defined by $z=4 x + 4 y$ for $-2\le x\le 2$ and $-1\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{2}{\int }_{-1}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $u + 12 v$
- $- 12 u$
- $- 7 u + 4 v$
- $7 u - 4 v$
- $9 u - 4 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 4 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 2,\,-1\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 4 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 4 v)⟩ \\  & =⟨0,\,1,\,4⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 4\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 4\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 4\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-4,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨x + y,\,2 x - y,\,x + z⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 4 v} \\  & =⟨u + v,\,2 u - v,\,u + (4 u + 4 v)⟩ \\  & =⟨u + v,\,2 u - v,\,5 u + 4 v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u + v,\,2 u - v,\,5 u + 4 v⟩\cdot ⟨-4,\,-4,\,1⟩ \\  & =(u + v)\cdot (-4)+(2 u - v)\cdot (-4)+(5 u + 4 v)\cdot (1) \\  & =- 4 u - 4 v- 8 u + 4 v+5 u + 4 v \\  & =- 7 u + 4 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨x + y,\,2 x - y,\,x + z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- 7 u + 4 v)\,\text{d}A \\  & ={\int }_{-2}^{2}{\int }_{-1}^{2}(- 7 u + 4 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161359 0

Consider the vector field $F(x,y,z)=⟨- y z,\,- x z,\,- xy⟩$ and the surface $S$ defined by $z=4 x + 3 y$ for $0\le x\le 5$ and $-3\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{5}{\int }_{-3}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $- 12 u^{2} - 24 uv - 12 v^{2}$
- $12 u^{2} + 24 uv + 12 v^{2}$
- $12 u^{2} + 25 uv + 12 v^{2}$
- $12 u^{2} - 8 uv - 12 v^{2}$
- $- 12 u^{2} + 6 uv + 12 v^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 3 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 5,\,-3\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 3 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 3 v)⟩ \\  & =⟨0,\,1,\,3⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 3\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 3\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 3\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-3,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨- y z,\,- x z,\,- xy⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 3 v} \\  & =⟨- v (4 u + 3 v),\,- u (4 u + 3 v),\,- uv⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨- v (4 u + 3 v),\,- u (4 u + 3 v),\,- uv⟩\cdot ⟨-4,\,-3,\,1⟩ \\  & =(- v (4 u + 3 v))\cdot (-4)+(- u (4 u + 3 v))\cdot (-3)+(- uv)\cdot (1) \\  & =16 uv + 12 v^{2}+12 u^{2} + 9 uv- uv \\  & =12 u^{2} + 24 uv + 12 v^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨- y z,\,- x z,\,- xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(12 u^{2} + 24 uv + 12 v^{2})\,\text{d}A \\  & ={\int }_{0}^{5}{\int }_{-3}^{4}(12 u^{2} + 24 uv + 12 v^{2})\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161359 1

Consider the vector field $F(x,y,z)=⟨y z,\,x z,\,xy⟩$ and the surface $S$ defined by $z=4 x + 4 y$ for $-2\le x\le 2$ and $-1\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{2}{\int }_{-1}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $- 16 u^{2} + uv + 16 v^{2}$
- $- 16 u^{2} - 32 uv - 16 v^{2}$
- $- 16 u^{2} - 31 uv - 16 v^{2}$
- $16 u^{2} + 31 uv + 16 v^{2}$
- $16 u^{2} + uv - 16 v^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 4 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 2,\,-1\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 4 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 4 v)⟩ \\  & =⟨0,\,1,\,4⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 4\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 4\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 4\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-4,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨y z,\,x z,\,xy⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 4 v} \\  & =⟨v (4 u + 4 v),\,u (4 u + 4 v),\,uv⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨v (4 u + 4 v),\,u (4 u + 4 v),\,uv⟩\cdot ⟨-4,\,-4,\,1⟩ \\  & =(v (4 u + 4 v))\cdot (-4)+(u (4 u + 4 v))\cdot (-4)+(uv)\cdot (1) \\  & =- 16 uv - 16 v^{2}- 16 u^{2} - 16 uv+uv \\  & =- 16 u^{2} - 31 uv - 16 v^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨y z,\,x z,\,xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- 16 u^{2} - 31 uv - 16 v^{2})\,\text{d}A \\  & ={\int }_{-2}^{2}{\int }_{-1}^{2}(- 16 u^{2} - 31 uv - 16 v^{2})\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161377 0

Consider the vector field $F(x,y,z)=⟨- x^{2} + y^{2},\,- y^{2} + z^{2},\,- z^{2}⟩$ and the surface $S$ defined by $z=4 x + 3 y$ for $0\le x\le 5$ and $-3\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{5}{\int }_{-3}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $60 u^{2} + 96 uv + 37 v^{2}$
- $- 60 u^{2} - 96 uv - 37 v^{2}$
- $- 44 u^{2} - 72 uv - 28 v^{2}$
- $- 68 u^{2} - 96 uv - 29 v^{2}$
- $36 u^{2} + 48 uv + 11 v^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 3 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 5,\,-3\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 3 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 3 v)⟩ \\  & =⟨0,\,1,\,3⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 3\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 3\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 3\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-3,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨- x^{2} + y^{2},\,- y^{2} + z^{2},\,- z^{2}⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 3 v} \\  & =⟨- u^{2} + v^{2},\,- v^{2} + (4 u + 3 v)^{2},\,- (4 u + 3 v)^{2}⟩\end{aligned}
$$

 

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨- u^{2} + v^{2},\,- v^{2} + (4 u + 3 v)^{2},\,- (4 u + 3 v)^{2}⟩\cdot ⟨-4,\,-3,\,1⟩ \\  & =(- u^{2} + v^{2})\cdot (-4)+(- v^{2} + (4 u + 3 v)^{2})\cdot (-3)+(- (4 u + 3 v)^{2})\cdot (1) \\  & =4 u^{2} - 4 v^{2}+3 v^{2} - 3 \left(4 u + 3 v\right)^{2}- \left(4 u + 3 v\right)^{2} \\  & =- 60 u^{2} - 96 uv - 37 v^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨- x^{2} + y^{2},\,- y^{2} + z^{2},\,- z^{2}⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- 60 u^{2} - 96 uv - 37 v^{2})\,\text{d}A \\  & ={\int }_{0}^{5}{\int }_{-3}^{4}(- 60 u^{2} - 96 uv - 37 v^{2})\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161377 1

Consider the vector field $F(x,y,z)=⟨x^{2} - y^{2},\,y^{2} - z^{2},\,z^{2}⟩$ and the surface $S$ defined by $z=4 x + 4 y$ for $-2\le x\le 2$ and $-1\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{2}{\int }_{-1}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $84 u^{2} + 160 uv + 72 v^{2}$
- $60 u^{2} + 128 uv + 64 v^{2}$
- $76 u^{2} + 160 uv + 80 v^{2}$
- $- 76 u^{2} - 160 uv - 80 v^{2}$
- $- 52 u^{2} - 96 uv - 40 v^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 4 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 2,\,-1\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 4 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 4 v)⟩ \\  & =⟨0,\,1,\,4⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 4\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 4\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 4\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-4,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨x^{2} - y^{2},\,y^{2} - z^{2},\,z^{2}⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 4 v} \\  & =⟨u^{2} - v^{2},\,v^{2} - (4 u + 4 v)^{2},\,(4 u + 4 v)^{2}⟩\end{aligned}
$$

 

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨u^{2} - v^{2},\,v^{2} - (4 u + 4 v)^{2},\,(4 u + 4 v)^{2}⟩\cdot ⟨-4,\,-4,\,1⟩ \\  & =(u^{2} - v^{2})\cdot (-4)+(v^{2} - (4 u + 4 v)^{2})\cdot (-4)+((4 u + 4 v)^{2})\cdot (1) \\  & =- 4 u^{2} + 4 v^{2}- 4 v^{2} + 4 \left(4 u + 4 v\right)^{2}+\left(4 u + 4 v\right)^{2} \\  & =76 u^{2} + 160 uv + 80 v^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨x^{2} - y^{2},\,y^{2} - z^{2},\,z^{2}⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(76 u^{2} + 160 uv + 80 v^{2})\,\text{d}A \\  & ={\int }_{-2}^{2}{\int }_{-1}^{2}(76 u^{2} + 160 uv + 80 v^{2})\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161379 0

Consider the vector field $F(x,y,z)=⟨- \left(x + y\right)^{2},\,- \left(x - y\right)^{2},\,- xy⟩$ and the surface $S$ defined by $z=4 x + 3 y$ for $0\le x\le 5$ and $-3\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{5}{\int }_{-3}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $- 7 u^{2} - uv - 7 v^{2}$
- $7 u^{2} + uv + 7 v^{2}$
- $7 u^{2} + 2 uv + 7 v^{2}$
- $- u^{2} - 15 uv - v^{2}$
- $u^{2} + 13 uv + v^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 3 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 5,\,-3\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 3 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 3 v)⟩ \\  & =⟨0,\,1,\,3⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 3\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 3\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 3\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-3,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨- \left(x + y\right)^{2},\,- \left(x - y\right)^{2},\,- xy⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 3 v} \\  & =⟨- \left(u + v\right)^{2},\,- \left(u - v\right)^{2},\,- uv⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨- \left(u + v\right)^{2},\,- \left(u - v\right)^{2},\,- uv⟩\cdot ⟨-4,\,-3,\,1⟩ \\  & =(- \left(u + v\right)^{2})\cdot (-4)+(- \left(u - v\right)^{2})\cdot (-3)+(- uv)\cdot (1) \\  & =7 u^{2} + uv + 7 v^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨- \left(x + y\right)^{2},\,- \left(x - y\right)^{2},\,- xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(7 u^{2} + uv + 7 v^{2})\,\text{d}A \\  & ={\int }_{0}^{5}{\int }_{-3}^{4}(7 u^{2} + uv + 7 v^{2})\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161379 1

Consider the vector field $F(x,y,z)=⟨\left(x + y\right)^{2},\,\left(x - y\right)^{2},\,xy⟩$ and the surface $S$ defined by $z=4 x + 4 y$ for $-2\le x\le 2$ and $-1\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{2}{\int }_{-1}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $17 uv$
- $- 8 u^{2} - 8 v^{2}$
- $- 8 u^{2} + uv - 8 v^{2}$
- $8 u^{2} - uv + 8 v^{2}$
- $- 15 uv$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 4 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 2,\,-1\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 4 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 4 v)⟩ \\  & =⟨0,\,1,\,4⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 4\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 4\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 4\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-4,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨\left(x + y\right)^{2},\,\left(x - y\right)^{2},\,xy⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 4 v} \\  & =⟨\left(u + v\right)^{2},\,\left(u - v\right)^{2},\,uv⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨\left(u + v\right)^{2},\,\left(u - v\right)^{2},\,uv⟩\cdot ⟨-4,\,-4,\,1⟩ \\  & =(\left(u + v\right)^{2})\cdot (-4)+(\left(u - v\right)^{2})\cdot (-4)+(uv)\cdot (1) \\  & =- 8 u^{2} + uv - 8 v^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨\left(x + y\right)^{2},\,\left(x - y\right)^{2},\,xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- 8 u^{2} + uv - 8 v^{2})\,\text{d}A \\  & ={\int }_{-2}^{2}{\int }_{-1}^{2}(- 8 u^{2} + uv - 8 v^{2})\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161471 0

Consider the vector field $F(x,y,z)=⟨- x - z,\,- 2 z,\,- y - z⟩$ and the surface $S$ defined by $z=4 x + 3 y$ for $0\le x\le 5$ and $-3\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{5}{\int }_{-3}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $- 40 u - 26 v$
- $40 u + 26 v$
- $44 u + 30 v$
- $2 v$
- $- 8 u - 10 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 3 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 5,\,-3\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 3 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 3 v)⟩ \\  & =⟨0,\,1,\,3⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 3\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 3\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 3\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-3,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨- x - z,\,- 2 z,\,- y - z⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 3 v} \\  & =⟨- u - (4 u + 3 v),\,- 2 (4 u + 3 v),\,- v - (4 u + 3 v)⟩ \\  & =⟨- 5 u - 3 v,\,- 8 u - 6 v,\,- 4 u - 4 v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨- 5 u - 3 v,\,- 8 u - 6 v,\,- 4 u - 4 v⟩\cdot ⟨-4,\,-3,\,1⟩ \\  & =(- 5 u - 3 v)\cdot (-4)+(- 8 u - 6 v)\cdot (-3)+(- 4 u - 4 v)\cdot (1) \\  & =20 u + 12 v+24 u + 18 v- 4 u - 4 v \\  & =40 u + 26 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨- x - z,\,- 2 z,\,- y - z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(40 u + 26 v)\,\text{d}A \\  & ={\int }_{0}^{5}{\int }_{-3}^{4}(40 u + 26 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated easy q-161471 1

Consider the vector field $F(x,y,z)=⟨x + z,\,2 z,\,y + z⟩$ and the surface $S$ defined by $z=4 x + 4 y$ for $-2\le x\le 2$ and $-1\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{2}{\int }_{-1}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $- 8 u - 11 v$
- $- 52 u - 48 v$
- $- 48 u - 43 v$
- $48 u + 43 v$
- $16 u + 21 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u + 4 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 2,\,-1\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u + 4 v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u + 4 v)⟩ \\  & =⟨0,\,1,\,4⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & 4\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & 4\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & 4\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,-4,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨x + z,\,2 z,\,y + z⟩{|}_{x=u,\,\,y=v,\,\,z=4 u + 4 v} \\  & =⟨u + (4 u + 4 v),\,2 (4 u + 4 v),\,v + (4 u + 4 v)⟩ \\  & =⟨5 u + 4 v,\,8 u + 8 v,\,4 u + 5 v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨5 u + 4 v,\,8 u + 8 v,\,4 u + 5 v⟩\cdot ⟨-4,\,-4,\,1⟩ \\  & =(5 u + 4 v)\cdot (-4)+(8 u + 8 v)\cdot (-4)+(4 u + 5 v)\cdot (1) \\  & =- 20 u - 16 v- 32 u - 32 v+4 u + 5 v \\  & =- 48 u - 43 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨x + z,\,2 z,\,y + z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- 48 u - 43 v)\,\text{d}A \\  & ={\int }_{-2}^{2}{\int }_{-1}^{2}(- 48 u - 43 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated moderate quadratic_graph 0

Consider the vector field $F(x,y,z)=⟨2 x + 2 y,\,x + 3 y,\,- z - 1⟩$ and the surface $S$ defined by $z=2 x^{2} + 2 y^{2}$ for $0\le x\le 5$ and $-3\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{5}{\int }_{-3}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $- 8 u^{2} - 12 uv - 12 v^{2}$
- $- 10 u^{2} - 4 uv + 10 v^{2} - 1$
- $- 10 u^{2} - 12 uv - 14 v^{2} - 1$
- $10 u^{2} + 12 uv + 14 v^{2} + 1$
- $6 u^{2} + 4 uv - 14 v^{2} - 1$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,2 u^{2} + 2 v^{2}⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 5,\,-3\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(2 u^{2} + 2 v^{2})⟩ \\  & =⟨1,\,0,\,4 u⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(2 u^{2} + 2 v^{2})⟩ \\  & =⟨0,\,1,\,4 v⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 u \\ 0 & 1 & 4 v\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 u \\ 1 & 4 v\end{aligned}|,\,-|\begin{aligned}1 & 4 u \\ 0 & 4 v\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨- 4 u,\,- 4 v,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 x + 2 y,\,x + 3 y,\,- z - 1⟩{|}_{x=u,\,\,y=v,\,\,z=2 u^{2} + 2 v^{2}} \\  & =⟨2 u + 2 v,\,u + 3 v,\,- (2 u^{2} + 2 v^{2}) - 1⟩ \\  & =⟨2 u + 2 v,\,u + 3 v,\,- 2 u^{2} - 2 v^{2} - 1⟩\end{aligned}
$$

 

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 u + 2 v,\,u + 3 v,\,- 2 u^{2} - 2 v^{2} - 1⟩\cdot ⟨- 4 u,\,- 4 v,\,1⟩ \\  & =(2 u + 2 v)\cdot (- 4 u)+(u + 3 v)\cdot (- 4 v)+(- 2 u^{2} - 2 v^{2} - 1)\cdot (1) \\  & =- 8 u^{2} - 8 uv- 4 uv - 12 v^{2}- 2 u^{2} - 2 v^{2} - 1 \\  & =- 10 u^{2} - 12 uv - 14 v^{2} - 1.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 x + 2 y,\,x + 3 y,\,- z - 1⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- 10 u^{2} - 12 uv - 14 v^{2} - 1)\,\text{d}A \\  & ={\int }_{0}^{5}{\int }_{-3}^{4}(- 10 u^{2} - 12 uv - 14 v^{2} - 1)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated moderate quadratic_graph 1

Consider the vector field $F(x,y,z)=⟨2 x + 2 y,\,- x + y,\,2 z - 2⟩$ and the surface $S$ defined by $z=2 x^{2} + 2 y^{2}$ for $-2\le x\le 2$ and $-1\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{2}{\int }_{-1}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $4 u^{2} + 4 uv + 2$
- $- 4 u^{2} - 4 uv - 2$
- $12 u^{2} + 12 uv - 2$
- $- 8 u^{2} - 4 uv - 4 v^{2}$
- $- 4 u^{2} - 12 uv + 8 v^{2} - 2$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,2 u^{2} + 2 v^{2}⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 2,\,-1\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(2 u^{2} + 2 v^{2})⟩ \\  & =⟨1,\,0,\,4 u⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(2 u^{2} + 2 v^{2})⟩ \\  & =⟨0,\,1,\,4 v⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 u \\ 0 & 1 & 4 v\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 u \\ 1 & 4 v\end{aligned}|,\,-|\begin{aligned}1 & 4 u \\ 0 & 4 v\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨- 4 u,\,- 4 v,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 x + 2 y,\,- x + y,\,2 z - 2⟩{|}_{x=u,\,\,y=v,\,\,z=2 u^{2} + 2 v^{2}} \\  & =⟨2 u + 2 v,\,- u + v,\,2 (2 u^{2} + 2 v^{2}) - 2⟩ \\  & =⟨2 u + 2 v,\,- u + v,\,4 u^{2} + 4 v^{2} - 2⟩\end{aligned}
$$

 

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 u + 2 v,\,- u + v,\,4 u^{2} + 4 v^{2} - 2⟩\cdot ⟨- 4 u,\,- 4 v,\,1⟩ \\  & =(2 u + 2 v)\cdot (- 4 u)+(- u + v)\cdot (- 4 v)+(4 u^{2} + 4 v^{2} - 2)\cdot (1) \\  & =- 8 u^{2} - 8 uv+4 uv - 4 v^{2}+4 u^{2} + 4 v^{2} - 2 \\  & =- 4 u^{2} - 4 uv - 2.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 x + 2 y,\,- x + y,\,2 z - 2⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- 4 u^{2} - 4 uv - 2)\,\text{d}A \\  & ={\int }_{-2}^{2}{\int }_{-1}^{2}(- 4 u^{2} - 4 uv - 2)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated hard mixed_graph 0

Consider the vector field $F(x,y,z)=⟨2 z,\,2 xy,\,x + y⟩$ and the surface $S$ defined by $z=2 xy + x + y$ for $0\le x\le 5$ and $-3\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{0}^{5}{\int }_{-3}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $- 4 u^{2} v + 8 uv^{2} + 6 uv + 3 u + 4 v^{2} + 3 v$
- $- 4 u^{2} v - 8 uv^{2} - 10 uv - u - 4 v^{2} - v$
- $4 u^{2} v - 8 uv^{2} - 6 uv - u - 4 v^{2} - v$
- $4 u^{2} v + 8 uv^{2} + 10 uv + u + 4 v^{2} + v$
- $- 4 u^{2} v - 8 uv^{2} - 10 uv - 2 u - 4 v^{2} - 2 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,2 uv + u + v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,0\le u\le 5,\,-3\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(2 uv + u + v)⟩ \\  & =⟨1,\,0,\,2 v + 1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(2 uv + u + v)⟩ \\  & =⟨0,\,1,\,2 u + 1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 2 v + 1 \\ 0 & 1 & 2 u + 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 2 v + 1 \\ 1 & 2 u + 1\end{aligned}|,\,-|\begin{aligned}1 & 2 v + 1 \\ 0 & 2 u + 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨- 2 v - 1,\,- 2 u - 1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 z,\,2 xy,\,x + y⟩{|}_{x=u,\,\,y=v,\,\,z=2 uv + u + v} \\  & =⟨2 (2 uv + u + v),\,2 uv,\,u + v⟩ \\  & =⟨4 uv + 2 u + 2 v,\,2 uv,\,u + v⟩\end{aligned}
$$

 

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨4 uv + 2 u + 2 v,\,2 uv,\,u + v⟩\cdot ⟨- 2 v - 1,\,- 2 u - 1,\,1⟩ \\  & =(4 uv + 2 u + 2 v)\cdot (- 2 v - 1)+(2 uv)\cdot (- 2 u - 1)+(u + v)\cdot (1) \\  & =- 8 uv^{2} - 8 uv - 2 u - 4 v^{2} - 2 v- 4 u^{2} v - 2 uv+u + v \\  & =- 4 u^{2} v - 8 uv^{2} - 10 uv - u - 4 v^{2} - v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 z,\,2 xy,\,x + y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- 4 u^{2} v - 8 uv^{2} - 10 uv - u - 4 v^{2} - v)\,\text{d}A \\  & ={\int }_{0}^{5}{\int }_{-3}^{4}(- 4 u^{2} v - 8 uv^{2} - 10 uv - u - 4 v^{2} - v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated hard mixed_graph 1

Consider the vector field $F(x,y,z)=⟨2 z,\,xy,\,x + y⟩$ and the surface $S$ defined by $z=2 xy + x + y$ for $-2\le x\le 2$ and $-1\le y\le 2.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{2}{\int }_{-1}^{2}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $- 2 u^{2} v - 8 uv^{2} - 9 uv - 2 u - 4 v^{2} - 2 v$
- $- 2 u^{2} v + 8 uv^{2} + 7 uv + 3 u + 4 v^{2} + 3 v$
- $2 u^{2} v + 8 uv^{2} + 9 uv + u + 4 v^{2} + v$
- $- 2 u^{2} v - 8 uv^{2} - 9 uv - u - 4 v^{2} - v$
- $2 u^{2} v - 8 uv^{2} - 7 uv - u - 4 v^{2} - v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,2 uv + u + v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 2,\,-1\le v\le 2\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(2 uv + u + v)⟩ \\  & =⟨1,\,0,\,2 v + 1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(2 uv + u + v)⟩ \\  & =⟨0,\,1,\,2 u + 1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 2 v + 1 \\ 0 & 1 & 2 u + 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 2 v + 1 \\ 1 & 2 u + 1\end{aligned}|,\,-|\begin{aligned}1 & 2 v + 1 \\ 0 & 2 u + 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨- 2 v - 1,\,- 2 u - 1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 z,\,xy,\,x + y⟩{|}_{x=u,\,\,y=v,\,\,z=2 uv + u + v} \\  & =⟨2 (2 uv + u + v),\,uv,\,u + v⟩ \\  & =⟨4 uv + 2 u + 2 v,\,uv,\,u + v⟩\end{aligned}
$$

 

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨4 uv + 2 u + 2 v,\,uv,\,u + v⟩\cdot ⟨- 2 v - 1,\,- 2 u - 1,\,1⟩ \\  & =(4 uv + 2 u + 2 v)\cdot (- 2 v - 1)+(uv)\cdot (- 2 u - 1)+(u + v)\cdot (1) \\  & =- 8 uv^{2} - 8 uv - 2 u - 4 v^{2} - 2 v- 2 u^{2} v - uv+u + v \\  & =- 2 u^{2} v - 8 uv^{2} - 9 uv - u - 4 v^{2} - v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 z,\,xy,\,x + y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- 2 u^{2} v - 8 uv^{2} - 9 uv - u - 4 v^{2} - v)\,\text{d}A \\  & ={\int }_{-2}^{2}{\int }_{-1}^{2}(- 2 u^{2} v - 8 uv^{2} - 9 uv - u - 4 v^{2} - v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-160887 101

Consider the vector field $F(x,y,z)=⟨- 2 y + 2 z,\,4 y - 2 z,\,2 xy⟩$ and the surface $S$ defined by $z=x + y$ for $1\le x\le 3$ and $1\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{1}^{3}{\int }_{1}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $4 u^{2} v - 2 uv + 2 v^{2}$
- $2 u + 2 v$
- $2 u^{2} + 2 uv + 2 v^{2}$
- $2 uv - 2 v$
- $2 uv + 2 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u + v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,1\le u\le 3,\,1\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u + v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u + v)⟩ \\  & =⟨0,\,1,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & 1\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,-1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨- 2 y + 2 z,\,4 y - 2 z,\,2 xy⟩{|}_{x=u,\,\,y=v,\,\,z=u + v} \\  & =⟨- 2 v + 2 (u + v),\,4 v - 2 (u + v),\,2 uv⟩ \\  & =⟨2 u,\,- 2 u + 2 v,\,2 uv⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 u,\,- 2 u + 2 v,\,2 uv⟩\cdot ⟨-1,\,-1,\,1⟩ \\  & =(2 u)\cdot (-1)+(- 2 u + 2 v)\cdot (-1)+(2 uv)\cdot (1) \\  & =- 2 u+2 u - 2 v+2 uv \\  & =2 uv - 2 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨- 2 y + 2 z,\,4 y - 2 z,\,2 xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(2 uv - 2 v)\,\text{d}A \\  & ={\int }_{1}^{3}{\int }_{1}^{4}(2 uv - 2 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-160887 102

Consider the vector field $F(x,y,z)=⟨- 2 y + 2 z,\,4 y - 2 z,\,2 xy⟩$ and the surface $S$ defined by $z=x + y$ for $-2\le x\le 4$ and $-2\le y\le 3.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{4}{\int }_{-2}^{3}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $2 uv - 2 v$
- $2 uv + 2 v$
- $2 u + 2 v$
- $4 u^{2} v - 2 uv + 2 v^{2}$
- $2 u^{2} + 2 uv + 2 v^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u + v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 4,\,-2\le v\le 3\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u + v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u + v)⟩ \\  & =⟨0,\,1,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & 1\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,-1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨- 2 y + 2 z,\,4 y - 2 z,\,2 xy⟩{|}_{x=u,\,\,y=v,\,\,z=u + v} \\  & =⟨- 2 v + 2 (u + v),\,4 v - 2 (u + v),\,2 uv⟩ \\  & =⟨2 u,\,- 2 u + 2 v,\,2 uv⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 u,\,- 2 u + 2 v,\,2 uv⟩\cdot ⟨-1,\,-1,\,1⟩ \\  & =(2 u)\cdot (-1)+(- 2 u + 2 v)\cdot (-1)+(2 uv)\cdot (1) \\  & =- 2 u+2 u - 2 v+2 uv \\  & =2 uv - 2 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨- 2 y + 2 z,\,4 y - 2 z,\,2 xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(2 uv - 2 v)\,\text{d}A \\  & ={\int }_{-2}^{4}{\int }_{-2}^{3}(2 uv - 2 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161360 101

Consider the vector field $F(x,y,z)=⟨2 x^{2},\,2 y^{2},\,2 z^{2}⟩$ and the surface $S$ defined by $z=x + y$ for $1\le x\le 3$ and $1\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{1}^{3}{\int }_{1}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $2 u^{2} - 2 v^{2}$
- $4 u^{2} + 8 uv + 4 v^{2}$
- $4 uv$
- $2 u^{2} + 2 uv + 2 v^{2}$
- $2 u^{2} + 2 v^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u + v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,1\le u\le 3,\,1\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u + v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u + v)⟩ \\  & =⟨0,\,1,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & 1\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,-1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 x^{2},\,2 y^{2},\,2 z^{2}⟩{|}_{x=u,\,\,y=v,\,\,z=u + v} \\  & =⟨2 u^{2},\,2 v^{2},\,2 (u + v)^{2}⟩\end{aligned}
$$

 

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 u^{2},\,2 v^{2},\,2 (u + v)^{2}⟩\cdot ⟨-1,\,-1,\,1⟩ \\  & =(2 u^{2})\cdot (-1)+(2 v^{2})\cdot (-1)+(2 (u + v)^{2})\cdot (1) \\  & =- 2 u^{2}- 2 v^{2}+2 u^{2} + 4 uv + 2 v^{2} \\  & =4 uv.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 x^{2},\,2 y^{2},\,2 z^{2}⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(4 uv)\,\text{d}A \\  & ={\int }_{1}^{3}{\int }_{1}^{4}(4 uv)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161360 102

Consider the vector field $F(x,y,z)=⟨2 x^{2},\,2 y^{2},\,2 z^{2}⟩$ and the surface $S$ defined by $z=x + y$ for $-2\le x\le 4$ and $-2\le y\le 3.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{4}{\int }_{-2}^{3}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $2 u^{2} + 2 uv + 2 v^{2}$
- $2 u^{2} + 2 v^{2}$
- $4 u^{2} + 8 uv + 4 v^{2}$
- $2 u^{2} - 2 v^{2}$
- $4 uv$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u + v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 4,\,-2\le v\le 3\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u + v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u + v)⟩ \\  & =⟨0,\,1,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & 1\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,-1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 x^{2},\,2 y^{2},\,2 z^{2}⟩{|}_{x=u,\,\,y=v,\,\,z=u + v} \\  & =⟨2 u^{2},\,2 v^{2},\,2 (u + v)^{2}⟩\end{aligned}
$$

 

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 u^{2},\,2 v^{2},\,2 (u + v)^{2}⟩\cdot ⟨-1,\,-1,\,1⟩ \\  & =(2 u^{2})\cdot (-1)+(2 v^{2})\cdot (-1)+(2 (u + v)^{2})\cdot (1) \\  & =- 2 u^{2}- 2 v^{2}+2 u^{2} + 4 uv + 2 v^{2} \\  & =4 uv.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 x^{2},\,2 y^{2},\,2 z^{2}⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(4 uv)\,\text{d}A \\  & ={\int }_{-2}^{4}{\int }_{-2}^{3}(4 uv)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161358 101

Consider the vector field $F(x,y,z)=⟨2 z,\,- 2 y,\,4 x⟩$ and the surface $S$ defined by $z=3 x - 2 y$ for $1\le x\le 3$ and $1\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{1}^{3}{\int }_{1}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $16 u - 14 v$
- $- 14 u - 16 v$
- $14 u + 16 v$
- $8 u + 14 v$
- $- 14 u + 8 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,3 u - 2 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,1\le u\le 3,\,1\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(3 u - 2 v)⟩ \\  & =⟨1,\,0,\,3⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(3 u - 2 v)⟩ \\  & =⟨0,\,1,\,-2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 3 \\ 0 & 1 & -2\end{aligned}| \\  & =⟨|\begin{aligned}0 & 3 \\ 1 & -2\end{aligned}|,\,-|\begin{aligned}1 & 3 \\ 0 & -2\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-3,\,2,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 z,\,- 2 y,\,4 x⟩{|}_{x=u,\,\,y=v,\,\,z=3 u - 2 v} \\  & =⟨2 (3 u - 2 v),\,- 2 v,\,4 u⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 (3 u - 2 v),\,- 2 v,\,4 u⟩\cdot ⟨-3,\,2,\,1⟩ \\  & =(2 (3 u - 2 v))\cdot (-3)+(- 2 v)\cdot (2)+(4 u)\cdot (1) \\  & =- 18 u + 12 v- 4 v+4 u \\  & =- 14 u + 8 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 z,\,- 2 y,\,4 x⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- 14 u + 8 v)\,\text{d}A \\  & ={\int }_{1}^{3}{\int }_{1}^{4}(- 14 u + 8 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161358 102

Consider the vector field $F(x,y,z)=⟨2 z,\,- 2 y,\,4 x⟩$ and the surface $S$ defined by $z=3 x - 2 y$ for $-2\le x\le 4$ and $-2\le y\le 3.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{4}{\int }_{-2}^{3}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $8 u + 14 v$
- $- 14 u + 8 v$
- $- 14 u - 16 v$
- $16 u - 14 v$
- $14 u + 16 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,3 u - 2 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 4,\,-2\le v\le 3\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(3 u - 2 v)⟩ \\  & =⟨1,\,0,\,3⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(3 u - 2 v)⟩ \\  & =⟨0,\,1,\,-2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 3 \\ 0 & 1 & -2\end{aligned}| \\  & =⟨|\begin{aligned}0 & 3 \\ 1 & -2\end{aligned}|,\,-|\begin{aligned}1 & 3 \\ 0 & -2\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-3,\,2,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 z,\,- 2 y,\,4 x⟩{|}_{x=u,\,\,y=v,\,\,z=3 u - 2 v} \\  & =⟨2 (3 u - 2 v),\,- 2 v,\,4 u⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 (3 u - 2 v),\,- 2 v,\,4 u⟩\cdot ⟨-3,\,2,\,1⟩ \\  & =(2 (3 u - 2 v))\cdot (-3)+(- 2 v)\cdot (2)+(4 u)\cdot (1) \\  & =- 18 u + 12 v- 4 v+4 u \\  & =- 14 u + 8 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 z,\,- 2 y,\,4 x⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- 14 u + 8 v)\,\text{d}A \\  & ={\int }_{-2}^{4}{\int }_{-2}^{3}(- 14 u + 8 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161441 101

Consider the vector field $F(x,y,z)=⟨2 x,\,2 y - 2 z,\,2 x + 2 y⟩$ and the surface $S$ defined by $z=x - 2 y$ for $1\le x\le 3$ and $1\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{1}^{3}{\int }_{1}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $- 4 u + 2 v$
- $4 u + 8 v$
- $- 2 u + 8 v$
- $8 u + 2 v$
- $- 4 u + 14 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u - 2 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,1\le u\le 3,\,1\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u - 2 v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u - 2 v)⟩ \\  & =⟨0,\,1,\,-2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & -2\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & -2\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & -2\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,2,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 x,\,2 y - 2 z,\,2 x + 2 y⟩{|}_{x=u,\,\,y=v,\,\,z=u - 2 v} \\  & =⟨2 u,\,2 v - 2 (u - 2 v),\,2 u + 2 v⟩ \\  & =⟨2 u,\,- 2 u + 6 v,\,2 u + 2 v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 u,\,- 2 u + 6 v,\,2 u + 2 v⟩\cdot ⟨-1,\,2,\,1⟩ \\  & =(2 u)\cdot (-1)+(- 2 u + 6 v)\cdot (2)+(2 u + 2 v)\cdot (1) \\  & =- 2 u- 4 u + 12 v+2 u + 2 v \\  & =- 4 u + 14 v.\end{aligned}
$$

 

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 x,\,2 y - 2 z,\,2 x + 2 y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- 4 u + 14 v)\,\text{d}A \\  & ={\int }_{1}^{3}{\int }_{1}^{4}(- 4 u + 14 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161441 102

Consider the vector field $F(x,y,z)=⟨2 x,\,2 y - 2 z,\,2 x + 2 y⟩$ and the surface $S$ defined by $z=x - 2 y$ for $-2\le x\le 4$ and $-2\le y\le 3.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{4}{\int }_{-2}^{3}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $8 u + 2 v$
- $- 4 u + 14 v$
- $4 u + 8 v$
- $- 4 u + 2 v$
- $- 2 u + 8 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u - 2 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 4,\,-2\le v\le 3\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u - 2 v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u - 2 v)⟩ \\  & =⟨0,\,1,\,-2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & -2\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & -2\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & -2\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,2,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 x,\,2 y - 2 z,\,2 x + 2 y⟩{|}_{x=u,\,\,y=v,\,\,z=u - 2 v} \\  & =⟨2 u,\,2 v - 2 (u - 2 v),\,2 u + 2 v⟩ \\  & =⟨2 u,\,- 2 u + 6 v,\,2 u + 2 v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 u,\,- 2 u + 6 v,\,2 u + 2 v⟩\cdot ⟨-1,\,2,\,1⟩ \\  & =(2 u)\cdot (-1)+(- 2 u + 6 v)\cdot (2)+(2 u + 2 v)\cdot (1) \\  & =- 2 u- 4 u + 12 v+2 u + 2 v \\  & =- 4 u + 14 v.\end{aligned}
$$

 

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 x,\,2 y - 2 z,\,2 x + 2 y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(- 4 u + 14 v)\,\text{d}A \\  & ={\int }_{-2}^{4}{\int }_{-2}^{3}(- 4 u + 14 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161462 101

Consider the vector field $F(x,y,z)=⟨2 z,\,2 y + 4 z,\,4 x - 2 y⟩$ and the surface $S$ defined by $z=- x + y$ for $1\le x\le 3$ and $1\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{1}^{3}{\int }_{1}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $4 u - 6 v$
- $2 u + 6 v$
- $2 u + 4 v$
- $4 u + 2 v$
- $6 u - 6 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,- u + v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,1\le u\le 3,\,1\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(- u + v)⟩ \\  & =⟨1,\,0,\,-1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(- u + v)⟩ \\  & =⟨0,\,1,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -1 \\ 0 & 1 & 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & -1 \\ 1 & 1\end{aligned}|,\,-|\begin{aligned}1 & -1 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨1,\,-1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 z,\,2 y + 4 z,\,4 x - 2 y⟩{|}_{x=u,\,\,y=v,\,\,z=- u + v} \\  & =⟨2 (- u + v),\,2 v + 4 (- u + v),\,4 u - 2 v⟩ \\  & =⟨- 2 u + 2 v,\,- 4 u + 6 v,\,4 u - 2 v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨- 2 u + 2 v,\,- 4 u + 6 v,\,4 u - 2 v⟩\cdot ⟨1,\,-1,\,1⟩ \\  & =(- 2 u + 2 v)\cdot (1)+(- 4 u + 6 v)\cdot (-1)+(4 u - 2 v)\cdot (1) \\  & =- 2 u + 2 v+4 u - 6 v+4 u - 2 v \\  & =6 u - 6 v.\end{aligned}
$$

 

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 z,\,2 y + 4 z,\,4 x - 2 y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(6 u - 6 v)\,\text{d}A \\  & ={\int }_{1}^{3}{\int }_{1}^{4}(6 u - 6 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161462 102

Consider the vector field $F(x,y,z)=⟨2 z,\,2 y + 4 z,\,4 x - 2 y⟩$ and the surface $S$ defined by $z=- x + y$ for $-2\le x\le 4$ and $-2\le y\le 3.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{4}{\int }_{-2}^{3}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $4 u + 2 v$
- $6 u - 6 v$
- $2 u + 6 v$
- $4 u - 6 v$
- $2 u + 4 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,- u + v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 4,\,-2\le v\le 3\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(- u + v)⟩ \\  & =⟨1,\,0,\,-1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(- u + v)⟩ \\  & =⟨0,\,1,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -1 \\ 0 & 1 & 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & -1 \\ 1 & 1\end{aligned}|,\,-|\begin{aligned}1 & -1 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨1,\,-1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 z,\,2 y + 4 z,\,4 x - 2 y⟩{|}_{x=u,\,\,y=v,\,\,z=- u + v} \\  & =⟨2 (- u + v),\,2 v + 4 (- u + v),\,4 u - 2 v⟩ \\  & =⟨- 2 u + 2 v,\,- 4 u + 6 v,\,4 u - 2 v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨- 2 u + 2 v,\,- 4 u + 6 v,\,4 u - 2 v⟩\cdot ⟨1,\,-1,\,1⟩ \\  & =(- 2 u + 2 v)\cdot (1)+(- 4 u + 6 v)\cdot (-1)+(4 u - 2 v)\cdot (1) \\  & =- 2 u + 2 v+4 u - 6 v+4 u - 2 v \\  & =6 u - 6 v.\end{aligned}
$$

 

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 z,\,2 y + 4 z,\,4 x - 2 y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(6 u - 6 v)\,\text{d}A \\  & ={\int }_{-2}^{4}{\int }_{-2}^{3}(6 u - 6 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161381 101

Consider the vector field $F(x,y,z)=⟨2 x + 2 z,\,2 y + 4 z,\,2 x - 8 y⟩$ and the surface $S$ defined by $z=2 x - 4 y$ for $1\le x\le 3$ and $1\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{1}^{3}{\int }_{1}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $2 u - 2 v$
- $48 uv$
- $22 u + 8 v$
- $22 u - 48 v$
- $14 uv - 8 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,2 u - 4 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,1\le u\le 3,\,1\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(2 u - 4 v)⟩ \\  & =⟨1,\,0,\,2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(2 u - 4 v)⟩ \\  & =⟨0,\,1,\,-4⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 2 \\ 0 & 1 & -4\end{aligned}| \\  & =⟨|\begin{aligned}0 & 2 \\ 1 & -4\end{aligned}|,\,-|\begin{aligned}1 & 2 \\ 0 & -4\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-2,\,4,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 x + 2 z,\,2 y + 4 z,\,2 x - 8 y⟩{|}_{x=u,\,\,y=v,\,\,z=2 u - 4 v} \\  & =⟨2 u + 2 (2 u - 4 v),\,2 v + 4 (2 u - 4 v),\,2 u - 8 v⟩ \\  & =⟨6 u - 8 v,\,8 u - 14 v,\,2 u - 8 v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨6 u - 8 v,\,8 u - 14 v,\,2 u - 8 v⟩\cdot ⟨-2,\,4,\,1⟩ \\  & =(6 u - 8 v)\cdot (-2)+(8 u - 14 v)\cdot (4)+(2 u - 8 v)\cdot (1) \\  & =- 12 u + 16 v+32 u - 56 v+2 u - 8 v \\  & =22 u - 48 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 x + 2 z,\,2 y + 4 z,\,2 x - 8 y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(22 u - 48 v)\,\text{d}A \\  & ={\int }_{1}^{3}{\int }_{1}^{4}(22 u - 48 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161381 102

Consider the vector field $F(x,y,z)=⟨2 x + 2 z,\,2 y + 4 z,\,2 x - 8 y⟩$ and the surface $S$ defined by $z=2 x - 4 y$ for $-2\le x\le 4$ and $-2\le y\le 3.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{4}{\int }_{-2}^{3}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $22 u - 48 v$
- $14 uv - 8 v$
- $48 uv$
- $2 u - 2 v$
- $22 u + 8 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,2 u - 4 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 4,\,-2\le v\le 3\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(2 u - 4 v)⟩ \\  & =⟨1,\,0,\,2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(2 u - 4 v)⟩ \\  & =⟨0,\,1,\,-4⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 2 \\ 0 & 1 & -4\end{aligned}| \\  & =⟨|\begin{aligned}0 & 2 \\ 1 & -4\end{aligned}|,\,-|\begin{aligned}1 & 2 \\ 0 & -4\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-2,\,4,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 x + 2 z,\,2 y + 4 z,\,2 x - 8 y⟩{|}_{x=u,\,\,y=v,\,\,z=2 u - 4 v} \\  & =⟨2 u + 2 (2 u - 4 v),\,2 v + 4 (2 u - 4 v),\,2 u - 8 v⟩ \\  & =⟨6 u - 8 v,\,8 u - 14 v,\,2 u - 8 v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨6 u - 8 v,\,8 u - 14 v,\,2 u - 8 v⟩\cdot ⟨-2,\,4,\,1⟩ \\  & =(6 u - 8 v)\cdot (-2)+(8 u - 14 v)\cdot (4)+(2 u - 8 v)\cdot (1) \\  & =- 12 u + 16 v+32 u - 56 v+2 u - 8 v \\  & =22 u - 48 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 x + 2 z,\,2 y + 4 z,\,2 x - 8 y⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(22 u - 48 v)\,\text{d}A \\  & ={\int }_{-2}^{4}{\int }_{-2}^{3}(22 u - 48 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161467 101

Consider the vector field $F(x,y,z)=⟨4 x - 2 z,\,2 y - 2 z,\,2 y + 2 z⟩$ and the surface $S$ defined by $z=4 x - y$ for $1\le x\le 3$ and $1\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{1}^{3}{\int }_{1}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $- 8 v$
- $4 u + 8 v$
- $16 u - 4 v$
- $2 u - 4 v$
- $16 u$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u - v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,1\le u\le 3,\,1\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u - v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u - v)⟩ \\  & =⟨0,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & -1\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & -1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨4 x - 2 z,\,2 y - 2 z,\,2 y + 2 z⟩{|}_{x=u,\,\,y=v,\,\,z=4 u - v} \\  & =⟨4 u - 2 (4 u - v),\,2 v - 2 (4 u - v),\,2 v + 2 (4 u - v)⟩ \\  & =⟨- 4 u + 2 v,\,- 8 u + 4 v,\,8 u⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨- 4 u + 2 v,\,- 8 u + 4 v,\,8 u⟩\cdot ⟨-4,\,1,\,1⟩ \\  & =(- 4 u + 2 v)\cdot (-4)+(- 8 u + 4 v)\cdot (1)+(8 u)\cdot (1) \\  & =16 u - 8 v- 8 u + 4 v+8 u \\  & =16 u - 4 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨4 x - 2 z,\,2 y - 2 z,\,2 y + 2 z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(16 u - 4 v)\,\text{d}A \\  & ={\int }_{1}^{3}{\int }_{1}^{4}(16 u - 4 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161467 102

Consider the vector field $F(x,y,z)=⟨4 x - 2 z,\,2 y - 2 z,\,2 y + 2 z⟩$ and the surface $S$ defined by $z=4 x - y$ for $-2\le x\le 4$ and $-2\le y\le 3.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{4}{\int }_{-2}^{3}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $2 u - 4 v$
- $16 u$
- $4 u + 8 v$
- $- 8 v$
- $16 u - 4 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,4 u - v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 4,\,-2\le v\le 3\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(4 u - v)⟩ \\  & =⟨1,\,0,\,4⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(4 u - v)⟩ \\  & =⟨0,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 4 \\ 0 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 4 \\ 1 & -1\end{aligned}|,\,-|\begin{aligned}1 & 4 \\ 0 & -1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-4,\,1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨4 x - 2 z,\,2 y - 2 z,\,2 y + 2 z⟩{|}_{x=u,\,\,y=v,\,\,z=4 u - v} \\  & =⟨4 u - 2 (4 u - v),\,2 v - 2 (4 u - v),\,2 v + 2 (4 u - v)⟩ \\  & =⟨- 4 u + 2 v,\,- 8 u + 4 v,\,8 u⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨- 4 u + 2 v,\,- 8 u + 4 v,\,8 u⟩\cdot ⟨-4,\,1,\,1⟩ \\  & =(- 4 u + 2 v)\cdot (-4)+(- 8 u + 4 v)\cdot (1)+(8 u)\cdot (1) \\  & =16 u - 8 v- 8 u + 4 v+8 u \\  & =16 u - 4 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨4 x - 2 z,\,2 y - 2 z,\,2 y + 2 z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(16 u - 4 v)\,\text{d}A \\  & ={\int }_{-2}^{4}{\int }_{-2}^{3}(16 u - 4 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161357 101

Consider the vector field $F(x,y,z)=⟨2 x + 2 y,\,4 x - 2 y,\,2 x + 2 z⟩$ and the surface $S$ defined by $z=2 x - 2 y$ for $1\le x\le 3$ and $1\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{1}^{3}{\int }_{1}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $2 u + 2 v$
- $10 u - 12 v$
- $22 uv$
- $6 uv$
- $- 4 u + 2 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,2 u - 2 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,1\le u\le 3,\,1\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(2 u - 2 v)⟩ \\  & =⟨1,\,0,\,2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(2 u - 2 v)⟩ \\  & =⟨0,\,1,\,-2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 2 \\ 0 & 1 & -2\end{aligned}| \\  & =⟨|\begin{aligned}0 & 2 \\ 1 & -2\end{aligned}|,\,-|\begin{aligned}1 & 2 \\ 0 & -2\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-2,\,2,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 x + 2 y,\,4 x - 2 y,\,2 x + 2 z⟩{|}_{x=u,\,\,y=v,\,\,z=2 u - 2 v} \\  & =⟨2 u + 2 v,\,4 u - 2 v,\,2 u + 2 (2 u - 2 v)⟩ \\  & =⟨2 u + 2 v,\,4 u - 2 v,\,6 u - 4 v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 u + 2 v,\,4 u - 2 v,\,6 u - 4 v⟩\cdot ⟨-2,\,2,\,1⟩ \\  & =(2 u + 2 v)\cdot (-2)+(4 u - 2 v)\cdot (2)+(6 u - 4 v)\cdot (1) \\  & =- 4 u - 4 v+8 u - 4 v+6 u - 4 v \\  & =10 u - 12 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 x + 2 y,\,4 x - 2 y,\,2 x + 2 z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(10 u - 12 v)\,\text{d}A \\  & ={\int }_{1}^{3}{\int }_{1}^{4}(10 u - 12 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161357 102

Consider the vector field $F(x,y,z)=⟨2 x + 2 y,\,4 x - 2 y,\,2 x + 2 z⟩$ and the surface $S$ defined by $z=2 x - 2 y$ for $-2\le x\le 4$ and $-2\le y\le 3.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{4}{\int }_{-2}^{3}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $6 uv$
- $- 4 u + 2 v$
- $10 u - 12 v$
- $2 u + 2 v$
- $22 uv$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,2 u - 2 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 4,\,-2\le v\le 3\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(2 u - 2 v)⟩ \\  & =⟨1,\,0,\,2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(2 u - 2 v)⟩ \\  & =⟨0,\,1,\,-2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 2 \\ 0 & 1 & -2\end{aligned}| \\  & =⟨|\begin{aligned}0 & 2 \\ 1 & -2\end{aligned}|,\,-|\begin{aligned}1 & 2 \\ 0 & -2\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-2,\,2,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 x + 2 y,\,4 x - 2 y,\,2 x + 2 z⟩{|}_{x=u,\,\,y=v,\,\,z=2 u - 2 v} \\  & =⟨2 u + 2 v,\,4 u - 2 v,\,2 u + 2 (2 u - 2 v)⟩ \\  & =⟨2 u + 2 v,\,4 u - 2 v,\,6 u - 4 v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 u + 2 v,\,4 u - 2 v,\,6 u - 4 v⟩\cdot ⟨-2,\,2,\,1⟩ \\  & =(2 u + 2 v)\cdot (-2)+(4 u - 2 v)\cdot (2)+(6 u - 4 v)\cdot (1) \\  & =- 4 u - 4 v+8 u - 4 v+6 u - 4 v \\  & =10 u - 12 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 x + 2 y,\,4 x - 2 y,\,2 x + 2 z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(10 u - 12 v)\,\text{d}A \\  & ={\int }_{-2}^{4}{\int }_{-2}^{3}(10 u - 12 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161359 101

Consider the vector field $F(x,y,z)=⟨2 y z,\,2 x z,\,2 xy⟩$ and the surface $S$ defined by $z=x - y$ for $1\le x\le 3$ and $1\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{1}^{3}{\int }_{1}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $2 u^{2} - 4 uv + 2 v^{2}$
- $2 u^{2} + 2 uv - 2 v^{2}$
- $2 u^{2} + 4 uv + 2 v^{2}$
- $2 u^{2} - 2 v^{2}$
- $2 u^{2} - 2 uv + 2 v^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u - v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,1\le u\le 3,\,1\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u - v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u - v)⟩ \\  & =⟨0,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & -1\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & -1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 y z,\,2 x z,\,2 xy⟩{|}_{x=u,\,\,y=v,\,\,z=u - v} \\  & =⟨2 v (u - v),\,2 u (u - v),\,2 uv⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 v (u - v),\,2 u (u - v),\,2 uv⟩\cdot ⟨-1,\,1,\,1⟩ \\  & =(2 v (u - v))\cdot (-1)+(2 u (u - v))\cdot (1)+(2 uv)\cdot (1) \\  & =- 2 uv + 2 v^{2}+2 u^{2} - 2 uv+2 uv \\  & =2 u^{2} - 2 uv + 2 v^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 y z,\,2 x z,\,2 xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(2 u^{2} - 2 uv + 2 v^{2})\,\text{d}A \\  & ={\int }_{1}^{3}{\int }_{1}^{4}(2 u^{2} - 2 uv + 2 v^{2})\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161359 102

Consider the vector field $F(x,y,z)=⟨2 y z,\,2 x z,\,2 xy⟩$ and the surface $S$ defined by $z=x - y$ for $-2\le x\le 4$ and $-2\le y\le 3.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{4}{\int }_{-2}^{3}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $2 u^{2} - 2 v^{2}$
- $2 u^{2} - 2 uv + 2 v^{2}$
- $2 u^{2} + 2 uv - 2 v^{2}$
- $2 u^{2} - 4 uv + 2 v^{2}$
- $2 u^{2} + 4 uv + 2 v^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u - v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 4,\,-2\le v\le 3\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u - v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u - v)⟩ \\  & =⟨0,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & -1\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & -1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 y z,\,2 x z,\,2 xy⟩{|}_{x=u,\,\,y=v,\,\,z=u - v} \\  & =⟨2 v (u - v),\,2 u (u - v),\,2 uv⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 v (u - v),\,2 u (u - v),\,2 uv⟩\cdot ⟨-1,\,1,\,1⟩ \\  & =(2 v (u - v))\cdot (-1)+(2 u (u - v))\cdot (1)+(2 uv)\cdot (1) \\  & =- 2 uv + 2 v^{2}+2 u^{2} - 2 uv+2 uv \\  & =2 u^{2} - 2 uv + 2 v^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 y z,\,2 x z,\,2 xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(2 u^{2} - 2 uv + 2 v^{2})\,\text{d}A \\  & ={\int }_{-2}^{4}{\int }_{-2}^{3}(2 u^{2} - 2 uv + 2 v^{2})\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161377 101

Consider the vector field $F(x,y,z)=⟨2 x^{2} - 2 y^{2},\,2 y^{2} - 2 z^{2},\,2 z^{2}⟩$ and the surface $S$ defined by $z=- x - y$ for $1\le x\le 3$ and $1\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{1}^{3}{\int }_{1}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $4 uv$
- $6 v$
- $2 u^{3}$
- $8 uv$
- $2 u^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,- u - v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,1\le u\le 3,\,1\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(- u - v)⟩ \\  & =⟨1,\,0,\,-1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(- u - v)⟩ \\  & =⟨0,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -1 \\ 0 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}0 & -1 \\ 1 & -1\end{aligned}|,\,-|\begin{aligned}1 & -1 \\ 0 & -1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨1,\,1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 x^{2} - 2 y^{2},\,2 y^{2} - 2 z^{2},\,2 z^{2}⟩{|}_{x=u,\,\,y=v,\,\,z=- u - v} \\  & =⟨2 u^{2} - 2 v^{2},\,2 v^{2} - 2 (- u - v)^{2},\,2 (- u - v)^{2}⟩\end{aligned}
$$

 

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 u^{2} - 2 v^{2},\,2 v^{2} - 2 (- u - v)^{2},\,2 (- u - v)^{2}⟩\cdot ⟨1,\,1,\,1⟩ \\  & =(2 u^{2} - 2 v^{2})\cdot (1)+(2 v^{2} - 2 (- u - v)^{2})\cdot (1)+(2 (- u - v)^{2})\cdot (1) \\  & =2 u^{2} - 2 v^{2}+2 v^{2} - 2 \left(- u - v\right)^{2}+2 \left(- u - v\right)^{2} \\  & =2 u^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 x^{2} - 2 y^{2},\,2 y^{2} - 2 z^{2},\,2 z^{2}⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(2 u^{2})\,\text{d}A \\  & ={\int }_{1}^{3}{\int }_{1}^{4}(2 u^{2})\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161377 102

Consider the vector field $F(x,y,z)=⟨2 x^{2} - 2 y^{2},\,2 y^{2} - 2 z^{2},\,2 z^{2}⟩$ and the surface $S$ defined by $z=- x - y$ for $-2\le x\le 4$ and $-2\le y\le 3.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{4}{\int }_{-2}^{3}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $8 uv$
- $2 u^{2}$
- $6 v$
- $4 uv$
- $2 u^{3}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,- u - v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 4,\,-2\le v\le 3\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(- u - v)⟩ \\  & =⟨1,\,0,\,-1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(- u - v)⟩ \\  & =⟨0,\,1,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -1 \\ 0 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}0 & -1 \\ 1 & -1\end{aligned}|,\,-|\begin{aligned}1 & -1 \\ 0 & -1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨1,\,1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 x^{2} - 2 y^{2},\,2 y^{2} - 2 z^{2},\,2 z^{2}⟩{|}_{x=u,\,\,y=v,\,\,z=- u - v} \\  & =⟨2 u^{2} - 2 v^{2},\,2 v^{2} - 2 (- u - v)^{2},\,2 (- u - v)^{2}⟩\end{aligned}
$$

 

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 u^{2} - 2 v^{2},\,2 v^{2} - 2 (- u - v)^{2},\,2 (- u - v)^{2}⟩\cdot ⟨1,\,1,\,1⟩ \\  & =(2 u^{2} - 2 v^{2})\cdot (1)+(2 v^{2} - 2 (- u - v)^{2})\cdot (1)+(2 (- u - v)^{2})\cdot (1) \\  & =2 u^{2} - 2 v^{2}+2 v^{2} - 2 \left(- u - v\right)^{2}+2 \left(- u - v\right)^{2} \\  & =2 u^{2}.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 x^{2} - 2 y^{2},\,2 y^{2} - 2 z^{2},\,2 z^{2}⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(2 u^{2})\,\text{d}A \\  & ={\int }_{-2}^{4}{\int }_{-2}^{3}(2 u^{2})\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161379 101

Consider the vector field $F(x,y,z)=⟨2 \left(x + y\right)^{2},\,2 \left(x - y\right)^{2},\,2 xy⟩$ and the surface $S$ defined by $z=- x + y$ for $1\le x\le 3$ and $1\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{1}^{3}{\int }_{1}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $2 uv + 2 v$
- $2 uv - 2 v$
- $6 uv^{2}$
- $10 uv$
- $- 2 uv$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,- u + v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,1\le u\le 3,\,1\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(- u + v)⟩ \\  & =⟨1,\,0,\,-1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(- u + v)⟩ \\  & =⟨0,\,1,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -1 \\ 0 & 1 & 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & -1 \\ 1 & 1\end{aligned}|,\,-|\begin{aligned}1 & -1 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨1,\,-1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 \left(x + y\right)^{2},\,2 \left(x - y\right)^{2},\,2 xy⟩{|}_{x=u,\,\,y=v,\,\,z=- u + v} \\  & =⟨2 \left(u + v\right)^{2},\,2 \left(u - v\right)^{2},\,2 uv⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 \left(u + v\right)^{2},\,2 \left(u - v\right)^{2},\,2 uv⟩\cdot ⟨1,\,-1,\,1⟩ \\  & =(2 \left(u + v\right)^{2})\cdot (1)+(2 \left(u - v\right)^{2})\cdot (-1)+(2 uv)\cdot (1) \\  & =10 uv.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 \left(x + y\right)^{2},\,2 \left(x - y\right)^{2},\,2 xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(10 uv)\,\text{d}A \\  & ={\int }_{1}^{3}{\int }_{1}^{4}(10 uv)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161379 102

Consider the vector field $F(x,y,z)=⟨2 \left(x + y\right)^{2},\,2 \left(x - y\right)^{2},\,2 xy⟩$ and the surface $S$ defined by $z=- x + y$ for $-2\le x\le 4$ and $-2\le y\le 3.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{4}{\int }_{-2}^{3}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $10 uv$
- $- 2 uv$
- $2 uv - 2 v$
- $2 uv + 2 v$
- $6 uv^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,- u + v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 4,\,-2\le v\le 3\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(- u + v)⟩ \\  & =⟨1,\,0,\,-1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(- u + v)⟩ \\  & =⟨0,\,1,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -1 \\ 0 & 1 & 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & -1 \\ 1 & 1\end{aligned}|,\,-|\begin{aligned}1 & -1 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨1,\,-1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 \left(x + y\right)^{2},\,2 \left(x - y\right)^{2},\,2 xy⟩{|}_{x=u,\,\,y=v,\,\,z=- u + v} \\  & =⟨2 \left(u + v\right)^{2},\,2 \left(u - v\right)^{2},\,2 uv⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 \left(u + v\right)^{2},\,2 \left(u - v\right)^{2},\,2 uv⟩\cdot ⟨1,\,-1,\,1⟩ \\  & =(2 \left(u + v\right)^{2})\cdot (1)+(2 \left(u - v\right)^{2})\cdot (-1)+(2 uv)\cdot (1) \\  & =10 uv.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 \left(x + y\right)^{2},\,2 \left(x - y\right)^{2},\,2 xy⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(10 uv)\,\text{d}A \\  & ={\int }_{-2}^{4}{\int }_{-2}^{3}(10 uv)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161471 101

Consider the vector field $F(x,y,z)=⟨2 x + 2 z,\,4 z,\,2 y + 2 z⟩$ and the surface $S$ defined by $z=x - 3 y$ for $1\le x\le 3$ and $1\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{1}^{3}{\int }_{1}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $10 u - 34 v$
- $2 u - 12 v$
- $16 u + 28 v$
- $24 u - 2 v$
- $16 u - 46 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u - 3 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,1\le u\le 3,\,1\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u - 3 v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u - 3 v)⟩ \\  & =⟨0,\,1,\,-3⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & -3\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & -3\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & -3\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,3,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 x + 2 z,\,4 z,\,2 y + 2 z⟩{|}_{x=u,\,\,y=v,\,\,z=u - 3 v} \\  & =⟨2 u + 2 (u - 3 v),\,4 (u - 3 v),\,2 v + 2 (u - 3 v)⟩ \\  & =⟨4 u - 6 v,\,4 u - 12 v,\,2 u - 4 v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨4 u - 6 v,\,4 u - 12 v,\,2 u - 4 v⟩\cdot ⟨-1,\,3,\,1⟩ \\  & =(4 u - 6 v)\cdot (-1)+(4 u - 12 v)\cdot (3)+(2 u - 4 v)\cdot (1) \\  & =- 4 u + 6 v+12 u - 36 v+2 u - 4 v \\  & =10 u - 34 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 x + 2 z,\,4 z,\,2 y + 2 z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(10 u - 34 v)\,\text{d}A \\  & ={\int }_{1}^{3}{\int }_{1}^{4}(10 u - 34 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161471 102

Consider the vector field $F(x,y,z)=⟨2 x + 2 z,\,4 z,\,2 y + 2 z⟩$ and the surface $S$ defined by $z=x - 3 y$ for $-2\le x\le 4$ and $-2\le y\le 3.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{4}{\int }_{-2}^{3}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $24 u - 2 v$
- $16 u - 46 v$
- $2 u - 12 v$
- $10 u - 34 v$
- $16 u + 28 v$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u - 3 v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 4,\,-2\le v\le 3\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u - 3 v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u - 3 v)⟩ \\  & =⟨0,\,1,\,-3⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & -3\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & -3\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & -3\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,3,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 x + 2 z,\,4 z,\,2 y + 2 z⟩{|}_{x=u,\,\,y=v,\,\,z=u - 3 v} \\  & =⟨2 u + 2 (u - 3 v),\,4 (u - 3 v),\,2 v + 2 (u - 3 v)⟩ \\  & =⟨4 u - 6 v,\,4 u - 12 v,\,2 u - 4 v⟩\end{aligned}
$$

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨4 u - 6 v,\,4 u - 12 v,\,2 u - 4 v⟩\cdot ⟨-1,\,3,\,1⟩ \\  & =(4 u - 6 v)\cdot (-1)+(4 u - 12 v)\cdot (3)+(2 u - 4 v)\cdot (1) \\  & =- 4 u + 6 v+12 u - 36 v+2 u - 4 v \\  & =10 u - 34 v.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 x + 2 z,\,4 z,\,2 y + 2 z⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(10 u - 34 v)\,\text{d}A \\  & ={\int }_{-2}^{4}{\int }_{-2}^{3}(10 u - 34 v)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161360-legacy 101

Consider the vector field $F(x,y,z)=⟨2 x^{2},\,2 y^{2},\,2 z^{2}⟩$ and the surface $S$ defined by $z=x + y$ for $1\le x\le 3$ and $1\le y\le 4.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{1}^{3}{\int }_{1}^{4}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $2 u^{2} - 2 v^{2}$
- $4 u^{2} + 8 uv + 4 v^{2}$
- $4 uv$
- $2 u^{2} + 2 uv + 2 v^{2}$
- $2 u^{2} + 2 v^{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u + v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,1\le u\le 3,\,1\le v\le 4\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u + v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u + v)⟩ \\  & =⟨0,\,1,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & 1\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,-1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 x^{2},\,2 y^{2},\,2 z^{2}⟩{|}_{x=u,\,\,y=v,\,\,z=u + v} \\  & =⟨2 u^{2},\,2 v^{2},\,2 (u + v)^{2}⟩\end{aligned}
$$

 

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 u^{2},\,2 v^{2},\,2 (u + v)^{2}⟩\cdot ⟨-1,\,-1,\,1⟩ \\  & =(2 u^{2})\cdot (-1)+(2 v^{2})\cdot (-1)+(2 (u + v)^{2})\cdot (1) \\  & =- 2 u^{2}- 2 v^{2}+2 u^{2} + 4 uv + 2 v^{2} \\  & =4 uv.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 x^{2},\,2 y^{2},\,2 z^{2}⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(4 uv)\,\text{d}A \\  & ={\int }_{1}^{3}{\int }_{1}^{4}(4 uv)\,\text{d}v\,\text{d}u.\end{aligned}
$$

## Generated evidence bank q-161360-legacy 102

Consider the vector field $F(x,y,z)=⟨2 x^{2},\,2 y^{2},\,2 z^{2}⟩$ and the surface $S$ defined by $z=x + y$ for $-2\le x\le 4$ and $-2\le y\le 3.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as

$$
{∬}_{S}F\cdot \text{d}S={\int }_{-2}^{4}{\int }_{-2}^{3}\boxed{}\,\text{d}v\,\text{d}u.
$$

What is the missing expression?

- $2 u^{2} + 2 uv + 2 v^{2}$
- $2 u^{2} + 2 v^{2}$
- $4 u^{2} + 8 uv + 4 v^{2}$
- $2 u^{2} - 2 v^{2}$
- $4 uv$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Using the parametrization, where $x=u$ and $y=v,$ our surface can be parameterized as

$$
r(u,v)=⟨u,\,v,\,u + v⟩
$$

over the domain 

$$
D=\{(u,v)\,:\,-2\le u\le 4,\,-2\le v\le 3\}.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u + v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u + v)⟩ \\  & =⟨0,\,1,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & 1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & 1\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & 1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,-1,\,1⟩.\end{aligned}
$$

Next, we substitute the coordinate expressions of $r(u,v)$ into $F(x,y,z):$

$$
\begin{aligned}F(r(u,v)) & =⟨2 x^{2},\,2 y^{2},\,2 z^{2}⟩{|}_{x=u,\,\,y=v,\,\,z=u + v} \\  & =⟨2 u^{2},\,2 v^{2},\,2 (u + v)^{2}⟩\end{aligned}
$$

 

Then, we calculate the dot product of $F$ and ${r}_{u}^{′}\times {r}_{v}^{′}:$

$$
\begin{aligned}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & =⟨2 u^{2},\,2 v^{2},\,2 (u + v)^{2}⟩\cdot ⟨-1,\,-1,\,1⟩ \\  & =(2 u^{2})\cdot (-1)+(2 v^{2})\cdot (-1)+(2 (u + v)^{2})\cdot (1) \\  & =- 2 u^{2}- 2 v^{2}+2 u^{2} + 4 uv + 2 v^{2} \\  & =4 uv.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}⟨2 x^{2},\,2 y^{2},\,2 z^{2}⟩\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A. \\  & ={∬}_{D}(4 uv)\,\text{d}A \\  & ={\int }_{-2}^{4}{\int }_{-2}^{3}(4 uv)\,\text{d}v\,\text{d}u.\end{aligned}
$$
