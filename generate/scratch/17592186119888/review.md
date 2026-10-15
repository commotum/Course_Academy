## q-105920

Source

Find the surface area of the parametric surface defined by the equations 

$$
x=2u-v,\,y=3u+2,\,z=u+2v
$$

for $0\le u\le 1$ and $-1\le v\le 1.$

- [x] $2\sqrt{70}$
- [ ] $20$
- [ ] $\sqrt{30}$
- [ ] $10$
- [ ] $\sqrt{35}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

In vector form, our surface has the equation 

$$
r(u,v)=⟨2u-v,\,3u+2,\,u+2v⟩.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(2u-v),\,\frac{∂}{∂u}(3u+2),\,\frac{∂}{∂u}(u+2v)⟩ \\  & =⟨2,\,3,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(2u-v),\,\frac{∂}{∂v}(3u+2),\,\frac{∂}{∂v}(u+2v)⟩ \\  & =⟨-1,\,0,\,2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2 & 3 & 1 \\ -1 & 0 & 2\end{aligned}| \\  & =⟨|\begin{aligned}3 & 1 \\ 0 & 2\end{aligned}|,\,-|\begin{aligned}2 & 1 \\ -1 & 2\end{aligned}|,\,|\begin{aligned}2 & 3 \\ -1 & 0\end{aligned}|⟩ \\  & =⟨6,\,-5,\,3⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨6,\,-5,\,3⟩‖ \\  & =\sqrt{{6}^{2}+(-5)^{2}+{3}^{2}} \\  & =\sqrt{36+25+9} \\  & =\sqrt{70}.\end{aligned}
$$

Next, let's denote

$$
D={(u,v)\,:\,0\le u\le 1,\,-1\le v\le 1}.
$$

Then, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\sqrt{70}\,\text{d}A \\  & =\sqrt{70}{∬}_{D}\text{ }\,\text{d}A \\  & =\sqrt{70}\cdot \text{Area}(D) \\  & =\sqrt{70}\cdot 1\cdot 2 \\  & =2\sqrt{70}.\end{aligned}
$$

Changed domain; identical surface

Find the surface area of the parametric surface defined by the equations 

$$
x=2u-v,\,y=3u+2,\,z=u+2v
$$

for $0\le u\le 2$ and $-1\le v\le 1.$

- [x] $4 \sqrt{70}$
- [ ] $40$
- [ ] $2 \sqrt{30}$
- [ ] $20$
- [ ] $2 \sqrt{35}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

In vector form, our surface has the equation 

$$
r(u,v)=⟨2u-v,\,3u+2,\,u+2v⟩.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(2u-v),\,\frac{∂}{∂u}(3u+2),\,\frac{∂}{∂u}(u+2v)⟩ \\  & =⟨2,\,3,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(2u-v),\,\frac{∂}{∂v}(3u+2),\,\frac{∂}{∂v}(u+2v)⟩ \\  & =⟨-1,\,0,\,2⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2 & 3 & 1 \\ -1 & 0 & 2\end{aligned}| \\  & =⟨|\begin{aligned}3 & 1 \\ 0 & 2\end{aligned}|,\,-|\begin{aligned}2 & 1 \\ -1 & 2\end{aligned}|,\,|\begin{aligned}2 & 3 \\ -1 & 0\end{aligned}|⟩ \\  & =⟨6,\,-5,\,3⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨6,\,-5,\,3⟩‖ \\  & =\sqrt{{6}^{2}+(-5)^{2}+{3}^{2}} \\  & =\sqrt{36+25+9} \\  & =\sqrt{70}.\end{aligned}
$$

Next, let's denote

$$
D={(u,v)\,:\,0\le u\le 2,\,-1\le v\le 1}.
$$

Then, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\sqrt{70}\,\text{d}A \\  & =\sqrt{70}{∬}_{D}\text{ }\,\text{d}A \\  & =\sqrt{70}\cdot \text{Area}(D) \\  & =\sqrt{70}\cdot 2\cdot 2 \\  & =4 \sqrt{70}.\end{aligned}
$$

## q-105922

Source

Find the surface area of the part of the parametric surface $r(u,v)=⟨-u+v,\,u-2v,\,3v⟩$ that is subject to the constraint ${u}^{2}+{v}^{2}\le 4.$

