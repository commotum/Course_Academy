# Original and generated Cartesian flux formula review

Raw originals and normal generator replays appear below. Four replays repair documented teaching errors. Generated labels distinguish variants from originals and label symbolic notation aliases honestly. No plots occur.

## Raw original q-161166

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\frac{}{∂x}-Q\frac{∂g}{}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $-P,\,$ $∂P,\,$ $∂x$
- $P,\,$ $∂g,\,$ $∂x$
- $-P,\,$ $∂g,\,$ $∂x$
- $P,\,$ $∂g,\,$ $∂y$
- $-P,\,$ $∂g,\,$ $∂y$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=g(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,g(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂g}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂g}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂g}{∂x} \\ 0 & 1 & \frac{∂g}{∂y}\end{aligned}|=⟨-\frac{∂g}{∂x},\,-\frac{∂g}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂g}{∂x},\,-\frac{∂g}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\,\text{d}A.\end{aligned}
$$

## Original replay q-161166

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\frac{}{∂x}-Q\frac{∂g}{}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $-P,\,$ $∂g,\,$ $∂x$
- $P,\,$ $∂g,\,$ $∂x$
- $-P,\,$ $∂P,\,$ $∂x$
- $-P,\,$ $∂g,\,$ $∂y$ (correct)
- $P,\,$ $∂g,\,$ $∂y$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=g(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,g(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂g}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂g}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂g}{∂x} \\ 0 & 1 & \frac{∂g}{∂y}\end{aligned}|=⟨-\frac{∂g}{∂x},\,-\frac{∂g}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂g}{∂x},\,-\frac{∂g}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161166 0 (notation alias; finite same formula mask)

For a surface $S$ given by $z=k(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\frac{}{∂x}-Q\frac{∂k}{}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $P,\,$ $∂k,\,$ $∂y$
- $-P,\,$ $∂k,\,$ $∂y$ (correct)
- $-P,\,$ $∂P,\,$ $∂x$
- $P,\,$ $∂k,\,$ $∂x$
- $-P,\,$ $∂k,\,$ $∂x$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=k(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,k(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂k}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂k}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂k}{∂x} \\ 0 & 1 & \frac{∂k}{∂y}\end{aligned}|=⟨-\frac{∂k}{∂x},\,-\frac{∂k}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂k}{∂x},\,-\frac{∂k}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂k}{∂x}-Q\frac{∂k}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161166 1 (notation alias; finite same formula mask)

For a surface $S$ given by $z=h(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\frac{}{∂x}-Q\frac{∂h}{}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $-P,\,$ $∂h,\,$ $∂y$ (correct)
- $P,\,$ $∂h,\,$ $∂x$
- $P,\,$ $∂h,\,$ $∂y$
- $-P,\,$ $∂h,\,$ $∂x$
- $-P,\,$ $∂P,\,$ $∂x$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=h(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,h(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂h}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂h}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂h}{∂x} \\ 0 & 1 & \frac{∂h}{∂y}\end{aligned}|=⟨-\frac{∂h}{∂x},\,-\frac{∂h}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂h}{∂x},\,-\frac{∂h}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂h}{∂x}-Q\frac{∂h}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Raw original q-161189

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\frac{∂g}{∂x}+\frac{∂g}{∂y}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $P$ and $Q$
- $-P$ and $Q$
- $Q$ and $P$
- $P$ and $-Q$
- $-P$ and $-Q$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=g(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,g(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂g}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂g}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂g}{∂x} \\ 0 & 1 & \frac{∂g}{∂y}\end{aligned}|=⟨-\frac{∂g}{∂x},\,-\frac{∂g}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂g}{∂x},\,-\frac{∂g}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂g}{∂x}+(-Q\,)\frac{∂g}{∂y}+R)\,\text{d}A.\end{aligned}
$$

## Original replay q-161189

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\frac{∂g}{∂x}+\frac{∂g}{∂y}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $Q$ and $P$
- $-P$ and $Q$
- $P$ and $Q$
- $-P$ and $-Q$ (correct)
- $P$ and $-Q$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=g(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,g(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂g}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂g}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂g}{∂x} \\ 0 & 1 & \frac{∂g}{∂y}\end{aligned}|=⟨-\frac{∂g}{∂x},\,-\frac{∂g}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂g}{∂x},\,-\frac{∂g}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂g}{∂x}+(-Q\,)\frac{∂g}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161189 0 (notation alias; finite same formula mask)

For a surface $S$ given by $z=k(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\frac{∂k}{∂x}+\frac{∂k}{∂y}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $P$ and $-Q$
- $-P$ and $-Q$ (correct)
- $P$ and $Q$
- $-P$ and $Q$
- $Q$ and $P$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=k(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,k(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂k}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂k}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂k}{∂x} \\ 0 & 1 & \frac{∂k}{∂y}\end{aligned}|=⟨-\frac{∂k}{∂x},\,-\frac{∂k}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂k}{∂x},\,-\frac{∂k}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂k}{∂x}+(-Q\,)\frac{∂k}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161189 1 (notation alias; finite same formula mask)

For a surface $S$ given by $z=h(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\frac{∂h}{∂x}+\frac{∂h}{∂y}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $-P$ and $-Q$ (correct)
- $-P$ and $Q$
- $P$ and $-Q$
- $Q$ and $P$
- $P$ and $Q$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=h(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,h(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂h}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂h}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂h}{∂x} \\ 0 & 1 & \frac{∂h}{∂y}\end{aligned}|=⟨-\frac{∂h}{∂x},\,-\frac{∂h}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂h}{∂x},\,-\frac{∂h}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂h}{∂x}+(-Q\,)\frac{∂h}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Raw original q-161446

For a surface $S$ given by $x=k(y,z)$ for $(y,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(P+\frac{∂k}{∂y}-R\frac{∂k}{})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $-Q$ and $∂z$ (correct)
- $-Q$ and $∂x$
- $Q$ and $∂x$
- $Q$ and $∂z$
- $-R$ and $∂z$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $x=k(y,z),$ it can be parameterized as

$$
r(y,z)=⟨k(y,z),\,y,\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{y}^{′} & =⟨\frac{∂k}{∂y},\,1,\,0⟩ \\ {r}_{z}^{′} & =⟨\frac{∂k}{∂z},\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{y}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ \frac{∂k}{∂y} & 1 & 0 \\ \frac{∂k}{∂z} & 0 & 1\end{aligned}|=⟨1,\,-\frac{∂k}{∂y},\,-\frac{∂k}{∂z}⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{y}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨1,\,-\frac{∂k}{∂y},\,-\frac{∂k}{∂z}⟩\,\text{d}A \\  & ={∬}_{D}(P+(-Q\,)\frac{∂k}{∂y}-R\frac{∂k}{∂z})\,\text{d}A.\end{aligned}
$$

## Original replay q-161446 (supported solution repair)

For a surface $S$ given by $x=k(y,z)$ for $(y,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(P+\frac{∂k}{∂y}-R\frac{∂k}{})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $Q$ and $∂x$
- $-Q$ and $∂x$
- $-Q$ and $∂z$ (correct)
- $-R$ and $∂z$
- $Q$ and $∂z$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $x=k(y,z),$ it can be parameterized as

$$
r(y,z)=⟨k(y,z),\,y,\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{y}^{′} & =⟨\frac{∂k}{∂y},\,1,\,0⟩ \\ {r}_{z}^{′} & =⟨\frac{∂k}{∂z},\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{y}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ \frac{∂k}{∂y} & 1 & 0 \\ \frac{∂k}{∂z} & 0 & 1\end{aligned}|=⟨1,\,-\frac{∂k}{∂y},\,-\frac{∂k}{∂z}⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(y,z))\cdot ({r}_{y}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨1,\,-\frac{∂k}{∂y},\,-\frac{∂k}{∂z}⟩\,\text{d}A \\  & ={∬}_{D}(P+(-Q\,)\frac{∂k}{∂y}-R\frac{∂k}{∂z})\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161446 0 (notation alias; finite same formula mask)

For a surface $S$ given by $x=k(y,z)$ for $(y,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(P+\frac{∂k}{∂y}-R\frac{∂k}{})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $Q$ and $∂z$
- $-R$ and $∂z$
- $-Q$ and $∂z$ (correct)
- $-Q$ and $∂x$
- $Q$ and $∂x$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $x=k(y,z),$ it can be parameterized as

$$
r(y,z)=⟨k(y,z),\,y,\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{y}^{′} & =⟨\frac{∂k}{∂y},\,1,\,0⟩ \\ {r}_{z}^{′} & =⟨\frac{∂k}{∂z},\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{y}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ \frac{∂k}{∂y} & 1 & 0 \\ \frac{∂k}{∂z} & 0 & 1\end{aligned}|=⟨1,\,-\frac{∂k}{∂y},\,-\frac{∂k}{∂z}⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(y,z))\cdot ({r}_{y}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨1,\,-\frac{∂k}{∂y},\,-\frac{∂k}{∂z}⟩\,\text{d}A \\  & ={∬}_{D}(P+(-Q\,)\frac{∂k}{∂y}-R\frac{∂k}{∂z})\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161446 1 (notation alias; finite same formula mask)

For a surface $S$ given by $x=h(y,z)$ for $(y,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(P+\frac{∂h}{∂y}-R\frac{∂h}{})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $-R$ and $∂z$
- $-Q$ and $∂x$
- $Q$ and $∂z$
- $Q$ and $∂x$
- $-Q$ and $∂z$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $x=h(y,z),$ it can be parameterized as

$$
r(y,z)=⟨h(y,z),\,y,\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{y}^{′} & =⟨\frac{∂h}{∂y},\,1,\,0⟩ \\ {r}_{z}^{′} & =⟨\frac{∂h}{∂z},\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{y}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ \frac{∂h}{∂y} & 1 & 0 \\ \frac{∂h}{∂z} & 0 & 1\end{aligned}|=⟨1,\,-\frac{∂h}{∂y},\,-\frac{∂h}{∂z}⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(y,z))\cdot ({r}_{y}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨1,\,-\frac{∂h}{∂y},\,-\frac{∂h}{∂z}⟩\,\text{d}A \\  & ={∬}_{D}(P+(-Q\,)\frac{∂h}{∂y}-R\frac{∂h}{∂z})\,\text{d}A.\end{aligned}
$$


## Raw original q-161453

For a surface $S$ given by $y=-{x}^{2}z$ for $(x,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\,xz+Q+\,{x}^{2})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

*Hint: The orientation of $S$ should be chosen such that the unit normal vector has a positive  $j$-component.*

- $2P$ and $R$ (correct)
- $P$ and $-2R$
- $P$ and $R$
- $-2P$ and $2R$
- $2P$ and $-2R$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $y=-{x}^{2}z,$ it can be parameterized as

$$
r(x,z)=⟨x,\,-{x}^{2}z,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,-2xz,\,0⟩ \\ {r}_{z}^{′} & =⟨0,\,-{x}^{2},\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 1 & -2xz & 0 \\ 0 & -{x}^{2} & 1\end{aligned}|=⟨-2xz,\,-1,\,-{x}^{2}⟩.\end{aligned}
$$

However, notice that the $j$-component is negative. Therefore, we select the normal vector that points in the *opposite* direction:

$$
{r}_{z}^{′}\times {r}_{x}^{′}=-{r}_{x}^{′}\times {r}_{z}^{′}=⟨2xz,\,1,\,{x}^{2}⟩
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,z))\cdot ({r}_{x}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,R\,⟩\cdot ⟨2xz,\,1,\,{x}^{2}⟩\,\text{d}A \\  & ={∬}_{D}(2P\,xz+Q+R\,{x}^{2})\,\text{d}A.\end{aligned}
$$

## Original replay q-161453 (supported solution repair)

For a surface $S$ given by $y=-{x}^{2}z$ for $(x,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\,xz+Q+\,{x}^{2})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

*Hint: The orientation of $S$ should be chosen such that the unit normal vector has a positive  $j$-component.*

- $P$ and $R$
- $P$ and $-2R$
- $2P$ and $R$ (correct)
- $2P$ and $-2R$
- $-2P$ and $2R$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $y=-{x}^{2}z,$ it can be parameterized as

$$
r(x,z)=⟨x,\,-{x}^{2}z,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,-2xz,\,0⟩ \\ {r}_{z}^{′} & =⟨0,\,-{x}^{2},\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 1 & -2xz & 0 \\ 0 & -{x}^{2} & 1\end{aligned}|=⟨-2xz,\,-1,\,-{x}^{2}⟩.\end{aligned}
$$

However, notice that the $j$-component is negative. Therefore, we select the normal vector that points in the *opposite* direction:

$$
{r}_{z}^{′}\times {r}_{x}^{′}=-{r}_{x}^{′}\times {r}_{z}^{′}=⟨2xz,\,1,\,{x}^{2}⟩
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,z))\cdot ({r}_{z}^{′}\times {r}_{x}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,R\,⟩\cdot ⟨2xz,\,1,\,{x}^{2}⟩\,\text{d}A \\  & ={∬}_{D}(2P\,xz+Q+R\,{x}^{2})\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161453 0

For a surface $S$ given by $y=2x{z}^{2}$ for $(x,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\,{z}^{2}+Q+\,xz)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

*Hint: The orientation of $S$ should be chosen such that the unit normal vector has a positive  $j$-component.*

- $2P$ and $-2R$
- $-4P$ and $-4R$
- $-2P$ and $-4R$ (correct)
- $-2P$ and $2R$
- $-4P$ and $2R$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $y=2x{z}^{2},$ it can be parameterized as

$$
r(x,z)=⟨x,\,2x{z}^{2},z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,2{z}^{2},\,0⟩ \\ {r}_{z}^{′} & =⟨0,\,4xz,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 1 & 2{z}^{2} & 0 \\ 0 & 4xz & 1\end{aligned}|=⟨2{z}^{2},\,-1,\,4xz⟩.\end{aligned}
$$

However, notice that the $j$-component is negative. Therefore, we select the normal vector that points in the *opposite* direction:

$$
{r}_{z}^{′}\times {r}_{x}^{′}=-{r}_{x}^{′}\times {r}_{z}^{′}=⟨-2{z}^{2},\,1,\,-4xz⟩
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,z))\cdot ({r}_{z}^{′}\times {r}_{x}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,R\,⟩\cdot ⟨-2{z}^{2},\,1,\,-4xz⟩\,\text{d}A \\  & ={∬}_{D}(-2P\,{z}^{2}+Q+(-4R)\,xz)\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161453 1

For a surface $S$ given by $y=-6{x}^{2}z$ for $(x,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\,xz+Q+\,{x}^{2})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

*Hint: The orientation of $S$ should be chosen such that the unit normal vector has a positive  $j$-component.*

- $12P$ and $6R$ (correct)
- $6P$ and $-12R$
- $-12P$ and $12R$
- $12P$ and $-12R$
- $6P$ and $6R$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $y=-6{x}^{2}z,$ it can be parameterized as

$$
r(x,z)=⟨x,\,-6{x}^{2}z,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,-12xz,\,0⟩ \\ {r}_{z}^{′} & =⟨0,\,-6{x}^{2},\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 1 & -12xz & 0 \\ 0 & -6{x}^{2} & 1\end{aligned}|=⟨-12xz,\,-1,\,-6{x}^{2}⟩.\end{aligned}
$$

However, notice that the $j$-component is negative. Therefore, we select the normal vector that points in the *opposite* direction:

$$
{r}_{z}^{′}\times {r}_{x}^{′}=-{r}_{x}^{′}\times {r}_{z}^{′}=⟨12xz,\,1,\,6{x}^{2}⟩
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,z))\cdot ({r}_{z}^{′}\times {r}_{x}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,R\,⟩\cdot ⟨12xz,\,1,\,6{x}^{2}⟩\,\text{d}A \\  & ={∬}_{D}(12P\,xz+Q+6R\,{x}^{2})\,\text{d}A.\end{aligned}
$$


## Raw original q-161456

For a surface $S$ given by $x=2yz$ for $(y,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(P+\,z+\,y)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $-2Q$ and $R$
- $-2Q$ and $-2R$ (correct)
- $Q$ and $R$
- $Q$ and $-2R$
- $-Q$ and $-R$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $x=2yz,$ it can be parameterized as

$$
r(y,z)=⟨2yz,\,y,\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{y}^{′} & =⟨2z,\,1,\,0⟩ \\ {r}_{z}^{′} & =⟨2y,\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{y}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 2z & 1 & 0 \\ 2y & 0 & 1\end{aligned}|=⟨1,\,-2z,\,-2y⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(y,z))\cdot ({r}_{y}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨1,\,-2z,\,-2y⟩\,\text{d}A \\  & ={∬}_{D}(P+(\,-2Q)\,z+(\,-2R)\,y\,)\,\text{d}A.\end{aligned}
$$

## Original replay q-161456

For a surface $S$ given by $x=2yz$ for $(y,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(P+\,z+\,y)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $Q$ and $R$
- $-2Q$ and $-2R$ (correct)
- $-2Q$ and $R$
- $-Q$ and $-R$
- $Q$ and $-2R$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $x=2yz,$ it can be parameterized as

$$
r(y,z)=⟨2yz,\,y,\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{y}^{′} & =⟨2z,\,1,\,0⟩ \\ {r}_{z}^{′} & =⟨2y,\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{y}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 2z & 1 & 0 \\ 2y & 0 & 1\end{aligned}|=⟨1,\,-2z,\,-2y⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(y,z))\cdot ({r}_{y}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨1,\,-2z,\,-2y⟩\,\text{d}A \\  & ={∬}_{D}(P+(\,-2Q)\,z+(\,-2R)\,y\,)\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161456 0

For a surface $S$ given by $x=2yz$ for $(y,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(P+\,z+\,y)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $Q$ and $-2R$
- $Q$ and $R$
- $-2Q$ and $R$
- $-Q$ and $-R$
- $-2Q$ and $-2R$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $x=2yz,$ it can be parameterized as

$$
r(y,z)=⟨2yz,\,y,\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{y}^{′} & =⟨2z,\,1,\,0⟩ \\ {r}_{z}^{′} & =⟨2y,\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{y}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 2z & 1 & 0 \\ 2y & 0 & 1\end{aligned}|=⟨1,\,-2z,\,-2y⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(y,z))\cdot ({r}_{y}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨1,\,-2z,\,-2y⟩\,\text{d}A \\  & ={∬}_{D}(P+(\,-2Q)\,z+(\,-2R)\,y\,)\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161456 1

For a surface $S$ given by $x=-6yz$ for $(y,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(P+\,z+\,y)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $6Q$ and $R$
- $6Q$ and $6R$ (correct)
- $Q$ and $6R$
- $-Q$ and $-R$
- $Q$ and $R$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $x=-6yz,$ it can be parameterized as

$$
r(y,z)=⟨-6yz,\,y,\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{y}^{′} & =⟨-6z,\,1,\,0⟩ \\ {r}_{z}^{′} & =⟨-6y,\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{y}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ -6z & 1 & 0 \\ -6y & 0 & 1\end{aligned}|=⟨1,\,6z,\,6y⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(y,z))\cdot ({r}_{y}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨1,\,6z,\,6y⟩\,\text{d}A \\  & ={∬}_{D}(P+(\,6Q)\,z+(\,6R)\,y\,)\,\text{d}A.\end{aligned}
$$


## Raw original q-161465

For a surface $S$ given by $x=k(y,z)$ for $(y,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(P-\bbox[3pt,border:1pt solid black]{\phantom{A}}\,\bbox[3pt,border:1pt solid black]{\phantom{A}}-R\,\bbox[3pt,border:1pt solid black]{\phantom{A}})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $-Q,\text{ }\frac{∂k}{∂z},\text{ }\frac{∂k}{∂y}$
- $-Q,\text{ }\frac{∂k}{∂x},\text{ }\frac{∂k}{∂z}$
- $-Q,\text{ }\frac{∂k}{∂y},\text{ }\frac{∂k}{∂z}$
- $Q,\text{ }\frac{∂k}{∂y},\text{ }\frac{∂k}{∂x}$
- $Q,\text{ }\frac{∂k}{∂y},\text{ }\frac{∂k}{∂z}$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $x=k(y,z),$ it can be parameterized as

$$
r(y,z)=⟨k(y,z),\,y,\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{y}^{′} & =⟨\frac{∂k}{∂y},\,1,\,0⟩ \\ {r}_{z}^{′} & =⟨\frac{∂k}{∂z},\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{y}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ \frac{∂k}{∂y} & 1 & 0 \\ \frac{∂k}{∂z} & 0 & 1\end{aligned}|=⟨1,\,-\frac{∂k}{∂y},\,-\frac{∂k}{∂z}⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{y}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨1,\,-\frac{∂k}{∂y},\,-\frac{∂k}{∂z}⟩\,\text{d}A \\  & ={∬}_{D}(P-Q\,\frac{∂k}{∂y}-R\,\frac{∂k}{∂z})\,\text{d}A.\end{aligned}
$$

## Original replay q-161465 (supported solution repair)

For a surface $S$ given by $x=k(y,z)$ for $(y,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(P-\bbox[3pt,border:1pt solid black]{\phantom{A}}\,\bbox[3pt,border:1pt solid black]{\phantom{A}}-R\,\bbox[3pt,border:1pt solid black]{\phantom{A}})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $-Q,\text{ }\frac{∂k}{∂y},\text{ }\frac{∂k}{∂z}$
- $-Q,\text{ }\frac{∂k}{∂x},\text{ }\frac{∂k}{∂z}$
- $-Q,\text{ }\frac{∂k}{∂z},\text{ }\frac{∂k}{∂y}$
- $Q,\text{ }\frac{∂k}{∂y},\text{ }\frac{∂k}{∂z}$ (correct)
- $Q,\text{ }\frac{∂k}{∂y},\text{ }\frac{∂k}{∂x}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $x=k(y,z),$ it can be parameterized as

$$
r(y,z)=⟨k(y,z),\,y,\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{y}^{′} & =⟨\frac{∂k}{∂y},\,1,\,0⟩ \\ {r}_{z}^{′} & =⟨\frac{∂k}{∂z},\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{y}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ \frac{∂k}{∂y} & 1 & 0 \\ \frac{∂k}{∂z} & 0 & 1\end{aligned}|=⟨1,\,-\frac{∂k}{∂y},\,-\frac{∂k}{∂z}⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(y,z))\cdot ({r}_{y}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨1,\,-\frac{∂k}{∂y},\,-\frac{∂k}{∂z}⟩\,\text{d}A \\  & ={∬}_{D}(P-Q\,\frac{∂k}{∂y}-R\,\frac{∂k}{∂z})\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161465 0 (notation alias; finite same formula mask)

For a surface $S$ given by $x=k(y,z)$ for $(y,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(P-\bbox[3pt,border:1pt solid black]{\phantom{A}}\,\bbox[3pt,border:1pt solid black]{\phantom{A}}-R\,\bbox[3pt,border:1pt solid black]{\phantom{A}})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $Q,\text{ }\frac{∂k}{∂y},\text{ }\frac{∂k}{∂x}$
- $Q,\text{ }\frac{∂k}{∂y},\text{ }\frac{∂k}{∂z}$ (correct)
- $-Q,\text{ }\frac{∂k}{∂z},\text{ }\frac{∂k}{∂y}$
- $-Q,\text{ }\frac{∂k}{∂x},\text{ }\frac{∂k}{∂z}$
- $-Q,\text{ }\frac{∂k}{∂y},\text{ }\frac{∂k}{∂z}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $x=k(y,z),$ it can be parameterized as

$$
r(y,z)=⟨k(y,z),\,y,\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{y}^{′} & =⟨\frac{∂k}{∂y},\,1,\,0⟩ \\ {r}_{z}^{′} & =⟨\frac{∂k}{∂z},\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{y}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ \frac{∂k}{∂y} & 1 & 0 \\ \frac{∂k}{∂z} & 0 & 1\end{aligned}|=⟨1,\,-\frac{∂k}{∂y},\,-\frac{∂k}{∂z}⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(y,z))\cdot ({r}_{y}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨1,\,-\frac{∂k}{∂y},\,-\frac{∂k}{∂z}⟩\,\text{d}A \\  & ={∬}_{D}(P-Q\,\frac{∂k}{∂y}-R\,\frac{∂k}{∂z})\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161465 1 (notation alias; finite same formula mask)

For a surface $S$ given by $x=h(y,z)$ for $(y,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(P-\bbox[3pt,border:1pt solid black]{\phantom{A}}\,\bbox[3pt,border:1pt solid black]{\phantom{A}}-R\,\bbox[3pt,border:1pt solid black]{\phantom{A}})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $Q,\text{ }\frac{∂h}{∂y},\text{ }\frac{∂h}{∂z}$ (correct)
- $-Q,\text{ }\frac{∂h}{∂x},\text{ }\frac{∂h}{∂z}$
- $Q,\text{ }\frac{∂h}{∂y},\text{ }\frac{∂h}{∂x}$
- $-Q,\text{ }\frac{∂h}{∂y},\text{ }\frac{∂h}{∂z}$
- $-Q,\text{ }\frac{∂h}{∂z},\text{ }\frac{∂h}{∂y}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $x=h(y,z),$ it can be parameterized as

$$
r(y,z)=⟨h(y,z),\,y,\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{y}^{′} & =⟨\frac{∂h}{∂y},\,1,\,0⟩ \\ {r}_{z}^{′} & =⟨\frac{∂h}{∂z},\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{y}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ \frac{∂h}{∂y} & 1 & 0 \\ \frac{∂h}{∂z} & 0 & 1\end{aligned}|=⟨1,\,-\frac{∂h}{∂y},\,-\frac{∂h}{∂z}⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(y,z))\cdot ({r}_{y}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨1,\,-\frac{∂h}{∂y},\,-\frac{∂h}{∂z}⟩\,\text{d}A \\  & ={∬}_{D}(P-Q\,\frac{∂h}{∂y}-R\,\frac{∂h}{∂z})\,\text{d}A.\end{aligned}
$$


## Raw original q-161460

For a surface $S$ given by $y=h(x,z)$ for $(x,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\,+Q-R\,)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

*Hint: The orientation of $S$ should be chosen such that the unit normal vector has a positive  $j$-component.*

- $P,\,\frac{∂h}{∂z},\,\frac{∂h}{∂x}$
- $-P,\,\frac{∂h}{∂x},\,\frac{∂h}{∂y}$
- $-P,\,\frac{∂h}{∂y},\,\frac{∂h}{∂z}$
- $-P,\,\frac{∂h}{∂x},\,\frac{∂h}{∂z}$ (correct)
- $-P,\,\frac{∂h}{∂y},\,\frac{∂h}{∂x}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $y=h(x,z),$ it can be parameterized as

$$
r(x,z)=⟨x,\,h(x,z),\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,\frac{∂h}{∂x},\,0⟩ \\ {r}_{z}^{′} & =⟨0,\frac{∂h}{∂z},\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 1 & \frac{∂h}{∂x} & 0 \\ 0 & \frac{∂h}{∂z} & 1\end{aligned}|=⟨\frac{∂h}{∂x},\,-1,\,\frac{∂h}{∂z}⟩.\end{aligned}
$$

However, notice that the $j$-component is negative. Therefore, we select the normal vector that points in the *opposite* direction:

$$
{r}_{z}^{′}\times {r}_{x}^{′}=-{r}_{x}^{′}\times {r}_{z}^{′}=⟨-\frac{∂h}{∂x},\,1,\,-\frac{∂h}{∂z}⟩
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,z))\cdot ({r}_{x}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂h}{∂x},\,1,\,-\frac{∂h}{∂z}⟩\,\text{d}A \\  & ={∬}_{D}(-P\,\frac{∂h}{∂x}+Q-R\,\frac{∂h}{∂z})\,\text{d}A.\end{aligned}
$$

## Original replay q-161460 (supported solution repair)

For a surface $S$ given by $y=h(x,z)$ for $(x,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\,+Q-R\,)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

*Hint: The orientation of $S$ should be chosen such that the unit normal vector has a positive  $j$-component.*

- $-P,\,\frac{∂h}{∂y},\,\frac{∂h}{∂z}$
- $-P,\,\frac{∂h}{∂x},\,\frac{∂h}{∂y}$
- $P,\,\frac{∂h}{∂z},\,\frac{∂h}{∂x}$
- $-P,\,\frac{∂h}{∂y},\,\frac{∂h}{∂x}$
- $-P,\,\frac{∂h}{∂x},\,\frac{∂h}{∂z}$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $y=h(x,z),$ it can be parameterized as

$$
r(x,z)=⟨x,\,h(x,z),\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,\frac{∂h}{∂x},\,0⟩ \\ {r}_{z}^{′} & =⟨0,\frac{∂h}{∂z},\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 1 & \frac{∂h}{∂x} & 0 \\ 0 & \frac{∂h}{∂z} & 1\end{aligned}|=⟨\frac{∂h}{∂x},\,-1,\,\frac{∂h}{∂z}⟩.\end{aligned}
$$

However, notice that the $j$-component is negative. Therefore, we select the normal vector that points in the *opposite* direction:

$$
{r}_{z}^{′}\times {r}_{x}^{′}=-{r}_{x}^{′}\times {r}_{z}^{′}=⟨-\frac{∂h}{∂x},\,1,\,-\frac{∂h}{∂z}⟩
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,z))\cdot ({r}_{z}^{′}\times {r}_{x}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂h}{∂x},\,1,\,-\frac{∂h}{∂z}⟩\,\text{d}A \\  & ={∬}_{D}(-P\,\frac{∂h}{∂x}+Q-R\,\frac{∂h}{∂z})\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161460 0 (notation alias; finite same formula mask)

For a surface $S$ given by $y=k(x,z)$ for $(x,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\,+Q-R\,)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

*Hint: The orientation of $S$ should be chosen such that the unit normal vector has a positive  $j$-component.*

- $-P,\,\frac{∂k}{∂x},\,\frac{∂k}{∂z}$ (correct)
- $-P,\,\frac{∂k}{∂y},\,\frac{∂k}{∂x}$
- $P,\,\frac{∂k}{∂z},\,\frac{∂k}{∂x}$
- $-P,\,\frac{∂k}{∂x},\,\frac{∂k}{∂y}$
- $-P,\,\frac{∂k}{∂y},\,\frac{∂k}{∂z}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $y=k(x,z),$ it can be parameterized as

$$
r(x,z)=⟨x,\,k(x,z),\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,\frac{∂k}{∂x},\,0⟩ \\ {r}_{z}^{′} & =⟨0,\frac{∂k}{∂z},\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 1 & \frac{∂k}{∂x} & 0 \\ 0 & \frac{∂k}{∂z} & 1\end{aligned}|=⟨\frac{∂k}{∂x},\,-1,\,\frac{∂k}{∂z}⟩.\end{aligned}
$$

However, notice that the $j$-component is negative. Therefore, we select the normal vector that points in the *opposite* direction:

$$
{r}_{z}^{′}\times {r}_{x}^{′}=-{r}_{x}^{′}\times {r}_{z}^{′}=⟨-\frac{∂k}{∂x},\,1,\,-\frac{∂k}{∂z}⟩
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,z))\cdot ({r}_{z}^{′}\times {r}_{x}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂k}{∂x},\,1,\,-\frac{∂k}{∂z}⟩\,\text{d}A \\  & ={∬}_{D}(-P\,\frac{∂k}{∂x}+Q-R\,\frac{∂k}{∂z})\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161460 1 (notation alias; finite same formula mask)

For a surface $S$ given by $y=h(x,z)$ for $(x,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\,+Q-R\,)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

*Hint: The orientation of $S$ should be chosen such that the unit normal vector has a positive  $j$-component.*

- $-P,\,\frac{∂h}{∂y},\,\frac{∂h}{∂x}$
- $-P,\,\frac{∂h}{∂x},\,\frac{∂h}{∂y}$
- $-P,\,\frac{∂h}{∂x},\,\frac{∂h}{∂z}$ (correct)
- $-P,\,\frac{∂h}{∂y},\,\frac{∂h}{∂z}$
- $P,\,\frac{∂h}{∂z},\,\frac{∂h}{∂x}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $y=h(x,z),$ it can be parameterized as

$$
r(x,z)=⟨x,\,h(x,z),\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,\frac{∂h}{∂x},\,0⟩ \\ {r}_{z}^{′} & =⟨0,\frac{∂h}{∂z},\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 1 & \frac{∂h}{∂x} & 0 \\ 0 & \frac{∂h}{∂z} & 1\end{aligned}|=⟨\frac{∂h}{∂x},\,-1,\,\frac{∂h}{∂z}⟩.\end{aligned}
$$

However, notice that the $j$-component is negative. Therefore, we select the normal vector that points in the *opposite* direction:

$$
{r}_{z}^{′}\times {r}_{x}^{′}=-{r}_{x}^{′}\times {r}_{z}^{′}=⟨-\frac{∂h}{∂x},\,1,\,-\frac{∂h}{∂z}⟩
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,z))\cdot ({r}_{z}^{′}\times {r}_{x}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂h}{∂x},\,1,\,-\frac{∂h}{∂z}⟩\,\text{d}A \\  & ={∬}_{D}(-P\,\frac{∂h}{∂x}+Q-R\,\frac{∂h}{∂z})\,\text{d}A.\end{aligned}
$$


## Raw original q-161455

For a surface $S$ given by $y=2x{z}^{3}$ for $(x,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\bbox[3pt,border:1pt solid black]{\phantom{A}}\,{z}^{3}+Q-\bbox[3pt,border:1pt solid black]{\phantom{A}}\,x{z}^{2})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

*Hint: The orientation of $S$ should be chosen such that the unit normal vector has a positive  $j$-component.*

- $-2R$ and $-2P$
- $P$ and $R$
- $P$ and $-6R$
- $-2P$ and $-R$
- $-2P$ and $6R$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $y=2x{z}^{3},$ it can be parameterized as

$$
r(x,z)=⟨x,\,2x{z}^{3},z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,2{z}^{3},\,0⟩ \\ {r}_{z}^{′} & =⟨0,\,6x{z}^{2},\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 1 & 2{z}^{3} & 0 \\ 0 & 6x{z}^{2} & 1\end{aligned}|=⟨2{z}^{3},\,-1,\,6x{z}^{2}⟩.\end{aligned}
$$

However, notice that the $j$-component is negative. Therefore, we select the normal vector that points in the *opposite* direction:

$$
{r}_{z}^{′}\times {r}_{x}^{′}=-{r}_{x}^{′}\times {r}_{z}^{′}=⟨-2{z}^{3},\,1,\,-6x{z}^{2}⟩
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,z))\cdot ({r}_{z}^{′}\times {r}_{x}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,R\,⟩\cdot ⟨-2{z}^{3},\,1,\,-6x{z}^{2}⟩\,\text{d}A \\  & ={∬}_{D}(-2P\,{z}^{3}+Q-6R\,x{z}^{2}\,)\,\text{d}A.\end{aligned}
$$

## Original replay q-161455

For a surface $S$ given by $y=2x{z}^{3}$ for $(x,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\bbox[3pt,border:1pt solid black]{\phantom{A}}\,{z}^{3}+Q-\bbox[3pt,border:1pt solid black]{\phantom{A}}\,x{z}^{2})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

*Hint: The orientation of $S$ should be chosen such that the unit normal vector has a positive  $j$-component.*

- $P$ and $-6R$
- $P$ and $R$
- $-2R$ and $-2P$
- $-2P$ and $6R$ (correct)
- $-2P$ and $-R$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $y=2x{z}^{3},$ it can be parameterized as

$$
r(x,z)=⟨x,\,2x{z}^{3},z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,2{z}^{3},\,0⟩ \\ {r}_{z}^{′} & =⟨0,\,6x{z}^{2},\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 1 & 2{z}^{3} & 0 \\ 0 & 6x{z}^{2} & 1\end{aligned}|=⟨2{z}^{3},\,-1,\,6x{z}^{2}⟩.\end{aligned}
$$

However, notice that the $j$-component is negative. Therefore, we select the normal vector that points in the *opposite* direction:

$$
{r}_{z}^{′}\times {r}_{x}^{′}=-{r}_{x}^{′}\times {r}_{z}^{′}=⟨-2{z}^{3},\,1,\,-6x{z}^{2}⟩
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,z))\cdot ({r}_{z}^{′}\times {r}_{x}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,R\,⟩\cdot ⟨-2{z}^{3},\,1,\,-6x{z}^{2}⟩\,\text{d}A \\  & ={∬}_{D}(-2P\,{z}^{3}+Q-6R\,x{z}^{2}\,)\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161455 0

For a surface $S$ given by $y=2{x}^{3}z$ for $(x,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\bbox[3pt,border:1pt solid black]{\phantom{A}}\,{x}^{2}z+Q-\bbox[3pt,border:1pt solid black]{\phantom{A}}\,{x}^{3})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

*Hint: The orientation of $S$ should be chosen such that the unit normal vector has a positive  $j$-component.*

- $-6P$ and $-R$
- $P$ and $-2R$
- $-6R$ and $-6P$
- $-6P$ and $2R$ (correct)
- $P$ and $R$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $y=2{x}^{3}z,$ it can be parameterized as

$$
r(x,z)=⟨x,\,2{x}^{3}z,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,6{x}^{2}z,\,0⟩ \\ {r}_{z}^{′} & =⟨0,\,2{x}^{3},\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 1 & 6{x}^{2}z & 0 \\ 0 & 2{x}^{3} & 1\end{aligned}|=⟨6{x}^{2}z,\,-1,\,2{x}^{3}⟩.\end{aligned}
$$

However, notice that the $j$-component is negative. Therefore, we select the normal vector that points in the *opposite* direction:

$$
{r}_{z}^{′}\times {r}_{x}^{′}=-{r}_{x}^{′}\times {r}_{z}^{′}=⟨-6{x}^{2}z,\,1,\,-2{x}^{3}⟩
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,z))\cdot ({r}_{z}^{′}\times {r}_{x}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,R\,⟩\cdot ⟨-6{x}^{2}z,\,1,\,-2{x}^{3}⟩\,\text{d}A \\  & ={∬}_{D}(-6P\,{x}^{2}z+Q-2R\,{x}^{3}\,)\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161455 1

For a surface $S$ given by $y=-6x{z}^{3}$ for $(x,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\bbox[3pt,border:1pt solid black]{\phantom{A}}\,{z}^{3}+Q-\bbox[3pt,border:1pt solid black]{\phantom{A}}\,x{z}^{2})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

*Hint: The orientation of $S$ should be chosen such that the unit normal vector has a positive  $j$-component.*

- $6R$ and $6P$
- $P$ and $R$
- $6P$ and $-R$
- $6P$ and $-18R$ (correct)
- $P$ and $18R$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $y=-6x{z}^{3},$ it can be parameterized as

$$
r(x,z)=⟨x,\,-6x{z}^{3},z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,-6{z}^{3},\,0⟩ \\ {r}_{z}^{′} & =⟨0,\,-18x{z}^{2},\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 1 & -6{z}^{3} & 0 \\ 0 & -18x{z}^{2} & 1\end{aligned}|=⟨-6{z}^{3},\,-1,\,-18x{z}^{2}⟩.\end{aligned}
$$

However, notice that the $j$-component is negative. Therefore, we select the normal vector that points in the *opposite* direction:

$$
{r}_{z}^{′}\times {r}_{x}^{′}=-{r}_{x}^{′}\times {r}_{z}^{′}=⟨6{z}^{3},\,1,\,18x{z}^{2}⟩
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,z))\cdot ({r}_{z}^{′}\times {r}_{x}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,R\,⟩\cdot ⟨6{z}^{3},\,1,\,18x{z}^{2}⟩\,\text{d}A \\  & ={∬}_{D}(6P\,{z}^{3}+Q-(-18R)\,x{z}^{2}\,)\,\text{d}A.\end{aligned}
$$


## Raw original q-161457

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{\bbox[3pt,border:1pt solid black]{\phantom{A}}}{∂x}-\bbox[3pt,border:1pt solid black]{\phantom{A}}\frac{∂g}{\bbox[3pt,border:1pt solid black]{\phantom{A}}}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $∂g,\text{ }-Q,\text{ }∂Q$
- $∂g,\text{ }Q,\text{ }∂z$
- $∂g,\text{ }-Q,\text{ }∂z$
- $∂g,\text{ }-Q,\text{ }∂y$
- $∂g,\text{ }Q,\text{ }∂y$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=g(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,g(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂g}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂g}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂g}{∂x} \\ 0 & 1 & \frac{∂g}{∂y}\end{aligned}|=⟨-\frac{∂g}{∂x},\,-\frac{∂g}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂g}{∂x},\,-\frac{∂g}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\,\text{d}A.\end{aligned}
$$