- [ ] $2\pi \sqrt{57}$
- [ ] $\pi \sqrt{19}$
- [x] $4\pi \sqrt{19}$
- [ ] $\pi \sqrt{38}$
- [ ] $2\pi \sqrt{38}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(-u+v),\,\frac{∂}{∂u}(u-2v),\,\frac{∂}{∂u}(3v)⟩ \\  & =⟨-1,\,1,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(-u+v),\,\frac{∂}{∂v}(u-2v),\,\frac{∂}{∂v}(3v)⟩ \\  & =⟨1,\,-2,\,3⟩\end{aligned}
$$

Therefore, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ -1 & 1 & 0 \\ 1 & -2 & 3\end{aligned}| \\  & =⟨|\begin{aligned}1 & 0 \\ -2 & 3\end{aligned}|,\,-|\begin{aligned}-1 & 0 \\ 1 & 3\end{aligned}|,\,|\begin{aligned}-1 & 1 \\ 1 & -2\end{aligned}|⟩ \\  & =⟨3,\,3,\,1⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨3,\,3,\,1⟩‖ \\  & =\sqrt{{3}^{2}+{3}^{2}+{1}^{2}} \\  & =\sqrt{9+9+1} \\  & =\sqrt{19}.\end{aligned}
$$

Next, notice that the region ${u}^{2}+{v}^{2}\le 4$ corresponds to the disk

$$
D={(u,v)\,:\,{u}^{2}+{v}^{2}\le 4},
$$

of radius $2.$

Therefore, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\sqrt{19}\,\text{d}A \\  & =\sqrt{19}{∬}_{D}\text{d}A \\  & =\sqrt{19}\cdot \text{Area}(D) \\  & =\sqrt{19}\cdot (\pi \cdot {2}^{2}) \\  & =4\pi \sqrt{19}.\end{aligned}
$$

Changed domain; identical surface

Find the surface area of the part of the parametric surface $r(u,v)=⟨-u+v,\,u-2v,\,3v⟩$ that is subject to the constraint ${u}^{2}+{v}^{2}\le 8.$

- [ ] $4 \sqrt{57} \pi$
- [ ] $2 \sqrt{19} \pi$
- [x] $8 \sqrt{19} \pi$
- [ ] $2 \sqrt{38} \pi$
- [ ] $4 \sqrt{38} \pi$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(-u+v),\,\frac{∂}{∂u}(u-2v),\,\frac{∂}{∂u}(3v)⟩ \\  & =⟨-1,\,1,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(-u+v),\,\frac{∂}{∂v}(u-2v),\,\frac{∂}{∂v}(3v)⟩ \\  & =⟨1,\,-2,\,3⟩\end{aligned}
$$

Therefore, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ -1 & 1 & 0 \\ 1 & -2 & 3\end{aligned}| \\  & =⟨|\begin{aligned}1 & 0 \\ -2 & 3\end{aligned}|,\,-|\begin{aligned}-1 & 0 \\ 1 & 3\end{aligned}|,\,|\begin{aligned}-1 & 1 \\ 1 & -2\end{aligned}|⟩ \\  & =⟨3,\,3,\,1⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨3,\,3,\,1⟩‖ \\  & =\sqrt{{3}^{2}+{3}^{2}+{1}^{2}} \\  & =\sqrt{9+9+1} \\  & =\sqrt{19}.\end{aligned}
$$

Next, notice that the region ${u}^{2}+{v}^{2}\le 8$ corresponds to the disk

$$
D={(u,v)\,:\,{u}^{2}+{v}^{2}\le 8},
$$

of radius $2 \sqrt{2}.$

Therefore, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\sqrt{19}\,\text{d}A \\  & =\sqrt{19}{∬}_{D}\text{d}A \\  & =\sqrt{19}\cdot \text{Area}(D) \\  & =\sqrt{19}\cdot (\pi \cdot (2 \sqrt{2})^{2}) \\  & =8 \sqrt{19} \pi.\end{aligned}
$$

## q-109710

Source

Find the surface area of the parametric surface defined by the equations 

$$
x=u+v,\,y=2-3u,\,z=1+u-v
$$

for $0\le u\le 2$ and $-1\le v\le 1.$

- [ ] $5\sqrt{10}$
- [ ] $6\sqrt{2}$
- [x] $4\sqrt{22}$
- [ ] $3\sqrt{14}$
- [ ] $8\sqrt{11}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

In vector form, our surface has the equation 