## Original replay q-161457

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{\bbox[3pt,border:1pt solid black]{\phantom{A}}}{∂x}-\bbox[3pt,border:1pt solid black]{\phantom{A}}\frac{∂g}{\bbox[3pt,border:1pt solid black]{\phantom{A}}}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $∂g,\text{ }-Q,\text{ }∂z$
- $∂g,\text{ }Q,\text{ }∂z$
- $∂g,\text{ }-Q,\text{ }∂Q$
- $∂g,\text{ }Q,\text{ }∂y$ (correct)
- $∂g,\text{ }-Q,\text{ }∂y$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=g(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,g(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂g}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂g}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂g}{∂x} \\ 0 & 1 & \frac{∂g}{∂y}\end{aligned}|=⟨-\frac{∂g}{∂x},\,-\frac{∂g}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂g}{∂x},\,-\frac{∂g}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161457 0 (notation alias; finite same formula mask)

For a surface $S$ given by $z=k(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{\bbox[3pt,border:1pt solid black]{\phantom{A}}}{∂x}-\bbox[3pt,border:1pt solid black]{\phantom{A}}\frac{∂k}{\bbox[3pt,border:1pt solid black]{\phantom{A}}}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $∂k,\text{ }-Q,\text{ }∂y$
- $∂k,\text{ }Q,\text{ }∂y$ (correct)
- $∂k,\text{ }-Q,\text{ }∂Q$
- $∂k,\text{ }Q,\text{ }∂z$
- $∂k,\text{ }-Q,\text{ }∂z$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=k(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,k(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂k}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂k}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂k}{∂x} \\ 0 & 1 & \frac{∂k}{∂y}\end{aligned}|=⟨-\frac{∂k}{∂x},\,-\frac{∂k}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂k}{∂x},\,-\frac{∂k}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂k}{∂x}-Q\frac{∂k}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161457 1 (notation alias; finite same formula mask)

For a surface $S$ given by $z=h(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{\bbox[3pt,border:1pt solid black]{\phantom{A}}}{∂x}-\bbox[3pt,border:1pt solid black]{\phantom{A}}\frac{∂h}{\bbox[3pt,border:1pt solid black]{\phantom{A}}}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $∂h,\text{ }Q,\text{ }∂y$ (correct)
- $∂h,\text{ }Q,\text{ }∂z$
- $∂h,\text{ }-Q,\text{ }∂y$
- $∂h,\text{ }-Q,\text{ }∂z$
- $∂h,\text{ }-Q,\text{ }∂Q$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=h(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,h(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂h}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂h}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂h}{∂x} \\ 0 & 1 & \frac{∂h}{∂y}\end{aligned}|=⟨-\frac{∂h}{∂x},\,-\frac{∂h}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂h}{∂x},\,-\frac{∂h}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂h}{∂x}-Q\frac{∂h}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Raw original q-161463

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂g}{\boxed{}}-Q\frac{∂g}{\boxed{}}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $∂z$ and $∂x$
- $∂x$ and $∂z$
- $∂y$ and $∂z$
- $∂x$ and $∂y$ (correct)
- $∂y$ and $∂x$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=g(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,g(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂g}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂g}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂g}{∂x} \\ 0 & 1 & \frac{∂g}{∂y}\end{aligned}|=⟨-\frac{∂g}{∂x},\,-\frac{∂g}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂g}{∂x},\,-\frac{∂g}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\,\text{d}A.\end{aligned}
$$