$$
r(u,v)=⟨u+v,\,2-3u,\,1+u-v⟩.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u+v),\,\frac{∂}{∂u}(2-3u),\,\frac{∂}{∂u}(1+u-v)⟩ \\  & =⟨1,\,-3,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u+v),\,\frac{∂}{∂v}(2-3u),\,\frac{∂}{∂v}(1+u-v)⟩ \\  & =⟨1,\,0,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & -3 & 1 \\ 1 & 0 & -1\end{aligned}| \\  & =⟨|\begin{aligned}-3 & 1 \\ 0 & -1\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 1 & -1\end{aligned}|,\,|\begin{aligned}1 & -3 \\ 1 & 0\end{aligned}|⟩ \\  & =⟨3,\,2,\,3⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨3,\,2,\,3⟩‖ \\  & =\sqrt{{3}^{2}+{2}^{2}+{3}^{2}} \\  & =\sqrt{9+4+9} \\  & =\sqrt{22}.\end{aligned}
$$

Next, let's denote

$$
D={(u,v)\,:\,0\le u\le 2,\,-1\le v\le 1}.
$$

Then, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\sqrt{22}\,\text{d}A \\  & =\sqrt{22}{∬}_{D}\text{d}A \\  & =\sqrt{22}\cdot \text{Area}(D) \\  & =\sqrt{22}\cdot 2\cdot 2 \\  & =4\sqrt{22}.\end{aligned}
$$

Changed domain; identical surface

Find the surface area of the parametric surface defined by the equations 

$$
x=u+v,\,y=2-3u,\,z=1+u-v
$$

for $0\le u\le 4$ and $-1\le v\le 1.$

- [ ] $10 \sqrt{10}$
- [ ] $12 \sqrt{2}$
- [x] $8 \sqrt{22}$
- [ ] $6 \sqrt{14}$
- [ ] $16 \sqrt{11}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

In vector form, our surface has the equation 

$$
r(u,v)=⟨u+v,\,2-3u,\,1+u-v⟩.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u+v),\,\frac{∂}{∂u}(2-3u),\,\frac{∂}{∂u}(1+u-v)⟩ \\  & =⟨1,\,-3,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u+v),\,\frac{∂}{∂v}(2-3u),\,\frac{∂}{∂v}(1+u-v)⟩ \\  & =⟨1,\,0,\,-1⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & -3 & 1 \\ 1 & 0 & -1\end{aligned}| \\  & =⟨|\begin{aligned}-3 & 1 \\ 0 & -1\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 1 & -1\end{aligned}|,\,|\begin{aligned}1 & -3 \\ 1 & 0\end{aligned}|⟩ \\  & =⟨3,\,2,\,3⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨3,\,2,\,3⟩‖ \\  & =\sqrt{{3}^{2}+{2}^{2}+{3}^{2}} \\  & =\sqrt{9+4+9} \\  & =\sqrt{22}.\end{aligned}
$$

Next, let's denote

$$
D={(u,v)\,:\,0\le u\le 4,\,-1\le v\le 1}.
$$

Then, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\sqrt{22}\,\text{d}A \\  & =\sqrt{22}{∬}_{D}\text{ }\,\text{d}A \\  & =\sqrt{22}\cdot \text{Area}(D) \\  & =\sqrt{22}\cdot 4\cdot 2 \\  & =8 \sqrt{22}.\end{aligned}
$$

## q-109712

Source

Find the surface area of the parametric surface defined by the equations 

$$
x=u,\,y={v}^{2},\,z=\frac{2}{3}{v}^{3}
$$

for $0\le u\le 1$ and $0\le v\le \sqrt{3}.$

- [x] $\frac{14}{3}$
- [ ] $\frac{5}{3}$
- [ ] $\frac{7}{2}$
- [ ] $\frac{19}{6}$
- [ ] $\frac{9}{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

In vector form, our surface has the equation 

$$
r(u,v)=⟨u,\,{v}^{2},\,\frac{2}{3}{v}^{3}⟩.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}({v}^{2}),\,\frac{∂}{∂u}(\frac{2}{3}{v}^{3})⟩ \\  & =⟨1,\,0,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}({v}^{2}),\,\frac{∂}{∂v}(\frac{2}{3}{v}^{3})⟩ \\  & =⟨0,\,2v,\,2{v}^{2}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 0 \\ 0 & 2v & 2{v}^{2}\end{aligned}| \\  & =⟨|\begin{aligned}0 & 0 \\ 2v & 2{v}^{2}\end{aligned}|,\,-|\begin{aligned}1 & 0 \\ 0 & 2{v}^{2}\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 2v\end{aligned}|⟩ \\  & =⟨0,\,-2{v}^{2},\,2v⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨0,\,-2{v}^{2},\,2v⟩‖ \\  & =\sqrt{{0}^{2}+(-2{v}^{2})^{2}+(2v)^{2}} \\  & =\sqrt{4{v}^{4}+4{v}^{2}} \\  & =\sqrt{4{v}^{2}({v}^{2}+1)} \\  & =2v\sqrt{{v}^{2}+1}.\end{aligned}
$$