## Original replay q-161463

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂g}{\boxed{}}-Q\frac{∂g}{\boxed{}}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $∂y$ and $∂z$
- $∂x$ and $∂z$
- $∂z$ and $∂x$
- $∂y$ and $∂x$
- $∂x$ and $∂y$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=g(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,g(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂g}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂g}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂g}{∂x} \\ 0 & 1 & \frac{∂g}{∂y}\end{aligned}|=⟨-\frac{∂g}{∂x},\,-\frac{∂g}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂g}{∂x},\,-\frac{∂g}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161463 0 (notation alias; finite same formula mask)

For a surface $S$ given by $z=k(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂k}{\boxed{}}-Q\frac{∂k}{\boxed{}}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $∂x$ and $∂y$ (correct)
- $∂y$ and $∂x$
- $∂z$ and $∂x$
- $∂x$ and $∂z$
- $∂y$ and $∂z$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=k(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,k(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂k}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂k}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂k}{∂x} \\ 0 & 1 & \frac{∂k}{∂y}\end{aligned}|=⟨-\frac{∂k}{∂x},\,-\frac{∂k}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂k}{∂x},\,-\frac{∂k}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂k}{∂x}-Q\frac{∂k}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161463 1 (notation alias; finite same formula mask)

For a surface $S$ given by $z=h(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂h}{\boxed{}}-Q\frac{∂h}{\boxed{}}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $∂y$ and $∂x$
- $∂x$ and $∂z$
- $∂x$ and $∂y$ (correct)
- $∂y$ and $∂z$
- $∂z$ and $∂x$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=h(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,h(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂h}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂h}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂h}{∂x} \\ 0 & 1 & \frac{∂h}{∂y}\end{aligned}|=⟨-\frac{∂h}{∂x},\,-\frac{∂h}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂h}{∂x},\,-\frac{∂h}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂h}{∂x}-Q\frac{∂h}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Raw original q-161449

For a surface $S$ given by $z={x}^{2}y$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\bbox[3pt,border:1pt solid black]{\phantom{A}}\,xy+\bbox[3pt,border:1pt solid black]{\phantom{A}}\,{x}^{2}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $-4P$ and $-2Q$
- $-2P$ and $-Q$ (correct)
- $-4Q$ and $P$
- $-2R$ and $Q$
- $P$ and $-R$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z={x}^{2}y,$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,{x}^{2}y⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,2xy⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,{x}^{2}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 2xy \\ 0 & 1 & {x}^{2}\end{aligned}|=⟨-2xy,\,-{x}^{2},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-2xy,\,-{x}^{2},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-2P\,xy+(\,-Q\,)\,{x}^{2}+R)\,\text{d}A.\end{aligned}
$$

## Original replay q-161449

For a surface $S$ given by $z={x}^{2}y$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\bbox[3pt,border:1pt solid black]{\phantom{A}}\,xy+\bbox[3pt,border:1pt solid black]{\phantom{A}}\,{x}^{2}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $-4Q$ and $P$
- $-2P$ and $-Q$ (correct)
- $-4P$ and $-2Q$
- $P$ and $-R$
- $-2R$ and $Q$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z={x}^{2}y,$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,{x}^{2}y⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,2xy⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,{x}^{2}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 2xy \\ 0 & 1 & {x}^{2}\end{aligned}|=⟨-2xy,\,-{x}^{2},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-2xy,\,-{x}^{2},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-2P\,xy+(\,-Q\,)\,{x}^{2}+R)\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161449 0

For a surface $S$ given by $z=2x{y}^{2}$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\bbox[3pt,border:1pt solid black]{\phantom{A}}\,{y}^{2}+\bbox[3pt,border:1pt solid black]{\phantom{A}}\,xy+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $-2R$ and $4Q$
- $-4Q$ and $4P$
- $-4P$ and $-8Q$
- $4P$ and $-4R$
- $-2P$ and $-4Q$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=2x{y}^{2},$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,2x{y}^{2}⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,2{y}^{2}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,4xy⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 2{y}^{2} \\ 0 & 1 & 4xy\end{aligned}|=⟨-2{y}^{2},\,-4xy,\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-2{y}^{2},\,-4xy,\,1⟩\,\text{d}A \\  & ={∬}_{D}(-2P\,{y}^{2}+(\,-4Q\,)\,xy+R)\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-161449 1

For a surface $S$ given by $z=-6{x}^{2}y$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\bbox[3pt,border:1pt solid black]{\phantom{A}}\,xy+\bbox[3pt,border:1pt solid black]{\phantom{A}}\,{x}^{2}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $24P$ and $12Q$
- $12P$ and $6Q$ (correct)
- $12R$ and $-6Q$
- $-6P$ and $6R$
- $24Q$ and $-6P$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=-6{x}^{2}y,$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,-6{x}^{2}y⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,-12xy⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,-6{x}^{2}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -12xy \\ 0 & 1 & -6{x}^{2}\end{aligned}|=⟨12xy,\,6{x}^{2},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨12xy,\,6{x}^{2},\,1⟩\,\text{d}A \\  & ={∬}_{D}(12P\,xy+(\,6Q\,)\,{x}^{2}+R)\,\text{d}A.\end{aligned}
$$


## Raw original q-162607

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂g}{\bbox[3pt,border:1pt solid black]{\phantom{A}}}-Q\frac{\bbox[3pt,border:1pt solid black]{\phantom{A}}}{∂y}+\bbox[3pt,border:1pt solid black]{\phantom{A}})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $∂z,∂g,$ and $-1$
- $∂x,∂g,$ and $-R$
- $∂x,∂g,$ and $1$
- $∂x,∂g,$ and $-1$
- $∂x,∂g,$ and $R$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=g(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,g(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂g}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂g}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂g}{∂x} \\ 0 & 1 & \frac{∂g}{∂y}\end{aligned}|=⟨-\frac{∂g}{∂x},\,-\frac{∂g}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂g}{∂x},\,-\frac{∂g}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\,\text{d}A.\end{aligned}
$$

## Original replay q-162607

For a surface $S$ given by $z=g(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂g}{\bbox[3pt,border:1pt solid black]{\phantom{A}}}-Q\frac{\bbox[3pt,border:1pt solid black]{\phantom{A}}}{∂y}+\bbox[3pt,border:1pt solid black]{\phantom{A}})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $∂x,∂g,$ and $1$
- $∂x,∂g,$ and $-R$
- $∂z,∂g,$ and $-1$
- $∂x,∂g,$ and $R$ (correct)
- $∂x,∂g,$ and $-1$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=g(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,g(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂g}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂g}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂g}{∂x} \\ 0 & 1 & \frac{∂g}{∂y}\end{aligned}|=⟨-\frac{∂g}{∂x},\,-\frac{∂g}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂g}{∂x},\,-\frac{∂g}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂g}{∂x}-Q\frac{∂g}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-162607 0 (notation alias; finite same formula mask)

For a surface $S$ given by $z=k(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂k}{\bbox[3pt,border:1pt solid black]{\phantom{A}}}-Q\frac{\bbox[3pt,border:1pt solid black]{\phantom{A}}}{∂y}+\bbox[3pt,border:1pt solid black]{\phantom{A}})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $∂x,∂k,$ and $-1$
- $∂x,∂k,$ and $R$ (correct)
- $∂z,∂k,$ and $-1$
- $∂x,∂k,$ and $-R$
- $∂x,∂k,$ and $1$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=k(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,k(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂k}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂k}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂k}{∂x} \\ 0 & 1 & \frac{∂k}{∂y}\end{aligned}|=⟨-\frac{∂k}{∂x},\,-\frac{∂k}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂k}{∂x},\,-\frac{∂k}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂k}{∂x}-Q\frac{∂k}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Generated observed profile q-162607 1 (notation alias; finite same formula mask)

For a surface $S$ given by $z=h(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂h}{\bbox[3pt,border:1pt solid black]{\phantom{A}}}-Q\frac{\bbox[3pt,border:1pt solid black]{\phantom{A}}}{∂y}+\bbox[3pt,border:1pt solid black]{\phantom{A}})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $∂x,∂h,$ and $R$ (correct)
- $∂x,∂h,$ and $-R$
- $∂x,∂h,$ and $-1$
- $∂x,∂h,$ and $1$
- $∂z,∂h,$ and $-1$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=h(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,h(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂h}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂h}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂h}{∂x} \\ 0 & 1 & \frac{∂h}{∂y}\end{aligned}|=⟨-\frac{∂h}{∂x},\,-\frac{∂h}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂h}{∂x},\,-\frac{∂h}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂h}{∂x}-Q\frac{∂h}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161166 0 (notation alias; finite same formula mask)