Notice that $\sqrt{{v}^{2}}=v$ since $v\ge 0$ on $D.$

Next, let's denote

$$
D={(u,v)\,:\,0\le u\le 1,\,0\le v\le \sqrt{3}}.
$$

Then, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}2v\sqrt{{v}^{2}+1}\,\text{d}A \\  & ={\int }_{0}^{\sqrt{3}}{\int }_{0}^{1}2v\sqrt{{v}^{2}+1}\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{\sqrt{3}}2v\sqrt{{v}^{2}+1}{\int }_{0}^{1}\text{d}u\,\text{d}v \\  & ={\int }_{0}^{\sqrt{3}}2v\sqrt{{v}^{2}+1}\,\text{d}v\end{aligned}
$$

Finally, using the substitution 

$$
w={v}^{2}+1\,⇒\,\text{d}w=2v\,\text{d}v,
$$

we get

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={\int }_{0}^{\sqrt{3}}2v\sqrt{{v}^{2}+1}\,\text{d}v \\  & ={\int }_{1}^{4}\sqrt{w}\,\text{d}w \\  & ={[\frac{2}{3}\sqrt{{w}^{3}}]}_{1}^{4} \\  & =\frac{2}{3}[\sqrt{{4}^{3}}-\sqrt{{1}^{3}}] \\  & =\frac{2}{3}(8-1) \\  & =\frac{14}{3}.\end{aligned}
$$

Changed domain; identical surface

Find the surface area of the parametric surface defined by the equations 

$$
x=u,\,y={v}^{2},\,z=\frac{2}{3}{v}^{3}
$$

for $0\le u\le 2$ and $0\le v\le \sqrt{3}.$

- [x] $\frac{28}{3}$
- [ ] $\frac{10}{3}$
- [ ] $7$
- [ ] $\frac{19}{3}$
- [ ] $9$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

In vector form, our surface has the equation 

$$
r(u,v)=⟨u,\,{v}^{2},\,\frac{2}{3}{v}^{3}⟩.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}({v}^{2}),\,\frac{∂}{∂u}(\frac{2}{3}{v}^{3})⟩ \\  & =⟨1,\,0,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}({v}^{2}),\,\frac{∂}{∂v}(\frac{2}{3}{v}^{3})⟩ \\  & =⟨0,\,2v,\,2{v}^{2}⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 0 \\ 0 & 2v & 2{v}^{2}\end{aligned}| \\  & =⟨|\begin{aligned}0 & 0 \\ 2v & 2{v}^{2}\end{aligned}|,\,-|\begin{aligned}1 & 0 \\ 0 & 2{v}^{2}\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 2v\end{aligned}|⟩ \\  & =⟨0,\,-2{v}^{2},\,2v⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨0,\,-2{v}^{2},\,2v⟩‖ \\  & =\sqrt{{0}^{2}+(-2{v}^{2})^{2}+(2v)^{2}} \\  & =\sqrt{4{v}^{4}+4{v}^{2}} \\  & =\sqrt{4{v}^{2}({v}^{2}+1)} \\  & =2v\sqrt{{v}^{2}+1}.\end{aligned}
$$

Notice that $\sqrt{{v}^{2}}=v$ since $v\ge 0$ on $D.$

Next, let's denote

$$
D={(u,v)\,:\,0\le u\le 2,\,0\le v\le \sqrt{3}}.
$$

Then, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}2v\sqrt{{v}^{2}+1}\,\text{d}A \\  & ={\int }_{0}^{\sqrt{3}}{\int }_{0}^{2}2v\sqrt{{v}^{2}+1}\,\text{d}u\,\text{d}v \\  & ={\int }_{0}^{\sqrt{3}}2v\sqrt{{v}^{2}+1}{\int }_{0}^{2}\text{d}u\,\text{d}v \\  & =2{\int }_{0}^{\sqrt{3}}2v\sqrt{{v}^{2}+1}\,\text{d}v\end{aligned}
$$

Finally, using the substitution 

$$
w={v}^{2}+1\,⇒\,\text{d}w=2v\,\text{d}v,
$$

we get