For a surface $S$ given by $z=f(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\bbox[3pt,border:1pt solid black]{\phantom{A}}\frac{\bbox[3pt,border:1pt solid black]{\phantom{A}}}{∂x}-Q\frac{∂f}{\bbox[3pt,border:1pt solid black]{\phantom{A}}}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $-P,\,$ $∂f,\,$ $∂y$ (correct)
- $-P,\,$ $∂f,\,$ $∂x$
- $P,\,$ $∂f,\,$ $∂x$
- $-P,\,$ $∂P,\,$ $∂x$
- $P,\,$ $∂f,\,$ $∂y$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=f(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,f(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂f}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂f}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂f}{∂x} \\ 0 & 1 & \frac{∂f}{∂y}\end{aligned}|=⟨-\frac{∂f}{∂x},\,-\frac{∂f}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂f}{∂x},\,-\frac{∂f}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂f}{∂x}-Q\frac{∂f}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161166 1 (notation alias; finite same formula mask)

For a surface $S$ given by $z=h(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\bbox[3pt,border:1pt solid black]{\phantom{A}}\frac{\bbox[3pt,border:1pt solid black]{\phantom{A}}}{∂x}-Q\frac{∂h}{\bbox[3pt,border:1pt solid black]{\phantom{A}}}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $-P,\,$ $∂h,\,$ $∂x$
- $P,\,$ $∂h,\,$ $∂y$
- $P,\,$ $∂h,\,$ $∂x$
- $-P,\,$ $∂P,\,$ $∂x$
- $-P,\,$ $∂h,\,$ $∂y$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=h(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,h(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂h}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂h}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂h}{∂x} \\ 0 & 1 & \frac{∂h}{∂y}\end{aligned}|=⟨-\frac{∂h}{∂x},\,-\frac{∂h}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂h}{∂x},\,-\frac{∂h}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂h}{∂x}-Q\frac{∂h}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161189 0 (notation alias; finite same formula mask)

For a surface $S$ given by $z=f(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\bbox[3pt,border:1pt solid black]{\phantom{A}}\frac{∂f}{∂x}+\bbox[3pt,border:1pt solid black]{\phantom{A}}\frac{∂f}{∂y}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $-P$ and $-Q$ (correct)
- $Q$ and $P$
- $-P$ and $Q$
- $P$ and $Q$
- $P$ and $-Q$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=f(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,f(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂f}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂f}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂f}{∂x} \\ 0 & 1 & \frac{∂f}{∂y}\end{aligned}|=⟨-\frac{∂f}{∂x},\,-\frac{∂f}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂f}{∂x},\,-\frac{∂f}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂f}{∂x}+(-Q\,)\frac{∂f}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161189 1 (notation alias; finite same formula mask)

For a surface $S$ given by $z=h(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\bbox[3pt,border:1pt solid black]{\phantom{A}}\frac{∂h}{∂x}+\bbox[3pt,border:1pt solid black]{\phantom{A}}\frac{∂h}{∂y}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $Q$ and $P$
- $P$ and $-Q$
- $-P$ and $Q$
- $P$ and $Q$
- $-P$ and $-Q$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=h(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,h(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂h}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂h}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂h}{∂x} \\ 0 & 1 & \frac{∂h}{∂y}\end{aligned}|=⟨-\frac{∂h}{∂x},\,-\frac{∂h}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂h}{∂x},\,-\frac{∂h}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂h}{∂x}+(-Q\,)\frac{∂h}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161446 0 (notation alias; finite same formula mask)