$$
\begin{aligned}{∬}_{S}\,\text{d}S & =2{\int }_{0}^{\sqrt{3}}2v\sqrt{{v}^{2}+1}\,\text{d}v \\  & =2{\int }_{1}^{4}\sqrt{w}\,\text{d}w \\  & =2{[\frac{2}{3}\sqrt{{w}^{3}}]}_{1}^{4} \\  & =2\cdot \frac{2}{3}[\sqrt{{4}^{3}}-\sqrt{{1}^{3}}] \\  & =2\cdot \frac{2}{3}(8-1) \\  & =\frac{28}{3}.\end{aligned}
$$

## q-109761

Source

Find the surface area of the parametric surface defined by the equations 

$$
x={u}^{2},\,y=uv,\,z=\frac{1}{2}{v}^{2}
$$

for $0\le u\le 1$ and $1\le v\le 2.$

- [ ] $\frac{10}{3}$
- [x] $3$
- [ ] $5$
- [ ] $\frac{7}{2}$
- [ ] $10$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

In vector form, our surface has the equation 

$$
r(u,v)=⟨{u}^{2},\,uv,\,\frac{1}{2}{v}^{2}⟩.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}({u}^{2}),\,\frac{∂}{∂u}(uv),\,\frac{∂}{∂u}(\frac{1}{2}{v}^{2})⟩ \\  & =⟨2u,\,v,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}({u}^{2}),\,\frac{∂}{∂v}(uv),\,\frac{∂}{∂v}(\frac{1}{2}{v}^{2})⟩ \\  & =⟨0,\,u,\,v⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2u & v & 0 \\ 0 & u & v\end{aligned}| \\  & =⟨|\begin{aligned}v & 0 \\ u & v\end{aligned}|,\,-|\begin{aligned}2u & 0 \\ 0 & v\end{aligned}|,\,|\begin{aligned}2u & v \\ 0 & u\end{aligned}|⟩ \\  & =⟨{v}^{2},\,-2uv,\,2{u}^{2}⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨{v}^{2},\,-2uv,\,2{u}^{2}⟩‖ \\  & =\sqrt{({v}^{2})^{2}+(-2uv)^{2}+(2{u}^{2})^{2}} \\  & =\sqrt{{v}^{4}+4{u}^{2}{v}^{2}+4{u}^{4}} \\  & =\sqrt{({v}^{2}+2{u}^{2})^{2}} \\  & ={v}^{2}+2{u}^{2}.\end{aligned}
$$

Next, let's denote

$$
D={(u,v)\,:\,0\le u\le 1,\,1\le v\le 2}.
$$

Then, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}({v}^{2}+2{u}^{2})\,\text{d}A \\  & ={\int }_{1}^{2}{\int }_{0}^{1}({v}^{2}+2{u}^{2})\,\text{d}u\,\text{d}v \\  & ={\int }_{1}^{2}{[u{v}^{2}+\frac{2}{3}{u}^{3}]}_{0}^{1}\text{d}v \\  & ={\int }_{1}^{2}({v}^{2}+\frac{2}{3})\text{d}v \\  & ={[\frac{1}{3}{v}^{3}+\frac{2}{3}v]}_{1}^{2} \\  & =\frac{1}{3}[{2}^{3}+2(2)-({1}^{3}+2(1))] \\  & =\frac{1}{3}(9) \\  & =3.\end{aligned}
$$

Changed domain; identical surface

Find the surface area of the parametric surface defined by the equations 

$$
x={u}^{2},\,y=uv,\,z=\frac{1}{2}{v}^{2}
$$

for $0\le u\le 2$ and $2\le v\le 4.$

- [ ] $\frac{160}{3}$
- [x] $48$
- [ ] $80$
- [ ] $56$
- [ ] $160$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

In vector form, our surface has the equation 

$$
r(u,v)=⟨{u}^{2},\,uv,\,\frac{1}{2}{v}^{2}⟩.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}({u}^{2}),\,\frac{∂}{∂u}(uv),\,\frac{∂}{∂u}(\frac{1}{2}{v}^{2})⟩ \\  & =⟨2u,\,v,\,0⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}({u}^{2}),\,\frac{∂}{∂v}(uv),\,\frac{∂}{∂v}(\frac{1}{2}{v}^{2})⟩ \\  & =⟨0,\,u,\,v⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 2u & v & 0 \\ 0 & u & v\end{aligned}| \\  & =⟨|\begin{aligned}v & 0 \\ u & v\end{aligned}|,\,-|\begin{aligned}2u & 0 \\ 0 & v\end{aligned}|,\,|\begin{aligned}2u & v \\ 0 & u\end{aligned}|⟩ \\  & =⟨{v}^{2},\,-2uv,\,2{u}^{2}⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨{v}^{2},\,-2uv,\,2{u}^{2}⟩‖ \\  & =\sqrt{({v}^{2})^{2}+(-2uv)^{2}+(2{u}^{2})^{2}} \\  & =\sqrt{{v}^{4}+4{u}^{2}{v}^{2}+4{u}^{4}} \\  & =\sqrt{({v}^{2}+2{u}^{2})^{2}} \\  & ={v}^{2}+2{u}^{2}.\end{aligned}
$$