For a surface $S$ given by $x=f(y,z)$ for $(y,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(P+\bbox[3pt,border:1pt solid black]{\phantom{A}}\frac{∂f}{∂y}-R\frac{∂f}{\bbox[3pt,border:1pt solid black]{\phantom{A}}})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $-R$ and $∂z$
- $Q$ and $∂x$
- $-Q$ and $∂x$
- $-Q$ and $∂z$ (correct)
- $Q$ and $∂z$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $x=f(y,z),$ it can be parameterized as

$$
r(y,z)=⟨f(y,z),\,y,\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{y}^{′} & =⟨\frac{∂f}{∂y},\,1,\,0⟩ \\ {r}_{z}^{′} & =⟨\frac{∂f}{∂z},\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{y}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ \frac{∂f}{∂y} & 1 & 0 \\ \frac{∂f}{∂z} & 0 & 1\end{aligned}|=⟨1,\,-\frac{∂f}{∂y},\,-\frac{∂f}{∂z}⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(y,z))\cdot ({r}_{y}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨1,\,-\frac{∂f}{∂y},\,-\frac{∂f}{∂z}⟩\,\text{d}A \\  & ={∬}_{D}(P+(-Q\,)\frac{∂f}{∂y}-R\frac{∂f}{∂z})\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161446 1 (notation alias; finite same formula mask)

For a surface $S$ given by $x=h(y,z)$ for $(y,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(P+\bbox[3pt,border:1pt solid black]{\phantom{A}}\frac{∂h}{∂y}-R\frac{∂h}{\bbox[3pt,border:1pt solid black]{\phantom{A}}})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $Q$ and $∂x$
- $Q$ and $∂z$
- $-Q$ and $∂x$
- $-Q$ and $∂z$ (correct)
- $-R$ and $∂z$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $x=h(y,z),$ it can be parameterized as

$$
r(y,z)=⟨h(y,z),\,y,\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{y}^{′} & =⟨\frac{∂h}{∂y},\,1,\,0⟩ \\ {r}_{z}^{′} & =⟨\frac{∂h}{∂z},\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{y}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ \frac{∂h}{∂y} & 1 & 0 \\ \frac{∂h}{∂z} & 0 & 1\end{aligned}|=⟨1,\,-\frac{∂h}{∂y},\,-\frac{∂h}{∂z}⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(y,z))\cdot ({r}_{y}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨1,\,-\frac{∂h}{∂y},\,-\frac{∂h}{∂z}⟩\,\text{d}A \\  & ={∬}_{D}(P+(-Q\,)\frac{∂h}{∂y}-R\frac{∂h}{∂z})\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161453 0

For a surface $S$ given by $y=5x{z}^{2}$ for $(x,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\bbox[3pt,border:1pt solid black]{\phantom{A}}\,{z}^{2}+Q+\bbox[3pt,border:1pt solid black]{\phantom{A}}\,xz)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

*Hint: The orientation of $S$ should be chosen such that the unit normal vector has a positive  $j$-component.*

- $-5P$ and $5R$
- $-10P$ and $5R$
- $5P$ and $-5R$
- $-10P$ and $-10R$
- $-5P$ and $-10R$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $y=5x{z}^{2},$ it can be parameterized as

$$
r(x,z)=⟨x,\,5x{z}^{2},z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,5{z}^{2},\,0⟩ \\ {r}_{z}^{′} & =⟨0,\,10xz,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 1 & 5{z}^{2} & 0 \\ 0 & 10xz & 1\end{aligned}|=⟨5{z}^{2},\,-1,\,10xz⟩.\end{aligned}
$$

However, notice that the $j$-component is negative. Therefore, we select the normal vector that points in the *opposite* direction:

$$
{r}_{z}^{′}\times {r}_{x}^{′}=-{r}_{x}^{′}\times {r}_{z}^{′}=⟨-5{z}^{2},\,1,\,-10xz⟩
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,z))\cdot ({r}_{z}^{′}\times {r}_{x}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,R\,⟩\cdot ⟨-5{z}^{2},\,1,\,-10xz⟩\,\text{d}A \\  & ={∬}_{D}(-5P\,{z}^{2}+Q+(-10R)\,xz)\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161453 1

For a surface $S$ given by $y=-7{x}^{2}z$ for $(x,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\bbox[3pt,border:1pt solid black]{\phantom{A}}\,xz+Q+\bbox[3pt,border:1pt solid black]{\phantom{A}}\,{x}^{2})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

*Hint: The orientation of $S$ should be chosen such that the unit normal vector has a positive  $j$-component.*

- $-14P$ and $14R$
- $14P$ and $-14R$
- $7P$ and $-14R$
- $14P$ and $7R$ (correct)
- $7P$ and $7R$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $y=-7{x}^{2}z,$ it can be parameterized as

$$
r(x,z)=⟨x,\,-7{x}^{2}z,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,-14xz,\,0⟩ \\ {r}_{z}^{′} & =⟨0,\,-7{x}^{2},\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 1 & -14xz & 0 \\ 0 & -7{x}^{2} & 1\end{aligned}|=⟨-14xz,\,-1,\,-7{x}^{2}⟩.\end{aligned}
$$

However, notice that the $j$-component is negative. Therefore, we select the normal vector that points in the *opposite* direction:

$$
{r}_{z}^{′}\times {r}_{x}^{′}=-{r}_{x}^{′}\times {r}_{z}^{′}=⟨14xz,\,1,\,7{x}^{2}⟩
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,z))\cdot ({r}_{z}^{′}\times {r}_{x}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,R\,⟩\cdot ⟨14xz,\,1,\,7{x}^{2}⟩\,\text{d}A \\  & ={∬}_{D}(14P\,xz+Q+7R\,{x}^{2})\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161456 0

For a surface $S$ given by $x=5yz$ for $(y,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(P+\bbox[3pt,border:1pt solid black]{\phantom{A}}\,z+\bbox[3pt,border:1pt solid black]{\phantom{A}}\,y)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $-Q$ and $-R$
- $-5Q$ and $-5R$ (correct)
- $Q$ and $-5R$
- $Q$ and $R$
- $-5Q$ and $R$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $x=5yz,$ it can be parameterized as

$$
r(y,z)=⟨5yz,\,y,\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{y}^{′} & =⟨5z,\,1,\,0⟩ \\ {r}_{z}^{′} & =⟨5y,\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{y}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 5z & 1 & 0 \\ 5y & 0 & 1\end{aligned}|=⟨1,\,-5z,\,-5y⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(y,z))\cdot ({r}_{y}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨1,\,-5z,\,-5y⟩\,\text{d}A \\  & ={∬}_{D}(P+(\,-5Q)\,z+(\,-5R)\,y\,)\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161456 1

For a surface $S$ given by $x=-7yz$ for $(y,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(P+\bbox[3pt,border:1pt solid black]{\phantom{A}}\,z+\bbox[3pt,border:1pt solid black]{\phantom{A}}\,y)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $Q$ and $7R$
- $-Q$ and $-R$
- $7Q$ and $7R$ (correct)
- $7Q$ and $R$
- $Q$ and $R$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $x=-7yz,$ it can be parameterized as

$$
r(y,z)=⟨-7yz,\,y,\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{y}^{′} & =⟨-7z,\,1,\,0⟩ \\ {r}_{z}^{′} & =⟨-7y,\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{y}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ -7z & 1 & 0 \\ -7y & 0 & 1\end{aligned}|=⟨1,\,7z,\,7y⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(y,z))\cdot ({r}_{y}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨1,\,7z,\,7y⟩\,\text{d}A \\  & ={∬}_{D}(P+(\,7Q)\,z+(\,7R)\,y\,)\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161465 0 (notation alias; finite same formula mask)

For a surface $S$ given by $x=f(y,z)$ for $(y,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(P-\bbox[3pt,border:1pt solid black]{\phantom{A}}\,\bbox[3pt,border:1pt solid black]{\phantom{A}}-R\,\bbox[3pt,border:1pt solid black]{\phantom{A}})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $Q,\text{ }\frac{∂f}{∂y},\text{ }\frac{∂f}{∂z}$ (correct)
- $-Q,\text{ }\frac{∂f}{∂y},\text{ }\frac{∂f}{∂z}$
- $-Q,\text{ }\frac{∂f}{∂x},\text{ }\frac{∂f}{∂z}$
- $-Q,\text{ }\frac{∂f}{∂z},\text{ }\frac{∂f}{∂y}$
- $Q,\text{ }\frac{∂f}{∂y},\text{ }\frac{∂f}{∂x}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $x=f(y,z),$ it can be parameterized as

$$
r(y,z)=⟨f(y,z),\,y,\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{y}^{′} & =⟨\frac{∂f}{∂y},\,1,\,0⟩ \\ {r}_{z}^{′} & =⟨\frac{∂f}{∂z},\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{y}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ \frac{∂f}{∂y} & 1 & 0 \\ \frac{∂f}{∂z} & 0 & 1\end{aligned}|=⟨1,\,-\frac{∂f}{∂y},\,-\frac{∂f}{∂z}⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(y,z))\cdot ({r}_{y}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨1,\,-\frac{∂f}{∂y},\,-\frac{∂f}{∂z}⟩\,\text{d}A \\  & ={∬}_{D}(P-Q\,\frac{∂f}{∂y}-R\,\frac{∂f}{∂z})\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161465 1 (notation alias; finite same formula mask)

For a surface $S$ given by $x=h(y,z)$ for $(y,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(P-\bbox[3pt,border:1pt solid black]{\phantom{A}}\,\bbox[3pt,border:1pt solid black]{\phantom{A}}-R\,\bbox[3pt,border:1pt solid black]{\phantom{A}})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $-Q,\text{ }\frac{∂h}{∂y},\text{ }\frac{∂h}{∂z}$
- $Q,\text{ }\frac{∂h}{∂y},\text{ }\frac{∂h}{∂x}$
- $-Q,\text{ }\frac{∂h}{∂x},\text{ }\frac{∂h}{∂z}$
- $-Q,\text{ }\frac{∂h}{∂z},\text{ }\frac{∂h}{∂y}$
- $Q,\text{ }\frac{∂h}{∂y},\text{ }\frac{∂h}{∂z}$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $x=h(y,z),$ it can be parameterized as

$$
r(y,z)=⟨h(y,z),\,y,\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{y}^{′} & =⟨\frac{∂h}{∂y},\,1,\,0⟩ \\ {r}_{z}^{′} & =⟨\frac{∂h}{∂z},\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{y}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ \frac{∂h}{∂y} & 1 & 0 \\ \frac{∂h}{∂z} & 0 & 1\end{aligned}|=⟨1,\,-\frac{∂h}{∂y},\,-\frac{∂h}{∂z}⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(y,z))\cdot ({r}_{y}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨1,\,-\frac{∂h}{∂y},\,-\frac{∂h}{∂z}⟩\,\text{d}A \\  & ={∬}_{D}(P-Q\,\frac{∂h}{∂y}-R\,\frac{∂h}{∂z})\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161460 0 (notation alias; finite same formula mask)

For a surface $S$ given by $y=f(x,z)$ for $(x,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\bbox[3pt,border:1pt solid black]{\phantom{A}}\bbox[3pt,border:1pt solid black]{\phantom{A}}+Q-R\bbox[3pt,border:1pt solid black]{\phantom{A}}\,)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

*Hint: The orientation of $S$ should be chosen such that the unit normal vector has a positive  $j$-component.*

- $-P,\,\frac{∂f}{∂y},\,\frac{∂f}{∂x}$
- $-P,\,\frac{∂f}{∂y},\,\frac{∂f}{∂z}$
- $-P,\,\frac{∂f}{∂x},\,\frac{∂f}{∂y}$
- $P,\,\frac{∂f}{∂z},\,\frac{∂f}{∂x}$
- $-P,\,\frac{∂f}{∂x},\,\frac{∂f}{∂z}$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $y=f(x,z),$ it can be parameterized as

$$
r(x,z)=⟨x,\,f(x,z),\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,\frac{∂f}{∂x},\,0⟩ \\ {r}_{z}^{′} & =⟨0,\frac{∂f}{∂z},\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 1 & \frac{∂f}{∂x} & 0 \\ 0 & \frac{∂f}{∂z} & 1\end{aligned}|=⟨\frac{∂f}{∂x},\,-1,\,\frac{∂f}{∂z}⟩.\end{aligned}
$$

However, notice that the $j$-component is negative. Therefore, we select the normal vector that points in the *opposite* direction:

$$
{r}_{z}^{′}\times {r}_{x}^{′}=-{r}_{x}^{′}\times {r}_{z}^{′}=⟨-\frac{∂f}{∂x},\,1,\,-\frac{∂f}{∂z}⟩
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,z))\cdot ({r}_{z}^{′}\times {r}_{x}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂f}{∂x},\,1,\,-\frac{∂f}{∂z}⟩\,\text{d}A \\  & ={∬}_{D}(-P\,\frac{∂f}{∂x}+Q-R\,\frac{∂f}{∂z})\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161460 1 (notation alias; finite same formula mask)

For a surface $S$ given by $y=h(x,z)$ for $(x,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\bbox[3pt,border:1pt solid black]{\phantom{A}}\bbox[3pt,border:1pt solid black]{\phantom{A}}+Q-R\bbox[3pt,border:1pt solid black]{\phantom{A}}\,)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

*Hint: The orientation of $S$ should be chosen such that the unit normal vector has a positive  $j$-component.*

- $-P,\,\frac{∂h}{∂y},\,\frac{∂h}{∂z}$
- $-P,\,\frac{∂h}{∂x},\,\frac{∂h}{∂z}$ (correct)
- $-P,\,\frac{∂h}{∂x},\,\frac{∂h}{∂y}$
- $P,\,\frac{∂h}{∂z},\,\frac{∂h}{∂x}$
- $-P,\,\frac{∂h}{∂y},\,\frac{∂h}{∂x}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $y=h(x,z),$ it can be parameterized as

$$
r(x,z)=⟨x,\,h(x,z),\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,\frac{∂h}{∂x},\,0⟩ \\ {r}_{z}^{′} & =⟨0,\frac{∂h}{∂z},\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 1 & \frac{∂h}{∂x} & 0 \\ 0 & \frac{∂h}{∂z} & 1\end{aligned}|=⟨\frac{∂h}{∂x},\,-1,\,\frac{∂h}{∂z}⟩.\end{aligned}
$$

However, notice that the $j$-component is negative. Therefore, we select the normal vector that points in the *opposite* direction:

$$
{r}_{z}^{′}\times {r}_{x}^{′}=-{r}_{x}^{′}\times {r}_{z}^{′}=⟨-\frac{∂h}{∂x},\,1,\,-\frac{∂h}{∂z}⟩
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,z))\cdot ({r}_{z}^{′}\times {r}_{x}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂h}{∂x},\,1,\,-\frac{∂h}{∂z}⟩\,\text{d}A \\  & ={∬}_{D}(-P\,\frac{∂h}{∂x}+Q-R\,\frac{∂h}{∂z})\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161455 0

For a surface $S$ given by $y=5{x}^{3}z$ for $(x,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\bbox[3pt,border:1pt solid black]{\phantom{A}}\,{x}^{2}z+Q-\bbox[3pt,border:1pt solid black]{\phantom{A}}\,{x}^{3})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

*Hint: The orientation of $S$ should be chosen such that the unit normal vector has a positive  $j$-component.*

- $-15P$ and $5R$ (correct)
- $P$ and $R$
- $-15P$ and $-R$
- $P$ and $-5R$
- $-15R$ and $-15P$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $y=5{x}^{3}z,$ it can be parameterized as

$$
r(x,z)=⟨x,\,5{x}^{3}z,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,15{x}^{2}z,\,0⟩ \\ {r}_{z}^{′} & =⟨0,\,5{x}^{3},\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 1 & 15{x}^{2}z & 0 \\ 0 & 5{x}^{3} & 1\end{aligned}|=⟨15{x}^{2}z,\,-1,\,5{x}^{3}⟩.\end{aligned}
$$

However, notice that the $j$-component is negative. Therefore, we select the normal vector that points in the *opposite* direction:

$$
{r}_{z}^{′}\times {r}_{x}^{′}=-{r}_{x}^{′}\times {r}_{z}^{′}=⟨-15{x}^{2}z,\,1,\,-5{x}^{3}⟩
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,z))\cdot ({r}_{z}^{′}\times {r}_{x}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,R\,⟩\cdot ⟨-15{x}^{2}z,\,1,\,-5{x}^{3}⟩\,\text{d}A \\  & ={∬}_{D}(-15P\,{x}^{2}z+Q-5R\,{x}^{3}\,)\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161455 1

For a surface $S$ given by $y=-7x{z}^{3}$ for $(x,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\bbox[3pt,border:1pt solid black]{\phantom{A}}\,{z}^{3}+Q-\bbox[3pt,border:1pt solid black]{\phantom{A}}\,x{z}^{2})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

*Hint: The orientation of $S$ should be chosen such that the unit normal vector has a positive  $j$-component.*

- $7P$ and $-R$
- $7P$ and $-21R$ (correct)
- $P$ and $R$
- $7R$ and $7P$
- $P$ and $21R$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $y=-7x{z}^{3},$ it can be parameterized as

$$
r(x,z)=⟨x,\,-7x{z}^{3},z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,-7{z}^{3},\,0⟩ \\ {r}_{z}^{′} & =⟨0,\,-21x{z}^{2},\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 1 & -7{z}^{3} & 0 \\ 0 & -21x{z}^{2} & 1\end{aligned}|=⟨-7{z}^{3},\,-1,\,-21x{z}^{2}⟩.\end{aligned}
$$

However, notice that the $j$-component is negative. Therefore, we select the normal vector that points in the *opposite* direction:

$$
{r}_{z}^{′}\times {r}_{x}^{′}=-{r}_{x}^{′}\times {r}_{z}^{′}=⟨7{z}^{3},\,1,\,21x{z}^{2}⟩
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,z))\cdot ({r}_{z}^{′}\times {r}_{x}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,R\,⟩\cdot ⟨7{z}^{3},\,1,\,21x{z}^{2}⟩\,\text{d}A \\  & ={∬}_{D}(7P\,{z}^{3}+Q-(-21R)\,x{z}^{2}\,)\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161457 0 (notation alias; finite same formula mask)

For a surface $S$ given by $z=f(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{\bbox[3pt,border:1pt solid black]{\phantom{A}}}{∂x}-\bbox[3pt,border:1pt solid black]{\phantom{A}}\frac{∂f}{\bbox[3pt,border:1pt solid black]{\phantom{A}}}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $∂f,\text{ }Q,\text{ }∂y$ (correct)
- $∂f,\text{ }-Q,\text{ }∂z$
- $∂f,\text{ }Q,\text{ }∂z$
- $∂f,\text{ }-Q,\text{ }∂Q$
- $∂f,\text{ }-Q,\text{ }∂y$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=f(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,f(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂f}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂f}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂f}{∂x} \\ 0 & 1 & \frac{∂f}{∂y}\end{aligned}|=⟨-\frac{∂f}{∂x},\,-\frac{∂f}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂f}{∂x},\,-\frac{∂f}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂f}{∂x}-Q\frac{∂f}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161457 1 (notation alias; finite same formula mask)