Next, let's denote

$$
D={(u,v)\,:\,0\le u\le 2,\,2\le v\le 4}.
$$

Then, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}({v}^{2}+2{u}^{2})\,\text{d}A \\  & ={\int }_{2}^{4}{\int }_{0}^{2}({v}^{2}+2{u}^{2})\,\text{d}u\,\text{d}v \\  & ={\int }_{2}^{4}{[u{v}^{2}+\frac{2}{3}{u}^{3}]}_{0}^{2}\text{d}v \\  & ={\int }_{2}^{4}(2{v}^{2}+\frac{16}{3})\text{d}v \\  & ={[\frac{2}{3}{v}^{3}+\frac{16}{3}v]}_{2}^{4} \\  & =\frac{2}{3}[{4}^{3}-{2}^{3}]+(\frac{16}{3})(4-2) \\  & =48 \\  & =48.\end{aligned}
$$

## q-109779

Source

Find the surface area of the part of the parametric surface $r(u,v)=⟨u,\,v,\,u-v⟩$ that is subject to the constraint ${u}^{2}+{v}^{2}\le 9.$

- [ ] $2\sqrt{3}$
- [ ] $\pi \sqrt{3}$
- [ ] $9\pi \sqrt{2}$
- [x] $9\pi \sqrt{3}$
- [ ] $\pi \sqrt{2}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u-v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u-v)⟩ \\  & =⟨0,\,1,\,-1⟩\end{aligned}
$$

Therefore, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & -1\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & -1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,1,\,1⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨-1,\,1,\,1⟩‖ \\  & =\sqrt{(-1)^{2}+{1}^{2}+{1}^{2}} \\  & =\sqrt{1+1+1} \\  & =\sqrt{3}.\end{aligned}
$$

Next, notice that the region ${u}^{2}+{v}^{2}\le 9$ corresponds to the disk

$$
D={(u,v)\,:\,{u}^{2}+{v}^{2}\le 9},
$$

of radius $3.$

Therefore, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\sqrt{3}\,\text{d}A \\  & =\sqrt{3}{∬}_{D}\text{d}A \\  & =\sqrt{3}\cdot \text{Area}(D) \\  & =\sqrt{3}\cdot (\pi \cdot {3}^{2}) \\  & =9\pi \sqrt{3}.\end{aligned}
$$

Changed domain; identical surface

Find the surface area of the part of the parametric surface $r(u,v)=⟨u,\,v,\,u-v⟩$ that is subject to the constraint ${u}^{2}+{v}^{2}\le 18.$

- [ ] $4 \sqrt{3}$
- [ ] $2 \sqrt{3} \pi$
- [ ] $18 \sqrt{2} \pi$
- [x] $18 \sqrt{3} \pi$
- [ ] $2 \sqrt{2} \pi$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(u-v)⟩ \\  & =⟨1,\,0,\,1⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(u-v)⟩ \\  & =⟨0,\,1,\,-1⟩\end{aligned}
$$

Therefore, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & 1 \\ 0 & 1 & -1\end{aligned}| \\  & =⟨|\begin{aligned}0 & 1 \\ 1 & -1\end{aligned}|,\,-|\begin{aligned}1 & 1 \\ 0 & -1\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨-1,\,1,\,1⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨-1,\,1,\,1⟩‖ \\  & =\sqrt{(-1)^{2}+{1}^{2}+{1}^{2}} \\  & =\sqrt{1+1+1} \\  & =\sqrt{3}.\end{aligned}
$$

Next, notice that the region ${u}^{2}+{v}^{2}\le 18$ corresponds to the disk

$$
D={(u,v)\,:\,{u}^{2}+{v}^{2}\le 18},
$$

of radius $3 \sqrt{2}.$

Therefore, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\sqrt{3}\,\text{d}A \\  & =\sqrt{3}{∬}_{D}\text{d}A \\  & =\sqrt{3}\cdot \text{Area}(D) \\  & =\sqrt{3}\cdot (\pi \cdot (3 \sqrt{2})^{2}) \\  & =18 \sqrt{3} \pi.\end{aligned}
$$

## q-110252

Source