For a surface $S$ given by $z=h(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{\bbox[3pt,border:1pt solid black]{\phantom{A}}}{∂x}-\bbox[3pt,border:1pt solid black]{\phantom{A}}\frac{∂h}{\bbox[3pt,border:1pt solid black]{\phantom{A}}}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $∂h,\text{ }-Q,\text{ }∂z$
- $∂h,\text{ }-Q,\text{ }∂y$
- $∂h,\text{ }Q,\text{ }∂z$
- $∂h,\text{ }-Q,\text{ }∂Q$
- $∂h,\text{ }Q,\text{ }∂y$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=h(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,h(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂h}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂h}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂h}{∂x} \\ 0 & 1 & \frac{∂h}{∂y}\end{aligned}|=⟨-\frac{∂h}{∂x},\,-\frac{∂h}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂h}{∂x},\,-\frac{∂h}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂h}{∂x}-Q\frac{∂h}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161463 0 (notation alias; finite same formula mask)

For a surface $S$ given by $z=f(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂f}{\boxed{}}-Q\frac{∂f}{\boxed{}}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $∂y$ and $∂x$
- $∂y$ and $∂z$
- $∂x$ and $∂z$
- $∂z$ and $∂x$
- $∂x$ and $∂y$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=f(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,f(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂f}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂f}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂f}{∂x} \\ 0 & 1 & \frac{∂f}{∂y}\end{aligned}|=⟨-\frac{∂f}{∂x},\,-\frac{∂f}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂f}{∂x},\,-\frac{∂f}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂f}{∂x}-Q\frac{∂f}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161463 1 (notation alias; finite same formula mask)

For a surface $S$ given by $z=h(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂h}{\boxed{}}-Q\frac{∂h}{\boxed{}}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $∂y$ and $∂z$
- $∂x$ and $∂y$ (correct)
- $∂x$ and $∂z$
- $∂z$ and $∂x$
- $∂y$ and $∂x$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=h(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,h(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂h}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂h}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂h}{∂x} \\ 0 & 1 & \frac{∂h}{∂y}\end{aligned}|=⟨-\frac{∂h}{∂x},\,-\frac{∂h}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂h}{∂x},\,-\frac{∂h}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂h}{∂x}-Q\frac{∂h}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161449 0

For a surface $S$ given by $z=5x{y}^{2}$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\bbox[3pt,border:1pt solid black]{\phantom{A}}\,{y}^{2}+\bbox[3pt,border:1pt solid black]{\phantom{A}}\,xy+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $10P$ and $-10R$
- $-5P$ and $-10Q$ (correct)
- $-5R$ and $10Q$
- $-10Q$ and $10P$
- $-10P$ and $-20Q$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=5x{y}^{2},$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,5x{y}^{2}⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,5{y}^{2}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,10xy⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 5{y}^{2} \\ 0 & 1 & 10xy\end{aligned}|=⟨-5{y}^{2},\,-10xy,\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-5{y}^{2},\,-10xy,\,1⟩\,\text{d}A \\  & ={∬}_{D}(-5P\,{y}^{2}+(\,-10Q\,)\,xy+R)\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-161449 1

For a surface $S$ given by $z=-7{x}^{2}y$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(\bbox[3pt,border:1pt solid black]{\phantom{A}}\,xy+\bbox[3pt,border:1pt solid black]{\phantom{A}}\,{x}^{2}+R)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $14R$ and $-7Q$
- $-7P$ and $7R$
- $14P$ and $7Q$ (correct)
- $28P$ and $14Q$
- $28Q$ and $-7P$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=-7{x}^{2}y,$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,-7{x}^{2}y⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,-14xy⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,-7{x}^{2}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -14xy \\ 0 & 1 & -7{x}^{2}\end{aligned}|=⟨14xy,\,7{x}^{2},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨14xy,\,7{x}^{2},\,1⟩\,\text{d}A \\  & ={∬}_{D}(14P\,xy+(\,7Q\,)\,{x}^{2}+R)\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-162607 0 (notation alias; finite same formula mask)

For a surface $S$ given by $z=f(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂f}{\bbox[3pt,border:1pt solid black]{\phantom{A}}}-Q\frac{\bbox[3pt,border:1pt solid black]{\phantom{A}}}{∂y}+\bbox[3pt,border:1pt solid black]{\phantom{A}})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $∂x,∂f,$ and $R$ (correct)
- $∂x,∂f,$ and $1$
- $∂x,∂f,$ and $-R$
- $∂z,∂f,$ and $-1$
- $∂x,∂f,$ and $-1$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=f(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,f(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂f}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂f}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂f}{∂x} \\ 0 & 1 & \frac{∂f}{∂y}\end{aligned}|=⟨-\frac{∂f}{∂x},\,-\frac{∂f}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂f}{∂x},\,-\frac{∂f}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂f}{∂x}-Q\frac{∂f}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Generated authored variant q-162607 1 (notation alias; finite same formula mask)

For a surface $S$ given by $z=h(x,y)$ for $(x,y)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(-P\frac{∂h}{\bbox[3pt,border:1pt solid black]{\phantom{A}}}-Q\frac{\bbox[3pt,border:1pt solid black]{\phantom{A}}}{∂y}+\bbox[3pt,border:1pt solid black]{\phantom{A}})\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $∂x,∂h,$ and $1$
- $∂x,∂h,$ and $-1$
- $∂x,∂h,$ and $-R$
- $∂z,∂h,$ and $-1$
- $∂x,∂h,$ and $R$ (correct)

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $z=h(x,y),$ it can be parameterized as

$$
r(x,y)=⟨x,\,y,\,h(x,y)⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{x}^{′} & =⟨1,\,0,\,\frac{∂h}{∂x}⟩ \\ {r}_{y}^{′} & =⟨0,\,1,\,\frac{∂h}{∂y}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{x}^{′}\times {r}_{y}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & \frac{∂h}{∂x} \\ 0 & 1 & \frac{∂h}{∂y}\end{aligned}|=⟨-\frac{∂h}{∂x},\,-\frac{∂h}{∂y},\,1⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(x,y))\cdot ({r}_{x}^{′}\times {r}_{y}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨-\frac{∂h}{∂x},\,-\frac{∂h}{∂y},\,1⟩\,\text{d}A \\  & ={∬}_{D}(-P\frac{∂h}{∂x}-Q\frac{∂h}{∂y}+R)\,\text{d}A.\end{aligned}
$$


## Generated authored shifted bilinear 0

For a surface $S$ given by $x=5z\left(y+2\right)+2$ for $(y,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(P+\bbox[3pt,border:1pt solid black]{\phantom{A}}\,z+\bbox[3pt,border:1pt solid black]{\phantom{A}}\,(y+2))\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $-5Q$ and $R$
- $Q$ and $R$
- $-5Q$ and $-5R$ (correct)
- $-Q$ and $-R$
- $Q$ and $-5R$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $x=5z\left(y+2\right)+2,$ it can be parameterized as

$$
r(y,z)=⟨5z\left(y+2\right)+2,\,y,\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{y}^{′} & =⟨5z,\,1,\,0⟩ \\ {r}_{z}^{′} & =⟨5y+10,\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{y}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ 5z & 1 & 0 \\ 5y+10 & 0 & 1\end{aligned}|=⟨1,\,-5z,\,-5y-10⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(y,z))\cdot ({r}_{y}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨1,\,-5z,\,-5y-10⟩\,\text{d}A \\  & ={∬}_{D}(P+(\,-5Q)\,z+(\,-5R)\,(y+2)\,)\,\text{d}A.\end{aligned}
$$


## Generated authored shifted bilinear 1

For a surface $S$ given by $x=-7y\left(z+2\right)+1$ for $(y,z)\in D,$ the flux of the vector field $F(x,y,z)=⟨P,\,Q,\,R⟩$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{D}(P+\bbox[3pt,border:1pt solid black]{\phantom{A}}\,(z+2)+\bbox[3pt,border:1pt solid black]{\phantom{A}}\,y)\,\text{d}A.
$$

From left to right, what are the missing parts of the formula?

- $7Q$ and $R$
- $7Q$ and $7R$ (correct)
- $Q$ and $R$
- $-Q$ and $-R$
- $Q$ and $7R$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the flux of a vector field $F$ over $S$ is given by

$$
{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.
$$

Since our surface $S$ is of the form $x=-7y\left(z+2\right)+1,$ it can be parameterized as

$$
r(y,z)=⟨-7y\left(z+2\right)+1,\,y,\,z⟩.
$$

We now compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{y}^{′} & =⟨-7z-14,\,1,\,0⟩ \\ {r}_{z}^{′} & =⟨-7y,\,0,\,1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{y}^{′}\times {r}_{z}^{′} & =|\begin{aligned}i & j & k \\ -7z-14 & 1 & 0 \\ -7y & 0 & 1\end{aligned}|=⟨1,\,7z+14,\,7y⟩.\end{aligned}
$$

Therefore, the surface integral can be written as

$$
\begin{aligned}{∬}_{S}F\cdot \text{d}S & ={∬}_{D}F(r(y,z))\cdot ({r}_{y}^{′}\times {r}_{z}^{′})\,\text{d}A \\  & ={∬}_{D}⟨P,\,Q,\,R⟩\cdot ⟨1,\,7z+14,\,7y⟩\,\text{d}A \\  & ={∬}_{D}(P+(\,7Q)\,(z+2)+(\,7R)\,y\,)\,\text{d}A.\end{aligned}
$$