Find the surface area of the part of the parametric surface $r(u,v)=⟨u,\,v,\,1-2u+5v⟩$ that is subject to the constraint ${u}^{2}+{v}^{2}\le 2.$

- [ ] $\pi \sqrt{20}$
- [ ] $2\pi \sqrt{10}$
- [ ] $3\pi \sqrt{5}$
- [ ] $\pi \sqrt{15}$
- [x] $2\pi \sqrt{30}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(1-2u+5v)⟩ \\  & =⟨1,\,0,\,-2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(1-2u+5v)⟩ \\  & =⟨0,\,1,\,5⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -2 \\ 0 & 1 & 5\end{aligned}| \\  & =⟨|\begin{aligned}0 & -2 \\ 1 & 5\end{aligned}|,\,-|\begin{aligned}1 & -2 \\ 0 & 5\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨2,\,-5,\,1⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨2,\,-5,\,1⟩‖ \\  & =\sqrt{{(2)}^{2}+{(-5)}^{2}+(1)^{2}} \\  & =\sqrt{4+25+1} \\  & =\sqrt{30}.\end{aligned}
$$

Next, notice that the region ${u}^{2}+{v}^{2}\le 2$ corresponds to the disk

$$
D={(u,v)\,:\,{u}^{2}+{v}^{2}\le 2}
$$

of radius $\sqrt{2}.$

Therefore, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\sqrt{30}\,\text{d}A \\  & =\sqrt{30}{∬}_{D}\text{d}A \\  & =\sqrt{30}\cdot \text{Area}(D) \\  & =\sqrt{30}\cdot (\pi \cdot (\sqrt{2})^{2}) \\  & =2\pi \sqrt{30}.\end{aligned}
$$

Changed domain; identical surface

Find the surface area of the part of the parametric surface $r(u,v)=⟨u,\,v,\,1-2u+5v⟩$ that is subject to the constraint ${u}^{2}+{v}^{2}\le 4.$

- [ ] $4 \sqrt{5} \pi$
- [ ] $4 \sqrt{10} \pi$
- [ ] $6 \sqrt{5} \pi$
- [ ] $2 \sqrt{15} \pi$
- [x] $4 \sqrt{30} \pi$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u),\,\frac{∂}{∂u}(v),\,\frac{∂}{∂u}(1-2u+5v)⟩ \\  & =⟨1,\,0,\,-2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u),\,\frac{∂}{∂v}(v),\,\frac{∂}{∂v}(1-2u+5v)⟩ \\  & =⟨0,\,1,\,5⟩\end{aligned}
$$

Now, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 0 & -2 \\ 0 & 1 & 5\end{aligned}| \\  & =⟨|\begin{aligned}0 & -2 \\ 1 & 5\end{aligned}|,\,-|\begin{aligned}1 & -2 \\ 0 & 5\end{aligned}|,\,|\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}|⟩ \\  & =⟨2,\,-5,\,1⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨2,\,-5,\,1⟩‖ \\  & =\sqrt{{(2)}^{2}+{(-5)}^{2}+(1)^{2}} \\  & =\sqrt{4+25+1} \\  & =\sqrt{30}.\end{aligned}
$$

Next, notice that the region ${u}^{2}+{v}^{2}\le 4$ corresponds to the disk

$$
D={(u,v)\,:\,{u}^{2}+{v}^{2}\le 4}
$$

of radius $2.$

Therefore, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\sqrt{30}\,\text{d}A \\  & =\sqrt{30}{∬}_{D}\text{d}A \\  & =\sqrt{30}\cdot \text{Area}(D) \\  & =\sqrt{30}\cdot (\pi \cdot (2)^{2}) \\  & =4 \sqrt{30} \pi.\end{aligned}
$$

## q-110551

Source

Find the surface area of the part of the parametric surface $r(u,v)=⟨u-v,\,u+2v,\,2u-v⟩$ that is subject to the constraint ${u}^{2}+{v}^{2}\le 1.$

- [ ] $\pi \sqrt{17}$
- [x] $\pi \sqrt{35}$
- [ ] $\pi \sqrt{15}$
- [ ] $6\pi \sqrt{2}$
- [ ] $2\pi \sqrt{11}$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u-v),\,\frac{∂}{∂u}(u+2v),\,\frac{∂}{∂u}(2u-v)⟩ \\  & =⟨1,\,1,\,2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u-v),\,\frac{∂}{∂v}(u+2v),\,\frac{∂}{∂v}(2u-v)⟩ \\  & =⟨-1,\,2,\,-1⟩\end{aligned}
$$

Therefore, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 1 & 2 \\ -1 & 2 & -1\end{aligned}| \\  & =⟨|\begin{aligned}1 & 2 \\ 2 & -1\end{aligned}|,\,-|\begin{aligned}1 & 2 \\ -1 & -1\end{aligned}|,\,|\begin{aligned}1 & 1 \\ -1 & 2\end{aligned}|⟩ \\  & =⟨-5,\,-1,\,3⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨-5,\,-1,\,3⟩‖ \\  & =\sqrt{(-5)^{2}+(-1)^{2}+{3}^{2}} \\  & =\sqrt{25+1+9} \\  & =\sqrt{35}.\end{aligned}
$$

Next, notice that the region ${u}^{2}+{v}^{2}\le 1$ corresponds to the disk

$$
D={(u,v)\,:\,{u}^{2}+{v}^{2}\le 1},
$$

of radius $1.$

Therefore, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\sqrt{35}\,\text{d}A \\  & =\sqrt{35}{∬}_{D}\text{d}A \\  & =\sqrt{35}\cdot \text{Area}(D) \\  & =\sqrt{35}\cdot (\pi \cdot {1}^{2}) \\  & =\pi \sqrt{35}.\end{aligned}
$$

Changed domain; identical surface

Find the surface area of the part of the parametric surface $r(u,v)=⟨u-v,\,u+2v,\,2u-v⟩$ that is subject to the constraint ${u}^{2}+{v}^{2}\le 2.$

- [ ] $2 \sqrt{17} \pi$
- [x] $2 \sqrt{35} \pi$
- [ ] $2 \sqrt{15} \pi$
- [ ] $12 \sqrt{2} \pi$
- [ ] $4 \sqrt{11} \pi$

For a surface $S$ with parametrization $r(u,v)$ for $(u,v)\in D,$ the surface area of $S$ is given by

$$
{∬}_{S}\,\text{d}S={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A.
$$

We first compute the tangent vectors to the grid curves:

$$
\begin{aligned}{r}_{u}^{′} & =⟨\frac{∂x}{∂u},\,\frac{∂y}{∂u},\,\frac{∂z}{∂u}⟩ \\  & =⟨\frac{∂}{∂u}(u-v),\,\frac{∂}{∂u}(u+2v),\,\frac{∂}{∂u}(2u-v)⟩ \\  & =⟨1,\,1,\,2⟩ \\ {r}_{v}^{′} & =⟨\frac{∂x}{∂v},\,\frac{∂y}{∂v},\,\frac{∂z}{∂v}⟩ \\  & =⟨\frac{∂}{∂v}(u-v),\,\frac{∂}{∂v}(u+2v),\,\frac{∂}{∂v}(2u-v)⟩ \\  & =⟨-1,\,2,\,-1⟩\end{aligned}
$$

Therefore, the fundamental vector product is

$$
\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & =|\begin{aligned}i & j & k \\ 1 & 1 & 2 \\ -1 & 2 & -1\end{aligned}| \\  & =⟨|\begin{aligned}1 & 2 \\ 2 & -1\end{aligned}|,\,-|\begin{aligned}1 & 2 \\ -1 & -1\end{aligned}|,\,|\begin{aligned}1 & 1 \\ -1 & 2\end{aligned}|⟩ \\  & =⟨-5,\,-1,\,3⟩,\end{aligned}
$$

and 

$$
\begin{aligned}‖{r}_{u}^{′}\times {r}_{v}^{′}‖ & =‖⟨-5,\,-1,\,3⟩‖ \\  & =\sqrt{(-5)^{2}+(-1)^{2}+{3}^{2}} \\  & =\sqrt{25+1+9} \\  & =\sqrt{35}.\end{aligned}
$$

Next, notice that the region ${u}^{2}+{v}^{2}\le 2$ corresponds to the disk

$$
D={(u,v)\,:\,{u}^{2}+{v}^{2}\le 2},
$$

of radius $\sqrt{2}.$

Therefore, the surface area is

$$
\begin{aligned}{∬}_{S}\,\text{d}S & ={∬}_{D}‖{r}_{u}^{′}\times {r}_{v}^{′}‖\text{d}A \\  & ={∬}_{D}\sqrt{35}\,\text{d}A \\  & =\sqrt{35}{∬}_{D}\text{d}A \\  & =\sqrt{35}\cdot \text{Area}(D) \\  & =\sqrt{35}\cdot (\pi \cdot (\sqrt{2})^{2}) \\  & =2 \sqrt{35} \pi.\end{aligned}
$$
